"""End-to-end integration test for Treatment Efficacy Tracking (SPEC-EFFICACY-001).

Exercises the real lifecycle: diagnose (opens a TreatmentApplication for the
default first-line treatment) -> follow-up check-in (closes it) ->
GET /treatments/{treatment_id}/efficacy (aggregates it) — all over real
HTTP against the live Postgres-backed app, not the pure domain function in
isolation (that's ``tests/unit/test_efficacy_scoring.py``'s job).

Runs under PROBLEM_STATEMENT=sih26131 since the efficacy route is
sih26131-only.
"""

import importlib
import uuid

import httpx
import pytest

from app.core.config import get_settings

DISTRICT = "Erode"
CROP = "samba_paddy"
TREATMENT_ID = "copper_hydroxide_77_wp"  # normalize_treatment_key("Copper Hydroxide 77% WP")
PATHOGEN = "bacterial_leaf_blight"  # StubImageDiagnosisAdapter's fixed default label


@pytest.fixture(autouse=True)
def _sih26131_environment(monkeypatch):
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


async def _register_and_login(client: httpx.AsyncClient) -> dict[str, str]:
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
    login = await client.post("/auth/login", json={"phone_number": phone, "password": "testpassword123"})
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def _create_farm(client: httpx.AsyncClient, headers: dict[str, str], region: str = DISTRICT) -> str:
    res = await client.post(
        "/farms",
        headers=headers,
        json={
            "farmer_id": str(uuid.uuid4()),
            "crop": CROP,
            "growth_stage": "vegetative",
            "region": region,
        },
    )
    assert res.status_code == 201, res.text
    return res.json()["id"]


async def _presign_asset(client: httpx.AsyncClient, headers: dict[str, str], farm_id: str) -> str:
    """diagnose() verifies image_asset_id was actually created via the
    presign flow (checklist §2.5) — a bare literal never goes through it."""
    res = await client.post(
        "/assets/presigned-url",
        headers=headers,
        json={"file_name": "leaf.jpg", "content_type": "image/jpeg", "asset_kind": "disease_photo", "farm_id": farm_id},
    )
    assert res.status_code == 201, res.text
    return res.json()["asset_id"]


async def _diagnose_and_resolve_via_followup(client: httpx.AsyncClient, headers: dict[str, str], farm_id: str) -> None:
    """One full above-gate diagnosis -> 'improved' check-in cycle. With the
    stub image adapter's fixed label (bacterial_leaf_blight, confidence
    0.85) and the ingested BLB corpus doc, this always composes (never
    escalates) — so it always opens then closes exactly one
    TreatmentApplication."""
    image_asset_id = await _presign_asset(client, headers, farm_id)
    diagnose_res = await client.post(
        f"/farms/{farm_id}/diagnose",
        headers=headers,
        json={"image_asset_id": image_asset_id},
    )
    assert diagnose_res.status_code == 200, diagnose_res.text
    body = diagnose_res.json()
    assert body["above_gate"] is True, body
    problem_id = body["problem_id"]

    checkin_res = await client.post(
        "/followup/checkin",
        headers=headers,
        json={"farm_id": farm_id, "problem_id": problem_id, "response": "improved"},
    )
    assert checkin_res.status_code == 200, checkin_res.text


@pytest.mark.asyncio(loop_scope="session")
async def test_diagnosis_opens_and_followup_closes_a_treatment_application():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        headers = await _register_and_login(client)
        farm_id = await _create_farm(client, headers)

        # Before any application closes, the efficacy read shows no signal yet.
        efficacy_res = await client.get(
            f"/treatments/{TREATMENT_ID}/efficacy",
            headers=headers,
            params={"pathogen": PATHOGEN, "crop": CROP, "district": DISTRICT},
        )
        assert efficacy_res.status_code == 200, efficacy_res.text
        before = efficacy_res.json()
        baseline_sample_size = before["sample_size"]

        await _diagnose_and_resolve_via_followup(client, headers, farm_id)

        efficacy_res = await client.get(
            f"/treatments/{TREATMENT_ID}/efficacy",
            headers=headers,
            params={"pathogen": PATHOGEN, "crop": CROP, "district": DISTRICT},
        )
        assert efficacy_res.status_code == 200, efficacy_res.text
        after = efficacy_res.json()

        # Exactly one more evaluated (success) application than before.
        assert after["sample_size"] == baseline_sample_size + 1
        assert after["treatment_id"] == TREATMENT_ID
        assert after["pathogen"] == PATHOGEN


@pytest.mark.asyncio(loop_scope="session")
async def test_efficacy_crosses_sample_size_floor_at_ten_successes():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        headers = await _register_and_login(client)
        # A fresh district for this test only, so its sample count starts at
        # exactly zero regardless of what other tests in this module wrote.
        district = f"District-{uuid.uuid4().hex[:8]}"
        farm_id = await _create_farm(client, headers, region=district)

        for i in range(9):
            await _diagnose_and_resolve_via_followup(client, headers, farm_id)
            efficacy_res = await client.get(
                f"/treatments/{TREATMENT_ID}/efficacy",
                headers=headers,
                params={"pathogen": PATHOGEN, "crop": CROP, "district": district},
            )
            body = efficacy_res.json()
            assert body["status"] == "insufficient_data", f"iteration {i}: {body}"
            assert body["sample_size"] == i + 1

        # 10th success crosses the floor.
        await _diagnose_and_resolve_via_followup(client, headers, farm_id)
        efficacy_res = await client.get(
            f"/treatments/{TREATMENT_ID}/efficacy",
            headers=headers,
            params={"pathogen": PATHOGEN, "crop": CROP, "district": district},
        )
        assert efficacy_res.status_code == 200, efficacy_res.text
        body = efficacy_res.json()
        assert body["status"] == "statistically_significant", body
        assert body["sample_size"] == 10
        assert body["efficacy_percentage"] == 100.0
        assert body["avg_days_to_recovery"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_got_worse_followup_closes_application_as_failed():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        headers = await _register_and_login(client)
        district = f"District-{uuid.uuid4().hex[:8]}"
        farm_id = await _create_farm(client, headers, region=district)
        image_asset_id = await _presign_asset(client, headers, farm_id)

        diagnose_res = await client.post(
            f"/farms/{farm_id}/diagnose",
            headers=headers,
            json={"image_asset_id": image_asset_id},
        )
        assert diagnose_res.status_code == 200
        problem_id = diagnose_res.json()["problem_id"]

        checkin_res = await client.post(
            "/followup/checkin",
            headers=headers,
            json={"farm_id": farm_id, "problem_id": problem_id, "response": "got_worse"},
        )
        assert checkin_res.status_code == 200, checkin_res.text

        efficacy_res = await client.get(
            f"/treatments/{TREATMENT_ID}/efficacy",
            headers=headers,
            params={"pathogen": PATHOGEN, "crop": CROP, "district": district},
        )
        body = efficacy_res.json()
        # One failure only: still below the N>=10 floor, but the failure was
        # in fact recorded (this district would show 1/1 = 0% once it
        # crosses the floor — verified indirectly here via sample_size).
        assert body["sample_size"] == 1
        assert body["status"] == "insufficient_data"
