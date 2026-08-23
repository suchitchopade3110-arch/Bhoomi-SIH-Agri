import React from 'react';
import { KvkCase } from '../types/case.types';
import { CaseListItem } from './case_list_item';
import { Spinner } from '../../../components/ui/spinner';
import { Inbox, AlertCircle } from 'lucide-react';

interface CaseQueueProps {
  cases: KvkCase[] | undefined;
  isLoading: boolean;
  isError: boolean;
  selectedCaseId: string | null;
  onSelectCase: (caseId: string) => void;
  onRetry: () => void;
  hasMore?: boolean;
  onLoadMore?: () => void;
  isLoadingMore?: boolean;
}

export const CaseQueue: React.FC<CaseQueueProps> = ({
  cases,
  isLoading,
  isError,
  selectedCaseId,
  onSelectCase,
  onRetry,
  hasMore = false,
  onLoadMore,
  isLoadingMore = false,
}) => {
  return (
    <div className="flex h-full w-full max-w-sm flex-col border-r border-slate-200 bg-slate-50/50">
      {/* Header */}
      <div className="border-b border-slate-200 bg-white p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-black tracking-tight text-slate-900">
            Escalated Case Queue
          </h2>
          <span className="rounded-full bg-[#2E7D32]/10 px-2.5 py-0.5 text-xs font-black text-[#2E7D32]">
            {cases?.length || 0}
          </span>
        </div>
        <p className="mt-1 text-[11px] text-slate-500">
          Cases requiring KVK agronomist review
        </p>
      </div>

      {/* Queue Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isLoading && (
          <div className="flex h-64 flex-col items-center justify-center gap-2">
            <Spinner size="md" />
            <span className="text-xs font-semibold text-slate-500">Loading cases...</span>
          </div>
        )}

        {isError && (
          <div className="rounded-2xl border border-red-200 bg-red-50/60 p-4 text-center">
            <AlertCircle className="mx-auto h-6 w-6 text-red-500" />
            <h4 className="mt-2 text-xs font-bold text-red-900">Failed to load queue</h4>
            <button
              onClick={onRetry}
              className="mt-3 rounded-lg bg-red-600 px-3 py-1 text-[11px] font-bold text-white shadow-xs hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        )}

        {!isLoading && !isError && cases?.length === 0 && (
          <div className="flex h-64 flex-col items-center justify-center p-6 text-center text-slate-400">
            <Inbox className="h-10 w-10 text-slate-300 stroke-1" />
            <span className="mt-2 text-xs font-semibold">No pending escalated cases</span>
          </div>
        )}

        {cases?.map((c) => (
          <CaseListItem
            key={c.case_id}
            kvkCase={c}
            isSelected={selectedCaseId === c.case_id}
            onSelect={() => onSelectCase(c.case_id)}
          />
        ))}

        {hasMore && onLoadMore && (
          <div className="pt-2 text-center">
            <button
              disabled={isLoadingMore}
              onClick={onLoadMore}
              className="w-full rounded-lg border border-slate-200 bg-white py-2 text-xs font-bold text-slate-700 shadow-xs hover:bg-slate-50 disabled:opacity-50"
            >
              {isLoadingMore ? 'Loading more...' : 'Load More Cases'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
