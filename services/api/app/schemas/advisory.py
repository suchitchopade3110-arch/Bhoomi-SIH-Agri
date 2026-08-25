"""Grounded 5-point advisory schemas — mirror contract §2.10/§2.11 exactly."""

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import SpokenResponseMixin


class FivePointAdvisory(BaseModel):
    """The fixed 5-point structure (PRD §5.8), grounded strictly in cited sources."""

    possible_issue: str = Field(..., description="Point 1: what it likely is, with confidence")
    what_to_check: str = Field(..., description="Point 2: how to confirm")
    what_to_avoid: str = Field(..., description="Point 3: common harmful mistakes (promoted ahead of next actions)")
    what_to_do_next: str = Field(..., description="Point 4: concrete action")
    expert_triggers: str = Field(..., description="Point 5: conditions under which to stop and escalate")


class Citation(BaseModel):
    """One grounded source citation (contract §2.10/§2.11)."""

    doc_id: str
    title: str
    reviewed_on: date


class AdvisoryQueryRequest(BaseModel):
    """POST /advisory/query request (contract §2.11)."""

    farm_id: str = Field(..., description="UUID string of farm")
    query_text: str = Field(..., min_length=1, description="Spoken or typed farmer query")
    lang: str = Field(default="en-IN", description="BCP-47 language tag, e.g. ta-IN")


class AdvisoryQueryResponse(SpokenResponseMixin):
    """POST /advisory/query response — exactly one of the two contract shapes.

    ``retrieved=True``: ``advisory`` and ``citations`` are populated,
    ``reason``/``escalation_offered`` are ``None``.
    ``retrieved=False``: ``advisory``/``citations`` are empty, ``reason`` is
    the fixed literal ``"no_relevant_source"``, ``escalation_offered=True``.
    """

    retrieved: bool
    advisory: FivePointAdvisory | None = None
    citations: list[Citation] = Field(default_factory=list)
    reason: str | None = None
    escalation_offered: bool | None = None
    provider: str = Field(
        default="stub", description="LLM provider that served this response: 'groq' | 'stub'"
    )
    model: str = Field(default="stub", description="LLM model that served this response, or 'stub'")
