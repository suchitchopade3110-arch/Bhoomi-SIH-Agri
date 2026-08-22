"""Port + adapters for cadastral (land registry) auto-lookup — PRD §5.3,
contract §1.5/§2.7.

Not one of the contract's six named ports (Weather/LLM/Embedding/
ImageDiagnosis/AsrTts/Storage), but the contract explicitly calls out
``LAND_API_MODE`` as a feature flag selecting between a mock and a live
adapter (§1.5), so it gets the same Protocol-plus-two-implementations shape
as every other external dependency (see module docstring in ``ports.py``).

Design (PRD §5.3, §5.6 risk #2 — "land APIs are fragmented/unavailable"):
  * ``MockLandRegistryAdapter`` (``LAND_API_MODE=mock``) simulates a working
    accelerator: survey numbers on the curated demo whitelist resolve
    instantly; anything else — the common case per the contract — falls
    into HITL.
  * ``LiveLandRegistryAdapter`` (``LAND_API_MODE=live``) represents the real
    government portal integration this project doesn't have (PRD §2.2 non-
    goal: "nationwide land-record API coverage"). It always reports
    ``failed`` — an honest simulation of exactly the fragmentation risk the
    PRD names, not a fake success.

Flipping the flag alone — no input changes — is what lets the demo show
both contract §2.7 response shapes (202 queued-to-officer vs. 200 verified)
from the same build (PRD §1.5).
"""

from typing import Any, Protocol


class LandRegistryPort(Protocol):
    """Port for automated cadastral boundary lookup."""

    async def lookup(
        self,
        survey_number: str,
        district: str,
        taluk: str,
        village: str,
    ) -> dict[str, Any]:
        """Attempt an automated cadastral match.

        Returns:
            ``{"matched": bool, "area_acres": float | None,
            "owner_name": str | None, "boundary_geojson": dict | None,
            "source": str}``.
        """
        ...


# Survey numbers the mock accelerator "recognizes" — anything else fails
# into HITL, which is deliberately the common path (PRD §5.3).
MOCK_KNOWN_SURVEY_NUMBERS: frozenset[str] = frozenset({"88/2A", "SAMPLE-001"})

_MOCK_BOUNDARY_GEOJSON = {
    "type": "Polygon",
    "coordinates": [[[77.71, 11.34], [77.712, 11.34], [77.712, 11.342], [77.71, 11.342], [77.71, 11.34]]],
}


class MockLandRegistryAdapter:
    """``LAND_API_MODE=mock``: deterministic accelerator over a small whitelist."""

    async def lookup(self, survey_number: str, district: str, taluk: str, village: str) -> dict[str, Any]:
        if survey_number in MOCK_KNOWN_SURVEY_NUMBERS:
            return {
                "matched": True,
                "area_acres": 2.0,
                "owner_name": "Registry Record Holder",
                "boundary_geojson": _MOCK_BOUNDARY_GEOJSON,
                "source": "mock_tn_edistrict",
            }
        return {"matched": False, "area_acres": None, "owner_name": None, "boundary_geojson": None, "source": "mock_tn_edistrict"}


class LiveLandRegistryAdapter:
    """``LAND_API_MODE=live``: the real state land-record portal this project
    does not integrate with (PRD §2.2 non-goal). Always reports ``failed`` —
    real coverage is fragmented/unavailable, so HITL is correctly the only
    path, not a bug to work around."""

    async def lookup(self, survey_number: str, district: str, taluk: str, village: str) -> dict[str, Any]:
        return {"matched": False, "area_acres": None, "owner_name": None, "boundary_geojson": None, "source": "live_state_portal_unavailable"}
