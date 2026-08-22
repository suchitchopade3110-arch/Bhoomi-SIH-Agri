"""Image diagnosis port — typed Protocol for crop disease computer vision model inference."""

from typing import Any, Protocol


class ImageDiagnosisPort(Protocol):
    """Port for crop disease computer vision model inference."""

    async def diagnose_crop_image(
        self,
        image_asset_url_or_id: str,
        crop_hint: str | None = None,
    ) -> tuple[str, float, dict[str, Any]]:
        """Run vision model to predict disease label and native model confidence score (0.0 - 1.0)."""
        ...


__all__ = ["ImageDiagnosisPort"]
