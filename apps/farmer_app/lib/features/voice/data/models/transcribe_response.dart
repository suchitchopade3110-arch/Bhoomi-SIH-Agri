class ParsedIntent {
  final String intent;
  final String? entity;
  final dynamic value;

  const ParsedIntent({
    required this.intent,
    this.entity,
    this.value,
  });

  factory ParsedIntent.fromJson(Map<String, dynamic> json) {
    return ParsedIntent(
      intent: json['intent'] as String? ?? 'unknown',
      entity: json['entity'] as String?,
      value: json['value'],
    );
  }

  Map<String, dynamic> toJson() => {
        'intent': intent,
        if (entity != null) 'entity': entity,
        if (value != null) 'value': value,
      };
}

class TranscribeResponse {
  final String text;
  final double confidence;
  final String lang;
  final ParsedIntent? parsedIntent;
  final bool needsConfirmation;

  const TranscribeResponse({
    required this.text,
    required this.confidence,
    this.lang = 'en-IN',
    this.parsedIntent,
    this.needsConfirmation = false,
  });

  bool get isHighConfidence => confidence >= 0.70;
  bool get isLowConfidence => confidence < 0.60;

  factory TranscribeResponse.fromJson(Map<String, dynamic> json) {
    return TranscribeResponse(
      text: json['transcript'] as String? ?? json['text'] as String? ?? '',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      lang: json['language'] as String? ?? json['lang'] as String? ?? 'ta',
      parsedIntent: json['parsed_intent'] != null
          ? ParsedIntent.fromJson(json['parsed_intent'] as Map<String, dynamic>)
          : null,
      needsConfirmation: json['needs_confirmation'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
        'text': text,
        'confidence': confidence,
        'lang': lang,
        if (parsedIntent != null) 'parsed_intent': parsedIntent!.toJson(),
        'needs_confirmation': needsConfirmation,
      };
}
