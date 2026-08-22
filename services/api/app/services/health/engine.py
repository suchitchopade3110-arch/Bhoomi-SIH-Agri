"""services/health/engine.py — spec-mandated module for the health-score entry point.

``compute_health`` is the single public API for the health engine.  Its
implementation lives in ``app.domain.health.score``; this shim exposes it
at the spec path ``app.services.health.engine``.

Determinism guarantee (Phase 1 requirement):
  - ``compute_health`` is pure: same ``HealthScoreInputs`` → same
    ``HealthScoreResult`` every time.
  - Timestamps are passed in via ``TriggeringInput``, never read from the
    clock inside the function.
  - No global mutable state; no randomness.
  - The acceptance test confirms this by calling the function twice with the
    same inputs and asserting equality.
"""

from app.domain.health.score import (  # noqa: F401
    HealthScoreResult,
    band_for,
    compute_health,
)

__all__ = ["compute_health", "band_for", "HealthScoreResult"]
