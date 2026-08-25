"""Speech transcription/synthesis endpoint logic.

Not currently called by services/api: ``adapters/dependencies.py`` only
ever wires ``AsrTtsPort`` to the stub or to a named third-party provider
(Bhashini/Sarvam/Whisper/gTTS) selected by ``ASR_PROVIDER``/``TTS_PROVIDER``
— there is no ``real`` option that points at ``ML_SERVICE_URL`` the way
``DIAGNOSIS_MODEL=real`` does for image diagnosis. This module exists so
the endpoint is available (mirroring the same context-hint heuristic as
``StubAsrTtsAdapter`` in services/api, for demo consistency) if/when a
future ``ASR_PROVIDER=ml_service`` option is wired up; it is not a real
speech model.
"""

from __future__ import annotations

import uuid

_CONTEXT_RESPONSES: dict[str, tuple[str, float]] = {
    "onboarding": ("என் நிலம் இரண்டு ஏக்கர் சம்பா நெல்", 0.91),
    "diagnosis": ("இலை நுனி மஞ்சள் நிறமாக உள்ளது", 0.88),
    "followup": ("மோசமாகிவிட்டது", 0.93),
    "followup_improved": ("சரியாகிவிட்டது", 0.92),
    "followup_nochange": ("மாற்றமில்லை", 0.90),
    "low_confidence": ("என் நிலம் இரண்டு ஏக்கர்", 0.60),
}
_DEFAULT_RESPONSE = ("வணக்கம், என் தக்காளி செடியில் இலைகளில் கரும்புள்ளிகள் காணப்படுகின்றன.", 0.94)


def transcribe(audio_asset_url_or_id: str, language: str = "ta") -> tuple[str, float]:
    asset_lower = audio_asset_url_or_id.lower()
    for key, response in _CONTEXT_RESPONSES.items():
        if key in asset_lower:
            return response
    return _DEFAULT_RESPONSE


def synthesize(text: str, language: str = "ta", gender: str = "female") -> tuple[str, str]:
    asset_id = str(uuid.uuid4())
    return asset_id, f"http://localhost:9000/bhoomi-assets/{asset_id}.mp3"
