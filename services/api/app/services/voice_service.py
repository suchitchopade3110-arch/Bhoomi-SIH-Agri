"""Voice interaction service — ASR/TTS orchestration (contract §2.5, PRD §5.1).

Enhanced with intent parsing and read-back confirmation:
  1. ASR transcribes the audio
  2. IntentParser extracts structured fields from the transcript
  3. ConfirmationService decides if read-back is needed
  4. Response includes parsed_intent + needs_confirmation + readback_text
"""

from typing import Annotated, Any

from fastapi import Depends

from app.adapters.dependencies import get_llm_adapter, get_speech_adapter
from app.core.config import get_settings
from app.core.errors import NotFoundError
from app.ports import AsrTtsPort, LLMPort
from app.schemas.voice import (
    ParsedIntent as ParsedIntentSchema,
    VoiceQueryRequest,
    VoiceQueryResponse,
    VoiceSynthesizeRequest,
    VoiceSynthesizeResponse,
    VoiceTranscribeRequest,
    VoiceTranscribeResponse,
)
from app.services.confirmation import ConfirmationService
from app.services.intent_parser import IntentParser
from app.services.storage_service import StorageService, get_storage_service


class VoiceService:
    """Transcribes/synthesizes regional speech via ``AsrTtsPort``.

    Now includes intent parsing and read-back confirmation per PRD §5.1.
    """

    def __init__(self, speech: AsrTtsPort, llm: LLMPort, storage: StorageService) -> None:
        self._speech = speech
        self._llm = llm
        self._storage = storage
        self._intent_parser = IntentParser()
        settings = get_settings()
        self._confirmation = ConfirmationService(
            confidence_floor=getattr(settings, "CONFIRMATION_CONFIDENCE_FLOOR", 0.85),
        )

    async def transcribe(self, request: VoiceTranscribeRequest) -> VoiceTranscribeResponse:
        """Transcribe audio, parse intent, and check if confirmation is needed."""
        # Resolve the real storage-key-based download URL up front — the
        # ASR adapter's own asset_id -> URL guess doesn't match how
        # StorageService actually keys objects (see storage_service fix),
        # so callers must hand it a resolvable URL, not a bare asset id.
        try:
            asset = await self._storage.get_asset(request.audio_asset_id)
            audio_source = asset.download_url
        except NotFoundError:
            # Fall back to the raw id — adapter's own fallback path handles
            # this the same way it always has (network/asset failure ->
            # graceful stub transcript), just surfaced one layer earlier.
            audio_source = request.audio_asset_id

        text, confidence = await self._speech.transcribe_audio(
            audio_source, request.language,
        )

        # Parse intent based on context
        parsed = await self._intent_parser.parse(
            text, request.language, request.context,
        )

        # Check if confirmation is needed
        needs_conf = self._confirmation.needs_confirmation(parsed, confidence)

        # Generate readback text if needed
        readback = None
        parsed_schema = None
        if parsed is not None:
            parsed_schema = ParsedIntentSchema(
                field=parsed.field,
                value=parsed.value,
                raw_text=parsed.raw_text,
            )
            if needs_conf:
                readback = self._confirmation.generate_readback_text(
                    parsed, request.language,
                )

        return VoiceTranscribeResponse(
            transcript=text,
            language=request.language,
            confidence=confidence,
            parsed_intent=parsed_schema,
            needs_confirmation=needs_conf,
            readback_text=readback,
            provider=self._speech.provider_name,
        )

    async def synthesize(self, request: VoiceSynthesizeRequest) -> VoiceSynthesizeResponse:
        asset_id, url = await self._speech.synthesize_speech(request.text, request.language, request.gender)
        return VoiceSynthesizeResponse(audio_asset_id=asset_id, audio_url=url, provider=self._speech.provider_name)

    async def confirm_field(
        self, field: str, value: Any, is_confirmed: bool, correction_text: str | None = None
    ) -> dict[str, Any]:
        """Process farmer confirmation of a read-back value."""
        if is_confirmed:
            return {
                "status": "committed",
                "field": field,
                "final_value": value,
                "message": "மதிப்பு வெற்றிகரமாக சேமிக்கப்பட்டது.",  # "Value successfully saved"
            }
        else:
            return {
                "status": "retry_prompt",
                "field": field,
                "final_value": None,
                "message": "தயவுசெய்து சரியான மதிப்பை மீண்டும் சொல்லவும்.",  # "Please state the correct value again"
            }


def get_voice_service(
    speech: Annotated[AsrTtsPort, Depends(get_speech_adapter)],
    llm: Annotated[LLMPort, Depends(get_llm_adapter)],
    storage: Annotated[StorageService, Depends(get_storage_service)],
) -> VoiceService:
    return VoiceService(speech, llm, storage)
