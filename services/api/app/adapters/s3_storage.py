"""Real S3/MinIO-compatible storage adapter (``StoragePort``) using boto3.

Selected via ``STORAGE_BACKEND=s3``. Uses ``STORAGE_ENDPOINT`` for both
signing and (implicitly) client reachability — set it to a host actually
reachable from the Flutter app's network, not "localhost", or the presigned
URLs this hands out will be dead on arrival for any client that isn't the
backend host itself (see ``docker-compose``'s ``minio`` service for the
reference deployment this targets).
"""

from __future__ import annotations

from typing import Any

from app.core.config import get_settings


class S3StorageAdapter:
    """``StoragePort`` implementation using a boto3 S3-compatible client."""

    def __init__(self) -> None:
        import boto3
        from botocore.config import Config as BotoConfig

        settings = get_settings()
        self._bucket = settings.STORAGE_BUCKET
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.STORAGE_ENDPOINT,
            aws_access_key_id=settings.STORAGE_ACCESS_KEY,
            aws_secret_access_key=settings.STORAGE_SECRET_KEY,
            region_name=settings.STORAGE_REGION,
            use_ssl=settings.STORAGE_SECURE,
            # MinIO (and most self-hosted S3-compatibles) need path-style
            # addressing — virtual-hosted-style ("bucket.host") only works
            # with real AWS S3 or a DNS setup most local deployments lack.
            config=BotoConfig(signature_version="s3v4", s3={"addressing_style": "path"}),
        )

    async def generate_presigned_upload_url(
        self,
        asset_id: str,
        file_name: str,
        content_type: str,
        asset_kind: str,
        expires_in: int = 3600,
    ) -> dict[str, Any]:
        key = f"{asset_kind}/{asset_id}/{file_name}"
        upload_url = self._client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self._bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=expires_in,
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
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expires_in,
        )


__all__ = ["S3StorageAdapter"]
