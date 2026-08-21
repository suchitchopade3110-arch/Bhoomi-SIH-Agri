"""Orchestrates POST /farms/{id}/diagnose (contract §2.10): image diagnosis
+ retrieval combined into the confidence gate, then compose (grounded
5-point advisory + health_delta) or escalate. No decision logic lives here —
the gate call is domain.gate.decide, output validation is
domain.rag.parse_advisory_output, scoring is Phase-1's HealthService, and
(Phase 4) escalation/case compilation is services.escalation.EscalationService.
"""

from dataclasses import dataclass
from typing import Annotated
from uuid import uuid4

from fastapi import Depends

from app.adapters.dependencies import get_image_diagnosis_adapter, get_llm_adapter
from app.adapters.ports import ImageDiagnosisPort, LLMPort
from app.core.config import Settings, get_settings
from app.core.enums import ProblemSeverity
from app.domain.gate import GateDecision, decide
from app.domain.health.inputs import TriggeringInput
from app.domain.rag import FivePointAdvisory, GroundedCitation, parse_advisory_output
from app.models.health_snapshot import HealthSnapshot
from app.repositories.dependencies import get_problem_registry
from app.repositories.interfaces import RetrievedChunk
from app.repositories.problem_registry import Problem, ProblemRegistry
from app.services.escalation.escalation_service import EscalationService, get_escalation_service
from app.services.gate_service import SUPPORTED_DIAGNOSIS_LABELS
from app.services.health_service import HealthService, get_health_service
from app.services.rag.retrieval import RetrievalService, get_retrieval_service

# A fresh diagnosis has no follow-up history yet, so it always starts at the
# lightest severity tier — later follow-ups (Phase 4's severity promotion,
# PRD §5.10) move it from there.
INITIAL_PROBLEM_SEVERITY = ProblemSeverity.EARLY

ESCALATE_SPOKEN_SUMMARY_FALLBACK = "I'm not sure — I've sent this to an expert."
COMPOSED_SPOKEN_SUMMARY = "Here's what I found, with sources."


@dataclass(frozen=True)
class DiagnoseEscalation:
    case_id: str
    assigned_to: str


@dataclass(frozen=True)
class DiagnoseOutcome:
    """Result of one diagnose call — exactly one of the two contract §2.10
    response shapes, never a mix."""

    above_gate: bool
    problem_id: str | None
    label: str | None
    stage: str | None
    confidence: float | None
    advisory: FivePointAdvisory | None
    citations: list[GroundedCitation]
    health_delta_from: int | None
    health_delta_to: int | None
    reason: str | None
    escalation: DiagnoseEscalation | None
    spoken_summary: str


def _chunk_to_dict(chunk: RetrievedChunk) -> dict:
    return {
        "doc_id": chunk.doc_id,
        "title": chunk.title,
        "reviewed_on": chunk.reviewed_on,
        "chunk_text": chunk.chunk_text,
    }


def _trigger_from_gate_decision(decision: GateDecision) -> str:
    """Categorize *which* gate check failed for the Case's ``trigger`` field
    (execution plan item 1). The gate's ``error_code`` alone can't
    distinguish below-gate-confidence from out-of-scope — both map to
    ``BELOW_CONFIDENCE_GATE`` (see domain/gate/constants.py) — so this reads
    the reason text domain.gate.decide already produces."""
    if decision.error_code == "NO_RELEVANT_SOURCE":
        return "no_relevant_source"
    if decision.reason and "supported set" in decision.reason:
        return "out_of_scope"
    return "below_gate"


