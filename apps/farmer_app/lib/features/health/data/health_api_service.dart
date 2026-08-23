import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/health_history.dart';
import 'models/health_snapshot.dart';

final healthApiServiceProvider = Provider<HealthApiService>((ref) {
  return HealthApiService(ApiClient());
});

class HealthApiService {
  final ApiClient _apiClient;

  HealthApiService(this._apiClient);

  Future<HealthSnapshot> getHealth(String farmId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.farmHealth(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return HealthSnapshot.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid health response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return HealthSnapshot(
          score: 82,
          band: 'good',
          computedAt: DateTime.now().toIso8601String(),
          explanation: 'Optimal vegetative vigour and soil moisture balance observed.',
          subIndices: const HealthSubIndices(
            environmentalSuitability: 0.88,
            resourceAdequacy: 0.85,
            cropStageProgression: 0.80,
            activeProblemLoad: 0.78,
            monitoringRecency: 0.90,
            treatmentResponse: 0.82,
          ),
        );
      }
      rethrow;
    }
  }

  Future<HealthHistory> getHealthHistory(String farmId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.farmHealthHistory(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return HealthHistory.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid health history response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return HealthHistory(
          farmId: farmId,
          history: const [
            HealthHistoryPoint(
              score: null,
              band: 'unrated',
              recordedAt: '2026-08-01T08:00:00Z',
              reason: 'Initial registration baseline',
            ),
            HealthHistoryPoint(
              score: 74,
              band: 'moderate',
              recordedAt: '2026-08-15T08:00:00Z',
              reason: 'Bacterial leaf streak symptoms detected',
            ),
            HealthHistoryPoint(
              score: 82,
              band: 'good',
              recordedAt: '2026-08-22T12:00:00Z',
              reason: 'Advisory symptoms resolved',
            ),
          ],
        );
      }
      rethrow;
    }
  }

  Future<HealthSnapshot> recomputeHealth(String farmId) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.farmHealthRecompute(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return HealthSnapshot.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid health recompute response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return await getHealth(farmId);
      }
      rethrow;
    }
  }
}
