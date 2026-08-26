"""Asset Storage API router (contract §2.4)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, status

from app.adapters.dependencies import get_storage_adapter
from app.core.errors import ValidationError
from app.core.security import get_current_token_payload
from app.ports.storage import StoragePort
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


@router.put(
    "/local-upload/{asset_kind}/{asset_id}/{file_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Receive raw bytes for the local ``STORAGE_BACKEND`` (mimics a presigned PUT)",
    include_in_schema=False,
)
async def local_upload(
    asset_kind: str,
    asset_id: str,
    file_name: str,
    request: Request,
    storage: Annotated[StoragePort, Depends(get_storage_adapter)],
) -> None:
    """Write the request body to disk under the local storage backend.

    Only meaningful when ``STORAGE_BACKEND=local`` — this is the endpoint
    ``LocalStorageAdapter.generate_presigned_upload_url`` hands back as the
    "upload_url", standing in for a real presigned S3 PUT so the same
    upload-then-fetch flow (used by e.g. the gTTS adapter) works with zero
    external storage infra.
    """
    if not hasattr(storage, "write_bytes"):
        raise ValidationError(
            "Local upload endpoint is only available when STORAGE_BACKEND=local.",
        )
    body = await request.body()
    key = f"{asset_kind}/{asset_id}/{file_name}"
    storage.write_bytes(key, body)
