import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

const BUSINESS_CASES = {
  'option-a': {
    investmentRange: '$800K – $1.5M',
    roiTimeline: '12–18 months',
    roiMultiple: '2.8×',
    paybackPeriod: '14 months',
    investment: {
      tools: '$250K–$400K (AI tools, IDE plugins, platform licenses)',
      infrastructure: '$100K–$200K (GPU compute, vector DBs, API costs)',
      implementation: '$300K–$600K (integration, prompt engineering, testing)',
      training: '$100K–$200K (upskilling all PDLC personas)',
      change: '$100K–$150K (org change management, communications)'
    },
    annualBenefits: {
      ttmImprovement: '$600K–$900K (faster feature delivery, competitive advantage)',
      productivityGains: '$400K–$600K (35% effort reduction across team)',
      qualityImprovement: '$200K–$300K (fewer defects, less rework)',
      operationalSavings: '$100K–$150K (automated testing, deployments)'
    },
    orgChanges: [
      'Upskill all PDLC personas in AI tool collaboration',
      'Redefine roles to include AI supervision and prompt engineering',
      'Establish AI Centre of Excellence (CoE) for governance',
      'Update ways of working guides for human-AI collaboration',
      'Introduce AI literacy training (mandatory for all roles)'
    ],
    toolsChanges: [
      'Jira / ADO: Add AI-powered backlog management plugins',
      'GitHub: Deploy Copilot Enterprise for all developers',
      'Testing: Upgrade to AI-enhanced test frameworks',
      'CI/CD: Integrate ML-based build optimizers and SAST tools',
      'Monitoring: Deploy AI APM (Dynatrace Davis AI or Datadog AI)'
    ],
    devSecOps: [
      'Shift-left security with AI-assisted SAST/DAST in every PR',
      'AI-generated IaC templates with security policy validation',
      'Automated compliance evidence collection for audit trails',
      'AI-powered secret scanning and dependency vulnerability alerts'
    ],
    aiOps: [
      'AI-driven anomaly detection and auto-remediation',
      'Predictive scaling based on ML traffic patterns',
      'Automated incident routing with NLP-based categorization',
      'Continuous feedback loop: production insights → backlog prioritization'
    ],
    productCentricChanges: [
      'Reorganize from project to persistent product teams',
      'OKRs tied to product outcomes, not delivery velocity',
      'Quarterly business review cadence with AI-generated insights',
      'Customer feedback integrated into product roadmap via AI'
    ]
  },
  'option-b': {
    investmentRange: '$1.2M – $2.2M',
    roiTimeline: '10–15 months',
    roiMultiple: '3.8×',
    paybackPeriod: '11 months',
    investment: {
      tools: '$400K–$700K (selective AI platforms for key phases)',
      infrastructure: '$200K–$350K (dedicated AI compute, model hosting)',
      implementation: '$400K–$800K (deep integrations, custom agent development)',
      training: '$100K–$200K (focused training for remaining human roles)',
      change: '$150K–$200K (significant role restructuring support)'
    },
    annualBenefits: {
      ttmImprovement: '$900K–$1.4M (55% faster delivery)',
      productivityGains: '$600K–$900K (55% effort reduction)',
      qualityImprovement: '$300K–$500K (AI-driven quality gates)',
      operationalSavings: '$200K–$350K (automated ops and monitoring)'
    },
    orgChanges: [
      'Consolidate 8+ roles to 5 core roles (Product Owner, Tech Lead, Developer, QA Lead, DevOps)',
      'Establish clear human-AI handoff protocols per phase',
      'Create AI Agent Operations team to manage and tune agents',
      'Redesign performance metrics to measure AI-human team output',
      'Executive sponsorship program for transformation governance'
    ],
    toolsChanges: [
      'Consolidate ALM tools to 1–2 AI-native platforms',
      'Deploy custom LangChain/LangGraph agent orchestration layer',
      'Replace manual test scripting with AI-generated test suites',
      'Implement GitOps-native CI/CD with AI release gating',
      'Unify observability into AI-powered single-pane-of-glass'
    ],
    devSecOps: [
      'Zero-trust security model enforced by AI policy agents',
      'AI-generated runbooks updated automatically after incidents',
      'Continuous compliance validation with AI audit agents',
      'ML-based threat modeling integrated into architecture reviews'
    ],
    aiOps: [
      'Self-healing pipelines with AI-driven failure prediction',
      'AIOps platform managing all production alerts and responses',
      'Automated capacity planning using ML forecasting',
      'AI-powered post-incident learning and backlog integration'
    ],
    productCentricChanges: [
      'Product teams own full value stream from ideation to production',
      'Eliminate hand-offs between dev, test, and ops teams',
      'Continuous product discovery embedded in product team rituals',
      'AI-generated product performance dashboards for stakeholders'
    ]
  },
  'option-c': {
    investmentRange: '$2.5M – $4.5M',
    roiTimeline: '18–24 months',
    roiMultiple: '5.5×',
    paybackPeriod: '19 months',
    investment: {
      tools: '$800K–$1.5M (comprehensive AI platform stack)',
      infrastructure: '$500K–$900K (enterprise AI compute, model fine-tuning)',
      implementation: '$800K–$1.5M (end-to-end agent development and orchestration)',
      training: '$200K–$300K (Product Definer + Product Builder intensive training)',
      change: '$300K–$500K (major org transformation support)'
    },
    annualBenefits: {
      ttmImprovement: '$1.8M–$2.8M (70% faster delivery, market leadership)',
      productivityGains: '$1.2M–$1.8M (70% effort reduction)',
      qualityImprovement: '$500K–$800K (AI quality gates, zero manual rework)',
      operationalSavings: '$400K–$700K (fully autonomous ops)'
    },
    orgChanges: [
      'Restructure entire PDLC workforce to 2 human roles only',
      'Product Definer: sets vision, outcomes, and acceptance criteria',
      'Product Builder: supervises agent orchestration and quality gates',
      'Major workforce transition plan with reskilling/redeployment',
      'New operating model approval at board level required',
      'External change management firm engagement recommended'
    ],
    toolsChanges: [
      'Custom AI-native product engineering platform (greenfield or heavily modified existing)',
      'Multi-agent orchestration layer (LangGraph / AutoGen / custom)',
      'AI-native ALM replacing traditional Jira/ADO',
      'Fully automated CI/CD/CD with AI-driven decisions at every gate',
      'Integrated AI product analytics replacing manual reporting'
    ],
    devSecOps: [
      'Fully AI-managed DevSecOps pipeline from code to production',
      'AI security agents continuously monitoring and auto-remediating',
      'Autonomous compliance management with human oversight only for exceptions',
      'AI-generated architecture decision records (ADRs) and security reviews'
    ],
    aiOps: [
      'Fully autonomous AIOps — zero Level 1 / Level 2 human intervention',
      'AI-driven capacity, performance, and cost optimization continuously',
      'Self-healing, self-scaling, self-documenting production systems',
      'AI incident commander with human escalation only for critical events'
    ],
    productCentricChanges: [
      'Abolish traditional SDLC phases — continuous product evolution model',
      'Product Definer sets weekly outcomes; agents execute autonomously',
      'Real-time product performance feeding back to AI roadmap prioritization',
      'Customer intent detection via AI — feature ideas generated proactively'
    ]
  }
}

