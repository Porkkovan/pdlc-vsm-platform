/**
 * VSMVisualFlow — Lean VSM horizontal flow diagram
 * Renders PDLC phases as connected process/decision cards
 * Used in Current State and Future State pages
 */
import clsx from 'clsx'

// PDLC phase type classification (PROCESS vs DECISION gate)
const PHASE_TYPE = {
  1: 'PROCESS',
  2: 'DECISION',  // Design review & approval gate
  3: 'PROCESS',
  4: 'PROCESS',
  5: 'DECISION',  // QA go/no-go gate
  6: 'DECISION',  // Release gate (CAB)
  7: 'PROCESS',
}

// Industry p75 benchmark flow efficiency per phase
const BENCH_FE = { 1: 34, 2: 24, 3: 71, 4: 43, 5: 55, 6: 11, 7: 29 }

function fmtTime(hours) {
  if (hours == null || isNaN(hours)) return '—'
  if (hours >= 16) return `${(hours / 8).toFixed(1)}d`
  return `${Math.round(hours)}h`
}

// ── Single phase card ──────────────────────────────────────────────
function PhaseCard({ phase, processTime, waitTime, isBottleneck, aiAgent, currPT, currWT, mode }) {
  const total  = processTime + waitTime
  const fe     = total > 0 ? (processTime / total) * 100 : 0
  const ptBarW = total > 0 ? Math.max(4, Math.round((processTime / total) * 100)) : 4
  const wtBarW = total > 0 ? Math.max(4, Math.round((waitTime  / total) * 100)) : 4

  const benchFE = BENCH_FE[phase.id] || 30
  const aboveBench = fe >= benchFE

  const ptDelta = (mode === 'future' && currPT > 0) ? Math.round((1 - processTime / currPT) * 100) : null
  const wtDelta = (mode === 'future' && currWT > 0) ? Math.round((1 - waitTime  / currWT) * 100) : null

  const phaseType = PHASE_TYPE[phase.id] || 'PROCESS'

  // Border & type-label colour logic
  let borderCls, typeColor, typeBg, typeLabel
  if (mode === 'future' && aiAgent) {
    borderCls  = 'border-green-500'
    typeColor  = 'text-green-400'
    typeBg     = 'bg-green-500/20'
    typeLabel  = 'AI AGENT'
  } else if (isBottleneck) {
    borderCls  = 'border-orange-400'
    typeColor  = 'text-orange-400'
    typeBg     = 'bg-orange-500/20'
    typeLabel  = phaseType
  } else if (phaseType === 'DECISION') {
    borderCls  = 'border-yellow-400'
    typeColor  = 'text-yellow-400'
    typeBg     = 'bg-yellow-500/20'
    typeLabel  = 'DECISION'
  } else {
    borderCls  = 'border-blue-500'
    typeColor  = 'text-blue-400'
    typeBg     = 'bg-blue-500/20'
    typeLabel  = 'PROCESS'
  }

  return (
    <div className={clsx(
      'flex-shrink-0 rounded-xl border-2 p-3.5 flex flex-col gap-0',
      'bg-[#0d1b2e]',
      borderCls
    )} style={{ width: '168px', minWidth: '168px' }}>

      {/* Type label */}
      <div className={clsx('inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-bold tracking-widest uppercase mb-2 self-start', typeBg, typeColor)}>
        {typeLabel}
      </div>

      {/* Phase name */}
      <div className="text-white font-bold text-sm leading-snug mb-3" style={{ minHeight: '36px' }}>
        {phase.name}
      </div>

      {/* Process Time */}
      <div className="mb-2.5">
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-400 text-xs">Process</span>
          <div className="flex items-center gap-1.5">
            <span className="text-blue-300 font-bold text-xs">{fmtTime(processTime)}</span>
            {ptDelta > 0 && (
              <span className="text-green-400 text-[10px] font-bold bg-green-500/20 px-1 rounded">▼{ptDelta}%</span>
            )}
          </div>
        </div>
        <div className="h-1.5 bg-gray-700/80 rounded-full overflow-hidden">
          <div
            className="h-full bg-blue-500 rounded-full"
            style={{ width: `${ptBarW}%` }}
          />
        </div>
      </div>

      {/* Wait Time */}
      <div className="mb-3">
        <div className="flex justify-between items-center mb-1">
          <span className="text-gray-400 text-xs">Wait</span>
          <div className="flex items-center gap-1.5">
            <span className={clsx('font-bold text-xs', isBottleneck ? 'text-orange-300' : 'text-amber-300')}>
              {fmtTime(waitTime)}
            </span>
            {wtDelta > 0 && (
              <span className="text-green-400 text-[10px] font-bold bg-green-500/20 px-1 rounded">▼{wtDelta}%</span>
            )}
          </div>
        </div>
        <div className="h-1.5 bg-gray-700/80 rounded-full overflow-hidden">
          <div
            className={clsx('h-full rounded-full', isBottleneck ? 'bg-orange-400' : 'bg-amber-400')}
            style={{ width: `${wtBarW}%` }}
          />
        </div>
      </div>

      {/* FE score */}
      <div className="flex items-center justify-between">
        <span className={clsx(
          'text-xs font-semibold',
          fe >= 50 ? 'text-green-400' : fe >= 30 ? 'text-yellow-400' : 'text-orange-400'
        )}>
          FE {fe.toFixed(0)}%
        </span>
        {aboveBench && !isBottleneck && (
          <span className="text-green-400 text-[10px] font-bold">✓ bench</span>
        )}
      </div>

      {/* Bottleneck warning */}
      {isBottleneck && (
        <div className="mt-1.5 flex items-center gap-1 text-orange-400 text-xs font-semibold">
          <span>⚠</span><span>Bottleneck</span>
        </div>
      )}

      {/* AI agent badge */}
      {mode === 'future' && aiAgent && (
        <div className="mt-1.5 text-green-300 text-[11px] leading-tight font-medium truncate">
          🤖 {aiAgent}
        </div>
      )}
    </div>
  )
}

