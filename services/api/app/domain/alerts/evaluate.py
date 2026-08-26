"""Pure hybrid meteorological-geospatial trigger evaluator (spec §2, §4).

No I/O, no ``datetime.now()``, no random IDs: the caller (``AlertService``)
assembles ``WeatherMetrics``/``ClusterCase`` rows and passes an injected
``evaluated_at`` — same inputs always produce a byte-identical
``AlertDraft`` (or ``None``), including the deterministic ``alert_id``
(spec §4.1's UUIDv5 formula).
"""

from datetime import datetime, timedelta
from uuid import NAMESPACE_URL, uuid5

from app.domain.alerts.models import (
    AlertDraft,
    AlertSeverity,
    AlertTarget,
    ClusterCase,
    DeliveryChannel,
    PathogenRiskThreshold,
    WeatherMetrics,
)

# Fixed namespace for deterministic alert_id generation (spec §4.1) — a
# constant UUID, not derived from anything request-specific.
NAMESPACE_BHOOMI_ALERTS = uuid5(NAMESPACE_URL, "bhoomi.alerts")

# Cooldown durations by severity (spec §6) — how long an alert of this
# severity suppresses a duplicate at the same cooldown_key.
_COOLDOWN_HOURS: dict[AlertSeverity, int] = {
    AlertSeverity.INFO: 72,
    AlertSeverity.ADVISORY: 72,
    AlertSeverity.WARNING: 48,
    AlertSeverity.EMERGENCY: 24,
}

_EMERGENCY_CHANNELS = (DeliveryChannel.PUSH_NOTIFICATION, DeliveryChannel.HOME_BANNER, DeliveryChannel.VOICE_BRIEFING)
_WARNING_CHANNELS = (DeliveryChannel.PUSH_NOTIFICATION, DeliveryChannel.HOME_BANNER, DeliveryChannel.VOICE_BRIEFING)
# INFO/ADVISORY skip push to avoid alert fatigue on general-vigilance
# notices (spec §2.2's own "crying wolf" rationale) — surfaced passively.
_ADVISORY_CHANNELS = (DeliveryChannel.HOME_BANNER, DeliveryChannel.VOICE_BRIEFING)


def _weather_favorable(weather: WeatherMetrics, threshold: PathogenRiskThreshold) -> bool:
    return (
        threshold.temp_min_c <= weather.avg_temp_c <= threshold.temp_max_c
        and weather.avg_humidity_pct >= threshold.humidity_min_pct
        and weather.sustained_hours >= threshold.sustained_hours
    )


def _cluster_case_count(cluster_summary: list[ClusterCase], pathogen_id: str) -> int:
    return sum(c.case_count for c in cluster_summary if c.label == pathogen_id)


def _classify_severity(
    weather_favorable: bool,
    cluster_triggered: bool,
    seasonal_triggered: bool = False,
) -> AlertSeverity | None:
    """Spec §2.2's decision matrix with 4th seasonal susceptibility trigger tier."""
    if cluster_triggered and weather_favorable:
        return AlertSeverity.EMERGENCY
    if cluster_triggered:
        return AlertSeverity.WARNING
    if weather_favorable:
        return AlertSeverity.ADVISORY
    if seasonal_triggered:
        return AlertSeverity.INFO
    return None


def _delivery_channels(severity: AlertSeverity) -> tuple[DeliveryChannel, ...]:
    if severity == AlertSeverity.EMERGENCY:
        return _EMERGENCY_CHANNELS
    if severity == AlertSeverity.WARNING:
        return _WARNING_CHANNELS
    return _ADVISORY_CHANNELS


def evaluate_alert(
    *,
    farm_id: str | None,
    district: str,
    crop: str,
    growth_stage: str,
    weather: WeatherMetrics,
    cluster_summary: list[ClusterCase],
    threshold: PathogenRiskThreshold,
    evaluated_at: datetime,
    seasonal_triggered: bool = False,
) -> AlertDraft | None:
    """Evaluate one pathogen's hybrid trigger for one farm (or district
    broadcast, when ``farm_id`` is ``None``) at ``evaluated_at``.

    Returns ``None`` when the crop/stage isn't susceptible or none of the
    weather, cluster, or seasonal tiers fire — no alert, not a suppressed one
    (cooldown suppression is a separate, service-level concern, spec §4.2).
    """
    if crop != threshold.target_crop or growth_stage not in threshold.susceptible_stages:
        return None

    weather_favorable = _weather_favorable(weather, threshold)
    cluster_case_count = _cluster_case_count(cluster_summary, threshold.pathogen_id)
    cluster_triggered = cluster_case_count >= threshold.cluster_count_threshold

    severity = _classify_severity(weather_favorable, cluster_triggered, seasonal_triggered)
    if severity is None:
        return None

    reason_parts = []
    if weather_favorable:
        reason_parts.append(
            f"Favorable conditions for {threshold.pathogen_name} "
            f"(RH {weather.avg_humidity_pct:.0f}%, {weather.avg_temp_c:.0f}°C, "
            f"sustained {weather.sustained_hours}h)"
        )
    if cluster_triggered:
        reason_parts.append(
            f"{cluster_case_count} confirmed case(s) within {threshold.cluster_radius_km:.0f}km "
            f"over the past 7 days"
        )
    if not reason_parts and seasonal_triggered:
        reason_parts.append(
            f"Seasonal susceptibility window: {crop} in '{growth_stage}' stage is entering high-risk window for {threshold.pathogen_name}"
        )
    trigger_reason = " + ".join(reason_parts)

    target = AlertTarget.PER_FARM if farm_id is not None else AlertTarget.REGIONAL_BROADCAST
    cooldown_key = f"{farm_id or district}:{threshold.pathogen_id}:{severity.value}"
    alert_id = str(
        uuid5(
            NAMESPACE_BHOOMI_ALERTS,
            f"{farm_id or district}:{threshold.pathogen_id}:{severity.value}:{evaluated_at.date().isoformat()}",
        )
    )
    expires_at = evaluated_at + timedelta(hours=_COOLDOWN_HOURS[severity])

    spoken_summary = (
        f"{severity.value.capitalize()}: {trigger_reason.split(' + ')[0]}. {threshold.preventative_action}"
    )

    return AlertDraft(
        alert_id=alert_id,
        farm_id=farm_id,
        district=district,
        pathogen_name=threshold.pathogen_name,
        target_crop=threshold.target_crop,
        target=target,
        severity=severity,
        trigger_reason=trigger_reason,
        preventative_action=threshold.preventative_action,
        inspection_tasks=threshold.inspection_tasks,
        spoken_summary=spoken_summary,
        delivery_channels=_delivery_channels(severity),
        created_at=evaluated_at,
        expires_at=expires_at,
        cooldown_key=cooldown_key,
    )
