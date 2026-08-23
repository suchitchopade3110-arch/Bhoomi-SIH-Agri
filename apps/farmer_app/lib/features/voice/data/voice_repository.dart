import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/synthesize_request.dart';
import 'models/synthesize_response.dart';
import 'models/transcribe_request.dart';
import 'models/transcribe_response.dart';
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

  Future<SynthesizeResponse> synthesize(String text, {String lang = 'en-IN'}) async {
    return await _apiService.synthesize(
      SynthesizeRequest(text: text, lang: lang),
    );
  }
}
