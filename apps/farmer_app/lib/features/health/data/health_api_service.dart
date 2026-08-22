import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
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
    final response = await _apiClient.get(
      ApiConstants.farmHealth(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return HealthSnapshot.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid health response format.');
  }

  Future<HealthHistory> getHealthHistory(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.farmHealthHistory(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return HealthHistory.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid health history response format.');
  }

  Future<HealthSnapshot> recomputeHealth(String farmId) async {
    final response = await _apiClient.post(
      ApiConstants.farmHealthRecompute(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return HealthSnapshot.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid health recompute response format.');
  }
}
