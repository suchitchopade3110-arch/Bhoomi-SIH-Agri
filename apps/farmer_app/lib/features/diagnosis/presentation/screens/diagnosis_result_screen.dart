import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../../../voice/application/voice_controller.dart';
import '../../application/diagnosis_controller.dart';
import '../widgets/advisory_action_card.dart';
import '../widgets/advisory_sources_section.dart';
import '../widgets/diagnosis_confidence_card.dart';
import '../widgets/symptoms_checklist.dart';

class DiagnosisResultScreen extends ConsumerWidget {
  final String farmId;

  const DiagnosisResultScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(diagnosisControllerProvider);
    final voiceState = ref.watch(voiceControllerProvider);
    final voiceController = ref.read(voiceControllerProvider.notifier);
    final response = state.diagnosisResponse;

    if (response == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Diagnosis Result')),
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('No diagnosis result available.'),
              const SizedBox(height: AppSpacing.md),
              BhoomiPrimaryButton(
                text: 'Ask BHOOMI',
                onPressed: () => context.go('/ask/$farmId'),
              ),
            ],
          ),
        ),
      );
    }

    final speechSummary = (response.spokenSummary != null && response.spokenSummary!.trim().isNotEmpty)
        ? response.spokenSummary!
        : "Possible Issue: ${response.possibleIssue}. Key actions: ${response.actions.join(', ')}.";

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("BHOOMI's Advisory"),
        actions: [
          IconButton(
            icon: Icon(
              voiceState.isPlaying ? Icons.stop_circle_rounded : Icons.volume_up_rounded,
              color: AppColors.primaryGreen,
              size: 26.0,
            ),
            tooltip: voiceState.isPlaying ? 'Stop Audio' : 'Listen to Advisory',
            onPressed: () {
              if (voiceState.isPlaying) {
                voiceController.stopPlayback();
              } else {
                voiceController.synthesizeAndSpeak(speechSummary);
              }
            },
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Card: Possible Issue
              BhoomiCard(
                padding: const EdgeInsets.all(AppSpacing.lg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.sm),
                          decoration: BoxDecoration(
                            color: AppColors.primaryGreen.withValues(alpha: 0.12),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.eco_rounded, color: AppColors.primaryGreen, size: 22.0),
                        ),
                        const SizedBox(width: AppSpacing.sm),
                        const Text('Possible Issue Identified', style: AppTypography.titleLarge),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                      response.possibleIssue,
                      style: AppTypography.headlineLarge.copyWith(
                        fontWeight: FontWeight.w800,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    Text(
                      'Diagnosis ID: ${response.diagnosisId}',
                      style: const TextStyle(fontSize: 11.0, fontFamily: 'monospace', color: AppColors.textMuted),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Confidence / Uncertainty Card
              DiagnosisConfidenceCard(response: response),

              const SizedBox(height: AppSpacing.lg),

              // Symptoms to Check Checklist
              SymptomsChecklistWidget(symptoms: response.symptomsToCheck),

              const SizedBox(height: AppSpacing.lg),

              // What you can do Actions Card
              AdvisoryActionCard(
                actions: response.actions,
                caution: response.caution,
              ),

              const SizedBox(height: AppSpacing.lg),

              // Information Sources
              AdvisorySourcesSection(sources: response.sources),

              const SizedBox(height: AppSpacing.xl),

              // Action Buttons: Follow-up & Expert Help
              Row(
                children: [
                  Expanded(
                    child: BhoomiSecondaryButton(
                      text: 'Track Progress',
                      icon: Icons.assignment_turned_in_outlined,
                      onPressed: () {
                        context.push('/followup/$farmId/${response.diagnosisId}');
                      },
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: BhoomiPrimaryButton(
                      text: 'Get Expert Help',
                      icon: Icons.support_agent_rounded,
                      onPressed: () {
                        context.push('/escalation/$farmId/${response.diagnosisId}');
                      },
                    ),
                  ),
                ],
              ),

              const SizedBox(height: AppSpacing.md),
            ],
          ),
        ),
      ),
    );
  }
}
