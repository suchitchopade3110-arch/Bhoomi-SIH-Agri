"""Closed-loop follow-up schemas — mirror contract §2.12
``POST /followups/{id}/respond`` exactly."""

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import FollowupResponse, ProblemSeverity
from app.schemas.common import HealthMovement


class FollowupRespondRequest(BaseModel):
    """POST /followups/{problem_id}/respond request body (contract §2.12).

    ``{problem_id}`` in the path identifies which open problem this
    follow-up is about — the body carries only the farmer's response.
    """
    response: FollowupResponse = Field(..., description="'improved', 'no_change', or 'got_worse'")
    image_asset_id: str | None = Field(default=None, description="Optional updated crop photo")


class SeverityChange(BaseModel):
    """Contract §2.12 ``severity_change`` — present only when 'got_worse'
    promoted the problem a tier; ``null`` otherwise."""
    from_: ProblemSeverity = Field(..., alias="from")
    to: ProblemSeverity

    model_config = ConfigDict(populate_by_name=True)


class FollowupRespondResponse(BaseModel):
    """POST /followups/{problem_id}/respond response (contract §2.12)."""
    problem_id: str
    severity_change: SeverityChange | None = Field(
        default=None, description="Present only when 'got_worse' promoted the problem a severity tier"
    )
    health: HealthMovement
    escalated: bool = Field(..., description="Whether 'got_worse' past the threshold auto-escalated")
    case_id: str | None = Field(default=None, description="The new case's id, if auto-escalated")
    spoken_summary: str | None = Field(
        default=None, description="Concise localized summary text optimized for voice readback"
    )
