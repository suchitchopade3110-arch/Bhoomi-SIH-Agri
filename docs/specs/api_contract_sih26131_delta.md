# Specification: API Contract Realignment Delta (SIH25076 → SIH26131)

> **Document ID:** SPEC-CONTRACT-DELTA-001  
> **Status:** Stage A Spec (Pending Team Alignment)  
> **Author:** Drafted on Shreekumar's behalf — pending his review, not yet authored/approved by him.  
> **Target Release:** SIH26131 Transition (Flag-Gated)  
> **Guiding Principle:** **Zero Regression** — SIH25076 routes remain functional under `PROBLEM_STATEMENT=sih25076`.

> [!WARNING]
> **§2.1/§2.3 superseded.** This doc's original plan was to unmount `land`,
> `officer`, and `schemes` under `sih26131` alongside `resource_plan`. The
> implementation shipped differently: only `resource_plan` is
> SIH25076-exclusive — `land`/`officer`/`schemes` stayed mounted in both
> modes. `tests/unit/test_problem_statement_gating.py` is the authoritative
> contract for what's actually gated; see README.md §5 for the reasoning.
> Section 3 (new SIH26131 routes) reflects what was planned; see README.md
> §9 for current build status of pest `target_type` support (§3.1) and
> treatment efficacy (§3.4).

---

## 1. Problem Statement Gating Strategy

To allow seamless pivoting between SIH25076 and SIH26131 without deleting working code, the backend introduces a top-level configuration toggle in `app/core/config.py`:

```python
PROBLEM_STATEMENT: Literal["sih25076", "sih26131"] = Field(
    default="sih25076",
    description="Switches API surface between SIH25076 (Cadastral/Resource) and SIH26131 (Pest/Alert/Efficacy)",
)
```

In `app/main.py`, routers are mounted conditionally:
- **`sih25076` (Default Mode):** SIH25076-specific routers (`land`, `resource_plan`, `schemes`, `officer`) mount alongside core intelligence.
- **`sih26131` (Surveillance & Efficacy Mode):** SIH25076-specific routes are unmounted (return `404 Not Found`). SIH26131-specific routers (`alerts`, `efficacy`) mount alongside core intelligence.
- **Core Intelligence (Active in All Modes):** `auth`, `farms`, `health`, `diagnose`, `followup`, `agronomist`, `voice`, `assets`, `timeline`, `weather`, and `system` remain active across both modes.

---

## 2. Deprecated Routes (SIH25076 Only)

The following routes are active under `sih25076` and are unmounted (respond with `404 Not Found`) when `PROBLEM_STATEMENT=sih26131`:

### 2.1 Cadastral Land & Officer Review Routers (`app/api/v1/land.py`, `app/api/v1/officer.py`)
- **Mounted Router Paths**:
  - `POST /api/v1/land/verify` (and spec alias `POST /api/v1/farms/{id}/land`)
  - `GET /api/v1/land/{farm_id}` (and spec alias `GET /api/v1/land/{id}`)
  - `POST /api/v1/land/cadastral-lookup`
  - `GET /api/v1/officer/queue` (and spec alias `GET /api/v1/officer/land-queue`)
  - `GET /api/v1/officer/review/{parcel_id}`
  - `POST /api/v1/officer/action` (and spec alias `POST /api/v1/officer/land/{id}/review`)
- **Deprecation Rationale**: SIH26131 focuses on pest surveillance and closed-loop treatment efficacy rather than land title verification and revenue officer boundary workflows.

### 2.2 Resource Planning Router (`app/api/v1/resource_plan.py`)
- **Mounted Router Paths**:
  - `POST /api/v1/resource-plan/{farm_id}` (and spec alias `POST /api/v1/farms/{id}/resource-plan`)
  - `GET /api/v1/resource-plan/{farm_id}/latest` (and spec alias `GET /api/v1/farms/{id}/resource-plan/latest`)
- **Deprecation Rationale**: Resource calculation (FAO-56 irrigation and seed budgeting) is de-scoped from SIH26131.

### 2.3 Government Scheme Discovery Router (`app/api/v1/schemes.py`)
- **Mounted Router Paths**:
  - `POST /api/v1/schemes/match` (and spec alias `GET /api/v1/farms/{id}/schemes`)
  - `GET /api/v1/schemes/active`
  - `GET /api/v1/schemes/{scheme_id}`
- **Deprecation Rationale**: Scheme discovery is de-scoped from SIH26131.

---

## 3. New Routes (SIH26131 Additions)

