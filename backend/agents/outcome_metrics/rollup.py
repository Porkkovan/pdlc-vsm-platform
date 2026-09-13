"""
Outcome Dashboard — scope roll-up & granularity engine.

Metrics are generated per leaf **team** (deterministic, seeded by team name +
scenario), then rolled up to the selected scope:

    segment ▸ product group ▸ product ▸ team

Selecting a product group with no product/team picked aggregates every product
and team beneath it; selecting a team narrows to that team. Aggregation honours
metric semantics:
    • counts (tokens, token cost, WIP, deploy freq)  → SUM across teams
    • rates / per-unit (%, days, $/SP, SP/pd, × …)    → team-size-weighted AVG
    • productivity economics                          → SP, effort, cost SUMMED,
      cost/SP and productivity recomputed from the aggregate (true roll-up).

A granularity level (feature vs user-story) scales cycle/lead time and WIP, so
the same scope can be viewed at feature or story altitude — mirroring the
current/future-state VSM level toggle.
"""
import hashlib

from .catalog import METRICS, METRICS_BY_ID
from .productivity import SCENARIO_INPUTS, BASELINE_SP_RATE

# Absolute counts are summed; everything else is a weighted average.
SUM_METRICS = {"token_usage", "token_cost", "wip", "deploy_freq"}

# Granularity level multipliers (feature work items are coarser than stories).
LEVEL_FACTORS = {
    "feature":    {"cycle_time": 2.2, "lead_time": 1.15, "wip": 0.45},
    "user-story": {"cycle_time": 1.0, "lead_time": 1.0,  "wip": 1.0},
}


def _hash01(s: str) -> float:
    return (int(hashlib.md5(s.encode()).hexdigest(), 16) % 10_000) / 10_000.0


def _maturity(team_key: str, scenario: str) -> float:
    """Per-team capability factor 0.85–1.15 (a 'better' team scores higher)."""
    return round(0.85 + _hash01(f"{team_key}|{scenario}|mat") * 0.30, 3)


def _team_size(team_key: str) -> int:
    return 4 + int(_hash01(f"{team_key}|size") * 6)        # 4–9 engineers


def _clamp_pct(v):
    return min(round(v, 1), 99.0)


def _team_metrics(team_key: str, scenario: str, level: str, size_override=None) -> dict:
    """Deterministic metric set + productivity inputs for one leaf team."""
    mat = _maturity(team_key, scenario)
    size = int(size_override) if size_override else _team_size(team_key)
    size_ratio = size / 6.0
    lvl = LEVEL_FACTORS.get(level, LEVEL_FACTORS["feature"])

    vals = {"_team_size": size, "_maturity": mat}
    for m in METRICS:
        mid = m["id"]
        demo = m["demo"][scenario]
        if mid in SUM_METRICS:
            # scale by team size; better teams emit a touch more (more AI use) /
            # fewer (WIP) depending on direction
            if m["better"] == "down":
                v = demo * size_ratio / mat
            else:
                v = demo * size_ratio * (mat if mid in ("token_usage", "token_cost") else 1.0)
        elif m["better"] == "up":
            v = demo * mat
        elif m["better"] == "down":
            v = demo / mat
        else:  # track
            v = demo
        # granularity level adjustment
        if mid in lvl:
            v *= lvl[mid]
        vals[mid] = _clamp_pct(v) if m["unit"] == "%" else round(v, 2)

    # productivity inputs for this team
    base = SCENARIO_INPUTS.get(scenario, SCENARIO_INPUTS["option-a"])
    sp_rate = round(base["sp_rate"] / mat, 4)
    sp_delivered = round(base["sp_delivered"] * size_ratio * mat, 1)
    cfr = METRICS_BY_ID["change_failure_rate"]["demo"][scenario] / 100.0 / mat
    vals.update({"_sp_rate": sp_rate, "_sp_delivered": sp_delivered,
                 "_cfr": round(cfr, 4)})
    return vals


