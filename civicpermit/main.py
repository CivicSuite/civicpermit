"""FastAPI runtime foundation for CivicPermit."""

import os
from typing import Annotated

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import staff_key_gate
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from civicpermit import __version__
from civicpermit.intake_review import review_intake_readiness
from civicpermit.integration_mocks import validate_development_review_mocks
from civicpermit.persistence import (
    PermitIntakeRepository,
    StaffReviewQueueItem,
    StaffReviewSummary,
    StoredIntakeReview,
)
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
_require_staff_key = staff_key_gate("CIVICPERMIT_STAFF_API_KEY", "X-CivicPermit-Staff-Key")


class RequirementLookupRequest(BaseModel):
    project_type: str = Field(min_length=1, max_length=255)
    location_context: str = Field(default="", max_length=500)


class IntakeReviewRequest(BaseModel):
    proposal: str = Field(min_length=1, max_length=5000)
    project_type: str = Field(min_length=1, max_length=255)


class DevelopmentReviewContextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_type: str = Field(min_length=1, max_length=255)
    proposal: str = Field(min_length=1, max_length=5000)
    location_context: str = Field(default="", max_length=500)
    zoning_context_id: str | None = Field(default=None, max_length=160)
    code_context_id: str | None = Field(default=None, max_length=160)


class SubmittalOutlineRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=500)
    proposal: str = Field(min_length=1, max_length=5000)
    project_type: str = Field(min_length=1, max_length=255)


class PermitExportRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    project_type: str = Field(min_length=1, max_length=255)
    format: str = Field(default="markdown", min_length=1, max_length=40)


class StaffReviewCreateRequest(BaseModel):
    proposal: str = Field(min_length=1, max_length=5000)
    project_type: str = Field(min_length=1, max_length=255)
    reason: str = Field(min_length=1, max_length=1000)
    intake_id: str | None = Field(default=None, max_length=36)


class StaffReviewUpdateRequest(BaseModel):
    status: str = Field(min_length=1, max_length=80)
    assigned_to: str | None = Field(default=None, max_length=255)
    resolution: str | None = Field(default=None, max_length=2000)


class IntegrationMockRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    scenario: str = Field(default="development-review-context", max_length=160)


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicPermit",
        "version": __version__,
        "status": "v1 permit pre-application and intake-readiness runtime",
        "message": (
            "CivicPermit package, API foundation, configurable permit requirement records, "
            "database-backed intake records, staff review queues, development-review context "
            "packets, intake-readiness review, submittal outline helper, records-ready export "
            "checklist, readiness gate, and public lookup UI are online; permit approvals, official "
            "completeness determinations, fee calculations, inspections, live GIS, live LLM "
            "calls, and permitting-system-of-record writeback are not implemented."
        ),
        "next_step": "Configure CIVICPERMIT_INTAKE_DB_URL, load local permit requirements, and verify /ready before public use.",
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


@app.get("/ready")
def ready() -> dict[str, object]:
    """Return public-use readiness without treating sample fallback as customer data."""

    return _readiness_payload()


@app.get("/api/v1/civicpermit/readiness")
def readiness() -> dict[str, object]:
    """Return detailed CivicPermit local-data readiness for installers and operators."""

    return _readiness_payload()


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
    """Return the public permit pre-application lookup UI."""

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
    x_civicpermit_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _intake_database_url() is not None:
        _require_staff_role(x_civicpermit_role, x_civicpermit_staff_key)
        stored = _get_intake_repository().create_intake_review(
            proposal=request.proposal,
            project_type=request.project_type,
        )
        staff_review = None
        if stored.missing_or_unclear:
            staff_review = _get_intake_repository().create_staff_review_queue_item(
                intake_id=stored.intake_id,
                proposal=stored.proposal,
                project_type=stored.project_type,
                reason=(
                    "Applicant follow-up required for: "
                    + ", ".join(stored.missing_or_unclear)
                    + ". Staff must review before formal intake."
                ),
                created_by="staff",
            )
        return _stored_intake_response(stored, staff_review=staff_review)

    result = review_intake_readiness(proposal=request.proposal, project_type=request.project_type)
    payload = result.__dict__
    payload["intake_id"] = None
    payload["staff_review_id"] = None
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


@app.post("/api/v1/civicpermit/integrations/mock/development-review")
def integration_mock_development_review(request: IntegrationMockRequest) -> dict[str, object]:
    result = validate_development_review_mocks(request.model_dump())
    return {
        "scenario": result.scenario,
        "status": result.status,
        "review_required": result.review_required,
        "findings": list(result.findings),
        "boundary": result.boundary,
    }


@app.get("/api/v1/civicpermit/intake/{intake_id}")
def get_intake_review(
    intake_id: str,
    x_civicpermit_role: Annotated[str | None, Header()] = None,
    x_civicpermit_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    if _intake_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicPermit intake persistence is not configured.",
                "fix": "Set CIVICPERMIT_INTAKE_DB_URL to retrieve persisted intake review records.",
            },
        )
    _require_staff_role(x_civicpermit_role, x_civicpermit_staff_key)
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


