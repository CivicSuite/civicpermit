"""Deterministic permit requirement lookup helpers for CivicPermit."""

from __future__ import annotations

from dataclasses import dataclass


DISCLAIMER = (
    "CivicPermit provides intake-support information only. It does not approve permits, "
    "calculate official fees, determine completeness, schedule inspections, or replace the "
    "permitting system of record."
)


@dataclass(frozen=True)
class PermitRequirement:
    requirement_id: str
    project_type: str
    title: str
    citation: str
    required_materials: tuple[str, ...]
    staff_note: str
    disclaimer: str = DISCLAIMER


REQUIREMENTS = {
    "adu": PermitRequirement(
        requirement_id="permit-adu-1.0",
        project_type="adu",
        title="Accessory dwelling unit pre-application checklist",
        citation="Sample Development Review Manual, ADU Intake Checklist",
        required_materials=(
            "Site plan showing existing and proposed structures.",
            "Parking and access narrative.",
            "Utility connection description.",
            "Owner affidavit or authorization form.",
        ),
        staff_note="Route zoning questions to planning staff before accepting a formal application.",
    ),
    "commercial": PermitRequirement(
        requirement_id="permit-commercial-tenant-2.0",
        project_type="commercial",
        title="Commercial tenant improvement intake checklist",
        citation="Sample Building Division Intake Guide, Tenant Improvements",
        required_materials=(
            "Floor plan and life-safety plan.",
            "Scope-of-work narrative.",
            "Contractor license information if known.",
            "Accessibility-impact statement for public-facing areas.",
        ),
        staff_note="Confirm whether fire prevention, health, or public works review is required.",
    ),
}


def lookup_permit_requirement(*, project_type: str, location_context: str = "") -> PermitRequirement:
    """Return a sample requirement set without live GIS, fee, or permit-system calls."""

    normalized = project_type.strip().casefold()
    for key, requirement in REQUIREMENTS.items():
        if key in normalized:
            return requirement
    context_note = (
        f" Location context received for staff review: {location_context.strip()}."
        if location_context.strip()
        else ""
    )
    return PermitRequirement(
        requirement_id="permit-general-1.0",
        project_type=project_type.strip() or "general",
        title="General pre-application intake checklist",
        citation="Sample Development Services Intake Guide, General Submittals",
        required_materials=(
            "Project description.",
            "Property address or parcel identifier.",
            "Applicant contact information.",
            "Conceptual site or floor plan if available.",
        ),
        staff_note=f"Route to permit counter staff for formal type assignment.{context_note}",
    )
