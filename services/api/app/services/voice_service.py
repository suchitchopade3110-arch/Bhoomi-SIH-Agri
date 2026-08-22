"""Voice interaction service — ASR/TTS orchestration (contract §2.5, PRD §5.1)."""

from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_llm_adapter, get_speech_adapter
from app.adapters.ports import AsrTtsPort, LLMPort
from app.schemas.voice import (
    VoiceQueryRequest,
    VoiceQueryResponse,
    VoiceSynthesizeRequest,
    VoiceSynthesizeResponse,
    VoiceTranscribeRequest,
    VoiceTranscribeResponse,
)


class VoiceService:
    """Transcribes/synthesizes regional speech via ``AsrTtsPort``."""

    def __init__(self, speech: AsrTtsPort, llm: LLMPort) -> None:
        self._speech = speech
        self._llm = llm

    async def transcribe(self, request: VoiceTranscribeRequest) -> VoiceTranscribeResponse:
        text, confidence = await self._speech.transcribe_audio(request.audio_asset_id, request.language)
        return VoiceTranscribeResponse(transcript=text, language=request.language, confidence=confidence)

    async def synthesize(self, request: VoiceSynthesizeRequest) -> VoiceSynthesizeResponse:
        asset_id, url = await self._speech.synthesize_speech(request.text, request.language, request.gender)
        return VoiceSynthesizeResponse(audio_asset_id=asset_id, audio_url=url)

    async def process_voice_query(self, request: VoiceQueryRequest) -> VoiceQueryResponse:
        transcript, _confidence = await self._speech.transcribe_audio(request.audio_asset_id, request.language)
        answer = f"Received: {transcript}"
        _asset_id, audio_url = await self._speech.synthesize_speech(answer, request.language)
        return VoiceQueryResponse(
            transcript=transcript,
            answer_text=answer,
            audio_response_url=audio_url,
            spoken_summary=answer,
        )


def get_voice_service(
    speech: Annotated[AsrTtsPort, Depends(get_speech_adapter)],
    llm: Annotated[LLMPort, Depends(get_llm_adapter)],
) -> VoiceService:
    return VoiceService(speech, llm)
