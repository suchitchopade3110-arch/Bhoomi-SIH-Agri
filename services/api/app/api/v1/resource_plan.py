"""FAO-56 Resource Planner API router (contract §2.8)."""

from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.resource_plan import ResourcePlanResponse
from app.services.resource_plan_service import ResourcePlanService, get_resource_plan_service

router = APIRouter(prefix="/resource-plan", tags=["Resource Planner & FAO-56"])


@router.post(
    "/{farm_id}",
    response_model=ResourcePlanResponse,
    summary="Compute (and persist) the FAO-56 daily irrigation + seed plan for a farm",
)
async def compute_resource_plan(
    farm_id: str,
    service: Annotated[ResourcePlanService, Depends(get_resource_plan_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    as_of: date | None = None,
) -> ResourcePlanResponse:
    """PRD §5.4 / contract §2.8. Every input that fed the result — ET0, Kc,
    effective rainfall — is returned inspectable, and the irrigation numbers
    are persisted onto the farm as the health engine's resource_adequacy
    input (PRD §7.2 #2)."""
    return await service.compute_and_persist(farm_id, as_of)


@router.get(
    "/{farm_id}",
    response_model=ResourcePlanResponse,
    summary="Get the current resource plan for a farm (recomputed fresh from live weather)",
)
async def get_resource_plan(
    farm_id: str,
    service: Annotated[ResourcePlanService, Depends(get_resource_plan_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> ResourcePlanResponse:
    return await service.compute_and_persist(farm_id)
