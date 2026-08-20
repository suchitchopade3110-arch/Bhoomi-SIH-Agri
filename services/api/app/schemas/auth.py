"""Authentication and user schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import UserRole


class UserRegisterRequest(BaseModel):
    """User registration payload."""
    phone_number: str = Field(..., description="10-digit mobile number")
    full_name: str = Field(..., description="Full name of user")
    role: UserRole = Field(default=UserRole.FARMER, description="Role claim")
    preferred_language: str = Field(default="ta", description="ISO 639-1 language code (e.g., 'ta' for Tamil)")
    password: str = Field(..., min_length=6, description="Account password")


class UserLoginRequest(BaseModel):
    """User login payload."""
    phone_number: str = Field(..., description="Mobile number")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """JWT Token response."""
    access_token: str = Field(..., description="Signed JWT Bearer token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    user_id: str = Field(..., description="UUID string of authenticated user")
    role: UserRole = Field(..., description="User role claim")


class UserResponse(BaseModel):
    """Public user profile response."""
    id: str = Field(..., description="UUID string of user")
    phone_number: str = Field(..., description="Phone number")
    full_name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="Role claim")
    preferred_language: str = Field(..., description="Language preference")
    created_at: datetime = Field(default_factory=datetime.utcnow)
