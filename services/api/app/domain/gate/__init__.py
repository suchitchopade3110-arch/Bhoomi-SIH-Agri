"""The confidence gate (PRD §5.6, §5.7, SIH26131 §2): the single decision point for
answer-vs-escalate. Pure, deterministic, no I/O.
"""

from app.domain.gate.constants import (
    GATE_REASON_BELOW_IMAGE_CONFIDENCE,
    GATE_REASON_BELOW_RETRIEVAL_RELEVANCE,
    GATE_REASON_OUT_OF_SCOPE,
    SUPPORTED_LABELS,
)
from app.domain.gate.decide import check_gate, decide
from app.domain.gate.decision import GateDecision

__all__ = [
    "check_gate",
    "decide",
    "GateDecision",
    "SUPPORTED_LABELS",
    "GATE_REASON_BELOW_IMAGE_CONFIDENCE",
    "GATE_REASON_OUT_OF_SCOPE",
    "GATE_REASON_BELOW_RETRIEVAL_RELEVANCE",
]
