import { useMutation, useQueryClient } from '@tanstack/react-query';
import { landReviewApi } from '../api/land_review_api';
import { ReviewLandRequest, ReviewLandResponse } from '../types/land.types';
import { LAND_QUEUE_QUERY_KEY } from './use_land_queue';

interface ReviewLandParams {
  landRecordId: string;
  decision: 'verified' | 'rejected';
  reason?: string;
  boundaryGeojson?: ReviewLandRequest['boundary_geojson'];
}

export function useReviewLand() {
  const queryClient = useQueryClient();

  return useMutation<ReviewLandResponse, Error, ReviewLandParams>({
    mutationFn: ({ landRecordId, decision, reason, boundaryGeojson }) =>
      landReviewApi.reviewLand(landRecordId, {
        decision,
        reason,
        boundary_geojson: boundaryGeojson,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: LAND_QUEUE_QUERY_KEY });
    },
  });
}
