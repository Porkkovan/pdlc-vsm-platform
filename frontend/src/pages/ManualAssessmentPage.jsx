import { useState, useEffect, useRef, useCallback } from 'react'
import { useApp } from '../contexts/AppContext'
import { manualAssessmentApi } from '../services/api'
import StepReviewBar from '../components/StepReviewBar'

// ── L1-L5 maturity levels ────────────────────────────────────────────────
const LEVELS = {
  1: { label: 'Foundation (Assisted)',               color: '#ef4444', bg: 'bg-red-500',    bgLight: 'bg-red-50',    border: 'border-red-300',    text: 'text-red-700',    badge: 'bg-red-100 text-red-700 border-red-300' },
  2: { label: 'Augmentation (Co-Piloted)',           color: '#f97316', bg: 'bg-orange-500', bgLight: 'bg-orange-50', border: 'border-orange-300', text: 'text-orange-700', badge: 'bg-orange-100 text-orange-700 border-orange-300' },
  3: { label: 'Automation (Supervised-Independent)', color: '#eab308', bg: 'bg-yellow-500', bgLight: 'bg-yellow-50', border: 'border-yellow-300', text: 'text-yellow-700', badge: 'bg-yellow-100 text-yellow-700 border-yellow-300' },
  4: { label: 'Transformation (Orchestrated)',       color: '#22c55e', bg: 'bg-green-500',  bgLight: 'bg-green-50',  border: 'border-green-300',  text: 'text-green-700',  badge: 'bg-green-100 text-green-700 border-green-300' },
  5: { label: 'Reinvention (Autonomous)',            color: '#3b82f6', bg: 'bg-blue-500',   bgLight: 'bg-blue-50',   border: 'border-blue-300',   text: 'text-blue-700',   badge: 'bg-blue-100 text-blue-700 border-blue-300' },
}

function scoreToLevel(score) {
  if (score >= 4.5) return 5
  if (score >= 3.5) return 4
  if (score >= 2.5) return 3
  if (score >= 1.5) return 2
  return 1
}

// ── Small reusable components ────────────────────────────────────────────

function LevelBadge({ level, size = 'sm' }) {
  if (!level || level < 1) return <span className="border text-xs font-bold px-2 py-0.5 rounded-full bg-gray-100 text-gray-400 border-gray-200">Not Assessed</span>
  const meta = LEVELS[level] || LEVELS[1]
  const cls = size === 'lg'
    ? `border text-sm font-bold px-3 py-1 rounded-full ${meta.badge}`
    : `border text-xs font-bold px-2 py-0.5 rounded-full ${meta.badge}`
  return <span className={cls}>L{level} — {meta.label.split(' (')[0]}</span>
}

function ProgressBar({ value, max, showLabel = true }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0
  const level = scoreToLevel(max === 5 ? value : (value / max) * 5)
  const meta = LEVELS[level]
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-2.5 rounded-full transition-all duration-500 ${meta.bg}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      {showLabel && (
        <span className="text-[11px] text-gray-500 font-semibold w-12 text-right">
          {typeof value === 'number' && max === 5 ? value.toFixed(1) : `${pct}%`}
        </span>
      )}
    </div>
  )
}

// ── Score button with rubric tooltip ─────────────────────────────────────

function ScoreButton({ score, selected, rubricText, onClick }) {
  const meta = LEVELS[score]
  const isSelected = selected === score
  return (
    <div className="relative group">
      <button
        onClick={() => onClick(score)}
        className={`w-9 h-9 rounded-lg text-sm font-bold border-2 transition-all duration-150 ${
          isSelected
            ? `${meta.bg} text-white border-transparent ring-2 ring-offset-1`
            : 'bg-white text-gray-400 border-gray-200 hover:border-gray-300 hover:text-gray-600'
        }`}
        style={isSelected ? { ringColor: meta.color } : {}}
        title={`L${score}: ${rubricText || ''}`}
      >
        {score}
      </button>
      {/* Tooltip */}
      {rubricText && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 p-2.5 bg-gray-900 text-white text-[11px] leading-relaxed rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 pointer-events-none">
          <div className="font-bold mb-0.5">L{score} — {(LEVELS[score]?.label || '').split(' (')[0]}</div>
          <div className="text-gray-300">{rubricText}</div>
          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-px border-4 border-transparent border-t-gray-900" />
        </div>
      )}
    </div>
  )
}

// ── Question row ─────────────────────────────────────────────────────────

