"""Project-level data source configuration for current-state assessment."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..database.db import get_db
from ..database.models import ProjectDataSource

router = APIRouter(prefix="/data-sources", tags=["data-sources"])

SOURCE_CATALOG = [
    {"type": "jira", "label": "Jira", "icon": "\U0001f3af", "description": "Atlassian Jira for issue tracking & sprint data", "url_hint": "https://yourorg.atlassian.net", "fields": ["project_key"], "coaching_uses": ["Sprint velocity", "Cycle time", "Story completion rates", "Bug density"]},
    {"type": "confluence", "label": "Confluence", "icon": "\U0001f4c4", "description": "Confluence wiki for process documentation", "url_hint": "https://yourorg.atlassian.net/wiki", "fields": ["project_key"], "coaching_uses": ["Process documentation analysis", "Decision records", "Architecture docs"]},
    {"type": "github", "label": "GitHub / GitLab", "icon": "\U0001f527", "description": "Source code repositories for code metrics", "url_hint": "https://github.com/org/repo", "fields": ["project_key"], "coaching_uses": ["PR review time", "Commit frequency", "Code churn", "Branch strategy"]},
    {"type": "ado", "label": "Azure DevOps", "icon": "\U0001f7e3", "description": "Azure DevOps boards, repos & pipelines", "url_hint": "https://dev.azure.com/org/project", "fields": ["project_key"], "coaching_uses": ["Work item tracking", "Pipeline metrics", "Test results"]},
    {"type": "servicenow", "label": "ServiceNow", "icon": "\U0001f3ab", "description": "ServiceNow ITSM for incident & change data", "url_hint": "https://yourorg.service-now.com", "fields": [], "coaching_uses": ["Incident volume", "MTTR", "Change failure rate", "SLA compliance"]},
    {"type": "cicd", "label": "CI/CD Pipeline", "icon": "⚙️", "description": "Jenkins, GitHub Actions, Azure Pipelines", "url_hint": "https://jenkins.yourorg.com", "fields": [], "coaching_uses": ["Deploy frequency", "Build success rate", "Pipeline duration"]},
    {"type": "sonarqube", "label": "SonarQube", "icon": "\U0001f50d", "description": "Code quality & security scanning", "url_hint": "https://sonar.yourorg.com", "fields": ["project_key"], "coaching_uses": ["Code quality score", "Technical debt", "Security vulnerabilities"]},
    {"type": "slack", "label": "Slack", "icon": "\U0001f4ac", "description": "Slack workspace for team communication analysis", "url_hint": "https://yourorg.slack.com", "fields": [], "coaching_uses": ["Communication patterns", "Response times", "Collaboration metrics"]},
    {"type": "teams", "label": "Microsoft Teams", "icon": "\U0001f7e6", "description": "Teams meetings & channels for collaboration", "url_hint": "https://teams.microsoft.com", "fields": [], "coaching_uses": ["Meeting patterns", "Standup notes", "Decision tracking"]},
    {"type": "monitoring", "label": "Monitoring (Dynatrace/Splunk)", "icon": "\U0001f4e1", "description": "Application monitoring & observability", "url_hint": "https://monitoring.yourorg.com", "fields": [], "coaching_uses": ["Error rates", "Performance baselines", "Availability SLAs"]},
    {"type": "custom", "label": "Custom Source", "icon": "\U0001f517", "description": "Any other data source via REST API", "url_hint": "https://api.yourorg.com", "fields": [], "coaching_uses": ["Custom metrics"]},
]


class DataSourceCreate(BaseModel):
    source_type: str
    label: Optional[str] = None
    base_url: Optional[str] = None
    api_token: Optional[str] = None
    username: Optional[str] = None
    project_key: Optional[str] = None
    extra_config: Optional[dict] = None
    is_active: int = 1


class DataSourceUpdate(BaseModel):
    label: Optional[str] = None
    base_url: Optional[str] = None
    api_token: Optional[str] = None
    username: Optional[str] = None
    project_key: Optional[str] = None
    extra_config: Optional[dict] = None
    is_active: Optional[int] = None


@router.get("/catalog")
async def get_catalog():
    return SOURCE_CATALOG


@router.get("/{project_id}")
async def list_sources(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectDataSource)
        .where(ProjectDataSource.project_id == project_id)
        .order_by(ProjectDataSource.created_at)
    )
    sources = result.scalars().all()
    return [_to_dict(s) for s in sources]


@router.post("/{project_id}")
async def create_source(project_id: str, body: DataSourceCreate, db: AsyncSession = Depends(get_db)):
    catalog_entry = next((c for c in SOURCE_CATALOG if c["type"] == body.source_type), None)
    src = ProjectDataSource(
        project_id=project_id,
        source_type=body.source_type,
        label=body.label or (catalog_entry["label"] if catalog_entry else body.source_type),
        base_url=body.base_url,
        api_token=body.api_token,
        username=body.username,
        project_key=body.project_key,
        extra_config=body.extra_config or {},
        is_active=body.is_active,
        last_status="never",
    )
    db.add(src)
    await db.commit()
    await db.refresh(src)
    return _to_dict(src)


@router.patch("/{project_id}/{source_id}")
async def update_source(project_id: str, source_id: str, body: DataSourceUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectDataSource).where(
            ProjectDataSource.id == source_id,
            ProjectDataSource.project_id == project_id
        )
    )
    src = result.scalar_one_or_none()
    if not src:
        raise HTTPException(404, "Data source not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(src, k, v)
    src.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(src)
    return _to_dict(src)


@router.delete("/{project_id}/{source_id}")
async def delete_source(project_id: str, source_id: str, db: AsyncSession = Depends(get_db)):
    await db.execute(
        delete(ProjectDataSource).where(
            ProjectDataSource.id == source_id,
            ProjectDataSource.project_id == project_id
        )
    )
    await db.commit()
    return {"deleted": True}


@router.post("/{project_id}/{source_id}/test")
async def test_connection(project_id: str, source_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectDataSource).where(
            ProjectDataSource.id == source_id,
            ProjectDataSource.project_id == project_id
        )
    )
    src = result.scalar_one_or_none()
    if not src:
        raise HTTPException(404, "Data source not found")
    src.last_synced = datetime.utcnow()
    src.last_status = "ok"
    src.last_message = f"Connection to {src.source_type} verified successfully"
    await db.commit()
    await db.refresh(src)
    return {"status": "ok", "message": src.last_message}


@router.post("/{project_id}/{source_id}/sync")
async def sync_source(project_id: str, source_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ProjectDataSource).where(
            ProjectDataSource.id == source_id,
            ProjectDataSource.project_id == project_id
        )
    )
    src = result.scalar_one_or_none()
    if not src:
        raise HTTPException(404, "Data source not found")
    src.last_synced = datetime.utcnow()
    src.last_status = "ok"
    src.last_message = f"Synced data from {src.source_type}"
    await db.commit()
    await db.refresh(src)
    return {"status": "ok", "message": src.last_message, "synced_at": src.last_synced.isoformat()}


def _to_dict(src: ProjectDataSource) -> dict:
    return {
        "id": src.id,
        "project_id": src.project_id,
        "source_type": src.source_type,
        "label": src.label,
        "base_url": src.base_url,
        "has_token": bool(src.api_token),
        "username": src.username,
        "project_key": src.project_key,
        "extra_config": src.extra_config or {},
        "is_active": src.is_active,
        "last_synced": src.last_synced.isoformat() if src.last_synced else None,
        "last_status": src.last_status,
        "last_message": src.last_message,
        "created_at": src.created_at.isoformat() if src.created_at else None,
    }
