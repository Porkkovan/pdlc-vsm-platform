import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Target, ChevronRight } from 'lucide-react'
import { useApp } from '../contexts/AppContext'
import { targetStateApi } from '../services/api'

const PLATFORM_LABEL = {
  homegrown: 'Home-grown', bmad: 'BMAD', copilot_workspace: 'Copilot Workspace',
  devin: 'Devin', cursor: 'Cursor', flowsource: 'Cognizant Flowsource',
}

/**
 * Shows the saved Target State (platform + target/interim levels) when configured,
 * linking to the Target State Studio. Renders nothing when no target state is set
 * (graceful fallback — the host page keeps its default A/B/C behaviour).
 */
export default function TargetStateBanner() {
  const { project } = useApp()
  const [cfg, setCfg] = useState(null)

  useEffect(() => {
    if (!project?.id) return
    targetStateApi.getConfig(project.id)
      .then(d => setCfg(d && d.configured !== false ? d : null))
      .catch(() => setCfg(null))
  }, [project?.id])

  if (!cfg) return null
  const levels = cfg.interim_levels || []
  const path = levels.length
    ? `L${cfg.current_level} → ${levels.map(l => `L${l}`).join(' → ')}`
    : `L${cfg.current_level} → L${cfg.target_level}`

  return (
    <Link to="/target-state"
      className="flex items-center justify-between gap-3 rounded-xl border border-sky-600/20 bg-gradient-to-r from-sky-600/5 to-emerald-50/40 px-4 py-2.5 hover:border-sky-600/40 transition-colors">
      <div className="flex items-center gap-2 text-sm">
        <Target size={16} className="text-sky-800" />
        <span className="font-semibold text-sky-800">Target State:</span>
        <span className="text-gray-600">{PLATFORM_LABEL[cfg.platform] || cfg.platform}</span>
        <span className="text-gray-300">·</span>
        <span className="text-gray-600">{path}</span>
        <span className="text-gray-300">·</span>
        <span className="text-gray-500">{(cfg.interim_count || 0) === 0 ? 'one go' : `${cfg.interim_count} interim${cfg.interim_count > 1 ? 's' : ''}`}</span>
      </div>
      <span className="text-xs font-semibold text-sky-800 flex items-center shrink-0">Open Studio <ChevronRight size={14} /></span>
    </Link>
  )
}
