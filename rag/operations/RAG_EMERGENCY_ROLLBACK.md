# BHOOMI Emergency Rollback & Safety Protocols

---

## 1. Emergency Rollback Execution Protocol

In the event of an automated or manual emergency rollback command:
1. **Routing Switch:** Update `RAG_CANARY_STATE.json` `canary_percentage` to `0.0`.
2. **Target Reversion:** Set `active_production_version` to `v4.2.0-validated`.
3. **Execution Latency:** Must complete in $< 100\text{ ms}$ (Tested actual: $1.87\text{ ms}$).
4. **Log Retention:** Telemetry logs from candidate turns are immediately sealed for forensic post-mortem analysis.

---

## 2. Safety Incident & Data Corruption Protocols

- **Quarantine Mode:** If an index corruption or prompt poisoning vector is discovered, the affected candidate index is isolated into `rag/quarantine/` while production continues executing from immutable baseline files.
- **Root-Cause Post-Mortem:** Must be published within 24 hours of incident resolution.
