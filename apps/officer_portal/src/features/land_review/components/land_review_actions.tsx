import React, { useState } from 'react';
import { Button } from '../../../components/ui/button';
import { Dialog } from '../../../components/ui/dialog';
import { LandQueueItem } from '../types/land.types';
import { useReviewLand } from '../hooks/use_review_land';
import { authStore } from '../../../core/auth/auth_store';
import { CheckCircle2, XCircle, ShieldCheck } from 'lucide-react';

interface LandReviewActionsProps {
  record: LandQueueItem;
  onSuccess?: () => void;
}

export const LandReviewActions: React.FC<LandReviewActionsProps> = ({ record, onSuccess }) => {
  const [isApproveOpen, setIsApproveOpen] = useState(false);
  const [isRejectOpen, setIsRejectOpen] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const reviewMutation = useReviewLand();
  const officer = authStore.getCurrentOfficer();

  const handleApprove = () => {
    reviewMutation.mutate(
      {
        landRecordId: record.land_record_id,
        decision: 'verified',
        boundaryGeojson: record.boundary_geojson,
      },
      {
        onSuccess: () => {
          setIsApproveOpen(false);
          if (onSuccess) onSuccess();
        },
      }
    );
  };

  const handleReject = () => {
    if (!rejectReason.trim()) return;
    reviewMutation.mutate(
      {
        landRecordId: record.land_record_id,
        decision: 'rejected',
        reason: rejectReason.trim(),
        boundaryGeojson: record.boundary_geojson,
      },
      {
        onSuccess: () => {
          setIsRejectOpen(false);
          setRejectReason('');
          if (onSuccess) onSuccess();
        },
      }
    );
  };

  return (
    <div className="flex items-center gap-3">
      {/* Reject Button */}
      <Button
        variant="outline"
        size="md"
        onClick={() => setIsRejectOpen(true)}
        className="border-red-300 text-red-700 hover:bg-red-50 hover:text-red-800 gap-1.5"
      >
        <XCircle className="h-4 w-4" />
        <span>Reject</span>
      </Button>

      {/* Approve Button */}
      <Button
        variant="primary"
        size="lg"
        onClick={() => setIsApproveOpen(true)}
        className="gap-2 shadow-md hover:shadow-lg"
      >
        <CheckCircle2 className="h-5 w-5" />
        <span>Approve Land</span>
      </Button>

      {/* Approve Modal */}
      <Dialog
        isOpen={isApproveOpen}
        onClose={() => setIsApproveOpen(false)}
        title="Approve Land Parcel"
        description="Official verification will sign and confirm this parcel in government records."
      >
        <div className="space-y-4 pt-2">
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-500">Survey No.</span>
              <span className="font-bold text-slate-900">{record.farmer_stated.survey_no}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Self-Reported Area</span>
              <span className="font-semibold text-slate-800">{record.farmer_stated.area_acres} Acres</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Farm ID</span>
              <span className="font-mono text-slate-800">{record.farm_id}</span>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded-xl bg-emerald-50 p-3 text-xs text-emerald-800 border border-emerald-200">
            <ShieldCheck className="h-4 w-4 text-emerald-700 shrink-0" />
            <span>Verifier: <strong>{officer.verifierTag}</strong></span>
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
            <Button variant="ghost" onClick={() => setIsApproveOpen(false)}>Cancel</Button>
            <Button
              variant="primary"
              onClick={handleApprove}
              isLoading={reviewMutation.isPending}
            >
              Confirm & Verify
            </Button>
          </div>
        </div>
      </Dialog>

      {/* Reject Modal */}
      <Dialog
        isOpen={isRejectOpen}
        onClose={() => setIsRejectOpen(false)}
        title="Reject Land Parcel"
        description="Specify the official discrepancy reason for rejection."
      >
        <div className="space-y-4 pt-2">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-700">Rejection Reason</label>
            <textarea
              rows={3}
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              placeholder="e.g. Survey number mismatch with revenue records or boundary overlap."
              className="w-full rounded-lg border border-slate-200 p-3 text-xs focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
            <Button variant="ghost" onClick={() => setIsRejectOpen(false)}>Cancel</Button>
            <Button
              variant="danger"
              onClick={handleReject}
              disabled={!rejectReason.trim()}
              isLoading={reviewMutation.isPending}
            >
              Confirm Rejection
            </Button>
          </div>
        </div>
      </Dialog>
    </div>
  );
};
