import React from 'react';
import { Settings, User, ShieldCheck, Database } from 'lucide-react';
import { env } from '../../../core/config/env';
import { authStore } from '../../../core/auth/auth_store';

export const SettingsPage: React.FC = () => {
  const agronomist = authStore.getCurrentAgronomist();

  return (
    <div className="flex-1 overflow-y-auto bg-slate-50/50 p-6 lg:p-8 space-y-6">
      <div>
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#2E7D32]/10 text-[#2E7D32]">
            <Settings className="h-5 w-5" />
          </div>
          <h1 className="text-xl font-extrabold text-slate-900">Agronomist Portal Settings</h1>
        </div>
        <p className="mt-1 text-xs text-slate-500">
          KVK Agronomist Profile, Center Details, and API Configuration
        </p>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* Agronomist Identity Card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-4">
            <User className="h-4 w-4 text-[#2E7D32]" />
            <h3 className="text-sm font-bold text-slate-900">Agronomist Profile Credentials</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">Agronomist Name</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                {agronomist.name}
              </div>
            </div>

            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">Designation / Role</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                Subject Matter Specialist (SMS) &bull; Agronomy
              </div>
            </div>

            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">KVK Center</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                {agronomist.kvkCenter}
              </div>
            </div>

            <div>
              <label className="font-bold text-slate-500 uppercase text-[10px]">Core Specialization</label>
              <div className="mt-1 rounded-xl bg-slate-50 p-3 font-semibold text-slate-800 border border-slate-200/60">
                {agronomist.specialization}
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
                <p className="text-[11px] text-slate-500">Official prescriptions are cryptographically signed with certified credentials.</p>
              </div>
              <ShieldCheck className="h-5 w-5 text-emerald-600" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
