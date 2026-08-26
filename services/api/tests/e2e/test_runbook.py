"""End-to-end integration test for the full Bhoomi runbook (Phase 5 DoD).

Drives the real FastAPI app in-process (ASGI transport, no network) against
the real Postgres database configured by ``DATABASE_URL`` — every layer is
exercised for real: Postgres-backed repositories, the confidence gate, RAG
retrieval against the ingested pgvector corpus, and the deterministic health
engine. Requires migrations applied and the RAG corpus ingested first (see
``Makefile`` targets ``migrate`` / ``ingest-corpus``, or just ``make smoke``).

Runbook, in order (SIH26131 feature checklist §15 / docs/specs/suchit_module_specs_sih26131.md §1.5):

    onboard (3-field: crop/growth_stage/region) -> land queues for HITL
    (no auto-lookup) -> officer verifies -> baseline health 82 -> diagnose
    above gate, cited -> 73 -> follow-up got_worse -> severity promotes,
    auto-escalate -> 57 -> agronomist resolves -> 91 -> verified profile
    matches a dated scheme.

    This is the same reconciliation walk domain-level-verified by
    tests/domain/test_health_score.py::test_sih26131_reconciliation, driven
    here over real HTTP against a real Postgres instead of calling
    compute_health() directly. Weather is forced unavailable for the
    duration of this test (a real, documented degraded-mode input path —
    see HealthService._get_weather_or_fallback — not a fabricated one) so
    environmental_risk stays at its neutral default (70) the whole walk,
    exactly matching the domain fixture; the stub weather adapter's fixed
    30C/75% reading otherwise falls inside SIH26131's default crop-ideal
    band and would score environmental_risk=100, producing a different
    (also real, just not this specific canonical) walk.

Uses a fresh, randomized phone number per run so the test is safe to run
repeatedly against the same database without unique-constraint collisions.
"""

from datetime import date, timedelta
from typing import Any
import uuid

import httpx
import pytest

from app.adapters.dependencies import get_weather_adapter
from app.core.db import AsyncSessionLocal
from app.core.enums import SchemeStatus
from app.main import app
from app.models.scheme import Scheme

BASE_URL = "http://test/api/v1"


