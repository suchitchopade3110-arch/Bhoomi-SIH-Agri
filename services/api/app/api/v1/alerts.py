"""Early-Warning Alerts API router (SPEC-ALERT-001, Phase 3 build order Step 4).

Two resources without a shared prefix — ``/farms/{id}/alerts`` (read) and
``/alerts/{id}/acknowledge`` (write) — so this router declares both full
paths rather than using a single ``APIRouter(prefix=...)``.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.alert import AlertAcknowledgeRequest, AlertAcknowledgeResponse, AlertItem, FarmAlertsResponse
from app.services.alerts.alert_service import AlertService, get_alert_service

router = APIRouter(tags=["Early-Warning Alerts"])


@router.get(
    "/farms/{farm_id}/alerts",
    response_model=FarmAlertsResponse,
    summary="Active meteorological and spatial cluster outbreak alerts for a farm",
)
async def get_farm_alerts(
    farm_id: str,
    service: Annotated[AlertService, Depends(get_alert_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmAlertsResponse:
    alerts = await service.evaluate_and_list(farm_id)
    return FarmAlertsResponse(
        farm_id=farm_id,
        active_alerts=[
            AlertItem(
                alert_id=a["id"],
                pathogen_name=a["pathogen_name"],
                severity=a["severity"],
                trigger_reason=a["trigger_reason"],
                preventative_action=a["preventative_action"],
                inspection_tasks=a["inspection_tasks"],
                spoken_summary=a["spoken_summary"],
                created_at=a["created_at"],
                expires_at=a["expires_at"],
            )
            for a in alerts
        ],
    )


@router.post(
    "/alerts/{alert_id}/acknowledge",
    response_model=AlertAcknowledgeResponse,
    summary="Farmer dismiss/confirm-seen for an active alert",
)
async def acknowledge_alert(
    alert_id: str,
    request: AlertAcknowledgeRequest,
    service: Annotated[AlertService, Depends(get_alert_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> AlertAcknowledgeResponse:
    await service.acknowledge(alert_id, request.farm_id, request.reason)
    return AlertAcknowledgeResponse(
        status="acknowledged",
        alert_id=alert_id,
        spoken_summary="Alert acknowledged.",
    )
