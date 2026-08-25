"""Configuration settings for Bhoomi API using Pydantic Settings."""

from functools import lru_cache
from typing import Literal
from pydantic import Field, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


from app.domain.constants import (
    CONFIDENCE_GATE as DOMAIN_CONFIDENCE_GATE,
    PEST_CONFIDENCE_GATE as DOMAIN_PEST_CONFIDENCE_GATE,
    RAG_RELEVANCE_THRESHOLD_PRODUCTION,
    RAG_RELEVANCE_THRESHOLD_STUB,
)


class Settings(BaseSettings):
    """Application settings and feature flags loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # General
    PROJECT_NAME: str = "Bhoomi API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    APP_ENV: Literal["development", "staging", "production", "test"] = "development"
    DEBUG: bool = True

    # Database (PostgreSQL + PostGIS + pgvector)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5433/bhoomi",
        description="Async SQLAlchemy database connection URL",
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Security & JWT
    JWT_SECRET_KEY: str = Field(
        default="bhoomi-super-secret-key-change-in-production-sih25076",
        description="Secret key for signing JWT tokens",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Object Storage (S3 / MinIO / Cloudflare R2)
    STORAGE_ENDPOINT: str = "http://localhost:9000"
    STORAGE_BUCKET: str = "bhoomi-assets"
    STORAGE_ACCESS_KEY: str = "minioadmin"
    STORAGE_SECRET_KEY: str = "minioadmin"
    STORAGE_REGION: str = "us-east-1"
    STORAGE_SECURE: bool = False

    # LLM & Embedding Service
    LLM_PROVIDER: Literal["groq", "stub"] = Field(
        default="stub",
        description=(
            "LLM provider mode: 'groq' (real grounded generation via Groq's "
            "OpenAI-compatible API) | 'stub' (canned advisory text templated "
            "from retrieved chunks, no real generation)"
        ),
    )
    LLM_API_KEY: str = "mock-llm-api-key"
    LLM_BASE_URL: str = Field(
        default="https://api.groq.com/openai/v1",
        description="OpenAI-compatible base URL for the LLM provider (used only when LLM_PROVIDER='groq')",
    )
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"
    EMBEDDING_MODEL: str = "BAAI/bge-m3"

    # Weather API (Open-Meteo)
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"

    # ML & Voice Service URL (if microservice mode)
    ML_SERVICE_URL: str = "http://localhost:8001"

    # Feature Flags
    PROBLEM_STATEMENT: Literal["sih25076", "sih26131"] = Field(
        default="sih26131",
        description=(
            "Switches API surface between SIH25076 (Cadastral/Resource) and "
            "SIH26131 (Pest/Alert/Efficacy). See docs/specs/api_contract_sih26131_delta.md."
        ),
    )
    LAND_API_MODE: Literal["mock", "live"] = Field(
        default="mock",
        description="Cadastral land API mode: 'mock' uses canned surveyor data, 'live' calls state portal",
    )
    DIAGNOSIS_MODEL: Literal["real", "stub"] = Field(
        default="stub",
        description="Crop disease diagnosis mode: 'real' runs PyTorch model, 'stub' returns settable confidence",
    )
    EMBEDDING_PROVIDER: Literal["bge_m3", "stub"] = Field(
        default="stub",
        description="Embedding provider mode: 'bge_m3' (dense embeddings) | 'stub' (token-hashing vectors)",
    )

    # Core Domain Thresholds (Enforced in orchestration layer)
    CONFIDENCE_GATE: float = Field(
        default=DOMAIN_CONFIDENCE_GATE,
        description="Decision gate threshold: Below this confidence, diagnosis auto-escalates to KVK expert",
    )
    PEST_CONFIDENCE_GATE: float = Field(
        default=DOMAIN_PEST_CONFIDENCE_GATE,
        description="Decision gate threshold for pest diagnosis (independently tunable from CONFIDENCE_GATE)",
    )

    # RAG relevance thresholds: calibrated per embedding provider (sourced from domain constants)
    RAG_RELEVANCE_THRESHOLD_STUB: float = RAG_RELEVANCE_THRESHOLD_STUB
    RAG_RELEVANCE_THRESHOLD_PRODUCTION: float = RAG_RELEVANCE_THRESHOLD_PRODUCTION
    RAG_RELEVANCE_THRESHOLD_OVERRIDE: float | None = Field(
        default=None,
        description="Optional manual override for RAG relevance threshold",
    )

    @model_validator(mode="after")
    def _validate_llm_provider_credentials(self) -> "Settings":
        """Fail loudly at startup rather than silently falling back (PRD
        no-fabrication rule): a real ``LLM_PROVIDER`` with no usable key must
        never boot into a state that later returns fabricated advisory text."""
        if self.LLM_PROVIDER == "groq":
            key = self.LLM_API_KEY.strip()
            if not key or key == "mock-llm-api-key":
                raise ValueError(
                    "LLM_PROVIDER=groq requires a real LLM_API_KEY. Refusing to start with a "
                    "missing key or the mock placeholder ('mock-llm-api-key'). Set a real Groq "
                    "API key from console.groq.com, or set LLM_PROVIDER=stub."
                )
            if not key.startswith("gsk_"):
                raise ValueError(
                    "LLM_PROVIDER=groq but LLM_API_KEY does not look like a Groq key (Groq keys "
                    "start with 'gsk_'). Refusing to start with a malformed key."
                )
        return self

    @computed_field
    @property
    def RAG_RELEVANCE_THRESHOLD(self) -> float:
        """Computed relevance threshold: automatically aligns with active embedding adapter."""
        if self.RAG_RELEVANCE_THRESHOLD_OVERRIDE is not None:
            return self.RAG_RELEVANCE_THRESHOLD_OVERRIDE
        return (
            self.RAG_RELEVANCE_THRESHOLD_PRODUCTION
            if self.EMBEDDING_PROVIDER == "bge_m3"
            else self.RAG_RELEVANCE_THRESHOLD_STUB
        )

    # Health score default rubric version
    WEIGHTS_VERSION: str = "v1.0.0"

    # Voice / ASR / TTS
    ASR_PROVIDER: str = Field(
        default="stub",
        description="ASR provider: 'bhashini' | 'sarvam' | 'stub'",
    )
    TTS_PROVIDER: str = Field(
        default="stub",
        description="TTS provider: 'bhashini' | 'gtts' | 'stub'",
    )
    CONFIRMATION_CONFIDENCE_FLOOR: float = Field(
        default=0.85,
        description="ASR confidence below this triggers read-back confirmation (PRD §5.1)",
    )

    # Bhashini API (optional — needed only when ASR_PROVIDER/TTS_PROVIDER = bhashini)
    BHASHINI_USER_ID: str = ""
    BHASHINI_API_KEY: str = ""
    BHASHINI_PIPELINE_ID: str = ""

    # Sarvam AI API (optional — needed only when ASR_PROVIDER/TTS_PROVIDER = sarvam)
    SARVAM_API_KEY: str = ""
    SARVAM_BASE_URL: str = "https://api.sarvam.ai"

    # Embedding
    EMBEDDING_DIM: int = 1024

    # Storage
    STORAGE_BACKEND: str = Field(
        default="local",
        description="Storage backend: 'local' | 's3'",
    )
    LOCAL_STORAGE_PATH: str = "./storage"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton provider for FastAPI dependency injection."""
    return Settings()


settings = get_settings()
