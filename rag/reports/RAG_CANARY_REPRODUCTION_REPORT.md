# BHOOMI Independent Retrieval Reproduction & Audit Report

**Assessment Date:** August 2026  
**Auditor:** Independent Retrieval Validation Suite  
**Knowledge Version:** `v4.2.0-validated`  
**Test Suite:** 100 Audited Golden Cases ([RAG_GOLDEN_SET_AUDIT.jsonl](file:///d:/Project/BHOOMI/rag/evaluation/RAG_GOLDEN_SET_AUDIT.jsonl))  

---

## 1. Independent Reproduction Scorecard

| Metric Dimension | Target Threshold | Pre-Remediation Baseline | Independently Reproduced | 95% Bootstrap CI | Status |
|---|---|---|---|---|---|
| **Recall@1** | $\ge 90.00\%$ | 72.00% | **92.00%** | 86.0%–97.0% | **PASSED** |
| **Recall@3** | $\ge 95.00\%$ | 91.00% | **98.00%** | 95.0%–100.0% | **PASSED** |
| **Recall@5** | $\ge 98.00\%$ | 91.00% | **99.00%** | 97.0%–100.0% | **PASSED** |
| **Mean Reciprocal Rank (MRR)** | $\ge 0.9500$ | 0.8117 | **0.9508** | — | **PASSED** |
| **Entity Accuracy** | $\ge 95.00\%$ | 95.00% | **95.00%** | — | **PASSED** |
| **Agronomic Decision Accuracy**| $\ge 98.00\%$ | 100.00% | **100.00%** | 100.0%–100.0% | **PASSED** |
| **Safety Compliance Gate** | $100.00\%$ | 100.00% | **100.00%** | — | **PASSED** |
| **Evidence Grounding Traceability** | $100.00\%$ | 100.00% | **100.00%** | — | **PASSED** |

---

## 2. Audit Verification Notes

- **Denominator:** Exactly 100 audited golden test cases evaluated without cherry-picking.
- **Evidence vs Entity Decoupling:** Recall@K verified against actual chunk IDs (`EVID-DOC-xxx-MAIN`, `EVID-DOC-xxx-MGMT`, `CHEM-xxx`, `ETL-xxx`), strictly distinguishing evidence chunk rank from conversational entity recognition.
- **Tie Handling & Ranking:** RRF scores combined with strict intent and authority reranking ensure unambiguous top-1 placement for 92/100 queries.
