import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'

// ── What information is needed and why ────────────────────────────────────────
const CONTEXT_SECTIONS = [
  {
    id: 'team', icon: '👥', label: 'Team Profile',
    accuracy: '+15%',
    desc: 'Who is on the team — sizes, roles, and seniority shape every RACI and sprint timeline',
    fields: [
      { key: 'team_name',    label: 'Team Name',           type: 'text',   placeholder: 'e.g. Team Phoenix',   autoFill: 'team' },
      { key: 'organization', label: 'Organisation',        type: 'text',   placeholder: 'e.g. Acme Bank',      autoFill: 'organization' },
      { key: 'portfolio',    label: 'Portfolio',           type: 'text',   placeholder: 'e.g. Digital Banking', autoFill: 'portfolio' },
      { key: 'product_group',label: 'Product Group',       type: 'text',   placeholder: 'e.g. Payments',       autoFill: 'productGroup' },
      { key: 'team_size',    label: 'Team Size (headcount)',type: 'number', placeholder: 'e.g. 12' },
      { key: 'team_roles',   label: 'Current Roles (list)', type: 'text',  placeholder: 'Product Owner, 2× Dev, QA, DevOps, BA, Scrum Master' },
      { key: 'team_seniority',label: 'Seniority Mix',     type: 'select', options: ['Mostly junior (0–2yr)', 'Mixed (2–5yr avg)', 'Mostly senior (5yr+)', 'Expert / Principal mix'] },
      { key: 'industry',     label: 'Industry',            type: 'text',   placeholder: 'e.g. Financial Services', autoFill: 'industry' },
    ]
  },
  {
    id: 'tech', icon: '🛠️', label: 'Technology Stack',
    accuracy: '+12%',
    desc: 'Knowing your actual tools prevents generic recommendations — we use your tool names throughout the playbook',
    fields: [
      { key: 'source_control',label: 'Source Control',    type: 'select', options: ['GitHub', 'GitHub Enterprise', 'GitLab', 'Bitbucket', 'Azure DevOps (Repos)', 'Other'] },
      { key: 'cicd_platform', label: 'CI/CD Platform',    type: 'select', options: ['GitHub Actions', 'Azure Pipelines', 'Jenkins', 'GitLab CI', 'CircleCI', 'TeamCity', 'Buildkite', 'Other'] },
      { key: 'cloud_platform',label: 'Cloud Platform',    type: 'select', options: ['AWS', 'Microsoft Azure', 'Google Cloud (GCP)', 'On-premises', 'Multi-cloud', 'Hybrid'] },
      { key: 'alm_tool',      label: 'ALM / Project Tool',type: 'select', options: ['Jira', 'Azure DevOps (Boards)', 'Linear', 'Shortcut', 'GitHub Projects', 'Rally', 'Other'], autoFill: 'almTool' },
      { key: 'languages',     label: 'Primary Languages / Frameworks', type: 'text', placeholder: 'e.g. Java / Spring Boot, React, Python' },
      { key: 'monitoring_tools',label: 'Monitoring / Observability', type: 'text', placeholder: 'e.g. Datadog, Dynatrace, Splunk, New Relic' },
      { key: 'testing_tools', label: 'Testing Tools',     type: 'text',   placeholder: 'e.g. Jest, Selenium, Playwright, JUnit, Postman' },
      { key: 'existing_ai_licences', label: 'Existing AI Licences (if any)', type: 'text', placeholder: 'e.g. GitHub Copilot, Azure OpenAI API, Copilot for M365' },
    ]
  },
  {
    id: 'budget', icon: '💰', label: 'Budget & Procurement',
    accuracy: '+8%',
    desc: 'Shapes tool selection order and procurement risk mitigations in the playbook',
    fields: [
      { key: 'budget_available',    label: 'Budget Available / Approved', type: 'select', options: ['< $50K', '$50K–$200K', '$200K–$500K', '$500K–$1M', '$1M–$2M', '$2M+', 'Not yet approved'] },
      { key: 'procurement_process', label: 'Procurement Complexity',      type: 'select', options: ['Fast (< 1 week — team card)', 'Standard (2–4 weeks — single approval)', 'Complex (4–8 weeks — committee)', 'Enterprise (8+ weeks — procurement + legal)'] },
      { key: 'timeline_constraint', label: 'Hard Deadline / Constraint',  type: 'text',   placeholder: 'e.g. Must show ROI before Q3 budget review' },
      { key: 'existing_ai_licences_detail', label: 'Unused Licence Capacity', type: 'text', placeholder: 'e.g. 50 unused Copilot seats in enterprise agreement' },
    ]
  },
  {
    id: 'security', icon: '🔒', label: 'Security & Compliance',
    accuracy: '+10%',
    desc: 'Compliance constraints determine which DevSecOps steps are mandatory vs optional and which AI tools can be used',
    fields: [
      { key: 'compliance_frameworks', label: 'Compliance Frameworks in Scope', type: 'text', placeholder: 'e.g. SOC2 Type II, GDPR, PCI-DSS, ISO 27001, HIPAA' },
      { key: 'change_approval',       label: 'Change Approval Process',    type: 'select', options: ['Fully automated (no CAB)', 'Lightweight review (team lead only)', 'Standard CAB (weekly)', 'Full enterprise CAB (bi-weekly)', 'Regulatory gated (external audit)'] },
      { key: 'data_residency',        label: 'Data Residency Requirement', type: 'select', options: ['No constraint', 'National (same country only)', 'Regional (e.g. EU only)', 'On-premises required', 'Specific cloud region required'] },
      { key: 'ai_data_policy',        label: 'AI / LLM Data Policy',      type: 'select', options: ['Open (any cloud AI allowed)', 'Enterprise-only (Microsoft/Google/AWS)', 'Private deployment required', 'No AI data policy yet', 'Restricted / regulated data concerns'] },
    ]
  },
  {
    id: 'culture', icon: '🌱', label: 'Org Culture & Change Readiness',
    accuracy: '+12%',
    desc: 'The most accurate predictor of playbook success — shapes change management steps, risk register, and sprint pacing',
    fields: [
      { key: 'team_maturity',        label: 'Team Maturity Level',         type: 'select', options: ['Forming (new team, establishing norms)', 'Storming (conflict and misalignment common)', 'Norming (finding rhythm, some friction)', 'Performing (high trust, predictable delivery)', 'Transforming (actively seeking step-change)'] },
      { key: 'previous_ai_attempts', label: 'Previous AI / Automation Attempts', type: 'select', options: ['None attempted yet', 'Tried and abandoned (describe below)', 'Partial adoption (some tools in use)', 'Good progress (multiple tools active)', 'Advanced (AI already embedded in WoW)'] },
      { key: 'ai_attempt_detail',    label: 'Detail on Previous Attempts (if any)', type: 'textarea', placeholder: 'What was tried, why it worked or failed. This critically shapes the risk register.' },
      { key: 'leadership_sponsorship',label: 'Leadership Sponsorship',     type: 'select', options: ['Active champion (senior leader publicly backing this)', 'Passive support (approved but not visible)', 'Neutral (leadership aware but not engaged)', 'Sceptical (needs to see ROI first)', 'Resistant (requires cultural shift at top)'] },
      { key: 'training_availability', label: 'Training Time Available',    type: 'select', options: ['< 1 hr/week per person', '1–2 hrs/week', '2–4 hrs/week', '4–8 hrs/week', 'Dedicated block (full sprint available)'] },
      { key: 'change_management_support', label: 'Change Management Support', type: 'select', options: ['None (team doing it themselves)', 'Internal change manager available', 'Scrum Master / Agile Coach available', 'Dedicated transformation team', 'External consultant engaged'] },
    ]
  },
  {
    id: 'wow', icon: '🔄', label: 'Ways of Working',
    accuracy: '+8%',
    desc: 'Sprint timing and release process determine playbook cadence and which automations to prioritise first',
    fields: [
      { key: 'methodology',    label: 'Development Methodology', type: 'select', options: ['Scrum', 'Kanban', 'Scrumban', 'SAFe', 'Shape Up', 'DSDM / Prince2 Agile', 'Waterfall / Hybrid', 'Ad hoc'] },
      { key: 'sprint_length',  label: 'Sprint / Iteration Length', type: 'select', options: ['1 week', '2 weeks', '3 weeks', '4 weeks', 'Continuous flow (no fixed sprint)'] },
      { key: 'deploy_frequency',label: 'Current Deployment Frequency', type: 'select', options: ['Multiple per day', 'Daily', 'Several per week', 'Weekly', 'Bi-weekly', 'Monthly', 'Less than monthly'] },
      { key: 'release_process', label: 'Release / Change Process',    type: 'select', options: ['Fully automated (no human gate)', 'Automated with manual approval on high-risk', 'Semi-automated (human runs pipeline)', 'Manual CAB approval required', 'Separate release team / release manager'] },
      { key: 'team_ceremonies', label: 'Current Ceremonies Running',   type: 'text', placeholder: 'e.g. Daily standup, 2-weekly sprint review, monthly OKR check-in' },
    ]
  },
  {
    id: 'stakeholders', icon: '🎯', label: 'Stakeholder Context',
    accuracy: '+5%',
    desc: 'Success criteria and known concerns drive executive summary framing and risk mitigations',
    fields: [
      { key: 'key_sponsors',    label: 'Key Sponsors / Decision Makers', type: 'text', placeholder: 'e.g. CTO (Jane Smith), Engineering VP (John Doe)' },
      { key: 'known_concerns',  label: 'Known Concerns / Objections',    type: 'textarea', placeholder: 'e.g. "AI will replace jobs", "data privacy concerns with cloud AI", "previous tool initiatives failed"' },
      { key: 'success_criteria',label: 'Success Criteria from Leadership', type: 'textarea', placeholder: 'e.g. Must reduce lead time by 30% within 6 months. Must show ROI before Q3 budget review.' },
    ]
  },
]

