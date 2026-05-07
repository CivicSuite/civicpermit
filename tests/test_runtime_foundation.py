from fastapi.testclient import TestClient

import civicpermit
from civicpermit.main import app


client = TestClient(app)


def test_package_version_is_100() -> None:
    assert civicpermit.__version__ == "1.0.0"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicPermit"
    assert payload["version"] == "1.0.0"
    assert payload["status"] == "v1 permit pre-application and intake-readiness runtime"
    assert "staff review queues" in payload["message"]
    assert "permit approvals" in payload["message"]
    assert "not implemented" in payload["message"]
    assert payload["next_step"].startswith("Configure local permit requirement data")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicpermit"
    assert payload["version"] == "1.0.0"
    assert payload["civiccore_version"] == "1.0.0"
