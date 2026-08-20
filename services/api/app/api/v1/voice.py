"""Voice interaction API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.voice import (
    VoiceQueryRequest,
    VoiceQueryResponse,
    VoiceSynthesizeRequest,
    VoiceSynthesizeResponse,
    VoiceTranscribeRequest,
    VoiceTranscribeResponse,
)

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post(
    "/transcribe",
    response_model=VoiceTranscribeResponse,
    summary="Transcribe regional spoken audio to text",
)
async def transcribe(request: VoiceTranscribeRequest) -> VoiceTranscribeResponse:
    raise NotImplementedAPIError("Endpoint POST /voice/transcribe will be implemented in subsequent phases.")


@router.post(
    "/synthesize",
    response_model=VoiceSynthesizeResponse,
    summary="Synthesize regional language text to speech audio",
)
async def synthesize(request: VoiceSynthesizeRequest) -> VoiceSynthesizeResponse:
    raise NotImplementedAPIError("Endpoint POST /voice/synthesize will be implemented in subsequent phases.")


@router.post(
    "/query",
    response_model=VoiceQueryResponse,
    summary="End-to-end voice query processing",
)
async def voice_query(request: VoiceQueryRequest) -> VoiceQueryResponse:
    raise NotImplementedAPIError("Endpoint POST /voice/query will be implemented in subsequent phases.")
