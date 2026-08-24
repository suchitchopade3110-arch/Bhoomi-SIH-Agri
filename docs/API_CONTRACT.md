# BHOOMI — Frontend & Mobile API Contract Specification

> **Version:** 1.0.0 (SIH25076)  
> **Target Base URL:** `http://localhost:8000` (Local / Web), `http://10.0.2.2:8000` (Android Emulator)  
> **Prefix:** `/api/v1`

---

## 1. Authentication & User (`/api/v1/auth`)

### 1.1 Request OTP / Phone Login
- **Endpoint:** `POST /api/v1/auth/otp/request`
- **Request Body:**
  ```json
  {
    "phone": "+919876543210"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "session_id": "sess_12345",
    "status": "otp_sent",
    "expires_in_seconds": 300
  }
  ```

### 1.2 Verify OTP
- **Endpoint:** `POST /api/v1/auth/otp/verify`
- **Request Body:**
  ```json
  {
    "phone": "+919876543210",
    "otp": "123456",
    "session_id": "sess_12345"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "access_token": "eyJhbGci...",
    "token_type": "bearer",
    "user_id": "u_farmer_1",
    "is_new_user": false,
    "role": "farmer"
  }
  ```

---

## 2. Farm Management (`/api/v1/farms`)

### 2.1 Register Farm Profile
- **Endpoint:** `POST /api/v1/farms/`
- **Request Body:**
  ```json
  {
    "farmer_id": "u_farmer_1",
    "farm_name": "My Farm (Samba Paddy)",
    "primary_crop": "Paddy",
    "crop": "Paddy",
    "total_area_acres": 2.0,
    "area_acres_self_reported": 2.0,
    "growth_stage": "vegetative",
    "soil_type": "Clay Loam",
    "irrigation_source": "Borewell",
    "irrigation_access": "Borewell",
    "season": "Rabi",
    "village": "Perundurai",
    "taluk": "Erode",
    "district": "Erode",
    "state": "Tamil Nadu",
    "latitude": 11.2742,
    "longitude": 77.5828
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "id": "farm_tamilnadu_001",
    "farmer_id": "u_farmer_1",
    "farm_name": "My Farm (Samba Paddy)",
    "primary_crop": "Paddy",
    "total_area_acres": 2.0,
    "growth_stage": "vegetative",
    "soil_type": "Clay Loam",
    "irrigation_source": "Borewell",
    "land_status": "pending_verification",
    "current_health_score": null,
    "health_band": "unrated",
    "created_at": "2026-08-22T10:00:00Z"
  }
  ```

### 2.2 Get Farm Summary & Identity
- **Endpoint:** `GET /api/v1/farms/{farm_id}`
- **Response:** `200 OK`
  ```json
  {
    "id": "farm_tamilnadu_001",
    "farm_name": "My Farm (Samba Paddy)",
    "primary_crop": "Paddy",
    "total_area_acres": 2.0,
    "growth_stage": "vegetative",
    "land_status": "verified",
    "current_health_score": 82,
    "health_band": "good",
    "open_cases_count": 0,
    "active_advisories_count": 1,
    "latest_resource_plan_id": "rp_erode_001"
  }
  ```

---

## 3. Land Verification (`/api/v1/land`)

### 3.1 Submit Land Record for Verification
- **Endpoint:** `POST /api/v1/land/verify`
- **Request Body:**
  ```json
  {
    "farm_id": "farm_tamilnadu_001",
    "survey_number": "142/3B",
    "suggested_boundary": {
      "type": "Polygon",
      "coordinates": [
        [
          [77.7214, 11.3412],
          [77.7289, 11.3415],
          [77.7285, 11.3478],
          [77.7211, 11.3475],
          [77.7214, 11.3412]
        ]
      ]
    }
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "parcel_id": "parcel_erode_142",
    "farm_id": "farm_tamilnadu_001",
    "status": "pending_verification",
    "survey_number": "142/3B",
    "suggested_boundary": { ... },
    "official_area_acres": null,
    "verified_boundary_geojson": null,
    "officer_notes": null,
    "updated_at": "2026-08-22T10:05:00Z"
  }
  ```

