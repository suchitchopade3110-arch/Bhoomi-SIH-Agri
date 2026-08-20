"""Contract §2.2 Enums for Bhoomi Backend API."""

from enum import Enum


class LandStatus(str, Enum):
    """Cadastral land verification status."""
    UNVERIFIED = "unverified"
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    REJECTED = "rejected"


class HealthBand(str, Enum):
    """Farm health score categorical band."""
    OPTIMAL = "optimal"       # 80 - 100
    GOOD = "good"             # 65 - 79
    MODERATE = "moderate"     # 50 - 64
    AT_RISK = "at_risk"       # 35 - 49
    CRITICAL = "critical"     # 0 - 34


class SubIndexKey(str, Enum):
    """Keys for the six weighted sub-indices of the farm health score."""
    SOIL_WATER = "soil_water"
    CROP_VIGOR = "crop_vigor"
    WEATHER_RISK = "weather_risk"
    PEST_DISEASE = "pest_disease"
    NUTRIENT_BALANCE = "nutrient_balance"
    INTERVENTION_HISTORY = "intervention_history"


class ProblemSeverity(str, Enum):
    """Severity level of identified crop problem."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProblemStatus(str, Enum):
    """Lifecycle status of a crop problem."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class FollowupResponse(str, Enum):
    """Farmer follow-up response."""
    IMPROVED = "improved"
    NO_CHANGE = "no_change"
    GOT_WORSE = "got_worse"


class CaseStatus(str, Enum):
    """Lifecycle status of an escalated case."""
    OPEN = "open"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SchemeStatus(str, Enum):
    """Government scheme match status."""
    ACTIVE = "active"
    UPCOMING = "upcoming"
    EXPIRED = "expired"
    APPLIED = "applied"
    APPROVED = "approved"
    REJECTED = "rejected"


class AssetKind(str, Enum):
    """Asset blob types."""
    AUDIO_QUERY = "audio_query"
    AUDIO_RESPONSE = "audio_response"
    DISEASE_PHOTO = "disease_photo"
    CADASTRAL_MAP = "cadastral_map"
    FIELD_PHOTO = "field_photo"
    REPORT_PDF = "report_pdf"


class UserRole(str, Enum):
    """JWT Role Claims."""
    FARMER = "farmer"
    OFFICER = "officer"
    AGRONOMIST = "agronomist"


class GateOutcome(str, Enum):
    """Confidence gate decision outcome."""
    ANSWER = "answer"
    ESCALATE = "escalate"
