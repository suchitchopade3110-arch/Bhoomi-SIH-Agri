# Specification: Treatment Efficacy & Outcome Tracking Engine (SIH26131)

> **Document ID:** SPEC-EFFICACY-001  
> **Status:** Stage A Spec (Pending Team Review & Shruthi Schema Confirmation)  
> **Author:** Shreekumar (Backend Intelligence)  
> **Target Release:** SIH26131 Realignment  
> **Stakeholders:** Thaariha (Agronomist Portal & Program Analytics), Shruthi (Database & ORM)

---

## 1. Context & Purpose

Bhoomi captures closed-loop follow-up check-ins (`improved`, `no_change`, `got_worse`). In SIH26131, we aggregate these localized outcomes across thousands of smallholders to measure **real-world treatment efficacy**.

This data directly feeds:
1. **Thaariha's Program-Level Agronomist Dashboard**: Providing regional KVKs with evidence-based data on which chemical/biological interventions are working versus failing against specific pathogens.
2. **Dynamic Advisory Re-Ranking**: Down-ranking treatments that exhibit declining efficacy in a given district due to antimicrobial or pesticide resistance.

---

## 2. Definition of Efficacy

**Treatment Efficacy** is defined as the population-level success rate of a specific `(pathogen_type, treatment_input)` combination across all recorded farm applications within a given crop and regional context.

Success is determined purely from the farmer's closed-loop follow-up trajectory:
- **Success (Positive Outcome)**: A treatment application that leads to an `improved` or `resolved` status within $\le 2$ consecutive check-in cycles without requiring emergency expert escalation.
- **Failure (Negative Outcome)**: An application that results in `got_worse` (triggering escalation) or remains `no_change` across $> 2$ consecutive follow-ups.

---

## 3. Data Model & Schema Recommendation for Shruthi

> [!IMPORTANT]
> **Schema Recommendation for Shruthi (Database Owner):**  
> We strongly recommend creating a dedicated `treatment_applications` table rather than adding treatment columns to `followups` or `problems`.

### 3.1 Rationale
1. **Cardinality**: A single `Problem` may undergo multiple sequential treatments (e.g., cultural draining $\rightarrow$ foliar bactericide spray). Overloading `problems` assumes 1 treatment per problem; overloading `followups` conflates observation check-ins with treatment applications.
2. **Analytical Indexing**: An isolated entity allows high-throughput aggregation queries filtered by `(treatment_id, region, crop, season)` without table scans across chat/voice logs.

### 3.2 Proposed Schema Structure (`app/models/treatment_application.py`)

```python
class TreatmentApplication(Base):
    __tablename__ = "treatment_applications"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_id: Mapped[str] = mapped_column(String, ForeignKey("problems.id"), nullable=False, index=True)
    farm_id: Mapped[str] = mapped_column(String, ForeignKey("farms.id"), nullable=False, index=True)
    
    # Controlled vocabulary from ICAR Package of Practices corpus
    pathogen_type: Mapped[str] = mapped_column(String, nullable=False, index=True)  # e.g., "bacterial_leaf_blight"
    treatment_name: Mapped[str] = mapped_column(String, nullable=False, index=True)  # e.g., "copper_hydroxide_77_wp"
    treatment_category: Mapped[str] = mapped_column(String, nullable=False)  # "chemical", "biological", "cultural"
    
    applied_on: Mapped[date] = mapped_column(Date, nullable=False)
    crop: Mapped[str] = mapped_column(String, nullable=False)
    district: Mapped[str] = mapped_column(String, nullable=False, index=True)
    
    # Final outcome resolved from FollowUp stream
    final_outcome: Mapped[str | None] = mapped_column(String, nullable=True)  # "resolved", "improved", "failed"
    followups_to_resolution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    days_to_resolution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
```

---

## 4. Efficacy Scoring Formula & Sample-Size Guard

### 4.1 Scoring Formula
Let $N_{\text{total}}$ be the total number of evaluated applications for a `(pathogen, treatment)` pair in the target filter scope.
Let $N_{\text{success}}$ be the count of applications where `final_outcome IN ('resolved', 'improved')` AND `escalated == False` AND `followups_to_resolution <= 2`.

$$\text{Efficacy Score (\%)} = \left( \frac{N_{\text{success}}}{N_{\text{total}}} \right) \times 100$$

### 4.2 Minimum Sample-Size Floor ($N \ge 10$)
- **Floor Rule**: To prevent misleading claims (e.g., $1/1 = 100\%$ efficacy), any aggregation with $N_{\text{total}} < 10$ returns `status: "insufficient_data"`.
- **Response Contract**:

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

When $N_{\text{total}} \ge 10$:

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

## 5. Next Steps & Stage B Checkpoints

1. Shruthi confirms the `TreatmentApplication` schema and generates Alembic migration.
2. Thaariha reviews response contract for the KVK analytics frontend.
3. Implementation of `app/services/efficacy/aggregator.py` with pure, deterministic unit tests.
