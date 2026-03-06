from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..database.db import get_db
from ..database.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name:          str
    organization:  Optional[str] = None
    portfolio:     Optional[str] = None
    product_group: Optional[str] = None
    team:          Optional[str] = None
    industry:      Optional[str] = None


class ProjectUpdate(ProjectCreate):
    pass


@router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    return [_to_dict(p) for p in result.scalars().all()]


@router.post("/", status_code=201)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(**data.model_dump())
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


def _to_dict(p: Project) -> dict:
    return {
        "id": p.id, "name": p.name, "organization": p.organization,
        "portfolio": p.portfolio, "product_group": p.product_group,
        "team": p.team, "industry": p.industry,
        "alm_tool": p.alm_tool, "created_at": str(p.created_at)
    }
