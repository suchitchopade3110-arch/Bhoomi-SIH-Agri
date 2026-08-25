class AlertItemModel {
  final String alertId;
  final String pathogenName;
  final String severity;
  final String triggerReason;
  final String preventativeAction;
  final List<String> inspectionTasks;
  final String spokenSummary;
  final String createdAt;
  final String expiresAt;

  const AlertItemModel({
    required this.alertId,
    required this.pathogenName,
    required this.severity,
    required this.triggerReason,
    required this.preventativeAction,
    required this.inspectionTasks,
    required this.spokenSummary,
    required this.createdAt,
    required this.expiresAt,
  });

  factory AlertItemModel.fromJson(Map<String, dynamic> json) => AlertItemModel(
        alertId: json['alert_id']?.toString() ?? '',
        pathogenName: json['pathogen_name']?.toString() ?? '',
        severity: json['severity']?.toString() ?? 'advisory',
        triggerReason: json['trigger_reason']?.toString() ?? '',
        preventativeAction: json['preventative_action']?.toString() ?? '',
        inspectionTasks: (json['inspection_tasks'] as List?)
                ?.map((e) => e.toString())
                .toList() ??
            const [],
        spokenSummary: json['spoken_summary']?.toString() ?? '',
        createdAt: json['created_at']?.toString() ?? '',
        expiresAt: json['expires_at']?.toString() ?? '',
      );

  Map<String, dynamic> toJson() => {
        'alert_id': alertId,
        'pathogen_name': pathogenName,
        'severity': severity,
        'trigger_reason': triggerReason,
        'preventative_action': preventativeAction,
        'inspection_tasks': inspectionTasks,
        'spoken_summary': spokenSummary,
        'created_at': createdAt,
        'expires_at': expiresAt,
      };
}

class FarmAlertsResponseModel {
  final String farmId;
  final List<AlertItemModel> activeAlerts;

  const FarmAlertsResponseModel({
    required this.farmId,
    required this.activeAlerts,
  });

  factory FarmAlertsResponseModel.fromJson(Map<String, dynamic> json) =>
      FarmAlertsResponseModel(
        farmId: json['farm_id']?.toString() ?? '',
        activeAlerts: (json['active_alerts'] as List?)
                ?.map((e) => AlertItemModel.fromJson(e as Map<String, dynamic>))
                .toList() ??
            const [],
      );

  Map<String, dynamic> toJson() => {
        'farm_id': farmId,
        'active_alerts': activeAlerts.map((e) => e.toJson()).toList(),
      };
}

class AlertAcknowledgeRequest {
  final String farmId;
  final String reason;

  const AlertAcknowledgeRequest({
    required this.farmId,
    this.reason = 'action_taken',
  });

  Map<String, dynamic> toJson() => {
        'farm_id': farmId,
        'reason': reason,
      };
}

class AlertAcknowledgeResponse {
  final String status;
  final String alertId;

  const AlertAcknowledgeResponse({
    required this.status,
    required this.alertId,
  });

  factory AlertAcknowledgeResponse.fromJson(Map<String, dynamic> json) =>
      AlertAcknowledgeResponse(
        status: json['status']?.toString() ?? 'acknowledged',
        alertId: json['alert_id']?.toString() ?? '',
      );

  Map<String, dynamic> toJson() => {
        'status': status,
        'alert_id': alertId,
      };
}
