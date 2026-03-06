import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

const DEFAULT_IMPROVEMENTS = [
  {
    id: 'imp-1', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Automated Performance Testing',
    priority: 'High', title: 'Deploy AI Performance Analyzer',
    problem: '16–40 hrs effort; manual performance test authoring and analysis',
    improvement: 'Deploy AI Performance Analyzer to auto-detect regressions, correlate metrics with code changes, and suggest root-cause optimizations. Reduces effort to 4–8 hrs.',
    agent: 'AI Performance Analyzer', type: 'AI Automation',
    expectedPTReduction: 75, expectedWTReduction: 60,
    category: 'GenAI / AI Automation', timeToValue: '4–6 weeks',
    roi: '3.2×', effort: 'Medium'
  },
  {
    id: 'imp-2', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Manual SIT / UAT / NF Signoff',
    priority: 'High', title: 'AI UAT Assistant + Risk-Based Signoff',
    problem: '2–5 day wait for human UAT approval; manual test consolidation',
    improvement: 'Implement AI UAT Assistant that auto-consolidates results, generates risk-scored readiness reports, enabling same-day signoff with exception-only human review.',
    agent: 'AI UAT Assistant', type: 'AI Automation',
    expectedPTReduction: 50, expectedWTReduction: 80,
    category: 'AI Automation', timeToValue: '6–8 weeks',
    roi: '4.1×', effort: 'High'
  },
  {
    id: 'imp-3', phaseId: 3, phaseName: 'Code Management', activity: 'Peer Code Review',
    priority: 'High', title: 'ReviewAgent — AI-Augmented Code Review',
    problem: '4–24 hr wait for reviewer availability; inconsistent review quality',
    improvement: 'Deploy ReviewAgent to instantly analyse diffs, flag bugs/security/style issues, and produce structured review summaries. Human reviewer focuses on architecture and business logic.',
    agent: 'ReviewAgent', type: 'GenAI Agent',
    expectedPTReduction: 40, expectedWTReduction: 70,
    category: 'GenAI Agent', timeToValue: '2–3 weeks',
    roi: '5.0×', effort: 'Low'
  },
  {
    id: 'imp-4', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Test Data Generation / Management',
    priority: 'High', title: 'DataGen Agent — Synthetic Test Data',
    problem: '4–16 hr wait for test data provisioning; privacy/compliance risk with prod data',
    improvement: 'Use DataGen Agent to generate privacy-compliant synthetic data on-demand from schema constraints, eliminating provisioning queues.',
    agent: 'DataGen Agent', type: 'GenAI Agent',
    expectedPTReduction: 60, expectedWTReduction: 85,
    category: 'GenAI Agent', timeToValue: '3–4 weeks',
    roi: '3.8×', effort: 'Low'
  },
  {
    id: 'imp-5', phaseId: 6, phaseName: 'Continuous Delivery', activity: 'Release Gates / Approvals',
    priority: 'High', title: 'AI Release Manager — Automated Gate Validation',
    problem: '1–5 day wait for CAB approval; manual risk assessment',
    improvement: 'AI Release Manager auto-validates all release criteria, generates risk assessments with compliance evidence, enabling continuous deployment with automated guardrails.',
    agent: 'AI Release Manager', type: 'AI Automation',
    expectedPTReduction: 60, expectedWTReduction: 75,
    category: 'AI Automation', timeToValue: '6–10 weeks',
    roi: '2.9×', effort: 'High'
  },
  {
    id: 'imp-6', phaseId: 1, phaseName: 'Backlog & Roadmap', activity: 'Feature Definition & Refinement',
    priority: 'Medium', title: 'FeatureGen Agent — AI Feature Authoring',
    problem: '4–8 hrs effort + 1–3 day wait for PM/BA iteration cycles',
    improvement: 'FeatureGen Agent generates structured feature definitions with acceptance criteria from high-level goals, accessing user personas via RAG. Reduces iteration from days to hours.',
    agent: 'FeatureGen Agent', type: 'GenAI Agent',
    expectedPTReduction: 50, expectedWTReduction: 70,
    category: 'GenAI Agent', timeToValue: '2–4 weeks',
    roi: '3.5×', effort: 'Low'
  },
  {
    id: 'imp-7', phaseId: 3, phaseName: 'Code Management', activity: 'Coding (Feature Development)',
    priority: 'Medium', title: 'CodeGen Agent — AI-Assisted Development',
    problem: '8–32 hrs effort; boilerplate and context-switching overhead',
    improvement: 'Deploy GitHub Copilot/CodeGen Agent for real-time suggestions, boilerplate generation, refactoring, and inline documentation. Reduces development effort by 30–40%.',
    agent: 'CodeGen Agent', type: 'GenAI Agent',
    expectedPTReduction: 35, expectedWTReduction: 0,
    category: 'GenAI Agent', timeToValue: '1–2 weeks',
    roi: '4.5×', effort: 'Low'
  },
  {
    id: 'imp-8', phaseId: 4, phaseName: 'Continuous Integration', activity: 'Static Code Analysis (SAST)',
    priority: 'Medium', title: 'ML-Powered SAST — Fewer False Positives',
    problem: '1–4 hr wait; high false-positive rate forces manual triaging',
    improvement: 'Upgrade to ML-powered SAST tools that contextually prioritize vulnerabilities and auto-suggest fixes, reducing triaging overhead by 60%.',
    agent: 'AI SAST Tools', type: 'AI Automation',
    expectedPTReduction: 40, expectedWTReduction: 60,
    category: 'AI Automation', timeToValue: '3–4 weeks',
    roi: '2.5×', effort: 'Medium'
  }
]

