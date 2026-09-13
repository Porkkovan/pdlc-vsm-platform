import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'

// ─── Role transformation data per phase ──────────────────────────────────────
const PHASE_ROLES = [
  {
    phase: 'Backlog & Roadmap', phaseId: 1, icon: '📋',
    current:  ['Product Manager', 'Business Analyst', 'Release Train Engineer', 'Scrum Master'],
    augmented:['Product Manager (AI-assisted prioritisation)', 'BA + AI Requirements Agent', 'Release Train Engineer'],
    autonomous:['Product Definer (strategic intent only)', 'AI Roadmap & Backlog Agent'],
    changeImpact: 'High',
  },
  {
    phase: 'Architecture & UX Design', phaseId: 2, icon: '🎨',
    current:  ['Solution Architect', 'UX Designer', 'Tech Lead', 'Security Architect'],
    augmented:['Solution Architect (AI design assistant)', 'UX Designer + AI Prototyping', 'Tech Lead'],
    autonomous:['Product Builder (design oversight)', 'AI Architecture Agent', 'AI UX Agent'],
    changeImpact: 'High',
  },
  {
    phase: 'Code Management', phaseId: 3, icon: '💻',
    current:  ['Software Engineers (4–6)', 'Code Reviewer', 'Tech Lead'],
    augmented:['Engineers + AI Pair Programmer', 'Automated Code Review Agent', 'Tech Lead (oversight)'],
    autonomous:['AI Code Generation Agent', 'AI Code Review Agent', 'Product Builder (acceptance)'],
    changeImpact: 'Critical',
  },
  {
    phase: 'Continuous Integration', phaseId: 4, icon: '⚙️',
    current:  ['DevOps Engineer', 'Build Engineer', 'QA Lead'],
    augmented:['DevOps Engineer + AI Pipeline Optimiser', 'AI Build Failure Analyser'],
    autonomous:['AI CI Orchestrator Agent', 'AI Build & Quality Gate Agent'],
    changeImpact: 'Medium',
  },
  {
    phase: 'Continuous Testing', phaseId: 5, icon: '🧪',
    current:  ['QA Engineers (3–5)', 'Test Manager', 'Performance Engineer', 'Security Tester'],
    augmented:['QA Lead + AI Test Generator', 'AI Regression Agent', 'Performance Engineer'],
    autonomous:['AI Test Suite Agent', 'AI Performance Agent', 'AI Security Scanner', 'QA Oversight (sign-off only)'],
    changeImpact: 'Critical',
  },
  {
    phase: 'Continuous Delivery', phaseId: 6, icon: '🚀',
    current:  ['Release Manager', 'DevOps Engineer', 'Change Advisory Board'],
    augmented:['Release Manager + AI Release Notes', 'DevOps + AI Deploy Validator'],
    autonomous:['AI Release Orchestrator', 'AI Change Risk Assessor', 'Human sign-off for prod only'],
    changeImpact: 'High',
  },
  {
    phase: 'Monitoring & Feedback', phaseId: 7, icon: '📡',
    current:  ['Site Reliability Engineer', 'Incident Manager', 'On-Call Engineer', 'Operations Analyst'],
    augmented:['SRE + AIOps Assistant', 'AI Incident Classifier', 'AI Anomaly Detector'],
    autonomous:['AI Self-Healing Agent', 'AI Incident Response Agent', 'SRE (major incidents only)'],
    changeImpact: 'High',
  },
]

const READINESS_DIMS = [
  { id: 'culture',    label: 'Culture & Mindset',         icon: '🧠', desc: 'Team openness to AI adoption, psychological safety, and growth mindset' },
  { id: 'process',    label: 'Process Maturity',           icon: '⚙️', desc: 'CI/CD pipeline maturity, DevOps practices, and delivery cadence' },
  { id: 'technology', label: 'Technology & Tooling',       icon: '🛠️', desc: 'Cloud-native infrastructure, observability, and developer toolchain' },
  { id: 'data',       label: 'Data & Knowledge Assets',    icon: '📊', desc: 'Availability of structured data, documentation, and knowledge bases for AI context' },
  { id: 'governance', label: 'Governance & Risk Appetite', icon: '🛡️', desc: 'Leadership support, risk frameworks, and change management capability' },
]

const CHANGE_IMPACT_COLOR = { Low: 'bg-green-100 text-green-700', Medium: 'bg-cyan-100 text-cyan-700', High: 'bg-teal-100 text-teal-700', Critical: 'bg-sky-100 text-sky-700' }

