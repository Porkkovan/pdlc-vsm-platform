"""
Outcome Dashboard — metrics engine.

Assembles the full dashboard payload for a given scenario (option-a/b/c) and the
three perspectives. Uses deterministic demo data derived from the STUMP metrics
framework (slides 12–18) and overlays any live values fetched from connected
data sources (Jira / GitHub / CI-CD / AI platform).

Payload shape (consumed directly by the React page):
{
  scenario, source_mode, generated_at,
  perspectives: {
    adoption|performance|ai_ops: {
      key, label, blurb,
      kpis:   [{id,label,value,display,unit,better,target,delta,delta_dir}],
      charts: [{id,title,subtitle,type,data,series,xKey,target,unit,metric_id}],
      facts:  [str, ...],         # plain-language facts fed to the inference generator
      inferences: [{title,text,severity}]   # filled in by inferences.py
    }
  },
  progression_matrix: [...]
}
"""
from datetime import datetime
from .catalog import (METRICS, METRICS_BY_ID, PERSPECTIVES, PHASE_SHORT,
                      matrix_rows)
from .productivity import compute_productivity, compute_value_trend

SCEN_LABEL = {"option-a": "Option A", "option-b": "Option B", "option-c": "Option C"}
SCEN_COLOR = {"option-a": "#2563eb", "option-b": "#7c3aed", "option-c": "#059669"}

# ── Per-phase / per-sprint demo breakdowns (illustrative, slide-aligned) ──────
UTIL_BY_PHASE = {
    "option-a": [38, 28, 52, 46, 42, 22, 18],
    "option-b": [62, 55, 78, 72, 68, 58, 52],
    "option-c": [88, 84, 95, 93, 90, 86, 84],
}
FLOW_EFF_BY_PHASE = {
    "option-a": [33, 41, 56, 38, 31, 40, 34],
    "option-b": [48, 52, 64, 50, 46, 54, 49],
    "option-c": [60, 64, 72, 62, 58, 66, 61],
}
PHASE_TOTAL_DAYS = {   # lead time per phase (process + wait), shrinks A→C
    "option-a": [4, 5, 6, 4, 5.5, 4, 5],
    "option-b": [2.4, 3, 3.5, 2.4, 3.2, 2.4, 3],
    "option-c": [1.2, 1.5, 1.8, 1.2, 1.6, 1.2, 1.5],
}
ACCEPT_TREND = {
    "option-a": [56, 61, 65, 68, 71, 72],
    "option-b": [70, 73, 76, 78, 80, 82],
    "option-c": [84, 87, 89, 90, 91, 92],
}
ROI_TREND = {
    "option-a": [1.4, 1.7, 1.9, 2.0, 2.1, 2.2],
    "option-b": [2.6, 3.0, 3.3, 3.5, 3.7, 3.8],
    "option-c": [3.8, 4.3, 4.7, 4.9, 5.1, 5.2],
}
LEAD_TREND = {
    "option-a": [28, 27, 26, 25, 24, 24],
    "option-b": [20, 17, 15, 14, 13, 12],
    "option-c": [11, 9, 7, 6, 5, 5],
}
CYCLE_TREND = {
    "option-a": [14, 13, 12, 11, 10, 10],
    "option-b": [9, 8, 7, 6, 5, 5],
    "option-c": [4, 3, 2.4, 2, 1.9, 1.8],
}
COST_PER_SP_TREND = {
    "option-a": [520, 515, 510, 505, 502, 500],
    "option-b": [490, 470, 455, 440, 430, 425],
    "option-c": [430, 410, 390, 375, 365, 360],
}
TOKEN_COST_TREND = {
    "option-a": [1100, 1250, 1380, 1480, 1550, 1600],
    "option-b": [2800, 3300, 3700, 4000, 4250, 4400],
    "option-c": [6000, 6900, 7600, 8200, 8700, 9000],
}
SPRINTS = ["S1", "S2", "S3", "S4", "S5", "S6"]

