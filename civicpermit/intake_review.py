"""Permit intake-readiness helpers for CivicPermit v0.1.1."""

from __future__ import annotations

from dataclasses import dataclass

from civicpermit.requirement_lookup import DISCLAIMER, lookup_permit_requirement


@dataclass(frozen=True)
class IntakeReadiness:
    project_type: str
    status: str
    missing_or_unclear: tuple[str, ...]
    next_step: str
    disclaimer: str = DISCLAIMER


def review_intake_readiness(*, proposal: str, project_type: str) -> IntakeReadiness:
    """Return deterministic sample intake readiness without deciding completeness."""

    text = proposal.casefold()
    requirement = lookup_permit_requirement(project_type=project_type)
    missing: list[str] = []
    checks = {
        "property address or parcel identifier": ("address", "parcel", "apn"),
        "project description": ("description", "scope", "propose"),
        "site or floor plan": ("site plan", "floor plan", "plan"),
        "applicant contact information": ("email", "phone", "contact"),
    }
    for label, terms in checks.items():
        if not any(term in text for term in terms):
            missing.append(label)
    status = "ready-for-staff-triage" if not missing else "needs-applicant-follow-up"
    return IntakeReadiness(
        project_type=requirement.project_type,
        status=status,
        missing_or_unclear=tuple(missing),
        next_step=(
            "Send the checklist to the applicant and route any zoning, code, or fee questions "
            "to the appropriate reviewer before accepting a formal application."
        ),
    )
