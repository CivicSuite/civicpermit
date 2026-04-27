"""FastAPI runtime foundation for CivicPermit."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicpermit import __version__
from civicpermit.intake_review import review_intake_readiness
from civicpermit.public_ui import render_public_lookup_page
from civicpermit.records_export import build_policy_export
from civicpermit.requirement_lookup import lookup_permit_requirement
from civicpermit.submittal_outline import draft_submittal_outline


app = FastAPI(
    title="CivicPermit",
    version=__version__,
    description="Permit pre-application and development-review intake support for CivicSuite.",
)


class RequirementLookupRequest(BaseModel):
    project_type: str
    location_context: str = ""


class IntakeReviewRequest(BaseModel):
    proposal: str
    project_type: str


class SubmittalOutlineRequest(BaseModel):
    project_name: str
    proposal: str
    project_type: str


class PermitExportRequest(BaseModel):
    title: str
    project_type: str
    format: str = "markdown"


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicPermit",
        "version": __version__,
        "status": "permit intake foundation",
        "message": (
            "CivicPermit package, API foundation, sample permit requirement lookup, intake-readiness review, submittal outline helper, records-ready export checklist, and public UI foundation are online; "
            "permit approvals, official completeness determinations, fee calculations, inspections, live GIS, live LLM calls, and permitting-system-of-record integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.0 roadmap: local permit type configuration, CivicZone/CivicCode context APIs, and staff review queues",
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


@app.get("/civicpermit", response_class=HTMLResponse)
def public_civicpermit_page() -> str:
    """Return the public sample permit pre-application UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civicpermit/requirements/lookup")
def requirement_lookup(request: RequirementLookupRequest) -> dict[str, object]:
    result = lookup_permit_requirement(
        project_type=request.project_type,
        location_context=request.location_context,
    )
    return result.__dict__


@app.post("/api/v1/civicpermit/intake/review")
def intake_review(request: IntakeReviewRequest) -> dict[str, object]:
    result = review_intake_readiness(proposal=request.proposal, project_type=request.project_type)
    return result.__dict__


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
