class DailyForecastItem {
  final String day;
  final double tempMaxC;
  final double tempMinC;
  final String condition;

  const DailyForecastItem({
    required this.day,
    required this.tempMaxC,
    required this.tempMinC,
    required this.condition,
  });

  factory DailyForecastItem.fromJson(Map<String, dynamic> json) {
    return DailyForecastItem(
      day: json['forecast_date'] as String? ?? json['day'] as String? ?? 'Today',
      tempMaxC: (json['temp_max_c'] as num?)?.toDouble() ?? 32.0,
      tempMinC: (json['temp_min_c'] as num?)?.toDouble() ?? 24.0,
      condition: json['condition_description'] as String? ?? json['condition'] as String? ?? 'Sunny',
    );
  }

  Map<String, dynamic> toJson() => {
        'day': day,
        'temp_max_c': tempMaxC,
        'temp_min_c': tempMinC,
        'condition': condition,
      };
}

class WeatherData {
  final String condition;
  final double temperatureC;
  final int humidityPct;
  final double rainfallMm;
  final int rainfallProbPct;
  final double? windSpeedKmh;
  final String? forecastSummary;
  final List<DailyForecastItem> dailyForecast;

  const WeatherData({
    required this.condition,
    required this.temperatureC,
    required this.humidityPct,
    required this.rainfallMm,
    required this.rainfallProbPct,
    this.windSpeedKmh,
    this.forecastSummary,
    this.dailyForecast = const [],
  });

  factory WeatherData.fromJson(Map<String, dynamic> json) {
    final forecastList = json['daily_forecasts'] ?? json['daily_forecast'];
    return WeatherData(
      condition: json['condition_description'] as String? ?? json['condition'] as String? ?? 'Partly Cloudy',
      temperatureC: (json['temperature_c'] as num?)?.toDouble() ?? 31.5,
      humidityPct: (json['relative_humidity_pct'] as num?)?.toInt() ?? (json['humidity_pct'] as num?)?.toInt() ?? 68,
      rainfallMm: (json['precipitation_mm'] as num?)?.toDouble() ?? (json['rainfall_mm'] as num?)?.toDouble() ?? 0.0,
      rainfallProbPct: (json['precipitation_probability_pct'] as num?)?.toInt() ?? (json['rainfall_prob_pct'] as num?)?.toInt() ?? 15,
      windSpeedKmh: (json['wind_speed_kmh'] as num?)?.toDouble() ?? 12.0,
      forecastSummary: json['spoken_summary'] as String? ?? json['forecast_summary'] as String? ?? 'Favorable dry conditions for fieldwork today.',
      dailyForecast: forecastList is List
          ? forecastList
              .map((i) => DailyForecastItem.fromJson(i as Map<String, dynamic>))
              .toList()
          : const [
              DailyForecastItem(day: 'Today', tempMaxC: 32, tempMinC: 24, condition: 'Partly Cloudy'),
              DailyForecastItem(day: 'Tomorrow', tempMaxC: 33, tempMinC: 24, condition: 'Sunny'),
              DailyForecastItem(day: 'Sat', tempMaxC: 31, tempMinC: 23, condition: 'Scattered Rain'),
            ],
    );
  }

  Map<String, dynamic> toJson() => {
        'condition': condition,
        'temperature_c': temperatureC,
        'humidity_pct': humidityPct,
        'rainfall_mm': rainfallMm,
        'rainfall_prob_pct': rainfallProbPct,
        if (windSpeedKmh != null) 'wind_speed_kmh': windSpeedKmh,
        if (forecastSummary != null) 'forecast_summary': forecastSummary,
        'daily_forecast': dailyForecast.map((f) => f.toJson()).toList(),
      };
}
