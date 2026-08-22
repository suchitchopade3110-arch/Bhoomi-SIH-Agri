"""Real ``ImageDiagnosisPort`` adapter (``DIAGNOSIS_MODEL=real``).

PRD §1: "Image disease model ... served in-process" or, per the tech-stack
alternative, "Hosted inference (Hugging Face) if you don't want the weights
in the API" — this project's chosen split puts it behind ``services/ml``
(``settings.ML_SERVICE_URL``), a separate small inference process.

That ML microservice is its own phase (not this one — "Build ONLY the phase
I name") and is not implemented yet, so this adapter is the real integration
point wired and selectable today: setting ``DIAGNOSIS_MODEL=real`` swaps it
in with zero call-site changes anywhere in ``services/``, exactly as the
port-and-adapter contract requires. Until the ML service exists, a real
call fails loudly (connection error) rather than silently returning a
plausible-looking guess — which is the correct behavior for a diagnosis
port: never fabricate a confidence score.
"""

from typing import Any

import httpx

DIAGNOSIS_ENDPOINT_PATH = "/diagnose"
REQUEST_TIMEOUT_SECONDS = 10.0


class RealImageDiagnosisAdapter:
    """Calls the ``services/ml`` image-diagnosis inference endpoint over HTTP."""

    def __init__(self, ml_service_url: str) -> None:
        self._base_url = ml_service_url.rstrip("/")

    async def diagnose_crop_image(
        self,
        image_asset_url_or_id: str,
        crop_hint: str | None = None,
    ) -> tuple[str, float, dict[str, Any]]:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"{self._base_url}{DIAGNOSIS_ENDPOINT_PATH}",
                json={"asset_id": image_asset_url_or_id, "crop_hint": crop_hint},
            )
            response.raise_for_status()
            payload = response.json()
        return payload["label"], float(payload["confidence"]), payload.get("meta", {})
