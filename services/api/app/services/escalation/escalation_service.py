"""Orchestrates escalation creation — the shared entrypoint every trigger
(Phase 4 item 1: below-gate/out-of-scope diagnosis, no-retrieval diagnosis,
a got_worse follow-up, and the manual ``POST /problems/{id}/escalate``)
routes through: compile a CaseSummary, assign the nearest available
agronomist, and persist the case. No compiling/routing logic lives here —
see ``case_compiler.CaseSummaryCompiler`` and ``routing.AgronomistRouter``.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated
from uuid import uuid4

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.enums import CaseStatus, ProblemSeverity
from app.core.errors import NotFoundError
from app.models.case import Case
from app.repositories.agronomist_repository import AgronomistDirectory
from app.repositories.case_repository import CaseRepository
from app.repositories.dependencies import (
    get_agronomist_directory,
    get_escalation_case_repository,
    get_farm_repository,
    get_problem_load_reader,
    get_treatment_trend_reader,
    get_user_repository,
)
from app.repositories.health_context import ProblemLoadReader, TreatmentTrendReader
from app.repositories.interfaces import FarmRepository, UserRepository
from app.schemas.agronomist import AgronomistQueueItem
from app.schemas.case import CaseSummary
from app.services.escalation.case_compiler import CaseSummaryCompiler
from app.services.escalation.routing import AgronomistRouter
from app.services.health_service import HealthService, get_health_service


@dataclass(frozen=True)
class EscalationResult:
    """Result of creating one escalation — everything a caller (a router, or
    another service triggering an escalation) needs to respond."""

    case_id: str
    farm_id: str
    status: CaseStatus
    severity: ProblemSeverity
    assigned_to: str
    assigned_kvk_center: str
    case_summary: CaseSummary
    created_at: datetime


class EscalationService:
    """Compiles and routes new cases; reads existing ones back."""

    def __init__(
        self,
        case_repo: CaseRepository,
        farm_repo: FarmRepository,
        compiler: CaseSummaryCompiler,
        router: AgronomistRouter,
    ) -> None:
        self._cases = case_repo
        self._farms = farm_repo
        self._compiler = compiler
        self._router = router

    async def create_escalation(
        self,
        farm_id: str,
        trigger_type: str,
        reason: str,
        severity: ProblemSeverity = ProblemSeverity.EARLY,
        problem_id: str | None = None,
        notes: str | None = None,
        latest_images: list[str] | None = None,
    ) -> EscalationResult:
        """Compile a Living Case Summary and route it — the single entrypoint
        every escalation trigger shares (Phase 4 item 1).

        Args:
            farm_id: UUID string of the escalating farm.
            trigger_type: What triggered this ("below_confidence_gate",
                "out_of_scope", "no_relevant_source", "got_worse_followup",
                or "manual").
            reason: Human-readable trigger reason, stored verbatim.
            severity: Assessed problem severity.
            problem_id: The open problem this case is about, if any.
            notes: Optional extra context folded into the case summary.
            latest_images: Presigned URLs / asset IDs of relevant photos.

        Returns:
            An ``EscalationResult`` with the persisted case's id and its
            complete, non-empty ``CaseSummary``.
        """
        farm = await self._farms.get_by_id(farm_id) or {}
        assigned = await self._router.assign(farm.get("district"))

        case_id = str(uuid4())
        summary = await self._compiler.compile(
            case_id=case_id,
            farm_id=farm_id,
            problem_summary=notes or reason,
            severity=severity,
            status=CaseStatus.ESCALATED,
            latest_images=latest_images or [],
            escalated_to=assigned.name,
        )

        case = Case(
            id=case_id,
            farm_id=farm_id,
            problem_id=problem_id,
            trigger_type=trigger_type,
            reason=reason,
            severity=severity.value,
            status=CaseStatus.ESCALATED.value,
            case_summary=summary.model_dump(mode="json"),
            assigned_to=assigned.agronomist_id,
            assigned_kvk_center=assigned.kvk_center,
        )
        saved = await self._cases.save(case)

        return EscalationResult(
            case_id=saved.id,
            farm_id=farm_id,
            status=CaseStatus.ESCALATED,
            severity=severity,
            assigned_to=assigned.name,
            assigned_kvk_center=assigned.kvk_center,
            case_summary=summary,
            created_at=saved.created_at,
        )

    async def get_case(self, case_id: str) -> CaseSummary:
        """The complete Living Case Summary for one case (contract §2.13)."""
        case = await self._cases.get_by_id(case_id)
        if case is None:
            raise NotFoundError(message=f"No case {case_id!r} found.")
        return CaseSummary(**case.case_summary)

    async def get_queue(self, status: CaseStatus | None = None) -> list[AgronomistQueueItem]:
        """The agronomist case queue, optionally filtered by status."""
        rows = await self._cases.get_queue(status.value if status else None)
        return [
            AgronomistQueueItem(
                escalation_id=row.id,
                farm_id=row.farm_id,
                farmer_name=row.case_summary.get("farmer_name", "Unknown Farmer"),
                village=row.case_summary.get("village", "Unknown"),
                crop=row.case_summary.get("crop", "Unknown crop"),
                severity=ProblemSeverity(row.severity),
                status=CaseStatus(row.status),
                health_score=row.case_summary.get("health_score", 0.0),
                escalated_at=row.created_at,
            )
            for row in rows
        ]


def get_escalation_service(
    case_repo: Annotated[CaseRepository, Depends(get_escalation_case_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    problem_reader: Annotated[ProblemLoadReader, Depends(get_problem_load_reader)],
    treatment_reader: Annotated[TreatmentTrendReader, Depends(get_treatment_trend_reader)],
    agronomist_directory: Annotated[AgronomistDirectory, Depends(get_agronomist_directory)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> EscalationService:
    """FastAPI dependency provider assembling ``EscalationService`` from its
    compiler + router + repositories."""
    compiler = CaseSummaryCompiler(farm_repo, user_repo, health_service, problem_reader, treatment_reader)
    router = AgronomistRouter(agronomist_directory, settings)
    return EscalationService(case_repo, farm_repo, compiler, router)
