"""services/health/subindices.py — spec-mandated module for sub-index calculators.

The six pure sub-index calculator functions live in
``app.domain.health.subindices``. This shim exposes them at the spec path
``app.services.health.subindices``.

All six calculators are pure: same inputs → same outputs; no I/O, no
randomness, no clock reads. The acceptance test (Phase 1) exercises them
via fixed fixtures.
"""

from app.domain.health.subindices import (  # noqa: F401
    SubIndexBreakdown,
    active_problem_load,
    compute_all_subindices,
    crop_stage_progression,
    environmental_suitability,
    monitoring_recency,
    resource_adequacy,
    treatment_response,
)

__all__ = [
    "environmental_suitability",
    "resource_adequacy",
    "crop_stage_progression",
    "active_problem_load",
    "monitoring_recency",
    "treatment_response",
    "SubIndexBreakdown",
    "compute_all_subindices",
]
