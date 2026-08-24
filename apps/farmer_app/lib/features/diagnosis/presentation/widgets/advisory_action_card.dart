import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';

class AdvisoryActionCard extends StatelessWidget {
  final List<String> actions;
  final String? caution;
  final VoidCallback? onSave;
  final VoidCallback? onShare;

  const AdvisoryActionCard({
    super.key,
    required this.actions,
    this.caution,
    this.onSave,
    this.onShare,
  });

  @override
  Widget build(BuildContext context) {
    if (actions.isEmpty && (caution == null || caution!.isEmpty)) {
      return const SizedBox.shrink();
    }

    final actionCount = actions.length;
    final planTitle = actionCount == 5 ? '5-Point Action Plan' : '$actionCount-Step Action Plan';

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
                    padding: const EdgeInsets.all(AppSpacing.xs + 2),
                    decoration: const BoxDecoration(
                      color: AppColors.lightGreen,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.assignment_turned_in_rounded, size: 18.0, color: AppColors.primaryGreen),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Text(
                    planTitle,
                    style: const TextStyle(
                      fontSize: 17.0,
                      fontWeight: FontWeight.w800,
                      color: AppColors.textPrimary,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 4.0),
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
                    width: 24.0,
                    height: 24.0,
                    decoration: const BoxDecoration(
                      color: AppColors.lightGreen,
                      shape: BoxShape.circle,
                    ),
                    child: Center(
                      child: Text(
                        '${idx + 1}',
                        style: const TextStyle(
                          fontSize: 12.0,
                          fontWeight: FontWeight.w900,
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
                        fontWeight: FontWeight.w600,
                        color: AppColors.textPrimary,
                        height: 1.35,
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
            const SizedBox(height: AppSpacing.md),
          ],

          const Divider(color: AppColors.divider),
          const SizedBox(height: AppSpacing.xs),

          // [ Save Advice ]   [ Share ] Action Buttons
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {
                    if (onSave != null) {
                      onSave!();
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Advice saved to your farm records!'),
                          backgroundColor: AppColors.primaryGreen,
                        ),
                      );
                    }
                  },
                  icon: const Icon(Icons.bookmark_border_rounded, size: 18.0),
                  label: const Text('Save Advice'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.primaryGreen,
                    side: const BorderSide(color: AppColors.primaryGreen, width: 1.5),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    padding: const EdgeInsets.symmetric(vertical: 10.0),
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {
                    if (onShare != null) {
                      onShare!();
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Advisory link copied to clipboard!'),
                          backgroundColor: AppColors.primaryGreen,
                        ),
                      );
                    }
                  },
                  icon: const Icon(Icons.share_outlined, size: 18.0),
                  label: const Text('Share'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.textSecondary,
                    side: const BorderSide(color: AppColors.border, width: 1.5),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    padding: const EdgeInsets.symmetric(vertical: 10.0),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
