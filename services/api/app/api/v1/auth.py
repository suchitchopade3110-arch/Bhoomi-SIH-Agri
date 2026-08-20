"""Authentication API router."""

from fastapi import APIRouter, status
from app.core.errors import NotImplementedAPIError
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new farmer or officer user",
)
async def register(request: UserRegisterRequest) -> UserResponse:
    raise NotImplementedAPIError("Endpoint POST /auth/register will be implemented in subsequent phases.")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and issue JWT token",
)
async def login(request: UserLoginRequest) -> TokenResponse:
    raise NotImplementedAPIError("Endpoint POST /auth/login will be implemented in subsequent phases.")


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh JWT access token",
)
async def refresh_token() -> TokenResponse:
    raise NotImplementedAPIError("Endpoint POST /auth/refresh will be implemented in subsequent phases.")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user profile",
)
async def get_me() -> UserResponse:
    raise NotImplementedAPIError("Endpoint GET /auth/me will be implemented in subsequent phases.")
