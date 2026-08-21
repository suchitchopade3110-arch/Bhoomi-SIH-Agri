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

from app.core.enums import CaseStatus, HealthBand, ProblemStatus
from app.core.errors import NotFoundError
from app.domain.health.inputs import TriggeringInput
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
    """Result of resolving one case — mirrors contract §2.13's
    ``POST /cases/{id}/resolve`` response exactly."""

    case_id: str
    status: CaseStatus
    problem_status: ProblemStatus
    health_from: int | None
    health_to: int | None
    health_band: HealthBand


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

    async def resolve(self, case_id: str, diagnosis: str, treatment: str, notes: str | None = None) -> CaseResolution:
        """Resolve ``case_id`` (PRD §7.4, contract §2.13).

        Clears the case's problem (``active_problem_load`` -> 100), marks
        the follow-up trend as a confirmed resolution (``treatment_response``
        -> its maximum), touches monitoring recency, and recomputes — the
        recovered score reflects a farm that is "now well-monitored with a
        logged, successful treatment," not merely a problem removed.

        Args:
            case_id: UUID string of the case to resolve.
            diagnosis: Agronomist-confirmed diagnosis.
            treatment: Prescribed treatment.
            notes: Optional follow-up guidance.

        Returns:
            A ``CaseResolution`` with the recovered health movement.

        Raises:
            NotFoundError: No case with ``case_id`` exists.
        """
        case = await self._cases.get_by_id(case_id)
        if case is None:
            raise NotFoundError(message=f"No case {case_id!r} found.")

        before_snapshot = await self._health.get_latest(case.farm_id)

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
        case.resolution = {"diagnosis": diagnosis, "treatment": treatment, "notes": notes}
        case = await self._cases.update(case)

        return CaseResolution(
            case_id=case.id,
            status=CaseStatus.RESOLVED,
            problem_status=ProblemStatus.RESOLVED,
            health_from=before_snapshot.score,
            health_to=snapshot.score,
            health_band=HealthBand(snapshot.band),
        )


def get_resolve_service(
    case_repo: Annotated[CaseRepository, Depends(get_escalation_case_repository)],
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    treatment_writer: Annotated[TreatmentTrendWriter, Depends(get_treatment_trend_writer)],
    context_writer: Annotated[FarmHealthContextWriter, Depends(get_farm_health_context_writer)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> ResolveService:
    """FastAPI dependency provider assembling ``ResolveService`` from its ports."""
    return ResolveService(case_repo, problem_writer, treatment_writer, context_writer, health_service)
