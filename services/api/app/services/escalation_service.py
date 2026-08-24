"""Expert escalation service — compiles and routes the Farm Case Summary
(contract §2.13, PRD §5.11).
"""

from typing import Annotated

from fastapi import Depends

from app.core.enums import CaseStatus, ProblemSeverity
from app.core.errors import NotFoundError
from app.domain.escalation import build_case_summary
from app.domain.kvk_directory import DEFAULT_KVK_CENTER_ID
from app.repositories.dependencies import get_case_repository, get_farm_repository
from app.repositories.interfaces import CaseRepository, FarmRepository
from app.schemas.escalation import EscalationCreateRequest, EscalationResponse
from app.services.kvk_routing import route_to_next_available_kvk

# Fallback only for the rare case a farm has no coordinates yet (should not
# happen post-onboarding — farm creation requires latitude/longitude).
DEFAULT_ASSIGNED_AGRONOMIST = DEFAULT_KVK_CENTER_ID


class EscalationService:
    """Creates escalation Cases and compiles their CaseSummary."""

    def __init__(self, case_repo: CaseRepository, farm_repo: FarmRepository) -> None:
        self._cases = case_repo
        self._farms = farm_repo

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

        assigned_to = DEFAULT_ASSIGNED_AGRONOMIST
        if farm.get("latitude") is not None and farm.get("longitude") is not None:
            assigned_to = await route_to_next_available_kvk(self._cases, farm["latitude"], farm["longitude"])

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
        return EscalationResponse(
            escalation_id=case["id"],
            farm_id=case["farm_id"],
            status=CaseStatus(case["status"]),
            severity=ProblemSeverity(case["severity"]),
            assigned_kvk_center=case.get("assigned_to") or DEFAULT_ASSIGNED_AGRONOMIST,
            case_summary=summary,
            spoken_summary=summary.spoken_summary,
        )


def get_escalation_service(
    case_repo: Annotated[CaseRepository, Depends(get_case_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> EscalationService:
    return EscalationService(case_repo, farm_repo)
