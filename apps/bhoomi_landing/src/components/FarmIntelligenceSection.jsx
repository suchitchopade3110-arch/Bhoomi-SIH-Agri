import React from 'react';
import { 
  Map, 
  FileCheck, 
  BarChart3, 
  Users, 
  ShieldAlert,
  Database,
  ShieldCheck
} from 'lucide-react';

export default function FarmIntelligenceSection() {
  return (
    <section id="features" className="py-20 bg-white relative z-20">
      <style>
        {`
          @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
            100% { transform: translateY(0px); }
          }
          .animate-float { animation: float 6s ease-in-out infinite; }
          .animate-float-delay-1 { animation: float 6s ease-in-out 1s infinite; }
          .animate-float-delay-2 { animation: float 6s ease-in-out 2s infinite; }
        `}
      </style>

      <div className="container mx-auto px-6 text-center">
        <div className="inline-flex items-center gap-2 text-blue-600 text-xs font-bold uppercase tracking-wider mb-2">
          <ShieldCheck size={14} fill="currentColor" /> CORE CAPABILITIES
        </div>
        <h2 className="text-3xl font-bold text-slate-900 mb-12">Everything you need to govern effectively</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {/* Card 1 */}
          <div className="animate-float bg-white border-2 border-slate-100 hover:border-blue-500 rounded-3xl p-8 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-10px_rgba(37,99,235,0.2)] transition-all duration-500 flex flex-col items-center text-center group cursor-pointer">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
              <Map size={28} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">Land<br/>Verification</h3>
            <p className="text-sm text-slate-600 leading-relaxed group-hover:text-slate-800 transition-colors">Match claimed boundaries against official cadastral maps instantly.</p>
          </div>
          
          {/* Card 2 */}
          <div className="animate-float-delay-1 bg-white border-2 border-slate-100 hover:border-blue-500 rounded-3xl p-8 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-10px_rgba(37,99,235,0.2)] transition-all duration-500 flex flex-col items-center text-center group cursor-pointer">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
              <FileCheck size={28} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">Subsidy<br/>Approvals</h3>
            <p className="text-sm text-slate-600 leading-relaxed group-hover:text-slate-800 transition-colors">One-click disbursement workflow after successful AI pre-checks.</p>
          </div>

          {/* Card 3 */}
          <div className="animate-float-delay-2 bg-white border-2 border-slate-100 hover:border-blue-500 rounded-3xl p-8 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-10px_rgba(37,99,235,0.2)] transition-all duration-500 flex flex-col items-center text-center group cursor-pointer">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
              <BarChart3 size={28} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">Regional<br/>Analytics</h3>
            <p className="text-sm text-slate-600 leading-relaxed group-hover:text-slate-800 transition-colors">View aggregated farm health, crop distributions, and risk heatmaps.</p>
          </div>

          {/* Card 4 */}
          <div className="animate-float bg-white border-2 border-slate-100 hover:border-blue-500 rounded-3xl p-8 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-10px_rgba(37,99,235,0.2)] transition-all duration-500 flex flex-col items-center text-center group cursor-pointer">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
              <Users size={28} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">Agronomist<br/>Collaboration</h3>
            <p className="text-sm text-slate-600 leading-relaxed group-hover:text-slate-800 transition-colors">Sync directly with KVK desks for complex agricultural problem resolution.</p>
          </div>

          {/* Card 5 */}
          <div className="animate-float-delay-1 bg-white border-2 border-slate-100 hover:border-blue-500 rounded-3xl p-8 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-10px_rgba(37,99,235,0.2)] transition-all duration-500 flex flex-col items-center text-center group cursor-pointer">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
              <ShieldAlert size={28} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">Fraud<br/>Prevention</h3>
            <p className="text-sm text-slate-600 leading-relaxed group-hover:text-slate-800 transition-colors">AI automatically flags anomalies in claims versus satellite data.</p>
          </div>

          {/* Card 6 */}
          <div className="animate-float-delay-2 bg-white border-2 border-slate-100 hover:border-blue-500 rounded-3xl p-8 shadow-[0_4px_20px_-10px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-10px_rgba(37,99,235,0.2)] transition-all duration-500 flex flex-col items-center text-center group cursor-pointer">
            <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
              <Database size={28} />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">Secure<br/>Records</h3>
            <p className="text-sm text-slate-600 leading-relaxed group-hover:text-slate-800 transition-colors">Immutable history of all verifications, claims, and officer actions.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
