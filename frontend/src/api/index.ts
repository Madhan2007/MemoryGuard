export * from './client';
export * from './deals';
export * from './assistant';
export * from './memories';
export * from './outcomes';
export * from './evaluation';
export * from './health';

import { dealsApi } from './deals';
import { assistantApi } from './assistant';
import { memoriesApi } from './memories';
import { outcomesApi } from './outcomes';
import { evaluationApi } from './evaluation';
import { healthApi } from './health';

export const api = {
  deals: dealsApi,
  assistant: assistantApi,
  memories: memoriesApi,
  outcomes: outcomesApi,
  evaluation: evaluationApi,
  health: healthApi,
};

export default api;
