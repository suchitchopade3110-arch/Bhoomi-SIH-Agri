"""Authentication service — register / login / current-user profile.

Simplification (flagged, PRD §3 vs. contract §2.3): the contract specifies
phone+OTP login for farmers and email+password for officers/agronomists.
Building real OTP delivery is out of scope for this phase, so every role
registers/logs in with phone_number (farmers) or email (officer/agronomist)
+ password through the same two endpoints — the JWT role claim (contract
§2.1) still gates every downstream route identically. See final report.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import Depends

from app.core.enums import UserRole
from app.core.errors import UnauthenticatedError, ValidationError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.dependencies import get_user_repository
from app.repositories.interfaces import UserRepository
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse

ACCESS_TOKEN_TTL_MINUTES = 60 * 24 * 7  # 7 days, matches contract §1.5's stateless-JWT posture


class AuthService:
    """Registers users and issues role-claim JWTs (contract §2.3)."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._users = user_repo

    async def register_user(self, request: UserRegisterRequest) -> UserResponse:
        existing = await self._users.get_by_phone(request.phone_number)
        if existing is not None:
            raise ValidationError(
                "A user with this phone number is already registered.",
                details={"phone_number": request.phone_number},
            )
        saved = await self._users.save(
            {
                "phone_number": request.phone_number,
                "full_name": request.full_name,
                "role": request.role.value,
                "preferred_language": request.preferred_language,
                "password_hash": get_password_hash(request.password),
            }
        )
        return _to_user_response(saved)

    async def login_user(self, request: UserLoginRequest) -> TokenResponse:
        user = await self._users.get_by_phone(request.phone_number)
        if user is None or not verify_password(request.password, user["password_hash"]):
            raise UnauthenticatedError("Invalid phone number or password.")
        token = create_access_token(
            subject=user["id"],
            role=UserRole(user["role"]),
            expires_delta=timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES),
        )
        return TokenResponse(
            access_token=token,
            expires_in=ACCESS_TOKEN_TTL_MINUTES * 60,
            user_id=user["id"],
            role=UserRole(user["role"]),
        )

    async def get_current_user(self, user_id: str) -> UserResponse:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise UnauthenticatedError("User no longer exists.")
        return _to_user_response(user)


def _to_user_response(row: dict) -> UserResponse:
    return UserResponse(
        id=row["id"],
        phone_number=row.get("phone_number") or "",
        full_name=row["full_name"],
        role=UserRole(row["role"]),
        preferred_language=row["preferred_language"],
        created_at=row["created_at"],
    )


def get_auth_service(user_repo: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(user_repo)
