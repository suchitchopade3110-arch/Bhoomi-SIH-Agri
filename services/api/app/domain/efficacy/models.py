"""Value objects for Treatment Efficacy Tracking (SPEC-EFFICACY-001, Phase 4).

No I/O — plain dataclasses and a pure normalization helper. Mirrors
``app/domain/alerts/models.py``'s pattern: kept local to this package since
these are Phase-4-only concepts.
"""

import re
from dataclasses import dataclass
from datetime import date
from typing import Literal


def normalize_treatment_key(raw_name: str) -> str:
    """Canonical form for a treatment name (spec §3.1) — prevents free-text
    fragmentation (``"Copper Hydroxide 77% WP"`` vs ``"copper_hydroxide"``)
    from splitting sample size across two keys for the same treatment."""
    return re.sub(r"[^a-z0-9]+", "_", raw_name.strip().lower()).strip("_")


@dataclass(frozen=True)
class TreatmentApplicationSnapshot:
    """One recorded treatment application (spec §3.2's ``TreatmentApplication``
    row), decoupled from the ORM model — the same pattern
    ``RetrievedChunk``/``ClusterCase`` use so this domain function never
    needs a live DB connection to be tested."""

    id: str
    pathogen_type: str
    treatment_name: str
    crop: str
    district: str
    applied_on: date
    final_outcome: str | None  # "resolved" | "improved" | "failed" | "superseded" | None
    followups_to_resolution: int | None
    days_to_resolution: int | None
    failed_on_got_worse: bool
    escalated_for_expert: bool


@dataclass(frozen=True)
class EfficacyResult:
    treatment_id: str
    pathogen: str
    crop: str
    region: str
    status: Literal["insufficient_data", "statistically_significant"]
    sample_size: int
    min_sample_threshold: int
    efficacy_percentage: float | None
    avg_days_to_recovery: float | None
