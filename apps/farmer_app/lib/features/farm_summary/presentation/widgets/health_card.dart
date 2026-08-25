import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/farm_summary.dart';

class HealthCard extends ConsumerWidget {
  final FarmHealth health;

  const HealthCard({
    super.key,
    required this.health,
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
  Widget build(BuildContext context, WidgetRef ref) {
    final strings = ref.watch(bhoomiStringsProvider);
    final isRated = health.isRated;
    final bandColor = _getBandColor(health.band);

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Row(
                  children: [
                    Icon(
                      Icons.favorite_rounded,
                      size: 20.0,
                      color: bandColor,
                    ),
                    const SizedBox(width: AppSpacing.sm),
                    Flexible(
                      child: Text(
                        strings.text('farm_health_score'),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: AppTypography.titleLarge,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: AppSpacing.xs),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.sm + 2,
                  vertical: AppSpacing.xs,
                ),
                decoration: BoxDecoration(
                  color: bandColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                  border: Border.all(color: bandColor.withValues(alpha: 0.3)),
                ),
                child: Text(
                  isRated ? strings.translateHealthBand(health.band) : strings.text('health_unrated'),
                  style: AppTypography.labelMedium.copyWith(
                    color: bandColor,
                    fontWeight: FontWeight.w700,
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
                  '${health.score}',
                  style: AppTypography.scoreLarge.copyWith(color: bandColor),
                ),
                const SizedBox(width: AppSpacing.xs),
                Text(
                  '/ 100',
                  style: AppTypography.titleMedium.copyWith(
                    color: AppColors.textMuted,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.sm),
            ClipRRect(
              borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
              child: LinearProgressIndicator(
                value: (health.score! / 100.0).clamp(0.0, 1.0),
                minHeight: 8.0,
                backgroundColor: AppColors.border,
                valueColor: AlwaysStoppedAnimation<Color>(bandColor),
              ),
            ),
          ] else ...[
            // STRICT CONTRACT: Never show 0/100 when score is null. Render "Unrated".
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.md,
                vertical: AppSpacing.md,
              ),
              decoration: BoxDecoration(
                color: AppColors.background,
                borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                border: Border.all(color: AppColors.border),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.info_outline_rounded,
                    color: AppColors.healthUnrated,
                    size: 24.0,
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          strings.text('health_unrated'),
                          style: AppTypography.headlineMedium.copyWith(
                            color: AppColors.healthUnrated,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(height: 2.0),
                        Text(
                          strings.text('health_unrated_desc'),
                          style: AppTypography.bodyMedium.copyWith(
                            color: AppColors.textMuted,
                            fontSize: 13.0,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
          if (health.computedAt != null) ...[
            const SizedBox(height: AppSpacing.md),
            Text(
              '${strings.text('last_computed')}: ${health.computedAt}',
              style: AppTypography.labelMedium.copyWith(
                color: AppColors.textMuted,
                fontSize: 11.0,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
