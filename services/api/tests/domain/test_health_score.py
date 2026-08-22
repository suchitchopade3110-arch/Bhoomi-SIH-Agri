"""Unit tests for the pure Farm Health Score engine (PRD §7).

The centerpiece is ``test_prd_7_4_reconciliation`` — the acceptance test:
fixed inputs walking baseline 82 -> early BLB 68 -> got_worse 59 -> resolved
86, reproducing PRD §7.4's worked example exactly (the 59 point also matches
the contract's own §2.12 follow-up and §2.13 case-resolution JSON examples).
"""

import pytest

from app.core.enums import FollowupResponse, HealthBand, ProblemSeverity, SubIndexKey
from app.domain.health.constants import WEIGHTS
from app.domain.health.inputs import (
    CropIdealConditions,
    HealthScoreInputs,
    OpenProblemInput,
    TriggeringInput,
    WeatherReading,
)
from app.domain.health.score import band_for, compute_health
from app.domain.health.subindices import (
    active_problem_load,
    crop_stage_progression,
    environmental_suitability,
    monitoring_recency,
    resource_adequacy,
    treatment_response,
)

# ---------------------------------------------------------------------------
# Shared fixture: samba paddy at vegetative stage, matching PRD §6's scenario.
# ---------------------------------------------------------------------------
IDEAL = CropIdealConditions(
    temp_min_c=25.0,
    temp_max_c=35.0,
    humidity_min_pct=60.0,
    humidity_max_pct=80.0,
    soil_moisture_min_pct=65.0,
)


def _inputs(**overrides) -> HealthScoreInputs:
    base = dict(
        triggering_input=TriggeringInput(type="test"),
        weather=WeatherReading(temp_c=30.0, relative_humidity_pct=80.0),
        crop_ideal=IDEAL,
        soil_moisture_pct=55.0,
        irrigation_delivered_mm=24.0,
        irrigation_required_mm=40.0,
        days_since_planting=10,
        expected_stage_day=30,
        open_problems=[],
        days_since_last_scan=2,
        latest_followup_response=None,
        consecutive_got_worse_count=0,
        problem_resolved_with_confirmed_treatment=False,
    )
    base.update(overrides)
    return HealthScoreInputs(**base)


# ---------------------------------------------------------------------------
# Constants sanity
# ---------------------------------------------------------------------------


def test_weights_sum_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_weights_match_prd_7_2():
    assert WEIGHTS[SubIndexKey.ENVIRONMENTAL_SUITABILITY] == 0.20
    assert WEIGHTS[SubIndexKey.RESOURCE_ADEQUACY] == 0.15
    assert WEIGHTS[SubIndexKey.CROP_STAGE_PROGRESSION] == 0.15
    assert WEIGHTS[SubIndexKey.ACTIVE_PROBLEM_LOAD] == 0.30
    assert WEIGHTS[SubIndexKey.MONITORING_RECENCY] == 0.10
    assert WEIGHTS[SubIndexKey.TREATMENT_RESPONSE] == 0.10


# ---------------------------------------------------------------------------
# band_for (PRD §7.5)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "score,expected",
    [
        (None, HealthBand.UNRATED),
        (0, HealthBand.CRITICAL),
        (39, HealthBand.CRITICAL),
        (40, HealthBand.POOR),
        (59, HealthBand.POOR),
        (60, HealthBand.WATCH),
        (74, HealthBand.WATCH),
        (75, HealthBand.GOOD),
        (89, HealthBand.GOOD),
        (90, HealthBand.EXCELLENT),
        (100, HealthBand.EXCELLENT),
    ],
)
def test_band_for(score, expected):
    assert band_for(score) == expected


# ---------------------------------------------------------------------------
# Sub-index #4 — active_problem_load (PRD §7.3), the formula the spec pins down exactly.
# ---------------------------------------------------------------------------


def test_active_problem_load_no_problems():
    assert active_problem_load([]) == 100


def test_active_problem_load_single_early():
    assert active_problem_load([OpenProblemInput(severity=ProblemSeverity.EARLY)]) == 70


def test_active_problem_load_single_moderate():
    assert active_problem_load([OpenProblemInput(severity=ProblemSeverity.MODERATE)]) == 45


def test_active_problem_load_single_severe():
    assert active_problem_load([OpenProblemInput(severity=ProblemSeverity.SEVERE)]) == 20


def test_active_problem_load_floors_at_zero():
    problems = [OpenProblemInput(severity=ProblemSeverity.SEVERE) for _ in range(3)]
    assert active_problem_load(problems) == 0


