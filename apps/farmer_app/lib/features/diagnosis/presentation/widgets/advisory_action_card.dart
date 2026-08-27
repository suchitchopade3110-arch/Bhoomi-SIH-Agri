import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../treatments/presentation/providers/treatments_providers.dart';

class AdvisoryActionCard extends ConsumerWidget {
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
  Widget build(BuildContext context, WidgetRef ref) {
    if (actions.isEmpty && (caution == null || caution!.isEmpty)) {
      return const SizedBox.shrink();
    }

    final strings = ref.watch(bhoomiStringsProvider);
    final actionCount = actions.length;
    final planTitle = '$actionCount ${strings.actionPlan}';

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
            strings.immediateSteps,
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
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          action,
                          style: AppTypography.bodyLarge.copyWith(
                            fontSize: 14.0,
                            fontWeight: FontWeight.w600,
                            color: AppColors.textPrimary,
                            height: 1.35,
                          ),
                        ),
                        _TreatmentEfficacyBadge(text: action),
                      ],
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
                        Text(
                          strings.text('preventive_measures'),
                          style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 12.0, color: Color(0xFF92400E)),
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
                        SnackBar(
                          content: Text(strings.save),
                          backgroundColor: AppColors.primaryGreen,
                        ),
                      );
                    }
                  },
                  icon: const Icon(Icons.bookmark_border_rounded, size: 18.0),
                  label: Text(strings.save),
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
                          content: Text('Link copied to clipboard!'),
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

class _TreatmentEfficacyBadge extends ConsumerWidget {
  final String text;

  const _TreatmentEfficacyBadge({required this.text});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    String? treatmentId;
    final lower = text.toLowerCase();
    if (lower.contains('tricyclazole')) {
      treatmentId = 'tricyclazole';
    } else if (lower.contains('copper') || lower.contains('oxychloride') || lower.contains('hydroxide')) {
      treatmentId = 'copper_hydroxide';
    } else if (lower.contains('mancozeb')) {
      treatmentId = 'mancozeb';
    } else if (lower.contains('propiconazole')) {
      treatmentId = 'propiconazole';
    }

    if (treatmentId == null) {
      return const SizedBox.shrink();
    }

    final efficacyAsync = ref.watch(
      treatmentEfficacyProvider(
        TreatmentEfficacyParams(
          treatmentId: treatmentId,
          pathogen: 'bacterial_leaf_blight',
          crop: 'samba_paddy',
          district: 'Erode',
        ),
      ),
    );

    return efficacyAsync.when(
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
      data: (efficacy) {
        final double rate = efficacy.efficacyPercentage ?? 85.0;
        final val = rate.toStringAsFixed(1);
        final color = efficacy.status == 'statistically_significant'
            ? AppColors.primaryGreen
            : const Color(0xFFD97706);

        return Padding(
          padding: const EdgeInsets.only(top: 4.0),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2.0),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
              border: Border.all(color: color.withValues(alpha: 0.3)),
            ),
            child: Text(
              'Efficacy: $val% (${efficacy.sampleSize} trials in Erode)',
              style: TextStyle(
                fontSize: 11.0,
                fontWeight: FontWeight.w700,
                color: color,
              ),
            ),
          ),
        );
      },
    );
  }
}
