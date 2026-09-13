"""
Shared 2026 model for the PDLC VSM consulting GTM pack.

Single source of truth for the refreshed narrative so all 35 documents stay
consistent. Pure data/text (no pptx/docx rendering) — each build script imports
these and renders with its own helpers.

Refresh themes (aligned to the platform's recent enhancements):
  • L1–L5 interim maturity ladder (prompting → orchestration), with the legacy
    Options A/B/C mapped onto it.
  • Target State Studio: define North-Star/target + delivery PLATFORM, then an
    auto-generated interim roadmap to get there.
  • DORA-aligned J-Curve ROI (cost-only): investment → tuition-cost dip →
    breakeven → savings that grow sprint-on-sprint. Platform-aware ongoing cost
    INCLUDING agent/token spend. Excludes feature-revenue/business-growth.
  • Outcome Dashboard with three monitoring perspectives.
  • Productivity economics: Story Points → Effort → Cost (USD).
"""

# ── L1–L5 interim maturity ladder (prompting → orchestration) ────────────────
# Each level maps to the legacy Option A/B/C framing so the decks stay recognisable.
LADDER = [
    {"level": "L1", "name": "Assisted Prompting", "ml": "ML1 · Foundation",
     "summary": "AI via simple prompting in a few phases (mainly Dev & Test). Humans do the work; AI suggests.",
     "agent_role": "none", "hitl": "all outputs", "automation": "~20%", "option": "pre-Option A"},
    {"level": "L2", "name": "Agent Co-pilots (assistive)", "ml": "ML2 · Augmentation",
     "summary": "Assistive/companion agents across most phases; every output human-reviewed. Agents draft, humans approve.",
     "agent_role": "assistant", "hitl": "all outputs", "automation": "~40%", "option": "Option A — Human in the Loop"},
    {"level": "L3", "name": "Supervised Independent Agents", "ml": "ML3 · Automation",
     "summary": "Agents act independently on standard cases and interact; humans review exceptions and quality gates.",
     "agent_role": "independent", "hitl": "exceptions", "automation": "~62%", "option": "Option B (lower) — Human on the Loop"},
    {"level": "L4", "name": "Orchestrated Agents (oversight)", "ml": "ML4 · Transformation",
     "summary": "Most phases agent-run with multi-agent orchestration end-to-end; humans govern and handle escalations.",
     "agent_role": "orchestrated", "hitl": "gates", "automation": "~78%", "option": "Option B (upper) — Human on the Loop"},
    {"level": "L5", "name": "Autonomous ADLC (North Star)", "ml": "ML5 · Reinvention",
     "summary": "Fully orchestrated agents across the SDLC/PDLC. Only humans: Product Definer, Product Builder, Architect (incl. risk).",
     "agent_role": "orchestrated", "hitl": "strategic", "automation": "~90%", "option": "Option C — Human Above the Loop"},
]

OPTION_TO_LEVEL = {
    "A": "L2 (Agent Co-pilots, assistive)",
    "B": "L3–L4 (Supervised Independent → Orchestrated)",
    "C": "L5 (Autonomous ADLC — North Star)",
}

# ── Target-state delivery platforms (the configurator choice) ────────────────
PLATFORMS = [
    {"id": "homegrown", "name": "Home-grown / Custom Build", "kind": "Home-grown",
     "note": "US Bank target baseline — full control, no vendor lock-in; build agents in-house (LangGraph + Azure OpenAI).",
     "pros": "Max control & best unit economics at scale; no lock-in",
     "cons": "Largest in-house platform team; slowest to value; scarce LLMOps talent",
     "ongoing": "No licence; high agent/token spend + platform-engineering team (shared across pods)"},
    {"id": "bmad", "name": "BMAD Method", "kind": "COTS",
     "note": "Open-source agentic methodology — bring your own LLM, lowest licence cost.",
     "pros": "No licence; LLM-agnostic; pre-curated agent patterns",
     "cons": "Framework only; smaller community; compliance evidence not bundled",
     "ongoing": "No licence; token spend + small ops pod"},
    {"id": "copilot_workspace", "name": "GitHub Copilot Workspace", "kind": "COTS",
     "note": "Vendor-managed agentic workspace inside the IDE/GitHub flow — fastest setup.",
     "pros": "Lowest internal capability needed; frontier models bundled",
     "cons": "Per-seat cost scales; data exposure review; weaker on non-dev phases",
     "ongoing": "Per-seat licence + token spend"},
    {"id": "devin", "name": "Devin (Cognition)", "kind": "COTS",
     "note": "Autonomous SWE agent — assign tickets; plans, codes, tests, opens PRs.",
     "pros": "Fastest dev-phase autonomy; parallel sessions scale throughput",
     "cons": "Dev/test-skewed; needs supervision on ambiguous work; per-seat cost",
     "ongoing": "Per-seat/session licence + token spend + small ops pod"},
    {"id": "cursor", "name": "Cursor (Anysphere)", "kind": "COTS",
     "note": "AI-native IDE + background agents — high developer adoption.",
     "pros": "Highest dev adoption; strong multi-file edits; low switching cost",
     "cons": "Assistive by default; limited non-dev coverage; per-seat cost",
     "ongoing": "Per-seat licence + token spend"},
    {"id": "flowsource", "name": "Cognizant Flowsource", "kind": "Service provider",
     "note": "AI-led SDLC platform — pre-integrated toolchain, accelerators and managed delivery agents.",
     "pros": "Fastest broad coverage; managed delivery; built-in governance",
     "cons": "Highest partner dependency; customisation within guardrails; recurring fee",
     "ongoing": "Managed platform + services fee + token spend (smaller in-house team)"},
]

