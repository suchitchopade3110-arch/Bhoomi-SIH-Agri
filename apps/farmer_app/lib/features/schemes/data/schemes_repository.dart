import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/scheme_summary.dart';
import 'schemes_api_service.dart';

final schemesRepositoryProvider = Provider<SchemesRepository>((ref) {
  final apiService = ref.watch(schemesApiServiceProvider);
  return SchemesRepository(apiService);
});

class SchemesRepository {
  final SchemesApiService _apiService;

  SchemesRepository(this._apiService);

  Future<List<SchemeSummary>> getSchemes(String farmId) async {
    return await _apiService.getSchemes(farmId);
  }

  Future<SchemeDetail> getSchemeDetail(String schemeId) async {
    return await _apiService.getSchemeDetail(schemeId);
  }

  Future<SchemeDetail> submitRequirements({
    required String farmId,
    required String schemeId,
    required Map<String, dynamic> additionalData,
  }) async {
    return await _apiService.submitRequirements(
      farmId: farmId,
      schemeId: schemeId,
      additionalData: additionalData,
    );
  }
}
