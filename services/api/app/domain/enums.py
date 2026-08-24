"""Domain enums — canonical public surface for the intelligence layer.

Re-exports every enum from ``app.core.enums`` at the spec-mandated path
(``app/domain/enums.py``) so routers, services, and external importers all
converge on one name.  The implementation continues to live in
``app.core.enums`` so existing callers are unbroken.

API Contract §2.2 spelling (exact):
    land_status        : pending_verification | under_review | verified | rejected
    health_band        : unrated | critical | poor | watch | good | excellent
    subindex_key       : active_problem_severity | environmental_risk |
                         monitoring_recency | treatment_response
    problem_severity   : early | moderate | severe
    problem_status     : open | resolved
    followup_response  : improved | no_change | got_worse
    case_status        : open | assigned | resolved
    scheme_status      : active | expiring | expired
    asset_kind         : image | audio
"""

from app.core.enums import (  # noqa: F401  (re-export)
    AssetKind,
    CaseStatus,
    FollowupResponse,
    GateOutcome,
    HealthBand,
    LandStatus,
    ProblemSeverity,
    ProblemStatus,
    SchemeStatus,
    SubIndexKey,
    UserRole,
)

__all__ = [
    "LandStatus",
    "HealthBand",
    "SubIndexKey",
    "ProblemSeverity",
    "ProblemStatus",
    "FollowupResponse",
    "CaseStatus",
    "SchemeStatus",
    "AssetKind",
    "GateOutcome",
    "UserRole",
]
