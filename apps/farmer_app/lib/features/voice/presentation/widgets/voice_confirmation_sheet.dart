import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../../data/models/transcribe_response.dart';

class VoiceConfirmationSheet extends StatelessWidget {
  final TranscribeResponse transcription;
  final VoidCallback onConfirm;
  final VoidCallback onCancel;

  const VoiceConfirmationSheet({
    super.key,
    required this.transcription,
    required this.onConfirm,
    required this.onCancel,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(AppSpacing.radiusXl)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Center(
            child: Container(
              width: 40.0,
              height: 4.0,
              decoration: BoxDecoration(
                color: AppColors.border,
                borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
              ),
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(AppSpacing.sm),
                decoration: BoxDecoration(
                  color: AppColors.warmAccent.withValues(alpha: 0.15),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.hearing_rounded, color: Color(0xFFD35400), size: 22.0),
              ),
              const SizedBox(width: AppSpacing.md),
              const Expanded(
                child: Text(
                  'Please Confirm Speech',
                  style: AppTypography.headlineMedium,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
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
                Text(
                  'We heard:',
                  style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted),
                ),
                const SizedBox(height: 4.0),
                Text(
                  '"${transcription.text}"',
                  style: AppTypography.titleLarge.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AppColors.textPrimary,
                  ),
                ),
                if (transcription.parsedIntent?.entity != null) ...[
                  const SizedBox(height: AppSpacing.sm),
                  Text(
                    'Parsed value: ${transcription.parsedIntent!.entity} = ${transcription.parsedIntent!.value}',
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.primaryGreen,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          Row(
            children: [
              Expanded(
                child: BhoomiSecondaryButton(
                  text: 'Change',
                  icon: Icons.edit_outlined,
                  onPressed: onCancel,
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: BhoomiPrimaryButton(
                  text: 'Yes, Correct',
                  icon: Icons.check_circle_rounded,
                  onPressed: onConfirm,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
        ],
      ),
    );
  }
}
