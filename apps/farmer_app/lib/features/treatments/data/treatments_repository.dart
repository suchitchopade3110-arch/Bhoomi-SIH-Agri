import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/treatment_efficacy_model.dart';
import 'treatments_api_service.dart';

final treatmentsRepositoryProvider = Provider<TreatmentsRepository>((ref) {
  final apiService = ref.watch(treatmentsApiServiceProvider);
  return TreatmentsRepository(apiService);
});

class TreatmentsRepository {
  final TreatmentsApiService _apiService;

  TreatmentsRepository(this._apiService);

  Future<TreatmentEfficacyModel> getTreatmentEfficacy({
    required String treatmentId,
    required String pathogen,
    required String crop,
    required String district,
    int windowMonths = 12,
  }) async {
    return await _apiService.getTreatmentEfficacy(
      treatmentId: treatmentId,
      pathogen: pathogen,
      crop: crop,
      district: district,
      windowMonths: windowMonths,
    );
  }
}
