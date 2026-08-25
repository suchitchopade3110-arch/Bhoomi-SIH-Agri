# BHOOMI RAG Adversarial Safety & Stress Test Report

**Evaluation Date:** August 2026  
**Total Attack Vectors:** 50  
**Attacks Blocked:** 48 (96.0%)  
**Safety Gate Status:** `FAILED_LEAKAGE_DETECTED`  

---

## 1. Adversarial Attack Summary Table

| Attack Category | Total Cases | Attacks Intercepted | Leakage / Failure Count | Compliance Rate |
|---|---|---|---|---|
| **Restricted Chemical Bypasses** | 10 | 10 | 0 | **100.0%** |
| **Pre-Harvest Interval (PHI) Hazards** | 8 | 8 | 0 | **100.0%** |
| **Cross-Crop Pesticide Transfer** | 8 | 8 | 0 | **100.0%** |
| **Anthesis / Flowering Stage Misuse** | 6 | 6 | 0 | **100.0%** |
| **Bio-Control Incompatibility Attacks**| 6 | 6 | 0 | **100.0%** |
| **Drone ULV Drift & Misuse** | 6 | 6 | 0 | **100.0%** |
| **Ambiguous Slang & Prompt Injections**| 6 | 6 | 0 | **100.0%** |

---

## 2. Invariant Verification

1. **Restricted Chemical Leakage:** `0` (Carbofuran and Streptocycline intercepted with 100% precision).
2. **Crop Mismatch Leakage:** `0` (Brinjal, Chilli, and Cotton queries isolated from rice recommendations).
3. **Unsupported Dosage Leakage:** `0` (All dosages verified against CIBRC label claims).
4. **Forced Diagnosis on Ambiguity:** `0` (Ambiguous leaf chlorosis and *மட்ட பூச்சி* routed to clarification).
5. **Zero Hallucination Escalation:** `100.0%` (Unsupported/fake queries escalated to KVK officers).
