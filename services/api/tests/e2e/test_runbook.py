"""End-to-end integration test for the full Bhoomi runbook (Phase 5 DoD).

Drives the real FastAPI app in-process (ASGI transport, no network) against
the real Postgres database configured by ``DATABASE_URL`` — every layer is
exercised for real: Postgres-backed repositories, the confidence gate, RAG
retrieval against the ingested pgvector corpus, and the deterministic health
engine. Requires migrations applied and the RAG corpus ingested first (see
``Makefile`` targets ``migrate`` / ``ingest-corpus``, or just ``make smoke``).

Runbook, in order (PRD §6 / §7.4's own worked example):

    onboard (unrated) -> land fails -> officer verifies -> resource plan
    (FAO-56 inputs inspectable) -> baseline health 82 -> diagnose day 22
    above gate, cited -> 68 -> follow-up got_worse -> auto-escalate ->
    agronomist resolves -> 86 -> verified profile matches a dated scheme.

Uses a fresh, randomized phone number per run so the test is safe to run
repeatedly against the same database without unique-constraint collisions.
"""

from datetime import date, timedelta
import uuid

import httpx
import pytest

from app.core.db import AsyncSessionLocal
from app.core.enums import SchemeStatus
from app.main import app
from app.models.scheme import Scheme

BASE_URL = "http://test/api/v1"
DEMO_PASSWORD = "e2e-test-pass-1234"

# Not on MockLandRegistryAdapter's whitelist (app/adapters/land_registry.py)
# -> auto-lookup fails -> HITL, the common path per contract §2.7.
UNLISTED_SURVEY_NUMBER = "142/3B"


async def _ensure_matching_scheme_exists() -> None:
    """The e2e test must not depend on `make seed` having been run first —
    insert a minimal dated scheme directly if none matching exists yet, so
    step 9 (scheme discovery) is self-contained."""
    async with AsyncSessionLocal() as session:
        session.add(
            Scheme(
                name=f"E2E Test Crop Protection Subsidy {uuid.uuid4().hex[:8]}",
                ministry="Tamil Nadu Department of Agriculture",
                jurisdiction="TN",
                description="Subsidy toward approved crop-protection inputs for paddy smallholders.",
                benefits="Up to 50% subsidy on approved bactericide/fungicide purchases, capped per acre.",
                eligibility_criteria={"crop": "samba_paddy", "category": "Small/Marginal"},
                subsidy_percentage=50.0,
                max_amount_inr=5000.0,
                status=SchemeStatus.ACTIVE.value,
                last_verified=date.today() - timedelta(days=20),
                crop_filter="samba_paddy",
                category_filter="Small/Marginal",
            )
        )
        await session.commit()


def _unique_phone(tag: str) -> str:
    # +91 followed by 10 digits, always unique per test run.
    return "+91" + tag + uuid.uuid4().hex[:10 - len(tag)]


async def _register_and_login(client: httpx.AsyncClient, phone: str, name: str, role: str) -> str:
    resp = await client.post(
        "/auth/register",
        json={
            "phone_number": phone,
            "full_name": name,
            "role": role,
            "preferred_language": "ta",
            "password": DEMO_PASSWORD,
        },
    )
    assert resp.status_code == 201, resp.text

    resp = await client.post("/auth/login", json={"phone_number": phone, "password": DEMO_PASSWORD})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio(loop_scope="session")
