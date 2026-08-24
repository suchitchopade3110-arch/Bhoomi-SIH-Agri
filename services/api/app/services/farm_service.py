"""Farm onboarding and profile service (contract §2.6, PRD §5.2).

A farm starts with its monitoring fields (soil moisture / irrigation /
planting-day / last-scan) unset — genuinely ``unrated`` (PRD §5.2, §7.1)
until enough real inputs exist. Onboarding may optionally self-report the
non-irrigation monitoring fields (crop-stage-progression and monitoring-
recency inputs); irrigation numbers are always filled in later, by the
FAO-56 resource-plan step (``resource_plan_service.py``) — see the final
report for why this ordering was chosen to match the runbook.
"""

from typing import Annotated, Any

from fastapi import Depends

from app.core.enums import LandStatus
from app.core.errors import NotFoundError
from app.domain.farm_reference_data import get_expected_stage_day
from app.repositories.dependencies import get_farm_repository
from app.repositories.interfaces import FarmRepository
from app.schemas.farm import FarmCreateRequest, FarmResponse, FarmSummaryResponse, FarmUpdateRequest


class FarmService:
    """Creates/reads/updates the Farm aggregate."""

    def __init__(self, farm_repo: FarmRepository) -> None:
        self._farms = farm_repo

    async def create_farm(self, request: FarmCreateRequest) -> FarmResponse:
        data: dict[str, Any] = {
            "farmer_id": request.farmer_id,
            "primary_crop": request.crop,
            "growth_stage": request.growth_stage,
            "region": request.region,
            "expected_stage_day": get_expected_stage_day(request.growth_stage or "vegetative"),
            "land_status": LandStatus.UNVERIFIED.value,
        }
        saved = await self._farms.save(data)
        return _to_farm_response(saved)

    async def get_farm(self, farm_id: str) -> FarmResponse:
        row = await self._farms.get_by_id(farm_id)
        if row is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})
        return _to_farm_response(row)

    async def update_farm(self, farm_id: str, request: FarmUpdateRequest) -> FarmResponse:
        updates = {k: v for k, v in request.model_dump().items() if v is not None}
        row = await self._farms.update(farm_id, updates)
        if row is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})
        return _to_farm_response(row)

    async def get_farm_summary(self, farm_id: str) -> FarmSummaryResponse:
        farm = await self.get_farm(farm_id)
        name = farm.farm_name or "your farm"
        return FarmSummaryResponse(
            farm=farm,
            spoken_summary=f"Here is the summary for {name}.",
        )


def _to_farm_response(row: dict[str, Any]) -> FarmResponse:
    kwargs = {
        "id": row["id"],
        "farmer_id": row["farmer_id"],
        "farm_name": row.get("farm_name"),
        "village": row.get("village"),
        "taluk": row.get("taluk"),
        "district": row.get("district"),
        "region": row.get("region"),
        "state": row.get("state") or "Tamil Nadu",
        "latitude": row.get("latitude"),
        "longitude": row.get("longitude"),
        "total_area_acres": row.get("total_area_acres"),
        "survey_number": row.get("survey_number"),
        "land_status": LandStatus(row["land_status"]) if row.get("land_status") else LandStatus.UNVERIFIED,
        "primary_crop": row.get("primary_crop", ""),
        "growth_stage": row.get("growth_stage"),
        "soil_type": row.get("soil_type"),
        "irrigation_source": row.get("irrigation_source"),
    }
    if row.get("created_at") is not None:
        kwargs["created_at"] = row["created_at"]
    return FarmResponse(**kwargs)


def get_farm_service(farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)]) -> FarmService:
    return FarmService(farm_repo)
