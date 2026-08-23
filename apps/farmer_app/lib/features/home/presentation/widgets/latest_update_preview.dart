import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../updates/application/updates_controller.dart';

class LatestUpdatePreview extends ConsumerWidget {
  final String farmId;

  const LatestUpdatePreview({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final updatesAsync = ref.watch(farmUpdatesProvider(farmId));

    return updatesAsync.when(
      loading: () => const SizedBox.shrink(),
      error: (e, _) => const SizedBox.shrink(),
      data: (updates) {
        if (updates.isEmpty) return const SizedBox.shrink();
        final latest = updates.first;

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
                      Icon(Icons.notifications_active_rounded, color: AppColors.primaryGreen, size: 18.0),
                      SizedBox(width: AppSpacing.xs),
                      Text(
                        'Latest Update',
                        style: TextStyle(fontSize: 14.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                      ),
                    ],
                  ),
                  TextButton(
                    onPressed: () => context.push('/updates/$farmId'),
                    child: const Text('View All', style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: AppColors.primaryGreen)),
                  ),
                ],
              ),
              const SizedBox(height: 2.0),
              Text(
                latest.title,
                style: const TextStyle(fontSize: 13.0, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
              ),
              const SizedBox(height: 2.0),
              Text(
                latest.description,
                style: const TextStyle(fontSize: 12.0, color: AppColors.textSecondary),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        );
      },
    );
  }
}
