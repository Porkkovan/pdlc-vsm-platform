import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { FUTURE_PHASE_MAP, getOptionTotals } from '../data/futureStatePhases'
import { agentsApi, targetStateApi } from '../services/api'
import ConfiguredFutureState from '../components/ConfiguredFutureState'
import { Link } from 'react-router-dom'
import { LANE_STYLE, PHASE_COLOR, TRANSFORMATION_ROADMAP } from '../data/transformationRoadmap'
import { STATIC_AGENT_CATALOG } from '../data/agentCatalog'
import TargetStateBanner from '../components/TargetStateBanner'
import StepReviewBar from '../components/StepReviewBar'
import InlineEditModal from '../components/common/InlineEditModal'

// Current state baseline (medium performer, feature level)
const CURRENT = { leadTime: 42.5, processTime: 100, waitTime: 536, flowEfficiency: 8.1, activities: 36 }
const CURRENT_STORY = { leadTime: 8.5, processTime: 40, waitTime: 130, flowEfficiency: 10.2, activities: 16 }

const TYPE_STYLE = {
  human:    { bg: 'bg-blue-50',   border: 'border-blue-200',   badge: 'bg-blue-100 text-blue-800',   icon: '👤', label: 'Human' },
  hybrid:   { bg: 'bg-violet-50', border: 'border-violet-200', badge: 'bg-violet-100 text-violet-800',icon: '🤝', label: 'Hybrid' },
  agent:    { bg: 'bg-green-50',  border: 'border-green-200',  badge: 'bg-green-100 text-green-800',  icon: '🤖', label: 'Agent' },
  oversight:{ bg: 'bg-cyan-50',  border: 'border-cyan-200',  badge: 'bg-cyan-100 text-cyan-800',  icon: '👁', label: 'Oversight' },
}

const SCENARIO_COLOR = {
  'option-a': { accent: 'blue',   ring: 'ring-blue-400',   bar: 'bg-blue-500',   badge: 'bg-blue-600' },
  'option-b': { accent: 'purple', ring: 'ring-purple-400', bar: 'bg-purple-500', badge: 'bg-purple-600' },
  'option-c': { accent: 'emerald',ring: 'ring-emerald-400',bar: 'bg-emerald-500',badge: 'bg-emerald-600' },
}

