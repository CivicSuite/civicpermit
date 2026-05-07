from fastapi.testclient import TestClient

from civicpermit.integration_mocks import validate_development_review_mocks
from civicpermit.main import app


client = TestClient(app)


def test_adversarial_mock_rejects_spoofed_approval_and_missing_context() -> None:
    result = validate_development_review_mocks(
        {
            "scenario": "spoofed-permit-approval",
            "role": "resident",
            "permit_approval": True,
            "fee_calculation": "$1,250",
            "source_date_status": "stale",
        }
    )

    assert result.status == "blocked-for-staff-review"
    assert result.review_required is True
    assert "Rejected context payload without trusted staff or service role." in result.findings
    assert "Rejected attempted permit approval in integration context." in result.findings
    assert "Rejected official fee calculation in integration context." in result.findings
    assert "does not call live CivicZone" in result.boundary


def test_integration_mock_api_accepts_complete_staff_context_for_review() -> None:
    response = client.post(
        "/api/v1/civicpermit/integrations/mock/development-review",
        json={
            "scenario": "complete-local-context",
            "role": "staff",
            "zoning_context_id": "zone-context-123",
            "code_context_id": "code-context-456",
            "source_date_status": "current",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready-for-staff-review"
    assert payload["findings"] == []
    assert payload["review_required"] is True


def test_integration_mock_api_blocks_stale_or_partial_context() -> None:
    response = client.post(
        "/api/v1/civicpermit/integrations/mock/development-review",
        json={
            "scenario": "stale-zone-context",
            "role": "service",
            "zoning_context_id": "zone-context-123",
            "source_date_status": "stale",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "blocked-for-staff-review"
    assert "Missing CivicCode context ID" in " ".join(payload["findings"])
    assert "Stale zoning/code context" in " ".join(payload["findings"])
