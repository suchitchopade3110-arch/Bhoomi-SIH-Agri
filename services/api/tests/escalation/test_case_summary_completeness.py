"""Required acceptance tests (execution plan): every escalation yields a
complete, non-empty CaseSummary with all contract §2.13 fields, and the
Got Worse -> escalate follow-up path returns a case_id.
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubImageDiagnosisAdapter, StubLLMAdapter
from app.core.enums import FollowupResponse
from app.services.diagnosis_service import DiagnosisService
from app.services.rag.retrieval import RetrievalService
from tests._stack import FARM_ID, Stack
from tests.rag._helpers import build_ingested_repo

CONTRACT_CASE_SUMMARY_FIELDS = (
    "case_id",
    "farm",
    "problem",
    "timeline",
    "images",
    "treatments_tried",
    "followup_trend",
    "current_health",
    "status",
)


def _assert_complete_case_summary(summary: dict) -> None:
    for field in CONTRACT_CASE_SUMMARY_FIELDS:
        assert field in summary, f"CaseSummary missing contract field: {field}"
    assert summary["case_id"]
    assert summary["farm"]["id"]
    assert summary["current_health"] is not None
    assert isinstance(summary["timeline"], list)
    assert isinstance(summary["images"], list)
    assert isinstance(summary["treatments_tried"], list)
    assert summary["status"] in {"open", "assigned", "resolved"}


async def _make_diagnosis_service(image_confidence: float, image_label: str, stack: Stack) -> DiagnosisService:
    repo = await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    return DiagnosisService(
        image_port=StubImageDiagnosisAdapter(label=image_label, confidence=image_confidence),
        retrieval=retrieval,
        llm_port=StubLLMAdapter(),
        health_service=stack.health_service,
        problem_registry=stack.problem_registry,
        escalation_service=stack.escalation_service,
        settings=stack.settings,
    )


@pytest.mark.asyncio
async def test_below_gate_diagnosis_yields_a_complete_case_summary_with_no_problem_yet():
    stack = Stack()
    service = await _make_diagnosis_service(image_confidence=0.10, image_label="bacterial_leaf_blight", stack=stack)

    outcome = await service.diagnose(FARM_ID, "a_9")
    case = await stack.case_repo.get_by_id(outcome.escalation.case_id)

    _assert_complete_case_summary(case.summary)
    assert case.summary["problem"] is None  # no problem was ever confirmed


@pytest.mark.asyncio
async def test_out_of_scope_diagnosis_yields_a_complete_case_summary():
    stack = Stack()
    service = await _make_diagnosis_service(image_confidence=0.95, image_label="tomato_yellow_leaf_curl", stack=stack)

    outcome = await service.diagnose(FARM_ID, "a_9")
    case = await stack.case_repo.get_by_id(outcome.escalation.case_id)

    _assert_complete_case_summary(case.summary)


@pytest.mark.asyncio
async def test_no_relevant_source_diagnosis_yields_a_complete_case_summary():
    stack = Stack()
    empty_repo = await build_ingested_repo(docs=[])
    retrieval = RetrievalService(empty_repo, StubEmbeddingAdapter())
    service = DiagnosisService(
        image_port=StubImageDiagnosisAdapter(label="bacterial_leaf_blight", confidence=0.95),
        retrieval=retrieval,
        llm_port=StubLLMAdapter(),
        health_service=stack.health_service,
        problem_registry=stack.problem_registry,
        escalation_service=stack.escalation_service,
        settings=stack.settings,
    )

    outcome = await service.diagnose(FARM_ID, "a_9")
    case = await stack.case_repo.get_by_id(outcome.escalation.case_id)

    _assert_complete_case_summary(case.summary)
    assert case.trigger == "no_relevant_source"


@pytest.mark.asyncio
async def test_got_worse_followup_yields_a_complete_case_summary_and_a_case_id():
    stack = Stack()
    service = await _make_diagnosis_service(image_confidence=0.87, image_label="bacterial_leaf_blight", stack=stack)

    await stack.health_service.get_latest(FARM_ID)  # establish baseline before diagnosing
    diagnosis = await service.diagnose(FARM_ID, "a_9")
    assert diagnosis.above_gate is True

    followup = next(
        f for f in stack.problem_registry._followups.values() if f.problem_id == diagnosis.problem_id  # noqa: SLF001
    )
    outcome = await stack.followup_service.respond(followup.followup_id, FollowupResponse.GOT_WORSE, None)

    assert outcome.escalated is True
    assert outcome.case_id is not None

    case = await stack.case_repo.get_by_id(outcome.case_id)
    _assert_complete_case_summary(case.summary)
    assert case.summary["problem"]["id"] == diagnosis.problem_id
    assert case.summary["problem"]["severity"] == "moderate"
    assert case.trigger == "got_worse"


@pytest.mark.asyncio
async def test_improved_followup_does_not_escalate_and_has_no_case_id():
    stack = Stack()
    service = await _make_diagnosis_service(image_confidence=0.87, image_label="bacterial_leaf_blight", stack=stack)

    await stack.health_service.get_latest(FARM_ID)
    diagnosis = await service.diagnose(FARM_ID, "a_9")
    followup = next(
        f for f in stack.problem_registry._followups.values() if f.problem_id == diagnosis.problem_id  # noqa: SLF001
    )

    outcome = await stack.followup_service.respond(followup.followup_id, FollowupResponse.IMPROVED, None)

    assert outcome.escalated is False
    assert outcome.case_id is None
    assert outcome.severity_from == "early"
    assert outcome.severity_to == "early"  # already at the lightest tier, demotion is a no-op
