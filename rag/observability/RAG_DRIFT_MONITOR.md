# BHOOMI Retrieval Drift Detection & Distribution Monitor

**Objective:** Continuous detection of linguistic, agronomic, seasonal, and confidence distribution drift in production query streams.

---

## 1. Monitored Drift Dimensions & Thresholds

| Drift Dimension | Baseline Distribution | Warning Threshold | Blocking / Action Threshold | Operational Action |
|---|---|---|---|---|
| **Top-1 Retrieval Confidence** | Median: 0.88 (P25: 0.76) | Median $< 0.70$ (over 10k turns) | Median $< 0.60$ | Trigger Diagnostic Analysis & Review |
| **Direct Advisory Rate** | $88.0\% - 94.0\%$ | $< 80.0\%$ | $< 70.0\%$ | Evaluate Corpus Chunk Coverage |
| **KVK Escalation Rate** | $4.0\% - 8.0\%$ | $> 15.0\%$ | $> 25.0\%$ | Check for Emerging Pests / Pathogens |
| **Dialect Mismatch Rate** | $< 2.0\%$ | $> 5.0\%$ | $> 10.0\%$ | Update Regional Tamil Lexicon Alias |
| **Safety Interception Rate** | $2.0\% - 5.0\%$ | $> 10.0\%$ | Sudden Spike ($>25\%$) | Investigate Adversarial Probe Attack |

---

## 2. Drift Response Workflow

$$\text{Drift Alert} \rightarrow \text{Diagnostic Log Sample} \rightarrow \text{Agronomic Review} \rightarrow \text{Feature Branch Fix} \rightarrow \text{Full CI Gate} \rightarrow \text{Staged Canary}$$
