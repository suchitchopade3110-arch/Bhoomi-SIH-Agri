import React from 'react';
import { 
  ShieldCheck, 
  LayoutDashboard, 
  Map, 
  FileCheck, 
  BarChart3, 
  Bell, 
  User, 
  Settings, 
  HelpCircle,
  MapPin,
  CheckCircle2,
  XCircle,
  Clock,
  Search
} from 'lucide-react';

export default function DashboardPreviewSection({ onOpenOfficerPortal }) {
  return (
    <section id="dashboard-preview" className="py-24 bg-white">
      <div className="container mx-auto px-6 flex flex-col xl:flex-row items-center gap-16">
        
        {/* Left Content */}
        <div className="flex-1 max-w-lg">
          <div className="inline-flex items-center gap-2 text-blue-600 text-xs font-bold uppercase tracking-wider mb-4">
            <ShieldCheck size={14} fill="currentColor" /> YOUR VERIFICATION HUB
          </div>
          <h2 className="text-4xl font-bold text-slate-900 mb-6 leading-tight">
            Govern with clarity and confidence
          </h2>
          <p className="text-slate-600 mb-8 leading-relaxed text-lg">
            Review pending profiles, cross-reference with official cadastral maps, and disburse subsidies to verified farmers seamlessly.
          </p>
          <button onClick={onOpenOfficerPortal} className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md font-bold inline-flex items-center gap-2 transition-colors shadow-md">
            Open Portal &rarr;
          </button>
          

        </div>

        {/* Right Dashboard Mockup */}
        <div className="flex-[1.5] w-full max-w-5xl bg-[#0f172a] rounded-3xl overflow-hidden shadow-[0_30px_60px_-15px_rgba(0,0,0,0.3)] flex text-sm">
          
          {/* Sidebar */}
          <div className="w-56 p-6 flex flex-col text-slate-400">
            <div className="flex items-center gap-2 text-white font-bold text-xl mb-10">
              <ShieldCheck size={24} fill="currentColor" className="text-blue-500" /> Bhoomi
            </div>
            
            <nav className="flex-1 space-y-2">
              <a href="#" className="flex items-center gap-3 bg-white/10 text-white px-4 py-2.5 rounded-lg font-medium"><LayoutDashboard size={18} /> Dashboard</a>
              <a href="#" className="flex items-center gap-3 hover:bg-white/5 hover:text-white px-4 py-2.5 rounded-lg transition-colors"><FileCheck size={18} /> Approvals <span className="ml-auto bg-blue-600 text-white text-[10px] px-2 py-0.5 rounded-full">18</span></a>
              <a href="#" className="flex items-center gap-3 hover:bg-white/5 hover:text-white px-4 py-2.5 rounded-lg transition-colors"><Map size={18} /> Cadastral Maps</a>
              <a href="#" className="flex items-center gap-3 hover:bg-white/5 hover:text-white px-4 py-2.5 rounded-lg transition-colors"><BarChart3 size={18} /> Analytics</a>
              <a href="#" className="flex items-center gap-3 hover:bg-white/5 hover:text-white px-4 py-2.5 rounded-lg transition-colors"><Bell size={18} /> Alerts</a>
              <a href="#" className="flex items-center gap-3 hover:bg-white/5 hover:text-white px-4 py-2.5 rounded-lg transition-colors"><User size={18} /> Profile</a>
              <a href="#" className="flex items-center gap-3 hover:bg-white/5 hover:text-white px-4 py-2.5 rounded-lg transition-colors"><Settings size={18} /> Settings</a>
            </nav>

            <a href="#" className="flex items-center gap-2 mt-auto hover:text-white py-2"><HelpCircle size={16} /> Officer Support</a>
          </div>

          {/* Main Dashboard Area */}
          <div className="flex-1 bg-slate-50 m-2 rounded-2xl p-8 overflow-hidden flex flex-col gap-6">
            
            {/* Topbar */}
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-2xl font-bold text-slate-900 flex items-center gap-2">Officer Dashboard</h3>
                <p className="text-slate-500 text-sm">Thanjavur Taluk Jurisdiction Overview</p>
              </div>
              <div className="flex items-center gap-4">
                <div className="bg-white border border-slate-200 px-3 py-1.5 rounded-md flex items-center gap-2 text-slate-400">
                  <Search size={16} /> <span className="text-xs">Search survey numbers...</span>
                </div>
                <div className="flex items-center gap-1.5 text-slate-600 text-sm font-bold bg-white px-3 py-1.5 rounded-md shadow-sm border border-slate-100">
                  <MapPin size={16} className="text-blue-500" /> Thanjavur, TN
                </div>
              </div>
            </div>

            {/* Top Cards Row */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                <div className="text-xs font-semibold text-slate-500 mb-1">Pending Verifications</div>
                <div className="font-black text-slate-900 text-3xl mb-2">18</div>
                <div className="text-xs font-semibold text-amber-600 bg-amber-50 px-2 py-0.5 rounded inline-block">Action Required</div>
                <div className="absolute -bottom-2 -right-2 text-slate-100">
                  <FileCheck size={64} fill="currentColor" />
                </div>
              </div>
              
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 mb-2">Subsidy Disbursed (MTD)</div>
                <div className="flex items-end gap-3 mb-4">
                  <div className="text-3xl font-black text-emerald-600 leading-none">₹ 4.2L</div>
                </div>
                <a href="#" className="text-blue-600 text-xs font-bold flex items-center gap-1 hover:underline">View Transaction Log &rarr;</a>
              </div>

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 mb-2">Total Verified Farmers</div>
                <div className="text-3xl font-black text-slate-800 leading-none mb-4">1,204</div>
                <a href="#" className="text-blue-600 text-xs font-bold flex items-center gap-1 hover:underline">View Registry &rarr;</a>
              </div>
            </div>

            {/* Bottom Row - Split Pane */}
            <div className="grid grid-cols-[3fr_2fr] gap-6">
              
              {/* Queue */}
              <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
                <div className="p-4 border-b border-slate-100 bg-slate-50">
                  <div className="text-sm font-bold text-slate-800">Priority Verification Queue</div>
                </div>
                <div className="p-0">
                  {/* Row 1 */}
                  <div className="p-4 border-b border-slate-50 flex items-center justify-between hover:bg-slate-50">
                    <div>
                      <div className="font-bold text-slate-800 text-sm">V. Kumar (Survey 142/3B)</div>
                      <div className="text-xs text-slate-500">2 Acres • Paddy • Village Boundary</div>
                    </div>
                    <button className="bg-blue-50 text-blue-700 font-bold text-xs px-3 py-1.5 rounded-lg border border-blue-200 hover:bg-blue-100">Review</button>
                  </div>
                  {/* Row 2 */}
                  <div className="p-4 border-b border-slate-50 flex items-center justify-between hover:bg-slate-50">
                    <div>
                      <div className="font-bold text-slate-800 text-sm">S. Rajendran (Survey 89/1A)</div>
                      <div className="text-xs text-slate-500">5 Acres • Sugarcane • Subsidy Claim</div>
                    </div>
                    <button className="bg-blue-50 text-blue-700 font-bold text-xs px-3 py-1.5 rounded-lg border border-blue-200 hover:bg-blue-100">Review</button>
                  </div>
                </div>
                <div className="p-3 mt-auto text-center border-t border-slate-100">
                  <a href="#" className="text-blue-600 text-xs font-bold hover:underline">View All 18 Pending &rarr;</a>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-slate-900 text-slate-300 p-5 rounded-xl shadow-sm relative overflow-hidden flex flex-col">
                <div className="text-xs font-semibold text-slate-400 mb-4 uppercase tracking-wider">System Audit Log</div>
                <div className="space-y-4 flex-1">
                  <div className="flex items-start gap-3 text-xs">
                    <CheckCircle2 size={16} className="text-emerald-500 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-white font-semibold">Survey 45/2A Verified</span>
                      <p className="text-slate-500 mt-0.5">Approved by Off. Ramesh • 10m ago</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 text-xs">
                    <XCircle size={16} className="text-rose-500 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-white font-semibold">Anomaly Detected</span>
                      <p className="text-slate-500 mt-0.5">Survey 12/B area mismatch • 1h ago</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 text-xs">
                    <Map size={16} className="text-blue-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-white font-semibold">Cadastral Sync</span>
                      <p className="text-slate-500 mt-0.5">Maps updated from State DB • 3h ago</p>
                    </div>
                  </div>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
    </section>
  );
}
