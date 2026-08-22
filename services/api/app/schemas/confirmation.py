"""Schemas for voice read-back confirmation flow (PRD §5.1)."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class AwaitingConfirmation(BaseModel):
    """Represents a parsed field waiting for user voice/button confirmation."""
    field: str = Field(..., description="Field name being confirmed (e.g. 'land_area', 'crop')")
    value: Any = Field(..., description="Parsed value requiring confirmation")
    readback_text: str = Field(..., description="Tamil voice prompt read back to farmer")


class ConfirmFieldRequest(BaseModel):
    """Farmer's confirmation of a readback value."""
    field: str = Field(..., description="Field name confirmed")
    confirmed_value: Any = Field(..., description="The value confirmed or corrected")
    is_confirmed: bool = Field(..., description="True if confirmed, False if user rejected/corrected")
    correction_text: Optional[str] = Field(default=None, description="Corrected transcript if rejected")


class ConfirmFieldResponse(BaseModel):
    """Response confirming value was committed or needs re-entry."""
    status: str = Field(..., description="'committed' | 'retry_prompt'")
    field: str = Field(..., description="Field name")
    final_value: Optional[Any] = Field(default=None, description="Committed value if accepted")
    message: str = Field(..., description="Status feedback message (in Tamil)")
