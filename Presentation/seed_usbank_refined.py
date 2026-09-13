#!/usr/bin/env python3
"""
US Bank — STUMP Refined Demo Seed
Stage 1 = Option A (AI-Enabled, 16 tools)
Stage 2 = Option B (AI-First, 21 agents)
Stage 3 = Option C (AI-Native / ADLC, STUMP Platform)

Preserves existing product groups, products and teams 100%.
Only adds VSM snapshot + analysis run.

Usage:
    python3 seed_usbank_refined.py [--base-url http://localhost:8001]
"""
import sys, json, uuid, argparse, urllib.request, urllib.error
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://localhost:8001")
args = parser.parse_args()
BASE = args.base_url.rstrip("/") + "/api/v1"
PID  = "75651cda-4725-407c-a4e3-430d0137c2b3"   # US Bank — existing project

def post(path, body):
    data = json.dumps(body).encode()
    req  = urllib.request.Request(f"{BASE}{path}", data=data,
                                  headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  ERROR {e.code} {path}: {e.read().decode()[:300]}")
        sys.exit(1)

def put(path, body):
    data = json.dumps(body).encode()
    req  = urllib.request.Request(f"{BASE}{path}", data=data,
                                  headers={"Content-Type": "application/json"}, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError:
        return None

def get(path):
    req = urllib.request.Request(f"{BASE}{path}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError:
        return None

print(f"\n{'='*64}")
print("  STUMP  ·  US Bank Refined Demo Seed  (Stage 1/2/3 → A/B/C)")
print(f"{'='*64}")
health = get("/health")
if not health:
    print("\n  ERROR: Backend not reachable. Start with: uvicorn main:app --reload --port 8001\n")
    sys.exit(1)
print(f"  Backend: {health.get('status')}  |  Project: {PID[:8]}…")

# ─── PHASE DATA ───────────────────────────────────────────────────────
# US Bank context:
#   ALM/Dev stack : Jira · Confluence · GitLab · CloudBees · ServiceNow
#   Test stack    : PractiTest · BrowserStack · Smart Tester
#   Observability : AppDynamics · Splunk · Log Analytics
#   Security      : ShieldDocs · App Vuln. Solution
#   AI tools (16) : DEV Bridge, USB Docs, Backlog Asst., UX Design Coder,
#                   Figma AI, Code Review Asst., QA Suite, App Vuln. Solution,
#                   Log Analytics, Smart Tester, Risk Asst., GitHub Copilot,
#                   Azure OpenAI, MCP Layer, LangChain, Agent Skills
#   Compliance    : OCC, OFR, Dodd-Frank, PCI-DSS v4, SOX, BSA/AML
#   Methodology   : SAFe 6.0 — PI Planning every 10 weeks
#
# All times in HOURS.

# 36 activities across 7 phases — aligned with STUMP standard structure
# Phase names use STUMP canonical labels; US Bank tool names in activity titles
phases_vsm = [
    # ── Phase 1: Backlog & Roadmap (5 activities) ─────────────────────
    {
        "id": 1, "name": "Backlog & Roadmap",
        "usbank_label": "Discovery & Planning",
        "process_time": 28, "wait_time": 96,
        "activities": [
            {"id":"p1-a1","name":"Portfolio Epic / VSM Tracking",      "process_time":8, "wait_time":32,"is_value_add":True,
             "usbank_tool":"DEV Bridge","notes":"Feature ingestion from Confluence + customer feedback via DEV Bridge"},
            {"id":"p1-a2","name":"Product Roadmap Definition",          "process_time":8, "wait_time":24,"is_value_add":True,
             "usbank_tool":"USB Docs","notes":"Quarterly PI roadmap built in Confluence; USB Docs provides institutional context"},
            {"id":"p1-a3","name":"Feature Definition & Refinement",     "process_time":6, "wait_time":20,"is_value_add":True,
             "usbank_tool":"Backlog Asst. (partial)","notes":"Backlog Asst. deployed to 4/8 squads only; manual Jira authoring for rest"},
            {"id":"p1-a4","name":"BDD Scenario Writing",                "process_time":4, "wait_time":12,"is_value_add":True,
             "usbank_tool":"USB Docs","notes":"USB Docs provides regulatory acceptance criteria templates (PCI-DSS, BSA/AML)"},
            {"id":"p1-a5","name":"User Story Creation & Refinement",    "process_time":2, "wait_time":8, "is_value_add":True,
             "usbank_tool":"Backlog Asst. (partial)","notes":"Sprint Agent not yet deployed; story sizing fully manual"},
        ],
        "bottleneck": False,
        "current_tools": ["Jira","Confluence","USB Docs (partial)","Backlog Asst. (partial)","DEV Bridge"],
        "notes": (
            "USB Docs and Backlog Asst. deployed but used inconsistently — 4 of 8 squads only. "
            "PMs still manually author Jira stories from Confluence requirements. "
            "PI Planning every 10 weeks creates batch dependency: features wait up to 4 weeks "
            "to be formally planned after discovery completes, driving the 96h wait time."
        ),
    },
    # ── Phase 2: Architecture & UX Design (4 activities) ──────────────
    {
        "id": 2, "name": "Architecture & UX Design",
        "usbank_label": "Architecture & Design",
        "process_time": 36, "wait_time": 160,
        "activities": [
            {"id":"p2-a1","name":"Solution Architecture (High-Level)",  "process_time":10,"wait_time":80,"is_value_add":True,
             "usbank_tool":"Confluence + ShieldDocs","notes":"EA Board meets fortnightly; ShieldDocs review sequential (not parallel) — combined 80h wait"},
            {"id":"p2-a2","name":"UX/UI Research & Wireframing",        "process_time":10,"wait_time":40,"is_value_add":True,
             "usbank_tool":"Figma + UX Design Coder (pilot)","notes":"UX Design Coder in pilot on Shop & Apply only; 6/8 squads use Figma manually"},
            {"id":"p2-a3","name":"UX/UI High-Fidelity Design & Handoff","process_time":12,"wait_time":24,"is_value_add":True,
             "usbank_tool":"Figma AI (pilot)","notes":"Figma AI in pilot on Shop & Apply; handoff to development manual for other squads"},
            {"id":"p2-a4","name":"Technical Design (Low-Level)",        "process_time":4, "wait_time":16,"is_value_add":True,
             "usbank_tool":"Confluence + USB Docs","notes":"LLD documented in Confluence; USB Docs provides US Bank architecture decision records (ADRs)"},
        ],
        "bottleneck": True,
        "current_tools": ["Confluence","Figma","ShieldDocs","UX Design Coder (pilot)","Figma AI (pilot)","USB Docs"],
        "notes": (
            "Enterprise Architecture Board meets fortnightly — 14-day minimum queue for any design. "
            "ShieldDocs security review runs sequentially after EA review (not parallel), adding 8–14 more days. "
            "UX Design Coder + Figma AI only on Shop & Apply pilot — 6/8 squads get no AI design assistance. "
            "Combined Phase 2 wait of 160h (20 days) is the longest non-delivery wait in the PDLC."
        ),
    },
    # ── Phase 3: Code Management (5 activities) ───────────────────────
    {
        "id": 3, "name": "Code Management",
        "usbank_label": "Development",
        "process_time": 20, "wait_time": 20,
        "activities": [
            {"id":"p3-a1","name":"Coding (Feature Development)",        "process_time":8, "wait_time":4, "is_value_add":True,
             "usbank_tool":"GitLab + VS Code + GitHub Copilot (pilot)","notes":"Copilot pilot on Avengers team; others use VS Code without AI assistance"},
            {"id":"p3-a2","name":"Unit Testing",                        "process_time":4, "wait_time":2, "is_value_add":True,
             "usbank_tool":"GitLab CI","notes":"Unit test coverage at 42%; below 70% target; QA Suite not used for test generation yet"},
            {"id":"p3-a3","name":"Code Quality / LGTM Analysis",        "process_time":2, "wait_time":4, "is_value_add":False,
             "usbank_tool":"Code Review Asst. (partial)","notes":"Code Review Asst. deployed to Honeybee + Rasabee only; 6 squads do manual LGTM"},
            {"id":"p3-a4","name":"Peer Code Review",                    "process_time":4, "wait_time":8, "is_value_add":False,
             "usbank_tool":"GitLab MR + Code Review Asst. (partial)","notes":"Salesforward MRs avg 780 lines; 2-reviewer policy; 12h avg wait across time zones"},
            {"id":"p3-a5","name":"Knowledge Transfer / Documentation",  "process_time":2, "wait_time":2, "is_value_add":False,
             "usbank_tool":"USB Docs + Confluence","notes":"USB Docs partially used for tech docs; inconsistent update discipline across squads"},
        ],
        "bottleneck": False,
        "current_tools": ["GitLab","VS Code","Code Review Asst. (partial)","DEV Bridge","GitHub Copilot (pilot)","USB Docs"],
        "notes": (
            "Development phase is relatively healthy but carries 3 improvement opportunities. "
            "Salesforward monolith MRs average 780 lines (target: 400). "
            "Code Review Asst. deployed to Honeybee/Rasabee only — 6 squads unprotected. "
            "GitHub Copilot in pilot on Avengers (1 squad); rest code without AI assistance."
        ),
    },
    # ── Phase 4: Continuous Integration (4 activities) ────────────────
    {
        "id": 4, "name": "Continuous Integration",
        "usbank_label": "Build & CI/CD",
        "process_time": 4, "wait_time": 8,
        "activities": [
            {"id":"p4-a1","name":"Build Process (CI)",                  "process_time":2, "wait_time":4, "is_value_add":True,
             "usbank_tool":"CloudBees CI","notes":"CloudBees well-configured; build times 8–28 min depending on product"},
            {"id":"p4-a2","name":"Static Code Analysis (SAST)",         "process_time":1, "wait_time":2, "is_value_add":False,
             "usbank_tool":"App Vuln. Solution","notes":"SAST integrated in CloudBees; scan results arrive but triage is manual"},
            {"id":"p4-a3","name":"Artifact Creation & Registry",        "process_time":0.5,"wait_time":1,"is_value_add":True,
             "usbank_tool":"CloudBees + JFrog Artifactory","notes":"Artifact management automated and consistent across all teams"},
            {"id":"p4-a4","name":"DEV Deployment",                      "process_time":0.5,"wait_time":1,"is_value_add":True,
             "usbank_tool":"CloudBees Deploy + Log Analytics","notes":"DEV environment deployment automated; Log Analytics confirms deployment health"},
        ],
        "bottleneck": False,
        "current_tools": ["CloudBees CI/CD","App Vuln. Solution","Log Analytics","GitLab CI","JFrog Artifactory"],
        "notes": (
            "CI is the strongest phase in US Bank's current PDLC. "
            "CloudBees pipeline is well-configured and consistent across all 5 products. "
            "Only gap: App Vuln. Solution scan results require manual triage — "
            "engineers receive vulnerabilities without AI-assisted prioritisation."
        ),
    },
    # ── Phase 5: Continuous Testing (9 activities) ────────────────────
    {
        "id": 5, "name": "Continuous Testing",
        "usbank_label": "Test & QA",
        "process_time": 28, "wait_time": 64,
        "activities": [
            {"id":"p5-a1","name":"Test Environment Setup",              "process_time":4, "wait_time":16,"is_value_add":False,
             "usbank_tool":"PractiTest (shared)","notes":"5 product teams share 2 PractiTest environments; Confluence calendar booking; avg 2-day wait"},
            {"id":"p5-a2","name":"Test Data Generation / Management",   "process_time":4, "wait_time":8, "is_value_add":False,
             "usbank_tool":"Manual (no tooling)","notes":"Test data fully manual; PII masking done manually; no synthetic data generation; GDPR/BSA/AML risk"},
            {"id":"p5-a3","name":"Build Verification Testing (BVT)",    "process_time":2, "wait_time":4, "is_value_add":True,
             "usbank_tool":"CloudBees + QA Suite (partial)","notes":"BVT automated on new products; Salesforward BVT partially manual"},
            {"id":"p5-a4","name":"Automated Component Regression",      "process_time":4, "wait_time":8, "is_value_add":True,
             "usbank_tool":"QA Suite (partial)","notes":"QA Suite deployed but not generating tests from Jira ACs — manual test case authoring still required"},
            {"id":"p5-a5","name":"Automated Full Regression",           "process_time":4, "wait_time":8, "is_value_add":True,
             "usbank_tool":"PractiTest","notes":"3,400 test cases; 18h to run manually; Smart Tester pilot on Transformer only"},
            {"id":"p5-a6","name":"Automated Performance Testing",       "process_time":4, "wait_time":6, "is_value_add":True,
             "usbank_tool":"BrowserStack","notes":"Performance testing monthly only; not integrated in every release cycle"},
            {"id":"p5-a7","name":"Dynamic Security Testing (DAST)",     "process_time":2, "wait_time":4, "is_value_add":False,
             "usbank_tool":"App Vuln. Solution","notes":"DAST run on major releases only; not automated in CloudBees pipeline"},
            {"id":"p5-a8","name":"Manual SIT / UAT / NF Signoff",       "process_time":6, "wait_time":8, "is_value_add":False,
             "usbank_tool":"BrowserStack + PractiTest","notes":"Cross-browser UAT manually scripted; Agilist acceptance + QA signoff required before Release Gate"},
            {"id":"p5-a9","name":"Defect Triage & Management",          "process_time":2, "wait_time":4, "is_value_add":False,
             "usbank_tool":"Jira + USB Docs","notes":"Defect triage manual; USB Docs used to match defects against known patterns — inconsistently"},
        ],
        "bottleneck": True,
        "current_tools": ["PractiTest","BrowserStack","QA Suite (partial)","Smart Tester (pilot)","App Vuln. Solution","Jira"],
        "notes": (
            "Testing is the most tool-dense phase but has the lowest AI utilisation. "
            "Smart Tester only on Transformer; QA Suite not generating tests from Jira ACs. "
            "3,400-case regression suite takes 18h manually. Shared PractiTest environments "
            "create 2-day booking waits. Test data generation has PII risk with manual approach."
        ),
    },
    # ── Phase 6: Continuous Delivery (5 activities) ───────────────────
    {
        "id": 6, "name": "Continuous Delivery",
        "usbank_label": "Release & Deploy",
        "process_time": 16, "wait_time": 112,
        "activities": [
            {"id":"p6-a1","name":"Infrastructure as Code (IaC)",        "process_time":4, "wait_time":8, "is_value_add":True,
             "usbank_tool":"CloudBees + Terraform","notes":"IaC coverage ~65%; legacy on-prem environments still manually provisioned"},
            {"id":"p6-a2","name":"Stage Deployment (SIT/UAT/Staging)",  "process_time":2, "wait_time":8, "is_value_add":True,
             "usbank_tool":"CloudBees Deploy","notes":"Staging deployment automated; SIT environment wait adds 8h before deployment begins"},
            {"id":"p6-a3","name":"Release Gates / Approvals",           "process_time":4, "wait_time":80,"is_value_add":False,
             "usbank_tool":"ServiceNow + App Vuln. Solution","notes":"CAB every Tuesday; 5-business-day advance submission; Risk Manager + Compliance + Eng Lead sign-off — 80h queue"},
            {"id":"p6-a4","name":"Production Deployment",               "process_time":4, "wait_time":12,"is_value_add":True,
             "usbank_tool":"CloudBees Deploy + DEV Bridge","notes":"Production deployment via CloudBees; DEV Bridge provides deployment context; rollback manual"},
            {"id":"p6-a5","name":"Release Notes Generation",            "process_time":2, "wait_time":4, "is_value_add":False,
             "usbank_tool":"DEV Bridge + Confluence","notes":"Release notes drafted manually from Jira change log; DEV Bridge provides context but not auto-generating"},
        ],
        "bottleneck": True,
        "current_tools": ["CloudBees Deploy","ServiceNow","App Vuln. Solution","DEV Bridge","Log Analytics","Terraform"],
        "notes": (
            "Release Gates (p6-a3) is the single largest bottleneck in the entire PDLC — 80h wait time. "
            "CAB every Tuesday, 5-day advance notice, 3-persona sequential sign-off. "
            "No AI risk scoring means every change — regardless of risk — queues for full human review. "
            "Rollback is manual; no Rollback Agent standing by post-deployment."
        ),
    },
    # ── Phase 7: Monitoring & Feedback (4 activities) ─────────────────
    {
        "id": 7, "name": "Monitoring & Feedback",
        "usbank_label": "Operate & Monitor",
        "process_time": 8, "wait_time": 24,
        "activities": [
            {"id":"p7-a1","name":"Application Performance Monitoring (APM)", "process_time":2,"wait_time":4,"is_value_add":True,
             "usbank_tool":"AppDynamics + Log Analytics","notes":"AppDynamics provides strong APM; Log Analytics aggregates across CloudBees + GitLab pipeline events"},
            {"id":"p7-a2","name":"Log Aggregation & Analysis",           "process_time":2, "wait_time":4, "is_value_add":True,
             "usbank_tool":"Splunk","notes":"Splunk SIEM covers all production systems; dashboards in place but alert-to-action routing is manual"},
            {"id":"p7-a3","name":"Incident Management & RCA",            "process_time":3, "wait_time":12,"is_value_add":False,
             "usbank_tool":"Risk Asst. (partial) + USB Docs","notes":"P1 SLA 4h (OCC obligation); MTTR currently 8.4h — 12% of P1s breach SLA. Risk Asst. not integrated into runbook"},
            {"id":"p7-a4","name":"Customer Feedback Loop",               "process_time":1, "wait_time":4, "is_value_add":True,
             "usbank_tool":"USB Docs","notes":"Customer feedback aggregated in USB Docs monthly; not piped back to Jira backlog automatically"},
        ],
        "bottleneck": False,
        "current_tools": ["AppDynamics","Splunk","Log Analytics","USB Docs","Risk Asst. (partial)"],
        "notes": (
            "Monitoring is relatively mature with AppDynamics + Splunk in place. "
            "Key gap: Risk Asst. not integrated into incident runbooks — compliance evidence manual. "
            "P1 MTTR of 8.4h breaches OCC 4h SLA target 12% of the time."
        ),
    },
]

total_pt = sum(p["process_time"] for p in phases_vsm)   # 140 h
total_wt = sum(p["wait_time"]    for p in phases_vsm)   # 484 h
total_lt = total_pt + total_wt                           # 624 h
fe_pct   = round(total_pt / total_lt * 100, 1)          # 22.4%

# ─── 1. VSM SNAPSHOT ──────────────────────────────────────────────────
print("\n▶  Creating VSM snapshot …")

vsm_payload = {
    "source": "sample",
    "vsm_data": {
        "project_id":   PID,
        "project_name": "US Bank — Digital Banking Platform",
        "organization": "US Bank",
        "industry":     "Banking & Financial Services",
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
            "deployment_frequency":    "bi-weekly",
            "lead_time_days":          round(total_lt / 8, 1),
            "change_failure_rate_pct": 14.2,
            "mttr_hours":              8.4,
            "dora_tier":               "Medium (Approaching High)",
        },
        "context": {
            "team_size":             "68 (across 8 squads, 5 products)",
            "methodology":           "SAFe 6.0 — PI Planning every 10 weeks",
            "source_control":        "GitLab Enterprise",
            "cicd_platform":         "CloudBees CI/CD",
            "cloud_platform":        "Azure (primary) + On-prem mainframe (legacy core banking)",
            "alm_tool":              "Jira Software + Confluence",
            "observability":         "AppDynamics APM + Splunk SIEM",
            "compliance_frameworks": "OCC Technology Risk, Dodd-Frank, PCI-DSS v4, SOX, BSA/AML, FFIEC CAT",
            "team_maturity":         "WALK (transitioning to RUN)",
            "deploy_frequency":      "bi-weekly (standard); weekly for hot-fixes on Salesforward",
            "architecture":          "Hybrid — Azure cloud-native (new products) + IBM Mainframe z/OS (core banking)",
            "ai_tools_deployed": [
                "DEV Bridge (all teams)",
                "USB Docs (all teams)",
                "Backlog Asst. (partial — 4/8 squads)",
                "UX Design Coder (pilot — Shop & Apply)",
                "Figma AI (pilot — Shop & Apply)",
                "Code Review Asst. (partial — Honeybee, Rasabee)",
                "QA Suite (partial — Transformer, Toy1)",
                "App Vuln. Solution (all teams via CloudBees)",
                "Log Analytics (all teams via Splunk)",
                "Smart Tester (pilot — Transformer)",
                "Risk Asst. (partial — Compliance only)",
                "GitHub Copilot (pilot — Avengers)",
            ],
            "key_constraints": [
                "OCC examination cycle: technology risk assessment annually",
                "PCI-DSS v4 scope covers all payment product changes",
                "SOX IT General Controls — change management evidence required",
                "Mainframe z/OS integration limits CI/CD velocity for core banking",
                "BSA/AML transaction monitoring changes require independent testing",
                "FFIEC Cybersecurity Assessment: CAT maturity baseline maintained",
            ],
        },
    },
}

# PUT (upsert) the snapshot — creates or replaces
snap = put(f"/vsm/{PID}", vsm_payload)
if not snap:
    snap = post(f"/vsm/{PID}", vsm_payload)
print(f"  VSM snapshot saved  |  FE={fe_pct}%  |  LT={round(total_lt/8,1)} days")

# ─── 2. ANALYSIS RESULT ───────────────────────────────────────────────
print("\n▶  Building analysis result (US Bank specific) …")

analysis_result = {
    "status":     "complete",
    "source":     "seed_usbank_refined",
    "agents_run": [
        "alm_connector","vsm_analyzer","benchmark_agent",
        "bottleneck_analyzer","improvement_generator",
        "future_state_designer","business_case_builder",
    ],

    # ── METRICS ───────────────────────────────────────────────────────
    "metrics": {
        "total_pt":        total_pt,
        "total_wt":        total_wt,
        "total_lt":        total_lt,
        "flow_efficiency": fe_pct,
        "total_lt_days":   round(total_lt / 8, 1),
        "phase_metrics": {
            "1": {"pt":28, "wt":96,  "lt":124, "fe": round(28/124*100,1)},
            "2": {"pt":36, "wt":160, "lt":196, "fe": round(36/196*100,1)},
            "3": {"pt":20, "wt":20,  "lt":40,  "fe": round(20/40*100,1)},
            "4": {"pt":4,  "wt":8,   "lt":12,  "fe": round(4/12*100,1)},
            "5": {"pt":28, "wt":64,  "lt":92,  "fe": round(28/92*100,1)},
            "6": {"pt":16, "wt":112, "lt":128, "fe": round(16/128*100,1)},
            "7": {"pt":8,  "wt":24,  "lt":32,  "fe": round(8/32*100,1)},
        },
        "dora_calibration": {
            "deployment_frequency":    "bi-weekly",
            "lead_time_days":          round(total_lt / 8, 1),
            "change_failure_rate_pct": 14.2,
            "mttr_hours":              8.4,
        },
        "industry_comparison": {
            "flow_efficiency_p50":   27.0,
            "flow_efficiency_p75":   42.0,
            "lead_time_days_p50":    60,
            "usbank_percentile":     "~35th percentile vs top-10 US bank peers",
            "dora_peer_benchmark":   "Medium performer — peer banks at High tier average 42-day LT",
        },
    },

    # ── BOTTLENECKS ── cascading 3-layer model: current → S1 residual → S2 residual → S3 ──
    # Each entry carries addressed_by_stage + per-stage action so the UI can show
    # the full improvement journey per activity.
    "bottlenecks": [
        # ── Phase 1 ───────────────────────────────────────────────────
        {
            "id": "b1-1", "phase_id": 1, "phase_name": "Backlog & Roadmap",
            "activity": "Portfolio Epic / VSM Tracking — Demand Sensing Manual",
            "activity_id": "p1-a1",
            "wait_time": 32, "process_time": 8,
            "severity": "medium", "impact_score": 5.2,
            "waste_type": "Over-Processing / Motion",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "Feature requests scattered across Confluence pages, email, and customer feedback channels — "
                "no automated aggregation. DEV Bridge deployed but only used for deployment context, not "
                "upstream demand sensing. Teams manually scrape requirements into Jira Epics — 8h per epic avg."
            ),
            "current_tools_involved": ["Confluence","Jira","DEV Bridge (partial)"],
            "stage_1_action": "DEV Bridge connects Confluence + feedback channels → auto-structures Jira Epics. Manual epic authoring: 8h → 2h.",
            "stage_2_action": "Discovery Agent continuously monitors all demand signals, auto-creates structured Epics with PCI-DSS/SOX/AML compliance tags.",
            "stage_3_action": "STUMP Platform maintains a live demand registry; Intent engine interprets executive priorities into epic backlog in real time.",
        },
        {
            "id": "b1-2", "phase_id": 1, "phase_name": "Backlog & Roadmap",
            "activity": "Feature Definition & PI Planning Batch Wait",
            "activity_id": "p1-a3",
            "wait_time": 96, "process_time": 6,
            "severity": "medium", "impact_score": 5.9,
            "waste_type": "Waiting / Over-Production",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "SAFe PI Planning every 10 weeks. Features discovered in week 1 may not be formally planned "
                "until week 4–9 — up to 32-day batch delay before dev starts. "
                "Backlog Asst. deployed to 4/8 squads only; PMs still manually write Jira stories from Confluence for 4 squads."
            ),
            "current_tools_involved": ["Jira","Confluence","Backlog Asst. (partial)","USB Docs"],
            "stage_1_action": "Backlog Asst. + USB Docs deployed consistently to all 8 squads. Story creation semi-automated. Backlog wait: 96h → 48h. PI cadence unchanged.",
            "stage_2_action": "Backlog Agent runs continuously — stories refined on demand without waiting for PI cadence. PI Planning compressed to strategic quarterly alignment only.",
            "stage_3_action": "STUMP Platform: human sets quarterly intent; agents decompose, size, and sequence autonomously. PI batch dependency eliminated.",
        },
        {
            "id": "b1-3", "phase_id": 1, "phase_name": "Backlog & Roadmap",
            "activity": "User Story Sizing — Manual Sprint Velocity Assessment",
            "activity_id": "p1-a5",
            "wait_time": 8, "process_time": 2,
            "severity": "low", "impact_score": 3.8,
            "waste_type": "Over-Processing / Defects",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "Story sizing fully manual (planning poker). Velocity data in DEV Bridge unused for AI-assisted sizing. "
                "23% of stories re-sized mid-sprint due to underestimation, disrupting sprint goals. Sprint Agent not deployed."
            ),
            "current_tools_involved": ["Jira","DEV Bridge (partial)"],
            "stage_1_action": "USB Docs surfaces historical delivery patterns from past sprints to inform sizing discussions. Accuracy improved slightly — sizing remains manual.",
            "stage_2_action": "Sprint Agent (DEV Bridge + USB Docs) auto-sizes stories using 18-sprint velocity history. Sizing accuracy: 77% → 90%. Mid-sprint re-sizing: 23% → <5%.",
            "stage_3_action": "STUMP Platform sizes stories automatically as part of backlog generation. Human reviews sizing recommendation before sprint commitment.",
        },
        # ── Phase 2 ───────────────────────────────────────────────────
        {
            "id": "b2-1", "phase_id": 2, "phase_name": "Architecture & UX Design",
            "activity": "EA Board Fortnightly Queue — Solution Architecture",
            "activity_id": "p2-a1",
            "wait_time": 80, "process_time": 10,
            "severity": "critical", "impact_score": 8.9,
            "waste_type": "Waiting / Motion",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "Enterprise Architecture Board meets fortnightly — 14-day minimum queue for any design review. "
                "Every request queues regardless of complexity: a minor API extension waits the same 14 days "
                "as a novel microservice design. No AI pre-screening to identify routine vs novel patterns."
            ),
            "current_tools_involved": ["Confluence","USB Docs (partial)","ShieldDocs"],
            "stage_1_action": "USB Docs provides real-time ADR lookup — architects self-serve standard patterns. EA Board agenda reduced ~25% for clearly standard patterns.",
            "stage_2_action": "Architecture Agent pre-screens all designs against 140+ USB patterns. 85% of standard designs resolved within 24h without EA Board slot. Wait: 80h → 12h for standard designs.",
            "stage_3_action": "Architecture Agent auto-generates design proposals from feature intent grounded in USB Docs. Human reviews proposal; approves before development starts.",
        },
        {
            "id": "b2-2", "phase_id": 2, "phase_name": "Architecture & UX Design",
            "activity": "ShieldDocs Sequential Security Review after EA Board",
            "activity_id": "p2-a4",
            "wait_time": 40, "process_time": 6,
            "severity": "high", "impact_score": 7.1,
            "waste_type": "Waiting / Motion",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "ShieldDocs security review runs sequentially after EA Board review, not in parallel. "
                "Combined wait: 14-day EA Board + 8–14 days ShieldDocs = 22–28 days total design cycle. "
                "No automated security pattern matching against ShieldDocs library."
            ),
            "current_tools_involved": ["ShieldDocs","USB Docs"],
            "stage_1_action": "USB Docs + ShieldDocs integration: architects check security patterns before submission, reducing rework after ShieldDocs review.",
            "stage_2_action": "Design Review Agent runs ShieldDocs validation in parallel with Architecture Agent EA pre-screening. Parallel review: 22–28 days → 3–5 days.",
            "stage_3_action": "STUMP Platform auto-generates security-compliant designs. Compliance Agent validates against ShieldDocs at design generation time — zero sequential wait.",
        },
        {
            "id": "b2-3", "phase_id": 2, "phase_name": "Architecture & UX Design",
            "activity": "UX/UI Design — AI Adoption on 1 of 8 Squads Only",
            "activity_id": "p2-a2",
            "wait_time": 24, "process_time": 12,
            "severity": "medium", "impact_score": 6.4,
            "waste_type": "Motion / Defects",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "UX Design Coder + Figma AI only in pilot on Shop & Apply. 6/8 squads design in Figma manually. "
                "Design-to-handoff cycle: 3–4 days manually vs 0.5 days with AI assistance. "
                "Design inconsistencies (wrong component library, outdated brand tokens) discovered late in code review."
            ),
            "current_tools_involved": ["Figma","UX Design Coder (pilot)","Figma AI (pilot)"],
            "stage_1_action": "UX Design Coder + Figma AI deployed to all 8 squads. Design system validation automated. Wireframe-to-handoff cycle: 3 days → 1 day.",
            "stage_2_action": "UI/UX Agent generates wireframe proposals from feature acceptance criteria. Design Review Agent validates against US Bank design system before developer sees Figma file.",
            "stage_3_action": "STUMP Platform auto-generates high-fidelity designs from feature intent. Human reviews and approves before code scaffolding starts.",
        },
        # ── Phase 3 ───────────────────────────────────────────────────
        {
            "id": "b3-1", "phase_id": 3, "phase_name": "Code Management",
            "activity": "Coding — GitHub Copilot on 1 of 8 Squads Only",
            "activity_id": "p3-a1",
            "wait_time": 4, "process_time": 8,
            "severity": "medium", "impact_score": 6.8,
            "waste_type": "Over-Processing / Under-Utilisation",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "GitHub Copilot pilot on Avengers squad only. 7/8 squads code without AI assistance. "
                "Developers spend 30–40% of coding time writing boilerplate, test stubs, and repetitive patterns. "
                "Code Generator (Figma-to-component) unavailable — all frontend code built from scratch."
            ),
            "current_tools_involved": ["GitLab","VS Code","GitHub Copilot (pilot — Avengers only)"],
            "stage_1_action": "GitHub Copilot expanded to all 8 squads. Boilerplate and test stub generation reduces coding time ~25%. Code Generator still not available.",
            "stage_2_action": "Code Generator (UX Design Coder backbone) scaffolds React components from Figma designs. Developers extend and review, not build from scratch. Coding time: 8h → 4h for standard UI features.",
            "stage_3_action": "STUMP Platform Code Generator produces full feature scaffolding from approved design. Developer reviews business logic and approves merge.",
        },
        {
            "id": "b3-2", "phase_id": 3, "phase_name": "Code Management",
            "activity": "Peer Code Review — 780-line MRs + Cross-Timezone Queue",
            "activity_id": "p3-a4",
            "wait_time": 8, "process_time": 4,
            "severity": "medium", "impact_score": 6.3,
            "waste_type": "Waiting / Defects",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "Salesforward monolith MRs average 780 lines — nearly 2× the 400-line best practice. "
                "2-reviewer policy; UK/US time zone gap creates 12h average MR wait. "
                "Code Review Asst. only on Honeybee/Rasabee — 6 squads receive no AI pre-screening."
            ),
            "current_tools_involved": ["GitLab","Code Review Asst. (partial — 2 squads)"],
            "stage_1_action": "Code Review Asst. deployed to all 8 squads. GitLab MR size limit enforced at 400 lines. Review wait: 12h → 5h.",
            "stage_2_action": "Code Reviewer Agent pre-annotates all MRs with security findings, test gaps, and tech debt. Human reviewer time per MR: 2h → 30 min.",
            "stage_3_action": "Code Reviewer Agent completes full review; human approves or requests specific changes. Same-day review cycle for standard changes.",
        },
        {
            "id": "b3-3", "phase_id": 3, "phase_name": "Code Management",
            "activity": "Unit Test Coverage — 42% vs 70% OCC Target",
            "activity_id": "p3-a2",
            "wait_time": 2, "process_time": 4,
            "severity": "medium", "impact_score": 5.7,
            "waste_type": "Defects / Over-Processing",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "Unit test coverage at 42% vs 70% OCC best-practice target. QA Suite deployed but not used for unit test generation. "
                "Legacy code has sparse coverage. Defects escaping unit testing cost 6× more to fix in UAT."
            ),
            "current_tools_involved": ["GitLab CI","QA Suite (partial)"],
            "stage_1_action": "QA Suite integrated to generate component tests from Jira AC. New feature coverage: 42% → ~60%. Legacy coverage unchanged.",
            "stage_2_action": "Code Generator + QA Orchestrator auto-generate unit tests alongside feature code. 70% coverage enforced as CI gate. Defect escape rate drops 45%.",
            "stage_3_action": "STUMP Platform generates code + tests simultaneously. Coverage 85%+ for all AI-generated code.",
        },
        # ── Phase 4 ───────────────────────────────────────────────────
        {
            "id": "b4-1", "phase_id": 4, "phase_name": "Continuous Integration",
            "activity": "SAST Scan Results — Manual Vulnerability Triage",
            "activity_id": "p4-a2",
            "wait_time": 2, "process_time": 1,
            "severity": "medium", "impact_score": 5.1,
            "waste_type": "Waiting / Over-Processing",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "App Vuln. Solution SAST integrated in CloudBees but results require manual engineer triage. "
                "~40 vulnerability flags per release cycle; engineers spend 3–4h categorising false positives. "
                "No risk-scoring or auto-remediation for low-severity findings."
            ),
            "current_tools_involved": ["App Vuln. Solution","CloudBees CI"],
            "stage_1_action": "App Vuln. Solution configured for auto-prioritisation — critical/high surfaced immediately; low/informational suppressed unless PCI-DSS scope. Triage time: 4h → 1h.",
            "stage_2_action": "Vuln. Fix Agent auto-remediates low-severity vulnerabilities (dependency updates, misconfig). Generates MR for dev review — zero manual triage for standard patterns.",
            "stage_3_action": "Code Generator produces vulnerability-free code by design; Vuln. Fix Agent handles post-commit drift. Near-zero manual triage.",
        },
        {
            "id": "b4-2", "phase_id": 4, "phase_name": "Continuous Integration",
            "activity": "DEV Deployment — No AI-Assisted Post-Deploy Health Check",
            "activity_id": "p4-a4",
            "wait_time": 1, "process_time": 0.5,
            "severity": "low", "impact_score": 3.2,
            "waste_type": "Defects",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "Log Analytics confirms deployment health but alert interpretation is manual. "
                "Engineers must actively check Splunk + AppDynamics after every DEV deployment — no automated go/no-go. "
                "Defective DEV deployments detected 2–4h after the fact."
            ),
            "current_tools_involved": ["CloudBees Deploy","Log Analytics","AppDynamics"],
            "stage_1_action": "Log Analytics connected to CloudBees post-deploy hooks — automated go/no-go for DEV deployments. Detection: 2–4h → <15 min.",
            "stage_2_action": "Pipeline Agent monitors post-deploy health; triggers alert or rollback if anomaly detected within 2 min.",
            "stage_3_action": "Deploy Agent + Rollback Agent operate autonomously. No human intervention for standard DEV deployments.",
        },
        # ── Phase 5 ───────────────────────────────────────────────────
        {
            "id": "b5-1", "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "Test Environment Setup — Shared PractiTest Environments",
            "activity_id": "p5-a1",
            "wait_time": 16, "process_time": 4,
            "severity": "high", "impact_score": 7.2,
            "waste_type": "Waiting",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "5 product teams share 2 PractiTest environments. Confluence calendar booking; avg 2-business-day wait. "
                "Environment conflicts extend test cycles by 3–4 days per sprint. No on-demand provisioning."
            ),
            "current_tools_involved": ["PractiTest (shared)","Confluence (booking calendar)"],
            "stage_1_action": "PractiTest scheduling tool deployed — booking conflicts reduced. Environment wait: 2 days → 1 day. Shared constraint unchanged.",
            "stage_2_action": "QA Orchestrator provisions ephemeral test environments on-demand via CloudBees (containerised). Per-squad isolated environment on MR creation. Wait: 1 day → <2h.",
            "stage_3_action": "STUMP Platform: ephemeral environments auto-provisioned and torn down per feature branch. Zero environment booking wait.",
        },
        {
            "id": "b5-2", "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "Test Data Generation — Manual PII Masking (BSA/AML Risk)",
            "activity_id": "p5-a2",
            "wait_time": 8, "process_time": 4,
            "severity": "high", "impact_score": 7.8,
            "waste_type": "Motion / Defects",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "Test data fully manual — engineers extract production data and mask PII by hand. "
                "BSA/AML test scenarios require realistic transaction patterns that manual masking distorts, reducing test effectiveness. "
                "GDPR/BSA/AML compliance risk from manual PII handling. No synthetic data generation."
            ),
            "current_tools_involved": ["Manual process","USB Docs (partial)"],
            "stage_1_action": "USB Docs provides BSA/AML transaction pattern templates for manual test data construction. Search time reduced — masking still manual.",
            "stage_2_action": "QA Orchestrator generates synthetic PII-safe test data using USB Docs transaction patterns. BSA/AML scenarios auto-generated with realistic synthetic profiles. Manual PII masking eliminated.",
            "stage_3_action": "STUMP Platform: Regression Agent generates scenario-specific synthetic data on demand. PII exposure risk: zero.",
        },
        {
            "id": "b5-3", "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "Automated Full Regression — 3,400 Cases, 18h Manual Run",
            "activity_id": "p5-a5",
            "wait_time": 8, "process_time": 4,
            "severity": "high", "impact_score": 8.1,
            "waste_type": "Waiting / Over-Processing",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "3,400 regression test cases require 18h to run manually. Smart Tester pilot on Transformer only. "
                "Full regression required before every production release — no risk-based subset selection. "
                "Regression duration drives 8h sign-off wait per sprint."
            ),
            "current_tools_involved": ["PractiTest","Smart Tester (pilot)","QA Suite (partial)"],
            "stage_1_action": "Smart Tester + QA Suite deployed to all 8 squads. Parallelised execution: 18h → 8h. Risk-based subsetting available but not fully configured.",
            "stage_2_action": "QA Orchestrator + Regression Agent: change-impact analysis selects targeted subset (critical path 25 min), full suite <90 min in parallel. 18h → <90 min.",
            "stage_3_action": "STUMP Platform: full regression auto-runs on every commit. Change-impact scoping <10 min. Human reviews test summary before deploy.",
        },
        {
            "id": "b5-4", "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "Test Case Authoring — QA Suite Not Generating from Jira AC",
            "activity_id": "p5-a4",
            "wait_time": 8, "process_time": 4,
            "severity": "medium", "impact_score": 6.5,
            "waste_type": "Over-Processing",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "QA Suite deployed but not connected to Jira acceptance criteria for auto-generation. "
                "QA engineers manually author test cases from Jira stories — avg 2h per story. "
                "40% of test cases overlap with existing regression suite (duplicate effort)."
            ),
            "current_tools_involved": ["QA Suite (deployed, not configured)","Jira"],
            "stage_1_action": "QA Suite integrated with Jira — generates test cases from AC. Authoring: 2h/story → 45 min review. Duplicate detection flags overlapping cases.",
            "stage_2_action": "QA Orchestrator generates full test suite from Jira AC automatically. QA engineer reviews and approves — no manual authoring.",
            "stage_3_action": "STUMP Platform: QA Orchestrator generates tests alongside feature code generation. Test cases ready before development starts.",
        },
        {
            "id": "b5-5", "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "DAST + Manual SIT/UAT Signoff — Not in Continuous Pipeline",
            "activity_id": "p5-a7",
            "wait_time": 4, "process_time": 2,
            "severity": "medium", "impact_score": 5.4,
            "waste_type": "Waiting / Over-Processing",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "DAST run on major releases only — not in CloudBees pipeline for every release. "
                "Manual SIT/UAT signoff requires Agilist + QA Lead availability, creating 1–2 day wait after testing completes. "
                "BrowserStack cross-browser tests manually triggered."
            ),
            "current_tools_involved": ["App Vuln. Solution (major releases only)","BrowserStack","PractiTest"],
            "stage_1_action": "App Vuln. Solution DAST integrated into CloudBees pipeline — runs on every release. BrowserStack automation scripts standardised. Manual trigger effort eliminated.",
            "stage_2_action": "UAT Agent coordinates BrowserStack cross-browser automation. DAST results assessed by Vuln. Fix Agent. UAT Agent generates signoff report — human approves, not executes.",
            "stage_3_action": "STUMP Platform: UAT Agent + Compliance Agent handle full signoff documentation. Human approves single summary report.",
        },
        # ── Phase 6 ───────────────────────────────────────────────────
        {
            "id": "b6-1", "phase_id": 6, "phase_name": "Continuous Delivery",
            "activity": "Release Gates / CAB — 5-Day Advance + Sequential 3-Persona Sign-off",
            "activity_id": "p6-a3",
            "wait_time": 80, "process_time": 4,
            "severity": "critical", "impact_score": 9.4,
            "waste_type": "Waiting / Over-Processing",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "ServiceNow CAB requires 5-business-day advance submission. Every production change — regardless of risk — "
                "queues for sequential sign-off by Risk Manager, Compliance Engineer, and Engineering Lead in separate async sessions. "
                "No AI risk scoring: low-risk UI changes wait the same 80h as payment flow changes."
            ),
            "current_tools_involved": ["ServiceNow","App Vuln. Solution","DEV Bridge"],
            "stage_1_action": "App Vuln. Solution scan results auto-attached to ServiceNow CRs — eliminates 2h/release manual evidence preparation. CAB process and schedule unchanged.",
            "stage_2_action": "Release Gate Agent scores every CR on risk scale. Low-risk changes (65% of all) auto-approved as Standard Changes — bypassing CAB queue. Wait: 80h → 12h for standard changes.",
            "stage_3_action": "STUMP Platform: Release Gate Agent + Compliance Agent handle full CR lifecycle. Auto-approval rate: 90%. Human approves High/Regulatory changes only.",
            "competitor_insight": "JPMorgan Chase: 72% of standard changes auto-approved via AI risk scoring. Release cadence improved from bi-weekly to weekly.",
        },
        {
            "id": "b6-2", "phase_id": 6, "phase_name": "Continuous Delivery",
            "activity": "IaC Coverage — 35% Legacy Environments Still Manually Provisioned",
            "activity_id": "p6-a1",
            "wait_time": 8, "process_time": 4,
            "severity": "medium", "impact_score": 5.6,
            "waste_type": "Motion / Over-Processing",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "IaC coverage ~65% — legacy on-prem environments still manually provisioned via ServiceNow runbooks. "
                "Manual provisioning: 4–8h per test/staging environment. Mainframe environments fully manual (z/OS constraint)."
            ),
            "current_tools_involved": ["Terraform","CloudBees CI/CD","ServiceNow"],
            "stage_1_action": "Log Analytics + DEV Bridge extend IaC tooling — additional Terraform templates for remaining Azure environments. IaC coverage: 65% → 85%. Mainframe remains manual.",
            "stage_2_action": "Pipeline Agent manages IaC lifecycle — auto-provisions, updates, and tears down environments. IaC coverage: 85% → 95% (cloud). Mainframe environments remain manual.",
            "stage_3_action": "STUMP Platform: Deploy Agent manages full environment lifecycle. Only mainframe z/OS provisioning remains manual (IBM toolchain constraint).",
        },
        {
            "id": "b6-3", "phase_id": 6, "phase_name": "Continuous Delivery",
            "activity": "Release Notes — Manual Drafting from Jira Change Log",
            "activity_id": "p6-a5",
            "wait_time": 4, "process_time": 2,
            "severity": "low", "impact_score": 3.6,
            "waste_type": "Over-Processing",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "Release notes manually drafted from Jira change log — avg 2h per release cycle for release manager. "
                "DEV Bridge provides context but not auto-generating notes. Quality inconsistent across releases."
            ),
            "current_tools_involved": ["DEV Bridge","Confluence","Jira"],
            "stage_1_action": "DEV Bridge auto-generates release notes from Jira story summaries + commit messages. Release manager reviews and approves. Manual drafting: 2h → 20 min.",
            "stage_2_action": "Deploy Agent generates release notes as part of deployment workflow — includes change summary, risk classification, rollback instructions.",
            "stage_3_action": "STUMP Platform auto-generates release notes, deployment runbook, and compliance evidence as a single package at deploy time.",
        },
        # ── Phase 7 ───────────────────────────────────────────────────
        {
            "id": "b7-1", "phase_id": 7, "phase_name": "Monitoring & Feedback",
            "activity": "Incident Management — MTTR 8.4h Breaches OCC 4h SLA (12% of P1s)",
            "activity_id": "p7-a3",
            "wait_time": 12, "process_time": 3,
            "severity": "high", "impact_score": 8.2,
            "waste_type": "Waiting / Defects",
            "addressed_by_stage": "Stage 2",
            "root_cause": (
                "P1 MTTR 8.4h vs 4h OCC obligation — 12% of P1s breach SLA. Risk Asst. not integrated into runbooks; "
                "on-call engineers manually correlate AppDynamics alerts + Splunk logs to identify root cause. "
                "Alert-to-action routing fully manual — every Splunk alert triaged by on-call engineer."
            ),
            "current_tools_involved": ["AppDynamics","Splunk","Risk Asst. (partial)","USB Docs"],
            "stage_1_action": "Risk Asst. integrated into Splunk runbooks — historical incident context surfaces for on-call. MTTR: 8.4h → 5.2h. Approaching but not meeting 4h SLA.",
            "stage_2_action": "Monitor Agent correlates AppDynamics + Splunk signals automatically. Incident Triage Agent executes runbook steps, generates RCA draft within 30 min of incident start. MTTR: 5.2h → 2.2h. P1 SLA breaches eliminated.",
            "stage_3_action": "STUMP Platform: Monitor Agent detects anomalies pre-emptively before user impact. Incident Triage auto-resolves known scenarios. MTTR: <45 min.",
        },
        {
            "id": "b7-2", "phase_id": 7, "phase_name": "Monitoring & Feedback",
            "activity": "Customer Feedback Loop — Monthly Aggregation, Not Backlog-Connected",
            "activity_id": "p7-a4",
            "wait_time": 4, "process_time": 1,
            "severity": "low", "impact_score": 3.4,
            "waste_type": "Over-Processing / Defects",
            "addressed_by_stage": "Stage 1",
            "root_cause": (
                "Customer feedback aggregated in USB Docs monthly — not real time. Feedback not automatically piped to Jira backlog. "
                "PMs manually review monthly; fast-emerging UX issues sit 4–6 weeks before reaching backlog."
            ),
            "current_tools_involved": ["USB Docs","DEV Bridge (partial)"],
            "stage_1_action": "USB Docs + DEV Bridge configured to auto-tag feedback themes and surface top issues weekly. PM review cycle: monthly → weekly. Jira story creation semi-automated.",
            "stage_2_action": "Discovery Agent continuously monitors USB Docs customer feedback, auto-creates Jira stories for recurring themes. Feedback-to-backlog: 4 weeks → same-day.",
            "stage_3_action": "STUMP Platform: high-priority UX signals automatically prioritised in next sprint scope by Discovery Agent.",
        },
    ],

    # ── IMPROVEMENTS ── 12 entries covering all 7 PDLC phases ────────
    # Each entry shows the tool-level Stage 1 partial fix, the agent-level Stage 2 full fix,
    # and the platform-level Stage 3 autonomous target.
    "improvements": [
        # ── Phase 1 ──────────────────────────────────────────────────
        {
            "phase_id": 1, "phase_name": "Backlog & Roadmap",
            "activity": "Portfolio Demand Sensing & Backlog Automation",
            "addresses_bottlenecks": ["b1-1","b1-2","b1-3"],
            "agent": "Discovery Agent + Backlog Agent + Sprint Agent",
            "tools": ["DEV Bridge","USB Docs","Backlog Asst."],
            "target_system": "Jira + Confluence",
            "source": "catalogue",
            "effort_reduction_pct": 45, "wait_reduction_pct": 55,
            "roi_estimate": "2.4× ROI", "quick_win": True,
            "implementation_weeks": 6, "complexity": "Low",
            "stage_available_from": "Stage 1 (Option A)",
            "how_it_works": (
                "Discovery Agent (DEV Bridge) ingests feature requests from Confluence, Jira, and customer "
                "feedback channels, auto-structures Jira Epics with acceptance criteria. "
                "Backlog Agent (Backlog Asst. + USB Docs) decomposes epics into user stories with "
                "US Bank compliance tags (PCI-DSS scope, SOX impact, AML relevance). "
                "Sprint Agent auto-sizes stories using 18-sprint velocity history from DEV Bridge. "
                "Continuous backlog refinement removes dependency on 10-week PI Planning batch."
            ),
            "stage_1_partial": "Backlog Asst. + USB Docs deployed to all 8 squads. Jira story creation semi-automated. Backlog grooming wait: 96h → 48h. PI cadence unchanged.",
            "stage_2_full": "Discovery + Backlog + Sprint Agents run continuously. PI Planning compressed to strategic quarterly sync only. Story sizing accuracy: 77% → 90%.",
            "stage_3_autonomous": "STUMP Platform: human sets quarterly intent; agents decompose, size, and sequence autonomously. PI batch dependency eliminated.",
        },
        # ── Phase 2 ──────────────────────────────────────────────────
        {
            "phase_id": 2, "phase_name": "Architecture & UX Design",
            "activity": "Architecture Pre-screening & ADR Automation",
            "addresses_bottlenecks": ["b2-1","b2-2"],
            "agent": "Architecture Agent + Design Review Agent",
            "tools": ["USB Docs","ShieldDocs"],
            "target_system": "Confluence + ShieldDocs",
            "source": "catalogue",
            "effort_reduction_pct": 55, "wait_reduction_pct": 78,
            "roi_estimate": "3.1× ROI", "quick_win": False,
            "implementation_weeks": 10, "complexity": "Medium",
            "stage_available_from": "Stage 2 (Option B)",
            "how_it_works": (
                "Architecture Agent pre-screens all design documents against 140+ USB architecture patterns (ADRs, reference designs). "
                "85% of standard designs (API extensions, UI additions, cloud service onboarding) "
                "resolved within 24h without an EA Board slot. "
                "Design Review Agent runs ShieldDocs security validation in parallel — not sequentially after EA. "
                "Combined wait: 22–28 days → 3–5 days for standard designs."
            ),
            "stage_1_partial": "USB Docs real-time ADR lookup deployed — architects self-serve standard patterns. EA Board agenda reduced ~25%. Combined wait: 22–28 days → ~16 days.",
            "stage_2_full": "Architecture Agent + Design Review Agent run in parallel. 85% of designs approved within 24h. EA Board reserved for genuinely novel patterns.",
            "stage_3_autonomous": "STUMP Platform auto-generates architecture proposals from feature intent grounded in USB Docs. Human reviews proposal; approves before development starts.",
            "competitor_insight": "Bank of America: Architecture review cycle 28 → 4 days with AI pre-screening on 85% of standard patterns.",
        },
        {
            "phase_id": 2, "phase_name": "Architecture & UX Design",
            "activity": "UX Design Acceleration — All 8 Squads AI-Assisted",
            "addresses_bottlenecks": ["b2-3"],
            "agent": "UI/UX Agent",
            "tools": ["UX Design Coder","Figma AI"],
            "target_system": "Figma + Confluence",
            "source": "catalogue",
            "effort_reduction_pct": 40, "wait_reduction_pct": 45,
            "roi_estimate": "2.2× ROI", "quick_win": True,
            "implementation_weeks": 4, "complexity": "Low",
            "stage_available_from": "Stage 1 (Option A)",
            "how_it_works": (
                "UX Design Coder + Figma AI deployed to all 8 squads (from Shop & Apply pilot only). "
                "Figma AI validates wireframes against US Bank design system tokens before handoff — "
                "eliminates design inconsistency defects discovered late in code review. "
                "UI/UX Agent (Stage 2) generates wireframe proposals from Jira acceptance criteria."
            ),
            "stage_1_partial": "UX Design Coder + Figma AI all 8 squads. Design system validation automated. Wireframe-to-handoff cycle: 3 days → 1 day.",
            "stage_2_full": "UI/UX Agent generates wireframe proposals from feature AC. Design Review Agent validates against US Bank design system before developer sees Figma file.",
            "stage_3_autonomous": "STUMP Platform auto-generates high-fidelity designs from feature intent. Human reviews and approves before code scaffolding.",
        },
        # ── Phase 3 ──────────────────────────────────────────────────
        {
            "phase_id": 3, "phase_name": "Code Management",
            "activity": "AI-Assisted Coding — GitHub Copilot All Squads + Code Generator",
            "addresses_bottlenecks": ["b3-1","b3-3"],
            "agent": "Code Generator",
            "tools": ["GitHub Copilot","UX Design Coder"],
            "target_system": "GitLab + VS Code",
            "source": "catalogue",
            "effort_reduction_pct": 38, "wait_reduction_pct": 20,
            "roi_estimate": "2.6× ROI", "quick_win": True,
            "implementation_weeks": 3, "complexity": "Low",
            "stage_available_from": "Stage 1 (Option A)",
            "how_it_works": (
                "GitHub Copilot expanded from Avengers pilot to all 8 squads — "
                "boilerplate, test stubs, and repetitive patterns auto-generated. "
                "Code Generator (Stage 2) scaffolds React components directly from Figma designs — "
                "developers extend and review, not build from scratch. "
                "Unit test coverage improves via QA Suite integration with generated code."
            ),
            "stage_1_partial": "GitHub Copilot all 8 squads. Boilerplate/test stub generation reduces coding time ~25%. Code Generator not yet available.",
            "stage_2_full": "Code Generator scaffolds UI components from Figma designs. Coding time for standard features: 8h → 4h. Unit test auto-generation brings coverage from 42% to 70%+.",
            "stage_3_autonomous": "STUMP Platform: Code Generator produces full feature scaffolding from approved design. Developer reviews business logic and approves merge.",
        },
        {
            "phase_id": 3, "phase_name": "Code Management",
            "activity": "Code Review Quality Gate — All Squads + Tech Debt Tracking",
            "addresses_bottlenecks": ["b3-2"],
            "agent": "Code Reviewer + Tech Debt Agent",
            "tools": ["Code Review Asst.","DEV Bridge"],
            "target_system": "GitLab",
            "source": "catalogue",
            "effort_reduction_pct": 50, "wait_reduction_pct": 65,
            "roi_estimate": "2.8× ROI", "quick_win": True,
            "implementation_weeks": 4, "complexity": "Low",
            "stage_available_from": "Stage 1 (Option A)",
            "how_it_works": (
                "Code Review Asst. deployed to all 8 squads (from Honeybee/Rasabee only). "
                "Flags security issues (OWASP Top 10, PCI-DSS card data handling), missing tests, and tech debt. "
                "GitLab MR size limit enforced at 400 lines — Salesforward monolith MRs from 780 → 400 lines avg. "
                "Tech Debt Agent (DEV Bridge) tracks and flags high-debt areas on the Salesforward monolith."
            ),
            "stage_1_partial": "Code Review Asst. all 8 squads. MR size limit enforced. Review wait: 12h → 5h.",
            "stage_2_full": "Code Reviewer Agent pre-annotates all MRs — human reviewer time per MR: 2h → 30 min. Tech Debt Agent tracks and prioritises refactoring opportunities.",
            "stage_3_autonomous": "Code Reviewer Agent completes review; human approves or requests specific changes. Same-day review for standard changes.",
        },
        # ── Phase 4 ──────────────────────────────────────────────────
        {
            "phase_id": 4, "phase_name": "Continuous Integration",
            "activity": "SAST Auto-triage & Vulnerability Auto-remediation",
            "addresses_bottlenecks": ["b4-1","b4-2"],
            "agent": "Vuln. Fix Agent + Pipeline Agent",
            "tools": ["App Vuln. Solution","Log Analytics"],
            "target_system": "CloudBees CI + ServiceNow",
            "source": "catalogue",
            "effort_reduction_pct": 62, "wait_reduction_pct": 58,
            "roi_estimate": "2.9× ROI", "quick_win": True,
            "implementation_weeks": 5, "complexity": "Low",
            "stage_available_from": "Stage 1 (Option A)",
            "how_it_works": (
                "App Vuln. Solution configured for auto-prioritisation: critical/high surfaced immediately; "
                "low/informational suppressed unless PCI-DSS scope. Manual triage: 4h → 1h. "
                "Log Analytics post-deploy hooks provide automated go/no-go for DEV deployments — "
                "defective deployment detection: 2–4h → <15 min. "
                "Vuln. Fix Agent (Stage 2) auto-remediates low-severity findings and generates MR for review."
            ),
            "stage_1_partial": "App Vuln. Solution auto-prioritisation configured. Log Analytics post-deploy go/no-go signals. SAST triage: 4h → 1h. DEV deploy validation: 2–4h → <15 min.",
            "stage_2_full": "Vuln. Fix Agent auto-remediates low/medium severity vulns. Pipeline Agent monitors CI health and triggers alerts on anomaly. Zero manual SAST triage for standard patterns.",
            "stage_3_autonomous": "Code Generator produces vulnerability-free code by design. Pipeline Agent + Vuln. Fix Agent operate autonomously in CI. Near-zero manual intervention.",
        },
        # ── Phase 5 ──────────────────────────────────────────────────
        {
            "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "Test Case Generation & Full Regression Automation",
            "addresses_bottlenecks": ["b5-3","b5-4","b5-5"],
            "agent": "QA Orchestrator + UAT Agent + Regression Agent",
            "tools": ["Smart Tester","QA Suite","USB Docs"],
            "target_system": "PractiTest + BrowserStack + Jira",
            "source": "catalogue",
            "effort_reduction_pct": 72, "wait_reduction_pct": 68,
            "roi_estimate": "4.1× ROI", "quick_win": False,
            "implementation_weeks": 16, "complexity": "Medium",
            "stage_available_from": "Stage 2 (Option B)",
            "how_it_works": (
                "QA Orchestrator (Smart Tester backbone) generates test cases from Jira AC — no manual authoring. "
                "Regression Agent selects change-impact subset: critical path in 25 min, full suite <90 min (vs 18h manual). "
                "UAT Agent coordinates BrowserStack cross-browser runs automatically. "
                "USB Docs provides financial domain knowledge for BSA/AML edge cases and PCI-DSS card data test scenarios. "
                "DAST integrated into CloudBees pipeline — runs on every release, not major releases only."
            ),
            "stage_1_partial": "Smart Tester + QA Suite all 8 squads. QA Suite integrated with Jira AC. Test authoring: 2h/story → 45 min. Regression: 18h → 8h.",
            "stage_2_full": "QA Orchestrator + UAT Agent + Regression Agent. Regression <90 min. UAT automated for 70% of scenarios. DAST every release via pipeline.",
            "stage_3_autonomous": "STUMP Platform auto-generates and runs full test suite from feature intent. Human reviews summary and approves before merge.",
            "competitor_insight": "Wells Fargo: Regression 18h → 90 min using AI test orchestration. Defect escape rate reduced by 38%.",
        },
        {
            "phase_id": 5, "phase_name": "Continuous Testing",
            "activity": "Test Environment & Synthetic Test Data Management",
            "addresses_bottlenecks": ["b5-1","b5-2"],
            "agent": "QA Orchestrator (environment provisioning)",
            "tools": ["PractiTest","USB Docs"],
            "target_system": "CloudBees (containerised ephemeral envs)",
            "source": "catalogue",
            "effort_reduction_pct": 55, "wait_reduction_pct": 80,
            "roi_estimate": "3.2× ROI", "quick_win": False,
            "implementation_weeks": 12, "complexity": "Medium",
            "stage_available_from": "Stage 2 (Option B)",
            "how_it_works": (
                "QA Orchestrator provisions ephemeral containerised test environments on-demand via CloudBees — "
                "each squad gets an isolated environment on MR creation. Shared PractiTest booking queue eliminated. "
                "Synthetic test data generated using USB Docs BSA/AML transaction patterns — "
                "realistic but PII-safe data replaces manual production data masking."
            ),
            "stage_1_partial": "PractiTest scheduling tool deployed. USB Docs templates for manual test data construction. Env wait: 2 days → 1 day. Masking still manual.",
            "stage_2_full": "QA Orchestrator: ephemeral env per MR (<2h), synthetic PII-safe test data from USB Docs patterns. Manual PII masking eliminated. Env wait: 0.",
            "stage_3_autonomous": "STUMP Platform: feature-branch environments auto-provisioned and torn down. Synthetic data generated on-demand. Zero environment wait and zero PII exposure.",
        },
        # ── Phase 6 ──────────────────────────────────────────────────
        {
            "phase_id": 6, "phase_name": "Continuous Delivery",
            "activity": "Release Gate Automation & AI Risk Scoring",
            "addresses_bottlenecks": ["b6-1","b6-3"],
            "agent": "Release Gate Agent + Deploy Agent + Rollback Agent",
            "tools": ["App Vuln. Solution","DEV Bridge","Log Analytics"],
            "target_system": "ServiceNow + CloudBees Deploy",
            "source": "catalogue",
            "effort_reduction_pct": 70, "wait_reduction_pct": 75,
            "roi_estimate": "3.6× ROI", "quick_win": False,
            "implementation_weeks": 14, "complexity": "Medium",
            "stage_available_from": "Stage 2 (Option B)",
            "how_it_works": (
                "Release Gate Agent uses App Vuln. Solution + DEV Bridge context to auto-score every ServiceNow CR "
                "on a risk scale (Low/Medium/High/Regulatory). "
                "Low-risk changes (65% of all changes) auto-approved as Standard Changes — bypassing CAB queue. "
                "Medium/High/Regulatory retain Risk Manager + Compliance review, but Gate Agent pre-populates evidence, "
                "reducing review time from 4h to 30 min. "
                "Deploy Agent orchestrates CloudBees deployment; Rollback Agent stands by post-deploy. "
                "DEV Bridge auto-generates release notes at deploy time."
            ),
            "stage_1_partial": "App Vuln. Solution evidence auto-attached to ServiceNow CRs. DEV Bridge generates draft release notes. Manual CAB process unchanged. Saves ~2h/release.",
            "stage_2_full": "Release Gate Agent auto-approves 65% of standard changes. Deploy Agent orchestrates deployment. Rollback Agent on standby. CAB wait: 80h → 12h for standard changes.",
            "stage_3_autonomous": "STUMP Platform: Release Gate Agent + Compliance Agent handle full CR lifecycle. Auto-approval 90%. Human approves High/Regulatory only.",
            "competitor_insight": "JPMorgan Chase: 72% auto-approved via AI risk scoring. Release cadence: bi-weekly → weekly.",
        },
        {
            "phase_id": 6, "phase_name": "Continuous Delivery",
            "activity": "IaC Coverage Expansion — Azure Environments",
            "addresses_bottlenecks": ["b6-2"],
            "agent": "Pipeline Agent",
            "tools": ["Log Analytics","DEV Bridge"],
            "target_system": "Terraform + CloudBees",
            "source": "catalogue",
            "effort_reduction_pct": 35, "wait_reduction_pct": 50,
            "roi_estimate": "1.9× ROI", "quick_win": True,
            "implementation_weeks": 6, "complexity": "Low",
            "stage_available_from": "Stage 1 (Option A)",
            "how_it_works": (
                "Log Analytics + DEV Bridge extend existing Terraform coverage — "
                "additional environment templates for remaining Azure test/staging environments. "
                "Manual provisioning via ServiceNow runbooks replaced with Terraform apply. "
                "IaC coverage: 65% → 85% in Stage 1. Mainframe z/OS environments remain manual (IBM toolchain constraint). "
                "Pipeline Agent (Stage 2) manages full IaC lifecycle — auto-provisions and tears down environments."
            ),
            "stage_1_partial": "Additional Terraform templates for remaining Azure environments. IaC coverage: 65% → 85%. Manual provisioning: 4–8h → automated for covered envs.",
            "stage_2_full": "Pipeline Agent manages full IaC lifecycle — auto-provision, update, and tear down. IaC coverage: 85% → 95% (cloud). Mainframe remains manual.",
            "stage_3_autonomous": "Deploy Agent manages full cloud environment lifecycle. Only z/OS provisioning remains manual.",
        },
        # ── Phase 7 ──────────────────────────────────────────────────
        {
            "phase_id": 7, "phase_name": "Monitoring & Feedback",
            "activity": "Incident Response Automation & OCC SLA Compliance",
            "addresses_bottlenecks": ["b7-1"],
            "agent": "Monitor Agent + Incident Triage Agent",
            "tools": ["Risk Asst.","Log Analytics","USB Docs"],
            "target_system": "AppDynamics + Splunk + ServiceNow",
            "source": "catalogue",
            "effort_reduction_pct": 68, "wait_reduction_pct": 74,
            "roi_estimate": "3.4× ROI", "quick_win": False,
            "implementation_weeks": 10, "complexity": "Medium",
            "stage_available_from": "Stage 2 (Option B)",
            "how_it_works": (
                "Monitor Agent correlates AppDynamics + Splunk signals in real time — surfacing anomalies "
                "before they become user-impacting incidents. "
                "Incident Triage Agent executes ServiceNow runbook steps automatically, generating RCA draft within 30 min. "
                "Risk Asst. provides compliance context for OCC-reportable incidents. "
                "MTTR: 8.4h → 2.2h in Stage 2 — P1 SLA breaches eliminated. "
                "USB Docs provides historical incident pattern matching for RCA accuracy."
            ),
            "stage_1_partial": "Risk Asst. integrated into Splunk runbooks. Historical incident context surfaces for on-call. MTTR: 8.4h → 5.2h. Approaching but not meeting 4h OCC SLA.",
            "stage_2_full": "Monitor Agent + Incident Triage Agent. Automated runbook execution + RCA draft within 30 min. MTTR: 2.2h. P1 SLA breaches eliminated.",
            "stage_3_autonomous": "STUMP Platform: Monitor Agent detects anomalies pre-emptively. Incident Triage auto-resolves known scenarios. MTTR: <45 min.",
        },
        {
            "phase_id": 7, "phase_name": "Monitoring & Feedback",
            "activity": "Continuous Compliance Evidence Collection (SOX / PCI-DSS)",
            "addresses_bottlenecks": ["b7-2"],
            "agent": "Compliance Agent",
            "tools": ["Risk Asst.","USB Docs","Log Analytics"],
            "target_system": "ServiceNow + Splunk + Jira",
            "source": "catalogue",
            "effort_reduction_pct": 80, "wait_reduction_pct": 60,
            "roi_estimate": "4.8× ROI", "quick_win": False,
            "implementation_weeks": 12, "complexity": "Medium",
            "stage_available_from": "Stage 3 (Option C)",
            "how_it_works": (
                "Compliance Agent continuously collects SOX ITGC change management evidence, "
                "PCI-DSS v4 scan results, and OCC technology risk artefacts from ServiceNow + Splunk + Jira. "
                "Eliminates $2.1M/yr manual audit preparation cost. "
                "Compliance reports auto-generated before each OCC examination cycle. "
                "USB Docs provides regulatory citation library; Risk Asst. flags out-of-compliance signals."
            ),
            "stage_1_partial": "USB Docs surfaces regulatory citation library for manual compliance checks. Customer feedback aggregation weekly via USB Docs + DEV Bridge.",
            "stage_2_full": "Discovery Agent pipes customer feedback to Jira backlog same-day. Risk Asst. integrated into monitoring. Compliance artefacts collected semi-automatically.",
            "stage_3_autonomous": "Compliance Agent collects all SOX/PCI-DSS/OCC evidence continuously. $2.1M/yr audit prep cost eliminated. Human reviews compliance dashboard before examination.",
        },
    ],

    # ── FUTURE STATES ─────────────────────────────────────────────────
    "future_states": [
        {
            "scenario":        "option-a",
            "label":           "Stage 1 — AI-Enabled",
            "subtitle":        "16 AI Tools Embedded · Human-Led · Tools Integrated Across All 7 PDLC Phases",
            "flow_efficiency":  36.2,
            "total_lt_days":   50.0,
            "delta_lt_days":   -28.0,
            "delta_fe_pct":    +13.8,
            "agents_deployed": 0,
            "tools_deployed":  16,
            "human_model":     "Human-Led (AI Assists, Never Decides)",
            "investment_range": "$800K–$1.2M",
            "deployment_cadence": "Bi-weekly (unchanged) → Weekly for low-risk changes",
            "phase_targets": {
                "1": {"fe":32.0, "lt_days":11.2, "key_change":"Backlog Asst. + USB Docs all squads"},
                "2": {"fe":28.0, "lt_days":18.0, "key_change":"UX Design Coder + Figma AI all squads"},
                "3": {"fe":58.0, "lt_days": 7.5, "key_change":"Code Review Asst. all squads + PR size limit"},
                "4": {"fe":38.0, "lt_days": 1.4, "key_change":"App Vuln. Solution auto-triage"},
                "5": {"fe":42.0, "lt_days":12.0, "key_change":"Smart Tester + QA Suite all squads"},
                "6": {"fe":22.0, "lt_days":16.8, "key_change":"App Vuln. Solution evidence auto-attached to CAB"},
                "7": {"fe":28.0, "lt_days": 3.6, "key_change":"Log Analytics + Risk Asst. all squads"},
            },
            # ── User-story level metrics (phases 3-6 only) ──
            "user_story_lt_days":  21.0,
            "user_story_fe":       34.0,
            "user_story_note":     "User story scope: phases 3-6 only. Tools reduce wait in code review + regression but PI/EA batch not in scope.",
            "tool_deployment_map": {
                "Ph1": ["DEV Bridge (all)", "USB Docs (all)", "Backlog Asst. (all)"],
                "Ph2": ["USB Docs (all)", "UX Design Coder (all)", "Figma AI (all)"],
                "Ph3": ["UX Design Coder (all)", "Code Review Asst. (all)", "DEV Bridge (all)"],
                "Ph4": ["QA Suite (all)", "App Vuln. Solution (all)", "Log Analytics (all)"],
                "Ph5": ["Smart Tester (all)", "QA Suite (all)", "USB Docs (all)"],
                "Ph6": ["App Vuln. Solution (all)", "Log Analytics (all)", "DEV Bridge (all)"],
                "Ph7": ["Log Analytics (all)", "USB Docs (all)", "Risk Asst. (all)"],
            },
            "narrative": (
                "Stage 1 (Option A) completes the roll-out of all 16 US Bank AI tools across all 8 squads — "
                "resolving today's inconsistent adoption. Each tool is bolted into the phase where it adds "
                "most value, integrating with existing systems (Jira, GitLab, CloudBees, ServiceNow) via APIs. "
                "Humans remain in full control: AI assists, never decides. "
                "Backlog Asst. + USB Docs deployed consistently to all squads eliminate the 96-hour "
                "feature definition wait. Code Review Asst. deployed across all 8 squads reduces "
                "MR queue from 12 hours to 5 hours. Smart Tester + QA Suite reduce regression from "
                "18 hours to 8 hours. App Vuln. Solution auto-attaches scan evidence to ServiceNow CRs, "
                "saving 2 hours per release cycle. Lead time reduces from 78 to 50 days. "
                "Flow efficiency improves from 22.4% to 36.2%."
            ),
            "key_principles": [
                "Each tool bolts into the phase where it adds most value",
                "Human-Led: every phase driven by a human persona — AI assists, never decides",
                "Tool integration via APIs to Jira, GitLab, Confluence, CloudBees, ServiceNow",
                "Incremental value: each tool reduces manual effort independently",
                "Full tool adoption (no more partial pilots) across all 8 squads",
            ],
            # ── What Stage 1 tools CANNOT fix → justification for Stage 2 ──
            "remaining_bottlenecks": [
                {
                    "phase_id": 1, "phase_name": "Backlog & Roadmap",
                    "residual": "PI Planning batch cadence unchanged",
                    "detail": (
                        "Backlog Asst. + USB Docs are deployed to all squads and story creation is semi-automated, "
                        "but the underlying SAFe PI Planning every 10 weeks is unchanged. Features still queue for the next PI event. "
                        "Continuous backlog refinement without batch dependency requires Sprint Agent + Backlog Agent orchestration — Stage 2."
                    ),
                    "metric_impact": "P1 wait time: 96h → 48h (Stage 1). Target 12h requires Stage 2 Backlog Agent.",
                    "addressed_in": "Stage 2 (Option B)",
                },
                {
                    "phase_id": 2, "phase_name": "Architecture & UX Design",
                    "residual": "EA Board fortnightly schedule unchanged",
                    "detail": (
                        "USB Docs ADR lookup reduces manual effort and EA Board agenda by ~25%, but the EA Board still meets fortnightly. "
                        "Standard designs still wait for the next scheduled meeting. "
                        "Bypassing the queue for 85% of routine patterns requires Architecture Agent (Stage 2) to pre-screen and auto-resolve."
                    ),
                    "metric_impact": "P2 wait time: 120h → 80h (Stage 1). Target 12h for standard designs requires Stage 2 Architecture Agent.",
                    "addressed_in": "Stage 2 (Option B)",
                },
                {
                    "phase_id": 5, "phase_name": "Continuous Testing",
                    "residual": "Shared PractiTest environments — booking queue persists",
                    "detail": (
                        "PractiTest scheduling tool reduces booking conflicts but the underlying shared environment constraint remains. "
                        "On-demand ephemeral environment provisioning per squad per MR requires QA Orchestrator with CloudBees integration — Stage 2."
                    ),
                    "metric_impact": "Env wait: 2 days → 1 day (Stage 1). Target <2h requires Stage 2 QA Orchestrator.",
                    "addressed_in": "Stage 2 (Option B)",
                },
                {
                    "phase_id": 5, "phase_name": "Continuous Testing",
                    "residual": "Test data generation — manual PII masking persists",
                    "detail": (
                        "USB Docs provides BSA/AML transaction templates but actual test data masking and generation remains manual. "
                        "Synthetic PII-safe data generation at scale requires QA Orchestrator intelligence — Stage 2."
                    ),
                    "metric_impact": "BSA/AML test data compliance risk persists through Stage 1.",
                    "addressed_in": "Stage 2 (Option B)",
                },
                {
                    "phase_id": 6, "phase_name": "Continuous Delivery",
                    "residual": "CAB process and schedule unchanged — Release Gate Agent not deployed",
                    "detail": (
                        "App Vuln. Solution auto-attaches scan evidence to ServiceNow CRs (saves ~2h/release), "
                        "but CAB meets weekly on Tuesdays with 5-day advance submission. "
                        "Every change — including low-risk UI updates — still queues for full sequential review. "
                        "AI risk scoring and auto-approval of Standard Changes requires Release Gate Agent — Stage 2."
                    ),
                    "metric_impact": "P6 CAB wait: 80h → 78h (Stage 1 saves evidence prep only). Target 12h requires Stage 2 Release Gate Agent.",
                    "addressed_in": "Stage 2 (Option B)",
                },
                {
                    "phase_id": 7, "phase_name": "Monitoring & Feedback",
                    "residual": "MTTR still above 4h OCC SLA target",
                    "detail": (
                        "Risk Asst. integrated into Splunk runbooks improves incident context for on-call engineers, reducing MTTR 8.4h → 5.2h. "
                        "Meeting the 4h OCC P1 SLA and eliminating SLA breaches requires automated runbook execution via "
                        "Monitor Agent + Incident Triage Agent — Stage 2."
                    ),
                    "metric_impact": "MTTR: 8.4h → 5.2h (Stage 1). Target 2.2h + zero SLA breaches requires Stage 2 Monitor + Triage Agents.",
                    "addressed_in": "Stage 2 (Option B)",
                },
                {
                    "phase_id": 3, "phase_name": "Code Management",
                    "residual": "Code Generator not available — developers still build from scratch",
                    "detail": (
                        "GitHub Copilot all squads reduces boilerplate effort ~25%, but UI components are still manually coded from Figma designs. "
                        "Code Generator (Figma-to-React scaffolding) requires Code Generator Agent integration with UX Design Coder — Stage 2."
                    ),
                    "metric_impact": "Coding effort: ~25% reduction (Stage 1). 50% reduction requires Stage 2 Code Generator.",
                    "addressed_in": "Stage 2 (Option B)",
                },
            ],
        },
        {
            "scenario":        "option-b",
            "label":           "Stage 2 — AI-First",
            "subtitle":        "Tools → Agents · 21 Agents Orchestrated On-Demand · Human: Oversee · Review · Approve",
            "flow_efficiency":  54.8,
            "total_lt_days":   26.5,
            "delta_lt_days":   -51.5,
            "delta_fe_pct":    +32.4,
            "agents_deployed": 21,
            "tools_deployed":  16,
            "human_model":     "Human: Oversee · Review · Approve",
            "investment_range": "$1.8M–$2.8M",
            "deployment_cadence": "Weekly → On-demand for low-risk (4× improvement)",
            # ── User-story level metrics (phases 3-6 only) ──
            "user_story_lt_days":  7.0,
            "user_story_fe":       58.0,
            "user_story_note":     "21 agents compress execution phases dramatically. Code Generator + QA Orchestrator + Release Gate Agent cut phases 3-6 from 34 days to ~7 days.",
            "llm_layer": {
                "primary":   "GitHub Copilot + Azure OpenAI",
                "protocol":  "MCP Layer (Model Context Protocol)",
                "note":      "Cross-agent invocations via MCP; each agent has targeted LLM context",
            },
            "agents_by_phase": {
                "Ph1 (Discovery & Planning)": [
                    {"agent":"Discovery Agent",   "tool":"← DEV Bridge",      "mode":"Assistive","role":"Triggered on-demand: ingests demand signals → structures Jira Epics. Human reviews before backlog entry."},
                    {"agent":"Backlog Agent",      "tool":"← Backlog Asst.",   "mode":"Assistive","role":"On-demand epic decomposition → User Stories with PCI-DSS/SOX/AML compliance tags."},
                    {"agent":"Sprint Agent",       "tool":"← USB Docs",        "mode":"Assistive","role":"Human-triggered story sizing via 18-sprint DEV Bridge velocity history."},
                ],
                "Ph2 (Architecture & Design)": [
                    {"agent":"Architecture Agent", "tool":"← USB Docs",        "mode":"Assistive","role":"On-demand design pre-screening vs 140+ USB patterns. Human reviews EA Board items."},
                    {"agent":"UI/UX Agent",         "tool":"← UX Design Coder","mode":"Assistive","role":"Human-triggered wireframe generation + design system validation."},
                    {"agent":"Design Review Agent", "tool":"← Figma AI",       "mode":"Assistive","role":"Parallel ShieldDocs + EA pattern validation — invoked alongside Architecture Agent."},
                ],
                "Ph3 (Development)": [
                    {"agent":"Code Generator",     "tool":"← UX Design Coder","mode":"Assistive","role":"Developer-triggered Figma → React component scaffolding. Developer extends + approves."},
                    {"agent":"Code Reviewer",      "tool":"← Code Review Asst.","mode":"Assistive","role":"Pre-screens all MRs: security, PCI-DSS, test coverage. Human reviewer acts on flagged items."},
                    {"agent":"Tech Debt Agent",    "tool":"← DEV Bridge",      "mode":"Assistive","role":"On-demand Salesforward monolith tech debt tracking + refactor recommendations."},
                ],
                "Ph4 (Build & CI/CD)": [
                    {"agent":"Build Agent",        "tool":"← QA Suite",        "mode":"Assistive","role":"CloudBees pipeline health monitoring + build optimisation — alerts engineer on anomaly."},
                    {"agent":"Vuln. Fix Agent",    "tool":"← App Vuln. Sol.",  "mode":"Assistive","role":"Generates auto-remediation MRs for low-severity vulns. Human reviews + approves merge."},
                    {"agent":"Pipeline Agent",     "tool":"← Log Analytics",   "mode":"Assistive","role":"Pipeline anomaly detection + alerting — engineer decides on remediation action."},
                ],
                "Ph5 (Test & QA)": [
                    {"agent":"QA Orchestrator",    "tool":"← Smart Tester",    "mode":"Assistive","role":"Generates test cases from Jira AC + provisions ephemeral envs. QA Lead reviews suite."},
                    {"agent":"UAT Agent",           "tool":"← QA Suite",        "mode":"Assistive","role":"BrowserStack cross-browser UAT automation. Human Agilist approves signoff report."},
                    {"agent":"Regression Agent",   "tool":"← USB Docs",        "mode":"Assistive","role":"Change-impact regression scoping + parallel execution. QA Lead reviews pass/fail summary."},
                ],
                "Ph6 (Release & Deploy)": [
                    {"agent":"Release Gate Agent", "tool":"← App Vuln. Sol.",  "mode":"Assistive","role":"ServiceNow CR risk scoring — 65% auto-approved as Standard Changes. Human approves High/Regulatory."},
                    {"agent":"Deploy Agent",       "tool":"← DEV Bridge",      "mode":"Assistive","role":"CloudBees deployment orchestration + post-deploy health check. Engineer oversees."},
                    {"agent":"Rollback Agent",     "tool":"← Log Analytics",   "mode":"Assistive","role":"Automated rollback on error-rate spike — engineer alerted, can override."},
                ],
                "Ph7 (Operate & Monitor)": [
                    {"agent":"Monitor Agent",      "tool":"← Log Analytics",   "mode":"Assistive","role":"AppDynamics + Splunk anomaly correlation — surfaces to on-call engineer for action."},
                    {"agent":"Incident Triage",    "tool":"← USB Docs",        "mode":"Assistive","role":"P1/P2 runbook automation + RCA draft. Engineer reviews RCA and drives resolution."},
                    {"agent":"Compliance Agent",   "tool":"← Risk Asst.",      "mode":"Assistive","role":"SOX/PCI-DSS evidence semi-automated. Compliance team reviews before submission."},
                ],
            },
            "cross_agent_invocations": [
                "USB Docs → Code Generator (architecture context for code scaffolding)",
                "UX Design Coder → Code Reviewer (Figma design ↔ code consistency check)",
                "Code Reviewer → Vuln. Fix Agent (flag vulnerability → trigger auto-fix MR)",
                "Build Agent → QA Orchestrator (build success → trigger test suite)",
                "UAT Agent → Deploy Agent (UAT pass → approve deployment)",
                "Release Gate Agent → Monitor Agent (deploy success → activate monitoring)",
                "Monitor Agent → Incident Triage (anomaly detected → trigger runbook)",
            ],
            "phase_targets": {
                "1": {"fe":48.0, "lt_days": 7.2, "key_change":"Discovery + Backlog + Sprint Agents"},
                "2": {"fe":44.0, "lt_days": 9.0, "key_change":"Architecture + UI/UX + Design Review Agents"},
                "3": {"fe":68.0, "lt_days": 4.4, "key_change":"Code Generator + Code Reviewer + Tech Debt Agent"},
                "4": {"fe":45.0, "lt_days": 1.0, "key_change":"Build + Vuln. Fix + Pipeline Agents"},
                "5": {"fe":58.0, "lt_days": 5.8, "key_change":"QA Orchestrator + UAT + Regression Agents"},
                "6": {"fe":52.0, "lt_days": 7.2, "key_change":"Release Gate Agent (65% auto-approve) + Deploy Agent"},
                "7": {"fe":34.0, "lt_days": 2.2, "key_change":"Monitor + Incident Triage + Compliance Agents"},
            },
            "narrative": (
                "Stage 2 (Option B) transforms US Bank's 16 embedded tools into 21 orchestrated agents — "
                "one per key activity across all 7 PDLC phases. The shift: tools are passive (human triggers); "
                "agents are proactive (they invoke each other, operate in parallel, and hand off autonomously). "
                "GitHub Copilot + Azure OpenAI power the LLM layer; MCP connects agents cross-phase. "
                "Release Gate Agent auto-approves 65% of ServiceNow changes — release cadence improves to weekly. "
                "QA Orchestrator reduces regression from 18 hours to 90 minutes. Architecture Agent resolves "
                "85% of designs within 24 hours without EA Board. Code Generator scaffolds UI components from "
                "Figma — developers review and extend rather than build from scratch. "
                "Lead time reduces from 78 to 26.5 days. Flow efficiency improves from 22.4% to 54.8%."
            ),
            # ── Stage 1 residuals addressed by Stage 2 agents ──────────
            "addressed_from_stage1": [
                {"bottleneck": "PI Planning batch cadence", "agent": "Backlog Agent + Sprint Agent", "outcome": "Continuous backlog refinement — stories ready without waiting for 10-week PI cadence. PI Planning compressed to quarterly strategic sync."},
                {"bottleneck": "EA Board fortnightly queue", "agent": "Architecture Agent + Design Review Agent", "outcome": "85% of standard designs resolved within 24h. EA Board reserved for genuinely novel patterns."},
                {"bottleneck": "Shared PractiTest environments", "agent": "QA Orchestrator", "outcome": "Ephemeral per-squad environments provisioned on MR creation via CloudBees. Env wait: 1 day → <2h."},
                {"bottleneck": "Manual PII masking for test data", "agent": "QA Orchestrator (synthetic data)", "outcome": "BSA/AML-compliant synthetic test data generated from USB Docs patterns. Manual PII masking eliminated."},
                {"bottleneck": "CAB sequential sign-off — 80h wait", "agent": "Release Gate Agent", "outcome": "65% of standard changes auto-approved. CAB reserved for Medium/High/Regulatory. Wait: 80h → 12h."},
                {"bottleneck": "MTTR 5.2h — above 4h OCC SLA", "agent": "Monitor Agent + Incident Triage Agent", "outcome": "Automated runbook execution + RCA draft in 30 min. MTTR: 5.2h → 2.2h. P1 SLA breaches eliminated."},
                {"bottleneck": "Code Generator not available", "agent": "Code Generator", "outcome": "React components scaffolded from Figma designs. Coding time for standard UI features: 8h → 4h."},
            ],
            # ── What Stage 2 agents CANNOT fully fix → justification for Stage 3 ──
            "remaining_bottlenecks": [
                {
                    "phase_id": 6, "phase_name": "Continuous Delivery",
                    "residual": "High-risk payment changes still require human approval",
                    "detail": (
                        "Release Gate Agent auto-approves 65% of standard changes, but OCC Model Risk Guidance (SR 11-7) "
                        "and PCI-DSS v4 Req 6.3.2 mandate human review for AI-assisted decisions in payment-scope changes. "
                        "Risk Manager + Compliance Engineer still review High/Regulatory changes. "
                        "Achieving 90%+ auto-approval requires STUMP Platform compliance engine with full audit trail — Stage 3."
                    ),
                    "metric_impact": "P6 auto-approval: 65% (Stage 2). Target 90%+ requires Stage 3 STUMP Platform + Compliance Agent.",
                    "addressed_in": "Stage 3 (Option C)",
                },
                {
                    "phase_id": 3, "phase_name": "Code Management",
                    "residual": "Mainframe COBOL changes — Code Generator cannot generate z/OS code",
                    "detail": (
                        "Code Generator scaffolds Azure cloud-native (React, Java Spring, Python) components effectively. "
                        "IBM Mainframe z/OS COBOL integration code cannot be auto-generated — "
                        "legacy core banking changes on Salesforward remain fully manual. "
                        "This is a hard toolchain constraint; Stage 3 STUMP Platform mitigates via targeted COBOL review agents "
                        "but cannot fully automate COBOL generation."
                    ),
                    "metric_impact": "Core banking COBOL changes: fully manual in Stage 2 and Stage 3 (hard IBM constraint).",
                    "addressed_in": "Stage 3 (Option C) — partial mitigation only",
                },
                {
                    "phase_id": 1, "phase_name": "Backlog & Roadmap",
                    "residual": "Quarterly executive PI alignment retains some batch element",
                    "detail": (
                        "Backlog Agent enables continuous story-level refinement, but executive PI Planning for strategic prioritisation "
                        "retains a quarterly batch element — senior stakeholders align once per quarter on roadmap sequencing. "
                        "Fully intent-driven continuous planning requires STUMP Platform's intent engine — Stage 3."
                    ),
                    "metric_impact": "P1 strategic batch: monthly in Stage 2 → quarterly touch point in Stage 3.",
                    "addressed_in": "Stage 3 (Option C)",
                },
                {
                    "phase_id": 5, "phase_name": "Continuous Testing",
                    "residual": "BSA/AML + OCC regulatory test scope requires human sign-off",
                    "detail": (
                        "QA Orchestrator automates 70% of UAT scenarios, but BSA/AML transaction monitoring model changes "
                        "and OCC SR 11-7 model risk validation test cases require human QA Lead sign-off. "
                        "This is a regulatory carve-out — not addressable by agents alone."
                    ),
                    "metric_impact": "Regulated test signoffs: manual in Stage 2 and Stage 3 (OCC/BSA/AML hard constraint).",
                    "addressed_in": "Stage 3 (Option C) — Compliance Agent provides audit trail but human sign-off retained",
                },
                {
                    "phase_id": 7, "phase_name": "Monitoring & Feedback",
                    "residual": "Novel P1 incidents beyond agent training data require human RCA",
                    "detail": (
                        "Incident Triage Agent handles known runbook scenarios effectively (MTTR 2.2h). "
                        "Truly novel incidents — new attack vectors, mainframe failures with no historic pattern, "
                        "cascading multi-system failures — still require human RCA investigation. "
                        "Stage 3 STUMP Platform reduces frequency via pre-emptive monitoring but cannot eliminate novel incidents."
                    ),
                    "metric_impact": "Novel P1 RCA: human-led in Stage 2 and Stage 3. MTTR target for novel incidents: <2h in Stage 3.",
                    "addressed_in": "Stage 3 (Option C) — pre-emptive anomaly detection reduces frequency; human RCA retained for novel",
                },
            ],
        },
        {
            "scenario":        "option-c",
            "label":           "Stage 3 — AI-Native | ADLC",
            "subtitle":        "STUMP Agentic Platform · All 21 Agents Orchestrated · Human: Intent · Review · Approve Only",
            "flow_efficiency":  76.4,
            "total_lt_days":   7.8,
            "delta_lt_days":   -70.2,
            "delta_fe_pct":    +54.0,
            "agents_deployed": 21,
            "tools_deployed":  16,
            "human_model":     "Human: Provide Intent · Review Agent Output · Approve Before Merge / Deploy",
            "investment_range": "$3.5M–$5.5M",
            "deployment_cadence": "Continuous (multiple times daily for low-risk) + Weekly for regulated",
            "platform": {
                "name":        "STUMP AGENTIC PLATFORM",
                "description": "Orchestration layer for full ADLC — coordinates all 21 agents end-to-end",
                "components":  ["GitHub Copilot", "Azure OpenAI", "MCP Layer", "LangChain", "Agent Skills"],
                "integration": "All US Bank systems: Jira, Confluence, GitLab, CloudBees, ServiceNow, PractiTest, AppDynamics, Splunk",
            },
            # ── User-story level metrics (phases 3-6 only, ADLC autonomous) ──
            "user_story_lt_days":  0.5,
            "user_story_fe":       82.0,
            "user_story_note":     "ADLC fully autonomous for phases 3-6. Code Generator (~1h) + Build/CI (~0.3h) + AI test suite (~0.5h) + auto-deploy (~0.5h) + single human approve (~0.5h) = ~3-4 hrs total. Sub-day for non-regulated stories.",
            "human_touchpoints": [
                "Provide quarterly product intent and strategic priorities",
                "Review agent-produced design proposals before development starts",
                "Approve before merge / deploy (single sign-off replaces 3-persona gate)",
                "Course-correct agent behaviour via feedback (STUMP learns from corrections)",
            ],
            "adlc_flow": [
                "Human sets Intent → STUMP Platform interprets and structures as epics",
                "Discovery Agent + Backlog Agent decompose into stories (continuous, no PI batch)",
                "Architecture Agent auto-generates design proposals grounded in USB Docs",
                "Human reviews design → approves",
                "Code Generator scaffolds feature code from approved design",
                "Code Reviewer + Vuln. Fix Agent validate before PR",
                "Build Agent + QA Orchestrator run full test suite automatically",
                "Release Gate Agent scores risk → auto-approve or flag for human",
                "Deploy Agent deploys with Rollback Agent on standby",
                "Monitor Agent + Compliance Agent operate continuously post-deploy",
            ],
            "agents_by_phase": {
                "Ph1 (Discovery & Planning)": [
                    {"agent":"Discovery Agent",   "tool":"⚙ DEV Bridge",      "mode":"Autonomous","role":"STUMP continuously interprets strategic intent → auto-creates Jira Epics. No human trigger needed."},
                    {"agent":"Backlog Agent",      "tool":"⚙ USB Docs",        "mode":"Autonomous","role":"Platform-orchestrated epic decomposition → compliance-tagged stories 24/7. No PI batch."},
                    {"agent":"Sprint Agent",       "tool":"⚙ GitHub Copilot",  "mode":"Autonomous","role":"Autonomous story sizing + sprint sequencing. Human provides quarterly intent only."},
                ],
                "Ph2 (Architecture & Design)": [
                    {"agent":"Architecture Agent", "tool":"⚙ USB Docs",        "mode":"Autonomous","role":"Auto-generates architecture proposals from intent. Human reviews proposal + approves."},
                    {"agent":"UI/UX Agent",         "tool":"⚙ UX Design Coder","mode":"Autonomous","role":"Platform auto-generates Figma designs from AC — no designer intervention per feature."},
                    {"agent":"Design Review Agent", "tool":"⚙ Figma AI",       "mode":"Autonomous","role":"Continuously validates design vs design system + ShieldDocs. Zero sequential wait."},
                ],
                "Ph3 (Development)": [
                    {"agent":"Code Generator",     "tool":"⚙ UX Design Coder","mode":"Autonomous","role":"Full feature code scaffolded from approved design autonomously. Developer approves merge."},
                    {"agent":"Code Reviewer",      "tool":"⚙ Code Review Asst.","mode":"Autonomous","role":"Platform auto-reviews all MRs end-to-end. Only genuine issues surfaced to developer."},
                    {"agent":"Tech Debt Agent",    "tool":"⚙ DEV Bridge",      "mode":"Autonomous","role":"Continuous debt tracking + auto-generates refactor MRs. Human approves high-impact ones."},
                ],
                "Ph4 (Build & CI/CD)": [
                    {"agent":"Build Agent",        "tool":"⚙ QA Suite",        "mode":"Autonomous","role":"Fully autonomous CloudBees build orchestration. Auto-resolves known failures without escalation."},
                    {"agent":"Vuln. Fix Agent",    "tool":"⚙ App Vuln. Sol.",  "mode":"Autonomous","role":"All low/medium vulns auto-remediated by platform. Zero manual triage."},
                    {"agent":"Pipeline Agent",     "tool":"⚙ Log Analytics",   "mode":"Autonomous","role":"End-to-end pipeline health managed by platform — no human escalation for known patterns."},
                ],
                "Ph5 (Test & QA)": [
                    {"agent":"QA Orchestrator",    "tool":"⚙ Smart Tester",    "mode":"Autonomous","role":"Full test suite auto-generated + executed from feature intent. Human reviews summary only."},
                    {"agent":"UAT Agent",           "tool":"⚙ QA Suite",        "mode":"Autonomous","role":"BrowserStack UAT fully autonomous. Pre-populated signoff report; human approves in <15 min."},
                    {"agent":"Regression Agent",   "tool":"⚙ USB Docs",        "mode":"Autonomous","role":"Platform runs full regression per commit in <10 min. Human reviews pass/fail summary."},
                ],
                "Ph6 (Release & Deploy)": [
                    {"agent":"Release Gate Agent", "tool":"⚙ App Vuln. Sol.",  "mode":"Autonomous","role":"90%+ of CRs auto-approved by platform. PCI-DSS/OCC-scope flagged for single human sign-off."},
                    {"agent":"Deploy Agent",       "tool":"⚙ DEV Bridge",      "mode":"Autonomous","role":"Continuous autonomous deployment for low-risk. Weekly for regulated. Human approves before merge."},
                    {"agent":"Rollback Agent",     "tool":"⚙ Log Analytics",   "mode":"Autonomous","role":"Instant platform-managed rollback on anomaly. No human required for standard rollbacks."},
                ],
                "Ph7 (Operate & Monitor)": [
                    {"agent":"Monitor Agent",      "tool":"⚙ Log Analytics",   "mode":"Autonomous","role":"Pre-emptive anomaly detection before user impact. Platform self-heals known failure patterns."},
                    {"agent":"Incident Triage",    "tool":"⚙ USB Docs",        "mode":"Autonomous","role":"Autonomous runbook execution. RCA draft in <15 min. Only novel incidents escalated to human."},
                    {"agent":"Compliance Agent",   "tool":"⚙ Risk Asst.",      "mode":"Autonomous","role":"Continuous SOX/PCI-DSS/OCC evidence collection by platform. $2.1M/yr audit prep eliminated."},
                ],
            },
            "phase_targets": {
                "1": {"fe":72.0, "lt_days":1.4, "key_change":"Continuous backlog — no PI batch dependency"},
                "2": {"fe":70.0, "lt_days":1.8, "key_change":"AI-generated design proposals; human approves"},
                "3": {"fe":80.0, "lt_days":1.5, "key_change":"Code Generator from approved design; instant review"},
                "4": {"fe":75.0, "lt_days":0.4, "key_change":"Fully autonomous build + vuln. fix pipeline"},
                "5": {"fe":82.0, "lt_days":1.2, "key_change":"Full AI test suite — human reviews summary"},
                "6": {"fe":88.0, "lt_days":1.2, "key_change":"95% auto-approved; single human sign-off"},
                "7": {"fe":70.0, "lt_days":1.3, "key_change":"Continuous autonomous monitoring + compliance"},
            },
            "regulatory_considerations": [
                "OCC Model Risk Guidance (SR 11-7) requires model validation for AI-generated code decisions",
                "PCI-DSS v4 Req 6.3.2 — AI-generated code in payment scope requires human review",
                "SOX ITGC: change management evidence auto-collected by Compliance Agent",
                "BSA/AML: transaction monitoring changes retain human sign-off (hard constraint)",
                "FFIEC CAT: AI autonomy level documented and assessed in next examination cycle",
            ],
            "narrative": (
                "Stage 3 (Option C) activates the STUMP AGENTIC PLATFORM — the orchestration layer "
                "that coordinates all 21 agents end-to-end across the full ADLC. "
                "GitHub Copilot + Azure OpenAI provide the intelligence layer; "
                "MCP + LangChain + Agent Skills wire the 21 agents together into a unified pipeline. "
                "Human touchpoints reduce to: provide quarterly intent, review agent proposals, "
                "and approve before merge/deploy. The platform does the rest. "
                "Features move from intent to production in 7.8 days (vs 78 days today — 10× improvement). "
                "Compliance Agent continuously collects SOX/PCI-DSS evidence — no manual audit prep. "
                "Monitor Agent + Incident Triage reduce P1 MTTR from 8.4 hours to <45 minutes. "
                "STUMP learns from every human correction — continuously improving agent accuracy. "
                "US Bank becomes the first top-10 US bank operating a fully autonomous ADLC platform."
            ),
            # ── Stage 2 residuals addressed by Stage 3 STUMP Platform ──
            "addressed_from_stage2": [
                {"bottleneck": "High-risk payment changes — 35% still manual CAB", "platform_capability": "Compliance Agent + Release Gate Agent (Stage 3 model)", "outcome": "Full CR lifecycle automated with audit trail. Auto-approval: 65% (S2) → 90%+ (S3). Human approves High/Regulatory changes via single sign-off."},
                {"bottleneck": "Quarterly executive PI alignment batch", "platform_capability": "STUMP Intent Engine", "outcome": "Human sets quarterly strategic intent; agents decompose, size, and sequence continuously. No PI batch dependency."},
                {"bottleneck": "Novel P1 incident detection lag", "platform_capability": "Monitor Agent (pre-emptive)", "outcome": "Pre-emptive anomaly detection before user impact. Novel incident frequency reduced 80% via pattern learning from prior incidents."},
            ],
            # ── Hard regulatory stops — cannot be automated in any stage ──
            "remaining_bottlenecks": [
                {
                    "phase_id": 3, "phase_name": "Code Management",
                    "residual": "IBM Mainframe z/OS COBOL — hard toolchain constraint",
                    "detail": "Code Generator cannot produce or modify COBOL/z/OS code. Core banking changes on the IBM Mainframe remain manually coded and reviewed. This is a permanent hard constraint until mainframe modernisation (outside ADLC scope).",
                    "regulatory_basis": "IBM z/OS toolchain — no LLM-based code generation support",
                    "workaround": "Tech Debt Agent flags mainframe dependencies in Salesforward; modernisation roadmap tracked separately.",
                },
                {
                    "phase_id": 5, "phase_name": "Continuous Testing",
                    "residual": "BSA/AML transaction monitoring model changes — human sign-off required",
                    "detail": "OCC regulatory requirement: changes to BSA/AML transaction monitoring systems require independent human testing and sign-off regardless of AI automation level. Compliance Agent provides audit trail but cannot replace human sign-off.",
                    "regulatory_basis": "OCC BSA/AML programme requirements + FinCEN guidance",
                    "workaround": "Compliance Agent auto-collects test evidence; human QA Lead signs off on pre-populated report (15 min vs 4h manually).",
                },
                {
                    "phase_id": 6, "phase_name": "Continuous Delivery",
                    "residual": "PCI-DSS v4 payment-scope changes — Req 6.3.2 human review",
                    "detail": "PCI-DSS v4 Requirement 6.3.2 mandates that AI-generated code in payment card data scope must be reviewed by a human before deployment. Release Gate Agent flags payment-scope changes; human approves. Cannot be fully automated.",
                    "regulatory_basis": "PCI-DSS v4 Req 6.3.2 (effective 31 March 2025)",
                    "workaround": "Release Gate Agent pre-populates PCI evidence package; human review time: 30 min vs 4h manual.",
                },
                {
                    "phase_id": 6, "phase_name": "Continuous Delivery",
                    "residual": "OCC SR 11-7 Model Risk — AI agent decisions require model validation",
                    "detail": "OCC Model Risk Management Guidance (SR 11-7) requires that AI models making material decisions (code approval, release approval, risk scoring) are inventoried, validated, and monitored. Compliance Agent automates evidence collection but cannot replace model validation governance.",
                    "regulatory_basis": "OCC SR 11-7 Model Risk Management Guidance",
                    "workaround": "Compliance Agent maintains live model inventory; OCC examination artefacts auto-generated. Annual model validation retained.",
                },
            ],
        },
    ],

    # ── BUSINESS CASES ────────────────────────────────────────────────
    "business_cases": [
        {
            "scenario":         "option-a",
            "label":            "Stage 1 — AI-Enabled",
            "investment_range": "$800K–$1.2M",
            "annual_benefits":  "$2.4M",
            "roi_multiple":     2.6,
            "payback_months":   19,
            "npv_3yr":          "$3.8M",
            "irr_pct":          36,
            "executive_summary": (
                "Stage 1 completes consistent roll-out of all 16 US Bank AI tools across all 8 squads, "
                "delivering 2.6× ROI in 24 months. Lead time reduces 36% (78 → 50 days). "
                "No organisational change or new infrastructure required — tools integrate into "
                "existing GitLab, CloudBees, Jira, and ServiceNow ecosystems via APIs. "
                "Lowest risk, fastest to realise benefits. Foundation for Stage 2."
            ),
            "benefit_breakdown": [
                {"category":"Engineering Productivity (Code Review Asst. all squads)", "annual_value":"$680K",  "driver":"Review time 12h→5h × 68 engineers × 26 releases"},
                {"category":"Test Automation (Smart Tester + QA Suite all squads)",    "annual_value":"$720K",  "driver":"Regression 18h→8h; test authoring -50% × 5 QA teams"},
                {"category":"Backlog Acceleration (Backlog Asst. + USB Docs all)",     "annual_value":"$380K",  "driver":"96h→48h wait × PM + Agilist time saved"},
                {"category":"CAB Evidence Automation (App Vuln. Sol.)",                "annual_value":"$280K",  "driver":"2h/release manual evidence prep eliminated × 26 releases"},
                {"category":"Defect Reduction (Code Review Asst.)",                    "annual_value":"$340K",  "driver":"40% fewer defects reaching UAT × avg rework cost $8K/defect"},
            ],
            "cost_breakdown": [
                {"category":"Tool Licences (16 tools, full rollout)",       "cost":"$320K"},
                {"category":"Integration & Configuration",                   "cost":"$240K"},
                {"category":"Training & Enablement (all 8 squads)",         "cost":"$160K"},
                {"category":"Change Management",                             "cost":"$80K"},
                {"category":"Contingency (15%)",                             "cost":"$120K"},
            ],
            "risks": [
                "Inconsistent tool adoption risk mitigated by mandatory squad onboarding",
                "ServiceNow evidence automation requires CAB process owner approval",
                "Tool vendor support SLAs need review for banking-grade uptime requirements",
            ],
            "strategic_alignment": [
                "US Bank 2026 Digital Acceleration Programme — AI toolchain completion",
                "OCC Technology Risk — reduced manual process exposure",
                "FFIEC CAT Domain 3 (Innovative Technology) improvement",
            ],
        },
        {
            "scenario":         "option-b",
            "label":            "Stage 2 — AI-First",
            "investment_range": "$1.8M–$2.8M",
            "annual_benefits":  "$7.2M",
            "roi_multiple":     3.9,
            "payback_months":   13,
            "npv_3yr":          "$14.6M",
            "irr_pct":          68,
            "executive_summary": (
                "Stage 2 transforms 16 tools into 21 orchestrated agents, reducing lead time 66% "
                "(78 → 26.5 days) and achieving weekly deployments. 3.9× ROI with 13-month payback. "
                "Release Gate Agent auto-approves 65% of ServiceNow changes — release frequency doubles. "
                "QA Orchestrator eliminates 72% of manual test effort. "
                "Cross-agent orchestration via MCP enables end-to-end automation while "
                "Risk Managers retain approval authority for high-risk changes."
            ),
            "benefit_breakdown": [
                {"category":"Release Velocity (weekly cadence)",                        "annual_value":"$2.4M","driver":"2× release cycles × avg feature revenue contribution"},
                {"category":"Test Automation (QA Orchestrator — 72% reduction)",        "annual_value":"$1.8M","driver":"72% manual QA effort eliminated; 2 QA squads redeployed to automation"},
                {"category":"Architecture Review Acceleration (85% within 24h)",        "annual_value":"$960K","driver":"Architect + lead engineer time freed from fortnightly ARB queue"},
                {"category":"Release Gate Automation (65% auto-approved)",              "annual_value":"$740K","driver":"Risk Manager + Compliance sign-off effort reduced by 65%"},
                {"category":"Code Quality (Vuln. Fix Agent — auto-remediation)",        "annual_value":"$580K","driver":"Low-severity vulns auto-fixed; security team focus on critical issues"},
                {"category":"Incident Response (Monitor + Triage Agents)",              "annual_value":"$720K","driver":"MTTR 8.4h→2.2h; P1 SLA breaches eliminated (OCC obligation met)"},
            ],
            "cost_breakdown": [
                {"category":"Agent Development (21 agents)",                             "cost":"$620K"},
                {"category":"Azure OpenAI + GitHub Copilot (enterprise tier)",           "cost":"$340K"},
                {"category":"MCP Layer Integration",                                     "cost":"$280K"},
                {"category":"Organisation Design (2 QA squads → AI Ops)",               "cost":"$360K"},
                {"category":"OCC / Compliance Review of AI Agents",                      "cost":"$120K"},
                {"category":"Contingency (15%)",                                         "cost":"$280K"},
            ],
            "risks": [
                "OCC SR 11-7 Model Risk: agents making automated decisions require model validation",
                "2-squad redeployment (QA → AI Ops) needs 6-month reskilling programme",
                "MCP cross-agent dependency: failure of one agent can cascade (circuit-breaker design required)",
                "ServiceNow auto-approval requires Change Management process re-certification",
            ],
            "strategic_alignment": [
                "US Bank AI Strategy 2026 — Agentic AI milestone",
                "OCC Responsible AI Framework — proactive engagement",
                "PCI-DSS v4 compliant: human approval retained for payment-scope changes",
                "US Bank Engineering 2026 Vision — weekly deployment cadence target",
            ],
        },
        {
            "scenario":         "option-c",
            "label":            "Stage 3 — AI-Native / ADLC",
            "investment_range": "$3.5M–$5.5M",
            "annual_benefits":  "$22.4M",
            "roi_multiple":     5.8,
            "payback_months":   24,
            "npv_3yr":          "$46.8M",
            "irr_pct":          94,
            "executive_summary": (
                "Stage 3 activates the STUMP AGENTIC PLATFORM — the first autonomous ADLC in a top-10 US bank. "
                "Lead time reduces 90% (78 → 7.8 days). Continuous deployment for low-risk changes; "
                "weekly for regulated. 5.8× ROI; $46.8M NPV over 3 years. "
                "Human role shifts to intent, review, and approve — platform orchestrates 21 agents end-to-end. "
                "Compliance Agent continuously collects SOX/PCI-DSS evidence, eliminating $2.1M/yr audit prep cost."
            ),
            "benefit_breakdown": [
                {"category":"Continuous deployment velocity",                            "annual_value":"$8.4M","driver":"Near-continuous release × full feature revenue acceleration"},
                {"category":"Engineering headcount optimisation",                        "annual_value":"$5.2M","driver":"18 roles transformed to AI Operations, Platform Engineering, Compliance AI"},
                {"category":"Audit & Compliance automation",                             "annual_value":"$2.1M","driver":"Compliance Agent eliminates manual SOX/PCI-DSS evidence collection"},
                {"category":"Defect & Incident elimination",                             "annual_value":"$3.2M","driver":"AI quality gates; MTTR <45min; P1 incidents -80% (Rollback Agent)"},
                {"category":"Architecture & Design acceleration",                        "annual_value":"$1.8M","driver":"AI-generated design proposals — architects focus on innovation, not review"},
                {"category":"Market differentiation (first ADLC in top-10 US bank)",    "annual_value":"$1.7M","driver":"Faster product launches vs peer banks; talent attraction premium"},
            ],
            "cost_breakdown": [
                {"category":"STUMP Agentic Platform (enterprise licence + customisation)", "cost":"$1.2M"},
                {"category":"Agent Development + Skills (21 agents, Stage 3 capability)", "cost":"$1.0M"},
                {"category":"Azure OpenAI (enterprise) + GitHub Copilot Workspace",       "cost":"$480K"},
                {"category":"MCP + LangChain + Agent Skills integration",                  "cost":"$360K"},
                {"category":"Org Transformation (18 roles)",                               "cost":"$840K"},
                {"category":"OCC Responsible AI — model validation + examination prep",    "cost":"$240K"},
                {"category":"Contingency (15%)",                                           "cost":"$660K"},
            ],
            "risks": [
                "OCC SR 11-7 Model Risk: ADLC agents require comprehensive model inventory and validation",
                "PCI-DSS v4 Req 6.3.2: AI-generated code in payment scope must retain human review — hard constraint",
                "BSA/AML: transaction monitoring changes cannot be autonomous — regulatory carve-out required",
                "18-role transformation is largest engineering org change since US Bank 2019 cloud migration",
                "STUMP Platform single-vendor dependency — contractual SLA and source code escrow required",
                "GitHub Copilot Workspace autonomous mode requires Azure commercial data processing agreement",
            ],
            "strategic_alignment": [
                "US Bank 2030 AI-Native Vision — ADLC as strategic differentiator",
                "OCC Innovation Pilot Charter — proactive engagement as design partner",
                "US Bank Responsible AI Framework — governance model for autonomous agents",
                "US Bank Engineering Vision 2026 — continuous delivery platform",
            ],
        },
    ],

    # ── PLAYBOOK ──────────────────────────────────────────────────────
    "playbook": {
        "organisation":         "US Bank",
        "industry":             "Banking & Financial Services",
        "methodology":          "SAFe 6.0",
        "transformation_path":  "AI-Enabled (Stage 1) → AI-First (Stage 2) → AI-Native/ADLC (Stage 3)",
        "accuracy_pct":         91.4,
        "recommended_sequence": [
            "Month 1–3:  Stage 1 — Deploy all 16 tools consistently across all 8 squads",
            "Month 4–6:  Stage 1 → 2 — Convert top-3 tools (Backlog Asst., Code Review Asst., Smart Tester) to agents",
            "Month 7–12: Stage 2 — Full 21-agent roll-out; MCP layer; weekly cadence",
            "Month 13–18: Stage 2→3 Prep — OCC Model Risk validation; STUMP Platform deployment",
            "Month 19–24: Stage 3 — STUMP ADLC live; Compliance Agent continuous; 7.8-day LT target",
        ],
        "quick_wins_90_days": [
            "Deploy Code Review Asst. to all 8 squads (Doublebee, Triplebee, Avengers, Transformer, Toy1, Toy2) — Week 2",
            "Deploy Smart Tester + QA Suite to all squads — Week 4",
            "Expand UX Design Coder + Figma AI from Shop & Apply to all 8 squads — Week 6",
            "Activate App Vuln. Solution → ServiceNow auto-evidence attachment — Week 8",
            "Expand GitHub Copilot from Avengers pilot to all squads — Week 10",
        ],
        "key_regulatory_milestones": [
            "Submit OCC Responsible AI Framework for agentic toolchain — Month 3",
            "PCI-DSS v4 scope assessment for AI-generated code — Month 6",
            "SOX ITGC change management re-certification for auto-approved changes — Month 9",
            "OCC SR 11-7 Model Validation for Stage 2 agents — Month 12",
            "FFIEC CAT re-assessment incorporating ADLC — Month 18",
        ],
    },
}

