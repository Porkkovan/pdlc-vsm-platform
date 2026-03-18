import { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { projectsApi } from '../services/api'

const AppContext = createContext(null)

const DEFAULT_PROJECT = {
  id: null,
  name: '',
  organization: '',
  portfolio: '',
  productGroup: '',
  team: '',
  almTool: null,
  almConfig: {},
  createdAt: null
}

// Map backend snake_case fields → frontend camelCase
function mapProjectFromApi(p) {
  return {
    id:           p.id,
    name:         p.name || '',
    organization: p.organization || '',
    portfolio:    p.portfolio || '',
    productGroup: p.product_group || '',
    team:         p.team || '',
    almTool:      p.alm_tool || null,
    almConfig:    p.alm_config || {},
    createdAt:    p.created_at || null
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

  // ── Load projects list from backend on mount ──────────────────────────────
  useEffect(() => {
    projectsApi.list().then(list => {
      setSavedProjects(list)
      // Restore last-used project from localStorage
      const lastId = localStorage.getItem('pdlc_active_project_id')
      if (lastId) {
        const found = list.find(p => p.id === lastId)
        if (found) setProject(mapProjectFromApi(found))
      }
    }).catch(() => {
      // Backend not available — try localStorage fallback
      const saved = localStorage.getItem('pdlc_project')
      if (saved) {
        try { setProject(JSON.parse(saved)) } catch { /* ignore */ }
      }
    })
  }, [])

  // ── Persist active project ID to localStorage whenever it changes ─────────
  useEffect(() => {
    if (project.id) {
      localStorage.setItem('pdlc_active_project_id', project.id)
      localStorage.setItem('pdlc_project', JSON.stringify(project))
    }
  }, [project])

  const addNotification = useCallback((msg, type = 'info') => {
    const id = Date.now()
    setNotifications(n => [...n, { id, msg, type }])
    setTimeout(() => setNotifications(n => n.filter(x => x.id !== id)), 5000)
  }, [])

  const updateAgentStatus = useCallback((agentId, status, result = null) => {
    setAgentStatus(prev => ({ ...prev, [agentId]: { status, result, updatedAt: Date.now() } }))
  }, [])

  // ── Save or update project in backend ────────────────────────────────────
  const saveProject = useCallback(async (data) => {
    const payload = {
      name:          data.name || data.organization || data.team || 'My Project',
      organization:  data.organization || null,
      portfolio:     data.portfolio || null,
      product_group: data.productGroup || null,
      team:          data.team || null,
      industry:      data.industry || null
    }
    try {
      let saved
      if (data.id) {
        saved = await projectsApi.update(data.id, payload)
      } else {
        saved = await projectsApi.create(payload)
      }
      const mapped = mapProjectFromApi(saved)
      setProject(mapped)
      setSavedProjects(prev => {
        const idx = prev.findIndex(p => p.id === saved.id)
        if (idx >= 0) {
          const updated = [...prev]
          updated[idx] = saved
          return updated
        }
        return [saved, ...prev]
      })
      return mapped
    } catch {
      // Offline — update local state only
      const withId = data.id ? data : { ...data, id: `local-${Date.now()}` }
      setProject(withId)
      return withId
    }
  }, [])

  // ── Switch active project (load from backend by id) ───────────────────────
  const switchProject = useCallback(async (projectId) => {
    if (!projectId) {
      setProject(DEFAULT_PROJECT)
      setVsmData(null)
      setAnalysisResult(null)
      setAgentStatus({})
      setCustomOverrides({})
      localStorage.removeItem('pdlc_active_project_id')
      return
    }
    try {
      const p = await projectsApi.get(projectId)
      setProject(mapProjectFromApi(p))
      setVsmData(null)
      setAnalysisResult(null)
      setAgentStatus({})
      setCustomOverrides({})
    } catch {
      const found = savedProjects.find(p => p.id === projectId)
      if (found) setProject(mapProjectFromApi(found))
    }
  }, [savedProjects])

  // ── Reload saved projects list ────────────────────────────────────────────
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
    localStorage.removeItem('pdlc_active_project_id')
    localStorage.removeItem('pdlc_project')
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
      pdlcPhases: PDLC_PHASES
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
