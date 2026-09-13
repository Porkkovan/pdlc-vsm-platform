"""
Settings Router
Manages platform configuration: LLM credentials, ALM credentials, pipeline schedule.
Credentials are stored encrypted in the database (not .env) so they can be set via UI.
"""
import json
import httpx
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from ..database.db import get_db, AsyncSessionLocal
from ..database.models import PlatformSettings, ScheduledPipelineRun
from ..core.config import settings as env_settings

router = APIRouter(prefix="/settings", tags=["settings"])


# ── Helpers ───────────────────────────────────────────────────────────────────

async def get_setting(db: AsyncSession, key: str, default: str = "") -> str:
    result = await db.execute(select(PlatformSettings).where(PlatformSettings.key == key))
    row = result.scalar_one_or_none()
    return row.value if row else default


async def set_setting(db: AsyncSession, key: str, value: str):
    result = await db.execute(select(PlatformSettings).where(PlatformSettings.key == key))
    row = result.scalar_one_or_none()
    if row:
        row.value = value
        row.updated_at = datetime.utcnow()
    else:
        db.add(PlatformSettings(key=key, value=value))
    await db.commit()


async def get_effective_llm_config(db: AsyncSession) -> dict:
    """Returns active LLM config: DB values take precedence over .env"""
    return {
        "provider":    await get_setting(db, "llm_provider", "azure" if env_settings.use_azure else "openai"),
        "azure_key":   await get_setting(db, "azure_openai_api_key",  env_settings.azure_openai_api_key),
        "azure_endpoint": await get_setting(db, "azure_openai_endpoint", env_settings.azure_openai_endpoint),
        "azure_deployment": await get_setting(db, "azure_openai_deployment", env_settings.azure_openai_deployment),
        "azure_api_version": await get_setting(db, "azure_openai_api_version", env_settings.azure_openai_api_version),
        "openai_key":  await get_setting(db, "openai_api_key", env_settings.openai_api_key),
        "openai_model": await get_setting(db, "openai_model", env_settings.openai_model),
    }


async def get_effective_alm_config(db: AsyncSession) -> dict:
    return {
        "jira_url":       await get_setting(db, "jira_url",       env_settings.jira_url),
        "jira_username":  await get_setting(db, "jira_username",  env_settings.jira_username),
        "jira_api_token": await get_setting(db, "jira_api_token", env_settings.jira_api_token),
        "ado_org_url":    await get_setting(db, "ado_org_url",    env_settings.ado_org_url),
        "ado_pat":        await get_setting(db, "ado_pat",        env_settings.ado_personal_access_token),
        "github_token":   await get_setting(db, "github_token",   ""),
        "confluence_url": await get_setting(db, "confluence_url", ""),
        "confluence_username": await get_setting(db, "confluence_username", ""),
        "confluence_token":    await get_setting(db, "confluence_token", ""),
    }


# ── Models ────────────────────────────────────────────────────────────────────

class LLMConfig(BaseModel):
    provider: str = "azure"            # azure | openai | anthropic
    azure_key: Optional[str] = None
    azure_endpoint: Optional[str] = None
    azure_deployment: Optional[str] = None
    azure_api_version: Optional[str] = None
    openai_key: Optional[str] = None
    openai_model: Optional[str] = None


class ALMConfig(BaseModel):
    jira_url: Optional[str] = None
    jira_username: Optional[str] = None
    jira_api_token: Optional[str] = None
    ado_org_url: Optional[str] = None
    ado_pat: Optional[str] = None
    github_token: Optional[str] = None
    confluence_url: Optional[str] = None
    confluence_username: Optional[str] = None
    confluence_token: Optional[str] = None


class ScheduleConfig(BaseModel):
    enabled: bool = False
    frequency: str = "weekly"      # daily | weekly | manual
    day_of_week: str = "monday"    # for weekly
    hour: int = 7                  # UTC hour to run


# ── Status endpoint ───────────────────────────────────────────────────────────

