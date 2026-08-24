"""The confidence gate: the single decision point for answer-vs-escalate
(PRD §5.6, §5.7, SIH26131 §2). Pure and deterministic — no I/O, no DB, no network.

"The confidence gate lives at the boundary, not inside the LLM" (tech stack
§1.3): the image model returns a probability, the RAG retriever returns a
relevance score, and this function checks both against thresholds before
anything downstream is allowed to compose an answer. It must be structurally
impossible for a caller to end up with both a "compose" and an "escalate" —
``decide()`` / ``check_gate()`` returns exactly one ``GateDecision``.
"""

from typing import Literal

from app.core.enums import GateOutcome
from app.domain.constants import CONFIDENCE_GATE
from app.domain.gate.constants import (
    GATE_REASON_BELOW_IMAGE_CONFIDENCE,
    GATE_REASON_BELOW_RETRIEVAL_RELEVANCE,
    GATE_REASON_OUT_OF_SCOPE,
    GATE_REASON_TO_ERROR_CODE,
    SUPPORTED_LABELS,
)
from app.domain.gate.decision import GateDecision

_ESCALATE_SPOKEN_SUMMARY = "I'm not sure — I've sent this to an expert."


def _escalate(reason: str, detail: str) -> GateDecision:
    return GateDecision(
        outcome=GateOutcome.ESCALATE,
        reason=detail,
        error_code=GATE_REASON_TO_ERROR_CODE.get(reason, "BELOW_CONFIDENCE_GATE"),
        spoken_summary=_ESCALATE_SPOKEN_SUMMARY,
    )


def check_gate(
    *,
    target_type: Literal["disease", "pest"] = "disease",
    label: str,
    confidence: float,
    retrieval_relevance: float | None = None,
    confidence_gate: float = CONFIDENCE_GATE,
    relevance_threshold: float | None = None,
) -> GateDecision:
    """Decide compose-vs-escalate for disease and pest diagnosis.

    Evaluates:
    1. Scope validation: label in SUPPORTED_LABELS[target_type]. If not, escalates
       with OUT_OF_SCOPE_TARGET.
    2. Image confidence: confidence >= confidence_gate (0.70). If below, escalates
       with BELOW_CONFIDENCE_GATE.
    3. Retrieval relevance (if provided): relevance >= relevance_threshold. If below,
       escalates with NO_RELEVANT_SOURCE.

    Returns:
        GateDecision with exactly one outcome: compose or escalate.
    """
    labels_for_type = SUPPORTED_LABELS.get(target_type, frozenset())
    if label not in labels_for_type:
        return _escalate(
            GATE_REASON_OUT_OF_SCOPE,
            f"Label '{label}' not in supported set for target_type={target_type}",
        )

    if confidence < confidence_gate:
        return _escalate(
            GATE_REASON_BELOW_IMAGE_CONFIDENCE,
            f"Confidence {confidence:.2f} < gate {confidence_gate:.2f}",
        )

    if (
        relevance_threshold is not None
        and retrieval_relevance is not None
        and retrieval_relevance < relevance_threshold
    ):
        return _escalate(
            GATE_REASON_BELOW_RETRIEVAL_RELEVANCE,
            f"relevance {retrieval_relevance:.2f} < threshold {relevance_threshold:.2f}",
        )

    return GateDecision(
        outcome=GateOutcome.COMPOSE,
        reason=None,
        error_code=None,
        spoken_summary=None,
    )


def decide(
    image_confidence: float | None,
    in_scope: bool,
    retrieval_relevance: float | None,
    *,
    confidence_gate: float,
    relevance_threshold: float,
) -> GateDecision:
    """Decide compose-vs-escalate for one diagnosis/advisory attempt.

    Args:
        image_confidence: The image model's native confidence (0.0-1.0), or
            ``None`` if no image was involved (e.g. a text-only advisory
            query). A missing signal is skipped, never treated as a pass.
        in_scope: Whether the identified crop/disease is within the bounded,
            supported set this version handles (PRD §5.6).
        retrieval_relevance: The RAG retriever's top relevance score
            (0.0-1.0), or ``None`` if retrieval wasn't performed for this
            call. A missing signal is skipped, never treated as a pass.
        confidence_gate: Minimum acceptable image confidence, from config
            (``settings.CONFIDENCE_GATE``) — never hardcoded here.
        relevance_threshold: Minimum acceptable retrieval relevance, from
            config (``settings.RAG_RELEVANCE_THRESHOLD``) — never hardcoded
            here.

    Returns:
        A ``GateDecision`` with ``outcome`` set to exactly one of
        ``GateOutcome.COMPOSE`` or ``GateOutcome.ESCALATE``. Checked in
        order: image confidence, then scope, then retrieval relevance — the
        first failing signal determines the escalation reason.
    """
    if image_confidence is not None and image_confidence < confidence_gate:
        return _escalate(
            GATE_REASON_BELOW_IMAGE_CONFIDENCE,
            f"confidence {image_confidence:.2f} < gate {confidence_gate:.2f}",
        )

    if not in_scope:
        return _escalate(
            GATE_REASON_OUT_OF_SCOPE,
            "crop/disease is outside the supported set",
        )

    if retrieval_relevance is not None and retrieval_relevance < relevance_threshold:
        return _escalate(
            GATE_REASON_BELOW_RETRIEVAL_RELEVANCE,
            f"relevance {retrieval_relevance:.2f} < threshold {relevance_threshold:.2f}",
        )

    return GateDecision(
        outcome=GateOutcome.COMPOSE,
        reason=None,
        error_code=None,
        spoken_summary=None,
    )
