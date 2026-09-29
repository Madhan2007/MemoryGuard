import { apiClient } from './client';
import { MemoryItem } from '../types';

export interface MemoriesListResponse {
  memories: MemoryItem[];
  total: number;
  project_memories_count: number;
  common_memories_count: number;
}

export interface MemoryQueryParams {
  deal_id?: string;
  scope?: string;
  decision?: string;
  rep_id?: string;
  query?: string;
}

export const memoriesApi = {
  list: (params: MemoryQueryParams = {}) => {
    const searchParams = new URLSearchParams();
    if (params.deal_id) searchParams.set('deal_id', params.deal_id);
    if (params.scope) searchParams.set('scope', params.scope);
    if (params.decision) searchParams.set('decision', params.decision);
    if (params.rep_id) searchParams.set('rep_id', params.rep_id);
    if (params.query) searchParams.set('query', params.query);

    const queryStr = searchParams.toString();
    return apiClient<MemoriesListResponse>(`/api/memories${queryStr ? `?${queryStr}` : ''}`);
  },
};
