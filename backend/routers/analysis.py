from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/analysis", tags=["analysis"])

# These endpoints serve pre-computed results that are stored after agent runs.
# In production these would read from DB (AnalysisRun table).
# For initial release they proxy to the agents router.

@router.get("/{project_id}/bottlenecks")
async def get_bottlenecks(project_id: str):
    from ..agents.bottleneck_analyzer.agent import _default_bottlenecks
    return {"bottlenecks": _default_bottlenecks(), "source": "default"}


@router.get("/{project_id}/improvements")
async def get_improvements(project_id: str):
    from ..agents.improvement_generator.agent import IMPROVEMENT_CATALOGUE
    from ..agents.bottleneck_analyzer.agent import _default_bottlenecks
    bns = _default_bottlenecks()
    bn_map = {b["activity"]: b for b in bns}
    improvements = []
    for i, (activity, entry) in enumerate(IMPROVEMENT_CATALOGUE.items(), 1):
        bn = bn_map.get(activity, {})
        improvements.append({
            "id":           f"imp-{i}",
            "bottleneckId": bn.get("id", ""),
            "phaseId":      bn.get("phaseId", 1),
            "phaseName":    bn.get("phaseName", ""),
            "activity":     activity,
            "priority":     "High" if bn.get("severity") in ("Critical", "High") else "Medium",
            **entry,
        })
    return {"improvements": improvements}


@router.get("/{project_id}/future-state/{scenario}")
async def get_future_state(project_id: str, scenario: str):
    from ..agents.state import VSMAgentState
    from ..agents.future_state_designer.agent import run_future_state_designer, SCENARIOS
    if scenario not in SCENARIOS:
        raise HTTPException(400, f"Unknown scenario: {scenario}. Must be one of {list(SCENARIOS.keys())}")
    state = {"project_id": project_id, "project": {}, "metrics": {}, "errors": []}
    result = await run_future_state_designer(state)
    return result.get("future_states", {}).get(scenario, {})


@router.get("/{project_id}/business-case/{scenario}")
async def get_business_case(project_id: str, scenario: str, platform: str | None = None):
    """
    Get the business case for a scenario.

    For Option C, an optional ?platform=<homegrown|stump|bmad|copilot_workspace> query param
    folds the selected platform choice's overrides (tools, devsecops, aiops, product-centric,
    org changes) and deltas (investment, timeline, pros/cons, ops team sizing, playbook phasing)
    into the response.
    """
    from ..agents.business_case_builder.agent import (
        BUSINESS_CASES, C_PLATFORM_OPTIONS, apply_c_platform
    )
    bc = BUSINESS_CASES.get(scenario)
    if not bc:
        raise HTTPException(400, f"Unknown scenario: {scenario}")
    if scenario == "option-c":
        # Always expose the catalogue so the frontend can render the selector
        bc = {
            **bc,
            "platform_catalog": {
                pid: {
                    "id":            opt["id"],
                    "name":          opt["name"],
                    "tagline":       opt["tagline"],
                    "weeks_to_prod": opt["production_ready_weeks"],
                    "investment_delta_text": opt["investment_delta_text"],
                }
                for pid, opt in C_PLATFORM_OPTIONS.items()
            },
            "default_platform": "homegrown",
        }
        # Apply the requested platform overrides, defaulting to homegrown
        bc = apply_c_platform(bc, platform or "homegrown")
    return bc


@router.get("/{project_id}/business-case/option-c/platforms")
async def list_option_c_platforms(project_id: str):
    """Return the Option C build-vs-buy platform catalogue (id, name, tagline, deltas)."""
    from ..agents.business_case_builder.agent import C_PLATFORM_OPTIONS
    return {
        "platforms": [
            {
                "id":                    opt["id"],
                "name":                  opt["name"],
                "tagline":               opt["tagline"],
                "weeks_to_prod":         opt["production_ready_weeks"],
                "investment_delta_text": opt["investment_delta_text"],
                "investment_delta_usd":  {"low": opt["investment_delta_usd_low"],
                                          "high": opt["investment_delta_usd_high"]},
                "timeline_delta_weeks":  opt["timeline_delta_weeks"],
                "team_size":             opt["platform_ops_team"]["size"],
                "pros":                  opt["pros"],
                "cons":                  opt["cons"],
            }
            for opt in C_PLATFORM_OPTIONS.values()
        ],
        "default": "homegrown",
    }


@router.get("/{project_id}/benchmarks")
async def get_benchmarks(project_id: str):
    from ..agents.pdlc_data import INDUSTRY_BENCHMARKS
    return {"benchmarks": INDUSTRY_BENCHMARKS}


@router.get("/{project_id}/export")
async def export_report(project_id: str, format: str = "json"):
    """Export full analysis report."""
    if format == "json":
        return {"project_id": project_id, "format": "json", "message": "Full export — run full analysis first"}
    raise HTTPException(400, "Only json format supported initially")
