import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/farm_update.dart';

final updatesApiServiceProvider = Provider<UpdatesApiService>((ref) {
  return UpdatesApiService(ApiClient());
});

class UpdatesApiService {
  final ApiClient _apiClient;

  UpdatesApiService(this._apiClient);

  Future<List<FarmUpdate>> getUpdates(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.farmUpdates(farmId),
    );

    if (response.data is List) {
      return (response.data as List)
          .map((u) => FarmUpdate.fromJson(u as Map<String, dynamic>))
          .toList();
    } else if (response.data is Map<String, dynamic> && response.data['updates'] is List) {
      return (response.data['updates'] as List)
          .map((u) => FarmUpdate.fromJson(u as Map<String, dynamic>))
          .toList();
    }
    throw Exception('Invalid updates payload format.');
  }
}
