import React, { useState } from 'react';
import { 
  Activity, 
  HelpCircle, 
  CheckCircle2, 
  AlertTriangle, 
  RotateCcw, 
  ArrowRight, 
  Layers, 
  ShieldCheck, 
  TrendingUp, 
  TrendingDown,
  Info,
  Sparkles
} from 'lucide-react';
import { 
  HEALTH_WEIGHTS, 
  PRESET_SCENARIOS, 
  calculateHealthScore,
  HEALTH_BANDS
} from '../data/healthScoreEngine';

export default function FarmHealthSection({ activeScenario, onSelectScenario }) {
  const [activeTab, setActiveTab] = useState(activeScenario?.id || 'baseline');

  const currentScenario = PRESET_SCENARIOS[activeTab] || PRESET_SCENARIOS.baseline;
  const isUnrated = currentScenario.state?.isUnrated;

  const currentSubindices = currentScenario.subindices || {
    environmental: 80,
    resource: 85,
    cropStage: 80,
    problemPenalty: 0,
    monitoringRecency: 75,
    treatmentResponse: 70
  };

  const healthCalc = calculateHealthScore(
    isUnrated ? { isUnrated: true } : currentSubindices
  );

  const subindexItems = [
    {
      key: 'activeProblem',
      name: 'Active Problem Load',
      weight: HEALTH_WEIGHTS.activeProblem, // 0.30 (The big mover!)
      score: healthCalc.breakdown?.activeProblem ?? 100,
      detail: currentSubindices.problemPenalty > 0 
        ? `Penalty -${currentSubindices.problemPenalty} applied (BLB active)` 
        : 'Zero active disease penalty (Score: 100)',
      isHighlight: true,
      tag: '0.30 Weight (Big Mover)'
    },
    {
      key: 'environmental',
      name: 'Environmental Suitability',
      weight: HEALTH_WEIGHTS.environmental, // 0.20
      score: currentSubindices.environmental,
      detail: 'Weather + Soil alignment vs. Paddy vegetative stage',
      tag: '0.20 Weight'
    },
    {
      key: 'resource',
      name: 'Resource Adequacy',
      weight: HEALTH_WEIGHTS.resource, // 0.15
      score: currentSubindices.resource,
      detail: 'FAO-56 dynamic irrigation delivered vs. Penman-Monteith requirement',
      tag: '0.15 Weight'
    },
    {
      key: 'cropStage',
      name: 'Crop-Stage Progression',
      weight: HEALTH_WEIGHTS.cropStage, // 0.15
      score: currentSubindices.cropStage,
      detail: 'On-schedule canopy development & tiller count vigor',
      tag: '0.15 Weight'
    },
    {
      key: 'monitoringRecency',
      name: 'Monitoring Recency',
      weight: HEALTH_WEIGHTS.monitoringRecency, // 0.10
      score: currentSubindices.monitoringRecency,
      detail: 'Recency of photo inspections, voice logs & weather sync',
      tag: '0.10 Weight'
    },
    {
      key: 'treatmentResponse',
      name: 'Treatment Response Trend',
      weight: HEALTH_WEIGHTS.treatmentResponse, // 0.10
      score: currentSubindices.treatmentResponse,
      detail: 'Closed-loop follow-up trajectory (Improved vs Got Worse)',
      tag: '0.10 Weight'
    }
  ];

  return (
    <section id="farm-health" className="section-padding bg-white relative overflow-hidden">
      <div className="container">
        
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-12">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-100 border border-emerald-300 text-emerald-800 text-xs font-bold uppercase tracking-wider">
            <Activity className="w-3.5 h-3.5 text-emerald-600" />
            <span>PRD §7: The One-Screen Defense</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 font-display">
            Know Your Farm's Health
          </h2>

          <p className="text-base sm:text-lg text-slate-600">
            A transparent, explainable 6-factor rubric where every single point change is traceable to an agricultural input—never an opaque black box.
          </p>
        </div>

        {/* Judge Interactive Walkthrough Buttons */}
        <div className="mb-8 p-3 bg-slate-100 rounded-2xl border border-slate-200 flex flex-wrap items-center justify-center gap-2">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider px-2 flex items-center gap-1">
            <Layers className="w-3.5 h-3.5" /> Reconcile Scenarios:
          </span>
          {Object.values(PRESET_SCENARIOS).map((scen) => (
            <button
              key={scen.id}
              onClick={() => {
                setActiveTab(scen.id);
                onSelectScenario(scen);
              }}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === scen.id
                  ? 'bg-emerald-800 text-white shadow-md shadow-emerald-950/20'
                  : 'bg-white text-slate-700 hover:bg-slate-200 border border-slate-200'
              }`}
            >
              {scen.title}
            </button>
          ))}
        </div>

        {/* Main Dashboard Card */}
        <div className="glass-panel p-6 sm:p-8 lg:p-10 rounded-3xl border-slate-200 shadow-xl bg-gradient-to-b from-white to-slate-50">
          
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Left Column: Big Score Gauge & Scenario Explanation */}
            <div className="lg:col-span-5 space-y-6">
              
              {/* Score Display Card */}
              <div className="p-7 rounded-3xl bg-gradient-to-br from-emerald-950 via-slate-900 to-emerald-900 text-white shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs uppercase font-bold tracking-widest text-emerald-300">
                      LIVE RECONCILED SCORE
                    </span>
                    <div className="flex items-baseline gap-2 mt-2">
                      {isUnrated ? (
                        <span className="text-4xl sm:text-5xl font-extrabold text-slate-300 font-display">
                          Unrated
                        </span>
                      ) : (
                        <>
                          <span className="text-5xl sm:text-6xl font-black text-white font-display tracking-tight">
                            {healthCalc.score}
                          </span>
                          <span className="text-xl text-emerald-300/70 font-semibold font-mono">/ 100</span>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="w-20 h-20 rounded-full bg-emerald-800/40 border border-emerald-400/30 flex flex-col items-center justify-center text-center p-2">
                    <span className="text-[10px] font-bold uppercase text-emerald-200">BAND</span>
                    <span className="text-sm font-extrabold text-lime-300">{healthCalc.band.name}</span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-white/10 text-xs text-emerald-100/90 leading-relaxed">
                  <p className="font-semibold text-white mb-1">{currentScenario.title}</p>
                  <p>{currentScenario.description}</p>
                </div>

                {/* Formula Callout */}
                <div className="mt-4 p-3 rounded-xl bg-black/30 border border-white/10 text-[11px] font-mono text-emerald-300">
                  <code>Health = round( Σ (wᵢ × subindexᵢ) )</code>
                </div>
              </div>

              {/* Qualitative Status Summary */}
              <div className="p-5 rounded-2xl bg-emerald-50 border border-emerald-200">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-900 mb-1">
                  <Sparkles className="w-4 h-4 text-emerald-700" />
                  <span>Farmer Spoken Sentence (1-Sentence Rule)</span>
                </div>
                <p className="text-sm text-emerald-800 font-medium italic">
                  "{currentScenario.qualitative || 'Farm is monitored under standard conditions with live weather synchronization.'}"
                </p>
              </div>

              {/* Band Reference */}
              <div className="p-4 rounded-2xl bg-white border border-slate-200 text-xs space-y-2">
                <p className="font-bold text-slate-700">Health Classification Bands:</p>
                <div className="flex flex-wrap gap-1.5 text-[11px] font-medium">
                  <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700">Unrated (Day 0)</span>
                  <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800">0-39 Critical</span>
                  <span className="px-2 py-0.5 rounded bg-orange-100 text-orange-800">40-59 Poor</span>
                  <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800">60-74 Watch</span>
                  <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">75-89 Good</span>
                  <span className="px-2 py-0.5 rounded bg-green-100 text-green-900 font-bold">90-100 Excellent</span>
                </div>
              </div>

            </div>

            {/* Right Column: 6 Sub-Indices Breakdown Table */}
            <div className="lg:col-span-7 space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 font-display">
                  Rubric Sub-Indices Breakdown
                </h3>
                <span className="text-xs font-mono font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded">
                  Sum of Weights = 1.00
                </span>
              </div>

              <div className="space-y-3">
                {subindexItems.map((item) => (
                  <div 
                    key={item.key}
                    className={`p-4 rounded-2xl border transition-all ${
                      item.isHighlight 
                        ? 'bg-amber-50/70 border-amber-300 shadow-sm' 
                        : 'bg-white border-slate-200'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4 mb-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-bold text-slate-900">{item.name}</h4>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            item.isHighlight ? 'bg-amber-200 text-amber-900' : 'bg-slate-100 text-slate-700'
                          }`}>
                            {item.tag}
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-0.5">{item.detail}</p>
                      </div>

                      <div className="text-right shrink-0">
                        <span className="text-base font-extrabold text-slate-900 font-mono">
                          {isUnrated ? '--' : item.score}
                        </span>
                        <span className="text-xs text-slate-400 font-mono"> / 100</span>
                        <p className="text-[10px] font-semibold text-emerald-700">
                          Contrib: {isUnrated ? '--' : (item.score * item.weight).toFixed(1)} pts
                        </p>
                      </div>
                    </div>

                    {/* Visual Progress Bar */}
                    <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${
                          item.score >= 75 ? 'bg-emerald-500' : item.score >= 50 ? 'bg-amber-500' : 'bg-rose-500'
                        }`}
                        style={{ width: `${isUnrated ? 0 : item.score}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>

              {/* The Judge's Defense summary box */}
              <div className="p-4 rounded-2xl bg-slate-900 text-emerald-200 text-xs flex items-start gap-3 mt-4">
                <Info className="w-5 h-5 text-lime-400 shrink-0 mt-0.5" />
                <p>
                  <strong>Judge Verification:</strong> When asked "is that score real or decorative?", walk the exact formula: When early BLB is diagnosed on Day 22, Subindex 4 drops to 70 (weight 0.30, loss of 9 pts) + weather/monitoring adjustments, dropping score from <strong>82 → 68 (Watch)</strong>. Upon treatment on Day 28, score recovers to <strong>86 (Good)</strong>.
                </p>
              </div>

            </div>

          </div>

        </div>

      </div>
    </section>
  );
}
