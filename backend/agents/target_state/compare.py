"""
Target State Studio — platform comparison & recommendation.

Compares the target-state delivery platforms (home-grown, COTS, service-provider)
across a fixed set of decision parameters (1–5 ratings, higher = better), plus
hard facts (weeks-to-prod, investment vs baseline, in-house team size) and the
pros/cons already in the catalog. Produces a weighted overall score, a rank, and
a recommended choice with a rationale.
"""
from .catalog import RISK_SCORE
from ..business_case_builder.agent import (C_PLATFORM_OPTIONS, PLATFORM_KIND,
                                           TARGET_STATE_PLATFORM_ORDER)

# Decision parameters (all "higher is better" after normalisation).
PARAMS = [
    {"key": "control",            "label": "Architectural control & customization"},
    {"key": "speed_to_value",     "label": "Speed to value"},
    {"key": "cost_at_scale",      "label": "Unit economics at scale"},
    {"key": "low_upfront",        "label": "Low upfront cost"},
    {"key": "low_inhouse_burden", "label": "Low in-house ops burden"},
    {"key": "vendor_independence","label": "Vendor independence (no lock-in)"},
    {"key": "compliance_ready",   "label": "Built-in compliance readiness"},
    {"key": "low_talent_need",    "label": "Low scarce-talent requirement"},
]

# 1–5 ratings per platform per parameter.
SCORES = {
    "homegrown":         {"control": 5, "speed_to_value": 2, "cost_at_scale": 5, "low_upfront": 1, "low_inhouse_burden": 1, "vendor_independence": 5, "compliance_ready": 3, "low_talent_need": 1},
    "bmad":              {"control": 3, "speed_to_value": 4, "cost_at_scale": 3, "low_upfront": 3, "low_inhouse_burden": 3, "vendor_independence": 2, "compliance_ready": 3, "low_talent_need": 3},
    "copilot_workspace": {"control": 3, "speed_to_value": 4, "cost_at_scale": 3, "low_upfront": 3, "low_inhouse_burden": 4, "vendor_independence": 2, "compliance_ready": 3, "low_talent_need": 4},
    "devin":             {"control": 2, "speed_to_value": 5, "cost_at_scale": 2, "low_upfront": 3, "low_inhouse_burden": 4, "vendor_independence": 2, "compliance_ready": 2, "low_talent_need": 4},
    "cursor":            {"control": 3, "speed_to_value": 4, "cost_at_scale": 3, "low_upfront": 4, "low_inhouse_burden": 4, "vendor_independence": 2, "compliance_ready": 3, "low_talent_need": 4},
    "flowsource":        {"control": 2, "speed_to_value": 5, "cost_at_scale": 2, "low_upfront": 2, "low_inhouse_burden": 5, "vendor_independence": 1, "compliance_ready": 4, "low_talent_need": 5},
    "baxter":            {"control": 2, "speed_to_value": 5, "cost_at_scale": 3, "low_upfront": 2, "low_inhouse_burden": 5, "vendor_independence": 1, "compliance_ready": 5, "low_talent_need": 5},
}

# Balanced weights; risk-appetite tilts speed/burden vs control/economics.
BASE_WEIGHTS = {
    "control": 0.15, "speed_to_value": 0.18, "cost_at_scale": 0.12, "low_upfront": 0.10,
    "low_inhouse_burden": 0.15, "vendor_independence": 0.10, "compliance_ready": 0.10, "low_talent_need": 0.10,
}


def _weights(risk_appetite: str | None) -> dict:
    r = RISK_SCORE.get(risk_appetite or "medium", 1)   # 0 low, 1 med, 2 high
    w = dict(BASE_WEIGHTS)
    if r == 0:        # low risk → value control, compliance, economics
        w["control"] += 0.05; w["compliance_ready"] += 0.05; w["cost_at_scale"] += 0.03
        w["speed_to_value"] -= 0.07; w["low_inhouse_burden"] -= 0.06
    elif r == 2:      # high risk → value speed & low burden
        w["speed_to_value"] += 0.07; w["low_inhouse_burden"] += 0.05
        w["control"] -= 0.07; w["cost_at_scale"] -= 0.05
    total = sum(w.values())
    return {k: v / total for k, v in w.items()}


def _team_size(pid: str) -> str:
    return (C_PLATFORM_OPTIONS.get(pid, {}).get("platform_ops_team") or {}).get("size", "—")


def compare_platforms(risk_appetite: str | None = None) -> dict:
    weights = _weights(risk_appetite)
    rows = []
    overall = {}
    for pid in TARGET_STATE_PLATFORM_ORDER:
        if pid not in SCORES:
            continue
        sc = SCORES[pid]
        overall[pid] = round(sum(sc[k] * weights[k] for k in weights) / 5 * 100)  # 0–100

    platforms = []
    ranked = sorted(overall.items(), key=lambda kv: -kv[1])
    rank_of = {pid: i + 1 for i, (pid, _) in enumerate(ranked)}
    for pid in TARGET_STATE_PLATFORM_ORDER:
        if pid not in SCORES:
            continue
        p = C_PLATFORM_OPTIONS[pid]
        platforms.append({
            "id": pid, "name": p["name"], "kind": PLATFORM_KIND.get(pid, "cots"),
            "is_us_bank_target": pid == "homegrown",
            "scores": SCORES[pid], "overall": overall[pid], "rank": rank_of[pid],
            "weeks_to_prod": p.get("production_ready_weeks"),
            "investment_delta_text": p.get("investment_delta_text", ""),
            "team_size": _team_size(pid),
            "pros": p.get("pros", []), "cons": p.get("cons", []),
        })

    # parameter × platform matrix (for the comparison table)
    matrix = [{"key": prm["key"], "label": prm["label"],
               "weight": round(weights[prm["key"]] * 100),
               "values": {pid: SCORES[pid][prm["key"]] for pid in overall}}
              for prm in PARAMS]

    top_id, top_score = ranked[0]
    top = C_PLATFORM_OPTIONS[top_id]
    top_dims = sorted(SCORES[top_id].items(), key=lambda kv: -kv[1])[:3]
    dim_label = {p["key"]: p["label"] for p in PARAMS}
    rationale = (f"{top['name']} scores highest overall ({top_score}/100) for a "
                 f"{(risk_appetite or 'medium')}-risk appetite — strongest on "
                 f"{', '.join(dim_label[k].lower() for k, _ in top_dims)}.")

    # context picks
    best_for = {
        "fastest_value": max(overall, key=lambda p: SCORES[p]["speed_to_value"]),
        "max_control": max(overall, key=lambda p: SCORES[p]["control"]),
        "lowest_burden": max(overall, key=lambda p: SCORES[p]["low_inhouse_burden"]),
    }

    return {
        "params": PARAMS, "platforms": platforms, "matrix": matrix,
        "risk_appetite": risk_appetite or "medium",
        "recommendation": {"platform": top_id, "name": top["name"],
                           "overall": top_score, "rationale": rationale,
                           "best_for": {k: C_PLATFORM_OPTIONS[v]["name"] for k, v in best_for.items()}},
    }
