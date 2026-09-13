"""
Outcome Dashboard — Productivity economics engine.

Implements the STUMP measurement formulas (deck slides 14–17) end-to-end:

    Story Points  →  Effort (person-days)  →  Cost (USD)  →  Unit economics

Formula chain:
    capacity            = team_size × sprint_days × utilisation
    SP rate (days/SP)   = avg effort logged ÷ SP accepted      (6-sprint calibration)
    effort (person-days)= SP delivered × SP rate
    cost ($)            = effort × blended daily rate
    cost per SP ($)     = total cost ÷ SP delivered            (= SP rate × daily rate)
    productivity        = SP delivered ÷ capacity              (SP / person-day)
    quality-adjusted    = SP × (1 − CFR) ÷ capacity
    productivity index  = (current SP/day ÷ baseline SP/day) × 100

Savings are measured against the pre-AI baseline (slide 15: same budget, more
value — −$/SP and $ saved per sprint).

Inputs default to slide-aligned per-scenario assumptions but accept overrides so
that, once a Jira/ADO + Finance feed is connected, the real SP delivered, effort
logs, CFR and blended rate flow straight in (zero manual entry).
"""
from .catalog import METRICS_BY_ID

# Shared cost/capacity assumptions (Finance/HR feed; slide 17 worked example).
TEAM_SIZE = 6
SPRINT_DAYS = 10
UTILISATION = 0.8
BLENDED_DAILY_RATE = 800        # $ per person-day

# Pre-AI baseline (slide 15): 60 SP/sprint @ $500/SP.
BASELINE_SP = 60
BASELINE_SP_RATE = 0.625        # days/SP  → 0.625 × $800 = $500/SP

# ── DORA "ROI of AI-assisted software development (2026)" alignment ───────────
# Investment (hard costs) — DORA sample defaults (per user / yr). Override per org.
AI_LICENSE_PER_USER_YR = 250     # base subscription
AI_USAGE_PER_USER_YR   = 80      # variable API / token cost
TRAINING_PER_USER_YR   = 2400    # enablement (DORA sample $9.6k is high; conservative default)
INFRA_COST_YR          = 100_000 # additional AI infra (compute/storage/monitoring), org-level
# J-Curve (Figure 2, p9 / p32): initial productivity dip = "tuition cost".
JCURVE_DROP_PCT        = 0.15    # 15% capacity temporarily lost
JCURVE_MONTHS          = 3       # duration of the dip
SPRINTS_PER_YEAR       = 26      # 2-week sprints
SPRINT_WEEKS           = 2
WORKDAYS_PER_YEAR      = 220     # to derive annual salary from blended daily rate
ADOPT_SPRINTS          = 6       # ramp to full steady-state productivity gain

# Per-platform recurring run-cost profile — the ONGOING cost differs by how the
# target state is delivered (home-grown vs COTS vs service-provider). It includes
# agent TOKEN/usage cost, per-seat licence, the platform-ops team headcount, and
# any managed-platform fee. Token cost also scales with the maturity level (more
# autonomous agents → more tokens) via the catalog `token_cost` metric.
#   license_user_yr  : per-developer subscription ($/user/yr); home-grown = 0
#   ops_fte          : platform/agent ops team headcount (recurring salaried)
#   platform_fee_yr  : managed-platform / service fee ($/yr), org-level
#   token_mult       : multiplier on the level's token_cost metric (build-your-own
#                      stacks tend to run hotter; managed platforms optimise usage)
PLATFORM_RUN = {
    "homegrown":         {"license_user_yr": 0,   "ops_fte": 7, "platform_fee_yr": 0,       "token_mult": 1.15},
    "bmad":              {"license_user_yr": 0,   "ops_fte": 4, "platform_fee_yr": 0,       "token_mult": 1.0},
    "copilot_workspace": {"license_user_yr": 400, "ops_fte": 2, "platform_fee_yr": 0,       "token_mult": 0.9},
    "devin":             {"license_user_yr": 600, "ops_fte": 2, "platform_fee_yr": 0,       "token_mult": 1.0},
    "cursor":            {"license_user_yr": 480, "ops_fte": 2, "platform_fee_yr": 0,       "token_mult": 0.9},
    "flowsource":        {"license_user_yr": 0,   "ops_fte": 2, "platform_fee_yr": 300_000, "token_mult": 0.85},
}
# Agent/token spend per developer per sprint, rising with autonomy (more agents,
# more orchestration → more tokens). Scales with team size; level-dependent.
TOKEN_PER_DEV_SPRINT = {"option-a": 40, "option-b": 90, "option-c": 180}
# Platform-ops team + managed fee are SHARED across the pods on the platform — a
# single team funds only its share. Prorate across this many pods by default.
PODS_SHARED = 6

