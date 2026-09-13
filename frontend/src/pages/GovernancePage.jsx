import { useState } from 'react'
import { useApp } from '../contexts/AppContext'

// ─── Static data ──────────────────────────────────────────────────────────────
const AGENTS_MATRIX = [
  // Data Layer
  { id: 'alm-connector',       name: 'ALM Connector',             icon: '🔗', layer: 'Data',         pdlcPhase: 'Phase 1',             action: 'Pulls work-item data from ALM tools (read-only)',                    owner: 'Engineering Lead',              risk: 'Low',    feedsInto: 'VSM Analyzer, Bottleneck Analyzer' },
  // Analysis Layer
  { id: 'vsm-analyzer',        name: 'VSM Analyzer',              icon: '🗺️', layer: 'Analysis',     pdlcPhase: 'Phase 2',             action: 'Calculates PT, WT, LT and Flow Efficiency per phase',                owner: 'VSM Coach / Lean Lead',         risk: 'Low',    feedsInto: 'Bottleneck Analyzer, Future State Designer' },
  { id: 'bottleneck-analyzer', name: 'Bottleneck Analyzer',       icon: '⚠️', layer: 'Analysis',     pdlcPhase: 'Phase 5',             action: 'Identifies waste and bottlenecks across all PDLC phases',            owner: 'Engineering Manager',           risk: 'Medium', feedsInto: 'Improvement Generator, Business Case Builder' },
  { id: 'benchmark-agent',     name: 'Benchmark Agent',           icon: '📊', layer: 'Analysis',     pdlcPhase: 'Phase 6',             action: 'Compares team metrics against industry p75 benchmarks',             owner: 'CTO / VP Engineering',          risk: 'Low',    feedsInto: 'Improvement Generator, Business Case Builder' },
  // Output Layer
  { id: 'improvement-gen',     name: 'Improvement Generator',     icon: '🚀', layer: 'Output',       pdlcPhase: 'Phase 3',             action: 'Generates AI-powered improvement and automation recommendations',     owner: 'Product Owner + Eng Lead',      risk: 'Medium', feedsInto: 'Future State Designer, Business Case Builder' },
  { id: 'future-state',        name: 'Future State Designer',     icon: '🔮', layer: 'Output',       pdlcPhase: 'Phase 7',             action: 'Designs future-state VSM scenarios (Options A / B / C)',             owner: 'CTO + Transformation Lead',     risk: 'High',   feedsInto: 'Business Case Builder' },
  { id: 'business-case',       name: 'Business Case Builder',     icon: '💼', layer: 'Output',       pdlcPhase: 'Phase 6',             action: 'Calculates ROI, investment ranges and payback projections',          owner: 'CFO / Finance BP',              risk: 'High',   feedsInto: '—' },
  { id: 'telemetry-sentinel',  name: 'Telemetry Sentinel',        icon: '📡', layer: 'Output',       pdlcPhase: 'Phase 7 + cross',     action: 'Aggregates multi-agent logs; translates failures into Business Risk Scores for governance teams', owner: 'VP Engineering / CTO',   risk: 'Medium', feedsInto: 'Governance Controller' },
  // Governance Layer
  { id: 'secure-by-design',    name: 'Secure-by-Design Architect', icon: '🔐', layer: 'Governance',  pdlcPhase: 'Phase 2 + Phase 6',   action: 'Auto-rejects IaC and deployment configs deviating from cloud architecture or security baseline', owner: 'CISO / Cloud Architect',  risk: 'High',   feedsInto: 'Governance Controller, Telemetry Sentinel' },
  { id: 'cac-orchestrator',    name: 'CaC Orchestrator',          icon: '📋', layer: 'Governance',   pdlcPhase: 'Phase 3 + Phase 5',   action: 'Validates every code commit and model update against GDPR, DORA, Basel III in real-time', owner: 'Chief Compliance Officer',    risk: 'High',   feedsInto: 'Governance Controller, Telemetry Sentinel' },
  { id: 'mrm-agent',           name: 'MRM Agent',                 icon: '🧬', layer: 'Governance',   pdlcPhase: 'Phase 5 + Phase 7',   action: 'Generates Explainability Reports; triggers kill-switch if model drift exceeds governed risk parameters', owner: 'Model Risk Officer / CRO', risk: 'High',  feedsInto: 'Governance Controller, Telemetry Sentinel' },
  // Orchestration Layer
  { id: 'orchestrator',        name: 'Orchestrator',              icon: '🎭', layer: 'Orchestration', pdlcPhase: 'Phase 1 + Phase 4',  action: 'Coordinates all delivery agents across the end-to-end pipeline via LangGraph StateGraph', owner: 'Platform Engineering Lead', risk: 'High',   feedsInto: 'All delivery agents' },
  { id: 'governance-controller',name: 'Governance Controller',   icon: '🏛️', layer: 'Orchestration', pdlcPhase: 'All phases',          action: 'Orchestrates all 13 agents; enforces workflow permissions, hand-offs, and protocol compliance at enterprise scale', owner: 'Platform Lead + CTO', risk: 'High',  feedsInto: 'All agents' },
]

