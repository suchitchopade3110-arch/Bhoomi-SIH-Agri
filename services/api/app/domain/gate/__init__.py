"""The confidence gate (PRD §5.6, §5.7): the single decision point for
answer-vs-escalate. Pure, deterministic, no I/O.
"""

from app.domain.gate.decide import decide
from app.domain.gate.decision import GateDecision

__all__ = ["decide", "GateDecision"]
