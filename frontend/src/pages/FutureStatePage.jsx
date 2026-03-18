import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { FUTURE_PHASE_MAP, getOptionTotals } from '../data/futureStatePhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

// Current state baseline (medium performer, feature level)
const CURRENT = { leadTime: 42.5, processTime: 100, waitTime: 536, flowEfficiency: 8.1, activities: 36 }
const CURRENT_STORY = { leadTime: 8.5, processTime: 40, waitTime: 130, flowEfficiency: 10.2, activities: 16 }

const TYPE_STYLE = {
  human:    { bg: 'bg-blue-50',   border: 'border-blue-200',   badge: 'bg-blue-100 text-blue-800',   icon: '👤', label: 'Human' },
  hybrid:   { bg: 'bg-violet-50', border: 'border-violet-200', badge: 'bg-violet-100 text-violet-800',icon: '🤝', label: 'Hybrid' },
  agent:    { bg: 'bg-green-50',  border: 'border-green-200',  badge: 'bg-green-100 text-green-800',  icon: '🤖', label: 'Agent' },
  oversight:{ bg: 'bg-amber-50',  border: 'border-amber-200',  badge: 'bg-amber-100 text-amber-800',  icon: '👁', label: 'Oversight' },
}

const SCENARIO_COLOR = {
  'option-a': { accent: 'blue',   ring: 'ring-blue-400',   bar: 'bg-blue-500',   badge: 'bg-blue-600' },
  'option-b': { accent: 'purple', ring: 'ring-purple-400', bar: 'bg-purple-500', badge: 'bg-purple-600' },
  'option-c': { accent: 'emerald',ring: 'ring-emerald-400',bar: 'bg-emerald-500',badge: 'bg-emerald-600' },
}

