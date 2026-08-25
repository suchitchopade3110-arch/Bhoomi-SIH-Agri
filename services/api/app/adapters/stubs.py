"""Stub implementations for all ports returning deterministic / settable values."""

from datetime import date, datetime
import hashlib
import logging
import re
from typing import Any
import uuid

from app.domain.kvk_directory import KVK_CENTERS


class StubWeatherAdapter:
    """Stub weather adapter returning fixed meteorological and ET₀ data."""

    def __init__(self, fixed_et0: float = 4.8, fixed_temp: float = 30.0, fixed_humidity: float = 75.0) -> None:
        self.fixed_et0 = fixed_et0
        self.fixed_temp = fixed_temp
        self.fixed_humidity = fixed_humidity

    async def get_current_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "temperature_c": self.fixed_temp,
            "relative_humidity_pct": self.fixed_humidity,
            "wind_speed_kmh": 12.4,
            "precipitation_mm": 0.0,
            "condition_description": "Partly Cloudy",
            "observed_at": datetime.utcnow().isoformat(),
        }

    async def get_daily_et0(self, latitude: float, longitude: float, target_date: date) -> float:
        return self.fixed_et0

    async def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> list[dict[str, Any]]:
        return [
            {
                "forecast_date": date.today().isoformat(),
                "temp_max_c": 34.0,
                "temp_min_c": 24.5,
                "precipitation_sum_mm": 1.2,
                "et0_fao_evapotranspiration_mm": self.fixed_et0,
                "precipitation_probability_pct": 20,
            }
            for _ in range(days)
        ]


class StubLLMAdapter:
    """Stub LLM adapter honoring the grounding contract (PRD §5.7, §5.8):
    it answers ONLY by constructing its response from the retrieved chunks
    it was actually given — it never invents content — and signals
    ``insufficient_context`` rather than guessing when no chunks are passed.

    Deterministic given deterministic chunks: same query + chunks in, same
    5-point output out. Real: Claude/GPT with the same grounding prompt
    (``domain.rag.prompt.build_grounding_prompt``) sent as the instruction.
    """

    async def generate_grounded_advisory(
        self,
        query: str,
        context_chunks: list[dict[str, Any]],
        farm_context: dict[str, Any],
    ) -> dict[str, Any]:
        if not context_chunks:
            return {
                "insufficient_context": True,
                "reason": "no retrieved chunks were provided to ground an answer",
            }

        top = context_chunks[0]
        excerpt = top["chunk_text"].strip().splitlines()[0][:240]

        return {
            "possible_issue": f"Based on \"{top['title']}\", this likely matches: {excerpt}",
            "what_to_check": f"Compare the symptoms described in your query against the guidance in \"{top['title']}\".",
            "what_to_do_next": "Follow the control steps described in the cited source(s) below.",
            "what_to_avoid": "Do not apply treatments that aren't covered by the cited guidance.",
            "expert_triggers": "If symptoms spread or persist after following the cited guidance, escalate to an agronomist.",
            "citations": [
                {"doc_id": c["doc_id"], "title": c["title"], "reviewed_on": str(c["reviewed_on"])}
                for c in context_chunks
            ],
        }

    async def synthesize_case_summary(
        self,
        farm_data: dict[str, Any],
        events: list[dict[str, Any]],
        health_history: list[dict[str, Any]],
    ) -> str:
        return (
            f"Farm in {farm_data.get('village', 'Unknown')} cultivating {farm_data.get('primary_crop', 'Crop')} "
            f"shows declining health score due to persistent fungal infection symptoms and water deficit."
        )


class StubEmbeddingAdapter:
    """Stub embedding adapter: deterministic token-level feature hashing
    (the "hashing trick" — each token hashes to a dimension it increments),
    not a whole-string hash.

    This matters for RAG: a whole-string hash gives two different texts
    essentially uncorrelated (near-orthogonal) vectors regardless of shared
    vocabulary, which would make relevance scoring meaningless for tests and
    for the demo. Token-level hashing means texts sharing vocabulary (e.g. a
    query and a corpus chunk both mentioning "bacterial leaf blight") get
    genuine cosine overlap, while unrelated text doesn't — deterministic and
    dependency-free, without downloading real embedding weights.
    """

    # Common function words filtered out before hashing: every document and
    # every query shares most of these, so leaving them in dilutes cosine
    # similarity with noise unrelated to actual topical overlap.
    _STOPWORDS = frozenset(
        {
            "a", "an", "and", "are", "as", "at", "be", "been", "by", "can", "do", "does",
            "for", "from", "has", "have", "how", "if", "in", "into", "is", "it", "its",
            "of", "on", "or", "should", "that", "the", "their", "then", "there", "this",
            "to", "was", "were", "what", "when", "where", "which", "who", "will", "with",
            "your", "you", "my", "i", "not", "than", "also",
        }
    )
    _MIN_TOKEN_LENGTH = 3

    def __init__(self, dimension: int = 1024) -> None:
        self.dimension = dimension

    def _tokenize(self, text: str) -> list[str]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        return [t for t in tokens if len(t) >= self._MIN_TOKEN_LENGTH and t not in self._STOPWORDS]

    def _hash_to_vector(self, text: str) -> list[float]:
        vec = [0.0] * self.dimension
        for token in self._tokenize(text):
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            index = int(digest[:8], 16) % self.dimension
            sign = 1.0 if int(digest[8], 16) % 2 == 0 else -1.0
            vec[index] += sign

        norm = sum(x * x for x in vec) ** 0.5
        if norm == 0.0:
            return vec
        return [round(x / norm, 6) for x in vec]

    async def embed_text(self, text: str) -> list[float]:
        return self._hash_to_vector(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._hash_to_vector(t) for t in texts]


