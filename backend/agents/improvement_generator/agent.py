"""
Improvement Generator Agent
For each bottleneck, generates targeted improvement actions using:
  - GenAI / LLM agent solutions
  - Industry best practices (Lean, DORA, SAFe)
  - Competitor insights (FAANG, fintech leaders)
  - ROI estimates based on effort/wait reduction

Output schema uses camelCase to match the frontend ImprovementsPage card layout:
  id, phaseId, phaseName, activity, priority, title, problem, improvement,
  agent, type, expectedPTReduction, expectedWTReduction, timeToValue, roi,
  effort, category, bottleneckId
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import ALL_ACTIVITIES
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)


# Pre-built improvement catalogue aligned to PDLC activities
# Keys match the activity names that bottleneck_analyzer emits
IMPROVEMENT_CATALOGUE = {
    "Feature Definition & Refinement": {
        "title":               "FeatureGen Agent — AI Feature Authoring",
        "problem":             "4–8 hrs effort + 1–3 day PM/BA iteration cycles to reach shippable acceptance criteria",
        "improvement":         "FeatureGen Agent generates structured feature definitions with ACs from high-level intent, using product personas via RAG. Reduces PM iteration from days to 30 minutes.",
        "agent":               "FeatureGen Agent",
        "type":                "GenAI Agent",
        "expectedPTReduction": 50, "expectedWTReduction": 70,
        "timeToValue":         "2–4 weeks", "roi": "3.5×", "effort": "Low",
        "bestPractices":       ["AI-assisted requirements", "RAG-powered feature gen", "INVEST criteria validation"],
        "competitorInsight":   "Linear, Notion AI used for AI-powered backlog management",
    },
    "Epic Decomposition & Story Splitting": {
        "title":               "AI Story Splitter — Epic-to-Sprint Decomposition",
        "problem":             "2–4 hrs per epic to split into sprint-ready stories; inconsistent vertical slicing quality across POs",
        "improvement":         "AI Story Splitter decomposes epics into vertically-sliced, independently-deliverable stories using INVEST criteria. Consistent quality, 80% time saved on decomposition.",
        "agent":               "AI Story Splitter",
        "type":                "GenAI Agent",
        "expectedPTReduction": 45, "expectedWTReduction": 30,
        "timeToValue":         "2–3 weeks", "roi": "3.2×", "effort": "Low",
        "bestPractices":       ["Vertical slicing", "INVEST criteria", "Story point calibration"],
        "competitorInsight":   "Atlassian Intelligence auto-splits epics in Jira for enterprise teams",
    },
    "Sprint Planning & Velocity Forecasting": {
        "title":               "Sprint Velocity Predictor — AI Capacity Planning",
        "problem":             "1–3 day manual sprint planning; velocity estimates inaccurate by 30–40%",
        "improvement":         "Velocity Predictor analyses 12-sprint rolling history, team capacity, and ticket complexity to forecast sprint throughput with 85%+ accuracy. Reduces planning ceremony time by 50%.",
        "agent":               "Velocity Predictor",
        "type":                "AI Automation",
        "expectedPTReduction": 30, "expectedWTReduction": 40,
        "timeToValue":         "3–5 weeks", "roi": "2.8×", "effort": "Low",
        "bestPractices":       ["Historical velocity analysis", "Capacity planning automation", "Monte Carlo simulation"],
        "competitorInsight":   "Planview, Agility Insights use ML-driven velocity forecasting for enterprise teams",
    },
    "Peer Code Review": {
        "title":               "ReviewAgent — AI-Augmented Code Review",
        "problem":             "4–24 hr wait for reviewer availability; inconsistent review quality; reviewers spend 70% on style/formatting",
        "improvement":         "ReviewAgent instantly analyses diffs, flags bugs/security/style issues, and produces structured summaries. Human reviewer focuses on architecture and business logic. Reduces wait from 24hrs to 30 mins.",
        "agent":               "ReviewAgent",
        "type":                "GenAI Agent",
        "expectedPTReduction": 40, "expectedWTReduction": 70,
        "timeToValue":         "2–3 weeks", "roi": "5.0×", "effort": "Low",
        "bestPractices":       ["Automated PR analysis", "LLM-powered diff summarization", "Security linting"],
        "competitorInsight":   "Google, Microsoft, Meta all use AI-assisted code review at scale",
    },
    "Coding (Feature Development)": {
        "title":               "CodeGen Agent — AI-Assisted Development",
        "problem":             "8–32 hrs effort; boilerplate, context-switching overhead, and documentation lag slow feature throughput",
        "improvement":         "Deploy GitHub Copilot/CodeGen Agent for real-time suggestions, boilerplate generation, refactoring, and inline documentation. Reduces development effort by 30–40% on typical features.",
        "agent":               "CodeGen Agent",
        "type":                "GenAI Agent",
        "expectedPTReduction": 35, "expectedWTReduction": 0,
        "timeToValue":         "1–2 weeks", "roi": "4.5×", "effort": "Low",
        "bestPractices":       ["AI pair programming", "Code generation", "Intelligent autocompletion"],
        "competitorInsight":   "GitHub reports 55% faster task completion with Copilot across 1M+ developers",
    },
    "Technical Debt Management": {
        "title":               "Tech Debt Prioritiser — AI-Scored Remediation Queue",
        "problem":             "8–16 hrs/quarter to manually assess and prioritise technical debt backlog; debt grows faster than addressed",
        "improvement":         "Tech Debt Prioritiser continuously scans codebase, scores debt items by business impact and refactor cost, and auto-populates a ranked remediation queue in Jira. Reduces assessment effort by 75%.",
        "agent":               "Tech Debt Prioritiser",
        "type":                "AI Automation",
        "expectedPTReduction": 20, "expectedWTReduction": 0,
        "timeToValue":         "3–5 weeks", "roi": "2.5×", "effort": "Medium",
        "bestPractices":       ["Automated debt detection", "Business-impact scoring", "Continuous debt monitoring"],
        "competitorInsight":   "SonarQube, CodeClimate AI provide automated debt scoring for 100K+ developers",
    },
    "Static Code Analysis (SAST)": {
        "title":               "ML-Powered SAST — Context-Aware Security Scanning",
        "problem":             "1–4 hr wait; high false-positive rate (60%+) forces manual triaging by developers",
        "improvement":         "Upgrade to ML-powered SAST (Semgrep, Snyk Code) with contextual vulnerability prioritisation and auto-fix suggestions. 60% false positive reduction; real vulnerabilities actioned same-day.",
        "agent":               "AI SAST Tools",
        "type":                "AI Automation",
        "expectedPTReduction": 40, "expectedWTReduction": 60,
        "timeToValue":         "3–4 weeks", "roi": "2.5×", "effort": "Medium",
        "bestPractices":       ["Shift-left security", "ML-powered SAST", "Auto-remediation"],
        "competitorInsight":   "Snyk, SonarQube AI used by top security-conscious engineering orgs",
    },
    "Build Failure Diagnosis": {
        "title":               "AI Build Failure Diagnostics — Root Cause in Seconds",
        "problem":             "30 min–2 hrs per flaky/failing build to diagnose root cause; developers blocked while CI queues clear",
        "improvement":         "AI Build Diagnostics analyses CI logs, correlates failures with recent code changes, and produces root-cause summaries with fix suggestions in < 30 seconds. Unblocks developers immediately.",
        "agent":               "AI Build Diagnostics",
        "type":                "AI Automation",
        "expectedPTReduction": 55, "expectedWTReduction": 30,
        "timeToValue":         "2–3 weeks", "roi": "3.8×", "effort": "Low",
        "bestPractices":       ["AI log analysis", "Flaky test quarantine", "Root cause correlation"],
        "competitorInsight":   "CircleCI, GitHub Actions use AI-powered failure insights for enterprise CI pipelines",
    },
    "Automated Performance Testing": {
        "title":               "AI Performance Analyzer — Regression Detection",
        "problem":             "16–40 hrs effort; manual performance test authoring and analysis; regressions missed until production",
        "improvement":         "AI Performance Analyzer auto-detects regressions, correlates metrics with code changes, and suggests root-cause optimisations. Reduces effort to 4–8 hrs; catches regressions at PR stage.",
        "agent":               "AI Performance Analyzer",
        "type":                "AI Automation",
        "expectedPTReduction": 75, "expectedWTReduction": 60,
        "timeToValue":         "4–6 weeks", "roi": "3.2×", "effort": "Medium",
        "bestPractices":       ["Test Impact Analysis", "Parallel test execution", "AI anomaly detection"],
        "competitorInsight":   "Netflix, Spotify use AI-driven performance regression detection in CI",
    },
    "Manual SIT / UAT / NF Signoff": {
        "title":               "AI UAT Assistant + Risk-Based Automated Signoff",
        "problem":             "2–5 day human approval wait; manual test consolidation across multiple testers and environments",
        "improvement":         "AI UAT Assistant auto-consolidates results, generates risk-scored readiness reports, enabling same-day signoff with exception-only human review. Reduces UAT cycle from 5 days to 4 hours.",
        "agent":               "AI UAT Assistant",
        "type":                "AI Automation",
        "expectedPTReduction": 50, "expectedWTReduction": 80,
        "timeToValue":         "6–8 weeks", "roi": "4.1×", "effort": "High",
        "bestPractices":       ["Continuous testing", "Risk-based signoff", "Test dashboard automation"],
        "competitorInsight":   "Amazon deploys 23,000 times/day with automated quality gates replacing manual UAT",
    },
    "Test Data Generation / Management": {
        "title":               "DataGen Agent — Synthetic Test Data on Demand",
        "problem":             "4–16 hr wait for test data provisioning; privacy/compliance risk with prod data copies in lower environments",
        "improvement":         "DataGen Agent generates privacy-compliant synthetic data on-demand from schema constraints. Eliminates provisioning queues and removes prod-data risk in lower environments permanently.",
        "agent":               "DataGen Agent",
        "type":                "GenAI Agent",
        "expectedPTReduction": 60, "expectedWTReduction": 85,
        "timeToValue":         "3–4 weeks", "roi": "3.8×", "effort": "Low",
        "bestPractices":       ["Synthetic data generation", "Schema-aware data masking", "GDPR-compliant TDM"],
        "competitorInsight":   "HSBC, Barclays use synthetic data generation for PII-safe test environments",
    },
    "Release Gates / Approvals": {
        "title":               "AI Release Manager — Automated Gate Validation",
        "problem":             "1–5 day wait for CAB approval; manual risk assessment repeated for every deployment regardless of change scope",
        "improvement":         "AI Release Manager auto-validates all release criteria, generates risk assessments with compliance evidence. Only outlier changes go to CAB; continuous deployment enabled with automated guardrails.",
        "agent":               "AI Release Manager",
        "type":                "AI Automation",
        "expectedPTReduction": 60, "expectedWTReduction": 75,
        "timeToValue":         "6–10 weeks", "roi": "2.9×", "effort": "High",
        "bestPractices":       ["Continuous delivery", "Progressive delivery", "Automated compliance"],
        "competitorInsight":   "Netflix, Spotify deploy continuously with automated risk gates replacing CAB",
    },
    "Solution Architecture (High-Level)": {
        "title":               "AI Architecture Reviewer — ADR Quality Gate",
        "problem":             "3–7 day wait for architecture review board; risks identified post-implementation cause costly rework",
        "improvement":         "AI Architecture Reviewer analyses proposed ADRs against existing patterns, flags risks, suggests alternatives, and generates structured feedback in < 5 minutes. Architect focuses on strategic trade-offs only.",
        "agent":               "AI Architecture Reviewer",
        "type":                "GenAI Agent",
        "expectedPTReduction": 35, "expectedWTReduction": 60,
        "timeToValue":         "3–4 weeks", "roi": "3.0×", "effort": "Medium",
        "bestPractices":       ["Architecture decision records", "Pattern library", "Automated risk detection"],
        "competitorInsight":   "ThoughtWorks, Atlassian use AI-assisted architecture review for faster ADR cycles",
    },
    "UX/UI High-Fidelity Design & Handoff": {
        "title":               "UX Prototype Generator — AI-Assisted Design Iteration",
        "problem":             "3–5 day cycles between design intent and low-fidelity prototypes; designers overwhelmed with iteration requests",
        "improvement":         "UX Prototype Generator creates clickable Figma-compatible wireframes from natural language specs and user personas. Reduces design cycle from 3 days to same-day for initial concepts.",
        "agent":               "UX Prototype Generator",
        "type":                "GenAI Agent",
        "expectedPTReduction": 50, "expectedWTReduction": 65,
        "timeToValue":         "4–6 weeks", "roi": "3.3×", "effort": "Medium",
        "bestPractices":       ["Design system automation", "AI-assisted wireframing", "Token-based handoff"],
        "competitorInsight":   "Figma AI, Adobe Firefly used by top-tier product teams to 10× iteration speed",
    },
    "Dynamic Security Testing (DAST)": {
        "title":               "AI DAST — Intelligent Fuzzing & False Positive Reduction",
        "problem":             "4–16 hr DAST scan queue; high false positive rate wastes security team time",
        "improvement":         "AI DAST tools learn application behaviour and perform targeted intelligent fuzzing. ML-based result filtering reduces false positives by 70%.",
        "agent":               "AI DAST Tools",
        "type":                "AI Automation",
        "expectedPTReduction": 50, "expectedWTReduction": 65,
        "timeToValue":         "4–5 weeks", "roi": "2.8×", "effort": "Medium",
        "bestPractices":       ["Intelligent fuzzing", "AI-driven DAST", "Risk-based scan scheduling"],
        "competitorInsight":   "StackHawk, OWASP ZAP AI used for continuous security testing in DevSecOps pipelines",
    },
    "Incident Management & RCA": {
        "title":               "AI Incident Auto-Triage — Severity & Owner Assignment",
        "problem":             "20–60 min to triage and route incidents; on-call engineers spend 40% of incident time on diagnosis vs resolution",
        "improvement":         "AI Incident Triage auto-classifies severity, identifies probable owner, pulls relevant runbook sections, and drafts initial customer communication. MTTR reduced by 45%.",
        "agent":               "AI Incident Triage",
        "type":                "AI Automation",
        "expectedPTReduction": 55, "expectedWTReduction": 70,
        "timeToValue":         "4–6 weeks", "roi": "4.2×", "effort": "Medium",
        "bestPractices":       ["AIOps", "Auto-remediation", "ML-based anomaly detection"],
        "competitorInsight":   "PagerDuty AI, Dynatwick Davis AI used by Fortune 500 ops teams",
    },
}


async def run_improvement_generator(state: VSMAgentState) -> VSMAgentState:
    """Generate improvement actions for each identified bottleneck."""
    logger.info("[Improvement Generator] Generating improvement actions")

    bottlenecks = state.get("bottlenecks", [])
    improvements = []
    imp_id = 1

    for bn in bottlenecks:
        activity_name = bn.get("activity", "").replace("[Phase Level] ", "")
        catalogue_entry = IMPROVEMENT_CATALOGUE.get(activity_name)

        if catalogue_entry:
            improvements.append({
                "id":           f"imp-{imp_id}",
                "bottleneckId": bn.get("id", ""),
                # camelCase phase fields matching frontend
                "phaseId":      bn.get("phaseId") or bn.get("phase_id"),
                "phaseName":    bn.get("phaseName") or bn.get("phase_name", ""),
                "activity":     activity_name,
                "priority":     "High" if bn.get("severity") in ("Critical", "High") else "Medium",
                "bottleneckSeverity": bn.get("severity", ""),
                **catalogue_entry,
            })
        else:
            improvements.append(_generic_improvement(bn, imp_id))

        imp_id += 1

    # Add improvements for activities not covered by bottlenecks
    for act in ALL_ACTIVITIES.values():
        if not any(i.get("activity") == act["name"] for i in improvements):
            catalogue_entry = IMPROVEMENT_CATALOGUE.get(act["name"])
            if catalogue_entry:
                improvements.append({
                    "id":        f"imp-{imp_id}",
                    "phaseId":   act["phase_id"],
                    "phaseName": act["phase_name"],
                    "activity":  act["name"],
                    "priority":  "Medium",
                    **catalogue_entry,
                    "source":    "Activity Opportunity",
                })
            else:
                improvements.append({
                    "id":                  f"imp-{imp_id}",
                    "phaseId":             act["phase_id"],
                    "phaseName":           act["phase_name"],
                    "activity":            act["name"],
                    "priority":            "Medium",
                    "title":               f"AI Automation for {act['name']}",
                    "problem":             f"Default effort {act['effort']['min']}–{act['effort']['max']}h with {act['wait']['min']}–{act['wait']['max']} wait",
                    "improvement":         f"Deploy {act['agent']} to automate or accelerate {act['name']}. Expected 30–50% effort reduction.",
                    "agent":               act["agent"],
                    "type":                act["type"],
                    "expectedPTReduction": 30, "expectedWTReduction": 40,
                    "timeToValue":         "4–8 weeks", "roi": "2.5×", "effort": "Medium",
                    "source":              "Activity Opportunity",
                })
            imp_id += 1

    # LLM enrichment: tailored GenAI recommendations for high-priority items
    if has_llm():
        high_pri = [i for i in improvements if i.get("priority") == "High"][:5]
        improvements = await _llm_enrich_improvements(high_pri, improvements, state)

    # Sort by priority then phase
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    improvements.sort(key=lambda i: (priority_order.get(i.get("priority", "Medium"), 1), i.get("phaseId", 0)))

    return {**state, "improvements": improvements, "recommendations": improvements}


async def _llm_enrich_improvements(high_pri: list, all_improvements: list, state: dict) -> list:
    """Use LLM to generate tailored improvement details with competitor insights."""
    project = state.get("project", {})
    metrics  = state.get("metrics", {})

    bottleneck_list = "\n".join(
        f"- {i['activity']} ({i.get('phaseName', '')}): {i.get('problem', '')}"
        for i in high_pri
    )
    prompt = f"""You are a world-class software engineering transformation expert specialising in GenAI-powered PDLC optimisation.