@router.get("/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    """Returns live connection status for all integrations."""
    llm   = await get_effective_llm_config(db)
    alm   = await get_effective_alm_config(db)
    sched = {
        "enabled":     await get_setting(db, "schedule_enabled", "false"),
        "frequency":   await get_setting(db, "schedule_frequency", "weekly"),
        "day_of_week": await get_setting(db, "schedule_day_of_week", "monday"),
        "hour":        await get_setting(db, "schedule_hour", "7"),
        "last_run_at": await get_setting(db, "schedule_last_run_at", ""),
        "last_run_status": await get_setting(db, "schedule_last_run_status", ""),
        "next_run_label": _next_run_label(
            await get_setting(db, "schedule_enabled", "false") == "true",
            await get_setting(db, "schedule_frequency", "weekly"),
            await get_setting(db, "schedule_day_of_week", "monday"),
            int(await get_setting(db, "schedule_hour", "7")),
        ),
    }

    # LLM connectivity: check whether keys are configured (don't call API on status check)
    llm_configured = bool(
        (llm["provider"] == "azure" and llm["azure_key"] and llm["azure_endpoint"]) or
        (llm["provider"] == "openai" and llm["openai_key"]) or
        (llm["provider"] == "anthropic" and await get_setting(db, "anthropic_api_key", ""))
    )

    # ALM: check which tools have credentials
    alm_status = {}
    if alm["jira_url"] and alm["jira_api_token"]:
        alm_status["jira"] = {"configured": True, "url": alm["jira_url"]}
    if alm["ado_org_url"] and alm["ado_pat"]:
        alm_status["ado"] = {"configured": True, "url": alm["ado_org_url"]}
    if alm["github_token"]:
        alm_status["github"] = {"configured": True}
    if alm["confluence_url"] and alm["confluence_token"]:
        alm_status["confluence"] = {"configured": True, "url": alm["confluence_url"]}

    return {
        "llm": {
            "configured": llm_configured,
            "provider":   llm["provider"],
            "deployment": llm.get("azure_deployment") or llm.get("openai_model") or "",
            "endpoint":   llm.get("azure_endpoint", "").replace(llm.get("azure_key", "____"), "***") if llm.get("azure_endpoint") else "",
        },
        "alm": alm_status,
        "schedule": sched,
    }


def _next_run_label(enabled: bool, frequency: str, day_of_week: str, hour: int) -> str:
    if not enabled:
        return "Not scheduled"
    if frequency == "daily":
        return f"Daily at {hour:02d}:00 UTC"
    if frequency == "weekly":
        return f"Weekly on {day_of_week.capitalize()} at {hour:02d}:00 UTC"
    return "Manual only"


# ── LLM Configuration ─────────────────────────────────────────────────────────

@router.get("/llm")
async def get_llm_config(db: AsyncSession = Depends(get_db)):
    llm = await get_effective_llm_config(db)
    # Mask keys in response
    def mask(v): return (v[:8] + "..." + v[-4:]) if v and len(v) > 12 else ("***" if v else "")
    return {
        "provider":          llm["provider"],
        "azure_key_set":     bool(llm["azure_key"]),
        "azure_key_masked":  mask(llm["azure_key"]),
        "azure_endpoint":    llm["azure_endpoint"],
        "azure_deployment":  llm["azure_deployment"],
        "azure_api_version": llm["azure_api_version"],
        "openai_key_set":    bool(llm["openai_key"]),
        "openai_key_masked": mask(llm["openai_key"]),
        "openai_model":      llm["openai_model"],
    }


@router.post("/llm")
async def save_llm_config(config: LLMConfig, db: AsyncSession = Depends(get_db)):
    await set_setting(db, "llm_provider", config.provider)
    if config.azure_key:       await set_setting(db, "azure_openai_api_key", config.azure_key)
    if config.azure_endpoint:  await set_setting(db, "azure_openai_endpoint", config.azure_endpoint)
    if config.azure_deployment: await set_setting(db, "azure_openai_deployment", config.azure_deployment)
    if config.azure_api_version: await set_setting(db, "azure_openai_api_version", config.azure_api_version)
    if config.openai_key:      await set_setting(db, "openai_api_key", config.openai_key)
    if config.openai_model:    await set_setting(db, "openai_model", config.openai_model)
    return {"saved": True}


@router.post("/llm/test")
async def test_llm(db: AsyncSession = Depends(get_db)):
    """Send a minimal prompt to verify the LLM connection works."""
    llm = await get_effective_llm_config(db)
    try:
        if llm["provider"] == "azure" and llm["azure_key"] and llm["azure_endpoint"]:
            url = f"{llm['azure_endpoint'].rstrip('/')}/openai/deployments/{llm['azure_deployment']}/chat/completions?api-version={llm['azure_api_version']}"
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(url,
                    headers={"api-key": llm["azure_key"], "Content-Type": "application/json"},
                    json={"messages": [{"role": "user", "content": "Reply with the word OK only."}], "max_tokens": 5}
                )
            if resp.status_code == 200:
                reply = resp.json()["choices"][0]["message"]["content"].strip()
                return {"ok": True, "provider": "Azure OpenAI", "deployment": llm["azure_deployment"], "reply": reply}
            return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}

        elif llm["provider"] == "openai" and llm["openai_key"]:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post("https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {llm['openai_key']}", "Content-Type": "application/json"},
                    json={"model": llm["openai_model"] or "gpt-4o-mini", "messages": [{"role": "user", "content": "Reply with the word OK only."}], "max_tokens": 5}
                )
            if resp.status_code == 200:
                reply = resp.json()["choices"][0]["message"]["content"].strip()
                return {"ok": True, "provider": "OpenAI", "model": llm["openai_model"], "reply": reply}
            return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}

        return {"ok": False, "error": "No LLM credentials configured. Add Azure OpenAI or OpenAI API key above."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── ALM Credentials ───────────────────────────────────────────────────────────

@router.get("/alm")
async def get_alm_config(db: AsyncSession = Depends(get_db)):
    alm = await get_effective_alm_config(db)
    def mask(v): return (v[:4] + "..." + v[-4:]) if v and len(v) > 8 else ("***" if v else "")
    return {
        "jira_url":              alm["jira_url"],
        "jira_username":         alm["jira_username"],
        "jira_token_set":        bool(alm["jira_api_token"]),
        "jira_token_masked":     mask(alm["jira_api_token"]),
        "ado_org_url":           alm["ado_org_url"],
        "ado_pat_set":           bool(alm["ado_pat"]),
        "ado_pat_masked":        mask(alm["ado_pat"]),
        "github_token_set":      bool(alm["github_token"]),
        "github_token_masked":   mask(alm["github_token"]),
        "confluence_url":        alm["confluence_url"],
        "confluence_username":   alm["confluence_username"],
        "confluence_token_set":  bool(alm["confluence_token"]),
        "confluence_token_masked": mask(alm["confluence_token"]),
    }


@router.post("/alm")
async def save_alm_config(config: ALMConfig, db: AsyncSession = Depends(get_db)):
    if config.jira_url is not None:       await set_setting(db, "jira_url", config.jira_url)
    if config.jira_username is not None:  await set_setting(db, "jira_username", config.jira_username)
    if config.jira_api_token is not None: await set_setting(db, "jira_api_token", config.jira_api_token)
    if config.ado_org_url is not None:    await set_setting(db, "ado_org_url", config.ado_org_url)
    if config.ado_pat is not None:        await set_setting(db, "ado_pat", config.ado_pat)
    if config.github_token is not None:   await set_setting(db, "github_token", config.github_token)
    if config.confluence_url is not None: await set_setting(db, "confluence_url", config.confluence_url)
    if config.confluence_username is not None: await set_setting(db, "confluence_username", config.confluence_username)
    if config.confluence_token is not None: await set_setting(db, "confluence_token", config.confluence_token)
    return {"saved": True}


@router.post("/alm/test")
async def test_alm(tool: str, db: AsyncSession = Depends(get_db)):
    """Test connectivity for a specific ALM tool."""
    alm = await get_effective_alm_config(db)
    try:
        if tool == "jira":
            if not alm["jira_url"] or not alm["jira_api_token"]:
                return {"ok": False, "error": "Jira URL and API token are required"}
            import base64
            creds = base64.b64encode(f"{alm['jira_username']}:{alm['jira_api_token']}".encode()).decode()
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{alm['jira_url'].rstrip('/')}/rest/api/2/myself",
                    headers={"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
                )
            if resp.status_code == 200:
                data = resp.json()
                return {"ok": True, "tool": "Jira", "user": data.get("displayName", ""), "email": data.get("emailAddress", "")}
            return {"ok": False, "error": f"Jira returned HTTP {resp.status_code}. Check URL and credentials."}

        elif tool == "ado":
            if not alm["ado_org_url"] or not alm["ado_pat"]:
                return {"ok": False, "error": "ADO org URL and PAT are required"}
            import base64
            creds = base64.b64encode(f":{alm['ado_pat']}".encode()).decode()
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{alm['ado_org_url'].rstrip('/')}/_apis/projects?api-version=7.0",
                    headers={"Authorization": f"Basic {creds}"}
                )
            if resp.status_code == 200:
                count = resp.json().get("count", 0)
                return {"ok": True, "tool": "Azure DevOps", "projects_found": count}
            return {"ok": False, "error": f"ADO returned HTTP {resp.status_code}. Check org URL and PAT."}

        elif tool == "github":
            if not alm["github_token"]:
                return {"ok": False, "error": "GitHub token is required"}
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://api.github.com/user",
                    headers={"Authorization": f"token {alm['github_token']}", "Accept": "application/vnd.github.v3+json"})
            if resp.status_code == 200:
                data = resp.json()
                return {"ok": True, "tool": "GitHub", "user": data.get("login", ""), "name": data.get("name", "")}
            return {"ok": False, "error": f"GitHub returned HTTP {resp.status_code}. Check token."}

        elif tool == "confluence":
            if not alm["confluence_url"] or not alm["confluence_token"]:
                return {"ok": False, "error": "Confluence URL and API token are required"}
            import base64
            creds = base64.b64encode(f"{alm['confluence_username']}:{alm['confluence_token']}".encode()).decode()
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{alm['confluence_url'].rstrip('/')}/rest/api/space?limit=1",
                    headers={"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
                )
            if resp.status_code == 200:
                return {"ok": True, "tool": "Confluence", "message": "Connected successfully"}
            return {"ok": False, "error": f"Confluence returned HTTP {resp.status_code}. Check URL and credentials."}

        return {"ok": False, "error": f"Unknown tool: {tool}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Pipeline Schedule ─────────────────────────────────────────────────────────

@router.get("/schedule")
async def get_schedule(db: AsyncSession = Depends(get_db)):
    # Last 5 pipeline runs
    result = await db.execute(
        select(ScheduledPipelineRun)
        .order_by(ScheduledPipelineRun.created_at.desc())
        .limit(5)
    )
    runs = result.scalars().all()
    return {
        "enabled":       await get_setting(db, "schedule_enabled", "false") == "true",
        "frequency":     await get_setting(db, "schedule_frequency", "weekly"),
        "day_of_week":   await get_setting(db, "schedule_day_of_week", "monday"),
        "hour":          int(await get_setting(db, "schedule_hour", "7")),
        "project_id":    await get_setting(db, "schedule_project_id", ""),
        "last_run_at":   await get_setting(db, "schedule_last_run_at", ""),
        "last_run_status": await get_setting(db, "schedule_last_run_status", ""),
        "recent_runs": [
            {
                "id": r.id,
                "trigger": r.trigger,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "error": r.error,
            }
            for r in runs
        ]
    }


@router.post("/schedule")
async def save_schedule(config: ScheduleConfig, project_id: str = "", db: AsyncSession = Depends(get_db)):
    await set_setting(db, "schedule_enabled", "true" if config.enabled else "false")
    await set_setting(db, "schedule_frequency", config.frequency)
    await set_setting(db, "schedule_day_of_week", config.day_of_week)
    await set_setting(db, "schedule_hour", str(config.hour))
    if project_id:
        await set_setting(db, "schedule_project_id", project_id)
    # Update the live scheduler
    _update_scheduler(config.enabled, config.frequency, config.day_of_week, config.hour)
    return {"saved": True, "next_run": _next_run_label(config.enabled, config.frequency, config.day_of_week, config.hour)}


@router.post("/pipeline/trigger")
async def trigger_pipeline(project_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Manually trigger a full pipeline run for a project."""
    run = ScheduledPipelineRun(project_id=project_id, trigger="manual", status="running")
    db.add(run)
    await db.commit()
    await db.refresh(run)
    run_id = run.id
    background_tasks.add_task(_execute_pipeline, project_id, run_id, "manual")
    await set_setting(db, "schedule_last_run_at", datetime.utcnow().isoformat())
    await set_setting(db, "schedule_last_run_status", "running")
    return {"triggered": True, "run_id": run_id, "project_id": project_id}


async def _execute_pipeline(project_id: str, run_id: str, trigger: str = "scheduled"):
    """Background: run full analysis pipeline and update the run record."""
    from ..agents.orchestrator.graph import run_full_analysis
    async with AsyncSessionLocal() as db:
        try:
            state = {
                "project_id": project_id,
                "project": {},
                "alm_raw_data": {},
                "vsm_data": {},
                "overrides": {},
                "errors": [],
                "run_id": run_id,
                "status": "running"
            }
            result = await run_full_analysis(state)
            result_run_id = result.get("run_id", run_id)

            run_result = await db.execute(select(ScheduledPipelineRun).where(ScheduledPipelineRun.id == run_id))
            run = run_result.scalar_one_or_none()
            if run:
                run.status = "complete"
                run.result_run_id = result_run_id
                run.completed_at = datetime.utcnow()
            await set_setting(db, "schedule_last_run_at", datetime.utcnow().isoformat())
            await set_setting(db, "schedule_last_run_status", "complete")
            await db.commit()
        except Exception as e:
            run_result = await db.execute(select(ScheduledPipelineRun).where(ScheduledPipelineRun.id == run_id))
            run = run_result.scalar_one_or_none()
            if run:
                run.status = "failed"
                run.error = str(e)
                run.completed_at = datetime.utcnow()
            await set_setting(db, "schedule_last_run_status", "failed")
            await db.commit()


# ── APScheduler integration ───────────────────────────────────────────────────
# Scheduler instance is created in main.py and passed here via module-level ref

_scheduler = None

def set_scheduler(sched):
    global _scheduler
    _scheduler = sched

def _update_scheduler(enabled: bool, frequency: str, day_of_week: str, hour: int):
    """Re-configure the running APScheduler job."""
    if _scheduler is None:
        return
    job_id = "auto_pipeline"
    try:
        _scheduler.remove_job(job_id)
    except Exception:
        pass
    if not enabled:
        return
    import asyncio
    from apscheduler.triggers.cron import CronTrigger

    async def _run_scheduled():
        from ..database.db import AsyncSessionLocal as _ASL
        async with _ASL() as db:
            project_id = await get_setting(db, "schedule_project_id", "")
        if not project_id:
            return
        run = ScheduledPipelineRun(project_id=project_id, trigger="scheduled", status="running")
        async with AsyncSessionLocal() as db:
            db.add(run)
            await db.commit()
            await db.refresh(run)
        await _execute_pipeline(project_id, run.id, "scheduled")

    if frequency == "daily":
        trigger = CronTrigger(hour=hour, minute=0)
    else:  # weekly
        day_map = {"monday": "mon", "tuesday": "tue", "wednesday": "wed",
                   "thursday": "thu", "friday": "fri", "saturday": "sat", "sunday": "sun"}
        trigger = CronTrigger(day_of_week=day_map.get(day_of_week, "mon"), hour=hour, minute=0)

    _scheduler.add_job(lambda: asyncio.create_task(_run_scheduled()), trigger=trigger, id=job_id, replace_existing=True)
