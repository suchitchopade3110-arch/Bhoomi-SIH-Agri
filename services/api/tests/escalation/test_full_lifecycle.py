"""End-to-end acceptance test for Phase 4: diagnose -> follow-up (Got Worse,
auto-escalate) -> resolve, walking Phase 1's exact fixture reconciliation
(82 -> 68 -> 59 -> 86) through the REAL service stack — not the domain unit
test's hand-fed inputs. Reuses the Phase 1 health engine throughout;
nothing here reimplements scoring.
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubImageDiagnosisAdapter, StubLLMAdapter
from app.core.enums import FollowupResponse, HealthBand, ProblemStatus
from app.services.diagnosis_service import DiagnosisService
from app.services.rag.retrieval import RetrievalService
from tests._stack import FARM_ID, Stack, baseline_context
from tests.rag._helpers import build_ingested_repo


@pytest.mark.asyncio
async def test_full_case_lifecycle_reconciles_phase_1_fixture_numbers():
    stack = Stack()
    repo = await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())

    diagnosis_service = DiagnosisService(
        image_port=StubImageDiagnosisAdapter(label="bacterial_leaf_blight", confidence=0.87),
        retrieval=retrieval,
        llm_port=StubLLMAdapter(),
        health_service=stack.health_service,
        problem_registry=stack.problem_registry,
        escalation_service=stack.escalation_service,
        settings=stack.settings,
    )

    # --- Establish the baseline snapshot (score 82) before anything else touches the farm ---
    baseline = await stack.health_service.get_latest(FARM_ID)
    assert baseline.score == 82
    assert baseline.band == HealthBand.GOOD.value

    # --- Day 22: diagnosis (humid conditions that favor BLB; monitoring goes stale) ---
    stack.weather.relative_humidity_pct = 92.0
    stack.context_reader.set_context(FARM_ID, baseline_context(days_since_last_scan=6))

    diagnosis = await diagnosis_service.diagnose(FARM_ID, "a_9", description_text="water soaked yellow lesions")
    assert diagnosis.above_gate is True
    assert diagnosis.health_delta_from == 82
    assert diagnosis.health_delta_to == 68

    problem_id = diagnosis.problem_id
    problem = await stack.problem_registry.get_problem(problem_id)
    assert problem is not None
    assert problem.status == ProblemStatus.OPEN

    # The diagnose flow scheduled a follow-up for this problem — find it
    # (no "pending follow-ups" endpoint exists yet to fetch it through).
    followup = next(f for f in stack.problem_registry._followups.values() if f.problem_id == problem_id)  # noqa: SLF001

    # --- Day 25: farmer reports Got Worse (same humid conditions persist) ---
    followup_outcome = await stack.followup_service.respond(
        followup.followup_id, FollowupResponse.GOT_WORSE, image_asset_id="a_15"
    )

    assert followup_outcome.severity_from == "early"
    assert followup_outcome.severity_to == "moderate"
    assert followup_outcome.health_from == 68
    assert followup_outcome.health_to == 59
    assert followup_outcome.health_band == "poor"
    assert followup_outcome.escalated is True
    assert followup_outcome.case_id is not None

    case_id = followup_outcome.case_id
    problem = await stack.problem_registry.get_problem(problem_id)
    assert problem.severity.value == "moderate"

    # --- Expert resolves the case: conditions normalize, treatment confirmed successful ---
    stack.weather.relative_humidity_pct = 80.0
    stack.context_reader.set_context(FARM_ID, baseline_context(soil_moisture_pct=60.0, days_since_last_scan=0))

    resolve_outcome = await stack.resolve_service.resolve(
        case_id,
        diagnosis="Confirmed BLB, moderate.",
        treatment="Copper-based bactericide per label; drain and dry field 48h.",
        notes="Recheck in 5 days.",
    )

    assert resolve_outcome.status == "resolved"
    assert resolve_outcome.problem_status == "resolved"
    assert resolve_outcome.health_from == 59
    assert resolve_outcome.health_to == 86
    assert resolve_outcome.health_band == "good"  # lands above the original baseline (PRD §7.4)

    problem = await stack.problem_registry.get_problem(problem_id)
    assert problem.status == ProblemStatus.RESOLVED

    # The case now carries the treatment in its record.
    case = await stack.case_repo.get_by_id(case_id)
    assert case.treatment == "Copper-based bactericide per label; drain and dry field 48h."
    assert case.diagnosis == "Confirmed BLB, moderate."
