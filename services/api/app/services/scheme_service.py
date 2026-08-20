"""Government scheme matching service."""

from typing import Any
from app.schemas.schemes import SchemeListResponse, SchemeMatchRequest, SchemeResponse


class SchemeService:
    """Matches active subsidies based on verified land, crop, and farmer category."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def match_schemes_for_farm(self, request: SchemeMatchRequest) -> SchemeListResponse:
        raise NotImplementedError("SchemeService.match_schemes_for_farm will be implemented in subsequent phases.")

    async def get_scheme_by_id(self, scheme_id: str) -> SchemeResponse:
        raise NotImplementedError("SchemeService.get_scheme_by_id will be implemented in subsequent phases.")
