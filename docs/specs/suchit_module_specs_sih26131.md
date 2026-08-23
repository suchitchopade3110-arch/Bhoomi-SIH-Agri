# Specification: Bhoomi Intelligence Layer Realignment (SIH26131)

> **Document ID:** SPEC-SUCHIT-001  
> **Status:** Draft v1.0 (Ready for Team Review & Stage B Implementation)  
> **Author:** Suchit (Backend Intelligence Lead)  
> **Modules Owned:** Health/Risk Score Engine, Confidence Gate, RAG Pipeline, Escalation Compiler  
> **Basis:** `Bhoomi_Feature_Realignment_SIH26131.md` + `Bhoomi_API_Contract_SIH26131.txt` §7–§11 + `Bhoomi_Team_Work_Split_SIH26131.md`

---

## 1. Crop Risk / Problem Severity Score (Rework of PRD §7)

### 1.1 Sub-Index Evolution & Pruning

The legacy PRD §7 model utilized six sub-indices. Two have been removed due to the simplification of farmer onboarding (dropping cadastral land verification and irrigation scheduling):

| Old Sub-Index | Weight | Fate | Rationale |
|:---|:---:|:---|:---|
| **Environmental suitability** | 0.20 | **Reworked** $\rightarrow$ `environmental_risk` | Reframed from "suitability for growth" to "pathogen/pest outbreak risk favoring infection". |
| **Resource adequacy** | 0.15 | **Cut** | Required irrigation-vs-evapotranspiration metrics from the cut resource planner. |
| **Crop-stage progression** | 0.15 | **Cut** | Required detailed planting schedules; simplified 3-field onboarding no longer collects this. |
| **Active problem load** | 0.30 | **Kept & Strengthened** $\rightarrow$ `active_problem_severity` | Core focus of pest/disease surveillance; expanded to 0.40 weight. |
| **Monitoring recency** | 0.10 | **Kept** $\rightarrow$ `monitoring_recency` | Tracks data freshness; increased to 0.15 weight. |
| **Treatment response** | 0.10 | **Kept & Strengthened** $\rightarrow$ `treatment_response` | Reflects management efficacy; increased to 0.20 weight. |

---

### 1.2 New Weights (Sum = 1.00)

```python
WEIGHTS_V2_SIH26131 = {
    "active_problem_severity": 0.40,
    "environmental_risk": 0.25,
    "monitoring_recency": 0.15,
    "treatment_response": 0.20,
}
WEIGHTS_VERSION = "v2-sih26131"
```

| # | Sub-Index | Weight | Metric Definition |
|:---:|:---|:---:|:---|
| 1 | **`active_problem_severity`** | **0.40** | Open disease and pest problems, weighted by severity tiers. |
| 2 | **`environmental_risk`** | **0.25** | Meteorological and regional outbreak pressure favoring pathogen multiplication. |
| 3 | **`monitoring_recency`** | **0.15** | Decay based on elapsed days since last photo diagnosis or active check-in. |
| 4 | **`treatment_response`** | **0.20** | Trajectory of active treatments (`improved`, `no_change`, `got_worse`), baseline 70. |

---

### 1.3 Sub-Index Calculations

#### 1. `active_problem_severity` (Unified Disease + Pest)
```
active_problem_severity = max(0, 100 - Σ(severity_penalty_j))
```
- **Severity Penalties**: Early = **30**, Moderate = **55**, Severe = **80**.
- **Unified Problem Model**: Penalties sum identically across both `problem_type: "disease"` and `problem_type: "pest"`.
- **Follow-up Transitions**: `got_worse` promotes severity one tier (e.g. early $\rightarrow$ moderate); `improved` demotes one tier; resolution clears the penalty.

#### 2. `environmental_risk`
- Inputs: Open-Meteo temperature, relative humidity, rainfall duration, and regional outbreak signals from Shreekumar's early-warning system.
- `environmental_risk = 100 - risk_penalty`.
- **Fallback**: If regional alert feed is not yet available, scores solely on weather thresholds with `is_partial_signal: true`.

#### 3. `monitoring_recency`
- Starts at 90–100 upon new photo diagnosis; decays steadily with time since last scan.

#### 4. `treatment_response`
- Defaults to neutral baseline **70** on onboarding (no track record yet).
- **Update Rules**:
  - `got_worse` $\rightarrow$ **40** (spec anchor from 82 $\rightarrow$ 57 step).
  - Agronomist verified resolution $\rightarrow$ **95** (spec anchor from 57 $\rightarrow$ 91 step).
  - `improved` $\rightarrow$ **90** (interpolated positive recovery step).
  - `no_change` $\rightarrow$ **50** (interpolated stagnant step below baseline).

---

### 1.4 Unrated Gating Policy

A farm remains **`Unrated` (`score: null, band: "unrated"`)** until it records:
1. **At least one diagnosis or advisory interaction**, AND
2. **At least one successful weather sync**.

A bare 3-field profile (`crop`, `growth_stage`, `region`) with zero activity is not scored.

---

### 1.5 Deterministic Reconciliation Fixture (82 → 73 → 57 → 91)

