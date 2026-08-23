import React, { useState, useEffect } from 'react';
import { useLandQueue } from '../hooks/use_land_queue';
import { LandQueueList } from '../components/land_queue_list';
import { LandDetailPanel } from '../components/land_detail_panel';
import { LandQueueItem } from '../types/land.types';

export const LandQueuePage: React.FC = () => {
  const { data: queueItems = [], isLoading, isError, error, refetch } = useLandQueue();
  const [selectedRecordId, setSelectedRecordId] = useState<string | null>(null);

  // Auto-select first item when loaded if none selected
  useEffect(() => {
    if (queueItems.length > 0 && !selectedRecordId) {
      // Prefer the first pending item
      const firstPending = queueItems.find((i) => i.status === 'pending_verification');
      setSelectedRecordId(firstPending ? firstPending.land_record_id : queueItems[0].land_record_id);
    }
  }, [queueItems, selectedRecordId]);

  const selectedRecord = queueItems.find((item) => item.land_record_id === selectedRecordId) || null;

  return (
    <div className="grid h-[calc(100vh-4rem)] grid-cols-1 md:grid-cols-12 overflow-hidden bg-slate-50">
      {/* Left Column: Land Queue List (4 cols on desktop) */}
      <div className="col-span-1 md:col-span-4 lg:col-span-4 h-full overflow-hidden">
        <LandQueueList
          items={queueItems}
          isLoading={isLoading}
          isError={isError}
          error={error}
          onRefresh={() => refetch()}
          selectedRecordId={selectedRecordId}
          onSelectRecord={(item: LandQueueItem) => setSelectedRecordId(item.land_record_id)}
        />
      </div>

      {/* Right Column: Selected Land Record Detail (8 cols on desktop) */}
      <div className="col-span-1 md:col-span-8 lg:col-span-8 h-full overflow-hidden">
        <LandDetailPanel selectedRecord={selectedRecord} />
      </div>
    </div>
  );
};
