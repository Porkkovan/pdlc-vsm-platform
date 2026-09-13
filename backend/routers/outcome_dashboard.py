"""
Outcome Dashboard router.

Monitors the outcomes of Options A / B / C across three perspectives:
  1. AI Adoption          — agent/tool uptake
  2. PDLC Performance     — flow, speed, stability, productivity (slides 12–18)
  3. AI Ops & Assurance   — token usage, agent quality, bias, explainability

Computes metrics from connected real-time data sources (Jira / GitHub / CI-CD /
AI platform) using the documented formulas, falling back to slide-aligned demo
data, and attaches LLM (or rule-based) inference & action points per chart group.
"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

import json

from ..database.db import get_db
from ..database.models import (MetricDataSource, OutcomeMetricSnapshot, Project, TargetStateConfig)
from ..agents.outcome_metrics.catalog import (PERSPECTIVES, SOURCE_TYPES,
                                              matrix_rows, METRICS)
from ..agents.outcome_metrics.engine import build_dashboard, SCEN_LABEL
from ..agents.outcome_metrics.inferences import attach_inferences
from ..agents.outcome_metrics.productivity import compute_productivity, compute_value_trend, dora_defaults
from ..agents.outcome_metrics.rollup import rollup
from ..agents.outcome_metrics import connectors
from .settings_router import get_setting, set_setting

router = APIRouter(prefix="/outcome-dashboard", tags=["outcome-dashboard"])


# ── Schemas ───────────────────────────────────────────────────────────────────
class DataSourceIn(BaseModel):
    perspective: str
    source_type: str
    label: Optional[str] = None
    base_url: Optional[str] = None
    username: Optional[str] = None
    token: Optional[str] = None
    config: Optional[dict] = None
    enabled: Optional[bool] = True


# Editable productivity inputs (what-if). All optional → only changed fields persist.
PROD_FIELDS = ("team_size", "sprint_days", "utilisation", "blended_daily_rate",
               "sp_rate", "sp_delivered", "cfr")


class ProductivityInputs(BaseModel):
    team_size: Optional[float] = None
    sprint_days: Optional[float] = None
    utilisation: Optional[float] = None
    blended_daily_rate: Optional[float] = None
    sp_rate: Optional[float] = None
    sp_delivered: Optional[float] = None
    cfr: Optional[float] = None

    def overrides(self) -> dict:
        return {k: v for k, v in self.model_dump().items() if v is not None}


class InferenceItem(BaseModel):
    title: Optional[str] = ""
    text: Optional[str] = ""
    severity: Optional[str] = "info"


class InferencesIn(BaseModel):
    inferences: List[InferenceItem]


def _prod_key(project_id: str, scenario: str) -> str:
    return f"prod_inputs:{project_id}:{scenario}"


def _inf_key(project_id: str, scenario: str, perspective: str) -> str:
    return f"inferences:{project_id}:{scenario}:{perspective}"


# Editable J-Curve / investment assumptions (DORA-aligned).
DORA_FIELDS = ("token_per_dev_sprint", "ai_license_per_user_yr", "training_per_user_yr",
               "infra_per_user_yr", "jcurve_drop_pct", "jcurve_months", "adopt_sprints", "pods_shared")


class DoraInputs(BaseModel):
    token_per_dev_sprint: Optional[float] = None
    ai_license_per_user_yr: Optional[float] = None
    training_per_user_yr: Optional[float] = None
    infra_per_user_yr: Optional[float] = None
    jcurve_drop_pct: Optional[float] = None     # percent (e.g. 15)
    jcurve_months: Optional[float] = None
    adopt_sprints: Optional[float] = None
    pods_shared: Optional[float] = None

    def overrides(self) -> dict:
        return {k: v for k, v in self.model_dump().items() if v is not None}


def _dora_key(project_id: str, scenario: str) -> str:
    return f"jcurve:{project_id}:{scenario}"


async def _get_dora_overrides(db: AsyncSession, project_id: str, scenario: str) -> dict:
    raw = await get_setting(db, _dora_key(project_id, scenario), "")
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        return {k: data[k] for k in DORA_FIELDS if k in data and data[k] is not None}
    except Exception:
        return {}


async def _get_inferences(db: AsyncSession, project_id: str, scenario: str, perspective: str):
    """Return saved custom inferences (list) for a perspective, or None if unset."""
    raw = await get_setting(db, _inf_key(project_id, scenario, perspective), "")
    if not raw:
        return None
    try:
        data = json.loads(raw)
        sev_ok = {"good", "warn", "info"}
        return [{"title": n.get("title", ""), "text": n.get("text", ""),
                 "severity": n["severity"] if n.get("severity") in sev_ok else "info"}
                for n in data if isinstance(n, dict)]
    except Exception:
        return None


async def _get_prod_overrides(db: AsyncSession, project_id: str, scenario: str) -> dict:
    raw = await get_setting(db, _prod_key(project_id, scenario), "")
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        return {k: data[k] for k in PROD_FIELDS if k in data and data[k] is not None}
    except Exception:
        return {}


def _source_dict(s: MetricDataSource, redact: bool = True) -> dict:
    return {
        "id": s.id, "project_id": s.project_id, "perspective": s.perspective,
        "source_type": s.source_type, "label": s.label, "base_url": s.base_url,
        "username": s.username,
        "token": ("••••" if (s.token and redact) else (s.token or "")),
        "has_token": bool(s.token),
        "config": s.config or {}, "enabled": bool(s.enabled),
        "last_synced": s.last_synced.isoformat() + "Z" if s.last_synced else None,
        "last_status": s.last_status, "last_message": s.last_message,
    }


async def _get_project(db: AsyncSession, project_id: str) -> Project:
    proj = (await db.execute(select(Project).where(Project.id == project_id))).scalar_one_or_none()
    if not proj:
        raise HTTPException(404, f"Project {project_id} not found")
    return proj


async def _load_sources(db: AsyncSession, project_id: str) -> list[MetricDataSource]:
    rows = await db.execute(
        select(MetricDataSource).where(MetricDataSource.project_id == project_id))
    return list(rows.scalars().all())


# ── Catalog / reference ─────────────────────────────────────────────────────
@router.get("/catalog")
async def get_catalog():
    """Metric definitions, progression matrix, perspectives & selectable source types."""
    return {
        "perspectives": PERSPECTIVES,
        "scenarios": [{"id": k, "label": v} for k, v in SCEN_LABEL.items()],
        "metrics": [{"id": m["id"], "name": m["name"], "perspective": m["perspective"],
                     "unit": m["unit"], "better": m["better"], "source": m["source"],
                     "formula": m["formula"], "ranges": m["ranges"]} for m in METRICS],
        "progression_matrix": matrix_rows(),
        "source_types": SOURCE_TYPES,
    }


# ── Data sources CRUD ─────────────────────────────────────────────────────────
@router.get("/{project_id}/sources")
async def list_sources(project_id: str, db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    return [_source_dict(s) for s in await _load_sources(db, project_id)]


@router.post("/{project_id}/sources")
async def create_source(project_id: str, body: DataSourceIn, db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    if body.perspective not in PERSPECTIVES:
        raise HTTPException(400, f"Unknown perspective '{body.perspective}'")
    s = MetricDataSource(
        project_id=project_id, perspective=body.perspective, source_type=body.source_type,
        label=body.label or body.source_type, base_url=body.base_url,
        username=body.username, token=body.token, config=body.config or {},
        enabled=1 if body.enabled else 0, last_status="never",
    )
    db.add(s)
    await db.commit()
    await db.refresh(s)
    return _source_dict(s)


@router.put("/{project_id}/sources/{source_id}")
async def update_source(project_id: str, source_id: str, body: DataSourceIn,
                        db: AsyncSession = Depends(get_db)):
    s = (await db.execute(select(MetricDataSource).where(
        MetricDataSource.id == source_id,
        MetricDataSource.project_id == project_id))).scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Data source not found")
    s.perspective = body.perspective
    s.source_type = body.source_type
    s.label = body.label or body.source_type
    s.base_url = body.base_url
    s.username = body.username
    # keep existing token if client sends the redacted placeholder or blank
    if body.token and body.token != "••••":
        s.token = body.token
    s.config = body.config or {}
    s.enabled = 1 if body.enabled else 0
    s.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(s)
    return _source_dict(s)


@router.delete("/{project_id}/sources/{source_id}")
async def delete_source(project_id: str, source_id: str, db: AsyncSession = Depends(get_db)):
    s = (await db.execute(select(MetricDataSource).where(
        MetricDataSource.id == source_id,
        MetricDataSource.project_id == project_id))).scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Data source not found")
    await db.delete(s)
    await db.commit()
    return {"deleted": source_id}


@router.post("/{project_id}/sources/{source_id}/test")
async def test_source(project_id: str, source_id: str, db: AsyncSession = Depends(get_db)):
    s = (await db.execute(select(MetricDataSource).where(
        MetricDataSource.id == source_id,
        MetricDataSource.project_id == project_id))).scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Data source not found")
    result = await connectors.test_source(_source_dict(s, redact=False))
    s.last_status = "ok" if result["ok"] else "error"
    s.last_message = result["message"]
    s.last_synced = datetime.utcnow()
    await db.commit()
    return result


# ── Dashboard ─────────────────────────────────────────────────────────────────
async def _compute(db: AsyncSession, project_id: str, scenario: str,
                   scope: dict | None = None, level: str = "feature",
                   persist: bool = True) -> dict:
    proj = await _get_project(db, project_id)
    product_groups = getattr(proj, "product_groups", None) or []
    roll = rollup(product_groups, scope, scenario, level)
    base = roll["base_values"] if roll else None
    prod_inputs = roll["prod_inputs"] if roll else None
    scope_meta = {**(scope or {}), "level": level,
                  **(roll["meta"] if roll else {"units": 1, "teams": 0, "breakdown": []})}

    sources = [_source_dict(s, redact=False) for s in await _load_sources(db, project_id)]
    live, mode, source_results = await connectors.fetch_live_values(sources)
    prod_ov = await _get_prod_overrides(db, project_id, scenario)
    # Configured target-state platform drives the J-curve ongoing (token/agent) cost.
    tcfg = (await db.execute(select(TargetStateConfig)
            .where(TargetStateConfig.project_id == project_id)
            .order_by(TargetStateConfig.updated_at.desc()).limit(1))).scalar_one_or_none()
    platform = (tcfg.platform if tcfg and tcfg.platform else "homegrown")
    dora_ov = await _get_dora_overrides(db, project_id, scenario)
    dashboard = build_dashboard(scenario, live=live, source_mode=mode, prod_overrides=prod_ov,
                                base=base, prod_inputs=prod_inputs, scope_meta=scope_meta,
                                platform=platform, dora_overrides=dora_ov)
    dashboard = await attach_inferences(dashboard)
    # Saved/custom inferences override the generated ones per perspective.
    for pkey, persp in dashboard["perspectives"].items():
        saved = await _get_inferences(db, project_id, scenario, pkey)
        if saved is not None:
            persp["inferences"] = saved
            persp["inferences_custom"] = True
    dashboard["live_values"] = live
    dashboard["source_results"] = source_results
    dashboard["productivity_overrides"] = prod_ov
    if persist:
        db.add(OutcomeMetricSnapshot(project_id=project_id, scenario=scenario,
                                     source_mode=mode, payload=dashboard))
        await db.commit()
    return dashboard


def _scope_from(segment, product_group, product, team) -> dict:
    s = {}
    if segment: s["segment"] = segment
    if product_group: s["product_group"] = product_group
    if product: s["product"] = product
    if team: s["team"] = team
    return s


# ── Productivity inputs (editable what-if) ───────────────────────────────────
@router.get("/{project_id}/productivity-inputs")
async def get_productivity_inputs(project_id: str, scenario: str = "option-a",
                                  db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    saved = await _get_prod_overrides(db, project_id, scenario)
    defaults = compute_productivity(scenario, {})["inputs"]
    effective = compute_productivity(scenario, saved)
    return {"scenario": scenario, "defaults": defaults, "saved_overrides": saved,
            "effective_inputs": effective["inputs"], "productivity": effective,
            "field_meta": _FIELD_META}


@router.post("/{project_id}/productivity-preview")
async def preview_productivity(project_id: str, body: ProductivityInputs,
                               scenario: str = "option-a",
                               db: AsyncSession = Depends(get_db)):
    """Stateless recompute for live what-if editing — does not persist."""
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    return compute_productivity(scenario, body.overrides())


@router.put("/{project_id}/productivity-inputs")
async def save_productivity_inputs(project_id: str, body: ProductivityInputs,
                                   scenario: str = "option-a", level: str = "feature",
                                   segment: str = "", product_group: str = "",
                                   product: str = "", team: str = "",
                                   db: AsyncSession = Depends(get_db)):
    """Persist overrides and recompute the full dashboard (KPIs, charts, inferences)."""
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    await set_setting(db, _prod_key(project_id, scenario), json.dumps(body.overrides()))
    scope = _scope_from(segment, product_group, product, team)
    return await _compute(db, project_id, scenario, scope=scope, level=level)


# ── J-Curve / investment assumptions (editable) ──────────────────────────────
_DORA_FIELD_META = [
    {"key": "token_per_dev_sprint", "label": "Agent/token spend", "unit": "$/dev/sprint", "step": 5, "source": "AI platform billing"},
    {"key": "ai_license_per_user_yr", "label": "Licence (COTS)", "unit": "$/user/yr", "step": 50, "source": "Vendor subscription"},
    {"key": "training_per_user_yr", "label": "Enablement / training", "unit": "$/user (one-time)", "step": 200, "source": "L&D"},
    {"key": "infra_per_user_yr", "label": "AI infrastructure", "unit": "$/user/yr", "step": 25, "source": "Cloud/infra"},
    {"key": "jcurve_drop_pct", "label": "J-Curve productivity drop", "unit": "%", "step": 1, "source": "DORA (Fig 2)"},
    {"key": "jcurve_months", "label": "J-Curve duration", "unit": "months", "step": 1, "source": "DORA (Fig 2)"},
    {"key": "adopt_sprints", "label": "Adoption ramp", "unit": "sprints", "step": 1, "source": "rollout plan"},
    {"key": "pods_shared", "label": "Pods sharing platform", "unit": "pods", "step": 1, "source": "portfolio"},
]


@router.get("/{project_id}/jcurve-inputs")
async def get_jcurve_inputs(project_id: str, scenario: str = "option-a",
                            db: AsyncSession = Depends(get_db)):
    """Defaults + saved J-Curve/investment overrides for the editable panel."""
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    tcfg = (await db.execute(select(TargetStateConfig)
            .where(TargetStateConfig.project_id == project_id)
            .order_by(TargetStateConfig.updated_at.desc()).limit(1))).scalar_one_or_none()
    platform = (tcfg.platform if tcfg and tcfg.platform else "homegrown")
    saved = await _get_dora_overrides(db, project_id, scenario)
    defaults = dora_defaults(scenario, platform)
    return {"scenario": scenario, "platform": platform, "defaults": defaults,
            "saved_overrides": saved, "effective": {**defaults, **saved},
            "field_meta": _DORA_FIELD_META}


@router.post("/{project_id}/jcurve-preview")
async def preview_jcurve(project_id: str, body: DoraInputs, scenario: str = "option-a",
                         db: AsyncSession = Depends(get_db)):
    """Stateless recompute of the J-Curve trend for live what-if editing."""
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    tcfg = (await db.execute(select(TargetStateConfig)
            .where(TargetStateConfig.project_id == project_id)
            .order_by(TargetStateConfig.updated_at.desc()).limit(1))).scalar_one_or_none()
    platform = (tcfg.platform if tcfg and tcfg.platform else "homegrown")
    prod_ov = await _get_prod_overrides(db, project_id, scenario)
    return compute_value_trend(scenario, prod_ov, horizon_sprints=13,
                               dora=body.overrides(), platform=platform)


@router.put("/{project_id}/jcurve-inputs")
async def save_jcurve_inputs(project_id: str, body: DoraInputs, scenario: str = "option-a",
                             level: str = "feature", segment: str = "", product_group: str = "",
                             product: str = "", team: str = "", db: AsyncSession = Depends(get_db)):
    """Persist J-Curve overrides and recompute the full dashboard."""
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    await set_setting(db, _dora_key(project_id, scenario), json.dumps(body.overrides()))
    return await _compute(db, project_id, scenario,
                          scope=_scope_from(segment, product_group, product, team), level=level)


@router.delete("/{project_id}/jcurve-inputs")
async def reset_jcurve_inputs(project_id: str, scenario: str = "option-a",
                              db: AsyncSession = Depends(get_db)):
    await _get_project(db, project_id)
    await set_setting(db, _dora_key(project_id, scenario), "")
    return await _compute(db, project_id, scenario)


@router.put("/{project_id}/inferences")
async def save_inferences(project_id: str, body: InferencesIn,
                          scenario: str = "option-a", perspective: str = "adoption",
                          db: AsyncSession = Depends(get_db)):
    """Persist custom inference & action points for a perspective (overrides generated)."""
    await _get_project(db, project_id)
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    if perspective not in PERSPECTIVES:
        raise HTTPException(400, f"Unknown perspective '{perspective}'")
    items = [n.model_dump() for n in body.inferences]
    await set_setting(db, _inf_key(project_id, scenario, perspective), json.dumps(items))
    saved = await _get_inferences(db, project_id, scenario, perspective)
    return {"inferences": saved, "custom": True}


@router.delete("/{project_id}/inferences")
async def reset_inferences(project_id: str, scenario: str = "option-a",
                           perspective: str = "adoption",
                           db: AsyncSession = Depends(get_db)):
    """Clear custom inferences for a perspective (revert to auto-generated)."""
    await _get_project(db, project_id)
    await set_setting(db, _inf_key(project_id, scenario, perspective), "")
    return {"reset": True, "perspective": perspective}


@router.delete("/{project_id}/productivity-inputs")
async def reset_productivity_inputs(project_id: str, scenario: str = "option-a",
                                    db: AsyncSession = Depends(get_db)):
    """Clear overrides (back to scenario defaults) and recompute the dashboard."""
    await _get_project(db, project_id)
    await set_setting(db, _prod_key(project_id, scenario), "")
    return await _compute(db, project_id, scenario)


_FIELD_META = [
    {"key": "team_size", "label": "Team size", "unit": "engineers", "step": 1, "source": "HR / org"},
    {"key": "sprint_days", "label": "Sprint length", "unit": "working days", "step": 1, "source": "Jira/ADO"},
    {"key": "utilisation", "label": "Utilisation (focus)", "unit": "0–1", "step": 0.05, "source": "config"},
    {"key": "blended_daily_rate", "label": "Blended daily rate", "unit": "$/person-day", "step": 25, "source": "Finance/HR"},
    {"key": "sp_rate", "label": "SP rate", "unit": "days/SP", "step": 0.01, "source": "Jira time logs (6-sprint calib.)"},
    {"key": "sp_delivered", "label": "SP delivered", "unit": "story points", "step": 1, "source": "Jira/ADO sprint close"},
    {"key": "cfr", "label": "Change failure rate", "unit": "0–1", "step": 0.01, "source": "CI/CD + incidents"},
]


@router.get("/{project_id}")
async def get_dashboard(project_id: str, scenario: str = "option-a",
                        refresh: bool = False, level: str = "feature",
                        segment: str = "", product_group: str = "",
                        product: str = "", team: str = "",
                        db: AsyncSession = Depends(get_db)):
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    scope = _scope_from(segment, product_group, product, team)
    # Always compute fresh (scope/level-aware); persist a snapshot only on refresh.
    return await _compute(db, project_id, scenario, scope=scope, level=level, persist=refresh)


@router.post("/{project_id}/refresh")
async def refresh_dashboard(project_id: str, scenario: str = "option-a",
                            level: str = "feature", segment: str = "",
                            product_group: str = "", product: str = "", team: str = "",
                            db: AsyncSession = Depends(get_db)):
    if scenario not in SCEN_LABEL:
        raise HTTPException(400, f"Unknown scenario '{scenario}'")
    scope = _scope_from(segment, product_group, product, team)
    return await _compute(db, project_id, scenario, scope=scope, level=level, persist=True)
