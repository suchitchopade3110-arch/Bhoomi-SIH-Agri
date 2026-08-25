# Bhoomi — Feature Checklist (SIH26131)

Derived from `SIH25076_PRD.md` §5/§7, `Bhoomi_Feature_Realignment_SIH26131.md`, the persona intake decisions, and `Bhoomi_36hr_Plan_Per_Teammate.md`. One line per feature, phrased as something you can actually check. Tick only when you've seen it work, not when the file exists.

Legend — A = core loop (never cut) · B = shallow trust side-feature · C = persona-accepted UX · D = supporting/conditional

## 0. Hard invariants (check these first, check them last)

- [ ] Never answers below the confidence gate — enforced in orchestration code, not prompt wording
- [ ] Never fabricates on no-retrieval — `retrieved:false` path returns escalation, not advice
- [ ] Every advisory carries ≥1 citation with `doc_id`, `title`, `reviewed_on`
- [ ] Risk/advisory output is deterministic — no `datetime.now()` in the compute path
- [ ] Every external dependency sits behind a typed Protocol; no direct adapter calls at call sites

## 1. Onboarding & profile — A

- [ ] `POST /farms` accepts exactly 3 fields: crop, growth_stage, region
- [ ] Old fields gone: area_acres, soil_type, irrigation_access, season
- [ ] Voice onboarding reads back each field for confirmation before saving
- [ ] Day 0 with missing inputs → `unrated`, never `0`
- [ ] Veteran/novice `ui_mode` toggle persists on the profile — C

## 2. Multimodal diagnosis — A (PRD §5.6)

- [ ] `POST /farms/{id}/diagnose` accepts image_asset_id + optional voice/text + `target_type`
- [ ] `target_type: disease | pest` routes to the right gate and corpus
- [ ] Bounded label set enforced — out-of-scope label escalates, never guesses
- [ ] Diagnosis returns label, stage, confidence
- [ ] Image upload goes via presign, never raw bytes to the API

## 3. Confidence gate — A (never cut)

- [ ] Shared 0.70 threshold across disease and pest, separate `SUPPORTED_LABELS` per type
- [ ] Below gate → escalation object only; above gate → advisory object only; never both, never neither
- [ ] Gate object visible in the response: `confidence`, `threshold`, `reason_code`, `alternatives[]` — C
- [ ] `alternatives[]` populated from Tharun's top-3 labels (fixed stub pair acceptable as fallback)
- [ ] Confidence chip renders at top of the diagnosis screen, colour-coded pass/fail
- [ ] Below-gate screen shows ranked alternatives + escalation status and no advice

## 4. RAG advisory — A (PRD §5.7, §5.8)

- [ ] Single pgvector index with `content_type` and `crop` metadata filters
- [ ] Relevance threshold traced to `constants.py` — not an invented value
- [ ] 5-point structure returned in full: possible issue / what to check / what to do next / what to avoid / expert triggers
- [ ] "What to avoid" ordered first and visually loudest on the farmer screen — C (never cut)
- [ ] `POST /advisory/query` standalone path works with `target_type`
- [ ] No-retrieval → `{retrieved:false, reason:"no_relevant_source", escalation_offered:true}`
- [ ] Corpus has real paddy/BLB content with `distinguishing_cues` (Checkpoint C at hour 16)

## 5. Crop risk / health advisory — A (rework of PRD §7)

- [ ] 4 sub-indices only: active_problem_severity 0.40, environmental_risk 0.25, monitoring_recency 0.15, treatment_response 0.20 — weights sum to 1.0
- [ ] Reconciliation walk reproduces 82 → 73 → 57 → 91 as a passing test
- [ ] Full breakdown persisted on every snapshot (values + weights + contributions + triggering_input)
- [ ] Farmer home screen shows trend arrow first, numeric one tap deeper — C
- [ ] Qualitative one-sentence advisory derived from existing data (no second scoring engine)
- [ ] `GET /farms/{id}/risk`, `/risk/history`, `POST /risk/recompute` all wired

## 6. Follow-up loop — A (PRD §5.10)

- [ ] `POST /followups/{id}/respond` accepts improved / no_change / got_worse + optional photo
- [ ] `got_worse` promotes severity one tier; `improved` demotes; resolve clears
- [ ] `got_worse` past threshold auto-escalates and returns `case_id`
- [ ] Response returns `severity_change` and `risk: {from, to, band}`

## 7. Escalation & case summary — A (PRD §5.11)

