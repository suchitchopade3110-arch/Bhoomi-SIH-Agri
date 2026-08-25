class SystemHealthModel {
  final String db;
  final String pgvector;
  final int corpusDocs;
  final int corpusChunks;
  final String demoFarm;
  final String embeddingProviderConfigured;
  final double ragRelevanceThresholdActive;
  final String embeddingMethodVerified;

  const SystemHealthModel({
    required this.db,
    required this.pgvector,
    required this.corpusDocs,
    required this.corpusChunks,
    required this.demoFarm,
    required this.embeddingProviderConfigured,
    required this.ragRelevanceThresholdActive,
    required this.embeddingMethodVerified,
  });

  factory SystemHealthModel.fromJson(Map<String, dynamic> json) =>
      SystemHealthModel(
        db: json['db']?.toString() ?? 'unknown',
        pgvector: json['pgvector']?.toString() ?? 'unknown',
        corpusDocs: (json['corpus_docs'] as num?)?.toInt() ?? 0,
        corpusChunks: (json['corpus_chunks'] as num?)?.toInt() ?? 0,
        demoFarm: json['demo_farm']?.toString() ?? 'not_seeded',
        embeddingProviderConfigured:
            json['embedding_provider_configured']?.toString() ?? 'stub',
        ragRelevanceThresholdActive:
            (json['rag_relevance_threshold_active'] as num?)?.toDouble() ?? 0.18,
        embeddingMethodVerified:
            json['embedding_method_verified']?.toString() ?? 'unknown',
      );

  Map<String, dynamic> toJson() => {
        'db': db,
        'pgvector': pgvector,
        'corpus_docs': corpusDocs,
        'corpus_chunks': corpusChunks,
        'demo_farm': demoFarm,
        'embedding_provider_configured': embeddingProviderConfigured,
        'rag_relevance_threshold_active': ragRelevanceThresholdActive,
        'embedding_method_verified': embeddingMethodVerified,
      };
}
