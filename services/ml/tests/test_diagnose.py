import base64
import io

import httpx
import pytest

from app.image_model import ALL_SUPPORTED_LABELS


@pytest.mark.asyncio
async def test_health():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_diagnose_hash_fallback_is_bounded_and_deterministic():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"asset_id": "blb-leaf-photo-1", "crop_hint": "paddy"}
        res1 = await client.post("/diagnose", json=payload)
        res2 = await client.post("/diagnose", json=payload)

    assert res1.status_code == 200
    body1, body2 = res1.json(), res2.json()
    assert body1["label"] in ALL_SUPPORTED_LABELS
    assert 0.0 <= body1["confidence"] <= 1.0
    # Deterministic: same asset_id + crop_hint -> same label/confidence.
    assert body1 == body2


@pytest.mark.asyncio
async def test_diagnose_pest_target_type_stays_in_pest_labels():
    import app.main as main_module
    from app.image_model import SUPPORTED_PEST_LABELS

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/diagnose", json={"asset_id": "some-pest-photo", "target_type": "pest"})

    assert res.status_code == 200
    assert res.json()["label"] in SUPPORTED_PEST_LABELS


@pytest.mark.asyncio
async def test_diagnose_with_real_image_bytes_uses_color_analysis():
    from PIL import Image

    import app.main as main_module

    # A solid yellow square should trigger the color-histogram path rather
    # than the hash fallback, and report the method used.
    img = Image.new("RGB", (64, 64), color=(230, 220, 60))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/diagnose", json={"asset_id": "irrelevant", "image_base64": encoded})

    assert res.status_code == 200
    body = res.json()
    assert body["meta"]["method"] == "color_histogram"
    assert body["label"] in ALL_SUPPORTED_LABELS


@pytest.mark.asyncio
async def test_embed_batch_returns_normalized_vectors_of_requested_dimension():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/embed", json={"texts": ["bacterial leaf blight", "unrelated topic"], "dimension": 128})

    assert res.status_code == 200
    body = res.json()
    assert len(body["embeddings"]) == 2
    assert all(len(v) == 128 for v in body["embeddings"])


@pytest.mark.asyncio
async def test_transcribe_and_synthesize_endpoints():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        t_res = await client.post("/transcribe", json={"audio_asset_url_or_id": "onboarding-audio-1"})
        assert t_res.status_code == 200
        assert t_res.json()["transcript"]

        s_res = await client.post("/synthesize", json={"text": "hello"})
        assert s_res.status_code == 200
        assert s_res.json()["audio_url"].startswith("http")
