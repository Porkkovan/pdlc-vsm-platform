from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, dict as Dict

from ..agents.alm_connector.agent import run_alm_connector, _generate_sample_data, _map_to_vsm

router = APIRouter(prefix="/alm", tags=["alm"])


class ALMConfig(BaseModel):
    tool: str                         # jira, ado, github, csv, sample
    url: Optional[str] = None
    username: Optional[str] = None
    token: Optional[str] = None
    project: Optional[str] = None
    board: Optional[str] = None
    filters: Optional[dict] = None


@router.get("/supported-tools")
async def get_supported_tools():
    return [
        {"id": "jira",       "name": "Jira",             "description": "Atlassian Jira Cloud/Server"},
        {"id": "ado",        "name": "Azure DevOps",     "description": "Microsoft Azure DevOps"},
        {"id": "github",     "name": "GitHub Issues",    "description": "GitHub Issues/Projects"},
        {"id": "linear",     "name": "Linear",           "description": "Linear issue tracker"},
        {"id": "servicenow", "name": "ServiceNow",       "description": "ServiceNow ITSM"},
        {"id": "csv",        "name": "CSV / Manual",     "description": "Upload CSV or enter manually"}
    ]


@router.post("/test-connection")
async def test_connection(config: ALMConfig):
    """Test ALM tool connectivity."""
    if config.tool in ("sample", "csv"):
        return {"connected": True, "message": "No connection required for this mode"}

    state = {"project_id": "test", "project": {}, "alm_raw_data": config.model_dump(), "errors": []}
    result = await run_alm_connector(state)

    if result.get("errors"):
        return {"connected": False, "message": result["errors"][-1]}
    return {"connected": True, "message": f"Connected to {config.tool.upper()} successfully"}


@router.post("/fetch-data")
async def fetch_data(config: ALMConfig):
    """Fetch data from ALM tool and map to VSM format."""
    state = {
        "project_id":   "fetch",
        "project":      {},
        "alm_raw_data": config.model_dump(),
        "errors":       []
    }
    result = await run_alm_connector(state)
    return {
        "vsm_data":    result.get("vsm_data", {}),
        "alm_raw":     result.get("alm_raw_data", {}),
        "summary":     result.get("vsm_data", {}).get("summary", {}),
        "errors":      result.get("errors", [])
    }


@router.post("/map-to-vsm")
async def map_to_vsm(data: dict):
    """Map raw data to VSM structure."""
    vsm = _map_to_vsm(data, {})
    return vsm
