import React, { useState } from 'react';
import { 
  X, 
  UserCheck, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  Clock, 
  Sparkles,
  Send,
  ArrowRight
} from 'lucide-react';
import { AGRONOMIST_CASE_QUEUE } from '../data/farmStore';

export default function AgronomistPortalModal({ isOpen, onClose }) {
  const [cases, setCases] = useState(AGRONOMIST_CASE_QUEUE);
  const [selectedCase, setSelectedCase] = useState(cases[0]);
  const [treatmentText, setTreatmentText] = useState(
    'Foliar spray of Streptocycline (100 mg/L) + Copper Hydroxide (2.0 g/L). Drain standing water for 48 hours. Withhold Urea application until next check-in.'
  );
  const [isResolved, setIsResolved] = useState(false);

  if (!isOpen) return null;

  const handleResolve = () => {
    setIsResolved(true);
    setCases(cases.map(c => c.id === selectedCase.id ? { ...c, priority: 'RESOLVED' } : c));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-3xl bg-slate-900 text-white border border-sky-500/40 shadow-2xl p-6 sm:p-8">
        
        {/* Modal Header */}
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
              <p className="text-xs text-slate-400">Pre-Analyzed Farm Case Triage & Prescription Desk</p>
            </div>
          </div>

          <button 
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Resolution Banner */}
        {isResolved && (
          <div className="my-4 p-4 rounded-2xl bg-emerald-950 border border-emerald-500/50 text-lime-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>Prescription dispatched to Ramesh's Tamil voice companion. Farm Health recovering to 86/100.</span>
          </div>
        )}

        {/* Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 mt-6">
          
          {/* Left Column: Triage Queue */}
          <div className="md:col-span-4 space-y-3">
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Active Triage Queue (Position #1)
            </p>

            <div className="space-y-2">
              {cases.map((c) => (
                <div
                  key={c.id}
                  className="p-4 rounded-2xl border border-sky-500/40 bg-sky-950/40 cursor-pointer"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-sm text-white">{c.farmerName}</span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-950 text-rose-300 border border-rose-600">
                      {c.priority}
                    </span>
                  </div>
                  <p className="text-xs text-sky-300 font-semibold">{c.issueTitle}</p>
                  <p className="text-[11px] text-slate-400 mt-1 font-mono">Score: {c.currentHealthScore}</p>
                </div>
              ))}
            </div>

            <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-400 space-y-1">
              <p className="font-bold text-slate-300">Next-Available Fallback:</p>
              <p>Routing to Thanjavur KVK Krishi Vigyan Kendra Extension Desk.</p>
            </div>
          </div>

          {/* Right Column: Pre-Analyzed Case Summary (PRD §5.11) */}
          <div className="md:col-span-8 space-y-5">
            <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
              
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-xs font-bold uppercase text-sky-300 font-mono">
                  Compiled Auto-Case Summary
                </span>
                <span className="text-xs text-slate-400">{selectedCase.slaTarget}</span>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <span className="text-slate-500 block">Farmer & Location</span>
                  <span className="font-bold text-white">{selectedCase.farmerName} ({selectedCase.farmLocation})</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Growth Stage & Soil</span>
                  <span className="font-bold text-white">{selectedCase.growthStage} · {selectedCase.soilType}</span>
                </div>
                <div className="col-span-2">
                  <span className="text-slate-500 block">Prior Treatments Attempted</span>
                  <span className="font-bold text-amber-300">{selectedCase.treatmentsTried}</span>
                </div>
                <div className="col-span-2">
                  <span className="text-slate-500 block">Closed-Loop Follow-up Trend</span>
                  <span className="font-bold text-rose-400">{selectedCase.followUpTrend}</span>
                </div>
              </div>

              {/* Treatment Prescription Form */}
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

              {/* Action */}
              <button
                onClick={handleResolve}
                disabled={isResolved}
                className="w-full btn btn-primary py-3 text-xs font-bold gap-2 bg-sky-700 hover:bg-sky-600 disabled:opacity-50"
              >
                <Send className="w-4 h-4 text-lime-300" />
                {isResolved ? 'Case Resolved & Logged' : 'Submit Prescription & Update Health Score'}
              </button>

            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
