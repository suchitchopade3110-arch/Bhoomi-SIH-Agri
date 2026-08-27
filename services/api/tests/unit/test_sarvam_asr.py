"""Sarvam AI ASR/TTS Adapter unit tests.

Covers:
  - transcribe_audio() with no API key returns valid (str, float) fallback without network calls
  - synthesize_speech() with no API key returns valid (str, str) fallback with valid URL
  - transcribe_audio() with mocked 200 response parses transcript and confidence
  - synthesize_speech() with mocked 200 response decodes base64 and returns asset url
  - Mock httpx non-200 and network exception: adapter falls back gracefully instead of raising
  - Dependency wiring: get_speech_adapter() selects SarvamAsrTtsAdapter when ASR_PROVIDER=sarvam
"""

from __future__ import annotations

import base64
import httpx
import pytest
from unittest.mock import AsyncMock, patch

from app.adapters.sarvam_asr import SarvamAsrTtsAdapter
from app.adapters.dependencies import get_speech_adapter


class TestSarvamAsrTtsAdapter:
    """Unit tests for SarvamAsrTtsAdapter."""

    @pytest.mark.asyncio
    async def test_transcribe_no_key_returns_fallback_without_network(self):
        """transcribe_audio() with no API key returns valid (str, float) tuple without network call."""
        adapter = SarvamAsrTtsAdapter(api_key="")
        with patch("httpx.AsyncClient") as mock_client:
            text, confidence = await adapter.transcribe_audio("audio-asset-123", language="ta")
            mock_client.assert_not_called()
            assert isinstance(text, str)
            assert len(text) > 0
            assert isinstance(confidence, float)
            assert 0.0 <= confidence <= 1.0

    @pytest.mark.asyncio
    async def test_synthesize_no_key_returns_fallback_without_network(self):
        """synthesize_speech() with no API key returns valid (str, str) tuple where URL starts with 'http'."""
        adapter = SarvamAsrTtsAdapter(api_key="")
        with patch("httpx.AsyncClient") as mock_client:
            asset_id, audio_url = await adapter.synthesize_speech("வணக்கம்", language="ta", gender="female")
            mock_client.assert_not_called()
            assert isinstance(asset_id, str)
            assert len(asset_id) > 0
            assert isinstance(audio_url, str)
            assert audio_url.startswith("http")

    @pytest.mark.asyncio
    async def test_transcribe_mock_success_response(self):
        """transcribe_audio() with successful 200 response fetches bytes, sends multipart upload, and returns transcript."""
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")
        fake_audio_bytes = b"RIFFfakeaudiobytes12345"
        mock_get_response = httpx.Response(
            status_code=200,
            content=fake_audio_bytes,
            request=httpx.Request("GET", "https://example.com/sample.wav"),
        )
        mock_post_response = httpx.Response(
            status_code=200,
            json={"transcript": "என் நிலம் இரண்டு ஏக்கர் சம்பா நெல்"},
            request=httpx.Request("POST", "https://api.sarvam.ai/speech-to-text"),
        )

        with (
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
        ):
            mock_get.return_value = mock_get_response
            mock_post.return_value = mock_post_response

            text, confidence = await adapter.transcribe_audio("https://example.com/sample.wav", language="ta")

            assert text == "என் நிலம் இரண்டு ஏக்கர் சம்பா நெல்"
            assert confidence == 0.90
            mock_get.assert_called_once_with("https://example.com/sample.wav")
            mock_post.assert_called_once()

            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["headers"]["api-subscription-key"] == "test-sarvam-key"
            assert call_kwargs["data"] == {"model": "saaras:v3", "language_code": "ta-IN"}
            assert "file" in call_kwargs["files"]
            filename, file_bytes, mime = call_kwargs["files"]["file"]
            assert filename == "audio.wav"
            assert file_bytes == fake_audio_bytes
            assert mime == "audio/wav"

    @pytest.mark.asyncio
    async def test_transcribe_resolves_asset_id_via_storage(self):
        """Adapter's own bare-id -> URL guess (last-resort fallback only).

        In the real flow, ``VoiceService`` now resolves the actual
        storage-key-based download URL via ``StorageService`` before ever
        calling this adapter (see test_storage_resolution_fix.py) — this
        guess only fires if a caller hands the adapter a bare id directly
        (e.g. asset lookup failed upstream). It won't match a real object
        key, so it's a fallback path, not the primary one.
        """
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")
        fake_audio_bytes = b"RIFFfakeaudiobytes12345"
        mock_get_response = httpx.Response(
            status_code=200,
            content=fake_audio_bytes,
            request=httpx.Request("GET", "http://localhost:9000/bhoomi-assets/asset-uuid-456"),
        )
        mock_post_response = httpx.Response(
            status_code=200,
            json={"transcript": "வணக்கம்"},
            request=httpx.Request("POST", "https://api.sarvam.ai/speech-to-text"),
        )

        with (
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
        ):
            mock_get.return_value = mock_get_response
            mock_post.return_value = mock_post_response

            text, confidence = await adapter.transcribe_audio("asset-uuid-456", language="ta")

            assert text == "வணக்கம்"
            mock_get.assert_called_once_with("http://localhost:9000/bhoomi-assets/asset-uuid-456")

    @pytest.mark.asyncio
    async def test_synthesize_mock_success_response(self):
        """synthesize_speech() with successful 200 response decodes the real
        audio bytes and pushes them through StoragePort — it must not just
        fabricate a plausible-looking URL for audio nothing actually stored.
        """
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")
        dummy_audio_bytes = b"RIFFdummywavdata"
        dummy_audio_b64 = base64.b64encode(dummy_audio_bytes).decode("utf-8")
        mock_response = httpx.Response(
            status_code=200,
            json={"audios": [dummy_audio_b64]},
            request=httpx.Request("POST", "https://api.sarvam.ai/text-to-speech"),
        )
        mock_upload_response = httpx.Response(
            status_code=200,
            request=httpx.Request("PUT", "http://testserver/upload"),
        )

        mock_storage = AsyncMock()
        mock_storage.generate_presigned_upload_url.return_value = {
            "upload_url": "http://testserver/upload",
            "fields": {"key": "voice_synthesis/asset/clip.wav"},
        }
        mock_storage.generate_presigned_download_url.return_value = "http://testserver/static/assets/clip.wav"

        with (
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
            patch("httpx.AsyncClient.put", new_callable=AsyncMock) as mock_put,
            patch("app.adapters.dependencies.get_storage_adapter", return_value=mock_storage),
        ):
            mock_post.return_value = mock_response
            mock_put.return_value = mock_upload_response
            asset_id, audio_url = await adapter.synthesize_speech("வணக்கம்", language="ta", gender="female")

            assert isinstance(asset_id, str)
            assert audio_url == "http://testserver/static/assets/clip.wav"
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["headers"]["api-subscription-key"] == "test-sarvam-key"
            assert call_kwargs["json"]["model"] == "bulbul:v3"
            assert call_kwargs["json"]["target_language_code"] == "ta-IN"

            # The real decoded audio bytes are what actually got uploaded —
            # not just a URL shaped like one.
            put_call_kwargs = mock_put.call_args.kwargs
            assert put_call_kwargs["content"] == dummy_audio_bytes
            # Must resolve using the real storage key the upload was written
            # under (voice_synthesis/asset/clip.wav), not the bare file_name
            # — a download URL built from file_name alone 404s in practice.
            mock_storage.generate_presigned_download_url.assert_called_once_with(
                asset_id, storage_key="voice_synthesis/asset/clip.wav"
            )

    @pytest.mark.asyncio
    async def test_synthesize_falls_back_when_storage_upload_fails(self):
        """If the real synthesis succeeds but the storage upload fails,
        synthesize_speech() falls back to the placeholder URL rather than
        claiming a download link for audio that was never actually stored.
        """
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")
        dummy_audio_b64 = base64.b64encode(b"RIFFdummywavdata").decode("utf-8")
        mock_response = httpx.Response(
            status_code=200,
            json={"audios": [dummy_audio_b64]},
            request=httpx.Request("POST", "https://api.sarvam.ai/text-to-speech"),
        )

        mock_storage = AsyncMock()
        mock_storage.generate_presigned_upload_url.side_effect = RuntimeError("storage unreachable")

        with (
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
            patch("app.adapters.dependencies.get_storage_adapter", return_value=mock_storage),
        ):
            mock_post.return_value = mock_response
            asset_id, audio_url = await adapter.synthesize_speech("வணக்கம்", language="ta")

            assert isinstance(asset_id, str)
            assert audio_url.startswith("http")
            assert audio_url.endswith(".mp3")

    @pytest.mark.asyncio
    async def test_transcribe_mock_http_error_falls_back_gracefully(self):
        """transcribe_audio() gracefully degrades on non-200 response without raising."""
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")
        mock_response = httpx.Response(
            status_code=500,
            content=b"Internal Server Error",
            request=httpx.Request("POST", "https://api.sarvam.ai/speech-to-text"),
        )

        with (
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
        ):
            mock_get.return_value = httpx.Response(status_code=200, content=b"audiobytes")
            mock_post.return_value = mock_response
            text, confidence = await adapter.transcribe_audio("audio-123", language="ta")
            assert isinstance(text, str)
            assert len(text) > 0
            assert isinstance(confidence, float)

    @pytest.mark.asyncio
    async def test_synthesize_mock_http_error_falls_back_gracefully(self):
        """synthesize_speech() gracefully degrades on non-200 response without raising."""
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")
        mock_response = httpx.Response(
            status_code=401,
            content=b"Unauthorized",
            request=httpx.Request("POST", "https://api.sarvam.ai/text-to-speech"),
        )

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            asset_id, audio_url = await adapter.synthesize_speech("வணக்கம்", language="ta")
            assert isinstance(asset_id, str)
            assert audio_url.startswith("http")

    @pytest.mark.asyncio
    async def test_network_exception_falls_back_gracefully(self):
        """transcribe_audio() and synthesize_speech() catch network exceptions and degrade gracefully."""
        adapter = SarvamAsrTtsAdapter(api_key="test-sarvam-key")

        with (
            patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get,
            patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post,
        ):
            mock_get.side_effect = httpx.ConnectError("Connection refused")
            text, confidence = await adapter.transcribe_audio("audio-123", language="ta")
            assert isinstance(text, str)
            assert isinstance(confidence, float)

            mock_post.side_effect = httpx.ConnectError("Connection refused")
            asset_id, audio_url = await adapter.synthesize_speech("வணக்கம்", language="ta")
            assert isinstance(asset_id, str)
            assert audio_url.startswith("http")

    def test_get_speech_adapter_resolves_sarvam_provider(self):
        """get_speech_adapter() returns a SarvamAsrTtsAdapter when ASR_PROVIDER is 'sarvam'."""
        get_speech_adapter.cache_clear()
        with patch("app.adapters.dependencies.get_settings") as mock_settings:
            mock_settings.return_value.ASR_PROVIDER = "sarvam"
            adapter = get_speech_adapter()
            assert isinstance(adapter, SarvamAsrTtsAdapter)
        get_speech_adapter.cache_clear()