const SECTION_ICONS = {
  investment: '💰', benefits: '📈', orgChanges: '👥', toolsChanges: '🛠️',
  devSecOps: '🔒', aiOps: '🤖', productCentric: '🎯'
}

export default function BusinessCasePage() {
  const { activeScenario, setActiveScenario, addNotification, project } = useApp()
  const [running, setRunning]   = useState(false)
  const [activeSection, setSection] = useState('overview')

  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const bc = BUSINESS_CASES[activeScenario]

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runBusinessCaseBuilder(project.id || 'demo', activeScenario)
      addNotification('Business case generated!', 'success')
    } catch {
      addNotification('Using built-in business case (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  const SECTIONS = [
    { id: 'overview',  label: 'Overview' },
    { id: 'investment',label: 'Investment' },
    { id: 'benefits',  label: 'Benefits' },
    { id: 'org',       label: 'Org Change' },
    { id: 'tools',     label: 'Tools' },
    { id: 'devsecops', label: 'DevSecOps' },
    { id: 'aiops',     label: 'AI Ops' },
    { id: 'product',   label: 'Product-Centric' }
  ]

  return (
    <div className="space-y-6 fade-in">
      <div className="bg-gradient-to-r from-amber-600 to-orange-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Business Case</h2>
            <p className="text-amber-100">Investment, ROI, org change, tools, DevSecOps, and AIOps requirements for each future state scenario</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-amber-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-amber-50 shadow">
            {running ? '⏳ Building...' : '🤖 Run Business Case Agent'}
          </button>
        </div>
      </div>

      {/* Scenario selector */}
      <div className="grid grid-cols-3 gap-4">
        {FUTURE_STATE_SCENARIOS.map(s => {
          const sbc = BUSINESS_CASES[s.id]
          return (
            <button key={s.id} onClick={() => setActiveScenario(s.id)}
              className={`p-4 rounded-xl text-left border-2 transition-all ${activeScenario === s.id ? 'border-amber-500 bg-amber-50 shadow-md' : 'border-gray-200 bg-white hover:border-gray-400'}`}>
              <div className="font-bold text-gray-800 mb-1">{s.label}: {s.title.split('—')[0].trim()}</div>
              <div className="text-xs text-gray-500 mb-2">{s.subtitle}</div>
              <div className="text-xs space-y-1">
                <div><span className="text-gray-500">Investment: </span><span className="font-bold text-amber-700">{sbc.investmentRange}</span></div>
                <div><span className="text-gray-500">ROI: </span><span className="font-bold text-green-700">{sbc.roiMultiple} in {sbc.roiTimeline}</span></div>
                <div><span className="text-gray-500">Payback: </span><span className="font-bold text-blue-700">{sbc.paybackPeriod}</span></div>
              </div>
            </button>
          )
        })}
      </div>

      {/* Section nav */}
      <div className="flex gap-2 overflow-x-auto bg-white p-3 rounded-xl border border-gray-200">
        {SECTIONS.map(s => (
          <button key={s.id} onClick={() => setSection(s.id)}
            className={`px-4 py-1.5 rounded-lg text-sm font-semibold whitespace-nowrap ${activeSection === s.id ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {s.label}
          </button>
        ))}
      </div>

      {/* Overview */}
      {activeSection === 'overview' && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Investment',    value: bc.investmentRange, color: 'amber', icon: '💰' },
            { label: 'ROI Multiple',  value: bc.roiMultiple,     color: 'green', icon: '📈' },
            { label: 'ROI Timeline',  value: bc.roiTimeline,     color: 'blue',  icon: '📅' },
            { label: 'Payback Period',value: bc.paybackPeriod,   color: 'purple',icon: '⏳' }
          ].map(m => (
            <div key={m.label} className="card card-body text-center">
              <div className="text-2xl mb-1">{m.icon}</div>
              <div className={`text-lg font-bold text-${m.color}-700`}>{m.value}</div>
              <div className="text-xs text-gray-500">{m.label}</div>
            </div>
          ))}
        </div>
      )}

      {/* Investment */}
      {activeSection === 'investment' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">💰 Investment Breakdown — {scenario?.label}</h3></div>
          <div className="card-body space-y-3">
            {Object.entries(bc.investment).map(([key, val]) => (
              <div key={key} className="flex items-start gap-4 p-4 bg-amber-50 rounded-lg border border-amber-200">
                <div className="w-32 shrink-0 text-xs font-bold text-amber-800 capitalize">{key}</div>
                <div className="text-sm text-gray-700">{val}</div>
              </div>
            ))}
            <div className="p-4 bg-amber-100 rounded-lg border border-amber-300 text-center">
              <div className="text-xl font-bold text-amber-800">Total: {bc.investmentRange}</div>
              <div className="text-xs text-amber-700 mt-1">One-time implementation investment</div>
            </div>
          </div>
        </div>
      )}

      {/* Benefits */}
      {activeSection === 'benefits' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">📈 Annual Benefits — {scenario?.label}</h3></div>
          <div className="card-body space-y-3">
            {Object.entries(bc.annualBenefits).map(([key, val]) => (
              <div key={key} className="flex items-start gap-4 p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="w-40 shrink-0 text-xs font-bold text-green-800">
                  {key === 'ttmImprovement' ? 'Time-to-Market' :
                   key === 'productivityGains' ? 'Productivity' :
                   key === 'qualityImprovement' ? 'Quality' : 'Operational Savings'}
                </div>
                <div className="text-sm text-gray-700">{val}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Org Changes */}
      {activeSection === 'org' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">👥 Organization Change Management — {scenario?.label}</h3></div>
          <div className="card-body">
            <ul className="space-y-3">
              {bc.orgChanges.map((c, i) => (
                <li key={i} className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <span className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">{i+1}</span>
                  <span className="text-sm text-gray-700">{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Tools */}
      {activeSection === 'tools' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🛠️ Tools & Platform Changes — {scenario?.label}</h3></div>
          <div className="card-body">
            <ul className="space-y-3">
              {bc.toolsChanges.map((c, i) => (
                <li key={i} className="flex items-start gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
                  <span className="text-purple-700 font-bold text-sm">🔧</span>
                  <span className="text-sm text-gray-700">{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* DevSecOps */}
      {activeSection === 'devsecops' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🔒 DevSecOps Changes — {scenario?.label}</h3></div>
          <div className="card-body">
            <ul className="space-y-3">
              {bc.devSecOps.map((c, i) => (
                <li key={i} className="flex items-start gap-3 p-4 bg-red-50 rounded-lg border border-red-200">
                  <span className="text-red-700">🛡️</span>
                  <span className="text-sm text-gray-700">{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* AIOps */}
      {activeSection === 'aiops' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🤖 AI Ops / Production Support — {scenario?.label}</h3></div>
          <div className="card-body">
            <ul className="space-y-3">
              {bc.aiOps.map((c, i) => (
                <li key={i} className="flex items-start gap-3 p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                  <span className="text-indigo-700">⚡</span>
                  <span className="text-sm text-gray-700">{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Product-centric */}
      {activeSection === 'product' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🎯 Product-Centric Ways of Working — {scenario?.label}</h3></div>
          <div className="card-body">
            <ul className="space-y-3">
              {bc.productCentricChanges.map((c, i) => (
                <li key={i} className="flex items-start gap-3 p-4 bg-teal-50 rounded-lg border border-teal-200">
                  <span className="text-teal-700">🎯</span>
                  <span className="text-sm text-gray-700">{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div className="flex gap-4">
        <Link to="/recommendations" className="btn-primary flex-1 text-center py-3">💡 View All Recommendations →</Link>
        <Link to="/future-state"    className="btn-secondary flex-1 text-center py-3">← Future State VSM</Link>
      </div>
    </div>
  )
}
