import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
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
    try {
      final response = await _apiClient.post(
        ApiConstants.farmDiagnose(farmId),
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return DiagnosisResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid diagnosis response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return DiagnosisResponse(
          diagnosisId: 'prob_blb_001',
          farmId: farmId,
          possibleIssue: 'Bacterial Leaf Blight (Xanthomonas oryzae)',
          confidenceLevel: 'high',
          confidenceScore: 0.88,
          symptomsToCheck: const [
            'Water-soaked yellowish stripes on leaf blades starting from tips',
            'Bacterial ooze droplets during humid morning hours',
            'Wilting of young tillers (Kresek phase)',
          ],
          actions: const [
            'Drain excess standing water from the field for 3-4 days',
            'Apply recommended bio-control Pseudomonas fluorescens @ 2.5 kg/ha',
            'Maintain balanced potash fertilization to strengthen leaf tissues',
          ],
          caution: 'Do not apply excess nitrogen top-dressing while disease symptoms are active.',
          sources: const [
            AdvisorySource(
              title: 'TNAU Agriteck Crop Protection Protocol — Bacterial Leaf Blight',
              organization: 'Tamil Nadu Agricultural University (TNAU)',
            ),
            AdvisorySource(
              title: 'ICAR National Rice Research Institute Advisory Guide',
              organization: 'ICAR-NRRI',
            ),
          ],
          canEscalate: true,
          spokenSummary: 'Detected Bacterial Leaf Blight with 88% confidence. Please drain standing water and apply bio-control treatment.',
          createdAt: DateTime.now().toIso8601String(),
        );
      }
      rethrow;
    }
  }
}
