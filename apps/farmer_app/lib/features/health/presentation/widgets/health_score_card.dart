import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/health_snapshot.dart';

class HealthScoreCard extends StatelessWidget {
  final HealthSnapshot snapshot;

  const HealthScoreCard({
    super.key,
    required this.snapshot,
  });

  Color _getBandColor(String band) {
    switch (band.toLowerCase()) {
      case 'good':
      case 'excellent':
        return AppColors.healthGood;
      case 'moderate':
      case 'fair':
        return AppColors.healthModerate;
      case 'poor':
      case 'critical':
        return AppColors.healthPoor;
      case 'unrated':
      default:
        return AppColors.healthUnrated;
    }
  }

  @override
  Widget build(BuildContext context) {
    final isRated = snapshot.isRated && snapshot.score != null;
    final bandColor = _getBandColor(snapshot.band);

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.xl),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Overall Farm Health',
                style: TextStyle(
                  fontSize: 18.0,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 3.0),
                decoration: BoxDecoration(
                  color: bandColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                  border: Border.all(color: bandColor.withValues(alpha: 0.4)),
                ),
                child: Text(
                  isRated ? snapshot.band.toUpperCase() : 'UNRATED',
                  style: TextStyle(
                    color: bandColor,
                    fontWeight: FontWeight.w800,
                    fontSize: 11.0,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xl),

          if (isRated) ...[
            // Circular Health Indicator
            SizedBox(
              width: 170.0,
              height: 170.0,
              child: CustomPaint(
                painter: _CircularGaugePainter(
                  progress: (snapshot.score! / 100.0).clamp(0.0, 1.0),
                  color: bandColor,
                  trackColor: AppColors.lightGreen,
                ),
                child: Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        snapshot.band.toUpperCase(),
                        style: TextStyle(
                          color: bandColor,
                          fontSize: 12.0,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 1.0,
                        ),
                      ),
                      const SizedBox(height: 2.0),
                      Text(
                        '${snapshot.score}',
                        style: const TextStyle(
                          fontSize: 42.0,
                          fontWeight: FontWeight.w900,
                          color: AppColors.textPrimary,
                          height: 1.1,
                        ),
                      ),
                      const Text(
                        '/ 100',
                        style: TextStyle(
                          fontSize: 13.0,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textMuted,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.lg),
            Text(
              snapshot.explanation ?? 'Farm parameters are in healthy range.',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
            ),
          ] else ...[
            // STRICT NULL HANDLING: Never show 0/100 or 0 score
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(AppSpacing.lg),
              decoration: BoxDecoration(
                color: AppColors.background,
                borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                border: Border.all(color: AppColors.border),
              ),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: AppColors.healthUnrated.withValues(alpha: 0.12),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.hourglass_empty_rounded, color: AppColors.healthUnrated, size: 32.0),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  const Text(
                    'Unrated',
                    style: TextStyle(
                      fontSize: 18.0,
                      fontWeight: FontWeight.w800,
                      color: AppColors.healthUnrated,
                    ),
                  ),
                  const SizedBox(height: 4.0),
                  const Text(
                    'Not enough data yet',
                    style: TextStyle(
                      fontSize: 14.0,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 4.0),
                  Text(
                    snapshot.explanation ?? 'Complete onboarding and upload farm photos to compute initial score.',
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 12.0, color: AppColors.textMuted),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class _CircularGaugePainter extends CustomPainter {
  final double progress;
  final Color color;
  final Color trackColor;

  _CircularGaugePainter({
    required this.progress,
    required this.color,
    required this.trackColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = (size.width / 2) - 10.0;
    const strokeWidth = 12.0;

    // Track Paint
    final trackPaint = Paint()
      ..color = trackColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -math.pi / 2,
      2 * math.pi,
      false,
      trackPaint,
    );

    // Progress Paint
    final progressPaint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -math.pi / 2,
      2 * math.pi * progress,
      false,
      progressPaint,
    );
  }

  @override
  bool shouldRepaint(covariant _CircularGaugePainter oldDelegate) {
    return oldDelegate.progress != progress ||
        oldDelegate.color != color ||
        oldDelegate.trackColor != trackColor;
  }
}
