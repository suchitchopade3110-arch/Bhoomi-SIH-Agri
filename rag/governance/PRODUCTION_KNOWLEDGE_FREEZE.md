# BHOOMI Production Knowledge Baseline Freeze

**Production Release:** `PRODUCTION_RAG_1.0.0`  
**Promoted Knowledge Version:** `KNOWLEDGE_VERSION_v4_3_0_PROD` (`v4.3.0-production-promoted`)  
**Active Production Baseline:** `v4.2.0-validated` (101/101 Files Verified SHA-256)  
**Historical Rollback Baseline:** `v4.1.0-validated` (Operational Standby)  
**Commit:** `ed2cef728b3823182e2a4aaee41e5f259bd24da8`  
**Immutability Status:** `LOCKED_READ_ONLY`  

---

## 1. Immutable Baseline Invariants

1. **Explicit Version Promotion:** The certified knowledge artifact has completed 100% canary validation and is officially locked as `KNOWLEDGE_VERSION_v4_3_0_PROD`.
2. **Byte-Level Protection:** Any modification to `data/curated/Dataset_v4_validated/` or `Dataset_v4_1_validated/` will immediately trigger `CANARY_BLOCKED_BASELINE_INTEGRITY` in CI.
3. **Decoupled Safety Gate:** Deterministic chemical safety and CIBRC policies are cryptographically hashed and cannot be altered by retrieval index rebuilds.
