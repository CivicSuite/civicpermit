"""FastAPI runtime foundation for CivicPermit."""

import os
from typing import Annotated

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from civicpermit import __version__
from civicpermit.intake_review import review_intake_readiness
from civicpermit.persistence import PermitIntakeRepository, StoredIntakeReview
from civicpermit.public_ui import render_public_lookup_page
from civicpermit.records_export import build_policy_export
from civicpermit.requirement_lookup import lookup_permit_requirement
from civicpermit.submittal_outline import draft_submittal_outline


app = FastAPI(
    title="CivicPermit",
    version=__version__,
    description="Permit pre-application and development-review intake support for CivicSuite.",
)

_intake_repository: PermitIntakeRepository | None = None
_intake_db_url: str | None = None


class RequirementLookupRequest(BaseModel):
    project_type: str = Field(min_length=1, max_length=255)
    location_context: str = Field(default="", max_length=500)


class IntakeReviewRequest(BaseModel):
    proposal: str = Field(min_length=1, max_length=5000)
    project_type: str = Field(min_length=1, max_length=255)


class DevelopmentReviewContextRequest(BaseModel):
    project_type: str = Field(min_length=1, max_length=255)
    proposal: str = Field(min_length=1, max_length=5000)
    location_context: str = Field(default="", max_length=500)
    zoning_context_id: str | None = Field(default=None, max_length=160)
    code_context_id: str | None = Field(default=None, max_length=160)
    zoning_context_summary: str | None = Field(default=None, max_length=1000)
    code_context_summary: str | None = Field(default=None, max_length=1000)


class SubmittalOutlineRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=500)
    proposal: str = Field(min_length=1, max_length=5000)
    project_type: str = Field(min_length=1, max_length=255)


class PermitExportRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    project_type: str = Field(min_length=1, max_length=255)
    format: str = Field(default="markdown", min_length=1, max_length=40)


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicPermit",
        "version": __version__,
        "status": "permit intake foundation plus intake persistence and CivicCore v1 alignment",
        "message": (
            "CivicPermit package, API foundation, sample permit requirement lookup, optional database-backed requirement and intake records, intake-readiness review, submittal outline helper, records-ready export checklist, and public UI foundation are online; "
            "permit approvals, official completeness determinations, fee calculations, inspections, live GIS, live LLM calls, and permitting-system-of-record integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.2 roadmap: local permit type configuration, CivicZone/CivicCode runtime consumption, and staff review queues",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civicpermit",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    fields = sorted(
        {
            ".".join(str(part) for part in error.get("loc", [])[1:])
            for error in exc.errors()
            if len(error.get("loc", [])) > 1
        }
    )
    field_list = ", ".join(fields) if fields else "request body"
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "message": f"CivicPermit could not validate: {field_list}.",
                "fix": (
                    "Send a JSON body that includes the required field names listed in "
                    "the fields array, using strings for text inputs."
                ),
                "fields": fields,
            }
        },
    )


