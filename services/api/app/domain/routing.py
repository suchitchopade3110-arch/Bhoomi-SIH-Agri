"""Pure domain logic for next-available KVK routing (PRD §5.11, Phase 2).

No I/O: the caller (a service) fetches the farm's coordinates and each
center's current open-case count and hands them in here. Same inputs, same
output, always — deterministic tie-breaking, no random choice among equally
good centers.
"""

from app.domain.geo import haversine_distance_km
from app.domain.kvk_directory import KvkCenter


def select_next_available_kvk(
    farm_lat: float,
    farm_lon: float,
    centers: list[KvkCenter],
    current_caseload: dict[str, int],
) -> KvkCenter:
    """Pick the KVK center a new case should route to.

    Preference order:
    1. Among centers with open caseload strictly below their ``capacity``
       ("available"), pick the nearest to the farm by great-circle distance.
    2. If every center is at or over capacity, fall back to the
       least-loaded center overall (so cases still get assigned rather than
       piling onto one center) — ties broken by nearest distance.

    Both tiers break remaining ties by ``center_id`` so the result is
    reproducible for identical inputs.

    Raises:
        ValueError: if ``centers`` is empty — there is nothing to route to.
    """
    if not centers:
        raise ValueError("No KVK centers available to route to.")

    def distance_km(center: KvkCenter) -> float:
        return haversine_distance_km(farm_lat, farm_lon, center.latitude, center.longitude)

    available = [c for c in centers if current_caseload.get(c.center_id, 0) < c.capacity]
    if available:
        return min(available, key=lambda c: (distance_km(c), c.center_id))

    return min(
        centers,
        key=lambda c: (current_caseload.get(c.center_id, 0), distance_km(c), c.center_id),
    )
