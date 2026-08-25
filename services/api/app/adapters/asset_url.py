"""Shared helper for building a placeholder asset URL from configured storage settings.

Voice adapters (stub / gTTS / Sarvam / Bhashini) need to hand back *some*
audio URL when they can't go through the real upload flow (no credentials
configured, or the provider call itself failed) — this builds that URL from
``STORAGE_ENDPOINT``/``STORAGE_BUCKET`` instead of a bare hardcoded
``localhost:9000`` literal, so it at least points at wherever storage is
actually configured to live rather than a host nothing is listening on once
deployed anywhere but the developer's own machine.
"""

from __future__ import annotations

from app.core.config import get_settings


def fallback_asset_url(asset_id: str, extension: str) -> str:
    """Build a ``{STORAGE_ENDPOINT}/{STORAGE_BUCKET}/{asset_id}.{extension}`` URL."""
    settings = get_settings()
    endpoint = getattr(settings, "STORAGE_ENDPOINT", "http://localhost:9000").rstrip("/")
    bucket = getattr(settings, "STORAGE_BUCKET", "bhoomi-assets")
    return f"{endpoint}/{bucket}/{asset_id}.{extension}"


__all__ = ["fallback_asset_url"]
