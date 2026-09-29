import { apiClient } from './client';
import { Deal, ConversationMessage } from '../types';

export interface DealsListResponse {
  deals: Deal[];
  total: number;
  total_pipeline_value: number;
  active_deals_count: number;
  verified_memories_count: number;
  pending_reviews_count: number;
  recent_outcomes_count: number;
}

export interface DealDetailResponse {
  deal: Deal;
  conversation: ConversationMessage[];
  conversation_id: string;
  turn_count: number;
}

export const dealsApi = {
  list: () => apiClient<DealsListResponse>('/api/deals'),
  get: (dealId: string) => apiClient<DealDetailResponse>(`/api/deals/${dealId}`),
  resetConversation: (dealId: string) => 
    apiClient<{ success: boolean; deal_id: string; message: string }>(`/api/deals/${dealId}/reset`, {
      method: 'POST',
    }),
};
