import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'daily_brief_api_service.dart';
import 'models/daily_brief_response.dart';

final dailyBriefRepositoryProvider = Provider<DailyBriefRepository>((ref) {
  final apiService = ref.watch(dailyBriefApiServiceProvider);
  return DailyBriefRepository(apiService);
});

class DailyBriefRepository {
  final DailyBriefApiService _apiService;

  DailyBriefRepository(this._apiService);

  Future<DailyBriefResponse> getDailyBrief(String farmId) async {
    return await _apiService.getDailyBrief(farmId);
  }
}

