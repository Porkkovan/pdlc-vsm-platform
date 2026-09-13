"""
Dynamic maturity ladder — L1-L5 definitions that vary by chosen platform approach.
Each platform has different implications for what each level looks like in terms of
People, Process, Tools, Outcomes, and Investment.
"""
from .catalog import INTERIM_LADDER

PLATFORM_KIND_MAP = {
    "homegrown": "home_grown",
    "bmad": "cots",
    "copilot_workspace": "cots",
    "devin": "cots",
    "cursor": "cots",
    "flowsource": "service_provider",
    "baxter": "service_provider",
}

# Per-level, per-platform-kind perspective overrides.
# Structure: LEVEL_PERSPECTIVES[level][platform_kind] = {people, process, tools, outcomes, investment}
# Falls back to a "default" key if the platform_kind is missing.

LEVEL_PERSPECTIVES = {
    1: {
        "default": {
            "people": {"summary": "All traditional roles retained", "team_shape": "8-12 per team", "key_roles": ["Product Owner", "BA", "Developers (4-6)", "QA (2-3)", "Scrum Master", "DevOps"]},
            "process": {"summary": "Standard sprint-based Agile", "ceremonies": ["Sprint Planning", "Daily Standup", "Sprint Review", "Retrospective"], "flow_model": "Sprint-based (2-week)"},
            "tools": {"summary": "Basic toolchain with some AI prompting", "stack": ["Jira/ADO", "GitHub/GitLab", "Jenkins/GHA", "Basic IDE"]},
            "outcomes": {"deploy_freq": "Monthly", "lead_time": "> 30 days", "automation": "5-20%"},
            "investment": {"upfront": "$50K-100K", "annual": "$200K-400K", "payback": "N/A (baseline)"},
        },
    },
    2: {
        "home_grown": {
            "people": {"summary": "Begin building AI/ML engineering capability in-house", "team_shape": "Core team + 2-3 AI engineers", "key_roles": ["Product Owner", "Developers", "QA", "AI/ML Engineers", "Platform Engineer"]},
            "process": {"summary": "Sprint-based with AI-assisted backlog refinement", "ceremonies": ["Sprint Planning (AI-assisted)", "Standups", "AI-assisted Code Review"], "flow_model": "Sprint-based with AI touchpoints"},
            "tools": {"summary": "Custom AI tooling begins; own LLM gateway", "stack": ["Custom LLM Gateway", "LangChain/LangGraph", "Self-hosted models", "Custom dashboards"]},
            "outcomes": {"deploy_freq": "Bi-weekly", "lead_time": "15-25 days", "automation": "20-35%"},
            "investment": {"upfront": "$200K-500K", "annual": "$300K-500K", "payback": "18-24 months"},
        },
        "cots": {
            "people": {"summary": "Developers adopt AI coding assistants; roles unchanged", "team_shape": "Standard team + AI tool licenses", "key_roles": ["Product Owner", "Developers (AI-assisted)", "QA", "Scrum Master"]},
            "process": {"summary": "Existing processes enhanced with AI co-pilots", "ceremonies": ["Standard Agile ceremonies", "AI-assisted code reviews"], "flow_model": "Sprint-based with AI assist"},
            "tools": {"summary": "COTS AI tools integrated into developer workflow", "stack": ["Copilot/Cursor/Devin", "Existing ALM tools", "AI-enhanced IDE"]},
            "outcomes": {"deploy_freq": "Bi-weekly", "lead_time": "15-20 days", "automation": "25-40%"},
            "investment": {"upfront": "$50K-150K", "annual": "$100K-300K (licenses)", "payback": "6-12 months"},
        },
        "service_provider": {
            "people": {"summary": "Cognizant team augments; minimal in-house ramp needed", "team_shape": "In-house team + Cognizant platform support", "key_roles": ["Product Owner", "Developers", "Cognizant Platform Lead", "Cognizant Integration Eng"]},
            "process": {"summary": "Cognizant platform onboarding; phased agent activation", "ceremonies": ["Standard ceremonies", "Platform onboarding sessions", "Agent configuration workshops"], "flow_model": "Sprint-based with managed AI"},
            "tools": {"summary": "Cognizant platform deployed; first agents activated", "stack": ["Flowsource/Baxter Platform", "Enterprise ALM Connectors", "Governance Dashboard"]},
            "outcomes": {"deploy_freq": "Bi-weekly", "lead_time": "12-20 days", "automation": "25-40%"},
            "investment": {"upfront": "$150K-400K", "annual": "$200K-500K (managed service)", "payback": "12-18 months"},
        },
    },
    3: {
        "home_grown": {
            "people": {"summary": "Dedicated platform team; developers become AI-fluent", "team_shape": "Product teams + 4-6 person platform team", "key_roles": ["Product Owner", "Senior Devs (AI-fluent)", "Platform Engineers", "QA Lead", "AI Architect"]},
            "process": {"summary": "AI-assisted across most phases; human approvals at gates", "ceremonies": ["Continuous planning (AI-drafted)", "Exception-based standups", "AI-assisted sprint reviews"], "flow_model": "Hybrid: sprints with AI automation"},
            "tools": {"summary": "Custom multi-agent framework operational", "stack": ["Custom Agent Orchestrator", "LangGraph agents per phase", "Own embedding/RAG pipeline", "Custom monitoring"]},
            "outcomes": {"deploy_freq": "Weekly", "lead_time": "5-12 days", "automation": "45-60%"},
            "investment": {"upfront": "$500K-1M", "annual": "$400K-700K", "payback": "12-18 months"},
        },
        "cots": {
            "people": {"summary": "Team reduces as AI handles more routine work", "team_shape": "Leaner team with AI agent subscriptions", "key_roles": ["Product Owner", "Senior Developers", "QA Lead", "DevOps Lead"]},
            "process": {"summary": "AI-first development; human review at quality gates", "ceremonies": ["Lightweight planning", "AI-generated code reviews", "Gate-based approvals"], "flow_model": "AI-first sprints"},
            "tools": {"summary": "Full COTS AI suite deployed with enterprise plugins", "stack": ["Copilot Workspace / Devin / Cursor Agent Mode", "AI-powered testing tools", "Automated security scanning"]},
            "outcomes": {"deploy_freq": "Weekly", "lead_time": "5-10 days", "automation": "50-65%"},
            "investment": {"upfront": "$100K-300K", "annual": "$200K-500K (licenses)", "payback": "9-15 months"},
        },
        "service_provider": {
            "people": {"summary": "Most SDLC execution shifts to Cognizant platform agents", "team_shape": "Reduced in-house + Cognizant managed agents", "key_roles": ["Product Owner", "Tech Lead", "QA Lead", "Cognizant Platform Manager"]},
            "process": {"summary": "Agent-driven across 5+ phases; human oversight at gates", "ceremonies": ["AI-drafted planning", "Exception reviews", "Weekly governance sync"], "flow_model": "Agent-driven with human gates"},
            "tools": {"summary": "Full Cognizant platform with all agents active", "stack": ["Flowsource/Baxter (all agents active)", "Enterprise integrations", "Compliance automation", "AI governance layer"]},
            "outcomes": {"deploy_freq": "Weekly to on-demand", "lead_time": "3-8 days", "automation": "55-70%"},
            "investment": {"upfront": "$300K-600K", "annual": "$400K-800K (managed service)", "payback": "10-16 months"},
        },
    },
    4: {
        "home_grown": {
            "people": {"summary": "Product Definers + Builders; platform team maintains agent fleet", "team_shape": "3-5 per product + 5-8 platform engineers", "key_roles": ["Product Definer", "Product Builder", "AI Architect", "Platform Engineers"]},
            "process": {"summary": "Continuous flow; no sprints; pull-based agent orchestration", "ceremonies": ["Continuous planning (on-demand)", "Async flow standup", "On-demand showcase"], "flow_model": "Continuous flow (no sprints)"},
            "tools": {"summary": "Mature custom agent fleet with self-healing capabilities", "stack": ["Custom Agent Orchestration Platform", "Self-healing CI/CD", "Autonomous testing agents", "AIOps monitoring"]},
            "outcomes": {"deploy_freq": "Daily", "lead_time": "1-3 days", "automation": "75-85%"},
            "investment": {"upfront": "$1M-2M (cumulative)", "annual": "$500K-900K", "payback": "6-12 months (from L3)"},
        },
        "cots": {
            "people": {"summary": "Small oversight team; AI handles 70%+ of SDLC", "team_shape": "3-5 per product line", "key_roles": ["Product Definer", "Senior Architect", "AI Governance", "DevOps Lead"]},
            "process": {"summary": "Continuous delivery; AI-driven with exception reviews", "ceremonies": ["On-demand planning", "AI-generated showcases", "Exception escalations"], "flow_model": "Continuous with AI orchestration"},
            "tools": {"summary": "Enterprise COTS AI suite with full agent mode", "stack": ["Advanced agent subscriptions", "Multi-tool orchestration (MCP)", "AI-powered CI/CD", "Predictive monitoring"]},
            "outcomes": {"deploy_freq": "Daily to on-demand", "lead_time": "1-3 days", "automation": "70-80%"},
            "investment": {"upfront": "$200K-500K", "annual": "$300K-600K", "payback": "6-10 months (from L3)"},
        },
        "service_provider": {
            "people": {"summary": "Minimal in-house; Cognizant platform fully autonomous", "team_shape": "2-4 in-house + Cognizant managed", "key_roles": ["Product Definer", "Product Builder", "Cognizant AI Governance Lead"]},
            "process": {"summary": "Fully managed by Cognizant agents; human veto at strategic decisions", "ceremonies": ["Outcome-triggered reviews", "Weekly governance report", "Monthly strategic alignment"], "flow_model": "Fully managed autonomous flow"},
            "tools": {"summary": "Cognizant platform at full maturity with predictive capabilities", "stack": ["Flowsource/Baxter (full autonomous mode)", "Predictive analytics", "Self-healing infrastructure", "Compliance autopilot"]},
            "outcomes": {"deploy_freq": "Multiple per day", "lead_time": "< 1 day", "automation": "80-90%"},
            "investment": {"upfront": "$400K-800K", "annual": "$500K-1M (managed service)", "payback": "6-10 months (from L3)"},
        },
    },
    5: {
        "home_grown": {
            "people": {"summary": "Product Definer + Product Builder + Architect only", "team_shape": "3 core roles per product line", "key_roles": ["Product Definer", "Product Builder", "Architect (incl. risk)"]},
            "process": {"summary": "Self-optimising autonomous ADLC; signal-driven governance", "ceremonies": ["Outcome-triggered reviews only", "Autonomous improvement cycles", "Strategic oversight board (monthly)"], "flow_model": "Fully autonomous"},
            "tools": {"summary": "Self-evolving custom platform with autonomous agents", "stack": ["Custom Autonomous ADLC Platform", "Self-evolving agents", "Predictive risk engine", "Autonomous infrastructure"]},
            "outcomes": {"deploy_freq": "Continuous", "lead_time": "< 1 day", "automation": "90%+"},
            "investment": {"upfront": "$1.5M-3M (cumulative)", "annual": "$600K-1M", "payback": "Ongoing ROI"},
        },
        "cots": {
            "people": {"summary": "Product Definer + Architect; AI handles rest", "team_shape": "2-3 per product line", "key_roles": ["Product Definer", "Product Builder", "AI Governance"]},
            "process": {"summary": "Fully autonomous; AI self-optimises delivery pipeline", "ceremonies": ["Signal-driven reviews", "Autonomous retros", "Monthly strategic check"], "flow_model": "Fully autonomous"},
            "tools": {"summary": "Best-of-breed COTS stack, fully orchestrated", "stack": ["Multi-vendor AI agents (orchestrated)", "Autonomous CI/CD", "Self-healing infrastructure"]},
            "outcomes": {"deploy_freq": "Continuous", "lead_time": "< 1 day", "automation": "88%+"},
            "investment": {"upfront": "$400K-800K (cumulative)", "annual": "$400K-700K", "payback": "Ongoing ROI"},
        },
        "service_provider": {
            "people": {"summary": "Product Definer + Strategic oversight only; Cognizant manages everything", "team_shape": "1-2 in-house + Cognizant full-managed", "key_roles": ["Product Definer", "Strategic Governance (in-house)", "Cognizant Delivery Lead"]},
            "process": {"summary": "Cognizant fully autonomous ADLC; customer defines intent only", "ceremonies": ["Outcome reviews (automated)", "Monthly strategic alignment", "Quarterly business review"], "flow_model": "Cognizant-managed autonomous"},
            "tools": {"summary": "Cognizant platform — fully autonomous, self-optimising", "stack": ["Flowsource/Baxter (autonomous mode)", "AI-driven governance", "Predictive delivery intelligence", "Self-evolving agents"]},
            "outcomes": {"deploy_freq": "Continuous", "lead_time": "< 0.5 day", "automation": "92%+"},
            "investment": {"upfront": "$600K-1.2M (cumulative)", "annual": "$600K-1.2M (managed)", "payback": "Ongoing ROI"},
        },
    },
}


