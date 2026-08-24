// PRD §7: Dynamic Farm Health Score Rubric Engine
// Formula: Health = round( Σ (w_i * subindex_i) ), clamped to [0, 100]

export const HEALTH_WEIGHTS = {
  environmental: 0.20,   // Weather + soil suitability
  resource: 0.15,        // Irrigation delivered vs ET-based requirement
  cropStage: 0.15,       // On-schedule vigor for growth stage
  activeProblem: 0.30,   // Open issues, weighted by severity (The big mover!)
  monitoringRecency: 0.10,// Recency of scans/data
  treatmentResponse: 0.10 // Follow-up trend: Improved / No Change / Got Worse
};

export const SEVERITY_PENALTIES = {
  none: 0,
  early: 30,     // Early / low severity
  moderate: 55,  // Moderate severity
  severe: 80     // Severe / spreading
};

export const HEALTH_BANDS = [
  { name: 'Unrated', min: -1, max: -1, color: '#94a3b8', bg: '#f1f5f9', badge: 'Unrated (Null)' },
  { name: 'Critical', min: 0, max: 39, color: '#ef4444', bg: '#fef2f2', badge: 'Critical Risk' },
  { name: 'Poor', min: 40, max: 59, color: '#f97316', bg: '#fff7ed', badge: 'Poor Health' },
  { name: 'Watch', min: 60, max: 74, color: '#eab308', bg: '#fefce8', badge: 'Watch / Monitor' },
  { name: 'Good', min: 75, max: 89, color: '#22c55e', bg: '#f0fdf4', badge: 'Good Health' },
  { name: 'Excellent', min: 90, max: 100, color: '#15803d', bg: '#dcfce7', badge: 'Excellent' }
];

export function calculateHealthScore(subindices) {
  if (!subindices || subindices.isUnrated) {
    return {
      score: null,
      band: HEALTH_BANDS[0],
      breakdown: subindices
    };
  }

  // Active problem subindex = 100 - sum(severity_penalties), floored at 0
  const activeProblemSubindex = Math.max(0, 100 - (subindices.problemPenalty || 0));

  const weightedSum =
    (subindices.environmental * HEALTH_WEIGHTS.environmental) +
    (subindices.resource * HEALTH_WEIGHTS.resource) +
    (subindices.cropStage * HEALTH_WEIGHTS.cropStage) +
    (activeProblemSubindex * HEALTH_WEIGHTS.activeProblem) +
    (subindices.monitoringRecency * HEALTH_WEIGHTS.monitoringRecency) +
    (subindices.treatmentResponse * HEALTH_WEIGHTS.treatmentResponse);

  const finalScore = Math.min(100, Math.max(0, Math.round(weightedSum)));

  const band = HEALTH_BANDS.find(b => finalScore >= b.min && finalScore <= b.max) || HEALTH_BANDS[0];

  return {
    score: finalScore,
    band,
    weightedSum,
    breakdown: {
      environmental: subindices.environmental,
      resource: subindices.resource,
      cropStage: subindices.cropStage,
      activeProblem: activeProblemSubindex,
      problemPenalty: subindices.problemPenalty || 0,
      monitoringRecency: subindices.monitoringRecency,
      treatmentResponse: subindices.treatmentResponse
    }
  };
}

// PRD §7.4 Worked Reconciliations (The Brief's exact numbers)
export const PRESET_SCENARIOS = {
  unrated: {
    id: 'unrated',
    title: 'Day 0: Onboarding (Unrated)',
    description: 'Day 0 with incomplete inputs is Unrated (null), never 0. A low number means bad health, never missing data.',
    state: { isUnrated: true, statusText: 'Pending Land & Weather Sync' }
  },
  baseline: {
    id: 'baseline',
    title: 'Day 1: Baseline Sync (82 / 100)',
    description: 'Land, soil, and live weather synced. No active disease (Problem Load = 100). Healthy real-world baseline.',
    subindices: {
      environmental: 80,
      resource: 85,
      cropStage: 80,
      problemPenalty: 0, // No active problems (Subindex 4 = 100)
      monitoringRecency: 75,
      treatmentResponse: 70
    },
    targetScore: 82,
    qualitative: 'Farm conditions normal. Paddy vegetative stage progressing on schedule with balanced moisture.'
  },
  diagnosedBLB: {
    id: 'diagnosedBLB',
    title: 'Day 22: BLB Diagnosed (68 / 100)',
    description: 'Early Bacterial Leaf Blight detected (Penalty 30). Subindex 4 drops to 70. 0.30 weight drops score immediately from 82 → 68 (Watch).',
    subindices: {
      environmental: 75,
      resource: 80,
      cropStage: 75,
      problemPenalty: 30, // Early BLB
      monitoringRecency: 90, // Just scanned
      treatmentResponse: 50  // Awaiting response
    },
    targetScore: 68,
    qualitative: 'Action required: Early Bacterial Leaf Blight identified. Reduce standing water and avoid nitrogen top-dressing.'
  },
  gotWorse: {
    id: 'gotWorse',
    title: 'Day 25: Got Worse → Auto-Escalated (54 / 100)',
    description: 'Follow-up check-in: Farmer reported "Got Worse". Severity promoted to Moderate (Penalty 55). Triggers auto-escalation to KVK agronomist.',
    subindices: {
      environmental: 70,
      resource: 75,
      cropStage: 65,
      problemPenalty: 55, // Moderate/Spreading BLB
      monitoringRecency: 95,
      treatmentResponse: 20  // Declining
    },
    targetScore: 54,
    qualitative: 'Critical Watch: Symptom progression detected. Case pre-packaged and auto-routed to Thanjavur KVK Officer.'
  },
  recovered: {
    id: 'recovered',
    title: 'Post-Expert Resolution (86 / 100)',
    description: 'KVK Agronomist intervention applied and verified. Active problem cleared (Subindex 4 = 100). High monitoring and logged treatment place farm above initial baseline (86 > 82).',
    subindices: {
      environmental: 85,
      resource: 90,
      cropStage: 85,
      problemPenalty: 0, // Cleared
      monitoringRecency: 90,
      treatmentResponse: 95  // Successfully resolved
    },
    targetScore: 86,
    qualitative: 'Excellent recovery: Bactericide treatment completed. Canopy vigor restored to optimal vegetative trajectory.'
  }
};
