"""FastAPI dependency providers for external adapter ports.

Selection is by config only (PRD §1.5) — no call site outside this module
ever imports a concrete adapter class, so flipping ``LAND_API_MODE`` or
``DIAGNOSIS_MODEL`` in ``.env`` changes behavior everywhere for free.
"""

from functools import lru_cache

from app.adapters.embeddings_real import RealEmbeddingAdapter
from app.adapters.image_diagnosis_real import RealImageDiagnosisAdapter
from app.adapters.land_registry import LandRegistryPort, LiveLandRegistryAdapter, MockLandRegistryAdapter
from app.ports import (
    AgronomistRosterPort,
    AsrTtsPort,
    EmbeddingPort,
    ImageDiagnosisPort,
    LLMPort,
    OtpDeliveryPort,
    StoragePort,
    WeatherPort,
)
from app.adapters.stubs import (
    StubAsrTtsAdapter,
    StubEmbeddingAdapter,
    StubImageDiagnosisAdapter,
    StubLLMAdapter,
    StubOtpDeliveryAdapter,
    StubRosterAdapter,
    StubStorageAdapter,
    StubWeatherAdapter,
)
from app.core.config import get_settings


@lru_cache
def get_weather_adapter() -> WeatherPort:
    """Return WeatherPort adapter based on settings.

    A real Open-Meteo adapter is a documented follow-up (see final report) —
    left on the stub for this phase so health/resource-plan scoring stays
    deterministic offline, matching the runbook's fixed expected numbers.
    """
    return StubWeatherAdapter()


@lru_cache
def get_roster_adapter() -> AgronomistRosterPort:
    """Return AgronomistRosterPort adapter.

    No officer/agronomist-capacity model exists in the schema yet (PRD §10
    risk #10) — real capacity comes from ``CaseRepository`` regardless, this
    only supplies the routable id list. Stub for this phase; swap for a real
    roster-service adapter once one exists, with no call-site changes.
    """
    return StubRosterAdapter()


@lru_cache
def get_llm_adapter() -> LLMPort:
    """Return LLMPort adapter based on settings."""
    return StubLLMAdapter()


@lru_cache
def get_embedding_adapter() -> EmbeddingPort:
    """Return EmbeddingPort adapter based on ``EMBEDDING_PROVIDER``.

    ``bge_m3`` calls out to services/ml over HTTP — see
    ``adapters/embeddings_real.py`` for why that's the honest integration
    point (real weights there if the optional dependency is installed and
    reachable, a hash fallback otherwise) rather than a fake "real" adapter
    that's secretly still the hash technique.
    """
    settings = get_settings()
    if settings.EMBEDDING_PROVIDER == "bge_m3":
        return RealEmbeddingAdapter(settings.ML_SERVICE_URL)
    return StubEmbeddingAdapter()


@lru_cache
def get_image_diagnosis_adapter() -> ImageDiagnosisPort:
    """Return ImageDiagnosisPort adapter based on ``DIAGNOSIS_MODEL``.

    ``real`` calls out to the (separately-phased) ML inference service —
    see ``adapters/image_diagnosis_real.py`` for why that's an honest
    integration point rather than a fake model.
    """
    settings = get_settings()
    if settings.DIAGNOSIS_MODEL == "real":
        return RealImageDiagnosisAdapter(settings.ML_SERVICE_URL)
    return StubImageDiagnosisAdapter(confidence=0.85)


@lru_cache
def get_speech_adapter() -> AsrTtsPort:
    """Return AsrTtsPort adapter based on ``ASR_PROVIDER`` / ``TTS_PROVIDER`` settings.

    An explicit real-provider selection fails loudly here if its required
    credentials are absent, rather than silently constructing an adapter
    that would return canned fallback text on every call while still
    claiming to be the real provider (see ``docs/`` voice provider audit).
    """
    settings = get_settings()
    provider = getattr(settings, "ASR_PROVIDER", "stub").lower()

    if provider == "bhashini":
        if not settings.BHASHINI_API_KEY or not settings.BHASHINI_USER_ID:
            raise RuntimeError(
                "ASR_PROVIDER=bhashini but BHASHINI_API_KEY/BHASHINI_USER_ID are not set. "
                "Set both credentials or set ASR_PROVIDER=stub."
            )
        from app.adapters.bhashini_asr import BhashiniAsrTtsAdapter
        return BhashiniAsrTtsAdapter()
    elif provider == "sarvam":
        if not settings.SARVAM_API_KEY:
            raise RuntimeError(
                "ASR_PROVIDER=sarvam but SARVAM_API_KEY is not set. "
                "Set the credential or set ASR_PROVIDER=stub."
            )
        from app.adapters.sarvam_asr import SarvamAsrTtsAdapter
        return SarvamAsrTtsAdapter()
    elif getattr(settings, "TTS_PROVIDER", "stub").lower() == "gtts":
        from app.adapters.gtts_adapter import GttsAdapter
        return GttsAdapter()

    return StubAsrTtsAdapter()


@lru_cache
def get_storage_adapter() -> StoragePort:
    """Return StoragePort adapter based on settings."""
    return StubStorageAdapter()


@lru_cache
def get_otp_delivery_adapter() -> OtpDeliveryPort:
    """Return OtpDeliveryPort adapter.

    No SMS gateway is configured anywhere in this project — see
    ``StubOtpDeliveryAdapter``'s docstring for why this is a stub rather
    than a ``real`` option the way ``DIAGNOSIS_MODEL=real`` is.
    """
    return StubOtpDeliveryAdapter()


@lru_cache
def get_land_registry_adapter() -> LandRegistryPort:
    """Return LandRegistryPort adapter based on ``LAND_API_MODE`` (PRD §1.5,
    §5.3). ``mock`` accelerates a small whitelist of survey numbers; ``live``
    represents the real (unavailable) state portal and always falls into
    HITL — flipping this flag alone demonstrates both contract §2.7 response
    shapes from one build."""
    settings = get_settings()
    if settings.LAND_API_MODE == "live":
        return LiveLandRegistryAdapter()
    return MockLandRegistryAdapter()
