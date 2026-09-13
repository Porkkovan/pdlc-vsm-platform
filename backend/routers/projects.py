from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

from ..database.db import get_db
from ..database.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name:           str
    organization:   Optional[str] = None
    portfolio:      Optional[str] = None
    product_group:  Optional[str] = None
    product:        Optional[str] = None
    team:           Optional[str] = None
    industry:       Optional[str] = None
    portfolios:     Optional[List[str]] = None
    product_groups: Optional[List[Any]] = None
    alm_tool:       Optional[str] = None
    alm_config:     Optional[dict] = None
    option_a_parent_map: Optional[dict] = None


class ProjectUpdate(ProjectCreate):
    name: Optional[str] = None


class OptionAParentMapUpdate(BaseModel):
    option_a_parent_map: dict


class CostModelOverridesUpdate(BaseModel):
    cost_model_overrides: dict


@router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    return [_to_dict(p) for p in result.scalars().all()]


@router.post("/", status_code=201)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(**data.model_dump(exclude_none=True))
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return _to_dict(project)


@router.get("/{project_id}")
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return _to_dict(project)


@router.put("/{project_id}")
async def update_project(project_id: str, data: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(project, k, v)
    project.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(project)
    return _to_dict(project)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    await db.delete(project)
    await db.commit()


@router.get("/{project_id}/option-a-parent-map")
async def get_option_a_parent_map(project_id: str, db: AsyncSession = Depends(get_db)):
    """Return the org-specific Option A → Option B agent lineage map for a project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return {"option_a_parent_map": project.option_a_parent_map or {}}


@router.put("/{project_id}/option-a-parent-map")
async def update_option_a_parent_map(
    project_id: str, data: OptionAParentMapUpdate, db: AsyncSession = Depends(get_db)
):
    """Replace the project's agent → Option A parent-tool lineage map."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    project.option_a_parent_map = data.option_a_parent_map
    project.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(project)
    return {"option_a_parent_map": project.option_a_parent_map or {}}


@router.get("/{project_id}/cost-model")
async def get_cost_model(project_id: str, db: AsyncSession = Depends(get_db)):
    """Return the project's effective cost model (defaults + per-project overrides) plus a rolled-up summary."""
    from ..agents.business_case_builder.agent import merge_cost_model, compute_cost_summary, TOKEN_OPTIMIZATIONS
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    overrides = project.cost_model_overrides or {}
    cost_model = merge_cost_model(overrides)
    return {
        "cost_model_overrides":  overrides,
        "cost_model":            cost_model,
        "summary":               compute_cost_summary(cost_model),
        "token_optimizations":   list(TOKEN_OPTIMIZATIONS.values()),
    }


@router.put("/{project_id}/cost-model")
async def update_cost_model(
    project_id: str, data: CostModelOverridesUpdate, db: AsyncSession = Depends(get_db)
):
    """Replace the project's cost model overrides. Returns the merged model and summary."""
    from ..agents.business_case_builder.agent import merge_cost_model, compute_cost_summary
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    project.cost_model_overrides = data.cost_model_overrides
    project.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(project)
    cost_model = merge_cost_model(project.cost_model_overrides or {})
    return {
        "cost_model_overrides": project.cost_model_overrides or {},
        "cost_model":           cost_model,
        "summary":              compute_cost_summary(cost_model),
    }


def _to_dict(p: Project) -> dict:
    return {
        "id":            p.id,
        "name":          p.name,
        "organization":  p.organization,
        "portfolio":     p.portfolio,
        "product_group": p.product_group,
        "product":       p.product,
        "team":          p.team,
        "industry":      p.industry,
        "portfolios":    p.portfolios or [],
        "product_groups": p.product_groups or [],
        "alm_tool":      p.alm_tool,
        "alm_config":    p.alm_config or {},
        "option_a_parent_map": p.option_a_parent_map or {},
        "created_at":    str(p.created_at),
    }
