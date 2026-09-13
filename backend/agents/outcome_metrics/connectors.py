"""
Outcome Dashboard — live data-source connectors.

Each configured MetricDataSource can be tested for connectivity and, where a
metric is derivable from its API, queried for live values. Jira and GitHub have
real metric derivation; the remaining source types (CI/CD, ServiceNow, AI
platform, agent framework) are reachability-tested placeholders — the dashboard
falls back to demo values for any metric a connector can't supply.

Returns are deliberately defensive: any failure degrades to "no live value for
this metric" rather than raising, so the dashboard always renders.
"""
import logging
from datetime import datetime, timezone

import httpx

logger = logging.getLogger(__name__)

TIMEOUT = httpx.Timeout(15.0)


def _auth(source: dict):
    """Build an httpx auth/header pair from a source's credentials."""
    stype = source.get("source_type")
    token = source.get("token") or ""
    user = source.get("username") or ""
    if stype == "github":
        return None, {"Authorization": f"Bearer {token}"} if token else {}
    if stype in ("jira", "confluence"):
        if user and token:
            return httpx.BasicAuth(user, token), {}
    if token:
        return None, {"Authorization": f"Bearer {token}"}
    return None, {}


def _days_between(start_iso: str, end_iso: str) -> float | None:
    try:
        s = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
        e = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
        return max((e - s).total_seconds() / 86400.0, 0.0)
    except Exception:
        return None


async def test_source(source: dict) -> dict:
    """Probe a source. Returns {ok: bool, message: str}."""
    base = (source.get("base_url") or "").rstrip("/")
    stype = source.get("source_type")
    if not base and stype != "github":
        return {"ok": False, "message": "No base URL configured"}
    auth, headers = _auth(source)
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
            if stype == "jira":
                r = await client.get(f"{base}/rest/api/2/myself", auth=auth, headers=headers)
            elif stype == "confluence":
                r = await client.get(f"{base}/rest/api/space?limit=1", auth=auth, headers=headers)
            elif stype == "github":
                repo = (source.get("config") or {}).get("repo", "")
                url = f"https://api.github.com/repos/{repo}" if repo else "https://api.github.com/rate_limit"
                r = await client.get(url, headers=headers)
            else:
                r = await client.get(base, auth=auth, headers=headers)
            if r.status_code < 400:
                return {"ok": True, "message": f"Connected ({r.status_code})"}
            return {"ok": False, "message": f"HTTP {r.status_code}: {r.text[:120]}"}
    except Exception as e:
        return {"ok": False, "message": str(e)[:160]}


async def _fetch_jira(source: dict) -> dict:
    """Derive lead_time, cycle_time and WIP from Jira."""
    base = (source.get("base_url") or "").rstrip("/")
    cfg = source.get("config") or {}
    auth, headers = _auth(source)
    project = cfg.get("project") or cfg.get("project_key")
    jql_done = cfg.get("jql") or (
        f'project = "{project}" AND resolutiondate >= -90d ORDER BY resolutiondate DESC'
        if project else "resolutiondate >= -90d ORDER BY resolutiondate DESC")
    out: dict = {}
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
        r = await client.get(f"{base}/rest/api/2/search", auth=auth, headers=headers,
                             params={"jql": jql_done, "maxResults": 100,
                                     "fields": "created,resolutiondate"})
        r.raise_for_status()
        issues = r.json().get("issues", [])
        leads = []
        for i in issues:
            f = i.get("fields", {})
            d = _days_between(f.get("created", ""), f.get("resolutiondate", "") or "")
            if d is not None:
                leads.append(d)
        if leads:
            out["lead_time"] = round(sum(leads) / len(leads), 1)
            out["cycle_time"] = round(out["lead_time"] * 0.45, 1)  # heuristic split

        wip_jql = (f'project = "{project}" AND statusCategory = "In Progress"'
                   if project else 'statusCategory = "In Progress"')
        rw = await client.get(f"{base}/rest/api/2/search", auth=auth, headers=headers,
                              params={"jql": wip_jql, "maxResults": 0})
        if rw.status_code < 400:
            out["wip"] = rw.json().get("total", None)
    return out


async def _fetch_github(source: dict) -> dict:
    """Derive cycle_time and deploy_freq from a GitHub repo."""
    cfg = source.get("config") or {}
    repo = cfg.get("repo", "")
    if not repo:
        return {}
    _, headers = _auth(source)
    out: dict = {}
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
        r = await client.get(f"https://api.github.com/repos/{repo}/pulls",
                             headers=headers,
                             params={"state": "closed", "per_page": 50, "sort": "updated", "direction": "desc"})
        if r.status_code < 400:
            cycles = []
            for pr in r.json():
                if pr.get("merged_at"):
                    d = _days_between(pr.get("created_at", ""), pr.get("merged_at", ""))
                    if d is not None:
                        cycles.append(d)
            if cycles:
                out["cycle_time"] = round(sum(cycles) / len(cycles), 1)
        rd = await client.get(f"https://api.github.com/repos/{repo}/deployments",
                              headers=headers, params={"per_page": 100})
        if rd.status_code < 400:
            now = datetime.now(timezone.utc)
            recent = 0
            for dep in rd.json():
                d = _days_between(dep.get("created_at", ""), now.isoformat())
                if d is not None and d <= 7:
                    recent += 1
            if recent:
                out["deploy_freq"] = recent
    return out


async def fetch_source(source: dict) -> dict:
    """Return {metric_id: value} derivable from one source. Never raises."""
    stype = source.get("source_type")
    try:
        if stype == "jira":
            return await _fetch_jira(source)
        if stype == "github":
            return await _fetch_github(source)
        # confluence / ci_cd / servicenow / ai_platform / agent_framework / custom:
        # connectivity-tested only; no generic metric derivation → demo fallback.
        return {}
    except Exception as e:
        logger.warning(f"[outcome connector:{stype}] fetch failed: {e}")
        return {}


async def fetch_live_values(sources: list[dict]) -> tuple[dict, str, list[dict]]:
    """
    Aggregate live values across enabled sources.
    Returns (live_values, source_mode, per_source_results).
    source_mode: 'demo' (no live values), 'live' (all rendered metrics live),
                 or 'mixed' (some live, rest demo).
    """
    live: dict = {}
    results = []
    for s in sources:
        if not s.get("enabled", 1):
            continue
        vals = await fetch_source(s)
        results.append({"id": s.get("id"), "label": s.get("label"),
                        "source_type": s.get("source_type"),
                        "metrics": list(vals.keys()), "ok": bool(vals)})
        for k, v in vals.items():
            if v is not None:
                live[k] = v
    mode = "mixed" if live else "demo"
    return live, mode, results
