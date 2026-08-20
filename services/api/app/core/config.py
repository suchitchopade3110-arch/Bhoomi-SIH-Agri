"""Configuration settings for Bhoomi API using Pydantic Settings."""

from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/bhoomi",
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
    LLM_API_KEY: str = "mock-llm-api-key"
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"
    EMBEDDING_MODEL: str = "BAAI/bge-m3"

    # Weather API (Open-Meteo)
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"

    # ML & Voice Service URL (if microservice mode)
    ML_SERVICE_URL: str = "http://localhost:8001"

    # Feature Flags
    LAND_API_MODE: Literal["mock", "live"] = Field(
        default="mock",
        description="Cadastral land API mode: 'mock' uses canned surveyor data, 'live' calls state portal",
    )
    DIAGNOSIS_MODEL: Literal["real", "stub"] = Field(
        default="stub",
        description="Crop disease diagnosis mode: 'real' runs PyTorch model, 'stub' returns settable confidence",
    )

    # Core Domain Thresholds (Enforced in orchestration layer)
    CONFIDENCE_GATE: float = Field(
        default=0.70,
        description="Decision gate threshold: Below this confidence, diagnosis auto-escalates to KVK expert",
    )
    RAG_RELEVANCE_THRESHOLD: float = Field(
        default=0.35,
        description="TODO-tune: Cosine similarity cutoff for RAG retrieval; below this, system reports no relevant source",
    )

    # Health score default rubric version
    WEIGHTS_VERSION: str = "v1.0.0"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton provider for FastAPI dependency injection."""
    return Settings()


settings = get_settings()
