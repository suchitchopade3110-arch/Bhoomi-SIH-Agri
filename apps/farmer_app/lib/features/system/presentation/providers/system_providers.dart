import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/system_health_model.dart';
import '../../data/system_repository.dart';

final systemHealthProvider = FutureProvider<SystemHealthModel>((ref) async {
  final repository = ref.watch(systemRepositoryProvider);
  return await repository.getSystemHealth();
});
