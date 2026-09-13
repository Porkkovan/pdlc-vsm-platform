"""
Platform implementation insights — what each target-state platform looks like
when deployed, including agents, tools, architecture, and differentiators.
"""

PLATFORM_INSIGHTS = {
    "homegrown": {
        "id": "homegrown",
        "implementation_summary": "Custom-built ADLC platform using open-source frameworks (LangGraph, CrewAI, etc.) with full architectural control.",
        "architecture": "Self-hosted multi-agent orchestration layer on Kubernetes. Custom agents per PDLC phase. Own LLM gateway.",
        "agents": [
            {"name": "Story Drafter", "phase": "Discovery", "description": "Generates user stories from product briefs and market signals"},
            {"name": "Architecture Advisor", "phase": "Architecture", "description": "Analyses requirements and proposes architecture patterns with ADRs"},
            {"name": "Code Generator", "phase": "Development", "description": "Generates implementation code from specifications"},
            {"name": "Test Synthesiser", "phase": "Testing", "description": "Creates test suites from acceptance criteria and code analysis"},
            {"name": "Security Scanner", "phase": "DevSecOps", "description": "SAST/DAST/SCA scanning with auto-remediation suggestions"},
            {"name": "Deploy Orchestrator", "phase": "DevSecOps", "description": "Manages CI/CD pipeline execution and rollback decisions"},
            {"name": "Incident Responder", "phase": "AIOps & Monitoring", "description": "Detects anomalies and initiates self-healing workflows"},
        ],
        "tools": ["LangGraph", "Custom LLM Gateway", "Kubernetes", "PostgreSQL", "Redis", "Prometheus/Grafana"],
        "differentiators": ["Full IP ownership", "Unlimited customisation", "No vendor lock-in", "Higher build cost but lower long-term TCO"],
        "investment_profile": {"upfront": "High", "ongoing": "Low-Medium", "team_ramp": "12-16 weeks"},
    },
    "bmad": {
        "id": "bmad",
        "implementation_summary": "BMad v6 (Breakthrough Method for Agile AI-Driven Development) — open-source persona-based agent framework with 6 consolidated agents. v6 merged the former Scrum Master (Bob) and QA (Quinn) personas into the Developer agent (Amelia), reducing handoffs. Each persona has defined checklists, templates, and artifact handoff protocols across 4 workflow phases: Analysis, Planning, Solutioning, Implementation.",
        "architecture": "Open-source agent orchestration built on Cursor/Claude. 6 persona-based agents with structured checklists and handoff protocols. Git-native workflow with markdown-driven knowledge base. Agents operate via IDE (Cursor/VS Code) — no separate platform.",
        "agents": [
            {"name": "Analyst (Mary)", "phase": "Discovery", "description": "Brainstorming, market research, domain research, technical research, project brief creation, PRFAQ challenge and documentation"},
            {"name": "Product Manager (John)", "phase": "Discovery", "description": "Creates and validates PRDs, defines epics and user stories, manages implementation readiness reviews, course-corrects scope"},
            {"name": "Architect (Winston)", "phase": "Architecture", "description": "Creates architecture designs, defines tech stack, API contracts, and DB schemas; conducts implementation readiness reviews"},
            {"name": "UX Designer (Sally)", "phase": "Architecture", "description": "UX spec creation, component and interaction patterns, wireframes, user journey maps, accessibility-compliant design specs"},
            {"name": "Developer (Amelia)", "phase": "Development", "description": "Dev story implementation, code generation, code review, QA test generation, sprint planning, epic retrospective, forensic investigation — absorbed former SM (Bob) and QA (Quinn) roles in v6"},
            {"name": "Tech Writer (Paige)", "phase": "AIOps & Monitoring", "description": "Auto-generates API documentation, runbooks, architecture diagrams, release notes, and knowledge base articles from code changes"},
        ],
        "tools": ["Cursor IDE / VS Code", "Claude / GPT Models", "Git-native Workflow", "Markdown Knowledge Base", "Checklist Engine", "BMad Templates", "GitHub/GitLab Integration"],
        "differentiators": ["Open-source (49K+ GitHub stars)", "6 consolidated persona agents — fewer handoffs than v5", "Checklist-driven artifact handoffs ensure quality gates", "Works inside Cursor/VS Code — no separate platform needed", "Community-driven agent templates and personas", "Lower entry cost than enterprise COTS", "Developer persona covers QA + sprint management — team can extend with custom personas"],
        "investment_profile": {"upfront": "Low-Medium", "ongoing": "Low", "team_ramp": "2-4 weeks"},
    },
    "copilot_workspace": {
        "id": "copilot_workspace",
        "implementation_summary": "GitHub Copilot (2026) — AI-powered development ecosystem embedded across all GitHub surfaces. Copilot Coding Agent autonomously implements issues as PRs. Agent Mode (GA in VS Code + JetBrains) handles multi-file editing with terminal access. GitHub Spark builds apps from natural language. Custom Agents extend via MCP.",
        "architecture": "GitHub-hosted SaaS. AI embedded across IDE, PRs, Issues, Actions, and Security surfaces. Copilot Coding Agent for asynchronous autonomous tasks. GitHub Advanced Security (GHAS) for CodeQL, secret scanning, and supply chain. Custom Agents via MCP for org-specific tooling.",
        "agents": [
            {"name": "Copilot Chat", "phase": "Discovery", "description": "Conversational AI across IDE sidebar, GitHub.com, and mobile — @workspace context for codebase-wide questions, requirement exploration, and code explanation"},
            {"name": "Semantic Code Search", "phase": "Discovery", "description": "Embedding-based conceptual code discovery — finds related code across repos by meaning, not just keywords; surfaces patterns and dependencies"},
            {"name": "GitHub Spark", "phase": "Architecture", "description": "Natural language app builder with live preview — generates full applications from descriptions, iterates on design through conversation"},
            {"name": "Copilot Code Completion", "phase": "Development", "description": "Inline suggestions for single lines, code blocks, and full functions — context-aware multi-line completions across all supported IDEs"},
            {"name": "Copilot Agent Mode", "phase": "Development", "description": "Autonomous multi-file editing with terminal command execution — plans changes, edits files, runs commands, iterates on errors (GA in VS Code + JetBrains)"},
            {"name": "Copilot Coding Agent", "phase": "Development", "description": "Fully autonomous background agent — assigned a GitHub Issue, plans implementation, writes code, creates PR, iterates on review feedback asynchronously"},
            {"name": "Copilot Code Review", "phase": "Testing", "description": "Agentic PR analysis with full project context — line-by-line suggestions, code quality checks, security review, and pattern enforcement"},
            {"name": "Copilot Autofix", "phase": "DevSecOps", "description": "Auto-generates fix PRs for CodeQL security alerts, Dependabot dependency vulnerabilities, and secret scanning findings"},
            {"name": "GitHub Advanced Security (GHAS)", "phase": "DevSecOps", "description": "CodeQL SAST, secret scanning, dependency review, and supply chain security with AI-powered alert prioritisation and Custom Agents via MCP"},
        ],
        "tools": ["GitHub Copilot Business/Enterprise", "GitHub Copilot Desktop App", "GitHub Actions", "GitHub Advanced Security (GHAS)", "CodeQL", "Dependabot", "Custom Agents + MCP", "VS Code / JetBrains"],
        "differentiators": ["Deepest GitHub-native integration across all surfaces", "Copilot Coding Agent for autonomous issue→PR workflows", "Agent Mode GA for multi-file + terminal autonomy", "GitHub Spark for NL-to-app prototyping", "GHAS security suite built in", "Custom Agents via MCP for org-specific extensions", "Limited to GitHub ecosystem", "No AIOps/monitoring — pair with Datadog/PagerDuty"],
        "investment_profile": {"upfront": "Low", "ongoing": "Medium ($19-39/user/mo)", "team_ramp": "1-2 weeks"},
    },
    "devin": {
        "id": "devin",
        "implementation_summary": "Devin by Cognition (2026) — a single unified autonomous AI software engineer, NOT separate agents. Operates in a persistent sandboxed cloud environment with its own terminal, editor, and browser. Multiple product surfaces access the same core agent: Devin Cloud, Devin Desktop IDE (formerly Windsurf, acquired 2025), Devin CLI, Devin Review, and DeepWiki. Supports parallel sessions with sub-agents.",
        "architecture": "Cloud-hosted sandboxed environment per session with persistent workspace and memory. Single unified agent with multiple product surfaces. Integrates via Slack, Microsoft Teams, Linear, Jira, GitHub, GitLab, and Bitbucket. Publishes MCP server (mcp.devin.ai) for external agent orchestration.",
        "agents": [
            {"name": "Devin (Plan & Research)", "phase": "Discovery", "description": "Unified agent capability — analyses requirements from Slack/GitHub/Linear/Jira, researches documentation and APIs using built-in browser, creates multi-step implementation plans"},
            {"name": "Devin (Architecture & Design)", "phase": "Architecture", "description": "Unified agent capability — evaluates codebase structure, proposes architecture changes, assesses dependency impacts, navigates and understands large codebases"},
            {"name": "Devin (Autonomous Coding)", "phase": "Development", "description": "Unified agent capability — full-stack code generation across multiple files, handles complex refactoring, creates PRs. Parallel sessions enable concurrent workstreams"},
            {"name": "Devin Desktop IDE", "phase": "Development", "description": "Local IDE surface (formerly Windsurf, acquired 2025) — agentic coding in a desktop environment, bundled with all paid plans"},
            {"name": "Devin Review", "phase": "Testing", "description": "Separate product surface — automated pull request analysis with deep context, line-by-line feedback, and security checks (paid tiers)"},
            {"name": "Devin (Test & Debug)", "phase": "Testing", "description": "Unified agent capability — writes test suites, runs tests in sandbox, reproduces bugs, traces root causes through stack traces and logs, implements and verifies fixes"},
            {"name": "Devin (DevOps & Deploy)", "phase": "DevSecOps", "description": "Unified agent capability — configures CI/CD pipelines, writes Dockerfiles/IaC, manages deployments. MCP server (mcp.devin.ai) enables external agents to manage sessions and playbooks"},
            {"name": "DeepWiki", "phase": "AIOps & Monitoring", "description": "Separate product surface — auto-generates and maintains codebase documentation, architecture maps, and knowledge articles (paid tiers)"},
        ],
        "tools": ["Devin Cloud Agent", "Devin Desktop IDE (Windsurf)", "Devin CLI", "Devin Review", "DeepWiki", "Ask Devin", "Devin MCP Server", "Slack/Teams/Linear/Jira Integration"],
        "differentiators": ["Single unified autonomous agent — highest autonomy, not a co-pilot", "Persistent sandboxed environment per session (terminal + editor + browser)", "Parallel sessions with sub-agents for concurrent workstreams", "Multiple product surfaces: Cloud, Desktop IDE, CLI, Review, DeepWiki", "MCP server enables orchestration by external agents", "Task intake via Slack, Teams, Linear, Jira, GitHub, GitLab, Bitbucket", "Session-based pricing — can be expensive at scale"],
        "investment_profile": {"upfront": "Low", "ongoing": "High ($500/mo base + per-session ACUs)", "team_ramp": "1-2 weeks"},
    },
    "cursor": {
        "id": "cursor",
        "implementation_summary": "Cursor 3 (2026) — AI-first IDE with Tab (Sonic model autocomplete), Composer for multi-file orchestration, Agent Mode with terminal autonomy, Background Agents in cloud sandboxes, and BugBot for automated PR review. Extends to external tools via MCP servers. Cursor Rules (.mdc) and Hooks enforce team standards.",
        "architecture": "Desktop IDE (VS Code fork) + JetBrains plugin + Web UI + Mobile apps. Cloud AI backend with Background Agents in sandboxed environments. MCP servers (stdio + SSE) extend agent capabilities to databases, observability, and project management tools. Cursor Rules (.cursor/rules/*.mdc) with YAML frontmatter for conditional rule application.",
        "agents": [
            {"name": "Cursor Chat", "phase": "Discovery", "description": "Conversational AI with @file, @folder, @docs, @web, @codebase, @diff, @terminal context — requirement exploration, code explanation, and architecture questions"},
            {"name": "Cursor Composer", "phase": "Architecture", "description": "Multi-file creation and editing orchestration (Cmd+I) — reads relevant files, identifies changes needed, proposes diffs across all files in one review surface"},
            {"name": "Cursor Tab", "phase": "Development", "description": "Predictive multi-line autocomplete on Sonic model — predicts next edits across current and related files, suggests cursor position moves"},
            {"name": "Cursor Agent Mode", "phase": "Development", "description": "Autonomous mode extending Composer — runs terminal commands (with configurable approval gates), reads output, runs tests, parses failures, proposes fixes, iterates"},
            {"name": "Background Agent", "phase": "Development", "description": "Cloud-hosted sandboxed agent — reads GitHub issues, opens branches, commits, and drafts PRs autonomously while developer works on other tasks"},
            {"name": "BugBot", "phase": "Testing", "description": "GitHub-integrated PR reviewer — inspects every pull request (human or agent-authored), posts inline comments on regressions, missing error handling, and risky changes"},
            {"name": "Cursor Rules & Hooks", "phase": "DevSecOps", "description": "Cursor Rules (.cursor/rules/*.mdc) enforce team coding standards via glob patterns. Cursor Hooks (onPreEdit, onPostEdit, onPreCommit, onApprove) trigger automation scripts"},
            {"name": "Cursor MCP", "phase": "DevSecOps", "description": "Model Context Protocol integration — connects to external tool servers (databases, CI/CD, observability, project management) via stdio and SSE transports for agent-driven DevOps"},
        ],
        "tools": ["Cursor IDE", "Cursor JetBrains Plugin", "Background Agents (cloud sandbox)", "BugBot", "MCP Servers (stdio + SSE)", "Cursor Rules (.mdc)", "Cursor Hooks", "Cursor CLI", "GitHub/GitLab Integration"],
        "differentiators": ["Best-in-class developer UX — Tab (Sonic), Composer, Agent Mode", "Background Agents for parallel autonomous work in cloud sandboxes", "BugBot for automated PR review on every pull request", "MCP protocol extends to any external tool or service", "Cursor Rules (.mdc) + Hooks enforce team standards at IDE level", "Available on desktop, JetBrains, web, and mobile", "IDE-centric — enterprise orchestration via MCP, not a separate platform", "No built-in security scanning — pair with GHAS/Snyk"],
        "investment_profile": {"upfront": "Low", "ongoing": "Medium ($20-40/user/mo)", "team_ramp": "1-2 weeks"},
    },
    "flowsource": {
        "id": "flowsource",
        "implementation_summary": "Cognizant Flowsource — enterprise-grade AI software engineering platform with managed agent fleet.",
        "architecture": "Cognizant cloud-hosted. Pre-built enterprise agents. Integrated governance, compliance, and reporting.",
        "agents": [
            {"name": "Flow Analyst", "phase": "Discovery", "description": "Analyses requirements and generates structured product backlogs"},
            {"name": "Flow Architect", "phase": "Architecture", "description": "Produces architecture designs aligned to enterprise patterns"},
            {"name": "Flow Builder", "phase": "Development", "description": "Enterprise-grade code generation with compliance guardrails"},
            {"name": "Flow Tester", "phase": "Testing", "description": "Comprehensive test generation: unit, integration, E2E, performance"},
            {"name": "Flow SecOps", "phase": "DevSecOps", "description": "Automated security scanning, compliance checks, and remediation"},
            {"name": "Flow Deployer", "phase": "DevSecOps", "description": "Managed CI/CD orchestration with approval gates"},
            {"name": "Flow Monitor", "phase": "AIOps & Monitoring", "description": "AIOps monitoring with anomaly detection and auto-remediation"},
        ],
        "tools": ["Flowsource Platform", "Cognizant AI CoE Integration", "Enterprise SSO", "Audit Dashboard"],
        "differentiators": ["Enterprise-ready out of box", "Cognizant managed service", "Built-in compliance (SOC2, ISO27001)", "Lowest in-house effort", "Higher ongoing cost"],
        "investment_profile": {"upfront": "Medium-High", "ongoing": "High (managed service)", "team_ramp": "3-4 weeks"},
    },
    "baxter": {
        "id": "baxter",
        "implementation_summary": "Cognizant Baxter — AI-powered software engineering platform with specialised agents for enterprise delivery, continuous testing, and intelligent automation.",
        "architecture": "Cognizant cloud-hosted. Specialised agent fleet per SDLC discipline. Deep integration with enterprise ALM tools. Built-in AI governance layer.",
        "agents": [
            {"name": "Baxter Story Crafter", "phase": "Discovery", "description": "Generates user stories with acceptance criteria from business requirements, market analysis, and competitor insights"},
            {"name": "Baxter Design Intelligence", "phase": "Architecture", "description": "AI-driven architecture recommendations with enterprise pattern library and tech debt analysis"},
            {"name": "Baxter Code Pilot", "phase": "Development", "description": "Context-aware code generation with enterprise coding standards enforcement and multi-repo awareness"},
            {"name": "Baxter Test Maestro", "phase": "Testing", "description": "Intelligent test generation across unit, integration, E2E, performance, and chaos engineering"},
            {"name": "Baxter Security Sentinel", "phase": "DevSecOps", "description": "Continuous security scanning with auto-remediation, compliance mapping, and risk scoring"},
            {"name": "Baxter Release Captain", "phase": "DevSecOps", "description": "Orchestrates release pipelines with canary deployments, feature flags, and auto-rollback"},
            {"name": "Baxter Ops Guardian", "phase": "AIOps & Monitoring", "description": "Predictive monitoring with self-healing capabilities, anomaly detection, and incident orchestration"},
            {"name": "Baxter Insight Engine", "phase": "AIOps & Monitoring", "description": "Continuous delivery intelligence — velocity trends, quality predictions, and team health metrics"},
        ],
        "tools": ["Baxter Platform", "Baxter Agent Studio", "Cognizant AI CoE", "Enterprise ALM Connectors", "Governance Dashboard", "Compliance Automation Suite"],
        "differentiators": [
            "8 specialised agents vs Flowsource's 7 — deeper coverage per phase",
            "Built-in continuous testing intelligence (Test Maestro)",
            "Predictive delivery analytics (Insight Engine)",
            "Enterprise ALM deep integration (Jira, ADO, ServiceNow native connectors)",
            "Cognizant managed service with 24/7 support",
            "Industry-specific compliance templates (Banking, Healthcare, Telco)",
        ],
        "vs_current_state": {
            "summary": "Replaces 60-80% of manual SDLC activities with specialised AI agents. Reduces lead time by 40-60%. Shifts team focus from execution to strategy and governance.",
            "before_after": [
                {"activity": "User story creation", "before": "Manual (PO writes)", "after": "Baxter Story Crafter drafts, PO reviews/approves"},
                {"activity": "Architecture review", "before": "Manual meetings + docs", "after": "Baxter Design Intelligence proposes, Architect validates"},
                {"activity": "Code development", "before": "Developer writes all code", "after": "Baxter Code Pilot generates 60-70%, developer refines"},
                {"activity": "Test creation", "before": "QA manually writes test cases", "after": "Baxter Test Maestro generates full test suites"},
                {"activity": "Security scanning", "before": "Periodic manual scans", "after": "Continuous automated scanning + auto-remediation"},
                {"activity": "Deployment", "before": "Manual release process", "after": "Automated canary + feature flag orchestration"},
                {"activity": "Incident response", "before": "Manual triage + escalation", "after": "Predictive detection + self-healing"},
            ],
        },
        "investment_profile": {"upfront": "Medium-High", "ongoing": "High (managed service + platform license)", "team_ramp": "4-6 weeks"},
    },
}


def get_platform_insight(platform_id: str) -> dict | None:
    return PLATFORM_INSIGHTS.get(platform_id)


def get_all_insights() -> dict:
    return PLATFORM_INSIGHTS
