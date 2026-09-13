import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link, useSearchParams } from 'react-router-dom'
import { DEFAULT_BOTTLENECKS } from '../data/bottleneckCatalogue'
import { BOTTLENECK_PROGRESSION } from '../data/bottleneckProgression'
import StepReviewBar from '../components/StepReviewBar'
import InlineEditModal from '../components/common/InlineEditModal'

// ── WS3: Automation Mode Classification ─────────────────────────────────────
// Classifies each SDLC activity as Manual, RPA, AI-Assisted, or AI-Agent.
// Driven by the automation classifier agent (data sources + uploaded documents + VSM metrics).
// Falls back to heuristic defaults when the agent hasn't been run.
const AUTOMATION_MODES = {
  manual:       { label: 'Manual',       color: 'bg-green-100 text-green-800 border-green-300',   dot: '🟢', description: 'Fully human-performed activity' },
  rpa:          { label: 'RPA',          color: 'bg-orange-100 text-orange-800 border-orange-300', dot: '🟠', description: 'Robotic process automation handles routine steps' },
  ai_assisted:  { label: 'AI-Assisted',  color: 'bg-blue-100 text-blue-800 border-blue-300',      dot: '🔵', description: 'AI assists human; human makes decisions' },
  ai_agent:     { label: 'AI Agent',     color: 'bg-purple-100 text-purple-800 border-purple-300', dot: '🟣', description: 'Autonomous AI agent performs the activity' },
}

// Bottleneck ID → PDLC activity ID mapping (bn-Xa → pX-aY)
const BN_TO_PDLC = {
  'bn-1a': 'p1-a3', 'bn-1b': 'p1-a5', 'bn-1c': 'p1-a1', 'bn-1d': 'p1-a2',
  'bn-2a': 'p2-a1', 'bn-2b': 'p2-a2', 'bn-2c': 'p2-a4', 'bn-2d': 'p2-a3',
  'bn-3a': 'p3-a1', 'bn-3b': 'p3-a4', 'bn-3c': 'p3-a3', 'bn-3d': 'p3-a2',
  'bn-4a': 'p4-a2', 'bn-4b': 'p4-a1', 'bn-4c': 'p4-a3', 'bn-4d': 'p4-a4',
  'bn-5a': 'p5-a6', 'bn-5b': 'p5-a8', 'bn-5c': 'p5-a2', 'bn-5d': 'p5-a4',
  'bn-5e': 'p5-a3', 'bn-5f': 'p5-a5',
  'bn-6a': 'p6-a3', 'bn-6b': 'p6-a4', 'bn-6c': 'p6-a5', 'bn-6d': 'p6-a2',
  'bn-7a': 'p7-a1', 'bn-7b': 'p7-a3', 'bn-7c': 'p7-a2', 'bn-7d': 'p7-a4',
  'bn-7e': 'p7-a1',
}

// Fallback static map when classifier hasn't run
const FALLBACK_MODE_MAP = {
  'bn-1a': 'manual', 'bn-1b': 'manual', 'bn-1c': 'manual', 'bn-1d': 'manual',
  'bn-2a': 'manual', 'bn-2b': 'manual', 'bn-2c': 'ai_assisted', 'bn-2d': 'rpa',
  'bn-3a': 'ai_assisted', 'bn-3b': 'ai_assisted', 'bn-3c': 'manual', 'bn-3d': 'rpa',
  'bn-4a': 'rpa', 'bn-4b': 'ai_assisted', 'bn-4c': 'rpa', 'bn-4d': 'rpa',
  'bn-5a': 'rpa', 'bn-5b': 'manual', 'bn-5c': 'ai_assisted', 'bn-5d': 'rpa',
  'bn-5e': 'rpa', 'bn-5f': 'ai_assisted',
  'bn-6a': 'manual', 'bn-6b': 'rpa', 'bn-6c': 'manual', 'bn-6d': 'rpa',
  'bn-7a': 'ai_assisted', 'bn-7b': 'ai_agent', 'bn-7c': 'ai_assisted',
  'bn-7d': 'manual', 'bn-7e': 'rpa',
}

const SEVERITY_STYLES = {
  Critical: { border: 'border-l-red-600',    badge: 'bg-sky-100 text-sky-800 border-sky-300',    dot: 'bg-sky-600' },
  High:     { border: 'border-l-orange-500', badge: 'bg-teal-100 text-teal-800 border-teal-300', dot: 'bg-teal-500' },
  Medium:   { border: 'border-l-yellow-500', badge: 'bg-yellow-100 text-yellow-800 border-yellow-300', dot: 'bg-yellow-500' },
  Low:      { border: 'border-l-blue-400',   badge: 'bg-blue-100 text-blue-800 border-blue-300',   dot: 'bg-blue-400' },
}

const CRITICALITY_GROUPS = [
  { severity: 'Critical', icon: '🔴', header: 'bg-sky-50 border-sky-200',     text: 'text-sky-800'    },
  { severity: 'High',     icon: '🟠', header: 'bg-teal-50 border-teal-200', text: 'text-teal-800' },
  { severity: 'Medium',   icon: '🟡', header: 'bg-yellow-50 border-yellow-200', text: 'text-yellow-800' },
  { severity: 'Low',      icon: '🔵', header: 'bg-blue-50 border-blue-200',    text: 'text-blue-800'   },
]

