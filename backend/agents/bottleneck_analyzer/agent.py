"""
Bottleneck Analyzer Agent
Identifies flow bottlenecks per PDLC phase and activity using Lean VSM criteria:
  - High wait time relative to benchmark
  - High effort (touch time) vs industry norm
  - Low flow efficiency vs target
  - Human dependency / approval gates
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import PDLC_PHASES, ALL_ACTIVITIES
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)

# Bottleneck thresholds
WAIT_CRITICAL_HOURS  = 16   # > 16 hours wait = Critical
WAIT_HIGH_HOURS      = 8    # > 8 hours wait = High
EFFORT_CRITICAL_HRS  = 20   # > 20 hours effort = Critical
FLOW_EFFICIENCY_LOW  = 15   # FE < 15% = bottleneck


async def run_bottleneck_analyzer(state: VSMAgentState) -> VSMAgentState:
    """Identify and classify bottlenecks across all 7 PDLC phases."""
    logger.info("[Bottleneck Analyzer] Identifying flow bottlenecks")

    vsm_data   = state.get("vsm_data", {})
    benchmarks = state.get("benchmarks", {})
    phases     = vsm_data.get("phases", [])

    if not phases:
        return {**state, "bottlenecks": _default_bottlenecks()}

    bottlenecks = []
    bn_id = 1

    for phase in phases:
        phase_id = phase.get("phase_id")
        phase_name = phase.get("phase_name", "")
        benchmark_phase = benchmarks.get("phases", {}).get(phase_id, {})
        benchmark_wt    = benchmark_phase.get("benchmark_wt_p50", 999)

        # Phase-level bottleneck check
        pt = phase.get("process_time", 0)
        wt = phase.get("wait_time", 0)
        fe = round((pt / max(pt + wt, 1)) * 100, 1)

        if fe < FLOW_EFFICIENCY_LOW:
            bottlenecks.append({
                "id":        f"bn-{bn_id}",
                "phase_id":  phase_id,
                "phase_name":phase_name,
                "activity":  f"[Phase Level] {phase_name}",
                "severity":  "Critical" if fe < 10 else "High",
                "metric":    "flow_efficiency",
                "value":     f"{fe}%",
                "impact":    f"Phase flow efficiency {fe}% is below {FLOW_EFFICIENCY_LOW}% threshold. Industry P75 target is {benchmark_phase.get('benchmark_fe_p75', 30)}%.",
                "benchmark": f"Target: {benchmark_phase.get('benchmark_fe_p75', 30)}%",
                "category":  "Flow Efficiency"
            })
            bn_id += 1

        # Activity-level bottleneck check
        for act in phase.get("activities", []):
            act_id   = act.get("activity_id", "")
            act_name = act.get("activity_name", act_id)
            act_pt   = act.get("process_time", 0)
            act_wt   = act.get("wait_time", 0)

            act_def = ALL_ACTIVITIES.get(act_id, {})
            default_wt_max = act_def.get("wait", {}).get("max", 0) if act_def else 0

            # Wait time bottleneck
            if act_wt >= WAIT_CRITICAL_HOURS or (act_wt > 0 and act_wt > benchmark_wt * 1.5):
                severity = "Critical" if act_wt >= WAIT_CRITICAL_HOURS else "High"
                bottlenecks.append({
                    "id":        f"bn-{bn_id}",
                    "phase_id":  phase_id,
                    "phase_name":phase_name,
                    "activity":  act_name,
                    "severity":  severity,
                    "metric":    "wait",
                    "value":     f"{act_wt:.0f} hrs",
                    "impact":    f"Wait time of {act_wt:.0f}h significantly exceeds benchmark. Creates queue buildup and flow disruption.",
                    "benchmark": f"Benchmark: {benchmark_wt:.0f}h",
                    "category":  "Wait Time"
                })
                bn_id += 1

            # Effort bottleneck
            if act_pt >= EFFORT_CRITICAL_HRS:
                bottlenecks.append({
                    "id":        f"bn-{bn_id}",
                    "phase_id":  phase_id,
                    "phase_name":phase_name,
                    "activity":  act_name,
                    "severity":  "Critical" if act_pt > 32 else "High",
                    "metric":    "effort",
                    "value":     f"{act_pt:.0f} hrs",
                    "impact":    f"High effort activity ({act_pt:.0f}h) creates resource contention and delays parallel work.",
                    "benchmark": "Industry target: < 16h per activity",
                    "category":  "Effort"
                })
                bn_id += 1

    # Add known structural bottlenecks (human approval gates)
    human_gates = [
        {"activity": "Manual SIT / UAT / NF Signoff",  "phase_id": 5, "phase_name": "Continuous Testing",   "wait": "2–5 days"},
        {"activity": "Release Gates / Approvals",        "phase_id": 6, "phase_name": "Continuous Delivery",  "wait": "1–5 days"},
        {"activity": "Solution Architecture (High-Level)","phase_id": 2, "phase_name": "Architecture & UX Design","wait": "3–7 days"}
    ]
    for gate in human_gates:
        if not any(b["activity"] == gate["activity"] for b in bottlenecks):
            bottlenecks.append({
                "id":        f"bn-{bn_id}",
                "phase_id":  gate["phase_id"],
                "phase_name":gate["phase_name"],
                "activity":  gate["activity"],
                "severity":  "High",
                "metric":    "wait",
                "value":     gate["wait"],
                "impact":    "Human approval gate creates scheduling dependency and flow stoppage.",
                "benchmark": "Best practice: automated gate with human exception-only review",
                "category":  "Approval Gate"
            })
            bn_id += 1

    # Sort by severity
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    bottlenecks.sort(key=lambda b: severity_order.get(b["severity"], 99))

    # LLM-enhanced: enrich top bottlenecks with deeper root-cause analysis
    if has_llm() and bottlenecks:
        bottlenecks = await _enrich_bottlenecks(bottlenecks[:6], state)

    logger.info(f"[Bottleneck Analyzer] Found {len(bottlenecks)} bottlenecks")
    return {**state, "bottlenecks": bottlenecks}


async def _enrich_bottlenecks(top_bns: list, state: dict) -> list:
    """Use LLM to generate deeper root-cause and business impact for top bottlenecks."""
    metrics = state.get("metrics", {})
    project = state.get("project", {})

    summary_lines = "\n".join(
        f"- {b['activity']} ({b['phase_name']}): {b['metric']}={b['value']}, severity={b['severity']}"
        for b in top_bns
    )
    prompt = f"""You are a Lean VSM and software engineering expert.

