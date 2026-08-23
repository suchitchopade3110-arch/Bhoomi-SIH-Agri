import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/scheme_summary.dart';
import '../data/schemes_repository.dart';

final schemesListProvider =
    FutureProvider.family<List<SchemeSummary>, String>((ref, farmId) async {
  final repository = ref.watch(schemesRepositoryProvider);
  return await repository.getSchemes(farmId);
});

final schemeDetailProvider =
    FutureProvider.family<SchemeDetail, String>((ref, schemeId) async {
  final repository = ref.watch(schemesRepositoryProvider);
  return await repository.getSchemeDetail(schemeId);
});
