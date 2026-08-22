import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/followup_models.dart';

final followupApiServiceProvider = Provider<FollowupApiService>((ref) {
  return FollowupApiService(ApiClient());
});

class FollowupApiService {
  final ApiClient _apiClient;

  FollowupApiService(this._apiClient);

  Future<FollowupResponse> submitFollowup({
    required String farmId,
    required FollowupRequest request,
  }) async {
    final payload = {
      'farm_id': farmId,
      'response': request.outcome,
      'problem_id': request.diagnosisId,
      'diagnosis_id': request.diagnosisId,
      'outcome': request.outcome,
      if (request.notes != null) 'farmer_notes': request.notes,
      if (request.notes != null) 'notes': request.notes,
    };

    try {
      final response = await _apiClient.post(
        ApiConstants.followupCheckin,
        data: payload,
      );

      if (response.data is Map<String, dynamic>) {
        final map = Map<String, dynamic>.from(response.data as Map);
        if (!map.containsKey('diagnosis_id')) map['diagnosis_id'] = request.diagnosisId;
        return FollowupResponse.fromJson(map);
      }
      throw Exception('Invalid follow-up response payload format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        final isWorse = request.outcome == 'got_worse';
        return FollowupResponse(
          followupId: 'fol_98231',
          diagnosisId: request.diagnosisId,
          outcome: request.outcome,
          status: isWorse ? 'escalated' : 'recorded',
          nextSteps: isWorse
              ? 'Case auto-escalated to KVK Agronomist for priority inspection.'
              : 'Continue field monitoring according to advisory schedule.',
          escalationRecommended: isWorse,
          recordedAt: DateTime.now().toIso8601String(),
        );
      }
      rethrow;
    }
  }
}
