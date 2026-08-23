import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';

class AdvisoryActionCard extends StatelessWidget {
  final List<String> actions;
  final String? caution;

  const AdvisoryActionCard({
    super.key,
    required this.actions,
    this.caution,
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
              Icon(Icons.assignment_turned_in_outlined, size: 20.0, color: AppColors.primaryGreen),
              SizedBox(width: AppSpacing.sm),
              Text('What You Can Do', style: AppTypography.titleLarge),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'Recommended immediate agronomic management steps:',
            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textMuted),
          ),
          const Divider(color: AppColors.divider, height: AppSpacing.lg),

          ...actions.asMap().entries.map((entry) {
            final idx = entry.key;
            final action = entry.value;

            return Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.md),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 22.0,
                    height: 22.0,
                    decoration: BoxDecoration(
                      color: AppColors.primaryGreen.withValues(alpha: 0.12),
                      shape: BoxShape.circle,
                    ),
                    child: Center(
                      child: Text(
                        '${idx + 1}',
                        style: const TextStyle(
                          fontSize: 12.0,
                          fontWeight: FontWeight.w800,
                          color: AppColors.primaryGreen,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Text(
                      action,
                      style: AppTypography.bodyLarge.copyWith(
                        fontSize: 14.0,
                        color: AppColors.textPrimary,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }),

          if (caution != null && caution!.isNotEmpty) ...[
            const SizedBox(height: AppSpacing.xs),
            Container(
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                color: const Color(0xFFFEF3C7),
                borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                border: Border.all(color: const Color(0xFFFDE68A)),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.warning_rounded, color: Color(0xFFD97706), size: 20.0),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Important Caution',
                          style: TextStyle(fontWeight: FontWeight.w800, fontSize: 12.0, color: Color(0xFF92400E)),
                        ),
                        const SizedBox(height: 2.0),
                        Text(
                          caution!,
                          style: const TextStyle(fontSize: 12.0, color: Color(0xFF78350F)),
                        ),
                      ],
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
