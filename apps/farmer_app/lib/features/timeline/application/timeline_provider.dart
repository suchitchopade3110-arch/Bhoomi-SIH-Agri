import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/timeline_event.dart';
import '../data/timeline_repository.dart';

final farmTimelineProvider =
    FutureProvider.family<FarmTimeline, String>((ref, farmId) async {
  final repository = ref.watch(timelineRepositoryProvider);
  return await repository.getTimeline(farmId);
});
