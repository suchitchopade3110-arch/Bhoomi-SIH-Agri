"""Asset Storage API router."""

from fastapi import APIRouter, status
from app.core.errors import NotImplementedAPIError
from app.schemas.assets import (
    AssetResponse,
    PresignedUploadRequest,
    PresignedUploadResponse,
)

router = APIRouter(prefix="/assets", tags=["Assets & Storage"])


@router.post(
    "/presigned-url",
    response_model=PresignedUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Get presigned S3/MinIO upload URL for direct blob transfer",
)
async def generate_presigned_url(request: PresignedUploadRequest) -> PresignedUploadResponse:
    raise NotImplementedAPIError("Endpoint POST /assets/presigned-url will be implemented in subsequent phases.")


@router.get(
    "/{asset_id}",
    response_model=AssetResponse,
    summary="Get asset metadata and secure download URL",
)
async def get_asset(asset_id: str) -> AssetResponse:
    raise NotImplementedAPIError("Endpoint GET /assets/{asset_id} will be implemented in subsequent phases.")
