import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/scheme_summary.dart';
import 'scheme_match_badge.dart';

class SchemeCard extends StatelessWidget {
  final SchemeSummary scheme;
  final VoidCallback onTap;

  const SchemeCard({
    super.key,
    required this.scheme,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    scheme.title,
                    style: AppTypography.titleLarge.copyWith(fontWeight: FontWeight.w800),
                  ),
                ),
                const SizedBox(width: AppSpacing.sm),
                SchemeMatchBadge(matchStatus: scheme.matchStatus),
              ],
            ),
            const SizedBox(height: AppSpacing.xs),
            Text(
              scheme.shortDescription,
              style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
            ),

            if (scheme.matchExplanation != null) ...[
              const SizedBox(height: AppSpacing.md),
              Container(
                padding: const EdgeInsets.all(AppSpacing.sm),
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.info_outline_rounded, size: 16.0, color: AppColors.primaryGreen),
                    const SizedBox(width: AppSpacing.xs),
                    Expanded(
                      child: Text(
                        scheme.matchExplanation!,
                        style: const TextStyle(fontSize: 11.0, color: AppColors.textPrimary, fontWeight: FontWeight.w500),
                      ),
                    ),
                  ],
                ),
              ),
            ],

            if (scheme.benefitSummary != null) ...[
              const SizedBox(height: AppSpacing.sm),
              Row(
                children: [
                  const Icon(Icons.card_giftcard_rounded, size: 16.0, color: Color(0xFFD97706)),
                  const SizedBox(width: AppSpacing.xs),
                  Text(
                    scheme.benefitSummary!,
                    style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: Color(0xFFD97706)),
                  ),
                ],
              ),
            ],

            const SizedBox(height: AppSpacing.md),
            Align(
              alignment: Alignment.centerRight,
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    scheme.isMoreInfoNeeded ? 'Provide Details' : 'View Scheme Details',
                    style: const TextStyle(
                      fontSize: 12.0,
                      fontWeight: FontWeight.w700,
                      color: AppColors.primaryGreen,
                    ),
                  ),
                  const SizedBox(width: 4.0),
                  const Icon(Icons.arrow_forward_rounded, size: 14.0, color: AppColors.primaryGreen),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
