import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../land/presentation/widgets/land_status_badge.dart';
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
    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: Container(
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
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.primaryGreen,
                      fontWeight: FontWeight.w700,
                      fontSize: 11.0,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.xs),
              LandStatusBadge(status: farm.landStatus),
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
