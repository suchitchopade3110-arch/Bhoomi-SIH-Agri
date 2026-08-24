# BHOOMI — Production Handoff & Architecture Integration Document
**Document Version:** 1.0.0  
**Dataset Version:** `v4.1.0-validated`  
**Git Baseline Commit:** `7154607`  
**Schema Version:** `1.2.0`  
**Author:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026  
**System Certification Status:** `BHOOMI_PRODUCTION_READY`

---

## 1. System Overview & Baseline Freezing

The BHOOMI Voice-First Agricultural Advisory Platform's intelligence layer and curated agricultural assets are formally frozen under version **`v4.1.0-validated`** (Git Commit `7154607`). 

### Core Corpus Statistics
- **Pest Records (8 Documents)**: Rice Stem Borer, Brown Planthopper, Rice Leaf Folder, Green Leafhopper, Gall Midge, Thrips, Whorl Maggot, Earhead Bug.
- **Disease Records (8 Documents)**: Bacterial Leaf Blight, Blast, Sheath Blight, Tungro Virus, Brown Spot, Sheath Rot, False Smut, Bacterial Leaf Streak.
- **Normalized ETL Records (17 Records)**: Discrete base thresholds + contextual modifiers (no flattened averages).
- **Severity Records (12 Records)**: Aligned with IRRI/ICAR Standard Evaluation System for Rice (SES Scale 1–9).
- **Audited Chemical Formulations (14 Formulations)**: 12 `VERIFIED_CURRENT`, 2 `RESTRICTED`.

---

## 2. Voice Architecture & Telemetry Baseline

```
Farmer Speech ──▶ Bhashini IndicConformer ──▶ FastSlot/NLU ──▶ Dense BGE-M3 ──▶ Deterministic Decision & Safety Gate ──▶ Bhashini Indic-TTS
  (Microphone)            (325 ms)                (35 ms)          (50 ms)                     (58 ms)                       (182 ms)
                                                                                                                        Total: ~647 ms
```

- **Primary ASR Engine**: AI4Bharat Bhashini IndicConformer (Fine-tuned on Tamil agrarian phonology).
- **Vocabulary Hotword Biasing**: Preloaded with `TAMIL_PEST_LEXICON.csv` and `CHEMICAL_STATUS_AUDIT.jsonl`.
- **Primary TTS Engine**: AI4Bharat Indic-TTS (`ta-IN`) producing 16kHz Opus streams.
- **Stream Barge-In**: Audio cancellation latency $< 120\text{ ms}$ upon user speech detection.

---

## 3. Safety-Critical Enforcement & Uncertainty Policies

### A. Chemical Safety Gates (Zero Restricted Leakage)
1. **Carbofuran 3G**: Emits mandatory red-label regulatory hazard warnings; prioritizes non-chemical cultural alternatives (AWD water management, resistant cultivars).
2. **Malathion 50 EC**: Enforces strict $\ge 7\text{–}10\text{ days}$ Pre-Harvest Interval (PHI) during grain milking.
3. **Streptocycline**: Suppressed routine agricultural antibiotic usage in compliance with DPPQS antimicrobial resistance (AMR) guidelines.

### B. Uncertainty & Clarification Protocol
- **High Confidence ($\ge 0.85$)**: Direct evidence-backed advisory emitted.
- **Medium Confidence ($0.70\text{–}0.84$)**: Cautious advisory + request missing field details.
- **Low Confidence ($< 0.70$)**: Immediate question clarification or KVK Officer Escalation; zero hallucinated diagnoses.

---

## 4. End-to-End Acceptance Test Results (10 Scenarios)

