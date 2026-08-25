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
        storage_key: str | None = None,
        expires_in: int = 3600,
    ) -> str:
        """Generate presigned GET URL for retrieving private assets.

        ``storage_key`` is the actual object key recorded at upload time
        (``{asset_kind}/{asset_id}/{file_name}``) — required to resolve the
        real object location. Optional only so existing callers that don't
        yet have the row (e.g. tests constructing bare adapters) don't break;
        callers that have the asset row must pass it.
        """
        ...


__all__ = ["StoragePort"]
