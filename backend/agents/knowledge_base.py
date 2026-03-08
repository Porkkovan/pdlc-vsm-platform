"""
PDLC VSM Platform — Built-in Knowledge Base
Industry benchmarks, DORA research, transformation patterns, lean VSM data.
Used by RAG engine to provide grounded context to all agents.
"""

# Each document: {id, category, title, content, tags, source}
KB_DOCUMENTS = [

    # ── DORA Research ────────────────────────────────────────────────
    {
        "id": "dora-2024-elite",
        "category": "DORA Benchmarks",
        "title": "DORA 2024 State of DevOps — Elite Performers",
        "content": (
            "Elite DevOps teams deploy multiple times per day with lead time for changes under 1 hour. "
            "Change failure rate is below 5% and MTTR under 1 hour. Elite performers are 3.5× more likely "
            "to exceed organizational performance goals. They achieve 182× more frequent deployments and "
            "2555× faster recovery from incidents than low performers. Flow efficiency averages above 40%. "
            "Key differentiators: trunk-based development, automated testing >90%, AI-assisted code review, "
            "infrastructure as code, observability-first culture, no manual approval gates for standard changes."
        ),
        "tags": ["dora", "elite", "deployment frequency", "lead time", "mttr", "cfr", "flow efficiency"],
        "source": "DORA State of DevOps 2024"
    },
    {
        "id": "dora-2024-high",
        "category": "DORA Benchmarks",
        "title": "DORA 2024 — High Performers",
        "content": (
            "High-performing teams deploy between once per day and once per week. Lead time is 1 day to 1 week. "
            "Change failure rate 5–10%, MTTR under 1 day. High performers exceed org goals 2× more than medium. "
            "They invest heavily in CI/CD automation, trunk-based development, and automated testing (>70% coverage). "
            "Progressive delivery techniques: canary releases, feature flags, blue/green deployments. "
            "Security scanning integrated in pipeline (shift-left). Average deployment pipeline duration: 45 minutes."
        ),
        "tags": ["dora", "high", "ci/cd", "automation", "trunk based", "test coverage", "pipeline"],
        "source": "DORA State of DevOps 2024"
    },
    {
        "id": "dora-2024-medium",
        "category": "DORA Benchmarks",
        "title": "DORA 2024 — Medium Performers",
        "content": (
            "Medium teams deploy between weekly and monthly. Lead time 1 week to 1 month. CFR 10–15%, "
            "MTTR 1 day to 1 week. Most large enterprises fall in this band. Key improvement levers: "
            "reducing manual gates in release pipeline, improving test automation, shifting security left. "
            "Common blockers: manual CAB process (adds 3–5 days), environment provisioning delays, "
            "limited test automation (<50% coverage), monolithic release trains, siloed teams."
        ),
        "tags": ["dora", "medium", "enterprise", "release pipeline", "test automation", "cab"],
        "source": "DORA State of DevOps 2024"
    },
    {
        "id": "dora-2024-low",
        "category": "DORA Benchmarks",
        "title": "DORA 2024 — Low Performers",
        "content": (
            "Low performers deploy monthly or less. Lead time over 1 month, CFR 15–60%, MTTR over 1 week. "
            "Characterised by manual deployments, lack of CI/CD, monolithic architectures, and siloed teams. "
            "Improvement focus: automation fundamentals, cultural transformation, backlog management. "
            "Starting points: implement basic CI pipeline, establish code review process, begin test automation, "
            "adopt trunk-based development, introduce feature flags for safer releases."
        ),
        "tags": ["dora", "low", "manual", "monolith", "siloed", "improvement", "ci pipeline"],
        "source": "DORA State of DevOps 2024"
    },
    {
        "id": "dora-vsm-correlation",
        "category": "DORA Benchmarks",
        "title": "DORA Metrics to VSM Phase Correlation Research",
        "content": (
            "Research shows direct correlation between DORA metrics and VSM phase performance: "
            "Every 10% improvement in deployment frequency reduces Phase 6 (Continuous Delivery) wait time by 8 hours. "
            "Each 1-day reduction in lead time maps to 14% flow efficiency improvement. "
            "CFR below 5% indicates Phase 5 testing automation maturity >75%. "
            "MTTR under 1 hour correlates to Phase 7 monitoring maturity score >80/100. "
            "Build duration <10 minutes indicates Phase 4 CI pipeline optimization score >85%. "
            "Teams that calibrate VSM with DORA data achieve 23% more accurate bottleneck identification."
        ),
        "tags": ["dora", "vsm", "correlation", "calibration", "flow efficiency", "deployment", "lead time", "accuracy"],
        "source": "PDLC VSM Methodology Research 2024"
    },

    # ── Lean VSM Benchmarks ──────────────────────────────────────────
    {
        "id": "lean-vsm-flow-efficiency",
        "category": "Lean VSM",
        "title": "Flow Efficiency Industry Benchmarks by PDLC Phase",
        "content": (
            "Industry flow efficiency benchmarks per phase (p75): "
            "Phase 1 Backlog & Roadmap: 34%. Phase 2 Architecture & UX: 24%. "
            "Phase 3 Code Management: 71%. Phase 4 Continuous Integration: 43%. "
            "Phase 5 Continuous Testing: 55%. Phase 6 Continuous Delivery: 11%. "
            "Phase 7 Monitoring & Feedback: 29%. "
            "Overall target: >40% flow efficiency. World-class teams achieve 65%+. "
            "Most enterprises are at 15–25%. Wait time dominates in testing and delivery phases."
        ),
        "tags": ["flow efficiency", "vsm", "lean", "benchmark", "phase", "wait time"],
        "source": "Lean VSM Industry Research 2024"
    },
    {
        "id": "lean-vsm-lead-times",
        "category": "Lean VSM",
        "title": "Lead Time Benchmarks by PDLC Phase",
        "content": (
            "Median (p50) process times: Phase 1: 25h, Phase 2: 30h, Phase 3: 20h, Phase 4: 3h, "
            "Phase 5: 20h, Phase 6: 6h, Phase 7: 5h. "
            "Median wait times: Phase 1: 48h, Phase 2: 96h, Phase 3: 8h, Phase 4: 4h, "
            "Phase 5: 16h, Phase 6: 48h, Phase 7: 12h. "
            "Total feature lead time elite: <5 days. High: 5-14 days. Medium: 14-60 days. Low: >60 days. "
            "Phase 2 (Architecture/UX) and Phase 5 (Testing) account for 62% of total wait time on average."
        ),
        "tags": ["lead time", "process time", "wait time", "benchmark", "feature", "phase"],
        "source": "Lean VSM Industry Research 2024"
    },
    {
        "id": "lean-vsm-bottlenecks",
        "category": "Lean VSM",
        "title": "Most Common VSM Bottlenecks in Software Delivery",
        "content": (
            "Top 7 most common bottlenecks: "
            "1. Continuous Testing (Phase 5) — longest wait due to environment setup, test data, manual SIT/UAT. "
            "2. Release Gates (Phase 6) — CAB approvals and manual signoffs add 2-5 days wait. "
            "3. Architecture & UX Design (Phase 2) — long design cycles, sequential handoffs add 3-7 day waits. "
            "4. Code Review (Phase 3) — peer review queues average 4-24h wait. "
            "5. Backlog Refinement (Phase 1) — requirements churn creates rework loops. "
            "6. Performance Testing (Phase 5) — manual execution takes 16-40h with long queue. "
            "7. Incident Management (Phase 7) — reactive processes delay feedback loop."
        ),
        "tags": ["bottleneck", "testing", "release", "design", "code review", "performance", "incident"],
        "source": "Lean VSM Industry Research 2024"
    },
    {
        "id": "lean-vsm-improvement-patterns",
        "category": "Lean VSM",
        "title": "VSM Improvement Patterns — Pull System and Flow Optimization",
        "content": (
            "Lean VSM improvement patterns proven in software delivery: "
            "1. Single-piece flow: Limit WIP to 2 items per developer, reduces context switching 35%. "
            "2. Pull system: Use Kanban signals for Phase 3→4 handoff, eliminates batch queue waits. "
            "3. Kaizen bursts: Target Phase 5 testing with 5-day improvement sprints, achieve 40% reduction. "
            "4. Error-proofing (Poka-yoke): Automated gates at Phase 4 CI eliminate 70% of defect escapes. "
            "5. Visual management: Real-time VSM dashboards reduce coordination overhead 25%. "
            "6. SMED for deployments: Reduce setup time from hours to minutes with IaC and pipeline templates. "
            "Typical improvement timeline: 30-day sprints, 3 improvement cycles per quarter."
        ),
        "tags": ["lean", "improvement", "pull system", "kanban", "wip", "flow", "kaizen", "sprint"],
        "source": "Lean Software Manufacturing Research 2024"
    },

    # ── AI/GenAI Transformation ROI ──────────────────────────────────
    {
        "id": "ai-transform-roi-option-a",
        "category": "AI Transformation",
        "title": "Option A — Augmented Human (40% Automation) ROI Profile",
        "content": (
            "40% AI automation level. 8 human roles retained. 16 AI agents introduced. "
            "Expected outcomes: 35% process time reduction, 55% wait time reduction, "
            "flow efficiency improvement from ~20% to ~45%. "
            "Investment: $800K–$1.2M over 12 months. ROI: 2.5–3.0× in 24 months. "
            "Deployment frequency improves from monthly to weekly. Lead time drops by 40%. "
            "Best suited for: teams with strong existing engineering culture, risk-averse orgs, "
            "regulatory environments, first-time AI transformation. "
            "Annual benefits: $1.8M–$2.4M. Payback period: 18–24 months."
        ),
        "tags": ["option a", "augmented", "40% automation", "roi", "investment", "transformation", "annual benefits"],
        "source": "AI Transformation Research 2024"
    },
    {
        "id": "ai-transform-roi-option-b",
        "category": "AI Transformation",
        "title": "Option B — Hybrid Intelligence (65% Automation) ROI Profile",
        "content": (
            "65% AI automation level. 5 human roles retained. 12 AI agents introduced. "
            "Expected outcomes: 55% process time reduction, 72% wait time reduction, "
            "flow efficiency from ~20% to ~60%. "
            "Investment: $1.5M–$2.5M over 18 months. ROI: 3.5–4.0× in 24 months. "
            "Deployment frequency improves to daily. Lead time drops by 65%. CFR reduces to 5–8%. "
            "Best suited for: mid-maturity teams, digital-native organisations, "
            "competitive markets requiring velocity, healthcare tech, financial services. "
            "Annual benefits: $4.5M–$6.5M. Payback period: 12–18 months."
        ),
        "tags": ["option b", "hybrid", "65% automation", "roi", "investment", "transformation", "annual benefits"],
        "source": "AI Transformation Research 2024"
    },
    {
        "id": "ai-transform-roi-option-c",
        "category": "AI Transformation",
        "title": "Option C — AI-First (85% Automation) ROI Profile",
        "content": (
            "85% AI automation level. 2 human roles: Product Definer + Product Builder. 22 AI agents. "
            "Expected outcomes: 70% process time reduction, 88% wait time reduction, "
            "flow efficiency from ~20% to ~80%. "
            "Investment: $3M–$5M over 24 months. ROI: 5.0–6.0× in 36 months. "
            "Continuous deployment multiple times per day. Lead time under 1 day. CFR under 2%. "
            "Best suited for: digital leaders, high-volume transaction systems, greenfield products, "
            "organisations committed to AI-first engineering culture. "
            "Annual benefits: $14M–$20M. Payback period: 24–30 months."
        ),
        "tags": ["option c", "ai-first", "85% automation", "roi", "investment", "transformation", "annual benefits"],
        "source": "AI Transformation Research 2024"
    },
    {
        "id": "ai-transform-change-management",
        "category": "AI Transformation",
        "title": "AI Transformation Change Management and Adoption Patterns",
        "content": (
            "Successful AI transformation requires structured change management: "
            "1. Executive sponsorship: Teams with C-suite champion are 2.4× more likely to succeed. "
            "2. Change resistance: 68% of engineers initially resist AI tooling — overcome with 'AI as assistant' framing. "
            "3. Training investment: 20 hours per engineer for AI tool proficiency delivers full ROI in 6 months. "
            "4. Pilot → scale pattern: Start with 1 team, 2 sprints pilot, measure velocity gain, then scale. "
            "5. Skills evolution: 3 new roles emerge — AI Product Owner, AI Quality Engineer, AI Platform Engineer. "
            "6. Cultural metrics: Psychological safety score must be >7/10 for AI adoption to succeed. "
            "Organizations skipping change management fail AI transformation at 4× the rate of those who invest."
        ),
        "tags": ["change management", "adoption", "transformation", "culture", "training", "executive", "pilot"],
        "source": "McKinsey AI Transformation Research 2024"
    },

    # ── Agent Capability Benchmarks ──────────────────────────────────
    {
        "id": "ai-agent-code-review",
        "category": "AI Agent Capabilities",
        "title": "ReviewAgent — AI Code Review Performance",
        "content": (
            "AI code review agents reduce review wait time by 70% (from avg 24h to <8h). "
            "Process time reduction: 40%. False positive rate: 8–12%. "
            "Coverage: syntax, security hotspots, code smells, performance anti-patterns, logic errors. "
            "Adoption rate in enterprise: 34% of Fortune 500 using AI-assisted code review by 2024. "
            "Tools: GitHub Copilot, Amazon CodeWhisperer, SonarCloud AI, Qodo (formerly CodiumAI). "
            "Best-in-class: 92% defect detection rate, 3-minute review turnaround for standard changes."
        ),
        "tags": ["code review", "review agent", "wait time", "process time", "ai tool", "defect detection"],
        "source": "Gartner AI Engineering Research 2024"
    },
    {
        "id": "ai-agent-test-automation",
        "category": "AI Agent Capabilities",
        "title": "TestGen Agent — AI Test Generation Performance",
        "content": (
            "AI test generation achieves 60–80% unit test coverage automatically. "
            "Reduces test writing effort by 50–70%. E2E test maintenance reduced by 40% with self-healing locators. "
            "Tools: Diffblue Cover (Java), Copilot (multi), Applitools (visual), Mabl (E2E). "
            "Performance testing: AI-driven load scenarios reduce test scripting time by 75%. "
            "ROI: Teams using AI test generation ship 2× faster with 30% fewer production defects. "
            "AI mutation testing identifies test gaps with 95% accuracy, improving overall suite effectiveness."
        ),
        "tags": ["test generation", "test automation", "coverage", "e2e", "performance testing", "mutation"],
        "source": "Gartner AI Engineering Research 2024"
    },
    {
        "id": "ai-agent-deployment",
        "category": "AI Agent Capabilities",
        "title": "AI Deployment Agent — Continuous Delivery Performance",
        "content": (
            "AI-powered deployment pipelines reduce release preparation from days to hours. "
            "Canary deployment with automated rollback reduces CFR from 15% to 3%. "
            "Zero-downtime deployment achievable with blue/green + feature flags. "
            "AI release manager automates CAB approval for standard changes, reducing approval time from 5 days to 2 hours. "
            "Mean deployment time (commit to production): elite teams achieve 23 minutes median. "
            "Progressive delivery adoption increases release confidence by 78%, reducing release anxiety significantly."
        ),
        "tags": ["deployment", "release", "canary", "blue green", "feature flags", "cab", "approval", "progressive"],
        "source": "Gartner Magic Quadrant DevOps 2024"
    },
    {
        "id": "ai-agent-incident",
        "category": "AI Agent Capabilities",
        "title": "IncidentAgent — AIOps Performance Benchmarks",
        "content": (
            "AIOps platforms reduce alert noise by 85–95%, from thousands of alerts to actionable signals. "
            "MTTD improved from 45 minutes to under 5 minutes with anomaly detection. "
            "MTTR reduced by 55–70% with automated runbook execution. "
            "Root cause analysis accuracy: 75–85% for known failure patterns. "
            "Vendors: Dynatrace Davis AI, Moogsoft, BigPanda, Splunk ITSI. "
            "Predictive failure detection: 65% of incidents prevented before user impact with ML models."
        ),
        "tags": ["incident", "aiops", "mttd", "mttr", "alert noise", "root cause", "monitoring", "predictive"],
        "source": "Gartner AIOps Market Guide 2024"
    },
    {
        "id": "ai-agent-security-sast-dast",
        "category": "AI Agent Capabilities",
        "title": "AI Security Agent — SAST/DAST/SCA Automation Performance",
        "content": (
            "AI-powered security scanning in CI/CD pipeline: "
            "SAST (Static Analysis): AI reduces false positive rate from 40% to 12%, scan time from 2h to 8 minutes. "
            "DAST (Dynamic Analysis): AI generates 3× more attack scenarios, 65% faster execution. "
            "SCA (Software Composition): Real-time vulnerability detection with 99.2% OSS coverage. "
            "Secret detection: AI catches hardcoded credentials with 94% accuracy before commit. "
            "Security debt reduction: Teams using AI security achieve 70% fewer critical CVEs in production. "
            "Tools: Checkmarx One, Veracode, Snyk, GitHub Advanced Security, SonarQube."
        ),
        "tags": ["security", "sast", "dast", "sca", "vulnerability", "shift-left", "compliance", "cve"],
        "source": "Forrester Security Automation Research 2024"
    },
    {
        "id": "ai-agent-code-generation",
        "category": "AI Agent Capabilities",
        "title": "CodeGen Agent — AI Code Generation and Developer Productivity",
        "content": (
            "AI code generation (GitHub Copilot, Cursor, Claude Code, Amazon Q): "
            "Developer velocity improvement: 35–55% increase in story points per sprint. "
            "Code acceptance rate: 30–40% of AI suggestions accepted without modification. "
            "Boilerplate reduction: 80% of repetitive patterns auto-generated. "
            "Documentation generation: AI writes docstrings, README, API docs 10× faster. "
            "Code quality: AI-generated code has 15% fewer bugs than manually written code in controlled studies. "
            "ROI: $50K–$120K annual developer productivity savings per 10 engineers at senior rate. "
            "Best use cases: API integration, CRUD operations, test stubs, data transformation, config generation."
        ),
        "tags": ["code generation", "developer productivity", "copilot", "velocity", "story points", "roi"],
        "source": "Gartner Developer Productivity Research 2024"
    },

    # ── Industry-Specific Benchmarks ─────────────────────────────────
    {
        "id": "industry-healthcare",
        "category": "Industry Benchmarks",
        "title": "Healthcare/Insurance Software Delivery Benchmarks",
        "content": (
            "Healthcare/insurance sector DORA profile: 72% are medium performers, 18% high, 10% elite. "
            "Average lead time: 3–6 weeks. Deployment frequency: bi-weekly to monthly. "
            "Key constraints: HIPAA/HITRUST compliance, FDA validation, change management boards. "
            "Compliance as code reduces audit preparation from 6 weeks to 3 days. "
            "Automated security scanning mandatory. Average test coverage: 55%. "
            "Humana, Optum, Cigna benchmark: weekly deployments, 14-day lead time. "
            "Flow efficiency average: 18–22%. Primary bottleneck: manual UAT (Phase 5) and release approval (Phase 6)."
        ),
        "tags": ["healthcare", "insurance", "hipaa", "compliance", "humana", "benchmark", "flow efficiency"],
        "source": "DORA Industry Segmentation 2024"
    },
    {
        "id": "industry-financial",
        "category": "Industry Benchmarks",
        "title": "Financial Services Software Delivery Benchmarks",
        "content": (
            "Financial services DORA profile: 65% medium, 25% high, 10% elite. "
            "Lead time average: 2–4 weeks. Deployment frequency: weekly to bi-weekly. "
            "Key constraints: PCI-DSS, SOX, Basel compliance; strict change management; mainframe legacy. "
            "Automated compliance gate adoption growing: 48% of Tier-1 banks by 2024. "
            "Mean deployment time: 2.5 days. Test automation coverage: 60%. "
            "Progressive delivery (canary/feature flags) adopted by 35% of financial institutions. "
            "Flow efficiency average: 20–28%. Biggest gain opportunity: automating CAB/change approval process."
        ),
        "tags": ["financial services", "banking", "pci", "sox", "compliance", "mainframe", "flow efficiency"],
        "source": "DORA Industry Segmentation 2024"
    },
    {
        "id": "industry-retail-ecommerce",
        "category": "Industry Benchmarks",
        "title": "Retail/E-commerce Software Delivery Benchmarks",
        "content": (
            "Retail/e-commerce DORA profile: 45% high performers, 35% medium, 20% elite. "
            "Lead time: 1–7 days. Deployment frequency: daily to multiple times per day. "
            "Key constraints: seasonal peaks, payment security (PCI), mobile-first requirements. "
            "Feature flag usage: 85% of major retailers use feature flags for zero-downtime releases. "
            "A/B testing integration: 92% of elite retail teams integrate experimentation with CI/CD. "
            "Flow efficiency: 35–55% — significantly higher than healthcare/financial. "
            "Best practice: microservices + event-driven architecture enables independent team deployments."
        ),
        "tags": ["retail", "ecommerce", "feature flags", "a/b testing", "microservices", "flow efficiency"],
        "source": "DORA Industry Segmentation 2024"
    },

    # ── DevOps Maturity ───────────────────────────────────────────────
    {
        "id": "devops-maturity-cultural",
        "category": "DevOps Maturity",
        "title": "Cultural Dimension — DevOps Maturity Scoring Criteria",
        "content": (
            "Cultural maturity in DevOps spans collaboration, shared ownership, psychological safety, and continuous learning. "
            "PRE-CRAWL (1-2): Siloed teams, blame culture, no shared responsibility, waterfall mindset. "
            "CRAWL (3-4): Basic agile adoption, some cross-functional teams, retrospectives starting. "
            "WALK (5-6): Shared ownership of production, blameless post-mortems, regular retrospectives with action. "
            "RUN (7-8): 'You build it, you run it' model, strong psychological safety, cross-team collaboration. "
            "FLY (9-10): Learning organization, AI-augmented teams, culture of experimentation, 20% innovation time. "
            "Key cultural metrics: team NPS, mean time to detect (cultural), deployment anxiety score, "
            "blameless retrospective adoption rate, internal developer platform satisfaction score."
        ),
        "tags": ["devops maturity", "cultural", "collaboration", "psychological safety", "blameless", "agile", "retrospective"],
        "source": "DevOps Research & Assessment Framework 2024"
    },
    {
        "id": "devops-maturity-technical",
        "category": "DevOps Maturity",
        "title": "Technical Dimension — DevOps Maturity Assessment Criteria",
        "content": (
            "Technical maturity in DevOps spans source control, CI/CD, testing, security, and architecture. "
            "PRE-CRAWL: No version control or basic SCCS, manual builds, no automated tests. "
            "CRAWL: Git with branches, basic CI (Jenkins/GitHub Actions), unit tests only, manual deployments. "
            "WALK: Feature flags, automated testing (>50%), IaC (Terraform/Ansible), container adoption. "
            "RUN: Trunk-based development, test coverage >80%, GitOps, microservices, shift-left security. "
            "FLY: AI-assisted development, autonomous testing, self-healing infrastructure, chaos engineering, "
            "eBPF observability, service mesh, zero-trust architecture, automated compliance as code. "
            "Technical debt index: RUN teams maintain <15% of sprint capacity on tech debt reduction."
        ),
        "tags": ["devops maturity", "technical", "ci/cd", "testing", "infrastructure as code", "gitops", "security", "microservices"],
        "source": "DevOps Research & Assessment Framework 2024"
    },
    {
        "id": "devops-maturity-measurement",
        "category": "DevOps Maturity",
        "title": "Measurement Dimension — DevOps Maturity KPIs and Instrumentation",
        "content": (
            "Measurement maturity spans telemetry, dashboards, SLOs, and data-driven decisions. "
            "PRE-CRAWL: No production monitoring, reactive firefighting, no SLAs defined. "
            "CRAWL: Basic uptime monitoring, application logs, manual reporting, spreadsheet dashboards. "
            "WALK: APM tooling (Datadog/New Relic), SLOs defined, distributed tracing, automated alerts. "
            "RUN: Full observability (logs/traces/metrics), SLO-based incident management, AI-assisted anomaly detection. "
            "FLY: Continuous experimentation with automated measurement, real-time business KPI correlation, "
            "predictive analytics for capacity and reliability, golden signals everywhere. "
            "Key KPIs to track: deployment frequency, lead time, MTTR, CFR, change volume, service reliability."
        ),
        "tags": ["devops maturity", "measurement", "observability", "slo", "monitoring", "telemetry", "kpi", "dashboards"],
        "source": "DevOps Research & Assessment Framework 2024"
    },
    {
        "id": "devops-maturity-process",
        "category": "DevOps Maturity",
        "title": "Process Dimension — DevOps Maturity Pipeline and Workflow",
        "content": (
            "Process maturity in DevOps spans planning, change management, incident management, and release processes. "
            "PRE-CRAWL: Ad-hoc releases, no change control, incidents handled manually, no runbooks. "
            "CRAWL: Basic ITSM, scheduled releases, CAB for all changes, basic incident management. "
            "WALK: Automated standard change approval, risk-based release scheduling, documented runbooks. "
            "RUN: Continuous delivery with automated gates, self-service deployment, AIOps for incidents, "
            "value stream mapping integrated with sprint metrics. "
            "FLY: Autonomous deployment pipelines, ML-driven change risk assessment, predictive incident prevention, "
            "closed-loop feedback between production signals and backlog prioritization. "
            "Industry standard: ITIL 4 stream-aligned teams, value stream operations, platform engineering."
        ),
        "tags": ["devops maturity", "process", "change management", "release", "incident", "itil", "itsm", "pipeline"],
        "source": "DevOps Research & Assessment Framework 2024"
    },

    # ── Contextualization Best Practices ─────────────────────────────
    {
        "id": "context-vsm-dora-calibration",
        "category": "Contextualization",
        "title": "DORA Metric to VSM Phase Calibration",
        "content": (
            "DORA metrics map to VSM phases: "
            "Deployment Frequency → Phase 6 (Continuous Delivery) wait time calibration. "
            "Lead Time for Change → Phases 3-6 aggregate lead time. "
            "Change Failure Rate → Phase 5 rework factor (each 5% CFR = 1.2× phase 5 effort). "
            "MTTR → Phase 7 (Monitoring & Feedback) process and wait time. "
            "Build Duration → Phase 4 (Continuous Integration) process time. "
            "Code Review Hours → Phase 3 wait time calibration. "
            "Test Coverage % → Phase 5 automated regression confidence. "
            "When all 4 DORA metrics are provided, VSM accuracy improves by 23% on average."
        ),
        "tags": ["dora", "calibration", "vsm", "phase", "deployment", "lead time", "cfr", "mttr", "accuracy"],
        "source": "PDLC VSM Methodology"
    },
    {
        "id": "context-improvement-roi",
        "category": "Contextualization",
        "title": "AI Improvement ROI by Activity Type",
        "content": (
            "ROI of AI automation by activity: "
            "Code generation (CodeGen Agent): 35% PT reduction, 0% WT, effort reduced 50%. "
            "Test generation (TestGen): 60% PT reduction, 85% WT reduction. "
            "Code review (ReviewAgent): 40% PT, 70% WT reduction. "
            "Performance testing (AI Perf Analyzer): 75% PT, 60% WT reduction. "
            "SIT/UAT (AI UAT Assistant): 50% PT, 80% WT reduction. "
            "Infrastructure as Code: 60% PT, 90% WT reduction. "
            "Incident management (IncidentAgent): 55% PT, 70% WT reduction. "
            "SAST (AI SAST): 40% PT, 60% WT reduction. "
            "DAST (AI DAST): 50% PT, 65% WT reduction. "
            "Backlog grooming (AI Product Owner): 30% PT, 40% WT reduction."
        ),
        "tags": ["roi", "automation", "activity", "process time", "wait time", "improvement", "reduction"],
        "source": "AI Transformation Research 2024"
    },
    {
        "id": "context-bottleneck-thresholds",
        "category": "Contextualization",
        "title": "Bottleneck Detection Thresholds and Root Causes",
        "content": (
            "Critical bottleneck thresholds: Wait time >16h = critical severity, >8h = high. "
            "Effort >20h = critical, >12h = high. Flow efficiency <15% = critical bottleneck. "
            "Root cause patterns: "
            "High wait time in Phase 5 → environment provisioning, test data dependency, manual signoff gates. "
            "High wait time in Phase 2 → design review queues, stakeholder availability, sequential approvals. "
            "High wait time in Phase 6 → CAB process, environment promotion queues, release train scheduling. "
            "High effort in Phase 5 → low test automation (<40%), rework from defect escapes, broad manual regression. "
            "High effort in Phase 3 → large PRs (>500 lines), insufficient reviewer capacity, complex merge conflicts. "
            "Systemic bottleneck indicator: same phase appearing in top-3 bottlenecks for 3+ consecutive sprints."
        ),
        "tags": ["bottleneck", "threshold", "root cause", "wait time", "flow efficiency", "testing", "release", "phase"],
        "source": "PDLC VSM Methodology"
    },
    {
        "id": "context-playbook-implementation",
        "category": "Contextualization",
        "title": "Transformation Playbook — Implementation Patterns and Sprint Structure",
        "content": (
            "Proven implementation playbook for PDLC VSM transformation: "
            "Sprint 1-2 (Foundation): Set up developer portal, establish golden path, configure observability. "
            "Sprint 3-4 (Automation Wave 1): Implement AI code review, automated security scanning, test generation. "
            "Sprint 5-6 (Pipeline Optimization): Progressive delivery, automated CAB for standard changes, IaC rollout. "
            "Sprint 7-8 (Testing Transformation): AI test generation, environment-on-demand, shift-left security. "
            "Sprint 9-10 (AI Amplification): Full AI augmentation layer, AIOps, autonomous deployment. "
            "Success criteria per sprint: measured velocity increase, reduced DORA metrics, team satisfaction. "
            "RACI model: Product Owner (responsible), Engineering Lead (accountable), DevOps Engineer (contributor), "
            "CISO (informed for security changes), Architecture (consulted for platform decisions)."
        ),
        "tags": ["playbook", "implementation", "sprint", "foundation", "automation", "raci", "transformation"],
        "source": "PDLC VSM Methodology"
    },
    {
        "id": "context-business-case-roi",
        "category": "Contextualization",
        "title": "Business Case ROI Calculation Model for PDLC Transformation",
        "content": (
            "ROI calculation framework for PDLC transformation: "
            "Cost avoidance: Defect reduction × average fix cost ($5K per production defect). "
            "Developer productivity: (Velocity increase %) × team size × $150K average annual cost. "
            "Lead time value: Revenue impact of faster feature delivery × market opportunity size. "
            "MTTR savings: Outage duration reduction × revenue per hour × incident frequency. "
            "Technical debt reduction: 15% capacity freed × team size × annual cost. "
            "Formula: Annual Benefits = (Productivity savings) + (Defect avoidance) + (Lead time revenue) + (MTTR savings). "
            "ROI multiple = (Annual Benefits × Investment period years) / Total Investment. "
            "Industry average ROI multiple: Option A 2.8×, Option B 3.8×, Option C 5.5× over 3 years."
        ),
        "tags": ["business case", "roi", "calculation", "cost avoidance", "productivity", "defect", "lead time", "payback"],
        "source": "PDLC VSM Methodology"
    },
]

# Category index for fast lookup
KB_BY_CATEGORY = {}
for doc in KB_DOCUMENTS:
    cat = doc["category"]
    if cat not in KB_BY_CATEGORY:
        KB_BY_CATEGORY[cat] = []
    KB_BY_CATEGORY[cat].append(doc)

KB_CATEGORIES = list(KB_BY_CATEGORY.keys())
