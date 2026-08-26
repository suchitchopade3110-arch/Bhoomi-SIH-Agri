# Bhoomi SIH25076 / SIH26131 — Live Demo Rehearsal Runbook & Checklist

**Target**: 32–36 Hour Hardening Block | **Cold Start Recovery Time**: ~3.7s | **Test Suite**: 409/409 Passing

---

## 1. Quick Cold-Start Recovery (DB Reset in < 5 Seconds)

If a state leak occurs or a fresh reset is needed between runs:

```powershell
# 1. Bring up Docker Stack (if not already running)
docker compose -f infra/docker-compose.yml up -d

# 2. Replay Migrations + Corpus Ingest + Demo Seed (Services/API)
cd services/api
python -m alembic upgrade head
python -m scripts.reset_demo
```

(`scripts.reset_demo` does the corpus ingest + demo seed in one step —
equivalent to running `python -m app.services.rag.ingest` then
`python -m scripts.seed` separately. Do **not** use
`scripts.load_corpus --corpus-dir corpus/` here: that's a separate,
disconnected ingestion path over a different 8-document markdown corpus
with zero pest docs — it does not populate the corpus this app's
retrieval, tests, and every other demo path actually run against, and a
diagnosis above the gate will fail to find a citation and escalate
instead of composing advice.)

| Service | Host Port | Internal Port | Health / Role |
| :--- | :--- | :--- | :--- |
| **PostgreSQL 16 + pgvector** | `5433` | `5432` | `bhoomi` database (`postgres/postgres`) |
| **MinIO Object Storage** | `9000` / `9001` | `9000` / `9001` | `bhoomi-assets` bucket (`minioadmin/minioadmin`) |
| **FastAPI Backend** | `8000` | `8000` | `http://localhost:8000/api/v1` |

---

## 2. Team Role Assignments

| Role | Team Member | Primary Responsibility |
| :--- | :--- | :--- |
| **Farmer (Ramesh)** | **Santheesh** | Operates Farmer App on physical device (voice Tamil onboarding, disease photo capture, got-worse report, recovery verification). |
| **Agronomist (Dr. Lakshmi)** | **Thaariha** | Operates Agronomist Web Portal / queue on laptop (reviews escalated case, inspects citations, issues prescription). |
| **Lead Speaker / Architecture** | **Suchit** | Guides judges through the math: explains deterministic health score formula, confidence gate (`0.70`), and land HITL workflow. |

---

## 3. Demo Walkthrough Click-Path (Exact Numbers & Taps)

### Path A: The `82 → 68 → 59 → 86` Health-Score Trajectory

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  1. Baseline    │  ──►  │ 2. BLB Diagnosis│  ──►  │ 3. Got Worse    │  ──►  │ 4. Resolution   │
│   Score: 82     │       │   Score: 68     │       │   Score: 59     │       │   Score: 86     │
│   Band: GOOD    │       │   Band: WATCH   │       │   Band: POOR    │       │   Band: GOOD    │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

#### Step 1: Farmer Login & Baseline Score (`82` — GOOD)
- **Actor**: Santheesh (Farmer App)
- **Action**: 
  1. Open Farmer App, log in with phone `+91 99444 00001` (PIN/Pass: `bhoomi123`).
  2. View **Ramesh's Paddy Farm** (2.0 acres, Samba Paddy, vegetative stage, Chithode, Erode).
- **Expected On-Screen**:
  - Overall Score: **`82`** (Band: **Good** / Green)
  - Sub-index Breakdown:
    - Active Problem Load: `90.0` (Weight: 0.30)
    - Resource Adequacy: `88.0` (Weight: 0.20)
    - Environmental Suitability: `85.0` (Weight: 0.15)
    - Crop Stage Progression: `80.0` (Weight: 0.15)
    - Monitoring Recency: `78.0` (Weight: 0.10)
    - Treatment Response: `75.0` (Weight: 0.10)
  - Voice / Spoken Summary (Tamil): *"பயிர் நலம் சீராக உள்ளது."*

---

#### Step 2: Photo Capture & Disease Diagnosis (`82 → 68` — WATCH)
- **Actor**: Santheesh
- **Action**:
  1. Tap **"Diagnose / கேமரா ஸ்கேன்"**.
  2. Scan / Select Leaf Blight sample (`blb_leaf_photo.jpg`).
  3. AI returns diagnosis with Confidence Gate check (`confidence: 0.88 >= 0.70`).
- **Expected On-Screen**:
  - Issue: **Bacterial Leaf Blight (BLB)** — *Xanthomonas oryzae* (Moderate severity)
  - 5-Point Advisory with ICAR PoP Citation: `ICAR PoP: Rice — Bacterial Leaf Blight (2025-11-02)`
  - What to Do Next: *"Apply Copper Hydroxide 77% WP at 2.5 g/L. Drain excess standing water."*
  - What to Avoid: *"Do not apply nitrogen top-dressing during active infection."*
  - Updated Farm Health Score: **`68`** (Band: **Watch** / Amber)
  - Sub-index shift: Active Problem Load drops from `90.0 → 55.0`.

---

#### Step 3: Follow-Up "Got Worse" & Auto-Escalation (`68 → 59` — POOR)
- **Actor**: Santheesh
- **Action**:
  1. Under active problem, tap **"Follow-up / பரிசோதனை"**.
  2. Select **"Got Worse / நிலை மோசம்"** (voice note / note: *"இலைகளில் மஞ்சள் நிறம் வேகமாகப் பரவுகிறது"*).
  3. Bhoomi triggers **Rule-3 Auto-Escalation** into Agronomist Queue.
