"""Phase 3: pure hybrid trigger evaluator (app/domain/alerts/evaluate.py).

SPEC-ALERT-001 §2.2's decision matrix, §4's determinism contract, §6's
cooldown durations — all exercised with no DB, no clock.
"""

from datetime import datetime, timezone

from app.domain.alerts.evaluate import evaluate_alert
from app.domain.alerts.models import AlertSeverity, AlertTarget, ClusterCase, DeliveryChannel, WeatherMetrics
from app.domain.alerts.thresholds import PATHOGEN_RISK_THRESHOLDS

BLB = PATHOGEN_RISK_THRESHOLDS["bacterial_leaf_blight"]
NOW = datetime(2026, 8, 24, 6, 0, 0, tzinfo=timezone.utc)

FAVORABLE_WEATHER = WeatherMetrics(avg_temp_c=28.0, avg_humidity_pct=84.0, sustained_hours=48)
UNFAVORABLE_WEATHER = WeatherMetrics(avg_temp_c=20.0, avg_humidity_pct=40.0, sustained_hours=10)

NO_CLUSTER: list[ClusterCase] = []
TRIGGERING_CLUSTER = [ClusterCase(label="bacterial_leaf_blight", severity="moderate", case_count=3, min_distance_km=5.0)]
SUB_THRESHOLD_CLUSTER = [
    ClusterCase(label="bacterial_leaf_blight", severity="early", case_count=1, min_distance_km=5.0)
]


def _evaluate(weather, cluster, farm_id="f_123", district="Erode", crop="samba_paddy", growth_stage="vegetative"):
    return evaluate_alert(
        farm_id=farm_id,
        district=district,
        crop=crop,
        growth_stage=growth_stage,
        weather=weather,
        cluster_summary=cluster,
        threshold=BLB,
        evaluated_at=NOW,
    )


def test_no_weather_no_cluster_returns_none():
    assert _evaluate(UNFAVORABLE_WEATHER, NO_CLUSTER) is None


def test_weather_only_yields_advisory():
    draft = _evaluate(FAVORABLE_WEATHER, NO_CLUSTER)
    assert draft is not None
    assert draft.severity == AlertSeverity.ADVISORY


def test_cluster_only_yields_warning():
    draft = _evaluate(UNFAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert draft is not None
    assert draft.severity == AlertSeverity.WARNING


def test_weather_and_cluster_yields_emergency():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert draft is not None
    assert draft.severity == AlertSeverity.EMERGENCY


def test_sub_threshold_cluster_count_does_not_trigger_cluster_tier():
    draft = _evaluate(UNFAVORABLE_WEATHER, SUB_THRESHOLD_CLUSTER)
    assert draft is None


def test_cluster_cases_for_a_different_pathogen_dont_count():
    other_pathogen_cluster = [ClusterCase(label="powdery_mildew", severity="moderate", case_count=5, min_distance_km=2.0)]
    assert _evaluate(UNFAVORABLE_WEATHER, other_pathogen_cluster) is None


def test_unsusceptible_growth_stage_returns_none_even_with_both_triggers():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER, growth_stage="late_season")
    assert draft is None


def test_wrong_crop_returns_none():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER, crop="cotton")
    assert draft is None


def test_deterministic_output_for_identical_inputs():
    draft1 = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    draft2 = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert draft1 == draft2


def test_alert_id_is_deterministic_uuid5():
    draft1 = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    draft2 = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert draft1.alert_id == draft2.alert_id
    # Different evaluated_at date -> different alert_id (new day, fresh alert).
    from datetime import timedelta

    later = evaluate_alert(
        farm_id="f_123",
        district="Erode",
        crop="samba_paddy",
        growth_stage="vegetative",
        weather=FAVORABLE_WEATHER,
        cluster_summary=TRIGGERING_CLUSTER,
        threshold=BLB,
        evaluated_at=NOW + timedelta(days=1),
    )
    assert later.alert_id != draft1.alert_id


def test_cooldown_key_uses_farm_id_when_present():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER, farm_id="f_123")
    assert draft.cooldown_key == "f_123:bacterial_leaf_blight:emergency"


def test_cooldown_key_uses_district_for_regional_broadcast():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER, farm_id=None)
    assert draft.cooldown_key == "Erode:bacterial_leaf_blight:emergency"
    assert draft.target == AlertTarget.REGIONAL_BROADCAST
    assert draft.farm_id is None


def test_per_farm_target_when_farm_id_given():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER, farm_id="f_123")
    assert draft.target == AlertTarget.PER_FARM


def test_expiry_matches_severity_cooldown_hours():
    emergency = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert (emergency.expires_at - emergency.created_at).total_seconds() == 24 * 3600

    advisory = _evaluate(FAVORABLE_WEATHER, NO_CLUSTER)
    assert (advisory.expires_at - advisory.created_at).total_seconds() == 72 * 3600

    warning = _evaluate(UNFAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert (warning.expires_at - warning.created_at).total_seconds() == 48 * 3600


def test_emergency_and_warning_include_push_advisory_does_not():
    emergency = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    warning = _evaluate(UNFAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    advisory = _evaluate(FAVORABLE_WEATHER, NO_CLUSTER)

    assert DeliveryChannel.PUSH_NOTIFICATION in emergency.delivery_channels
    assert DeliveryChannel.PUSH_NOTIFICATION in warning.delivery_channels
    assert DeliveryChannel.PUSH_NOTIFICATION not in advisory.delivery_channels


def test_created_at_is_the_injected_evaluated_at_never_wall_clock():
    draft = _evaluate(FAVORABLE_WEATHER, TRIGGERING_CLUSTER)
    assert draft.created_at == NOW


def test_inspection_tasks_propagated_from_threshold_and_never_empty():
    """Phase 3 'never cut' item: every issued AlertDraft carries the
    threshold's corpus-sourced inspection tasks."""
    for weather, cluster in [
        (FAVORABLE_WEATHER, NO_CLUSTER),
        (UNFAVORABLE_WEATHER, TRIGGERING_CLUSTER),
        (FAVORABLE_WEATHER, TRIGGERING_CLUSTER),
    ]:
        draft = _evaluate(weather, cluster)
        assert draft is not None
        assert len(draft.inspection_tasks) >= 1
        assert draft.inspection_tasks == BLB.inspection_tasks
