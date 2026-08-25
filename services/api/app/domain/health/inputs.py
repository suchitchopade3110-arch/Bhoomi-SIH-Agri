"""Input value objects for the Farm Health / Risk Score engine.

These are plain, immutable data carriers — no I/O, no defaults sourced from a
database. ``services/health_service.py`` is responsible for assembling a
``HealthScoreInputs`` from repositories/adapters before calling
``domain.health.score.compute_health``.
"""

from dataclasses import dataclass, field
from typing import Any

from app.core.enums import FollowupResponse, ProblemSeverity


@dataclass(frozen=True)
class WeatherReading:
    """A single point-in-time weather observation."""

    temp_c: float
    relative_humidity_pct: float


@dataclass(frozen=True)
class CropIdealConditions:
    """The ideal environmental band for a crop at its current growth stage."""

    temp_min_c: float
    temp_max_c: float
    humidity_min_pct: float
    humidity_max_pct: float
    soil_moisture_min_pct: float | None = None


@dataclass(frozen=True)
class OpenProblemInput:
    """One currently-open problem contributing to active problem severity."""

    severity: ProblemSeverity


@dataclass(frozen=True)
class TriggeringInput:
    """Describes the event that caused a score recompute — echoed verbatim
    onto the persisted snapshot so every score movement is auditable."""

    type: str
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"type": self.type, **self.details}


@dataclass(frozen=True)
class HealthScoreInputs:
    """Everything ``compute_health`` needs for one farm, at one point in time."""

    triggering_input: TriggeringInput

    # Sub-index #1: active_problem_severity
    open_problems: list[OpenProblemInput] = field(default_factory=list)

    # Sub-index #2: environmental_risk
    weather: WeatherReading | None = None
    crop_ideal: CropIdealConditions | None = None

    # Sub-index #3: monitoring_recency
    days_since_last_scan: int | None = None
    is_expert_verified: bool = False

    # Sub-index #4: treatment_response
    latest_followup_response: FollowupResponse | None = None
    consecutive_got_worse_count: int = 0
    problem_resolved_with_confirmed_treatment: bool = False

    # Gating & activity flag (Day 0 unrated policy)
    has_interaction: bool = True

    # Legacy/compatibility fields (optional/ignored in v2 calculation)
    soil_moisture_pct: float | None = None
    irrigation_delivered_mm: float | None = None
    irrigation_required_mm: float | None = None
    days_since_planting: int | None = None
    expected_stage_day: int = 0

    def required_inputs_present(self) -> bool:
        """True once enough fields exist to compute a real score.
        A farm remains Unrated until it records at least one interaction."""
        return self.has_interaction
