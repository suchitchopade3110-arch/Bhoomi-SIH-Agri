"""Google Text-to-Speech (gTTS) Adapter.

Implements the TTS half of ``AsrTtsPort`` using ``gTTS`` for regional synthesis (Tamil/Hindi).
"""

from __future__ import annotations

import io
import logging
import uuid

import httpx

from app.adapters.asset_url import fallback_asset_url
from app.ports.asr_tts import AsrTtsPort

logger = logging.getLogger(__name__)


class GttsAdapter:
    """TTS adapter utilizing Google Translate's gTTS library.

    ``transcribe_audio`` is not implemented by gTTS (it is TTS-only); this
    adapter is only ever selected via ``TTS_PROVIDER=gtts`` while
    ``ASR_PROVIDER`` stays on ``stub``, so a call here returns the same
    canned stub transcript rather than claiming a real ASR result.
    """

    provider_name = "gtts"

    async def transcribe_audio(
        self, audio_asset_url_or_id: str, language: str = "ta"
    ) -> tuple[str, float]:
        """Transcribe fallback (gTTS only handles TTS)."""
        return ("வணக்கம், பயிர் நிலைமை பற்றிய தகவல்.", 0.90)

    async def synthesize_speech(
        self, text: str, language: str = "ta", gender: str = "female"
    ) -> tuple[str, str]:
        """Synthesize regional text to mp3 using gTTS and upload it via the storage port.

        Generates real audio, then pushes it through ``StoragePort`` instead of
        discarding it and returning a URL nothing was ever written to. Falls back
        to a placeholder URL only if generation or upload actually fails.
        """
        mock_asset_id = str(uuid.uuid4())
        fallback = (mock_asset_id, fallback_asset_url(mock_asset_id, "mp3"))

        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang=language, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            audio_bytes = fp.getvalue()

            # Imported lazily to avoid a module-level import cycle with
            # ``app.adapters.dependencies`` (which imports this adapter lazily too).
            from app.adapters.dependencies import get_storage_adapter

            storage = get_storage_adapter()
            asset_file_name = f"{mock_asset_id}.mp3"
            presigned = await storage.generate_presigned_upload_url(
                asset_id=mock_asset_id,
                file_name=asset_file_name,
                content_type="audio/mpeg",
                asset_kind="voice_synthesis",
            )

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(
                    presigned["upload_url"],
                    content=audio_bytes,
                    headers={"Content-Type": "audio/mpeg"},
                )
                response.raise_for_status()

            download_url = await storage.generate_presigned_download_url(asset_file_name)
            return (mock_asset_id, download_url)
        except Exception:
            logger.warning("gTTS synthesis or upload failed; returning placeholder URL", exc_info=True)
            return fallback
