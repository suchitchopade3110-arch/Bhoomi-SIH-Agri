import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../data/models/diagnosis_response.dart';

class DiagnosisConfidenceCard extends StatelessWidget {
  final DiagnosisResponse response;

  const DiagnosisConfidenceCard({
    super.key,
    required this.response,
  });

  @override
  Widget build(BuildContext context) {
    final isHigh = response.isHighConfidence;
    final isLow = response.isLowConfidence;

    final Color color = isHigh
        ? AppColors.primaryGreen
        : isLow
            ? const Color(0xFFC62828)
            : const Color(0xFFD97706);

    final Color bgColor = color.withValues(alpha: 0.08);
    final Color borderColor = color.withValues(alpha: 0.25);

    final String title = isHigh
        ? 'Strong Match'
        : isLow
            ? 'Expert Verification Recommended'
            : 'Possible Match';

    final String description = isHigh
        ? 'The available information strongly supports this diagnosis.'
        : isLow
            ? 'The available symptoms are insufficient for a definite conclusion. Expert review is advised.'
            : 'Please verify the symptoms in your field before applying remedies.';

    final IconData icon = isHigh
        ? Icons.verified_rounded
        : isLow
            ? Icons.warning_amber_rounded
            : Icons.info_outline_rounded;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
        border: Border.all(color: borderColor),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 22.0),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      title,
                      style: AppTypography.titleMedium.copyWith(
                        color: color,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    if (response.confidenceScore != null)
                      Text(
                        '${(response.confidenceScore! * 100).toInt()}%',
                        style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w800, color: color),
                      ),
                  ],
                ),
                const SizedBox(height: 2.0),
                Text(
                  description,
                  style: AppTypography.bodyMedium.copyWith(
                    fontSize: 12.0,
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
