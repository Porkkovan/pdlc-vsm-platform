import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { Link } from 'react-router-dom'
import { US_BANK_DEMO } from '../data/demoData'

// ─── DORA Benchmark bands ────────────────────────────────────────────────────
const DORA_BANDS = {
  Elite:  { color: 'green',  bg: 'bg-green-50',  border: 'border-green-400', badge: 'bg-green-600',  label: 'Elite Performer' },
  High:   { color: 'blue',   bg: 'bg-blue-50',   border: 'border-blue-400',  badge: 'bg-blue-600',   label: 'High Performer' },
  Medium: { color: 'emerald',  bg: 'bg-cyan-50',  border: 'border-cyan-400', badge: 'bg-cyan-500',  label: 'Medium Performer' },
  Low:    { color: 'sky',    bg: 'bg-sky-50',    border: 'border-sky-400',   badge: 'bg-sky-600',    label: 'Low Performer' },
}

const DEPLOY_FREQ_SCORES = {
  'Multiple per day': 4, 'Once per day': 3.5, 'Several per week': 3,
  'Once per week': 2.5, 'Once per 2 weeks': 2, 'Once per month': 1, 'Less than monthly': 0,
}
const LT_CHANGE_SCORES = {
  'Less than 1 hour': 4, '1–24 hours': 3.5, '1–7 days': 3,
  '1–2 weeks': 2, '1 month': 1, '2–6 months': 0.5, 'More than 6 months': 0,
}
const CFR_SCORES     = (pct) => pct <= 5 ? 4 : pct <= 10 ? 3 : pct <= 15 ? 2 : pct <= 30 ? 1 : 0
const MTTR_SCORES = {
  'Less than 1 hour': 4, '1–24 hours': 3, '1–7 days': 2, '1–4 weeks': 1, 'More than 1 month': 0,
}

function calcProfile(m) {
  const scores = []
  if (m.deployFreq)    scores.push(DEPLOY_FREQ_SCORES[m.deployFreq] ?? 2)
  if (m.leadTimeChange) scores.push(LT_CHANGE_SCORES[m.leadTimeChange] ?? 2)
  if (m.changeFailRate !== '') scores.push(CFR_SCORES(Number(m.changeFailRate) || 0))
  if (m.mttr)          scores.push(MTTR_SCORES[m.mttr] ?? 2)
  if (!scores.length)  return null
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length
  if (avg >= 3.5) return 'Elite'
  if (avg >= 2.5) return 'High'
  if (avg >= 1.5) return 'Medium'
  return 'Low'
}

export function doraToVsmCalibration(m) {
  const cal = {}
  const deployWtMap = {
    'Multiple per day': 1, 'Once per day': 4, 'Several per week': 12,
    'Once per week': 24, 'Once per 2 weeks': 40, 'Once per month': 80, 'Less than monthly': 160
  }
  if (m.deployFreq)    cal.phase6_wt = deployWtMap[m.deployFreq]
  const mttrWtMap = {
    'Less than 1 hour': 2, '1–24 hours': 8, '1–7 days': 24, '1–4 weeks': 60, 'More than 1 month': 120
  }
  if (m.mttr)          cal.phase7_wt = mttrWtMap[m.mttr]
  if (m.buildDuration) cal.phase4_pt = Math.round(Number(m.buildDuration) / 60 * 8)
  if (m.codeReviewHours) cal.phase3_wt = Number(m.codeReviewHours)
  if (m.changeFailRate) cal.phase5_rework_factor = 1 + (Number(m.changeFailRate) / 100) * 0.5
  const ltDaysMap = {
    'Less than 1 hour': 0.1, '1–24 hours': 0.5, '1–7 days': 3,
    '1–2 weeks': 10, '1 month': 22, '2–6 months': 60, 'More than 6 months': 120
  }
  if (m.leadTimeChange) cal.phases3to6_lt_days = ltDaysMap[m.leadTimeChange]
  return cal
}

const PROFILE_RECS = {
  Elite:  { vsm_note: 'World-class delivery. VSM focuses on phases 1–2 (product definition) and remaining approval gates.', option_rec: 'Option C (AI-First / ADLC)', priority_phases: [1, 2, 7], key_gap: 'Eliminate remaining planning cycle waste and automate final human gates' },
  High:   { vsm_note: 'Strong performance. VSM will surface remaining wait time in testing and planning phases.', option_rec: 'Option B or C', priority_phases: [1, 2, 5], key_gap: 'Reduce planning WT (phases 1–2) and testing approval gates (phase 5)' },
  Medium: { vsm_note: 'Significant bottlenecks in testing and release. VSM confirms which phases are the primary drag.', option_rec: 'Option A or B', priority_phases: [5, 6, 3], key_gap: 'Automate testing signoff (phase 5), release gating (phase 6), code review (phase 3)' },
  Low:    { vsm_note: 'Substantial transformation needed. Multiple compounding bottlenecks across delivery pipeline.', option_rec: 'Option A (start), then B', priority_phases: [3, 4, 5, 6], key_gap: 'Build CI/CD foundation first (phases 3–6) before adding AI automation' },
}

