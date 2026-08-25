import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/system_health_model.dart';
import 'system_api_service.dart';

final systemRepositoryProvider = Provider<SystemRepository>((ref) {
  final apiService = ref.watch(systemApiServiceProvider);
  return SystemRepository(apiService);
});

class SystemRepository {
  final SystemApiService _apiService;

  SystemRepository(this._apiService);

  Future<SystemHealthModel> getSystemHealth() async {
    return await _apiService.getSystemHealth();
  }
}
