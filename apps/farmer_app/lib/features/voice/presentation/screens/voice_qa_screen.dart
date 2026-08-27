import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../application/voice_qa_controller.dart';
import '../../application/voice_qa_state.dart';
import '../widgets/voice_qa_mic_button.dart';

/// Speech-to-speech: ask BHOOMI a question out loud and hear a grounded,
/// cited spoken answer back — no photo or typing required. Distinct from
/// AskBhoomiScreen, which is the image-diagnosis flow (voice there only
/// fills the problem-description text field).
class VoiceQaScreen extends ConsumerStatefulWidget {
  final String farmId;

  const VoiceQaScreen({super.key, required this.farmId});

  @override
  ConsumerState<VoiceQaScreen> createState() => _VoiceQaScreenState();
}

class _VoiceQaScreenState extends ConsumerState<VoiceQaScreen> {
  // No manual dispose cleanup needed — voiceQaControllerProvider is
  // .autoDispose, so leaving this screen tears the conversation state
  // down on its own; VoiceQaController.dispose() stops any in-flight
  // playback as part of that.

  String _statusLabel(VoiceQaStep step) {
    switch (step) {
      case VoiceQaStep.recording:
        return 'Listening... tap to send';
      case VoiceQaStep.uploading:
        return 'Uploading your question...';
      case VoiceQaStep.thinking:
        return 'BHOOMI is thinking...';
      case VoiceQaStep.speaking:
        return 'Speaking the answer...';
      case VoiceQaStep.answered:
        return 'Tap to ask another question';
      case VoiceQaStep.error:
        return 'Tap to try again';
      case VoiceQaStep.idle:
        return 'Tap and ask any question out loud';
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(voiceQaControllerProvider);
    final controller = ref.read(voiceQaControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Ask BHOOMI', style: TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: state.turns.isEmpty
                  ? _EmptyPrompt(step: state.step)
                  : _ConversationList(
                      turns: state.turns,
                      onReplay: controller.replayLastAnswer,
                    ),
            ),
            if (state.errorMessage != null)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(AppSpacing.md),
                  margin: const EdgeInsets.only(bottom: AppSpacing.md),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFEBEE),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                    border: Border.all(color: const Color(0xFFFFCDD2)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.error_outline, color: Color(0xFFC62828), size: 18.0),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(
                        child: Text(
                          state.errorMessage!,
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
              ),
            Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.lg, AppSpacing.md, AppSpacing.lg, AppSpacing.xl,
              ),
              child: Column(
                children: [
                  VoiceQaMicButton(
                    state: state,
                    onStartRecording: controller.startRecording,
                    onStopRecording: () => controller.stopAndAsk(farmId: widget.farmId),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  Text(
                    _statusLabel(state.step),
                    style: AppTypography.labelMedium.copyWith(
                      color: state.step == VoiceQaStep.error
                          ? const Color(0xFFC62828)
                          : AppColors.textSecondary,
                      fontWeight: FontWeight.w700,
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
}

class _EmptyPrompt extends StatelessWidget {
  final VoiceQaStep step;

  const _EmptyPrompt({required this.step});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.record_voice_over_rounded, size: 56.0, color: AppColors.primaryGreen.withValues(alpha: 0.5)),
            const SizedBox(height: AppSpacing.md),
            const Text(
              'Speak with BHOOMI',
              style: TextStyle(fontSize: 18.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
            ),
            const SizedBox(height: AppSpacing.xs),
            const Text(
              'Ask about crops, diseases, pests, soil or schemes in your own language — BHOOMI will answer out loud.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
            ),
          ],
        ),
      ),
    );
  }
}

class _ConversationList extends StatelessWidget {
  final List<VoiceQaTurn> turns;
  final Future<void> Function() onReplay;

  const _ConversationList({required this.turns, required this.onReplay});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(AppSpacing.lg),
      itemCount: turns.length,
      itemBuilder: (context, index) {
        final turn = turns[index];
        final isLast = index == turns.length - 1;
        return Padding(
          padding: const EdgeInsets.only(bottom: AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Farmer's question, right-aligned bubble.
              Align(
                alignment: Alignment.centerRight,
                child: Container(
                  constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
                  padding: const EdgeInsets.symmetric(horizontal: 14.0, vertical: 10.0),
                  margin: const EdgeInsets.only(bottom: AppSpacing.sm),
                  decoration: BoxDecoration(
                    color: AppColors.primaryGreen,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                  ),
                  child: Text(
                    turn.transcript,
                    style: const TextStyle(color: Colors.white, fontSize: 13.5, fontWeight: FontWeight.w600),
                  ),
                ),
              ),
              // BHOOMI's spoken answer, left-aligned card with a replay button.
              Align(
                alignment: Alignment.centerLeft,
                child: BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  child: ConstrainedBox(
                    constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.78),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Padding(
                          padding: EdgeInsets.only(top: 2.0),
                          child: Icon(Icons.spa_rounded, color: AppColors.primaryGreen, size: 18.0),
                        ),
                        const SizedBox(width: AppSpacing.sm),
                        Expanded(
                          child: Text(
                            turn.answerText,
                            style: const TextStyle(fontSize: 13.5, color: AppColors.textPrimary, height: 1.35),
                          ),
                        ),
                        if (turn.audioResponseUrl.isNotEmpty && isLast) ...[
                          const SizedBox(width: AppSpacing.xs),
                          InkWell(
                            onTap: onReplay,
                            borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                            child: const Padding(
                              padding: EdgeInsets.all(4.0),
                              child: Icon(Icons.volume_up_rounded, color: AppColors.primaryGreen, size: 20.0),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
