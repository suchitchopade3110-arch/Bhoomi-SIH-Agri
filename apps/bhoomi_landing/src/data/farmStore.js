// PRD §5.12 & §9: Subsidies, Land Records, and Ramesh Case Store

export const INITIAL_FARM_DATA = {
  id: 'farm-ramesh-01',
  farmerName: 'Ramesh Sundaram',
  phone: '+91 98421 XXXXX',
  village: 'Thiruvaiyaru, Thanjavur District',
  state: 'Tamil Nadu',
  language: 'Tamil (தமிழ்)',
  crop: 'Samba Paddy (CR 1009 / Ponni)',
  cropKey: 'paddy',
  areaAcres: 2.0,
  growthStage: 'Vegetative (Day 25)',
  stageKey: 'vegetative',
  soilType: 'Clayey Alluvium (Deltaic)',
  irrigationSource: 'Canal Lift + Borewell (Alternate Wetting)',
  croppingSeason: 'Samba (Late Thaladi 2024)',
  
  // Land Registry Status (PRD §5.3)
  landStatus: 'VERIFIED', // 'PENDING_VERIFICATION' | 'UNDER_REVIEW' | 'VERIFIED' | 'REJECTED'
  surveyNumber: '142/3B-Thiruvaiyaru',
  pattaNumber: 'TN-THJ-2023-88910',
  verifiedBy: 'M. Selvaraj, Revenue Inspector (Taluk Office, Thanjavur)',
  verifiedAt: '2024-10-12T14:30:00Z',

  // Live Weather & ET0
  weather: {
    condition: 'Passing Monsoon Showers',
    temperatureC: 29.4,
    humidityPct: 82,
    rainfallForecastMm: 12.5,
    windKmh: 14,
    et0MmDay: 4.2
  },

  // Active Advisory State
  activeAlerts: [
    {
      id: 'alert-01',
      type: 'WEATHER_RAIN_IMMINENT',
      title: 'Rain Forecast (12.5 mm in 24 hrs)',
      instruction: 'Delay nitrogen top-dressing and field irrigation. Water logging alert for low-lying bunds.',
      inspectionTasks: [
        'Check bund drainage outlets are unobstructed',
        'Inspect leaf margins for water-soaked streaks',
        'Verify no standing water > 5cm during vegetative phase'
      ],
      mandatoryActionRequired: true
    }
  ],

  // Farm Problem Timeline & History (PRD §5.9)
  timeline: [
    {
      id: 'evt-1',
      date: 'Day 1 · Oct 10',
      type: 'ONBOARDING',
      title: 'Voice Onboarding & Land Verification Request',
      description: 'Profile created by voice in Tamil. Survey No. 142/3B submitted for Taluk HITL validation.',
      scoreDelta: null,
      scoreAfter: 'Unrated',
      badge: 'Onboarding'
    },
    {
      id: 'evt-2',
      date: 'Day 2 · Oct 12',
      type: 'LAND_VERIFIED',
      title: 'Land Record Verified by Taluk Officer',
      description: 'Revenue Inspector validated 2.0 Acres. Land status shifted to Verified. Baseline score initialized.',
      scoreDelta: '+82',
      scoreAfter: '82 / 100 (Good)',
      badge: 'HITL Verified'
    },
    {
      id: 'evt-3',
      date: 'Day 22 · Nov 01',
      type: 'DIAGNOSIS',
      title: 'Voice Query & Leaf Photo Uploaded',
      description: 'Yellowing leaf margins analyzed with 88% confidence. Early Bacterial Leaf Blight detected. 5-point guidance issued.',
      scoreDelta: '-14',
      scoreAfter: '68 / 100 (Watch)',
      badge: 'AI Diagnosis'
    },
    {
      id: 'evt-4',
      date: 'Day 25 · Nov 04',
      type: 'FOLLOW_UP',
      title: 'Closed-Loop Check-in: "Got Worse"',
      description: 'Farmer reported lesion expansion. Severity promoted to Moderate. Auto-escalated to Thanjavur KVK case queue.',
      scoreDelta: '-14',
      scoreAfter: '54 / 100 (Poor)',
      badge: 'Escalated to KVK'
    },
    {
      id: 'evt-5',
      date: 'Day 28 · Nov 07',
      type: 'EXPERT_RESOLUTION',
      title: 'KVK Agronomist Prescription Applied',
      description: 'Field officer confirmed formulation: Streptocycline + Copper Hydroxide. BLB halted. Full audit logged.',
      scoreDelta: '+32',
      scoreAfter: '86 / 100 (Good)',
      badge: 'Case Resolved'
    }
  ]
};

