import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/weather_data.dart';
import 'forecast_strip.dart';

class WeatherCard extends StatelessWidget {
  final WeatherData weather;

  const WeatherCard({
    super.key,
    required this.weather,
  });

  IconData _getWeatherIcon(String condition) {
    final lower = condition.toLowerCase();
    if (lower.contains('rain') || lower.contains('shower')) {
      return Icons.grain_rounded;
    } else if (lower.contains('cloud')) {
      return Icons.cloud_queue_rounded;
    } else if (lower.contains('thunder')) {
      return Icons.thunderstorm_rounded;
    }
    return Icons.wb_sunny_rounded;
  }

  @override
  Widget build(BuildContext context) {
    final icon = _getWeatherIcon(weather.condition);

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  const Icon(Icons.location_on, size: 16.0, color: AppColors.primaryGreen),
                  const SizedBox(width: AppSpacing.xs),
                  Text(
                    'Field Weather',
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.textMuted,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2.0),
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                ),
                child: Text(
                  weather.condition,
                  style: AppTypography.labelMedium.copyWith(
                    color: AppColors.primaryGreen,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),

          // Main Weather Row
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(AppSpacing.md),
                decoration: BoxDecoration(
                  color: AppColors.warmAccent.withValues(alpha: 0.12),
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, color: AppColors.warmAccent, size: 36.0),
              ),
              const SizedBox(width: AppSpacing.lg),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${weather.temperatureC.toInt()}',
                        style: AppTypography.displayLarge.copyWith(
                          fontWeight: FontWeight.w800,
                          fontSize: 36.0,
                        ),
                      ),
                      const Text(
                        '°C',
                        style: TextStyle(
                          fontSize: 20.0,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textMuted,
                        ),
                      ),
                    ],
                  ),
                  Text(
                    'Humidity: ${weather.humidityPct}% • Rain: ${weather.rainfallProbPct}%',
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                ],
              ),
            ],
          ),

          if (weather.forecastSummary != null) ...[
            const SizedBox(height: AppSpacing.md),
            Text(
              weather.forecastSummary!,
              style: AppTypography.bodyMedium.copyWith(
                fontSize: 13.0,
                color: AppColors.textSecondary,
              ),
            ),
          ],

          if (weather.dailyForecast.isNotEmpty) ...[
            const Divider(color: AppColors.divider, height: AppSpacing.lg),
            ForecastStrip(forecast: weather.dailyForecast),
          ],
        ],
      ),
    );
  }
}
