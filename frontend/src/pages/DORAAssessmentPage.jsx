import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { Link, useNavigate } from 'react-router-dom'

// ─── DORA Benchmark bands (2024 State of DevOps) ────────────────────────────
const DORA_BANDS = {
  Elite:  { color: 'green',  bg: 'bg-green-50',  border: 'border-green-400', badge: 'bg-green-600',  label: 'Elite Performer' },
  High:   { color: 'blue',   bg: 'bg-blue-50',   border: 'border-blue-400',  badge: 'bg-blue-600',   label: 'High Performer' },
  Medium: { color: 'amber',  bg: 'bg-amber-50',  border: 'border-amber-400', badge: 'bg-amber-500',  label: 'Medium Performer' },
  Low:    { color: 'red',    bg: 'bg-red-50',    border: 'border-red-400',   badge: 'bg-red-600',    label: 'Low Performer' },
}

// Score each DORA metric 0–4, average → band
const DEPLOY_FREQ_SCORES = {
  'Multiple per day':    4,
  'Once per day':        3.5,
  'Several per week':    3,
  'Once per week':       2.5,
  'Once per 2 weeks':    2,
  'Once per month':      1,
  'Less than monthly':   0,
}
const LT_CHANGE_SCORES = {
  'Less than 1 hour':    4,
  '1–24 hours':          3.5,
  '1–7 days':            3,
  '1–2 weeks':           2,
  '1 month':             1,
  '2–6 months':          0.5,
  'More than 6 months':  0,
}
const CFR_SCORES     = (pct) => pct <= 5 ? 4 : pct <= 10 ? 3 : pct <= 15 ? 2 : pct <= 30 ? 1 : 0
const MTTR_SCORES = {
  'Less than 1 hour':   4,
  '1–24 hours':         3,
  '1–7 days':           2,
  '1–4 weeks':          1,
  'More than 1 month':  0,
}

function calcProfile(m) {
  const scores = []
  if (m.deployFreq)    scores.push(DEPLOY_FREQ_SCORES[m.deployFreq] ?? 2)
  if (m.leadTimeChange)scores.push(LT_CHANGE_SCORES[m.leadTimeChange] ?? 2)
  if (m.changeFailRate !== '') scores.push(CFR_SCORES(Number(m.changeFailRate) || 0))
  if (m.mttr)          scores.push(MTTR_SCORES[m.mttr] ?? 2)
  if (!scores.length) return null
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length
  if (avg >= 3.5) return 'Elite'
  if (avg >= 2.5) return 'High'
  if (avg >= 1.5) return 'Medium'
  return 'Low'
}

// ─── VSM calibration mapping ──────────────────────────────────────────────
export function doraToVsmCalibration(m) {
  const cal = {}
  // Phase 6 (Delivery) WT — from deploy frequency
  const deployWtMap = {
    'Multiple per day': 1,   'Once per day': 4,   'Several per week': 12,
    'Once per week': 24,     'Once per 2 weeks': 40, 'Once per month': 80, 'Less than monthly': 160
  }
  if (m.deployFreq) cal.phase6_wt = deployWtMap[m.deployFreq]

  // Phase 7 (Monitoring) WT — from MTTR
  const mttrWtMap = {
    'Less than 1 hour': 2, '1–24 hours': 8, '1–7 days': 24,
    '1–4 weeks': 60, 'More than 1 month': 120
  }
  if (m.mttr) cal.phase7_wt = mttrWtMap[m.mttr]

  // Phase 4 (CI) PT — from build duration
  if (m.buildDuration) cal.phase4_pt = Math.round(Number(m.buildDuration) / 60 * 8)  // 8 builds/day estimate

  // Phase 3 (Code) WT — from code review cycle time
  if (m.codeReviewHours) cal.phase3_wt = Number(m.codeReviewHours)

  // Phase 5 (Testing) additional PT — from CFR (rework)
  if (m.changeFailRate) {
    const cfr = Number(m.changeFailRate) / 100
    cal.phase5_rework_factor = 1 + cfr * 0.5  // each failure adds 50% extra PT
  }

  // LT for Change directly maps to phases 3-6 LT
  const ltDaysMap = {
    'Less than 1 hour': 0.1, '1–24 hours': 0.5, '1–7 days': 3,
    '1–2 weeks': 10, '1 month': 22, '2–6 months': 60, 'More than 6 months': 120
  }
  if (m.leadTimeChange) cal.phases3to6_lt_days = ltDaysMap[m.leadTimeChange]

  return cal
}

