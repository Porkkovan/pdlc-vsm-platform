import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import * as XLSX from 'xlsx'
import TargetStepBar from '../components/TargetStepBar'
import { useTargetScenario } from '../components/useTargetScenario'
import StepReviewBar from '../components/StepReviewBar'
import InlineEditModal from '../components/common/InlineEditModal'

// Option B/C Compliance & Governance recommendations (static, always shown when relevant)
const COMPLIANCE_GOV_RECS = [
  {
    id: 'cg-1', tier: 'Option B/C', priority: 'High', icon: '🔐',
    agent: 'Secure-by-Design Architect',
    phase: 'Phase 2 — Architecture & UX / Phase 6 — Continuous Delivery',
    title: 'Enforce Security-by-Design on All IaC via Secure-by-Design Architect Agent',
    recommendation: 'Deploy the Secure-by-Design Architect Agent to auto-reject deployment configs deviating from your cloud architecture baseline. Estimated benefit: eliminates ~80% of cloud misconfiguration incidents; avg cost of a cloud misconfiguration in financial services = $500K+. Configure before Phase 2 architecture reviews begin.',
    benefit: '$100K–$200K/yr in security incident avoidance'
  },
  {
    id: 'cg-2', tier: 'Option B/C', priority: 'High', icon: '📋',
    agent: 'Compliance-as-Code Orchestrator',
    phase: 'Phase 3 — Code Management / Phase 5 — Continuous Testing',
    title: 'Shift Compliance Left with Compliance-as-Code Orchestrator',
    recommendation: 'Replace periodic manual compliance audits with continuous real-time validation via the CaC Orchestrator Agent. Validates every commit against GDPR, DORA, and Basel III. Estimated benefit: reduces manual audit effort by ~60%, eliminates last-minute compliance failures at release gates. Activate on every PR pipeline in Phase 3.',
    benefit: '$150K–$300K/yr in compliance automation savings'
  },
  {
    id: 'cg-3', tier: 'Option B/C', priority: 'High', icon: '🧬',
    agent: 'Model Risk Management (MRM) Agent',
    phase: 'Phase 5 — Continuous Testing / Phase 7 — Monitoring & Feedback',
    title: 'Implement AI Model Explainability & Kill-Switch via MRM Agent',
    recommendation: 'Activate the MRM Agent to generate Explainability Reports for every model version deployed to production. Configure automated kill-switch with dual-authorisation (MRO + CTO) for models drifting outside governed risk parameters. Critical for SR 11-7 compliance in financial services. Estimated benefit: prevents catastrophic model failures; regulatory fines avoided estimated at $200K–$400K/yr.',
    benefit: '$200K–$400K/yr in model risk avoidance'
  },
  {
    id: 'cg-4', tier: 'Option B/C', priority: 'Medium', icon: '📡',
    agent: 'Telemetry & Observability Sentinel',
    phase: 'Phase 7 — Monitoring & Feedback (cross-phase)',
    title: 'Surface Business Risk Scores from Multi-Agent Telemetry via Sentinel',
    recommendation: 'Deploy the Telemetry & Observability Sentinel to aggregate logs from all agent workflows and translate technical failures into Business Risk Scores for governance teams. Eliminates the translation gap between engineering alerts and business risk — governance boards receive real-time risk dashboards instead of raw technical metrics.',
    benefit: '$50K–$100K/yr in mean time to governance escalation reduction'
  },
  {
    id: 'cg-5', tier: 'Option B/C', priority: 'High', icon: '🏛️',
    agent: 'Multi-Agent Governance Controller',
    phase: 'All phases — orchestration layer',
    title: 'Activate Multi-Agent Governance Controller to Prevent Protocol Bypass',
    recommendation: 'The Governance Controller is the "agent of agents" — it synchronises all development and governance agents to ensure no single agent can bypass a compliance protocol. Critical for Option C at full autonomy: without it, a misconfigured dev agent could execute without compliance sign-off. Configure in shadow mode first (2 weeks), then activate enforcement. Requires CTO + CCO dual approval for any config change.',
    benefit: 'Prevents single-agent compliance bypass; mandatory for Option C'
  },
]

