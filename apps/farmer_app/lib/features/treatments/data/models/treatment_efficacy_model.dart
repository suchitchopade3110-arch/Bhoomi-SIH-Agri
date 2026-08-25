class TreatmentEfficacyModel {
  final String treatmentId;
  final String pathogen;
  final String crop;
  final String region;
  final String status;
  final int sampleSize;
  final int minSampleThreshold;
  final double? efficacyPercentage;
  final double? avgDaysToRecovery;

  const TreatmentEfficacyModel({
    required this.treatmentId,
    required this.pathogen,
    required this.crop,
    required this.region,
    required this.status,
    required this.sampleSize,
    required this.minSampleThreshold,
    this.efficacyPercentage,
    this.avgDaysToRecovery,
  });

  factory TreatmentEfficacyModel.fromJson(Map<String, dynamic> json) =>
      TreatmentEfficacyModel(
        treatmentId: json['treatment_id']?.toString() ?? '',
        pathogen: json['pathogen']?.toString() ?? '',
        crop: json['crop']?.toString() ?? '',
        region: json['region']?.toString() ?? '',
        status: json['status']?.toString() ?? 'insufficient_data',
        sampleSize: (json['sample_size'] as num?)?.toInt() ?? 0,
        minSampleThreshold: (json['min_sample_threshold'] as num?)?.toInt() ?? 10,
        efficacyPercentage: (json['efficacy_percentage'] as num?)?.toDouble(),
        avgDaysToRecovery: (json['avg_days_to_recovery'] as num?)?.toDouble(),
      );

  Map<String, dynamic> toJson() => {
        'treatment_id': treatmentId,
        'pathogen': pathogen,
        'crop': crop,
        'region': region,
        'status': status,
        'sample_size': sampleSize,
        'min_sample_threshold': minSampleThreshold,
        if (efficacyPercentage != null) 'efficacy_percentage': efficacyPercentage,
        if (avgDaysToRecovery != null) 'avg_days_to_recovery': avgDaysToRecovery,
      };
}
