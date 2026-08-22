import 'package:flutter_test/flutter_test.dart';
import 'package:farmer_app/features/onboarding/data/models/create_farm_request.dart';
import 'package:farmer_app/features/voice/data/models/transcribe_response.dart';
import 'package:farmer_app/features/health/data/models/health_snapshot.dart';
import 'package:farmer_app/features/diagnosis/data/models/diagnosis_response.dart';
import 'package:farmer_app/features/timeline/data/models/timeline_event.dart';
import 'package:farmer_app/features/schemes/data/models/scheme_summary.dart';
import 'package:farmer_app/features/daily_brief/data/models/daily_brief_response.dart';
import 'package:farmer_app/features/updates/data/models/farm_update.dart';

void main() {
  group('BHOOMI Complete Phase 1-5 Contract & Integration Tests', () {
    test('Phase 1: CreateFarmRequest serialization matches exact API contract', () {
      const request = CreateFarmRequest(
        crop: 'samba_paddy',
        areaAcresSelfReported: 2.0,
        growthStage: 'vegetative',
        soilType: 'clay_loam',
        irrigationAccess: 'canal',
        season: 'samba',
      );

      final json = request.toJson();
      expect(json['crop'], equals('samba_paddy'));
      expect(json['area_acres_self_reported'], equals(2.0));
      expect(json['soil_type'], equals('clay_loam'));
    });

    test('Phase 2: TranscribeResponse parses confidence and intent', () {
      final response = TranscribeResponse.fromJson({
        'text': 'Two acres of paddy',
        'confidence': 0.92,
        'lang': 'en-IN',
        'needs_confirmation': true,
      });
      expect(response.confidence, equals(0.92));
      expect(response.isHighConfidence, isTrue);
    });

    test('Phase 2: HealthSnapshot preserves null composite score as Unrated', () {
      final snapshot = HealthSnapshot.fromJson({
        'score': null,
        'band': 'unrated',
        'sub_indices': {
          'environmental_suitability': 0.70,
          'resource_adequacy': 0.80,
        },
      });
      expect(snapshot.score, isNull);
      expect(snapshot.band, equals('unrated'));
    });

    test('Phase 3: DiagnosisResponse parses structured advice, checklist & sources', () {
      final response = DiagnosisResponse.fromJson({
        'diagnosis_id': 'diag_101',
        'farm_id': 'f_1',
        'possible_issue': 'Bacterial Leaf Blight',
        'confidence_level': 'high',
        'symptoms_to_check': ['Yellow margins', 'Bacterial ooze beads'],
        'actions': ['Drain excess standing water', 'Apply certified bactericide'],
        'sources': [
          {
            'title': 'TNAU Agritech Portal',
            'organization': 'Tamil Nadu Agricultural University',
          }
        ],
        'can_escalate': true,
        'created_at': '2026-08-21T08:30:00Z',
      });
      expect(response.possibleIssue, equals('Bacterial Leaf Blight'));
      expect(response.isHighConfidence, isTrue);
      expect(response.symptomsToCheck.length, equals(2));
      expect(response.sources.first.organization, contains('Tamil Nadu'));
    });

    test('Phase 3: TimelineEvent parses chronological history', () {
      final event = TimelineEvent.fromJson({
        'event_id': 'evt_1',
        'event_type': 'diagnosis',
        'title': 'Crop problem reported',
        'summary': 'Bacterial Leaf Blight diagnosed',
        'status': 'monitoring',
        'timestamp': '2026-08-21T08:30:00Z',
      });
      expect(event.eventId, equals('evt_1'));
      expect(event.eventType, equals('diagnosis'));
    });

    test('Phase 4: SchemeSummary and SchemeDetail serialize correctly', () {
      final summary = SchemeSummary.fromJson({
        'scheme_id': 'sch_pmkisan',
        'title': 'PM-KISAN Samman Nidhi',
        'short_description': '₹6,000 per year income support',
        'match_status': 'likely_relevant',
        'match_explanation': 'Applicable for registered agricultural land holdings.',
      });
      expect(summary.schemeId, equals('sch_pmkisan'));
      expect(summary.isLikelyRelevant, isTrue);

      final detail = SchemeDetail.fromJson({
        'scheme_id': 'sch_pmkisan',
        'title': 'PM-KISAN',
        'department': 'Ministry of Agriculture',
        'description': 'Direct income support',
        'benefits': ['₹2,000 every 4 months'],
        'official_url': 'https://pmkisan.gov.in',
      });
      expect(detail.officialUrl, equals('https://pmkisan.gov.in'));
    });

    test('Phase 4: DailyBriefResponse parses prioritized brief without frontend computation', () {
      final brief = DailyBriefResponse.fromJson({
        'brief_date': '2026-08-21',
        'crop': 'Paddy',
        'growth_stage': 'Vegetative',
        'important_action': 'Apply scheduled 2,200 L irrigation',
        'advisory_summary': 'Favorable fieldwork window today',
      });
      expect(brief.crop, equals('Paddy'));
      expect(brief.importantAction, contains('2,200 L'));
    });

    test('Phase 4: FarmUpdate parses update type and action route', () {
      final update = FarmUpdate.fromJson({
        'update_id': 'up_1',
        'update_type': 'advisory',
        'title': 'New Pest Alert',
        'description': 'Leaf blight reported in Erode taluk',
        'timestamp': '2026-08-21T07:00:00Z',
        'action_route': '/health/f_1',
      });
      expect(update.updateType, equals('advisory'));
      expect(update.actionRoute, equals('/health/f_1'));
    });
  });
}