function QuestionRow({ q, response, onChange }) {
  const [showNotes, setShowNotes] = useState(!!response?.notes)
  const currentScore = response?.response || null
  const rubric = q.rubric || {}

  return (
    <div className="border border-gray-100 rounded-lg p-4 bg-white hover:border-gray-200 hover:shadow-sm transition-all">
      <div className="flex items-start gap-4">
        {/* Question text */}
        <div className="flex-1 min-w-0">
          <div className="text-sm text-gray-800 font-medium leading-snug">{q.question}</div>
          {/* Show selected rubric description */}
          {currentScore && rubric[currentScore] && (
            <div className={`mt-1.5 text-xs leading-relaxed px-2.5 py-1.5 rounded-md ${LEVELS[currentScore]?.bgLight || 'bg-gray-50'} ${LEVELS[currentScore]?.text || 'text-gray-600'}`}>
              {rubric[currentScore]}
            </div>
          )}
        </div>

        {/* Score buttons 1-5 */}
        <div className="flex gap-1.5 shrink-0">
          {[1, 2, 3, 4, 5].map(score => (
            <ScoreButton
              key={score}
              score={score}
              selected={currentScore}
              rubricText={rubric[score] || rubric[String(score)] || ''}
              onClick={val => onChange(q.id, val, response?.notes)}
            />
          ))}
        </div>
      </div>

      {/* Notes */}
      <div className="mt-2">
        {!showNotes ? (
          <button
            onClick={() => setShowNotes(true)}
            className="text-[11px] text-blue-500 hover:text-blue-700 font-medium"
          >
            + Add note
          </button>
        ) : (
          <input
            type="text"
            value={response?.notes || ''}
            onChange={e => onChange(q.id, currentScore, e.target.value)}
            placeholder="Optional notes..."
            className="w-full px-3 py-1.5 border border-gray-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-teal-400 bg-gray-50"
          />
        )}
      </div>
    </div>
  )
}

// ── Pillar accordion ─────────────────────────────────────────────────────

function PillarAccordion({ pillar, questions, responses, maturityPillar, onChange }) {
  const [open, setOpen] = useState(true)
  const pillarQs = questions.filter(q => q.pillar_id === pillar.id)
  const answered = pillarQs.filter(q => responses[q.id]?.response).length
  const total = pillarQs.length

  // Compute average score for this pillar from responses
  const scores = pillarQs.map(q => responses[q.id]?.response).filter(Boolean)
  const avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0
  const pillarLevel = maturityPillar?.level ?? (avgScore > 0 ? scoreToLevel(avgScore) : null)

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center justify-between px-5 py-3.5 bg-gray-50 border-b border-gray-200 hover:bg-gray-100 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold bg-teal-100 text-teal-700 px-2.5 py-0.5 rounded">
            {pillar.id}
          </span>
          <span className="font-bold text-gray-800 text-sm">{pillar.name}</span>
          {pillarLevel && <LevelBadge level={pillarLevel} />}
          <span className="text-[11px] text-gray-400">
            {answered}/{total} scored
          </span>
        </div>
        <div className="flex items-center gap-3">
          <div className="w-28">
            <ProgressBar value={answered} max={total} showLabel={false} />
          </div>
          <span className="text-gray-400 text-xs select-none">{open ? '▲' : '▼'}</span>
        </div>
      </button>
      {open && (
        <div className="p-4 bg-white space-y-2.5">
          {pillarQs.map(q => (
            <QuestionRow
              key={q.id}
              q={q}
              response={responses[q.id]}
              onChange={onChange}
            />
          ))}
        </div>
      )}
    </div>
  )
}

// ── Maturity summary cards ───────────────────────────────────────────────

