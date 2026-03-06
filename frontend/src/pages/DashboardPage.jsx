import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'
import { PDLC_PHASES, FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'

const WORKFLOW_STEPS = [
  { step: 1, label: 'Connect ALM',         path: '/alm-connect',  icon: '🔗', desc: 'Jira, ADO, CSV' },
  { step: 2, label: 'Review VSM Data',     path: '/vsm-editor',   icon: '✏️', desc: 'Override / enrich' },
  { step: 3, label: 'Current State VSM',   path: '/current-vsm',  icon: '🗺️', desc: 'PT, WT, LT, FE' },
  { step: 4, label: 'Bottleneck Analysis', path: '/bottlenecks',  icon: '⚠️', desc: 'AI-identified gaps' },
  { step: 5, label: 'Improvements',        path: '/improvements', icon: '🚀', desc: 'GenAI recommendations' },
  { step: 6, label: 'Future State',        path: '/future-state', icon: '🔮', desc: 'Options A / B / C' },
  { step: 7, label: 'Business Case',       path: '/business-case',icon: '💼', desc: 'ROI & change plan' }
]

export default function DashboardPage() {
  const { project, analysisResult, agentStatus } = useApp()
  const hasData = !!analysisResult

  return (
    <div className="space-y-8 fade-in">
      {/* Hero */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-8 text-white shadow-lg">
        <div className="max-w-3xl">
          <h2 className="text-3xl font-bold mb-2">PDLC Value Stream Mapping Platform</h2>
          <p className="text-blue-100 text-lg mb-4">
            End-to-end multi-agent platform — connect your ALM tools, baseline your engineering practices, identify bottlenecks, and design AI-powered future states.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link to="/alm-connect" className="bg-white text-blue-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-50 transition-colors shadow">
              🔗 Connect ALM Tool
            </Link>
            <Link to="/current-vsm" className="bg-blue-500 text-white px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-400 transition-colors">
              🗺️ View Current VSM
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'PDLC Phases',    value: '7',  color: 'blue',   icon: '📋' },
          { label: 'Activities',     value: '36', color: 'purple', icon: '⚡' },
          { label: 'AI Agents',      value: '22', color: 'indigo', icon: '🤖' },
          { label: 'Future Options', value: '3',  color: 'green',  icon: '🔮' }
        ].map(s => (
          <div key={s.label} className="card card-body text-center">
            <div className="text-3xl mb-1">{s.icon}</div>
            <div className={`text-3xl font-bold text-${s.color}-600`}>{s.value}</div>
            <div className="text-sm text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Workflow steps */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Analysis Workflow</h3>
          <p className="text-sm text-gray-500">Follow these steps to complete your VSM analysis</p>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {WORKFLOW_STEPS.map((s, i) => (
              <Link key={s.step} to={s.path} className="block">
                <div className="border border-gray-200 rounded-xl p-4 hover:border-blue-400 hover:shadow-md transition-all group">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">
                      {s.step}
                    </span>
                    <span className="text-lg">{s.icon}</span>
                  </div>
                  <div className="font-semibold text-gray-800 text-sm group-hover:text-blue-700">{s.label}</div>
                  <div className="text-xs text-gray-500 mt-1">{s.desc}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* PDLC phases overview */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">7 PDLC Phases — 36 Activities</h3>
          <p className="text-sm text-gray-500">Complete product engineering value stream, from backlog to monitoring</p>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {PDLC_PHASES.map(phase => (
              <div key={phase.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg flex items-center justify-center font-bold text-sm">
                    {phase.id}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-800 text-sm">{phase.name}</div>
                    <div className="text-xs text-gray-500">{phase.activities.length} activities</div>
                  </div>
                </div>
                <div className="flex gap-2 text-xs">
                  <span className="tag-metric">Effort: {phase.defaultEffortRange.min}–{phase.defaultEffortRange.max}h</span>
                  <span className="tag-time">Wait: {phase.defaultWaitRange.min}–{phase.defaultWaitRange.max} {phase.waitUnit}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Future state scenarios overview */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">3 Future State Scenarios</h3>
          <p className="text-sm text-gray-500">AI-designed transformation options with predicted metrics & business cases</p>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {FUTURE_STATE_SCENARIOS.map(s => (
              <div key={s.id} className="border-2 border-gray-200 rounded-xl p-5 hover:border-blue-400 hover:shadow-md transition-all">
                <div className="flex items-center gap-2 mb-3">
                  <span className="bg-blue-600 text-white px-2 py-0.5 rounded font-bold text-sm">{s.label}</span>
                  <span className="text-xs font-semibold text-gray-600">{Math.round(s.automationLevel)}% Automation</span>
                </div>
                <div className="font-bold text-gray-800 mb-1">{s.title}</div>
                <div className="text-xs text-gray-500 mb-3">{s.subtitle}</div>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Lead Time reduction</span>
                    <span className="font-bold text-green-600">-{s.expectedImprovements.leadTime}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Flow Efficiency gain</span>
                    <span className="font-bold text-green-600">+{s.expectedImprovements.flowEfficiency}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Effort reduction</span>
                    <span className="font-bold text-green-600">-{s.expectedImprovements.effort}%</span>
                  </div>
                </div>
                <div className="mt-3 text-xs text-gray-600">
                  <span className="font-semibold">Human roles:</span> {s.humanRoles.length} · <span className="font-semibold">AI Agents:</span> {s.aiAgents.length}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
