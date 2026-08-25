# BHOOMI BM25 Optimization & Hyperparameter Tuning Report

**Assessment Date:** August 2026  
**Corpus Chunks Indexed:** 140 chunks  
**Vocabulary Size:** 1394 unique token & subword n-gram features  
**Optimal Parameter Selection:** $k_1 = 1.5$, $b = 0.6$  

---

## 1. Grid Search Benchmark Results

| Configuration | Recall@1 | Recall@3 | Recall@5 | MRR | Avg Latency | Index Size |
|---|---|---|---|---|---|---|
| $k_1=1.5, b=0.6$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.027 ms | 140 chunks |
| $k_1=1.5, b=0.75$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.027 ms | 140 chunks |
| $k_1=1.5, b=0.85$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.028 ms | 140 chunks |
| $k_1=1.8, b=0.6$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.026 ms | 140 chunks |
| $k_1=1.8, b=0.75$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.028 ms | 140 chunks |
| $k_1=1.8, b=0.85$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.027 ms | 140 chunks |
| $k_1=2.0, b=0.6$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.029 ms | 140 chunks |
| $k_1=2.0, b=0.75$ | 57.0% | 63.0% | 70.0% | 0.6082 | 0.027 ms | 140 chunks |
| $k_1=2.0, b=0.85$ | 57.0% | 62.0% | 70.0% | 0.6073 | 0.029 ms | 140 chunks |
| $k_1=1.2, b=0.6$ | 56.0% | 63.0% | 70.0% | 0.6015 | 0.028 ms | 140 chunks |
| $k_1=1.2, b=0.75$ | 56.0% | 63.0% | 70.0% | 0.6015 | 0.027 ms | 140 chunks |
| $k_1=1.2, b=0.85$ | 56.0% | 63.0% | 70.0% | 0.6015 | 0.027 ms | 140 chunks |

---

## 2. Tokenization & Morphological Analysis

- **Tamil Script Character 3-Grams:** Subword n-grams capture Tamil agglutinative inflectional suffixes (e.g. *-களுக்கு*, *-யால்*, *-ஆல்*, *-இல்*), preventing zero lexical match on inflected farmer utterances.
- **Latin Binomial Preservation:** Full binomial names (e.g. *Scirpophaga incertulas*, *Magnaporthe oryzae*) and acronyms (*BPH*, *GLH*, *BLB*, *BLS*) are preserved intact with case-insensitivity.
- **Formulation & Number Tokenization:** Formulations (*18.5 SC*, *25 WG*, *75 WP*, *1250 g/ha*) maintain numeric and symbol continuity.
