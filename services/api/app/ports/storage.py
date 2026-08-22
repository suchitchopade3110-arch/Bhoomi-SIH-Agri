"""Storage port — typed Protocol for S3/MinIO presigned object storage operations."""

from typing import Any, Protocol


class StoragePort(Protocol):
    """Port for S3/MinIO presigned object storage operations."""

    async def generate_presigned_upload_url(
        self,
        asset_id: str,
        file_name: str,
        content_type: str,
        asset_kind: str,
        expires_in: int = 3600,
    ) -> dict[str, Any]:
        """Generate presigned PUT/POST URL for direct client upload."""
        ...

    async def generate_presigned_download_url(
        self,
        asset_id: str,
        expires_in: int = 3600,
    ) -> str:
        """Generate presigned GET URL for retrieving private assets."""
        ...


__all__ = ["StoragePort"]
