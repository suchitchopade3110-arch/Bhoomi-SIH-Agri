import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/resource_plan.dart';
import 'resource_plan_api_service.dart';

final resourcePlanRepositoryProvider = Provider<ResourcePlanRepository>((ref) {
  final apiService = ref.watch(resourcePlanApiServiceProvider);
  return ResourcePlanRepository(apiService);
});

class ResourcePlanRepository {
  final ResourcePlanApiService _apiService;

  ResourcePlanRepository(this._apiService);

  Future<ResourcePlan> getLatestPlan(String farmId) async {
    return await _apiService.getLatestPlan(farmId);
  }

  Future<ResourcePlan> generatePlan(String farmId) async {
    return await _apiService.generatePlan(farmId);
  }
}
