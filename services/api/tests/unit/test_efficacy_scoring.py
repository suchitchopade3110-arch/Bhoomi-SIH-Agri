"""Phase 4: pure treatment-efficacy scoring engine
(app/domain/efficacy/score.py). SPEC-EFFICACY-001 §5.2's Stage B contract.
"""

from datetime import date, timedelta

from app.domain.efficacy.models import TreatmentApplicationSnapshot
from app.domain.efficacy.score import compute_efficacy

TREATMENT = "copper_hydroxide_77_wp"
PATHOGEN = "bacterial_leaf_blight"
CROP = "samba_paddy"
DISTRICT = "Erode"
AS_OF = date(2026, 8, 24)


def _app(
    outcome,
    *,
    app_id="a",
    applied_on=None,
    followups=1,
    days_to_resolution=4,
    got_worse=False,
    escalated=False,
    treatment_name=TREATMENT,
    pathogen_type=PATHOGEN,
    crop=CROP,
    district=DISTRICT,
) -> TreatmentApplicationSnapshot:
    return TreatmentApplicationSnapshot(
        id=app_id,
        pathogen_type=pathogen_type,
        treatment_name=treatment_name,
        crop=crop,
        district=district,
        applied_on=applied_on or (AS_OF - timedelta(days=10)),
        final_outcome=outcome,
        followups_to_resolution=followups,
        days_to_resolution=days_to_resolution,
        failed_on_got_worse=got_worse,
        escalated_for_expert=escalated,
    )


def _compute(applications, as_of=AS_OF, **kwargs):
    return compute_efficacy(
        treatment_name=TREATMENT,
        pathogen_type=PATHOGEN,
        crop=CROP,
        district=DISTRICT,
        applications=applications,
        as_of=as_of,
        **kwargs,
    )


def test_eight_of_ten_successes_is_80_percent():
    apps = [_app("improved", app_id=f"s{i}") for i in range(8)] + [
        _app("failed", app_id=f"f{i}", got_worse=True) for i in range(2)
    ]
    result = _compute(apps)
    assert result.status == "statistically_significant"
    assert result.sample_size == 10
    assert result.efficacy_percentage == 80.0


def test_floor_boundary_nine_is_insufficient_ten_is_significant():
    nine = [_app("improved", app_id=f"a{i}") for i in range(9)]
    result_nine = _compute(nine)
    assert result_nine.status == "insufficient_data"
    assert result_nine.sample_size == 9
    assert result_nine.efficacy_percentage is None
    assert result_nine.avg_days_to_recovery is None

    ten = nine + [_app("improved", app_id="a9")]
    result_ten = _compute(ten)
    assert result_ten.status == "statistically_significant"
    assert result_ten.sample_size == 10
    assert result_ten.efficacy_percentage == 100.0


def test_applications_outside_trailing_window_excluded():
    in_window = [_app("improved", app_id=f"a{i}", applied_on=AS_OF - timedelta(days=10)) for i in range(10)]
    out_of_window = [
        _app("improved", app_id=f"old{i}", applied_on=AS_OF - timedelta(days=400)) for i in range(20)
    ]
    result = _compute(in_window + out_of_window)
    assert result.sample_size == 10  # the 20 stale ones never counted


def test_superseded_and_null_outcome_excluded_from_n_total():
    counted = [_app("improved", app_id=f"a{i}") for i in range(10)]
    excluded = [_app("superseded", app_id="sup1")] + [_app(None, app_id="null1")]
    result = _compute(counted + excluded)
    assert result.sample_size == 10  # excluded ones don't inflate N_total


def test_precautionary_escalation_that_resolved_counts_as_success():
    apps = [
        _app("improved", app_id=f"a{i}", escalated=(i == 0)) for i in range(10)
    ]
    result = _compute(apps)
    assert result.status == "statistically_significant"
    assert result.efficacy_percentage == 100.0  # escalated-but-resolved still a success


def test_failed_on_got_worse_counts_as_failure_even_with_improved_outcome_never_set():
    apps = [_app("improved", app_id=f"s{i}") for i in range(9)] + [
        _app(None, app_id="w1", got_worse=True)
    ]
    result = _compute(apps)
    assert result.status == "statistically_significant"
    assert result.sample_size == 10
    assert result.efficacy_percentage == 90.0


def test_more_than_two_followups_without_improvement_excluded_not_a_success():
    # final_outcome="improved" but followups_to_resolution > 2 fails spec
    # §4.1's explicit success guard ("followups_to_resolution <= 2") — and
    # it isn't a failure either (failed_on_got_worse=False, final_outcome
    # != "failed"), so it's excluded from N_total entirely, same as a
    # superseded/NULL application.
    ten_successes = [_app("improved", app_id=f"s{i}") for i in range(10)]
    borderline = _app("improved", app_id="stalled", followups=3)
    result = _compute(ten_successes + [borderline])
    assert result.sample_size == 10  # the borderline one doesn't count
    assert result.efficacy_percentage == 100.0


def test_avg_days_to_recovery_averages_only_successes():
    apps = [_app("improved", app_id=f"s{i}", days_to_resolution=4) for i in range(5)] + [
        _app("improved", app_id=f"s2_{i}", days_to_resolution=6) for i in range(5)
    ]
    result = _compute(apps)
    assert result.avg_days_to_recovery == 5.0


def test_wrong_treatment_pathogen_crop_or_district_excluded_defensively():
    matching = [_app("improved", app_id=f"a{i}") for i in range(10)]
    noise = [
        _app("improved", app_id="wrong_treatment", treatment_name="other_treatment"),
        _app("improved", app_id="wrong_pathogen", pathogen_type="other_pathogen"),
        _app("improved", app_id="wrong_crop", crop="cotton"),
        _app("improved", app_id="wrong_district", district="Madurai"),
    ]
    result = _compute(matching + noise)
    assert result.sample_size == 10


def test_deterministic_for_identical_inputs():
    apps = [_app("improved", app_id=f"a{i}") for i in range(8)] + [
        _app("failed", app_id=f"f{i}", got_worse=True) for i in range(2)
    ]
    result1 = _compute(apps)
    result2 = _compute(apps)
    assert result1 == result2


def test_no_wall_clock_read_result_stable_regardless_of_when_test_runs():
    # If compute_efficacy ever called date.today() instead of using as_of,
    # this would be flaky depending on the actual calendar date.
    apps = [_app("improved", app_id=f"a{i}", applied_on=date(2020, 1, 1)) for i in range(10)]
    result = _compute(apps, as_of=date(2020, 6, 1), window_days=365)
    assert result.status == "statistically_significant"
    assert result.sample_size == 10
