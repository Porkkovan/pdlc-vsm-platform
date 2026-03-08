import { useState, useEffect, useCallback } from 'react'
import clsx from 'clsx'

const API = '/api/v1'

// ─── Maturity band config ────────────────────────────────────────────
const MATURITY_BANDS = {
  'Pre-Crawl': { color: 'bg-red-100 text-red-700 border-red-300',      dot: 'bg-red-500',    range: '1–2' },
  'Crawl':     { color: 'bg-orange-100 text-orange-700 border-orange-300', dot: 'bg-orange-500', range: '3–4' },
  'Walk':      { color: 'bg-yellow-100 text-yellow-700 border-yellow-300', dot: 'bg-yellow-500', range: '5–6' },
  'Run':       { color: 'bg-green-100 text-green-700 border-green-300',  dot: 'bg-green-500',  range: '7–8' },
  'Fly':       { color: 'bg-blue-100 text-blue-700 border-blue-300',    dot: 'bg-blue-500',   range: '9–10' },
}

const PRIORITY_COLORS = {
  Critical: 'bg-red-100 text-red-700',
  High:     'bg-orange-100 text-orange-700',
  Medium:   'bg-yellow-100 text-yellow-700',
  Low:      'bg-gray-100 text-gray-600',
}

const STATUS_COLORS = {
  Open:        'bg-gray-100 text-gray-700',
  'In Progress': 'bg-blue-100 text-blue-700',
  Done:        'bg-green-100 text-green-700',
  Deferred:    'bg-purple-100 text-purple-700',
}

const SOURCE_TYPES = [
  { type: 'jira',         label: 'Jira / ALM',                   icon: '🎯', placeholder: 'https://yourorg.atlassian.net/jira' },
  { type: 'github',       label: 'GitHub / GitLab / Bitbucket',  icon: '🔧', placeholder: 'https://github.com/org/repo' },
  { type: 'cicd',         label: 'CI/CD Pipeline (Jenkins/GHA)', icon: '⚙️', placeholder: 'https://jenkins.yourorg.com' },
  { type: 'sonarqube',    label: 'SonarQube / Code Quality',     icon: '🔍', placeholder: 'https://sonar.yourorg.com' },
  { type: 'release_mgmt', label: 'Release Management Portal',    icon: '🚀', placeholder: 'https://release.yourorg.com' },
  { type: 'risk_portal',  label: 'Digital Risk Assessment',      icon: '🛡️', placeholder: 'https://risk.yourorg.com' },
  { type: 'itsm',         label: 'ServiceNow / ITSM',            icon: '🎫', placeholder: 'https://yourorg.service-now.com' },
  { type: 'monitoring',   label: 'Monitoring (Dynatrace/Splunk)', icon: '📡', placeholder: 'https://monitoring.yourorg.com' },
  { type: 'confluence',   label: 'Confluence / Wiki',            icon: '📄', placeholder: 'https://yourorg.atlassian.net/wiki' },
  { type: 'oncall',       label: 'PagerDuty / OpsGenie',         icon: '🔔', placeholder: 'https://yourorg.pagerduty.com' },
]

const DIMENSIONS = ['Cultural', 'Measurement', 'Process', 'Technical']
const DIM_COLORS = {
  Cultural:    { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-700', icon: '👥' },
  Measurement: { bg: 'bg-blue-50',   border: 'border-blue-200',   text: 'text-blue-700',   icon: '📊' },
  Process:     { bg: 'bg-green-50',  border: 'border-green-200',  text: 'text-green-700',  icon: '⚙️' },
  Technical:   { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', icon: '💻' },
}

function scoreColor(score) {
  if (!score || score === 0) return 'bg-gray-100 text-gray-400'
  if (score <= 2) return 'bg-red-100 text-red-700'
  if (score <= 4) return 'bg-orange-100 text-orange-700'
  if (score <= 6) return 'bg-yellow-100 text-yellow-800'
  if (score <= 8) return 'bg-green-100 text-green-700'
  return 'bg-blue-100 text-blue-700'
}

function ScoreBadge({ score }) {
  if (!score) return <span className="text-xs text-gray-400 px-2 py-0.5 bg-gray-100 rounded">—</span>
  const band = score <= 2 ? 'Pre-Crawl' : score <= 4 ? 'Crawl' : score <= 6 ? 'Walk' : score <= 8 ? 'Run' : 'Fly'
  const cfg = MATURITY_BANDS[band]
  return (
    <span className={clsx('text-xs font-semibold px-2 py-0.5 rounded border', cfg.color)}>
      {score}/10 · {band}
    </span>
  )
}

function RadarChart({ scores }) {
  const dims = Object.keys(scores)
  if (!dims.length) return null
  const cx = 120, cy = 120, r = 90
  const points = dims.map((d, i) => {
    const angle = (i / dims.length) * 2 * Math.PI - Math.PI / 2
    const val = scores[d] || 0
    const fr = (val / 10) * r
    return { x: cx + fr * Math.cos(angle), y: cy + fr * Math.sin(angle), label: d, score: val, angle }
  })
  const gridPoints = [2, 4, 6, 8, 10].map(g =>
    dims.map((_, i) => {
      const angle = (i / dims.length) * 2 * Math.PI - Math.PI / 2
      const fr = (g / 10) * r
      return `${cx + fr * Math.cos(angle)},${cy + fr * Math.sin(angle)}`
    }).join(' ')
  )

  return (
    <svg viewBox="0 0 240 240" className="w-48 h-48 mx-auto">
      {/* Grid */}
      {gridPoints.map((pts, i) => (
        <polygon key={i} points={pts} fill="none" stroke="#e5e7eb" strokeWidth="0.5" />
      ))}
      {/* Axes */}
      {dims.map((_, i) => {
        const angle = (i / dims.length) * 2 * Math.PI - Math.PI / 2
        return <line key={i} x1={cx} y1={cy} x2={cx + r * Math.cos(angle)} y2={cy + r * Math.sin(angle)} stroke="#d1d5db" strokeWidth="0.5" />
      })}
      {/* Score polygon */}
      <polygon
        points={points.map(p => `${p.x},${p.y}`).join(' ')}
        fill="rgba(59,130,246,0.2)"
        stroke="#3b82f6"
        strokeWidth="2"
      />
      {/* Data points */}
      {points.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r="3" fill="#3b82f6" />
      ))}
      {/* Labels */}
      {dims.map((d, i) => {
        const angle = (i / dims.length) * 2 * Math.PI - Math.PI / 2
        const lx = cx + (r + 15) * Math.cos(angle)
        const ly = cy + (r + 15) * Math.sin(angle)
        return (
          <text key={i} x={lx} y={ly} textAnchor="middle" dominantBaseline="middle"
            className="text-xs" fontSize="8" fill="#374151">
            {d.slice(0, 4)}
          </text>
        )
      })}
    </svg>
  )
}

