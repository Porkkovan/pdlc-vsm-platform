"""
DevOps Maturity Assessment API Router
Endpoints for creating assessments, running AI scoring, managing responses,
and tracking action plan items.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import uuid
import logging

from ..database.db import get_db, AsyncSessionLocal
from ..database.models import DevOpsAssessment, AssessmentActionItem
from ..agents.devops_maturity_agent.agent import run_devops_maturity_assessment
from ..agents.devops_maturity_questions import QUESTIONS, DIMENSIONS, SOURCE_TYPES

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/devops-maturity", tags=["DevOps Maturity"])

# In-memory status store for running assessments
_assessment_runs: dict = {}


# ─── Pydantic Models ─────────────────────────────────────────────────

class SourceConfig(BaseModel):
    type: str
    url: str
    label: Optional[str] = None
    token: Optional[str] = None


class CreateAssessmentRequest(BaseModel):
    project_id: Optional[str] = None
    organization: str
    portfolio: str
    product_group: str
    team_name: str
    industry: Optional[str] = "Financial Services"
    sources: list[SourceConfig] = []
    notes: Optional[str] = None


class UpdateResponseRequest(BaseModel):
    responses: dict[str, Any]   # {question_id: {manual_score, notes}}


class UpdateActionItemRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible: Optional[str] = None
    target_date: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[str] = None


# ─── Assessment CRUD ─────────────────────────────────────────────────

@router.post("/assessments")
async def create_assessment(body: CreateAssessmentRequest, db: AsyncSession = Depends(get_db)):
    assessment = DevOpsAssessment(
        id=str(uuid.uuid4()),
        project_id=body.project_id,
        organization=body.organization,
        portfolio=body.portfolio,
        product_group=body.product_group,
        team_name=body.team_name,
        industry=body.industry,
        sources=[s.model_dump() for s in body.sources],
        notes=body.notes,
        status="pending",
        responses={},
        result=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    return _assessment_to_dict(assessment)


@router.get("/assessments/project/{project_id}")
async def list_assessments_by_project(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DevOpsAssessment)
        .where(DevOpsAssessment.project_id == project_id)
        .order_by(DevOpsAssessment.created_at.desc())
    )
    return [_assessment_to_dict(a) for a in result.scalars().all()]


@router.get("/assessments/all")
async def list_all_assessments(db: AsyncSession = Depends(get_db)):
    """List all assessments (for picker)."""
    result = await db.execute(
        select(DevOpsAssessment).order_by(DevOpsAssessment.created_at.desc())
    )
    return [_assessment_to_dict(a) for a in result.scalars().all()]


@router.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: str, db: AsyncSession = Depends(get_db)):
    assessment = await db.get(DevOpsAssessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    # Merge in-memory run status if still running
    run_info = _assessment_runs.get(assessment_id, {})
    d = _assessment_to_dict(assessment)
    if run_info.get("status") == "running":
        d["status"] = "running"
    return d


@router.put("/assessments/{assessment_id}")
async def update_assessment(
    assessment_id: str,
    body: CreateAssessmentRequest,
    db: AsyncSession = Depends(get_db)
):
    assessment = await db.get(DevOpsAssessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.organization  = body.organization
    assessment.portfolio     = body.portfolio
    assessment.product_group = body.product_group
    assessment.team_name     = body.team_name
    assessment.industry      = body.industry
    assessment.sources       = [s.model_dump() for s in body.sources]
    assessment.notes         = body.notes
    assessment.updated_at    = datetime.utcnow()

    await db.commit()
    await db.refresh(assessment)
    return _assessment_to_dict(assessment)


@router.delete("/assessments/{assessment_id}")
async def delete_assessment(assessment_id: str, db: AsyncSession = Depends(get_db)):
    assessment = await db.get(DevOpsAssessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    await db.delete(assessment)
    await db.commit()
    return {"message": "Assessment deleted"}


# ─── Run AI Scoring ──────────────────────────────────────────────────

@router.post("/assessments/{assessment_id}/run")
async def run_assessment(
    assessment_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Trigger AI-powered assessment scoring in the background."""
    assessment = await db.get(DevOpsAssessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.status = "running"
    assessment.updated_at = datetime.utcnow()
    await db.commit()

    _assessment_runs[assessment_id] = {"status": "running"}

    async def _run():
        try:
            async with AsyncSessionLocal() as session:
                a = await session.get(DevOpsAssessment, assessment_id)
                if not a:
                    return

                team_context = {
                    "organization": a.organization,
                    "portfolio": a.portfolio,
                    "product_group": a.product_group,
                    "team_name": a.team_name,
                    "industry": a.industry,
                }

                result = await run_devops_maturity_assessment(
                    team_context=team_context,
                    sources=a.sources or [],
                    existing_responses=a.responses or {}
                )

                a.result = result
                a.status = "complete"
                a.updated_at = datetime.utcnow()

                # Clear old action items
                old_items = await session.execute(
                    select(AssessmentActionItem).where(
                        AssessmentActionItem.assessment_id == assessment_id
                    )
                )
                for item in old_items.scalars().all():
                    await session.delete(item)

                # Create new action items
                for action in result.get("action_items", []):
                    item = AssessmentActionItem(
                        id=str(uuid.uuid4()),
                        assessment_id=assessment_id,
                        question_id=action.get("question_id", ""),
                        dimension=action.get("dimension", ""),
                        competency=action.get("competency", ""),
                        title=action.get("title", ""),
                        description=action.get("description", ""),
                        priority=action.get("priority", "Medium"),
                        current_score=action.get("current_score", 0),
                        target_score=action.get("target_score", 0),
                        current_level=action.get("current_level", ""),
                        target_level=action.get("target_level", ""),
                        suggested_actions=action.get("suggested_actions", []),
                        responsible=action.get("responsible_role", action.get("responsible", "")),
                        target_date=action.get("target_date", ""),
                        status="Open",
                        notes="",
                        effort_estimate=action.get("effort_estimate", ""),
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    session.add(item)

                await session.commit()
                _assessment_runs[assessment_id] = {"status": "complete"}
                logger.info(f"Assessment {assessment_id} completed")

        except Exception as e:
            logger.error(f"Assessment {assessment_id} failed: {e}")
            _assessment_runs[assessment_id] = {"status": "failed", "error": str(e)}
            async with AsyncSessionLocal() as session:
                a = await session.get(DevOpsAssessment, assessment_id)
                if a:
                    a.status = "failed"
                    a.updated_at = datetime.utcnow()
                    await session.commit()

    background_tasks.add_task(_run)
    return {"message": "Assessment scoring started", "assessment_id": assessment_id, "status": "running"}


# ─── Manual Responses ────────────────────────────────────────────────

@router.patch("/assessments/{assessment_id}/responses")
async def update_responses(
    assessment_id: str,
    body: UpdateResponseRequest,
    db: AsyncSession = Depends(get_db)
):
    """Save manual scores and notes for individual questions."""
    assessment = await db.get(DevOpsAssessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    current = assessment.responses or {}
    current.update(body.responses)
    assessment.responses = current
    assessment.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(assessment)
    return {"message": "Responses saved", "response_count": len(current)}


# ─── Action Items (Action Plan) ──────────────────────────────────────

@router.get("/assessments/{assessment_id}/action-items")
async def get_action_items(assessment_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AssessmentActionItem)
        .where(AssessmentActionItem.assessment_id == assessment_id)
        .order_by(AssessmentActionItem.dimension, AssessmentActionItem.priority)
    )
    return [_action_to_dict(item) for item in result.scalars().all()]


@router.patch("/assessments/{assessment_id}/action-items/{item_id}")
async def update_action_item(
    assessment_id: str,
    item_id: str,
    body: UpdateActionItemRequest,
    db: AsyncSession = Depends(get_db)
):
    """Update an action plan item for continuous tracking."""
    result = await db.execute(
        select(AssessmentActionItem).where(
            AssessmentActionItem.id == item_id,
            AssessmentActionItem.assessment_id == assessment_id
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")

    if body.title is not None:       item.title = body.title
    if body.description is not None: item.description = body.description
    if body.responsible is not None: item.responsible = body.responsible
    if body.target_date is not None: item.target_date = body.target_date
    if body.status is not None:      item.status = body.status
    if body.notes is not None:       item.notes = body.notes
    if body.priority is not None:    item.priority = body.priority
    item.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(item)
    return _action_to_dict(item)


@router.post("/assessments/{assessment_id}/action-items")
async def create_action_item(
    assessment_id: str,
    body: UpdateActionItemRequest,
    db: AsyncSession = Depends(get_db)
):
    """Manually add a custom action item."""
    item = AssessmentActionItem(
        id=str(uuid.uuid4()),
        assessment_id=assessment_id,
        question_id="custom",
        dimension="Custom",
        competency="",
        title=body.title or "Custom Action",
        description=body.description or "",
        priority=body.priority or "Medium",
        current_score=0,
        target_score=0,
        current_level="",
        target_level="",
        suggested_actions=[],
        responsible=body.responsible or "",
        target_date=body.target_date or "",
        status=body.status or "Open",
        notes=body.notes or "",
        effort_estimate="",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return _action_to_dict(item)


@router.delete("/assessments/{assessment_id}/action-items/{item_id}")
async def delete_action_item(
    assessment_id: str,
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AssessmentActionItem).where(
            AssessmentActionItem.id == item_id,
            AssessmentActionItem.assessment_id == assessment_id
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    await db.delete(item)
    await db.commit()
    return {"message": "Deleted"}


# ─── Questions Reference ─────────────────────────────────────────────

@router.get("/questions")
async def get_questions():
    """Get all 73 assessment questions grouped by dimension."""
    grouped = {}
    for q in QUESTIONS:
        dim = q["dimension"]
        if dim not in grouped:
            grouped[dim] = []
        grouped[dim].append(q)
    return {
        "total": len(QUESTIONS),
        "dimensions": DIMENSIONS,
        "source_types": SOURCE_TYPES,
        "questions_by_dimension": grouped
    }


# ─── VSM Integration ─────────────────────────────────────────────────

@router.get("/assessments/{assessment_id}/vsm-input")
async def get_vsm_input(assessment_id: str, db: AsyncSession = Depends(get_db)):
    """Export assessment findings as structured input for Current State VSM."""
    assessment = await db.get(DevOpsAssessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    if not assessment.result:
        raise HTTPException(status_code=400, detail="Assessment not yet scored — run scoring first")

    summary     = assessment.result.get("summary", {})
    inferences  = assessment.result.get("inferences", {})
    critical    = summary.get("critical_gaps", [])

    return {
        "team": assessment.team_name,
        "overall_maturity": summary.get("overall_maturity_level", "Unknown"),
        "overall_score": summary.get("overall_score", 0),
        "dimension_scores": {
            dim: data.get("average", 0)
            for dim, data in summary.get("dimension_scores", {}).items()
        },
        "bottlenecks": [
            {
                "source": "DevOps Maturity Assessment",
                "dimension": gap.get("dimension", ""),
                "competency": gap.get("competency", ""),
                "description": gap.get("title", ""),
                "severity": "Critical" if gap.get("current_score", 0) <= 2 else "High",
            }
            for gap in critical[:10]
        ],
        "low_maturity_areas": [
            inf for dim_infs in inferences.values()
            for inf in dim_infs
            if inf.get("level_category") == "low"
        ][:15]
    }


# ─── Helpers ─────────────────────────────────────────────────────────

def _assessment_to_dict(a) -> dict:
    return {
        "id": a.id,
        "project_id": a.project_id,
        "organization": a.organization,
        "portfolio": a.portfolio,
        "product_group": a.product_group,
        "team_name": a.team_name,
        "industry": a.industry,
        "sources": a.sources or [],
        "notes": a.notes,
        "status": a.status,
        "responses": a.responses or {},
        "result": a.result,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
    }


def _action_to_dict(item) -> dict:
    return {
        "id": item.id,
        "assessment_id": item.assessment_id,
        "question_id": item.question_id,
        "dimension": item.dimension,
        "competency": item.competency,
        "title": item.title,
        "description": item.description,
        "priority": item.priority,
        "current_score": item.current_score,
        "target_score": item.target_score,
        "current_level": item.current_level,
        "target_level": item.target_level,
        "suggested_actions": item.suggested_actions or [],
        "responsible": item.responsible,
        "target_date": item.target_date,
        "status": item.status,
        "notes": item.notes,
        "effort_estimate": item.effort_estimate,
        "created_at": item.created_at.isoformat() if item.created_at else None,
        "updated_at": item.updated_at.isoformat() if item.updated_at else None,
    }
