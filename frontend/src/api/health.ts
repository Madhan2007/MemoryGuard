import { apiClient } from './client';
import { SystemStatus, AuditEvent, UserProfile } from '../types';

export interface AuditListResponse {
  audit_events: AuditEvent[];
  total: number;
}

export const healthApi = {
  getStatus: () => apiClient<SystemStatus>('/api/health'),
  getAuditTrail: (dealId?: string, limit: number = 50) => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (dealId) params.set('deal_id', dealId);
    return apiClient<AuditListResponse>(`/api/audit?${params.toString()}`);
  },
  getDemoUser: () => apiClient<UserProfile>('/api/auth/demo-user'),
  login: (email: string, password: string) =>
    apiClient<{ success: boolean; uid: string; email: string; display_name: string; custom_token?: string }>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  signup: (email: string, password: string, display_name: string) =>
    apiClient<{ success: boolean; uid: string; email: string; display_name: string }>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, display_name }),
    }),
};