const LAYER_BADGE = {
  Data:          'bg-blue-100 text-blue-700',
  Analysis:      'bg-purple-100 text-purple-700',
  Output:        'bg-green-100 text-green-700',
  Governance:    'bg-indigo-100 text-indigo-700',
  Orchestration: 'bg-gray-200 text-gray-700',
}

const GUARDRAIL_DEFS = [
  { id: 'human-review',        label: 'Require human review before persisting any AI-generated results',             defaultOn: true,  category: 'Accountability' },
  { id: 'audit-logging',       label: 'Enable full audit logging of all AI agent actions and decisions',             defaultOn: true,  category: 'Accountability' },
  { id: 'block-auto-deploy',   label: 'Block autonomous deployment recommendations without CTO sign-off',            defaultOn: true,  category: 'Safety'         },
  { id: 'confidence-gate',     label: 'Only surface AI suggestions with ≥ 75% confidence score',                    defaultOn: true,  category: 'Quality'        },
  { id: 'data-residency',      label: 'Enforce data residency — no PII transmitted to external AI APIs',             defaultOn: true,  category: 'Privacy'        },
  { id: 'readonly-alm',        label: 'Restrict ALM Connector to read-only; disable write-back capabilities',        defaultOn: true,  category: 'Safety'         },
  { id: 'rate-limit',          label: 'Rate-limit agent runs to prevent runaway API cost accumulation',              defaultOn: false, category: 'Cost'           },
  { id: 'explainability',      label: 'Require explainability notes for every AI recommendation surfaced',           defaultOn: false, category: 'Transparency'   },
  { id: 'rollback',            label: 'Create rollback checkpoint before each major AI-driven transformation change', defaultOn: false, category: 'Safety'         },
  { id: 'drift-alerts',        label: 'Alert when AI model output distribution drifts > 15% from baseline',          defaultOn: false, category: 'Quality'        },
  { id: 'secure-by-design-gate', label: 'Block all IaC deployments that fail Secure-by-Design Architect validation',  defaultOn: true,  category: 'Safety'         },
  { id: 'compliance-as-code',  label: 'Enforce Compliance-as-Code checks on every code commit (GDPR, DORA, Basel III)', defaultOn: true, category: 'Accountability' },
  { id: 'mrm-kill-switch',     label: 'Enable MRM Agent automated kill-switch when model drift exceeds risk threshold', defaultOn: true, category: 'Safety'         },
  { id: 'biz-risk-score',      label: 'Surface Business Risk Scores from Telemetry Sentinel to governance dashboard',  defaultOn: false, category: 'Transparency'   },
  { id: 'governance-controller-log', label: 'Log all Multi-Agent Governance Controller orchestration decisions for audit', defaultOn: true, category: 'Accountability' },
]

const AUDIT_LOG = [
  { ts: '2026-04-03 09:14', agent: 'Bottleneck Analyzer',   action: 'Generated 8 bottleneck recommendations',          user: 'John Smith', decision: 'Accepted',       items: 6    },
  { ts: '2026-04-02 16:48', agent: 'DORA Assessment',       action: 'AI auto-scored 4 core DORA metrics',               user: 'Jane Lee',   decision: 'Partial Accept', items: 3    },
  { ts: '2026-04-02 14:05', agent: 'Future State Designer', action: 'Generated Option B future-state VSM',              user: 'John Smith', decision: 'Under Review',   items: null },
  { ts: '2026-04-01 16:45', agent: 'Business Case Builder', action: 'Calculated ROI projections for Option A',          user: 'Mary Chen',  decision: 'Accepted',       items: null },
  { ts: '2026-04-01 11:12', agent: 'Improvement Generator', action: 'Proposed 12 improvement initiatives',             user: 'John Smith', decision: 'Accepted',       items: 9    },
  { ts: '2026-03-31 15:20', agent: 'VSM Analyzer',          action: 'Recalculated flow efficiency across 7 phases',     user: 'Jane Lee',   decision: 'Accepted',       items: null },
  { ts: '2026-03-30 10:33', agent: 'Benchmark Agent',       action: 'Compared metrics against p75 banking benchmarks', user: 'Mary Chen',  decision: 'Accepted',       items: null },
]

