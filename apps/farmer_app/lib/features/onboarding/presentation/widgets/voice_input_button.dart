import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';

class VoiceInputButton extends StatefulWidget {
  final bool isListening;
  final VoidCallback onTap;
  final String promptText;
  final String? activeValue;

  const VoiceInputButton({
    super.key,
    required this.isListening,
    required this.onTap,
    required this.promptText,
    this.activeValue,
  });

  @override
  State<VoiceInputButton> createState() => _VoiceInputButtonState();
}

class _VoiceInputButtonState extends State<VoiceInputButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.15).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        GestureDetector(
          onTap: widget.onTap,
          child: AnimatedBuilder(
            animation: _pulseAnimation,
            builder: (context, child) {
              final scale = widget.isListening ? _pulseAnimation.value : 1.0;
              return Transform.scale(
                scale: scale,
                child: Container(
                  width: 96.0,
                  height: 96.0,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: widget.isListening
                          ? [
                              AppColors.warmAccent,
                              const Color(0xFFE76F51),
                            ]
                          : [
                              AppColors.primaryGreen,
                              AppColors.secondaryGreen,
                            ],
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: widget.isListening
                            ? AppColors.warmAccent.withValues(alpha: 0.4)
                            : AppColors.primaryGreen.withValues(alpha: 0.3),
                        blurRadius: widget.isListening ? 24.0 : 12.0,
                        spreadRadius: widget.isListening ? 4.0 : 0.0,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Icon(
                    widget.isListening ? Icons.mic_rounded : Icons.mic_none_rounded,
                    color: Colors.white,
                    size: 44.0,
                  ),
                ),
              );
            },
          ),
        ),
        const SizedBox(height: AppSpacing.md),
        Text(
          widget.isListening ? 'Listening... speak clearly' : 'Tap to speak your answer',
          style: AppTypography.labelMedium.copyWith(
            color: widget.isListening ? AppColors.warmAccent : AppColors.textMuted,
            fontWeight: FontWeight.w600,
          ),
        ),
        if (widget.activeValue != null && widget.activeValue!.isNotEmpty) ...[
          const SizedBox(height: AppSpacing.sm),
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: AppSpacing.xs + 2,
            ),
            decoration: BoxDecoration(
              color: AppColors.primaryGreen.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
              border: Border.all(color: AppColors.primaryGreen.withValues(alpha: 0.2)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.check_circle, size: 16.0, color: AppColors.primaryGreen),
                const SizedBox(width: AppSpacing.xs),
                Flexible(
                  child: Text(
                    'Selected: ${widget.activeValue}',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: AppTypography.labelMedium.copyWith(
                      color: AppColors.primaryGreen,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }
}
