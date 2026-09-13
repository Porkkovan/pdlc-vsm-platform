"""
Agents Router
Endpoints to trigger individual agents or the full multi-agent pipeline.
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from ..agents.orchestrator.graph import run_full_analysis
from ..agents.vsm_analyzer.agent      import run_vsm_analyzer
from ..agents.bottleneck_analyzer.agent import run_bottleneck_analyzer
from ..agents.improvement_generator.agent import run_improvement_generator
from ..agents.future_state_designer.agent import run_future_state_designer
from ..agents.business_case_builder.agent import run_business_case_builder
from ..agents.benchmark_agent.agent   import run_benchmark_agent
from ..agents.playbook_contextualizer.agent import run_playbook_contextualizer
from ..agents.automation_classifier.agent import classify_activities
from ..database.db import get_db, AsyncSessionLocal
from ..database.models import VSMSnapshot, AnalysisRun, ManualAssessmentResponse

router = APIRouter(prefix="/agents", tags=["agents"])

# In-memory run store (use Redis in production)
_runs: dict = {}


class RunRequest(BaseModel):
    scenario: Optional[str] = "all"  # option-a, option-b, option-c, or all


class AnalysisRequest(BaseModel):
    dora_calibration: Optional[dict] = None


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


async def _load_vsm_state(project_id: str, db: AsyncSession) -> dict:
    """Build state dict with VSM snapshot loaded from DB."""
    state = _empty_state(project_id)
    snap_result = await db.execute(
        select(VSMSnapshot)
        .where(VSMSnapshot.project_id == project_id)
        .order_by(VSMSnapshot.created_at.desc())
        .limit(1)
    )
    snap = snap_result.scalar_one_or_none()
    if snap:
        state["vsm_data"] = snap.vsm_data or {}
        state["alm_raw_data"] = snap.raw_data or {}
        state["overrides"] = snap.overrides or {}
    return state


@router.post("/run-analysis/{project_id}")
async def run_analysis(project_id: str, background_tasks: BackgroundTasks, req: AnalysisRequest = None):
    """Kick off the full multi-agent pipeline in the background."""
    run_id = str(uuid.uuid4())
    dora_calibration = (req.dora_calibration or {}) if req else {}
    _runs[run_id] = {"status": "running", "project_id": project_id}

    async def _run():
        # Create DB record for this run
        async with AsyncSessionLocal() as db:
            db_run = AnalysisRun(
                id=run_id,
                project_id=project_id,
                status="running",
                created_at=datetime.utcnow()
            )
            db.add(db_run)
            await db.commit()

        try:
            result = await run_full_analysis(project_id, {}, {}, dora_calibration=dora_calibration)
            _runs[run_id] = {"status": "complete", "result": result}
            # Persist result to DB
            async with AsyncSessionLocal() as db:
                db_run = await db.get(AnalysisRun, run_id)
                if db_run:
                    db_run.status = "complete"
                    db_run.result = result
                    db_run.completed_at = datetime.utcnow()
                    await db.commit()
        except Exception as e:
            _runs[run_id] = {"status": "failed", "error": str(e)}
            async with AsyncSessionLocal() as db:
                db_run = await db.get(AnalysisRun, run_id)
                if db_run:
                    db_run.status = "failed"
                    db_run.error = str(e)
                    db_run.completed_at = datetime.utcnow()
                    await db.commit()

    background_tasks.add_task(_run)
    return {"run_id": run_id, "status": "started"}


@router.get("/status/{run_id}")
async def get_status(run_id: str):
    run = _runs.get(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    return {"run_id": run_id, **run}


@router.get("/result/{project_id}")
async def get_result(project_id: str, db: AsyncSession = Depends(get_db)):
    """Get the latest analysis result for a project."""
    # Check in-memory first (fastest)
    run = next((r for r in reversed(list(_runs.values())) if r.get("project_id") == project_id and r.get("status") == "complete"), None)
    if run:
        return run.get("result", {})
    # Fall back to DB (survives restarts)
    db_result = await db.execute(
        select(AnalysisRun)
        .where(AnalysisRun.project_id == project_id, AnalysisRun.status == "complete")
        .order_by(AnalysisRun.created_at.desc())
        .limit(1)
    )
    db_run = db_result.scalar_one_or_none()
    if not db_run:
        raise HTTPException(404, "No completed analysis found")
    return db_run.result or {}


@router.get("/history/{project_id}")
async def get_history(project_id: str):
    """Get all runs for a project."""
    return [{"run_id": k, **v} for k, v in _runs.items() if v.get("project_id") == project_id]


# Individual agent endpoints
@router.post("/vsm-analyzer/{project_id}")
async def run_vsm_analyzer_ep(project_id: str, db: AsyncSession = Depends(get_db)):
    state = await _load_vsm_state(project_id, db)
    result = await run_vsm_analyzer(state)
    return {"metrics": result.get("metrics"), "narrative": result.get("narrative")}


@router.post("/bottleneck-analyzer/{project_id}")
async def run_bottleneck_ep(project_id: str, db: AsyncSession = Depends(get_db)):
    state = await _load_vsm_state(project_id, db)
    result = await run_bottleneck_analyzer(state)
    return {"bottlenecks": result.get("bottlenecks", [])}


@router.post("/improvement-generator/{project_id}")
async def run_improvement_ep(project_id: str, db: AsyncSession = Depends(get_db)):
    state = await _load_vsm_state(project_id, db)
    result = await run_improvement_generator(state)
    return {"improvements": result.get("improvements", [])}


@router.post("/future-state-designer/{project_id}")
async def run_future_state_ep(project_id: str, req: RunRequest, db: AsyncSession = Depends(get_db)):
    state = await _load_vsm_state(project_id, db)
    result = await run_future_state_designer(state)
    fs = result.get("future_states", {})
    return fs if req.scenario == "all" else {req.scenario: fs.get(req.scenario)}


@router.post("/business-case-builder/{project_id}")
async def run_bc_ep(project_id: str, req: RunRequest, db: AsyncSession = Depends(get_db)):
    state = await _load_vsm_state(project_id, db)
    fs_result = await run_future_state_designer(state)
    bc_result = await run_business_case_builder(fs_result)
    bc = bc_result.get("business_cases", {})
    return bc if req.scenario == "all" else {req.scenario: bc.get(req.scenario)}


@router.post("/benchmark-agent/{project_id}")
async def run_benchmark_ep(project_id: str, db: AsyncSession = Depends(get_db)):
    state = await _load_vsm_state(project_id, db)
    result = await run_benchmark_agent(state)
    return {"benchmarks": result.get("benchmarks", {})}


class SeedResultRequest(BaseModel):
    result: dict
    agents_run: Optional[list] = None


@router.post("/seed-result/{project_id}", status_code=201)
async def seed_analysis_result(project_id: str, req: SeedResultRequest, db: AsyncSession = Depends(get_db)):
    """Insert a pre-built analysis result as a completed run (demo seed only)."""
    run_id = str(uuid.uuid4())
    now    = datetime.utcnow()
    db_run = AnalysisRun(
        id           = run_id,
        project_id   = project_id,
        status       = "complete",
        agents_run   = req.agents_run or [],
        result       = req.result,
        created_at   = now,
        completed_at = now,
    )
    db.add(db_run)
    await db.commit()
    _runs[run_id] = {"status": "complete", "project_id": project_id, "result": req.result}
    return {"id": run_id, "project_id": project_id, "status": "complete"}


class PlaybookContextRequest(BaseModel):
    scenario_id:    str
    scenario_label: str
    analysis_context: dict = {}
    team_context:   dict = {}
    documents:      dict = {}


@router.post("/contextualise-playbook/{project_id}")
async def contextualise_playbook(project_id: str, req: PlaybookContextRequest):
    """Generate a personalised implementation playbook from team context + analysis data."""
    result = await run_playbook_contextualizer(
        scenario_id=req.scenario_id,
        scenario_label=req.scenario_label,
        analysis_context=req.analysis_context,
        team_context=req.team_context,
        documents=req.documents,
    )
    return result


# ── Automation Classifier ────────────────────────────────────────────────────

@router.post("/classify-automation/{project_id}")
async def classify_automation(project_id: str, db: AsyncSession = Depends(get_db)):
    """
    Classify all 36 PDLC activities as Manual / RPA / AI-Assisted / AI-Agent.
    Uses configured data sources, uploaded documents, VSM metrics, and
    manual assessment responses as evidence.
    """
    # Load VSM data
    state = await _load_vsm_state(project_id, db)
    vsm_data = state.get("vsm_data")

    # Load manual assessment responses
    resp_result = await db.execute(
        select(ManualAssessmentResponse)
        .where(ManualAssessmentResponse.project_id == project_id)
    )
    resp_rows = resp_result.scalars().all()
    manual_responses = {
        r.question_id: {"response": r.response, "notes": r.notes}
        for r in resp_rows
    }

    result = await classify_activities(
        project_id=project_id,
        vsm_data=vsm_data,
        manual_responses=manual_responses,
    )
    return result


@router.get("/automation-classifications/{project_id}")
async def get_automation_classifications(project_id: str, db: AsyncSession = Depends(get_db)):
    """GET endpoint — same as classify but cached-friendly (runs fresh each time for now)."""
    state = await _load_vsm_state(project_id, db)
    resp_result = await db.execute(
        select(ManualAssessmentResponse)
        .where(ManualAssessmentResponse.project_id == project_id)
    )
    resp_rows = resp_result.scalars().all()
    manual_responses = {
        r.question_id: {"response": r.response, "notes": r.notes}
        for r in resp_rows
    }
    return await classify_activities(
        project_id=project_id,
        vsm_data=state.get("vsm_data"),
        manual_responses=manual_responses,
    )
