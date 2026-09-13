"""One-shot seed endpoint — creates demo projects + assessment + VSM + analysis + target state."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import json

from ..database.db import get_db
from ..database.models import (
    Project, ManualAssessmentResponse, VSMSnapshot, AnalysisRun, TargetStateConfig,
)

router = APIRouter(tags=["seed"])

US_BANK_ID  = "75651cda-4725-407c-a4e3-430d0137c2b3"
CENTRICA_ID = "86148f61-b697-4761-be69-16c9b0d8b4d4"

DEMO_PROJECTS = [
    {
        "id": US_BANK_ID,
        "name": "US Bank — Digital Banking Platform",
        "organization": "US Bank",
        "industry": "Banking & Financial Services",
        "team": "BeCloud",
        "product_groups": json.dumps([
            {"name": "RetailNL Tech", "products": [
                {"name": "Tribe APF", "teams": ["BeCloud"]},
                {"name": "Tribe Payments", "teams": ["PARN"]},
            ]}
        ]),
    },
    {
        "id": CENTRICA_ID,
        "name": "Centrica UK — Digital Transformation",
        "organization": "Centrica",
        "industry": "Energy & Utilities",
        "team": "Digital Platform",
        "product_groups": json.dumps([
            {"name": "Energy Platform", "products": [
                {"name": "Smart Home", "teams": ["Digital Platform"]},
                {"name": "Billing Engine", "teams": ["Payments Team"]},
            ]}
        ]),
    },
]

DEMO_TEAMS = [
    {
        "product_group": "RetailNL Tech", "product": "Tribe APF", "team": "BeCloud",
        "assessor": "Rammurthy Mudaliar",
        "scores": {
            "q01": 1, "q02": 2, "q03": 3, "q04": 2, "q05": 1,
            "q06": 1, "q07": 3, "q08": 3, "q09": 3, "q10": 2,
            "q11": 2, "q12": 2, "q13": 1, "q14": 1, "q15": 2,
            "q16": 3, "q17": 2, "q18": 3, "q19": 3, "q20": 4,
            "q21": 3, "q22": 3, "q23": 2, "q24": 2, "q25": 1,
            "q26": 2, "q27": 1, "q28": 2, "q29": 4, "q30": 3,
        },
    },
    {
        "product_group": "RetailNL Tech", "product": "Tribe Payments", "team": "PARN",
        "assessor": "Jagannathan Jayaraaman",
        "scores": {
            "q01": 1, "q02": 2, "q03": 3, "q04": 3, "q05": 1,
            "q06": 1, "q07": 3, "q08": 3, "q09": 3, "q10": 2,
            "q11": 2, "q12": 2, "q13": 1, "q14": 1, "q15": 2,
            "q16": 3, "q17": 2, "q18": 3, "q19": 3, "q20": 4,
            "q21": 3, "q22": 3, "q23": 2, "q24": 2, "q25": 1,
            "q26": 2, "q27": 1, "q28": 2, "q29": 4, "q30": 3,
        },
    },
]


# ── VSM snapshot data (7 phases, 36 activities) ────────────────────────────────
def _build_vsm_data(variant="usbank"):
    """Build realistic VSM data with per-activity metrics.
    variant='usbank' gives a banking team profile (heavy compliance wait);
    variant='centrica' gives an energy/utility profile (heavy testing effort).
    """
    multiplier = 1.0 if variant == "usbank" else 1.15

    activities = [
        # Phase 1: Backlog & Roadmap
        {"activityId": "p1-a1", "phaseId": 1, "name": "Portfolio Epic / VSM Tracking",     "processTime": 12*multiplier, "waitTime": 16*multiplier},
        {"activityId": "p1-a2", "phaseId": 1, "name": "Product Roadmap Definition",         "processTime": 28*multiplier, "waitTime": 0},
        {"activityId": "p1-a3", "phaseId": 1, "name": "Feature Definition & Refinement",    "processTime": 6*multiplier,  "waitTime": 16*multiplier},
        {"activityId": "p1-a4", "phaseId": 1, "name": "BDD Scenario Writing",               "processTime": 3*multiplier,  "waitTime": 4*multiplier},
        {"activityId": "p1-a5", "phaseId": 1, "name": "User Story Creation & Refinement",   "processTime": 1.5*multiplier,"waitTime": 6*multiplier},
        # Phase 2: Architecture & UX Design
        {"activityId": "p2-a1", "phaseId": 2, "name": "Solution Architecture (High-Level)", "processTime": 12*multiplier, "waitTime": 40*multiplier},
        {"activityId": "p2-a2", "phaseId": 2, "name": "UX/UI Research & Wireframing",       "processTime": 16*multiplier, "waitTime": 28*multiplier},
        {"activityId": "p2-a3", "phaseId": 2, "name": "UX/UI High-Fidelity Design & Handoff","processTime": 28*multiplier,"waitTime": 28*multiplier},
        {"activityId": "p2-a4", "phaseId": 2, "name": "Technical Design (Low-Level)",       "processTime": 6*multiplier,  "waitTime": 4*multiplier},
        # Phase 3: Code Management
        {"activityId": "p3-a1", "phaseId": 3, "name": "Coding (Feature Development)",       "processTime": 20*multiplier, "waitTime": 0},
        {"activityId": "p3-a2", "phaseId": 3, "name": "Unit Testing",                       "processTime": 1.5*multiplier,"waitTime": 0},
        {"activityId": "p3-a3", "phaseId": 3, "name": "Code Quality / LGTM Analysis",       "processTime": 0.75*multiplier,"waitTime": 1*multiplier},
        {"activityId": "p3-a4", "phaseId": 3, "name": "Peer Code Review",                   "processTime": 1.5*multiplier,"waitTime": 14*multiplier},
        {"activityId": "p3-a5", "phaseId": 3, "name": "Knowledge Transfer / Documentation", "processTime": 5*multiplier,  "waitTime": 0},
        # Phase 4: Continuous Integration
        {"activityId": "p4-a1", "phaseId": 4, "name": "Build Process (CI)",                 "processTime": 0.75*multiplier,"waitTime": 2.5*multiplier},
        {"activityId": "p4-a2", "phaseId": 4, "name": "Static Code Analysis (SAST)",        "processTime": 0.75*multiplier,"waitTime": 2.5*multiplier},
        {"activityId": "p4-a3", "phaseId": 4, "name": "Artifact Creation & Registry",       "processTime": 0.75*multiplier,"waitTime": 0.75*multiplier},
        {"activityId": "p4-a4", "phaseId": 4, "name": "DEV Deployment",                     "processTime": 1.25*multiplier,"waitTime": 0.75*multiplier},
        # Phase 5: Continuous Testing
        {"activityId": "p5-a1", "phaseId": 5, "name": "Test Environment Setup",             "processTime": 5*multiplier,  "waitTime": 2.5*multiplier},
        {"activityId": "p5-a2", "phaseId": 5, "name": "Test Data Generation / Management",  "processTime": 5*multiplier,  "waitTime": 10*multiplier},
        {"activityId": "p5-a3", "phaseId": 5, "name": "Build Verification Testing (BVT)",   "processTime": 0.75*multiplier,"waitTime": 0.75*multiplier},
        {"activityId": "p5-a4", "phaseId": 5, "name": "Automated Component Regression",     "processTime": 1.5*multiplier,"waitTime": 0.75*multiplier},
        {"activityId": "p5-a5", "phaseId": 5, "name": "Automated Full Regression",          "processTime": 8*multiplier,  "waitTime": 2.5*multiplier},
        {"activityId": "p5-a6", "phaseId": 5, "name": "Automated Performance Testing",      "processTime": 28*multiplier, "waitTime": 3.5*multiplier},
        {"activityId": "p5-a7", "phaseId": 5, "name": "Dynamic Security Testing (DAST)",    "processTime": 3*multiplier,  "waitTime": 10*multiplier},
        {"activityId": "p5-a8", "phaseId": 5, "name": "Manual SIT / UAT / NF Signoff",      "processTime": 6*multiplier,  "waitTime": 3.5*multiplier},
        {"activityId": "p5-a9", "phaseId": 5, "name": "Defect Triage & Management",         "processTime": 5*multiplier,  "waitTime": 0},
        # Phase 6: Continuous Delivery
        {"activityId": "p6-a1", "phaseId": 6, "name": "Infrastructure as Code (IaC)",       "processTime": 10*multiplier, "waitTime": 0},
        {"activityId": "p6-a2", "phaseId": 6, "name": "Stage Deployment (SIT/UAT/Staging)", "processTime": 3*multiplier,  "waitTime": 10*multiplier},
        {"activityId": "p6-a3", "phaseId": 6, "name": "Release Gates / Approvals",          "processTime": 1.5*multiplier,"waitTime": 24*multiplier},
        {"activityId": "p6-a4", "phaseId": 6, "name": "Production Deployment",              "processTime": 2.5*multiplier,"waitTime": 16*multiplier},
        {"activityId": "p6-a5", "phaseId": 6, "name": "Release Notes Generation",           "processTime": 1.25*multiplier,"waitTime": 0},
        # Phase 7: Monitoring & Feedback
        {"activityId": "p7-a1", "phaseId": 7, "name": "Application Performance Monitoring (APM)","processTime": 3*multiplier,"waitTime": 0},
        {"activityId": "p7-a2", "phaseId": 7, "name": "Log Aggregation & Analysis",         "processTime": 2.5*multiplier,"waitTime": 0},
        {"activityId": "p7-a3", "phaseId": 7, "name": "Incident Management & RCA",          "processTime": 5*multiplier,  "waitTime": 20*multiplier},
        {"activityId": "p7-a4", "phaseId": 7, "name": "Customer Feedback Loop",             "processTime": 1.5*multiplier,"waitTime": 20*multiplier},
    ]

    phase_map = {}
    for act in activities:
        pid = act["phaseId"]
        if pid not in phase_map:
            phase_map[pid] = {"phaseId": pid, "processTime": 0, "waitTime": 0}
        phase_map[pid]["processTime"] += act["processTime"]
        phase_map[pid]["waitTime"]    += act["waitTime"]

    for p in phase_map.values():
        p["processTime"] = round(p["processTime"], 1)
        p["waitTime"]    = round(p["waitTime"], 1)
        p["leadTime"]    = round((p["processTime"] + p["waitTime"]) / 8, 1)

    for act in activities:
        act["processTime"] = round(act["processTime"], 2)
        act["waitTime"]    = round(act["waitTime"], 2)

    phases = sorted(phase_map.values(), key=lambda p: p["phaseId"])

    total_pt = sum(p["processTime"] for p in phases)
    total_wt = sum(p["waitTime"] for p in phases)
    fe = round(total_pt / (total_pt + total_wt) * 100, 1) if (total_pt + total_wt) else 0

    return {
        "phases": phases,
        "activities": activities,
        "summary": {
            "total_process_time": round(total_pt, 1),
            "total_wait_time": round(total_wt, 1),
            "total_lead_time": round((total_pt + total_wt) / 8, 1),
            "flow_efficiency": fe,
        },
    }


# ── Analysis result (bottlenecks + improvements + future states + benchmarks) ──
def _build_analysis_result(variant="usbank"):
    vsm = _build_vsm_data(variant)
    phases = vsm["phases"]

    bottlenecks = [
        {
            "phase_id": 2, "phase_name": "Architecture & UX Design",
            "severity": "critical",
            "description": "Long wait times in UX design approval and architecture review cycles create the largest bottleneck in the pipeline.",
            "flow_efficiency": round(phases[1]["processTime"] / (phases[1]["processTime"] + phases[1]["waitTime"]) * 100, 1),
            "wait_time_hours": phases[1]["waitTime"],
            "root_causes": ["Manual architecture review boards meet weekly", "UX signoff requires multiple stakeholders", "No parallel tracks for design and development"],
            "impact": "Adds 10-15 business days to every feature release",
        },
        {
            "phase_id": 5, "phase_name": "Continuous Testing",
            "severity": "high",
            "description": "Performance testing and test data management consume disproportionate effort with significant wait for environment provisioning.",
            "flow_efficiency": round(phases[4]["processTime"] / (phases[4]["processTime"] + phases[4]["waitTime"]) * 100, 1),
            "wait_time_hours": phases[4]["waitTime"],
            "root_causes": ["Test environments provisioned manually", "Test data not synthetic — relies on masked production copies", "Performance tests run only in dedicated windows"],
            "impact": "Testing phase alone accounts for 35% of total lead time",
        },
        {
            "phase_id": 6, "phase_name": "Continuous Delivery",
            "severity": "medium",
            "description": "Release gate approvals and production deployment windows create long wait queues.",
            "flow_efficiency": round(phases[5]["processTime"] / (phases[5]["processTime"] + phases[5]["waitTime"]) * 100, 1),
            "wait_time_hours": phases[5]["waitTime"],
            "root_causes": ["Change Advisory Board meets bi-weekly", "Production deployment restricted to maintenance windows", "Manual release checklist with 40+ items"],
            "impact": "Features wait 3-5 days in release queue after testing completes",
        },
    ]

    improvements = [
        {
            "id": "imp-1", "phase_id": 2, "priority": "P1",
            "title": "AI-Assisted Architecture Review",
            "description": "Deploy AI Architecture Advisor agent to pre-validate designs against org standards, reducing review board meetings from weekly to exception-only.",
            "expected_reduction_pct": 45,
            "effort": "Medium", "timeline": "8-12 weeks",
            "category": "AI Automation",
        },
        {
            "id": "imp-2", "phase_id": 5, "priority": "P1",
            "title": "Synthetic Test Data Generation",
            "description": "Implement AI DataGen Agent for on-demand synthetic test data, eliminating 10+ hour waits for masked production data.",
            "expected_reduction_pct": 60,
            "effort": "High", "timeline": "12-16 weeks",
            "category": "GenAI Agent",
        },
        {
            "id": "imp-3", "phase_id": 5, "priority": "P2",
            "title": "AI-Driven Test Orchestration",
            "description": "Deploy QA Orchestrator agent for intelligent test selection and parallel execution across environments.",
            "expected_reduction_pct": 35,
            "effort": "Medium", "timeline": "10-14 weeks",
            "category": "AI Automation",
        },
        {
            "id": "imp-4", "phase_id": 6, "priority": "P2",
            "title": "Automated Release Gates",
            "description": "Replace manual CAB review with AI Release Manager that validates compliance, security, and quality gates automatically.",
            "expected_reduction_pct": 70,
            "effort": "Medium", "timeline": "6-10 weeks",
            "category": "AI Automation",
        },
        {
            "id": "imp-5", "phase_id": 3, "priority": "P3",
            "title": "AI Code Review Acceleration",
            "description": "Deploy Code Reviewer agent for immediate first-pass review, reducing peer review wait from 14h to under 2h.",
            "expected_reduction_pct": 80,
            "effort": "Low", "timeline": "4-6 weeks",
            "category": "GenAI Agent",
        },
    ]

    future_states = {}
    for scenario, label, reduction in [("option-a", "Conservative", 0.25), ("option-b", "Moderate", 0.45), ("option-c", "Aggressive", 0.65)]:
        fs_phases = []
        for p in phases:
            new_pt = round(p["processTime"] * (1 - reduction * 0.3), 1)
            new_wt = round(p["waitTime"] * (1 - reduction), 1)
            fs_phases.append({
                "phaseId": p["phaseId"],
                "processTime": new_pt,
                "waitTime": new_wt,
                "leadTime": round((new_pt + new_wt) / 8, 1),
            })
        total_pt = sum(p["processTime"] for p in fs_phases)
        total_wt = sum(p["waitTime"] for p in fs_phases)
        fe = round(total_pt / (total_pt + total_wt) * 100, 1) if (total_pt + total_wt) else 0
        future_states[scenario] = {
            "label": label,
            "phases": fs_phases,
            "summary": {
                "total_process_time": round(total_pt, 1),
                "total_wait_time": round(total_wt, 1),
                "total_lead_time": round((total_pt + total_wt) / 8, 1),
                "flow_efficiency": fe,
            },
        }

    benchmarks = {
        "industry": "Banking & Financial Services" if variant == "usbank" else "Energy & Utilities",
        "phases": [
            {"phase_id": 1, "phase_name": "Backlog & Roadmap",       "industry_p50_pt": 25, "industry_p50_wt": 48,  "flow_efficiency_p75": 34},
            {"phase_id": 2, "phase_name": "Architecture & UX Design", "industry_p50_pt": 30, "industry_p50_wt": 96,  "flow_efficiency_p75": 24},
            {"phase_id": 3, "phase_name": "Code Management",          "industry_p50_pt": 20, "industry_p50_wt": 8,   "flow_efficiency_p75": 71},
            {"phase_id": 4, "phase_name": "Continuous Integration",    "industry_p50_pt": 3,  "industry_p50_wt": 4,   "flow_efficiency_p75": 43},
            {"phase_id": 5, "phase_name": "Continuous Testing",        "industry_p50_pt": 20, "industry_p50_wt": 16,  "flow_efficiency_p75": 55},
            {"phase_id": 6, "phase_name": "Continuous Delivery",       "industry_p50_pt": 6,  "industry_p50_wt": 48,  "flow_efficiency_p75": 11},
            {"phase_id": 7, "phase_name": "Monitoring & Feedback",     "industry_p50_pt": 5,  "industry_p50_wt": 12,  "flow_efficiency_p75": 29},
        ],
    }

    return {
        "vsm_analysis": vsm["summary"],
        "bottlenecks": bottlenecks,
        "improvements": improvements,
        "future_states": future_states,
        "benchmarks": benchmarks,
    }


# ── Target state composition (21 agents, 7 phases) ────────────────────────────
def _build_target_composition():
    return {
        "agents": [
            {"name": "Discovery Agent",      "phase": "Backlog & Roadmap",       "tool": "DEV Bridge",       "role_posture": "orchestrated", "activities": ["Product Roadmap Definition", "Feature Definition & Refinement"]},
            {"name": "Backlog Agent",         "phase": "Backlog & Roadmap",       "tool": "USB Docs",         "role_posture": "orchestrated", "activities": ["Portfolio Epic / VSM Tracking", "User Story Creation & Refinement"]},
            {"name": "Sprint Agent",          "phase": "Backlog & Roadmap",       "tool": "GitHub Copilot",   "role_posture": "independent",  "activities": ["BDD Scenario Writing"]},
            {"name": "Architecture Agent",    "phase": "Architecture & UX Design","tool": "USB Docs",         "role_posture": "orchestrated", "activities": ["Solution Architecture (High-Level)"]},
            {"name": "UI/UX Agent",           "phase": "Architecture & UX Design","tool": "UX Design Coder",  "role_posture": "orchestrated", "activities": ["UX/UI Research & Wireframing", "UX/UI High-Fidelity Design & Handoff"]},
            {"name": "Design Review Agent",   "phase": "Architecture & UX Design","tool": "Figma AI",         "role_posture": "independent",  "activities": ["Technical Design (Low-Level)"]},
            {"name": "Code Generator",        "phase": "Code Management",         "tool": "UX Design Coder",  "role_posture": "orchestrated", "activities": ["Coding (Feature Development)", "Unit Testing"]},
            {"name": "Code Reviewer",         "phase": "Code Management",         "tool": "Code Review Asst.","role_posture": "orchestrated", "activities": ["Code Quality / LGTM Analysis", "Peer Code Review"]},
            {"name": "Tech Debt Agent",       "phase": "Code Management",         "tool": "DEV Bridge",       "role_posture": "independent",  "activities": ["Knowledge Transfer / Documentation"]},
            {"name": "Build Agent",           "phase": "Continuous Integration",   "tool": "QA Suite",         "role_posture": "orchestrated", "activities": ["Build Process (CI)", "Artifact Creation & Registry"]},
            {"name": "Vuln. Fix Agent",       "phase": "Continuous Integration",   "tool": "App Vuln. Sol.",   "role_posture": "orchestrated", "activities": ["Static Code Analysis (SAST)"]},
            {"name": "Pipeline Agent",        "phase": "Continuous Integration",   "tool": "Log Analytics",    "role_posture": "independent",  "activities": ["DEV Deployment"]},
            {"name": "QA Orchestrator",       "phase": "Continuous Testing",       "tool": "Smart Tester",     "role_posture": "orchestrated", "activities": ["Test Environment Setup", "Test Data Generation / Management", "Build Verification Testing (BVT)", "Defect Triage & Management"]},
            {"name": "UAT Agent",             "phase": "Continuous Testing",       "tool": "QA Suite",         "role_posture": "orchestrated", "activities": ["Manual SIT / UAT / NF Signoff", "Automated Performance Testing", "Dynamic Security Testing (DAST)"]},
            {"name": "Regression Agent",      "phase": "Continuous Testing",       "tool": "USB Docs",         "role_posture": "independent",  "activities": ["Automated Component Regression", "Automated Full Regression"]},
            {"name": "Release Gate Agent",    "phase": "Continuous Delivery",      "tool": "App Vuln. Sol.",   "role_posture": "orchestrated", "activities": ["Release Gates / Approvals", "Release Notes Generation"]},
            {"name": "Deploy Agent",          "phase": "Continuous Delivery",      "tool": "DEV Bridge",       "role_posture": "orchestrated", "activities": ["Infrastructure as Code (IaC)", "Stage Deployment (SIT/UAT/Staging)"]},
            {"name": "Rollback Agent",        "phase": "Continuous Delivery",      "tool": "Log Analytics",    "role_posture": "independent",  "activities": ["Production Deployment"]},
            {"name": "Monitor Agent",         "phase": "Monitoring & Feedback",    "tool": "Log Analytics",    "role_posture": "orchestrated", "activities": ["Application Performance Monitoring (APM)", "Log Aggregation & Analysis"]},
            {"name": "Incident Triage",       "phase": "Monitoring & Feedback",    "tool": "USB Docs",         "role_posture": "orchestrated", "activities": ["Incident Management & RCA"]},
            {"name": "Compliance Agent",      "phase": "Monitoring & Feedback",    "tool": "Risk Asst.",       "role_posture": "independent",  "activities": ["Customer Feedback Loop"]},
        ],
        "human_roles": [
            "Product Owner", "Scrum Master", "Principal Engineer",
            "Security Architect", "Release Manager",
        ],
        "tools": [
            "DEV Bridge", "USB Docs", "GitHub Copilot", "UX Design Coder",
            "Figma AI", "Code Review Asst.", "QA Suite", "App Vuln. Sol.",
            "Log Analytics", "Smart Tester", "Risk Asst.",
        ],
    }


@router.post("/seed-demo")
async def seed_demo(db: AsyncSession = Depends(get_db)):
    from .manual_assessment import ASSESSMENT_QUESTIONS

    stats = {"projects": [], "assessment_responses": 0, "vsm_snapshots": 0,
             "analysis_runs": 0, "target_state_configs": 0}

    # ── 1. Projects ────────────────────────────────────────────────────────────
    for proj_data in DEMO_PROJECTS:
        existing = await db.execute(
            select(Project).where(Project.id == proj_data["id"])
        )
        if existing.scalar_one_or_none():
            stats["projects"].append(f"{proj_data['name']} (exists)")
            continue
        db.add(Project(**proj_data))
        stats["projects"].append(proj_data["name"])
    await db.commit()

    # ── 2. Manual Assessment Responses ─────────────────────────────────────────
    for proj_data in DEMO_PROJECTS:
        pid = proj_data["id"]
        for team_info in DEMO_TEAMS:
            for qid, score in team_info["scores"].items():
                q = next((q for q in ASSESSMENT_QUESTIONS if q["id"] == qid), None)
                if not q:
                    continue
                existing = await db.execute(
                    select(ManualAssessmentResponse).where(
                        ManualAssessmentResponse.project_id == pid,
                        ManualAssessmentResponse.question_id == qid,
                        ManualAssessmentResponse.team == team_info["team"],
                    )
                )
                if existing.scalar_one_or_none():
                    continue
                db.add(ManualAssessmentResponse(
                    project_id=pid,
                    phase_id=q["pillar_id"],
                    question_id=qid,
                    response=str(score),
                    respondent=team_info["assessor"],
                    product_group=team_info["product_group"],
                    product=team_info["product"],
                    team=team_info["team"],
                ))
                stats["assessment_responses"] += 1
    await db.commit()

    # ── 3. VSM Snapshots ──────────────────────────────────────────────────────
    for proj_id, variant in [(US_BANK_ID, "usbank"), (CENTRICA_ID, "centrica")]:
        existing = await db.execute(
            select(VSMSnapshot).where(VSMSnapshot.project_id == proj_id).limit(1)
        )
        if existing.scalar_one_or_none():
            continue
        vsm = _build_vsm_data(variant)
        db.add(VSMSnapshot(
            project_id=proj_id,
            source="sample",
            vsm_data=vsm,
            summary=vsm["summary"],
        ))
        stats["vsm_snapshots"] += 1
    await db.commit()

    # ── 4. Analysis Runs (completed) ──────────────────────────────────────────
    for proj_id, variant in [(US_BANK_ID, "usbank"), (CENTRICA_ID, "centrica")]:
        existing = await db.execute(
            select(AnalysisRun).where(
                AnalysisRun.project_id == proj_id,
                AnalysisRun.status == "complete"
            ).limit(1)
        )
        if existing.scalar_one_or_none():
            continue
        now = datetime.utcnow()
        db.add(AnalysisRun(
            project_id=proj_id,
            status="complete",
            agents_run=["vsm_analyzer", "bottleneck_analyzer", "improvement_generator",
                        "future_state_designer", "business_case_builder", "benchmark_agent"],
            result=_build_analysis_result(variant),
            created_at=now - timedelta(hours=1),
            completed_at=now,
        ))
        stats["analysis_runs"] += 1
    await db.commit()

    # ── 5. Target State Configs ───────────────────────────────────────────────
    for proj_id in [US_BANK_ID, CENTRICA_ID]:
        existing = await db.execute(
            select(TargetStateConfig).where(TargetStateConfig.project_id == proj_id).limit(1)
        )
        if existing.scalar_one_or_none():
            continue
        db.add(TargetStateConfig(
            project_id=proj_id,
            platform="homegrown",
            platform_kind="home_grown",
            target_composition=_build_target_composition(),
            current_level=1,
            target_level=5,
            interim_count=2,
            interim_levels=[2, 4, 5],
            risk_appetite="medium",
        ))
        stats["target_state_configs"] += 1
    await db.commit()

    return {"status": "ok", **stats}


# ── Full data import from local PostgreSQL export ────────────────────────────
from pydantic import BaseModel
from typing import Any


class FullSeedPayload(BaseModel):
    projects: list[dict[str, Any]] = []
    vsm_snapshots: list[dict[str, Any]] = []
    analysis_runs: list[dict[str, Any]] = []
    target_state_configs: list[dict[str, Any]] = []
    outcome_metric_snapshots: list[dict[str, Any]] = []
    manual_assessment_responses: list[dict[str, Any]] = []
    devops_assessments: list[dict[str, Any]] = []
    assessment_action_items: list[dict[str, Any]] = []
    platform_settings: list[dict[str, Any]] = []
    project_data_sources: list[dict[str, Any]] = []
    project_documents: list[dict[str, Any]] = []


@router.post("/seed-full")
async def seed_full(payload: FullSeedPayload, db: AsyncSession = Depends(get_db)):
    """Import a full data dump exported from local PostgreSQL.

    Wipes ALL existing data first (FK-safe child→parent order),
    then inserts everything from the payload (parent→child order).
    """
    from ..database.models import (
        Project, VSMSnapshot, AnalysisRun, TargetStateConfig,
        OutcomeMetricSnapshot, ManualAssessmentResponse, DevOpsAssessment,
        AssessmentActionItem, PlatformSettings, ProjectDataSource, ProjectDocument,
    )
    from datetime import datetime as dt
    from sqlalchemy import delete, text

    stats: dict[str, int] = {}

    def parse_dt(v):
        if v is None:
            return None
        if isinstance(v, dt):
            return v
        return dt.fromisoformat(v.replace("Z", "+00:00")) if isinstance(v, str) else v

    def fix_dates(row):
        for k in list(row.keys()):
            if k.endswith("_at") or k in ("completed_at", "reviewed_at", "last_synced"):
                row[k] = parse_dt(row[k])
        return row

    # ── 1. Wipe everything (children first to respect FK) ─────────────
    for tbl in [
        "assessment_action_items", "manual_assessment_responses",
        "outcome_metric_snapshots", "target_state_configs",
        "analysis_runs", "vsm_snapshots", "project_data_sources",
        "project_documents", "devops_assessments", "platform_settings",
        "activity_metrics", "metric_data_sources", "step_reviews",
        "scheduled_pipeline_runs", "projects",
    ]:
        await db.execute(text(f"DELETE FROM {tbl}"))
    await db.commit()

    # ── 2. Insert everything (parents first) ──────────────────────────
    table_map = [
        ("projects", Project),
        ("vsm_snapshots", VSMSnapshot),
        ("analysis_runs", AnalysisRun),
        ("target_state_configs", TargetStateConfig),
        ("outcome_metric_snapshots", OutcomeMetricSnapshot),
        ("manual_assessment_responses", ManualAssessmentResponse),
        ("devops_assessments", DevOpsAssessment),
        ("assessment_action_items", AssessmentActionItem),
        ("platform_settings", PlatformSettings),
        ("project_data_sources", ProjectDataSource),
    ]

    for key, model_cls in table_map:
        rows = getattr(payload, key, [])
        count = 0
        for row in rows:
            fix_dates(row)
            db.add(model_cls(**row))
            count += 1
        await db.commit()
        stats[key] = count

    doc_count = 0
    for doc in payload.project_documents:
        doc.pop("file_content", None)
        fix_dates(doc)
        db.add(ProjectDocument(**doc))
        doc_count += 1
    await db.commit()
    stats["project_documents"] = doc_count

    return {"status": "ok", "inserted": stats}
