"""
Outcome Dashboard — Metric Catalog & Demo Data Bands.

Source of truth for the three monitoring perspectives. The Option A→B→C
progression matrix (PERSPECTIVES + METRICS) is lifted directly from the STUMP
"Metrics & Measurement Framework" deck (slides 12–18). Perspective 3 (AI Ops &
Assurance) is not in the deck — it is designed here per requirements
(token usage, agent performance, bias, explainability, governance).

Each metric carries:
  - target ranges as displayed in the progression matrix (option_a/b/c strings)
  - a numeric demo midpoint per option (used when no live source is connected)
  - unit, better direction, formula text and measurement source

The engine consumes these to assemble the dashboard payload; live connector
values override the demo midpoints where available.
"""

SCENARIOS = ["option-a", "option-b", "option-c"]

# Short PDLC phase labels (mirrors backend/agents/pdlc_data.PDLC_PHASES order).
PHASES = ["Discovery", "Architecture", "Development", "Build",
          "Testing", "Deployment", "Operations"]
PHASE_SHORT = ["Disc", "Arch", "Dev", "Bld", "Test", "Dep", "Ops"]

PERSPECTIVES = {
    "adoption": {
        "label": "AI Adoption",
        "blurb": "How deeply agents & AI tooling are adopted across the PDLC",
        "icon": "Bot",
    },
    "performance": {
        "label": "PDLC Performance",
        "blurb": "Delivery outcomes — flow, speed, stability & productivity",
        "icon": "Gauge",
    },
    "ai_ops": {
        "label": "AI Ops & Assurance",
        "blurb": "Token economics, agent quality, bias, explainability & governance",
        "icon": "ShieldCheck",
    },
}

