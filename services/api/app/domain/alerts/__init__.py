"""Early-Warning Alert System domain package (SPEC-ALERT-001, Phase 3)."""

from app.domain.alerts.evaluate import evaluate_alert
from app.domain.alerts.models import (
    AlertDraft,
    AlertSeverity,
    AlertTarget,
    ClusterCase,
    DeliveryChannel,
    PathogenRiskThreshold,
    WeatherMetrics,
)
from app.domain.alerts.thresholds import PATHOGEN_RISK_THRESHOLDS, get_threshold

__all__ = [
    "evaluate_alert",
    "AlertDraft",
    "AlertSeverity",
    "AlertTarget",
    "ClusterCase",
    "DeliveryChannel",
    "PathogenRiskThreshold",
    "WeatherMetrics",
    "PATHOGEN_RISK_THRESHOLDS",
    "get_threshold",
]
