class DiagnoseRequest {
  final String problemDescription;
  final String? imageAssetId;
  final String? audioAssetId;

  const DiagnoseRequest({
    required this.problemDescription,
    this.imageAssetId,
    this.audioAssetId,
  });

  Map<String, dynamic> toJson() => {
        'image_asset_id': imageAssetId ?? 'asset_default',
        'description_text': problemDescription,
        'problem_description': problemDescription,
        if (audioAssetId != null) 'description_asset_id': audioAssetId,
        if (audioAssetId != null) 'audio_asset_id': audioAssetId,
      };

  factory DiagnoseRequest.fromJson(Map<String, dynamic> json) {
    return DiagnoseRequest(
      problemDescription: json['description_text'] as String? ?? json['problem_description'] as String? ?? '',
      imageAssetId: json['image_asset_id'] as String?,
      audioAssetId: json['description_asset_id'] as String? ?? json['audio_asset_id'] as String?,
    );
  }
}
