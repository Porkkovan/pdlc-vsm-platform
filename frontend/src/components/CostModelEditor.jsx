import { useState, useEffect, useMemo } from 'react'
import { projectsApi } from '../services/api'

const CATEGORIES = [
  'People', 'Tools', 'Infrastructure', 'Implementation',
  'Training', 'Change Mgmt', 'LLM Tokens', 'Agent Maint.', 'Platform', 'Other',
]

const fmt = n => n == null ? '—' : '$' + Math.round(Number(n) || 0).toLocaleString()

const COLLECTIONS = {
  current_state_per_pod_annual: { label: 'Current State (Option A) — Per Pod Annual',           target: 'current_state_per_pod_annual' },
  option_b_one_time:            { label: 'Option B — One-Time Migration Cost',                  target: 'option_b_one_time' },
  option_b_ongoing:             { label: 'Option B — Per-Pod Ongoing Annual',                   target: 'option_b_ongoing' },
  option_c_one_time:            { label: 'Option C — One-Time Migration Cost',                  target: 'option_c_one_time' },
  option_c_ongoing:             { label: 'Option C — Per-Pod Ongoing Annual',                   target: 'option_c_ongoing' },
}

// Map model structure paths to the collection-id used in overrides for adding custom lines
const PATH_TO_TARGET = {
  current_state_per_pod_annual: 'current_state_per_pod_annual',
  'option_b.one_time_migration':    'option_b_one_time',
  'option_b.ongoing_per_pod_annual':'option_b_ongoing',
  'option_c.one_time_migration':    'option_c_one_time',
  'option_c.ongoing_per_pod_annual':'option_c_ongoing',
}

function lineMidpoint(line) {
  if (line == null) return 0
  if (line.amount != null) return Number(line.amount) || 0
  return ((Number(line.low) || 0) + (Number(line.high) || 0)) / 2
}

function sumLines(lines) {
  return (lines || []).reduce((acc, l) => acc + lineMidpoint(l), 0)
}

