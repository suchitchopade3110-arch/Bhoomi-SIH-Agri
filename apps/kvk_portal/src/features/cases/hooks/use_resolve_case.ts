import { useMutation, useQueryClient } from '@tanstack/react-query';
import { caseApi } from '../api/case_api';
import { ResolveCaseRequest, ResolveCaseResponse } from '../types/case.types';
import { CASE_QUEUE_QUERY_KEY } from './use_case_queue';

interface ResolveCaseParams {
  caseId: string;
  payload: ResolveCaseRequest;
}

export function useResolveCase() {
  const queryClient = useQueryClient();

  return useMutation<ResolveCaseResponse, Error, ResolveCaseParams>({
    mutationFn: ({ caseId, payload }) => caseApi.resolveCase(caseId, payload),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: CASE_QUEUE_QUERY_KEY });
      queryClient.invalidateQueries({ queryKey: ['kvk', 'case_detail', variables.caseId] });
    },
  });
}
