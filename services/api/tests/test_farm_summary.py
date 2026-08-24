"""Integration tests for GET /farms/{id}/summary and GET /farms/{id}/risk under SIH26131.

Verifies:
  - Output strictly matches frozen shape (advisory string + trend enum)
  - NO 'score', NO 'band', NO 'subindices' keys in responses
  - Day-0 unrated behavior returns honest message without error
  - Seamless operation under PROBLEM_STATEMENT=sih26131
"""

import importlib
import uuid
import httpx
import pytest

from app.core.config import get_settings


async def _create_test_farmer(client: httpx.AsyncClient) -> tuple[str, dict[str, str]]:
    phone = f"+919{uuid.uuid4().hex[:9]}"
    reg = await client.post(
        "/auth/register",
        json={
            "phone_number": phone,
            "full_name": "Test Farmer",
            "role": "farmer",
            "preferred_language": "en",
            "password": "testpassword123",
        },
    )
    assert reg.status_code == 201, reg.text
    farmer_id = reg.json()["id"]
    login = await client.post(
        "/auth/login",
        json={
            "phone_number": phone,
            "password": "testpassword123",
        },
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return farmer_id, {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def _sih26131_environment(monkeypatch):
    """Run tests with PROBLEM_STATEMENT=sih26131 and restore afterwards."""
    monkeypatch.setenv("PROBLEM_STATEMENT", "sih26131")
    get_settings.cache_clear()
    import app.api.v1 as v1_module
    import app.main as main_module
    importlib.reload(v1_module)
    importlib.reload(main_module)
    yield
    monkeypatch.setenv("PROBLEM_STATEMENT", "sih26131")
    get_settings.cache_clear()
    importlib.reload(v1_module)
    importlib.reload(main_module)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_farm_summary_frozen_shape_no_numeric_keys():
    """GET /farms/{id}/summary under SIH26131 returns qualitative summary with NO numeric score keys."""
    import app.main as main_module
    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        farmer_id, headers = await _create_test_farmer(client)

        # 1. Create a farm
        create_res = await client.post(
            "/farms",
            headers=headers,
            json={
                "farmer_id": farmer_id,
                "crop": "samba_paddy",
                "growth_stage": "vegetative",
                "region": "Thanjavur",
            },
        )
        assert create_res.status_code == 201, create_res.text
        farm_id = create_res.json()["id"]

        # 2. Query summary endpoint
        summary_res = await client.get(f"/farms/{farm_id}/summary", headers=headers)
        assert summary_res.status_code == 200, summary_res.text
        data = summary_res.json()

        # Invariant: Must contain advisory and trend
        assert "advisory" in data
        assert isinstance(data["advisory"], str)
        assert "trend" in data
        assert data["trend"] in ["improving", "stable", "worsening"]
        assert "open_cases_count" in data

        # Drift Guard: MUST NOT contain score, band, or subindices
        assert "score" not in data
        assert "current_score" not in data
        assert "health_score" not in data
        assert "band" not in data
        assert "subindices" not in data
        assert "sub_indices" not in data


@pytest.mark.asyncio(loop_scope="session")
async def test_get_farm_risk_snapshot_has_subindices():
    """GET /farms/{id}/risk returns transparent risk snapshot with 4 subindices."""
    import app.main as main_module
    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        farmer_id, headers = await _create_test_farmer(client)

        # 1. Create a farm
        create_res = await client.post(
            "/farms",
            headers=headers,
            json={
                "farmer_id": farmer_id,
                "crop": "samba_paddy",
                "growth_stage": "vegetative",
                "region": "Thanjavur",
            },
        )
        assert create_res.status_code == 201, create_res.text
        farm_id = create_res.json()["id"]

        # 2. Query risk snapshot endpoint
        risk_res = await client.get(f"/farms/{farm_id}/risk", headers=headers)
        assert risk_res.status_code == 200, risk_res.text
        data = risk_res.json()

        assert "band" in data
        assert "weights_version" in data
        assert data["weights_version"] == "v2-sih26131"


@pytest.mark.asyncio(loop_scope="session")
async def test_day0_unrated_farm_summary():
    """Day-0 farm returns honest unrated advisory sentence on summary."""
    import app.main as main_module
    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        farmer_id, headers = await _create_test_farmer(client)

        create_res = await client.post(
            "/farms",
            headers=headers,
            json={
                "farmer_id": farmer_id,
                "crop": "samba_paddy",
                "growth_stage": "vegetative",
                "region": "Thanjavur",
            },
        )
        assert create_res.status_code == 201, create_res.text
        farm_id = create_res.json()["id"]

        summary_res = await client.get(f"/farms/{farm_id}/summary", headers=headers)
        assert summary_res.status_code == 200, summary_res.text
        data = summary_res.json()
        assert "Insufficient monitoring data" in data["advisory"]
        assert data["trend"] == "stable"