export default function CostModelEditor({ projectId, addNotification }) {
  const [model, setModel]         = useState(null)
  const [tokenOptCatalog, setTokenOptCatalog] = useState([])
  const [overrides, setOverrides] = useState({ lines: {}, token_optimizations: { option_b: [], option_c: [] } })
  const [loading, setLoading]     = useState(false)
  const [saving, setSaving]       = useState(false)
  const [dirty, setDirty]         = useState(false)

  // Load on mount + when project changes
  useEffect(() => {
    if (!projectId) return
    setLoading(true)
    projectsApi.getCostModel(projectId)
      .then(r => {
        setModel(r.cost_model)
        setTokenOptCatalog(r.token_optimizations || [])
        const ov = r.cost_model_overrides && Object.keys(r.cost_model_overrides).length
          ? r.cost_model_overrides
          : { lines: {}, token_optimizations: { option_b: [], option_c: [] } }
        // Ensure shape
        if (!ov.token_optimizations) ov.token_optimizations = { option_b: [], option_c: [] }
        if (!ov.lines)               ov.lines = {}
        setOverrides(ov)
        setDirty(false)
      })
      .finally(() => setLoading(false))
  }, [projectId])

  // Reload effective model from backend when token opts change so reductions render correctly
  useEffect(() => {
    if (!projectId || !overrides.token_optimizations) return
    // Don't refetch on initial mount — only after toggle
    if (!dirty) return
    const id = setTimeout(() => {
      // Local recompute is cheaper than a round-trip — apply on the fly
      // (handled in the `effective` memo below via the token catalog)
    }, 0)
    return () => clearTimeout(id)
  }, [overrides.token_optimizations, projectId, dirty])

  // Recompute the effective model from base + overrides
  const effective = useMemo(() => {
    if (!model) return null
    const next = JSON.parse(JSON.stringify(model))
    if (overrides.fte_loaded_cost_usd != null) next.fte_loaded_cost_usd = overrides.fte_loaded_cost_usd
    if (overrides.pods_in_portfolio != null)   next.pods_in_portfolio   = overrides.pods_in_portfolio

    const lineMap = overrides.lines || {}
    const applyTo = (coll, target) => {
      // Apply patches by id
      const seen = new Set()
      for (let i = coll.length - 1; i >= 0; i--) {
        const line = coll[i]
        const patch = lineMap[line.id]
        if (patch === null) { coll.splice(i, 1); continue }
        if (patch && patch !== '_applied') {
          coll[i] = { ...line, ...patch }
          seen.add(line.id)
        }
      }
      // Add custom lines that target this collection
      for (const [id, patch] of Object.entries(lineMap)) {
        if (!patch || seen.has(id) || coll.find(l => l.id === id)) continue
        if ((patch._collection) === target) {
          const { _collection, ...clean } = patch
          coll.push({ id, editable: true, ...clean })
        }
      }
    }
    applyTo(next.current_state_per_pod_annual,            'current_state_per_pod_annual')
    applyTo(next.option_b.one_time_migration,             'option_b_one_time')
    applyTo(next.option_b.ongoing_per_pod_annual,         'option_b_ongoing')
    applyTo(next.option_c.one_time_migration,             'option_c_one_time')
    applyTo(next.option_c.ongoing_per_pod_annual,         'option_c_ongoing')

    // Apply token optimisations as compounding reductions on the token line.
    // Mirrors backend apply_token_optimizations() so the UI stays in sync.
    const tokOpts = overrides.token_optimizations || { option_b: [], option_c: [] }
    const applyTokOpts = (lines, lineId, scenarioId, enabled) => {
      if (!enabled || enabled.length === 0) return
      const line = lines.find(l => l.id === lineId)
      if (!line) return
      const baseLow  = Number(line.low ?? line.amount ?? 0)
      const baseHigh = Number(line.high ?? line.amount ?? 0)
      let factor = 1.0
      const applied = []
      for (const lid of enabled) {
        const lever = tokenOptCatalog.find(l => l.id === lid)
        if (!lever || !lever.applies_to.includes(scenarioId)) continue
        factor *= (1 - lever.reduction_pct / 100)
        applied.push(lever)
      }
      const effPct = +(100 * (1 - factor)).toFixed(1)
      line.low  = Math.round(baseLow * factor)
      line.high = Math.round(baseHigh * factor)
      delete line.amount
      line.token_optimizations_applied = applied
      line.token_optimizations_effective_reduction_pct = effPct
      line.token_optimizations_baseline = { low: baseLow, high: baseHigh }
      line.label = (line.label || '').split(' — optimisations applied')[0]
                   + ` — optimisations applied (${effPct.toFixed(0)}% reduction)`
    }
    applyTokOpts(next.option_b.ongoing_per_pod_annual, 'b-tokens', 'option-b', tokOpts.option_b)
    applyTokOpts(next.option_c.ongoing_per_pod_annual, 'c-tokens', 'option-c', tokOpts.option_c)
    return next
  }, [model, overrides, tokenOptCatalog])

  // Compute summary on the client (mirrors backend compute_cost_summary)
  const summary = useMemo(() => {
    if (!effective) return null
    const pods = Number(effective.pods_in_portfolio) || 1
    const aPP = sumLines(effective.current_state_per_pod_annual)
    const bOT = sumLines(effective.option_b.one_time_migration)
    const bPP = sumLines(effective.option_b.ongoing_per_pod_annual)
    const cOT = sumLines(effective.option_c.one_time_migration)
    const cPP = sumLines(effective.option_c.ongoing_per_pod_annual)
    const payback = (one, save) => save > 0 ? Number((one / save * 12).toFixed(1)) : -1
    return {
      pods,
      a: { perPod: aPP, portfolio: aPP * pods },
      b: { oneTime: bOT, perPod: bPP, portfolio: bPP * pods,
           savingsPerPod: aPP - bPP, savingsPortfolio: (aPP - bPP) * pods,
           paybackMo: payback(bOT, (aPP - bPP) * pods) },
      c: { oneTime: cOT, perPod: cPP, portfolio: cPP * pods,
           savingsPerPod: aPP - cPP, savingsPortfolio: (aPP - cPP) * pods,
           paybackMo: payback(cOT, (aPP - cPP) * pods) },
    }
  }, [effective])

  // ───────── Edit helpers ─────────
  const patchLine = (id, patch) => {
    setOverrides(prev => {
      const lines = { ...(prev.lines || {}) }
      lines[id] = { ...(lines[id] || {}), ...patch }
      return { ...prev, lines }
    })
    setDirty(true)
  }

  const deleteLine = (id) => {
    setOverrides(prev => ({ ...prev, lines: { ...(prev.lines || {}), [id]: null } }))
    setDirty(true)
  }

  const addLine = (target) => {
    const id = `custom-${target}-${Date.now()}`
    setOverrides(prev => ({
      ...prev,
      lines: { ...(prev.lines || {}), [id]: {
        _collection: target, category: 'Other', label: 'New cost component', amount: 0, editable: true,
      } },
    }))
    setDirty(true)
  }

  const reset = () => {
    setOverrides({ lines: {}, token_optimizations: { option_b: [], option_c: [] } })
    setDirty(true)
  }

  const toggleOpt = (scenarioKey, leverId) => {
    setOverrides(prev => {
      const opts = { ...(prev.token_optimizations || { option_b: [], option_c: [] }) }
      const list = new Set(opts[scenarioKey] || [])
      if (list.has(leverId)) list.delete(leverId); else list.add(leverId)
      opts[scenarioKey] = Array.from(list)
      return { ...prev, token_optimizations: opts }
    })
    setDirty(true)
  }

  const enableAll = (scenarioKey, scenarioId) => {
    const ids = tokenOptCatalog.filter(l => l.applies_to.includes(scenarioId)).map(l => l.id)
    setOverrides(prev => ({ ...prev, token_optimizations: { ...(prev.token_optimizations || {}), [scenarioKey]: ids } }))
    setDirty(true)
  }

  const disableAll = (scenarioKey) => {
    setOverrides(prev => ({ ...prev, token_optimizations: { ...(prev.token_optimizations || {}), [scenarioKey]: [] } }))
    setDirty(true)
  }

  const save = async () => {
    setSaving(true)
    try {
      const r = await projectsApi.putCostModelOverrides(projectId, overrides)
      setModel(r.cost_model)
      setDirty(false)
      addNotification?.({ type: 'success', message: 'Cost model saved' })
    } catch (e) {
      addNotification?.({ type: 'error', message: 'Save failed: ' + (e?.message || 'unknown') })
    } finally {
      setSaving(false)
    }
  }

  if (loading || !effective || !summary) {
    return <div className="p-8 text-center text-gray-500">Loading cost model…</div>
  }

  return (
    <div className="space-y-6">
      {/* Summary ribbon */}
      <div className="rounded-2xl border border-gray-200 overflow-hidden bg-white">
        <div className="bg-emerald-900 px-5 py-4">
          <div className="font-semibold text-white text-lg tracking-tight">Cost Model & ROI — {summary.pods} pod portfolio</div>
          <div className="text-emerald-100 text-xs mt-1">Edit any line, add custom rows, change pod count or loaded-cost. ROI recomputes live.</div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-0 divide-x divide-gray-200">
          <SummaryCard
            title="Today (Option A)"
            tone="gray"
            lines={[
              { label: 'Per pod / year',  value: fmt(summary.a.perPod) },
              { label: 'Portfolio total', value: fmt(summary.a.portfolio) },
            ]}
          />
          <SummaryCard
            title="Option B (Hybrid)"
            tone="purple"
            lines={[
              { label: 'One-time migration',     value: fmt(summary.b.oneTime) },
              { label: 'Ongoing / pod / yr',     value: fmt(summary.b.perPod) },
              { label: 'Annual saving / pod',    value: fmt(summary.b.savingsPerPod), positive: summary.b.savingsPerPod > 0 },
              { label: 'Payback (portfolio)',    value: summary.b.paybackMo > 0 ? `${summary.b.paybackMo} mo` : '—' },
            ]}
          />
          <SummaryCard
            title="Option C (AI-Native)"
            tone="emerald"
            lines={[
              { label: 'One-time migration',     value: fmt(summary.c.oneTime) },
              { label: 'Ongoing / pod / yr',     value: fmt(summary.c.perPod) },
              { label: 'Annual saving / pod',    value: fmt(summary.c.savingsPerPod), positive: summary.c.savingsPerPod > 0 },
              { label: 'Payback (portfolio)',    value: summary.c.paybackMo > 0 ? `${summary.c.paybackMo} mo` : '—' },
            ]}
          />
        </div>
      </div>

      {/* Portfolio settings */}
      <div className="rounded-2xl border border-gray-200 bg-white p-4 flex items-end gap-6">
        <div>
          <label className="text-[11px] font-semibold text-gray-600 uppercase tracking-wide">FTE Loaded Cost</label>
          <div className="flex items-center gap-1 mt-1">
            <span className="text-gray-500">$</span>
            <input
              type="number"
              value={effective.fte_loaded_cost_usd}
              onChange={e => { setOverrides(prev => ({ ...prev, fte_loaded_cost_usd: Number(e.target.value) })); setDirty(true) }}
              className="w-28 px-2 py-1 border border-gray-300 rounded-md text-sm"
            />
            <span className="text-gray-500 text-xs">/ year</span>
          </div>
        </div>
        <div>
          <label className="text-[11px] font-semibold text-gray-600 uppercase tracking-wide">Pods in Portfolio</label>
          <input
            type="number" min="1"
            value={effective.pods_in_portfolio}
            onChange={e => { setOverrides(prev => ({ ...prev, pods_in_portfolio: Math.max(1, Number(e.target.value)) })); setDirty(true) }}
            className="w-20 px-2 py-1 border border-gray-300 rounded-md text-sm mt-1 block"
          />
        </div>
        <div className="ml-auto flex items-center gap-2">
          <button onClick={reset}
            className="text-xs px-3 py-1.5 rounded-md border border-gray-300 text-gray-600 hover:bg-gray-50">
            Reset to defaults
          </button>
          <button onClick={save} disabled={!dirty || saving || !projectId}
            className="text-xs px-4 py-1.5 rounded-md bg-emerald-600 text-white font-semibold hover:bg-emerald-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
            {saving ? 'Saving…' : dirty ? 'Save Changes' : 'Saved'}
          </button>
        </div>
      </div>

      {/* ── Token Optimisation Levers ── */}
      <TokenOptimisationPanel
        catalog={tokenOptCatalog}
        enabledB={overrides.token_optimizations?.option_b || []}
        enabledC={overrides.token_optimizations?.option_c || []}
        baselineB={summary && {
          baseLow:  effective.option_b.ongoing_per_pod_annual.find(l => l.id === 'b-tokens')?.token_optimizations_baseline?.low,
          baseHigh: effective.option_b.ongoing_per_pod_annual.find(l => l.id === 'b-tokens')?.token_optimizations_baseline?.high,
          curLow:   effective.option_b.ongoing_per_pod_annual.find(l => l.id === 'b-tokens')?.low,
          curHigh:  effective.option_b.ongoing_per_pod_annual.find(l => l.id === 'b-tokens')?.high,
        }}
        baselineC={summary && {
          baseLow:  effective.option_c.ongoing_per_pod_annual.find(l => l.id === 'c-tokens')?.token_optimizations_baseline?.low,
          baseHigh: effective.option_c.ongoing_per_pod_annual.find(l => l.id === 'c-tokens')?.token_optimizations_baseline?.high,
          curLow:   effective.option_c.ongoing_per_pod_annual.find(l => l.id === 'c-tokens')?.low,
          curHigh:  effective.option_c.ongoing_per_pod_annual.find(l => l.id === 'c-tokens')?.high,
        }}
        onToggle={toggleOpt}
        onEnableAll={enableAll}
        onDisableAll={disableAll}
      />

      {/* Five editable tables */}
      <CostTable title="Current State (Option A) — Per Pod / Year" tone="gray"
        lines={effective.current_state_per_pod_annual} target="current_state_per_pod_annual"
        onPatch={patchLine} onDelete={deleteLine} onAdd={addLine} />

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <CostTable title="Option B — One-Time Migration Cost" tone="purple"
          lines={effective.option_b.one_time_migration} target="option_b_one_time"
          onPatch={patchLine} onDelete={deleteLine} onAdd={addLine} />
        <CostTable title="Option B — Ongoing / Pod / Year" tone="purple"
          lines={effective.option_b.ongoing_per_pod_annual} target="option_b_ongoing"
          onPatch={patchLine} onDelete={deleteLine} onAdd={addLine} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <CostTable title="Option C — One-Time Migration Cost" tone="emerald"
          lines={effective.option_c.one_time_migration} target="option_c_one_time"
          onPatch={patchLine} onDelete={deleteLine} onAdd={addLine} />
        <CostTable title="Option C — Ongoing / Pod / Year" tone="emerald"
          lines={effective.option_c.ongoing_per_pod_annual} target="option_c_ongoing"
          onPatch={patchLine} onDelete={deleteLine} onAdd={addLine} />
      </div>
    </div>
  )
}

