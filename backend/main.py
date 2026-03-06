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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown — nothing to clean up


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Multi-agent PDLC Value Stream Mapping platform — FastAPI + LangGraph",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health.router,    prefix="/api/v1")
app.include_router(projects.router,  prefix="/api/v1")
app.include_router(vsm.router,       prefix="/api/v1")
app.include_router(agents.router,    prefix="/api/v1")
app.include_router(alm.router,       prefix="/api/v1")
app.include_router(analysis.router,  prefix="/api/v1")
