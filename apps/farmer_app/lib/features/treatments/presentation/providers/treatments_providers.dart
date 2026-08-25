import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/treatment_efficacy_model.dart';
import '../../data/treatments_repository.dart';

class TreatmentEfficacyParams {
  final String treatmentId;
  final String pathogen;
  final String crop;
  final String district;
  final int windowMonths;

  const TreatmentEfficacyParams({
    required this.treatmentId,
    required this.pathogen,
    required this.crop,
    required this.district,
    this.windowMonths = 12,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is TreatmentEfficacyParams &&
          runtimeType == other.runtimeType &&
          treatmentId == other.treatmentId &&
          pathogen == other.pathogen &&
          crop == other.crop &&
          district == other.district &&
          windowMonths == other.windowMonths;

  @override
  int get hashCode =>
      treatmentId.hashCode ^
      pathogen.hashCode ^
      crop.hashCode ^
      district.hashCode ^
      windowMonths.hashCode;
}

final treatmentEfficacyProvider = FutureProvider.family<TreatmentEfficacyModel, TreatmentEfficacyParams>(
    (ref, params) async {
  final repository = ref.watch(treatmentsRepositoryProvider);
  return await repository.getTreatmentEfficacy(
    treatmentId: params.treatmentId,
    pathogen: params.pathogen,
    crop: params.crop,
    district: params.district,
    windowMonths: params.windowMonths,
  );
});