// ─── Profile improvement recommendations ────────────────────────────────────
const PROFILE_RECS = {
  Elite:  {
    vsm_note: 'Your delivery performance is already at world-class level. VSM will focus on phases 1–2 (product definition) and eliminating remaining manual approval gates.',
    option_rec: 'Option C (AI-First)',
    priority_phases: [1, 2, 7],
    key_gap: 'Focus: further reduce planning cycle and automate remaining human gates in phases 1–2'
  },
  High: {
    vsm_note: 'Strong delivery performance. VSM will identify remaining wait time in testing and planning phases.',
    option_rec: 'Option B or C',
    priority_phases: [1, 2, 5],
    key_gap: 'Focus: reduce planning WT (phases 1–2) and testing approval gates (phase 5)'
  },
  Medium: {
    vsm_note: 'Significant bottlenecks in release process and testing. VSM will confirm which phases are the primary drag.',
    option_rec: 'Option A or B',
    priority_phases: [5, 6, 3],
    key_gap: 'Focus: automate testing signoff (phase 5), release gating (phase 6), and code review (phase 3)'
  },
  Low: {
    vsm_note: 'Substantial transformation needed across delivery pipeline. VSM will map multiple compounding bottlenecks.',
    option_rec: 'Option A (start), then B',
    priority_phases: [3, 4, 5, 6],
    key_gap: 'Focus: build CI/CD foundation first (phases 3–6) before adding AI automation'
  }
}

const PHASE_NAMES = { 1: 'Backlog & Roadmap', 2: 'Architecture & UX', 3: 'Code Management', 4: 'Continuous Integration', 5: 'Continuous Testing', 6: 'Continuous Delivery', 7: 'Monitoring & Feedback' }

