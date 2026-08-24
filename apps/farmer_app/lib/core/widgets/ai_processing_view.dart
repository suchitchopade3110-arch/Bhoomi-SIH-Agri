import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';
import '../../app/theme/app_typography.dart';

class AiProcessingView extends StatefulWidget {
  final String? title;
  final String? subtitle;
  final bool showIntelligenceModules;

  const AiProcessingView({
    super.key,
    this.title,
    this.subtitle,
    this.showIntelligenceModules = true,
  });

  @override
  State<AiProcessingView> createState() => _AiProcessingViewState();
}

class _AiProcessingViewState extends State<AiProcessingView>
    with SingleTickerProviderStateMixin {
  late AnimationController _animController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
    _scaleAnimation = Tween<double>(begin: 0.92, end: 1.08).animate(
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
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Header
            Text(
              widget.title ?? 'Processing Your Query',
              style: const TextStyle(
                fontSize: 22.0,
                fontWeight: FontWeight.w800,
                color: AppColors.textPrimary,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: AppSpacing.xl),

            // Pulsing Sprout Emblem (🌱)
            AnimatedBuilder(
              animation: _scaleAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _scaleAnimation.value,
                  child: Container(
                    width: 90.0,
                    height: 90.0,
                    decoration: BoxDecoration(
                      color: AppColors.lightGreen,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primaryGreen.withValues(alpha: 0.2),
                          blurRadius: 20.0,
                          spreadRadius: 4.0,
                        ),
                      ],
                    ),
                    child: const Center(
                      child: Text(
                        '🌱',
                        style: TextStyle(fontSize: 44.0),
                      ),
                    ),
                  ),
                );
              },
            ),

            const SizedBox(height: AppSpacing.lg),
            Text(
              widget.subtitle ?? 'Analyzing your farm...',
              style: AppTypography.titleMedium.copyWith(
                fontWeight: FontWeight.w700,
                color: AppColors.primaryGreen,
              ),
            ),
            const SizedBox(height: AppSpacing.lg),

            // Step Progress Checklist
            Container(
              constraints: const BoxConstraints(maxWidth: 320.0),
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                children: [
                  _buildStepRow('Understanding your issue', isCompleted: true),
                  const SizedBox(height: AppSpacing.sm),
                  _buildStepRow('Searching agricultural knowledge', isCompleted: true),
                  const SizedBox(height: AppSpacing.sm),
                  _buildStepRow('Checking farm indicators', isCompleted: false),
                ],
              ),
            ),

            if (widget.showIntelligenceModules) ...[
              const SizedBox(height: AppSpacing.xl),
              const Text(
                'Our Intelligence Working',
                style: TextStyle(
                  fontSize: 16.0,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: AppSpacing.md),

              // Module Cards Grid
              Column(
                children: [
                  _buildModuleTile(
                    emoji: '📖',
                    title: 'RAG Advisory',
                    description: 'Finding relevant agricultural knowledge',
                    color: AppColors.primaryGreen,
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  _buildModuleTile(
                    emoji: '💧',
                    title: 'FAO-56 Planner',
                    description: 'Checking irrigation requirements',
                    color: const Color(0xFF0284C7),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  _buildModuleTile(
                    emoji: '🌿',
                    title: 'Health Indicator',
                    description: 'Analyzing farm conditions',
                    color: const Color(0xFF059669),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStepRow(String label, {required bool isCompleted}) {
    return Row(
      children: [
        Container(
          width: 20.0,
          height: 20.0,
          decoration: BoxDecoration(
            color: isCompleted ? AppColors.lightGreen : AppColors.background,
            shape: BoxShape.circle,
            border: Border.all(
              color: isCompleted ? AppColors.primaryGreen : AppColors.border,
            ),
          ),
          child: Center(
            child: isCompleted
                ? const Icon(Icons.check_rounded, size: 14.0, color: AppColors.primaryGreen)
                : const SizedBox(
                    width: 8.0,
                    height: 8.0,
                    child: CircularProgressIndicator(
                      strokeWidth: 1.5,
                      valueColor: AlwaysStoppedAnimation<Color>(AppColors.primaryGreen),
                    ),
                  ),
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: Text(
            label,
            style: TextStyle(
              fontSize: 13.0,
              fontWeight: isCompleted ? FontWeight.w600 : FontWeight.w500,
              color: isCompleted ? AppColors.textPrimary : AppColors.textMuted,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildModuleTile({
    required String emoji,
    required String title,
    required String description,
    required Color color,
  }) {
    return Container(
      constraints: const BoxConstraints(maxWidth: 340.0),
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.xs + 2),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
            ),
            child: Text(emoji, style: const TextStyle(fontSize: 18.0)),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 13.5,
                    fontWeight: FontWeight.w800,
                    color: AppColors.textPrimary,
                  ),
                ),
                Text(
                  description,
                  style: const TextStyle(fontSize: 11.5, color: AppColors.textMuted),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
