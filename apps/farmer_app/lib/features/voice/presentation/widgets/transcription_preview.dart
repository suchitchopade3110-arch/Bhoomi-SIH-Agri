import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../data/models/transcribe_response.dart';

class TranscriptionPreview extends StatelessWidget {
  final TranscribeResponse transcription;

  const TranscriptionPreview({
    super.key,
    required this.transcription,
  });

  @override
  Widget build(BuildContext context) {
    final confidencePct = (transcription.confidence * 100).toInt();

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  const Icon(Icons.record_voice_over_rounded, size: 16.0, color: AppColors.primaryGreen),
                  const SizedBox(width: AppSpacing.xs),
                  Text(
                    'Recognized Speech',
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.primaryGreen,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.sm,
                  vertical: 2.0,
                ),
                decoration: BoxDecoration(
                  color: transcription.isHighConfidence
                      ? AppColors.primaryGreen.withValues(alpha: 0.1)
                      : AppColors.warmAccent.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                ),
                child: Text(
                  '$confidencePct% confidence',
                  style: AppTypography.labelMedium.copyWith(
                    fontSize: 10.0,
                    color: transcription.isHighConfidence
                        ? AppColors.primaryGreen
                        : const Color(0xFFD35400),
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            '"${transcription.text}"',
            style: AppTypography.titleMedium.copyWith(
              fontWeight: FontWeight.w600,
              fontStyle: FontStyle.italic,
            ),
          ),
        ],
      ),
    );
  }
}
