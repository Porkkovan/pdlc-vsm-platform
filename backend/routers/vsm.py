from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from ..database.db import get_db
from ..database.models import VSMSnapshot

router = APIRouter(prefix="/vsm", tags=["vsm"])


class VSMSave(BaseModel):
    source:    Optional[str] = "manual"
    vsm_data:  dict
    overrides: Optional[dict] = None


@router.post("/{project_id}", status_code=201)
async def save_vsm(project_id: str, data: VSMSave, db: AsyncSession = Depends(get_db)):
    snap = VSMSnapshot(
        project_id=project_id,
        source=data.source,
        vsm_data=data.vsm_data,
        overrides=data.overrides,
        summary=data.vsm_data.get("summary")
    )
    db.add(snap)
    await db.commit()
    await db.refresh(snap)
    return {"id": snap.id, "project_id": project_id, "source": snap.source}


@router.get("/{project_id}")
async def get_vsm(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(VSMSnapshot).where(VSMSnapshot.project_id == project_id).order_by(VSMSnapshot.created_at.desc()).limit(1)
    )
    snap = result.scalar_one_or_none()
    if not snap:
        raise HTTPException(404, "No VSM data found for this project")
    return {"vsm_data": snap.vsm_data, "overrides": snap.overrides, "source": snap.source, "created_at": str(snap.created_at)}


@router.put("/{project_id}")
async def update_vsm(project_id: str, data: VSMSave, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(VSMSnapshot).where(VSMSnapshot.project_id == project_id).order_by(VSMSnapshot.created_at.desc()).limit(1)
    )
    snap = result.scalar_one_or_none()
    if snap:
        snap.vsm_data  = data.vsm_data
        snap.overrides = data.overrides
        await db.commit()
        return {"updated": True}
    # If no existing snapshot, create one
    return await save_vsm(project_id, data, db)


@router.get("/{project_id}/metrics")
async def get_metrics(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(VSMSnapshot).where(VSMSnapshot.project_id == project_id).order_by(VSMSnapshot.created_at.desc()).limit(1)
    )
    snap = result.scalar_one_or_none()
    if not snap:
        raise HTTPException(404, "No VSM data found")
    return snap.summary or {}
