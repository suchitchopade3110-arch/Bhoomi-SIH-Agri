"""Unit tests for the pure Farm Risk Score engine (SIH26131).

The centerpiece is ``test_sih26131_reconciliation`` — the acceptance test:
fixed inputs walking baseline 82 -> early stem borer 73 -> got_worse 57 -> resolved 91,
reproducing docs/specs/suchit_module_specs_sih26131.md §1.5 worked reconciliation exactly.
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
    active_problem_severity,
    environmental_risk,
    monitoring_recency,
    treatment_response,
)

# ---------------------------------------------------------------------------
# Shared fixture: samba paddy at vegetative stage.
# ---------------------------------------------------------------------------
IDEAL = CropIdealConditions(
    temp_min_c=25.0,
    temp_max_c=35.0,
    humidity_min_pct=60.0,
    humidity_max_pct=80.0,
)

# Weather reading that produces environmental_risk = 70 (30 penalty: 24% humidity excess @ 1.25/pct)
WEATHER_ENV_70 = WeatherReading(temp_c=30.0, relative_humidity_pct=104.0)


def _inputs(**overrides) -> HealthScoreInputs:
    base = dict(
        triggering_input=TriggeringInput(type="test"),
        weather=WEATHER_ENV_70,
        crop_ideal=IDEAL,
        open_problems=[],
        days_since_last_scan=6,
        latest_followup_response=None,
        consecutive_got_worse_count=0,
        problem_resolved_with_confirmed_treatment=False,
        has_interaction=True,
    )
    base.update(overrides)
    return HealthScoreInputs(**base)


# ---------------------------------------------------------------------------
# Constants sanity
# ---------------------------------------------------------------------------


def test_weights_sum_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_weights_match_sih26131():
    assert WEIGHTS[SubIndexKey.ACTIVE_PROBLEM_SEVERITY] == 0.40
    assert WEIGHTS[SubIndexKey.ENVIRONMENTAL_RISK] == 0.25
    assert WEIGHTS[SubIndexKey.MONITORING_RECENCY] == 0.15
    assert WEIGHTS[SubIndexKey.TREATMENT_RESPONSE] == 0.20


# ---------------------------------------------------------------------------
# band_for (PRD §7.5 / SIH26131)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "score,expected",
    [
        (None, HealthBand.UNRATED),
        (0, HealthBand.CRITICAL),
        (39, HealthBand.CRITICAL),
        (40, HealthBand.POOR),
        (57, HealthBand.POOR),
        (59, HealthBand.POOR),
        (60, HealthBand.WATCH),
        (73, HealthBand.WATCH),
        (74, HealthBand.WATCH),
        (75, HealthBand.GOOD),
        (82, HealthBand.GOOD),
        (89, HealthBand.GOOD),
        (90, HealthBand.EXCELLENT),
        (91, HealthBand.EXCELLENT),
        (100, HealthBand.EXCELLENT),
    ],
)
def test_band_for(score, expected):
    assert band_for(score) == expected


# ---------------------------------------------------------------------------
# Sub-index #1 — active_problem_severity
# ---------------------------------------------------------------------------


def test_active_problem_severity_no_problems():
    assert active_problem_severity([]) == 100


def test_active_problem_severity_single_early():
    assert active_problem_severity([OpenProblemInput(severity=ProblemSeverity.EARLY)]) == 70


def test_active_problem_severity_single_moderate():
    assert active_problem_severity([OpenProblemInput(severity=ProblemSeverity.MODERATE)]) == 45


def test_active_problem_severity_single_severe():
    assert active_problem_severity([OpenProblemInput(severity=ProblemSeverity.SEVERE)]) == 20


def test_active_problem_severity_floors_at_zero():
    problems = [OpenProblemInput(severity=ProblemSeverity.SEVERE) for _ in range(3)]
    assert active_problem_severity(problems) == 0


# ---------------------------------------------------------------------------
# Sub-index #2 — environmental_risk
# ---------------------------------------------------------------------------


def test_environmental_risk_within_ideal_band_scores_100():
    ideal = CropIdealConditions(20, 35, 50, 85)
    assert environmental_risk(WeatherReading(temp_c=28, relative_humidity_pct=70), ideal) == 100


def test_environmental_risk_penalizes_humidity_deviation():
    # 24 points humidity excess (1.25/pt) = 30 penalty -> 70
    assert environmental_risk(WeatherReading(temp_c=30, relative_humidity_pct=104), IDEAL) == 70


def test_environmental_risk_penalizes_temp_deviation():
    # 5 degrees temp excess (2.0/pt) = 10 penalty -> 90
    assert environmental_risk(WeatherReading(temp_c=40, relative_humidity_pct=75), IDEAL) == 90


# ---------------------------------------------------------------------------
# Sub-index #3 — monitoring_recency
# ---------------------------------------------------------------------------


def test_monitoring_recency_fresh_scan():
    assert monitoring_recency(days_since_last_scan=0) == 100


def test_monitoring_recency_recent_scan():
    assert monitoring_recency(days_since_last_scan=2) == 90


def test_monitoring_recency_stale_scan():
    assert monitoring_recency(days_since_last_scan=6) == 70


def test_monitoring_recency_resolved_scan():
    assert monitoring_recency(days_since_last_scan=1) == 95


def test_monitoring_recency_expert_verified():
    assert monitoring_recency(days_since_last_scan=None, is_expert_verified=True) == 90


# ---------------------------------------------------------------------------
# Sub-index #4 — treatment_response
# ---------------------------------------------------------------------------


def test_treatment_response_baseline():
    assert treatment_response([], None, 0, False) == 70


def test_treatment_response_got_worse():
    assert treatment_response([OpenProblemInput(severity=ProblemSeverity.MODERATE)], FollowupResponse.GOT_WORSE, 1, False) == 40


def test_treatment_response_no_change():
    assert treatment_response([OpenProblemInput(severity=ProblemSeverity.EARLY)], FollowupResponse.NO_CHANGE, 0, False) == 50


def test_treatment_response_improved():
    assert treatment_response([], FollowupResponse.IMPROVED, 0, False) == 90


def test_treatment_response_confirmed_resolution():
    assert treatment_response([], FollowupResponse.GOT_WORSE, 3, True) == 95


# ---------------------------------------------------------------------------
# compute_health: determinism and the Unrated sentinel.
# ---------------------------------------------------------------------------


def test_compute_health_is_deterministic():
    inputs = _inputs(
        weather=WeatherReading(temp_c=31.5, relative_humidity_pct=88.0),
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


def test_compute_health_unrated_when_no_interactions():
    inputs = _inputs(has_interaction=False)
    result = compute_health(inputs)
    assert result.score is None
    assert result.band == HealthBand.UNRATED
    assert result.subindices == []
    assert "interactions" in result.missing_fields


def test_compute_health_unrated_is_not_zero():
    """Day 0 must never be conflated with a genuinely bad score of 0."""
    unrated = compute_health(_inputs(weather=None))
    zero_score_problems = [OpenProblemInput(severity=ProblemSeverity.SEVERE) for _ in range(3)]
    critical = compute_health(_inputs(open_problems=zero_score_problems))
    assert unrated.score is None
    assert unrated.band == HealthBand.UNRATED
    assert critical.score is not None
    assert critical.band != HealthBand.UNRATED


def test_compute_health_clamps_to_0_100():
    problems = [OpenProblemInput(severity=ProblemSeverity.SEVERE) for _ in range(5)]
    result = compute_health(_inputs(open_problems=problems))
    assert 0 <= result.score <= 100


# ---------------------------------------------------------------------------
# THE ACCEPTANCE TEST — SIH26131 worked reconciliation (82 -> 73 -> 57 -> 91)
# ---------------------------------------------------------------------------


def test_sih26131_reconciliation():
    """Walks baseline 82 -> early stem borer 73 -> got_worse 57 -> resolved 91 with
    fixed fixture inputs, matching docs/specs/suchit_module_specs_sih26131.md §1.5.
    """
    # --- 1. Baseline: Day 0 onboarding scan, no open problems (82) ---
    baseline_inputs = _inputs(
        triggering_input=TriggeringInput(type="baseline_calibration"),
        open_problems=[],
        days_since_last_scan=6,  # monitoring: 100 - 6*5 = 70 -> 10.5
        latest_followup_response=None,
    )
    baseline = compute_health(baseline_inputs)
    assert baseline.score == 82
    assert baseline.band == HealthBand.GOOD
    assert [s.contribution for s in baseline.subindices] == [40.0, 17.5, 10.5, 14.0]

    # --- 2. Diagnosis: Early Stem Borer detected (-30 penalty) (73) ---
    diagnosed_inputs = _inputs(
        triggering_input=TriggeringInput(
            type="diagnosis", details={"problem_id": "p_7", "severity": "early"}
        ),
        open_problems=[OpenProblemInput(severity=ProblemSeverity.EARLY)],  # active_prob: 70 -> 28.0
        days_since_last_scan=2,  # monitoring: 100 - 2*5 = 90 -> 13.5
        latest_followup_response=None,
    )
    diagnosed = compute_health(diagnosed_inputs)
    assert diagnosed.score == 73
    assert diagnosed.band == HealthBand.WATCH
    assert [s.contribution for s in diagnosed.subindices] == [28.0, 17.5, 13.5, 14.0]

    # --- 3. Follow-up "Got Worse" -> moderate severity + negative trend (57) ---
    worse_inputs = _inputs(
        triggering_input=TriggeringInput(
            type="followup", details={"problem_id": "p_7", "response": "got_worse"}
        ),
        open_problems=[OpenProblemInput(severity=ProblemSeverity.MODERATE)],  # active_prob: 45 -> 18.0
        days_since_last_scan=2,  # monitoring: 90 -> 13.5
        latest_followup_response=FollowupResponse.GOT_WORSE,  # treat_resp: 40 -> 8.0
        consecutive_got_worse_count=1,
    )
    worse = compute_health(worse_inputs)
    assert worse.score == 57
    assert worse.band == HealthBand.POOR  # auto-escalation trigger
    assert [s.contribution for s in worse.subindices] == [18.0, 17.5, 13.5, 8.0]

    # --- 4. Expert resolves the case: problem cleared, verified recovery (91) ---
    resolved_inputs = _inputs(
        triggering_input=TriggeringInput(type="case_resolution", details={"problem_id": "p_7"}),
        open_problems=[],  # active_prob: 100 -> 40.0
        days_since_last_scan=1,  # monitoring: 95 -> 14.25
        latest_followup_response=FollowupResponse.GOT_WORSE,
        consecutive_got_worse_count=1,
        problem_resolved_with_confirmed_treatment=True,  # treat_resp: 95 -> 19.0
    )
    resolved = compute_health(resolved_inputs)
    assert resolved.score == 91
    assert resolved.band == HealthBand.EXCELLENT  # 90.75 rounds to 91
    assert [s.contribution for s in resolved.subindices] == [40.0, 17.5, 14.25, 19.0]

    # Every movement is traceable to its triggering input (audit trail).
    assert diagnosed.triggering_input.type == "diagnosis"
    assert worse.triggering_input.details["response"] == "got_worse"
    assert resolved.triggering_input.type == "case_resolution"

    # Active problem severity sub-index arc: 100 -> 70 -> 45 -> 100.
    def problem_severity_value(result):
        return next(s.value for s in result.subindices if s.key == SubIndexKey.ACTIVE_PROBLEM_SEVERITY)

    assert problem_severity_value(baseline) == 100
    assert problem_severity_value(diagnosed) == 70
    assert problem_severity_value(worse) == 45
    assert problem_severity_value(resolved) == 100
