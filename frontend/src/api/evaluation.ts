import { apiClient } from './client';
import { EvaluationBenchmark } from '../types';

export const evaluationApi = {
  getBenchmark: () => apiClient<EvaluationBenchmark>('/api/evaluation'),
};
