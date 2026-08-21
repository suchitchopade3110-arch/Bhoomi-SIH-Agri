# API Contract
## AI-Based Farmer Query Support & Advisory System

**Project code:** SIH25076
**Companion to:** `PRD.md` (enums, entities, and the health-score model here mirror PRD §7 and §9), `TECH_STACK.md` (Part 1 of the original combined doc)
**Status:** Draft v1.0 · for team review

---

## 2.1 Conventions

- **Base URL:** `/api/v1`
- **Format:** JSON everywhere; `multipart/form-data` only for the presign step is avoided — uploads go straight to storage via presigned URLs.
- **IDs:** UUID strings.
- **Timestamps:** ISO 8601, UTC (`2026-08-20T09:30:00Z`).
- **Auth:** `Authorization: Bearer <jwt>`. Role claim (`farmer | officer | agronomist`) gates the portal routes.
- **Pagination:** `?limit=20&cursor=<opaque>` → response includes `next_cursor` (null when exhausted).
- **Localization:** requests carry `lang` (BCP-47, e.g. `ta-IN`) where text is returned; responses echo it.

### Error envelope (all non-2xx)

```json
{
  "error": {
    "code": "LAND_NOT_VERIFIED",
    "message": "Scheme matching requires a verified land record.",
    "details": { "land_status": "pending_verification" }
  }
}
```

Stable machine codes (subset): `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `VALIDATION_FAILED`, `LAND_NOT_VERIFIED`, `BELOW_CONFIDENCE_GATE`, `NO_RELEVANT_SOURCE`, `OFFICER_UNAVAILABLE`.

## 2.2 Shared enums (mirror PRD §7, §9)

```
land_status        : pending_verification | under_review | verified | rejected
health_band        : unrated | critical | poor | watch | good | excellent
subindex_key       : environmental_suitability | resource_adequacy |
                     crop_stage_progression | active_problem_load |
                     monitoring_recency | treatment_response
