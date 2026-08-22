import React, { useState, useEffect } from 'react';
import { useCaseQueue } from '../hooks/use_case_queue';
import { CaseQueue } from '../components/case_queue';
import { CaseDetail } from '../components/case_detail';
import { CaseStatus } from '../types/case.types';

interface CaseQueuePageProps {
  statusFilter?: CaseStatus;
}

export const CaseQueuePage: React.FC<CaseQueuePageProps> = ({ statusFilter }) => {
  const { data: queueResponse, isLoading, isError, refetch } = useCaseQueue();
  const cases = queueResponse?.cases || [];
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);

  const filteredCases = statusFilter
    ? cases.filter((c) => c.status === statusFilter)
    : cases;

  // Default select first case on load or filter change
  useEffect(() => {
    if (filteredCases && filteredCases.length > 0) {
      if (!selectedCaseId || !filteredCases.some((c) => c.case_id === selectedCaseId)) {
        setSelectedCaseId(filteredCases[0].case_id);
      }
    } else {
      setSelectedCaseId(null);
    }
  }, [filteredCases, selectedCaseId]);

  const selectedCase = cases?.find((c) => c.case_id === selectedCaseId) || null;

  return (
    <div className="flex h-[calc(100vh-4rem)] w-full overflow-hidden">
      <CaseQueue
        cases={filteredCases}
        isLoading={isLoading}
        isError={isError}
        selectedCaseId={selectedCaseId}
        onSelectCase={setSelectedCaseId}
        onRetry={refetch}
      />
      <CaseDetail selectedCase={selectedCase} />
    </div>
  );
};
