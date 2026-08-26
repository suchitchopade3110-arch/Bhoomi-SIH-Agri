import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';
import '../../app/theme/app_typography.dart';
import 'offline_upload_queue.dart';
import 'pending_upload.dart';

/// Visible per-item state for the offline upload queue (checklist §12.4).
///
/// Shows nothing when the queue is empty. Otherwise surfaces a compact
/// summary row that expands into one line per queued/uploading/failed item,
/// each independently retryable — the "per-item state" the checklist asks
/// for, not just a single blanket "something is uploading" spinner.
class PendingUploadsBanner extends ConsumerStatefulWidget {
  const PendingUploadsBanner({super.key});

  @override
  ConsumerState<PendingUploadsBanner> createState() => _PendingUploadsBannerState();
}

class _PendingUploadsBannerState extends ConsumerState<PendingUploadsBanner> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    final items = ref
        .watch(offlineUploadQueueProvider)
        .where((u) => !u.isUploaded)
        .toList();

    if (items.isEmpty) return const SizedBox.shrink();

    final failedCount = items.where((u) => u.isFailed).length;
    final summaryColor = failedCount > 0 ? const Color(0xFFC62828) : AppColors.networkDegradedText;
    final summaryBg = failedCount > 0 ? const Color(0xFFFFEBEE) : AppColors.networkDegradedBg;

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: summaryBg,
        border: const Border(bottom: BorderSide(color: AppColors.divider, width: 1.0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          InkWell(
            onTap: () => setState(() => _expanded = !_expanded),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.sm + 2),
              child: Row(
                children: [
                  Icon(Icons.cloud_upload_outlined, size: 18.0, color: summaryColor),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      _summaryText(items, failedCount),
                      style: AppTypography.labelMedium.copyWith(
                        color: summaryColor,
                        fontWeight: FontWeight.w600,
                        fontSize: 13.0,
                      ),
                    ),
                  ),
                  Icon(
                    _expanded ? Icons.expand_less_rounded : Icons.expand_more_rounded,
                    size: 20.0,
                    color: summaryColor,
                  ),
                ],
              ),
            ),
          ),
          if (_expanded)
            for (final item in items) _PendingUploadRow(item: item),
        ],
      ),
    );
  }

  String _summaryText(List<PendingUpload> items, int failedCount) {
    if (failedCount > 0) {
      return '$failedCount upload${failedCount == 1 ? '' : 's'} failed — tap to review';
    }
    return '${items.length} photo${items.length == 1 ? '' : 's'} waiting to upload';
  }
}

class _PendingUploadRow extends ConsumerWidget {
  final PendingUpload item;

  const _PendingUploadRow({required this.item});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final (label, color) = switch (item.status) {
      PendingUploadStatus.queued => ('Waiting for connection', AppColors.networkDegradedText),
      PendingUploadStatus.uploading => ('Uploading…', AppColors.primaryGreen),
      PendingUploadStatus.failed => (item.errorMessage ?? 'Upload failed', const Color(0xFFC62828)),
      PendingUploadStatus.uploaded => ('Uploaded', AppColors.primaryGreen),
    };

    return Padding(
      padding: const EdgeInsets.fromLTRB(AppSpacing.md, 0, AppSpacing.sm, AppSpacing.sm),
      child: Row(
        children: [
          const SizedBox(width: 26.0),
          Expanded(
            child: Text(
              label,
              style: AppTypography.labelMedium.copyWith(color: color, fontSize: 12.0),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          if (item.isFailed)
            TextButton(
              onPressed: () => ref.read(offlineUploadQueueProvider.notifier).retry(item.id),
              child: const Text('Retry'),
            ),
        ],
      ),
    );
  }
}
