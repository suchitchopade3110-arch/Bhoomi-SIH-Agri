"""Orchestration service for Crop Disease Diagnosis and Confidence Gating."""

from typing import Any
from app.schemas.diagnosis import CropDiagnosisRequest, CropDiagnosisResponse


class DiagnosisService:
    """Orchestrates computer vision diagnosis, confidence gating, and escalation routing."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def diagnose_crop_disease(self, request: CropDiagnosisRequest) -> CropDiagnosisResponse:
        """Run vision model, evaluate confidence gate, and route to advisory or escalation."""
        raise NotImplementedError("DiagnosisService.diagnose_crop_disease will be implemented in subsequent phases.")

    async def get_diagnosis_by_id(self, diagnosis_id: str) -> CropDiagnosisResponse:
        """Retrieve diagnosis record by UUID."""
        raise NotImplementedError("DiagnosisService.get_diagnosis_by_id will be implemented in subsequent phases.")
