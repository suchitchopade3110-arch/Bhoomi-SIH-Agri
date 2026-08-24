import React, { useState } from 'react';
import { 
  X, 
  Mic, 
  Volume2, 
  Sparkles, 
  Send, 
  CheckCircle2, 
  AlertTriangle,
  FileCheck2
} from 'lucide-react';
import { CURATED_CORPUS } from '../data/corpusData';

export default function VoiceQueryModal({ isOpen, onClose, onSelectScenario }) {
  const [isRecording, setIsRecording] = useState(false);
  const [queryText, setQueryText] = useState('இலை நுனி மஞ்சள் நிறமாகி கருகுகிறது, என்ன செய்ய வேண்டும்?');
  const [hasSubmitted, setHasSubmitted] = useState(true);

  if (!isOpen) return null;

  const blbAdvisory = CURATED_CORPUS[0].advisory5Point;

  const handleSimulateVoice = () => {
    setIsRecording(true);
    setTimeout(() => {
      setIsRecording(false);
      setQueryText('நெல் இலைகளில் மஞ்சள் கோடுகள் தெரிகிறது...');
      setHasSubmitted(true);
    }, 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl bg-slate-950 text-white border border-emerald-500/40 shadow-2xl p-6 sm:p-8">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-400/40 flex items-center justify-center">
              <Mic className="w-5 h-5 text-lime-400 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-xl font-bold text-white font-display">Ask Bhoomi (Regional Voice)</h3>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-950 text-lime-300 border border-emerald-600/40 font-mono">
                  PRD §5.1 Spoken Tamil
                </span>
              </div>
              <p className="text-xs text-slate-400">Context-Aware Spoken Query Companion</p>
            </div>
          </div>

          <button 
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Spoken Input Box */}
        <div className="my-6 space-y-4">
          <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Parsed Spoken Input (Tamil):</span>
              <span className="text-emerald-400 font-mono">Confidence: 96%</span>
            </div>
            <textarea
              value={queryText}
              onChange={(e) => setQueryText(e.target.value)}
              rows={2}
              className="w-full bg-transparent border-none text-white text-sm font-semibold focus:outline-none"
            />
          </div>

          {/* Voice Record Button */}
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={handleSimulateVoice}
              className={`w-16 h-16 rounded-full flex items-center justify-center transition-all ${
                isRecording 
                  ? 'bg-rose-600 animate-ping text-white shadow-xl shadow-rose-900/50' 
                  : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-xl shadow-emerald-950/60'
              }`}
            >
              <Mic className="w-7 h-7 text-lime-200" />
            </button>
          </div>
          <p className="text-center text-xs text-slate-400">
            {isRecording ? 'Listening in Tamil / English...' : 'Tap to speak your farm question'}
          </p>
        </div>

        {/* Grounded 5-Point Voice Read-Back (PRD §5.8) */}
        {hasSubmitted && (
          <div className="space-y-4 pt-4 border-t border-slate-800 animate-fade-in">
            <div className="flex items-center justify-between">
              <span className="text-xs uppercase font-bold tracking-wider text-lime-400 flex items-center gap-1.5">
                <Volume2 className="w-4 h-4" /> Bhoomi Spoken Read-Back
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-lime-300 border border-emerald-600/40">
                ICAR-CRRI Grounded
              </span>
            </div>

            <div className="p-5 rounded-2xl bg-emerald-950/70 border border-emerald-500/40 space-y-3 text-xs">
              <div>
                <p className="font-bold text-white text-sm">{blbAdvisory.possibleIssue}</p>
                <p className="text-emerald-200/90 mt-1">Ramesh, for your 2.0-acre Samba Paddy, bacterial leaf blight is detected with 88% certainty.</p>
              </div>

              {/* What to avoid alert */}
              <div className="p-3 rounded-xl bg-rose-950/80 border border-rose-500/60 text-rose-100 font-medium">
                <strong>🚫 {blbAdvisory.whatToAvoid}</strong>
              </div>

              <div className="space-y-1.5 text-slate-300">
                <p><strong>Remedy:</strong> {blbAdvisory.whatToDoNext}</p>
                <p className="text-amber-300"><strong>Escalation:</strong> {blbAdvisory.expertTriggers}</p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="w-full btn btn-primary py-3 text-xs font-bold"
            >
              Done & Add to Farm Timeline
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
