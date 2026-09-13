#!/usr/bin/env python3
"""
Centrica UK — STUMP Demo Seed Data
Adds a fully-populated Centrica UK organisation without touching any
existing projects or seed data.

Usage:
    python3 seed_centrica_uk.py [--base-url http://localhost:8001]

Requires the STUMP backend to be running.
"""

import sys
import json
import uuid
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ─── CLI ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--base-url",   default="http://localhost:8001", help="STUMP backend base URL")
parser.add_argument("--project-id", default=None,                    help="Existing project ID (skip project creation)")
args = parser.parse_args()
BASE = args.base_url.rstrip("/") + "/api/v1"

# ─── HTTP helpers ─────────────────────────────────────────────────────
def post(path, body, fatal=True):
    data = json.dumps(body).encode()
    req  = urllib.request.Request(f"{BASE}{path}", data=data,
                                  headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if fatal:
            print(f"  ERROR {e.code} {path}: {e.read().decode()[:300]}")
            sys.exit(1)
        return None

def get(path):
    req = urllib.request.Request(f"{BASE}{path}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return None

# ─── Healthcheck ──────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("  STUMP  ·  Centrica UK Demo Seed")
print(f"{'='*60}")
print(f"  Target: {BASE}")

health = get("/health")
if not health:
    print("\n  ERROR: Backend not reachable. Start it first:\n"
          "  cd backend && uvicorn main:app --reload --port 8001\n")
    sys.exit(1)
print(f"  Backend: {health.get('status','?')}\n")

# ─── 1. PROJECT ───────────────────────────────────────────────────────
print("▶  Creating project …")

if args.project_id:
    pid = args.project_id
    print(f"  Using existing project → id={pid}")
    proj = get(f"/projects/{pid}") or {"organization": "Centrica UK", "industry": "Energy & Utilities"}
else:
    pid = None

project_body = {
    "name": "Centrica UK — Digital Transformation",
    "organization": "Centrica UK",
    "industry": "Energy & Utilities",
    "portfolios": [
        "Consumer & Smart Home",
        "Energy Operations",
        "B2B Solutions",
        "Technology & Infrastructure",
    ],
    "product_groups": [
        {
            "name": "Customer Digital Platform",
            "products": [
                {
                    "name": "Customer Web Portal",
                    "description": "my.britishgas.co.uk — self-service for 8M+ consumer accounts",
                    "teams": [
                        {"name": "Web Platform Team",    "size": 12, "methodology": "SAFe Scrum",
                         "cloud": "Azure", "alm": "Jira"},
                        {"name": "Portal DevOps Team",   "size": 6,  "methodology": "Kanban",
                         "cloud": "Azure", "alm": "Jira"},
                    ],
                },
                {
                    "name": "British Gas Mobile App",
                    "description": "iOS & Android app (4.5★, 2M+ active users)",
                    "teams": [
                        {"name": "iOS Engineering",      "size": 8,  "methodology": "SAFe Scrum",
                         "cloud": "Azure", "alm": "Jira"},
                        {"name": "Android Engineering",  "size": 7,  "methodology": "SAFe Scrum",
                         "cloud": "Azure", "alm": "Jira"},
                    ],
                },
                {
                    "name": "Smart Home Hub",
                    "description": "Hive connected home — thermostats, lights, EV chargers, solar",
                    "teams": [
                        {"name": "Hive Platform Team",   "size": 14, "methodology": "Scrum",
                         "cloud": "AWS", "alm": "Azure DevOps"},
                        {"name": "IoT Firmware Team",    "size": 9,  "methodology": "Scrum",
                         "cloud": "AWS", "alm": "Azure DevOps"},
                    ],
                },
            ],
        },
        {
            "name": "Energy Operations Platform",
            "products": [
                {
                    "name": "Smart Meter Platform",
                    "description": "DCC-connected SMETS2 metering — 11M+ meters under management",
                    "teams": [
                        {"name": "Smart Meter Engineering", "size": 18, "methodology": "SAFe PI Planning",
                         "cloud": "Azure", "alm": "Jira"},
                        {"name": "Meter Data Services",     "size": 10, "methodology": "Kanban",
                         "cloud": "Azure", "alm": "Jira"},
                    ],
                },
                {
                    "name": "Grid Operations Dashboard",
                    "description": "Real-time half-hourly settlement, balancing, and constraint monitoring",
                    "teams": [
                        {"name": "Grid Tech Team",       "size": 11, "methodology": "Scrum",
                         "cloud": "AWS", "alm": "Jira"},
                        {"name": "Data & Analytics",     "size": 8,  "methodology": "Kanban",
                         "cloud": "AWS", "alm": "Jira"},
                    ],
                },
                {
                    "name": "Energy Trading System",
                    "description": "Wholesale gas & power trading, risk management & P&L reporting",
                    "teams": [
                        {"name": "Trading Tech Team",    "size": 13, "methodology": "Scrum",
                         "cloud": "Azure", "alm": "Azure DevOps"},
                    ],
                },
            ],
        },
        {
            "name": "B2B Solutions Platform",
            "products": [
                {
                    "name": "Business Energy Portal",
                    "description": "SME & I&C customer self-service — 500K+ business accounts",
                    "teams": [
                        {"name": "B2B Platform Team",   "size": 10, "methodology": "SAFe Scrum",
                         "cloud": "Azure", "alm": "Jira"},
                    ],
                },
                {
                    "name": "EV & Fleet Solutions",
                    "description": "EV charging infrastructure management for fleet operators",
                    "teams": [
                        {"name": "EV Integration Team", "size": 9,  "methodology": "Scrum",
                         "cloud": "AWS", "alm": "GitHub"},
                        {"name": "Fleet Analytics",     "size": 5,  "methodology": "Kanban",
                         "cloud": "AWS", "alm": "GitHub"},
                    ],
                },
                {
                    "name": "Energy Management API",
                    "description": "RESTful API platform for third-party integrators & DSR aggregators",
                    "teams": [
                        {"name": "API & Integration",   "size": 8,  "methodology": "Kanban",
                         "cloud": "Azure", "alm": "Azure DevOps"},
                    ],
                },
            ],
        },
        {
            "name": "Technology & Infrastructure",
            "products": [
                {
                    "name": "Cloud Enablement Platform",
                    "description": "Azure Landing Zones, IaC templates, DevSecOps toolchain",
                    "teams": [
                        {"name": "Cloud Platform Team", "size": 14, "methodology": "Kanban",
                         "cloud": "Azure", "alm": "Azure DevOps"},
                        {"name": "Security Engineering","size": 7,  "methodology": "Kanban",
                         "cloud": "Azure", "alm": "Azure DevOps"},
                    ],
                },
            ],
        },
    ],
    "portfolio":      "Consumer & Smart Home",
    "product_group":  "Customer Digital Platform",
    "product":        "Customer Web Portal",
    "team":           "Web Platform Team",
    "alm_tool":       "jira",
    "alm_config": {
        "tool":     "jira",
        "url":      "https://centrica.atlassian.net",
        "username": "devops-admin@centrica.com",
        "project":  "CDP",
        "board":    "Customer Digital Platform Board",
    },
}

if not args.project_id:
    proj = post("/projects/", project_body)
    pid  = proj["id"]
    print(f"  Created project → id={pid}")
    print(f"  Org: {proj['organization']}  |  Industry: {proj['industry']}")

# ── VSM already created? skip if project existed ──────────────────────
_skip_vsm = bool(args.project_id)

# ─── 2. VSM SNAPSHOT ──────────────────────────────────────────────────
# Centrica context: large UK energy & utility enterprise
#   - Complex regulatory compliance (Ofgem, FCA, DCC, GDPR)
#   - Monthly release windows (mandated CAB + Ofgem change notification periods)
#   - Mixture of cloud-native (Hive/EV) and legacy mainframe (billing, metering)
#   - High manual UAT burden for smart meter firmware releases
#   - Sequential Architecture Review Board with 9 TOGAF-certified architects
#
# All times in HOURS for consistency; summary converts to days.
print("\n▶  Creating VSM snapshot …")
if _skip_vsm:
    print("  (skipped — using existing snapshot)")
else:

phases_vsm = [
    {
        "id": 1, "name": "Backlog & Roadmap",
        "process_time": 38, "wait_time": 130,
        "activities": [
            {"id": "p1-a1", "name": "Portfolio Epic / VSM Tracking",      "process_time": 6,  "wait_time": 16, "is_value_add": True},
            {"id": "p1-a2", "name": "Product Roadmap Definition",          "process_time": 10, "wait_time": 40, "is_value_add": True},
            {"id": "p1-a3", "name": "Feature Definition & Refinement",     "process_time": 8,  "wait_time": 24, "is_value_add": True},
            {"id": "p1-a4", "name": "BDD Scenario Writing",                "process_time": 6,  "wait_time": 30, "is_value_add": True},
            {"id": "p1-a5", "name": "User Story Creation & Refinement",    "process_time": 8,  "wait_time": 20, "is_value_add": True},
        ],
        "bottleneck": False,
        "notes": "Backlog refinement hampered by competing regulatory roadmap items (Ofgem smart tariff mandate, DSR API requirements).",
    },
    {
        "id": 2, "name": "Architecture & UX Design",
        "process_time": 52, "wait_time": 344,
        "activities": [
            {"id": "p2-a1", "name": "Solution Architecture (High-Level)", "process_time": 12, "wait_time": 96,  "is_value_add": True},
            {"id": "p2-a2", "name": "UX/UI Research & Wireframing",       "process_time": 14, "wait_time": 72,  "is_value_add": True},
            {"id": "p2-a3", "name": "UX/UI High-Fidelity Design & Handoff","process_time": 16, "wait_time": 112, "is_value_add": True},
            {"id": "p2-a4", "name": "Technical Design (Low-Level)",        "process_time": 10, "wait_time": 64,  "is_value_add": True},
        ],
        "bottleneck": True,
        "notes": "Sequential Architecture Review Board (ARB) with 9 TOGAF architects meets fortnightly. "
                 "Average queue time for design sign-off is 14 days.",
    },
    {
        "id": 3, "name": "Code Management",
        "process_time": 32, "wait_time": 40,
        "activities": [
            {"id": "p3-a1", "name": "Coding (Feature Development)",        "process_time": 10, "wait_time": 8,  "is_value_add": True},
            {"id": "p3-a2", "name": "Unit Testing",                        "process_time": 6,  "wait_time": 4,  "is_value_add": True},
            {"id": "p3-a3", "name": "Code Quality / LGTM Analysis",        "process_time": 4,  "wait_time": 8,  "is_value_add": False},
            {"id": "p3-a4", "name": "Peer Code Review",                    "process_time": 8,  "wait_time": 16, "is_value_add": False},
            {"id": "p3-a5", "name": "Knowledge Transfer / Documentation",  "process_time": 4,  "wait_time": 4,  "is_value_add": False},
        ],
        "bottleneck": False,
        "notes": "PRs on the monolithic Billing Engine average 1,200 lines; review queue averages 2 days.",
    },
    {
        "id": 4, "name": "Continuous Integration",
        "process_time": 5, "wait_time": 10,
        "activities": [
            {"id": "p4-a1", "name": "Build Process (CI)",                  "process_time": 2, "wait_time": 3,  "is_value_add": True},
            {"id": "p4-a2", "name": "Static Code Analysis (SAST)",         "process_time": 1, "wait_time": 4,  "is_value_add": False},
            {"id": "p4-a3", "name": "Artifact Creation & Registry",        "process_time": 1, "wait_time": 2,  "is_value_add": True},
            {"id": "p4-a4", "name": "DEV Deployment",                      "process_time": 1, "wait_time": 1,  "is_value_add": True},
        ],
        "bottleneck": False,
        "notes": "Azure Pipelines build is reasonable but legacy billing module takes 28 min to compile.",
    },
    {
        "id": 5, "name": "Continuous Testing",
        "process_time": 42, "wait_time": 96,
        "activities": [
            {"id": "p5-a1", "name": "Test Environment Setup",             "process_time": 4,  "wait_time": 16, "is_value_add": False},
            {"id": "p5-a2", "name": "Test Data Generation / Management",  "process_time": 4,  "wait_time": 8,  "is_value_add": False},
            {"id": "p5-a3", "name": "Build Verification Testing (BVT)",   "process_time": 2,  "wait_time": 4,  "is_value_add": True},
            {"id": "p5-a4", "name": "Automated Component Regression",     "process_time": 4,  "wait_time": 8,  "is_value_add": True},
            {"id": "p5-a5", "name": "Automated Full Regression",          "process_time": 6,  "wait_time": 16, "is_value_add": True},
            {"id": "p5-a6", "name": "Automated Performance Testing",      "process_time": 6,  "wait_time": 8,  "is_value_add": True},
            {"id": "p5-a7", "name": "Dynamic Security Testing (DAST)",    "process_time": 4,  "wait_time": 8,  "is_value_add": False},
            {"id": "p5-a8", "name": "Manual SIT / UAT / NF Signoff",      "process_time": 10, "wait_time": 24, "is_value_add": False},
            {"id": "p5-a9", "name": "Defect Triage & Management",         "process_time": 2,  "wait_time": 4,  "is_value_add": False},
        ],
        "bottleneck": True,
        "notes": "Manual SIT/UAT for smart meter firmware and billing changes requires Ofgem-accredited testers. "
                 "Test environment provisioning is manual and shared across 6 teams.",
    },
    {
        "id": 6, "name": "Continuous Delivery",
        "process_time": 22, "wait_time": 208,
        "activities": [
            {"id": "p6-a1", "name": "Infrastructure as Code (IaC)",        "process_time": 4, "wait_time": 16,  "is_value_add": True},
            {"id": "p6-a2", "name": "Stage Deployment (SIT/UAT/Staging)",  "process_time": 4, "wait_time": 24,  "is_value_add": True},
            {"id": "p6-a3", "name": "Release Gates / Approvals",           "process_time": 6, "wait_time": 120, "is_value_add": False},
            {"id": "p6-a4", "name": "Production Deployment",               "process_time": 4, "wait_time": 40,  "is_value_add": True},
            {"id": "p6-a5", "name": "Release Notes Generation",            "process_time": 4, "wait_time": 8,   "is_value_add": False},
        ],
        "bottleneck": True,
        "notes": "CAB approval requires 5-business-day advance notice. Smart meter firmware updates require "
                 "Ofgem 28-day notification period. Release windows restricted to monthly Saturday maintenance slots.",
    },
    {
        "id": 7, "name": "Monitoring & Feedback",
        "process_time": 12, "wait_time": 56,
        "activities": [
            {"id": "p7-a1", "name": "Application Performance Monitoring (APM)", "process_time": 3, "wait_time": 8,  "is_value_add": True},
            {"id": "p7-a2", "name": "Log Aggregation & Analysis",               "process_time": 3, "wait_time": 16, "is_value_add": True},
            {"id": "p7-a3", "name": "Incident Management & RCA",                "process_time": 4, "wait_time": 24, "is_value_add": False},
            {"id": "p7-a4", "name": "Customer Feedback Loop",                   "process_time": 2, "wait_time": 8,  "is_value_add": True},
        ],
        "bottleneck": False,
        "notes": "P1 incident SLA is 4 hours for smart meter outages (Ofgem obligation). "
                 "Grafana + Azure Monitor deployed; RCA cycle averages 3 days.",
    },
]

total_pt = sum(ph["process_time"] for ph in phases_vsm)   # 203 h
total_wt = sum(ph["wait_time"]    for ph in phases_vsm)   # 884 h
total_lt = total_pt + total_wt                             # 1087 h
fe_pct   = round(total_pt / total_lt * 100, 1)            # ~18.7%

vsm_payload = {
    "source": "sample",
    "vsm_data": {
        "project_id":  pid,
        "project_name": "Centrica UK — Digital Transformation",
        "organization": "Centrica UK",
        "industry":     "Energy & Utilities",
        "phases": phases_vsm,
        "summary": {
            "total_pt_hours":    total_pt,
            "total_wt_hours":    total_wt,
            "total_lt_hours":    total_lt,
            "total_pt_days":     round(total_pt / 8, 1),
            "total_wt_days":     round(total_wt / 8, 1),
            "total_lt_days":     round(total_lt / 8, 1),
            "flow_efficiency":   fe_pct,
            "phase_count":       7,
            "activity_count":    36,
            "bottleneck_phases": [2, 5, 6],
        },
        "dora": {
            "deployment_frequency":    "monthly",
            "lead_time_days":          round(total_lt / 8, 1),
            "change_failure_rate_pct": 19.4,
            "mttr_hours":              11.2,
            "dora_tier":               "Medium (Approaching High)",
        },
        "context": {
            "team_size":             "142 (across 16 squads)",
            "methodology":           "Scaled Agile (SAFe 6.0)",
            "source_control":        "Azure DevOps + GitHub Enterprise",
            "cicd_platform":         "Azure Pipelines + GitHub Actions",
            "cloud_platform":        "Azure (primary) + AWS (Hive/EV)",
            "alm_tool":              "Jira + Azure Boards",
            "compliance_frameworks": "Ofgem Smart Metering, FCA SYSC, GDPR, Cyber Essentials+, PCI-DSS",
            "team_maturity":         "WALK",
            "deploy_frequency":      "monthly (restricted release windows)",
            "architecture":          "Hybrid — Cloud-native (Hive, EV) + Legacy mainframe (Billing, Metering)",
            "key_constraints":       [
                "Ofgem 28-day change notification for smart meter firmware",
                "FCA mandated change freeze periods (Q4)",
                "DCC interface changes require joint testing with Smart DCC Ltd",
                "Legacy COBOL billing engine limits CI velocity",
                "Shared test environments across 6 product teams",
            ],
        },
    },
}

snap = post(f"/vsm/{pid}", vsm_payload)
print(f"  Created VSM snapshot → id={snap['id']}")
print(f"  Flow Efficiency: {fe_pct}%  |  Lead Time: {round(total_lt/8,1)} days")

# ─── 3. ANALYSIS RUN ──────────────────────────────────────────────────
print("\n▶  Creating analysis run (bottlenecks + improvements + future states + business case) …")

analysis_result = {
    "status": "complete",
    "agents_run": [
        "alm_connector", "vsm_analyzer", "benchmark_agent",
        "bottleneck_analyzer", "improvement_generator",
        "future_state_designer", "business_case_builder",
    ],
    "vsm_data": {
        "project_id":   pid,
        "organization": "Centrica UK",
        "industry":     "Energy & Utilities",
        "phases":       phases_vsm,
    },
    "metrics": {
        "total_pt":       total_pt,
        "total_wt":       total_wt,
        "total_lt":       total_lt,
        "flow_efficiency": fe_pct,
        "total_lt_days":  round(total_lt / 8, 1),
        "phase_metrics": {
            "1": {"pt": 38,  "wt": 130, "lt": 168,  "fe": round(38/168*100,1)},
            "2": {"pt": 52,  "wt": 344, "lt": 396,  "fe": round(52/396*100,1)},
            "3": {"pt": 32,  "wt": 40,  "lt": 72,   "fe": round(32/72*100,1)},
            "4": {"pt": 5,   "wt": 10,  "lt": 15,   "fe": round(5/15*100,1)},
            "5": {"pt": 42,  "wt": 96,  "lt": 138,  "fe": round(42/138*100,1)},
            "6": {"pt": 22,  "wt": 208, "lt": 230,  "fe": round(22/230*100,1)},
            "7": {"pt": 12,  "wt": 56,  "lt": 68,   "fe": round(12/68*100,1)},
        },
        "dora_calibration": {
            "deployment_frequency":    "monthly",
            "lead_time_days":          round(total_lt/8,1),
            "change_failure_rate_pct": 19.4,
            "mttr_hours":              11.2,
        },
        "industry_comparison": {
            "flow_efficiency_p50":   24.0,
            "flow_efficiency_p75":   38.0,
            "lead_time_days_p50":    45,
            "centrica_percentile":   "~30th percentile vs utilities sector peers",
        },
    },

    # ── Bottlenecks ──────────────────────────────────────────────────
    "bottlenecks": [
        {
            "phase_id":    6,
            "phase_name":  "Continuous Delivery",
            "activity":    "Release Gates / CAB + Ofgem Notifications",
            "wait_time":   120,
            "process_time": 6,
            "severity":    "critical",
            "impact_score": 9.2,
            "root_cause":  (
                "CAB approval process mandates 5-business-day advance change request submission. "
                "Smart meter firmware updates require Ofgem 28-day notification. "
                "Monthly release windows restrict production deployments to one Saturday per month, "
                "creating a 3–4 week queue for changes ready ahead of the window."
            ),
            "waste_type":  "Waiting / Over-Processing",
            "remediation": (
                "Implement risk-tiered change classification: standard low-risk changes pre-approved via AI "
                "risk scoring, bypassing manual CAB. Engage Ofgem for SMETS2 firmware sandbox approval. "
                "Target bi-weekly deployment cadence via pre-approval playbooks."
            ),
            "competitor_insight": "Octopus Energy deploys 10× per day using risk-based automated change approval.",
        },
        {
            "phase_id":    2,
            "phase_name":  "Architecture & UX Design",
            "activity":    "Architecture Review Board (ARB) Sequential Sign-off",
            "wait_time":   112,
            "process_time": 12,
            "severity":    "critical",
            "impact_score": 8.7,
            "root_cause":  (
                "ARB meets fortnightly with 9 TOGAF architects. All solution designs require full ARB sign-off "
                "regardless of risk profile. Average queue is 14 days; hot topics can wait 3 cycles (42 days)."
            ),
            "waste_type":  "Waiting / Defects",
            "remediation": (
                "Implement async AI-assisted architecture review for standard patterns (API extensions, "
                "UI changes, cloud resource scaling). Reserve ARB for novel architectural decisions. "
                "Target 80% of PRDs reviewed within 3 days via AI pre-screening."
            ),
            "competitor_insight": "E.ON UK reduced architecture review cycle from 21 to 4 days with async AI review tooling.",
        },
        {
            "phase_id":    5,
            "phase_name":  "Continuous Testing",
            "activity":    "Manual SIT / UAT — Smart Meter & Billing",
            "wait_time":   24,
            "process_time": 10,
            "severity":    "high",
            "impact_score": 7.9,
            "root_cause":  (
                "Ofgem-accredited testers required for all smart meter firmware validation. "
                "Billing engine changes require end-to-end COBOL + cloud integration tests run manually. "
                "Shared SIT environment creates 3-day provisioning wait per release cycle."
            ),
            "waste_type":  "Waiting / Motion",
            "remediation": (
                "Deploy AI-assisted test data generation to reduce SIT data preparation by 70%. "
                "Containerise SIT environment using Terraform; provision on-demand in <15 min. "
                "Work with Ofgem to pre-certify AI-generated test evidence for low-risk firmware builds."
            ),
            "competitor_insight": "SSE Renewables reduced manual UAT by 72% by containerising environments and AI test generation.",
        },
        {
            "phase_id":    5,
            "phase_name":  "Continuous Testing",
            "activity":    "Test Environment Setup / Shared Env Contention",
            "wait_time":   16,
            "process_time": 4,
            "severity":    "high",
            "impact_score": 7.1,
            "root_cause":  (
                "6 product teams share 2 SIT environments and 1 performance environment. "
                "Environment booking is manual (Confluence calendar). Average wait 2 days; "
                "conflicts during PI boundaries can delay a team by 5+ days."
            ),
            "waste_type":  "Waiting",
            "remediation": (
                "Implement ephemeral environment provisioning using Azure Container Apps and Terraform. "
                "Each team gets an on-demand isolated SIT environment provisioned in <10 minutes. "
                "Estimated 90% reduction in environment wait time."
            ),
            "competitor_insight": "National Grid ESO reduced environment wait time by 88% with ephemeral Azure Container Apps.",
        },
        {
            "phase_id":    1,
            "phase_name":  "Backlog & Roadmap",
            "activity":    "Regulatory Feature Prioritisation Conflicts",
            "wait_time":   80,
            "process_time": 14,
            "severity":    "medium",
            "impact_score": 5.8,
            "root_cause":  (
                "Competing priorities from Ofgem mandates, FCA obligations, and commercial roadmap items "
                "cause backlog deadlock. Product Owners lack decision authority on regulatory vs commercial "
                "priority trade-offs without SVP involvement. Average PI Planning epic refinement backlog "
                "queue is 18 days."
            ),
            "waste_type":  "Waiting / Defects",
            "remediation": (
                "Implement AI-powered regulatory impact classifier to auto-tag epics with compliance "
                "obligation, deadline, and penalty risk score. Route high-risk regulatory items to fast-track "
                "lane with pre-delegated SVP authority. Target backlog-to-sprint average of 8 days."
            ),
        },
    ],

    # ── Improvements ─────────────────────────────────────────────────
    "improvements": [
        {
            "activity":            "Release Gates / CAB + Ofgem",
            "agent":               "AI Release Risk Classifier",
            "source":              "catalogue",
            "effort_reduction_pct": 65,
            "wait_reduction_pct":   72,
            "roi_estimate":        "3.4× ROI",
            "quick_win":           False,
            "implementation_weeks": 16,
            "complexity":          "Medium",
            "genai_recommendation": (
                "Fine-tune risk classification model on Centrica's 3-year CAB decision history. "
                "Standard low-risk changes (API parameter extensions, UI copy, config flags) auto-approved. "
                "High-risk changes (billing engine, DCC interface) retain manual CAB. "
                "Projected: 65% of monthly changes pre-approved; release cadence improves to bi-weekly."
            ),
            "competitor_insight": "Octopus Energy's automated change pipeline processes 8K changes/month with <0.1% rollback rate.",
            "regulatory_note": "Ofgem sandbox pre-approval pathway required for firmware changes; 6-month lead time.",
        },
        {
            "activity":            "Architecture Review Board",
            "agent":               "AI Architecture Advisor",
            "source":              "catalogue",
            "effort_reduction_pct": 50,
            "wait_reduction_pct":   78,
            "roi_estimate":        "2.9× ROI",
            "quick_win":           True,
            "implementation_weeks": 8,
            "complexity":          "Low",
            "genai_recommendation": (
                "Deploy GPT-4o fine-tuned on Centrica Architecture Decision Records (ADRs). "
                "AI pre-screens design docs against 140+ known architectural patterns and constraints. "
                "90% of standard API / UI designs resolved within 24 hours without ARB meeting. "
                "ARB retains review of novel distributed systems, data sovereignty, and DCC integration decisions."
            ),
            "competitor_insight": "Ørsted reduced architectural review cycle from 28 to 3 days with GPT-4 ADR screening.",
        },
        {
            "activity":            "Manual SIT / UAT",
            "agent":               "AI Test Intelligence Platform",
            "source":              "catalogue",
            "effort_reduction_pct": 70,
            "wait_reduction_pct":   65,
            "roi_estimate":        "3.7× ROI",
            "quick_win":           False,
            "implementation_weeks": 20,
            "complexity":          "High",
            "genai_recommendation": (
                "AI test generation from BDD scenarios covers 85% of regression cases automatically. "
                "Smart meter test data synthesised by AI from SMETS2 DCC message schemas. "
                "Containerised SIT environments provisioned on-demand via Terraform + Azure Container Apps. "
                "Manual testing retained for Ofgem-mandated accredited test evidence (15% of test scope)."
            ),
            "competitor_insight": "British Telecom reduced UAT cycle from 14 to 3 days with AI test generation + containerised envs.",
        },
        {
            "activity":            "Test Environment Setup",
            "agent":               "AI Environment Orchestrator",
            "source":              "catalogue",
            "effort_reduction_pct": 80,
            "wait_reduction_pct":   90,
            "roi_estimate":        "2.5× ROI",
            "quick_win":           True,
            "implementation_weeks": 6,
            "complexity":          "Low",
            "genai_recommendation": (
                "Replace Confluence calendar booking with GitOps-driven ephemeral environments. "
                "Each PR triggers an isolated SIT environment via Azure Container Apps + Bicep. "
                "Environment live in <8 minutes; auto-destroyed after 48 hours. "
                "Eliminates 100% of environment contention wait time."
            ),
        },
        {
            "activity":            "Peer Code Review",
            "agent":               "AI Code Review Assistant",
            "source":              "catalogue",
            "effort_reduction_pct": 45,
            "wait_reduction_pct":   60,
            "roi_estimate":        "2.2× ROI",
            "quick_win":           True,
            "implementation_weeks": 4,
            "complexity":          "Low",
            "genai_recommendation": (
                "GitHub Copilot Code Review + custom security rules for Centrica's PCI-DSS and GDPR patterns. "
                "AI pre-screens all PRs — flags security issues, COBOL integration anti-patterns, and "
                "missing unit tests before human reviewer. PR size limit enforced at 400 lines. "
                "Estimated 60% reduction in review wait time."
            ),
            "competitor_insight": "RWE reduced code review cycle from 48 to 18 hours with Copilot + mandatory PR size limits.",
        },
    ],

    # ── Future State Scenarios ────────────────────────────────────────
    "future_states": [
        {
            "scenario":       "option-a",
            "label":          "Option A — Augmentation",
            "flow_efficiency": 32.4,
            "total_lt_days":  52.0,
            "delta_lt_days":  -83.5,
            "delta_fe_pct":   13.7,
            "agents_deployed": 5,
            "human_roles_retained": "All 142",
            "investment_range": "£600K–£900K",
            "narrative": (
                "Option A introduces AI augmentation at the two critical bottlenecks: Architecture Review "
                "and Release Gates. An AI Architecture Advisor pre-screens 80% of design documents within "
                "24 hours, reducing ARB wait from 14 days to 3 days. An AI Release Risk Classifier pre-approves "
                "65% of standard changes, reducing release gate wait from 5 weeks to 10 days. All 142 team "
                "members are retained; AI acts as a force multiplier, not a replacement."
            ),
            "phase_targets": {
                "1": {"fe": 25.2, "lt_days": 21.0},
                "2": {"fe": 22.5, "lt_days": 25.0},
                "3": {"fe": 50.0, "lt_days":  9.0},
                "4": {"fe": 35.0, "lt_days":  1.9},
                "5": {"fe": 36.8, "lt_days": 17.2},
                "6": {"fe": 38.0, "lt_days": 10.4},
                "7": {"fe": 22.0, "lt_days":  8.5},
            },
            "key_initiatives": [
                "AI Architecture Advisor (GPT-4o on Centrica ADRs)",
                "AI Release Risk Classifier (CAB automation)",
                "GitHub Copilot Code Review + Centrica security rulesets",
                "Ephemeral SIT environments (Azure Container Apps + Bicep)",
            ],
            "regulatory_path": "Standard CAB automation approved; Ofgem sandbox pathway takes 6 months.",
        },
        {
            "scenario":       "option-b",
            "label":          "Option B — Hybrid Intelligence",
            "flow_efficiency": 51.8,
            "total_lt_days":  28.0,
            "delta_lt_days":  -107.5,
            "delta_fe_pct":   33.1,
            "agents_deployed": 10,
            "human_roles_retained": "95 (all senior roles; junior testing roles redeployed to SRE)",
            "investment_range": "£1.4M–£2.2M",
            "narrative": (
                "Option B deploys 10 AI agents across the full PDLC, targeting all 5 identified bottlenecks. "
                "AI-driven test generation replaces 70% of manual SIT/UAT. Ephemeral environments eliminate "
                "shared environment contention entirely. AI regulatory impact classifier accelerates backlog "
                "prioritisation. Bi-weekly deployments become achievable for non-firmware changes. "
                "Smart meter firmware retains monthly cadence pending Ofgem sandbox approval."
            ),
            "phase_targets": {
                "1": {"fe": 34.0, "lt_days": 11.2},
                "2": {"fe": 40.0, "lt_days":  8.5},
                "3": {"fe": 60.0, "lt_days":  7.5},
                "4": {"fe": 40.0, "lt_days":  1.5},
                "5": {"fe": 52.0, "lt_days": 10.8},
                "6": {"fe": 55.0, "lt_days":  6.0},
                "7": {"fe": 28.0, "lt_days":  6.5},
            },
            "key_initiatives": [
                "All Option A initiatives",
                "AI Test Intelligence Platform (BDD → automated tests)",
                "AI Environment Orchestrator (GitOps ephemeral envs)",
                "AI Regulatory Impact Classifier (backlog tagging)",
                "Intelligent UX Research Synthesiser (Figma AI + user feedback clustering)",
                "AI Pipeline Observability Agent (anomaly detection, auto-rollback)",
            ],
            "regulatory_path": "Ofgem sandbox approval required in months 4–10; firmware deployments unblocked by month 12.",
        },
        {
            "scenario":       "option-c",
            "label":          "Option C — AI-Native ADLC",
            "flow_efficiency": 73.5,
            "total_lt_days":   8.5,
            "delta_lt_days":  -127.0,
            "delta_fe_pct":   54.8,
            "agents_deployed": 16,
            "human_roles_retained": "60 (SREs, architects, product leaders, compliance owners)",
            "investment_range": "£3.2M–£5.5M",
            "narrative": (
                "Option C reimagines Centrica's PDLC as an AI-native Autonomous Delivery Loop (ADLC). "
                "16 purpose-built agents orchestrate end-to-end delivery from Epic creation to production. "
                "Continuous deployment (multiple times daily for web/mobile) with AI-managed risk gates. "
                "Smart meter platform moves to weekly firmware cycles after Ofgem ADLC framework approval. "
                "82 roles transitioned to Site Reliability, AI Operations, and Regulatory AI governance. "
                "Full carbon-aware deployment scheduling aligned with Centrica Net Zero 2035 commitments."
            ),
            "phase_targets": {
                "1": {"fe": 58.0, "lt_days": 3.5},
                "2": {"fe": 65.0, "lt_days": 2.8},
                "3": {"fe": 75.0, "lt_days": 2.5},
                "4": {"fe": 72.0, "lt_days": 0.5},
                "5": {"fe": 80.0, "lt_days": 2.8},
                "6": {"fe": 85.0, "lt_days": 1.2},
                "7": {"fe": 62.0, "lt_days": 2.2},
            },
            "key_initiatives": [
                "All Option B initiatives (evolved to autonomous mode)",
                "Autonomous Epic-to-Story Decomposition Agent",
                "Generative Architecture Agent (ADR synthesis + design generation)",
                "Autonomous Code Generation Agent (GitHub Copilot Workspace tier)",
                "AI Security & Compliance Gate (replaces manual penetration testing for 80% of scope)",
                "Ofgem Regulatory AI Framework — novel regulatory pathway engagement",
                "Carbon-Aware Deployment Scheduler (Net Zero 2035 alignment)",
            ],
            "regulatory_path": (
                "Requires 18-month Ofgem ADLC engagement. FCA AI governance framework compliance. "
                "Novel regulatory pathway — Centrica would be first UK energy company at this scale."
            ),
        },
    ],

    # ── Business Cases ────────────────────────────────────────────────
    "business_cases": [
        {
            "scenario":         "option-a",
            "label":            "Option A — Augmentation",
            "investment_range": "£600K–£900K",
            "annual_benefits":  "£2.1M",
            "roi_multiple":     2.8,
            "payback_months":   19,
            "npv_3yr":          "£3.4M",
            "irr_pct":          38,
            "executive_summary": (
                "Option A delivers targeted AI augmentation at the two highest-impact bottlenecks — "
                "Architecture Review and Release Gates — achieving a 2.8× ROI within 24 months. "
                "Lead time reduces by 60% (135 → 52 days). No organisational restructuring required; "
                "all 142 team members retained and augmented. Lowest risk path for regulatory and "
                "cultural change management."
            ),
            "benefit_breakdown": [
                {"category": "Engineering Productivity",      "annual_value": "£820K",  "driver": "65% ARB wait reduction × 52 architects/seniors"},
                {"category": "Faster Time-to-Market",         "annual_value": "£640K",  "driver": "2 additional release cycles/year × avg feature revenue"},
                {"category": "Release Gate Automation",       "annual_value": "£380K",  "driver": "CAB analyst time saved on 65% pre-approved changes"},
                {"category": "Defect Reduction (early catch)", "annual_value": "£260K",  "driver": "AI code review catching 40% of defects pre-UAT"},
            ],
            "cost_breakdown": [
                {"category": "AI Tooling Licences (year 1)",  "cost": "£180K"},
                {"category": "Integration & Configuration",    "cost": "£220K"},
                {"category": "Training & Change Management",   "cost": "£120K"},
                {"category": "Ofgem Sandbox Engagement",       "cost": "£80K"},
                {"category": "Contingency (15%)",              "cost": "£90K"},
            ],
            "risks": [
                "Ofgem sandbox approval for firmware pre-approval takes 6–9 months",
                "ARB cultural resistance to AI-assisted reviews",
                "CAB automation requires ITIL 4 practices alignment (3-month change freeze risk)",
            ],
            "strategic_alignment": [
                "Centrica Group Net Zero 2035 — faster delivery of smart meter & EV features",
                "Ofgem Smart Metering Implementation Programme (SMIP) deadline compliance",
                "£200M Centrica digital transformation programme Phase 2",
            ],
        },
        {
            "scenario":         "option-b",
            "label":            "Option B — Hybrid Intelligence",
            "investment_range": "£1.4M–£2.2M",
            "annual_benefits":  "£5.8M",
            "roi_multiple":     3.8,
            "payback_months":   14,
            "npv_3yr":          "£11.2M",
            "irr_pct":          62,
            "executive_summary": (
                "Option B deploys 10 AI agents across all 5 identified bottlenecks, reducing lead time "
                "by 79% (135 → 28 days) and achieving bi-weekly deployments for web/mobile products. "
                "3.8× ROI with 14-month payback driven by test automation (70% manual UAT eliminated), "
                "ephemeral environments (zero contention wait), and intelligent release management. "
                "47 junior testing roles transitioned to SRE and AI Operations by month 18."
            ),
            "benefit_breakdown": [
                {"category": "Test Automation (70% UAT elimination)", "annual_value": "£1.8M",  "driver": "47 QA FTE redeployed; reduced defect escape rate"},
                {"category": "Release Velocity (bi-weekly cadence)",  "annual_value": "£1.6M",  "driver": "5× additional release cycles × feature revenue contribution"},
                {"category": "Environment Cost Savings",              "annual_value": "£420K",  "driver": "Retire 2 dedicated SIT environments; Azure Container Apps PAYG"},
                {"category": "Architecture Review Acceleration",      "annual_value": "£680K",  "driver": "Architects freed from ARB queue for strategic work"},
                {"category": "Defect Reduction (AI quality gates)",   "annual_value": "£560K",  "driver": "AI security & regression catching 65% of defects pre-prod"},
                {"category": "Regulatory Feature Velocity",           "annual_value": "£740K",  "driver": "Ofgem mandates delivered 40% faster; avoiding penalty risk"},
            ],
            "cost_breakdown": [
                {"category": "AI Platform & Agent Licences",           "cost": "£380K"},
                {"category": "Custom Agent Development (10 agents)",   "cost": "£520K"},
                {"category": "Infrastructure (Ephemeral Envs, Infra)", "cost": "£180K"},
                {"category": "Organisation Design & Reskilling",       "cost": "£320K"},
                {"category": "Ofgem / FCA Regulatory Engagement",      "cost": "£120K"},
                {"category": "Contingency (15%)",                      "cost": "£220K"},
            ],
            "risks": [
                "18-month transformation timeline with incremental value delivery milestones",
                "47-role transition requires robust reskilling programme (SRE, AI Ops pathways)",
                "DCC interface testing retains manual element until Ofgem sandbox confirmed",
                "FCA AI governance framework compliance adds 3-month review overhead",
            ],
            "strategic_alignment": [
                "Centrica Group 2030 Digital Strategy — AI-first operations target",
                "Ofgem SMIP Phase 3 acceleration",
                "British Gas Net Promoter Score improvement via faster feature delivery",
                "Hive Smart Home market leadership — bi-weekly IoT feature cadence",
            ],
        },
        {
            "scenario":         "option-c",
            "label":            "Option C — AI-Native ADLC",
            "investment_range": "£3.2M–£5.5M",
            "annual_benefits":  "£18.4M",
            "roi_multiple":     5.5,
            "payback_months":   26,
            "npv_3yr":          "£38.2M",
            "irr_pct":          87,
            "executive_summary": (
                "Option C transforms Centrica into the UK's first AI-native energy delivery organisation. "
                "16 agents orchestrate the full PDLC from Epic to Production with minimal human-in-the-loop. "
                "Lead time compresses from 135 to 8.5 days (94% reduction). Continuous deployment for "
                "web/mobile; weekly for smart home; monthly for regulated firmware (improving to weekly "
                "post-Ofgem ADLC framework). 82 roles transformed into SRE, AI Operations, and Regulatory "
                "AI governance functions. 5.5× ROI over 3 years; £38.2M NPV."
            ),
            "benefit_breakdown": [
                {"category": "Autonomous delivery velocity",          "annual_value": "£6.2M",  "driver": "Continuous deployment × full feature revenue realisation acceleration"},
                {"category": "Engineering headcount optimisation",     "annual_value": "£4.8M",  "driver": "82 roles transitioned; senior engineers retained for strategy"},
                {"category": "Defect & Incident cost elimination",    "annual_value": "£2.9M",  "driver": "AI quality gates reduce prod incidents by 75%; MTTR <30 min"},
                {"category": "Regulatory compliance automation",       "annual_value": "£1.8M",  "driver": "AI compliance agents eliminate manual audit prep for SOC2, PCI-DSS"},
                {"category": "Carbon-aware savings (Net Zero 2035)",   "annual_value": "£840K",  "driver": "Off-peak deployment scheduling reduces Azure compute cost 22%"},
                {"category": "Market differentiation (new products)",  "annual_value": "£1.8M",  "driver": "EV, Hive, DSR products to market 6 months earlier on average"},
            ],
            "cost_breakdown": [
                {"category": "AI Platform (enterprise tier)",          "cost": "£680K"},
                {"category": "Custom ADLC Agent Suite (16 agents)",    "cost": "£1.2M"},
                {"category": "Infrastructure Modernisation",           "cost": "£480K"},
                {"category": "Organisational Transformation (82 roles)","cost": "£920K"},
                {"category": "Ofgem ADLC Regulatory Pathway",          "cost": "£280K"},
                {"category": "FCA AI Governance Compliance",           "cost": "£180K"},
                {"category": "Contingency (15%)",                      "cost": "£560K"},
            ],
            "risks": [
                "No precedent for Ofgem ADLC approval — 18-month regulatory engagement minimum",
                "82-role transformation is largest workforce change in Centrica Technology since 2018",
                "COBOL Billing Engine must be modernised before autonomous code generation viable (24-month dependency)",
                "FCA mandates human-in-the-loop for financial product pricing changes — hard constraint",
                "Carbon-aware scheduler requires Azure carbon intensity API integration (6 months)",
            ],
            "strategic_alignment": [
                "Centrica Group 2035 Vision — AI-first energy services company",
                "Net Zero 2035 commitment — carbon-aware deployment scheduling",
                "UK Government AI Opportunities Action Plan — Centrica flagship case study potential",
                "Centrica Ventures AI portfolio — internal showcase for portfolio companies",
            ],
        },
    ],

    # ── Playbook ─────────────────────────────────────────────────────
    "playbook": {
        "organisation":    "Centrica UK",
        "industry":        "Energy & Utilities",
        "methodology":     "SAFe 6.0",
        "transformation_tier": "WALK → RUN",
        "accuracy_pct":    87.2,
        "key_regulatory_constraints": [
            "Ofgem Smart Metering Implementation Programme (SMIP)",
            "FCA SYSC operational resilience obligations",
            "GDPR / UK GDPR data minimisation for smart meter data",
            "DCC interface testing standards",
            "Cyber Essentials+ mandatory for energy CNI",
        ],
        "recommended_frameworks": [
            "DORA Act compliance mapping (operational resilience)",
            "Ofgem AI Sandbox (new regulatory pathway)",
            "NIST AI RMF for AI-assisted change management",
            "IEEE 7001 for autonomous deployment transparency",
        ],
        "quick_wins_90_days": [
            "Deploy GitHub Copilot Code Review with Centrica security rulesets (4 weeks)",
            "Implement ephemeral SIT environments via Azure Container Apps (6 weeks)",
            "AI Architecture Advisor pilot on CDP product group (8 weeks)",
            "Ofgem sandbox engagement letter submitted (2 weeks)",
        ],
    },
}

# Insert AnalysisRun directly into PostgreSQL (no seed endpoint on agents router)
async def _insert_analysis_run(project_id: str, result: dict) -> str:
    import asyncpg
    conn = await asyncpg.connect("postgresql://postgres@localhost:5432/stump_db")
    run_id = str(uuid.uuid4())
    now    = datetime.utcnow()
    await conn.execute(
        """INSERT INTO analysis_runs
               (id, project_id, status, agents_run, result, error, created_at, completed_at)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
        run_id,
        project_id,
        "complete",
        json.dumps(result["agents_run"]),
        json.dumps(result),
        None,
        now,
        now,
    )
    await conn.close()
    return run_id

run_resp = post(f"/agents/seed-result/{pid}", {
    "agents_run": analysis_result["agents_run"],
    "result":     analysis_result,
})
print(f"  Created analysis run → id={run_resp['id']}")

# ─── 4. DEVOPS MATURITY ASSESSMENT ────────────────────────────────────
print("\n▶  Creating DevOps maturity assessment …")

dora_resp = post("/devops-maturity/assessments", {
    "project_id":   pid,
    "organization": "Centrica UK",
    "portfolio":    "Consumer & Smart Home",
    "product_group": "Customer Digital Platform",
    "team_name":    "Web Platform Team",
    "industry":     "Energy & Utilities",
    "notes": (
        "Assessment conducted for Web Platform Team as representative cohort. "
        "Scores reflect Centrica's hybrid cloud-native / legacy mainframe estate. "
        "Smart meter and billing teams score 0.5–1.0 lower on CI/CD dimensions due to "
        "Ofgem regulatory constraints on deployment cadence."
    ),
    "sources": [
        {"type": "jira",   "url": "https://centrica.atlassian.net", "label": "Jira Software — CDP board"},
        {"type": "github", "url": "https://github.com/centrica",    "label": "GitHub Enterprise"},
    ],
})

assess_id = dora_resp.get("id")
if assess_id:
    print(f"  Created DevOps assessment → id={assess_id}")

    # Seed pre-scored responses (73 questions; scoring 1–5 per question)
    # Centrica profile: strong on monitoring/feedback, weak on deployment freq & test automation
    responses = {
        # ── D1: Source Code Management ──
        "d1-q1": {"manual_score": 4, "notes": "Git everywhere; GitFlow on legacy, trunk on new products"},
        "d1-q2": {"manual_score": 4, "notes": "PRs enforced; 2 approvals required"},
        "d1-q3": {"manual_score": 3, "notes": "Branch strategies inconsistent across legacy and new teams"},
        "d1-q4": {"manual_score": 3, "notes": "Secrets scanning in place but IaC not fully in source control"},
        "d1-q5": {"manual_score": 4, "notes": "Good commit hygiene on CDP; legacy billing team less consistent"},
        # ── D2: Build & CI ──
        "d2-q1": {"manual_score": 3, "notes": "Azure Pipelines on new products; Jenkins legacy for billing"},
        "d2-q2": {"manual_score": 3, "notes": "Build times 6–28 min; COBOL module slow"},
        "d2-q3": {"manual_score": 4, "notes": "Artifact registry (Azure Container Registry) standardised"},
        "d2-q4": {"manual_score": 3, "notes": "SAST (Checkmarx) integrated; not all repos covered"},
        "d2-q5": {"manual_score": 2, "notes": "Build failures not always addressed same-day; known flaky tests"},
        # ── D3: Test Automation ──
        "d3-q1": {"manual_score": 2, "notes": "Unit test coverage ~42% (below 70% target)"},
        "d3-q2": {"manual_score": 2, "notes": "Integration tests partial; UAT predominantly manual"},
        "d3-q3": {"manual_score": 3, "notes": "API regression automated via Postman/Newman collections"},
        "d3-q4": {"manual_score": 2, "notes": "Performance testing manual; scheduled monthly only"},
        "d3-q5": {"manual_score": 1, "notes": "Test data management entirely manual; GDPR-compliant synthetic data not in place"},
        # ── D4: Deployment & Release ──
        "d4-q1": {"manual_score": 2, "notes": "Monthly release windows; bi-weekly only for low-risk UI changes"},
        "d4-q2": {"manual_score": 2, "notes": "Blue-green on CDP web; canary not implemented"},
        "d4-q3": {"manual_score": 1, "notes": "Full manual CAB process; no risk-based automation"},
        "d4-q4": {"manual_score": 3, "notes": "IaC coverage ~60%; Terraform on new infra; manual for legacy VMs"},
        "d4-q5": {"manual_score": 2, "notes": "Rollback documented but tested only quarterly"},
        # ── D5: Monitoring & Observability ──
        "d5-q1": {"manual_score": 4, "notes": "Azure Monitor + Application Insights; Grafana dashboards"},
        "d5-q2": {"manual_score": 4, "notes": "ELK + Azure Log Analytics; good structured logging"},
        "d5-q3": {"manual_score": 3, "notes": "Distributed tracing partial (web only; billing not instrumented)"},
        "d5-q4": {"manual_score": 4, "notes": "PagerDuty alerting; P1/P2 SLAs well-defined (Ofgem obligation)"},
        "d5-q5": {"manual_score": 3, "notes": "SLOs defined for customer-facing services; smart meter SLOs TBD"},
        # ── D6: Security & Compliance ──
        "d6-q1": {"manual_score": 3, "notes": "Cyber Essentials+ certified; DAST (OWASP ZAP) on major releases"},
        "d6-q2": {"manual_score": 4, "notes": "GDPR/UK GDPR controls strong; Centrica DPO oversight"},
        "d6-q3": {"manual_score": 3, "notes": "Vulnerability patching SLA 30 days (critical 7 days)"},
        "d6-q4": {"manual_score": 2, "notes": "IAM inconsistent; PAM tooling not deployed for all environments"},
        "d6-q5": {"manual_score": 3, "notes": "Pen testing annual; no continuous security testing program"},
        # ── D7: Culture & Collaboration ──
        "d7-q1": {"manual_score": 3, "notes": "SAFe PI Planning every 12 weeks; good alignment on CDP"},
        "d7-q2": {"manual_score": 3, "notes": "Post-incident reviews conducted; action items tracked in Jira"},
        "d7-q3": {"manual_score": 3, "notes": "Blameless culture developing; some legacy team resistance"},
        "d7-q4": {"manual_score": 3, "notes": "OKRs at product level; inconsistent DORA metric tracking"},
        "d7-q5": {"manual_score": 2, "notes": "Knowledge silos between legacy mainframe and cloud-native teams"},
        # ── D8: Cloud & Infrastructure ──
        "d8-q1": {"manual_score": 3, "notes": "Azure Landing Zones deployed; ~35% of workloads still on VMs"},
        "d8-q2": {"manual_score": 3, "notes": "Containerisation ~50%; Kubernetes on CDP and Hive; billing not containerised"},
        "d8-q3": {"manual_score": 2, "notes": "Cost optimisation informal; FinOps practice nascent"},
        "d8-q4": {"manual_score": 3, "notes": "DR tested bi-annually; RTO/RPO defined for all Tier 1 services"},
        "d8-q5": {"manual_score": 2, "notes": "Auto-scaling configured for web tier only; smart meter platform manual scaling"},
    }

    # PATCH endpoint for responses
    data = json.dumps({"responses": responses}).encode()
    req  = urllib.request.Request(
        f"{BASE}/devops-maturity/assessments/{assess_id}/responses",
        data=data, headers={"Content-Type": "application/json"}, method="PATCH")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            pass
    except Exception:
        pass
    print(f"  Seeded {len(responses)} scored question responses")

    # Seed action items (top priorities from assessment)
    action_items_to_add = [
        {
            "assessment_id": assess_id,
            "question_id": "d4-q3",
            "dimension": "Deployment & Release",
            "competency": "Change Management Automation",
            "title": "Implement AI-Driven Risk-Based Change Classification",
            "description": (
                "Replace full manual CAB review with AI risk classifier trained on Centrica's 3-year "
                "change history. Standard low-risk changes (UI, config, API extensions) pre-approved. "
                "High-risk changes retain CAB. Target: 65% of changes pre-approved; bi-weekly cadence."
            ),
            "priority": "Critical",
            "current_score": 1.0,
            "target_score":  4.0,
            "current_level": "Initial",
            "target_level":  "Optimised",
            "suggested_actions": [
                "Train risk classification model on 3 years of CAB decisions (2022–2025)",
                "Define change risk taxonomy (Low/Medium/High/Regulatory)",
                "Pilot on CDP Web Portal product group for 3 months",
                "Submit automated change evidence framework to ITIL 4 change manager",
                "Engage Ofgem for sandbox firmware pre-approval pathway",
            ],
            "responsible": "Head of Delivery Excellence + ITIL Change Manager",
            "target_date":  "2026-12-31",
            "effort_estimate": "16 weeks",
        },
        {
            "assessment_id": assess_id,
            "question_id": "d3-q5",
            "dimension": "Test Automation",
            "competency": "Test Data Management",
            "title": "Deploy AI Synthetic Test Data Platform (GDPR-Compliant)",
            "description": (
                "Replace manual test data creation with AI-driven synthetic data generation. "
                "Synthesise realistic customer, smart meter, and billing data from production schemas "
                "without exposing PII. Eliminates GDPR risk in SIT environments; reduces test data "
                "preparation time by 85%."
            ),
            "priority": "Critical",
            "current_score": 1.0,
            "target_score":  4.0,
            "current_level": "Initial",
            "target_level":  "Managed",
            "suggested_actions": [
                "Evaluate Synthesised.io / Gretel.ai / Faker.js + custom SMETS2 schema generators",
                "Define data masking standards with Centrica DPO (GDPR Article 25)",
                "Integrate with Azure DevOps pipeline as a pre-test stage",
                "Validate synthetic data fidelity against production distributions",
            ],
            "responsible": "QE Lead + Data Privacy Officer",
            "target_date":  "2026-09-30",
            "effort_estimate": "10 weeks",
        },
        {
            "assessment_id": assess_id,
            "question_id": "d3-q1",
            "dimension": "Test Automation",
            "competency": "Unit & Integration Testing",
            "title": "Raise Unit Test Coverage from 42% to 75%",
            "description": (
                "Current 42% unit test coverage falls below industry threshold. Focus on Billing Engine "
                "(COBOL wrappers), Smart Meter Platform integration tests, and CDP Web Portal API layer. "
                "Use AI-assisted test generation (GitHub Copilot) to accelerate coverage uplift."
            ),
            "priority": "High",
            "current_score": 2.0,
            "target_score":  4.0,
            "current_level": "Repeatable",
            "target_level":  "Managed",
            "suggested_actions": [
                "Set coverage gate at 65% (CI will fail below threshold) — immediate",
                "Deploy GitHub Copilot for test generation on new code from month 2",
                "Identify top 20 uncovered billing engine classes; assign to team Q3",
                "Introduce mutation testing (PITest/Stryker) for quality gate by Q4",
            ],
            "responsible": "Engineering Leads (all 16 squads)",
            "target_date":  "2026-12-31",
            "effort_estimate": "20 weeks (parallel across teams)",
        },
        {
            "assessment_id": assess_id,
            "question_id": "d4-q2",
            "dimension": "Deployment & Release",
            "competency": "Progressive Delivery",
            "title": "Implement Canary Deployments for Customer Digital Platform",
            "description": (
                "CDP serves 8M+ customers; production incidents have direct customer impact and Ofgem "
                "reporting obligations. Canary deployment (5% → 20% → 100%) with automatic rollback "
                "on error rate spike reduces blast radius for every production release."
            ),
            "priority": "High",
            "current_score": 2.0,
            "target_score":  4.0,
            "current_level": "Repeatable",
            "target_level":  "Managed",
            "suggested_actions": [
                "Implement Azure Front Door traffic splitting for web portal",
                "Define automated rollback triggers (error rate >2%, P99 latency >3s)",
                "Instrument Application Insights for canary-specific metrics",
                "Run first canary release in staging environment within 6 weeks",
            ],
            "responsible": "Web Platform Team + Cloud Platform Team",
            "target_date":  "2026-08-31",
            "effort_estimate": "8 weeks",
        },
        {
            "assessment_id": assess_id,
            "question_id": "d8-q3",
            "dimension": "Cloud & Infrastructure",
            "competency": "Cloud Cost Optimisation",
            "title": "Establish FinOps Practice — Azure Cost Governance",
            "description": (
                "Centrica's Azure spend growing 28% YoY with no formal FinOps function. "
                "Implement tagging standards, showback dashboards, and rightsizing automation. "
                "Target 22% cost reduction within 12 months (estimated saving: £1.1M/yr)."
            ),
            "priority": "Medium",
            "current_score": 2.0,
            "target_score":  4.0,
            "current_level": "Repeatable",
            "target_level":  "Managed",
            "suggested_actions": [
                "Enforce mandatory cost-centre tagging on all Azure resources (Terraform policy)",
                "Deploy Azure Cost Management + Power BI showback dashboard",
                "Implement Azure Advisor rightsizing recommendations monthly review",
                "Introduce carbon-aware scheduling for non-prod workloads (Net Zero alignment)",
            ],
            "responsible": "Cloud Platform Team + Finance Business Partner",
            "target_date":  "2026-10-31",
            "effort_estimate": "12 weeks",
        },
    ]

    for item in action_items_to_add:
        post(f"/devops-maturity/assessments/{assess_id}/action-items", item, fatal=False)

    print(f"  Seeded {len(action_items_to_add)} action items")
else:
    print("  (DevOps assessment endpoint not available — skipping)")

# ─── SUMMARY ──────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("  SEED COMPLETE")
print(f"{'='*60}")
print(f"""
  Organisation  : Centrica UK
  Industry      : Energy & Utilities
  Project ID    : {pid}
  Project Name  : Centrica UK — Digital Transformation

  Portfolios    : 4 (Consumer & Smart Home, Energy Operations,
                    B2B Solutions, Technology & Infrastructure)
  Product Groups: 4
  Products      : 9
  Teams         : 16 squads (~142 FTE total)

  VSM State
  ─────────
  Lead Time     : {round(total_lt/8,1)} days  (industry median ~90d for utilities)
  Flow Efficiency: {fe_pct}%  (industry p50: 24%)
  Bottlenecks   : 3 critical phases (P2 ARB, P5 Testing, P6 Release Gates)
  DORA Tier     : Medium (monthly deploys, 19.4% CFR)

  Analysis Run  : 7 agents, 5 bottlenecks, 5 improvements, 3 scenarios
  Business Case : £600K–£5.5M investment range; 2.8–5.5× ROI
  DevOps Maturity: {len(responses)} questions scored; 5 critical action items

  ✓ No existing projects were modified.
  ✓ Load in STUMP UI → Switch Project → select "Centrica UK"
""")
