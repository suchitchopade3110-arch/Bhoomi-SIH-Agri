import { kvkApi } from '../../../api/kvk_api';
import {
  KvkCase,
  KvkCaseQueueResponse,
  ResolveCaseRequest,
  ResolveCaseResponse,
} from '../types/case.types';

export const caseApi = {
  fetchQueue: (params?: { cursor?: string; limit?: number }): Promise<KvkCaseQueueResponse> => {
    return kvkApi.getCaseQueue(params);
  },

  fetchQueueItems: async (params?: { cursor?: string; limit?: number }): Promise<KvkCase[]> => {
    const res = await kvkApi.getCaseQueue(params);
    return res.cases;
  },

  fetchDetail: (caseId: string): Promise<KvkCase> => {
    return kvkApi.getCaseDetail(caseId);
  },

  resolveCase: (caseId: string, payload: ResolveCaseRequest): Promise<ResolveCaseResponse> => {
    return kvkApi.resolveCase(caseId, payload);
  },
};
