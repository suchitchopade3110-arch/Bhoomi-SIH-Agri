import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/connectivity/connectivity_service.dart';
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

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Tell us about your farm'),
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
                      totalSteps: 6,
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    // Step specific prompt & interaction
                    _buildStepContent(context, state, controller),

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
                        text: 'Back',
                        onPressed: () => controller.previousStep(),
                      ),
                    ),
                    const SizedBox(width: AppSpacing.md),
                  ],
                  Expanded(
                    flex: 2,
                    child: BhoomiPrimaryButton(
                      text: state.currentStep == 5 ? 'Review Profile' : 'Next Step',
                      icon: state.currentStep == 5
                          ? Icons.check_circle_outline
                          : Icons.arrow_forward_rounded,
                      onPressed: state.isCurrentStepValid
                          ? () {
                              if (state.currentStep == 5) {
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
  ) {
    switch (state.currentStep) {
      case 0:
        return _buildCropStep(state, controller);
      case 1:
        return _buildAreaStep(state, controller);
      case 2:
        return _buildGrowthStageStep(state, controller);
      case 3:
        return _buildSoilTypeStep(state, controller);
      case 4:
        return _buildIrrigationStep(state, controller);
      case 5:
        return _buildSeasonStep(state, controller);
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildCropStep(dynamic state, OnboardingController controller) {
    final crops = [
      {'id': 'samba_paddy', 'title': 'Samba Paddy', 'sub': 'Traditional long-duration rice', 'icon': Icons.grass_rounded},
      {'id': 'kuruvai_paddy', 'title': 'Kuruvai Paddy', 'sub': 'Short-duration summer crop', 'icon': Icons.grain_rounded},
      {'id': 'sugarcane', 'title': 'Sugarcane', 'sub': 'Commercial perennial crop', 'icon': Icons.nature_rounded},
      {'id': 'cotton', 'title': 'Cotton', 'sub': 'Cash fiber crop', 'icon': Icons.cloud_outlined},
      {'id': 'banana', 'title': 'Banana', 'sub': 'Fruit plantation', 'icon': Icons.park_outlined},
      {'id': 'maize', 'title': 'Maize (Corn)', 'sub': 'Nutrient-rich grain', 'icon': Icons.local_florist_rounded},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'What crop are you growing?',
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          'Speak clearly or select your crop from the list below',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        // Voice Input Button
        VoiceInputButton(
          isListening: state.isListening,
          promptText: 'Tap to speak your crop',
          activeValue: crops.firstWhere(
            (c) => c['id'] == state.crop,
            orElse: () => {'title': state.crop},
          )['title'] as String?,
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        const Text('Quick Selection Options', style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...crops.map(
          (c) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: c['title'] as String,
              subtitle: c['sub'] as String,
              icon: c['icon'] as IconData,
              isSelected: state.crop == c['id'],
              onTap: () {
                controller.setCrop(c['id'] as String);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAreaStep(dynamic state, OnboardingController controller) {
    final areas = [
      {'val': 0.5, 'label': '0.5 Acres', 'sub': 'Small homestead plot'},
      {'val': 1.0, 'label': '1.0 Acre', 'sub': 'Standard 1 acre parcel'},
      {'val': 2.0, 'label': '2.0 Acres', 'sub': 'Self-reported field (Standard)'},
      {'val': 3.5, 'label': '3.5 Acres', 'sub': 'Medium farm holdings'},
      {'val': 5.0, 'label': '5.0 Acres', 'sub': 'Large cultivation block'},
      {'val': 10.0, 'label': '10.0 Acres', 'sub': 'Commercial scale farm'},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'How much land are you farming?',
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          'Self-reported area in acres for official verification',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: 'Tap to speak your farm size',
          activeValue: '${state.areaAcresSelfReported} Acres',
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        const Text('Select Farm Area (Acres)', style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...areas.map(
          (a) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: a['label'] as String,
              subtitle: a['sub'] as String,
              icon: Icons.square_foot_rounded,
              isSelected: state.areaAcresSelfReported == (a['val'] as double),
              onTap: () {
                controller.setAreaAcres(a['val'] as double);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildGrowthStageStep(dynamic state, OnboardingController controller) {
    final stages = [
      {'id': 'vegetative', 'title': 'Vegetative', 'sub': 'Leaf & stem rapid growth stage', 'icon': Icons.spa_rounded},
      {'id': 'flowering', 'title': 'Flowering', 'sub': 'Bloom and pollination active', 'icon': Icons.filter_vintage_rounded},
      {'id': 'grain_filling', 'title': 'Grain Filling', 'sub': 'Panicle & grain development', 'icon': Icons.grain_rounded},
      {'id': 'maturity', 'title': 'Maturity', 'sub': 'Crop turning golden / ripening', 'icon': Icons.wb_sunny_rounded},
      {'id': 'harvest_ready', 'title': 'Harvest Ready', 'sub': 'Ready for cutting and yield collection', 'icon': Icons.content_cut_rounded},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'What stage is your crop in?',
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          'Helps track growth phase and land readiness',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: 'Tap to speak current stage',
          activeValue: stages.firstWhere(
            (s) => s['id'] == state.growthStage,
            orElse: () => {'title': state.growthStage},
          )['title'] as String?,
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        const Text('Select Current Stage', style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...stages.map(
          (s) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: s['title'] as String,
              subtitle: s['sub'] as String,
              icon: s['icon'] as IconData,
              isSelected: state.growthStage == s['id'],
              onTap: () {
                controller.setGrowthStage(s['id'] as String);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSoilTypeStep(dynamic state, OnboardingController controller) {
    final soils = [
      {'id': 'clay_loam', 'title': 'Clay Loam', 'sub': 'High moisture retention, nutrient dense', 'icon': Icons.terrain_rounded},
      {'id': 'alluvial', 'title': 'Alluvial Soil', 'sub': 'Fertile river basin soil', 'icon': Icons.waves_rounded},
      {'id': 'red_soil', 'title': 'Red Soil', 'sub': 'Rich in iron oxide, porous', 'icon': Icons.circle_rounded},
      {'id': 'black_soil', 'title': 'Black Soil', 'sub': 'Regur soil, ideal for cotton & pulses', 'icon': Icons.brightness_1_rounded},
      {'id': 'sandy_loam', 'title': 'Sandy Loam', 'sub': 'Well-drained light soil', 'icon': Icons.grain_outlined},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'What is your soil type?',
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          'Select your predominant farm soil composition',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: 'Tap to speak soil type',
          activeValue: soils.firstWhere(
            (s) => s['id'] == state.soilType,
            orElse: () => {'title': state.soilType},
          )['title'] as String?,
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        const Text('Select Soil Type', style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...soils.map(
          (s) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: s['title'] as String,
              subtitle: s['sub'] as String,
              icon: s['icon'] as IconData,
              isSelected: state.soilType == s['id'],
              onTap: () {
                controller.setSoilType(s['id'] as String);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildIrrigationStep(dynamic state, OnboardingController controller) {
    final irrigations = [
      {'id': 'canal', 'title': 'Canal Irrigation', 'sub': 'Direct river / public canal water', 'icon': Icons.water_rounded},
      {'id': 'borewell', 'title': 'Borewell / Tube Well', 'sub': 'Groundwater pump source', 'icon': Icons.offline_bolt_rounded},
      {'id': 'drip', 'title': 'Drip / Micro Irrigation', 'sub': 'Precision pipe delivery system', 'icon': Icons.bubble_chart_rounded},
      {'id': 'rainfed', 'title': 'Rainfed', 'sub': 'Dependent on seasonal monsoon rain', 'icon': Icons.cloud_queue_rounded},
      {'id': 'open_well', 'title': 'Open Dug Well', 'sub': 'Traditional farm open well', 'icon': Icons.radio_button_checked_rounded},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'What is your irrigation access?',
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          'Primary water source powering your field',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: 'Tap to speak irrigation source',
          activeValue: irrigations.firstWhere(
            (i) => i['id'] == state.irrigationAccess,
            orElse: () => {'title': state.irrigationAccess},
          )['title'] as String?,
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        const Text('Select Irrigation Access', style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...irrigations.map(
          (i) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: i['title'] as String,
              subtitle: i['sub'] as String,
              icon: i['icon'] as IconData,
              isSelected: state.irrigationAccess == i['id'],
              onTap: () {
                controller.setIrrigationAccess(i['id'] as String);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSeasonStep(dynamic state, OnboardingController controller) {
    final seasons = [
      {'id': 'samba', 'title': 'Samba Season', 'sub': 'August to January (Main Rabi/Paddy)', 'icon': Icons.calendar_month_rounded},
      {'id': 'kuruvai', 'title': 'Kuruvai Season', 'sub': 'June to September (Kharif/Summer)', 'icon': Icons.wb_sunny_outlined},
      {'id': 'navarai', 'title': 'Navarai Season', 'sub': 'December to April (Late winter/spring)', 'icon': Icons.filter_drama_rounded},
      {'id': 'kharif', 'title': 'Kharif Season', 'sub': 'Monsoon crop season', 'icon': Icons.thunderstorm_outlined},
      {'id': 'rabi', 'title': 'Rabi Season', 'sub': 'Winter cultivation period', 'icon': Icons.ac_unit_rounded},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'What is the current season?',
          style: AppTypography.headlineLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          'The agricultural crop season for this planting',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.lg),

        VoiceInputButton(
          isListening: state.isListening,
          promptText: 'Tap to speak current season',
          activeValue: seasons.firstWhere(
            (s) => s['id'] == state.season,
            orElse: () => {'title': state.season},
          )['title'] as String?,
          onTap: () {
            controller.toggleListening();
          },
        ),

        const SizedBox(height: AppSpacing.xl),
        const Text('Select Season', style: AppTypography.titleMedium),
        const SizedBox(height: AppSpacing.md),

        ...seasons.map(
          (s) => Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.sm),
            child: FarmFieldOptionCard(
              title: s['title'] as String,
              subtitle: s['sub'] as String,
              icon: s['icon'] as IconData,
              isSelected: state.season == s['id'],
              onTap: () {
                controller.setSeason(s['id'] as String);
                controller.stopListening();
              },
            ),
          ),
        ),
      ],
    );
  }
}
