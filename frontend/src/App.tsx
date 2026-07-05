import { useEffect, useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  api,
  type ApplicationItem,
  type Company,
  type DashboardStats,
  type JobFilters,
  type JobPostingDetail,
  type JobPostingSummary,
  type Skill,
} from './services/api';

type Page = 'home' | 'jobs' | 'detail' | 'bookmarks' | 'applications' | 'dashboard' | 'compare';

const navItems: Array<{ page: Page; label: string }> = [
  { page: 'home', label: 'Home' },
  { page: 'jobs', label: 'Job List' },
  { page: 'bookmarks', label: 'Bookmark' },
  { page: 'applications', label: 'Application Board' },
  { page: 'dashboard', label: 'Dashboard' },
  { page: 'compare', label: 'Compare Jobs' },
];

const applicationStatuses = ['관심', '지원 예정', '지원 완료', '서류 합격', '면접', '최종 합격', '불합격'];

const readStoredNumbers = (key: string) => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as number[]) : [];
  } catch {
    return [];
  }
};

const writeStoredNumbers = (key: string, values: number[]) => {
  localStorage.setItem(key, JSON.stringify(values));
};

const formatDate = (value?: string | null) => {
  if (!value) {
    return '미정';
  }
  return value.slice(0, 10);
};

const uniqueValues = (jobs: JobPostingSummary[], selector: (job: JobPostingSummary) => string | null | undefined) =>
  Array.from(new Set(jobs.map(selector).filter(Boolean) as string[])).sort();

const statusLabel = (status: string) => {
  const labels: Record<string, string> = {
    관심: '관심',
    '지원 예정': '지원 예정',
    '지원 완료': '지원 완료',
    '서류 합격': '서류 합격',
    면접: '면접',
    '최종 합격': '최종 합격',
    불합격: '불합격',
  };
  return labels[status] ?? status;
};

const emptyFilters: JobFilters = {
  q: '',
  job_category: '',
  company_name: '',
  location: '',
  experience_level: '',
  skill: '',
  deadline_to: '',
};

