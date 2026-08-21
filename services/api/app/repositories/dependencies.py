"""FastAPI dependency providers for repositories."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.health_context import (
    FarmHealthContextReader,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
    ProblemLoadReader,
    TreatmentTrendReader,
)
from app.repositories.health_snapshot_repository import HealthSnapshotRepository
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
# don't have their own phase/migration yet — see repositories/health_context.py.
_problem_load_reader = InMemoryProblemLoadReader()
_treatment_trend_reader = InMemoryTreatmentTrendReader()
_farm_health_context_reader = InMemoryFarmHealthContextReader()


@lru_cache
def get_problem_load_reader() -> ProblemLoadReader:
    return _problem_load_reader


@lru_cache
def get_treatment_trend_reader() -> TreatmentTrendReader:
    return _treatment_trend_reader


@lru_cache
def get_farm_health_context_reader() -> FarmHealthContextReader:
    return _farm_health_context_reader
