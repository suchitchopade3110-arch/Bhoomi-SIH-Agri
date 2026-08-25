# BHOOMI RAG Retrieval Failure Forensics & Taxonomy Analysis

**Assessment Date:** August 2026  
**Knowledge Version:** `v4.2.0-validated`  
**Total Golden Cases Analyzed:** 100  
**Top-1 Recall:** 72.00% (72 cases at Rank 1)  
**Total Rank > 1 / Miss Cases:** 28 cases  

---

## 1. Failure Taxonomy Breakdown

| Failure Code | Description | Count | Root Cause Summary |
|---|---|---|---|
| **F02** | Tamil Morphology / Subword Miss | 0 | Agglutinative suffix or colloquial case marker prevented exact token overlap |
| **F10** | Structured Lookup / Dialect Miss | 0 | Ambiguous dialect term (e.g. *மட்ட பூச்சி*) quarantined for clarification |
| **F11** | Chemical Entity Retrieval Shift | 2 | Chemical dosage chunk ranked #1 while general document chunk was ranked #2 |
| **F12** | ETL Retrieval Collision | 1 | SES severity chunk or specific stage ETL chunk tied in rank |
| **F14** | Diagnostic Evidence Intent | 0 | Multi-turn symptom disambiguation (Zinc vs Brown Spot) |
| **F17** | Reranker Authority/Intent Collision | 18 | Agronomic reranker prioritized regulatory CIBRC chemical chunk over general extension bulletin |
| **F09** | Document Retrieval Miss | 7 | General document chunk fell outside top-5 |

---

## 2. Granular Forensic Case Log (Rank > 1)

| Query ID | Query Text | Expected ID | Actual Top 1 | Overall Rank | Code | Root Cause |
|---|---|---|---|---|---|---|
| `GOLDEN-013` | இலைப்பேன் பூச்சிக்கு தயாமீதாக்சம் எவ்வளவ... | `['DOC-PEST-006']` | `CHEM-004` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-014` | வோர்ல் மேகட் அல்லது குருத்து ஈ தாக்குதல்... | `['DOC-PEST-007']` | `ETL-014` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-018` | BPH hopper burn வட்ட திட்டு கருகல் எதனால... | `['DOC-PEST-002']` | `ETL-004` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-019` | வெள்ளிக்குருத்து வெங்காயத்தாள் போன்ற குழ... | `['DOC-PEST-005']` | `ETL-011` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-022` | பாக்டீரியா இலைக்கருகல் (BLB) நோய்க்கு என... | `['DOC-DIS-001']` | `CHEM-007` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-023` | குலை நோய் அல்லது Blast நோய்க்கு டிரைசைக்... | `['DOC-DIS-002']` | `CHEM-008` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-024` | கழுத்து குலை நோய் (Neck Blast) கதிர் உடை... | `['DOC-DIS-002']` | `CHEM-008` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-025` | மடல்கருகல் நோய் (Sheath Blight) தண்டு மட... | `['DOC-DIS-003']` | `CHEM-015` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-026` | Sheath Blight நோய்க்கு Hexaconazole அல்ல... | `['DOC-DIS-003']` | `CHEM-010` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-028` | மஞ்சள் கதிர் பூஞ்சாணம் (False Smut) நெல்... | `['DOC-DIS-005']` | `ETL-018` | 3 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-029` | False Smut வராம இருக்க கதிர் வெளிவரும் ம... | `['DOC-DIS-005']` | `ETL-018` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-030` | தண்டு அழுகல் நோய் (Stem Rot) அடிமட்டத்தி... | `['DOC-DIS-006']` | `CHEM-013` | 3 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-031` | Stem Rot நோய்க்கு வயலில் தண்ணீரை வடிக்க ... | `['DOC-DIS-006']` | `ETL-019` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-032` | மடல் அழுகல் நோய் (Sheath Rot) கதிர் முழு... | `['DOC-DIS-007']` | `CHEM-013` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-033` | செம்புள்ளி நோய் (Brown Spot) இலைகளில் வட... | `['DOC-DIS-008']` | `DDT-001` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-034` | பாக்டீரியா இலைக்கோடு நோய் (BLS) ஒளி ஊடுர... | `['DOC-DIS-009']` | `CHEM-007` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-043` | வயலில் சிலந்திகள் நிறைய இருந்தால் புகையா... | `['ETL-004']` | `ETL-003` | 2 | **F12** | ETL record outranked or rank collision with SES severity chunk |
| `GOLDEN-052` | வோர்ல் மேகட் இலைகளில் எத்தனை சதவீதம் சேத... | `['ETL-015']` | `ETL-014` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-064` | அண்ணாமலை கலவை இலை வெளுத்து போனால் எப்படி... | `AGRO-NUTRITION-IRON-CHLOROSIS` | `SEV-PEST-001` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-071` | குலை நோய்க்கு Tricyclazole ஸ்ப்ரே பண்ணலா... | `DIS-002` | `CHEM-008` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-073` | இலைப்பேன் சுருள் பேன் தாக்குதலுக்கு என்ன... | `PEST-006` | `CHEM-015` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-080` | மஞ்சள் கதிர் பூஞ்சாணம் வந்து நெல் மணி கர... | `DIS-007` | `ETL-018` | 2 | **F17** | Agronomic reranker ranked peer chemical/severity chunk above target document chunk |
| `GOLDEN-088` | ட்ரோன் மூலமா மருந்து அடிக்க ஏக்கருக்கு எ... | `` | `CHEM-003` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-089` | ட்ரோன் ஸ்ப்ரே பண்ணும்போது காற்றின் வேகம்... | `` | `CHEM-003` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-092` | Pseudomonas தெளித்த எத்தனை நாட்கள் கழித்... | `` | `CHEM-015` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-097` | தண்டு துளைப்பானுக்கு Chlorantraniliprole... | `` | `CHEM-001` | None | **F11** | Chemical entity outranked doc chunk or vice versa |
| `GOLDEN-098` | Thiamethoxam 25 WG மருந்துக்கு PHI நாட்க... | `` | `CHEM-004` | None | **F09** | Target document chunk not retrieved in top-5 |
| `GOLDEN-099` | Buprofezin 25 SC மருந்து பச்சை லேபிளா நீ... | `` | `CHEM-002` | None | **F11** | Chemical entity outranked doc chunk or vice versa |

---

## 3. Engineering Recommendations for Hardening

1. **Context-Preserving Chunk Enrichment:** Enrich all chemical chunks (`CHEM-001` to `CHEM-015`) and ETL chunks (`ETL-001` to `ETL-019`) with explicit parent document references (`DOC-PEST-001` to `DOC-DIS-008`), canonical pest/disease names, Latin binomials, and Tamil aliases.
2. **Tamil Subword & Morphological Stemming:** Implement root lemmatization and character 3-gram indexing in BM25 so colloquial suffixes (e.g. *தாக்குதலுக்கு*, *தென்படுகிறது*, *காஞ்சுபோச்சு*) do not reduce term frequency scores of core roots.
3. **Multi-Scale Field Boosts:** Apply explicit query-context alignment in RRF: when an intent is `QUERY_DOSAGE`, boost chemical chunks while linking parent document citations in the returned evidence object.
