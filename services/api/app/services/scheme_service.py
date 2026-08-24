"""Government scheme discovery service — verified-gated (contract §2.14, PRD §5.12)."""

from typing import Annotated

from fastapi import Depends

from app.core.enums import LandStatus, SchemeStatus
from app.core.errors import LandNotVerifiedError, NotFoundError
from app.repositories.dependencies import get_farm_repository, get_scheme_repository
from app.repositories.interfaces import FarmRepository, SchemeRepository
from app.schemas.schemes import SchemeListResponse, SchemeMatchRequest, SchemeResponse


class SchemeService:
    """Matches active/expiring subsidies to a farm — gated on verified land."""

    def __init__(self, scheme_repo: SchemeRepository, farm_repo: FarmRepository) -> None:
        self._schemes = scheme_repo
        self._farms = farm_repo

    async def match_schemes_for_farm(self, request: SchemeMatchRequest) -> SchemeListResponse:
        farm = await self._farms.get_by_id(request.farm_id)
        if farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": request.farm_id})
        
        land_status = farm.get("land_status")
        if land_status != "verified" and land_status != LandStatus.VERIFIED.value:
            raise LandNotVerifiedError(details={"land_status": land_status or "unverified"})

        rows = await self._schemes.match_schemes(
            crop=farm.get("primary_crop", ""),
            category=request.farmer_category or "Small/Marginal",
            acres=farm.get("total_area_acres") or 2.0,
        )
        matched = [_to_scheme_response(r) for r in rows]
        return SchemeListResponse(
            farm_id=request.farm_id,
            matched_schemes=matched,
            match_count=len(matched),
            spoken_summary=f"You are eligible for {len(matched)} scheme(s).",
        )

    async def get_scheme_by_id(self, scheme_id: str) -> SchemeResponse:
        row = await self._schemes.get_by_id(scheme_id)
        if row is None:
            raise NotFoundError("Scheme not found.", details={"scheme_id": scheme_id})
        return _to_scheme_response(row)


def _to_scheme_response(row: dict) -> SchemeResponse:
    return SchemeResponse(
        id=row["id"],
        name=row["name"],
        ministry=row["ministry"],
        description=row["description"],
        benefits=row["benefits"],
        eligibility_criteria=row.get("eligibility_criteria") or {},
        subsidy_percentage=row.get("subsidy_percentage"),
        max_amount_inr=row.get("max_amount_inr"),
        portal_url=row.get("portal_url"),
        status=SchemeStatus(row["status"]),
        last_verified=row["last_verified"],
    )


def get_scheme_service(
    scheme_repo: Annotated[SchemeRepository, Depends(get_scheme_repository)],
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
) -> SchemeService:
    return SchemeService(scheme_repo, farm_repo)
