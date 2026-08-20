"""FAO-56 Resource Planner API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.resource_plan import (
    Fao56CalculateRequest,
    Fao56CalculateResponse,
    ResourcePlanResponse,
)

router = APIRouter(prefix="/resource-plan", tags=["Resource Planner & FAO-56"])


@router.post(
    "/fao56",
    response_model=Fao56CalculateResponse,
    summary="Calculate daily crop water requirements via FAO-56 Penman-Monteith",
)
async def calculate_fao56(request: Fao56CalculateRequest) -> Fao56CalculateResponse:
    raise NotImplementedAPIError("Endpoint POST /resource-plan/fao56 will be implemented in subsequent phases.")


@router.get(
    "/{farm_id}",
    response_model=ResourcePlanResponse,
    summary="Get active resource plan (water, seeds, nutrients) for farm",
)
async def get_resource_plan(farm_id: str) -> ResourcePlanResponse:
    raise NotImplementedAPIError("Endpoint GET /resource-plan/{farm_id} will be implemented in subsequent phases.")
