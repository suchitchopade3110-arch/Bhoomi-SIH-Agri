class HealthSubIndices {
  final double environmentalSuitability;
  final double resourceAdequacy;
  final double cropStageProgression;
  final double activeProblemLoad;
  final double monitoringRecency;
  final double treatmentResponse;

  const HealthSubIndices({
    required this.environmentalSuitability,
    required this.resourceAdequacy,
    required this.cropStageProgression,
    required this.activeProblemLoad,
    required this.monitoringRecency,
    required this.treatmentResponse,
  });

  factory HealthSubIndices.fromJson(dynamic json) {
    if (json is List) {
      double env = 0.85;
      double res = 0.78;
      double crop = 0.90;
      double prob = 0.95;
      double rec = 0.70;
      double treat = 0.88;

      for (final item in json) {
        if (item is Map<String, dynamic>) {
          final key = item['key']?.toString().toLowerCase() ?? '';
          final val = (item['value'] as num?)?.toDouble() ??
              (item['score'] as num?)?.toDouble();
          if (val != null) {
            if (key.contains('environment') || key.contains('soil') || key.contains('weather')) {
              env = val;
            } else if (key.contains('resource') || key.contains('moisture') || key.contains('water')) {
              res = val;
            } else if (key.contains('crop') || key.contains('vigour') || key.contains('growth') || key.contains('stage')) {
              crop = val;
            } else if (key.contains('problem') || key.contains('pest') || key.contains('load')) {
              prob = val;
            } else if (key.contains('monitoring') || key.contains('recency') || key.contains('integrity')) {
              rec = val;
            } else if (key.contains('treatment') || key.contains('response')) {
              treat = val;
            }
          }
        }
      }

      return HealthSubIndices(
        environmentalSuitability: env,
        resourceAdequacy: res,
        cropStageProgression: crop,
        activeProblemLoad: prob,
        monitoringRecency: rec,
        treatmentResponse: treat,
      );
    }

    if (json is Map<String, dynamic>) {
      return HealthSubIndices(
        environmentalSuitability: (json['environmental_suitability'] as num?)?.toDouble() ??
            (json['soil_moisture'] as num?)?.toDouble() ?? 0.85,
        resourceAdequacy: (json['resource_adequacy'] as num?)?.toDouble() ??
            (json['irrigation_adequacy'] as num?)?.toDouble() ?? 0.78,
        cropStageProgression: (json['crop_stage_progression'] as num?)?.toDouble() ??
            (json['crop_vigour'] as num?)?.toDouble() ?? 0.90,
        activeProblemLoad: (json['active_problem_load'] as num?)?.toDouble() ??
            (json['pest_disease_risk'] as num?)?.toDouble() ?? 0.95,
        monitoringRecency: (json['monitoring_recency'] as num?)?.toDouble() ??
            (json['land_integrity'] as num?)?.toDouble() ?? 0.70,
        treatmentResponse: (json['treatment_response'] as num?)?.toDouble() ?? 0.88,
      );
    }

    return const HealthSubIndices(
      environmentalSuitability: 0.85,
      resourceAdequacy: 0.78,
      cropStageProgression: 0.90,
      activeProblemLoad: 0.95,
      monitoringRecency: 0.70,
      treatmentResponse: 0.88,
    );
  }

  Map<String, dynamic> toJson() => {
        'environmental_suitability': environmentalSuitability,
        'resource_adequacy': resourceAdequacy,
        'crop_stage_progression': cropStageProgression,
        'active_problem_load': activeProblemLoad,
        'monitoring_recency': monitoringRecency,
        'treatment_response': treatmentResponse,
      };
}

class HealthSnapshot {
  final int? score;
  final String band;
  final String? computedAt;
  final String? explanation;
  final HealthSubIndices? subIndices;

  const HealthSnapshot({
    this.score,
    required this.band,
    this.computedAt,
    this.explanation,
    this.subIndices,
  });

  bool get isRated => score != null;

  factory HealthSnapshot.fromJson(Map<String, dynamic> json) {
    final dynamic rawSubIndices = json['sub_indices'] ?? json['subindices'];
    final rawScore = json['score'] ?? json['composite_score'] ?? json['current_health_score'];

    return HealthSnapshot(
      score: rawScore is num ? rawScore.toInt() : null,
      band: json['band'] as String? ?? json['health_band'] as String? ?? (rawScore != null ? 'good' : 'unrated'),
      computedAt: json['computed_at'] as String? ?? json['created_at'] as String?,
      explanation: json['explanation'] as String?,
      subIndices: rawSubIndices != null
          ? HealthSubIndices.fromJson(rawSubIndices)
          : (json.containsKey('environmental_suitability') || json.containsKey('soil_moisture')
              ? HealthSubIndices.fromJson(json)
              : null),
    );
  }

  Map<String, dynamic> toJson() => {
        'score': score,
        'band': band,
        if (computedAt != null) 'computed_at': computedAt,
        if (explanation != null) 'explanation': explanation,
        if (subIndices != null) 'sub_indices': subIndices!.toJson(),
      };
}
