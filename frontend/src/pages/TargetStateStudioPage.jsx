import { useEffect, useState, useMemo, useCallback, useRef } from 'react'
import {
  Rocket, Server, Boxes, Building2, Check, ChevronLeft, ChevronRight, Bot,
  Users, Wrench, Layers, Map, DollarSign, Gauge, Plus, Trash2, Target, Save,
  ChevronDown, ChevronUp, Cpu, ArrowRight, Eye, Briefcase,
} from 'lucide-react'
import { useApp } from '../contexts/AppContext'
import { targetStateApi } from '../services/api'
import { seedAdlcAgents, seedAgentsForPlatform } from '../data/adlcTargetState'
import ADLCGrid from '../components/ADLCGrid'
import StepReviewBar from '../components/StepReviewBar'

const KIND_BADGE = {
  home_grown: { label: 'Home-grown', cls: 'bg-gray-700 text-white' },
  cots: { label: 'COTS', cls: 'bg-indigo-600 text-white' },
  service_provider: { label: 'Service provider', cls: 'bg-cyan-600 text-white' },
}
const ROLE_POSTURE = ['assistant', 'independent', 'orchestrated']
const STEPS = [
  { n: 1, label: 'Platform', icon: Server },
  { n: 2, label: 'Compose target', icon: Boxes },
  { n: 3, label: 'Path', icon: Map },
  { n: 4, label: 'Review & generate', icon: Rocket },
]
const usd = (n) => `$${Math.round(n || 0).toLocaleString()}`

const LEVEL_POSTURE_MAP = {
  1: { default: 'assistant',    mix: { assistant: 1.0 } },
  2: { default: 'assistant',    mix: { assistant: 0.7, independent: 0.3 } },
  3: { default: 'independent',  mix: { assistant: 0.2, independent: 0.6, orchestrated: 0.2 } },
  4: { default: 'orchestrated', mix: { independent: 0.3, orchestrated: 0.7 } },
  5: { default: 'orchestrated', mix: { orchestrated: 1.0 } },
}

// Seed editable composition from the US Bank AI-Native ADLC target grid.
const seedAgents = seedAdlcAgents

// Mirror the backend's interim-stop spacing (roadmap.py _stop_levels).
function computeStops(current, target, count) {
  const avail = []
  for (let l = current + 1; l < target; l++) avail.push(l)
  const k = Math.max(0, Math.min(count ?? 0, avail.length))
  const picks = new Set()
  for (let i = 0; i < k; i++) picks.add(avail[Math.min(avail.length - 1, Math.floor((i + 0.5) * avail.length / k))])
  return [...picks].sort((a, b) => a - b).concat([target])
}