### 3.2 Get Land Record Status
- **Endpoint:** `GET /api/v1/land/{farm_id}`
- **Response:** `200 OK`
  ```json
  {
    "parcel_id": "parcel_erode_142",
    "farm_id": "farm_tamilnadu_001",
    "status": "verified",
    "survey_number": "142/3B",
    "official_area_acres": 2.0,
    "suggested_boundary": { ... },
    "verified_boundary_geojson": { ... },
    "officer_notes": "Survey boundary matched official village revenue FMB record.",
    "updated_at": "2026-08-22T11:00:00Z"
  }
  ```

---

## 4. Farm Health & Explainability (`/api/v1/health`)

### 4.1 Compute / Fetch Health Snapshot
- **Endpoint:** `GET /api/v1/health/{farm_id}`
- **Response:** `200 OK`
  ```json
  {
    "farm_id": "farm_tamilnadu_001",
    "composite_score": 82,
    "health_band": "good",
    "environmental_suitability": 88,
    "resource_adequacy": 85,
    "crop_stage_progression": 80,
    "active_problem_load": 78,
    "monitoring_recency": 90,
    "treatment_response": 82,
    "computed_at": "2026-08-22T12:00:00Z"
  }
  ```

### 4.2 Fetch Health History Timeline
- **Endpoint:** `GET /api/v1/health/{farm_id}/history`
- **Response:** `200 OK`
  ```json
  {
    "farm_id": "farm_tamilnadu_001",
    "history": [
      {
        "score": 82,
        "band": "good",
        "timestamp": "2026-08-22T12:00:00Z",
        "primary_factor": "Advisory symptoms resolved"
      },
      {
        "score": 74,
        "band": "moderate",
        "timestamp": "2026-08-15T08:00:00Z",
        "primary_factor": "Bacterial leaf streak symptoms detected"
      }
    ]
  }
  ```

---

## 5. Crop Diagnosis & 5-Point Advisory (`/api/v1/diagnose`)

### 5.1 Run Diagnostic Pipeline
- **Endpoint:** `POST /api/v1/diagnose/{farm_id}`
- **Request Body:**
  ```json
  {
    "image_asset_id": "asset_img_901",
    "description_text": "Yellow lesions along leaf tips with water-soaked margins",
    "description_asset_id": null
  }
  ```
- **Response (Above Confidence Gate):** `200 OK`
  ```json
  {
    "above_gate": true,
    "problem_id": "prob_blb_001",
    "diagnosis": {
      "label": "Bacterial Leaf Blight (BLB)",
      "stage": "early_tillering",
      "confidence": 0.88
    },
    "advisory": {
      "possible_issue": "Bacterial Leaf Blight (Xanthomonas oryzae)",
      "what_to_check": [
        "Water-soaked yellowish stripes on leaf blades starting from tips",
        "Bacterial ooze droplets during humid morning hours",
        "Wilting of young tillers (Kresek phase)"
      ],
      "what_to_do_next": [
        "Drain excess standing water from the field for 3-4 days",
        "Apply recommended bio-control Pseudomonas fluorescens @ 2.5 kg/ha",
        "Maintain balanced potash fertilization to strengthen leaf tissues"
      ],
      "what_to_avoid": "Do not apply excess nitrogen top-dressing while disease symptoms are active.",
      "expert_triggers": [
        "More than 25% foliage exhibiting leaf drying",
        "Kresek wilting spreading across contiguous field patches"
      ]
    },
    "citations": [
      {
        "doc_id": "doc_tnau_paddy_blb_2025",
        "title": "TNAU Agriteck Crop Protection Protocol — Bacterial Leaf Blight",
        "reviewed_on": "2025-11-15"
      },
      {
        "doc_id": "doc_icar_rice_mgmt_v3",
        "title": "ICAR National Rice Research Institute Advisory Guide",
        "reviewed_on": "2025-08-10"
      }
    ],
    "reason": null,
    "escalation": null,
    "spoken_summary": "Detected Bacterial Leaf Blight with 88% confidence. Please drain standing water and pause nitrogen fertilizers."
  }
  ```

