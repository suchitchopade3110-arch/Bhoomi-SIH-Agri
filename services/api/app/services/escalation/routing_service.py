"""Agronomist routing (PRD §5.11, execution plan item 3).

Real by default: queries the agronomist roster for the nearest available
agronomist, falling back to the next available, raising
``OFFICER_UNAVAILABLE`` only when the whole pool is unavailable.
``ROUTING_MODE=demo_fixed`` bypasses the query and always assigns
``DEMO_FIXED_AGRONOMIST`` for a reliable pitch demo — the interface below
stays identical either way, so flipping the flag is the only change needed
to go from demo to real routing.
"""

from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.db import get_db
from app.core.errors import OfficerUnavailableError
from app.domain.escalation import select_agronomist
from app.repositories.agronomist_repository import AgronomistRepository
from sqlalchemy.ext.asyncio import AsyncSession


class RoutingService:
    def __init__(self, agronomist_repo: AgronomistRepository, settings: Settings) -> None:
        self._agronomists = agronomist_repo
        self._settings = settings

    async def assign_agronomist(self, jurisdiction: str | None = None) -> str:
        """Return the identifier of the agronomist a new case should be
        assigned to.

        Raises:
            OfficerUnavailableError: (``OFFICER_UNAVAILABLE``, contract
                §2.1) if no agronomist in the roster is available.
        """
        if self._settings.ROUTING_MODE == "demo_fixed":
            return self._settings.DEMO_FIXED_AGRONOMIST

        candidates = await self._agronomists.list_candidates()
        chosen = select_agronomist(candidates, jurisdiction=jurisdiction)
        if chosen is None:
            raise OfficerUnavailableError(
                message="No extension officer is currently available for this jurisdiction.",
                details={"jurisdiction": jurisdiction},
            )
        return chosen.identifier

    async def record_assignment(self, identifier: str) -> None:
        """Bump the assigned agronomist's load — a no-op in demo_fixed mode
        (there's no roster row backing the fixed demo identifier to bump)."""
        if self._settings.ROUTING_MODE == "real":
            await self._agronomists.increment_case_count(identifier)

    async def record_resolution(self, identifier: str) -> None:
        """Free up capacity on case resolution — the counterpart to
        ``record_assignment``, same demo_fixed no-op."""
        if self._settings.ROUTING_MODE == "real":
            await self._agronomists.decrement_case_count(identifier)


def get_agronomist_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> AgronomistRepository:
    return AgronomistRepository(session)


def get_routing_service(
    agronomist_repo: Annotated[AgronomistRepository, Depends(get_agronomist_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> RoutingService:
    return RoutingService(agronomist_repo, settings)
