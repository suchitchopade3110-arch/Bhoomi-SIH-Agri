# BHOOMI ETL Contextual Interpretations & Source Divergence Notes
**Document ID:** ETL-CONFLICT-001  
**Location:** `data/curated/Dataset_v4_validated/validation/`  
**Auditor:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026

---

## 1. Overview

This document analyzes the 6 threshold areas in `ETL_EVIDENCE.jsonl` where source interpretation depends on critical agronomic context (e.g., presence of viral vectors, predator ratios, specific growth stages, or divergent sampling units). 

No thresholds have been combined, calculated, or modified.

---

## 2. Context-Dependent Thresholds & Discrepancies

### A. Green Leafhopper (GLH): Direct Feeding Damage vs. Virus Vector Role
- **Records Affected:** `ETL-008`, `ETL-009`, `ETL-010` (`DOC-PEST-004`)
- **Dataset v4 Threshold:**
  - Seedling: `5 hoppers/hill`
  - Vegetative: `10–15 hoppers/hill`
  - Reproductive: `20 hoppers/hill`
- **Agronomic Context & Source Divergence:**
  - **Direct Sap-Feeding Context (Non-Endemic)**: The Dataset v4 thresholds accurately reflect feeding tolerance established in the ICAR-IIRR Production Manual.
  - **Tungro Virus Vector Context (Endemic Delta Tracts)**: In regions with active Rice Tungro Virus (RTV) history (e.g., Thanjavur, Tiruvarur), the economic threshold drops drastically to **1–2 hoppers per hill** (or 1 hopper per 2 hills in nursery). A single viruliferous hopper can inoculate multiple plants, causing complete loss before direct feeding thresholds are reached.
- **RAG Advisory Guidance:** The intelligence layer must evaluate whether Tungro is present in the farm context before advising the higher feeding threshold.

---

### B. Brown Planthopper (BPH): Natural Enemy & Predator Ratios
- **Records Affected:** `ETL-004`, `ETL-005` (`DOC-PEST-002`)
- **Dataset v4 Threshold:**
  - Vegetative: `5–10 nymphs/hill`
  - Reproductive: `10–20 nymphs/hill`
- **Agronomic Context & Source Divergence:**
  - **Predator-Depleted Context**: If insecticide misuse has destroyed beneficial predators, spraying is warranted at the lower boundary (`5 nymphs/hill`).
  - **Predator-Rich Context**: IRRI and TNAU guidelines specify that if mirid bugs (*Cyrtorhinus lividipennis*) or wolf spiders (*Lycosa pseudoannulata*) are present at $\ge 1\text{ per hill}$, the economic injury threshold increases to **15–20 nymphs per hill**, because biological predation naturally controls the population without chemical intervention.
- **RAG Advisory Guidance:** Advisories should prompt the farmer to check for predatory mirid bugs before applying chemical sprays like Buprofezin.

---

### C. Leaf Folder: Vegetative vs. Flag Leaf Emergence Vulnerability
- **Records Affected:** `ETL-007` (`DOC-PEST-003`)
- **Dataset v4 Threshold:**
  - Reproductive: `2 larvae/hill` OR `20% folded leaves`
- **Agronomic Context & Source Divergence:**
  - **General Tillering Context**: Paddy foliage can tolerate up to 20% leaf area damage during vegetative tillering with compensatory growth.
  - **Flag Leaf Emergence Context (Booting Stage)**: During panicle emergence and boot leaf stage, the threshold tightens to **5–10% damaged flag leaves**. The flag leaf alone provides over $50\%$ of the carbohydrates for grain filling; 20% flag leaf damage causes direct yield collapse.
- **RAG Advisory Guidance:** Flag leaf damage must trigger early intervention even if overall canopy damage is below 20%.

---

### D. Earhead Bug: Visual Panicle Count vs. Hill Sampling Units
- **Records Affected:** `ETL-017` (`DOC-PEST-008`)
- **Dataset v4 Threshold:**
  - Flowering: `5 bugs/100 panicles`
  - Milking: `10 bugs/100 panicles`
- **Agronomic Context & Source Divergence:**
  - **ICAR-IIRR Technical Standard**: Uses a panicle-based sampling unit (`5–10 bugs per 100 panicles` observed across 20 random spots).
  - **State Extension / TNAU Field Standard**: Several field-level advisory bulletins cite **1 bug per hill at flowering** or **2 bugs per hill during grain milking**.
- **Sampling Equivalence**: In a standard planting density of $50\text{ hills/m}^2$ (approx. 4–6 tillers/hill), 1–2 bugs per hill equates to approximately 10–20 bugs per 100 panicles.
- **RAG Advisory Guidance:** Support both panicle-count and hill-count phrasing when processing farmer voice inputs.

---

### E. Stem Borer: Egg Mass Count vs. Symptom Damage Duality
- **Records Affected:** `ETL-001`, `ETL-002` (`DOC-PEST-001`)
- **Dataset v4 Threshold:**
  - Vegetative: `1 egg mass/m²` OR `10% dead hearts`
  - Reproductive: `1 egg mass/m²` OR `5% white ears`
- **Agronomic Context & Source Divergence:**
  - **Preventive Scouting**: Scouting egg masses (1/m²) enables biocontrol release (*Trichogramma*) before internal larval boring occurs.
  - **Curative Assessment**: Dead hearts (10%) and white ears (5%) indicate established larval infestation where systemic chemicals or immediate water management are required.
- **RAG Advisory Guidance:** The system must distinguish between egg-mass triggers (preventive/biological) and symptom triggers (curative).

---

## 3. Summary of Findings

- **No irreconcilable source contradictions** exist among the 8 pest definitions.
- All 17 threshold records are grounded in verified ICAR, IRRI, and TNAU publications.
- Contextual differences arise from **environmental factors** (presence of viral pathogens or natural predators) and **sampling methods** rather than conflicting research data.
