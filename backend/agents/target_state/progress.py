"""
Target State Studio — transformation progress.

Measures how far the org has moved toward the next interim stop and the target
(North-Star) level across several components: maturity level, phase coverage,
agents activated, human-role transition, and outcome KPIs (reconciled with the
Outcome Dashboard scenario bands). Uses the saved config; agent-activation can be
fed from the composition (per-agent `active` flag) or inferred from the level.
"""
from .catalog import LADDER_BY_LEVEL, INTERIM_LADDER, PDLC_PHASES


def _pct(n, d):
    return round((n / d) * 100) if d else 0


def compute_progress(config: dict) -> dict:
    target_level = int(config.get("target_level") or 5)
    current_level = int(config.get("current_level") or 0)
    stops = config.get("interim_levels") or []
    comp = config.get("target_composition") or {}

    L_target = LADDER_BY_LEVEL.get(target_level, INTERIM_LADDER[-1])
    L_cur = LADDER_BY_LEVEL.get(current_level)
    L1 = INTERIM_LADDER[0]

    # next milestone = first stop above the current level (else target)
    next_level = next((s for s in sorted(stops) if s > current_level), target_level)
    L_next = LADDER_BY_LEVEL.get(next_level, L_target)

    # ── components ────────────────────────────────────────────────────────────
    cur_auto = L_cur["automation_pct"] if L_cur else 0
    maturity_pct = _pct(current_level, target_level)

    cur_phases = len(L_cur["phase_coverage"]) if L_cur else 0
    phase_pct = _pct(cur_phases, len(L_target["phase_coverage"]))

    agents = comp.get("agents") or []
    if agents:
        active = sum(1 for a in agents if (a.get("active") if isinstance(a, dict) else False))
        agents_pct = _pct(active, len(agents))
        agents_detail = f"{active}/{len(agents)} agents activated"
    else:
        agents_pct = _pct(cur_auto, L_target["automation_pct"])
        agents_detail = f"~{cur_auto}% automation vs {L_target['automation_pct']}% target"

    # human-role transition: from L1's full roster down to target's lean roster
    roles_l1, roles_tgt = len(L1["human_roles_retained"]), len(L_target["human_roles_retained"])
    roles_cur = len(L_cur["human_roles_retained"]) if L_cur else roles_l1
    role_pct = _pct(roles_l1 - roles_cur, max(1, roles_l1 - roles_tgt))

    # outcome: automation as proxy for KPI gap closed toward target
    outcome_pct = _pct(cur_auto, L_target["automation_pct"])

    components = [
        {"key": "maturity", "label": "Maturity level", "pct": maturity_pct,
         "detail": f"L{current_level} → L{target_level} ({L_target['ml_band']})"},
        {"key": "phases", "label": "Phases agentified", "pct": phase_pct,
         "detail": f"{cur_phases}/{len(L_target['phase_coverage'])} PDLC phases"},
        {"key": "agents", "label": "Agents activated", "pct": agents_pct, "detail": agents_detail},
        {"key": "roles", "label": "Human-role transition", "pct": role_pct,
         "detail": f"{roles_cur} → {roles_tgt} retained human roles"},
        {"key": "outcomes", "label": "Outcome KPIs", "pct": outcome_pct,
         "detail": f"toward {L_target['outcome_scenario'].replace('option-', 'Option ').upper()} bands"},
    ]
    overall = round(sum(c["pct"] for c in components) / len(components))

    return {
        "overall_pct": overall,
        "current_level": current_level, "target_level": target_level,
        "next_milestone": {"level": next_level, "label": L_next["label"], "ml_band": L_next["ml_band"]},
        "components": components,
    }
