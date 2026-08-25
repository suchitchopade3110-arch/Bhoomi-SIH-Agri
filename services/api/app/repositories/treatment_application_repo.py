"""Postgres-backed ``TreatmentApplicationRepository`` (SPEC-EFFICACY-001).

Same ``_row_to_dict`` dict-in/dict-out shape ``repositories/postgres.py``
uses everywhere else — kept in its own module rather than added to that
file since the ``treatment_applications`` table is Phase-4-only and this
keeps the diff for wiring it in localized.
"""

from datetime import datetime
from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.treatment_application import TreatmentApplication


def _row_to_dict(row: Any) -> dict[str, Any]:
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


class PostgresTreatmentApplicationRepository:
    """Real ``TreatmentApplicationRepository`` backed by ``treatment_applications``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def open_application(self, application: dict[str, Any]) -> dict[str, Any]:
        application_id = application.get("id") or str(uuid.uuid4())
        application["id"] = application_id
        row = TreatmentApplication(
            **{k: v for k, v in application.items() if hasattr(TreatmentApplication, k)}
        )
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def get_latest_open_for_problem(self, problem_id: str) -> dict[str, Any] | None:
        stmt = (
            select(TreatmentApplication)
            .where(
                TreatmentApplication.problem_id == problem_id,
                TreatmentApplication.final_outcome.is_(None),
            )
            .order_by(TreatmentApplication.applied_on.desc(), TreatmentApplication.created_at.desc())
            .limit(1)
        )
        row = (await self._session.execute(stmt)).scalars().first()
        return _row_to_dict(row) if row else None

    async def close_application(self, application_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        row = await self._session.get(TreatmentApplication, application_id)
        if row is None:
            return None
        for key, value in updates.items():
            if hasattr(row, key):
                setattr(row, key, value)
        row.updated_at = datetime.utcnow()
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def increment_followups(self, application_id: str) -> dict[str, Any] | None:
        row = await self._session.get(TreatmentApplication, application_id)
        if row is None:
            return None
        row.followups_to_resolution = (row.followups_to_resolution or 0) + 1
        row.updated_at = datetime.utcnow()
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def list_for_aggregation(
        self, pathogen_type: str, treatment_name: str, crop: str, district: str
    ) -> list[dict[str, Any]]:
        stmt = select(TreatmentApplication).where(
            TreatmentApplication.pathogen_type == pathogen_type,
            TreatmentApplication.treatment_name == treatment_name,
            TreatmentApplication.crop == crop,
            TreatmentApplication.district == district,
        )
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]
