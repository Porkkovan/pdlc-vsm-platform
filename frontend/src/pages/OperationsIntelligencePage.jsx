import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'

// ─── AIOps maturity model ─────────────────────────────────────────────────────
const AIOPS_LEVELS = [
  {
    level: 1, label: 'Reactive',    color: 'sky',
    desc:  'Manual monitoring, alert storms, human-driven triage. Teams respond after incidents occur.',
    traits: ['Manual dashboards and runbooks', 'Alert noise — low signal-to-noise ratio', 'Reactive incident response (paged on failure)', 'No predictive capability', 'High MTTR (days–weeks)'],
  },
  {
    level: 2, label: 'Proactive',   color: 'emerald',
    desc:  'Automated alerting with some correlation. Teams begin to anticipate common failure patterns.',
    traits: ['Centralised log aggregation (ELK, Splunk)', 'Basic anomaly detection via thresholds', 'On-call runbooks partially automated', 'SLO tracking established', 'MTTR hours–days'],
  },
  {
    level: 3, label: 'Predictive',  color: 'blue',
    desc:  'AI-driven anomaly detection surfaces issues before impact. Root cause analysis assisted by ML models.',
    traits: ['ML-based anomaly detection (dynamic baselines)', 'AI-assisted root cause analysis', 'Automated ticket creation and triage', 'Predictive capacity scaling', 'MTTR 30 min – 2 hrs'],
  },
  {
    level: 4, label: 'Autonomous',  color: 'green',
    desc:  'Self-healing systems execute remediation autonomously for known failure classes. Humans handle novel incidents only.',
    traits: ['Automated self-healing for known failure patterns', 'AI-driven chaos engineering in non-prod', 'Zero-touch incident resolution for P3/P4', 'Continuous SLO optimisation by agents', 'MTTR < 15 min for auto-resolved incidents'],
  },
  {
    level: 5, label: 'Governed Autonomy', color: 'indigo',
    desc:  'Telemetry & Observability Sentinel aggregates multi-agent workflow logs and translates technical failures into Business Risk Scores. Governance teams receive real-time risk dashboards; compliance and model risk monitored alongside ops health.',
    traits: ['Telemetry Sentinel aggregating all agent workflow telemetry', 'Business Risk Scores surfaced to governance and exec dashboards', 'MRM Agent monitoring AI model drift alongside ops metrics', 'Compliance-as-Code gates integrated into incident response workflow', 'Multi-Agent Governance Controller enforcing protocol compliance in real-time', 'MTTR < 5 min with automated risk classification'],
  },
]

// ─── Phase 7 deep-dive activities ────────────────────────────────────────────
const PHASE7_ACTIVITIES = [
  { name: 'Production Monitoring',      currentPT: 4,  currentWT: 0,  aiPT: 0,  aiWT: 0,  aiAgent: 'AI Monitoring Agent — real-time anomaly detection with zero human watch time',   automationPct: 95 },
  { name: 'Incident Detection',         currentPT: 2,  currentWT: 8,  aiPT: 0,  aiWT: 0,  aiAgent: 'AI Incident Detector — detects P1/P2 incidents within seconds via pattern matching', automationPct: 90 },
  { name: 'Incident Triage',            currentPT: 4,  currentWT: 12, aiPT: 1,  aiWT: 2,  aiAgent: 'AI Triage Agent — auto-classifies severity, assigns owners, creates tickets',       automationPct: 70 },
  { name: 'Root Cause Analysis',        currentPT: 8,  currentWT: 16, aiPT: 1,  aiWT: 1,  aiAgent: 'AI RCA Agent — correlates logs, traces, and metrics to surface root cause',          automationPct: 65 },
  { name: 'Automated Remediation',      currentPT: 6,  currentWT: 24, aiPT: 0,  aiWT: 0,  aiAgent: 'AI Self-Healing Agent — executes runbooks automatically for known failure classes',  automationPct: 80 },
  { name: 'Capacity Planning',          currentPT: 16, currentWT: 72, aiPT: 2,  aiWT: 4,  aiAgent: 'AI Capacity Agent — predictive scaling recommendations based on usage patterns',    automationPct: 75 },
  { name: 'Performance Analysis',       currentPT: 8,  currentWT: 48, aiPT: 1,  aiWT: 2,  aiAgent: 'AI Performance Agent — continuous regression detection across all environments',     automationPct: 80 },
  { name: 'User Feedback Processing',   currentPT: 12, currentWT: 96, aiPT: 2,  aiWT: 4,  aiAgent: 'AI Feedback Agent — NLP-driven feedback synthesis into actionable product signals',  automationPct: 60 },
]