### 3.1 Pest Diagnosis Integration (`POST /api/v1/diagnose` with `target_type: "pest"`)
> [!NOTE]
> **Resolved Architectural Decision (Confidence Gate Extension):**  
> We use a single unified `POST /api/v1/diagnose` endpoint with a `target_type: Literal["disease", "pest"] = "disease"` discriminator (per API Contract §8).  
> **Confidence Gate Mechanism:** The gate evaluates `target_type` internally against independent thresholds:
> - `CONFIDENCE_GATE = 0.70` for `target_type="disease"` (checked against `DISEASE_SCOPE`)
> - `PEST_CONFIDENCE_GATE = 0.70` for `target_type="pest"` (checked against `PEST_SCOPE`, independently tunable)
> 
> **Retrieval & Grounding Guarantee:** `RAG_RELEVANCE_THRESHOLD` is computed dynamically from `EMBEDDING_PROVIDER` — `0.18` against the stub adapter, `0.60` against real BGE-m3 embeddings. Swapping the adapter swaps the threshold automatically; there is no manual step to remember. Pest advisories use the same threshold and no-fabrication guarantee as disease advisories — no separate, weaker threshold.

**Request Schema:**
```json
{
  "farm_id": "f_123",
  "image_asset_id": "asset_pest_102",
  "target_type": "pest",
  "pest_type_hint": "stem_borer",
  "crop_stage": "vegetative",
  "additional_notes": "Larvae holes visible on central shoot"
}
```

**Response Schema:**
```json
{
  "above_gate": true,
  "target_type": "pest",
  "label": "Yellow Stem Borer (Scirpophaga incertulas)",
  "confidence": 0.88,
  "stage": "moderate",
  "pest_count_estimate": 4,
  "advisory": {
    "possible_issue": "Yellow Stem Borer vegetative damage (Deadheart)",
    "what_to_check": "Pull central shoot; check for larval boreholes at base",
    "what_to_do_next": "Install pheromone traps @ 5/acre; apply cartap hydrochloride 4G",
    "what_to_avoid": "Do not apply excessive urea which attracts oviposition",
    "expert_triggers": "More than 10% deadhearts in field",
    "citations": [
      {
        "doc_id": "rice_stem_borer",
        "title": "ICAR PoP: Rice Stem Borer Management",
        "reviewed_on": "2025-11-02"
      }
    ]
  },
  "health_delta": null,
  "escalation": null,
  "spoken_summary": "Identified Yellow Stem Borer with 88% confidence. Install 5 pheromone traps per acre."
}
```
*Note on `health_delta`: Set to `null` in this illustrative response. Exact score movement depends on pest severity tiers — pending Tharun's severity criteria spec. The underlying mechanism is identical to disease: the active problem load sub-index drops per severity penalty. The fields `stage: "moderate"` and `pest_count_estimate: 4` are illustrative placeholders pending Tharun's pest classification schema.*

### 3.2 Early-Warning Alerts (`GET /api/v1/farms/{id}/alerts`)
- **Method:** `GET`
- **Path:** `/api/v1/farms/{farm_id}/alerts`
- **Description:** Retrieve active meteorological and spatial cluster outbreak alerts for the farm.

**Response:**
```json
{
  "farm_id": "f_123",
  "active_alerts": [
    {
      "alert_id": "alt_889",
      "pathogen_name": "Bacterial Leaf Blight",
      "severity": "warning",
      "trigger_reason": "High humidity (84%) sustained >48h + 3 confirmed cases within 8km",
      "preventative_action": "Apply prophylactic Pseudomonas fluorescens; avoid field movement while wet",
      "spoken_summary": "Warning: High risk of leaf blight in your village. Spray Pseudomonas within 2 days.",
      "created_at": "2026-08-23T06:00:00Z",
      "expires_at": "2026-08-25T06:00:00Z"
    }
  ]
}
```

### 3.3 Alert Acknowledgement (`POST /api/v1/alerts/{alert_id}/acknowledge`)
> [!NOTE]
> **Phase 3 build-order correction:** this route was originally drafted as
> `POST /api/v1/alerts/{alert_id}/dismiss`; the Phase 3 build order names it
> `/acknowledge` instead ("farmer dismiss/confirm-seen"). Implemented as
> `/acknowledge` — the path below reflects the corrected, implemented route.
- **Method:** `POST`
- **Path:** `/api/v1/alerts/{alert_id}/acknowledge`
- **Request:** `{"farm_id": "f_123", "reason": "action_taken"}`
- **Response:** `200 OK` `{"status": "acknowledged", "alert_id": "alt_889"}`

### 3.4 Treatment Efficacy Query (`GET /api/v1/treatments/{treatment_id}/efficacy`)
- **Method:** `GET`
- **Path:** `/api/v1/treatments/{treatment_id}/efficacy`
- **Query Parameters:** `crop=samba_paddy&district=Erode`
- **Description:** Program-level real-world efficacy statistics aggregated from closed-loop follow-up streams.

---

## 4. Realigned Complete Endpoint Index (§2.16 Replacement)

> [!WARNING]
> **⚠️ DEVIATION FROM PRD §2.3:** Current backend implementation uses generic authentication (`/auth/register`, `/auth/login`, `/auth/me`) across all roles; PRD §2.3 specifies farmer phone-OTP (`/auth/otp/request`, `/auth/otp/verify`) and officer/agronomist password auth. Needs a separate decision, out of scope for this delta doc.

