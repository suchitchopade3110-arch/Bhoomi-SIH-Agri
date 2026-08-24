"""Orchestrates next-available KVK routing (PRD §5.11, Phase 2).

Replaces the ``DEFAULT_ASSIGNED_AGRONOMIST`` single-center stand-in
previously duplicated in ``escalation_service.py`` and
``diagnosis_service.py``. Fetches current per-center caseload from
``CaseRepository`` (already available on every ``get_agronomist_queue()``
row — no repository interface change needed) and hands it to the pure
``domain.routing.select_next_available_kvk``.
"""

from app.core.enums import CaseStatus
from app.domain.kvk_directory import KVK_CENTERS
from app.domain.routing import select_next_available_kvk
from app.repositories.interfaces import CaseRepository

# A case still counts against a center's capacity until it's resolved or
# closed — everything else ("open", "assigned", "escalated", "investigating")
# is active work.
_INACTIVE_STATUSES = {CaseStatus.RESOLVED.value, CaseStatus.CLOSED.value}


async def route_to_next_available_kvk(case_repo: CaseRepository, farm_lat: float, farm_lon: float) -> str:
    """Returns the ``center_id`` a new case for this farm should route to."""
    queue = await case_repo.get_agronomist_queue()
    caseload: dict[str, int] = {}
    for case in queue:
        if case.get("status") in _INACTIVE_STATUSES:
            continue
        center_id = case.get("assigned_to")
        if center_id:
            caseload[center_id] = caseload.get(center_id, 0) + 1

    center = select_next_available_kvk(farm_lat, farm_lon, centers=KVK_CENTERS, current_caseload=caseload)
    return center.center_id
