import React from 'react';
import { Settings, User, ShieldCheck, Database } from 'lucide-react';
import { env } from '../../../core/config/env';

export const SettingsPage: React.FC = () => {
  return (
    <div className="flex-1 overflow-y-auto bg-slate-50/50 p-6 lg:p-8 space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#2E7D32]/10 text-[#2E7D32]">
            <Settings className="h-5 w-5" />
          </div>
          <h1 className="text-xl font-extrabold text-slate-900">Officer Portal Settings</h1>
        </div>
        <p className="mt-1 text-xs text-slate-500">
          Revenue Administration Officer Profile, Jurisdiction, and API Configuration
        </p>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* Officer Identity Card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-4">
            <User className="h-4 w-4 text-[#2E7D32]" />
            <h3 className="text-sm font-bold text-slate-900">Officer Profile Credentials</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">Officer Name</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                Tmt. K. Bhavani, VAO
              </div>
            </div>

            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">Officer Role / Designation</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                Village Administrative Officer (VAO)
              </div>
            </div>

            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">Assigned Taluk</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                Erode Taluk Revenue Division
              </div>
            </div>

            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">District Jurisdiction</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                Erode District, Tamil Nadu
              </div>
            </div>
          </div>
        </div>

        {/* API & Security Configuration */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-4">
            <Database className="h-4 w-4 text-[#2E7D32]" />
            <h3 className="text-sm font-bold text-slate-900">API Connection & System Status</h3>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 border border-slate-200/60">
              <div>
                <span className="font-bold text-slate-800">API Base URL</span>
                <p className="text-[11px] text-slate-500 font-mono">{env.apiBaseUrl || 'http://localhost:8000'}</p>
              </div>
              <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800">
                Connected
              </span>
            </div>

            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 border border-slate-200/60">
              <div>
                <span className="font-bold text-slate-800">Security & Signatures</span>
                <p className="text-[11px] text-slate-500">Official review actions are cryptographically signed with officer token.</p>
              </div>
              <ShieldCheck className="h-5 w-5 text-emerald-600" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
