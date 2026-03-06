"""
Future State Designer Agent
Designs 3 future state VSM scenarios with predicted lean metrics:
  Option A: Augmented Human (AI co-pilots all roles)
  Option B: Hybrid (strategic agents + core human roles)
  Option C: AI-First (agents across PDLC + 2 roles: Product Definer + Product Builder)
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import PDLC_PHASES
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)

SCENARIOS = {
    "option-a": {
        "id":           "option-a",
        "label":        "Option A",
        "title":        "Augmented Human — AI as Co-pilot",
        "automation_pct": 40,
        "pt_reduction":   35,
        "wt_reduction":   55,
        "human_roles":  ["Product Manager", "Business Analyst", "Solution Architect", "UX Designer",
                         "Developer", "QA Engineer", "DevOps Engineer", "Operations"],
        "agent_count":  16,
        "description":  "All PDLC personas assisted by AI agents. Humans retain decision authority.",
    },
    "option-b": {
        "id":           "option-b",
        "label":        "Option B",
        "title":        "Hybrid — Selective AI + Core Human Roles",
        "automation_pct": 65,
        "pt_reduction":   55,
        "wt_reduction":   72,
        "human_roles":  ["Product Owner", "Tech Lead / Architect", "Developer", "QA Lead", "DevOps Engineer"],
        "agent_count":  12,
        "description":  "Strategic AI deployment in high-impact phases; humans focus on design and decision-making.",
    },
    "option-c": {
        "id":           "option-c",
        "label":        "Option C",
        "title":        "AI-First — Agents Across PDLC + Two Roles",
        "automation_pct": 85,
        "pt_reduction":   70,
        "wt_reduction":   88,
        "human_roles":  ["Product Definer", "Product Builder"],
        "agent_count":  22,
        "description":  "Maximum automation. Product Definer sets outcomes; Product Builder oversees agent orchestration.",
    }
}


async def run_future_state_designer(state: VSMAgentState) -> VSMAgentState:
    """Design future state VSMs for all 3 scenarios."""
    logger.info("[Future State Designer] Designing 3 future state scenarios")

    current_metrics = state.get("metrics", {})
    current_lt  = current_metrics.get("total_lead_time_days", 42)
    current_pt  = current_metrics.get("total_process_time", 100)
    current_wt  = current_metrics.get("total_wait_time", 536)
    current_fe  = current_metrics.get("overall_flow_efficiency", 8)

    future_states = {}

    for scenario_id, scenario in SCENARIOS.items():
        pt_factor = 1 - (scenario["pt_reduction"] / 100)
        wt_factor = 1 - (scenario["wt_reduction"] / 100)

        future_pt = round(current_pt * pt_factor, 1)
        future_wt = round(current_wt * wt_factor, 1)
        future_lt = round((future_pt + future_wt) / 8, 2)
        future_fe = round((future_pt / max(future_pt + future_wt, 1)) * 100, 1)

        # Per-phase future metrics
        future_phases = []
        for phase in PDLC_PHASES:
            current_phase = next(
                (p for p in current_metrics.get("phases", []) if p.get("phase_id") == phase["id"]), {}
            )
            phase_pt = current_phase.get("process_time", (phase["effort_range"]["min"] + phase["effort_range"]["max"]) / 2)
            phase_wt = current_phase.get("wait_time",    (phase["wait_range"]["min"]   + phase["wait_range"]["max"])   / 2 * 8)

            # Testing phase gets more wt reduction (biggest bottleneck phase)
            wt_multiplier = 1.2 if phase["id"] == 5 else 1.0
            wt_mult_factor = 1 - (scenario["wt_reduction"] * wt_multiplier / 100)
            wt_mult_factor = max(wt_mult_factor, 0.05)   # floor at 5%

            f_pt = round(phase_pt * pt_factor, 1)
            f_wt = round(phase_wt * wt_mult_factor, 1)
            f_lt = round((f_pt + f_wt) / 8, 2)
            f_fe = round((f_pt / max(f_pt + f_wt, 1)) * 100, 1)

            future_phases.append({
                "phase_id":        phase["id"],
                "phase_name":      phase["name"],
                "process_time":    f_pt,
                "wait_time":       f_wt,
                "lead_time":       f_lt,
                "flow_efficiency": f_fe,
                "improvement_pct": {
                    "pt": round((1 - pt_factor) * 100),
                    "wt": round((1 - wt_mult_factor) * 100)
                }
            })

        future_states[scenario_id] = {
            **scenario,
            "metrics": {
                "total_process_time":      future_pt,
                "total_wait_time":         future_wt,
                "total_lead_time_days":    future_lt,
                "overall_flow_efficiency": future_fe,
                "phases":                  future_phases
            },
            "vs_current": {
                "lt_reduction_pct":  round((1 - future_lt / max(current_lt, 1)) * 100, 1),
                "pt_reduction_pct":  round((1 - future_pt / max(current_pt, 1)) * 100, 1),
                "wt_reduction_pct":  round((1 - future_wt / max(current_wt, 1)) * 100, 1),
                "fe_improvement_pct":round((future_fe - current_fe) / max(current_fe, 1) * 100, 1),
                "fe_absolute_gain":  round(future_fe - current_fe, 1)
            },
            "dora_predicted": {
                "deployment_frequency": "Multiple per day" if scenario["automation_pct"] > 80
                                        else "Daily" if scenario["automation_pct"] > 60
                                        else "Weekly",
                "lead_time_for_change": f"{future_lt:.1f} days",
                "change_failure_rate":  "< 5%" if future_fe > 35 else "5–10%",
                "mttr_hours":           round(future_wt * 0.02, 1)
            }
        }

    # LLM-enhanced: generate narrative for each scenario
    if has_llm():
        future_states = await _enrich_with_narratives(future_states, state)

    return {**state, "future_states": future_states}


async def _enrich_with_narratives(future_states: dict, state: dict) -> dict:
    """Add LLM-generated executive narrative and specific agent deployment plan per scenario."""
    project = state.get("project", {})
    current_metrics = state.get("metrics", {})

    for scenario_id, fs in future_states.items():
        m = fs.get("metrics", {})
        vc = fs.get("vs_current", {})
        prompt = f"""You are a digital transformation strategist. Write an executive summary for a future state VSM scenario.

