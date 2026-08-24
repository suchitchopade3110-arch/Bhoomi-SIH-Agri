import React from 'react';
import { X } from 'lucide-react';

export default function OfficerPortalModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex flex-col text-slate-900 animate-fade-in bg-white overflow-hidden">
      
      {/* 
        ========================================================================
        PLACEHOLDER WRAPPER
        ========================================================================
        This is a full-screen modal container. 
        Import and drop your actual Dashboard component below.
        
        Example:
        import MyRealDashboard from './MyRealDashboard';
        ...
        <div className="flex-grow overflow-auto">
          <MyRealDashboard />
        </div>
        ========================================================================
      */}

      {/* Header with Close Button (Optional, can be removed if your dashboard has its own navigation/close) */}
      <div className="absolute top-4 right-6 z-[60]">
        <button 
          onClick={onClose}
          className="p-2 rounded-full bg-white shadow-md border border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-colors"
          title="Close Dashboard"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      {/* Your Dashboard Component Goes Here */}
      <div className="flex-grow w-full h-full overflow-y-auto flex items-center justify-center bg-slate-50">
        <div className="text-center space-y-4">
          <h2 className="text-2xl font-bold text-slate-400">Dashboard Placeholder</h2>
          <p className="text-slate-500">Connect your external dashboard file here.</p>
        </div>
      </div>
      
    </div>
  );
}
