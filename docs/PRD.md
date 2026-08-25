# Bhoomi — Product Requirements Document

> **Status:** Reconstructed. The original `docs/PRD.md` file exists as a
> 0-byte stub in this repo's history — every other doc and every service
> module cites it ("PRD §5.6", "PRD §7.4", etc.), but the file itself was
> never committed. This document reassembles those requirements from every
> `PRD §x.y` citation across the codebase, `docs/API_CONTRACT.md`, and
> `README.md`, cross-checked against what's actually implemented. Section
> numbers match the citations exactly so existing code comments stay
> correct. Anywhere the implementation and a citation's apparent intent
> diverge, that's called out explicitly rather than silently resolved.

---

## §1. System Overview

Bhoomi is a voice-first, multimodal crop advisory system for smallholder
farmers, built around one governing rule: **the system answers only when it
can show its work, and hands off to a human otherwise.** It never
fabricates a confident-sounding answer to cover a gap in its knowledge or
its model's certainty.

### §1.4 — Degraded-mode behavior

Every external dependency (weather, LLM, embeddings, image diagnosis,
ASR/TTS, storage) is a typed port with a stub fallback. The system must
stay usable — offline-degraded, not dead — when a real integration is
unreachable or not yet built:

- No weather signal → the health engine's `environmental_risk` sub-index
  falls back to `ENVIRONMENTAL_RISK_DEFAULT` (70), not an error.
- No Postgres at all → repositories fall back to in-memory implementations
  (loses persistence and real retrieval, keeps the app booting).
- No asset yet uploaded → `StorageService` still returns valid presigned-URL
  metadata shapes.

### §1.5 — Adapter selection is config-only

No call site outside `adapters/dependencies.py` (or, for a handful of
migrated aggregates, `repositories/dependencies.py`) may import a concrete
adapter class directly. Every port is selected by a config flag
(`DIAGNOSIS_MODEL`, `LAND_API_MODE`, `EMBEDDING_PROVIDER`,
`ASR_PROVIDER`/`TTS_PROVIDER`) so flipping one env var changes behavior
everywhere for free, with zero code edits at any call site.

---

## §2. Roles, Access, and Non-Goals

### §2.2 — Land registry is a trust signal, not a government integration

Cadastral/land verification exists to build farmer trust and gate subsidy
eligibility — it is explicitly **not** a real integration with any state
land-records portal. `LAND_API_MODE=mock` accelerates a small whitelist of
survey numbers for demo purposes; `LAND_API_MODE=live` represents the real
(nonexistent) state portal and always falls through to human-in-the-loop
(HITL) officer review. Building a real government API integration is a
stated non-goal of this project.

### §2.3 — Authentication contract

**Specified:** farmers authenticate via phone number + OTP
(`POST /auth/otp/request`, `POST /auth/otp/verify`); officers and
agronomists authenticate via email + password. Every issued token carries a
role claim (farmer / officer / agronomist) that gates every downstream
route identically regardless of how the token was obtained.

**Implemented:** `POST /auth/otp/request` + `POST /auth/otp/verify`
(`services/otp_service.py`) now exist as spec'd, additively — the original
generic `POST /auth/register` / `POST /auth/login` (phone or email +
password) still work unchanged for every role, per this project's
zero-regression principle. No SMS gateway is configured anywhere in this
project, so the OTP is returned directly in the request response outside
`APP_ENV=production` rather than only delivered by SMS — see README.md §9
for that caveat and the in-memory OTP store's multi-worker limitation. The
role-claim JWT behavior downstream is unaffected either way — only the
credential-collection step ever differed from spec.

---

## §3. User Roles

| Role | Primary surface | Core actions |
|---|---|---|
| **Farmer** | `farmer_app` (Flutter) | Onboard a farm, diagnose crop photos, ask advisory questions by voice, check in on treatment follow-ups, view farm health score and timeline |
| **Revenue Officer** | `officer_portal` (React) | Review and approve/reject land-boundary verification submissions (HITL) |
| **KVK Agronomist** | `kvk_portal` (React) | Triage the escalation queue, resolve cases with an expert prescription |

The `User` model (contract §2.3) is a single table with a `role` enum
discriminator — not three separate identity systems.

---

## §5. Features

### §5.1 — Voice-first interaction with a mandatory safety net

Every consequential response carries a `spoken_summary` the client can read
aloud locally (thin-bandwidth concession — no server-side audio round
trip). Any voice-transcribed **numeric** field (area, dosage, dates) always
requires an explicit read-back confirmation (`confirmation.py`) before it's
trusted — a farmer confirms what the system understood, out loud, before it
acts on it. This is a hard rule, not a UX nicety: misheard numbers on a
farm-area or dosage field are exactly the kind of error that compounds
silently.

### §5.2 — Onboarding starts `unrated`, never a fake baseline

