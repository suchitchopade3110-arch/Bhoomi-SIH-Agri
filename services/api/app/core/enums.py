"""Contract §2.2 Enums for Bhoomi Backend API."""

from enum import Enum


class ThinLandStatus(str, Enum):
    """Thin land status enum (strictly 3 states: pending_verification | verified | rejected)."""
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    REJECTED = "rejected"


class LandStatus(str, Enum):
    """Land verification status (thin enum: pending_verification | verified | rejected)."""
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    REJECTED = "rejected"
    # Legacy cadastral values from Phase-0 scaffold
    UNVERIFIED = "unverified"
    PENDING_REVIEW = "pending_review"


class HealthBand(str, Enum):
    """Farm health score categorical band (PRD §7.5, contract §2.2).

    `UNRATED` is a distinct state, not a numeric score of zero — PRD §7.1:
    "Day 0 with no inputs is Unrated (null). A *low* number means *bad
    health*, never *no data*."
    """
    UNRATED = "unrated"
    CRITICAL = "critical"     # 0 - 39
    POOR = "poor"             # 40 - 59
    WATCH = "watch"           # 60 - 74
    GOOD = "good"             # 75 - 89
    EXCELLENT = "excellent"   # 90 - 100


class SubIndexKey(str, Enum):
    """Keys for the six weighted sub-indices of the farm health score (PRD §7.2, contract §2.2)."""
    ENVIRONMENTAL_SUITABILITY = "environmental_suitability"
    RESOURCE_ADEQUACY = "resource_adequacy"
    CROP_STAGE_PROGRESSION = "crop_stage_progression"
    ACTIVE_PROBLEM_LOAD = "active_problem_load"
    MONITORING_RECENCY = "monitoring_recency"
    TREATMENT_RESPONSE = "treatment_response"


class ProblemSeverity(str, Enum):
    """Severity level of an identified crop problem (PRD §7.3, contract §2.2)."""
    EARLY = "early"
    MODERATE = "moderate"
    SEVERE = "severe"


class ProblemStatus(str, Enum):
    """Lifecycle status of a crop problem (contract §2.2)."""
    OPEN = "open"
    RESOLVED = "resolved"


class FollowupResponse(str, Enum):
    """Farmer follow-up response."""
    IMPROVED = "improved"
    NO_CHANGE = "no_change"
    GOT_WORSE = "got_worse"


class CaseStatus(str, Enum):
    """Lifecycle status of an escalated case (contract §2.13: open | assigned | resolved,
    plus a couple of internal-only states this codebase also tracks)."""
    OPEN = "open"
    ASSIGNED = "assigned"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SchemeStatus(str, Enum):
    """Government scheme match status (contract §2.2: active | expiring | expired)."""
    ACTIVE = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    UPCOMING = "upcoming"
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
    """Confidence gate decision outcome (PRD §5.6, §5.7).

    Exactly one of these two — never both, never neither (domain/gate/decide.py).
    """
    COMPOSE = "compose"
    ESCALATE = "escalate"
