"""Farm Health Score API router (contract §2.9)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_token_payload
from app.schemas.farm import FarmRiskTrendResponse
from app.schemas.health import HealthHistoryResponse, HealthSnapshot
from app.services.health_service import HealthService, get_health_service
from app.services.health_snapshot_mapping import snapshot_row_to_schema

router = APIRouter(prefix="/farms", tags=["Farm Health Score"])

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100

_to_schema = snapshot_row_to_schema


@router.get(
    "/{farm_id}/risk",
    response_model=FarmRiskTrendResponse,
    summary="Get the qualitative condition risk summary for a farm (SIH26131)",
)
async def get_risk(
    farm_id: str,
    service: Annotated[HealthService, Depends(get_health_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmRiskTrendResponse:
    """PRD §7 / contract §2.9 / SIH26131. Returns the qualitative advisory
    and trend indicator without numeric scores or sub-indices."""
    return await service.get_farm_risk(farm_id)


@router.get(
    "/{farm_id}/health",
    response_model=HealthSnapshot,
    summary="Get the current transparent health score for a farm",
)
async def get_health(
    farm_id: str,
    service: Annotated[HealthService, Depends(get_health_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> HealthSnapshot:
    """PRD §7 / contract §2.9. Returns the most recent snapshot, computing and
    persisting an initial one on first read so a new farm sees an explicit
    ``unrated`` state rather than a 404."""
    row = await service.get_latest(farm_id)
    return _to_schema(row)


@router.get(
    "/{farm_id}/health/history",
    response_model=HealthHistoryResponse,
    summary="Get the ordered health-score history for a farm",
)
async def get_health_history(
    farm_id: str,
    service: Annotated[HealthService, Depends(get_health_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_LIMIT)] = DEFAULT_PAGE_LIMIT,
    cursor: Annotated[str | None, Query()] = None,
) -> HealthHistoryResponse:
    """Newest-first, cursor-paginated snapshot history (contract §2.1, §2.9) —
    each entry carries the same full sub-index breakdown so the timeline can
    render why every movement happened."""
    rows, next_cursor = await service.get_history(farm_id, limit=limit, cursor=cursor)
    return HealthHistoryResponse(items=[_to_schema(r) for r in rows], next_cursor=next_cursor)


@router.post(
    "/{farm_id}/health/recompute",
    response_model=HealthSnapshot,
    summary="Force a health-score recompute (demo/admin)",
)
async def recompute_health(
    farm_id: str,
    service: Annotated[HealthService, Depends(get_health_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> HealthSnapshot:
    """Contract §2.9: "handy for walking the numbers live." Any authenticated
    role may trigger it; the contract does not restrict this endpoint by role."""
    row = await service.recompute(farm_id)
    return _to_schema(row)
