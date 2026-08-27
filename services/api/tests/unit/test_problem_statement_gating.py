"""Phase 1: PROBLEM_STATEMENT flag gates SIH25076-only routers.

Verifies docs/specs/api_contract_sih26131_delta.md §1:
- sih25076 (default): resource_plan/schemes mount.
- sih26131: resource_plan/schemes stay mounted too (see README.md §5 — the
  original deprecation plan was superseded); alerts and efficacy mount
  additionally.

NOTE: the ``land``/``officer`` routers this test used to assert on were
removed along with the Officer Portal and its HITL land-verification
workflow.
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
    _reload_app_with_problem_statement(monkeypatch, "sih26131")


def test_default_is_sih26131():
    assert get_settings().PROBLEM_STATEMENT == "sih26131"


def test_sih25076_mounts_legacy_routers(monkeypatch):
    app = _reload_app_with_problem_statement(monkeypatch, "sih25076")
    client = TestClient(app)

    openapi = client.get("/api/v1/openapi.json").json()
    paths = openapi["paths"]

    assert "/api/v1/resource-plan/{farm_id}" in paths
    assert "/api/v1/schemes/match" in paths

    # Phase 3/4: alerts and efficacy routers are sih26131-only, absent here.
    assert "/api/v1/farms/{farm_id}/alerts" not in paths
    assert "/api/v1/alerts/{alert_id}/acknowledge" not in paths
    assert "/api/v1/treatments/{treatment_id}/efficacy" not in paths


def test_sih26131_unmounts_legacy_routers_and_keeps_core(monkeypatch):
    app = _reload_app_with_problem_statement(monkeypatch, "sih26131")
    client = TestClient(app)

    openapi = client.get("/api/v1/openapi.json").json()
    paths = openapi["paths"]

    # SIH26131: resource_plan, schemes, alerts, efficacy all mount.
    assert "/api/v1/resource-plan/{farm_id}" in paths
    assert "/api/v1/schemes/match" in paths
    assert "/api/v1/farms/{farm_id}/alerts" in paths
    assert "/api/v1/alerts/{alert_id}/acknowledge" in paths
    assert "/api/v1/treatments/{treatment_id}/efficacy" in paths

    # Core intelligence routers remain mounted in every mode.
    assert "/api/v1/auth/register" in paths
    assert "/api/v1/farms" in paths
    assert "/api/v1/farms/{farm_id}/risk" in paths
    assert "/api/v1/farms/{farm_id}/diagnose" in paths
    assert "/api/v1/followup/checkin" in paths
    assert "/api/v1/agronomist/queue" in paths
    assert "/api/v1/voice/transcribe" in paths
    assert "/api/v1/assets/presigned-url" in paths
    assert "/api/v1/timeline/{farm_id}" in paths
    assert "/api/v1/weather/current" in paths


def test_alerts_routes_dependency_chain_resolves_without_db(monkeypatch):
    """Proves the alerts router's DI graph (AlertService -> AlertRepository/
    FarmRepository/WeatherPort -> get_db) builds cleanly under sih26131 —
    an unauthenticated call hits the auth gate (401), never a 500 from
    broken wiring, matching every other protected route's contract."""
    app = _reload_app_with_problem_statement(monkeypatch, "sih26131")
    client = TestClient(app)

    response = client.get("/api/v1/farms/f_1/alerts")
    assert response.status_code == 401

    response = client.post("/api/v1/alerts/alt_1/acknowledge", json={"farm_id": "f_1", "reason": "action_taken"})
    assert response.status_code == 401


def test_root_reports_active_contract(monkeypatch):
    app = _reload_app_with_problem_statement(monkeypatch, "sih26131")
    client = TestClient(app)

    data = client.get("/").json()
    assert data["contract"] == "SIH26131"
