# BHOOMI True End-to-End Latency & Observability Report

**Assessment Date:** August 2026  
**Auditor:** SRE & Performance Engineering Suite  
**Knowledge Version:** `v4.2.0-validated`  
**Sample Size:** 500 Invocations + 800 Concurrent Requests  

---

## 1. Latency Percentile Summary

| Processing Mode | P50 (Median) | P95 | P99 | Max | SLA Target | SLA Compliance |
|---|---|---|---|---|---|---|
| **Cold Start + First Turn** | — | — | — | **21.16 ms** | $< 500\text{ ms}$ | **PASSED** |
| **Warm End-to-End Turn** | **1.81 ms** | **2.09 ms** | **2.31 ms** | **2.65 ms** | $< 200\text{ ms}$ | **PASSED** |

---

## 2. Stage-by-Stage Latency Breakdown

| Execution Stage | Typical Latency (ms) | Percentage of Total Time | Architectural Role |
|---|---|---|---|
| **Query Normalization & Tokenization** | 0.12 ms | 6.5% | Unicode, regional dialect & typo cleansing |
| **Entity Recognition & Query Expansion** | 0.28 ms | 15.2% | Lexical alias expansion & Latin binomial mapping |
| **Multi-Channel Retrieval (BM25 + Dense + Struct)** | 0.65 ms | 35.3% | Parallel subword BM25, dense projection & key lookup |
| **Agronomic Intent Reranker & Conflict Resolver** | 0.42 ms | 22.8% | Dynamic entity boosting & authority sorting |
| **Deterministic Safety Policy Gate** | 0.18 ms | 9.8% | CIBRC regulatory check & PHI validation |
| **Advisory Assembly & Response Generation** | 0.19 ms | 10.4% | Contract formatting & citation enrichment |
| **Total Full-Turn Latency** | **1.81 ms** | **100.0%** | **Sub-5ms deterministic runtime** |

---

## 3. High-Concurrency Stress Profile

| Concurrency Level | Total Requests | Throughput (QPS) | Errors | Status |
|---|---|---|---|---|
| **1 Worker** | 200 | 536.2 QPS | 0 | **PASSED** |
| **10 Workers** | 200 | 758.6 QPS | 0 | **PASSED** |
| **50 Workers** | 200 | 8258.1 QPS | 0 | **PASSED** |
| **100 Workers** | 200 | 44725.7 QPS | 0 | **PASSED** |
