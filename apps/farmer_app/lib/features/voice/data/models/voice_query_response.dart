class VoiceQueryResponse {
  final String transcript;
  final String answerText;
  final String audioResponseUrl;
  final String? spokenSummary;

  const VoiceQueryResponse({
    required this.transcript,
    required this.answerText,
    required this.audioResponseUrl,
    this.spokenSummary,
  });

  factory VoiceQueryResponse.fromJson(Map<String, dynamic> json) {
    return VoiceQueryResponse(
      transcript: json['transcript'] as String? ?? '',
      answerText: json['answer_text'] as String? ?? '',
      audioResponseUrl: json['audio_response_url'] as String? ?? '',
      spokenSummary: json['spoken_summary'] as String?,
    );
  }
}
