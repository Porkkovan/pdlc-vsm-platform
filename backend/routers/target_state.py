"""
Target State Studio router.

Lets a customer define their North-Star / target ADLC state by picking a delivery
platform (Home-grown = US Bank target, COTS, or service-provider — STUMP excluded),
composing the agents/tools/human-roles/hierarchy, choosing how to get there
(1-go / 1 / 2 interim steps via the L1–L5 ladder), and tracking progress. The
roadmap + business case reuse the existing cost model and platform deltas.
"""
from typing import Optional, List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..database.db import get_db
from ..database.models import TargetStateConfig, Project, VSMSnapshot
from ..agents.business_case_builder.agent import (target_state_platforms,
                                                  C_PLATFORM_OPTIONS, PLATFORM_KIND)
from ..agents.target_state.catalog import INTERIM_LADDER, RISK_APPETITE
from ..agents.target_state.roadmap import build_roadmap, suggest_interims
from ..agents.target_state.progress import compute_progress
from ..agents.target_state.compare import compare_platforms
from ..agents.target_state.platform_insights import get_platform_insight, get_all_insights
from ..agents.target_state.dynamic_ladder import get_dynamic_ladder

router = APIRouter(prefix="/target-state", tags=["target-state"])


# ── Schemas ───────────────────────────────────────────────────────────────────
class TargetStateConfigIn(BaseModel):
    platform: Optional[str] = None
    target_composition: Optional[dict] = None
    current_level: Optional[int] = 0
    target_level: Optional[int] = 5
    interim_count: Optional[int] = 0
    interim_levels: Optional[List[int]] = None
    risk_appetite: Optional[str] = "medium"
    business_case_overrides: Optional[dict] = None


class RoadmapIn(BaseModel):
    platform: str = "homegrown"
    current_level: int = 0
    target_level: int = 5
    interim_count: Optional[int] = None       # None = auto-suggest
    risk_appetite: str = "medium"
    maturity_band: Optional[str] = None        # from DevOps assessment, for auto-suggest


async def _get_project(db: AsyncSession, project_id: str) -> Project:
    proj = (await db.execute(select(Project).where(Project.id == project_id))).scalar_one_or_none()
    if not proj:
        raise HTTPException(404, f"Project {project_id} not found")
    return proj


def _cfg_dict(c: TargetStateConfig) -> dict:
    return {
        "id": c.id, "project_id": c.project_id, "platform": c.platform,
        "platform_kind": c.platform_kind, "target_composition": c.target_composition or {},
        "current_level": c.current_level, "target_level": c.target_level,
        "interim_count": c.interim_count, "interim_levels": c.interim_levels or [],
        "risk_appetite": c.risk_appetite, "business_case_overrides": c.business_case_overrides or {},
        "updated_at": c.updated_at.isoformat() + "Z" if c.updated_at else None,
    }


# ── Reference ─────────────────────────────────────────────────────────────────
@router.get("/platforms")
async def get_platforms():
    """Target-state delivery platform catalog (excludes STUMP)."""
    return {"platforms": target_state_platforms()}


@router.get("/ladder")
async def get_ladder():
    """L1–L5 interim maturity ladder + risk-appetite options."""
    return {"ladder": INTERIM_LADDER, "risk_appetite": RISK_APPETITE}


@router.get("/compare")
async def compare(risk_appetite: str = "medium"):
    """Parameter comparison + weighted recommendation across target-state platforms."""
    return compare_platforms(risk_appetite)


@router.get("/platforms/{platform_id}")
async def get_platform_detail(platform_id: str):
    p = C_PLATFORM_OPTIONS.get(platform_id)
    if not p or platform_id == "stump":
        raise HTTPException(404, f"Platform '{platform_id}' not available for target state")
    return {**p, "kind": PLATFORM_KIND.get(platform_id, "cots"),
            "is_us_bank_target": platform_id == "homegrown"}


# ── Platform insights & dynamic ladder (WS6 / WS7) ──────────────────────────
@router.get("/platform-insights/all")
async def all_platform_insights():
    """Implementation details (agents, tools, architecture) for every target-state platform."""
    return get_all_insights()


@router.get("/platform-insights/{platform_id}")
async def platform_insight_detail(platform_id: str):
    """Implementation details for a single platform, including agent catalog and differentiators."""
    ins = get_platform_insight(platform_id)
    if not ins:
        raise HTTPException(404, f"No insights for platform: {platform_id}")
    return ins


@router.get("/dynamic-ladder/{platform_id}")
async def dynamic_ladder(platform_id: str):
    """L1-L5 ladder enriched with platform-specific People/Process/Tools/Outcomes/Investment perspectives."""
    return {"ladder": get_dynamic_ladder(platform_id)}


