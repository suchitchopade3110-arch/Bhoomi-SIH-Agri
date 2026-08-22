import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/health_snapshot.dart';

class HealthBreakdownCard extends StatelessWidget {
  final HealthSubIndices subIndices;

  const HealthBreakdownCard({
    super.key,
    required this.subIndices,
  });

  @override
  Widget build(BuildContext context) {
    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.analytics_outlined, size: 20.0, color: AppColors.primaryGreen),
              SizedBox(width: AppSpacing.sm),
              Text('Explainable Score Breakdown', style: AppTypography.titleLarge),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'Composite health calculated across 6 key agronomic dimensions.',
            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textMuted),
          ),
          const Divider(color: AppColors.divider, height: AppSpacing.lg),

          _buildMetricRow('Environmental Suitability', subIndices.environmentalSuitability),
          const SizedBox(height: AppSpacing.md),
          _buildMetricRow('Resource Adequacy', subIndices.resourceAdequacy),
          const SizedBox(height: AppSpacing.md),
          _buildMetricRow('Crop Stage Progression', subIndices.cropStageProgression),
          const SizedBox(height: AppSpacing.md),
          _buildMetricRow('Active Problem Load', subIndices.activeProblemLoad),
          const SizedBox(height: AppSpacing.md),
          _buildMetricRow('Monitoring Recency', subIndices.monitoringRecency),
          const SizedBox(height: AppSpacing.md),
          _buildMetricRow('Treatment Response', subIndices.treatmentResponse),
        ],
      ),
    );
  }

  Widget _buildMetricRow(String label, double value) {
    final pct = (value * 100).toInt();
    final Color barColor = value >= 0.8
        ? AppColors.primaryGreen
        : value >= 0.6
            ? AppColors.warmAccent
            : const Color(0xFFC62828);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(fontSize: 13.0, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
            Text('$pct / 100', style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: barColor)),
          ],
        ),
        const SizedBox(height: 4.0),
        ClipRRect(
          borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
          child: LinearProgressIndicator(
            value: value.clamp(0.0, 1.0),
            minHeight: 6.0,
            backgroundColor: AppColors.border,
            valueColor: AlwaysStoppedAnimation<Color>(barColor),
          ),
        ),
      ],
    );
  }
}
