"""
ALM Connector Agent
Connects to Jira / Azure DevOps, fetches issue data, and computes lean VSM metrics.
Falls back to sample data when no ALM credentials are available.
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import PDLC_PHASES

logger = logging.getLogger(__name__)


async def run_alm_connector(state: VSMAgentState) -> VSMAgentState:
    """
    Fetch raw work item data from ALM tool and compute per-activity metrics.
    Updates state with: alm_raw_data, vsm_data
    """
    logger.info(f"[ALM Connector] Starting for project {state.get('project_id')}")
    project = state.get("project", {})
    alm_config = state.get("alm_raw_data", {})

    tool = alm_config.get("tool", "sample")

    try:
        if tool == "jira":
            raw_data = await _fetch_jira(alm_config)
        elif tool == "ado":
            raw_data = await _fetch_ado(alm_config)
        else:
            raw_data = _generate_sample_data(project)

        vsm_data = _map_to_vsm(raw_data, alm_config.get("overrides", {}))
        return {**state, "alm_raw_data": raw_data, "vsm_data": vsm_data}

    except Exception as e:
        logger.warning(f"[ALM Connector] Error: {e} — using sample data")
        raw_data = _generate_sample_data(project)
        vsm_data = _map_to_vsm(raw_data, {})
        return {**state, "alm_raw_data": raw_data, "vsm_data": vsm_data,
                "errors": state.get("errors", []) + [f"ALM Connector: {str(e)}"]}


async def _fetch_jira(config: dict) -> dict:
    """Fetch Jira issues and compute cycle time / lead time per activity."""
    try:
        from jira import JIRA
        jira = JIRA(server=config["url"], basic_auth=(config["username"], config["token"]))
        issues = jira.search_issues(
            f'project = "{config.get("project", "")}" ORDER BY created DESC',
            maxResults=500,
            fields="summary,status,assignee,created,resolutiondate,customfield_10016,customfield_10014"
        )
        return {"source": "jira", "issue_count": len(issues), "issues": [
            {"key": i.key, "summary": i.fields.summary, "status": str(i.fields.status),
             "created": str(i.fields.created), "resolved": str(getattr(i.fields, "resolutiondate", "") or "")}
            for i in issues
        ]}
    except Exception as e:
        raise RuntimeError(f"Jira connection failed: {e}")


async def _fetch_ado(config: dict) -> dict:
    """Fetch Azure DevOps work items."""
    import httpx
    import base64
    token = base64.b64encode(f":{config['token']}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}
    org_url = config.get("url", "").rstrip("/")
    project = config.get("project", "")

    wiql = {"query": "SELECT [System.Id], [System.Title], [System.State], [System.CreatedDate], [Microsoft.VSTS.Common.ClosedDate] FROM WorkItems WHERE [System.TeamProject] = @project ORDER BY [System.CreatedDate] DESC"}

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{org_url}/{project}/_apis/wit/wiql?api-version=7.0", json=wiql, headers=headers)
        r.raise_for_status()
        ids = [item["id"] for item in r.json().get("workItems", [])[:200]]

    return {"source": "ado", "issue_count": len(ids), "work_item_ids": ids}


def _generate_sample_data(project: dict) -> dict:
    """
    Generate realistic sample data based on industry averages.
    Used when no ALM tool is connected (demo mode).
    """
    import random
    random.seed(42)  # Deterministic

    phases = []
    for phase in PDLC_PHASES:
        activities = []
        for act in phase["activities"]:
            # Add realistic variance to defaults
            effort_mid = (act["effort"]["min"] + act["effort"]["max"]) / 2
            wait_mid   = (act["wait"]["min"]   + act["wait"]["max"])   / 2
            activities.append({
                "activity_id":   act["id"],
                "activity_name": act["name"],
                "process_time":  round(effort_mid * random.uniform(0.8, 1.3), 1),
                "wait_time":     round(wait_mid   * random.uniform(0.7, 1.5), 1),
                "sample_count":  random.randint(15, 80)
            })
        phases.append({"phase_id": phase["id"], "phase_name": phase["name"], "activities": activities})

    return {"source": "sample", "phases": phases}


def _map_to_vsm(raw_data: dict, overrides: dict) -> dict:
    """Convert raw ALM data to VSM format with lean metrics."""
    phases = []
    total_pt = 0
    total_wt = 0

    for phase_data in raw_data.get("phases", []):
        phase_pt = sum(a.get("process_time", 0) for a in phase_data.get("activities", []))
        phase_wt = sum(a.get("wait_time", 0)    for a in phase_data.get("activities", []))
        lead_time_days = (phase_pt + phase_wt) / 8  # assume 8h workday

        # Apply user overrides
        phase_override = overrides.get(str(phase_data["phase_id"]), {})

        phases.append({
            "phase_id":    phase_data["phase_id"],
            "phase_name":  phase_data["phase_name"],
            "process_time": phase_override.get("process_time", round(phase_pt, 1)),
            "wait_time":    phase_override.get("wait_time",    round(phase_wt, 1)),
            "lead_time":    round(lead_time_days, 2),
            "activities":   phase_data.get("activities", [])
        })
        total_pt += phase_pt
        total_wt += phase_wt

    total_lt = (total_pt + total_wt) / 8
    flow_efficiency = round((total_pt / (total_pt + total_wt)) * 100, 1) if (total_pt + total_wt) > 0 else 0

    return {
        "source": raw_data.get("source", "unknown"),
        "phases": phases,
        "summary": {
            "total_process_time": round(total_pt, 1),
            "total_wait_time":    round(total_wt, 1),
            "total_lead_time":    round(total_lt, 2),
            "flow_efficiency":    flow_efficiency,
            "avg_cycle_time":     round(total_lt / 7, 2)
        }
    }
