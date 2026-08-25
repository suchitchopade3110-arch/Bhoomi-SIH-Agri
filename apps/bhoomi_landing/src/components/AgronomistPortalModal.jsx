import React, { useEffect, useState } from 'react';
import {
  X,
  UserCheck,
  CheckCircle2,
  Sparkles,
  Send,
  Loader2,
} from 'lucide-react';
import { getAgronomistQueue, resolveAgronomistCase } from '../api/bhoomi_api';
import { AGRONOMIST_CASE_QUEUE } from '../data/farmStore';

export default function AgronomistPortalModal({ isOpen, onClose }) {
  const [cases, setCases] = useState(null);
  const [isLive, setIsLive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState(null);
  const [treatmentText, setTreatmentText] = useState(
    'Foliar spray of Streptocycline (100 mg/L) + Copper Hydroxide (2.0 g/L). Drain standing water for 48 hours. Withhold Urea application until next check-in.'
  );
  const [isResolved, setIsResolved] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    let cancelled = false;
    setLoading(true);
    setIsResolved(false);

    getAgronomistQueue().then((live) => {
      if (cancelled) return;
      if (live && live.length > 0) {
        setCases(live);
        setIsLive(true);
        setSelectedCase(live[0]);
      } else {
        setCases(AGRONOMIST_CASE_QUEUE);
        setIsLive(false);
        setSelectedCase(AGRONOMIST_CASE_QUEUE[0]);
      }
      setLoading(false);
    });

    return () => {
      cancelled = true;
    };
  }, [isOpen]);

  if (!isOpen || !selectedCase) return null;

  const handleResolve = async () => {
    setIsSubmitting(true);
    if (isLive) {
      await resolveAgronomistCase({
        escalationId: selectedCase.escalation_id,
        diagnosis: selectedCase.crop ? `Confirmed field diagnosis for ${selectedCase.crop}` : 'Confirmed field diagnosis',
        advice: treatmentText,
        prescribedInputs: treatmentText.split('.').map((s) => s.trim()).filter(Boolean),
      });
    }
    setIsSubmitting(false);
    setIsResolved(true);
    setCases((prev) =>
      prev.map((c) =>
        (c.escalation_id || c.id) === (selectedCase.escalation_id || selectedCase.id)
          ? { ...c, priority: 'RESOLVED', status: 'resolved' }
          : c
      )
    );
  };

  // Normalize field names across live schema (AgronomistQueueItem) and the
  // local demo shape (AGRONOMIST_CASE_QUEUE) so the JSX below is uniform.
  const farmerName = selectedCase.farmer_name || selectedCase.farmerName;
  const location = selectedCase.village || selectedCase.farmLocation;
  const healthScore = selectedCase.health_score ?? selectedCase.currentHealthScore;
  const severity = selectedCase.severity || selectedCase.followUpTrend;
  const crop = selectedCase.crop || '';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-3xl bg-slate-900 text-white border border-sky-500/40 shadow-2xl p-6 sm:p-8">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-sky-500/20 border border-sky-400/40 flex items-center justify-center">
              <UserCheck className="w-5 h-5 text-sky-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-xl font-bold text-white font-display">KVK Agronomist Escalation Portal</h3>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-950 text-sky-300 border border-sky-600/40 font-mono">
                  PRD §5.11 SLA Target &lt; 3 min
                </span>
              </div>
              <p className="text-xs text-slate-400">
                {loading
                  ? 'Loading case queue…'
                  : isLive
                    ? 'Live data from the Bhoomi API (GET /api/v1/agronomist/queue)'
                    : 'Backend unreachable — showing bundled demo data'}
              </p>
            </div>
          </div>

          <button onClick={onClose} className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors">
            <X className="w-6 h-6" />
          </button>
        </div>

        {isResolved && (
          <div className="my-4 p-4 rounded-2xl bg-emerald-950 border border-emerald-500/50 text-lime-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>
              {isLive
                ? 'Prescription dispatched via POST /api/v1/agronomist/resolve. Farm health score recomputing.'
                : `Prescription dispatched to ${farmerName}'s Tamil voice companion.`}
            </span>
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-20 text-slate-500">
            <Loader2 className="w-6 h-6 animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 mt-6">
            <div className="md:col-span-4 space-y-3">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Active Triage Queue</p>

              <div className="space-y-2">
                {cases.map((c) => {
                  const id = c.escalation_id || c.id;
                  const selectedId = selectedCase.escalation_id || selectedCase.id;
                  return (
                    <div
                      key={id}
                      onClick={() => {
                        setSelectedCase(c);
                        setIsResolved(false);
                      }}
                      className={`p-4 rounded-2xl border cursor-pointer transition-colors ${
                        id === selectedId ? 'border-sky-500/40 bg-sky-950/40' : 'border-slate-800 bg-slate-950/40 hover:border-slate-700'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-sm text-white">{c.farmer_name || c.farmerName}</span>
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-950 text-rose-300 border border-rose-600">
                          {c.priority || c.severity}
                        </span>
                      </div>
                      <p className="text-xs text-sky-300 font-semibold">{c.crop || c.issueTitle}</p>
                      <p className="text-[11px] text-slate-400 mt-1 font-mono">Score: {c.health_score ?? c.currentHealthScore}</p>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="md:col-span-8 space-y-5">
              <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <span className="text-xs font-bold uppercase text-sky-300 font-mono">Compiled Auto-Case Summary</span>
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-slate-500 block">Farmer & Location</span>
                    <span className="font-bold text-white">
                      {farmerName} ({location})
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Crop & Health Score</span>
                    <span className="font-bold text-white">
                      {crop} · {healthScore}
                    </span>
                  </div>
                  <div className="col-span-2">
                    <span className="text-slate-500 block">Severity / Trend</span>
                    <span className="font-bold text-rose-400">{severity}</span>
                  </div>
                </div>

                <div className="pt-2 space-y-2">
                  <label className="text-xs font-bold text-lime-300 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    Agronomist Recommended Prescription:
                  </label>
                  <textarea
                    value={treatmentText}
                    onChange={(e) => setTreatmentText(e.target.value)}
                    rows={3}
                    className="w-full p-3 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white focus:border-sky-500 focus:outline-none"
                  />
                </div>

                <button
                  onClick={handleResolve}
                  disabled={isResolved || isSubmitting}
                  className="w-full btn btn-primary py-3 text-xs font-bold gap-2 bg-sky-700 hover:bg-sky-600 disabled:opacity-50 flex items-center justify-center"
                >
                  {isSubmitting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4 text-lime-300" />
                  )}
                  {isResolved ? 'Case Resolved & Logged' : 'Submit Prescription & Update Health Score'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
