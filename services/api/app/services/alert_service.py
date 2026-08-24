"""Early-Warning Alert System service (SPEC-ALERT-001 §4.2, Phase 3).

Orchestrates the three-step pipeline the spec mandates:
  1. Pure domain evaluation (``domain.alerts.evaluate_alert``) per pathogen
     threshold — no I/O, no cooldown awareness.
  2. Service-level cooldown gating against ``AlertRepository`` — suppress a
     duplicate at the same ``cooldown_key``, unless severity upgraded, in
     which case supersede the prior lower-severity alert.
  3. Persistence via ``AlertRepository.save``.

``GET /farms/{id}/alerts`` calls ``evaluate_and_list`` (evaluate fresh, then
return every currently active alert for the farm — both newly created ones
and pre-existing regional broadcasts). Nothing here runs as a background
job in this phase; evaluation is on-demand, driven by the read.
"""

from datetime import datetime
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_weather_adapter
from app.core.errors import NotFoundError
from app.domain.alerts.evaluate import evaluate_alert
from app.domain.alerts.models import AlertDraft, ClusterCase, WeatherMetrics
from app.domain.alerts.thresholds import PATHOGEN_RISK_THRESHOLDS
from app.ports.weather import WeatherPort
from app.repositories.dependencies import get_alert_repository, get_farm_repository
from app.repositories.interfaces import AlertRepository, FarmRepository

# Spec §2.1's cluster window ("past 7 days").
CLUSTER_WINDOW_DAYS = 7

# WeatherPort exposes only a current point-in-time reading, not a 48h
# historical series (spec §3.2 wants "48-hour average ... sustained >=Xh").
# Until a historical weather store exists, a current reading that satisfies
# the temp/humidity band is treated as having been sustained for exactly
# the threshold's required duration — an honest, documented approximation,
# not a fabricated reading. See early_warning_alert_spec.md follow-up note.


def _weather_metrics_from_current_reading(reading: dict, threshold) -> WeatherMetrics:
    temp_c = reading.get("temperature_c", 0.0)
    humidity_pct = reading.get("relative_humidity_pct", 0.0)
    band_met = threshold.temp_min_c <= temp_c <= threshold.temp_max_c and humidity_pct >= threshold.humidity_min_pct
    return WeatherMetrics(
        avg_temp_c=temp_c,
        avg_humidity_pct=humidity_pct,
        sustained_hours=threshold.sustained_hours if band_met else 0,
    )


class AlertService:
    def __init__(self, alert_repo: AlertRepository, farm_repo: FarmRepository, weather_port: WeatherPort) -> None:
        self._alerts = alert_repo
        self._farms = farm_repo
        self._weather = weather_port

    async def _evaluate_farm(self, farm: dict, evaluated_at: datetime) -> list[AlertDraft]:
        crop = farm.get("primary_crop")
        growth_stage = farm.get("growth_stage")
        lat, lon = farm["latitude"], farm["longitude"]

        drafts: list[AlertDraft] = []
        for threshold in PATHOGEN_RISK_THRESHOLDS.values():
            if crop != threshold.target_crop:
                continue

            reading = await self._weather.get_current_weather(lat, lon)
            weather = _weather_metrics_from_current_reading(reading, threshold)

            cluster_summary: list[ClusterCase] = await self._alerts.get_nearby_cluster_summary(
                target_farm_lat=lat,
                target_farm_lon=lon,
                target_farm_id=farm["id"],
                radius_km=threshold.cluster_radius_km,
                window_days=CLUSTER_WINDOW_DAYS,
            )

            draft = evaluate_alert(
                farm_id=farm["id"],
                district=farm.get("district", ""),
                crop=crop,
                growth_stage=growth_stage,
                weather=weather,
                cluster_summary=cluster_summary,
                threshold=threshold,
                evaluated_at=evaluated_at,
            )
            if draft is not None:
                drafts.append(draft)

        return drafts

    async def _gate_and_persist(self, draft: AlertDraft, evaluated_at: datetime) -> None:
        """Spec §4.2 step 2-3: cooldown gate, then persist (and supersede
        any prior lower-severity alert for the same subject+pathogen)."""
        existing = await self._alerts.get_active_cooldown(draft.cooldown_key, as_of=evaluated_at)
        if existing is not None:
            return  # same or higher severity already active — suppressed

        subject = draft.farm_id or draft.district
        pathogen_id = draft.cooldown_key.split(":")[1]
        await self._alerts.supersede_active_alerts(subject, pathogen_id, as_of=evaluated_at)

        await self._alerts.save(
            {
                "id": draft.alert_id,
                "farm_id": draft.farm_id,
                "district": draft.district,
                "pathogen_name": draft.pathogen_name,
                "target_crop": draft.target_crop,
                "target": draft.target.value,
                "severity": draft.severity.value,
                "trigger_reason": draft.trigger_reason,
                "preventative_action": draft.preventative_action,
                "spoken_summary": draft.spoken_summary,
                "delivery_channels": [c.value for c in draft.delivery_channels],
                "cooldown_key": draft.cooldown_key,
                "created_at": draft.created_at,
                "expires_at": draft.expires_at,
                "status": "active",
            }
        )

    async def evaluate_and_list(self, farm_id: str) -> list[dict]:
        farm = await self._farms.get_by_id(farm_id)
        if farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})

        evaluated_at = datetime.utcnow()
        drafts = await self._evaluate_farm(farm, evaluated_at)
        for draft in drafts:
            await self._gate_and_persist(draft, evaluated_at)

        return await self._alerts.get_farm_alerts(
            farm_id=farm_id,
            district=farm.get("district", ""),
            crop=farm.get("primary_crop"),
            as_of=evaluated_at,
        )

    async def dismiss(self, alert_id: str, farm_id: str, reason: str) -> dict:
        dismissed = await self._alerts.dismiss(alert_id, farm_id, reason, as_of=datetime.utcnow())
        if dismissed is None:
            raise NotFoundError("Alert not found.", details={"alert_id": alert_id})
        return dismissed


def get_alert_service(
    alert_repo: Annotated[AlertRepository, Depends(get_alert_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    weather_port: Annotated[WeatherPort, Depends(get_weather_adapter)],
) -> AlertService:
    return AlertService(alert_repo, farm_repo, weather_port)
