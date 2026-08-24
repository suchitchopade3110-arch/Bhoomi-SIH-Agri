import React from 'react';
import { 
  MapPin, 
  ShieldCheck, 
  FileText, 
  CheckCircle2, 
  Clock,
  TrendingUp,
  Map
} from 'lucide-react';

export default function RegionStatsCard({ 
  onInspectScore
}) {
  return (
    <div className="bg-white rounded-2xl shadow-[0_20px_50px_-12px_rgba(0,0,0,0.15)] p-6 w-full relative z-20 transition-all">
      
      {/* Top Tag & Region Identification */}
      <div className="flex justify-between items-start mb-6">
        <div className="flex items-center gap-2 text-blue-600 font-bold text-sm uppercase tracking-wider">
          <Map size={16} fill="currentColor" />
          My Jurisdiction
        </div>
        <div className="flex items-center gap-1 text-slate-500 text-xs font-semibold">
          <MapPin size={12} />
          Thanjavur Taluk
        </div>
      </div>

      <div className="text-sm font-semibold text-slate-700 mb-6 pb-4 border-b border-slate-100 flex justify-between items-center">
        <span>Active Villages: 42</span>
        <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs">Division A</span>
      </div>

      {/* Main Metric */}
      <div className="mb-6">
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Pending Land Verifications</div>
        <div className="flex items-center justify-between">
          <div className="text-5xl font-black text-amber-500 tracking-tighter">
            18
          </div>
          
          {/* Action button in place of arc */}
          <button 
            onClick={onInspectScore}
            className="bg-amber-100 text-amber-800 text-xs font-bold py-2 px-3 rounded-lg hover:bg-amber-200 transition-colors"
          >
            Review Now &rarr;
          </button>
        </div>
      </div>

      {/* 4 Core Indicators Rows */}
      <div className="space-y-4">
        
        {/* Verification Status */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <CheckCircle2 size={16} className="text-[#1b8c47]" /> Verified this month
          </div>
          <div className="text-xs font-bold text-slate-700">142 Cases</div>
        </div>

        {/* Subsidy Status */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <FileText size={16} className="text-blue-500" /> Subsidies Disbursed
          </div>
          <div className="text-xs font-bold text-slate-700">₹ 4.2L</div>
        </div>

        {/* Fraud Risk */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <ShieldCheck size={16} className="text-emerald-500" /> Boundary Conflicts
          </div>
          <div className="text-xs font-bold text-rose-500">2 Alerts</div>
        </div>

        {/* Regional Health */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <TrendingUp size={16} className="text-amber-500" /> Avg Farm Health
          </div>
          <div className="text-xs font-bold text-[#1b8c47]">78/100</div>
        </div>

      </div>

      {/* Footer sync timestamp */}
      <div className="mt-4 flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
        <Clock size={12} /> Live synced with State Registry
      </div>

    </div>
  );
}
