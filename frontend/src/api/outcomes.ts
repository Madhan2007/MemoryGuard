import { apiClient } from './client';
import { DealOutcome } from '../types';

export interface OutcomesListResponse {
  outcomes: DealOutcome[];
  total: number;
  learning_impact: {
    memories_recalled_total: number;
    relevant_memories_used: number;
    personalized_recommendations: number;
    win_rate_delta: string;
    avg_cycle_reduction_days: number;
  };
  learning_timeline: Array<{
    step: number;
    label: string;
    icon: string;
    desc: string;
  }>;
}

export interface OutcomeRecordPayload {
  deal_id: string;
  customer_name: string;
  objection: string;
  strategy: string;
  outcome?: string;
  confidence?: number;
  recommendation: string;
}

export const outcomesApi = {
  list: (dealId?: string) => {
    const query = dealId ? `?deal_id=${encodeURIComponent(dealId)}` : '';
    return apiClient<OutcomesListResponse>(`/api/outcomes${query}`);
  },
  record: (payload: OutcomeRecordPayload) =>
    apiClient<{ success: boolean; outcome: DealOutcome }>('/api/outcomes', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
