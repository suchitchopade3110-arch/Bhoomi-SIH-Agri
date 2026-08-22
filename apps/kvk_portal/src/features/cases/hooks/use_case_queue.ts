import { useQuery } from '@tanstack/react-query';
import { caseApi } from '../api/case_api';
import { KvkCaseQueueResponse } from '../types/case.types';

export const CASE_QUEUE_QUERY_KEY = ['kvk', 'case_queue'];

export function useCaseQueue(params?: { cursor?: string; limit?: number }) {
  return useQuery<KvkCaseQueueResponse, Error>({
    queryKey: [...CASE_QUEUE_QUERY_KEY, params?.cursor, params?.limit],
    queryFn: () => caseApi.fetchQueue(params),
    refetchInterval: 30000,
  });
}
