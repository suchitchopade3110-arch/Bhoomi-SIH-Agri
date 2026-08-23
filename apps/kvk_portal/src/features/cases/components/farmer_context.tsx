import React from 'react';
import { FarmerContext as FarmerContextType } from '../types/case.types';
import { Badge } from '../../../components/ui/badge';
import { Sprout, MapPin } from 'lucide-react';

interface FarmerContextProps {
  context: FarmerContextType;
}

export const FarmerContext: React.FC<FarmerContextProps> = ({ context }) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#2E7D32]/10 text-[#2E7D32]">
            <Sprout className="h-4 w-4" />
          </div>
          <h3 className="text-sm font-bold text-slate-900">Farm Context</h3>
        </div>
        <Badge variant={context.land_status === 'verified' ? 'resolved' : 'review'}>
          {context.land_status === 'verified' ? 'Verified Land' : 'Pending Verification'}
        </Badge>
      </div>

      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="rounded-xl bg-slate-50 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Farmer Name</div>
          <div className="mt-1 font-bold text-slate-800">{context.farmer_name || 'Registered Farmer'}</div>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Crop & Variety</div>
          <div className="mt-1 font-bold text-slate-900">{context.crop}</div>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Growth Stage</div>
          <div className="mt-1 font-bold text-slate-800">{context.growth_stage}</div>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Location</div>
          <div className="mt-1 flex items-center gap-1 font-semibold text-slate-700">
            <MapPin className="h-3 w-3 text-slate-400 shrink-0" />
            <span className="truncate">{context.district || 'Erode, TN'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
