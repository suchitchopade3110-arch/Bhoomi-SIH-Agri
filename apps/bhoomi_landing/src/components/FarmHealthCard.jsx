import React from 'react';
import { 
  MapPin, 
  Droplets, 
  CloudRain, 
  ShieldAlert, 
  Clock,
  Leaf,
  Sprout
} from 'lucide-react';
import { calculateHealthScore } from '../data/healthScoreEngine';

export default function FarmHealthCard({ 
  farm, 
  activeScenario, 
  onInspectScore,
  compact = false 
}) {
  const currentSubindices = activeScenario?.subindices || {
    environmental: 80,
    resource: 85,
    cropStage: 80,
    problemPenalty: 0,
    monitoringRecency: 75,
    treatmentResponse: 70
  };

  const healthResult = calculateHealthScore(
    activeScenario?.state?.isUnrated ? { isUnrated: true } : currentSubindices
  );

  const isUnrated = healthResult.score === null;
  const score = isUnrated ? '-' : healthResult.score;

  return (
    <div className="bg-white rounded-2xl shadow-[0_20px_50px_-12px_rgba(0,0,0,0.15)] p-6 w-full relative z-20 transition-all">
      
      {/* Top Tag & Farm Identification */}
      <div className="flex justify-between items-start mb-6">
        <div className="flex items-center gap-2 text-yellow-500 font-bold text-sm">
          <Leaf size={16} fill="currentColor" />
          MY FARM
        </div>
        <div className="flex items-center gap-1 text-slate-500 text-xs font-semibold">
          <MapPin size={12} />
          {farm?.village || 'Alappuzha, Kerala'}
        </div>
      </div>

      <div className="text-sm font-semibold text-slate-700 mb-6 pb-4 border-b border-slate-100">
        {farm?.crop || 'Paddy'} • {farm?.areaAcres || '2'} Acres
      </div>

      {/* Main Health Score */}
      <div className="mb-6">
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Farm Health</div>
        <div className="flex items-center justify-between">
          <div className="text-5xl font-black text-[#1b8c47] tracking-tighter">
            {score}<span className="text-2xl text-slate-400 font-semibold">/100</span>
          </div>
          
          {/* Semicircular Arc */}
          <div className="relative w-20 h-12 cursor-pointer hover:scale-105 transition-transform" onClick={onInspectScore}>
            <svg viewBox="0 0 100 50" className="w-full h-full overflow-visible">
              <path 
                className="text-slate-100" 
                strokeWidth="10" 
                stroke="currentColor" 
                fill="none" 
                d="M 10 50 A 40 40 0 0 1 90 50" 
                strokeLinecap="round" 
              />
              {!isUnrated && (
                <path 
                  className="text-[#1b8c47]" 
                  strokeWidth="10" 
                  stroke="currentColor" 
                  fill="none" 
                  d="M 10 50 A 40 40 0 0 1 90 50" 
                  strokeDasharray="125.6" 
                  strokeDashoffset={125.6 - (125.6 * score) / 100} 
                  strokeLinecap="round" 
                />
              )}
            </svg>
          </div>
        </div>
      </div>

      {/* 4 Core Indicators Rows */}
      <div className="space-y-4">
        
        {/* Crop Status */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <Sprout size={16} className="text-[#1b8c47]" /> Crop
          </div>
          <div className="text-xs font-bold text-[#1b8c47]">GOOD</div>
        </div>

        {/* Water Status */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <Droplets size={16} className="text-blue-500" /> Water
          </div>
          <div className="text-xs font-bold text-[#1b8c47]">GOOD</div>
        </div>

        {/* Weather Risk */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <CloudRain size={16} className="text-slate-500" /> Weather
          </div>
          <div className="text-xs font-bold text-amber-500">MEDIUM RISK</div>
        </div>

        {/* Disease Risk */}
        <div className="flex items-center justify-between py-2 border-b border-slate-50">
          <div className="flex items-center gap-3 text-sm font-bold text-slate-700">
            <ShieldAlert size={16} className="text-amber-500" /> Disease
          </div>
          <div className="text-xs font-bold text-amber-500">LOW &rarr; MEDIUM</div>
        </div>

      </div>

      {/* Footer sync timestamp */}
      <div className="mt-4 flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
        <Clock size={12} /> Updated just now
      </div>

    </div>
  );
}
