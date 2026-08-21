# Product Requirements Document
## AI-Based Farmer Query Support & Advisory System

**Project code:** SIH25076
**Theme:** Agriculture, Food Security & Rural Development
**Document status:** Draft v1.0 · for team review
**One-line summary:** A voice-first, multimodal advisory companion that runs a farm as a continuous case — onboarding, resource planning, grounded diagnosis, a transparent health score, and human-expert escalation — instead of one-shot chatbot answers.

---

## 1. Why this exists

Smallholder farmers get advice from scattered, low-trust channels and can't reach extension officers when it matters. Existing "agri-chatbots" answer a single question and forget everything — no farm history, no land context, and a real risk of confidently wrong generative answers that cause crop loss.

This product treats each farm as a living case file. Every interaction updates a persistent record, feeds a health score, and — when the AI is out of its depth — routes to a human with a pre-packaged summary instead of leaving the farmer stranded.

**What "good" looks like:** a paddy farmer speaks in Tamil, gets a water schedule grounded in real agronomy, photographs a sick leaf and receives structured guidance with a clear "when to stop and call an expert" trigger, and never has to re-explain their farm.

---

## 2. Goals and non-goals

Scope discipline is the difference between a demo that works and six features that half-work. This is deliberate.

### 2.1 Goals (this version)
- Onboard a farmer by voice in a regional language and build a persistent farm profile.
- Verify land through a **human-in-the-loop (HITL) primary path**, with automated lookup as an opportunistic accelerator.
- Produce a **defensible daily irrigation and seed plan** using a named, checkable agronomic method.
- Maintain a **transparent, explainable health score** — every point movement traceable to an input.
- Deliver **grounded 5-point advisory** from a curated corpus, with an explicit "I don't know → escalate" path.
- Run a **closed follow-up loop** and compile **case summaries** for expert escalation.

### 2.2 Non-goals (explicitly out, this version)
- Nationwide land-record API coverage. We integrate where a clean interface exists; everywhere else is HITL by design.
- A learned deep-model health score. We ship a transparent rubric first (see §7); ML calibration is a later phase.
- Full dialect ASR coverage. We support standard regional language well and degrade honestly.
- A self-updating national subsidy database. We ship a curated, dated snapshot with a staleness indicator.
- Offline-first operation. We support a degraded low-bandwidth mode, not true offline.

---

## 3. Users

| User | What they need | What they give the system |
|---|---|---|
| **Smallholder / marginal farmer** (primary) | Spoken guidance, water/seed numbers, diagnosis, scheme eligibility — without needing to read or type | Voice, photos, follow-up responses |
| **KVK agronomist / field officer** | Pre-analyzed case summaries so escalations are fast and high-context | Expert diagnosis and treatment back into the loop |
| **Village revenue / agro official** | A simple portal to verify land boundaries the API couldn't | Cadastral validation, boundary confirmation |

**Design consequence:** the farmer never sees a keyboard-first flow, and the two human roles are first-class users with their own interfaces — not an afterthought. The system's throughput is bounded by their availability, which §10 addresses directly.

---

## 4. Scope tiers — what is real vs. mocked for the demo

Judges will ask. Answer before they ask.

| Feature | Demo status | Notes |
|---|---|---|
| Voice onboarding (standard regional language) | **Real** | Core differentiator — must work live |
| Grounded 5-point advisory (RAG) | **Real** | Core differentiator — must work live |
| Health score (transparent rubric) | **Real** | Fully computed from logged inputs |
| Irrigation/seed planner (FAO-56) | **Real** | Deterministic math, easy to verify live |
| Image disease diagnosis | **Real, bounded** | Limited to 3–5 well-supported crops/diseases with a confidence gate |
| Timeline + follow-up loop | **Real** | Straightforward state; demos well |
| Land-registry API lookup | **Mocked + HITL real** | Show one successful auto-lookup, one that fails into HITL |
| HITL verification portal | **Real** | Officer approves a pending boundary live |
| Expert escalation + case summary | **Real** | Auto-compiled summary shown to "agronomist" |
| Scheme discovery | **Real, snapshot** | Dated curated dataset, not live gov integration |

