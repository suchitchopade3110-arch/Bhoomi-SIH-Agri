"""Orchestration for the Farm Health Score (PRD §7, contract §2.9).

Gathers real-world inputs from repositories/adapters, hands them to the pure
``domain.health.compute_health`` function, and persists the resulting
snapshot. No scoring logic lives here — only wiring.
"""

import logging
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_weather_adapter
from app.ports.weather import WeatherPort
from app.domain.advisory import derive_qualitative_advisory
from app.domain.health import compute_health
from app.domain.health.inputs import (
    CropIdealConditions,
    HealthScoreInputs,
    OpenProblemInput,
    TriggeringInput,
    WeatherReading,
)
from app.models.health_snapshot import HealthSnapshot
from app.schemas.farm import FarmRiskTrendResponse, FarmSummaryTrendResponse
from app.repositories.health_context import (
    FarmHealthContextReader,
    ProblemLoadReader,
    TreatmentTrendReader,
)
from app.repositories.dependencies import (
    get_farm_health_context_reader,
    get_health_snapshot_repository,
    get_problem_load_reader,
    get_treatment_trend_reader,
)
from app.repositories.health_snapshot_repository import HealthSnapshotRepository

logger = logging.getLogger("bhoomi.health_service")

# Fallback weather used when WeatherPort is unavailable (PRD §1.4 degraded
# mode; execution plan item 7). Flagged self-reported rather than silently
# treated as a live reading.
FALLBACK_TEMP_C = 30.0
FALLBACK_HUMIDITY_PCT = 70.0

RECOMPUTE_TRIGGER_TYPE = "manual_recompute"
INITIAL_TRIGGER_TYPE = "initial_view"

# A neutral placeholder ideal-conditions band used only when a farm has no
# context yet (the resulting inputs are already all-``None``, so this value
# never affects a real score — see HealthScoreInputs.required_inputs_present).
_DEFAULT_CROP_IDEAL = CropIdealConditions(
    temp_min_c=20.0,
    temp_max_c=35.0,
    humidity_min_pct=50.0,
    humidity_max_pct=85.0,
    soil_moisture_min_pct=60.0,
)


