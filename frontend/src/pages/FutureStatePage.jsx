import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES, FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

const BASE_METRICS = { leadTime: 42.5, processTime: 100, waitTime: 536, flowEfficiency: 8.1 }

export default function FutureStatePage() {
  const { activeScenario, setActiveScenario, vsmData, addNotification, project } = useApp()
  const [running, setRunning]   = useState(false)
  const [openPhase, setOpenPhase] = useState(null)

  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)

  const futureMetrics = {
    leadTime:      +(BASE_METRICS.leadTime * (1 - scenario.expectedImprovements.leadTime / 100)).toFixed(1),
    processTime:   +(BASE_METRICS.processTime * (1 - scenario.expectedImprovements.effort / 100)).toFixed(0),
    waitTime:      +(BASE_METRICS.waitTime * (1 - scenario.expectedImprovements.leadTime / 100 * 1.4)).toFixed(0),
    flowEfficiency:+(BASE_METRICS.flowEfficiency * (1 + scenario.expectedImprovements.flowEfficiency / 100)).toFixed(1)
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

  const getActivityFutureState = (activity, scenarioId) => {
    const agentMap = {
      'option-a': { automationPct: 40, keepHuman: true },
      'option-b': { automationPct: 65, keepHuman: true  },
      'option-c': { automationPct: 85, keepHuman: false }
    }
    const cfg = agentMap[scenarioId]
    const isAgentActivity = scenario.aiAgents.includes(activity.agent)
    const ptFactor  = isAgentActivity ? (1 - cfg.automationPct / 100 * 0.9) : 0.9
    const wtFactor  = isAgentActivity ? (1 - cfg.automationPct / 100 * 0.85) : 0.7
    return {
      processTime: +(((activity.defaultEffort.min + activity.defaultEffort.max) / 2) * ptFactor).toFixed(1),
      waitTime:    +(((activity.defaultWait.min   + activity.defaultWait.max)   / 2) * wtFactor).toFixed(1),
      automated:   isAgentActivity,
      agent:       isAgentActivity ? activity.agent : null
    }
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-violet-600 to-purple-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Future State VSM</h2>
            <p className="text-violet-100">Three transformation scenarios with AI-predicted PT, WT, LT, and Flow Efficiency</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-violet-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-violet-50 shadow">
            {running ? '⏳ Designing...' : '🤖 Run Future State Agent'}
          </button>
        </div>
      </div>

      {/* Scenario tabs */}
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
            <div className="text-xs text-gray-500 mt-1">{s.subtitle}</div>
            <div className="mt-3 grid grid-cols-2 gap-1 text-xs">
              <div><span className="text-gray-500">LT reduction:</span> <span className="font-bold text-green-600">-{s.expectedImprovements.leadTime}%</span></div>
              <div><span className="text-gray-500">FE gain:</span> <span className="font-bold text-green-600">+{s.expectedImprovements.flowEfficiency}%</span></div>
            </div>
          </button>
        ))}
      </div>

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

          {/* Metrics comparison */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Predicted Metrics — Current vs {scenario.label}</h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Lead Time', current: `${BASE_METRICS.leadTime} days`, future: `${futureMetrics.leadTime} days`, improvement: scenario.expectedImprovements.leadTime, lower: true },
                  { label: 'Process Time', current: `${BASE_METRICS.processTime} hrs`, future: `${futureMetrics.processTime} hrs`, improvement: scenario.expectedImprovements.effort, lower: true },
                  { label: 'Wait Time', current: `${BASE_METRICS.waitTime} hrs`, future: `${futureMetrics.waitTime} hrs`, improvement: Math.round(scenario.expectedImprovements.leadTime * 1.2), lower: true },
                  { label: 'Flow Efficiency', current: `${BASE_METRICS.flowEfficiency}%`, future: `${Math.min(futureMetrics.flowEfficiency, 85).toFixed(1)}%`, improvement: scenario.expectedImprovements.flowEfficiency, lower: false }
                ].map(m => (
                  <div key={m.label} className="border border-gray-200 rounded-xl p-4">
                    <div className="text-xs text-gray-500 mb-3 font-semibold">{m.label}</div>
                    <div className="grid grid-cols-2 gap-2 text-center mb-2">
                      <div>
                        <div className="text-xs text-gray-400">Current</div>
                        <div className="font-bold text-gray-800">{m.current}</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-400">Future</div>
                        <div className="font-bold text-green-600">{m.future}</div>
                      </div>
                    </div>
                    <div className={`text-center text-xs font-bold ${m.lower ? 'text-green-600' : 'text-blue-600'}`}>
                      {m.lower ? '▼' : '▲'} {m.improvement}% {m.lower ? 'reduction' : 'improvement'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Future VSM by phase */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Future State Value Stream — Phase by Phase</h3>
            </div>
            <div className="card-body space-y-3">
              {PDLC_PHASES.map(phase => {
                const isOpen = openPhase === phase.id
                const phaseActivities = phase.activities.map(a => ({
                  ...a, future: getActivityFutureState(a, activeScenario)
                }))
                const phasePT = phaseActivities.reduce((s, a) => s + a.future.processTime, 0)
                const phaseWT = phaseActivities.reduce((s, a) => s + a.future.waitTime, 0)
                const automatedCount = phaseActivities.filter(a => a.future.automated).length
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
                      <div className="flex items-center gap-4 text-xs">
                        <div className="text-center"><div className="text-gray-400">PT</div><div className="font-bold text-blue-600">{phasePT.toFixed(0)}h</div></div>
                        <div className="text-center"><div className="text-gray-400">WT</div><div className="font-bold text-red-600">{phaseWT.toFixed(0)}h</div></div>
                        <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                      </div>
                    </button>
                    {isOpen && (
                      <div className="px-5 pb-5 border-t border-gray-100 slide-down">
                        <div className="mt-3 space-y-2">
                          {phaseActivities.map(act => (
                            <div key={act.id} className={`rounded-lg p-3 border text-xs ${
                              act.future.automated ? 'bg-violet-50 border-violet-200' : 'bg-gray-50 border-gray-200'
                            }`}>
                              <div className="flex items-center justify-between">
                                <div className="font-semibold text-gray-800">{act.name}</div>
                                <div className="flex gap-2">
                                  {act.future.automated && <span className="tag-agent">{act.future.agent}</span>}
                                  <span className="font-bold text-blue-600">PT: {act.future.processTime}h</span>
                                  <span className="font-bold text-red-600">WT: {act.future.waitTime}h</span>
                                </div>
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
          </div>
        </>
      )}

      <div className="flex gap-4">
        <Link to="/business-case" className="btn-primary flex-1 text-center py-3">💼 View Business Case →</Link>
        <Link to="/improvements"  className="btn-secondary flex-1 text-center py-3">← Improvements</Link>
      </div>
    </div>
  )
}