- **Response (Below Confidence Gate — Rule 1 & 2 Enforced):** `200 OK`
  ```json
  {
    "above_gate": false,
    "problem_id": "prob_uncertain_002",
    "diagnosis": {
      "label": "Uncertain Leaf Lesion",
      "stage": "vegetative",
      "confidence": 0.54
    },
    "advisory": null,
    "citations": [],
    "reason": "Image confidence 0.54 is below the required 0.70 threshold. Escalated to KVK Agronomist.",
    "escalation": {
      "case_id": "esc_kvk_701",
      "assigned_to": "KVK Agronomist (Erode)"
    },
    "spoken_summary": "Image confidence is below 70%. We have forwarded this case to your local KVK agronomist for expert review."
  }
  ```

---

## 6. Resource Planning & FAO-56 (`/api/v1/resource-plan`)

### 6.1 Generate / Calculate Resource Plan
- **Endpoint:** `POST /api/v1/resource-plan/{farm_id}`
- **Response:** `200 OK`
  ```json
  {
    "irrigation_plan": {
      "area_acres": 2.0,
      "daily_liters_total": 2200.0,
      "irrigation_need_mm": 5.5,
      "et0_mm_day": 4.8,
      "kc_factor": 1.15,
      "effective_rainfall_mm": 0.0,
      "calculation_formula": "Daily need = (ET0 * Kc - Pe) * Area * 4046.86 L"
    },
    "recommended_seed_kg": 57.0,
    "farm_id": "farm_tamilnadu_001",
    "created_at": "2026-08-22T06:00:00Z"
  }
  ```

### 6.2 Get Latest Plan
- **Endpoint:** `GET /api/v1/resource-plan/{farm_id}`
- **Response:** `200 OK` (matches schema above)

---

## 7. Scheme Discovery & Eligibility (`/api/v1/schemes`)

### 7.1 Match Government Schemes
- **Endpoint:** `POST /api/v1/schemes/match`
- **Request Body:**
  ```json
  {
    "farm_id": "farm_tamilnadu_001"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "farm_id": "farm_tamilnadu_001",
    "matched_schemes": [
      {
        "scheme_id": "pm_kisan",
        "title": "PM-KISAN Samman Nidhi",
        "short_description": "Direct income support of ₹6,000 per year in three equal installments to landholding farmer families.",
        "match_status": "likely_relevant",
        "match_explanation": "Verified landholding size of 2.0 acres satisfies small/marginal farmer eligibility criteria.",
        "missing_requirements": [],
        "benefit_summary": "₹6,000 / year direct benefit transfer"
      },
      {
        "scheme_id": "pmfby_crop_insurance",
        "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "short_description": "Comprehensive crop insurance covering non-preventable natural risks from pre-sowing to post-harvest.",
        "match_status": "likely_relevant",
        "match_explanation": "Samba Paddy in Erode notified under PMFBY seasonal coverage.",
        "missing_requirements": ["Sowing Certificate"],
        "benefit_summary": "Up to ₹35,000 / acre sum insured"
      }
    ]
  }
  ```

