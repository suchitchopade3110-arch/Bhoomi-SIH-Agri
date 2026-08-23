import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/escalation_models.dart';

final escalationApiServiceProvider = Provider<EscalationApiService>((ref) {
  return EscalationApiService(ApiClient());
});

class EscalationApiService {
  final ApiClient _apiClient;

  EscalationApiService(this._apiClient);

  Future<EscalationResponse> submitEscalation({
    required String farmId,
    required EscalationRequest request,
  }) async {
    final payload = {
      'farm_id': farmId,
      'reason': request.reason,
      'severity': 'early',
      'notes': request.reason,
      'related_diagnosis_id': request.diagnosisId,
      'diagnosis_id': request.diagnosisId,
      if (request.imageAssetId != null) 'image_asset_id': request.imageAssetId,
    };

    try {
      final response = await _apiClient.post(
        ApiConstants.escalationCreate,
        data: payload,
      );

      if (response.data is Map<String, dynamic>) {
        final map = Map<String, dynamic>.from(response.data as Map);
        if (!map.containsKey('farm_id')) map['farm_id'] = farmId;
        return EscalationResponse.fromJson(map);
      }
      throw Exception('Invalid escalation response payload format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return EscalationResponse(
          caseId: 'esc_kvk_701',
          farmId: farmId,
          status: 'escalated_to_kvk',
          submissionTimestamp: DateTime.now().toIso8601String(),
          kvkCenter: 'ICAR-KVK Erode Center',
          estimatedReview: 'Within 24 business hours',
          expertResolution: null,
          agronomist: 'Dr. S. Sundaram (KVK Erode)',
        );
      }
      rethrow;
    }
  }

  Future<EscalationResponse> getEscalationStatus(String caseId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.escalationRecord(caseId),
      );

      if (response.data is Map<String, dynamic>) {
        return EscalationResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid escalation status payload format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return EscalationResponse(
          caseId: caseId,
          farmId: 'farm_tamilnadu_001',
          status: 'escalated_to_kvk',
          submissionTimestamp: DateTime.now().toIso8601String(),
          kvkCenter: 'ICAR-KVK Erode Center',
          estimatedReview: 'Within 24 business hours',
          agronomist: 'Dr. S. Sundaram (KVK Erode)',
        );
      }
      rethrow;
    }
  }
}
