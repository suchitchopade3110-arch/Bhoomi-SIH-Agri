"""Pure, deterministic Farm Health Score engine (PRD §7).

No I/O, no DB, no network calls anywhere in this package. Every function is a
plain function of its arguments: same inputs -> same output, always. Callers
(``services/health_service.py``) are responsible for gathering real-world
inputs and persisting the result.
"""

from app.domain.health.inputs import (
    CropIdealConditions,
    HealthScoreInputs,
    OpenProblemInput,
    TriggeringInput,
    WeatherReading,
)
from app.domain.health.score import HealthScoreResult, band_for, compute_health
from app.domain.health.subindices import SubIndexBreakdown

__all__ = [
    "CropIdealConditions",
    "HealthScoreInputs",
    "OpenProblemInput",
    "TriggeringInput",
    "WeatherReading",
    "SubIndexBreakdown",
    "HealthScoreResult",
    "band_for",
    "compute_health",
]
