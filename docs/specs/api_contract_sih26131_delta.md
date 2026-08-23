# Specification: API Contract Realignment Delta (SIH25076 → SIH26131)

> **Document ID:** SPEC-CONTRACT-DELTA-001  
> **Status:** Stage A Spec (Pending Team Alignment)  
> **Author:** Shreekumar (Backend Intelligence)  
> **Target Release:** SIH26131 Transition (Flag-Gated)  
> **Guiding Principle:** **Zero Regression** — SIH25076 routes remain functional under `PROBLEM_STATEMENT=sih25076`.

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
- SIH25076-specific routers (`land`, `resource_plan`, `schemes`) mount only when `settings.PROBLEM_STATEMENT == "sih25076"`.
- SIH26131-specific routers (`alerts`, `efficacy`, `pest_diagnosis`) mount when `settings.PROBLEM_STATEMENT == "sih26131"`.
- Core intelligence routers (`auth`, `farms`, `health`, `diagnose`, `followup`, `agronomist`, `voice`) remain active across both modes.

---

## 2. Deprecated Routes (SIH25076 Only)

The following routes are active under `sih25076` and respond with `404 Not Found` (or `410 Gone`) under `sih26131`:

| Method | Path | Original Purpose | Deprecation Reason in SIH26131 |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/land/verify` | Cadastral land auto-lookup | SIH26131 focuses on pest/disease surveillance, not land registry |
| `GET` | `/api/v1/land/{id}` | Land parcel boundary & status | Land verification HITL removed from scope |
| `GET` | `/api/v1/officer/queue` | Revenue officer land review queue | Officer portal superseded by KVK agronomist dashboard |
| `POST` | `/api/v1/officer/action` | Officer boundary verification | Replaced by agronomist case review |
| `POST` | `/api/v1/resource-plan/{farm_id}` | FAO-56 irrigation/seed planner | Resource planning cut from SIH26131 core workflow |
| `GET` | `/api/v1/resource-plan/{farm_id}/latest`| Read active resource plan | Cut from SIH26131 core workflow |
| `POST` | `/api/v1/schemes/match` | Scheme eligibility matching | Scheme discovery cut from SIH26131 core workflow |

---

## 3. New Routes (SIH26131 Additions)

### 3.1 Pest Diagnosis Extension (`POST /api/v1/farms/{id}/diagnose/pest`)
> [!IMPORTANT]
> **Decision Flag (Blocked on Suchit's Confidence Gate Extension):**  
> We recommend a dedicated endpoint `POST /farms/{id}/diagnose/pest` rather than overloading the disease diagnosis endpoint with a `type: pest|disease` parameter.  
> **Rationale:** Pest detection typically employs an object-detection model (YOLOv8 bounding boxes with count density) with a separate confidence gate (e.g., $0.65$) rather than disease classification ($0.70$). A dedicated endpoint provides distinct request/response contracts while reusing the same RAG citation pipeline.

**Request Schema:**
```json
{
  "image_asset_id": "asset_pest_102",
  "pest_type_hint": "stem_borer",
  "crop_stage": "vegetative",
  "additional_notes": "Larvae holes visible on central shoot"
}
```

**Response Schema:**
```json
{
  "pest_name": "Yellow Stem Borer (Scirpophaga incertulas)",
  "confidence": 0.88,
  "above_gate": true,
  "infestation_level": "moderate",
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
  "escalation": null
}
```

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

### 3.3 Alert Dismissal (`POST /api/v1/alerts/{alert_id}/dismiss`)
- **Method:** `POST`
- **Path:** `/api/v1/alerts/{alert_id}/dismiss`
- **Request:** `{"farm_id": "f_123", "reason": "action_taken"}`
- **Response:** `200 OK` `{"status": "dismissed", "alert_id": "alt_889"}`

### 3.4 Treatment Efficacy Query (`GET /api/v1/treatments/{treatment_id}/efficacy`)
- **Method:** `GET`
- **Path:** `/api/v1/treatments/{treatment_id}/efficacy`
- **Query Parameters:** `crop=samba_paddy&district=Erode`
- **Description:** Program-level real-world efficacy statistics aggregated from closed-loop follow-up streams.

---

## 4. Realigned Complete Endpoint Index (§2.16 Replacement)

| Method | Path | Role / Access | Mode Gating | Description |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Public | All | Register farmer, officer, or agronomist |
| `POST` | `/api/v1/auth/login` | Public | All | OAuth2 password login, returns JWT |
| `GET` | `/api/v1/system/health` | Public | All | System health, DB connectivity, version |
| `POST` | `/api/v1/voice/transcribe` | Farmer | All | ASR transcription + intent extraction |
| `POST` | `/api/v1/voice/confirm` | Farmer | All | Voice read-back field confirmation gate |
| `POST` | `/api/v1/farms` | Farmer | All | Create farm profile (Day 0 Unrated) |
| `GET` | `/api/v1/farms/{id}` | Farmer | All | Read farm profile & health status |
| `GET` | `/api/v1/farms/{id}/health` | Farmer | All | Transparent 6-part HealthSnapshot |
| `POST` | `/api/v1/farms/{id}/health/recompute` | Farmer/Admin | All | Deterministic health score recompute |
| `POST` | `/api/v1/farms/{id}/diagnose` | Farmer | All | Image diagnosis + cited advisory (Gate 0.70) |
| `POST` | `/api/v1/farms/{id}/diagnose/pest`| Farmer | `sih26131` | Pest detection & bounding-box advisory |
| `GET` | `/api/v1/farms/{id}/alerts` | Farmer | `sih26131` | Early-warning outbreak alerts |
| `POST` | `/api/v1/alerts/{id}/dismiss` | Farmer | `sih26131` | Dismiss/acknowledge active alert |
| `POST` | `/api/v1/followup/checkin` | Farmer | All | Closed-loop follow-up (`improved`/`got_worse`) |
| `GET` | `/api/v1/agronomist/queue` | Agronomist | All | Case summary queue for escalated problems |
| `POST` | `/api/v1/agronomist/resolve` | Agronomist | All | Expert prescription resolution (86 Health) |
| `GET` | `/api/v1/treatments/{id}/efficacy`| Agronomist | `sih26131` | Treatment efficacy analytics |
| `POST` | `/api/v1/land/verify` | Farmer | `sih25076` | Land registry auto-lookup / HITL queue |
| `GET` | `/api/v1/land/{id}` | Farmer/Officer | `sih25076` | Cadastral land parcel status |
| `GET` | `/api/v1/officer/queue` | Officer | `sih25076` | Revenue officer land review queue |
| `POST` | `/api/v1/officer/action` | Officer | `sih25076` | Boundary review approval/rejection |
| `POST` | `/api/v1/resource-plan/{farm_id}` | Farmer | `sih25076` | FAO-56 resource planning calculation |
| `GET` | `/api/v1/resource-plan/{id}/latest`| Farmer | `sih25076` | Inspect active resource plan |
| `POST` | `/api/v1/schemes/match` | Farmer | `sih25076` | Scheme matching for verified farmers |
