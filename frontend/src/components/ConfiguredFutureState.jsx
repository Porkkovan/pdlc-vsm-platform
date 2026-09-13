import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Target, Gauge, ArrowRight } from 'lucide-react'
import { targetStateApi } from '../services/api'
import ADLCGrid from './ADLCGrid'

const usd = (n) => `$${Math.round(n || 0).toLocaleString()}`

/**
 * Config-driven Future State view. When a Target State is configured, the future
 * state IS the interim/target steps (replacing generic A/B/C). Each step shows its
 * ADLC composition board, projected metrics, and the full Business Case tabs
 * (cost/ROI, operating model, agents/tools, DevSecOps, AIOps, org/product) populated
 * for the chosen platform + level.
 */
export default function ConfiguredFutureState({ cfg }) {
  const navigate = useNavigate()
  const [roadmap, setRoadmap] = useState(null)
  const [active, setActive] = useState(0)
  const composition = cfg.target_composition || {}

  useEffect(() => {
    targetStateApi.roadmap(cfg.project_id, {
      platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
      interim_count: cfg.interim_count, risk_appetite: cfg.risk_appetite,
    }).then(setRoadmap).catch(() => {})
  }, [cfg])

  if (!roadmap) return <div className="card card-body text-center text-gray-400 py-16">Loading configured future state…</div>
  const steps = roadmap.steps || []
  const step = steps[Math.min(active, steps.length - 1)] || steps[0]

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="text-sm text-gray-600 flex items-center gap-2">
          <Target size={16} className="text-sky-800" />
          Future state driven by <b>{roadmap.platform_name}</b> target · path {steps.map(s => `L${s.level}`).join(' → ')}
        </div>
        <Link to="/target-state" className="text-xs font-semibold text-sky-800 hover:underline">Edit in Target State Studio →</Link>
      </div>

      {/* Step selector */}
      <div className="flex gap-2 flex-wrap">
        {steps.map((s, i) => (
          <button key={s.step} onClick={() => setActive(i)}
            className={`px-3 py-2 rounded-lg text-sm font-semibold border-2 ${i === active ? 'border-sky-600 bg-sky-500 text-white' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>
            {s.is_target ? '★ ' : ''}{s.label} · L{s.level}
          </button>
        ))}
      </div>

      {/* Step posture banner */}
      <div className="card card-body py-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
        <span className="font-bold text-sky-800">L{step.level} · {step.label}</span>
        <span className="text-gray-400">{step.ml_band}</span>
        <span className="text-gray-600">Agents: <b>{step.agent_role}</b></span>
        <span className="text-gray-600">HITL: <b>{step.hitl}</b></span>
        <span className="text-gray-600">{step.automation_pct}% automation</span>
        <span className="text-gray-600">Humans: {step.human_roles_retained.join(', ')}</span>
      </div>

      {/* ADLC composition board */}
      <ADLCGrid agents={composition.agents || []} platformId={cfg.platform}
        title={`${step.label} — ADLC Composition (L${step.level})`} />

      {/* Projected metrics */}
      <div className="card">
        <div className="card-header py-3"><h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Gauge size={15} /> Projected outcome metrics</h3></div>
        <div className="card-body py-3 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {step.metric_band.map(m => (
            <div key={m.id}>
              <div className="text-[11px] text-gray-500">{m.name}</div>
              <div className="text-lg font-extrabold text-sky-800">{m.target}{m.unit === '%' ? '%' : m.unit === '$' ? '' : ''}</div>
              <div className="text-[10px] text-gray-400">{m.unit !== '%' && m.unit !== '$' ? m.unit : ''}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Business case summary (full detail is in the Business Case module) */}
      <div className="card card-body py-3 grid grid-cols-2 md:grid-cols-4 gap-3">
        <Stat label="Step investment" value={usd(step.business_case.step_investment_usd)} />
        <Stat label="Annual benefit" value={usd(step.business_case.annual_benefit_usd)} />
        <Stat label="Timeline" value={`${step.business_case.timeline_weeks} wks`} />
        <Stat label="Progress to target" value={`${step.business_case.cumulative_pct}%`} />
      </div>

      {/* Accept → detailed Business Case module */}
      <div className="flex items-center justify-between flex-wrap gap-2 rounded-xl border border-sky-600/20 bg-sky-500/5 px-4 py-3">
        <div className="text-sm text-gray-600">Accept this future state to open the full, detailed Business Case (cost model, org, tools, DevSecOps, AIOps, playbook & roadmap) for this step.</div>
        <button onClick={() => navigate('/business-case')}
          className="btn-primary text-sm flex items-center gap-1.5">Accept &amp; continue to Business Case <ArrowRight size={15} /></button>
      </div>
    </div>
  )
}

function Stat({ label, value }) {
  return <div className="card p-3"><div className="text-[11px] text-gray-500">{label}</div><div className="text-lg font-extrabold text-sky-800">{value}</div></div>
}
