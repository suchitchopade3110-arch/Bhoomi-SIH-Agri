import 'package:flutter_test/flutter_test.dart';
import 'package:farmer_app/shared/constants/api_constants.dart';
import 'package:farmer_app/features/auth/data/models/auth_models.dart';
import 'package:farmer_app/features/voice/data/models/confirm_field_models.dart';
import 'package:farmer_app/features/onboarding/data/models/farm_update_models.dart';
import 'package:farmer_app/features/guidance/data/models/guidance_card_model.dart';
import 'package:farmer_app/features/alerts/data/models/alert_models.dart';
import 'package:farmer_app/features/treatments/data/models/treatment_efficacy_model.dart';
import 'package:farmer_app/features/escalation/data/models/case_pdf_payload_model.dart';
import 'package:farmer_app/features/onboarding/data/models/farm_model.dart';
import 'package:farmer_app/features/system/data/models/system_health_model.dart';

void main() {
  group('Bhoomi Missing Endpoints Integration Tests', () {
    test('1. Authentication Schemas match backend API contract', () {
      expect(ApiConstants.authRegister, '/api/v1/auth/register');
      expect(ApiConstants.authLogin, '/api/v1/auth/login');
      expect(ApiConstants.authMe, '/api/v1/auth/me');
      expect(ApiConstants.authOtpRequest, '/api/v1/auth/otp/request');
      expect(ApiConstants.authOtpVerify, '/api/v1/auth/otp/verify');

      final regReq = const UserRegisterRequest(
        phoneNumber: '+919876543210',
        fullName: 'Muthu',
        password: 'Password123!',
      ).toJson();
      expect(regReq['phone_number'], '+919876543210');
      expect(regReq['role'], 'farmer');
      expect(regReq['preferred_language'], 'ta');

      final token = TokenResponse.fromJson({
        'access_token': 'test_token_abc',
        'token_type': 'bearer',
        'expires_in': 3600,
        'user_id': 'u123',
        'role': 'farmer',
      });
      expect(token.accessToken, 'test_token_abc');
      expect(token.expiresIn, 3600);
      expect(token.role, 'farmer');

      final user = UserResponse.fromJson({
        'id': 'u123',
        'phone_number': '+919876543210',
        'full_name': 'Muthu',
        'role': 'farmer',
        'preferred_language': 'ta',
      });
      expect(user.id, 'u123');
      expect(user.fullName, 'Muthu');
    });

    test('2. Voice Confirm Schemas match backend contract', () {
      expect(ApiConstants.voiceConfirm, '/api/v1/voice/confirm');

      final req = const ConfirmFieldRequest(
        field: 'crop',
        confirmedValue: 'samba_paddy',
        isConfirmed: true,
      ).toJson();
      expect(req['field'], 'crop');
      expect(req['is_confirmed'], true);

      final res = ConfirmFieldResponse.fromJson({
        'status': 'committed',
        'field': 'crop',
        'final_value': 'samba_paddy',
        'message': 'Saved successfully',
      });
      expect(res.status, 'committed');
      expect(res.finalValue, 'samba_paddy');
    });

    test('3. Farm Update & Link Land Schemas match backend contract', () {
      expect(ApiConstants.updateFarm('farm_1'), '/api/v1/farms/farm_1');
      expect(ApiConstants.farmLandLink('farm_1'), '/api/v1/farms/farm_1/land');
      expect(ApiConstants.farmScopedSchemes('farm_1'), '/api/v1/farms/farm_1/schemes');

      final updateReq = const FarmUpdateRequest(
        primaryCrop: 'samba_paddy',
        growthStage: 'vegetative',
      ).toJson();
      expect(updateReq['primary_crop'], 'samba_paddy');
      expect(updateReq['growth_stage'], 'vegetative');

      final landReq = const ThinLandSubmissionRequest(
        surveyNumber: '142/3B',
      ).toJson();
      expect(landReq['survey_number'], '142/3B');

      final landRes = ThinLandSubmissionResponse.fromJson({
        'farm_id': 'farm_1',
        'survey_number': '142/3B',
        'status': 'pending_verification',
      });
      expect(landRes.farmId, 'farm_1');
      expect(landRes.status, 'pending_verification');
    });

    test('4. Guidance Cards Schemas match backend contract', () {
      expect(ApiConstants.guidanceList, '/api/v1/guidance');
      expect(ApiConstants.cropGuidance('samba_paddy'), '/api/v1/guidance/samba_paddy');

      final card = GuidanceCardModel.fromJson({
        'crop': 'samba_paddy',
        'problem_type': 'disease',
        'problem_label': 'bacterial_leaf_blight',
        'title': 'Bacterial Leaf Blight (BLB) Containment',
        'containment_advice': 'Drain standing water immediately.',
        'what_to_avoid': 'Do not apply excess urea.',
        'immediate_actions': ['Drain water for 3-4 days'],
        'expert_trigger': 'If lesion spreads rapidly',
      });
      expect(card.crop, 'samba_paddy');
      expect(card.immediateActions.length, 1);
      expect(card.title, contains('BLB'));
    });

    test('5. Early-Warning Alerts Schemas match backend contract', () {
      expect(ApiConstants.farmAlerts('farm_1'), '/api/v1/farms/farm_1/alerts');
      expect(ApiConstants.alertAcknowledge('alert_1'), '/api/v1/alerts/alert_1/acknowledge');

      final farmAlerts = FarmAlertsResponseModel.fromJson({
        'farm_id': 'farm_1',
        'active_alerts': [
          {
            'alert_id': 'a1',
            'pathogen_name': 'BLB',
            'severity': 'warning',
            'trigger_reason': 'High humidity',
            'preventative_action': 'Drain water',
            'inspection_tasks': ['Check border rows'],
            'spoken_summary': 'BLB alert in area',
            'created_at': '2026-08-25T10:00:00Z',
            'expires_at': '2026-08-28T10:00:00Z',
          }
        ],
      });
      expect(farmAlerts.activeAlerts.length, 1);
      expect(farmAlerts.activeAlerts.first.pathogenName, 'BLB');

      final ackRes = AlertAcknowledgeResponse.fromJson({
        'status': 'acknowledged',
        'alert_id': 'a1',
      });
      expect(ackRes.status, 'acknowledged');
      expect(ackRes.alertId, 'a1');
    });

    test('6. Treatment Efficacy Schemas match backend contract', () {
      expect(ApiConstants.treatmentEfficacy('trt_copper'), '/api/v1/treatments/trt_copper/efficacy');

      final efficacy = TreatmentEfficacyModel.fromJson({
        'treatment_id': 'trt_copper',
        'pathogen': 'bacterial_leaf_blight',
        'crop': 'samba_paddy',
        'region': 'Erode',
        'status': 'statistically_significant',
        'sample_size': 15,
        'min_sample_threshold': 10,
        'efficacy_percentage': 88.5,
        'avg_days_to_recovery': 6.0,
      });
      expect(efficacy.status, 'statistically_significant');
      expect(efficacy.sampleSize, 15);
      expect(efficacy.efficacyPercentage, 88.5);
    });

    test('7. Agronomist PDF Payload Schemas match backend contract', () {
      expect(ApiConstants.agronomistCasePdfPayload('esc_1'), '/api/v1/agronomist/case/esc_1/pdf-payload');

      final pdfPayload = CasePDFPayloadModel.fromJson({
        'case_id': 'esc_1',
        'farm_id': 'f1',
        'farmer_name': 'Muthu',
        'village': 'Perundurai',
        'district': 'Erode',
        'severity': 'early',
        'status': 'escalated',
        'generated_at': '2026-08-25T12:00:00Z',
        'bundle': {
          'crop': 'samba_paddy',
          'region': 'Erode',
          'growth_stage': 'vegetative',
          'problem_history': [],
          'images': [],
          'treatments_tried': [],
          'followup_trend': 'mild symptoms',
          'current_advisory': 'Awaiting expert opinion',
        },
        'summary_headline': 'Samba Paddy Early Escalation',
      });
      expect(pdfPayload.caseId, 'esc_1');
      expect(pdfPayload.bundle.crop, 'samba_paddy');
      expect(pdfPayload.farmerName, 'Muthu');
    });

    test('8. System Health Schemas match backend contract', () {
      expect(ApiConstants.systemHealth, '/api/v1/system/health');

      final health = SystemHealthModel.fromJson({
        'db': 'ok',
        'pgvector': 'ok',
        'corpus_docs': 8,
        'corpus_chunks': 120,
        'demo_farm': 'seeded',
        'embedding_provider_configured': 'stub',
        'rag_relevance_threshold_active': 0.18,
        'embedding_method_verified': 'hash',
      });
      expect(health.db, 'ok');
      expect(health.corpusDocs, 8);
      expect(health.ragRelevanceThresholdActive, 0.18);
    });

    test('9. Multi-Farm List Schemas match backend contract', () {
      expect(ApiConstants.farms, '/api/v1/farms');

      final farm = FarmModel.fromJson({
        'id': 'f_erode_01',
        'farm_name': 'Cauvery Delta Paddy',
        'farmer_id': 'u123',
        'village': 'Perundurai',
        'taluk': 'Erode',
        'district': 'Erode',
        'state': 'Tamil Nadu',
        'primary_crop': 'Samba Paddy',
        'growth_stage': 'vegetative',
        'soil_type': 'Clay Loam',
        'total_area_acres': 2.5,
        'survey_number': '104/2A',
        'land_status': 'verified',
      });

      expect(farm.id, 'f_erode_01');
      expect(farm.farmName, 'Cauvery Delta Paddy');
      expect(farm.village, 'Perundurai');
      expect(farm.district, 'Erode');
      expect(farm.totalAreaAcres, 2.5);
      expect(farm.landStatus, 'verified');
    });
  });
}
