"""Cadastral lookup and HITL land verification service (contract §2.7, PRD §5.3).

HITL is the primary path — automated lookup (``LandRegistryPort``) is only
an accelerator. On a match, the parcel is verified immediately (the
showcase path); otherwise it's queued to the officer, which the contract
notes is the common case.
"""

from typing import Annotated, Any

from fastapi import Depends

from app.adapters.dependencies import get_land_registry_adapter
from app.adapters.land_registry import LandRegistryPort
from app.core.enums import LandStatus
from app.core.errors import NotFoundError
from app.repositories.dependencies import get_farm_repository, get_land_repository
from app.repositories.interfaces import FarmRepository, LandParcelRepository
from app.schemas.land import CadastralLookupRequest, CadastralLookupResponse, LandVerifyRequest, LandVerifyResponse


class LandService:
    """Manages automated cadastral lookups and HITL officer verification submissions."""

    def __init__(self, land_repo: LandParcelRepository, farm_repo: FarmRepository, registry: LandRegistryPort) -> None:
        self._land = land_repo
        self._farms = farm_repo
        self._registry = registry

    async def lookup_cadastral_record(self, request: CadastralLookupRequest) -> CadastralLookupResponse:
        result = await self._registry.lookup(request.survey_number, request.district, request.taluk, request.village)
        return CadastralLookupResponse(
            found=result["matched"],
            survey_number=request.survey_number,
            owner_name=result.get("owner_name"),
            area_acres=result.get("area_acres"),
            boundary_geojson=result.get("boundary_geojson"),
            source=result.get("source", "mock_tn_edistrict"),
        )

    async def submit_for_verification(self, request: LandVerifyRequest) -> LandVerifyResponse:
        farm = await self._farms.get_by_id(request.farm_id)
        if farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": request.farm_id})

        lookup = await self._registry.lookup(request.survey_number, farm["district"], farm["taluk"], farm["village"])

        parcel_data: dict[str, Any] = {
            "farm_id": request.farm_id,
            "survey_number": request.survey_number,
            "patta_passbook_asset_id": request.patta_passbook_asset_id,
            "district": farm["district"],
            "suggested_boundary": request.suggested_boundary,
        }

        if lookup["matched"]:
            parcel_data["status"] = LandStatus.VERIFIED.value
            parcel_data["auto_lookup_outcome"] = "matched"
            parcel_data["confirmed_boundary"] = lookup.get("boundary_geojson")
            parcel_data["verified_by"] = "auto_lookup"
        else:
            parcel_data["status"] = LandStatus.PENDING_REVIEW.value
            parcel_data["auto_lookup_outcome"] = "failed"

        saved = await self._land.save(parcel_data)

        await self._farms.update(request.farm_id, {"land_status": saved["status"]})

        return LandVerifyResponse(
            parcel_id=saved["id"],
            farm_id=request.farm_id,
            status=LandStatus(saved["status"]),
            submitted_at=saved["submitted_at"],
            officer_notes=None if lookup["matched"] else "Queued for officer review — automated lookup found no match.",
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
    registry: Annotated[LandRegistryPort, Depends(get_land_registry_adapter)],
) -> LandService:
    return LandService(land_repo, farm_repo, registry)