const RI_FRAMEWORK = [
  { category: 'Transparency', icon: '🔍', items: [
    { label: 'AI model and version documented for each agent',                done: true  },
    { label: 'Prompt templates version-controlled and auditable',            done: true  },
    { label: 'Confidence scores displayed for all AI suggestions',           done: true  },
    { label: 'Source evidence provided for each recommendation',             done: true  },
    { label: 'Explainability report available on demand per agent run',      done: false },
  ]},
  { category: 'Accountability', icon: '👤', items: [
    { label: 'Human owner assigned to every AI agent',                      done: true  },
    { label: 'All AI decisions logged with user attribution',               done: true  },
    { label: 'Escalation path defined for rejected AI suggestions',         done: false },
    { label: 'Quarterly AI performance review process established',         done: false },
    { label: 'Agent output quality SLA defined and measured',               done: false },
  ]},
  { category: 'Fairness & Bias', icon: '⚖️', items: [
    { label: 'Benchmark datasets reviewed for industry bias',               done: false },
    { label: 'Recommendations validated across org sizes and industries',   done: false },
    { label: 'AI suggestions reviewed for team / role bias',                done: false },
    { label: 'Diversity of training and benchmark data documented',         done: false },
  ]},
  { category: 'Security & Privacy', icon: '🔒', items: [
    { label: 'No PII transmitted to external LLM APIs',                     done: true  },
    { label: 'API tokens stored in secrets manager (not plain text)',       done: true  },
    { label: 'Data encryption in transit and at rest confirmed',            done: true  },
    { label: 'Penetration testing completed on all API endpoints',          done: false },
    { label: 'Access controls and RBAC enforced per data sensitivity level',done: false },
  ]},
  { category: 'Model Risk & Compliance', icon: '🧬', items: [
    { label: 'MRM Agent Explainability Report generated for every model version in production', done: false },
    { label: 'Compliance-as-Code validations covering GDPR, DORA, and Basel III active',       done: false },
    { label: 'Secure-by-Design Architect blocking non-compliant IaC on all environments',      done: false },
    { label: 'MRM kill-switch tested and dual-authorisation process documented',               done: false },
    { label: 'Governance Controller orchestration audit trail reviewed quarterly',             done: false },
    { label: 'Business Risk Scores from Telemetry Sentinel reported to governance board',      done: false },
  ]},
]

