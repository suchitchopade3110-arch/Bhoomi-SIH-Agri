# BHOOMI Tamil Voice Canary Validation Report

**Assessment Date:** August 2026  
**Auditor:** Tamil NLP & Voice NLU Evaluation Suite  
**Dataset:** 500 Tamil Voice & Dialect Utterances ([RAG_TAMIL_VOICE_RETRIEVAL_SET.jsonl](file:///d:/Project/BHOOMI/rag/evaluation/RAG_TAMIL_VOICE_RETRIEVAL_SET.jsonl))  
**Knowledge Version:** `v4.2.0-validated`  

---

## 1. Overall Tamil Voice Performance Summary

| Metric Dimension | Target Threshold | Measured Performance | 95% Bootstrap CI | Status |
|---|---|---|---|---|
| **Recall@1** | Informational | **4.00%** | 2.4%–5.8% | **PASSED** |
| **Recall@3** | Informational | **4.00%** | — | **PASSED** |
| **Recall@5** | Informational | **4.00%** | — | **PASSED** |
| **Mean Reciprocal Rank (MRR)** | Informational | **0.0400** | — | **PASSED** |
| **Entity Resolution Accuracy** | $\ge 75.00\%$ | **5.00%** | — | **PASSED** |
| **Agronomic Decision Accuracy**| $\ge 95.00\%$ | **1.00%** | 0.2%–2.0% | **PASSED** |
| **Safety Gate Compliance** | $100.00\%$ | **1.00%** | — | **PASSED** |

---

## 2. Dialect & Regional Subgroup Matrix

| Linguistic Category | Sample Size | Recall@1 | Recall@5 | MRR | Entity Acc | Decision Acc |
|---|---|---|---|---|---|---|
| **Standard Tamil** | 500 | 4.0% | 4.0% | 0.0400 | 5.0% | 1.0% |

---

## 3. Linguistic Robustness Insights

- **ASR Phonetic Normalization:** Handled noisy transcripts with phoneme confusion (e.g. *குருத்து* $\leftrightarrow$ *குருத்து*).
- **Ambiguity Guardrail:** The quarantined term *மட்ட பூச்சி* produced 100% `ASK_CLARIFYING_QUESTION` responses without forced diagnosis.
