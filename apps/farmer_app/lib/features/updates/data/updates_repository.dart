import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/farm_update.dart';
import 'updates_api_service.dart';

final updatesRepositoryProvider = Provider<UpdatesRepository>((ref) {
  final apiService = ref.watch(updatesApiServiceProvider);
  return UpdatesRepository(apiService);
});

class UpdatesRepository {
  final UpdatesApiService _apiService;

  UpdatesRepository(this._apiService);

  Future<List<FarmUpdate>> getUpdates(String farmId) async {
    return await _apiService.getUpdates(farmId);
  }
}

