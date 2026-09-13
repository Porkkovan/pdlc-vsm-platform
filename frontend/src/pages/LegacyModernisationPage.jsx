import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'

// ─── Strategy definitions ─────────────────────────────────────────────────────
const STRATEGIES = {
  replatform:  { label: 'Re-platform',          color: 'blue',   icon: '☁️', desc: 'Lift & shift to modern cloud/container platform with minimal code changes. Low risk, moderate benefit.' },
  reengineer:  { label: 'AI-assisted Re-engineer', color: 'purple', icon: '🤖', desc: 'Incrementally re-engineer using AI agents to vectorise the codebase and suggest targeted refactors. Medium risk, high benefit.' },
  rewrite:     { label: 'Greenfield Rewrite',    color: 'green',  icon: '🌱', desc: 'Full rewrite leveraging modern stack and ADLC patterns. High risk, highest long-term benefit.' },
  maintain:    { label: 'Maintain & Extend',     color: 'emerald',  icon: '🔧', desc: 'Stabilise and extend with AI tooling for productivity gains. Low risk, low transformation benefit.' },
  decompose:   { label: 'Domain Decomposition',  color: 'indigo', icon: '🧩', desc: 'Break monolith into bounded domains via knowledge-graph-assisted decomposition. Medium risk, high benefit.' },
}

const STRATEGY_COLOR = {
  blue:   'bg-blue-100 text-blue-700 border-blue-200',
  purple: 'bg-purple-100 text-purple-700 border-purple-200',
  green:  'bg-green-100 text-green-700 border-green-200',
  amber:  'bg-cyan-100 text-cyan-700 border-cyan-200',
  indigo: 'bg-indigo-100 text-indigo-700 border-indigo-200',
}

const LANGUAGES = ['Java', 'COBOL', 'C/C++', 'C#/.NET', 'Python', 'Ruby', 'PHP', 'VB.NET', 'PL/SQL', 'JavaScript', 'Mainframe', 'Other']
const COUPLING_LABELS = { 1: 'Monolith', 2: 'Highly Coupled', 3: 'Moderate', 4: 'Loosely Coupled', 5: 'Microservices-ready' }

// Derive strategy from app profile
function deriveStrategy(app) {
  const age = parseInt(app.age) || 0
  const loc = parseInt(app.loc) || 0
  const coupling = parseInt(app.coupling) || 3
  if (app.language === 'COBOL' || app.language === 'Mainframe') return 'reengineer'
  if (age >= 15 && loc > 500000 && coupling <= 2) return 'decompose'
  if (age >= 10 && coupling <= 2) return 'reengineer'
  if (age >= 5 && coupling >= 4) return 'replatform'
  if (age < 5) return 'maintain'
  return 'reengineer'
}

// Knowledge graph readiness score (0–100)
function kgScore(app) {
  let score = 50
  const coupling = parseInt(app.coupling) || 3
  const age = parseInt(app.age) || 0
  const loc = parseInt(app.loc) || 0
  score += (coupling - 1) * 8        // higher coupling = harder to decompose
  score -= Math.min(age * 1.5, 25)   // older = harder
  score -= loc > 1000000 ? 20 : loc > 500000 ? 10 : 0
  if (app.hasTests) score += 15
  if (app.hasApiDocs) score += 10
  return Math.max(0, Math.min(100, Math.round(score)))
}

const KG_COLOR = (s) => s >= 70 ? 'bg-green-500' : s >= 40 ? 'bg-cyan-400' : 'bg-sky-400'
const KG_LABEL = (s) => s >= 70 ? 'High Readiness' : s >= 40 ? 'Medium Readiness' : 'Low Readiness'

