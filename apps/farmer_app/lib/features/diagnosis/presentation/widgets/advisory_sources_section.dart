import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/diagnosis_response.dart';

class AdvisorySourcesSection extends StatefulWidget {
  final List<AdvisorySource> sources;

  const AdvisorySourcesSection({
    super.key,
    required this.sources,
  });

  @override
  State<AdvisorySourcesSection> createState() => _AdvisorySourcesSectionState();
}

class _AdvisorySourcesSectionState extends State<AdvisorySourcesSection> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    if (widget.sources.isEmpty) return const SizedBox.shrink();

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Row(
                children: [
                  Icon(Icons.menu_book_rounded, size: 20.0, color: AppColors.primaryGreen),
                  SizedBox(width: AppSpacing.sm),
                  Text('Information Sources', style: AppTypography.titleLarge),
                ],
              ),
              IconButton(
                icon: Icon(
                  _isExpanded ? Icons.keyboard_arrow_up_rounded : Icons.keyboard_arrow_down_rounded,
                  color: AppColors.primaryGreen,
                ),
                onPressed: () {
                  setState(() {
                    _isExpanded = !_isExpanded;
                  });
                },
              ),
            ],
          ),
          const SizedBox(height: 2.0),
          Text(
            'Based on verified agricultural research and university guides.',
            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textMuted),
          ),

          if (_isExpanded) ...[
            const Divider(color: AppColors.divider, height: AppSpacing.lg),
            ...widget.sources.map((source) {
              return Padding(
                padding: const EdgeInsets.only(bottom: AppSpacing.md),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.library_books_outlined, size: 16.0, color: AppColors.primaryGreen),
                    const SizedBox(width: AppSpacing.sm),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            source.title,
                            style: AppTypography.titleMedium.copyWith(
                              fontSize: 13.0,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          const SizedBox(height: 2.0),
                          Text(
                            source.organization,
                            style: const TextStyle(fontSize: 11.0, color: AppColors.textSecondary),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            }),
          ],
        ],
      ),
    );
  }
}
