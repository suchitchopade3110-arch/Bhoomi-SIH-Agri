# BHOOMI SRE Operations Runbook & Operational Procedures

---

## 1. Routine Maintenance & Health Checks

- **Daily Baseline Checksum Validation:**
  ```powershell
  python -m rag.audits.verify_baseline_integrity
  ```
- **Live Latency & Health Check:**
  ```powershell
  python -m rag.scripts.run_true_e2e_latency_benchmark
  ```
- **Circuit Breaker Status Check:** Inspect `rag/deployment/RAG_CANARY_STATE.json` for `circuit_breaker_status`.

---

## 2. Emergency Escalation Contacts

- **On-Call SRE:** PagerDuty Primary Rotation (`sre-oncall@bhoomi.gov.in`)
- **Lead Safety Engineer:** `safety-officer@bhoomi.gov.in`
- **Lead Agronomist:** `icar-liaison@bhoomi.gov.in`
