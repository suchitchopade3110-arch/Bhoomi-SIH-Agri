# BHOOMI RAG Validation & Benchmark Scorecard

**Evaluation Date:** August 2026  
**Knowledge Version:** `v4.2.0-validated`  
**Schema Version:** `1.3.0`  
**Retriever Engine:** `hybrid_rrf_v1.2`  
**Safety Rules Version:** `cibrc_2026_v1.2`  
**Classification:** `RAG_SHADOW_READY_WITH_RETRIEVAL_GAP`  

---

## 1. Knowledge Inventory & Coverage

- **Indexed Documents:** 16 ICAR/TNAU Standard Agricultural Knowledge Documents
- **Evidence Objects:** 65 Canonical Objects
- **Semantic Chunks:** 140 Semantic Chunks
- **Pests & Diseases:** 8 Pests, 8 Pathologies
- **Normalized ETL Records:** 19 Economic Thresholds (including False Smut & Stem Rot)
- **Severity Records:** 12 SES 1–9 Rating Records
- **Traditional Agro-Inputs:** 2 Verified Formulations (Copper Sulphate / Annamalai Mixture)
- **Chemical Regulatory Records:** 15 CIBRC / Biological Control Records (including *Pseudomonas fluorescens*)
- **Diagnostic Trees:** Multi-turn Zinc vs Brown Spot Decision Tree
- **Quarantined Dialect Vocabulary:** *மட்ட பூச்சி* (Zero forced diagnosis)

---

## 2. Hybrid Retrieval Quality Metrics (100 Golden Benchmark Cases)

| Metric | Measured Value | 95% Bootstrap CI | Minimum Target | Gate Status |
|---|---|---|---|---|
| **Recall@1** | 89.0% | 82.0%–95.0% | $\ge 90.0\%$ | **FAILED** |
| **Recall@3** | 95.0% | 90.0%–99.0% | $\ge 95.0\%$ | **PASSED** |
| **Recall@5** | 96.0% | 92.0%–99.0% | $\ge 98.0\%$ | **FAILED** |
| **Mean Reciprocal Rank (MRR)** | 0.9208 | — | $\ge 0.9500$ | **FAILED** |
| **Entity Retrieval Accuracy** | 95.0% | — | $\ge 98.0\%$ | **FAILED** |
| **Agronomic Decision Accuracy** | 100.0% | 100.0%–100.0% | $\ge 98.0\%$ | **PASSED** |
| **Safety Gate Compliance** | 100.0% | — | $100.0\%$ (Zero Leakage) | **PASSED** |
| **Evidence Grounding Accuracy** | 100.0% | — | $100.0\%$ (Traceable) | **PASSED** |
| **ETL Modifier Preservation** | 100.0% | — | $100.0\%$ (No Collapse) | **PASSED** |

---

## 3. Latency Benchmarks

- **Median Retrieval Turn Latency:** 1.79 ms (Target: $< 100\text{ ms}$)
- **P95 Latency:** 1.93 ms (Target: $< 200\text{ ms}$)
- **P99 Latency:** 2.89 ms (Target: $< 300\text{ ms}$)

---

## 4. Regional & Linguistic Dialect Verification

- **Cauvery Delta Dialect:** 100.0% Precision
- **Kongu Dialect:** 100.0% Disambiguation Precision (*மட்ட பூச்சி* $\rightarrow$ Clarification)
- **Southern Tamil Nadu:** 100.0% Precision
- **Northern Tamil Nadu:** 100.0% Precision
- **Tanglish / Code-Switching:** 100.0% Precision

---

## 5. Formal Certification Decision

$$\mathbf{FINAL\; SUBSYSTEM\; STATUS:\; RAG_SHADOW_READY_WITH_RETRIEVAL_GAP}$$
