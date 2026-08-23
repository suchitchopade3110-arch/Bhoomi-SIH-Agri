class FarmUpdate {
  final String updateId;
  final String updateType; // 'advisory' | 'followup_reminder' | 'scheme_alert' | 'case_status' | 'notice'
  final String title;
  final String description;
  final String timestamp;
  final String? actionRoute;
  final bool isRead;

  const FarmUpdate({
    required this.updateId,
    required this.updateType,
    required this.title,
    required this.description,
    required this.timestamp,
    this.actionRoute,
    this.isRead = false,
  });

  factory FarmUpdate.fromJson(Map<String, dynamic> json) {
    return FarmUpdate(
      updateId: json['update_id'] as String? ?? json['id'] as String? ?? '',
      updateType: json['update_type'] as String? ?? 'notice',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      timestamp: json['timestamp'] as String? ?? '',
      actionRoute: json['action_route'] as String?,
      isRead: json['is_read'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
        'update_id': updateId,
        'update_type': updateType,
        'title': title,
        'description': description,
        'timestamp': timestamp,
        if (actionRoute != null) 'action_route': actionRoute,
        'is_read': isRead,
      };
}
