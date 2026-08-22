"""services/health/ — spec-mandated package for the health-score engine.

Re-exports the pure sub-index calculators and the ``compute_health`` entry
point from their implementation homes so the spec-path
``from app.services.health.engine import compute_health`` works alongside
the existing ``from app.domain.health.score import compute_health`` path.
"""

from app.domain.health.score import compute_health  # noqa: F401
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
    "compute_health",
    "compute_all_subindices",
    "SubIndexBreakdown",
    "environmental_suitability",
    "resource_adequacy",
    "crop_stage_progression",
    "active_problem_load",
    "monitoring_recency",
    "treatment_response",
]
