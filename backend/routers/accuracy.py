"""
Accuracy & RAG scoring API
GET /api/v1/accuracy/{project_id}   — score full pipeline for a project
GET /api/v1/accuracy/demo           — demo score with sample state
GET /api/v1/accuracy/kb             — list knowledge base documents
GET /api/v1/accuracy/kb/search      — search knowledge base
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database.db import get_db
from ..database.models import Project, AnalysisRun, VSMSnapshot
from ..agents.accuracy_scorer import score_full_pipeline
from ..agents.rag_engine import retrieve, get_retrieval_stats
from ..agents.knowledge_base import KB_DOCUMENTS, KB_CATEGORIES

router = APIRouter(prefix="/accuracy", tags=["Accuracy & RAG"])


@router.get("/demo")
async def get_demo_accuracy():
    """Return accuracy scores for a demo/sample state (no project needed)."""
    sample_state = {
        "alm_raw_data": {"tool": "alm_csv", "source": "alm_csv", "tickets": 842, "sprints": 12},
        "vsm_data": {
            "phases": [
                {"id": 1, "name": "Backlog & Roadmap",        "process_time": 25, "wait_time": 48},
                {"id": 2, "name": "Architecture & UX",        "process_time": 30, "wait_time": 96},
                {"id": 3, "name": "Code Management",          "process_time": 20, "wait_time": 16},
                {"id": 4, "name": "Continuous Integration",   "process_time": 3,  "wait_time": 4},
                {"id": 5, "name": "Continuous Testing",       "process_time": 20, "wait_time": 40},
                {"id": 6, "name": "Continuous Delivery",      "process_time": 6,  "wait_time": 24},
                {"id": 7, "name": "Monitoring & Feedback",    "process_time": 5,  "wait_time": 12},
            ]
        },
        "metrics": {
            "total_pt": 109, "total_wt": 240, "total_lt": 349,
            "flow_efficiency": 23.8,
            "phase_metrics": {
                "1": {"pt": 25, "wt": 48, "fe": 34.2},
                "2": {"pt": 30, "wt": 96, "fe": 23.8},
                "3": {"pt": 20, "wt": 16, "fe": 55.6},
                "4": {"pt": 3,  "wt": 4,  "fe": 42.9},
                "5": {"pt": 20, "wt": 40, "fe": 33.3},
                "6": {"pt": 6,  "wt": 24, "fe": 20.0},
                "7": {"pt": 5,  "wt": 12, "fe": 29.4},
            }
        },
        "dora_calibration": {
            "deployment_frequency": "bi-weekly",
            "lead_time_days": 14.6,
            "change_failure_rate_pct": 12.3,
            "mttr_hours": 6.5,
        },
        "bottlenecks": [
            {"phase_id": 5, "activity": "Manual SIT/UAT",   "wait_time": 40, "process_time": 8,
             "severity": "critical", "root_cause": "Manual test environment setup and test data dependency"},
            {"phase_id": 6, "activity": "Release Gates",     "wait_time": 24, "process_time": 2,
             "severity": "high",     "root_cause": "CAB approval process requires 3-day advance notice"},
            {"phase_id": 2, "activity": "Architecture Review","wait_time": 32, "process_time": 4,
             "severity": "high",     "root_cause": "Sequential design reviews with limited stakeholder availability"},
            {"phase_id": 3, "activity": "Peer Code Review",  "wait_time": 16, "process_time": 3,
             "severity": "medium",   "root_cause": "Large PR sizes (avg 850 lines) causing long review queues"},
            {"phase_id": 5, "activity": "Performance Testing","wait_time": 20, "process_time": 12,
             "severity": "medium",   "root_cause": "Manual performance test scripting and environment provisioning"},
        ],
        "improvements": [
            {"activity": "Manual SIT/UAT",    "agent": "AI UAT Assistant",   "source": "catalogue",
             "effort_reduction_pct": 80, "wait_reduction_pct": 80, "roi_estimate": "2.4× ROI",
             "quick_win": True, "competitor_insight": "Humana reduced UAT wait by 78% with AI test automation"},
            {"activity": "Release Gates",     "agent": "AI Release Manager", "source": "catalogue",
             "effort_reduction_pct": 60, "wait_reduction_pct": 65, "roi_estimate": "3.1× ROI",
             "quick_win": False, "competitor_insight": "JPMorgan automated 70% of standard change approvals"},
            {"activity": "Architecture Review","agent": "AI Design Reviewer", "source": "catalogue",
             "effort_reduction_pct": 40, "wait_reduction_pct": 55, "roi_estimate": "1.9× ROI",
             "quick_win": True, "genai_recommendation": "Async review with AI pre-screening reduces queue by 55%"},
            {"activity": "Peer Code Review",  "agent": "ReviewAgent",        "source": "catalogue",
             "effort_reduction_pct": 40, "wait_reduction_pct": 70, "roi_estimate": "2.2× ROI",
             "quick_win": True, "competitor_insight": "GitHub Copilot Code Review reduces review time by 65%"},
            {"activity": "Performance Testing","agent": "AI Perf Analyzer",  "source": "catalogue",
             "effort_reduction_pct": 75, "wait_reduction_pct": 60, "roi_estimate": "3.5× ROI",
             "quick_win": False, "genai_recommendation": "AI-driven load test generation reduces scripting by 75%"},
        ],
        "future_states": [
            {"scenario": "option-a", "flow_efficiency": 42.0, "total_lt_days": 8.4,
             "narrative": "Option A introduces AI augmentation across testing and code review phases, "
                          "reducing wait time by 55% while maintaining existing team structure.",
             "llm_narrative": True, "investment_range": "$800K–$1.2M"},
            {"scenario": "option-b", "flow_efficiency": 58.0, "total_lt_days": 5.2,
             "narrative": "Option B implements hybrid intelligence with 12 AI agents replacing manual gates, "
                          "achieving daily deployments and 65% lead time reduction.",
             "llm_narrative": True, "investment_range": "$1.5M–$2.5M"},
            {"scenario": "option-c", "flow_efficiency": 76.0, "total_lt_days": 2.1,
             "narrative": "Option C transforms to AI-first operations with 22 agents and 2 human roles, "
                          "enabling continuous deployment and near-zero defect production releases.",
             "llm_narrative": True, "investment_range": "$3M–$5M"},
        ],
        "business_cases": [
            {"scenario": "option-a", "roi_multiple": 2.8, "investment_range": "$800K–$1.2M",
             "annual_benefits": "$1.9M", "payback_months": 21,
             "executive_summary": "Conservative AI augmentation delivering 2.8× ROI in 24 months.",
             "risks": ["Change management overhead", "Partial automation requires ongoing human oversight"]},
            {"scenario": "option-b", "roi_multiple": 3.8, "investment_range": "$1.5M–$2.5M",
             "annual_benefits": "$5.2M", "payback_months": 15,
             "executive_summary": "Balanced hybrid intelligence achieving daily deployments and 3.8× ROI.",
             "risks": ["18-month transformation timeline", "Skills gap for AI-native operations"]},
            {"scenario": "option-c", "roi_multiple": 5.5, "investment_range": "$3M–$5M",
             "annual_benefits": "$16.5M", "payback_months": 27,
             "executive_summary": "AI-first transformation delivering 5.5× ROI with near-zero manual toil.",
             "risks": ["High upfront investment", "Cultural transformation complexity", "2-role model requires careful change management"]},
        ],
    }
    context = {
        "industry": "Financial Services / Healthcare",
        "team": "Platform Engineering — Demo Team",
        "team_context": {
            "team_size": "45",
            "team_roles": "Engineers, QA, DevOps, Product",
            "source_control": "GitHub Enterprise",
            "cicd_platform": "GitHub Actions + Jenkins",
            "cloud_platform": "AWS + Azure",
            "alm_tool": "Jira Software",
            "compliance_frameworks": "HIPAA, SOX, PCI-DSS",
            "team_maturity": "WALK",
            "methodology": "Scaled Agile (SAFe)",
            "deploy_frequency": "bi-weekly",
            "leadership_sponsorship": "CTO + VP Engineering",
        },
        "provided_docs": {
            "doc1": "DevOps Maturity Assessment Report Q1 2025",
            "doc2": "DORA Benchmark Report 2024",
        },
    }
    return score_full_pipeline(sample_state, context)


@router.get("/{project_id}")
async def get_project_accuracy(project_id: str, db: AsyncSession = Depends(get_db)):
    """Return accuracy scores for a project's latest analysis run."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    # Get latest analysis run
    run_result = await db.execute(
        select(AnalysisRun)
        .where(AnalysisRun.project_id == project_id, AnalysisRun.status == "complete")
        .order_by(AnalysisRun.created_at.desc())
        .limit(1)
    )
    run = run_result.scalar_one_or_none()

    # Get latest VSM snapshot
    snap_result = await db.execute(
        select(VSMSnapshot)
        .where(VSMSnapshot.project_id == project_id)
        .order_by(VSMSnapshot.created_at.desc())
        .limit(1)
    )
    snap = snap_result.scalar_one_or_none()

    # Build state from available data
    state: dict = {}
    if snap:
        state["vsm_data"]     = snap.vsm_data or {}
        state["alm_raw_data"] = snap.raw_data or {}

    if run and run.result:
        r = run.result
        state["metrics"]        = r.get("metrics", {})
        state["bottlenecks"]    = r.get("bottlenecks", [])
        state["improvements"]   = r.get("improvements", [])
        state["future_states"]  = r.get("future_states", [])
        state["business_cases"] = r.get("business_cases", [])
        state["dora_calibration"] = r.get("dora_calibration", {})

    context = {
        "industry": project.industry or "",
        "team":     project.team or project.name,
    }

    # Extract playbook accuracy if available
    playbook_accuracy = None
    if run and run.result:
        playbook_accuracy = run.result.get("playbook", {}).get("accuracy_pct")

    scores = score_full_pipeline(state, context, playbook_accuracy)
    scores["project_id"]   = project_id
    scores["project_name"] = project.name
    scores["data_source"]  = "real_analysis" if run else ("vsm_snapshot" if snap else "no_data")
    return scores


@router.get("/kb/search")
async def search_kb(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=20),
    category: str = Query(None)
):
    """Search the knowledge base."""
    results = retrieve(q, top_k=top_k, category=category)
    return {
        "query": q,
        "results": results,
        "total_kb_docs": len(KB_DOCUMENTS),
    }


@router.get("/kb/all")
async def list_kb():
    """List all knowledge base documents."""
    return {
        "total": len(KB_DOCUMENTS),
        "categories": KB_CATEGORIES,
        "documents": [
            {"id": d["id"], "category": d["category"], "title": d["title"],
             "tags": d["tags"], "source": d["source"]}
            for d in KB_DOCUMENTS
        ]
    }