class _WeatherUnavailableAdapter:
    """Simulates WeatherPort being unavailable (PRD §1.4 degraded mode) —
    HealthService._get_weather_or_fallback treats a falsy reading as "no
    live weather," which is exactly the input the SIH26131 reconciliation
    fixture (spec §1.5) is written against (weather=None -> environmental_risk
    stays at its ENVIRONMENTAL_RISK_DEFAULT=70 baseline throughout)."""

    async def get_current_weather(self, latitude: float | None, longitude: float | None) -> dict[str, Any]:
        return {}
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
async def test_full_runbook_walks_82_73_57_91():
    """SIH26131 core-loop runbook, end to end over real HTTP: 82 -> 73 ->
    57 -> 91, matching docs/specs/suchit_module_specs_sih26131.md §1.5 and
    tests/domain/test_health_score.py::test_sih26131_reconciliation exactly
    — same numbers, this time proven through the real FastAPI app, real
    Postgres, real gate, and real RAG retrieval instead of a direct
    compute_health() call."""
    await _ensure_matching_scheme_exists()

    app.dependency_overrides[get_weather_adapter] = lambda: _WeatherUnavailableAdapter()
    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as client:
            farmer_token = await _register_and_login(client, _unique_phone("9"), "Ramesh", "farmer")
            officer_token = await _register_and_login(client, _unique_phone("8"), "Officer Kumar", "officer")
            agronomist_token = await _register_and_login(client, _unique_phone("7"), "Dr. Lakshmi", "agronomist")

            # --- 1. Onboard: 3-field SIH26131 onboarding (checklist §1) ---
            resp = await client.post(
                "/farms",
                headers=_auth(farmer_token),
                json={"farmer_id": "placeholder", "crop": "samba_paddy", "growth_stage": "vegetative", "region": "Erode"},
            )
            assert resp.status_code == 201, resp.text
            farm = resp.json()
            farm_id = farm["id"]
            assert farm["land_status"] == "unverified"
            assert farm["primary_crop"] == "samba_paddy"

            # --- 2. Land submission -> always queues to officer (checklist §10.1/§13) ---
            resp = await client.post(
                "/land/verify",
                headers=_auth(farmer_token),
                json={"farm_id": farm_id, "survey_number": UNLISTED_SURVEY_NUMBER},
            )
            assert resp.status_code == 202, resp.text
            assert resp.json()["status"] == "pending_review"

            # --- 3. Officer verifies — approve/reject + reason only, no boundary (checklist §10.2) ---
            resp = await client.get("/officer/queue", headers=_auth(officer_token))
            assert resp.status_code == 200
            queue_items = [item for item in resp.json() if item["farm_id"] == farm_id]
            assert len(queue_items) == 1
            parcel_id = queue_items[0]["parcel_id"]

            resp = await client.post(
                "/officer/action",
                headers=_auth(officer_token),
                json={"parcel_id": parcel_id, "action": "verified", "officer_notes": "Survey number confirmed."},
            )
            assert resp.status_code == 200
            assert resp.json()["status"] == "verified"

            resp = await client.get(f"/farms/{farm_id}", headers=_auth(farmer_token))
            assert resp.json()["land_status"] == "verified"

            # --- 4. Baseline risk == 82 / good (SIH26131 spec §1.5) --------
            resp = await client.get(f"/farms/{farm_id}/risk", headers=_auth(farmer_token))
            health = resp.json()
            assert health["score"] == 82, health
            assert health["band"] == "good"

            # --- 5. Diagnose above gate, cited 5-point advisory -> 73 ------
            # Real client behavior: presign the asset before referencing it —
            # diagnose() now verifies image_asset_id was actually created via
            # this flow (checklist §2.5), so a bare literal like "a_9" that
            # was never presigned would 422.
            resp = await client.post(
                "/assets/presigned-url",
                headers=_auth(farmer_token),
                json={"file_name": "leaf.jpg", "content_type": "image/jpeg", "asset_kind": "disease_photo", "farm_id": farm_id},
            )
            assert resp.status_code == 201, resp.text
            image_asset_id = resp.json()["asset_id"]

            resp = await client.post(
                f"/farms/{farm_id}/diagnose",
                headers=_auth(farmer_token),
                json={"image_asset_id": image_asset_id, "description_text": "yellow water-soaked lesions on leaf tips"},
            )
            assert resp.status_code == 200, resp.text
            diagnosis = resp.json()
            assert diagnosis["above_gate"] is True
            assert diagnosis["reason"] is None
            assert diagnosis["escalation"] is None
            assert len(diagnosis["citations"]) > 0
            # "What to avoid" is first in the advisory (never-cut, checklist §4).
            assert diagnosis["advisory"] is not None
            assert list(diagnosis["advisory"].keys())[0] == "what_to_avoid"
            assert diagnosis["health_delta"] == {"from": 82, "to": 73}

            resp = await client.get(f"/farms/{farm_id}/risk", headers=_auth(farmer_token))
            health = resp.json()
            assert health["score"] == 73, health
            assert health["band"] == "watch"

            # --- 6. Follow-up got_worse -> severity promotes, auto-escalate -> 57 ---
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
            assert followup["severity_change"] == {"from": "early", "to": "moderate"}
            assert followup["risk"]["from"] == 73
            assert followup["risk"]["to"] == 57
            assert followup["risk"]["band"] == "poor"
            assert followup["updated_health_snapshot"]["score"] == 57

            # --- 7. Agronomist resolves -> 91 -------------------------------
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
            resolution = resp.json()
            assert resolution["status"] == "resolved"
            assert resolution["risk"]["from"] == 57
            assert resolution["risk"]["to"] == 91
            assert resolution["risk"]["band"] == "excellent"

            resp = await client.get(f"/farms/{farm_id}/risk", headers=_auth(farmer_token))
            health = resp.json()
            assert health["score"] == 91, health
            assert health["band"] == "excellent"

            # --- The 82 -> 73 -> 57 -> 91 walk, asserted end to end (SIH26131 spec §1.5) --
            assert (
                diagnosis["health_delta"]["from"] == 82
                and diagnosis["health_delta"]["to"] == 73
                and followup["updated_health_snapshot"]["score"] == 57
                and health["score"] == 91
            )

            # --- 8. Verified profile matches a dated scheme -----------------
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
    finally:
        app.dependency_overrides.pop(get_weather_adapter, None)


@pytest.mark.asyncio(loop_scope="session")
async def test_land_verify_always_queues_for_officer_review():
    """SIH26131 feature checklist §10.1/§13.2/§13.3: no automated cadastral
    lookup, no auto-verify — every /land/verify submission queues to the
    officer (202, pending_review), regardless of survey number."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as client:
        farmer_token = await _register_and_login(client, _unique_phone("6"), "Flag Test Farmer", "farmer")

        resp = await client.post(
            "/farms",
            headers=_auth(farmer_token),
            json={"farmer_id": "placeholder", "crop": "samba_paddy", "growth_stage": "vegetative", "region": "Erode"},
        )
        farm_id = resp.json()["id"]

        resp = await client.post(
            "/land/verify",
            headers=_auth(farmer_token),
            json={"farm_id": farm_id, "survey_number": "88/2A"},
        )
        assert resp.status_code == 202, resp.text
        assert resp.json()["status"] == "pending_review"
