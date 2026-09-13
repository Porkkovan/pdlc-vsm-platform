import axios from 'axios'

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || '') + '/api/v1',
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
  delete: (id)     => api.delete(`/projects/${id}`),
  getOptionAParentMap: (id)      => api.get(`/projects/${id}/option-a-parent-map`),
  putOptionAParentMap: (id, map) => api.put(`/projects/${id}/option-a-parent-map`, { option_a_parent_map: map }),
  getCostModel:        (id)      => api.get(`/projects/${id}/cost-model`),
  putCostModelOverrides: (id, ov) => api.put(`/projects/${id}/cost-model`, { cost_model_overrides: ov }),
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
  // Run the full end-to-end analysis pipeline (optionally with DORA calibration)
  runFullAnalysis:    (projectId, doraCalibration) => api.post(`/agents/run-analysis/${projectId}`, doraCalibration ? { dora_calibration: doraCalibration } : {}),
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
  getRunHistory: (projectId) => api.get(`/agents/history/${projectId}`),

  // Automation Classifier — classifies SDLC activities as Manual/RPA/AI-Assisted/AI-Agent
  classifyAutomation: (projectId) => api.post(`/agents/classify-automation/${projectId}`),
  getAutomationClassifications: (projectId) => api.get(`/agents/automation-classifications/${projectId}`),
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

// ── Outcome Dashboard ─────────────────────────────────────────────────────
// q = { scenario, level, refresh, segment, product_group, product, team }
const ocq = (q = {}) => {
  const p = new URLSearchParams()
  Object.entries(q).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== '') p.append(k, v) })
  const s = p.toString()
  return s ? `?${s}` : ''
}
export const outcomeApi = {
  getCatalog:    ()                  => api.get('/outcome-dashboard/catalog'),
  getDashboard:  (projectId, q)      => api.get(`/outcome-dashboard/${projectId}${ocq(q)}`),
  refresh:       (projectId, q)      => api.post(`/outcome-dashboard/${projectId}/refresh${ocq(q)}`),
  listSources:   (projectId)         => api.get(`/outcome-dashboard/${projectId}/sources`),
  createSource:  (projectId, data)   => api.post(`/outcome-dashboard/${projectId}/sources`, data),
  updateSource:  (projectId, sid, d) => api.put(`/outcome-dashboard/${projectId}/sources/${sid}`, d),
  deleteSource:  (projectId, sid)    => api.delete(`/outcome-dashboard/${projectId}/sources/${sid}`),
  testSource:    (projectId, sid)    => api.post(`/outcome-dashboard/${projectId}/sources/${sid}/test`),
  getProdInputs: (projectId, scenario)        => api.get(`/outcome-dashboard/${projectId}/productivity-inputs?scenario=${scenario}`),
  previewProd:   (projectId, scenario, inputs)=> api.post(`/outcome-dashboard/${projectId}/productivity-preview?scenario=${scenario}`, inputs),
  saveProdInputs:(projectId, q, inputs)       => api.put(`/outcome-dashboard/${projectId}/productivity-inputs${ocq(q)}`, inputs),
  resetProdInputs:(projectId, scenario)       => api.delete(`/outcome-dashboard/${projectId}/productivity-inputs?scenario=${scenario}`),
  saveInferences:(projectId, scenario, perspective, inferences) =>
    api.put(`/outcome-dashboard/${projectId}/inferences?scenario=${scenario}&perspective=${perspective}`, { inferences }),
  resetInferences:(projectId, scenario, perspective) =>
    api.delete(`/outcome-dashboard/${projectId}/inferences?scenario=${scenario}&perspective=${perspective}`),
  getJcurveInputs:(projectId, scenario)         => api.get(`/outcome-dashboard/${projectId}/jcurve-inputs?scenario=${scenario}`),
  previewJcurve:  (projectId, scenario, inputs) => api.post(`/outcome-dashboard/${projectId}/jcurve-preview?scenario=${scenario}`, inputs),
  saveJcurve:     (projectId, q, inputs)        => api.put(`/outcome-dashboard/${projectId}/jcurve-inputs${ocq(q)}`, inputs),
  resetJcurve:    (projectId, scenario)         => api.delete(`/outcome-dashboard/${projectId}/jcurve-inputs?scenario=${scenario}`),
}

