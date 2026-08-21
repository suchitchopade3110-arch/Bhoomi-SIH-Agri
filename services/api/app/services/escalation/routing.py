"""Nearest-available-agronomist routing (PRD §5.11, Phase 4 item 3).

The routing interface itself is real — a genuine nearest-district-then-any-
available directory query — even though the default config
(``AGRONOMIST_ROUTING_MODE=demo_fixed``) hard-assigns a single seeded
agronomist, since no real agronomist geodata/farm-district data is seeded
yet. Flip the flag to ``directory`` once that data exists; nothing else in
the escalation subsystem changes.
"""

from dataclasses import dataclass

from app.core.config import Settings
from app.core.errors import OfficerUnavailableError
from app.repositories.agronomist_repository import AgronomistDirectory


@dataclass(frozen=True)
class AssignedAgronomist:
    agronomist_id: str
    name: str
    kvk_center: str


class AgronomistRouter:
    """Assigns one available agronomist to a new case."""

    def __init__(self, directory: AgronomistDirectory, settings: Settings) -> None:
        self._directory = directory
        self._settings = settings

    async def assign(self, district: str | None) -> AssignedAgronomist:
        """Pick an agronomist for a case in ``district`` (or an unknown farm's
        ``None`` district).

        Args:
            district: The escalating farm's district, or ``None`` if unknown.

        Returns:
            The assigned ``AssignedAgronomist``.

        Raises:
            OfficerUnavailableError: contract §2.1's stable ``OFFICER_UNAVAILABLE``
                code — only once every agronomist in the directory has been
                tried and none is available.
        """
        if self._settings.AGRONOMIST_ROUTING_MODE == "demo_fixed":
            agro = await self._directory.get_by_name(self._settings.DEMO_AGRONOMIST_NAME)
            if agro is None:
                raise OfficerUnavailableError(
                    message="The demo agronomist is not seeded; run migrations first.",
                    details={"demo_agronomist_name": self._settings.DEMO_AGRONOMIST_NAME},
                )
            return AssignedAgronomist(agro.id, agro.name, agro.kvk_center)

        # "directory" mode: nearest (same district), falling through to any
        # available agronomist elsewhere — only a fully exhausted directory
        # surfaces OFFICER_UNAVAILABLE.
        agro = await self._directory.find_available_in_district(district) if district else None
        if agro is None:
            agro = await self._directory.find_any_available()
        if agro is None:
            raise OfficerUnavailableError(
                message="No agronomist is currently available to take this case.",
                details={"district": district},
            )
        return AssignedAgronomist(agro.id, agro.name, agro.kvk_center)
