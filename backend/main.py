"""
PDLC VSM Platform — FastAPI Backend
Multi-agent platform for Product Development Lifecycle Value Stream Mapping.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.db import init_db
from .core.config import settings
from .routers import projects, vsm, agents, alm, analysis, health
from .routers import devops_maturity
from .routers import accuracy
from .routers import outcome_dashboard
from .routers import target_state
from .routers import settings_router
from .routers import data_sources
from .routers import documents
from .routers import manual_assessment
from .routers import step_reviews
from .routers import seed_demo
from .routers.settings_router import set_scheduler, _update_scheduler, get_setting
from .database.db import AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()

    # Start APScheduler
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        sched = AsyncIOScheduler()
        sched.start()
        set_scheduler(sched)

        # Restore schedule from DB if it was configured previously
        async with AsyncSessionLocal() as db:
            enabled     = await get_setting(db, "schedule_enabled", "false") == "true"
            frequency   = await get_setting(db, "schedule_frequency", "weekly")
            day_of_week = await get_setting(db, "schedule_day_of_week", "monday")
            hour        = int(await get_setting(db, "schedule_hour", "7"))
        if enabled:
            _update_scheduler(enabled, frequency, day_of_week, hour)
    except ImportError:
        pass  # APScheduler not installed — scheduled pipeline unavailable

    yield
    # Shutdown
    try:
        sched.shutdown(wait=False)
    except Exception:
        pass


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-agent PDLC Value Stream Mapping platform — FastAPI + LangGraph",
    lifespan=lifespan
)

import os as _os

_cors_origins = [
    "http://localhost:3000", "http://127.0.0.1:3000",
    "http://localhost:3001", "http://127.0.0.1:3001",
    "http://localhost:5175", "http://127.0.0.1:5175",
]
_extra = _os.environ.get("CORS_ALLOWED_ORIGINS", "")
if _extra:
    _cors_origins.extend(o.strip() for o in _extra.split(",") if o.strip())
_cors_origins.extend([
    "https://stump-app.azurewebsites.net",
    "https://stump-api.azurewebsites.net",
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health.router,              prefix="/api/v1")
app.include_router(projects.router,            prefix="/api/v1")
app.include_router(vsm.router,                 prefix="/api/v1")
app.include_router(agents.router,              prefix="/api/v1")
app.include_router(alm.router,                 prefix="/api/v1")
app.include_router(analysis.router,            prefix="/api/v1")
app.include_router(devops_maturity.router,     prefix="/api/v1")
app.include_router(accuracy.router,            prefix="/api/v1")
app.include_router(outcome_dashboard.router,   prefix="/api/v1")
app.include_router(target_state.router,        prefix="/api/v1")
app.include_router(settings_router.router,     prefix="/api/v1")
app.include_router(data_sources.router,        prefix="/api/v1")
app.include_router(documents.router,           prefix="/api/v1")
app.include_router(manual_assessment.router,   prefix="/api/v1")
app.include_router(step_reviews.router,        prefix="/api/v1")
app.include_router(seed_demo.router,           prefix="/api/v1")