const OPTION_LABELS = { a: 'Option A — AI-Augmented', b: 'Option B — Hybrid', c: 'Option C — ADLC' }
const OPTION_COLORS = { a: 'blue', b: 'purple', c: 'emerald' }
const CHANGE_EFFORT = {
  a: {
    effort: 'Moderate', duration: '6–12 months', headcountImpact: 'Role re-skilling for ~30% of team',
    keyChanges: ['Introduce AI co-pilot tooling per phase', 'Train engineers on prompt engineering', 'Establish AI output review processes', 'Update job descriptions to include AI proficiency'],
  },
  b: {
    effort: 'Significant', duration: '12–18 months', headcountImpact: 'Role transformation for ~55% of team',
    keyChanges: ['Redefine roles from doers to AI supervisors', 'Establish AI Center of Excellence', 'Build internal AI model governance', 'Restructure teams around AI-human pods', 'Update performance frameworks for AI-led delivery'],
  },
  c: {
    effort: 'Transformational', duration: '18–30 months', headcountImpact: 'New operating model — ~80% role redesign',
    keyChanges: ['Shift to Product Definer + Product Builder model', 'Full ADLC platform engineering investment', 'Enterprise AI governance board established', 'Continuous AI model monitoring and retraining', 'Org structure redesigned around outcomes not functions'],
  },
}

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function TransformationReadinessPage() {
  const { project } = useApp()
  const [scores, setScores] = useState({ culture: 3, process: 3, technology: 3, data: 2, governance: 2 })
  const [activeTab, setActiveTab]       = useState('readiness')
  const [selectedOption, setOption]     = useState('b')
  const [expandedPhase, setExpandPhase] = useState(null)

  const totalScore = Object.values(scores).reduce((a, b) => a + b, 0)
  const maxScore   = READINESS_DIMS.length * 5
  const readinessPct = Math.round(totalScore / maxScore * 100)
  const readinessLabel = readinessPct >= 80 ? 'Ready' : readinessPct >= 60 ? 'Mostly Ready' : readinessPct >= 40 ? 'Developing' : 'Early Stage'
  const readinessColor = readinessPct >= 80 ? 'text-green-600' : readinessPct >= 60 ? 'text-blue-600' : readinessPct >= 40 ? 'text-cyan-600' : 'text-sky-600'

  const TABS = [
    { id: 'readiness', label: '📊 Readiness Assessment' },
    { id: 'roles',     label: '👥 Role Transformation'  },
    { id: 'change',    label: '🗓️ Change Management'    },
  ]

  return (
    <div className="space-y-6 fade-in">

      {/* Hero */}
      <div className="bg-gradient-to-r from-violet-600 to-purple-800 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">Transformation Readiness</h2>
            <p className="text-violet-100 text-sm max-w-2xl">
              Assess your organisation's readiness for AI-led transformation. Map role changes per PDLC phase,
              understand change management effort, and identify the people and governance changes needed alongside technology adoption.
            </p>
            {project.organization && (
              <div className="mt-2 flex items-center gap-2 flex-wrap">
                <span className="bg-white/20 text-xs font-semibold px-2.5 py-1 rounded-full">🏢 {project.organization}</span>
                {project.team && <span className="bg-white/20 text-xs font-semibold px-2.5 py-1 rounded-full">👥 {project.team}</span>}
              </div>
            )}
          </div>
          <div className="flex gap-3 shrink-0">
            <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[90px]">
              <div className={`text-2xl font-bold ${readinessPct >= 60 ? 'text-green-300' : readinessPct >= 40 ? 'text-cyan-300' : 'text-sky-300'}`}>{readinessPct}%</div>
              <div className="text-xs text-violet-200 mt-0.5">{readinessLabel}</div>
            </div>
            <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[90px]">
              <div className="text-2xl font-bold">{totalScore}<span className="text-sm text-violet-300">/{maxScore}</span></div>
              <div className="text-xs text-violet-200 mt-0.5">Readiness Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === t.id ? 'border-violet-600 text-violet-600' : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── Readiness Assessment ── */}
      {activeTab === 'readiness' && (
        <div className="space-y-4">
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Transformation Readiness Assessment</h3>
              <p className="text-xs text-gray-500">Rate your organisation across 5 dimensions — 1 (Early Stage) to 5 (Fully Mature)</p>
            </div>
            <div className="card-body space-y-5">
              {READINESS_DIMS.map(dim => (
                <div key={dim.id}>
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{dim.icon}</span>
                        <span className="text-sm font-bold text-gray-800">{dim.label}</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          scores[dim.id] >= 4 ? 'bg-green-100 text-green-700' :
                          scores[dim.id] >= 3 ? 'bg-blue-100 text-blue-700' :
                          scores[dim.id] >= 2 ? 'bg-cyan-100 text-cyan-700' : 'bg-sky-100 text-sky-700'
                        }`}>{scores[dim.id]}/5</span>
                      </div>
                      <p className="text-xs text-gray-500 ml-7">{dim.desc}</p>
                    </div>
                  </div>
                  <div className="flex gap-2 ml-7">
                    {[1, 2, 3, 4, 5].map(n => (
                      <button key={n} onClick={() => setScores(s => ({ ...s, [dim.id]: n }))}
                        className={`w-10 h-8 rounded-lg text-xs font-bold transition-all ${
                          scores[dim.id] === n
                            ? 'bg-violet-600 text-white shadow-md scale-105'
                            : scores[dim.id] > n
                            ? 'bg-violet-100 text-violet-700'
                            : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                        }`}>{n}</button>
                    ))}
                    <span className="text-xs text-gray-400 self-center ml-2">
                      {scores[dim.id] === 1 ? 'Early Stage' : scores[dim.id] === 2 ? 'Developing' : scores[dim.id] === 3 ? 'Established' : scores[dim.id] === 4 ? 'Advanced' : 'Leading'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Radar summary */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Readiness Summary</h3>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-5 gap-3 mb-4">
                {READINESS_DIMS.map(dim => {
                  const s = scores[dim.id]
                  const pct = (s / 5) * 100
                  return (
                    <div key={dim.id} className="text-center">
                      <div className="text-xl mb-1">{dim.icon}</div>
                      <div className="w-full bg-gray-200 rounded-full h-20 relative overflow-hidden">
                        <div className={`absolute bottom-0 w-full transition-all rounded-b-full ${
                          s >= 4 ? 'bg-green-500' : s >= 3 ? 'bg-blue-500' : s >= 2 ? 'bg-cyan-400' : 'bg-sky-400'
                        }`} style={{ height: `${pct}%` }} />
                      </div>
                      <div className="text-xs font-bold text-gray-700 mt-1">{s}/5</div>
                      <div className="text-xs text-gray-500 truncate">{dim.label.split(' ')[0]}</div>
                    </div>
                  )
                })}
              </div>
              <div className={`p-4 rounded-xl border ${
                readinessPct >= 70 ? 'bg-green-50 border-green-200 text-green-800' :
                readinessPct >= 50 ? 'bg-blue-50 border-blue-200 text-blue-800' :
                'bg-cyan-50 border-cyan-200 text-cyan-800'
              }`}>
                <div className="font-bold text-sm mb-1">{readinessLabel} for AI Transformation — {readinessPct}%</div>
                <p className="text-xs">
                  {readinessPct >= 70 ? 'Strong foundation across all dimensions. Ready to accelerate to Option B or C transformation.' :
                   readinessPct >= 50 ? 'Solid base — address gaps in lower-scored dimensions before scaling AI adoption.' :
                   'Key gaps identified. Focus on Process and Culture dimensions first before investing in AI tooling.'}
                </p>
                <div className="mt-2 text-xs font-semibold">
                  Recommended starting point: {' '}
                  <Link to="/future-state" className="underline">
                    {readinessPct >= 70 ? 'Option B or C' : readinessPct >= 50 ? 'Option A or B' : 'Option A — AI-Augmented'}
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Role Transformation ── */}
      {activeTab === 'roles' && (
        <div className="space-y-3">
          <div className="bg-violet-50 border border-violet-200 rounded-xl p-4 text-sm text-violet-800">
            <strong>How to read this:</strong> Each phase shows current human roles → AI-augmented roles (Option A/B) → autonomous AI agents (Option C).
            Roles in purple are redesigned. Roles removed in a scenario are replaced by AI agents.
          </div>
          {PHASE_ROLES.map(phase => (
            <div key={phase.phaseId} className="card">
              <button
                className="card-header flex items-center justify-between w-full text-left hover:bg-gray-50 transition-colors rounded-t-xl"
                onClick={() => setExpandPhase(expandedPhase === phase.phaseId ? null : phase.phaseId)}>
                <div className="flex items-center gap-3">
                  <span className="text-xl">{phase.icon}</span>
                  <div>
                    <div className="font-bold text-gray-800 text-sm">Phase {phase.phaseId}: {phase.phase}</div>
                    <div className="text-xs text-gray-500">{phase.current.length} current roles → {phase.autonomous.length} future roles (Option C)</div>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${CHANGE_IMPACT_COLOR[phase.changeImpact]}`}>{phase.changeImpact} Impact</span>
                  <span className="text-gray-400 text-sm">{expandedPhase === phase.phaseId ? '▲' : '▼'}</span>
                </div>
              </button>
              {expandedPhase === phase.phaseId && (
                <div className="card-body grid grid-cols-3 gap-4 border-t border-gray-100">
                  {[
                    { label: 'Current State', color: 'gray',   icon: '👤', roles: phase.current    },
                    { label: 'Option A / B — AI-Augmented', color: 'blue',   icon: '🤝', roles: phase.augmented  },
                    { label: 'Option C — ADLC Autonomous',  color: 'emerald',icon: '🤖', roles: phase.autonomous },
                  ].map(col => (
                    <div key={col.label}>
                      <div className={`text-xs font-bold text-${col.color}-700 bg-${col.color}-50 px-3 py-1.5 rounded-lg mb-2`}>
                        {col.icon} {col.label}
                      </div>
                      <div className="space-y-1.5">
                        {col.roles.map((r, i) => (
                          <div key={i} className={`text-xs px-2.5 py-1.5 rounded-lg border ${
                            col.color === 'gray'   ? 'bg-gray-50 border-gray-200 text-gray-700' :
                            col.color === 'blue'   ? 'bg-blue-50 border-blue-200 text-blue-800' :
                            'bg-emerald-50 border-emerald-200 text-emerald-800'
                          }`}>{r}</div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* ── Change Management ── */}
      {activeTab === 'change' && (
        <div className="space-y-4">
          {/* Option selector */}
          <div className="flex gap-3">
            {Object.entries(OPTION_LABELS).map(([key, label]) => (
              <button key={key} onClick={() => setOption(key)}
                className={`flex-1 py-3 px-4 rounded-xl border-2 text-sm font-semibold transition-all ${
                  selectedOption === key
                    ? key === 'a' ? 'border-blue-500 bg-blue-50 text-blue-700' :
                      key === 'b' ? 'border-purple-500 bg-purple-50 text-purple-700' :
                                    'border-emerald-500 bg-emerald-50 text-emerald-700'
                    : 'border-gray-200 text-gray-500 hover:border-gray-300'
                }`}>
                {label}
              </button>
            ))}
          </div>

          {/* Change details */}
          {(() => {
            const opt = CHANGE_EFFORT[selectedOption]
            const color = OPTION_COLORS[selectedOption]
            return (
              <div className="space-y-4">
                <div className={`grid grid-cols-3 gap-4`}>
                  {[
                    { label: 'Change Effort',      value: opt.effort },
                    { label: 'Typical Duration',   value: opt.duration },
                    { label: 'Headcount Impact',   value: opt.headcountImpact },
                  ].map(m => (
                    <div key={m.label} className={`bg-${color}-50 border border-${color}-200 rounded-xl p-4`}>
                      <div className={`text-xs font-semibold text-${color}-500 mb-1`}>{m.label}</div>
                      <div className={`text-sm font-bold text-${color}-800`}>{m.value}</div>
                    </div>
                  ))}
                </div>

                <div className="card">
                  <div className="card-header">
                    <h3 className="font-bold text-gray-800">Key Change Management Activities</h3>
                  </div>
                  <div className="card-body space-y-2">
                    {opt.keyChanges.map((c, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <span className={`w-6 h-6 rounded-full bg-${color}-600 text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5`}>{i+1}</span>
                        <span className="text-sm text-gray-700">{c}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Phase impact summary */}
                <div className="card">
                  <div className="card-header">
                    <h3 className="font-bold text-gray-800">Role Change Impact by Phase</h3>
                  </div>
                  <div className="card-body p-0">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50 border-b border-gray-200">
                        <tr>
                          {['Phase', 'Current Roles', selectedOption === 'c' ? 'ADLC Roles' : 'Augmented Roles', 'Impact'].map(h => (
                            <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {PHASE_ROLES.map(p => (
                          <tr key={p.phaseId} className="hover:bg-gray-50 transition-colors">
                            <td className="px-4 py-3 text-xs font-semibold text-gray-700">{p.icon} {p.phase}</td>
                            <td className="px-4 py-3 text-xs text-gray-600">{p.current.length} roles</td>
                            <td className="px-4 py-3 text-xs text-gray-600">
                              {selectedOption === 'c' ? p.autonomous.length : p.augmented.length} roles
                            </td>
                            <td className="px-4 py-3">
                              <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${CHANGE_IMPACT_COLOR[p.changeImpact]}`}>{p.changeImpact}</span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )
          })()}
        </div>
      )}
    </div>
  )
}
