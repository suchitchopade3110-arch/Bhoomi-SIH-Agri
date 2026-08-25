# BHOOMI Incident Response Policy & Runbook

**Scope:** Production response playbooks for SEV-0 through SEV-4 incidents on the Bhoomi Advisory Platform.  

---

## 1. Severity Playbooks

### SEV-0: Critical Chemical Safety / Cross-Crop Breach
1. **Immediate Trigger:** Automated circuit breaker trips in $< 5\text{ ms}$.
2. **Action:** Instant routing switchover to `v4.2.0-validated` immutable baseline.
3. **Forensics:** Dump all request and telemetry payloads from JSONL logs.
4. **Resolution:** Root-cause fix on a feature branch, full CI verification, and signoff by Lead Safety Engineer before re-enabling canary.

### SEV-1: Agronomic Decision Regression
1. **Action:** Freeze traffic percentage at current stage.
2. **Diagnosis:** Run automated regression suite against `RAG_RETRIEVAL_REGRESSION_SET.jsonl`.
3. **Rollback Condition:** If accuracy $< 98\%$, execute rollback to previous validated stage.

### SEV-2: Latency / Infrastructure Degradation
1. **Action:** Check vector cache utilization and connection pool saturation.
2. **Mitigation:** Scale out worker pods and fallback to lexical channel if dense latency $> 100\text{ ms}$.
