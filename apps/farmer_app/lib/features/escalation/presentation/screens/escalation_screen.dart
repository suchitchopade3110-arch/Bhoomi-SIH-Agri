import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../diagnosis/application/diagnosis_controller.dart';
import '../../application/escalation_controller.dart';

class EscalationScreen extends ConsumerStatefulWidget {
  final String farmId;
  final String diagnosisId;

  const EscalationScreen({
    super.key,
    required this.farmId,
    required this.diagnosisId,
  });

  @override
  ConsumerState<EscalationScreen> createState() => _EscalationScreenState();
}

class _EscalationScreenState extends ConsumerState<EscalationScreen> {
  final TextEditingController _reasonController = TextEditingController();

  @override
  void dispose() {
    _reasonController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(escalationControllerProvider);
    final controller = ref.read(escalationControllerProvider.notifier);
    final diagnosisState = ref.watch(diagnosisControllerProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('KVK Expert Review'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (state.response == null) ...[
                // Info Card
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Column(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: const Color(0xFF9333EA).withValues(alpha: 0.12),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.support_agent_rounded, color: Color(0xFF9333EA), size: 32.0),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      const Text(
                        'Expert Verification Recommended',
                        style: AppTypography.headlineMedium,
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        'This issue may need agricultural review by Krishi Vigyan Kendra (KVK) agronomists. Your farm context, diagnosis history, and crop photo will be forwarded.',
                        style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Reason Input
                BhoomiCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Why do you need expert help? (Optional)', style: AppTypography.titleMedium),
                      const SizedBox(height: AppSpacing.sm),
                      TextField(
                        controller: _reasonController,
                        maxLines: 3,
                        onChanged: controller.setReason,
                        decoration: InputDecoration(
                          hintText: 'e.g. Yellowing is spreading rapidly to 50% of tillers despite initial drainage...',
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

                // Submit Escalation
                BhoomiPrimaryButton(
                  text: 'Submit to KVK Agronomist',
                  isLoading: state.isSubmitting,
                  icon: Icons.send_rounded,
                  onPressed: () async {
                    controller.setReason(_reasonController.text);
                    await controller.submitEscalation(
                      farmId: widget.farmId,
                      diagnosisId: widget.diagnosisId,
                      imageAssetId: diagnosisState.imageAssetId,
                    );
                  },
                ),
              ] else ...[
                // Escalation Submitted Confirmation
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
                          const Text('Expert Request Submitted', style: AppTypography.headlineMedium),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.md),
                      _buildInfoRow('Case Identifier', state.response!.caseId),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow('Assigned KVK Center', state.response!.kvkCenter),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow('Estimated Review', state.response!.estimatedReview),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow(
                        'Submitted At',
                        state.response!.submissionTimestamp.length >= 10
                            ? state.response!.submissionTimestamp.substring(0, 10)
                            : state.response!.submissionTimestamp,
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                BhoomiPrimaryButton(
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

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(fontSize: 12.0, color: AppColors.textMuted)),
        Text(value, style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
      ],
    );
  }
}
