"""Treatment Efficacy API router (SPEC-EFFICACY-001 §3.4, §6). SIH26131-only."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_token_payload
from app.domain.efficacy import normalize_treatment_key
from app.schemas.efficacy import EfficacyResponse
from app.services.efficacy.aggregator_service import (
    DEFAULT_WINDOW_MONTHS,
    EfficacyAggregatorService,
    get_efficacy_aggregator_service,
)

router = APIRouter(prefix="/treatments", tags=["Treatment Efficacy"])


@router.get(
    "/{treatment_id}/efficacy",
    response_model=EfficacyResponse,
    summary="Population-level real-world efficacy for one (pathogen, treatment, crop, district) combination",
)
async def get_treatment_efficacy(
    treatment_id: str,
    pathogen: Annotated[str, Query(description="Pathogen/pest label, e.g. 'bacterial_leaf_blight'")],
    crop: Annotated[str, Query(description="Crop key, e.g. 'samba_paddy'")],
    district: Annotated[str, Query(description="District name, e.g. 'Erode'")],
    service: Annotated[EfficacyAggregatorService, Depends(get_efficacy_aggregator_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    window_months: Annotated[int, Query(ge=1, le=60, description="Trailing evaluation window in months")] = (
        DEFAULT_WINDOW_MONTHS
    ),
) -> EfficacyResponse:
    """Spec §2: below the sample-size floor (N < 10), returns
    ``status: insufficient_data`` rather than a misleading small-sample
    percentage — never `1/1 = 100%`."""
    result = await service.get_efficacy(
        treatment_name=normalize_treatment_key(treatment_id),
        pathogen_type=pathogen,
        crop=crop,
        district=district,
        window_months=window_months,
    )
    return EfficacyResponse(
        treatment_id=result.treatment_id,
        pathogen=result.pathogen,
        crop=result.crop,
        region=result.region,
        status=result.status,
        sample_size=result.sample_size,
        min_sample_threshold=result.min_sample_threshold,
        efficacy_percentage=result.efficacy_percentage,
        avg_days_to_recovery=result.avg_days_to_recovery,
    )
