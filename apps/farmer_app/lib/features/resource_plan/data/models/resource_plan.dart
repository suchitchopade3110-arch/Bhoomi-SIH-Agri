class ExplainabilityInputs {
  final double? evapotranspirationEt0;
  final double? cropStageKc;
  final double? effectiveRainfallMm;
  final double? soilRetentionFactor;
  final String? formulaDescription;

  const ExplainabilityInputs({
    this.evapotranspirationEt0,
    this.cropStageKc,
    this.effectiveRainfallMm,
    this.soilRetentionFactor,
    this.formulaDescription,
  });

  factory ExplainabilityInputs.fromJson(Map<String, dynamic> json) {
    return ExplainabilityInputs(
      evapotranspirationEt0: (json['evapotranspiration_et0'] as num?)?.toDouble() ?? (json['et0'] as num?)?.toDouble(),
      cropStageKc: (json['crop_stage_kc'] as num?)?.toDouble() ?? (json['kc'] as num?)?.toDouble(),
      effectiveRainfallMm: (json['effective_rainfall_mm'] as num?)?.toDouble() ?? (json['rainfall'] as num?)?.toDouble(),
      soilRetentionFactor: (json['soil_retention_factor'] as num?)?.toDouble(),
      formulaDescription: json['formula_description'] as String? ?? 'Crop Water Need = ET0 × Kc adjusted for effective rainfall',
    );
  }

  Map<String, dynamic> toJson() => {
        if (evapotranspirationEt0 != null) 'evapotranspiration_et0': evapotranspirationEt0,
        if (cropStageKc != null) 'crop_stage_kc': cropStageKc,
        if (effectiveRainfallMm != null) 'effective_rainfall_mm': effectiveRainfallMm,
        if (soilRetentionFactor != null) 'soil_retention_factor': soilRetentionFactor,
        if (formulaDescription != null) 'formula_description': formulaDescription,
      };
}

class ResourcePlan {
  final String id;
  final String farmId;
  final double tillableAreaAcres;
  final double seedRateKgPerAcre;
  final double totalSeedRequirementKg;
  final double? et0MmPerDay;
  final double? cropCoefficientKc;
  final double? cropWaterNeedMm;
  final double irrigationAmount;
  final String irrigationUnit;
  final String irrigationAdvice;
  final ExplainabilityInputs? explainabilityInputs;
  final String createdAt;

  const ResourcePlan({
    required this.id,
    required this.farmId,
    required this.tillableAreaAcres,
    required this.seedRateKgPerAcre,
    required this.totalSeedRequirementKg,
    this.et0MmPerDay,
    this.cropCoefficientKc,
    this.cropWaterNeedMm,
    required this.irrigationAmount,
    required this.irrigationUnit,
    required this.irrigationAdvice,
    this.explainabilityInputs,
    required this.createdAt,
  });

  factory ResourcePlan.fromJson(Map<String, dynamic> json) {
    final irri = json['irrigation_plan'] as Map<String, dynamic>?;

    final tillableArea = (irri?['area_acres'] as num?)?.toDouble() ??
        (json['tillable_area_acres'] as num?)?.toDouble() ??
        2.0;

    final seedReq = (json['recommended_seed_kg'] as num?)?.toDouble() ??
        (json['total_seed_requirement_kg'] as num?)?.toDouble() ??
        57.0;

    final et0 = (irri?['et0_mm_day'] as num?)?.toDouble() ??
        (json['et0_mm_per_day'] as num?)?.toDouble() ??
        4.8;

    final kc = (irri?['kc_factor'] as num?)?.toDouble() ??
        (json['crop_coefficient_kc'] as num?)?.toDouble() ??
        1.15;

    final waterNeed = (irri?['irrigation_need_mm'] as num?)?.toDouble() ??
        (json['crop_water_need_mm'] as num?)?.toDouble() ??
        5.5;

    final irriAmount = (irri?['daily_liters_total'] as num?)?.toDouble() ??
        (json['irrigation_amount'] as num?)?.toDouble() ??
        2200.0;

    final explain = json['explainability_inputs'] != null
        ? ExplainabilityInputs.fromJson(json['explainability_inputs'] as Map<String, dynamic>)
        : irri != null
            ? ExplainabilityInputs(
                evapotranspirationEt0: (irri['et0_mm_day'] as num?)?.toDouble(),
                cropStageKc: (irri['kc_factor'] as num?)?.toDouble(),
                effectiveRainfallMm: (irri['effective_rainfall_mm'] as num?)?.toDouble(),
                formulaDescription: irri['calculation_formula'] as String?,
              )
            : null;

    return ResourcePlan(
      id: json['id'] as String? ?? 'rp_default',
      farmId: json['farm_id'] as String? ?? '',
      tillableAreaAcres: tillableArea,
      seedRateKgPerAcre: (json['seed_rate_kg_per_acre'] as num?)?.toDouble() ?? (tillableArea > 0 ? seedReq / tillableArea : 28.5),
      totalSeedRequirementKg: seedReq,
      et0MmPerDay: et0,
      cropCoefficientKc: kc,
      cropWaterNeedMm: waterNeed,
      irrigationAmount: irriAmount,
      irrigationUnit: json['irrigation_unit'] as String? ?? 'Litres / Day',
      irrigationAdvice: json['irrigation_advice'] as String? ??
          'Apply ${(irriAmount).toStringAsFixed(0)} L through standard field irrigation.',
      explainabilityInputs: explain,
      createdAt: json['created_at'] as String? ?? DateTime.now().toIso8601String(),
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'farm_id': farmId,
        'tillable_area_acres': tillableAreaAcres,
        'seed_rate_kg_per_acre': seedRateKgPerAcre,
        'total_seed_requirement_kg': totalSeedRequirementKg,
        if (et0MmPerDay != null) 'et0_mm_per_day': et0MmPerDay,
        if (cropCoefficientKc != null) 'crop_coefficient_kc': cropCoefficientKc,
        if (cropWaterNeedMm != null) 'crop_water_need_mm': cropWaterNeedMm,
        'irrigation_amount': irrigationAmount,
        'irrigation_unit': irrigationUnit,
        'irrigation_advice': irrigationAdvice,
        if (explainabilityInputs != null) 'explainability_inputs': explainabilityInputs!.toJson(),
        'created_at': createdAt,
      };
}
