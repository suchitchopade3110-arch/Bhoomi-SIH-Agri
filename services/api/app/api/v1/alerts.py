"""Early-Warning Alerts API router (SPEC-ALERT-001, delta spec §3.2-3.3).

Two resources without a shared prefix — ``/farms/{id}/alerts`` (read) and
``/alerts/{id}/dismiss`` (write) — so this router declares both full paths
rather than using a single ``APIRouter(prefix=...)``.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.alert import AlertDismissRequest, AlertDismissResponse, AlertItem, FarmAlertsResponse
from app.services.alert_service import AlertService, get_alert_service

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
                spoken_summary=a["spoken_summary"],
                created_at=a["created_at"],
                expires_at=a["expires_at"],
            )
            for a in alerts
        ],
    )


@router.post(
    "/alerts/{alert_id}/dismiss",
    response_model=AlertDismissResponse,
    summary="Dismiss/acknowledge an active alert",
)
async def dismiss_alert(
    alert_id: str,
    request: AlertDismissRequest,
    service: Annotated[AlertService, Depends(get_alert_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> AlertDismissResponse:
    await service.dismiss(alert_id, request.farm_id, request.reason)
    return AlertDismissResponse(status="dismissed", alert_id=alert_id)