A newly onboarded farm has no monitoring history. Rather than defaulting
its health score to some neutral number, the score field stays `null` and
the band is `UNRATED` until real inputs (soil moisture, days since
planting, a scan) exist. `band_for(None)` returning `UNRATED` (§7.5) is the
enforcement point — a farm on day one must never look identical to a
declining one.

### §5.3 — Thin land verification (HITL)

A farmer submits a cadastral survey number. `LAND_API_MODE=mock` accepts a
small demo whitelist automatically; anything else — and everything under
`LAND_API_MODE=live` — queues for a Revenue Officer to review the submitted
boundary against the source imagery and approve/reject
(`land_service.py`, `officer_service.py`). Zero automated boundary
geometry validation; the officer's judgment is the whole point.

### §5.4 — FAO-56 irrigation resource planning

Given a crop, growth stage, and location, computes the daily crop water
requirement (`ET0 × Kc`) against actual irrigation delivered, producing a
resource plan and (indirectly) the health engine's irrigation-adequacy
signal. SIH25076-only — de-scoped under `PROBLEM_STATEMENT=sih26131`,
which narrows focus to disease/pest management. Reference crop-calendar
data is deliberately centralized in one pure module
(`domain/farm_reference_data.py`) rather than scattered.

### §5.6 — The confidence gate

The single decision point for answer-vs-escalate (`domain/gate/decide.py`).
Checked in order, first failure wins:

1. **Scope** — is the identified label inside the bounded, supported
   disease/pest set? Outside it → `OUT_OF_SCOPE_TARGET`.
2. **Image confidence** — at or above `CONFIDENCE_GATE` (disease, default
   0.70) or `PEST_CONFIDENCE_GATE` (pest, default 0.70, independently
   tunable)? Below → `BELOW_CONFIDENCE_GATE`.
3. **Retrieval relevance** — did the RAG retriever find grounded content
   above `RAG_RELEVANCE_THRESHOLD`? Below → `NO_RELEVANT_SOURCE`.

Pure, deterministic, no I/O — a judge or reviewer can point at this one
function instead of trusting a prompt. `target_type: "disease" | "pest"`
(SIH26131 delta spec §3.1) selects which scope list and confidence gate
apply to the same photo.

### §5.7/§5.8 — Grounded, cited 5-point advisory

Once the gate passes, the LLM composes an answer **strictly from retrieved
corpus chunks** — never from its own training-data knowledge of crop
disease. The fixed 5-point structure, in this exact order (frozen per
`contract_freeze_log.md`):

1. `possible_issue` — what it likely is, with confidence
2. `what_to_check` — how to confirm
3. `what_to_avoid` — common harmful mistakes (promoted ahead of next
   actions, per farmer-persona research: harm prevention first)
4. `what_to_do_next` — concrete action
5. `expert_triggers` — conditions under which to stop and escalate

Every point carries citations back to the specific corpus document(s) it
came from. If nothing in the corpus clears the relevance threshold, the
response is `retrieved: false` with an honest `no_relevant_source` reason
and an escalation offer — never a plausible-sounding guess.

### §5.9 — The living farm timeline

Every diagnosis, follow-up, escalation, and resolution is a timeline event
on the farm's case file (`timeline_service.py`). The farm is a continuous
record, not a series of disconnected one-off chatbot sessions — a
diagnosis today should be legible against last month's follow-up.

### §5.10 — Closed-loop follow-up

A farmer reports back on a diagnosed problem: `improved` / `no_change` /
`got_worse`. This demotes/leaves/promotes the problem's severity tier
respectively (§7.3), resets the monitoring-recency signal (a follow-up
photo is a fresh scan), and — for `got_worse` — always auto-escalates to
an agronomist. This is also the attribution point for Treatment Efficacy
Tracking (`docs/specs/treatment_efficacy_spec.md`): each check-in closes
out whichever treatment application is open on that problem.

### §5.11 — Agronomist escalation and resolution

