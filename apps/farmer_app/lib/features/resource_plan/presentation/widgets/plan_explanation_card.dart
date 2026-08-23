import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../data/models/resource_plan.dart';

class PlanExplanationCard extends StatelessWidget {
  final ExplainabilityInputs inputs;
  final double? et0;
  final double? kc;
  final double? waterNeed;

  const PlanExplanationCard({
    super.key,
    required this.inputs,
    this.et0,
    this.kc,
    this.waterNeed,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
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
              const Icon(Icons.psychology_alt_rounded, size: 16.0, color: AppColors.primaryGreen),
              const SizedBox(width: AppSpacing.xs),
              Text(
                'Scientific Calculation Inputs',
                style: AppTypography.labelMedium.copyWith(
                  color: AppColors.primaryGreen,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            inputs.formulaDescription ?? 'Computed from standard reference evapotranspiration adjusted for crop growth stage.',
            style: AppTypography.bodyMedium.copyWith(fontSize: 11.0, color: AppColors.textMuted),
          ),
          const Divider(color: AppColors.divider, height: AppSpacing.md),

          // Inspectable grid
          _buildParamRow('Evapotranspiration (ET0)', '${inputs.evapotranspirationEt0 ?? et0 ?? 4.8} mm/day'),
          const SizedBox(height: AppSpacing.xs),
          _buildParamRow('Crop Coefficient (Kc)', '${inputs.cropStageKc ?? kc ?? 1.15} (Vegetative)'),
          const SizedBox(height: AppSpacing.xs),
          _buildParamRow('Effective Rainfall', '${inputs.effectiveRainfallMm ?? 0.0} mm'),
          if (inputs.soilRetentionFactor != null) ...[
            const SizedBox(height: AppSpacing.xs),
            _buildParamRow('Soil Retention Factor', '${inputs.soilRetentionFactor}'),
          ],
        ],
      ),
    );
  }

  Widget _buildParamRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(fontSize: 12.0, color: AppColors.textSecondary)),
        Text(value, style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
      ],
    );
  }
}
