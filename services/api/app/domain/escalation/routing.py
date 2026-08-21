"""Pure agronomist-selection rule (PRD §5.11, execution plan item 3). No I/O.

"Nearest available agronomist; if none [in that jurisdiction], the next
available; if none at all, ``OFFICER_UNAVAILABLE``" — the actual DB lookup
and jurisdiction/capacity data live in
``repositories/agronomist_repository.py``; this module only decides, given
a candidate list, who gets the case.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AgronomistCandidate:
    identifier: str
    jurisdiction: str
    is_available: bool
    active_case_count: int


def select_agronomist(
    candidates: list[AgronomistCandidate],
    jurisdiction: str | None = None,
) -> AgronomistCandidate | None:
    """Pick the best available agronomist, or ``None`` if none are.

    Prefers an available agronomist in the requested ``jurisdiction``,
    breaking ties by lowest current case load. Falls back to any available
    agronomist (again by lowest load) if no local match exists. Returns
    ``None`` only when the entire candidate pool has nobody available — the
    caller is responsible for raising ``OFFICER_UNAVAILABLE`` in that case.
    """
    available = [c for c in candidates if c.is_available]
    if not available:
        return None

    if jurisdiction:
        local = [c for c in available if c.jurisdiction == jurisdiction]
        if local:
            return min(local, key=lambda c: c.active_case_count)

    return min(available, key=lambda c: c.active_case_count)