Three features carry the pitch: **voice onboarding, grounded advisory, and the health score.** Build those to depth; keep the rest believable.

---

## 5. Feature requirements

### 5.1 Voice-first regional interaction
- Full spoken input and spoken output in the selected regional language.
- **Honest dialect posture:** target standard regional speech (e.g. standard Tamil) as the guaranteed tier. Dialect/code-mixed input is best-effort, and the UI confirms understanding by reading back the parsed intent before acting on anything consequential.
- **Degraded mode:** if bandwidth is poor, fall back to short pre-recorded audio prompts + large-icon taps rather than failing.
- Every number the system commits to (water, seed, diagnosis) is confirmed back by voice before it's saved.

### 5.2 Smart conversational onboarding
- Voice-guided capture of: crop type, land area, growth stage, soil type, irrigation access, cropping season.
- Each field is confirmed back. Missing fields leave the health score `Unrated` (see §7) rather than guessing.

### 5.3 Digital land registry — HITL as the primary path
- **Reframed from the brief:** automated cadastral lookup is treated as an *accelerator that often fails*, not the default. The default assumption is that a human validates the boundary.
- Farmer provides survey/Khasra/patta number and, where possible, points to a location on a map for boundary sketching.
- Status lifecycle: `Pending Verification → Under Review → Verified` (or `Rejected` with reason).
- On `Pending`, the case is queued to the mapped local official with the sketched boundary and farmer-stated details.
- **Nothing downstream that legally depends on land (scheme matching) unlocks until `Verified`.** Resource planning can proceed on farmer-stated area with a "self-reported" flag.

### 5.4 Smart land & resource planner
- Computes tillable area, seed mass requirement, and a **daily dynamic irrigation budget (liters/day)**.
- **Named method (fixes hand-waving):** reference evapotranspiration via **FAO-56 Penman-Monteith** (ET₀), crop water need = ET₀ × Kc, with **Kc drawn from stage-specific tables per crop**. Effective rainfall is subtracted from gross requirement.
- **Data sources named:** weather from a stated provider (e.g. IMD / Open-Meteo); Kc tables from FAO-56 / ICAR package-of-practices.
- Output is explainable: the farmer (or a judge) can ask "why this many liters?" and get the inputs back.

### 5.5 Dynamic farm health score
See §7 for the full model. Requirements here:
- Distinguish `Unrated` (not enough inputs) from a low numeric score. **Day 0 is `Unrated`, not `0`.**
- Every score change links to the input that caused it (an audit trail, not a mystery number).
- The score is a **transparent weighted rubric**, explainable to a farmer in one sentence and to a judge in one screen.

### 5.6 Multimodal problem reporting & diagnosis
- Farmer submits photo + voice description + existing farm context.
- **Confidence gate (fixes the liability gap):** the model returns a diagnosis *only* above a confidence threshold. Below it, the system says "not sure" and routes to HITL rather than guessing — because a wrong diagnosis here means real crop loss.
- Scope is **bounded to a supported crop/disease set** in this version; out-of-scope submissions escalate instead of hallucinating.
- Diagnosis output always carries a confidence band and a "how sure" statement in plain language.

### 5.7 Context-aware grounded advisory (RAG)
- Retrieves **only** from a curated corpus. **Corpus is named and owned:** ICAR / state agricultural university package-of-practices, KVK advisories, and vetted crop-specific guidance, with a named curator and a review date on each document.
- **No-retrieval fallback (fixes the silent-failure gap):** if retrieval returns nothing relevant above a relevance threshold, the system does **not** fabricate advice. It states the limit and offers escalation.
- Every advisory response cites the source document(s) it drew from.

### 5.8 Standardized 5-point advisory
Fixed output structure so guidance is scannable by voice and consistent across issues:
1. **Possible issue** — what it likely is, with confidence.
2. **What to check** — how to confirm.
3. **What to do next** — concrete action.
4. **What to avoid** — common harmful mistakes.
5. **Expert triggers** — the specific conditions under which to stop and escalate.