# Agents that consume tokens (for the token-by-agent chart)
TOKEN_AGENTS = ["Requirements", "Architecture", "CodeGen", "Code Review",
                "QA / Test", "Release Gate", "Ops Monitor"]


def _num(scenario, metric_id, live):
    """Live value if present, else demo midpoint for the metric/scenario."""
    if live and metric_id in live and live[metric_id] is not None:
        return live[metric_id]
    return METRICS_BY_ID[metric_id]["demo"][scenario]


def _kpi_insight(metric_id, val):
    """One-line takeaway for a metric vs its Option-B target."""
    m = METRICS_BY_ID[metric_id]
    rng_b = m["ranges"]["option-b"]
    better = m["better"]
    if better == "track" or val is None:
        return f"Monitor sprint-over-sprint against the established baseline."
    try:
        on = (val >= m["demo"]["option-b"]) if better == "up" else (val <= m["demo"]["option-b"])
    except TypeError:
        return f"Monitor against the Option B target ({rng_b})."
    if on:
        return f"Meets the Option B target ({rng_b}) — hold the gain and shift to the next weakest metric."
    verb = "raise" if better == "up" else "reduce"
    return f"Off the Option B target ({rng_b}) — {verb} it next sprint to progress toward Option B."


def _kpi(scenario, metric_id, live, delta=None, delta_dir=None):
    m = METRICS_BY_ID[metric_id]
    val = _num(scenario, metric_id, live)
    display = m.get("display", {}).get(scenario)
    return {
        "id": metric_id, "label": m["name"], "value": val,
        "display": display if display is not None else _fmt(val, m["unit"]),
        "unit": m["unit"], "better": m["better"],
        "target": m["ranges"]["option-b"],   # Option B is the canonical "next" target
        "delta": delta, "delta_dir": delta_dir,
        "source": m["source"], "formula": m["formula"], "ranges": m["ranges"],
        "insight": _kpi_insight(metric_id, val),
    }


def _fmt(val, unit):
    if unit == "$":
        return f"${val:,.0f}" if val >= 100 else f"${val:,.2f}"
    if unit == "M":
        return f"{val}M"
    if unit == "×":
        return f"{val}×"
    if unit == "%":
        return f"{val}%"
    if unit in ("hrs", "days", "s", "/wk", "items", "SP/pd"):
        return f"{val} {unit}"
    return str(val)


def _scale_delta(scenario):
    """Illustrative sprint-over-sprint deltas get larger as adoption deepens."""
    return {"option-a": 1.0, "option-b": 1.6, "option-c": 2.2}[scenario]


def _ratio(scenario, metric_id, live):
    """Ratio of the effective (rolled-up/live) value to the scenario demo midpoint."""
    demo = METRICS_BY_ID[metric_id]["demo"][scenario]
    if not demo:
        return 1.0
    return _num(scenario, metric_id, live) / demo


def _scale_series(scenario, metric_id, live, values, pct=False):
    """Scale a demo phase/sprint series so it tracks the rolled-up headline value."""
    r = _ratio(scenario, metric_id, live)
    out = [v * r for v in values]
    return [min(round(x, 1), 99.0) for x in out] if pct else [round(x, 2) for x in out]


def _prod_overrides(live):
    """Map any live ALM/Finance signals to productivity-engine override keys."""
    keys = ("team_size", "sprint_days", "utilisation", "blended_daily_rate",
            "sp_rate", "sp_delivered", "cfr")
    ov = {k: live[k] for k in keys if live and k in live and live[k] is not None}
    # change_failure_rate arrives as a percentage; the engine wants a 0–1 fraction.
    if live and live.get("change_failure_rate") is not None and "cfr" not in ov:
        ov["cfr"] = live["change_failure_rate"] / 100.0
    return ov


