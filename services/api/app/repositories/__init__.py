"""Data access repository interfaces, Postgres-backed implementations, and
in-memory fallback doubles (kept for DB-free unit tests)."""

from app.repositories.interfaces import (
    AdvisoryRepository,
    AssetRepository,
    CaseRepository,
    FarmRepository,
    HealthRepository,
    SchemeRepository,
    UserRepository,
)
from app.repositories.in_memory import (
    InMemoryAdvisoryRepository,
    InMemoryAssetRepository,
    InMemoryCaseRepository,
    InMemoryFarmRepository,
    InMemoryHealthRepository,
    InMemorySchemeRepository,
    InMemoryUserRepository,
)
from app.repositories.dependencies import (
    get_asset_repository,
    get_case_repository,
    get_farm_health_context_reader,
    get_farm_repository,
    get_health_snapshot_repository,
    get_knowledge_chunk_reader,
    get_problem_load_reader,
    get_problem_writer,
    get_scheme_repository,
    get_treatment_trend_reader,
    get_user_repository,
)
from app.repositories.health_snapshot_repository import HealthSnapshotRepository
from app.repositories.postgres import (
    PostgresAssetRepository,
    PostgresCaseRepository,
    PostgresFarmRepository,
    PostgresSchemeRepository,
    PostgresUserRepository,
)

__all__ = [
    "UserRepository",
    "FarmRepository",
    "CaseRepository",
    "AdvisoryRepository",
    "HealthRepository",
    "SchemeRepository",
    "AssetRepository",
    "InMemoryUserRepository",
    "InMemoryFarmRepository",
    "InMemoryCaseRepository",
    "InMemoryAdvisoryRepository",
    "InMemoryHealthRepository",
    "InMemorySchemeRepository",
    "InMemoryAssetRepository",
    "HealthSnapshotRepository",
    "PostgresUserRepository",
    "PostgresFarmRepository",
    "PostgresCaseRepository",
    "PostgresSchemeRepository",
    "PostgresAssetRepository",
    "get_user_repository",
    "get_farm_repository",
    "get_case_repository",
    "get_health_snapshot_repository",
    "get_knowledge_chunk_reader",
    "get_problem_load_reader",
    "get_problem_writer",
    "get_treatment_trend_reader",
    "get_farm_health_context_reader",
    "get_scheme_repository",
    "get_asset_repository",
]
