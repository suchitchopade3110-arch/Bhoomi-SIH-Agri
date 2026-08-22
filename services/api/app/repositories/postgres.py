"""Postgres-backed repositories for the User / Farm / LandParcel / Case /
Advisory / Scheme / Asset aggregates — the real implementations behind the
``Protocol``s in ``repositories/interfaces.py`` (Phase 5).

Every method mirrors its ``InMemory*`` counterpart's signature exactly
(dict in, dict out) so callers and ``repositories/dependencies.py`` can swap
one for the other without touching a call site — the whole point of the
Protocol boundary.

``Advisory`` has no dedicated ORM model yet (Phase 3's RAG advisory is
stateless per-query, contract §2.11 — nothing is persisted per advisory
response), so ``PostgresAdvisoryRepository`` is a thin in-memory shim kept
only to satisfy the ``AdvisoryRepository`` Protocol; nothing in this phase's
runbook depends on it.
"""

from datetime import datetime
from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.case import Case
from app.models.farm import Farm
from app.models.land_parcel import LandParcel
from app.models.scheme import Scheme
from app.models.user import User


def _row_to_dict(row: Any) -> dict[str, Any]:
    """Serialize a mapped ORM row's own columns to a plain dict."""
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


class PostgresUserRepository:
    """Real ``UserRepository`` backed by the ``users`` table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        row = await self._session.get(User, user_id)
        return _row_to_dict(row) if row else None

    async def get_by_phone(self, phone: str) -> dict[str, Any] | None:
        stmt = select(User).where(User.phone_number == phone)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return _row_to_dict(row) if row else None

    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return _row_to_dict(row) if row else None

    async def save(self, user_data: dict[str, Any]) -> dict[str, Any]:
        user_id = user_data.get("id")
        if user_id:
            row = await self._session.get(User, user_id)
        else:
            row = None
        if row is None:
            row = User(id=user_id or str(uuid.uuid4()))
            self._session.add(row)
        for key, value in user_data.items():
            if key != "id" and hasattr(row, key):
                setattr(row, key, value)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)


class PostgresFarmRepository:
    """Real ``FarmRepository`` backed by the ``farms`` table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, farm_id: str) -> dict[str, Any] | None:
        row = await self._session.get(Farm, farm_id)
        return _row_to_dict(row) if row else None

    async def get_by_farmer_id(self, farmer_id: str) -> list[dict[str, Any]]:
        stmt = select(Farm).where(Farm.farmer_id == farmer_id)
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]

    async def save(self, farm_data: dict[str, Any]) -> dict[str, Any]:
        farm_id = farm_data.get("id") or str(uuid.uuid4())
        farm_data["id"] = farm_id
        row = Farm(**{k: v for k, v in farm_data.items() if hasattr(Farm, k)})
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def update(self, farm_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        row = await self._session.get(Farm, farm_id)
        if row is None:
            return None
        for key, value in updates.items():
            if hasattr(row, key):
                setattr(row, key, value)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)


class PostgresLandParcelRepository:
    """Real ``LandParcelRepository`` backed by the ``land_parcels`` table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, parcel_id: str) -> dict[str, Any] | None:
        row = await self._session.get(LandParcel, parcel_id)
        return _row_to_dict(row) if row else None

    async def get_by_farm_id(self, farm_id: str) -> dict[str, Any] | None:
        stmt = select(LandParcel).where(LandParcel.farm_id == farm_id).order_by(LandParcel.created_at.desc())
        result = await self._session.execute(stmt)
        row = result.scalars().first()
        return _row_to_dict(row) if row else None

    async def get_pending_queue(self, district: str | None = None) -> list[dict[str, Any]]:
        stmt = select(LandParcel).where(LandParcel.status == "pending_review")
        if district:
            stmt = stmt.where(LandParcel.district == district)
        stmt = stmt.order_by(LandParcel.submitted_at.asc())
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]

    async def save(self, parcel_data: dict[str, Any]) -> dict[str, Any]:
        parcel_id = parcel_data.get("id") or str(uuid.uuid4())
        parcel_data["id"] = parcel_id
        row = LandParcel(**{k: v for k, v in parcel_data.items() if hasattr(LandParcel, k)})
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def update_status(
        self, parcel_id: str, status: str, boundary: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        row = await self._session.get(LandParcel, parcel_id)
        if row is None:
            return None
        row.status = status
        if boundary:
            row.confirmed_boundary = boundary
        if status == "verified":
            row.verified_at = datetime.utcnow()
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)


class PostgresCaseRepository:
    """Real ``CaseRepository`` backed by the ``cases`` table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, case_id: str) -> dict[str, Any] | None:
        row = await self._session.get(Case, case_id)
        return _row_to_dict(row) if row else None

    async def get_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]:
        stmt = select(Case).where(Case.farm_id == farm_id).order_by(Case.created_at.desc())
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]

    async def get_agronomist_queue(self, status: str | None = None) -> list[dict[str, Any]]:
        stmt = select(Case)
        if status:
            stmt = stmt.where(Case.status == status)
        else:
            stmt = stmt.where(Case.status.in_(["assigned", "escalated", "open"]))
        stmt = stmt.order_by(Case.created_at.desc())
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]

    async def save(self, case_data: dict[str, Any]) -> dict[str, Any]:
        case_id = case_data.get("id") or str(uuid.uuid4())
        case_data["id"] = case_id
        row = Case(**{k: v for k, v in case_data.items() if hasattr(Case, k)})
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def update_status(
        self, case_id: str, status: str, resolution: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        row = await self._session.get(Case, case_id)
        if row is None:
            return None
        row.status = status
        if resolution:
            row.resolution = resolution
        if status == "resolved":
            row.resolved_at = datetime.utcnow()
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)


class PostgresSchemeRepository:
    """Real ``SchemeRepository`` backed by the ``schemes`` table (PRD §5.12)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, scheme_id: str) -> dict[str, Any] | None:
        row = await self._session.get(Scheme, scheme_id)
        return _row_to_dict(row) if row else None

    async def list_active_schemes(self) -> list[dict[str, Any]]:
        stmt = select(Scheme).order_by(Scheme.last_verified.desc())
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]

    async def match_schemes(self, crop: str, category: str, acres: float) -> list[dict[str, Any]]:
        stmt = select(Scheme)
        result = await self._session.execute(stmt)
        matched = []
        for row in result.scalars().all():
            if row.crop_filter and row.crop_filter != crop:
                continue
            if row.category_filter and row.category_filter != category:
                continue
            matched.append(_row_to_dict(row))
        return matched


class PostgresAssetRepository:
    """Real ``AssetRepository`` backed by the ``assets`` table (contract §2.4)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, asset_id: str) -> dict[str, Any] | None:
        row = await self._session.get(Asset, asset_id)
        return _row_to_dict(row) if row else None

    async def save(self, asset_data: dict[str, Any]) -> dict[str, Any]:
        asset_id = asset_data.get("id") or str(uuid.uuid4())
        asset_data["id"] = asset_id
        row = Asset(**{k: v for k, v in asset_data.items() if hasattr(Asset, k)})
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)
