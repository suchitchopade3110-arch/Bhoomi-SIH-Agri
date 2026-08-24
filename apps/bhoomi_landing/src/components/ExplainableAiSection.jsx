import React, { useState } from 'react';
import { 
  HelpCircle, 
  Droplets, 
  CloudRain, 
  AlertOctagon, 
  ShieldAlert, 
  CheckCircle2, 
  FileText, 
  ChevronRight,
  Info
} from 'lucide-react';
import { calculateDynamicIrrigation } from '../data/fao56Engine';

export default function ExplainableAiSection() {
  const [activeExample, setActiveExample] = useState('irrigation');

  // Interactive FAO-56 calculator state
  const [area, setArea] = useState(2.0);
  const [rainfall, setRainfall] = useState(12.5);
  const [et0, setEt0] = useState(4.2);

  const irriResult = calculateDynamicIrrigation({
    cropKey: 'paddy',
    stageKey: 'vegetative',
    areaAcres: area,
    et0MmDay: et0,
    rainfallMm: rainfall
  });

  return (
    <section id="explainable-ai" className="section-padding bg-slate-50 relative overflow-hidden">
      <div className="container">
        
        {/* Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-100 border border-emerald-300 text-emerald-800 text-xs font-bold uppercase tracking-wider">
            <HelpCircle className="w-3.5 h-3.5 text-emerald-600" />
            <span>PRD §5.4 & §13: Explainable Agronomy</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 font-display">
            Why This Advice?
          </h2>

          <p className="text-base sm:text-lg text-slate-600">
            Never trust a black-box recommendation. Bhoomi provides full agronomic provenance, Penman-Monteith formulas, and cited peer-reviewed package-of-practices for every decision.
          </p>

          {/* Tab switchers */}
          <div className="pt-4 flex justify-center gap-2">
            <button
              onClick={() => setActiveExample('irrigation')}
              className={`px-5 py-2.5 rounded-full text-xs font-bold transition-all ${
                activeExample === 'irrigation'
                  ? 'bg-emerald-800 text-white shadow-md'
                  : 'bg-white text-slate-700 hover:bg-slate-200 border border-slate-200'
              }`}
            >
              💧 Irrigation Math (FAO-56)
            </button>
            <button
              onClick={() => setActiveExample('disease')}
              className={`px-5 py-2.5 rounded-full text-xs font-bold transition-all ${
                activeExample === 'disease'
                  ? 'bg-emerald-800 text-white shadow-md'
                  : 'bg-white text-slate-700 hover:bg-slate-200 border border-slate-200'
              }`}
            >
              🌿 Disease Treatment Reasoning
            </button>
          </div>
        </div>

        {/* Content Box */}
        {activeExample === 'irrigation' ? (
          <div className="glass-panel p-6 sm:p-8 lg:p-10 rounded-3xl bg-white border-slate-200 shadow-xl">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              
              {/* Left Column: Recommendation Card */}
              <div className="lg:col-span-6 space-y-6">
                <div className="p-6 rounded-3xl bg-emerald-950 text-white space-y-4 shadow-xl">
                  <div className="flex items-center justify-between">
                    <span className="text-xs uppercase font-bold tracking-wider text-lime-400">
                      TODAY'S WATER ADVISORY
                    </span>
                    <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-800 text-emerald-200">
                      FAO-56 Penman-Monteith
                    </span>
                  </div>

                  <h3 className="text-2xl font-bold font-display text-white">
                    {irriResult.netIrrigationMm <= 1.0 
                      ? '⏸ Delay Field Irrigation Today' 
                      : `💧 Deliver ${(irriResult.dailyBudgetLiters / 1000).toFixed(1)} m³ of Water`}
                  </h3>

                  <p className="text-xs text-emerald-100/90 leading-relaxed">
                    {irriResult.advisoryNote}
                  </p>

                  <div className="p-4 rounded-2xl bg-black/40 border border-white/10 space-y-2 text-xs">
                    <div className="flex justify-between text-slate-300">
                      <span>Crop Evapotranspiration (ETc = ET₀ × Kc):</span>
                      <span className="font-mono font-bold text-white">{irriResult.grossWaterNeedMm} mm/day</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Effective Rainfall Credit (75% of {rainfall}mm):</span>
                      <span className="font-mono font-bold text-lime-400">-{irriResult.effectiveRainMm} mm</span>
                    </div>
                    <div className="flex justify-between pt-2 border-t border-white/10 text-white font-bold">
                      <span>Net Irrigation Required:</span>
                      <span className="font-mono text-lime-300">{irriResult.netIrrigationMm} mm/day ({irriResult.dailyBudgetLiters.toLocaleString()} L)</span>
                    </div>
                  </div>
                </div>

                {/* Seed mass budget summary */}
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold text-slate-800">Seed Mass Budget for {area} Acres:</p>
                    <p className="text-[11px] text-slate-500">Based on 20 kg/acre transplanted Samba Paddy standard</p>
                  </div>
                  <span className="text-lg font-black text-emerald-800 font-mono">{irriResult.totalSeedKg} kg</span>
                </div>
              </div>

              {/* Right Column: Interactive Parameter Sliders */}
              <div className="lg:col-span-6 space-y-6">
                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-slate-900 font-display">
                    Interactive FAO-56 Proof Simulator
                  </h3>
                  <p className="text-xs text-slate-500">
                    Adjust weather and farm inputs to see real-time recalculation of the crop water budget.
                  </p>
                </div>

                {/* Sliders */}
                <div className="space-y-4 bg-slate-50 p-5 rounded-2xl border border-slate-200">
                  
                  {/* Land Area */}
                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                      <span>Land Area (Acres):</span>
                      <span className="font-mono text-emerald-700">{area} Acres</span>
                    </div>
                    <input 
                      type="range" 
                      min="0.5" 
                      max="10" 
                      step="0.5"
                      value={area}
                      onChange={(e) => setArea(parseFloat(e.target.value))}
                      className="w-full accent-emerald-700"
                    />
                  </div>

                  {/* Rainfall Forecast */}
                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                      <span>Rainfall Forecast (mm/day):</span>
                      <span className="font-mono text-sky-700">{rainfall} mm</span>
                    </div>
                    <input 
                      type="range" 
                      min="0" 
                      max="40" 
                      step="1"
                      value={rainfall}
                      onChange={(e) => setRainfall(parseFloat(e.target.value))}
                      className="w-full accent-sky-600"
                    />
                  </div>

                  {/* Reference Evapotranspiration ET0 */}
                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                      <span>Reference Evapotranspiration (ET₀ mm/day):</span>
                      <span className="font-mono text-amber-700">{et0} mm/day</span>
                    </div>
                    <input 
                      type="range" 
                      min="2.0" 
                      max="8.0" 
                      step="0.2"
                      value={et0}
                      onChange={(e) => setEt0(parseFloat(e.target.value))}
                      className="w-full accent-amber-600"
                    />
                  </div>

                </div>

                <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 leading-relaxed flex items-start gap-2">
                  <Info className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                  <span>
                    <strong>Named Agronomic Method:</strong> Standard FAO-56 Penman-Monteith with crop coefficient $K_c = 1.15$ (Samba Paddy vegetative phase). Effective rainfall is credited at 75% efficiency.
                  </span>
                </div>

              </div>

            </div>
          </div>
        ) : (
          <div className="glass-panel p-6 sm:p-8 lg:p-10 rounded-3xl bg-white border-slate-200 shadow-xl space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-200">
              <div>
                <h3 className="text-xl font-bold text-slate-900 font-display">
                  Why Avoid Nitrogen Top-Dressing During BLB Outbreak?
                </h3>
                <p className="text-xs text-slate-500">ICAR-CRRI Rice Advisory Bulletin 2024 / TNAU Crop Production Guide</p>
              </div>
              <span className="text-xs font-bold px-3 py-1 rounded-full bg-rose-100 text-rose-800 border border-rose-300">
                Mandatory "What to Avoid" Rule
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div className="w-8 h-8 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold">1</div>
                <h4 className="text-sm font-bold text-slate-900">Cell Wall Softening</h4>
                <p className="text-xs text-slate-600">Excess nitrogen triggers succulent vegetative tissue with thinner parenchymal cell walls, accelerating <em>Xanthomonas oryzae</em> bacterial entry.</p>
              </div>

              <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div className="w-8 h-8 rounded-xl bg-rose-100 text-rose-700 flex items-center justify-center font-bold">2</div>
                <h4 className="text-sm font-bold text-slate-900">Kresek Wilting Risk</h4>
                <p className="text-xs text-slate-600">Top-dressing Urea during active lesion spread increases seedling mortality and systemic vascular occlusion by over 40%.</p>
              </div>

              <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div className="w-8 h-8 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">3</div>
                <h4 className="text-sm font-bold text-slate-900">Correct Alternative</h4>
                <p className="text-xs text-slate-600">Hold nitrogen. Apply Potassium (MOP) to harden cell walls, drain standing water, and apply Copper Hydroxide + Streptocycline.</p>
              </div>
            </div>
          </div>
        )}

      </div>
    </section>
  );
}
