# Specification: Treatment Efficacy & Outcome Tracking Engine (SIH26131)

> **Document ID:** SPEC-EFFICACY-001  
> **Status:** Stage A Spec (Revised & Aligned)  
> **Author:** Drafted on Shreekumar's behalf — pending his review, not yet authored/approved by him.  
> **Target Release:** SIH26131 Realignment  
> **Stakeholders:** Thaariha (Agronomist Portal & Program Analytics), Shruthi (Database & ORM)

---

## 1. Context & Purpose

Bhoomi captures closed-loop follow-up check-ins (`improved`, `no_change`, `got_worse`). In SIH26131, we aggregate these localized outcomes across thousands of smallholders to measure **real-world treatment efficacy**.

This data directly feeds:
1. **Thaariha's Program-Level Agronomist Dashboard**: Providing regional KVKs with evidence-based data on which chemical/biological interventions are working versus failing against specific pathogens.
2. **Dynamic Trailing Efficacy & Resistance Tracking**: Monitoring trailing 12-month efficacy across districts to detect emerging antimicrobial or pesticide resistance.

---

## 2. Definition of Efficacy & Trailing Time Window

### 2.1 Definition of Efficacy
**Treatment Efficacy** is defined as the population-level success rate of a specific `(pathogen_type, treatment_name)` combination across all recorded farm applications within a given crop and regional context over a defined trailing evaluation window.

### 2.2 Trailing Time Window (Resistance Detection)
To detect emerging chemical/biological resistance rather than hiding recent declines inside lifetime averages:
- **Default Evaluation Window**: **Trailing 12 months (365 days)** ($T_{\text{applied}} \in [T_{\text{as\_of}} - 365\text{d}, T_{\text{as\_of}}]$).
- **Query-Time Evaluation**: Computed dynamically on-read from indexed aggregation tables, supporting an optional `window_months: int = 12` parameter (e.g., comparing trailing 3-month vs 12-month efficacy to spot seasonal resistance spikes).

---

## 3. Data Model, Attribution & Schema Specification

> [!IMPORTANT]
> **Schema Recommendation for Shruthi (Database Owner):**  
> We specify a dedicated `treatment_applications` table and an optional `treatment_application_id` Foreign Key on `followups`.

### 3.1 Controlled Vocabulary & Normalization
To prevent free-text fragmentation (e.g., `"Copper Hydroxide 77% WP"` vs `"copper_hydroxide"` splitting sample size):
- `treatment_name` is validated against canonical active ingredients in the **ICAR Package of Practices catalog** (seeded from `services/api/corpus/`).
- Prior to database insert, all treatment inputs undergo normalization:
  ```python
  def normalize_treatment_key(raw_name: str) -> str:
      return re.sub(r"[^a-z0-9]+", "_", raw_name.strip().lower()).strip("_")
  ```

### 3.2 Proposed Schema Structure (`app/models/treatment_application.py`)

```python
class TreatmentApplication(Base):
    __tablename__ = "treatment_applications"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_id: Mapped[str] = mapped_column(String, ForeignKey("problems.id"), nullable=False, index=True)
    farm_id: Mapped[str] = mapped_column(String, ForeignKey("farms.id"), nullable=False, index=True)
    
    # Normalized ICAR PoP vocabulary
    pathogen_type: Mapped[str] = mapped_column(String, nullable=False, index=True)  # e.g., "bacterial_leaf_blight"
    treatment_name: Mapped[str] = mapped_column(String, nullable=False, index=True)  # e.g., "copper_hydroxide_77_wp"
    treatment_category: Mapped[str] = mapped_column(String, nullable=False)          # "chemical", "biological", "cultural"
    
    applied_on: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    crop: Mapped[str] = mapped_column(String, nullable=False)
    district: Mapped[str] = mapped_column(String, nullable=False, index=True)
    
    # Resolved outcome state
    final_outcome: Mapped[str | None] = mapped_column(String, nullable=True)  # "resolved", "improved", "failed", "superseded"
    followups_to_resolution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    days_to_resolution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    failed_on_got_worse: Mapped[bool] = mapped_column(Boolean, default=False)
    escalated_for_expert: Mapped[bool] = mapped_column(Boolean, default=False)
```

