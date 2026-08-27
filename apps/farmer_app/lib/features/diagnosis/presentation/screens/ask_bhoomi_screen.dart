import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/ai_processing_view.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../voice/application/voice_controller.dart';
import '../../../voice/presentation/widgets/voice_confirmation_sheet.dart';
import '../../../voice/presentation/widgets/voice_record_button.dart';
import '../../application/diagnosis_controller.dart';
import '../widgets/crop_image_picker.dart';
import '../../../../shared/widgets/bhoomi_bottom_navigation.dart';

class AskBhoomiScreen extends ConsumerStatefulWidget {
  final String farmId;

  const AskBhoomiScreen({
    super.key,
    required this.farmId,
  });

  @override
  ConsumerState<AskBhoomiScreen> createState() => _AskBhoomiScreenState();
}

class _AskBhoomiScreenState extends ConsumerState<AskBhoomiScreen> {
  late TextEditingController _textController;

  final List<Map<String, dynamic>> _topics = const [
    {'key': 'topic_crops', 'icon': Icons.grass_rounded},
    {'key': 'topic_diseases', 'icon': Icons.coronavirus_rounded},
    {'key': 'topic_pests', 'icon': Icons.pest_control_rounded},
    {'key': 'topic_soil', 'icon': Icons.landscape_rounded},
    {'key': 'topic_weather', 'icon': Icons.cloud_queue_rounded},
    {'key': 'topic_prices', 'icon': Icons.currency_rupee_rounded},
    {'key': 'topic_schemes', 'icon': Icons.account_balance_rounded},
  ];

  @override
  void initState() {
    super.initState();
    final state = ref.read(diagnosisControllerProvider);
    _textController = TextEditingController(text: state.problemDescription);
  }

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final strings = ref.watch(bhoomiStringsProvider);
    final diagnosisState = ref.watch(diagnosisControllerProvider);
    final diagnosisController = ref.read(diagnosisControllerProvider.notifier);
    final voiceState = ref.watch(voiceControllerProvider);
    final voiceController = ref.read(voiceControllerProvider.notifier);

