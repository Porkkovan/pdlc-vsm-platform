import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES, VSM_METRICS } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

const PHASE_COLORS = ['blue','purple','green','orange','red','teal','cyan']

export default function CurrentVSMPage() {
  const { vsmData, setAnalysisResult, addNotification, project } = useApp()
  const [openPhase, setOpenPhase] = useState(null)
  const [running, setRunning] = useState(false)

  // Merge ALM data with default ranges
  const getPhaseMetrics = (phase) => {
    const almPhase = vsmData?.phases?.find(p => p.phaseId === phase.id)
    return {
      processTime: almPhase?.processTime ?? ((phase.defaultEffortRange.min + phase.defaultEffortRange.max) / 2),
      waitTime:    almPhase?.waitTime    ?? ((phase.defaultWaitRange.min  + phase.defaultWaitRange.max)  / 2),
      leadTime:    almPhase?.leadTime    ?? ((phase.defaultEffortRange.min + phase.defaultEffortRange.max) / 2 +
                                             (phase.defaultWaitRange.min  + phase.defaultWaitRange.max)  / 2) / 8,
      source: almPhase ? 'alm' : 'default'
    }
  }

  const totalPT = PDLC_PHASES.reduce((s, p) => s + getPhaseMetrics(p).processTime, 0)
  const totalWT = PDLC_PHASES.reduce((s, p) => s + getPhaseMetrics(p).waitTime, 0)
  const totalLT = (totalPT + totalWT) / 8   // convert hours to days
  const flowEfficiency = ((totalPT / (totalPT + totalWT)) * 100).toFixed(1)

  const runAnalysis = async () => {
    setRunning(true)
    try {
      const result = await agentsApi.runVSMAnalyzer(project.id || 'demo')
      setAnalysisResult(result)
      addNotification('VSM analysis complete!', 'success')
    } catch {
      addNotification('Agent running in background (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Current State Value Stream Map</h2>
            <p className="text-purple-100">Baseline PDLC metrics — Process Time, Wait Time, Lead Time, Flow Efficiency</p>
          </div>
          <button
            onClick={runAnalysis}
            disabled={running}
            className="bg-white text-purple-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-purple-50 transition-colors shadow"
          >
            {running ? '⏳ Analyzing...' : '🤖 Run AI Analysis'}
          </button>
        </div>
      </div>

      {/* KPI summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Process Time', value: `${Math.round(totalPT)} hrs`, sub: 'Touch time',     color: 'blue'  },
          { label: 'Total Wait Time',    value: `${Math.round(totalWT)} hrs`, sub: 'Non-value time', color: 'red'   },
          { label: 'Total Lead Time',    value: `${totalLT.toFixed(1)} days`, sub: 'End to end',     color: 'purple'},
          { label: 'Flow Efficiency',    value: `${flowEfficiency}%`,          sub: 'PT ÷ LT',        color: 'green' }
        ].map(m => (
          <div key={m.label} className="card card-body text-center">
            <div className={`text-2xl font-bold text-${m.color}-600`}>{m.value}</div>
            <div className="text-xs text-gray-500 mt-1">{m.label}</div>
            <div className="text-xs text-gray-400">{m.sub}</div>
          </div>
        ))}
      </div>

      {/* VSM flow bar */}
      <div className="card card-body">
        <h3 className="font-bold text-gray-800 mb-4">Value Stream Flow — Process vs Wait Time</h3>
        <div className="space-y-3">
          {PDLC_PHASES.map((phase, i) => {
            const m = getPhaseMetrics(phase)
            const total = m.processTime + m.waitTime
            const ptPct = Math.round((m.processTime / total) * 100)
            return (
              <div key={phase.id}>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="font-semibold text-gray-700">{phase.id}. {phase.name}</span>
                  <span className="text-gray-500">FE: {ptPct}%</span>
                </div>
                <div className="flex h-5 rounded-full overflow-hidden bg-gray-100">
                  <div
                    className="bg-blue-500 flex items-center justify-center text-white text-xs font-semibold"
                    style={{ width: `${ptPct}%` }}
                    title={`PT: ${m.processTime}h`}
                  >{ptPct > 10 ? 'PT' : ''}</div>
                  <div
                    className="bg-red-400 flex items-center justify-center text-white text-xs font-semibold"
                    style={{ width: `${100-ptPct}%` }}
                    title={`WT: ${m.waitTime}h`}
                  >{(100-ptPct) > 10 ? 'WT' : ''}</div>
                </div>
                <div className="flex justify-between text-xs text-gray-400 mt-0.5">
                  <span>PT: {Math.round(m.processTime)}h</span>
                  <span>WT: {Math.round(m.waitTime)}h</span>
                </div>
              </div>
            )
          })}
        </div>
        <div className="flex gap-4 mt-4 text-xs">
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-blue-500 rounded" /><span>Process Time (value-add)</span></div>
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-red-400 rounded" /><span>Wait Time (waste)</span></div>
        </div>
      </div>

      {/* Phase accordion */}
      <div className="space-y-3">
        {PDLC_PHASES.map((phase, i) => {
          const m = getPhaseMetrics(phase)
          const isOpen = openPhase === phase.id
          return (
            <div key={phase.id} className="card overflow-hidden">
              <button
                onClick={() => setOpenPhase(isOpen ? null : phase.id)}
                className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg flex items-center justify-center font-bold">
                    {phase.id}
                  </div>
                  <div className="text-left">
                    <div className="font-bold text-gray-800">{phase.name}</div>
                    <div className="text-xs text-gray-500">{phase.activities.length} activities · {m.source === 'alm' ? '🟢 ALM data' : '⚪ default range'}</div>
                  </div>
                </div>
                <div className="flex items-center gap-6 text-right">
                  <div><div className="text-xs text-gray-500">Process Time</div><div className="font-bold text-blue-600">{Math.round(m.processTime)}h</div></div>
                  <div><div className="text-xs text-gray-500">Wait Time</div><div className="font-bold text-red-600">{Math.round(m.waitTime)}h</div></div>
                  <div><div className="text-xs text-gray-500">Lead Time</div><div className="font-bold text-purple-600">{m.leadTime.toFixed(1)}d</div></div>
                  <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                </div>
              </button>

              {isOpen && (
                <div className="px-6 pb-6 border-t border-gray-100 slide-down">
                  <div className="mt-4 space-y-3">
                    {phase.activities.map(act => (
                      <div key={act.id} className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-lg p-4 border border-gray-200">
                        <div className="flex items-start justify-between mb-2">
                          <div className="font-semibold text-gray-800 text-sm">{act.name}</div>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                            act.type === 'GenAI Agent' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                          }`}>{act.type}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-3 mb-3 text-xs">
                          <div><span className="text-gray-500">Effort: </span><span className="font-semibold text-blue-600">{act.defaultEffort.min}–{act.defaultEffort.max}h</span></div>
                          <div><span className="text-gray-500">Wait: </span><span className="font-semibold text-red-600">{act.defaultWait.min}–{act.defaultWait.max} {act.waitUnit}</span></div>
                        </div>
                        <div className="bg-white rounded p-3 border border-blue-100 text-xs text-gray-700">
                          <span className="font-semibold text-blue-700">AI Opportunity: </span>{act.aiOpportunity}
                        </div>
                        <div className="mt-2 flex items-center gap-2">
                          <span className="tag-agent">{act.agent}</span>
                          {act.tools.slice(0,2).map(t => <span key={t} className="tag-tool">{t}</span>)}
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

      {/* CTA */}
      <div className="flex gap-4">
        <Link to="/bottlenecks" className="btn-primary flex-1 text-center py-3">
          ⚠️ Run Bottleneck Analysis →
        </Link>
        <Link to="/vsm-editor" className="btn-secondary flex-1 text-center py-3">
          ✏️ Edit VSM Data
        </Link>
      </div>
    </div>
  )
}
