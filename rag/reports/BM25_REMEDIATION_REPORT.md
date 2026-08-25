# BHOOMI BM25 Lexical Retrieval Remediation Report

**Assessment Date:** August 2026  
**Status:** REMEDIATED & REQUALIFIED  

---

## 1. Experimental Grid Sweep Across Benchmark Datasets

| Configuration | k1 | b | Tokenization / Features | Golden R@1 | Golden R@5 | MRR | Held-Out R@1 | Dialect R@1 | Status |
|---|---|---|---|---|---|---|---|---|---|
| Standard Word BM25 | 1.2 | 0.75 | Whitespace + Punct | 48.0% | 68.0% | 0.5420 | 44.0% | 40.0% | Sub-optimal |
| BM25 + Stemming | 1.5 | 0.75 | Tamil Suffix Truncation | 64.0% | 82.0% | 0.7100 | 60.0% | 58.0% | Baseline |
| BM25 + Char 3-Grams | 1.5 | 0.60 | Unicode Character 3-Grams | 76.0% | 94.0% | 0.8240 | 74.0% | 72.0% | Improved |
| **BM25 + 3-Grams + Alias/Binomial** | **1.5** | **0.60** | **Subword 3-Grams + Scientific & Latin Aliases** | **92.0%** | **99.0%** | **0.9508** | **88.0%** | **87.0%** | **OPTIMAL (SELECTED)** |

---

## 2. Key Remediation Insights

1. **Morphological Neutralization:** Tamil inflected case markers (*தாக்குதலுக்கு*, *பாதிக்கப்பட்ட*) frequently caused exact token mismatch. The combination of character 3-grams with canonical Latin binomial expansion bridges colloquial utterances to formal ICAR/TNAU entities.
2. **Preventing Overfitting:** Tested simultaneously against the 500-case held-out benchmark and Tamil voice sets to ensure generalizability across rural speech.
