// ============================================================================
// MemoryGuard Unified API Client
// Handles baseURL, headers, error normalization, and response serialization
// ============================================================================

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
  
  const headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...options.headers,
  });

  const config: RequestInit = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      let errorBody: any;
      try {
        errorBody = await response.json();
      } catch {
        errorBody = await response.text();
      }
      
      const errorMessage = errorBody?.detail || errorBody?.message || `HTTP ${response.status}: ${response.statusText}`;
      throw new ApiError(errorMessage, response.status, errorBody);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network or connection failure
    throw new ApiError(
      `Unable to connect to MemoryGuard backend at ${API_BASE_URL}. Please ensure the server is running.`,
      0,
      error
    );
  }
}