// PRD §5.12 Curated Subsidies with Staleness Protection
export const GOVERNMENT_SCHEMES = [
  {
    id: 'scheme-pmksy',
    code: 'TN-AGRI-2024-01',
    title: 'PMKSY Micro-Irrigation & Drip Subsidy',
    subsidyAmount: '100% for Small/Marginal Farmers (Up to ₹45,000/acre)',
    applicableCrops: ['Paddy', 'Sugarcane', 'Cotton', 'Banana'],
    eligibility: 'Verified Land Record required (Survey No. & Patta authenticated). Smallholder <= 5 acres.',
    lastVerifiedDate: '2024-11-01',
    stalenessStatus: 'ACTIVE & CURRENT',
    isGatedOnLand: true,
    department: 'Tamil Nadu Department of Agricultural Engineering'
  },
  {
    id: 'scheme-paddy-seed',
    code: 'TN-SEED-2024-09',
    title: 'TNAU Certified Samba Paddy Seed Distribution Subsidy',
    subsidyAmount: '50% Subsidy on certified CR-1009 / BPT-5204 seeds',
    applicableCrops: ['Paddy'],
    eligibility: 'Active farmer profile in delta districts with registered crop cycle.',
    lastVerifiedDate: '2024-10-15',
    stalenessStatus: 'ACTIVE & CURRENT',
    isGatedOnLand: true,
    department: 'State Agricultural Extension Center (AEC)'
  },
  {
    id: 'scheme-crop-ins',
    code: 'PMFBY-RABI-2024',
    title: 'PMFBY Crop Protection & Weather Damage Insurance',
    subsidyAmount: 'Premium subsidized at 1.5% for Rabi/Samba paddy',
    applicableCrops: ['Paddy', 'Pulses', 'Oilseeds'],
    eligibility: 'Loanee & non-loanee farmers holding verified land records.',
    lastVerifiedDate: '2024-11-15',
    stalenessStatus: 'ACTIVE & CURRENT',
    isGatedOnLand: true,
    department: 'Ministry of Agriculture & Farmers Welfare'
  }
];

// Pending Cases for Officer and Agronomist Portals
export const PENDING_LAND_REVIEWS = [
  {
    id: 'land-req-01',
    farmerName: 'Ramesh Sundaram',
    village: 'Thiruvaiyaru, Thanjavur',
    surveyNumber: '142/3B-Thiruvaiyaru',
    pattaNumber: 'TN-THJ-2023-88910',
    statedArea: '2.0 Acres',
    crop: 'Samba Paddy',
    submittedAt: '2024-10-10 09:40 AM',
    status: 'Pending Verification',
    geoCoordinates: '10.8804° N, 79.1065° E'
  },
  {
    id: 'land-req-02',
    farmerName: 'Karthik Chinnasamy',
    village: 'Kumbakonam, Thanjavur',
    surveyNumber: '89/1A-Kumbakonam',
    pattaNumber: 'TN-THJ-2024-11029',
    statedArea: '3.5 Acres',
    crop: 'Cotton & Black Gram',
    submittedAt: '2024-10-11 11:15 AM',
    status: 'Pending Verification',
    geoCoordinates: '10.9602° N, 79.3845° E'
  }
];

export const AGRONOMIST_CASE_QUEUE = [
  {
    id: 'case-thj-8821',
    farmerName: 'Ramesh Sundaram',
    farmLocation: 'Thiruvaiyaru, Thanjavur (Samba Paddy · 2 Acres)',
    growthStage: 'Vegetative (Day 25)',
    soilType: 'Clayey Alluvium',
    issueTitle: 'Bacterial Leaf Blight Progression (Got Worse)',
    confidenceScore: '88% AI Confidence',
    treatmentsTried: 'Copper Hydroxide 2.0g/L spray on Day 23; Standing water drained.',
    followUpTrend: 'Got Worse (Lesions expanded from tips down outer margin)',
    symptomPhotos: ['paddy_blb_symptom.jpg'],
    currentHealthScore: '54 / 100 (Critical Watch)',
    queuePosition: 1,
    priority: 'HIGH',
    slaTarget: '< 3 minutes triage time'
  }
];