# ── DORA-aligned J-Curve ROI (cost-only) ─────────────────────────────────────
# Ref: DORA "ROI of AI-assisted Software Development" (2026) — Fig 2 (J-Curve),
# Fig 5 (value model). We deliberately EXCLUDE feature-revenue/business-growth.
JCURVE = {
    "headline": "Investment first, a J-Curve dip, then net savings that grow sprint-on-sprint and cross breakeven.",
    "phases": [
        ("Investment", "Hard costs up front: licences + agent/token usage + enablement/training + AI infrastructure."),
        ("J-Curve dip (tuition cost)", "Early sprints carry a productivity dip — the learning curve + verification tax (reviewing AI output) — so net savings start negative."),
        ("Breakeven", "As adoption ramps and the dip fades, net savings turn positive and cumulative benefit crosses zero."),
        ("Compounding savings", "Net savings grow sprint-on-sprint; freed capacity is reinvested (cost avoided), not headcount cut."),
    ],
    "investment_formula": "Hard cost = (licence + agent/token usage + training + infra) × staff;  J-Curve cost = staff × salary × productivity-drop% × duration",
    "roi_formula": "ROI % = (Value − Investment) ÷ Investment   —   Value = cost-avoidance (freed capacity), NOT new-feature revenue",
    "ongoing_note": "Ongoing cost is PLATFORM-AWARE and INCLUDES agent/token spend: home-grown = token + platform-eng team; COTS = per-seat licence + token; service-provider = managed fee + token. Shared platform costs are prorated across pods.",
    "dora_defaults": "DORA sample levers (override per engagement): J-Curve drop 15% over 3 months; AI licence ~$250/user/yr; token/usage variable; training; infra.",
    "exclusion": "Business growth from new features is intentionally excluded — value is engineering cost-efficiency and capacity reinvestment only.",
}

# ── Outcome Dashboard — three monitoring perspectives ────────────────────────
OUTCOME_PERSPECTIVES = [
    {"key": "adoption", "name": "AI Adoption",
     "blurb": "How deeply agents/tools are adopted across the PDLC.",
     "metrics": ["Agent Utilisation Rate", "AI Acceptance Rate", "Human Override Rate", "Time Saved / Agent / Sprint", "Agent ROI Multiple"]},
    {"key": "performance", "name": "PDLC Performance (Outcomes)",
     "blurb": "Delivery outcomes — flow, speed, stability & productivity.",
     "metrics": ["Lead Time", "Cycle Time", "Flow Efficiency", "Deployment Frequency", "Change Failure Rate", "MTTR", "Cost per Story Point", "Productivity (SP/person-day)"]},
    {"key": "ai_ops", "name": "AI Ops & Assurance",
     "blurb": "Token economics, agent quality, bias, explainability & governance.",
     "metrics": ["Token Usage & Cost / Sprint", "AI Cost / Story Point", "Agent Success Rate", "Hallucination Rate", "RAG Groundedness", "Bias / Fairness", "Explainability", "Guardrail Compliance"]},
]
OUTCOME_SOURCES = "Real-time data sources: Jira / ADO, GitHub, CI/CD, ServiceNow/PagerDuty, AI-platform billing & agent-framework telemetry — zero manual entry; metrics computed via documented formulas with per-chart inference & action points."

# ── Productivity economics: Story Points → Effort → Cost ─────────────────────
PRODUCTIVITY = {
    "chain": "Story Points → Effort (person-days) → Cost (USD) → Unit economics",
    "formulas": [
        "Effort = SP delivered × SP-rate (days/SP)",
        "Cost = Effort × blended daily rate",
        "Cost per SP = SP-rate × blended daily rate",
        "Productivity = SP delivered ÷ capacity (SP/person-day)",
        "Saving (one figure, three units): effort-saved (pd) = cost-saved ($) = SP freed",
    ],
    "note": "Baseline (pre-AI) is derived from the same effort/budget at the pre-AI SP-rate, so SP-uplift %, productivity index and cost/SP reduction all move together. Inputs are editable (team, sprint days, utilisation, blended rate, SP-rate, CFR) and auto-pull from Jira/ADO + Finance once connected.",
}

# ── Three-phase engagement (kept; Design/Deliver modernised) ─────────────────
PHASES_2026 = [
    ("PHASE 1 · DIAGNOSE", "Current-state VSM + AI-quantified metrics; auto-derived current maturity level (L0–Lx); top-5 bottlenecks; sector benchmark.",
     "2–4 wks"),
    ("PHASE 2 · DESIGN", "Target State Studio: pick the North-Star level + delivery platform; auto-generate the L1–L5 interim roadmap; DORA J-Curve business case per interim step.",
     "2–3 wks"),
    ("PHASE 3 · DELIVER", "Execute interim steps; operating model + agents/tools per step; continuous measurement on the 3-perspective Outcome Dashboard; progress vs interim/target.",
     "ongoing"),
]

PLATFORM_ACCEL = "STUMP makes the offering faster and AI-accurate: minutes-not-months diagnosis, Target State Studio configurator, DORA J-Curve business case, and an always-on 3-perspective Outcome Dashboard — turning a one-off project into a live operating capability."

# US Bank reference (kept; reframed via the J-curve where used)
USBANK = {
    "team": "US Bank — Team Phoenix (Financial Services)",
    "lead_time": "42 → 8 days", "flow_eff": "17.8% → 61%",
    "target": "L4–L5 (home-grown ADLC)", "platform": "Home-grown",
    "note": "Outcomes shown on the J-Curve basis: investment + tuition-cost dip, breakeven, then compounding cost-avoidance — measured continuously on the Outcome Dashboard.",
}
