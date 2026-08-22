class SynthesizeRequest {
  final String text;
  final String lang;

  const SynthesizeRequest({
    required this.text,
    this.lang = 'en-IN',
  });

  Map<String, dynamic> toJson() => {
        'text': text,
        'lang': lang,
      };
}
