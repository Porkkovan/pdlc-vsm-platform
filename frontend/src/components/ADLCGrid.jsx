import {
  ADLC_PHASES, ADLC_PHASE_TINT, ADLC_ORCH_STACK, ADLC_PLATFORM_NAME, ADLC_HUMAN_ROLE,
  AGENT_ACTIVITY_MAP,
} from '../data/adlcTargetState'

const POSTURE_STYLE = {
  assistant:    { bg: 'bg-blue-500',    label: 'ASSISTANT' },
  independent:  { bg: 'bg-violet-500',  label: 'INDEPENDENT' },
  orchestrated: { bg: 'bg-emerald-500', label: 'ORCHESTRATED' },
}

/**
 * US Bank AI-Native ADLC target board. Phase names + activities come from the VSM
 * editor (PDLC_PHASES); the 21 agents/tools are fixed and each is mapped to the VSM
 * activities it owns. Reflects the live composition (`agents`); inactive agents are
 * dimmed; optional `coveredPhases` dims phases not yet agentified at the level.
 */
export default function ADLCGrid({ agents = [], platformId = 'homegrown', coveredPhases = null, title = 'AI-Native · ADLC Target' }) {
  // Match agents to a phase column by the leading "PhN" token (robust to older
  // saved phase labels that used different phase names).
  const phaseKey = (s) => (s || '').split('·')[0].trim()
  const byPhase = {}
  agents.forEach(a => { const k = phaseKey(a.phase); (byPhase[k] = byPhase[k] || []).push(a) })
  const orch = ADLC_ORCH_STACK[platformId] || ADLC_ORCH_STACK.homegrown
  const platName = ADLC_PLATFORM_NAME[platformId] || 'Agentic Platform'
  const covered = (name) => !coveredPhases || coveredPhases.includes(name)

  return (
    <div className="card overflow-hidden">
      <div className="bg-sky-500 text-white px-4 py-2.5 flex items-center justify-between">
        <div>
          <div className="font-bold text-sm">{title}</div>
          <div className="text-[11px] text-sky-100">Agentic Development Lifecycle · Platform Orchestrates All Agents · Human: Intent · Review · Approve Only</div>
        </div>
        <span className="text-[11px] font-bold bg-sky-600 border border-white/20 rounded px-2 py-1 shrink-0">🚀 Full ADLC · Autonomous</span>
      </div>
      <div className="bg-sky-50 text-sky-800 px-4 py-1.5 text-[11px] font-semibold border-b border-sky-100">
        🧠 {platName} — Orchestration Layer <span className="text-sky-500 font-normal">({orch})</span>
      </div>
      <div className="overflow-x-auto">
        <div className="grid min-w-[1180px]" style={{ gridTemplateColumns: `repeat(${ADLC_PHASES.length}, minmax(0, 1fr))` }}>
          {ADLC_PHASES.map((ph, i) => {
            const items = byPhase[ph.id] || []
            const on = covered(ph.name)
            return (
              <div key={ph.id} className={`border-r border-gray-100 last:border-r-0 ${on ? '' : 'opacity-45'}`}>
                <div className={`${ADLC_PHASE_TINT[i]} text-white px-2 py-1.5`}>
                  <div className="text-[11px] font-bold leading-tight">{ph.id} · {ph.name}</div>
                </div>
                {/* VSM editor activities for this phase */}
                <div className="px-2 py-1.5 border-b border-gray-100 min-h-[42px]">
                  <div className="flex flex-wrap gap-1">
                    {ph.activities.map((act, j) => (
                      <span key={j} className="text-[8.5px] text-slate-500 bg-slate-50 border border-slate-100 rounded px-1 py-0.5 leading-tight">{act}</span>
                    ))}
                  </div>
                </div>
                <div className="p-1.5 space-y-1.5">
                  {items.map((a, idx) => {
                    const acts = a.activities || AGENT_ACTIVITY_MAP[a.agent] || []
                    return (
                      <div key={idx} className={`rounded border px-2 py-1.5 ${a.active ? 'border-sky-100 bg-sky-50/40' : 'border-gray-100 bg-white opacity-40'}`}>
                        {(() => { const ps = POSTURE_STYLE[a.role_posture] || POSTURE_STYLE.orchestrated; return <span className={`text-[8px] font-bold text-white ${ps.bg} rounded px-1 py-0.5`}>{ps.label}</span> })()}
                        <div className="text-[11px] font-bold text-slate-700 mt-1 leading-tight">{a.agent}</div>
                        <div className="text-[10px] text-slate-400 flex items-center gap-0.5"><span>⚙</span>{a.tool}</div>
                        {acts.length > 0 && (
                          <ul className="mt-1 space-y-0.5">
                            {acts.map((act, k) => <li key={k} className="text-[9px] text-slate-500 leading-tight flex gap-1"><span className="text-sky-400">›</span>{act}</li>)}
                          </ul>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      </div>
      {(() => {
        const counts = {}
        agents.filter(a => a.active).forEach(a => { counts[a.role_posture || 'orchestrated'] = (counts[a.role_posture || 'orchestrated'] || 0) + 1 })
        const parts = Object.entries(counts).map(([k, v]) => `${v} ${k}`)
        return (
          <div className="bg-emerald-50 border-t border-emerald-100 px-4 py-2 text-[11px] font-semibold text-emerald-800">
            👤 HUMAN ROLE: {ADLC_HUMAN_ROLE}
            <span className="ml-3 text-emerald-500 font-normal">({parts.join(' · ')})</span>
          </div>
        )
      })()}
    </div>
  )
}
