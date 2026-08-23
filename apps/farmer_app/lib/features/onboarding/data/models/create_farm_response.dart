class FarmHealthInitial {
  final String band;
  final int? score;

  const FarmHealthInitial({
    required this.band,
    this.score,
  });

  factory FarmHealthInitial.fromJson(Map<String, dynamic> json) {
    return FarmHealthInitial(
      band: json['band'] as String? ?? 'unrated',
      score: json['score'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'band': band,
      'score': score,
    };
  }
}

class CreateFarmResponse {
  final String id;
  final String landStatus;
  final FarmHealthInitial health;
  final List<String>? missingFields;

  const CreateFarmResponse({
    required this.id,
    required this.landStatus,
    required this.health,
    this.missingFields,
  });

  factory CreateFarmResponse.fromJson(Map<String, dynamic> json) {
    return CreateFarmResponse(
      id: json['id'] as String? ?? '',
      landStatus: json['land_status'] as String? ?? 'pending_verification',
      health: json['health'] != null
          ? FarmHealthInitial.fromJson(json['health'] as Map<String, dynamic>)
          : const FarmHealthInitial(band: 'unrated', score: null),
      missingFields: json['missing_fields'] != null
          ? List<String>.from(json['missing_fields'] as List)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'land_status': landStatus,
      'health': health.toJson(),
      if (missingFields != null) 'missing_fields': missingFields,
    };
  }
}
