import { useQuery } from '@tanstack/react-query';
import { landReviewApi } from '../api/land_review_api';
import { LandQueueItem, LandQueueResponse } from '../types/land.types';

export const LAND_QUEUE_QUERY_KEY = ['officer', 'land-queue'] as const;

export function useLandQueue(params?: { cursor?: string; limit?: number }) {
  return useQuery<LandQueueItem[], Error>({
    queryKey: [...LAND_QUEUE_QUERY_KEY, params?.cursor, params?.limit],
    queryFn: () => landReviewApi.fetchQueueItems(params),
    staleTime: 30000,
    refetchOnWindowFocus: true,
  });
}

export function usePaginatedLandQueue(params?: { cursor?: string; limit?: number }) {
  return useQuery<LandQueueResponse, Error>({
    queryKey: [...LAND_QUEUE_QUERY_KEY, 'paginated', params?.cursor, params?.limit],
    queryFn: () => landReviewApi.fetchQueue(params),
    staleTime: 30000,
    refetchOnWindowFocus: true,
  });
}
