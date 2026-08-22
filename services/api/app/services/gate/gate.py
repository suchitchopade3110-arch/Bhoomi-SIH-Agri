"""services/gate/gate.py — spec-mandated module: decide() → Decision.

This module is the public entry point for the confidence gate per the
AGENTS.md spec.  The pure decision logic lives in
``app.domain.gate.decide``; this shim exposes it at the spec path
``app.services.gate.gate``.

Invariant (hard rule #1): No code path may yield an advisory when either
``image_confidence < CONFIDENCE_GATE`` or
``retrieval_relevance < RAG_RELEVANCE_THRESHOLD``.  The gate is the only
place this check happens — routers never bypass it.

Gate order (PRD §5.6, checked in ``decide()``):
  1. image confidence < CONFIDENCE_GATE     → escalate (BELOW_CONFIDENCE_GATE)
  2. crop/disease not in supported set       → escalate (BELOW_CONFIDENCE_GATE)
  3. retrieval relevance < RAG_RELEVANCE_THRESHOLD → escalate (NO_RELEVANT_SOURCE)
  4. all clear                               → compose
"""

from app.domain.gate.decide import decide  # noqa: F401
from app.domain.gate.decision import GateDecision  # noqa: F401

__all__ = ["decide", "GateDecision"]
