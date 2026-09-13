import { useEffect, useState } from 'react'
import { targetStateApi } from '../services/api'

/**
 * Shared hook for A/B/C → target-state alignment.
 *
 * When a Target State is configured for the project, the generic Option A/B/C
 * selector should be replaced by the configured interim/target steps. Each step
 * maps to an underlying scenario (option-a/b/c) so existing per-scenario content
 * keeps working — the page just sets activeScenario from the selected step.
 *
 * Returns:
 *   configured  — true when a target state exists (show the step selector)
 *   steps       — [{level,label,outcome_scenario,is_target}, ...]
 *   stepIdx     — selected step index
 *   pickStep(i) — select a step (caller maps steps[i].outcome_scenario → activeScenario)
 *   platform    — configured platform id
 *   refresh()   — re-read config (also runs on window focus)
 */
export function useTargetScenario(projectId, setActiveScenario) {
  const [configured, setConfigured] = useState(false)
  const [steps, setSteps] = useState([])
  const [stepIdx, setStepIdx] = useState(0)
  const [platform, setPlatform] = useState(null)

  useEffect(() => {
    if (!projectId) { setConfigured(false); setSteps([]); return }
    const load = () => targetStateApi.getConfig(projectId).then(cfg => {
      if (!cfg || cfg.configured === false) { setConfigured(false); setSteps([]); return }
      setConfigured(true); setPlatform(cfg.platform)
      targetStateApi.roadmap(projectId, {
        platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
        interim_count: cfg.interim_count, risk_appetite: cfg.risk_appetite,
      }).then(rm => {
        const st = rm.steps || []
        setSteps(st)
        const ti = st.findIndex(s => s.is_target)
        const idx = ti >= 0 ? ti : st.length - 1
        setStepIdx(idx)
        const sc = st[idx]?.outcome_scenario
        if (sc && setActiveScenario) setActiveScenario(sc)
      }).catch(() => {})
    }).catch(() => setConfigured(false))
    load()
    const onFocus = () => load()
    window.addEventListener('focus', onFocus)
    return () => window.removeEventListener('focus', onFocus)
  }, [projectId]) // eslint-disable-line

  const pickStep = (i) => {
    setStepIdx(i)
    const sc = steps[i]?.outcome_scenario
    if (sc && setActiveScenario) setActiveScenario(sc)
  }

  return { configured, steps, stepIdx, pickStep, platform }
}