const RISK_COLOR    = { Low: 'bg-green-100 text-green-700', Medium: 'bg-cyan-100 text-cyan-700', High: 'bg-sky-100 text-sky-700' }
const DECISION_COLOR = { 'Accepted': 'bg-green-100 text-green-700', 'Partial Accept': 'bg-blue-100 text-blue-700', 'Under Review': 'bg-cyan-100 text-cyan-700', 'Rejected': 'bg-sky-100 text-sky-700' }
const CAT_COLOR     = { Accountability: 'bg-blue-100 text-blue-700', Safety: 'bg-sky-100 text-sky-700', Quality: 'bg-purple-100 text-purple-700', Privacy: 'bg-teal-100 text-teal-700', Cost: 'bg-teal-100 text-teal-700', Transparency: 'bg-indigo-100 text-indigo-700' }

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function GovernancePage() {
  const { project } = useApp()
  const [guardrails, setGuardrails] = useState(
    Object.fromEntries(GUARDRAIL_DEFS.map(g => [g.id, g.defaultOn]))
  )
  const [activeTab, setActiveTab] = useState('matrix')

  const enabledCount = Object.values(guardrails).filter(Boolean).length
  const riItems   = RI_FRAMEWORK.flatMap(c => c.items)
  const riDone    = riItems.filter(i => i.done).length
  const riPct     = Math.round(riDone / riItems.length * 100)

  const toggleGuardrail = (id) => setGuardrails(g => ({ ...g, [id]: !g[id] }))

  const TABS = [
    { id: 'matrix',     label: '🤖 Agent Accountability' },
    { id: 'guardrails', label: '🛡️ Guardrails'           },
    { id: 'audit',      label: '📋 Audit Log'             },
    { id: 'ri',         label: '⚖️ Responsible AI'        },
  ]

  return (
    <div className="space-y-6 fade-in">

      {/* Hero */}
      <div className="bg-gradient-to-r from-slate-700 to-gray-900 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">Governance & Guardrails</h2>
            <p className="text-gray-300 text-sm max-w-2xl">
              Responsible AI framework — agent accountability matrix, configurable platform guardrails, full audit trail,
              and enterprise compliance scorecard. AI agents are treated as junior developers; humans remain accountable for all decisions.
            </p>
            {project.organization && (
              <div className="mt-2 flex items-center gap-2 flex-wrap">
                <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">🏢 {project.organization}</span>
                {project.team && <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">👥 {project.team}</span>}
              </div>
            )}
          </div>
          <div className="flex gap-3 shrink-0">
            <div className="bg-white/10 rounded-xl px-4 py-3 text-center min-w-[80px]">
              <div className="text-2xl font-bold">{enabledCount}<span className="text-sm text-gray-400">/{GUARDRAIL_DEFS.length}</span></div>
              <div className="text-xs text-gray-400 mt-0.5">Guardrails On</div>
            </div>
            <div className={`rounded-xl px-4 py-3 text-center min-w-[80px] ${riPct >= 70 ? 'bg-green-500/40' : riPct >= 40 ? 'bg-cyan-500/40' : 'bg-sky-500/40'}`}>
              <div className="text-2xl font-bold">{riPct}%</div>
              <div className="text-xs text-gray-400 mt-0.5">RI Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === t.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── Agent Accountability Matrix ── */}
      {activeTab === 'matrix' && (
        <div className="card">
          <div className="card-header">
            <h3 className="font-bold text-gray-800">AI Agent Accountability Matrix — All 13 Agents</h3>
            <p className="text-xs text-gray-500">Every agent has a designated human owner. Delivery, governance, and orchestration agents are shown as one unified system.</p>
          </div>
          <div className="card-body p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    {['Agent', 'Layer', 'PDLC Phase', 'Human Owner', 'Risk Tier', 'Feeds Into'].map(h => (
                      <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {AGENTS_MATRIX.map(a => (
                    <tr key={a.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">{a.icon}</span>
                          <span className="text-xs font-semibold text-gray-800">{a.name}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${LAYER_BADGE[a.layer] || 'bg-gray-100 text-gray-600'}`}>{a.layer}</span>
                      </td>
                      <td className="px-4 py-3 text-xs text-gray-600 whitespace-nowrap">{a.pdlcPhase}</td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className="text-xs font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-full">{a.owner}</span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${RISK_COLOR[a.risk]}`}>{a.risk}</span>
                      </td>
                      <td className="px-4 py-3 text-xs text-gray-500 max-w-[160px]">{a.feedsInto}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="px-4 py-3 border-t border-gray-100 bg-gray-50 rounded-b-xl">
            <div className="flex flex-wrap gap-3 text-xs mb-2">
              {Object.entries(LAYER_BADGE).map(([layer, cls]) => (
                <span key={layer} className={`px-2 py-0.5 rounded-full font-semibold ${cls}`}>{layer}</span>
              ))}
            </div>
            <p className="text-xs text-gray-500">
              ℹ️ Risk tiers: <span className="font-semibold text-green-700">Low</span> = informational outputs only ·
              <span className="font-semibold text-cyan-700"> Medium</span> = recommendations affecting team planning ·
              <span className="font-semibold text-sky-700"> High</span> = financial, architectural, deployment, or compliance decisions
            </p>
          </div>
        </div>
      )}

      {/* ── Guardrails ── */}
      {activeTab === 'guardrails' && (
        <div className="space-y-4">
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Platform Guardrails</h3>
              <p className="text-xs text-gray-500">Governance policies applied across all AI agents and platform workflows — changes take effect immediately</p>
            </div>
            <div className="card-body space-y-2">
              {GUARDRAIL_DEFS.map(g => (
                <div key={g.id} className={`flex items-center justify-between gap-4 p-4 rounded-xl border transition-all ${
                  guardrails[g.id] ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                }`}>
                  <div className="flex items-center gap-3 min-w-0">
                    <span className={`shrink-0 w-2 h-2 rounded-full ${guardrails[g.id] ? 'bg-green-500' : 'bg-gray-300'}`} />
                    <span className={`text-sm ${guardrails[g.id] ? 'text-gray-800 font-medium' : 'text-gray-500'}`}>{g.label}</span>
                    <span className={`shrink-0 text-xs font-semibold px-2 py-0.5 rounded-full ${CAT_COLOR[g.category] || 'bg-gray-100 text-gray-600'}`}>{g.category}</span>
                  </div>
                  <button onClick={() => toggleGuardrail(g.id)}
                    className={`relative shrink-0 w-11 h-6 rounded-full transition-colors ${guardrails[g.id] ? 'bg-green-500' : 'bg-gray-300'}`}>
                    <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform duration-200 ${guardrails[g.id] ? 'translate-x-5' : 'translate-x-0.5'}`} />
                  </button>
                </div>
              ))}
            </div>
            <div className="px-4 py-3 border-t border-gray-100 bg-blue-50 rounded-b-xl">
              <p className="text-sm text-blue-800 font-medium">
                {enabledCount} of {GUARDRAIL_DEFS.length} guardrails active
                {enabledCount < 6 && ' — consider enabling more guardrails for enterprise deployments'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ── Audit Log ── */}
      {activeTab === 'audit' && (
        <div className="card">
          <div className="card-header flex items-center justify-between">
            <div>
              <h3 className="font-bold text-gray-800">AI Action Audit Log</h3>
              <p className="text-xs text-gray-500">Complete trail of AI recommendations generated, reviewed, and accepted or overridden by users</p>
            </div>
            <span className="text-xs bg-gray-100 text-gray-600 px-3 py-1 rounded-full font-semibold">{AUDIT_LOG.length} entries</span>
          </div>
          <div className="card-body p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    {['Timestamp', 'Agent', 'Action', 'Reviewed By', 'Decision'].map(h => (
                      <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {AUDIT_LOG.map((e, i) => (
                    <tr key={i} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-xs text-gray-500 whitespace-nowrap">{e.ts}</td>
                      <td className="px-4 py-3 text-xs font-semibold text-gray-700 whitespace-nowrap">{e.agent}</td>
                      <td className="px-4 py-3 text-xs text-gray-600">{e.action}{e.items != null ? ` (${e.items} items)` : ''}</td>
                      <td className="px-4 py-3 text-xs text-gray-600 whitespace-nowrap">{e.user}</td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${DECISION_COLOR[e.decision]}`}>{e.decision}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ── Responsible AI Scorecard ── */}
      {activeTab === 'ri' && (
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-slate-600 to-slate-900 rounded-2xl p-5 text-white flex items-center justify-between gap-4 flex-wrap">
            <div>
              <div className="font-bold text-lg">Responsible AI Scorecard</div>
              <div className="text-gray-300 text-sm">Enterprise governance across Transparency, Accountability, Fairness, and Security</div>
            </div>
            <div className="text-right shrink-0">
              <div className={`text-4xl font-bold ${riPct >= 70 ? 'text-green-400' : riPct >= 40 ? 'text-cyan-400' : 'text-sky-400'}`}>{riPct}%</div>
              <div className="text-xs text-gray-400">{riDone} of {riItems.length} checks passed</div>
            </div>
          </div>

          {RI_FRAMEWORK.map(cat => {
            const catDone = cat.items.filter(i => i.done).length
            const catPct  = Math.round(catDone / cat.items.length * 100)
            return (
              <div key={cat.category} className="card">
                <div className="card-header flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{cat.icon}</span>
                    <h3 className="font-bold text-gray-800">{cat.category}</h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-gray-200 rounded-full h-1.5">
                      <div className={`h-1.5 rounded-full ${catPct === 100 ? 'bg-green-500' : catPct >= 50 ? 'bg-cyan-400' : 'bg-sky-400'}`}
                        style={{ width: `${catPct}%` }} />
                    </div>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${catPct === 100 ? 'bg-green-100 text-green-700' : 'bg-cyan-100 text-cyan-700'}`}>
                      {catDone}/{cat.items.length}
                    </span>
                  </div>
                </div>
                <div className="card-body space-y-2">
                  {cat.items.map((item, i) => (
                    <div key={i} className={`flex items-center gap-3 p-3 rounded-lg ${item.done ? 'bg-green-50 border border-green-100' : 'bg-gray-50 border border-gray-100'}`}>
                      <span className="text-lg shrink-0">{item.done ? '✅' : '⬜'}</span>
                      <span className={`text-sm flex-1 ${item.done ? 'text-gray-800' : 'text-gray-500'}`}>{item.label}</span>
                      {!item.done && <span className="text-xs text-cyan-600 font-semibold shrink-0 bg-cyan-50 px-2 py-0.5 rounded-full">Action needed</span>}
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