def _leaf_units(product_groups, scope: dict) -> list[dict]:
    """Resolve the leaf teams under the selected scope from a project hierarchy."""
    sel_group = (scope or {}).get("product_group")
    sel_product = (scope or {}).get("product")
    sel_team = (scope or {}).get("team")
    units = []
    for g in (product_groups or []):
        gname = g.get("name") if isinstance(g, dict) else str(g)
        if sel_group and gname != sel_group:
            continue
        products = g.get("products", []) if isinstance(g, dict) else []
        if not products:
            units.append({"group": gname, "product": "(all)", "team": "(all)",
                          "key": f"{gname}"})
            continue
        for p in products:
            pname = p.get("name") if isinstance(p, dict) else str(p)
            if sel_product and pname != sel_product:
                continue
            teams = p.get("teams", []) if isinstance(p, dict) else []
            if not teams:
                units.append({"group": gname, "product": pname, "team": "(all)",
                              "key": f"{gname}/{pname}", "size": None})
                continue
            for t in teams:
                tname = t.get("name") if isinstance(t, dict) else str(t)
                tsize = t.get("size") if isinstance(t, dict) else None
                if sel_team and tname != sel_team:
                    continue
                units.append({"group": gname, "product": pname, "team": tname,
                              "key": f"{gname}/{pname}/{tname}", "size": tsize})
    return units


def rollup(product_groups, scope: dict, scenario: str, level: str) -> dict | None:
    """
    Aggregate leaf-team metrics for the selected scope.
    Returns None when there is no usable hierarchy (caller keeps single-unit demo).
    """
    units = _leaf_units(product_groups, scope)
    if not units:
        return None

    tm = [{**u, **_team_metrics(u["key"], scenario, level, u.get("size"))} for u in units]
    total_w = sum(t["_team_size"] for t in tm) or 1

    base_values = {}
    for m in METRICS:
        mid = m["id"]
        if mid in SUM_METRICS:
            val = sum(t[mid] for t in tm)
        else:
            val = sum(t[mid] * t["_team_size"] for t in tm) / total_w
        base_values[mid] = _clamp_pct(val) if m["unit"] == "%" else round(val, 2)

    # productivity roll-up — SP, effort, cost summed; rates recomputed from totals
    team_size_total = sum(t["_team_size"] for t in tm)
    sp_total = sum(t["_sp_delivered"] for t in tm)
    effort_total = sum(t["_sp_delivered"] * t["_sp_rate"] for t in tm)
    sp_rate_eff = round(effort_total / sp_total, 4) if sp_total else BASELINE_SP_RATE
    cfr_eff = round(sum(t["_cfr"] * t["_sp_delivered"] for t in tm) / sp_total, 4) if sp_total else 0
    prod_inputs = {
        "team_size": team_size_total,
        "sp_delivered": round(sp_total, 1),
        "sp_rate": sp_rate_eff,
        "cfr": cfr_eff,
    }

    breakdown = [{
        "label": t["team"] if t["team"] not in ("(all)", None) else (t["product"] if t["product"] != "(all)" else t["group"]),
        "group": t["group"], "product": t["product"], "team": t["team"],
        "team_size": t["_team_size"],
        "sp_delivered": t["_sp_delivered"],
        "cost_per_sp": round(t["_sp_rate"] * 800),
        "productivity": round(t["_sp_delivered"] / (t["_team_size"] * 10 * 0.8), 2),
    } for t in tm]

    return {
        "base_values": base_values,
        "prod_inputs": prod_inputs,
        "meta": {
            "units": len(tm),
            "teams": sum(1 for t in tm if t["team"] not in ("(all)", None)),
            "level": level,
            "scope": scope or {},
            "breakdown": breakdown,
            "sp_total": round(sp_total, 1),
            "team_size_total": team_size_total,
        },
    }
