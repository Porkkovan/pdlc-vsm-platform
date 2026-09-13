import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'
import { PDLC_PHASES, FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { useTargetScenario } from '../components/useTargetScenario'

const WORKFLOW_STEPS = [
  { step: 1, label: 'Connect ALM',         path: '/alm-connect',     icon: '🔗', desc: 'Jira, ADO, CSV' },
  { step: 2, label: 'DORA Assessment',     path: '/dora-assessment', icon: '📈', desc: 'Calibrate VSM baselines' },
  { step: 3, label: 'Review VSM Data',     path: '/vsm-editor',      icon: '✏️', desc: 'Override / enrich' },
  { step: 4, label: 'Current State VSM',   path: '/current-vsm',     icon: '🗺️', desc: 'PT, WT, LT, FE' },
  { step: 5, label: 'Bottleneck Analysis', path: '/bottlenecks',     icon: '⚠️', desc: 'AI-identified gaps' },
  { step: 6, label: 'Improvements',        path: '/improvements',    icon: '🚀', desc: 'GenAI recommendations' },
  { step: 7, label: 'Future State',        path: '/future-state',    icon: '🔮', desc: 'Options A / B / C' },
  { step: 8, label: 'Business Case',       path: '/business-case',   icon: '💼', desc: 'ROI & change plan' }
]

export default function DashboardPage() {
  const { project, analysisResult, vsmLevel, setVsmLevel } = useApp()
  const ts = useTargetScenario(project?.id)

  const hasContext = project.organization || project.team

  return (
    <div className="space-y-6 fade-in">
      {/* Hero */}
      <div className="bg-gradient-to-r from-sky-500 to-indigo-400 rounded-2xl p-8 text-white shadow-lg">
        <div className="max-w-3xl">
          <h2 className="text-3xl font-bold mb-2">Strategic Transformation Unified Mapping Platform</h2>
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

      {/* Team Context + VSM Level selector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Org / Team Context */}
        <div className="lg:col-span-2 card">
          <div className="card-header flex items-center justify-between">
            <div>
              <h3 className="font-bold text-gray-800">Team Context</h3>
              <p className="text-xs text-gray-500">Active team scope for VSM analysis across all modules</p>
            </div>
            <div className="flex gap-2">
              {project.productGroups?.length > 0 ? (
                <Link to="/dora-assessment"
                  className="text-xs px-3 py-1 rounded-lg bg-violet-100 hover:bg-violet-200 font-semibold text-violet-700">
                  Switch Team
                </Link>
              ) : null}
              <Link to="/alm-connect"
                className="text-xs px-3 py-1 rounded-lg bg-gray-100 hover:bg-gray-200 font-semibold text-gray-700">
                {project.organization ? 'Edit Org Setup' : 'Setup Org'}
              </Link>
            </div>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {[
                { label: 'Organisation', value: project.organization, icon: '🏢' },
                { label: 'Portfolio',    value: project.portfolio,    icon: '📁' },
                { label: 'Product Group',value: project.productGroup, icon: '📦' },
                { label: 'Product',      value: project.product,      icon: '🗂' },
                { label: 'Product Team', value: project.team,         icon: '👥' },
              ].map(f => (
                <div key={f.label} className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                  <div className="text-xs text-gray-500 mb-1">{f.icon} {f.label}</div>
                  <div className="font-semibold text-gray-800 text-sm truncate">
                    {f.value || <span className="text-gray-400 font-normal italic">Not set</span>}
                  </div>
                </div>
              ))}
            </div>
            {project.productGroups?.length > 0 && (
              <div className="mt-3 text-xs text-gray-500 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2">
                📦 {project.productGroups.length} product group{project.productGroups.length !== 1 ? 's' : ''} · {project.productGroups.reduce((n, g) => n + (g.teams?.length || 0), 0)} teams defined.
                {' '}To assess a different team, use <strong>Switch Team</strong> above or go to DORA Assessment.
              </div>
            )}
            {!hasContext && (
              <p className="text-xs text-cyan-600 mt-3 bg-cyan-50 border border-cyan-200 rounded-lg px-3 py-2">
                Set up your organisation structure in <strong>ALM Connect → Organisation Setup</strong>, then select a product team in <strong>DORA Assessment</strong>.
              </p>
            )}
          </div>
        </div>

        {/* VSM Level toggle */}
        <div className="card">
          <div className="card-header">
            <h3 className="font-bold text-gray-800">VSM Analysis Level</h3>
            <p className="text-xs text-gray-500">Choose the backlog item level for VSM</p>
          </div>
          <div className="card-body space-y-3">
            {[
              {
                id: 'feature',
                label: 'Feature Level',
                icon: '⚡',
                desc: 'All 7 PDLC phases. Lead Time ~30–50 days. Best for portfolio and product planning.',
                lt: '30–50 days', phases: '7 phases'
              },
              {
                id: 'user-story',
                label: 'User Story Level',
                icon: '📝',
                desc: 'Phases 3–6 (Code → Delivery). Lead Time ~3–10 days. Best for sprint and team flow.',
                lt: '3–10 days', phases: 'Phases 3–6'
              }
            ].map(opt => (
              <button
                key={opt.id}
                onClick={() => setVsmLevel(opt.id)}
                className={`w-full text-left p-3 rounded-xl border-2 transition-all ${
                  vsmLevel === opt.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-400'
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{opt.icon}</span>
                  <span className="font-bold text-sm text-gray-800">{opt.label}</span>
                  {vsmLevel === opt.id && <span className="ml-auto text-xs bg-blue-600 text-white px-2 py-0.5 rounded-full">Active</span>}
                </div>
                <p className="text-xs text-gray-500 mb-2">{opt.desc}</p>
                <div className="flex gap-3 text-xs">
                  <span className="bg-gray-100 px-2 py-0.5 rounded font-semibold text-gray-700">LT: {opt.lt}</span>
                  <span className="bg-gray-100 px-2 py-0.5 rounded font-semibold text-gray-700">{opt.phases}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'PDLC Phases',    value: vsmLevel === 'user-story' ? '4' : '7',  color: 'blue',   icon: '📋', note: vsmLevel === 'user-story' ? 'Story cycle (3–6)' : 'Full PDLC' },
          { label: 'Activities',     value: vsmLevel === 'user-story' ? '16' : '36', color: 'purple', icon: '⚡', note: vsmLevel === 'user-story' ? 'Story activities' : 'All activities' },
          { label: 'AI Agents',      value: '22', color: 'indigo', icon: '🤖', note: 'Available agents' },
          { label: 'Future Options', value: '3',  color: 'green',  icon: '🔮', note: 'A / B / C scenarios' }
        ].map(s => (
          <div key={s.label} className="card card-body text-center">
            <div className="text-3xl mb-1">{s.icon}</div>
            <div className={`text-3xl font-bold text-${s.color}-600`}>{s.value}</div>
            <div className="text-sm text-gray-700 font-medium">{s.label}</div>
            <div className="text-xs text-gray-400 mt-0.5">{s.note}</div>
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
            {WORKFLOW_STEPS.map(s => (
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
          <h3 className="font-bold text-gray-800">
            {vsmLevel === 'user-story' ? 'User Story Cycle — Phases 3–6 (active)' : '7 PDLC Phases — 36 Activities'}
          </h3>
          <p className="text-sm text-gray-500">
            {vsmLevel === 'user-story'
              ? 'Phases 1–2 are planning prerequisites, not included in story cycle time'
              : 'Complete product engineering value stream, from backlog to monitoring'}
          </p>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {PDLC_PHASES.map(phase => {
              const isStoryCycle = phase.id >= 3 && phase.id <= 6
              const isPrereq = vsmLevel === 'user-story' && !isStoryCycle
              return (
                <div key={phase.id}
                  className={`border rounded-lg p-4 transition-shadow ${isPrereq ? 'border-gray-100 bg-gray-50 opacity-60' : 'border-gray-200 hover:shadow-sm'}`}>
                  <div className="flex items-center gap-3 mb-2">
                    <div className={`w-8 h-8 text-white rounded-lg flex items-center justify-center font-bold text-sm ${isPrereq ? 'bg-gray-400' : 'bg-gradient-to-br from-blue-500 to-blue-600'}`}>
                      {phase.id}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-800 text-sm">{phase.name}</div>
                      <div className="text-xs text-gray-500">
                        {isPrereq ? 'Planning prerequisite' : `${phase.activities.length} activities`}
                      </div>
                    </div>
                  </div>
                  {!isPrereq && (
                    <div className="flex gap-2 text-xs">
                      <span className="tag-metric">Effort: {phase.defaultEffortRange.min}–{phase.defaultEffortRange.max}h</span>
                      <span className="tag-time">Wait: {phase.defaultWaitRange.min}–{phase.defaultWaitRange.max} {phase.waitUnit}</span>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Future state overview — configured target path, or generic A/B/C */}
      {ts.configured ? (
        <div className="card">
          <div className="card-header flex items-center justify-between">
            <div>
              <h3 className="font-bold text-gray-800">Your Target State Path</h3>
              <p className="text-sm text-gray-500">Configured journey to your envisioned future state{ts.platform && <> on {(ts.platform || '').replace('_', ' ')}</>}</p>
            </div>
            <Link to="/target-state" className="text-xs font-semibold text-sky-700 hover:underline">Open Studio →</Link>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {ts.steps.map((s, i) => (
                <div key={s.step ?? i} className={`border-2 rounded-xl p-5 ${s.is_target ? 'border-emerald-300 bg-emerald-50/40' : 'border-gray-200'}`}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-0.5 rounded font-bold text-sm text-white ${s.is_target ? 'bg-emerald-600' : 'bg-sky-600'}`}>{s.is_target ? '★ ' : ''}L{s.level}</span>
                    <span className="text-xs font-semibold text-gray-600">{s.automation_pct}% automation</span>
                  </div>
                  <div className="font-bold text-gray-800 mb-1">{s.label}</div>
                  <div className="text-xs text-gray-500 mb-2">{s.ml_band}</div>
                  <div className="text-xs text-gray-600">Humans: {s.human_roles_retained?.join(', ')}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
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
                    <span className="text-gray-600">Process Time reduction</span>
                    <span className="font-bold text-green-600">-{s.expectedImprovements.effort}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Flow Efficiency gain</span>
                    <span className="font-bold text-green-600">+{s.expectedImprovements.flowEfficiency}%</span>
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
      )}
    </div>
  )
}
