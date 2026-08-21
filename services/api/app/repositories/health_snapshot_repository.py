"""All DB access for the HealthSnapshot aggregate (contract §2.9)."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.health_snapshot import HealthSnapshot


class HealthSnapshotRepository:
    """Persists and reads ``HealthSnapshot`` rows for one farm at a time."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, snapshot: HealthSnapshot) -> HealthSnapshot:
        """Persist a new snapshot and return it with its generated id."""
        self._session.add(snapshot)
        await self._session.commit()
        await self._session.refresh(snapshot)
        return snapshot

    async def get_latest(self, farm_id: str) -> HealthSnapshot | None:
        """Most recent snapshot for a farm, or ``None`` if never computed."""
        stmt = (
            select(HealthSnapshot)
            .where(HealthSnapshot.farm_id == farm_id)
            .order_by(HealthSnapshot.computed_at.desc(), HealthSnapshot.id.desc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_history(
        self, farm_id: str, limit: int, cursor: str | None = None
    ) -> tuple[list[HealthSnapshot], str | None]:
        """Newest-first page of snapshots for a farm (contract §2.1 cursor pagination).

        Args:
            farm_id: UUID string of the farm.
            limit: Page size.
            cursor: The ``id`` of the last snapshot on the previous page, or
                ``None`` for the first page.

        Returns:
            ``(snapshots, next_cursor)`` — ``next_cursor`` is ``None`` once
            the history is exhausted.
        """
        stmt = (
            select(HealthSnapshot)
            .where(HealthSnapshot.farm_id == farm_id)
            .order_by(HealthSnapshot.computed_at.desc(), HealthSnapshot.id.desc())
        )
        if cursor:
            anchor = await self._session.get(HealthSnapshot, cursor)
            if anchor is not None:
                stmt = stmt.where(
                    (HealthSnapshot.computed_at < anchor.computed_at)
                    | (
                        (HealthSnapshot.computed_at == anchor.computed_at)
                        & (HealthSnapshot.id < anchor.id)
                    )
                )
        stmt = stmt.limit(limit + 1)

        result = await self._session.execute(stmt)
        rows = list(result.scalars().all())

        next_cursor: str | None = None
        if len(rows) > limit:
            rows = rows[:limit]
            next_cursor = rows[-1].id
        return rows, next_cursor
