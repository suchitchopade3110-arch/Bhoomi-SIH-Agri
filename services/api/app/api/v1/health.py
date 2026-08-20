"""Farm Health Score API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.health import (
    HealthHistoryResponse,
    HealthSnapshot,
)

router = APIRouter(prefix="/health", tags=["Farm Health Score"])


@router.get(
    "/score/{farm_id}",
    response_model=HealthSnapshot,
    summary="Get current transparent 6-sub-index health score for farm",
)
async def get_health_score(farm_id: str) -> HealthSnapshot:
    raise NotImplementedAPIError("Endpoint GET /health/score/{farm_id} will be implemented in subsequent phases.")


@router.get(
    "/history/{farm_id}",
    response_model=HealthHistoryResponse,
    summary="Get historical timeline of health score snapshots for farm",
)
async def get_health_history(farm_id: str) -> HealthHistoryResponse:
    raise NotImplementedAPIError("Endpoint GET /health/history/{farm_id} will be implemented in subsequent phases.")
