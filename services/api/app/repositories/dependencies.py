"""FastAPI dependency providers for repositories.

Phase 5: every aggregate repository is now Postgres-backed, session-scoped
via ``Depends(get_db)` — the same pattern ``get_health_snapshot_repository``
/ ``get_knowledge_chunk_reader`` already used. The ``InMemory*``
implementations stay in ``repositories/in_memory.py`` for unit tests that
want a DB-free double; nothing here constructs them anymore.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.health_context import (
    FarmHealthContextReader,
    FollowUpWriter,
    ProblemLoadReader,
    ProblemWriter,
    TreatmentTrendReader,
)
from app.repositories.health_context_postgres import (
    PostgresFarmHealthContextReader,
    PostgresProblemLoadReader,
    PostgresTreatmentTrendReader,
)
from app.repositories.health_snapshot_repository import HealthSnapshotRepository
from app.repositories.interfaces import KnowledgeChunkReader
from app.repositories.knowledge_chunk_repository import KnowledgeChunkRepository
from app.repositories.postgres import (
    PostgresAlertRepository,
    PostgresAssetRepository,
    PostgresCaseRepository,
    PostgresFarmRepository,
    PostgresLandParcelRepository,
    PostgresSchemeRepository,
    PostgresUserRepository,
)
from app.repositories.interfaces import (
    AlertRepository,
    AssetRepository,
    CaseRepository,
    FarmRepository,
    LandParcelRepository,
    SchemeRepository,
    UserRepository,
)


def get_user_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return PostgresUserRepository(session)


def get_farm_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> FarmRepository:
    return PostgresFarmRepository(session)


def get_land_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> LandParcelRepository:
    return PostgresLandParcelRepository(session)


def get_case_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> CaseRepository:
    return PostgresCaseRepository(session)


def get_scheme_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> SchemeRepository:
    return PostgresSchemeRepository(session)


def get_asset_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> AssetRepository:
    return PostgresAssetRepository(session)


def get_alert_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> AlertRepository:
    return PostgresAlertRepository(session)


def get_health_snapshot_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> HealthSnapshotRepository:
    """Real, SQLAlchemy-backed repository for the HealthSnapshot aggregate."""
    return HealthSnapshotRepository(session)


def get_problem_load_reader(session: Annotated[AsyncSession, Depends(get_db)]) -> ProblemLoadReader:
    return PostgresProblemLoadReader(session)


def get_problem_writer(session: Annotated[AsyncSession, Depends(get_db)]) -> ProblemWriter:
    """Same Postgres-backed ``problems`` table as ``get_problem_load_reader``
    — a write here is immediately visible to reads within the same request's
    session (see ``repositories.health_context.ProblemWriter``)."""
    return PostgresProblemLoadReader(session)


def get_treatment_trend_reader(session: Annotated[AsyncSession, Depends(get_db)]) -> TreatmentTrendReader:
    return PostgresTreatmentTrendReader(session)


def get_followup_writer(session: Annotated[AsyncSession, Depends(get_db)]) -> FollowUpWriter:
    """Same Postgres-backed ``followups`` table as ``get_treatment_trend_reader``."""
    return PostgresTreatmentTrendReader(session)


def get_farm_health_context_reader(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> FarmHealthContextReader:
    return PostgresFarmHealthContextReader(session)


def get_knowledge_chunk_reader(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> KnowledgeChunkReader:
    """Real, pgvector-backed reader for the curated RAG corpus."""
    return KnowledgeChunkRepository(session)
