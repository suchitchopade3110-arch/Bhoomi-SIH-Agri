"""All DB access for the Case aggregate (PRD §5.11, contract §2.13). Real,
Postgres-backed — Phase 4's escalation subsystem owns this table outright,
unlike the placeholder dict-based ``CaseRepository`` in
``repositories/interfaces.py`` that Phase 3 used before this table existed.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case


class CaseRepository:
    """Persists and reads ``Case`` rows."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, case: Case) -> Case:
        """Persist a new case."""
        self._session.add(case)
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def get_by_id(self, case_id: str) -> Case | None:
        return await self._session.get(Case, case_id)

    async def get_queue(self, status: str | None = None) -> list[Case]:
        """Newest-first case list, optionally filtered by status (contract
        §2.1's ``GET /agronomist/case-queue``)."""
        stmt = select(Case).order_by(Case.created_at.desc())
        if status is not None:
            stmt = stmt.where(Case.status == status)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, case: Case) -> Case:
        """Flush in-place mutations made directly on an already-loaded row
        (e.g. status/resolution set by ``ResolveService``) and return it."""
        await self._session.commit()
        await self._session.refresh(case)
        return case