| Step | State Description | `active_prob` (0.40) | `env_risk` (0.25) | `mon_rec` (0.15) | `treat_resp` (0.20) | Weighted Sum | Band |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **1. Baseline** | Day 0, first onboarding scan, no open problems | 100 (40.0) | 70 (17.5) | 70 (10.5) | 70 (14.0) | **82** | **Good** |
| **2. Diagnosis** | Early-stage stem borer pest detected (−30 penalty) | 70 (28.0) | 70 (17.5) | 90 (13.5) | 70 (14.0) | **73** | **Watch** |
| **3. Got Worse** | Severity promotes early $\rightarrow$ moderate; negative trend | 45 (18.0) | 70 (17.5) | 90 (13.5) | 40 (8.0) | **57** | **Poor (Escalated)** |
| **4. Resolved** | Agronomist intervenes, problem cleared, verified | 100 (40.0) | 70 (17.5) | 95 (14.25) | 95 (19.0) | **91** (90.75) | **Excellent** |

---

## 2. Confidence Gate Extension (Disease + Pest)

### 2.1 Decision: Shared Threshold (0.70), Separate Scope Vocabularies
- **`CONFIDENCE_GATE = 0.70`**: Shared across both `target_type: "disease"` and `target_type: "pest"`.
- **Target-Specific Scope Validation**: `SUPPORTED_LABELS["disease"]` vs `SUPPORTED_LABELS["pest"]`. A pest label appearing on a disease query triggers `OUT_OF_SCOPE_TARGET`, not confidence failure.

### 2.2 Gate Logic & Invariants

```python
def check_gate(
    *, target_type: Literal["disease", "pest"], label: str, confidence: float
) -> GateDecision:
    if label not in SUPPORTED_LABELS[target_type]:
        return GateDecision(
            above_gate=False,
            action="escalate",
            reason=f"Label '{label}' not in supported set for target_type={target_type}",
            error_code="OUT_OF_SCOPE_TARGET",
        )
    if confidence < CONFIDENCE_GATE:
        return GateDecision(
            above_gate=False,
            action="escalate",
            reason=f"Confidence {confidence:.2f} < gate {CONFIDENCE_GATE:.2f}",
            error_code="BELOW_CONFIDENCE_GATE",
        )
    return GateDecision(above_gate=True, action="compose_advisory")
```

**Testing Contract**: 8 deterministic test cases:
$\{\text{disease}, \text{pest}\} \times \{\text{above gate}, \text{below gate}\} \times \{\text{in scope}, \text{out of scope}\}$.

---

## 3. RAG Pipeline Scope (Pest vs Disease Retrieval)

### 3.1 Decision: Unified Index with Metadata Filtering
- Single `embeddings` pgvector table.
- Tagged with `content_type: "disease" | "pest"` and `crop: "samba_paddy" | ...`.
- Retrieval query: Vector similarity search + `WHERE content_type = :target_type AND crop = :crop`.

### 3.2 Dynamic Relevance Threshold (Codebase Inheritance)
- `RAG_RELEVANCE_THRESHOLD` is a single, shared threshold across both `disease` and `pest` content types (no separate pest threshold is invented).
- Sourced from the codebase's existing single-source-of-truth configuration (`app/domain/constants.py` $\rightarrow$ `app/core/config.py`):
  - Calibrated to `0.18` when `EMBEDDING_PROVIDER="stub"` (token-hashing vectors).
  - Calibrated to `0.60` when `EMBEDDING_PROVIDER="bge_m3"` (dense semantic embeddings).
  - Supports `RAG_RELEVANCE_THRESHOLD_OVERRIDE` for manual tuning.
- **Crop Filter**: Inherits Phase 3's metadata scoping (`crop: "samba_paddy" | ...`) to prevent cross-crop advisory leakage.
- Below threshold $\rightarrow$ `{retrieved: false, reason: "no_relevant_source"}` $\rightarrow$ prompt escalation to KVK expert.

---

## 4. Escalation Compiler: Redefined Case-Summary Bundle

### 4.1 Replaced Fields
- **Removed**: `area_acres_verified` and `soil_type` (cadastral land data cut).
- **Added**: `environmental_context` (weather/outbreak pressure) and `problem_history` (prior resolved/recurring problem log).

### 4.2 Case Summary Contract

```json
{
  "case_id": "c_5",
  "farm": {
    "id": "f_1",
    "crop": "cotton",
    "growth_stage": "flowering",
    "region": "Yavatmal"
  },
  "problem": {
    "id": "p_7",
    "target_type": "pest",
    "label": "stem_borer",
    "severity": "moderate"
  },
  "environmental_context": {
    "risk_subindex_value": 70,
    "note": "Elevated humidity and regional outbreak pressure favoring stem borer activity"
  },
  "problem_history": [
    {
      "problem_id": "p_3",
      "target_type": "pest",
      "label": "stem_borer",
      "resolved_at": "2026-07-02T10:00:00Z",
      "outcome": "resolved"
    }
  ],
  "timeline": [
    { "at": "2026-09-10T08:00:00Z", "event": "diagnosis", "detail": "stem_borer early" },
    { "at": "2026-09-12T09:00:00Z", "event": "followup", "detail": "got_worse" }
  ],
  "images": [
    { "asset_id": "a_9", "url": "https://storage.bhoomi.ag/assets/a_9.jpg" }
  ],
  "treatments_tried": [ "neem_oil_spray" ],
  "followup_trend": "got_worse",
  "current_risk": { "score": 57, "band": "poor" },
  "status": "assigned"
}
```

