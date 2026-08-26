import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../data/auth_repository.dart';
import '../../data/models/auth_models.dart';
import '../providers/auth_providers.dart';

class OtpVerifyScreen extends ConsumerStatefulWidget {
  final String phoneNumber;
  final String? initialDebugOtp;

  const OtpVerifyScreen({
    super.key,
    required this.phoneNumber,
    this.initialDebugOtp,
  });

  @override
  ConsumerState<OtpVerifyScreen> createState() => _OtpVerifyScreenState();
}

class _OtpVerifyScreenState extends ConsumerState<OtpVerifyScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _otpController;
  final _nameController = TextEditingController(text: 'Bhoomi Farmer');
  String? _debugOtp;
  String? _infoMessage;
  String? _errorMessage;
  bool _isResending = false;

  @override
  void initState() {
    super.initState();
    _debugOtp = widget.initialDebugOtp;
    _otpController = TextEditingController(text: _debugOtp != null && _debugOtp!.isNotEmpty ? _debugOtp : '');
  }

  @override
  void dispose() {
    _otpController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _handleVerify() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _errorMessage = null;
      _infoMessage = null;
    });

    final otp = _otpController.text.trim();

    try {
      await ref.read(authStateProvider.notifier).verifyOtp(
            OtpVerifyRequest(
              phoneNumber: widget.phoneNumber,
              otp: otp,
              fullName: _nameController.text.trim(),
              preferredLanguage: 'ta',
            ),
          );

      if (mounted) {
        context.go('/home/f_1');
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Invalid OTP: ${e.toString().replaceAll('Exception: ', '')}';
      });
    }
  }

  Future<void> _handleResendOtp() async {
    setState(() {
      _isResending = true;
      _errorMessage = null;
      _infoMessage = null;
    });

    try {
      final repo = ref.read(authRepositoryProvider);
      final res = await repo.requestOtp(widget.phoneNumber);

      setState(() {
        _debugOtp = res.debugOtp;
        _infoMessage = res.message;
        if (res.debugOtp != null && res.debugOtp!.isNotEmpty) {
          _otpController.text = res.debugOtp!;
        }
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to resend OTP: ${e.toString().replaceAll('Exception: ', '')}';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isResending = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authStateProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Enter OTP Code', style: TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: AppSpacing.md),
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.xl),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Enter 6-Digit OTP',
                        style: AppTypography.headlineMedium.copyWith(color: AppColors.primaryDeepGreen),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        'Enter the verification code sent to ${widget.phoneNumber}.',
                        style: const TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
                      ),
                      const Divider(color: AppColors.divider, height: AppSpacing.xl),

                      // Name Field
                      Text('Full Name', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _nameController,
                        decoration: InputDecoration(
                          hintText: 'e.g. Muthu Kumar',
                          prefixIcon: const Icon(Icons.person_outline_rounded, color: AppColors.primaryGreen),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),

                      // OTP Input Field
                      Text('Verification Code (OTP)', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _otpController,
                        keyboardType: TextInputType.number,
                        maxLength: 6,
                        decoration: InputDecoration(
                          hintText: '123456',
                          prefixIcon: const Icon(Icons.pin_outlined, color: AppColors.primaryGreen),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().length < 6) {
                            return 'Please enter 6-digit OTP code';
                          }
                          return null;
                        },
                      ),

                      if (_infoMessage != null) ...[
                        const SizedBox(height: AppSpacing.sm),
                        Text(
                          _infoMessage!,
                          style: const TextStyle(fontSize: 12.5, color: AppColors.primaryGreen, fontWeight: FontWeight.w600),
                        ),
                      ],

                      if (_debugOtp != null && _debugOtp!.isNotEmpty) ...[
                        const SizedBox(height: AppSpacing.sm),
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.xs + 2),
                          decoration: BoxDecoration(
                            color: AppColors.lightGreen,
                            borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                          ),
                          child: Text(
                            'Debug OTP: $_debugOtp',
                            style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: AppColors.primaryGreen),
                          ),
                        ),
                      ],

                      if (_errorMessage != null) ...[
                        const SizedBox(height: AppSpacing.md),
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.md),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFFEBEE),
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            border: Border.all(color: const Color(0xFFEF9A9A)),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.error_outline_rounded, color: Color(0xFFC62828), size: 20.0),
                              const SizedBox(width: AppSpacing.sm),
                              Expanded(
                                child: Text(
                                  _errorMessage!,
                                  style: const TextStyle(fontSize: 12.5, color: Color(0xFFC62828), fontWeight: FontWeight.w600),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                BhoomiPrimaryButton(
                  text: 'Verify & Sign In',
                  isLoading: authState.isLoading,
                  icon: Icons.check_circle_outline_rounded,
                  onPressed: _handleVerify,
                ),

                const SizedBox(height: AppSpacing.md),

                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    TextButton.icon(
                      onPressed: _isResending ? null : _handleResendOtp,
                      icon: const Icon(Icons.refresh_rounded, size: 16.0),
                      label: Text(_isResending ? 'Resending...' : 'Resend OTP'),
                      style: TextButton.styleFrom(foregroundColor: AppColors.primaryGreen),
                    ),
                    TextButton(
                      onPressed: () => context.pop(),
                      child: const Text('Change Number', style: TextStyle(color: AppColors.textMuted)),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
