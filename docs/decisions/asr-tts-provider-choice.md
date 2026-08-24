# Decision: ASR / TTS Provider — Sarvam AI vs Bhashini

**Status:** Decided
**Owner:** Shruthi (Voice + Database)
**Date:** 2026-08-23

## Context

The voice module (PRD §5.1, §5.2) needs a real Speech-to-Text and Text-to-Speech
provider for Tamil. The codebase ships with adapter implementations for two
candidates — Bhashini (AI4Bharat/ULCA) and Sarvam AI — behind a common
`AsrTtsPort` interface, selectable via `ASR_PROVIDER` in `.env`. This document
records why Sarvam AI was chosen for the demo.

## Candidates evaluated

### Sarvam AI (Saaras v3 STT / Bulbul v3 TTS)
- **Access:** Self-serve. Signed up, generated an API key, and was making
  authenticated calls within minutes.
- **Tamil TTS:** Verified manually via direct API calls before wiring the
  adapter — clean base64 audio returned, valid WAV (16-bit PCM, mono,
  22,050 Hz), correct duration for the input phrase, confirmed by ear.
- **STT:** Requires multipart/form-data file upload (not a JSON body with a
  URL) — this was initially implemented incorrectly and caught during code
  review before it reached production; fixed and covered by a dedicated unit
  test (`test_transcribe_resolves_asset_id_via_storage`).
- **Integration effort:** Adapter implemented cleanly against the existing
  `BhashiniAsrTtsAdapter` pattern with no architectural changes needed.

### Bhashini (AI4Bharat / ULCA)
- **Access:** Requires registering as an "Integrator" via the ULCA portal,
  email verification, and — per Bhashini's own onboarding docs — manual
  approval by the DIBD (Digital India Bhashini Division) team before
  credentials become usable.
- **Outcome:** Registration/credential access did not complete within the
  project's working timeline. Could not obtain a working `BHASHINI_USER_ID` /
  `BHASHINI_API_KEY` / `BHASHINI_PIPELINE_ID` set to test against.
- **Adapter status:** `bhashini_asr.py` already exists in the codebase and
  remains available as a fallback/future option — no code was removed. If
  Bhashini access is obtained later (e.g. during Phase 2 pilot), it can be
  enabled by setting `ASR_PROVIDER=bhashini` with no other changes required.

## Decision

**Use Sarvam AI (`ASR_PROVIDER=sarvam`) as the primary ASR/TTS provider for
the hackathon demo.**

## Rationale

1. Sarvam was the only candidate with a working, testable integration within
   the project timeline — Bhashini's approval step was the blocking factor,
   not code or technical fit.
2. Sarvam's Tamil TTS output was independently verified (audio played back,
   confirmed correct language/content) before committing to the integration.
3. The existing port/adapter architecture (`AsrTtsPort`) means this is not a
   permanent lock-in — switching providers, or supporting both, is a
   config-only change (`ASR_PROVIDER` in `.env`), not a rearchitecture.

## What would change this decision

- If Bhashini credentials become available with time to properly test
  accuracy/latency against real farmer-style Tamil audio (accented, noisy,
  code-mixed), a proper side-by-side comparison should be run before Phase 2
  (per `Bhoomi_Execution_Plan.md`), since Bhashini has a stronger
  government/Indian-language narrative that may matter for the pitch and for
  production-scale cost.
- Sarvam's per-second billing model should be revisited before scaling past
  the demo — free-tier usage was sufficient for development/testing but was
  not evaluated for pilot-scale cost.

## Open items / not yet verified

- [ ] Sarvam STT accuracy on real (non-synthetic) farmer audio, not just
      TTS round-trips
- [ ] Latency under realistic mobile/rural network conditions (only tested
      from a local dev machine so far)
- [ ] Full live end-to-end test through the FastAPI app (`/voice/synthesize`,
      `/voice/transcribe`) — pending local Docker/Postgres environment setup
