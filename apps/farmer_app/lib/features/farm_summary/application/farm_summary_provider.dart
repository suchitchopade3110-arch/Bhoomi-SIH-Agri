import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/farm_summary_repository.dart';
import '../data/models/farm_summary.dart';

final farmSummaryProvider =
    FutureProvider.family<FarmSummary, String>((ref, farmId) async {
  final repository = ref.watch(farmSummaryRepositoryProvider);
  return await repository.getFarmSummary(farmId);
});