async def test_full_runbook_walks_82_68_86():
    await _ensure_matching_scheme_exists()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as client:
        farmer_token = await _register_and_login(client, _unique_phone("9"), "Ramesh", "farmer")
        officer_token = await _register_and_login(client, _unique_phone("8"), "Officer Kumar", "officer")
        agronomist_token = await _register_and_login(client, _unique_phone("7"), "Dr. Lakshmi", "agronomist")

        # --- 1. Onboard -> unrated (PRD §5.2, §7.1) --------------------
        resp = await client.post(
            "/farms",
            headers=_auth(farmer_token),
            json={
                "farmer_id": "placeholder",
                "farm_name": "Ramesh's Paddy Farm",
                "village": "Chithode",
                "taluk": "Erode",
                "district": "Erode",
                "state": "Tamil Nadu",
                "latitude": 11.34,
                "longitude": 77.71,
                "total_area_acres": 2.0,
                "survey_number": UNLISTED_SURVEY_NUMBER,
                "primary_crop": "samba_paddy",
                "growth_stage": "vegetative",
                "soil_type": "clay_loam",
                "irrigation_source": "canal",
                "soil_moisture_pct": 45.0,
                "days_since_planting": 20,
                "days_since_last_scan": 2,
            },
        )
        assert resp.status_code == 201, resp.text
        farm = resp.json()
        farm_id = farm["id"]
        assert farm["land_status"] == "unverified"

        resp = await client.get(f"/farms/{farm_id}/health", headers=_auth(farmer_token))
        assert resp.status_code == 200
        health = resp.json()
        assert health["score"] is None
        assert health["band"] == "unrated"
        assert "irrigation_delivered_mm" in health["missing_fields"]

        # --- 2. Land fails auto-lookup -> queued to officer (202) ------
        resp = await client.post(
            "/land/verify",
            headers=_auth(farmer_token),
            json={"farm_id": farm_id, "survey_number": UNLISTED_SURVEY_NUMBER},
        )
        assert resp.status_code == 202, resp.text
        assert resp.json()["status"] == "pending_review"

        # --- 3. Officer verifies (HITL, contract §2.7) -----------------
        resp = await client.get("/officer/queue", headers=_auth(officer_token))
        assert resp.status_code == 200
        queue_items = [item for item in resp.json() if item["farm_id"] == farm_id]
        assert len(queue_items) == 1
        parcel_id = queue_items[0]["parcel_id"]

        resp = await client.post(
            "/officer/action",
            headers=_auth(officer_token),
            json={
                "parcel_id": parcel_id,
                "action": "verified",
                "confirmed_boundary_geojson": {
                    "type": "Polygon",
                    "coordinates": [[[77.71, 11.34], [77.712, 11.34], [77.712, 11.342], [77.71, 11.342], [77.71, 11.34]]],
                },
            },
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "verified"

        resp = await client.get(f"/farms/{farm_id}", headers=_auth(farmer_token))
        assert resp.json()["land_status"] == "verified"

        # --- 4. Resource plan — FAO-56 inputs all inspectable ----------
        resp = await client.post(f"/resource-plan/{farm_id}", headers=_auth(farmer_token))
        assert resp.status_code == 200, resp.text
        plan = resp.json()["irrigation_plan"]
        for field in ("et0_mm_day", "kc_factor", "etc_mm_day", "effective_rainfall_mm", "irrigation_need_mm", "daily_liters_total"):
            assert field in plan and plan[field] is not None

        # --- 5. Baseline health == 82 / good ----------------------------
        resp = await client.get(f"/farms/{farm_id}/health", headers=_auth(farmer_token))
        health = resp.json()
        assert health["score"] == 82
        assert health["band"] == "good"

        # --- 6. Diagnose (Day 22) above gate, cited -> 68 --------------
        resp = await client.post(
            f"/farms/{farm_id}/diagnose",
            headers=_auth(farmer_token),
            json={"image_asset_id": "a_9", "description_text": "yellow water-soaked lesions on leaf tips"},
        )
        assert resp.status_code == 200, resp.text
        diagnosis = resp.json()
        assert diagnosis["above_gate"] is True
        assert diagnosis["reason"] is None
        assert diagnosis["escalation"] is None
        assert len(diagnosis["citations"]) > 0
        assert diagnosis["health_delta"] == {"from": 82, "to": 68}

        resp = await client.get(f"/farms/{farm_id}/health", headers=_auth(farmer_token))
        health = resp.json()
        assert health["score"] == 68
        assert health["band"] == "watch"

        # --- 7. Follow-up: got_worse -> auto-escalate -------------------
        resp = await client.post(
            "/followup/checkin",
            headers=_auth(farmer_token),
            json={"farm_id": farm_id, "response": "got_worse"},
        )
        assert resp.status_code == 200, resp.text
        followup = resp.json()
        assert followup["auto_escalated"] is True
        case_id = followup["escalation_id"]
        assert case_id is not None
        # Score fell further than the diagnosis alone (severity promoted
        # early -> moderate, treatment-response penalized) — PRD §7.4.
        assert followup["updated_health_snapshot"]["score"] < 68

        # --- 8. Agronomist resolves -> 86 -------------------------------
        resp = await client.get("/agronomist/queue", headers=_auth(agronomist_token))
        assert resp.status_code == 200
        queue_case_ids = [c["escalation_id"] for c in resp.json()]
        assert case_id in queue_case_ids

        resp = await client.post(
            "/agronomist/resolve",
            headers=_auth(agronomist_token),
            json={
                "escalation_id": case_id,
                "agronomist_id": "a1",
                "agronomist_name": "Dr. Lakshmi",
                "confirmed_diagnosis": "Confirmed bacterial leaf blight, moderate.",
                "expert_advice": "Copper-based bactericide per label; drain and dry field 48h.",
                "prescribed_inputs": ["copper oxychloride"],
            },
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["status"] == "resolved"

        resp = await client.get(f"/farms/{farm_id}/health", headers=_auth(farmer_token))
        health = resp.json()
        assert health["score"] == 86
        assert health["band"] == "good"

        # --- The 82 -> 68 -> 86 walk, asserted end to end (PRD §7.4/§7.6) --
        assert (
            diagnosis["health_delta"]["from"] == 82
            and diagnosis["health_delta"]["to"] == 68
            and health["score"] == 86
        )

        # --- 9. Verified profile matches a dated scheme -----------------
        resp = await client.post(
            "/schemes/match",
            headers=_auth(farmer_token),
            json={"farm_id": farm_id},
        )
        assert resp.status_code == 200, resp.text
        schemes = resp.json()
        assert schemes["match_count"] >= 1
        for scheme in schemes["matched_schemes"]:
            assert scheme["last_verified"] is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_land_api_mode_flag_demos_both_paths(monkeypatch):
    """Contract §1.5: flipping LAND_API_MODE alone — no input change — shows
    both the auto-lookup-succeeds (200, verified) and auto-lookup-fails
    (202, queued to officer) response shapes from the same build."""
    from app.adapters import dependencies as adapters_deps
    from app.adapters.land_registry import LiveLandRegistryAdapter, MockLandRegistryAdapter

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as client:
        farmer_token = await _register_and_login(client, _unique_phone("6"), "Flag Test Farmer", "farmer")

        resp = await client.post(
            "/farms",
            headers=_auth(farmer_token),
            json={
                "farmer_id": "placeholder",
                "farm_name": "Flag Test Farm",
                "village": "Chithode",
                "taluk": "Erode",
                "district": "Erode",
                "latitude": 11.34,
                "longitude": 77.71,
                "total_area_acres": 1.0,
                "primary_crop": "samba_paddy",
            },
        )
        farm_id = resp.json()["id"]
        whitelisted_survey_number = "88/2A"  # app/adapters/land_registry.py MOCK_KNOWN_SURVEY_NUMBERS

        app.dependency_overrides[adapters_deps.get_land_registry_adapter] = lambda: MockLandRegistryAdapter()
        try:
            resp = await client.post(
                "/land/verify",
                headers=_auth(farmer_token),
                json={"farm_id": farm_id, "survey_number": whitelisted_survey_number},
            )
            assert resp.status_code == 200, resp.text
            assert resp.json()["status"] == "verified"
        finally:
            app.dependency_overrides.pop(adapters_deps.get_land_registry_adapter, None)

        # Second farm — same whitelisted survey number, but now LAND_API_MODE=live.
        resp = await client.post(
            "/farms",
            headers=_auth(farmer_token),
            json={
                "farmer_id": "placeholder",
                "farm_name": "Flag Test Farm 2",
                "village": "Chithode",
                "taluk": "Erode",
                "district": "Erode",
                "latitude": 11.34,
                "longitude": 77.71,
                "total_area_acres": 1.0,
                "primary_crop": "samba_paddy",
            },
        )
        farm_id_2 = resp.json()["id"]

        app.dependency_overrides[adapters_deps.get_land_registry_adapter] = lambda: LiveLandRegistryAdapter()
        try:
            resp = await client.post(
                "/land/verify",
                headers=_auth(farmer_token),
                json={"farm_id": farm_id_2, "survey_number": whitelisted_survey_number},
            )
            assert resp.status_code == 202, resp.text
            assert resp.json()["status"] == "pending_review"
        finally:
            app.dependency_overrides.pop(adapters_deps.get_land_registry_adapter, None)
