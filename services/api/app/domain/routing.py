"""Pure domain logic for next-available agronomist routing (PRD §5.11, Phase 2).

No I/O: the caller (a service) fetches the agronomist roster and each
agronomist's current open-case count and hands them in here. Same inputs,
same output, always — deterministic tie-breaking (lexicographic by id), no
random choice among equally loaded agronomists.
"""


def select_next_available_agronomist(
    agronomist_ids: list[str],
    open_case_counts: dict[str, int],
) -> str:
    """Pick the agronomist a new case should route to: fewest open cases,
    ties broken lexicographically by ``agronomist_id`` for a reproducible
    result on identical inputs.

    Raises:
        ValueError: if ``agronomist_ids`` is empty — there is nothing to
            route to (the caller should fall back to a default assignment).
    """
    if not agronomist_ids:
        raise ValueError("No agronomists available to route to.")

    return min(agronomist_ids, key=lambda aid: (open_case_counts.get(aid, 0), aid))
