import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';
import '../../app/theme/app_typography.dart';
import '../connectivity/network_state.dart';

class DegradedNetworkBanner extends StatelessWidget {
  final NetworkState networkState;

  const DegradedNetworkBanner({
    super.key,
    required this.networkState,
  });

  @override
  Widget build(BuildContext context) {
    if (networkState.isOnline) {
      return const SizedBox.shrink();
    }

    final isDegraded = networkState.isDegraded;
    final bgColor = isDegraded ? AppColors.networkDegradedBg : const Color(0xFFFFEBEE);
    final borderColor = isDegraded ? AppColors.networkDegradedBorder : const Color(0xFFFFCDD2);
    final textColor = isDegraded ? AppColors.networkDegradedText : const Color(0xFFC62828);
    final icon = isDegraded ? Icons.wifi_protected_setup : Icons.wifi_off_rounded;
    final message = isDegraded
        ? (networkState.message ?? "Weak connection. We'll keep the experience lightweight.")
        : (networkState.message ?? "No connection. Actions will retry when network returns.");

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm + 2,
      ),
      decoration: BoxDecoration(
        color: bgColor,
        border: Border(
          bottom: BorderSide(color: borderColor, width: 1.0),
        ),
      ),
      child: Row(
        children: [
          Icon(icon, size: 18.0, color: textColor),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Text(
              message,
              style: AppTypography.labelMedium.copyWith(
                color: textColor,
                fontWeight: FontWeight.w600,
                fontSize: 13.0,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
