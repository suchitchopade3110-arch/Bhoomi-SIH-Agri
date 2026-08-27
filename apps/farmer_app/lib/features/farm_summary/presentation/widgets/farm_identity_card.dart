import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../land/presentation/widgets/land_status_badge.dart';
import '../../data/models/farm_summary.dart';
import '../../../onboarding/data/farm_repository.dart';
import '../../../onboarding/data/models/farm_update_models.dart';
import '../../application/farm_summary_provider.dart';

class FarmIdentityCard extends ConsumerWidget {
  final FarmIdentity farm;

  const FarmIdentityCard({
    super.key,
    required this.farm,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final strings = ref.watch(bhoomiStringsProvider);

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
                    color: AppColors.lightGreen,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                  ),
                  child: Text(
                    'FARM ID: ${farm.id}',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.primaryGreen,
                      fontWeight: FontWeight.w800,
                      fontSize: 11.0,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.xs),
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  LandStatusBadge(status: farm.landStatus),
                  const SizedBox(width: AppSpacing.xs),
                  IconButton(
                    icon: const Icon(Icons.edit_outlined, color: AppColors.primaryGreen, size: 20.0),
                    tooltip: 'Edit Farm Info',
                    constraints: const BoxConstraints(),
                    padding: EdgeInsets.zero,
                    onPressed: () => _showEditFarmSheet(context, ref, farm),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(AppSpacing.md),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppColors.primaryDeepGreen, AppColors.secondaryGreen],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                ),
                child: const Icon(
                  Icons.eco_rounded,
                  size: 28.0,
                  color: Colors.white,
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      strings.primaryCropLabel,
                      style: AppTypography.labelMedium.copyWith(
                        color: AppColors.textMuted,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 2.0),
                    Text(
                      strings.cropName(farm.crop),
                      style: const TextStyle(
                        fontSize: 20.0,
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

  void _showEditFarmSheet(BuildContext context, WidgetRef ref, FarmIdentity farm) {
    String crop = farm.crop;
    String stage = 'tillering';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(AppSpacing.radiusXl)),
      ),
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return Padding(
              padding: EdgeInsets.only(
                left: AppSpacing.lg,
                right: AppSpacing.lg,
                top: AppSpacing.lg,
                bottom: MediaQuery.of(context).viewInsets.bottom + AppSpacing.lg,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    strings.text('edit'),
                    style: const TextStyle(
                      fontSize: 18.0,
                      fontWeight: FontWeight.w800,
                      color: AppColors.primaryDeepGreen,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.md),
                  const Divider(color: AppColors.divider),
                  const SizedBox(height: AppSpacing.md),
                  Text(strings.primaryCropLabel, style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w600, color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.xs),
                  DropdownButtonFormField<String>(
                    initialValue: crop,
                    items: [
                      DropdownMenuItem(value: 'samba_paddy', child: Text(strings.cropName('samba_paddy'))),
                      DropdownMenuItem(value: 'kuruvai_paddy', child: Text(strings.cropName('kuruvai_paddy'))),
                      DropdownMenuItem(value: 'maize', child: Text(strings.cropName('maize'))),
                    ],
                    onChanged: (val) {
                      if (val != null) {
                        setState(() => crop = val);
                      }
                    },
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: AppColors.background,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    ),
                  ),
                  const SizedBox(height: AppSpacing.md),
                  Text(strings.text('growth_stage'), style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w600, color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.xs),
                  DropdownButtonFormField<String>(
                    initialValue: stage,
                    items: [
                      DropdownMenuItem(value: 'vegetative', child: Text(strings.translateStage('vegetative'))),
                      DropdownMenuItem(value: 'tillering', child: Text(strings.translateStage('tillering'))),
                      DropdownMenuItem(value: 'flowering', child: Text(strings.translateStage('flowering'))),
                      DropdownMenuItem(value: 'maturity', child: Text(strings.translateStage('maturity'))),
                    ],
                    onChanged: (val) {
                      if (val != null) {
                        setState(() => stage = val);
                      }
                    },
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: AppColors.background,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xl),
                  ElevatedButton(
                    onPressed: () async {
                      try {
                        final req = FarmUpdateRequest(
                          primaryCrop: crop,
                          growthStage: stage,
                          soilType: 'clay_loam',
                          irrigationSource: 'canal',
                        );
                        await ref.read(farmRepositoryProvider).updateFarm(farm.id, req);
                        ref.invalidate(farmSummaryProvider(farm.id));
                        if (context.mounted) {
                          Navigator.pop(context);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(strings.save),
                              backgroundColor: AppColors.primaryGreen,
                            ),
                          );
                        }
                      } catch (e) {
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Failed: $e')),
                          );
                        }
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryGreen,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    ),
                    child: Text(strings.save, style: const TextStyle(fontWeight: FontWeight.w700)),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}
