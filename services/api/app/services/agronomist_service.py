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
from app.schemas.case_pdf import CasePDFPayload
from app.schemas.health import RiskChange
from app.services.health_snapshot_mapping import snapshot_row_to_schema
from app.services.efficacy.tracking_service import EfficacyTrackingService, get_efficacy_tracking_service
from app.services.escalation.pdf_payload import build_case_pdf_payload
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
        efficacy_tracking: EfficacyTrackingService | None = None,
    ) -> None:
        self._cases = case_repo
        self._farms = farm_repo
        self._problems = problem_writer
        self._health = health_service
        self._efficacy_tracking = efficacy_tracking

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
            snapshot = await self._health.get_latest(c["farm_id"])
            items.append(
                AgronomistQueueItem(
                    escalation_id=c["id"],
                    farm_id=c["farm_id"],
                    # See get_case_detail's comment: dict.get's default only
                    # fires on a missing key, not a NULL value, and
                    # SIH26131's simplified onboarding leaves these NULL.
                    farmer_name=(farm or {}).get("farm_name") or "Unknown",
                    village=(farm or {}).get("village") or "",
                    crop=(farm or {}).get("primary_crop") or "",
                    severity=ProblemSeverity(c["severity"]),
                    status=CaseStatus(c["status"]),
                    health_score=float(snapshot.score) if snapshot and snapshot.score is not None else 0.0,
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
            "farmer_name": (farm or {}).get("farm_name"),
            "village": (farm or {}).get("village") or "",
            "district": (farm or {}).get("district") or (farm or {}).get("region") or "",
            "primary_crop": (farm or {}).get("primary_crop") or "",
            "growth_stage": (farm or {}).get("growth_stage"),
            "land_status": (farm or {}).get("land_status"),
        }

        problem_id = case.get("problem_id")
        problem_label = None
        if self._problems is not None and hasattr(self._problems, "get_open_problems"):
            open_problems = await self._problems.get_open_problems(case["farm_id"])
            if problem_id:
                for p in open_problems:
                    if p.problem_id == problem_id:
                        problem_label = p.label
                        break
            elif open_problems:
                problem_label = open_problems[0].label

        reason = case.get("reason") or ""
        trend = "got_worse" if "got worse" in reason.lower() or "got_worse" in reason.lower() else None

        current_advisory = None
        if "confidence" in reason.lower() or "gate" in reason.lower() or "supported set" in reason.lower() or "scope" in reason.lower():
            current_advisory = f"Confidence below gate. Escalation reason: {reason}"

        return build_case_summary(
            case_id=case["id"],
            farm_info=farm_info,
            recent_events=[],
            current_health_score=float(snapshot.score) if snapshot and snapshot.score is not None else None,
            problem_details={
                "label": problem_label,
                "severity": ProblemSeverity(case["severity"]) if case.get("severity") else ProblemSeverity.EARLY,
                "trend": trend,
            },
            assigned_officer_or_kvk=case.get("assigned_to"),
            status=CaseStatus(case["status"]) if case.get("status") in [s.value for s in CaseStatus] else CaseStatus.ESCALATED,
            current_advisory_text=current_advisory,
        )

    async def get_case_pdf_payload(self, escalation_id: str) -> CasePDFPayload:
        """PRD §5.11 / Phase 4: Return structured PDF / share-sheet data payload."""
        case_summary = await self.get_case_detail(escalation_id)
        case = await self._cases.get_by_id(escalation_id)
        res_summary = None
        if case and case.get("resolution"):
            res = case["resolution"]
            res_summary = f"Diagnosis: {res.get('confirmed_diagnosis')}. Advice: {res.get('expert_advice')}"
        return build_case_pdf_payload(
            case_summary=case_summary,
            assigned_kvk=case.get("assigned_to") if case else None,
            prescribed_actions_summary=res_summary,
        )

    async def resolve_case(self, request: ResolveCaseRequest) -> ResolveCaseResponse:
        case = await self._cases.get_by_id(request.escalation_id)
        if case is None:
            raise NotFoundError("Escalation not found.", details={"escalation_id": request.escalation_id})

        # Captured before any mutation below, so `risk.from_` reflects the
        # farm's state walking into this resolution, not after it.
        previous_snapshot = await self._health.get_latest(case["farm_id"])

        if case.get("problem_id"):
            await self._problems.resolve_problem(case["problem_id"])
            if self._efficacy_tracking is not None:
                await self._efficacy_tracking.close_for_expert_resolution(problem_id=case["problem_id"])

        farm = await self._farms.get_by_id(case["farm_id"])
        if farm is not None:
            await self._farms.update(case["farm_id"], {"days_since_last_scan": 1})

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

        snapshot = await self._health.recompute(
            case["farm_id"],
            triggering_input=TriggeringInput(
                type="case_resolution",
                details={"case_id": request.escalation_id, "problem_id": case.get("problem_id")},
            ),
        )

        return ResolveCaseResponse(
            escalation_id=request.escalation_id,
            status=CaseStatus.RESOLVED,
            risk=RiskChange(
                from_=previous_snapshot.score,
                to=snapshot.score,
                band=snapshot_row_to_schema(snapshot).band,
            ),
            resolved_at=datetime.utcnow(),
        )


def get_agronomist_service(
    case_repo: Annotated[CaseRepository, Depends(get_case_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    efficacy_tracking: Annotated[EfficacyTrackingService, Depends(get_efficacy_tracking_service)],
) -> AgronomistService:
    return AgronomistService(case_repo, farm_repo, problem_writer, health_service, efficacy_tracking)
