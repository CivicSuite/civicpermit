"""Submittal outline helpers for CivicPermit."""

from __future__ import annotations

from dataclasses import dataclass

from civicpermit.intake_review import review_intake_readiness
from civicpermit.requirement_lookup import DISCLAIMER, lookup_permit_requirement


@dataclass(frozen=True)
class SubmittalOutline:
    project_name: str
    heading: str
    required_materials: tuple[str, ...]
    applicant_message: str
    review_required: bool
    disclaimer: str = DISCLAIMER


def draft_submittal_outline(*, project_name: str, proposal: str, project_type: str) -> SubmittalOutline:
    """Create a deterministic applicant-facing submittal outline."""

    requirement = lookup_permit_requirement(project_type=project_type)
    readiness = review_intake_readiness(proposal=proposal, project_type=project_type)
    clean_name = project_name.strip() or "Untitled permit inquiry"
    return SubmittalOutline(
        project_name=clean_name,
        heading=f"Pre-application intake outline for {clean_name}",
        required_materials=requirement.required_materials,
        applicant_message=(
            f"Sample intake status: {readiness.status}. Staff must confirm official "
            "application type, completeness, fees, and review routing."
        ),
        review_required=True,
    )
