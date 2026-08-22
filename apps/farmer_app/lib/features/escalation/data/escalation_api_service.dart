import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
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
  }

  Future<EscalationResponse> getEscalationStatus(String caseId) async {
    final response = await _apiClient.get(
      ApiConstants.escalationRecord(caseId),
    );

    if (response.data is Map<String, dynamic>) {
      return EscalationResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid escalation status payload format.');
  }
}
