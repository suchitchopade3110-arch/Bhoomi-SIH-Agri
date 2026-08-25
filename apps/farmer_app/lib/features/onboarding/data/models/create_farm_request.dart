class CreateFarmRequest {
  final String crop;
  final String growthStage;
  final String region;
  final double? areaAcresSelfReported;
  final String soilType;
  final String irrigationAccess;
  final String season;

  const CreateFarmRequest({
    required this.crop,
    required this.growthStage,
    required this.region,
    this.areaAcresSelfReported,
    this.soilType = 'Clay Loam',
    this.irrigationAccess = 'Borewell',
    this.season = 'samba',
  });

  Map<String, dynamic> toJson() {
    return {
      'farmer_id': 'u_farmer_1',
      'farm_name': 'My Farm ($crop)',
      'primary_crop': crop,
      'crop': crop,
      'growth_stage': growthStage.isNotEmpty ? growthStage.toLowerCase() : 'vegetative',
      'region': region.isNotEmpty ? region : 'Cauvery Delta',
      'soil_type': soilType.isNotEmpty ? soilType : 'Clay Loam',
      'irrigation_source': irrigationAccess.isNotEmpty ? irrigationAccess : 'Borewell',
      'irrigation_access': irrigationAccess,
      'season': season,
      if (areaAcresSelfReported != null && areaAcresSelfReported! > 0)
        'area_acres_self_reported': areaAcresSelfReported,
      if (areaAcresSelfReported != null && areaAcresSelfReported! > 0)
        'total_area_acres': areaAcresSelfReported,
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
      growthStage: json['growth_stage'] as String? ?? '',
      region: json['region'] as String? ?? 'Cauvery Delta',
      areaAcresSelfReported: (json['area_acres_self_reported'] as num?)?.toDouble(),
      soilType: json['soil_type'] as String? ?? 'Clay Loam',
      irrigationAccess: json['irrigation_access'] as String? ?? 'Borewell',
      season: json['season'] as String? ?? 'samba',
    );
  }

  CreateFarmRequest copyWith({
    String? crop,
    String? growthStage,
    String? region,
    double? areaAcresSelfReported,
    String? soilType,
    String? irrigationAccess,
    String? season,
  }) {
    return CreateFarmRequest(
      crop: crop ?? this.crop,
      growthStage: growthStage ?? this.growthStage,
      region: region ?? this.region,
      areaAcresSelfReported: areaAcresSelfReported ?? this.areaAcresSelfReported,
      soilType: soilType ?? this.soilType,
      irrigationAccess: irrigationAccess ?? this.irrigationAccess,
      season: season ?? this.season,
    );
  }
}
