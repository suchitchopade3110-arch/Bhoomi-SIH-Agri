// PRD §5.7 & §5.8: Curated Agricultural Corpus & 5-Point Advisory
// Strict grounding with ICAR/TNAU source citations and confidence gating

export const CURATED_CORPUS = [
  {
    id: 'blb-paddy',
    crop: 'Paddy',
    disease: 'Bacterial Leaf Blight (Xanthomonas oryzae)',
    citation: 'ICAR-CRRI Rice Advisory Bulletin 2024 / TNAU Crop Production Guide (Updated Oct 2024)',
    curator: 'Dr. S. Ramanathan, Principal Scientist (Plant Pathology), ICAR-CRRI',
    confidenceThreshold: 0.72,
    distinguishingCues: 'Water-soaked wavy lesions starting from leaf tips moving downward along leaf margins with creamy bacterial ooze in early morning.',
    advisory5Point: {
      possibleIssue: 'Bacterial Leaf Blight (BLB) - Early to Moderate Stage',
      whatToCheck: 'Examine leaf tips at early dawn for translucent yellow-orange stripes along margins and tiny turbid droplets of bacterial exudate.',
      whatToDoNext: 'Drain excess standing water immediately to reduce field humidity. Spray Copper Hydroxide (2.0 g/L) + Streptocycline (100 mg/L) during dry morning hours.',
      whatToAvoid: 'CRITICAL: Do NOT top-dress nitrogen (Urea) until disease halts. Avoid evening sprinkler irrigation that splashes bacterial cells to adjoining plants.',
      expertTriggers: 'Stop and escalate to KVK if lesion coverage exceeds 25% of top canopy, or if wilting (Kresek phase) is observed on tillers.'
    }
  },
  {
    id: 'blast-paddy',
    crop: 'Paddy',
    disease: 'Rice Blast (Magnaporthe oryzae)',
    citation: 'ICAR Package of Practices for Kharif Rice & TNAU Agri-Portal (Reviewed Dec 2024)',
    curator: 'Dr. M. Soundararajan, Agronomy Specialist, Tamil Nadu Agricultural University',
    confidenceThreshold: 0.75,
    distinguishingCues: 'Spindle/eye-shaped lesions with grayish ash center and dark brown or reddish borders on leaf blade.',
    advisory5Point: {
      possibleIssue: 'Leaf Blast / Node Blast',
      whatToCheck: 'Look for elliptical diamond-shaped spots on younger leaves with gray centres and yellow halos.',
      whatToDoNext: 'Foliar spray of Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 mL/L at the first appearance of leaf spots.',
      whatToAvoid: 'Avoid excessive nitrogen fertilization. Do not allow field to undergo severe moisture stress followed by sudden flooding.',
      expertTriggers: 'Escalate if neck/panicle blast strikes before grain emergence (risk of total grain sterility).'
    }
  },
  {
    id: 'stem-borer-paddy',
    crop: 'Paddy',
    disease: 'Yellow Stem Borer (Scirpophaga incertulas)',
    citation: 'Directorate of Rice Research (ICAR-IIRR) IPM Guidelines 2024',
    curator: 'Dr. A. K. Nayak, Entomologist, ICAR-IIRR Hyderabad',
    confidenceThreshold: 0.70,
    distinguishingCues: 'Dead central shoots (deadheart) during vegetative stage or dried empty panicles (whitehead) at reproductive stage.',
    advisory5Point: {
      possibleIssue: 'Yellow Stem Borer Infestation',
      whatToCheck: 'Tug the central leaf shoot. If it pulls out easily with an unpleasant decaying smell or visible frass at base, stem borer is confirmed.',
      whatToDoNext: 'Install pheromone traps @ 5 per acre. Release egg parasitoid Trichogramma japonicum @ 1,00,000/ha or apply Cartap Hydrochloride 4G @ 10 kg/acre.',
      whatToAvoid: 'Avoid blanket insecticide spraying during early vegetative stage to preserve beneficial spiders and mirid bugs.',
      expertTriggers: 'Escalate if deadheart incidence exceeds 10% or if whiteheads appear in more than 5% of panicles.'
    }
  },
  {
    id: 'brown-spot-paddy',
    crop: 'Paddy',
    disease: 'Brown Spot (Bipolaris oryzae)',
    citation: 'ICAR-National Rice Research Institute Cuttack (NRRI Manual 2024)',
    curator: 'Dr. P. C. Rath, Crop Protection Division, NRRI',
    confidenceThreshold: 0.70,
    distinguishingCues: 'Circular to oval dark brown spots resembling sesame seeds, often associated with potash or zinc deficiency.',
    advisory5Point: {
      possibleIssue: 'Brown Spot Disease (Nutritional Stress Linked)',
      whatToCheck: 'Small oval brown spots uniformly scattered across leaf surface, frequently occurring on sandy or nutrient-depleted soils.',
      whatToDoNext: 'Apply balanced MOP (Potassium) fertilizer top dressing. Spray Mancozeb 75% WP @ 2.0 g/L.',
      whatToAvoid: 'Do not ignore soil nutrient exhaustion; fungus proliferates predominantly on nutrient-starved crops.',
      expertTriggers: 'Escalate if spots progress to panicle glumes causing grain discoloration.'
    }
  }
];

export const MOCK_DIAGNOSES = [
  {
    id: 'diag-1',
    imageName: 'paddy_leaf_blb.jpg',
    crop: 'Paddy',
    confidence: 0.88, // Above threshold (0.72) -> Auto Advisory
    isAboveGate: true,
    topMatch: CURATED_CORPUS[0],
    alternatives: [
      { name: 'Bacterial Leaf Blight', confidence: '88%', status: 'Primary Diagnosis' },
      { name: 'Brown Spot', confidence: '8%', status: 'Excluded: Lesion pattern dissimilar' },
      { name: 'Bacterial Leaf Streak', confidence: '4%', status: 'Excluded: Interveinal lines missing' }
    ]
  },
  {
    id: 'diag-2',
    imageName: 'unclear_leaf_specimen.jpg',
    crop: 'Paddy',
    confidence: 0.52, // Below threshold -> Confidence Gate Tripped
    isAboveGate: false,
    reasonCode: 'LOW_CONFIDENCE_GATE_TRIPPED',
    reasonText: 'Image resolution and lighting too low for reliable automatic identification (< 70% threshold).',
    topMatch: null,
    alternatives: [
      { name: 'Sheath Rot', confidence: '52%', status: 'Uncertain' },
      { name: 'False Smut', confidence: '31%', status: 'Uncertain' }
    ],
    escalationAction: 'Case pre-packaged with photo and forwarded to KVK agronomist queue to avoid misdiagnosis crop loss.'
  }
];
