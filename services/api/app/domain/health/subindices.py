"""The six pure sub-index calculators behind the Farm Health Score (PRD §7.2).

Each function takes plain values and returns an ``int`` in ``[0, 100]``. None
of them touch a database, the network, or a clock — every "recency"-style
input arrives pre-computed (e.g. ``days_since_last_scan``) so the functions
stay trivially unit-testable with fixed inputs.
"""

from dataclasses import dataclass

from app.core.enums import FollowupResponse, SubIndexKey
from app.domain.health import constants as c
from app.domain.health.inputs import (
    CropIdealConditions,
    HealthScoreInputs,
    OpenProblemInput,
    WeatherReading,
)


def _clamp_int(value: float, low: int = 0, high: int = 100) -> int:
    """Round to the nearest int and clamp into ``[low, high]``."""
    return max(low, min(high, round(value)))


def environmental_suitability(weather: WeatherReading, ideal: CropIdealConditions, soil_moisture_pct: float) -> int:
    """Sub-index #1: current weather + soil vs. this crop's needs at its stage.

    Starts at 100 and subtracts a penalty for every degree/percent the
    reading falls outside the crop's ideal band. Weight: 0.20 (PRD §7.2).
    """
    penalty = 0.0
    penalty += c.TEMP_DEVIATION_PENALTY_PER_DEGREE_C * max(0.0, ideal.temp_min_c - weather.temp_c)
    penalty += c.TEMP_DEVIATION_PENALTY_PER_DEGREE_C * max(0.0, weather.temp_c - ideal.temp_max_c)
    penalty += c.HUMIDITY_DEVIATION_PENALTY_PER_PCT * max(0.0, weather.relative_humidity_pct - ideal.humidity_max_pct)
    penalty += c.HUMIDITY_DEVIATION_PENALTY_PER_PCT * max(0.0, ideal.humidity_min_pct - weather.relative_humidity_pct)
    penalty += c.SOIL_MOISTURE_DEFICIT_PENALTY_PER_PCT * max(0.0, ideal.soil_moisture_min_pct - soil_moisture_pct)
    return _clamp_int(100 - penalty)


def resource_adequacy(irrigation_delivered_mm: float, irrigation_required_mm: float) -> int:
    """Sub-index #2: irrigation actually delivered vs. the ET0-based requirement.

    A 1:1 ratio (or better) scores 100; shortfall scores proportionally
    lower. Weight: 0.15 (PRD §7.2).
    """
    if irrigation_required_mm <= 0:
        return 100
    ratio = irrigation_delivered_mm / irrigation_required_mm
    return _clamp_int(100 * ratio)


def crop_stage_progression(days_since_planting: int, expected_stage_day: int) -> int:
    """Sub-index #3: on-schedule vigor for the current growth stage.

    Penalizes the gap between actual days-since-planting and the crop
    calendar's expected day for this stage. Weight: 0.15 (PRD §7.2).
    """
    deviation_days = abs(days_since_planting - expected_stage_day)
    penalty = c.STAGE_DEVIATION_PENALTY_PER_DAY * deviation_days
    return _clamp_int(100 - penalty)


def active_problem_load(open_problems: list[OpenProblemInput]) -> int:
    """Sub-index #4 (weight 0.30 — the big mover, PRD §7.2/§7.3).

    ``100 - sum(severity_penalty per open problem)``, floored at 0.
    """
    total_penalty = sum(c.SEVERITY_PENALTY[p.severity] for p in open_problems)
    return _clamp_int(100 - total_penalty)


def monitoring_recency(days_since_last_scan: int) -> int:
    """Sub-index #5: are scans/data recent enough to trust the score?

    Weight: 0.10 (PRD §7.2).
    """
    penalty = c.MONITORING_RECENCY_PENALTY_PER_DAY * days_since_last_scan
    return _clamp_int(100 - penalty)


def treatment_response(
    latest_followup_response: FollowupResponse | None,
    consecutive_got_worse_count: int,
    problem_resolved_with_confirmed_treatment: bool,
) -> int:
    """Sub-index #6: follow-up trend (Improved / No Change / Got Worse).

    Weight: 0.10 (PRD §7.2). A confirmed expert resolution always yields the
    maximum score, regardless of the trend leading up to it (PRD §7.4:
    "the farm is now well-monitored with a logged, successful treatment").
    """
    if problem_resolved_with_confirmed_treatment:
        return c.TREATMENT_RESPONSE_CONFIRMED_RESOLVED
    if latest_followup_response is None:
        return c.TREATMENT_RESPONSE_DEFAULT
    if latest_followup_response == FollowupResponse.IMPROVED:
        return c.TREATMENT_RESPONSE_IMPROVED
    if latest_followup_response == FollowupResponse.NO_CHANGE:
        return c.TREATMENT_RESPONSE_NO_CHANGE
    # GOT_WORSE: step down for every consecutive worsening report.
    penalty = c.TREATMENT_RESPONSE_GOT_WORSE_PENALTY_STEP * max(1, consecutive_got_worse_count)
    return _clamp_int(c.TREATMENT_RESPONSE_DEFAULT - penalty)


@dataclass(frozen=True)
class SubIndexBreakdown:
    """One row of the transparent score breakdown (contract §2.9)."""

    key: SubIndexKey
    value: int
    weight: float
    contribution: float


def compute_all_subindices(inputs: HealthScoreInputs) -> list[SubIndexBreakdown]:
    """Run all six calculators against ``inputs`` and return them in the
    fixed contract order (PRD §7.2 / contract §2.9), each carrying its
    weight and weighted contribution.

    Requires ``inputs.required_inputs_present()`` to be true — callers must
    check that first and route to the ``unrated`` path otherwise.
    """
    assert inputs.weather is not None
    assert inputs.soil_moisture_pct is not None
    assert inputs.irrigation_delivered_mm is not None
    assert inputs.irrigation_required_mm is not None
    assert inputs.days_since_planting is not None
    assert inputs.days_since_last_scan is not None

    values: dict[SubIndexKey, int] = {
        SubIndexKey.ENVIRONMENTAL_SUITABILITY: environmental_suitability(
            inputs.weather, inputs.crop_ideal, inputs.soil_moisture_pct
        ),
        SubIndexKey.RESOURCE_ADEQUACY: resource_adequacy(
            inputs.irrigation_delivered_mm, inputs.irrigation_required_mm
        ),
        SubIndexKey.CROP_STAGE_PROGRESSION: crop_stage_progression(
            inputs.days_since_planting, inputs.expected_stage_day
        ),
        SubIndexKey.ACTIVE_PROBLEM_LOAD: active_problem_load(inputs.open_problems),
        SubIndexKey.MONITORING_RECENCY: monitoring_recency(inputs.days_since_last_scan),
        SubIndexKey.TREATMENT_RESPONSE: treatment_response(
            inputs.latest_followup_response,
            inputs.consecutive_got_worse_count,
            inputs.problem_resolved_with_confirmed_treatment,
        ),
    }

    return [
        SubIndexBreakdown(
            key=key,
            value=values[key],
            weight=c.WEIGHTS[key],
            contribution=round(values[key] * c.WEIGHTS[key], 4),
        )
        for key in c.SUBINDEX_ORDER
    ]
