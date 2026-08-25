"""External adapter ports and implementations."""

from app.adapters.image_diagnosis_real import RealImageDiagnosisAdapter
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
from app.adapters.dependencies import (
    get_embedding_adapter,
    get_image_diagnosis_adapter,
    get_llm_adapter,
    get_speech_adapter,
    get_storage_adapter,
    get_weather_adapter,
)

__all__ = [
    "WeatherPort",
    "LLMPort",
    "EmbeddingPort",
    "ImageDiagnosisPort",
    "AsrTtsPort",
    "StoragePort",
    "StubWeatherAdapter",
    "StubLLMAdapter",
    "StubEmbeddingAdapter",
    "StubImageDiagnosisAdapter",
    "StubAsrTtsAdapter",
    "StubStorageAdapter",
    "RealImageDiagnosisAdapter",
    "get_weather_adapter",
    "get_llm_adapter",
    "get_embedding_adapter",
    "get_image_diagnosis_adapter",
    "get_speech_adapter",
    "get_storage_adapter",
]