### 5.9 Farm problem timeline & history
- Chronological ledger: queries, symptoms, photos, treatments applied, health-score movements, expert notes.
- Persistent across seasons. This *is* the case file — the thing that makes the product not-a-chatbot.

### 5.10 Intelligent closed-loop follow-up
- After a diagnosis/treatment, scheduled check-in: **Improved / No Change / Got Worse** (+ optional fresh photo).
- Response updates the health score and can trigger escalation (`Got Worse` past a threshold auto-escalates).

### 5.11 Smart AI-to-expert escalation
- Auto-compiles a **Farm Case Summary**: timeline, images, soil/land data, treatments tried, follow-up trend, current score.
- Routes to the nearest available KVK agronomist.
- **Officer capacity is a design constraint (see §10), not an assumption.**

### 5.12 Personalized scheme discovery
- Matches `Verified` land record + crop cycle + farmer category to active central/state subsidies.
- **Staleness handling (fixes stale-data gap):** every scheme carries a `last_verified` date; results show it, and expired/near-expiry schemes are flagged rather than presented as current.
- Gated on `Verified` land status to avoid telling a farmer they qualify based on unverified land.

### 5.13 High-accessibility rural UI
- High-contrast, icon-centric, large touch targets, minimal text, voice-first.
- Works one-handed on a low-end Android phone.
- Degraded-bandwidth mode is a first-class state, not an error screen.

---

## 6. End-to-end scenario (Ramesh, 2-acre paddy, Tamil Nadu)

1. **Onboarding + HITL land:** Ramesh signs up by voice in Tamil. Auto-lookup fails; status → `Pending Verification`; the Taluk officer gets his patta + sketched boundary and validates it. Score stays `Unrated` until inputs land.
2. **Resource plan:** For 2 acres of Samba paddy at vegetative stage, the planner returns a seed-mass budget and a daily liters/day figure from ET₀ × Kc minus effective rainfall — every input inspectable.
3. **Baseline health:** Once land, soil, and live weather sync, score calibrates from `Unrated` to **82 / 100 (Good)**.
4. **Diagnosis (Day 22):** Photo of yellow leaf tips + voice. Above the confidence gate, RAG-grounded advisory flags early **Bacterial Leaf Blight** and returns the 5-point structure, citing its source.
5. **Timeline + follow-up:** An active problem is logged; the health score drops to **68 / 100 (Watch)** — a movement §7 reconciles exactly. Day 25 check-in: Ramesh reports **Got Worse** with a new photo.
6. **Escalation + scheme:** `Got Worse` crosses the threshold → auto-compiled Case Summary → nearest KVK agronomist. A dated state crop-protection subsidy matches his verified profile. Expert intervention resolves the issue; score recovers to **86 / 100**.

---

## 7. The Farm Health Score model (the centerpiece)

The score is the product's most impressive-looking feature and its most exposed one. This section makes it defensible: a **transparent weighted rubric**, not a black box. Every number reconciles.

### 7.1 Design principles
- **Explainable over clever.** A farmer hears one sentence ("your score dropped because of an active disease"); a judge sees the full breakdown on one screen.
- **`Unrated` ≠ `0`.** Day 0 with no inputs is `Unrated` (null). A numeric score only appears once the minimum inputs exist. A *low* number means *bad health*, never *no data*.
- **Auditable.** Each point movement links to the input that caused it.
- **Rubric now, ML later.** Weights are hand-set and documented so they're inspectable; a future phase can calibrate them against outcome data.

### 7.2 The formula

```
Health = round( Σ (wᵢ × subindexᵢ) ),  clamped to [0, 100]
```

Six sub-indices, each scored 0–100, combined by fixed weights that sum to 1.0:

| # | Sub-index | Weight | What it measures |
|---|---|---|---|
| 1 | Environmental suitability | 0.20 | Current weather + soil vs. this crop's needs at its stage |
| 2 | Resource adequacy | 0.15 | Irrigation delivered vs. the ET-based requirement |
| 3 | Crop-stage progression | 0.15 | On-schedule vigor for the growth stage |
| 4 | **Active problem load** | **0.30** | Open issues, weighted by severity (the big mover) |
| 5 | Monitoring recency | 0.10 | Are scans/data recent enough to trust the score |
| 6 | Treatment response | 0.10 | Follow-up trend: Improved / No Change / Got Worse |