problem_severity   : early | moderate | severe
problem_status     : open | resolved
followup_response  : improved | no_change | got_worse
case_status        : open | assigned | resolved
scheme_status       : active | expiring | expired
asset_kind         : image | audio
```

> **Known drift (flagged, not yet reconciled):** the shipped `app/core/enums.py` predates this contract text landing in the repo and diverges from it in three places outside Phase 4's scope: `LandStatus` uses `unverified | pending_review | verified | rejected` instead of the four values above; `AssetKind` is a granular six-value enum (`audio_query`, `disease_photo`, ...) instead of `image | audio`; `SchemeStatus` uses `active | upcoming | expired | applied | approved | rejected` instead of `active | expiring | expired`. `CaseStatus` (Phase 4's own aggregate) has been reconciled to match this contract exactly (`open | assigned | resolved`). The other three belong to the land-verification and scheme-discovery phases and should be reconciled when those phases are next touched.

## 2.3 Auth

**`POST /auth/otp/request`** — farmer login step 1
```json
// req
{ "phone": "+91XXXXXXXXXX" }
// res 200
{ "request_id": "5f...", "expires_in": 300 }
```

**`POST /auth/otp/verify`** — farmer login step 2
```json
// req
{ "request_id": "5f...", "otp": "482913" }
// res 200
{
  "access_token": "eyJ...", "refresh_token": "eyJ...",
  "user": { "id": "u_1", "role": "farmer", "phone": "+91XXXXXXXXXX" }
}
```

**`POST /auth/login`** — officer / agronomist
```json
// req
{ "email": "officer@taluk.gov.in", "password": "..." }
// res 200 → same token shape, role = officer | agronomist
```

## 2.4 Media (presigned upload)

Keeps large blobs off the API (see §1.4 of `TECH_STACK.md`). Client uploads, then references the returned `asset_id` in later calls.

**`POST /assets/presign`**
```json
// req
{ "kind": "image", "content_type": "image/jpeg", "farm_id": "f_1" }
// res 200
{
  "asset_id": "a_9",
  "upload_url": "https://storage.../a_9?sig=...",
  "method": "PUT",
  "expires_in": 600
}
```
Client `PUT`s the bytes to `upload_url`, then uses `asset_id` downstream.

## 2.5 Voice (ASR / TTS)

**`POST /voice/transcribe`** — audio `asset_id` → text + parsed intent
```json
// req
{ "asset_id": "a_2", "lang": "ta-IN", "context": "onboarding" }
// res 200
{
  "text": "என் நிலம் இரண்டு ஏக்கர்",
  "confidence": 0.91,
  "lang": "ta-IN",
  "parsed_intent": { "field": "land_area", "value_acres": 2.0 },
  "needs_confirmation": true
}
```
`needs_confirmation` is `true` for anything consequential (PRD §5.1 read-back rule). Below the ASR confidence floor, `parsed_intent` is omitted and the client re-prompts.

**`POST /voice/synthesize`** — text → audio
```json
// req
{ "text": "உங்கள் நீர் தேவை 4200 லிட்டர்", "lang": "ta-IN" }
// res 200
{ "audio_url": "https://storage.../tts_88.mp3", "expires_in": 600 }
```

*(Streaming ASR via `WS /voice/stream` is a Phase-2 nicety; the request/response pair above is what the demo needs.)*

## 2.6 Farm profile & onboarding

**`POST /farms`** — create from confirmed onboarding fields
```json
// req
{
  "crop": "samba_paddy",
  "area_acres_self_reported": 2.0,
  "growth_stage": "vegetative",
  "soil_type": "clay_loam",
  "irrigation_access": "canal",
  "season": "samba"
}
// res 201
{ "id": "f_1", "land_status": "pending_verification", "health": { "band": "unrated", "score": null } }
```
Missing required fields are allowed but leave `health.band = unrated` (PRD §5.2) — the response lists them:
```json
{ "id": "f_1", "missing_fields": ["soil_type"], "health": { "band": "unrated", "score": null } }
```

**`GET /farms/{id}`** → full profile (self-reported + verified area, land_status, current health summary).

**`PATCH /farms/{id}`** → update any onboarding field; triggers a health recompute.

**`GET /farms/{id}/summary`** — the farmer home screen in one call
```json
// res 200
{
  "farm": { "id": "f_1", "crop": "samba_paddy", "land_status": "verified" },
  "health": { "score": 82, "band": "good", "computed_at": "..." },
  "open_problems": 0,
  "pending_followups": 0,
  "latest_resource_plan_id": "rp_3",
  "spoken_summary": "உங்கள் பண்ணை நல்ல நிலையில் உள்ளது. மதிப்பெண் 82."
}
```

## 2.7 Land registry & HITL verification

**`POST /farms/{id}/land`** — submit land identifiers; attempts auto-lookup, falls into HITL on failure
```json
// req
{
  "survey_no": "142/3B",
  "patta_no": "TN-...-0912",
  "boundary_geojson": { "type": "Polygon", "coordinates": [[[77.1,11.0],[...]]] }
}
// res 202  (auto-lookup failed → queued to officer; the common case, per PRD §5.3)
{
  "land_record_id": "l_1",
  "status": "pending_verification",
  "auto_lookup": "failed",
  "queued_to": "officer:taluk_erode"
}
// res 200  (auto-lookup succeeded → the showcase path)
{ "land_record_id": "l_1", "status": "verified", "auto_lookup": "matched" }
```

**`GET /land/{id}`** → record with status, boundary, verifier, verified_at.

### Officer portal

**`GET /officer/land-queue`** → pending/under-review items assigned to this officer
```json
// res 200
{
  "items": [
    {
      "land_record_id": "l_1", "farm_id": "f_1",
      "farmer_stated": { "survey_no": "142/3B", "area_acres": 2.0 },
      "boundary_geojson": { "type": "Polygon", "coordinates": [[...]] },
      "submitted_at": "...", "status": "pending_verification"
    }
  ],
  "next_cursor": null
}
```

**`POST /officer/land/{id}/review`** — the live-demo approval
```json
// req  (approve, optionally correcting the boundary)
{ "decision": "verified", "boundary_geojson": { "type": "Polygon", "coordinates": [[...]] } }
// req  (reject)
{ "decision": "rejected", "reason": "Boundary overlaps adjacent survey number." }
// res 200
{ "land_record_id": "l_1", "status": "verified", "verified_at": "...", "verifier": "officer:taluk_erode" }
```
On `verified`, scheme matching (§2.14) unlocks for the farm.

## 2.8 Resource planner (FAO-56)

**`POST /farms/{id}/resource-plan`** — compute seed + daily irrigation
```json
// req  (all optional; defaults pulled from farm profile + live weather)
{ "as_of": "2026-08-20" }
// res 200
{
  "id": "rp_3",
  "tillable_area_acres": 1.9,
  "seed": { "rate_kg_per_acre": 30, "total_kg": 57 },
  "irrigation": {
    "et0_mm": 5.1,
    "kc": 1.05,
    "crop_water_need_mm": 5.36,
    "effective_rainfall_mm": 1.2,
    "net_requirement_mm": 4.16,
    "net_liters_per_day": 31940
  },
  "inputs": {
    "et0_source": "open-meteo",
    "kc_source": "FAO-56 / ICAR PoP (samba_paddy, vegetative)",
    "weather_as_of": "2026-08-20T06:00:00Z"
  },
  "explanation": "31,940 L/day = (ET₀ 5.1mm × Kc 1.05 − effective rain 1.2mm) over 1.9 acres.",
  "spoken_summary": "இன்றைய நீர் தேவை சுமார் 31,940 லிட்டர்."
}
```
The `inputs` block is the "why this many liters?" answer (PRD §5.4) — every figure that fed the result is returned, not hidden.

**`GET /farms/{id}/resource-plan/latest`** → most recent plan.

## 2.9 Health score

**`GET /farms/{id}/health`** — current score with full sub-index breakdown (the §7 defense, as data)
```json
// res 200
{
  "score": 68,
  "band": "watch",
  "computed_at": "2026-09-11T...",
  "weights_version": "v1",
  "subindices": [
    { "key": "environmental_suitability", "value": 88, "weight": 0.20, "contribution": 17.6 },
    { "key": "resource_adequacy",         "value": 90, "weight": 0.15, "contribution": 13.5 },
    { "key": "crop_stage_progression",    "value": 85, "weight": 0.15, "contribution": 12.75 },
    { "key": "active_problem_load",       "value": 70, "weight": 0.30, "contribution": 21.0 },
    { "key": "monitoring_recency",        "value": 80, "weight": 0.10, "contribution": 8.0 },
    { "key": "treatment_response",        "value": 100, "weight": 0.10, "contribution": 10.0 }
  ],
  "triggering_input": { "type": "diagnosis", "problem_id": "p_7", "severity": "early" },
  "spoken_summary": "உங்கள் மதிப்பெண் 68. காரணம்: ஒரு செயலில் உள்ள நோய்."
}
```

**`GET /farms/{id}/health/history`** → ordered `HealthSnapshot`s; each carries the same sub-index breakdown, so the timeline can render *why* every movement happened.

**`POST /farms/{id}/health/recompute`** *(demo/admin)* → forces a recompute; handy for walking the numbers live.

## 2.10 Diagnosis (image + voice → gated advisory)

**`POST /farms/{id}/diagnose`** — the confidence-gated path (PRD §5.6)
```json
// req
{
  "image_asset_id": "a_9",
  "description_asset_id": "a_10",   // optional voice note
  "description_text": "இலை நுனி மஞ்சள்"  // optional, from prior transcription
}
// res 200 — above the gate AND corpus had a relevant source
{
  "above_gate": true,
  "problem_id": "p_7",
  "diagnosis": { "label": "bacterial_leaf_blight", "stage": "early", "confidence": 0.87 },
  "advisory": {
    "possible_issue": "Early bacterial leaf blight (confidence: high).",
    "what_to_check": "Look for water-soaked lesions along leaf margins.",
    "what_to_do_next": "Drain the field to reduce standing water; avoid excess nitrogen.",
    "what_to_avoid": "Do not apply nitrogen top-dressing now — it accelerates spread.",
    "expert_triggers": "If lesions cover >25% of leaves within 3 days, escalate."
  },
  "citations": [
    { "doc_id": "kb_211", "title": "ICAR PoP: Rice — Bacterial Leaf Blight", "reviewed_on": "2025-11-02" }
  ],
  "health_delta": { "from": 82, "to": 68 },
  "spoken_summary": "இது பாக்டீரியல் இலை கருகல் நோயாக இருக்கலாம்..."
}
// res 200 — BELOW the gate  (never guesses; escalates instead)
{
  "above_gate": false,
  "reason": "confidence 0.41 < gate 0.70",
  "escalation": { "case_id": "c_5", "assigned_to": "agronomist:kvk_erode" },
  "spoken_summary": "எனக்கு உறுதியாகத் தெரியவில்லை. நிபுணருக்கு அனுப்பப்பட்டது."
}
```
Out-of-scope crop/disease and below-gate confidence both take the escalation branch — the model is never allowed to compose advice it isn't sure of.

## 2.11 Advisory (standalone RAG query)

For spoken questions that aren't a photo diagnosis.

**`POST /advisory/query`**
```json
// req
{ "farm_id": "f_1", "query_text": "எப்போது நெல் அறுவடை செய்ய வேண்டும்?", "lang": "ta-IN" }
// res 200 — relevant source found
{
  "retrieved": true,
  "advisory": { "...5-point structure..." },
  "citations": [ { "doc_id": "kb_190", "title": "...", "reviewed_on": "2025-10-14" } ]
}
// res 200 — NO source above relevance threshold  (no fabrication; PRD §5.7)
{
  "retrieved": false,
  "reason": "no_relevant_source",
  "escalation_offered": true,
  "spoken_summary": "இதற்கான நம்பகமான தகவல் என்னிடம் இல்லை. நிபுணருக்கு அனுப்பட்டுமா?"
}
```

## 2.12 Timeline, problems & follow-up

**`GET /farms/{id}/timeline`** → chronological events (queries, diagnoses, treatments, score movements, expert notes), paginated. This is the case file (PRD §5.9).

**`GET /farms/{id}/problems?status=open`** → problem list.

**`GET /problems/{id}`** → problem detail with linked photos and advisory.

**`GET /farms/{id}/followups/pending`** → scheduled check-ins due.

**`POST /followups/{id}/respond`** — closes the loop (PRD §5.10)
```json
// req
{ "response": "got_worse", "image_asset_id": "a_15" }
// res 200
{
  "problem_id": "p_7",
  "severity_change": { "from": "early", "to": "moderate" },
  "health": { "from": 68, "to": 59, "band": "poor" },
  "escalated": true,
  "case_id": "c_5"
}
```
`got_worse` past the threshold auto-escalates and returns the new `case_id`.

## 2.13 Escalation & case summary

**`POST /problems/{id}/escalate`** *(also fired automatically)* → compiles the Farm Case Summary and routes it.
```json
// res 201
{ "case_id": "c_5", "assigned_to": "agronomist:kvk_erode", "status": "assigned" }
```

**`GET /cases/{id}`** — the pre-analyzed bundle the agronomist opens (PRD §5.11)
```json
// res 200
{
  "case_id": "c_5",
  "farm": { "id": "f_1", "crop": "samba_paddy", "area_acres_verified": 1.9, "soil_type": "clay_loam" },
  "problem": { "id": "p_7", "label": "bacterial_leaf_blight", "severity": "moderate" },
  "timeline": [ { "at": "...", "event": "diagnosis", "detail": "..." }, { "at": "...", "event": "followup", "detail": "got_worse" } ],
  "images": [ { "asset_id": "a_9", "url": "..." }, { "asset_id": "a_15", "url": "..." } ],
  "treatments_tried": [ "field drainage", "nitrogen withheld" ],
  "followup_trend": "got_worse",
  "current_health": { "score": 59, "band": "poor" },
  "status": "assigned"
}
```

### Agronomist portal

**`GET /agronomist/case-queue`** → assigned cases, newest first.

**`POST /cases/{id}/resolve`** — expert diagnosis/treatment back into the loop
```json
// req
{
  "diagnosis": "Confirmed BLB, moderate.",
  "treatment": "Copper-based bactericide per label; drain and dry field 48h.",
  "notes": "Recheck in 5 days."
}
// res 200
{ "case_id": "c_5", "status": "resolved", "problem_status": "resolved", "health": { "from": 59, "to": 86, "band": "good" } }
```
Resolution clears the problem (sub-index 4 → 100) and lifts monitoring/treatment sub-indices, which is why the score recovers *above* baseline (PRD §7.4).

## 2.14 Scheme discovery

**`GET /farms/{id}/schemes`** — gated on `land_status = verified` (PRD §5.12)
```json
// res 200
{
  "schemes": [
    {
      "id": "s_22",
      "name": "TN Crop Protection Subsidy",
      "jurisdiction": "TN",
      "match_reason": "samba_paddy + verified 1.9 acres + smallholder category",
      "status": "active",
      "last_verified": "2026-07-30"
    },
    {
      "id": "s_08", "name": "…", "status": "expiring",
      "last_verified": "2026-01-10", "note": "Window closes in 12 days."
    }
  ]
}
// res 409 — land not verified
{ "error": { "code": "LAND_NOT_VERIFIED", "message": "Verify land to see eligible schemes.",
             "details": { "land_status": "pending_verification" } } }
