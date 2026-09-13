import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'

// ─── Static data ──────────────────────────────────────────────────────────────
const VALIDATION_GATES = [
  {
    agent: 'ALM Connector Agent', icon: '🔗',
    gates: [
      { label: 'Data schema validated against expected ALM API contract',               status: 'pass'    },
      { label: 'Null / empty field handling tested across all ALM tool types',          status: 'pass'    },
      { label: 'Rate limit and pagination edge cases covered',                          status: 'warning' },
      { label: 'Data freshness SLA defined (max staleness for cached data)',            status: 'fail'    },
    ],
  },
  {
    agent: 'VSM Analyzer Agent', icon: '🗺️',
    gates: [
      { label: 'Flow efficiency calculation validated against known-good datasets',     status: 'pass'    },
      { label: 'Edge cases tested: zero wait time, missing phases, single activity',   status: 'pass'    },
      { label: 'Metric units consistent (hours vs days) across all output fields',     status: 'pass'    },
      { label: 'Results reproducible given same input data',                           status: 'pass'    },
    ],
  },
  {
    agent: 'Bottleneck Analyzer', icon: '⚠️',
    gates: [
      { label: 'Bottleneck severity thresholds calibrated against industry benchmarks', status: 'pass'    },
      { label: 'Phase classification tested for all 7 PDLC phases',                   status: 'pass'    },
      { label: 'False positive rate measured and within acceptable range (< 15%)',     status: 'warning' },
      { label: 'Recommendations do not contain hallucinated phase references',         status: 'pass'    },
    ],
  },
  {
    agent: 'Improvement Generator', icon: '🚀',
    gates: [
      { label: 'Recommendations grounded in provided context documents (RAG)',         status: 'pass'    },
      { label: 'Source attribution present for all AI-generated suggestions',          status: 'pass'    },
      { label: 'Output tested for bias toward specific vendors or tools',              status: 'warning' },
      { label: 'Hallucination rate assessed via human evaluation sample',              status: 'fail'    },
    ],
  },
  {
    agent: 'Future State Designer', icon: '🔮',
    gates: [
      { label: 'Scenario projections benchmarked against industry case studies',       status: 'pass'    },
      { label: 'Conservative / expected / optimistic ranges clearly differentiated',  status: 'pass'    },
      { label: 'Automation percentages validated against DORA research data',         status: 'pass'    },
      { label: 'Human role definitions reviewed by domain SMEs',                      status: 'warning' },
    ],
  },
  {
    agent: 'Business Case Builder', icon: '💼',
    gates: [
      { label: 'ROI calculations peer-reviewed by Finance for methodology accuracy',  status: 'fail'    },
      { label: 'Investment ranges validated against real programme delivery data',    status: 'pass'    },
      { label: 'Sensitivity analysis included for key assumptions',                  status: 'fail'    },
      { label: 'Currency and cost normalisation applied for cross-geography use',    status: 'warning' },
    ],
  },
  // ── Option B/C — Compliance & Governance Agent Gates ──────────────────────────
  {
    agent: 'Secure-by-Design Architect (Option B/C)', icon: '🔐',
    gates: [
      { label: 'IaC rejection rules validated against cloud architecture standards (AWS Well-Architected / CIS Benchmarks)', status: 'warning' },
      { label: 'Security baseline policies version-controlled and auditable',                                                status: 'pass'    },
      { label: 'Override workflow tested: CISO approval path documented and functional',                                    status: 'fail'    },
      { label: 'Rejection false-positive rate measured and below 5%',                                                       status: 'warning' },
    ],
  },
  {
    agent: 'Compliance-as-Code Orchestrator (Option B/C)', icon: '📋',
    gates: [
      { label: 'GDPR Article 25 (privacy by design) rules encoded and tested against sample commits',   status: 'warning' },
      { label: 'DORA regulation checks implemented: incident reporting, ICT risk, third-party controls', status: 'fail'    },
      { label: 'Basel III capital requirement rules validated with compliance SME sign-off',             status: 'fail'    },
      { label: 'Audit trail retention tested: 7-year log archival confirmed for regulated entities',    status: 'warning' },
      { label: 'Real-time validation latency tested: must not block CI pipelines by > 30 seconds',     status: 'pass'    },
    ],
  },
  {
    agent: 'Model Risk Management (MRM) Agent (Option B/C)', icon: '🧬',
    gates: [
      { label: 'Explainability Report generated and reviewed for at least 3 model versions in staging', status: 'fail'    },
      { label: 'Bias detection coverage: minimum 5 protected attributes tested per model',              status: 'fail'    },
      { label: 'Drift detection threshold calibrated: kill-switch fires at correct performance delta',  status: 'warning' },
      { label: 'Kill-switch dual-authorisation workflow tested end-to-end (MRO + CTO sign-off)',        status: 'fail'    },
      { label: 'Model versioning schema documented; every report linked to a specific model hash',      status: 'pass'    },
    ],
  },
  {
    agent: 'Multi-Agent Governance Controller (Option B/C)', icon: '🏛️',
    gates: [
      { label: 'Agent bypass detection tested: no agent can execute without Governance Controller approval', status: 'warning' },
      { label: 'Orchestration audit log captures all agent hand-offs with timestamps and decision context',  status: 'pass'    },
      { label: 'Protocol enforcement tested: governance agents (security, compliance) block dev agent actions when required', status: 'warning' },
      { label: 'Controller config change process documented: CTO + CCO dual approval tested',               status: 'fail'    },
      { label: 'Enterprise scaling tested: controller maintains consistency with 10+ concurrent agent runs', status: 'fail'    },
    ],
  },
]

