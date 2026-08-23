class TimelineEvent {
  final String eventId;
  final String eventType; // 'onboarding' | 'land' | 'resource_plan' | 'diagnosis' | 'followup' | 'escalation'
  final String title;
  final String summary;
  final String status;
  final String timestamp;

  const TimelineEvent({
    required this.eventId,
    required this.eventType,
    required this.title,
    required this.summary,
    required this.status,
    required this.timestamp,
  });

  factory TimelineEvent.fromJson(Map<String, dynamic> json) {
    return TimelineEvent(
      eventId: json['event_id'] as String? ?? json['id'] as String? ?? '',
      eventType: json['event_type'] as String? ?? 'general',
      title: json['title'] as String? ?? 'Farm Activity',
      summary: json['summary'] as String? ?? json['description'] as String? ?? '',
      status: json['status'] as String? ?? 'completed',
      timestamp: json['timestamp'] as String? ?? json['created_at'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
        'event_id': eventId,
        'event_type': eventType,
        'title': title,
        'summary': summary,
        'status': status,
        'timestamp': timestamp,
      };
}

class FarmTimeline {
  final String farmId;
  final List<TimelineEvent> events;

  const FarmTimeline({
    required this.farmId,
    required this.events,
  });

  factory FarmTimeline.fromJson(Map<String, dynamic> json) {
    return FarmTimeline(
      farmId: json['farm_id'] as String? ?? '',
      events: json['events'] != null
          ? (json['events'] as List).map((e) => TimelineEvent.fromJson(e as Map<String, dynamic>)).toList()
          : [
              const TimelineEvent(
                eventId: 'ev_1',
                eventType: 'diagnosis',
                title: 'Crop problem reported',
                summary: 'Paddy leaves turning yellow — Bacterial Leaf Blight advisory generated',
                status: 'monitoring',
                timestamp: '2026-08-21T08:30:00Z',
              ),
              const TimelineEvent(
                eventId: 'ev_2',
                eventType: 'land',
                title: 'Land verification completed',
                summary: 'Survey No. 142/3B officially verified by Taluk agricultural officer',
                status: 'verified',
                timestamp: '2026-08-21T07:15:00Z',
              ),
              const TimelineEvent(
                eventId: 'ev_3',
                eventType: 'resource_plan',
                title: 'Daily farm plan generated',
                summary: '2,200 L irrigation recommended based on ET0 and soil retention',
                status: 'active',
                timestamp: '2026-08-21T06:00:00Z',
              ),
              const TimelineEvent(
                eventId: 'ev_4',
                eventType: 'onboarding',
                title: 'Farm profile created',
                summary: 'Samba Paddy, 2.0 Acres registered in Erode district',
                status: 'completed',
                timestamp: '2026-08-20T10:00:00Z',
              ),
            ],
    );
  }

  Map<String, dynamic> toJson() => {
        'farm_id': farmId,
        'events': events.map((e) => e.toJson()).toList(),
      };
}
