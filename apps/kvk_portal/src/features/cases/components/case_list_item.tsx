import React from 'react';
import { KvkCase } from '../types/case.types';
import { Badge } from '../../../components/ui/badge';
import { Sprout, ChevronRight } from 'lucide-react';

interface CaseListItemProps {
  kvkCase: KvkCase;
  isSelected: boolean;
  onSelect: () => void;
}

export const CaseListItem: React.FC<CaseListItemProps> = ({
  kvkCase,
  isSelected,
  onSelect,
}) => {
  const isResolved = kvkCase.status === 'resolved';
  const isUnderReview = kvkCase.status === 'under_review';

  return (
    <div
      onClick={onSelect}
      className={`group relative cursor-pointer rounded-2xl border p-4 transition-all ${
        isSelected
          ? 'border-[#2E7D32] bg-[#2E7D32]/5 shadow-sm'
          : 'border-slate-200/80 bg-white hover:border-slate-300 hover:shadow-xs'
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="font-mono text-[11px] font-extrabold text-slate-500">
            {kvkCase.case_id}
          </span>
          <Badge
            variant={
              isResolved
                ? 'resolved'
                : isUnderReview
                ? 'review'
                : 'escalated'
            }
          >
            {isResolved ? 'Resolved' : isUnderReview ? 'Under Review' : 'Escalated'}
          </Badge>
        </div>
        <ChevronRight
          className={`h-4 w-4 transition-transform ${
            isSelected ? 'text-[#2E7D32] translate-x-0.5' : 'text-slate-300 group-hover:text-slate-500'
          }`}
        />
      </div>

      <div className="mt-2.5">
        <div className="flex items-center gap-1.5 text-xs font-bold text-slate-900">
          <Sprout className="h-3.5 w-3.5 text-[#2E7D32]" />
          <span>{kvkCase.farmer_context.crop}</span>
        </div>
        <p className="mt-1 line-clamp-2 text-xs text-slate-600 font-medium">
          {kvkCase.problem_description}
        </p>
      </div>

      <div className="mt-3 flex items-center justify-between border-t border-slate-100/80 pt-2.5 text-[11px] text-slate-400">
        <span className="truncate max-w-[130px] font-semibold text-slate-600">
          {kvkCase.farmer_context.farmer_name || kvkCase.farm_id}
        </span>
        <span>
          {new Date(kvkCase.submission_timestamp).toLocaleDateString(undefined, {
            month: 'short',
            day: 'numeric',
          })}
        </span>
      </div>
    </div>
  );
};
