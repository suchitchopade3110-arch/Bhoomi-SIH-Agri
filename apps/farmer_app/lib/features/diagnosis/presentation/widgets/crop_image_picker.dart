import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../application/diagnosis_state.dart';

class CropImagePickerWidget extends ConsumerWidget {
  final DiagnosisState state;
  final void Function(ImageSource source) onPickImage;

  const CropImagePickerWidget({
    super.key,
    required this.state,
    required this.onPickImage,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final strings = ref.watch(bhoomiStringsProvider);
    final hasImage = state.selectedImageBytes != null;
    final isUploading = state.imageUploadStatus == ImageUploadStatus.uploading;
    final isUploaded = state.imageUploadStatus == ImageUploadStatus.uploaded;
    final isFailed = state.imageUploadStatus == ImageUploadStatus.failed;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(AppSpacing.radiusXl),
        border: Border.all(
          color: isUploaded ? AppColors.primaryGreen : AppColors.border,
          width: isUploaded ? 1.5 : 1.0,
        ),
        boxShadow: const [
          BoxShadow(
            color: AppColors.cardShadow,
            blurRadius: 10.0,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    strings.showToBhoomi,
                    style: const TextStyle(
                      fontSize: 16.0,
                      fontWeight: FontWeight.w800,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 2.0),
                  Text(
                    strings.uploadOrTakePhoto,
                    style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted),
                  ),
                ],
              ),
              if (isUploaded)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm + 2, vertical: 4.0),
                  decoration: BoxDecoration(
                    color: AppColors.lightGreen,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                    border: Border.all(color: AppColors.primaryGreen.withValues(alpha: 0.3)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.check_circle_rounded, size: 14.0, color: AppColors.primaryGreen),
                      const SizedBox(width: 4.0),
                      Text(
                        strings.attached,
                        style: const TextStyle(fontSize: 11.0, fontWeight: FontWeight.w800, color: AppColors.primaryGreen),
                      ),
                    ],
                  ),
                ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),

          // Image Preview Container
          if (hasImage) ...[
            ClipRRect(
              borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
              child: Stack(
                children: [
                  Image.memory(
                    state.selectedImageBytes!,
                    height: 180.0,
                    width: double.infinity,
                    fit: BoxFit.cover,
                  ),
                  if (isUploading)
                    Positioned.fill(
                      child: Container(
                        color: Colors.black54,
                        child: Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const CircularProgressIndicator(color: Colors.white, strokeWidth: 3.0),
                              const SizedBox(height: AppSpacing.sm),
                              Text(
                                '${strings.text('analyzing_image')} ${(state.imageUploadProgress * 100).toInt()}%',
                                style: const TextStyle(color: Colors.white, fontSize: 13.0, fontWeight: FontWeight.w600),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.md),
          ] else ...[
            Container(
              height: 120.0,
              width: double.infinity,
              decoration: BoxDecoration(
                color: AppColors.background,
                borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                border: Border.all(color: AppColors.border, style: BorderStyle.solid),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.sm),
                    decoration: const BoxDecoration(
                      color: AppColors.lightGreen,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.add_photo_alternate_rounded, size: 28.0, color: AppColors.primaryGreen),
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    strings.noImageSelected,
                    style: const TextStyle(fontSize: 12.0, color: AppColors.textMuted, fontWeight: FontWeight.w500),
                  ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.md),
          ],

          if (isFailed) ...[
            Container(
              padding: const EdgeInsets.all(AppSpacing.sm),
              decoration: BoxDecoration(
                color: const Color(0xFFFFEBEE),
                borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
              ),
              child: Row(
                children: [
                  const Icon(Icons.error_outline, size: 16.0, color: Color(0xFFC62828)),
                  const SizedBox(width: AppSpacing.xs),
                  Expanded(
                    child: Text(
                      '${strings.text('upload_crop_photo')} - ${strings.retry}',
                      style: const TextStyle(fontSize: 11.0, color: Color(0xFFC62828)),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
          ],

          // Camera & Gallery Buttons
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: isUploading ? null : () => onPickImage(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera_rounded, size: 18.0),
                  label: Text(strings.camera),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.primaryGreen,
                    side: const BorderSide(color: AppColors.primaryGreen, width: 1.5),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: isUploading ? null : () => onPickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library_rounded, size: 18.0),
                  label: Text(strings.gallery),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.textSecondary,
                    side: const BorderSide(color: AppColors.border, width: 1.5),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                    padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: AppSpacing.sm),
          Center(
            child: Text(
              strings.aiCropAssistHint,
              style: const TextStyle(
                fontSize: 12.0,
                color: AppColors.textMuted,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
