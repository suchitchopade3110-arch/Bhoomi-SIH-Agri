import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'diagnosis_api_service.dart';
import 'models/diagnose_request.dart';
import 'models/diagnosis_response.dart';

final diagnosisRepositoryProvider = Provider<DiagnosisRepository>((ref) {
  final apiService = ref.watch(diagnosisApiServiceProvider);
  return DiagnosisRepository(apiService);
});

class DiagnosisRepository {
  final DiagnosisApiService _apiService;

  DiagnosisRepository(this._apiService);

  Future<DiagnosisResponse> diagnoseCrop({
    required String farmId,
    required DiagnoseRequest request,
  }) async {
    return await _apiService.diagnoseCrop(farmId: farmId, request: request);
  }
}