// ════════════════════════════════════════════════════════════════════
export default function DevOpsMaturityPage() {
  const [activeTab, setActiveTab] = useState('setup')   // setup | assessment | results | actions

  // Assessment state
  const [assessment, setAssessment] = useState(null)
  const [allAssessments, setAllAssessments] = useState([])
  const [questions, setQuestions] = useState({})         // {dimension: [q,...]}
  const [actionItems, setActionItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [pollTimer, setPollTimer] = useState(null)

  // Form state
  const [form, setForm] = useState({
    organization: '',
    portfolio: '',
    product_group: '',
    team_name: '',
    industry: 'Financial Services / Healthcare',
    notes: '',
  })
  const [sources, setSources] = useState([])
  const [newSource, setNewSource] = useState({ type: 'jira', url: '' })

  // Assessment UI state
  const [activeDim, setActiveDim] = useState('Cultural')
  const [localScores, setLocalScores]  = useState({})   // {qid: {manual_score, notes}}
  const [saveTimer, setSaveTimer]  = useState(null)

  // Action plan filter
  const [apFilter, setApFilter] = useState({ dim: 'All', priority: 'All', status: 'All' })
  const [editingItem, setEditingItem] = useState(null)

  // Load questions on mount
  useEffect(() => {
    fetch(`${API}/devops-maturity/questions`)
      .then(r => r.json())
      .then(d => setQuestions(d.questions_by_dimension || {}))
      .catch(() => {})

    fetch(`${API}/devops-maturity/assessments/all`)
      .then(r => r.json())
      .then(d => setAllAssessments(d || []))
      .catch(() => {})
  }, [])

  // Poll while running
  useEffect(() => {
    if (assessment?.status === 'running' && !pollTimer) {
      const t = setInterval(async () => {
        try {
          const r = await fetch(`${API}/devops-maturity/assessments/${assessment.id}`)
          const d = await r.json()
          setAssessment(d)
          if (d.status !== 'running') {
            clearInterval(t)
            setPollTimer(null)
            if (d.status === 'complete') {
              loadActionItems(d.id)
              setActiveTab('results')
            }
          }
        } catch {}
      }, 3000)
      setPollTimer(t)
    }
    return () => { if (pollTimer && assessment?.status !== 'running') clearInterval(pollTimer) }
  }, [assessment?.status])

  async function loadActionItems(id) {
    try {
      const r = await fetch(`${API}/devops-maturity/assessments/${id}/action-items`)
      const d = await r.json()
      setActionItems(d || [])
    } catch {}
  }

  function loadAssessment(a) {
    setAssessment(a)
    setForm({
      organization: a.organization || '',
      portfolio: a.portfolio || '',
      product_group: a.product_group || '',
      team_name: a.team_name || '',
      industry: a.industry || '',
      notes: a.notes || '',
    })
    setSources(a.sources || [])
    // Restore local scores from saved responses
    const saved = a.responses || {}
    const scores = {}
    Object.entries(saved).forEach(([qid, v]) => {
      scores[qid] = { manual_score: v.manual_score, notes: v.notes || '' }
    })
    setLocalScores(scores)
    loadActionItems(a.id)
  }

  // ── Setup Tab ─────────────────────────────────────────────────────

  async function handleCreateOrUpdate() {
    setLoading(true); setError(null)
    try {
      const body = { ...form, sources }
      let r
      if (assessment?.id) {
        r = await fetch(`${API}/devops-maturity/assessments/${assessment.id}`, {
          method: 'PUT', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body)
        })
      } else {
        r = await fetch(`${API}/devops-maturity/assessments`, {
          method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body)
        })
      }
      const d = await r.json()
      setAssessment(d)
      // Refresh list
      const listR = await fetch(`${API}/devops-maturity/assessments/all`)
      setAllAssessments(await listR.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleRunScoring() {
    if (!assessment?.id) return
    setLoading(true); setError(null)
    try {
      await fetch(`${API}/devops-maturity/assessments/${assessment.id}/run`, { method: 'POST' })
      setAssessment(prev => ({ ...prev, status: 'running' }))
      setActiveTab('results')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function addSource() {
    if (!newSource.url.trim()) return
    setSources(prev => [...prev, { ...newSource }])
    setNewSource({ type: 'jira', url: '' })
  }

  function removeSource(i) {
    setSources(prev => prev.filter((_, idx) => idx !== i))
  }

  // ── Assessment Tab ────────────────────────────────────────────────

  function handleScoreChange(qid, field, value) {
    setLocalScores(prev => ({
      ...prev,
      [qid]: { ...(prev[qid] || {}), [field]: field === 'manual_score' ? (value ? Number(value) : null) : value }
    }))

    // Debounced auto-save
    if (saveTimer) clearTimeout(saveTimer)
    const t = setTimeout(() => autoSaveResponses(), 2000)
    setSaveTimer(t)
  }

  async function autoSaveResponses() {
    if (!assessment?.id) return
    try {
      await fetch(`${API}/devops-maturity/assessments/${assessment.id}/responses`, {
        method: 'PATCH',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ responses: localScores })
      })
    } catch {}
  }

  function dimProgress(dim) {
    const qs = questions[dim] || []
    const scored = qs.filter(q => {
      const saved = (assessment?.responses || {})[q.id] || localScores[q.id] || {}
      const result = (assessment?.result?.scored_questions?.[dim] || []).find(s => s.question_id === q.id)
      return saved.manual_score != null || (result?.auto_score > 0)
    })
    return { scored: scored.length, total: qs.length }
  }

  function getScore(qid, dim) {
    // Priority: manual > auto
    const manual = localScores[qid]?.manual_score ?? (assessment?.responses?.[qid]?.manual_score)
    if (manual != null) return { score: manual, type: 'manual' }
    const result = (assessment?.result?.scored_questions?.[dim] || []).find(s => s.question_id === qid)
    if (result?.auto_score > 0) return { score: result.auto_score, type: 'auto', rationale: result.rationale }
    return { score: null, type: null }
  }

  // ── Results Tab ───────────────────────────────────────────────────

  const result = assessment?.result
  const summary = result?.summary
  const dimScores = summary?.dimension_scores || {}

  // ── Action Plan Tab ───────────────────────────────────────────────

  async function updateActionItem(id, changes) {
    try {
      const r = await fetch(`${API}/devops-maturity/assessments/${assessment.id}/action-items/${id}`, {
        method: 'PATCH',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(changes)
      })
      const updated = await r.json()
      setActionItems(prev => prev.map(item => item.id === id ? updated : item))
      setEditingItem(null)
    } catch {}
  }

  const filteredActions = actionItems.filter(item => {
    if (apFilter.dim !== 'All' && item.dimension !== apFilter.dim) return false
    if (apFilter.priority !== 'All' && item.priority !== apFilter.priority) return false
    if (apFilter.status !== 'All' && item.status !== apFilter.status) return false
    return true
  })

  // ── Render ────────────────────────────────────────────────────────

  return (
    <div className="space-y-4">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">DevOps Maturity Assessment</h2>
          <p className="text-sm text-gray-500 mt-0.5">73 questions · 4 dimensions · Automated scoring from connected sources</p>
        </div>
        <div className="flex gap-2">
          {allAssessments.length > 0 && (
            <select
              className="text-sm border border-gray-300 rounded px-2 py-1.5"
              value={assessment?.id || ''}
              onChange={e => {
                const a = allAssessments.find(x => x.id === e.target.value)
                if (a) loadAssessment(a)
              }}
            >
              <option value="">— Select existing assessment —</option>
              {allAssessments.map(a => (
                <option key={a.id} value={a.id}>
                  {a.team_name} / {a.product_group} ({a.status})
                </option>
              ))}
            </select>
          )}
          <button
            onClick={() => { setAssessment(null); setForm({ organization:'',portfolio:'',product_group:'',team_name:'',industry:'',notes:'' }); setSources([]); setLocalScores({}); setActionItems([]); setActiveTab('setup') }}
            className="text-sm px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50"
          >
            + New
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded px-4 py-2 text-sm">{error}</div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200 flex gap-0">
        {[
          { id: 'setup',      label: '1. Setup & Sources', icon: '⚙️' },
          { id: 'assessment', label: '2. Assessment',       icon: '📝', disabled: !assessment?.id },
          { id: 'results',    label: '3. Results & Insights', icon: '📊', disabled: !result },
          { id: 'actions',    label: '4. Action Plan',      icon: '✅', disabled: !actionItems.length },
        ].map(tab => (
          <button
            key={tab.id}
            disabled={tab.disabled}
            onClick={() => setActiveTab(tab.id)}
            className={clsx(
              'px-5 py-2.5 text-sm font-medium border-b-2 transition-colors',
              activeTab === tab.id
                ? 'border-blue-600 text-blue-600'
                : tab.disabled
                  ? 'border-transparent text-gray-300 cursor-not-allowed'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
            )}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* ══ TAB 1: SETUP ══════════════════════════════════════════════ */}
      {activeTab === 'setup' && (
        <div className="grid grid-cols-12 gap-4">
          {/* Left: Team context */}
          <div className="col-span-5 space-y-4">
            <div className="bg-white border border-gray-200 rounded-lg p-5">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <span>🏢</span> Team Context
              </h3>
              <div className="space-y-3">
                {[
                  { key: 'organization',  label: 'Organization',   placeholder: 'e.g. Humana' },
                  { key: 'portfolio',     label: 'Portfolio',      placeholder: 'e.g. Digital Health' },
                  { key: 'product_group', label: 'Product Group',  placeholder: 'e.g. Member Experience' },
                  { key: 'team_name',     label: 'Product Team',   placeholder: 'e.g. Claims Portal Team' },
                  { key: 'industry',      label: 'Industry',       placeholder: 'e.g. Healthcare / Insurance' },
                ].map(f => (
                  <div key={f.key}>
                    <label className="text-xs font-medium text-gray-600 block mb-1">{f.label}</label>
                    <input
                      value={form[f.key]}
                      onChange={e => setForm(prev => ({ ...prev, [f.key]: e.target.value }))}
                      placeholder={f.placeholder}
                      className="w-full text-sm border border-gray-300 rounded px-3 py-1.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                ))}
                <div>
                  <label className="text-xs font-medium text-gray-600 block mb-1">Assessment Notes</label>
                  <textarea
                    rows={2}
                    value={form.notes}
                    onChange={e => setForm(prev => ({ ...prev, notes: e.target.value }))}
                    placeholder="Context, scope, any pre-conditions..."
                    className="w-full text-sm border border-gray-300 rounded px-3 py-1.5 focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              <button
                onClick={handleCreateOrUpdate}
                disabled={loading || !form.organization || !form.team_name}
                className="flex-1 bg-blue-600 text-white text-sm font-semibold py-2 rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {assessment?.id ? 'Update Setup' : 'Create Assessment'}
              </button>
              {assessment?.id && (
                <button
                  onClick={() => setActiveTab('assessment')}
                  className="flex-1 bg-gray-800 text-white text-sm font-semibold py-2 rounded hover:bg-gray-900"
                >
                  Go to Assessment →
                </button>
              )}
            </div>

            {assessment?.id && (
              <button
                onClick={handleRunScoring}
                disabled={loading || assessment.status === 'running'}
                className="w-full bg-green-600 text-white text-sm font-semibold py-2 rounded hover:bg-green-700 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {assessment.status === 'running' ? (
                  <><span className="animate-spin">⟳</span> AI Scoring in Progress...</>
                ) : (
                  <><span>🤖</span> Run AI-Powered Scoring</>
                )}
              </button>
            )}
          </div>

          {/* Right: Sources */}
          <div className="col-span-7 space-y-4">
            <div className="bg-white border border-gray-200 rounded-lg p-5">
              <h3 className="font-semibold text-gray-800 mb-1 flex items-center gap-2">
                <span>🔌</span> Data Sources
              </h3>
              <p className="text-xs text-gray-500 mb-4">
                Connect your team's tools to enable automated scoring. The AI agent will analyze data from
                each source to score the 73 maturity questions.
              </p>

              {/* Add source */}
              <div className="flex gap-2 mb-4">
                <select
                  value={newSource.type}
                  onChange={e => setNewSource(prev => ({ ...prev, type: e.target.value }))}
                  className="text-sm border border-gray-300 rounded px-2 py-1.5 w-48"
                >
                  {SOURCE_TYPES.map(s => (
                    <option key={s.type} value={s.type}>{s.icon} {s.label}</option>
                  ))}
                </select>
                <input
                  value={newSource.url}
                  onChange={e => setNewSource(prev => ({ ...prev, url: e.target.value }))}
                  placeholder={SOURCE_TYPES.find(s => s.type === newSource.type)?.placeholder}
                  className="flex-1 text-sm border border-gray-300 rounded px-3 py-1.5"
                  onKeyDown={e => e.key === 'Enter' && addSource()}
                />
                <button
                  onClick={addSource}
                  className="bg-blue-600 text-white text-sm px-3 py-1.5 rounded hover:bg-blue-700"
                >+ Add</button>
              </div>

              {/* Source list */}
              {sources.length === 0 ? (
                <div className="text-center py-8 text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-lg">
                  <div className="text-2xl mb-2">🔌</div>
                  No sources configured yet.<br />
                  Add sources above for automated scoring, or score questions manually.
                </div>
              ) : (
                <div className="space-y-2">
                  {sources.map((s, i) => {
                    const cfg = SOURCE_TYPES.find(t => t.type === s.type)
                    return (
                      <div key={i} className="flex items-center gap-3 bg-gray-50 rounded px-3 py-2 border border-gray-200">
                        <span>{cfg?.icon || '🔗'}</span>
                        <div className="flex-1 min-w-0">
                          <div className="text-xs font-medium text-gray-700">{cfg?.label || s.type}</div>
                          <div className="text-xs text-gray-500 truncate">{s.url}</div>
                        </div>
                        <button onClick={() => removeSource(i)} className="text-red-400 hover:text-red-600 text-sm">✕</button>
                      </div>
                    )
                  })}
                </div>
              )}

              {/* Source guide */}
              <div className="mt-4 grid grid-cols-2 gap-1">
                {SOURCE_TYPES.map(s => (
                  <div key={s.type} className="flex items-center gap-1.5 text-xs text-gray-500">
                    <span>{s.icon}</span>
                    <span className="truncate">{s.label}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Upload docs */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                <span>📎</span> Upload Documents (Optional)
              </h4>
              <div
                className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center text-sm text-gray-500 hover:border-blue-400 cursor-pointer transition-colors"
                onDragOver={e => e.preventDefault()}
              >
                <div className="text-2xl mb-1">📄</div>
                Drop files here or click to upload<br />
                <span className="text-xs text-gray-400">Audit reports, pipeline configs, test reports, architecture docs</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ══ TAB 2: ASSESSMENT ══════════════════════════════════════════ */}
      {activeTab === 'assessment' && assessment?.id && (
        <div className="space-y-4">
          {/* Dimension tabs + progress */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-3 flex-wrap">
              {DIMENSIONS.map(dim => {
                const { scored, total } = dimProgress(dim)
                const cfg = DIM_COLORS[dim]
                const pct = total > 0 ? Math.round((scored / total) * 100) : 0
                return (
                  <button
                    key={dim}
                    onClick={() => setActiveDim(dim)}
                    className={clsx(
                      'flex items-center gap-2 px-4 py-2 rounded-lg border text-sm font-medium transition-all',
                      activeDim === dim
                        ? `${cfg.bg} ${cfg.border} ${cfg.text}`
                        : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                    )}
                  >
                    <span>{cfg.icon}</span>
                    <span>{dim}</span>
                    <span className={clsx(
                      'text-xs px-1.5 py-0.5 rounded',
                      pct === 100 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
                    )}>
                      {scored}/{total}
                    </span>
                  </button>
                )
              })}
              <div className="ml-auto flex gap-2">
                <button
                  onClick={autoSaveResponses}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  💾 Save Scores
                </button>
                <button
                  onClick={handleRunScoring}
                  disabled={assessment.status === 'running' || loading}
                  className="bg-green-600 text-white text-sm px-4 py-1.5 rounded hover:bg-green-700 disabled:opacity-50 flex items-center gap-1.5"
                >
                  {assessment.status === 'running'
                    ? <><span className="animate-spin">⟳</span> Scoring...</>
                    : <><span>🤖</span> Run AI Scoring</>
                  }
                </button>
              </div>
            </div>
          </div>

          {/* Questions for active dimension */}
          <div className="space-y-3">
            {(questions[activeDim] || []).map((q, idx) => {
              const { score, type, rationale } = getScore(q.id, activeDim)
              const localNote = localScores[q.id]?.notes || ''

              return (
                <div key={q.id} className="bg-white border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    {/* Question number */}
                    <div className={clsx(
                      'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0 mt-0.5',
                      DIM_COLORS[activeDim].bg, DIM_COLORS[activeDim].text
                    )}>
                      {q.id}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <div>
                          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                            {q.competency}
                          </span>
                          {q.weight === 3 && (
                            <span className="ml-2 text-xs bg-red-50 text-red-600 border border-red-200 px-1.5 py-0.5 rounded">High Impact</span>
                          )}
                        </div>
                        {score != null && <ScoreBadge score={score} />}
                      </div>

                      <p className="text-sm text-gray-800 mb-2">{q.question}</p>

                      {/* Scoring guide (collapsible) */}
                      <details className="mb-3">
                        <summary className="text-xs text-blue-600 cursor-pointer hover:text-blue-800">
                          View scoring criteria
                        </summary>
                        <div className="mt-2 grid grid-cols-5 gap-1 text-xs">
                          {[
                            { range: '1-2', label: 'Pre-Crawl', bg: 'bg-red-50 border-red-200' },
                            { range: '3-4', label: 'Crawl',     bg: 'bg-orange-50 border-orange-200' },
                            { range: '5-6', label: 'Walk',      bg: 'bg-yellow-50 border-yellow-200' },
                            { range: '7-8', label: 'Run',       bg: 'bg-green-50 border-green-200' },
                            { range: '9-10',label: 'Fly',       bg: 'bg-blue-50 border-blue-200' },
                          ].map(band => (
                            <div key={band.range} className={clsx('border rounded p-1.5', band.bg)}>
                              <div className="font-semibold mb-0.5">{band.range} {band.label}</div>
                              <div className="text-gray-600 leading-tight">
                                {q.scoring_criteria[band.range]?.slice(0, 120)}...
                              </div>
                            </div>
                          ))}
                        </div>
                      </details>

                      {/* Auto-score rationale */}
                      {type === 'auto' && rationale && (
                        <div className="mb-2 text-xs text-blue-700 bg-blue-50 border border-blue-200 rounded px-2 py-1.5 flex gap-1">
                          <span>🤖</span>
                          <span><strong>AI:</strong> {rationale}</span>
                        </div>
                      )}

                      {/* Manual scoring */}
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1">
                          <label className="text-xs text-gray-500">Score:</label>
                          <select
                            value={localScores[q.id]?.manual_score ?? ''}
                            onChange={e => handleScoreChange(q.id, 'manual_score', e.target.value || null)}
                            className={clsx(
                              'text-sm border rounded px-2 py-1 font-semibold',
                              score != null ? scoreColor(score) : 'border-gray-300 text-gray-600'
                            )}
                          >
                            <option value="">— Score —</option>
                            {[1,2,3,4,5,6,7,8,9,10].map(n => (
                              <option key={n} value={n}>{n} – {n <= 2 ? 'Pre-Crawl' : n <= 4 ? 'Crawl' : n <= 6 ? 'Walk' : n <= 8 ? 'Run' : 'Fly'}</option>
                            ))}
                          </select>
                          {type === 'manual' && (
                            <span className="text-xs text-gray-400">manual</span>
                          )}
                        </div>

                        {/* Data source badges */}
                        <div className="flex gap-1 flex-wrap">
                          {(q.data_sources || []).map(src => {
                            const cfg = SOURCE_TYPES.find(s => s.type === src)
                            const connected = sources.some(s => s.type === src)
                            return (
                              <span key={src} className={clsx(
                                'text-xs px-1.5 py-0.5 rounded border',
                                connected ? 'bg-green-50 text-green-700 border-green-200' : 'bg-gray-50 text-gray-400 border-gray-200'
                              )}>
                                {cfg?.icon || '🔗'} {src}
                              </span>
                            )
                          })}
                        </div>

                        {/* Notes */}
                        <input
                          value={localNote}
                          onChange={e => handleScoreChange(q.id, 'notes', e.target.value)}
                          placeholder="Notes..."
                          className="flex-1 text-xs border border-gray-200 rounded px-2 py-1"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* ══ TAB 3: RESULTS ═════════════════════════════════════════════ */}
      {activeTab === 'results' && (
        <div className="space-y-4">
          {/* Running state */}
          {assessment?.status === 'running' && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center">
              <div className="text-4xl mb-3 animate-spin">⟳</div>
              <div className="font-semibold text-blue-800">AI Scoring in Progress</div>
              <div className="text-sm text-blue-600 mt-1">
                Analyzing connected sources and scoring 73 questions across 4 dimensions...
              </div>
            </div>
          )}

          {/* Failed state */}
          {assessment?.status === 'failed' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
              <div className="text-3xl mb-2">❌</div>
              <div className="font-semibold text-red-800">Scoring Failed</div>
              <button onClick={handleRunScoring} className="mt-3 text-sm bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
                Retry Scoring
              </button>
            </div>
          )}

          {/* No result yet */}
          {assessment?.status === 'pending' && !result && (
            <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <div className="text-3xl mb-3">🤖</div>
              <div className="font-semibold text-gray-700">Run AI Scoring to see results</div>
              <div className="text-sm text-gray-500 mt-1">Or score questions manually in the Assessment tab</div>
              <button
                onClick={handleRunScoring}
                className="mt-4 bg-blue-600 text-white text-sm px-6 py-2 rounded hover:bg-blue-700"
              >
                🚀 Run Scoring Now
              </button>
            </div>
          )}

          {result && (
            <>
              {/* Overall Summary */}
              <div className="grid grid-cols-4 gap-3">
                <div className="col-span-1 bg-white border border-gray-200 rounded-lg p-4 flex flex-col items-center justify-center">
                  <RadarChart scores={Object.fromEntries(
                    Object.entries(dimScores).map(([k, v]) => [k, v.average || 0])
                  )} />
                  <div className="text-center mt-2">
                    <div className="text-3xl font-bold text-gray-800">{summary?.overall_score || 0}</div>
                    <div className="text-xs text-gray-500">/ 10 Overall</div>
                    <ScoreBadge score={summary?.overall_score} />
                  </div>
                </div>

                {Object.entries(dimScores).map(([dim, data]) => {
                  const cfg = DIM_COLORS[dim]
                  return (
                    <div key={dim} className={clsx('bg-white border rounded-lg p-4', cfg.border)}>
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-lg">{cfg.icon}</span>
                        <span className={clsx('font-semibold text-sm', cfg.text)}>{dim}</span>
                      </div>
                      <div className="text-3xl font-bold text-gray-800 mb-1">{data.average}</div>
                      <ScoreBadge score={data.average} />
                      <div className="mt-3 text-xs text-gray-500 space-y-1">
                        <div className="flex justify-between">
                          <span>Highest</span>
                          <span className="font-medium text-green-600">{data.highest}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Lowest</span>
                          <span className="font-medium text-red-600">{data.lowest}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Scored</span>
                          <span className="font-medium">{data.scored_count}/{data.total_count}</span>
                        </div>
                      </div>
                      {/* Score bar */}
                      <div className="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={clsx('h-full rounded-full', data.average >= 7 ? 'bg-green-500' : data.average >= 5 ? 'bg-yellow-500' : 'bg-red-500')}
                          style={{ width: `${(data.average / 10) * 100}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>

              {/* Strengths & Critical Gaps */}
              <div className="grid grid-cols-2 gap-4">
                {summary?.strengths?.length > 0 && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <h4 className="text-sm font-semibold text-green-800 mb-3 flex items-center gap-2">
                      <span>✅</span> Strengths (Score ≥ 8)
                    </h4>
                    <div className="space-y-1">
                      {summary.strengths.slice(0, 6).map((s, i) => (
                        <div key={i} className="flex items-center gap-2 text-sm">
                          <span className="text-green-500">●</span>
                          <span className="text-gray-700">{s.competency}</span>
                          <span className="ml-auto text-green-700 font-semibold">{s.score}/10</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {summary?.critical_gaps?.length > 0 && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <h4 className="text-sm font-semibold text-red-800 mb-3 flex items-center gap-2">
                      <span>🚨</span> Critical Gaps (Immediate Action)
                    </h4>
                    <div className="space-y-1">
                      {summary.critical_gaps.slice(0, 6).map((g, i) => (
                        <div key={i} className="flex items-center gap-2 text-sm">
                          <span className="text-red-500">●</span>
                          <span className="text-gray-700 truncate">{g.competency}</span>
                          <span className="ml-auto text-red-700 font-semibold">{g.current_score}/10</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Dimension-by-dimension inferences */}
              {DIMENSIONS.map(dim => {
                const inferences = result.inferences?.[dim] || []
                const dimScore = dimScores[dim]
                const cfg = DIM_COLORS[dim]
                if (!inferences.length) return null

                const lowInfs  = inferences.filter(i => i.level_category === 'low')
                const highInfs = inferences.filter(i => i.level_category === 'high')
                const midInfs  = inferences.filter(i => i.level_category === 'medium')

                return (
                  <div key={dim} className={clsx('bg-white border rounded-lg p-5', cfg.border)}>
                    <div className="flex items-center gap-3 mb-4">
                      <span className="text-xl">{cfg.icon}</span>
                      <div>
                        <h4 className={clsx('font-semibold', cfg.text)}>{dim} Dimension</h4>
                        <div className="flex items-center gap-2 mt-0.5">
                          <ScoreBadge score={dimScore?.average} />
                          <span className="text-xs text-gray-500">{dimScore?.scored_count} questions scored</span>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                      {/* Low scores */}
                      {lowInfs.length > 0 && (
                        <div>
                          <div className="text-xs font-semibold text-red-600 uppercase tracking-wide mb-2">
                            ⚠️ Low Areas (Scores 1–4)
                          </div>
                          <div className="space-y-2">
                            {lowInfs.map((inf, i) => (
                              <div key={i} className="bg-red-50 border border-red-100 rounded p-2 text-xs">
                                <div className="font-semibold text-red-700 mb-0.5">
                                  {inf.competency} · {inf.score}/10
                                </div>
                                <div className="text-gray-600 leading-snug">{inf.inference}</div>
                                {inf.impact === 'High' && (
                                  <div className="mt-1 text-red-600 font-medium">⚡ High business impact</div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Medium scores */}
                      {midInfs.length > 0 && (
                        <div>
                          <div className="text-xs font-semibold text-yellow-600 uppercase tracking-wide mb-2">
                            📈 Developing Areas (Scores 5–7)
                          </div>
                          <div className="space-y-2">
                            {midInfs.slice(0, 5).map((inf, i) => (
                              <div key={i} className="bg-yellow-50 border border-yellow-100 rounded p-2 text-xs">
                                <div className="font-semibold text-yellow-700 mb-0.5">
                                  {inf.competency} · {inf.score}/10
                                </div>
                                <div className="text-gray-600 leading-snug">{inf.inference}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* High scores */}
                      {highInfs.length > 0 && (
                        <div>
                          <div className="text-xs font-semibold text-green-600 uppercase tracking-wide mb-2">
                            ✅ Strong Areas (Scores 8–10)
                          </div>
                          <div className="space-y-2">
                            {highInfs.map((inf, i) => (
                              <div key={i} className="bg-green-50 border border-green-100 rounded p-2 text-xs">
                                <div className="font-semibold text-green-700 mb-0.5">
                                  {inf.competency} · {inf.score}/10
                                </div>
                                <div className="text-gray-600 leading-snug">{inf.inference}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Dimension recommendations summary */}
                    {(result.recommendations?.[dim] || []).length > 0 && (
                      <div className="mt-4 border-t border-gray-100 pt-3">
                        <div className="text-xs font-semibold text-gray-600 mb-2">Top Recommendations</div>
                        <div className="space-y-1">
                          {result.recommendations[dim].slice(0, 3).map((rec, i) => (
                            <div key={i} className="flex items-start gap-2 text-xs">
                              <span className={clsx(
                                'px-1.5 py-0.5 rounded text-xs font-medium shrink-0',
                                PRIORITY_COLORS[rec.priority]
                              )}>{rec.priority}</span>
                              <span className="text-gray-700">{rec.title}</span>
                            </div>
                          ))}
                        </div>
                        <button
                          onClick={() => setActiveTab('actions')}
                          className="mt-2 text-xs text-blue-600 hover:text-blue-800"
                        >
                          View all in Action Plan →
                        </button>
                      </div>
                    )}
                  </div>
                )
              })}
            </>
          )}
        </div>
      )}

      {/* ══ TAB 4: ACTION PLAN ═════════════════════════════════════════ */}
      {activeTab === 'actions' && (
        <div className="space-y-4">
          {/* Header + filters */}
          <div className="bg-white border border-gray-200 rounded-lg p-4 flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-4 text-sm">
              <span className="font-semibold text-gray-700">
                {actionItems.length} action items
              </span>
              <span className="text-gray-400">|</span>
              {['Critical','High','Medium','Low'].map(p => {
                const cnt = actionItems.filter(a => a.priority === p).length
                return cnt > 0 ? (
                  <span key={p} className={clsx('px-2 py-0.5 rounded text-xs font-medium', PRIORITY_COLORS[p])}>
                    {cnt} {p}
                  </span>
                ) : null
              })}
            </div>

            <div className="flex gap-2 ml-auto">
              <select
                value={apFilter.dim}
                onChange={e => setApFilter(f => ({...f, dim: e.target.value}))}
                className="text-xs border border-gray-300 rounded px-2 py-1"
              >
                <option value="All">All Dimensions</option>
                {DIMENSIONS.map(d => <option key={d} value={d}>{d}</option>)}
                <option value="Custom">Custom</option>
              </select>
              <select
                value={apFilter.priority}
                onChange={e => setApFilter(f => ({...f, priority: e.target.value}))}
                className="text-xs border border-gray-300 rounded px-2 py-1"
              >
                <option value="All">All Priorities</option>
                {['Critical','High','Medium','Low'].map(p => <option key={p} value={p}>{p}</option>)}
              </select>
              <select
                value={apFilter.status}
                onChange={e => setApFilter(f => ({...f, status: e.target.value}))}
                className="text-xs border border-gray-300 rounded px-2 py-1"
              >
                <option value="All">All Status</option>
                {['Open','In Progress','Done','Deferred'].map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
          </div>

          {/* Progress summary */}
          {actionItems.length > 0 && (
            <div className="grid grid-cols-4 gap-3">
              {['Open','In Progress','Done','Deferred'].map(s => {
                const cnt = actionItems.filter(a => a.status === s).length
                const pct = Math.round((cnt / actionItems.length) * 100)
                return (
                  <div key={s} className="bg-white border border-gray-200 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-gray-800">{cnt}</div>
                    <div className={clsx('text-xs font-medium px-2 py-0.5 rounded inline-block mt-1', STATUS_COLORS[s])}>{s}</div>
                    <div className="mt-2 h-1 bg-gray-100 rounded-full">
                      <div className="h-full bg-blue-500 rounded-full" style={{width:`${pct}%`}} />
                    </div>
                  </div>
                )
              })}
            </div>
          )}

          {/* Action items table by dimension */}
          {DIMENSIONS.concat(['Custom']).map(dim => {
            const items = filteredActions.filter(a => a.dimension === dim)
            if (!items.length) return null
            const cfg = DIM_COLORS[dim] || { bg: 'bg-gray-50', border: 'border-gray-200', text: 'text-gray-700', icon: '📋' }

            return (
              <div key={dim} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                <div className={clsx('px-4 py-2.5 flex items-center gap-2', cfg.bg, `border-b ${cfg.border}`)}>
                  <span>{cfg.icon}</span>
                  <span className={clsx('font-semibold text-sm', cfg.text)}>{dim}</span>
                  <span className="ml-auto text-xs text-gray-500">{items.length} items</span>
                </div>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50 text-xs text-gray-500">
                      <th className="text-left px-4 py-2 w-8">#</th>
                      <th className="text-left px-3 py-2">Action Item</th>
                      <th className="text-left px-3 py-2 w-24">Priority</th>
                      <th className="text-left px-3 py-2 w-28">Score Gap</th>
                      <th className="text-left px-3 py-2 w-36">Responsible</th>
                      <th className="text-left px-3 py-2 w-28">Target Date</th>
                      <th className="text-left px-3 py-2 w-28">Status</th>
                      <th className="text-left px-3 py-2 w-16">Edit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {items.map((item, idx) => (
                      editingItem?.id === item.id ? (
                        <EditableActionRow key={item.id} item={item} onSave={updateActionItem} onCancel={() => setEditingItem(null)} />
                      ) : (
                        <tr key={item.id} className="border-b border-gray-50 hover:bg-gray-50">
                          <td className="px-4 py-2.5 text-xs text-gray-400">{idx + 1}</td>
                          <td className="px-3 py-2.5">
                            <div className="font-medium text-gray-800">{item.title}</div>
                            {item.description && (
                              <div className="text-xs text-gray-500 mt-0.5 line-clamp-2">{item.description}</div>
                            )}
                            {item.notes && (
                              <div className="text-xs text-blue-600 mt-0.5 italic">Note: {item.notes}</div>
                            )}
                            {/* Suggested actions */}
                            {item.suggested_actions?.length > 0 && (
                              <details className="mt-1">
                                <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-600">
                                  {item.suggested_actions.length} suggested steps
                                </summary>
                                <ol className="mt-1 space-y-0.5 pl-3">
                                  {item.suggested_actions.map((step, si) => (
                                    <li key={si} className="text-xs text-gray-500 list-decimal">{step}</li>
                                  ))}
                                </ol>
                              </details>
                            )}
                          </td>
                          <td className="px-3 py-2.5">
                            <span className={clsx('text-xs px-2 py-0.5 rounded font-medium', PRIORITY_COLORS[item.priority])}>
                              {item.priority}
                            </span>
                            {item.effort_estimate && (
                              <div className="text-xs text-gray-400 mt-0.5">{item.effort_estimate}</div>
                            )}
                          </td>
                          <td className="px-3 py-2.5">
                            {item.current_score > 0 ? (
                              <div className="text-xs">
                                <span className={clsx('px-1 rounded font-medium', scoreColor(item.current_score))}>
                                  {item.current_level} ({item.current_score})
                                </span>
                                <span className="mx-1 text-gray-400">→</span>
                                <span className={clsx('px-1 rounded font-medium', scoreColor(item.target_score))}>
                                  {item.target_level} ({item.target_score})
                                </span>
                              </div>
                            ) : (
                              <span className="text-xs text-gray-400">—</span>
                            )}
                          </td>
                          <td className="px-3 py-2.5 text-xs text-gray-600">{item.responsible || '—'}</td>
                          <td className="px-3 py-2.5 text-xs text-gray-600">{item.target_date || '—'}</td>
                          <td className="px-3 py-2.5">
                            <select
                              value={item.status}
                              onChange={e => updateActionItem(item.id, { status: e.target.value })}
                              className={clsx(
                                'text-xs border-0 rounded px-2 py-1 font-medium cursor-pointer',
                                STATUS_COLORS[item.status]
                              )}
                            >
                              {['Open','In Progress','Done','Deferred'].map(s => (
                                <option key={s} value={s}>{s}</option>
                              ))}
                            </select>
                          </td>
                          <td className="px-3 py-2.5">
                            <button
                              onClick={() => setEditingItem(item)}
                              className="text-blue-500 hover:text-blue-700 text-xs"
                            >
                              ✏️ Edit
                            </button>
                          </td>
                        </tr>
                      )
                    ))}
                  </tbody>
                </table>
              </div>
            )
          })}

          {filteredActions.length === 0 && (
            <div className="bg-gray-50 border border-dashed border-gray-300 rounded-lg p-8 text-center text-gray-500">
              No action items match the current filters.
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ─── Editable Action Row ─────────────────────────────────────────────
function EditableActionRow({ item, onSave, onCancel }) {
  const [form, setForm] = useState({
    title:       item.title || '',
    description: item.description || '',
    responsible: item.responsible || '',
    target_date: item.target_date || '',
    status:      item.status || 'Open',
    priority:    item.priority || 'Medium',
    notes:       item.notes || '',
  })

  return (
    <tr className="bg-blue-50 border-b border-blue-100">
      <td className="px-4 py-2.5 text-xs text-gray-400">✏️</td>
      <td className="px-3 py-2.5">
        <input
          value={form.title}
          onChange={e => setForm(f => ({...f, title: e.target.value}))}
          className="w-full text-sm border border-gray-300 rounded px-2 py-1 mb-1"
          placeholder="Action title"
        />
        <textarea
          rows={2}
          value={form.description}
          onChange={e => setForm(f => ({...f, description: e.target.value}))}
          className="w-full text-xs border border-gray-300 rounded px-2 py-1 mb-1"
          placeholder="Description..."
        />
        <input
          value={form.notes}
          onChange={e => setForm(f => ({...f, notes: e.target.value}))}
          className="w-full text-xs border border-gray-300 rounded px-2 py-1"
          placeholder="Notes..."
        />
      </td>
      <td className="px-3 py-2.5">
        <select
          value={form.priority}
          onChange={e => setForm(f => ({...f, priority: e.target.value}))}
          className="text-xs border border-gray-300 rounded px-2 py-1 w-full"
        >
          {['Critical','High','Medium','Low'].map(p => <option key={p} value={p}>{p}</option>)}
        </select>
      </td>
      <td className="px-3 py-2.5 text-xs text-gray-400">unchanged</td>
      <td className="px-3 py-2.5">
        <input
          value={form.responsible}
          onChange={e => setForm(f => ({...f, responsible: e.target.value}))}
          className="w-full text-xs border border-gray-300 rounded px-2 py-1"
          placeholder="Owner/Role"
        />
      </td>
      <td className="px-3 py-2.5">
        <input
          type="date"
          value={form.target_date}
          onChange={e => setForm(f => ({...f, target_date: e.target.value}))}
          className="w-full text-xs border border-gray-300 rounded px-2 py-1"
        />
      </td>
      <td className="px-3 py-2.5">
        <select
          value={form.status}
          onChange={e => setForm(f => ({...f, status: e.target.value}))}
          className="text-xs border border-gray-300 rounded px-2 py-1 w-full"
        >
          {['Open','In Progress','Done','Deferred'].map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </td>
      <td className="px-3 py-2.5">
        <div className="flex flex-col gap-1">
          <button
            onClick={() => onSave(item.id, form)}
            className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700"
          >
            Save
          </button>
          <button onClick={onCancel} className="text-xs text-gray-500 hover:text-gray-700">Cancel</button>
        </div>
      </td>
    </tr>
  )
}
