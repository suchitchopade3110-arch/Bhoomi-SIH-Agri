import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'guidance_api_service.dart';
import 'models/guidance_card_model.dart';

final guidanceRepositoryProvider = Provider<GuidanceRepository>((ref) {
  final apiService = ref.watch(guidanceApiServiceProvider);
  return GuidanceRepository(apiService);
});

class GuidanceRepository {
  final GuidanceApiService _apiService;

  GuidanceRepository(this._apiService);

  Future<List<GuidanceCardModel>> listGuidance() async {
    return await _apiService.listGuidance();
  }

  Future<GuidanceCardModel> getCropGuidance(
    String crop, {
    String? problemLabel,
    String? problemType,
  }) async {
    return await _apiService.getCropGuidance(
      crop,
      problemLabel: problemLabel,
      problemType: problemType,
    );
  }
}