@app.post("/api/v1/civicpermit/staff/reviews")
def create_staff_review(
    request: StaffReviewCreateRequest,
    x_civicpermit_role: Annotated[str | None, Header()] = None,
    x_civicpermit_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    _require_persistence_configured()
    _require_staff_role(x_civicpermit_role, x_civicpermit_staff_key)
    item = _get_intake_repository().create_staff_review_queue_item(
        intake_id=request.intake_id,
        proposal=request.proposal,
        project_type=request.project_type,
        reason=request.reason,
        created_by="staff",
    )
    return _staff_review_payload(item)


@app.get("/api/v1/civicpermit/staff/reviews")
def list_staff_reviews(
    status: str | None = None,
    x_civicpermit_role: Annotated[str | None, Header()] = None,
    x_civicpermit_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    _require_persistence_configured()
    _require_staff_role(x_civicpermit_role, x_civicpermit_staff_key)
    return {
        "visibility": "staff_only",
        "items": [
            _staff_review_payload(item)
            for item in _get_intake_repository().list_staff_review_queue_items(status=status)
        ],
    }


@app.patch("/api/v1/civicpermit/staff/reviews/{review_id}")
def update_staff_review(
    review_id: str,
    request: StaffReviewUpdateRequest,
    x_civicpermit_role: Annotated[str | None, Header()] = None,
    x_civicpermit_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    _require_persistence_configured()
    _require_staff_role(x_civicpermit_role, x_civicpermit_staff_key)
    try:
        item = _get_intake_repository().update_staff_review_queue_item(
            review_id=review_id,
            status=request.status,
            assigned_to=request.assigned_to,
            resolution=request.resolution,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"message": "Staff review update is invalid.", "fix": str(exc)},
        ) from exc
    if item is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "CivicPermit staff review item was not found.",
                "fix": "List staff reviews and retry with an existing review_id.",
            },
        )
    return _staff_review_payload(item)


@app.get("/api/v1/civicpermit/staff/reviews/summary")
def staff_review_summary(
    x_civicpermit_role: Annotated[str | None, Header()] = None,
    x_civicpermit_staff_key: Annotated[str | None, Header()] = None,
) -> dict[str, object]:
    _require_persistence_configured()
    _require_staff_role(x_civicpermit_role, x_civicpermit_staff_key)
    return _staff_review_summary_payload(_get_intake_repository().staff_review_summary())


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
        _intake_repository = PermitIntakeRepository(db_url=db_url, seed_defaults=False)
    return _intake_repository


def _dispose_intake_repository() -> None:
    global _intake_repository
    if _intake_repository is not None:
        _intake_repository.engine.dispose()
        _intake_repository = None


def _require_staff_role(role: str | None, staff_key_header: str | None) -> None:
    _require_staff_key(role=role, staff_key=staff_key_header)


def _require_persistence_configured() -> None:
    if _intake_database_url() is not None:
        return
    raise HTTPException(
        status_code=503,
        detail={
            "message": "CivicPermit staff review persistence is not configured.",
            "fix": "Set CIVICPERMIT_INTAKE_DB_URL before using staff review queue routes.",
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


def _readiness_payload() -> dict[str, object]:
    db_url = _intake_database_url()
    if db_url is None:
        return {
            "status": "not-ready",
            "ready": False,
            "intake_database_configured": False,
            "schema_ready": False,
            "schema_version": None,
            "expected_schema_version": None,
            "requirement_count": 0,
            "blockers": [
                "Set CIVICPERMIT_INTAKE_DB_URL to a local permit intake database.",
                "Load adopted local permit requirement records before public use.",
            ],
        }

    repository = _get_intake_repository()
    schema_status = repository.schema_status()
    requirements = repository.list_requirements()
    blockers: list[str] = []
    if not schema_status.ready:
        blockers.append("Run the local CivicPermit schema status/migration check.")
    if not requirements:
        blockers.append("Load adopted local permit requirement records before public use.")
    ready_for_public_use = not blockers
    return {
        "status": "ready" if ready_for_public_use else "not-ready",
        "ready": ready_for_public_use,
        "intake_database_configured": True,
        "schema_ready": schema_status.ready,
        "schema_version": schema_status.schema_version,
        "expected_schema_version": schema_status.expected_schema_version,
        "requirement_count": len(requirements),
        "blockers": blockers,
    }


def _stored_intake_response(
    stored: StoredIntakeReview, *, staff_review: StaffReviewQueueItem | None = None
) -> dict[str, object]:
    return {
        "intake_id": stored.intake_id,
        "staff_review_id": None if staff_review is None else staff_review.review_id,
        "project_type": stored.project_type,
        "proposal": stored.proposal,
        "status": stored.status,
        "missing_or_unclear": list(stored.missing_or_unclear),
        "next_step": stored.next_step,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }


def _staff_review_payload(item: StaffReviewQueueItem) -> dict[str, object]:
    return {
        "review_id": item.review_id,
        "intake_id": item.intake_id,
        "project_type": item.project_type,
        "proposal": item.proposal,
        "status": item.status,
        "reason": item.reason,
        "assigned_to": item.assigned_to,
        "resolution": item.resolution,
        "created_by": item.created_by,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
        "visibility": item.visibility,
        "boundary": (
            "Staff review queues support intake triage only; they do not approve permits, "
            "determine official completeness, calculate fees, or write to a permitting system."
        ),
    }


def _staff_review_summary_payload(summary: StaffReviewSummary) -> dict[str, object]:
    return {
        "total_items": summary.total_items,
        "by_status": summary.by_status,
        "open_items": summary.open_items,
        "generated_at": summary.generated_at.isoformat(),
        "visibility": summary.visibility,
    }
