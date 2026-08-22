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
from app.services.auth_service import AuthService, get_auth_service

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
