import React from 'react';
import { HelpCircle, BookOpen, CheckCircle, AlertTriangle, FileText } from 'lucide-react';

export const HelpGuidelinesPage: React.FC = () => {
  return (
    <div className="flex-1 overflow-y-auto bg-slate-50/50 p-6 lg:p-8 space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#2E7D32]/10 text-[#2E7D32]">
            <HelpCircle className="h-5 w-5" />
          </div>
          <h1 className="text-xl font-extrabold text-slate-900">Land Verification Guidelines</h1>
        </div>
        <p className="mt-1 text-xs text-slate-500">
          Standard Operating Procedures (SOP) for Revenue Officers & Land Parcel Authentication
        </p>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* SOP 1: Spatial Boundary Inspection */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-3">
            <BookOpen className="h-4 w-4 text-[#2E7D32]" />
            <h3 className="text-sm font-bold text-slate-900">1. Spatial Boundary Inspection</h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Verify the farmer-submitted GeoJSON polygon boundaries on OpenStreetMap against official Tamil Nadu Revenue (e-Adangal / Patta) records. Ensure the registered survey number corresponds precisely with the cadastral plot layout.
          </p>
          <div className="mt-3 rounded-xl bg-emerald-50 p-3 text-xs text-emerald-900 border border-emerald-200 flex items-start gap-2">
            <CheckCircle className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
            <span>Check that self-reported acreage matches computed polygon surface area within ±5% tolerance.</span>
          </div>
        </div>

        {/* SOP 2: Rejection & Discrepancy Protocols */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-3">
            <AlertTriangle className="h-4 w-4 text-amber-600" />
            <h3 className="text-sm font-bold text-slate-900">2. Discrepancy Protocols</h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            In the event of boundary overlap, unverified survey subdivision (e.g. 142/3B vs 142/3), or conflicting ownership records, reject the submission with clear clinical remarks so the farmer companion app prompts for corrected survey inputs.
          </p>
        </div>

        {/* SOP 3: SIH 2025 Verification Workflow */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-3">
            <FileText className="h-4 w-4 text-[#2E7D32]" />
            <h3 className="text-sm font-bold text-slate-900">3. Human-in-the-Loop Revenue Workflow</h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            BHOOMI follows a strict Human-in-the-Loop policy. Automated algorithms ingest survey submissions, but final parcel certification requires official officer authentication via this portal.
          </p>
        </div>
      </div>
    </div>
  );
};