```
Every scheme carries `last_verified`; `expiring`/`expired` are flagged, never shown as plainly current.

## 2.15 Weather (supporting)

**`GET /farms/{id}/weather`** → current + short forecast (ET₀, rainfall) used by the planner and the environmental sub-index. Exposed mainly so the UI can show "why" behind a water figure; internally the planner and scorer call the same source.

---

## 2.16 Endpoint index

| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/otp/request` · `/auth/otp/verify` · `/auth/login` | Auth (farmer OTP, staff login) |
| POST | `/assets/presign` | Presigned upload for photo/audio |
| POST | `/voice/transcribe` · `/voice/synthesize` | ASR / TTS |
| POST/GET/PATCH | `/farms` · `/farms/{id}` · `/farms/{id}/summary` | Profile & onboarding |
| POST/GET | `/farms/{id}/land` · `/land/{id}` | Land submission & lookup |
| GET/POST | `/officer/land-queue` · `/officer/land/{id}/review` | HITL land portal |
| POST/GET | `/farms/{id}/resource-plan` · `/farms/{id}/resource-plan/latest` | FAO-56 planner |
| GET/POST | `/farms/{id}/health` · `/farms/{id}/health/history` · `/farms/{id}/health/recompute` | Health score |
| POST | `/farms/{id}/diagnose` | Gated image+voice diagnosis |
| POST | `/advisory/query` | Standalone grounded RAG query |
| GET | `/farms/{id}/timeline` · `/farms/{id}/problems` · `/problems/{id}` | Case file |
| GET/POST | `/farms/{id}/followups/pending` · `/followups/{id}/respond` | Closed-loop follow-up |
| POST/GET | `/problems/{id}/escalate` · `/cases/{id}` | Escalation & case summary |
| GET/POST | `/agronomist/case-queue` · `/cases/{id}/resolve` | KVK portal |
| GET | `/farms/{id}/schemes` | Scheme discovery (verified-gated) |
| GET | `/farms/{id}/weather` | Supporting weather |

