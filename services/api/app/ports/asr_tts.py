"""ASR/TTS port — typed Protocol for regional speech recognition and synthesis."""

from typing import Protocol


class AsrTtsPort(Protocol):
    """Port for regional automatic speech recognition and text-to-speech synthesis."""

    provider_name: str
    """Identifies which implementation actually ran (e.g. 'stub', 'sarvam', 'bhashini'),
    so callers can tell a stub response from a real one instead of inferring it from
    confidence values that happen to overlap."""

    async def transcribe_audio(self, audio_asset_url_or_id: str, language: str = "ta") -> tuple[str, float]:
        """Transcribe regional audio into text, returning (transcript_text, confidence)."""
        ...

    async def synthesize_speech(self, text: str, language: str = "ta", gender: str = "female") -> tuple[str, str]:
        """Synthesize text into speech audio, returning (generated_asset_id, audio_url)."""
        ...


__all__ = ["AsrTtsPort"]
