"""Authentication API router (contract §2.3)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_token_payload
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.schemas.otp import OtpRequestRequest, OtpRequestResponse, OtpVerifyRequest
from app.services.auth_service import AuthService, get_auth_service
from app.services.otp_service import OtpService, get_otp_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new farmer, officer, or agronomist user",
)
async def register(
    request: UserRegisterRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    return await service.register_user(request)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and issue role-claim JWT",
)
async def login(
    request: UserLoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    return await service.login_user(request)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user profile",
)
async def get_me(
    service: Annotated[AuthService, Depends(get_auth_service)],
    payload: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> UserResponse:
    return await service.get_current_user(payload["sub"])


@router.post(
    "/otp/request",
    response_model=OtpRequestResponse,
    summary="Request a farmer login OTP (PRD §2.3) — additive alongside /login, never replaces it",
)
async def request_otp(
    request: OtpRequestRequest,
    service: Annotated[OtpService, Depends(get_otp_service)],
) -> OtpRequestResponse:
    return await service.request_otp(request.phone_number)


@router.post(
    "/otp/verify",
    response_model=TokenResponse,
    summary="Verify a farmer login OTP and issue a role-claim JWT (creates the account on first verification)",
)
async def verify_otp(
    request: OtpVerifyRequest,
    service: Annotated[OtpService, Depends(get_otp_service)],
) -> TokenResponse:
    return await service.verify_otp(
        request.phone_number, request.otp, request.full_name, request.preferred_language
    )
