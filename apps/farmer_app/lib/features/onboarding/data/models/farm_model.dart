class FarmModel {
  final String id;
  final String farmName;
  final String? farmerId;
  final String village;
  final String taluk;
  final String district;
  final String state;
  final String primaryCrop;
  final String? crop;
  final String? growthStage;
  final String soilType;
  final String? irrigationSource;
  final double totalAreaAcres;
  final String? surveyNumber;
  final String landStatus;

  const FarmModel({
    required this.id,
    required this.farmName,
    this.farmerId,
    required this.village,
    required this.taluk,
    required this.district,
    this.state = 'Tamil Nadu',
    required this.primaryCrop,
    this.crop,
    this.growthStage,
    required this.soilType,
    this.irrigationSource,
    required this.totalAreaAcres,
    this.surveyNumber,
    required this.landStatus,
  });

  factory FarmModel.fromJson(Map<String, dynamic> json) {
    return FarmModel(
      id: json['id'] as String? ?? json['farm_id'] as String? ?? '',
      farmName: json['farm_name'] as String? ?? json['primary_crop'] as String? ?? 'Farm',
      farmerId: json['farmer_id'] as String?,
      village: json['village'] as String? ?? '',
      taluk: json['taluk'] as String? ?? '',
      district: json['district'] as String? ?? '',
      state: json['state'] as String? ?? 'Tamil Nadu',
      primaryCrop: json['primary_crop'] as String? ?? json['crop'] as String? ?? 'Paddy',
      crop: json['crop'] as String?,
      growthStage: json['growth_stage'] as String?,
      soilType: json['soil_type'] as String? ?? 'Clay Loam',
      irrigationSource: json['irrigation_source'] as String?,
      totalAreaAcres: (json['total_area_acres'] as num?)?.toDouble() ?? 2.0,
      surveyNumber: json['survey_number'] as String?,
      landStatus: json['land_status'] as String? ?? 'pending_verification',
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'farm_name': farmName,
        if (farmerId != null) 'farmer_id': farmerId,
        'village': village,
        'taluk': taluk,
        'district': district,
        'state': state,
        'primary_crop': primaryCrop,
        if (crop != null) 'crop': crop,
        if (growthStage != null) 'growth_stage': growthStage,
        'soil_type': soilType,
        if (irrigationSource != null) 'irrigation_source': irrigationSource,
        'total_area_acres': totalAreaAcres,
        if (surveyNumber != null) 'survey_number': surveyNumber,
        'land_status': landStatus,
      };
}
