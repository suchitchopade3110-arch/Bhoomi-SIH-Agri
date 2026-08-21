"""Common schemas for pagination, errors, and standard wrappers."""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import HealthBand

T = TypeVar("T")


class HealthMovement(BaseModel):
    """Before/after health-score movement plus the new band — the
    ``{"from": ..., "to": ..., "band": ...}`` shape used by both contract
    §2.12 (follow-up respond) and §2.13 (case resolve)."""

    model_config = ConfigDict(populate_by_name=True)

    from_: int | None = Field(default=None, alias="from")
    to: int | None = None
    band: HealthBand


class ErrorDetail(BaseModel):
    """Error object contained inside the error envelope."""
    code: str = Field(..., description="Stable error code string")
    message: str = Field(..., description="Human-readable error description")
    details: dict[str, Any] = Field(default_factory=dict, description="Additional contextual metadata or field validation errors")


class ErrorEnvelope(BaseModel):
    """Standardized error envelope for all non-2xx responses."""
    error: ErrorDetail


class CursorPaginationParams(BaseModel):
    """Query parameters for cursor-based pagination."""
    limit: int = Field(default=20, ge=1, le=100, description="Number of items to return")
    cursor: str | None = Field(default=None, description="Cursor pointer for next page of items")


class PaginatedResponse(BaseModel, Generic[T]):
    """Cursor-paginated list wrapper."""
    items: list[T] = Field(..., description="List of items for current page")
    next_cursor: str | None = Field(default=None, description="Cursor for the subsequent page; null if no more items")
    total_count: int | None = Field(default=None, description="Optional total count if known")


class SpokenResponseMixin(BaseModel):
    """Mixin providing spoken_summary for voice-first client TTS."""
    spoken_summary: str | None = Field(
        default=None,
        description="Concise localized summary text optimized for voice readback",
    )