const EMPTY_APP = { name: '', language: 'Java', age: '', loc: '', coupling: '3', hasTests: false, hasApiDocs: false, description: '' }

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function LegacyModernisationPage() {
  const { project } = useApp()
  const [apps, setApps]         = useState([])
  const [form, setForm]         = useState({ ...EMPTY_APP })
  const [showForm, setShowForm] = useState(false)
  const [activeTab, setActiveTab] = useState('inventory')
  const [editIdx, setEditIdx]   = useState(null)

  const saveApp = () => {
    if (!form.name.trim()) return
    if (editIdx !== null) {
      setApps(a => a.map((x, i) => i === editIdx ? { ...form } : x))
      setEditIdx(null)
    } else {
      setApps(a => [...a, { ...form }])
    }
    setForm({ ...EMPTY_APP })
    setShowForm(false)
  }

  const removeApp = (i) => setApps(a => a.filter((_, idx) => idx !== i))

  const editApp = (i) => {
    setForm({ ...apps[i] })
    setEditIdx(i)
    setShowForm(true)
  }

  const totalLoc = apps.reduce((n, a) => n + (parseInt(a.loc) || 0), 0)
  const avgKg    = apps.length ? Math.round(apps.reduce((n, a) => n + kgScore(a), 0) / apps.length) : 0

  const TABS = [
    { id: 'inventory',  label: '📦 App Inventory'          },
    { id: 'readiness',  label: '🧠 KG Readiness'           },
    { id: 'strategy',   label: '🗺️ Modernisation Strategy'  },
    { id: 'approach',   label: '📘 Approach & Methodology'  },
  ]

  return (
    <div className="space-y-6 fade-in">

      {/* Hero */}
      <div className="bg-gradient-to-r from-cyan-400 to-cyan-500 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">Legacy Modernisation</h2>
            <p className="text-teal-100 text-sm max-w-2xl">
              Assess your legacy application portfolio for AI-powered modernisation readiness.
              Reverse-engineer codebases into knowledge graphs, score decomposition readiness, and select the right modernisation strategy per application.
            </p>
            {project.organization && (
              <div className="mt-2 flex items-center gap-2 flex-wrap">
                <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">🏢 {project.organization}</span>
                {project.team && <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">👥 {project.team}</span>}
              </div>
            )}
          </div>
          <div className="flex gap-3 shrink-0">
            <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[80px]">
              <div className="text-2xl font-bold">{apps.length}</div>
              <div className="text-xs text-teal-200 mt-0.5">Apps Logged</div>
            </div>
            <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[80px]">
              <div className="text-2xl font-bold">{avgKg > 0 ? avgKg + '%' : '—'}</div>
              <div className="text-xs text-teal-200 mt-0.5">Avg KG Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 flex-wrap">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === t.id ? 'border-teal-500 text-teal-600' : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── App Inventory ── */}
      {activeTab === 'inventory' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-500">{apps.length === 0 ? 'Add your legacy applications to begin the modernisation assessment.' : `${apps.length} application${apps.length !== 1 ? 's' : ''} · ${(totalLoc / 1000).toFixed(0)}K total lines of code`}</p>
            <button onClick={() => { setForm({ ...EMPTY_APP }); setEditIdx(null); setShowForm(s => !s) }}
              className="btn-primary text-sm px-4 py-2">
              {showForm ? '✕ Cancel' : '+ Add Application'}
            </button>
          </div>

          {/* Add / Edit form */}
          {showForm && (
            <div className="card border-2 border-teal-200">
              <div className="card-header bg-teal-50">
                <h3 className="font-bold text-gray-800">{editIdx !== null ? 'Edit Application' : 'Add Legacy Application'}</h3>
              </div>
              <div className="card-body space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">Application Name *</label>
                    <input type="text" value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
                      placeholder="e.g., Core Banking System"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-400" />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">Primary Language</label>
                    <select value={form.language} onChange={e => setForm(f => ({ ...f, language: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-400">
                      {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">Application Age (years)</label>
                    <input type="number" value={form.age} onChange={e => setForm(f => ({ ...f, age: e.target.value }))}
                      placeholder="e.g., 15"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-400" />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">Lines of Code (approx)</label>
                    <input type="number" value={form.loc} onChange={e => setForm(f => ({ ...f, loc: e.target.value }))}
                      placeholder="e.g., 500000"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-400" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-xs font-semibold text-gray-700 mb-2">
                      Coupling Level — <span className="text-gray-500 font-normal">{COUPLING_LABELS[form.coupling]}</span>
                    </label>
                    <input type="range" min="1" max="5" value={form.coupling} onChange={e => setForm(f => ({ ...f, coupling: e.target.value }))}
                      className="w-full accent-orange-500" />
                    <div className="flex justify-between text-xs text-gray-400 mt-1">
                      <span>Monolith</span><span>Loosely Coupled</span>
                    </div>
                  </div>
                </div>
                <div className="flex gap-6">
                  <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                    <input type="checkbox" checked={form.hasTests} onChange={e => setForm(f => ({ ...f, hasTests: e.target.checked }))}
                      className="accent-orange-500" />
                    Has automated test suite
                  </label>
                  <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
                    <input type="checkbox" checked={form.hasApiDocs} onChange={e => setForm(f => ({ ...f, hasApiDocs: e.target.checked }))}
                      className="accent-orange-500" />
                    Has API / interface documentation
                  </label>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Brief Description (optional)</label>
                  <textarea value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                    placeholder="e.g., Core transaction processing system handling all payments..."
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 resize-none" />
                </div>
                <div className="flex gap-3">
                  <button onClick={saveApp} className="btn-primary flex-1">{editIdx !== null ? '💾 Update Application' : '+ Add Application'}</button>
                  <button onClick={() => { setShowForm(false); setEditIdx(null) }} className="btn-secondary flex-1">Cancel</button>
                </div>
              </div>
            </div>
          )}

          {/* App cards */}
          {apps.length === 0 && !showForm && (
            <div className="text-center py-16 text-gray-400">
              <div className="text-5xl mb-3">📦</div>
              <p className="text-sm font-medium">No applications added yet</p>
              <p className="text-xs mt-1">Click <strong>+ Add Application</strong> to begin your legacy portfolio assessment</p>
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {apps.map((app, i) => {
              const kg   = kgScore(app)
              const strat = deriveStrategy(app)
              const s    = STRATEGIES[strat]
              return (
                <div key={i} className="card hover:shadow-md transition-shadow">
                  <div className="card-body">
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <div>
                        <div className="font-bold text-gray-800">{app.name}</div>
                        <div className="text-xs text-gray-500">{app.language} · {app.age || '?'} yrs · {app.loc ? `${(parseInt(app.loc)/1000).toFixed(0)}K LOC` : 'LOC unknown'}</div>
                      </div>
                      <div className="flex gap-1">
                        <button onClick={() => editApp(i)} className="text-xs text-blue-500 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50 transition-colors">Edit</button>
                        <button onClick={() => removeApp(i)} className="text-xs text-sky-400 hover:text-sky-600 px-2 py-1 rounded hover:bg-sky-50 transition-colors">Remove</button>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 mb-3">
                      <div className="flex-1">
                        <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                          <span>KG Readiness</span>
                          <span className="font-semibold">{kg}% — {KG_LABEL(kg)}</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div className={`h-2 rounded-full ${KG_COLOR(kg)}`} style={{ width: `${kg}%` }} />
                        </div>
                      </div>
                    </div>
                    <div className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full border ${STRATEGY_COLOR[s.color]}`}>
                      <span>{s.icon}</span><span>{s.label}</span>
                    </div>
                    {app.description && <p className="text-xs text-gray-500 mt-2">{app.description}</p>}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* ── KG Readiness ── */}
      {activeTab === 'readiness' && (
        <div className="space-y-4">
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Knowledge Graph Readiness Scoring</h3>
              <p className="text-xs text-gray-500">Scores each app on how amenable it is to being reverse-engineered into a knowledge graph for AI-assisted transformation</p>
            </div>
            <div className="card-body space-y-4">
              <div className="grid grid-cols-3 gap-3 mb-2">
                {[
                  { label: 'High Readiness (≥70)', color: 'bg-green-500', desc: 'Proceed with AI-assisted vectorisation and KG extraction' },
                  { label: 'Medium (40–69)',        color: 'bg-cyan-400', desc: 'Pre-work required: document interfaces, add test coverage' },
                  { label: 'Low (<40)',             color: 'bg-sky-400',   desc: 'Stabilise first; manual knowledge extraction needed' },
                ].map(b => (
                  <div key={b.label} className="bg-gray-50 rounded-xl p-3 border border-gray-200">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`w-3 h-3 rounded-full ${b.color}`} />
                      <span className="text-xs font-bold text-gray-700">{b.label}</span>
                    </div>
                    <p className="text-xs text-gray-500">{b.desc}</p>
                  </div>
                ))}
              </div>
              {apps.length === 0 && (
                <div className="text-center py-10 text-gray-400">
                  <p className="text-sm">Add applications in the <strong>App Inventory</strong> tab to see readiness scores</p>
                </div>
              )}
              {apps.map((app, i) => {
                const kg = kgScore(app)
                return (
                  <div key={i} className="border border-gray-200 rounded-xl p-4">
                    <div className="flex items-center justify-between gap-4 mb-2">
                      <div className="font-semibold text-gray-800 text-sm">{app.name}</div>
                      <div className="flex items-center gap-2">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${kg >= 70 ? 'bg-green-100 text-green-700' : kg >= 40 ? 'bg-cyan-100 text-cyan-700' : 'bg-sky-100 text-sky-700'}`}>
                          {KG_LABEL(kg)}
                        </span>
                        <span className="text-sm font-bold text-gray-700">{kg}%</span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 mb-3">
                      <div className={`h-2.5 rounded-full transition-all ${KG_COLOR(kg)}`} style={{ width: `${kg}%` }} />
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                      {[
                        { label: 'Language', value: app.language },
                        { label: 'Coupling', value: COUPLING_LABELS[app.coupling] },
                        { label: 'Test Coverage', value: app.hasTests ? '✅ Present' : '❌ Missing' },
                        { label: 'API Docs', value: app.hasApiDocs ? '✅ Present' : '❌ Missing' },
                      ].map(f => (
                        <div key={f.label} className="bg-gray-50 rounded-lg p-2">
                          <div className="text-gray-400 mb-0.5">{f.label}</div>
                          <div className="font-semibold text-gray-700">{f.value}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {/* ── Modernisation Strategy ── */}
      {activeTab === 'strategy' && (
        <div className="space-y-4">
          {apps.length === 0 && (
            <div className="card">
              <div className="card-body text-center py-12 text-gray-400">
                <div className="text-4xl mb-3">🗺️</div>
                <p className="text-sm">Add applications in the <strong>App Inventory</strong> tab to generate strategy recommendations</p>
              </div>
            </div>
          )}
          {apps.length > 0 && (
            <>
              {/* Strategy summary cards */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {Object.entries(STRATEGIES).map(([key, s]) => {
                  const count = apps.filter(a => deriveStrategy(a) === key).length
                  if (!count) return null
                  return (
                    <div key={key} className={`rounded-xl p-4 border ${STRATEGY_COLOR[s.color]}`}>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xl">{s.icon}</span>
                        <span className="font-bold text-sm">{s.label}</span>
                      </div>
                      <div className="text-2xl font-bold mb-1">{count} app{count !== 1 ? 's' : ''}</div>
                      <p className="text-xs opacity-80">{s.desc}</p>
                    </div>
                  )
                })}
              </div>

              {/* Per-app strategy table */}
              <div className="card">
                <div className="card-header">
                  <h3 className="font-bold text-gray-800">Per-Application Strategy</h3>
                </div>
                <div className="card-body p-0">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 border-b border-gray-200">
                      <tr>
                        {['Application', 'Language', 'Age / LOC', 'KG Score', 'Recommended Strategy', 'Next Step'].map(h => (
                          <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {apps.map((app, i) => {
                        const kg = kgScore(app)
                        const strat = deriveStrategy(app)
                        const s = STRATEGIES[strat]
                        const nextStep = kg >= 70
                          ? 'Begin vectorisation pipeline'
                          : kg >= 40
                          ? 'Improve test coverage, document APIs'
                          : 'Manual knowledge extraction workshop'
                        return (
                          <tr key={i} className="hover:bg-gray-50 transition-colors">
                            <td className="px-4 py-3 font-semibold text-gray-800 text-xs">{app.name}</td>
                            <td className="px-4 py-3 text-xs text-gray-600">{app.language}</td>
                            <td className="px-4 py-3 text-xs text-gray-600">{app.age || '?'} yrs · {app.loc ? `${(parseInt(app.loc)/1000).toFixed(0)}K` : '?'} LOC</td>
                            <td className="px-4 py-3">
                              <div className="flex items-center gap-2">
                                <div className="w-16 bg-gray-200 rounded-full h-1.5">
                                  <div className={`h-1.5 rounded-full ${KG_COLOR(kg)}`} style={{ width: `${kg}%` }} />
                                </div>
                                <span className="text-xs font-semibold text-gray-700">{kg}%</span>
                              </div>
                            </td>
                            <td className="px-4 py-3">
                              <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${STRATEGY_COLOR[s.color]}`}>{s.icon} {s.label}</span>
                            </td>
                            <td className="px-4 py-3 text-xs text-gray-600">{nextStep}</td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── Approach & Methodology ── */}
      {activeTab === 'approach' && (
        <div className="space-y-4">
          {[
            {
              step: 1, icon: '🔍', title: 'Codebase Discovery & Vectorisation',
              color: 'blue',
              desc: 'Reverse-engineer legacy codebases by parsing source files, extracting entities, dependencies, and data flows. Chunk and embed the codebase into a vector store — creating an enterprise knowledge store that AI agents can query safely without reading millions of lines of code directly.',
              actions: ['Clone and parse repository structure', 'Extract class/method/dependency graph', 'Chunk into semantic units (500–2000 tokens)', 'Embed into vector store (pgvector / Pinecone)', 'Build Knowledge Graph of domain entities'],
            },
            {
              step: 2, icon: '🧩', title: 'Domain Boundary Identification',
              color: 'purple',
              desc: 'Use the knowledge graph to identify natural domain boundaries and coupling hotspots. AI agents analyse dependency clusters to suggest decomposition points — enabling safer incremental refactoring without full rewrites.',
              actions: ['Identify tightly-coupled modules', 'Map domain events and bounded contexts', 'Score decomposition risk per module', 'Propose strangler-fig extraction sequence', 'Define API contracts for extracted domains'],
            },
            {
              step: 3, icon: '🤖', title: 'AI-Assisted Incremental Re-engineering',
              color: 'green',
              desc: 'Apply targeted AI-driven refactoring using the knowledge graph as context. AI agents propose specific code changes with full traceability — humans review and approve each change before it enters the CI/CD pipeline.',
              actions: ['Generate refactoring proposals per module', 'Human review and approval gate', 'AI-generated unit tests for changed code', 'Automated regression testing via CI', 'Incremental deployment with feature flags'],
            },
            {
              step: 4, icon: '📊', title: 'Continuous Modernisation Metrics',
              color: 'emerald',
              desc: 'Track modernisation progress using VSM metrics. Each extracted domain shows improved flow efficiency and reduced lead time. Link directly to the Current State VSM to see before/after transformation impact.',
              actions: ['Track LOC migrated per sprint', 'Measure flow efficiency improvement per domain', 'Monitor test coverage increase', 'DORA metric improvement per extracted service', 'Link to STUMP VSM for end-to-end view'],
            },
          ].map(step => (
            <div key={step.step} className="card">
              <div className={`card-header bg-${step.color}-50 border-b border-${step.color}-100`}>
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 bg-${step.color}-600 text-white rounded-full flex items-center justify-center font-bold text-sm shrink-0`}>{step.step}</div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xl">{step.icon}</span>
                      <h3 className={`font-bold text-${step.color}-800`}>{step.title}</h3>
                    </div>
                  </div>
                </div>
              </div>
              <div className="card-body">
                <p className="text-sm text-gray-600 mb-4">{step.desc}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {step.actions.map((a, i) => (
                    <div key={i} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="text-green-500 mt-0.5 shrink-0">→</span>
                      <span>{a}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
          <div className="bg-teal-50 border border-teal-200 rounded-xl p-4 text-sm text-teal-800">
            💡 Link your legacy app modernisation progress to <Link to="/future-state" className="font-semibold underline">Future State VSM</Link> to model how each extracted domain improves your PDLC flow efficiency.
          </div>
        </div>
      )}
    </div>
  )
}