# ── Config (load / save) ──────────────────────────────────────────────────────
async def _load_cfg(db: AsyncSession, project_id: str) -> Optional[TargetStateConfig]:
    return (await db.execute(
        select(TargetStateConfig).where(TargetStateConfig.project_id == project_id)
        .order_by(TargetStateConfig.updated_at.desc()).limit(1))).scalar_one_or_none()


@router.get("/{project_id}")
async def get_config(project_id: str, db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    c = await _load_cfg(db, project_id)
    return _cfg_dict(c) if c else {"project_id": project_id, "configured": False}


@router.put("/{project_id}")
async def save_config(project_id: str, body: TargetStateConfigIn,
                      db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    c = await _load_cfg(db, project_id)
    if not c:
        c = TargetStateConfig(project_id=project_id)
        db.add(c)
    if body.platform is not None:
        c.platform = body.platform
        c.platform_kind = PLATFORM_KIND.get(body.platform, "cots")
    if body.target_composition is not None:
        c.target_composition = body.target_composition
    if body.current_level is not None:
        c.current_level = body.current_level
    if body.target_level is not None:
        c.target_level = body.target_level
    if body.interim_count is not None:
        c.interim_count = body.interim_count
    if body.interim_levels is not None:
        c.interim_levels = body.interim_levels
    if body.risk_appetite is not None:
        c.risk_appetite = body.risk_appetite
    if body.business_case_overrides is not None:
        c.business_case_overrides = body.business_case_overrides
    await db.commit()
    await db.refresh(c)
    return _cfg_dict(c)


# ── Compose / roadmap / progress ──────────────────────────────────────────────
@router.post("/{project_id}/compose")
async def compose(project_id: str, platform: str = "homegrown",
                  db: AsyncSession = Depends(get_db)):
    """
    Return the platform overlay (agent construction, tooling, ops team, phasing) +
    the ladder so the frontend can seed the editable composition from the US-Bank
    target (Option C) and overlay platform-specific deltas.
    """
    proj = await _get_project(db, project_id)
    p = C_PLATFORM_OPTIONS.get(platform)
    if not p or platform == "stump":
        raise HTTPException(404, f"Platform '{platform}' not available for target state")
    return {
        "platform": {**p, "kind": PLATFORM_KIND.get(platform, "cots"),
                     "is_us_bank_target": platform == "homegrown"},
        "ladder": INTERIM_LADDER,
        "hierarchy": {
            "segments": proj.portfolios or [],
            "product_groups": proj.product_groups or [],
        },
    }


def _level_from_fe(fe: float) -> dict:
    """Map current-state flow efficiency → current maturity level + DevOps band."""
    if fe is None:
        return {"current_level": 0, "maturity_band": "CRAWL", "flow_efficiency": None}
    if fe < 15:   lvl, band = 0, "PRE_CRAWL"
    elif fe < 25: lvl, band = 0, "CRAWL"
    elif fe < 35: lvl, band = 1, "WALK"
    elif fe < 50: lvl, band = 1, "RUN"
    else:         lvl, band = 2, "FLY"
    return {"current_level": lvl, "maturity_band": band, "flow_efficiency": round(fe, 1)}


@router.get("/{project_id}/current-state")
async def current_state(project_id: str, db: AsyncSession = Depends(get_db)):
    """Auto-derive the current maturity level from the latest Current-State VSM analysis."""
    await _get_project(db, project_id)
    snap = (await db.execute(
        select(VSMSnapshot).where(VSMSnapshot.project_id == project_id)
        .order_by(VSMSnapshot.created_at.desc()).limit(1))).scalar_one_or_none()
    fe = None
    if snap and isinstance(snap.summary, dict):
        fe = snap.summary.get("flow_efficiency")
    res = _level_from_fe(fe)
    res["source"] = "current-state-vsm" if fe is not None else "default"
    return res


@router.post("/{project_id}/roadmap")
async def roadmap(project_id: str, body: RoadmapIn, db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    count = body.interim_count
    suggestion = suggest_interims(body.maturity_band, body.risk_appetite)
    if count is None:
        count = suggestion["interim_count"]
    rm = build_roadmap(body.current_level, body.target_level, count,
                       body.risk_appetite, body.platform)
    rm["suggestion"] = suggestion
    return rm


@router.get("/{project_id}/progress")
async def progress(project_id: str, db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    c = await _load_cfg(db, project_id)
    if not c:
        raise HTTPException(404, "No target state configured for this project")
    return compute_progress(_cfg_dict(c))
