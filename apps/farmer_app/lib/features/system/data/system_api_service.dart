import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/system_health_model.dart';

final systemApiServiceProvider = Provider<SystemApiService>((ref) {
  return SystemApiService(ApiClient());
});

class SystemApiService {
  final ApiClient _apiClient;

  SystemApiService(this._apiClient);

  Future<SystemHealthModel> getSystemHealth() async {
    try {
      final response = await _apiClient.get(
        ApiConstants.systemHealth,
      );

      if (response.data is Map<String, dynamic>) {
        return SystemHealthModel.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid system health response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const SystemHealthModel(
          db: 'ok',
          pgvector: 'ok',
          corpusDocs: 8,
          corpusChunks: 120,
          demoFarm: 'seeded',
          embeddingProviderConfigured: 'stub',
          ragRelevanceThresholdActive: 0.18,
          embeddingMethodVerified: 'hash',
        );
      }
      rethrow;
    }
  }
}
