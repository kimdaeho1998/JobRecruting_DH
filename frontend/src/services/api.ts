const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export type JobPostingSummary = {
  id: number;
  company_id: number;
  company_name: string;
  title: string;
  job_category?: string | null;
  location?: string | null;
  job_type?: string | null;
  experience_level?: string | null;
  salary_range?: string | null;
  deadline?: string | null;
  source_site?: string | null;
  source_url?: string | null;
  is_active: boolean;
  skills: string[];
};

export type JobPostingDetail = JobPostingSummary & {
  description?: string | null;
  created_at: string;
  updated_at: string;
};

export type JobFilters = {
  q?: string;
  job_category?: string;
  company_name?: string;
  location?: string;
  experience_level?: string;
  skill?: string;
  deadline_from?: string;
  deadline_to?: string;
  limit?: number;
};

export type Company = {
  id: number;
  name: string;
  website?: string | null;
  industry?: string | null;
  description?: string | null;
  created_at: string;
  updated_at: string;
};

export type Skill = {
  id: number;
  name: string;
  category?: string | null;
  created_at: string;
  updated_at: string;
};

export type ApplicationItem = {
  id: number;
  user_id: number;
  job_posting_id: number;
  status: string;
  notes?: string | null;
  applied_at?: string | null;
  deadline?: string | null;
  created_at: string;
  updated_at: string;
  job_title?: string | null;
  company_name?: string | null;
};

export type DashboardStats = {
  total_job_postings: number;
  active_job_postings: number;
  new_job_postings: number;
  deadline_soon_job_postings: number;
  total_companies: number;
  total_skills: number;
  total_bookmarks: number;
  total_applications: number;
  total_company_follows: number;
  applications_by_status: Record<string, number>;
  completed_applications: number;
  top_skills: Array<{ name: string; value: number }>;
  job_count_by_location: Array<{ name: string; value: number }>;
  job_count_by_category: Array<{ name: string; value: number }>;
  application_status_ratio: Array<{ name: string; value: number }>;
};

export type AIAnalysisRequest = {
  prompt_file?: string;
  company_name?: string | null;
  job_title?: string | null;
  job_description?: string | null;
  resume_text?: string | null;
  job_a_title?: string | null;
  job_a_description?: string | null;
  job_b_title?: string | null;
  job_b_description?: string | null;
};

export type AIAnalysisResponse = {
  prompt_file: string;
  result: Record<string, unknown>;
};

export type BookmarkPayload = {
  user_id?: number;
  job_posting_id: number;
};

export type ApplicationPayload = {
  user_id?: number;
  job_posting_id: number;
  status: string;
  notes?: string;
  applied_at?: string;
  deadline?: string;
};

const buildQuery = (params: Record<string, string | number | boolean | undefined>) => {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      query.set(key, String(value));
    }
  });
  const queryString = query.toString();
  return queryString ? `?${queryString}` : '';
};

const request = async <T>(path: string, options?: RequestInit): Promise<T> => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `API request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
};

export const api = {
  listJobPostings: (filters: JobFilters = {}) =>
    request<JobPostingSummary[]>(`/job-postings${buildQuery({ limit: 50, ...filters })}`),

  getJobPosting: (id: number) => request<JobPostingDetail>(`/job-postings/${id}`),

  listCompanies: () => request<Company[]>('/companies'),

  listSkills: () => request<Skill[]>('/skills'),

  addBookmark: (payload: BookmarkPayload) =>
    request('/bookmarks', {
      method: 'POST',
      body: JSON.stringify({ user_id: 1, ...payload }),
    }),

  deleteBookmark: (jobPostingId: number, userId = 1) =>
    request<void>(`/bookmarks${buildQuery({ user_id: userId, job_posting_id: jobPostingId })}`, {
      method: 'DELETE',
    }),

  listApplications: (userId = 1) =>
    request<ApplicationItem[]>(`/applications${buildQuery({ user_id: userId })}`),

  createApplication: (payload: ApplicationPayload) =>
    request<ApplicationItem>('/applications', {
      method: 'POST',
      body: JSON.stringify({ user_id: 1, ...payload }),
    }),

  updateApplication: (applicationId: number, status: string) =>
    request<ApplicationItem>(`/applications/${applicationId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    }),

  addCompanyFollow: (companyId: number, userId = 1) =>
    request('/company-follows', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, company_id: companyId }),
    }),

  deleteCompanyFollow: (companyId: number, userId = 1) =>
    request<void>(`/company-follows${buildQuery({ user_id: userId, company_id: companyId })}`, {
      method: 'DELETE',
    }),

  getDashboardStats: () => request<DashboardStats>('/dashboard/stats'),

  analyzeAI: (payload: AIAnalysisRequest, path = '/ai/analyze') =>
    request<AIAnalysisResponse>(path, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
