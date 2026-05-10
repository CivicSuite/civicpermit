"""Adversarial local integration contracts for CivicPermit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IntegrationMockResult:
    scenario: str
    status: str
    review_required: bool
    findings: tuple[str, ...]
    boundary: str


def validate_development_review_mocks(payload: dict[str, Any]) -> IntegrationMockResult:
    """Validate local CivicZone/CivicCode handoff payloads without external calls."""

    findings: list[str] = []
    scenario = str(payload.get("scenario", "development-review-context"))

    if payload.get("role") not in {"staff", "service"}:
        findings.append("Rejected context payload without trusted staff or service role.")
    if not payload.get("zoning_context_id"):
        findings.append("Missing CivicZone context ID; route parcel assumptions to planning staff.")
    if not payload.get("code_context_id"):
        findings.append("Missing CivicCode context ID; cite code context before applicant guidance.")
    if payload.get("permit_approval") is True:
        findings.append("Rejected attempted permit approval in integration context.")
    if payload.get("fee_calculation") is not None:
        findings.append("Rejected official fee calculation in integration context.")
    if payload.get("source_date_status") == "stale":
        findings.append("Stale zoning/code context requires staff refresh before formal intake.")

    status = "ready-for-staff-review" if not findings else "blocked-for-staff-review"
    return IntegrationMockResult(
        scenario=scenario,
        status=status,
        review_required=True,
        findings=tuple(findings),
        boundary=(
            "CivicPermit validates local integration context only; it does not call live "
            "CivicZone, CivicCode, GIS, LLM, or permitting-system services in this recovery release."
        ),
    )
