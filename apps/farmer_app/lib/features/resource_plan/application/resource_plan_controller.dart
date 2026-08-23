import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/resource_plan.dart';
import '../data/resource_plan_repository.dart';

final latestResourcePlanProvider =
    FutureProvider.family<ResourcePlan, String>((ref, farmId) async {
  final repository = ref.watch(resourcePlanRepositoryProvider);
  return await repository.getLatestPlan(farmId);
});