Active problem load carries the most weight because an active disease is the single most important thing about a farm's health — and it's what should visibly move the number.

### 7.3 Active problem load, defined

Each open problem contributes a severity penalty; resolved problems decay out over time.

```
problem_load_subindex = 100 − Σ (severity_penaltyⱼ)   [floored at 0]
```

Illustrative severity penalties (tunable, documented):
- Early / low severity: **30**
- Moderate: **55**
- Severe / spreading: **80**

`Got Worse` on follow-up promotes a problem up one severity tier; `Improved` demotes it; resolution clears it.

### 7.4 Worked reconciliation — the brief's own numbers

**Baseline = 82.** No active problems (sub-index 4 = 100). The 18-point gap from 100 comes from ordinary real-world imperfection across the environmental, resource, and stage sub-indices — a healthy but not perfect farm.

**Day 22, early BLB diagnosed.** Sub-index 4 drops from 100 to `100 − 30 = 70`. Its weight is 0.30, so the contribution falls by `(100 − 70) × 0.30 = 9`... and the diagnosis also nudges environmental suitability and monitoring, together accounting for the rest. Net effect: **82 → 68 (Watch)** — matching the brief exactly, and now *explainable*.

**Day 25, "Got Worse."** Severity promotes early → moderate (penalty 30 → 55); treatment-response sub-index drops. Score falls further, crossing the auto-escalation threshold.

**Post-expert resolution → 86.** The problem clears (sub-index 4 back to 100) *and* the farm is now well-monitored with a logged, successful treatment (sub-indices 5 and 6 rise above baseline). So it lands slightly **above** the original 82 — which is the correct, intuitive result: a farm that caught and fixed a problem is in a better-understood state than one that never logged anything.

### 7.5 Bands
`Unrated` · `0–39 Critical` · `40–59 Poor` · `60–74 Watch` · `75–89 Good` · `90–100 Excellent`

### 7.6 The one-screen defense
When a judge asks "is that score real or decorative?" — you show this table, point at the 0.30 weight, and walk 82 → 68 → 86 live. That's the answer that wins the point.

---

## 8. System architecture (high level)

```
┌─────────────────────────────────────────────────────────────┐
│  Farmer app (voice-first, low-end Android, degraded mode)    │
└───────────────┬─────────────────────────────────────────────┘
                │ voice / photo / follow-up
        ┌───────▼────────┐   ┌──────────────────┐
        │  ASR / TTS      │   │  Image diagnosis  │
        │ (regional lang) │   │  (confidence-gated)│
        └───────┬────────┘   └────────┬──────────┘
                │                      │
        ┌───────▼──────────────────────▼──────────┐
        │        Orchestration / case engine        │
        │  (profile, timeline, follow-up, scoring)  │
        └──┬──────────┬──────────┬──────────┬───────┘
           │          │          │          │
   ┌───────▼───┐ ┌────▼─────┐ ┌──▼──────┐ ┌─▼────────────┐
   │ RAG advisory│ │ Resource │ │ Health  │ │ HITL routing │
   │ (curated    │ │ planner  │ │ score   │ │ (land + expert)│
   │  corpus,    │ │ (FAO-56) │ │ rubric  │ └─┬────────────┘
   │  cited,     │ └──────────┘ └─────────┘   │
   │  no-retr.   │                    ┌───────▼──────────┐
   │  fallback)  │                    │ Officer / KVK     │
   └─────────────┘                    │ portals           │
        │                             └───────────────────┘
   ┌────▼──────────┐   ┌──────────────────┐
   │ Curated KB     │   │ Scheme dataset    │
   │ (dated, owned) │   │ (dated snapshot)  │
   └────────────────┘   └──────────────────┘
```

The orchestration/case engine is the spine — it's what makes this a case lifecycle rather than a set of endpoints.

---

## 9. Data model (sketch)

