class SynthesizeResponse {
  final String audioUrl;
  final double durationSeconds;

  const SynthesizeResponse({
    required this.audioUrl,
    required this.durationSeconds,
  });

  factory SynthesizeResponse.fromJson(Map<String, dynamic> json) {
    return SynthesizeResponse(
      audioUrl: json['audio_url'] as String? ?? '',
      durationSeconds: (json['duration_seconds'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toJson() => {
        'audio_url': audioUrl,
        'duration_seconds': durationSeconds,
      };
}
