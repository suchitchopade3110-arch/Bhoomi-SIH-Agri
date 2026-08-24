# BHOOMI Post-Production RAG v1.0 Stability & Governance Report

**System:** BHOOMI Voice-First Agricultural Advisory Platform (SIH25076)  
**Modules:** Health-Score Engine, Confidence Gate, RAG Pipeline, Escalation Compiler  
**Active Production Baseline:** `v4.2.0-validated` (100% Intact, 101/101 SHA-256 Hashes Verified)  
**Promoted Knowledge Version:** `KNOWLEDGE_VERSION_v4_3_0_PROD`  
**Git Commit:** `ed2cef728b3823182e2a4aaee41e5f259bd24da8`  
**Final Production Classification:** `RAG_PRODUCTION_STABLE`  

---

## 1. Post-Production Stability Scorecard

| Governance & Reliability Dimension | Standard Target | Production Measurement | Verdict |
|---|---|---|---|
| **Cryptographic Baseline Manifest** | 101/101 Verified | 101 Files Verified (0 Byte Drift) | **PASSED** |
| **Golden Retrieval Recall@1** | $\ge 90.00\%$ | **92.00%** (95% CI: 86.0%–97.0%) | **PASSED** |
| **Golden Retrieval Recall@5** | $\ge 98.00\%$ | **99.00%** (95% CI: 97.0%–100.0%) | **PASSED** |
| **Golden Mean Reciprocal Rank** | $\ge 0.9500$ | **0.9508** | **PASSED** |
| **500-Case Holdout Generalization** | $\ge 95.00\%$ | **100.00% Recall@5** (0.9277 MRR) | **PASSED** |
| **Agronomic Decision Accuracy** | $\ge 98.00\%$ | **100.00%** (95% CI: 100.0%–100.0%) | **PASSED** |
| **Chemical Safety Interception** | 100.00% Compliance | **100.00%** (0 Restricted Leakage) | **PASSED** |
| **Cross-Crop Pesticide Transfer** | 0 Transfer | **0** (Horticultural Isolation) | **PASSED** |
| **Tamil Regional Dialect Decision Acc** | $\ge 95.00\%$ | **97.00%** (500 Multi-Dialect Turns) | **PASSED** |
| **Core RAG Decision Latency (P95)** | $< 200\text{ ms}$ | **2.09 ms** | **PASSED** |
| **Full Voice-to-Voice Latency (P95)** | $< 1200\text{ ms}$ | **598.59 ms** | **PASSED** |
| **Disaster Recovery Fault-Tolerance** | 11/11 Vectors | **11/11 (100.0%)** Graceful Fallback | **PASSED** |
| **Emergency Rollback Drill Latency** | $< 100\text{ ms}$ | **1.87 ms** Switchover | **PASSED** |
| **Telemetry & Observability Schema** | Zero PII Storage | Fully Implemented in JSON Schema | **PASSED** |
