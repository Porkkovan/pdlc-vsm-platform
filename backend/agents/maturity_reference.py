"""
Maturity Reference Model — L1-L5 definitions across People, Process, Tools/Technology,
Automation Level, and Outcomes. Used by agents for automated maturity assessment.
"""

MATURITY_REFERENCE = {
    1: {
        "level": 1,
        "label": "Initial / Ad-hoc",
        "summary": "Processes are informal and reactive. Limited tooling. Success depends on individual heroes.",
        "people": {
            "description": "Siloed roles; hero culture; limited cross-functional collaboration",
            "indicators": ["No dedicated DevOps/SRE roles", "Knowledge concentrated in individuals", "Manual handoffs between teams", "Limited training or upskilling programs"],
            "human_pct": 95, "digital_pct": 5,
        },
        "process": {
            "description": "Ad-hoc processes; no standard SDLC cadence; reactive firefighting",
            "indicators": ["No formal sprint/iteration cadence", "Requirements captured informally", "No defined Definition of Done", "Change management is ad-hoc"],
        },
        "tools": {
            "description": "Basic tools with minimal integration; mostly manual workflows",
            "indicators": ["Basic issue tracker (or spreadsheets)", "Manual builds and deployments", "No CI/CD pipeline", "Limited or no automated testing"],
        },
        "automation": {
            "description": "Almost entirely manual processes",
            "level": "Manual",
            "automation_pct": 5,
            "ai_involvement": "None",
        },
        "outcomes": {
            "deploy_frequency": "Monthly or less",
            "lead_time": "> 30 days",
            "change_failure_rate": "> 30%",
            "mttr": "> 24 hours",
            "flow_efficiency": "< 10%",
        },
    },
    2: {
        "level": 2,
        "label": "Managed / Repeatable",
        "summary": "Basic processes established. Some automation. Teams follow defined workflows.",
        "people": {
            "description": "Defined roles; some cross-functional collaboration; beginning of DevOps culture",
            "indicators": ["Defined team roles (PO, SM, Dev, QA)", "Some pair programming or mob programming", "Regular retrospectives", "Basic training programs"],
            "human_pct": 80, "digital_pct": 20,
        },
        "process": {
            "description": "Standard sprint cadence; basic Agile practices; documented workflows",
            "indicators": ["Regular sprint/iteration cycles", "Backlog refinement sessions", "Basic Definition of Done", "Standard code review process"],
        },
        "tools": {
            "description": "Integrated toolchain; basic CI pipeline; some automated testing",
            "indicators": ["Jira/ADO for work management", "Basic CI pipeline (build + unit tests)", "Source control with branching strategy", "Some automated test suites"],
        },
        "automation": {
            "description": "Basic automation of build and simple tests",
            "level": "Basic Automation",
            "automation_pct": 25,
            "ai_involvement": "None or minimal (simple linting)",
        },
        "outcomes": {
            "deploy_frequency": "Bi-weekly to monthly",
            "lead_time": "15-30 days",
            "change_failure_rate": "20-30%",
            "mttr": "12-24 hours",
            "flow_efficiency": "10-20%",
        },
    },
    3: {
        "level": 3,
        "label": "Defined / AI-Assisted",
        "summary": "Standardised processes across teams. AI tools assist developers. Shift-left practices adopted.",
        "people": {
            "description": "Cross-functional product teams; DevOps culture established; AI-assisted workflows",
            "indicators": ["Product-oriented team structure", "DevOps/Platform engineering roles", "AI code assistants used by most developers", "Regular knowledge sharing"],
            "human_pct": 60, "digital_pct": 40,
        },
        "process": {
            "description": "Standardised SDLC; shift-left testing; trunk-based development",
            "indicators": ["Trunk-based development or short-lived branches", "Shift-left testing strategy", "Automated release processes", "Data-driven decisions using metrics"],
        },
        "tools": {
            "description": "Full CI/CD pipeline; AI code assistants; automated quality gates",
            "indicators": ["Full CI/CD with automated deployments", "AI coding assistants (Copilot/similar)", "Automated SAST/DAST scanning", "Feature flags for controlled rollouts"],
        },
        "automation": {
            "description": "AI assists in code, test, and review; humans decide",
            "level": "AI-Assisted",
            "automation_pct": 45,
            "ai_involvement": "Co-pilot: AI suggests, human decides and acts",
        },
        "outcomes": {
            "deploy_frequency": "Weekly to bi-weekly",
            "lead_time": "5-15 days",
            "change_failure_rate": "10-20%",
            "mttr": "4-12 hours",
            "flow_efficiency": "20-35%",
        },
    },
    4: {
        "level": 4,
        "label": "Orchestrated / AI-First",
        "summary": "Multi-agent orchestration. AI drives most SDLC activities. Humans govern and handle exceptions.",
        "people": {
            "description": "Product Definers + Product Builders; AI handles routine work; humans focus on strategy",
            "indicators": ["Roles evolve: PO->Product Definer, Dev->Product Builder", "Team sizes reduce as AI handles routine tasks", "Humans focus on architecture, strategy, edge cases", "AI Governance roles established"],
            "human_pct": 35, "digital_pct": 65,
        },
        "process": {
            "description": "Continuous flow (no sprints); AI-driven planning; exception-based human review",
            "indicators": ["Continuous flow replaces sprint boundaries", "AI drafts stories, designs, and test plans", "Human review at quality gates only", "Automated compliance and security checks"],
        },
        "tools": {
            "description": "Multi-agent platform; orchestrated AI agents; self-healing pipelines",
            "indicators": ["Multi-agent orchestration platform", "AI agents for each PDLC phase", "Self-healing CI/CD pipelines", "Automated performance optimization"],
        },
        "automation": {
            "description": "AI-first: agents act independently; humans review exceptions",
            "level": "AI-First / Agentic",
            "automation_pct": 75,
            "ai_involvement": "Independent agents with human oversight at gates",
        },
        "outcomes": {
            "deploy_frequency": "Daily to on-demand",
            "lead_time": "1-5 days",
            "change_failure_rate": "5-10%",
            "mttr": "< 4 hours",
            "flow_efficiency": "35-55%",
        },
    },
    5: {
        "level": 5,
        "label": "Autonomous / AI-Native",
        "summary": "Fully autonomous ADLC. Self-optimising agents across all phases. Humans define intent and govern.",
        "people": {
            "description": "Minimal human roles: Product Definer (intent), Product Builder (architecture), AI Governance",
            "indicators": ["3 core roles: Product Definer, Product Builder, Architect", "Humans define 'what' and 'why'; AI handles 'how'", "Continuous learning and self-improvement culture", "AI Governance board for strategic oversight"],
            "human_pct": 15, "digital_pct": 85,
        },
        "process": {
            "description": "Fully autonomous; self-optimising; signal-driven governance; no fixed ceremonies",
            "indicators": ["No fixed sprint ceremonies - signal-driven", "AI autonomously plans, builds, tests, deploys", "Self-healing and self-optimising processes", "Outcome-triggered reviews (not calendar-driven)"],
        },
        "tools": {
            "description": "Fully orchestrated agent fleet; autonomous ADLC platform; predictive capabilities",
            "indicators": ["Autonomous ADLC platform (e.g., STUMP)", "Self-coordinating agent fleet", "Predictive analytics for risk & quality", "Autonomous infrastructure management"],
        },
        "automation": {
            "description": "Fully autonomous with human strategic oversight only",
            "level": "Autonomous / AI-Native",
            "automation_pct": 90,
            "ai_involvement": "Fully autonomous agents; human veto and strategic direction only",
        },
        "outcomes": {
            "deploy_frequency": "Continuous (multiple per day)",
            "lead_time": "< 1 day",
            "change_failure_rate": "< 5%",
            "mttr": "< 1 hour (often self-healed)",
            "flow_efficiency": "> 55%",
        },
    },
}


def get_reference_model():
    """Return the full L1-L5 reference model."""
    return MATURITY_REFERENCE


def get_level_definition(level: int) -> dict:
    """Return definition for a specific level."""
    return MATURITY_REFERENCE.get(level, MATURITY_REFERENCE[1])
