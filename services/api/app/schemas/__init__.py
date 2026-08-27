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
from app.schemas.gate import Decision, GateObject
from app.schemas.advisory import (
    AdvisoryQueryRequest,
    AdvisoryQueryResponse,
    Citation,
    FivePointAdvisory,
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
    FarmRiskTrendResponse,
    FarmSummaryResponse,
    FarmSummaryTrendResponse,
    FarmUpdateRequest,
)
from app.schemas.land import ThinLandVerification
from app.core.enums import ThinLandStatus
from app.schemas.resource_plan import (
    Fao56CalculateRequest,
    Fao56CalculateResponse,
    ResourcePlanResponse,
)
from app.schemas.diagnosis import (
    DiagnoseRequest,
    DiagnoseResponse,
    DiagnosisResult,
    EscalationRef,
    HealthDelta,
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
    "FivePointAdvisory",
    "AdvisoryQueryRequest",
    "AdvisoryQueryResponse",
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
    "Fao56CalculateRequest",
    "Fao56CalculateResponse",
    "ResourcePlanResponse",
    "DiagnoseRequest",
    "DiagnoseResponse",
    "DiagnosisResult",
    "HealthDelta",
    "EscalationRef",
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
    "GateObject",
    "FarmRiskTrendResponse",
    "FarmSummaryTrendResponse",
    "ThinLandVerification",
    "ThinLandStatus",
    "WeatherCurrentResponse",
    "WeatherForecastResponse",
    "WeatherEt0Response",
]