function PhaseCard({ phase, isOpen, onClick, scenarioId, isAdlc }) {
  const col = SCENARIO_COLOR[scenarioId]
  const fe = phase.flowEfficiency
  const feColor = fe >= 60 ? 'text-emerald-600' : fe >= 40 ? 'text-green-600' : fe >= 25 ? 'text-blue-600' : 'text-amber-600'
  const feBg   = fe >= 60 ? 'bg-emerald-50' : fe >= 40 ? 'bg-green-50' : fe >= 25 ? 'bg-blue-50' : 'bg-amber-50'

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
            <div className={`font-bold ${phase.waitTime <= 1 ? 'text-emerald-600' : 'text-amber-600'}`}>{phase.waitTime}h</div>
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

function ActivityRow({ act, scenarioId }) {
  const ts = TYPE_STYLE[act.type] || TYPE_STYLE.hybrid
  return (
    <div className={`rounded-lg border ${ts.bg} ${ts.border} p-3`}>
      <div className="flex items-start justify-between gap-2 mb-1">
        <div className="flex items-center gap-1.5 flex-1 min-w-0">
          <span className="text-base shrink-0">{ts.icon}</span>
          <div className="font-semibold text-gray-800 text-sm truncate">{act.name}</div>
        </div>
        <span className={`text-xs px-2 py-0.5 rounded font-bold shrink-0 ${ts.badge}`}>{ts.label}</span>
      </div>
      <div className="text-xs text-gray-500 mb-2">{act.role}</div>
      <p className="text-xs text-gray-600 mb-2 leading-relaxed">{act.desc}</p>
      <div className="flex flex-wrap gap-2 text-xs">
        <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-bold">
          PT: {act.processTime}h
        </span>
        <span className={`px-2 py-0.5 rounded font-bold ${act.waitTime === 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
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

export default function FutureStatePage() {
  const { activeScenario, setActiveScenario, addNotification, project, vsmLevel } = useApp()
  const [running, setRunning] = useState(false)
  const [openPhase, setOpenPhase] = useState(null)
  const [view, setView] = useState('visual') // 'visual' | 'table'

  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const phases   = FUTURE_PHASE_MAP[activeScenario] || FUTURE_PHASE_MAP['option-a']
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

      {/* Header */}
      <div className={`bg-gradient-to-r ${isAdlc ? 'from-emerald-600 to-teal-700' : 'from-violet-600 to-purple-700'} rounded-2xl p-6 text-white shadow-lg`}>
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

      {/* Scenario tabs */}
      <div className="grid grid-cols-3 gap-4">
        {FUTURE_STATE_SCENARIOS.map(s => {
          const t = getOptionTotals(s.id)
          const sc = SCENARIO_COLOR[s.id]
          const isC = s.id === 'option-c'
          return (
            <button
              key={s.id}
              onClick={() => { setActiveScenario(s.id); setOpenPhase(null) }}
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
          {[['visual','🗺 Phase Map'], ['table','📋 Activity Detail']].map(([v, l]) => (
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
                      <ActivityRow key={act.id} act={act} scenarioId={activeScenario} />
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

          {/* All 3 scenarios comparison */}
          <div className="card card-body">
            <h3 className="font-bold text-gray-800 mb-4">All 3 Options — Activity-Level Comparison</h3>
            <div className="grid grid-cols-4 gap-4">
              {/* Current state */}
              <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                <div className="text-xs font-bold text-gray-500 uppercase mb-2">Current State</div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between"><span className="text-gray-500">Flow Efficiency</span><span className="font-bold text-red-500">{base.flowEfficiency}%</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Lead Time</span><span className="font-bold text-gray-700">{base.leadTime}d</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Process Time</span><span className="font-bold text-gray-700">{base.processTime}h</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Wait Time</span><span className="font-bold text-red-500">{base.waitTime}h</span></div>
                  <div className="flex justify-between"><span className="text-gray-500">Activities</span><span className="font-bold text-gray-700">{base.activities}</span></div>
                </div>
                <div className="mt-3 h-2 bg-gray-200 rounded-full"><div className="h-full bg-red-400 rounded-full" style={{ width: `${base.flowEfficiency}%` }} /></div>
              </div>
              {FUTURE_STATE_SCENARIOS.map(s => {
                const t = getOptionTotals(s.id)
                const sc = SCENARIO_COLOR[s.id]
                const feGain = t ? +(t.flowEfficiency - base.flowEfficiency).toFixed(1) : 0
                const ltDrop = t ? +(((base.leadTime - t.leadTime) / base.leadTime) * 100).toFixed(0) : 0
                return (
                  <button key={s.id}
                    onClick={() => { setActiveScenario(s.id); setOpenPhase(null) }}
                    className={`text-left rounded-xl p-4 border-2 transition-all ${
                      activeScenario === s.id ? `border-${sc.accent}-400 bg-${sc.accent}-50` : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`${sc.badge} text-white px-2 py-0.5 rounded font-bold text-xs`}>{s.label}</span>
                      {s.id === 'option-c' && <span className="text-xs bg-emerald-100 text-emerald-700 px-1 py-0.5 rounded font-bold">ADLC</span>}
                    </div>
                    {t && (
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between"><span className="text-gray-500">Flow Efficiency</span><span className={`font-bold text-${sc.accent}-600`}>{t.flowEfficiency.toFixed(0)}%</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Lead Time</span><span className="font-bold text-blue-600">{t.leadTime}d</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Process Time</span><span className="font-bold text-gray-700">{t.processTime}h</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Wait Time</span><span className={`font-bold ${t.waitTime < 10 ? 'text-emerald-600' : 'text-amber-600'}`}>{t.waitTime}h</span></div>
                        <div className="flex justify-between"><span className="text-gray-500">Activities</span><span className="font-bold text-gray-700">{t.totalActivities}</span></div>
                      </div>
                    )}
                    {t && (
                      <div className="mt-3">
                        <div className={`h-2 bg-gray-100 rounded-full overflow-hidden`}>
                          <div className={`h-full ${sc.bar} rounded-full transition-all`} style={{ width: `${Math.min(t.flowEfficiency, 100)}%` }} />
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
                      <span className={`font-bold ${phase.waitTime <= 1 ? 'text-emerald-600' : 'text-amber-600'}`}>
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
                        <ActivityRow key={act.id} act={act} scenarioId={activeScenario} />
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
                  { label: 'Total WT', value: `${totals.waitTime}h`, color: isAdlc ? 'text-emerald-600' : 'text-amber-600' },
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
                    <h4 className="text-xs font-semibold text-gray-700 mb-2">AI Agents ({scenario.aiAgents.length})</h4>
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
    </div>
  )
}
