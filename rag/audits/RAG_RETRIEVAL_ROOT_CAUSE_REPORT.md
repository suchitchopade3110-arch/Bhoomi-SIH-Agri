# BHOOMI RAG Retrieval Root-Cause Forensic Report

**Assessment Date:** August 2026  
**Active Production Baseline:** `v4.2.0-validated` (Strict Read-Only)  
**Total Sub-optimal Queries Analyzed:** 39 cases (Rank > 1 or unranked in Top-5)  

---

## 1. Failure Category Taxonomy Breakdown

| Code | Failure Category | Count | Percentage | Primary Root Cause Summary |
|---|---|---|---|---|
| **A** | Query Parsing Failure | 0 | 0.0% | Misparsed intent or crop entity |
| **B** | Tamil Normalization Failure | 0 | 0.0% | Unicode diacritic or punctuation normalization |
| **C** | Alias Expansion Failure | 0 | 0.0% | Dialect slang term missing from verified synonyms |
| **D** | Tokenization Failure | 8 | 20.5% | Tamil inflectional suffixes preventing root match |
| **E** | BM25 Lexical Failure | 0 | 0.0% | Term frequency diluted across large chunks |
| **F** | Dense Retrieval Failure | 0 | 0.0% | Projection hash collision across unrelated symptoms |
| **G** | Structured Retrieval Failure | 0 | 0.0% | Missing lookup key in structured index |
| **H** | RRF Fusion Failure | 0 | 0.0% | Channel weighting bias suppressing relevant chunks |
| **I** | Reranker Scoring Failure | 15 | 38.5% | Authority tier overriding intent-matched chunks |
| **J** | Chunking / Context Fragmentation | 2 | 5.1% | ETL thresholds fragmented from crop stage context |
| **N** | Multi-Document Evidence Overlap | 1 | 2.6% | Chemical chunk vs parent document ranking collision |
| **P** | Other / Residual Rank Gaps | 13 | 33.3% | General rank order variance |

---

## 2. Granular Query-by-Query Failure Matrix

| Query ID | Expected ID | Actual Top 1 | BM25 | Dense | Struct | Final Rank | Code | Root Cause & Proposed Fix |
|---|---|---|---|---|---|---|---|---|
| `GOLDEN-005` | `DOC-PEST-002` | `CHEM-001` | 1 | None | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-006` | `DOC-PEST-003` | `CHEM-007` | 1 | 1 | None | **2** | **N** | Multi-document evidence: Chemical chunk ranked #1, parent document ranked #2 $\rightarrow$ *Unified semantic evidence chunk bundling active ingredient with parent document* |
| `GOLDEN-013` | `DOC-PEST-006` | `LEX-PEST-008` | 1 | None | 1 | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-021` | `DOC-DIS-001` | `CHEM-009` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-022` | `DOC-DIS-001` | `CHEM-015` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-023` | `DOC-DIS-002` | `CHEM-008` | 3 | 1 | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-024` | `DOC-DIS-002` | `CHEM-008` | 4 | 1 | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-025` | `DOC-DIS-003` | `CHEM-015` | 7 | 1 | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-026` | `DOC-DIS-003` | `CHEM-010` | 2 | 3 | 2 | **4** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-027` | `DOC-DIS-004` | `SEV-DIS-001` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-028` | `DOC-DIS-005` | `ETL-018` | 4 | 1 | 1 | **4** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-029` | `DOC-DIS-005` | `ETL-018` | 4 | 1 | 1 | **4** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-030` | `DOC-DIS-006` | `ETL-019` | 4 | 1 | 1 | **4** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-031` | `DOC-DIS-006` | `CHEM-013` | 3 | 1 | 1 | **4** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-032` | `DOC-DIS-007` | `CHEM-015` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-033` | `DOC-DIS-008` | `CHEM-003` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-034` | `DOC-DIS-009` | `CHEM-007` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-035` | `DOC-DIS-002` | `CHEM-012` | None | None | 1 | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-038` | `DOC-DIS-002` | `CHEM-001` | None | None | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-040` | `DOC-DIS-004` | `CHEM-010` | None | None | None | **None** | **D** | Tamil compound inflection / case-marker tokenization mismatch $\rightarrow$ *Tamil Unicode subword n-gram and root stemming* |
| `GOLDEN-041` | `ETL-001` | `LEX-PEST-005` | 1 | 7 | None | **2** | **J** | ETL chunk fragmented separately from crop stage modifier $\rightarrow$ *Semantic evidence unit linking ETL threshold with stage/predator context* |
| `GOLDEN-042` | `ETL-004` | `CHEM-015` | 1 | None | 1 | **4** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-043` | `ETL-004` | `ETL-003` | 1 | 5 | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-046` | `ETL-008` | `CHEM-015` | 1 | 2 | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-052` | `ETL-015` | `AGRO-INPUT-COPPER-SULPHATE` | 4 | None | 1 | **None** | **J** | ETL chunk fragmented separately from crop stage modifier $\rightarrow$ *Semantic evidence unit linking ETL threshold with stage/predator context* |
| `GOLDEN-053` | `ETL-004` | `CHEM-003` | 1 | 6 | 1 | **3** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-054` | `SEV-DIS-003` | `CHEM-015` | None | 1 | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-055` | `SEV-DIS-002` | `AGRO-INPUT-COPPER-SULPHATE` | None | None | 1 | **2** | **I** | Reranker downweighted structured chemical match vs general bulletin $\rightarrow$ *Intent-matched chunk boosting in reranker* |
| `GOLDEN-065` | `PEST-002` | `SEV-PEST-005` | 3 | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-071` | `DIS-002` | `CHEM-008` | None | None | 2 | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-078` | `CHEM-015` | `CHEM-008` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-079` | `CHEM-015` | `LEX-PEST-005` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-080` | `DIS-007` | `CHEM-003` | None | None | 1 | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-088` | `` | `AGRO-NUTRITION-IRON-CHLOROSIS` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-089` | `` | `CHEM-001` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-092` | `` | `CHEM-015` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-097` | `` | `CHEM-001` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-098` | `` | `CHEM-004` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |
| `GOLDEN-099` | `` | `CHEM-002` | None | None | None | **None** | **P** | General rank gap $\rightarrow$ *Hierarchical evidence unit linking* |

---

## 3. Core Architectural Remedies

1. **Semantic Evidence Units (`semantic_chunker.py`):** Re-architect chunking so every chunk is a self-contained *Semantic Evidence Unit* containing parent document metadata, pest/disease identity, Latin binomials, active ingredients, dosages, PHI, and ETL modifiers.
2. **Hierarchical Document-Chunk Linking:** Ensure that when a specific chemical or ETL chunk is retrieved, its parent authoritative document chunk (`DOC-PEST-xxx` / `DOC-DIS-xxx`) is co-indexed and linked.
3. **Subword & Morphological Stemming:** Augment BM25 with root lemmatization and character 3-grams to neutralize inflectional case endings without altering semantic precision.
4. **Intent-Conditioned Reranker:** Weight chemical chunks for `QUERY_DOSAGE` intents and document overview chunks for `DIAGNOSE_SYMPTOM` intents.