# better: 'up' = higher is better, 'down' = lower is better, 'track' = monitor only.
# demo: representative numeric value per option (midpoint of matrix range).
METRICS = [
    # ── Perspective 1 — AI Adoption ──────────────────────────────────────────
    {"id": "agent_utilisation", "name": "Agent Utilisation Rate", "perspective": "adoption",
     "unit": "%", "better": "up", "source": "Agent Logs / STUMP",
     "formula": "AI-assisted activities ÷ total activities",
     "ranges": {"option-a": "30–50%", "option-b": "60–75%", "option-c": "85–95%"},
     "demo": {"option-a": 48, "option-b": 68, "option-c": 90}},
    {"id": "ai_acceptance", "name": "AI Acceptance Rate", "perspective": "adoption",
     "unit": "%", "better": "up", "source": "GitHub / LLM API",
     "formula": "Accepted AI suggestions ÷ total AI suggestions",
     "ranges": {"option-a": "55–70%", "option-b": "70–85%", "option-c": "88–95%"},
     "demo": {"option-a": 72, "option-b": 82, "option-c": 92}},
    {"id": "override_rate", "name": "Human Override Rate", "perspective": "adoption",
     "unit": "%", "better": "down", "source": "STUMP / GitHub",
     "formula": "Human-reverted AI outputs ÷ AI outputs",
     "ranges": {"option-a": "< 35%", "option-b": "< 20%", "option-c": "< 10%"},
     "demo": {"option-a": 18, "option-b": 14, "option-c": 8}},
    {"id": "time_saved", "name": "Time Saved / Agent / Sprint", "perspective": "adoption",
     "unit": "hrs", "better": "up", "source": "Jira Worklogs",
     "formula": "Baseline effort − AI-assisted effort, per agent per sprint",
     "ranges": {"option-a": "2–8 hrs", "option-b": "8–20 hrs", "option-c": "20–40 hrs"},
     "demo": {"option-a": 5, "option-b": 14, "option-c": 30}},
    {"id": "agent_roi", "name": "Agent ROI Multiple", "perspective": "adoption",
     "unit": "×", "better": "up", "source": "Billing + HR Cost",
     "formula": "Value of time saved ÷ agent run cost",
     "ranges": {"option-a": "1.5–3×", "option-b": "3–4.5×", "option-c": "4.5–6×"},
     "demo": {"option-a": 2.2, "option-b": 3.8, "option-c": 5.2}},

    # ── Perspective 2 — PDLC Performance ─────────────────────────────────────
    {"id": "lead_time", "name": "Lead Time", "perspective": "performance",
     "unit": "days", "better": "down", "source": "Jira + CI/CD",
     "formula": "AVG(prod deploy date − work start date)",
     "ranges": {"option-a": "21–28 days", "option-b": "10–14 days", "option-c": "3–7 days"},
     "demo": {"option-a": 24, "option-b": 12, "option-c": 5}},
    {"id": "cycle_time", "name": "Cycle Time", "perspective": "performance",
     "unit": "days", "better": "down", "source": "GitHub PRs",
     "formula": "AVG(merge date − first-commit date)",
     "ranges": {"option-a": "7–14 days", "option-b": "3–7 days", "option-c": "< 2 days"},
     "demo": {"option-a": 10, "option-b": 5, "option-c": 1.8}},
    {"id": "flow_efficiency", "name": "Flow Efficiency", "perspective": "performance",
     "unit": "%", "better": "up", "source": "VSM Analyzer",
     "formula": "Process time ÷ (process time + wait time)",
     "ranges": {"option-a": "18–28%", "option-b": "32–45%", "option-c": "50–65%"},
     "demo": {"option-a": 24, "option-b": 38, "option-c": 57}},
    {"id": "wip", "name": "Work In Progress", "perspective": "performance",
     "unit": "items", "better": "down", "source": "Jira Board",
     "formula": "Items in active states (rolling avg)",
     "ranges": {"option-a": "≤ 2× team", "option-b": "≤ 1.5× team", "option-c": "≤ 1× team"},
     "demo": {"option-a": 14, "option-b": 10, "option-c": 7}},
    {"id": "deploy_freq", "name": "Deployment Frequency", "perspective": "performance",
     "unit": "/wk", "better": "up", "source": "CI/CD Pipeline",
     "formula": "Successful production deployments per week",
     "ranges": {"option-a": "Weekly", "option-b": "Daily", "option-c": "Multiple / day"},
     "demo": {"option-a": 1, "option-b": 5, "option-c": 20},
     "display": {"option-a": "Weekly", "option-b": "Daily", "option-c": "Multiple/day"}},
    {"id": "change_failure_rate", "name": "Change Failure Rate", "perspective": "performance",
     "unit": "%", "better": "down", "source": "CI/CD + Incidents",
     "formula": "Failed deployments ÷ total deployments",
     "ranges": {"option-a": "< 15%", "option-b": "< 8%", "option-c": "< 5%"},
     "demo": {"option-a": 12, "option-b": 7, "option-c": 4}},
    {"id": "mttr", "name": "MTTR", "perspective": "performance",
     "unit": "hrs", "better": "down", "source": "ServiceNow / PagerDuty",
     "formula": "AVG(incident resolved − incident raised)",
     "ranges": {"option-a": "< 4 hours", "option-b": "< 2 hours", "option-c": "< 1 hour"},
     "demo": {"option-a": 3.5, "option-b": 1.5, "option-c": 0.7}},
    {"id": "cost_per_sp", "name": "Cost per Story Point", "perspective": "performance",
     "unit": "$", "better": "down", "source": "Jira + Finance/HR",
     "formula": "Total cost ÷ story points delivered (vs $500 pre-AI baseline)",
     "ranges": {"option-a": "~$472", "option-b": "~$425", "option-c": "~$360"},
     "demo": {"option-a": 472, "option-b": 425, "option-c": 360}},
    {"id": "productivity", "name": "Productivity (SP/person-day)", "perspective": "performance",
     "unit": "SP/pd", "better": "up", "source": "Jira + Capacity",
     "formula": "SP delivered ÷ capacity; index vs pre-AI baseline",
     "ranges": {"option-a": "~+6%", "option-b": "~+18%", "option-c": "~+39%"},
     "demo": {"option-a": 1.33, "option-b": 1.49, "option-c": 1.74}},

    # ── Perspective 3 — AI Ops & Assurance (designed, not in deck) ───────────
    {"id": "token_cost", "name": "Token Cost / Sprint", "perspective": "ai_ops",
     "unit": "$", "better": "track", "source": "AI Platform Billing",
     "formula": "Σ(tokens × unit price) across all agents per sprint",
     "ranges": {"option-a": "~$1.6k", "option-b": "~$4.4k", "option-c": "~$9.0k"},
     "demo": {"option-a": 1600, "option-b": 4400, "option-c": 9000}},
    {"id": "token_usage", "name": "Tokens / Sprint", "perspective": "ai_ops",
     "unit": "M", "better": "track", "source": "AI Platform API",
     "formula": "Σ input+output tokens across agents per sprint",
     "ranges": {"option-a": "~8M", "option-b": "~22M", "option-c": "~55M"},
     "demo": {"option-a": 8, "option-b": 22, "option-c": 55}},
    {"id": "ai_cost_per_sp", "name": "AI Cost / Story Point", "perspective": "ai_ops",
     "unit": "$", "better": "track", "source": "AI Billing + Jira",
     "formula": "Token cost ÷ story points delivered",
     "ranges": {"option-a": "~$40", "option-b": "~$70", "option-c": "~$95"},
     "demo": {"option-a": 40, "option-b": 70, "option-c": 95}},
    {"id": "agent_latency", "name": "Avg Agent Latency", "perspective": "ai_ops",
     "unit": "s", "better": "down", "source": "Agent Framework",
     "formula": "AVG(agent task completion time)",
     "ranges": {"option-a": "~4.5s", "option-b": "~3.2s", "option-c": "~2.1s"},
     "demo": {"option-a": 4.5, "option-b": 3.2, "option-c": 2.1}},
    {"id": "agent_success", "name": "Agent Success Rate", "perspective": "ai_ops",
     "unit": "%", "better": "up", "source": "Agent Framework",
     "formula": "Successful agent runs ÷ total runs",
     "ranges": {"option-a": "~88%", "option-b": "~93%", "option-c": "~97%"},
     "demo": {"option-a": 88, "option-b": 93, "option-c": 97}},
    {"id": "hallucination_rate", "name": "Hallucination Rate", "perspective": "ai_ops",
     "unit": "%", "better": "down", "source": "Accuracy / RAG Eval",
     "formula": "Ungrounded outputs ÷ evaluated outputs",
     "ranges": {"option-a": "~6%", "option-b": "~3%", "option-c": "~1.5%"},
     "demo": {"option-a": 6, "option-b": 3, "option-c": 1.5}},
    {"id": "rag_groundedness", "name": "RAG Groundedness", "perspective": "ai_ops",
     "unit": "%", "better": "up", "source": "Accuracy Scorer",
     "formula": "Citations supported by source ÷ claims",
     "ranges": {"option-a": "~82%", "option-b": "~89%", "option-c": "~95%"},
     "demo": {"option-a": 82, "option-b": 89, "option-c": 95}},
    {"id": "bias_flag_rate", "name": "Bias Flag Rate", "perspective": "ai_ops",
     "unit": "%", "better": "down", "source": "Governance Guardrails",
     "formula": "Outputs flagged for bias ÷ outputs screened",
     "ranges": {"option-a": "~4%", "option-b": "~2.5%", "option-c": "~1.2%"},
     "demo": {"option-a": 4, "option-b": 2.5, "option-c": 1.2}},
    {"id": "fairness_pass", "name": "Fairness Pass Rate", "perspective": "ai_ops",
     "unit": "%", "better": "up", "source": "Governance Guardrails",
     "formula": "Outputs passing fairness checks ÷ screened",
     "ranges": {"option-a": "~92%", "option-b": "~96%", "option-c": "~98.5%"},
     "demo": {"option-a": 92, "option-b": 96, "option-c": 98.5}},
    {"id": "explainability", "name": "Explainability Score", "perspective": "ai_ops",
     "unit": "%", "better": "up", "source": "Governance / XAI",
     "formula": "Decisions with traceable rationale ÷ decisions",
     "ranges": {"option-a": "~70%", "option-b": "~82%", "option-c": "~91%"},
     "demo": {"option-a": 70, "option-b": 82, "option-c": 91}},
    {"id": "citation_coverage", "name": "Citation Coverage", "perspective": "ai_ops",
     "unit": "%", "better": "up", "source": "RAG Pipeline",
     "formula": "AI outputs carrying source citations ÷ outputs",
     "ranges": {"option-a": "~75%", "option-b": "~88%", "option-c": "~96%"},
     "demo": {"option-a": 75, "option-b": 88, "option-c": 96}},
    {"id": "guardrail_compliance", "name": "Guardrail Compliance", "perspective": "ai_ops",
     "unit": "%", "better": "up", "source": "Governance Engine",
     "formula": "Runs passing all guardrails ÷ runs",
     "ranges": {"option-a": "~90%", "option-b": "~95%", "option-c": "~99%"},
     "demo": {"option-a": 90, "option-b": 95, "option-c": 99}},
]

