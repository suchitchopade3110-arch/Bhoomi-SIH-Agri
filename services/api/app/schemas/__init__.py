"""Pydantic schemas for Bhoomi API."""

from app.schemas.common import (
    CursorPaginationParams,
    ErrorDetail,
    ErrorEnvelope,
    PaginatedResponse,
    SpokenResponseMixin,
)
from app.schemas.health import (
    HealthHistoryResponse,
    HealthSnapshot,
    SubIndexBreakdown,
)
from app.schemas.gate import Decision
from app.schemas.advisory import (
    Advisory,
    AdvisoryGenerateRequest,
    Citation,
)
from app.schemas.case import CaseSummary
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.schemas.assets import (
    AssetResponse,
    PresignedUploadRequest,
    PresignedUploadResponse,
)
from app.schemas.voice import (
    VoiceQueryRequest,
    VoiceQueryResponse,
    VoiceSynthesizeRequest,
    VoiceSynthesizeResponse,
    VoiceTranscribeRequest,
    VoiceTranscribeResponse,
)
from app.schemas.farm import (
    FarmCreateRequest,
    FarmResponse,
    FarmSummaryResponse,
    FarmUpdateRequest,
)
from app.schemas.land import (
    CadastralLookupRequest,
    CadastralLookupResponse,
    LandVerifyRequest,
    LandVerifyResponse,
)
from app.schemas.officer import (
    OfficerActionRequest,
    OfficerActionResponse,
    OfficerQueueItem,
    OfficerReviewDetail,
)
from app.schemas.resource_plan import (
    Fao56CalculateRequest,
    Fao56CalculateResponse,
    ResourcePlanResponse,
)
from app.schemas.diagnosis import (
    CropDiagnosisRequest,
    CropDiagnosisResponse,
)
from app.schemas.timeline import (
    TimelineEventResponse,
    TimelineResponse,
)
from app.schemas.followup import (
    FollowupCheckinRequest,
    FollowupCheckinResponse,
)
from app.schemas.escalation import (
    EscalationCreateRequest,
    EscalationResponse,
)
from app.schemas.agronomist import (
    AgronomistQueueItem,
    ResolveCaseRequest,
    ResolveCaseResponse,
)
from app.schemas.schemes import (
    SchemeListResponse,
    SchemeMatchRequest,
    SchemeResponse,
)
from app.schemas.weather import (
    WeatherCurrentResponse,
    WeatherEt0Response,
    WeatherForecastResponse,
)

__all__ = [
    "CursorPaginationParams",
    "ErrorDetail",
    "ErrorEnvelope",
    "PaginatedResponse",
    "SpokenResponseMixin",
    "HealthSnapshot",
    "SubIndexBreakdown",
    "HealthHistoryResponse",
    "Decision",
    "Citation",
    "Advisory",
    "AdvisoryGenerateRequest",
    "CaseSummary",
    "UserRegisterRequest",
    "UserLoginRequest",
    "TokenResponse",
    "UserResponse",
    "PresignedUploadRequest",
    "PresignedUploadResponse",
    "AssetResponse",
    "VoiceTranscribeRequest",
    "VoiceTranscribeResponse",
    "VoiceSynthesizeRequest",
    "VoiceSynthesizeResponse",
    "VoiceQueryRequest",
    "VoiceQueryResponse",
    "FarmCreateRequest",
    "FarmUpdateRequest",
    "FarmResponse",
    "FarmSummaryResponse",
    "CadastralLookupRequest",
    "CadastralLookupResponse",
    "LandVerifyRequest",
    "LandVerifyResponse",
    "OfficerQueueItem",
    "OfficerReviewDetail",
    "OfficerActionRequest",
    "OfficerActionResponse",
    "Fao56CalculateRequest",
    "Fao56CalculateResponse",
    "ResourcePlanResponse",
    "CropDiagnosisRequest",
    "CropDiagnosisResponse",
    "TimelineEventResponse",
    "TimelineResponse",
    "FollowupCheckinRequest",
    "FollowupCheckinResponse",
    "EscalationCreateRequest",
    "EscalationResponse",
    "AgronomistQueueItem",
    "ResolveCaseRequest",
    "ResolveCaseResponse",
    "SchemeResponse",
    "SchemeMatchRequest",
    "SchemeListResponse",
    "WeatherCurrentResponse",
    "WeatherForecastResponse",
    "WeatherEt0Response",
]
