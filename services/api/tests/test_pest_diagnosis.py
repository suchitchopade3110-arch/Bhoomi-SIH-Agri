"""Integration tests for pest diagnosis via POST /farms/{id}/diagnose with
target_type="pest" (SIH26131 delta spec §3.1).

The image adapter isn't target-type-aware (see diagnosis_service.py's
module docstring), so these tests drive it directly via the shared stub
singleton's ``set_label``/``set_confidence`` — the same pattern
StubImageDiagnosisAdapter's own docstring names for exercising the
out-of-scope branch. Always restored in a ``finally`` so other tests in
the suite keep seeing the default disease label.
"""

import uuid

import httpx
import pytest

from app.adapters.dependencies import get_image_diagnosis_adapter


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
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def _create_farm(client: httpx.AsyncClient, headers: dict[str, str]) -> str:
    res = await client.post(
        "/farms",
        headers=headers,
        json={
            "farmer_id": str(uuid.uuid4()),
            "crop": "samba_paddy",
            "growth_stage": "vegetative",
            "region": "Erode",
        },
    )
    assert res.status_code == 201, res.text
    return res.json()["id"]


@pytest.mark.asyncio(loop_scope="session")
async def test_in_scope_pest_above_gate_escalates_on_no_corpus_never_fabricates():
    """stem_borer is a valid pest label and 0.85 clears PEST_CONFIDENCE_GATE
    (0.70 default) — but the ingested corpus has zero pest documents, so
    this must still honestly escalate (NO_RELEVANT_SOURCE), never compose
    fabricated pest advice."""
    import app.main as main_module

    adapter = get_image_diagnosis_adapter()
    original_label, original_confidence = adapter.label, adapter.confidence
    adapter.set_label("stem_borer")
    adapter.set_confidence(0.85)
    try:
        transport = httpx.ASGITransport(app=main_module.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
            headers = await _register_and_login(client)
            farm_id = await _create_farm(client, headers)

            res = await client.post(
                f"/farms/{farm_id}/diagnose",
                headers=headers,
                json={"image_asset_id": "pest-photo-1", "target_type": "pest"},
            )
            assert res.status_code == 200, res.text
            body = res.json()
            assert body["above_gate"] is False
            assert body["gate"]["reason_code"] == "NO_RELEVANT_SOURCE"
            assert body["gate"]["threshold"] == 0.70
            assert body["escalation"] is not None
    finally:
        adapter.set_label(original_label)
        adapter.set_confidence(original_confidence)


@pytest.mark.asyncio(loop_scope="session")
async def test_pest_label_out_of_scope_for_disease_target_type():
    """The same in-scope pest label is OUT_OF_SCOPE_TARGET when the request
    declares target_type="disease" — proves the scope list genuinely
    differs by target_type, not just accepting every label."""
    import app.main as main_module

    adapter = get_image_diagnosis_adapter()
    original_label, original_confidence = adapter.label, adapter.confidence
    adapter.set_label("stem_borer")
    adapter.set_confidence(0.85)
    try:
        transport = httpx.ASGITransport(app=main_module.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
            headers = await _register_and_login(client)
            farm_id = await _create_farm(client, headers)

            res = await client.post(
                f"/farms/{farm_id}/diagnose",
                headers=headers,
                json={"image_asset_id": "pest-photo-2", "target_type": "disease"},
            )
            assert res.status_code == 200, res.text
            body = res.json()
            assert body["above_gate"] is False
            assert body["gate"]["reason_code"] == "OUT_OF_SCOPE_TARGET"
    finally:
        adapter.set_label(original_label)
        adapter.set_confidence(original_confidence)


@pytest.mark.asyncio(loop_scope="session")
async def test_disease_label_out_of_scope_for_pest_target_type():
    """The default disease label is OUT_OF_SCOPE_TARGET under target_type="pest"."""
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        headers = await _register_and_login(client)
        farm_id = await _create_farm(client, headers)

        res = await client.post(
            f"/farms/{farm_id}/diagnose",
            headers=headers,
            json={"image_asset_id": "pest-photo-3", "target_type": "pest"},
        )
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["above_gate"] is False
        assert body["gate"]["reason_code"] == "OUT_OF_SCOPE_TARGET"


@pytest.mark.asyncio(loop_scope="session")
async def test_pest_below_confidence_gate_uses_pest_threshold():
    """A confidence between the two gates would pass a lower disease gate
    but must still fail if PEST_CONFIDENCE_GATE is higher — proves the
    pest-specific threshold, not the disease one, is what's enforced."""
    import app.main as main_module
    from app.core.config import get_settings

    settings = get_settings()
    adapter = get_image_diagnosis_adapter()
    original_label, original_confidence = adapter.label, adapter.confidence
    adapter.set_label("stem_borer")
    adapter.set_confidence(settings.PEST_CONFIDENCE_GATE - 0.05)
    try:
        transport = httpx.ASGITransport(app=main_module.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
            headers = await _register_and_login(client)
            farm_id = await _create_farm(client, headers)

            res = await client.post(
                f"/farms/{farm_id}/diagnose",
                headers=headers,
                json={"image_asset_id": "pest-photo-4", "target_type": "pest"},
            )
            assert res.status_code == 200, res.text
            body = res.json()
            assert body["above_gate"] is False
            assert body["gate"]["reason_code"] == "BELOW_CONFIDENCE_GATE"
            assert body["gate"]["threshold"] == settings.PEST_CONFIDENCE_GATE
    finally:
        adapter.set_label(original_label)
        adapter.set_confidence(original_confidence)
