class BriefWeatherContext {
  final String summary;
  final String temperatureRange;
  final String rainRisk;

  const BriefWeatherContext({
    required this.summary,
    required this.temperatureRange,
    required this.rainRisk,
  });

  factory BriefWeatherContext.fromJson(Map<String, dynamic> json) {
    return BriefWeatherContext(
      summary: json['summary'] as String? ?? 'Dry conditions favorable for fieldwork.',
      temperatureRange: json['temperature_range'] as String? ?? '24°C - 33°C',
      rainRisk: json['rain_risk'] as String? ?? 'Low (10%)',
    );
  }

  Map<String, dynamic> toJson() => {
        'summary': summary,
        'temperature_range': temperatureRange,
        'rain_risk': rainRisk,
      };
}

class DailyBriefResponse {
  final String briefDate;
  final String crop;
  final String growthStage;
  final String? importantAction;
  final String? farmPriority;
  final BriefWeatherContext? weatherContext;
  final List<String> cropWatch;
  final String advisorySummary;
  final String? spokenSummary;

  const DailyBriefResponse({
    required this.briefDate,
    required this.crop,
    required this.growthStage,
    this.importantAction,
    this.farmPriority,
    this.weatherContext,
    this.cropWatch = const [],
    required this.advisorySummary,
    this.spokenSummary,
  });

  factory DailyBriefResponse.fromJson(Map<String, dynamic> json) {
    return DailyBriefResponse(
      briefDate: json['brief_date'] as String? ?? DateTime.now().toIso8601String().substring(0, 10),
      crop: json['crop'] as String? ?? 'Paddy',
      growthStage: json['growth_stage'] as String? ?? 'Vegetative Stage',
      importantAction: json['important_action'] as String? ?? 'Apply recommended 2,200 L irrigation during early morning hours.',
      farmPriority: json['farm_priority'] as String? ?? 'Inspect field bunds and maintain 2cm uniform water depth across paddy plots.',
      weatherContext: json['weather_context'] != null
          ? BriefWeatherContext.fromJson(json['weather_context'] as Map<String, dynamic>)
          : null,
      cropWatch: json['crop_watch'] != null
          ? List<String>.from(json['crop_watch'] as List)
          : [
              'Inspect lower tillers for blast or leaf blight lesions',
              'Check nitrogen top-dressing schedule based on leaf color chart',
            ],
      advisorySummary: json['advisory_summary'] as String? ?? 'Today is favorable for scheduled moisture management and field scouting.',
      spokenSummary: json['spoken_summary'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'brief_date': briefDate,
        'crop': crop,
        'growth_stage': growthStage,
        if (importantAction != null) 'important_action': importantAction,
        if (farmPriority != null) 'farm_priority': farmPriority,
        if (weatherContext != null) 'weather_context': weatherContext!.toJson(),
        'crop_watch': cropWatch,
        'advisory_summary': advisorySummary,
        if (spokenSummary != null) 'spoken_summary': spokenSummary,
      };
}