const WASTE_COLOURS = {
  'Waiting':           'bg-sky-50 text-sky-700 border-sky-200',
  'Over-processing':   'bg-teal-50 text-teal-700 border-teal-200',
  'Defect':            'bg-purple-50 text-purple-700 border-purple-200',
  'Effort':            'bg-yellow-50 text-yellow-700 border-yellow-200',
}

function wasteColour(wasteType) {
  if (!wasteType || typeof wasteType !== 'string') return 'bg-gray-50 text-gray-700 border-gray-200'
  for (const [key, cls] of Object.entries(WASTE_COLOURS)) {
    if (wasteType.includes(key)) return cls
  }
  return 'bg-gray-50 text-gray-700 border-gray-200'
}

// Normalize backend snake_case bottleneck to frontend camelCase format
function normalizeBn(bn) {
  if (bn.phase_id === undefined) return bn  // already frontend format
  const cap = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : s
  return {
    id: bn.id,
    phaseId: bn.phase_id,
    phaseName: bn.phase_name,
    activity: bn.activity,
    severity: cap(bn.severity),
    wasteType: bn.waste_type,
    currentPT: bn.process_time != null ? `${bn.process_time}h` : '—',
    currentWT: bn.wait_time   != null ? `${bn.wait_time}h`    : '—',
    impact: bn.root_cause || '',
    feImpact: bn.impact_score != null ? `${bn.impact_score}/10 impact` : '—',
    rootCauses: bn.root_cause ? [bn.root_cause] : [],
    contributingFactors: [],
    businessImpact: '',
    linkedImprovements: [],
    // Tool-stack progression — comes directly from backend seed data
    currentTools: bn.current_tools_involved || [],
    stageA: bn.stage_1_action || '',
    stageB: bn.stage_2_action || '',
    stageC: bn.stage_3_action || '',
  }
}

// Deterministic severity shift per team — makes each team's bottleneck profile look different
function teamBnHash(teamName, id) {
  let h = 0
  const str = teamName + id
  for (let i = 0; i < str.length; i++) h = (Math.imul(h, 37) + str.charCodeAt(i)) & 0x7fffffff
  return h
}

const SEVERITIES = ['Low', 'Medium', 'High', 'Critical']

function applyTeamVariance(bottlenecks, teamName) {
  if (!teamName) return bottlenecks
  return bottlenecks.map(bn => {
    const h = teamBnHash(teamName, bn.id)
    const idx = SEVERITIES.indexOf(bn.severity)
    const shift = (h % 5) - 2  // -2, -1, 0, +1, +2 — weighted so most stay same
    const newIdx = Math.max(0, Math.min(3, idx + (Math.abs(shift) <= 1 ? shift : 0)))
    // also vary the displayed WT metric for illustrative realism
    const wtVariants = ['0–4 hrs', '2–6 hrs', '4–8 hrs', '1–2 days', '2–3 days', '3–5 days']
    const wtIdx = (h >> 4) % wtVariants.length
    return { ...bn, severity: SEVERITIES[newIdx], currentWT: wtVariants[wtIdx] }
  })
}

