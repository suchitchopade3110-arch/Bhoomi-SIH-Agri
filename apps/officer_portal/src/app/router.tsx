import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppHeader } from '../components/layout/app_header';
import { AppSidebar } from '../components/layout/app_sidebar';
import { LandQueuePage } from '../features/land_review/pages/land_queue_page';
import { VerifiedArchivePage } from '../features/land_review/pages/verified_archive_page';
import { DistrictAnalyticsPage } from '../features/land_review/pages/district_analytics_page';
import { SettingsPage } from '../features/land_review/pages/settings_page';
import { HelpGuidelinesPage } from '../features/land_review/pages/help_guidelines_page';
import { useLandQueue } from '../features/land_review/hooks/use_land_queue';
import { OfficerLandingPage } from '../features/landing/pages/officer_landing_page';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { data: queueItems = [] } = useLandQueue();
  const pendingCount = queueItems.filter((i) => i.status === 'pending_verification').length;

  return (
    <div className="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900">
      <AppHeader />
      <div className="flex flex-1 overflow-hidden">
        <AppSidebar pendingCount={pendingCount} />
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
};

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Officer Landing Experience */}
        <Route path="/" element={<OfficerLandingPage />} />
        <Route path="/landing" element={<OfficerLandingPage />} />
        <Route path="/welcome" element={<OfficerLandingPage />} />

        {/* Operational Officer Workspace Routes */}
        <Route
          path="/queue"
          element={
            <DashboardLayout>
              <LandQueuePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/land"
          element={
            <DashboardLayout>
              <LandQueuePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/dashboard"
          element={
            <DashboardLayout>
              <LandQueuePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/archive"
          element={
            <DashboardLayout>
              <VerifiedArchivePage />
            </DashboardLayout>
          }
        />
        <Route
          path="/analytics"
          element={
            <DashboardLayout>
              <DistrictAnalyticsPage />
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
          path="/help"
          element={
            <DashboardLayout>
              <HelpGuidelinesPage />
            </DashboardLayout>
          }
        />

        {/* Wildcard Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

