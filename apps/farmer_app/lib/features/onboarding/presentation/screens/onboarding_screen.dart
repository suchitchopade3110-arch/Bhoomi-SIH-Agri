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
import '../../application/onboarding_state.dart';
import '../../../voice/application/voice_controller.dart';
import '../../../voice/presentation/widgets/voice_confirmation_sheet.dart';
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
    final voiceState = ref.watch(voiceControllerProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.onboardingTitle),
        leading: state.currentStep > 0
            ? IconButton(
                icon: const Icon(Icons.arrow_back_rounded),
                onPressed: () {
                  controller.stopListening();
                  controller.previousStep();
                },
              )
            : IconButton(
                icon: const Icon(Icons.close_rounded),
                onPressed: () {
                  controller.stopListening();
                  if (context.canPop()) {
                    context.pop();
                  } else {
                    context.go('/welcome');
                  }
                },
              ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Degraded network banner if needed
            DegradedNetworkBanner(networkState: networkState),

            // Visible voice error banner if any
            if (voiceState.errorMessage != null)
              Container(
                margin: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.xs),
                padding: const EdgeInsets.all(AppSpacing.sm),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFEBEE),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                  border: Border.all(color: const Color(0xFFFFCDD2)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.mic_off_rounded, color: Color(0xFFC62828), size: 18.0),
                    const SizedBox(width: AppSpacing.xs),
                    Expanded(
                      child: Text(
                        voiceState.errorMessage!,
                        style: const TextStyle(color: Color(0xFFC62828), fontSize: 12.0, fontWeight: FontWeight.w600),
                      ),
                    ),
                  ],
                ),
              ),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const SizedBox(height: AppSpacing.md),

                    // Progress indicator (3 steps: Crop, Growth Stage, Region)
                    OnboardingProgress(
                      currentStep: state.currentStep,
                      totalSteps: 3,
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    // Step specific prompt & interaction
                    _buildStepContent(context, ref, state, controller, strings),

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
                        onPressed: () {
                          controller.stopListening();
                          controller.previousStep();
                        },
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
                              controller.stopListening();
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
    WidgetRef ref,
    OnboardingState state,
    OnboardingController controller,
    BhoomiStrings strings,
  ) {
    switch (state.currentStep) {
      case 0:
        return _buildCropStep(context, ref, state, controller, strings);
      case 1:
        return _buildGrowthStageStep(context, ref, state, controller, strings);
      case 2:
        return _buildRegionStep(context, ref, state, controller, strings);
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildCropStep(
    BuildContext context,
    WidgetRef ref,
    OnboardingState state,
    OnboardingController controller,
    BhoomiStrings strings,
  ) {
    final crops = [
      {'id': 'samba_paddy', 'icon': Icons.grass_rounded},
      {'id': 'kuruvai_paddy', 'icon': Icons.grain_rounded},
      {'id': 'sugarcane', 'icon': Icons.nature_rounded},
      {'id': 'cotton', 'icon': Icons.cloud_outlined},
      {'id': 'banana', 'icon': Icons.park_outlined},
      {'id': 'maize', 'icon': Icons.local_florist_rounded},
    ];

    final isRecordingThisField = state.isFieldRecording('crop');

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          strings.letsGetToKnow,
          style: const TextStyle(
            fontSize: 22.0,
            fontWeight: FontWeight.w800,
            color: AppColors.textPrimary,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 4.0),
        Text(
          strings.youCanSpeak,
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.md),

        // Concentric Voice Button for Crop
        VoiceInputButton(
          isListening: isRecordingThisField,
          promptText: isRecordingThisField ? 'Listening for crop...' : strings.cropVoicePrompt,
          activeValue: strings.cropName(state.crop),
          onTap: () => _handleVoiceInput(
            context: context,
            ref: ref,
            field: 'crop',
            strings: strings,
          ),
        ),

        const SizedBox(height: AppSpacing.sm),
        Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 6.0),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
              border: Border.all(color: AppColors.border),
            ),
            child: const Text(
              'Example: "I have a samba paddy field" / "சம்பா நெல்"',
              style: TextStyle(
                fontSize: 12.0,
                color: AppColors.textMuted,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ),

        const SizedBox(height: AppSpacing.lg),
        Text(strings.quickSelectOptions, style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w700)),
        const SizedBox(height: AppSpacing.sm),

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

  Widget _buildGrowthStageStep(
    BuildContext context,
    WidgetRef ref,
    OnboardingState state,
    OnboardingController controller,
    BhoomiStrings strings,
  ) {
    final stages = [
      {'id': 'vegetative', 'icon': Icons.spa_rounded},
      {'id': 'flowering', 'icon': Icons.filter_vintage_rounded},
      {'id': 'grain_filling', 'icon': Icons.grain_rounded},
      {'id': 'maturity', 'icon': Icons.wb_sunny_rounded},
      {'id': 'harvest_ready', 'icon': Icons.content_cut_rounded},
    ];

    final isRecordingThisField = state.isFieldRecording('growth_stage');

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          strings.growthStepTitle,
          style: const TextStyle(
            fontSize: 22.0,
            fontWeight: FontWeight.w800,
            color: AppColors.textPrimary,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 4.0),
        Text(
          strings.growthStepSub,
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.md),

        VoiceInputButton(
          isListening: isRecordingThisField,
          promptText: isRecordingThisField ? 'Listening for stage...' : strings.growthVoicePrompt,
          activeValue: strings.stageName(state.growthStage),
          onTap: () => _handleVoiceInput(
            context: context,
            ref: ref,
            field: 'growth_stage',
            strings: strings,
          ),
        ),

        const SizedBox(height: AppSpacing.sm),
        Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 6.0),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
              border: Border.all(color: AppColors.border),
            ),
            child: const Text(
              'Example: "Flowering stage" / "பூக்கும் நிலை"',
              style: TextStyle(
                fontSize: 12.0,
                color: AppColors.textMuted,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ),

        const SizedBox(height: AppSpacing.lg),
        Text(strings.selectGrowthStageTitle, style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w700)),
        const SizedBox(height: AppSpacing.sm),

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

  Widget _buildRegionStep(
    BuildContext context,
    WidgetRef ref,
    OnboardingState state,
    OnboardingController controller,
    BhoomiStrings strings,
  ) {
    final regions = [
      {'id': 'Cauvery Delta', 'icon': Icons.water_rounded},
      {'id': 'Western Zone', 'icon': Icons.terrain_rounded},
      {'id': 'Southern Zone', 'icon': Icons.wb_sunny_rounded},
      {'id': 'North Eastern Zone', 'icon': Icons.landscape_rounded},
      {'id': 'High Rainfall Zone', 'icon': Icons.beach_access_rounded},
      {'id': 'North Western Zone', 'icon': Icons.agriculture_rounded},
    ];

    final isRecordingThisField = state.isFieldRecording('region');

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          strings.regionStepTitle,
          style: const TextStyle(
            fontSize: 22.0,
            fontWeight: FontWeight.w800,
            color: AppColors.textPrimary,
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 4.0),
        Text(
          strings.regionStepSub,
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.md),

        VoiceInputButton(
          isListening: isRecordingThisField,
          promptText: isRecordingThisField ? 'Listening for region...' : strings.regionVoicePrompt,
          activeValue: strings.regionName(state.region),
          onTap: () => _handleVoiceInput(
            context: context,
            ref: ref,
            field: 'region',
            strings: strings,
          ),
        ),

        const SizedBox(height: AppSpacing.sm),
        Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 6.0),
            decoration: BoxDecoration(
              color: AppColors.surface,
              borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
              border: Border.all(color: AppColors.border),
            ),
            child: const Text(
              'Example: "Cauvery Delta" / "காவிரி டெல்டா தஞ்சாவூர்"',
              style: TextStyle(
                fontSize: 12.0,
                color: AppColors.textMuted,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ),

        const SizedBox(height: AppSpacing.lg),
        Text(strings.selectRegionTitle, style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w700)),
        const SizedBox(height: AppSpacing.sm),

        ...regions.map(
          (r) {
            final regionId = r['id'] as String;
            return Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
              child: FarmFieldOptionCard(
                title: strings.regionName(regionId),
                subtitle: strings.regionSubtitle(regionId),
                icon: r['icon'] as IconData,
                isSelected: state.region == regionId,
                onTap: () {
                  controller.setRegion(regionId);
                  controller.stopListening();
                },
              ),
            );
          },
        ),
      ],
    );
  }

  Future<void> _handleVoiceInput({
    required BuildContext context,
    required WidgetRef ref,
    required String field,
    required BhoomiStrings strings,
  }) async {
    final onboardingState = ref.read(onboardingControllerProvider);
    final onboardingController = ref.read(onboardingControllerProvider.notifier);
    final voiceController = ref.read(voiceControllerProvider.notifier);
    final userLang = ref.read(languageProvider);

    if (onboardingState.isFieldRecording(field)) {
      onboardingController.stopListening();
      final transcription = await voiceController.stopAndProcessAudio(lang: userLang);
      final currentVoiceState = ref.read(voiceControllerProvider);

      if (currentVoiceState.errorMessage != null && context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(currentVoiceState.errorMessage!),
            backgroundColor: const Color(0xFFC62828),
            behavior: SnackBarBehavior.floating,
          ),
        );
        return;
      }

      if (transcription == null) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('No speech detected. Please tap and speak again or select an option below.'),
              behavior: SnackBarBehavior.floating,
            ),
          );
        }
        return;
      }

      // Map parsed intent or match transcript to field
      String? matchedValue;
      final parsed = transcription.parsedIntent;
      if (parsed != null && (parsed.field == field || parsed.intent == field || parsed.entity == field)) {
        matchedValue = parsed.value?.toString();
      }

      if (matchedValue == null) {
        if (field == 'crop') {
          matchedValue = _matchCrop(transcription.text);
        } else if (field == 'growth_stage') {
          matchedValue = _matchGrowthStage(transcription.text);
        } else if (field == 'region') {
          matchedValue = _matchRegion(transcription.text);
        }
      }

      if (matchedValue != null && context.mounted) {
        if (transcription.needsConfirmation || transcription.readbackText != null) {
          final readbackText = transcription.readbackText ??
              (field == 'crop'
                  ? 'Selected crop ${strings.cropName(matchedValue)}, is that correct?'
                  : field == 'growth_stage'
                      ? 'Selected stage ${strings.stageName(matchedValue)}, is that correct?'
                      : 'Selected region ${strings.regionName(matchedValue)}, is that correct?');

          // Speak readback using Sarvam TTS if active
          voiceController.synthesizeAndSpeak(readbackText, lang: userLang);

          final confirmed = await showModalBottomSheet<bool>(
            context: context,
            isScrollControlled: true,
            backgroundColor: Colors.transparent,
            builder: (ctx) => VoiceConfirmationSheet(
              transcription: transcription,
              onConfirm: () {
                ref.read(voiceControllerProvider.notifier).confirmVoiceField(
                  field: field,
                  confirmedValue: matchedValue,
                  isConfirmed: true,
                );
                Navigator.of(ctx).pop(true);
              },
              onCancel: () {
                ref.read(voiceControllerProvider.notifier).confirmVoiceField(
                  field: field,
                  confirmedValue: matchedValue,
                  isConfirmed: false,
                );
                Navigator.of(ctx).pop(false);
              },
            ),
          );

          if (confirmed == true && context.mounted) {
            _commitFieldValue(onboardingController, field, matchedValue);
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  field == 'crop'
                      ? 'Crop set to ${strings.cropName(matchedValue)}'
                      : field == 'growth_stage'
                          ? 'Stage set to ${strings.stageName(matchedValue)}'
                          : 'Region set to ${strings.regionName(matchedValue)}',
                ),
                backgroundColor: AppColors.primaryDeepGreen,
                behavior: SnackBarBehavior.floating,
              ),
            );
          }
        } else {
          _commitFieldValue(onboardingController, field, matchedValue);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                field == 'crop'
                    ? 'Crop set to ${strings.cropName(matchedValue)}'
                    : field == 'growth_stage'
                        ? 'Stage set to ${strings.stageName(matchedValue)}'
                        : 'Region set to ${strings.regionName(matchedValue)}',
              ),
              backgroundColor: AppColors.primaryDeepGreen,
              behavior: SnackBarBehavior.floating,
            ),
          );
        }
      } else if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Heard: "${transcription.text}". Please select an option below.'),
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    } else {
      onboardingController.startListening(field);
      await voiceController.startRecording();
      final currentVoiceState = ref.read(voiceControllerProvider);
      if (currentVoiceState.errorMessage != null && context.mounted) {
        onboardingController.stopListening();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(currentVoiceState.errorMessage!),
            backgroundColor: const Color(0xFFC62828),
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }

  void _commitFieldValue(OnboardingController controller, String field, String value) {
    if (field == 'crop') {
      controller.setCrop(value);
    } else if (field == 'growth_stage') {
      controller.setGrowthStage(value);
    } else if (field == 'region') {
      controller.setRegion(value);
    }
  }

  String? _matchCrop(String text) {
    final lower = text.toLowerCase();
    if (lower.contains('samba') || lower.contains('சம்பா')) return 'samba_paddy';
    if (lower.contains('kuruvai') || lower.contains('குறுவை')) return 'kuruvai_paddy';
    if (lower.contains('sugar') || lower.contains('கரும்பு')) return 'sugarcane';
    if (lower.contains('cotton') || lower.contains('பருத்தி')) return 'cotton';
    if (lower.contains('banana') || lower.contains('வாழை')) return 'banana';
    if (lower.contains('maize') || lower.contains('corn') || lower.contains('மக்காச்சோளம்')) return 'maize';
    if (lower.contains('paddy') || lower.contains('rice') || lower.contains('நெல்')) return 'samba_paddy';
    return null;
  }

  String? _matchGrowthStage(String text) {
    final lower = text.toLowerCase();
    if (lower.contains('vegetative') || lower.contains('வளர்ச்சி') || lower.contains('leaf') || lower.contains('stem')) return 'vegetative';
    if (lower.contains('flower') || lower.contains('பூக்கும்') || lower.contains('bloom')) return 'flowering';
    if (lower.contains('grain') || lower.contains('தானியம்') || lower.contains('filling') || lower.contains('milk')) return 'grain_filling';
    if (lower.contains('matur') || lower.contains('முதிர்ச்சி') || lower.contains('ripen') || lower.contains('golden')) return 'maturity';
    if (lower.contains('harvest') || lower.contains('அறுவடை') || lower.contains('ready') || lower.contains('cut')) return 'harvest_ready';
    return null;
  }

  String? _matchRegion(String text) {
    final lower = text.toLowerCase();
    if (lower.contains('delta') || lower.contains('cauvery') || lower.contains('டெல்டா') || lower.contains('காவிரி') || lower.contains('thanjavur')) return 'Cauvery Delta';
    if (lower.contains('west') || lower.contains('மேற்கு') || lower.contains('coimbatore') || lower.contains('erode') || lower.contains('tirupur')) return 'Western Zone';
    if (lower.contains('south') || lower.contains('தெற்கு') || lower.contains('madurai') || lower.contains('theni') || lower.contains('dindigul')) return 'Southern Zone';
    if (lower.contains('north east') || lower.contains('வடகிழக்கு') || lower.contains('kanchipuram') || lower.contains('cuddalore')) return 'North Eastern Zone';
    if (lower.contains('rain') || lower.contains('மழை') || lower.contains('kanyakumari') || lower.contains('nilgiris')) return 'High Rainfall Zone';
    if (lower.contains('north west') || lower.contains('salem') || lower.contains('சேலம்') || lower.contains('dharmapuri') || lower.contains('krishnagiri') || lower.contains('namakkal')) return 'North Western Zone';
    return null;
  }
}
