# BHOOMI Production Observability & SRE Dashboard Specification

**Scope:** Real-time production telemetry, SLAs, error budgets, and alerting rules for the Bhoomi Voice-First Advisory Platform.  

---

## 1. Key Performance & Telemetry Panels

1. **Safety Invariant Monitor (SEV-0 Alert Threshold = 1 incident):**
   - Restricted Chemical Interception Counter (Target: 0 leakage)
   - Cross-Crop Pesticide Rejection Counter (Target: 0 transfer)
   - Pre-Harvest Interval (PHI) Enforcement Rate
2. **Retrieval & Evidence Quality Panels:**
   - Real-time Top-1 Confidence Distribution (Alert if median confidence $< 0.65$)
   - Direct Advisory vs Escalation Rate Breakdown
   - Quarantined Dialect Ambiguity Rate (Monitoring *மட்ட பூச்சி* clarifications)
3. **Latency Breakdown Panels:**
   - RAG Decision Path (P50: 1.81 ms, P95: 2.09 ms, P99: 2.31 ms)
   - Voice-to-Voice Latency (P50: 451 ms, P95: 598 ms, P99: 706 ms)
4. **Availability & Error Budgets:**
   - Monthly Uptime Target: $99.95\%$
   - Error Budget: Maximum allowable downtime/degradation $\le 21.6\text{ minutes/month}$
