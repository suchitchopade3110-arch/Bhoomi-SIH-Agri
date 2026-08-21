"""All DB access for the Case aggregate (PRD §5.11, contract §2.13).

Named ``EscalationCaseRepository`` — not ``CaseRepository`` — to avoid
colliding with the Phase-0 ``repositories.interfaces.CaseRepository``
Protocol, a generic dict-based placeholder that predates this real,
ORM-backed implementation and is left alone rather than touched here.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case


class EscalationCaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        farm_id: str,
        problem_id: str | None,
        reason: str,
        trigger: str,
        assigned_to: str | None,
        summary: dict,
        status: str = "open",
    ) -> Case:
        case = Case(
            farm_id=farm_id,
            problem_id=problem_id,
            status=status,
            reason=reason,
            trigger=trigger,
            assigned_to=assigned_to,
            summary=summary,
        )
        self._session.add(case)
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def get_by_id(self, case_id: str) -> Case | None:
        return await self._session.get(Case, case_id)

    async def update_summary(self, case_id: str, summary: dict) -> Case | None:
        case = await self.get_by_id(case_id)
        if case is None:
            return None
        case.summary = summary
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def list_queue(
        self, assigned_to: str | None = None, limit: int = 20, cursor: str | None = None
    ) -> tuple[list[Case], str | None]:
        """Newest-first, cursor-paginated case queue (contract §2.1, §2.13's
        ``GET /agronomist/case-queue``)."""
        stmt = select(Case).order_by(Case.created_at.desc(), Case.id.desc())
        if assigned_to:
            stmt = stmt.where(Case.assigned_to == assigned_to)
        if cursor:
            anchor = await self._session.get(Case, cursor)
            if anchor is not None:
                stmt = stmt.where(
                    (Case.created_at < anchor.created_at)
                    | ((Case.created_at == anchor.created_at) & (Case.id < anchor.id))
                )
        stmt = stmt.limit(limit + 1)

        result = await self._session.execute(stmt)
        rows = list(result.scalars().all())

        next_cursor: str | None = None
        if len(rows) > limit:
            rows = rows[:limit]
            next_cursor = rows[-1].id
        return rows, next_cursor

    async def resolve(self, case_id: str, diagnosis: str, treatment: str, notes: str | None) -> Case | None:
        case = await self.get_by_id(case_id)
        if case is None:
            return None
        case.status = "resolved"
        case.diagnosis = diagnosis
        case.treatment = treatment
        case.notes = notes
        case.resolved_at = datetime.utcnow()
        await self._session.commit()
        await self._session.refresh(case)
        return case

    async def update_assignment(self, case_id: str, assigned_to: str, status: str = "assigned") -> Case | None:
        case = await self.get_by_id(case_id)
        if case is None:
            return None
        case.assigned_to = assigned_to
        case.status = status
        await self._session.commit()
        await self._session.refresh(case)
        return case
