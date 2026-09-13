"""HITL review & approval for each platform step output."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..database.db import get_db
from ..database.models import StepReview

router = APIRouter(prefix="/step-reviews", tags=["step-reviews"])

STEP_KEYS = [
    {"key": "current_vsm", "label": "Current State VSM", "description": "VSM metrics and flow analysis"},
    {"key": "bottlenecks", "label": "Bottleneck Analysis", "description": "Identified flow blockers and root causes"},
    {"key": "improvements", "label": "Improvement Actions", "description": "Suggested improvements for each bottleneck"},
    {"key": "future_state", "label": "Future State Design", "description": "AI-designed future state VSM"},
    {"key": "business_case", "label": "Business Case", "description": "ROI, investment, and payback analysis"},
    {"key": "target_state", "label": "Target State Studio", "description": "Platform selection and roadmap"},
    {"key": "recommendations", "label": "Recommendations", "description": "Playbook and contextualised recommendations"},
    {"key": "dora_assessment", "label": "DORA Assessment", "description": "DevOps performance baseline"},
    {"key": "devops_maturity", "label": "DevOps Maturity", "description": "DevOps maturity assessment"},
    {"key": "manual_assessment", "label": "Manual Assessment", "description": "Manual PDLC maturity checklist"},
]


class ReviewCreate(BaseModel):
    status: str = "draft"
    reviewer_notes: Optional[str] = None
    edited_content: Optional[dict] = None
    reviewed_by: Optional[str] = None


@router.get("/steps")
async def get_step_keys():
    return STEP_KEYS


@router.get("/{project_id}")
async def list_reviews(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StepReview).where(StepReview.project_id == project_id)
    )
    reviews = result.scalars().all()
    return {r.step_key: _to_dict(r) for r in reviews}


@router.get("/{project_id}/{step_key}")
async def get_review(project_id: str, step_key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StepReview).where(
            StepReview.project_id == project_id,
            StepReview.step_key == step_key
        )
    )
    review = result.scalar_one_or_none()
    if not review:
        return {"step_key": step_key, "status": "draft", "reviewer_notes": None, "edited_content": None}
    return _to_dict(review)


@router.put("/{project_id}/{step_key}")
async def upsert_review(project_id: str, step_key: str, body: ReviewCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StepReview).where(
            StepReview.project_id == project_id,
            StepReview.step_key == step_key
        )
    )
    review = result.scalar_one_or_none()
    now = datetime.utcnow()
    if review:
        review.status = body.status
        review.reviewer_notes = body.reviewer_notes
        review.edited_content = body.edited_content
        review.reviewed_by = body.reviewed_by
        review.reviewed_at = now if body.status in ("approved", "rejected", "reviewed") else review.reviewed_at
        review.updated_at = now
    else:
        review = StepReview(
            project_id=project_id,
            step_key=step_key,
            status=body.status,
            reviewer_notes=body.reviewer_notes,
            edited_content=body.edited_content,
            reviewed_by=body.reviewed_by,
            reviewed_at=now if body.status in ("approved", "rejected", "reviewed") else None,
        )
        db.add(review)
    await db.commit()
    await db.refresh(review)
    return _to_dict(review)


def _to_dict(r: StepReview) -> dict:
    return {
        "id": r.id,
        "project_id": r.project_id,
        "step_key": r.step_key,
        "status": r.status,
        "reviewer_notes": r.reviewer_notes,
        "edited_content": r.edited_content,
        "reviewed_by": r.reviewed_by,
        "reviewed_at": r.reviewed_at.isoformat() if r.reviewed_at else None,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }
