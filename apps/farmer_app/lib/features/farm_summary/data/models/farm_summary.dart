class FarmIdentity {
  final String id;
  final String crop;
  final String landStatus;

  const FarmIdentity({
    required this.id,
    required this.crop,
    required this.landStatus,
  });

  factory FarmIdentity.fromJson(Map<String, dynamic> json) {
    return FarmIdentity(
      id: json['id'] as String? ?? '',
      crop: json['primary_crop'] as String? ?? json['crop'] as String? ?? '',
      landStatus: json['land_status'] as String? ?? 'pending_verification',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'crop': crop,
      'land_status': landStatus,
    };
  }
}

class FarmHealth {
  final int? score;
  final String band;
  final String? computedAt;

  const FarmHealth({
    this.score,
    required this.band,
    this.computedAt,
  });

  bool get isRated => score != null;

  factory FarmHealth.fromJson(Map<String, dynamic> json) {
    final rawScore = json['score'] ?? json['current_health_score'] ?? json['composite_score'];
    return FarmHealth(
      score: (rawScore as num?)?.toInt(),
      band: json['band'] as String? ?? json['health_band'] as String? ?? (rawScore != null ? 'rated' : 'unrated'),
      computedAt: json['computed_at'] as String? ?? json['created_at'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'score': score,
      'band': band,
      if (computedAt != null) 'computed_at': computedAt,
    };
  }
}

class FarmSummary {
  final FarmIdentity farm;
  final FarmHealth health;
  final int openProblems;
  final int pendingFollowups;
  final String? latestResourcePlanId;

  const FarmSummary({
    required this.farm,
    required this.health,
    required this.openProblems,
    required this.pendingFollowups,
    this.latestResourcePlanId,
  });

  factory FarmSummary.fromJson(Map<String, dynamic> json) {
    final farmMap = json['farm'] as Map<String, dynamic>? ?? {};
    final healthMap = json['health'] as Map<String, dynamic>? ??
        (farmMap.containsKey('current_health_score')
            ? {'score': farmMap['current_health_score'], 'band': farmMap['current_health_score'] != null ? 'good' : 'unrated'}
            : {});

    return FarmSummary(
      farm: FarmIdentity.fromJson(farmMap),
      health: FarmHealth.fromJson(healthMap),
      openProblems: (json['open_cases_count'] as num?)?.toInt() ??
          (json['active_advisories_count'] as num?)?.toInt() ??
          (json['open_problems'] as num?)?.toInt() ??
          0,
      pendingFollowups: (json['pending_followups'] as num?)?.toInt() ?? 0,
      latestResourcePlanId: json['latest_resource_plan_id'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'farm': farm.toJson(),
      'health': health.toJson(),
      'open_problems': openProblems,
      'pending_followups': pendingFollowups,
      if (latestResourcePlanId != null) 'latest_resource_plan_id': latestResourcePlanId,
    };
  }
}
