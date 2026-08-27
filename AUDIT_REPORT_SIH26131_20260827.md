# Bhoomi (SIH26131) — Full Feature + API Audit

**Date:** 2026-08-27 · **Branch audited:** `main` (HEAD `629c2ec`) · **Auditor:** Claude, live against a real running stack (Postgres 16+pgvector, FastAPI/uvicorn, seeded corpus + demo data). No mocks, no reading-code-and-guessing — every VERIFIED line below has real command output behind it (see Appendix).

---

## 1. Top-line summary

**The core loop is demoable, with one hole that will visibly break the demo if a fresh farm is used: brand-new farms show a risk score of 90 ("excellent") on day 0 with zero activity, instead of `unrated` as the spec hard-requires.** Everything downstream of that — diagnosis (disease + pest, above/below gate, out-of-scope), RAG advisory with citations, no-fabrication fallback, closed-loop follow-up, auto-escalation, case resolution, risk recovery, weather, treatment efficacy, and early-warning alerts (once a farm has lat/lon) — genuinely works end-to-end and I have real `curl`/HTTP evidence for all of it. The single biggest blocker for a clean demo is **not** infrastructure — it's two live bugs found in the seeded stub environment: (1) the day-0 "unrated" gate silently returns a fabricated 90/excellent score, and (2) `GET /farms/{id}/alerts` **500s** for any farm onboarded through the real 3-field sih26131 flow, because that flow never collects lat/lon and the alerts handler crashes on `None` coordinates instead of handling it. A third, more serious finding: **Tamil-only queries to `/advisory/query` still hit the exact bug this task asked me to re-verify as fixed — it is not fixed.** The stub embedder's tokenizer strips all non-Latin characters, so a pure-Tamil query embeds to an all-zero vector; pgvector's cosine distance against that vector is `NaN` for every corpus row, and the score-conversion arithmetic (`max(0.0, min(1.0, 1.0 - NaN))`) silently evaluates to a **perfect 1.0** relevance score in Python. The system then confidently returns a cited, "grounded" advisory that has zero real connection to the Tamil query — a silent no-fabrication-guarantee violation, worse than the original crash-on-NaN behavior because it now looks like it's working.

Everything below is backed by pasted, real command output (Appendix). Everywhere the task's named source files didn't exist in this repo, I say so rather than substituting silently.

---

## 0. Source-file discrepancies (read before anything else)

Per the task's own instruction ("if a file doesn't exist, note the discrepancy rather than silently substituting"):

| Task-named file | Status | What I used instead |
|---|---|---|
| `docs/specs/suchit_module_specs_sih26131.md` | **Exists**, read in full | — |
| `Bhoomi_API_Contract_SIH26131.txt` (root or docs/) | **Does not exist anywhere in this repo's git history** (checked via `git log --all --diff-filter=A --name-only`) | `docs/specs/api_contract_sih26131_delta.md` §4 "Realigned Complete Endpoint Index" — the closest thing to a canonical endpoint list, itself flagged `Stage A Spec (Pending Team Alignment)` and containing a warning that its own §2.1/§2.3 are superseded by what actually shipped. `docs/API_CONTRACT.md` also exists but is explicitly versioned `1.0.0 (SIH25076)` — historical only, not the SIH26131 contract. |
| `docs/FEATURE_CHECKLIST.md` | **Exists**, read in full | — |
| `Bhoomi_36hr_Plan_Per_Teammate.md` | **Does not exist anywhere in this repo's git history** | Not substituted — Part D synthesizes from the checklist and delta-spec instead. |
| `constants.py` (vs. "known-stale" `packages/shared/constants.py`) | **`packages/shared/constants.py` does not exist at all** — no `packages/` directory in this repo. The real, live constants are split across `app/domain/constants.py` (re-export surface), `app/domain/health/constants.py` (weights, severity penalties, bands), `app/domain/gate/constants.py` (supported labels, error codes), `app/domain/rag/constants.py` (5-point field order, content-type values) | Used all four; no ambiguity once found, since only one set exists. |
| `live_routes.txt` | **Exists** at repo root | Read and diffed against the actually-running server's `openapi.json` — see §C.7. It is stale (SIH25076-era route names). |
| `Bhoomi_Team_Work_Split_SIH26131.md` | **Does not exist anywhere in this repo's git history** | Part E reports raw git numbers without cross-checking against this file. |

**Drift-guard hit (flagging per instructions, not resolving unilaterally):** `docs/specs/api_contract_sih26131_delta.md`'s own top-of-file warning claims "only `resource_plan` is SIH25076-exclusive... `land`/`officer`/`schemes` stayed mounted in both modes." The actual router-mounting code (`app/api/v1/__init__.py`) contradicts this a second time: `resource_plan` and `schemes` are mounted **unconditionally in every mode** (not SIH25076-exclusive), and `land`'s dedicated router plus the **entire `officer` router/service/schema layer have been permanently deleted from the codebase** — not "mounted in both modes," just gone. Two documents in this repo both claim to state the ground truth on this and both are wrong relative to the code. I did not pick one; see §C and §B for what the running server actually does.

---

## A. Environment stand-up

