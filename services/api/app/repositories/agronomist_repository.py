"""All DB access for the Agronomist roster (PRD §5.11, execution plan item 3)."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.escalation import AgronomistCandidate
from app.models.agronomist import Agronomist


class AgronomistRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_candidates(self) -> list[AgronomistCandidate]:
        """All agronomists, shaped as the pure ``domain.escalation.routing``
        selector expects — the DB is the only place jurisdiction/capacity
        data lives; selecting among them is pure."""
        result = await self._session.execute(select(Agronomist))
        return [
            AgronomistCandidate(
                identifier=a.identifier,
                jurisdiction=a.jurisdiction,
                is_available=a.is_available,
                active_case_count=a.active_case_count,
            )
            for a in result.scalars().all()
        ]

    async def get_by_identifier(self, identifier: str) -> Agronomist | None:
        result = await self._session.execute(select(Agronomist).where(Agronomist.identifier == identifier))
        return result.scalar_one_or_none()

    async def increment_case_count(self, identifier: str) -> None:
        agronomist = await self.get_by_identifier(identifier)
        if agronomist is not None:
            agronomist.active_case_count += 1
            await self._session.commit()

    async def decrement_case_count(self, identifier: str) -> None:
        agronomist = await self.get_by_identifier(identifier)
        if agronomist is not None:
            agronomist.active_case_count = max(0, agronomist.active_case_count - 1)
            await self._session.commit()
