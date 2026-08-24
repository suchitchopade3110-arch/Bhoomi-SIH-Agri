import React, { useState } from 'react';
import { 
  Camera, 
  UploadCloud, 
  AlertTriangle, 
  CheckCircle2, 
  ShieldAlert, 
  FileText, 
  ArrowRight,
  Sparkles,
  Info,
  Layers,
  HelpCircle
} from 'lucide-react';
import { CURATED_CORPUS, MOCK_DIAGNOSES } from '../data/corpusData';

export default function DiseaseDetectionSection({ onOpenAgronomistPortal }) {
  const [activeTab, setActiveTab] = useState('high_conf'); // 'high_conf' | 'low_conf'
  const [selectedDisease, setSelectedDisease] = useState(CURATED_CORPUS[0]);

  const activeDiagnosis = activeTab === 'high_conf' ? MOCK_DIAGNOSES[0] : MOCK_DIAGNOSES[1];

  return (
    <section id="disease-detection" className="section-padding bg-white relative overflow-hidden">
      <div className="container">
        
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-4 mb-14">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-100 border border-emerald-300 text-emerald-800 text-xs font-bold uppercase tracking-wider">
            <Camera className="w-3.5 h-3.5 text-emerald-600" />
            <span>PRD §5.6 & §5.8: Multimodal Grounded Diagnosis</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 font-display">
            Crop Problem & Disease Diagnosis
          </h2>

          <p className="text-base sm:text-lg text-slate-600">
            Upload leaf photos for AI analysis bounded strictly to verified ICAR corpora with an enforced <strong>Confidence Gate (&gt; 70%)</strong>.
          </p>

          {/* Gate Demonstration Switcher for Judges */}
          <div className="pt-3 flex justify-center gap-3">
            <button
              onClick={() => setActiveTab('high_conf')}
              className={`px-4 py-2 rounded-full text-xs font-bold transition-all flex items-center gap-2 ${
                activeTab === 'high_conf'
                  ? 'bg-emerald-800 text-white shadow-md'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <CheckCircle2 className="w-4 h-4 text-lime-400" />
              <span>Above Gate: 88% Confidence (BLB Detected)</span>
            </button>
            <button
              onClick={() => setActiveTab('low_conf')}
              className={`px-4 py-2 rounded-full text-xs font-bold transition-all flex items-center gap-2 ${
                activeTab === 'low_conf'
                  ? 'bg-amber-800 text-white shadow-md'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <ShieldAlert className="w-4 h-4 text-amber-300" />
              <span>Below Gate: 52% (Trips Safety Gate → Escalates)</span>
            </button>
          </div>
        </div>

        {/* 4-Step Diagnosis Visual Pipeline */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">1</div>
            <div>
              <p className="text-xs font-bold text-slate-900">Upload Crop Image</p>
              <p className="text-[11px] text-slate-500">Camera / Voice note</p>
            </div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center font-bold">2</div>
            <div>
              <p className="text-xs font-bold text-slate-900">AI Confidence Gate</p>
              <p className="text-[11px] text-slate-500">Threshold check (&gt; 70%)</p>
            </div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-100 text-cyan-700 flex items-center justify-center font-bold">3</div>
            <div>
              <p className="text-xs font-bold text-slate-900">ICAR RAG Match</p>
              <p className="text-[11px] text-slate-500">Curated & dated citations</p>
            </div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-lime-100 text-lime-800 flex items-center justify-center font-bold">4</div>
            <div>
              <p className="text-xs font-bold text-slate-900">5-Point Advisory</p>
              <p className="text-[11px] text-slate-500">Action + What to Avoid</p>
            </div>
          </div>
        </div>

        {/* Live Diagnosis Inspection Card */}
        {activeTab === 'high_conf' ? (
          <div className="glass-panel p-6 sm:p-8 lg:p-10 rounded-3xl bg-slate-900 text-white border-slate-800 shadow-2xl">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              
              {/* Left: Specimen Details & Confidence Badge */}
              <div className="lg:col-span-5 space-y-5">
                <div className="p-5 rounded-2xl bg-slate-950 border border-emerald-500/30 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                      SPECIES & FIELD SPECIMEN
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-lime-300 border border-emerald-600/40">
                      CR-1009 Samba Paddy
                    </span>
                  </div>

                  <div className="h-44 rounded-xl bg-gradient-to-br from-emerald-950 to-slate-900 border border-slate-800 flex flex-col items-center justify-center text-center p-4 relative overflow-hidden">
                    <span className="text-5xl mb-2">🌾</span>
                    <p className="text-sm font-bold text-white">Samba Paddy Leaf Margin Sample</p>
                    <p className="text-xs text-slate-400">Captured at Thiruvaiyaru · Day 22</p>
                    <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/60 text-[10px] font-mono text-lime-300">
                      Confidence: 88.4%
                    </div>
                  </div>

                  {/* Confidence Breakdown Alternatives */}
                  <div className="space-y-1.5 pt-2">
                    <p className="text-xs font-bold text-slate-300">Model Top-3 Softmax Distribution:</p>
                    {activeDiagnosis.alternatives.map((alt) => (
                      <div key={alt.name} className="flex justify-between items-center text-xs p-2 rounded-lg bg-slate-900 border border-slate-800">
                        <span className="text-slate-300">{alt.name}</span>
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-bold text-lime-400">{alt.confidence}</span>
                          <span className="text-[10px] text-slate-500">{alt.status}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Source Citation */}
                <div className="p-4 rounded-2xl bg-emerald-950/70 border border-emerald-700/50 text-xs space-y-1">
                  <p className="font-bold text-lime-300">📜 ICAR Grounding & Provenance:</p>
                  <p className="text-emerald-100/90">{selectedDisease.citation}</p>
                  <p className="text-[10px] text-slate-400">Curator: {selectedDisease.curator}</p>
                </div>
              </div>

              {/* Right: Standardized 5-Point Advisory Structure (PRD §5.8) */}
              <div className="lg:col-span-7 space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                  <h3 className="text-xl font-bold font-display text-white flex items-center gap-2">
                    <FileText className="w-5 h-5 text-lime-400" />
                    Standardized 5-Point Advisory
                  </h3>
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-900 text-lime-300 border border-emerald-600">
                    Grounded Output
                  </span>
                </div>

                <div className="space-y-3">
                  
                  {/* Point 1: Possible Issue */}
                  <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-1">
                    <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">
                      1. Possible Issue & Confidence
                    </span>
                    <p className="text-sm font-bold text-white">
                      {selectedDisease.advisory5Point.possibleIssue}
                    </p>
                    <p className="text-xs text-slate-400">
                      Cues: {selectedDisease.distinguishingCues}
                    </p>
                  </div>

                  {/* Point 2: What to Check */}
                  <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-1">
                    <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider">
                      2. What to Check (Differential Symptoms)
                    </span>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {selectedDisease.advisory5Point.whatToCheck}
                    </p>
                  </div>

                  {/* Point 3: What to Do Next */}
                  <div className="p-3.5 rounded-2xl bg-slate-950 border border-emerald-600/40 space-y-1">
                    <span className="text-[11px] font-bold text-lime-400 uppercase tracking-wider">
                      3. What to Do Next (Actionable Remedy)
                    </span>
                    <p className="text-xs text-emerald-100 leading-relaxed">
                      {selectedDisease.advisory5Point.whatToDoNext}
                    </p>
                  </div>

                  {/* Point 4: What to Avoid (LOUDEST AND FIRST) */}
                  <div className="p-4 rounded-2xl bg-rose-950/70 border-2 border-rose-500/80 space-y-1">
                    <div className="flex items-center gap-1.5 text-xs font-black text-rose-300 uppercase tracking-wider">
                      <AlertTriangle className="w-4 h-4 text-rose-400" />
                      <span>4. WHAT TO AVOID (CRITICAL AGRONOMIC MISTAKE)</span>
                    </div>
                    <p className="text-xs font-semibold text-rose-100 leading-relaxed">
                      {selectedDisease.advisory5Point.whatToAvoid}
                    </p>
                  </div>

                  {/* Point 5: Expert Escalation Triggers */}
                  <div className="p-3.5 rounded-2xl bg-slate-950 border border-amber-500/40 space-y-1">
                    <span className="text-[11px] font-bold text-amber-400 uppercase tracking-wider">
                      5. Human Expert Escalation Triggers
                    </span>
                    <p className="text-xs text-amber-200/90 leading-relaxed">
                      {selectedDisease.advisory5Point.expertTriggers}
                    </p>
                  </div>

                </div>
              </div>

            </div>
          </div>
        ) : (
          /* Low Confidence / Safety Gate Tripped State */
          <div className="glass-panel p-8 rounded-3xl bg-slate-950 text-white border-amber-500/40 shadow-2xl space-y-6">
            <div className="flex items-center gap-4 text-left p-4 rounded-2xl bg-amber-950/50 border border-amber-500/30">
              <ShieldAlert className="w-8 h-8 text-amber-400 shrink-0" />
              <div>
                <h3 className="text-lg font-bold text-amber-300 font-display">
                  Confidence Gate Tripped: 52% Confidence (&lt; 70% Minimum Threshold)
                </h3>
                <p className="text-xs text-slate-300">
                  {activeDiagnosis.reasonText} To protect smallholders from crop loss caused by hallucinated generative advice, Bhoomi refuses to guess and triggers human agronomist escalation.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-slate-400 block mb-1">Attempted Softmax 1:</span>
                <p className="font-bold text-amber-300">Sheath Rot (52% - Uncertain)</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-slate-400 block mb-1">Attempted Softmax 2:</span>
                <p className="font-bold text-slate-300">False Smut (31% - Uncertain)</p>
              </div>
              <div className="p-4 rounded-xl bg-emerald-950 border border-emerald-700/50">
                <span className="text-emerald-400 font-bold block mb-1">Safety Action:</span>
                <p className="text-emerald-200 font-semibold">Auto-routed to Thanjavur KVK Queue</p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={onOpenAgronomistPortal}
                className="btn btn-accent text-xs font-bold py-2.5 px-6 gap-2"
              >
                <span>View in KVK Agronomist Portal</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

      </div>
    </section>
  );
}
