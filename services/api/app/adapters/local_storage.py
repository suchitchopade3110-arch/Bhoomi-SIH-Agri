"""Local-filesystem storage adapter — zero-infra ``StoragePort`` implementation.

Writes uploaded bytes under ``LOCAL_STORAGE_PATH`` and serves them back from
this same API process (mounted as static files in ``app.main``), so the
"presigned" upload/download URLs it hands out are just ordinary endpoints on
``PUBLIC_BASE_URL`` — the same host the Flutter app already talks to for
every other request. That sidesteps the "localhost only resolves on the
server itself" trap that a hardcoded MinIO-style URL falls into when nothing
real is listening there.

Intended as the default/demo backend (``STORAGE_BACKEND=local``); switch to
``S3StorageAdapter`` (``STORAGE_BACKEND=s3``) for a real S3/MinIO deployment.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import quote

from app.core.config import get_settings


class LocalStorageAdapter:
    """``StoragePort`` implementation backed by the local filesystem."""

    def __init__(self) -> None:
        settings = get_settings()
        self._root = Path(settings.LOCAL_STORAGE_PATH).resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        self._public_base_url = settings.PUBLIC_BASE_URL.rstrip("/")
        self._api_v1_str = settings.API_V1_STR

    async def generate_presigned_upload_url(
        self,
        asset_id: str,
        file_name: str,
        content_type: str,
        asset_kind: str,
        expires_in: int = 3600,
    ) -> dict[str, Any]:
        key = f"{asset_kind}/{asset_id}/{file_name}"
        upload_url = (
            f"{self._public_base_url}{self._api_v1_str}/assets/local-upload/"
            f"{quote(asset_kind)}/{quote(asset_id)}/{quote(file_name)}"
        )
        return {
            "asset_id": asset_id,
            "upload_url": upload_url,
            "expires_in": expires_in,
            "fields": {"key": key},
        }

    async def generate_presigned_download_url(
        self,
        asset_id: str,
        storage_key: str | None = None,
        expires_in: int = 3600,
    ) -> str:
        key = storage_key or asset_id
        return f"{self._public_base_url}/static/assets/{quote(key)}"

    def resolve_path(self, key: str) -> Path:
        """Map a storage key to an on-disk path, guarding against traversal."""
        candidate = (self._root / key).resolve()
        if self._root not in candidate.parents and candidate != self._root:
            raise ValueError("Invalid storage key.")
        return candidate

    def write_bytes(self, key: str, data: bytes) -> None:
        path = self.resolve_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


__all__ = ["LocalStorageAdapter"]
