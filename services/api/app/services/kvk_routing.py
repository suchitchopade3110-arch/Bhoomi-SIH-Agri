"""Orchestrates next-available agronomist routing (PRD §5.11, Phase 2).

Replaces the ``DEFAULT_ASSIGNED_AGRONOMIST`` flat-constant stand-in
previously duplicated in ``escalation_service.py`` and
``diagnosis_service.py``. Reads the roster from ``AgronomistRosterPort``
and current open-case counts from ``CaseRepository.get_open_case_counts()``
(both typed, no SQL here), then hands them to the pure
``domain.routing.select_next_available_agronomist``.
"""

from app.domain.routing import select_next_available_agronomist
from app.ports.roster import AgronomistRosterPort
from app.repositories.interfaces import CaseRepository


async def route_to_next_available_agronomist(
    case_repo: CaseRepository,
    roster: AgronomistRosterPort,
    default_agronomist: str,
) -> str:
    """Returns the agronomist id a new case should route to.

    Falls back to ``default_agronomist`` only when the roster has no
    entries — i.e. no capacity data exists to route against — so nothing
    regresses if the roster adapter is ever empty.
    """
    agronomist_ids = await roster.list_agronomist_ids()
    if not agronomist_ids:
        return default_agronomist

    open_case_counts = await case_repo.get_open_case_counts()
    return select_next_available_agronomist(agronomist_ids, open_case_counts)
