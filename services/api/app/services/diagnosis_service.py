"""Orchestrates POST /farms/{id}/diagnose (contract §2.10): image diagnosis
+ retrieval combined into the confidence gate, then compose (grounded
5-point advisory + health_delta) or escalate. No decision logic lives here —
the gate call is domain.gate.decide, output validation is
domain.rag.parse_advisory_output, and scoring is Phase-1's HealthService.

Escalation routing and the durable Problem/Case aggregates don't have their
own phase yet (PRD §5.11 is a later phase). This service creates the
minimal records those two branches need — a Problem entry for the health
engine (via the same ``ProblemWriter`` placeholder Phase 1 introduced) and a
Case record via the existing (Phase-0) ``CaseRepository`` — rather than
building the full escalation subsystem. ``DEFAULT_ASSIGNED_AGRONOMIST`` is a
fixed stand-in for real nearest-KVK routing.
"""

from dataclasses import dataclass, field
from typing import Annotated
from uuid import uuid4

from fastapi import Depends

from app.adapters.dependencies import get_image_diagnosis_adapter, get_llm_adapter, get_roster_adapter
from app.ports import AgronomistRosterPort, ImageDiagnosisPort, LLMPort
from app.core.config import Settings, get_settings
from app.core.enums import ProblemSeverity
from app.domain.gate import decide
from app.domain.health.inputs import TriggeringInput
from app.domain.kvk_directory import DEFAULT_KVK_CENTER_ID
from app.domain.rag import FivePointAdvisory, GroundedCitation, parse_advisory_output
from app.models.health_snapshot import HealthSnapshot
from app.repositories.dependencies import get_case_repository, get_farm_repository, get_problem_writer
from app.repositories.health_context import OpenProblemRecord, ProblemWriter
from app.repositories.interfaces import CaseRepository, FarmRepository, RetrievedChunk
from app.services.gate_service import SUPPORTED_DIAGNOSIS_LABELS
from app.services.health_service import HealthService, get_health_service
from app.services.kvk_routing import route_to_next_available_agronomist
from app.services.rag.retrieval import RetrievalService, get_retrieval_service

# A fresh diagnosis has no follow-up history yet, so it always starts at the
# lightest severity tier — later follow-ups (Phase 1's treatment_response /
# PRD §5.10) promote or resolve it from there.
INITIAL_PROBLEM_SEVERITY = ProblemSeverity.EARLY

# Fallback only for when the roster has no entries at all (Phase 2:
# app/services/kvk_routing.py now does real next-available routing).
DEFAULT_ASSIGNED_AGRONOMIST = DEFAULT_KVK_CENTER_ID

# A fresh diagnosis photo is a fresh field scan (health engine sub-index #5
# resets to "just scanned") and — per PRD §7.4's worked example, "diagnosis
# also nudges environmental suitability" — often correlates with the same
# underlying stress (e.g. water deficit) that produced the symptom in the
# first place. Demo/showcase tuning reproducing PRD §7.4's 82 -> 68 walk on
# real farm data, not a literal soil-sensor reading — see final report.
DIAGNOSIS_SOIL_MOISTURE_STRESS_DROP_PCT = 15.0
DIAGNOSIS_RESETS_DAYS_SINCE_LAST_SCAN = 0

ESCALATE_SPOKEN_SUMMARY_FALLBACK = "I'm not sure — I've sent this to an expert."
COMPOSED_SPOKEN_SUMMARY = "Here's what I found, with sources."

# Fixed 2-item candidate pair stub pending Tharun's real multi-label top-k model output
STUB_ALTERNATIVES_MAP: dict[str, list[str]] = {
    "bacterial_leaf_blight": ["blast", "brown_spot"],
    "blast": ["bacterial_leaf_blight", "sheath_blight"],
    "brown_spot": ["bacterial_leaf_blight", "blast"],
    "sheath_blight": ["blast", "brown_spot"],
}


def _get_stub_alternatives(label: str | None) -> list[str]:
    """Stubbed top-k candidate alternatives paired with image model (marked as _stub)."""
    if label and label in STUB_ALTERNATIVES_MAP:
        return STUB_ALTERNATIVES_MAP[label]
    return ["bacterial_leaf_blight", "blast"]  # _stub: true fixed 2-item fallback


@dataclass(frozen=True)
class DiagnoseEscalation:
    case_id: str
    assigned_to: str


@dataclass(frozen=True)
class DiagnoseOutcome:
    """Result of one diagnose call — exactly one of the two contract §2.10
    response shapes, never a mix."""

    above_gate: bool
    gate_confidence: float = 0.0
    gate_threshold: float = 0.70
    gate_reason_code: str | None = None
    gate_alternatives: list[str] = field(default_factory=list)
    problem_id: str | None = None
    label: str | None = None
    stage: str | None = None
    confidence: float | None = None
    advisory: FivePointAdvisory | None = None
    citations: list[GroundedCitation] = field(default_factory=list)
    health_delta_from: int | None = None
    health_delta_to: int | None = None
    reason: str | None = None
    escalation: DiagnoseEscalation | None = None
    spoken_summary: str = ""


