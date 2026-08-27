import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/confirm_field_models.dart';
import 'models/synthesize_request.dart';
import 'models/synthesize_response.dart';
import 'models/transcribe_request.dart';
import 'models/transcribe_response.dart';
import 'models/voice_query_request.dart';
import 'models/voice_query_response.dart';
import 'voice_api_service.dart';

final voiceRepositoryProvider = Provider<VoiceRepository>((ref) {
  final apiService = ref.watch(voiceApiServiceProvider);
  return VoiceRepository(apiService);
});

class VoiceRepository {
  final VoiceApiService _apiService;

  VoiceRepository(this._apiService);

  Future<TranscribeResponse> transcribe(String assetId, {String lang = 'en-IN'}) async {
    return await _apiService.transcribe(
      TranscribeRequest(assetId: assetId, lang: lang),
    );
  }

  Future<ConfirmFieldResponse> confirmField(ConfirmFieldRequest request) async {
    return await _apiService.confirmField(request);
  }

  Future<SynthesizeResponse> synthesize(String text, {String lang = 'en-IN'}) async {
    return await _apiService.synthesize(
      SynthesizeRequest(text: text, lang: lang),
    );
  }

  /// Ask a spoken question and get back a spoken answer, end to end.
  Future<VoiceQueryResponse> askQuestion({
    required String audioAssetId,
    required String farmId,
    String lang = 'en-IN',
  }) async {
    return await _apiService.query(
      VoiceQueryRequest(audioAssetId: audioAssetId, farmId: farmId, lang: lang),
    );
  }
}
