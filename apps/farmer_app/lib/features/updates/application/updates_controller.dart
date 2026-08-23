import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/farm_update.dart';
import '../data/updates_repository.dart';

final farmUpdatesProvider =
    FutureProvider.family<List<FarmUpdate>, String>((ref, farmId) async {
  final repository = ref.watch(updatesRepositoryProvider);
  return await repository.getUpdates(farmId);
});
