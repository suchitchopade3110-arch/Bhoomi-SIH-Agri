import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
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
  XFile? _selectedImage;
  final ImagePicker _picker = ImagePicker();

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(source: source, imageQuality: 85);
      if (picked != null) {
        setState(() {
          _selectedImage = picked;
        });
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final strings = ref.watch(bhoomiStringsProvider);
    final state = ref.watch(followupControllerProvider);
    final controller = ref.read(followupControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.trackProgress, style: const TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (state.response == null) ...[
                // Prompt Card: How is it now?
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Column(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: const BoxDecoration(
                          color: AppColors.lightGreen,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.psychology_alt_rounded, color: AppColors.primaryGreen, size: 30.0),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Text(
                        strings.howIsItNow,
                        style: const TextStyle(
                          fontSize: 22.0,
                          fontWeight: FontWeight.w900,
                          color: AppColors.textPrimary,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 4.0),
                      Text(
                        strings.followupQuestion,
                        style: const TextStyle(fontSize: 13.5, color: AppColors.textSecondary, height: 1.35),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.lg),

                      // Outcome Options: Improved, No Change, Got Worse
                      _buildOutcomeOption(
                        title: '✓ ${strings.improved}',
                        subtitle: strings.improvedDesc,
                        value: 'improved',
                        color: AppColors.primaryGreen,
                        isSelected: state.selectedOutcome == 'improved',
                        onSelect: () => controller.selectOutcome('improved'),
                      ),
                      const SizedBox(height: AppSpacing.sm),

                      _buildOutcomeOption(
                        title: '○ ${strings.noChange}',
                        subtitle: strings.noChangeDesc,
                        value: 'no_change',
                        color: const Color(0xFFD97706),
                        isSelected: state.selectedOutcome == 'no_change',
                        onSelect: () => controller.selectOutcome('no_change'),
                      ),
                      const SizedBox(height: AppSpacing.sm),

                      _buildOutcomeOption(
                        title: '✕ ${strings.gotWorse}',
                        subtitle: strings.gotWorseDesc,
                        value: 'got_worse',
                        color: const Color(0xFFC62828),
                        isSelected: state.selectedOutcome == 'got_worse',
                        onSelect: () => controller.selectOutcome('got_worse'),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Add Update Card: Photo + Notes
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.add_a_photo_outlined, size: 18.0, color: AppColors.primaryGreen),
                          const SizedBox(width: AppSpacing.sm),
                          Text(
                            strings.uploadNewPhoto,
                            style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.sm),

                      if (_selectedImage != null) ...[
                        ClipRRect(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          child: Stack(
                            children: [
                              Image.file(
                                File(_selectedImage!.path),
                                height: 160.0,
                                width: double.infinity,
                                fit: BoxFit.cover,
                              ),
                              Positioned(
                                top: 8.0,
                                right: 8.0,
                                child: InkWell(
                                  onTap: () => setState(() => _selectedImage = null),
                                  child: Container(
                                    padding: const EdgeInsets.all(4.0),
                                    decoration: const BoxDecoration(
                                      color: Colors.black54,
                                      shape: BoxShape.circle,
                                    ),
                                    child: const Icon(Icons.close, color: Colors.white, size: 18.0),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: AppSpacing.sm),
                      ],

                      Row(
                        children: [
                          Expanded(
                            child: OutlinedButton.icon(
                              onPressed: () => _pickImage(ImageSource.camera),
                              icon: const Icon(Icons.camera_alt_outlined, size: 18.0),
                              label: Text(strings.camera),
                              style: OutlinedButton.styleFrom(
                                foregroundColor: AppColors.textPrimary,
                                side: const BorderSide(color: AppColors.border),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                              ),
                            ),
                          ),
                          const SizedBox(width: AppSpacing.md),
                          Expanded(
                            child: OutlinedButton.icon(
                              onPressed: () => _pickImage(ImageSource.gallery),
                              icon: const Icon(Icons.photo_library_outlined, size: 18.0),
                              label: Text(strings.gallery),
                              style: OutlinedButton.styleFrom(
                                foregroundColor: AppColors.textPrimary,
                                side: const BorderSide(color: AppColors.border),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                              ),
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: AppSpacing.lg),
                      const Divider(color: AppColors.divider),
                      const SizedBox(height: AppSpacing.sm),

                      Text(
                        strings.additionalContextOptional,
                        style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      TextField(
                        controller: _notesController,
                        maxLines: 2,
                        onChanged: controller.setNotes,
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
                    child: Text(
                      state.errorMessage!,
                      style: const TextStyle(fontSize: 12.5, color: Color(0xFFC62828)),
                    ),
                  ),
                ],

                const SizedBox(height: AppSpacing.xl),

                // Action Buttons: Submit Update & Skip for Now
                BhoomiPrimaryButton(
                  text: strings.save,
                  isLoading: state.isSubmitting,
                  icon: Icons.send_rounded,
                  onPressed: state.selectedOutcome == null
                      ? null
                      : () => controller.submitFollowup(
                            farmId: widget.farmId,
                            diagnosisId: widget.diagnosisId,
                          ),
                ),
                const SizedBox(height: AppSpacing.sm),
                TextButton(
                  onPressed: () => context.pop(),
                  child: Text(
                    strings.cancel,
                    style: const TextStyle(
                      fontSize: 14.0,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.md),
              ] else ...[
                // Tracking Progress Card
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
                    children: [
                      const Text(
                        'Tracking Progress',
                        style: TextStyle(
                          fontSize: 20.0,
                          fontWeight: FontWeight.w900,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.lg),

                      // Progress Circular Counter
                      Container(
                        width: 90.0,
                        height: 90.0,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: AppColors.lightGreen,
                          border: Border.all(color: AppColors.primaryGreen, width: 3.0),
                        ),
                        child: const Center(
                          child: Text(
                            '100%',
                            style: TextStyle(
                              fontSize: 22.0,
                              fontWeight: FontWeight.w900,
                              color: AppColors.primaryGreen,
                            ),
                          ),
                        ),
                      ),

                      const SizedBox(height: AppSpacing.lg),

                      // Step Indicators
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: AppColors.background,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                        ),
                        child: const Column(
                          children: [
                            _ProgressStepRow(label: 'Update received', isDone: true),
                            SizedBox(height: AppSpacing.xs),
                            _ProgressStepRow(label: 'Analyzing field data', isDone: true),
                            SizedBox(height: AppSpacing.xs),
                            _ProgressStepRow(label: 'Comparing progress', isDone: true),
                            SizedBox(height: AppSpacing.xs),
                            _ProgressStepRow(label: 'Preparing next advice', isDone: true),
                          ],
                        ),
                      ),

                      const SizedBox(height: AppSpacing.lg),
                      const Divider(color: AppColors.divider),
                      const SizedBox(height: AppSpacing.md),

                      Align(
                        alignment: Alignment.centerLeft,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Outcome: ${state.response!.outcome.toUpperCase()}',
                              style: const TextStyle(
                                fontSize: 13.0,
                                fontWeight: FontWeight.w800,
                                color: AppColors.primaryGreen,
                              ),
                            ),
                            const SizedBox(height: AppSpacing.xs),
                            const Text(
                              'Recommended Next Steps',
                              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                            ),
                            const SizedBox(height: 4.0),
                            Text(
                              state.response!.nextSteps,
                              style: const TextStyle(fontSize: 13.5, height: 1.4, color: AppColors.textSecondary),
                            ),
                          ],
                        ),
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
                            Text(
                              'Expert Review Recommended',
                              style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.xs),
                        const Text(
                          'Since the symptoms have not stabilized, an agricultural officer at KVK can personally review your case.',
                          style: TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
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
                const SizedBox(height: AppSpacing.md),
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
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.w800,
                      color: isSelected ? color : AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 2.0),
                  Text(
                    subtitle,
                    style: const TextStyle(fontSize: 11.5, color: AppColors.textMuted),
                  ),
                ],
              ),
            ),
            if (isSelected)
              Icon(Icons.check_circle_rounded, color: color, size: 22.0),
          ],
        ),
      ),
    );
  }
}

class _ProgressStepRow extends StatelessWidget {
  final String label;
  final bool isDone;

  const _ProgressStepRow({required this.label, required this.isDone});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          isDone ? Icons.check_circle_rounded : Icons.radio_button_unchecked_rounded,
          size: 16.0,
          color: isDone ? AppColors.primaryGreen : AppColors.textMuted,
        ),
        const SizedBox(width: AppSpacing.sm),
        Text(
          label,
          style: TextStyle(
            fontSize: 12.5,
            fontWeight: isDone ? FontWeight.w700 : FontWeight.w500,
            color: isDone ? AppColors.textPrimary : AppColors.textMuted,
          ),
        ),
      ],
    );
  }
}

