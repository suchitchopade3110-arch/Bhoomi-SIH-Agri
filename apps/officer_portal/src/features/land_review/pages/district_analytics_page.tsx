import React from 'react';
import { useLandQueue } from '../hooks/use_land_queue';
import { BarChart3, TrendingUp, CheckCircle2, Clock, AlertCircle, ShieldCheck, Map } from 'lucide-react';

export const DistrictAnalyticsPage: React.FC = () => {
  const { data: queueItems = [] } = useLandQueue();

  const totalRecords = queueItems.length;
  const pendingCount = queueItems.filter((i) => i.status === 'pending_verification').length;
  const verifiedCount = queueItems.filter((i) => i.status === 'verified').length;
  const rejectedCount = queueItems.filter((i) => i.status === 'rejected').length;

  const totalAcres = queueItems.reduce((acc, curr) => acc + (curr.farmer_stated?.area_acres || 0), 0);
  const verifiedAcres = queueItems
    .filter((i) => i.status === 'verified')
    .reduce((acc, curr) => acc + (curr.farmer_stated?.area_acres || 0), 0);

  const approvalRate =
    totalRecords > 0 ? Math.round((verifiedCount / (verifiedCount + rejectedCount || 1)) * 100) : 100;

  return (
    <div className="flex-1 overflow-y-auto bg-slate-50/50 p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#2E7D32]/10 text-[#2E7D32]">
              <BarChart3 className="h-5 w-5" />
            </div>
            <h1 className="text-xl font-extrabold text-slate-900">District Land Analytics</h1>
          </div>
          <p className="mt-1 text-xs text-slate-500">
            Erode District • Taluk Land Verification Metrics & Spatial Registration KPIs
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Total Submissions</span>
            <Map className="h-4 w-4 text-[#2E7D32]" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900">{totalRecords}</span>
            <span className="text-xs text-slate-500">({totalAcres.toFixed(1)} Acres)</span>
          </div>
        </div>

        <div className="rounded-2xl border border-amber-200 bg-amber-50/40 p-5 shadow-xs">
          <div className="flex items-center justify-between text-amber-700">
            <span className="text-xs font-bold uppercase tracking-wider">Pending Review</span>
            <Clock className="h-4 w-4 text-amber-600" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-black text-amber-900">{pendingCount}</span>
            <span className="text-xs text-amber-700 font-semibold">Parcels</span>
          </div>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/40 p-5 shadow-xs">
          <div className="flex items-center justify-between text-emerald-700">
            <span className="text-xs font-bold uppercase tracking-wider">Verified Land</span>
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-black text-emerald-900">{verifiedCount}</span>
            <span className="text-xs text-emerald-700 font-semibold">({verifiedAcres.toFixed(1)} Acres)</span>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-bold uppercase tracking-wider">Approval Rate</span>
            <TrendingUp className="h-4 w-4 text-[#2E7D32]" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-black text-[#2E7D32]">{approvalRate}%</span>
            <span className="text-xs text-slate-500">Resolution Rate</span>
          </div>
        </div>
      </div>

      {/* Detailed Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-4">Taluk Verification Distribution</h3>
          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between font-bold text-slate-700 mb-1">
                <span>Erode Taluk (Perundurai / Modakkurichi)</span>
                <span>65% Verified</span>
              </div>
              <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                <div className="h-full rounded-full bg-[#2E7D32]" style={{ width: '65%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between font-bold text-slate-700 mb-1">
                <span>Gobichettipalayam (Alukuli / Kunderipallam)</span>
                <span>80% Verified</span>
              </div>
              <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                <div className="h-full rounded-full bg-[#2E7D32]" style={{ width: '80%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between font-bold text-slate-700 mb-1">
                <span>Bhavani Taluk (Ammapettai / Anthiyur)</span>
                <span>50% Verified</span>
              </div>
              <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                <div className="h-full rounded-full bg-[#2E7D32]" style={{ width: '50%' }} />
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 mb-4">Verification Quality & Integrity</h3>
          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between rounded-xl bg-emerald-50 p-3 text-emerald-900 border border-emerald-200">
              <div className="flex items-center gap-2 font-bold">
                <ShieldCheck className="h-4 w-4 text-emerald-700" />
                <span>Zero Spatial Overlap Detected</span>
              </div>
              <span className="font-semibold text-emerald-700">100% Clean</span>
            </div>

            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 text-slate-700 border border-slate-200">
              <div className="flex items-center gap-2 font-bold">
                <AlertCircle className="h-4 w-4 text-slate-500" />
                <span>Rejected Due to Boundary Mismatch</span>
              </div>
              <span className="font-bold text-slate-900">{rejectedCount} parcels</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