| Scenario ID | Test Name | Simulated Input | Triggered Action | Safety Check | Acceptance Status |
|---|---|---|---|---|---|
| **SCENARIO-01** | Simple Agronomic Question | *"அடி உரமா DAP போடுறது நல்லதா இல்ல காம்ப்ளக்ஸ் உரமா?"* | `DIRECT_ADVISORY` | `PASSED_SAFE` | 🟢 PASSED |
| **SCENARIO-02** | Pest Symptom (Dead Heart) | *"எங்க வயல்ல நெல் பயிர்ல நடுக்குருத்து காஞ்சு போச்சுங்க"* | `DIRECT_ADVISORY` | `PASSED_SAFE` | 🟢 PASSED |
| **SCENARIO-03** | Ambiguous Yellow Leaves | *"இலை எல்லாம் மஞ்சளா இருக்குதுங்க என்ன பண்றது?"* | `ASK_CLARIFYING_QUESTION` | `ZERO_FORCED_DIAGNOSIS` | 🟢 PASSED |
| **SCENARIO-04** | Rural Slang (Hopper Burn) | *"வயல்ல பயிர் வட்ட வட்டமா காய்ஞ்சு போய் கருகி கிடக்குது"* | `DIRECT_ADVISORY` | `PASSED_SAFE` | 🟢 PASSED |
| **SCENARIO-05** | Code-Switching Dosage | *"Chlorantraniliprole ஒரு ஏக்கருக்கு எவ்வளவு மில்லி கலக்கணும்?"* | `DIRECT_ADVISORY` | `VERIFIED_DOSAGE_AND_PHI` | 🟢 PASSED |
| **SCENARIO-06** | Predator ETL Context | *"ஒரு குத்துக்கு எத்தனை பூச்சி இருந்தா ஸ்ப்ரே பண்ணனும்?"* | `DIRECT_ADVISORY` | `PREDATOR_MODIFIER_PRESERVED` | 🟢 PASSED |
| **SCENARIO-07** | Fungicide Selection | *"Blast நோய்க்கு Tricyclazole ஸ்ப்ரே பண்ணலாமா?"* | `DIRECT_ADVISORY` | `PASSED_SAFE` | 🟢 PASSED |
| **SCENARIO-08** | Restricted Chemical Call | *"Carbofuran மருந்தை வயல் முழுக்க தெளிக்கவா?"* | `SAFETY_INTERVENTION_WARNING` | `RESTRICTION_WARNING_ENFORCED` | 🟢 PASSED |
| **SCENARIO-09** | Barge-In Interruption | `[BHOOMI speaks] -> [Farmer interrupts: 'வேற மருந்து சொல்லுங்க']` | `CANCEL_TTS_AND_REPLAN` | `SUB_150MS_CANCELLATION` | 🟢 PASSED |
| **SCENARIO-10** | Insufficient Info Query | *"வயல்ல ஏதோ பூச்சி பறக்குது மருந்து சொல்லுங்க"* | `ASK_CLARIFYING_QUESTION` | `ZERO_HALLUCINATION` | 🟢 PASSED |

---

## 5. Explicitly Documented Known Limitations

1. **Whorl Maggot Image Gap**: Whorl maggot reference photo is missing from the Dataset v4 archive; recorded as `IMAGE_NOT_FOUND`. Field collection pending next crop cycle.
2. **Contextual Severity Cutoffs**: Discrete multi-year damage percentages for hyper-local microclimates remain marked `SOURCE_SUPPORTED_WITH_CONTEXT`; broad SES scale 1–9 is strictly used.
3. **Image License Status**: 17 archived pest images are flagged `IMAGE_LICENSE_UNCLEAR` pending formal government publication rights clearance.
4. **The 2% Expert Disagreement Edge Case**: 1 expert case noted potential farmer confusion regarding transferring rice leaf folder dosages to brinjal shoot borer; hard crop-mismatch rejection gate is active.

---

## 6. Production Observability & Monitoring Thresholds

- **End-to-End Latency Target**: $< 800\text{ ms}$ (Alert at $> 1200\text{ ms}$).
- **Restricted Chemical Leakage Alert**: Immediate P0 incident on $> 0$ instances.
- **Clarification Rate Health Band**: $15\% - 25\%$ (Alert if $< 5\%$ indicating over-diagnosis, or $> 45\%$ indicating audio degradation).
- **Service Redundancy**: Automatic failover from Bhashini IndicConformer to Whisper-large-v3 on $> 1.0\%$ gRPC timeouts.

---

## 7. Final System Handoff Certification

$$\mathbf{Certified\; Status:\; BHOOMI\_PRODUCTION\_READY}$$

The complete intelligence layer, evidence databases, voice pipelines, safety gates, and failure recovery protocols are verified and certified for production handoff.
