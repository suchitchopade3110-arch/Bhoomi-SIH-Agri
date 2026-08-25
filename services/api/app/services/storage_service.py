"""Presigned upload / asset metadata service (contract §2.4, PRD §1.4)."""

from typing import Annotated
import uuid

from fastapi import Depends

from app.adapters.dependencies import get_storage_adapter
from app.ports.storage import StoragePort
from app.core.errors import NotFoundError
from app.repositories.dependencies import get_asset_repository
from app.repositories.interfaces import AssetRepository
from app.schemas.assets import AssetResponse, PresignedUploadRequest, PresignedUploadResponse


class StorageService:
    """Issues presigned upload URLs and resolves asset metadata."""

    def __init__(self, asset_repo: AssetRepository, storage: StoragePort) -> None:
        self._assets = asset_repo
        self._storage = storage

    async def create_presigned_upload(self, request: PresignedUploadRequest) -> PresignedUploadResponse:
        asset_id = str(uuid.uuid4())
        presign = await self._storage.generate_presigned_upload_url(
            asset_id=asset_id,
            file_name=request.file_name,
            content_type=request.content_type,
            asset_kind=request.asset_kind.value,
        )
        await self._assets.save(
            {
                "id": asset_id,
                "asset_kind": request.asset_kind.value,
                "file_name": request.file_name,
                "content_type": request.content_type,
                "farm_id": request.farm_id,
                "storage_key": presign.get("fields", {}).get("key", asset_id),
            }
        )
        return PresignedUploadResponse(
            asset_id=asset_id,
            upload_url=presign["upload_url"],
            expires_in=presign.get("expires_in", 3600),
            fields=presign.get("fields", {}),
        )

    async def get_asset(self, asset_id: str) -> AssetResponse:
        row = await self._assets.get_by_id(asset_id)
        if row is None:
            raise NotFoundError("Asset not found.", details={"asset_id": asset_id})
        download_url = await self._storage.generate_presigned_download_url(
            asset_id, storage_key=row.get("storage_key"),
        )
        return AssetResponse(
            id=row["id"],
            asset_kind=row["asset_kind"],
            file_name=row["file_name"],
            content_type=row["content_type"],
            download_url=download_url,
            created_at=row["created_at"],
        )


def get_storage_service(
    asset_repo: Annotated[AssetRepository, Depends(get_asset_repository)],
    storage: Annotated[StoragePort, Depends(get_storage_adapter)],
) -> StorageService:
    return StorageService(asset_repo, storage)
