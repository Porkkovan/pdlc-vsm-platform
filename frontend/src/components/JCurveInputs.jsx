import { useEffect, useState, useCallback } from 'react'
import { Calculator, Check, PenSquare, X, TrendingUp } from 'lucide-react'
import { outcomeApi } from '../services/api'

const usd = (n) => `$${Math.round(n || 0).toLocaleString()}`

/**
 * Editable DORA J-Curve / investment assumptions (cost-only). Lets the user tune
 * token/dev, licence, training, infra, J-Curve drop/duration, adoption ramp and
 * pods-shared, with a live preview of breakeven/ROI/ongoing cost. Save recomputes
 * the whole dashboard; Reset reverts to platform defaults.
 */
export default function JCurveInputs({ projectId, scenario, query, onApplied, addNotification }) {
  const [meta, setMeta] = useState([])
  const [platform, setPlatform] = useState('')
  const [form, setForm] = useState(null)
  const [preview, setPreview] = useState(null)
  const [edit, setEdit] = useState(false)
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => {
    outcomeApi.getJcurveInputs(projectId, scenario).then(d => {
      setMeta(d.field_meta); setPlatform(d.platform)
      setForm({ ...d.effective })
    }).catch(() => {})
  }, [projectId, scenario])
  useEffect(() => { load() }, [load])

  // live preview while editing
  useEffect(() => {
    if (!edit || !form) return
    const t = setTimeout(() => {
      outcomeApi.previewJcurve(projectId, scenario, numeric(form)).then(setPreview).catch(() => {})
    }, 350)
    return () => clearTimeout(t)
  }, [form, edit, projectId, scenario])

  const save = async () => {
    setBusy(true)
    try {
      const dash = await outcomeApi.saveJcurve(projectId, { ...query }, numeric(form))
      onApplied(dash); setEdit(false)
      addNotification('J-Curve assumptions saved — dashboard recomputed', 'success')
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }
  const reset = async () => {
    setBusy(true)
    try { const dash = await outcomeApi.resetJcurve(projectId, scenario); onApplied(dash); setEdit(false); load()
      addNotification('Reset to platform defaults', 'success') }
    catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }

  if (!form) return null
  const t = edit ? preview : null

  return (
    <div className="card">
      <div className="card-header py-3 flex items-center justify-between">
        <div>
          <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2">
            <Calculator size={15} className="text-sky-700" /> J-Curve &amp; Investment Assumptions
          </h3>
          <p className="text-[11px] text-gray-400 mt-0.5">Cost-only (excl. feature revenue) · ongoing cost incl. agent/token · platform: <b>{(platform || '').replace('_', ' ')}</b></p>
        </div>
        <button onClick={() => setEdit(e => !e)} className="text-xs font-semibold px-2.5 py-1.5 rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 flex items-center gap-1.5">
          {edit ? <><X size={13} /> Cancel</> : <><PenSquare size={13} /> Edit assumptions</>}
        </button>
      </div>

      {edit && (
        <div className="px-6 pt-3">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {meta.map(f => (
              <div key={f.key}>
                <label className="block text-[10px] font-semibold text-gray-500 mb-0.5" title={`Source: ${f.source}`}>{f.label}</label>
                <input type="number" step={f.step} className="inp !px-2 !py-1.5 text-sm"
                  value={form[f.key] ?? ''} onChange={e => setForm(s => ({ ...s, [f.key]: e.target.value }))} />
                <div className="text-[9px] text-gray-400 mt-0.5">{f.unit}</div>
              </div>
            ))}
          </div>
          {t && (
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-3 text-xs bg-sky-50 border border-sky-100 rounded-lg px-3 py-2">
              <span className="font-bold text-sky-800 flex items-center gap-1"><TrendingUp size={13} /> Live preview</span>
              <span>Ongoing <b>{usd(t.tool_cost_per_sprint_usd)}</b>/sprint (token {usd(t.ongoing_cost_breakdown.token_agent_usd)} · ops {t.ongoing_cost_breakdown.ops_fte}FTE)</span>
              <span>Breakeven <b>{t.breakeven_sprint ? `sprint ${t.breakeven_sprint}` : 'none in horizon'}</b></span>
              <span>ROI <b>{t.roi_pct}%</b></span>
              <span className="text-gray-400">one-time {usd(t.one_time_investment_usd)} · J-curve cost {usd(t.jcurve_cost_total_usd)}</span>
            </div>
          )}
          <div className="flex gap-2 mt-3 pb-1">
            <button onClick={save} disabled={busy} className="btn-primary text-xs flex items-center gap-1.5"><Check size={13} /> Save &amp; recompute</button>
            <button onClick={reset} disabled={busy} className="btn-secondary text-xs">Reset to platform defaults</button>
          </div>
        </div>
      )}
    </div>
  )
}

function numeric(form) {
  const out = {}
  Object.entries(form).forEach(([k, v]) => {
    if (v !== '' && v !== null && v !== undefined && !Number.isNaN(Number(v))) out[k] = Number(v)
  })
  return out
}
