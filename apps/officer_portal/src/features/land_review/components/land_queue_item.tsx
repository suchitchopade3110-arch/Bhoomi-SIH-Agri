import React from 'react';
import { LandQueueItem as LandQueueItemType } from '../types/land.types';
import { Badge } from '../../../components/ui/badge';
import { Calendar, SquareActivity } from 'lucide-react';

interface LandQueueItemProps {
  item: LandQueueItemType;
  isSelected: boolean;
  onSelect: (item: LandQueueItemType) => void;
}

export const LandQueueItem: React.FC<LandQueueItemProps> = ({
  item,
  isSelected,
  onSelect,
}) => {
  const isPending = item.status === 'pending_verification';

  return (
    <div
      onClick={() => onSelect(item)}
      className={`cursor-pointer rounded-xl border p-4 transition-all duration-150 ${
        isSelected
          ? 'border-[#2E7D32] bg-[#F1F8E9]/60 shadow-sm ring-1 ring-[#2E7D32]'
          : 'border-slate-200/80 bg-white hover:border-slate-300 hover:bg-slate-50/70'
      }`}
    >
      {/* Header: Survey No & Status Badge */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#2E7D32]/10 text-[#2E7D32] font-bold text-xs">
            SN
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400">Survey No.</span>
            <h4 className="text-sm font-extrabold text-slate-900 leading-tight">
              {item.farmer_stated.survey_no}
            </h4>
          </div>
        </div>
        <Badge variant={isPending ? 'pending' : 'verified'}>
          {isPending ? 'Pending Review' : 'Verified'}
        </Badge>
      </div>

      {/* Identifiers & Details */}
      <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
        <div className="flex items-center gap-1.5 text-slate-600">
          <SquareActivity className="h-3.5 w-3.5 text-slate-400" />
          <span>
            Area: <strong className="text-slate-800">{item.farmer_stated.area_acres} Acres</strong>
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-500 font-mono text-[11px]">
          <span className="text-slate-400">Farm:</span>
          <span>{item.farm_id}</span>
        </div>
      </div>

      {/* Footer: Submission Date & Land Record ID */}
      <div className="mt-3 flex items-center justify-between border-t border-slate-100 pt-2 text-[11px] text-slate-400">
        <div className="flex items-center gap-1">
          <Calendar className="h-3 w-3" />
          <span>{new Date(item.submitted_at).toLocaleDateString()}</span>
        </div>
        <span className="font-mono text-[10px] text-slate-400">
          ID: {item.land_record_id}
        </span>
      </div>
    </div>
  );
};
