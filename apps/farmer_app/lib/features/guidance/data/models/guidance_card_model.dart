class GuidanceCardModel {
  final String crop;
  final String problemType;
  final String? problemLabel;
  final String title;
  final String containmentAdvice;
  final String whatToAvoid;
  final List<String> immediateActions;
  final String expertTrigger;

  const GuidanceCardModel({
    required this.crop,
    this.problemType = 'general',
    this.problemLabel,
    required this.title,
    required this.containmentAdvice,
    required this.whatToAvoid,
    this.immediateActions = const [],
    required this.expertTrigger,
  });

  factory GuidanceCardModel.fromJson(Map<String, dynamic> json) =>
      GuidanceCardModel(
        crop: json['crop']?.toString() ?? '',
        problemType: json['problem_type']?.toString() ?? 'general',
        problemLabel: json['problem_label']?.toString(),
        title: json['title']?.toString() ?? '',
        containmentAdvice: json['containment_advice']?.toString() ?? '',
        whatToAvoid: json['what_to_avoid']?.toString() ?? '',
        immediateActions: (json['immediate_actions'] as List?)
                ?.map((e) => e.toString())
                .toList() ??
            const [],
        expertTrigger: json['expert_trigger']?.toString() ?? '',
      );

  Map<String, dynamic> toJson() => {
        'crop': crop,
        'problem_type': problemType,
        if (problemLabel != null) 'problem_label': problemLabel,
        'title': title,
        'containment_advice': containmentAdvice,
        'what_to_avoid': whatToAvoid,
        'immediate_actions': immediateActions,
        'expert_trigger': expertTrigger,
      };
}
