import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Inbox,
  CheckCircle2,
  AlertTriangle,
  History,
  HelpCircle,
  Activity,
  Settings,
} from 'lucide-react';

export const AppSidebar: React.FC = () => {
  const navItems = [
    { label: 'Escalated Cases', path: '/', icon: Inbox, badge: '3' },
    { label: 'Under Review', path: '/review', icon: AlertTriangle },
    { label: 'Resolved History', path: '/history', icon: CheckCircle2 },
    { label: 'Treatment Efficacy', path: '/efficacy', icon: Activity },
    { label: 'Activity Logs', path: '/logs', icon: History },
  ];

  const systemItems = [
    { label: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="flex h-[calc(100vh-4rem)] w-64 flex-col justify-between border-r border-slate-200 bg-white p-4">
      <div className="space-y-6">
        <div>
          <div className="px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Case Management
          </div>
          <nav className="mt-2 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
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
                  <span
                    className={`rounded-full px-2 py-0.5 text-[10px] font-extrabold ${
                      item.path === '/'
                        ? 'bg-white/20 text-white'
                        : 'bg-slate-100 text-slate-600'
                    }`}
                  >
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
            {systemItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
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

      {/* Support Info Footer */}
      <div className="rounded-xl border border-slate-100 bg-slate-50/80 p-3.5">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
          <HelpCircle className="h-4 w-4 text-[#2E7D32]" />
          <span>KVK Extension Guide</span>
        </div>
        <p className="mt-1 text-[11px] text-slate-500">
          Review crop photographs and prescribe scientific management based on TNAU/ICAR bulletins.
        </p>
      </div>
    </aside>
  );
};