# ── Perspective builders ──────────────────────────────────────────────────────
def _adoption(scenario, live):
    k = _scale_delta(scenario)
    kpis = [
        _kpi(scenario, "agent_utilisation", live, delta=f"+{round(8*k)}pt", delta_dir="up"),
        _kpi(scenario, "ai_acceptance", live, delta=f"+{round(5*k)}pt", delta_dir="up"),
        _kpi(scenario, "override_rate", live, delta=f"−{round(4*k)}pt", delta_dir="down"),
        _kpi(scenario, "agent_roi", live, delta=f"+{round(0.4*k,1)}×", delta_dir="up"),
    ]
    util = _scale_series(scenario, "agent_utilisation", live, UTIL_BY_PHASE[scenario], pct=True)
    accept = _scale_series(scenario, "ai_acceptance", live, ACCEPT_TREND[scenario], pct=True)
    roi = _scale_series(scenario, "agent_roi", live, ROI_TREND[scenario])
    # Human override rate — declining trend toward the current value.
    ovr_now = _num(scenario, "override_rate", live)
    ovr = [round(ovr_now * (1.6 - 0.12 * i), 1) for i in range(6)]
    ovr_target = METRICS_BY_ID["override_rate"]["demo"]["option-b"]
    util_target = METRICS_BY_ID["agent_utilisation"]["demo"]["option-b"]
    charts = [
        {"id": "util_by_phase", "type": "bar", "metric_id": "agent_utilisation",
         "title": "Agent Utilisation by PDLC Phase", "unit": "%",
         "subtitle": f"% activities AI-assisted · target {util_target}% (Option B)",
         "xKey": "phase", "target": {"value": util_target, "label": "Opt B target"},
         "series": [{"key": "value", "name": "Utilisation %", "color": SCEN_COLOR[scenario]}],
         "data": [{"phase": PHASE_SHORT[i], "value": util[i]} for i in range(7)]},
        {"id": "acceptance_trend", "type": "line", "metric_id": "ai_acceptance",
         "title": "AI Acceptance Rate — 6-sprint trend", "unit": "%",
         "subtitle": "Accepted AI suggestions ÷ total · target 85% by Option B",
         "xKey": "sprint", "target": {"value": 85, "label": "85% target"},
         "series": [{"key": "value", "name": "Acceptance %", "color": "#0ea5e9"}],
         "data": [{"sprint": SPRINTS[i], "value": accept[i]} for i in range(6)]},
        {"id": "roi_trend", "type": "area", "metric_id": "agent_roi",
         "title": "Agent ROI Multiple — 6-sprint trend", "unit": "×",
         "subtitle": f"$ value of time saved ÷ agent run cost. Now ≈ {roi[-1]}× "
                     f"(every $1 of agent spend returns ${roi[-1]:g} of capacity).",
         "xKey": "sprint", "yLabel": "ROI (× multiple)", "xLabel": "Sprint",
         "series": [{"key": "value", "name": "ROI ×", "color": "#f59e0b"}],
         "data": [{"sprint": SPRINTS[i], "value": roi[i]} for i in range(6)]},
        {"id": "override_trend", "type": "line", "metric_id": "override_rate",
         "title": "Human Override Rate — 6-sprint trend", "unit": "%",
         "subtitle": f"AI outputs reverted by humans (lower = more trust). "
                     f"Target < {ovr_target}% for Option B.",
         "xKey": "sprint", "target": {"value": ovr_target, "label": f"<{ovr_target}% target"},
         "series": [{"key": "value", "name": "Override %", "color": "#ef4444"}],
         "data": [{"sprint": SPRINTS[i], "value": ovr[i]} for i in range(6)]},
    ]
    lead_phase = PHASE_SHORT[util.index(max(util))]
    lag_phase = PHASE_SHORT[util.index(min(util))]
    facts = [
        f"Agent utilisation overall ≈ {_num(scenario,'agent_utilisation',live)}% "
        f"(target {util_target}% for Option B). {lead_phase} phase leads at {max(util)}%, "
        f"{lag_phase} lags at {min(util)}%.",
        f"AI acceptance rose {accept[0]}%→{accept[-1]}% over 6 sprints "
        f"(~{round((accept[-1]-accept[0])/5,1)} pts/sprint).",
        f"Human override rate at {_num(scenario,'override_rate',live)}% "
        f"(target {METRICS_BY_ID['override_rate']['ranges'][scenario]}).",
        f"Agent ROI at {_num(scenario,'agent_roi',live)}× and trending up.",
    ]
    return _perspective("adoption", scenario, kpis, charts, facts)