---

## Implementation status (updated as phases land)

- **Phase 0** — repo skeleton, config, ports/adapters, in-memory repositories, every endpoint above scaffolded as a `501 NOT_IMPLEMENTED` stub.
- **Phase 1** — §7's Farm Health Score engine (`app/domain/health/`), pure and unit-tested against the 82 → 68 → 59 → 86 worked example.
- **Phase 2** — the confidence gate (`app/domain/gate/`), the single compose-vs-escalate decision point.
- **Phase 3** — §2.10/§2.11 (`POST /farms/{id}/diagnose`, `POST /advisory/query`): grounded, cited 5-point advisory with the honest no-retrieval escalation.
- **Phase 4** — §2.12/§2.13's escalation subsystem: `POST /problems/{id}/escalate`, `GET /cases/{id}`, `GET /agronomist/case-queue`, `POST /followups/{id}/respond`, `POST /cases/{id}/resolve` — all real, wired in `app/api/v1/cases.py` and `app/services/escalation/`. The Phase-0 stubs at `POST /followup/checkin`, `POST /escalation/create`, `GET /agronomist/queue`, `GET /agronomist/case/{id}`, `POST /agronomist/resolve` are marked `deprecated` in the OpenAPI schema and kept only because earlier tests assert their presence — remove them once those tests are updated to point at the real paths above.
- **Not yet built:** §2.3 (auth beyond the JWT primitives), §2.4–2.9 (assets/voice/farms/land/resource-plan/weather remain 501 stubs), §2.14 (scheme discovery).

---

*End of API Contract v1.0. The contract is intentionally aligned to the PRD's enums and health-score model so the frontend, backend, and pitch all tell one story: a case lifecycle where every number is inspectable and the system escalates instead of guessing.*