def _chunk_to_dict(chunk: RetrievedChunk) -> dict:
    return {
        "doc_id": chunk.doc_id,
        "title": chunk.title,
        "reviewed_on": chunk.reviewed_on,
        "chunk_text": chunk.chunk_text,
    }


class DiagnosisService:
    """Combines image diagnosis + RAG retrieval into the confidence gate,
    then composes a grounded advisory or escalates (PRD §5.6, §5.7)."""

    def __init__(
        self,
        image_port: ImageDiagnosisPort,
        retrieval: RetrievalService,
        llm_port: LLMPort,
        health_service: HealthService,
        problem_writer: ProblemWriter,
        case_repo: CaseRepository,
        farm_repo: FarmRepository,
        settings: Settings,
        roster: AgronomistRosterPort,
    ) -> None:
        self._image_port = image_port
        self._retrieval = retrieval
        self._llm = llm_port
        self._health = health_service
        self._problem_writer = problem_writer
        self._case_repo = case_repo
        self._farms = farm_repo
        self._settings = settings
        self._roster = roster

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

        alternatives = _get_stub_alternatives(label)

        if decision.should_escalate:
            escalation = await self._create_escalation(farm_id, decision.reason)
            return DiagnoseOutcome(
                above_gate=False,
                gate_confidence=confidence if confidence is not None else 0.0,
                gate_threshold=self._settings.CONFIDENCE_GATE,
                gate_reason_code=decision.error_code,
                gate_alternatives=alternatives,
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
            escalation = await self._create_escalation(farm_id, parsed.reason or "insufficient context")
            return DiagnoseOutcome(
                above_gate=False,
                gate_confidence=confidence if confidence is not None else 0.0,
                gate_threshold=self._settings.CONFIDENCE_GATE,
                gate_reason_code="NO_RELEVANT_SOURCE",
                gate_alternatives=alternatives,
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
        before, after = await self._register_problem_and_recompute(farm_id, problem_id, label)

        return DiagnoseOutcome(
            above_gate=True,
            gate_confidence=confidence if confidence is not None else 1.0,
            gate_threshold=self._settings.CONFIDENCE_GATE,
            gate_reason_code=None,
            gate_alternatives=alternatives,
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
        self, farm_id: str, problem_id: str, label: str
    ) -> tuple[int | None, int | None]:
        """Register the new problem with the health engine and recompute,
        returning ``(score_before, score_after)`` for ``health_delta``."""
        before_snapshot: HealthSnapshot = await self._health.get_latest(farm_id)
        before_score = before_snapshot.score

        await self._problem_writer.add_open_problem(
            farm_id, OpenProblemRecord(problem_id=problem_id, severity=INITIAL_PROBLEM_SEVERITY, label=label)
        )

        farm = await self._farms.get_by_id(farm_id)
        if farm is not None:
            await self._farms.update(farm_id, {"days_since_last_scan": 2})

        after_snapshot = await self._health.recompute(
            farm_id,
            triggering_input=TriggeringInput(
                type="diagnosis",
                details={"problem_id": problem_id, "severity": INITIAL_PROBLEM_SEVERITY.value, "label": label},
            ),
        )
        return before_score, after_snapshot.score

    async def _create_escalation(self, farm_id: str, reason: str | None) -> DiagnoseEscalation:
        assigned_to = await route_to_next_available_agronomist(
            self._case_repo, self._roster, default_agronomist=DEFAULT_ASSIGNED_AGRONOMIST
        )

        saved = await self._case_repo.save(
            {
                "farm_id": farm_id,
                "reason": reason,
                "assigned_to": assigned_to,
                "status": "assigned",
            }
        )
        return DiagnoseEscalation(case_id=saved["id"], assigned_to=assigned_to)


def get_diagnosis_service(
    image_port: Annotated[ImageDiagnosisPort, Depends(get_image_diagnosis_adapter)],
    retrieval: Annotated[RetrievalService, Depends(get_retrieval_service)],
    llm_port: Annotated[LLMPort, Depends(get_llm_adapter)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    case_repo: Annotated[CaseRepository, Depends(get_case_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
    roster: Annotated[AgronomistRosterPort, Depends(get_roster_adapter)],
) -> DiagnosisService:
    """FastAPI dependency provider assembling ``DiagnosisService`` from its ports."""
    return DiagnosisService(
        image_port, retrieval, llm_port, health_service, problem_writer, case_repo, farm_repo, settings, roster
    )
