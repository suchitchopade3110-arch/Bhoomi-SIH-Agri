import { officerApi } from '../../../api/officer_api';
import {
  LandQueueItem,
  LandQueueResponse,
  ReviewLandRequest,
  ReviewLandResponse,
} from '../types/land.types';

export const landReviewApi = {
  fetchQueue: (params?: { cursor?: string; limit?: number }): Promise<LandQueueResponse> => {
    return officerApi.getLandQueue(params);
  },

  fetchQueueItems: async (params?: { cursor?: string; limit?: number }): Promise<LandQueueItem[]> => {
    const res = await officerApi.getLandQueue(params);
    return res.items;
  },

  reviewLand: (
    landRecordId: string,
    payload: ReviewLandRequest
  ): Promise<ReviewLandResponse> => {
    return officerApi.reviewLand(landRecordId, payload);
  },
};
