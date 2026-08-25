"""Farmer phone-OTP login orchestration (PRD §2.3).

Additive, not a replacement: ``/auth/register`` + ``/auth/login`` (password)
keep working exactly as before for every role, per this project's own
"Zero Regression" principle (docs/specs/api_contract_sih26131_delta.md) —
this just adds the farmer-facing OTP path the PRD actually specifies,
alongside it.
"""

from datetime import datetime, timedelta
import secrets
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_otp_delivery_adapter
from app.core.config import Settings, get_settings
from app.core.enums import UserRole
from app.core.errors import RateLimitedError, UnauthenticatedError, ValidationError
from app.core.security import create_access_token, get_password_hash
from app.ports.otp_delivery import OtpDeliveryPort
from app.repositories.dependencies import get_user_repository
from app.repositories.interfaces import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.otp import OtpRequestResponse
from app.services.otp_store import OTP_LENGTH, OTP_TTL, OtpStore, get_otp_store

ACCESS_TOKEN_TTL_MINUTES = 60 * 24 * 7  # matches auth_service.py's password-login TTL


def _generate_otp() -> str:
    """Cryptographically random, not ``random`` — this is a credential."""
    return "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))


class OtpService:
    def __init__(
        self,
        user_repo: UserRepository,
        delivery: OtpDeliveryPort,
        store: OtpStore,
        settings: Settings,
    ) -> None:
        self._users = user_repo
        self._delivery = delivery
        self._store = store
        self._settings = settings

    async def request_otp(self, phone_number: str) -> OtpRequestResponse:
        now = datetime.utcnow()
        if not self._store.can_request(phone_number, now):
            raise RateLimitedError(
                "An OTP was already sent recently. Please wait before requesting another.",
                details={"phone_number": phone_number},
            )

        code = _generate_otp()
        self._store.issue(phone_number, code, now)
        await self._delivery.send_otp(phone_number, code)

        is_debug = self._settings.APP_ENV != "production"
        return OtpRequestResponse(
            expires_in=int(OTP_TTL.total_seconds()),
            debug_otp=code if is_debug else None,
        )

    async def verify_otp(
        self, phone_number: str, otp: str, full_name: str | None, preferred_language: str
    ) -> TokenResponse:
        now = datetime.utcnow()
        if not self._store.verify(phone_number, otp, now):
            raise UnauthenticatedError("Invalid or expired OTP.", details={"phone_number": phone_number})

        user = await self._users.get_by_phone(phone_number)
        if user is None:
            if not full_name:
                raise ValidationError(
                    "full_name is required to create an account on first verification.",
                    details={"phone_number": phone_number},
                )
            # OTP accounts have no farmer-known password — a random,
            # unusable bcrypt hash satisfies the NOT NULL column without
            # creating a guessable/default credential (see users.password_hash).
            unusable_password = secrets.token_urlsafe(32)
            user = await self._users.save(
                {
                    "phone_number": phone_number,
                    "full_name": full_name,
                    "role": UserRole.FARMER.value,
                    "preferred_language": preferred_language,
                    "password_hash": get_password_hash(unusable_password),
                }
            )

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


def get_otp_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> OtpService:
    return OtpService(user_repo, get_otp_delivery_adapter(), get_otp_store(), settings)
