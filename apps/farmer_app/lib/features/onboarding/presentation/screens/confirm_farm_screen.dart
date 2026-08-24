import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/degraded_network_banner.dart';
import '../../application/onboarding_controller.dart';

class ConfirmFarmScreen extends ConsumerWidget {
  const ConfirmFarmScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(onboardingControllerProvider);
    final controller = ref.read(onboardingControllerProvider.notifier);
    final networkState = ref.watch(networkStateProvider);
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.confirmProfileTitle),
      ),
      body: SafeArea(
        child: Column(
          children: [
            DegradedNetworkBanner(networkState: networkState),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(AppSpacing.lg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Header card
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.lg),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: [
                            AppColors.primaryGreen,
                            Color(0xFF1B5E20),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(AppSpacing.sm),
                                decoration: BoxDecoration(
                                  color: Colors.white.withValues(alpha: 0.2),
                                  shape: BoxShape.circle,
                                ),
                                child: const Icon(
                                  Icons.agriculture_rounded,
                                  color: Colors.white,
                                  size: 24.0,
                                ),
                              ),
                              const SizedBox(width: AppSpacing.md),
                              Text(
                                strings.yourFarmProfile,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 20.0,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: AppSpacing.sm),
                          Text(
                            strings.confirmProfileReviewDesc,
                            style: TextStyle(
                              color: Colors.white.withValues(alpha: 0.9),
                              fontSize: 14.0,
                              height: 1.4,
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    // Error Message Banner if any
                    if (state.errorMessage != null) ...[
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFFEBEE),
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          border: Border.all(color: const Color(0xFFFFCDD2)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.error_outline, color: Color(0xFFC62828)),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(
                              child: Text(
                                state.errorMessage!,
                                style: const TextStyle(
                                  color: Color(0xFFC62828),
                                  fontSize: 13.0,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: AppSpacing.lg),
                    ],

                    // Details Card
                    BhoomiCard(
                      child: Column(
                        children: [
                          _buildReviewRow(
                            icon: Icons.grass_rounded,
                            label: strings.labelCrop,
                            value: strings.cropName(state.crop),
                            onEdit: () {
                              controller.goToStep(0);
                              context.pop();
                            },
                          ),
                          const Divider(color: AppColors.divider, height: AppSpacing.lg),
                          _buildReviewRow(
                            icon: Icons.square_foot_rounded,
                            label: strings.labelLandArea,
                            value: strings.formatAcres(state.areaAcresSelfReported),
                            onEdit: () {
                              controller.goToStep(1);
                              context.pop();
                            },
                          ),
                          const Divider(color: AppColors.divider, height: AppSpacing.lg),
                          _buildReviewRow(
                            icon: Icons.spa_rounded,
                            label: strings.labelGrowthStage,
                            value: strings.stageName(state.growthStage),
                            onEdit: () {
                              controller.goToStep(2);
                              context.pop();
                            },
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: AppSpacing.xl),
                  ],
                ),
              ),
            ),

            // Submit Button Area
            Container(
              padding: const EdgeInsets.all(AppSpacing.lg),
              decoration: const BoxDecoration(
                color: AppColors.surface,
                border: Border(
                  top: BorderSide(color: AppColors.border, width: 1.0),
                ),
              ),
              child: BhoomiPrimaryButton(
                text: strings.saveMyFarm,
                isLoading: state.isSubmitting,
                icon: Icons.save_rounded,
                onPressed: () async {
                  final farmId = await controller.submitFarm();
                  if (farmId != null && context.mounted) {
                    context.go('/home/$farmId');
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildReviewRow({
    required IconData icon,
    required String label,
    required String value,
    required VoidCallback onEdit,
  }) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(AppSpacing.sm),
          decoration: BoxDecoration(
            color: AppColors.primaryGreen.withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, size: 18.0, color: AppColors.primaryGreen),
        ),
        const SizedBox(width: AppSpacing.md),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted),
              ),
              const SizedBox(height: 2.0),
              Text(
                value,
                style: AppTypography.titleMedium.copyWith(
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
        IconButton(
          icon: const Icon(Icons.edit_outlined, size: 18.0, color: AppColors.primaryGreen),
          onPressed: onEdit,
          tooltip: 'Edit $label',
        ),
      ],
    );
  }
}
