"""FastAPI dependency providers for repositories."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.health_context import (
    FarmHealthContextReader,
    InMemoryFarmHealthContextReader,
    InMemoryTreatmentTrendReader,
    ProblemLoadReader,
    ProblemWriter,
    TreatmentTrendReader,
)
from app.repositories.case_repository import EscalationCaseRepository
from app.repositories.health_snapshot_repository import HealthSnapshotRepository
from app.repositories.interfaces import KnowledgeChunkReader
from app.repositories.knowledge_chunk_repository import KnowledgeChunkRepository
from app.repositories.problem_registry import ProblemRegistry
from app.repositories.in_memory import (
    InMemoryAdvisoryRepository,
    InMemoryAssetRepository,
    InMemoryCaseRepository,
    InMemoryFarmRepository,
    InMemoryHealthRepository,
    InMemoryLandParcelRepository,
    InMemorySchemeRepository,
    InMemoryUserRepository,
)
from app.repositories.interfaces import (
    AdvisoryRepository,
    AssetRepository,
    CaseRepository,
    FarmRepository,
    HealthRepository,
    LandParcelRepository,
    SchemeRepository,
    UserRepository,
)

# Singletons for in-memory repositories
_user_repo = InMemoryUserRepository()
_farm_repo = InMemoryFarmRepository()
_land_repo = InMemoryLandParcelRepository()
_case_repo = InMemoryCaseRepository()
_advisory_repo = InMemoryAdvisoryRepository()
_health_repo = InMemoryHealthRepository()
_scheme_repo = InMemorySchemeRepository()
_asset_repo = InMemoryAssetRepository()


@lru_cache
def get_user_repository() -> UserRepository:
    return _user_repo


@lru_cache
def get_farm_repository() -> FarmRepository:
    return _farm_repo


@lru_cache
def get_land_repository() -> LandParcelRepository:
    return _land_repo


@lru_cache
def get_case_repository() -> CaseRepository:
    return _case_repo


@lru_cache
def get_advisory_repository() -> AdvisoryRepository:
    return _advisory_repo


@lru_cache
def get_health_repository() -> HealthRepository:
    return _health_repo


@lru_cache
def get_scheme_repository() -> SchemeRepository:
    return _scheme_repo


@lru_cache
def get_asset_repository() -> AssetRepository:
    return _asset_repo


def get_health_snapshot_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> HealthSnapshotRepository:
    """Real, SQLAlchemy-backed repository for the HealthSnapshot aggregate."""
    return HealthSnapshotRepository(session)


# Placeholder readers for aggregates (Farm profile, Problem, FollowUp) that
# don't have their own phase/migration yet — see repositories/health_context.py
# and repositories/problem_registry.py.
_problem_registry = ProblemRegistry()
_treatment_trend_reader = InMemoryTreatmentTrendReader()
_farm_health_context_reader = InMemoryFarmHealthContextReader()


@lru_cache
def get_problem_load_reader() -> ProblemLoadReader:
    """``ProblemRegistry`` structurally satisfies this Phase-1 Protocol —
    same singleton as ``get_problem_registry``, so a Phase-4 write is
    immediately visible to the health engine's reads."""
    return _problem_registry


@lru_cache
def get_problem_writer() -> ProblemWriter:
    return _problem_registry


@lru_cache
def get_problem_registry() -> ProblemRegistry:
    """The richer Phase-4 registry (escalation, follow-up, resolution) —
    same singleton as ``get_problem_load_reader``/``get_problem_writer``."""
    return _problem_registry


@lru_cache
def get_treatment_trend_reader() -> TreatmentTrendReader:
    return _treatment_trend_reader


@lru_cache
def get_treatment_trend_writer() -> InMemoryTreatmentTrendReader:
    """Same singleton as ``get_treatment_trend_reader``, typed concretely so
    callers can reach its ``set_trend`` (Phase 4's follow-up/resolve flows)."""
    return _treatment_trend_reader


@lru_cache
def get_farm_health_context_reader() -> FarmHealthContextReader:
    return _farm_health_context_reader


def get_knowledge_chunk_reader(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> KnowledgeChunkReader:
    """Real, pgvector-backed reader for the curated RAG corpus."""
    return KnowledgeChunkRepository(session)


def get_escalation_case_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> EscalationCaseRepository:
    """Real, SQLAlchemy-backed repository for the Case aggregate (Phase 4) —
    distinct from the Phase-0 ``get_case_repository`` dict-based placeholder."""
    return EscalationCaseRepository(session)