Team: {project.get('team', 'Engineering Team')}  Industry: {project.get('industry', '')}
Overall Flow Efficiency: {metrics.get('overall_flow_efficiency', '?')}%
Total Lead Time: {metrics.get('total_lead_time_days', '?')} days

Top bottlenecks identified:
{summary_lines}

For each bottleneck, provide a one-sentence root cause and a one-sentence business impact (time-to-market, quality, or cost angle).
Return ONLY a JSON array in this exact format, no extra text:
[
  {{"activity": "<name>", "root_cause": "<sentence>", "business_impact": "<sentence>"}},
  ...
]"""
    try:
        raw = await ainvoke(prompt)
        import json, re
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            enrichments = json.loads(match.group())
            enrichment_map = {e["activity"]: e for e in enrichments}
            for bn in top_bns:
                e = enrichment_map.get(bn["activity"], {})
                if e:
                    bn["root_cause"]      = e.get("root_cause", "")
                    bn["business_impact"] = e.get("business_impact", "")
    except Exception as ex:
        logger.warning(f"[Bottleneck Analyzer] LLM enrichment failed: {ex}")

    # Return enriched top bns; the rest stay as-is (appended below by caller)
    return top_bns


def _default_bottlenecks() -> list:
    """Pre-computed bottlenecks when no data is available."""
    return [
        {"id": "bn-1", "phase_id": 5, "phase_name": "Continuous Testing",    "activity": "Automated Performance Testing",    "severity": "Critical", "metric": "effort", "value": "16–40 hrs", "impact": "Highest effort activity — manual authoring, long execution cycles", "category": "Effort"},
        {"id": "bn-2", "phase_id": 5, "phase_name": "Continuous Testing",    "activity": "Manual SIT / UAT / NF Signoff",    "severity": "Critical", "metric": "wait",   "value": "2–5 days",  "impact": "Human approval dependency creates multi-day flow stoppage", "category": "Approval Gate"},
        {"id": "bn-3", "phase_id": 3, "phase_name": "Code Management",       "activity": "Peer Code Review",                 "severity": "High",     "metric": "wait",   "value": "4–24 hrs",  "impact": "Reviewer availability blocks developer flow", "category": "Wait Time"},
        {"id": "bn-4", "phase_id": 5, "phase_name": "Continuous Testing",    "activity": "Test Data Generation / Management","severity": "High",     "metric": "wait",   "value": "4–16 hrs",  "impact": "Data provisioning delays test execution", "category": "Wait Time"},
        {"id": "bn-5", "phase_id": 6, "phase_name": "Continuous Delivery",   "activity": "Release Gates / Approvals",        "severity": "High",     "metric": "wait",   "value": "1–5 days",  "impact": "CAB scheduling creates release backlogs", "category": "Approval Gate"},
        {"id": "bn-6", "phase_id": 2, "phase_name": "Architecture & UX Design","activity": "UX/UI High-Fidelity Design & Handoff","severity": "Medium","metric": "effort","value": "16–40 hrs","impact": "Design-to-dev handoff creates rework loops", "category": "Effort"},
        {"id": "bn-7", "phase_id": 5, "phase_name": "Continuous Testing",    "activity": "Dynamic Security Testing (DAST)",  "severity": "Medium",   "metric": "wait",   "value": "4–16 hrs",  "impact": "DAST queue and false-positive triaging overhead", "category": "Wait Time"},
    ]
