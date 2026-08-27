import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
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
    final strings = ref.watch(bhoomiStringsProvider);
    final state = ref.watch(escalationControllerProvider);
    final controller = ref.read(escalationControllerProvider.notifier);
    final diagnosisState = ref.watch(diagnosisControllerProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('get_expert_help'), style: const TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (state.response == null) ...[
                // Escalating to Expert Card
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.xl),
                  child: Column(
                    children: [
                      // Expert Illustration / Emblem
                      Container(
                        width: 80.0,
                        height: 80.0,
                        decoration: BoxDecoration(
                          color: const Color(0xFFFAF5FF),
                          shape: BoxShape.circle,
                          border: Border.all(color: const Color(0xFFE9D5FF), width: 2.0),
                          boxShadow: const [
                            BoxShadow(
                              color: Color(0x1A9333EA),
                              blurRadius: 14.0,
                              offset: Offset(0, 4),
                            ),
                          ],
                        ),
                        child: const Center(
                          child: Icon(Icons.support_agent_rounded, color: Color(0xFF9333EA), size: 40.0),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Text(
                        strings.text('get_expert_help'),
                        style: const TextStyle(
                          fontSize: 22.0,
                          fontWeight: FontWeight.w900,
                          color: AppColors.textPrimary,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 4.0),
                      Text(
                        strings.expertVerificationRequired,
                        style: const TextStyle(fontSize: 14.0, fontWeight: FontWeight.w600, color: AppColors.primaryGreen),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Text(
                        strings.belowConfidenceGateDesc,
                        style: const TextStyle(fontSize: 13.0, color: AppColors.textSecondary, height: 1.35),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.lg),

                      // Stepper Status Preview
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: AppColors.background,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          border: Border.all(color: AppColors.border),
                        ),
                        child: Column(
                          children: [
                            _EscalationStepRow(label: strings.caseTransferred, isPending: true),
                            const SizedBox(height: AppSpacing.xs),
                            _EscalationStepRow(label: strings.expertNotified, isPending: true),
                            const SizedBox(height: AppSpacing.xs),
                            _EscalationStepRow(label: strings.reviewInProgress, isPending: true),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Reason Input
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        strings.whyNeedExpert,
                        style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      TextField(
                        controller: _reasonController,
                        maxLines: 3,
                        onChanged: controller.setReason,
                        decoration: InputDecoration(
                          hintText: strings.text('type_problem_hint'),
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

                if (state.errorMessage != null) ...[
                  const SizedBox(height: AppSpacing.md),
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: const Color(0xFFFFEBEE),
                      borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                      border: Border.all(color: const Color(0xFFEF9A9A)),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline, color: Color(0xFFC62828), size: 20.0),
                        const SizedBox(width: AppSpacing.sm),
                        Expanded(
                          child: Text(
                            state.errorMessage!,
                            style: const TextStyle(fontSize: 12.5, color: Color(0xFFC62828)),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],

                const SizedBox(height: AppSpacing.xl),

                // Submit Escalation
                BhoomiPrimaryButton(
                  text: strings.submitToKvk,
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
                const SizedBox(height: AppSpacing.md),
              ] else ...[
                // Expert Case Summary Screen
                Container(
                  padding: const EdgeInsets.all(AppSpacing.xl),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusXl),
                    boxShadow: const [
                      BoxShadow(
                        color: AppColors.cardShadow,
                        blurRadius: 10.0,
                        offset: Offset(0, 4),
                      ),
                    ],
                  ),
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
                            child: const Icon(Icons.check_circle_rounded, color: AppColors.primaryGreen, size: 24.0),
                          ),
                          const SizedBox(width: AppSpacing.sm),
                          Expanded(
                            child: Text(
                              strings.expertCaseSummary,
                              style: const TextStyle(fontSize: 20.0, fontWeight: FontWeight.w900, color: AppColors.textPrimary),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.lg),

                      // Live Stepper
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: AppColors.background,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                        ),
                        child: Column(
                          children: [
                            _EscalationStepRow(label: strings.caseTransferred, isPending: false),
                            const SizedBox(height: AppSpacing.xs),
                            _EscalationStepRow(label: strings.expertNotified, isPending: false),
                            const SizedBox(height: AppSpacing.xs),
                            _EscalationStepRow(label: strings.reviewInProgress, isPending: false),
                          ],
                        ),
                      ),

                      const SizedBox(height: AppSpacing.lg),
                      const Divider(color: AppColors.divider),
                      const SizedBox(height: AppSpacing.md),

                      _buildInfoRow(strings.farmer, strings.text('primary_crop')),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow(strings.location, strings.text('village')),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow(strings.cropLabel, strings.cropName('samba_paddy')),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow(strings.caseIdentifier, state.response!.caseId),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow(strings.assignedKvk, state.response!.kvkCenter),
                      const SizedBox(height: AppSpacing.sm),
                      _buildInfoRow(strings.estimatedReview, state.response!.estimatedReview),

                      const SizedBox(height: AppSpacing.lg),
                      const Divider(color: AppColors.divider),
                      const SizedBox(height: AppSpacing.md),

                      Text(
                        strings.summary,
                        style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                      ),
                      const SizedBox(height: 2.0),
                      Text(
                        strings.belowConfidenceGateDesc,
                        style: const TextStyle(fontSize: 13.0, height: 1.35, color: AppColors.textSecondary),
                      ),

                      const SizedBox(height: AppSpacing.md),

                      Text(
                        strings.expertNote,
                        style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: AppColors.primaryGreen),
                      ),
                      const SizedBox(height: 2.0),
                      Text(
                        '${state.response!.kvkCenter} - ${state.response!.estimatedReview}',
                        style: const TextStyle(fontSize: 13.0, height: 1.35, color: AppColors.textSecondary),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                BhoomiPrimaryButton(
                  text: 'View Full Case',
                  icon: Icons.assignment_outlined,
                  onPressed: () {
                    context.go('/home/${widget.farmId}');
                  },
                ),
                const SizedBox(height: AppSpacing.sm),
                BhoomiSecondaryButton(
                  text: 'Share Case PDF Payload',
                  icon: Icons.picture_as_pdf_rounded,
                  onPressed: () => _shareCasePdf(context, ref, state.response!.caseId),
                ),
                const SizedBox(height: AppSpacing.sm),
                BhoomiSecondaryButton(
                  text: 'Return to Farm Home',
                  icon: Icons.home_rounded,
                  onPressed: () {
                    context.go('/home/${widget.farmId}');
                  },
                ),
                const SizedBox(height: AppSpacing.md),
              ],
            ],
          ),
        ),
      ),
    );
  }

  void _shareCasePdf(BuildContext context, WidgetRef ref, String caseId) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(child: CircularProgressIndicator(color: AppColors.primaryGreen)),
    );

    try {
      final payload = await ref.read(casePdfPayloadProvider(caseId).future);
      if (context.mounted) {
        Navigator.pop(context); // Dismiss loading indicator
        
        showDialog(
          context: context,
          builder: (context) {
            return AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusLg)),
              title: const Row(
                children: [
                  Icon(Icons.picture_as_pdf_rounded, color: Color(0xFFC62828)),
                  SizedBox(width: AppSpacing.sm),
                  Text('Case PDF Details', style: TextStyle(fontWeight: FontWeight.w800)),
                ],
              ),
              content: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text('Below is the structured agronomist case summary payload:', style: TextStyle(fontSize: 12.0, color: AppColors.textSecondary)),
                    const SizedBox(height: AppSpacing.md),
                    _buildPopupDetailRow('Case Identifier', payload.caseId),
                    _buildPopupDetailRow('Created At', payload.generatedAt),
                    _buildPopupDetailRow('Crop', payload.bundle.crop),
                    _buildPopupDetailRow('Region', payload.bundle.region),
                    _buildPopupDetailRow('Growth Stage', payload.bundle.growthStage),
                    _buildPopupDetailRow('Severity', payload.severity),
                    _buildPopupDetailRow('Summary', payload.summaryHeadline),
                    _buildPopupDetailRow('Recommended', payload.prescribedActionsSummary ?? 'None'),
                    _buildPopupDetailRow('Treatments Tried', payload.bundle.treatmentsTried.join(', ')),
                    const SizedBox(height: AppSpacing.md),
                    const Divider(),
                    const SizedBox(height: AppSpacing.sm),
                    const Text('PDF Share Link:', style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 2.0),
                    SelectableText(
                      payload.shareUrl ?? '',
                      style: const TextStyle(fontSize: 11.5, color: Colors.blue, decoration: TextDecoration.underline),
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Close'),
                ),
              ],
            );
          },
        );
      }
    } catch (e) {
      if (context.mounted) {
        Navigator.pop(context); // Dismiss loading indicator
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load Case PDF: $e')),
        );
      }
    }
  }

  Widget _buildPopupDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.xs),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontSize: 10.0, fontWeight: FontWeight.w700, color: AppColors.textMuted)),
          Text(value, style: const TextStyle(fontSize: 12.0, color: AppColors.textPrimary)),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(fontSize: 12.5, color: AppColors.textMuted)),
        Text(
          value,
          style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
        ),
      ],
    );
  }
}

class _EscalationStepRow extends StatelessWidget {
  final String label;
  final bool isPending;

  const _EscalationStepRow({required this.label, required this.isPending});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          isPending ? Icons.radio_button_unchecked_rounded : Icons.check_circle_rounded,
          size: 16.0,
          color: isPending ? AppColors.textMuted : AppColors.primaryGreen,
        ),
        const SizedBox(width: AppSpacing.sm),
        Text(
          label,
          style: TextStyle(
            fontSize: 12.5,
            fontWeight: isPending ? FontWeight.w500 : FontWeight.w700,
            color: isPending ? AppColors.textMuted : AppColors.textPrimary,
          ),
        ),
      ],
    );
  }
}