const PRIORITY_STYLES = {
  High:   'border-l-red-500',
  Medium: 'border-l-orange-400',
  Low:    'border-l-blue-400'
}

export default function ImprovementsPage() {
  const { analysisResult, addNotification, project } = useApp()
  const [running, setRunning] = useState(false)
  const [filter, setFilter] = useState('all')
  const [phaseFilter, setPhaseFilter] = useState('all')

  const improvements = analysisResult?.improvements ?? DEFAULT_IMPROVEMENTS

  const filtered = improvements.filter(imp =>
    (filter === 'all' || imp.priority === filter) &&
    (phaseFilter === 'all' || imp.phaseId === parseInt(phaseFilter))
  )

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runImprovementGen(project.id || 'demo')
      addNotification('Improvement generation complete!', 'success')
    } catch {
      addNotification('Using built-in improvement catalogue (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Improvement Actions</h2>
            <p className="text-green-100">AI-generated improvement actions per bottleneck — focused on GenAI agents, industry best practices, and faster time-to-market</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-green-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-green-50 shadow">
            {running ? '⏳ Generating...' : '🤖 Run Improvement Agent'}
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'High Priority',  value: improvements.filter(i => i.priority === 'High').length,   color: 'red'   },
          { label: 'Medium Priority',value: improvements.filter(i => i.priority === 'Medium').length, color: 'orange'},
          { label: 'GenAI Agents',   value: improvements.filter(i => i.type === 'GenAI Agent').length,color: 'purple'},
          { label: 'AI Automation',  value: improvements.filter(i => i.type === 'AI Automation').length,color:'blue' }
        ].map(s => (
          <div key={s.label} className="card card-body text-center">
            <div className={`text-3xl font-bold text-${s.color}-600`}>{s.value}</div>
            <div className="text-xs text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 bg-white p-4 rounded-xl border border-gray-200">
        {['all','High','Medium','Low'].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-lg text-sm font-semibold ${filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {f === 'all' ? `All (${improvements.length})` : `${f} (${improvements.filter(i => i.priority === f).length})`}
          </button>
        ))}
        <select value={phaseFilter} onChange={e => setPhaseFilter(e.target.value)}
          className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm">
          <option value="all">All Phases</option>
          {PDLC_PHASES.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {filtered.map(imp => (
          <div key={imp.id} className={`card border-l-4 ${PRIORITY_STYLES[imp.priority]}`}>
            <div className="card-body space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="font-bold text-gray-800">{imp.title}</div>
                  <div className="text-xs text-gray-500">{imp.phaseName} · {imp.activity}</div>
                </div>
                <span className={`px-2 py-0.5 rounded-full text-xs font-bold border ${
                  imp.priority === 'High' ? 'bg-red-100 text-red-700 border-red-300' : 'bg-orange-100 text-orange-700 border-orange-300'
                }`}>{imp.priority}</span>
              </div>

              <div className="bg-red-50 rounded p-3 text-xs border border-red-100">
                <span className="font-semibold text-red-700">Problem: </span>{imp.problem}
              </div>
              <div className="bg-green-50 rounded p-3 text-xs border border-green-100">
                <span className="font-semibold text-green-700">Improvement: </span>{imp.improvement}
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs">
                <div className="bg-gray-50 rounded p-2 text-center">
                  <div className="font-bold text-blue-600">-{imp.expectedPTReduction}%</div>
                  <div className="text-gray-500">PT Reduction</div>
                </div>
                <div className="bg-gray-50 rounded p-2 text-center">
                  <div className="font-bold text-red-600">-{imp.expectedWTReduction}%</div>
                  <div className="text-gray-500">WT Reduction</div>
                </div>
                <div className="bg-gray-50 rounded p-2 text-center">
                  <div className="font-bold text-green-600">{imp.roi}</div>
                  <div className="text-gray-500">Est. ROI</div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 text-xs">
                <span className={imp.type === 'GenAI Agent' ? 'tag-agent' : 'tag-ai'}>{imp.agent}</span>
                <span className="tag-process">⏱ {imp.timeToValue}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${
                  imp.effort === 'Low' ? 'bg-green-100 text-green-700 border-green-300' :
                  imp.effort === 'High' ? 'bg-red-100 text-red-700 border-red-300' :
                  'bg-yellow-100 text-yellow-700 border-yellow-300'
                }`}>{imp.effort} effort</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-4">
        <Link to="/future-state"  className="btn-primary flex-1 text-center py-3">🔮 Design Future State →</Link>
        <Link to="/bottlenecks"   className="btn-secondary flex-1 text-center py-3">← Bottlenecks</Link>
      </div>
    </div>
  )
}
