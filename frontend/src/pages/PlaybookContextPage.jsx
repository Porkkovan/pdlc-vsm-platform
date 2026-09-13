import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { STATIC_PLAYBOOKS } from '../data/playbookGuides'
import TargetStepBar from '../components/TargetStepBar'
import { useTargetScenario } from '../components/useTargetScenario'

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
  const accColor = accPct >= 85 ? 'green' : accPct >= 70 ? 'emerald' : 'sky'

  return (
    <div className="space-y-6 fade-in">
      {/* Accuracy badge + summary */}
      <div className="bg-gradient-to-r from-indigo-400 to-violet-400 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start gap-6">
          <div className="text-center shrink-0">
            <div className={`text-4xl font-black text-${accColor}-300`}>{accPct}%</div>
            <div className="text-xs text-indigo-200 mt-0.5">Accuracy</div>
            <div className={`mt-2 px-3 py-1 rounded-full text-xs font-bold ${
              accPct >= 85 ? 'bg-green-500' : accPct >= 70 ? 'bg-cyan-500' : 'bg-sky-500'
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
        <div className="bg-cyan-50 border border-cyan-300 rounded-xl p-4">
          <div className="font-bold text-cyan-800 mb-2 text-sm">📎 Add these documents to reach 90%+ accuracy:</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {playbook.document_gaps.map((g, i) => (
              <div key={i} className="bg-white rounded-lg border border-cyan-200 p-3 text-xs">
                <div className="font-bold text-cyan-900">{g.document}</div>
                <div className="text-gray-600 mt-0.5">{g.why_needed}</div>
                <div className="text-cyan-700 mt-1 italic">Get from: {g.where_to_get}</div>
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
                  <th className="text-center py-2 px-2 font-semibold text-cyan-700">Consulted</th>
                  <th className="text-center py-2 px-2 font-semibold text-gray-500">Informed</th>
                </tr>
              </thead>
              <tbody>
                {playbook.raci.map((row, i) => (
                  <tr key={i} className={`border-b border-gray-100 ${i%2===0?'bg-gray-50':''}`}>
                    <td className="py-2.5 pr-4 font-medium text-gray-800">{row.activity}</td>
                    <td className="py-2.5 px-2 text-center text-blue-700 font-semibold">{row.r}</td>
                    <td className="py-2.5 px-2 text-center text-purple-700 font-semibold">{row.a}</td>
                    <td className="py-2.5 px-2 text-center text-cyan-700">{row.c}</td>
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
              const col = r.severity === 'Critical' ? 'sky' : r.severity === 'High' ? 'teal' : 'emerald'
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

// ── Static Playbook Component ─────────────────────────────────────────────────
const DIM_COLORS = {
  '🔄 Process':      'bg-blue-50 border-blue-200 text-blue-800',
  '👥 People':       'bg-purple-50 border-purple-200 text-purple-800',
  '🛠 Tools':        'bg-cyan-50 border-cyan-200 text-cyan-800',
  '⚙ Infra':        'bg-gray-50 border-gray-200 text-gray-800',
}

function StaticPlaybook({ scenarioId }) {
  const [editedPb, setEditedPb] = useState(() => JSON.parse(JSON.stringify(STATIC_PLAYBOOKS[scenarioId] || null)))
  const [tab, setTab] = useState('roadmap')
  const [openPhase, setOpenPhase] = useState(0)
  const [dimFilter, setDimFilter] = useState('all')
  const [expandedStep, setExpandedStep] = useState(null)
  const [openTool, setOpenTool] = useState(null)
  const [editingItem, setEditingItem] = useState(null)
  const [editForm, setEditForm]       = useState({})

  useEffect(() => {
    setEditedPb(JSON.parse(JSON.stringify(STATIC_PLAYBOOKS[scenarioId] || null)))
  }, [scenarioId])

  const pb = editedPb

  if (!pb) return null

  const openEdit = (label, fields, saveFn) => {
    setEditingItem({ label, saveFn })
    setEditForm({ ...fields })
  }

  const saveItem = () => {
    editingItem.saveFn(editForm)
    setEditingItem(null)
  }

  const TABS = [
    { id: 'roadmap',   label: '🗓 Roadmap',            desc: 'Sprint-by-sprint plan' },
    { id: 'process',   label: '🔄 Process Changes',    desc: 'Before / After per phase' },
    { id: 'people',    label: '👥 People & Roles',      desc: 'Who changes, training, RACI' },
    { id: 'tools',     label: '🛠 Tools & Infra',       desc: 'Setup guides per tool' },
    { id: 'risks',     label: '⚠️ Governance & Risks',  desc: 'Risk register' },
  ]

  const phaseColors = { blue: 'bg-blue-600', purple: 'bg-purple-600', green: 'bg-green-600', amber: 'bg-cyan-600', red: 'bg-sky-600', emerald: 'bg-emerald-600' }
  const phaseBorders = { blue: 'border-blue-300 bg-blue-50', purple: 'border-purple-300 bg-purple-50', green: 'border-green-300 bg-green-50', amber: 'border-cyan-300 bg-cyan-50', red: 'border-sky-300 bg-sky-50', emerald: 'border-emerald-300 bg-emerald-50' }

  return (
    <div className="space-y-4">
      {/* Summary strip */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {[
          { label: 'Duration',        value: pb.duration },
          { label: 'Agents',          value: pb.agents },
          { label: 'Team Impact',     value: pb.teamImpact },
          { label: 'Target FE',       value: pb.targetFE },
          { label: 'Lead Time Target',value: pb.targetLeadTime },
        ].map(s => (
          <div key={s.label} className="bg-white border border-gray-200 rounded-xl p-3 text-center">
            <div className="font-bold text-gray-800 text-sm">{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="bg-indigo-50 border border-indigo-200 rounded-xl px-4 py-3 text-sm text-indigo-800">
        {pb.summary}
      </div>

      {/* Tab navigation */}
      <div className="flex gap-2 flex-wrap border-b border-gray-200 pb-2">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`px-4 py-2 rounded-t-lg text-sm font-semibold transition-colors ${
              tab === t.id ? 'bg-indigo-600 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* ── ROADMAP TAB ── */}
      {tab === 'roadmap' && (
        <div className="space-y-3">
          <div className="flex gap-2 flex-wrap">
            {['all', '🔄 Process', '👥 People', '🛠 Tools', '⚙ Infra'].map(d => (
              <button key={d} onClick={() => setDimFilter(d)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold border ${
                  dimFilter === d ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}>
                {d === 'all' ? 'All Dimensions' : d}
              </button>
            ))}
          </div>
          {pb.roadmap.map((phase, pi) => (
            <div key={pi} className={`border rounded-xl overflow-hidden ${phaseBorders[phase.color]}`}>
              <button onClick={() => setOpenPhase(openPhase === pi ? -1 : pi)}
                className="w-full flex items-center gap-4 px-5 py-4 text-left">
                <div className={`w-8 h-8 ${phaseColors[phase.color]} text-white rounded-lg flex items-center justify-center font-bold text-xs shrink-0`}>{pi + 1}</div>
                <div className="flex-1">
                  <div className="font-bold text-gray-800">{phase.phase}</div>
                  <div className="text-xs text-gray-600">{phase.weeks} · {phase.goal}</div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">{phase.steps.length} actions</span>
                  <button onClick={e => { e.stopPropagation(); openEdit('Phase: ' + phase.phase, { phase: phase.phase, weeks: phase.weeks, goal: phase.goal }, form => {
                    setEditedPb(prev => { const next = JSON.parse(JSON.stringify(prev)); Object.assign(next.roadmap[pi], form); return next })
                  })} } className="text-[10px] bg-white/60 hover:bg-white text-gray-600 border border-gray-300 px-2 py-0.5 rounded font-semibold">✏</button>
                  <span className="text-gray-400">{openPhase === pi ? '▲' : '▼'}</span>
                </div>
              </button>
              {openPhase === pi && (
                <div className="border-t border-gray-200 px-5 pb-5 pt-4 space-y-2">
                  {phase.steps
                    .map((step, originalSi) => ({ step, originalSi }))
                    .filter(({ step }) => dimFilter === 'all' || step.dim === dimFilter)
                    .map(({ step, originalSi }, si) => {
                    const stepKey = `${pi}-${originalSi}`
                    const isExpanded = expandedStep === stepKey
                    return (
                    <div key={si} className={`border rounded-lg ${DIM_COLORS[step.dim] || 'bg-gray-50 border-gray-200'}`}>
                      <div className="flex items-start gap-2 p-3">
                        <span className="text-xs font-bold px-2 py-0.5 rounded border border-current opacity-70 shrink-0 mt-0.5">{step.dim}</span>
                        <div className="flex-1">
                          <span className="text-xs font-bold mr-1">{step.who}:</span>
                          <span className="text-xs">{step.what}</span>
                        </div>
                        {(step.how || step.example) && (
                          <button
                            onClick={() => setExpandedStep(isExpanded ? null : stepKey)}
                            className="text-[10px] font-bold px-2 py-1 rounded bg-white/60 border border-current opacity-70 hover:opacity-100 shrink-0 whitespace-nowrap"
                          >
                            {isExpanded ? '▲ less' : '▼ how →'}
                          </button>
                        )}
                        <button onClick={() => openEdit('Step', { who: step.who, what: step.what, ...(step.how !== undefined && { how: step.how || '' }), ...(step.example !== undefined && { example: step.example || '' }) }, form => {
                          setEditedPb(prev => { const next = JSON.parse(JSON.stringify(prev)); Object.assign(next.roadmap[pi].steps[originalSi], form); return next })
                        })}
                          className="text-[10px] font-bold px-2 py-1 rounded bg-white/60 border border-current opacity-50 hover:opacity-100 shrink-0">✏</button>
                      </div>
                      {isExpanded && (
                        <div className="border-t border-current/20 px-3 pb-3 pt-2 space-y-2">
                          {step.how && (
                            <div>
                              <div className="text-[10px] font-bold uppercase tracking-wide opacity-60 mb-1.5">HOW TO EXECUTE</div>
                              <div className="space-y-1.5">
                                {step.how.split(/(?=\d+\.)/).filter(s => s.trim()).map((s, i) => (
                                  <div key={i} className="flex gap-2 text-xs">
                                    <span className="bg-current/20 rounded-full w-4 h-4 flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5">{i + 1}</span>
                                    <span>{s.replace(/^\d+\./, '').trim()}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                          {step.example && (
                            <pre className="bg-gray-900 text-green-300 font-mono text-[10px] p-3 rounded-lg overflow-x-auto whitespace-pre mt-1">{step.example}</pre>
                          )}
                        </div>
                      )}
                    </div>
                    )
                  })}
                  {phase.steps.filter(s => dimFilter === 'all' || s.dim === dimFilter).length === 0 && (
                    <div className="text-xs text-gray-400 text-center py-2">No {dimFilter} actions in this phase</div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* ── PROCESS CHANGES TAB ── */}
      {tab === 'process' && (
        <div className="space-y-4">
          {pb.processChanges.map((pc, i) => (
            <div key={i} className="card border border-gray-200">
              <div className="card-header bg-gray-50 border-b border-gray-200 flex items-center justify-between">
                <h4 className="font-bold text-gray-800">📍 {pc.phase}</h4>
                <button onClick={() => openEdit('Process Change: ' + pc.phase, { before: pc.before, after: pc.after, howTo: pc.howTo }, form => {
                  setEditedPb(prev => { const next = JSON.parse(JSON.stringify(prev)); Object.assign(next.processChanges[i], form); return next })
                })}
                  className="text-xs bg-indigo-100 text-indigo-700 hover:bg-indigo-200 px-2.5 py-1 rounded-lg font-semibold border border-indigo-200">
                  ✏ Edit
                </button>
              </div>
              <div className="card-body grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-sky-50 border border-sky-200 rounded-xl p-4">
                  <div className="text-xs font-bold text-sky-700 mb-2">BEFORE</div>
                  <p className="text-sm text-gray-700">{pc.before}</p>
                </div>
                <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                  <div className="text-xs font-bold text-green-700 mb-2">AFTER</div>
                  <p className="text-sm text-gray-700">{pc.after}</p>
                </div>
                <div className="md:col-span-2 bg-indigo-50 border border-indigo-200 rounded-xl p-4">
                  <div className="text-xs font-bold text-indigo-700 mb-2 uppercase tracking-wide">HOW TO TRANSITION</div>
                  <p className="text-sm text-gray-700 mb-3">{pc.howTo}</p>
                  {pc.transitionSteps?.length > 0 && (
                    <div className="space-y-2 border-t border-indigo-200 pt-3">
                      <div className="text-xs font-bold text-indigo-600 mb-2">Step-by-Step Transition Plan:</div>
                      {pc.transitionSteps.map((ts, tsi) => (
                        <div key={tsi} className="flex gap-3 bg-white border border-indigo-200 rounded-lg p-3">
                          <span className="bg-indigo-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0">{ts.step}</span>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1 flex-wrap">
                              <span className="text-xs font-bold text-purple-700">{ts.who}</span>
                              <span className="text-xs text-gray-400">·</span>
                              <span className="text-xs text-gray-500 italic">{ts.timing}</span>
                            </div>
                            <div className="text-sm text-gray-700">{ts.action}</div>
                            {ts.example && (
                              <pre className="bg-gray-900 text-green-300 font-mono text-[10px] p-2 rounded mt-1.5 overflow-x-auto whitespace-pre">{ts.example}</pre>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ── PEOPLE & ROLES TAB ── */}
      {tab === 'people' && (
        <div className="space-y-6">
          {/* Role changes */}
          <div className="card">
            <div className="card-header"><h3 className="font-bold text-gray-800">Role Impact — What Changes</h3></div>
            <div className="card-body space-y-3">
              {pb.people.roleChanges.map((r, i) => (
                <div key={i} className="border border-gray-200 rounded-xl p-4">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div className="font-bold text-gray-800 text-sm">{r.role}</div>
                    <span className="bg-purple-100 text-purple-700 text-xs font-bold px-2 py-0.5 rounded-full border border-purple-200 shrink-0">{r.timeImpact}</span>
                  </div>
                  <p className="text-xs text-gray-600 mb-2">{r.changes}</p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                    <div className="bg-cyan-50 border border-cyan-200 rounded-lg p-2">
                      <span className="font-semibold text-cyan-800">New skills: </span>{r.newSkills}
                    </div>
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-2">
                      <span className="font-semibold text-blue-800">Training: </span>{r.training}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* New roles */}
          {pb.people.newRoles?.length > 0 && (
            <div className="card">
              <div className="card-header"><h3 className="font-bold text-gray-800">New Roles Required</h3></div>
              <div className="card-body grid grid-cols-1 md:grid-cols-2 gap-4">
                {pb.people.newRoles.map((r, i) => (
                  <div key={i} className="bg-indigo-50 border border-indigo-200 rounded-xl p-4">
                    <div className="font-bold text-indigo-800 mb-1">{r.role}</div>
                    <div className="text-xs font-semibold text-indigo-600 mb-2">{r.fteRequired} · {r.source}</div>
                    <p className="text-xs text-gray-700 mb-2">{r.responsibilities}</p>
                    <div className="text-xs text-gray-500"><span className="font-semibold">Key skills: </span>{r.skills}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Training plan */}
          <div className="card">
            <div className="card-header"><h3 className="font-bold text-gray-800">Training Plan</h3></div>
            <div className="card-body overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b-2 border-gray-200">
                    <th className="text-left py-2 pr-3 font-semibold text-gray-700">Timing</th>
                    <th className="text-left py-2 pr-3 font-semibold text-gray-700">Who</th>
                    <th className="text-left py-2 pr-3 font-semibold text-gray-700">Topic</th>
                    <th className="text-left py-2 pr-3 font-semibold text-gray-700">Duration</th>
                    <th className="text-left py-2 font-semibold text-gray-700">Format</th>
                  </tr>
                </thead>
                <tbody>
                  {pb.people.training.map((t, i) => (
                    <tr key={i} className={`border-b border-gray-100 ${i%2===0?'bg-gray-50':''}`}>
                      <td className="py-2 pr-3 font-semibold text-indigo-700 whitespace-nowrap">{t.week}</td>
                      <td className="py-2 pr-3 text-gray-700">{t.who}</td>
                      <td className="py-2 pr-3 font-medium text-gray-800">{t.topic}</td>
                      <td className="py-2 pr-3 text-gray-600 whitespace-nowrap">{t.duration}</td>
                      <td className="py-2 text-gray-600">{t.format}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* RACI */}
          <div className="card">
            <div className="card-header"><h3 className="font-bold text-gray-800">RACI Matrix</h3></div>
            <div className="card-body overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b-2 border-gray-200">
                    <th className="text-left py-2 pr-4 font-semibold text-gray-700">Activity</th>
                    <th className="text-center py-2 px-2 font-semibold text-blue-700">Responsible</th>
                    <th className="text-center py-2 px-2 font-semibold text-purple-700">Accountable</th>
                    <th className="text-center py-2 px-2 font-semibold text-cyan-700">Consulted</th>
                    <th className="text-center py-2 font-semibold text-gray-500">Informed</th>
                  </tr>
                </thead>
                <tbody>
                  {pb.people.raci.map((row, i) => (
                    <tr key={i} className={`border-b border-gray-100 ${i%2===0?'bg-gray-50':''}`}>
                      <td className="py-2 pr-4 font-medium text-gray-800">{row.activity}</td>
                      <td className="py-2 px-2 text-center text-blue-700 font-semibold">{row.r}</td>
                      <td className="py-2 px-2 text-center text-purple-700 font-semibold">{row.a}</td>
                      <td className="py-2 px-2 text-center text-cyan-700">{row.c}</td>
                      <td className="py-2 text-center text-gray-500">{row.i}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ── TOOLS & INFRA TAB ── */}
      {tab === 'tools' && (
        <div className="space-y-4">
          {pb.tools.map((tool, i) => (
            <div key={i} className="card border border-gray-200 overflow-hidden">
              {/* Tool header — always visible */}
              <button
                onClick={() => setOpenTool(openTool === i ? null : i)}
                className="w-full card-header flex items-start gap-3 text-left hover:bg-gray-50"
              >
                <span className="text-2xl shrink-0">{tool.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="font-bold text-gray-800">{tool.name}</div>
                  <div className="text-xs text-gray-500 mt-0.5">{tool.purpose}</div>
                </div>
                <div className="flex gap-2 flex-wrap items-center shrink-0">
                  <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded border border-green-200">{tool.setupTime} setup</span>
                  <span className="bg-blue-100 text-blue-700 text-xs font-bold px-2 py-0.5 rounded border border-blue-200">{tool.costRange}</span>
                  <button onClick={e => { e.stopPropagation(); openEdit('Tool: ' + tool.name, {
                    purpose: tool.purpose || '',
                    procurement: tool.procurement || '',
                    integration: tool.integration || '',
                    ...(tool.configExample !== undefined && { configExample: tool.configExample || '' }),
                    ...(tool.verifySetup !== undefined && { verifySetup: tool.verifySetup || '' }),
                    ...(tool.validationTest !== undefined && { validationTest: tool.validationTest || '' }),
                  }, form => {
                    setEditedPb(prev => { const next = JSON.parse(JSON.stringify(prev)); Object.assign(next.tools[i], form); return next })
                  })}}
                    className="text-xs bg-indigo-100 text-indigo-700 hover:bg-indigo-200 px-2 py-0.5 rounded border border-indigo-200 font-semibold">✏ Edit</button>
                  <span className="text-gray-400 text-sm">{openTool === i ? '▲' : '▼'}</span>
                </div>
              </button>

              {openTool === i && (
                <div className="card-body space-y-5">
                  {/* Procurement + Integration */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <div className="text-xs font-bold text-cyan-700 mb-2 uppercase tracking-wide">Procurement</div>
                      <p className="text-xs text-gray-700">{tool.procurement}</p>
                    </div>
                    <div>
                      <div className="text-xs font-bold text-blue-700 mb-2 uppercase tracking-wide">Integration Points</div>
                      <p className="text-xs text-gray-700">{tool.integration}</p>
                    </div>
                  </div>

                  {/* Setup Steps */}
                  <div>
                    <div className="text-xs font-bold text-green-700 mb-2 uppercase tracking-wide">Setup Steps</div>
                    <div className="space-y-1.5">
                      {tool.setup.map((step, si) => (
                        <div key={si} className="flex items-start gap-2 bg-green-50 border border-green-100 rounded-lg p-2.5">
                          <span className="bg-green-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5">{si+1}</span>
                          <span className="text-xs text-gray-700">{step}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Configuration Example */}
                  {tool.configExample && (
                    <div>
                      <div className="text-xs font-bold text-purple-700 mb-2 uppercase tracking-wide">Configuration Example</div>
                      <pre className="bg-gray-900 text-green-300 font-mono text-[11px] p-4 rounded-xl border border-gray-700 overflow-x-auto whitespace-pre leading-relaxed">{tool.configExample}</pre>
                    </div>
                  )}

                  {/* Verify + Test */}
                  {(tool.verifySetup || tool.validationTest) && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {tool.verifySetup && (
                        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                          <div className="text-xs font-bold text-blue-700 mb-2 uppercase tracking-wide flex items-center gap-1.5">
                            <span>✓</span> How to Verify Setup
                          </div>
                          <p className="text-xs text-blue-900 leading-relaxed">{tool.verifySetup}</p>
                        </div>
                      )}
                      {tool.validationTest && (
                        <div className="bg-purple-50 border border-purple-200 rounded-xl p-4">
                          <div className="text-xs font-bold text-purple-700 mb-2 uppercase tracking-wide flex items-center gap-1.5">
                            <span>🧪</span> End-to-End Validation Test
                          </div>
                          <p className="text-xs text-purple-900 leading-relaxed">{tool.validationTest}</p>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Common Pitfalls */}
                  {tool.pitfalls?.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-sky-700 mb-2 uppercase tracking-wide flex items-center gap-1.5">
                        <span>⚠</span> Common Pitfalls — Read Before Setup
                      </div>
                      <div className="space-y-2">
                        {tool.pitfalls.map((pitfall, pi) => (
                          <div key={pi} className="flex items-start gap-2.5 bg-sky-50 border border-sky-200 rounded-lg p-3">
                            <span className="bg-sky-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5">{pi+1}</span>
                            <span className="text-xs text-sky-900 leading-relaxed">{pitfall}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* ── EDIT MODAL ── */}
      {editingItem && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4" onClick={() => setEditingItem(null)}>
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[92vh] overflow-y-auto flex flex-col" onClick={e => e.stopPropagation()}>
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl z-10">
              <div>
                <div className="font-bold text-gray-800 text-base">✏ Edit: {editingItem.label}</div>
                <div className="text-xs text-gray-500 mt-0.5">Changes are local to this session.</div>
              </div>
              <div className="flex gap-2">
                <button onClick={saveItem} className="bg-green-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-green-700 shadow-sm">✓ Save</button>
                <button onClick={() => setEditingItem(null)} className="bg-gray-100 text-gray-600 px-4 py-2 rounded-xl text-sm hover:bg-gray-200">✕</button>
              </div>
            </div>
            <div className="p-6 space-y-5 flex-1">
              {Object.entries(editForm).map(([key, val]) => {
                const isCode = ['configExample', 'example'].includes(key)
                const isLarge = ['how', 'howTo', 'verifySetup', 'validationTest'].includes(key)
                const LABELS = {
                  who: 'Who', what: 'What', how: 'How (numbered: "1. step. 2. step.")',
                  before: 'Before (Current State)', after: 'After (Target State)',
                  howTo: 'How to Transition', action: 'Action', timing: 'Timing',
                  configExample: 'Config Example', example: 'Example / Code',
                  verifySetup: 'How to Verify Setup', validationTest: 'End-to-End Validation Test',
                  risk: 'Risk Description', mitigation: 'Mitigation Steps',
                  purpose: 'Purpose / Description', procurement: 'Procurement', integration: 'Integration Points',
                  phase: 'Phase Name', weeks: 'Weeks / Timing', goal: 'Phase Goal',
                }
                return (
                  <div key={key}>
                    <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">{LABELS[key] || key}</label>
                    <textarea
                      className={`w-full border rounded-xl px-3 py-2 resize-y focus:outline-none focus:ring-2 ${
                        isCode
                          ? 'font-mono text-[11px] bg-gray-900 text-green-300 border-gray-700 focus:ring-green-500'
                          : 'text-sm border-gray-300 focus:ring-blue-400'
                      }`}
                      rows={isCode ? 10 : isLarge ? 6 : 3}
                      value={val || ''}
                      onChange={e => setEditForm(f => ({ ...f, [key]: e.target.value }))}
                    />
                  </div>
                )
              })}
            </div>
            <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-3 flex justify-end gap-2 rounded-b-2xl">
              <button onClick={() => setEditingItem(null)} className="bg-gray-200 text-gray-600 px-5 py-2 rounded-xl text-sm hover:bg-gray-300">Cancel</button>
              <button onClick={saveItem} className="bg-green-600 text-white px-6 py-2 rounded-xl text-sm font-semibold hover:bg-green-700 shadow-sm">✓ Save Changes</button>
            </div>
          </div>
        </div>
      )}

      {/* ── GOVERNANCE & RISKS TAB ── */}
      {tab === 'risks' && (
        <div className="space-y-3">
          <div className="grid grid-cols-3 gap-3 mb-4">
            {['Critical', 'High', 'Medium'].map(sev => {
              const count = pb.risks.filter(r => r.probability === sev || r.impact === sev).length
              const colors = { Critical: 'bg-sky-100 text-sky-800 border-sky-300', High: 'bg-teal-100 text-teal-800 border-teal-300', Medium: 'bg-cyan-100 text-cyan-800 border-cyan-300' }
              return (
                <div key={sev} className={`border rounded-xl p-3 text-center ${colors[sev]}`}>
                  <div className="text-2xl font-bold">{pb.risks.filter(r => r.impact === sev).length}</div>
                  <div className="text-xs font-semibold">{sev} Impact Risks</div>
                </div>
              )
            })}
          </div>
          {pb.risks.map((r, i) => {
            const impactColors = { Critical: 'border-sky-400 bg-sky-50', High: 'border-teal-400 bg-teal-50', Medium: 'border-cyan-400 bg-cyan-50', Low: 'border-blue-300 bg-blue-50' }
            const badgeColors = { Critical: 'bg-sky-600', High: 'bg-teal-600', Medium: 'bg-cyan-500', Low: 'bg-blue-500' }
            return (
              <div key={i} className={`border-l-4 rounded-xl p-4 ${impactColors[r.impact] || 'border-gray-300 bg-gray-50'}`}>
                <div className="flex items-start gap-3">
                  <div className="flex flex-col gap-1 shrink-0">
                    <span className={`${badgeColors[r.impact] || 'bg-gray-500'} text-white text-xs font-bold px-2 py-0.5 rounded-full`}>{r.impact} impact</span>
                    <span className="bg-gray-600 text-white text-xs font-bold px-2 py-0.5 rounded-full">{r.probability} prob</span>
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800 text-sm mb-1">{r.risk}</div>
                    <div className="text-xs text-gray-700"><span className="font-semibold text-gray-600">Mitigation: </span>{r.mitigation}</div>
                  </div>
                  <button onClick={() => openEdit('Risk', { risk: r.risk, mitigation: r.mitigation }, form => {
                    setEditedPb(prev => { const next = JSON.parse(JSON.stringify(prev)); Object.assign(next.risks[i], form); return next })
                  })}
                    className="text-xs bg-white/70 hover:bg-white text-gray-500 hover:text-gray-800 border border-gray-300 px-2 py-0.5 rounded font-semibold shrink-0">✏</button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function PlaybookContextPage() {
  const { project, analysisResult, activeScenario, setActiveScenario } = useApp()
  const navigate = useNavigate()
  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const ts = useTargetScenario(project?.id, setActiveScenario)

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
  const [view, setView]               = useState('guide')  // 'guide' | 'customise'

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
      {ts.configured && <TargetStepBar steps={ts.steps} stepIdx={ts.stepIdx} pickStep={ts.pickStep} platform={ts.platform} />}
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-violet-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Implementation Playbook</h2>
            <p className="text-indigo-100">
              Detailed implementation guide for{' '}
              <strong>{scenario?.label} — {scenario?.title}</strong>
            </p>
            <p className="text-indigo-200 text-xs mt-1">Covers Process · People · Tools · Infrastructure — use as your team's implementation user guide</p>
          </div>
          <Link to="/business-case" className="bg-white/20 hover:bg-white/30 text-white text-sm font-semibold px-4 py-2 rounded-lg">
            ← Business Case
          </Link>
        </div>
      </div>

      {/* View toggle */}
      <div className="flex gap-3 bg-white border border-gray-200 rounded-xl p-2">
        <button onClick={() => setView('guide')}
          className={`flex-1 py-2.5 rounded-lg text-sm font-semibold transition-colors ${view === 'guide' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 hover:bg-gray-50'}`}>
          📖 Standard Implementation Guide
        </button>
        <button onClick={() => setView('customise')}
          className={`flex-1 py-2.5 rounded-lg text-sm font-semibold transition-colors ${view === 'customise' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600 hover:bg-gray-50'}`}>
          ✏️ Customise & Refine ({currentAccuracy}% accuracy)
        </button>
      </div>

      {/* Static guide */}
      {view === 'guide' && (
        <div className="space-y-4">
          <div className="flex items-center gap-3 bg-indigo-50 border border-indigo-200 rounded-xl px-4 py-3">
            <span className="text-indigo-600 text-lg">📖</span>
            <div className="text-sm text-indigo-800">
              <strong>Standard Playbook</strong> — Detailed implementation guide covering all dimensions.
              Switch to <strong>Customise & Refine</strong> to tailor this to your specific team context and generate a personalised version.
            </div>
          </div>
          <StaticPlaybook scenarioId={activeScenario} />
        </div>
      )}

      {/* Customise view */}
      {view === 'customise' && (<>

      {/* Live accuracy gauge */}
      <div className="card card-body">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="font-bold text-gray-800 text-lg">{currentAccuracy}% Accuracy</span>
            <span className="text-sm text-gray-500 ml-2">— estimated contextualisation level</span>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold ${
            currentAccuracy >= 85 ? 'bg-green-100 text-green-800' :
            currentAccuracy >= 70 ? 'bg-cyan-100 text-cyan-800' : 'bg-gray-100 text-gray-600'
          }`}>
            {currentAccuracy >= 85 ? 'High confidence — ready to generate' :
             currentAccuracy >= 70 ? 'Good — add more for better accuracy' : 'Fill in more context to improve'}
          </span>
        </div>
        <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              currentAccuracy >= 85 ? 'bg-green-500' : currentAccuracy >= 70 ? 'bg-cyan-500' : 'bg-indigo-500'
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
                  <div className="text-xs text-cyan-700 bg-cyan-50 border border-cyan-200 rounded-lg px-3 py-2 mb-3">
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
      {error && <div className="bg-sky-50 border border-sky-200 rounded-xl p-4 text-sm text-sky-700">{error}</div>}
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

      {/* Unified 13-Agent Deployment Sequence */}
      <div className="card border-l-4 border-indigo-500">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Integrated 13-Agent Deployment Sequence</h3>
          <p className="text-xs text-gray-500">One phased rollout — delivery agents first, then governance layer, then full autonomous orchestration</p>
        </div>
        <div className="card-body space-y-2">
          {[
            { weeks: 'Week 1–2',  label: 'Foundation Layer', agents: ['ALM Connector', 'VSM Analyzer'], color: 'blue',
              desc: 'Connect ALM tool (Jira/ADO), pull ticket history, generate first current-state VSM with PT/WT/LT/FE metrics.' },
            { weeks: 'Week 3–4',  label: 'Analysis Layer',   agents: ['Bottleneck Analyzer', 'Benchmark Agent'], color: 'purple',
              desc: 'Run Bottleneck Analyzer against VSM data; compare metrics to 12 sector peers via Benchmark Agent.' },
            { weeks: 'Week 5–6',  label: 'Improvement Layer', agents: ['Improvement Generator', 'Future State Designer'], color: 'green',
              desc: 'Generate AI-powered improvement catalogue; model 3 transformation scenarios (A/B/C) with predicted metrics.' },
            { weeks: 'Week 7–8',  label: 'Business Case Complete', agents: ['Business Case Builder', 'Orchestrator'], color: 'emerald',
              desc: 'Build ROI/payback/NPV models per scenario. Orchestrator coordinates full end-to-end pipeline run. Phase 1 of transformation complete.' },
            { weeks: 'Week 9–10', label: 'Compliance Layer',  agents: ['Secure-by-Design Architect', 'CaC Orchestrator'], color: 'sky',
              desc: 'Activate Secure-by-Design (IaC validation at Phase 2 + Phase 6) and CaC Orchestrator (GDPR/DORA/Basel III at Phase 3 + Phase 5). Run in advisory mode first sprint.' },
            { weeks: 'Week 11–12',label: 'Risk & Observability Layer', agents: ['MRM Agent', 'Telemetry Sentinel'], color: 'purple',
              desc: 'Activate MRM Agent (Explainability Reports, drift monitoring) and Telemetry Sentinel (Business Risk Scores from all agent telemetry).' },
            { weeks: 'Week 13–14',label: 'Unified Orchestration', agents: ['Multi-Agent Governance Controller'], color: 'indigo',
              desc: 'Deploy Governance Controller in shadow mode (Week 13), then enforcement mode (Week 14). All 13 agents now operate as one unified, governance-assured system.' },
            { weeks: 'Week 15+',  label: 'Full 13-Agent Autonomous Pipeline', agents: ['All 13 agents running'], color: 'emerald',
              desc: activeScenario === 'option-c'
                ? 'Option C: Fully autonomous ADLC. Governance Controller is the safety net — no agent can bypass a protocol. Only Product Definer and Product Builder roles remain.'
                : 'Option B: All 13 agents active with human approval gates at governance checkpoints. Continuous improvement cycle running.' },
          ].map((step, i) => {
            const colorMap = {
              blue: { bg: 'bg-blue-50', border: 'border-blue-200', badge: 'bg-blue-600', text: 'text-blue-800', agentBg: 'bg-blue-100 text-blue-700 border-blue-200' },
              purple: { bg: 'bg-purple-50', border: 'border-purple-200', badge: 'bg-purple-600', text: 'text-purple-800', agentBg: 'bg-purple-100 text-purple-700 border-purple-200' },
              green: { bg: 'bg-green-50', border: 'border-green-200', badge: 'bg-green-600', text: 'text-green-800', agentBg: 'bg-green-100 text-green-700 border-green-200' },
              amber: { bg: 'bg-cyan-50', border: 'border-cyan-200', badge: 'bg-cyan-600', text: 'text-cyan-800', agentBg: 'bg-cyan-100 text-cyan-700 border-cyan-200' },
              red: { bg: 'bg-sky-50', border: 'border-sky-200', badge: 'bg-sky-600', text: 'text-sky-800', agentBg: 'bg-sky-100 text-sky-700 border-sky-200' },
              indigo: { bg: 'bg-indigo-50', border: 'border-indigo-200', badge: 'bg-indigo-600', text: 'text-indigo-800', agentBg: 'bg-indigo-100 text-indigo-700 border-indigo-200' },
              emerald: { bg: 'bg-emerald-50', border: 'border-emerald-200', badge: 'bg-emerald-600', text: 'text-emerald-800', agentBg: 'bg-emerald-100 text-emerald-700 border-emerald-200' },
            }
            const c = colorMap[step.color]
            return (
              <div key={i} className={`rounded-xl border p-4 ${c.bg} ${c.border}`}>
                <div className="flex items-start gap-3">
                  <div className={`w-8 h-8 ${c.badge} text-white rounded-lg flex items-center justify-center font-bold text-xs shrink-0 mt-0.5`}>{i+1}</div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs font-bold ${c.text}`}>{step.weeks}</span>
                      <span className="font-bold text-gray-800 text-sm">{step.label}</span>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">{step.desc}</p>
                    <div className="flex flex-wrap gap-1">
                      {step.agents.map(a => (
                        <span key={a} className={`text-xs border px-2 py-0.5 rounded-full font-semibold ${c.agentBg}`}>{a}</span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Option B/C — Compliance & Governance Agent Configuration Checklist */}
      {(activeScenario === 'option-b' || activeScenario === 'option-c') && (
        <div className="card border-l-4 border-sky-400">
          <div className="card-header flex items-center justify-between">
            <div>
              <h3 className="font-bold text-gray-800">Governance Agent Pre-Deployment Checklist</h3>
              <p className="text-xs text-gray-500">Required configuration activities for the 5 governance agents before Week 9 activation in {scenario?.label}</p>
            </div>
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-indigo-100 text-indigo-700">Weeks 9–14</span>
          </div>
          <div className="card-body space-y-4">
            {[
              {
                agent: 'Secure-by-Design Architect', icon: '🔐', color: 'sky',
                phase: 'Phase 2 (Architecture & UX) + Phase 6 (Continuous Delivery)',
                activities: [
                  { who: 'CISO + Cloud Architect', what: 'Define and version-control cloud architecture standards (AWS Well-Architected / CIS Benchmarks) as policy-as-code rules' },
                  { who: 'DevOps Engineer', what: 'Integrate Secure-by-Design Architect into CI/CD pipeline — configure IaC validation step blocking non-compliant deployments' },
                  { who: 'CISO', what: 'Document CISO override approval workflow; test and sign off the escalation path for legitimate overrides' },
                  { who: 'Cloud Architect', what: 'Run baseline scan of all existing IaC — remediate violations before go-live to avoid false-positive alert storm' },
                ]
              },
              {
                agent: 'Compliance-as-Code Orchestrator', icon: '📋', color: 'blue',
                phase: 'Phase 3 (Code Management) + Phase 5 (Continuous Testing)',
                activities: [
                  { who: 'Chief Compliance Officer', what: 'Sign off on GDPR Article 25, DORA, and Basel III rule encoding — confirm coverage and exceptions are documented' },
                  { who: 'Tech Lead', what: 'Integrate CaC Orchestrator into git hooks and PR pipelines; configure advisory mode for first sprint before switching to blocking' },
                  { who: 'Compliance Officer', what: 'Define 7-year audit trail retention policy; confirm storage tier, encryption, and access controls for regulatory log archive' },
                  { who: 'QA Lead', what: 'Run CaC rules against 3 months of existing commits in staging to measure false-positive rate; tune thresholds before production rollout' },
                ]
              },
              {
                agent: 'Model Risk Management (MRM) Agent', icon: '🧬', color: 'purple',
                phase: 'Phase 5 (Continuous Testing) + Phase 7 (Monitoring & Feedback)',
                activities: [
                  { who: 'Model Risk Officer (MRO)', what: 'Define explainability score thresholds per model type (regression, classification, LLM) aligned with SR 11-7 model risk guidance' },
                  { who: 'MRO + CTO', what: 'Document and test kill-switch dual-authorisation workflow — confirm both can trigger within SLA; run a tabletop exercise' },
                  { who: 'Data Science Lead', what: 'Establish bias detection baseline: select protected attributes, run initial bias audit on all models entering production' },
                  { who: 'MRO', what: 'Configure drift monitoring thresholds per model; set alerting cadence and link to model versioning pipeline so every deploy auto-generates an Explainability Report' },
                  ...(activeScenario === 'option-c' ? [{ who: 'Product Builder', what: 'At full autonomy (Option C): MRM Agent is a critical control point — validate kill-switch integration with Governance Controller before removing human model review checkpoints' }] : []),
                ]
              },
              {
                agent: 'Telemetry & Observability Sentinel', icon: '📡', color: 'cyan',
                phase: 'Phase 7 (Monitoring & Feedback) + Cross-phase',
                activities: [
                  { who: 'VP Engineering + Governance Board', what: 'Define Business Risk Score rubric: agree on which technical signals map to which risk levels (Low / Medium / High / Critical)' },
                  { who: 'DevOps Engineer', what: 'Connect Telemetry Sentinel to all agent workflow logs; configure aggregation pipeline and Business Risk Score calculation engine' },
                  { who: 'Governance Team', what: 'Set up governance dashboard feed: configure alert thresholds for mandatory review triggers; test escalation notifications' },
                  { who: 'Platform Engineering Lead', what: 'Validate data residency for telemetry logs — confirm no agent workflow data leaves approved cloud regions' },
                ]
              },
              {
                agent: 'Multi-Agent Governance Controller', icon: '🏛️', color: 'indigo',
                phase: 'All phases — orchestration layer',
                activities: [
                  { who: 'CTO + CCO', what: 'Approve Governance Controller configuration: review and sign off on all agent permissions, protocol definitions, and bypass detection rules' },
                  { who: 'Platform Engineering Lead', what: 'Deploy Governance Controller in shadow mode for 2 weeks: log all would-be interventions without blocking, review output before activating enforcement' },
                  { who: 'Platform Engineering Lead', what: 'Test bypass detection: attempt to run a dev agent without Governance Controller approval; confirm it is blocked and logged' },
                  { who: 'CTO + CCO', what: 'Define change management process for Governance Controller config updates — require dual approval for any protocol or permission change' },
                  ...(activeScenario === 'option-c' ? [{ who: 'Product Builder', what: 'Option C critical: Governance Controller is the only mechanism preventing a fully autonomous agent from bypassing compliance protocols — treat it as a tier-1 production service with 99.9% availability SLA' }] : []),
                ]
              },
            ].map(item => (
              <div key={item.agent} className={`border border-${item.color}-200 rounded-xl overflow-hidden`}>
                <div className={`bg-${item.color}-50 px-4 py-3 flex items-center gap-3`}>
                  <span className="text-xl">{item.icon}</span>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800 text-sm">{item.agent}</div>
                    <div className="text-xs text-gray-500">{item.phase}</div>
                  </div>
                </div>
                <div className="p-4 space-y-2">
                  {item.activities.map((a, ai) => (
                    <div key={ai} className={`flex items-start gap-3 p-3 rounded-lg bg-${item.color}-50 border border-${item.color}-100`}>
                      <span className={`bg-${item.color}-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5`}>{ai + 1}</span>
                      <div>
                        <div className={`text-xs font-bold text-${item.color}-900 mb-0.5`}>{a.who}</div>
                        <div className="text-sm text-gray-700">{a.what}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

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

      </>) /* end customise view */}

    </div>
  )
}