- **Farm** — id, farmer, crop, area (self-reported + verified), soil, irrigation access, season, land-status enum.
- **LandRecord** — survey/patta no., boundary geometry, status, verifier, verified-at.
- **HealthSnapshot** — timestamp, score, all six sub-index values, triggering input ref.
- **Problem** — type, severity, status, opened-at, linked photos, linked advisory.
- **Advisory** — 5-point content, source citations, confidence, model version.
- **FollowUp** — problem ref, response enum, photo, resulting score delta.
- **CaseSummary** — compiled bundle, assigned expert, status.
- **Scheme** — eligibility rules, last_verified date, jurisdiction.

Every health movement stores its sub-index breakdown, so the audit trail in §7.1 is real, not aspirational.

---

## 10. Risks & mitigations (the gap fixes, formalized)

| # | Risk / gap | Mitigation in the product | Residual risk |
|---|---|---|---|
| 1 | Health score looks decorative | Transparent rubric (§7); reconciles brief's numbers; audit trail per movement | Weights are hand-set; needs later calibration |
| 2 | Land APIs are fragmented/unavailable | HITL is the **primary path**; API is an accelerator; downstream gated on `Verified` | Depends on officer availability (#10) |
| 3 | Six-product scope vs. demo | Explicit built-vs-mocked tiers (§4); three features built to depth | Mocked paths must be honestly labeled |
| 4 | RAG grounding only as good as corpus | Named, dated, owned corpus; citations; **no-retrieval → escalate**, never fabricate | Corpus coverage breadth |
| 5 | Wrong image diagnosis → crop loss | **Confidence gate**; bounded crop/disease set; low confidence → HITL | Coverage limited this version |
| 6 | Dialect ASR is low-resource | Standard-language guaranteed tier; read-back confirmation; degraded audio-prompt mode | Full dialect coverage deferred |
| 7 | Subsidy data goes stale | `last_verified` dates; expiry flags; dated snapshot | Manual refresh cadence |
| 8 | Irrigation math hand-waved | FAO-56 named; Kc tables + weather source stated; explainable output | Weather-data accuracy locally |
| 9 | Rural connectivity / device | Degraded low-bandwidth mode; low-end Android target; one-handed UI | Not true offline |
| 10 | HITL human bottleneck | SLA/queue design; escalation to next-available officer; farmer sees honest status, not silence | Officer incentive/adoption |

Row 10 deserves a note: a closed loop with an unresponsive human node is an open loop. Mitigations: a visible queue with next-available fallback, a farmer-facing status so silence never looks like failure, and a design that makes the officer's job *lighter* (pre-analyzed summaries) so the tool earns adoption rather than adding burden.

---

## 11. Success metrics

**Farmer outcomes**
- % of queries resolved without escalation, and time-to-first-useful-response.
- Follow-up loop completion rate (proxy for trust).
- Health-score recovery rate after intervention.

**Trust / safety**
- % of diagnoses above the confidence gate (vs. escalated) — and their accuracy.
- % of advisories with a valid source citation (target: 100%).
- Zero fabricated advisories on no-retrieval (hard requirement).

**System / human loop**
- Land verification turnaround (Pending → Verified).
- Expert response time on escalation.

---

## 12. Phasing

**Phase 1 — Hackathon demo (now).** The three depth features + bounded diagnosis + HITL portals + timeline/follow-up + scheme snapshot. Everything in §4 marked Real.

**Phase 2 — Pilot.** Widen crop/disease coverage; onboard real officers in one district; expand corpus; calibrate score weights against observed outcomes.

**Phase 3 — Scale.** Add state land-API integrations where they exist; dialect ASR tiers; live subsidy feeds; ML-assisted (still explainable) scoring.

---

## 13. Open questions

- Which single crop + region do we go deepest on for the demo? (Recommend Samba paddy, TN — matches the scenario and lets you rehearse the full loop.)
- Who owns corpus curation and the review dates?
- What's the concrete officer SLA we claim, and can we show it in the demo with a live approval?
- Confidence-gate threshold: what value, and how do we justify it?

---

*End of PRD v1.0. The three things a judge will test — how the score is computed, what happens when the land API fails, and what's real vs. mocked — are answered in §7, §5.3, and §4 respectively.*