- **Expected On-Screen**:
  - Health Score drops to **`59`** (Band: **Poor** / Red).
  - Status banner: **"Escalated to KVK Agronomist — Case # assigned to Dr. Lakshmi"**.
  - ETA timer displayed: *"Agronomist review within 4 hours"*.

---

#### Step 4: Agronomist Resolution & Recovery (`59 → 86` — GOOD)
- **Actor**: Thaariha (Agronomist Portal) & Santheesh (Farmer App)
- **Action**:
  1. Thaariha logs in at Agronomist Portal (`+91 99444 00003` / `bhoomi123`).
  2. Opens Ramesh's Case from `kvk_erode` queue (inspects farmer notes, BLB photo, ICAR PoP reference).
  3. Submits Prescription: *"Copper Hydroxide 77% WP @ 2.5g/L + field drainage for 48h. Strict nitrogen pause."*
  4. Marks Case **Resolved**.
- **Expected On-Screen**:
  - Santheesh refreshes Farmer App / receives push notification.
  - Problem status moves to **Resolved**.
  - Final Health Score: **`86`** (Band: **Good** / Green).
  - Sub-index shift: Active Problem Load recovers to `95.0`, Treatment Response rises to `92.0`.

---

### Path B: `LAND_API_MODE` Flip (Auto-Lookup vs. HITL Fallback)

Demonstrating resilience when government cadastral API fails:

| Mode | Trigger | System Behavior | On-Screen Outcome |
| :--- | :--- | :--- | :--- |
| **Auto-Lookup Success** | `LAND_API_MODE=mock` | Survey # `142/3B` auto-matches state registry polygon | **Green Checkmark**: Instant Verified (`status: verified`), 2.0 acres boundary plotted on satellite map. |
| **Fail-into-HITL** | `LAND_API_MODE=error` or unmatched survey # | External API times out / no record found | **Graceful Escalation**: Status marked `unverified_pending_review`. Case automatically routes to **Officer Kumar** (`taluk_erode` queue) for manual Patta inspection. |

---

## 4. Rehearsal Timing Matrix & Stopwatch Benchmarks

| Milestone | Target Duration | Rehearsal 1 (Actual) | Rehearsal 2 (Actual) |
| :--- | :--- | :--- | :--- |
| **1. Intro & Problem Hook** | 0:00 – 0:45 (45s) | `[  :  ]` | `[  :  ]` |
| **2. Baseline & Health Formula Walk** | 0:45 – 1:30 (45s) | `[  :  ]` | `[  :  ]` |
| **3. Voice Scan & Disease Diagnosis (82→68)** | 1:30 – 2:30 (60s) | `[  :  ]` | `[  :  ]` |
| **4. Got-Worse & Agronomist Escalation (68→59→86)** | 2:30 – 3:45 (75s) | `[  :  ]` | `[  :  ]` |
| **5. Land HITL / Resilience Showcase** | 3:45 – 4:30 (45s) | `[  :  ]` | `[  :  ]` |
| **6. Scheme Discovery & Q&A Close** | 4:30 – 5:00 (30s) | `[  :  ]` | `[  :  ]` |
| **Total Presentation Time** | **< 5:00 min** | `[  :  ]` | `[  :  ]` |

---

## 5. Judge Defense / Point-Winning Answers

### Q1: "Is this health score just an arbitrary number generated by an LLM?"
> **Suchit's Answer**: 
> *"No. The LLM never touches the score calculation. It is a strictly deterministic, mathematical composite of 6 weighted sub-indices calculated in pure Python domain code:*
> $$\text{Health Score} = \sum_{i=1}^6 w_i \times S_i$$
> *Active Problem Load carries 30% weight, Resource Adequacy 20%, Environmental 15%, Crop Stage 15%, Recency 10%, and Treatment Response 10%. When BLB is detected, the severity deduction directly drops Active Problem Load from 90 to 55, bringing the composite down to exactly 68. The calculation is 100% reproducible and verifiable."*

### Q2: "What happens if the AI makes an erroneous or low-confidence diagnosis?"
> **Suchit / Thaariha's Answer**:
> *"We enforce a hard Confidence Gate at `0.70` in code. If image diagnosis confidence is below 0.70, the system is blocked from issuing speculative advice. Instead, it compiles an Escalation object and transfers the case directly to an agronomist with all collected context."*

### Q3: "What happens if the government land registry API is down?"
> **Suchit's Answer**:
> *"Bhoomi never blocks the farmer. When `LAND_API_MODE` fails or records mismatch, it falls into our Human-In-The-Loop (HITL) queue for Taluk Revenue Officers while keeping the farmer's advisory functionality fully active."*

---

## 6. Locked Cut List (Under Time Pressure)

If rehearsal or live presentation runs behind schedule, cut in this exact order:

```
[CUT FIRST]
  1. Seasonal Advisory Calendar
  2. Offline Voice Upload Queuing
  3. Government Schemes Deep-Dive
  4. Land Manual Boundary Editing Tool
  5. Case PDF Export
  6. Veteran / Novice UI Toggle
[NEVER CUT]
  ★ Confidence Gate (0.70 floor)
  ★ "What to Avoid" Advisory Rule
  ★ Deterministic 82 → 68 → 86 Score Progression
  ★ Agronomist Escalation & Resolution Loop
```