    // Calm Agricultural Intelligence Processing Screen
    if (diagnosisState.isDiagnosing) {
      return Scaffold(
        backgroundColor: AppColors.background,
        appBar: AppBar(
          title: Text(strings.bhoomiIntelligence, style: const TextStyle(fontWeight: FontWeight.w800)),
          scrolledUnderElevation: 0,
        ),
        body: SafeArea(
          child: AiProcessingView(
            title: strings.processingQuery,
            subtitle: strings.analyzingFarm,
            showIntelligenceModules: true,
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.askBhoomi, style: const TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Voice Card with Concentric Microphone
              BhoomiCard(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.xl),
                child: Column(
                  children: [
                    Text(
                      strings.askBhoomi,
                      style: const TextStyle(
                        fontSize: 22.0,
                        fontWeight: FontWeight.w800,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 4.0),
                    Text(
                      strings.askBhoomiSub,
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
                    ),
                    const SizedBox(height: AppSpacing.lg),

                    VoiceRecordButton(
                      state: voiceState,
                      onStartRecording: () => voiceController.startRecording(),
                      onStopRecording: () async {
                        final transcription = await voiceController.stopAndProcessAudio();
                        if (transcription != null && context.mounted) {
                          showModalBottomSheet(
                            context: context,
                            isScrollControlled: true,
                            backgroundColor: Colors.transparent,
                            builder: (_) => VoiceConfirmationSheet(
                              transcription: transcription,
                              onConfirm: () {
                                ref.read(voiceControllerProvider.notifier).confirmVoiceField(
                                  field: 'problem_description',
                                  confirmedValue: transcription.text,
                                  isConfirmed: true,
                                );
                                Navigator.pop(context);
                                _textController.text = transcription.text;
                                diagnosisController.setProblemDescription(transcription.text);
                              },
                              onCancel: () {
                                ref.read(voiceControllerProvider.notifier).confirmVoiceField(
                                  field: 'problem_description',
                                  confirmedValue: transcription.text,
                                  isConfirmed: false,
                                );
                                Navigator.pop(context);
                                voiceController.reset();
                              },
                            ),
                          );
                        }
                      },
                    ),

                    const SizedBox(height: AppSpacing.md),
                    InkWell(
                      onTap: () => context.push('/voice-qa/${widget.farmId}'),
                      borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.record_voice_over_rounded, size: 16.0, color: AppColors.primaryGreen),
                            const SizedBox(width: 6.0),
                            Text(
                              'Or have a spoken conversation — hear BHOOMI answer',
                              style: AppTypography.labelMedium.copyWith(
                                color: AppColors.primaryGreen,
                                fontWeight: FontWeight.w700,
                                decoration: TextDecoration.underline,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                    const SizedBox(height: AppSpacing.lg),
                    const Divider(color: AppColors.divider),
                    const SizedBox(height: AppSpacing.sm),

                    // You can ask about topics
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        strings.youCanAskAbout,
                        style: AppTypography.labelMedium.copyWith(
                          fontWeight: FontWeight.w700,
                          color: AppColors.textSecondary,
                        ),
                      ),
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    Wrap(
                      spacing: AppSpacing.xs + 2,
                      runSpacing: AppSpacing.xs + 2,
                      children: _topics.map((t) {
                        final topicName = strings.text(t['key'] as String);
                        return InkWell(
                          onTap: () {
                            if (_textController.text.isEmpty) {
                              _textController.text = topicName;
                            } else {
                              _textController.text += ' $topicName';
                            }
                            diagnosisController.setProblemDescription(_textController.text);
                          },
                          borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 6.0),
                            decoration: BoxDecoration(
                              color: AppColors.lightGreen,
                              borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                              border: Border.all(color: AppColors.primaryGreen.withValues(alpha: 0.2)),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(t['icon'] as IconData, size: 14.0, color: AppColors.primaryGreen),
                                const SizedBox(width: 4.0),
                                Text(
                                  topicName,
                                  style: const TextStyle(
                                    fontSize: 11.5,
                                    fontWeight: FontWeight.w700,
                                    color: AppColors.primaryGreen,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Crop Image Upload Card
              CropImagePickerWidget(
                state: diagnosisState,
                onPickImage: (source) => diagnosisController.pickAndUploadImage(source),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Text Problem Description Input
              BhoomiCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // A photo is required — the backend has no text-only
                    // diagnosis path (image_asset_id is mandatory and must
                    // be a real presigned asset). This field only adds
                    // context to a photo submission, it can't replace one.
                    Text(strings.additionalContextOptional, style: AppTypography.titleMedium),
                    const SizedBox(height: AppSpacing.sm),
                    TextField(
                      controller: _textController,
                      maxLines: 3,
                      onChanged: diagnosisController.setProblemDescription,
                      decoration: InputDecoration(
                        hintText: strings.text('type_problem_hint'),
                        hintStyle: const TextStyle(fontSize: 13.0, color: AppColors.textMuted),
                      ),
                    ),
                  ],
                ),
              ),

              if (diagnosisState.errorMessage != null) ...[
                const SizedBox(height: AppSpacing.md),
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
                          diagnosisState.errorMessage!,
                          style: const TextStyle(
                            color: Color(0xFFC62828),
                            fontSize: 12.0,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],

              const SizedBox(height: AppSpacing.xl),

              if (diagnosisState.imageAssetId == null) ...[
                Padding(
                  padding: const EdgeInsets.only(bottom: AppSpacing.md),
                  child: Text(
                    strings.photoRequiredHint,
                    style: const TextStyle(fontSize: 12.0, color: AppColors.textMuted),
                  ),
                ),
              ],

              // Primary CTA — disabled until a real image has finished
              // uploading, since the backend has no text-only diagnosis
              // path (see DiagnosisState.isValid).
              BhoomiPrimaryButton(
                text: strings.text('diagnose_get_advice'),
                isLoading: diagnosisState.isDiagnosing,
                icon: Icons.auto_awesome_rounded,
                onPressed: diagnosisState.isValid
                    ? () async {
                        diagnosisController.setProblemDescription(_textController.text);
                        final response = await diagnosisController.submitDiagnosis(widget.farmId);
                        if (response != null && context.mounted) {
                          context.push('/diagnosis/result/${widget.farmId}');
                        }
                      }
                    : null,
              ),

              const SizedBox(height: AppSpacing.xl),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BhoomiBottomNavigation(farmId: widget.farmId, currentIndex: 1),
    );
  }
}
