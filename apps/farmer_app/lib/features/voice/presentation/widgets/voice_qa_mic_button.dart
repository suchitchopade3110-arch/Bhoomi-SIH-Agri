import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../application/voice_qa_state.dart';

/// Same pulsing mic affordance as [VoiceRecordButton], adapted for
/// [VoiceQaState]'s step machine (idle/recording/uploading/thinking/
/// speaking/answered/error) instead of the form-filling flow's states.
class VoiceQaMicButton extends StatefulWidget {
  final VoiceQaState state;
  final VoidCallback onStartRecording;
  final VoidCallback onStopRecording;

  const VoiceQaMicButton({
    super.key,
    required this.state,
    required this.onStartRecording,
    required this.onStopRecording,
  });

  @override
  State<VoiceQaMicButton> createState() => _VoiceQaMicButtonState();
}

class _VoiceQaMicButtonState extends State<VoiceQaMicButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _animController;
  late Animation<double> _pulse;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat(reverse: true);
    _pulse = Tween<double>(begin: 1.0, end: 1.2).animate(
      CurvedAnimation(parent: _animController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isRecording = widget.state.isRecording;
    final isBusy = widget.state.isBusy;
    final isSpeaking = widget.state.step == VoiceQaStep.speaking;
    final isDisabled = isBusy || isSpeaking;

    final List<Color> gradient = isRecording
        ? [const Color(0xFFE76F51), const Color(0xFFC62828)]
        : isDisabled
            ? [AppColors.warmAccent, const Color(0xFFE76F51)]
            : [AppColors.primaryGreen, AppColors.secondaryGreen];

    return GestureDetector(
      onTap: () {
        if (isRecording) {
          widget.onStopRecording();
        } else if (!isDisabled) {
          widget.onStartRecording();
        }
      },
      child: AnimatedBuilder(
        animation: _pulse,
        builder: (context, child) {
          final scale = isRecording || isSpeaking ? _pulse.value : 1.0;
          return Transform.scale(
            scale: scale,
            child: Container(
              width: 90.0,
              height: 90.0,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: gradient,
                ),
                boxShadow: [
                  BoxShadow(
                    color: (isRecording ? const Color(0xFFE76F51) : AppColors.primaryGreen)
                        .withValues(alpha: 0.35),
                    blurRadius: isRecording ? 24.0 : 12.0,
                    spreadRadius: isRecording ? 4.0 : 0.0,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Center(
                child: isBusy
                    ? const SizedBox(
                        width: 32.0,
                        height: 32.0,
                        child: CircularProgressIndicator(
                          strokeWidth: 3.0,
                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      )
                    : Icon(
                        isRecording
                            ? Icons.stop_rounded
                            : isSpeaking
                                ? Icons.volume_up_rounded
                                : Icons.mic_rounded,
                        color: Colors.white,
                        size: 42.0,
                      ),
              ),
            ),
          );
        },
      ),
    );
  }
}