def _performance(scenario, live, prod_overrides=None, prod_inputs=None, platform="homegrown",
                 dora_overrides=None):
    k = _scale_delta(scenario)
    # Productivity economics — computed via the SP→Effort→Cost formula chain.
    # Manual UI overrides take precedence over live-derived signals (what-if).
    base_prod = prod_inputs if prod_inputs else _prod_overrides(live)
    prod_in = {**base_prod, **(prod_overrides or {})}
    prod = compute_productivity(scenario, prod_in)
    # DORA J-Curve value trend (cost-only, platform-aware ongoing cost incl. tokens).
    trend = compute_value_trend(scenario, prod_in, horizon_sprints=13, platform=platform,
                                dora=dora_overrides or {})
    # Inject formula-derived values so the KPIs reflect the real computation.
    perf_live = {**live,
                 "cost_per_sp": prod["results"]["cost_per_sp_usd"],
                 "productivity": prod["results"]["productivity_sp_per_pd"]}
    cost_drop_pct = round((1 - prod["results"]["cost_per_sp_usd"] /
                           prod["baseline"]["cost_per_sp_usd"]) * 100)
    prod_gain_pct = prod["results"]["productivity_index"] - 100
    kpis = [
        _kpi(scenario, "lead_time", live, delta=f"−{round(6*k)}%", delta_dir="down"),
        _kpi(scenario, "flow_efficiency", live, delta=f"+{round(4*k)}pt", delta_dir="up"),
        _kpi(scenario, "cost_per_sp", perf_live,
             delta=f"−{cost_drop_pct}%" if cost_drop_pct else "baseline", delta_dir="down"),
        _kpi(scenario, "productivity", perf_live,
             delta=f"+{prod_gain_pct}%" if prod_gain_pct else "baseline", delta_dir="up"),
        _kpi(scenario, "deploy_freq", live, delta="↑", delta_dir="up"),
        _kpi(scenario, "change_failure_rate", live, delta=f"−{round(2*k)}pt", delta_dir="down"),
    ]
    fe = _scale_series(scenario, "flow_efficiency", live, FLOW_EFF_BY_PHASE[scenario], pct=True)
    totals = _scale_series(scenario, "lead_time", live, PHASE_TOTAL_DAYS[scenario])
    lead_t = _scale_series(scenario, "lead_time", live, LEAD_TREND[scenario])
    cycle_t = _scale_series(scenario, "cycle_time", live, CYCLE_TREND[scenario])
    flow_data = []
    for i in range(7):
        proc = round(totals[i] * fe[i] / 100, 2)
        wait = round(totals[i] - proc, 2)
        flow_data.append({"phase": PHASE_SHORT[i], "process": proc, "wait": wait, "fe": fe[i]})
    dora_idx = {"option-a": 1, "option-b": 2, "option-c": 3}[scenario]
    # SP-delivered & effort trends ramping from the pre-AI baseline to the
    # computed current values (so "more SP, less effort/SP" is visible).
    sp_now = prod["inputs"]["sp_delivered"]
    base_sp = prod["baseline"]["sp_delivered"]
    sp_series = [round(base_sp + (sp_now - base_sp) * i / 5, 1) for i in range(6)]
    # Effort chart normalised to an EQUIVALENT fixed-output basket (baseline SP),
    # so it isolates the AI effect from rising volume:
    #   pre-AI line  = flat effort to deliver `base_sp` at the old SP-rate (0.625 d/SP)
    #   AI-enabled   = effort to deliver the SAME `base_sp` as the SP-rate improves
    # The widening gap = effort saved per equivalent release.
    BASELINE_RATE = 0.625
    cur_rate = prod["inputs"]["sp_rate"]
    rate_series = [round(BASELINE_RATE + (cur_rate - BASELINE_RATE) * i / 5, 4) for i in range(6)]
    eff_baseline = [round(base_sp * BASELINE_RATE, 1)] * 6
    eff_ai = [round(base_sp * r, 1) for r in rate_series]
    eff_saved_equiv = round(eff_baseline[0] - eff_ai[-1], 1)
    charts = [
        {"id": "flow_by_phase", "type": "stacked-bar", "metric_id": "flow_efficiency",
         "title": "Flow Efficiency by Phase — Process vs Wait", "unit": "days",
         "subtitle": "Process time (value-add) vs wait time per phase",
         "xKey": "phase",
         "series": [{"key": "process", "name": "Process (days)", "color": "#2563eb"},
                    {"key": "wait", "name": "Wait (days)", "color": "#cbd5e1"}],
         "data": flow_data},
        {"id": "lead_cycle_trend", "type": "line", "metric_id": "lead_time",
         "title": "Lead & Cycle Time — 6-sprint trend", "unit": "days",
         "subtitle": "Calendar days, lower is better",
         "xKey": "sprint",
         "series": [{"key": "lead", "name": "Lead time", "color": "#dc2626"},
                    {"key": "cycle", "name": "Cycle time", "color": "#f59e0b"}],
         "data": [{"sprint": SPRINTS[i], "lead": lead_t[i],
                   "cycle": cycle_t[i]} for i in range(6)]},
        {"id": "cost_per_sp_trend", "type": "line", "metric_id": "cost_per_sp",
         "title": "Cost per Story Point — 6-sprint trend", "unit": "$",
         "subtitle": f"Fully-loaded cost ÷ SP delivered · baseline ${prod['baseline']['cost_per_sp_usd']} → "
                     f"computed ${prod['results']['cost_per_sp_usd']:,.0f}",
         "xKey": "sprint", "target": {"value": 425, "label": "Opt B $425"},
         "series": [{"key": "value", "name": "Cost / SP", "color": "#059669"}],
         "data": ([{"sprint": SPRINTS[i], "value": COST_PER_SP_TREND[scenario][i]} for i in range(5)]
                  + [{"sprint": SPRINTS[5], "value": prod["results"]["cost_per_sp_usd"]}])},
        {"id": "sp_delivered_trend", "type": "area", "metric_id": "productivity",
         "title": "Story Points Delivered — 6-sprint trend", "unit": "SP",
         "subtitle": f"SP delivered rising {base_sp:g} → {sp_now:g} "
                     f"(+{prod['savings']['sp_uplift']:g} SP, {prod['savings']['sp_uplift_pct']}% more)",
         "xKey": "sprint", "target": {"value": base_sp, "label": "baseline"},
         "series": [{"key": "value", "name": "SP delivered", "color": "#0891b2"}],
         "data": [{"sprint": SPRINTS[i], "value": sp_series[i]} for i in range(6)]},
        {"id": "effort_trend", "type": "line", "metric_id": "cost_per_sp",
         "title": f"Effort to Deliver an Equivalent {base_sp:g}-SP Release (person-days)", "unit": "pd",
         "subtitle": f"Same output, without AI (flat) vs AI-enabled (falling). Gap ≈ "
                     f"{prod['savings']['effort_saved_pd']:g} pd saved "
                     f"= ${prod['savings']['cost_saved_usd']:,} = {prod['savings']['sp_gained']:g} SP of freed capacity "
                     f"({prod['savings']['effort_reduction_pct']}% less effort)",
         "xKey": "sprint", "yLabel": "Person-days", "xLabel": "Sprint",
         "series": [{"key": "baseline", "name": "Pre-AI (no assistance)", "color": "#94a3b8"},
                    {"key": "ai", "name": "AI-enabled", "color": "#7c3aed"}],
         "data": [{"sprint": SPRINTS[i], "baseline": eff_baseline[i], "ai": eff_ai[i]} for i in range(6)]},
        {"id": "dora_bands", "type": "dora", "metric_id": "deploy_freq",
         "title": "DORA Band Positioning", "unit": "",
         "subtitle": "Current state vs Option B & C targets",
         "current": dora_idx,
         "bands": [
             {"name": "Low", "desc": "LT > 6m · Monthly deploys"},
             {"name": "Medium", "desc": "LT 1w–6m · Weekly deploys"},
             {"name": "High", "desc": "LT 1d–1wk · Daily deploys"},
             {"name": "Elite", "desc": "LT < 1d · Multiple/day"},
         ],
         "markers": [{"at": 1, "label": "Opt A"}, {"at": 2, "label": "Opt B"}, {"at": 3, "label": "Opt C"}]},
        # DORA J-Curve (Figure 2): net savings per sprint — negative during the
        # learning/verification-tax dip, then growing sprint-on-sprint.
        {"id": "jcurve_net", "type": "bar", "metric_id": "cost_per_sp", "unit": "$",
         "title": "Net Saving per Sprint — DORA J-Curve (cost-only)",
         "subtitle": f"Investment + verification-tax dip first ({trend['jcurve_drop_pct']}% over "
                     f"{trend['jcurve_sprints']} sprints), then net savings grow. Ongoing cost incl. "
                     f"agent/token (${trend['ongoing_cost_breakdown']['token_agent_usd']:,}/sprint) on {platform}.",
         "xKey": "sprint", "yLabel": "Net $ / sprint", "xLabel": "Sprint",
         "series": [{"key": "net_saving", "name": "Net saving", "color": "#0ea5e9"}],
         "data": [{"sprint": s["sprint"], "net_saving": s["net_saving"]} for s in trend["series"]]},
        # Cumulative net benefit — the J-curve; crosses zero at breakeven.
        {"id": "jcurve_cumulative", "type": "line", "metric_id": "cost_per_sp", "unit": "$",
         "title": "Cumulative Net Benefit — Breakeven (J-Curve)",
         "subtitle": (f"Breakeven at sprint {trend['breakeven_sprint']} · ROI {trend['roi_pct']}% over "
                      f"{trend['horizon_sprints']} sprints"
                      if trend['breakeven_sprint'] else
                      f"No breakeven within {trend['horizon_sprints']} sprints at this scope — "
                      f"shared platform cost needs more pods/scale (ROI {trend['roi_pct']}%)"),
         "xKey": "sprint", "yLabel": "Cumulative $", "xLabel": "Sprint",
         "target": {"value": 0, "label": "breakeven"},
         "series": [{"key": "cumulative_net", "name": "Cumulative net", "color": "#059669"}],
         "data": [{"sprint": s["sprint"], "cumulative_net": s["cumulative_net"]} for s in trend["series"]]},
    ]
    worst = min(range(7), key=lambda i: fe[i])
    facts = [
        f"Lead time at {_num(scenario,'lead_time',live)} days, cycle time "
        f"{_num(scenario,'cycle_time',live)} days; both trending down over 6 sprints.",
        f"Overall flow efficiency ≈ {_num(scenario,'flow_efficiency',live)}%; "
        f"{PHASE_SHORT[worst]} phase is the weakest at {fe[worst]}% (highest wait).",
        f"Deployment frequency: {METRICS_BY_ID['deploy_freq']['display'][scenario]}; "
        f"DORA position = {['','Medium','High','Elite'][dora_idx]} band.",
        f"Change failure rate {_num(scenario,'change_failure_rate',live)}% and "
        f"MTTR {_num(scenario,'mttr',live)} hrs.",
        f"Productivity {prod['results']['productivity_sp_per_pd']} SP/person-day "
        f"(index {prod['results']['productivity_index']} vs pre-AI baseline of "
        f"{prod['baseline']['productivity_sp_per_pd']}). Quality-adjusted "
        f"{prod['results']['quality_adjusted_sp_per_pd']} SP/person-day after CFR.",
        f"Cost per story point ${prod['results']['cost_per_sp_usd']:,.0f} vs $500 baseline "
        f"(−${prod['savings']['saving_per_sp_usd']:,.0f}/SP). Reconciled saving to deliver the "
        f"pre-AI equivalent {prod['baseline']['sp_delivered']:g}-SP output: "
        f"{prod['savings']['effort_saved_pd']:g} person-days "
        f"= ${prod['savings']['cost_saved_usd']:,} = {prod['savings']['sp_gained']:g} SP of freed capacity.",
        f"Story points up +{prod['savings']['sp_uplift']:g} ({prod['savings']['sp_uplift_pct']}%) vs baseline; "
        f"effort reduced ≈ {prod['savings']['effort_saved_pd']:g} person-days/sprint "
        f"({prod['savings']['effort_reduction_pct']}% less effort for the same output).",
    ]
    facts.append(
        f"DORA J-Curve ({platform}): one-time investment ${trend['one_time_investment_usd']:,} + "
        f"ongoing ${trend['tool_cost_per_sprint_usd']:,}/sprint (token ${trend['ongoing_cost_breakdown']['token_agent_usd']:,} · "
        f"ops {trend['ongoing_cost_breakdown']['ops_fte']} FTE shared). "
        + (f"Breakeven sprint {trend['breakeven_sprint']}, ROI {trend['roi_pct']}% over {trend['horizon_sprints']} sprints (cost-only, excl. feature revenue)."
           if trend['breakeven_sprint'] else
           f"No breakeven in {trend['horizon_sprints']} sprints at this team scope (ROI {trend['roi_pct']}%) — home-grown/shared platform pays off at portfolio scale."))
    persp = _perspective("performance", scenario, kpis, charts, facts)
    persp["productivity"] = prod
    persp["value_trend"] = trend
    return persp


