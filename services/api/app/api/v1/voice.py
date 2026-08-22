"""Voice interaction API router (contract §2.5)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.voice import (
    VoiceQueryRequest,
    VoiceQueryResponse,
    VoiceSynthesizeRequest,
    VoiceSynthesizeResponse,
    VoiceTranscribeRequest,
    VoiceTranscribeResponse,
)
from app.services.voice_service import VoiceService, get_voice_service

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post(
    "/transcribe",
    response_model=VoiceTranscribeResponse,
    summary="Transcribe regional spoken audio to text",
)
async def transcribe(
    request: VoiceTranscribeRequest,
    service: Annotated[VoiceService, Depends(get_voice_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> VoiceTranscribeResponse:
    return await service.transcribe(request)


@router.post(
    "/synthesize",
    response_model=VoiceSynthesizeResponse,
    summary="Synthesize regional language text to speech audio",
)
async def synthesize(
    request: VoiceSynthesizeRequest,
    service: Annotated[VoiceService, Depends(get_voice_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> VoiceSynthesizeResponse:
    return await service.synthesize(request)


@router.post(
    "/query",
    response_model=VoiceQueryResponse,
    summary="End-to-end voice query processing",
)
async def voice_query(
    request: VoiceQueryRequest,
    service: Annotated[VoiceService, Depends(get_voice_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> VoiceQueryResponse:
    return await service.process_voice_query(request)
