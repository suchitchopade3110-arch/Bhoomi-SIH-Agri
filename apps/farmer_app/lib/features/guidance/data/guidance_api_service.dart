import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/guidance_card_model.dart';

final guidanceApiServiceProvider = Provider<GuidanceApiService>((ref) {
  return GuidanceApiService(ApiClient());
});

class GuidanceApiService {
  final ApiClient _apiClient;

  GuidanceApiService(this._apiClient);

  Future<List<GuidanceCardModel>> listGuidance() async {
    try {
      final response = await _apiClient.get(
        ApiConstants.guidanceList,
      );

      if (response.data is List) {
        return (response.data as List)
            .map((e) => GuidanceCardModel.fromJson(e as Map<String, dynamic>))
            .toList();
      }
      throw Exception('Invalid guidance list response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const [
          GuidanceCardModel(
            crop: 'samba_paddy',
            problemType: 'disease',
            problemLabel: 'bacterial_leaf_blight',
            title: 'Bacterial Leaf Blight (BLB) Containment',
            containmentAdvice: 'Drain standing water immediately and reduce nitrogen application until fresh tillers show no lesions.',
            whatToAvoid: 'Do not apply excess urea/nitrogen fertilizer. Do not irrigate from infected fields to healthy plots.',
            immediateActions: [
              'Drain excess water from field for 3-4 days.',
              'Avoid top-dressing nitrogenous fertilizers during active lesion expansion.',
              'Spray Copper Hydroxide (2.0 g/L) or Copper Oxychloride (2.5 g/L) at early symptom onset.',
            ],
            expertTrigger: 'If water-soaked lesions spread across more than 25% of canopy within 48 hours.',
          ),
        ];
      }
      rethrow;
    }
  }

  Future<GuidanceCardModel> getCropGuidance(
    String crop, {
    String? problemLabel,
    String? problemType,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        if (problemLabel != null) 'problem_label': problemLabel,
        if (problemType != null) 'problem_type': problemType,
      };

      final response = await _apiClient.get(
        ApiConstants.cropGuidance(crop),
        queryParameters: queryParams.isNotEmpty ? queryParams : null,
      );

      if (response.data is Map<String, dynamic>) {
        return GuidanceCardModel.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid crop guidance response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return GuidanceCardModel(
          crop: crop,
          problemType: problemType ?? 'general',
          problemLabel: problemLabel,
          title: 'Field Containment Protocol for $crop',
          containmentAdvice: 'Maintain field scouting and balanced moisture management.',
          whatToAvoid: 'Avoid chemical spraying without definitive diagnosis.',
          immediateActions: const [
            'Inspect border rows for early symptom onset.',
            'Maintain optimal drainage.',
          ],
          expertTrigger: 'If leaf yellowing or pest damage exceeds threshold.',
        );
      }
      rethrow;
    }
  }
}
