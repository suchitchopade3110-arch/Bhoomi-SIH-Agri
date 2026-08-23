import React from 'react';
import { Dialog } from '../../../components/ui/dialog';
import { Button } from '../../../components/ui/button';
import { authStore } from '../../../core/auth/auth_store';
import { ShieldCheck } from 'lucide-react';

interface ResolveCaseDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  isLoading: boolean;
  caseId: string;
  advisory: string;
}

export const ResolveCaseDialog: React.FC<ResolveCaseDialogProps> = ({
  isOpen,
  onClose,
  onConfirm,
  isLoading,
  caseId,
  advisory,
}) => {
  const agronomist = authStore.getCurrentAgronomist();

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title="Confirm Case Resolution"
      description="Your expert advisory and prescription will update the farmer's mobile companion."
    >
      <div className="space-y-4 pt-2">
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-slate-500">Case ID</span>
            <span className="font-mono font-bold text-slate-900">{caseId}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Signatory Agronomist</span>
            <span className="font-semibold text-slate-800">{agronomist.name}</span>
          </div>
          <div className="border-t border-slate-200/60 pt-2 mt-2">
            <span className="text-slate-500 block mb-1">Advisory Summary:</span>
            <p className="font-medium text-slate-800 italic">"{advisory.slice(0, 140)}..."</p>
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 p-3 text-xs text-emerald-800 border border-emerald-200">
          <ShieldCheck className="h-4 w-4 text-emerald-700 shrink-0" />
          <span>Authorized by <strong>{agronomist.kvkCenter}</strong></span>
        </div>

        <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
          <Button variant="ghost" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button variant="primary" onClick={onConfirm} isLoading={isLoading}>
            Confirm & Dispatch
          </Button>
        </div>
      </div>
    </Dialog>
  );
};
