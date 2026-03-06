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
    improvements = [
        {"id": f"imp-{i}", "title": v["title"], "activity": k, **v}
        for i, (k, v) in enumerate(IMPROVEMENT_CATALOGUE.items(), 1)
    ]
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
async def get_business_case(project_id: str, scenario: str):
    from ..agents.business_case_builder.agent import BUSINESS_CASES
    bc = BUSINESS_CASES.get(scenario)
    if not bc:
        raise HTTPException(400, f"Unknown scenario: {scenario}")
    return bc


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