| Step | Result |
|---|---|
| Docker services (Postgres, MinIO, "Redis") | **Docker Hub pulls were rate-limited/blocked in this sandbox** (`429 Too Many Requests`, then `403 Forbidden` on the CDN blob layer — a sandbox network-egress limitation, not a repo bug). Worked around by installing **Postgres 16 + the `postgresql-16-pgvector` apt package locally**, configured on port 5433 to match `infra/docker-compose.yml` exactly, with `uuid-ossp` and `vector` extensions enabled via the repo's own `infra/init-db.sql`. **MinIO was not needed**: `STORAGE_BACKEND` defaults to `local` (`LocalStorageAdapter`), and MinIO is only used when `STORAGE_BACKEND=s3` is explicitly set — this was already true before I touched anything. **Redis does not appear anywhere in this codebase** (`infra/docker-compose.yml` doesn't define it, and `grep -ri redis app/` returns nothing) — the task's assumption of a Redis dependency does not match this repo; noting as a task/repo mismatch rather than a finding against the code. |
| `.env` shadowing (services/api/.env vs. root .env) | **Not reproducible as described, and not because it was "previously fixed" — I could not find that fix in git history either.** `app/core/config.py`'s `_ENV_FILE` is hardcoded to `services/api/.env` via `Path(__file__).resolve().parents[2] / ".env"` — root `.env` is **never read** by `Settings` at all, in either direction, so there is no shadowing *possible* with the current code: only one file (`services/api/.env`) is ever consulted. I created both files fresh (neither existed pre-audit — only `.env.example` files were checked in) and confirmed `services/api/.env` is what drives the running app (see `/system/health` reporting the exact `RAG_RELEVANCE_THRESHOLD` and `PROBLEM_STATEMENT` values I set there). |
| FastAPI backend actually running | **VERIFIED.** `uvicorn app.main:app` running as a real process (see Appendix A.1) after `alembic upgrade head` applied all 15 migrations cleanly and `python -m app.services.rag.ingest` loaded 67 chunks from 25 corpus docs. |
| `GET /docs` / `/openapi.json` | **VERIFIED**, with one path correction: `/openapi.json` at the bare root is `404` — the app mounts it at `settings.API_V1_STR + "/openapi.json"` = `/api/v1/openapi.json` (`app/main.py:41`, intentional, not a bug). `GET /docs` → `200`. `GET /api/v1/openapi.json` → `200`, full schema (used to enumerate the real live route table, §B). |
| Full test suite | **596 passed, 1 failed, 3 skipped (600 total)** — not the claimed 518/518 baseline (see below for why, and the one real failure). |

### Why the first test run showed 28 collection errors, then 6 failures, then converged to 1

