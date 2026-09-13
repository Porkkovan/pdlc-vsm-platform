"""
DevOps Maturity Assessment Questions
73 questions across 4 dimensions: Cultural, Measurement, Process, Technical
Scoring: L1 Foundation (1-2), L2 Augmentation (3-4), L3 Automation (5-6), L4 Transformation (7-8), L5 Reinvention (9-10)
Aligned to ADLC L1-L5 Maturity Ladder
"""

MATURITY_BANDS = {
    "PRE_CRAWL": {"range": "1-2", "label": "L1 — Foundation",     "color": "#ef4444"},
    "CRAWL":     {"range": "3-4", "label": "L2 — Augmentation",   "color": "#f97316"},
    "WALK":      {"range": "5-6", "label": "L3 — Automation",     "color": "#eab308"},
    "RUN":       {"range": "7-8", "label": "L4 — Transformation", "color": "#22c55e"},
    "FLY":       {"range": "9-10","label": "L5 — Reinvention",    "color": "#3b82f6"},
}

# Data source types for auto-scoring
SOURCE_TYPES = {
    "jira":          {"label": "Jira / ALM",              "icon": "🎯", "metrics": ["sprint_velocity", "cycle_time", "defect_rate", "wip", "lead_time"]},
    "github":        {"label": "GitHub / GitLab / Bitbucket","icon": "🔧","metrics": ["commit_freq", "pr_size", "review_time", "branch_strategy", "coverage"]},
    "cicd":          {"label": "CI/CD Pipeline (Jenkins/GHA)","icon": "⚙️","metrics": ["build_time", "build_success_rate", "deploy_freq", "pipeline_stages"]},
    "sonarqube":     {"label": "SonarQube / Code Quality", "icon": "🔍", "metrics": ["coverage", "bugs", "vulnerabilities", "code_smells", "duplication"]},
    "release_mgmt":  {"label": "Release Management Portal","icon": "🚀", "metrics": ["deploy_freq", "mttr", "cfr", "change_lead_time"]},
    "risk_portal":   {"label": "Digital Risk Assessment",  "icon": "🛡️", "metrics": ["security_posture", "compliance_score", "risk_items"]},
    "itsm":          {"label": "ServiceNow / ITSM",        "icon": "🎫", "metrics": ["mttr", "mttd", "incident_count", "change_success_rate"]},
    "monitoring":    {"label": "Monitoring (Dynatrace/Splunk)","icon": "📡","metrics": ["alert_noise", "observability_coverage", "slo_compliance"]},
    "confluence":    {"label": "Confluence / Wiki",        "icon": "📄", "metrics": ["doc_coverage", "runbooks", "architecture_docs"]},
    "oncall":        {"label": "PagerDuty / OpsGenie",     "icon": "🔔", "metrics": ["incident_response_time", "escalation_rate", "mttr"]},
}