// ── Arrow connector ────────────────────────────────────────────────
function Arrow() {
  return (
    <div className="flex items-center flex-shrink-0 self-center" style={{ marginTop: '20px' }}>
      <div className="h-px w-6 bg-gray-500" />
      <div className="text-gray-500 text-lg leading-none" style={{ marginLeft: '-2px' }}>▶</div>
    </div>
  )
}

// ── Summary metric pill ────────────────────────────────────────────
function MetricPill({ label, value, sub, color }) {
  const colorMap = {
    white:  'text-white',
    blue:   'text-blue-400',
    amber:  'text-amber-400',
    green:  'text-green-400',
    orange: 'text-orange-400',
    red:    'text-red-400',
    purple: 'text-purple-400',
  }
  return (
    <div className="flex-1 min-w-[120px] bg-[#111e33] rounded-xl px-5 py-3 border border-gray-700/60">
      <div className="text-gray-400 text-xs mb-1">{label}</div>
      <div className={clsx('text-2xl font-bold', colorMap[color] || 'text-white')}>{value}</div>
      {sub && <div className="text-gray-500 text-xs mt-0.5">{sub}</div>}
    </div>
  )
}

// ── Main component ─────────────────────────────────────────────────
/**
 * @param {Array}  phases   — [{id, name, processTime, waitTime, aiAgent?, currPT?, currWT?}]
 * @param {string} mode     — 'current' | 'future'
 * @param {string} scenarioLabel — e.g. 'Option A'
 * @param {number} totalPT
 * @param {number} totalWT
 * @param {number} flowEfficiency
 */
