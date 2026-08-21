"""All DB access for the Agronomist directory (PRD §5.11 routing). Real,
Postgres-backed.
"""

from dataclasses import dataclass
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agronomist import Agronomist


@dataclass(frozen=True)
class AgronomistRecord:
    """One agronomist, as read from the directory."""

    id: str
    name: str
    kvk_center: str
    district: str


class AgronomistDirectory(Protocol):
    """Read access to the agronomist routing directory (PRD §5.11)."""

    async def get_by_name(self, name: str) -> AgronomistRecord | None: ...
    async def find_available_in_district(self, district: str) -> AgronomistRecord | None: ...
    async def find_any_available(self) -> AgronomistRecord | None: ...


def _to_record(row: Agronomist) -> AgronomistRecord:
    return AgronomistRecord(id=row.id, name=row.name, kvk_center=row.kvk_center, district=row.district)


class AgronomistRepository:
    """Real, Postgres-backed ``AgronomistDirectory``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> AgronomistRecord | None:
        stmt = select(Agronomist).where(Agronomist.name == name)
        row = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_record(row) if row is not None else None

    async def find_available_in_district(self, district: str) -> AgronomistRecord | None:
        stmt = (
            select(Agronomist)
            .where(Agronomist.district == district, Agronomist.is_available.is_(True))
            .order_by(Agronomist.name)
            .limit(1)
        )
        row = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_record(row) if row is not None else None

    async def find_any_available(self) -> AgronomistRecord | None:
        stmt = (
            select(Agronomist)
            .where(Agronomist.is_available.is_(True))
            .order_by(Agronomist.district, Agronomist.name)
            .limit(1)
        )
        row = (await self._session.execute(stmt)).scalar_one_or_none()
        return _to_record(row) if row is not None else None
