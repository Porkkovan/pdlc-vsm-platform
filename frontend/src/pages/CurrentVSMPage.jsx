import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES, VSM_METRICS } from '../data/pdlcPhases'
import { agentsApi, manualAssessmentApi } from '../services/api'
import { Link, useNavigate } from 'react-router-dom'
import VSMVisualFlow from '../components/vsm/VSMVisualFlow'
import StepReviewBar from '../components/StepReviewBar'

const PHASE_COLORS = ['blue','purple','green','teal','sky','teal','cyan']
const BOTTLENECK_FE_THRESHOLD = 30

// Deterministic per-team variance so each team shows illustratively different metrics.
// Same team + phase always produces the same multiplier (stable across re-renders).
function teamVariance(teamName, phaseId, slot) {
  let h = (phaseId * 1009) ^ (slot * 769)
  for (let i = 0; i < teamName.length; i++) {
    h = (Math.imul(h, 37) + teamName.charCodeAt(i)) & 0x7fffffff
  }
  return 0.55 + (h % 1100) / 1000  // range: 0.55 – 1.65
}

// ── Inline team context selector ──────────────────────────────────────────────
function TeamContextPanel({ project, applyContext, applying,
  selGroup, setSelGroup, selProduct, setSelProduct, selTeam, setSelTeam }) {
  // If productGroups hierarchy is missing but flat fields exist, synthesize it
  const rawGroups = project.productGroups || []
  const productGroups = rawGroups.length > 0 ? rawGroups
    : (project.productGroup && project.product && project.team)
      ? [{ name: project.productGroup, products: [{ name: project.product, teams: [project.team] }] }]
      : []

  const groupObj    = productGroups.find(g => g.name === selGroup)
  const products    = groupObj?.products || []
  const productObj  = products.find(p => p.name === selProduct)
  const teams       = productObj?.teams || []

  const onGroupChange = (v) => { setSelGroup(v); setSelProduct(''); setSelTeam('') }
  const onProductChange = (v) => { setSelProduct(v); setSelTeam('') }

  const isCurrent = project.productGroup === selGroup &&
                    project.product === selProduct &&
                    project.team === selTeam && !!selTeam

  const handleApply = () => applyContext(selGroup, selProduct, selTeam)

  return (
    <div className="card">
      <div className="card-header bg-gradient-to-r from-indigo-600 to-blue-700 text-white rounded-t-xl">
        <div className="flex items-center justify-between gap-4 flex-wrap">
          <div>
            <h3 className="font-bold text-base">Team Context — Current State VSM</h3>
            <p className="text-indigo-100 text-xs mt-0.5">
              Select the product group, product, and team whose VSM you want to analyse.
              Metrics, bottlenecks, and AI recommendations all apply to this context.
            </p>
          </div>
          {project.team && (
            <div className="shrink-0 bg-white/20 rounded-xl px-4 py-2 text-sm text-white font-semibold text-right">
              <div className="text-xs text-indigo-200 mb-0.5">Currently analysing</div>
              <div>👥 {project.team}</div>
              {project.product      && <div className="text-xs text-indigo-200">🗂 {project.product}</div>}
              {project.productGroup && <div className="text-xs text-indigo-200">📦 {project.productGroup}</div>}
            </div>
          )}
        </div>
      </div>

      <div className="card-body">
        {!rawGroups.length ? (
          /* Free-text mode — no hierarchy set up yet, allow direct editing */
          <div className="space-y-3">
            <div className="flex items-start gap-2 bg-blue-50 border border-blue-200 rounded-lg px-3 py-2">
              <span className="text-blue-500 text-sm shrink-0">ℹ</span>
              <p className="text-xs text-blue-800">
                No organisation hierarchy configured yet. Type your team details below, or{' '}
                <Link to="/alm-connect" className="font-semibold underline hover:text-blue-900">set up a full hierarchy in ALM Connect</Link>.
              </p>
            </div>
            <div className="flex flex-wrap gap-4 items-end">
              <div className="flex-1 min-w-36">
                <label className="block text-xs font-semibold text-gray-700 mb-1">Product Group</label>
                <input value={selGroup} onChange={e => setSelGroup(e.target.value)}
                  placeholder="e.g. Digital Banking"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
              </div>
              <div className="flex-1 min-w-36">
                <label className="block text-xs font-semibold text-gray-700 mb-1">Product</label>
                <input value={selProduct} onChange={e => setSelProduct(e.target.value)}
                  placeholder="e.g. Payments"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
              </div>
              <div className="flex-1 min-w-36">
                <label className="block text-xs font-semibold text-gray-700 mb-1">Team *</label>
                <input value={selTeam} onChange={e => setSelTeam(e.target.value)}
                  placeholder="e.g. Team Alpha"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
              </div>
              <button
                onClick={handleApply}
                disabled={!selTeam || isCurrent || applying}
                className="px-5 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-40 shrink-0">
                {applying ? '⏳ Applying…' : isCurrent ? '✓ Active' : 'Apply Context'}
              </button>
            </div>
          </div>
        ) : (
          /* Dropdown mode — full hierarchy available */
          <div className="flex flex-wrap gap-4 items-end">
            <div className="flex-1 min-w-36">
              <label className="block text-xs font-semibold text-gray-700 mb-1">Product Group *</label>
              <select value={selGroup} onChange={e => onGroupChange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400">
                <option value="">— select —</option>
                {productGroups.map(g => <option key={g.name} value={g.name}>{g.name}</option>)}
              </select>
            </div>
            <div className="flex-1 min-w-36">
              <label className="block text-xs font-semibold text-gray-700 mb-1">Product *</label>
              <select value={selProduct} onChange={e => onProductChange(e.target.value)}
                disabled={!selGroup}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50">
                <option value="">— select —</option>
                {products.map(p => <option key={p.name} value={p.name}>{p.name}</option>)}
              </select>
            </div>
            <div className="flex-1 min-w-36">
              <label className="block text-xs font-semibold text-gray-700 mb-1">Team *</label>
              <select value={selTeam} onChange={e => setSelTeam(e.target.value)}
                disabled={!selProduct}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50">
                <option value="">— select —</option>
                {teams.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <button
              onClick={handleApply}
              disabled={!selGroup || !selProduct || !selTeam || isCurrent || applying}
              className="px-5 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-40 shrink-0">
              {applying ? '⏳ Applying…' : isCurrent ? '✓ Active' : 'Apply Context'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

const MATURITY_BANDS = {
  1: { label: 'L1 — Foundation',      color: 'red',    bg: 'bg-red-50',    border: 'border-red-200',    text: 'text-red-700',    badge: 'bg-red-100 text-red-800' },
  2: { label: 'L2 — Augmentation',    color: 'orange', bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', badge: 'bg-orange-100 text-orange-800' },
  3: { label: 'L3 — Automation',      color: 'yellow', bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-700', badge: 'bg-yellow-100 text-yellow-800' },
  4: { label: 'L4 — Transformation',  color: 'blue',   bg: 'bg-blue-50',   border: 'border-blue-200',   text: 'text-blue-700',   badge: 'bg-blue-100 text-blue-800' },
  5: { label: 'L5 — Reinvention',     color: 'green',  bg: 'bg-emerald-50',border: 'border-emerald-200',text: 'text-emerald-700',badge: 'bg-emerald-100 text-emerald-800' },
}

function MaturityBanner({ maturity }) {
  if (!maturity) return null
  const band = MATURITY_BANDS[maturity.overall_level] || MATURITY_BANDS[1]
  const pct = Math.round(maturity.overall_score * 100)
  return (
    <div className={`rounded-xl border-2 ${band.border} ${band.bg} p-4`}>
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-xl ${band.badge} flex items-center justify-center font-bold text-lg`}>
            L{maturity.overall_level}
          </div>
          <div>
            <div className={`font-bold text-sm ${band.text}`}>Current State Maturity: {band.label}</div>
            <div className="text-xs text-gray-500">
              {maturity.total_answered}/{maturity.total_questions} questions answered · Overall score: {pct}%
            </div>
          </div>
        </div>
        <div className="flex gap-2 flex-wrap">
          {maturity.phases?.map(ph => {
            const pb = MATURITY_BANDS[ph.level] || MATURITY_BANDS[1]
            return (
              <div key={ph.phase_id} className={`text-xs px-2 py-1 rounded-lg border ${pb.border} ${pb.bg} ${pb.text} font-semibold`}
                title={`${ph.phase_name}: L${ph.level} (${Math.round(ph.avg_score * 100)}%)`}>
                P{ph.phase_id}: L{ph.level}
              </div>
            )
          })}
        </div>
        <div className="flex gap-3">
          {maturity.dimensions?.map(d => (
            <div key={d.dimension} className="text-center">
              <div className="text-xs text-gray-400">{d.dimension}</div>
              <div className={`font-bold text-sm ${(MATURITY_BANDS[d.level] || MATURITY_BANDS[1]).text}`}>L{d.level}</div>
            </div>
          ))}
        </div>
      </div>
      {maturity.total_answered === 0 && (
        <div className="mt-2 text-xs text-gray-500 flex items-center gap-1">
          <span>ℹ</span>
          <span>No assessment responses yet — <Link to="/manual-assessment" className="text-indigo-600 font-semibold hover:underline">complete the Manual Assessment</Link> to see accurate maturity scores.</span>
        </div>
      )}
    </div>
  )
}

export default function CurrentVSMPage() {
  const { vsmData, analysisResult, setAnalysisResult, addNotification, project, saveProject,
          vsmLevel, setVsmLevel, customOverrides } = useApp()
  const [openPhase, setOpenPhase] = useState(null)
  const [running,   setRunning]   = useState(false)
  const [applying,  setApplying]  = useState(false)
  const [view,      setView]      = useState('visual') // 'visual' | 'bars' | 'phases'
  const [maturity,  setMaturity]  = useState(null)

  // Team context selection — lifted so runAnalysis can auto-apply
  const [selGroup,   setSelGroup]   = useState(project.productGroup || '')
  const [selProduct, setSelProduct] = useState(project.product      || '')
  const [selTeam,    setSelTeam]    = useState(project.team         || '')

  const navigate = useNavigate()

  // Load maturity score on mount and when project changes
  useEffect(() => {
    if (!project?.id) return
    manualAssessmentApi.getMaturity(project.id)
      .then(setMaturity)
      .catch(() => setMaturity(null))
  }, [project?.id])

  // User-story level counts only phases 3–6; all 7 are always rendered (prereqs dimmed)
  const STORY_PHASE_IDS = new Set([3, 4, 5, 6])
  const isStory = vsmLevel === 'user-story'

  const goToBottlenecks = (phaseId) => navigate(`/bottlenecks?phase=${phaseId}`)

  // Merge seeded/ALM data with default ranges, then apply user overrides from VSM Editor.
  // Override priority: customOverrides (user edits) > ALM data > team-varied defaults.
  const getPhaseMetrics = (phase) => {
    // Check for activity-level overrides from VSM Editor
    const phaseOverrides = phase.activities?.map(act => customOverrides?.[act.id]).filter(Boolean) || []
    if (phaseOverrides.length > 0) {
      const almPhase = vsmData?.phases?.find(p => (p.phaseId ?? p.id) === phase.id)
      let totalPt = 0, totalWt = 0, overriddenCount = 0
      for (const act of phase.activities) {
        const ov = customOverrides?.[act.id]
        if (ov && (ov.effort || ov.wait)) {
          totalPt += parseFloat(ov.effort) || 0
          totalWt += parseFloat(ov.wait) || 0
          overriddenCount++
        } else {
          const almAct = vsmData?.activities?.find(a => a.activityId === act.id)
          totalPt += almAct?.processTime ?? (act.defaultEffort.min + act.defaultEffort.max) / 2
          totalWt += almAct?.waitTime ?? (act.defaultWait.min + act.defaultWait.max) / 2 * 8
        }
      }
      return { processTime: totalPt, waitTime: totalWt, leadTime: (totalPt + totalWt) / 8, source: overriddenCount === phase.activities.length ? 'override' : 'override+alm' }
    }

    const almPhase = vsmData?.phases?.find(p => (p.phaseId ?? p.id) === phase.id)
    if (almPhase) {
      const pt = almPhase.processTime ?? almPhase.process_time ?? 0
      const wt = almPhase.waitTime    ?? almPhase.wait_time    ?? 0
      return { processTime: pt, waitTime: wt, leadTime: (pt + wt) / 8, source: 'alm' }
    }
    // Vary defaults by team name so each team shows illustratively different metrics
    const team = project.team || ''
    const ptBase = (phase.defaultEffortRange.min + phase.defaultEffortRange.max) / 2
    const wtBase = (phase.defaultWaitRange.min   + phase.defaultWaitRange.max)   / 2 * 8
    const pt = Math.round(ptBase * teamVariance(team, phase.id, 1) * 10) / 10
    const wt = Math.round(wtBase * teamVariance(team, phase.id, 2) * 10) / 10
    return { processTime: pt, waitTime: wt, leadTime: (pt + wt) / 8, source: 'team-varied' }
  }

  // Totals use only the phases that count for the selected level
  const totalPT = PDLC_PHASES
    .filter(p => !isStory || STORY_PHASE_IDS.has(p.id))
    .reduce((s, p) => s + getPhaseMetrics(p).processTime, 0)
  const totalWT = PDLC_PHASES
    .filter(p => !isStory || STORY_PHASE_IDS.has(p.id))
    .reduce((s, p) => s + getPhaseMetrics(p).waitTime, 0)
  const totalLT = (totalPT + totalWT) / 8
  const flowEfficiency = ((totalPT / (totalPT + totalWT)) * 100).toFixed(1)

  // All 7 phases always rendered; non-story phases marked as prereqs when in user-story mode
  const visualPhases = PDLC_PHASES.map(phase => {
    const m = getPhaseMetrics(phase)
    const isPrereq = isStory && !STORY_PHASE_IDS.has(phase.id)
    const fe = m.processTime / (m.processTime + m.waitTime) * 100
    return {
      id:           phase.id,
      name:         phase.name,
      processTime:  m.processTime,
      waitTime:     m.waitTime,
      isBottleneck: !isPrereq && fe < BOTTLENECK_FE_THRESHOLD,
      isPrereq,
    }
  })

  const applyContext = async (g, prod, t) => {
    if (!t) return
    setApplying(true)
    try {
      await saveProject({ ...project, productGroup: g, product: prod, team: t })
      addNotification(`VSM context set: ${[g, prod, t].filter(Boolean).join(' → ')}`, 'success')
    } catch {
      addNotification('Context applied (not persisted — backend offline)', 'info')
    } finally { setApplying(false) }
  }

  const runAnalysis = async () => {
    setRunning(true)
    try {
      // Auto-apply pending context before running so analysis uses the selected team
      const isPending = selTeam && (
        project.team !== selTeam ||
        project.product !== selProduct ||
        project.productGroup !== selGroup
      )
      if (isPending) await applyContext(selGroup, selProduct, selTeam)

      const result = await agentsApi.runVSMAnalyzer(project.id || 'demo')
      setAnalysisResult(result)
      addNotification('VSM analysis complete!', 'success')
    } catch {
      addNotification('Agent running in background (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  return (
    <div className="space-y-6 fade-in">

      {/* Team Context Selector */}
      <TeamContextPanel
        project={project}
        applyContext={applyContext}
        applying={applying}
        selGroup={selGroup}   setSelGroup={setSelGroup}
        selProduct={selProduct} setSelProduct={setSelProduct}
        selTeam={selTeam}     setSelTeam={setSelTeam}
      />

      {/* Header + controls */}
      <div className="bg-gradient-to-r from-violet-400 to-violet-500 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Current State Value Stream Map</h2>
            <p className="text-purple-100 text-sm">
              Baseline PDLC metrics — Process Time, Wait Time, Lead Time, Flow Efficiency
            </p>
            {project.team && (
              <div className="mt-2 flex flex-wrap gap-2 text-xs">
                {project.organization  && <span className="bg-white/20 px-2 py-0.5 rounded-full font-semibold">🏢 {project.organization}</span>}
                {project.productGroup  && <span className="bg-white/20 px-2 py-0.5 rounded-full font-semibold">📦 {project.productGroup}</span>}
                {project.product       && <span className="bg-white/20 px-2 py-0.5 rounded-full font-semibold">🗂 {project.product}</span>}
                <span className="bg-white/20 px-2 py-0.5 rounded-full font-semibold">👥 {project.team}</span>
              </div>
            )}
          </div>
          <div className="flex flex-col gap-2 items-end">
            {/* VSM Level toggle */}
            <div className="flex bg-white/20 rounded-lg overflow-hidden text-xs">
              {[
                { id: 'feature',    label: '⚡ Feature Level',     sub: '7 phases · LT ~30–50d' },
                { id: 'user-story', label: '📝 User Story Level',  sub: 'Ph 3–6 · LT ~3–10d'   },
              ].map(opt => (
                <button key={opt.id} onClick={() => setVsmLevel(opt.id)}
                  className={`px-3 py-1.5 font-semibold transition-colors text-left ${
                    vsmLevel === opt.id ? 'bg-white text-purple-700' : 'text-white hover:bg-white/10'
                  }`}>
                  <div>{opt.label}</div>
                  <div className={`text-xs font-normal ${vsmLevel === opt.id ? 'text-purple-500' : 'text-purple-200'}`}>{opt.sub}</div>
                </button>
              ))}
            </div>
            {/* View + Run */}
            <div className="flex items-center gap-3">
              <div className="flex bg-white/20 rounded-lg overflow-hidden text-sm">
                {[['visual','🗺 Visual'],['bars','📊 Bars'],['phases','📋 Phases']].map(([v,l]) => (
                  <button key={v} onClick={() => setView(v)}
                    className={`px-3 py-1.5 font-semibold text-xs transition-colors ${view===v ? 'bg-white text-purple-700' : 'text-white hover:bg-white/10'}`}>
                    {l}
                  </button>
                ))}
              </div>
              {(() => {
                const hasPending = selTeam && (
                  project.team !== selTeam || project.product !== selProduct || project.productGroup !== selGroup
                )
                return (
                  <button onClick={runAnalysis} disabled={running}
                    className={`px-4 py-2 rounded-lg font-semibold text-sm transition-colors shadow ${
                      hasPending
                        ? 'bg-cyan-400 text-cyan-900 hover:bg-cyan-300'
                        : 'bg-white text-purple-700 hover:bg-purple-50'
                    }`}
                    title={hasPending ? 'Will auto-apply selected team context before running' : undefined}>
                    {running ? '⏳ Analyzing...' : hasPending ? '🤖 Run Analysis (applies new context)' : '🤖 Run AI Analysis'}
                  </button>
                )
              })()}
            </div>
          </div>
        </div>
      </div>

      <StepReviewBar stepKey="current_vsm" stepLabel="Current State VSM" />

      {/* Current State Maturity Score */}
      <MaturityBanner maturity={maturity} />

      {/* VSM level context note */}
      {vsmLevel === 'user-story' && (
        <div className="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 text-xs text-blue-800 flex items-start gap-2">
          <span className="text-blue-500 mt-0.5 shrink-0">ℹ</span>
          <span>
            <strong>User Story Level:</strong> showing Phase 3 (Code) → Phase 6 (Delivery) only.
            Phases 1–2 (Backlog, Architecture) are planning prerequisites excluded from story cycle time.
            Switch to <strong>Feature Level</strong> to see the full 7-phase PDLC map.
          </span>
        </div>
      )}

      {/* Visual Flow diagram */}
      {view === 'visual' && (
        <VSMVisualFlow
          mode="current"
          phases={visualPhases}
          totalPT={totalPT}
          totalWT={totalWT}
          flowEfficiency={flowEfficiency}
          onPhaseClick={goToBottlenecks}
        />
      )}

      {/* KPI summary (always visible) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Process Time', value: `${Math.round(totalPT)} hrs`, sub: 'Touch time',     color: 'blue'  },
          { label: 'Total Wait Time',    value: `${Math.round(totalWT)} hrs`, sub: 'Non-value time', color: 'sky'   },
          { label: 'Total Lead Time',    value: `${totalLT.toFixed(1)} days`, sub: 'End to end',     color: 'purple'},
          { label: 'Flow Efficiency',    value: `${flowEfficiency}%`,          sub: 'PT ÷ LT',        color: 'green' }
        ].map(m => (
          <div key={m.label} className="card card-body text-center">
            <div className={`text-2xl font-bold text-${m.color}-600`}>{m.value}</div>
            <div className="text-xs text-gray-500 mt-1">{m.label}</div>
            <div className="text-xs text-gray-400">{m.sub}</div>
          </div>
        ))}
      </div>

      {/* VSM flow bar */}
      {view === 'bars' && (
      <div className="card card-body">
        <h3 className="font-bold text-gray-800 mb-1">Value Stream Flow — Process vs Wait Time</h3>
        <p className="text-xs text-gray-400 mb-4">Click a phase bar to see its bottlenecks</p>
        <div className="space-y-3">
          {PDLC_PHASES.map((phase, i) => {
            const m = getPhaseMetrics(phase)
            const total = m.processTime + m.waitTime
            const ptPct = Math.round((m.processTime / total) * 100)
            const isPrereq = isStory && !STORY_PHASE_IDS.has(phase.id)
            return (
              <div key={phase.id}
                className={`rounded-lg px-2 py-1 -mx-2 transition-colors ${isPrereq ? 'opacity-40' : 'cursor-pointer hover:bg-gray-50'}`}
                onClick={isPrereq ? undefined : () => goToBottlenecks(phase.id)}
                title={isPrereq ? 'Planning prerequisite — excluded from story cycle time' : `View bottlenecks for ${phase.name}`}
              >
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="font-semibold text-gray-700">
                    {phase.id}. {phase.name}
                    {isPrereq && <span className="ml-1.5 text-[10px] bg-gray-200 text-gray-500 px-1.5 py-0.5 rounded font-normal">prereq</span>}
                  </span>
                  <span className="text-gray-500">{isPrereq ? '— excluded' : `FE: ${ptPct}% →`}</span>
                </div>
                <div className="flex h-5 rounded-full overflow-hidden bg-gray-100">
                  <div
                    className="bg-blue-500 flex items-center justify-center text-white text-xs font-semibold"
                    style={{ width: `${ptPct}%` }}
                    title={`PT: ${m.processTime}h`}
                  >{ptPct > 10 ? 'PT' : ''}</div>
                  <div
                    className="bg-sky-400 flex items-center justify-center text-white text-xs font-semibold"
                    style={{ width: `${100-ptPct}%` }}
                    title={`WT: ${m.waitTime}h`}
                  >{(100-ptPct) > 10 ? 'WT' : ''}</div>
                </div>
                <div className="flex justify-between text-xs text-gray-400 mt-0.5">
                  <span>PT: {Math.round(m.processTime)}h</span>
                  <span>WT: {Math.round(m.waitTime)}h</span>
                </div>
              </div>
            )
          })}
        </div>
        <div className="flex gap-4 mt-4 text-xs">
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-blue-500 rounded" /><span>Process Time (value-add)</span></div>
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-sky-400 rounded" /><span>Wait Time (waste)</span></div>
        </div>
      </div>
      )}

      {/* Phase accordion */}
      {view === 'phases' && (
      <div className="space-y-3">
        {PDLC_PHASES.map((phase, i) => {
          const m = getPhaseMetrics(phase)
          const isOpen = openPhase === phase.id
          const isPrereq = isStory && !STORY_PHASE_IDS.has(phase.id)
          return (
            <div key={phase.id} className={`card overflow-hidden ${isPrereq ? 'opacity-50' : ''}`}>
              <button
                onClick={() => setOpenPhase(isOpen ? null : phase.id)}
                className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg flex items-center justify-center font-bold">
                    {phase.id}
                  </div>
                  <div className="text-left">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-800">{phase.name}</span>
                      {isPrereq && <span className="text-[10px] bg-gray-200 text-gray-500 px-1.5 py-0.5 rounded font-semibold">PREREQ — excluded from story cycle</span>}
                    </div>
                    <div className="text-xs text-gray-500">{phase.activities.length} activities · {m.source.startsWith('override') ? '✏️ User overrides' : m.source === 'alm' ? '🟢 ALM data' : '⚪ default range'}</div>
                  </div>
                </div>
                <div className="flex items-center gap-6 text-right">
                  <div><div className="text-xs text-gray-500">Process Time</div><div className="font-bold text-blue-600">{Math.round(m.processTime)}h</div></div>
                  <div><div className="text-xs text-gray-500">Wait Time</div><div className="font-bold text-sky-600">{Math.round(m.waitTime)}h</div></div>
                  <div><div className="text-xs text-gray-500">Lead Time</div><div className="font-bold text-purple-600">{m.leadTime.toFixed(1)}d</div></div>
                  <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                </div>
              </button>

              {isOpen && (
                <div className="px-6 pb-6 border-t border-gray-100 slide-down">
                  <div className="mt-4 space-y-3">
                    {phase.activities.map(act => (
                      <div key={act.id} className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-lg p-4 border border-gray-200">
                        <div className="flex items-start justify-between mb-2">
                          <div className="font-semibold text-gray-800 text-sm">{act.name}</div>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                            act.type === 'GenAI Agent' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                          }`}>{act.type}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-3 mb-3 text-xs">
                          <div><span className="text-gray-500">Effort: </span><span className="font-semibold text-blue-600">{act.defaultEffort.min}–{act.defaultEffort.max}h</span></div>
                          <div><span className="text-gray-500">Wait: </span><span className="font-semibold text-sky-600">{act.defaultWait.min}–{act.defaultWait.max} {act.waitUnit}</span></div>
                        </div>
                        <div className="bg-white rounded p-3 border border-blue-100 text-xs text-gray-700">
                          <span className="font-semibold text-blue-700">AI Opportunity: </span>{act.aiOpportunity}
                        </div>
                        <div className="mt-2 flex items-center gap-2">
                          <span className="tag-agent">{act.agent}</span>
                          {act.tools.slice(0,2).map(t => <span key={t} className="tag-tool">{t}</span>)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
      )}

      {/* Transformation Pathway — driven by analysisResult when available */}
      {(() => {
        // Build pathway from seeded analysis result (US Bank Stage 1/2/3) when available
        const fs = analysisResult?.future_states || []
        const optA = fs.find(s => s.scenario === 'option-a')
        const optB = fs.find(s => s.scenario === 'option-b')
        const optC = fs.find(s => s.scenario === 'option-c')

        // Use user-story level metrics when that level is active
        const usStory = isStory

        // Current state: use dynamically computed metrics for the active level
        const curFe = usStory ? parseFloat(flowEfficiency) : (analysisResult?.metrics?.flow_efficiency ?? null)
        const curLt = usStory ? parseFloat(totalLT.toFixed(1)) : (analysisResult?.metrics?.total_lt_days ?? null)

        // Helper: pick feature vs user-story metric
        const fe = (opt, fallback) => {
          if (!opt) return fallback
          return usStory
            ? `${opt.user_story_fe ?? (opt.flow_efficiency * 0.92).toFixed(0)}%`
            : `${opt.flow_efficiency}%`
        }
        const lt = (opt, fallback) => {
          if (!opt) return fallback
          return usStory
            ? `${opt.user_story_lt_days ?? (opt.total_lt_days * 0.43).toFixed(1)} days`
            : `${opt.total_lt_days} days`
        }

        const stages = [
          {
            label: 'Current State', badge: '0 AI tools', color: 'gray',
            desc: usStory
              ? `User story scope (phases 3–6). Manual coding, peer review queue, shared test environments, CAB approval wait. High WT-to-PT ratio in testing and delivery phases.`
              : `Manual PDLC — ${analysisResult?.bottlenecks?.length || 0} bottlenecks across 7 phases. High wait time, low flow efficiency. Tools partially deployed with inconsistent adoption.`,
            highlights: [
              `Bottlenecks: ${analysisResult?.bottlenecks?.length || 0} identified`,
              `DORA: ${analysisResult?.metrics?.dora_calibration?.deployment_frequency || 'bi-weekly'}`,
              usStory ? 'Scope: phases 3–6 (code → deploy)' : 'Scope: all 7 PDLC phases',
            ],
            fe: curFe ? `${curFe}%` : (usStory ? '~25%' : '~22%'),
            lt: curLt ? `${curLt} days` : (usStory ? '~34 days' : '~78 days'),
          },
          {
            label: optA?.label || 'Stage 1 — AI-Enabled', badge: optA ? `${optA.tools_deployed || 16} AI tools` : '16 tools', color: 'blue',
            desc: usStory
              ? `Code Review Asst. + GitHub Copilot all squads. Smart Tester + QA Suite reduce regression 18h→8h. App Vuln. auto-attaches CAB evidence. Human-led throughout.`
              : (optA?.narrative?.slice(0, 200) + (optA?.narrative?.length > 200 ? '…' : '') || 'AI tools bolted into each PDLC phase. Human-led — AI assists, never decides.'),
            highlights: optA ? [
              `${optA.tools_deployed || 16} tools across ${usStory ? 'phases 3–6' : '7 phases'}`,
              `Human model: ${optA.human_model}`,
              `Investment: ${optA.investment_range}`,
              usStory && optA.user_story_note ? optA.user_story_note.slice(0, 80) + '…' : null,
            ].filter(Boolean) : [],
            fe: fe(optA, '~36%'),
            lt: lt(optA, usStory ? '~21 days' : '~50 days'),
          },
          {
            label: optB?.label || 'Stage 2 — AI-First', badge: optB ? `${optB.agents_deployed || 21} agents` : '21 agents', color: 'purple',
            desc: usStory
              ? `Code Generator scaffolds from Figma. Code Reviewer + QA Orchestrator + Release Gate Agent compress phases 3–6 from ~21 to ~7 days. Human oversees each agent step.`
              : (optB?.narrative?.slice(0, 200) + (optB?.narrative?.length > 200 ? '…' : '') || 'Tools evolve into 21 orchestrated agents. Human: Oversee · Review · Approve.'),
            highlights: optB ? [
              `${optB.agents_deployed || 21} agents across ${usStory ? 'phases 3–6' : '7 phases'}`,
              `Human model: ${optB.human_model}`,
              `Investment: ${optB.investment_range}`,
              usStory && optB.user_story_note ? optB.user_story_note.slice(0, 80) + '…' : null,
            ].filter(Boolean) : [],
            fe: fe(optB, '~55%'),
            lt: lt(optB, usStory ? '~7 days' : '~26 days'),
          },
          {
            label: optC?.label || 'Stage 3 — AI-Native', badge: 'STUMP Platform', color: 'emerald',
            desc: usStory
              ? `STUMP Platform: Code Generator (~1h) → Build/CI (~0.3h) → AI test suite (~0.5h) → auto-deploy (~0.5h) → single human approve (~0.5h). Sub-day for non-regulated user stories.`
              : (optC?.narrative?.slice(0, 200) + (optC?.narrative?.length > 200 ? '…' : '') || 'STUMP Agentic Platform orchestrates all agents end-to-end. Human: Intent · Review · Approve only.'),
            highlights: optC ? [
              optC.platform?.name || 'STUMP Agentic Platform',
              `Human model: ${optC.human_model?.slice(0, 60)}`,
              `Investment: ${optC.investment_range}`,
              usStory ? '~3–4 hrs code→deploy (non-regulated stories)' : null,
            ].filter(Boolean) : [],
            fe: fe(optC, '~76%'),
            lt: lt(optC, usStory ? '~0.5 days' : '~8 days'),
          },
        ]

        return (
      <div className="card">
        <div className="card-header">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div>
              <h3 className="font-bold text-gray-800">
                Transformation Pathway — Current State → Stage 1 → Stage 2 → Stage 3
              </h3>
              <p className="text-xs text-gray-500">
                {analysisResult ? `${project.organization || 'Organisation'} · Source: analysis result` : 'Four stages from manual PDLC to fully autonomous ADLC'}
              </p>
            </div>
            <span className={`text-xs px-2.5 py-1 rounded-full font-bold border ${
              isStory
                ? 'bg-violet-100 text-violet-800 border-violet-300'
                : 'bg-blue-100 text-blue-800 border-blue-300'
            }`}>
              {isStory ? '📖 User Story level (phases 3–6)' : '🗂 Feature level (all 7 phases)'}
            </span>
          </div>
        </div>
        <div className="card-body grid grid-cols-1 md:grid-cols-4 gap-4">
          {stages.map((stage, i) => (
            <div key={stage.label} className={`rounded-xl border-2 p-4 ${
              stage.color === 'gray'    ? 'border-gray-200 bg-gray-50' :
              stage.color === 'blue'   ? 'border-blue-200 bg-blue-50' :
              stage.color === 'purple' ? 'border-purple-200 bg-purple-50' :
              'border-emerald-200 bg-emerald-50'
            }`}>
              <div className="flex items-center justify-between mb-2">
                <span className={`font-bold text-sm ${
                  stage.color === 'gray' ? 'text-gray-700' : stage.color === 'blue' ? 'text-blue-800' :
                  stage.color === 'purple' ? 'text-purple-800' : 'text-emerald-800'
                }`}>{stage.label}</span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full text-white ${
                  stage.color === 'gray' ? 'bg-gray-500' : stage.color === 'blue' ? 'bg-blue-600' :
                  stage.color === 'purple' ? 'bg-purple-600' : 'bg-emerald-600'
                }`}>{stage.badge}</span>
              </div>
              <p className="text-xs text-gray-600 mb-3 leading-relaxed">{stage.desc}</p>
              <div className="flex gap-3 text-xs mb-3">
                <div className="bg-white rounded-lg px-2 py-1.5 border border-gray-200 text-center flex-1">
                  <div className="text-gray-400">Flow Eff.</div>
                  <div className={`font-bold ${stage.color === 'gray' ? 'text-sky-500' : stage.color === 'emerald' ? 'text-emerald-600' : 'text-blue-600'}`}>{stage.fe}</div>
                </div>
                <div className="bg-white rounded-lg px-2 py-1.5 border border-gray-200 text-center flex-1">
                  <div className="text-gray-400">Lead Time</div>
                  <div className={`font-bold ${stage.color === 'gray' ? 'text-sky-500' : stage.color === 'emerald' ? 'text-emerald-600' : 'text-blue-600'}`}>{stage.lt}</div>
                </div>
              </div>
              {stage.highlights?.length > 0 && (
                <div className="flex flex-col gap-1 mt-2">
                  {stage.highlights.filter(Boolean).map(h => (
                    <span key={h} className="text-xs bg-white border border-gray-200 text-gray-600 px-1.5 py-0.5 rounded leading-tight">{h}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
        )
      })()}

      {/* CTA */}
      <div className="flex gap-4">
        <Link to="/bottlenecks" className="btn-primary flex-1 text-center py-3">
          ⚠️ Run Bottleneck Analysis →
        </Link>
        <Link to="/vsm-editor" className="btn-secondary flex-1 text-center py-3">
          ✏️ Edit VSM Data
        </Link>
      </div>
    </div>
  )
}
