"""Phase 0 Skeleton verification tests."""

import pytest
from fastapi.testclient import TestClient
from app.core.config import get_settings
from app.core.enums import (
    AssetKind,
    CaseStatus,
    FollowupResponse,
    GateOutcome,
    HealthBand,
    LandStatus,
    ProblemSeverity,
    ProblemStatus,
    SchemeStatus,
    SubIndexKey,
    UserRole,
)
from app.core.errors import AppError, NotImplementedAPIError
from app.main import app
from app.repositories import (
    InMemoryAdvisoryRepository,
    InMemoryAssetRepository,
    InMemoryCaseRepository,
    InMemoryFarmRepository,
    InMemoryHealthRepository,
    InMemoryLandParcelRepository,
    InMemorySchemeRepository,
    InMemoryUserRepository,
)
from app.adapters.stubs import (
    StubAsrTtsAdapter,
    StubEmbeddingAdapter,
    StubImageDiagnosisAdapter,
    StubLLMAdapter,
    StubStorageAdapter,
    StubWeatherAdapter,
)


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Bhoomi API"
    assert data["version"] == "0.1.0"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_openapi_schema_generation(client):
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    paths = schema["paths"]

    # Verify key routes are present in OpenAPI documentation
    expected_routes = [
        "/api/v1/auth/register",
        "/api/v1/auth/login",
        "/api/v1/assets/presigned-url",
        "/api/v1/voice/transcribe",
        "/api/v1/farms",
        "/api/v1/land/verify",
        "/api/v1/officer/queue",
        "/api/v1/resource-plan/fao56",
        "/api/v1/farms/{farm_id}/health",
        "/api/v1/farms/{farm_id}/health/history",
        "/api/v1/farms/{farm_id}/health/recompute",
        "/api/v1/diagnose/crop-disease",
        "/api/v1/advisory/generate",
        "/api/v1/timeline/{farm_id}",
        "/api/v1/followup/checkin",
        "/api/v1/escalation/create",
        "/api/v1/agronomist/queue",
        "/api/v1/schemes/match",
        "/api/v1/weather/current",
    ]
    for route in expected_routes:
        assert route in paths, f"Route {route} not found in OpenAPI schema"


def test_stubs_and_error_envelope(client):
    # Call a scaffolded route that returns 501
    response = client.get("/api/v1/officer/queue")
    assert response.status_code == 501
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "NOT_IMPLEMENTED"


def test_config_settings():
    settings = get_settings()
    assert settings.CONFIDENCE_GATE == 0.70
    assert settings.RAG_RELEVANCE_THRESHOLD == 0.35
    assert settings.LAND_API_MODE in ["mock", "live"]
    assert settings.DIAGNOSIS_MODEL in ["real", "stub"]


def test_all_contract_enums():
    assert LandStatus.VERIFIED == "verified"
    assert HealthBand.UNRATED == "unrated"
    assert HealthBand.GOOD == "good"
    assert SubIndexKey.ACTIVE_PROBLEM_LOAD == "active_problem_load"
    assert ProblemSeverity.EARLY == "early"
    assert ProblemStatus.OPEN == "open"
    assert FollowupResponse.IMPROVED == "improved"
    assert CaseStatus.ESCALATED == "escalated"
    assert SchemeStatus.ACTIVE == "active"
    assert AssetKind.AUDIO_QUERY == "audio_query"
    assert UserRole.FARMER == "farmer"
    assert GateOutcome.COMPOSE == "compose"


@pytest.mark.asyncio
async def test_in_memory_repositories():
    user_repo = InMemoryUserRepository()
    user = await user_repo.save({"phone_number": "9876543210", "full_name": "Murugan"})
    assert user["id"] is not None
    fetched = await user_repo.get_by_phone("9876543210")
    assert fetched["full_name"] == "Murugan"


@pytest.mark.asyncio
async def test_stub_adapters():
    weather = StubWeatherAdapter()
    et0 = await weather.get_daily_et0(10.0, 78.0, None)
    assert et0 == 4.8

    embed = StubEmbeddingAdapter(dimension=1024)
    vec = await embed.embed_text("test")
    assert len(vec) == 1024

    diag = StubImageDiagnosisAdapter(confidence=0.92)
    label, conf, meta = await diag.diagnose_crop_image("asset_123")
    assert conf == 0.92
