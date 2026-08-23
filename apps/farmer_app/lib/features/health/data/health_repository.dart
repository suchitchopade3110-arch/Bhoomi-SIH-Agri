import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'health_api_service.dart';
import 'models/health_history.dart';
import 'models/health_snapshot.dart';

final healthRepositoryProvider = Provider<HealthRepository>((ref) {
  final apiService = ref.watch(healthApiServiceProvider);
  return HealthRepository(apiService);
});

class HealthRepository {
  final HealthApiService _apiService;

  HealthRepository(this._apiService);

  Future<HealthSnapshot> getHealth(String farmId) async {
    return await _apiService.getHealth(farmId);
  }

  Future<HealthHistory> getHealthHistory(String farmId) async {
    return await _apiService.getHealthHistory(farmId);
  }

  Future<HealthSnapshot> recomputeHealth(String farmId) async {
    return await _apiService.recomputeHealth(farmId);
  }
}

