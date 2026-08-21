"""Agronomist portal schemas — mirror contract §2.13 exactly."""

from pydantic import BaseModel, Field

from app.core.enums import HealthBand
from app.schemas.case import CaseQueueItem
from app.schemas.common import PaginatedResponse


class CaseQueueResponse(PaginatedResponse[CaseQueueItem]):
    """``GET /agronomist/case-queue``: assigned cases, newest first."""


class ResolveCaseRequest(BaseModel):
    """``POST /cases/{id}/resolve`` request (contract §2.13)."""

    diagnosis: str = Field(..., min_length=1)
    treatment: str = Field(..., min_length=1)
    notes: str | None = None


class ResolveCaseHealthRef(BaseModel):
    from_: int | None = Field(default=None, alias="from")
    to: int | None = None
    band: HealthBand

    model_config = {"populate_by_name": True}


class ResolveCaseResponse(BaseModel):
    """``POST /cases/{id}/resolve`` response (contract §2.13):
    ``{ "case_id": "c_5", "status": "resolved", "problem_status": "resolved", "health": { "from": 59, "to": 86, "band": "good" } }``.
    """

    case_id: str
    status: str
    problem_status: str | None = None
    health: ResolveCaseHealthRef