Team: {project.get('team', 'Engineering')}  Industry: {project.get('industry', 'Technology')}
Current Flow Efficiency: {metrics.get('overall_flow_efficiency', '?')}%
Current Lead Time: {metrics.get('total_lead_time_days', '?')} days

Top bottlenecks requiring improvement actions:
{bottleneck_list}

For each, provide a specific, actionable improvement recommendation that:
1. Names the exact GenAI agent, tool, or technique to deploy
2. Quantifies the expected PT and WT reduction (%)
3. References a real-world company and their measured outcome
4. Gives one specific quick-win implementable in < 2 weeks

Return ONLY a JSON array, no extra text:
[
  {{
    "activity": "<exact activity name>",
    "genaiRecommendation": "<specific GenAI/AI tool and how to deploy it>",
    "competitorInsight": "<real company, tool, and measured outcome>",
    "quickWin": "<one specific first step implementable in < 2 weeks>",
    "expectedPTReduction": <number 0–90>,
    "expectedWTReduction": <number 0–95>
  }},
  ...
]"""
    try:
        import json, re
        raw = await ainvoke(prompt)
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if not match:
            return all_improvements
        enrichments = json.loads(match.group())
        enrichment_map = {e["activity"]: e for e in enrichments}
        for imp in all_improvements:
            e = enrichment_map.get(imp.get("activity", ""), {})
            if e:
                if e.get("genaiRecommendation"):  imp["genaiRecommendation"] = e["genaiRecommendation"]
                if e.get("competitorInsight"):     imp["competitorInsight"]   = e["competitorInsight"]
                if e.get("quickWin"):              imp["quickWin"]            = e["quickWin"]
                if e.get("expectedPTReduction"):   imp["expectedPTReduction"] = e["expectedPTReduction"]
                if e.get("expectedWTReduction"):   imp["expectedWTReduction"] = e["expectedWTReduction"]
    except Exception as ex:
        logger.warning(f"[Improvement Generator] LLM enrichment failed: {ex}")

    return all_improvements


def _generic_improvement(bn: dict, imp_id: int) -> dict:
    metric   = bn.get("metric", "wait")
    activity = bn.get("activity", "")
    return {
        "id":                  f"imp-{imp_id}",
        "bottleneckId":        bn.get("id", ""),
        "phaseId":             bn.get("phaseId") or bn.get("phase_id"),
        "phaseName":           bn.get("phaseName") or bn.get("phase_name", ""),
        "activity":            activity,
        "priority":            "High" if bn.get("severity") in ("Critical", "High") else "Medium",
        "bottleneckSeverity":  bn.get("severity", ""),
        "title":               f"Reduce {activity} {'Wait Time' if metric == 'wait' else 'Effort'}",
        "problem":             bn.get("impact", "Flow bottleneck identified"),
        "improvement":         f"Apply AI automation and Lean principles to reduce {metric} for {activity}. Eliminate handoff wait, parallelise work, automate repetitive steps.",
        "agent":               "AI Automation",
        "type":                "AI Automation",
        "expectedPTReduction": 30, "expectedWTReduction": 50,
        "timeToValue":         "4–8 weeks", "roi": "2.0×", "effort": "Medium",
    }