const BIAS_CHECKS = [
  { category: 'Industry Bias',       icon: '🏭', desc: 'Recommendations over-index toward specific sectors (e.g., Banking)', risk: 'Medium', mitigated: false },
  { category: 'Tool Vendor Bias',    icon: '🛠️', desc: 'AI suggests specific vendor products not explicitly in the playbook', risk: 'Low',    mitigated: true  },
  { category: 'Team Size Bias',      icon: '👥', desc: 'Models trained on large enterprise data; small team applicability varies', risk: 'Medium', mitigated: false },
  { category: 'Recency Bias',        icon: '📅', desc: 'Benchmark data may not reflect latest tooling or methodology advances', risk: 'Low',    mitigated: false },
  { category: 'Output Length Bias',  icon: '📝', desc: 'LLMs tend to produce longer recommendations regardless of quality', risk: 'Low',    mitigated: true  },
  { category: 'Confirmation Bias',   icon: '✅', desc: 'Agent may reinforce the user\'s existing direction rather than challenge it', risk: 'High',   mitigated: false },
  // MRM Agent-specific bias/drift entries
  { category: 'Model Explainability Gap', icon: '🧬', desc: 'MRM Agent: AI model decisions lack sufficient explainability for regulated financial services audit requirements', risk: 'High',   mitigated: false },
  { category: 'Protected Attribute Bias', icon: '⚖️', desc: 'MRM Agent: Models may encode bias across age, gender, or geography — systematic bias detection required per model version', risk: 'High',   mitigated: false },
  { category: 'Governance Bypass Risk',   icon: '🏛️', desc: 'Governance Controller: A misconfigured agent orchestration could allow a dev agent to execute without compliance sign-off', risk: 'High',   mitigated: false },
]

const QUALITY_METRICS = [
  { agent: 'VSM Analyzer',       accuracy: 94, precision: 97, hallucination: 2,  citation: 100 },
  { agent: 'Bottleneck Analyzer',accuracy: 87, precision: 91, hallucination: 5,  citation: 92  },
  { agent: 'Improvement Gen.',   accuracy: 79, precision: 84, hallucination: 9,  citation: 88  },
  { agent: 'Future State',       accuracy: 82, precision: 86, hallucination: 7,  citation: 95  },
  { agent: 'Business Case',      accuracy: 76, precision: 80, hallucination: 8,  citation: 83  },
  { agent: 'Benchmark Agent',    accuracy: 91, precision: 94, hallucination: 3,  citation: 99  },
]

const TESTING_FOR_AI = [
  {
    area: 'Functional Correctness', icon: '✅', color: 'green',
    tests: [
      'Golden dataset tests: known inputs → verify expected VSM metric outputs',
      'Regression suite: 50+ curated test cases run on every agent update',
      'Edge case library: empty data, extreme values, malformed inputs',
      'Cross-phase consistency: ensure metrics are coherent across all 7 phases',
    ],
  },
  {
    area: 'Output Quality',         icon: '📊', color: 'blue',
    tests: [
      'Human evaluation panel: sample 10% of outputs monthly for quality rating',
      'Automated factuality checks: verify claims against uploaded knowledge base',
      'Citation completeness: all recommendations must reference source documents',
      'Duplicate detection: ensure agent does not repeat same suggestion multiple times',
    ],
  },
  {
    area: 'Robustness & Safety',    icon: '🛡️', color: 'purple',
    tests: [
      'Adversarial prompt testing: attempt to elicit harmful or nonsensical outputs',
      'Injection resistance: verify agent ignores malicious user-injected instructions',
      'Boundary condition testing: responses within expected token and content limits',
      'Fail-safe validation: graceful degradation when external APIs are unavailable',
    ],
  },
  {
    area: 'Performance & Cost',     icon: '⚡', color: 'emerald',
    tests: [
      'Latency SLA: agent must respond within defined timeout per tier (P1/P2/P3)',
      'Token usage monitoring: alert when cost per run exceeds baseline by 20%',
      'Throughput testing: verify behaviour under concurrent multi-team usage',
      'Cache effectiveness: measure rate of redundant API calls avoided by caching',
    ],
  },
]

