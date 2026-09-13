import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { agentsApi } from '../services/api'
import { doraToVsmCalibration } from './DORAAssessmentPage'

// ── Layer definitions ─────────────────────────────────────────────────────────
const LAYERS = [
  { id: 'data',         label: 'Data Layer',        color: 'blue',   desc: 'Ingestion & connectivity' },
  { id: 'analysis',     label: 'Analysis Layer',     color: 'purple', desc: 'VSM metrics & benchmarking' },
  { id: 'governance',   label: 'Governance Layer',   color: 'indigo', desc: 'Compliance, risk & security' },
  { id: 'output',       label: 'Output Layer',       color: 'green',  desc: 'Improvements, futures & financials' },
  { id: 'orchestration',label: 'Orchestration',      color: 'gray',   desc: 'Coordination & control plane' },
]

const AGENTS = [
  // ── Data Layer ───────────────────────────────────────────────────────────────
  {
    id: 'alm-connector', name: 'ALM Connector', icon: '🔗', color: 'blue', layer: 'data', endpoint: 'alm',
    desc: 'Connects to Jira/ADO/Rally, pulls ticket data, computes PT/WT/LT metrics from ALM history',
    pdlcPhases: ['Phase 1 — Backlog & Roadmap'],
    feedsInto: ['VSM Analyzer', 'Bottleneck Analyzer'],
    receivesFrom: [],
  },
  // ── Analysis Layer ───────────────────────────────────────────────────────────
  {
    id: 'vsm-analyzer', name: 'VSM Analyzer', icon: '🗺️', color: 'purple', layer: 'analysis', endpoint: 'vsm-analyzer',
    desc: 'Builds comprehensive current-state VSM with PT/WT/LT/FE metrics per phase using LangGraph',
    pdlcPhases: ['Phase 2 — Architecture & UX'],
    feedsInto: ['Bottleneck Analyzer', 'Future State Designer'],
    receivesFrom: ['ALM Connector'],
  },
  {
    id: 'bottleneck-analyzer', name: 'Bottleneck Analyzer', icon: '⚠️', color: 'sky', layer: 'analysis', endpoint: 'bottleneck-analyzer',
    desc: 'Identifies flow bottlenecks per phase using Lean VSM methodology, assigns severity scores and root cause',
    pdlcPhases: ['Phase 5 — Continuous Testing'],
    feedsInto: ['Improvement Generator', 'Business Case Builder'],
    receivesFrom: ['VSM Analyzer', 'ALM Connector'],
  },
  {
    id: 'benchmark-agent', name: 'Benchmark Agent', icon: '📊', color: 'teal', layer: 'analysis', endpoint: 'benchmark-agent',
    desc: 'Compares team metrics against 12 sector peers using DORA, Gartner, and Forrester industry datasets',
    pdlcPhases: ['Phase 6 — Continuous Delivery'],
    feedsInto: ['Improvement Generator', 'Business Case Builder'],
    receivesFrom: ['VSM Analyzer'],
  },
  // ── Governance Layer ─────────────────────────────────────────────────────────
  {
    id: 'secure-by-design', name: 'Secure-by-Design Architect', icon: '🔐', color: 'sky', layer: 'governance', endpoint: null,
    desc: 'Auto-rejects IaC/cloud configs deviating from security baseline. Scope: IaC, security protocol selection, architectural standards.',
    pdlcPhases: ['Phase 2 — Architecture & UX', 'Phase 6 — Continuous Delivery'],
    feedsInto: ['Multi-Agent Governance Controller', 'Telemetry Sentinel'],
    receivesFrom: ['Orchestrator', 'Multi-Agent Governance Controller'],
  },
  {
    id: 'cac-orchestrator', name: 'Compliance-as-Code Orchestrator', icon: '📋', color: 'blue', layer: 'governance', endpoint: null,
    desc: 'Validates every commit against GDPR/DORA/Basel III in real-time. Shifts compliance from final checkpoint to continuous background process.',
    pdlcPhases: ['Phase 3 — Code Management', 'Phase 5 — Continuous Testing'],
    feedsInto: ['Multi-Agent Governance Controller', 'Telemetry Sentinel'],
    receivesFrom: ['Orchestrator', 'Multi-Agent Governance Controller'],
  },
  {
    id: 'mrm-agent', name: 'Model Risk Management (MRM) Agent', icon: '🧬', color: 'purple', layer: 'governance', endpoint: null,
    desc: 'Generates Explainability Reports, detects bias, triggers automated kill-switch if model performance drifts outside governed risk parameters.',
    pdlcPhases: ['Phase 5 — Continuous Testing', 'Phase 7 — Monitoring & Feedback'],
    feedsInto: ['Multi-Agent Governance Controller', 'Telemetry Sentinel'],
    receivesFrom: ['Orchestrator', 'Multi-Agent Governance Controller'],
  },
  // ── Output Layer ─────────────────────────────────────────────────────────────
  {
    id: 'improvement-generator', name: 'Improvement Generator', icon: '🚀', color: 'green', layer: 'output', endpoint: 'improvement-generator',
    desc: 'Generates AI-focused improvement catalogue with effort/impact scoring based on GenAI and industry best practices',
    pdlcPhases: ['Phase 3 — Code Management'],
    feedsInto: ['Future State Designer', 'Business Case Builder'],
    receivesFrom: ['Bottleneck Analyzer', 'Benchmark Agent'],
  },
  {
    id: 'future-state-designer', name: 'Future State Designer', icon: '🔮', color: 'violet', layer: 'output', endpoint: 'future-state-designer',
    desc: 'Designs 3 transformation scenarios (Option A/B/C) with predicted PT, WT, LT, and FE metrics per phase',
    pdlcPhases: ['Phase 7 — Monitoring & Feedback'],
    feedsInto: ['Business Case Builder'],
    receivesFrom: ['VSM Analyzer', 'Improvement Generator'],
  },
  {
    id: 'business-case-builder', name: 'Business Case Builder', icon: '💼', color: 'emerald', layer: 'output', endpoint: 'business-case-builder',
    desc: 'Generates ROI/payback/NPV financial models with investment ranges, org changes, tooling, DevSecOps, and AIOps per scenario',
    pdlcPhases: ['Phase 6 — Continuous Delivery'],
    feedsInto: [],
    receivesFrom: ['Bottleneck Analyzer', 'Benchmark Agent', 'Improvement Generator', 'Future State Designer'],
  },
  {
    id: 'telemetry-sentinel', name: 'Telemetry & Observability Sentinel', icon: '📡', color: 'cyan', layer: 'output', endpoint: null,
    desc: 'Aggregates logs from multi-agent workflows and translates technical failures into Business Risk Scores for governance teams.',
    pdlcPhases: ['Phase 7 — Monitoring & Feedback', 'Cross-phase'],
    feedsInto: ['Multi-Agent Governance Controller'],
    receivesFrom: ['Secure-by-Design Architect', 'CaC Orchestrator', 'MRM Agent'],
  },
  // ── Orchestration Layer ──────────────────────────────────────────────────────
  {
    id: 'orchestrator', name: 'Orchestrator', icon: '🎭', color: 'gray', layer: 'orchestration', endpoint: 'orchestrator',
    desc: 'Coordinates all delivery agents in sequence via LangGraph StateGraph, managing state and handoffs across the pipeline',
    pdlcPhases: ['Phase 1 — Backlog & Roadmap', 'Phase 4 — CI'],
    feedsInto: ['All delivery agents'],
    receivesFrom: ['Multi-Agent Governance Controller'],
  },
  {
    id: 'governance-controller', name: 'Multi-Agent Governance Controller', icon: '🏛️', color: 'indigo', layer: 'orchestration', endpoint: null,
    desc: 'Agent of Agents — syncs all 13 agents, enforces protocols, prevents bypass. No single agent can circumvent a governance rule.',
    pdlcPhases: ['All phases — orchestration layer', 'Phase 4 — CI'],
    feedsInto: ['All agents'],
    receivesFrom: ['Telemetry Sentinel', 'Orchestrator'],
  },
]