// ─── Sub-components ────────────────────────────────────────────────────────

function SummaryCard({ title, tone, lines }) {
  const head = {
    gray:    'bg-gray-50 text-gray-700',
    purple:  'bg-purple-50 text-purple-800',
    emerald: 'bg-emerald-50 text-emerald-800',
  }[tone] || 'bg-gray-50 text-gray-700'
  return (
    <div className="p-4">
      <div className={`text-[11px] font-bold uppercase tracking-wide rounded-md px-2 py-1 inline-block mb-3 ${head}`}>{title}</div>
      <div className="space-y-1.5">
        {lines.map((l, i) => (
          <div key={i} className="flex items-baseline justify-between text-xs">
            <span className="text-gray-500">{l.label}</span>
            <span className={`font-bold tabular-nums ${l.positive ? 'text-emerald-700' : 'text-gray-900'}`}>{l.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function TokenOptimisationPanel({ catalog, enabledB, enabledC, baselineB, baselineC, onToggle, onEnableAll, onDisableAll }) {
  if (!catalog || catalog.length === 0) return null
  const leversForB = catalog.filter(l => l.applies_to.includes('option-b'))
  const leversForC = catalog.filter(l => l.applies_to.includes('option-c'))

  const renderSavings = (b) => {
    if (!b || b.baseLow == null) return null
    const baseMid = (b.baseLow + b.baseHigh) / 2
    const curMid = (b.curLow + b.curHigh) / 2
    const pct = baseMid > 0 ? Math.round((1 - curMid / baseMid) * 100) : 0
    return (
      <div className="text-[11px] text-gray-600 mt-1">
        <span className="tabular-nums">{fmt(b.baseLow)}–{fmt(b.baseHigh)}</span>
        <span className="mx-1.5 text-gray-400">→</span>
        <span className="font-bold text-emerald-700 tabular-nums">{fmt(b.curLow)}–{fmt(b.curHigh)}</span>
        <span className="ml-2 inline-block bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full text-[10px] font-bold">{pct}% saved</span>
      </div>
    )
  }

  return (
    <div className="rounded-2xl border border-gray-200 bg-white overflow-hidden">
      <div className="bg-cyan-500 px-5 py-4">
        <div className="font-semibold text-white text-lg tracking-tight">Token Optimisation Levers</div>
        <div className="text-cyan-100 text-xs mt-1">Toggle techniques to compound LLM-token reductions on Options B and C. ROI updates live.</div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-gray-200">
        {/* Option B panel */}
        <div className="p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-bold text-purple-800">Option B — token line</div>
            <div className="flex gap-2">
              <button onClick={() => onEnableAll('option_b', 'option-b')} className="text-[10px] text-purple-700 hover:underline">Enable all</button>
              <span className="text-gray-300">·</span>
              <button onClick={() => onDisableAll('option_b')} className="text-[10px] text-gray-500 hover:underline">Disable all</button>
            </div>
          </div>
          {renderSavings(baselineB)}
          <div className="mt-3 space-y-1.5">
            {leversForB.map(l => {
              const checked = enabledB.includes(l.id)
              return (
                <label key={l.id} className={`flex items-start gap-2 p-2 rounded-md cursor-pointer transition-colors ${checked ? 'bg-purple-50 border border-purple-200' : 'border border-transparent hover:bg-gray-50'}`}>
                  <input type="checkbox" checked={checked} onChange={() => onToggle('option_b', l.id)} className="mt-0.5" />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-gray-900">{l.name}</span>
                      <span className="text-[10px] font-bold text-emerald-700">−{l.reduction_pct}%</span>
                      <span className={`text-[9px] px-1.5 py-0.5 rounded-full ${l.effort === 'Low' ? 'bg-green-100 text-green-700' : l.effort === 'Medium' ? 'bg-cyan-100 text-cyan-700' : l.effort === 'High' ? 'bg-teal-100 text-teal-700' : 'bg-sky-100 text-sky-700'}`}>{l.effort}</span>
                    </div>
                    <div className="text-[10.5px] text-gray-600 leading-tight mt-0.5">{l.description}</div>
                  </div>
                </label>
              )
            })}
          </div>
        </div>
        {/* Option C panel */}
        <div className="p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-bold text-emerald-800">Option C — token line</div>
            <div className="flex gap-2">
              <button onClick={() => onEnableAll('option_c', 'option-c')} className="text-[10px] text-emerald-700 hover:underline">Enable all</button>
              <span className="text-gray-300">·</span>
              <button onClick={() => onDisableAll('option_c')} className="text-[10px] text-gray-500 hover:underline">Disable all</button>
            </div>
          </div>
          {renderSavings(baselineC)}
          <div className="mt-3 space-y-1.5">
            {leversForC.map(l => {
              const checked = enabledC.includes(l.id)
              return (
                <label key={l.id} className={`flex items-start gap-2 p-2 rounded-md cursor-pointer transition-colors ${checked ? 'bg-emerald-50 border border-emerald-200' : 'border border-transparent hover:bg-gray-50'}`}>
                  <input type="checkbox" checked={checked} onChange={() => onToggle('option_c', l.id)} className="mt-0.5" />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-gray-900">{l.name}</span>
                      <span className="text-[10px] font-bold text-emerald-700">−{l.reduction_pct}%</span>
                      <span className={`text-[9px] px-1.5 py-0.5 rounded-full ${l.effort === 'Low' ? 'bg-green-100 text-green-700' : l.effort === 'Medium' ? 'bg-cyan-100 text-cyan-700' : l.effort === 'High' ? 'bg-teal-100 text-teal-700' : 'bg-sky-100 text-sky-700'}`}>{l.effort}</span>
                    </div>
                    <div className="text-[10.5px] text-gray-600 leading-tight mt-0.5">{l.description}</div>
                  </div>
                </label>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}

function CostTable({ title, tone, lines, target, onPatch, onDelete, onAdd }) {
  const head = {
    gray:    'bg-gray-100 text-gray-800',
    purple:  'bg-purple-100 text-purple-900',
    emerald: 'bg-emerald-100 text-emerald-900',
  }[tone] || 'bg-gray-100 text-gray-800'
  const total = sumLines(lines)
  return (
    <div className="rounded-2xl border border-gray-200 bg-white overflow-hidden">
      <div className={`px-4 py-3 flex items-center justify-between ${head}`}>
        <div className="text-sm font-semibold">{title}</div>
        <div className="text-xs tabular-nums font-bold">Σ {fmt(total)}</div>
      </div>
      <table className="w-full text-xs">
        <thead className="bg-gray-50 border-b border-gray-200 text-[10px] uppercase tracking-wide text-gray-500">
          <tr>
            <th className="px-3 py-2 text-left w-32">Category</th>
            <th className="px-3 py-2 text-left">Label</th>
            <th className="px-3 py-2 text-right w-28">Low / Amount</th>
            <th className="px-3 py-2 text-right w-28">High</th>
            <th className="w-8"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {lines.map(line => {
            const hasRange = line.low != null || line.high != null
            return (
              <tr key={line.id} className="hover:bg-gray-50">
                <td className="px-3 py-2">
                  <select value={line.category || 'Other'} onChange={e => onPatch(line.id, { category: e.target.value })}
                    className="w-full text-xs border border-gray-200 rounded px-1.5 py-1 bg-white">
                    {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </td>
                <td className="px-3 py-2">
                  <input type="text" value={line.label || ''}
                    onChange={e => onPatch(line.id, { label: e.target.value })}
                    className="w-full text-xs border border-gray-200 rounded px-2 py-1" />
                </td>
                <td className="px-3 py-2">
                  <input type="number" value={hasRange ? (line.low ?? '') : (line.amount ?? '')}
                    onChange={e => {
                      const v = e.target.value === '' ? 0 : Number(e.target.value)
                      if (hasRange) onPatch(line.id, { low: v }); else onPatch(line.id, { amount: v })
                    }}
                    className="w-full text-xs border border-gray-200 rounded px-2 py-1 text-right tabular-nums" />
                </td>
                <td className="px-3 py-2">
                  <input type="number" value={line.high ?? ''} placeholder={hasRange ? '' : '— flat —'}
                    onChange={e => {
                      const v = e.target.value
                      if (v === '') {
                        // Collapsing range to flat — promote low to amount
                        const lo = line.low ?? line.amount ?? 0
                        onPatch(line.id, { amount: lo, low: undefined, high: undefined })
                      } else {
                        const lo = line.low ?? line.amount ?? 0
                        onPatch(line.id, { low: lo, high: Number(v), amount: undefined })
                      }
                    }}
                    className="w-full text-xs border border-gray-200 rounded px-2 py-1 text-right tabular-nums disabled:bg-gray-50"
                    disabled={!hasRange && line.amount != null && false} />
                </td>
                <td className="px-2 py-2 text-center">
                  <button onClick={() => onDelete(line.id)} title="Remove"
                    className="text-sky-400 hover:text-sky-600 text-xs">×</button>
                </td>
              </tr>
            )
          })}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan={5} className="px-3 py-2 bg-gray-50">
              <button onClick={() => onAdd(target)}
                className="text-xs text-blue-600 hover:text-blue-800 font-medium">+ Add cost component</button>
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  )
}
