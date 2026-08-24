import React, { useState } from 'react';
import { 
  FileSignature, 
  Bot, 
  Eye, 
  Map, 
  CheckCircle, 
  Banknote, 
  ChevronRight,
  ShieldCheck
} from 'lucide-react';

export default function HowItWorksSection() {
  const [activeStep, setActiveStep] = useState(null);

  const steps = [
    { icon: FileSignature, title: 'Submit', desc: 'Farmer submits land and crop profile details.' },
    { icon: Bot, title: 'Pre-check', desc: 'AI scans data for obvious errors or anomalies.' },
    { icon: Eye, title: 'Review', desc: 'Case enters Officer verification queue.' },
    { icon: Map, title: 'Validate', desc: 'Verify boundaries using cadastral map overlay.' },
    { icon: CheckCircle, title: 'Approve', desc: 'Approve authentic profiles with one click.' },
    { icon: Banknote, title: 'Disburse', desc: 'Subsidy matching is unlocked for the farmer.' },
  ];

  return (
    <section id="how-it-works" className="py-20 bg-slate-50 border-t border-slate-100">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 text-blue-600 text-xs font-bold uppercase tracking-wider">
            <ShieldCheck size={14} fill="currentColor" /> WORKFLOW
          </div>
        </div>
        
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 relative max-w-6xl mx-auto">
          {steps.map((step, idx) => {
            const isActive = activeStep === idx;
            
            return (
              <React.Fragment key={idx}>
                <div 
                  className={`flex flex-col items-center text-center w-full md:w-[140px] relative z-10 group cursor-pointer transition-all duration-300 ${isActive ? 'scale-110' : 'hover:scale-105'}`}
                  onClick={() => setActiveStep(isActive ? null : idx)}
                >
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 transition-all duration-500 ease-out ${
                    isActive 
                      ? 'bg-blue-600 text-white shadow-[0_0_30px_rgba(37,99,235,0.4)] ring-4 ring-blue-100 scale-110' 
                      : 'bg-white shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] border border-slate-100 text-blue-600 group-hover:border-blue-200'
                  }`}>
                    <step.icon size={28} fill={idx === 5 && !isActive ? "currentColor" : "none"} className={isActive ? 'animate-bounce' : ''} />
                  </div>
                  <h4 className={`font-bold text-sm mb-2 transition-colors ${isActive ? 'text-blue-700' : 'text-slate-900'}`}>
                    {step.title}
                  </h4>
                  <p className={`text-[11px] leading-relaxed px-2 transition-all duration-300 ${
                    isActive ? 'text-slate-700 font-medium' : 'text-slate-500'
                  }`}>
                    {step.desc}
                  </p>
                </div>
                
                {/* Arrow separator (hidden on mobile, visible on desktop) */}
                {idx < 5 && (
                  <div className={`hidden md:flex transition-colors duration-300 ${activeStep !== null && (idx === activeStep || idx === activeStep - 1) ? 'text-blue-500' : 'text-blue-200'}`}>
                    <ChevronRight size={24} className={activeStep === idx ? 'animate-pulse' : ''} />
                  </div>
                )}
                
                {/* Vertical arrow for mobile */}
                {idx < 5 && (
                  <div className={`flex md:hidden justify-center w-full my-2 transition-colors duration-300 ${activeStep !== null && (idx === activeStep || idx === activeStep - 1) ? 'text-blue-500' : 'text-blue-200'}`}>
                    <ChevronRight size={24} className={`transform rotate-90 ${activeStep === idx ? 'animate-pulse' : ''}`} />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </section>
  );
}
