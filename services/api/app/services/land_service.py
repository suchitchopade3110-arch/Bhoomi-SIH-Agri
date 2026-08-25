"""HITL land verification service (contract §2.7, PRD §5.3).

HITL officer review is the only path (SIH26131 feature checklist §13.3:
"Live government land or scheme integration — cut"; §10.1: "No polygon, no
map, no auto-lookup mock"). Every submission queues to the officer — there
is no automated cadastral lookup that can verify a parcel without a human.
"""

from typing import Annotated, Any

from fastapi import Depends

from app.core.enums import LandStatus
from app.core.errors import NotFoundError
from app.repositories.dependencies import get_farm_repository, get_land_repository
from app.repositories.interfaces import FarmRepository, LandParcelRepository
from app.schemas.land import LandVerifyRequest, LandVerifyResponse


class LandService:
    """Manages HITL officer verification submissions."""

    def __init__(self, land_repo: LandParcelRepository, farm_repo: FarmRepository) -> None:
        self._land = land_repo
        self._farms = farm_repo

    async def submit_for_verification(self, request: LandVerifyRequest) -> LandVerifyResponse:
        farm = await self._farms.get_by_id(request.farm_id)
        if farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": request.farm_id})

        parcel_data: dict[str, Any] = {
            "farm_id": request.farm_id,
            "survey_number": request.survey_number,
            "patta_passbook_asset_id": request.patta_passbook_asset_id,
            # SIH26131's simplified onboarding never collects `district`
            # (only `region`) — `land_parcels.district` is NOT NULL, so
            # fall back rather than crash on every SIH26131-onboarded farm.
            "district": farm.get("district") or farm.get("region") or "Unknown",
            "status": LandStatus.PENDING_REVIEW.value,
            "auto_lookup_outcome": "not_attempted",
        }

        saved = await self._land.save(parcel_data)

        await self._farms.update(request.farm_id, {"land_status": saved["status"]})

        return LandVerifyResponse(
            parcel_id=saved["id"],
            farm_id=request.farm_id,
            status=LandStatus(saved["status"]),
            submitted_at=saved["submitted_at"],
            officer_notes="Queued for officer review.",
        )

    async def get_land_status(self, farm_id: str) -> LandVerifyResponse:
        row = await self._land.get_by_farm_id(farm_id)
        if row is None:
            raise NotFoundError("No land submission found for this farm.", details={"farm_id": farm_id})
        return LandVerifyResponse(
            parcel_id=row["id"],
            farm_id=farm_id,
            status=LandStatus(row["status"]),
            submitted_at=row["submitted_at"],
            officer_notes=row.get("officer_notes"),
        )


def get_land_service(
    land_repo: Annotated[LandParcelRepository, Depends(get_land_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> LandService:
    return LandService(land_repo, farm_repo)