| Method | Path | Role / Access | Mode Gating | Description |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Public | All | Register farmer, officer, or agronomist |
| `POST` | `/api/v1/auth/login` | Public | All | Password login, returns role-claim JWT |
| `GET` | `/api/v1/auth/me` | Authenticated | All | Retrieve authenticated user profile |
| `GET` | `/api/v1/system/health` | Public | All | System health, DB connectivity, version |
| `POST` | `/api/v1/assets/presign` | Authenticated | All | Presigned URL upload for audio/photos |
| `GET` | `/api/v1/assets/{asset_id}` | Authenticated | All | Retrieve metadata/stream for stored asset |
| `POST` | `/api/v1/voice/transcribe` | Farmer | All | ASR transcription + intent extraction |
| `POST` | `/api/v1/voice/confirm` | Farmer | All | Voice read-back field confirmation gate |
| `POST` | `/api/v1/voice/synthesize` | Farmer | All | Text-to-speech synthesis for responses |
| `POST` | `/api/v1/voice/process` | Farmer | All | Full audio-in / audio-out processing |
| `POST` | `/api/v1/farms` | Farmer | All | Create farm profile *(Note: Request schema differs by `PROBLEM_STATEMENT` — `sih25076`: 6 fields [crop, area, growth_stage, soil_type, irrigation_access, season]; `sih26131`: 3 fields [crop, growth_stage, region]. See Bhoomi_Feature_Realignment_SIH26131.md Rework table.)* |
| `GET` | `/api/v1/farms/{id}` | Farmer | All | Read farm profile & status |
| `PUT` | `/api/v1/farms/{id}` | Farmer | All | Update farm profile attributes |
| `GET` | `/api/v1/farms/{id}/summary` | Farmer | All | Spoken & visual farm summary |
| `GET` | `/api/v1/farms/{id}/health` | Farmer | All | Transparent 6-part HealthSnapshot |
| `GET` | `/api/v1/farms/{id}/health/history` | Farmer | All | Historical health score snapshots |
| `POST` | `/api/v1/farms/{id}/health/recompute` | Farmer/Admin | All | Deterministic health score recompute |
| `GET` | `/api/v1/farms/{id}/weather` | Farmer | All | Current weather & observation data |
| `GET` | `/api/v1/farms/{id}/weather/forecast`| Farmer | All | Multi-day meteorological forecast |
| `GET` | `/api/v1/farms/{id}/weather/et0` | Farmer | All | Daily ET0 evapotranspiration values |
| `GET` | `/api/v1/farms/{id}/timeline` | Farmer | All | Chronological events timeline |
| `POST` | `/api/v1/farms/{id}/timeline/event` | Farmer | All | Append manual event to timeline |
| `POST` | `/api/v1/diagnose` | Farmer | All | Image diagnosis (`target_type: disease\|pest`, Gate 0.70 / Pest Gate 0.70) |
| `POST` | `/api/v1/advisory` | Farmer | All | 5-point ICAR PoP grounded advisory |
| `POST` | `/api/v1/followup/checkin` | Farmer | All | Closed-loop follow-up (`improved`/`got_worse`) |
| `POST` | `/api/v1/escalation` | Farmer/System | All | Create manual/automatic escalation case |
| `GET` | `/api/v1/cases/{id}` | Agronomist/Farmer | All | Read living case summary by ID |
| `GET` | `/api/v1/agronomist/queue` | Agronomist | All | Case summary queue for escalated problems |
| `GET` | `/api/v1/agronomist/cases/{id}` | Agronomist | All | Agronomist detail view of living case |
| `POST` | `/api/v1/agronomist/resolve` | Agronomist | All | Expert prescription resolution (86 Health) |
| `GET` | `/api/v1/farms/{id}/alerts` | Farmer | `sih26131` | Early-warning outbreak alerts |
| `POST` | `/api/v1/alerts/{id}/acknowledge` | Farmer | `sih26131` | Dismiss/acknowledge active alert |
| `GET` | `/api/v1/treatments/{id}/efficacy`| Agronomist | `sih26131` | Treatment efficacy analytics |
| `POST` | `/api/v1/land/verify` | Farmer | `sih25076` | Land registry auto-lookup / HITL queue |
| `POST` | `/api/v1/land/cadastral-lookup` | Farmer | `sih25076` | Cadastral survey lookup |
| `GET` | `/api/v1/land/{id}` | Farmer/Officer | `sih25076` | Cadastral land parcel status |
| `GET` | `/api/v1/officer/queue` | Officer | `sih25076` | Revenue officer land review queue |
| `GET` | `/api/v1/officer/review/{id}` | Officer | `sih25076` | Officer detail review for parcel |
| `POST` | `/api/v1/officer/action` | Officer | `sih25076` | Boundary review approval/rejection |
| `POST` | `/api/v1/resource-plan/{farm_id}` | Farmer | `sih25076` | FAO-56 resource planning calculation |
| `GET` | `/api/v1/resource-plan/{id}/latest`| Farmer | `sih25076` | Inspect active resource plan |
| `POST` | `/api/v1/schemes/match` | Farmer | `sih25076` | Scheme matching for verified farmers |
| `GET` | `/api/v1/schemes/active` | Farmer | `sih25076` | List currently active government schemes |
