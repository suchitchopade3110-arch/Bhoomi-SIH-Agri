import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../data/models/land_submission_request.dart';

class BoundaryMapWidget extends StatelessWidget {
  final GeoJsonPolygonData? boundaryGeojson;
  final bool isEditable;
  final VoidCallback? onSketchBoundary;

  const BoundaryMapWidget({
    super.key,
    this.boundaryGeojson,
    this.isEditable = false,
    this.onSketchBoundary,
  });

  @override
  Widget build(BuildContext context) {
    final points = boundaryGeojson?.coordinates.firstOrNull ?? [];

    return Container(
      height: 220.0,
      width: double.infinity,
      decoration: BoxDecoration(
        color: const Color(0xFFE8F5E9),
        borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
        border: Border.all(color: AppColors.border),
      ),
      child: Stack(
        children: [
          // OpenStreetMap Grid Simulation Background
          Positioned.fill(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
              child: CustomPaint(
                painter: _MapGridPainter(),
              ),
            ),
          ),

          // Render Polygon Shape Visualization
          if (points.isNotEmpty) ...[
            Positioned.fill(
              child: Center(
                child: Container(
                  width: 160.0,
                  height: 120.0,
                  decoration: BoxDecoration(
                    color: AppColors.primaryGreen.withValues(alpha: 0.25),
                    border: Border.all(color: AppColors.primaryGreen, width: 2.5),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                  ),
                  child: Stack(
                    children: [
                      const Positioned(
                        top: 6,
                        left: 6,
                        child: Icon(Icons.location_on, size: 16.0, color: AppColors.primaryGreen),
                      ),
                      const Positioned(
                        bottom: 6,
                        right: 6,
                        child: Icon(Icons.my_location, size: 14.0, color: AppColors.primaryGreen),
                      ),
                      Center(
                        child: Text(
                          '${points.length} Vertices Preserved',
                          style: AppTypography.labelMedium.copyWith(
                            color: AppColors.primaryGreen,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],

          // Map Attribution & Controls Overlay
          Positioned(
            bottom: AppSpacing.sm,
            left: AppSpacing.sm,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2.0),
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.85),
                borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
              ),
              child: const Text(
                '© OpenStreetMap contributors',
                style: TextStyle(fontSize: 9.0, color: AppColors.textMuted),
              ),
            ),
          ),

          if (isEditable && onSketchBoundary != null) ...[
            Positioned(
              bottom: AppSpacing.sm,
              right: AppSpacing.sm,
              child: ElevatedButton.icon(
                onPressed: onSketchBoundary,
                icon: const Icon(Icons.edit_location_alt_rounded, size: 16.0),
                label: const Text('Sketch Boundary'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryGreen,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.xs),
                  textStyle: AppTypography.labelMedium.copyWith(color: Colors.white),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class _MapGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFC8E6C9).withValues(alpha: 0.5)
      ..strokeWidth = 1.0;

    const step = 24.0;
    for (double x = 0; x < size.width; x += step) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }
    for (double y = 0; y < size.height; y += step) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
