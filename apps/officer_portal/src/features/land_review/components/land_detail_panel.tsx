import React, { useState } from 'react';
import { LandQueueItem } from '../types/land.types';
import { Badge } from '../../../components/ui/badge';
import { Button } from '../../../components/ui/button';
import { BoundaryMap } from './boundary_map';
import { LandReviewActions } from './land_review_actions';
import {
  FileCheck2,
  Layers,
  CheckCircle2,
  XCircle,
} from 'lucide-react';

interface LandDetailPanelProps {
  selectedRecord: LandQueueItem | null;
}

export const LandDetailPanel: React.FC<LandDetailPanelProps> = ({ selectedRecord }) => {
  const [successNotice, setSuccessNotice] = useState<string | null>(null);

  if (!selectedRecord) {
    return (
      <div className="flex h-full flex-col items-center justify-center bg-slate-50/50 p-8 text-center">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <FileCheck2 className="mx-auto h-12 w-12 text-[#2E7D32]/40" />
          <h3 className="mt-4 text-base font-bold text-slate-800">
            No Land Record Selected
          </h3>
          <p className="mt-1 max-w-sm text-xs text-slate-500">
            Select a land parcel record from the queue on the left to review farmer-stated survey details, inspect OpenStreetMap boundary, and issue official verification.
          </p>
        </div>
      </div>
    );
  }

  const isPending = selectedRecord.status === 'pending_verification' || selectedRecord.status === 'under_review' || selectedRecord.status === 'submitted';
  const isVerified = selectedRecord.status === 'verified';
  const isRejected = selectedRecord.status === 'rejected';

  return (
    <div className="flex h-full flex-col overflow-y-auto bg-slate-50/30 p-6 lg:p-8">
      {/* Verification Success Notice */}
      {successNotice && (
        <div className="mb-6 flex items-center justify-between rounded-xl border border-emerald-300 bg-emerald-50 p-4 text-emerald-900 shadow-sm">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="h-6 w-6 text-emerald-600" />
            <div>
              <h4 className="font-extrabold text-sm text-emerald-900">{successNotice}</h4>
              <p className="text-xs text-emerald-800">
                Record updated for Survey No. {selectedRecord.farmer_stated.survey_no}.
              </p>
            </div>
          </div>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setSuccessNotice(null)}
            className="text-emerald-800 hover:bg-emerald-100"
          >
            Dismiss
          </Button>
        </div>
      )}

      {/* Main Detail Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-4 border-b border-slate-100 pb-5">
          <div>
            <div className="flex items-center gap-2">
              <span className="rounded bg-[#2E7D32]/10 px-2 py-0.5 text-xs font-extrabold text-[#2E7D32]">
                SURVEY NO.
              </span>
              <Badge variant={isVerified ? 'verified' : isRejected ? 'neutral' : 'pending'}>
                {isVerified ? 'Verified' : isRejected ? 'Rejected' : 'Pending Verification'}
              </Badge>
            </div>
            <h1 className="mt-2 text-2xl font-black text-slate-900">
              {selectedRecord.farmer_stated.survey_no}
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Land Record ID: <span className="font-mono font-semibold text-slate-700">{selectedRecord.land_record_id}</span>
            </p>
          </div>

          {/* Action CTAs */}
          {isPending ? (
            <LandReviewActions
              record={selectedRecord}
              onSuccess={() => setSuccessNotice('Review Decision Recorded Successfully')}
            />
          ) : isVerified ? (
            <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2.5 text-xs font-bold text-emerald-800">
              <CheckCircle2 className="h-5 w-5 text-emerald-600" />
              <span>Verified & Signed</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 rounded-xl border border-red-200 bg-red-50 px-4 py-2.5 text-xs font-bold text-red-800">
              <XCircle className="h-5 w-5 text-red-600" />
              <span>Verification Rejected</span>
            </div>
          )}
        </div>

        {/* Contract Data Grid */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="rounded-xl border border-slate-100 bg-slate-50/80 p-4">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Self-Reported Area
            </div>
            <div className="mt-1 flex items-baseline gap-1">
              <span className="text-2xl font-extrabold text-slate-900">
                {selectedRecord.farmer_stated.area_acres}
              </span>
              <span className="text-xs font-semibold text-slate-500">Acres</span>
            </div>
          </div>

          <div className="rounded-xl border border-slate-100 bg-slate-50/80 p-4">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Farm Identifier
            </div>
            <div className="mt-1 font-mono text-lg font-bold text-slate-800">
              {selectedRecord.farm_id}
            </div>
          </div>

          <div className="rounded-xl border border-slate-100 bg-slate-50/80 p-4">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Submission Timestamp
            </div>
            <div className="mt-1 text-sm font-semibold text-slate-800">
              {new Date(selectedRecord.submitted_at).toLocaleString()}
            </div>
          </div>
        </div>
      </div>

      {/* Interactive OpenStreetMap Leaflet Boundary Viewer */}
      <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#2E7D32]/10 text-[#2E7D32]">
              <Layers className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">OpenStreetMap Parcel Boundary</h3>
              <p className="text-[11px] text-slate-500">
                Interactive map rendering farmer-submitted polygon GeoJSON coordinates
              </p>
            </div>
          </div>
          <span className="rounded-md bg-slate-100 px-2 py-1 text-[11px] font-mono font-semibold text-slate-600">
            {selectedRecord.boundary_geojson?.type || 'No GeoJSON'}
          </span>
        </div>

        <div className="mt-4">
          <BoundaryMap
            boundaryGeojson={selectedRecord.boundary_geojson}
            surveyNo={selectedRecord.farmer_stated.survey_no}
            areaAcres={selectedRecord.farmer_stated.area_acres}
          />
        </div>
      </div>
    </div>
  );
};
