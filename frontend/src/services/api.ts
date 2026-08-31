/**
 * api.ts — Centralized HTTP client for Aegis360 backend
 *
 * All API calls go through this module. It:
 * - Sets the base URL pointing at the Flask backend
 * - Automatically attaches the JWT Bearer token to every request
 * - Handles 401 responses by clearing the session and redirecting to login
 */

const BASE_URL = 'http://localhost:5000'

/**
 * Retrieve the stored JWT token from localStorage
 */
export function getToken(): string | null {
  return localStorage.getItem('aegis_token')
}

/**
 * Save JWT token to localStorage
 */
export function saveToken(token: string): void {
  localStorage.setItem('aegis_token', token)
}

/**
 * Remove JWT token from localStorage (logout)
 */
export function clearToken(): void {
  localStorage.removeItem('aegis_token')
}

/**
 * Build standard headers for every request.
 * Includes Authorization header if a token is present.
 */
function buildHeaders(extra: Record<string, string> = {}): HeadersInit {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...extra,
  }
  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

/**
 * Core fetch wrapper. Throws an error with the backend's error message
 * if the response status is not OK.
 */
async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: buildHeaders(options.headers as Record<string, string>),
  })

  // If the server returns 401 (token expired / invalid), clear session
  if (response.status === 401) {
    clearToken()
    window.location.href = '/login'
    throw new Error('Session expired. Please log in again.')
  }

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || data.message || `Request failed: ${response.status}`)
  }

  return data as T
}

// ─── Auth endpoints ────────────────────────────────────────────────────────────

export interface LoginResponse {
  message: string
  access_token: string
  user: {
    id: string
    email: string
    first_name: string
    last_name: string
    is_active: boolean
  }
  roles: string[]
  permissions: string[]
}

export const authApi = {
  /**
   * POST /api/auth/mock-login
   * Authenticates with the backend and returns a JWT token + user metadata.
   */
  mockLogin(email: string): Promise<LoginResponse> {
    return request<LoginResponse>('/api/auth/mock-login', {
      method: 'POST',
      body: JSON.stringify({ email }),
    })
  },
}

// ─── DPIA / Assessment endpoints ───────────────────────────────────────────────

export interface AssessmentSummary {
  id: string
  title: string
  project_manager: string
  department_function_agency: string | null
  status: string
  created_by: string
  created_at: string
  updated_at: string
}

export interface AssessmentListResponse {
  assessments: AssessmentSummary[]
  total: number
}

export const dpiaApi = {
  /**
   * GET /api/dpia/assessments
   * List all assessments, optionally filtered by comma-separated statuses.
   * e.g. dpiaApi.listAssessments('draft,screening')
   */
  listAssessments(status?: string): Promise<AssessmentListResponse> {
    const query = status ? `?status=${encodeURIComponent(status)}` : ''
    return request<AssessmentListResponse>(`/api/dpia/assessments${query}`)
  },

  /**
   * GET /api/dpia/assessments/:id
   */
  getAssessment(id: string): Promise<{ assessment: AssessmentSummary }> {
    return request(`/api/dpia/assessments/${id}`)
  },

  /**
   * POST /api/dpia/assessments
   */
  createAssessment(payload: {
    title: string
    project_manager: string
  }): Promise<{ message: string; id: string }> {
    return request('/api/dpia/assessments', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  // Questions
  getQuestions(section?: string): Promise<{ questions: any[] }> {
    const query = section ? `?section=${encodeURIComponent(section)}` : ''
    return request(`/api/dpia/questions${query}`)
  },

  createQuestion(payload: any): Promise<{ message: string; id: string }> {
    return request('/api/dpia/questions', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  updateQuestion(id: number | string, payload: any): Promise<{ message: string }> {
    return request(`/api/dpia/questions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },

  deleteQuestion(id: number | string): Promise<{ message: string }> {
    return request(`/api/dpia/questions/${id}`, {
      method: 'DELETE',
    })
  },

  // Responses
  getResponses(assessmentId: string, section?: string): Promise<{ responses: Record<string, any> }> {
    const query = section ? `?section=${encodeURIComponent(section)}` : ''
    return request(`/api/dpia/assessments/${assessmentId}/responses${query}`)
  },

  saveResponses(assessmentId: string, responses: Record<string, any>): Promise<{ message: string }> {
    return request(`/api/dpia/assessments/${assessmentId}/responses`, {
      method: 'PUT',
      body: JSON.stringify({ responses }),
    })
  },
}

// ─── Users endpoints ────────────────────────────────────────────────────────

export interface UserRecord {
  id: string
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  roles: string[]
  created_at: string
}

export interface RoleRecord {
  id: string
  name: string
  description: string | null
}

export const usersApi = {
  listUsers(): Promise<{ users: UserRecord[]; total: number }> {
    return request('/api/users')
  },

  toggleStatus(userId: string): Promise<{ id: string; is_active: boolean; message: string }> {
    return request(`/api/users/${userId}/toggle-status`, { method: 'PATCH' })
  },

  assignRole(userId: string, role: string): Promise<{ message: string; roles: string[] }> {
    return request(`/api/users/${userId}/roles`, {
      method: 'POST',
      body: JSON.stringify({ role }),
    })
  },

  removeRole(userId: string, roleName: string): Promise<{ message: string; roles: string[] }> {
    return request(`/api/users/${userId}/roles/${encodeURIComponent(roleName)}`, { method: 'DELETE' })
  },

  listRoles(): Promise<{ roles: RoleRecord[] }> {
    return request('/api/users/meta/roles')
  },
}