Below-gate diagnoses, `got_worse` follow-ups, and stalled `no_change`
streaks all route to the next-available agronomist (roster-based, no real
officer-capacity model yet — §10 risk #10). The agronomist's case queue
shows a pre-compiled summary (symptoms, prior treatment, follow-up trend)
so resolution doesn't require re-deriving context from scratch. Resolving
a case clears the problem, marks the farm freshly monitored and
successfully treated, and recovers the health score — a farm that caught
and fixed a problem should read as *better understood*, not just
"back to normal."

### §5.12 — Government scheme discovery (SIH25076 only)

Matches a verified farm against a small curated list of subsidy schemes
(irrigation, seed, crop insurance) with explicit `last_verified` staleness
tracking. Gated on `land_status == verified` (§5.3) — an unverified farm
gets `409 LAND_NOT_VERIFIED`, not a scheme list it can't actually claim.
De-scoped under `sih26131`.

---

## §6/§7.4 — The worked walkthrough (the demo runbook)

The canonical end-to-end scenario every rehearsal and E2E test reproduces,
proving the health score isn't decorative:

**82 → 68 → 59 → 86**

1. **82** (good) — baseline, onboarded, no active problems.
2. **68** (watch) — an early bacterial leaf blight diagnosis opens a
   problem; `active_problem_severity` drops, monitoring/environmental
   nudge down too.
3. **59** (poor) — a `got_worse` follow-up promotes severity early→moderate
   and collapses `treatment_response`; the drop crosses the
   auto-escalation threshold.
4. **86** (good) — the agronomist resolves the case: the problem clears,
   and the farm now has a logged scan and a successful treatment, so
   `monitoring_recency` and `treatment_response` land *above* baseline.
   Ending above 82 is correct — a farm that caught and fixed a problem is
   better understood than one that never logged anything.

`scripts/seed_full_demo.py --stage full` and `tests/e2e/test_runbook.py`
both reproduce this. See `README.md` §9 for the current status of that
specific test (a scoring-assertion mismatch surfaced once the Alembic
migration conflict blocking it from running at all was fixed).

---

## §7. Health / Risk Score Model

### §7.1 — `unrated` is a real state, not a default

See §5.2. Enforced structurally: `score: int | None`, and `None` is never
silently coerced to 0 or any other numeric default.

### §7.2 — Sub-indices (live model, SIH26131)

Four sub-indices, each 0–100, combined by fixed weights summing to exactly
1.0 (`domain/health/constants.py`):

| # | Sub-index | Weight | Input |
|---|---|---|---|
| 1 | `active_problem_severity` | 0.40 | Open problems, penalized by severity |
| 2 | `environmental_risk` | 0.25 | Weather deviation from the crop's ideal band |
| 3 | `monitoring_recency` | 0.15 | Staleness of the last field scan |
| 4 | `treatment_response` | 0.20 | Latest follow-up trend / expert resolution |

(An earlier six-sub-index write-up — `environmental_suitability`,
`resource_adequacy`, `crop_stage_progression`, `active_problem_load`,
`monitoring_recency`, `treatment_response` — appears in some historical
docs/comments. It is **not** what the engine runs; treat any reference to
six sub-indices as describing a superseded design. See `README.md` §3.)

### §7.3 — Severity tiers and promotion/demotion

`early → moderate → severe`, each with a fixed penalty (30 / 55 / 80)
subtracted from `active_problem_severity`. A `got_worse` follow-up promotes
one tier; `improved` demotes one tier (or resolves outright from `early`);
`no_change` leaves severity untouched.

### §7.5 — Health bands

`unrated` (score is `null`) · 0–39 `critical` · 40–59 `poor` · 60–74
`watch` · 75–89 `good` · 90–100 `excellent`.

---

## §9. Known Gaps

Tracked in `README.md` §9 rather than duplicated here — that section is
the maintained, current-as-of-last-audit list (treatment efficacy status,
pest-diagnosis corpus coverage, embedding provider wiring, etc.) and is
kept in sync with the code; this PRD document is not.

---

## §10. Named Risks

**Risk #10 — no officer/agronomist capacity model.** Escalation routing
(§5.11) uses a static roster (`domain/kvk_directory.py`) and simple
next-available-by-open-case-count logic
(`services/kvk_routing.py`) — there's no real staffing-capacity or
availability schema yet. A production rollout at scale would need one
before routing decisions could reflect actual agronomist bandwidth.

---

## §12. Phase-2 Roadmap Notes

Explicitly deferred, not forgotten:

- **Widen crop/disease coverage** beyond the current reference-data table
  (`domain/farm_reference_data.py`) — today's crop-ideal-conditions and
  crop-calendar data covers a curated subset, not every crop the app
  nominally supports.
- **Per-crop growth-stage calendar refinement** for the FAO-56 resource
  planner (`domain/fao56.py`) — the current calculation doesn't yet adjust
  for stage-specific `Kc` curves beyond the base lookup.

### §13 — Crop reference data strategy

A curated per-crop lookup table (paddy, and a documented short list of
others) with a generic fallback for any crop name outside that table —
deliberately not a hardcoded single-crop assumption, so the system degrades
gracefully rather than erroring on an unlisted crop.

---

## Provenance

Every section above traces to a specific citation in the codebase or a
sibling doc (see the `grep -rn "PRD §"` output this document was built
from, in the connectivity-audit session that reconstructed it). If a
future PRD revision supersedes this reconstruction, update the citations
this file's structure mirrors — `services/api/app/**/*.py`,
`docs/API_CONTRACT.md`, `docs/specs/*.md` — or they'll point at stale
section numbers again.