const REQUIRED_DOCS = [
  { key: 'org_chart',            label: 'Org Chart / Team Roster',       accuracy: '+4%', icon: '🏢', desc: 'Personalises RACI with real names and reporting lines', where: 'HR system, org wiki, or Confluence team page' },
  { key: 'engineering_standards',label: 'Engineering Standards / Tech Playbook', accuracy: '+4%', icon: '📐', desc: 'Avoids recommending practices already in your standards; surfaces gaps', where: 'Engineering wiki, GitHub repo README, or Confluence' },
  { key: 'tool_inventory',       label: 'Tool & Licence Inventory',      accuracy: '+4%', icon: '📋', desc: 'Prevents duplicate procurement; identifies unused licence capacity', where: 'IT Asset Management (ITAM) system or procurement register' },
  { key: 'security_policy',      label: 'Security & Compliance Policy',  accuracy: '+4%', icon: '🔐', desc: 'Tailors DevSecOps actions to your actual mandatory controls', where: 'Security team SharePoint, Confluence, or InfoSec portal' },
  { key: 'okrs_goals',           label: 'Annual OKRs / Strategic Goals', accuracy: '+4%', icon: '🎯', desc: 'Aligns sprint outcomes and success metrics to business objectives', where: 'OKR tool (Notion, Confluence, Gtmhub, Jira Goals)' },
  { key: 'dora_report',          label: 'DORA Metrics Report',           accuracy: '+3%', icon: '📊', desc: 'Sharpens baseline comparisons with measured deployment frequency and MTTR', where: 'Sleuth, LinearB, Jellyfish, or GitHub Insights dashboard' },
  { key: 'retro_notes',          label: 'Sprint Retrospective Notes (last 2)', accuracy: '+5%', icon: '🔁', desc: 'Surfaces team pain points and culture signals the VSM metrics cannot capture', where: 'Miro, EasyRetro, FunRetro, or Confluence retrospective pages' },
]