function MaturitySummary({ maturity }) {
  if (!maturity || maturity.total_answered === 0) return null

  const overallLevel = maturity.overall_level || scoreToLevel(maturity.overall_score || 0)
  const overallMeta = LEVELS[overallLevel] || LEVELS[1]
  const pillars = maturity.pillars || maturity.phases || []

  return (
    <div className="space-y-4">
      {/* Overall summary card */}
      <div className={`card card-body border-2 ${overallMeta.border}`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs text-gray-500 font-medium mb-1">Overall Maturity</div>
            <div className="flex items-center gap-3">
              <span className={`text-3xl font-bold ${overallMeta.text}`}>
                {typeof maturity.overall_score === 'number' ? maturity.overall_score.toFixed(1) : '--'}
              </span>
              <span className="text-gray-400 text-lg">/</span>
              <span className="text-lg text-gray-400">5.0</span>
            </div>
          </div>
          <LevelBadge level={overallLevel} size="lg" />
        </div>
      </div>

      {/* Pillar cards */}
      {pillars.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {pillars.map(p => {
            const pLevel = p.level ?? scoreToLevel(p.avg_score || p.score || 0)
            const pScore = p.avg_score ?? p.score ?? 0
            const meta = LEVELS[pLevel] || LEVELS[1]
            return (
              <div key={p.pillar_id || p.phase_id || p.name} className={`card card-body border-l-4 ${meta.border}`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-gray-800 text-sm truncate">{p.pillar_name || p.phase_name || p.name}</span>
                  <LevelBadge level={pLevel} />
                </div>
                <ProgressBar value={pScore} max={5} />
                <div className="flex items-center justify-between mt-1.5">
                  <span className="text-[11px] text-gray-400">{meta.label}</span>
                  <span className={`text-xs font-bold ${meta.text}`}>{pScore.toFixed(1)} / 5</span>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ── Main page component ──────────────────────────────────────────────────

export default function ManualAssessmentPage() {
  const { project, addNotification } = useApp()

  // Data state
  const [pillars, setPillars]       = useState([])
  const [questions, setQuestions]    = useState([])
  const [responses, setResponses]   = useState({})   // { question_id: { response (1-5), notes } }
  const [maturity, setMaturity]     = useState(null)
  const [apiTeams, setApiTeams]     = useState([])    // teams from assessment data (fallback)

  // Filter state
  const [selGroup, setSelGroup]     = useState('')
  const [selProduct, setSelProduct] = useState('')
  const [selTeam, setSelTeam]       = useState('')

  // UI state
  const [saveStatus, setSaveStatus] = useState(null)  // null | 'pending' | 'saving' | 'saved'
  const [calcBusy, setCalcBusy]     = useState(false)
  const [seedBusy, setSeedBusy]     = useState(false)

  const timerRef = useRef(null)
  const responsesRef = useRef(responses)
  responsesRef.current = responses

  // ── Derived: cascading dropdown options ────────────────────────────────
  // Use project.productGroups from org setup if available, otherwise build from assessment API data

  const projectGroups = project?.productGroups || project?.product_groups || []

  const groupNames = projectGroups.length > 0
    ? projectGroups.map(g => g.name)
    : [...new Set(apiTeams.map(t => t.product_group).filter(Boolean))]

  const productsForGroup = selGroup
    ? (projectGroups.length > 0
        ? (projectGroups.find(g => g.name === selGroup)?.products || [])
        : apiTeams.filter(t => t.product_group === selGroup)
            .reduce((acc, t) => {
              if (t.product && !acc.find(p => p.name === t.product)) acc.push({ name: t.product, teams: [] })
              return acc
            }, []))
    : []

  const teamsForProduct = selProduct
    ? (projectGroups.length > 0
        ? (productsForGroup.find(p => p.name === selProduct)?.teams || [])
        : apiTeams.filter(t => t.product_group === selGroup && t.product === selProduct).map(t => t.team).filter(Boolean))
    : []

  // ── Load questions (once) ──────────────────────────────────────────────

  useEffect(() => {
    manualAssessmentApi.getQuestions()
      .then(data => {
        if (data?.pillars) setPillars(data.pillars)
        if (data?.questions) setQuestions(data.questions)
        if (Array.isArray(data)) setQuestions(data)
      })
      .catch(() => addNotification('Failed to load assessment questions', 'error'))
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Load team list from assessment data (for filter dropdowns) ─────────

  useEffect(() => {
    if (!project?.id) return
    manualAssessmentApi.listTeams(project.id)
      .then(teams => {
        const list = Array.isArray(teams) ? teams : []
        setApiTeams(list)
        if (list.length > 0 && !selTeam) {
          const first = list[0]
          if (first.product_group) setSelGroup(first.product_group)
          if (first.product) setSelProduct(first.product)
          if (first.team) setSelTeam(first.team)
        }
      })
      .catch(() => setApiTeams([]))
  }, [project?.id]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Load responses when project or team filter changes ─────────────────

  useEffect(() => {
    if (!project?.id) return
    const params = {}
    if (selTeam) params.team = selTeam
    if (selGroup) params.product_group = selGroup
    if (selProduct) params.product = selProduct

    manualAssessmentApi.getResponses(project.id, params)
      .then(r => {
        if (Array.isArray(r)) {
          const map = {}
          r.forEach(item => { map[item.question_id] = { response: parseInt(item.response) || null, notes: item.notes || '' } })
          setResponses(map)
        } else if (r && typeof r === 'object') {
          const map = {}
          Object.entries(r).forEach(([qid, val]) => {
            map[qid] = { response: parseInt(val.response) || null, notes: val.notes || '' }
          })
          setResponses(map)
        } else {
          setResponses({})
        }
      })
      .catch(() => setResponses({}))

    // Also load maturity if responses exist
    manualAssessmentApi.getMaturity(project.id, params)
      .then(setMaturity)
      .catch(() => setMaturity(null))
  }, [project?.id, selTeam, selGroup, selProduct])

  // ── Auto-save with debounce ────────────────────────────────────────────

  const flushSave = useCallback(async () => {
    if (!project?.id) return
    const payload = Object.entries(responsesRef.current)
      .filter(([, val]) => val.response)
      .map(([qid, val]) => ({
        question_id: qid,
        response: val.response,
        notes: val.notes || null,
      }))
    if (!payload.length) return

    setSaveStatus('saving')
    try {
      const ctx = {}
      if (selGroup)   ctx.product_group = selGroup
      if (selProduct) ctx.product = selProduct
      if (selTeam)    ctx.team = selTeam
      await manualAssessmentApi.saveResponses(project.id, payload, ctx)
      setSaveStatus('saved')
      setTimeout(() => setSaveStatus(null), 2500)
    } catch {
      setSaveStatus(null)
      addNotification('Failed to save responses', 'error')
    }
  }, [project?.id, selGroup, selProduct, selTeam, addNotification])

  const handleChange = useCallback((questionId, response, notes) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: { response, notes: notes ?? prev[questionId]?.notes ?? '' },
    }))
    setSaveStatus('pending')
    clearTimeout(timerRef.current)
    timerRef.current = setTimeout(flushSave, 1500)
  }, [flushSave])

  // ── Calculate maturity ─────────────────────────────────────────────────

  const calculateMaturity = async () => {
    if (!project?.id) return
    clearTimeout(timerRef.current)
    await flushSave()
    setCalcBusy(true)
    try {
      const params = {}
      if (selTeam) params.team = selTeam
      if (selGroup) params.product_group = selGroup
      if (selProduct) params.product = selProduct
      const m = await manualAssessmentApi.getMaturity(project.id, params)
      setMaturity(m)
      const lvl = m.overall_level ?? scoreToLevel(m.overall_score || 0)
      addNotification(`Assessment complete — L${lvl}: ${LEVELS[lvl]?.label || ''}`, 'success')
    } catch {
      addNotification('Failed to calculate maturity', 'error')
    } finally {
      setCalcBusy(false)
    }
  }

  // ── Seed demo data ─────────────────────────────────────────────────────

  const handleSeedDemo = async () => {
    if (!project?.id) return
    setSeedBusy(true)
    try {
      await manualAssessmentApi.seedDemo(project.id)
      addNotification('Demo data seeded successfully', 'success')
      // Refresh team list
      manualAssessmentApi.listTeams(project.id).then(t => setApiTeams(Array.isArray(t) ? t : [])).catch(() => {})
      // Reload responses
      const params = {}
      if (selTeam) params.team = selTeam
      if (selGroup) params.product_group = selGroup
      const r = await manualAssessmentApi.getResponses(project.id, params)
      if (Array.isArray(r)) {
        const map = {}
        r.forEach(item => { map[item.question_id] = { response: parseInt(item.response) || null, notes: item.notes || '' } })
        setResponses(map)
      } else if (r && typeof r === 'object') {
        const map = {}
        Object.entries(r).forEach(([qid, val]) => {
          map[qid] = { response: parseInt(val.response) || null, notes: val.notes || '' }
        })
        setResponses(map)
      } else {
        setResponses({})
      }
    } catch {
      addNotification('Failed to seed demo data', 'error')
    } finally {
      setSeedBusy(false)
    }
  }

  // ── Cascade resets ─────────────────────────────────────────────────────

  const handleGroupChange = (val) => {
    setSelGroup(val)
    setSelProduct('')
    setSelTeam('')
  }

  const handleProductChange = (val) => {
    setSelProduct(val)
    setSelTeam('')
  }

  // ── Derive unique pillars from questions if not returned by API ────────

  const effectivePillars = pillars.length > 0
    ? pillars
    : [...new Map(questions.map(q => [q.pillar_id, { id: q.pillar_id, name: q.pillar_name }])).values()]
        .sort((a, b) => (a.id > b.id ? 1 : -1))

  // ── Count stats ────────────────────────────────────────────────────────

  const totalAnswered = Object.values(responses).filter(r => r.response).length

  // ── Render ─────────────────────────────────────────────────────────────

  if (!project?.id) {
    return (
      <div className="card card-body text-center text-gray-500 py-16">
        Select or create a project to run a Pod Agentic Maturity Assessment.
      </div>
    )
  }

  return (
    <div className="space-y-6 fade-in">

      {/* ── Header ──────────────────────────────────────────────────────── */}
      <div className="bg-gradient-to-r from-teal-500 to-cyan-500 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">Pod Agentic Maturity Assessment</h2>
            <p className="text-teal-100 text-sm">
              6-pillar, 30-question self-assessment. Score each question 1-5 across the L1 Foundation to L5 Reinvention scale.
              Hover over score buttons to see rubric descriptions.
            </p>
            {/* Save status indicator */}
            <div className="mt-2 h-4">
              {saveStatus === 'saving'  && <span className="text-xs text-teal-200 animate-pulse">Saving...</span>}
              {saveStatus === 'saved'   && <span className="text-xs text-green-300 font-semibold">Saved</span>}
              {saveStatus === 'pending' && <span className="text-xs text-teal-200">Unsaved changes</span>}
            </div>
          </div>
          <div className="flex gap-2 shrink-0">
            <button
              onClick={handleSeedDemo}
              disabled={seedBusy}
              className="bg-white/20 text-white px-4 py-2.5 rounded-lg font-semibold text-sm hover:bg-white/30 border border-white/30 transition-colors"
            >
              {seedBusy ? 'Seeding...' : 'Seed Demo Data'}
            </button>
            <button
              onClick={calculateMaturity}
              disabled={calcBusy}
              className="bg-white text-teal-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-teal-50 shadow transition-colors"
            >
              {calcBusy ? 'Calculating...' : 'Calculate Maturity'}
            </button>
          </div>
        </div>
      </div>

      {/* ── Team Context Filter Bar ─────────────────────────────────────── */}
      <div className="card card-body">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="text-xs font-bold text-gray-500 uppercase tracking-wide">Scope</div>

          {/* Product Group */}
          <div className="flex flex-col gap-1">
            <label className="text-[10px] text-gray-400 font-semibold uppercase">Product Group</label>
            <select
              value={selGroup}
              onChange={e => handleGroupChange(e.target.value)}
              className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 min-w-[160px]"
            >
              <option value="">All Groups</option>
              {groupNames.map(g => <option key={g} value={g}>{g}</option>)}
            </select>
          </div>

          {/* Product */}
          <div className="flex flex-col gap-1">
            <label className="text-[10px] text-gray-400 font-semibold uppercase">Product</label>
            <select
              value={selProduct}
              onChange={e => handleProductChange(e.target.value)}
              disabled={!selGroup}
              className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 min-w-[160px] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <option value="">All Products</option>
              {productsForGroup.map(p => <option key={p.name} value={p.name}>{p.name}</option>)}
            </select>
          </div>

          {/* Team */}
          <div className="flex flex-col gap-1">
            <label className="text-[10px] text-gray-400 font-semibold uppercase">Team</label>
            <select
              value={selTeam}
              onChange={e => setSelTeam(e.target.value)}
              disabled={!selProduct}
              className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 min-w-[160px] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <option value="">All Teams</option>
              {teamsForProduct.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>

          {/* Answered count */}
          <div className="ml-auto text-right">
            <div className="text-2xl font-bold text-teal-600">{totalAnswered}<span className="text-base text-gray-400">/{questions.length}</span></div>
            <div className="text-[10px] text-gray-400">Questions Scored</div>
          </div>
        </div>
      </div>

      <StepReviewBar stepKey="manual_assessment" stepLabel="Pod Agentic Maturity Assessment" />

      {/* ── Maturity summary (after calculation) ────────────────────────── */}
      {maturity && <MaturitySummary maturity={maturity} />}

      {/* ── Pillar accordions ───────────────────────────────────────────── */}
      <div className="space-y-3">
        {effectivePillars.map(pillar => (
          <PillarAccordion
            key={pillar.id}
            pillar={pillar}
            questions={questions}
            responses={responses}
            maturityPillar={
              (maturity?.pillars || maturity?.phases || []).find(
                p => (p.pillar_id || p.phase_id) === pillar.id
              )
            }
            onChange={handleChange}
          />
        ))}
      </div>

      {/* ── Empty state ─────────────────────────────────────────────────── */}
      {questions.length === 0 && (
        <div className="text-center py-16 text-gray-400">
          <div className="text-4xl mb-3">...</div>
          <div className="font-medium">Loading assessment questions...</div>
        </div>
      )}
    </div>
  )
}