// Agents that have runnable endpoints
const RUNNABLE_AGENTS = AGENTS.filter(a => a.endpoint !== null)

const STATUS_STYLES = {
  idle:     'bg-gray-100 text-gray-600',
  running:  'bg-blue-100 text-blue-700 animate-pulse',
  complete: 'bg-green-100 text-green-700',
  error:    'bg-sky-100 text-sky-700',
}

// Layer colour maps
const LAYER_COLORS = {
  data:         { bg: 'bg-blue-50',   border: 'border-blue-300',   badge: 'bg-blue-600',   text: 'text-blue-700'   },
  analysis:     { bg: 'bg-purple-50', border: 'border-purple-300', badge: 'bg-purple-600', text: 'text-purple-700' },
  governance:   { bg: 'bg-indigo-50', border: 'border-indigo-300', badge: 'bg-indigo-600', text: 'text-indigo-700' },
  output:       { bg: 'bg-green-50',  border: 'border-green-300',  badge: 'bg-green-600',  text: 'text-green-700'  },
  orchestration:{ bg: 'bg-gray-100',  border: 'border-gray-400',   badge: 'bg-gray-700',   text: 'text-gray-700'   },
}

export default function AgentsPage() {
  const { agentStatus, updateAgentStatus, addNotification, project, doraMetrics } = useApp()
  const [runningAll, setRunningAll] = useState(false)
  const [activeLayer, setActiveLayer] = useState(null) // null = show all

  const runAgent = async (agent) => {
    updateAgentStatus(agent.id, 'running')
    try {
      const result = await agentsApi[`run${toCamel(agent.endpoint)}`]?.(project.id || 'demo')
      updateAgentStatus(agent.id, 'complete', result)
      addNotification(`${agent.name} completed!`, 'success')
    } catch {
      updateAgentStatus(agent.id, 'complete')
      addNotification(`${agent.name} ran in demo mode`, 'info')
    }
  }

  const runAll = async () => {
    setRunningAll(true)
    const doraCalibration = doraMetrics ? doraToVsmCalibration(doraMetrics) : null
    try {
      await agentsApi.runFullAnalysis(project.id || 'demo', doraCalibration)
      addNotification('Full multi-agent analysis complete!', 'success')
    } catch {
      for (const agent of RUNNABLE_AGENTS.slice(0, -1)) {
        updateAgentStatus(agent.id, 'running')
        await new Promise(r => setTimeout(r, 800))
        updateAgentStatus(agent.id, 'complete')
      }
      addNotification('Full analysis ran in demo mode', 'info')
    } finally { setRunningAll(false) }
  }

  const getStatus = (id) => agentStatus[id]?.status || 'idle'

  const visibleAgents = activeLayer
    ? AGENTS.filter(a => a.layer === activeLayer)
    : AGENTS

  // Count agents per layer for pipeline display
  const layerGroups = LAYERS.map(l => ({
    ...l,
    agents: AGENTS.filter(a => a.layer === l.id),
  }))

  return (
    <div className="space-y-6 fade-in">

      {/* Header */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">AI Agent Orchestration</h2>
            <p className="text-gray-300">
              <span className="font-semibold text-white">13 AI Agents</span> — unified pipeline from data ingestion to
              governance-assured outputs, coordinated by the Multi-Agent Governance Controller
            </p>
          </div>
          <button onClick={runAll} disabled={runningAll}
            className="bg-blue-500 text-white px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-600 shadow">
            {runningAll ? '⏳ Running All...' : '▶ Run Full Analysis'}
          </button>
        </div>
      </div>

      {/* Unified Pipeline Diagram */}
      <div className="card card-body">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-gray-800">Unified 13-Agent Pipeline</h3>
          <span className="text-xs text-gray-500">Click a layer to filter the agent catalogue below</span>
        </div>

        {/* Pipeline flow — layers */}
        <div className="grid grid-cols-5 gap-2 mb-4">
          {layerGroups.map((layer, i) => {
            const lc = LAYER_COLORS[layer.id]
            const isActive = activeLayer === layer.id
            return (
              <button
                key={layer.id}
                onClick={() => setActiveLayer(isActive ? null : layer.id)}
                className={`rounded-xl border-2 p-3 text-left transition-all ${
                  isActive ? `${lc.bg} ${lc.border} shadow-md` : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className={`text-xs font-bold mb-1 ${isActive ? lc.text : 'text-gray-500'}`}>{layer.label}</div>
                <div className="text-xs text-gray-400 mb-2">{layer.desc}</div>
                <div className="flex flex-wrap gap-1">
                  {layer.agents.map(a => (
                    <div
                      key={a.id}
                      title={a.name}
                      className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm border ${
                        getStatus(a.id) === 'complete' ? 'border-green-400 bg-green-50' :
                        getStatus(a.id) === 'running'  ? 'border-blue-400 bg-blue-50 animate-pulse' :
                        isActive ? `${lc.bg} ${lc.border}` : 'border-gray-200 bg-gray-50'
                      }`}
                    >
                      {a.icon}
                    </div>
                  ))}
                </div>
                <div className={`mt-2 text-xs font-semibold ${isActive ? lc.text : 'text-gray-400'}`}>
                  {layer.agents.length} agent{layer.agents.length > 1 ? 's' : ''}
                </div>
              </button>
            )
          })}
        </div>

        {/* Flow arrows */}
        <div className="flex items-center justify-between px-4 text-gray-400 text-sm mb-1">
          <span className="text-xs text-gray-400 italic">Data flows left → right through the pipeline</span>
          <div className="flex items-center gap-2 text-xs">
            <span className="flex items-center gap-1"><span className="w-3 h-3 bg-indigo-600 rounded inline-block" /> Orchestration wraps all layers</span>
          </div>
        </div>

        {/* Linear agent flow (all runnable agents in sequence) */}
        <div className="flex flex-wrap items-center gap-1.5 bg-gray-50 rounded-xl p-3 border border-gray-200">
          {AGENTS.filter(a => a.layer !== 'orchestration').map((a, i, arr) => {
            const lc = LAYER_COLORS[a.layer]
            return (
              <div key={a.id} className="flex items-center gap-1.5">
                <div className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold border ${lc.bg} ${lc.border} ${lc.text} ${
                  getStatus(a.id) === 'complete' ? 'ring-2 ring-green-400' :
                  getStatus(a.id) === 'running'  ? 'ring-2 ring-blue-400 animate-pulse' : ''
                }`} title={a.desc}>
                  {a.icon} {a.name.replace(' Agent', '').replace(' Orchestrator', '').substring(0, 18)}
                </div>
                {i < arr.length - 1 && <span className="text-gray-300 text-xs">→</span>}
              </div>
            )
          })}
          <div className="flex items-center gap-1.5 ml-2 pl-2 border-l border-gray-300">
            {AGENTS.filter(a => a.layer === 'orchestration').map(a => {
              const lc = LAYER_COLORS[a.layer]
              return (
                <div key={a.id} className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold border ${lc.bg} ${lc.border} ${lc.text}`} title={a.desc}>
                  {a.icon} {a.name.replace(' Agent', '')}
                </div>
              )
            })}
          </div>
        </div>

        {/* Layer legend */}
        <div className="flex flex-wrap gap-2 mt-3">
          {LAYERS.map(l => {
            const lc = LAYER_COLORS[l.id]
            return (
              <div key={l.id} className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full border ${lc.bg} ${lc.border}`}>
                <span className={`w-2 h-2 rounded-full ${lc.badge}`} />
                <span className={`text-xs font-semibold ${lc.text}`}>{l.label}</span>
              </div>
            )
          })}
          {activeLayer && (
            <button onClick={() => setActiveLayer(null)} className="text-xs text-gray-500 underline ml-2">Show all layers</button>
          )}
        </div>
      </div>

      {/* Unified agent catalogue — single grid, all 13 */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-gray-800">
            {activeLayer
              ? `${LAYERS.find(l => l.id === activeLayer)?.label} — ${visibleAgents.length} Agent${visibleAgents.length > 1 ? 's' : ''}`
              : 'All 13 Agents — Unified Catalogue'}
          </h3>
          {activeLayer && (
            <button onClick={() => setActiveLayer(null)} className="text-xs text-blue-600 underline">← Show all 13</button>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {visibleAgents.map(agent => {
            const status = getStatus(agent.id)
            const lc = LAYER_COLORS[agent.layer]
            const layer = LAYERS.find(l => l.id === agent.layer)
            return (
              <div key={agent.id} className={`rounded-xl border-2 overflow-hidden ${
                status === 'complete' ? 'border-green-400' :
                status === 'running'  ? 'border-blue-400' :
                lc.border
              }`}>
                {/* Layer banner */}
                <div className={`px-4 py-1.5 flex items-center justify-between ${lc.bg}`}>
                  <span className={`text-xs font-bold ${lc.text}`}>{layer?.label}</span>
                  {agent.pdlcPhases.map((ph, i) => (
                    <span key={i} className={`text-xs px-2 py-0.5 rounded-full font-semibold text-white ${lc.badge}`}>{ph}</span>
                  ))[0]}
                </div>
                <div className="p-4 space-y-3 bg-white">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{agent.icon}</span>
                      <div>
                        <div className="font-bold text-gray-800 text-sm">{agent.name}</div>
                        <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${STATUS_STYLES[status]}`}>
                          {status === 'idle' ? 'Ready' : status.charAt(0).toUpperCase() + status.slice(1)}
                        </span>
                      </div>
                    </div>
                    {agent.endpoint ? (
                      <button
                        onClick={() => runAgent(agent)}
                        disabled={status === 'running'}
                        className="btn-primary text-xs px-3 py-1.5"
                      >
                        {status === 'running' ? '⏳' : '▶ Run'}
                      </button>
                    ) : (
                      <span className="text-xs px-2 py-1 bg-indigo-50 border border-indigo-200 text-indigo-700 rounded-lg font-semibold">Option B/C</span>
                    )}
                  </div>

                  <p className="text-xs text-gray-600 leading-relaxed">{agent.desc}</p>

                  {/* PDLC phases */}
                  {agent.pdlcPhases.length > 1 && (
                    <div className="flex flex-wrap gap-1">
                      {agent.pdlcPhases.map((ph, i) => (
                        <span key={i} className={`text-xs px-2 py-0.5 rounded-full border font-semibold ${lc.bg} ${lc.border} ${lc.text}`}>{ph}</span>
                      ))}
                    </div>
                  )}

                  {/* Feeds into / receives from */}
                  <div className="grid grid-cols-2 gap-2">
                    {agent.receivesFrom.length > 0 && (
                      <div className="bg-gray-50 rounded-lg p-2">
                        <div className="text-xs font-semibold text-gray-500 mb-1">Receives from</div>
                        <div className="flex flex-wrap gap-1">
                          {agent.receivesFrom.map(f => (
                            <span key={f} className="text-xs bg-white border border-gray-200 text-gray-600 px-1.5 py-0.5 rounded">{f}</span>
                          ))}
                        </div>
                      </div>
                    )}
                    {agent.feedsInto.length > 0 && (
                      <div className="bg-gray-50 rounded-lg p-2">
                        <div className="text-xs font-semibold text-gray-500 mb-1">Feeds into</div>
                        <div className="flex flex-wrap gap-1">
                          {agent.feedsInto.map(f => (
                            <span key={f} className="text-xs bg-white border border-gray-200 text-gray-600 px-1.5 py-0.5 rounded">{f}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {status === 'complete' && (
                    <div className="bg-green-50 border border-green-200 rounded p-2 text-xs text-green-700">
                      ✅ Analysis complete — results available in the platform
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Architecture note */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-5 rounded-lg text-sm text-blue-800">
        <p className="font-semibold mb-2">Multi-Agent Architecture — 13 Agents, One Unified System</p>
        <p className="text-xs leading-relaxed">
          Built with Python FastAPI + LangGraph StateGraph. The 8 core delivery agents handle data ingestion, VSM analysis, benchmarking,
          improvements, future-state design, and financial modelling. The 5 governance agents (Secure-by-Design, Compliance-as-Code,
          MRM, Telemetry Sentinel, Governance Controller) run as a continuous compliance and risk layer alongside the delivery pipeline —
          not as a separate phase. The Multi-Agent Governance Controller ensures no delivery agent can bypass a governance protocol,
          making the 13-agent system safe for enterprise-scale autonomous operation.
        </p>
      </div>
    </div>
  )
}

function toCamel(str) {
  return str.split('-').map((w, i) => i === 0 ? w : w[0].toUpperCase() + w.slice(1)).join('')
}
