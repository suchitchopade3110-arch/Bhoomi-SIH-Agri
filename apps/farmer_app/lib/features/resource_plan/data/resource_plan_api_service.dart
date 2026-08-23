import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/resource_plan.dart';

final resourcePlanApiServiceProvider = Provider<ResourcePlanApiService>((ref) {
  return ResourcePlanApiService(ApiClient());
});

class ResourcePlanApiService {
  final ApiClient _apiClient;

  ResourcePlanApiService(this._apiClient);

  Future<ResourcePlan> getLatestPlan(String farmId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.latestResourcePlan(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return ResourcePlan.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid resource plan response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return ResourcePlan(
          id: 'rp_erode_001',
          farmId: farmId,
          tillableAreaAcres: 2.0,
          seedRateKgPerAcre: 28.5,
          totalSeedRequirementKg: 57.0,
          et0MmPerDay: 4.8,
          cropCoefficientKc: 1.15,
          cropWaterNeedMm: 5.5,
          irrigationAmount: 2200.0,
          irrigationUnit: 'Liters/Day',
          irrigationAdvice: 'Irrigate every alternate morning using furrow method to maintain soil saturation without standing stagnation.',
          createdAt: DateTime.now().toIso8601String(),
        );
      }
      rethrow;
    }
  }

  Future<ResourcePlan> generatePlan(String farmId) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.resourcePlan(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return ResourcePlan.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid resource plan response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return await getLatestPlan(farmId);
      }
      rethrow;
    }
  }
}
