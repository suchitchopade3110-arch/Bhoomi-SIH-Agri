"""Extension Officer verification service."""

from typing import Any
from app.schemas.officer import OfficerActionRequest, OfficerActionResponse, OfficerQueueItem, OfficerReviewDetail


class OfficerService:
    """Manages officer queue, boundary inspection, and HITL verification decisions."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def get_queue(self, officer_id: str) -> list[OfficerQueueItem]:
        raise NotImplementedError("OfficerService.get_queue will be implemented in subsequent phases.")

    async def get_parcel_detail(self, parcel_id: str) -> OfficerReviewDetail:
        raise NotImplementedError("OfficerService.get_parcel_detail will be implemented in subsequent phases.")

    async def process_action(self, request: OfficerActionRequest) -> OfficerActionResponse:
        raise NotImplementedError("OfficerService.process_action will be implemented in subsequent phases.")
