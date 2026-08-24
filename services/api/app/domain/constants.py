"""Domain constants — canonical public surface for the intelligence layer.

Re-exports the named scoring constants from their implementation homes so the
spec-mandated import path ``app.domain.constants`` works alongside the
existing ``app.domain.health.constants`` path.

API Contract §2.9 / PRD §7.2–§7.3:
    WEIGHTS          — six sub-index weights, sum == 1.0 (asserted at load time)
    SEVERITY_PENALTY — early=30, moderate=55, severe=80
    CONFIDENCE_GATE  — 0.70  (re-exported from config; kept here so domain
                                code can reference it without importing settings)
    RAG_RELEVANCE_THRESHOLD — 0.60 nominal (runtime value lives in settings)
"""

from app.domain.health.constants import (  # noqa: F401  (re-export)
    BAND_THRESHOLDS,
    SEVERITY_PENALTY,
    SUBINDEX_ORDER,
    WEIGHTS,
    WEIGHTS_VERSION,
)

# Pure domain gate thresholds (no I/O, no Settings dependencies)
CONFIDENCE_GATE: float = 0.70
PEST_CONFIDENCE_GATE: float = CONFIDENCE_GATE

# RAG relevance thresholds: calibrated per embedding modality
RAG_RELEVANCE_THRESHOLD_STUB: float = 0.18        # calibrated for token-hashing stub vectors
RAG_RELEVANCE_THRESHOLD_PRODUCTION: float = 0.60  # target for real BGE-m3 dense embeddings

__all__ = [
    "WEIGHTS",
    "SEVERITY_PENALTY",
    "BAND_THRESHOLDS",
    "SUBINDEX_ORDER",
    "WEIGHTS_VERSION",
    "CONFIDENCE_GATE",
    "PEST_CONFIDENCE_GATE",
    "RAG_RELEVANCE_THRESHOLD_STUB",
    "RAG_RELEVANCE_THRESHOLD_PRODUCTION",
]