class DiagnosisService:
    """Combines image diagnosis + RAG retrieval into the confidence gate,
    then composes a grounded advisory or escalates (PRD §5.6, §5.7)."""

    def __init__(
        self,
        image_port: ImageDiagnosisPort,
        retrieval: RetrievalService,
        llm_port: LLMPort,
        health_service: HealthService,
        problem_registry: ProblemRegistry,
        escalation_service: EscalationService,
        settings: Settings,
    ) -> None:
        self._image_port = image_port
        self._retrieval = retrieval
        self._llm = llm_port
        self._health = health_service
        self._problems = problem_registry
        self._escalation = escalation_service
        self._settings = settings

    async def diagnose(
        self,
        farm_id: str,
        image_asset_id: str,
        description_text: str | None = None,
    ) -> DiagnoseOutcome:
        """Run the full gated diagnosis flow for one photo (+ optional text).

        Args:
            farm_id: UUID string of the farm.
            image_asset_id: The uploaded disease photo's asset reference.
            description_text: Optional farmer-provided symptom text (from a
                prior voice transcription or typed note) to enrich the
                retrieval query.

        Returns:
            A ``DiagnoseOutcome``: either a composed, cited advisory with
            its health_delta, or an honest escalation. Never both.
        """
        label, confidence, _meta = await self._image_port.diagnose_crop_image(image_asset_id)
        in_scope = label in SUPPORTED_DIAGNOSIS_LABELS

        query = f"{label.replace('_', ' ')} {description_text or ''}".strip()
        chunks = await self._retrieval.retrieve(query)
        top_relevance = RetrievalService.top_relevance(chunks)

        decision = decide(
            image_confidence=confidence,
            in_scope=in_scope,
            retrieval_relevance=top_relevance,
            confidence_gate=self._settings.CONFIDENCE_GATE,
            relevance_threshold=self._settings.RAG_RELEVANCE_THRESHOLD,
        )

        if decision.should_escalate:
            escalation = await self._escalate(farm_id, None, decision.reason, _trigger_from_gate_decision(decision))
            return DiagnoseOutcome(
                above_gate=False,
                problem_id=None,
                label=None,
                stage=None,
                confidence=None,
                advisory=None,
                citations=[],
                health_delta_from=None,
                health_delta_to=None,
                reason=decision.reason,
                escalation=escalation,
                spoken_summary=decision.spoken_summary or ESCALATE_SPOKEN_SUMMARY_FALLBACK,
            )

        raw = await self._llm.generate_grounded_advisory(
            query=query,
            context_chunks=[_chunk_to_dict(c) for c in chunks],
            farm_context={"farm_id": farm_id, "label": label},
        )
        parsed = parse_advisory_output(raw)

        if parsed.insufficient_context:
            # Gate passed on relevance, but the model still couldn't ground
            # an answer (or failed validation) — still escalate, never guess.
            escalation = await self._escalate(
                farm_id, None, parsed.reason or "insufficient context", "no_relevant_source"
            )
            return DiagnoseOutcome(
                above_gate=False,
                problem_id=None,
                label=None,
                stage=None,
                confidence=None,
                advisory=None,
                citations=[],
                health_delta_from=None,
                health_delta_to=None,
                reason=parsed.reason,
                escalation=escalation,
                spoken_summary=ESCALATE_SPOKEN_SUMMARY_FALLBACK,
            )

        problem_id = str(uuid4())
        before, after = await self._register_problem_and_recompute(farm_id, problem_id, label, image_asset_id)

        return DiagnoseOutcome(
            above_gate=True,
            problem_id=problem_id,
            label=label,
            stage=INITIAL_PROBLEM_SEVERITY.value,
            confidence=confidence,
            advisory=parsed.advisory,
            citations=parsed.citations,
            health_delta_from=before,
            health_delta_to=after,
            reason=None,
            escalation=None,
            spoken_summary=COMPOSED_SPOKEN_SUMMARY,
        )

    async def _register_problem_and_recompute(
        self, farm_id: str, problem_id: str, label: str, image_asset_id: str
    ) -> tuple[int | None, int | None]:
        """Register the new problem (with its photo and an initial timeline
        entry) with the health engine, schedule its first follow-up
        (PRD §5.10), and recompute — returning ``(score_before, score_after)``
        for ``health_delta``."""
        before_snapshot: HealthSnapshot = await self._health.get_latest(farm_id)
        before_score = before_snapshot.score

        await self._problems.register_problem(
            Problem(
                problem_id=problem_id,
                farm_id=farm_id,
                label=label,
                severity=INITIAL_PROBLEM_SEVERITY,
                image_asset_ids=[image_asset_id],
            )
        )
        await self._problems.schedule_followup(problem_id, farm_id)

        after_snapshot = await self._health.recompute(
            farm_id,
            triggering_input=TriggeringInput(
                type="diagnosis",
                details={"problem_id": problem_id, "severity": INITIAL_PROBLEM_SEVERITY.value, "label": label},
            ),
        )
        return before_score, after_snapshot.score

    async def _escalate(
        self, farm_id: str, problem_id: str | None, reason: str | None, trigger: str
    ) -> DiagnoseEscalation:
        case = await self._escalation.escalate(
            farm_id=farm_id, problem_id=problem_id, reason=reason or trigger, trigger=trigger
        )
        return DiagnoseEscalation(case_id=case.id, assigned_to=case.assigned_to)


def get_diagnosis_service(
    image_port: Annotated[ImageDiagnosisPort, Depends(get_image_diagnosis_adapter)],
    retrieval: Annotated[RetrievalService, Depends(get_retrieval_service)],
    llm_port: Annotated[LLMPort, Depends(get_llm_adapter)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    problem_registry: Annotated[ProblemRegistry, Depends(get_problem_registry)],
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> DiagnosisService:
    """FastAPI dependency provider assembling ``DiagnosisService`` from its ports."""
    return DiagnosisService(
        image_port, retrieval, llm_port, health_service, problem_registry, escalation_service, settings
    )
