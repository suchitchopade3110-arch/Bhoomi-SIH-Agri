"""FAO-56 resource planner orchestration (contract §2.8, PRD §5.4).

Wiring only — the calculation itself is the pure ``domain.fao56`` function.
This service fetches ET0/rainfall from ``WeatherPort``, looks up Kc/seed-rate
from ``domain.farm_reference_data``, and persists the resulting irrigation
numbers onto the farm's monitoring state (the last missing health-engine
inputs — see ``services/farm_service.py``'s module docstring for why this is
where ``irrigation_delivered_mm`` / ``irrigation_required_mm`` get filled in).
"""

from datetime import date
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_weather_adapter
from app.adapters.ports import WeatherPort
from app.core.errors import NotFoundError
from app.domain.fao56 import calculate_fao56_irrigation, effective_rainfall_mm
from app.domain.farm_reference_data import get_kc, get_seed_rate_kg_per_acre
from app.domain.health.inputs import TriggeringInput
from app.repositories.dependencies import get_farm_repository
from app.repositories.interfaces import FarmRepository
from app.schemas.resource_plan import Fao56CalculateResponse, ResourcePlanResponse
from app.services.health_service import HealthService, get_health_service

# What fraction of the FAO-56 requirement the farmer is assumed to actually
# deliver before any real irrigation telemetry exists — feeds the health
# engine's resource_adequacy sub-index (PRD §7.2 #2) with an honest "not yet
# instrumented" default rather than assuming perfect compliance.
DEFAULT_IRRIGATION_COMPLIANCE_RATIO = 0.75


class ResourcePlanService:
    """Computes and persists the FAO-56 irrigation + seed plan for a farm."""

    def __init__(self, farm_repo: FarmRepository, weather: WeatherPort, health_service: HealthService) -> None:
        self._farms = farm_repo
        self._weather = weather
        self._health = health_service

    async def compute_and_persist(self, farm_id: str, as_of: date | None = None) -> ResourcePlanResponse:
        farm = await self._farms.get_by_id(farm_id)
        if farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})

        target_date = as_of or date.today()
        et0 = await self._weather.get_daily_et0(farm["latitude"], farm["longitude"], target_date)
        current = await self._weather.get_current_weather(farm["latitude"], farm["longitude"])
        rainfall = effective_rainfall_mm(float(current.get("precipitation_mm", 0.0)))

        growth_stage = farm.get("growth_stage") or "vegetative"
        kc = get_kc(farm["primary_crop"], growth_stage)

        irrigation_plan: Fao56CalculateResponse = calculate_fao56_irrigation(
            crop=farm["primary_crop"],
            growth_stage=growth_stage,
            area_acres=farm["total_area_acres"],
            et0_mm_day=et0,
            kc_factor=kc,
            effective_rainfall_mm=rainfall,
            soil_type=farm["soil_type"],
        )

        delivered_mm = round(irrigation_plan.irrigation_need_mm * DEFAULT_IRRIGATION_COMPLIANCE_RATIO, 4)
        await self._farms.update(
            farm_id,
            {
                "irrigation_required_mm": irrigation_plan.irrigation_need_mm,
                "irrigation_delivered_mm": delivered_mm,
            },
        )
        # These are the last health-engine inputs a brand-new farm is
        # typically missing (see farm_service.py's module docstring) — a
        # fresh plan is exactly the event that can flip a farm from
        # `unrated` to its first real score, so recompute now rather than
        # waiting for someone to separately call the recompute endpoint.
        await self._health.recompute(farm_id, triggering_input=TriggeringInput(type="resource_plan"))

        seed_rate = get_seed_rate_kg_per_acre(farm["primary_crop"])
        recommended_seed_kg = round(seed_rate * farm["total_area_acres"], 2)

        return ResourcePlanResponse(
            farm_id=farm_id,
            irrigation_plan=irrigation_plan,
            recommended_seed_kg=recommended_seed_kg,
            seed_variety=farm["primary_crop"],
            fertilizer_schedule=[],
            spoken_summary=irrigation_plan.spoken_summary,
        )


def get_resource_plan_service(
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    weather: Annotated[WeatherPort, Depends(get_weather_adapter)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> ResourcePlanService:
    return ResourcePlanService(farm_repo, weather, health_service)
