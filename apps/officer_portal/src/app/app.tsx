import React from 'react';
import { AppHeader } from '../components/layout/app_header';
import { AppSidebar } from '../components/layout/app_sidebar';
import { LandQueuePage } from '../features/land_review/pages/land_queue_page';
import { useLandQueue } from '../features/land_review/hooks/use_land_queue';

export const App: React.FC = () => {
  const { data: queueItems = [] } = useLandQueue();
  const pendingCount = queueItems.filter((i) => i.status === 'pending_verification').length;

  return (
    <div className="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900">
      <AppHeader />
      <div className="flex flex-1 overflow-hidden">
        <AppSidebar pendingCount={pendingCount} />
        <main className="flex-1 overflow-hidden">
          <LandQueuePage />
        </main>
      </div>
    </div>
  );
};
