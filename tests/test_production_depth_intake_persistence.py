from fastapi.testclient import TestClient

import civicpermit.main as main_module
from civicpermit.main import app
from civicpermit.persistence import PermitIntakeRepository
from civicpermit.requirement_lookup import PermitRequirement


client = TestClient(app)


def test_requirement_and_intake_records_persist(tmp_path) -> None:
    db_path = tmp_path / "intake-records.db"
    repository = PermitIntakeRepository(db_url=f"sqlite:///{db_path}")

    requirement = repository.lookup_requirement(project_type="adu")
    stored = repository.create_intake_review(
        proposal="ADU at 100 Main Street with site plan, project description, contact email, and parcel.",
        project_type="adu",
    )
    repository.engine.dispose()

    second_repository = PermitIntakeRepository(db_url=f"sqlite:///{db_path}", seed_defaults=False)
    try:
        reloaded_requirement = second_repository.lookup_requirement(project_type="adu")
        reloaded_intake = second_repository.get_intake_review(stored.intake_id)
    finally:
        second_repository.engine.dispose()

    assert reloaded_requirement == requirement
    assert reloaded_intake is not None
    assert reloaded_intake.status == "ready-for-staff-triage"
    assert reloaded_intake.missing_or_unclear == ()
    db_path.unlink()


def test_api_uses_configured_intake_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-intake-records.db"
    monkeypatch.setenv("CIVICPERMIT_INTAKE_DB_URL", f"sqlite:///{db_path}")

    try:
        requirement_response = client.post(
            "/api/v1/civicpermit/requirements/lookup",
            json={"project_type": "adu", "location_context": "R-2 parcel"},
        )
        create_response = client.post(
            "/api/v1/civicpermit/intake/review",
            json={
                "proposal": "ADU at 100 Main Street with site plan, project description, contact email, and parcel.",
                "project_type": "adu",
            },
            headers={"X-CivicPermit-Role": "staff"},
        )
        intake_id = create_response.json()["intake_id"]
        get_response = client.get(
            f"/api/v1/civicpermit/intake/{intake_id}",
            headers={"X-CivicPermit-Role": "staff"},
        )
    finally:
        main_module._dispose_intake_repository()
        main_module._intake_db_url = None

    assert requirement_response.status_code == 200
    assert requirement_response.json()["requirement_id"] == "permit-adu-1.0"
    assert create_response.status_code == 200
    assert intake_id
    assert get_response.status_code == 200
    assert get_response.json()["intake_id"] == intake_id
    assert get_response.json()["status"] == "ready-for-staff-triage"
    db_path.unlink()


def test_persisted_intake_requires_staff_role(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "intake-auth.db"
    monkeypatch.setenv("CIVICPERMIT_INTAKE_DB_URL", f"sqlite:///{db_path}")

    try:
        create_response = client.post(
            "/api/v1/civicpermit/intake/review",
            json={
                "proposal": "CONFIDENTIAL: pre-application acquisition inquiry.",
                "project_type": "adu",
            },
        )
        get_response = client.get("/api/v1/civicpermit/intake/not-authorized")
    finally:
        main_module._dispose_intake_repository()
        main_module._intake_db_url = None

    assert create_response.status_code == 403
    assert get_response.status_code == 403
    assert "X-CivicPermit-Role: staff" in create_response.json()["detail"]["fix"]
    db_path.unlink(missing_ok=True)


def test_development_review_context_uses_configured_requirement_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "context-requirements.db"
    db_url = f"sqlite:///{db_path}"
    repository = PermitIntakeRepository(db_url=db_url, seed_defaults=False)
    repository.seed_requirements(
        [
            (
                "solar canopy",
                PermitRequirement(
                    requirement_id="permit-solar-canopy-1.0",
                    project_type="solar-canopy",
                    title="Solar canopy intake checklist",
                    citation="Building Intake Guide, Solar Canopy Checklist",
                    required_materials=(
                        "Structural drawings.",
                        "Electrical one-line diagram.",
                    ),
                    staff_note="Route structural and electrical review before formal intake.",
                ),
            )
        ]
    )
    repository.engine.dispose()
    monkeypatch.setenv("CIVICPERMIT_INTAKE_DB_URL", db_url)

    try:
        response = client.post(
            "/api/v1/civicpermit/context/development-review",
            json={
                "project_type": "solar canopy",
                "proposal": "Solar canopy at 100 Main with structural drawings.",
                "zoning_context_id": "zone-2",
                "code_context_id": "code-7",
            },
        )
    finally:
        main_module._dispose_intake_repository()
        main_module._intake_db_url = None

    assert response.status_code == 200
    payload = response.json()
    assert payload["requirement_id"] == "permit-solar-canopy-1.0"
    assert payload["source"] == "configured"
    assert payload["review_required"] is True
    assert payload["zoning_context_id"] == "zone-2"
    assert payload["code_context_id"] == "code-7"
    db_path.unlink()


def test_intake_lookup_requires_configured_database() -> None:
    response = client.get("/api/v1/civicpermit/intake/not-configured")

    assert response.status_code == 503
    assert "Set CIVICPERMIT_INTAKE_DB_URL" in response.json()["detail"]["fix"]
