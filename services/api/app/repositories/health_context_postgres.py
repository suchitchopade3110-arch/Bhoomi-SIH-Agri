"""Postgres-backed implementations of the ``health_context.py`` Protocols
(Phase 5) — the real ``Problem`` / ``FollowUp`` / ``Farm`` aggregates that
``repositories/health_context.py``'s module docstring said would eventually
land. ``health_service.py`` is unchanged by this swap, as promised there.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import FollowupResponse, ProblemSeverity, ProblemStatus
from app.domain.farm_reference_data import get_crop_ideal
from app.models.farm import Farm
from app.models.followup import FollowUp
from app.models.problem import Problem
from app.repositories.health_context import (
    FarmHealthContext,
    OpenProblemRecord,
    TreatmentTrend,
)


class PostgresProblemLoadReader:
    """Real ``ProblemLoadReader`` / ``ProblemWriter`` backed by ``problems``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_open_problems(self, farm_id: str) -> list[OpenProblemRecord]:
        stmt = select(Problem).where(Problem.farm_id == farm_id, Problem.status == ProblemStatus.OPEN.value)
        result = await self._session.execute(stmt)
        return [
            OpenProblemRecord(problem_id=row.id, severity=ProblemSeverity(row.severity))
            for row in result.scalars().all()
        ]

    async def add_open_problem(self, farm_id: str, problem: OpenProblemRecord) -> None:
        row = Problem(
            id=problem.problem_id,
            farm_id=farm_id,
            label=problem.label or "unspecified",
            severity=problem.severity.value,
            status=ProblemStatus.OPEN.value,
        )
        self._session.add(row)
        await self._session.commit()

    async def get_latest_open_problem(self, farm_id: str) -> OpenProblemRecord | None:
        stmt = (
            select(Problem)
            .where(Problem.farm_id == farm_id, Problem.status == ProblemStatus.OPEN.value)
            .order_by(Problem.created_at.desc())
            .limit(1)
        )
        row = (await self._session.execute(stmt)).scalars().first()
        if row is None:
            return None
        return OpenProblemRecord(problem_id=row.id, severity=ProblemSeverity(row.severity), label=row.label)

    async def set_problem_severity(self, problem_id: str, severity: ProblemSeverity) -> None:
        row = await self._session.get(Problem, problem_id)
        if row is not None:
            row.severity = severity.value
            await self._session.commit()

    async def resolve_problem(self, problem_id: str) -> None:
        row = await self._session.get(Problem, problem_id)
        if row is not None:
            row.status = ProblemStatus.RESOLVED.value
            row.resolved_at = datetime.utcnow()
            await self._session.commit()


class PostgresTreatmentTrendReader:
    """Real ``TreatmentTrendReader`` backed by ``followups`` + ``problems``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record_followup(
        self,
        followup_id: str,
        problem_id: str,
        farm_id: str,
        response: FollowupResponse,
        farmer_notes: str | None,
        photo_asset_id: str | None,
    ) -> None:
        row = FollowUp(
            id=followup_id,
            problem_id=problem_id,
            farm_id=farm_id,
            response=response.value,
            farmer_notes=farmer_notes,
            photo_asset_id=photo_asset_id,
        )
        self._session.add(row)
        await self._session.commit()

    async def get_treatment_trend(self, farm_id: str) -> TreatmentTrend:
        followup_stmt = (
            select(FollowUp).where(FollowUp.farm_id == farm_id).order_by(FollowUp.created_at.desc()).limit(1)
        )
        result = await self._session.execute(followup_stmt)
        latest = result.scalars().first()

        consecutive_got_worse = 0
        if latest is not None and latest.response == FollowupResponse.GOT_WORSE.value:
            recent_stmt = (
                select(FollowUp).where(FollowUp.farm_id == farm_id).order_by(FollowUp.created_at.desc()).limit(20)
            )
            recent = (await self._session.execute(recent_stmt)).scalars().all()
            for f in recent:
                if f.response == FollowupResponse.GOT_WORSE.value:
                    consecutive_got_worse += 1
                else:
                    break

        resolved_stmt = (
            select(Problem)
            .where(Problem.farm_id == farm_id, Problem.status == ProblemStatus.RESOLVED.value)
            .order_by(Problem.resolved_at.desc())
            .limit(1)
        )
        resolved_row = (await self._session.execute(resolved_stmt)).scalars().first()
        # "Confirmed" resolution == resolved via the agronomist case-resolution
        # flow, which always sets resolved_at — a farmer just marking
        # "improved" never resolves the Problem row itself (contract §2.13).
        confirmed_resolved = resolved_row is not None

        return TreatmentTrend(
            latest_followup_response=FollowupResponse(latest.response) if latest else None,
            consecutive_got_worse_count=consecutive_got_worse,
            problem_resolved_with_confirmed_treatment=confirmed_resolved,
        )


class PostgresFarmHealthContextReader:
    """Real ``FarmHealthContextReader`` backed by ``farms``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_context(self, farm_id: str) -> FarmHealthContext | None:
        row = await self._session.get(Farm, farm_id)
        if row is None:
            return None
        return FarmHealthContext(
            latitude=row.latitude,
            longitude=row.longitude,
            crop_ideal=get_crop_ideal(row.primary_crop),
            soil_moisture_pct=row.soil_moisture_pct,
            irrigation_delivered_mm=row.irrigation_delivered_mm,
            irrigation_required_mm=row.irrigation_required_mm,
            days_since_planting=row.days_since_planting,
            expected_stage_day=row.expected_stage_day or 0,
            days_since_last_scan=row.days_since_last_scan,
        )
