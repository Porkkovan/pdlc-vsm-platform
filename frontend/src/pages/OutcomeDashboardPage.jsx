import { useEffect, useState, useCallback, useMemo } from 'react'
import {
  ResponsiveContainer, BarChart, Bar, LineChart, Line, AreaChart, Area,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, Cell,
} from 'recharts'
import {
  Bot, Gauge, ShieldCheck, RefreshCw, Plug, Plus, Trash2, X, Check,
  AlertCircle, TrendingUp, TrendingDown, Minus, Database, Table2,
  Calculator, ArrowRight, DollarSign, PenSquare, Filter, Layers, Info,
} from 'lucide-react'
import { useApp } from '../contexts/AppContext'
import { outcomeApi } from '../services/api'
import TargetStateBanner from '../components/TargetStateBanner'
import TargetStepBar from '../components/TargetStepBar'
import { useTargetScenario } from '../components/useTargetScenario'
import JCurveInputs from '../components/JCurveInputs'

const PERSPECTIVE_ICON = { adoption: Bot, performance: Gauge, ai_ops: ShieldCheck }
const SCEN = [
  { id: 'option-a', label: 'Option A', sub: 'Augmented Human', color: '#2563eb' },
  { id: 'option-b', label: 'Option B', sub: 'Hybrid Agents',    color: '#7c3aed' },
  { id: 'option-c', label: 'Option C', sub: 'AI-First',         color: '#059669' },
]
const SEV = {
  good: { dot: 'bg-emerald-500', chip: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
  warn: { dot: 'bg-cyan-500',   chip: 'bg-cyan-50 text-cyan-700 border-cyan-200' },
  info: { dot: 'bg-sky-500',     chip: 'bg-sky-50 text-sky-700 border-sky-200' },
}

// ── KPI card ──────────────────────────────────────────────────────────────
function KpiCard({ kpi }) {
  const goodDir = kpi.better === 'down' ? 'down' : 'up'
  const isGood = kpi.better === 'track' ? null : kpi.delta_dir === goodDir
  const Arrow = kpi.delta_dir === 'up' ? TrendingUp : kpi.delta_dir === 'down' ? TrendingDown : Minus
  const deltaColor = isGood === null ? 'text-gray-400' : isGood ? 'text-emerald-600' : 'text-sky-500'
  return (
    <div className="card p-4 flex flex-col gap-1 relative group cursor-help">
      <div className="text-[11px] font-semibold text-gray-500 uppercase tracking-wide leading-tight flex items-center gap-1">
        {kpi.label}<Info size={11} className="text-gray-300 group-hover:text-sky-800 shrink-0" />
      </div>
      <div className="flex items-end justify-between">
        <div className="text-2xl font-extrabold text-sky-800">{kpi.display}</div>
        {kpi.delta && (
          <div className={`flex items-center gap-0.5 text-xs font-bold ${deltaColor}`}>
            <Arrow size={13} />{kpi.delta}
          </div>
        )}
      </div>
      <div className="flex items-center justify-between text-[10px] text-gray-400">
        <span>Opt B target: <span className="font-semibold text-gray-500">{kpi.target}</span></span>
        <span className="truncate ml-1">{kpi.source}</span>
      </div>
      {/* hover detail — formula · data source · A/B/C bands · one-line insight */}
      <div className="hidden group-hover:block absolute left-0 top-full mt-1.5 z-30 w-72 bg-sky-500 text-white rounded-lg shadow-2xl p-3 text-left">
        <div className="font-bold text-xs mb-1.5">{kpi.label}</div>
        {kpi.formula && <>
          <div className="text-[9px] font-bold uppercase tracking-wide text-blue-300">Formula</div>
          <div className="font-mono text-[10.5px] text-blue-50 mb-1.5 leading-snug">{kpi.formula}</div>
        </>}
        {kpi.source && <>
          <div className="text-[9px] font-bold uppercase tracking-wide text-blue-300">Data source</div>
          <div className="text-[11px] text-blue-50 mb-1.5">{kpi.source}</div>
        </>}
        {kpi.ranges && (
          <div className="text-[10px] text-blue-100 mb-1.5">
            A {kpi.ranges['option-a']} · B {kpi.ranges['option-b']} · C {kpi.ranges['option-c']}
          </div>
        )}
        {kpi.insight && (
          <div className="pt-1.5 border-t border-white/15">
            <div className="text-[9px] font-bold uppercase tracking-wide text-cyan-300">Inference</div>
            <div className="text-[11px] text-blue-50 leading-snug">{kpi.insight}</div>
          </div>
        )}
      </div>
    </div>
  )
}

// ── Generic chart renderer ──────────────────────────────────────────────────
const X_LABELS = { sprint: 'Sprint', phase: 'PDLC Phase', agent: 'Agent', check: 'Assurance Check', dim: '' }
const Y_BY_UNIT = {
  '%': 'Percent (%)', days: 'Calendar days', $: 'USD ($)', pd: 'Person-days', SP: 'Story Points',
  '×': 'ROI (× multiple)', M: 'Tokens (M)', '/wk': 'Deploys / week', hrs: 'Hours', s: 'Seconds',
  'SP/pd': 'SP / person-day', items: 'Items',
}
function ChartCard({ chart, meta }) {
  const { type, title, subtitle, data, series = [], xKey, target } = chart
  const axisProps = { tick: { fontSize: 11, fill: '#64748b' }, axisLine: { stroke: '#e2e8f0' }, tickLine: false }
  const tip = { contentStyle: { fontSize: 12, borderRadius: 8, border: '1px solid #e2e8f0' } }
  const margin = { top: 8, right: 18, left: 14, bottom: 18 }
  const xLabel = chart.xLabel || X_LABELS[xKey] || ''
  const yLabel = chart.yLabel || Y_BY_UNIT[chart.unit] || ''
  const xLab = xLabel ? { value: xLabel, position: 'insideBottom', offset: -6, fontSize: 11, fill: '#64748b' } : undefined
  const yLab = yLabel ? { value: yLabel, angle: -90, position: 'insideLeft', offset: 6, fontSize: 11, fill: '#64748b', style: { textAnchor: 'middle' } } : undefined

  let body = null
  if (type === 'dora') {
    body = <DoraBands chart={chart} />
  } else if (type === 'radar') {
    body = (
      <ResponsiveContainer width="100%" height={260}>
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="72%">
          <PolarGrid stroke="#e2e8f0" />
          <PolarAngleAxis dataKey={xKey} tick={{ fontSize: 10, fill: '#475569' }} />
          <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 9, fill: '#94a3b8' }} />
          {series.map(s => (
            <Radar key={s.key} dataKey={s.key} name={s.name} stroke={s.color}
                   fill={s.color} fillOpacity={0.35} />
          ))}
          <Tooltip {...tip} />
        </RadarChart>
      </ResponsiveContainer>
    )
  } else if (type === 'line') {
    body = (
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={data} margin={margin}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey={xKey} {...axisProps} label={xLab} />
          <YAxis {...axisProps} label={yLab} />
          <Tooltip {...tip} /><Legend wrapperStyle={{ fontSize: 11 }} verticalAlign="top" height={24} />
          {target && <ReferenceLine y={target.value} stroke="#94a3b8" strokeDasharray="4 4"
            label={{ value: target.label, fontSize: 10, fill: '#64748b', position: 'right' }} />}
          {series.map(s => (
            <Line key={s.key} type="monotone" dataKey={s.key} name={s.name}
                  stroke={s.color} strokeWidth={2.5} dot={{ r: 3 }} activeDot={{ r: 5 }} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    )
  } else if (type === 'area') {
    body = (
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={data} margin={margin}>
          <defs>
            {series.map(s => (
              <linearGradient key={s.key} id={`g-${chart.id}-${s.key}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={s.color} stopOpacity={0.4} />
                <stop offset="95%" stopColor={s.color} stopOpacity={0.03} />
              </linearGradient>
            ))}
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey={xKey} {...axisProps} label={xLab} /><YAxis {...axisProps} label={yLab} />
          <Tooltip {...tip} />
          {series.map(s => (
            <Area key={s.key} type="monotone" dataKey={s.key} name={s.name}
                  stroke={s.color} strokeWidth={2.5} fill={`url(#g-${chart.id}-${s.key})`} />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    )
  } else {
    // bar / stacked-bar
    const stacked = type === 'stacked-bar'
    body = (
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} margin={margin}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey={xKey} {...axisProps} label={xLab} /><YAxis {...axisProps} label={yLab} />
          <Tooltip {...tip} />{series.length > 1 && <Legend wrapperStyle={{ fontSize: 11 }} verticalAlign="top" height={24} />}
          {target && <ReferenceLine y={target.value} stroke="#0ea5e9" strokeDasharray="4 4"
            label={{ value: target.label, fontSize: 10, fill: '#0ea5e9', position: 'right' }} />}
          {series.map(s => (
            <Bar key={s.key} dataKey={s.key} name={s.name} fill={s.color}
                 stackId={stacked ? 'a' : undefined} radius={stacked ? 0 : [4, 4, 0, 0]} maxBarSize={48} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    )
  }

  return (
    <div className="card">
      <div className="card-header py-3">
        <div className="relative inline-block group">
          <h3 className="font-bold text-gray-800 text-sm inline-flex items-center gap-1 cursor-help border-b border-dotted border-gray-300">
            {title}<Info size={12} className="text-gray-300 group-hover:text-sky-800" />
          </h3>
          {meta && (meta.formula || meta.source) && (
            <div className="hidden group-hover:block absolute left-0 top-full mt-1.5 z-30 w-72 bg-sky-500 text-white rounded-lg shadow-2xl p-3 text-left">
              <div className="font-bold text-xs mb-1.5">{meta.name || title}</div>
              {meta.formula && <>
                <div className="text-[9px] font-bold uppercase tracking-wide text-blue-300">Formula</div>
                <div className="font-mono text-[10.5px] text-blue-50 mb-1.5 leading-snug">{meta.formula}</div>
              </>}
              {meta.source && <>
                <div className="text-[9px] font-bold uppercase tracking-wide text-blue-300">Data source</div>
                <div className="text-[11px] text-blue-50">{meta.source}</div>
              </>}
              {meta.ranges && (
                <div className="mt-1.5 pt-1.5 border-t border-white/15 text-[10px] text-blue-100">
                  A {meta.ranges['option-a']} · B {meta.ranges['option-b']} · C {meta.ranges['option-c']}
                </div>
              )}
            </div>
          )}
        </div>
        {subtitle && <p className="text-[11px] text-gray-400 mt-0.5">{subtitle}</p>}
      </div>
      <div className="card-body py-3">{body}</div>
    </div>
  )
}

// ── DORA band positioning (custom) ──────────────────────────────────────────
function DoraBands({ chart }) {
  const { bands = [], current = 0, markers = [] } = chart
  const tone = ['bg-sky-100 border-sky-200', 'bg-cyan-100 border-cyan-200',
                'bg-sky-100 border-sky-200', 'bg-emerald-100 border-emerald-200']
  return (
    <div className="space-y-2 py-2">
      {bands.map((b, i) => {
        const isCurrent = i === current
        const m = markers.filter(x => x.at === i)
        return (
          <div key={b.name}
               className={`flex items-center justify-between rounded-lg border px-3 py-2 ${tone[i]} ${isCurrent ? 'ring-2 ring-sky-500' : 'opacity-80'}`}>
            <div>
              <div className="font-bold text-sm text-gray-800">{b.name}{isCurrent && ' ◀ Now'}</div>
              <div className="text-[10px] text-gray-500">{b.desc}</div>
            </div>
            <div className="flex gap-1">
              {m.map(x => (
                <span key={x.label} className="text-[10px] font-bold bg-white/70 border border-gray-300 rounded px-1.5 py-0.5 text-gray-700">{x.label}</span>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}

// ── Inference panel (editable + addable) ────────────────────────────────────
function Inferences({ items, engine, custom, projectId, scenario, perspectiveKey, onSaved, onReload, addNotification }) {
  const [edit, setEdit] = useState(false)
  const [list, setList] = useState(items)
  const [busy, setBusy] = useState(false)
  useEffect(() => { setList(items); setEdit(false) }, [items, scenario, perspectiveKey])

  const upd = (i, patch) => setList(l => l.map((n, idx) => idx === i ? { ...n, ...patch } : n))
  const del = (i) => setList(l => l.filter((_, idx) => idx !== i))
  const add = () => setList(l => [...l, { title: '', text: '', severity: 'info' }])

  const save = async () => {
    setBusy(true)
    try {
      const clean = list.filter(n => (n.title || '').trim() || (n.text || '').trim())
      const res = await outcomeApi.saveInferences(projectId, scenario, perspectiveKey, clean)
      onSaved(perspectiveKey, res.inferences); setEdit(false)
      addNotification('Inference & action points saved', 'success')
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }
  const resetToAI = async () => {
    setBusy(true)
    try {
      await outcomeApi.resetInferences(projectId, scenario, perspectiveKey)
      setEdit(false); onReload()
      addNotification('Reverted to generated inferences', 'success')
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }
  const cancel = () => { setList(items); setEdit(false) }

  return (
    <div className="card">
      <div className="card-header py-3 flex items-center justify-between">
        <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2">
          <AlertCircle size={15} className="text-sky-600" /> Inference & Action Points
          {custom && <span className="badge-navy !py-0">edited</span>}
        </h3>
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-gray-400 italic">{custom ? 'custom' : engine === 'llm' ? 'AI-generated' : 'rule-based'}</span>
          {!edit && (
            <button onClick={() => setEdit(true)} className="text-xs font-semibold px-2 py-1 rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 flex items-center gap-1">
              <PenSquare size={12} /> Edit
            </button>
          )}
        </div>
      </div>

      {!edit ? (
        <div className="card-body py-3 grid grid-cols-1 md:grid-cols-2 gap-3">
          {list.length === 0 && <p className="text-xs text-gray-400">No inferences. Click Edit → Add to create one.</p>}
          {list.map((n, i) => {
            const s = SEV[n.severity] || SEV.info
            return (
              <div key={i} className={`rounded-lg border px-3 py-2.5 ${s.chip}`}>
                <div className="flex items-center gap-2 mb-1">
                  <span className={`w-2 h-2 rounded-full ${s.dot}`} />
                  <span className="font-bold text-xs">{n.title}</span>
                </div>
                <p className="text-[11.5px] leading-snug text-gray-600">{n.text}</p>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="card-body py-3 space-y-2">
          {list.map((n, i) => (
            <div key={i} className="border border-gray-200 rounded-lg p-2.5 flex gap-2 items-start">
              <select value={n.severity} onChange={e => upd(i, { severity: e.target.value })}
                className="inp !w-24 !px-2 !py-1.5 text-xs shrink-0">
                <option value="good">good</option><option value="warn">warn</option><option value="info">info</option>
              </select>
              <div className="flex-1 space-y-1.5">
                <input className="inp !px-2 !py-1.5 text-sm font-semibold" placeholder="Title"
                  value={n.title} onChange={e => upd(i, { title: e.target.value })} />
                <textarea className="inp !px-2 !py-1.5 text-xs" rows={2} placeholder="Inference & recommended action…"
                  value={n.text} onChange={e => upd(i, { text: e.target.value })} />
              </div>
              <button onClick={() => del(i)} className="text-gray-400 hover:text-sky-500 p-1 shrink-0"><Trash2 size={15} /></button>
            </div>
          ))}
          <div className="flex flex-wrap gap-2 pt-1">
            <button onClick={add} className="btn-secondary text-xs flex items-center gap-1"><Plus size={13} /> Add inference</button>
            <button onClick={save} disabled={busy} className="btn-primary text-xs flex items-center gap-1"><Check size={13} /> Save</button>
            <button onClick={cancel} className="btn-secondary text-xs">Cancel</button>
            <button onClick={resetToAI} disabled={busy} className="text-xs text-gray-500 hover:text-sky-800 ml-auto self-center">Revert to {engine === 'llm' ? 'AI' : 'auto'}-generated</button>
          </div>
        </div>
      )}
    </div>
  )
}

// ── Data source modal ────────────────────────────────────────────────────────
const BLANK = { perspective: 'performance', source_type: 'jira', label: '', base_url: '',
                username: '', token: '', config: {}, enabled: true }

function SourceModal({ projectId, catalog, onClose, addNotification }) {
  const [sources, setSources] = useState([])
  const [form, setForm] = useState(BLANK)
  const [editing, setEditing] = useState(null)
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => {
    outcomeApi.listSources(projectId).then(setSources).catch(e => addNotification(e.message, 'error'))
  }, [projectId, addNotification])
  useEffect(() => { load() }, [load])

  const sourceTypes = catalog?.source_types?.[form.perspective] || []
  const cfgKey = form.source_type === 'github' ? 'repo' : 'project'
  const cfgLabel = form.source_type === 'github' ? 'Repo (owner/name)' : 'Project / board key'

  const save = async () => {
    setBusy(true)
    try {
      if (editing) await outcomeApi.updateSource(projectId, editing, form)
      else await outcomeApi.createSource(projectId, form)
      addNotification('Data source saved', 'success')
      setForm(BLANK); setEditing(null); load()
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }
  const test = async (id) => {
    try { const r = await outcomeApi.testSource(projectId, id); addNotification(r.message, r.ok ? 'success' : 'error'); load() }
    catch (e) { addNotification(e.message, 'error') }
  }
  const del = async (id) => {
    try { await outcomeApi.deleteSource(projectId, id); load() } catch (e) { addNotification(e.message, 'error') }
  }
  const edit = (s) => { setEditing(s.id); setForm({ ...s, token: '' }) }

  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[88vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100 sticky top-0 bg-white z-10">
          <h2 className="font-bold text-sky-800 flex items-center gap-2"><Plug size={18} /> Real-time Data Sources</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600"><X size={20} /></button>
        </div>

        <div className="px-6 py-4">
          {/* existing sources */}
          <div className="space-y-2 mb-5">
            {sources.length === 0 && <p className="text-sm text-gray-400">No data sources yet. Add Jira, GitHub, CI/CD, AI-platform, etc. below.</p>}
            {sources.map(s => (
              <div key={s.id} className="flex items-center justify-between border border-gray-200 rounded-lg px-3 py-2">
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm text-gray-800 truncate">{s.label}</span>
                    <span className="tag-metric">{s.source_type}</span>
                    <span className="text-[10px] text-gray-400">{catalog?.perspectives?.[s.perspective]?.label}</span>
                  </div>
                  <div className="text-[11px] text-gray-400 truncate">{s.base_url || '—'}
                    {s.last_status && s.last_status !== 'never' &&
                      <span className={s.last_status === 'ok' ? 'text-emerald-600 ml-2' : 'text-sky-500 ml-2'}>· {s.last_status}: {s.last_message}</span>}
                  </div>
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  <button onClick={() => test(s.id)} className="text-xs px-2 py-1 rounded bg-sky-50 text-sky-700 hover:bg-sky-100 font-medium">Test</button>
                  <button onClick={() => edit(s)} className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-600 hover:bg-gray-200 font-medium">Edit</button>
                  <button onClick={() => del(s.id)} className="text-gray-400 hover:text-sky-500 p-1"><Trash2 size={15} /></button>
                </div>
              </div>
            ))}
          </div>

          {/* form */}
          <div className="border-t border-gray-100 pt-4">
            <div className="text-xs font-bold uppercase tracking-wide text-gray-500 mb-3">
              {editing ? 'Edit source' : 'Add data source'}
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Field label="Perspective">
                <select className="inp" value={form.perspective}
                        onChange={e => setForm(f => ({ ...f, perspective: e.target.value, source_type: (catalog?.source_types?.[e.target.value]?.[0]?.[0]) || 'custom' }))}>
                  {Object.entries(catalog?.perspectives || {}).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
                </select>
              </Field>
              <Field label="Source type">
                <select className="inp" value={form.source_type} onChange={e => setForm(f => ({ ...f, source_type: e.target.value }))}>
                  {sourceTypes.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
              </Field>
              <Field label="Label"><input className="inp" value={form.label} onChange={e => setForm(f => ({ ...f, label: e.target.value }))} placeholder="e.g. US Bank Jira" /></Field>
              <Field label={cfgLabel}><input className="inp" value={form.config?.[cfgKey] || ''} onChange={e => setForm(f => ({ ...f, config: { ...f.config, [cfgKey]: e.target.value } }))} placeholder={form.source_type === 'github' ? 'org/repo' : 'PAY'} /></Field>
              <Field label="Base URL" full><input className="inp" value={form.base_url || ''} onChange={e => setForm(f => ({ ...f, base_url: e.target.value }))} placeholder="https://yourcompany.atlassian.net" /></Field>
              <Field label="Username / email"><input className="inp" value={form.username || ''} onChange={e => setForm(f => ({ ...f, username: e.target.value }))} placeholder="user@company.com" /></Field>
              <Field label={editing ? 'API token (blank = keep)' : 'API token / PAT'}><input className="inp" type="password" value={form.token || ''} onChange={e => setForm(f => ({ ...f, token: e.target.value }))} placeholder="••••••••" /></Field>
            </div>
            <div className="flex gap-2 mt-4">
              <button onClick={save} disabled={busy} className="btn-primary text-sm flex items-center gap-1.5">
                <Check size={15} />{editing ? 'Update' : 'Add'} source
              </button>
              {editing && <button onClick={() => { setEditing(null); setForm(BLANK) }} className="btn-secondary text-sm">Cancel</button>}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
function Field({ label, children, full }) {
  return <div className={full ? 'col-span-2' : ''}><label className="block text-[11px] font-semibold text-gray-500 mb-1">{label}</label>{children}</div>
}

// ── Productivity economics (SP → Effort → Cost) ──────────────────────────────
const PROD_FIELDS = [
  { key: 'team_size', label: 'Team size', unit: 'engineers', step: 1, src: 'HR / org' },
  { key: 'sprint_days', label: 'Sprint length', unit: 'days', step: 1, src: 'Jira/ADO' },
  { key: 'utilisation', label: 'Utilisation', unit: '0–1 focus', step: 0.05, src: 'config' },
  { key: 'blended_daily_rate', label: 'Blended rate', unit: '$/day', step: 25, src: 'Finance/HR' },
  { key: 'sp_rate', label: 'SP rate', unit: 'days/SP', step: 0.01, src: 'Jira time logs' },
  { key: 'sp_delivered', label: 'SP delivered', unit: 'story pts', step: 1, src: 'Jira sprint close' },
  { key: 'cfr', label: 'Change failure', unit: '0–1', step: 0.01, src: 'CI/CD + incidents' },
]

function seedForm(inp) {
  const f = {}
  PROD_FIELDS.forEach(({ key }) => { f[key] = inp[key] })
  return f
}
function numericForm(form) {
  const out = {}
  Object.entries(form).forEach(([k, v]) => {
    if (v !== '' && v !== null && v !== undefined && !Number.isNaN(Number(v))) out[k] = Number(v)
  })
  return out
}

function ProductivityPanel({ prod: prodProp, projectId, scenario, query, onApplied, addNotification }) {
  const [prod, setProd] = useState(prodProp)
  const [edit, setEdit] = useState(false)
  const [form, setForm] = useState(() => seedForm(prodProp.inputs))
  const [busy, setBusy] = useState(false)
  const { inputs: inp, results: r, baseline: b, savings: sv, steps, conversion: cv = {} } = prod
  const usd = (n) => `$${Math.round(n).toLocaleString()}`

  // live preview (debounced) while editing
  useEffect(() => {
    if (!edit) return
    const t = setTimeout(async () => {
      try { setProd(await outcomeApi.previewProd(projectId, scenario, numericForm(form))) }
      catch (e) { /* keep last good */ }
    }, 350)
    return () => clearTimeout(t)
  }, [form, edit, projectId, scenario])

  const save = async () => {
    setBusy(true)
    try {
      const dash = await outcomeApi.saveProdInputs(projectId, { ...query }, numericForm(form))
      onApplied(dash); setEdit(false)
      addNotification('Productivity inputs saved — dashboard recomputed', 'success')
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }
  const reset = async () => {
    setBusy(true)
    try {
      const dash = await outcomeApi.resetProdInputs(projectId, scenario)
      onApplied(dash); setEdit(false)
      addNotification('Reset to scenario defaults', 'success')
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }
  const cancel = () => { setProd(prodProp); setForm(seedForm(prodProp.inputs)); setEdit(false) }

  return (
    <div className="card">
      <div className="card-header py-3 flex items-start justify-between gap-3">
        <div>
          <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2">
            <Calculator size={15} className="text-sky-800" /> Productivity Economics — Story Points → Effort → Cost (USD)
          </h3>
          <p className="text-[11px] text-gray-400 mt-0.5">
            {edit ? 'Editing inputs — values recompute live; Save to update KPIs, charts & inferences' :
              <>Capacity {inp.capacity} person-days ({inp.team_size} × {inp.sprint_days}d × {Math.round(inp.utilisation * 100)}% focus) · blended {usd(inp.blended_daily_rate)}/day</>}
          </p>
        </div>
        <button onClick={() => edit ? cancel() : setEdit(true)}
          className="shrink-0 text-xs font-semibold px-2.5 py-1.5 rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 flex items-center gap-1.5">
          {edit ? <><X size={13} /> Cancel</> : <><PenSquare size={13} /> Edit inputs</>}
        </button>
      </div>

      {/* editable inputs */}
      {edit && (
        <div className="px-6 pt-3">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
            {PROD_FIELDS.map(f => (
              <div key={f.key}>
                <label className="block text-[10px] font-semibold text-gray-500 mb-0.5" title={`Source: ${f.src}`}>{f.label}</label>
                <input type="number" step={f.step} className="inp !px-2 !py-1.5 text-sm"
                  value={form[f.key]} onChange={e => setForm(s => ({ ...s, [f.key]: e.target.value }))} />
                <div className="text-[9px] text-gray-400 mt-0.5">
                  {f.unit}
                  {f.key === 'sp_rate' && Number(form.sp_rate) > 0 && ` · ≈ ${(1 / Number(form.sp_rate)).toFixed(2)} SP/pd`}
                </div>
              </div>
            ))}
          </div>
          <div className="flex gap-2 mt-3 pb-1">
            <button onClick={save} disabled={busy} className="btn-primary text-xs flex items-center gap-1.5"><Check size={13} /> Save &amp; recompute</button>
            <button onClick={reset} disabled={busy} className="btn-secondary text-xs">Reset to defaults</button>
            <span className="text-[10px] text-gray-400 self-center">Capacity = team × days × utilisation = {inp.capacity} pd</span>
          </div>
        </div>
      )}

      <div className="card-body py-4 space-y-4">
        {/* 4-step worked chain */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
          {steps.map((s, i) => (
            <div key={s.step} className="relative bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div className="flex items-center gap-1.5 mb-1.5">
                <span className="w-5 h-5 rounded-full bg-sky-500 text-white text-[10px] font-bold flex items-center justify-center">{s.step}</span>
                <span className="text-[11px] font-bold text-gray-700 uppercase tracking-wide">{s.title}</span>
              </div>
              <div className="text-[10.5px] font-mono text-gray-500 leading-tight mb-1.5">{s.formula}</div>
              <div className="text-[11px] text-gray-600 mb-1">{s.substitution}</div>
              <div className="text-lg font-extrabold text-sky-800">{s.result}</div>
              <div className="text-[10px] text-gray-400 mt-1 leading-tight">{s.note}</div>
              {i < steps.length - 1 && (
                <ArrowRight size={16} className="hidden md:block absolute -right-[11px] top-1/2 -translate-y-1/2 text-gray-300 z-10" />
              )}
            </div>
          ))}
        </div>

        {/* SP per person-day & future SP per sprint — current vs revised/new */}
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 bg-blue-50 border border-blue-100 rounded-lg px-3 py-2">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wide text-blue-700">SP / person-day</span>
            <span className="text-sm text-gray-500">{b.productivity_sp_per_pd}</span>
            <ArrowRight size={14} className="text-blue-400" />
            <b className="text-emerald-700 text-base">{r.productivity_sp_per_pd}</b>
            <span className="text-xs font-bold text-emerald-600">+{r.productivity_index - 100}%</span>
          </div>
          <div className="h-5 w-px bg-blue-200" />
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wide text-blue-700">Future SP / sprint</span>
            <span className="text-sm text-gray-500">{b.sp_delivered}</span>
            <ArrowRight size={14} className="text-blue-400" />
            <b className="text-emerald-700 text-base">{inp.sp_delivered}</b>
            <span className="text-xs font-bold text-emerald-600">+{sv.sp_uplift} SP ({sv.sp_uplift_pct}%)</span>
          </div>
          <span className="text-[10px] text-gray-400 ml-auto">same budget · more output · capacity {inp.capacity} pd · quality-adj {r.quality_adjusted_sp_per_pd} SP/pd</span>
        </div>

        {/* before / after + savings */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
          {/* Before vs After */}
          <div className="lg:col-span-2 grid grid-cols-2 gap-3">
            <div className="rounded-lg border border-gray-200 p-3">
              <div className="text-[10px] font-bold uppercase tracking-wide text-gray-400 mb-2">Before AI (baseline)</div>
              <Row label="SP / sprint" value={b.sp_delivered} />
              <Row label="Cost / SP" value={usd(b.cost_per_sp_usd)} />
              <Row label="Productivity" value={`${b.productivity_sp_per_pd} SP/pd`} />
              <Row label="Sprint budget" value={usd(b.sprint_budget_usd)} />
            </div>
            <div className="rounded-lg border-2 border-emerald-200 bg-emerald-50/40 p-3">
              <div className="text-[10px] font-bold uppercase tracking-wide text-emerald-600 mb-2">After AI ({prod.scenario.replace('option-', 'Option ').toUpperCase()})</div>
              <Row label="SP / sprint" value={inp.sp_delivered} good />
              <Row label="Cost / SP" value={usd(r.cost_per_sp_usd)} good />
              <Row label="Productivity" value={`${r.productivity_sp_per_pd} SP/pd`} good />
              <Row label="Quality-adj. (×1−CFR)" value={`${r.quality_adjusted_sp_per_pd} SP/pd`} good />
            </div>
          </div>
          {/* Savings — one reconciled saving, three units */}
          <div className="rounded-lg bg-sky-500 text-white p-3 flex flex-col justify-center">
            <div className="text-[10px] font-bold uppercase tracking-wide text-blue-200 mb-2 flex items-center gap-1">
              <DollarSign size={12} /> Saving to deliver the pre-AI {b.sp_delivered}-SP output
            </div>
            <div className="flex items-center justify-between gap-1 bg-white/5 rounded-lg px-2 py-2">
              <Stat big={`${sv.effort_saved_pd}`} small="person-days" />
              <span className="text-blue-300 font-bold">=</span>
              <Stat big={usd(sv.cost_saved_usd)} small="cost saved" />
              <span className="text-blue-300 font-bold">=</span>
              <Stat big={`${sv.sp_gained}`} small="SP of capacity" />
            </div>
            <div className="grid grid-cols-3 gap-2 mt-2">
              <Stat big={`+${r.productivity_index - 100}%`} small="productivity ↑" />
              <Stat big={`−${usd(sv.saving_per_sp_usd)}`} small="per story point" />
              <Stat big={`${sv.effort_reduction_pct}%`} small="less effort" />
            </div>
            <div className="text-[10px] text-blue-200 mt-2 leading-tight">
              One saving, three units: {sv.effort_saved_pd} pd × {usd(cv.blended_daily_rate)}/day = {usd(sv.cost_saved_usd)};
              {' '}{sv.effort_saved_pd} pd ÷ {cv.sp_rate} d/SP = {sv.sp_gained} SP.
              Current delivery is +{sv.sp_uplift} SP ({sv.sp_uplift_pct}%) above the pre-AI equivalent.
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
function Row({ label, value, good }) {
  return (
    <div className="flex items-center justify-between py-0.5 text-xs">
      <span className="text-gray-500">{label}</span>
      <span className={`font-bold ${good ? 'text-emerald-700' : 'text-gray-700'}`}>{value}</span>
    </div>
  )
}
function Stat({ big, small }) {
  return (
    <div>
      <div className="text-lg font-extrabold leading-none">{big}</div>
      <div className="text-[9.5px] text-blue-200 mt-0.5">{small}</div>
    </div>
  )
}

// ── Progression matrix ───────────────────────────────────────────────────────
function ProgressionMatrix({ rows }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="card">
      <button onClick={() => setOpen(o => !o)} className="w-full card-header py-3 flex items-center justify-between">
        <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Table2 size={15} /> Option A → B → C Progression Matrix</h3>
        <span className="text-xs text-gray-400">{open ? 'Hide' : 'Show'} ({rows.length} metrics)</span>
      </button>
      {open && (
        <div className="card-body py-0 overflow-x-auto">
          <table className="w-full text-xs">
            <thead><tr className="text-left text-gray-400 border-b border-gray-100">
              <th className="py-2 pr-3 font-semibold">Metric</th><th className="py-2 pr-3 font-semibold">Perspective</th>
              <th className="py-2 pr-3 font-semibold text-blue-600">Option A</th><th className="py-2 pr-3 font-semibold text-purple-600">Option B</th>
              <th className="py-2 pr-3 font-semibold text-emerald-600">Option C</th><th className="py-2 pr-3 font-semibold">Source</th>
            </tr></thead>
            <tbody>
              {rows.map(r => (
                <tr key={r.id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-2 pr-3 font-medium text-gray-700" title={r.formula}>{r.metric}</td>
                  <td className="py-2 pr-3 text-gray-400">{r.perspective_label}</td>
                  <td className="py-2 pr-3 text-gray-600">{r.option_a}</td><td className="py-2 pr-3 text-gray-600">{r.option_b}</td>
                  <td className="py-2 pr-3 text-gray-600">{r.option_c}</td><td className="py-2 pr-3 text-gray-400">{r.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// ── Scope (org hierarchy) + granularity level selector ──────────────────────
function ScopeBar({ project, scope, setScope, level, setLevel, rollup }) {
  const groups = project.productGroups || []
  const segments = project.portfolios || []
  const groupObj = groups.find(g => g.name === scope.product_group)
  const products = groupObj?.products || []
  const productObj = products.find(p => p.name === scope.product)
  const teams = (productObj?.teams || []).map(t => (typeof t === 'string' ? t : t.name))

  const set = (patch) => setScope(s => ({ ...s, ...patch }))
  const sel = "px-2.5 py-1.5 border border-gray-300 rounded-lg text-xs text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-sky-400/40 disabled:bg-gray-50 disabled:text-gray-400"

  return (
    <div className="card card-body py-3">
      <div className="flex flex-wrap items-end gap-3">
        <div className="flex items-center gap-1.5 text-gray-500 mr-1"><Filter size={15} /><span className="text-xs font-semibold">Scope</span></div>
        {segments.length > 0 && (
          <Sel label="Segment" value={scope.segment} onChange={v => set({ segment: v })} cls={sel}
               opts={segments} allLabel="All segments" />
        )}
        <Sel label="Product Group" value={scope.product_group} cls={sel}
             onChange={v => set({ product_group: v, product: '', team: '' })}
             opts={groups.map(g => g.name)} allLabel="All groups" />
        <Sel label="Product" value={scope.product} cls={sel} disabled={!scope.product_group}
             onChange={v => set({ product: v, team: '' })}
             opts={products.map(p => p.name)} allLabel="All products" />
        <Sel label="Team" value={scope.team} cls={sel} disabled={!scope.product}
             onChange={v => set({ team: v })} opts={teams} allLabel="All teams" />

        <div className="flex flex-col">
          <label className="text-[10px] font-semibold text-gray-500 mb-1 flex items-center gap-1"><Layers size={11} /> Level</label>
          <div className="flex rounded-lg border border-gray-300 overflow-hidden">
            {[['feature', 'Feature'], ['user-story', 'User Story']].map(([v, l]) => (
              <button key={v} onClick={() => setLevel(v)}
                className={`px-3 py-1.5 text-xs font-semibold ${level === v ? 'bg-sky-500 text-white' : 'bg-white text-gray-500 hover:bg-gray-50'}`}>{l}</button>
            ))}
          </div>
        </div>

        {rollup && (
          <div className="ml-auto text-[11px] text-gray-500 self-center">
            Rolled up across <span className="font-bold text-sky-800">{rollup.teams || rollup.units}</span> team{(rollup.teams || rollup.units) === 1 ? '' : 's'}
            {scope.product_group ? ` in ${scope.team || scope.product || scope.product_group}` : ' (org-wide)'} · {rollup.sp_total} SP total
          </div>
        )}
      </div>
    </div>
  )
}
function Sel({ label, value, onChange, opts, allLabel, cls, disabled }) {
  return (
    <div className="flex flex-col">
      <label className="text-[10px] font-semibold text-gray-500 mb-1">{label}</label>
      <select className={cls} value={value} disabled={disabled} onChange={e => onChange(e.target.value)}>
        <option value="">{allLabel}</option>
        {opts.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────
export default function OutcomeDashboardPage() {
  const { project, activeScenario, setActiveScenario, vsmLevel, setVsmLevel, addNotification } = useApp()
  const [catalog, setCatalog] = useState(null)
  const [dash, setDash] = useState(null)
  const [tab, setTab] = useState('adoption')
  const [loading, setLoading] = useState(false)
  const [showSources, setShowSources] = useState(false)
  const [scope, setScope] = useState({ segment: '', product_group: '', product: '', team: '' })
  const scenario = activeScenario || 'option-a'
  const level = vsmLevel || 'feature'
  const query = { scenario, level, ...scope }
  // Align the A/B/C selector to the configured target/interim steps when present.
  const ts = useTargetScenario(project?.id, setActiveScenario)

  useEffect(() => { outcomeApi.getCatalog().then(setCatalog).catch(() => {}) }, [])
  const metricsById = useMemo(() => {
    const m = {}; (catalog?.metrics || []).forEach(x => { m[x.id] = x }); return m
  }, [catalog])

  const fetchDash = useCallback(async (refresh = false) => {
    if (!project?.id) return
    setLoading(true)
    try {
      const q = { scenario, level, ...scope, ...(refresh ? { refresh: true } : {}) }
      const d = refresh ? await outcomeApi.refresh(project.id, q) : await outcomeApi.getDashboard(project.id, q)
      setDash(d)
      if (refresh) addNotification(`Outcomes refreshed (${d.source_mode})`, 'success')
    } catch (e) { addNotification(e.message, 'error') } finally { setLoading(false) }
  }, [project?.id, scenario, level, scope, addNotification])

  useEffect(() => { fetchDash(false) }, [fetchDash])

  if (!project?.id) {
    return <div className="card card-body text-center text-gray-500 py-16">
      Select or create a project to view outcome monitoring.
    </div>
  }

  const persp = dash?.perspectives?.[tab]
  const modeBadge = { demo: 'bg-gray-100 text-gray-600', live: 'bg-emerald-50 text-emerald-700', mixed: 'bg-cyan-50 text-cyan-700' }

  return (
    <div className="space-y-5 fade-in">
      {/* Hero */}
      <div className="bg-gradient-to-r from-sky-500 to-cyan-500 rounded-2xl p-6 text-white shadow-lg flex items-center justify-between flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-bold">Outcome Dashboard</h2>
          <p className="text-blue-200 text-sm mt-1">Monitor Option A / B / C across AI Adoption · PDLC Performance · AI Ops &amp; Assurance</p>
        </div>
        <div className="flex items-center gap-2">
          {dash && <span className={`text-[11px] font-bold px-2.5 py-1 rounded-full ${modeBadge[dash.source_mode]}`}>
            {dash.source_mode === 'demo' ? 'DEMO DATA' : dash.source_mode === 'live' ? 'LIVE' : 'MIXED (live + demo)'}
          </span>}
          <button onClick={() => setShowSources(true)} className="bg-white/10 hover:bg-white/20 border border-white/20 text-white text-sm font-medium px-3 py-2 rounded-lg flex items-center gap-1.5">
            <Database size={15} /> Data Sources
          </button>
          <button onClick={() => fetchDash(true)} disabled={loading} className="bg-sky-600 hover:bg-sky-700 text-white text-sm font-medium px-3 py-2 rounded-lg flex items-center gap-1.5">
            <RefreshCw size={15} className={loading ? 'animate-spin' : ''} /> Refresh
          </button>
        </div>
      </div>

      <TargetStateBanner />

      {/* Scenario selector — replaced by the configured target steps when set */}
      {ts.configured ? (
        <TargetStepBar steps={ts.steps} stepIdx={ts.stepIdx} pickStep={ts.pickStep} platform={ts.platform}
          onPick={() => fetchDash(true)} />
      ) : (
        <div className="grid grid-cols-3 gap-3">
          {SCEN.map(s => (
            <button key={s.id} onClick={() => setActiveScenario(s.id)}
              className={`text-left p-3 rounded-xl border-2 transition-all ${scenario === s.id ? 'border-sky-600 bg-white shadow-md' : 'border-gray-200 bg-white/60 hover:border-gray-300'}`}>
              <div className="flex items-center justify-between">
                <span className="font-bold text-sky-800">{s.label}</span>
                <span className="w-3 h-3 rounded-full" style={{ background: s.color }} />
              </div>
              <div className="text-xs text-gray-500">{s.sub}</div>
            </button>
          ))}
        </div>
      )}

      {/* Scope + level selector */}
      <ScopeBar project={project} scope={scope} setScope={setScope}
        level={level} setLevel={setVsmLevel} rollup={dash?.scope} />

      {/* Perspective tabs */}
      <div className="flex gap-2 border-b border-gray-200">
        {Object.entries(catalog?.perspectives || { adoption: { label: 'AI Adoption' }, performance: { label: 'PDLC Performance' }, ai_ops: { label: 'AI Ops & Assurance' } }).map(([k, v]) => {
          const Icon = PERSPECTIVE_ICON[k] || Bot
          return (
            <button key={k} onClick={() => setTab(k)}
              className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 -mb-px transition-colors ${tab === k ? 'border-sky-500 text-sky-800' : 'border-transparent text-gray-400 hover:text-gray-600'}`}>
              <Icon size={16} /> {v.label}
            </button>
          )
        })}
      </div>

      {loading && !dash && <div className="card card-body text-center text-gray-400 py-16">Loading outcomes…</div>}

      {persp && (
        <>
          <p className="text-sm text-gray-500 -mt-1">{persp.blurb}</p>
          {/* KPI row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {persp.kpis.map(k => <KpiCard key={k.id} kpi={k} />)}
          </div>
          {/* Productivity economics (Performance tab) */}
          {persp.productivity && (
            <ProductivityPanel key={`${scenario}-${level}-${JSON.stringify(scope)}`} prod={persp.productivity}
              projectId={project.id} scenario={scenario} query={query}
              onApplied={setDash} addNotification={addNotification} />
          )}
          {/* J-Curve / investment assumptions (editable) */}
          {persp.value_trend && (
            <JCurveInputs key={`jc-${scenario}-${level}`} projectId={project.id} scenario={scenario} query={query}
              onApplied={setDash} addNotification={addNotification} />
          )}
          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {persp.charts.map(c => <ChartCard key={c.id} chart={c} meta={metricsById[c.metric_id]} />)}
          </div>
          {/* Inferences */}
          <Inferences key={`${tab}-${scenario}`} items={persp.inferences} engine={dash.inferences_engine}
            custom={persp.inferences_custom} projectId={project.id} scenario={scenario} perspectiveKey={tab}
            onSaved={(pk, listv) => setDash(d => ({ ...d, perspectives: { ...d.perspectives, [pk]: { ...d.perspectives[pk], inferences: listv, inferences_custom: true } } }))}
            onReload={() => fetchDash(false)} addNotification={addNotification} />
        </>
      )}

      {/* Progression matrix */}
      {dash?.progression_matrix && <ProgressionMatrix rows={dash.progression_matrix} />}

      {showSources && (
        <SourceModal projectId={project.id} catalog={catalog} onClose={() => { setShowSources(false); fetchDash(true) }} addNotification={addNotification} />
      )}
    </div>
  )
}