### 7.2 Get Scheme Details
- **Endpoint:** `GET /api/v1/schemes/{scheme_id}`
- **Response:** `200 OK`
  ```json
  {
    "scheme_id": "pm_kisan",
    "title": "PM-KISAN Samman Nidhi",
    "department": "Ministry of Agriculture & Farmers Welfare",
    "description": "Financial assistance for all landholding farmer families with cultivable land.",
    "match_explanation": "Verified landholding size of 2.0 acres satisfies small/marginal farmer criteria.",
    "benefits": [
      "₹6,000 per year transferred directly to Aadhaar-linked bank account",
      "Paid in three 4-monthly installments of ₹2,000 each"
    ],
    "eligibility_criteria": [
      "All landholding farmer families with cultivable land parcel records",
      "Excludes institutional landholders and high-income tax payees"
    ],
    "required_documents": [
      "Aadhaar Card",
      "Verified Land Ownership Record (Patta / Chitta / RoR)",
      "Bank Account Passbook"
    ],
    "official_url": "https://pmkisan.gov.in",
    "helpline": "155261 / 011-24300606"
  }
  ```

---

## 8. Follow-ups & Check-ins (`/api/v1/followup`)

### 8.1 Submit Advisory Outcome Check-in
- **Endpoint:** `POST /api/v1/followup/checkin`
- **Request Body:** (matches `app/schemas/followup.py::FollowupCheckinRequest` — the
  earlier `diagnosis_id`/`outcome` aliases below were dropped; `problem_id` and
  `response` are the single source of truth for each)
  ```json
  {
    "farm_id": "farm_tamilnadu_001",
    "response": "improved",
    "problem_id": "prob_blb_001",
    "advisory_id": null,
    "farmer_notes": "Yellow lesions drying out after draining field and bio-control spray",
    "photo_asset_id": null
  }
  ```
  - `problem_id` is optional — omit it to check in on the farm's latest open problem.
- **Response:** `200 OK` (matches `FollowupCheckinResponse`)
  ```json
  {
    "followup_id": "fol_98231",
    "problem_id": "prob_blb_001",
    "response": "improved",
    "auto_escalated": false,
    "escalation_id": null,
    "updated_health_snapshot": { "...": "HealthSnapshot, see §5" },
    "spoken_summary": "Thanks for the update — your health score is now 74.",
    "created_at": "2026-08-22T14:00:00Z"
  }
  ```
  - `response: "got_worse"` **always** auto-escalates (`auto_escalated: true`,
    `escalation_id` populated) — the problem's severity is promoted one tier
    and an escalation case is created in the same call.
  - `response: "improved"` demotes severity one tier, or resolves the problem
    outright if it was already at the lightest tier.
  - `response: "no_change"` leaves severity untouched.

---

## 9. Farmer Escalation (`/api/v1/escalation`)

### 9.1 Create Escalation Request
- **Endpoint:** `POST /api/v1/escalation/create`
- **Request Body:**
  ```json
  {
    "farm_id": "farm_tamilnadu_001",
    "reason": "Symptoms rapidly spreading despite bio-control treatment",
    "severity": "high",
    "notes": "Need urgent agronomist review",
    "related_diagnosis_id": "prob_blb_001"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "escalation_id": "esc_kvk_701",
    "farm_id": "farm_tamilnadu_001",
    "status": "escalated_to_kvk",
    "assigned_kvk_center": "ICAR-KVK Erode Center",
    "created_at": "2026-08-22T14:30:00Z",
    "case_summary": {
      "problem_summary": "Advisory outcome got worse; severe bacterial blight spread reported.",
      "escalated_to": "Dr. S. Sundaram (KVK Erode)"
    }
  }
  ```

---

## 10. KVK Agronomist Portal (`/api/v1/agronomist`)

### 10.1 Get Agronomist Escalation Queue
- **Endpoint:** `GET /api/v1/agronomist/queue`
- **Response:** `200 OK`
  ```json
  [
    {
      "escalation_id": "esc_kvk_701",
      "farm_id": "farm_tamilnadu_001",
      "farmer_name": "R. Murugesan",
      "village": "Perundurai",
      "district": "Erode",
      "crop": "Samba Paddy",
      "severity": "high",
      "problem_summary": "Suspected bacterial leaf streak / severe blight with rapid leaf drying",
      "escalated_at": "2026-08-22T14:30:00Z",
      "status": "escalated_to_kvk",
      "latest_images": [
        "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=800"
      ]
    }
  ]
  ```

