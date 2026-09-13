"""
Target State Studio — interim roadmap generator.

Given the current maturity level, the target (North-Star) level, the number of
interim steps (auto-suggested or chosen), the risk appetite and the selected
delivery platform, produce a step-by-step roadmap. Each step carries the ladder
definition, the agents/role posture, retained human roles, an outcome metric band
(reconciled with the Outcome Dashboard scenarios) and a business-case slice that
reuses the real cost model + platform deltas from business_case_builder.
"""
from .catalog import (INTERIM_LADDER, LADDER_BY_LEVEL, MAX_LEVEL, MATURITY_SCORE,
                      RISK_SCORE)
from ..business_case_builder.agent import (C_PLATFORM_OPTIONS, merge_cost_model,
                                           compute_cost_summary)
from ..outcome_metrics.catalog import METRICS_BY_ID

HEADLINE_METRICS = ["cost_per_sp", "lead_time", "flow_efficiency", "deploy_freq",
                    "change_failure_rate", "agent_utilisation"]


def suggest_interims(maturity_band: str | None, risk_appetite: str) -> dict:
    """Recommend the number of interim steps from current-state maturity + risk."""
    m = MATURITY_SCORE.get((maturity_band or "").upper(), 1)   # default ~ CRAWL
    r = RISK_SCORE.get(risk_appetite, 1)
    combined = m + r                       # 0..6
    if combined <= 1:
        count, why = 2, "Low maturity and cautious risk appetite — phase the journey in two interim steps."
    elif combined <= 3:
        count, why = 1, "Moderate maturity / risk — one interim step de-risks the transition."
    else:
        count, why = 0, "High maturity and risk appetite — go to the target state in one move."
    return {"interim_count": count, "rationale": why,
            "maturity_band": maturity_band, "risk_appetite": risk_appetite}


def _stop_levels(current_level: int, target_level: int, interim_count: int) -> list[int]:
    """Pick interim stop levels evenly spread between current & target, then the target.
    1 interim → midpoint (e.g. L0→L5 picks L3); 2 → spread (e.g. L2 & L4)."""
    avail = list(range(current_level + 1, target_level))
    k = max(0, min(interim_count, len(avail)))
    interims = []
    if k:
        n = len(avail)
        interims = sorted({avail[min(n - 1, int((i + 0.5) * n / k))] for i in range(k)})
    return interims + [target_level]


def _metric_band(scenario: str) -> list[dict]:
    out = []
    for mid in HEADLINE_METRICS:
        m = METRICS_BY_ID.get(mid)
        if not m:
            continue
        disp = m.get("display", {}).get(scenario)
        out.append({"id": mid, "name": m["name"], "unit": m["unit"],
                    "target": disp if disp is not None else m["demo"][scenario]})
    return out


def build_roadmap(current_level: int, target_level: int, interim_count: int,
                  risk_appetite: str, platform_id: str) -> dict:
    target_level = max(1, min(target_level, MAX_LEVEL))
    current_level = max(0, min(current_level, target_level - 1))
    platform = C_PLATFORM_OPTIONS.get(platform_id, C_PLATFORM_OPTIONS["homegrown"])
    summary = compute_cost_summary(merge_cost_model(None))

    # Total target economics: platform delta (in $K) applied to homegrown Option C baseline.
    base = summary["option_c"]
    delta_avg_k = (platform.get("investment_delta_usd_low", 0) + platform.get("investment_delta_usd_high", 0)) / 2
    total_one_time = max(0.0, base["one_time"] + delta_avg_k * 1000)
    total_savings = base["annual_savings_portfolio"]
    total_weeks = platform.get("production_ready_weeks", 26)

    stops = _stop_levels(current_level, target_level, interim_count)
    target_automation = LADDER_BY_LEVEL[target_level]["automation_pct"]
    cur_auto = LADDER_BY_LEVEL[current_level]["automation_pct"] if current_level in LADDER_BY_LEVEL else 0

    steps = []
    prev_auto = cur_auto
    for idx, lvl in enumerate(stops):
        L = LADDER_BY_LEVEL[lvl]
        cum_frac = (L["automation_pct"] - cur_auto) / max(1, (target_automation - cur_auto))
        step_frac = (L["automation_pct"] - prev_auto) / max(1, (target_automation - cur_auto))
        prev_auto = L["automation_pct"]
        scen_summary = summary.get(L["outcome_scenario"], base) if L["outcome_scenario"].startswith("option") else base
        steps.append({
            "step": idx + 1,
            "is_target": lvl == target_level,
            "level": lvl, "label": L["label"], "ml_band": L["ml_band"],
            "summary": L["summary"], "agent_role": L["agent_role"], "hitl": L["hitl"],
            "automation_pct": L["automation_pct"],
            "phase_coverage": L["phase_coverage"],
            "human_roles_retained": L["human_roles_retained"],
            "outcome_scenario": L["outcome_scenario"],
            "metric_band": _metric_band(L["outcome_scenario"]),
            "business_case": {
                "cumulative_pct": round(cum_frac * 100),
                "investment_usd": round(total_one_time * cum_frac),
                "step_investment_usd": round(total_one_time * step_frac),
                "annual_benefit_usd": round(scen_summary.get("annual_savings_portfolio", total_savings)),
                "payback_months": scen_summary.get("payback_months"),
                "timeline_weeks": round(total_weeks * cum_frac),
            },
        })

    # Platform business-case detail (same across steps) so the future-state view can
    # render all Business Case tabs — operating model, agents/tools, DevSecOps, AIOps,
    # org/product changes — populated for the chosen platform.
    platform_detail = {
        "id": platform_id, "name": platform["name"],
        "tagline": platform.get("tagline", ""),
        "investment_delta_text": platform.get("investment_delta_text", ""),
        "platform_ops_team": platform.get("platform_ops_team", {}),
        "agents_construction": platform.get("agents_construction", ""),
        "tools_changes": platform.get("tools_changes", []),
        "devsecops_changes": platform.get("devsecops_changes", []),
        "aiops_changes": platform.get("aiops_changes", []),
        "product_centric_changes": platform.get("product_centric_changes", []),
        "org_changes_override": platform.get("org_changes_override", []),
        "playbook_phasing": platform.get("playbook_phasing", []),
        "pros": platform.get("pros", []), "cons": platform.get("cons", []),
    }

    return {
        "platform": platform_id, "platform_name": platform["name"],
        "current_level": current_level, "target_level": target_level,
        "interim_count": len(stops) - 1, "risk_appetite": risk_appetite,
        "ladder": INTERIM_LADDER,
        "stops": stops,
        "steps": steps,
        "platform_detail": platform_detail,
        "cost_summary": {k: summary[k] for k in ("option_b", "option_c") if k in summary},
        "totals": {"one_time_usd": round(total_one_time),
                   "annual_benefit_usd": round(total_savings),
                   "timeline_weeks": total_weeks,
                   "payback_months": base.get("payback_months")},
    }
