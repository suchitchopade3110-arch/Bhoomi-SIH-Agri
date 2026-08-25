import React from 'react';
import {
  ShieldCheck,
  Map,
  Star,
  Layers,
  Mic,
} from 'lucide-react';


export default function HeroSection({
  onOpenOfficerPortal,
  onOpenVoiceModal,
}) {
  return (
    <section id="hero" className="relative min-h-screen flex items-center pt-20 pb-16 overflow-hidden">
      
      {/* Background Image and Gradients */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center"
        style={{ backgroundImage: "url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop')" }}
      >
        {/* Gradient to make top white (blends with navbar) and bottom clear */}
        <div className="absolute inset-0 bg-gradient-to-b from-white via-white/60 to-transparent/30"></div>
        {/* Subtle green/blue tint for theme */}
        <div className="absolute inset-0 bg-green-900/10 mix-blend-overlay"></div>
      </div>

      <div className="container mx-auto px-6 relative z-30">
        <div className="max-w-4xl mx-auto flex flex-col items-center justify-center text-center">
          
          <div className="space-y-6 flex flex-col items-center">
            
            {/* Badge */}
            <div className="inline-flex items-center gap-2 bg-blue-50/90 backdrop-blur text-blue-800 px-4 py-2 rounded-full text-sm font-bold border border-blue-200 shadow-sm">
              <ShieldCheck className="w-5 h-5 text-blue-600" />
              Government Authorized Portal
            </div>

            {/* Main Heading */}
            <h1 className="font-display text-4xl sm:text-5xl lg:text-[4rem] font-bold tracking-tight text-slate-900 leading-[1.05] text-center">
              Streamline Verification.<br />
              Empower Farmers.<br />
              <span className="text-blue-600">Disburse Subsidies.</span>
            </h1>

            {/* Supporting Text */}
            <p className="text-base lg:text-xl text-slate-800 max-w-2xl font-semibold leading-relaxed text-center">
              Your dedicated portal to validate cadastral boundaries, approve farm profiles, and unlock gated subsidies efficiently across your jurisdiction.
            </p>

            {/* Call to Actions */}
            <div className="flex flex-col items-center gap-4 pt-4 w-full sm:w-auto">
              <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
                <button
                  onClick={onOpenOfficerPortal}
                  className="w-full sm:w-auto bg-[#1b8c47] hover:bg-green-700 text-white py-4 px-10 rounded-full text-lg font-bold flex items-center justify-center gap-3 shadow-xl shadow-green-900/30 transition-transform hover:scale-105"
                >
                  <Map className="w-6 h-6" />
                  <span>Open Verification Dashboard</span>
                </button>

                <button
                  onClick={onOpenVoiceModal}
                  className="w-full sm:w-auto bg-white border-2 border-emerald-600 text-emerald-700 hover:bg-emerald-50 py-4 px-8 rounded-full text-lg font-bold flex items-center justify-center gap-3 shadow-sm transition-transform hover:scale-105"
                >
                  <Mic className="w-6 h-6" />
                  <span>Ask Bhoomi (Voice Demo)</span>
                </button>
              </div>
            </div>



          </div>

        </div>
      </div>
      
      {/* Curvy divider SVG */}
      <div className="absolute bottom-0 left-0 w-full overflow-hidden leading-none z-10">
        <svg className="relative block w-full h-[60px] md:h-[120px]" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,60 C300,120 900,0 1200,60 L1200,120 L0,120 Z" fill="#ffffff"></path>
        </svg>
      </div>
    </section>
  );
}
