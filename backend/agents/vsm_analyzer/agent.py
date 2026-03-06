"""
VSM Analyzer Agent
Computes comprehensive lean VSM metrics from the mapped data.
Uses LLM (if available) to provide contextual narrative analysis.
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import PDLC_PHASES

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

    narrative = _build_narrative(metrics, state.get("project", {}))

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


def _build_narrative(metrics: dict, project: dict) -> str:
    fe = metrics["overall_flow_efficiency"]
    lt = metrics["total_lead_time_days"]
    team = project.get("team", "the team")

    assessment = "elite" if fe > 40 else "high" if fe > 25 else "medium" if fe > 15 else "needs improvement"

    return (
        f"{team} has a total lead time of {lt:.1f} days with {fe}% flow efficiency. "
        f"This places the team in the '{assessment}' performance category. "
        f"{'The majority of lead time is wait time, indicating significant flow impediments.' if fe < 20 else 'Flow efficiency is reasonable but further improvements are achievable.'} "
        f"Deployment frequency is estimated at '{metrics['deployment_frequency']}'. "
        f"Key focus areas are wait time reduction and bottleneck elimination."
    )
