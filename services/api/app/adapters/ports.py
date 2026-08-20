"""Protocols (Ports) for all external dependencies in Bhoomi."""

from datetime import date
from typing import Any, Protocol


class WeatherPort(Protocol):
    """Port for retrieving meteorological data, ET₀, and rainfall forecasts."""

    async def get_current_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        """Fetch current weather metrics (temperature, humidity, precipitation)."""
        ...

    async def get_daily_et0(self, latitude: float, longitude: float, target_date: date) -> float:
        """Fetch FAO-56 reference evapotranspiration (ET₀) in mm/day."""
        ...

    async def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> list[dict[str, Any]]:
        """Fetch daily weather and precipitation forecast for specified days."""
        ...


class LLMPort(Protocol):
    """Port for grounded LLM generation and case file synthesis."""

    async def generate_grounded_advisory(
        self,
        query: str,
        context_chunks: list[dict[str, Any]],
        farm_context: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate structured 5-point advisory grounded strictly in provided context chunks."""
        ...

    async def synthesize_case_summary(
        self,
        farm_data: dict[str, Any],
        events: list[dict[str, Any]],
        health_history: list[dict[str, Any]],
    ) -> str:
        """Synthesize a concise, multi-factor problem summary for expert escalation."""
        ...


class EmbeddingPort(Protocol):
    """Port for generating dense vector embeddings for RAG retrieval."""

    async def embed_text(self, text: str) -> list[float]:
        """Generate vector embedding for a single text string."""
        ...

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate vector embeddings for a batch of text strings."""
        ...


class ImageDiagnosisPort(Protocol):
    """Port for crop disease computer vision model inference."""

    async def diagnose_crop_image(
        self,
        image_asset_url_or_id: str,
        crop_hint: str | None = None,
    ) -> tuple[str, float, dict[str, Any]]:
        """Run vision model to predict disease label and native model confidence score (0.0 - 1.0)."""
        ...


class AsrTtsPort(Protocol):
    """Port for regional automatic speech recognition and text-to-speech synthesis."""

    async def transcribe_audio(self, audio_asset_url_or_id: str, language: str = "ta") -> tuple[str, float]:
        """Transcribe regional audio into text, returning (transcript_text, confidence)."""
        ...

    async def synthesize_speech(self, text: str, language: str = "ta", gender: str = "female") -> tuple[str, str]:
        """Synthesize text into speech audio, returning (generated_asset_id, audio_url)."""
        ...


class StoragePort(Protocol):
    """Port for S3/MinIO presigned object storage operations."""

    async def generate_presigned_upload_url(
        self,
        asset_id: str,
        file_name: str,
        content_type: str,
        asset_kind: str,
        expires_in: int = 3600,
    ) -> dict[str, Any]:
        """Generate presigned PUT/POST URL for direct client upload."""
        ...

    async def generate_presigned_download_url(
        self,
        asset_id: str,
        expires_in: int = 3600,
    ) -> str:
        """Generate presigned GET URL for retrieving private assets."""
        ...
