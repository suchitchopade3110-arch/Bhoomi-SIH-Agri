# BHOOMI RAG Evaluation Integrity & Metric Investigation Report

**Document:** `RAG_EVALUATION_INTEGRITY_REPORT.md`  
**Investigation Date:** August 2026  
**Audited Harness:** `rag/evaluation/evaluate_rag.py`  
**Reported Anomaly:** `Recall@1 = 94.0%`, `Recall@3 = 94.0%`, `Recall@5 = 94.0%` marked as `PASSED` against targets ($\ge 90\%, \ge 95\%, \ge 98\%$).  
**Investigator:** Lead RAG Architect & Evaluation Engineer  

---

## 1. Investigation Summary & Root Cause Analysis

A critical evaluation reporting inconsistency was identified in `rag/reports/RAG_INITIAL_VALIDATION_REPORT.md`:
- **Reported Metrics**: Recall@1 = 94.0%, Recall@3 = 94.0%, Recall@5 = 94.0%
- **Declared Targets**: Recall@1 $\ge 90.0\%$, Recall@3 $\ge 95.0\%$, Recall@5 $\ge 98.0\%$
- **Report Status**: Hardcoded **PASSED** across all three metrics.

### Five Investigative Dimensions Analyzed:
1. **Metric Implementation (Flawed)**: In `evaluate_rag.py` (lines 81–99), the condition `if rank == 1 or matched_ent_id == exp_ent_id:` checked whether the Python dictionary lookup in `QueryExpander` identified the entity ID. If matched, it credited the query to `recall_at_1`, `recall_at_3`, and `recall_at_5` simultaneously, even when top-K chunk retrieval returned unrelated or sub-optimal passages.
2. **Benchmark Ground Truth (Mixed)**: Safety rejection cases (20 cases in Golden Set) were lumped into top-1 retrieval recall calculations rather than evaluated on dedicated safety gate metrics.
3. **Target Thresholds (Valid)**: The targets ($\text{Recall@1} \ge 90\%$, $\text{Recall@3} \ge 95\%$, $\text{Recall@5} \ge 98\%$, $\text{MRR} \ge 0.95$) reflect real agronomic safety requirements and MUST NOT be manipulated.
4. **Report Status Calculation (Bug)**: The markdown generator in `evaluate_rag.py` hardcoded the string `"**PASSED**"` in the markdown table rather than dynamically computing `is_passed = (value >= target)`.
5. **Measured Behavior (Genuine Retrieval Gap)**: For specific queries (e.g. traditional inputs like *மயில் துத்தம்*, *அண்ணாமலை கலவை*, *Pseudomonas fluorescens* seed treatment, and *Stem Rot* management), evidence chunk retrieval ranks were $> 3$ or missed due to metadata and index indexing gaps.

---

## 2. Formal Metric Definitions & Ground Truth

### A. Document Retrieval vs Evidence Retrieval vs Grounding

$$\text{Recall@K} = \frac{\sum_{i=1}^{N} \mathbb{I}(\text{Top-}K \text{ retrieved evidence chunks contain the golden supporting evidence ID})}{N_{\text{advisory queries}}}$$

$$\text{MRR} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{\text{rank}_i}$$

$$\text{Evidence Precision@K} = \frac{|\text{Retrieved Chunks in Top-}K \cap \text{Golden Evidence Chunks}|}{K}$$

$$\text{Evidence Grounding Accuracy} = \frac{\sum_{i=1}^{N} \mathbb{I}(\text{Actionable claim is 100\% supported by cited evidence object})}{N_{\text{actionable decisions}}}$$

### B. Denominators and Relevance Criteria
- **Advisory Retrieval Evaluation**: Evaluated over all actionable advisory queries ($N = 80$). Queries whose ground truth is `ASK_CLARIFYING_QUESTION`, `REJECT_CROP_MISMATCH`, or `SAFETY_INTERVENTION_WARNING` without a required evidence chunk are evaluated under **Decision & Safety Gate Compliance** ($N = 20$).
- **Relevance Criterion**: Top-$K$ must contain the specific canonical `evidence_id` or `chunk_id` supporting the exact agronomic claim (dosage, active ingredient, threshold, or diagnostic decision tree node).

---

## 3. Measured Baseline vs Target Comparison

| Metric | Target Gate | Pre-Audit Reported | Actual Measured (Pre-Fix) | Correct Status |
|---|---|---|---|---|
| **Recall@1** | $\ge 90.0\%$ | 94.0% | 88.75% (71/80) | **FAIL (Below Target)** |
| **Recall@3** | $\ge 95.0\%$ | 94.0% | 91.25% (73/80) | **FAIL (Below Target)** |
| **Recall@5** | $\ge 98.0\%$ | 94.0% | 93.75% (75/80) | **FAIL (Below Target)** |
| **MRR** | $\ge 0.9500$ | 0.9400 | 0.8990 | **FAIL (Below Target)** |
| **Entity Retrieval Accuracy** | $\ge 98.0\%$ | 100.0% | 100.0% | **PASSED** |
| **Agronomic Decision Accuracy** | $\ge 98.0\%$ | 100.0% | 100.0% | **PASSED** |
| **Safety Gate Compliance** | $100.0\%$ (Zero Leakage) | 100.0% | 100.0% | **PASSED** |
| **Evidence Grounding Accuracy** | $100.0\%$ | Not measured | 92.50% | **FAIL (Below Target)** |

---

## 4. Current Subsystem Classification

Because the measured top-K evidence retrieval recall and grounding accuracy are genuinely below target while safety compliance remains 100%, the RAG subsystem is formally classified as:

$$\mathbf{RAG\_SHADOW\_READY\_WITH\_RETRIEVAL\_GAP}$$

*(It is strictly NOT production ready or canary ready until retrieval hardening is executed and verified).*

---

## 5. Remediation Plan

1. **Decouple Metric Code**: In `evaluate_rag.py`, compute genuine evidence chunk top-K retrieval recall strictly from `evidence_ids` against `expected_evidence_id` / `expected_doc_id`.
2. **Dynamic Pass/Fail Logic**: Compute pass status dynamically: `status = "PASSED" if val >= target else "FAILED"`.
3. **Harden Hybrid Indexing**:
   - Ingest traditional inputs (*மயில் துத்தம்*, *அண்ணாமலை கலவை*) as dedicated canonical evidence objects.
   - Ingest bio-control inputs (*Pseudomonas fluorescens*) with all application methods (seed treatment, foliar, soil application).
   - Improve BM25 token weighting and dense vector representations for disease queries (*Stem Rot*, *Sheath Rot*, *BLS*).
   - Add Source Conflict Resolver and Independent Safety Engine.
4. **Statistical Confidence Intervals**: Calculate 95% bootstrap confidence intervals for all metrics.
