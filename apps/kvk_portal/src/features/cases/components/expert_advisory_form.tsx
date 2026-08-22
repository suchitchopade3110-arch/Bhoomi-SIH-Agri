import React, { useState } from 'react';
import { Button } from '../../../components/ui/button';
import { ResolveCaseDialog } from './resolve_case_dialog';
import { useResolveCase } from '../hooks/use_resolve_case';
import { KvkCase } from '../types/case.types';
import { CheckCircle2, ShieldCheck, Plus, Trash2 } from 'lucide-react';

interface ExpertAdvisoryFormProps {
  kvkCase: KvkCase;
}

export const ExpertAdvisoryForm: React.FC<ExpertAdvisoryFormProps> = ({ kvkCase }) => {
  const [advisory, setAdvisory] = useState('');
  const [severity, setSeverity] = useState<'low' | 'moderate' | 'high' | 'critical'>('moderate');
  const [actions, setActions] = useState<string[]>([
    'Apply recommended certified formulation strictly during morning spray window.',
  ]);
  const [newAction, setNewAction] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const resolveMutation = useResolveCase();

  const handleAddAction = () => {
    if (!newAction.trim()) return;
    setActions([...actions, newAction.trim()]);
    setNewAction('');
  };

  const handleRemoveAction = (index: number) => {
    setActions(actions.filter((_, i) => i !== index));
  };

  const handleConfirmResolve = () => {
    resolveMutation.mutate(
      {
        caseId: kvkCase.case_id,
        payload: {
          agronomist_advisory: advisory.trim(),
          prescribed_actions: actions,
          severity,
          status: 'resolved',
        },
      },
      {
        onSuccess: () => {
          setIsDialogOpen(false);
        },
      }
    );
  };

  if (kvkCase.status === 'resolved') {
    return (
      <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5">
        <div className="flex items-center gap-2 text-emerald-900 font-extrabold text-sm">
          <CheckCircle2 className="h-5 w-5 text-emerald-600" />
          <span>Case Resolved by Agronomist</span>
        </div>
        <p className="mt-2 text-xs font-semibold text-emerald-800">
          "{kvkCase.agronomist_advisory}"
        </p>
        {kvkCase.prescribed_actions && kvkCase.prescribed_actions.length > 0 && (
          <div className="mt-3">
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700">Prescribed Actions:</span>
            <ul className="mt-1 space-y-1 text-xs text-emerald-900">
              {kvkCase.prescribed_actions.map((act, i) => (
                <li key={i}>&bull; {act}</li>
              ))}
            </ul>
          </div>
        )}
        <div className="mt-4 flex items-center justify-between text-[11px] text-emerald-700 border-t border-emerald-200/60 pt-3">
          <span>Agronomist: <strong>{kvkCase.agronomist || 'Dr. S. Sundaram'}</strong></span>
          <span>Resolved: {new Date(kvkCase.resolved_at || Date.now()).toLocaleDateString()}</span>
        </div>
      </div>
    );
  }

  const isValid = advisory.trim().length > 10 && actions.length > 0;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
      <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#2E7D32]/10 text-[#2E7D32]">
          <ShieldCheck className="h-4 w-4" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-slate-900">Official KVK Expert Advisory</h3>
          <p className="text-[11px] text-slate-500">
            Prescribe verified remedial diagnosis and dosage instructions
          </p>
        </div>
      </div>

      <div className="mt-4 space-y-4 text-xs">
        {/* Severity Selection */}
        <div>
          <label className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
            Field Discrepancy Severity
          </label>
          <div className="mt-1.5 flex gap-2">
            {(['low', 'moderate', 'high', 'critical'] as const).map((sev) => (
              <button
                key={sev}
                type="button"
                onClick={() => setSeverity(sev)}
                className={`rounded-lg px-3 py-1.5 font-bold uppercase text-[10px] transition-all ${
                  severity === sev
                    ? 'bg-[#2E7D32] text-white shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>

        {/* Advisory Textarea */}
        <div>
          <label className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
            Agronomist Clinical Findings & Advisory
          </label>
          <textarea
            rows={3}
            value={advisory}
            onChange={(e) => setAdvisory(e.target.value)}
            placeholder="e.g. Confirmed Bacterial Leaf Blight stage 2. Bacterial ooze beads verified on upper leaf margins. Discontinue urea and spray fresh cow dung slurry or copper formulation..."
            className="mt-1.5 w-full rounded-xl border border-slate-200 p-3 text-xs focus:border-[#2E7D32] focus:ring-1 focus:ring-[#2E7D32] focus:outline-none"
          />
        </div>

        {/* Action Items List */}
        <div>
          <label className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
            Prescribed Action Directives
          </label>
          <div className="mt-1.5 space-y-2">
            {actions.map((act, i) => (
              <div key={i} className="flex items-center justify-between rounded-lg bg-slate-50 p-2.5 border border-slate-100">
                <span className="text-slate-800 font-medium">{act}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveAction(i)}
                  className="text-slate-400 hover:text-red-600 p-1"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            ))}

            <div className="flex gap-2 mt-2">
              <input
                type="text"
                value={newAction}
                onChange={(e) => setNewAction(e.target.value)}
                placeholder="Add another directive..."
                className="flex-1 rounded-lg border border-slate-200 px-3 py-1.5 text-xs focus:border-[#2E7D32] focus:outline-none"
              />
              <Button size="sm" variant="outline" onClick={handleAddAction} className="gap-1">
                <Plus className="h-3.5 w-3.5" />
                <span>Add</span>
              </Button>
            </div>
          </div>
        </div>

        {/* Submit Resolve CTA */}
        <div className="pt-3 border-t border-slate-100 flex justify-end">
          <Button
            variant="primary"
            size="md"
            disabled={!isValid}
            onClick={() => setIsDialogOpen(true)}
            className="gap-2 shadow-md hover:shadow-lg"
          >
            <CheckCircle2 className="h-4 w-4" />
            <span>Resolve & Dispatch Advisory</span>
          </Button>
        </div>
      </div>

      <ResolveCaseDialog
        isOpen={isDialogOpen}
        onClose={() => setIsDialogOpen(false)}
        onConfirm={handleConfirmResolve}
        isLoading={resolveMutation.isPending}
        caseId={kvkCase.case_id}
        advisory={advisory}
      />
    </div>
  );
};