### 3.3 FollowUp Attribution Rules & Lifecycle Updates

1. **Attribution Foreign Key & Default Rule**:
   - `followups.treatment_application_id` is an optional FK.
   - **Default Rule**: Every farmer check-in is attributed to the **most recent open `TreatmentApplication`** for that `problem_id`.
2. **Synchronous Lifecycle Updates (Who & When)**:
   - Updates are written **synchronously inside `FollowupService.checkin` and `AgronomistService.resolve`**.
   - *Rationale*: Synchronous updates within the check-in transaction guarantee immediate consistency for KVK analytics dashboards, eliminate background job lag, and avoid complex eventual-consistency reconciliation.
   - **On `improved` or problem resolution**: The active application is closed with `final_outcome = "improved"` / `"resolved"`, `followups_to_resolution = count(followups_for_app)`, `days_to_resolution = (checkin_date - applied_on).days`.
   - **On `got_worse`**: The active application is closed with `final_outcome = "failed"`, `failed_on_got_worse = True`.
   - **On `no_change`**: Increments `followups_to_resolution`. If $> 2$ consecutive `no_change` check-ins occur without improvement, the application is closed with `final_outcome = "failed"`.
   - **On treatment switch**: If a new treatment is prescribed for an open problem, the previous application is closed as `final_outcome = "superseded"`.

### 3.4 Worked Attribution Example (Sequential Treatments)
- **Scenario**: Problem $P_1$ diagnosed with Bacterial Leaf Blight on Day 0.
  1. **Day 0**: Farmer applies Treatment $A$ (`pseudomonas_fluorescens_spray`). System creates $T_1$ with `applied_on=Day 0, final_outcome=None`.
  2. **Day 7**: Farmer submits FollowUp 1 (`response="no_change"`). Attributed to $T_1$. $T_1$ remains open (`followups_to_resolution=1`).
  3. **Day 8**: Agronomist advises switching to Treatment $B$ (`copper_hydroxide_77_wp`). System marks $T_1$ as `final_outcome="superseded"`, and creates $T_2$ with `applied_on=Day 8, final_outcome=None`.
  4. **Day 14**: Farmer submits FollowUp 2 (`response="improved"`). Attributed to $T_2$. System updates $T_2$ to `final_outcome="improved", followups_to_resolution=1, days_to_resolution=6`.
- **Efficacy Attribution**: $T_1$ (superseded) is excluded from $N_{\text{total}}$ for `pseudomonas_fluorescens_spray`'s efficacy calculation — it is neither a success nor a failure. $T_2$ (improved) counts as one success out of one evaluated application ($1/1$) for `copper_hydroxide_77_wp`.

### 3.5 Database Indexing Requirement (Stage B)
To support fast regional aggregation across millions of check-in records:
```sql
CREATE INDEX idx_treatment_apps_efficacy 
ON treatment_applications (pathogen_type, treatment_name, crop, district, applied_on);
```

---

## 4. Efficacy Scoring Formula & Sample-Size Guard

### 4.1 Scoring Formula & Escalation Distinction

> [!IMPORTANT]
> **Resolution to Escalation Bias (PRD §7.4 Alignment):**  
> We distinguish between **Treatment Failure Escalation** (where the condition deteriorated despite treatment) and **Precautionary/Protocol Escalation** (safety checks or confidence gates that successfully resolved under expert care).

Let $N_{\text{total}}$ be the total number of evaluated applications for a `(pathogen_type, treatment_name)` pair within the trailing 12-month window (`applied_on >= as_of - 365 days`):

- **Success ($N_{\text{success}}$)**: Applications where:
  - `final_outcome IN ('resolved', 'improved')`
  - `failed_on_got_worse == False`
  - `followups_to_resolution <= 2`
  *(Note: Cases escalated for precautionary/gate reasons that achieved resolution are included in $N_{\text{success}}$).*
- **Failure ($N_{\text{failed}}$)**: Applications where:
  - `failed_on_got_worse == True` (problem worsened on follow-up), OR
  - `final_outcome == 'failed'` (e.g., $> 2$ consecutive `no_change` check-ins).