class HealthService:
    """Orchestrates health score computation, persistence, and history reads."""

    def __init__(
        self,
        snapshot_repo: HealthSnapshotRepository,
        context_reader: FarmHealthContextReader,
        problem_reader: ProblemLoadReader,
        treatment_reader: TreatmentTrendReader,
        weather_port: WeatherPort,
    ) -> None:
        self._snapshots = snapshot_repo
        self._context_reader = context_reader
        self._problem_reader = problem_reader
        self._treatment_reader = treatment_reader
        self._weather = weather_port

    async def _build_inputs(self, farm_id: str, triggering_input: TriggeringInput) -> HealthScoreInputs:
        """Assemble a ``HealthScoreInputs`` for ``farm_id`` from repositories
        and ``WeatherPort``. Missing farm context yields an inputs object
        that reports every field missing (-> ``unrated``, never a guess).
        """
        context = await self._context_reader.get_context(farm_id)

        open_problems = await self._problem_reader.get_open_problems(farm_id)
        trend = await self._treatment_reader.get_treatment_trend(farm_id)

        if context is None:
            return HealthScoreInputs(
                triggering_input=triggering_input,
                weather=None,
                crop_ideal=_DEFAULT_CROP_IDEAL,
                soil_moisture_pct=None,
                irrigation_delivered_mm=None,
                irrigation_required_mm=None,
                days_since_planting=None,
                expected_stage_day=0,
                open_problems=[OpenProblemInput(severity=p.severity) for p in open_problems],
                days_since_last_scan=None,
                latest_followup_response=trend.latest_followup_response,
                consecutive_got_worse_count=trend.consecutive_got_worse_count,
                problem_resolved_with_confirmed_treatment=trend.problem_resolved_with_confirmed_treatment,
            )

        weather = await self._get_weather_or_fallback(context.latitude, context.longitude)

        return HealthScoreInputs(
            triggering_input=triggering_input,
            weather=weather,
            crop_ideal=context.crop_ideal,
            soil_moisture_pct=context.soil_moisture_pct,
            irrigation_delivered_mm=context.irrigation_delivered_mm,
            irrigation_required_mm=context.irrigation_required_mm,
            days_since_planting=context.days_since_planting,
            expected_stage_day=context.expected_stage_day,
            open_problems=[OpenProblemInput(severity=p.severity) for p in open_problems],
            days_since_last_scan=context.days_since_last_scan,
            latest_followup_response=trend.latest_followup_response,
            consecutive_got_worse_count=trend.consecutive_got_worse_count,
            problem_resolved_with_confirmed_treatment=trend.problem_resolved_with_confirmed_treatment,
        )

    async def _get_weather_or_fallback(self, latitude: float, longitude: float) -> WeatherReading:
        """Read live weather via ``WeatherPort``; fall back to a fixed,
        self-reported reading if the port is unavailable (PRD §1.4)."""
        try:
            current = await self._weather.get_current_weather(latitude, longitude)
            return WeatherReading(
                temp_c=float(current["temperature_c"]),
                relative_humidity_pct=float(current["relative_humidity_pct"]),
            )
        except Exception:
            logger.warning(
                "WeatherPort unavailable for (%s, %s); falling back to a fixed, self-reported reading.",
                latitude,
                longitude,
            )
            return WeatherReading(temp_c=FALLBACK_TEMP_C, relative_humidity_pct=FALLBACK_HUMIDITY_PCT)

    async def _compute_and_persist(self, farm_id: str, triggering_input: TriggeringInput) -> HealthSnapshot:
        inputs = await self._build_inputs(farm_id, triggering_input)
        result = compute_health(inputs)

        row = HealthSnapshot(
            farm_id=farm_id,
            score=result.score,
            band=result.band.value,
            weights_version=result.weights_version,
            subindices=[
                {
                    "key": s.key.value,
                    "value": s.value,
                    "weight": s.weight,
                    "contribution": s.contribution,
                }
                for s in result.subindices
            ],
            triggering_input=result.triggering_input.as_dict(),
            missing_fields=result.missing_fields,
        )
        return await self._snapshots.save(row)

    async def recompute(
        self,
        farm_id: str,
        reason: str = RECOMPUTE_TRIGGER_TYPE,
        triggering_input: TriggeringInput | None = None,
    ) -> HealthSnapshot:
        """Force a fresh computation and persist it (contract §2.9 recompute endpoint).

        Pass ``triggering_input`` for a richer audit trail (e.g. a Phase-3
        diagnosis: ``TriggeringInput(type="diagnosis", details={"problem_id": ..., "severity": "early"})``)
        — it takes precedence over ``reason``, which stays as the plain
        default for the demo/admin recompute endpoint.
        """
        return await self._compute_and_persist(farm_id, triggering_input or TriggeringInput(type=reason))

    async def get_latest(self, farm_id: str) -> HealthSnapshot:
        """Most recent snapshot for a farm; computes and persists an initial
        one on first read so a brand-new farm sees an explicit ``unrated``
        state rather than a 404."""
        existing = await self._snapshots.get_latest(farm_id)
        if existing is not None:
            return existing
        return await self._compute_and_persist(farm_id, TriggeringInput(type=INITIAL_TRIGGER_TYPE))

    async def get_history(
        self, farm_id: str, limit: int, cursor: str | None = None
    ) -> tuple[list[HealthSnapshot], str | None]:
        """Newest-first, cursor-paginated snapshot history for a farm."""
        return await self._snapshots.get_history(farm_id, limit, cursor)

    async def get_farm_risk(self, farm_id: str) -> FarmRiskTrendResponse:
        """Derive qualitative farm risk summary (no weights, no sub-indices) per SIH26131."""
        context = await self._context_reader.get_context(farm_id)
        open_problems = await self._problem_reader.get_open_problems(farm_id)
        trend = await self._treatment_reader.get_treatment_trend(farm_id)

        highest_sev = None
        primary_label = None
        if open_problems:
            primary_label = open_problems[0].label or None
            sevs = [p.severity.value for p in open_problems]
            if "severe" in sevs:
                highest_sev = "severe"
            elif "moderate" in sevs:
                highest_sev = "moderate"
            else:
                highest_sev = "early"

        days_since_scan = context.days_since_last_scan if context else None
        followup_resp = (
            trend.latest_followup_response.value
            if (trend and trend.latest_followup_response)
            else None
        )

        res = derive_qualitative_advisory(
            open_problems_count=len(open_problems),
            highest_severity=highest_sev,
            primary_problem_label=primary_label,
            days_since_last_scan=days_since_scan,
            latest_followup_response=followup_resp,
        )

        return FarmRiskTrendResponse(
            farm_id=farm_id,
            advisory=res.advisory,
            trend=res.trend.value,
            spoken_summary=f"Condition is {res.trend.value}. {res.advisory}",
        )

    async def get_farm_summary_trend(
        self,
        farm_id: str,
        farm_name: str = "",
        village: str = "",
        primary_crop: str = "",
    ) -> FarmSummaryTrendResponse:
        """Derive qualitative farm summary card for SIH26131."""
        risk = await self.get_farm_risk(farm_id)
        open_problems = await self._problem_reader.get_open_problems(farm_id)
        return FarmSummaryTrendResponse(
            farm_id=farm_id,
            advisory=risk.advisory,
            trend=risk.trend,
            open_cases_count=len(open_problems),
            last_interaction_at=risk.updated_at,
            spoken_summary=risk.spoken_summary,
        )


def get_health_service(
    snapshot_repo: Annotated[HealthSnapshotRepository, Depends(get_health_snapshot_repository)],
    context_reader: Annotated[FarmHealthContextReader, Depends(get_farm_health_context_reader)],
    problem_reader: Annotated[ProblemLoadReader, Depends(get_problem_load_reader)],
    treatment_reader: Annotated[TreatmentTrendReader, Depends(get_treatment_trend_reader)],
    weather_port: Annotated[WeatherPort, Depends(get_weather_adapter)],
) -> HealthService:
    """FastAPI dependency provider assembling ``HealthService`` from its ports."""
    return HealthService(snapshot_repo, context_reader, problem_reader, treatment_reader, weather_port)
