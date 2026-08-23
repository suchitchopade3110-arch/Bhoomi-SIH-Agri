import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/health_repository.dart';
import '../data/models/health_history.dart';
import '../data/models/health_snapshot.dart';

final farmHealthProvider =
    FutureProvider.family<HealthSnapshot, String>((ref, farmId) async {
  final repository = ref.watch(healthRepositoryProvider);
  return await repository.getHealth(farmId);
});

final farmHealthHistoryProvider =
    FutureProvider.family<HealthHistory, String>((ref, farmId) async {
  final repository = ref.watch(healthRepositoryProvider);
  return await repository.getHealthHistory(farmId);
});
