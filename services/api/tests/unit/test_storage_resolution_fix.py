"""Regression tests for the asset download URL resolution bug.

Root cause: ``StorageService.get_asset()`` fetched the asset row (which has
the real ``storage_key``, e.g. ``audio_query/{id}/sample.wav``) but never
passed it to ``generate_presigned_download_url()`` — only the bare
``asset_id``. ``StubStorageAdapter`` then built a URL from just the id,
which never matches the real object key, so any consumer resolving a
download URL through the "correct" path (not just the Sarvam ASR adapter's
own guess) got a 404.

Covers:
  1. StubStorageAdapter.generate_presigned_download_url uses storage_key
     when given one, falls back to bare asset_id when not (back-compat).
  2. StorageService.get_asset() passes the row's storage_key through.
  3. VoiceService.transcribe() resolves the real download URL via
     StorageService before calling the ASR adapter, instead of handing it
     a bare asset id.
  4. VoiceService.transcribe() falls back to the raw asset id (old
     behavior) if the asset can't be found, rather than raising.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.adapters.stubs import StubStorageAdapter
from app.core.errors import NotFoundError
from app.repositories.in_memory import InMemoryAssetRepository
from app.schemas.voice import VoiceTranscribeRequest
from app.services.storage_service import StorageService
from app.services.voice_service import VoiceService


class TestStubStorageAdapterDownloadUrl:
    @pytest.mark.asyncio
    async def test_uses_storage_key_when_provided(self):
        adapter = StubStorageAdapter()
        url = await adapter.generate_presigned_download_url(
            "asset-1", storage_key="audio_query/asset-1/sample.wav",
        )
        assert url == "http://localhost:9000/bhoomi-assets/audio_query/asset-1/sample.wav"

    @pytest.mark.asyncio
    async def test_falls_back_to_asset_id_without_storage_key(self):
        adapter = StubStorageAdapter()
        url = await adapter.generate_presigned_download_url("asset-1")
        assert url == "http://localhost:9000/bhoomi-assets/asset-1"


class TestStorageServiceGetAsset:
    @pytest.mark.asyncio
    async def test_get_asset_passes_real_storage_key_to_download_url(self):
        repo = InMemoryAssetRepository()
        await repo.save(
            {
                "id": "asset-1",
                "asset_kind": "audio_query",
                "file_name": "sample.wav",
                "content_type": "audio/wav",
                "storage_key": "audio_query/asset-1/sample.wav",
                "created_at": "2026-08-25T00:00:00",
            }
        )
        service = StorageService(repo, StubStorageAdapter())

        asset = await service.get_asset("asset-1")

        assert asset.download_url == "http://localhost:9000/bhoomi-assets/audio_query/asset-1/sample.wav"


class TestVoiceServiceResolvesRealUrl:
    @pytest.mark.asyncio
    async def test_transcribe_passes_resolved_download_url_to_adapter(self):
        repo = InMemoryAssetRepository()
        await repo.save(
            {
                "id": "asset-1",
                "asset_kind": "audio_query",
                "file_name": "sample.wav",
                "content_type": "audio/wav",
                "storage_key": "audio_query/asset-1/sample.wav",
                "created_at": "2026-08-25T00:00:00",
            }
        )
        storage = StorageService(repo, StubStorageAdapter())

        mock_speech = AsyncMock()
        mock_speech.transcribe_audio.return_value = ("வணக்கம்", 0.9)
        mock_llm = AsyncMock()
        mock_advisory = AsyncMock()

        service = VoiceService(mock_speech, mock_llm, storage, mock_advisory)
        request = VoiceTranscribeRequest(audio_asset_id="asset-1", language="ta", context="general")

        await service.transcribe(request)

        mock_speech.transcribe_audio.assert_called_once_with(
            "http://localhost:9000/bhoomi-assets/audio_query/asset-1/sample.wav", "ta",
        )

    @pytest.mark.asyncio
    async def test_transcribe_falls_back_to_raw_id_when_asset_missing(self):
        repo = InMemoryAssetRepository()  # empty — asset not found
        storage = StorageService(repo, StubStorageAdapter())

        mock_speech = AsyncMock()
        mock_speech.transcribe_audio.return_value = ("வணக்கம்", 0.85)
        mock_llm = AsyncMock()
        mock_advisory = AsyncMock()

        service = VoiceService(mock_speech, mock_llm, storage, mock_advisory)
        request = VoiceTranscribeRequest(audio_asset_id="missing-asset", language="ta", context="general")

        await service.transcribe(request)

        mock_speech.transcribe_audio.assert_called_once_with("missing-asset", "ta")
