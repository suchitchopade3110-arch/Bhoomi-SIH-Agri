import React, { useState } from 'react';
import { 
  Sparkles, 
  Layers, 
  Mic, 
  CheckCircle2, 
  ShieldAlert, 
  TrendingUp, 
  TrendingDown, 
  ArrowRight,
  UserCheck,
  Calendar,
  AlertCircle,
  FileCheck2,
  RefreshCw
} from 'lucide-react';
import { INITIAL_FARM_DATA } from '../data/farmStore';
import { PRESET_SCENARIOS, calculateHealthScore } from '../data/healthScoreEngine';

export default function FarmTimelineSection({ onSelectScenario, onOpenVoiceModal }) {
  const [selectedEvent, setSelectedEvent] = useState(INITIAL_FARM_DATA.timeline[2]); // Default Day 22 BLB
  const [timelineEvents, setTimelineEvents] = useState(INITIAL_FARM_DATA.timeline);

  const getEventIcon = (type) => {
    switch (type) {
      case 'ONBOARDING': return '🎙';
      case 'LAND_VERIFIED': return '🛡';
      case 'DIAGNOSIS': return '📷';
      case 'FOLLOW_UP': return '🔄';
      case 'EXPERT_RESOLUTION': return '👨‍🌾';
      default: return '🌱';
    }
  };

  const getBadgeStyle = (type) => {
    switch (type) {
      case 'ONBOARDING': return 'bg-slate-100 text-slate-700 border-slate-300';
      case 'LAND_VERIFIED': return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'DIAGNOSIS': return 'bg-amber-100 text-amber-800 border-amber-300';
      case 'FOLLOW_UP': return 'bg-rose-100 text-rose-800 border-rose-300';
      case 'EXPERT_RESOLUTION': return 'bg-green-100 text-green-900 border-green-300';
      default: return 'bg-slate-100 text-slate-700 border-slate-300';
    }
  };

  return (
    <section id="timeline" className="section-padding bg-slate-900 text-white relative overflow-hidden">
      
      {/* Background Ambience */}
      <div className="absolute top-1/4 right-0 w-96 h-96 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-10 left-10 w-80 h-80 bg-lime-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="container relative z-10">
        
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-950 border border-emerald-500/40 text-lime-400 text-xs font-bold uppercase tracking-wider">
            <Calendar className="w-3.5 h-3.5" />
            <span>PRD §5.9: Persistent Farm Case File</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white font-display">
            Your Farm Has a Memory
          </h2>

          <p className="text-base sm:text-lg text-slate-300">
            Bhoomi connects every question, photo, irrigation event, and agronomist prescription into a living case file across seasons—farmers never have to re-explain their land.
          </p>
        </div>

        {/* Interactive Timeline Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Chronological Event Nodes */}
          <div className="lg:col-span-7 space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 font-mono">
                Chronological Case Ledger (Ramesh Sundaram · 2 Acres)
              </h3>
              <span className="text-xs text-lime-400 font-bold">5 Verified Entries</span>
            </div>

            <div className="relative pl-6 sm:pl-8 border-l-2 border-emerald-800/80 space-y-6">
              {timelineEvents.map((evt, idx) => {
                const isSelected = selectedEvent?.id === evt.id;
                return (
                  <div 
                    key={evt.id}
                    onClick={() => {
                      setSelectedEvent(evt);
                      if (evt.type === 'ONBOARDING') onSelectScenario(PRESET_SCENARIOS.unrated);
                      if (evt.type === 'LAND_VERIFIED') onSelectScenario(PRESET_SCENARIOS.baseline);
                      if (evt.type === 'DIAGNOSIS') onSelectScenario(PRESET_SCENARIOS.diagnosedBLB);
                      if (evt.type === 'FOLLOW_UP') onSelectScenario(PRESET_SCENARIOS.gotWorse);
                      if (evt.type === 'EXPERT_RESOLUTION') onSelectScenario(PRESET_SCENARIOS.recovered);
                    }}
                    className={`relative p-5 rounded-2xl cursor-pointer transition-all border ${
                      isSelected 
                        ? 'bg-emerald-950/90 border-lime-400 shadow-xl shadow-emerald-950/80 scale-[1.01]' 
                        : 'bg-slate-950/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'
                    }`}
                  >
                    {/* Node Dot on Line */}
                    <div className={`absolute -left-[31px] sm:-left-[39px] top-6 w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all ${
                      isSelected 
                        ? 'bg-lime-400 border-white text-slate-950 scale-125' 
                        : 'bg-slate-900 border-emerald-500 text-white'
                    }`}>
                      <span className="text-[10px] font-black">{idx + 1}</span>
                    </div>

                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{getEventIcon(evt.type)}</span>
                        <h4 className="text-sm sm:text-base font-bold text-white font-display">
                          {evt.title}
                        </h4>
                      </div>
                      <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${getBadgeStyle(evt.type)}`}>
                        {evt.badge}
                      </span>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed mb-3">
                      {evt.description}
                    </p>

                    <div className="flex items-center justify-between text-[11px] font-mono pt-2 border-t border-white/5">
                      <span className="text-slate-400">{evt.date}</span>
                      <div className="flex items-center gap-2">
                        {evt.scoreDelta && (
                          <span className={`font-bold ${evt.scoreDelta.startsWith('+') ? 'text-lime-400' : 'text-rose-400'}`}>
                            {evt.scoreDelta} pts
                          </span>
                        )}
                        <span className="text-emerald-300 font-bold">
                          Score: {evt.scoreAfter}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Column: Case Deep-Dive Detail Inspector */}
          <div className="lg:col-span-5 space-y-6">
            <div className="p-6 sm:p-7 rounded-3xl bg-slate-950 border border-emerald-500/30 shadow-2xl space-y-5">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-xs uppercase font-bold tracking-wider text-lime-400 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" /> Selected Case Snapshot
                </span>
                <span className="text-xs font-mono text-slate-400">{selectedEvent?.date}</span>
              </div>

              <div>
                <h4 className="text-xl font-bold text-white font-display flex items-center gap-2">
                  <span>{getEventIcon(selectedEvent?.type)}</span>
                  {selectedEvent?.title}
                </h4>
                <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                  {selectedEvent?.description}
                </p>
              </div>

              {/* Event Specific Agronomic Invariants */}
              <div className="p-4 rounded-2xl bg-emerald-950/50 border border-emerald-800/60 space-y-2 text-xs">
                <div className="flex justify-between text-slate-300">
                  <span>Farm Parcel:</span>
                  <span className="font-bold text-white">Samba Paddy (2.0 Acres)</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Land Status:</span>
                  <span className="font-bold text-emerald-400 font-mono">Survey 142/3B (Verified)</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Resulting Health Index:</span>
                  <span className="font-bold text-lime-300 font-mono">{selectedEvent?.scoreAfter}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-2 pt-2">
                <button
                  onClick={onOpenVoiceModal}
                  className="w-full btn btn-primary py-3 text-xs font-bold flex items-center justify-center gap-2"
                >
                  <Mic className="w-4 h-4 text-lime-300" />
                  <span>Log New Voice Query or Photo to Case</span>
                </button>
                <p className="text-[11px] text-center text-slate-400">
                  Every interaction is cryptographically hashed to Ramesh's case record.
                </p>
              </div>
            </div>

            {/* Closed Loop Notice */}
            <div className="p-5 rounded-2xl bg-emerald-900/30 border border-emerald-700/40 text-xs text-emerald-200 space-y-1.5">
              <p className="font-bold text-white flex items-center gap-1.5">
                <FileCheck2 className="w-4 h-4 text-lime-400" />
                PRD §5.10 Closed-Loop Guarantee:
              </p>
              <p className="text-emerald-300/80">
                After any diagnosis, a 72-hour check-in asks: <em>"Improved / No Change / Got Worse"</em>. If the problem gets worse, it auto-promotes to the KVK officer queue rather than leaving the farmer stranded.
              </p>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
}
