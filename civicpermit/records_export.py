"""Records-ready export helpers for CivicPermit v0.1.0."""

from __future__ import annotations

from dataclasses import dataclass

from civicpermit.requirement_lookup import lookup_permit_requirement


@dataclass(frozen=True)
class PermitExport:
    title: str
    project_type: str
    format: str
    checklist: tuple[str, ...]
    retention_note: str


def build_policy_export(*, title: str, project_type: str, format: str = "markdown") -> PermitExport:
    """Build a deterministic records-ready permit-intake export checklist."""

    requirement = lookup_permit_requirement(project_type=project_type)
    return PermitExport(
        title=title.strip() or "Untitled permit intake export",
        project_type=requirement.project_type,
        format=format,
        checklist=(
            "Preserve applicant-provided proposal text.",
            "Preserve sample checklist returned to applicant.",
            "Record staff reviewer and date before accepting formal submittal.",
            "Include the non-approval disclaimer with any public-facing export.",
        ),
        retention_note=(
            "Keep inquiry text, requirement checklist, reviewer, generated outline, and final "
            "staff edits with the municipal permit intake record."
        ),
    )
