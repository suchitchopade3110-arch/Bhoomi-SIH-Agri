"""Tests for DiagnosisService — POST /farms/{id}/diagnose's orchestration
(contract §2.10): image confidence + retrieval combined into the gate, then
compose (with health_delta) or escalate. All offline and deterministic.
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubImageDiagnosisAdapter, StubLLMAdapter
from app.services.diagnosis_service import DiagnosisService
from app.services.rag.retrieval import RetrievalService
from tests._stack import FARM_ID, Stack
from tests.rag._helpers import build_ingested_repo


async def _make_service(image_confidence: float = 0.87, image_label: str = "bacterial_leaf_blight", repo=None):
    stack = Stack()
    repo = repo if repo is not None else await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    image_port = StubImageDiagnosisAdapter(label=image_label, confidence=image_confidence)
    service = DiagnosisService(
        image_port=image_port,
        retrieval=retrieval,
        llm_port=StubLLMAdapter(),
        health_service=stack.health_service,
        problem_registry=stack.problem_registry,
        escalation_service=stack.escalation_service,
        settings=stack.settings,
    )
    return service, stack


@pytest.mark.asyncio
async def test_above_gate_composes_advisory_with_citation_and_health_delta():
    service, _ = await _make_service(image_confidence=0.87, image_label="bacterial_leaf_blight")
    outcome = await service.diagnose(FARM_ID, "a_9", description_text="yellow water soaked lesions")

    assert outcome.above_gate is True
    assert outcome.reason is None
    assert outcome.escalation is None
    assert outcome.problem_id is not None
    assert outcome.label == "bacterial_leaf_blight"
    assert outcome.stage == "early"
    assert outcome.advisory is not None
    assert len(outcome.citations) >= 1
    assert outcome.health_delta_from == 82  # the baseline fixture's known score
    assert outcome.health_delta_to is not None
    assert outcome.health_delta_to < outcome.health_delta_from  # a new problem must lower the score


@pytest.mark.asyncio
async def test_below_image_confidence_escalates_without_advisory_or_problem():
    service, _ = await _make_service(image_confidence=0.10, image_label="bacterial_leaf_blight")
    outcome = await service.diagnose(FARM_ID, "a_9")

    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.problem_id is None
    assert outcome.health_delta_from is None
    assert outcome.health_delta_to is None
    assert "0.10" in outcome.reason
    assert outcome.escalation is not None
    assert outcome.escalation.case_id
    assert outcome.escalation.assigned_to


@pytest.mark.asyncio
async def test_out_of_scope_label_escalates_even_with_high_confidence():
    service, _ = await _make_service(image_confidence=0.99, image_label="tomato_yellow_leaf_curl")
    outcome = await service.diagnose(FARM_ID, "a_9")

    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert "supported set" in outcome.reason


@pytest.mark.asyncio
async def test_empty_corpus_escalates_even_with_confident_in_scope_diagnosis():
    empty_repo = await build_ingested_repo(docs=[])
    service, _ = await _make_service(image_confidence=0.95, image_label="bacterial_leaf_blight", repo=empty_repo)
    outcome = await service.diagnose(FARM_ID, "a_9")

    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert outcome.citations == []


@pytest.mark.asyncio
async def test_escalation_never_carries_advisory_and_compose_never_carries_reason():
    """Structural invariant: exactly one branch populated, never a mix."""
    composed_service, _ = await _make_service(image_confidence=0.90)
    composed = await composed_service.diagnose(FARM_ID, "a_9")
    assert composed.above_gate and composed.advisory is not None and composed.reason is None and composed.escalation is None

    escalated_service, _ = await _make_service(image_confidence=0.10)
    escalated = await escalated_service.diagnose(FARM_ID, "a_9")
    assert not escalated.above_gate and escalated.advisory is None and escalated.reason is not None and escalated.escalation is not None


@pytest.mark.asyncio
async def test_below_gate_diagnosis_opens_a_case_with_compiled_summary():
    """The escalate branch now routes through the shared EscalationService —
    the case it opens must carry a fully compiled CaseSummary, not a bare id."""
    service, stack = await _make_service(image_confidence=0.10)
    outcome = await service.diagnose(FARM_ID, "a_9")

    case = await stack.case_repo.get_by_id(outcome.escalation.case_id)
    assert case is not None
    assert case.status == "assigned"
    assert case.trigger == "below_gate"
    assert case.summary  # a non-empty compiled CaseSummary was attached
    assert case.summary["case_id"] == case.id
