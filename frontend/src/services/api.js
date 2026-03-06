import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 120000,  // agents can take a while
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.response.use(
  r => r.data,
  err => {
    const msg = err.response?.data?.detail || err.message || 'Request failed'
    return Promise.reject(new Error(msg))
  }
)

// ── Projects ──────────────────────────────────────────────────────────────
export const projectsApi = {
  list:   ()       => api.get('/projects'),
  get:    (id)     => api.get(`/projects/${id}`),
  create: (data)   => api.post('/projects', data),
  update: (id, d)  => api.put(`/projects/${id}`, d),
  delete: (id)     => api.delete(`/projects/${id}`)
}

// ── ALM Integration ───────────────────────────────────────────────────────
export const almApi = {
  testConnection: (config)   => api.post('/alm/test-connection', config),
  fetchData:      (config)   => api.post('/alm/fetch-data', config),
  getSupportedTools: ()      => api.get('/alm/supported-tools'),
  mapToVSM:       (data)     => api.post('/alm/map-to-vsm', data)
}

// ── VSM Data ──────────────────────────────────────────────────────────────
export const vsmApi = {
  save:    (projectId, data)  => api.post(`/vsm/${projectId}`, data),
  get:     (projectId)        => api.get(`/vsm/${projectId}`),
  update:  (projectId, data)  => api.put(`/vsm/${projectId}`, data),
  getMetrics: (projectId)     => api.get(`/vsm/${projectId}/metrics`)
}

// ── Multi-Agent Orchestration ─────────────────────────────────────────────
export const agentsApi = {
  // Run the full end-to-end analysis pipeline
  runFullAnalysis:    (projectId) => api.post(`/agents/run-analysis/${projectId}`),
  getAnalysisStatus:  (runId)    => api.get(`/agents/status/${runId}`),
  getAnalysisResult:  (projectId) => api.get(`/agents/result/${projectId}`),

  // Individual agents (can be triggered separately)
  runVSMAnalyzer:       (projectId) => api.post(`/agents/vsm-analyzer/${projectId}`),
  runBottleneckAnalyzer:(projectId) => api.post(`/agents/bottleneck-analyzer/${projectId}`),
  runImprovementGen:    (projectId) => api.post(`/agents/improvement-generator/${projectId}`),
  runFutureStateDesign: (projectId, scenario) => api.post(`/agents/future-state-designer/${projectId}`, { scenario }),
  runBusinessCaseBuilder:(projectId, scenario) => api.post(`/agents/business-case-builder/${projectId}`, { scenario }),
  runBenchmarkAgent:    (projectId) => api.post(`/agents/benchmark-agent/${projectId}`),

  // Agent run history
  getRunHistory: (projectId) => api.get(`/agents/history/${projectId}`)
}

// ── Analysis Results ──────────────────────────────────────────────────────
export const analysisApi = {
  getBottlenecks:   (projectId) => api.get(`/analysis/${projectId}/bottlenecks`),
  getImprovements:  (projectId) => api.get(`/analysis/${projectId}/improvements`),
  getFutureState:   (projectId, scenario) => api.get(`/analysis/${projectId}/future-state/${scenario}`),
  getBusinessCase:  (projectId, scenario) => api.get(`/analysis/${projectId}/business-case/${scenario}`),
  getBenchmarks:    (projectId) => api.get(`/analysis/${projectId}/benchmarks`),
  exportReport:     (projectId, format) => api.get(`/analysis/${projectId}/export?format=${format}`, { responseType: 'blob' })
}

// ── Health ────────────────────────────────────────────────────────────────
export const healthApi = {
  check: () => api.get('/health')
}

export default api
