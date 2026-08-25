class ConfirmFieldRequest {
  final String field;
  final dynamic confirmedValue;
  final bool isConfirmed;
  final String? correctionText;

  const ConfirmFieldRequest({
    required this.field,
    required this.confirmedValue,
    required this.isConfirmed,
    this.correctionText,
  });

  Map<String, dynamic> toJson() => {
        'field': field,
        'confirmed_value': confirmedValue,
        'is_confirmed': isConfirmed,
        if (correctionText != null) 'correction_text': correctionText,
      };
}

class ConfirmFieldResponse {
  final String status;
  final String field;
  final dynamic finalValue;
  final String message;

  const ConfirmFieldResponse({
    required this.status,
    required this.field,
    this.finalValue,
    required this.message,
  });

  factory ConfirmFieldResponse.fromJson(Map<String, dynamic> json) =>
      ConfirmFieldResponse(
        status: json['status']?.toString() ?? 'retry_prompt',
        field: json['field']?.toString() ?? '',
        finalValue: json['final_value'],
        message: json['message']?.toString() ?? '',
      );

  Map<String, dynamic> toJson() => {
        'status': status,
        'field': field,
        if (finalValue != null) 'final_value': finalValue,
        'message': message,
      };
}
