# Specification: Early-Warning Pest & Disease Outbreak Alert System (SIH26131)

> **Document ID:** SPEC-ALERT-001  
> **Status:** Stage A Spec (Revised & Aligned)  
> **Author:** Drafted on Shreekumar's behalf — pending his review, not yet authored/approved by him.  
> **Target Release:** SIH26131 Realignment  
> **Dependencies:** Agronomic thresholds backed by ICAR PoP corpus (`services/api/corpus/rice_blb.md`, doc_id `rice_blb` — corrected from this doc's original `rice_bacterial_leaf_blight.md` reference, which doesn't exist in the corpus; see Phase 3 build order); full pathogen matrix pending Tharun's criteria.

---

## 1. Executive Summary & Problem Context

In SIH26131, Bhoomi evolves from a purely reactive advisory platform (where the farmer notices symptoms and submits a photo) to a **proactive early-warning surveillance network**. The Early-Warning Alert System monitors meteorological conditions and spatial disease clusters to warn farmers *before* pathogens spread uncontrollably.

---

## 2. Trigger Model & Architectural Recommendation

### 2.1 Recommended Model: Hybrid Meteorological-Geospatial Cluster Trigger

We specify a **two-tier hybrid trigger model** combining:
1. **Macro-Meteorological Thresholds**: Temperature, relative humidity, and rainfall duration crossing pathogen-favorable multiplication bands.
   - *Example (Bacterial Leaf Blight)*: $RH \ge 80\%$, $Temp \in [25^\circ C, 32^\circ C]$ sustained for $\ge 48\text{h}$ *(doc_id: `rice_blb` — `services/api/corpus/rice_blb.md`; note the corpus prose itself only states "high humidity (above 70%)" with no explicit temp/duration figures, so the tighter band above is this spec's own directed value, not a literal corpus quote)*.
   - *Other Pathogens*: Illustrative defaults, pending Tharun's full pathogen risk threshold matrix.
2. **Micro-Geospatial Outbreak Density**: Confirmed diagnoses recorded in neighboring farms within a geographic radius $R$ crossing a density threshold $K$ within a sliding time window $T$ (e.g., $\ge 3$ confirmed cases within $10\text{ km}$ over the past $7\text{ days}$).

### 2.2 Decision Rationale
- **Single-Trigger Failure Modes**: Pure weather forecasting yields high false-alarm rates (crying wolf), reducing farmer compliance. Pure outbreak clusters detect infections only after significant spread has already occurred.
- **Hybrid Synergy**:
  - Weather favorable + No local cluster $\rightarrow$ `INFO` / `ADVISORY` (general vigilance notice).
  - Local spatial cluster + Normal weather $\rightarrow$ `WARNING` (spatial proximity alert).
  - Local spatial cluster + Pathogen-virulent weather $\rightarrow$ `EMERGENCY` (critical proactive intervention alert).

---

## 3. System Inputs & Repository Layering

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

> [!WARNING]
> **Phase 3 implementation note (deviation from "48-hour average"):**
> `WeatherPort.get_current_weather()` returns a single current-moment
> reading (`app/ports/weather.py`) — there is no historical weather store
> backing a true 48-hour rolling average or a "sustained N hours" signal.
> `AlertService` (`app/services/alert_service.py`) uses an honest, documented
> approximation instead: a current reading that already falls inside a
> pathogen's temp/humidity band is treated as having been sustained for
> exactly the threshold's required duration; a reading outside the band is
> treated as zero sustained hours. This is flagged in code, not silently
> assumed — swap in a real historical aggregation once a weather-history
> store exists, with no change to `evaluate_alert` itself (it only consumes
> `WeatherMetrics`, never `WeatherPort` directly).

### 3.3 Spatial Cluster Query (Repository Layered)

> [!WARNING]
> **Phase 1 Geo-Approach Decision (corrects this section's original PostGIS draft):**
> This spec originally called for `ST_DWithin`/`ST_Distance` over a PostGIS
> `location` geography column. The project's actual Postgres image is
> `pgvector/pgvector:pg16` — pgvector only; `infra/init-db.sql` has the
> `CREATE EXTENSION postgis` line commented out as "available when using
> postgis-enabled image", and no `farms.location` geometry column exists
> (`farms` has plain `latitude`/`longitude` `Float` columns — see
> `app/models/farm.py`). Standing up PostGIS is infra work nothing else in
> the codebase currently needs.
>
> **Decision:** until that infra change happens, the spatial cluster query
> uses the existing `latitude`/`longitude` columns: the repository
> pre-filters candidate farms with a cheap bounding-box `WHERE` clause (or a
> `district`/`taluk` filter), then applies the exact radius cutoff via the
> pure `haversine_distance_km` function in `app/domain/geo.py` (unit-tested
> in `tests/domain/test_geo.py`, no DB). Acceptable at this project's scale;
> revisit if per-district farm density grows large enough that the
> bounding-box pre-filter stops being selective.

> [!IMPORTANT]
> **Layering Guarantee (AGENTS.md Compliance):**  
> `services/alerts/` never executes raw SQL or imports database engines. The spatial query is encapsulated strictly inside `app/repositories/alert_repo.py` behind the typed interface method:
> ```python
> async def get_nearby_cluster_summary(
>     self, target_farm_id: str, radius_meters: float, window_days: int
> ) -> list[ClusterCase]: ...
> ```
> Internally it (1) looks up the target farm's own coordinates, (2) SQL-
> filters `problems`/`farms` rows to a bounding box + time window, then
> (3) calls `app.domain.geo.haversine_distance_km` per candidate to apply
> the exact radius cutoff and compute `min_distance_km` before grouping by
> `(label, severity)` into `ClusterCase` rows.

> [!WARNING]
> **Phase 1 `problem_status` Decision (corrects this section's original filter):**
> This spec originally filtered `p.status IN ('diagnosed', 'escalated')`.
> Neither value exists: `app/core/enums.py::ProblemStatus` is only
> `open | resolved` (contract §2.2); `escalated` is a `CaseStatus` value
> that lives on the separate escalation/case entity, not on `Problem.status`
> — that query would have silently returned zero rows forever.
>
> Also `p.problem_type` doesn't exist on the ORM model — `app/models/problem.py`
> names the column `label` (e.g. `"Bacterial Leaf Blight"`).
>
> **Decision:** apply **no status filter** — count every `Problem` row in
> the time window, `open` or `resolved`. Per §4.3 above, a `Problem` row is
> only ever created on a *confirmed* diagnosis, so every row is already a
> confirmed case by construction; the 7-day `created_at` window is what
> scopes recency. Restricting to `status = 'open'` would *undercount*: a
> neighboring farm whose blight was already treated and resolved is still
> real evidence the pathogen was circulating in the area within the window,
> which is exactly the signal this cluster query exists to catch.

**Repository SQL Implementation (bounding-box pre-filter):**
```sql
SELECT
    p.label,
    p.severity,
    f.id AS farm_id,
    f.latitude,
    f.longitude
FROM problems p
JOIN farms f ON p.farm_id = f.id
WHERE
    p.created_at >= NOW() - INTERVAL '7 days'
    AND f.latitude BETWEEN :min_lat AND :max_lat
    AND f.longitude BETWEEN :min_lon AND :max_lon
    AND f.id != :target_farm_id;
-- :min_lat/:max_lat/:min_lon/:max_lon come from
-- app.domain.geo.bounding_box(target_lat, target_lon, radius_km).
-- No status filter: every Problem row is a confirmed diagnosis by
-- construction (see the problem_status decision above); the repository
-- then filters these rows to the exact radius with
-- haversine_distance_km(...) and groups by (label, severity) in
-- Python before returning list[ClusterCase].
```

### 3.4 Risk Threshold Interface (*Pending Tharun's Matrix*)
> [!NOTE]
> **Dependency Flag:** Backed by an in-memory stub table with ICAR PoP seed values until Tharun delivers the full pest threshold matrix:

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

## 4. Pure Domain Evaluator & Determinism Contract

### 4.1 Determinism and Purity Rule
Mirroring the health score engine and confidence gate:
1. **Pure Domain Function**: The core evaluation logic lives in `app/domain/alerts/evaluate.py`:
   ```python
   def evaluate_alert(
       *,
       farm_id: str | None,
       district: str,
       crop: str,
       growth_stage: str,
       weather: WeatherMetrics,
       cluster_summary: list[ClusterCase],
       threshold: PathogenRiskThreshold,
       evaluated_at: datetime,
   ) -> AlertDraft | None:
   ```
2. **Deterministic Output**: Same inputs + injected `evaluated_at` timestamp $\rightarrow$ strictly identical `AlertDraft` every time. No random UUIDs, no `datetime.now()` calls inside the domain function.
3. **Deterministic `alert_id`**: Generated via UUIDv5 from a fixed namespace and deterministic key: `uuid5(NAMESPACE_BHOOMI_ALERTS, f"{farm_id or district}:{threshold.pathogen_id}:{severity.value}:{evaluated_at.date().isoformat()}")`.

### 4.2 Pipeline Separation: Pure Evaluation vs Cooldown State
To keep domain logic pure while preventing alert fatigue:
1. **Step 1 (Pure Domain Evaluation)**: `evaluate_alert(...)` calculates if conditions trigger an alert and returns an `AlertDraft` with computed `cooldown_key = f"{farm_id or district}:{pathogen_id}:{severity.value}"`.
2. **Step 2 (Service-Level Cooldown Gating)**: `AlertService` checks `AlertRepository.get_active_cooldown(cooldown_key)`.
   - If an active alert exists with $\ge$ same severity, the draft is suppressed (no duplicate delivery).
   - If no active alert exists, or if severity has upgraded (e.g., `ADVISORY` $\rightarrow$ `EMERGENCY`), the alert passes the cooldown gate. **On upgrade, `AlertService` marks any prior active lower-severity alert for that `(farm_id or district, pathogen_id)` as superseded/expired** so the farmer never sees redundant or contradictory concurrent banners.
3. **Step 3 (Persistence & Dispatch)**: `AlertService` persists the alert and dispatches delivery channels.

### 4.3 Relationship to the Problem Entity (Open Question Resolution)

> [!NOTE]
> **Resolution to Contract Open Question (§12):**  
> *"Does an alert create a Problem row or stay separate?"*

- **`INFO`, `ADVISORY`, `WARNING`**: **Do NOT create a `Problem` row.** They remain pure surveillance notices. A farm's `HealthSnapshot` is not penalized for an infection in a neighboring village that has not yet reached its own parcel.
- **`EMERGENCY`**: Does **NOT** directly create an open `Problem` row (which would artificially drop the health score before actual crop infection). Instead:
  1. It writes an advisory alert event to the farm's `Timeline`.
  2. It surfaces an urgent notification prompting farmer action: *"Outbreak alert: BLB detected within 3km in humid weather. Inspect your field now."*
  3. The prompt offers a one-tap action: **"I see symptoms"** (initiates `/diagnose` image upload) or **"Sprayed preventative"** (records treatment event on timeline).
  4. Only when a problem is confirmed via diagnosis does it create a `Problem` entity and apply the health score deduction.

---

## 5. Domain Model & Delivery Semantics

### 5.1 Alert Domain Entity

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
    farm_id: str | None          # None for regional broadcast
    district: str                # Administrative anchor for broadcasts
    pathogen_name: str
    target_crop: str
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

### 5.2 Regional Broadcast Fan-Out Mechanics
To avoid inserting tens of thousands of duplicate alert rows across all farms in a district:
- A regional outbreak alert is persisted **once** with `target = AlertTarget.REGIONAL_BROADCAST`, `farm_id = None`, and `district = "Erode"`.
- When querying `GET /api/v1/farms/{id}/alerts`, `AlertRepository` resolves relevant alerts via:
  ```sql
  SELECT * FROM alerts
  WHERE 
    (farm_id = :target_farm_id 
     OR (farm_id IS NULL AND district = :farm_district AND (target_crop IS NULL OR target_crop = :farm_crop)))
    AND expires_at > :current_time
  ORDER BY created_at DESC;
  ```
- *Database Indexing Requirement (Stage B)*: Requires a partial composite index `CREATE INDEX idx_alerts_broadcast ON alerts (district, target_crop, expires_at) WHERE farm_id IS NULL;` to prevent sequential scans during high-concurrency alert retrieval.
- This guarantees instantaneous zero-copy delivery across entire districts.

### 5.3 Delivery Channels
1. **Active Push Notification (`push`)**: FCM/APNS for `WARNING` and `EMERGENCY`.
2. **Passive Dashboard Surfacing (`home_banner` & `GET /farms/{id}/summary`)**: Surfaced in farm summary block for offline recovery.
3. **Voice Read-Out (`voice_briefing`)**: Unacknowledged alerts read during the next voice session.

---

## 6. Deduplication & Cooldown Policy

- **Cooldown Key Formula**: `f"{farm_id or district}:{pathogen_name}:{severity_level}"`
- **Cooldown Duration**:
  - `INFO` / `ADVISORY`: **72 hours**
  - `WARNING`: **48 hours**
  - `EMERGENCY`: **24 hours**
- **Escalation Exception**: Upgrading severity (e.g., `ADVISORY` $\rightarrow$ `EMERGENCY`) bypasses active cooldowns immediately.

---

## 7. Next Steps & Stage B Checkpoints

1. Unit tests for pure `evaluate_alert` using deterministic weather/cluster fixtures.
2. `AlertRepository` implementation with PostGIS spatial query.
3. Integration of `GET /farms/{id}/alerts` and `POST /alerts/{id}/acknowledge` routes in `app/api/v1/alerts.py` (Phase 3 build order Step 4 renamed `/dismiss` to `/acknowledge` — see `docs/specs/api_contract_sih26131_delta.md` §3.3's correction note).
