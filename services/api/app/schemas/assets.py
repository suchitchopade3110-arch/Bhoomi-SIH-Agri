"""Asset storage and presigned URL schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import AssetKind


class PresignedUploadRequest(BaseModel):
    """Request for presigned upload URL."""
    file_name: str = Field(..., description="Original file name")
    content_type: str = Field(..., description="MIME content type (e.g. image/jpeg, audio/wav)")
    asset_kind: AssetKind = Field(..., description="Asset kind classification")
    farm_id: str | None = Field(default=None, description="Optional associated farm UUID")


class PresignedUploadResponse(BaseModel):
    """Presigned upload URL and asset token."""
    asset_id: str = Field(..., description="UUID string generated for the asset")
    upload_url: str = Field(..., description="Presigned S3/MinIO upload endpoint")
    expires_in: int = Field(default=3600, description="Expiration time in seconds")
    fields: dict[str, str] = Field(default_factory=dict, description="Additional form fields for multipart uploads")


class AssetResponse(BaseModel):
    """Asset metadata response."""
    id: str = Field(..., description="UUID string of the asset")
    asset_kind: AssetKind = Field(..., description="Asset kind classification")
    file_name: str = Field(..., description="File name")
    content_type: str = Field(..., description="MIME type")
    download_url: str = Field(..., description="Presigned GET URL for viewing/downloading")
    created_at: datetime = Field(default_factory=datetime.utcnow)
