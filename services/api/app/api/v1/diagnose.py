"""Crop Disease Diagnosis API router."""

from fastapi import APIRouter, status
from app.core.errors import NotImplementedAPIError
from app.schemas.diagnosis import (
    CropDiagnosisRequest,
    CropDiagnosisResponse,
)

router = APIRouter(prefix="/diagnose", tags=["Diagnosis & Vision"])


@router.post(
    "/crop-disease",
    response_model=CropDiagnosisResponse,
    status_code=status.HTTP_200_OK,
    summary="Run computer vision model to diagnose crop disease from photo asset",
)
async def diagnose_crop_disease(request: CropDiagnosisRequest) -> CropDiagnosisResponse:
    raise NotImplementedAPIError("Endpoint POST /diagnose/crop-disease will be implemented in subsequent phases.")


@router.get(
    "/{diagnosis_id}",
    response_model=CropDiagnosisResponse,
    summary="Get diagnosis result details and confidence gate decision",
)
async def get_diagnosis(diagnosis_id: str) -> CropDiagnosisResponse:
    raise NotImplementedAPIError("Endpoint GET /diagnose/{diagnosis_id} will be implemented in subsequent phases.")
