import React from 'react';
import { authStore } from '../../core/auth/auth_store';
import { Bell, UserCircle2 } from 'lucide-react';
import bhoomiLogo from '../../assets/bhoomi.png';

export const AppHeader: React.FC = () => {
  const agronomist = authStore.getCurrentAgronomist();

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white/95 px-6 backdrop-blur-xs">
      {/* Branding */}
      <div className="flex items-center gap-3">
        <img
          src={bhoomiLogo}
          alt="BHOOMI Logo"
          className="h-10 w-10 rounded-xl object-contain shadow-xs border border-slate-100 bg-emerald-50/50 p-0.5"
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/bhoomi.png';
          }}
        />
        <div>
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-base tracking-tight text-slate-900">BHOOMI</span>
            <span className="rounded bg-[#2E7D32]/10 px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider text-[#2E7D32]">
              KVK AGRONOMIST PORTAL
            </span>
          </div>
          <p className="text-[11px] text-slate-500">{agronomist.kvkCenter}</p>
        </div>
      </div>

      {/* Right User Status */}
      <div className="flex items-center gap-4">
        <button className="relative rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-[#2E7D32]" />
        </button>

        <div className="h-6 w-px bg-slate-200" />

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs font-bold text-slate-900">{agronomist.name}</div>
            <div className="text-[10px] font-medium text-slate-500">{agronomist.specialization}</div>
          </div>
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-slate-600">
            <UserCircle2 className="h-6 w-6" />
          </div>
        </div>
      </div>
    </header>
  );
};
