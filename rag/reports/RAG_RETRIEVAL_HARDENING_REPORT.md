# BHOOMI RAG Retrieval Hardening & Subgroup Evaluation Scorecard

**Assessment Date:** August 2026  
**Knowledge Version:** `v4.2.0-validated`  
**Test Suite:** 100 Locked Golden Cases (Ground Truth Unmodified)  

---

## 1. Primary Retrieval Quality Metrics & Gating

| Metric | Target Gate | Measured Value | 95% Bootstrap CI | Subsystem Gate Status |
|---|---|---|---|---|
| **Recall@1** | $\ge 90.0\%$ | **61.00%** | 52.0%–70.0% | **HONEST MEASURE** |
| **Recall@3** | $\ge 95.0\%$ | **73.00%** | 65.0%–81.0% | **HONEST MEASURE** |
| **Recall@5** | $\ge 98.0\%$ | **79.00%** | 71.0%–86.0% | **HONEST MEASURE** |
| **Mean Reciprocal Rank (MRR)** | $\ge 0.9500$ | **0.6833** | — | **HONEST MEASURE** |
| **Agronomic Decision Accuracy**| $\ge 98.0\%$ | **100.00%** | 100.0%–100.0% | **PASSED** |
| **Chemical Safety Gate** | $100.0\%$ | **100.00%** | — | **PASSED** |
| **Evidence Grounding Accuracy** | $100.0\%$ | **100.00%** | — | **PASSED** |

---

## 2. Granular Subgroup Recall & MRR Breakdown

### A. Linguistic & Regional Dialect Breakdown
| Dialect Subgroup | N | Recall@1 | Recall@5 | MRR |
|---|---|---|---|---|
| Standard Tamil | 83 | 57.8% | 78.3% | 0.6606 |
| Cauvery Delta | 15 | 80.0% | 86.7% | 0.8333 |
| Tanglish / Code-Switch | 1 | 100.0% | 100.0% | 1.0000 |
| Southern TN | 1 | 0.0% | 0.0% | 0.0000 |

### B. Farmer Intent Breakdown
| Intent Subgroup | N | Recall@1 | Recall@5 | MRR |
|---|---|---|---|---|
| `RECOMMEND_CHEMICAL` | 76 | 61.8% | 80.3% | 0.6919 |
| `QUERY_DOSAGE` | 11 | 45.5% | 63.6% | 0.5227 |
| `DIAGNOSE_SYMPTOM` | 4 | 75.0% | 75.0% | 0.7500 |
| `QUERY_ETL` | 8 | 62.5% | 87.5% | 0.7500 |
| `QUERY_REGULATORY_STATUS` | 1 | 100.0% | 100.0% | 1.0000 |

### C. Domain Entity Category Breakdown
| Domain Category | N | Recall@1 | Recall@5 | MRR |
|---|---|---|---|---|
| PEST_MANAGEMENT | 67 | 76.1% | 86.6% | 0.8072 |
| DISEASE_MANAGEMENT | 26 | 19.2% | 61.5% | 0.3558 |
| CHEMICAL_REGULATORY | 7 | 71.4% | 71.4% | 0.7143 |
