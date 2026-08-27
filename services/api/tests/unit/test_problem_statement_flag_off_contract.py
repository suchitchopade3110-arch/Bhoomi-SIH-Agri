"""The PROBLEM_STATEMENT flag-off contract for the SIH26131-only endpoints.

Locks docs/specs/problem_statement_flag_off_contract.md: when the deployment
is not on ``sih26131``, ``/farms/{id}/alerts``, ``/alerts/{id}/acknowledge``
and ``/treatments/{id}/efficacy`` answer with one stable, documented payload
— never an empty 200, never a 500, never a bare 404 that a client cannot tell
apart from "no such farm".
"""

import importlib

import pytest
from fastapi.testclient import TestClient

from app.config import PROBLEM_STATEMENT_DEFAULT, get_settings
from app.core.feature_flags import FEATURE_ALERTS, FEATURE_TREATMENT_EFFICACY

# (method, path, expected details.feature, expected details.endpoint)
SIH26131_ONLY_ENDPOINTS = [
    ("GET", "/api/v1/farms/f_demo/alerts", FEATURE_ALERTS, "GET /api/v1/farms/{farm_id}/alerts"),
    (
        "POST",
        "/api/v1/alerts/alt_demo/acknowledge",
        FEATURE_ALERTS,
        "POST /api/v1/alerts/{alert_id}/acknowledge",
    ),
    (
        "GET",
        "/api/v1/treatments/neem_oil/efficacy?pathogen=blb&crop=samba_paddy&district=Erode",
        FEATURE_TREATMENT_EFFICACY,
        "GET /api/v1/treatments/{treatment_id}/efficacy",
    ),
]


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
    """Every test here reloads app.main; put it back on the default afterwards."""
    yield
    _reload_app_with_problem_statement(monkeypatch, PROBLEM_STATEMENT_DEFAULT)


@pytest.fixture
def flag_off_client(monkeypatch) -> TestClient:
    return TestClient(_reload_app_with_problem_statement(monkeypatch, "sih25076"))


@pytest.mark.parametrize(("method", "path", "feature", "endpoint"), SIH26131_ONLY_ENDPOINTS)
def test_flag_off_returns_documented_501_envelope(flag_off_client, method, path, feature, endpoint):
    response = flag_off_client.request(method, path, json={"farm_id": "f_demo", "reason": "action_taken"})

    assert response.status_code == 501
    body = response.json()
    assert body == {
        "error": {
            "code": "FEATURE_NOT_AVAILABLE",
            "message": (
                f"'{feature}' is not available under PROBLEM_STATEMENT=sih25076. "
                "It is part of the sih26131 feature set; set PROBLEM_STATEMENT=sih26131 "
                "to enable it."
            ),
            "details": {
                "feature": feature,
                "endpoint": endpoint,
                "active_problem_statement": "sih25076",
                "required_problem_statement": "sih26131",
            },
        }
    }


@pytest.mark.parametrize(("method", "path", "feature", "endpoint"), SIH26131_ONLY_ENDPOINTS)
def test_flag_off_is_never_an_empty_200_or_a_500(flag_off_client, method, path, feature, endpoint):
    """The two failure modes this contract exists to rule out."""
    response = flag_off_client.request(method, path, json={"farm_id": "f_demo", "reason": "action_taken"})

    assert response.status_code != 200, "an empty 200 reads as 'no alerts', not 'no such feature'"
    assert response.status_code < 500 or response.status_code == 501
    assert response.status_code != 500, "the flag being off is a configured state, not a server fault"
    assert response.status_code != 404, "a bare 404 is indistinguishable from an unknown farm id"


def test_flag_off_answer_does_not_require_authentication(flag_off_client):
    """No Authorization header at all still yields the real reason, not a 401 —
    a client with an expired token learns the call will never work here."""
    response = flag_off_client.get("/api/v1/farms/f_demo/alerts")

    assert response.status_code == 501
    assert response.json()["error"]["code"] == "FEATURE_NOT_AVAILABLE"


def test_flag_off_stubs_stay_out_of_the_openapi_schema(flag_off_client):
    """The published schema describes only what this deployment serves."""
    paths = flag_off_client.get("/api/v1/openapi.json").json()["paths"]

    assert "/api/v1/farms/{farm_id}/alerts" not in paths
    assert "/api/v1/alerts/{alert_id}/acknowledge" not in paths
    assert "/api/v1/treatments/{treatment_id}/efficacy" not in paths


def test_flag_on_serves_the_real_routers_not_the_stubs(monkeypatch):
    """Under sih26131 the live routers win: an unauthenticated call hits the
    auth gate (401), proving no flag-off stub is shadowing them."""
    client = TestClient(_reload_app_with_problem_statement(monkeypatch, "sih26131"))

    assert client.get("/api/v1/farms/f_demo/alerts").status_code == 401
    assert (
        client.post(
            "/api/v1/alerts/alt_demo/acknowledge",
            json={"farm_id": "f_demo", "reason": "action_taken"},
        ).status_code
        == 401
    )
    assert (
        client.get(
            "/api/v1/treatments/neem_oil/efficacy",
            params={"pathogen": "blb", "crop": "samba_paddy", "district": "Erode"},
        ).status_code
        == 401
    )
