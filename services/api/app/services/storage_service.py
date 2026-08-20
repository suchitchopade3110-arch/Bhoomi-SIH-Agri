"""Presigned asset storage service."""

from typing import Any
from app.schemas.assets import AssetResponse, PresignedUploadRequest, PresignedUploadResponse


class StorageService:
    """Manages presigned direct uploads and download URL generation."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def create_presigned_upload(self, request: PresignedUploadRequest) -> PresignedUploadResponse:
        raise NotImplementedError("StorageService.create_presigned_upload will be implemented in subsequent phases.")

    async def get_asset(self, asset_id: str) -> AssetResponse:
        raise NotImplementedError("StorageService.get_asset will be implemented in subsequent phases.")
