"""Asset Storage API router (contract §2.4)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_token_payload
from app.schemas.assets import (
    AssetResponse,
    PresignedUploadRequest,
    PresignedUploadResponse,
)
from app.services.storage_service import StorageService, get_storage_service

router = APIRouter(prefix="/assets", tags=["Assets & Storage"])


@router.post(
    "/presigned-url",
    response_model=PresignedUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Get presigned S3/MinIO upload URL for direct blob transfer",
)
async def generate_presigned_url(
    request: PresignedUploadRequest,
    service: Annotated[StorageService, Depends(get_storage_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> PresignedUploadResponse:
    return await service.create_presigned_upload(request)


@router.get(
    "/{asset_id}",
    response_model=AssetResponse,
    summary="Get asset metadata and secure download URL",
)
async def get_asset(
    asset_id: str,
    service: Annotated[StorageService, Depends(get_storage_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> AssetResponse:
    return await service.get_asset(asset_id)
