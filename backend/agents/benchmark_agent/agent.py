"""
Benchmark Agent
Loads industry best-practice metrics (DORA Elite, Lean VSM targets, Gartner benchmarks)
and compares them to the current state, setting the improvement target baseline.
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import INDUSTRY_BENCHMARKS, PDLC_PHASES

logger = logging.getLogger(__name__)

# Industry benchmark data by source
DORA_ELITE = {
    "deployment_frequency": "Multiple per day",
    "lead_time_for_change": "< 1 hour",
    "change_failure_rate":  "< 5%",
    "mttr":                 "< 1 hour",
    "flow_efficiency":      "> 40%"
}

LEAN_VSMS_TARGETS = {
    "overall_flow_efficiency": 40,  # World-class is 40%+
    "max_queue_depth":         3,   # No more than 3 items in any queue
    "release_cadence_days":    14,  # Bi-weekly at minimum
}

COMPETITOR_BENCHMARKS = {
    "top_quartile_lt_days":  12,
    "median_lt_days":        28,
    "top_quartile_fe_pct":   35,
    "median_fe_pct":         15,
    "source": "Gartner/DORA 2024 State of DevOps Report"
}


async def run_benchmark_agent(state: VSMAgentState) -> VSMAgentState:
    """Load benchmarks and compare to current state."""
    logger.info("[Benchmark Agent] Loading industry benchmarks")

    metrics = state.get("metrics", {})
    current_lt = metrics.get("total_lead_time_days", 42)
    current_fe = metrics.get("overall_flow_efficiency", 8)

    phase_benchmarks = {}
    for phase in PDLC_PHASES:
        bm = INDUSTRY_BENCHMARKS.get(phase["id"], {})
        current_phase = next((p for p in metrics.get("phases", []) if p.get("phase_id") == phase["id"]), {})
        current_phase_pt = current_phase.get("process_time", (phase["effort_range"]["min"] + phase["effort_range"]["max"]) / 2)
        current_phase_wt = current_phase.get("wait_time", 0)
        current_phase_fe = round((current_phase_pt / max(current_phase_pt + current_phase_wt, 1)) * 100, 1)

        gap_fe  = bm.get("fe_p75", 30) - current_phase_fe
        gap_wt  = current_phase_wt - bm.get("wt_p50", current_phase_wt)

        phase_benchmarks[phase["id"]] = {
            "phase_name":        phase["name"],
            "current_pt":        round(current_phase_pt, 1),
            "current_wt":        round(current_phase_wt, 1),
            "current_fe":        current_phase_fe,
            "benchmark_pt_p50":  bm.get("pt_p50", round(current_phase_pt * 0.75, 1)),
            "benchmark_wt_p50":  bm.get("wt_p50", round(current_phase_wt * 0.6, 1)),
            "benchmark_fe_p75":  bm.get("fe_p75", 30),
            "gap_fe_pct":        round(gap_fe, 1),
            "gap_wt_hours":      round(gap_wt, 1),
            "benchmark_source":  "Lean VSM Industry Standard / DORA 2024"
        }

    benchmarks = {
        "phases":               phase_benchmarks,
        "overall": {
            "current_lt_days":  current_lt,
            "current_fe_pct":   current_fe,
            "target_lt_days":   LEAN_VSMS_TARGETS["release_cadence_days"],
            "target_fe_pct":    LEAN_VSMS_TARGETS["overall_flow_efficiency"],
            "competitor_top_quartile_lt": COMPETITOR_BENCHMARKS["top_quartile_lt_days"],
            "competitor_median_lt":       COMPETITOR_BENCHMARKS["median_lt_days"],
            "competitor_source":          COMPETITOR_BENCHMARKS["source"],
            "dora_elite":                 DORA_ELITE
        }
    }

    return {**state, "benchmarks": benchmarks}
