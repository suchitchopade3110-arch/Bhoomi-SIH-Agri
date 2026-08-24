import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/widgets/bhoomi_card.dart';

class RelatedResourcesSection extends StatelessWidget {
  final String? cropName;

  const RelatedResourcesSection({
    super.key,
    this.cropName,
  });

  @override
  Widget build(BuildContext context) {
    final crop = cropName ?? 'Crop';

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.menu_book_rounded, color: AppColors.primaryGreen, size: 20.0),
              SizedBox(width: AppSpacing.sm),
              Text(
                'Related Resources',
                style: TextStyle(
                  fontSize: 16.0,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),

          // 1. Articles
          _buildResourceCategory(
            title: 'Articles',
            icon: Icons.article_outlined,
            color: AppColors.primaryGreen,
            items: [
              'How to Control Leaf Blast in $crop?',
              'Integrated Pest Management for $crop',
            ],
          ),
          const SizedBox(height: AppSpacing.md),

          // 2. Videos
          _buildResourceCategory(
            title: 'Videos',
            icon: Icons.play_circle_outline_rounded,
            color: const Color(0xFFE76F51),
            items: [
              'Top Tips for Healthy $crop Field',
              'Symptoms of Nutrient Deficiency vs Disease',
            ],
          ),
          const SizedBox(height: AppSpacing.md),

          // 3. Documents
          _buildResourceCategory(
            title: 'Documents',
            icon: Icons.description_outlined,
            color: const Color(0xFF0284C7),
            items: [
              'FAO-56 Irrigation & Water Management Guide',
              'ICAR Package of Practices: $crop Guidelines',
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildResourceCategory({
    required String title,
    required IconData icon,
    required Color color,
    required List<String> items,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 16.0, color: color),
            const SizedBox(width: 4.0),
            Text(
              title,
              style: TextStyle(
                fontSize: 12.5,
                fontWeight: FontWeight.w700,
                color: color,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.xs),
        ...items.map((item) => Padding(
              padding: const EdgeInsets.only(bottom: 6.0),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 8.0),
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                  border: Border.all(color: AppColors.border),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        item,
                        style: const TextStyle(
                          fontSize: 12.0,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                    ),
                    const Icon(Icons.arrow_forward_ios_rounded, size: 12.0, color: AppColors.textMuted),
                  ],
                ),
              ),
            )),
      ],
    );
  }
}