def _ai_ops(scenario, live, prod_overrides=None, prod_inputs=None):
    k = _scale_delta(scenario)
    # AI cost per SP = token cost ÷ SP delivered (derived, not hardcoded).
    base_prod = prod_inputs if prod_inputs else _prod_overrides(live)
    prod = compute_productivity(scenario, {**base_prod, **(prod_overrides or {})})
    token_cost_val = _num(scenario, "token_cost", live)
    sp_delivered = prod["inputs"]["sp_delivered"]
    ai_live = {**live, "ai_cost_per_sp": round(token_cost_val / sp_delivered, 1) if sp_delivered else 0}
    kpis = [
        _kpi(scenario, "token_cost", live, delta=f"+{round(8*k)}%", delta_dir="up"),
        _kpi(scenario, "agent_success", live, delta=f"+{round(1*k)}pt", delta_dir="up"),
        _kpi(scenario, "hallucination_rate", live, delta=f"−{round(1*k,1)}pt", delta_dir="down"),
        _kpi(scenario, "explainability", live, delta=f"+{round(3*k)}pt", delta_dir="up"),
    ]
    total_tokens = _num(scenario, "token_usage", live)
    weights = [0.10, 0.12, 0.28, 0.14, 0.18, 0.08, 0.10]   # token share per agent
    token_data = [{"agent": TOKEN_AGENTS[i], "tokens": round(total_tokens * weights[i], 2)}
                  for i in range(7)]
    radar_dims = [
        ("Success", _num(scenario, "agent_success", live)),
        ("Groundedness", _num(scenario, "rag_groundedness", live)),
        ("Fairness", _num(scenario, "fairness_pass", live)),
        ("Explainability", _num(scenario, "explainability", live)),
        ("Citations", _num(scenario, "citation_coverage", live)),
        ("Factuality", round(100 - _num(scenario, "hallucination_rate", live), 1)),
    ]
    gov = [
        ("Fairness Pass", _num(scenario, "fairness_pass", live)),
        ("Explainability", _num(scenario, "explainability", live)),
        ("Citation Cov.", _num(scenario, "citation_coverage", live)),
        ("Guardrail Comp.", _num(scenario, "guardrail_compliance", live)),
        ("RAG Grounded", _num(scenario, "rag_groundedness", live)),
    ]
    charts = [
        {"id": "token_by_agent", "type": "bar", "metric_id": "token_usage", "unit": "M",
         "title": "Token Usage by Agent", "subtitle": f"Tokens (M) per sprint · total ≈ {total_tokens}M",
         "xKey": "agent",
         "series": [{"key": "tokens", "name": "Tokens (M)", "color": "#6366f1"}],
         "data": token_data},
        {"id": "token_cost_trend", "type": "area", "metric_id": "token_cost", "unit": "$",
         "title": "Token Cost — 6-sprint trend", "subtitle": "AI platform spend per sprint",
         "xKey": "sprint",
         "series": [{"key": "value", "name": "Token cost $", "color": "#ec4899"}],
         "data": [{"sprint": SPRINTS[i], "value": v} for i, v in
                  enumerate(_scale_series(scenario, "token_cost", live, TOKEN_COST_TREND[scenario]))]},
        {"id": "agent_quality_radar", "type": "radar", "metric_id": "agent_success", "unit": "%",
         "title": "Agent Quality Profile", "subtitle": "Higher is better on all axes (0–100)",
         "xKey": "dim",
         "series": [{"key": "score", "name": SCEN_LABEL[scenario], "color": SCEN_COLOR[scenario]}],
         "data": [{"dim": d, "score": v} for d, v in radar_dims]},
        {"id": "governance_bar", "type": "bar", "metric_id": "guardrail_compliance", "unit": "%",
         "title": "Governance & Assurance Scores", "subtitle": "Bias/fairness/explainability guardrails",
         "xKey": "check", "target": {"value": 95, "label": "95% bar"},
         "series": [{"key": "score", "name": "Score %", "color": "#10b981"}],
         "data": [{"check": c, "score": v} for c, v in gov]},
    ]
    facts = [
        f"Token cost ≈ ${_num(scenario,'token_cost',live):,.0f}/sprint on ≈ {total_tokens}M tokens "
        f"over {sp_delivered} SP delivered; AI cost per SP ≈ ${_num(scenario,'ai_cost_per_sp',ai_live):,.0f}.",
        f"Agent success rate {_num(scenario,'agent_success',live)}%, latency "
        f"{_num(scenario,'agent_latency',live)}s; CodeGen is the largest token consumer.",
        f"Hallucination rate {_num(scenario,'hallucination_rate',live)}% with RAG groundedness "
        f"{_num(scenario,'rag_groundedness',live)}%.",
        f"Bias flag rate {_num(scenario,'bias_flag_rate',live)}%, fairness pass "
        f"{_num(scenario,'fairness_pass',live)}%, explainability {_num(scenario,'explainability',live)}%, "
        f"guardrail compliance {_num(scenario,'guardrail_compliance',live)}%.",
    ]
    return _perspective("ai_ops", scenario, kpis, charts, facts)


