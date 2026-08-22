import React from 'react';
import { Image as ImageIcon, AlertCircle } from 'lucide-react';

interface ProblemMediaProps {
  description: string;
  imageUrl?: string;
  followupNotes?: string;
  escalationReason?: string;
}

export const ProblemMedia: React.FC<ProblemMediaProps> = ({
  description,
  imageUrl,
  followupNotes,
  escalationReason,
}) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-4">
      {/* Problem Description */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400">
          <AlertCircle className="h-4 w-4 text-amber-500" />
          <span>Farmer Stated Problem</span>
        </div>
        <p className="mt-2 text-sm leading-relaxed font-semibold text-slate-800 bg-amber-50/50 rounded-xl p-3.5 border border-amber-200/60">
          "{description}"
        </p>
      </div>

      {/* Follow-up Notes & Escalation Reason */}
      {(followupNotes || escalationReason) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          {followupNotes && (
            <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
              <span className="font-bold text-slate-500 uppercase tracking-wider text-[10px]">
                Follow-up Tracking
              </span>
              <p className="mt-1 font-medium text-slate-700">{followupNotes}</p>
            </div>
          )}
          {escalationReason && (
            <div className="rounded-xl border border-purple-100 bg-purple-50/50 p-3">
              <span className="font-bold text-purple-600 uppercase tracking-wider text-[10px]">
                Escalation Trigger
              </span>
              <p className="mt-1 font-medium text-purple-900">{escalationReason}</p>
            </div>
          )}
        </div>
      )}

      {/* Uploaded Crop Photograph */}
      {imageUrl && (
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            <ImageIcon className="h-4 w-4 text-[#2E7D32]" />
            <span>Uploaded Field Media</span>
          </div>
          <div className="overflow-hidden rounded-xl border border-slate-200 shadow-xs max-h-72">
            <img
              src={imageUrl}
              alt="Farmer uploaded crop problem"
              className="h-full w-full object-cover"
            />
          </div>
        </div>
      )}
    </div>
  );
};
