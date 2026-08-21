"""Shared offline test fakes for the escalation subsystem — Postgres-free
``CaseRepository``/``AgronomistDirectory`` stand-ins with the same async
method surface as the real ones (same pattern as
``tests/rag/test_diagnosis_service.py``'s ``_FakeHealthSnapshotRepo``), so
tests exercise identical service code paths, offline and deterministic.
"""

import uuid
from datetime import datetime

from app.core.config import Settings
from app.models.case import Case
from app.repositories.agronomist_repository import AgronomistRecord
from app.repositories.health_context import (
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
)
from app.services.escalation.case_compiler import CaseSummaryCompiler
from app.services.escalation.escalation_service import EscalationService
from app.services.escalation.followup_service import FollowupService
from app.services.escalation.resolve_service import ResolveService
from app.services.escalation.routing import AgronomistRouter
from app.services.health_service import HealthService

DEMO_AGRONOMIST = AgronomistRecord(
    id="agro_demo", name="Dr. Meena Krishnan", kvk_center="TNAU KVK - Madurai", district="Madurai"
)


class FakeCaseRepository:
    def __init__(self) -> None:
        self._rows: dict[str, Case] = {}

    async def save(self, case: Case) -> Case:
        case.id = case.id or str(uuid.uuid4())
        case.created_at = case.created_at or datetime.utcnow()
        case.updated_at = case.updated_at or case.created_at
        self._rows[case.id] = case
        return case

    async def get_by_id(self, case_id: str) -> Case | None:
        return self._rows.get(case_id)

    async def get_queue(self, status: str | None = None) -> list[Case]:
        rows = list(self._rows.values())
        if status is not None:
            rows = [r for r in rows if r.status == status]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)

    async def update(self, case: Case) -> Case:
        self._rows[case.id] = case
        return case


class FakeAgronomistDirectory:
    def __init__(self, agronomists: list[AgronomistRecord] | None = None) -> None:
        self._agronomists = agronomists if agronomists is not None else [DEMO_AGRONOMIST]

    async def get_by_name(self, name: str) -> AgronomistRecord | None:
        return next((a for a in self._agronomists if a.name == name), None)

    async def find_available_in_district(self, district: str) -> AgronomistRecord | None:
        return next((a for a in self._agronomists if a.district == district), None)

    async def find_any_available(self) -> AgronomistRecord | None:
        return self._agronomists[0] if self._agronomists else None


def build_escalation_service(
    farm_repo,
    user_repo,
    health_service: HealthService,
    problem_reader: InMemoryProblemLoadReader,
    treatment_reader: InMemoryTreatmentTrendReader,
    settings: Settings | None = None,
    case_repo: FakeCaseRepository | None = None,
    directory: FakeAgronomistDirectory | None = None,
) -> EscalationService:
    """Wires a fully-offline ``EscalationService`` for tests — same
    compiler/router wiring as ``get_escalation_service``, backed by fakes."""
    settings = settings or Settings(AGRONOMIST_ROUTING_MODE="demo_fixed", DEMO_AGRONOMIST_NAME=DEMO_AGRONOMIST.name)
    case_repo = case_repo if case_repo is not None else FakeCaseRepository()
    directory = directory if directory is not None else FakeAgronomistDirectory()
    compiler = CaseSummaryCompiler(farm_repo, health_service, problem_reader, treatment_reader)
    router = AgronomistRouter(directory, settings)
    return EscalationService(case_repo, farm_repo, user_repo, compiler, router)


def build_followup_service(
    problem_reader: InMemoryProblemLoadReader,
    treatment_reader: InMemoryTreatmentTrendReader,
    context_reader: InMemoryFarmHealthContextReader,
    health_service: HealthService,
    escalation_service: EscalationService,
) -> FollowupService:
    return FollowupService(
        problem_reader=problem_reader,
        problem_writer=problem_reader,
        treatment_writer=treatment_reader,
        context_writer=context_reader,
        health_service=health_service,
        escalation_service=escalation_service,
    )


def build_resolve_service(
    case_repo: FakeCaseRepository,
    problem_reader: InMemoryProblemLoadReader,
    treatment_reader: InMemoryTreatmentTrendReader,
    context_reader: InMemoryFarmHealthContextReader,
    health_service: HealthService,
) -> ResolveService:
    return ResolveService(
        case_repo=case_repo,
        problem_writer=problem_reader,
        treatment_writer=treatment_reader,
        context_writer=context_reader,
        health_service=health_service,
    )
