import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/daily_brief_repository.dart';
import '../data/models/daily_brief_response.dart';

final dailyBriefProvider =
    FutureProvider.family<DailyBriefResponse, String>((ref, farmId) async {
  final repository = ref.watch(dailyBriefRepositoryProvider);
  return await repository.getDailyBrief(farmId);
});
