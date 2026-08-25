"""Bhoomi ML inference microservice.

Real integration point for ``services/api``'s ``DIAGNOSIS_MODEL=real``
(``adapters/image_diagnosis_real.py`` calls ``POST {ML_SERVICE_URL}/diagnose``).
See ``app/image_model.py`` for exactly what "diagnose" means here — a bounded
heuristic, not a trained CV model; there is no labeled dataset or model
weights checked into this repo (README.md §9 "Known gaps").

``/embed`` and ``/transcribe``+``/synthesize`` are also exposed (matching
services/api's ``EmbeddingPort``/``AsrTtsPort`` contracts) for future wiring,
but neither is called by services/api today — see their modules' docstrings.

Run: ``uvicorn app.main:app --port 8001`` (matches the default
``ML_SERVICE_URL=http://localhost:8001`` in services/api/app/core/config.py).
"""

from __future__ import annotations

import base64
import logging

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.asr_tts import synthesize, transcribe
from app.embeddings import DEFAULT_DIMENSION, embed_batch
from app.image_model import ALL_SUPPORTED_LABELS, diagnose

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("bhoomi.ml")

app = FastAPI(
    title="Bhoomi ML Inference Service",
    version="0.1.0",
    description=(
        "Heuristic crop disease/pest diagnosis, text embedding, and speech "
        "endpoints for the Bhoomi backend. See module docstrings for exactly "
        "what is (and isn't) a real trained model here."
    ),
)


@app.get("/health", summary="Liveness check")
async def health() -> dict:
    return {"status": "ok", "supported_labels": len(ALL_SUPPORTED_LABELS)}


class DiagnoseRequest(BaseModel):
    asset_id: str = Field(..., description="Opaque asset id/URL the backend passes for the uploaded crop photo")
    crop_hint: str | None = Field(default=None, description="Farmer-stated crop, if known")
    target_type: str = Field(default="disease", description="'disease' or 'pest'")
    image_base64: str | None = Field(
        default=None,
        description=(
            "Optional raw image bytes, base64-encoded. Not sent by services/api today "
            "(no service-to-service auth is wired for this service to resolve asset_id "
            "into bytes via the main API) — supply this directly to exercise the real "
            "pixel-analysis path instead of the asset-id-hash fallback."
        ),
    )


class DiagnoseResponse(BaseModel):
    label: str
    confidence: float
    meta: dict


@app.post("/diagnose", response_model=DiagnoseResponse, summary="Diagnose a crop image")
async def diagnose_endpoint(request: DiagnoseRequest) -> DiagnoseResponse:
    image_bytes = base64.b64decode(request.image_base64) if request.image_base64 else None
    result = diagnose(
        asset_id=request.asset_id,
        crop_hint=request.crop_hint,
        image_bytes=image_bytes,
        target_type=request.target_type,
    )
    logger.info("diagnose asset_id=%s -> label=%s confidence=%.4f", request.asset_id, result.label, result.confidence)
    return DiagnoseResponse(label=result.label, confidence=result.confidence, meta=result.meta)


class EmbedRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, description="Texts to embed")
    dimension: int = Field(default=DEFAULT_DIMENSION, gt=0, le=4096)


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    dimension: int


@app.post("/embed", response_model=EmbedResponse, summary="Embed a batch of texts")
async def embed_endpoint(request: EmbedRequest) -> EmbedResponse:
    vectors = embed_batch(request.texts, dimension=request.dimension)
    return EmbedResponse(embeddings=vectors, dimension=request.dimension)


class TranscribeRequest(BaseModel):
    audio_asset_url_or_id: str
    language: str = "ta"


class TranscribeResponse(BaseModel):
    transcript: str
    confidence: float


@app.post("/transcribe", response_model=TranscribeResponse, summary="Transcribe audio (not yet called by services/api)")
async def transcribe_endpoint(request: TranscribeRequest) -> TranscribeResponse:
    transcript, confidence = transcribe(request.audio_asset_url_or_id, request.language)
    return TranscribeResponse(transcript=transcript, confidence=confidence)


class SynthesizeRequest(BaseModel):
    text: str
    language: str = "ta"
    gender: str = "female"


class SynthesizeResponse(BaseModel):
    asset_id: str
    audio_url: str


@app.post("/synthesize", response_model=SynthesizeResponse, summary="Synthesize speech (not yet called by services/api)")
async def synthesize_endpoint(request: SynthesizeRequest) -> SynthesizeResponse:
    asset_id, audio_url = synthesize(request.text, request.language, request.gender)
    return SynthesizeResponse(asset_id=asset_id, audio_url=audio_url)
