from fastapi.testclient import TestClient

import civicpermit
from civicpermit.main import app


client = TestClient(app)


def test_package_version_is_012() -> None:
    assert civicpermit.__version__ == "0.1.2"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicPermit"
    assert payload["version"] == "0.1.2"
    assert payload["status"] == "permit intake foundation plus intake persistence and CivicCore v1 alignment"
    assert "database-backed requirement and intake records" in payload["message"]
    assert "permit approvals" in payload["message"]
    assert "not implemented yet" in payload["message"]
    assert payload["next_step"].startswith("Post-v0.1.2 roadmap")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicpermit"
    assert payload["version"] == "0.1.2"
    assert payload["civiccore_version"] == "1.0.0"
