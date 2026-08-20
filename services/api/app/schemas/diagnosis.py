"""Crop disease diagnosis schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin
from app.schemas.gate import Decision


class CropDiagnosisRequest(BaseModel):
    """Request to diagnose crop disease from photo asset."""
    farm_id: str = Field(..., description="UUID string of farm context")
    photo_asset_id: str = Field(..., description="UUID string of uploaded disease image")
    crop_type: str | None = Field(default=None, description="Optional crop hint to constrain model")
    symptoms_description: str | None = Field(default=None, description="Optional farmer-provided text/voice description")


class CropDiagnosisResponse(SpokenResponseMixin):
    """Disease diagnosis response including confidence gate evaluation."""
    diagnosis_id: str = Field(..., description="UUID string of diagnosis event")
    crop: str = Field(...)
    predicted_disease: str = Field(..., description="Identified disease or pest label")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Raw model confidence score")
    gate_decision: Decision = Field(..., description="Confidence gate evaluation outcome")
    advisory_id: str | None = Field(default=None, description="Generated advisory UUID if confidence passed")
    escalation_id: str | None = Field(default=None, description="Escalation UUID if confidence failed gate")
    created_at: datetime = Field(default_factory=datetime.utcnow)
