"""Stub implementations for all ports returning deterministic / settable values."""

from datetime import date, datetime
import hashlib
from typing import Any
import uuid


class StubWeatherAdapter:
    """Stub weather adapter returning fixed meteorological and ET₀ data."""

    def __init__(self, fixed_et0: float = 4.8, fixed_temp: float = 31.5) -> None:
        self.fixed_et0 = fixed_et0
        self.fixed_temp = fixed_temp

    async def get_current_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "temperature_c": self.fixed_temp,
            "relative_humidity_pct": 68.0,
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
    """Stub LLM adapter returning canned grounded 5-point advisory."""

    async def generate_grounded_advisory(
        self,
        query: str,
        context_chunks: list[dict[str, Any]],
        farm_context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "diagnosis": "Early Blight (Alternaria solani)",
            "cause": "Fungal pathogen favored by warm temperatures (24-29°C) and alternating wet/dry cycles.",
            "immediate_action": "Prune infected lower leaves and burn or bury away from field. Ensure drip lines do not splash soil.",
            "preventative_action": "Apply copper oxychloride (2.5 g/L) or Mancozeb (2 g/L) as a prophylactic spray; implement crop rotation with non-solanaceous crops.",
            "recommended_inputs": [
                "Copper Oxychloride 50% WP @ 2.5g/liter",
                "Neem Oil 10,000 ppm @ 3ml/liter for preventive cover",
            ],
            "confidence_score": 0.88,
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
    """Stub embedding adapter returning deterministic 1024-dimensional hashed vectors."""

    def __init__(self, dimension: int = 1024) -> None:
        self.dimension = dimension

    def _hash_to_vector(self, text: str) -> list[float]:
        # Generate deterministic float vector from md5 hash
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        seed = int(h[:8], 16)
        vec = [((seed * (i + 1)) % 1000) / 1000.0 for i in range(self.dimension)]
        # Normalize
        norm = sum(x * x for x in vec) ** 0.5 or 1.0
        return [round(x / norm, 6) for x in vec]

    async def embed_text(self, text: str) -> list[float]:
        return self._hash_to_vector(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._hash_to_vector(t) for t in texts]


class StubImageDiagnosisAdapter:
    """Stub image disease model adapter with settable confidence score."""

    def __init__(self, label: str = "Tomato Early Blight", confidence: float = 0.85) -> None:
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
    """Stub speech adapter returning echo transcription and mock audio URL."""

    async def transcribe_audio(self, audio_asset_url_or_id: str, language: str = "ta") -> tuple[str, float]:
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