class StubImageDiagnosisAdapter:
    """Stub image disease model adapter with settable confidence score.

    Default label is one of ``gate_service.SUPPORTED_DIAGNOSIS_LABELS`` (the
    bounded crop/disease set, PRD §5.6) so a default call is in-scope; tests
    exercising the out-of-scope branch call ``set_label`` with anything
    outside that set.
    """

    def __init__(self, label: str = "bacterial_leaf_blight", confidence: float = 0.85) -> None:
        self.label = label
        self.confidence = confidence

    def set_confidence(self, confidence: float) -> None:
        """Allow test suites to simulate below-gate and above-gate scenarios."""
        self.confidence = confidence

    def set_label(self, label: str) -> None:
        self.label = label

    async def diagnose_crop_image(
        self,
        image_asset_url_or_id: str,
        crop_hint: str | None = None,
    ) -> tuple[str, float, dict[str, Any]]:
        return (
            self.label,
            self.confidence,
            {
                "model_version": "stub-vit-v1",
                "inference_time_ms": 12.4,
                "crop_detected": crop_hint or "Tomato",
            },
        )


class StubAsrTtsAdapter:
    """Stub speech adapter returning context-specific transcription and mock audio URL.

    The transcript returned depends on a hint embedded in the ``audio_asset_url_or_id``:
    - contains "onboarding" → Tamil farm onboarding text (crop + area)
    - contains "diagnosis"  → Tamil leaf symptoms
    - contains "followup"   → Tamil "got worse" response
    - default               → generic Tamil greeting with tomato symptoms
    """

    provider_name = "stub"

    # Context-specific response tuples: (transcript, confidence)
    _CONTEXT_RESPONSES: dict[str, tuple[str, float]] = {
        "onboarding": ("என் நிலம் இரண்டு ஏக்கர் சம்பா நெல்", 0.91),
        "diagnosis": ("இலை நுனி மஞ்சள் நிறமாக உள்ளது", 0.88),
        "followup": ("மோசமாகிவிட்டது", 0.93),
        "followup_improved": ("சரியாகிவிட்டது", 0.92),
        "followup_nochange": ("மாற்றமில்லை", 0.90),
        "low_confidence": ("என் நிலம் இரண்டு ஏக்கர்", 0.60),
    }

    async def transcribe_audio(self, audio_asset_url_or_id: str, language: str = "ta") -> tuple[str, float]:
        asset_lower = audio_asset_url_or_id.lower()
        for key, response in self._CONTEXT_RESPONSES.items():
            if key in asset_lower:
                return response
        # Default response
        return ("வணக்கம், என் தக்காளி செடியில் இலைகளில் கரும்புள்ளிகள் காணப்படுகின்றன.", 0.94)

    async def synthesize_speech(self, text: str, language: str = "ta", gender: str = "female") -> tuple[str, str]:
        mock_asset_id = str(uuid.uuid4())
        return (mock_asset_id, f"http://localhost:9000/bhoomi-assets/{mock_asset_id}.mp3")


class StubStorageAdapter:
    """Stub storage adapter returning mock presigned URLs."""

    async def generate_presigned_upload_url(
        self,
        asset_id: str,
        file_name: str,
        content_type: str,
        asset_kind: str,
        expires_in: int = 3600,
    ) -> dict[str, Any]:
        return {
            "asset_id": asset_id,
            "upload_url": f"http://localhost:9000/bhoomi-assets/{asset_id}?upload=true",
            "expires_in": expires_in,
            "fields": {"key": f"{asset_kind}/{asset_id}/{file_name}"},
        }

    async def generate_presigned_download_url(
        self,
        asset_id: str,
        expires_in: int = 3600,
    ) -> str:
        return f"http://localhost:9000/bhoomi-assets/{asset_id}"


class StubRosterAdapter:
    """Stub ``AgronomistRosterPort`` — a static agronomist roster (PRD §5.11,
    Phase 2), until a real officer/agronomist-capacity model exists in the
    schema (PRD §10 risk #10). Reuses the KVK center directory's ids
    (``app/domain/kvk_directory.py``) so the roster and the known KVK
    centers don't drift into two separate lists of the same thing."""

    async def list_agronomist_ids(self) -> list[str]:
        return [center.center_id for center in KVK_CENTERS]


class StubOtpDeliveryAdapter:
    """Stub ``OtpDeliveryPort`` — logs the OTP instead of sending a real SMS.

    No SMS gateway (Twilio/MSG91/etc.) is configured anywhere in this
    project, so there is no "real" adapter to select here the way
    ``DIAGNOSIS_MODEL=real`` selects a real image-diagnosis backend — that
    integration doesn't exist yet. ``otp_service.py`` also returns the code
    directly in the API response outside ``APP_ENV=production``, which is
    what actually makes the OTP flow usable/testable without a real SMS
    provider; this adapter's logging is a secondary, ops-facing trace.
    """

    def __init__(self) -> None:
        self.last_sent: tuple[str, str] | None = None  # (phone_number, otp), settable for tests

    async def send_otp(self, phone_number: str, otp: str) -> None:
        self.last_sent = (phone_number, otp)
        logging.getLogger("bhoomi.otp").info("OTP for %s: %s (stub delivery, no real SMS sent)", phone_number, otp)
