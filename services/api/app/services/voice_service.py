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
from app.services.rag.advisory_service import AdvisoryService, get_advisory_service
from app.services.storage_service import StorageService, get_storage_service


class VoiceService:
    """Transcribes/synthesizes regional speech via ``AsrTtsPort``.

    Now includes intent parsing and read-back confirmation per PRD §5.1.
    """

    def __init__(
        self,
        speech: AsrTtsPort,
        llm: LLMPort,
        storage: StorageService,
        advisory: AdvisoryService,
    ) -> None:
        self._speech = speech
        self._llm = llm
        self._storage = storage
        self._advisory = advisory
        self._intent_parser = IntentParser()
        settings = get_settings()
        self._confirmation = ConfirmationService(
            confidence_floor=getattr(settings, "CONFIRMATION_CONFIDENCE_FLOOR", 0.85),
        )

    async def _resolve_audio_source(self, audio_asset_id: str) -> str:
        """Same asset-id -> download-URL resolution used by ``transcribe`` —
        factored out so ``process_voice_query`` doesn't fabricate its own
        (previously nonexistent) copy."""
        try:
            asset = await self._storage.get_asset(audio_asset_id)
            return asset.download_url
        except NotFoundError:
            return audio_asset_id

    async def transcribe(self, request: VoiceTranscribeRequest) -> VoiceTranscribeResponse:
        """Transcribe audio, parse intent, and check if confirmation is needed."""
        # Resolve the real storage-key-based download URL up front — the
        # ASR adapter's own asset_id -> URL guess doesn't match how
        # StorageService actually keys objects (see storage_service fix),
        # so callers must hand it a resolvable URL, not a bare asset id.
        audio_source = await self._resolve_audio_source(request.audio_asset_id)

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

        provider_name = getattr(self._speech, "provider_name", "stub")
        if not isinstance(provider_name, str):
            provider_name = "stub"

        return VoiceTranscribeResponse(
            transcript=text,
            language=request.language,
            confidence=confidence,
            parsed_intent=parsed_schema,
            needs_confirmation=needs_conf,
            readback_text=readback,
            provider=provider_name,
        )

    async def synthesize(self, request: VoiceSynthesizeRequest) -> VoiceSynthesizeResponse:
        asset_id, url = await self._speech.synthesize_speech(request.text, request.language, request.gender)
        provider_name = getattr(self._speech, "provider_name", "stub")
        if not isinstance(provider_name, str):
            provider_name = "stub"
        return VoiceSynthesizeResponse(audio_asset_id=asset_id, audio_url=url, provider=provider_name)

    async def process_voice_query(self, request: VoiceQueryRequest) -> VoiceQueryResponse:
        """End-to-end speech-to-speech: transcribe the farmer's spoken query,
        answer it via the grounded RAG advisory pipeline, and synthesize the
        answer back into speech (contract §2.5, PRD §5.1)."""
        audio_source = await self._resolve_audio_source(request.audio_asset_id)
        transcript, _confidence = await self._speech.transcribe_audio(
            audio_source, request.language,
        )

        outcome = await self._advisory.answer_query(request.farm_id, transcript)

        if outcome.retrieved and outcome.advisory is not None:
            advisory = outcome.advisory
            answer_text = " ".join(
                part
                for part in (
                    advisory.possible_issue,
                    advisory.what_to_avoid,
                    advisory.what_to_check,
                    advisory.what_to_do_next,
                )
                if part
            )
        else:
            answer_text = outcome.spoken_summary

        audio_asset_id, audio_url = await self._speech.synthesize_speech(
            answer_text, request.language,
        )

        return VoiceQueryResponse(
            transcript=transcript,
            answer_text=answer_text,
            audio_response_url=audio_url,
            spoken_summary=outcome.spoken_summary,
        )

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

        # If correction_text is provided, attempt to extract the corrected value
        if correction_text:
            corrected_value = self._intent_parser.parse_field(correction_text, field)
            if corrected_value is not None:
                return {
                    "status": "committed",
                    "field": field,
                    "final_value": corrected_value,
                    "message": "மதிப்பு வெற்றிகரமாக திருத்தப்பட்டு சேமிக்கப்பட்டது.",  # "Value successfully corrected and saved"
                }

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
    advisory: Annotated[AdvisoryService, Depends(get_advisory_service)],
) -> VoiceService:
    return VoiceService(speech, llm, storage, advisory)
