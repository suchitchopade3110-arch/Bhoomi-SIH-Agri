"""FastAPI dependency providers for repositories."""

from functools import lru_cache
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