// ── Target State Studio ─────────────────────────────────────────────────────
export const targetStateApi = {
  getPlatforms: ()                  => api.get('/target-state/platforms'),
  getLadder:    ()                  => api.get('/target-state/ladder'),
  compare:      (risk)             => api.get(`/target-state/compare${risk ? `?risk_appetite=${risk}` : ''}`),
  getConfig:    (pid)              => api.get(`/target-state/${pid}`),
  saveConfig:   (pid, body)        => api.put(`/target-state/${pid}`, body),
  compose:      (pid, platform)    => api.post(`/target-state/${pid}/compose?platform=${platform}`),
  currentState: (pid)              => api.get(`/target-state/${pid}/current-state`),
  roadmap:      (pid, body)        => api.post(`/target-state/${pid}/roadmap`, body),
  progress:     (pid)              => api.get(`/target-state/${pid}/progress`),
  // WS6: Platform insights (agent catalog, architecture, tools, differentiators)
  allInsights:     ()              => api.get('/target-state/platform-insights/all'),
  platformInsight: (platformId)    => api.get(`/target-state/platform-insights/${platformId}`),
  // WS7: Dynamic ladder (L1-L5 × People/Process/Tools/Outcomes/Investment per platform kind)
  dynamicLadder:   (platformId)    => api.get(`/target-state/dynamic-ladder/${platformId}`),
}

// ── Settings ──────────────────────────────────────────────────────────────
export const settingsApi = {
  getStatus:       ()            => api.get('/settings/status'),
  getLLM:          ()            => api.get('/settings/llm'),
  saveLLM:         (data)        => api.post('/settings/llm', data),
  testLLM:         ()            => api.post('/settings/llm/test'),
  getALM:          ()            => api.get('/settings/alm'),
  saveALM:         (data)        => api.post('/settings/alm', data),
  testALM:         (tool)        => api.post(`/settings/alm/test?tool=${tool}`),
  getSchedule:     ()            => api.get('/settings/schedule'),
  saveSchedule:    (config, pid) => api.post(`/settings/schedule${pid ? `?project_id=${pid}` : ''}`, config),
  triggerPipeline: (projectId)   => api.post(`/settings/pipeline/trigger?project_id=${projectId}`),
}

// ── Project Data Sources (WS1) ───────────────────────────────────────────
export const dataSourcesApi = {
  getCatalog:    ()                    => api.get('/data-sources/catalog'),
  list:          (projectId)           => api.get(`/data-sources/${projectId}`),
  create:        (projectId, data)     => api.post(`/data-sources/${projectId}`, data),
  update:        (projectId, sid, d)   => api.patch(`/data-sources/${projectId}/${sid}`, d),
  remove:        (projectId, sid)      => api.delete(`/data-sources/${projectId}/${sid}`),
  test:          (projectId, sid)      => api.post(`/data-sources/${projectId}/${sid}/test`),
  sync:          (projectId, sid)      => api.post(`/data-sources/${projectId}/${sid}/sync`),
}

// ── Project Documents (WS2) ─────────────────────────────────────────────
export const documentsApi = {
  getCategories: ()                    => api.get('/documents/categories'),
  list:          (projectId)           => api.get(`/documents/${projectId}`),
  upload:        (projectId, formData) => api.post(`/documents/${projectId}`, formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  remove:        (projectId, docId)    => api.delete(`/documents/${projectId}/${docId}`),
}

// ── Manual Assessment (WS4) ─────────────────────────────────────────────
export const manualAssessmentApi = {
  getQuestions:   ()                                => api.get('/manual-assessment/questions'),
  getLevels:      ()                                => api.get('/manual-assessment/levels'),
  getResponses:   (projectId, params = {})          => api.get(`/manual-assessment/${projectId}/responses`, { params }),
  saveResponses:  (projectId, responses, ctx = {})  => api.post(`/manual-assessment/${projectId}/responses`, { responses, ...ctx }),
  getMaturity:    (projectId, params = {})           => api.get(`/manual-assessment/${projectId}/maturity`, { params }),
  listTeams:      (projectId)                       => api.get(`/manual-assessment/${projectId}/teams`),
  getDashboard:   (projectId)                       => api.get(`/manual-assessment/${projectId}/dashboard`),
  seedDemo:       (projectId)                       => api.post(`/manual-assessment/${projectId}/seed-demo`),
}

// ── Step Reviews / HITL (WS8) ───────────────────────────────────────────
export const stepReviewsApi = {
  getStepKeys:   ()                           => api.get('/step-reviews/steps'),
  listReviews:   (projectId)                  => api.get(`/step-reviews/${projectId}`),
  getReview:     (projectId, stepKey)         => api.get(`/step-reviews/${projectId}/${stepKey}`),
  upsertReview:  (projectId, stepKey, body)   => api.put(`/step-reviews/${projectId}/${stepKey}`, body),
}

// ── Health ────────────────────────────────────────────────────────────────
export const healthApi = {
  check: () => api.get('/health')
}

export default api
