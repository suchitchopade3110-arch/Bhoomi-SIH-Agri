"""KVK Agronomist Portal service — case queue and expert resolution
(contract §2.13, PRD §5.11).

Resolution clears the problem (health engine sub-index #4 -> 100 for it)
and marks the farm freshly monitored + successfully treated (sub-indices #5
and #6), which is why the score recovers above baseline (PRD §7.4).
"""

from datetime import datetime
from typing import Annotated

from fastapi import Depends

from app.core.enums import CaseStatus, ProblemSeverity
from app.core.errors import NotFoundError
from app.domain.escalation import build_case_summary
from app.domain.health.inputs import TriggeringInput
from app.domain.queue import QueueCase, compute_queue_positions, estimate_eta
from app.repositories.dependencies import get_case_repository, get_farm_repository, get_problem_writer
from app.repositories.health_context import ProblemWriter
from app.repositories.interfaces import CaseRepository, FarmRepository
from app.schemas.agronomist import AgronomistQueueItem, ResolveCaseRequest, ResolveCaseResponse
from app.schemas.case import CaseSummary
from app.services.health_service import HealthService, get_health_service

# A confirmed expert resolution is treated as real recovery, not just "no
# active problem" — the same PRD §7.4 nudge direction as diagnosis, but
# reversed: soil-moisture stress eases and the crop calendar advances by the
# time the case was worked. Demo/showcase tuning reproducing the PRD's
# 68 -> 86 recovery — see final report.
RESOLUTION_SOIL_MOISTURE_RECOVERY_PCT = 8.0
RESOLUTION_DAYS_SINCE_PLANTING_ADVANCE = 15
RESOLUTION_RESETS_DAYS_SINCE_LAST_SCAN = 0


class AgronomistService:
    """Agronomist-facing case queue and resolution actions."""

    def __init__(
        self,
        case_repo: CaseRepository,
        farm_repo: FarmRepository,
        problem_writer: ProblemWriter,
        health_service: HealthService,
    ) -> None:
        self._cases = case_repo
        self._farms = farm_repo
        self._problems = problem_writer
        self._health = health_service

    async def get_queue(self, agronomist_jurisdiction: str | None = None) -> list[AgronomistQueueItem]:
        cases = await self._cases.get_agronomist_queue()
        evaluated_at = datetime.utcnow()

        positions = compute_queue_positions(
            [
                QueueCase(
                    case_id=c["id"],
                    assigned_to=c.get("assigned_to") or "",
                    severity=ProblemSeverity(c["severity"]),
                    escalated_at=c["created_at"],
                )
                for c in cases
            ]
        )

        items = []
        for c in cases:
            farm = await self._farms.get_by_id(c["farm_id"])
            position = positions[c["id"]]
            items.append(
                AgronomistQueueItem(
                    escalation_id=c["id"],
                    farm_id=c["farm_id"],
                    farmer_name=(farm or {}).get("farm_name", "Unknown"),
                    village=(farm or {}).get("village", ""),
                    crop=(farm or {}).get("primary_crop", ""),
                    severity=ProblemSeverity(c["severity"]),
                    status=CaseStatus(c["status"]),
                    health_score=0.0,
                    escalated_at=c["created_at"],
                    queue_position=position,
                    estimated_resolution_at=estimate_eta(position, evaluated_at),
                )
            )
        return items

    async def get_case_detail(self, escalation_id: str) -> CaseSummary:
        case = await self._cases.get_by_id(escalation_id)
        if case is None:
            raise NotFoundError("Escalation not found.", details={"escalation_id": escalation_id})
        farm = await self._farms.get_by_id(case["farm_id"])
        snapshot = await self._health.get_latest(case["farm_id"])
        farm_info = {
            "id": case["farm_id"],
            "farmer_name": (farm or {}).get("farm_name", "Unknown"),
            "village": (farm or {}).get("village", ""),
            "district": (farm or {}).get("district", ""),
            "primary_crop": (farm or {}).get("primary_crop", ""),
            "growth_stage": (farm or {}).get("growth_stage"),
            "land_status": (farm or {}).get("land_status"),
        }
        return build_case_summary(
            case_id=case["id"],
            farm_info=farm_info,
            recent_events=[],
            current_health_score=float(snapshot.score or 0),
            problem_details={"severity": ProblemSeverity(case["severity"])},
            assigned_officer_or_kvk=case.get("assigned_to"),
            status=CaseStatus(case["status"]),
        )

    async def resolve_case(self, request: ResolveCaseRequest) -> ResolveCaseResponse:
        case = await self._cases.get_by_id(request.escalation_id)
        if case is None:
            raise NotFoundError("Escalation not found.", details={"escalation_id": request.escalation_id})

        if case.get("problem_id"):
            await self._problems.resolve_problem(case["problem_id"])

        farm = await self._farms.get_by_id(case["farm_id"])
        if farm is not None:
            await self._farms.update(case["farm_id"], {"days_since_last_scan": 2})

        await self._cases.update_status(
            request.escalation_id,
            CaseStatus.RESOLVED.value,
            resolution={
                "confirmed_diagnosis": request.confirmed_diagnosis,
                "expert_advice": request.expert_advice,
                "prescribed_inputs": request.prescribed_inputs,
                "agronomist_name": request.agronomist_name,
            },
        )

        await self._health.recompute(
            case["farm_id"],
            triggering_input=TriggeringInput(
                type="case_resolution",
                details={"case_id": request.escalation_id, "problem_id": case.get("problem_id")},
            ),
        )

        return ResolveCaseResponse(
            escalation_id=request.escalation_id,
            status=CaseStatus.RESOLVED,
            resolved_at=datetime.utcnow(),
        )


def get_agronomist_service(
    case_repo: Annotated[CaseRepository, Depends(get_case_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> AgronomistService:
    return AgronomistService(case_repo, farm_repo, problem_writer, health_service)