function BottleneckCard({ bn, getAutomationMode, onEdit }) {
  const [expanded, setExpanded] = useState(false)
  const sty = SEVERITY_STYLES[bn.severity] || SEVERITY_STYLES.Medium

  return (
    <div className={`card border-l-4 ${sty.border}`}>
      <div className="card-body space-y-3">

        {/* Header row */}
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <div className="font-bold text-gray-800 leading-tight">{bn.activity}</div>
            <div className="text-xs text-gray-500 mt-0.5">Phase {bn.phaseId} · {bn.phaseName}</div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            {onEdit && (
              <button onClick={() => onEdit(bn)} className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold px-2 py-0.5 rounded hover:bg-indigo-50 transition-colors" title="Edit bottleneck">
                ✏️
              </button>
            )}
            <span className={`border px-2 py-0.5 rounded-full text-xs font-bold ${sty.badge}`}>
              {bn.severity}
            </span>
          </div>
        </div>

        {/* Waste type + PT/WT metrics + Automation Mode */}
        <div className="flex flex-wrap gap-2 text-xs">
          <span className={`border px-2 py-0.5 rounded font-medium ${wasteColour(bn.wasteType)}`}>
            {bn.wasteType}
          </span>
          {(() => { const am = getAutomationMode(bn.id); return (
            <span className={`border px-2 py-0.5 rounded font-bold ${am.color}`} title={am.evidence ? am.evidence.join(' · ') : am.description}>
              {am.dot} {am.label}{am.confidence != null ? ` (${Math.round(am.confidence * 100)}%)` : ''}
            </span>
          ) })()}
          <span className="bg-gray-100 text-gray-700 border border-gray-200 px-2 py-0.5 rounded">
            ⚙️ PT: {bn.currentPT}
          </span>
          <span className="bg-sky-50 text-sky-700 border border-sky-200 px-2 py-0.5 rounded">
            ⏳ WT: {bn.currentWT}
          </span>
        </div>

        {/* Impact summary */}
        <div className="bg-sky-50 rounded-lg p-3 text-xs text-sky-800 border border-sky-100 leading-relaxed">
          <span className="font-semibold">Impact: </span>{bn.impact}
        </div>

        {/* Flow efficiency badge */}
        <div className="flex items-center gap-2 text-xs">
          <span className="bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded font-medium">
            📉 Flow: {bn.feImpact}
          </span>
        </div>

        {/* Expand / collapse toggle */}
        <button
          onClick={() => setExpanded(v => !v)}
          className="w-full text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center justify-center gap-1 py-1 border-t border-gray-100 mt-1"
        >
          {expanded ? '▲ Hide root cause analysis' : '▼ Show root cause analysis & business impact'}
        </button>

        {expanded && (
          <div className="space-y-3 pt-1">

            {/* Root causes */}
            {bn.rootCauses?.length > 0 && (
            <div>
              <div className="text-xs font-bold text-gray-700 mb-2">Root Causes (5-Whys)</div>
              <ul className="space-y-1.5">
                {bn.rootCauses.map((rc, i) => (
                  <li key={i} className="flex gap-2 text-xs text-gray-700">
                    <span className="text-sky-500 font-bold shrink-0 mt-0.5">{i + 1}.</span>
                    <span>{rc}</span>
                  </li>
                ))}
              </ul>
            </div>
            )}

            {/* Contributing factors */}
            {bn.contributingFactors?.length > 0 && (
            <div>
              <div className="text-xs font-bold text-gray-700 mb-2">Contributing Factors</div>
              <div className="flex flex-wrap gap-1.5">
                {bn.contributingFactors.map((cf, i) => (
                  <span key={i} className="bg-yellow-50 text-yellow-800 border border-yellow-200 px-2 py-0.5 rounded text-xs">
                    {cf}
                  </span>
                ))}
              </div>
            </div>
            )}

            {/* Business impact */}
            <div className="bg-teal-50 rounded-lg p-3 text-xs text-teal-900 border border-teal-200">
              <div className="font-bold mb-1">Business Impact</div>
              {bn.businessImpact}
            </div>

            {/* Link to improvement */}
            {bn.linkedImprovements?.length > 0 && (
              <Link
                to={`/improvements`}
                state={{ highlightIds: bn.linkedImprovements }}
                className="flex items-center gap-1.5 text-xs text-green-700 font-semibold hover:text-green-900 bg-green-50 border border-green-200 rounded-lg px-3 py-2"
              >
                🚀 View improvement action →
              </Link>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

// ── Tool Stack Progression Components ─────────────────────────────────────────

const OPTION_COLS = [
  {
    key: 'current',
    label: 'Current State',
    sub: 'Today — Partial AI',
    bg: 'bg-slate-50',
    header: 'bg-slate-100 border-b border-slate-200',
    text: 'text-slate-700',
    badge: 'text-[10px] font-bold text-slate-400 uppercase tracking-wider',
  },
  {
    key: 'stageA',
    label: 'Option A',
    sub: '16 Tools · AI-Enabled',
    bg: 'bg-blue-50',
    header: 'bg-blue-100 border-b border-blue-200',
    text: 'text-blue-800',
    badge: 'text-[10px] font-bold text-blue-500 uppercase tracking-wider',
  },
  {
    key: 'stageB',
    label: 'Option B',
    sub: '21 Agents · AI-First',
    bg: 'bg-purple-50',
    header: 'bg-purple-100 border-b border-purple-200',
    text: 'text-purple-800',
    badge: 'text-[10px] font-bold text-purple-500 uppercase tracking-wider',
  },
  {
    key: 'stageC',
    label: 'Option C',
    sub: 'STUMP ADLC · AI-Native',
    bg: 'bg-emerald-50',
    header: 'bg-emerald-100 border-b border-emerald-200',
    text: 'text-emerald-800',
    badge: 'text-[10px] font-bold text-emerald-600 uppercase tracking-wider',
  },
]

function ProgressionCard({ bn, getAutomationMode }) {
  const prog = BOTTLENECK_PROGRESSION[bn.id] || {}
  // Inline data from backend seed takes priority over static progression map
  const currentTools = (bn.currentTools?.length ? bn.currentTools : prog.currentTools) || []
  const stageA = bn.stageA || prog.stageA || '—'
  const stageB = bn.stageB || prog.stageB || '—'
  const stageC = bn.stageC || prog.stageC || '—'
  const sty = SEVERITY_STYLES[bn.severity] || SEVERITY_STYLES.Medium

  return (
    <div className={`border border-gray-200 rounded-xl overflow-hidden border-l-4 ${sty.border}`}>
      {/* Card header */}
      <div className="bg-gray-50 px-4 py-2.5 flex flex-wrap items-center justify-between gap-2 border-b border-gray-200">
        <div>
          <div className="font-bold text-gray-800 text-sm leading-tight">{bn.activity}</div>
          <div className="text-xs text-gray-500 mt-0.5">Phase {bn.phaseId} · {bn.phaseName}</div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className={`border px-2 py-0.5 rounded-full text-xs font-bold ${sty.badge}`}>{bn.severity}</span>
          <span className={`border px-2 py-0.5 rounded text-xs font-medium ${wasteColour(bn.wasteType)}`}>{bn.wasteType}</span>
          {(() => { const am = getAutomationMode(bn.id); return (
            <span className={`border px-2 py-0.5 rounded text-xs font-bold ${am.color}`} title={am.evidence ? am.evidence.join(' · ') : am.description}>
              {am.dot} {am.label}{am.confidence != null ? ` (${Math.round(am.confidence * 100)}%)` : ''}
            </span>
          ) })()}
          <span className="text-xs text-indigo-600 bg-indigo-50 border border-indigo-200 px-2 py-0.5 rounded font-medium">
            {bn.feImpact}
          </span>
        </div>
      </div>

      {/* 4-column grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-gray-200">

        {/* Current State */}
        <div className="p-3 bg-slate-50">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Current State · Today</div>
          {currentTools.length > 0 && (
            <div className="flex flex-wrap gap-1 mb-2">
              {currentTools.map((t, i) => (
                <span key={i} className="bg-white text-slate-600 border border-slate-300 px-1.5 py-0.5 rounded text-[10px] font-medium leading-tight">{t}</span>
              ))}
            </div>
          )}
          <div className="text-xs text-sky-700 leading-snug mt-1">
            <span className="font-semibold">Bottleneck: </span>{bn.impact}
          </div>
        </div>

        {/* Option A */}
        <div className="p-3 bg-blue-50">
          <div className="text-[10px] font-bold text-blue-500 uppercase tracking-wider mb-1.5">Option A · 16 AI Tools</div>
          <div className="text-xs text-blue-800 leading-snug">{stageA}</div>
        </div>

        {/* Option B */}
        <div className="p-3 bg-purple-50">
          <div className="text-[10px] font-bold text-purple-500 uppercase tracking-wider mb-1.5">Option B · 21 Agents</div>
          <div className="text-xs text-purple-800 leading-snug">{stageB}</div>
        </div>

        {/* Option C */}
        <div className="p-3 bg-emerald-50">
          <div className="text-[10px] font-bold text-emerald-600 uppercase tracking-wider mb-1.5">Option C · STUMP ADLC</div>
          <div className="text-xs text-emerald-800 leading-snug">{stageC}</div>
        </div>

      </div>
    </div>
  )
}

function PhaseProgressionAccordion({ phase, bottlenecks, getAutomationMode }) {
  const [open, setOpen] = useState(true)
  const phaseBns = bottlenecks.filter(b => b.phaseId === phase.id)
  if (phaseBns.length === 0) return null

  const critCount = phaseBns.filter(b => b.severity === 'Critical').length
  const highCount = phaseBns.filter(b => b.severity === 'High').length

  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center justify-between px-5 py-3 bg-gray-50 border-b border-gray-200 hover:bg-gray-100 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="font-bold text-gray-800">Phase {phase.id}: {phase.name}</span>
          <div className="flex gap-1.5">
            {critCount > 0 && <span className="text-[10px] bg-sky-100 text-sky-700 border border-sky-300 rounded px-1.5 py-0.5 font-bold">{critCount} Critical</span>}
            {highCount > 0 && <span className="text-[10px] bg-teal-100 text-teal-700 border border-teal-300 rounded px-1.5 py-0.5 font-bold">{highCount} High</span>}
            <span className="text-[10px] bg-gray-100 text-gray-600 border border-gray-300 rounded px-1.5 py-0.5 font-medium">{phaseBns.length} bottleneck{phaseBns.length !== 1 ? 's' : ''}</span>
          </div>
        </div>
        <span className="text-gray-400 text-xs">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="p-4 bg-white space-y-3">
          {phaseBns.map(bn => <ProgressionCard key={bn.id} bn={bn} getAutomationMode={getAutomationMode} />)}
        </div>
      )}
    </div>
  )
}

function CriticalityAccordion({ group, bottlenecks, getAutomationMode, onEdit }) {
  const [open, setOpen] = useState(true)
  const bns = bottlenecks.filter(b => b.severity === group.severity)
  if (bns.length === 0) return null
  return (
    <div className="rounded-xl border overflow-hidden">
      <button
        onClick={() => setOpen(v => !v)}
        className={`w-full flex items-center justify-between px-5 py-3 border-b ${group.header} hover:opacity-90 transition-opacity`}
      >
        <div className="flex items-center gap-2">
          <span>{group.icon}</span>
          <span className={`font-bold text-sm ${group.text}`}>{group.severity} Bottlenecks</span>
          {/* phase breakdown */}
          <div className="flex gap-1 ml-2">
            {PDLC_PHASES.map(p => {
              const c = bns.filter(b => b.phaseId === p.id).length
              if (!c) return null
              return (
                <span key={p.id} className="text-[10px] bg-white/70 border border-gray-300 rounded px-1.5 py-0.5 text-gray-600 font-medium">
                  P{p.id}:{c}
                </span>
              )
            })}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">{bns.length} bottleneck{bns.length !== 1 ? 's' : ''}</span>
          <span className="text-gray-400 text-xs">{open ? '▲' : '▼'}</span>
        </div>
      </button>
      {open && (
        <div className="p-4 bg-white">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {bns.map(bn => <BottleneckCard key={bn.id} bn={bn} getAutomationMode={getAutomationMode} onEdit={onEdit} />)}
          </div>
        </div>
      )}
    </div>
  )
}

export default function BottlenecksPage() {
  const { analysisResult, addNotification, project } = useApp()
  const [running, setRunning] = useState(false)
  const [viewMode, setViewMode] = useState('phase')       // 'phase' | 'criticality' | 'toolstack'
  const [severityFilter, setSeverityFilter] = useState('all')
  const [phaseFilter, setPhaseFilter] = useState('all')
  const [wasteFilter, setWasteFilter] = useState('all')
  const [searchParams] = useSearchParams()

  // ── Automation classifications from the classifier agent ──────────────────
  const [autoClassifications, setAutoClassifications] = useState(null)  // null = not loaded
  const [classifyBusy, setClassifyBusy] = useState(false)
  const [classifyMeta, setClassifyMeta] = useState(null)               // {summary, method, data_sources_used, documents_used}

  // ── Inline editing ─────────────────────────────────────────────────────────
  const [editingBn, setEditingBn]   = useState(null)
  const [bnEdits, setBnEdits]       = useState({})  // { [bnId]: {field overrides} }

  const BN_EDIT_FIELDS = [
    { key: 'severity', label: 'Severity', type: 'select', options: ['Low', 'Medium', 'High', 'Critical'] },
    { key: 'wasteType', label: 'Waste Type', type: 'text' },
    { key: 'impact', label: 'Impact Description', type: 'textarea', rows: 3 },
    { key: 'currentPT', label: 'Process Time (e.g. 4h)', type: 'text' },
    { key: 'currentWT', label: 'Wait Time (e.g. 2–3 days)', type: 'text' },
    { key: 'businessImpact', label: 'Business Impact', type: 'textarea', rows: 3 },
  ]

  const saveBnEdit = (updated) => {
    setBnEdits(prev => ({ ...prev, [updated.id]: updated }))
    addNotification(`Bottleneck "${updated.activity}" updated`, 'success')
  }

  const applyBnEdits = (bns) => bns.map(bn => bnEdits[bn.id] ? { ...bn, ...bnEdits[bn.id] } : bn)

  // Load existing classifications on mount / project change
  useEffect(() => {
    if (!project?.id) return
    agentsApi.getAutomationClassifications(project.id)
      .then(result => {
        if (result?.classifications) {
          setAutoClassifications(result.classifications)
          setClassifyMeta({
            summary: result.summary,
            method: result.method,
            data_sources_used: result.data_sources_used || [],
            documents_used: result.documents_used || [],
          })
        }
      })
      .catch(() => {})  // no classifications yet — use fallback
  }, [project?.id])

  const runClassifier = async () => {
    if (!project?.id) return
    setClassifyBusy(true)
    try {
      const result = await agentsApi.classifyAutomation(project.id)
      setAutoClassifications(result.classifications)
      setClassifyMeta({
        summary: result.summary,
        method: result.method,
        data_sources_used: result.data_sources_used || [],
        documents_used: result.documents_used || [],
      })
      addNotification(
        `Automation classified: ${result.summary.manual} manual, ${result.summary.rpa} RPA, ${result.summary.ai_assisted} AI-assisted, ${result.summary.ai_agent} AI-agent (${result.method})`,
        'success'
      )
    } catch (e) {
      addNotification(e.message || 'Classification failed', 'error')
    } finally { setClassifyBusy(false) }
  }

  // Resolve automation mode for a bottleneck ID — prefers agent classification, falls back to static map
  function getAutomationMode(bnId) {
    let mode = FALLBACK_MODE_MAP[bnId] || 'manual'
    let confidence = null
    let evidence = null

    if (autoClassifications) {
      const pdlcId = BN_TO_PDLC[bnId]
      const cls = pdlcId && autoClassifications[pdlcId]
      if (cls) {
        mode = cls.mode || mode
        confidence = cls.confidence
        evidence = cls.evidence
      }
    }

    return { mode, confidence, evidence, ...AUTOMATION_MODES[mode] }
  }

  // Pre-select phase from URL query param (?phase=X) — also reset severity/waste
  useEffect(() => {
    const p = searchParams.get('phase')
    if (p) {
      setPhaseFilter(p)
      setSeverityFilter('all')
      setWasteFilter('all')
      setViewMode('phase')
    }
  }, [searchParams])

  const bottlenecks = applyBnEdits(applyTeamVariance(
    analysisResult?.bottlenecks?.map(normalizeBn) ?? DEFAULT_BOTTLENECKS,
    project.team
  ))

  const filtered = bottlenecks.filter(b =>
    (severityFilter === 'all' || b.severity === severityFilter) &&
    (phaseFilter === 'all' || b.phaseId === parseInt(phaseFilter)) &&
    (wasteFilter === 'all' || (b.wasteType && b.wasteType.includes(wasteFilter)))
  )

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runBottleneckAnalyzer(project.id || 'demo')
      addNotification('Bottleneck analysis complete!', 'success')
    } catch {
      addNotification('Running in demo mode — using built-in bottleneck catalogue', 'info')
    } finally { setRunning(false) }
  }

  // Bottlenecks scoped to the active phase (used for severity/waste filter counts in phase view)
  const phaseScoped = phaseFilter === 'all'
    ? bottlenecks
    : bottlenecks.filter(b => b.phaseId === parseInt(phaseFilter))

  // Summary stat cards ALWAYS show global totals across all phases
  const criticalCount = bottlenecks.filter(b => b.severity === 'Critical').length
  const highCount     = bottlenecks.filter(b => b.severity === 'High').length
  const waitCount     = bottlenecks.filter(b => b.wasteType?.includes('Waiting')).length
  const defectCount   = bottlenecks.filter(b => b.wasteType?.includes('Defect')).length

  // Helper: reset severity+waste and select phase
  const selectPhase = (id) => {
    setPhaseFilter(id)
    setSeverityFilter('all')
    setWasteFilter('all')
  }

  const phaseGroups = PDLC_PHASES.map(p => ({
    ...p,
    bns: bottlenecks.filter(b => b.phaseId === p.id),
    hasCritical: bottlenecks.some(b => b.phaseId === p.id && b.severity === 'Critical'),
    hasHigh:     bottlenecks.some(b => b.phaseId === p.id && b.severity === 'High'),
  }))

  return (
    <div className="space-y-6 fade-in">

      {/* Header */}
      <div className="bg-gradient-to-r from-sky-400 to-teal-400 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Bottleneck Analysis</h2>
            <p className="text-sky-100">
              Deep-dive flow blockers across all 7 PDLC phases — root causes, 5-Whys analysis,
              waste classification, and quantified business impact
            </p>
          </div>
          <button onClick={runAgent} disabled={running}
            className="bg-white text-sky-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-sky-50 shadow">
            {running ? '⏳ Analyzing...' : '🤖 Run Agent'}
          </button>
        </div>
      </div>

      <StepReviewBar stepKey="bottlenecks" stepLabel="Bottleneck Analysis" />

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Critical',       count: criticalCount, color: 'sky',    icon: '🔴' },
          { label: 'High',           count: highCount,     color: 'teal', icon: '🟠' },
          { label: 'Wait Blockers',  count: waitCount,     color: 'emerald', icon: '⏳' },
          { label: 'Defect / Rework',count: defectCount,   color: 'purple', icon: '🐛' }
        ].map(s => (
          <div key={s.label} className="card card-body text-center">
            <div className="text-2xl mb-1">{s.icon}</div>
            <div className={`text-3xl font-bold text-${s.color}-600`}>{s.count}</div>
            <div className="text-xs text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Automation Mode Legend + Classifier */}
      <div className="bg-white border border-gray-200 rounded-xl px-4 py-3">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-gray-700">Activity Automation Classification</span>
            {classifyMeta ? (
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                classifyMeta.method === 'llm_refined'
                  ? 'bg-purple-100 text-purple-700 border border-purple-300'
                  : 'bg-teal-100 text-teal-700 border border-teal-300'
              }`}>
                {classifyMeta.method === 'llm_refined' ? 'LLM-Refined' : 'Evidence-Based'}
              </span>
            ) : (
              <span className="text-[10px] font-medium text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full border border-gray-200">
                Fallback (static)
              </span>
            )}
          </div>
          <button
            onClick={runClassifier}
            disabled={classifyBusy}
            className="text-xs px-3 py-1.5 bg-violet-600 text-white rounded-lg font-semibold hover:bg-violet-700 transition-colors disabled:opacity-50"
          >
            {classifyBusy ? '⏳ Classifying...' : '🤖 Classify from Sources'}
          </button>
        </div>

        <div className="flex flex-wrap gap-3">
          {Object.entries(AUTOMATION_MODES).map(([key, m]) => {
            const count = classifyMeta?.summary?.[key]
              ?? bottlenecks.filter(b => getAutomationMode(b.id).mode === key).length
            return (
              <div key={key} className="flex items-center gap-2">
                <span className={`border px-2 py-0.5 rounded text-xs font-bold ${m.color}`}>
                  {m.dot} {m.label}
                </span>
                <span className="text-xs text-gray-500">{m.description} ({count})</span>
              </div>
            )
          })}
        </div>

        {/* Evidence sources row */}
        {classifyMeta && (
          <div className="mt-2 pt-2 border-t border-gray-100 flex flex-wrap gap-2 text-[10px]">
            {classifyMeta.data_sources_used?.length > 0 && (
              <span className="text-violet-600 bg-violet-50 border border-violet-200 px-2 py-0.5 rounded">
                🔗 {classifyMeta.data_sources_used.length} data source{classifyMeta.data_sources_used.length !== 1 ? 's' : ''}:
                {' '}{classifyMeta.data_sources_used.map(s => s.label || s.type).join(', ')}
              </span>
            )}
            {classifyMeta.documents_used?.length > 0 && (
              <span className="text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded">
                📎 {classifyMeta.documents_used.length} document{classifyMeta.documents_used.length !== 1 ? 's' : ''}:
                {' '}{classifyMeta.documents_used.filter(d => d.has_text).length} with extracted text
              </span>
            )}
            {classifyMeta.data_sources_used?.length === 0 && classifyMeta.documents_used?.length === 0 && (
              <span className="text-amber-600 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
                ⚠️ No data sources or documents configured — classification uses baseline heuristics.
                Add sources in ALM Connect for evidence-based results.
              </span>
            )}
          </div>
        )}
      </div>

      {/* Phase Heatmap */}
      <div className="card">
        <div className="card-header">
          <h3 className="font-bold text-gray-800">Phase Bottleneck Heatmap</h3>
          <p className="text-xs text-gray-500 mt-0.5">Click a phase to filter</p>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-7 gap-2">
            {phaseGroups.map(phase => (
              <button
                key={phase.id}
                onClick={() => {
                  setViewMode('phase')
                  phaseFilter === String(phase.id) ? selectPhase('all') : selectPhase(String(phase.id))
                }}
                className={`text-center p-3 rounded-lg border-2 transition-all ${
                  phaseFilter === String(phase.id) ? 'ring-2 ring-blue-400' : ''
                } ${
                  phase.hasCritical ? 'bg-sky-100 border-sky-400' :
                  phase.hasHigh     ? 'bg-teal-100 border-teal-300' :
                  phase.bns.length  ? 'bg-yellow-50 border-yellow-300' :
                                      'bg-green-50 border-green-200'
                }`}
              >
                <div className="text-xl font-bold">{phase.bns.length > 0 ? '⚠️' : '✅'}</div>
                <div className="text-sm font-bold text-gray-700 mt-1">{phase.bns.length}</div>
                <div className="text-xs text-gray-500 leading-tight mt-1">{phase.name.split(' ').slice(0,2).join(' ')}</div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* View toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-gray-500">View by:</span>
        <button
          onClick={() => setViewMode('phase')}
          className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            viewMode === 'phase' ? 'bg-blue-600 text-white shadow' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          📋 PDLC Phase
        </button>
        <button
          onClick={() => { setViewMode('criticality'); setPhaseFilter('all'); setSeverityFilter('all'); setWasteFilter('all') }}
          className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            viewMode === 'criticality' ? 'bg-sky-600 text-white shadow' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          🔴 Criticality
        </button>
        <button
          onClick={() => { setViewMode('toolstack'); setPhaseFilter('all'); setSeverityFilter('all'); setWasteFilter('all') }}
          className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            viewMode === 'toolstack' ? 'bg-indigo-600 text-white shadow' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          🔀 Tool Stack Progression
        </button>
      </div>

      {/* ── PDLC Phase View: original filters + cards ── */}
      {viewMode === 'phase' && (
        <>
          {/* Filters */}
          <div className="bg-white p-4 rounded-xl border border-gray-200 space-y-3">
            {/* PDLC Phase filter */}
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 mr-1">PDLC Phase:</span>
              <button
                onClick={() => selectPhase('all')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                  phaseFilter === 'all' ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}>
                All Phases
              </button>
              {PDLC_PHASES.map(p => {
                const count = bottlenecks.filter(b => b.phaseId === p.id).length
                const hasCrit = bottlenecks.some(b => b.phaseId === p.id && b.severity === 'Critical')
                const hasHigh = bottlenecks.some(b => b.phaseId === p.id && b.severity === 'High')
                const isActive = phaseFilter === String(p.id)
                return (
                  <button
                    key={p.id}
                    onClick={() => isActive ? selectPhase('all') : selectPhase(String(p.id))}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 ${
                      isActive
                        ? 'bg-blue-600 text-white'
                        : count === 0
                          ? 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100'
                          : hasCrit
                            ? 'bg-sky-50 text-sky-700 border border-sky-300 hover:bg-sky-100'
                            : hasHigh
                              ? 'bg-teal-50 text-teal-700 border border-teal-300 hover:bg-teal-100'
                              : 'bg-yellow-50 text-yellow-700 border border-yellow-300 hover:bg-yellow-100'
                    }`}>
                    <span>P{p.id} {p.name.split(' ')[0]}</span>
                    {count > 0 && (
                      <span className={`rounded-full px-1.5 text-[10px] font-bold ${
                        isActive ? 'bg-white/30' : hasCrit ? 'bg-sky-200' : hasHigh ? 'bg-teal-200' : 'bg-yellow-200'
                      }`}>{count}</span>
                    )}
                  </button>
                )
              })}
            </div>

            {/* Severity filter */}
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 mr-1">Severity:</span>
              {['all','Critical','High','Medium','Low'].map(f => (
                <button key={f} onClick={() => setSeverityFilter(f)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                    severityFilter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}>
                  {f === 'all'
                    ? `All (${phaseScoped.length})`
                    : `${f} (${phaseScoped.filter(b => b.severity === f).length})`}
                </button>
              ))}
            </div>

            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 mr-1">Waste type:</span>
              {['all','Waiting','Over-processing','Defect'].map(w => (
                <button key={w} onClick={() => setWasteFilter(w)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                    wasteFilter === w ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}>
                  {w === 'all'
                    ? `All types (${phaseScoped.length})`
                    : `${w} (${phaseScoped.filter(b => b.wasteType?.includes(w)).length})`}
                </button>
              ))}
              <span className="text-xs text-gray-400 ml-auto">
                {filtered.length} of {phaseScoped.length}{phaseFilter !== 'all' ? ' in phase' : ''} shown
              </span>
            </div>
          </div>

          {/* Phase activity breakdown — shown when a phase is selected */}
          {phaseFilter !== 'all' && (() => {
            const phase = PDLC_PHASES.find(p => p.id === parseInt(phaseFilter))
            const phaseBns = filtered
            if (!phase) return null
            return (
              <div className="bg-white rounded-xl border border-blue-200 overflow-hidden">
                <div className="bg-blue-50 px-5 py-3 border-b border-blue-100 flex items-center justify-between">
                  <div>
                    <span className="font-bold text-blue-800">Phase {phase.id}: {phase.name}</span>
                    <span className="ml-3 text-xs text-blue-600">{phase.activities.length} activities · {phaseBns.length} bottleneck{phaseBns.length !== 1 ? 's' : ''} shown</span>
                  </div>
                  <button onClick={() => selectPhase('all')} className="text-xs text-blue-500 hover:text-blue-700">✕ Clear</button>
                </div>
                <div className="px-5 py-3">
                  <div className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Activities in this phase</div>
                  <div className="flex flex-wrap gap-2">
                    {phase.activities.map(act => {
                      const hasBn = bottlenecks.some(b => b.phaseId === phase.id && b.activity === act.name)
                      return (
                        <span key={act.id} className={`text-xs px-2.5 py-1 rounded-full border font-medium ${
                          hasBn
                            ? 'bg-sky-50 text-sky-700 border-sky-300'
                            : 'bg-gray-50 text-gray-600 border-gray-200'
                        }`}>
                          {hasBn ? '⚠ ' : ''}{act.name}
                        </span>
                      )
                    })}
                  </div>
                </div>
              </div>
            )
          })()}

          {/* Bottleneck cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {filtered.map(bn => <BottleneckCard key={bn.id} bn={bn} getAutomationMode={getAutomationMode} onEdit={setEditingBn} />)}
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-12 text-gray-400">
              <div className="text-4xl mb-3">🔍</div>
              <div className="font-medium">No bottlenecks match the current filters</div>
            </div>
          )}
        </>
      )}

      {/* ── Criticality View: accordion per severity, ALL bottlenecks unfiltered ── */}
      {viewMode === 'criticality' && (
        <div className="space-y-4">
          <div className="text-xs text-gray-500 px-1">
            All {bottlenecks.length} bottlenecks across {PDLC_PHASES.length} PDLC phases — grouped by criticality
          </div>

          {CRITICALITY_GROUPS.map(group => (
            <CriticalityAccordion
              key={group.severity}
              group={group}
              bottlenecks={bottlenecks}
              getAutomationMode={getAutomationMode}
              onEdit={setEditingBn}
            />
          ))}
        </div>
      )}

      {/* ── Tool Stack Progression View ── */}
      {viewMode === 'toolstack' && (
        <div className="space-y-4">

          {/* Legend header */}
          <div className="bg-white border border-gray-200 rounded-xl p-4">
            <div className="text-sm font-bold text-gray-700 mb-3">
              Illustrative Bottleneck Resolution — Current State → Option A → Option B → Option C
            </div>
            <div className="grid grid-cols-4 gap-3 text-xs">
              <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5">
                <div className="font-bold text-slate-600 mb-1">Current State</div>
                <div className="text-slate-500">Partial AI adoption. Bottlenecks persist. Human-led across all phases.</div>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-2.5">
                <div className="font-bold text-blue-700 mb-1">Option A · AI-Enabled</div>
                <div className="text-blue-600">16 AI tools embedded. Human-led, AI as co-pilot. Each tool tackles its phase bottleneck independently.</div>
              </div>
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-2.5">
                <div className="font-bold text-purple-700 mb-1">Option B · AI-First</div>
                <div className="text-purple-600">21 agents orchestrated on-demand. Tools evolve into agents. Humans oversee, review, approve.</div>
              </div>
              <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-2.5">
                <div className="font-bold text-emerald-700 mb-1">Option C · STUMP ADLC</div>
                <div className="text-emerald-600">Full agentic pipeline. STUMP Platform orchestrates all agents. Human: intent, review, approve only.</div>
              </div>
            </div>
          </div>

          <div className="text-xs text-gray-500 px-1">
            {bottlenecks.length} bottlenecks across {PDLC_PHASES.length} PDLC phases — showing tool-stack progression per phase
          </div>

          {PDLC_PHASES.map(phase => (
            <PhaseProgressionAccordion
              key={phase.id}
              phase={phase}
              bottlenecks={bottlenecks}
              getAutomationMode={getAutomationMode}
            />
          ))}
        </div>
      )}

      {/* Footer nav */}
      <div className="flex gap-4">
        <Link to="/improvements" className="btn-primary flex-1 text-center py-3">
          🚀 View Improvement Actions →
        </Link>
        <Link to="/current-vsm" className="btn-secondary flex-1 text-center py-3">
          ← Current State VSM
        </Link>
      </div>

      {/* Inline edit modal */}
      <InlineEditModal
        item={editingBn}
        fields={BN_EDIT_FIELDS}
        title={editingBn ? `Edit: ${editingBn.activity}` : 'Edit Bottleneck'}
        onSave={saveBnEdit}
        onClose={() => setEditingBn(null)}
      />

      {Object.keys(bnEdits).length > 0 && (
        <div className="fixed bottom-4 right-4 bg-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg text-xs font-semibold z-40">
          ✏️ {Object.keys(bnEdits).length} bottleneck{Object.keys(bnEdits).length !== 1 ? 's' : ''} edited (session)
        </div>
      )}
    </div>
  )
}
