"""app/deps.py — spec-mandated shim to app.adapters.dependencies.

DI wiring: selects real vs stub adapters based on config flags
(``LAND_API_MODE``, ``DIAGNOSIS_MODEL``). The implementation lives in
``app.adapters.dependencies``; this shim satisfies the spec-mandated
``from app.deps import ...`` import path.
"""

from app.adapters.dependencies import (  # noqa: F401
    get_embedding_adapter,
    get_image_diagnosis_adapter,
    get_llm_adapter,
    get_speech_adapter,
    get_storage_adapter,
    get_weather_adapter,
)

__all__ = [
    "get_weather_adapter",
    "get_llm_adapter",
    "get_embedding_adapter",
    "get_image_diagnosis_adapter",
    "get_speech_adapter",
    "get_storage_adapter",
]
