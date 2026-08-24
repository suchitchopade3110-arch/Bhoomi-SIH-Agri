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
        data: dict[str, Any] = request.model_dump()
        # expected_stage_day is a derived reference-table lookup (PRD §7.2 #3
        # input), not something the farmer reports — computed once here so
        # every later health recompute reads a stable, inspectable value.
        data["expected_stage_day"] = get_expected_stage_day(request.growth_stage or "vegetative")
        data["land_status"] = LandStatus.UNVERIFIED.value
        saved = await self._farms.save(data)
        return _to_farm_response(saved)

    async def get_farm(self, farm_id: str) -> FarmResponse:
        row = await self._farms.get_by_id(farm_id)
        if row is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})
        return _to_farm_response(row)

    async def list_farms_for_farmer(self, farmer_id: str) -> list[FarmResponse]:
        """List every farm owned by the authenticated farmer.

        Backs ``GET /farms`` — the client-side counterpart to onboarding's
        ``POST /farms``. Without this, a client that only has a JWT (no
        farm_id in hand yet, e.g. right after login) has no way to discover
        which farm to call ``/farms/{id}/...`` against.
        """
        rows = await self._farms.get_by_farmer_id(farmer_id)
        return [_to_farm_response(row) for row in rows]

    async def update_farm(self, farm_id: str, request: FarmUpdateRequest) -> FarmResponse:
        updates = {k: v for k, v in request.model_dump().items() if v is not None}
        row = await self._farms.update(farm_id, updates)
        if row is None:
            raise NotFoundError("Farm not found.", details={"farm_id": farm_id})
        return _to_farm_response(row)

    async def get_farm_summary(self, farm_id: str) -> FarmSummaryResponse:
        farm = await self.get_farm(farm_id)
        return FarmSummaryResponse(
            farm=farm,
            spoken_summary=f"Here is the summary for {farm.farm_name}.",
        )


def _to_farm_response(row: dict[str, Any]) -> FarmResponse:
    return FarmResponse(
        id=row["id"],
        farmer_id=row["farmer_id"],
        farm_name=row["farm_name"],
        village=row["village"],
        taluk=row["taluk"],
        district=row["district"],
        state=row["state"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        total_area_acres=row["total_area_acres"],
        survey_number=row.get("survey_number"),
        land_status=LandStatus(row["land_status"]),
        primary_crop=row["primary_crop"],
        growth_stage=row.get("growth_stage"),
        soil_type=row["soil_type"],
        irrigation_source=row["irrigation_source"],
        created_at=row["created_at"],
    )


def get_farm_service(farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)]) -> FarmService:
    return FarmService(farm_repo)
