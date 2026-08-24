"""Expert escalation service — compiles and routes the Farm Case Summary
(contract §2.13, PRD §5.11).
"""

from datetime import datetime
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_roster_adapter
from app.core.enums import CaseStatus, ProblemSeverity
from app.core.errors import NotFoundError
from app.domain.escalation import build_case_summary
from app.domain.kvk_directory import DEFAULT_KVK_CENTER_ID
from app.domain.queue import QueueCase, compute_queue_positions, estimate_eta
from app.ports.roster import AgronomistRosterPort
from app.repositories.dependencies import get_case_repository, get_farm_repository
from app.repositories.interfaces import CaseRepository, FarmRepository
from app.schemas.escalation import EscalationCreateRequest, EscalationResponse
from app.services.kvk_routing import route_to_next_available_agronomist

# Fallback only for when the roster has no entries at all — i.e. no
# capacity data exists yet to route against (PRD §10 risk #10).
DEFAULT_ASSIGNED_AGRONOMIST = DEFAULT_KVK_CENTER_ID


class EscalationService:
    """Creates escalation Cases and compiles their CaseSummary."""

    def __init__(self, case_repo: CaseRepository, farm_repo: FarmRepository, roster: AgronomistRosterPort) -> None:
        self._cases = case_repo
        self._farms = farm_repo
        self._roster = roster

    async def _compile_and_save(
        self,
        farm_id: str,
        reason: str,
        severity: ProblemSeverity,
        problem_id: str | None,
        problem_label: str | None,
    ) -> EscalationResponse:
        farm = await self._farms.get_by_id(farm_id)
        if farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})

        open_case_counts_before = await self._cases.get_open_case_counts()
        assigned_to = await route_to_next_available_agronomist(
            self._cases, self._roster, default_agronomist=DEFAULT_ASSIGNED_AGRONOMIST
        )
        # This case's queue position at its assigned agronomist, before it's
        # counted itself — the case just ahead of it is the last one queued.
        queue_position = open_case_counts_before.get(assigned_to, 0) + 1
        eta = estimate_eta(queue_position, evaluated_at=datetime.utcnow())

        saved = await self._cases.save(
            {
                "farm_id": farm_id,
                "problem_id": problem_id,
                "reason": reason,
                "severity": severity.value,
                "status": CaseStatus.ESCALATED.value,
                "assigned_to": assigned_to,
            }
        )

        farm_info = {
            "id": farm_id,
            "farmer_name": farm.get("farm_name", "Unknown"),
            "village": farm.get("village", ""),
            "district": farm.get("district", ""),
            "primary_crop": farm.get("primary_crop", ""),
            "growth_stage": farm.get("growth_stage"),
            "land_status": farm.get("land_status"),
        }
        summary = build_case_summary(
            case_id=saved["id"],
            farm_info=farm_info,
            recent_events=[],
            current_health_score=0.0,
            problem_details={"label": problem_label or "unspecified", "severity": severity},
            assigned_officer_or_kvk=assigned_to,
            status=CaseStatus.ESCALATED,
        )
        await self._cases.update_status(saved["id"], CaseStatus.ESCALATED.value, resolution=None)

        return EscalationResponse(
            escalation_id=saved["id"],
            farm_id=farm_id,
            status=CaseStatus.ESCALATED,
            severity=severity,
            assigned_kvk_center=assigned_to,
            case_summary=summary,
            spoken_summary=summary.spoken_summary,
            queue_position=queue_position,
            eta=eta,
        )

    async def create_escalation(self, request: EscalationCreateRequest) -> EscalationResponse:
        return await self._compile_and_save(
            farm_id=request.farm_id,
            reason=request.reason,
            severity=request.severity,
            problem_id=None,
            problem_label=None,
        )

    async def escalate_for_followup(
        self, farm_id: str, problem_id: str, reason: str, severity: ProblemSeverity
    ) -> EscalationResponse:
        """PRD §5.10: "Got Worse ... triggers escalation" — called directly
        by ``FollowupService``, not through the public create-escalation route."""
        return await self._compile_and_save(
            farm_id=farm_id, reason=reason, severity=severity, problem_id=problem_id, problem_label=None
        )

    async def get_escalation_by_id(self, escalation_id: str) -> EscalationResponse:
        case = await self._cases.get_by_id(escalation_id)
        if case is None:
            raise NotFoundError("Escalation not found.", details={"escalation_id": escalation_id})
        farm = await self._farms.get_by_id(case["farm_id"])
        farm_info = {
            "id": case["farm_id"],
            "farmer_name": (farm or {}).get("farm_name", "Unknown"),
            "village": (farm or {}).get("village", ""),
            "district": (farm or {}).get("district", ""),
            "primary_crop": (farm or {}).get("primary_crop", ""),
            "growth_stage": (farm or {}).get("growth_stage"),
            "land_status": (farm or {}).get("land_status"),
        }
        summary = build_case_summary(
            case_id=case["id"],
            farm_info=farm_info,
            recent_events=[],
            current_health_score=0.0,
            problem_details={"severity": ProblemSeverity(case["severity"])},
            assigned_officer_or_kvk=case.get("assigned_to"),
            status=CaseStatus(case["status"]),
        )

        queue = await self._cases.get_agronomist_queue()
        positions = compute_queue_positions(
            [
                QueueCase(
                    case_id=c["id"],
                    assigned_to=c.get("assigned_to") or "",
                    severity=ProblemSeverity(c["severity"]),
                    escalated_at=c["created_at"],
                )
                for c in queue
            ]
        )
        queue_position = positions.get(case["id"], 1)
        eta = estimate_eta(queue_position, evaluated_at=datetime.utcnow())

        return EscalationResponse(
            escalation_id=case["id"],
            farm_id=case["farm_id"],
            status=CaseStatus(case["status"]),
            severity=ProblemSeverity(case["severity"]),
            assigned_kvk_center=case.get("assigned_to") or DEFAULT_ASSIGNED_AGRONOMIST,
            case_summary=summary,
            spoken_summary=summary.spoken_summary,
            queue_position=queue_position,
            eta=eta,
        )


def get_escalation_service(
    case_repo: Annotated[CaseRepository, Depends(get_case_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    roster: Annotated[AgronomistRosterPort, Depends(get_roster_adapter)],
) -> EscalationService:
    return EscalationService(case_repo, farm_repo, roster)
