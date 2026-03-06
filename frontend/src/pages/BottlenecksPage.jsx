import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

// Built-in bottleneck catalogue (used when agents haven't run yet)
const DEFAULT_BOTTLENECKS = [
  { id: 'bn-1', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Automated Performance Testing', severity: 'Critical', metric: 'effort', value: '16–40 hrs', impact: 'Longest effort activity in PDLC, blocks release readiness', category: 'Effort' },
  { id: 'bn-2', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Manual SIT / UAT / NF Signoff',  severity: 'Critical', metric: 'wait', value: '2–5 days', impact: 'Human approval dependency creates flow stoppage', category: 'Wait' },
  { id: 'bn-3', phaseId: 3, phaseName: 'Code Management',    activity: 'Peer Code Review',               severity: 'High',     metric: 'wait', value: '4–24 hrs', impact: 'Reviewer availability blocks developer throughput', category: 'Wait' },
  { id: 'bn-4', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Test Data Generation / Management',severity: 'High',    metric: 'wait', value: '4–16 hrs', impact: 'Data provisioning delays test execution start', category: 'Wait' },
  { id: 'bn-5', phaseId: 6, phaseName: 'Continuous Delivery', activity: 'Release Gates / Approvals',     severity: 'High',     metric: 'wait', value: '1–5 days', impact: 'Change advisory board scheduling delays', category: 'Wait' },
  { id: 'bn-6', phaseId: 2, phaseName: 'Architecture & UX Design', activity: 'UX/UI High-Fidelity Design & Handoff', severity: 'Medium', metric: 'effort', value: '16–40 hrs', impact: 'Design-to-dev handoff creates rework loops', category: 'Effort' },
  { id: 'bn-7', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Dynamic Security Testing (DAST)', severity: 'Medium',  metric: 'wait', value: '4–16 hrs', impact: 'DAST scan queue and false-positive triaging', category: 'Wait' },
  { id: 'bn-8', phaseId: 2, phaseName: 'Architecture & UX Design', activity: 'Solution Architecture (High-Level)', severity: 'Medium', metric: 'wait', value: '3–7 days', impact: 'Architecture review board scheduling bottleneck', category: 'Wait' }
]

const SEVERITY_STYLES = {
  Critical: 'bg-red-100 text-red-800 border-red-300',
  High:     'bg-orange-100 text-orange-800 border-orange-300',
  Medium:   'bg-yellow-100 text-yellow-800 border-yellow-300',
  Low:      'bg-blue-100 text-blue-800 border-blue-300'
}

export default function BottlenecksPage() {
  const { analysisResult, addNotification, project } = useApp()
  const [running, setRunning] = useState(false)
  const [filter, setFilter] = useState('all')
  const [viewMode, setViewMode] = useState('cards')

  const bottlenecks = analysisResult?.bottlenecks ?? DEFAULT_BOTTLENECKS
  const filtered = filter === 'all' ? bottlenecks : bottlenecks.filter(b => b.severity === filter)

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runBottleneckAnalyzer(project.id || 'demo')
      addNotification('Bottleneck analysis complete!', 'success')
    } catch {
      addNotification('Running in demo mode — using built-in bottleneck catalogue', 'info')
    } finally { setRunning(false) }
  }

  const criticalCount = bottlenecks.filter(b => b.severity === 'Critical').length
  const highCount     = bottlenecks.filter(b => b.severity === 'High').length
  const waitCount     = bottlenecks.filter(b => b.metric === 'wait').length
  const effortCount   = bottlenecks.filter(b => b.metric === 'effort').length

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-red-600 to-orange-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Bottleneck Analysis</h2>
            <p className="text-red-100">AI-identified flow blockers across all PDLC phases and practices</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-red-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-red-50 shadow">
            {running ? '⏳ Analyzing...' : '🤖 Run Agent'}
          </button>
        </div>
      </div>

      {/* Severity summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Critical',     count: criticalCount, color: 'red',    icon: '🔴' },
          { label: 'High',         count: highCount,     color: 'orange', icon: '🟠' },
          { label: 'Wait Blockers',count: waitCount,     color: 'yellow', icon: '⏳' },
          { label: 'Effort Peaks', count: effortCount,   color: 'blue',   icon: '⚡' }
        ].map(s => (
          <div key={s.label} className="card card-body text-center">
            <div className="text-2xl mb-1">{s.icon}</div>
            <div className={`text-3xl font-bold text-${s.color}-600`}>{s.count}</div>
            <div className="text-xs text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 bg-white p-4 rounded-xl border border-gray-200">
        {['all','Critical','High','Medium'].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-lg text-sm font-semibold transition-colors ${
              filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {f === 'all' ? `All (${bottlenecks.length})` : `${f} (${bottlenecks.filter(b => b.severity === f).length})`}
          </button>
        ))}
      </div>

      {/* Bottleneck cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {filtered.map((bn, i) => (
          <div key={bn.id} className={`card border-l-4 ${
            bn.severity === 'Critical' ? 'border-l-red-600' :
            bn.severity === 'High'     ? 'border-l-orange-500' :
            'border-l-yellow-500'
          }`}>
            <div className="card-body space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="font-bold text-gray-800">{bn.activity}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{bn.phaseName}</div>
                </div>
                <span className={`border px-2 py-0.5 rounded-full text-xs font-bold shrink-0 ${SEVERITY_STYLES[bn.severity]}`}>
                  {bn.severity}
                </span>
              </div>
              <div className="flex gap-3 text-xs">
                <span className={bn.metric === 'wait' ? 'tag-time' : 'tag-metric'}>
                  {bn.metric === 'wait' ? '⏳' : '⚡'} {bn.metric === 'wait' ? 'Wait' : 'Effort'}: {bn.value}
                </span>
                <span className="tag-phase">{bn.category}</span>
              </div>
              <div className="bg-red-50 rounded-lg p-3 text-xs text-red-800 border border-red-100">
                <span className="font-semibold">Impact: </span>{bn.impact}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Phase heatmap */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Phase Bottleneck Heatmap</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-7 gap-2">
            {PDLC_PHASES.map(phase => {
              const count = bottlenecks.filter(b => b.phaseId === phase.id).length
              const hasCritical = bottlenecks.some(b => b.phaseId === phase.id && b.severity === 'Critical')
              return (
                <div key={phase.id} className={`text-center p-3 rounded-lg ${
                  hasCritical ? 'bg-red-100 border-2 border-red-400' :
                  count > 0   ? 'bg-orange-100 border border-orange-300' :
                  'bg-green-50 border border-green-200'
                }`}>
                  <div className="text-xl font-bold">{count > 0 ? '⚠️' : '✅'}</div>
                  <div className="text-xs font-bold text-gray-700 mt-1">{count}</div>
                  <div className="text-xs text-gray-500 leading-tight mt-1">{phase.name.split(' ').slice(0,2).join(' ')}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div className="flex gap-4">
        <Link to="/improvements" className="btn-primary flex-1 text-center py-3">🚀 View Improvement Actions →</Link>
        <Link to="/current-vsm"  className="btn-secondary flex-1 text-center py-3">← Current State VSM</Link>
      </div>
    </div>
  )
}
