"""Orchestrates POST /cases/{case_id}/resolve (contract §2.13): an expert
diagnosis/treatment clears the problem, lifts the monitoring + treatment
sub-indices, and triggers a Phase 1 recompute — the score must recover
above baseline (PRD §7.4). No scoring logic lives here — see
``domain.health.compute_health`` (Phase 1), reused unchanged via
``HealthService`` (Phase 4 item 5).
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from app.core.enums import CaseStatus
from app.core.errors import NotFoundError
from app.domain.health.inputs import TriggeringInput
from app.models.health_snapshot import HealthSnapshot
from app.repositories.case_repository import CaseRepository
from app.repositories.dependencies import (
    get_escalation_case_repository,
    get_farm_health_context_writer,
    get_problem_writer,
    get_treatment_trend_writer,
)
from app.repositories.health_context import FarmHealthContextWriter, ProblemWriter, TreatmentTrendWriter
from app.services.health_service import HealthService, get_health_service

RESOLUTION_TRIGGER_TYPE = "case_resolution"


@dataclass(frozen=True)
class CaseResolution:
    """Result of resolving one case — its new status plus the recovered
    health snapshot."""

    case_id: str
    status: CaseStatus
    snapshot: HealthSnapshot


class ResolveService:
    """Applies an agronomist's confirmed resolution to a case and its farm."""

    def __init__(
        self,
        case_repo: CaseRepository,
        problem_writer: ProblemWriter,
        treatment_writer: TreatmentTrendWriter,
        context_writer: FarmHealthContextWriter,
        health_service: HealthService,
    ) -> None:
        self._cases = case_repo
        self._problem_writer = problem_writer
        self._treatment_writer = treatment_writer
        self._context_writer = context_writer
        self._health = health_service

    async def resolve(
        self,
        case_id: str,
        agronomist_id: str,
        agronomist_name: str,
        confirmed_diagnosis: str,
        expert_advice: str,
        prescribed_inputs: list[str] | None = None,
    ) -> CaseResolution:
        """Resolve ``case_id`` (PRD §7.4).

        Clears the case's problem (``active_problem_load`` -> 100), marks
        the follow-up trend as a confirmed resolution (``treatment_response``
        -> its maximum), touches monitoring recency, and recomputes — the
        recovered score reflects a farm that is "now well-monitored with a
        logged, successful treatment," not merely a problem removed.

        Args:
            case_id: UUID string of the case to resolve.
            agronomist_id: UUID string of the resolving agronomist.
            agronomist_name: Display name, stored on the resolution record.
            confirmed_diagnosis: Agronomist-validated diagnosis.
            expert_advice: Actionable prescription for the farmer.
            prescribed_inputs: Optional list of prescribed inputs.

        Returns:
            A ``CaseResolution`` with the recovered health snapshot.

        Raises:
            NotFoundError: No case with ``case_id`` exists.
        """
        case = await self._cases.get_by_id(case_id)
        if case is None:
            raise NotFoundError(message=f"No case {case_id!r} found.")

        if case.problem_id is not None:
            await self._problem_writer.resolve_problem(case.farm_id, case.problem_id)
        await self._treatment_writer.record_confirmed_resolution(case.farm_id)
        await self._context_writer.touch_last_scan(case.farm_id)

        snapshot = await self._health.recompute(
            case.farm_id,
            triggering_input=TriggeringInput(
                type=RESOLUTION_TRIGGER_TYPE, details={"problem_id": case.problem_id, "case_id": case_id}
            ),
        )

        case.status = CaseStatus.RESOLVED.value
        case.resolution = {
            "agronomist_id": agronomist_id,
            "agronomist_name": agronomist_name,
            "confirmed_diagnosis": confirmed_diagnosis,
            "expert_advice": expert_advice,
            "prescribed_inputs": prescribed_inputs or [],
        }
        case = await self._cases.update(case)

        return CaseResolution(case_id=case.id, status=CaseStatus.RESOLVED, snapshot=snapshot)


def get_resolve_service(
    case_repo: Annotated[CaseRepository, Depends(get_escalation_case_repository)],
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    treatment_writer: Annotated[TreatmentTrendWriter, Depends(get_treatment_trend_writer)],
    context_writer: Annotated[FarmHealthContextWriter, Depends(get_farm_health_context_writer)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> ResolveService:
    """FastAPI dependency provider assembling ``ResolveService`` from its ports."""
    return ResolveService(case_repo, problem_writer, treatment_writer, context_writer, health_service)
