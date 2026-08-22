"""Domain errors — canonical public surface for the intelligence layer.

Re-exports the stable error codes and exception hierarchy from
``app.core.errors`` at the spec-mandated path ``app/domain/errors.py``.

Stable machine codes (API Contract §2.1):
    UNAUTHENTICATED · FORBIDDEN · NOT_FOUND · VALIDATION_FAILED
    LAND_NOT_VERIFIED · BELOW_CONFIDENCE_GATE · NO_RELEVANT_SOURCE
    OFFICER_UNAVAILABLE
"""

from app.core.errors import (  # noqa: F401  (re-export)
    AppError,
    BelowConfidenceGateError,
    ForbiddenError,
    LandNotVerifiedError,
    NoRelevantSourceError,
    NotFoundError,
    NotImplementedAPIError,
    OfficerUnavailableError,
    UnauthenticatedError,
    ValidationError,
    build_error_response,
    register_error_handlers,
)

__all__ = [
    "AppError",
    "UnauthenticatedError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "LandNotVerifiedError",
    "BelowConfidenceGateError",
    "NoRelevantSourceError",
    "OfficerUnavailableError",
    "NotImplementedAPIError",
    "build_error_response",
    "register_error_handlers",
]
