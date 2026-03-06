"""
Improvement Generator Agent
For each bottleneck, generates targeted improvement actions using:
  - GenAI / LLM agent solutions
  - Industry best practices (Lean, DORA, SAFe)
  - Competitor insights (FAANG, fintech leaders)
  - ROI estimates based on effort/wait reduction
"""
import logging
from ..state import VSMAgentState
from ..pdlc_data import ALL_ACTIVITIES

logger = logging.getLogger(__name__)

# Pre-built improvement catalogue aligned to PDLC activities
IMPROVEMENT_CATALOGUE = {
    "Automated Performance Testing": {
        "title":        "Deploy AI Performance Analyzer",
        "problem":      "16–40 hrs manual performance test authoring, analysis, and reporting",
        "improvement":  "Deploy AI Performance Analyzer to auto-detect regressions, correlate metrics with code changes, suggest root-cause fixes, and generate reports. Target: reduce to 4–8 hrs.",
        "agent":        "AI Performance Analyzer",
        "type":         "AI Automation",
        "pt_reduction": 75, "wt_reduction": 60,
        "time_to_value": "4–6 weeks", "roi": "3.2×", "effort": "Medium",
        "best_practices": ["Test Impact Analysis", "Parallel test execution", "AI anomaly detection"],
        "competitors":    "Netflix, Spotify use AI-driven performance regression detection"
    },
    "Manual SIT / UAT / NF Signoff": {
        "title":        "AI UAT Assistant + Risk-Based Automated Signoff",
        "problem":      "2–5 day human approval wait; manual test consolidation and reporting",
        "improvement":  "AI UAT Assistant consolidates all test results, generates risk-scored readiness reports with compliance evidence, enabling same-day signoff. Human reviews only risk-flagged items.",
        "agent":        "AI UAT Assistant",
        "type":         "AI Automation",
        "pt_reduction": 50, "wt_reduction": 80,
        "time_to_value": "6–8 weeks", "roi": "4.1×", "effort": "High",
        "best_practices": ["Continuous testing", "Risk-based signoff", "Test dashboard automation"],
        "competitors":    "Amazon deploys 23,000 times/day with automated quality gates"
    },
    "Peer Code Review": {
        "title":        "ReviewAgent — AI-Augmented Code Review",
        "problem":      "4–24 hr wait for reviewer availability; inconsistent review quality and coverage",
        "improvement":  "Deploy ReviewAgent to instantly analyse diffs, identify bugs/security/style issues, and produce structured summaries. Human reviewer focuses on architecture and business logic only.",
        "agent":        "ReviewAgent",
        "type":         "GenAI Agent",
        "pt_reduction": 40, "wt_reduction": 70,
        "time_to_value": "2–3 weeks", "roi": "5.0×", "effort": "Low",
        "best_practices": ["Automated PR analysis", "LLM-powered diff summarization", "Security linting"],
        "competitors":    "Google, Microsoft, Meta all use AI-assisted code review at scale"
    },
    "Test Data Generation / Management": {
        "title":        "DataGen Agent — On-Demand Synthetic Test Data",
        "problem":      "4–16 hr wait for test data provisioning; privacy/compliance risk with prod data copies",
        "improvement":  "DataGen Agent generates privacy-compliant synthetic data on-demand from database schemas, business rules, and constraints. Zero-wait data provisioning for all test environments.",
        "agent":        "DataGen Agent",
        "type":         "GenAI Agent",
        "pt_reduction": 60, "wt_reduction": 85,
        "time_to_value": "3–4 weeks", "roi": "3.8×", "effort": "Low",
        "best_practices": ["Synthetic data generation", "Schema-aware data masking", "GDPR-compliant TDM"],
        "competitors":    "HSBC, Barclays use synthetic data generation for PII-safe test environments"
    },
    "Release Gates / Approvals": {
        "title":        "AI Release Manager — Automated Gate Validation",
        "problem":      "1–5 day wait for CAB approval; manual risk assessment and evidence collection",
        "improvement":  "AI Release Manager auto-validates all release criteria (quality, security, performance), generates risk-scored assessment with compliance evidence. CAB approves exceptions only.",
        "agent":        "AI Release Manager",
        "type":         "AI Automation",
        "pt_reduction": 60, "wt_reduction": 75,
        "time_to_value": "6–10 weeks", "roi": "2.9×", "effort": "High",
        "best_practices": ["Continuous delivery", "Progressive delivery", "Automated compliance"],
        "competitors":    "Netflix, Spotify deploy continuously with automated risk gates"
    },
    "UX/UI High-Fidelity Design & Handoff": {
        "title":        "DesignGen Agent — AI-Accelerated Design & Handoff",
        "problem":      "16–40 hrs manual design + 2–5 day handoff wait; design-to-dev specification gaps",
        "improvement":  "DesignGen Agent applies style guides to wireframes, generates responsive mockups, and exports developer-ready specs (Figma tokens, CSS variables, component library mappings) automatically.",
        "agent":        "DesignGen Agent",
        "type":         "GenAI Agent",
        "pt_reduction": 50, "wt_reduction": 70,
        "time_to_value": "4–6 weeks", "roi": "3.1×", "effort": "Medium",
        "best_practices": ["Design system automation", "AI-assisted wireframing", "Token-based handoff"],
        "competitors":    "Figma AI, Adobe Firefly used by top-tier product teams"
    },
    "Feature Definition & Refinement": {
        "title":        "FeatureGen Agent — AI-Assisted Feature Authoring",
        "problem":      "4–8 hrs effort + 1–3 day iteration cycles between PM and BA",
        "improvement":  "FeatureGen Agent generates structured feature definitions, acceptance criteria, and BDD scenarios from high-level goals, accessing user personas and market data via RAG.",
        "agent":        "FeatureGen Agent",
        "type":         "GenAI Agent",
        "pt_reduction": 50, "wt_reduction": 70,
        "time_to_value": "2–4 weeks", "roi": "3.5×", "effort": "Low",
        "best_practices": ["AI-assisted requirements", "RAG-powered feature gen", "INVEST criteria validation"],
        "competitors":    "Linear, Notion AI used for AI-powered backlog management"
    },
    "Coding (Feature Development)": {
        "title":        "CodeGen Agent — AI Pair Programming",
        "problem":      "8–32 hrs effort; boilerplate overhead, context-switching, slow ramp-up",
        "improvement":  "Deploy AI coding assistant (GitHub Copilot / CodeGen Agent) for real-time suggestions, boilerplate generation, refactoring, and inline documentation. 30–40% effort reduction.",
        "agent":        "CodeGen Agent",
        "type":         "GenAI Agent",
        "pt_reduction": 35, "wt_reduction": 0,
        "time_to_value": "1–2 weeks", "roi": "4.5×", "effort": "Low",
        "best_practices": ["AI pair programming", "Code generation", "Intelligent autocompletion"],
        "competitors":    "GitHub reports 55% faster task completion with Copilot"
    },
    "Static Code Analysis (SAST)": {
        "title":        "ML-Powered SAST — Context-Aware Security Scanning",
        "problem":      "1–4 hr wait; high false-positive rate forces manual triaging by developers",
        "improvement":  "Upgrade to ML-powered SAST (Semgrep, Checkmarx One AI) with contextual vulnerability prioritization and auto-fix suggestions. 60% false positive reduction.",
        "agent":        "AI SAST Tools",
        "type":         "AI Automation",
        "pt_reduction": 40, "wt_reduction": 60,
        "time_to_value": "3–4 weeks", "roi": "2.5×", "effort": "Medium",
        "best_practices": ["Shift-left security", "ML-powered SAST", "Auto-remediation"],
        "competitors":    "Snyk, SonarQube AI used by top security-conscious engineering orgs"
    },
    "Dynamic Security Testing (DAST)": {
        "title":        "AI DAST — Intelligent Fuzzing & False Positive Reduction",
        "problem":      "4–16 hr wait for DAST scan completion; high false positive rate",
        "improvement":  "AI DAST tools learn application behaviour and perform targeted intelligent fuzzing. ML-based result filtering reduces false positives by 70%.",
        "agent":        "AI DAST Tools",
        "type":         "AI Automation",
        "pt_reduction": 50, "wt_reduction": 65,
        "time_to_value": "4–5 weeks", "roi": "2.8×", "effort": "Medium",
        "best_practices": ["Intelligent fuzzing", "AI-driven DAST", "Risk-based scan scheduling"],
        "competitors":    "StackHawk, OWASP ZAP AI used for continuous security testing"
    },
    "Incident Management & RCA": {
        "title":        "IncidentAgent — AI-Driven Incident Response",
        "problem":      "2–8 hrs effort + 1–4 day wait for RCA; manual triage and routing",
        "improvement":  "IncidentAgent auto-categorizes incidents, routes to correct team, suggests resolution playbooks, and generates structured RCA drafts. Reduces MTTR by 60%.",
        "agent":        "IncidentAgent",
        "type":         "GenAI Agent",
        "pt_reduction": 55, "wt_reduction": 70,
        "time_to_value": "4–6 weeks", "roi": "3.3×", "effort": "Medium",
        "best_practices": ["AIOps", "Auto-remediation", "ML-based anomaly detection"],
        "competitors":    "PagerDuty AI, Dynatrace Davis AI used by Fortune 500 ops teams"
    }
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
                "id":             f"imp-{imp_id}",
                "bottleneck_id":  bn["id"],
                "phase_id":       bn["phase_id"],
                "phase_name":     bn["phase_name"],
                "activity":       activity_name,
                "priority":       "High" if bn["severity"] in ("Critical", "High") else "Medium",
                **catalogue_entry,
                "bottleneck_severity": bn["severity"]
            })
        else:
            # Generate a generic improvement action
            improvements.append(_generic_improvement(bn, imp_id))

        imp_id += 1

    # Add improvements for all activities not covered by bottlenecks (from AI opportunity catalogue)
    for act in ALL_ACTIVITIES.values():
        if not any(i.get("activity") == act["name"] for i in improvements):
            improvements.append({
                "id":        f"imp-{imp_id}",
                "phase_id":  act["phase_id"],
                "phase_name":act["phase_name"],
                "activity":  act["name"],
                "priority":  "Medium",
                "title":     f"AI Automation for {act['name']}",
                "problem":   f"Default effort {act['effort']['min']}–{act['effort']['max']}h with {act['wait']['min']}–{act['wait']['max']} wait",
                "improvement": f"Deploy {act['agent']} to automate or accelerate {act['name']}. Expected 30–50% effort reduction.",
                "agent":     act["agent"],
                "type":      act["type"],
                "pt_reduction": 30, "wt_reduction": 40,
                "time_to_value": "4–8 weeks", "roi": "2.5×", "effort": "Medium",
                "source":    "Activity Opportunity"
            })
            imp_id += 1

    # Sort by priority and phase
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    improvements.sort(key=lambda i: (priority_order.get(i.get("priority", "Medium"), 1), i.get("phase_id", 0)))

    return {**state, "improvements": improvements, "recommendations": improvements}


def _generic_improvement(bn: dict, imp_id: int) -> dict:
    metric = bn.get("metric", "wait")
    activity = bn.get("activity", "")
    return {
        "id":        f"imp-{imp_id}",
        "phase_id":  bn["phase_id"],
        "phase_name":bn["phase_name"],
        "activity":  activity,
        "priority":  "High" if bn["severity"] in ("Critical", "High") else "Medium",
        "title":     f"Reduce {activity} {'Wait Time' if metric == 'wait' else 'Effort'}",
        "problem":   bn.get("impact", "Flow bottleneck identified"),
        "improvement": f"Apply AI automation and process improvements to reduce {metric} for {activity}. Consider lean principles: eliminate handoff wait, parallelize work, automate repetitive steps.",
        "agent":     "AI Automation",
        "type":      "AI Automation",
        "pt_reduction": 30, "wt_reduction": 50,
        "time_to_value": "4–8 weeks", "roi": "2.0×", "effort": "Medium"
    }