Team: {project.get('team', 'Engineering')}  Industry: {project.get('industry', '')}
Scenario: {fs['label']} — {fs['title']}
Description: {fs['description']}
Automation Level: {fs.get('automation_pct', fs.get('automation_level', '?'))}%
Human Roles: {', '.join(fs['human_roles'])}
AI Agents Deployed: {', '.join(fs['aiAgents']) if isinstance(fs.get('aiAgents'), list) and fs['aiAgents'] else str(fs.get('agent_count', '?')) + ' AI agents'}

Current State: LT={current_metrics.get('total_lead_time_days', '?')}d, FE={current_metrics.get('overall_flow_efficiency', '?')}%
Future State:  LT={m.get('total_lead_time_days', '?')}d, FE={m.get('overall_flow_efficiency', '?')}%
Improvements:  LT -{vc.get('lt_reduction_pct', '?')}%, FE +{vc.get('fe_absolute_gain', '?')} pts

Write 4–5 sentences covering:
1. What this transformation achieves and who it affects
2. Key AI agents enabling the improvement and their specific role
3. Expected engineering culture and ways-of-working change
4. Predicted competitive advantage in time-to-market

Be specific and inspiring. No bullet points."""
        try:
            fs["narrative"] = await ainvoke(prompt)
        except Exception as ex:
            logger.warning(f"[Future State Designer] LLM narrative failed for {scenario_id}: {ex}")

    return future_states
