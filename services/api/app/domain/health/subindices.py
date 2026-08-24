"""The four pure sub-index calculators behind the Farm Health / Risk Score (SIH26131).

Each function takes plain values and returns an ``int`` in ``[0, 100]``. None
of them touch a database, the network, or a clock — every input arrives pre-computed
so the functions stay trivially unit-testable with fixed inputs.
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


def active_problem_severity(open_problems: list[OpenProblemInput]) -> int:
    """Sub-index #1: active disease and pest problem severity (Weight: 0.40).

    ``100 - sum(severity_penalty per open problem)``, floored at 0.
    """
    total_penalty = sum(c.SEVERITY_PENALTY[p.severity] for p in open_problems)
    return _clamp_int(100 - total_penalty)


def environmental_risk(weather: WeatherReading | None, ideal: CropIdealConditions | None = None) -> int:
    """Sub-index #2: weather deviation from crop's ideal band (Weight: 0.25).

    Returns ENVIRONMENTAL_RISK_DEFAULT (70) when weather is None/unavailable.
    Otherwise starts at 100 and subtracts penalties for temperature and humidity deviations.
    """
    if weather is None:
        return c.ENVIRONMENTAL_RISK_DEFAULT
    if ideal is None:
        return 100
    penalty = 0.0
    penalty += c.TEMP_DEVIATION_PENALTY_PER_DEGREE_C * max(0.0, ideal.temp_min_c - weather.temp_c)
    penalty += c.TEMP_DEVIATION_PENALTY_PER_DEGREE_C * max(0.0, weather.temp_c - ideal.temp_max_c)
    penalty += c.HUMIDITY_DEVIATION_PENALTY_PER_PCT * max(0.0, weather.relative_humidity_pct - ideal.humidity_max_pct)
    penalty += c.HUMIDITY_DEVIATION_PENALTY_PER_PCT * max(0.0, ideal.humidity_min_pct - weather.relative_humidity_pct)
    return _clamp_int(100 - penalty)


def monitoring_recency(days_since_last_scan: int | None, is_expert_verified: bool = False) -> int:
    """Sub-index #3: data recency (Weight: 0.15).

    Starts at 100 minus recency penalty (5/day).
    Expert verified resolution achieves 95 (or 90).
    """
    if is_expert_verified:
        return c.MONITORING_RECENCY_EXPERT_VERIFIED
    if days_since_last_scan is None:
        return c.MONITORING_RECENCY_DEFAULT
    penalty = c.MONITORING_RECENCY_PENALTY_PER_DAY * days_since_last_scan
    return _clamp_int(100 - penalty)


def treatment_response(
    open_problems: list[OpenProblemInput],
    latest_followup_response: FollowupResponse | None,
    consecutive_got_worse_count: int,
    problem_resolved_with_confirmed_treatment: bool,
) -> int:
    """Sub-index #4: follow-up trend & treatment resolution (Weight: 0.20).

    - Neutral baseline (no active problems / baseline): 70
    - Follow-up "got worse": 40
    - Follow-up "no change": 50
    - Follow-up "improved": 90
    - Confirmed expert resolution: 95
    """
    if problem_resolved_with_confirmed_treatment:
        return c.TREATMENT_RESPONSE_CONFIRMED_RESOLVED
    if latest_followup_response == FollowupResponse.GOT_WORSE:
        return c.TREATMENT_RESPONSE_GOT_WORSE
    if latest_followup_response == FollowupResponse.IMPROVED:
        return c.TREATMENT_RESPONSE_IMPROVED
    if latest_followup_response == FollowupResponse.NO_CHANGE:
        return c.TREATMENT_RESPONSE_NO_CHANGE
    return c.TREATMENT_RESPONSE_DEFAULT


@dataclass(frozen=True)
class SubIndexBreakdown:
    """One row of the transparent score breakdown (contract §2.9)."""

    key: SubIndexKey
    value: int
    weight: float
    contribution: float


def compute_all_subindices(inputs: HealthScoreInputs) -> list[SubIndexBreakdown]:
    """Run all four calculators against ``inputs`` and return them in the
    fixed contract order, each carrying its weight and weighted contribution.
    """
    values: dict[SubIndexKey, int] = {
        SubIndexKey.ACTIVE_PROBLEM_SEVERITY: active_problem_severity(inputs.open_problems),
        SubIndexKey.ENVIRONMENTAL_RISK: environmental_risk(inputs.weather, inputs.crop_ideal),
        SubIndexKey.MONITORING_RECENCY: monitoring_recency(
            inputs.days_since_last_scan, inputs.is_expert_verified
        ),
        SubIndexKey.TREATMENT_RESPONSE: treatment_response(
            inputs.open_problems,
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
