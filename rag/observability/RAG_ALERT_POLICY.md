# BHOOMI SRE Alerting & Severity Policy

**Authority:** Lead Reliability Engineer, Safety Officer  

---

## 1. Incident Severity Definitions & Escalation Matrix

| Severity | Definition | Alert Channel | Response Time | Action Required |
|---|---|---|---|---|
| **SEV-0** | Critical safety breach (restricted chemical leakage, cross-crop transfer) | PagerDuty, SMS, Slack #war-room | **$< 5\text{ minutes}$** | Instant automatic circuit breaker $\rightarrow$ Rollback to `v4.2.0-validated` |
| **SEV-1** | Major agronomic decision regression or system crash | PagerDuty, Slack #prod-alerts | **$< 15\text{ minutes}$** | Freeze traffic expansion, initiate SRE investigation |
| **SEV-2** | Retrieval quality degradation (R@1 $< 85\%$) or latency spike (P95 $> 200\text{ ms}$) | Slack #rag-alerts, Email | **$< 1\text{ hour}$** | Analyze telemetry logs, prepare hotfix branch |
| **SEV-3** | Minor telemetry drift or non-blocking component degradation | Slack #rag-monitoring | **$< 4\text{ hours}$** | Triage during regular on-call cycle |
| **SEV-4** | Cosmetic/observability log format inconsistency | Jira Backlog | **$< 24\text{ hours}$** | Address in next standard sprint |
