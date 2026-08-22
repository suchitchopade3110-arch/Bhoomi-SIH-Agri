"""app/config.py — spec-mandated shim to app.core.config.

The implementation lives in ``app.core.config`` (pydantic-settings, reads
``.env``). This shim exists so the spec-path ``from app.config import ...``
works alongside the existing ``from app.core.config import ...`` path.
"""

from app.core.config import Settings, get_settings, settings  # noqa: F401

__all__ = ["Settings", "get_settings", "settings"]
