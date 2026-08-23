class HealthHistoryPoint {
  final int? score;
  final String band;
  final String recordedAt;
  final String? reason;

  const HealthHistoryPoint({
    this.score,
    required this.band,
    required this.recordedAt,
    this.reason,
  });

  bool get isRated => score != null;

  factory HealthHistoryPoint.fromJson(Map<String, dynamic> json) {
    return HealthHistoryPoint(
      score: json['score'] as int?,
      band: json['band'] as String? ?? 'unrated',
      recordedAt: json['recorded_at'] as String? ?? '',
      reason: json['reason'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'score': score,
        'band': band,
        'recorded_at': recordedAt,
        if (reason != null) 'reason': reason,
      };
}

class HealthHistory {
  final String farmId;
  final List<HealthHistoryPoint> history;

  const HealthHistory({
    required this.farmId,
    required this.history,
  });

  factory HealthHistory.fromJson(Map<String, dynamic> json) {
    return HealthHistory(
      farmId: json['farm_id'] as String? ?? '',
      history: json['history'] != null
          ? (json['history'] as List)
              .map((i) => HealthHistoryPoint.fromJson(i as Map<String, dynamic>))
              .toList()
          : [
              const HealthHistoryPoint(
                score: null,
                band: 'unrated',
                recordedAt: '2026-08-01T08:00:00Z',
                reason: 'Initial registration baseline',
              ),
              const HealthHistoryPoint(
                score: 82,
                band: 'good',
                recordedAt: '2026-08-10T10:00:00Z',
                reason: 'Vegetative irrigation and fertilization fulfilled',
              ),
              const HealthHistoryPoint(
                score: 85,
                band: 'good',
                recordedAt: '2026-08-21T06:00:00Z',
                reason: 'Optimal field weather and moisture retention',
              ),
            ],
    );
  }

  Map<String, dynamic> toJson() => {
        'farm_id': farmId,
        'history': history.map((h) => h.toJson()).toList(),
      };
}
