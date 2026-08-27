class VoiceQueryRequest {
  final String audioAssetId;
  final String farmId;
  final String lang;

  const VoiceQueryRequest({
    required this.audioAssetId,
    required this.farmId,
    this.lang = 'ta',
  });

  // Field names must match VoiceQueryRequest in
  // services/api/app/schemas/voice.py exactly (audio_asset_id, farm_id,
  // language are all required/consumed there) — see the same gotcha
  // documented in transcribe_request.dart / synthesize_request.dart.
  Map<String, dynamic> toJson() => {
        'audio_asset_id': audioAssetId,
        'farm_id': farmId,
        'language': lang,
      };
}
