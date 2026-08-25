import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/treatment_efficacy_model.dart';

final treatmentsApiServiceProvider = Provider<TreatmentsApiService>((ref) {
  return TreatmentsApiService(ApiClient());
});

class TreatmentsApiService {
  final ApiClient _apiClient;

  TreatmentsApiService(this._apiClient);

  Future<TreatmentEfficacyModel> getTreatmentEfficacy({
    required String treatmentId,
    required String pathogen,
    required String crop,
    required String district,
    int windowMonths = 12,
  }) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.treatmentEfficacy(treatmentId),
        queryParameters: {
          'pathogen': pathogen,
          'crop': crop,
          'district': district,
          'window_months': windowMonths,
        },
      );

      if (response.data is Map<String, dynamic>) {
        return TreatmentEfficacyModel.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid treatment efficacy response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return TreatmentEfficacyModel(
          treatmentId: treatmentId,
          pathogen: pathogen,
          crop: crop,
          region: district,
          status: 'statistically_significant',
          sampleSize: 14,
          minSampleThreshold: 10,
          efficacyPercentage: 84.5,
          avgDaysToRecovery: 6.2,
        );
      }
      rethrow;
    }
  }
}