const App = () => {
  const [page, setPage] = useState<Page>('home');
  const [jobs, setJobs] = useState<JobPostingSummary[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [applications, setApplications] = useState<ApplicationItem[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [selectedJob, setSelectedJob] = useState<JobPostingDetail | null>(null);
  const [filters, setFilters] = useState<JobFilters>(emptyFilters);
  const [bookmarkedIds, setBookmarkedIds] = useState<number[]>(() => readStoredNumbers('jobinsight.bookmarks'));
  const [compareIds, setCompareIds] = useState<number[]>(() => readStoredNumbers('jobinsight.compare'));
  const [aiDetailAnalysis, setAiDetailAnalysis] = useState<Record<string, unknown> | null>(null);
  const [compareAnalysis, setCompareAnalysis] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const categoryOptions = useMemo(() => uniqueValues(jobs, (job) => job.job_category), [jobs]);
  const locationOptions = useMemo(() => uniqueValues(jobs, (job) => job.location), [jobs]);
  const experienceOptions = useMemo(() => uniqueValues(jobs, (job) => job.experience_level), [jobs]);
  const bookmarkedJobs = useMemo(
    () => jobs.filter((job) => bookmarkedIds.includes(job.id)),
    [bookmarkedIds, jobs],
  );
  const compareJobs = useMemo(() => jobs.filter((job) => compareIds.includes(job.id)), [compareIds, jobs]);

  const loadCatalog = async () => {
    const [companyData, skillData] = await Promise.all([api.listCompanies(), api.listSkills()]);
    setCompanies(companyData);
    setSkills(skillData);
  };

  const loadJobs = async (nextFilters = filters) => {
    setLoading(true);
    setError('');
    try {
      const data = await api.listJobPostings(nextFilters);
      setJobs(data);
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '채용공고를 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const loadApplications = async () => {
    try {
      setApplications(await api.listApplications());
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '지원현황을 불러오지 못했습니다.');
    }
  };

  const loadStats = async () => {
    try {
      setStats(await api.getDashboardStats());
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '대시보드 통계를 불러오지 못했습니다.');
    }
  };

  const loadAiDetailAnalysis = async (job: JobPostingDetail) => {
    try {
      const [summaryResponse, skillResponse, fitResponse] = await Promise.all([
        api.analyzeAI(
          {
            company_name: job.company_name,
            job_title: job.title,
            job_description: job.description ?? '',
          },
          '/ai/summary',
        ),
        api.analyzeAI(
          {
            company_name: job.company_name,
            job_title: job.title,
            job_description: job.description ?? '',
          },
          '/ai/skills',
        ),
        api.analyzeAI(
          {
            company_name: job.company_name,
            job_title: job.title,
            job_description: job.description ?? '',
            resume_text: '',
          },
          '/ai/fit',
        ),
      ]);

      setAiDetailAnalysis({
        summary: summaryResponse.result,
        skills: skillResponse.result,
        fit: fitResponse.result,
      });
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : 'AI 분석 결과를 불러오지 못했습니다.');
    }
  };

  useEffect(() => {
    void loadJobs();
    void loadCatalog();
    void loadApplications();
    void loadStats();
  }, []);

  useEffect(() => {
    writeStoredNumbers('jobinsight.bookmarks', bookmarkedIds);
  }, [bookmarkedIds]);

  useEffect(() => {
    writeStoredNumbers('jobinsight.compare', compareIds);
  }, [compareIds]);

  useEffect(() => {
    const loadCompareAnalysis = async () => {
      if (compareJobs.length < 2) {
        setCompareAnalysis(null);
        return;
      }

      try {
        const [firstJob, secondJob] = compareJobs;
        const response = await api.analyzeAI(
          {
            job_a_title: firstJob.title,
            job_a_description: '',
            job_b_title: secondJob.title,
            job_b_description: '',
          },
          '/ai/compare',
        );
        setCompareAnalysis(response.result);
      } catch (apiError) {
        setError(apiError instanceof Error ? apiError.message : '공고 비교 AI 분석에 실패했습니다.');
      }
    };

    void loadCompareAnalysis();
  }, [compareJobs]);

  const openDetail = async (jobId: number) => {
    setLoading(true);
    setError('');
    try {
      const detail = await api.getJobPosting(jobId);
      setSelectedJob(detail);
      setAiDetailAnalysis(null);
      void loadAiDetailAnalysis(detail);
      setPage('detail');
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '상세 정보를 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: keyof JobFilters, value: string) => {
    setFilters((current) => ({ ...current, [key]: value }));
  };

  const submitSearch = () => {
    void loadJobs(filters);
    setPage('jobs');
  };

  const resetFilters = () => {
    setFilters(emptyFilters);
    void loadJobs(emptyFilters);
  };

  const toggleBookmark = async (job: JobPostingSummary) => {
    const isBookmarked = bookmarkedIds.includes(job.id);
    setBookmarkedIds((current) =>
      isBookmarked ? current.filter((id) => id !== job.id) : Array.from(new Set([...current, job.id])),
    );
    try {
      if (isBookmarked) {
        await api.deleteBookmark(job.id);
      } else {
        await api.addBookmark({ job_posting_id: job.id });
      }
      void loadStats();
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '북마크 변경에 실패했습니다.');
    }
  };

  const toggleCompare = (jobId: number) => {
    setCompareIds((current) => {
      if (current.includes(jobId)) {
        return current.filter((id) => id !== jobId);
      }
      return current.length >= 3 ? [...current.slice(1), jobId] : [...current, jobId];
    });
  };

  const changeApplicationStatus = async (job: JobPostingSummary, status: string) => {
    try {
      const existing = applications.find((application) => application.job_posting_id === job.id);
      if (existing) {
        await api.updateApplication(existing.id, status);
      } else {
        await api.createApplication({ job_posting_id: job.id, status });
      }
      await loadApplications();
      await loadStats();
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '지원현황 변경에 실패했습니다.');
    }
  };

  const toggleCompanyFollow = async (companyId: number) => {
    try {
      await api.addCompanyFollow(companyId);
      await loadStats();
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : '관심기업 변경에 실패했습니다.');
    }
  };

  const renderPage = () => {
    if (page === 'home') {
      return (
        <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-teal-700">JobInsight AI</p>
            <h1 className="mt-3 text-3xl font-bold text-slate-950">채용공고를 한 곳에서 검색하고 관리하세요.</h1>
            <p className="mt-3 text-slate-600">
              공고 탐색, 북마크, 지원현황, 비교, 대시보드까지 MVP 흐름을 한 화면 구조에서 확인할 수 있습니다.
            </p>
            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              <SearchBox filters={filters} onChange={handleFilterChange} onSubmit={submitSearch} compact />
              <button className="btn-primary" type="button" onClick={() => setPage('jobs')}>
                공고 보기
              </button>
            </div>
          </div>
          <StatsPreview stats={stats} />
        </section>
      );
    }

    if (page === 'detail') {
      return selectedJob ? (
        <JobDetailPage
          job={selectedJob}
          aiAnalysis={aiDetailAnalysis}
          isBookmarked={bookmarkedIds.includes(selectedJob.id)}
          isCompared={compareIds.includes(selectedJob.id)}
          onBack={() => setPage('jobs')}
          onBookmark={() => void toggleBookmark(selectedJob)}
          onCompare={() => toggleCompare(selectedJob.id)}
          onApply={(status) => void changeApplicationStatus(selectedJob, status)}
          onFollow={() => void toggleCompanyFollow(selectedJob.company_id)}
        />
      ) : (
        <EmptyState title="선택된 공고가 없습니다." actionLabel="목록으로 이동" onAction={() => setPage('jobs')} />
      );
    }

    if (page === 'bookmarks') {
      return (
        <JobCollection
          title="Bookmark"
          description="로컬 목록과 백엔드 북마크 API를 함께 사용해 저장한 공고를 보여줍니다."
          jobs={bookmarkedJobs}
          bookmarkedIds={bookmarkedIds}
          compareIds={compareIds}
          onOpen={openDetail}
          onBookmark={toggleBookmark}
          onCompare={toggleCompare}
          onApply={changeApplicationStatus}
        />
      );
    }

    if (page === 'applications') {
      return <ApplicationBoard applications={applications} />;
    }

    if (page === 'dashboard') {
      return <Dashboard stats={stats} jobs={jobs} />;
    }

    if (page === 'compare') {
      return <CompareJobs jobs={compareJobs} analysis={compareAnalysis} onOpen={openDetail} onRemove={toggleCompare} />;
    }

    return (
      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <FilterSidebar
          filters={filters}
          categories={categoryOptions}
          companies={companies}
          locations={locationOptions}
          experiences={experienceOptions}
          skills={skills}
          onChange={handleFilterChange}
          onSubmit={submitSearch}
          onReset={resetFilters}
        />
        <JobCollection
          title="Job List"
          description={`${jobs.length}개의 공고를 탐색 중입니다.`}
          jobs={jobs}
          bookmarkedIds={bookmarkedIds}
          compareIds={compareIds}
          onOpen={openDetail}
          onBookmark={toggleBookmark}
          onCompare={toggleCompare}
          onApply={changeApplicationStatus}
        />
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-950">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 lg:flex-row lg:items-center lg:justify-between">
          <button className="text-left" type="button" onClick={() => setPage('home')}>
            <p className="text-sm font-semibold text-teal-700">JobInsight AI</p>
            <p className="text-xl font-bold">Recruiting Workspace</p>
          </button>
          <nav className="flex gap-2 overflow-x-auto pb-1">
            {navItems.map((item) => (
              <button
                className={`nav-button ${page === item.page ? 'nav-button-active' : ''}`}
                key={item.page}
                type="button"
                onClick={() => setPage(item.page)}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto flex max-w-7xl flex-col gap-5 px-4 py-6">
        <SearchBar filters={filters} onChange={handleFilterChange} onSubmit={submitSearch} />
        {error ? <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div> : null}
        {loading ? <div className="rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm">불러오는 중...</div> : null}
        {renderPage()}
      </main>
    </div>
  );
};

type SearchProps = {
  filters: JobFilters;
  onChange: (key: keyof JobFilters, value: string) => void;
  onSubmit: () => void;
  compact?: boolean;
};

const SearchBox = ({ filters, onChange, onSubmit, compact = false }: SearchProps) => (
  <div className={`flex w-full gap-2 ${compact ? 'sm:max-w-xl' : ''}`}>
    <input
      className="input"
      placeholder="직무, 회사, 기술스택 검색"
      value={filters.q ?? ''}
      onChange={(event) => onChange('q', event.target.value)}
      onKeyDown={(event) => {
        if (event.key === 'Enter') {
          onSubmit();
        }
      }}
    />
    <button className="btn-primary shrink-0" type="button" onClick={onSubmit}>
      검색
    </button>
  </div>
);

const SearchBar = ({ filters, onChange, onSubmit }: SearchProps) => (
  <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
    <SearchBox filters={filters} onChange={onChange} onSubmit={onSubmit} />
  </section>
);

type FilterSidebarProps = {
  filters: JobFilters;
  categories: string[];
  companies: Company[];
  locations: string[];
  experiences: string[];
  skills: Skill[];
  onChange: (key: keyof JobFilters, value: string) => void;
  onSubmit: () => void;
  onReset: () => void;
};

const FilterSidebar = ({
  filters,
  categories,
  companies,
  locations,
  experiences,
  skills,
  onChange,
  onSubmit,
  onReset,
}: FilterSidebarProps) => (
  <aside className="h-fit rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
    <div className="flex items-center justify-between">
      <h2 className="text-lg font-bold">필터</h2>
      <button className="text-sm font-semibold text-slate-500 hover:text-slate-950" type="button" onClick={onReset}>
        초기화
      </button>
    </div>
    <div className="mt-4 grid gap-4">
      <SelectField label="직무" value={filters.job_category} options={categories} onChange={(value) => onChange('job_category', value)} />
      <SelectField label="회사명" value={filters.company_name} options={companies.map((company) => company.name)} onChange={(value) => onChange('company_name', value)} />
      <SelectField label="지역" value={filters.location} options={locations} onChange={(value) => onChange('location', value)} />
      <SelectField label="경력" value={filters.experience_level} options={experiences} onChange={(value) => onChange('experience_level', value)} />
      <SelectField label="기술스택" value={filters.skill} options={skills.map((skill) => skill.name)} onChange={(value) => onChange('skill', value)} />
      <label className="grid gap-1 text-sm font-semibold text-slate-700">
        마감일
        <input className="input" type="date" value={filters.deadline_to ?? ''} onChange={(event) => onChange('deadline_to', event.target.value)} />
      </label>
      <button className="btn-primary" type="button" onClick={onSubmit}>
        필터 적용
      </button>
    </div>
  </aside>
);

type SelectFieldProps = {
  label: string;
  value?: string;
  options: string[];
  onChange: (value: string) => void;
};

const SelectField = ({ label, value, options, onChange }: SelectFieldProps) => (
  <label className="grid gap-1 text-sm font-semibold text-slate-700">
    {label}
    <select className="input" value={value ?? ''} onChange={(event) => onChange(event.target.value)}>
      <option value="">전체</option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  </label>
);

type JobCollectionProps = {
  title: string;
  description: string;
  jobs: JobPostingSummary[];
  bookmarkedIds: number[];
  compareIds: number[];
  onOpen: (jobId: number) => void;
  onBookmark: (job: JobPostingSummary) => void;
  onCompare: (jobId: number) => void;
  onApply: (job: JobPostingSummary, status: string) => void;
};

const JobCollection = ({
  title,
  description,
  jobs,
  bookmarkedIds,
  compareIds,
  onOpen,
  onBookmark,
  onCompare,
  onApply,
}: JobCollectionProps) => (
  <section className="grid gap-4">
    <div>
      <h1 className="text-2xl font-bold">{title}</h1>
      <p className="text-sm text-slate-600">{description}</p>
    </div>
    {jobs.length ? (
      <div className="grid gap-4 xl:grid-cols-2">
        {jobs.map((job) => (
          <JobCard
            isBookmarked={bookmarkedIds.includes(job.id)}
            isCompared={compareIds.includes(job.id)}
            job={job}
            key={job.id}
            onApply={onApply}
            onBookmark={onBookmark}
            onCompare={onCompare}
            onOpen={onOpen}
          />
        ))}
      </div>
    ) : (
      <EmptyState title="표시할 공고가 없습니다." actionLabel="공고 목록 새로고침" onAction={() => window.location.reload()} />
    )}
  </section>
);

type JobCardProps = {
  job: JobPostingSummary;
  isBookmarked: boolean;
  isCompared: boolean;
  onOpen: (jobId: number) => void;
  onBookmark: (job: JobPostingSummary) => void;
  onCompare: (jobId: number) => void;
  onApply: (job: JobPostingSummary, status: string) => void;
};

const JobCard = ({ job, isBookmarked, isCompared, onOpen, onBookmark, onCompare, onApply }: JobCardProps) => (
  <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
    <div className="flex items-start justify-between gap-3">
      <div>
        <p className="text-sm font-semibold text-teal-700">{job.company_name}</p>
        <button className="mt-1 text-left text-xl font-bold hover:text-teal-700" type="button" onClick={() => onOpen(job.id)}>
          {job.title}
        </button>
      </div>
      <button className={isBookmarked ? 'btn-dark' : 'btn-secondary'} type="button" onClick={() => onBookmark(job)}>
        {isBookmarked ? '저장됨' : '북마크'}
      </button>
    </div>
    <div className="mt-4 grid gap-2 text-sm text-slate-600 sm:grid-cols-2">
      <span>직무: {job.job_category ?? '미정'}</span>
      <span>지역: {job.location ?? '미정'}</span>
      <span>경력: {job.experience_level ?? '미정'}</span>
      <span>마감: {formatDate(job.deadline)}</span>
    </div>
    <div className="mt-4 flex flex-wrap gap-2">
      {job.skills.map((skill) => (
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700" key={skill}>
          {skill}
        </span>
      ))}
    </div>
    <div className="mt-5 flex flex-wrap gap-2">
      <button className="btn-secondary" type="button" onClick={() => onOpen(job.id)}>
        상세
      </button>
      <button className={isCompared ? 'btn-dark' : 'btn-secondary'} type="button" onClick={() => onCompare(job.id)}>
        {isCompared ? '비교중' : '비교'}
      </button>
      <select className="input max-w-40" defaultValue="" onChange={(event) => onApply(job, event.target.value)}>
        <option value="" disabled>
          지원현황 변경
        </option>
        {applicationStatuses.map((status) => (
          <option key={status} value={status}>
            {statusLabel(status)}
          </option>
        ))}
      </select>
    </div>
  </article>
);

type JobDetailPageProps = {
  job: JobPostingDetail;
  aiAnalysis: Record<string, unknown> | null;
  isBookmarked: boolean;
  isCompared: boolean;
  onBack: () => void;
  onBookmark: () => void;
  onCompare: () => void;
  onApply: (status: string) => void;
  onFollow: () => void;
};

const JobDetailPage = ({ job, aiAnalysis, isBookmarked, isCompared, onBack, onBookmark, onCompare, onApply, onFollow }: JobDetailPageProps) => {
  const summaryPayload = aiAnalysis?.summary as { summary?: string; key_responsibilities?: string[]; required_skills?: string[] } | undefined;
  const skillPayload = aiAnalysis?.skills as { technical_skills?: string[]; preferred_skills?: string[] } | undefined;
  const fitPayload = aiAnalysis?.fit as { fit_score?: number; summary?: string; strengths?: string[]; gaps?: string[] } | undefined;

  return (
    <section className="grid gap-5">
    <button className="w-fit text-sm font-semibold text-slate-600 hover:text-slate-950" type="button" onClick={onBack}>
      목록으로 돌아가기
    </button>
    <article className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <p className="text-sm font-semibold text-teal-700">{job.company_name}</p>
          <h1 className="mt-2 text-3xl font-bold">{job.title}</h1>
          <p className="mt-3 text-slate-600">{job.description ?? '상세 설명이 없습니다.'}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button className={isBookmarked ? 'btn-dark' : 'btn-secondary'} type="button" onClick={onBookmark}>
            {isBookmarked ? '북마크 해제' : '북마크'}
          </button>
          <button className={isCompared ? 'btn-dark' : 'btn-secondary'} type="button" onClick={onCompare}>
            {isCompared ? '비교 제거' : '비교 추가'}
          </button>
          <button className="btn-secondary" type="button" onClick={onFollow}>
            관심기업
          </button>
        </div>
      </div>
      <div className="mt-6 grid gap-3 rounded-lg bg-slate-50 p-4 text-sm md:grid-cols-3">
        <span>직무: {job.job_category ?? '미정'}</span>
        <span>지역: {job.location ?? '미정'}</span>
        <span>경력: {job.experience_level ?? '미정'}</span>
        <span>급여: {job.salary_range ?? '협의'}</span>
        <span>마감: {formatDate(job.deadline)}</span>
        <span>출처: {job.source_site ?? '미정'}</span>
      </div>
      <div className="mt-5 flex flex-wrap gap-2">
        {job.skills.map((skill) => (
          <span className="rounded-full bg-teal-50 px-3 py-1 text-sm font-semibold text-teal-800" key={skill}>
            {skill}
          </span>
        ))}
      </div>
      <div className="mt-6 flex flex-wrap gap-2">
        {applicationStatuses.map((status) => (
          <button className="btn-secondary" key={status} type="button" onClick={() => onApply(status)}>
            {statusLabel(status)}
          </button>
        ))}
      </div>
      {aiAnalysis ? (
        <div className="mt-6 rounded-lg border border-teal-200 bg-teal-50 p-5">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-lg font-bold text-teal-900">AI 분석 결과</h2>
            <span className="rounded-full bg-white px-3 py-1 text-sm font-semibold text-teal-700">Mock Response</span>
          </div>
          <div className="mt-4 grid gap-4 lg:grid-cols-3">
            <div className="rounded-lg bg-white p-4">
              <p className="text-sm font-semibold text-slate-700">공고 요약</p>
              <p className="mt-2 text-sm text-slate-600">{summaryPayload?.summary ?? '요약 준비 중입니다.'}</p>
              <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">
                {(summaryPayload?.key_responsibilities ?? []).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="rounded-lg bg-white p-4">
              <p className="text-sm font-semibold text-slate-700">기술스택</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {(skillPayload?.technical_skills ?? []).concat(skillPayload?.preferred_skills ?? []).map((item) => (
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700" key={item}>
                    {item}
                  </span>
                ))}
              </div>
            </div>
            <div className="rounded-lg bg-white p-4">
              <p className="text-sm font-semibold text-slate-700">적합도</p>
              <p className="mt-2 text-3xl font-bold text-teal-700">{fitPayload?.fit_score ?? 0}</p>
              <p className="mt-2 text-sm text-slate-600">{fitPayload?.summary ?? '적합도 분석 준비 중입니다.'}</p>
            </div>
          </div>
        </div>
      ) : null}
    </article>
  </section>
  );
};

const ApplicationBoard = ({ applications }: { applications: ApplicationItem[] }) => {
  const [draggedId, setDraggedId] = useState<number | null>(null);

  const updateStatus = async (applicationId: number, status: string) => {
    try {
      await api.updateApplication(applicationId, status);
      window.location.reload();
    } catch {
      // noop
    }
  };

  return (
    <section className="grid gap-4">
      <div>
        <h1 className="text-2xl font-bold">Application Board</h1>
        <p className="text-sm text-slate-600">드래그 앤 드롭으로 지원 상태를 변경하고, 마감일과 메모를 관리합니다.</p>
      </div>
      <div className="grid gap-4 xl:grid-cols-2 2xl:grid-cols-4">
        {applicationStatuses.map((status) => (
          <div
            className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
            key={status}
            onDragOver={(event) => event.preventDefault()}
            onDrop={() => {
              if (draggedId) {
                void updateStatus(draggedId, status);
              }
            }}
          >
            <div className="flex items-center justify-between">
              <h2 className="font-bold">{statusLabel(status)}</h2>
              <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">
                {applications.filter((application) => application.status === status).length}
              </span>
            </div>
            <div className="mt-3 grid gap-3">
              {applications.filter((application) => application.status === status).map((application) => {
                const deadline = application.deadline ? new Date(application.deadline) : null;
                const isDeadlineSoon = deadline && deadline.getTime() - Date.now() < 7 * 24 * 60 * 60 * 1000;

                return (
                  <div
                    className={`rounded-lg border p-3 text-sm ${isDeadlineSoon ? 'border-red-200 bg-red-50' : 'border-slate-200 bg-slate-50'}`}
                    draggable
                    key={application.id}
                    onDragStart={() => setDraggedId(application.id)}
                  >
                    <p className="font-semibold">{application.job_title ?? `공고 #${application.job_posting_id}`}</p>
                    <p className="text-slate-600">{application.company_name ?? '회사 미정'}</p>
                    <p className="mt-2 text-xs text-slate-500">지원일: {application.applied_at ? new Date(application.applied_at).toLocaleDateString() : '미기록'}</p>
                    <p className="text-xs text-slate-500">마감일: {application.deadline ? new Date(application.deadline).toLocaleDateString() : '미정'}</p>
                    <label className="mt-2 block text-xs text-slate-600">
                      메모
                      <div className="mt-1 rounded border border-slate-200 bg-white px-2 py-1 text-xs">{application.notes ?? '메모 없음'}</div>
                    </label>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

const Dashboard = ({
  stats,
  jobs,
}: {
  stats: DashboardStats | null;
  jobs: JobPostingSummary[];
}) => {
  const cards = [
    ['전체 공고', stats?.total_job_postings ?? jobs.length],
    ['신규 공고', stats?.new_job_postings ?? 0],
    ['마감 임박', stats?.deadline_soon_job_postings ?? 0],
    ['북마크', stats?.total_bookmarks ?? 0],
    ['지원 완료', stats?.completed_applications ?? 0],
    ['기술스택', stats?.total_skills ?? 0],
  ];

  const barData = (stats?.top_skills ?? []).map((item) => ({ name: item.name, value: item.value }));
  const locationData = (stats?.job_count_by_location ?? []).map((item) => ({ name: item.name, value: item.value }));
  const categoryData = (stats?.job_count_by_category ?? []).map((item) => ({ name: item.name, value: item.value }));
  const ratioData = (stats?.application_status_ratio ?? []).map((item) => ({ name: item.name, value: item.value }));

  return (
    <section className="grid gap-5">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-sm text-slate-600">공고와 지원 흐름을 한눈에 파악합니다.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map(([label, value]) => (
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm" key={label}>
            <p className="text-sm font-semibold text-slate-500">{label}</p>
            <p className="mt-2 text-3xl font-bold">{value}</p>
          </div>
        ))}
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="font-bold">기술스택 빈도 TOP 10</h2>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#0f766e" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="font-bold">지원현황 비율</h2>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={ratioData} dataKey="value" nameKey="name" outerRadius={90} label>
                  {ratioData.map((entry, index) => (
                    <Cell key={`${entry.name}-${index}`} fill={['#0f766e', '#14b8a6', '#2dd4bf', '#5eead4', '#99f6e4', '#ccfbf1'][index % 6]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="font-bold">지역별 공고 수</h2>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={locationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="font-bold">직무별 공고 수</h2>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#7c3aed" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="font-bold">지원 상태 분포</h2>
        <div className="mt-4 grid gap-3">
          {applicationStatuses.map((status) => (
            <div className="flex items-center justify-between rounded-lg bg-slate-50 px-4 py-3" key={status}>
              <span>{statusLabel(status)}</span>
              <strong>{stats?.applications_by_status[status] ?? 0}</strong>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

const CompareJobs = ({
  jobs,
  analysis,
  onOpen,
  onRemove,
}: {
  jobs: JobPostingSummary[];
  analysis: Record<string, unknown> | null;
  onOpen: (jobId: number) => void;
  onRemove: (jobId: number) => void;
}) => (
  <section className="grid gap-4">
    <div>
      <h1 className="text-2xl font-bold">Compare Jobs</h1>
      <p className="text-sm text-slate-600">최대 3개 공고를 나란히 비교합니다.</p>
    </div>
    {analysis ? (
      <div className="rounded-lg border border-teal-200 bg-teal-50 p-5">
        <h2 className="text-lg font-bold text-teal-900">AI 공고 비교 분석</h2>
        <p className="mt-2 text-sm text-slate-600">{(analysis as { comparison?: { differences?: string[] } } | null)?.comparison?.differences?.join(' · ') ?? '비교 분석이 준비되었습니다.'}</p>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div className="rounded-lg bg-white p-4">
            <p className="text-sm font-semibold text-slate-700">공고 A 장점</p>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
              {((analysis as { comparison?: { strengths_a?: string[] } } | null)?.comparison?.strengths_a ?? []).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-lg bg-white p-4">
            <p className="text-sm font-semibold text-slate-700">공고 B 장점</p>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
              {((analysis as { comparison?: { strengths_b?: string[] } } | null)?.comparison?.strengths_b ?? []).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
        <p className="mt-4 text-sm font-semibold text-teal-700">추천 공고: {(analysis as { recommended_job?: string } | null)?.recommended_job ?? '없음'}</p>
      </div>
    ) : null}
    {jobs.length ? (
      <div className="grid gap-4 lg:grid-cols-3">
        {jobs.map((job) => (
          <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm" key={job.id}>
            <p className="text-sm font-semibold text-teal-700">{job.company_name}</p>
            <h2 className="mt-2 text-xl font-bold">{job.title}</h2>
            <dl className="mt-4 grid gap-2 text-sm">
              <div className="flex justify-between gap-3">
                <dt className="text-slate-500">직무</dt>
                <dd className="text-right font-semibold">{job.job_category ?? '미정'}</dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-slate-500">지역</dt>
                <dd className="text-right font-semibold">{job.location ?? '미정'}</dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-slate-500">경력</dt>
                <dd className="text-right font-semibold">{job.experience_level ?? '미정'}</dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-slate-500">마감</dt>
                <dd className="text-right font-semibold">{formatDate(job.deadline)}</dd>
              </div>
            </dl>
            <div className="mt-4 flex flex-wrap gap-2">
              {job.skills.map((skill) => (
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold" key={skill}>
                  {skill}
                </span>
              ))}
            </div>
            <div className="mt-5 flex gap-2">
              <button className="btn-secondary" type="button" onClick={() => onOpen(job.id)}>
                상세
              </button>
              <button className="btn-secondary" type="button" onClick={() => onRemove(job.id)}>
                제거
              </button>
            </div>
          </article>
        ))}
      </div>
    ) : (
      <EmptyState title="비교할 공고가 없습니다." actionLabel="공고 목록으로 이동" onAction={() => window.scrollTo(0, 0)} />
    )}
  </section>
);

const StatsPreview = ({ stats }: { stats: DashboardStats | null }) => (
  <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
    <h2 className="text-lg font-bold">MVP Snapshot</h2>
    <div className="mt-4 grid grid-cols-2 gap-3">
      <MiniStat label="공고" value={stats?.total_job_postings ?? 0} />
      <MiniStat label="회사" value={stats?.total_companies ?? 0} />
      <MiniStat label="기술" value={stats?.total_skills ?? 0} />
      <MiniStat label="지원" value={stats?.total_applications ?? 0} />
    </div>
  </div>
);

const MiniStat = ({ label, value }: { label: string; value: number }) => (
  <div className="rounded-lg bg-slate-50 p-4">
    <p className="text-sm text-slate-500">{label}</p>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

const EmptyState = ({ title, actionLabel, onAction }: { title: string; actionLabel: string; onAction: () => void }) => (
  <div className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center">
    <p className="font-semibold">{title}</p>
    <button className="btn-primary mt-4" type="button" onClick={onAction}>
      {actionLabel}
    </button>
  </div>
);

export default App;
