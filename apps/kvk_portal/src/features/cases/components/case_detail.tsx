import React from 'react';
import { KvkCase } from '../types/case.types';
import { FarmerContext } from './farmer_context';
import { ProblemMedia } from './problem_media';
import { PreviousAdvisory } from './previous_advisory';
import { ExpertAdvisoryForm } from './expert_advisory_form';
import { FileQuestion } from 'lucide-react';

interface CaseDetailProps {
  selectedCase: KvkCase | null;
}

export const CaseDetail: React.FC<CaseDetailProps> = ({ selectedCase }) => {
  if (!selectedCase) {
    return (
      <div className="flex h-full flex-1 flex-col items-center justify-center bg-slate-50/50 p-8 text-center">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-xs max-w-sm">
          <FileQuestion className="mx-auto h-12 w-12 text-[#2E7D32]/40" />
          <h3 className="mt-4 text-base font-bold text-slate-800">
            No Escalated Case Selected
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            Select an escalated case from the left queue to review crop photographs, automated AI diagnostics, and prescribe official clinical guidance.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-slate-50/30 p-6 lg:p-8 space-y-6">
      {/* 1. Farmer Context Card */}
      <FarmerContext context={selectedCase.farmer_context} />

      {/* 2. Problem Description & Media */}
      <ProblemMedia
        description={selectedCase.problem_description}
        imageUrl={selectedCase.image_url}
        followupNotes={selectedCase.followup_notes}
        escalationReason={selectedCase.escalation_reason}
      />

      {/* 3. Previous AI Advisory */}
      <PreviousAdvisory advisory={selectedCase.previous_ai_advisory} />

      {/* 4. Agronomist Advisory & Resolution Form */}
      <ExpertAdvisoryForm kvkCase={selectedCase} />
    </div>
  );
};