const OPS_METRICS = [
  { label: 'MTTR (Mean Time to Restore)',     current: '6.2 hrs',  target: '< 30 min', aiTarget: '< 5 min',   icon: '🔧', trend: 'improving' },
  { label: 'MTTD (Mean Time to Detect)',      current: '28 min',   target: '< 5 min',  aiTarget: '< 30 sec',  icon: '🔍', trend: 'stable'    },
  { label: 'Incident Rate (per sprint)',      current: '4.2',      target: '< 2',      aiTarget: '< 0.5',     icon: '🚨', trend: 'worsening' },
  { label: 'Auto-Resolved Incidents',         current: '18%',      target: '> 50%',    aiTarget: '> 85%',     icon: '🤖', trend: 'improving' },
  { label: 'Alert Noise Ratio',               current: '73%',      target: '< 30%',    aiTarget: '< 5%',      icon: '📢', trend: 'stable'    },
  { label: 'SLO Compliance',                  current: '97.2%',    target: '> 99.5%',  aiTarget: '> 99.9%',   icon: '📊', trend: 'improving' },
  { label: 'Business Risk Score (Sentinel)',  current: 'N/A',      target: '< 40 / 100', aiTarget: '< 15 / 100', icon: '📡', trend: 'stable', sentinelNote: true },
]

