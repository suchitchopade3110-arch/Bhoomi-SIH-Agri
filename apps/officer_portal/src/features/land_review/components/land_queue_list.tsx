import React, { useState, useMemo } from 'react';
import { LandQueueItem as LandQueueItemType } from '../types/land.types';
import { LandQueueItem } from './land_queue_item';
import { Skeleton } from '../../../components/ui/skeleton';
import { Button } from '../../../components/ui/button';
import { Search, RefreshCw, Inbox } from 'lucide-react';

interface LandQueueListProps {
  items?: LandQueueItemType[];
  isLoading: boolean;
  isError: boolean;
  error?: Error | null;
  onRefresh: () => void;
  selectedRecordId: string | null;
  onSelectRecord: (item: LandQueueItemType) => void;
  hasMore?: boolean;
  onLoadMore?: () => void;
  isLoadingMore?: boolean;
}

export const LandQueueList: React.FC<LandQueueListProps> = ({
  items = [],
  isLoading,
  isError,
  error,
  onRefresh,
  selectedRecordId,
  onSelectRecord,
  hasMore = false,
  onLoadMore,
  isLoadingMore = false,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'verified'>('all');

  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      const matchesSearch =
        item.farmer_stated.survey_no.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.farm_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.land_record_id.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesStatus =
        statusFilter === 'all'
          ? true
          : statusFilter === 'pending'
          ? item.status === 'pending_verification'
          : item.status === 'verified';

      return matchesSearch && matchesStatus;
    });
  }, [items, searchQuery, statusFilter]);

  const pendingCount = items.filter((i) => i.status === 'pending_verification').length;
  const verifiedCount = items.filter((i) => i.status === 'verified').length;

  return (
    <div className="flex h-full flex-col border-r border-slate-200/80 bg-white">
      {/* Search and Header Section */}
      <div className="border-b border-slate-200/80 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h2 className="text-base font-bold text-slate-900">Land Queue</h2>
            <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-600">
              {items.length}
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onRefresh}
            title="Refresh Queue"
            className="h-8 w-8 p-0"
          >
            <RefreshCw className={`h-4 w-4 text-slate-600 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </div>

        {/* Search Bar */}
        <div className="relative mt-3">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by survey no, farm, or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-9 w-full rounded-lg border border-slate-200 bg-slate-50/70 pl-9 pr-3 text-xs text-slate-800 placeholder-slate-400 transition-colors focus:border-[#2E7D32] focus:bg-white focus:outline-none focus:ring-1 focus:ring-[#2E7D32]"
          />
        </div>

        {/* Status Filter Tabs */}
        <div className="mt-3 flex gap-1.5 rounded-lg bg-slate-100/80 p-1 text-xs">
          <button
            onClick={() => setStatusFilter('all')}
            className={`flex-1 rounded-md py-1 font-semibold transition-all ${
              statusFilter === 'all'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            All ({items.length})
          </button>
          <button
            onClick={() => setStatusFilter('pending')}
            className={`flex-1 rounded-md py-1 font-semibold transition-all ${
              statusFilter === 'pending'
                ? 'bg-white text-amber-800 shadow-xs'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            Pending ({pendingCount})
          </button>
          <button
            onClick={() => setStatusFilter('verified')}
            className={`flex-1 rounded-md py-1 font-semibold transition-all ${
              statusFilter === 'verified'
                ? 'bg-white text-emerald-800 shadow-xs'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            Verified ({verifiedCount})
          </button>
        </div>
      </div>

      {/* Queue Items List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="rounded-xl border border-slate-100 p-4 space-y-2">
                <div className="flex justify-between">
                  <Skeleton className="h-4 w-28" />
                  <Skeleton className="h-4 w-20" />
                </div>
                <Skeleton className="h-3 w-36" />
                <Skeleton className="h-3 w-48" />
              </div>
            ))}
          </div>
        ) : isError ? (
          <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
            <p className="text-xs font-semibold text-red-800">
              Failed to load queue
            </p>
            <p className="mt-1 text-[11px] text-red-600">{error?.message || 'Error occurred'}</p>
            <Button
              variant="outline"
              size="sm"
              onClick={onRefresh}
              className="mt-3 bg-white"
            >
              Retry
            </Button>
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center text-slate-400">
            <div className="rounded-full bg-slate-100 p-4">
              <Inbox className="h-8 w-8 text-slate-400" />
            </div>
            <p className="mt-3 text-xs font-semibold text-slate-700">No records found</p>
            <p className="mt-1 text-[11px] text-slate-400">
              {searchQuery ? 'Try adjusting your search query' : 'No records match this filter'}
            </p>
          </div>
        ) : (
          <>
            {filteredItems.map((item) => (
              <LandQueueItem
                key={item.land_record_id}
                item={item}
                isSelected={item.land_record_id === selectedRecordId}
                onSelect={onSelectRecord}
              />
            ))}
            {hasMore && onLoadMore && (
              <div className="pt-2 text-center">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={isLoadingMore}
                  onClick={onLoadMore}
                  className="w-full bg-white text-xs"
                >
                  {isLoadingMore ? 'Loading more records...' : 'Load More Records'}
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
