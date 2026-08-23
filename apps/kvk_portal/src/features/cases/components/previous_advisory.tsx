import React from 'react';
import { PreviousAiAdvisory as PreviousAiAdvisoryType } from '../types/case.types';
import { Bot, CheckCircle, AlertTriangle } from 'lucide-react';
import { Badge } from '../../../components/ui/badge';

interface PreviousAdvisoryProps {
  advisory?: PreviousAiAdvisoryType;
}

export const PreviousAdvisory: React.FC<PreviousAdvisoryProps> = ({ advisory }) => {
  if (!advisory) return null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
            <Bot className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Initial AI Advisory Snapshot</h3>
            <p className="text-[11px] text-slate-500">Automated diagnosis generated for farmer</p>
          </div>
        </div>
        <Badge variant={advisory.confidence_level === 'high' ? 'resolved' : 'review'}>
          {advisory.confidence_level} Confidence
        </Badge>
      </div>

      <div className="mt-4 space-y-3 text-xs">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Identified Anomaly
          </span>
          <div className="mt-0.5 text-sm font-extrabold text-slate-900">
            {advisory.possible_issue}
          </div>
        </div>

        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Initial Action Recommendations
          </span>
          <ul className="mt-1.5 space-y-1.5">
            {advisory.actions.map((act, i) => (
              <li key={i} className="flex items-start gap-2 text-slate-700">
                <CheckCircle className="h-3.5 w-3.5 text-[#2E7D32] shrink-0 mt-0.5" />
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>

        {advisory.caution && (
          <div className="flex items-start gap-2 rounded-xl bg-amber-50 p-2.5 text-amber-900 border border-amber-200/60">
            <AlertTriangle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
            <span className="text-[11px]">{advisory.caution}</span>
          </div>
        )}
      </div>
    </div>
  );
};
