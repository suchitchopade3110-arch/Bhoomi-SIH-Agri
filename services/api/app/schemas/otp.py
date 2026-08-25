"""Farmer phone-OTP login schemas (PRD §2.3)."""

from pydantic import BaseModel, Field


class OtpRequestRequest(BaseModel):
    """POST /auth/otp/request request."""

    phone_number: str = Field(..., description="Farmer's mobile number")


class OtpRequestResponse(BaseModel):
    """POST /auth/otp/request response."""

    message: str = Field(default="OTP sent.")
    expires_in: int = Field(..., description="Seconds until the code expires")
    debug_otp: str | None = Field(
        default=None,
        description=(
            "The OTP itself — present only when APP_ENV is not 'production' "
            "(no real SMS gateway is configured anywhere in this project, "
            "so this is how the flow is actually usable/testable today)."
        ),
    )


class OtpVerifyRequest(BaseModel):
    """POST /auth/otp/verify request."""

    phone_number: str = Field(..., description="Farmer's mobile number")
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit code")
    full_name: str | None = Field(
        default=None,
        description="Required only the first time this phone number verifies (creates the account)",
    )
    preferred_language: str = Field(default="ta", description="ISO 639-1 language code")