const TREND_COLOR = { improving: 'text-green-600', stable: 'text-cyan-600', worsening: 'text-sky-600' }
const TREND_ICON  = { improving: '↑', stable: '→', worsening: '↓' }

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function OperationsIntelligencePage() {
  const { project, doraMetrics } = useApp()
  const [aiopsMaturiy, setAiopsMaturity] = useState(2)
  const [activeTab, setActiveTab]        = useState('aiops')

  const TABS = [
    { id: 'aiops',   label: '🤖 AIOps Maturity'     },
    { id: 'metrics', label: '📊 Ops Metrics'         },
    { id: 'phase7',  label: '📡 Phase 7 Deep-Dive'   },
    { id: 'resilience', label: '🛡️ Resilience Design' },
  ]

  const currentLevel = AIOPS_LEVELS.find(l => l.level === aiopsMaturiy) || AIOPS_LEVELS[1]

  return (
    <div className="space-y-6 fade-in">

      {/* Hero */}
      <div className="bg-gradient-to-r from-cyan-700 to-teal-800 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">Operations Intelligence</h2>
            <p className="text-cyan-100 text-sm max-w-2xl">
              AI-enabled resilient IT operations — assess AIOps maturity, model Phase 7 transformation,
              track MTTR/MTTD trends, and design the path to self-healing autonomous operations.
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
              <div className="text-2xl font-bold">{currentLevel.label}</div>
              <div className="text-xs text-cyan-200 mt-0.5">AIOps Level {aiopsMaturiy}/5</div>
            </div>
            {doraMetrics?.mttr && (
              <div className="bg-white/15 rounded-xl px-4 py-3 text-center min-w-[90px]">
                <div className="text-2xl font-bold">{doraMetrics.mttr}</div>
                <div className="text-xs text-cyan-200 mt-0.5">MTTR (DORA)</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200 flex-wrap">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === t.id ? 'border-cyan-600 text-cyan-700' : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── AIOps Maturity ── */}
      {activeTab === 'aiops' && (
        <div className="space-y-4">
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">AIOps Maturity Assessment</h3>
              <p className="text-xs text-gray-500">Select your current operational maturity level</p>
            </div>
            <div className="card-body space-y-3">
              {AIOPS_LEVELS.map(level => (
                <button key={level.level} onClick={() => setAiopsMaturity(level.level)}
                  className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                    aiopsMaturiy === level.level
                      ? `border-${level.color}-400 bg-${level.color}-50`
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}>
                  <div className="flex items-start gap-3">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0 ${
                      aiopsMaturiy === level.level ? `bg-${level.color}-600 text-white` : 'bg-gray-200 text-gray-600'
                    }`}>L{level.level}</div>
                    <div className="flex-1">
                      <div className={`font-bold text-sm ${aiopsMaturiy === level.level ? `text-${level.color}-800` : 'text-gray-700'}`}>
                        {level.label}
                      </div>
                      <p className="text-xs text-gray-500 mt-0.5">{level.desc}</p>
                      {aiopsMaturiy === level.level && (
                        <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-1.5">
                          {level.traits.map((t, i) => (
                            <div key={i} className="flex items-start gap-1.5 text-xs text-gray-600">
                              <span className="shrink-0 mt-0.5">•</span><span>{t}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    {aiopsMaturiy === level.level && <span className="text-xl shrink-0">✓</span>}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Maturity progression path */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Maturity Progression Path</h3>
              <p className="text-xs text-gray-500">Steps to advance from current level to Autonomous (Level 4)</p>
            </div>
            <div className="card-body space-y-3">
              {AIOPS_LEVELS.filter(l => l.level > aiopsMaturiy).map((level, i) => (
                <div key={level.level} className={`p-4 rounded-xl border ${i === 0 ? 'border-cyan-200 bg-cyan-50' : 'border-gray-200 bg-gray-50'}`}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${i === 0 ? 'bg-cyan-600 text-white' : 'bg-gray-300 text-gray-700'}`}>
                      {i === 0 ? 'Next Step' : `Step ${i + 1}`}
                    </span>
                    <span className="font-bold text-sm text-gray-800">Level {level.level}: {level.label}</span>
                  </div>
                  <p className="text-xs text-gray-600">{level.desc}</p>
                </div>
              ))}
              {aiopsMaturiy === 5 && (
                <div className="p-4 rounded-xl border border-indigo-200 bg-indigo-50 text-sm text-indigo-800 font-semibold text-center">
                  ✅ Governed Autonomy Achieved — highest AIOps maturity with Telemetry Sentinel &amp; Governance Controller active
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ── Ops Metrics ── */}
      {activeTab === 'metrics' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {OPS_METRICS.map(m => (
              <div key={m.label} className="card">
                <div className="card-body">
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{m.icon}</span>
                      <span className="text-sm font-bold text-gray-800">{m.label}</span>
                    </div>
                    <span className={`text-xs font-semibold ${TREND_COLOR[m.trend]}`}>
                      {TREND_ICON[m.trend]} {m.trend}
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <div className="bg-gray-50 rounded-lg p-2">
                      <div className="text-sm font-bold text-gray-700">{m.current}</div>
                      <div className="text-xs text-gray-400">Current</div>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-2">
                      <div className="text-sm font-bold text-blue-700">{m.target}</div>
                      <div className="text-xs text-blue-400">Target</div>
                    </div>
                    <div className="bg-green-50 rounded-lg p-2">
                      <div className="text-sm font-bold text-green-700">{m.aiTarget}</div>
                      <div className="text-xs text-green-400">AI-driven</div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="bg-teal-50 border border-teal-200 rounded-xl p-4 text-sm text-teal-800">
            💡 Connect your <Link to="/dora-assessment" className="font-semibold underline">DORA Assessment</Link> MTTR/MTTD values to populate live metrics above.
          </div>
        </div>
      )}

      {/* ── Phase 7 Deep-Dive ── */}
      {activeTab === 'phase7' && (
        <div className="space-y-4">
          <div className="bg-cyan-50 border border-cyan-200 rounded-xl p-4 text-sm text-cyan-800">
            Phase 7 (Monitoring & Feedback) typically has the highest wait time in the PDLC — incidents queue up, triage is manual, and feedback loops to Product are slow.
            AI agents compress this phase dramatically by automating detection, triage, and remediation.
          </div>

          {/* Telemetry Sentinel + MRM Agent integration panel */}
          <div className="card border-l-4 border-indigo-500">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Governance Agents Active in Phase 7</h3>
              <p className="text-xs text-gray-500">The Telemetry Sentinel and MRM Agent run continuously alongside delivery operations, feeding risk signals back to the Governance Controller</p>
            </div>
            <div className="card-body grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Telemetry Sentinel */}
              <div className="rounded-xl border border-cyan-200 bg-cyan-50 p-4 space-y-3">
                <div className="flex items-start gap-3">
                  <span className="text-2xl shrink-0">📡</span>
                  <div>
                    <div className="font-bold text-gray-800 text-sm">Telemetry & Observability Sentinel</div>
                    <span className="text-xs bg-cyan-100 text-cyan-700 px-2 py-0.5 rounded-full font-semibold">Phase 7 + Cross-phase</span>
                  </div>
                </div>
                <p className="text-xs text-gray-600">Aggregates logs from all multi-agent workflow executions and translates technical signals into <strong>Business Risk Scores</strong> (0–100 scale) for governance and executive dashboards.</p>
                <div className="space-y-1.5">
                  {[
                    'Aggregates logs from all 13 agent workflow executions',
                    'Calculates Business Risk Score per incident class',
                    'Surfaces risk dashboards to governance teams in real-time',
                    'Triggers mandatory review when Business Risk Score > threshold',
                    'Feeds risk signals to Multi-Agent Governance Controller',
                  ].map((item, i) => (
                    <div key={i} className="flex items-start gap-2 text-xs text-gray-600">
                      <span className="text-cyan-500 shrink-0 mt-0.5">→</span><span>{item}</span>
                    </div>
                  ))}
                </div>
                <div className="bg-white border border-cyan-200 rounded-lg p-2.5 text-xs">
                  <div className="font-semibold text-cyan-800 mb-1">Flow: Sentinel → Governance Controller</div>
                  <div className="text-gray-600">Business Risk Score &gt; 60 → Governance Controller flags agents for human review · Score &gt; 80 → automatic pipeline pause pending CTO approval</div>
                </div>
              </div>

              {/* MRM Agent */}
              <div className="rounded-xl border border-purple-200 bg-purple-50 p-4 space-y-3">
                <div className="flex items-start gap-3">
                  <span className="text-2xl shrink-0">🧬</span>
                  <div>
                    <div className="font-bold text-gray-800 text-sm">Model Risk Management (MRM) Agent</div>
                    <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full font-semibold">Phase 5 + Phase 7</span>
                  </div>
                </div>
                <p className="text-xs text-gray-600">Monitors all AI model versions running in production. Generates <strong>Explainability Reports</strong> per deploy and triggers an automated kill-switch if model performance drifts outside governed risk parameters.</p>
                <div className="space-y-1.5">
                  {[
                    'Generates Explainability Report for every model version pushed to production',
                    'Detects bias in model outputs across protected attribute groups',
                    'Monitors drift vs baseline — triggers alert if > governed threshold',
                    'Executes kill-switch (dual-authorisation: MRO + CTO) on critical drift',
                    'Feeds model risk signals to Telemetry Sentinel for consolidated scoring',
                  ].map((item, i) => (
                    <div key={i} className="flex items-start gap-2 text-xs text-gray-600">
                      <span className="text-purple-500 shrink-0 mt-0.5">→</span><span>{item}</span>
                    </div>
                  ))}
                </div>
                <div className="bg-white border border-purple-200 rounded-lg p-2.5 text-xs">
                  <div className="font-semibold text-purple-800 mb-1">Flow: MRM Agent → Sentinel → Governance Controller</div>
                  <div className="text-gray-600">Model drift detected → MRM raises risk signal → Sentinel updates Business Risk Score → Governance Controller enforces review protocol</div>
                </div>
              </div>
            </div>

            {/* Feedback loop diagram */}
            <div className="px-5 pb-5">
              <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                <div className="text-xs font-semibold text-gray-700 mb-3">Phase 7 Risk Feedback Loop</div>
                <div className="flex items-center flex-wrap gap-2 text-xs">
                  {[
                    { label: 'Production Event', color: 'bg-gray-500' },
                    { label: '→' },
                    { label: 'Telemetry Sentinel', color: 'bg-cyan-600' },
                    { label: '+' },
                    { label: 'MRM Agent', color: 'bg-purple-600' },
                    { label: '→' },
                    { label: 'Business Risk Score', color: 'bg-cyan-600' },
                    { label: '→' },
                    { label: 'Governance Controller', color: 'bg-indigo-500' },
                    { label: '→' },
                    { label: 'Human Review / Auto-pause', color: 'bg-sky-600' },
                  ].map((item, i) => (
                    item.label === '→' || item.label === '+' ? (
                      <span key={i} className="text-gray-400 font-bold">{item.label}</span>
                    ) : (
                      <span key={i} className={`text-white px-2 py-0.5 rounded-full font-semibold ${item.color}`}>{item.label}</span>
                    )
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Summary metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { label: 'Current Process Time',  value: `${PHASE7_ACTIVITIES.reduce((n, a) => n + a.currentPT, 0)}h`,  color: 'gray'  },
              { label: 'Current Wait Time',      value: `${PHASE7_ACTIVITIES.reduce((n, a) => n + a.currentWT, 0)}h`,  color: 'sky'   },
              { label: 'AI Process Time',        value: `${PHASE7_ACTIVITIES.reduce((n, a) => n + a.aiPT, 0)}h`,       color: 'green' },
              { label: 'AI Wait Time',           value: `${PHASE7_ACTIVITIES.reduce((n, a) => n + a.aiWT, 0)}h`,       color: 'green' },
            ].map(m => (
              <div key={m.label} className={`bg-${m.color}-50 border border-${m.color}-200 rounded-xl p-4 text-center`}>
                <div className={`text-2xl font-bold text-${m.color}-700`}>{m.value}</div>
                <div className={`text-xs text-${m.color}-500 mt-1`}>{m.label}</div>
              </div>
            ))}
          </div>

          {/* Activity table */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Phase 7 Activity Transformation</h3>
            </div>
            <div className="card-body p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 border-b border-gray-200">
                    <tr>
                      {['Activity', 'Current PT/WT', 'AI PT/WT', 'Automation', 'AI Agent'].map(h => (
                        <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {PHASE7_ACTIVITIES.map((a, i) => (
                      <tr key={i} className="hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 text-xs font-semibold text-gray-800">{a.name}</td>
                        <td className="px-4 py-3 text-xs text-gray-600">{a.currentPT}h / {a.currentWT}h</td>
                        <td className="px-4 py-3 text-xs text-green-700 font-semibold">{a.aiPT}h / {a.aiWT}h</td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            <div className="w-16 bg-gray-200 rounded-full h-1.5">
                              <div className="h-1.5 rounded-full bg-green-500" style={{ width: `${a.automationPct}%` }} />
                            </div>
                            <span className="text-xs font-bold text-green-700">{a.automationPct}%</span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-xs text-gray-600 max-w-xs">{a.aiAgent}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Resilience Design ── */}
      {activeTab === 'resilience' && (
        <div className="space-y-4">
          {[
            {
              title: 'Observability Foundation',    icon: '🔭', color: 'blue',
              desc:  'The prerequisite for AI-driven operations. Without structured telemetry, AI agents cannot learn or detect anomalies.',
              pillars: ['Unified logging (structured JSON, correlation IDs)', 'Distributed tracing across all services', 'Golden signals: latency, traffic, errors, saturation', 'Real-time metric streaming (Prometheus / OpenTelemetry)', 'Synthetic monitoring for critical user journeys'],
            },
            {
              title: 'Incident Intelligence',       icon: '🧠', color: 'purple',
              desc:  'AI-powered incident management that moves from human-paged response to intelligent, context-aware triage and response.',
              pillars: ['ML-based alert correlation (reduce alert storms by 80%)', 'Automated severity classification via NLP on logs', 'AI-generated incident summaries for on-call engineers', 'Runbook automation for top 20 incident types', 'Post-incident AI root cause report generation'],
            },
            {
              title: 'Self-Healing Patterns',       icon: '🔄', color: 'green',
              desc:  'Automated remediation for known failure classes, allowing engineering teams to focus on novel and high-complexity incidents.',
              pillars: ['Circuit breakers and bulkhead patterns', 'Automated pod restart / scaling on memory/CPU thresholds', 'AI-triggered canary rollback on SLO breach', 'Automated cache purge on stale-data anomalies', 'Chaos engineering pipeline to validate resilience'],
            },
            {
              title: 'Continuous Resilience Improvement', icon: '📈', color: 'emerald',
              desc:  'Treat resilience as a product — continuously measure, learn, and improve using AI-driven insights from production data.',
              pillars: ['Weekly SLO review with AI trend analysis', 'Automated game days triggered by AI resilience agent', 'MTTR/MTTD KPI dashboards linked to team OKRs', 'AI-generated resilience improvement backlog items', 'Quarterly chaos experiment planning assisted by AI'],
            },
          ].map(sec => (
            <div key={sec.title} className="card">
              <div className={`card-header bg-${sec.color}-50 border-b border-${sec.color}-100`}>
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{sec.icon}</span>
                  <h3 className={`font-bold text-${sec.color}-800`}>{sec.title}</h3>
                </div>
              </div>
              <div className="card-body">
                <p className="text-sm text-gray-600 mb-4">{sec.desc}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {sec.pillars.map((p, i) => (
                    <div key={i} className={`flex items-start gap-2 text-xs p-2.5 rounded-lg bg-${sec.color}-50 border border-${sec.color}-100 text-${sec.color}-800`}>
                      <span className="shrink-0 mt-0.5">→</span><span>{p}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
