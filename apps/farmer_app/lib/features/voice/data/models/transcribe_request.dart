class TranscribeRequest {
  final String assetId;
  final String lang;

  const TranscribeRequest({
    required this.assetId,
    this.lang = 'ta',
  });

  // Field names must match VoiceTranscribeRequest in
  // services/api/app/schemas/voice.py exactly — audio_asset_id is a
  // required field there, so sending "asset_id" instead left it missing
  // and every transcribe call 422'd (checklist: voice pipeline gap).
  Map<String, dynamic> toJson() => {
        'audio_asset_id': assetId,
        'language': lang,
      };
}
