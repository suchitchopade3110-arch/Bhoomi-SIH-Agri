"""Data access repository interfaces and in-memory fallback implementations."""

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
from app.repositories.dependencies import (
    get_advisory_repository,
    get_asset_repository,
    get_case_repository,
    get_farm_repository,
    get_health_repository,
    get_land_repository,
    get_scheme_repository,
    get_user_repository,
)

__all__ = [
    "UserRepository",
    "FarmRepository",
    "LandParcelRepository",
    "CaseRepository",
    "AdvisoryRepository",
    "HealthRepository",
    "SchemeRepository",
    "AssetRepository",
    "InMemoryUserRepository",
    "InMemoryFarmRepository",
    "InMemoryLandParcelRepository",
    "InMemoryCaseRepository",
    "InMemoryAdvisoryRepository",
    "InMemoryHealthRepository",
    "InMemorySchemeRepository",
    "InMemoryAssetRepository",
    "get_user_repository",
    "get_farm_repository",
    "get_land_repository",
    "get_case_repository",
    "get_advisory_repository",
    "get_health_repository",
    "get_scheme_repository",
    "get_asset_repository",
]
