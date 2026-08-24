"""Phase 1: PROBLEM_STATEMENT flag gates SIH25076-only routers.

Verifies docs/specs/api_contract_sih26131_delta.md §1:
- sih25076 (default): land/officer/resource_plan/schemes mount.
- sih26131: those four unmount (404); core intelligence stays mounted.
"""

import importlib

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings


def _reload_app_with_problem_statement(monkeypatch, value: str):
    monkeypatch.setenv("PROBLEM_STATEMENT", value)
    get_settings.cache_clear()

    import app.api.v1 as v1_module
    importlib.reload(v1_module)

    import app.main as main_module
    importlib.reload(main_module)

    return main_module.app


@pytest.fixture(autouse=True)
def _restore_default_app(monkeypatch):
    """Every test in this module reloads app.main; put it back afterwards."""
    yield
    _reload_app_with_problem_statement(monkeypatch, "sih25076")


def test_default_is_sih25076():
    assert get_settings().PROBLEM_STATEMENT == "sih25076"


def test_sih25076_mounts_legacy_routers(monkeypatch):
    app = _reload_app_with_problem_statement(monkeypatch, "sih25076")
    client = TestClient(app)

    openapi = client.get("/api/v1/openapi.json").json()
    paths = openapi["paths"]

    assert "/api/v1/land/verify" in paths
    assert "/api/v1/officer/queue" in paths
    assert "/api/v1/resource-plan/{farm_id}" in paths
    assert "/api/v1/schemes/match" in paths


def test_sih26131_unmounts_legacy_routers_and_keeps_core(monkeypatch):
    app = _reload_app_with_problem_statement(monkeypatch, "sih26131")
    client = TestClient(app)

    openapi = client.get("/api/v1/openapi.json").json()
    paths = openapi["paths"]

    # SIH25076-only routers must be gone from the API surface entirely.
    assert "/api/v1/land/verify" not in paths
    assert "/api/v1/officer/queue" not in paths
    assert "/api/v1/resource-plan/{farm_id}" not in paths
    assert "/api/v1/schemes/match" not in paths

    # A direct call to a deprecated route 404s rather than 401/other.
    response = client.get("/api/v1/officer/queue")
    assert response.status_code == 404

    # Verification-gate assertion: schemes specifically 404s in sih26131.
    response = client.get("/api/v1/schemes/active")
    assert response.status_code == 404

    # Core intelligence routers remain mounted in every mode.
    assert "/api/v1/auth/register" in paths
    assert "/api/v1/farms" in paths
    assert "/api/v1/farms/{farm_id}/health" in paths
    assert "/api/v1/farms/{farm_id}/diagnose" in paths
    assert "/api/v1/followup/checkin" in paths
    assert "/api/v1/agronomist/queue" in paths
    assert "/api/v1/voice/transcribe" in paths
    assert "/api/v1/assets/presigned-url" in paths
    assert "/api/v1/timeline/{farm_id}" in paths
    assert "/api/v1/weather/current" in paths


def test_root_reports_active_contract(monkeypatch):
    app = _reload_app_with_problem_statement(monkeypatch, "sih26131")
    client = TestClient(app)

    data = client.get("/").json()
    assert data["contract"] == "SIH26131"
