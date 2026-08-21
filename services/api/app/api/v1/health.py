"""Farm Health Score API router (contract §2.9)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.enums import HealthBand
from app.core.security import get_current_token_payload
from app.models.health_snapshot import HealthSnapshot as HealthSnapshotRow
from app.schemas.health import HealthHistoryResponse, HealthSnapshot, SubIndexBreakdown
from app.services.health_service import HealthService, get_health_service

router = APIRouter(prefix="/farms", tags=["Farm Health Score"])

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100


def _spoken_summary(row: HealthSnapshotRow) -> str:
    """Short, voice-first summary for local TTS (PRD §5.1, contract §1.4)."""
    if row.band == HealthBand.UNRATED.value:
        return "Your farm health score is not yet available. A few more details are needed."
    summary = f"Your farm health score is {row.score}, which is {row.band}."
    trigger_type = (row.triggering_input or {}).get("type")
    if trigger_type == "diagnosis":
        summary += " This reflects an active problem on your farm."
    elif trigger_type == "followup":
        summary += " This reflects your latest follow-up report."
    elif trigger_type == "case_resolution":
        summary += " Your problem has been resolved."
    return summary


def _to_schema(row: HealthSnapshotRow) -> HealthSnapshot:
    """Map a persisted ``HealthSnapshot`` row onto the contract §2.9 response shape."""
    return HealthSnapshot(
        score=row.score,
        band=HealthBand(row.band),
        computed_at=row.computed_at,
        weights_version=row.weights_version,
        subindices=[SubIndexBreakdown(**s) for s in row.subindices],
        triggering_input=row.triggering_input,
        missing_fields=row.missing_fields,
        spoken_summary=_spoken_summary(row),
    )


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
