import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppHeader } from '../components/layout/app_header';
import { AppSidebar } from '../components/layout/app_sidebar';
import { CaseQueuePage } from '../features/cases/pages/case_queue_page';

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen flex-col bg-slate-50">
        <AppHeader />
        <div className="flex flex-1 overflow-hidden">
          <AppSidebar />
          <main className="flex-1 overflow-hidden">
            <Routes>
              <Route path="/" element={<CaseQueuePage />} />
              <Route path="/review" element={<CaseQueuePage statusFilter="under_review" />} />
              <Route path="/history" element={<CaseQueuePage statusFilter="resolved" />} />
              <Route path="/logs" element={<CaseQueuePage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
};
