import { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { projectsApi, vsmApi, agentsApi } from '../services/api'

const AppContext = createContext(null)

const LS_KEY = 'pdlc_active_project_id'   // session hint only — no project data stored locally

const DEFAULT_PROJECT = {
  id: null,
  name: '',
  organization: '',
  industry: '',
  portfolios: [],
  productGroups: [],
  portfolio: '',
  productGroup: '',
  product: '',
  team: '',
  almTool: null,
  almConfig: {},
  createdAt: null,
}

// All fields now come fully from Postgres — no localOverride merge needed
function mapProjectFromApi(p) {
  return {
    id:            p.id,
    name:          p.name          || '',
    organization:  p.organization  || '',
    industry:      p.industry      || '',
    portfolios:    p.portfolios    || [],
    productGroups: p.product_groups || [],
    portfolio:     p.portfolio     || '',
    productGroup:  p.product_group || '',
    product:       p.product       || '',
    team:          p.team          || '',
    almTool:       p.alm_tool      || null,
    almConfig:     p.alm_config    || {},
    createdAt:     p.created_at    || null,
  }
}

export function AppProvider({ children }) {
  const [project, setProject]               = useState(DEFAULT_PROJECT)
  const [savedProjects, setSavedProjects]   = useState([])
  const [vsmData, setVsmData]               = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [agentStatus, setAgentStatus]       = useState({})
  const [activeScenario, setActiveScenario] = useState('option-a')
  const [customOverrides, setCustomOverrides] = useState({})
  const [notifications, setNotifications]   = useState([])
  const [vsmLevel, setVsmLevel]             = useState('feature')
  const [doraMetrics, setDoraMetrics]       = useState(null)
  const [doraProfile, setDoraProfile]       = useState(null)

  // ── Auto-load VSM snapshot + analysis result for a project ID ─────────────
  const loadProjectData = useCallback(async (projectId) => {
    if (!projectId) return
    try {
      const vsm = await vsmApi.get(projectId)
      setVsmData(vsm?.vsm_data || null)
    } catch {}
    try {
      const result = await agentsApi.getAnalysisResult(projectId)
      setAnalysisResult(result)
    } catch {}
  }, [])

  // ── Restore last session from Postgres on mount ───────────────────────────
  useEffect(() => {
    projectsApi.list().then(list => {
      setSavedProjects(list)
      const lastId = localStorage.getItem(LS_KEY)
      if (lastId) {
        const found = list.find(p => p.id === lastId)
        if (found) {
          setProject(mapProjectFromApi(found))
          loadProjectData(found.id)
        }
      }
    }).catch(() => {
      // Backend unreachable — start with empty project
    })
  }, [loadProjectData])

  // ── Persist active project ID (session hint only) ─────────────────────────
  useEffect(() => {
    if (project.id) {
      localStorage.setItem(LS_KEY, project.id)
    }
  }, [project.id])

  const addNotification = useCallback((msg, type = 'info') => {
    const id = Date.now()
    setNotifications(n => [...n, { id, msg, type }])
    setTimeout(() => setNotifications(n => n.filter(x => x.id !== id)), 5000)
  }, [])

  const updateAgentStatus = useCallback((agentId, status, result = null) => {
    setAgentStatus(prev => ({ ...prev, [agentId]: { status, result, updatedAt: Date.now() } }))
  }, [])

  // ── Save or update project — all fields persisted to Postgres ────────────
  const saveProject = useCallback(async (data) => {
    const payload = {
      name:           data.name || data.organization || data.team || 'My Project',
      organization:   data.organization   || null,
      portfolio:      data.portfolio      || null,
      product_group:  data.productGroup   || null,
      product:        data.product        || null,
      team:           data.team           || null,
      industry:       data.industry       || null,
      portfolios:     data.portfolios     || [],
      product_groups: data.productGroups  || [],
      alm_tool:       data.almTool        || null,
      alm_config:     data.almConfig      || {},
    }
    try {
      const saved = data.id
        ? await projectsApi.update(data.id, payload)
        : await projectsApi.create(payload)
      const mapped = mapProjectFromApi(saved)
      setProject(mapped)
      setSavedProjects(prev => {
        const idx = prev.findIndex(p => p.id === saved.id)
        if (idx >= 0) { const u = [...prev]; u[idx] = saved; return u }
        return [saved, ...prev]
      })
      return mapped
    } catch {
      // Offline fallback — keep in-memory state, no persistence
      const withId = data.id ? data : { ...data, id: `local-${Date.now()}` }
      setProject(withId)
      return withId
    }
  }, [])

  // ── Switch active project ────────────────────────────────────────────────
  const switchProject = useCallback(async (projectId) => {
    if (!projectId) {
      setProject(DEFAULT_PROJECT)
      setVsmData(null)
      setAnalysisResult(null)
      setAgentStatus({})
      setCustomOverrides({})
      localStorage.removeItem(LS_KEY)
      return
    }
    try {
      const p = await projectsApi.get(projectId)
      setProject(mapProjectFromApi(p))
      setVsmData(null)
      setAnalysisResult(null)
      setAgentStatus({})
      setCustomOverrides({})
      loadProjectData(projectId)
    } catch {
      const found = savedProjects.find(p => p.id === projectId)
      if (found) {
        setProject(mapProjectFromApi(found))
        loadProjectData(projectId)
      }
    }
  }, [savedProjects, loadProjectData])

  // ── Reload project list ───────────────────────────────────────────────────
  const refreshProjects = useCallback(async () => {
    try {
      const list = await projectsApi.list()
      setSavedProjects(list)
      return list
    } catch { return [] }
  }, [])

  const resetProject = useCallback(() => {
    setProject(DEFAULT_PROJECT)
    setVsmData(null)
    setAnalysisResult(null)
    setAgentStatus({})
    setCustomOverrides({})
    localStorage.removeItem(LS_KEY)
  }, [])

  return (
    <AppContext.Provider value={{
      project, setProject,
      savedProjects, setSavedProjects,
      vsmData, setVsmData,
      analysisResult, setAnalysisResult,
      agentStatus, updateAgentStatus,
      activeScenario, setActiveScenario,
      customOverrides, setCustomOverrides,
      notifications, addNotification,
      resetProject,
      saveProject,
      switchProject,
      refreshProjects,
      vsmLevel, setVsmLevel,
      doraMetrics, setDoraMetrics,
      doraProfile, setDoraProfile,
      pdlcPhases: PDLC_PHASES,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}
