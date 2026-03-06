"""
Canonical PDLC data — Python mirror of frontend/src/data/pdlcPhases.js
Used by all backend agents for reference.
"""

PDLC_PHASES = [
    {
        "id": 1, "name": "Backlog & Roadmap",
        "effort_range": {"min": 31, "max": 74}, "wait_range": {"min": 3.5, "max": 9},
        "wait_unit": "days",
        "activities": [
            {"id": "p1-a1", "name": "Portfolio Epic / VSM Tracking",     "effort": {"min": 8, "max": 16},  "wait": {"min": 1,   "max": 3},   "agent": "AI VSM Analyzer",         "type": "AI Automation"},
            {"id": "p1-a2", "name": "Product Roadmap Definition",         "effort": {"min": 16, "max": 40}, "wait": {"min": 0,   "max": 0},   "agent": "AI Roadmap Assistant",    "type": "AI Automation"},
            {"id": "p1-a3", "name": "Feature Definition & Refinement",    "effort": {"min": 4,  "max": 8},  "wait": {"min": 1,   "max": 3},   "agent": "FeatureGen Agent",         "type": "GenAI Agent"},
            {"id": "p1-a4", "name": "BDD Scenario Writing",               "effort": {"min": 2,  "max": 4},  "wait": {"min": 0.5, "max": 1},   "agent": "ScenarioGen Agent",        "type": "GenAI Agent"},
            {"id": "p1-a5", "name": "User Story Creation & Refinement",   "effort": {"min": 1,  "max": 2},  "wait": {"min": 0.5, "max": 1},   "agent": "StoryGen Agent",           "type": "GenAI Agent"},
        ]
    },
    {
        "id": 2, "name": "Architecture & UX Design",
        "effort_range": {"min": 36, "max": 88}, "wait_range": {"min": 8, "max": 18.5},
        "wait_unit": "days",
        "activities": [
            {"id": "p2-a1", "name": "Solution Architecture (High-Level)", "effort": {"min": 8,  "max": 16}, "wait": {"min": 3,   "max": 7},   "agent": "AI Architecture Advisor", "type": "AI Automation"},
            {"id": "p2-a2", "name": "UX/UI Research & Wireframing",       "effort": {"min": 8,  "max": 24}, "wait": {"min": 2,   "max": 5},   "agent": "DesignGen Agent",          "type": "GenAI Agent"},
            {"id": "p2-a3", "name": "UX/UI High-Fidelity Design & Handoff","effort": {"min":16, "max": 40}, "wait": {"min": 2,   "max": 5},   "agent": "DesignGen Agent",          "type": "GenAI Agent"},
            {"id": "p2-a4", "name": "Technical Design (Low-Level)",       "effort": {"min": 4,  "max": 8},  "wait": {"min": 0.5, "max": 1},   "agent": "DesignDoc Agent",          "type": "GenAI Agent"},
        ]
    },
    {
        "id": 3, "name": "Code Management",
        "effort_range": {"min": 13, "max": 47}, "wait_range": {"min": 4, "max": 24},
        "wait_unit": "hours",
        "activities": [
            {"id": "p3-a1", "name": "Coding (Feature Development)",       "effort": {"min": 8,  "max": 32}, "wait": {"min": 0,   "max": 0},   "agent": "CodeGen Agent",            "type": "GenAI Agent"},
            {"id": "p3-a2", "name": "Unit Testing",                       "effort": {"min": 1,  "max": 2},  "wait": {"min": 0,   "max": 0},   "agent": "TestGen Agent",            "type": "GenAI Agent"},
            {"id": "p3-a3", "name": "Code Quality / LGTM Analysis",       "effort": {"min": 0.5,"max": 1},  "wait": {"min": 0.5, "max": 2},   "agent": "AI Code Quality Tools",   "type": "AI Automation"},
            {"id": "p3-a4", "name": "Peer Code Review",                   "effort": {"min": 1,  "max": 2},  "wait": {"min": 4,   "max": 24},  "agent": "ReviewAgent",              "type": "GenAI Agent"},
            {"id": "p3-a5", "name": "Knowledge Transfer / Documentation", "effort": {"min": 2,  "max": 8},  "wait": {"min": 0,   "max": 0},   "agent": "DocGen Agent",             "type": "GenAI Agent"},
        ]
    },
    {
        "id": 4, "name": "Continuous Integration",
        "effort_range": {"min": 2, "max": 6}, "wait_range": {"min": 3, "max": 10},
        "wait_unit": "hours",
        "activities": [
            {"id": "p4-a1", "name": "Build Process (CI)",                 "effort": {"min": 0.5,"max": 1},  "wait": {"min": 1,   "max": 4},   "agent": "AI Build Optimizer",      "type": "AI Automation"},
            {"id": "p4-a2", "name": "Static Code Analysis (SAST)",        "effort": {"min": 0.5,"max": 1},  "wait": {"min": 1,   "max": 4},   "agent": "AI SAST Tools",           "type": "AI Automation"},
            {"id": "p4-a3", "name": "Artifact Creation & Registry",       "effort": {"min": 0.5,"max": 1},  "wait": {"min": 0.5, "max": 1},   "agent": "AI Artifact Manager",     "type": "AI Automation"},
            {"id": "p4-a4", "name": "DEV Deployment",                     "effort": {"min": 0.5,"max": 2},  "wait": {"min": 0.5, "max": 1},   "agent": "AI Deployment Agent",     "type": "AI Automation"},
        ]
    },
    {
        "id": 5, "name": "Continuous Testing",
        "effort_range": {"min": 34, "max": 98}, "wait_range": {"min": 14.5, "max": 41},
        "wait_unit": "hours",
        "activities": [
            {"id": "p5-a1", "name": "Test Environment Setup",             "effort": {"min": 2,  "max": 8},  "wait": {"min": 1,   "max": 4},   "agent": "AI Environment Manager",  "type": "AI Automation"},
            {"id": "p5-a2", "name": "Test Data Generation / Management",  "effort": {"min": 2,  "max": 8},  "wait": {"min": 4,   "max": 16},  "agent": "DataGen Agent",            "type": "GenAI Agent"},
            {"id": "p5-a3", "name": "Build Verification Testing (BVT)",   "effort": {"min": 0.5,"max": 1},  "wait": {"min": 0.5, "max": 1},   "agent": "AI Test Selection",        "type": "AI Automation"},
            {"id": "p5-a4", "name": "Automated Component Regression",     "effort": {"min": 1,  "max": 2},  "wait": {"min": 0.5, "max": 1},   "agent": "AI Test Selection",        "type": "AI Automation"},
            {"id": "p5-a5", "name": "Automated Full Regression",          "effort": {"min": 4,  "max": 12}, "wait": {"min": 1,   "max": 4},   "agent": "AI Test Execution",        "type": "AI Automation"},
            {"id": "p5-a6", "name": "Automated Performance Testing",      "effort": {"min": 16, "max": 40}, "wait": {"min": 2,   "max": 5},   "agent": "AI Performance Analyzer", "type": "AI Automation"},
            {"id": "p5-a7", "name": "Dynamic Security Testing (DAST)",    "effort": {"min": 2,  "max": 4},  "wait": {"min": 4,   "max": 16},  "agent": "AI DAST Tools",           "type": "AI Automation"},
            {"id": "p5-a8", "name": "Manual SIT / UAT / NF Signoff",      "effort": {"min": 4,  "max": 8},  "wait": {"min": 2,   "max": 5},   "agent": "AI UAT Assistant",         "type": "AI Automation"},
            {"id": "p5-a9", "name": "Defect Triage & Management",         "effort": {"min": 2,  "max": 8},  "wait": {"min": 0,   "max": 0},   "agent": "AI Defect Triage",         "type": "AI Automation"},
        ]
    },
    {
        "id": 6, "name": "Continuous Delivery",
        "effort_range": {"min": 8, "max": 28}, "wait_range": {"min": 2, "max": 10},
        "wait_unit": "days",
        "activities": [
            {"id": "p6-a1", "name": "Infrastructure as Code (IaC)",       "effort": {"min": 4,  "max": 16}, "wait": {"min": 0,   "max": 0},   "agent": "IaC Agent",                "type": "GenAI Agent"},
            {"id": "p6-a2", "name": "Stage Deployment (SIT/UAT/Staging)", "effort": {"min": 2,  "max": 4},  "wait": {"min": 0.5, "max": 2},   "agent": "AI Deployment Agent",     "type": "AI Automation"},
            {"id": "p6-a3", "name": "Release Gates / Approvals",          "effort": {"min": 1,  "max": 2},  "wait": {"min": 1,   "max": 5},   "agent": "AI Release Manager",      "type": "AI Automation"},
            {"id": "p6-a4", "name": "Production Deployment",              "effort": {"min": 1,  "max": 4},  "wait": {"min": 0.5, "max": 3},   "agent": "AI Production Deploy",    "type": "AI Automation"},
            {"id": "p6-a5", "name": "Release Notes Generation",           "effort": {"min": 0.5,"max": 2},  "wait": {"min": 0,   "max": 0},   "agent": "ReleaseNotes Agent",       "type": "GenAI Agent"},
        ]
    },
    {
        "id": 7, "name": "Monitoring & Feedback",
        "effort_range": {"min": 6, "max": 18}, "wait_range": {"min": 2, "max": 8},
        "wait_unit": "days",
        "activities": [
            {"id": "p7-a1", "name": "Application Performance Monitoring (APM)", "effort": {"min": 2, "max": 4},  "wait": {"min": 0, "max": 0}, "agent": "AI APM (Davis AI)",   "type": "AI Automation"},
            {"id": "p7-a2", "name": "Log Aggregation & Analysis",         "effort": {"min": 1,  "max": 4},  "wait": {"min": 0,   "max": 0},   "agent": "AI Log Analyzer",          "type": "AI Automation"},
            {"id": "p7-a3", "name": "Incident Management & RCA",          "effort": {"min": 2,  "max": 8},  "wait": {"min": 1,   "max": 4},   "agent": "IncidentAgent",            "type": "GenAI Agent"},
            {"id": "p7-a4", "name": "Customer Feedback Loop",             "effort": {"min": 1,  "max": 2},  "wait": {"min": 1,   "max": 4},   "agent": "FeedbackAgent",            "type": "GenAI Agent"},
        ]
    },
]

# Flat activity lookup
ALL_ACTIVITIES = {
    act["id"]: {**act, "phase_id": phase["id"], "phase_name": phase["name"]}
    for phase in PDLC_PHASES
    for act in phase["activities"]
}

# Industry benchmark data (Lean VSM best-practice targets)
INDUSTRY_BENCHMARKS = {
    1: {"pt_p50": 25, "wt_p50": 48,  "fe_p75": 34, "label": "Backlog & Roadmap"},
    2: {"pt_p50": 30, "wt_p50": 96,  "fe_p75": 24, "label": "Architecture & UX Design"},
    3: {"pt_p50": 20, "wt_p50": 8,   "fe_p75": 71, "label": "Code Management"},
    4: {"pt_p50": 3,  "wt_p50": 4,   "fe_p75": 43, "label": "Continuous Integration"},
    5: {"pt_p50": 20, "wt_p50": 16,  "fe_p75": 55, "label": "Continuous Testing"},
    6: {"pt_p50": 6,  "wt_p50": 48,  "fe_p75": 11, "label": "Continuous Delivery"},
    7: {"pt_p50": 5,  "wt_p50": 12,  "fe_p75": 29, "label": "Monitoring & Feedback"},
}
