"""
VSM Analyzer Agent
Computes comprehensive lean VSM metrics from the mapped data.
Uses LLM (if available) to provide contextual narrative analysis.
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import PDLC_PHASES
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)


async def run_vsm_analyzer(state: VSMAgentState) -> VSMAgentState:
    """Compute lean metrics and build the full current-state VSM model."""
    logger.info("[VSM Analyzer] Computing lean metrics")

    vsm_data = state.get("vsm_data", {})
    phases = vsm_data.get("phases", [])

    if not phases:
        logger.warning("[VSM Analyzer] No VSM data — cannot compute metrics")
        return {**state, "metrics": {}, "errors": state.get("errors", []) + ["VSM Analyzer: no data"]}

    # Compute per-phase and aggregate metrics
    computed_phases = []
    total_pt = 0
    total_wt = 0
    total_lt = 0

    for phase in phases:
        pt = phase.get("process_time", 0)
        wt = phase.get("wait_time", 0)
        lt = phase.get("lead_time", (pt + wt) / 8)
        fe = round((pt / (pt + wt)) * 100, 1) if (pt + wt) > 0 else 0

        computed_phases.append({
            **phase,
            "process_time": pt,
            "wait_time": wt,
            "lead_time": lt,
            "flow_efficiency": fe,
            "value_add_ratio": fe
        })
        total_pt += pt
        total_wt += wt
        total_lt += lt

    overall_fe = round((total_pt / (total_pt + total_wt)) * 100, 1) if (total_pt + total_wt) > 0 else 0

    metrics = {
        "total_process_time":   round(total_pt, 1),
        "total_wait_time":      round(total_wt, 1),
        "total_lead_time_days": round(total_lt, 2),
        "overall_flow_efficiency": overall_fe,
        "phases": computed_phases,
        # DORA-aligned metrics (estimated from VSM data)
        "deployment_frequency": _estimate_deployment_freq(total_lt),
        "lead_time_for_change": round(total_lt, 1),
        "change_failure_rate":  _estimate_cfr(overall_fe),
        "mttr_hours":           round(total_wt * 0.05, 1)   # estimate 5% of wait time
    }

    narrative = await _build_narrative(metrics, state.get("project", {}))

    return {**state, "metrics": metrics, "vsm_data": {**vsm_data, "phases": computed_phases}, "narrative": narrative}


def _estimate_deployment_freq(lead_time_days: float) -> str:
    if lead_time_days < 3:   return "Multiple times per day"
    if lead_time_days < 7:   return "Daily"
    if lead_time_days < 14:  return "Weekly"
    if lead_time_days < 30:  return "Bi-weekly"
    return "Monthly or slower"


def _estimate_cfr(flow_efficiency: float) -> str:
    if flow_efficiency > 40:  return "< 5%"
    if flow_efficiency > 25:  return "5–10%"
    if flow_efficiency > 15:  return "10–20%"
    return "> 20%"


async def _build_narrative(metrics: dict, project: dict) -> str:
    fe  = metrics["overall_flow_efficiency"]
    lt  = metrics["total_lead_time_days"]
    pt  = metrics["total_process_time"]
    wt  = metrics["total_wait_time"]
    team = project.get("team", "the team")
    industry = project.get("industry", "")

    if has_llm():
        prompt = f"""You are a Lean VSM expert analysing a Product Development Lifecycle value stream.

Team: {team}  Industry: {industry}
Total Lead Time: {lt:.1f} days
Total Process Time: {pt:.1f} hours (value-adding)
Total Wait Time: {wt:.1f} hours (waste)
Flow Efficiency: {fe}%
Deployment Frequency (estimated): {metrics.get('deployment_frequency', 'unknown')}
DORA Lead Time for Change: {metrics.get('lead_time_for_change', lt)} days
Estimated Change Failure Rate: {metrics.get('change_failure_rate', 'unknown')}

Write a concise executive narrative (5–7 sentences) assessing the current state VSM:
- Overall performance category (elite/high/medium/low) with justification
- Key flow efficiency findings
- Main areas of waste (wait time concentration)
- Comparison to industry benchmarks (world-class is 40%+ FE, elite DORA is sub-day lead time)
- Top 2–3 strategic priorities for improvement

Be specific, data-driven, and actionable. No bullet points — flowing prose."""
        try:
            return await ainvoke(prompt)
        except Exception as e:
            logger.warning(f"[VSM Analyzer] LLM narrative failed: {e} — using rule-based")

    # Rule-based fallback
    assessment = "elite" if fe > 40 else "high" if fe > 25 else "medium" if fe > 15 else "needs improvement"
    return (
        f"{team} has a total lead time of {lt:.1f} days with {fe}% flow efficiency, "
        f"placing the team in the '{assessment}' performance category. "
        f"{'The majority of lead time ({:.0f}h) is non-value-adding wait time, indicating significant flow impediments across the PDLC.'.format(wt) if fe < 20 else 'Flow efficiency is moderate; further wait time elimination will unlock significant delivery speed gains.'} "
        f"Deployment frequency is estimated at '{metrics.get('deployment_frequency', 'unknown')}'. "
        f"World-class teams achieve 40%+ flow efficiency and sub-day lead times (DORA Elite). "
        f"Priority focus areas: wait time reduction in Continuous Testing and Delivery phases, and eliminating human approval gate dependencies."
    )
