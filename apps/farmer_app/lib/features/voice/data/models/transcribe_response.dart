class ParsedIntent {
  final String intent;
  final String? entity;
  final String? field;
  final dynamic value;
  final String? rawText;

  const ParsedIntent({
    required this.intent,
    this.entity,
    this.field,
    this.value,
    this.rawText,
  });

  factory ParsedIntent.fromJson(Map<String, dynamic> json) {
    final fieldVal = json['field'] as String?;
    return ParsedIntent(
      intent: json['intent'] as String? ?? fieldVal ?? 'unknown',
      entity: json['entity'] as String? ?? fieldVal,
      field: fieldVal,
      value: json['value'],
      rawText: json['raw_text'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'intent': intent,
        if (entity != null) 'entity': entity,
        if (field != null) 'field': field,
        if (value != null) 'value': value,
        if (rawText != null) 'raw_text': rawText,
      };
}

class TranscribeResponse {
  final String text;
  final double confidence;
  final String lang;
  final ParsedIntent? parsedIntent;
  final bool needsConfirmation;
  final String? readbackText;
  final String? provider;

  const TranscribeResponse({
    required this.text,
    required this.confidence,
    this.lang = 'en-IN',
    this.parsedIntent,
    this.needsConfirmation = false,
    this.readbackText,
    this.provider,
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
      readbackText: json['readback_text'] as String?,
      provider: json['provider'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'text': text,
        'confidence': confidence,
        'lang': lang,
        if (parsedIntent != null) 'parsed_intent': parsedIntent!.toJson(),
        'needs_confirmation': needsConfirmation,
        if (readbackText != null) 'readback_text': readbackText,
        if (provider != null) 'provider': provider,
      };
}