@app.get("/civicpermit", response_class=HTMLResponse)
def public_civicpermit_page() -> str:
    """Return the public sample permit pre-application UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civicpermit/requirements/lookup")
def requirement_lookup(request: RequirementLookupRequest) -> dict[str, object]:
    result = _lookup_permit_requirement(
        project_type=request.project_type,
        location_context=request.location_context,
    )
    return result.__dict__


@app.post("/api/v1/civicpermit/intake/review")
def intake_review(
    request: IntakeReviewRequest,
    x_civicpermit_role: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _intake_database_url() is not None:
        _require_staff_role(x_civicpermit_role)
        stored = _get_intake_repository().create_intake_review(
            proposal=request.proposal,
            project_type=request.project_type,
        )
        return _stored_intake_response(stored)

    result = review_intake_readiness(proposal=request.proposal, project_type=request.project_type)
    payload = result.__dict__
    payload["intake_id"] = None
    return payload


@app.post("/api/v1/civicpermit/context/development-review")
def development_review_context(request: DevelopmentReviewContextRequest) -> dict[str, object]:
    requirement, source = _lookup_permit_requirement_with_source(
        project_type=request.project_type,
        location_context=request.location_context,
    )
    readiness = review_intake_readiness(
        proposal=request.proposal,
        project_type=request.project_type,
    )
    citations = [requirement.citation]
    if request.zoning_context_id:
        citations.append(f"CivicZone context: {request.zoning_context_id}")
    if request.code_context_id:
        citations.append(f"CivicCode context: {request.code_context_id}")
    return {
        "requirement_id": requirement.requirement_id,
        "project_type": requirement.project_type,
        "required_materials": list(requirement.required_materials),
        "zoning_context_id": request.zoning_context_id,
        "code_context_id": request.code_context_id,
        "citations": citations,
        "missing_or_unclear": list(readiness.missing_or_unclear),
        "review_required": True,
        "source": source,
        "boundary": (
            "CivicPermit provides pre-application intake context only; it is not a "
            "permit approval, official completeness determination, fee calculation, "
            "inspection result, or system-of-record action."
        ),
    }


@app.get("/api/v1/civicpermit/intake/{intake_id}")
def get_intake_review(
    intake_id: str,
    x_civicpermit_role: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _intake_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicPermit intake persistence is not configured.",
                "fix": "Set CIVICPERMIT_INTAKE_DB_URL to retrieve persisted intake review records.",
            },
        )
    _require_staff_role(x_civicpermit_role)
    stored = _get_intake_repository().get_intake_review(intake_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Permit intake record not found.",
                "fix": "Use an intake_id returned by POST /api/v1/civicpermit/intake/review.",
            },
        )
    return _stored_intake_response(stored)


@app.post("/api/v1/civicpermit/submittal/outline")
def submittal_outline(request: SubmittalOutlineRequest) -> dict[str, object]:
    result = draft_submittal_outline(
        project_name=request.project_name,
        proposal=request.proposal,
        project_type=request.project_type,
    )
    return result.__dict__


@app.post("/api/v1/civicpermit/export")
def permit_export(request: PermitExportRequest) -> dict[str, object]:
    result = build_policy_export(
        title=request.title,
        project_type=request.project_type,
        format=request.format,
    )
    return result.__dict__


def _intake_database_url() -> str | None:
    return os.environ.get("CIVICPERMIT_INTAKE_DB_URL")


def _get_intake_repository() -> PermitIntakeRepository:
    global _intake_db_url, _intake_repository
    db_url = _intake_database_url()
    if db_url is None:
        raise RuntimeError("CIVICPERMIT_INTAKE_DB_URL is not configured.")
    if _intake_repository is None or db_url != _intake_db_url:
        _dispose_intake_repository()
        _intake_db_url = db_url
        _intake_repository = PermitIntakeRepository(db_url=db_url)
    return _intake_repository


def _dispose_intake_repository() -> None:
    global _intake_repository
    if _intake_repository is not None:
        _intake_repository.engine.dispose()
        _intake_repository = None


def _require_staff_role(role: str | None) -> None:
    if role == "staff":
        return
    raise HTTPException(
        status_code=403,
        detail={
            "message": "Persisted CivicPermit intake records require staff access.",
            "fix": "Send X-CivicPermit-Role: staff from a trusted staff or service workflow when intake persistence is enabled.",
        },
    )


def _lookup_permit_requirement(*, project_type: str, location_context: str = ""):
    if _intake_database_url() is None:
        return lookup_permit_requirement(project_type=project_type, location_context=location_context)
    return _get_intake_repository().lookup_requirement(
        project_type=project_type,
        location_context=location_context,
    )


def _lookup_permit_requirement_with_source(*, project_type: str, location_context: str = ""):
    if _intake_database_url() is None:
        return (
            lookup_permit_requirement(project_type=project_type, location_context=location_context),
            "sample",
        )
    return _get_intake_repository().lookup_requirement_with_source(
        project_type=project_type,
        location_context=location_context,
    )


def _stored_intake_response(stored: StoredIntakeReview) -> dict[str, object]:
    return {
        "intake_id": stored.intake_id,
        "project_type": stored.project_type,
        "proposal": stored.proposal,
        "status": stored.status,
        "missing_or_unclear": list(stored.missing_or_unclear),
        "next_step": stored.next_step,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }
