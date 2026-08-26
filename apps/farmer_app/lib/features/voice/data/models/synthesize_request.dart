class SynthesizeRequest {
  final String text;
  final String lang;

  const SynthesizeRequest({
    required this.text,
    this.lang = 'ta',
  });

  // "language" (not "lang") to match VoiceSynthesizeRequest in
  // services/api/app/schemas/voice.py — since that field has a server-side
  // default, sending the wrong key didn't 422, it silently always
  // synthesized in the default language regardless of what was requested.
  Map<String, dynamic> toJson() => {
        'text': text,
        'language': lang,
      };
}
