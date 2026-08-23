"""Security, JWT token utilities, and Role-Based Access Control dependencies."""

from datetime import datetime, timedelta
from typing import Annotated, Any
from fastapi import Depends, Header
from jose import JWTError, jwt
import bcrypt
from app.core.config import get_settings
from app.core.enums import UserRole
from app.core.errors import ForbiddenError, UnauthenticatedError

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify raw password against bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8")[:72], hashed_password.encode("utf-8"))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for password."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def create_access_token(
    subject: str,
    role: UserRole,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create signed JWT access token with user_id and role claims."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": subject,
        "role": role.value if isinstance(role, UserRole) else role,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    if extra_claims:
        to_encode.update(extra_claims)

    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT access token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as exc:
        raise UnauthenticatedError(
            message="Invalid or expired authentication token.",
            details={"error": str(exc)},
        ) from exc


async def get_current_token_payload(
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, Any]:
    """Extract and validate bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthenticatedError("Missing or invalid Authorization header.")

    token = authorization.split(" ")[1]
    return decode_access_token(token)


def require_roles(allowed_roles: list[UserRole]):
    """FastAPI dependency factory enforcing role-based route access."""

    async def role_checker(
        payload: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    ) -> dict[str, Any]:
        user_role = payload.get("role")
        allowed_str_roles = [r.value for r in allowed_roles]
        if user_role not in allowed_str_roles:
            raise ForbiddenError(
                message=f"Access requires one of roles: {allowed_str_roles}. User has role: '{user_role}'.",
                details={"required_roles": allowed_str_roles, "user_role": user_role},
            )
        return payload

    return role_checker
