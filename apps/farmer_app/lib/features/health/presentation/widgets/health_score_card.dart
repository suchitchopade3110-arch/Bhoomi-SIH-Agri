import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/health_snapshot.dart';

class HealthScoreCard extends StatelessWidget {
  final HealthSnapshot snapshot;

  const HealthScoreCard({
    super.key,
    required this.snapshot,
  });

  Color _getBandColor(String band) {
    switch (band.toLowerCase()) {
      case 'good':
      case 'excellent':
        return AppColors.healthGood;
      case 'moderate':
      case 'fair':
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
    final isRated = snapshot.isRated;
    final bandColor = _getBandColor(snapshot.band);

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
                  Icon(Icons.favorite_rounded, color: bandColor, size: 22.0),
                  const SizedBox(width: AppSpacing.sm),
                  const Text('Farm Health Score', style: AppTypography.titleLarge),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 2.0),
                decoration: BoxDecoration(
                  color: bandColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                  border: Border.all(color: bandColor.withValues(alpha: 0.3)),
                ),
                child: Text(
                  snapshot.band.toUpperCase(),
                  style: AppTypography.labelMedium.copyWith(
                    color: bandColor,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.lg),

          if (isRated) ...[
            Row(
              crossAxisAlignment: CrossAxisAlignment.baseline,
              textBaseline: TextBaseline.alphabetic,
              children: [
                Text(
                  '${snapshot.score}',
                  style: AppTypography.scoreLarge.copyWith(color: bandColor, fontSize: 52.0),
                ),
                const SizedBox(width: AppSpacing.xs),
                Text(
                  '/ 100',
                  style: AppTypography.titleLarge.copyWith(color: AppColors.textMuted),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.xs),
            ClipRRect(
              borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
              child: LinearProgressIndicator(
                value: (snapshot.score! / 100.0).clamp(0.0, 1.0),
                minHeight: 10.0,
                backgroundColor: AppColors.border,
                valueColor: AlwaysStoppedAnimation<Color>(bandColor),
              ),
            ),
          ] else ...[
            // STRICT NULL HANDLING: Never show 0/100
            Container(
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                color: AppColors.background,
                borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.info_outline_rounded, color: AppColors.healthUnrated, size: 24.0),
                      const SizedBox(width: AppSpacing.sm),
                      Text(
                        'Unrated',
                        style: AppTypography.headlineMedium.copyWith(
                          color: AppColors.healthUnrated,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    snapshot.explanation ?? 'We need more farm information to calculate your health score.',
                    style: AppTypography.bodyMedium.copyWith(
                      color: AppColors.textSecondary,
                      fontSize: 13.0,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}
