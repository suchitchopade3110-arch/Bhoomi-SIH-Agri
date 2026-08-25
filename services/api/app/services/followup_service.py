"""Closed-loop follow-up check-in service (contract §2.12, PRD §5.10).

Improved demotes a problem's severity one tier (or resolves it if already at
the lightest tier); No Change leaves it as-is; Got Worse promotes it one
tier and — per the contract §2.12 example — always auto-escalates. A fresh
follow-up photo is also a fresh field scan, so it resets the health engine's
monitoring-recency input, same as a diagnosis.
"""

from typing import Annotated
from uuid import uuid4

from fastapi import Depends

from app.core.enums import FollowupResponse, ProblemSeverity
from app.core.errors import NotFoundError, ValidationError
from app.domain.health.inputs import TriggeringInput
from app.repositories.dependencies import get_farm_repository, get_followup_writer, get_problem_writer
from app.repositories.health_context import FollowUpWriter, ProblemWriter
from app.repositories.interfaces import FarmRepository
from app.schemas.followup import FollowupCheckinRequest, FollowupCheckinResponse, SeverityChange
from app.schemas.health import RiskChange
from app.services.efficacy.tracking_service import EfficacyTrackingService, get_efficacy_tracking_service
from app.services.escalation_service import EscalationService, get_escalation_service
from app.services.health_service import HealthService, get_health_service
from app.services.health_snapshot_mapping import snapshot_row_to_schema

FOLLOWUP_RESETS_DAYS_SINCE_LAST_SCAN = 0

# One severity tier up/down (PRD §7.3).
_SEVERITY_ORDER: list[ProblemSeverity] = [ProblemSeverity.EARLY, ProblemSeverity.MODERATE, ProblemSeverity.SEVERE]


def _promote(severity: ProblemSeverity) -> ProblemSeverity:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _demote(severity: ProblemSeverity) -> ProblemSeverity | None:
    """Returns ``None`` when the problem should resolve outright (already at
    the lightest tier and still improving)."""
    idx = _SEVERITY_ORDER.index(severity)
    if idx == 0:
        return None
    return _SEVERITY_ORDER[idx - 1]


class FollowupService:
    """Applies a farmer check-in to its problem and recomputes health."""

    def __init__(
        self,
        problem_writer: ProblemWriter,
        followup_writer: FollowUpWriter,
        farm_repo: FarmRepository,
        health_service: HealthService,
        escalation_service: EscalationService,
        efficacy_tracking: EfficacyTrackingService | None = None,
    ) -> None:
        self._problems = problem_writer
        self._followups = followup_writer
        self._farms = farm_repo
        self._health = health_service
        self._escalation = escalation_service
        self._efficacy_tracking = efficacy_tracking

    async def checkin(self, request: FollowupCheckinRequest) -> FollowupCheckinResponse:
        problem_id = request.problem_id
        if problem_id is None:
            latest = await self._problems.get_latest_open_problem(request.farm_id)
            if latest is None:
                raise ValidationError(
                    "No open problem to check in on for this farm.", details={"farm_id": request.farm_id}
                )
            problem_id = latest.problem_id
            current_severity = latest.severity
        else:
            open_problems = await self._problems.get_open_problems(request.farm_id)
            match = next((p for p in open_problems if p.problem_id == problem_id), None)
            if match is None:
                raise NotFoundError("Open problem not found for this farm.", details={"problem_id": problem_id})
            current_severity = match.severity

        auto_escalated = False
        escalation_id: str | None = None
        followup_id = str(uuid4())

        # Captured before any mutation below, so `risk.from_` reflects the
        # farm's state walking into this check-in, not after it.
        previous_snapshot = await self._health.get_latest(request.farm_id)

        await self._followups.record_followup(
            followup_id=followup_id,
            problem_id=problem_id,
            farm_id=request.farm_id,
            response=request.response,
            farmer_notes=request.farmer_notes,
            photo_asset_id=request.photo_asset_id,
        )

        new_severity: ProblemSeverity | None = current_severity
        if request.response == FollowupResponse.GOT_WORSE:
            new_severity = _promote(current_severity)
            await self._problems.set_problem_severity(problem_id, new_severity)
        elif request.response == FollowupResponse.IMPROVED:
            new_severity = _demote(current_severity)
            if new_severity is None:
                await self._problems.resolve_problem(problem_id)
            else:
                await self._problems.set_problem_severity(problem_id, new_severity)
        # NO_CHANGE: severity untouched (new_severity stays == current_severity).

        if request.photo_asset_id is not None:
            farm = await self._farms.get_by_id(request.farm_id)
            if farm is not None:
                await self._farms.update(request.farm_id, {"days_since_last_scan": FOLLOWUP_RESETS_DAYS_SINCE_LAST_SCAN})

        if self._efficacy_tracking is not None:
            await self._efficacy_tracking.attribute_followup(problem_id=problem_id, response=request.response)

        snapshot = await self._health.recompute(
            request.farm_id,
            triggering_input=TriggeringInput(
                type="followup", details={"problem_id": problem_id, "response": request.response.value}
            ),
        )

        if request.response == FollowupResponse.GOT_WORSE:
            escalation = await self._escalation.escalate_for_followup(
                farm_id=request.farm_id,
                problem_id=problem_id,
                reason="Farmer reported the problem got worse on follow-up.",
                severity=_promote(current_severity),
            )
            auto_escalated = True
            escalation_id = escalation.escalation_id

        return FollowupCheckinResponse(
            followup_id=followup_id,
            problem_id=problem_id,
            response=request.response,
            auto_escalated=auto_escalated,
            escalation_id=escalation_id,
            severity_change=SeverityChange(from_=current_severity, to=new_severity),
            risk=RiskChange(
                from_=previous_snapshot.score,
                to=snapshot.score,
                band=snapshot_row_to_schema(snapshot).band,
            ),
            updated_health_snapshot=snapshot_row_to_schema(snapshot),
            spoken_summary=f"Thanks for the update — your health score is now {snapshot.score}.",
        )


def get_followup_service(
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    followup_writer: Annotated[FollowUpWriter, Depends(get_followup_writer)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
    efficacy_tracking: Annotated[EfficacyTrackingService, Depends(get_efficacy_tracking_service)],
) -> FollowupService:
    return FollowupService(
        problem_writer, followup_writer, farm_repo, health_service, escalation_service, efficacy_tracking
    )
