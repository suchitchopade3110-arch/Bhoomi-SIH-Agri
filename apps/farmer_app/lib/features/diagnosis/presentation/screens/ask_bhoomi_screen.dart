import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../voice/application/voice_controller.dart';
import '../../../voice/presentation/widgets/voice_confirmation_sheet.dart';
import '../../../voice/presentation/widgets/voice_record_button.dart';
import '../../application/diagnosis_controller.dart';
import '../widgets/crop_image_picker.dart';

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
    final diagnosisState = ref.watch(diagnosisControllerProvider);
    final diagnosisController = ref.read(diagnosisControllerProvider.notifier);
    final voiceState = ref.watch(voiceControllerProvider);
    final voiceController = ref.read(voiceControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Ask BHOOMI'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Intro Card
              Container(
                padding: const EdgeInsets.all(AppSpacing.lg),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppColors.primaryGreen, Color(0xFF1B5E20)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.2),
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.psychology_rounded, color: Colors.white, size: 28.0),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Crop Advisory & Support',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 18.0,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          SizedBox(height: 2.0),
                          Text(
                            'Speak or describe symptoms. Add a photo for trusted agronomic guidance.',
                            style: TextStyle(color: Colors.white70, fontSize: 12.0),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Voice Assistant Card
              BhoomiCard(
                child: Column(
                  children: [
                    const Text('What problem are you seeing?', style: AppTypography.titleLarge),
                    const SizedBox(height: AppSpacing.md),

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
                                Navigator.pop(context);
                                _textController.text = transcription.text;
                                diagnosisController.setProblemDescription(transcription.text);
                              },
                              onCancel: () {
                                Navigator.pop(context);
                                voiceController.reset();
                              },
                            ),
                          );
                        }
                      },
                    ),

                    const SizedBox(height: AppSpacing.md),
                    const Text('or type your problem below', style: TextStyle(fontSize: 12.0, color: AppColors.textMuted)),
                    const SizedBox(height: AppSpacing.sm),

                    TextField(
                      controller: _textController,
                      maxLines: 3,
                      onChanged: diagnosisController.setProblemDescription,
                      decoration: InputDecoration(
                        hintText: 'e.g. My paddy leaves are turning yellow from the edges with wavy margins...',
                        filled: true,
                        fillColor: AppColors.background,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.border),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.primaryGreen, width: 2.0),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Crop Photo Picker
              CropImagePickerWidget(
                state: diagnosisState,
                onPickImage: (source) => diagnosisController.pickAndUploadImage(source),
              ),

              const SizedBox(height: AppSpacing.xl),

              // Submit Diagnosis CTA
              BhoomiPrimaryButton(
                text: 'Diagnose & Get Advice',
                isLoading: diagnosisState.isDiagnosing,
                icon: Icons.auto_awesome_rounded,
                onPressed: () async {
                  diagnosisController.setProblemDescription(_textController.text);
                  final response = await diagnosisController.submitDiagnosis(widget.farmId);
                  if (response != null && context.mounted) {
                    context.push('/diagnosis/result/${widget.farmId}');
                  }
                },
              ),

              const SizedBox(height: AppSpacing.md),
            ],
          ),
        ),
      ),
    );
  }
}
