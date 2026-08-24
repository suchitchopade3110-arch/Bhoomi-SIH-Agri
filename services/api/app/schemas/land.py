"""Cadastral and Land Verification schemas."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from app.core.enums import LandStatus


class BoundaryGeoJSON(BaseModel):
    """GeoJSON geometry polygon."""
    type: str = "Polygon"
    coordinates: list[list[list[float]]] = Field(..., description="Array of polygon linear ring coordinates [lon, lat]")


class CadastralLookupRequest(BaseModel):
    """Automated cadastral lookup query."""
    state: str = Field(default="Tamil Nadu")
    district: str = Field(...)
    taluk: str = Field(...)
    village: str = Field(...)
    survey_number: str = Field(...)
    subdivision: str | None = None


class CadastralLookupResponse(BaseModel):
    """Cadastral lookup result from government records or mock accelerator."""
    found: bool = Field(..., description="Whether parcel was located in cadastral registry")
    survey_number: str = Field(...)
    owner_name: str | None = None
    area_acres: float | None = None
    boundary_geojson: dict[str, Any] | None = None
    source: str = Field(default="mock_tn_edistrict", description="Source provider")


class LandVerifyRequest(BaseModel):
    """Submission of land parcel for officer verification."""
    farm_id: str = Field(..., description="UUID string of farm")
    survey_number: str = Field(...)
    patta_passbook_asset_id: str | None = None
    suggested_boundary: dict[str, Any] | None = None


class LandVerifyResponse(BaseModel):
    """Land verification status response."""
    parcel_id: str = Field(..., description="UUID string of parcel record")
    farm_id: str = Field(...)
    status: LandStatus = Field(...)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    officer_notes: str | None = None


class ThinLandVerification(BaseModel):
    """Thin land status schema without cut boundary/geometry fields (SIH26131)."""
    farm_id: str = Field(..., description="UUID string of farm")
    status: LandStatus = Field(..., description="Thin status: pending_verification | verified | rejected")
    last_verified_at: datetime | None = Field(default=None, description="Timestamp of status update")

