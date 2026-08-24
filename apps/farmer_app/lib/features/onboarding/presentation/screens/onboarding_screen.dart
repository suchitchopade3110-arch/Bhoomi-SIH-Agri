import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../../../../core/widgets/degraded_network_banner.dart';
import '../../application/onboarding_controller.dart';
import '../widgets/farm_field_card.dart';
import '../widgets/onboarding_progress.dart';
import '../widgets/voice_input_button.dart';

class OnboardingScreen extends ConsumerWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(onboardingControllerProvider);
    final controller = ref.read(onboardingControllerProvider.notifier);
    final networkState = ref.watch(networkStateProvider);
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.onboardingTitle),
        leading: state.currentStep > 0
            ? IconButton(
                icon: const Icon(Icons.arrow_back_rounded),
                onPressed: () => controller.previousStep(),
              )
            : IconButton(
                icon: const Icon(Icons.close_rounded),
                onPressed: () => context.pop(),
              ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Degraded network banner if needed
            DegradedNetworkBanner(networkState: networkState),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const SizedBox(height: AppSpacing.md),

                    // Progress indicator
                    OnboardingProgress(
                      currentStep: state.currentStep,
                      totalSteps: 3,
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    // Step specific prompt & interaction
                    _buildStepContent(context, state, controller, strings),

                    const SizedBox(height: AppSpacing.xl),
                  ],
                ),
              ),
            ),

            // Bottom Navigation Actions
            Container(
              padding: const EdgeInsets.all(AppSpacing.lg),
              decoration: const BoxDecoration(
                color: AppColors.surface,
                border: Border(
                  top: BorderSide(color: AppColors.border, width: 1.0),
                ),
              ),
              child: Row(
                children: [
                  if (state.currentStep > 0) ...[
                    Expanded(
                      flex: 1,
                      child: BhoomiSecondaryButton(
                        text: strings.back,
                        onPressed: () => controller.previousStep(),
                      ),
                    ),
                    const SizedBox(width: AppSpacing.md),
                  ],
                  Expanded(
                    flex: 2,
                    child: BhoomiPrimaryButton(
                      text: state.currentStep == 2 ? strings.reviewProfile : strings.nextStep,
                      icon: state.currentStep == 2
                          ? Icons.check_circle_outline
                          : Icons.arrow_forward_rounded,
                      onPressed: state.isCurrentStepValid
                          ? () {
                              if (state.currentStep == 2) {
                                context.push('/confirm-farm');
                              } else {
                                controller.nextStep();
                              }
                            }
                          : null,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStepContent(
    BuildContext context,
    dynamic state,
    OnboardingController controller,
    BhoomiStrings strings,
  ) {
    switch (state.currentStep) {
      case 0:
        return _buildCropStep(state, controller, strings);
      case 1:
        return _buildAreaStep(state, controller, strings);
      case 2:
        return _buildGrowthStageStep(state, controller, strings);
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildCropStep(dynamic state, OnboardingController controller, BhoomiStrings strings) {
    final crops = [
      {'id': 'samba_paddy', 'icon': Icons.grass_rounded},
      {'id': 'kuruvai_paddy', 'icon': Icons.grain_rounded},
      {'id': 'sugarcane', 'icon': Icons.nature_rounded},
      {'id': 'cotton', 'icon': Icons.cloud_outlined},
      {'id': 'banana', 'icon': Icons.park_outlined},
      {'id': 'maize', 'icon': Icons.local_florist_rounded},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          strings.cropStepTitle,
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          strings.cropStepSub,
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        // Voice Input Button
        VoiceInputButton(
          isListening: state.isListening,
          promptText: strings.cropVoicePrompt,
          activeValue: strings.cropName(state.crop),
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        Text(strings.quickSelectOptions, style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...crops.map(
          (c) {
            final cropId = c['id'] as String;
            return Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
              child: FarmFieldOptionCard(
                title: strings.cropName(cropId),
                subtitle: strings.cropSubtitle(cropId),
                icon: c['icon'] as IconData,
                isSelected: state.crop == cropId,
                onTap: () {
                  controller.setCrop(cropId);
                  controller.stopListening();
                },
              ),
            );
          },
        ),
      ],
    );
  }

  Widget _buildAreaStep(dynamic state, OnboardingController controller, BhoomiStrings strings) {
    final areas = [0.5, 1.0, 2.0, 3.5, 5.0, 10.0];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          strings.areaStepTitle,
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          strings.areaStepSub,
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: strings.areaVoicePrompt,
          activeValue: strings.formatAcres(state.areaAcresSelfReported),
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        Text(strings.selectFarmAreaTitle, style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...areas.map(
          (val) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: strings.formatAcres(val),
              subtitle: null,
              icon: Icons.square_foot_rounded,
              isSelected: state.areaAcresSelfReported == val,
              onTap: () {
                controller.setAreaAcres(val);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildGrowthStageStep(dynamic state, OnboardingController controller, BhoomiStrings strings) {
    final stages = [
      {'id': 'vegetative', 'icon': Icons.spa_rounded},
      {'id': 'flowering', 'icon': Icons.filter_vintage_rounded},
      {'id': 'grain_filling', 'icon': Icons.grain_rounded},
      {'id': 'maturity', 'icon': Icons.wb_sunny_rounded},
      {'id': 'harvest_ready', 'icon': Icons.content_cut_rounded},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          strings.growthStepTitle,
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          strings.growthStepSub,
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: strings.growthVoicePrompt,
          activeValue: strings.stageName(state.growthStage),
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        Text(strings.selectGrowthStageTitle, style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...stages.map(
          (s) {
            final stageId = s['id'] as String;
            return Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
              child: FarmFieldOptionCard(
                title: strings.stageName(stageId),
                subtitle: strings.stageSubtitle(stageId),
                icon: s['icon'] as IconData,
                isSelected: state.growthStage == stageId,
                onTap: () {
                  controller.setGrowthStage(stageId);
                  controller.stopListening();
                },
              ),
            );
          },
        ),
      ],
    );
  }
}
