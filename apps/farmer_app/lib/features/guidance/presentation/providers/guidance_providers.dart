import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/guidance_repository.dart';
import '../../data/models/guidance_card_model.dart';

final guidanceListProvider = FutureProvider<List<GuidanceCardModel>>((ref) async {
  final repository = ref.watch(guidanceRepositoryProvider);
  return await repository.listGuidance();
});

class CropGuidanceParams {
  final String crop;
  final String? problemLabel;
  final String? problemType;

  const CropGuidanceParams({
    required this.crop,
    this.problemLabel,
    this.problemType,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is CropGuidanceParams &&
          runtimeType == other.runtimeType &&
          crop == other.crop &&
          problemLabel == other.problemLabel &&
          problemType == other.problemType;

  @override
  int get hashCode => crop.hashCode ^ (problemLabel?.hashCode ?? 0) ^ (problemType?.hashCode ?? 0);
}

final cropGuidanceProvider =
    FutureProvider.family<GuidanceCardModel, CropGuidanceParams>((ref, params) async {
  final repository = ref.watch(guidanceRepositoryProvider);
  return await repository.getCropGuidance(
    params.crop,
    problemLabel: params.problemLabel,
    problemType: params.problemType,
  );
});