---

## 5. Finalized Endpoint Interfaces (API Contract §7–§11)

### 1. `GET /api/v1/farms/{id}/risk`
- **Response 200 (Active)**:
```json
{
  "score": 73,
  "band": "watch",
  "computed_at": "2026-09-11T06:00:00Z",
  "weights_version": "v2-sih26131",
  "subindices": [
    { "key": "active_problem_severity", "value": 70, "weight": 0.40, "contribution": 28.0 },
    { "key": "environmental_risk",      "value": 70, "weight": 0.25, "contribution": 17.5 },
    { "key": "monitoring_recency",      "value": 90, "weight": 0.15, "contribution": 13.5 },
    { "key": "treatment_response",      "value": 70, "weight": 0.20, "contribution": 14.0 }
  ],
  "triggering_input": {
    "type": "diagnosis",
    "problem_id": "p_7",
    "target_type": "pest",
    "severity": "early"
  },
  "spoken_summary": "Your farm risk score is 73 (Watch), triggered by a new early-stage stem borer diagnosis."
}
```
- **Response 200 (Unrated)**:
```json
{
  "score": null,
  "band": "unrated",
  "computed_at": "2026-09-11T06:00:00Z",
  "weights_version": "v2-sih26131",
  "subindices": [],
  "triggering_input": null,
  "spoken_summary": "Your farm is currently unrated. Submit a crop photo or sync weather to generate your score."
}
```

### 2. `GET /api/v1/farms/{id}/risk/history`
- Returns paginated list of snapshots walking the progression `[82, 73, 57, 91]`.

### 3. `POST /api/v1/farms/{id}/diagnose`
- **Request**:
```json
{
  "image_asset_id": "a_9",
  "description_asset_id": "a_10",
  "description_text": "Yellowing leaf tips with bore holes",
  "target_type": "pest"
}
```
- **Response (Above Gate)**:
```json
{
  "above_gate": true,
  "problem_id": "p_7",
  "target_type": "pest",
  "diagnosis": {
    "label": "stem_borer",
    "stage": "early",
    "confidence": 0.81
  },
  "advisory": {
    "possible_issue": "Paddy Stem Borer (Scirpophaga incertulas)",
    "what_to_check": "Inspect central shoots for dead hearts and bore holes near the waterline.",
    "what_to_do_next": "Apply pheromone traps at 5/ha or spray Bacillus thuringiensis @ 1 kg/ha.",
    "what_to_avoid": "Avoid excessive nitrogen application which accelerates larval feeding.",
    "expert_triggers": "Escalate if dead hearts exceed 10% in the tillering stage."
  },
  "citations": [
    { "doc_id": "rice_stem_borer.md", "title": "ICAR Package of Practices: Stem Borer Management", "reviewed_on": "2026-06-01" }
  ],
  "risk_delta": { "from": 82, "to": 73 },
  "spoken_summary": "Stem borer detected with 81% confidence. Advisory provided from ICAR guidelines."
}
```

### 4. `POST /api/v1/advisory/query`
- **Request**: `{ "farm_id": "f_1", "query_text": "How to control stem borer?", "lang": "en", "target_type": "pest" }`
- **Response**: 5-point advisory grounded strictly in retrieved ICAR chunks.

### 5. `GET /api/v1/cases/{id}`
- Returns the complete compiled case bundle defined in §4.2.

### 6. `GET /api/v1/farms/{id}/summary`
- Returns high-level dashboard summary card:
```json
{
  "farm": { "id": "f_1", "crop": "samba_paddy", "growth_stage": "tillering", "region": "Erode" },
  "risk": { "score": 73, "band": "watch", "computed_at": "2026-09-11T06:00:00Z" },
  "open_problems": 1,
  "pending_followups": 0,
  "spoken_summary": "1 active pest problem detected. Current risk score is 73 (Watch)."
}
```

---

## 6. Implementation Readiness & Stage B Scope
1. **Deterministic Unit Tests**: Extend existing `tests/domain/test_health_score.py` and `tests/domain/test_gate.py` with the 82 $\rightarrow$ 73 $\rightarrow$ 57 $\rightarrow$ 91 fixtures and the 8-case confidence gate test matrix.
2. **Scoring Backward Compatibility**: Introduce `WEIGHTS_V2_SIH26131 = {"active_problem_severity": 0.40, "environmental_risk": 0.25, "monitoring_recency": 0.15, "treatment_response": 0.20}` in `app/domain/health/constants.py` alongside the existing `v1` dictionary, stamped via `weights_version: "v2-sih26131"`.
3. **Database Repository Encapsulation**: Follow existing AGENTS.md rules where all DB queries for `TreatmentApplication` and `ProblemHistory` live strictly within `app/repositories/`.
