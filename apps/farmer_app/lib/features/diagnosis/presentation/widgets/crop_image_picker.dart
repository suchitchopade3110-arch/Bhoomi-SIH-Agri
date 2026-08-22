import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../application/diagnosis_state.dart';

class CropImagePickerWidget extends StatelessWidget {
  final DiagnosisState state;
  final void Function(ImageSource source) onPickImage;

  const CropImagePickerWidget({
    super.key,
    required this.state,
    required this.onPickImage,
  });

  @override
  Widget build(BuildContext context) {
    final hasImage = state.selectedImageBytes != null;
    final isUploading = state.imageUploadStatus == ImageUploadStatus.uploading;
    final isUploaded = state.imageUploadStatus == ImageUploadStatus.uploaded;
    final isFailed = state.imageUploadStatus == ImageUploadStatus.failed;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
        border: Border.all(
          color: isUploaded ? AppColors.primaryGreen : AppColors.border,
          width: isUploaded ? 1.5 : 1.0,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.camera_alt_outlined,
                    size: 18.0,
                    color: isUploaded ? AppColors.primaryGreen : AppColors.textMuted,
                  ),
                  const SizedBox(width: AppSpacing.xs),
                  const Text('Crop Photograph (Optional)', style: AppTypography.titleMedium),
                ],
              ),
              if (isUploaded)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2.0),
                  decoration: BoxDecoration(
                    color: AppColors.primaryGreen.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                  ),
                  child: const Row(
                    children: [
                      Icon(Icons.check_circle, size: 12.0, color: AppColors.primaryGreen),
                      SizedBox(width: 4.0),
                      Text(
                        'Attached',
                        style: TextStyle(fontSize: 10.0, fontWeight: FontWeight.w700, color: AppColors.primaryGreen),
                      ),
                    ],
                  ),
                ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),

          if (hasImage) ...[
            ClipRRect(
              borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
              child: Stack(
                children: [
                  Image.memory(
                    state.selectedImageBytes!,
                    height: 160.0,
                    width: double.infinity,
                    fit: BoxFit.cover,
                  ),
                  if (isUploading)
                    Positioned.fill(
                      child: Container(
                        color: Colors.black45,
                        child: Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const CircularProgressIndicator(color: Colors.white, strokeWidth: 3.0),
                              const SizedBox(height: AppSpacing.sm),
                              Text(
                                'Uploading image... ${(state.imageUploadProgress * 100).toInt()}%',
                                style: const TextStyle(color: Colors.white, fontSize: 12.0, fontWeight: FontWeight.w600),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
          ],

          if (isFailed) ...[
            Container(
              padding: const EdgeInsets.all(AppSpacing.sm),
              decoration: BoxDecoration(
                color: const Color(0xFFFFEBEE),
                borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
              ),
              child: const Row(
                children: [
                  Icon(Icons.error_outline, size: 16.0, color: Color(0xFFC62828)),
                  SizedBox(width: AppSpacing.xs),
                  Text('Upload failed. Tap to re-select.', style: TextStyle(fontSize: 11.0, color: Color(0xFFC62828))),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
          ],

          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: isUploading ? null : () => onPickImage(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera_rounded, size: 16.0),
                  label: const Text('Take Photo'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.primaryGreen,
                    side: const BorderSide(color: AppColors.primaryGreen),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: isUploading ? null : () => onPickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library_rounded, size: 16.0),
                  label: const Text('Choose Photo'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.textSecondary,
                    side: const BorderSide(color: AppColors.border),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
