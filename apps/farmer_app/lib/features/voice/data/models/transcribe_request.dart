class TranscribeRequest {
  final String assetId;
  final String lang;

  const TranscribeRequest({
    required this.assetId,
    this.lang = 'en-IN',
  });

  Map<String, dynamic> toJson() => {
        'asset_id': assetId,
        'lang': lang,
      };
}
