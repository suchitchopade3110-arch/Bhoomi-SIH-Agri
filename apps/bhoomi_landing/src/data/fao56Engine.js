// PRD §5.4: Smart Land & Resource Planner (FAO-56 Penman-Monteith)
// Water Need = ET0 * Kc - Effective Rainfall

export const CROP_KC_VALUES = {
  paddy: {
    name: 'Samba Paddy (Rice)',
    stages: {
      initial: { name: 'Initial / Transplanting (0-20d)', kc: 1.10 },
      vegetative: { name: 'Vegetative / Tillering (20-50d)', kc: 1.15 },
      reproductive: { name: 'Panicle / Flowering (50-80d)', kc: 1.25 },
      maturation: { name: 'Ripening / Maturity (80-110d)', kc: 0.95 }
    },
    seedRateKgPerAcre: 20 // 20 kg/acre for transplanted Samba Paddy
  },
  wheat: {
    name: 'Wheat',
    stages: {
      initial: { name: 'Crown Root (0-25d)', kc: 0.40 },
      vegetative: { name: 'Tillering / Jointing (25-60d)', kc: 0.85 },
      reproductive: { name: 'Heading / Flowering (60-90d)', kc: 1.15 },
      maturation: { name: 'Grain Filling / Maturity (90-120d)', kc: 0.45 }
    },
    seedRateKgPerAcre: 40
  },
  cotton: {
    name: 'Cotton',
    stages: {
      initial: { name: 'Early Vegetative (0-30d)', kc: 0.45 },
      vegetative: { name: 'Square Formation (30-65d)', kc: 0.75 },
      reproductive: { name: 'Boll Development (65-115d)', kc: 1.20 },
      maturation: { name: 'Boll Opening (115-150d)', kc: 0.65 }
    },
    seedRateKgPerAcre: 8
  }
};

/**
 * Calculates daily dynamic irrigation budget based on FAO-56 Penman-Monteith
 * @param {Object} params
 * @param {string} params.cropKey - e.g. 'paddy'
 * @param {string} params.stageKey - e.g. 'vegetative'
 * @param {number} params.areaAcres - Land area in acres (1 acre = 4046.86 m²)
 * @param {number} params.et0MmDay - Reference Evapotranspiration ET₀ (mm/day) from weather API
 * @param {number} params.rainfallMm - Forecasted/actual daily rainfall (mm)
 * @param {number} params.effectiveRainfallPct - Usable percentage of rainfall (default ~0.75)
 */
export function calculateDynamicIrrigation({
  cropKey = 'paddy',
  stageKey = 'vegetative',
  areaAcres = 2.0,
  et0MmDay = 4.8, // Typical tropical summer/monsoon baseline
  rainfallMm = 2.0,
  effectiveRainfallPct = 0.75
}) {
  const crop = CROP_KC_VALUES[cropKey] || CROP_KC_VALUES.paddy;
  const stage = crop.stages[stageKey] || crop.stages.vegetative;
  const kc = stage.kc;

  // 1 acre = 4046.86 sq meters. 1 mm of water depth over 1 sq meter = 1 Liter.
  const areaSqMeters = areaAcres * 4046.86;

  // Gross Crop Water Need (mm/day) = ET0 * Kc
  const grossWaterNeedMm = et0MmDay * kc;

  // Effective Rainfall (mm/day)
  const effectiveRainMm = Math.max(0, rainfallMm * effectiveRainfallPct);

  // Net Irrigation Requirement (mm/day) = max(0, Gross - Effective Rain)
  const netIrrigationMm = Math.max(0, grossWaterNeedMm - effectiveRainMm);

  // Total daily budget in Liters = netIrrigationMm * areaSqMeters
  const dailyBudgetLiters = Math.round(netIrrigationMm * areaSqMeters);

  // Total Seed Mass Requirement
  const totalSeedKg = Math.round(areaAcres * crop.seedRateKgPerAcre);

  return {
    cropName: crop.name,
    stageName: stage.name,
    areaAcres,
    et0MmDay,
    kc,
    grossWaterNeedMm: parseFloat(grossWaterNeedMm.toFixed(2)),
    rainfallMm,
    effectiveRainMm: parseFloat(effectiveRainMm.toFixed(2)),
    netIrrigationMm: parseFloat(netIrrigationMm.toFixed(2)),
    dailyBudgetLiters,
    totalSeedKg,
    advisoryNote: netIrrigationMm <= 1.0 
      ? 'Rainfall meets or exceeds evapotranspiration. Delay mechanical irrigation today to conserve energy and prevent root waterlogging.'
      : `Deliver ~${(dailyBudgetLiters / 1000).toFixed(1)} m³ (${dailyBudgetLiters.toLocaleString()} L) of water today to match stage evapotranspiration.`
  };
}
