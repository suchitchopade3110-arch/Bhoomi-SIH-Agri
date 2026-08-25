"""Extension Officer portal service — the HITL land verification queue
(contract §2.7, PRD §5.3).
"""

from typing import Annotated

from fastapi import Depends

from app.core.enums import LandStatus
from app.core.errors import NotFoundError
from app.repositories.dependencies import get_farm_repository, get_land_repository
from app.repositories.interfaces import FarmRepository, LandParcelRepository
from app.schemas.officer import OfficerActionRequest, OfficerActionResponse, OfficerQueueItem, OfficerReviewDetail


class OfficerService:
    """Officer-facing queue and boundary-approval actions."""

    def __init__(self, land_repo: LandParcelRepository, farm_repo: FarmRepository) -> None:
        self._land = land_repo
        self._farms = farm_repo

    async def get_queue(self, district: str | None = None) -> list[OfficerQueueItem]:
        parcels = await self._land.get_pending_queue(district)
        items = []
        for p in parcels:
            farm = await self._farms.get_by_id(p["farm_id"])
            items.append(
                OfficerQueueItem(
                    parcel_id=p["id"],
                    farm_id=p["farm_id"],
                    # dict.get's default only fires on a missing key, not a
                    # NULL value — SIH26131's simplified onboarding leaves
                    # farm_name/village NULL (not absent), so `or` is
                    # required here to actually catch None (same pattern as
                    # agronomist_service.py's get_case_detail).
                    farmer_name=(farm or {}).get("farm_name") or "Unknown",
                    village=(farm or {}).get("village") or "",
                    survey_number=p["survey_number"],
                    submitted_at=p["submitted_at"],
                    status=LandStatus(p["status"]),
                    patta_asset_url=None,
                )
            )
        return items

    async def get_parcel_detail(self, parcel_id: str) -> OfficerReviewDetail:
        parcel = await self._land.get_by_id(parcel_id)
        if parcel is None:
            raise NotFoundError("Land parcel not found.", details={"parcel_id": parcel_id})
        farm = await self._farms.get_by_id(parcel["farm_id"])
        return OfficerReviewDetail(
            parcel_id=parcel["id"],
            farm_id=parcel["farm_id"],
            farmer_name=(farm or {}).get("farm_name") or "Unknown",
            farmer_phone="",
            village=(farm or {}).get("village") or "",
            taluk=(farm or {}).get("taluk") or "",
            survey_number=parcel["survey_number"],
        )

    async def process_action(self, request: OfficerActionRequest) -> OfficerActionResponse:
        parcel = await self._land.get_by_id(request.parcel_id)
        if parcel is None:
            raise NotFoundError("Land parcel not found.", details={"parcel_id": request.parcel_id})

        updated = await self._land.update_status(request.parcel_id, request.action.value)
        await self._farms.update(parcel["farm_id"], {"land_status": request.action.value})

        return OfficerActionResponse(parcel_id=updated["id"], status=LandStatus(updated["status"]))


def get_officer_service(
    land_repo: Annotated[LandParcelRepository, Depends(get_land_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> OfficerService:
    return OfficerService(land_repo, farm_repo)
