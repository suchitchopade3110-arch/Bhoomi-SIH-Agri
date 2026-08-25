# BHOOMI Knowledge Governance & Provenance Classification Report

**Assessment Date:** August 2026  
**Auditor:** Agricultural Knowledge & Dataset Governance Engineer  
**Classification Standard:** 7-Tier Lifecycle (`AUTHORITATIVE`, `REVIEWED`, `CONDITIONAL`, `AMBIGUOUS`, `QUARANTINED`, `REJECTED`, `SUPERSEDED`)  

---

## 1. Document Ingestion Classification Matrix

| Document Title | Source Institution | Classification | Ingestion Action | Policy Rationale |
|---|---|---|---|---|
| **ICAR-IIRR Rice Blast Management Protocol 2024** | ICAR-IIRR | `AUTHORITATIVE` | `APPROVED_FOR_PRODUCTION_INDEX` | Peer-reviewed standard from ICAR-IIRR (Authority Tier 9). |
| **Carbofuran 3G Stem Borer Advisory** | State Extension Old Bulletin | `REJECTED` | `BLOCK_FROM_INDEXING` | Active ingredient 'carbofuran 3g' is restricted/banned under CIBRC regulatory gazette. |
| **மட்ட பூச்சி கட்டுப்பாடு நாட்டு முறை** | Farmer Community Survey | `QUARANTINED` | `REQUIRE_KVK_ESCALATION` | Contains colloquial ambiguity; requires expert clarification. |
| **TNAU Sheath Blight Biological Management Guide** | TNAU Agritech Portal | `AUTHORITATIVE` | `APPROVED_FOR_PRODUCTION_INDEX` | Peer-reviewed standard from TNAU AGRITECH PORTAL (Authority Tier 8). |

---

## 2. Invariant Ingestion Principles

- **Zero Unverified Direct Ingestion:** No raw document can enter production vector/BM25 indices without passing cryptographic schema verification.
- **Mandatory CIBRC Alignment:** Any advisory contradicting CIBRC banned chemical notifications is classified as `REJECTED` at pre-ingestion time.
