import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'farm_summary_api_service.dart';
import 'models/farm_summary.dart';

final farmSummaryRepositoryProvider = Provider<FarmSummaryRepository>((ref) {
  final apiService = ref.watch(farmSummaryApiServiceProvider);
  return FarmSummaryRepository(apiService);
});

class FarmSummaryRepository {
  final FarmSummaryApiService _apiService;

  FarmSummaryRepository(this._apiService);

  Future<FarmSummary> getFarmSummary(String farmId) async {
    return await _apiService.getFarmSummary(farmId);
  }
}