const PHASE_NAMES = { 1: 'Backlog & Roadmap', 2: 'Architecture & UX', 3: 'Code Management', 4: 'Continuous Integration', 5: 'Continuous Testing', 6: 'Continuous Delivery', 7: 'Monitoring & Feedback' }

const CONFIDENCE_COLOR = (c) => c >= 90 ? 'text-green-600' : c >= 75 ? 'text-blue-600' : 'text-cyan-600'
const CONFIDENCE_BG    = (c) => c >= 90 ? 'bg-green-50 border-green-200' : c >= 75 ? 'bg-blue-50 border-blue-200' : 'bg-cyan-50 border-cyan-200'

// Map metric key → notes key
const METRIC_NOTES_MAP = {
  deployFreq:        'deployFreq',
  leadTimeChange:    'leadTimeChange',
  changeFailRate:    'changeFailRate',
  mttr:              'mttr',
  buildDuration:     'buildDuration',
  codeReviewHours:   'codeReviewHours',
  testCoverage:      'testCoverage',
  automatedTestPct:  'automatedTestPct',
  infraAutomationPct:'infraAutomationPct',
}

// ─── SourceNote component ─────────────────────────────────────────────────────
function SourceNote({ metricKey, notes, accepted, onAccept, onOverride }) {
  const n = notes?.[metricKey]
  const [showSources, setShowSources] = useState(false)
  if (!n) return null
  return (
    <div className={`mt-2 rounded-xl border p-3 ${CONFIDENCE_BG(n.confidence)}`}>
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-gray-600">🤖 AI Suggested:</span>
          <span className="text-xs font-bold text-blue-700">{n.aiSuggestedValue}</span>
          <span className={`text-xs font-semibold ${CONFIDENCE_COLOR(n.confidence)}`}>
            {n.confidence}% confidence
          </span>
        </div>
        <div className="flex gap-1 shrink-0">
          {!accepted ? (
            <>
              <button onClick={onAccept}
                className="text-xs px-2 py-0.5 bg-green-600 text-white rounded font-semibold hover:bg-green-700">
                ✓ Accept
              </button>
              <button onClick={onOverride}
                className="text-xs px-2 py-0.5 bg-gray-200 text-gray-700 rounded font-semibold hover:bg-gray-300">
                Override
              </button>
            </>
          ) : (
            <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded font-semibold">✓ Accepted</span>
          )}
        </div>
      </div>

      {/* Root cause / gap */}
      <div className="mb-2">
        <div className="text-xs font-semibold text-sky-600 mb-0.5">⚠ Root Cause / Gap:</div>
        <p className="text-xs text-gray-700 leading-relaxed">{n.rootCause}</p>
      </div>

      {n.gap && (
        <div className="mb-2 bg-white/70 rounded-lg px-2.5 py-1.5 border border-gray-200">
          <div className="text-xs font-semibold text-blue-600 mb-0.5">📊 Improvement Opportunity:</div>
          <p className="text-xs text-gray-600">{n.gap}</p>
        </div>
      )}

      {/* Sources */}
      <button onClick={() => setShowSources(s => !s)}
        className="text-xs text-blue-500 hover:text-blue-700 font-semibold">
        {showSources ? '▲ Hide sources' : `▼ Show ${n.sources?.length || 0} source documents`}
      </button>
      {showSources && n.sources && (
        <div className="mt-2 space-y-1.5">
          {n.sources.map((src, i) => (
            <div key={i} className="bg-white border border-gray-200 rounded-lg p-2.5">
              <div className="text-xs font-bold text-gray-700 mb-0.5">📄 {src.doc}</div>
              <div className="text-xs text-gray-600">{src.finding}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── Team Context Selector ────────────────────────────────────────────────────
function TeamContextSelector({ project, onApply }) {
  const portfolios    = project.portfolios    || []
  const productGroups = project.productGroups || []
  const hasStructure  = portfolios.length > 0 || productGroups.length > 0

  const [selPortfolio, setSelPortfolio] = useState(project.portfolio    || '')
  const [selGroup,     setSelGroup]     = useState(project.productGroup || '')
  const [selProduct,   setSelProduct]   = useState(project.product      || '')
  const [selTeam,      setSelTeam]      = useState(project.team         || '')

  const groupObj          = productGroups.find(g => g.name === selGroup)
  const availableProducts = groupObj?.products || []
  const productObj        = availableProducts.find(p => p.name === selProduct)
  const availableTeams    = productObj?.teams || []

  const handleGroupChange   = (g) => { setSelGroup(g); setSelProduct(''); setSelTeam('') }
  const handleProductChange = (p) => { setSelProduct(p); setSelTeam('') }

  const handleApply = () => {
    if (!selGroup || !selProduct || !selTeam) return
    onApply(selPortfolio, selGroup, selProduct, selTeam)
  }

  const isCurrentSelection =
    project.productGroup === selGroup &&
    project.product      === selProduct &&
    project.team         === selTeam && !!selTeam

  const colCount = portfolios.length > 0 ? 4 : 3

  return (
    <div className="card">
      <div className="card-header bg-gradient-to-r from-violet-400 to-violet-500 text-white rounded-t-xl">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h3 className="font-bold text-lg">Select Team Context</h3>
            <p className="text-violet-100 text-sm">
              Choose the product group, product, and team to assess. All subsequent modules
              (VSM, Bottlenecks, Future State, etc.) run for this context. Return here to switch teams.
            </p>
          </div>
          {project.team && (
            <div className="shrink-0 bg-white/20 rounded-xl px-4 py-2 text-sm text-white font-semibold text-right">
              <div className="text-xs text-violet-200 mb-0.5">Currently assessing</div>
              <div>👥 {project.team}</div>
              {project.product      && <div className="text-xs text-violet-200">🗂 {project.product}</div>}
              {project.productGroup && <div className="text-xs text-violet-200">📦 {project.productGroup}</div>}
            </div>
          )}
        </div>
      </div>

      <div className="card-body">
        {!hasStructure && (
          <div className="mb-4 flex items-start gap-3 bg-cyan-50 border border-cyan-200 rounded-lg px-4 py-3">
            <span className="text-cyan-500 text-lg shrink-0">⚠</span>
            <div className="text-xs text-cyan-800">
              <span className="font-semibold">No org structure set up yet.</span>{' '}
              The dropdowns below are empty.{' '}
              <a href="/alm-connect" className="font-semibold underline hover:text-cyan-900">
                Go to ALM Connect → Organisation Setup
              </a>{' '}
              to add your Product Groups, Products, and Teams — then return here to select from dropdowns.
            </div>
          </div>
        )}

        <div
          className="grid gap-4"
          style={{ gridTemplateColumns: `repeat(${colCount}, minmax(0, 1fr))` }}
        >
          {portfolios.length > 0 && (
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Portfolio / Segment</label>
              <select value={selPortfolio} onChange={e => setSelPortfolio(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500">
                <option value="">All Portfolios</option>
                {portfolios.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1">Product Group *</label>
            <select value={selGroup} onChange={e => handleGroupChange(e.target.value)}
              disabled={!hasStructure}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 disabled:bg-gray-100 disabled:text-gray-400">
              <option value="">{hasStructure ? 'Select group...' : 'Set up org structure first'}</option>
              {productGroups.map(g => <option key={g.name} value={g.name}>{g.name}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1">Product *</label>
            <select value={selProduct} onChange={e => handleProductChange(e.target.value)}
              disabled={!selGroup}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 disabled:bg-gray-100 disabled:text-gray-400">
              <option value="">{selGroup ? 'Select product...' : 'Select group first'}</option>
              {availableProducts.map(p => <option key={p.name} value={p.name}>{p.name}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1">Product Team *</label>
            <select value={selTeam} onChange={e => setSelTeam(e.target.value)}
              disabled={!selProduct}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 disabled:bg-gray-100 disabled:text-gray-400">
              <option value="">{selProduct ? 'Select team...' : 'Select product first'}</option>
              {availableTeams.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
        </div>

        <div className="mt-4 flex items-center gap-3">
          <button onClick={handleApply}
            disabled={!selGroup || !selProduct || !selTeam || !!isCurrentSelection}
            className="px-5 py-2 bg-violet-600 text-white text-sm font-semibold rounded-lg hover:bg-violet-700 transition-colors disabled:opacity-50">
            {isCurrentSelection ? '✓ Context Applied' : 'Apply Team Context →'}
          </button>
          {hasStructure && (!selGroup || !selProduct || !selTeam) && (
            <p className="text-xs text-gray-500">Select Product Group → Product → Team to apply.</p>
          )}
        </div>
      </div>
    </div>
  )
}

// ─── Main Component ───────────────────────────────────────────────────────────
export default function DORAAssessmentPage() {
  const { doraMetrics, setDoraMetrics, doraProfile, setDoraProfile, addNotification, project,
          saveProject, setProject, setVsmLevel } = useApp()

  const [m, setM] = useState(doraMetrics || {
    deployFreq: '', leadTimeChange: '', changeFailRate: '', mttr: '',
    buildDuration: '', codeReviewHours: '', testCoverage: '', mttd: '',
    automatedTestPct: '', infraAutomationPct: '', incidentFreq: '',
  })
  const [saved, setSaved]           = useState(!!doraMetrics)
  const [aiNotes, setAiNotes]       = useState(null)   // null = not loaded, {} = loaded
  const [accepted, setAccepted]     = useState({})     // which metrics user accepted
  const [aiLoading, setAiLoading]   = useState(false)
  const [showNotes, setShowNotes]   = useState(true)

  const profile = calcProfile(m)
  const band    = profile ? DORA_BANDS[profile] : null
  const rec     = profile ? PROFILE_RECS[profile] : null
  const cal     = doraToVsmCalibration(m)
  const setF    = (k, v) => { setM(p => ({ ...p, [k]: v })); setSaved(false) }

  const handleApply = () => {
    setDoraMetrics(m)
    setDoraProfile(profile)
    setSaved(true)
    addNotification(`DORA profile: ${profile} — VSM calibration applied`, 'success')
  }

  // ── Load demo data (US Bank) ──────────────────────────────────────────────
  const loadDemoData = async () => {
    setAiLoading(true)
    await new Promise(r => setTimeout(r, 800)) // simulate AI analysis
    const dm = US_BANK_DEMO.doraMetrics
    setM(dm)
    setAiNotes(US_BANK_DEMO.doraAutoScoreNotes)
    setAccepted({})
    // also pre-fill project if empty
    if (!project.organization) {
      saveProject(US_BANK_DEMO.project).catch(() => {})
    }
    setAiLoading(false)
    addNotification('US Bank demo data loaded — AI analysis ready for review', 'success')
  }

  // ── Accept a single AI suggestion ─────────────────────────────────────────
  const acceptOne = (key) => {
    if (!aiNotes?.[key]) return
    setAccepted(a => ({ ...a, [key]: true }))
    // value already set from loadDemoData — just mark accepted
  }

  // ── Accept all suggestions ────────────────────────────────────────────────
  const acceptAll = () => {
    if (!aiNotes) return
    const all = {}
    Object.keys(aiNotes).forEach(k => { all[k] = true })
    setAccepted(all)
    addNotification('All AI suggestions accepted', 'success')
  }

  // ── Override (clear acceptance) ───────────────────────────────────────────
  const overrideOne = (key) => setAccepted(a => ({ ...a, [key]: false }))

  const coreCount = [m.deployFreq, m.leadTimeChange, m.changeFailRate, m.mttr].filter(Boolean).length
  const extCount  = [m.buildDuration, m.codeReviewHours, m.testCoverage, m.mttd, m.automatedTestPct, m.infraAutomationPct].filter(Boolean).length
  const acceptedCount = Object.values(accepted).filter(Boolean).length
  const totalNotes = Object.keys(aiNotes || {}).length

  const handleTeamApply = async (portfolio, productGroup, product, team) => {
    const updated = { ...project, portfolio, productGroup, product, team }
    try {
      await saveProject(updated)
    } catch {
      setProject(prev => ({ ...prev, portfolio, productGroup, product, team }))
    }
    addNotification(`Team context set: ${productGroup} → ${product} → ${team}`, 'success')
  }

  return (
    <div className="space-y-6 fade-in">

      {/* Team context selector (only shown when org structure is defined) */}
      <TeamContextSelector project={project} onApply={handleTeamApply} />

      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-600 to-blue-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">DORA Assessment</h2>
            <p className="text-cyan-100 text-sm">
              Baseline your DevOps performance before creating the current state VSM.
              AI auto-scores each metric from uploaded data sources — review root causes, validate sources, then apply calibration.
            </p>
            {project.team && (
              <div className="mt-2 flex items-center gap-2 flex-wrap">
                {project.organization && <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">🏢 {project.organization}</span>}
                {project.productGroup && <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">📦 {project.productGroup}</span>}
                {project.product      && <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">🗂 {project.product}</span>}
                <span className="bg-white/20 text-white text-xs font-semibold px-2.5 py-1 rounded-full">👥 {project.team}</span>
              </div>
            )}
          </div>
          <div className="flex items-center gap-3">
            {saved && profile && (
              <div className={`${band.badge} text-white px-4 py-2 rounded-xl font-bold text-sm shadow`}>
                {profile} Performer ✓
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI Auto-Score panel */}
      <div className={`border-2 rounded-2xl p-5 ${aiNotes ? 'border-blue-300 bg-blue-50' : 'border-dashed border-gray-300 bg-gray-50'}`}>
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xl">🤖</span>
              <h3 className="font-bold text-gray-800">AI Auto-Score from Data Sources</h3>
              {aiNotes && <span className="text-xs bg-blue-600 text-white px-2 py-0.5 rounded font-bold">Active — {acceptedCount}/{totalNotes} accepted</span>}
            </div>
            <p className="text-sm text-gray-600">
              {aiNotes
                ? 'AI has analysed uploaded data sources (Jira, GitHub, PagerDuty, SonarQube) and suggested DORA scores with root cause explanations. Review each metric, validate the source evidence, then accept or override.'
                : 'Load demo data to see AI-suggested DORA scores with source evidence and root cause analysis per metric. In live mode, connect your ALM tool and upload data sources first.'}
            </p>
          </div>
          <div className="flex gap-2 shrink-0">
            {aiNotes && (
              <>
                <button onClick={() => setShowNotes(s => !s)}
                  className="text-xs px-3 py-2 bg-white border border-gray-300 rounded-lg font-semibold hover:bg-gray-50">
                  {showNotes ? '▲ Hide Notes' : '▼ Show Notes'}
                </button>
                <button onClick={acceptAll}
                  className="text-xs px-3 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700">
                  ✓ Accept All ({totalNotes - acceptedCount} remaining)
                </button>
              </>
            )}
            <button onClick={loadDemoData} disabled={aiLoading}
              className="text-sm px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 shadow">
              {aiLoading ? '⏳ Analysing...' : '🏦 Load US Bank Demo Data'}
            </button>
          </div>
        </div>

        {aiNotes && showNotes && (
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { key: 'deployFreq',    label: 'Deploy Frequency',        icon: '🚀' },
              { key: 'leadTimeChange',label: 'Lead Time for Change',     icon: '⏱' },
              { key: 'changeFailRate',label: 'Change Failure Rate',      icon: '⚠️' },
              { key: 'mttr',          label: 'MTTR',                     icon: '🔧' },
            ].filter(f => aiNotes[f.key]).map(f => (
              <div key={f.key} className="bg-white rounded-xl border border-gray-200 p-3">
                <div className="text-sm font-bold text-gray-800 mb-1">{f.icon} {f.label}</div>
                <SourceNote
                  metricKey={f.key}
                  notes={aiNotes}
                  accepted={accepted[f.key]}
                  onAccept={() => acceptOne(f.key)}
                  onOverride={() => overrideOne(f.key)}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Why DORA maps to VSM */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {[
          { metric: 'Deployment Frequency', feeds: 'Phase 6 Wait Time', icon: '🚀', desc: 'Weekly deploys → 24h release gate WT' },
          { metric: 'Lead Time for Change', feeds: 'Phases 3–6 Total LT', icon: '⏱', desc: 'Commit-to-prod time calibrates 4 phases' },
          { metric: 'Change Failure Rate',  feeds: 'Phase 5 Rework PT', icon: '⚠️', desc: 'Each failure adds ~50% rework to testing PT' },
          { metric: 'MTTR',                 feeds: 'Phase 7 Wait Time', icon: '🔧', desc: 'Recovery time calibrates monitoring phase WT' },
        ].map(d => (
          <div key={d.metric} className="bg-white border border-gray-200 rounded-xl p-4">
            <div className="text-2xl mb-2">{d.icon}</div>
            <div className="font-bold text-gray-800 text-sm">{d.metric}</div>
            <div className="text-xs text-blue-700 font-semibold mt-1">→ {d.feeds}</div>
            <div className="text-xs text-gray-500 mt-1">{d.desc}</div>
          </div>
        ))}
      </div>

      {/* Core 4 DORA metrics */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Core DORA Metrics ({coreCount}/4)</h3>
          <p className="text-xs text-gray-500">The 4 official DORA metrics — each maps to a specific VSM phase calibration</p>
        </div>
        <div className="card-body grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Deployment Frequency */}
          <div>
            <label className="text-sm font-bold text-gray-700 block mb-1">
              Deployment Frequency
              <span className="ml-2 text-xs font-normal text-gray-400">How often do you deploy to production?</span>
            </label>
            <select value={m.deployFreq} onChange={e => setF('deployFreq', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500">
              <option value="">— Select —</option>
              {Object.keys(DEPLOY_FREQ_SCORES).map(o => <option key={o} value={o}>{o}</option>)}
            </select>
            <div className="mt-1 text-xs text-gray-400 grid grid-cols-4 gap-1">
              <span className="text-green-600">Elite: Multiple/day</span>
              <span className="text-blue-600">High: Daily</span>
              <span className="text-cyan-600">Med: Weekly</span>
              <span className="text-sky-600">Low: Monthly+</span>
            </div>
            {aiNotes && showNotes && (
              <SourceNote metricKey="deployFreq" notes={aiNotes} accepted={accepted.deployFreq}
                onAccept={() => acceptOne('deployFreq')} onOverride={() => overrideOne('deployFreq')} />
            )}
          </div>

          {/* Lead Time for Change */}
          <div>
            <label className="text-sm font-bold text-gray-700 block mb-1">
              Lead Time for Change
              <span className="ml-2 text-xs font-normal text-gray-400">Commit → running in production</span>
            </label>
            <select value={m.leadTimeChange} onChange={e => setF('leadTimeChange', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500">
              <option value="">— Select —</option>
              {Object.keys(LT_CHANGE_SCORES).map(o => <option key={o} value={o}>{o}</option>)}
            </select>
            <div className="mt-1 text-xs text-gray-400 grid grid-cols-4 gap-1">
              <span className="text-green-600">Elite: &lt;1h</span>
              <span className="text-blue-600">High: &lt;1 day</span>
              <span className="text-cyan-600">Med: &lt;1 week</span>
              <span className="text-sky-600">Low: 1 month+</span>
            </div>
            {aiNotes && showNotes && (
              <SourceNote metricKey="leadTimeChange" notes={aiNotes} accepted={accepted.leadTimeChange}
                onAccept={() => acceptOne('leadTimeChange')} onOverride={() => overrideOne('leadTimeChange')} />
            )}
          </div>

          {/* Change Failure Rate */}
          <div>
            <label className="text-sm font-bold text-gray-700 block mb-1">
              Change Failure Rate (%)
              <span className="ml-2 text-xs font-normal text-gray-400">% of deployments causing production failures</span>
            </label>
            <div className="relative">
              <input type="number" min="0" max="100" value={m.changeFailRate}
                onChange={e => setF('changeFailRate', e.target.value)}
                placeholder="e.g. 12"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 pr-8" />
              <span className="absolute right-3 top-2.5 text-gray-400 text-sm">%</span>
            </div>
            <div className="mt-1 text-xs text-gray-400 grid grid-cols-4 gap-1">
              <span className="text-green-600">Elite: &lt;5%</span>
              <span className="text-blue-600">High: 5–10%</span>
              <span className="text-cyan-600">Med: 10–15%</span>
              <span className="text-sky-600">Low: &gt;15%</span>
            </div>
            {aiNotes && showNotes && (
              <SourceNote metricKey="changeFailRate" notes={aiNotes} accepted={accepted.changeFailRate}
                onAccept={() => acceptOne('changeFailRate')} onOverride={() => overrideOne('changeFailRate')} />
            )}
          </div>

          {/* MTTR */}
          <div>
            <label className="text-sm font-bold text-gray-700 block mb-1">
              MTTR (Mean Time to Restore)
              <span className="ml-2 text-xs font-normal text-gray-400">Time to recover from production failure</span>
            </label>
            <select value={m.mttr} onChange={e => setF('mttr', e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500">
              <option value="">— Select —</option>
              {Object.keys(MTTR_SCORES).map(o => <option key={o} value={o}>{o}</option>)}
            </select>
            <div className="mt-1 text-xs text-gray-400 grid grid-cols-4 gap-1">
              <span className="text-green-600">Elite: &lt;1h</span>
              <span className="text-blue-600">High: &lt;1 day</span>
              <span className="text-cyan-600">Med: &lt;1 week</span>
              <span className="text-sky-600">Low: &gt;1 week</span>
            </div>
            {aiNotes && showNotes && (
              <SourceNote metricKey="mttr" notes={aiNotes} accepted={accepted.mttr}
                onAccept={() => acceptOne('mttr')} onOverride={() => overrideOne('mttr')} />
            )}
          </div>
        </div>
      </div>

      {/* Extended metrics */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Extended Metrics ({extCount}/6) — VSM Phase Calibration</h3>
          <p className="text-xs text-gray-500">Measured actuals that replace estimated PT/WT ranges in the VSM — each metric calibrates a specific phase</p>
        </div>
        <div className="card-body grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[
            { key: 'buildDuration',      label: 'Average CI Build Duration', unit: 'minutes', placeholder: 'e.g. 18', calibrates: 'Phase 4 PT', hint: 'P50 build time from git push to pipeline complete' },
            { key: 'codeReviewHours',    label: 'Code Review Cycle Time',    unit: 'hours',   placeholder: 'e.g. 6',  calibrates: 'Phase 3 WT', hint: 'PR opened to first review comment (P50 median)' },
            { key: 'testCoverage',       label: 'Automated Test Coverage',   unit: '%',       placeholder: 'e.g. 68', calibrates: 'Phase 5 WT', hint: 'Percentage of code covered by automated tests' },
            { key: 'mttd',               label: 'MTTD (Mean Time to Detect)',unit: 'hours',   placeholder: 'e.g. 4',  calibrates: 'Phase 7 WT', hint: 'Time from failure to alert firing (P50)' },
            { key: 'automatedTestPct',   label: 'Automated Test Execution %',unit: '%',       placeholder: 'e.g. 55', calibrates: 'Phase 5 PT', hint: 'Percentage of test execution that is fully automated' },
            { key: 'infraAutomationPct', label: 'Infrastructure Automation', unit: '%',       placeholder: 'e.g. 70', calibrates: 'Phase 6 PT', hint: 'Percentage of infra provisioned via IaC (Terraform, ARM, CDK)' },
          ].map(f => (
            <div key={f.key}>
              <label className="text-xs font-bold text-gray-700 block mb-0.5">{f.label}</label>
              <div className="text-xs text-blue-600 mb-1 font-semibold">→ calibrates {f.calibrates}</div>
              <div className="relative">
                <input type="number" min="0" value={m[f.key] || ''}
                  onChange={e => setF(f.key, e.target.value)}
                  placeholder={f.placeholder}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 pr-14" />
                <span className="absolute right-3 top-2.5 text-gray-400 text-xs">{f.unit}</span>
              </div>
              <div className="text-xs text-gray-400 mt-1">{f.hint}</div>
              {aiNotes && showNotes && aiNotes[f.key] && (
                <SourceNote metricKey={f.key} notes={aiNotes} accepted={accepted[f.key]}
                  onAccept={() => acceptOne(f.key)} onOverride={() => overrideOne(f.key)} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Live DORA Profile */}
      {profile && band && rec && (
        <div className={`${band.bg} border-2 ${band.border} rounded-2xl p-6`}>
          <div className="flex items-start gap-5 flex-wrap">
            <div className="text-center">
              <div className={`${band.badge} text-white text-3xl font-black w-24 h-24 rounded-2xl flex items-center justify-center shadow-lg`}>
                {profile[0]}
              </div>
              <div className={`text-sm font-bold mt-2 text-${band.color}-800`}>{band.label}</div>
            </div>
            <div className="flex-1 min-w-0">
              <h3 className={`font-bold text-${band.color}-800 text-lg mb-2`}>DORA Profile: {profile} Performer</h3>
              <p className={`text-sm text-${band.color}-700 mb-4`}>{rec.vsm_note}</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                <div className="bg-white/70 rounded-xl p-3 border border-white/50">
                  <div className="text-xs text-gray-500 mb-0.5">Recommended Scenario</div>
                  <div className={`font-bold text-${band.color}-700`}>{rec.option_rec}</div>
                </div>
                <div className="bg-white/70 rounded-xl p-3 border border-white/50 md:col-span-2">
                  <div className="text-xs text-gray-500 mb-0.5">Primary Focus for Improvement</div>
                  <div className="font-semibold text-gray-800 text-sm">{rec.key_gap}</div>
                </div>
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-600 mb-2">VSM phases requiring most attention for your profile:</div>
                <div className="flex flex-wrap gap-2">
                  {rec.priority_phases.map(p => (
                    <span key={p} className={`bg-${band.color}-100 text-${band.color}-800 text-xs font-bold px-3 py-1.5 rounded-lg border border-${band.color}-300`}>
                      Phase {p}: {PHASE_NAMES[p]}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Validation status banner (when AI notes loaded) */}
      {aiNotes && (
        <div className={`rounded-xl border px-4 py-3 flex items-center justify-between flex-wrap gap-3 ${
          acceptedCount === totalNotes
            ? 'bg-green-50 border-green-300'
            : 'bg-cyan-50 border-cyan-300'
        }`}>
          <div>
            <div className={`font-bold text-sm ${acceptedCount === totalNotes ? 'text-green-800' : 'text-cyan-800'}`}>
              {acceptedCount === totalNotes
                ? '✅ All AI scores validated — ready to apply calibration'
                : `⚠️ ${totalNotes - acceptedCount} metric${totalNotes - acceptedCount > 1 ? 's' : ''} pending validation`}
            </div>
            <div className={`text-xs ${acceptedCount === totalNotes ? 'text-green-700' : 'text-cyan-700'}`}>
              {acceptedCount}/{totalNotes} metrics accepted · Validation confirms relevance, context, and accuracy before proceeding to VSM
            </div>
          </div>
          {acceptedCount < totalNotes && (
            <button onClick={acceptAll}
              className="text-sm px-4 py-2 bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-700">
              Accept Remaining {totalNotes - acceptedCount}
            </button>
          )}
        </div>
      )}

      {/* VSM Calibration Preview */}
      {Object.keys(cal).length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="font-bold text-gray-800">VSM Calibration Preview</h3>
            <p className="text-xs text-gray-500">These measured values will replace estimated defaults in your current state VSM</p>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {[
                { key: 'phase3_wt',          label: 'Phase 3 — Code Review WT',       unit: 'h', source: 'Code review cycle time' },
                { key: 'phase4_pt',           label: 'Phase 4 — CI Build PT',          unit: 'h', source: 'Build duration metric' },
                { key: 'phase5_rework_factor',label: 'Phase 5 — Rework Multiplier',    unit: '×', source: 'Change failure rate' },
                { key: 'phase6_wt',           label: 'Phase 6 — Release Gate WT',      unit: 'h', source: 'Deployment frequency' },
                { key: 'phase7_wt',           label: 'Phase 7 — Incident Response WT', unit: 'h', source: 'MTTR' },
                { key: 'phases3to6_lt_days',  label: 'Phases 3–6 — Delivery LT',       unit: 'd', source: 'Lead time for change' },
              ].filter(c => cal[c.key] !== undefined).map(c => (
                <div key={c.key} className="bg-blue-50 border border-blue-200 rounded-xl p-3">
                  <div className="text-xs text-gray-500">{c.label}</div>
                  <div className="font-bold text-blue-700 text-lg mt-0.5">
                    {typeof cal[c.key] === 'number' ? cal[c.key].toFixed(c.unit === '×' ? 2 : 0) : cal[c.key]}{c.unit}
                  </div>
                  <div className="text-xs text-blue-500 mt-0.5">Source: {c.source}</div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-xl">
              <div className="font-bold text-green-800 text-sm mb-1">
                ✅ VSM Accuracy Improvement: +{Math.min(Object.keys(cal).length * 3 + (profile ? 5 : 0), 25)}% from DORA calibration
              </div>
              <div className="text-xs text-green-700">
                {Object.keys(cal).length} phase metric{Object.keys(cal).length > 1 ? 's' : ''} will use your measured DORA values instead of industry-default estimates.
                {profile === 'Medium' && ' Medium profile: testing signoff and release gating are likely the largest bottlenecks — VSM will confirm.'}
                {profile === 'Low'    && ' Low profile: multiple compounding bottlenecks across phases 3–6 expected.'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* DORA bands reference table */}
      <div className="card">
        <div className="card-header"><h3 className="font-bold text-gray-800">DORA Performance Bands — 2024 State of DevOps Benchmarks</h3></div>
        <div className="card-body overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-2 pr-4 font-semibold text-gray-700">Profile</th>
                <th className="text-center py-2 px-3 font-semibold">Deploy Frequency</th>
                <th className="text-center py-2 px-3 font-semibold">Lead Time</th>
                <th className="text-center py-2 px-3 font-semibold">Failure Rate</th>
                <th className="text-center py-2 px-3 font-semibold">MTTR</th>
                <th className="text-left py-2 pl-3 font-semibold">VSM Implication</th>
              </tr>
            </thead>
            <tbody>
              {[
                { profile: 'Elite',  df: 'Multiple/day',   lt: '< 1 hour',    cfr: '< 5%',   mttr: '< 1 hour',   impl: 'Phases 1–2 are the bottleneck — delivery already automated', color: 'green' },
                { profile: 'High',   df: 'Daily–weekly',   lt: '1 day–1 wk',  cfr: '5–10%',  mttr: '< 1 day',    impl: 'Testing and planning phases drive remaining WT', color: 'blue' },
                { profile: 'Medium', df: 'Weekly–monthly', lt: '1–4 weeks',   cfr: '10–15%', mttr: '< 1 week',   impl: 'Release gating and UAT signoff are critical bottlenecks', color: 'emerald' },
                { profile: 'Low',    df: '< Monthly',      lt: '1–6 months',  cfr: '> 15%',  mttr: '> 1 week',   impl: 'CI/CD foundation needs building before AI automation', color: 'sky' },
              ].map(r => (
                <tr key={r.profile} className={`border-b border-gray-100 ${profile === r.profile ? `bg-${r.color}-50` : ''}`}>
                  <td className="py-2.5 pr-4"><span className={`bg-${r.color}-600 text-white text-xs font-bold px-2 py-0.5 rounded-full`}>{r.profile}</span></td>
                  <td className="py-2.5 px-3 text-center text-gray-700">{r.df}</td>
                  <td className="py-2.5 px-3 text-center text-gray-700">{r.lt}</td>
                  <td className="py-2.5 px-3 text-center text-gray-700">{r.cfr}</td>
                  <td className="py-2.5 px-3 text-center text-gray-700">{r.mttr}</td>
                  <td className="py-2.5 pl-3 text-gray-600">{r.impl}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Apply button */}
      <div className="bg-white border-2 border-cyan-200 rounded-2xl p-6 text-center">
        <div className="mb-3">
          {!profile && <p className="text-gray-600 text-sm">Fill in at least the 4 core DORA metrics to classify your profile and apply calibration to the VSM.</p>}
          {profile && !saved && (
            <p className="text-gray-700 text-sm">
              Profile: <strong className={`text-${band.color}-700`}>{profile} Performer</strong>.
              {aiNotes && acceptedCount < totalNotes && <span className="text-cyan-600"> Validate {totalNotes - acceptedCount} remaining AI suggestions before applying.</span>}
              {(!aiNotes || acceptedCount === totalNotes) && ' Click below to apply calibration to your VSM.'}
            </p>
          )}
          {saved && <p className="text-green-700 font-semibold text-sm">✅ DORA calibration applied — {Object.keys(cal).length} VSM phase metrics use measured values.</p>}
        </div>
        <div className="flex gap-3 justify-center flex-wrap">
          <button onClick={handleApply} disabled={!profile}
            className="btn-primary px-8 py-3 text-sm font-bold disabled:opacity-40">
            {saved ? '✅ Calibration Applied' : `🎯 Apply ${profile || 'DORA'} Calibration to VSM`}
          </button>
          {saved && (
            <Link to="/current-vsm" className="btn-secondary px-8 py-3 text-sm font-bold">
              View DORA-Calibrated VSM →
            </Link>
          )}
        </div>
        {profile && (
          <div className="text-xs text-gray-400 mt-2">
            Calibrating {Object.keys(cal).length} phase metrics · {profile} profile → recommends {rec.option_rec}
          </div>
        )}
      </div>

      <div className="flex gap-4 pb-6">
        <Link to="/alm-connect"  className="btn-secondary flex-1 text-center py-3">← ALM Connect</Link>
        <Link to="/current-vsm"  className="btn-primary  flex-1 text-center py-3">Current State VSM →</Link>
      </div>
    </div>
  )
}
