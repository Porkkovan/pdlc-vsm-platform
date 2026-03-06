import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { agentsApi } from '../services/api'

const AGENTS = [
  { id: 'alm-connector',        name: 'ALM Connector Agent',       icon: '🔗', desc: 'Connects to Jira/ADO, pulls ticket data, computes PT/WT/LT metrics from ALM history', color: 'blue', endpoint: 'alm' },
  { id: 'vsm-analyzer',         name: 'VSM Analyzer Agent',        icon: '🗺️', desc: 'Builds comprehensive VSM with current state metrics per phase/activity using LangGraph', color: 'purple', endpoint: 'vsm-analyzer' },
  { id: 'bottleneck-analyzer',  name: 'Bottleneck Analyzer Agent', icon: '⚠️', desc: 'Identifies flow bottlenecks per phase using Lean VSM methodology and industry benchmarks', color: 'red', endpoint: 'bottleneck-analyzer' },
  { id: 'benchmark-agent',      name: 'Benchmark Agent',           icon: '📊', desc: 'Sources industry best practice metrics (DORA, Gartner, Forrester) for comparison', color: 'orange', endpoint: 'benchmark-agent' },
  { id: 'improvement-generator',name: 'Improvement Generator Agent',icon: '🚀', desc: 'Generates AI-focused improvement actions per bottleneck based on GenAI and industry best practices', color: 'green', endpoint: 'improvement-generator' },
  { id: 'future-state-designer',name: 'Future State Designer Agent',icon: '🔮', desc: 'Designs 3 future state scenarios (A/B/C) with predicted PT, WT, LT, FE metrics', color: 'violet', endpoint: 'future-state-designer' },
  { id: 'business-case-builder',name: 'Business Case Builder Agent',icon: '💼', desc: 'Generates business case with investment, ROI, org changes, tools, DevSecOps, AIOps for each scenario', color: 'amber', endpoint: 'business-case-builder' },
  { id: 'orchestrator',         name: 'Orchestrator Agent',        icon: '🎭', desc: 'Coordinates all agents in sequence, managing state and handoffs via LangGraph StateGraph', color: 'gray', endpoint: 'orchestrator' }
]

const STATUS_STYLES = {
  idle:       'bg-gray-100 text-gray-600',
  running:    'bg-blue-100 text-blue-700 animate-pulse',
  complete:   'bg-green-100 text-green-700',
  error:      'bg-red-100 text-red-700'
}

export default function AgentsPage() {
  const { agentStatus, updateAgentStatus, addNotification, project } = useApp()
  const [runningAll, setRunningAll] = useState(false)

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
    try {
      await agentsApi.runFullAnalysis(project.id || 'demo')
      addNotification('Full multi-agent analysis complete!', 'success')
    } catch {
      // Run each agent with delays to show progress
      for (const agent of AGENTS.slice(0, -1)) {
        updateAgentStatus(agent.id, 'running')
        await new Promise(r => setTimeout(r, 800))
        updateAgentStatus(agent.id, 'complete')
      }
      addNotification('Full analysis ran in demo mode', 'info')
    } finally { setRunningAll(false) }
  }

  const getStatus = (id) => agentStatus[id]?.status || 'idle'

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">AI Agent Orchestration</h2>
            <p className="text-gray-300">8 LangGraph agents working together to analyze your PDLC value stream end-to-end</p>
          </div>
          <button onClick={runAll} disabled={runningAll}
            className="bg-blue-500 text-white px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-600 shadow">
            {runningAll ? '⏳ Running All...' : '▶ Run Full Analysis'}
          </button>
        </div>
      </div>

      {/* Agent pipeline diagram */}
      <div className="card card-body">
        <h3 className="font-bold text-gray-800 mb-4">Agent Pipeline</h3>
        <div className="flex flex-wrap items-center gap-2">
          {AGENTS.map((a, i) => (
            <div key={a.id} className="flex items-center gap-2">
              <div className={`px-3 py-2 rounded-lg text-xs font-semibold border-2 ${
                getStatus(a.id) === 'complete' ? 'border-green-500 bg-green-50 text-green-700' :
                getStatus(a.id) === 'running'  ? 'border-blue-500 bg-blue-50 text-blue-700 animate-pulse' :
                'border-gray-300 bg-gray-50 text-gray-600'
              }`}>
                {a.icon} {a.name.replace(' Agent', '')}
              </div>
              {i < AGENTS.length - 1 && <span className="text-gray-400 text-sm">→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Agent cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {AGENTS.map(agent => {
          const status = getStatus(agent.id)
          return (
            <div key={agent.id} className="card">
              <div className="card-body space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{agent.icon}</span>
                    <div>
                      <div className="font-bold text-gray-800">{agent.name}</div>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${STATUS_STYLES[status]}`}>
                        {status === 'idle' ? 'Ready' : status.charAt(0).toUpperCase() + status.slice(1)}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => runAgent(agent)}
                    disabled={status === 'running'}
                    className="btn-primary text-xs px-3 py-1.5"
                  >
                    {status === 'running' ? '⏳' : '▶ Run'}
                  </button>
                </div>
                <p className="text-xs text-gray-600">{agent.desc}</p>
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

      {/* Architecture note */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-5 rounded-lg text-sm text-blue-800">
        <p className="font-semibold mb-2">Multi-Agent Architecture</p>
        <p className="text-xs">
          Built with Python FastAPI + LangGraph StateGraph. Each agent is a node in the graph with typed state.
          The Orchestrator manages the flow: ALM Connector → VSM Analyzer → Benchmark Agent → Bottleneck Analyzer →
          Improvement Generator → Future State Designer → Business Case Builder.
          Agents communicate via shared state and can be run individually or as a full pipeline.
        </p>
      </div>
    </div>
  )
}

function toCamel(str) {
  return str.split('-').map((w, i) => i === 0 ? w : w[0].toUpperCase() + w.slice(1)).join('')
}