def _perspective(key, scenario, kpis, charts, facts):
    meta = PERSPECTIVES[key]
    return {
        "key": key, "label": meta["label"], "blurb": meta["blurb"], "icon": meta["icon"],
        "kpis": kpis, "charts": charts, "facts": facts, "inferences": [],
    }


def build_dashboard(scenario: str, live: dict | None = None, source_mode: str = "demo",
                    prod_overrides: dict | None = None, base: dict | None = None,
                    prod_inputs: dict | None = None, scope_meta: dict | None = None,
                    platform: str = "homegrown", dora_overrides: dict | None = None) -> dict:
    """
    Assemble the full dashboard payload for a scenario.

    `base`        — rolled-up per-scope metric values (from rollup.py). Used as the
                    demo source; real `live` values still take precedence.
    `prod_inputs` — rolled-up productivity inputs (summed SP/effort/cost) for the scope.
    """
    if scenario not in SCEN_LABEL:
        scenario = "option-a"
    live = live or {}
    # Effective value map: rolled-up base first, real live overrides on top.
    eff = {**(base or {}), **live}
    return {
        "scenario": scenario,
        "scenario_label": SCEN_LABEL[scenario],
        "scenario_color": SCEN_COLOR[scenario],
        "source_mode": source_mode,
        "scope": scope_meta or {},
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "platform": platform,
        "perspectives": {
            "adoption": _adoption(scenario, eff),
            "performance": _performance(scenario, eff, prod_overrides, prod_inputs, platform, dora_overrides),
            "ai_ops": _ai_ops(scenario, eff, prod_overrides, prod_inputs),
        },
        "progression_matrix": matrix_rows(),
    }