def get_dynamic_ladder(platform_id: str) -> list[dict]:
    """Return the L1-L5 ladder enriched with platform-specific perspectives."""
    kind = PLATFORM_KIND_MAP.get(platform_id, "cots")
    result = []
    for base in INTERIM_LADDER:
        level = base["level"]
        perspectives = LEVEL_PERSPECTIVES.get(level, {})
        persp = perspectives.get(kind, perspectives.get("default", {}))

        actions = _level_actions(level, kind)

        result.append({
            **base,
            "perspectives": persp,
            "platform_kind": kind,
            "platform_id": platform_id,
            "level_actions": actions,
        })
    return result


def _level_actions(level: int, kind: str) -> list[str]:
    """High-level actions needed to achieve this level."""
    base_actions = {
        1: [
            "Introduce AI coding assistants to development team",
            "Set up basic prompt engineering training",
            "Identify 2-3 highest-impact activities for AI assistance",
            "Establish AI usage guidelines and policies",
        ],
        2: [
            "Deploy AI co-pilots across development and testing phases",
            "Implement AI-assisted code review workflows",
            "Set up AI-powered test generation for new features",
            "Train team on prompt engineering and AI collaboration",
            "Establish metrics for AI-assisted vs manual productivity",
        ],
        3: [
            "Deploy independent AI agents for routine SDLC tasks",
            "Implement multi-agent handoffs between phases",
            "Set up quality gates with human review at key checkpoints",
            "Shift team roles: developers focus on architecture and edge cases",
            "Implement continuous measurement of automation coverage",
        ],
        4: [
            "Activate full multi-agent orchestration across all phases",
            "Transition to continuous flow (remove sprint boundaries)",
            "Implement exception-based human review (AI handles standard cases)",
            "Deploy self-healing CI/CD pipelines",
            "Evolve roles: Product Definer, Product Builder, AI Governance",
        ],
        5: [
            "Enable fully autonomous agent fleet across all PDLC phases",
            "Implement signal-driven governance (no fixed ceremonies)",
            "Deploy self-optimising agent capabilities",
            "Human involvement limited to intent definition and strategic oversight",
            "Continuous autonomous improvement cycles",
        ],
    }

    kind_extras = {
        "home_grown": {
            2: ["Build custom LLM gateway and agent framework", "Hire AI/ML engineering talent"],
            3: ["Scale custom agent fleet to cover 5+ PDLC phases", "Build internal RAG pipeline"],
            4: ["Mature platform team to 5-8 engineers", "Implement autonomous agent coordination"],
            5: ["Achieve self-evolving agent capabilities", "Reduce platform team to maintenance mode"],
        },
        "cots": {
            2: ["Procure and deploy COTS AI tool licenses", "Configure integrations with existing ALM"],
            3: ["Upgrade to enterprise AI tool plans with agent mode", "Set up multi-tool orchestration"],
            4: ["Implement full agent mode across tool suite", "Set up MCP-based orchestration"],
            5: ["Achieve autonomous operation across best-of-breed tools"],
        },
        "service_provider": {
            2: ["Onboard Cognizant platform team", "Configure platform connectors to enterprise tools"],
            3: ["Activate all phase-specific agents on Cognizant platform", "Complete compliance configuration"],
            4: ["Enable autonomous mode on Cognizant platform", "Transition to managed service model"],
            5: ["Enable full autonomous Cognizant-managed delivery", "Customer retains strategic oversight only"],
        },
    }

    actions = list(base_actions.get(level, []))
    extras = kind_extras.get(kind, {}).get(level, [])
    actions.extend(extras)
    return actions
