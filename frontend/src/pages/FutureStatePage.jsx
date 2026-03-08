import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES, FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'
import VSMVisualFlow from '../components/vsm/VSMVisualFlow'

// Feature-level base metrics (all 7 phases)
const FEATURE_METRICS = { leadTime: 42.5, processTime: 100, waitTime: 536, flowEfficiency: 8.1 }
// User-story-level base metrics (phases 3–6 only, ~40% of feature scale)
const STORY_METRICS   = { leadTime: 8.5,  processTime: 40,  waitTime: 130,  flowEfficiency: 10.2 }

// Phases relevant to user story cycle (3–6)
const STORY_PHASES = new Set([3, 4, 5, 6])

export default function FutureStatePage() {
  const { activeScenario, setActiveScenario, addNotification, project, vsmLevel } = useApp()
  const [running, setRunning]   = useState(false)
  const [openPhase, setOpenPhase] = useState(null)
  const [futureView, setFutureView] = useState('visual') // 'visual' | 'table'

  const scenario    = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const baseMetrics = vsmLevel === 'user-story' ? STORY_METRICS : FEATURE_METRICS

  const futureMetrics = {
    leadTime:      +(baseMetrics.leadTime * (1 - scenario.expectedImprovements.leadTime / 100)).toFixed(1),
    processTime:   +(baseMetrics.processTime * (1 - scenario.expectedImprovements.effort / 100)).toFixed(0),
    waitTime:      +(baseMetrics.waitTime * (1 - scenario.expectedImprovements.leadTime / 100 * 1.4)).toFixed(0),
    flowEfficiency:+(baseMetrics.flowEfficiency * (1 + scenario.expectedImprovements.flowEfficiency / 100)).toFixed(1)
  }

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runFutureStateDesign(project.id || 'demo', activeScenario)
      addNotification(`Future state design for ${scenario.label} complete!`, 'success')
    } catch {
      addNotification('Using built-in predictions (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  // For a given activity: compute current PT/WT and future PT/WT
  const getActivityMetrics = (activity) => {
    const agentMap = {
      'option-a': { automationPct: 40 },
      'option-b': { automationPct: 65 },
      'option-c': { automationPct: 85 }
    }
    const cfg = agentMap[activeScenario]
    const isAgentActivity = scenario.aiAgents.includes(activity.agent)
    const scale  = vsmLevel === 'user-story' ? 0.4 : 1.0
    const ptFactor = isAgentActivity ? (1 - cfg.automationPct / 100 * 0.9) : 0.9
    const wtFactor = isAgentActivity ? (1 - cfg.automationPct / 100 * 0.85) : 0.7

    // Wait times: activity.defaultWait is in days → convert to hours (* 8)
    const currentPT = +((activity.defaultEffort.min + activity.defaultEffort.max) / 2 * scale).toFixed(1)
    const currentWT = +((activity.defaultWait.min + activity.defaultWait.max) / 2 * 8 * scale).toFixed(1)
    const futurePT  = +(currentPT * ptFactor).toFixed(1)
    const futureWT  = +(currentWT * wtFactor).toFixed(1)
    const ptDelta   = currentPT > 0 ? Math.round((1 - futurePT / currentPT) * 100) : 0
    const wtDelta   = currentWT > 0 ? Math.round((1 - futureWT / currentWT) * 100) : 0

    return { currentPT, currentWT, futurePT, futureWT, ptDelta, wtDelta, automated: isAgentActivity, agent: isAgentActivity ? activity.agent : null }
  }

  const visiblePhases = vsmLevel === 'user-story'
    ? PDLC_PHASES.filter(p => STORY_PHASES.has(p.id))
    : PDLC_PHASES

  // Build visual flow phases for the active scenario
  const buildVisualPhases = (scen) => {
    const cfg = { 'option-a': 40, 'option-b': 65, 'option-c': 85 }
    const automationPct = cfg[scen.id] || 40
    const scale = vsmLevel === 'user-story' ? 0.4 : 1.0
    return visiblePhases.map(phase => {
      const isAI = scen.aiAgents.some(ag =>
        phase.activities.some(act => act.agent === ag)
      )
      const ptFactor = isAI ? (1 - automationPct / 100 * 0.9) : 0.9
      const wtFactor = isAI ? (1 - automationPct / 100 * 0.85) : 0.7
      const currPT = phase.activities.reduce((s, a) => s + (a.defaultEffort.min + a.defaultEffort.max) / 2 * scale, 0)
      const currWT = phase.activities.reduce((s, a) => s + (a.defaultWait.min  + a.defaultWait.max)  / 2 * 8 * scale, 0)
      const futurePT = +(currPT * ptFactor).toFixed(1)
      const futureWT = +(currWT * wtFactor).toFixed(1)
      const futFE = (futurePT + futureWT) > 0 ? futurePT / (futurePT + futureWT) * 100 : 0
      const aiAgent = isAI
        ? (scen.aiAgents.find(ag => phase.activities.some(act => act.agent === ag)) || null)
        : null
      return {
        id: phase.id, name: phase.name,
        processTime: futurePT, waitTime: futureWT,
        currPT, currWT,
        isBottleneck: futFE < 20,
        aiAgent,
      }
    })
  }

  const currentVisualPhases = visiblePhases.map(phase => {
    const scale = vsmLevel === 'user-story' ? 0.4 : 1.0
    const pt = phase.activities.reduce((s, a) => s + (a.defaultEffort.min + a.defaultEffort.max) / 2 * scale, 0)
    const wt = phase.activities.reduce((s, a) => s + (a.defaultWait.min  + a.defaultWait.max)  / 2 * 8 * scale, 0)
    const fe = (pt + wt) > 0 ? pt / (pt + wt) * 100 : 0
    return { id: phase.id, name: phase.name, processTime: pt, waitTime: wt, isBottleneck: fe < 30 }
  })

  const currentTotalPT = currentVisualPhases.reduce((s, p) => s + p.processTime, 0)
  const currentTotalWT = currentVisualPhases.reduce((s, p) => s + p.waitTime, 0)
  const currentFE = (currentTotalPT / (currentTotalPT + currentTotalWT) * 100).toFixed(1)

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-violet-600 to-purple-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Future State VSM</h2>
            <p className="text-violet-100">
              Three transformation scenarios — {vsmLevel === 'user-story' ? 'User Story level (Phases 3–6)' : 'Feature level (All 7 phases)'}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {/* Level indicator */}
            <div className="flex bg-white/20 rounded-lg overflow-hidden text-sm">
              <span className={`px-3 py-1.5 font-semibold cursor-default ${vsmLevel === 'feature' ? 'bg-white text-violet-700' : 'text-white'}`}>Feature</span>
              <span className={`px-3 py-1.5 font-semibold cursor-default ${vsmLevel === 'user-story' ? 'bg-white text-violet-700' : 'text-white'}`}>User Story</span>
            </div>
            <button onClick={runAgent} disabled={running} className="bg-white text-violet-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-violet-50 shadow">
              {running ? '⏳ Designing...' : '🤖 Run Future State Agent'}
            </button>
          </div>
        </div>
      </div>

      {/* Scenario tabs — now with PT reduction */}
      <div className="grid grid-cols-3 gap-4">
        {FUTURE_STATE_SCENARIOS.map(s => (
          <button
            key={s.id}
            onClick={() => setActiveScenario(s.id)}
            className={`p-5 rounded-xl text-left border-2 transition-all ${
              activeScenario === s.id
                ? 'border-violet-500 bg-violet-50 shadow-md'
                : 'border-gray-200 bg-white hover:border-gray-400'
            }`}
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-violet-600 text-white px-2 py-0.5 rounded font-bold text-sm">{s.label}</span>
              <span className="text-xs text-gray-500">{s.automationLevel}% AI</span>
            </div>
            <div className="font-bold text-gray-800 text-sm">{s.title}</div>
            <div className="text-xs text-gray-500 mt-1 mb-3">{s.subtitle}</div>
            <div className="grid grid-cols-3 gap-1 text-xs">
              <div><div className="text-gray-400">LT</div><div className="font-bold text-green-600">-{s.expectedImprovements.leadTime}%</div></div>
              <div><div className="text-gray-400">PT</div><div className="font-bold text-blue-600">-{s.expectedImprovements.effort}%</div></div>
              <div><div className="text-gray-400">FE</div><div className="font-bold text-purple-600">+{s.expectedImprovements.flowEfficiency}%</div></div>
            </div>
          </button>
        ))}
      </div>

      {/* Visual Flow toggle */}
      {scenario && (
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-gray-700">
            {scenario.label} — Value Stream Map Visualization
          </div>
          <div className="flex bg-gray-100 rounded-lg overflow-hidden text-sm border border-gray-200">
            {[['visual','🗺 Visual Flow'],['table','📋 Phase Table']].map(([v,l]) => (
              <button key={v} onClick={() => setFutureView(v)}
                className={`px-3 py-1.5 font-semibold text-xs transition-colors ${futureView===v ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-200'}`}>
                {l}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Current State Visual (reference) */}
      {scenario && futureView === 'visual' && (
        <div>
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 pl-1">
            Current State (Baseline)
          </div>
          <VSMVisualFlow
            mode="current"
            phases={currentVisualPhases}
            totalPT={currentTotalPT}
            totalWT={currentTotalWT}
            flowEfficiency={currentFE}
          />
        </div>
      )}

      {/* Future State Visual — active scenario */}
      {scenario && futureView === 'visual' && (() => {
        const fPhases = buildVisualPhases(scenario)
        const fTotalPT = fPhases.reduce((s, p) => s + p.processTime, 0)
        const fTotalWT = fPhases.reduce((s, p) => s + p.waitTime, 0)
        const fFE = (fTotalPT / (fTotalPT + fTotalWT) * 100).toFixed(1)
        return (
          <div>
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 pl-1">
              {scenario.label} — {scenario.title}
            </div>
            <VSMVisualFlow
              mode="future"
              scenarioLabel={`${scenario.label} · ${scenario.automationLevel}% AI Automation`}
              phases={fPhases}
              totalPT={fTotalPT}
              totalWT={fTotalWT}
              flowEfficiency={fFE}
            />
          </div>
        )
      })()}

      {/* All 3 scenarios side-by-side summary when in visual mode */}
      {scenario && futureView === 'visual' && (
        <div className="card card-body">
          <h3 className="font-bold text-gray-800 mb-4">All 3 Future State Options — Flow Efficiency Comparison</h3>
          <div className="grid grid-cols-3 gap-4">
            {FUTURE_STATE_SCENARIOS.map(scen => {
              const fp = buildVisualPhases(scen)
              const fpt = fp.reduce((s, p) => s + p.processTime, 0)
              const fwt = fp.reduce((s, p) => s + p.waitTime, 0)
              const ffe = (fpt / (fpt + fwt) * 100).toFixed(1)
              const flt = ((fpt + fwt) / 8).toFixed(1)
              const aiCount = fp.filter(p => p.aiAgent).length
              return (
                <button
                  key={scen.id}
                  onClick={() => setActiveScenario(scen.id)}
                  className={`text-left rounded-xl p-4 border-2 transition-all ${
                    activeScenario === scen.id
                      ? 'border-violet-500 bg-violet-50'
                      : 'border-gray-200 bg-gray-50 hover:border-violet-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <span className="bg-violet-600 text-white px-2 py-0.5 rounded font-bold text-sm">{scen.label}</span>
                    <span className="text-xs text-gray-500">{scen.automationLevel}% AI</span>
                  </div>
                  <div className="space-y-1.5 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Flow Efficiency</span>
                      <span className="font-bold text-green-600">{ffe}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Lead Time</span>
                      <span className="font-bold text-blue-600">{flt}d</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">AI-Automated Phases</span>
                      <span className="font-bold text-purple-600">{aiCount}/{fp.length}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">FE vs Current</span>
                      <span className="font-bold text-emerald-600">+{(parseFloat(ffe) - parseFloat(currentFE)).toFixed(1)}%</span>
                    </div>
                  </div>
                  {/* Mini FE bar */}
                  <div className="mt-3">
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-violet-500 to-green-500 rounded-full"
                        style={{ width: `${Math.min(parseFloat(ffe), 100)}%` }} />
                    </div>
                    <div className="flex justify-between text-xs text-gray-400 mt-0.5">
                      <span>0%</span><span>100%</span>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>
        </div>
      )}

      {/* Scenario detail */}
      {scenario && (
        <>
          {/* Description */}
          <div className="card">
            <div className="card-body">
              <div className="flex items-start gap-4">
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
                        {scenario.aiAgents.slice(0, 8).map(a => (
                          <span key={a} className="tag-agent text-xs">{a}</span>
                        ))}
                        {scenario.aiAgents.length > 8 && (
                          <span className="text-xs text-gray-500">+{scenario.aiAgents.length - 8} more</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Metrics comparison — Current vs Future */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Predicted Metrics — Current vs {scenario.label}</h3>
              <p className="text-xs text-gray-500">{vsmLevel === 'user-story' ? 'User Story level baseline (Phases 3–6)' : 'Feature level baseline (All 7 phases)'}</p>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Lead Time', current: `${baseMetrics.leadTime}d`, future: `${futureMetrics.leadTime}d`, pct: scenario.expectedImprovements.leadTime, arrow: '▼', color: 'green' },
                  { label: 'Process Time', current: `${baseMetrics.processTime}h`, future: `${futureMetrics.processTime}h`, pct: scenario.expectedImprovements.effort, arrow: '▼', color: 'blue' },
                  { label: 'Wait Time', current: `${baseMetrics.waitTime}h`, future: `${futureMetrics.waitTime}h`, pct: Math.round(scenario.expectedImprovements.leadTime * 1.2), arrow: '▼', color: 'orange' },
                  { label: 'Flow Efficiency', current: `${baseMetrics.flowEfficiency}%`, future: `${Math.min(futureMetrics.flowEfficiency, 85).toFixed(1)}%`, pct: scenario.expectedImprovements.flowEfficiency, arrow: '▲', color: 'purple' }
                ].map(m => (
                  <div key={m.label} className="border border-gray-200 rounded-xl p-4 text-center">
                    <div className="text-xs text-gray-500 mb-3 font-semibold">{m.label}</div>
                    <div className="grid grid-cols-2 gap-2 mb-2">
                      <div className="bg-gray-50 rounded-lg p-2">
                        <div className="text-xs text-gray-400 mb-0.5">Current</div>
                        <div className="font-bold text-gray-700 text-sm">{m.current}</div>
                      </div>
                      <div className={`bg-${m.color}-50 rounded-lg p-2`}>
                        <div className="text-xs text-gray-400 mb-0.5">Future</div>
                        <div className={`font-bold text-${m.color}-600 text-sm`}>{m.future}</div>
                      </div>
                    </div>
                    <div className={`text-xs font-bold text-${m.color}-600`}>
                      {m.arrow} {m.pct}% {m.arrow === '▼' ? 'reduction' : 'improvement'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* User story notice if applicable */}
          {vsmLevel === 'user-story' && (
            <div className="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 text-sm text-blue-800">
              <span className="font-bold">User Story mode:</span> Showing Phases 3–6 (Code Management → Continuous Delivery). Phases 1–2 are planning prerequisites and not included in story cycle time. Switch to Feature level on the Dashboard to see the full PDLC.
            </div>
          )}

          {/* Future VSM by phase — with current vs future PT/WT */}
          {futureView === 'table' && <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Future State Value Stream — Phase by Phase</h3>
              <p className="text-xs text-gray-500">Current PT/WT shown alongside predicted future values for each phase and activity</p>
            </div>
            <div className="card-body space-y-3">
              {visiblePhases.map(phase => {
                const isOpen = openPhase === phase.id
                const phaseActivities = phase.activities.map(a => ({
                  ...a, m: getActivityMetrics(a)
                }))
                const currPT = phaseActivities.reduce((s, a) => s + a.m.currentPT, 0)
                const currWT = phaseActivities.reduce((s, a) => s + a.m.currentWT, 0)
                const futPT  = phaseActivities.reduce((s, a) => s + a.m.futurePT, 0)
                const futWT  = phaseActivities.reduce((s, a) => s + a.m.futureWT, 0)
                const ptDelta = currPT > 0 ? Math.round((1 - futPT / currPT) * 100) : 0
                const wtDelta = currWT > 0 ? Math.round((1 - futWT / currWT) * 100) : 0
                const automatedCount = phaseActivities.filter(a => a.m.automated).length

                return (
                  <div key={phase.id} className="border border-gray-200 rounded-xl overflow-hidden">
                    <button
                      onClick={() => setOpenPhase(isOpen ? null : phase.id)}
                      className="w-full flex items-center justify-between px-5 py-3.5 hover:bg-gray-50"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-violet-600 text-white rounded-lg flex items-center justify-center font-bold text-sm">{phase.id}</div>
                        <div className="text-left">
                          <div className="font-semibold text-gray-800 text-sm">{phase.name}</div>
                          <div className="text-xs text-gray-500">{automatedCount}/{phase.activities.length} activities AI-automated</div>
                        </div>
                      </div>
                      {/* Phase-level current vs future metrics */}
                      <div className="flex items-center gap-5 text-xs">
                        <div className="text-center">
                          <div className="text-gray-400 mb-0.5">Process Time</div>
                          <div className="flex items-center gap-1.5">
                            <span className="text-gray-600 font-semibold">{currPT.toFixed(0)}h</span>
                            <span className="text-gray-400">→</span>
                            <span className="font-bold text-blue-600">{futPT.toFixed(0)}h</span>
                            <span className="bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded font-bold text-xs">-{ptDelta}%</span>
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-gray-400 mb-0.5">Wait Time</div>
                          <div className="flex items-center gap-1.5">
                            <span className="text-gray-600 font-semibold">{currWT.toFixed(0)}h</span>
                            <span className="text-gray-400">→</span>
                            <span className="font-bold text-green-600">{futWT.toFixed(0)}h</span>
                            <span className="bg-green-100 text-green-700 px-1.5 py-0.5 rounded font-bold text-xs">-{wtDelta}%</span>
                          </div>
                        </div>
                        <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                      </div>
                    </button>

                    {isOpen && (
                      <div className="px-5 pb-5 border-t border-gray-100 slide-down">
                        {/* Activity header row */}
                        <div className="mt-3 grid grid-cols-12 gap-2 px-3 py-1.5 text-xs text-gray-400 font-semibold bg-gray-50 rounded-lg">
                          <div className="col-span-4">Activity</div>
                          <div className="col-span-2 text-center">Current PT</div>
                          <div className="col-span-2 text-center">Future PT</div>
                          <div className="col-span-2 text-center">Current WT</div>
                          <div className="col-span-2 text-center">Future WT</div>
                        </div>
                        <div className="mt-1.5 space-y-1.5">
                          {phaseActivities.map(act => (
                            <div key={act.id} className={`rounded-lg px-3 py-2.5 border text-xs grid grid-cols-12 gap-2 items-center ${
                              act.m.automated ? 'bg-violet-50 border-violet-200' : 'bg-gray-50 border-gray-200'
                            }`}>
                              <div className="col-span-4">
                                <div className="font-semibold text-gray-800">{act.name}</div>
                                {act.m.automated && <span className="tag-agent text-xs mt-0.5">{act.m.agent}</span>}
                              </div>
                              {/* Current PT */}
                              <div className="col-span-2 text-center">
                                <span className="font-semibold text-gray-600">{act.m.currentPT}h</span>
                              </div>
                              {/* Future PT with delta */}
                              <div className="col-span-2 text-center">
                                <span className="font-bold text-blue-600">{act.m.futurePT}h</span>
                                {act.m.ptDelta > 0 && (
                                  <div className="text-xs text-blue-500">-{act.m.ptDelta}%</div>
                                )}
                              </div>
                              {/* Current WT */}
                              <div className="col-span-2 text-center">
                                <span className="font-semibold text-gray-600">{act.m.currentWT}h</span>
                              </div>
                              {/* Future WT with delta */}
                              <div className="col-span-2 text-center">
                                <span className="font-bold text-green-600">{act.m.futureWT}h</span>
                                {act.m.wtDelta > 0 && (
                                  <div className="text-xs text-green-500">-{act.m.wtDelta}%</div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>}
        </>
      )}

      <div className="flex gap-4">
        <Link to="/business-case" className="btn-primary flex-1 text-center py-3">💼 View Business Case →</Link>
        <Link to="/improvements"  className="btn-secondary flex-1 text-center py-3">← Improvements</Link>
      </div>
    </div>
  )
}