export default function TargetStateStudioPage() {
  const { project, addNotification } = useApp()
  const [step, setStep] = useState(1)
  const [platforms, setPlatforms] = useState([])
  const [ladder, setLadder] = useState([])
  const [risks, setRisks] = useState([])
  const [roadmap, setRoadmap] = useState(null)
  const [progress, setProgress] = useState(null)
  const [currentState, setCurrentState] = useState(null)
  const [suggestionCount, setSuggestionCount] = useState(null)
  const [loaded, setLoaded] = useState(false)
  const [busy, setBusy] = useState(false)

  const [cfg, setCfg] = useState({
    platform: 'homegrown', current_level: 0, target_level: 5,
    interim_count: null, risk_appetite: 'medium', maturity_band: 'WALK',
    composition: { agents: [], human_roles: [], tools: [] },
  })

  useEffect(() => {
    targetStateApi.getPlatforms().then(d => setPlatforms(d.platforms)).catch(() => {})
    targetStateApi.getLadder().then(d => { setLadder(d.ladder); setRisks(d.risk_appetite) }).catch(() => {})
  }, [])

  // Load saved config (if any) for this project
  useEffect(() => {
    if (!project?.id) return
    targetStateApi.getConfig(project.id).then(d => {
      if (d && d.configured !== false) {
        setCfg(c => ({
          ...c, platform: d.platform || c.platform,
          current_level: d.current_level ?? c.current_level,
          target_level: d.target_level ?? c.target_level,
          interim_count: d.interim_count ?? c.interim_count,
          risk_appetite: d.risk_appetite || c.risk_appetite,
          composition: {
            agents: d.target_composition?.agents?.length ? d.target_composition.agents : seedAgents(),
            human_roles: d.target_composition?.human_roles || [],
            tools: d.target_composition?.tools || [],
          },
        }))
      } else {
        setCfg(c => ({ ...c, composition: { ...c.composition, agents: seedAgents() } }))
      }
    }).catch(() => setCfg(c => ({ ...c, composition: { ...c.composition, agents: seedAgents() } })))
      .finally(() => setLoaded(true))
    // Auto-populate current level + maturity band from the Current-State VSM analysis.
    targetStateApi.currentState(project.id).then(cs => {
      setCurrentState(cs)
      setCfg(c => ({ ...c, current_level: cs.current_level ?? c.current_level, maturity_band: cs.maturity_band || c.maturity_band }))
    }).catch(() => {})
  }, [project?.id])

  // Keep the auto-suggested interim count current (drives Auto mode + autosave).
  useEffect(() => {
    if (!project?.id) return
    targetStateApi.roadmap(project.id, {
      platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
      interim_count: null, risk_appetite: cfg.risk_appetite, maturity_band: cfg.maturity_band,
    }).then(rm => setSuggestionCount(rm.suggestion?.interim_count ?? 0)).catch(() => {})
  }, [project?.id, cfg.platform, cfg.current_level, cfg.target_level, cfg.risk_appetite, cfg.maturity_band])

  // Effective interim count (Auto → suggestion) and the resulting stop levels.
  const effCount = cfg.interim_count == null ? (suggestionCount ?? 0) : cfg.interim_count
  const stops = computeStops(cfg.current_level, cfg.target_level, effCount)

  // Autosave (debounced) so Future State / Business Case reflect edits without an
  // explicit Save click. Persists composition, platform, levels and computed stops.
  useEffect(() => {
    if (!loaded || !project?.id) return
    const t = setTimeout(() => {
      targetStateApi.saveConfig(project.id, {
        platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
        interim_count: effCount, interim_levels: stops, risk_appetite: cfg.risk_appetite,
        target_composition: { agents: cfg.composition.agents, human_roles: cfg.composition.human_roles, tools: cfg.composition.tools },
      }).catch(() => {})
    }, 700)
    return () => clearTimeout(t)
  }, [loaded, project?.id, cfg.platform, cfg.current_level, cfg.target_level, effCount,
      cfg.risk_appetite, JSON.stringify(stops), JSON.stringify(cfg.composition)]) // eslint-disable-line

  // Seed human roles + tools from ladder target level + agent tools when entering compose
  const ladderTarget = useMemo(() => ladder.find(l => l.level === cfg.target_level), [ladder, cfg.target_level])
  useEffect(() => {
    setCfg(c => {
      if (c.composition.human_roles.length || !ladderTarget) return c
      const tools = [...new Set(c.composition.agents.map(a => a.tool).filter(Boolean))]
      return { ...c, composition: { ...c.composition, human_roles: [...ladderTarget.human_roles_retained], tools } }
    })
  }, [ladderTarget]) // eslint-disable-line

  // Reseed agents when platform changes (not on initial load where saved composition is preserved)
  const prevPlatformRef = useRef(null)
  useEffect(() => {
    if (!loaded) return
    if (prevPlatformRef.current !== null && prevPlatformRef.current !== cfg.platform) {
      targetStateApi.platformInsight(cfg.platform).then(insight => {
        const newAgents = seedAgentsForPlatform(cfg.platform, insight?.agents)
        setCfg(c => ({
          ...c,
          composition: { ...c.composition, agents: newAgents },
        }))
      }).catch(() => {})
    }
    prevPlatformRef.current = cfg.platform
  }, [cfg.platform, loaded]) // eslint-disable-line

  // Auto-adjust agent postures based on target level
  const prevTargetLevelRef = useRef(null)
  useEffect(() => {
    if (!loaded) return
    if (prevTargetLevelRef.current !== null && prevTargetLevelRef.current !== cfg.target_level) {
      const levelCfg = LEVEL_POSTURE_MAP[cfg.target_level] || LEVEL_POSTURE_MAP[5]
      const postures = Object.keys(levelCfg.mix)
      const weights = Object.values(levelCfg.mix)
      setCfg(c => ({
        ...c,
        composition: {
          ...c.composition,
          agents: c.composition.agents.map((a, i) => {
            let cumulative = 0
            const ratio = i / Math.max(c.composition.agents.length, 1)
            let posture = levelCfg.default
            for (let j = 0; j < postures.length; j++) {
              cumulative += weights[j]
              if (ratio < cumulative) { posture = postures[j]; break }
            }
            return { ...a, role_posture: posture }
          }),
        },
      }))
    }
    prevTargetLevelRef.current = cfg.target_level
  }, [cfg.target_level, loaded]) // eslint-disable-line

  const selPlatform = platforms.find(p => p.id === cfg.platform)

  const genRoadmap = useCallback(async () => {
    if (!project?.id) return
    setBusy(true)
    try {
      const rm = await targetStateApi.roadmap(project.id, {
        platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
        interim_count: cfg.interim_count, risk_appetite: cfg.risk_appetite, maturity_band: cfg.maturity_band,
      })
      setRoadmap(rm)
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }, [project?.id, cfg, addNotification])

  useEffect(() => { if (step === 4) genRoadmap() }, [step]) // eslint-disable-line

  const save = async () => {
    setBusy(true)
    try {
      const stops = roadmap?.stops || []
      const saved = await targetStateApi.saveConfig(project.id, {
        platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
        interim_count: roadmap?.interim_count ?? cfg.interim_count ?? 0,
        interim_levels: stops, risk_appetite: cfg.risk_appetite,
        target_composition: { agents: cfg.composition.agents, human_roles: cfg.composition.human_roles, tools: cfg.composition.tools },
      })
      addNotification('Target state saved — Future State, Business Case & Outcome Dashboard will reflect it', 'success')
      const p = await targetStateApi.progress(project.id); setProgress(p)
    } catch (e) { addNotification(e.message, 'error') } finally { setBusy(false) }
  }

  if (!project?.id) {
    return <div className="card card-body text-center text-gray-500 py-16">Select or create a project to define a target state.</div>
  }

  return (
    <div className="space-y-5 fade-in">
      {/* Hero */}
      <div className="bg-gradient-to-r from-sky-500 to-cyan-500 rounded-2xl p-6 text-white shadow-lg">
        <h2 className="text-2xl font-bold flex items-center gap-2"><Target size={22} /> Target State Studio</h2>
        <p className="text-blue-200 text-sm mt-1">Define your North-Star ADLC state, choose how to get there, and generate the operating model, agents/tools, business case & progress.</p>
      </div>

      <StepReviewBar stepKey="target_state" stepLabel="Target State Studio" />

      {/* Stepper */}
      <div className="flex items-center gap-1">
        {STEPS.map((s, i) => (
          <div key={s.n} className="flex items-center flex-1">
            <button onClick={() => setStep(s.n)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold w-full justify-center transition-colors ${
                step === s.n ? 'bg-sky-500 text-white' : step > s.n ? 'bg-emerald-50 text-emerald-700' : 'bg-white text-gray-400 border border-gray-200'}`}>
              {step > s.n ? <Check size={15} /> : <s.icon size={15} />}<span className="hidden md:inline">{s.n}. {s.label}</span>
            </button>
            {i < STEPS.length - 1 && <ChevronRight size={16} className="text-gray-300 shrink-0" />}
          </div>
        ))}
      </div>

      {step === 1 && <StepPlatform platforms={platforms} selected={cfg.platform} riskAppetite={cfg.risk_appetite} onSelect={p => setCfg(c => ({ ...c, platform: p }))} />}
      {step === 2 && <StepCompose cfg={cfg} setCfg={setCfg} platform={selPlatform} />}
      {step === 3 && <StepPath cfg={cfg} setCfg={setCfg} ladder={ladder} risks={risks} projectId={project.id} currentState={currentState} />}
      {step === 4 && <StepReview roadmap={roadmap} busy={busy} progress={progress} onSave={save} platform={selPlatform} composition={cfg.composition} />}

      {/* Nav */}
      <div className="flex justify-between">
        <button disabled={step === 1} onClick={() => setStep(s => s - 1)}
          className="btn-secondary text-sm flex items-center gap-1 disabled:opacity-40"><ChevronLeft size={15} /> Back</button>
        {step < 4
          ? <button onClick={() => setStep(s => s + 1)} className="btn-navy text-sm flex items-center gap-1">Next <ChevronRight size={15} /></button>
          : <button onClick={save} disabled={busy} className="btn-primary text-sm flex items-center gap-1"><Save size={15} /> Save target state</button>}
      </div>
    </div>
  )
}

// ── Step 1: Platform ──────────────────────────────────────────────────────────
function StepPlatform({ platforms, selected, onSelect, riskAppetite }) {
  const [cmp, setCmp] = useState(null)
  useEffect(() => { targetStateApi.compare(riskAppetite).then(setCmp).catch(() => {}) }, [riskAppetite])

  const sel = (cmp?.platforms || []).find(p => p.id === selected)
  const ids = (cmp?.platforms || []).map(p => p.id)
  const rec = cmp?.recommendation

  const dots = (v) => (
    <span className="inline-flex gap-0.5">
      {[1, 2, 3, 4, 5].map(i => <span key={i} className={`w-1.5 h-1.5 rounded-full ${i <= v ? 'bg-sky-500' : 'bg-gray-200'}`} />)}
    </span>
  )

  return (
    <div className="space-y-4">
      {/* Platform cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {platforms.map(p => {
          const badge = KIND_BADGE[p.kind] || KIND_BADGE.cots
          const on = selected === p.id
          const isRec = rec?.platform === p.id
          return (
            <button key={p.id} onClick={() => onSelect(p.id)}
              className={`text-left card p-4 border-2 transition-all ${on ? 'border-sky-600 shadow-md' : 'border-transparent hover:border-gray-200'}`}>
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-sky-800">{p.name}</span>
                <div className="flex items-center gap-1">
                  {isRec && <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-600 text-white">★ Recommended</span>}
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${badge.cls}`}>{badge.label}</span>
                </div>
              </div>
              {p.is_us_bank_target && <span className="badge-green !py-0 mb-1 inline-block">US Bank target state</span>}
              <p className="text-xs text-gray-500 mb-2">{p.tagline}</p>
              <div className="flex flex-wrap gap-x-4 gap-y-0.5 text-[11px] text-gray-500">
                <span>⏱ {p.production_ready_weeks} wks to prod</span>
                <span>💲 {p.investment_delta_text?.split('.')[0] || 'baseline'}</span>
              </div>
            </button>
          )
        })}
      </div>

      {/* Recommendation */}
      {rec && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50/50 px-4 py-3">
          <div className="text-sm font-bold text-emerald-800 flex items-center gap-2">★ Recommended: {rec.name} <span className="text-emerald-600 font-normal">({rec.overall}/100)</span></div>
          <p className="text-xs text-gray-600 mt-1">{rec.rationale}</p>
          <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2 text-[11px] text-gray-500">
            <span>Fastest value: <b className="text-gray-700">{rec.best_for?.fastest_value}</b></span>
            <span>Max control: <b className="text-gray-700">{rec.best_for?.max_control}</b></span>
            <span>Lowest in-house burden: <b className="text-gray-700">{rec.best_for?.lowest_burden}</b></span>
          </div>
          <div className="text-[10px] text-gray-400 mt-1">Ranking reflects a <b>{cmp.risk_appetite}</b>-risk appetite (set in step 3) — it re-weights toward control/compliance for low risk and speed/low-burden for high risk.</div>
        </div>
      )}

      {/* Comparison matrix */}
      {cmp && (
        <div className="card overflow-hidden">
          <div className="card-header py-3"><h3 className="font-bold text-gray-800 text-sm">Platform comparison — parameters × options</h3></div>
          <div className="overflow-x-auto">
            <table className="w-full text-xs min-w-[760px]">
              <thead>
                <tr className="text-left text-gray-400 border-b border-gray-100">
                  <th className="py-2 px-3 font-semibold">Parameter</th>
                  {cmp.platforms.map(p => (
                    <th key={p.id} className={`py-2 px-2 font-semibold text-center ${p.id === selected ? 'bg-sky-500/5 text-sky-800' : ''}`}>
                      {p.name.split(' ')[0].split('/')[0]}{p.id === selected && ' ◀'}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {cmp.matrix.map(row => (
                  <tr key={row.key} className="border-b border-gray-50">
                    <td className="py-2 px-3 text-gray-600">{row.label} <span className="text-gray-300">·{row.weight}%</span></td>
                    {ids.map(pid => (
                      <td key={pid} className={`py-2 px-2 text-center ${pid === selected ? 'bg-sky-500/5' : ''}`}>{dots(row.values[pid])}</td>
                    ))}
                  </tr>
                ))}
                <tr className="border-t-2 border-gray-200 font-bold">
                  <td className="py-2 px-3 text-gray-700">Overall score</td>
                  {cmp.platforms.map(p => (
                    <td key={p.id} className={`py-2 px-2 text-center ${p.id === selected ? 'bg-sky-500/5 text-sky-800' : 'text-gray-700'}`}>{p.overall}<span className="text-[9px] text-gray-400"> #{p.rank}</span></td>
                  ))}
                </tr>
                <tr className="text-gray-500">
                  <td className="py-2 px-3">Time to prod / Team</td>
                  {cmp.platforms.map(p => (
                    <td key={p.id} className={`py-1.5 px-2 text-center text-[10px] ${p.id === selected ? 'bg-sky-500/5' : ''}`}>{p.weeks_to_prod}w · {p.team_size?.split(' ')[0]}</td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Selected pros / cons (updates on selection) */}
      {sel && (
        <div className="card">
          <div className="card-header py-3"><h3 className="font-bold text-gray-800 text-sm">{sel.name} — pros &amp; cons</h3></div>
          <div className="card-body py-3 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><div className="font-bold text-emerald-700 text-xs mb-1">Pros</div><ul className="list-disc ml-4 text-xs text-gray-600 space-y-1">{sel.pros?.map((x, i) => <li key={i}>{x}</li>)}</ul></div>
            <div><div className="font-bold text-sky-600 text-xs mb-1">Cons</div><ul className="list-disc ml-4 text-xs text-gray-600 space-y-1">{sel.cons?.map((x, i) => <li key={i}>{x}</li>)}</ul></div>
          </div>
        </div>
      )}

      {/* WS6: Platform implementation details */}
      <PlatformInsightsPanel platformId={selected} />
    </div>
  )
}

// ── WS6: Platform Insights Panel ─────────────────────────────────────────────
function PlatformInsightsPanel({ platformId }) {
  const [insight, setInsight] = useState(null)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!platformId) return
    setInsight(null)
    targetStateApi.platformInsight(platformId).then(setInsight).catch(() => {})
  }, [platformId])

  if (!insight) return null

  const PHASE_COLORS = {
    Discovery: 'bg-violet-100 text-violet-700 border-violet-200',
    Architecture: 'bg-blue-100 text-blue-700 border-blue-200',
    Development: 'bg-sky-100 text-sky-700 border-sky-200',
    Testing: 'bg-amber-100 text-amber-700 border-amber-200',
    DevSecOps: 'bg-rose-100 text-rose-700 border-rose-200',
    'AIOps & Monitoring': 'bg-emerald-100 text-emerald-700 border-emerald-200',
  }

  return (
    <div className="card">
      <button onClick={() => setOpen(o => !o)}
        className="card-header py-3 w-full flex items-center justify-between hover:bg-gray-50 transition-colors">
        <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Cpu size={15} /> Implementation details — {insight.id === 'baxter' ? 'Cognizant Baxter' : insight.id === 'flowsource' ? 'Cognizant Flowsource' : platformId}</h3>
        {open ? <ChevronUp size={16} className="text-gray-400" /> : <ChevronDown size={16} className="text-gray-400" />}
      </button>
      {open && (
        <div className="card-body py-4 space-y-4">
          <p className="text-xs text-gray-600">{insight.implementation_summary}</p>

          {/* Architecture */}
          <div>
            <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-1">Architecture</div>
            <p className="text-xs text-gray-600">{insight.architecture}</p>
          </div>

          {/* Agent catalog */}
          <div>
            <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-2">Agent catalog ({insight.agents?.length})</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {insight.agents?.map((a, i) => (
                <div key={i} className="flex items-start gap-2 border border-gray-100 rounded-lg px-3 py-2">
                  <Bot size={14} className="text-sky-500 mt-0.5 shrink-0" />
                  <div>
                    <div className="text-xs font-semibold text-gray-800">{a.name}</div>
                    <span className={`inline-block text-[10px] px-1.5 py-0.5 rounded border mt-0.5 ${PHASE_COLORS[a.phase] || 'bg-gray-100 text-gray-600 border-gray-200'}`}>{a.phase}</span>
                    <p className="text-[11px] text-gray-500 mt-1">{a.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tools & Differentiators */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-1">Tools &amp; platforms</div>
              <div className="flex flex-wrap gap-1.5">
                {insight.tools?.map((t, i) => (
                  <span key={i} className="text-[10px] px-2 py-1 rounded-lg border border-gray-200 bg-gray-50 text-gray-600">{t}</span>
                ))}
              </div>
            </div>
            <div>
              <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-1">Differentiators</div>
              <ul className="list-disc ml-4 text-[11px] text-gray-600 space-y-0.5">
                {insight.differentiators?.map((d, i) => <li key={i}>{d}</li>)}
              </ul>
            </div>
          </div>

          {/* Investment profile */}
          <div>
            <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-1">Investment profile</div>
            <div className="flex flex-wrap gap-4 text-xs text-gray-600">
              <span><b className="text-gray-700">Upfront:</b> {insight.investment_profile?.upfront}</span>
              <span><b className="text-gray-700">Ongoing:</b> {insight.investment_profile?.ongoing}</span>
              <span><b className="text-gray-700">Team ramp:</b> {insight.investment_profile?.team_ramp}</span>
            </div>
          </div>

          {/* Baxter: Before / After comparison */}
          {insight.vs_current_state && (
            <div>
              <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-1">Before vs after — current state impact</div>
              <p className="text-xs text-gray-600 mb-2">{insight.vs_current_state.summary}</p>
              <div className="overflow-x-auto">
                <table className="w-full text-xs min-w-[500px]">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-100">
                      <th className="py-1.5 px-2 font-semibold">Activity</th>
                      <th className="py-1.5 px-2 font-semibold">Before</th>
                      <th className="py-1.5 px-2 font-semibold w-6"></th>
                      <th className="py-1.5 px-2 font-semibold">After (Baxter)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {insight.vs_current_state.before_after?.map((row, i) => (
                      <tr key={i} className="border-b border-gray-50">
                        <td className="py-1.5 px-2 text-gray-700 font-medium">{row.activity}</td>
                        <td className="py-1.5 px-2 text-gray-500">{row.before}</td>
                        <td className="py-1.5 px-2 text-center"><ArrowRight size={12} className="text-sky-400" /></td>
                        <td className="py-1.5 px-2 text-sky-700 font-medium">{row.after}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Step 2: Compose target ──────────────────────────────────────────────────
function StepCompose({ cfg, setCfg, platform }) {
  const comp = cfg.composition
  const setComp = (patch) => setCfg(c => ({ ...c, composition: { ...c.composition, ...patch } }))
  const phases = [...new Set(comp.agents.map(a => a.phase))]
  const updAgent = (idx, patch) => setComp({ agents: comp.agents.map((a, i) => i === idx ? { ...a, ...patch } : a) })
  const delAgent = (idx) => setComp({ agents: comp.agents.filter((_, i) => i !== idx) })
  const addAgent = () => setComp({ agents: [...comp.agents, { phase: phases[0] || 'Development', agent: 'New Agent', tool: '', role_posture: 'assistant', active: true }] })
  const activeCount = comp.agents.filter(a => a.active).length

  const ChipList = ({ items, onChange, color }) => {
    const [v, setV] = useState('')
    return (
      <div className="flex flex-wrap gap-1.5 items-center">
        {items.map((t, i) => (
          <span key={i} className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded-lg border ${color}`}>
            {t}<button onClick={() => onChange(items.filter((_, idx) => idx !== i))} className="hover:text-sky-500"><Trash2 size={11} /></button>
          </span>
        ))}
        <input value={v} onChange={e => setV(e.target.value)} placeholder="+ add"
          onKeyDown={e => { if (e.key === 'Enter' && v.trim()) { onChange([...items, v.trim()]); setV('') } }}
          className="inp !w-28 !px-2 !py-1 text-xs" />
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="card card-body py-3 text-sm text-gray-600">
        Target composition seeded from the <b>US Bank AI-Native ADLC target state</b>{platform && <> for <b>{platform.name}</b></>}. Select / modify / add agents, tools and human roles. <span className="text-gray-400">{activeCount}/{comp.agents.length} agents active</span>
      </div>

      {/* US Bank AI-Native ADLC target board (reflects edits) */}
      <ADLCGrid agents={comp.agents} platformId={cfg.platform} />

      {/* Agents by phase */}
      <div className="card">
        <div className="card-header py-3 flex items-center justify-between">
          <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Bot size={15} /> Agents ({comp.agents.length})</h3>
          <button onClick={addAgent} className="btn-secondary text-xs flex items-center gap-1"><Plus size={12} /> Add agent</button>
        </div>
        <div className="card-body py-3 space-y-3">
          {phases.map(ph => (
            <div key={ph}>
              <div className="text-[11px] font-bold uppercase tracking-wide text-gray-400 mb-1">{ph}</div>
              <div className="space-y-1.5">
                {comp.agents.map((a, i) => a.phase === ph && (
                  <div key={i} className={`flex items-center gap-2 border rounded-lg px-2.5 py-1.5 ${a.active ? 'border-gray-200' : 'border-gray-100 opacity-50'}`}>
                    <input type="checkbox" checked={a.active} onChange={e => updAgent(i, { active: e.target.checked })} />
                    <input value={a.agent} onChange={e => updAgent(i, { agent: e.target.value })} className="inp !px-2 !py-1 text-sm font-semibold flex-1" />
                    <input value={a.tool} onChange={e => updAgent(i, { tool: e.target.value })} placeholder="tool" className="inp !px-2 !py-1 text-xs flex-1 hidden md:block" />
                    <select value={a.role_posture} onChange={e => updAgent(i, { role_posture: e.target.value })} className="inp !w-32 !px-2 !py-1 text-xs shrink-0">
                      {ROLE_POSTURE.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                    <button onClick={() => delAgent(i)} className="text-gray-400 hover:text-sky-500 p-1 shrink-0"><Trash2 size={14} /></button>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card"><div className="card-header py-3"><h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Users size={15} /> Human roles retained</h3></div>
          <div className="card-body py-3"><ChipList items={comp.human_roles} onChange={v => setComp({ human_roles: v })} color="bg-blue-50 text-blue-700 border-blue-200" /></div></div>
        <div className="card"><div className="card-header py-3"><h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Wrench size={15} /> Tools / platforms</h3></div>
          <div className="card-body py-3"><ChipList items={comp.tools} onChange={v => setComp({ tools: v })} color="bg-violet-50 text-violet-700 border-violet-200" /></div></div>
      </div>
    </div>
  )
}

// ── Step 3: Path ──────────────────────────────────────────────────────────────
function StepPath({ cfg, setCfg, ladder, risks, projectId, currentState }) {
  const [suggestion, setSuggestion] = useState(null)
  const [dynLadder, setDynLadder] = useState(null)
  const [expandedLevel, setExpandedLevel] = useState(cfg.target_level)
  useEffect(() => { setExpandedLevel(cfg.target_level) }, [cfg.target_level])
  useEffect(() => { if (dynLadder) setExpandedLevel(cfg.target_level) }, [dynLadder]) // eslint-disable-line
  const set = (patch) => setCfg(c => ({ ...c, ...patch }))

  // recompute auto-suggestion when maturity/risk change
  useEffect(() => {
    targetStateApi.roadmap(projectId, {
      platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
      interim_count: null, risk_appetite: cfg.risk_appetite, maturity_band: cfg.maturity_band,
    }).then(rm => setSuggestion(rm.suggestion)).catch(() => {})
  }, [cfg.maturity_band, cfg.risk_appetite, cfg.current_level, cfg.target_level, cfg.platform, projectId])

  // WS7: Fetch dynamic ladder when platform changes
  useEffect(() => {
    targetStateApi.dynamicLadder(cfg.platform).then(d => setDynLadder(d.ladder)).catch(() => setDynLadder(null))
  }, [cfg.platform])

  const chosen = cfg.interim_count
  const effective = chosen == null ? suggestion?.interim_count : chosen
  const stopLevels = useMemo(() => {
    // mirror backend spacing for the preview
    const avail = []; for (let l = cfg.current_level + 1; l < cfg.target_level; l++) avail.push(l)
    const k = Math.max(0, Math.min(effective ?? 0, avail.length))
    const picks = new Set()
    for (let i = 0; i < k; i++) picks.add(avail[Math.min(avail.length - 1, Math.floor((i + 0.5) * avail.length / k))])
    return [...picks].sort((a, b) => a - b).concat([cfg.target_level])
  }, [cfg.current_level, cfg.target_level, effective])

  const Field = ({ label, children }) => <div><label className="block text-[11px] font-semibold text-gray-500 mb-1">{label}</label>{children}</div>

  return (
    <div className="space-y-4">
      {currentState && (
        <div className="text-xs text-gray-500 -mb-1">
          🤖 Current state auto-populated from the Current-State VSM analysis
          {currentState.flow_efficiency != null && <> (flow efficiency {currentState.flow_efficiency}%)</>}
          {' '}→ <b className="text-sky-800">L{currentState.current_level} · {currentState.maturity_band}</b>. You can override below.
        </div>
      )}
      <div className="card card-body py-4 grid grid-cols-2 md:grid-cols-4 gap-3">
        <Field label="Current maturity (DevOps band) · auto">
          <select className="inp" value={cfg.maturity_band} onChange={e => set({ maturity_band: e.target.value })}>
            {[
              { v: 'PRE_CRAWL', l: 'L1 — Foundation' }, { v: 'CRAWL', l: 'L2 — Augmentation' },
              { v: 'WALK', l: 'L3 — Automation' }, { v: 'RUN', l: 'L4 — Transformation' }, { v: 'FLY', l: 'L5 — Reinvention' },
            ].map(b => <option key={b.v} value={b.v}>{b.l}</option>)}
          </select>
        </Field>
        <Field label="Risk appetite">
          <select className="inp" value={cfg.risk_appetite} onChange={e => set({ risk_appetite: e.target.value })}>
            {risks.map(r => <option key={r.id} value={r.id}>{r.label}</option>)}
          </select>
        </Field>
        <Field label="Current level">
          <select className="inp" value={cfg.current_level} onChange={e => set({ current_level: +e.target.value })}>
            {[0, 1, 2, 3, 4].map(l => <option key={l} value={l}>L{l}{l === 0 ? ' (pre-AI)' : ''}</option>)}
          </select>
        </Field>
        <Field label="Target (North Star)">
          <select className="inp" value={cfg.target_level} onChange={e => set({ target_level: +e.target.value })}>
            {[3, 4, 5].map(l => <option key={l} value={l}>L{l}</option>)}
          </select>
        </Field>
      </div>

      {/* Interim choice */}
      <div className="card card-body py-4">
        <div className="text-sm font-semibold text-gray-700 mb-2">How do you want to get there?</div>
        {suggestion && <div className="text-xs text-gray-500 mb-2">💡 Suggested: <b>{['one go', '1 interim', '2 interims'][suggestion.interim_count]}</b> — {suggestion.rationale}</div>}
        <div className="flex flex-wrap gap-2">
          {[{ v: null, l: 'Auto-suggest' }, { v: 0, l: 'One go' }, { v: 1, l: '1 interim' }, { v: 2, l: '2 interims' }].map(o => (
            <button key={String(o.v)} onClick={() => set({ interim_count: o.v })}
              className={`px-3 py-2 rounded-lg text-sm font-semibold border-2 ${chosen === o.v ? 'border-sky-600 bg-sky-500 text-white' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>{o.l}</button>
          ))}
        </div>
      </div>

      {/* Ladder with stops highlighted + dynamic perspectives (WS7) */}
      <div className="card">
        <div className="card-header py-3">
          <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2"><Layers size={15} /> L1–L5 Maturity Ladder</h3>
          {dynLadder?.[0]?.platform_kind && <span className="text-[10px] text-gray-400 ml-2">Perspectives adjusted for <b className="text-gray-600">{dynLadder[0].platform_kind.replace('_', ' ')}</b> delivery model</span>}
        </div>
        <div className="text-[10px] text-gray-400 px-3 pb-1">
          {(() => {
            const active = cfg.composition.agents.filter(a => a.active)
            const counts = {}
            active.forEach(a => { counts[a.role_posture || 'orchestrated'] = (counts[a.role_posture || 'orchestrated'] || 0) + 1 })
            const parts = Object.entries(counts).map(([k, v]) => `${v} ${k}`)
            return <>Your composition: <b className="text-gray-600">{active.length} agents</b> ({parts.join(', ')})</>
          })()}
        </div>
        <div className="card-body py-3 space-y-2">
          {(dynLadder || ladder).map(l => {
            const isStop = stopLevels.includes(l.level)
            const isTarget = l.level === cfg.target_level
            const isExpanded = expandedLevel === l.level
            const persp = l.perspectives
            const actions = l.level_actions

            return (
              <div key={l.level} className={`rounded-lg border ${isTarget ? 'border-emerald-300 bg-emerald-50/50' : isStop ? 'border-sky-600/40 bg-blue-50/40' : 'border-gray-100 opacity-70'}`}>
                <button onClick={() => setExpandedLevel(isExpanded ? null : l.level)}
                  className="w-full text-left px-3 py-2">
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${isTarget ? 'bg-emerald-600 text-white' : isStop ? 'bg-sky-500 text-white' : 'bg-gray-200 text-gray-600'}`}>L{l.level}</span>
                    <span className="font-semibold text-sm text-gray-800">{l.label}</span>
                    <span className="text-[10px] text-gray-400">{l.ml_band}</span>
                    {isStop && <span className="ml-auto text-[10px] font-bold text-sky-800 mr-2">{isTarget ? '★ TARGET' : '◀ interim stop'}</span>}
                    {persp ? (isExpanded ? <ChevronUp size={14} className="text-gray-400 ml-auto" /> : <ChevronDown size={14} className="text-gray-400 ml-auto" />) : null}
                  </div>
                  <p className="text-[11px] text-gray-500 mt-1 leading-snug">{l.summary}</p>
                  <div className="text-[10px] text-gray-400 mt-1">Agents: {l.agent_role} · HITL: {l.hitl} · {l.automation_pct}% automation · humans: {l.human_roles_retained?.join(', ')}</div>
                  {l.level === cfg.target_level && (
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[10px] text-sky-600 font-semibold">Agent postures at L{l.level}:</span>
                      {(() => {
                        const lc = LEVEL_POSTURE_MAP[l.level] || LEVEL_POSTURE_MAP[5]
                        return Object.entries(lc.mix).map(([p, w]) => (
                          <span key={p} className={`text-[9px] px-1.5 py-0.5 rounded font-bold ${p === 'orchestrated' ? 'bg-emerald-100 text-emerald-700' : p === 'independent' ? 'bg-violet-100 text-violet-700' : 'bg-blue-100 text-blue-700'}`}>
                            {Math.round(w * 100)}% {p}
                          </span>
                        ))
                      })()}
                      <span className="text-[9px] text-gray-400">(editable in Step 2)</span>
                    </div>
                  )}
                </button>

                {/* WS7: Multi-perspective panel */}
                {isExpanded && !persp && !dynLadder && (
                  <div className="border-t border-gray-100 px-3 py-3 text-xs text-gray-400 animate-pulse">Loading perspectives…</div>
                )}
                {isExpanded && persp && Object.keys(persp).length > 0 && (
                  <div className="border-t border-gray-100 px-3 py-3 space-y-3">
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                      <PerspectiveCard icon={Users} title="People" data={persp.people} color="blue" />
                      <PerspectiveCard icon={Layers} title="Process" data={persp.process} color="violet" />
                      <PerspectiveCard icon={Wrench} title="Tools" data={persp.tools} color="amber" />
                      <PerspectiveCard icon={Eye} title="Outcomes" data={persp.outcomes} color="emerald" />
                      <PerspectiveCard icon={Briefcase} title="Investment" data={persp.investment} color="rose" />
                    </div>
                    {actions?.length > 0 && (
                      <div>
                        <div className="text-[11px] font-bold text-gray-500 mb-1">Actions to reach L{l.level}</div>
                        <ul className="grid grid-cols-1 md:grid-cols-2 gap-1">
                          {actions.map((a, i) => (
                            <li key={i} className="flex items-start gap-1.5 text-[11px] text-gray-600">
                              <Check size={12} className="text-sky-500 shrink-0 mt-0.5" />{a}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

// ── Step 4: Review & generate ──────────────────────────────────────────────
function StepReview({ roadmap, busy, progress, onSave, platform, composition }) {
  const [edits, setEdits] = useState({})
  const [editingStep, setEditingStep] = useState(null)

  useEffect(() => { if (roadmap) setEdits({}) }, [roadmap])

  if (busy && !roadmap) return <div className="card card-body text-center text-gray-400 py-16">Generating roadmap…</div>
  if (!roadmap) return <div className="card card-body text-center text-gray-400 py-16">No roadmap yet.</div>

  const t = roadmap.totals
  const totalEdits = edits._totals || {}
  const getTotal = (key) => totalEdits[key] ?? t[key]
  const setTotal = (key, val) => setEdits(e => ({ ...e, _totals: { ...e._totals, [key]: val } }))
  const setStepEdit = (stepIdx, key, val) => setEdits(e => ({ ...e, [stepIdx]: { ...e[stepIdx], [key]: val } }))
  const hasEdits = Object.keys(edits).length > 0

  return (
    <div className="space-y-4">
      {/* Edit mode banner */}
      {hasEdits && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-2 text-xs text-amber-800 flex items-center justify-between">
          <span>✏️ You have unsaved edits to the roadmap values</span>
          <button onClick={() => setEdits({})} className="text-amber-600 hover:text-amber-800 font-semibold">Reset all edits</button>
        </div>
      )}

      {/* Totals — editable */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { key: 'one_time_usd', label: 'One-time investment', icon: DollarSign },
          { key: 'annual_benefit_usd', label: 'Annual benefit', icon: DollarSign },
          { key: 'timeline_weeks', label: 'Timeline (weeks)', icon: Map },
          { key: 'payback_months', label: 'Payback (months)', icon: Gauge },
        ].map(item => (
          <div key={item.key} className="card p-4">
            <div className="text-[11px] font-semibold text-gray-500 uppercase tracking-wide flex items-center gap-1"><item.icon size={12} /> {item.label}</div>
            <input
              type="number"
              value={getTotal(item.key) ?? ''}
              onChange={e => setTotal(item.key, parseFloat(e.target.value) || 0)}
              className="text-2xl font-extrabold text-sky-800 mt-1 bg-transparent border-b border-dashed border-gray-300 focus:border-sky-500 focus:outline-none w-full"
            />
            {totalEdits[item.key] != null && (
              <div className="text-[9px] text-amber-600 mt-0.5">Original: {item.key.includes('usd') ? usd(t[item.key]) : t[item.key]}</div>
            )}
          </div>
        ))}
      </div>

      {/* Composition summary from Step 2 */}
      {composition?.agents?.length > 0 && (
        <div className="bg-sky-50 border border-sky-100 rounded-xl px-4 py-2 text-xs text-sky-800">
          <b>Your agent composition:</b>{' '}
          {(() => {
            const active = composition.agents.filter(a => a.active)
            if (!active.length) return <span className="text-gray-400">No active agents — configure in Step 2</span>
            const counts = {}
            active.forEach(a => { counts[a.role_posture || 'orchestrated'] = (counts[a.role_posture || 'orchestrated'] || 0) + 1 })
            return Object.entries(counts).map(([k, v]) => (
              <span key={k} className="inline-flex items-center gap-1 mr-3">
                <span className={`w-2 h-2 rounded-full ${k === 'orchestrated' ? 'bg-emerald-500' : k === 'independent' ? 'bg-violet-500' : 'bg-blue-500'}`} />
                {v} {k}
              </span>
            ))
          })()}
        </div>
      )}

      {/* Steps — editable */}
      <div className="space-y-3">
        {roadmap.steps.map((s, si) => {
          const isEditing = editingStep === si
          const stepE = edits[si] || {}
          return (
            <div key={s.step} className={`card ${s.is_target ? 'border-2 border-emerald-300' : ''}`}>
              <div className="card-header py-3 flex items-center justify-between">
                <h3 className="font-bold text-gray-800 text-sm flex items-center gap-2">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${s.is_target ? 'bg-emerald-600 text-white' : 'bg-sky-500 text-white'}`}>Step {s.step} · L{s.level}</span>
                  {s.label}<span className="text-[10px] text-gray-400">{s.ml_band}</span>
                  {s.is_target && <span className="badge-green !py-0">North Star</span>}
                </h3>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">{s.business_case.cumulative_pct}% there · wk {s.business_case.timeline_weeks}</span>
                  <button
                    onClick={() => setEditingStep(isEditing ? null : si)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold border transition-colors ${isEditing ? 'bg-sky-500 text-white border-sky-500' : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'}`}
                  >
                    {isEditing ? '✓ Done' : '✏️ Edit'}
                  </button>
                </div>
              </div>
              <div className="card-body py-3 grid grid-cols-1 lg:grid-cols-3 gap-4 text-xs">
                <div>
                  {isEditing ? (
                    <textarea
                      value={stepE.summary ?? s.summary}
                      onChange={e => setStepEdit(si, 'summary', e.target.value)}
                      rows={3}
                      className="w-full px-2 py-1.5 border border-gray-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-sky-500 resize-none"
                    />
                  ) : (
                    <p className="text-gray-600 mb-2">{stepE.summary ?? s.summary}</p>
                  )}
                  {isEditing ? (
                    <div className="space-y-1.5 mt-2">
                      <div className="flex items-center gap-2">
                        <label className="text-[10px] text-gray-500 w-16 shrink-0">Agent role:</label>
                        <input value={stepE.agent_role ?? s.agent_role} onChange={e => setStepEdit(si, 'agent_role', e.target.value)}
                          className="inp !px-2 !py-1 text-[11px] flex-1" />
                      </div>
                      <div className="flex items-center gap-2">
                        <label className="text-[10px] text-gray-500 w-16 shrink-0">HITL:</label>
                        <select value={stepE.hitl ?? s.hitl} onChange={e => setStepEdit(si, 'hitl', e.target.value)}
                          className="inp !px-2 !py-1 text-[11px] flex-1">
                          <option value="all">All (full human oversight)</option>
                          <option value="critical">Critical path only</option>
                          <option value="exceptions">Exceptions only</option>
                          <option value="audit">Audit trail (post-hoc)</option>
                          <option value="none">None (fully autonomous)</option>
                        </select>
                      </div>
                      <div className="flex items-center gap-2">
                        <label className="text-[10px] text-gray-500 w-16 shrink-0">Automation:</label>
                        <input type="number" min="0" max="100" value={stepE.automation_pct ?? s.automation_pct}
                          onChange={e => setStepEdit(si, 'automation_pct', parseInt(e.target.value) || 0)}
                          className="inp !px-2 !py-1 text-[11px] w-20" />
                        <span className="text-[10px] text-gray-400">%</span>
                      </div>
                    </div>
                  ) : (
                    <>
                      <div className="text-[11px] text-gray-500">Agents: <b>{stepE.agent_role ?? s.agent_role}</b> · HITL: <b>{stepE.hitl ?? s.hitl}</b> · {stepE.automation_pct ?? s.automation_pct}% automation</div>
                      <div className="text-[11px] text-gray-500 mt-1">Humans: {s.human_roles_retained.join(', ')}</div>
                      <div className="text-[11px] text-gray-400 mt-1">Phases: {s.phase_coverage.join(' · ')}</div>
                    </>
                  )}
                </div>
                <div>
                  <div className="font-bold text-gray-500 uppercase text-[10px] tracking-wide mb-1">Outcome bands</div>
                  {s.metric_band.map(m => (
                    <div key={m.id} className="flex justify-between items-center">
                      <span className="text-gray-500">{m.name}</span>
                      {isEditing ? (
                        <input type="number" value={stepE[`metric_${m.id}`] ?? m.target}
                          onChange={e => setStepEdit(si, `metric_${m.id}`, parseFloat(e.target.value) || 0)}
                          className="inp !px-1.5 !py-0.5 text-[11px] w-20 text-right font-bold" />
                      ) : (
                        <b className="text-gray-700">{stepE[`metric_${m.id}`] ?? m.target}{m.unit === '%' ? '%' : m.unit === '$' ? '' : ` ${m.unit}`}</b>
                      )}
                    </div>
                  ))}
                </div>
                <div className="bg-sky-500 text-white rounded-lg p-3">
                  <div className="text-[10px] font-bold uppercase tracking-wide text-blue-200 mb-1">Business case (this step)</div>
                  {isEditing ? (
                    <div className="space-y-2">
                      <div>
                        <label className="text-[9px] text-blue-200">Step investment ($)</label>
                        <input type="number" value={stepE.step_investment ?? s.business_case.step_investment_usd}
                          onChange={e => setStepEdit(si, 'step_investment', parseFloat(e.target.value) || 0)}
                          className="w-full bg-white/20 text-white border border-white/30 rounded px-2 py-1 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-white/50" />
                      </div>
                      <div>
                        <label className="text-[9px] text-blue-200">Annual benefit ($)</label>
                        <input type="number" value={stepE.annual_benefit ?? s.business_case.annual_benefit_usd}
                          onChange={e => setStepEdit(si, 'annual_benefit', parseFloat(e.target.value) || 0)}
                          className="w-full bg-white/20 text-white border border-white/30 rounded px-2 py-1 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-white/50" />
                      </div>
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 gap-1.5">
                      <div><div className="text-base font-extrabold">{usd(stepE.step_investment ?? s.business_case.step_investment_usd)}</div><div className="text-[9px] text-blue-200">step investment</div></div>
                      <div><div className="text-base font-extrabold">{usd(stepE.annual_benefit ?? s.business_case.annual_benefit_usd)}</div><div className="text-[9px] text-blue-200">annual benefit</div></div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Save + progress */}
      <div className="flex items-center gap-3">
        <button onClick={onSave} disabled={busy} className="btn-primary text-sm flex items-center gap-1.5"><Save size={15} /> Save target state</button>
        {hasEdits && <span className="text-xs text-amber-600 font-semibold">⚠ Unsaved edits</span>}
        {progress && <span className="text-sm text-gray-600">Progress baseline: <b className="text-sky-800">{progress.overall_pct}%</b> toward target · next: {progress.next_milestone.label}</span>}
      </div>
      {progress && (
        <div className="card card-body py-3 grid grid-cols-2 md:grid-cols-5 gap-3">
          {progress.components.map(c => (
            <div key={c.key}>
              <div className="text-[11px] font-semibold text-gray-500">{c.label}</div>
              <div className="text-xl font-extrabold text-sky-800">{c.pct}%</div>
              <div className="h-1.5 bg-gray-100 rounded-full mt-1"><div className="h-1.5 bg-sky-500 rounded-full" style={{ width: `${c.pct}%` }} /></div>
              <div className="text-[10px] text-gray-400 mt-1">{c.detail}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ── WS7: Perspective card for dynamic ladder ────────────────────────────────
const PERSP_COLORS = {
  blue: 'border-blue-200 bg-blue-50/50',
  violet: 'border-violet-200 bg-violet-50/50',
  amber: 'border-amber-200 bg-amber-50/50',
  emerald: 'border-emerald-200 bg-emerald-50/50',
  rose: 'border-rose-200 bg-rose-50/50',
}
const PERSP_TITLE = {
  blue: 'text-blue-700',
  violet: 'text-violet-700',
  amber: 'text-amber-700',
  emerald: 'text-emerald-700',
  rose: 'text-rose-700',
}

function PerspectiveCard({ icon: Icon, title, data, color }) {
  if (!data || Object.keys(data).length === 0) return null
  const cls = PERSP_COLORS[color] || PERSP_COLORS.blue
  const ttl = PERSP_TITLE[color] || PERSP_TITLE.blue

  const entries = Object.entries(data).filter(([k]) => k !== 'summary')

  return (
    <div className={`border rounded-lg p-2.5 ${cls}`}>
      <div className={`text-[10px] font-bold uppercase tracking-wide mb-1 flex items-center gap-1 ${ttl}`}>
        <Icon size={12} /> {title}
      </div>
      <p className="text-[11px] text-gray-600 mb-1.5 leading-snug">{data.summary}</p>
      {entries.map(([key, val]) => (
        <div key={key} className="text-[10px] text-gray-500">
          <span className="font-semibold text-gray-600">{key.replace(/_/g, ' ')}:</span>{' '}
          {Array.isArray(val) ? val.join(', ') : typeof val === 'object' ? JSON.stringify(val) : String(val)}
        </div>
      ))}
    </div>
  )
}

function Stat({ icon: Icon, label, value }) {
  return (
    <div className="card p-4">
      <div className="text-[11px] font-semibold text-gray-500 uppercase tracking-wide flex items-center gap-1"><Icon size={12} /> {label}</div>
      <div className="text-2xl font-extrabold text-sky-800 mt-1">{value}</div>
    </div>
  )
}
