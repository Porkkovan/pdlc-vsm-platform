"""
Agents Router
Endpoints to trigger individual agents or the full multi-agent pipeline.
"""
import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..agents.orchestrator.graph import run_full_analysis
from ..agents.vsm_analyzer.agent      import run_vsm_analyzer
from ..agents.bottleneck_analyzer.agent import run_bottleneck_analyzer
from ..agents.improvement_generator.agent import run_improvement_generator
from ..agents.future_state_designer.agent import run_future_state_designer
from ..agents.business_case_builder.agent import run_business_case_builder
from ..agents.benchmark_agent.agent   import run_benchmark_agent

router = APIRouter(prefix="/agents", tags=["agents"])

# In-memory run store (use Redis in production)
_runs: dict = {}


class RunRequest(BaseModel):
    scenario: Optional[str] = "all"  # option-a, option-b, option-c, or all


def _empty_state(project_id: str) -> dict:
    return {
        "project_id": project_id,
        "project": {},
        "alm_raw_data": {},
        "vsm_data": {},
        "overrides": {},
        "errors": [],
        "run_id": str(uuid.uuid4()),
        "status": "running"
    }


@router.post("/run-analysis/{project_id}")
async def run_analysis(project_id: str, background_tasks: BackgroundTasks):
    """Kick off the full multi-agent pipeline in the background."""
    run_id = str(uuid.uuid4())
    _runs[run_id] = {"status": "running", "project_id": project_id}

    async def _run():
        try:
            result = await run_full_analysis(project_id, {}, {})
            _runs[run_id] = {"status": "complete", "result": result}
        except Exception as e:
            _runs[run_id] = {"status": "failed", "error": str(e)}

    background_tasks.add_task(_run)
    return {"run_id": run_id, "status": "started"}


@router.get("/status/{run_id}")
async def get_status(run_id: str):
    run = _runs.get(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    return {"run_id": run_id, **run}


@router.get("/result/{project_id}")
async def get_result(project_id: str):
    """Get the latest analysis result for a project."""
    run = next((r for r in reversed(list(_runs.values())) if r.get("project_id") == project_id and r.get("status") == "complete"), None)
    if not run:
        raise HTTPException(404, "No completed analysis found")
    return run.get("result", {})


@router.get("/history/{project_id}")
async def get_history(project_id: str):
    """Get all runs for a project."""
    return [{"run_id": k, **v} for k, v in _runs.items() if v.get("project_id") == project_id]


# Individual agent endpoints
@router.post("/vsm-analyzer/{project_id}")
async def run_vsm_analyzer_ep(project_id: str):
    state = _empty_state(project_id)
    result = await run_vsm_analyzer(state)
    return {"metrics": result.get("metrics"), "narrative": result.get("narrative")}


@router.post("/bottleneck-analyzer/{project_id}")
async def run_bottleneck_ep(project_id: str):
    state = _empty_state(project_id)
    result = await run_bottleneck_analyzer(state)
    return {"bottlenecks": result.get("bottlenecks", [])}


@router.post("/improvement-generator/{project_id}")
async def run_improvement_ep(project_id: str):
    state = _empty_state(project_id)
    result = await run_improvement_generator(state)
    return {"improvements": result.get("improvements", [])}


@router.post("/future-state-designer/{project_id}")
async def run_future_state_ep(project_id: str, req: RunRequest):
    state = _empty_state(project_id)
    result = await run_future_state_designer(state)
    fs = result.get("future_states", {})
    return fs if req.scenario == "all" else {req.scenario: fs.get(req.scenario)}


@router.post("/business-case-builder/{project_id}")
async def run_bc_ep(project_id: str, req: RunRequest):
    state = _empty_state(project_id)
    fs_result = await run_future_state_designer(state)
    bc_result = await run_business_case_builder(fs_result)
    bc = bc_result.get("business_cases", {})
    return bc if req.scenario == "all" else {req.scenario: bc.get(req.scenario)}


@router.post("/benchmark-agent/{project_id}")
async def run_benchmark_ep(project_id: str):
    state = _empty_state(project_id)
    result = await run_benchmark_agent(state)
    return {"benchmarks": result.get("benchmarks", {})}
