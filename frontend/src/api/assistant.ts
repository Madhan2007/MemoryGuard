import { apiClient } from './client';
import { TurnResult } from '../types';

export interface TurnPayload {
  user_input: string;
  rep_id?: string;
  conversation_id?: string;
  turn_id?: number;
  customer_name?: string;
  deal_stage?: string;
}

export interface ScenarioRunResult {
  scenario_id: string;
  customer: string;
  deal_id: string;
  turns_executed: number;
  results: Array<{
    turn_id: number;
    speaker: string;
    input: string;
    answer: string;
    memory_decisions: any[];
    recalled_memories: any[];
    latency_ms: number;
  }>;
  ground_truth: any;
}

export const assistantApi = {
  processTurn: (dealId: string, payload: TurnPayload) =>
    apiClient<TurnResult>(`/api/deals/${dealId}/turn`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  
  runScenario: (scenarioId: string) =>
    apiClient<ScenarioRunResult>(`/api/scenarios/${scenarioId}/run`, {
      method: 'POST',
    }),
    
  listScenarios: () =>
    apiClient<{ scenarios: any[] }>('/api/scenarios'),
};