# ---------------------------------------------------------------------------
# The other five sub-indices, each with a fixed-input example.
# ---------------------------------------------------------------------------


def test_environmental_suitability_within_ideal_band_scores_100():
    ideal = CropIdealConditions(20, 35, 50, 85, 60)
    assert environmental_suitability(WeatherReading(temp_c=28, relative_humidity_pct=70), ideal, soil_moisture_pct=65) == 100


def test_environmental_suitability_penalizes_humidity_and_soil_deficit():
    # 12 points humidity excess (1.25/pt) + 10 points soil deficit (2.0/pt) = 35 penalty
    assert environmental_suitability(WeatherReading(temp_c=30, relative_humidity_pct=92), IDEAL, soil_moisture_pct=55) == 65


def test_resource_adequacy_full_delivery():
    assert resource_adequacy(40.0, 40.0) == 100


def test_resource_adequacy_partial_delivery():
    assert resource_adequacy(24.0, 40.0) == 60


def test_crop_stage_progression_on_schedule():
    assert crop_stage_progression(days_since_planting=30, expected_stage_day=30) == 100


def test_crop_stage_progression_penalizes_deviation():
    assert crop_stage_progression(days_since_planting=10, expected_stage_day=30) == 60


def test_monitoring_recency_fresh_scan():
    assert monitoring_recency(days_since_last_scan=0) == 100


def test_monitoring_recency_stale_scan():
    assert monitoring_recency(days_since_last_scan=6) == 70


def test_treatment_response_no_followup_yet_is_below_max():
    assert treatment_response([], None, 0, False) == 70
    assert treatment_response([OpenProblemInput(severity=ProblemSeverity.EARLY)], None, 0, False) == 20


def test_treatment_response_improved():
    assert treatment_response([], FollowupResponse.IMPROVED, 0, False) == 100


def test_treatment_response_got_worse_steps_down():
    assert treatment_response([OpenProblemInput(severity=ProblemSeverity.MODERATE)], FollowupResponse.GOT_WORSE, 1, False) == 5


def test_treatment_response_confirmed_resolution_is_always_max():
    assert treatment_response([], FollowupResponse.GOT_WORSE, 3, True) == 90


# ---------------------------------------------------------------------------
# compute_health: determinism and the Unrated sentinel.
# ---------------------------------------------------------------------------


def test_compute_health_is_deterministic():
    inputs = _inputs(
        weather=WeatherReading(temp_c=31.5, relative_humidity_pct=88.0),
        soil_moisture_pct=52.0,
        irrigation_delivered_mm=45.0,
        irrigation_required_mm=50.0,
        days_since_planting=42,
        days_since_last_scan=3,
        open_problems=[OpenProblemInput(severity=ProblemSeverity.MODERATE)],
        latest_followup_response=FollowupResponse.GOT_WORSE,
        consecutive_got_worse_count=1,
    )
    res1 = compute_health(inputs)
    res2 = compute_health(inputs)
    assert res1 == res2
    assert res1.score == res2.score
    assert res1.band == res2.band
    assert res1.subindices == res2.subindices
    assert res1.missing_fields == res2.missing_fields


def test_compute_health_unrated_when_required_input_missing():
    inputs = _inputs(weather=None)
    result = compute_health(inputs)
    assert result.score is None
    assert result.band == HealthBand.UNRATED
    assert result.subindices == []
    assert "weather" in result.missing_fields


def test_compute_health_unrated_is_not_zero():
    """Day 0 must never be conflated with a genuinely bad score of 0 (PRD §7.1)."""
    unrated = compute_health(_inputs(soil_moisture_pct=None))
    zero_score_problems = [OpenProblemInput(severity=ProblemSeverity.SEVERE) for _ in range(3)]
    critical = compute_health(_inputs(open_problems=zero_score_problems))
    assert unrated.score is None
    assert unrated.band == HealthBand.UNRATED
    assert critical.score is not None
    assert critical.band != HealthBand.UNRATED


def test_compute_health_clamps_to_0_100():
    problems = [OpenProblemInput(severity=ProblemSeverity.SEVERE) for _ in range(5)]
    result = compute_health(_inputs(open_problems=problems, irrigation_delivered_mm=0.0))
    assert 0 <= result.score <= 100


# ---------------------------------------------------------------------------
# THE ACCEPTANCE TEST — PRD §7.4's worked reconciliation, exactly.
# ---------------------------------------------------------------------------


