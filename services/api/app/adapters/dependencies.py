"""FastAPI dependency providers for external adapter ports."""

from functools import lru_cache
from app.adapters.ports import (
    AsrTtsPort,
    EmbeddingPort,
    ImageDiagnosisPort,
    LLMPort,
    StoragePort,
    WeatherPort,
)
from app.adapters.stubs import (
    StubAsrTtsAdapter,
    StubEmbeddingAdapter,
    StubImageDiagnosisAdapter,
    StubLLMAdapter,
    StubStorageAdapter,
    StubWeatherAdapter,
)
from app.core.config import get_settings


@lru_cache
def get_weather_adapter() -> WeatherPort:
    """Return WeatherPort adapter based on settings."""
    return StubWeatherAdapter()


@lru_cache
def get_llm_adapter() -> LLMPort:
    """Return LLMPort adapter based on settings."""
    return StubLLMAdapter()


@lru_cache
def get_embedding_adapter() -> EmbeddingPort:
    """Return EmbeddingPort adapter based on settings."""
    return StubEmbeddingAdapter()


@lru_cache
def get_image_diagnosis_adapter() -> ImageDiagnosisPort:
    """Return ImageDiagnosisPort adapter based on settings."""
    settings = get_settings()
    # In Phase 0, both stub and real flag use the stub
    return StubImageDiagnosisAdapter(confidence=0.85)


@lru_cache
def get_speech_adapter() -> AsrTtsPort:
    """Return AsrTtsPort adapter based on settings."""
    return StubAsrTtsAdapter()


@lru_cache
def get_storage_adapter() -> StoragePort:
    """Return StoragePort adapter based on settings."""
    return StubStorageAdapter()
