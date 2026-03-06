from fastapi import APIRouter
from ..core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "agents": 8,
        "pdlc_phases": 7,
        "activities": 36
    }
