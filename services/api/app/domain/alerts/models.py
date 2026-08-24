"""Value objects for the Early-Warning Alert System (SPEC-ALERT-001, Phase 3).

No I/O — plain enums and immutable dataclasses. Kept local to this package
rather than added to ``app.core.enums`` since these are brand-new,
Phase-3-only concepts nothing else in the codebase references yet.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AlertSeverity(str, Enum):
    INFO = "info"
    ADVISORY = "advisory"
    WARNING = "warning"
    EMERGENCY = "emergency"


class AlertTarget(str, Enum):
    PER_FARM = "per_farm"
    REGIONAL_BROADCAST = "regional_broadcast"


class DeliveryChannel(str, Enum):
    PUSH_NOTIFICATION = "push"
    HOME_BANNER = "home_banner"
    VOICE_BRIEFING = "voice_briefing"


@dataclass(frozen=True)
class WeatherMetrics:
    """48-hour rolling weather signal (spec §3.2) — assembled by the caller
    from ``WeatherPort``, never fetched here."""

    avg_temp_c: float
    avg_humidity_pct: float
    sustained_hours: int


@dataclass(frozen=True)
class ClusterCase:
    """One (label, severity) group of confirmed diagnoses within the
    repository's bounding-box + radius + time-window pre-filter (spec §3.3
    / Phase 1's haversine decision) — already scoped, this is just the
    typed row the repository hands back."""

    label: str
    severity: str
    case_count: int
    min_distance_km: float


@dataclass(frozen=True)
class PathogenRiskThreshold:
    """Trigger thresholds for one pathogen (spec §3.4) — backed by a static
    seed table (``thresholds.py``) until Tharun's full pathogen risk matrix
    lands. ``pathogen_id`` matches the diagnosis label vocabulary
    (``SUPPORTED_DIAGNOSIS_LABELS`` in ``gate_service.py``), e.g.
    ``"bacterial_leaf_blight"`` — not a separate id space."""

    pathogen_id: str
    pathogen_name: str
    target_crop: str
    susceptible_stages: tuple[str, ...]
    temp_min_c: float
    temp_max_c: float
    humidity_min_pct: float
    sustained_hours: int
    cluster_radius_km: float
    cluster_count_threshold: int
    preventative_action: str


@dataclass(frozen=True)
class AlertDraft:
    """Pure ``evaluate_alert`` output — an alert that *would* fire, before
    ``AlertService`` applies cooldown gating (spec §4.2) and persists it."""

    alert_id: str
    farm_id: str | None
    district: str
    pathogen_name: str
    target_crop: str
    target: AlertTarget
    severity: AlertSeverity
    trigger_reason: str
    preventative_action: str
    spoken_summary: str
    delivery_channels: tuple[DeliveryChannel, ...]
    created_at: datetime
    expires_at: datetime
    cooldown_key: str