METRICS_BY_ID = {m["id"]: m for m in METRICS}

# Source types selectable when configuring a data source, grouped by perspective.
SOURCE_TYPES = {
    "adoption":    [("jira", "Jira (worklogs / boards)"), ("github", "GitHub (Copilot / PRs)"),
                    ("ai_platform", "AI Platform API"), ("custom", "Custom URL")],
    "performance": [("jira", "Jira (issues / cycle)"), ("github", "GitHub PRs"),
                    ("ci_cd", "CI/CD Pipeline"), ("servicenow", "ServiceNow / PagerDuty"),
                    ("confluence", "Confluence (runbooks)"), ("custom", "Custom URL")],
    "ai_ops":      [("ai_platform", "AI Platform Billing/Telemetry"),
                    ("agent_framework", "Agent Framework (LangGraph)"),
                    ("github", "GitHub (eval logs)"), ("custom", "Custom URL")],
}


def matrix_rows():
    """Return the Option A→B→C progression matrix rows for display."""
    out = []
    for m in METRICS:
        out.append({
            "id": m["id"],
            "metric": m["name"],
            "perspective": m["perspective"],
            "perspective_label": PERSPECTIVES[m["perspective"]]["label"],
            "option_a": m["ranges"]["option-a"],
            "option_b": m["ranges"]["option-b"],
            "option_c": m["ranges"]["option-c"],
            "source": m["source"],
            "formula": m["formula"],
            "unit": m["unit"],
        })
    return out