const STATUS_STYLE = {
  pass:    { bg: 'bg-green-50',  border: 'border-green-200', icon: '✅', text: 'text-green-700',  badge: 'bg-green-100 text-green-700'  },
  warning: { bg: 'bg-cyan-50',  border: 'border-cyan-200', icon: '⚠️', text: 'text-cyan-700',  badge: 'bg-cyan-100 text-cyan-700'  },
  fail:    { bg: 'bg-sky-50',    border: 'border-sky-200',   icon: '❌', text: 'text-sky-700',    badge: 'bg-sky-100 text-sky-700'      },
}

const RISK_COLOR = { Low: 'bg-green-100 text-green-700', Medium: 'bg-cyan-100 text-cyan-700', High: 'bg-sky-100 text-sky-700' }

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function AIAssurancePage() {
  const { project } = useApp()
  const [activeTab, setActiveTab] = useState('validation')

  const allGates    = VALIDATION_GATES.flatMap(g => g.gates)
  const passCount   = allGates.filter(g => g.status === 'pass').length
  const warnCount   = allGates.filter(g => g.status === 'warning').length
  const failCount   = allGates.filter(g => g.status === 'fail').length
  const overallPct  = Math.round(passCount / allGates.length * 100)
  const avgAccuracy = Math.round(QUALITY_METRICS.reduce((n, m) => n + m.accuracy, 0) / QUALITY_METRICS.length)

  const TABS = [
    { id: 'validation', label: '✅ Validation Gates'  },
    { id: 'bias',       label: '⚖️ Bias & Drift'      },
    { id: 'quality',    label: '📊 Output Quality'    },
    { id: 'testing',    label: '🧪 Testing for AI'    },
  ]

  return (
    <div className="space-y-6 fade-in">

      {/* Hero */}
      <div className="bg-gradient-to-r from-sky-600 to-pink-800 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">AI Assurance</h2>
            <p className="text-sky-100 text-sm max-w-2xl">
              Quality and assurance framework for the AI agents themselves — not just using AI for testing, but testing AI.
              Covers model validation gates, bias monitoring, output quality scoring, and the test strategy for every agent.
            </p>
            {project.organization && (
              <div className="mt-2 flex items-center gap-2 flex-wrap">
                <span className="bg-white/20 text-xs font-semibold px-2.5 py-1 rounded-full">🏢 {project.organization}</span>
                {project.team && <span className="bg-white/20 text-xs font-semibold px-2.5 py-1 rounded-full">👥 {project.team}</span>}
              </div>
            )}
          </div>
          <div className="flex gap-3 shrink-0">
            <div className={`rounded-xl px-4 py-3 text-center min-w-[80px] ${overallPct >= 80 ? 'bg-green-500/40' : overallPct >= 60 ? 'bg-cyan-500/40' : 'bg-sky-500/40'}`}>
              <div className="text-2xl font-bold">{overallPct}%</div>
              <div className="text-xs text-sky-200 mt-0.5">Gates Passed</div>
            </div>
            <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[80px]">
              <div className="text-2xl font-bold">{avgAccuracy}%</div>
              <div className="text-xs text-sky-200 mt-0.5">Avg Accuracy</div>
            </div>
            <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[80px]">
              <div className="text-2xl font-bold text-sky-300">{failCount}</div>
              <div className="text-xs text-sky-200 mt-0.5">Failing Gates</div>
            </div>
          </div>
        </div>
      </div>

      {/* Status summary bar */}
      <div className="flex gap-3">
        {[
          { label: 'Passed', count: passCount,   style: 'bg-green-50 border-green-200 text-green-700' },
          { label: 'Warning', count: warnCount,  style: 'bg-cyan-50 border-cyan-200 text-cyan-700' },
          { label: 'Failing', count: failCount,  style: 'bg-sky-50 border-sky-200 text-sky-700'       },
          { label: 'Total',   count: allGates.length, style: 'bg-gray-50 border-gray-200 text-gray-700' },
        ].map(s => (
          <div key={s.label} className={`flex-1 rounded-xl border p-3 text-center ${s.style}`}>
            <div className="text-2xl font-bold">{s.count}</div>
            <div className="text-xs font-semibold mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 flex-wrap">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === t.id ? 'border-sky-600 text-sky-600' : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── Validation Gates ── */}
      {activeTab === 'validation' && (
        <div className="space-y-4">
          {VALIDATION_GATES.map(vg => {
            const vgPass = vg.gates.filter(g => g.status === 'pass').length
            return (
              <div key={vg.agent} className="card">
                <div className="card-header flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{vg.icon}</span>
                    <h3 className="font-bold text-gray-800 text-sm">{vg.agent}</h3>
                  </div>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${vgPass === vg.gates.length ? 'bg-green-100 text-green-700' : vgPass >= vg.gates.length * 0.75 ? 'bg-cyan-100 text-cyan-700' : 'bg-sky-100 text-sky-700'}`}>
                    {vgPass}/{vg.gates.length} passed
                  </span>
                </div>
                <div className="card-body space-y-2">
                  {vg.gates.map((gate, i) => {
                    const s = STATUS_STYLE[gate.status]
                    return (
                      <div key={i} className={`flex items-center gap-3 p-3 rounded-lg border ${s.bg} ${s.border}`}>
                        <span className="text-lg shrink-0">{s.icon}</span>
                        <span className={`text-sm flex-1 ${s.text}`}>{gate.label}</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full shrink-0 ${s.badge}`}>
                          {gate.status === 'pass' ? 'Pass' : gate.status === 'warning' ? 'Warning' : 'Fail'}
                        </span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* ── Bias & Drift ── */}
      {activeTab === 'bias' && (
        <div className="space-y-4">
          <div className="bg-sky-50 border border-sky-200 rounded-xl p-4 text-sm text-sky-800">
            <strong>Why this matters:</strong> AI agents trained on historical data can encode and amplify existing biases. Regular bias audits ensure recommendations remain fair, balanced, and applicable across all organisational contexts.
          </div>
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Bias Risk Register</h3>
              <p className="text-xs text-gray-500">Known bias vectors identified through evaluation — track mitigation status</p>
            </div>
            <div className="card-body space-y-3">
              {BIAS_CHECKS.map((b, i) => (
                <div key={i} className={`flex items-start gap-4 p-4 rounded-xl border ${b.mitigated ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
                  <span className="text-2xl shrink-0">{b.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="font-bold text-sm text-gray-800">{b.category}</span>
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${RISK_COLOR[b.risk]}`}>{b.risk} Risk</span>
                      {b.mitigated
                        ? <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-green-100 text-green-700">✅ Mitigated</span>
                        : <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-100 text-sky-700">⚠️ Open</span>
                      }
                    </div>
                    <p className="text-xs text-gray-600">{b.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Model Drift Monitoring</h3>
            </div>
            <div className="card-body space-y-3">
              {[
                { label: 'Output Distribution Drift',   desc: 'Track distribution shift of agent outputs over time. Alert if deviation > 15% from baseline.',  status: 'Monitoring Active',  statusColor: 'green' },
                { label: 'Confidence Score Drift',      desc: 'Monitor average confidence scores across agents. Declining confidence may indicate data or model degradation.', status: 'Monitoring Active',  statusColor: 'green' },
                { label: 'Recommendation Diversity',    desc: 'Ensure agent does not converge on a narrow set of recommendations across different organisations.',  status: 'Not Configured',     statusColor: 'emerald' },
                { label: 'Benchmark Data Freshness',    desc: 'Benchmark datasets should be refreshed at least annually. Flag when data is > 18 months old.',    status: 'Action Needed',      statusColor: 'sky'   },
                { label: 'MRM Kill-Switch Drift Threshold', desc: 'MRM Agent monitors model performance against governed risk parameters. Kill-switch fires if drift exceeds threshold.', status: 'Not Configured', statusColor: 'emerald' },
                { label: 'Compliance Rule Freshness',   desc: 'Compliance-as-Code rules must be updated when GDPR, DORA, or Basel III regulations are amended. Review quarterly.', status: 'Not Configured', statusColor: 'emerald' },
              ].map((item, i) => (
                <div key={i} className="p-4 rounded-xl bg-gray-50 border border-gray-200">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="font-semibold text-sm text-gray-800">{item.label}</span>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full bg-${item.statusColor}-100 text-${item.statusColor}-700`}>{item.status}</span>
                  </div>
                  <p className="text-xs text-gray-500">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ── Output Quality ── */}
      {activeTab === 'quality' && (
        <div className="space-y-4">
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Agent Output Quality Scorecard</h3>
              <p className="text-xs text-gray-500">Measured via automated evaluation + monthly human review panel</p>
            </div>
            <div className="card-body p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 border-b border-gray-200">
                    <tr>
                      {['Agent', 'Accuracy', 'Precision', 'Hallucination Rate', 'Citation Rate'].map(h => (
                        <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {QUALITY_METRICS.map((m, i) => (
                      <tr key={i} className="hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 text-xs font-semibold text-gray-800">{m.agent}</td>
                        {[
                          { val: m.accuracy,     good: 85, warn: 70 },
                          { val: m.precision,    good: 85, warn: 70 },
                          { val: 100 - m.hallucination, good: 92, warn: 85, invert: true, rawLabel: `${m.hallucination}%` },
                          { val: m.citation,     good: 90, warn: 75 },
                        ].map((col, j) => (
                          <td key={j} className="px-4 py-3">
                            <div className="flex items-center gap-2">
                              <div className="w-20 bg-gray-200 rounded-full h-1.5">
                                <div className={`h-1.5 rounded-full ${col.val >= col.good ? 'bg-green-500' : col.val >= col.warn ? 'bg-cyan-400' : 'bg-sky-400'}`}
                                  style={{ width: `${col.val}%` }} />
                              </div>
                              <span className={`text-xs font-bold ${col.val >= col.good ? 'text-green-700' : col.val >= col.warn ? 'text-cyan-700' : 'text-sky-700'}`}>
                                {col.rawLabel || `${col.val}%`}
                              </span>
                            </div>
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="px-4 py-3 border-t border-gray-100 bg-gray-50 rounded-b-xl">
                <p className="text-xs text-gray-500">
                  Thresholds: <span className="text-green-600 font-semibold">≥ 85% = Good</span> · <span className="text-cyan-600 font-semibold">70–84% = Warning</span> · <span className="text-sky-600 font-semibold">&lt; 70% = Action needed</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Testing for AI ── */}
      {activeTab === 'testing' && (
        <div className="space-y-4">
          <div className="bg-sky-50 border border-sky-200 rounded-xl p-4 text-sm text-sky-800">
            <strong>Testing for AI ≠ AI for Testing.</strong> This section covers how we validate the quality, safety, and reliability of the AI agents themselves — a distinct discipline from using AI to generate test cases.
          </div>
          {TESTING_FOR_AI.map(sec => (
            <div key={sec.area} className="card">
              <div className={`card-header bg-${sec.color}-50 border-b border-${sec.color}-100`}>
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{sec.icon}</span>
                  <h3 className={`font-bold text-${sec.color}-800`}>{sec.area}</h3>
                </div>
              </div>
              <div className="card-body space-y-2">
                {sec.tests.map((t, i) => (
                  <div key={i} className={`flex items-start gap-3 p-3 rounded-lg bg-${sec.color}-50 border border-${sec.color}-100`}>
                    <span className={`text-${sec.color}-500 shrink-0 mt-0.5 font-bold`}>{i + 1}.</span>
                    <span className={`text-sm text-${sec.color}-800`}>{t}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Assurance Integration with CI/CD</h3>
            </div>
            <div className="card-body space-y-2">
              {[
                { gate: 'Pre-merge',       checks: 'Unit tests for prompt templates, schema validation for agent outputs' },
                { gate: 'Pre-deployment',  checks: 'Golden dataset regression suite, hallucination rate check (fail if > 10%)' },
                { gate: 'Post-deployment', checks: 'Canary evaluation: route 10% of requests, compare output quality to baseline' },
                { gate: 'Weekly',          checks: 'Human evaluation panel review, bias register update, drift monitoring report' },
                { gate: 'Monthly',         checks: 'Full RI scorecard review, benchmark data freshness audit, model update assessment' },
              ].map((row, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-lg border border-gray-200 bg-gray-50">
                  <span className="shrink-0 text-xs font-bold bg-gray-200 text-gray-700 px-2 py-0.5 rounded-full mt-0.5 whitespace-nowrap">{row.gate}</span>
                  <span className="text-sm text-gray-700">{row.checks}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
