import { createContext, useContext, useState, useCallback } from 'react'
import { PDLC_PHASES } from '../data/pdlcPhases'

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

export function AppProvider({ children }) {
  const [project, setProject]           = useState(DEFAULT_PROJECT)
  const [vsmData, setVsmData]           = useState(null)        // current state VSM (from ALM or manual)
  const [analysisResult, setAnalysisResult] = useState(null)   // agent analysis result
  const [agentStatus, setAgentStatus]   = useState({})          // per-agent run status
  const [activeScenario, setActiveScenario] = useState('option-a')
  const [customOverrides, setCustomOverrides] = useState({})    // activity-level overrides
  const [notifications, setNotifications] = useState([])
  const [vsmLevel, setVsmLevel]         = useState('feature')   // 'feature' | 'user-story'

  const addNotification = useCallback((msg, type = 'info') => {
    const id = Date.now()
    setNotifications(n => [...n, { id, msg, type }])
    setTimeout(() => setNotifications(n => n.filter(x => x.id !== id)), 5000)
  }, [])

  const updateAgentStatus = useCallback((agentId, status, result = null) => {
    setAgentStatus(prev => ({ ...prev, [agentId]: { status, result, updatedAt: Date.now() } }))
  }, [])

  const resetProject = useCallback(() => {
    setProject(DEFAULT_PROJECT)
    setVsmData(null)
    setAnalysisResult(null)
    setAgentStatus({})
    setCustomOverrides({})
  }, [])

  return (
    <AppContext.Provider value={{
      project, setProject,
      vsmData, setVsmData,
      analysisResult, setAnalysisResult,
      agentStatus, updateAgentStatus,
      activeScenario, setActiveScenario,
      customOverrides, setCustomOverrides,
      notifications, addNotification,
      resetProject,
      vsmLevel, setVsmLevel,
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
