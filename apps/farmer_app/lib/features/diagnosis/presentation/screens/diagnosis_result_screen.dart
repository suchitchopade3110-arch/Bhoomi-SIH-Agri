import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../../../voice/application/voice_controller.dart';
import '../../application/diagnosis_controller.dart';
import '../widgets/advisory_action_card.dart';
import '../widgets/advisory_sources_section.dart';
import '../widgets/diagnosis_confidence_card.dart';
import '../widgets/related_resources_section.dart';
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

    // STRICT CONFIDENCE GATE HANDLING: If below gate, render clean fallback UI
    if (!response.aboveGate) {
      return Scaffold(
        backgroundColor: AppColors.background,
        appBar: AppBar(
          title: const Text('Review Required'),
          scrolledUnderElevation: 0,
        ),
        body: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Container(
                  padding: const EdgeInsets.all(AppSpacing.xl),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusXl),
                    border: Border.all(color: const Color(0xFFFFCDD2)),
                    boxShadow: const [
                      BoxShadow(
                        color: AppColors.cardShadow,
                        blurRadius: 10.0,
                        offset: Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFFEBEE),
                          shape: BoxShape.circle,
                          border: Border.all(color: const Color(0xFFC62828).withValues(alpha: 0.2)),
                        ),
                        child: const Icon(
                          Icons.support_agent_rounded,
                          color: Color(0xFFC62828),
                          size: 40.0,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      const Text(
                        'Expert Verification Required',
                        style: TextStyle(
                          fontSize: 20.0,
                          fontWeight: FontWeight.w800,
                          color: Color(0xFFC62828),
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      const Text(
                        'The diagnosis confidence is below the safety threshold. To ensure safe and accurate guidance, this case has been prepared for expert review.',
                        style: TextStyle(fontSize: 13.5, color: AppColors.textSecondary, height: 1.4),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.sm),
                        decoration: BoxDecoration(
                          color: AppColors.background,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                        ),
                        child: Text(
                          'Diagnosis ID: ${response.diagnosisId}',
                          style: const TextStyle(fontSize: 11.0, fontFamily: 'monospace', color: AppColors.textMuted),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                BhoomiPrimaryButton(
                  text: 'Escalate to KVK Agronomist',
                  icon: Icons.send_rounded,
                  onPressed: () {
                    context.push('/escalation/$farmId/${response.diagnosisId}');
                  },
                ),
                const SizedBox(height: AppSpacing.md),
                BhoomiSecondaryButton(
                  text: 'Return to Farm Home',
                  icon: Icons.home_rounded,
                  onPressed: () {
                    context.go('/home/$farmId');
                  },
                ),
              ],
            ),
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
        title: const Text("BHOOMI's Advisory", style: TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
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
                          decoration: const BoxDecoration(
                            color: AppColors.lightGreen,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.eco_rounded, color: AppColors.primaryGreen, size: 22.0),
                        ),
                        const SizedBox(width: AppSpacing.sm),
                        const Text(
                          'Possible Issue Identified',
                          style: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w700, color: AppColors.textSecondary),
                        ),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                      response.possibleIssue,
                      style: const TextStyle(
                        fontSize: 22.0,
                        fontWeight: FontWeight.w900,
                        color: AppColors.textPrimary,
                        letterSpacing: -0.3,
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
              if (response.symptomsToCheck.isNotEmpty) ...[
                SymptomsChecklistWidget(symptoms: response.symptomsToCheck),
                const SizedBox(height: AppSpacing.lg),
              ],

              // 5-Point Action Plan Card with Save/Share
              AdvisoryActionCard(
                actions: response.actions,
                caution: response.caution,
              ),

              const SizedBox(height: AppSpacing.lg),

              // Related Resources (Articles, Videos, Documents)
              const RelatedResourcesSection(cropName: 'Paddy'),

              const SizedBox(height: AppSpacing.lg),

              // Information Sources (ICAR / FAO Citations)
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

              const SizedBox(height: AppSpacing.xl),
            ],
          ),
        ),
      ),
    );
  }
}