# Per-scenario calibrated SP rate (effort per SP falls as AI deepens) and the
# observed SP delivered. Cost/SP = sp_rate × daily_rate → $500 / $425 / $360,
# matching the Option A→B→C progression matrix.
SCENARIO_INPUTS = {
    # Option A (augmented human / AI co-pilot) is the FIRST AI step — a modest gain
    # over the pre-AI baseline (0.625 d/SP), not equal to it. B and C deepen it.
    "option-a": {"sp_rate": 0.590, "sp_delivered": 72},   # → ~$472/SP, ~+6%
    "option-b": {"sp_rate": 0.531, "sp_delivered": 84},   # → ~$425/SP, ~+18%
    "option-c": {"sp_rate": 0.450, "sp_delivered": 100},  # → ~$360/SP, ~+39%
}


def _cfr(scenario: str) -> float:
    """Change failure rate (0–1) from the metric catalog demo midpoints."""
    return METRICS_BY_ID["change_failure_rate"]["demo"][scenario] / 100.0


def compute_productivity(scenario: str, overrides: dict | None = None) -> dict:
    """
    Run the full SP→Effort→Cost→unit-economics chain for a scenario.
    `overrides` may supply any of: team_size, sprint_days, utilisation,
    blended_daily_rate, sp_rate, sp_delivered, cfr (live ALM/Finance values).
    """
    o = overrides or {}
    base = SCENARIO_INPUTS.get(scenario, SCENARIO_INPUTS["option-a"])

    team_size   = o.get("team_size", TEAM_SIZE)
    sprint_days = o.get("sprint_days", SPRINT_DAYS)
    utilisation = o.get("utilisation", UTILISATION)
    daily_rate  = o.get("blended_daily_rate", BLENDED_DAILY_RATE)
    sp_rate     = o.get("sp_rate", base["sp_rate"])
    sp_delivered = o.get("sp_delivered", base["sp_delivered"])
    cfr         = o.get("cfr", _cfr(scenario))

    # AI is never WORSE than the pre-AI baseline effort-per-SP, so a scenario or a
    # rolled-up average that drifts slightly above 0.625 d/SP can't produce negative
    # "savings". (Option A sits exactly at the baseline → zero gain, which is correct.)
    sp_rate = min(sp_rate, BASELINE_SP_RATE)

    # ── formula chain (all figures derive from these inputs) ──────────────────
    capacity      = round(team_size * sprint_days * utilisation, 1)        # person-days
    effort        = round(sp_delivered * sp_rate, 1)                       # person-days consumed
    sprint_cost   = round(effort * daily_rate)                             # $ — the budget
    cost_per_sp   = round(sp_rate * daily_rate, 2)                         # = sprint_cost ÷ sp_delivered
    productivity  = round(sp_delivered / capacity, 2) if capacity else 0   # SP/person-day delivered
    adj_prod      = round(sp_delivered * (1 - cfr) / capacity, 2) if capacity else 0
    baseline_cost_per_sp = round(BASELINE_SP_RATE * daily_rate)            # $500 @ $800/day

    # ── Baseline is DERIVED from the SAME effort/budget at the pre-AI SP-rate ─────
    # i.e. "with this exact spend, how many SP would the team have shipped before AI?"
    # This guarantees SP uplift %, productivity index and cost/SP reduction all move
    # together (one lever = sp_rate); budget is identical pre/post (same-budget story).
    baseline_sp_scope = round(effort / BASELINE_SP_RATE, 1)                # ≤ sp_delivered
    baseline_budget   = sprint_cost                                        # SAME budget
    baseline_prod     = round(baseline_sp_scope / capacity, 3) if capacity else 0
    prod_index        = round((sp_delivered / baseline_sp_scope) * 100) if baseline_sp_scope else 100
    saving_per_sp     = round(baseline_cost_per_sp - cost_per_sp, 2)

    # ── The single gain, expressed as MORE OUTPUT and as the reconciled trio ──────
    # More output (same budget): extra SP shipped for the identical spend.
    sp_uplift            = round(sp_delivered - baseline_sp_scope, 1)
    sp_uplift_pct        = round((sp_uplift / baseline_sp_scope) * 100) if baseline_sp_scope else 0
    extra_sp_same_budget = sp_uplift
    pct_more_value       = sp_uplift_pct
    # The SAME gain banked as effort instead (deliver the baseline output with AI):
    #   effort_saved(pd) × daily = cost_saved($) ; effort_saved ÷ sp_rate = sp_gained(SP)
    # and sp_gained == sp_uplift, so the two framings reconcile exactly.
    effort_baseline_equiv = round(baseline_sp_scope * BASELINE_SP_RATE, 1)  # = effort (same budget)
    effort_ai_equiv       = round(baseline_sp_scope * sp_rate, 1)
    effort_saved          = round(effort_baseline_equiv - effort_ai_equiv, 1)
    effort_reduction_pct  = round((effort_saved / effort_baseline_equiv) * 100) if effort_baseline_equiv else 0
    cost_saved            = round(effort_saved * daily_rate)
    sp_gained             = round(effort_saved / sp_rate, 1) if sp_rate else 0

    # ── transparent 4-step worked breakdown (slide 17 layout) ────────────────
    steps = [
        {"step": 1, "title": "Calibrate SP rate",
         "formula": "SP rate (days/SP) = avg effort logged ÷ SP accepted",
         "substitution": f"6-sprint rolling calibration → {sp_rate} days/SP",
         "result": f"{sp_rate} days/SP",
         "note": "Recalibrated quarterly from Jira/ADO time logs."},
        {"step": 2, "title": "SP → Effort",
         "formula": "Effort (person-days) = SP delivered × SP rate",
         "substitution": f"{sp_delivered} SP × {sp_rate} = {effort} person-days",
         "result": f"{effort} person-days",
         "note": "Productive capacity actually consumed."},
        {"step": 3, "title": "Effort → Cost",
         "formula": "Cost ($) = effort × blended daily rate",
         "substitution": f"{effort} × ${daily_rate:,}/day = ${sprint_cost:,}",
         "result": f"${sprint_cost:,}",
         "note": "Blended rate from Finance/HR feed."},
        {"step": 4, "title": "Unit economics",
         "formula": "Cost per SP = total cost ÷ SP delivered",
         "substitution": f"${sprint_cost:,} ÷ {sp_delivered} SP = ${cost_per_sp:,.0f}/SP",
         "result": f"${cost_per_sp:,.0f} / SP",
         "note": "Tracked sprint-over-sprint vs the $500 baseline."},
    ]

    return {
        "scenario": scenario,
        "inputs": {
            "team_size": team_size, "sprint_days": sprint_days,
            "utilisation": utilisation, "blended_daily_rate": daily_rate,
            "sp_rate": sp_rate, "sp_delivered": sp_delivered,
            "cfr": round(cfr, 3), "capacity": capacity,
        },
        "results": {
            "capacity_person_days": capacity,
            "effort_person_days": effort,
            "sprint_cost_usd": sprint_cost,
            "cost_per_sp_usd": cost_per_sp,
            "productivity_sp_per_pd": productivity,
            "quality_adjusted_sp_per_pd": adj_prod,
            "productivity_index": prod_index,
        },
        "baseline": {
            "sp_delivered": baseline_sp_scope,        # pre-AI equivalent output for this scope
            "cost_per_sp_usd": baseline_cost_per_sp,
            "productivity_sp_per_pd": baseline_prod,
            "sprint_budget_usd": baseline_budget,
            "effort_person_days": effort_baseline_equiv,
        },
        "savings": {
            "saving_per_sp_usd": saving_per_sp,
            # the SAME saving expressed three ways (fully reconciled):
            "effort_saved_pd": effort_saved,          # days
            "cost_saved_usd": cost_saved,             # = effort_saved × blended daily rate
            "sp_gained": sp_gained,                   # = effort_saved ÷ SP rate
            "effort_reduction_pct": effort_reduction_pct,
            # equivalent framings (algebraically identical to the trio above):
            "extra_sp_same_budget": extra_sp_same_budget,
            "pct_more_value": pct_more_value,
            "effort_baseline_equiv_pd": effort_baseline_equiv,
            "effort_ai_equiv_pd": effort_ai_equiv,
            "equiv_basis_sp": baseline_sp_scope,
            # actual throughput uplift (current delivery vs scope pre-AI equivalent):
            "sp_uplift": sp_uplift,
            "sp_uplift_pct": sp_uplift_pct,
        },
        "conversion": {
            "blended_daily_rate": daily_rate,
            "sp_rate": sp_rate,
            "note": f"Effort {effort_saved:g} pd × ${daily_rate:,}/day = ${cost_saved:,} ; "
                    f"{effort_saved:g} pd ÷ {sp_rate} d/SP = {sp_gained:g} SP ; "
                    f"check: {sp_gained:g} SP × ${cost_per_sp:,.0f}/SP = ${round(sp_gained*cost_per_sp):,}",
        },
        "steps": steps,
    }


