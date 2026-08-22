import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/resource_plan.dart';

final resourcePlanApiServiceProvider = Provider<ResourcePlanApiService>((ref) {
  return ResourcePlanApiService(ApiClient());
});

class ResourcePlanApiService {
  final ApiClient _apiClient;

  ResourcePlanApiService(this._apiClient);

  Future<ResourcePlan> getLatestPlan(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.latestResourcePlan(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return ResourcePlan.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid resource plan response payload.');
  }

  Future<ResourcePlan> generatePlan(String farmId) async {
    final response = await _apiClient.post(
      ApiConstants.resourcePlan(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return ResourcePlan.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid resource plan response payload.');
  }
}