QUESTIONS = [
    # ═══════════════════════════════════════════════════════════════════
    # CULTURAL DIMENSION (9 questions)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "C1",
        "dimension": "Cultural",
        "competency": "Collective Ownership",
        "humana_capability": "Talent and Community",
        "humana_sub_capability": "Collective Code Ownership",
        "question": "Does the team practice collective code ownership where any team member can modify any part of the codebase, and is there shared accountability for quality and reliability?",
        "data_sources": ["github", "jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Siloed ownership — individuals own specific modules/services. Knowledge hoarding is common. Bus-factor is high (1-2 people own critical paths). Code reviews are rare or absent.",
            "3-4": "Some shared ownership emerging. Teams discuss cross-component changes. A few 'go-to' people but others can contribute. Code reviews exist but are inconsistent.",
            "5-6": "Team actively shares knowledge. Rotating responsibilities practiced. Code reviews are standard. Documentation covers most critical areas. Bus-factor reduced to 3+.",
            "7-8": "Strong collective ownership culture. Any team member can make changes anywhere. Pair programming or mob programming practiced regularly. Low bus-factor across all areas.",
            "9-10": "Fully collective ownership. No knowledge silos. Team rotates roles (on-call, lead, architect) seamlessly. Continuous documentation. External teams seek collaboration. Bus-factor > 5 everywhere."
        }
    },
    {
        "id": "C2",
        "dimension": "Cultural",
        "competency": "Cross-functional Collaboration",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Cross-functional Teams",
        "question": "How effectively do development, operations, security, and QA teams collaborate daily — from planning through production?",
        "data_sources": ["jira", "confluence"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Siloed teams with hand-off culture. Dev 'throws over the wall' to Ops. Security is an afterthought at end of cycle. QA is a separate gate. No shared goals.",
            "3-4": "Some cross-team meetings exist. Joint retrospectives occasionally. Security consulted during design (not embedded). Shared sprint goals emerging but not consistent.",
            "5-6": "Integrated teams with shared ceremonies. Security participates in sprint planning. Ops involved in design decisions. Shared on-call rotations beginning. Team charters defined.",
            "7-8": "Full DevSecOps teams — Dev, Ops, Security, QA collocated or in same sprint. Shared OKRs tied to customer outcomes. Security champions embedded. Joint incident response.",
            "9-10": "Fully integrated product teams. No functional silos. Security, Ops, Data embedded. External stakeholders (business, UX) participate in ceremonies. Team is self-organizing and optimizing."
        }
    },
    {
        "id": "C3",
        "dimension": "Cultural",
        "competency": "Transformational Leadership",
        "humana_capability": "Talent and Community",
        "humana_sub_capability": "Leadership Support",
        "question": "Does leadership actively champion DevOps transformation, remove impediments, and create psychological safety for experimentation and failure?",
        "data_sources": ["confluence", "jira"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Leadership views DevOps as an IT initiative only. Blame culture exists. Failure is punished. Investment in transformation is minimal or zero. Command-and-control management style.",
            "3-4": "Leadership acknowledges DevOps value. Some funding allocated. Transformation is top-down directive but not servant leadership. Blame culture softening but still present.",
            "5-6": "Leadership sponsors transformation actively. Regular impediment removal reviews. Beginning to create safety for experimentation. Some innovation time allocated (e.g., 10%).",
            "7-8": "Leadership demonstrates servant leadership. Team autonomy respected. Failure is treated as learning. Innovation budgets exist. Leaders participate in gemba walks. OKRs set at team level.",
            "9-10": "Leadership is a transformation accelerator. Full psychological safety. Leaders participate in retrospectives. Strategy co-created with teams. Continuous investment in capability building."
        }
    },
    {
        "id": "C4",
        "dimension": "Cultural",
        "competency": "Impediment Management",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Impediment Removal Speed",
        "question": "How quickly are team impediments identified, escalated, and resolved — and is there a systematic process for impediment management?",
        "data_sources": ["jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No formal impediment tracking. Issues surfaced ad-hoc or not at all. Resolution depends on individual relationships. Average resolution time > 2 weeks.",
            "3-4": "Impediments tracked in backlog or Jira. Scrum Master escalates. Average resolution 1-2 weeks. Some systemic issues repeat without root cause fix.",
            "5-6": "Dedicated impediment board visible to all. Weekly review. SLAs for escalation exist. Average resolution < 1 week. Root cause analysis for recurring issues.",
            "7-8": "Real-time impediment tracking. Average resolution < 3 days. Leadership reviews weekly. Systemic patterns identified and addressed structurally. Team empowered to resolve most autonomously.",
            "9-10": "Impediments resolved in < 24 hours on average. Proactive identification before they block work. Self-organizing team resolves 90%+ without escalation. Systemic improvements visible quarter-over-quarter."
        }
    },
    {
        "id": "C5",
        "dimension": "Cultural",
        "competency": "Learning Culture",
        "humana_capability": "Talent and Community",
        "humana_sub_capability": "Psychological Safety & Risk Taking",
        "question": "Does the team encourage experimentation, treat failures as learning opportunities, and have structured mechanisms for knowledge sharing and continuous improvement?",
        "data_sources": ["confluence", "jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Risk-averse culture. Failure is blamed. No time for learning. Knowledge sharing is accidental. No blameless post-mortems. Change is feared.",
            "3-4": "Some learning activities. Retrospectives exist but action items often not completed. Occasional post-mortems. Training budget exists but not used proactively.",
            "5-6": "Blameless post-mortems practiced. Learning from incidents is standard. Innovation spikes occasionally. Communities of practice forming. Knowledge base being built.",
            "7-8": "Structured learning culture. Regular hackathons/innovation time. CoPs active with monthly events. Post-mortems drive systemic improvements. External conference participation encouraged.",
            "9-10": "Learning is central to team identity. Continuous experimentation built into delivery. Team publishes internal and external case studies. Contributes to open source. Coaches other teams."
        }
    },
    {
        "id": "C6",
        "dimension": "Cultural",
        "competency": "Incident Response Culture",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Issue Resolution",
        "question": "How does the team respond to production incidents — is there a shared sense of urgency, clear roles, and blameless culture that drives rapid recovery?",
        "data_sources": ["itsm", "oncall", "monitoring"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Incident response is chaotic. No clear roles. Blame assigned to individuals. War rooms are unstructured. Recovery is manual and slow. Post-mortems rare or punitive.",
            "3-4": "Basic incident response process. On-call rotation exists. Runbooks for some incidents. Blame softening. Some post-mortems. MTTR measured but not improving.",
            "5-6": "Structured incident management. Clear commander/communicator roles. Blameless post-mortems standard. Runbooks cover 60%+ of incidents. MTTR trending down.",
            "7-8": "Automated incident detection and triage. Self-healing capabilities for common failures. Blameless culture fully established. Post-mortem action items tracked to completion. MTTR < 1 hour for most incidents.",
            "9-10": "Proactive reliability engineering. Chaos engineering practiced. Mean time to detect < 5 min. Mean time to recover < 15 min. Post-mortems feed continuous improvement. Team presents at external conferences."
        }
    },
    {
        "id": "C7",
        "dimension": "Cultural",
        "competency": "Quality Culture",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Defect Prevention",
        "question": "Does the team prioritize defect prevention over defect detection — is quality built into the process rather than tested in at the end?",
        "data_sources": ["sonarqube", "jira", "github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Quality is QA's job. Defects found in production frequently. Testing is an end-stage gate. Technical debt is not tracked. Code quality metrics not measured.",
            "3-4": "Unit testing exists but coverage is low (<30%). Code reviews are inconsistent. Quality gates exist in theory but bypassed under pressure. Defect escape rate high.",
            "5-6": "Quality gates enforced in pipeline (coverage >50%). Shift-left testing in place. Definition of Done includes testing. Technical debt board exists. Security scanning integrated.",
            "7-8": "Quality built-in from design. Test coverage > 70%. SAST/DAST/SCA integrated. Zero-defect sprint philosophy. Technical debt actively managed and trending down.",
            "9-10": "Quality is team identity. Coverage > 85%. Mutation testing used. Formal verification for critical paths. Defect escape rate < 0.5%. Quality metrics presented to stakeholders."
        }
    },
    {
        "id": "C8",
        "dimension": "Cultural",
        "competency": "Job Satisfaction",
        "humana_capability": "Talent and Community",
        "humana_sub_capability": "Team Engagement",
        "question": "How satisfied is the team with their current engineering practices, tooling, and delivery process — and do they feel empowered to improve it?",
        "data_sources": ["confluence"],
        "weight": 1,
        "scoring_criteria": {
            "1-2": "Team is frustrated. High toil, poor tooling, bureaucratic processes. High turnover. Low eNPS. Team feels powerless to change their working practices.",
            "3-4": "Mixed satisfaction. Some pain points acknowledged. Some tooling improvements made. Team can raise issues but changes are slow. eNPS is neutral.",
            "5-6": "Generally positive team sentiment. Team has autonomy over some tooling choices. Improvement cycles happen each quarter. eNPS positive. Toil measured and reducing.",
            "7-8": "High team satisfaction. Engineers proud of their delivery practices. Regular tooling investment. Team has budget for improvements. Low toil. eNPS strongly positive.",
            "9-10": "Exceptional team satisfaction. Team is externally recognized for engineering excellence. Attracts top talent. eNPS > 50. Team contributes to platform and tooling for other teams."
        }
    },
    {
        "id": "C9",
        "dimension": "Cultural",
        "competency": "Community Engagement",
        "humana_capability": "Talent and Community",
        "humana_sub_capability": "Community of Practice",
        "question": "Does the team actively participate in Communities of Practice and contribute to organizational DevOps capability building beyond their own team?",
        "data_sources": ["confluence"],
        "weight": 1,
        "scoring_criteria": {
            "1-2": "No CoP participation. Team is isolated. No knowledge sharing with other teams. Reinventing the wheel is common. Not contributing to shared platforms or practices.",
            "3-4": "Aware of CoPs. Occasionally participates. Some sharing of internal blog posts or wiki articles. Reuses some shared components but doesn't contribute back.",
            "5-6": "Active CoP member. Presents in CoP meetings occasionally. Contributes reusable components to shared platform. Participates in cross-team retrospectives.",
            "7-8": "CoP champion. Regularly presents learnings. Contributes to internal developer platform. Mentors other teams. Published case studies on intranet.",
            "9-10": "Community leader. Runs CoPs or working groups. Contributes to open source. Speaks at industry events. Drives organizational DevOps standards. Recognized as center of excellence."
        }
    },

    # ═══════════════════════════════════════════════════════════════════
    # MEASUREMENT DIMENSION (11 questions)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "M1",
        "dimension": "Measurement",
        "competency": "Recovery Metrics",
        "humana_capability": "DevOps",
        "humana_sub_capability": "MTTR Measurement",
        "question": "Is Mean Time to Recovery (MTTR) tracked, visible to the team, and demonstrably improving over time?",
        "data_sources": ["itsm", "oncall", "monitoring", "release_mgmt"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "MTTR is not tracked. Recovery time is unknown and highly variable. No baseline exists.",
            "3-4": "MTTR tracked manually post-incident. Reported monthly. No trend analysis. MTTR > 24 hours average.",
            "5-6": "MTTR tracked automatically from monitoring tools. Available in dashboard. Quarterly trend review. MTTR 1-24 hours.",
            "7-8": "MTTR < 1 hour average. Real-time dashboard. Team reviews weekly. Active reduction program. MTTR trending down 20%+ per quarter.",
            "9-10": "MTTR < 15 minutes for most incident categories. Automated recovery for known failure patterns. MTTR by service/severity visible. Published SLOs tied to MTTR."
        }
    },
    {
        "id": "M2",
        "dimension": "Measurement",
        "competency": "Monitoring Coverage",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Application Monitoring",
        "question": "Is comprehensive application monitoring in place covering infrastructure, application performance, business metrics, and user experience?",
        "data_sources": ["monitoring", "release_mgmt"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Basic infrastructure monitoring only (CPU/memory). No application-level monitoring. Issues reported by end users. No alerting.",
            "3-4": "Application monitoring for critical paths. Basic alerting. Some dashboards. Business metrics tracked separately in spreadsheets. Alert noise is high.",
            "5-6": "APM tool in place (Dynatrace/New Relic/AppDynamics). Dashboards per service. Alerting with some runbooks. Business KPIs connected to technical metrics.",
            "7-8": "Full observability: logs, metrics, traces correlated. SLOs/SLIs defined per service. Anomaly detection active. User journey monitoring. Alert noise < 20% false positives.",
            "9-10": "AIOps-powered monitoring. Predictive alerts before user impact. Full distributed tracing. Business and technical metrics unified. SLO compliance > 99.9%. Automated remediation for common alerts."
        }
    },
    {
        "id": "M3",
        "dimension": "Measurement",
        "competency": "Quality Metrics",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Defect Density",
        "question": "Is defect density tracked per sprint/release, with root cause analysis driving systemic quality improvements?",
        "data_sources": ["jira", "sonarqube"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Defect count tracked but not normalized (per feature point or story). No trend analysis. Root causes not investigated.",
            "3-4": "Defect density measured per sprint. Monthly reports. Some root cause analysis. No systemic improvement program.",
            "5-6": "Defect density by component/service. Trending weekly. Root cause categories tracked. Top 3 sources addressed each quarter.",
            "7-8": "Defect density < 1 per sprint. Real-time quality dashboard. Root cause analysis drives process improvements. Defect prevention metrics (escaped defects) tracked.",
            "9-10": "Near-zero defect density. Predictive quality model identifies high-risk changes. Defect prevention > 95%. Quality metrics tied to team OKRs."
        }
    },
    {
        "id": "M4",
        "dimension": "Measurement",
        "competency": "Process Effectiveness",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Flow Metrics",
        "question": "Are process flow metrics (cycle time, lead time, flow efficiency) measured and used to drive continuous improvement?",
        "data_sources": ["jira", "release_mgmt"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "No flow metrics. Velocity tracked but cycle time and lead time unknown. No visibility into wait time vs. active work.",
            "3-4": "Cycle time measured in Jira. Lead time tracked manually. Flow efficiency unknown. Metrics reviewed monthly.",
            "5-6": "Cycle time, lead time, and throughput measured. Flow efficiency calculated. Weekly reviews. Bottlenecks identified from data.",
            "7-8": "Full flow metrics suite. Real-time Kanban flow board. Monte Carlo forecasting used. Flow efficiency > 40%. Metrics drive sprint planning.",
            "9-10": "Predictive flow analytics. ML-assisted forecasting. Flow efficiency > 60%. Continuous flow (not sprints) for some work types. Metrics published to stakeholders."
        }
    },
    {
        "id": "M5",
        "dimension": "Measurement",
        "competency": "WIP Management",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "WIP Limits",
        "question": "Are Work-In-Progress (WIP) limits enforced at team and individual levels, and is the team disciplined about not starting new work when WIP limits are reached?",
        "data_sources": ["jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No WIP limits. Team members juggle 5+ concurrent items. Context switching is constant. No awareness of WIP impact on flow.",
            "3-4": "WIP limits defined but frequently violated. Team knows the concept. Some discipline. Average WIP 3-5 items per person.",
            "5-6": "WIP limits enforced in sprints. Team respects limits mostly. WIP per person typically 2-3. Blocker resolution prioritized over new starts.",
            "7-8": "Strict WIP limits. Team stops starting and starts finishing. WIP per person ≤ 2. Pull-based system. WIP violations tracked and reviewed.",
            "9-10": "WIP limits embedded in culture. Team naturally finishes before starting. Average WIP per person ≤ 1.5. Flow optimization over utilization optimization."
        }
    },
    {
        "id": "M6",
        "dimension": "Measurement",
        "competency": "Visual Management",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Dashboards & Radiators",
        "question": "Does the team use visual management dashboards (information radiators) that make team health, delivery status, and quality metrics visible to all stakeholders at a glance?",
        "data_sources": ["jira", "monitoring", "sonarqube"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No dashboards. Status communicated via email or meetings. Stakeholders don't know delivery status without asking.",
            "3-4": "Basic Jira dashboard. Sprint board visible. Some metrics in PowerPoint for leadership. Manual updates required.",
            "5-6": "Automated dashboards for team metrics. DORA metrics visible. Quality gates dashboard. Stakeholders can self-serve status.",
            "7-8": "Real-time dashboards covering DORA, quality, incidents, and team health. Executive-level summary auto-generated. Team radiators in team space.",
            "9-10": "Comprehensive observability platform. Business and technical metrics unified. AI-powered insights surfaced automatically. Stakeholders trust dashboards over status meetings."
        }
    },
    {
        "id": "M7",
        "dimension": "Measurement",
        "competency": "Throughput",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Delivery Throughput",
        "question": "Is team delivery throughput (stories/features per sprint) measured, consistent, and improving?",
        "data_sources": ["jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Throughput not measured. Velocity tracked but inconsistent (±50%). Commitments frequently missed. Stakeholders cannot rely on delivery estimates.",
            "3-4": "Velocity tracked. Inconsistent (±30%). Some analysis of variance. Commitments met 60-70% of the time.",
            "5-6": "Consistent velocity (±20%). Throughput improving trend. Commitment reliability 75-85%. Some forecasting using historical data.",
            "7-8": "High throughput consistency (±15%). Commitment reliability > 85%. Throughput trending up. Capacity planning uses historical throughput.",
            "9-10": "Predictable, high throughput. Commitment reliability > 92%. Monte Carlo-based forecasting. Continuous flow metrics supplement velocity."
        }
    },
    {
        "id": "M8",
        "dimension": "Measurement",
        "competency": "Predictability",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Delivery Predictability",
        "question": "Can the team reliably forecast delivery dates for features and releases based on historical data?",
        "data_sources": ["jira", "release_mgmt"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Delivery dates are guesses. Significant slippage common. Stakeholders have no confidence in estimates.",
            "3-4": "Story point estimation used. Velocity-based forecasting. Accuracy ±40%. Frequent replanning needed.",
            "5-6": "Historical velocity used for forecasting. Accuracy ±25%. Release dates usually met within 1 sprint. Risk tracking improving confidence.",
            "7-8": "Probabilistic forecasting (Monte Carlo). Accuracy ±15%. Date commitments met 85%+ of the time. Risk factors quantified.",
            "9-10": "High predictability. ±10% accuracy. Stakeholders trust delivery commitments. Continuous flow metrics enable real-time forecasting."
        }
    },
    {
        "id": "M9",
        "dimension": "Measurement",
        "competency": "Work Traceability",
        "humana_capability": "DevOps",
        "humana_sub_capability": "End-to-End Traceability",
        "question": "Is there complete end-to-end traceability from business requirement through development to deployment — linking Jira stories to commits, builds, and releases?",
        "data_sources": ["jira", "github", "cicd", "release_mgmt"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No traceability. Cannot determine which feature is in which release. Commits not linked to stories. Compliance audits are manual and slow.",
            "3-4": "Commits reference Jira tickets by convention. Some releases tagged. Partial traceability. Compliance reports possible but manual effort.",
            "5-6": "Automated traceability from Jira to commit to build to release. Release notes auto-generated. Audit trail available. Compliance automated for 60% of requirements.",
            "7-8": "Full traceability across the toolchain. Release content visible in Jira. Compliance reports auto-generated. Security scans linked to stories. 90% compliance automated.",
            "9-10": "Immutable audit trail. Full traceability with cryptographic signing. Compliance reports instant. Regulatory evidence packages auto-generated. Zero manual effort for audits."
        }
    },
    {
        "id": "M10",
        "dimension": "Measurement",
        "competency": "Detection Metrics",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Mean Time to Detect",
        "question": "Is Mean Time to Detect (MTTD) issues tracked, and is the team proactively reducing the time between an issue occurring and its detection?",
        "data_sources": ["monitoring", "itsm", "oncall"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Issues detected by end users. No proactive monitoring. MTTD unknown but likely hours to days.",
            "3-4": "Basic alerting in place. MTTD tracked manually. Average MTTD 1-4 hours. Reactive approach.",
            "5-6": "Automated alerting. MTTD < 30 minutes average. Dashboard visible. Trend tracked monthly.",
            "7-8": "MTTD < 10 minutes. Anomaly detection active. Synthetic monitoring. MTTD by severity tracked. Trending down.",
            "9-10": "MTTD < 2 minutes for critical issues. Predictive alerting before user impact. AI-powered anomaly detection. Near-zero user-reported incidents."
        }
    },
    {
        "id": "M11",
        "dimension": "Measurement",
        "competency": "Feedback Loop Speed",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Build & Test Feedback",
        "question": "How fast are developer feedback loops — time from code commit to getting build, test, and code quality results?",
        "data_sources": ["cicd", "sonarqube", "github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Build takes > 30 minutes. Test feedback takes hours. Developers work on other tasks while waiting. Context switching is constant.",
            "3-4": "Build in 15-30 minutes. Test feedback in 30-60 minutes. Some optimization attempts. Developers still lose context.",
            "5-6": "Build in 10-15 minutes. Fast unit test feedback in < 10 minutes. Integration tests in 30 minutes. Developers mostly stay in flow.",
            "7-8": "Build in < 5 minutes. Full test suite in < 15 minutes. Code quality results instant. Developers maintain flow state.",
            "9-10": "Commit-to-feedback < 2 minutes for critical path. Parallel test execution. Incremental builds. Developer experience optimized as a product."
        }
    },

    # ═══════════════════════════════════════════════════════════════════
    # PROCESS DIMENSION (16 questions)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "P1",
        "dimension": "Process",
        "competency": "Continuous Improvement",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Structured Experimentation",
        "question": "Does the team run structured improvement experiments using data-driven hypotheses, and do retrospective action items consistently get implemented?",
        "data_sources": ["jira", "confluence"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Retrospectives are box-ticking exercises. Action items rarely completed. No experiments. Same problems recur sprint after sprint.",
            "3-4": "Retrospectives happen. Some action items completed (< 50%). Occasional experiments. Improvement is ad-hoc rather than systematic.",
            "5-6": "Retrospectives drive improvement. Action item completion > 70%. Some hypothesis-driven experiments. Quarterly improvement goals set.",
            "7-8": "Data-driven improvement cycle. All retrospective actions tracked to completion. Regular experiments with hypotheses and measurements. Improvement velocity increasing.",
            "9-10": "Continuous improvement is embedded in team DNA. Experiments run every sprint. Improvement metrics on team dashboard. Team coaches others on improvement practices."
        }
    },
    {
        "id": "P2",
        "dimension": "Process",
        "competency": "Change Management",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Streamlined Change Approval",
        "question": "How streamlined is the change approval process — can standard changes be deployed without CAB review, and is change lead time under 1 day?",
        "data_sources": ["itsm", "release_mgmt", "cicd"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "All changes require CAB approval. Manual approval process takes 1-2 weeks. Emergency changes are chaotic. Change success rate < 80%.",
            "3-4": "Standard changes pre-approved in principle but still require ticket and manual review. Approval time 3-5 days. Change success rate 80-90%.",
            "5-6": "Standard changes auto-approved if automated tests pass. CAB for significant changes only. Change lead time < 1 week. Change success rate > 90%.",
            "7-8": "Most changes flow through pipeline without CAB. Automated change record creation. Change lead time < 1 day. Change success rate > 95%. CAB for high-risk only.",
            "9-10": "Fully automated change management. Risk scoring determines approval path. < 5% of changes need human approval. Change lead time < 1 hour. Change success rate > 99%."
        }
    },
    {
        "id": "P3",
        "dimension": "Process",
        "competency": "Customer Feedback",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Customer Feedback Integration",
        "question": "How frequently is real customer feedback gathered, analyzed, and actioned in the delivery process?",
        "data_sources": ["jira", "confluence"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Customer feedback gathered once a year via surveys. Not connected to delivery planning. Team does not interact with customers.",
            "3-4": "User research conducted at project milestones. NPS tracked quarterly. Some feedback incorporated in roadmap planning.",
            "5-6": "Customer feedback loops in place. User interviews monthly. NPS/CSAT tracked. Product analytics used. Feedback influences sprint priorities.",
            "7-8": "Continuous customer feedback loops. Product analytics inform every sprint. A/B tests run for feature decisions. Customer satisfaction a team OKR.",
            "9-10": "Real-time customer signals drive delivery. Automated feedback analysis. Customer journey analytics. Team co-creates features with customers. Customer outcome metrics primary success measure."
        }
    },
    {
        "id": "P4",
        "dimension": "Process",
        "competency": "Experimentation",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "A/B Testing",
        "question": "Does the team use A/B testing, feature flags, and controlled experiments to validate hypotheses before full rollout?",
        "data_sources": ["cicd", "jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No experimentation. Features released to all users simultaneously. No way to test hypotheses with real users. All-or-nothing releases.",
            "3-4": "Feature flags used for some features. Limited A/B testing. Manual experiment analysis. Some canary deployments.",
            "5-6": "Feature flag platform in use. Regular A/B tests for significant features. Experiment results inform product decisions. Canary deployments standard.",
            "7-8": "Comprehensive experimentation platform. A/B tests for most new features. Statistical significance calculated automatically. Multi-variate testing used.",
            "9-10": "Continuous experimentation culture. Most releases are controlled experiments. ML-powered personalization. Automated experiment analysis. Decisions are evidence-based."
        }
    },
    {
        "id": "P5",
        "dimension": "Process",
        "competency": "Retrospective Effectiveness",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Feedback Loops",
        "question": "How effective are team retrospectives — do they surface systemic issues, generate actionable improvements, and produce measurable outcomes?",
        "data_sources": ["jira", "confluence"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Retrospectives skipped under pressure. When held, discussions are superficial. Same issues surface repeatedly. No measurable outcomes.",
            "3-4": "Retrospectives held every sprint. Some good discussions. Action items created but often not prioritized. Improvements hard to measure.",
            "5-6": "Structured retrospectives with varied formats. Action items always assigned and tracked. Improvements measurable. Team sentiment improving.",
            "7-8": "Highly effective retrospectives. Evidence-based discussions using data. Root cause analysis on systemic issues. Action items completed sprint-over-sprint.",
            "9-10": "Retrospectives drive continuous breakthroughs. Team uses multiple improvement frameworks. Systemic improvements visible in metrics. Retrospective techniques shared with other teams."
        }
    },
    {
        "id": "P6",
        "dimension": "Process",
        "competency": "Systems Thinking",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "End-to-End Visibility",
        "question": "Does the team understand and optimize the full value stream end-to-end, including upstream dependencies and downstream impacts?",
        "data_sources": ["jira", "confluence"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Team optimizes locally without end-to-end view. Upstream/downstream impacts not considered. Decisions create downstream bottlenecks.",
            "3-4": "Team is aware of upstream dependencies. Some end-to-end mapping done. Occasional cross-team reviews. Local optimization still dominant.",
            "5-6": "Value stream mapped end-to-end. Cross-team dependencies tracked. Impact analysis for major changes. Regular cross-team reviews.",
            "7-8": "Active systems thinking. Optimization decisions made with end-to-end view. Dependencies proactively managed. Teams collaborate to remove shared bottlenecks.",
            "9-10": "Full systems thinking culture. Team co-owns enterprise value stream improvements. Regularly optimizes across organizational boundaries. Recognized for cross-team impact."
        }
    },
    {
        "id": "P7",
        "dimension": "Process",
        "competency": "Backlog Management",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Unified Product Backlog",
        "question": "Is there a single, prioritized backlog that represents all work (features, technical debt, defects, security, compliance) with clear business value?",
        "data_sources": ["jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Multiple disconnected backlogs. Priorities unclear. Technical debt and security work not visible. Stakeholders have conflicting priority views.",
            "3-4": "Single Jira backlog but poorly maintained. Technical items buried. Priority conflicts common. Refinement inconsistent.",
            "5-6": "Well-maintained single backlog. All work types included. Regular refinement (10% capacity). Business value estimated. Priorities clear and communicated.",
            "7-8": "Optimized backlog with clear value scoring. WSJF or similar framework used. Technical debt and security given dedicated capacity. Stakeholders aligned on priorities.",
            "9-10": "Dynamic backlog with real-time prioritization. Outcome-based stories. Technical health given equal priority to features. Backlog is single source of truth for all stakeholders."
        }
    },
    {
        "id": "P8",
        "dimension": "Process",
        "competency": "Outcome Alignment",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Business Outcomes Focus",
        "question": "Are team delivery objectives aligned to measurable business outcomes (not just output), with clear line-of-sight from team work to business KPIs?",
        "data_sources": ["jira", "confluence"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Team measures output (stories delivered, velocity). No connection to business KPIs. Success = on-time delivery of scope, not business outcomes.",
            "3-4": "Some team OKRs connected to business goals. Product metrics tracked separately. Success criteria exist in stories but not always measurable.",
            "5-6": "Team OKRs include business outcome metrics. Product analytics tracked. Stories have acceptance criteria linked to business metrics. Quarterly business reviews.",
            "7-8": "Strong outcome alignment. DORA + business metrics on same dashboard. Team celebrates business wins not just feature launches. All epics have success metrics.",
            "9-10": "Team is fully outcome-driven. Delivery decisions made against business impact projections. Team can demonstrate ROI per sprint. Business partners consider team strategic asset."
        }
    },
    {
        "id": "P9",
        "dimension": "Process",
        "competency": "Lead Time Reduction",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Lead Time for Change",
        "question": "Is the team actively working to reduce lead time for changes — from idea to production — and is there a measurable improvement trend?",
        "data_sources": ["jira", "release_mgmt", "cicd"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Lead time > 3 months. No measurement. No reduction program. Release cycle is quarterly or longer.",
            "3-4": "Lead time 1-3 months. Measured at release level. Some initiatives to reduce lead time but limited progress.",
            "5-6": "Lead time 2-4 weeks. Measured per story. Active reduction initiatives. Monthly sprint reviews of lead time.",
            "7-8": "Lead time 1-7 days for most changes. Continuous measurement. Active reduction experiments. Lead time trending down 10%+ per quarter.",
            "9-10": "Lead time < 1 day for standard changes. Continuous flow. On-demand deployments. Lead time is a primary team metric. Recognized as industry-leading."
        }
    },
    {
        "id": "P10",
        "dimension": "Process",
        "competency": "Dependency Management",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Cross-team Dependencies",
        "question": "How well does the team identify, track, and proactively manage dependencies on other teams to avoid delivery delays?",
        "data_sources": ["jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Dependencies discovered late, causing delivery delays. No dependency tracking. Cross-team coordination is ad-hoc and reactive.",
            "3-4": "Dependencies tracked in Jira. Some advance notice. Regular cross-team syncs. Dependencies still cause delays frequently.",
            "5-6": "Dependencies identified in PI planning or equivalent. Tracked with owners. Early warning system. Delays from dependencies < 20% of sprints.",
            "7-8": "Proactive dependency management. Dependencies resolved in planning, not during delivery. API contracts and integration contracts in place. Delays < 10% of sprints.",
            "9-10": "Near-zero dependency delays. Team architects for independence. API-first design. Dependencies minimized through architecture decisions. Cross-team SLAs in place."
        }
    },
    {
        "id": "P11",
        "dimension": "Process",
        "competency": "Cycle Time Optimization",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Story Cycle Time",
        "question": "Is story/ticket cycle time measured, consistently short, and actively optimized?",
        "data_sources": ["jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Cycle time not measured. Stories take weeks and the reason is unknown. Large batch sizes make cycle time analysis difficult.",
            "3-4": "Cycle time measured in Jira. Average 5-10 days. Some analysis but limited action.",
            "5-6": "Cycle time average 3-5 days. Regular analysis. Outliers investigated. Some reduction experiments.",
            "7-8": "Cycle time 1-3 days average. Continuous monitoring. Blockers detected and resolved quickly. Cycle time a sprint-level metric.",
            "9-10": "Cycle time < 1 day for most stories. Continuous flow board. Story sizing optimized for fast cycle times. Cycle time is primary delivery metric."
        }
    },
    {
        "id": "P12",
        "dimension": "Process",
        "competency": "Batch Size Control",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Small Batch Delivery",
        "question": "Does the team deliberately limit batch sizes — delivering small, frequent changes rather than large, infrequent releases?",
        "data_sources": ["jira", "github", "release_mgmt"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Large batch releases. Features bundled for quarterly releases. High risk per release. Change failure rate elevated due to batch size.",
            "3-4": "Monthly releases. Some effort to break down large stories. Batch sizes reducing but still large (> 2 weeks of work per release).",
            "5-6": "Bi-weekly releases. Stories consistently < 2 days. Feature flags decouple deploy from release. Batch sizes actively managed.",
            "7-8": "Weekly or more frequent releases. Micro-feature delivery. Batch size < 1 day of work per story. Low-risk incremental delivery.",
            "9-10": "Continuous delivery. Multiple deployments per day. Smallest possible batch sizes. Dark launches common. Each commit could be a release."
        }
    },
    {
        "id": "P13",
        "dimension": "Process",
        "competency": "Definition of Done",
        "humana_capability": "Working Differently",
        "humana_sub_capability": "Quality Gates",
        "question": "Is there a clear, comprehensive, and consistently enforced Definition of Done that includes security, performance, documentation, and operational readiness?",
        "data_sources": ["jira", "confluence", "sonarqube"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No DoD or it exists on paper but is not enforced. 'Done' means code written. No quality checks before marking done.",
            "3-4": "DoD exists and includes basic testing. Sometimes bypassed under pressure. Does not include security, performance, or ops readiness.",
            "5-6": "DoD enforced consistently. Includes unit tests, code review, and basic security scan. Some operational readiness criteria.",
            "7-8": "Comprehensive DoD. Includes security scan, performance test, documentation, and deployment readiness. Automated enforcement in pipeline.",
            "9-10": "DoD is automated and non-bypassable. Includes security, performance, observability, compliance, and runbooks. 100% enforcement rate."
        }
    },
    {
        "id": "P14",
        "dimension": "Process",
        "competency": "Release Cadence",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Predictable Release Rhythm",
        "question": "How predictable and frequent is the release cadence — can the team deploy on demand or at a regular, reliable cadence?",
        "data_sources": ["release_mgmt", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Releases are unpredictable events. Quarterly or less frequent. Release preparation takes weeks. Releases cause significant disruption.",
            "3-4": "Monthly release cycle. Some predictability. Release process documented but manual steps remain. Release takes 1-2 days.",
            "5-6": "Bi-weekly releases on a defined schedule. Release process largely automated. Release preparation < 4 hours. Stakeholders can rely on release schedule.",
            "7-8": "Weekly releases on demand. Fully automated release pipeline. Release < 1 hour including smoke tests. Rollback automated.",
            "9-10": "On-demand releases multiple times daily. Release is a non-event. Zero-downtime deployments. Stakeholders barely notice releases. Rollback in < 5 minutes."
        }
    },
    {
        "id": "P15",
        "dimension": "Process",
        "competency": "Value Stream Visibility",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Flow Visibility",
        "question": "Is the complete value stream from idea to production visible to all team members and stakeholders, with bottlenecks easily identifiable?",
        "data_sources": ["jira", "confluence"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Value stream not mapped. Teams see only their part. Bottlenecks hidden in hand-off queues. Stakeholders have no visibility.",
            "3-4": "Value stream mapped annually. Some visibility into queues. Limited data. Hard to identify bottlenecks in real-time.",
            "5-6": "Value stream map maintained and updated quarterly. Flow metrics tracked. Bottlenecks identified from data. Reviewed in quarterly planning.",
            "7-8": "Dynamic value stream view in real-time. Bottlenecks visible on team dashboard. Weekly optimization review. Flow efficiency tracked per stage.",
            "9-10": "Real-time value stream dashboard. AI-assisted bottleneck detection. Continuous optimization. Value stream is central to all planning and improvement."
        }
    },
    {
        "id": "P16",
        "dimension": "Process",
        "competency": "Process Automation",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Manual Process Elimination",
        "question": "What percentage of manual steps in the delivery process (testing, deployment, compliance checks, notifications) have been automated?",
        "data_sources": ["cicd", "itsm", "release_mgmt"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "< 20% of delivery steps automated. Deployments are manual. Testing is largely manual. Compliance checks are spreadsheet-based.",
            "3-4": "20-40% automation. CI automated. Some CD. Manual deployment steps remain. Automated testing covers unit tests only.",
            "5-6": "40-60% automation. Full CI/CD for standard changes. Automated regression suite. Some compliance automation. Manual steps in releases declining.",
            "7-8": "60-80% automation. Near-fully automated pipeline. Security scans automated. Compliance checks automated. Manual steps < 5 per release.",
            "9-10": "> 80% automation. Fully automated end-to-end pipeline. Human in loop only for strategic decisions. Toil < 10% of team capacity."
        }
    },

    # ═══════════════════════════════════════════════════════════════════
    # TECHNICAL DIMENSION (37 questions)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "T1",
        "dimension": "Technical",
        "competency": "Architecture",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Visible Architecture",
        "question": "Is the application architecture modular, loosely coupled, and designed for independent deployability — enabling teams to release without coordinating with other teams?",
        "data_sources": ["github", "confluence", "cicd"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Monolithic architecture. Changes in one area affect everything. Deployments require full regression. Release coordination across teams required.",
            "3-4": "Some modularization. N-tier architecture. Some independent components. Release coordination still needed. Shared databases common.",
            "5-6": "Service-oriented or microservices architecture in progress. Most services independently deployable. Shared services identified and being decoupled.",
            "7-8": "Microservices or modular monolith. True independent deployability for most services. API contracts tested. Team can release independently.",
            "9-10": "Fully modular architecture. Cell-based or service mesh. Zero coupling between team services. Independent release for every component. Architecture documented as code."
        }
    },
    {
        "id": "T2",
        "dimension": "Technical",
        "competency": "Deployment Automation",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Build & Deploy Automation",
        "question": "What percentage of deployments are fully automated end-to-end (from code commit to production) without manual steps?",
        "data_sources": ["cicd", "release_mgmt"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "< 20% automated. Deployments are manual scripts run by ops. Deployment runbooks are long and error-prone.",
            "3-4": "20-50% automated. CI automated. Manual deployment steps for production. Deployment runbooks exist.",
            "5-6": "50-80% automated. Full CI. Automated deployment to non-prod. Production deployment semi-automated with manual approval.",
            "7-8": "80-95% automated. Fully automated CD pipeline. Production deployment automated. Manual approval only for high-risk changes.",
            "9-10": "95-100% automated. Zero-touch deployment to production. Feature flags enable instant rollback. Deployment is a non-event."
        }
    },
    {
        "id": "T3",
        "dimension": "Technical",
        "competency": "Feature Flags",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Decoupled Deployment",
        "question": "Are feature flags used systematically to decouple deployment from release, enabling dark launches, canary releases, and instant rollback?",
        "data_sources": ["github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No feature flags. Deploy = release. All-or-nothing releases. Rollback requires full redeployment.",
            "3-4": "Feature flags used occasionally. Manual flag management. No consistent strategy. Some dark launches.",
            "5-6": "Feature flag platform in use. Standard for new features. Canary releases practiced. Flags cleaned up regularly.",
            "7-8": "Systematic feature flag usage. All significant features flagged. Percentage rollouts. A/B experiments via flags. Automated cleanup.",
            "9-10": "Feature flags are core delivery mechanism. Every release is an experiment. Instant kill switch for any feature. Flags managed as configuration-as-code."
        }
    },
    {
        "id": "T4",
        "dimension": "Technical",
        "competency": "Infrastructure as Code",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Infrastructure Automation",
        "question": "Is all infrastructure (servers, networking, databases, security groups) defined as code, version controlled, and provisioned via automated pipelines?",
        "data_sources": ["github", "cicd"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Infrastructure provisioned manually through console/UI. No IaC. Configuration drift common. Environments are 'snowflakes' — not reproducible.",
            "3-4": "Some IaC (Terraform/CloudFormation) for some resources. Mixed manual and automated provisioning. Some environment drift.",
            "5-6": "IaC for most infrastructure. Automated provisioning pipeline. Environments mostly reproducible. Configuration drift managed.",
            "7-8": "Full IaC coverage. Infrastructure provisioned via pipeline. Zero manual console changes. Drift detection automated. Environments fully reproducible.",
            "9-10": "GitOps for all infrastructure. Infrastructure changes go through same review process as code. Self-healing infrastructure. Policy-as-code enforced."
        }
    },
    {
        "id": "T5",
        "dimension": "Technical",
        "competency": "Branching Strategy",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Trunk-Based Development",
        "question": "Does the team practice trunk-based development (or equivalent short-lived branches) to minimize merge conflicts and enable continuous integration?",
        "data_sources": ["github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Long-lived feature branches (weeks to months). Merge conflicts are frequent and painful. Multiple release branches maintained. Integration is a project.",
            "3-4": "2-week branches. Some merge conflicts. Git flow or similar branching model. Feature branch PRs merged weekly.",
            "5-6": "Branches < 1 week. Daily merges to main. Feature flags enable merging incomplete features. Merge conflicts occasional.",
            "7-8": "Trunk-based development. Branches < 2 days. Commit to main multiple times per day. Feature flags for all incomplete features. Zero long-lived branches.",
            "9-10": "Pure trunk-based development. All work committed directly to main or via same-day PRs. Feature flags ubiquitous. No release branches — tags only."
        }
    },
    {
        "id": "T6",
        "dimension": "Technical",
        "competency": "Version Control",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Everything as Code",
        "question": "Is all code, configuration, infrastructure, pipeline definitions, and scripts version controlled — with a policy of no manual changes that bypass version control?",
        "data_sources": ["github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Source code in version control but configs, scripts, and infrastructure are not. Manual changes to servers are common. Config drift unmanageable.",
            "3-4": "Most code versioned. Some config in VCS. Infrastructure scripts in repos. Manual changes still happen. No policy enforcement.",
            "5-6": "Code, config, and infrastructure in VCS. Pipeline definitions versioned. Policy exists. Some exceptions tolerated.",
            "7-8": "Everything in VCS. No manual changes to any environment. Policy enforced. Change detection alerts for drift.",
            "9-10": "Immutable infrastructure. All changes via code and pipeline. Cryptographic verification. No human has shell access to production. Full audit trail."
        }
    },
    {
        "id": "T7",
        "dimension": "Technical",
        "competency": "Security Testing",
        "humana_capability": "DevSecOps",
        "humana_sub_capability": "Shift-Left Security",
        "question": "Is security testing (SAST, DAST, SCA, container scanning) integrated into the CI/CD pipeline and does it gate deployments on critical findings?",
        "data_sources": ["cicd", "sonarqube", "risk_portal", "github"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Security testing is a separate activity done by a security team before major releases. Not automated. Critical vulnerabilities sometimes found in production.",
            "3-4": "SAST tool integrated in pipeline. Results reviewed manually. Some critical findings gate deployments but process is inconsistent.",
            "5-6": "SAST + SCA integrated. Critical/high findings block deployment automatically. DAST run in staging. Container scanning in place.",
            "7-8": "Full DevSecOps pipeline: SAST, DAST, SCA, container scanning, IaC scanning. All critical findings auto-block. Security champions in team. Risk score per build.",
            "9-10": "Security-as-code. All security policies automated. Threat modeling automated. Security scan results feed risk dashboard. Zero known critical vulnerabilities in production. Pen tests confirm."
        }
    },
    {
        "id": "T8",
        "dimension": "Technical",
        "competency": "Test Automation",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Test Automation Coverage",
        "question": "What is the automated test coverage across unit, integration, and end-to-end tests — and is coverage improving sprint over sprint?",
        "data_sources": ["sonarqube", "cicd", "github"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "< 20% automated test coverage. Testing is primarily manual. Regression takes weeks. Test suites are unreliable.",
            "3-4": "20-40% coverage. Unit tests for critical paths. Some integration tests. Manual regression for new features.",
            "5-6": "40-60% coverage. Unit and integration test suites. E2E for critical user journeys. Coverage improving. Manual regression < 30% of test effort.",
            "7-8": "60-80% coverage. Comprehensive test pyramid. E2E for all key journeys. Coverage enforced as pipeline gate. Manual testing < 15%.",
            "9-10": "> 80% coverage. Test pyramid well-balanced. Mutation testing used. AI-assisted test generation. Manual exploratory testing only. Coverage gates enforced."
        }
    },
    {
        "id": "T9",
        "dimension": "Technical",
        "competency": "CI Pipeline",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Continuous Integration",
        "question": "Is continuous integration practiced — are all developers integrating to main at least daily, with an automated build and test pipeline that provides fast feedback?",
        "data_sources": ["cicd", "github"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "No CI. Integration is a manual, infrequent event. Builds done locally. Integration issues discovered late.",
            "3-4": "CI server exists. Builds triggered on commit. Basic tests run. Build time 20+ minutes. Some builds broken for extended periods.",
            "5-6": "CI pipeline well-established. Builds in 10-20 minutes. Unit + integration tests. PR checks required. Build success rate > 80%.",
            "7-8": "Optimized CI. Build in < 10 minutes. Full test suite (unit + integration + security). Branch protection enforced. Build success rate > 90%.",
            "9-10": "Elite CI. Build + feedback in < 5 minutes. Parallel execution. Incremental builds. Build success rate > 95%. Developers integrate multiple times per day."
        }
    },
    {
        "id": "T10",
        "dimension": "Technical",
        "competency": "Deployment Frequency",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Continuous Delivery",
        "question": "How frequently does the team deploy to production — and is deployment frequency increasing toward on-demand?",
        "data_sources": ["release_mgmt", "cicd"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Fewer than monthly deployments. Releases are major events causing significant disruption.",
            "3-4": "Monthly deployments. Some effort to increase frequency. Deployments cause moderate disruption.",
            "5-6": "Weekly to bi-weekly deployments. Automated deployment pipeline. Deployments are low-risk.",
            "7-8": "Daily or multiple times per week. Deployments are routine. Zero-downtime deployments. Stakeholders unaware of deployments.",
            "9-10": "On-demand, multiple times daily. Deployment is a non-event. Completely automated. Rollback in < 5 minutes."
        }
    },
    {
        "id": "T11",
        "dimension": "Technical",
        "competency": "Recovery Capability",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Fast Recovery (MTTR)",
        "question": "Can the team recover from production failures in under 1 hour — with automated detection, automated or rapid manual remediation, and validated recovery procedures?",
        "data_sources": ["itsm", "oncall", "monitoring", "cicd"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Recovery from failures takes days. No runbooks. Manual processes. Recovery depends on specific individuals. MTTR unknown.",
            "3-4": "MTTR 4-24 hours. Some runbooks exist. Recovery process documented but slow. Escalation paths exist.",
            "5-6": "MTTR 1-4 hours. Runbooks for most common failures. Rollback possible but takes time. On-call rotation with clear escalation.",
            "7-8": "MTTR < 1 hour. Automated rollback for deployments. Runbooks for 80%+ of failure scenarios. Self-healing for common issues.",
            "9-10": "MTTR < 15 minutes. Automated detection and recovery. Self-healing infrastructure. Human intervention only for novel failure modes. Chaos engineering validates recovery."
        }
    },
    {
        "id": "T12",
        "dimension": "Technical",
        "competency": "Detection Speed",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Mean Time to Detect",
        "question": "Is anomaly detection and alerting in place to detect production issues in under 5 minutes, before customers are impacted?",
        "data_sources": ["monitoring", "oncall"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Issues detected by customer complaints or manual checks. No proactive monitoring. MTTD hours to days.",
            "3-4": "Basic threshold alerting. MTTD 30 minutes to 2 hours. High false-positive rate. Alert fatigue common.",
            "5-6": "APM in place. MTTD < 30 minutes. Alert noise managed. Runbooks linked to alerts. Business impact understood.",
            "7-8": "Anomaly detection active. MTTD < 10 minutes. Synthetic monitoring. SLO-based alerts. Low false-positive rate (< 20%).",
            "9-10": "MTTD < 2 minutes. Predictive alerting. AIOps reducing false positives. Business metrics correlated with technical signals. User-perceived impact prevented proactively."
        }
    },
    {
        "id": "T13",
        "dimension": "Technical",
        "competency": "Test Data Management",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Test Data Automation",
        "question": "Is test data available on demand for all test environments — provisioned automatically, masked/anonymized, and refreshed regularly?",
        "data_sources": ["cicd", "jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Test data is a constant bottleneck. Manual data preparation. Production data used in test (compliance risk). Environments share data causing conflicts.",
            "3-4": "Test data provisioned manually but documented. Some masking. Takes 1-2 days to get test data. Some environment conflicts.",
            "5-6": "Test data management process. On-demand generation for unit/integration tests. Masked production subset for E2E. Refresh process documented.",
            "7-8": "Automated test data provisioning. On-demand in < 30 minutes. Full masking/anonymization automated. Environments fully isolated.",
            "9-10": "Synthetic test data generation. On-demand in < 5 minutes. AI-generated test data for edge cases. Compliance-safe by design. No dependency on production data."
        }
    },
    {
        "id": "T14",
        "dimension": "Technical",
        "competency": "Release Confidence",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Stakeholder Confidence",
        "question": "Do stakeholders (business, ops, security) trust automated testing enough to approve releases without manual testing or additional validation?",
        "data_sources": ["cicd", "sonarqube", "release_mgmt"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Stakeholders do not trust automation. Manual UAT required for every release. Extended approval cycles. Release fear is high.",
            "3-4": "Limited trust. Manual UAT for major features. Automated tests treated as necessary but not sufficient. Approval cycle 1-2 weeks.",
            "5-6": "Growing trust. Manual UAT only for high-risk changes. Automated tests trusted for regression. Approval cycle < 1 week.",
            "7-8": "High trust. Manual UAT rare (< 20% of releases). Automated quality gates trusted. Release approval < 1 day.",
            "9-10": "Full stakeholder trust. No manual UAT. Automated quality gates are sole approval. Release is self-service for teams. Rollback if issues occur post-release."
        }
    },
    {
        "id": "T15",
        "dimension": "Technical",
        "competency": "Code Quality",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Static Analysis & Code Review",
        "question": "Is automated code quality analysis (SonarQube, linting, complexity analysis) integrated as a mandatory pipeline gate?",
        "data_sources": ["sonarqube", "github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No automated code quality analysis. Code reviews are inconsistent. Technical debt is invisible.",
            "3-4": "Linting in place. Basic SonarQube integration. Results visible but not mandatory. Code reviews required but quality inconsistent.",
            "5-6": "SonarQube quality gate mandatory. PR reviews enforced. Coverage gate set. New technical debt tracked.",
            "7-8": "Comprehensive quality gates. Multiple quality dimensions measured. Technical debt trend monitored. Security hotspots reviewed.",
            "9-10": "Zero-tolerance quality gates. Multiple analysis tools. Automated security analysis. Technical debt below threshold as pipeline gate. Code quality improving sprint-over-sprint."
        }
    },
    {
        "id": "T16",
        "dimension": "Technical",
        "competency": "Cloud Native",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Container & Cloud Adoption",
        "question": "Are workloads containerized and running on cloud-native platforms (Kubernetes, ECS, etc.) with automated scaling and self-healing?",
        "data_sources": ["github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Applications run on bare-metal or traditional VMs. Manual scaling. No container strategy. Cloud lift-and-shift only.",
            "3-4": "Some containerization. Docker used for some services. Basic Kubernetes. Limited auto-scaling. Cloud-native patterns not fully adopted.",
            "5-6": "Most services containerized. Kubernetes for orchestration. Auto-scaling configured. Health checks in place. Cloud-native patterns for new services.",
            "7-8": "Fully containerized. Kubernetes with GitOps. Auto-scaling and self-healing. Cloud-native design for all services. Multi-region capability.",
            "9-10": "Cloud-native first. Serverless for appropriate workloads. Service mesh. AI-driven auto-scaling. Zero-downtime deployments. Cost-optimized cloud usage."
        }
    },
    {
        "id": "T17",
        "dimension": "Technical",
        "competency": "Observability",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Full Observability",
        "question": "Is full observability implemented — structured logs, distributed traces, and metrics correlated across all services for rapid debugging?",
        "data_sources": ["monitoring"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Log files on servers. No distributed tracing. Debugging in production requires SSH access. Root cause analysis takes days.",
            "3-4": "Centralized logging. Some metrics. Limited tracing. Debugging still slow. Correlation between services manual.",
            "5-6": "ELK or Splunk for logs. Basic APM. Some distributed tracing. Dashboards per service. Debugging time < 2 hours.",
            "7-8": "Full observability stack: structured logs, traces, metrics correlated. Distributed tracing across all services. Root cause in < 30 minutes.",
            "9-10": "Exceptional observability. AI-assisted root cause analysis. Business and technical metrics unified. Real-time service dependency maps. MTTD < 2 minutes."
        }
    },
    {
        "id": "T18",
        "dimension": "Technical",
        "competency": "Rollback Capability",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Zero-Risk Deployments",
        "question": "Can the team rollback any deployment in under 30 minutes — with automated rollback triggered by monitoring anomalies?",
        "data_sources": ["cicd", "release_mgmt", "monitoring"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Rollback is not practiced. Fixing forward is the only option. Rollback would take days due to database schema changes or data migration.",
            "3-4": "Rollback possible for some deployments. Takes 1-4 hours. Manual process. DB rollback is risky and rare.",
            "5-6": "Rollback documented and practiced. Takes 30-60 minutes. Blue/green deployments for critical services. DB rollback strategy exists.",
            "7-8": "Automated rollback on monitoring trigger. < 30 minutes. Blue/green or canary for all services. DB change management enables rollback.",
            "9-10": "Instant rollback via feature flags. Automated canary analysis triggers rollback. < 5 minutes. No manual intervention. Rollback is tested regularly."
        }
    },
    {
        "id": "T19",
        "dimension": "Technical",
        "competency": "Database DevOps",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Database Change Management",
        "question": "Are database schema changes automated, versioned, tested, and deployed through the same CI/CD pipeline as application code?",
        "data_sources": ["github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Database changes are manual SQL scripts applied directly to production by DBAs. No versioning. Change conflicts common. Rollback impossible.",
            "3-4": "Migration scripts versioned in VCS. Manual execution by DBAs. Some automation for non-prod. Rollback scripts exist but not tested.",
            "5-6": "Flyway/Liquibase or equivalent. Automated migration in CI/CD. Non-prod automated. Production semi-automated with DBA review. Rollback scripts automated.",
            "7-8": "Full database DevOps. Schema changes in CI/CD pipeline. Automated rollback. Zero-downtime schema changes (expand/contract pattern). DBA reviews high-risk changes only.",
            "9-10": "Database changes are code. Automated review, test, and deploy. Expand-contract pattern standard. Online schema changes. DBA as consultant not gatekeeper."
        }
    },
    {
        "id": "T20",
        "dimension": "Technical",
        "competency": "Secrets Management",
        "humana_capability": "DevSecOps",
        "humana_sub_capability": "Credential Security",
        "question": "Are secrets (API keys, passwords, certificates) managed securely using a vault/secrets manager — with no hardcoded credentials in code or config files?",
        "data_sources": ["github", "sonarqube", "risk_portal"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Credentials hardcoded in source code or config files. Secrets in VCS. No rotation. High security risk.",
            "3-4": "Secrets in environment variables. Some use of secrets manager for new services. Rotation manual and infrequent. Legacy services still have hardcoded credentials.",
            "5-6": "Secrets manager (HashiCorp Vault/AWS SSM) for most services. No new hardcoded secrets. Automated rotation for some secrets. Scanning for hardcoded creds in pipeline.",
            "7-8": "Full secrets management. Automated rotation. Dynamic secrets for databases. Pre-commit hooks scan for secrets. Regular audits.",
            "9-10": "Zero-trust secrets model. Dynamic, short-lived secrets everywhere. Automated rotation. Secrets access monitored and anomalies alerted. Regular penetration tests validate."
        }
    },
    {
        "id": "T21",
        "dimension": "Technical",
        "competency": "Dependency Security",
        "humana_capability": "DevSecOps",
        "humana_sub_capability": "Supply Chain Security",
        "question": "Are third-party dependencies (libraries, containers, OS packages) continuously scanned for known vulnerabilities and kept up to date?",
        "data_sources": ["cicd", "sonarqube", "github", "risk_portal"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "No dependency scanning. Outdated dependencies used for years. CVEs in production unknown. No process for security patches.",
            "3-4": "OWASP Dependency Check or Snyk in place. Monthly scan reports. Manual remediation. Critical CVEs sometimes go unpatched for weeks.",
            "5-6": "SCA integrated in CI pipeline. Critical CVEs block deployment. Regular dependency updates. Automated PR for security patches.",
            "7-8": "Comprehensive SCA: libraries, containers, OS. Automated patching for minor updates. Critical CVEs remediated within SLA (< 1 week). Software Bill of Materials (SBOM) generated.",
            "9-10": "Continuous dependency monitoring. Automated remediation where safe. SBOM published. Container image signing. Zero known critical CVEs in production > 24 hours."
        }
    },
    {
        "id": "T22",
        "dimension": "Technical",
        "competency": "Artifact Management",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Artifact Versioning",
        "question": "Are build artifacts (binaries, containers, packages) versioned, signed, stored in a registry, and promoted through environments rather than rebuilt?",
        "data_sources": ["cicd", "github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No artifact management. Applications rebuilt at each environment. Version tracking manual. No audit trail of what is deployed where.",
            "3-4": "Basic artifact repository. Some versioning. Artifacts stored but not consistently promoted. Manual promotion process.",
            "5-6": "Nexus/Artifactory in use. Semantic versioning. Artifacts promoted from dev to prod. Deployment audit trail exists.",
            "7-8": "Immutable artifacts. Signed and verified. Promoted through pipeline stages. Full traceability. Vulnerability scanning on artifacts.",
            "9-10": "Complete artifact governance. Signed, scanned, versioned artifacts. SBOM per artifact. Automated promotion with quality gates. 100% traceability."
        }
    },
    {
        "id": "T23",
        "dimension": "Technical",
        "competency": "Environment Management",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Environment Parity",
        "question": "Are development, staging, and production environments consistent and reproducible — eliminating 'it works on my machine' problems?",
        "data_sources": ["cicd", "github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Environments are manually configured snowflakes. Configuration drift is constant. 'Works on my machine' is a frequent phrase. Production differs significantly from dev.",
            "3-4": "Environments partially consistent. IaC for some infrastructure. Some config drift. Environment provisioning takes days.",
            "5-6": "Environments provisioned from IaC. Configuration managed. Drift detection in place. New environment in < 1 day.",
            "7-8": "Fully consistent environments. Containerized for local dev (Docker Compose). IaC for cloud environments. New environment in < 1 hour. Drift alerts.",
            "9-10": "Ephemeral environments. PR preview environments auto-created. Environments are disposable. Full local-to-prod parity. Environment provisioning < 10 minutes."
        }
    },
    {
        "id": "T24",
        "dimension": "Technical",
        "competency": "Performance Testing",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Performance Engineering",
        "question": "Is performance testing automated and integrated into the delivery pipeline — with performance baselines and SLO gates?",
        "data_sources": ["cicd", "monitoring"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Performance testing done manually before major releases. No automated performance tests. Performance issues discovered in production.",
            "3-4": "Load tests run before major releases. Manual execution. Some baselines. Performance issues discovered in staging.",
            "5-6": "Automated load tests in CI/CD for critical services. Performance baselines established. SLO gates for major releases.",
            "7-8": "Performance tests in pipeline for all services. Automated baseline comparison. SLO gates mandatory. Continuous performance monitoring in production.",
            "9-10": "Continuous performance testing. AI-predicted performance regression. Chaos engineering for performance. Performance SLOs met 99.9% of time. Capacity planning automated."
        }
    },
    {
        "id": "T25",
        "dimension": "Technical",
        "competency": "Compliance Automation",
        "humana_capability": "DevSecOps",
        "humana_sub_capability": "Compliance as Code",
        "question": "Are regulatory and policy compliance checks automated in the pipeline — generating evidence for audits automatically?",
        "data_sources": ["cicd", "risk_portal", "sonarqube"],
        "weight": 3,
        "scoring_criteria": {
            "1-2": "Compliance checks are manual and periodic. Audit preparation takes weeks. Evidence gathered manually from multiple systems.",
            "3-4": "Some compliance checks automated. Audit evidence partially automated. Compliance reports generated monthly with some manual effort.",
            "5-6": "Key compliance controls automated in pipeline. Audit evidence auto-collected. Compliance dashboard maintained. Audit prep takes days.",
            "7-8": "Comprehensive compliance-as-code. Policy checks automated. Continuous compliance monitoring. Audit evidence instantly available. Compliance score visible on dashboard.",
            "9-10": "Zero-friction compliance. All controls automated. Real-time compliance posture. Audit evidence cryptographically signed. Regulatory audits take hours not weeks."
        }
    },
    {
        "id": "T26",
        "dimension": "Technical",
        "competency": "Resilience Engineering",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Chaos Engineering",
        "question": "Does the team proactively test system resilience through chaos engineering, game days, or failure injection to validate recovery procedures?",
        "data_sources": ["cicd", "monitoring"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No resilience testing. System resilience unknown until production incidents. Recovery procedures untested.",
            "3-4": "Manual game days for major incidents. DR testing annually. Some runbook validation. Limited chaos engineering awareness.",
            "5-6": "Regular game days (quarterly). Chaos experiments in non-prod. Recovery procedures tested and documented. MTTR targets validated.",
            "7-8": "Automated chaos experiments in staging. Monthly game days. DR tested quarterly. Recovery procedures automated and validated. Confidence in resilience.",
            "9-10": "Continuous chaos engineering. Automated failure injection in production (with safeguards). Verified resilience across all failure modes. Recovery procedures are code."
        }
    },
    {
        "id": "T27",
        "dimension": "Technical",
        "competency": "Deployment Patterns",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Zero-Downtime Deployment",
        "question": "Are zero-downtime deployment patterns (blue/green, canary, rolling) used for all production deployments?",
        "data_sources": ["cicd", "release_mgmt"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Deployments cause downtime. Maintenance windows required. Users experience outages during releases.",
            "3-4": "Some zero-downtime for critical services. Blue/green for some deployments. Canary deployments being explored.",
            "5-6": "Zero-downtime for most services. Blue/green standard. Canary for high-risk changes. Scheduled maintenance windows rare.",
            "7-8": "Zero-downtime for all services. Automated canary with metric-based promotion/rollback. No maintenance windows.",
            "9-10": "Invisible deployments. Continuous deployment with canary. Instant rollback via feature flags. Stakeholders unaware of deployments. 100% uptime during deployments."
        }
    },
    {
        "id": "T28",
        "dimension": "Technical",
        "competency": "API Testing",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Contract Testing",
        "question": "Are API contracts defined and tested automatically — ensuring consumer-driven contract testing prevents breaking changes?",
        "data_sources": ["cicd", "github"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No API contract testing. Breaking changes discovered in integration or production. API versioning ad-hoc.",
            "3-4": "OpenAPI specs defined. Manual API testing. Some integration tests. Breaking changes occasionally slip through.",
            "5-6": "OpenAPI specs in VCS. Automated API tests in pipeline. Schema validation. Breaking changes caught in CI.",
            "7-8": "Consumer-driven contract testing (Pact or similar). Automated contract validation in pipeline. API versioning strategy enforced.",
            "9-10": "Full contract testing suite. Breaking changes impossible to deploy. API governance automated. API catalog maintained. Backward compatibility guaranteed."
        }
    },
    {
        "id": "T29",
        "dimension": "Technical",
        "competency": "Static Analysis",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Code Quality Gates",
        "question": "Is static code analysis (complexity, duplication, code smells, security hotspots) enforced as a non-bypassable pipeline gate?",
        "data_sources": ["sonarqube", "github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No static analysis. Code quality declining. Technical debt invisible. Security hotspots unknown.",
            "3-4": "SonarQube configured. Results visible. Not a pipeline gate. Quality issues reviewed periodically.",
            "5-6": "Quality gate enforced. Critical issues block PR merge. Technical debt tracked. Security hotspots reviewed.",
            "7-8": "Strict quality gates. Multiple metrics gated. Technical debt budget enforced. Complexity thresholds mandatory. Trend tracking.",
            "9-10": "Zero-tolerance quality gates. AI-assisted code review. Technical debt as a team OKR. Quality metrics published to stakeholders."
        }
    },
    {
        "id": "T30",
        "dimension": "Technical",
        "competency": "Build Reproducibility",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Reproducible Builds",
        "question": "Are builds fully reproducible — can any historical version be rebuilt from source to produce an identical artifact?",
        "data_sources": ["github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Builds not reproducible. Dependencies not locked. Environment-specific builds. Cannot reproduce builds from 6 months ago.",
            "3-4": "Dependencies partially locked (some package-lock files). Builds mostly reproducible for recent versions. Historical builds unreliable.",
            "5-6": "Dependencies fully locked. Builds reproducible for all recent versions. Build environment containerized.",
            "7-8": "Fully reproducible builds. Deterministic dependencies. Build environment as code. Any commit rebuildable identically.",
            "9-10": "Cryptographically verified reproducible builds. SBOM per build. Any historical version rebuildable in < 10 minutes. Build provenance tracked."
        }
    },
    {
        "id": "T31",
        "dimension": "Technical",
        "competency": "Alert Management",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Actionable Alerting",
        "question": "Are monitoring alerts actionable, with low noise, clear runbooks, and routed to the right people — not causing alert fatigue?",
        "data_sources": ["monitoring", "oncall"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Alert storm. Hundreds of alerts per day. Most are noise. Alert fatigue severe. Critical alerts missed. No runbooks.",
            "3-4": "Alerts categorized. Some runbooks. False positive rate > 50%. On-call engineers regularly paged for non-issues.",
            "5-6": "Alert quality improving. False positive rate < 30%. Runbooks for 60%+ alerts. Alert routing to correct team.",
            "7-8": "Low-noise alerting. False positive rate < 15%. Runbooks for all alerts. Automated remediation for common alerts. On-call quality of life improving.",
            "9-10": "Near-zero false positives. AI-powered alert correlation. Automated remediation for 50%+ alerts. On-call pager volume < 2 per week. Alerts are meaningful signals."
        }
    },
    {
        "id": "T32",
        "dimension": "Technical",
        "competency": "Incident Management",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Incident Process",
        "question": "Is there a formal, well-practiced incident management process with defined roles, communication templates, and post-incident review?",
        "data_sources": ["itsm", "oncall", "confluence"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "No formal incident process. Ad-hoc response. No defined roles. Communication is chaotic. Incidents repeat.",
            "3-4": "Basic incident process. Incident commander role defined. Some runbooks. Post-mortems rare. Incidents sometimes repeat.",
            "5-6": "Formal incident process. Defined roles and communication channels. Blameless post-mortems standard. Action items tracked.",
            "7-8": "Well-practiced incident process. Regular game days. Automated incident timeline. Post-mortems drive improvements. Incident recurrence declining.",
            "9-10": "Incident management excellence. Automated detection and triage. AI-assisted diagnosis. Post-mortems published widely. Incident learning shared across organization."
        }
    },
    {
        "id": "T33",
        "dimension": "Technical",
        "competency": "Capacity Planning",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Predictive Capacity Management",
        "question": "Is capacity planning proactive and data-driven — using historical trends to predict and provision capacity before performance degradation occurs?",
        "data_sources": ["monitoring"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Reactive capacity management. Scale after incidents. No trend analysis. Frequent performance issues due to capacity.",
            "3-4": "Manual capacity reviews monthly. Some auto-scaling. Trend analysis for major events. Occasional capacity-related incidents.",
            "5-6": "Auto-scaling configured. Capacity trends reviewed monthly. Predictive scaling for known events. Capacity incidents rare.",
            "7-8": "Predictive capacity management. Auto-scaling policies data-driven. Capacity forecasting integrated with roadmap. Proactive upgrades.",
            "9-10": "AI-driven capacity management. Fully automated scaling. Capacity never a constraint. Cost-optimized. Capacity planning invisible to team."
        }
    },
    {
        "id": "T34",
        "dimension": "Technical",
        "competency": "Technical Debt",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Technical Debt Management",
        "question": "Is technical debt tracked, prioritized, and given dedicated capacity each sprint — with a measurable reduction trend?",
        "data_sources": ["sonarqube", "jira"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Technical debt invisible and unmanaged. No tracking. Code quality declining. Team spends increasing time fighting legacy issues.",
            "3-4": "Technical debt in backlog but deprioritized. SonarQube shows debt. Occasional refactoring. Debt growing.",
            "5-6": "Technical debt tracked and measured. 10-15% sprint capacity for debt. SonarQube debt ratio tracked. Debt trend flat.",
            "7-8": "Technical debt actively managed. 15-20% sprint capacity. Debt ratio declining. Architecture decisions consider debt impact.",
            "9-10": "Technical debt as a team metric. Debt below threshold as pipeline gate. Refactoring integrated into feature delivery. Debt ratio < 5%. Clean code culture."
        }
    },
    {
        "id": "T35",
        "dimension": "Technical",
        "competency": "Documentation",
        "humana_capability": "DevOps",
        "humana_sub_capability": "Documentation as Code",
        "question": "Is documentation (architecture decisions, runbooks, API specs, onboarding guides) versioned alongside code and kept current?",
        "data_sources": ["github", "confluence"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Documentation out of date or non-existent. Onboarding new team members takes months. Architecture decisions undocumented. Tribal knowledge dominant.",
            "3-4": "Some documentation in Confluence. Partially maintained. Runbooks exist for some services. Architecture docs stale. Onboarding takes 2-4 weeks.",
            "5-6": "Documentation-as-code for key areas. ADRs tracked. API specs in VCS. Runbooks cover 60%+ of services. Onboarding < 2 weeks.",
            "7-8": "Comprehensive, current documentation. ADRs for all architecture decisions. Runbooks automated where possible. API docs auto-generated. Onboarding < 1 week.",
            "9-10": "Documentation excellence. Docs-as-code standard. Auto-generated from source. Always current (CI fails if docs outdated). New engineer productive in 2 days."
        }
    },
    {
        "id": "T36",
        "dimension": "Technical",
        "competency": "Cloud Cost Optimization",
        "humana_capability": "DevOps",
        "humana_sub_capability": "FinOps",
        "question": "Are cloud costs monitored, attributed to teams, and actively optimized — with cost efficiency as part of engineering best practices?",
        "data_sources": ["monitoring"],
        "weight": 1,
        "scoring_criteria": {
            "1-2": "Cloud costs unknown or reviewed only by finance. No cost attribution by team. No optimization activities. Costs growing unchecked.",
            "3-4": "Monthly cost reviews. Some tagging for attribution. Manual optimization of obvious waste. Cost awareness limited.",
            "5-6": "Cost dashboards per team/product. Monthly optimization reviews. Automated right-sizing recommendations. Cost a consideration in architecture decisions.",
            "7-8": "Real-time cost dashboards. Cost budgets per team. Automated optimization (reserved instances, spot). Cost efficiency a team metric.",
            "9-10": "FinOps culture. Engineers make cost-informed decisions. Automated cost optimization. Cost per unit of business value tracked. Industry-leading cost efficiency."
        }
    },
    {
        "id": "T37",
        "dimension": "Technical",
        "competency": "Developer Experience",
        "humana_capability": "Talent and Community",
        "humana_sub_capability": "Developer Productivity Platform",
        "question": "Does the team have an excellent developer experience — fast local setup, golden paths for common tasks, and internal developer platform support?",
        "data_sources": ["github", "cicd"],
        "weight": 2,
        "scoring_criteria": {
            "1-2": "Developer setup takes days. No golden paths. Every project has different tooling. High cognitive load. Significant toil in dev workflow.",
            "3-4": "Setup guides exist. Some standardization. CI/CD templates. Local development works but is slow. Some toil remains.",
            "5-6": "Developer portal or templates. Local dev streamlined. Golden paths for most use cases. Toil below 20% of dev time.",
            "7-8": "Internal developer platform. Self-service provisioning. Golden paths for all common scenarios. Toil < 10%. Developers love their tooling.",
            "9-10": "World-class developer experience. Self-service everything. Developer experience team dedicated. Toil < 5%. Onboarding to first PR in < 1 day. Developers are highly productive and satisfied."
        }
    },
]

# Quick lookup maps
QUESTIONS_BY_ID = {q["id"]: q for q in QUESTIONS}
QUESTIONS_BY_DIMENSION = {}
for q in QUESTIONS:
    dim = q["dimension"]
    if dim not in QUESTIONS_BY_DIMENSION:
        QUESTIONS_BY_DIMENSION[dim] = []
    QUESTIONS_BY_DIMENSION[dim].append(q)

DIMENSIONS = ["Cultural", "Measurement", "Process", "Technical"]
DIMENSION_QUESTION_COUNTS = {dim: len(QUESTIONS_BY_DIMENSION.get(dim, [])) for dim in DIMENSIONS}


def get_maturity_band(score: float) -> dict:
    if score <= 2:
        return MATURITY_BANDS["PRE_CRAWL"]
    elif score <= 4:
        return MATURITY_BANDS["CRAWL"]
    elif score <= 6:
        return MATURITY_BANDS["WALK"]
    elif score <= 8:
        return MATURITY_BANDS["RUN"]
    else:
        return MATURITY_BANDS["FLY"]


def get_maturity_level(score: float) -> str:
    return get_maturity_band(score)["label"]
