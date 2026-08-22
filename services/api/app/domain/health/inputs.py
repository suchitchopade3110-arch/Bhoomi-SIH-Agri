"""Input value objects for the Farm Health Score engine.

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
    """The ideal environmental band for a crop at its current growth stage.

    Sourced from the same FAO-56 / ICAR package-of-practices tables the
    resource planner uses (PRD §5.4) — this domain package only consumes the
    numbers, it does not look them up.
    """

    temp_min_c: float
    temp_max_c: float
    humidity_min_pct: float
    humidity_max_pct: float
    soil_moisture_min_pct: float


@dataclass(frozen=True)
class OpenProblemInput:
    """One currently-open problem contributing to the active problem load."""

    severity: ProblemSeverity


@dataclass(frozen=True)
class TriggeringInput:
    """Describes the event that caused a health recompute — echoed verbatim
    onto the persisted snapshot so every score movement is auditable
    (PRD §7.1, contract §2.9 ``triggering_input``)."""

    type: str
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"type": self.type, **self.details}


@dataclass(frozen=True)
class HealthScoreInputs:
    """Everything ``compute_health`` needs for one farm, at one point in time.

    Any of the fields below may be ``None`` to represent a genuinely missing
    input (PRD §5.2: "Missing fields leave the health score Unrated rather
    than guessing"). When any required field is ``None``, ``compute_health``
    returns an ``unrated`` snapshot instead of guessing a number.
    """

    triggering_input: TriggeringInput

    # Sub-index #1 inputs
    weather: WeatherReading | None
    crop_ideal: CropIdealConditions
    soil_moisture_pct: float | None

    # Sub-index #2 inputs
    irrigation_delivered_mm: float | None
    irrigation_required_mm: float | None

    # Sub-index #3 inputs
    days_since_planting: int | None
    expected_stage_day: int

    # Sub-index #4 inputs
    open_problems: list[OpenProblemInput]

    # Sub-index #5 inputs
    days_since_last_scan: int | None

    # Sub-index #6 inputs
    latest_followup_response: FollowupResponse | None
    consecutive_got_worse_count: int
    problem_resolved_with_confirmed_treatment: bool
    is_expert_verified: bool = False

    def required_inputs_present(self) -> bool:
        """True once enough fields exist to compute a real (non-``unrated``)
        score. Per PRD §5.2/§7.1, Day 0 (or any farm still missing a
        required onboarding/monitoring field) stays ``unrated`` rather than
        being scored on guessed defaults."""
        return (
            self.weather is not None
            and self.soil_moisture_pct is not None
            and self.irrigation_delivered_mm is not None
            and self.irrigation_required_mm is not None
            and self.days_since_planting is not None
            and self.days_since_last_scan is not None
        )
