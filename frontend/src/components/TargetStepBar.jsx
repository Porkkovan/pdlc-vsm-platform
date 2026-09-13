import { Link } from 'react-router-dom'
import { Target } from 'lucide-react'

/**
 * Step selector that replaces the A/B/C scenario cards when a Target State is set.
 * Shows the configured interim/target path; picking a step drives the page's scenario.
 */
export default function TargetStepBar({ steps, stepIdx, pickStep, platform, onPick }) {
  if (!steps?.length) return null
  return (
    <div className="bg-white p-3 rounded-xl border border-sky-600/20">
      <div className="text-xs text-gray-500 mb-2 flex items-center gap-1.5">
        <Target size={13} className="text-sky-700" />
        Aligned to your envisioned future state — <b className="text-sky-800">{steps.map(s => `L${s.level}`).join(' → ')}</b>
        {platform && <> on <b className="text-sky-800">{(platform || '').replace('_', ' ')}</b></>}.
        <Link to="/target-state" className="ml-auto font-semibold text-sky-700 hover:underline">Edit in Studio →</Link>
      </div>
      <div className="flex flex-wrap gap-2">
        {steps.map((s, i) => (
          <button key={s.step ?? i} onClick={() => { pickStep(i); onPick && onPick(i) }}
            className={`px-3 py-2 rounded-lg text-sm font-semibold border-2 ${i === stepIdx ? 'border-sky-600 bg-sky-700 text-white' : 'border-gray-200 text-gray-600 hover:border-gray-300'}`}>
            {s.is_target ? '★ ' : ''}L{s.level} · {s.label}
            <span className="opacity-70 text-[11px]"> ({(s.outcome_scenario || '').replace('option-', 'Opt ').toUpperCase()})</span>
          </button>
        ))}
      </div>
    </div>
  )
}
