class CreateFarmRequest {
  final String crop;
  final double areaAcresSelfReported;
  final String growthStage;
  final String soilType;
  final String irrigationAccess;
  final String season;

  const CreateFarmRequest({
    required this.crop,
    required this.areaAcresSelfReported,
    required this.growthStage,
    required this.soilType,
    required this.irrigationAccess,
    required this.season,
  });

  Map<String, dynamic> toJson() {
    return {
      'farmer_id': 'u_farmer_1',
      'farm_name': 'My Farm ($crop)',
      'primary_crop': crop,
      'crop': crop,
      'total_area_acres': areaAcresSelfReported > 0 ? areaAcresSelfReported : 2.0,
      'area_acres_self_reported': areaAcresSelfReported,
      'growth_stage': growthStage.isNotEmpty ? growthStage.toLowerCase() : 'vegetative',
      'soil_type': soilType.isNotEmpty ? soilType : 'Clay Loam',
      'irrigation_source': irrigationAccess.isNotEmpty ? irrigationAccess : 'Borewell',
      'irrigation_access': irrigationAccess,
      'season': season,
      'village': 'Perundurai',
      'taluk': 'Erode',
      'district': 'Erode',
      'state': 'Tamil Nadu',
      'latitude': 11.2742,
      'longitude': 77.5828,
    };
  }

  factory CreateFarmRequest.fromJson(Map<String, dynamic> json) {
    return CreateFarmRequest(
      crop: json['crop'] as String? ?? '',
      areaAcresSelfReported: (json['area_acres_self_reported'] as num?)?.toDouble() ?? 0.0,
      growthStage: json['growth_stage'] as String? ?? '',
      soilType: json['soil_type'] as String? ?? '',
      irrigationAccess: json['irrigation_access'] as String? ?? '',
      season: json['season'] as String? ?? '',
    );
  }

  CreateFarmRequest copyWith({
    String? crop,
    double? areaAcresSelfReported,
    String? growthStage,
    String? soilType,
    String? irrigationAccess,
    String? season,
  }) {
    return CreateFarmRequest(
      crop: crop ?? this.crop,
      areaAcresSelfReported: areaAcresSelfReported ?? this.areaAcresSelfReported,
      growthStage: growthStage ?? this.growthStage,
      soilType: soilType ?? this.soilType,
      irrigationAccess: irrigationAccess ?? this.irrigationAccess,
      season: season ?? this.season,
    );
  }
}
