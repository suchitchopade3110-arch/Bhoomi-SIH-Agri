import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/alerts_repository.dart';
import '../../data/models/alert_models.dart';

final farmAlertsProvider =
    FutureProvider.family<FarmAlertsResponseModel, String>((ref, farmId) async {
  final repository = ref.watch(alertsRepositoryProvider);
  return await repository.getFarmAlerts(farmId);
});
