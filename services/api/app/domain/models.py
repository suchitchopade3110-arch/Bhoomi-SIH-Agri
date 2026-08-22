"""Domain models — Pydantic v2 value objects for the intelligence layer.

These are the shared API-level data contracts (API Contract §2.9–§2.13).
They are intentionally separate from:
  - The internal dataclasses (HealthScoreResult, SubIndexBreakdown, GateDecision)
    used inside domain logic — those are in ``app.domain.health.*`` and
    ``app.domain.gate.*`` and carry no Pydantic overhead.
  - The SQLAlchemy ORM rows (``db/models.py``) that persist these values.

Routers and services use these Pydantic models for serialisation / validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from app.domain.enums import CaseStatus, FollowupResponse, HealthBand, ProblemSeverity, SubIndexKey


# ---------------------------------------------------------------------------
# Health score models (API Contract §2.9)
# ---------------------------------------------------------------------------


class SubIndex(BaseModel):
    """One row of the transparent health-score breakdown (contract §2.9)."""

    key: SubIndexKey
    value: int = Field(ge=0, le=100)
    weight: float = Field(gt=0.0, le=1.0)
    contribution: float

    model_config = {"frozen": True}


class TriggeringInputModel(BaseModel):
    """Describes the event that caused a health recompute (contract §2.9)."""

    type: str
    details: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class HealthSnapshot(BaseModel):
    """Full health score result with inspectable sub-index breakdown (contract §2.9).

    ``score=None`` and ``band='unrated'`` when required inputs are missing —
    Day 0 is Unrated, not 0 (PRD §7.1).
    """

    score: int | None = Field(default=None, ge=0, le=100)
    band: HealthBand
    computed_at: datetime
    weights_version: str = "v1"
    subindices: list[SubIndex] = Field(default_factory=list)
    triggering_input: TriggeringInputModel | None = None
    missing_fields: list[str] = Field(default_factory=list)
    spoken_summary: str | None = None

    model_config = {"frozen": True}


# ---------------------------------------------------------------------------
# Advisory models (API Contract §2.10/§2.11)
# ---------------------------------------------------------------------------


class Citation(BaseModel):
    """Source citation attached to every advisory (contract §2.10/§2.11)."""

    doc_id: str
    title: str
    reviewed_on: str  # ISO date string, e.g. "2025-11-02"

    model_config = {"frozen": True}


class Advisory(BaseModel):
    """Fixed 5-point advisory structure (PRD §5.8, contract §2.10).

    Every field must be populated — a partial advisory is never returned.
    ``citations`` must be non-empty; an uncited response is rejected.
    """

    possible_issue: str
    what_to_check: str
    what_to_do_next: str
    what_to_avoid: str
    expert_triggers: str
    citations: list[Citation] = Field(min_length=1)

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def citations_not_empty(self) -> Advisory:
        if not self.citations:
            raise ValueError("Advisory must carry at least one citation (PRD §5.7).")
        return self


# ---------------------------------------------------------------------------
# Decision models (API Contract §2.10)
# ---------------------------------------------------------------------------


class EscalationBranch(BaseModel):
    """The escalation branch of a gate decision (contract §2.10 below-gate shape)."""

    case_id: str
    assigned_to: str
    spoken_summary: str
    reason: str
    error_code: str

    model_config = {"frozen": True}


class AdvisoryBranch(BaseModel):
    """The compose branch of a gate decision (contract §2.10 above-gate shape)."""

    advisory: Advisory
    health_delta: dict[str, Any] | None = None
    spoken_summary: str | None = None

    model_config = {"frozen": True}


class Decision(BaseModel):
    """Discriminated union: the gate routes to exactly one branch (contract §2.10).

    ``above_gate=True``  → ``advisory`` is set,   ``escalation`` is None.
    ``above_gate=False`` → ``escalation`` is set,  ``advisory``  is None.
    Never both, never neither — enforced by the validator.
    """

    above_gate: bool
    advisory: AdvisoryBranch | None = None
    escalation: EscalationBranch | None = None

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def exactly_one_branch(self) -> Decision:
        if self.above_gate:
            if self.advisory is None:
                raise ValueError("above_gate=True requires advisory branch.")
            if self.escalation is not None:
                raise ValueError("above_gate=True must not carry escalation branch.")
        else:
            if self.escalation is None:
                raise ValueError("above_gate=False requires escalation branch.")
            if self.advisory is not None:
                raise ValueError("above_gate=False must not carry advisory branch.")
        return self


# ---------------------------------------------------------------------------
# Case summary model (API Contract §2.13)
# ---------------------------------------------------------------------------


class CaseSummary(BaseModel):
    """Pre-analyzed bundle compiled for expert escalation (PRD §5.11, contract §2.13).

    Every field must be populated — ``build_case_summary`` never returns a
    partial summary. The agronomist opens this and has everything they need
    without asking follow-up questions.
    """

    case_id: str
    farm: dict[str, Any]        # farm id, crop, area, soil_type
    problem: dict[str, Any]     # problem id, label, severity
    timeline: list[dict[str, Any]]
    images: list[dict[str, Any]]  # [{"asset_id": ..., "url": ...}]
    treatments_tried: list[str]
    followup_trend: FollowupResponse | None
    current_health: HealthSnapshot
    status: CaseStatus
    assigned_to: str | None = None

    model_config = {"frozen": True}
