"""
Business Case Builder Agent
Generates comprehensive business cases for each future state scenario:
  - Investment breakdown (tools, infra, implementation, training, change)
  - Annual benefits (TTM, productivity, quality, ops)
  - ROI timeline and payback period
  - Org change management requirements
  - Tools & platform changes
  - DevSecOps changes
  - AI Ops / production support changes
  - Product-centric ways of working changes
"""
import logging
from ..state import VSMAgentState

logger = logging.getLogger(__name__)

BUSINESS_CASES = {
    "option-a": {
        "investment_range":    "$800K – $1.5M",
        "roi_timeline":        "12–18 months",
        "roi_multiple":        2.8,
        "payback_months":      14,
        "investment": {
            "tools":           "$250K–$400K (AI tools, IDE plugins, platform licenses)",
            "infrastructure":  "$100K–$200K (GPU compute, vector DBs, API costs)",
            "implementation":  "$300K–$600K (integration, prompt engineering, testing)",
            "training":        "$100K–$200K (upskilling all PDLC personas)",
            "change_mgmt":     "$100K–$150K (org change management, communications)"
        },
        "annual_benefits": {
            "ttm_improvement":     "$600K–$900K (faster feature delivery, competitive advantage)",
            "productivity_gains":  "$400K–$600K (35% effort reduction across team)",
            "quality_improvement": "$200K–$300K (fewer defects, less rework)",
            "operational_savings": "$100K–$150K (automated testing, deployments)"
        },
        "org_changes": [
            "Upskill all PDLC personas in AI tool collaboration and prompt engineering",
            "Redefine roles to include AI supervision, output validation, and exception handling",
            "Establish AI Centre of Excellence (CoE) for governance and best practices",
            "Update ways of working guides for human-AI collaboration patterns",
            "Introduce mandatory AI literacy training for all team members"
        ],
        "tools_changes": [
            "Jira / ADO: Deploy AI-powered backlog management and VSM plugins",
            "GitHub: Roll out Copilot Enterprise for all developers",
            "Testing: Upgrade to AI-enhanced test frameworks (Playwright AI, Testim)",
            "CI/CD: Integrate ML-based build optimizers and AI-powered SAST",
            "Monitoring: Deploy AI APM (Dynatrace Davis AI or Datadog AI)"
        ],
        "devsecops_changes": [
            "Shift-left security with AI-assisted SAST/DAST integrated in every PR",
            "AI-generated IaC templates with automated security policy validation",
            "Continuous compliance evidence collection for audit trails",
            "AI-powered secret scanning and dependency vulnerability monitoring"
        ],
        "aiops_changes": [
            "AI-driven anomaly detection and auto-remediation for common issues",
            "Predictive scaling using ML traffic pattern analysis",
            "Automated incident routing with NLP-based categorization",
            "Continuous feedback loop: production insights → AI-prioritized backlog"
        ],
        "product_centric_changes": [
            "Reorganize from project to persistent product teams with stable membership",
            "OKRs tied to product outcomes and customer value, not delivery velocity",
            "Quarterly business review cadence enhanced by AI-generated insights",
            "Customer feedback continuously integrated into roadmap via AI analysis"
        ]
    },
    "option-b": {
        "investment_range":    "$1.2M – $2.2M",
        "roi_timeline":        "10–15 months",
        "roi_multiple":        3.8,
        "payback_months":      11,
        "investment": {
            "tools":           "$400K–$700K (selective AI platforms for high-impact phases)",
            "infrastructure":  "$200K–$350K (dedicated AI compute, model hosting)",
            "implementation":  "$400K–$800K (deep integrations, custom LangGraph agents)",
            "training":        "$100K–$200K (focused training for remaining human roles)",
            "change_mgmt":     "$150K–$200K (significant role restructuring support)"
        },
        "annual_benefits": {
            "ttm_improvement":     "$900K–$1.4M (55% faster delivery, market share)",
            "productivity_gains":  "$600K–$900K (55% effort reduction)",
            "quality_improvement": "$300K–$500K (AI-driven quality gates, fewer escapes)",
            "operational_savings": "$200K–$350K (automated ops and monitoring)"
        },
        "org_changes": [
            "Consolidate 8+ roles to 5 core roles: Product Owner, Tech Lead, Developer, QA Lead, DevOps",
            "Establish clear human-AI handoff protocols and escalation paths per phase",
            "Create AI Agent Operations team to manage, tune, and govern agents",
            "Redesign performance metrics to measure AI-human collaborative output",
            "Executive sponsorship program with monthly transformation governance reviews"
        ],
        "tools_changes": [
            "Consolidate ALM tools to 1–2 AI-native platforms (Linear, Shortcut or Jira AI)",
            "Deploy custom LangChain/LangGraph agent orchestration layer",
            "Replace manual test scripting with AI-generated and self-healing test suites",
            "Implement GitOps-native CI/CD with AI-driven release gating",
            "Unify observability into AI-powered single-pane-of-glass platform"
        ],
        "devsecops_changes": [
            "Zero-trust security model enforced by AI policy agents in every pipeline stage",
            "AI-generated and auto-updated runbooks after every incident",
            "Continuous compliance validation with AI audit agents (SOC2, ISO 27001)",
            "ML-based threat modeling integrated into architecture review process"
        ],
        "aiops_changes": [
            "Self-healing CI/CD pipelines with AI-driven failure prediction and prevention",
            "AIOps platform managing all production alerts, triage, and initial response",
            "Automated capacity planning using ML demand forecasting",
            "AI-powered post-incident learning with automatic backlog story creation"
        ],
        "product_centric_changes": [
            "Product teams own the full value stream from ideation to production support",
            "Eliminate hand-offs between development, testing, and operations functions",
            "Continuous product discovery embedded as a permanent ritual in product teams",
            "AI-generated real-time product performance dashboards for all stakeholders"
        ]
    },
    "option-c": {
        "investment_range":    "$2.5M – $4.5M",
        "roi_timeline":        "18–24 months",
        "roi_multiple":        5.5,
        "payback_months":      19,
        "investment": {
            "tools":           "$800K–$1.5M (comprehensive AI-native platform stack)",
            "infrastructure":  "$500K–$900K (enterprise AI compute, model fine-tuning infrastructure)",
            "implementation":  "$800K–$1.5M (end-to-end agent development, orchestration, integration)",
            "training":        "$200K–$300K (intensive training for Product Definer + Product Builder roles)",
            "change_mgmt":     "$300K–$500K (major org transformation, workforce transition plan)"
        },
        "annual_benefits": {
            "ttm_improvement":     "$1.8M–$2.8M (70% faster delivery, market leadership position)",
            "productivity_gains":  "$1.2M–$1.8M (70% effort reduction, 2-person core team)",
            "quality_improvement": "$500K–$800K (AI quality gates, near-zero rework)",
            "operational_savings": "$400K–$700K (fully autonomous operations)"
        },
        "org_changes": [
            "Restructure entire PDLC workforce to 2 core human roles: Product Definer and Product Builder",
            "Product Definer: sets strategic vision, outcomes, constraints, and acceptance criteria",
            "Product Builder: supervises agent orchestration, reviews outputs, manages exceptions",
            "Major workforce transition plan: reskilling, redeployment, and attrition management",
            "Board-level approval required for operating model change of this magnitude",
            "External change management specialist engagement strongly recommended"
        ],
        "tools_changes": [
            "Build or adopt AI-native product engineering platform (Devin AI, GitHub Copilot Workspace)",
            "Custom multi-agent orchestration using LangGraph / AutoGen / Agency Swarm",
            "AI-native project management replacing traditional Jira/ADO entirely",
            "Fully automated CI/CD/CD pipelines with AI decisions at every quality and release gate",
            "Integrated AI product analytics replacing all manual reporting and dashboards"
        ],
        "devsecops_changes": [
            "Fully AI-managed DevSecOps pipeline from code commit to production deployment",
            "AI security agents continuously monitoring, detecting, and auto-remediating threats",
            "Autonomous compliance management with human oversight only for regulatory exceptions",
            "AI-generated and maintained Architecture Decision Records (ADRs) and security reviews"
        ],
        "aiops_changes": [
            "Fully autonomous AIOps — zero Level 1 / Level 2 human intervention in production",
            "AI-driven continuous capacity, performance, and cost optimization",
            "Self-healing, self-scaling, and self-documenting production systems",
            "AI incident commander managing all production events with human escalation only for Sev-1"
        ],
        "product_centric_changes": [
            "Abolish traditional SDLC phase gates — move to continuous product evolution model",
            "Product Definer sets weekly outcome goals; AI agents execute and deliver autonomously",
            "Real-time customer intent detection feeding directly into AI-driven roadmap prioritization",
            "Proactive feature generation: AI identifies market opportunities before humans request them"
        ]
    }
}


async def run_business_case_builder(state: VSMAgentState) -> VSMAgentState:
    """Generate business cases for all 3 future state scenarios."""
    logger.info("[Business Case Builder] Building business cases for 3 scenarios")

    future_states = state.get("future_states", {})
    business_cases = {}

    for scenario_id, bc in BUSINESS_CASES.items():
        fs = future_states.get(scenario_id, {})
        vs_current = fs.get("vs_current", {})

        # Enrich with calculated metrics
        business_cases[scenario_id] = {
            **bc,
            "scenario_id":     scenario_id,
            "scenario_label":  fs.get("label", scenario_id),
            "scenario_title":  fs.get("title", ""),
            "metrics_summary": {
                "lt_reduction":  vs_current.get("lt_reduction_pct", 0),
                "fe_gain":       vs_current.get("fe_absolute_gain", 0),
                "pt_reduction":  vs_current.get("pt_reduction_pct", 0),
                "wt_reduction":  vs_current.get("wt_reduction_pct", 0)
            }
        }

    return {**state, "business_cases": business_cases}
