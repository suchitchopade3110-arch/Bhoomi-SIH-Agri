"""Farm profile and living context service."""

from typing import Any
from app.schemas.farm import FarmCreateRequest, FarmResponse, FarmSummaryResponse, FarmUpdateRequest


class FarmService:
    """Manages farm profiles, crop stages, and aggregated summaries."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def create_farm(self, request: FarmCreateRequest) -> FarmResponse:
        raise NotImplementedError("FarmService.create_farm will be implemented in subsequent phases.")

    async def get_farm(self, farm_id: str) -> FarmResponse:
        raise NotImplementedError("FarmService.get_farm will be implemented in subsequent phases.")

    async def update_farm(self, farm_id: str, request: FarmUpdateRequest) -> FarmResponse:
        raise NotImplementedError("FarmService.update_farm will be implemented in subsequent phases.")

    async def get_farm_summary(self, farm_id: str) -> FarmSummaryResponse:
        raise NotImplementedError("FarmService.get_farm_summary will be implemented in subsequent phases.")
