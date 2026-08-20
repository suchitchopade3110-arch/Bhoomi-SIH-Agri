"""Cadastral lookup and land verification service."""

from typing import Any
from app.schemas.land import CadastralLookupRequest, CadastralLookupResponse, LandVerifyRequest, LandVerifyResponse


class LandService:
    """Manages automated cadastral lookups and HITL officer verification submissions."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def lookup_cadastral_record(self, request: CadastralLookupRequest) -> CadastralLookupResponse:
        raise NotImplementedError("LandService.lookup_cadastral_record will be implemented in subsequent phases.")

    async def submit_for_verification(self, request: LandVerifyRequest) -> LandVerifyResponse:
        raise NotImplementedError("LandService.submit_for_verification will be implemented in subsequent phases.")

    async def get_land_status(self, farm_id: str) -> LandVerifyResponse:
        raise NotImplementedError("LandService.get_land_status will be implemented in subsequent phases.")
