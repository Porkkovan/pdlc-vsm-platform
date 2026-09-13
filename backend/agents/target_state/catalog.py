"""
Target State Studio — interim maturity ladder (L1–L5).

Encodes the customer's prompting→orchestration ladder for going from the current
(pre-AI) state to the North-Star / target ADLC state, with the AI-CoE-Tower
ML0–ML5 (Foundation→Reinvention) bands shown alongside each level. Each level
maps to an Outcome-Dashboard scenario so metric bands & progress reconcile with
the rest of the platform.
"""

PDLC_PHASES = ["Discovery", "Feature Definition", "Architecture",
               "Development", "Testing", "DevSecOps", "AIOps & Monitoring"]

# agent_role: none | assistant | independent | orchestrated
# hitl (human-in-the-loop): all | exceptions | gates | strategic
# outcome_scenario maps the level to the Outcome Dashboard A/B/C bands.
INTERIM_LADDER = [
    {
        "level": 1, "id": "l1", "label": "Assisted Prompting",
        "ml_band": "ML1 — Foundation",
        "summary": "Teams use AI via simple prompting in a few high-value phases (mainly Development & Testing). "
                   "Humans do the work; AI suggests. No autonomous agents yet.",
        "agent_role": "none", "hitl": "all", "automation_pct": 20,
        "phase_coverage": ["Development", "Testing"],
        "human_roles_retained": ["Product Owner", "Business Analyst", "Architect", "Developers",
                                 "QA Engineers", "Scrum Master", "DevOps", "L3 Support"],
        "outcome_scenario": "option-a",
    },
    {
        "level": 2, "id": "l2", "label": "Agent Co-pilots (assistive)",
        "ml_band": "ML2 — Augmentation",
        "summary": "Assistive/companion agents across most phases. Every agent output is reviewed by a human "
                   "(human-in-the-loop on all). Agents draft; humans approve.",
        "agent_role": "assistant", "hitl": "all", "automation_pct": 40,
        "phase_coverage": ["Discovery", "Feature Definition", "Architecture", "Development", "Testing"],
        "human_roles_retained": ["Product Owner", "Business Analyst", "Architect", "Developers",
                                 "QA Lead", "Scrum Master", "DevOps"],
        "outcome_scenario": "option-a",
    },
    {
        "level": 3, "id": "l3", "label": "Supervised Independent Agents",
        "ml_band": "ML3 — Automation",
        "summary": "More agents act independently on standard cases and interact with each other; humans review "
                   "exceptions and quality gates. First multi-agent hand-offs appear.",
        "agent_role": "independent", "hitl": "exceptions", "automation_pct": 62,
        "phase_coverage": ["Discovery", "Feature Definition", "Architecture", "Development", "Testing", "DevSecOps"],
        "human_roles_retained": ["Product Owner", "Architect (incl. risk)", "Tech Lead", "QA Lead", "Compliance"],
        "outcome_scenario": "option-b",
    },
    {
        "level": 4, "id": "l4", "label": "Orchestrated Agents (oversight)",
        "ml_band": "ML4 — Transformation",
        "summary": "Most phases are agent-run with multi-agent orchestration end-to-end; humans provide oversight, "
                   "handle escalations and govern. Agents coordinate hand-offs autonomously.",
        "agent_role": "orchestrated", "hitl": "gates", "automation_pct": 78,
        "phase_coverage": PDLC_PHASES,
        "human_roles_retained": ["Product Definer", "Product Builder", "Architect (incl. risk)", "AI Governance"],
        "outcome_scenario": "option-c",
    },
    {
        "level": 5, "id": "l5", "label": "Autonomous ADLC (North Star)",
        "ml_band": "ML5 — Reinvention",
        "summary": "Fully orchestrated agents across the whole SDLC/PDLC with autonomous interaction. The only human "
                   "roles are Product Definer, Product Builder, and Architect (including risk).",
        "agent_role": "orchestrated", "hitl": "strategic", "automation_pct": 90,
        "phase_coverage": PDLC_PHASES,
        "human_roles_retained": ["Product Definer", "Product Builder", "Architect (incl. risk)"],
        "outcome_scenario": "option-c",
    },
]

LADDER_BY_LEVEL = {l["level"]: l for l in INTERIM_LADDER}
MAX_LEVEL = 5

RISK_APPETITE = [
    {"id": "low", "label": "Low (regulated, cautious)", "score": 0},
    {"id": "medium", "label": "Medium (balanced)", "score": 1},
    {"id": "high", "label": "High (fast mover)", "score": 2},
]
RISK_SCORE = {r["id"]: r["score"] for r in RISK_APPETITE}

# DevOps maturity band → readiness score (from devops_maturity_questions MATURITY_BANDS).
MATURITY_SCORE = {"PRE_CRAWL": 0, "CRAWL": 1, "WALK": 2, "RUN": 3, "FLY": 4}


def ladder() -> list[dict]:
    return INTERIM_LADDER
