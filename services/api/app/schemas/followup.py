"""Closed-loop follow-up schemas — mirror contract §2.12 exactly."""

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import FollowupResponse, HealthBand


class FollowupRespondRequest(BaseModel):
    """``POST /followups/{id}/respond`` request (contract §2.12)."""

    response: FollowupResponse
    image_asset_id: str | None = None


class SeverityChange(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(alias="from")
    to: str


class FollowupHealthRef(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_: int | None = Field(default=None, alias="from")
    to: int | None = None
    band: HealthBand


class FollowupRespondResponse(BaseModel):
    """``POST /followups/{id}/respond`` response (contract §2.12):
    ``{ "problem_id": "p_7", "severity_change": {"from":"early","to":"moderate"}, "health": {"from":68,"to":59,"band":"poor"}, "escalated": true, "case_id": "c_5" }``.
    """

    problem_id: str
    severity_change: SeverityChange
    health: FollowupHealthRef
    escalated: bool
    case_id: str | None = None
