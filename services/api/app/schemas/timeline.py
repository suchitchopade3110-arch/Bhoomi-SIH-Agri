"""Living farm case timeline and event history schemas."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class TimelineEventResponse(BaseModel):
    """Single event in a farm's continuous case timeline."""
    event_id: str = Field(..., description="UUID string of timeline event")
    farm_id: str = Field(...)
    event_type: str = Field(..., description="diagnosis, advisory, followup, health_update, land_verification, escalation")
    title: str = Field(...)
    description: str = Field(...)
    health_score_delta: float | None = Field(default=None, description="Score change (+ / -) resulting from this event")
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TimelineResponse(BaseModel):
    """Farm timeline feed."""
    farm_id: str = Field(...)
    events: list[TimelineEventResponse] = Field(default_factory=list)