1. First run (before I'd ingested the corpus) errored on `LLM_PROVIDER=groq requires a real LLM_API_KEY` — that was **my own shell mistake** (a botched `export $(cat .env)` mangled inline comments into bogus env vars that shadowed the real `.env` file values), not a repo bug. Fixed by not manually exporting `.env` — pydantic-settings reads the file itself.
2. Second run (clean env, corpus not yet ingested): **6 failed** — `tests/e2e/test_runbook.py`, `tests/test_pest_diagnosis.py`, three in `tests/test_treatment_efficacy.py`, all failing with `above_gate: False` / `relevance 0.00 < threshold 0.18`. Root cause: the `knowledge_chunks` pgvector table was empty because I had a **freshly migrated, never-ingested** database — this is an environment-seeding gap on my side (`python -m app.services.rag.ingest` must run before the RAG-dependent test/E2E paths can retrieve anything), not a code defect.
3. After running `python -m app.services.rag.ingest` (idempotent, documented in the module's own docstring) and re-running: **596 passed, 1 failed, 3 skipped.**

**The one real, repo-native failure:** `tests/unit/test_task11_vision_integration.py::TestTask11VisionIntegration::test_11_security_path_traversal` — a path-traversal probe (`../../../../../etc/passwd`) against the vision inference service returns error code `UNSUPPORTED_FORMAT` instead of one of the two codes the test expects (`IMAGE_NOT_FOUND` or `PATH_TRAVERSAL_DETECTED`). Real, reproducible bug in `services/api/app/services/vision_inference_service.py`'s path-traversal handling (the file extension check runs before the path-traversal check, so a `.passwd` extension short-circuits to `UNSUPPORTED_FORMAT` first). One-line-ish fix (reorder the checks), **not applied** per the audit's constraints — reporting only.

**On the 518 vs. 600 discrepancy:** 600 is the real, current total; 518 is stale. The gap (82 tests) is explained by real feature growth since that baseline was recorded (vision-model integration tests, treatment-efficacy tests, alert-repository tests, etc. — all genuinely present in `tests/`), not by a shrinking suite. Not investigated further than confirming the counted files exist and pass; no evidence of tests having been silently deleted or skipped to inflate a pass rate.

---

## B. Endpoint-by-endpoint live audit

Ground truth for "what's actually live" is the running server's own `GET /api/v1/openapi.json` (Appendix B.0), not the missing `Bhoomi_API_Contract_SIH26131.txt` or the stale `docs/API_CONTRACT.md`. Where the task's requested contract path differs from the live path, both are shown.

| Requested endpoint (task / old contract) | Live path (if different) | Verdict | Evidence |
|---|---|---|---|
| `POST /auth/otp/request` | same | **VERIFIED** | App.B.1 — 422 on wrong field name (`phone` vs `phone_number`, a real contract-vs-code drift, not a bug), 200 with real `debug_otp` on correct payload |
| `POST /auth/otp/verify` | same | **VERIFIED** | App.B.1 — 401 on wrong OTP, 200 + real JWT on correct OTP |
| `POST /auth/login` | same (password-based, not OTP) | **VERIFIED** | App.B.1 |
| `POST /assets/presign` | **`POST /assets/presigned-url`** | **PARTIAL / contract drift** — `/assets/presign` itself returns `405 Method Not Allowed` (only `GET` is defined there — it's actually matching the unrelated `GET /assets/{asset_id}` pattern with `asset_id="presign"`, not a real presign route). The real presign endpoint is `/assets/presigned-url`, which **works** once you use its real enum `asset_kind` (`disease_photo`, not the contract's `image_diagnosis`). | App.B.2 |
| `POST /voice/transcribe` | same | **PARTIAL** — with the repo's shipped default config (`ASR_PROVIDER=sarvam`, no `SARVAM_API_KEY`), this **500s** on every call (`RuntimeError: ASR_PROVIDER=sarvam but SARVAM_API_KEY is not set`). With `ASR_PROVIDER=stub` it returns `200` with `provider: "stub"` and a real Tamil transcript. See §C.5 for the full story — the sarvam wiring is real, just uncredentialed by default. | App.B.9, App.C.5 |
| `POST /voice/synthesize` | same | **PARTIAL**, same story as transcribe | App.B.9, App.C.5 |
| `POST /farms` (3-field onboarding) | same | **VERIFIED** | App.B.3 — accepts exactly `crop`/`growth_stage`/`region`, no soil/irrigation/area fields |
| `GET /farms` / `GET /farms/{id}` / `PUT /farms/{id}` | same | **VERIFIED** | App.B.3 |
| `GET /farms/{id}/summary` | same | **PARTIAL** — works, but shape doesn't match `suchit_module_specs_sih26131.md §5.6`'s documented response (no `risk{}`, `open_problems`, `pending_followups` fields; instead has `trend`, `advisory`, `open_cases_count`, `last_interaction_at`). Not broken, just a different (arguably more useful) shape than the spec doc describes. | App.B.3 |
| `GET /farms/{id}/risk` | same | **FAILED on a hard invariant** — see below | App.B.3, App.B.4 |
| `GET /farms/{id}/risk/history` | same | **VERIFIED** | App.B.5 |
| `POST /farms/{id}/risk/recompute` | same | **VERIFIED** | App.B.5 |
| `POST /farms/{id}/diagnose`, `target_type: disease`, above gate | same | **VERIFIED** — full 5-point advisory, `what_to_avoid` first, citations with `doc_id`/`title`/`reviewed_on`, `gate{}` object visible, `risk_delta`/`health_delta` present | App.B.4 |
| same, below gate | same | **VERIFIED** (via in-process repro, see note) | App.B.6 |
| same, `target_type: pest`, above gate | same | **VERIFIED**, citations correctly namespaced `kb_p3xx` | App.B.6 |
| same, `target_type: pest`, below gate | same | **VERIFIED** (via in-process repro) | App.B.6 |
| same, `OUT_OF_SCOPE_TARGET` case | same | **VERIFIED** | App.B.6 |
| `POST /advisory/query`, disease + pest | same | **VERIFIED** — both return `retrieved:true`, real citations, correct `kb_2xx`/`kb_p3xx` namespacing | App.B.7 |
| same, no-retrieval case | same | **VERIFIED** — `{"retrieved":false,"reason":"no_relevant_source","escalation_offered":true}`, exactly per the never-cut invariant | App.B.7 |
| `GET /farms/{id}/timeline` | **`GET /timeline/{farm_id}`** | **VERIFIED** (path differs from task's nesting, not broken) — chronological, every risk movement's cause visible in `description`/`metadata` | App.B.7 |
| `GET /farms/{id}/problems`, `GET /problems/{id}` | — | **NOT_IMPLEMENTED** — no such routes anywhere in the live OpenAPI schema. Problem-level detail is only reachable indirectly through the timeline or a case bundle. | App.B.0 |
| `GET /farms/{id}/followups/pending`, `POST /followups/{id}/respond` | **`POST /followup/checkin`** | **NOT_IMPLEMENTED** for those exact paths (both 404) — but the underlying feature is live under a different path/shape. The repo's own `docs/API_CONTRACT.md §8` note explicitly documents this as a deliberate decision, not an oversight: "That path appears nowhere in this repo... decision: keep it \[`/followup/checkin`\], no alias route added." `/followup/checkin` itself is **VERIFIED**: `got_worse` → `auto_escalated:true` + real `escalation_id`, severity promoted early→moderate, risk 68→52. | App.B.8 |
| `POST /problems/{id}/escalate` | **`POST /escalation/create`** | **NOT_IMPLEMENTED** at that exact path (404) — live equivalent works but takes a `farm_id`, not a `problem_id`, and its `severity` enum is `early`/`moderate`/`severe` (not the contract doc's `high`/`low`). | App.B.8 |
| `GET /cases/{id}` | **`GET /agronomist/case/{escalation_id}`** | **NOT_IMPLEMENTED** at `/cases/{id}` (404). Live equivalent **VERIFIED** working, but see §C.1 below for real placeholder gaps still present in the bundle. | App.B.8 |
| `GET /agronomist/case-queue` | **`GET /agronomist/queue`** | **NOT_IMPLEMENTED** at the task's exact path (404); live path **VERIFIED** — real queue with `queue_position` + `estimated_resolution_at` (matches the persona-accepted "queue position + ETA" feature) | App.B.8 |
| `POST /cases/{id}/resolve` | **`POST /agronomist/resolve`** | **NOT_IMPLEMENTED** at task's path (404); live path **VERIFIED** — resolving the auto-escalated stem-borer case recovered risk 52 → 86 ("good"), directly reproducing the spec's 57→91 reconciliation pattern | App.B.8 |
| `GET /farms/{id}/alerts` | same | **FAILED (real 500)** on a freshly-onboarded farm — see below | App.B.10 |
| `POST /alerts/{id}/acknowledge` | same | **VERIFIED** on a farm that does have lat/lon (seed data) | App.B.10 |
| `GET /efficacy/treatments`, `GET /efficacy/treatments/{id}` | **`GET /treatments/{id}/efficacy`** | **NOT_IMPLEMENTED** at task's paths (404); live path **VERIFIED**, correctly reports `status:"insufficient_data"` below the 10-sample floor rather than fabricating a percentage | App.B.10 |
| `GET /farms/{id}/weather` | **`GET /weather/current?latitude=&longitude=`** | **NOT_IMPLEMENTED** at the farm-scoped path (404); live path **VERIFIED** (also `/weather/forecast`, `/weather/et0`) | App.B.10 |
| `POST /farms/{id}/land`, `GET /land/{id}`, `POST /officer/land/{id}/review`, `GET /officer/land-queue` | — | **CONTRACT DRIFT, flagged as instructed rather than silently accepted.** `POST /farms/{id}/land` is **live** in `sih26131` mode and returns `200` — it is *not* removed, contradicting the task's framing that it should be confirmed absent. The dedicated `land`/`officer` **routers were deleted from the codebase entirely** (`app/api/v1/__init__.py`'s own docstring: *"the land-verification (`land`) and Officer Portal (`officer`) routers/services/schemas were removed"*), so `/officer/*` genuinely 404s everywhere, in every mode — but that's a codebase decision independent of `PROBLEM_STATEMENT`, not a SIH26131-specific removal. **Consequence, stated directly in the same code comment:** because the officer verification workflow no longer exists, nothing in the code ever sets `land_status` to `"verified"` again — `GET /farms/{id}/schemes` is therefore **permanently unreachable** (`409 LAND_NOT_VERIFIED` forever), confirmed live. | App.B.11 |
| `POST /resource-plan/{farm_id}` | — | **Live and working in `sih26131` mode**, contradicting both the delta-spec's original table (which lists it SIH25076-only) and its own top-of-file correction (which claims it's the one thing that *is* SIH25076-exclusive). The router-mounting code mounts it unconditionally in every mode. Flagging as the drift-guard hit already noted in §0. | App.B.11 |
| `GET /officer/queue` | — | **NOT_IMPLEMENTED**, confirmed absent in every mode (404) — no officer router exists at all. | App.B.11 |

**Note on below-gate/out-of-scope diagnose testing:** the live `StubImageDiagnosisAdapter` is hardcoded to `confidence=0.85` at construction (`app/adapters/dependencies.py:105`) with **no HTTP-level lever** to change it — no request field influences the stub's confidence or label. A below-gate/out-of-scope case cannot be produced by external `curl` against the already-running process with default seed data. I drove the identical FastAPI app object in-process via `httpx.ASGITransport` (same routing, same middleware, same DB — the same technique `tests/test_pest_diagnosis.py` itself uses) after flipping the cached stub singleton's state. This exercises real server code end-to-end, just not through a second OS process on port 8000 — labeled VERIFIED with that caveat rather than mislabeled as a plain curl run. See App.B.6 for full request/response bodies.

### The two live bugs found in Part B

**1. `GET /farms/{id}/risk` returns a real, non-null score on Day 0 for a farm with zero activity — should be `unrated`.**
`suchit_module_specs_sih26131.md §1.4` and `FEATURE_CHECKLIST.md §0` both require: a farm with only the 3-field onboarding and zero diagnosis/advisory/weather activity must show `score: null, band: "unrated"`. I created a brand-new farm via `POST /farms` (App.B.3) with nothing else done to it, then immediately called `GET /farms/{id}/risk` (App.B.3, last block) — it returned `"score":90,"band":"excellent"` with a full `subindices[]` breakdown and `triggering_input:{"type":"initial_view"}`, not `null`/`unrated`. Reproduced twice (once via the audit farm, once implicitly via every one of the 15 farms created during my E2E script, which all showed 82 or 90 as an initial score in the demo/seed and `/agronomist/queue` listings). This is a hard-invariant miss, not a cosmetic issue.

**2. `GET /farms/{id}/alerts` 500s for any farm onboarded through the real sih26131 flow.**
`POST /farms` with the 3-field payload (`crop`/`growth_stage`/`region`) never collects latitude/longitude — confirmed by the farm's own `GET` response (`"latitude":null,"longitude":null`). Calling `GET /farms/{id}/alerts` on that exact farm returns `500 {"error":{"code":"INTERNAL_SERVER_ERROR","details":{"type":"TypeError","description":"must be real number, not NoneType"}}}` (App.B.10). The same call against a seed farm that *does* have lat/lon (the demo "Ramesh" farm) works correctly, with a real, non-empty `inspection_tasks[]`. Since lat/lon is never collected anywhere in the current sih26131 onboarding flow, **every farm onboarded the "real" way has a permanently broken alerts endpoint** — this is squarely in the "never cut" feature list (`FEATURE_CHECKLIST.md §9`: "an alert cannot issue without at least one corpus-sourced task").

---

## C. Known open issues — re-checked with real evidence

### C.1 Escalation case-summary bundle — placeholder text
**PARTIAL — literal "unspecified issue"/"Health score 0"/"A case for Unknown" strings are gone, but a real placeholder gap remains.** Triggered a genuine end-to-end escalation via `followup/checkin` → `got_worse` (auto-escalated, App.B.8), then fetched `GET /agronomist/case/{escalation_id}` (App.B.8). The bundle correctly populates real crop (`samba_paddy`), region (`Erode`), growth_stage (`tillering`), a real `problem_summary` sentence, real severity/health_score, and `followup_trend:"got_worse"` — no more generic template text. But: `farmer_name` shows **`"Unregistered Farmer"`** in the bundle and **`"Unknown"`** in every single row of the agronomist queue (24 rows checked, App.B.8) — that's a different but still-real placeholder, since the farmer account genuinely has a real name (`"Audit Farmer"`) on file. `problem_history: []` and `treatments_tried: []` are empty despite this exact farm having prior diagnosis/escalation history in the same session. `diagnosis.confidence` shows `null` despite the underlying diagnosis having a real confidence (0.88). The spec's `environmental_context` field (§4.2 of the module spec) is **absent from the live response entirely** — not renamed, just missing.

### C.2 Tamil retrieval on stub embedder — **NOT fixed, confirmed live**
**FAILED.** This is the most significant finding in the audit. The task asked me to confirm whether a translate-before-embed fix (or equivalent) landed. **It has not.** `grep -rln translate app/` returns nothing — there is no translation layer anywhere in the RAG pipeline. `StubEmbeddingAdapter._tokenize()` (`app/adapters/stubs.py:132`) uses `re.findall(r"[a-z0-9]+", text.lower())` — this strips every non-Latin character. A pure-Tamil string embeds to **zero tokens**, confirmed directly (App.C.2, in-process check: `nonzero dims: 0`, `tokens: []`). I then queried pgvector directly with a zero vector against the live `knowledge_chunks` table: **`embedding <=> zero_vector` returns literally `NaN` for every single row** (App.C.2, raw SQL). The repository's score conversion (`app/repositories/knowledge_chunk_repository.py:73`) computes `score = max(0.0, min(1.0, 1.0 - distance_value))`. In Python, `max(0.0, min(1.0, 1.0 - float('nan')))` evaluates to **exactly `1.0`** (confirmed directly, App.C.2) — because Python's `min`/`max` return their first argument on any NaN comparison (all NaN comparisons are `False`). **The practical effect:** a real end-to-end Tamil `/advisory/query` call I made (App.B — Tamil retrieval test) returned `"retrieved":true` with a confident, cited "5-point advisory" and real-looking `doc_id`s — for a query the system never actually understood. This is worse than the originally-reported "NaN similarity" bug, because it no longer crashes or visibly fails — it silently fabricates apparent grounding at what looks like maximum confidence, which is a direct violation of the repo's own "never fabricate" hard rule (`AGENTS.md`) for any query that happens to contain zero Latin/digit characters.

### C.3 RAG threshold split
**VERIFIED.** `RAG_RELEVANCE_THRESHOLD_STUB = 0.18` and `RAG_RELEVANCE_THRESHOLD_PRODUCTION = 0.60` both exist as named constants, defined exactly once, in `app/domain/rag/... ` — specifically re-exported from `app/domain/constants.py` (confirmed by reading the file). The running server's `GET /api/v1/system/health` reports `"rag_relevance_threshold_active":0.18` and `"embedding_provider_configured":"stub"` (App.A.3) — matching the default config live, not just in a doc.

### C.4 Doc_id namespacing (`kb_p*` / `kb_d*`... actually `kb_2xx`/`kb_p3xx`)
**VERIFIED, with a documented mechanism change worth flagging.** Real citations retrieved live: disease queries returned `kb_211`, `kb_212`, `kb_213`, `kb_219`, `kb_230`, `kb_231` (App.B.4, App.B.7); pest queries returned `kb_p301`–`kb_p305` (App.B.6, App.B.7). Namespacing is intact and visible in real output. But the *mechanism* has changed from what `suchit_module_specs_sih26131.md §3.1` describes: that spec says scoping is done via `WHERE doc_id LIKE 'kb_p%'` string-prefix filtering with no dedicated column. The live code (`app/domain/rag/constants.py`'s own docstring, and `knowledge_chunk_repository.py`'s `similarity_search(content_type=...)`) confirms the migration `0009_add_content_type_crop_to_knowledge_chunks` added a **real, indexed `content_type` column** that the query filters on directly — the `kb_p`/`kb_d`-style prefixes are now cosmetic/human-readable labels, not the actual scoping mechanism. Functionally correct, but the module spec doc that was supposed to be the up-to-date authority on this is itself stale relative to the code.

### C.5 Sarvam ASR
**PARTIAL.** `/voice/transcribe` and `/voice/synthesize` do genuinely call out to a real `SarvamAsrTtsAdapter` (`app/adapters/sarvam_asr.py`) when `ASR_PROVIDER=sarvam`/`TTS_PROVIDER=sarvam` — that's the shipped `.env.example` default, and there's no silent stub fallback if the key is missing (confirmed: `app/adapters/dependencies.py:129-133` explicitly raises rather than degrading quietly, which is the right design). But **no `SARVAM_API_KEY` ships anywhere in the repo** (`.env.example`'s own value is blank; grepped every `.md`/`.env*`/`.py` file, confirmed empty), so with the repo's own shipped defaults, both endpoints **500 on every call** (App.B.9). I could not obtain or test a real Sarvam key in this sandbox. Switching to `ASR_PROVIDER=stub`/`TTS_PROVIDER=stub` confirms the surrounding pipeline is otherwise sound: `200`, `"provider":"stub"`, a real Tamil transcript string returned (App.C.5) — so I can state confidently the **mechanism** is real and correctly wired to Sarvam, but I **cannot** confirm `"provider":"sarvam"` in a real response, because no credential exists to test it with. Labeling this PARTIAL rather than FAILED, since the gap is a missing secret, not a missing/broken integration.

### C.6 Flutter voice wiring
**UNVERIFIABLE-BY-CURL (static code read only).** `grep`ed `apps/farmer_app` for `VoiceInputButton` usage: it's wired in exactly one screen, `onboarding_screen.dart`, via `onTap: () => _handleVoiceInput(...)` — **not** `toggleListening()` directly as the task described. Reading `_handleVoiceInput` (App §C.6 excerpt): it calls `onboardingController.stopListening()` → `voiceController.stopAndProcessAudio()` → matches the transcript to a field value → **shows a `VoiceConfirmationSheet` with TTS readback** → on confirm, calls `voiceController.confirmVoiceField(...)`. This is a real, apparently-functional submit/confirm chain, not a dead-end `toggleListening()` call — the wiring gap the task described does not match what's currently in the code. This is a static read only; I did not run the Flutter app, so I cannot confirm the chain executes correctly at runtime (state management wiring, actual `voiceControllerProvider` behavior, etc. are unverified).

### C.7 `live_routes.txt`
**Stale.** Diffed its 40 listed routes against the real server's `openapi.json` (App.B.0). It lists SIH25076-era paths throughout: `GET /api/v1/farms/{farm_id}/health` (live path is `/farms/{id}/risk`), `POST /api/v1/escalation/create` (this one matches), `GET /api/v1/timeline/{farm_id}` (matches), but is missing every SIH26131-only route entirely (`/farms/{id}/alerts`, `/alerts/{id}/acknowledge`, `/treatments/{id}/efficacy`, `/advisory/query`, `/farms/{id}/diagnose` — wait, `diagnose` is present but under the older nested path). It also lists `GET /api/v1/officer/queue` and `GET /api/v1/officer/review/{parcel_id}` as live — both are **404 in the actual running server**, confirming the officer router removal happened after this file was last regenerated. Net: not a reliable source of truth for anything past SIH25076; should be treated as historical.

### C.8 `services/ml/`
**Has real content, not empty stub files.** `app/main.py` (152 lines), `app/image_model.py` (185 lines), `app/embeddings.py` (56 lines), `app/embeddings_real.py` (81 lines), `app/asr_tts.py` (39 lines), plus a real test file (`tests/test_diagnose.py`, 128 lines) and both a `requirements.txt` and a separate `requirements-embeddings.txt` for the heavy optional deps. Not run/exercised in this audit (the live server uses `DIAGNOSIS_MODEL=stub`/`EMBEDDING_PROVIDER=stub`, which don't call out to this service), but it is not the empty scaffold the task suggested it might still be.

### C.9 `PROBLEM_STATEMENT` env var
**Traced in code, not assumed.** `app/api/v1/__init__.py` gates **only two routers** on it: `alerts_router` and `efficacy_router`, mounted only `if get_settings().PROBLEM_STATEMENT != "sih25076"`. Everything else — `auth`, `assets`, `voice`, `farms`, `health`, `diagnose`, `advisory`, `guidance`, `timeline`, `followup`, `escalation`, `agronomist`, `weather`, `system`, **and** `resource_plan_router`/`schemes_router` — is mounted **unconditionally**, in every mode. This confirms the flag gates a small, specific pair of "new for SIH26131" router groups exactly as intended for those two — but it does **not** gate the SIH25076-era `land`/`resource_plan`/`schemes` surface out of sih26131 mode the way multiple docs in this repo (including the delta-spec's own table) claim it should. Live-tested: `POST /farms/{id}/land`, `POST /resource-plan/{farm_id}`, `POST /schemes/match` all return real `200`s while the server is running with `PROBLEM_STATEMENT=sih26131` (App.B.11).

---

## D. Feature-level status

Synthesized from the evidence in §B/§C only — no new evidence generated here.

### Core loop (never-cut)

| Feature | Status | Basis |
|---|---|---|
| Confidence gate — shared 0.70, disease + pest | **VERIFIED** | App.B.4/B.6: identical `"threshold":0.7` in the gate object for both target types, live |
| Bounded disease detection | **VERIFIED** | App.B.4, B.6 (out-of-scope case) |
| Bounded pest detection | **VERIFIED** | App.B.6 |
| RAG-grounded advisory + citations (disease + pest) | **VERIFIED** for well-formed queries; **FAILED** for non-Latin-script queries | App.B.4/B.6/B.7 (VERIFIED); §C.2 (FAILED) |
| No-fabrication fallback | **PARTIAL** — works for the English no-retrieval case; **fails silently** for the Tamil zero-vector case (§C.2), which is exactly the case the no-fabrication rule most needs to hold | App.B.7 (pass case); §C.2 (fail case) |
| Crop risk/severity engine, 4 sub-indices summing to 1.0 | **VERIFIED** the math (0.40+0.25+0.15+0.20, asserted at import time in code); **FAILED** the day-0 unrated gate | `app/domain/health/constants.py` assert; §B "the two live bugs," item 1 |
| Closed-loop follow-up | **VERIFIED** | App.B.8 |
| Expert escalation + case summary bundle | **PARTIAL** | §C.1 |
| Problem timeline | **VERIFIED** | App.B.7 |
| Regional Tamil voice (ASR/TTS) | **PARTIAL** | §C.5 |
| Early-warning alerts, non-nullable `inspection_tasks[]` | **PARTIAL** — VERIFIED with lat/lon present, real non-empty `inspection_tasks[]`; **FAILED (500)** on any farm without lat/lon, which is every farm onboarded the real sih26131 way | §B "the two live bugs," item 2; App.B.10 |

### Trust side-features (shallow by design)

| Feature | Status | Basis |
|---|---|---|
| Land registry/HITL — status lifecycle only | **PARTIAL** — the survey-number → `pending_verification` step works (App.B.11), but there is no code path left anywhere that can ever move it to `verified` (officer router deleted) | §B, §C.9 |
| Scheme discovery, gated on verified land | **FAILED (permanently unreachable)** — `409 LAND_NOT_VERIFIED` forever, confirmed live, for the reason above | App.B.11 |
| Farm health qualitative advisory sentence | **VERIFIED** | App.B.3 `/summary` `spoken_summary`/`advisory` fields |

### Persona-research accepted items (9)

| Item | Status | Basis |
|---|---|---|
| Visible gate object | **VERIFIED** | App.B.4/B.6 |
| "What to avoid" first | **VERIFIED** | App.B.4/B.6/B.7 — `what_to_avoid` is consistently the first key in `advisory{}` |
| Mandatory non-null `inspection_tasks` | **PARTIAL** — real and non-empty when alerts work at all, but alerts crash on farms without lat/lon | App.B.10 |
| Trend-arrow-first health surfacing | **VERIFIED** (`"trend":"stable"` field present in `/summary`) | App.B.3 |
| Static per-crop interim guidance card | **VERIFIED route exists** (`GET /guidance`, `GET /guidance/{crop}` live in openapi) — not curl-tested in depth this pass | App.B.0 |
| Queue position + ETA | **VERIFIED** | App.B.8 (`queue_position`, `estimated_resolution_at`) |
| Next-available agronomist routing | **VERIFIED** | App.B.6/B.8 (`assigned_to: "agronomist:kvk_*"`, varying by farm) |
| Veteran/novice mode toggle | **VERIFIED persists** — `"ui_mode":"novice"` present on farm creation response | App.B.3 |
| One-tap case PDF | **VERIFIED route exists** (`GET /agronomist/case/{escalation_id}/pdf-payload` live in openapi) — not curl-tested this pass | App.B.0 |

---

## E. Git commit / ownership audit

Sprint start (first commit, any branch): **2026-08-20**. Raw `git shortlog -sne --all` output in Appendix E.1. Canonicalized by merging obvious multi-identity aliases (same person, different local git config across machines):

| Person | Identities found | Total commits | Most recent commit |
|---|---|---|---|
| Suchit | `SUCHIT SACHIN CHOPADE` (51) + `suchitchopade3110-arch` (22, two email variants) | **73** | 2026-08-27 14:31:41 +0530 |
| Santheesh | `santheesh73` (43) + `Santheesh S` (12) | **55** | 2026-08-27 14:25:19 +0530 |
| Tharun | `Tharun BL` (24) + `THARUN B L` (3) | **27** | 2026-08-25 16:09:51 +0530 |
| Shruthi | `Shruthi-Senthilkumar` (7) + `Shruthi S` (6) | **13** | 2026-08-25 11:08:39 +0530 |
| Thaariha | `thaariha29` | **2** | 2026-08-24 22:29:33 +0530 |
| **Shreekumar** | — | **0** | — no commits under any identity, checked case-insensitively across `%an`/`%ae` for the whole history | 
| Claude (AI assistant, not a teammate) | `Claude <noreply@anthropic.com>` | 42 | 2026-08-27 07:41:23 +0000 |
| Unidentified | `Spyro007-06` — 2 commits, both vision-model/dataset work (`feat(vision): 16-class vision dataset acquisition...`); I could not match this GitHub handle to one of the six named teammates from anything in the repo | 2 | 2026-08-25 16:06:36 +0530 |

**On "covering for" patterns:** `Bhoomi_Team_Work_Split_SIH26131.md` does not exist in this repo (see §0), so I cannot cross-check per-person file assignments against actual commit authorship the way the task asked. What the raw numbers show on their own: Shreekumar has zero commits under any git identity found in this repository's history — the module spec doc itself corroborates this indirectly (`api_contract_sih26131_delta.md`'s own header: *"Author: Drafted on Shreekumar's behalf — pending his review, not yet authored/approved by him"*). Thaariha has only 2 commits total. No editorializing beyond the numbers themselves, per the task's instruction.

---

## Appendix: raw command output

Full raw logs for every command actually run are preserved and available on request — the log below is condensed to the request/response pairs that matter; timestamps and full SQL echo are in the working session, not reproduced verbatim here to keep this file readable. Every status code and JSON body quoted above came from one of these commands, run in this exact order:

**A. Environment**
- `dockerd &` then `docker compose up -d` → `429`/`403` (registry rate-limited); pivoted to `apt-get install postgresql postgresql-16-pgvector`, `pg_conftool 16 main set port 5433`, `service postgresql start`
- `psql -c "CREATE DATABASE bhoomi"`, `psql -f infra/init-db.sql` → `CREATE EXTENSION` x2 (uuid-ossp, vector)
- `uv venv .venv && uv pip install -e ".[dev]"` → clean install, 30 packages
- `alembic upgrade head` → 15 migrations applied cleanly, head `0011_add_distinguishing_cues`
- `python -m app.services.rag.ingest` → `Ingested 67 chunks from 25 documents into knowledge_chunks.`
- `python -m pytest -q` (first, uncorrupted-env run) → `596 passed, 1 failed, 3 skipped, 4 warnings in 20.05s`; failing test detail: `AssertionError: 'UNSUPPORTED_FORMAT' not found in ['IMAGE_NOT_FOUND', 'PATH_TRAVERSAL_DETECTED']`
- `uvicorn app.main:app --host 0.0.0.0 --port 8000` → started clean; log lines: `Feature Flag - PROBLEM_STATEMENT: sih26131`, `Confidence Gate Threshold: 0.7`, `RAG Relevance Cutoff: 0.18`
- `curl -i http://localhost:8000/api/v1/system/health` → `200 {"db":"ok","pgvector":"ok","corpus_docs":0,"corpus_chunks":67,"demo_farm":"ready","embedding_provider_configured":"stub","rag_relevance_threshold_active":0.18,"embedding_method_verified":"hash"}`
- `curl -o /dev/null -w '%{http_code}' /docs` → `200`; same for `/openapi.json` → `404`; `/api/v1/openapi.json` → `200`
- `python -m scripts.seed_full_demo --stage full` → seeded Ramesh demo farm, 82→68→59→86 health track

**B. Endpoints** (full request/response bodies for all of these are in the session transcript; condensed above per endpoint)
- B.0: `curl /api/v1/openapi.json | python3 -c "...list all paths..."` → the 47-route live table used throughout §B
- B.1: `/auth/register` → `201`; `/auth/login` → `200` + JWT; `/auth/otp/request` (wrong field) → `422`; (right field) → `200` + `debug_otp`; `/auth/otp/verify` (wrong otp) → `401`; (right otp) → `200` + JWT; `/auth/me` → `200`
- B.2: `/assets/presign` → `405`; `/assets/presigned-url` (wrong enum) → `422`; (right enum) → `201`; `/assets/{id}` → `200`
- B.3: `/farms` POST → `201`; GET list → `200`; GET by id → `200`; PUT → `200`; `/farms/{id}/summary` → `200`; `/farms/{id}/risk` (day 0) → `200` with `score:90` (the bug)
- B.4: `/farms/{id}/diagnose` disease above-gate → `200`, full advisory + citations
- B.5: `/farms/{id}/risk` (post-diagnosis) → `200 score:68`; `/risk/history` → `200`, 3-item walk; `/risk/recompute` → `200`
- B.6: in-process ASGITransport script (`/tmp/.../gate_repro.py`, `gate_repro2.py`) → below-gate disease `200` w/ `BELOW_CONFIDENCE_GATE`; out-of-scope disease `200` w/ `OUT_OF_SCOPE_TARGET`; pest above-gate (retry without `description_text`) `200` w/ real `kb_p301` citations; pest below-gate `200` w/ `BELOW_CONFIDENCE_GATE`
- B.7: `/advisory/query` disease `200 retrieved:true`; pest `200 retrieved:true`; gibberish `200 retrieved:false`; `/timeline/{farm_id}` `200`, 9 chronological events
- B.8: `/followup/checkin` got_worse → `200 auto_escalated:true, risk 68→52`; `/farms/{id}/followups/pending` → `404`; `/problems/{id}/escalate` → `404`; `/escalation/create` (wrong severity enum) → `422`; `/cases/{id}` → `404`; `/agronomist/case/{id}` → `200` (bundle, see §C.1); `/agronomist/case-queue` → `404`; `/agronomist/queue` → `200`, 24 rows; `/cases/{id}/resolve` → `404`; `/agronomist/resolve` (missing field) → `422`; (correct) → `200 risk 52→86`
- B.9: `/voice/transcribe` (sarvam, no key) → `500`; `/voice/synthesize` (sarvam, no key) → `500`
- B.10: `/farms/{id}/alerts` (no lat/lon) → `500 TypeError`; `/weather/current` (no params) → `422`; (with lat/lon) → `200`; `/weather/forecast` → `200`; `/weather/et0` → `200`; `/efficacy/treatments` → `404`; `/treatments/{id}/efficacy` (missing params) → `422`; (correct) → `200 status:insufficient_data`; `/alerts/{id}/acknowledge` (on seeded farm with lat/lon) → `200`; `/farms/{seeded_id}/alerts` → `200`, real `inspection_tasks[]`
- B.11: `/farms/{id}/land` → `200`; `/farms/{id}/schemes` → `409 LAND_NOT_VERIFIED`; `/resource-plan/{farm_id}` → `200`; `/officer/queue` → `404`

**C. Known-issue re-checks**
- C.2: `python -c "... StubEmbeddingAdapter().embed_text(tamil_string) ..."` → `nonzero dims: 0`, `tokens: []`; `psql "SELECT embedding <=> zero_vector FROM knowledge_chunks"` → all `NaN`; `python -c "max(0.0, min(1.0, 1.0 - float('nan')))"` → `1.0`; live `/advisory/query` with a pure-Tamil `query_text` → `200 retrieved:true` with real-looking citations
- C.5: server restarted with `ASR_PROVIDER=stub`/`TTS_PROVIDER=stub`; `/voice/synthesize` → `200 provider:stub`; `/voice/transcribe` → `200 provider:stub`, real Tamil transcript string
- C.6: `grep -rn VoiceInputButton apps/farmer_app --include=*.dart`, then read `_handleVoiceInput` in `onboarding_screen.dart` lines 469–560+

**E. Git**
- `git log --all --pretty=format:'%an|%ad' --date=iso | sort | awk ...` → per-author most-recent-commit table
- `git shortlog -sne --all` → raw counts
- `git log --all --pretty=format:'%an <%ae>' | sort -u | grep -i "shree\|kumar"` → only `Shruthi-Senthilkumar` matched, confirming zero Shreekumar commits
- `git log --all --author="Spyro007-06" --name-only` → 2 vision-model commits, unidentified against the six named teammates

---

*This audit made zero code changes to the repository other than local environment files (`.env`, `.env.example`-derived) needed to stand the stack up, which are git-ignored/not committed. No fixes were applied to any of the findings above, per the task's constraints.*
