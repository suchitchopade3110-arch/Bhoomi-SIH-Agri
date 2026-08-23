import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/farm_summary.dart';

class FarmIdentityCard extends StatelessWidget {
  final FarmIdentity farm;

  const FarmIdentityCard({
    super.key,
    required this.farm,
  });

  String _formatCrop(String crop) {
    switch (crop) {
      case 'samba_paddy':
        return 'Samba Paddy';
      case 'kuruvai_paddy':
        return 'Kuruvai Paddy';
      case 'sugarcane':
        return 'Sugarcane';
      case 'cotton':
        return 'Cotton';
      case 'banana':
        return 'Banana';
      case 'maize':
        return 'Maize (Corn)';
      default:
        return crop.replaceAll('_', ' ').toUpperCase();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isVerified = farm.landStatus == 'verified';

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.sm + 2,
                  vertical: AppSpacing.xs,
                ),
                decoration: BoxDecoration(
                  color: AppColors.primaryGreen.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                ),
                child: Text(
                  'FARM ID: ${farm.id}',
                  style: AppTypography.labelMedium.copyWith(
                    color: AppColors.primaryGreen,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.md,
                  vertical: AppSpacing.xs,
                ),
                decoration: BoxDecoration(
                  color: isVerified
                      ? AppColors.statusVerified.withValues(alpha: 0.1)
                      : AppColors.statusPending.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                  border: Border.all(
                    color: isVerified
                        ? AppColors.statusVerified.withValues(alpha: 0.3)
                        : AppColors.statusPending.withValues(alpha: 0.3),
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      isVerified ? Icons.verified_rounded : Icons.pending_actions_rounded,
                      size: 14.0,
                      color: isVerified ? AppColors.statusVerified : AppColors.statusPending,
                    ),
                    const SizedBox(width: AppSpacing.xs),
                    Text(
                      isVerified ? 'Verified Land' : 'Pending Verification',
                      style: AppTypography.labelMedium.copyWith(
                        color: isVerified ? AppColors.statusVerified : AppColors.statusPending,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(AppSpacing.md),
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                ),
                child: const Icon(
                  Icons.eco_rounded,
                  size: 32.0,
                  color: AppColors.primaryGreen,
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Primary Crop',
                      style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted),
                    ),
                    const SizedBox(height: 2.0),
                    Text(
                      _formatCrop(farm.crop),
                      style: AppTypography.headlineMedium.copyWith(
                        fontWeight: FontWeight.w800,
                        color: AppColors.textPrimary,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
