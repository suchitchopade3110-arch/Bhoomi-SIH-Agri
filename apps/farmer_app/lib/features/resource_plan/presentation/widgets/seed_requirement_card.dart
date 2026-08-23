import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/resource_plan.dart';

class SeedRequirementCard extends StatelessWidget {
  final ResourcePlan plan;

  const SeedRequirementCard({
    super.key,
    required this.plan,
  });

  @override
  Widget build(BuildContext context) {
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
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.sm),
                    decoration: const BoxDecoration(
                      color: Color(0xFFFEF3C7),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.grain_rounded, color: Color(0xFFD97706), size: 20.0),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  const Text('Seed Requirement', style: AppTypography.titleLarge),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm + 2, vertical: 2.0),
                decoration: BoxDecoration(
                  color: AppColors.warmAccent.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                ),
                child: Text(
                  '${plan.tillableAreaAcres} Acres',
                  style: AppTypography.labelMedium.copyWith(
                    color: const Color(0xFFD35400),
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.lg),

          Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                plan.totalSeedRequirementKg.toStringAsFixed(plan.totalSeedRequirementKg.truncateToDouble() == plan.totalSeedRequirementKg ? 0 : 1),
                style: AppTypography.displayLarge.copyWith(
                  color: const Color(0xFFD97706),
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              const Text('kg total', style: AppTypography.titleMedium),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'Calculated based on standard certified seed rate of ${plan.seedRateKgPerAcre} kg / acre.',
            style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
          ),
        ],
      ),
    );
  }
}