### 10.2 Get Case Summary
- **Endpoint:** `GET /api/v1/agronomist/case/{escalation_id}`
- **Response:** `200 OK`

### 10.3 Resolve Escalation with Expert Prescription
- **Endpoint:** `POST /api/v1/agronomist/resolve`
- **Request Body:**
  ```json
  {
    "escalation_id": "esc_kvk_701",
    "agronomist_id": "agronomist_kvk_1",
    "agronomist_name": "Dr. S. Sundaram",
    "confirmed_diagnosis": "Severe Bacterial Leaf Blight (BLB) aggravated by micro-nutrient deficiency",
    "expert_advice": "Apply Copper Hydroxide 77% WP @ 2.0 g/L combined with Zinc Sulphate 0.5% foliar spray during clear sunshine.",
    "prescribed_inputs": [
      "Copper Hydroxide 77% WP @ 500g / acre",
      "Zinc Sulphate 21% @ 1 kg / acre foliar spray"
    ],
    "status": "resolved"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "escalation_id": "esc_kvk_701",
    "status": "resolved",
    "resolved_at": "2026-08-22T15:00:00Z",
    "message": "Resolution recorded and dispatched to farmer mobile device."
  }
  ```

---

## 11. Revenue Officer Portal (`/api/v1/officer`)

### 11.1 Get Land Parcel Verification Queue
- **Endpoint:** `GET /api/v1/officer/queue`
- **Response:** `200 OK`
  ```json
  [
    {
      "parcel_id": "parcel_erode_142",
      "farm_id": "farm_tamilnadu_001",
      "farmer_name": "R. Murugesan",
      "survey_number": "142/3B",
      "area_acres": 2.0,
      "village": "Perundurai",
      "district": "Erode",
      "status": "pending_verification",
      "suggested_boundary": {
        "type": "Polygon",
        "coordinates": [
          [
            [77.7214, 11.3412],
            [77.7289, 11.3415],
            [77.7285, 11.3478],
            [77.7211, 11.3475],
            [77.7214, 11.3412]
          ]
        ]
      },
      "created_at": "2026-08-21T08:30:00Z"
    }
  ]
  ```

### 11.2 Record Revenue Officer Verification / Action
- **Endpoint:** `POST /api/v1/officer/action`
- **Request Body:**
  ```json
  {
    "parcel_id": "parcel_erode_142",
    "action": "verify",
    "confirmed_boundary_geojson": { ... },
    "officer_notes": "Survey boundary verified against Taluk Revenue FMB records.",
    "officer_id": "officer_erode_1",
    "officer_name": "M. Radhakrishnan (Tahsildar Erode)"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "parcel_id": "parcel_erode_142",
    "status": "verified",
    "verified_boundary_geojson": { ... },
    "officer_notes": "Survey boundary verified against Taluk Revenue FMB records.",
    "updated_at": "2026-08-22T15:15:00Z"
  }
  ```

---

## 12. Asset Management & Storage (`/api/v1/assets`)

### 12.1 Generate Presigned Upload URL
- **Endpoint:** `POST /api/v1/assets/presigned-url`
- **Request Body:**
  ```json
  {
    "file_name": "leaf_symptom.jpg",
    "content_type": "image/jpeg",
    "asset_kind": "image_diagnosis"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "asset_id": "asset_img_901",
    "upload_url": "http://localhost:9000/bhoomi-assets/asset_img_901.jpg?X-Amz-Signature=...",
    "public_url": "http://localhost:9000/bhoomi-assets/asset_img_901.jpg",
    "expires_in_seconds": 900
  }
  ```
