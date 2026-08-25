import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authStore } from '../../core/auth/auth_store';
import { Bell, UserCircle2, CheckCheck, AlertCircle, Clock, CheckCircle2, ChevronRight, X } from 'lucide-react';
import bhoomiLogo from '../../assets/bhoomi_logo.png';

interface NotificationItem {
  id: string;
  title: string;
  description: string;
  time: string;
  priority: 'high' | 'medium' | 'low';
  read: boolean;
  caseId?: string;
}

const INITIAL_NOTIFICATIONS: NotificationItem[] = [
  {
    id: 'n1',
    title: 'High Priority Escalation',
    description: 'Farmer Murugan (Erode, Samba Paddy 2.0 Ac) submitted low confidence diagnosis (0.58). ICAR expert review required.',
    time: '5m ago',
    priority: 'high',
    read: false,
    caseId: 'case-001',
  },
  {
    id: 'n2',
    title: 'Follow-Up Check-In Ready',
    description: 'Farmer Selvan reported 48h check-in for Stem Borer bio-control. Verification needed.',
    time: '25m ago',
    priority: 'medium',
    read: false,
    caseId: 'case-002',
  },
  {
    id: 'n3',
    title: 'Advisory Delivered Successfully',
    description: 'Potassium deficiency resolution protocol acknowledged by Farmer Ramesh.',
    time: '2h ago',
    priority: 'low',
    read: true,
    caseId: 'case-003',
  },
];

export const AppHeader: React.FC = () => {
  const agronomist = authStore.getCurrentAgronomist();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState<NotificationItem[]>(INITIAL_NOTIFICATIONS);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter((n) => !n.read).length;

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const handleNotificationClick = (item: NotificationItem) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === item.id ? { ...n, read: true } : n))
    );
    setIsOpen(false);
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white/95 px-6 backdrop-blur-xs">
      {/* Branding */}
      <div className="flex items-center gap-3">
        <img
          src={bhoomiLogo}
          alt="BHOOMI Logo"
          className="h-10 w-10 rounded-xl object-contain shadow-xs border border-slate-100 bg-white p-0.5"
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/bhoomi_logo.png';
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

      {/* Right User Status & Notification Dropdown */}
      <div className="flex items-center gap-4">
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsOpen((prev) => !prev)}
            className={`relative rounded-lg p-2 transition-colors cursor-pointer ${
              isOpen ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-700'
            }`}
            title="Notifications"
          >
            <Bell className="h-5 w-5" />
            {unreadCount > 0 && (
              <span className="absolute top-1.5 right-1.5 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#2E7D32] opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#2E7D32]"></span>
              </span>
            )}
          </button>

          {/* Notification Popover Dropdown */}
          {isOpen && (
            <div className="absolute right-0 mt-2 w-96 rounded-2xl border border-slate-200 bg-white shadow-2xl z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
              {/* Header */}
              <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3 bg-slate-50/80">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-slate-900">Notifications</span>
                  {unreadCount > 0 && (
                    <span className="rounded-full bg-[#2E7D32]/15 px-2 py-0.5 text-[11px] font-extrabold text-[#2E7D32]">
                      {unreadCount} New
                    </span>
                  )}
                </div>
                {unreadCount > 0 && (
                  <button
                    onClick={markAllAsRead}
                    className="flex items-center gap-1 text-xs font-semibold text-[#2E7D32] hover:text-[#1B5E20] transition-colors cursor-pointer"
                  >
                    <CheckCheck className="h-3.5 w-3.5" />
                    Mark all read
                  </button>
                )}
              </div>

              {/* Notification List */}
              <div className="max-h-[380px] overflow-y-auto divide-y divide-slate-100">
                {notifications.length === 0 ? (
                  <div className="p-8 text-center text-slate-400">
                    <Bell className="mx-auto h-8 w-8 text-slate-300 mb-2" />
                    <p className="text-xs font-medium">No new notifications</p>
                  </div>
                ) : (
                  notifications.map((item) => (
                    <div
                      key={item.id}
                      onClick={() => handleNotificationClick(item)}
                      className={`p-3.5 transition-colors cursor-pointer hover:bg-slate-50 flex gap-3 items-start ${
                        !item.read ? 'bg-emerald-50/25' : ''
                      }`}
                    >
                      <div className="mt-0.5 shrink-0">
                        {item.priority === 'high' ? (
                          <div className="h-7 w-7 rounded-full bg-red-100 text-red-600 flex items-center justify-center">
                            <AlertCircle className="h-4 w-4" />
                          </div>
                        ) : item.priority === 'medium' ? (
                          <div className="h-7 w-7 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center">
                            <Clock className="h-4 w-4" />
                          </div>
                        ) : (
                          <div className="h-7 w-7 rounded-full bg-emerald-100 text-[#2E7D32] flex items-center justify-center">
                            <CheckCircle2 className="h-4 w-4" />
                          </div>
                        )}
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-1">
                          <p className={`text-xs ${!item.read ? 'font-bold text-slate-900' : 'font-semibold text-slate-700'}`}>
                            {item.title}
                          </p>
                          <span className="text-[10px] text-slate-400 shrink-0">{item.time}</span>
                        </div>
                        <p className="text-[11px] text-slate-600 mt-1 line-clamp-2 leading-relaxed">
                          {item.description}
                        </p>
                      </div>

                      {!item.read && (
                        <span className="mt-1.5 h-2 w-2 rounded-full bg-[#2E7D32] shrink-0" />
                      )}
                    </div>
                  ))
                )}
              </div>

              {/* Footer */}
              <div className="border-t border-slate-100 p-2.5 bg-slate-50 text-center">
                <Link
                  to="/"
                  onClick={() => setIsOpen(false)}
                  className="inline-flex items-center gap-1 text-xs font-bold text-[#2E7D32] hover:text-[#1B5E20] transition-colors"
                >
                  View Escalation Case Queue
                  <ChevronRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          )}
        </div>

        <div className="h-6 w-px bg-slate-200" />

        <Link
          to="/settings"
          className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity select-none"
        >
          <div className="text-right">
            <div className="text-xs font-bold text-slate-900">{agronomist.name}</div>
            <div className="text-[10px] font-medium text-slate-500">{agronomist.specialization}</div>
          </div>
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-slate-600">
            <UserCircle2 className="h-6 w-6" />
          </div>
        </Link>
      </div>
    </header>
  );
};
