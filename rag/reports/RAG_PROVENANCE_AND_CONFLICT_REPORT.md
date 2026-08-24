# BHOOMI Source Conflict Resolution & Evidence Provenance Report

**Assessment Date:** August 2026  
**Auditor:** Provenance & Hierarchy Evaluator  
**Hierarchy Policy:** Level 10 (CIBRC Regulatory) $>$ Level 9 (ICAR / IRRI) $>$ Level 8 (TNAU University) $>$ Level 7 (KVK District Extension)  
**Total Conflict Scenarios Tested:** 2  
**Resolution Accuracy:** 100.0%  

---

## 1. Conflict Resolution Verification Matrix

| Scenario Name | Competing Sources | Resolved Top Authority | Conflict Handled | Status |
|---|---|---|---|---|
| **CIBRC Ban vs Local Advisory Practice (Carbofuran)** | CIBRC vs Extension | `CIBRC_REG_01` (Tier 10) | Deterministic Override | **PASSED** |
| **ICAR National Dosage vs Local Sub-Tier Dosage** | CIBRC vs Extension | `ICAR_IIRR_GUIDE_02` (Tier 9) | Deterministic Override | **PASSED** |

---

## 2. Invariant Citation Contract

Every generated advisory embeds verifiable provenance metadata:
- `document_id` (e.g. `DOC-PEST-001`)
- `authority_level` (10, 9, 8, or 7)
- `citation` (e.g. `ICAR-IIRR Technical Bulletin No. 94/2024`)
- `publication_date` and `cibrc_registration_number`