// Pull from improvements + all activity AI opportunities
const getAllRecs = (analysisResult) => {
  const base = PDLC_PHASES.flatMap(phase =>
    phase.activities.map(act => ({
      id: `activity-${act.id}`,
      phase: phase.name,
      activity: act.name,
      priority: 'Medium',
      title: `AI Automation: ${act.name}`,
      description: `Default effort: ${act.defaultEffort.min}–${act.defaultEffort.max}h · Wait: ${act.defaultWait.min}–${act.defaultWait.max} ${act.waitUnit}`,
      recommendation: act.aiOpportunity,
      agent: act.agent,
      type: act.type,
      source: 'Activity Opportunity'
    }))
  )
  return analysisResult?.recommendations ?? base
}

const REC_EDIT_FIELDS = [
  { key: 'priority', label: 'Priority', type: 'select', options: ['Low', 'Medium', 'High'] },
  { key: 'title', label: 'Title', type: 'text' },
  { key: 'recommendation', label: 'Recommendation', type: 'textarea', rows: 4 },
  { key: 'description', label: 'Description', type: 'textarea', rows: 2 },
  { key: 'agent', label: 'Agent / Tool', type: 'text' },
]

export default function RecommendationsPage() {
  const { analysisResult, activeScenario, setActiveScenario, project, addNotification } = useApp()
  const ts = useTargetScenario(project?.id, setActiveScenario)
  const [priorityFilter, setPriority] = useState('all')
  const [typeFilter, setType]         = useState('all')
  const [phaseFilter, setPhase]       = useState('all')
  const [search, setSearch]           = useState('')
  const [editingRec, setEditingRec]   = useState(null)
  const [recEdits, setRecEdits]       = useState({})

  const saveRecEdit = (updated) => {
    setRecEdits(prev => ({ ...prev, [updated.id]: updated }))
    addNotification(`Recommendation "${updated.title}" updated`, 'success')
  }

  const applyRecEdits = (recs) => recs.map(r => recEdits[r.id] ? { ...r, ...recEdits[r.id] } : r)

  const all = applyRecEdits(getAllRecs(analysisResult))

  const filtered = all.filter(r =>
    (priorityFilter === 'all' || r.priority === priorityFilter) &&
    (typeFilter     === 'all' || r.type     === typeFilter) &&
    (phaseFilter    === 'all' || r.phase    === phaseFilter) &&
    (!search || r.title.toLowerCase().includes(search.toLowerCase()) || r.recommendation.toLowerCase().includes(search.toLowerCase()))
  )

  const exportExcel = () => {
    const ws = XLSX.utils.aoa_to_sheet([
      ['Phase', 'Activity', 'Priority', 'Title', 'Description', 'Recommendation', 'Type', 'Agent', 'Source'],
      ...filtered.map(r => [r.phase, r.activity, r.priority, r.title, r.description, r.recommendation, r.type, r.agent, r.source])
    ])
    ws['!cols'] = [20,30,10,40,40,80,18,30,20].map(w => ({ wch: w }))
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Recommendations')
    XLSX.writeFile(wb, `STUMP_Recommendations.xlsx`)
  }

  return (
    <div className="space-y-6 fade-in">
      {ts.configured && <TargetStepBar steps={ts.steps} stepIdx={ts.stepIdx} pickStep={ts.pickStep} platform={ts.platform} />}
      <div className="bg-gradient-to-r from-green-600 to-emerald-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">All Recommendations</h2>
            <p className="text-green-100">Comprehensive AI improvement recommendations across all PDLC phases and activities</p>
          </div>
          <button onClick={exportExcel} className="bg-white text-green-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-green-50 shadow">
            📥 Export to Excel
          </button>
        </div>
      </div>

      <StepReviewBar stepKey="recommendations" stepLabel="Recommendations" />

      {/* Filters */}
      <div className="card card-body space-y-3">
        <input type="text" value={search} onChange={e => setSearch(e.target.value)}
          placeholder="Search recommendations..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        <div className="flex flex-wrap gap-3">
          {['all','High','Medium','Low'].map(f => (
            <button key={f} onClick={() => setPriority(f)}
              className={`px-4 py-1.5 rounded-lg text-sm font-semibold ${priorityFilter === f ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
              {f === 'all' ? `All Priority (${all.length})` : `${f} (${all.filter(r => r.priority === f).length})`}
            </button>
          ))}
          <select value={typeFilter} onChange={e => setType(e.target.value)}
            className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm">
            <option value="all">All Types</option>
            <option value="GenAI Agent">GenAI Agent</option>
            <option value="AI Automation">AI Automation</option>
          </select>
          <select value={phaseFilter} onChange={e => setPhase(e.target.value)}
            className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm">
            <option value="all">All Phases</option>
            {PDLC_PHASES.map(p => <option key={p.id} value={p.name}>{p.name}</option>)}
          </select>
        </div>
        <div className="text-xs text-gray-500">Showing {filtered.length} of {all.length} recommendations</div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {filtered.map(rec => (
          <div key={rec.id} className={`card border-l-4 ${
            rec.priority === 'High' ? 'border-l-red-500' : rec.priority === 'Medium' ? 'border-l-orange-400' : 'border-l-blue-400'
          }`}>
            <div className="card-body space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="font-bold text-gray-800 text-sm">{rec.title}</div>
                    <button onClick={() => setEditingRec(rec)} className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold px-1.5 py-0.5 rounded hover:bg-indigo-50" title="Edit recommendation">
                      ✏️
                    </button>
                  </div>
                  <div className="text-xs text-gray-500 mt-0.5">{rec.phase} · {rec.activity}</div>
                </div>
                <div className="flex flex-col gap-1 items-end shrink-0">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                    rec.priority === 'High' ? 'bg-sky-100 text-sky-700' : rec.priority === 'Medium' ? 'bg-teal-100 text-teal-700' : 'bg-blue-100 text-blue-700'
                  }`}>{rec.priority}</span>
                  <span className="px-2 py-0.5 rounded-full text-xs bg-purple-100 text-purple-700">{rec.source}</span>
                </div>
              </div>
              <p className="text-xs text-gray-600">{rec.description}</p>
              <div className="bg-green-50 rounded p-3 text-xs border border-green-100">
                <span className="font-semibold text-green-700">Recommendation: </span>{rec.recommendation}
              </div>
              <div className="flex items-center justify-between">
                <span className={rec.type === 'GenAI Agent' ? 'tag-agent' : 'tag-ai'}>{rec.type}</span>
                <code className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-xs">{rec.agent}</code>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Option B/C — Compliance & Governance Agent Recommendations */}
      {(activeScenario === 'option-b' || activeScenario === 'option-c') && (
        <div className="space-y-4">
          <div className="flex items-center gap-3 pt-2">
            <div className="flex-1 border-t border-indigo-200" />
            <span className="text-sm font-bold text-indigo-700 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-200">
              {activeScenario === 'option-b' ? 'Option B' : 'Option C'} — Compliance &amp; Governance Agent Recommendations
            </span>
            <div className="flex-1 border-t border-indigo-200" />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {COMPLIANCE_GOV_RECS.map(rec => (
              <div key={rec.id} className="card border-l-4 border-l-indigo-500">
                <div className="card-body space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xl shrink-0">{rec.icon}</span>
                      <div>
                        <div className="font-bold text-gray-800 text-sm">{rec.title}</div>
                        <div className="text-xs text-gray-500 mt-0.5">{rec.phase}</div>
                      </div>
                    </div>
                    <div className="flex flex-col gap-1 items-end shrink-0">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${rec.priority === 'High' ? 'bg-sky-100 text-sky-700' : 'bg-teal-100 text-teal-700'}`}>{rec.priority}</span>
                      <span className="px-2 py-0.5 rounded-full text-xs bg-indigo-100 text-indigo-700">{rec.tier}</span>
                    </div>
                  </div>
                  <div className="bg-indigo-50 rounded p-3 text-xs border border-indigo-100">
                    <span className="font-semibold text-indigo-700">Recommendation: </span>{rec.recommendation}
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="bg-green-100 text-green-700 text-xs font-semibold px-2 py-0.5 rounded">💰 {rec.benefit}</span>
                    <code className="bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded text-xs">{rec.agent}</code>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <InlineEditModal
        item={editingRec}
        fields={REC_EDIT_FIELDS}
        title={editingRec ? `Edit: ${editingRec.title}` : 'Edit Recommendation'}
        onSave={saveRecEdit}
        onClose={() => setEditingRec(null)}
      />

      {Object.keys(recEdits).length > 0 && (
        <div className="fixed bottom-4 right-4 bg-emerald-600 text-white px-4 py-2 rounded-lg shadow-lg text-xs font-semibold z-40">
          ✏️ {Object.keys(recEdits).length} recommendation{Object.keys(recEdits).length !== 1 ? 's' : ''} edited (session)
        </div>
      )}
    </div>
  )
}
