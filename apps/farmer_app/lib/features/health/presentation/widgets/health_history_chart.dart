import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/health_history.dart';

class HealthHistoryChart extends StatelessWidget {
  final HealthHistory healthHistory;

  const HealthHistoryChart({
    super.key,
    required this.healthHistory,
  });

  Color _getBandColor(String band) {
    switch (band.toLowerCase()) {
      case 'good':
      case 'excellent':
        return AppColors.healthGood;
      case 'moderate':
      case 'fair':
      case 'watch':
        return AppColors.healthModerate;
      case 'poor':
      case 'critical':
        return AppColors.healthPoor;
      case 'unrated':
      default:
        return AppColors.healthUnrated;
    }
  }

  @override
  Widget build(BuildContext context) {
    final points = healthHistory.history;

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.timeline_rounded, color: AppColors.primaryGreen, size: 20.0),
              SizedBox(width: AppSpacing.sm),
              Text('Health Journey Timeline', style: AppTypography.titleLarge),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'Chronological score movements with verified triggering causes.',
            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textMuted),
          ),
          const Divider(color: AppColors.divider, height: AppSpacing.lg),

          ...points.asMap().entries.map((entry) {
            final idx = entry.key;
            final pt = entry.value;
            final isLast = idx == points.length - 1;
            final bandColor = _getBandColor(pt.band);

            return Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Column(
                  children: [
                    Container(
                      width: 32.0,
                      height: 32.0,
                      decoration: BoxDecoration(
                        color: bandColor.withValues(alpha: 0.15),
                        shape: BoxShape.circle,
                        border: Border.all(color: bandColor, width: 2.0),
                      ),
                      child: Center(
                        child: Text(
                          pt.isRated ? '${pt.score}' : '–',
                          style: TextStyle(
                            fontSize: 11.0,
                            fontWeight: FontWeight.w800,
                            color: bandColor,
                          ),
                        ),
                      ),
                    ),
                    if (!isLast)
                      Container(
                        width: 2.0,
                        height: 36.0,
                        color: AppColors.border,
                      ),
                  ],
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.md),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              pt.isRated ? '${pt.score}/100 • ${pt.band.toUpperCase()}' : 'UNRATED BASELINE',
                              style: TextStyle(
                                fontSize: 13.0,
                                fontWeight: FontWeight.w700,
                                color: bandColor,
                              ),
                            ),
                            Text(
                              pt.recordedAt.length >= 10 ? pt.recordedAt.substring(0, 10) : pt.recordedAt,
                              style: const TextStyle(fontSize: 11.0, color: AppColors.textMuted),
                            ),
                          ],
                        ),
                        if (pt.reason != null && pt.reason!.isNotEmpty) ...[
                          const SizedBox(height: 2.0),
                          Text(
                            pt.reason!,
                            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textSecondary),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            );
          }),
        ],
      ),
    );
  }
}
