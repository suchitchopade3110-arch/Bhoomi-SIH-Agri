import { useQuery } from '@tanstack/react-query';
import { caseApi } from '../api/case_api';
import { KvkCase } from '../types/case.types';

export function useCaseDetail(caseId?: string) {
  return useQuery<KvkCase, Error>({
    queryKey: ['kvk', 'case_detail', caseId],
    queryFn: () => caseApi.fetchDetail(caseId!),
    enabled: !!caseId,
  });
}
