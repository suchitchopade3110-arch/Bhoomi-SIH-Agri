import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Layers,
  Archive,
  BarChart3,
  Settings,
  HelpCircle,
  FileCheck2,
} from 'lucide-react';

interface AppSidebarProps {
  pendingCount?: number;
}

export const AppSidebar: React.FC<AppSidebarProps> = ({ pendingCount = 0 }) => {
  const operationsNav = [
    {
      to: '/',
      label: 'Land Queue',
      icon: FileCheck2,
      badge: pendingCount > 0 ? pendingCount.toString() : undefined,
    },
    {
      to: '/archive',
      label: 'Verified Archive',
      icon: Archive,
    },
    {
      to: '/analytics',
      label: 'District Analytics',
      icon: BarChart3,
    },
  ];

  const systemNav = [
    {
      to: '/settings',
      label: 'Settings',
      icon: Settings,
    },
    {
      to: '/help',
      label: 'Help & Guidelines',
      icon: HelpCircle,
    },
  ];

  return (
    <aside className="hidden lg:flex w-64 flex-col justify-between border-r border-slate-200/80 bg-white p-4">
      {/* Navigation Links */}
      <div className="space-y-6">
        <div>
          <div className="px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Operations
          </div>
          <nav className="mt-2 space-y-1">
            {operationsNav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) =>
                  `flex items-center justify-between rounded-xl px-3 py-2.5 text-xs font-bold transition-all ${
                    isActive
                      ? 'bg-[#2E7D32] text-white shadow-xs'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <item.icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="rounded-full bg-white/20 px-2 py-0.5 text-[11px] font-bold text-white shadow-xs">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            ))}
          </nav>
        </div>

        <div>
          <div className="px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            System
          </div>
          <nav className="mt-2 space-y-1">
            {systemNav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-bold transition-all ${
                    isActive
                      ? 'bg-[#2E7D32] text-white shadow-xs'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`
                }
              >
                <item.icon className="h-4 w-4" />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </div>

      {/* Footer Info Box */}
      <div className="rounded-xl border border-slate-200/80 bg-slate-50 p-3.5 text-xs text-slate-500">
        <div className="flex items-center gap-2 font-bold text-slate-700">
          <Layers className="h-4 w-4 text-[#2E7D32]" />
          <span>BHOOMI Officer Portal</span>
        </div>
        <p className="mt-1 text-[11px] text-slate-500">
          Land Verification System • SIH25076
        </p>
      </div>
    </aside>
  );
};
