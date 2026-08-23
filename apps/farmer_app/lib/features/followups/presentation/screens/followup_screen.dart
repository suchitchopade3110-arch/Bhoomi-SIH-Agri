import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../../application/followup_controller.dart';

class FollowupScreen extends ConsumerStatefulWidget {
  final String farmId;
  final String diagnosisId;

  const FollowupScreen({
    super.key,
    required this.farmId,
    required this.diagnosisId,
  });

  @override
  ConsumerState<FollowupScreen> createState() => _FollowupScreenState();
}

class _FollowupScreenState extends ConsumerState<FollowupScreen> {
  final TextEditingController _notesController = TextEditingController();

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(followupControllerProvider);
    final controller = ref.read(followupControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Track Problem Progress'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (state.response == null) ...[
                // Prompt Card
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Column(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: AppColors.primaryGreen.withValues(alpha: 0.12),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.psychology_alt_rounded, color: AppColors.primaryGreen, size: 28.0),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      const Text(
                        'How is your crop now?',
                        style: AppTypography.headlineMedium,
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        'Reporting your field outcome updates your farm health profile and verifies treatment effectiveness.',
                        style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.lg),

                      // Outcome Options
                      _buildOutcomeOption(
                        title: 'Improved',
                        subtitle: 'Yellowing stopped, new healthy leaves emerging',
                        icon: Icons.thumb_up_alt_rounded,
                        value: 'improved',
                        color: AppColors.primaryGreen,
                        isSelected: state.selectedOutcome == 'improved',
                        onSelect: () => controller.selectOutcome('improved'),
                      ),
                      const SizedBox(height: AppSpacing.sm),

                      _buildOutcomeOption(
                        title: 'No Change',
                        subtitle: 'Symptoms remain visible at the same level',
                        icon: Icons.horizontal_rule_rounded,
                        value: 'no_change',
                        color: const Color(0xFFD97706),
                        isSelected: state.selectedOutcome == 'no_change',
                        onSelect: () => controller.selectOutcome('no_change'),
                      ),
                      const SizedBox(height: AppSpacing.sm),

                      _buildOutcomeOption(
                        title: 'Got Worse',
                        subtitle: 'Lesions expanding or spreading to adjacent tillers',
                        icon: Icons.warning_amber_rounded,
                        value: 'got_worse',
                        color: const Color(0xFFC62828),
                        isSelected: state.selectedOutcome == 'got_worse',
                        onSelect: () => controller.selectOutcome('got_worse'),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Field Observation Notes (Optional)
                BhoomiCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Observation Notes (Optional)', style: AppTypography.titleMedium),
                      const SizedBox(height: AppSpacing.sm),
                      TextField(
                        controller: _notesController,
                        maxLines: 2,
                        onChanged: controller.setNotes,
                        decoration: InputDecoration(
                          hintText: 'e.g. Applied recommended copper bactericide 2 days ago...',
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                // Submit Follow-up Button
                BhoomiPrimaryButton(
                  text: 'Submit Follow-up Status',
                  isLoading: state.isSubmitting,
                  icon: Icons.send_rounded,
                  onPressed: state.selectedOutcome == null
                      ? null
                      : () => controller.submitFollowup(
                            farmId: widget.farmId,
                            diagnosisId: widget.diagnosisId,
                          ),
                ),
              ] else ...[
                // Success / Next Steps Card
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
                            child: const Icon(Icons.check_circle_rounded, color: AppColors.primaryGreen, size: 24.0),
                          ),
                          const SizedBox(width: AppSpacing.sm),
                          const Text('Follow-up Recorded', style: AppTypography.headlineMedium),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.xs),
                        decoration: BoxDecoration(
                          color: AppColors.background,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                        ),
                        child: Text(
                          'Outcome: ${state.response!.outcome.toUpperCase()}',
                          style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 12.0, color: AppColors.primaryGreen),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.lg),
                      const Text('Recommended Next Steps', style: AppTypography.titleLarge),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        state.response!.nextSteps,
                        style: AppTypography.bodyLarge.copyWith(height: 1.4, color: AppColors.textPrimary),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // If outcome got worse or escalation recommended, show Expert Help CTA
                if (state.response!.escalationRecommended || state.response!.outcome == 'got_worse') ...[
                  BhoomiCard(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.support_agent_rounded, color: Color(0xFF9333EA), size: 22.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Expert Review Recommended', style: AppTypography.titleLarge),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.xs),
                        Text(
                          'Since the symptoms have not stabilized, an agricultural officer at KVK can personally review your case.',
                          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                        ),
                        const SizedBox(height: AppSpacing.md),
                        BhoomiPrimaryButton(
                          text: 'Request KVK Expert Review',
                          icon: Icons.arrow_forward_rounded,
                          onPressed: () {
                            context.push('/escalation/${widget.farmId}/${widget.diagnosisId}');
                          },
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                BhoomiSecondaryButton(
                  text: 'Return to Farm Home',
                  icon: Icons.home_rounded,
                  onPressed: () {
                    context.go('/home/${widget.farmId}');
                  },
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildOutcomeOption({
    required String title,
    required String subtitle,
    required IconData icon,
    required String value,
    required Color color,
    required bool isSelected,
    required VoidCallback onSelect,
  }) {
    return InkWell(
      onTap: onSelect,
      borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          color: isSelected ? color.withValues(alpha: 0.08) : AppColors.background,
          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
          border: Border.all(
            color: isSelected ? color : AppColors.border,
            width: isSelected ? 2.0 : 1.0,
          ),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(AppSpacing.sm),
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.12),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: color, size: 20.0),
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.w700,
                      color: isSelected ? color : AppColors.textPrimary,
                    ),
                  ),
                  Text(
                    subtitle,
                    style: const TextStyle(fontSize: 11.0, color: AppColors.textMuted),
                  ),
                ],
              ),
            ),
            if (isSelected)
              Icon(Icons.check_circle, color: color, size: 20.0),
          ],
        ),
      ),
    );
  }
}
