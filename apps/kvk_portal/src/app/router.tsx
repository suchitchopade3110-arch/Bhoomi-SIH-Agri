import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppHeader } from '../components/layout/app_header';
import { AppSidebar } from '../components/layout/app_sidebar';
import { CaseQueuePage } from '../features/cases/pages/case_queue_page';
import { TreatmentEfficacyPage } from '../features/cases/pages/treatment_efficacy_page';
import { SettingsPage } from '../features/cases/pages/settings_page';
import { KvkLandingPage } from '../features/landing/pages/kvk_landing_page';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <AppHeader />
      <div className="flex flex-1 overflow-hidden">
        <AppSidebar />
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
};

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public KVK Landing Experience */}
        <Route path="/" element={<KvkLandingPage />} />
        <Route path="/landing" element={<KvkLandingPage />} />
        <Route path="/welcome" element={<KvkLandingPage />} />

        {/* Authenticated / Agronomist Console Routes */}
        <Route
          path="/queue"
          element={
            <DashboardLayout>
              <CaseQueuePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/cases"
          element={
            <DashboardLayout>
              <CaseQueuePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/dashboard"
          element={
            <DashboardLayout>
              <CaseQueuePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/review"
          element={
            <DashboardLayout>
              <CaseQueuePage statusFilter="under_review" />
            </DashboardLayout>
          }
        />
        <Route
          path="/history"
          element={
            <DashboardLayout>
              <CaseQueuePage statusFilter="resolved" />
            </DashboardLayout>
          }
        />
        <Route
          path="/efficacy"
          element={
            <DashboardLayout>
              <TreatmentEfficacyPage />
            </DashboardLayout>
          }
        />
        <Route
          path="/settings"
          element={
            <DashboardLayout>
              <SettingsPage />
            </DashboardLayout>
          }
        />
        <Route
          path="/logs"
          element={
            <DashboardLayout>
              <CaseQueuePage />
            </DashboardLayout>
          }
        />

        {/* Wildcard Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};