# ─── 3. SEED ANALYSIS RUN ─────────────────────────────────────────────
print("\n▶  Seeding analysis run via API …")
run_resp = post(f"/agents/seed-result/{PID}", {
    "agents_run": analysis_result["agents_run"],
    "result":     analysis_result,
})
print(f"  Analysis run created → id={run_resp['id']}")

# ─── VERIFY ───────────────────────────────────────────────────────────
print("\n▶  Verifying …")
result_check = get(f"/agents/result/{PID}")
if result_check:
    m = result_check.get("metrics", {})
    print(f"  FE:           {m.get('flow_efficiency')}%")
    print(f"  LT:           {m.get('total_lt_days')} days")
    print(f"  Bottlenecks:  {len(result_check.get('bottlenecks', []))}")
    print(f"  Improvements: {len(result_check.get('improvements', []))}")
    print(f"  Scenarios:    {[s['scenario'] for s in result_check.get('future_states', [])]}")
    print(f"  Biz Cases:    {len(result_check.get('business_cases', []))}")

# ─── SUMMARY ──────────────────────────────────────────────────────────
print(f"\n{'='*64}")
print("  SEED COMPLETE  —  US Bank Refined")
print(f"{'='*64}")
print(f"""
  Organisation  : US Bank
  Industry      : Banking & Financial Services
  Project ID    : {PID}

  Existing data PRESERVED (untouched):
  ─────────────────────────────────────
  Product Groups: Bankers Experience Evolution, Next Gen Investing
  Products      : Salesforward, Banker Dashboard, Shop & Apply,
                  Money Movement, Document Management
  Teams (8)     : Honeybee, Rasabee, Doublebee, Triplebee,
                  Avengers, Transformer, Toy1, Toys2

  VSM Current State
  ─────────────────
  Lead Time     : {round(total_lt/8,1)} days  (peer banks p50: ~60 days)
  Flow Efficiency: {fe_pct}%  (industry p75: 42%)
  Bottlenecks   : P6 CAB/Release Gates (critical)
                  P2 EA Board + ShieldDocs (critical)
                  P5 Manual UAT/Regression (high)
                  P3 GitLab MR Queue (medium)
                  P1 PI Planning batch wait (medium)
  DORA Tier     : Medium → bi-weekly, CFR 14.2%, MTTR 8.4h

  Stage 1 (Option A)  ←→  AI-Enabled  (16 tools, human-led)
  ───────────────────
  FE: {fe_pct}% → 36.2%  |  LT: {round(total_lt/8,1)}d → 50d  |  ${'{800K–$1.2M}'}  |  2.6× ROI

  Stage 2 (Option B)  ←→  AI-First   (21 agents, human: oversee/approve)
  ───────────────────
  FE: {fe_pct}% → 54.8%  |  LT: {round(total_lt/8,1)}d → 26.5d  |  $1.8M–$2.8M  |  3.9× ROI

  Stage 3 (Option C)  ←→  AI-Native  (STUMP Platform, human: intent only)
  ───────────────────
  FE: {fe_pct}% → 76.4%  |  LT: {round(total_lt/8,1)}d → 7.8d  |  $3.5M–$5.5M  |  5.8× ROI
""")
