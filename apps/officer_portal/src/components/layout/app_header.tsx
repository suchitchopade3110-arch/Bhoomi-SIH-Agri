import React from 'react';
import { Link } from 'react-router-dom';
import { UserCheck, Activity } from 'lucide-react';
import { authStore } from '../../core/auth/auth_store';
import bhoomiLogo from '../../assets/bhoomi.png';

export const AppHeader: React.FC = () => {
  const officer = authStore.getCurrentOfficer();

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-slate-200/80 bg-white px-6 shadow-xs">
      {/* Brand & Emblem */}
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
            <span className="text-base font-extrabold tracking-tight text-slate-900">
              BHOOMI
            </span>
            <span className="rounded bg-[#2E7D32]/10 px-1.5 py-0.5 text-[10px] font-bold text-[#2E7D32]">
              OFFICER PORTAL
            </span>
          </div>
          <p className="text-[11px] font-medium text-slate-500">
            Smart Land Verification System &bull; SIH25076
          </p>
        </div>
      </div>

      {/* Right Side: Officer Profile & Status */}
      <div className="flex items-center gap-4">
        {/* System API Status */}
        <div className="hidden sm:flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50/80 px-3 py-1 text-xs">
          <Activity className="h-3.5 w-3.5 text-[#2E7D32] animate-pulse" />
          <span className="font-semibold text-slate-700">API: /api/v1</span>
          <span className="h-1.5 w-1.5 rounded-full bg-[#2E7D32]" />
        </div>

        {/* Officer Badge */}
        <Link
          to="/settings"
          className="flex items-center gap-3 border-l border-slate-200 pl-4 cursor-pointer hover:opacity-80 transition-opacity select-none"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#2E7D32]/10 text-[#2E7D32]">
            <UserCheck className="h-4 w-4" />
          </div>
          <div className="text-left hidden md:block">
            <div className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <span>{officer.name}</span>
              <span className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.2 rounded font-mono">
                {officer.verifierTag}
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium">
              {officer.jurisdiction}
            </p>
          </div>
        </Link>
      </div>
    </header>
  );
};