function PhaseCard({ phase, isOpen, onClick, scenarioId, isAdlc }) {
  const col = SCENARIO_COLOR[scenarioId]
  const fe = phase.flowEfficiency
  const feColor = fe >= 60 ? 'text-emerald-600' : fe >= 40 ? 'text-green-600' : fe >= 25 ? 'text-blue-600' : 'text-cyan-600'
  const feBg   = fe >= 60 ? 'bg-emerald-50' : fe >= 40 ? 'bg-green-50' : fe >= 25 ? 'bg-blue-50' : 'bg-cyan-50'

  return (
    <div
      className={`rounded-xl border-2 transition-all cursor-pointer select-none ${
        isOpen
          ? `border-${col.accent}-400 shadow-md`
          : `border-gray-200 hover:border-${col.accent}-300`
      } ${isAdlc ? 'bg-gradient-to-b from-emerald-50 to-white' : 'bg-white'}`}
      onClick={onClick}
    >
      <div className="p-3">
        <div className="flex items-center justify-between mb-2">
          <div className={`w-7 h-7 ${isAdlc ? 'bg-emerald-600' : `bg-${col.accent}-600`} text-white rounded-lg flex items-center justify-center font-bold text-xs`}>
            {phase.id}
          </div>
          {isAdlc && <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded font-bold">ADLC</span>}
        </div>
        <div className="font-semibold text-gray-800 text-xs leading-tight mb-0.5">{phase.name}</div>
        {phase.subtitle && <div className="text-xs text-gray-400 mb-2">{phase.subtitle}</div>}

        {/* FE bar */}
        <div className="mb-2">
          <div className="flex justify-between text-xs mb-0.5">
            <span className="text-gray-400">Flow Eff.</span>
            <span className={`font-bold ${feColor}`}>{fe.toFixed(0)}%</span>
          </div>
          <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div className={`h-full rounded-full ${col.bar}`} style={{ width: `${Math.min(fe, 100)}%` }} />
          </div>
        </div>

        <div className="flex gap-1 text-xs">
          <div className="flex-1 bg-gray-50 rounded p-1.5 text-center">
            <div className="text-gray-400 text-xs">PT</div>
            <div className="font-bold text-blue-600">{phase.processTime}h</div>
          </div>
          <div className="flex-1 bg-gray-50 rounded p-1.5 text-center">
            <div className="text-gray-400 text-xs">WT</div>
            <div className={`font-bold ${phase.waitTime <= 1 ? 'text-emerald-600' : 'text-cyan-600'}`}>{phase.waitTime}h</div>
          </div>
          <div className="flex-1 bg-gray-50 rounded p-1.5 text-center">
            <div className="text-gray-400 text-xs">Acts</div>
            <div className="font-bold text-gray-700">{phase.activityCount}</div>
          </div>
        </div>
      </div>
      <div className={`text-center text-xs py-1 border-t border-gray-100 text-gray-400 ${isOpen ? `text-${col.accent}-600 font-semibold` : ''}`}>
        {isOpen ? '▲ Hide Activities' : '▼ Show Activities'}
      </div>
    </div>
  )
}

function ActivityRow({ act, scenarioId, onEdit }) {
  const ts = TYPE_STYLE[act.type] || TYPE_STYLE.hybrid
  return (
    <div className={`rounded-lg border ${ts.bg} ${ts.border} p-3`}>
      <div className="flex items-start justify-between gap-2 mb-1">
        <div className="flex items-center gap-1.5 flex-1 min-w-0">
          <span className="text-base shrink-0">{ts.icon}</span>
          <div className="font-semibold text-gray-800 text-sm truncate">{act.name}</div>
          {onEdit && (
            <button onClick={() => onEdit(act)} className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold px-1 py-0.5 rounded hover:bg-indigo-50 shrink-0" title="Edit activity">
              ✏️
            </button>
          )}
        </div>
        <span className={`text-xs px-2 py-0.5 rounded font-bold shrink-0 ${ts.badge}`}>{ts.label}</span>
      </div>
      <div className="text-xs text-gray-500 mb-2">{act.role}</div>
      <p className="text-xs text-gray-600 mb-2 leading-relaxed">{act.desc}</p>
      <div className="flex flex-wrap gap-2 text-xs">
        <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-bold">
          PT: {act.processTime}h
        </span>
        <span className={`px-2 py-0.5 rounded font-bold ${act.waitTime === 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-cyan-50 text-cyan-700'}`}>
          WT: {act.waitTime}h {act.waitTime === 0 ? '✓ Zero wait' : ''}
        </span>
        {act.agent && (
          <span className="bg-violet-50 text-violet-700 px-2 py-0.5 rounded font-semibold">
            🤖 {act.agent}
          </span>
        )}
      </div>
    </div>
  )
}


const FS_ACTIVITY_EDIT_FIELDS = [
  { key: 'name', label: 'Activity Name', type: 'text' },
  { key: 'role', label: 'Role / Responsibility', type: 'text' },
  { key: 'desc', label: 'Description', type: 'textarea', rows: 3 },
  { key: 'processTime', label: 'Process Time (hrs)', type: 'number', min: 0, step: 0.5 },
  { key: 'waitTime', label: 'Wait Time (hrs)', type: 'number', min: 0, step: 0.5 },
  { key: 'type', label: 'Activity Type', type: 'select', options: ['human', 'hybrid', 'agent', 'oversight'] },
  { key: 'agent', label: 'Agent Name', type: 'text' },
]

export default function FutureStatePage() {
  const { activeScenario, setActiveScenario, addNotification, project, vsmLevel,
          analysisResult } = useApp()
  const [running, setRunning] = useState(false)
  const [openPhase, setOpenPhase] = useState(null)
  const [view, setView] = useState('visual') // 'visual' | 'table' | 'tools' | 'roadmap'
  const [rmPhaseIdx, setRmPhaseIdx] = useState(null)
  const [rmLane, setRmLane] = useState('all')
  const [editingAct, setEditingAct] = useState(null)
  const [actEdits, setActEdits] = useState({})

  const saveActEdit = (updated) => {
    setActEdits(prev => ({ ...prev, [updated.id]: updated }))
    addNotification(`Activity "${updated.name}" updated`, 'success')
  }

  // When a Target State is configured, the future state IS the interim/target steps
  // (replaces generic A/B/C). undefined = loading, null = none, object = configured.
  const [tsCfg, setTsCfg] = useState(undefined)
  useEffect(() => {
    if (!project?.id) { setTsCfg(null); return }
    const load = () => targetStateApi.getConfig(project.id)
      .then(d => setTsCfg(d && d.configured !== false ? d : null))
      .catch(() => setTsCfg(null))
    load()
    // Refresh when returning to the tab/page (e.g. after editing in the Studio).
    const onFocus = () => load()
    window.addEventListener('focus', onFocus)
    document.addEventListener('visibilitychange', onFocus)
    return () => { window.removeEventListener('focus', onFocus); document.removeEventListener('visibilitychange', onFocus) }
  }, [project?.id])

  if (tsCfg === undefined && project?.id) {
    return <div className="card card-body text-center text-gray-400 py-16">Loading future state…</div>
  }
  if (tsCfg) {
    return (
      <div className="space-y-6 fade-in">
        <TargetStateBanner />
        <ConfiguredFutureState cfg={tsCfg} />
      </div>
    )
  }

  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const phases   = FUTURE_PHASE_MAP[activeScenario] || FUTURE_PHASE_MAP['option-a']

  // Pull seeded future states from analysisResult when available
  const arFutureStates = analysisResult?.future_states || []
  const arScenario     = arFutureStates.find(s => s.scenario === activeScenario)
  const arMetrics      = analysisResult?.metrics || null
  const totals   = getOptionTotals(activeScenario)
  const isAdlc   = activeScenario === 'option-c'
  const base     = vsmLevel === 'user-story' ? CURRENT_STORY : CURRENT

  const col = SCENARIO_COLOR[activeScenario]

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runFutureStateDesign(project.id || 'demo', activeScenario)
      addNotification(`Future state design for ${scenario.label} complete!`, 'success')
    } catch {
      addNotification('Using built-in predictions (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  // User-story mode: filter to phases 3-6
  const visiblePhases = vsmLevel === 'user-story'
    ? phases.filter(p => p.id >= 3 && p.id <= 6)
    : phases

  // Lead time from activity data
  const displayLT = totals
    ? vsmLevel === 'user-story'
      ? +(totals.leadTime * 0.4).toFixed(1)
      : totals.leadTime
    : null

  // FE improvement vs current
  const feImprovement = totals
    ? +(((totals.flowEfficiency - base.flowEfficiency) / base.flowEfficiency) * 100).toFixed(0)
    : 0

  return (
    <div className="space-y-6 fade-in">
      <TargetStateBanner />

      {/* Header */}
      <div className={`bg-gradient-to-r ${isAdlc ? 'from-emerald-600 to-teal-700' : 'from-violet-400 to-violet-500'} rounded-2xl p-6 text-white shadow-lg`}>
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Future State VSM</h2>
            <p className="text-white/80">
              Three transformation scenarios — distinct activities, metrics and roles per option
              {isAdlc && ' · Option C uses ADLC (AI-Driven Lifecycle) with BMAD approach'}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex bg-white/20 rounded-lg overflow-hidden text-sm">
              <span className={`px-3 py-1.5 font-semibold cursor-default ${vsmLevel === 'feature' ? 'bg-white text-violet-700' : 'text-white'}`}>Feature</span>
              <span className={`px-3 py-1.5 font-semibold cursor-default ${vsmLevel === 'user-story' ? 'bg-white text-violet-700' : 'text-white'}`}>User Story</span>
            </div>
            <button onClick={runAgent} disabled={running}
              className="bg-white text-violet-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-violet-50 shadow">
              {running ? '⏳ Designing...' : '🤖 Run Future State Agent'}
            </button>
          </div>
        </div>
      </div>

      <StepReviewBar stepKey="future_state" stepLabel="Future State VSM" />

      {/* Scenario tabs */}
      <div className="grid grid-cols-3 gap-4">
        {FUTURE_STATE_SCENARIOS.map(s => {
          const t = getOptionTotals(s.id)
          const sc = SCENARIO_COLOR[s.id]
          const isC = s.id === 'option-c'
          return (
            <button
              key={s.id}
              onClick={() => { setActiveScenario(s.id); setOpenPhase(null); setRmPhaseIdx(null) }}
              className={`p-5 rounded-xl text-left border-2 transition-all ${
                activeScenario === s.id
                  ? `border-${sc.accent}-500 bg-${sc.accent}-50 shadow-md`
                  : 'border-gray-200 bg-white hover:border-gray-400'
              }`}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className={`${sc.badge} text-white px-2 py-0.5 rounded font-bold text-sm`}>{s.label}</span>
                <span className="text-xs text-gray-500">{s.automationLevel}% AI</span>
                {isC && <span className="text-xs bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded font-bold">ADLC</span>}
              </div>
              <div className="font-bold text-gray-800 text-sm">{s.title}</div>
              <div className="text-xs text-gray-500 mt-0.5 mb-3">{s.subtitle}</div>
              {t && (
                <div className="grid grid-cols-3 gap-1 text-xs">
                  <div>
                    <div className="text-gray-400">Act. FE</div>
                    <div className={`font-bold text-${sc.accent}-600`}>{t.flowEfficiency.toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-gray-400">PT</div>
                    <div className="font-bold text-blue-600">{t.processTime}h</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Activities</div>
                    <div className="font-bold text-gray-700">{t.totalActivities}</div>
                  </div>
                </div>
              )}
            </button>
          )
        })}
      </div>

      {/* View toggle */}
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold text-gray-700">
          {scenario?.label} — {isAdlc ? 'ADLC Phase Map' : 'Value Stream Map'}
          {totals && (
            <span className="ml-3 text-xs font-normal text-gray-400">
              {totals.totalActivities} activities · {totals.agentActivities} AI-automated · Activity FE: {totals.flowEfficiency.toFixed(0)}%
            </span>
          )}
        </div>
        <div className="flex bg-gray-100 rounded-lg overflow-hidden text-sm border border-gray-200">
          {[['visual','🗺 Phase Map'], ['table','📋 Activity Detail'], ['tools','⚙️ Tools & Agents'], ['roadmap','📅 Roadmap']].map(([v, l]) => (
            <button key={v} onClick={() => setView(v)}
              className={`px-3 py-1.5 font-semibold text-xs transition-colors ${view === v ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-200'}`}>
              {l}
            </button>
          ))}
        </div>
      </div>

      {/* ── VISUAL / PHASE MAP view ─────────────────────────────────────────── */}
      {view === 'visual' && (
        <div className="space-y-4">
          {/* Phase grid — clickable cards */}
          <div className={`grid gap-3 ${visiblePhases.length <= 4 ? 'grid-cols-4' : 'grid-cols-7'}`}>
            {visiblePhases.map((phase, i) => (
              <div key={phase.id}>
                {/* Connector arrow except first */}
                {i > 0 && (
                  <div className="hidden" />
                )}
                <PhaseCard
                  phase={phase}
                  isOpen={openPhase === phase.id}
                  onClick={() => setOpenPhase(openPhase === phase.id ? null : phase.id)}
                  scenarioId={activeScenario}
                  isAdlc={isAdlc && phase.adlcPhase}
                />
              </div>
            ))}
          </div>

          {/* Activity drill-down panel (visual view) */}
          {openPhase && (() => {
            const ph = visiblePhases.find(p => p.id === openPhase)
            if (!ph) return null
            return (
              <div className={`border-2 border-${col.accent}-200 rounded-xl overflow-hidden`}>
                <div className={`bg-${col.accent}-600 px-5 py-3 flex items-center justify-between`}>
                  <div>
                    <span className="text-white font-bold">Phase {ph.id}: {ph.name}</span>
                    {ph.subtitle && <span className="text-white/70 text-sm ml-3">{ph.subtitle}</span>}
                  </div>
                  <div className="flex gap-4 text-white/90 text-sm">
                    <span>PT: <strong>{ph.processTime}h</strong></span>
                    <span>WT: <strong>{ph.waitTime}h</strong></span>
                    <span>FE: <strong>{ph.flowEfficiency.toFixed(0)}%</strong></span>
                  </div>
                </div>
                <div className="p-4 bg-gray-50">
                  {/* Activity type legend */}
                  <div className="flex gap-3 text-xs mb-3 flex-wrap">
                    {Object.entries(TYPE_STYLE).map(([k, v]) => (
                      <span key={k} className={`px-2 py-0.5 rounded font-semibold ${v.badge}`}>{v.icon} {v.label}</span>
                    ))}
                    <span className="ml-auto text-gray-400 italic">{ph.activities.length} activities in this phase</span>
                  </div>
                  <div className="space-y-2">
                    {ph.activities.map(act => (
                      <ActivityRow key={act.id} act={actEdits[act.id] || act} scenarioId={activeScenario} onEdit={setEditingAct} />
                    ))}
                  </div>
                </div>
              </div>
            )
          })()}

          {/* Option C ADLC explanation banner */}
          {isAdlc && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
              <div className="flex items-start gap-3">
                <span className="text-2xl">🏗️</span>
                <div>
                  <div className="font-bold text-emerald-800 mb-1">ADLC: AI-Driven Lifecycle (BMAD Approach)</div>
                  <p className="text-sm text-emerald-700 mb-2">
                    Option C redesigns the PDLC as an AI-Driven Lifecycle. Inspired by the BMAD (Build, Measure, Automate, Deploy) methodology,
                    the 7 phases are renamed as AI capabilities, not human workflows. Only two human roles exist:
                  </p>
                  <div className="flex gap-4 text-sm">
                    <div className="bg-white rounded-lg p-3 border border-emerald-200 flex-1">
                      <div className="font-bold text-emerald-800">👤 Product Definer</div>
                      <div className="text-emerald-700 text-xs mt-1">Sets vision, OKRs, and strategic intent. The sole creative human input. All execution is agent-led.</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 border border-emerald-200 flex-1">
                      <div className="font-bold text-emerald-800">🔧 Product Builder</div>
                      <div className="text-emerald-700 text-xs mt-1">Supervises agent orchestration layer. Exception handling and production approval gate. ~20% of features require intervention.</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* All 3 scenarios comparison — uses analysisResult when available */}
          <div className="card card-body">
            <h3 className="font-bold text-gray-800 mb-4">All 3 Options — VSM Metrics Comparison</h3>
            <div className="grid grid-cols-4 gap-4">
              {/* Current state */}
              {(() => {
                const curFe = arMetrics?.flow_efficiency ?? base.flowEfficiency
                const curLt = arMetrics?.total_lt_days   ?? base.leadTime
                const curPt = arMetrics?.total_pt        ?? base.processTime
                const curWt = arMetrics?.total_wt        ?? base.waitTime
                return (
                  <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                    <div className="text-xs font-bold text-gray-500 uppercase mb-1">Current State</div>
                    {arMetrics && <div className="text-[10px] text-blue-500 mb-2">● Live data</div>}
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between"><span className="text-gray-500">Flow Efficiency</span><span className="font-bold text-sky-500">{curFe}%</span></div>
                      <div className="flex justify-between"><span className="text-gray-500">Lead Time</span><span className="font-bold text-gray-700">{curLt}d</span></div>
                      <div className="flex justify-between"><span className="text-gray-500">Process Time</span><span className="font-bold text-gray-700">{curPt}h</span></div>
                      <div className="flex justify-between"><span className="text-gray-500">Wait Time</span><span className="font-bold text-sky-500">{curWt}h</span></div>
                      <div className="flex justify-between"><span className="text-gray-500">Bottlenecks</span><span className="font-bold text-gray-700">{analysisResult?.bottlenecks?.length ?? base.activities} found</span></div>
                    </div>
                    <div className="mt-3 h-2 bg-gray-200 rounded-full"><div className="h-full bg-sky-400 rounded-full" style={{ width: `${Math.min(curFe, 100)}%` }} /></div>
                  </div>
                )
              })()}
              {FUTURE_STATE_SCENARIOS.map(s => {
                const t = getOptionTotals(s.id)
                const sc = SCENARIO_COLOR[s.id]
                // Prefer analysisResult future_states data for metrics
                const arFs = arFutureStates.find(f => f.scenario === s.id)
                const curFe = arMetrics?.flow_efficiency ?? base.flowEfficiency
                const curLt = arMetrics?.total_lt_days   ?? base.leadTime
                const displayFe  = arFs?.flow_efficiency   ?? t?.flowEfficiency
                const displayLt  = arFs?.total_lt_days     ?? t?.leadTime
                const displayPt  = t?.processTime
                const displayWt  = t?.waitTime
                const feGain = displayFe ? +(displayFe - curFe).toFixed(1) : 0
                const ltDrop = (displayLt && curLt) ? +(((curLt - displayLt) / curLt) * 100).toFixed(0) : 0
                return (
                  <button key={s.id}
                    onClick={() => { setActiveScenario(s.id); setOpenPhase(null); setRmPhaseIdx(null) }}
                    className={`text-left rounded-xl p-4 border-2 transition-all ${
                      activeScenario === s.id ? `border-${sc.accent}-400 bg-${sc.accent}-50` : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`${sc.badge} text-white px-2 py-0.5 rounded font-bold text-xs`}>{s.label}</span>
                      {s.id === 'option-c' && <span className="text-xs bg-emerald-100 text-emerald-700 px-1 py-0.5 rounded font-bold">ADLC</span>}
                    </div>
                    {(arFs || t) && (
                      <div className="space-y-2 text-sm">
                        {arFs && <div className="text-[10px] text-blue-500 mb-1">● Seeded data</div>}
                        <div className="flex justify-between"><span className="text-gray-500">Flow Efficiency</span><span className={`font-bold text-${sc.accent}-600`}>{displayFe ?? '—'}%</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Lead Time</span><span className="font-bold text-blue-600">{displayLt ?? t?.leadTime ?? '—'}d</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Process Time</span><span className="font-bold text-gray-700">{displayPt ?? '—'}h</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Wait Time</span><span className={`font-bold ${(displayWt ?? 999) < 10 ? 'text-emerald-600' : 'text-cyan-600'}`}>{displayWt ?? '—'}h</span></div>
                        {arFs && <div className="flex justify-between"><span className="text-gray-500">Tools / Agents</span><span className="font-bold text-gray-700">{arFs.tools_deployed || 0}T / {arFs.agents_deployed || 0}A</span></div>}
                        {arFs && <div className="flex justify-between"><span className="text-gray-500">Investment</span><span className="font-bold text-gray-700">{arFs.investment_range}</span></div>}
                      </div>
                    )}
                    {(arFs || t) && (
                      <div className="mt-3">
                        <div className={`h-2 bg-gray-100 rounded-full overflow-hidden`}>
                          <div className={`h-full ${sc.bar} rounded-full transition-all`} style={{ width: `${Math.min(displayFe ?? t?.flowEfficiency ?? 0, 100)}%` }} />
                        </div>
                        <div className="flex justify-between text-xs text-gray-400 mt-1">
                          <span>+{feGain}% FE gain</span>
                          <span>LT -{ltDrop}%</span>
                        </div>
                      </div>
                    )}
                  </button>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {/* ── TABLE / ACTIVITY DETAIL view ────────────────────────────────────── */}
      {view === 'table' && (
        <div className="space-y-3">
          {isAdlc && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-3 text-sm text-emerald-800">
              <strong>ADLC Mode:</strong> Phases renamed as AI capabilities. Human activities limited to strategic intent (Product Definer) and production oversight (Product Builder).
              Near-zero wait times — no human approval queues.
            </div>
          )}

          {visiblePhases.map(phase => {
            const isOpen = openPhase === phase.id
            const agentActs = phase.activities.filter(a => a.type === 'agent' || a.type === 'hybrid').length
            const humanActs = phase.activities.filter(a => a.type === 'human' || a.type === 'oversight').length
            return (
              <div key={phase.id} className="border border-gray-200 rounded-xl overflow-hidden">
                <button
                  onClick={() => setOpenPhase(isOpen ? null : phase.id)}
                  className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 ${isAdlc ? 'bg-emerald-600' : `bg-${col.accent}-600`} text-white rounded-lg flex items-center justify-center font-bold text-sm`}>{phase.id}</div>
                    <div className="text-left">
                      <div className="font-semibold text-gray-800 text-sm">{phase.name}</div>
                      <div className="text-xs text-gray-500">
                        {phase.subtitle} · {phase.activityCount} activities
                        <span className="ml-2 text-green-600">🤖 {agentActs} AI</span>
                        {humanActs > 0 && <span className="ml-1 text-blue-600">👤 {humanActs} human</span>}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-6 text-xs">
                    <div className="text-center">
                      <div className="text-gray-400 mb-0.5">Process Time</div>
                      <span className="font-bold text-blue-600">{phase.processTime}h</span>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-400 mb-0.5">Wait Time</div>
                      <span className={`font-bold ${phase.waitTime <= 1 ? 'text-emerald-600' : 'text-cyan-600'}`}>
                        {phase.waitTime}h {phase.waitTime === 0 ? '✓' : ''}
                      </span>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-400 mb-0.5">Flow Eff.</div>
                      <span className="font-bold text-purple-600">{phase.flowEfficiency.toFixed(0)}%</span>
                    </div>
                    <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                  </div>
                </button>

                {isOpen && (
                  <div className="px-5 pb-5 border-t border-gray-100">
                    <div className="mt-3 flex gap-2 text-xs mb-3 flex-wrap">
                      {Object.entries(TYPE_STYLE).map(([k, v]) => (
                        <span key={k} className={`px-2 py-0.5 rounded font-semibold ${v.badge}`}>{v.icon} {v.label}</span>
                      ))}
                    </div>
                    <div className="space-y-2">
                      {phase.activities.map(act => (
                        <ActivityRow key={act.id} act={actEdits[act.id] || act} scenarioId={activeScenario} onEdit={setEditingAct} />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          })}

          {/* Phase totals summary */}
          {totals && (
            <div className={`border-2 border-${col.accent}-200 rounded-xl p-4 bg-${col.accent}-50`}>
              <div className="font-bold text-gray-800 mb-3">{scenario?.label} — Total Metrics</div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-center">
                {[
                  { label: 'Total PT', value: `${totals.processTime}h`, color: 'text-blue-600' },
                  { label: 'Total WT', value: `${totals.waitTime}h`, color: isAdlc ? 'text-emerald-600' : 'text-cyan-600' },
                  { label: 'Activity FE', value: `${totals.flowEfficiency.toFixed(0)}%`, color: `text-${col.accent}-600` },
                  { label: 'Approx LT', value: `${totals.leadTime}d`, color: 'text-purple-600' },
                  { label: 'Activities', value: `${totals.agentActivities}/${totals.totalActivities} AI`, color: 'text-gray-700' },
                ].map(m => (
                  <div key={m.label} className="bg-white rounded-lg p-3 border border-gray-200">
                    <div className="text-xs text-gray-400 mb-1">{m.label}</div>
                    <div className={`font-bold text-lg ${m.color}`}>{m.value}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── Tools & Agents view — dedicated tab ──────────────────────────────── */}
      {view === 'tools' && (() => {
        const fs = arFutureStates.find(s => s.scenario === activeScenario)
        const catalog = STATIC_AGENT_CATALOG[activeScenario]

        // Option A: tool_deployment_map per phase
        if (activeScenario === 'option-a') {
          const phaseEntries = fs?.tool_deployment_map
            ? Object.entries(fs.tool_deployment_map)
            : Object.entries(catalog.byPhase).map(([ph, tools]) => [ph, tools])
          return (
            <div className="space-y-4">
              <div className="card">
                <div className="card-header">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-gray-800">Stage 1 — 16 AI Tools Deployment Map</h3>
                      <p className="text-xs text-gray-500">{fs?.tools_deployed || catalog.totalTools} GenAI tools embedded across all 7 PDLC phases · {catalog.humanModel}</p>
                    </div>
                    <div className="flex gap-2 items-center">
                      <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-bold">{fs?.tools_deployed || catalog.totalTools} Tools</span>
                      <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded font-semibold">Human-Led</span>
                    </div>
                  </div>
                </div>
                <div className="card-body p-0">
                  <table className="w-full text-xs">
                    <thead className="bg-blue-50 border-b border-blue-100">
                      <tr>
                        <th className="text-left px-4 py-2.5 font-semibold text-blue-700 w-40">PDLC Phase</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-blue-700">GenAI Tools to Configure &amp; Integrate (Stage 1)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {phaseEntries.map(([phase, tools], i) => (
                        <tr key={phase} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50/40'}>
                          <td className="px-4 py-2.5 font-semibold text-gray-700">{phase}</td>
                          <td className="px-4 py-2.5">
                            <div className="flex flex-wrap gap-1">
                              {tools.map(t => (
                                <span key={t} className="bg-blue-50 border border-blue-200 text-blue-700 px-2 py-0.5 rounded font-semibold">{t}</span>
                              ))}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {fs?.remaining_bottlenecks?.length > 0 && (
                    <div className="px-4 py-3 bg-cyan-50 border-t border-cyan-200 text-xs text-cyan-800">
                      <strong>Remaining bottlenecks after Stage 1 → justification for Stage 2:</strong>
                      <ul className="mt-1 space-y-0.5 list-disc list-inside">
                        {fs.remaining_bottlenecks.map(b => (
                          <li key={b.residual}><span className="font-semibold">Ph{b.phase_id}:</span> {b.residual} — <span className="italic">{b.metric_impact}</span></li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )
        }

        // Option B: 21 agents across phases
        if (activeScenario === 'option-b') {
          const phaseList = fs?.agents_by_phase
            ? Object.entries(fs.agents_by_phase)
            : Object.entries(catalog.byPhase).map(([ph, agents]) => [ph, agents.map(a => ({ agent: a.agent.replace('← ', ''), tool: a.tool, role: a.role }))])
          const llm = fs?.llm_layer || {}
          return (
            <div className="space-y-4">
              <div className="card">
                <div className="card-header">
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <div>
                      <h3 className="font-bold text-gray-800">Stage 2 — 21 Assistive Agents Across 7 PDLC Phases</h3>
                      <p className="text-xs text-gray-500">{catalog.humanModel}</p>
                    </div>
                    <div className="flex gap-2 flex-wrap">
                      <span className="bg-purple-600 text-white text-xs px-3 py-1 rounded-full font-bold">{fs?.agents_deployed || catalog.totalAgents} Agents</span>
                      {llm.primary && <span className="bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded font-semibold">{llm.primary}</span>}
                      {llm.primary && llm.protocol && <span className="bg-indigo-100 text-indigo-700 text-xs px-2 py-1 rounded font-semibold">{llm.protocol}</span>}
                      <span className="bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded font-semibold">LangGraph StateGraph</span>
                      <span className="bg-indigo-100 text-indigo-700 text-xs px-2 py-1 rounded font-semibold">MCP Protocol</span>
                    </div>
                  </div>
                </div>
                <div className="card-body p-0">
                  <div className="px-4 py-2 bg-purple-50 border-b border-purple-100 text-xs text-purple-700">
                    <span className="font-bold">← Arrow notation</span> = agent wraps the US Bank tool, invoked <span className="font-semibold">on-demand</span> by a human. Human: Oversee · Review · Approve at each step.
                  </div>
                  <table className="w-full text-xs">
                    <thead className="bg-purple-50 border-b border-purple-100">
                      <tr>
                        <th className="text-left px-4 py-2.5 font-semibold text-purple-700 w-40">PDLC Phase</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-purple-700">Agent</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-gray-600 w-20">Mode</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-gray-600">Tool (← wraps)</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-gray-600">Role — Human oversees each action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {phaseList.map(([phase, agents], pi) =>
                        agents.map((ag, ai) => (
                          <tr key={`${pi}-${ai}`} className={pi % 2 === 0 ? 'bg-white' : 'bg-purple-50/30'}>
                            {ai === 0 && (
                              <td className="px-4 py-2 font-semibold text-gray-700 align-top" rowSpan={agents.length}>{phase}</td>
                            )}
                            <td className="px-4 py-2">
                              <span className="bg-purple-50 border border-purple-200 text-purple-800 px-2 py-0.5 rounded font-bold">🤖 {ag.agent}</span>
                            </td>
                            <td className="px-4 py-2">
                              <span className="bg-teal-50 border border-teal-200 text-teal-700 px-1.5 py-0.5 rounded text-[10px] font-bold">Assistive</span>
                            </td>
                            <td className="px-4 py-2">
                              <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-mono">{ag.tool}</span>
                            </td>
                            <td className="px-4 py-2 text-gray-600">{ag.role}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                  {fs?.cross_agent_invocations?.length > 0 && (
                    <div className="px-4 py-3 bg-purple-50 border-t border-purple-100">
                      <div className="text-xs font-bold text-purple-700 mb-2">Cross-Agent Invocations via MCP Layer</div>
                      <div className="flex flex-wrap gap-1.5">
                        {fs.cross_agent_invocations.map(inv => (
                          <span key={inv} className="text-xs bg-white border border-purple-200 text-purple-700 px-2 py-0.5 rounded">{inv}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {fs?.remaining_bottlenecks?.length > 0 && (
                    <div className="px-4 py-3 bg-cyan-50 border-t border-cyan-200">
                      <div className="text-xs font-bold text-cyan-700 mb-1.5">Residual bottlenecks after Stage 2 → justification for Stage 3</div>
                      <div className="flex flex-col gap-1">
                        {fs.remaining_bottlenecks.map(b => (
                          <div key={b.residual} className="text-xs text-cyan-800">
                            <span className="font-semibold">Ph{b.phase_id}:</span> {b.residual} — <span className="italic">{b.detail?.slice(0,120)}…</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )
        }

        // Option C: STUMP Platform + all 21 agents (autonomous)
        if (activeScenario === 'option-c') {
          const platform = fs?.platform || {}
          const adlcFlow = fs?.adlc_flow || []
          const humanTouchpoints = fs?.human_touchpoints || []
          const regConsiderations = fs?.regulatory_considerations || []
          const phaseList = fs?.agents_by_phase
            ? Object.entries(fs.agents_by_phase)
            : Object.entries(catalog.byPhase).map(([ph, agents]) => [ph, agents.map(a => ({ agent: a.agent.replace('⚙ ', ''), tool: a.tool, role: a.role }))])
          return (
            <div className="space-y-4">
              {/* Platform stack */}
              <div className="card">
                <div className="card-header">
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <div>
                      <h3 className="font-bold text-gray-800">Stage 3 — {platform.name || 'STUMP Agentic Platform'} · 21 Agents Autonomous</h3>
                      <p className="text-xs text-gray-500">{platform.description || 'Orchestration layer for full ADLC — coordinates all 21 agents end-to-end'}</p>
                    </div>
                    <div className="flex gap-2 flex-wrap">
                      <span className="bg-emerald-600 text-white text-xs px-3 py-1 rounded-full font-bold">{fs?.agents_deployed || catalog.totalAgents} Agents</span>
                      <span className="bg-emerald-100 text-emerald-800 text-xs px-2 py-1 rounded font-semibold">AI-Native · ADLC</span>
                    </div>
                  </div>
                </div>
                <div className="card-body space-y-4">
                  {platform.components?.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-700 mb-2">Platform Stack (Stage 3 additions vs Stage 2 underlined)</div>
                      <div className="flex flex-wrap gap-2">
                        {platform.components.map((c, i) => (
                          <span key={c} className={`px-3 py-1 rounded font-semibold text-xs border ${i >= 2 ? 'bg-emerald-100 border-emerald-400 text-emerald-900 underline decoration-dotted' : 'bg-emerald-50 border-emerald-200 text-emerald-800'}`}>{c}</span>
                        ))}
                      </div>
                      <p className="text-xs text-gray-500 mt-1.5">Stage 2 had: GitHub Copilot + Azure OpenAI + MCP Layer &nbsp;|&nbsp; Stage 3 adds: LangChain + Agent Skills → full autonomous orchestration</p>
                      {platform.integration && <p className="text-xs text-gray-400 mt-0.5">Integrates with: {platform.integration}</p>}
                    </div>
                  )}
                  {adlcFlow.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-700 mb-2">ADLC End-to-End Pipeline Flow</div>
                      <div className="grid grid-cols-2 gap-1.5">
                        {adlcFlow.map((step, i) => (
                          <div key={i} className="flex items-start gap-2 text-xs">
                            <span className="w-5 h-5 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold shrink-0 text-[10px]">{i+1}</span>
                            <span className="text-gray-700">{step}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  <div className="grid grid-cols-2 gap-4">
                    {humanTouchpoints.length > 0 && (
                      <div>
                        <div className="text-xs font-bold text-gray-700 mb-2">Human Touchpoints Only (vs every step in Stage 2)</div>
                        <div className="flex flex-col gap-1">
                          {humanTouchpoints.map((t, i) => (
                            <div key={i} className="text-xs text-gray-600 flex items-start gap-1.5">
                              <span className="text-emerald-500 shrink-0">✓</span>{t}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {regConsiderations.length > 0 && (
                      <div>
                        <div className="text-xs font-bold text-gray-700 mb-2">Regulatory Hard Stops (cannot be automated)</div>
                        <div className="flex flex-col gap-1">
                          {regConsiderations.map((r, i) => (
                            <div key={i} className="text-xs text-cyan-700 flex items-start gap-1.5">
                              <span className="text-cyan-500 shrink-0">⚠</span>{r}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              {/* All 21 agents — autonomous mode */}
              {(
                <div className="card">
                  <div className="card-header">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-bold text-gray-800">All 21 Agents — Autonomous Mode on STUMP Platform</h3>
                        <p className="text-xs text-gray-500">Same agents as Stage 2, now orchestrated end-to-end by STUMP Platform. Human: Intent · Review · Approve Only.</p>
                      </div>
                      <span className="bg-emerald-600 text-white text-xs px-3 py-1 rounded-full font-bold">21 Agents · Full Autonomy</span>
                    </div>
                  </div>
                  <div className="card-body p-0">
                    <div className="px-4 py-2 bg-emerald-50 border-b border-emerald-100 text-xs text-emerald-800">
                      <span className="font-bold">⚙ Gear notation</span> = agent is <span className="font-semibold">platform-managed</span> — STUMP orchestrates it continuously without human triggers. Human: Provide Intent · Approve Only.
                    </div>
                    <table className="w-full text-xs">
                      <thead className="bg-emerald-50 border-b border-emerald-100">
                        <tr>
                          <th className="text-left px-4 py-2.5 font-semibold text-emerald-700 w-40">ADLC Phase</th>
                          <th className="text-left px-4 py-2.5 font-semibold text-emerald-700">Agent</th>
                          <th className="text-left px-4 py-2.5 font-semibold text-gray-600 w-20">Mode</th>
                          <th className="text-left px-4 py-2.5 font-semibold text-gray-600">Tool (⚙ platform-managed)</th>
                          <th className="text-left px-4 py-2.5 font-semibold text-gray-600">Role — Platform orchestrates autonomously</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {phaseList.map(([phase, agents], pi) =>
                          agents.map((ag, ai) => (
                            <tr key={`${pi}-${ai}`} className={pi % 2 === 0 ? 'bg-white' : 'bg-emerald-50/20'}>
                              {ai === 0 && (
                                <td className="px-4 py-2 font-semibold text-gray-700 align-top" rowSpan={agents.length}>{phase}</td>
                              )}
                              <td className="px-4 py-2">
                                <span className="bg-emerald-50 border border-emerald-300 text-emerald-900 px-2 py-0.5 rounded font-bold">🤖 {ag.agent}</span>
                              </td>
                              <td className="px-4 py-2">
                                <span className="bg-emerald-600 text-white px-1.5 py-0.5 rounded text-[10px] font-bold">Autonomous</span>
                              </td>
                              <td className="px-4 py-2">
                                <span className="bg-teal-50 text-teal-700 px-2 py-0.5 rounded font-mono text-[11px]">{ag.tool}</span>
                              </td>
                              <td className="px-4 py-2 text-gray-600">{ag.role}</td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                    {fs?.addressed_from_stage2?.length > 0 && (
                      <div className="px-4 py-3 bg-emerald-50 border-t border-emerald-100">
                        <div className="text-xs font-bold text-emerald-700 mb-2">Stage 2 residuals addressed by STUMP Platform</div>
                        <div className="flex flex-col gap-1">
                          {fs.addressed_from_stage2.map((a, i) => (
                            <div key={i} className="text-xs text-emerald-800">
                              <span className="font-semibold">{a.bottleneck}</span> → {a.platform_capability}: <span className="italic">{a.outcome}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )
        }

        return null
      })()}

      {/* ── Transformation Roadmap view ───────────────────────────────────────── */}
      {view === 'roadmap' && (() => {
        const rm = TRANSFORMATION_ROADMAP[activeScenario]
        if (!rm) return null
        const lanes = Object.keys(LANE_STYLE)
        const openPhaseIdx = rmPhaseIdx
        const setOpenPhaseIdx = setRmPhaseIdx
        const activeLane = rmLane
        const setActiveLane = setRmLane

        return (
          <div className="space-y-4">
            {/* Header banner */}
            <div className={`bg-gradient-to-r ${isAdlc ? 'from-emerald-600 to-teal-700' : 'from-violet-400 to-violet-500'} rounded-2xl p-5 text-white`}>
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h3 className="font-bold text-xl mb-1">Transformation Roadmap — {scenario?.label}</h3>
                  <p className="text-sm opacity-90">{rm.humanModel}</p>
                </div>
                <div className="flex gap-3 flex-wrap">
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Duration</div>
                    <div className="font-bold">{rm.duration}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Phases</div>
                    <div className="font-bold">{rm.phases.length}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Swim Lanes</div>
                    <div className="font-bold">5</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Lane filter */}
            <div className="flex gap-2 flex-wrap">
              <button onClick={() => setActiveLane('all')}
                className={`px-3 py-1 rounded-full text-xs font-semibold border transition-all ${activeLane === 'all' ? 'bg-gray-700 text-white border-gray-700' : 'bg-white text-gray-600 border-gray-300 hover:border-gray-500'}`}>
                All Lanes
              </button>
              {lanes.map(l => {
                const s = LANE_STYLE[l]
                return (
                  <button key={l} onClick={() => setActiveLane(activeLane === l ? 'all' : l)}
                    className={`px-3 py-1 rounded-full text-xs font-semibold border transition-all ${activeLane === l ? `${s.badge} text-white border-transparent` : `bg-white ${s.text} ${s.border} hover:${s.bg}`}`}>
                    {s.label}
                  </button>
                )
              })}
            </div>

            {/* Summary strip — all phases */}
            <div className={`grid gap-1`} style={{ gridTemplateColumns: `repeat(${rm.phases.length}, 1fr)` }}>
              {rm.phases.map((ph, i) => {
                const clr = PHASE_COLOR[ph.color] || 'bg-gray-500'
                const isOpen = openPhaseIdx === i
                return (
                  <button key={i} onClick={() => setOpenPhaseIdx(isOpen ? null : i)}
                    className={`rounded-lg p-2 text-left border-2 transition-all ${isOpen ? 'border-gray-400 shadow-md' : 'border-gray-200 hover:border-gray-300'} bg-white`}>
                    <div className={`${clr} text-white text-xs font-bold px-2 py-0.5 rounded-full mb-1.5 inline-block`}>{ph.range}</div>
                    <div className="font-semibold text-gray-800 text-xs leading-tight">{ph.name}</div>
                    <div className="flex gap-0.5 mt-1.5 flex-wrap">
                      {lanes.filter(l => ph[l]?.length > 0).map(l => (
                        <span key={l} className={`w-2 h-2 rounded-full ${LANE_STYLE[l].dot}`} title={LANE_STYLE[l].label} />
                      ))}
                    </div>
                  </button>
                )
              })}
            </div>

            {/* Expanded phase swim-lane view */}
            {openPhaseIdx !== null && (() => {
              const ph = rm.phases[openPhaseIdx]
              const visibleLanes = activeLane === 'all' ? lanes : [activeLane]
              return (
                <div className="border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
                  <div className={`${PHASE_COLOR[ph.color] || 'bg-gray-600'} px-5 py-3 flex items-center justify-between`}>
                    <div>
                      <span className="font-bold text-white text-base">{ph.range} — {ph.name}</span>
                      <span className="ml-3 text-white/70 text-xs">
                        {lanes.reduce((n, l) => n + (ph[l]?.length || 0), 0)} activities across {lanes.filter(l => ph[l]?.length > 0).length} lanes
                      </span>
                    </div>
                    <button onClick={() => setOpenPhaseIdx(null)} className="text-white/70 hover:text-white text-sm">✕ Close</button>
                  </div>
                  <div className="bg-white divide-y divide-gray-100">
                    {visibleLanes.map(lane => {
                      const items = ph[lane] || []
                      if (items.length === 0) return null
                      const ls = LANE_STYLE[lane]
                      return (
                        <div key={lane} className={`px-5 py-4 ${ls.bg}`}>
                          <div className={`flex items-center gap-2 mb-3`}>
                            <span className={`${ls.badge} text-white text-xs font-bold px-3 py-0.5 rounded-full`}>{ls.label}</span>
                            <span className="text-xs text-gray-500">{items.length} actions</span>
                          </div>
                          <div className="space-y-2">
                            {items.map((item, ii) => (
                              <div key={ii} className={`flex items-start gap-3 bg-white border ${ls.border} rounded-lg px-3 py-2.5`}>
                                <span className={`${ls.badge} text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5`}>{ii + 1}</span>
                                <span className="text-sm text-gray-700">{item}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })()}

            {/* Full swim-lane Gantt table */}
            <div className="card overflow-hidden">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Full Swim-Lane Roadmap</h3>
                <p className="text-xs text-gray-500">Click any cell to expand · {activeLane === 'all' ? 'Showing all lanes' : `Filtered: ${LANE_STYLE[activeLane]?.label}`}</p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-xs border-collapse min-w-max">
                  <thead>
                    <tr>
                      <th className="text-left px-3 py-2 bg-gray-50 border border-gray-200 font-semibold text-gray-600 w-36 sticky left-0 z-10">Lane</th>
                      {rm.phases.map((ph, i) => {
                        const clr = PHASE_COLOR[ph.color] || 'bg-gray-500'
                        return (
                          <th key={i} className="px-3 py-2 bg-gray-50 border border-gray-200 text-center" style={{ minWidth: '140px' }}>
                            <div className={`${clr} text-white px-2 py-0.5 rounded-full font-bold inline-block mb-0.5`}>{ph.range}</div>
                            <div className="font-semibold text-gray-700 text-xs">{ph.name}</div>
                          </th>
                        )
                      })}
                    </tr>
                  </thead>
                  <tbody>
                    {(activeLane === 'all' ? lanes : [activeLane]).map(lane => {
                      const ls = LANE_STYLE[lane]
                      const hasAny = rm.phases.some(ph => (ph[lane] || []).length > 0)
                      if (!hasAny) return null
                      return (
                        <tr key={lane} className="align-top">
                          <td className={`px-3 py-3 border border-gray-200 font-semibold ${ls.text} ${ls.bg} sticky left-0`}>
                            {ls.label}
                          </td>
                          {rm.phases.map((ph, pi) => {
                            const items = ph[lane] || []
                            return (
                              <td key={pi} className={`px-2 py-2 border border-gray-200 ${ls.bg} align-top`}>
                                {items.length === 0 ? (
                                  <div className="text-gray-300 text-center py-2">—</div>
                                ) : (
                                  <ul className="space-y-1">
                                    {items.map((item, ii) => (
                                      <li key={ii} className={`flex items-start gap-1.5 bg-white border ${ls.border} rounded px-2 py-1.5`}>
                                        <span className={`${ls.dot} w-1.5 h-1.5 rounded-full shrink-0 mt-1`} />
                                        <span className="text-gray-700 leading-snug">{item}</span>
                                      </li>
                                    ))}
                                  </ul>
                                )}
                              </td>
                            )
                          })}
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* CTA to full business case */}
            <div className="bg-cyan-50 border border-cyan-200 rounded-xl p-4 flex items-center justify-between gap-4">
              <div>
                <div className="font-semibold text-cyan-800 text-sm">Detailed how-to, examples & success criteria</div>
                <div className="text-xs text-cyan-700">Each activity above has step-by-step guidance, config examples, and measurable outcomes in the Business Case module.</div>
              </div>
              <Link to="/business-case" className="shrink-0 bg-cyan-600 hover:bg-cyan-700 text-white text-xs font-bold px-4 py-2 rounded-lg whitespace-nowrap">
                💼 Open Business Case →
              </Link>
            </div>
          </div>
        )
      })()}

      {/* Scenario description + roles */}
      {scenario && (
        <div className="card">
          <div className="card-body">
            <div className="flex items-start gap-4 flex-wrap">
              <div className="flex-1">
                <h3 className="font-bold text-gray-800 text-lg mb-1">{scenario.title}</h3>
                <p className="text-gray-600 text-sm mb-4">{scenario.description}</p>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-xs font-semibold text-gray-700 mb-2">Human Roles ({scenario.humanRoles.length})</h4>
                    <div className="flex flex-wrap gap-1">
                      {scenario.humanRoles.map(r => (
                        <span key={r} className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded text-xs font-semibold">{r}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-gray-700 mb-2">
                      AI Agents ({activeScenario === 'option-a' ? '3–5 core' : '13 — full suite'})
                    </h4>
                    <div className="flex flex-wrap gap-1">
                      {scenario.aiAgents.slice(0, 10).map(a => (
                        <span key={a} className="tag-agent text-xs">{a}</span>
                      ))}
                      {scenario.aiAgents.length > 10 && (
                        <span className="text-xs text-gray-500">+{scenario.aiAgents.length - 10} more</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex gap-4">
        <Link to="/business-case" className="btn-primary flex-1 text-center py-3">💼 View Business Case →</Link>
        <Link to="/improvements"  className="btn-secondary flex-1 text-center py-3">← Improvements</Link>
      </div>

      <InlineEditModal
        item={editingAct}
        fields={FS_ACTIVITY_EDIT_FIELDS}
        title={editingAct ? `Edit Activity: ${editingAct.name}` : 'Edit Activity'}
        onSave={saveActEdit}
        onClose={() => setEditingAct(null)}
      />

      {Object.keys(actEdits).length > 0 && (
        <div className="fixed bottom-4 right-4 bg-violet-600 text-white px-4 py-2 rounded-lg shadow-lg text-xs font-semibold z-40">
          ✏️ {Object.keys(actEdits).length} activit{Object.keys(actEdits).length !== 1 ? 'ies' : 'y'} edited (session)
        </div>
      )}
    </div>
  )
}