def dora_defaults(scenario: str = "option-c", platform: str = "homegrown") -> dict:
    """Default J-Curve / investment assumptions (for the editable inputs UI)."""
    pf = PLATFORM_RUN.get(platform, PLATFORM_RUN["homegrown"])
    return {
        "token_per_dev_sprint": TOKEN_PER_DEV_SPRINT.get(scenario, 90),
        "ai_license_per_user_yr": pf["license_user_yr"],
        "training_per_user_yr": TRAINING_PER_USER_YR,
        "infra_per_user_yr": round(INFRA_COST_YR / 500),
        "jcurve_drop_pct": round(JCURVE_DROP_PCT * 100),   # shown as percent
        "jcurve_months": JCURVE_MONTHS,
        "adopt_sprints": ADOPT_SPRINTS,
        "pods_shared": PODS_SHARED,
    }


def compute_value_trend(scenario: str, overrides: dict | None = None,
                        horizon_sprints: int = 13, dora: dict | None = None,
                        platform: str = "homegrown") -> dict:
    """
    DORA-aligned, cost-only J-Curve value trend (Figure 2 p9 + Figure 5 p22).

    Models, sprint-by-sprint, the journey to an interim/target state:
      • Investment   — hard costs (license + AI usage/token + training + infra) × staff.
      • J-Curve dip  — initial extra effort/cost (learning curve + verification tax),
                       = J-Curve drop% × team capacity cost, decaying over the dip period.
      • Net saving   — gross efficiency saving (cost-avoidance only; NO feature revenue)
                       ramped by adoption, minus the J-Curve drag and recurring tool cost.
      • Cumulative   — running net minus upfront investment → the J-Curve; the sprint it
                       crosses zero is breakeven; net saving grows sprint-on-sprint after.

    Excludes business-growth/revenue levers entirely, per requirement.
    """
    d = dora or {}
    prod = compute_productivity(scenario, overrides)
    team_size   = prod["inputs"]["team_size"]
    daily_rate  = prod["inputs"]["blended_daily_rate"]
    capacity_pd = prod["inputs"]["capacity"]
    baseline_prod = prod["baseline"]["productivity_sp_per_pd"]
    after_prod    = prod["results"]["productivity_sp_per_pd"]
    # Steady-state $ saved per sprint at full productivity (cost-avoidance basis).
    steady_saving = prod["savings"]["cost_saved_usd"]

    train_u   = d.get("training_per_user_yr", TRAINING_PER_USER_YR)
    infra_u   = d.get("infra_per_user_yr", round(INFRA_COST_YR / 500))   # ≈ $200/user
    jdrop     = d.get("jcurve_drop_pct", JCURVE_DROP_PCT)
    if jdrop > 1:            # accept percent (e.g. 15) from the UI → fraction
        jdrop = jdrop / 100.0
    jmonths   = d.get("jcurve_months", JCURVE_MONTHS)
    adopt     = max(1, d.get("adopt_sprints", ADOPT_SPRINTS))

    # ── Platform-aware ONGOING cost (includes agent TOKEN cost) ──────────────
    pf = PLATFORM_RUN.get(platform, PLATFORM_RUN["homegrown"])
    pods_shared = max(1, d.get("pods_shared", PODS_SHARED))
    license_u = d.get("ai_license_per_user_yr", pf["license_user_yr"])
    # Agent/token spend — per-developer × team size × platform multiplier (scales
    # with the level's autonomy). Direct, usage-based cost charged to the team.
    token_per_dev = d.get("token_per_dev_sprint", TOKEN_PER_DEV_SPRINT.get(scenario, 90))
    token_cost_per_sprint = round(token_per_dev * team_size * pf["token_mult"])
    # Per-seat licence (COTS) amortised to a sprint — direct, scales with the team.
    license_per_sprint = round(license_u * team_size / SPRINTS_PER_YEAR)
    # Platform / agent-ops team — SHARED across pods, so charge only this team's share.
    annual_salary = daily_rate * WORKDAYS_PER_YEAR
    ops_cost_per_sprint = round(pf["ops_fte"] * annual_salary / SPRINTS_PER_YEAR / pods_shared)
    # Managed-platform / service-provider fee — shared across pods.
    fee_per_sprint = round(pf["platform_fee_yr"] / SPRINTS_PER_YEAR / pods_shared)
    # Infra (compute/storage/monitoring) — scales with the team.
    infra_per_sprint = round(infra_u * team_size / SPRINTS_PER_YEAR)
    # Total recurring ongoing cost per sprint for the selected platform.
    tool_cost_per_sprint = (token_cost_per_sprint + license_per_sprint
                            + ops_cost_per_sprint + fee_per_sprint + infra_per_sprint)

    # Investment split: enablement is upfront; the above are recurring.
    one_time_investment = round(train_u * team_size)
    sprint_capacity_cost = capacity_pd * daily_rate
    jcurve_sprints = max(1, round(jmonths / 12 * SPRINTS_PER_YEAR))

    series, cumulative, breakeven = [], -float(one_time_investment), None
    value_total = drag_total = tool_total = 0.0
    for t in range(1, horizon_sprints + 1):
        adoption = min(1.0, t / adopt)
        decay = max(0.0, 1 - (t - 1) / jcurve_sprints)
        gross = steady_saving * adoption
        drag = jdrop * sprint_capacity_cost * decay
        net = gross - drag - tool_cost_per_sprint
        cumulative += net
        productivity = round(baseline_prod * (1 - jdrop * decay) + (after_prod - baseline_prod) * adoption, 2)
        value_total += gross; drag_total += drag; tool_total += tool_cost_per_sprint
        if breakeven is None and cumulative >= 0:
            breakeven = t
        series.append({
            "sprint": f"S{t}",
            "gross_saving": round(gross),
            "jcurve_drag": -round(drag),                 # negative = cost during dip
            "tool_cost": -round(tool_cost_per_sprint),
            "net_saving": round(net),
            "cumulative_net": round(cumulative),
            "productivity": productivity,
        })

    investment_total = one_time_investment + tool_total + drag_total
    roi_pct = round((value_total - investment_total) / investment_total * 100) if investment_total else 0
    return {
        "scenario": scenario,
        "platform": platform,
        "horizon_sprints": horizon_sprints,
        "sprint_weeks": SPRINT_WEEKS,
        "one_time_investment_usd": one_time_investment,
        "tool_cost_per_sprint_usd": tool_cost_per_sprint,
        "ongoing_cost_breakdown": {
            "token_agent_usd": token_cost_per_sprint,
            "licence_usd": license_per_sprint,
            "platform_ops_usd": ops_cost_per_sprint,
            "managed_fee_usd": fee_per_sprint,
            "infra_usd": infra_per_sprint,
            "ops_fte": pf["ops_fte"],
        },
        "jcurve_drop_pct": round(jdrop * 100),
        "jcurve_sprints": jcurve_sprints,
        "jcurve_cost_total_usd": round(drag_total),
        "steady_state_saving_per_sprint_usd": round(steady_saving),
        "breakeven_sprint": breakeven,
        "value_total_usd": round(value_total),
        "investment_total_usd": round(investment_total),
        "roi_pct": roi_pct,
        "series": series,
        "assumptions": {
            "ai_license_per_user_yr": license_u, "training_per_user_yr": train_u,
            "infra_per_user_yr": infra_u, "team_size": team_size,
            "blended_daily_rate": daily_rate, "token_mult": pf["token_mult"],
        },
        "note": ("Cost-only (excludes feature-revenue/business-growth). Investment + J-Curve "
                 "tuition cost early; net savings grow sprint-on-sprint and cross breakeven."),
    }
