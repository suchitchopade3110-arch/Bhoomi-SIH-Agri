import React, { useEffect, useState } from 'react';
import { kvkApi } from '../../../api/kvk_api';
import { HealthSnapshot } from '../types/case.types';
import { Activity, RefreshCw, AlertCircle, ShieldAlert } from 'lucide-react';
import { Button } from '../../../components/ui/button';

interface TreatmentEfficacyCardProps {
  farmId: string;
}

export const TreatmentEfficacyCard: React.FC<TreatmentEfficacyCardProps> = ({ farmId }) => {
  const [snapshot, setSnapshot] = useState<HealthSnapshot | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = async () => {
    if (!farmId) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await kvkApi.getFarmHealth(farmId);
      setSnapshot(data);
    } catch (err: any) {
      setError(err?.message || 'Unable to fetch farm health and treatment metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, [farmId]);

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs animate-pulse space-y-3">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="h-4 w-40 bg-slate-200 rounded" />
          <div className="h-4 w-16 bg-slate-200 rounded-full" />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2">
          <div className="h-14 bg-slate-100 rounded-xl" />
          <div className="h-14 bg-slate-100 rounded-xl" />
          <div className="h-14 bg-slate-100 rounded-xl" />
          <div className="h-14 bg-slate-100 rounded-xl" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-4 text-xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-amber-900 font-bold">
            <AlertCircle className="h-4 w-4 text-amber-600" />
            <span>Farm Health & Treatment Response</span>
          </div>
          <Button
            size="sm"
            variant="outline"
            onClick={fetchHealth}
            className="h-7 text-[11px] gap-1 border-amber-300 hover:bg-amber-100"
          >
            <RefreshCw className="h-3 w-3" />
            <span>Retry</span>
          </Button>
        </div>
        <p className="mt-1 text-amber-800 text-[11px]">{error}</p>
      </div>
    );
  }

  if (!snapshot) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs text-xs text-slate-500 text-center">
        <ShieldAlert className="h-5 w-5 mx-auto text-slate-400 mb-1" />
        No health snapshot or treatment efficacy data recorded yet for this farm.
      </div>
    );
  }

  const treatmentScore = snapshot.treatment_response ?? 70;
  const compositeScore = snapshot.composite_score;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
            <Activity className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Treatment Response & Farm Health</h3>
            <p className="text-[11px] text-slate-500">Continuous diagnostic recovery tracking</p>
          </div>
        </div>
        <span className="rounded-full bg-emerald-50 px-2.5 py-0.5 text-[11px] font-extrabold uppercase text-emerald-700 border border-emerald-200/60">
          {snapshot.health_band || 'Good'}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        {/* Treatment Response Subindex */}
        <div className="rounded-xl bg-emerald-50/70 border border-emerald-200/60 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-800">
            Treatment Response
          </div>
          <div className="mt-1 flex items-baseline gap-1">
            <span className="text-lg font-black text-emerald-900">{treatmentScore}</span>
            <span className="text-[10px] text-emerald-700 font-semibold">/ 100</span>
          </div>
          <p className="mt-0.5 text-[10px] text-emerald-700">Advisory outcome recovery</p>
        </div>

        {/* Composite Health Score */}
        <div className="rounded-xl bg-slate-50 border border-slate-100 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Composite Health
          </div>
          <div className="mt-1 flex items-baseline gap-1">
            <span className="text-lg font-black text-slate-900">
              {compositeScore !== null ? compositeScore : 'Unrated'}
            </span>
            {compositeScore !== null && (
              <span className="text-[10px] text-slate-500 font-semibold">/ 100</span>
            )}
          </div>
          <p className="mt-0.5 text-[10px] text-slate-500">Transparent health index</p>
        </div>

        {/* Environmental Suitability */}
        <div className="rounded-xl bg-slate-50 border border-slate-100 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Environment Match
          </div>
          <div className="mt-1 flex items-baseline gap-1">
            <span className="text-lg font-black text-slate-900">
              {snapshot.environmental_suitability ?? 85}
            </span>
            <span className="text-[10px] text-slate-500 font-semibold">/ 100</span>
          </div>
          <p className="mt-0.5 text-[10px] text-slate-500">Weather & microclimate</p>
        </div>

        {/* Active Problem Load */}
        <div className="rounded-xl bg-slate-50 border border-slate-100 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Problem Load Index
          </div>
          <div className="mt-1 flex items-baseline gap-1">
            <span className="text-lg font-black text-slate-900">
              {snapshot.active_problem_load ?? 78}
            </span>
            <span className="text-[10px] text-slate-500 font-semibold">/ 100</span>
          </div>
          <p className="mt-0.5 text-[10px] text-slate-500">Severity load on crop</p>
        </div>
      </div>
    </div>
  );
};
