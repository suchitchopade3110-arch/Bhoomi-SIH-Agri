import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../data/auth_repository.dart';

class OtpRequestScreen extends ConsumerStatefulWidget {
  const OtpRequestScreen({super.key});

  @override
  ConsumerState<OtpRequestScreen> createState() => _OtpRequestScreenState();
}

class _OtpRequestScreenState extends ConsumerState<OtpRequestScreen> {
  final _formKey = GlobalKey<FormState>();
  final _phoneController = TextEditingController(text: '+919876543210');
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  Future<void> _handleRequestOtp() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final phone = _phoneController.text.trim();

    try {
      final repo = ref.read(authRepositoryProvider);
      final res = await repo.requestOtp(phone);

      if (mounted) {
        final debugOtp = res.debugOtp ?? '';
        final encodedPhone = Uri.encodeComponent(phone);
        context.push('/otp-verify?phone=$encodedPhone&debugOtp=$debugOtp');
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error requesting OTP: ${e.toString().replaceAll('Exception: ', '')}';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('SMS Verification', style: TextStyle(fontWeight: FontWeight.w800)),
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
                        'Request One-Time Code',
                        style: AppTypography.headlineMedium.copyWith(color: AppColors.primaryDeepGreen),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      const Text(
                        'Enter your registered mobile phone number to receive a 6-digit verification code.',
                        style: TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
                      ),
                      const Divider(color: AppColors.divider, height: AppSpacing.xl),

                      Text('Phone Number', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        decoration: InputDecoration(
                          hintText: '+919876543210',
                          prefixIcon: const Icon(Icons.phone_outlined, color: AppColors.primaryGreen),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().length < 10) {
                            return 'Please enter a valid mobile phone number';
                          }
                          return null;
                        },
                      ),

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
                  text: 'Send Verification OTP',
                  isLoading: _isLoading,
                  icon: Icons.sms_rounded,
                  onPressed: _handleRequestOtp,
                ),

                const SizedBox(height: AppSpacing.md),

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Back to ', style: TextStyle(color: AppColors.textMuted, fontSize: 13.0)),
                    TextButton(
                      onPressed: () => context.go('/login'),
                      child: const Text(
                        'Password Sign In',
                        style: TextStyle(color: AppColors.primaryGreen, fontWeight: FontWeight.w800, fontSize: 13.0),
                      ),
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
