"""Error classes and FastAPI exception handlers implementing the Bhoomi Error Envelope."""

from typing import Any
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application error carrying code, message, and details for the error envelope."""

    def __init__(
        self,
        code: str = "INTERNAL_ERROR",
        message: str = "An unexpected error occurred.",
        details: dict[str, Any] | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code


class UnauthenticatedError(AppError):
    def __init__(self, message: str = "Authentication credentials were not provided or are invalid.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="UNAUTHENTICATED", message=message, details=details, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppError):
    def __init__(self, message: str = "You do not have permission to perform this action.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="FORBIDDEN", message=message, details=details, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundError(AppError):
    def __init__(self, message: str = "The requested resource was not found.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="NOT_FOUND", message=message, details=details, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(AppError):
    def __init__(self, message: str = "The input provided failed validation.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="VALIDATION_FAILED", message=message, details=details, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LandNotVerifiedError(AppError):
    def __init__(self, message: str = "Action requires a verified land parcel. Complete HITL verification first.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="LAND_NOT_VERIFIED", message=message, details=details, status_code=status.HTTP_409_CONFLICT)


class BelowConfidenceGateError(AppError):
    def __init__(self, message: str = "Model confidence score is below the operating threshold. Auto-escalating.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="BELOW_CONFIDENCE_GATE", message=message, details=details, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class NoRelevantSourceError(AppError):
    def __init__(self, message: str = "No grounded source found in knowledge corpus. Never fabricate advice.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="NO_RELEVANT_SOURCE", message=message, details=details, status_code=status.HTTP_404_NOT_FOUND)


class OfficerUnavailableError(AppError):
    def __init__(self, message: str = "No extension officer is currently available for this jurisdiction.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="OFFICER_UNAVAILABLE", message=message, details=details, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


class NotImplementedAPIError(AppError):
    def __init__(self, message: str = "This endpoint is scaffolded and will be implemented in subsequent phases.", details: dict[str, Any] | None = None) -> None:
        super().__init__(code="NOT_IMPLEMENTED", message=message, details=details, status_code=status.HTTP_501_NOT_IMPLEMENTED)


def build_error_response(code: str, message: str, details: dict[str, Any], status_code: int) -> JSONResponse:
    """Build standardized JSON error envelope."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details,
            }
        },
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle custom application errors."""
    return build_error_response(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        status_code=exc.status_code,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle standard FastAPI/Starlette HTTPExceptions with the error envelope."""
    code = "HTTP_ERROR"
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        code = "UNAUTHENTICATED"
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        code = "FORBIDDEN"
    elif exc.status_code == status.HTTP_404_NOT_FOUND:
        code = "NOT_FOUND"
    elif exc.status_code == status.HTTP_501_NOT_IMPLEMENTED:
        code = "NOT_IMPLEMENTED"

    details = exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}
    message = exc.detail if isinstance(exc.detail, str) else "An HTTP error occurred."
    return build_error_response(
        code=code,
        message=message,
        details=details,
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic request validation errors."""
    return build_error_response(
        code="VALIDATION_FAILED",
        message="Request validation failed.",
        details={"errors": exc.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler for unhandled internal exceptions."""
    return build_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An internal server error occurred.",
        details={"type": type(exc).__name__, "description": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register all standard error handlers to the FastAPI instance."""
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