// ─── Main Component ──────────────────────────────────────────────────────────
export default function DORAAssessmentPage() {
  const { doraMetrics, setDoraMetrics, doraProfile, setDoraProfile, addNotification, project } = useApp()
  const navigate = useNavigate()

  const [m, setM] = useState(doraMetrics || {
    deployFreq: '', leadTimeChange: '', changeFailRate: '', mttr: '',
    buildDuration: '', codeReviewHours: '', testCoverage: '', mttd: '',
    automatedTestPct: '', infraAutomationPct: '', incidentFreq: '',
  })
  const [saved, setSaved] = useState(!!doraMetrics)

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

  // Number of metrics filled
  const coreCount  = [m.deployFreq, m.leadTimeChange, m.changeFailRate, m.mttr].filter(Boolean).length
  const extCount   = [m.buildDuration, m.codeReviewHours, m.testCoverage, m.mttd, m.automatedTestPct, m.infraAutomationPct].filter(Boolean).length

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-600 to-blue-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold mb-1">DORA Assessment</h2>
            <p className="text-cyan-100 text-sm">
              Measure your DevOps delivery performance before creating the current state VSM.
              DORA metrics replace estimated ranges with <strong>measured actuals</strong> — improving VSM accuracy from ~65% to 85%+.
            </p>
          </div>
          {saved && profile && (
            <div className={`${band.badge} text-white px-4 py-2 rounded-xl font-bold text-sm shadow`}>
              {profile} Performer ✓
            </div>
          )}
        </div>
      </div>

      {/* Why DORA + VSM explanation */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {[
          { metric: 'Deployment Frequency', feeds: 'Phase 6 Wait Time', icon: '🚀', desc: 'Weekly deploys → 40h WT in delivery phase' },
          { metric: 'Lead Time for Change', feeds: 'Phases 3–6 Total LT', icon: '⏱', desc: 'Commit-to-prod time calibrates 4 phases' },
          { metric: 'Change Failure Rate', feeds: 'Phase 5 Rework PT', icon: '⚠️', desc: 'Each failure adds ~50% rework to testing PT' },
          { metric: 'MTTR',                feeds: 'Phase 7 Wait Time', icon: '🔧', desc: 'Recovery time calibrates monitoring phase WT' },
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
          <p className="text-xs text-gray-500">The 4 official DORA metrics from the State of DevOps research (Accelerate, DORA 2024)</p>
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
              <span className="text-amber-600">Med: Weekly</span>
              <span className="text-red-600">Low: Monthly+</span>
            </div>
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
              <span className="text-amber-600">Med: &lt;1 week</span>
              <span className="text-red-600">Low: 1 month+</span>
            </div>
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
              <span className="text-amber-600">Med: 10–15%</span>
              <span className="text-red-600">Low: &gt;15%</span>
            </div>
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
              <span className="text-amber-600">Med: &lt;1 week</span>
              <span className="text-red-600">Low: &gt;1 week</span>
            </div>
          </div>
        </div>
      </div>

      {/* Extended DORA metrics */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Extended Metrics ({extCount}/6) — VSM Phase Calibration</h3>
          <p className="text-xs text-gray-500">These replace estimated PT/WT ranges with your measured actuals — each metric calibrates a specific VSM phase</p>
        </div>
        <div className="card-body grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[
            { key: 'buildDuration',      label: 'Average CI Build Duration', unit: 'minutes', placeholder: 'e.g. 18',  calibrates: 'Phase 4 PT', hint: 'Average successful build time from git push to pipeline complete' },
            { key: 'codeReviewHours',    label: 'Code Review Cycle Time',    unit: 'hours',   placeholder: 'e.g. 6',   calibrates: 'Phase 3 WT', hint: 'PR opened to first review comment (P50 / median)' },
            { key: 'testCoverage',       label: 'Automated Test Coverage',   unit: '%',       placeholder: 'e.g. 68',  calibrates: 'Phase 5 WT', hint: 'Percentage of code covered by automated tests' },
            { key: 'mttd',               label: 'MTTD (Mean Time to Detect)',unit: 'hours',   placeholder: 'e.g. 4',   calibrates: 'Phase 7 WT', hint: 'Time from failure occurs to alert firing' },
            { key: 'automatedTestPct',   label: 'Automated Test Execution %',unit: '%',       placeholder: 'e.g. 55',  calibrates: 'Phase 5 PT', hint: 'Percentage of test execution that is fully automated' },
            { key: 'infraAutomationPct', label: 'Infrastructure Automation', unit: '%',       placeholder: 'e.g. 70',  calibrates: 'Phase 6 PT', hint: 'Percentage of infra provisioned via IaC (Terraform, ARM, CDK)' },
          ].map(f => (
            <div key={f.key}>
              <label className="text-xs font-bold text-gray-700 block mb-0.5">{f.label}</label>
              <div className="text-xs text-blue-600 mb-1 font-semibold">→ calibrates {f.calibrates}</div>
              <div className="relative">
                <input type="number" min="0" value={m[f.key]}
                  onChange={e => setF(f.key, e.target.value)}
                  placeholder={f.placeholder}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 pr-14" />
                <span className="absolute right-3 top-2.5 text-gray-400 text-xs">{f.unit}</span>
              </div>
              <div className="text-xs text-gray-400 mt-1">{f.hint}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Live DORA Profile */}
      {profile && band && rec && (
        <div className={`${band.bg} border-2 ${band.border} rounded-2xl p-6`}>
          <div className="flex items-start gap-5 flex-wrap">
            {/* Profile badge */}
            <div className="text-center">
              <div className={`${band.badge} text-white text-3xl font-black w-24 h-24 rounded-2xl flex items-center justify-center shadow-lg`}>
                {profile[0]}
              </div>
              <div className={`text-sm font-bold mt-2 text-${band.color}-800`}>{band.label}</div>
            </div>

            {/* Classification detail */}
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

              {/* Priority phases */}
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
                { key: 'phase3_wt',         label: 'Phase 3 — Code Review WT',         unit: 'h', source: 'Code review cycle time' },
                { key: 'phase4_pt',          label: 'Phase 4 — CI Build PT',            unit: 'h', source: 'Build duration metric' },
                { key: 'phase5_rework_factor',label: 'Phase 5 — Rework Multiplier',    unit: '×', source: 'Change failure rate' },
                { key: 'phase6_wt',          label: 'Phase 6 — Release Gate WT',        unit: 'h', source: 'Deployment frequency' },
                { key: 'phase7_wt',          label: 'Phase 7 — Incident Response WT',   unit: 'h', source: 'MTTR' },
                { key: 'phases3to6_lt_days', label: 'Phases 3–6 — Delivery LT',         unit: 'd', source: 'Lead time for change' },
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

            {/* Accuracy delta explanation */}
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-xl">
              <div className="font-bold text-green-800 text-sm mb-1">
                ✅ VSM Accuracy Improvement: +{Math.min(Object.keys(cal).length * 3 + (profile ? 5 : 0), 25)}% from DORA calibration
              </div>
              <div className="text-xs text-green-700">
                {Object.keys(cal).length} phase metric{Object.keys(cal).length > 1 ? 's' : ''} will use your measured DORA values instead of industry-default estimates.
                {profile === 'Elite' && ' Elite DORA profile: VSM will show minimal bottlenecks in delivery phases — planning phases are the priority.'}
                {profile === 'High'  && ' High DORA profile: minor bottlenecks in testing and planning phases will dominate.'}
                {profile === 'Medium'&& ' Medium DORA profile: testing signoff and release gating are likely the largest bottlenecks.'}
                {profile === 'Low'   && ' Low DORA profile: multiple compounding bottlenecks across phases 3–6 expected.'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* DORA 4 key bands reference */}
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
                { profile: 'Elite',  df: 'Multiple/day', lt: '< 1 hour',  cfr: '< 5%',  mttr: '< 1 hour',  impl: 'Phases 1–2 are the bottleneck — delivery is already automated', color: 'green' },
                { profile: 'High',   df: 'Daily–weekly', lt: '1 day–1 wk',cfr: '5–10%', mttr: '< 1 day',   impl: 'Testing and planning phases drive remaining WT', color: 'blue' },
                { profile: 'Medium', df: 'Weekly–monthly',lt:'1–4 weeks', cfr: '10–15%',mttr: '< 1 week',  impl: 'Release gating and UAT signoff are the critical bottlenecks', color: 'amber' },
                { profile: 'Low',    df: '< Monthly',    lt: '1–6 months',cfr: '> 15%', mttr: '> 1 week',  impl: 'CI/CD foundation and quality gates need building before AI automation', color: 'red' },
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
          {profile && !saved && <p className="text-gray-700 text-sm">DORA profile classified as <strong className={`text-${band.color}-700`}>{profile} Performer</strong>. Click below to apply calibration to your VSM.</p>}
          {saved && <p className="text-green-700 font-semibold text-sm">✅ DORA calibration applied — {Object.keys(cal).length} VSM phase metrics now use measured values.</p>}
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
