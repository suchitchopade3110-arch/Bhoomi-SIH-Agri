import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppHeader } from '../components/layout/app_header';
import { AppSidebar } from '../components/layout/app_sidebar';
import { LandQueuePage } from '../features/land_review/pages/land_queue_page';
import { VerifiedArchivePage } from '../features/land_review/pages/verified_archive_page';
import { DistrictAnalyticsPage } from '../features/land_review/pages/district_analytics_page';
import { SettingsPage } from '../features/land_review/pages/settings_page';
import { HelpGuidelinesPage } from '../features/land_review/pages/help_guidelines_page';
import { LandingPage } from '../features/landing/pages/landing_page';
import { useLandQueue } from '../features/land_review/hooks/use_land_queue';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
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
        {/* Public Landing Pages */}
        <Route path="/landing" element={<LandingPage />} />
        <Route path="/welcome" element={<LandingPage />} />

        {/* Authenticated Dashboard Workspace */}
        <Route
          path="/*"
          element={
            <Layout>
              <Routes>
                <Route path="/" element={<LandQueuePage />} />
                <Route path="/archive" element={<VerifiedArchivePage />} />
                <Route path="/analytics" element={<DistrictAnalyticsPage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="/help" element={<HelpGuidelinesPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Layout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};
