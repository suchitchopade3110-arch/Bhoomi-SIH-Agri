"""Agronomist roster port — typed Protocol for "which agronomists exist to
route cases to" (PRD §5.11, Phase 2).

No officer-availability/capacity model exists in the schema yet (PRD §10
risk #10), so this is intentionally the thinnest possible port: just the
list of routable agronomist ids. Real capacity comes from
``CaseRepository.get_open_case_counts()`` (repository, not this port) —
this port only answers "who is on the roster at all."
"""

from typing import Protocol


class AgronomistRosterPort(Protocol):
    """Port for retrieving the set of agronomist ids eligible for routing."""

    async def list_agronomist_ids(self) -> list[str]:
        """Return every agronomist id new cases may be routed to."""
        ...


__all__ = ["AgronomistRosterPort"]
