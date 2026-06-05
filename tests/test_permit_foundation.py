from fastapi.testclient import TestClient

from civicpermit.intake_review import review_intake_readiness
from civicpermit.main import app
from civicpermit.records_export import build_policy_export
from civicpermit.requirement_lookup import lookup_permit_requirement
from civicpermit.submittal_outline import draft_submittal_outline


client = TestClient(app)


def test_requirement_lookup_returns_actionable_checklist() -> None:
    result = lookup_permit_requirement(project_type="ADU", location_context="R-2 parcel")
    assert result.requirement_id == "permit-adu-1.0"
    assert "Site plan" in result.required_materials[0]
    assert "does not approve permits" in result.disclaimer


def test_intake_review_keeps_completeness_boundary() -> None:
    result = review_intake_readiness(
        proposal="ADU at 100 Main Street with site plan, project description, contact email, and parcel.",
        project_type="adu",
    )
    assert result.status == "ready-for-staff-triage"
    assert result.missing_or_unclear == ()
    assert "formal application" in result.next_step


def test_submittal_outline_requires_staff_review() -> None:
    result = draft_submittal_outline(
        project_name="Backyard ADU",
        proposal="ADU at 100 Main Street with site plan.",
        project_type="adu",
    )
    assert result.heading == "Pre-application intake outline for Backyard ADU"
    assert result.review_required is True
    assert "official application type" in result.applicant_message


def test_permit_export_preserves_records_context() -> None:
    result = build_policy_export(title="Backyard ADU Intake", project_type="adu")
    assert result.title == "Backyard ADU Intake"
    assert result.project_type == "adu"
    assert "Preserve applicant-provided proposal text." in result.checklist
    assert "municipal permit intake record" in result.retention_note


def test_requirement_lookup_api_success_shape() -> None:
    response = client.post(
        "/api/v1/civicpermit/requirements/lookup",
        json={"project_type": "commercial tenant", "location_context": "downtown"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["requirement_id"] == "permit-commercial-tenant-2.0"
    assert payload["required_materials"]
    assert payload["disclaimer"]


def test_requirement_lookup_validation_is_actionable() -> None:
    response = client.post("/api/v1/civicpermit/requirements/lookup", json={})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "project_type" in detail["message"]
    assert "project_type" in detail["fields"]
    assert "fields array" in detail["fix"]


def test_oversized_intake_validation_is_actionable() -> None:
    response = client.post(
        "/api/v1/civicpermit/intake/review",
        json={"proposal": "x" * 5001, "project_type": "adu"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "proposal" in detail["fields"]
    assert "fields array" in detail["fix"]


def test_intake_and_submittal_apis() -> None:
    intake = client.post(
        "/api/v1/civicpermit/intake/review",
        json={"proposal": "ADU at 100 Main with site plan and contact email.", "project_type": "adu"},
    )
    outline = client.post(
        "/api/v1/civicpermit/submittal/outline",
        json={
            "project_name": "Backyard ADU",
            "proposal": "ADU at 100 Main with site plan.",
            "project_type": "adu",
        },
    )
    assert intake.status_code == 200
    assert intake.json()["status"] == "needs-applicant-follow-up"
    assert outline.status_code == 200
    assert outline.json()["review_required"] is True


def test_development_review_context_returns_review_required_contract() -> None:
    response = client.post(
        "/api/v1/civicpermit/context/development-review",
        json={
            "project_type": "adu",
            "proposal": "ADU at 100 Main with site plan and contact email.",
            "location_context": "R-2 parcel",
            "zoning_context_id": "zone-ledger-1",
            "code_context_id": "code-section-1",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["requirement_id"] == "permit-adu-1.0"
    assert payload["required_materials"]
    assert payload["zoning_context_id"] == "zone-ledger-1"
    assert payload["code_context_id"] == "code-section-1"
    assert "Sample Development Review Manual, ADU Intake Checklist" in payload["citations"]
    assert "CivicZone context: zone-ledger-1" in payload["citations"]
    assert "CivicCode context: code-section-1" in payload["citations"]
    assert payload["review_required"] is True
    assert payload["source"] == "sample"
    assert "not a permit approval" in payload["boundary"]
    assert "system-of-record action" in payload["boundary"]


def test_development_review_context_rejects_unsupported_summary_fields() -> None:
    response = client.post(
        "/api/v1/civicpermit/context/development-review",
        json={
            "project_type": "adu",
            "proposal": "ADU at 100 Main with site plan and contact email.",
            "zoning_context_summary": "R-2 allows ADU subject to staff review.",
        },
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert "zoning_context_summary" in detail["fields"]
    assert "fields array" in detail["fix"]


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/civicpermit")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert '<a class="skip-link" href="#main">Skip to main content</a>' in text
    assert '<main id="main" tabindex="-1">' in text
    assert "v0.2.2 permit pre-application + staff review queues" in text
    assert '<form id="lookup-form">' in text
    assert '<button id="lookup-submit" type="submit">Lookup checklist</button>' in text
    assert '<textarea id="proposal-note"' in text
    assert 'fetch("/api/v1/civicpermit/requirements/lookup"' in text
    assert "Static sample proposal" not in text
    assert "does not approve permits" in text
    assert "permitting system of record" in text
