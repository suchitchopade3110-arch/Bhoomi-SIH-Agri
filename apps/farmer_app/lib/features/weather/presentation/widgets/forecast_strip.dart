import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../data/models/weather_data.dart';

class ForecastStrip extends StatelessWidget {
  final List<DailyForecastItem> forecast;

  const ForecastStrip({
    super.key,
    required this.forecast,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: forecast.map((item) {
        return Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
            margin: const EdgeInsets.symmetric(horizontal: 2.0),
            decoration: BoxDecoration(
              color: AppColors.background,
              borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
            ),
            child: Column(
              children: [
                Text(
                  item.day,
                  style: AppTypography.labelMedium.copyWith(
                    fontSize: 11.0,
                    color: AppColors.textMuted,
                  ),
                ),
                const SizedBox(height: 2.0),
                Text(
                  '${item.tempMaxC.toInt()}°',
                  style: AppTypography.labelLarge.copyWith(
                    fontSize: 13.0,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}
