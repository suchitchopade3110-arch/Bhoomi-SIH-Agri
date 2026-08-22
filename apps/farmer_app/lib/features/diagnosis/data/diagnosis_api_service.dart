import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/diagnose_request.dart';
import 'models/diagnosis_response.dart';

final diagnosisApiServiceProvider = Provider<DiagnosisApiService>((ref) {
  return DiagnosisApiService(ApiClient());
});

class DiagnosisApiService {
  final ApiClient _apiClient;

  DiagnosisApiService(this._apiClient);

  Future<DiagnosisResponse> diagnoseCrop({
    required String farmId,
    required DiagnoseRequest request,
  }) async {
    final response = await _apiClient.post(
      ApiConstants.farmDiagnose(farmId),
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return DiagnosisResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid diagnosis response format.');
  }
}
