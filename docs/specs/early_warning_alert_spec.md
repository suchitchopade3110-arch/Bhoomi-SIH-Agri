# Specification: Early-Warning Pest & Disease Outbreak Alert System (SIH26131)

> **Document ID:** SPEC-ALERT-001  
> **Status:** Stage A Spec (Pending Team Review)  
> **Author:** Shreekumar (Backend Intelligence)  
> **Target Release:** SIH26131 Realignment  
> **Dependencies:** Blocked on Tharun's Pest Severity Criteria & Risk Thresholds

---

## 1. Executive Summary & Problem Context

In SIH26131, Bhoomi evolves from a purely reactive advisory platform (where the farmer notices symptoms and submits a photo) to a **proactive early-warning surveillance network**. The Early-Warning Alert System monitors meteorological conditions and spatial disease clusters to warn farmers *before* pathogens spread uncontrollably.

---

## 2. Trigger Model & Architectural Recommendation

### 2.1 Recommended Model: Hybrid Meteorological-Geospatial Cluster Trigger

We recommend a **two-tier hybrid trigger model** combining:
1. **Macro-Meteorological Thresholds**: Temperature, relative humidity, and rainfall duration crossing pathogen-favorable multiplication bands (e.g., $RH > 80\%$, $Temp \in [25^\circ C, 32^\circ C]$ sustained for $\ge 48\text{h}$ for Bacterial Leaf Blight / Blast).
2. **Micro-Geospatial Outbreak Density**: Confirmed diagnoses recorded in neighboring farms within a geographic radius $R$ crossing a density threshold $K$ within a sliding time window $T$ (e.g., $\ge 3$ confirmed cases within $10\text{ km}$ over the past $7\text{ days}$).

### 2.2 Decision Rationale
- **Single-Trigger Failure Modes**: Pure weather forecasting yields high false-alarm rates (crying wolf), reducing farmer compliance. Pure outbreak clusters detect infections only after significant spread has already occurred.
- **Hybrid Synergy**: A spatial cluster in adjacent villages elevates risk from `INFO` to `WARNING`; combining a local cluster with favorable outbreak weather escalates the alert to `EMERGENCY` with mandatory preventative spray advisories.

---

## 3. System Inputs & Port Dependencies

### 3.1 Per-Farm Context
- `farm_id`: UUID
- `coordinates`: `(latitude, longitude)` (WGS84)
- `crop`: Primary crop (e.g., `samba_paddy`)
- `growth_stage`: e.g., `vegetative`, `tillering`, `panicle_initiation`, `flowering`
- `taluk` / `district`: Administrative boundary

### 3.2 Live Meteorological Data
- Accessed strictly through the existing `WeatherPort` protocol (`app/ports/weather.py`).
- Metrics evaluated:
  - 48-hour average temperature ($^\circ\text{C}$)
  - 48-hour average relative humidity ($\%$)
  - Rainfall accumulation (mm)

### 3.3 PostGIS Spatial Cluster Query
Recent verified problem records within radius $R$ are queried via PostGIS `ST_DWithin`:

```sql
SELECT 
    p.problem_type,
    p.severity,
    COUNT(p.id) AS case_count,
    MIN(ST_Distance(f.location, target_farm.location)) AS min_distance_meters
FROM problems p
JOIN farms f ON p.farm_id = f.id
CROSS JOIN (SELECT location FROM farms WHERE id = :target_farm_id) AS target_farm
WHERE 
    p.created_at >= NOW() - INTERVAL '7 days'
    AND p.status IN ('diagnosed', 'escalated')
    AND ST_DWithin(f.location, target_farm.location, :radius_meters)
    AND f.id != :target_farm_id
GROUP BY p.problem_type, p.severity;
```

### 3.4 Risk Threshold Interface (*Blocked on Tharun*)
> [!IMPORTANT]
> **Dependency Flag:** The engine requires agronomic pathogen thresholds from Tharun. Until delivered, the engine consumes this typed lookup interface backed by an in-memory stub table:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PathogenRiskThreshold:
    pathogen_id: str
    target_crop: str
    susceptible_stages: tuple[str, ...]
    temp_min_c: float
    temp_max_c: float
    humidity_min_pct: float
    sustained_hours: int
    cluster_radius_km: float
    cluster_count_threshold: int
```

---

## 4. Domain Model & Output Contract

### 4.1 Alert Domain Entity

```python
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

class Alert(BaseModel):
    alert_id: str
    farm_id: str | None  # None for regional broadcast
    pathogen_name: str
    target: AlertTarget
    severity: AlertSeverity
    trigger_reason: str
    preventative_action: str
    spoken_summary: str
    delivery_channels: list[DeliveryChannel]
    created_at: datetime
    expires_at: datetime
    cooldown_key: str
```

---

## 5. Delivery Semantics & Push/Passive Dual Strategy

To guarantee reach across varying farmer connectivity levels, alerts use a **dual delivery strategy**:

1. **Active Push Notification (`push`)**: Broadcasted via FCM/APNS for immediate high-priority warnings (`WARNING`, `EMERGENCY`).
2. **Passive Dashboard Surfacing (`home_banner` & `GET /farms/{id}/summary`)**:
   - Every active alert is indexed in `GET /farms/{id}/alerts`.
   - The farm summary endpoint includes an `active_alerts` summary block so that even if push permissions are disabled or the device was offline, the farmer sees the warning upon next opening the app.
3. **Voice Read-Out (`voice_briefing`)**: Integrated with Bhoomi's voice assistant to read unacknowledged alerts on the next voice interaction.

---

## 6. Deduplication & Cooldown Policy

To prevent alert fatigue:
- **Cooldown Key Formula**: `hash(farm_id, pathogen_name, severity_level)`
- **Cooldown Duration**:
  - `INFO` / `ADVISORY`: **72 hours**
  - `WARNING`: **48 hours**
  - `EMERGENCY`: **24 hours**
- **Escalation Exception**: If the alert severity upgrades (e.g., from `ADVISORY` to `EMERGENCY` due to a newly detected nearby cluster), the cooldown is bypassed immediately.

---

## 7. Next Steps & Stage B Checkpoints

1. Team review & sign-off on trigger formula and PostGIS query.
2. Ingestion of Tharun's pest severity lookup tables.
3. Implementation of `app/domain/alerts/`, `app/services/alerts/engine.py`, and `app/repositories/alert_repo.py`.
