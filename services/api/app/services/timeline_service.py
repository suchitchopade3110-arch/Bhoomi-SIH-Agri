"""Farm living timeline service (contract §2.12, PRD §5.9) — the case file.

Reads across several aggregates (Problem, FollowUp, Case, HealthSnapshot)
purely to render a chronological feed; there's no business rule here, so —
unlike every other service — this one queries the ORM directly via an
injected session rather than through per-aggregate repositories, the same
way a reporting/read-model query would in a larger system.
"""

from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.case import Case
from app.models.followup import FollowUp
from app.models.health_snapshot import HealthSnapshot
from app.models.problem import Problem
from app.schemas.timeline import TimelineEventResponse, TimelineResponse


class TimelineService:
    """Compiles a chronological event feed for one farm."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_timeline(self, farm_id: str) -> TimelineResponse:
        events: list[TimelineEventResponse] = []

        problems = (await self._session.execute(select(Problem).where(Problem.farm_id == farm_id))).scalars().all()
        for p in problems:
            events.append(
                TimelineEventResponse(
                    event_id=p.id,
                    farm_id=farm_id,
                    event_type="diagnosis",
                    title=f"Diagnosed: {p.label}",
                    description=f"Severity {p.severity}, status {p.status}.",
                    metadata={"problem_id": p.id, "severity": p.severity, "status": p.status},
                    created_at=p.created_at,
                )
            )

        followups = (
            (await self._session.execute(select(FollowUp).where(FollowUp.farm_id == farm_id))).scalars().all()
        )
        for f in followups:
            events.append(
                TimelineEventResponse(
                    event_id=f.id,
                    farm_id=farm_id,
                    event_type="followup",
                    title=f"Follow-up: {f.response}",
                    description=f.farmer_notes or "",
                    metadata={"problem_id": f.problem_id, "response": f.response},
                    created_at=f.created_at,
                )
            )

        cases = (await self._session.execute(select(Case).where(Case.farm_id == farm_id))).scalars().all()
        for c in cases:
            events.append(
                TimelineEventResponse(
                    event_id=c.id,
                    farm_id=farm_id,
                    event_type="escalation",
                    title=f"Escalated to {c.assigned_to or 'expert'}",
                    description=c.reason or "",
                    metadata={"case_id": c.id, "status": c.status},
                    created_at=c.created_at,
                )
            )

        snapshots = (
            (await self._session.execute(select(HealthSnapshot).where(HealthSnapshot.farm_id == farm_id)))
            .scalars()
            .all()
        )
        for s in snapshots:
            events.append(
                TimelineEventResponse(
                    event_id=s.id,
                    farm_id=farm_id,
                    event_type="health_update",
                    title=f"Health score: {s.score if s.score is not None else 'unrated'}",
                    description=f"Band: {s.band}.",
                    health_score_delta=None,
                    metadata={"triggering_input": s.triggering_input},
                    created_at=s.computed_at,
                )
            )

        events.sort(key=lambda e: e.created_at)
        return TimelineResponse(farm_id=farm_id, events=events)

    async def append_event(self, event: TimelineEventResponse) -> TimelineEventResponse:
        """Contract §2.12's ``POST /timeline/events`` — every real event in
        this system already originates from a specific aggregate write
        (diagnose/followup/escalate/health recompute), so this endpoint is
        for client-side-only annotations (e.g. a farmer's free-text note)
        that don't need their own aggregate; it's echoed back, not persisted
        as a new table — a documented scope cut, see final report."""
        if not event.event_id:
            event.event_id = str(uuid4())
        return event


def get_timeline_service(session: Annotated[AsyncSession, Depends(get_db)]) -> TimelineService:
    return TimelineService(session)