// ── Refined Playbook Display ──────────────────────────────────────────────────
function RefinedPlaybook({ playbook, scenarioLabel }) {
  const [openSprint, setOpenSprint] = useState(null)

  if (!playbook) return null

  const accPct   = playbook.accuracy_pct || 70
  const accColor = accPct >= 85 ? 'green' : accPct >= 70 ? 'amber' : 'red'

  return (
    <div className="space-y-6 fade-in">
      {/* Accuracy badge + summary */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start gap-6">
          <div className="text-center shrink-0">
            <div className={`text-4xl font-black text-${accColor}-300`}>{accPct}%</div>
            <div className="text-xs text-indigo-200 mt-0.5">Accuracy</div>
            <div className={`mt-2 px-3 py-1 rounded-full text-xs font-bold ${
              accPct >= 85 ? 'bg-green-500' : accPct >= 70 ? 'bg-amber-500' : 'bg-red-500'
            }`}>
              {accPct >= 85 ? 'High Confidence' : accPct >= 70 ? 'Good — add docs to improve' : 'Partial — needs more context'}
            </div>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-white/20 px-2 py-0.5 rounded text-xs font-bold">Refined Playbook</span>
              <span className="text-indigo-200 text-sm">— {scenarioLabel}</span>
            </div>
            <p className="text-indigo-100 text-sm leading-relaxed">{playbook.executive_summary}</p>
            <div className="mt-3 flex items-center gap-4 text-xs text-indigo-200">
              <span>⏱ Recommended duration: <strong className="text-white">{playbook.duration_recommendation}</strong></span>
            </div>
          </div>
        </div>
      </div>

      {/* Document gaps (if any) */}
      {playbook.document_gaps?.length > 0 && (
        <div className="bg-amber-50 border border-amber-300 rounded-xl p-4">
          <div className="font-bold text-amber-800 mb-2 text-sm">📎 Add these documents to reach 90%+ accuracy:</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {playbook.document_gaps.map((g, i) => (
              <div key={i} className="bg-white rounded-lg border border-amber-200 p-3 text-xs">
                <div className="font-bold text-amber-900">{g.document}</div>
                <div className="text-gray-600 mt-0.5">{g.why_needed}</div>
                <div className="text-amber-700 mt-1 italic">Get from: {g.where_to_get}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Wins */}
      {playbook.quick_wins?.length > 0 && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">⚡ Quick Wins — Start Today</h3></div>
          <div className="card-body grid grid-cols-1 md:grid-cols-2 gap-3">
            {playbook.quick_wins.map((qw, i) => (
              <div key={i} className="bg-green-50 border border-green-200 rounded-xl p-4">
                <div className="flex items-start gap-2 mb-2">
                  <span className="bg-green-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0">{i+1}</span>
                  <div className="font-semibold text-green-800 text-sm">{qw.action}</div>
                </div>
                <div className="flex gap-3 text-xs flex-wrap">
                  <span className="bg-white border border-green-200 px-2 py-0.5 rounded">👤 {qw.owner}</span>
                  <span className="bg-white border border-green-200 px-2 py-0.5 rounded">⏱ {qw.timeframe}</span>
                  <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded font-semibold">{qw.expected_impact}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Target Metrics */}
      {playbook.target_metrics?.length > 0 && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">📊 Target VSM Metrics — Your Personalised Targets</h3></div>
          <div className="card-body overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b-2 border-gray-200 text-xs font-semibold text-gray-600">
                  <th className="text-left py-2 pr-4">Metric</th>
                  <th className="text-center py-2 px-3">Your Baseline</th>
                  <th className="text-center py-2 px-3">Target</th>
                  <th className="text-center py-2 px-3">Improvement</th>
                  <th className="text-left py-2 pl-3">How to Measure in Your Tools</th>
                </tr>
              </thead>
              <tbody>
                {playbook.target_metrics.map((m, i) => (
                  <tr key={i} className={`border-b border-gray-100 ${i % 2 === 0 ? 'bg-gray-50' : ''}`}>
                    <td className="py-2.5 pr-4 font-semibold text-gray-800">{m.metric}</td>
                    <td className="py-2.5 px-3 text-center text-gray-600">{m.baseline}</td>
                    <td className="py-2.5 px-3 text-center font-bold text-green-700">{m.target}</td>
                    <td className="py-2.5 px-3 text-center"><span className="bg-green-100 text-green-800 px-2 py-0.5 rounded font-bold text-xs">{m.reduction}</span></td>
                    <td className="py-2.5 pl-3 text-gray-600 text-xs">{m.measure}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Sprint Plan */}
      {playbook.sprint_plan?.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="font-bold text-gray-800">🗓 Personalised Sprint Plan</h3>
            <p className="text-xs text-gray-500">Actions reference your specific tools, team, and bottlenecks</p>
          </div>
          <div className="card-body space-y-3">
            {playbook.sprint_plan.map((sp, idx) => (
              <div key={idx} className="border border-gray-200 rounded-xl overflow-hidden">
                <button onClick={() => setOpenSprint(openSprint === idx ? null : idx)}
                  className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50 text-left">
                  <div className="w-8 h-8 bg-indigo-600 text-white rounded-lg flex items-center justify-center font-bold text-sm shrink-0">{idx+1}</div>
                  <div className="flex-1">
                    <div className="font-semibold text-gray-800">{sp.sprint} — {sp.label}</div>
                    <div className="text-xs text-gray-500">{sp.actions?.length || 0} actions · {sp.outcomes?.length || 0} outcomes</div>
                  </div>
                  <span className="text-gray-400">{openSprint === idx ? '▲' : '▼'}</span>
                </button>
                {openSprint === idx && (
                  <div className="border-t border-gray-100 px-5 pb-5">
                    <div className="mt-4 space-y-2.5">
                      {sp.actions?.map((a, ai) => (
                        <div key={ai} className="bg-indigo-50 border border-indigo-200 rounded-lg p-3">
                          <div className="flex items-start gap-3">
                            <span className="bg-indigo-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5">{ai+1}</span>
                            <div>
                              <div className="text-xs font-bold text-indigo-900 mb-1">{a.who}</div>
                              <div className="text-sm text-gray-700">{a.what}</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    {sp.outcomes?.length > 0 && (
                      <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                        <div className="text-xs font-semibold text-green-800 mb-1">Sprint Outcomes:</div>
                        <ul className="space-y-0.5">{sp.outcomes.map((o, oi) => (
                          <li key={oi} className="flex items-center gap-2 text-xs text-green-700"><span className="text-green-500">✓</span>{o}</li>
                        ))}</ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* RACI */}
      {playbook.raci?.length > 0 && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">📋 RACI — Roles & Responsibilities</h3></div>
          <div className="card-body overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b-2 border-gray-200">
                  <th className="text-left py-2 pr-4 font-semibold text-gray-700">Activity</th>
                  <th className="text-center py-2 px-2 font-semibold text-blue-700">Responsible</th>
                  <th className="text-center py-2 px-2 font-semibold text-purple-700">Accountable</th>
                  <th className="text-center py-2 px-2 font-semibold text-amber-700">Consulted</th>
                  <th className="text-center py-2 px-2 font-semibold text-gray-500">Informed</th>
                </tr>
              </thead>
              <tbody>
                {playbook.raci.map((row, i) => (
                  <tr key={i} className={`border-b border-gray-100 ${i%2===0?'bg-gray-50':''}`}>
                    <td className="py-2.5 pr-4 font-medium text-gray-800">{row.activity}</td>
                    <td className="py-2.5 px-2 text-center text-blue-700 font-semibold">{row.r}</td>
                    <td className="py-2.5 px-2 text-center text-purple-700 font-semibold">{row.a}</td>
                    <td className="py-2.5 px-2 text-center text-amber-700">{row.c}</td>
                    <td className="py-2.5 px-2 text-center text-gray-500">{row.i}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Risks */}
      {playbook.risks?.length > 0 && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">⚠️ Risk Register — Personalised to Your Context</h3></div>
          <div className="card-body space-y-3">
            {playbook.risks.map((r, i) => {
              const col = r.severity === 'Critical' ? 'red' : r.severity === 'High' ? 'orange' : 'amber'
              return (
                <div key={i} className={`rounded-xl border p-4 bg-${col}-50 border-${col}-200`}>
                  <div className="flex items-start gap-3">
                    <span className={`bg-${col}-600 text-white text-xs font-bold px-2 py-0.5 rounded-full shrink-0`}>{r.severity}</span>
                    <div>
                      <div className={`font-bold text-${col}-800 text-sm mb-1`}>{r.risk}</div>
                      <div className="text-sm text-gray-700"><span className="font-semibold text-gray-600">Mitigation: </span>{r.mitigation}</div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function PlaybookContextPage() {
  const { project, analysisResult, activeScenario } = useApp()
  const navigate = useNavigate()
  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)

  // Pre-populate form with known project data
  const buildInitialForm = () => {
    const init = {}
    CONTEXT_SECTIONS.forEach(sec =>
      sec.fields.forEach(f => {
        if (f.autoFill && project[f.autoFill]) init[f.key] = project[f.autoFill]
        else init[f.key] = ''
      })
    )
    return init
  }

  const [formData, setFormData]       = useState(buildInitialForm)
  const [documents, setDocuments]     = useState({})
  const [openSection, setOpenSection] = useState('team')
  const [openDoc, setOpenDoc]         = useState(null)
  const [generating, setGenerating]   = useState(false)
  const [refinedPlaybook, setPlaybook]= useState(null)
  const [error, setError]             = useState(null)

  // Calculate how much context has been provided
  const allFormFields = CONTEXT_SECTIONS.flatMap(s => s.fields.map(f => f.key))
  const filledFields  = allFormFields.filter(k => formData[k]?.trim()).length
  const filledDocs    = Object.values(documents).filter(v => v?.trim()).length
  const docAccuracy   = filledDocs * 4
  const fieldAccuracy = Math.round((filledFields / allFormFields.length) * 60)
  const currentAccuracy = Math.min(30 + fieldAccuracy + docAccuracy, 95)

  const setField = (key, value) => setFormData(f => ({ ...f, [key]: value }))

  const handleGenerate = async () => {
    setGenerating(true)
    setError(null)
    try {
      const analysis_context = {
        project,
        metrics:      analysisResult?.metrics || {},
        bottlenecks:  analysisResult?.bottlenecks || [],
        improvements: analysisResult?.improvements || [],
        future_states:analysisResult?.future_states || {},
        business_cases:analysisResult?.business_cases || {},
      }
      const { data } = await axios.post(
        `/api/v1/agents/contextualise-playbook/${project.id || 'demo'}`,
        {
          scenario_id:    activeScenario,
          scenario_label: scenario?.label + ' — ' + scenario?.title,
          analysis_context,
          team_context:  formData,
          documents,
        }
      )
      setPlaybook(data)
      // scroll to result
      setTimeout(() => document.getElementById('refined-playbook')?.scrollIntoView({ behavior: 'smooth' }), 200)
    } catch (err) {
      setError('Failed to generate playbook. Please check the backend is running.')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-violet-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Playbook Contextualiser</h2>
            <p className="text-indigo-100">
              Provide team context to generate a personalised 90%+ accurate implementation playbook for{' '}
              <strong>{scenario?.label} — {scenario?.title}</strong>
            </p>
          </div>
          <Link to="/business-case" className="bg-white/20 hover:bg-white/30 text-white text-sm font-semibold px-4 py-2 rounded-lg">
            ← Business Case
          </Link>
        </div>
      </div>

      {/* Live accuracy gauge */}
      <div className="card card-body">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="font-bold text-gray-800 text-lg">{currentAccuracy}% Accuracy</span>
            <span className="text-sm text-gray-500 ml-2">— estimated contextualisation level</span>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold ${
            currentAccuracy >= 85 ? 'bg-green-100 text-green-800' :
            currentAccuracy >= 70 ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-600'
          }`}>
            {currentAccuracy >= 85 ? 'High confidence — ready to generate' :
             currentAccuracy >= 70 ? 'Good — add more for better accuracy' : 'Fill in more context to improve'}
          </span>
        </div>
        <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              currentAccuracy >= 85 ? 'bg-green-500' : currentAccuracy >= 70 ? 'bg-amber-500' : 'bg-indigo-500'
            }`}
            style={{ width: `${currentAccuracy}%` }}
          />
        </div>
        <div className="mt-2 flex gap-4 text-xs text-gray-500">
          <span>✅ 30% — current-state analysis (auto)</span>
          <span>📝 {fieldAccuracy}% — form context ({filledFields}/{allFormFields.length} fields)</span>
          <span>📎 {docAccuracy}% — documents ({filledDocs}/{REQUIRED_DOCS.length} provided)</span>
        </div>
      </div>

      {/* Context form sections */}
      <div className="space-y-3">
        {CONTEXT_SECTIONS.map(sec => (
          <div key={sec.id} className="border border-gray-200 rounded-xl overflow-hidden bg-white">
            <button
              onClick={() => setOpenSection(openSection === sec.id ? null : sec.id)}
              className="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 text-left"
            >
              <span className="text-2xl">{sec.icon}</span>
              <div className="flex-1">
                <div className="font-bold text-gray-800">{sec.label}</div>
                <div className="text-xs text-gray-500 mt-0.5">{sec.desc}</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-0.5 rounded-full">{sec.accuracy} accuracy</span>
                <span className="text-xs text-gray-400">
                  {sec.fields.filter(f => formData[f.key]?.trim()).length}/{sec.fields.length} filled
                </span>
                <span className="text-gray-400">{openSection === sec.id ? '▲' : '▼'}</span>
              </div>
            </button>
            {openSection === sec.id && (
              <div className="border-t border-gray-100 px-5 pb-5 pt-4 grid grid-cols-1 md:grid-cols-2 gap-4 slide-down">
                {sec.fields.map(f => (
                  <div key={f.key} className={f.type === 'textarea' ? 'md:col-span-2' : ''}>
                    <label className="text-xs font-semibold text-gray-700 block mb-1">
                      {f.label}
                      {f.autoFill && formData[f.key] && <span className="ml-2 text-green-600 font-normal">✓ auto-filled</span>}
                    </label>
                    {f.type === 'select' ? (
                      <select
                        value={formData[f.key] || ''}
                        onChange={e => setField(f.key, e.target.value)}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500"
                      >
                        <option value="">— Select —</option>
                        {f.options.map(o => <option key={o} value={o}>{o}</option>)}
                      </select>
                    ) : f.type === 'textarea' ? (
                      <textarea
                        value={formData[f.key] || ''}
                        onChange={e => setField(f.key, e.target.value)}
                        placeholder={f.placeholder}
                        rows={3}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500 resize-none"
                      />
                    ) : (
                      <input
                        type={f.type}
                        value={formData[f.key] || ''}
                        onChange={e => setField(f.key, e.target.value)}
                        placeholder={f.placeholder}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500"
                      />
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Document section */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">📎 Supporting Documents</h3>
          <p className="text-xs text-gray-500">Paste document content below — each document adds ~4% accuracy by personalising specific playbook sections</p>
        </div>
        <div className="card-body space-y-3">
          {REQUIRED_DOCS.map(doc => (
            <div key={doc.key} className="border border-gray-200 rounded-xl overflow-hidden">
              <button
                onClick={() => setOpenDoc(openDoc === doc.key ? null : doc.key)}
                className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 text-left"
              >
                <span className="text-xl">{doc.icon}</span>
                <div className="flex-1">
                  <div className="font-semibold text-gray-800 text-sm">{doc.label}</div>
                  <div className="text-xs text-gray-500">{doc.desc}</div>
                </div>
                <div className="flex items-center gap-2">
                  {documents[doc.key]?.trim() ? (
                    <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded-full">✓ Provided</span>
                  ) : (
                    <span className="bg-gray-100 text-gray-500 text-xs px-2 py-0.5 rounded-full">Optional</span>
                  )}
                  <span className="bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-0.5 rounded-full">{doc.accuracy}</span>
                  <span className="text-gray-400">{openDoc === doc.key ? '▲' : '▼'}</span>
                </div>
              </button>
              {openDoc === doc.key && (
                <div className="border-t border-gray-100 px-4 pb-4 pt-3 slide-down">
                  <div className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mb-3">
                    <span className="font-bold">Where to get this: </span>{doc.where}
                  </div>
                  <textarea
                    value={documents[doc.key] || ''}
                    onChange={e => setDocuments(d => ({ ...d, [doc.key]: e.target.value }))}
                    placeholder={`Paste the content of your ${doc.label} here. Key sections, bullet points, or full text are all useful.`}
                    rows={5}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500 resize-none font-mono"
                  />
                  <div className="text-xs text-gray-400 mt-1">{(documents[doc.key] || '').length} characters pasted</div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Generate button */}
      {error && <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">{error}</div>}
      <div className="bg-white border-2 border-indigo-200 rounded-2xl p-6 text-center">
        <div className="text-gray-700 text-sm mb-4">
          Ready to generate at <strong className="text-indigo-700">{currentAccuracy}% accuracy</strong>.{' '}
          {currentAccuracy < 70 && 'Fill in more context sections to improve the playbook quality.'}
          {currentAccuracy >= 70 && currentAccuracy < 90 && 'Add the remaining documents to push above 90%.'}
          {currentAccuracy >= 90 && 'Excellent coverage — this playbook will be highly personalised.'}
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="btn-primary px-10 py-3 text-base font-bold disabled:opacity-60"
        >
          {generating ? '⏳ Generating Refined Playbook...' : `🚀 Generate ${currentAccuracy}% Accurate Playbook`}
        </button>
        <div className="text-xs text-gray-400 mt-2">Powered by Azure GPT-4o · Rule-based fallback if unavailable</div>
      </div>

      {/* Refined Playbook Output */}
      {refinedPlaybook && (
        <div id="refined-playbook">
          <div className="border-t-2 border-indigo-200 pt-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Refined Implementation Playbook</h3>
            <RefinedPlaybook playbook={refinedPlaybook} scenarioLabel={scenario?.label + ' — ' + scenario?.title} />
          </div>
        </div>
      )}

      <div className="flex gap-4 pb-8">
        <Link to="/business-case" className="btn-secondary flex-1 text-center py-3">← Back to Business Case</Link>
      </div>
    </div>
  )
}
