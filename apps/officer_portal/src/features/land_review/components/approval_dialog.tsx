import React from 'react';
import { Dialog } from '../../../components/ui/dialog';
import { Button } from '../../../components/ui/button';
import { LandQueueItem } from '../types/land.types';
import { authStore } from '../../../core/auth/auth_store';
import { CheckCircle2, ShieldCheck } from 'lucide-react';

interface ApprovalDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isLoading: boolean;
  record: LandQueueItem | null;
}

export const ApprovalDialog: React.FC<ApprovalDialogProps> = ({
  isOpen,
  onClose,
  onConfirm,
  isLoading,
  record,
}) => {
  if (!record) return null;

  const officer = authStore.getCurrentOfficer();
  const pointCount = record.boundary_geojson?.coordinates?.[0]?.length || 0;

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title="Confirm Land Verification"
      description="You are about to issue official government verification for this agricultural land parcel."
    >
      <div className="space-y-4 pt-2">
        {/* Verification Summary Card */}
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-2 text-xs">
          <div className="flex justify-between items-center pb-2 border-b border-slate-200">
            <span className="text-slate-500 font-medium">Survey Number</span>
            <span className="text-slate-900 font-bold text-sm">{record.farmer_stated.survey_no}</span>
          </div>
          <div className="flex justify-between items-center py-1">
            <span className="text-slate-500 font-medium">Self-Reported Area</span>
            <span className="text-slate-800 font-semibold">{record.farmer_stated.area_acres} Acres</span>
          </div>
          <div className="flex justify-between items-center py-1">
            <span className="text-slate-500 font-medium">Farm Identifier</span>
            <span className="text-slate-800 font-mono">{record.farm_id}</span>
          </div>
          <div className="flex justify-between items-center py-1">
            <span className="text-slate-500 font-medium">Land Record ID</span>
            <span className="text-slate-800 font-mono">{record.land_record_id}</span>
          </div>
          {pointCount > 0 && (
            <div className="flex justify-between items-center py-1">
              <span className="text-slate-500 font-medium">Preserved Boundary</span>
              <span className="text-emerald-700 font-semibold">{pointCount} polygon vertices</span>
            </div>
          )}
        </div>

        {/* Verifier Signature Notice */}
        <div className="flex items-start gap-3 rounded-xl border border-emerald-200 bg-emerald-50/60 p-3.5 text-xs text-emerald-900">
          <ShieldCheck className="h-5 w-5 text-emerald-700 shrink-0 mt-0.5" />
          <div>
            <div className="font-bold">Official Verification Stamp</div>
            <p className="mt-0.5 text-[11px] text-emerald-800">
              This record will be signed with verifier tag: <strong className="font-mono">{officer.verifierTag}</strong>.
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={onConfirm}
            isLoading={isLoading}
            className="px-6"
          >
            <CheckCircle2 className="h-4 w-4 mr-2" />
            Confirm & Verify Land
          </Button>
        </div>
      </div>
    </Dialog>
  );
};