$N_{\text{total}} = N_{\text{success}} + N_{\text{failed}}$ only. Applications with `final_outcome IN ('superseded', NULL)` are excluded from $N_{\text{total}}$ entirely — they represent an application that was switched away from or has not yet reached a resolved state within the window, and contribute no signal about the treatment's own effectiveness.

$$\text{Efficacy Score (\%)} = \left( \frac{N_{\text{success}}}{N_{\text{total}}} \right) \times 100$$

### 4.2 Minimum Sample-Size Floor ($N \ge 10$)
- **Floor Rule**: To prevent misleading claims (e.g., $1/1 = 100\%$ efficacy), any aggregation with $N_{\text{total}} < 10$ returns `status: "insufficient_data"`.
- **Response Contract (Insufficient Data)**:

```json
{
  "treatment_id": "copper_hydroxide_77_wp",
  "pathogen": "bacterial_leaf_blight",
  "crop": "samba_paddy",
  "region": "Erode",
  "status": "insufficient_data",
  "sample_size": 4,
  "min_sample_threshold": 10,
  "efficacy_percentage": null,
  "avg_days_to_recovery": null
}
```

- **Response Contract (Statistically Significant)** ($N_{\text{total}} \ge 10$):

```json
{
  "treatment_id": "copper_hydroxide_77_wp",
  "pathogen": "bacterial_leaf_blight",
  "crop": "samba_paddy",
  "region": "Erode",
  "status": "statistically_significant",
  "sample_size": 48,
  "min_sample_threshold": 10,
  "efficacy_percentage": 85.4,
  "avg_days_to_recovery": 4.2
}
```

---

## 5. Pure Domain Engine & Determinism Contract

### 5.1 Pure Calculation Signature
Mirroring the health engine and confidence gate, the aggregation calculation is a pure domain function in `app/domain/efficacy/score.py`:

```python
from dataclasses import dataclass
from datetime import date
from typing import Literal

@dataclass(frozen=True)
class TreatmentApplicationSnapshot:
    id: str
    pathogen_type: str
    treatment_name: str
    crop: str
    district: str
    applied_on: date
    final_outcome: str | None
    followups_to_resolution: int | None
    days_to_resolution: int | None
    failed_on_got_worse: bool
    escalated_for_expert: bool

@dataclass(frozen=True)
class EfficacyResult:
    treatment_id: str
    pathogen: str
    crop: str
    region: str
    status: Literal["insufficient_data", "statistically_significant"]
    sample_size: int
    min_sample_threshold: int
    efficacy_percentage: float | None
    avg_days_to_recovery: float | None

def compute_efficacy(
    *,
    treatment_name: str,
    pathogen_type: str,
    crop: str,
    district: str,
    applications: list[TreatmentApplicationSnapshot],
    as_of: date,
    window_days: int = 365,
    min_sample_threshold: int = 10,
) -> EfficacyResult:
    """Pure domain function computing real-world treatment efficacy.
    
    Invariants:
    1. Zero wall-clock reads (as_of is an injected parameter).
    2. Deterministic ordering: applications are filtered and sorted deterministically.
    3. Same inputs + same as_of date -> byte-identical EfficacyResult.
    """
```

### 5.2 Stage B Testing Contract
Stage B must include a deterministic unit test suite in `tests/unit/test_efficacy_scoring.py` with fixed fixtures asserting:
1. Exact expected percentage calculation (e.g. 8 successes out of 10 applications = `80.0%`).
2. Floor enforcement (e.g. 9 applications $\rightarrow$ `insufficient_data`, 10 applications $\rightarrow$ `statistically_significant`).
3. Correct exclusion of applications outside the trailing window (`applied_on < as_of - window_days`).
4. Proper handling of precautionary escalations versus `failed_on_got_worse` failures.

---

## 6. Next Steps & Stage B Checkpoints

1. Shruthi confirms the `TreatmentApplication` schema and generates Alembic migration.
2. Thaariha integrates the `GET /api/v1/treatments/{treatment_id}/efficacy` response contract into the KVK Agronomist Portal.
3. Implementation of `app/domain/efficacy/score.py` and `app/services/efficacy/aggregator.py`.