def test_prd_7_4_reconciliation():
    """Walks baseline 82 -> early BLB 68 -> got_worse 59 -> resolved 86 with
    fixed fixture inputs, matching PRD §7.4 single source of truth table.
    """
    # --- Baseline: no active problems, ordinary real-world imperfection (82) ---
    baseline_inputs = _inputs(
        triggering_input=TriggeringInput(type="baseline_calibration"),
        soil_moisture_pct=53.0,  # env: 76 -> 15.2
        irrigation_delivered_mm=32.0,  # resource: 80 -> 12.0
        irrigation_required_mm=40.0,
        days_since_planting=17,  # stage: 74 -> 11.1
        expected_stage_day=30,
        days_since_last_scan=6,  # monitoring: 70 -> 7.0 (100 - 6*5)
    )
    baseline = compute_health(baseline_inputs)
    assert baseline.score == 82
    assert baseline.band == HealthBand.GOOD
    assert [s.contribution for s in baseline.subindices] == [15.2, 12.0, 11.1, 30.0, 7.0, 7.0]

    # --- Day 22: early Bacterial Leaf Blight diagnosed (68) ---
    diagnosed_inputs = _inputs(
        triggering_input=TriggeringInput(
            type="diagnosis", details={"problem_id": "p_7", "severity": "early"}
        ),
        soil_moisture_pct=53.0,
        irrigation_delivered_mm=32.0,
        irrigation_required_mm=40.0,
        days_since_planting=17,
        expected_stage_day=30,
        open_problems=[OpenProblemInput(severity=ProblemSeverity.EARLY)],
        days_since_last_scan=6,
    )
    diagnosed = compute_health(diagnosed_inputs)
    assert diagnosed.score == 68
    assert diagnosed.band == HealthBand.WATCH
    assert [s.contribution for s in diagnosed.subindices] == [15.2, 12.0, 11.1, 21.0, 7.0, 2.0]

    # --- Day 25: follow-up reports "Got Worse" -> severity promotes to moderate (59) ---
    worse_inputs = _inputs(
        triggering_input=TriggeringInput(
            type="followup", details={"problem_id": "p_7", "response": "got_worse"}
        ),
        soil_moisture_pct=53.0,
        irrigation_delivered_mm=32.0,
        irrigation_required_mm=40.0,
        days_since_planting=17,
        expected_stage_day=30,
        open_problems=[OpenProblemInput(severity=ProblemSeverity.MODERATE)],
        days_since_last_scan=6,
        latest_followup_response=FollowupResponse.GOT_WORSE,
        consecutive_got_worse_count=1,
    )
    worse = compute_health(worse_inputs)
    assert worse.score == 59
    assert worse.band == HealthBand.POOR  # auto-escalation trigger
    assert [s.contribution for s in worse.subindices] == [15.2, 12.0, 11.1, 13.5, 7.0, 0.5]

    # --- Expert resolves the case: problem clears, treatment confirmed successful (86) ---
    resolved_inputs = _inputs(
        triggering_input=TriggeringInput(type="case_resolution", details={"problem_id": "p_7"}),
        soil_moisture_pct=53.0,
        irrigation_delivered_mm=32.0,
        irrigation_required_mm=40.0,
        days_since_planting=17,
        expected_stage_day=30,
        open_problems=[],
        days_since_last_scan=0,
        is_expert_verified=True,
        latest_followup_response=FollowupResponse.GOT_WORSE,
        consecutive_got_worse_count=1,
        problem_resolved_with_confirmed_treatment=True,
    )
    resolved = compute_health(resolved_inputs)
    assert resolved.score == 86
    assert resolved.band == HealthBand.GOOD  # lands above original baseline (+4)
    assert [s.contribution for s in resolved.subindices] == [15.2, 12.0, 11.1, 30.0, 9.0, 9.0]

    # Every movement is traceable to its triggering input (PRD §7.1 audit trail).
    assert diagnosed.triggering_input.type == "diagnosis"
    assert worse.triggering_input.details["response"] == "got_worse"
    assert resolved.triggering_input.type == "case_resolution"

    # The active-problem-load sub-index alone should show the 100 -> 70 -> 45 -> 100
    # arc PRD §7.3 describes.
    def problem_load_value(result):
        return next(s.value for s in result.subindices if s.key == SubIndexKey.ACTIVE_PROBLEM_LOAD)

    assert problem_load_value(baseline) == 100
    assert problem_load_value(diagnosed) == 70
    assert problem_load_value(worse) == 45
    assert problem_load_value(resolved) == 100
