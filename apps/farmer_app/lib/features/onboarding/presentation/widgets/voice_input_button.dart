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
  late Animation<double> _scaleAnimation;
  late Animation<double> _wave1Animation;
  late Animation<double> _wave2Animation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1600),
    )..repeat();

    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.08).animate(
      CurvedAnimation(
        parent: _pulseController,
        curve: const Interval(0.0, 0.5, curve: Curves.easeInOut),
      ),
    );

    _wave1Animation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeOut),
    );

    _wave2Animation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: _pulseController,
        curve: const Interval(0.25, 1.0, curve: Curves.easeOut),
      ),
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
          child: SizedBox(
            width: 140.0,
            height: 140.0,
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Outer concentric ring 1
                if (widget.isListening) ...[
                  AnimatedBuilder(
                    animation: _wave1Animation,
                    builder: (context, child) {
                      return Container(
                        width: 90.0 + (50.0 * _wave1Animation.value),
                        height: 90.0 + (50.0 * _wave1Animation.value),
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: (widget.isListening ? AppColors.accentGold : AppColors.primaryGreen)
                              .withValues(alpha: 0.25 * (1.0 - _wave1Animation.value)),
                        ),
                      );
                    },
                  ),
                  AnimatedBuilder(
                    animation: _wave2Animation,
                    builder: (context, child) {
                      return Container(
                        width: 90.0 + (35.0 * _wave2Animation.value),
                        height: 90.0 + (35.0 * _wave2Animation.value),
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: (widget.isListening ? AppColors.accentGold : AppColors.primaryGreen)
                              .withValues(alpha: 0.35 * (1.0 - _wave2Animation.value)),
                        ),
                      );
                    },
                  ),
                ] else ...[
                  // Static soft concentric halo
                  Container(
                    width: 116.0,
                    height: 116.0,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppColors.lightGreen.withValues(alpha: 0.8),
                    ),
                  ),
                ],

                // Core Circular Microphone Button
                AnimatedBuilder(
                  animation: _scaleAnimation,
                  builder: (context, child) {
                    final scale = widget.isListening ? _scaleAnimation.value : 1.0;
                    return Transform.scale(
                      scale: scale,
                      child: Container(
                        width: 88.0,
                        height: 88.0,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          gradient: LinearGradient(
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                            colors: widget.isListening
                                ? [
                                    const Color(0xFFF4A261),
                                    const Color(0xFFE76F51),
                                  ]
                                : [
                                    AppColors.primaryDeepGreen,
                                    AppColors.secondaryGreen,
                                  ],
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: widget.isListening
                                  ? const Color(0xFFF4A261).withValues(alpha: 0.4)
                                  : AppColors.primaryGreen.withValues(alpha: 0.3),
                              blurRadius: widget.isListening ? 20.0 : 12.0,
                              spreadRadius: widget.isListening ? 3.0 : 0.0,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: Icon(
                          widget.isListening ? Icons.mic_rounded : Icons.mic_none_rounded,
                          color: Colors.white,
                          size: 40.0,
                        ),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: AppSpacing.sm),

        // Spoken state prompt
        Text(
          widget.isListening
              ? 'Listening... speak in your language'
              : (widget.promptText.isNotEmpty ? widget.promptText : 'Tap and speak'),
          style: AppTypography.labelLarge.copyWith(
            color: widget.isListening ? const Color(0xFFE76F51) : AppColors.primaryGreen,
            fontWeight: FontWeight.w700,
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
              color: AppColors.lightGreen,
              borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
              border: Border.all(color: AppColors.primaryGreen.withValues(alpha: 0.2)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.check_circle_rounded, size: 16.0, color: AppColors.primaryGreen),
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
