import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import clsx from 'clsx'

const API = '/api/v1'

const GRADE_CONFIG = {
  'A — Highly Accurate':    { bg: 'bg-blue-50',   text: 'text-blue-700',   border: 'border-blue-200',   bar: 'bg-blue-500' },
  'B — Good Accuracy':      { bg: 'bg-green-50',  text: 'text-green-700',  border: 'border-green-200',  bar: 'bg-green-500' },
  'C — Adequate':           { bg: 'bg-yellow-50', text: 'text-yellow-700', border: 'border-yellow-200', bar: 'bg-yellow-400' },
  'D — Limited Accuracy':   { bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200', bar: 'bg-teal-400' },
  'F — Insufficient Data':  { bg: 'bg-sky-50',    text: 'text-sky-700',    border: 'border-sky-200',    bar: 'bg-sky-400' },
}

const STEP_ICONS = ['🔗', '📐', '📊', '⚠️', '💡', '🔮', '💼', '📋']

function ScoreBar({ score, max = 100, colorClass }) {
  const pct = (score / max) * 100
  const color = colorClass || (score >= 80 ? 'bg-blue-500' : score >= 65 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-400' : score >= 35 ? 'bg-teal-400' : 'bg-sky-400')
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div className={clsx('h-full rounded-full transition-all duration-700', color)} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-sm font-bold w-10 text-right">{score}%</span>
    </div>
  )
}

function ComponentRow({ label, value }) {
  return (
    <div className="flex items-center justify-between text-xs py-1 border-b border-gray-50 last:border-0">
      <span className="text-gray-500">{label}</span>
      <div className="flex items-center gap-2 w-36">
        <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div
            className={clsx('h-full rounded-full',
              value >= 70 ? 'bg-green-400' : value >= 45 ? 'bg-yellow-400' : 'bg-sky-400'
            )}
            style={{ width: `${value}%` }}
          />
        </div>
        <span className="font-semibold text-gray-700 w-8 text-right">{value}%</span>
      </div>
    </div>
  )
}

function StepCard({ step, expanded, onToggle }) {
  const gradeCfg = step.score >= 80 ? GRADE_CONFIG['A — Highly Accurate']
    : step.score >= 65 ? GRADE_CONFIG['B — Good Accuracy']
    : step.score >= 50 ? GRADE_CONFIG['C — Adequate']
    : step.score >= 35 ? GRADE_CONFIG['D — Limited Accuracy']
    : GRADE_CONFIG['F — Insufficient Data']

  return (
    <div className={clsx('border rounded-lg overflow-hidden', gradeCfg.border)}>
      {/* Header */}
      <button
        className={clsx('w-full flex items-center gap-3 px-4 py-3 text-left hover:opacity-90 transition-opacity', gradeCfg.bg)}
        onClick={onToggle}
      >
        <span className="text-lg shrink-0">{STEP_ICONS[step.step - 1]}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold text-gray-400">Step {step.step}</span>
            <span className={clsx('font-semibold text-sm', gradeCfg.text)}>{step.agent}</span>
            {step.llm_enriched && (
              <span className="text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded border border-purple-200">🤖 LLM</span>
            )}
            {step.rag_docs_used > 0 && (
              <span className="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded border border-blue-200">
                📚 {step.rag_docs_used} KB docs
              </span>
            )}
          </div>
          <ScoreBar score={step.score} />
        </div>
        <span className="text-gray-400 text-sm">{expanded ? '▲' : '▼'}</span>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="bg-white px-4 py-3 border-t border-gray-100 space-y-3">
          {/* Interpretation */}
          <div className="text-sm text-gray-600 bg-gray-50 rounded px-3 py-2 border border-gray-100">
            💬 {step.interpretation}
          </div>

          {/* Score components */}
          <div>
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Score Components</div>
            {Object.entries(step.components || {}).map(([k, v]) => (
              <ComponentRow key={k} label={k.replace(/_/g, ' ')} value={typeof v === 'number' ? Math.round(v) : 0} />
            ))}
          </div>

          {/* RAG top docs */}
          {step.rag_top_docs?.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
                📚 Knowledge Base Matches
              </div>
              <div className="space-y-1">
                {step.rag_top_docs.map((doc, i) => (
                  <div key={i} className="flex items-center justify-between text-xs bg-blue-50 border border-blue-100 rounded px-2 py-1">
                    <span className="text-blue-700 truncate">{doc.title}</span>
                    <span className="text-blue-500 font-semibold ml-2 shrink-0">{doc.relevance}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Step metadata */}
          <div className="grid grid-cols-3 gap-2 text-xs text-gray-500">
            {step.source_type     && <div><span className="font-medium">Source:</span> {step.source_type}</div>}
            {step.phases_with_data != null && <div><span className="font-medium">Phases:</span> {step.phases_with_data}/7</div>}
            {step.bottlenecks_detected != null && <div><span className="font-medium">Bottlenecks:</span> {step.bottlenecks_detected}</div>}
            {step.improvements_generated != null && <div><span className="font-medium">Improvements:</span> {step.improvements_generated}</div>}
            {step.scenarios_generated != null && <div><span className="font-medium">Scenarios:</span> {step.scenarios_generated}/3</div>}
            {step.form_fields_filled != null && <div><span className="font-medium">Fields filled:</span> {step.form_fields_filled}/{step.form_fields_total}</div>}
          </div>
        </div>
      )}
    </div>
  )
}

// ── KB Search Panel ──────────────────────────────────────────────────
function KBSearchPanel() {
  const [query, setQuery]     = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [kb, setKb]           = useState(null)

  useEffect(() => {
    fetch(`${API}/accuracy/kb/all`)
      .then(r => r.json())
      .then(d => setKb(d))
      .catch(() => {})
  }, [])

  async function search() {
    if (!query.trim()) return
    setLoading(true)
    try {
      const r = await fetch(`${API}/accuracy/kb/search?q=${encodeURIComponent(query)}&top_k=5`)
      const d = await r.json()
      setResults(d.results || [])
    } catch {}
    setLoading(false)
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 space-y-3">
      <h3 className="font-semibold text-gray-800 flex items-center gap-2">
        <span>📚</span> Knowledge Base ({kb?.total || 0} documents)
      </h3>

      {/* Category breakdown */}
      {kb?.categories && (
        <div className="flex flex-wrap gap-1">
          {kb.categories.map(cat => {
            const count = kb.documents.filter(d => d.category === cat).length
            return (
              <span key={cat} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded border border-gray-200">
                {cat} ({count})
              </span>
            )
          })}
        </div>
      )}

      {/* Search */}
      <div className="flex gap-2">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && search()}
          placeholder="Search knowledge base... e.g. 'DORA elite deployment frequency'"
          className="flex-1 text-sm border border-gray-300 rounded px-3 py-1.5 focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={search}
          disabled={loading || !query.trim()}
          className="bg-blue-600 text-white text-sm px-4 py-1.5 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? '⟳' : 'Search'}
        </button>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-2 max-h-72 overflow-y-auto">
          {results.map(doc => (
            <div key={doc.id} className="border border-gray-100 rounded p-3 bg-gray-50">
              <div className="flex items-start justify-between gap-2 mb-1">
                <span className="text-xs font-semibold text-blue-700">{doc.category}</span>
                <span className="text-xs text-green-600 font-semibold shrink-0">
                  {doc.relevance_pct}% match
                </span>
              </div>
              <div className="text-sm font-medium text-gray-800 mb-1">{doc.title}</div>
              <div className="text-xs text-gray-600 leading-relaxed">{doc.content?.slice(0, 200)}...</div>
              <div className="flex flex-wrap gap-1 mt-1.5">
                {doc.tags?.slice(0, 5).map(tag => (
                  <span key={tag} className="text-xs bg-blue-50 text-blue-600 border border-blue-100 px-1.5 py-0.5 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Main Page ────────────────────────────────────────────────────────
export default function AccuracyScorePage() {
  const { project } = useApp()
  const [data, setData]         = useState(null)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState(null)
  const [expanded, setExpanded] = useState({})
  const [activeTab, setActiveTab] = useState('scores')  // scores | rag | kb

  async function loadScores(useDemo = false) {
    setLoading(true); setError(null)
    try {
      const url = useDemo || !project?.id
        ? `${API}/accuracy/demo`
        : `${API}/accuracy/${project.id}`
      const r = await fetch(url)
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      const d = await r.json()
      setData(d)
      // Auto-expand weakest step
      if (d.improvement_opportunities?.length > 0) {
        const weakStep = d.steps.find(s => s.agent === d.improvement_opportunities[0].step)
        if (weakStep) setExpanded({ [weakStep.step]: true })
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadScores() }, [project?.id])

  const gradeCfg = data ? (GRADE_CONFIG[data.overall_grade] || GRADE_CONFIG['C — Adequate']) : null

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Accuracy Score & RAG Analysis</h2>
          <p className="text-sm text-gray-500 mt-0.5">
            Per-step confidence scores · Knowledge base retrieval · Contextualization quality
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => loadScores(true)}
            className="text-sm border border-gray-300 px-3 py-1.5 rounded hover:bg-gray-50"
          >
            Demo Mode
          </button>
          <button
            onClick={() => loadScores(false)}
            disabled={loading}
            className="text-sm bg-blue-600 text-white px-4 py-1.5 rounded hover:bg-blue-700 disabled:opacity-50 flex items-center gap-1.5"
          >
            {loading ? <><span className="animate-spin">⟳</span> Loading...</> : '↻ Refresh Scores'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-sky-50 border border-sky-200 text-sky-700 text-sm px-4 py-2 rounded">{error}</div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200 flex gap-0">
        {[
          { id: 'scores', label: '📊 Step Accuracy Scores' },
          { id: 'rag',    label: '🔍 RAG & Contextualization' },
          { id: 'kb',     label: '📚 Knowledge Base' },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={clsx(
              'px-5 py-2.5 text-sm font-medium border-b-2 transition-colors',
              activeTab === t.id
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
            )}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* ── TAB: SCORES ─────────────────────────────────────────────── */}
      {activeTab === 'scores' && data && (
        <div className="grid grid-cols-12 gap-4">
          {/* Left: overall score */}
          <div className="col-span-3 space-y-3">
            {/* Overall score card */}
            <div className={clsx('border rounded-lg p-5 text-center', gradeCfg?.border, gradeCfg?.bg)}>
              <div className="text-6xl font-black text-gray-800 mb-1">{data.overall_accuracy}</div>
              <div className="text-sm text-gray-500 mb-2">Overall Accuracy %</div>
              <div className={clsx('font-semibold text-sm px-3 py-1 rounded-full inline-block', gradeCfg?.text, gradeCfg?.bg, 'border', gradeCfg?.border)}>
                {data.overall_grade}
              </div>

              {/* Overall bar */}
              <div className="mt-4">
                <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={clsx('h-full rounded-full transition-all duration-1000', gradeCfg?.bar)}
                    style={{ width: `${data.overall_accuracy}%` }}
                  />
                </div>
              </div>

              {/* Data source badge */}
              {data.data_source && (
                <div className="mt-3 text-xs text-gray-400">
                  Source: <span className="font-medium">{data.data_source.replace(/_/g, ' ')}</span>
                </div>
              )}
            </div>

            {/* Step scores mini */}
            <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">All Steps</div>
              {data.steps?.map(step => (
                <div key={step.step} className="flex items-center gap-2">
                  <span className="text-sm w-4 shrink-0">{STEP_ICONS[step.step - 1]}</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-gray-600 truncate">{step.agent}</div>
                    <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden mt-0.5">
                      <div
                        className={clsx('h-full rounded-full',
                          step.score >= 75 ? 'bg-green-400' : step.score >= 55 ? 'bg-yellow-400' : 'bg-sky-400'
                        )}
                        style={{ width: `${step.score}%` }}
                      />
                    </div>
                  </div>
                  <span className="text-xs font-bold text-gray-600 w-8 text-right shrink-0">{step.score}%</span>
                </div>
              ))}
            </div>

            {/* Pipeline notes */}
            {data.pipeline_notes?.length > 0 && (
              <div className="bg-cyan-50 border border-cyan-200 rounded-lg p-3">
                <div className="text-xs font-semibold text-cyan-700 mb-2">💡 To Improve Accuracy</div>
                <ul className="space-y-1.5">
                  {data.pipeline_notes.map((note, i) => (
                    <li key={i} className="text-xs text-cyan-700 flex items-start gap-1">
                      <span className="shrink-0 mt-0.5">→</span>{note}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Right: step cards */}
          <div className="col-span-9 space-y-2">
            {data.steps?.map(step => (
              <StepCard
                key={step.step}
                step={step}
                expanded={!!expanded[step.step]}
                onToggle={() => setExpanded(prev => ({ ...prev, [step.step]: !prev[step.step] }))}
              />
            ))}
          </div>
        </div>
      )}

      {/* ── TAB: RAG ─────────────────────────────────────────────────── */}
      {activeTab === 'rag' && data && (
        <div className="space-y-4">
          {/* RAG summary */}
          <div className="grid grid-cols-4 gap-3">
            {[
              { label: 'KB Documents',        value: data.rag_summary?.kb_total_documents,        icon: '📄', suffix: ' docs' },
              { label: 'Docs Retrieved',       value: data.rag_summary?.total_kb_docs_retrieved,   icon: '🔍', suffix: ' total' },
              { label: 'Avg Retrieval Quality',value: data.rag_summary?.avg_retrieval_relevance,   icon: '🎯', suffix: '%' },
              { label: 'LLM Enrichment',       value: data.rag_summary?.llm_enrichment_active ? 'Active' : 'Not configured', icon: '🤖', suffix: '' },
            ].map(m => (
              <div key={m.label} className="bg-white border border-gray-200 rounded-lg p-4 text-center">
                <div className="text-2xl mb-1">{m.icon}</div>
                <div className="text-2xl font-bold text-gray-800">{m.value}{m.suffix}</div>
                <div className="text-xs text-gray-500 mt-1">{m.label}</div>
              </div>
            ))}
          </div>

          {/* Per-step RAG breakdown */}
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="px-4 py-2.5 bg-gray-50 border-b border-gray-200 flex items-center gap-2">
              <span>🔍</span>
              <span className="font-semibold text-sm text-gray-700">Knowledge Base Retrieval — Per Step</span>
            </div>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100 text-xs text-gray-500 bg-gray-50">
                  <th className="text-left px-4 py-2">Step</th>
                  <th className="text-left px-3 py-2">Agent</th>
                  <th className="text-left px-3 py-2 w-16">Docs</th>
                  <th className="text-left px-3 py-2 w-40">Retrieval Quality</th>
                  <th className="text-left px-3 py-2">Top KB Match</th>
                  <th className="text-left px-3 py-2 w-20">LLM</th>
                </tr>
              </thead>
              <tbody>
                {data.steps?.map(step => (
                  <tr key={step.step} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-2.5 text-sm">
                      <span className="mr-1">{STEP_ICONS[step.step - 1]}</span>
                      <span className="text-gray-400">{step.step}</span>
                    </td>
                    <td className="px-3 py-2.5 font-medium text-gray-700">{step.agent}</td>
                    <td className="px-3 py-2.5 text-center">
                      <span className="text-xs bg-blue-50 text-blue-700 border border-blue-100 px-1.5 py-0.5 rounded">
                        {step.rag_docs_used}
                      </span>
                    </td>
                    <td className="px-3 py-2.5">
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className={clsx('h-full rounded-full', step.components?.kb_retrieval >= 70 ? 'bg-green-400' : step.components?.kb_retrieval >= 40 ? 'bg-yellow-400' : 'bg-sky-400')}
                            style={{ width: `${step.components?.kb_retrieval || 0}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-600">{step.components?.kb_retrieval || 0}%</span>
                      </div>
                    </td>
                    <td className="px-3 py-2.5 text-xs text-gray-500">
                      {step.rag_top_docs?.[0]
                        ? <span className="text-blue-600">{step.rag_top_docs[0].title} <span className="text-gray-400">({step.rag_top_docs[0].relevance}%)</span></span>
                        : <span className="text-gray-300">—</span>
                      }
                    </td>
                    <td className="px-3 py-2.5">
                      {step.llm_enriched
                        ? <span className="text-xs bg-purple-100 text-purple-700 border border-purple-200 px-1.5 py-0.5 rounded">✓ Active</span>
                        : <span className="text-xs text-gray-300">—</span>
                      }
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Contextualization quality */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h4 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <span>🧠</span> Contextualization Sources
            </h4>
            <div className="grid grid-cols-3 gap-3 text-sm">
              {[
                { label: 'Static Knowledge Base',   desc: '18 curated documents: DORA 2024, Lean VSM, AI agent benchmarks, industry-specific data', status: 'active', icon: '📚' },
                { label: 'PDLC Canonical Data',      desc: '7 phases, 36 activities, industry benchmarks per phase — always applied', status: 'active', icon: '📐' },
                { label: 'DORA Calibration',         desc: 'User-provided DORA metrics override estimated phase timings for +15% VSM accuracy', status: data.steps?.find(s => s.dora_calibration_active) ? 'active' : 'inactive', icon: '📈' },
                { label: 'LLM Enrichment',           desc: 'Azure OpenAI / OpenAI for narrative generation, root-cause analysis, competitor insights', status: data.rag_summary?.llm_enrichment_active ? 'active' : 'inactive', icon: '🤖' },
                { label: 'Team Context (Playbook)',  desc: '11 profile fields + 7 documents for personalised playbook generation', status: 'partial', icon: '👥' },
                { label: 'Vector Embeddings',        desc: 'Semantic embedding-based retrieval (planned — currently BM25 keyword retrieval)', status: 'planned', icon: '🧬' },
              ].map(src => (
                <div key={src.label} className={clsx(
                  'border rounded-lg p-3',
                  src.status === 'active'   ? 'border-green-200 bg-green-50' :
                  src.status === 'partial'  ? 'border-yellow-200 bg-yellow-50' :
                  src.status === 'planned'  ? 'border-gray-200 bg-gray-50' :
                  'border-sky-100 bg-sky-50'
                )}>
                  <div className="flex items-center gap-2 mb-1">
                    <span>{src.icon}</span>
                    <span className="text-xs font-semibold text-gray-700">{src.label}</span>
                    <span className={clsx(
                      'ml-auto text-xs px-1.5 py-0.5 rounded font-medium',
                      src.status === 'active'   ? 'bg-green-100 text-green-700' :
                      src.status === 'partial'  ? 'bg-yellow-100 text-yellow-700' :
                      src.status === 'planned'  ? 'bg-gray-100 text-gray-500' :
                      'bg-sky-100 text-sky-600'
                    )}>
                      {src.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 leading-snug">{src.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ── TAB: KB ──────────────────────────────────────────────────── */}
      {activeTab === 'kb' && <KBSearchPanel />}

      {/* Loading state */}
      {loading && !data && (
        <div className="bg-gray-50 border border-dashed border-gray-300 rounded-lg p-12 text-center">
          <div className="text-4xl mb-3 animate-spin">⟳</div>
          <div className="text-gray-600 font-medium">Calculating accuracy scores...</div>
        </div>
      )}

      {/* No data state */}
      {!loading && !data && !error && (
        <div className="bg-gray-50 border border-dashed border-gray-300 rounded-lg p-12 text-center">
          <div className="text-4xl mb-3">📊</div>
          <div className="text-gray-700 font-semibold mb-2">No accuracy data yet</div>
          <p className="text-gray-500 text-sm mb-4">
            Run a VSM analysis first, or try Demo Mode to see how scoring works.
          </p>
          <button
            onClick={() => loadScores(true)}
            className="bg-blue-600 text-white text-sm px-6 py-2 rounded hover:bg-blue-700"
          >
            View Demo Scores
          </button>
        </div>
      )}
    </div>
  )
}
