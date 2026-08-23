import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../application/voice_state.dart';

class VoiceRecordButton extends StatefulWidget {
  final VoiceState state;
  final VoidCallback onStartRecording;
  final VoidCallback onStopRecording;

  const VoiceRecordButton({
    super.key,
    required this.state,
    required this.onStartRecording,
    required this.onStopRecording,
  });

  @override
  State<VoiceRecordButton> createState() => _VoiceRecordButtonState();
}

class _VoiceRecordButtonState extends State<VoiceRecordButton>
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
    final isProcessing = widget.state.isUploading || widget.state.isTranscribing;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        GestureDetector(
          onTap: () {
            if (isRecording) {
              widget.onStopRecording();
            } else if (!isProcessing) {
              widget.onStartRecording();
            }
          },
          child: AnimatedBuilder(
            animation: _pulse,
            builder: (context, child) {
              final scale = isRecording ? _pulse.value : 1.0;
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
                      colors: isRecording
                          ? [const Color(0xFFE76F51), const Color(0xFFC62828)]
                          : isProcessing
                              ? [AppColors.warmAccent, const Color(0xFFE76F51)]
                              : [AppColors.primaryGreen, AppColors.secondaryGreen],
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
                    child: isProcessing
                        ? const SizedBox(
                            width: 32.0,
                            height: 32.0,
                            child: CircularProgressIndicator(
                              strokeWidth: 3.0,
                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                            ),
                          )
                        : Icon(
                            isRecording ? Icons.stop_rounded : Icons.mic_rounded,
                            color: Colors.white,
                            size: 42.0,
                          ),
                  ),
                ),
              );
            },
          ),
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          isRecording
              ? 'Recording... Tap to send'
              : isProcessing
                  ? (widget.state.isUploading ? 'Uploading audio...' : 'Transcribing speech...')
                  : 'Tap to Ask BHOOMI',
          style: AppTypography.labelMedium.copyWith(
            color: isRecording
                ? const Color(0xFFC62828)
                : isProcessing
                    ? AppColors.warmAccent
                    : AppColors.textPrimary,
            fontWeight: FontWeight.w700,
          ),
        ),
      ],
    );
  }
}