- [ ] Bundle uses `environmental_context` + `problem_history` in place of land/soil fields
- [ ] Bundle carries crop, region, growth_stage, both photos, AI diagnosis + confidence, treatments tried, follow-up trend
- [ ] Next-available agronomist routing; `OFFICER_UNAVAILABLE` falls through, never dead-ends — C
- [ ] Queue position + ETA shown to the farmer on escalation confirmation — C
- [ ] Static per-crop interim guidance card shown while waiting — C
- [ ] `POST /cases/{id}/resolve` clears the problem and triggers a risk recompute (→ 91)
- [ ] Case detail is one screen, above the fold, three actions: confirm / correct / request info
- [ ] Case PDF: backend payload + Flutter share sheet — C

## 8. Problem timeline — A (PRD §5.9)

- [ ] Chronological, scoped to problem history only (no land/resource events)
- [ ] Every risk movement renders its cause, not just the number

## 9. Early-warning alerts — A (new for this PS)

- [ ] Trigger spec decided: weather / seasonal / regional_outbreak / combined
- [ ] `inspection_tasks[]` is non-null and non-empty — an alert cannot issue without at least one corpus-sourced task — C (never cut)
- [ ] Alert card non-dismissible until: inspected-nothing / inspected-found / remind-tomorrow
- [ ] `POST /alerts/{id}/acknowledge` records which of the three the farmer chose

## 10. Trust side-features — B (build thin, cut first under pressure)

- [ ] Land: `POST /farms/{id}/land` takes a survey number → `pending_verification`. No polygon, no map, no auto-lookup mock
- [ ] Officer review screen: approve/reject + reason. No boundary correction UI
- [ ] Scheme discovery: static dated JSON filtered by crop + region + `land_status=verified`
- [ ] Scheme staleness: `last_verified` shown, expiring/expired flagged
- [ ] `GET /farms/{id}/schemes` returns 409 `LAND_NOT_VERIFIED` when land isn't verified

## 11. Treatment efficacy — D

- [ ] Scope decided (per_farm vs aggregated) — no cross-farmer efficacy claims without real sample size
- [ ] Dashboard granularity agreed with Thaariha before building the response shape

## 12. Voice & accessibility — A/D

- [ ] `POST /voice/transcribe` + `/voice/synthesize` working in the demo language
- [ ] `spoken_summary` present on every consequential response
- [ ] High-contrast, icon-first, large targets, one-handed on a low-end Android
- [ ] Offline upload queue with per-item state — D, cut early if hours slip

## 13. Explicitly NOT in scope (guard against creep)

- [ ] FAO-56 irrigation planner — cut
- [ ] Boundary geometry / map sketching — cut
- [ ] Live government land or scheme integration — cut
- [ ] Numeric farm health score as the pitch centerpiece — reworked, not restored
- [ ] Grad-CAM heatmap — infeasible in 36h
- [ ] SMS fallback — infeasible in 36h
- [ ] Soil texture guide — conflicts with 3-field onboarding
- [ ] Cross-farmer efficacy comparisons — no sample size, violates no-fabrication
- [ ] Veteran voice network — adds a second human bottleneck

## 14. Checkpoint gates

- [ ] A (hr 2–6) — every name has a commit today, or their block gets reassigned on the spot
- [ ] B (hr 10) — core loop runs end to end on seed data before any side feature starts
- [ ] C (hr 16) — corpus is real with `distinguishing_cues`, or Suchit/Shruthi hand-write 5–6 docs
- [ ] D (hr 24) — land + scheme visibly working, even thin, or cut per the cut order
- [ ] Hour 29 — hard merge freeze
- [ ] Hours 32–36 — two timed rehearsals; the second clean run is the demo

## 15. Demo-day runbook

- [ ] Onboard by voice → 3 fields → `unrated`
- [ ] Diagnose above gate → cited 5-point advisory, "what to avoid" first → risk 82 → 73
- [ ] Diagnose below gate → gate object + alternatives + escalation, zero advice shown
- [ ] Follow-up `got_worse` → severity promotes → 57 → auto-escalate
- [ ] Agronomist opens case, resolves → risk recovers to 91
- [ ] Alert fires with non-empty inspection tasks
- [ ] Land submitted → officer verifies → scheme list unlocks
- [ ] Full script runs clean twice in a row on the demo box

## Cut order if the clock slips

Seasonal calendar → offline upload queue → scheme discovery → land/HITL → case PDF → veteran/novice toggle → health advisory → interim guidance card.

Never cut: confidence gate · gate object · "what to avoid" ordering · mandatory inspection tasks · the core loop.