export default function VSMVisualFlow({ phases, mode = 'current', scenarioLabel, totalPT, totalWT, flowEfficiency }) {
  const totalLT   = (totalPT + totalWT) / 8
  const feNum     = parseFloat(flowEfficiency) || 0
  const feColor   = feNum >= 40 ? 'green' : feNum >= 25 ? 'amber' : 'orange'
  const ptDays    = totalPT / 8
  const wtDays    = totalWT / 8

  return (
    <div className="rounded-2xl overflow-hidden" style={{ background: '#0a1628' }}>
      {/* Header */}
      <div className="flex items-center justify-between px-6 pt-5 pb-4">
        <div>
          <div className="text-white font-bold text-base">
            {mode === 'current' ? 'Current State — PDLC Value Stream Map' : `Future State — ${scenarioLabel}`}
          </div>
          <div className="text-gray-400 text-xs mt-0.5">
            {mode === 'current'
              ? '7 Phases · 36 Activities · Lean VSM · Industry Benchmarks'
              : `AI-Transformed State · Benchmark-grounded projections`}
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1.5 text-gray-400">
            <span className="w-3 h-3 rounded-sm bg-blue-500 inline-block" /> Process Time
          </span>
          <span className="flex items-center gap-1.5 text-gray-400">
            <span className="w-3 h-3 rounded-sm bg-amber-400 inline-block" /> Wait Time
          </span>
          {mode === 'current' && (
            <span className="flex items-center gap-1.5 text-gray-400">
              <span className="w-3 h-3 rounded-sm bg-orange-400 inline-block" /> Bottleneck
            </span>
          )}
          {mode === 'future' && (
            <span className="flex items-center gap-1.5 text-gray-400">
              <span className="w-3 h-3 rounded-sm bg-green-500 inline-block" /> AI Automated
            </span>
          )}
        </div>
      </div>

      {/* Summary metrics */}
      <div className="flex gap-3 px-6 pb-5 flex-wrap">
        <MetricPill
          label="Total Lead Time"
          value={`${totalLT.toFixed(1)}d`}
          color="white"
        />
        <MetricPill
          label="Process Time"
          value={`${ptDays.toFixed(1)}d`}
          sub={`${Math.round(totalPT)}h total`}
          color="blue"
        />
        <MetricPill
          label="Wait Time"
          value={`${wtDays.toFixed(1)}d`}
          sub={`${Math.round(totalWT)}h total`}
          color="amber"
        />
        <MetricPill
          label="Flow Efficiency"
          value={`${feNum.toFixed(1)}%`}
          sub={feNum >= 40 ? '✓ Above target (40%)' : `Target: 40% · Gap: ${(40 - feNum).toFixed(1)}%`}
          color={feColor}
        />
      </div>

      {/* Flow diagram */}
      <div className="overflow-x-auto pb-6 px-6">
        <div className="flex items-stretch gap-0" style={{ minWidth: 'max-content' }}>
          {phases.map((p, idx) => (
            <div key={p.id} className="flex items-center">
              <PhaseCard
                phase={p}
                processTime={p.processTime}
                waitTime={p.waitTime}
                isBottleneck={p.isBottleneck}
                aiAgent={p.aiAgent}
                currPT={p.currPT}
                currWT={p.currWT}
                mode={mode}
              />
              {idx < phases.length - 1 && <Arrow />}
            </div>
          ))}
        </div>
      </div>

      {/* Benchmark legend */}
      <div className="px-6 pb-5 border-t border-gray-700/40 pt-4">
        <div className="flex flex-wrap gap-x-6 gap-y-1.5 text-xs text-gray-500">
          <span className="font-semibold text-gray-400">Industry p75 Benchmarks:</span>
          {Object.entries(BENCH_FE).map(([pid, benchFe]) => {
            const ph = phases.find(p => p.id === parseInt(pid))
            const label = ph ? ph.name.split(' ')[0] : `Ph${pid}`
            return (
              <span key={pid}>
                P{pid} {label}: <span className="text-gray-300 font-semibold">{benchFe}% FE</span>
              </span>
            )
          })}
        </div>
      </div>
    </div>
  )
}
