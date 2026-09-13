"""
STUMP Platform — Detailed Functional & Technical Specification
Generates: STUMP-Platform-Functional-Tech-Spec.docx
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x00, 0x00, 0x48)
BLUE   = RGBColor(0x2F, 0x78, 0xC4)
TEAL   = RGBColor(0x06, 0xC7, 0xCC)
PURPLE = RGBColor(0x2E, 0x30, 0x8E)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY  = RGBColor(0xF3, 0xF4, 0xF6)
MGRAY  = RGBColor(0x6B, 0x72, 0x80)
DGRAY  = RGBColor(0x1F, 0x29, 0x37)
AMBER  = RGBColor(0xB4, 0x5A, 0x09)
GREEN  = RGBColor(0x05, 0x7A, 0x55)

doc = Document()

# ── Page setup ────────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Inches(8.27)   # A4
section.page_height = Inches(11.69)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)
section.top_margin    = Inches(1.0)
section.bottom_margin = Inches(1.0)

# ── Style helpers ─────────────────────────────────────────────────────────────
def set_cell_bg(cell, rgb: RGBColor):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    hex_color = f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def set_run_color(run, rgb: RGBColor):
    run.font.color.rgb = rgb

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run(text)
    r.font.size  = Pt(20)
    r.font.bold  = True
    r.font.color.rgb = NAVY
    # Bottom border
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'),   'single')
    bottom.set(qn('w:sz'),    '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '00004800'[:6] if False else '2F78C4')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    r.font.size  = Pt(14)
    r.font.bold  = True
    r.font.color.rgb = NAVY
    return p

def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.size  = Pt(12)
    r.font.bold  = True
    r.font.color.rgb = BLUE
    return p

def h4(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.size  = Pt(11)
    r.font.bold  = True
    r.font.color.rgb = PURPLE
    return p

def body(text, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.color.rgb = DGRAY
    return p

def bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.25 + level * 0.25)
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.color.rgb = DGRAY
    return p

def numbered(text, level=0):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.color.rgb = DGRAY
    return p

def callout(text, color=BLUE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.3)
    r = p.add_run(text)
    r.font.size   = Pt(10)
    r.font.italic = True
    r.font.color.rgb = color
    return p

def table_header_row(tbl, cols, bg=NAVY, fg=WHITE):
    row = tbl.rows[0]
    for i, col in enumerate(cols):
        cell = row.cells[i]
        set_cell_bg(cell, bg)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(col)
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = fg

def add_table_row(tbl, values, alt=False, bold_first=False):
    row = tbl.add_row()
    bg = RGBColor(0xF3,0xF4,0xF6) if alt else WHITE
    for i, val in enumerate(values):
        cell = row.cells[i]
        set_cell_bg(cell, bg)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        r = p.add_run(str(val))
        r.font.size = Pt(9)
        r.font.color.rgb = NAVY if (bold_first and i == 0) else DGRAY
        if bold_first and i == 0:
            r.font.bold = True

def make_table(headers, rows, col_widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    if col_widths:
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = Inches(w)
    table_header_row(tbl, headers)
    for ri, row in enumerate(rows):
        add_table_row(tbl, row, alt=(ri % 2 == 1), bold_first=True)
    doc.add_paragraph()
    return tbl

def page_break():
    doc.add_page_break()

def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)

# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(80)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("STUMP")
r.font.size = Pt(48)
r.font.bold = True
r.font.color.rgb = NAVY

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("Strategic Transformation Unified Mapping Platform")
r2.font.size = Pt(18)
r2.font.color.rgb = BLUE

doc.add_paragraph()
p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = p3.add_run("Detailed Functional & Technical Specification")
r3.font.size = Pt(14)
r3.font.bold = True
r3.font.color.rgb = DGRAY

doc.add_paragraph()
p4 = doc.add_paragraph()
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
r4 = p4.add_run(f"Version 1.0  ·  {datetime.date.today().strftime('%B %Y')}  ·  Cognizant")
r4.font.size = Pt(11)
r4.font.color.rgb = MGRAY

doc.add_paragraph()
doc.add_paragraph()
p5 = doc.add_paragraph()
p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
r5 = p5.add_run("CONFIDENTIAL — For Internal Use Only")
r5.font.size = Pt(10)
r5.font.italic = True
r5.font.color.rgb = AMBER

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS (manual)
# ═══════════════════════════════════════════════════════════════════════════════
h1("Table of Contents")
toc_items = [
    ("1", "Executive Summary", ""),
    ("2", "Platform Overview", ""),
    ("  2.1", "Vision & Objectives", ""),
    ("  2.2", "Key Business Benefits", ""),
    ("  2.3", "High-Level Architecture", ""),
    ("3", "Functional Specification", ""),
    ("  3.1", "Module Map & User Journeys", ""),
    ("  3.2", "Dashboard", ""),
    ("  3.3", "ALM Connect & Project Setup", ""),
    ("  3.4", "Current State VSM", ""),
    ("  3.5", "Bottleneck Analysis", ""),
    ("  3.6", "Improvement Recommendations", ""),
    ("  3.7", "Future State Design (Options A/B/C)", ""),
    ("  3.8", "Business Case Builder", ""),
    ("  3.9", "DORA Assessment", ""),
    ("  3.10", "DevOps Maturity Assessment", ""),
    ("  3.11", "Playbook & Context", ""),
    ("  3.12", "AI Assurance & Accuracy Scoring", ""),
    ("  3.13", "Operations Intelligence", ""),
    ("  3.14", "Governance & Transformation Readiness", ""),
    ("  3.15", "Settings & Platform Configuration", ""),
    ("4", "Technical Architecture", ""),
    ("  4.1", "Technology Stack", ""),
    ("  4.2", "System Architecture Diagram", ""),
    ("  4.3", "Backend API Design (FastAPI)", ""),
    ("  4.4", "Frontend Architecture (React/Vite)", ""),
    ("5", "Multi-Agent Architecture", ""),
    ("  5.1", "Agent Orchestration Pipeline", ""),
    ("  5.2", "Shared Agent State", ""),
    ("  5.3", "Agent Specifications (all 8 agents)", ""),
    ("  5.4", "LLM Integration & Graceful Degradation", ""),
    ("6", "Data Architecture", ""),
    ("  6.1", "Database Schema", ""),
    ("  6.2", "Entity Relationship Overview", ""),
    ("  6.3", "Key Data Flows", ""),
    ("7", "Integration Specifications", ""),
    ("  7.1", "ALM Integrations (Jira, ADO, GitHub)", ""),
    ("  7.2", "LLM Integration (Azure OpenAI / OpenAI)", ""),
    ("  7.3", "Scheduler & Pipeline Automation", ""),
    ("8", "PDLC Phases, Activities & Benchmarks", ""),
    ("9", "API Reference", ""),
    ("10", "Security, Configuration & Deployment", ""),
    ("11", "Glossary", ""),
]
for num, title, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(f"{num}  {title}")
    r.font.size = Pt(10)
    r.font.bold  = num.strip() in [str(i) for i in range(1,12)]
    r.font.color.rgb = NAVY if num.strip() in [str(i) for i in range(1,12)] else DGRAY

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
h1("1. Executive Summary")
body(
    "STUMP (Strategic Transformation Unified Mapping Platform) is an AI-powered Value Stream "
    "Management platform designed to accelerate software delivery transformation within large "
    "enterprises. It maps the full Product Development Lifecycle (PDLC) from backlog to production "
    "monitoring, identifies waste and bottlenecks using Lean VSM principles, and prescribes "
    "AI-driven improvement paths from an augmented-human model (Option A) through to a fully "
    "orchestrated agent-first delivery model (Option C)."
)
body(
    "The platform is built on a FastAPI/Python backend with a LangGraph multi-agent orchestration "
    "layer, a React/Vite frontend, and a PostgreSQL persistence store. It connects to real ALM tools "
    "(Jira, Azure DevOps) to ingest live work item data, applies industry benchmarks (DORA elite "
    "profiles, Lean VSM p50/p75 targets), and produces quantified business cases with ROI modelling "
    "for each transformation scenario."
)
make_table(
    ["Dimension", "Detail"],
    [
        ["Platform Name", "STUMP — Strategic Transformation Unified Mapping Platform"],
        ["Version",       "1.0 (Production)"],
        ["Stack",         "React 18 + Vite 5 (frontend)  ·  FastAPI 0.115 + LangGraph (backend)  ·  PostgreSQL 15+"],
        ["Agents",        "8 LangGraph agents in sequential pipeline  +  3 supporting on-demand agents"],
        ["PDLC Phases",   "7 phases  ·  36 activities  ·  Full flow metrics (PT, WT, LT, FE%)"],
        ["Integrations",  "Jira Cloud  ·  Azure DevOps  ·  GitHub  ·  Azure OpenAI  ·  OpenAI  ·  APScheduler"],
        ["Target User",   "Engineering Leads, Transformation Architects, DevOps Coaches, Product Managers"],
        ["Deployment",    "Local dev (Docker-ready)  ·  Cloud-deployable (Azure / AWS)"],
    ],
    col_widths=[1.8, 4.7]
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PLATFORM OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
h1("2. Platform Overview")

h2("2.1  Vision & Objectives")
body(
    "STUMP exists to answer a single question that engineering leaders struggle to quantify: "
    '"Where exactly in our PDLC are we losing time, and what AI agents should we deploy first '
    'to recover it?" It does this by combining three capabilities that are typically siloed:'
)
bullet("Value Stream Mapping — visualising the full flow of work from idea to production with process time, wait time and flow efficiency per phase")
bullet("AI Benchmarking — comparing current performance against DORA elite profiles and Lean VSM industry benchmarks")
bullet("Agent Prescription — recommending a prioritised sequence of AI agent deployments mapped to the identified bottlenecks, with ROI projections")

doc.add_paragraph()
body("The platform's five primary objectives are:")
numbered("Provide a real-time, data-driven view of the current state PDLC using live ALM data (Jira / Azure DevOps)")
numbered("Identify and quantify bottlenecks by phase, activity, severity and business impact")
numbered("Model three transformation scenarios (Option A: AI assistants; Option B: selective agents; Option C: agent-first orchestration)")
numbered("Quantify the ROI of each transformation path with investment breakdown, payback period and annual benefit modelling")
numbered("Track adoption and performance metrics to continuously improve from one option level to the next")

h2("2.2  Key Business Benefits")
make_table(
    ["Benefit", "Description", "Measurable Outcome"],
    [
        ["Faster Delivery",        "AI agents compress process time and eliminate handoff wait in every phase", "40–70% lead time reduction by Option C"],
        ["Flow Efficiency",        "Lean VSM principles applied at activity level to remove non-value-adding wait", "FE% from ~24% (baseline) to 50–65% (Option C)"],
        ["Quantified ROI",         "Business case builder calculates cost vs benefit per agent deployed", "3–6× ROI multiple at Option B–C scale"],
        ["Data-Driven Decisions",  "Decisions backed by live ALM data + DORA benchmarks + industry p50/p75 targets", "Replaces gut-feel with evidence-based transformation planning"],
        ["Reduced Change Risk",    "Transformation roadmap shows incremental steps with checkpoints", "CFR reduced from ~15% to <5% by Option C"],
        ["Rapid Time-to-Value",    "Sample data mode allows demonstration in minutes without ALM connection", "Proof-of-concept ready in 1 day"],
        ["Continuous Improvement", "Scheduled pipeline auto-runs analysis each sprint/week", "Living VSM updated without manual effort"],
        ["AI Adoption Measurement","Tracks utilisation, acceptance, override rates, time saved per agent", "Validates AI investment sprint-by-sprint"],
    ],
    col_widths=[1.6, 3.3, 1.6]
)

h2("2.3  High-Level Architecture")
body("The platform follows a three-tier architecture with a dedicated agent orchestration layer:")

make_table(
    ["Tier", "Technology", "Responsibility"],
    [
        ["Presentation Tier",      "React 18 · Vite 5 · Tailwind CSS · Recharts · Lucide React",   "22-page SPA with interactive VSM visualisations, agent dashboards, scenario comparison"],
        ["API Tier",               "FastAPI 0.115 · Python 3.11 · Pydantic v2 · Uvicorn",            "11 REST routers · async endpoints · CORS · background task execution"],
        ["Agent Tier",             "LangGraph · LangChain · Azure OpenAI / OpenAI",                  "8-node sequential agent pipeline · LLM-enriched analysis · graceful degradation"],
        ["Persistence Tier",       "PostgreSQL 15 · SQLAlchemy 2.0 async · asyncpg",                 "7 tables · UUID PKs · JSON columns for structured data · no ORM migrations needed"],
        ["Scheduler",              "APScheduler (AsyncIOScheduler)",                                  "Automated pipeline runs (daily/weekly) · configurable via UI"],
        ["Integration Layer",      "httpx · REST APIs",                                               "Jira Cloud API · Azure DevOps WIQL · GitHub Issues API"],
    ],
    col_widths=[1.6, 2.5, 2.4]
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 3. FUNCTIONAL SPECIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
h1("3. Functional Specification")

h2("3.1  Module Map & User Journey")
body("The platform consists of 22 UI pages organised into six functional domains:")
make_table(
    ["Domain", "Pages / Modules"],
    [
        ["Project & Data Setup",           "Dashboard  ·  ALM Connect  ·  VSM Editor  ·  DORA Assessment"],
        ["Current State Analysis",         "Current State VSM  ·  Bottleneck Analysis  ·  Operations Intelligence"],
        ["Future State Design",            "Improvements  ·  Future State (Options A/B/C)  ·  Business Case"],
        ["Maturity & Readiness",           "DevOps Maturity  ·  Transformation Readiness  ·  Legacy Modernisation"],
        ["AI Governance & Quality",        "Agents Monitor  ·  AI Assurance  ·  Accuracy Scoring  ·  Playbook & Context"],
        ["Platform Admin",                 "Settings  ·  Governance  ·  Recommendations  ·  Glossary"],
    ],
    col_widths=[2.0, 4.5]
)

body("Typical user journey for a new engagement:")
numbered("Configure project context in Dashboard (organisation, portfolio, team, industry)")
numbered("Connect ALM tool in ALM Connect (Jira / ADO) or use sample data")
numbered("Optionally calibrate with DORA Assessment (measured deployment frequency, lead time)")
numbered("Run the full agent pipeline (triggers all 7 core agents sequentially)")
numbered("Review Current State VSM — identify phases with high wait time and low flow efficiency")
numbered("Drill into Bottleneck Analysis — understand root causes and business impact per activity")
numbered("Review Improvement Recommendations — prioritised AI agent deployment sequence")
numbered("Compare Future State Options A, B, C — choose transformation scenario")
numbered("Review Business Case — validate ROI, investment, payback period")
numbered("Export report / configure scheduled pipeline for continuous monitoring")

h2("3.2  Dashboard")
body("The Dashboard is the landing page and workflow orchestration hub.")
h4("Features")
bullet("Team context form: organisation, portfolio, product group, product, team, industry — persisted to PostgreSQL")
bullet("VSM level selector: Feature / Epic / Story (controls granularity of ALM data mapping)")
bullet("Pipeline run trigger with real-time agent progress tracking (polling /agents/status/{run_id})")
bullet("Agent status cards showing per-agent status (pending / running / complete / failed) with elapsed time")
bullet("Workflow step guide showing the recommended sequence of platform modules")
bullet("Quick-access links to all major analysis pages")

h2("3.3  ALM Connect & Project Setup")
body("Connects the platform to live work item data sources and manages the organisational hierarchy.")
h4("Supported ALM Tools")
make_table(
    ["Tool", "Connection Method", "Data Fetched"],
    [
        ["Jira Cloud",       "Basic Auth (username + API token)",       "Issues via /rest/api/3/search · up to 500 issues · status, cycle time, sprint"],
        ["Azure DevOps",     "PAT (Personal Access Token)",             "Work items via WIQL query · all active items with state transitions"],
        ["GitHub",           "OAuth / PAT",                             "Issues and Projects (basic implementation)"],
        ["CSV Upload",       "File upload",                             "Custom CSV with configurable column mapping"],
        ["Sample Data",      "No credentials needed",                   "Deterministic demo dataset (seed=42) covering all 7 phases"],
    ],
    col_widths=[1.4, 1.8, 3.3]
)
h4("Organisational Hierarchy")
body("STUMP models a full org hierarchy stored in the Project JSON columns:")
bullet("Portfolios — top-level groupings (e.g. Digital Banking, Payments)")
bullet("Product Groups — collections of related products within a portfolio")
bullet("Products — individual products with associated teams")
bullet("Teams — the delivery unit being mapped")
body("All hierarchy data is persisted to PostgreSQL (no localStorage dependency).")

h2("3.4  Current State VSM")
body("Visualises the current-state Value Stream Map with per-phase metrics.")
h4("Features")
bullet("Interactive flow diagram showing all 7 PDLC phases as connected boxes")
bullet("Per-phase metrics displayed inline: Process Time (hours), Wait Time (hours), Lead Time (days), Flow Efficiency %")
bullet("Colour-coded severity overlay (green/amber/red by FE% threshold)")
bullet("Summary bar: Total Lead Time · Total Process Time · Total Wait Time · Overall Flow Efficiency")
bullet("DORA metrics panel: Deployment Frequency, Lead Time for Change, Change Failure Rate, MTTR")
bullet("Manual override capability via VSM Editor (user can adjust PT/WT per phase)")
bullet("Snapshot history — view previous VSM runs to track improvement over time")
h4("Data Sources")
bullet("Primary: ALM connector output (mapped from Jira/ADO work item history)")
bullet("Override: User-specified values via VSM Editor, persisted to VSMSnapshot.overrides")
bullet("Calibration: DORA Assessment measurements (adjust phase 3–6 timing)")

h2("3.5  Bottleneck Analysis")
body("Deep-dive analysis of flow impediments across all 36 PDLC activities.")
h4("Bottleneck Detection Algorithm")
body("Bottlenecks are identified by applying three threshold rules simultaneously:")
make_table(
    ["Rule", "Threshold", "Severity"],
    [
        ["Wait Time Critical",   "Wait Time > 16 hours",    "Critical"],
        ["Wait Time High",       "Wait Time > 8 hours",     "High"],
        ["Effort Critical",      "Process Time > 20 hours", "High"],
        ["Flow Efficiency Low",  "FE% < 15%",               "Critical"],
        ["Flow Efficiency Med",  "FE% < 30%",               "Medium"],
    ],
    col_widths=[2.0, 2.5, 2.0]
)
h4("Bottleneck Card Contents")
bullet("Phase, Activity, Severity badge (Critical/High/Medium/Low)")
bullet("Current Process Time vs benchmark p50")
bullet("Current Wait Time vs benchmark p50")
bullet("Flow Efficiency % with gap to p75 target")
bullet("Root Causes (3–5 bullet points, LLM-enriched if available)")
bullet("Contributing Factors and Waste Type classification")
bullet("Business Impact narrative")
bullet("Linked improvement suggestions (cross-referenced to Improvement Recommendations)")

h2("3.6  Improvement Recommendations")
body("Prescriptive AI agent deployment recommendations mapped to each bottleneck.")
h4("Improvement Catalogue")
body("The platform contains a pre-built catalogue of 36 improvement entries (one per PDLC activity) covering:")
bullet("Recommended AI agent name and type (GenAI Agent / AI Automation)")
bullet("Expected PT reduction % and WT reduction %")
bullet("Implementation effort (Low / Medium / High)")
bullet("Time to value (weeks)")
bullet("ROI estimate (× multiple)")
bullet("Competitor insight (which industry peers have deployed this agent)")
bullet("Priority rating derived from bottleneck severity")
h4("Filtering & Sorting")
bullet("Filter by phase, effort level, ROI range, time to value")
bullet("Sort by priority, ROI, effort, phase order")

h2("3.7  Future State Design — Options A, B, C")
body(
    "Models three transformation scenarios with full metrics projections, agent deployment plans "
    "and narrative explanation. Each scenario is calculated relative to the current-state baseline."
)
make_table(
    ["",                      "Option A — Augmented Human", "Option B — Hybrid Agents",   "Option C — AI-First Orchestration"],
    [
        ["Automation %",          "40%",                          "65%",                        "85%"],
        ["Agent Count",           "16",                           "12",                          "22"],
        ["PT Reduction",          "35%",                          "55%",                         "70%"],
        ["WT Reduction",          "55%",                          "72%",                         "88%"],
        ["Human Roles",           "All roles (AI assists)",        "5 core roles",                "2 roles (Oversee & Approve only)"],
        ["Lead Time Target",      "21–28 days",                    "10–14 days",                  "3–7 days"],
        ["Flow Efficiency",       "38–48%",                        "52–65%",                      "68–80%"],
        ["Deploy Frequency",      "Weekly",                        "Daily",                       "Multiple / day"],
        ["DORA Band",             "Medium → High",                 "High",                        "Elite"],
        ["ROI Multiple",          "1.5–3×",                        "3–4.5×",                      "4.5–6×"],
    ],
    col_widths=[1.6, 1.7, 1.7, 1.5]
)
body("Each scenario page displays: per-phase metric comparison, LLM-generated scenario narrative, agent deployment plan, DORA prediction, and VS-current delta cards.")

h2("3.8  Business Case Builder")
body("Quantifies the financial case for each transformation scenario.")
h4("Investment Components")
bullet("Tools & Licensing (LLM API, agent frameworks, platform subscription)")
bullet("Infrastructure (cloud compute, storage, CI/CD tooling)")
bullet("Implementation (consulting, integration, customisation effort)")
bullet("Training (team upskilling, certification, change management workshops)")
bullet("Change Management (stakeholder comms, adoption programmes)")
h4("Benefit Categories")
bullet("Time-to-Market Improvement — value of faster feature delivery (revenue opportunity)")
bullet("Productivity Gains — engineering hours saved × loaded team rate")
bullet("Quality Improvement — defect reduction, rework avoided, CFR improvement")
bullet("Operational Savings — reduced on-call burden, faster MTTR, infrastructure optimisation")
h4("Output Metrics")
bullet("Total Annual Benefit (£/$)")
bullet("Total Investment (one-time + recurring)")
bullet("ROI Multiple (annual benefit ÷ annualised investment)")
bullet("Payback Period (months)")
bullet("3-Year NPV projection")
body("Also generates organisational change plan: org structure changes, tooling changes, DevSecOps maturity steps, AIops changes, product-centric operating model shifts.")

h2("3.9  DORA Assessment")
body("Captures the four DORA (DevOps Research & Assessment) metrics directly from the team.")
h4("Inputs")
bullet("Deployment Frequency — how often code is deployed to production")
bullet("Lead Time for Change — time from commit to production deployment")
bullet("Change Failure Rate — % of deployments causing incidents")
bullet("Mean Time to Recovery — average time to restore service after failure")
h4("Calibration Output")
body("DORA values are used to calibrate the VSM Analyzer's phase timing estimates. Phase 3–6 lead time is overridden with measured LT values; WT/PT proportions are preserved and adjusted proportionally.")
h4("DORA Band Classification")
make_table(
    ["Band",    "Deploy Freq",        "LT for Change",    "CFR",      "MTTR"],
    [
        ["Elite",   "Multiple/day",       "< 1 hour",         "< 5%",     "< 1 hour"],
        ["High",    "Daily",              "< 1 day",          "< 10%",    "< 1 day"],
        ["Medium",  "Weekly",             "1 day – 1 week",   "16–30%",   "1 day – 1 week"],
        ["Low",     "Monthly or less",    "> 1 month",        "> 30%",    "> 1 week"],
    ],
    col_widths=[1.0, 1.6, 1.6, 1.2, 1.1]
)

h2("3.10  DevOps Maturity Assessment")
body("Structured 73-question assessment covering four engineering practice dimensions.")
h4("Dimensions & Competencies")
make_table(
    ["Dimension", "Sample Competencies", "Questions"],
    [
        ["Dev Practices",          "Source Control, Code Review, TDD, Pair Programming, API Design", "~20"],
        ["DevOps Practices",       "CI/CD, IaC, Container Strategy, Deployment Automation, Monitoring", "~20"],
        ["Security Practices",     "SAST/DAST, Secret Management, Dependency Scanning, AppSec Training", "~18"],
        ["Team Practices",         "Agile Ceremonies, Psychological Safety, DORA Tracking, Retrospectives", "~15"],
    ],
    col_widths=[1.6, 3.5, 1.4]
)
h4("Scoring")
bullet("Each question scored 1–10 across five maturity levels: PRE-CRAWL (1–2), CRAWL (3–4), WALK (5–6), RUN (7–8), FLY (9–10)")
bullet("Auto-scoring available when data sources (GitHub, Jira, SonarQube) are connected")
bullet("Manual override per question with free-text notes")
bullet("AI enrichment generates dimension narrative and improvement priorities if LLM available")
h4("Output")
bullet("Heatmap matrix (dimension × competency) showing current maturity level")
bullet("Overall maturity score per dimension + aggregate")
bullet("Action items auto-generated for competencies scoring below 5 (Walk level)")
bullet("Action items include: title, description, priority, current level, target level, suggested actions, responsible, target date, effort estimate")

h2("3.11  Playbook & Context")
body("Generates a personalised implementation playbook by combining platform analysis with team-specific context documents.")
h4("Context Document Types")
make_table(
    ["Document Type", "Purpose"],
    [
        ["Organisation Chart",         "Maps team structure to identify change impact and sponsorship chain"],
        ["Engineering Standards",      "Informs tool recommendations and integration constraints"],
        ["Tool Inventory",             "Avoids recommending tools already licensed or being phased out"],
        ["Security Policy",            "Applies compliance constraints to agent deployment choices"],
        ["OKRs / Goals",               "Aligns improvement priorities to business objectives"],
        ["DORA Report",                "Enriches calibration beyond the 4-metric form"],
        ["Retrospective Notes",        "Surfaces team-specific friction points not visible in ALM data"],
    ],
    col_widths=[2.0, 4.5]
)
h4("Accuracy Model")
body("Playbook confidence score built from four components:")
bullet("Base analysis quality: up to 30% (from agent pipeline completeness)")
bullet("Form field completeness: up to 60% (team size, roles, tech stack, compliance flags)")
bullet("Document uploads: up to 28% additional (7 document types × 4% each)")
bullet("Maximum: 95% (reserves 5% for unknown context)")

h2("3.12  AI Assurance & Accuracy Scoring")
body("Provides transparency into how confident the platform is in each analysis output.")
h4("Confidence Components per Agent Step")
bullet("Data Quality Score — completeness and recency of ALM data (0–100)")
bullet("KB Retrieval Score — relevance of knowledge base documents retrieved (0–100)")
bullet("LLM Enrichment Bonus — additional confidence when LLM is available and active (+15–20 pts)")
bullet("Coverage Score — % of activities with measured vs estimated data")
h4("Knowledge Base")
body("The platform's internal knowledge base contains ~50+ structured documents covering:")
bullet("DORA benchmark profiles (Elite / High / Medium / Low performer characteristics)")
bullet("Lean VSM targets (p50 process time, p50 wait time, p75 flow efficiency per phase)")
bullet("Transformation patterns (Agile, SAFe, CI/CD maturity, DevSecOps)")
bullet("Technology guides (Git workflows, container practices, IaC, monitoring)")
bullet("Case studies (FAANG deployments, fintech transformation, healthcare compliance)")

h2("3.13  Operations Intelligence")
body("Real-time view of production operations, incident trends and deployment health.")
h4("Features")
bullet("Production deployment frequency trend (daily/weekly/sprint)")
bullet("Incident volume by severity and phase correlation")
bullet("MTTR trend with DORA band overlay")
bullet("Change failure rate trend vs target")
bullet("Alert feed: active incidents, SLA breaches, WIP limit violations")
bullet("On-call burden metrics: pages per engineer per week")

h2("3.14  Governance & Transformation Readiness")
body("Transformation governance and organisational readiness assessment.")
h4("Governance Features")
bullet("Steering committee dashboard — transformation programme status per workstream")
bullet("Gate approval tracking — which milestones have been formally approved")
bullet("Risk register — transformation risks with likelihood, impact, mitigation status")
bullet("Decision log — key architectural and process decisions with rationale")
h4("Readiness Assessment")
bullet("Readiness dimensions: Leadership Sponsorship, Team Skills, Tooling, Process Maturity, Culture")
bullet("Traffic-light scoring per dimension with recommended actions")
bullet("Change impact radar chart showing blast radius of proposed transformation")

h2("3.15  Settings & Platform Configuration")
body("All platform credentials and operational settings are stored in the PlatformSettings database table (not .env files) enabling UI-driven configuration without deployment changes.")
h4("Configuration Categories")
make_table(
    ["Category",        "Settings"],
    [
        ["LLM Config",      "Provider (Azure OpenAI / OpenAI) · API key · Endpoint URL · Deployment name · API version · Test connection button"],
        ["ALM Config",      "Tool (Jira / ADO / GitHub) · URL · Username · API token / PAT · Test connection button"],
        ["Schedule Config", "Enable/disable · Frequency (daily/weekly) · Day of week · Hour (UTC) · Last run status"],
        ["Status",          "LLM availability · ALM connectivity · Last pipeline run · Agent health summary"],
    ],
    col_widths=[1.6, 4.9]
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 4. TECHNICAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
h1("4. Technical Architecture")

h2("4.1  Technology Stack")
make_table(
    ["Layer", "Technology", "Version", "Purpose"],
    [
        ["Frontend Framework",    "React",               "18",       "Component-based SPA"],
        ["Frontend Build",        "Vite",                "5",        "Dev server + bundler"],
        ["Styling",               "Tailwind CSS",        "3",        "Utility-first CSS"],
        ["Charts",                "Recharts",            "Latest",   "VSM flow charts, metrics"],
        ["Icons",                 "Lucide React",        "1.8",      "Consistent icon set"],
        ["HTTP Client",           "Axios",               "Latest",   "API layer (120s timeout)"],
        ["State Management",      "React Context API",   "Built-in", "AppContext + AppProvider"],
        ["Routing",               "React Router",        "v6",       "22-page SPA routing"],
        ["Backend Framework",     "FastAPI",             "0.115",    "Async REST API"],
        ["ASGI Server",           "Uvicorn",             "Latest",   "Production HTTP server"],
        ["ORM",                   "SQLAlchemy",          "2.0",      "Async DB access"],
        ["DB Driver",             "asyncpg",             "0.29+",    "PostgreSQL native async"],
        ["Data Validation",       "Pydantic",            "v2",       "Request/response models"],
        ["Agent Framework",       "LangGraph",           "Latest",   "Multi-agent orchestration"],
        ["LLM Abstraction",       "LangChain",           "Latest",   "OpenAI / Azure OpenAI"],
        ["Scheduler",             "APScheduler",         "3.x",      "Async cron jobs"],
        ["Database",              "PostgreSQL",          "15+",      "Primary persistence store"],
        ["Language",              "Python",              "3.11+",    "Backend + agents"],
    ],
    col_widths=[1.6, 1.5, 0.8, 2.6]
)

h2("4.2  System Architecture Overview")
body("The platform follows a clean separation between presentation, API, agent orchestration, and data layers:")
body("")
callout("Browser → React SPA (port 3001)", BLUE)
callout("    ↓  HTTP REST (Axios, /api/v1/*)", MGRAY)
callout("FastAPI (port 8001)  —  11 routers", BLUE)
callout("    ├─ PostgreSQL  (SQLAlchemy async + asyncpg)", NAVY)
callout("    └─ LangGraph Agent Pipeline", NAVY)
callout("         ├─ ALM Connector  → Jira REST / ADO WIQL / Sample", MGRAY)
callout("         ├─ VSM Analyzer   → metrics computation + DORA calibration", MGRAY)
callout("         ├─ Benchmark Agent → industry p50/p75 comparison", MGRAY)
callout("         ├─ Bottleneck Analyzer → severity scoring + LLM root causes", MGRAY)
callout("         ├─ Improvement Generator → agent prescription catalogue", MGRAY)
callout("         ├─ Future State Designer → Options A/B/C projections", MGRAY)
callout("         └─ Business Case Builder → ROI / investment / org change", MGRAY)
callout("    └─ APScheduler → automated nightly/weekly pipeline runs", NAVY)
body("")

h2("4.3  Backend API Design")
body("All API routes are prefixed with /api/v1. The FastAPI application mounts 11 routers:")
make_table(
    ["Router Module", "URL Prefix", "Key Endpoints"],
    [
        ["health.py",             "/health",             "GET / — system health, agent count, phase count"],
        ["projects.py",           "/projects",           "CRUD: list, create, get/{id}, update/{id}, delete/{id}"],
        ["vsm.py",                "/vsm",                "POST /{project_id}, GET /{project_id}, PUT /{project_id}, GET /{project_id}/metrics"],
        ["agents.py",             "/agents",             "POST /run-analysis/{project_id}, GET /status/{run_id}, GET /result/{project_id}, + 6 individual agent triggers"],
        ["alm.py",                "/alm",                "GET /supported-tools, POST /test-connection, POST /fetch-data, POST /map-to-vsm"],
        ["analysis.py",           "/analysis",           "GET /{id}/bottlenecks, /improvements, /future-state/{scenario}, /business-case/{scenario}, /benchmarks, /export"],
        ["devops_maturity.py",    "/devops-maturity",    "Full assessment CRUD (8 endpoints), action items CRUD (4 endpoints), GET /questions, POST /{id}/run"],
        ["accuracy.py",           "/accuracy",           "GET /demo, GET /{project_id}, GET /kb, POST /kb/search"],
        ["settings_router.py",    "/settings",           "LLM config (3), ALM config (3), Schedule config (3), GET /status"],
    ],
    col_widths=[1.6, 1.4, 3.5]
)

h4("Request / Response Pattern")
bullet("All endpoints use Pydantic v2 models for request validation")
bullet("Responses: 200 (success), 201 (created), 204 (deleted), 404 (not found), 422 (validation error), 500 (server error)")
bullet("Long-running analysis: POST /agents/run-analysis returns {run_id} immediately; client polls GET /agents/status/{run_id}")
bullet("Background tasks: FastAPI BackgroundTasks used for pipeline execution to avoid HTTP timeout")

h2("4.4  Frontend Architecture")
body("The frontend is a single-page application (SPA) built with React 18 and Vite 5.")
h4("State Management")
body("AppContext (React Context API) provides global state to all components:")
bullet("project — current project metadata (id, name, org, team, ALM config)")
bullet("vsmData — latest VSM snapshot data")
bullet("analysisResult — full pipeline output (bottlenecks, improvements, future states, business cases)")
bullet("agentStatus — per-agent run status for live progress tracking")
bullet("doraMetrics / doraProfile — DORA calibration values")
bullet("activeScenario — selected option (option-a / option-b / option-c)")
bullet("customOverrides — user-adjusted PT/WT values from VSM Editor")

h4("Data Persistence Strategy")
bullet("All project data persisted to PostgreSQL via API calls")
bullet("localStorage used ONLY for session hint (last active project ID)")
bullet("No business data stored in localStorage — all reads from PostgreSQL on load")
body("")
h4("Key Component Libraries")
bullet("Recharts — VSM flow charts, bar charts, radar charts, trend lines")
bullet("Lucide React — consistent icon set (LayoutDashboard, BarChart3, Trophy, etc.)")
bullet("Tailwind CSS — utility-first styling with custom navy/teal/usred palette")
body("")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 5. MULTI-AGENT ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
h1("5. Multi-Agent Architecture")

h2("5.1  Agent Orchestration Pipeline")
body(
    "The core agent pipeline uses LangGraph to orchestrate 7 agents in a sequential DAG "
    "(directed acyclic graph). Each agent reads from the shared VSMAgentState TypedDict and "
    "writes its output back to state before passing to the next node."
)
body("Pipeline execution order (no branching — all nodes always execute):")
make_table(
    ["Step", "Agent", "Input From State", "Output to State"],
    [
        ["1", "ALM Connector",           "project, alm_config, overrides",             "alm_raw_data, vsm_data"],
        ["2", "VSM Analyzer",            "vsm_data, dora_calibration",                 "metrics, narrative"],
        ["3", "Benchmark Agent",         "metrics",                                     "benchmarks"],
        ["4", "Bottleneck Analyzer",     "vsm_data, metrics",                          "bottlenecks"],
        ["5", "Improvement Generator",   "bottlenecks",                                "improvements"],
        ["6", "Future State Designer",   "metrics",                                    "future_states"],
        ["7", "Business Case Builder",   "future_states",                              "business_cases"],
    ],
    col_widths=[0.5, 1.8, 2.2, 2.0]
)
body("On-demand agents (not in main graph, called via dedicated endpoints):")
bullet("DevOps Maturity Agent — triggered by POST /devops-maturity/assessments/{id}/run")
bullet("Playbook Contextualizer — triggered by POST /agents/playbook/{project_id}")
bullet("Accuracy Scorer — triggered by GET /accuracy/{project_id}")

h2("5.2  Shared Agent State")
body("All agents communicate via a single shared TypedDict (VSMAgentState) containing:")
make_table(
    ["State Field", "Type", "Description"],
    [
        ["project_id",        "str",      "UUID of the active project"],
        ["project",           "dict",     "{name, organization, portfolio, team, industry}"],
        ["alm_raw_data",      "dict",     "Raw ALM response (issues, work items) as fetched"],
        ["vsm_data",          "dict",     "Mapped VSM data — phases[] each with PT, WT, LT, activities[]"],
        ["overrides",         "dict",     "User-specified PT/WT overrides per phase/activity"],
        ["metrics",           "dict",     "Computed metrics: total LT, FE%, DORA values, per-phase breakdown"],
        ["benchmarks",        "dict",     "Industry benchmark comparison per phase + overall"],
        ["bottlenecks",       "list",     "Bottleneck objects: id, phase, activity, severity, root causes, impact"],
        ["improvements",      "list",     "Improvement objects: id, agent, ROI, effort, PT/WT reduction %"],
        ["future_states",     "dict",     "option-a/b/c: each with projected metrics, narrative, agent plan"],
        ["business_cases",    "dict",     "option-a/b/c: each with investment, benefits, ROI, org changes"],
        ["dora_calibration",  "dict",     "Measured DORA values used to override phase timing estimates"],
        ["errors",            "list",     "Error messages from any agent step (non-fatal)"],
        ["run_id",            "str",      "UUID of the current AnalysisRun record"],
        ["status",            "str",      "pending / running / complete / failed"],
    ],
    col_widths=[1.5, 0.8, 4.2]
)

h2("5.3  Agent Specifications")

h3("Agent 1 — ALM Connector")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",     "Fetch work item data from configured ALM tool and map it to the 7-phase VSM structure"],
        ["Input",       "alm_config {tool, url, username, api_token}, project context, user overrides"],
        ["Output",      "alm_raw_data (normalised), vsm_data {phases[], summary {total_PT, total_WT, total_LT, FE%}}"],
        ["Jira Mode",   "REST API /rest/api/3/search — fetches up to 500 issues; derives PT from time_spent, WT from status transition history"],
        ["ADO Mode",    "WIQL API — queries all active work items; maps State transitions to WT, Completed Work to PT"],
        ["Sample Mode", "Deterministic dataset (seed=42) covering all 36 activities; reproducible for demos"],
        ["Overrides",   "User-specified PT/WT values applied after ALM data mapped — preserved in VSMSnapshot.overrides"],
        ["LLM Used",    "No"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Agent 2 — VSM Analyzer")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",         "Compute flow metrics from mapped VSM data; optionally calibrate with DORA measurements"],
        ["Input",           "vsm_data (phases with PT/WT), dora_calibration (optional)"],
        ["Output",          "metrics {total_PT_hrs, total_WT_hrs, total_LT_days, FE%, deploy_freq, LT_for_change, CFR, MTTR_hrs}"],
        ["Computation",     "FE = PT/(PT+WT)*100 per phase; total LT = sum(PT+WT)/8 hours per day; DORA estimates derived from FE and LT"],
        ["DORA Calibration","If phases3to6_lt_days provided: override phase 3–6 total LT, scale PT/WT proportionally"],
        ["Narrative",       "LLM generates 200-word VSM analysis narrative if available; template used otherwise"],
        ["LLM Used",        "Optional — narrative generation only"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Agent 3 — Benchmark Agent")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",     "Compare current phase metrics against industry benchmark data (p50 process, p50 wait, p75 flow efficiency)"],
        ["Input",       "metrics (per-phase breakdown)"],
        ["Output",      "benchmarks {phases: each with current vs p50 PT, p50 WT, p75 FE and gap; overall: current vs target LT and FE}"],
        ["Data Source", "Hardcoded PDLC_PHASES metadata + INDUSTRY_BENCHMARKS lookup (no external API call)"],
        ["Benchmark Values", "Phase 1: 25h PT / 48h WT / 34% FE  ·  Phase 3: 20h PT / 8h WT / 71% FE  ·  Phase 5: 20h PT / 16h WT / 55% FE"],
        ["LLM Used",    "No"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Agent 4 — Bottleneck Analyzer")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",     "Identify and score flow impediments across all activities; enrich with root causes and business impact"],
        ["Input",       "vsm_data (per-phase activities), metrics"],
        ["Output",      "bottlenecks[] — each with id, phase, activity, severity, wasteType, impact metrics, root causes, contributing factors, business impact, linked improvements"],
        ["Detection",   "Rule-based threshold scoring (WT>16h=Critical, WT>8h=High, PT>20h=High, FE<15%=Critical, FE<30%=Medium)"],
        ["Enrichment",  "12 known activities have pre-computed enrichments (root causes, waste type, business impact text)"],
        ["LLM Enrichment", "If LLM available: prompt generates additional root causes and business impact narrative per bottleneck"],
        ["Fallback",    "33 hardcoded bottleneck records with full metadata used when rule-based thresholds find no data"],
        ["LLM Used",    "Optional — root cause and business impact enrichment"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Agent 5 — Improvement Generator")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",     "Prescribe AI agent deployments mapped to each identified bottleneck"],
        ["Input",       "bottlenecks[]"],
        ["Output",      "improvements[] — each with agent name, type (GenAI Agent / AI Automation), expected PT/WT reduction %, ROI, effort, time-to-value, competitor insight"],
        ["Catalogue",   "Pre-built catalogue of 36 improvements (one per PDLC activity); deterministic mapping from bottleneck activity_id to improvement record"],
        ["Priority",    "Inherited from linked bottleneck severity"],
        ["LLM Used",    "No (catalogue-driven)"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Agent 6 — Future State Designer")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",     "Project current metrics into three future-state scenarios (Options A, B, C) with full per-phase metric modelling"],
        ["Input",       "metrics (current baseline)"],
        ["Output",      "future_states {option-a, option-b, option-c} — each with projected phases[], vs_current deltas, DORA predicted values, narrative, agent deployment plan"],
        ["Scenario A",  "40% automation — 35% PT↓, 55% WT↓, all human roles retained — 16 agents deployed"],
        ["Scenario B",  "65% automation — 55% PT↓, 72% WT↓ — 12 agents, 5 core roles"],
        ["Scenario C",  "85% automation — 70% PT↓, 88% WT↓ — 22 agents, human role = Oversee/Review/Approve only"],
        ["LLM Usage",   "Generates scenario narrative (~300 words) + agent deployment plan per option"],
        ["LLM Used",    "Optional — narrative and agent deployment plan; hardcoded metric projections always run"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Agent 7 — Business Case Builder")
make_table(
    ["Attribute", "Detail"],
    [
        ["Purpose",     "Build quantified financial business case per transformation scenario"],
        ["Input",       "future_states (projected metrics per option)"],
        ["Output",      "business_cases {option-a, option-b, option-c} — each with investment breakdown, annual benefits, ROI multiple, payback months, org/tools/DevSecOps/AIops change plans"],
        ["Option A ROI","1.5–3× multiple, £150–300K investment range, 12–18 month payback"],
        ["Option B ROI","3–4.5× multiple, £350–600K investment range, 8–14 month payback"],
        ["Option C ROI","4.5–6× multiple, £700–1.2M investment range, 14–24 month payback"],
        ["LLM Used",    "No (pre-computed financial models per scenario)"],
    ],
    col_widths=[1.4, 5.1]
)

h2("5.4  LLM Integration & Graceful Degradation")
h4("Supported Providers")
make_table(
    ["Provider",        "Config Keys",                                         "Priority"],
    [
        ["Azure OpenAI", "AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT",       "1st — preferred for enterprise deployments"],
        ["OpenAI",       "OPENAI_API_KEY",                                     "2nd — fallback if Azure not configured"],
        ["None",         "Neither key present",                                "Agents run in rule-based mode (no LLM calls)"],
    ],
    col_widths=[1.4, 3.2, 1.9]
)
h4("LLM Parameters")
bullet("Model: Azure deployment name (configurable) / gpt-4o (OpenAI default)")
bullet("Temperature: 0.2 (low randomness for factual analysis output)")
bullet("Max tokens: 4096")
bullet("Caching: @lru_cache — single LLM instance per process lifecycle")
h4("Graceful Degradation")
body("Every agent that uses LLM wraps the call in try/except:")
bullet("LLM unavailable → pre-built template responses used (narrative, root causes)")
bullet("LLM timeout → same fallback, error logged to state.errors[] (non-fatal)")
bullet("Platform continues to function without LLM — all analysis still runs using catalogue and rule-based logic")
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 6. DATA ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
h1("6. Data Architecture")

h2("6.1  Database Schema")
body("PostgreSQL database (stump_db) managed via SQLAlchemy 2.0 async ORM. Schema auto-created on startup via Base.metadata.create_all(). No migration framework required for initial deployment.")

h3("Table: projects")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",             "VARCHAR (PK)",   "UUID generated by gen_id()"],
        ["name",           "VARCHAR",        "Project display name (required)"],
        ["organization",   "VARCHAR",        "Organisation name"],
        ["portfolio",      "VARCHAR",        "Portfolio name (string, current active)"],
        ["product_group",  "VARCHAR",        "Product group name"],
        ["product",        "VARCHAR",        "Product name"],
        ["team",           "VARCHAR",        "Delivery team name"],
        ["industry",       "VARCHAR",        "Industry sector (Banking, Healthcare, etc.)"],
        ["portfolios",     "JSON",           "Full portfolio hierarchy array [{name, products: [{name, teams:[]}]}]"],
        ["product_groups", "JSON",           "Product group hierarchy array"],
        ["alm_tool",       "VARCHAR",        "jira | ado | github | csv | sample"],
        ["alm_config",     "JSON",           "ALM credentials {url, username, api_token}"],
        ["created_at",     "DATETIME",       "UTC creation timestamp"],
        ["updated_at",     "DATETIME",       "UTC last-modified timestamp (auto-updated)"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h3("Table: vsm_snapshots")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",          "VARCHAR (PK)", "UUID"],
        ["project_id",  "VARCHAR (FK)", "→ projects.id (cascade delete)"],
        ["source",      "VARCHAR",      "alm | manual | sample — data origin"],
        ["raw_data",    "JSON",         "Raw ALM response as fetched (issues array)"],
        ["vsm_data",    "JSON",         "Mapped VSM structure {phases[], summary{}}"],
        ["summary",     "JSON",         "Aggregated metrics {total_PT, total_WT, total_LT, FE%}"],
        ["overrides",   "JSON",         "User-specified PT/WT overrides applied to this snapshot"],
        ["created_at",  "DATETIME",     "Snapshot creation timestamp"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h3("Table: analysis_runs")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",           "VARCHAR (PK)", "UUID"],
        ["project_id",   "VARCHAR (FK)", "→ projects.id (cascade delete)"],
        ["status",       "VARCHAR",      "pending | running | complete | failed"],
        ["agents_run",   "JSON",         "List of agent names that were executed"],
        ["result",       "JSON",         "Full pipeline output (bottlenecks, improvements, future_states, business_cases)"],
        ["error",        "TEXT",         "Error message if status=failed"],
        ["created_at",   "DATETIME",     "Pipeline start timestamp"],
        ["completed_at", "DATETIME",     "Pipeline completion timestamp (null if running)"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h3("Table: platform_settings")
make_table(
    ["Column", "Type", "Description"],
    [
        ["key",        "VARCHAR (PK)", "Setting key (e.g. llm_api_key, alm_jira_url, schedule_enabled)"],
        ["value",      "TEXT",         "Setting value (string, JSON string, or boolean string)"],
        ["updated_at", "DATETIME",     "Last modification timestamp"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)
body("Key names stored in platform_settings:")
bullet("llm_provider, llm_api_key, llm_endpoint, llm_deployment, llm_api_version, llm_model")
bullet("alm_tool, alm_url, alm_username, alm_api_token")
bullet("schedule_enabled, schedule_frequency, schedule_day_of_week, schedule_hour, schedule_last_run_at, schedule_last_run_status")

h3("Table: devops_assessments")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",            "VARCHAR (PK)",  "UUID"],
        ["project_id",    "VARCHAR",       "Optional link to projects table"],
        ["organization",  "VARCHAR",       "Organisation being assessed"],
        ["team_name",     "VARCHAR",       "Team name"],
        ["industry",      "VARCHAR",       "Industry sector"],
        ["sources",       "JSON",          "Connected data sources [{type, url, label, token}]"],
        ["status",        "VARCHAR",       "pending | running | complete | failed"],
        ["responses",     "JSON",          "Per-question responses {question_id: {manual_score, notes}}"],
        ["result",        "JSON",          "Full assessment result (dimension scores, maturity levels, insights)"],
        ["created_at",    "DATETIME",      "Creation timestamp"],
        ["updated_at",    "DATETIME",      "Last update timestamp"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h3("Table: assessment_action_items")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",                "VARCHAR (PK)", "UUID"],
        ["assessment_id",     "VARCHAR (FK)", "→ devops_assessments.id (cascade delete)"],
        ["dimension",         "VARCHAR",      "Dev Practices | DevOps Practices | Security | Team"],
        ["competency",        "VARCHAR",      "Specific competency area"],
        ["title",             "VARCHAR",      "Action item title"],
        ["priority",          "VARCHAR",      "Critical | High | Medium | Low"],
        ["current_score",     "FLOAT",        "Current maturity score (1–10)"],
        ["target_score",      "FLOAT",        "Target maturity score"],
        ["current_level",     "VARCHAR",      "PRE-CRAWL | CRAWL | WALK | RUN | FLY"],
        ["target_level",      "VARCHAR",      "Target maturity level"],
        ["suggested_actions", "JSON",         "List of concrete actions to take"],
        ["responsible",       "VARCHAR",      "Accountable role/person"],
        ["target_date",       "VARCHAR",      "Target completion date"],
        ["status",            "VARCHAR",      "Open | In Progress | Done | Deferred"],
        ["effort_estimate",   "VARCHAR",      "Low | Medium | High"],
        ["notes",             "TEXT",         "Free-text notes"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h3("Table: scheduled_pipeline_runs")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",            "VARCHAR (PK)", "UUID"],
        ["project_id",    "VARCHAR",      "Target project ID"],
        ["trigger",       "VARCHAR",      "manual | scheduled"],
        ["status",        "VARCHAR",      "pending | running | complete | failed"],
        ["result_run_id", "VARCHAR",      "Links to analysis_runs.id"],
        ["error",         "TEXT",         "Error message if failed"],
        ["created_at",    "DATETIME",     "Trigger timestamp"],
        ["completed_at",  "DATETIME",     "Completion timestamp"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h3("Table: activity_metrics")
body("Fine-grained per-sprint metric storage for trend analysis and monitoring dashboard.")
make_table(
    ["Column", "Type", "Description"],
    [
        ["id",           "VARCHAR (PK)", "UUID"],
        ["project_id",   "VARCHAR (FK)", "→ projects.id"],
        ["phase_id",     "INTEGER",      "Phase number (1–7)"],
        ["activity_id",  "VARCHAR",      "Activity identifier"],
        ["process_time", "FLOAT",        "Process time (hours)"],
        ["wait_time",    "FLOAT",        "Wait time (hours)"],
        ["lead_time",    "FLOAT",        "Lead time (hours)"],
        ["cycle_time",   "FLOAT",        "Cycle time (hours)"],
        ["throughput",   "FLOAT",        "Items completed per period"],
        ["wip",          "FLOAT",        "Work in progress count"],
        ["source",       "VARCHAR",      "alm | manual | calculated"],
        ["period_start", "DATETIME",     "Start of measurement period"],
        ["period_end",   "DATETIME",     "End of measurement period"],
        ["created_at",   "DATETIME",     "Record creation timestamp"],
    ],
    col_widths=[1.4, 1.2, 3.9]
)

h2("6.2  Entity Relationships")
body("Key relationships between tables:")
bullet("projects (1) → (*) vsm_snapshots  [cascade delete]")
bullet("projects (1) → (*) analysis_runs  [cascade delete]")
bullet("devops_assessments (1) → (*) assessment_action_items  [cascade delete]")
bullet("projects (1) → (*) activity_metrics  [no cascade]")
bullet("scheduled_pipeline_runs.result_run_id → analysis_runs.id  [reference, no FK constraint]")

h2("6.3  Key Data Flows")
h4("Flow 1: New Project + ALM Fetch + Pipeline Run")
numbered("User submits project context form (Dashboard) → POST /projects → INSERT into projects table")
numbered("User configures ALM in ALM Connect → POST /settings/alm → stored in platform_settings")
numbered("User clicks 'Run Analysis' → POST /agents/run-analysis/{project_id}")
numbered("Backend creates AnalysisRun record (status=running) → returns run_id to frontend")
numbered("Background task invokes LangGraph pipeline: ALM Connector → … → Business Case Builder")
numbered("Each agent updates state; final state written to analysis_runs.result (status=complete)")
numbered("Frontend polls GET /agents/status/{run_id} → receives status=complete → loads results")
numbered("VSM snapshot saved to vsm_snapshots for historical tracking")

h4("Flow 2: Scheduled Pipeline Run")
numbered("APScheduler fires at configured time (stored in platform_settings)")
numbered("Scheduler calls run_full_analysis(project_id) → creates ScheduledPipelineRun record")
numbered("Same pipeline as Flow 1 executes; on completion ScheduledPipelineRun.status = complete")
numbered("Platform dashboard shows last scheduled run status")

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 7. INTEGRATION SPECIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════
h1("7. Integration Specifications")

h2("7.1  ALM Integrations")
h3("Jira Cloud")
make_table(
    ["Attribute", "Detail"],
    [
        ["Auth Method",   "Basic Auth — base64(username:api_token) in Authorization header"],
        ["API Version",   "Jira REST API v3 (/rest/api/3/)"],
        ["Key Endpoint",  "/rest/api/3/search?jql=...&maxResults=500&fields=summary,status,priority,timespent,timeoriginalestimate,assignee,created,updated"],
        ["JQL Query",     "project = {project_key} AND issuetype in (Story, Task, Bug) ORDER BY created DESC"],
        ["PT Mapping",    "timespent field (seconds → hours)"],
        ["WT Mapping",    "Derived from status transition history (time in non-active statuses)"],
        ["Pagination",    "Up to 500 issues per request; no pagination in current implementation"],
        ["Test Endpoint", "POST /alm/test-connection validates credentials before saving"],
    ],
    col_widths=[1.4, 5.1]
)

h3("Azure DevOps")
make_table(
    ["Attribute", "Detail"],
    [
        ["Auth Method",   "HTTP Basic Auth with PAT (Personal Access Token) — base64(':' + PAT)"],
        ["API Version",   "Azure DevOps REST API 7.1"],
        ["Key Endpoint",  "POST /{org}/{project}/_apis/wit/wiql?api-version=7.1"],
        ["WIQL Query",    "SELECT [Id],[Title],[State],[Effort],[Remaining Work],[Completed Work] FROM WorkItems WHERE [Team Project] = @project"],
        ["PT Mapping",    "Completed Work field (hours)"],
        ["WT Mapping",    "Derived from State transition history for Blocked/In Review/Waiting states"],
        ["Phase Mapping", "WorkItemType: Epic→Phase1, Feature→Phase2-3, User Story→Phase3-4, Task→Phase4-5, Bug→Phase5"],
    ],
    col_widths=[1.4, 5.1]
)

h2("7.2  LLM Integration")
make_table(
    ["Attribute", "Detail"],
    [
        ["Azure OpenAI Auth",  "API key in header + endpoint URL → LangChain AzureChatOpenAI"],
        ["OpenAI Auth",        "API key → LangChain ChatOpenAI"],
        ["Selection Logic",    "if azure_key AND azure_endpoint → use Azure; elif openai_key → use OpenAI; else → None"],
        ["LangChain Usage",    "chain = LLMChain(llm=get_llm(), prompt=PromptTemplate(…)) → chain.ainvoke(input)"],
        ["Prompt Style",       "System + Human message format; explicit JSON output requested via prompt suffix"],
        ["Error Handling",     "All LLM calls wrapped in try/except; errors logged to state.errors[]; pipeline continues"],
        ["Token Management",   "max_tokens=4096; typical prompt + response uses 800–2500 tokens per agent"],
        ["Config Storage",     "LLM credentials stored in platform_settings table (not .env); updatable via Settings UI"],
    ],
    col_widths=[1.6, 4.9]
)

h2("7.3  Scheduler & Pipeline Automation")
make_table(
    ["Attribute", "Detail"],
    [
        ["Library",          "APScheduler 3.x with AsyncIOScheduler"],
        ["Job Type",         "CronTrigger (configurable day_of_week + hour)"],
        ["Startup",          "Scheduler created in FastAPI lifespan() context manager; starts on app boot if schedule_enabled=true"],
        ["Config Source",    "Reads schedule_enabled, schedule_frequency, schedule_day_of_week, schedule_hour from platform_settings"],
        ["Dynamic Reconfigure", "POST /settings/schedule saves new config + removes old job + adds new job (no restart needed)"],
        ["Execution",        "Calls run_full_analysis(project_id) → creates AnalysisRun + ScheduledPipelineRun records"],
        ["Manual Trigger",   "POST /settings/schedule/trigger → immediate pipeline run independent of schedule"],
        ["Audit",            "Every run (scheduled or manual) creates ScheduledPipelineRun record with timestamps + status"],
    ],
    col_widths=[1.6, 4.9]
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 8. PDLC PHASES, ACTIVITIES & BENCHMARKS
# ═══════════════════════════════════════════════════════════════════════════════
h1("8. PDLC Phases, Activities & Benchmarks")

body("The STUMP platform maps all software delivery work to 7 standardised PDLC phases with 36 discrete activities.")

make_table(
    ["Phase", "Name", "Activities", "Benchmark PT (p50)", "Benchmark WT (p50)", "Target FE (p75)"],
    [
        ["1", "Backlog & Roadmap",       "Portfolio Epic/VSM Tracking, Product Roadmap, Feature Definition & Refinement, BDD Scenario Writing, User Story Creation",             "25 hrs", "48 hrs",  "34%"],
        ["2", "Architecture & UX Design","Solution Architecture, UX/UI Research, HiFi Design & Handoff, Technical Design",                                                      "30 hrs", "96 hrs",  "24%"],
        ["3", "Code Management",         "Feature Development, Unit Testing, Code Quality/LGTM, Peer Code Review, Knowledge Transfer/Docs",                                     "20 hrs", "8 hrs",   "71%"],
        ["4", "Continuous Integration",  "Build Process (CI), SAST, Artifact Creation, DEV Deployment",                                                                         "3 hrs",  "4 hrs",   "43%"],
        ["5", "Continuous Testing",      "Test Environment Setup, Test Data Gen, BVT, Component Regression, Full Regression, Performance Testing, DAST, Manual SIT/UAT, Defect Triage", "20 hrs", "16 hrs",  "55%"],
        ["6", "Continuous Delivery",     "IaC, Stage Deployment, Release Gates/Approvals, Production Deployment, Release Notes Gen",                                            "6 hrs",  "48 hrs",  "11%"],
        ["7", "Monitoring & Feedback",   "APM, Log Aggregation, Incident Management & RCA, Customer Feedback Loop",                                                             "5 hrs",  "12 hrs",  "29%"],
    ],
    col_widths=[0.4, 1.6, 2.2, 1.0, 1.0, 0.8]
)

body("Key observations from benchmark data:")
bullet("Phase 6 (Continuous Delivery) has the lowest FE% target (11%) — release gates and approval processes are the most significant source of wait time across the industry")
bullet("Phase 3 (Code Management) has the highest FE% target (71%) — modern CI/CD and code review tooling has made this phase the most efficient")
bullet("Phase 2 (Architecture & UX Design) has the highest absolute wait time (96 hrs p50) — design review and stakeholder approval cycles dominate")
bullet("Phase 5 (Continuous Testing) has the most activities (9) and highest process time variability — a primary target for AI automation")

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 9. API REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
h1("9. API Reference")
body("All API routes are mounted under /api/v1. The FastAPI application serves an OpenAPI spec at /docs (Swagger UI) and /redoc.")

h2("9.1  Projects API  (/api/v1/projects)")
make_table(
    ["Method", "Path", "Request Body", "Response", "Description"],
    [
        ["GET",    "/",          "—",                    "Project[]",    "List all projects (sorted by created_at desc)"],
        ["POST",   "/",          "ProjectCreate",        "Project (201)","Create new project"],
        ["GET",    "/{id}",      "—",                    "Project",      "Get project by ID (404 if not found)"],
        ["PUT",    "/{id}",      "ProjectUpdate",        "Project",      "Update project fields (partial update)"],
        ["DELETE", "/{id}",      "—",                    "204",          "Delete project + all related data"],
    ],
    col_widths=[0.7, 1.0, 1.5, 1.0, 2.3]
)
body("ProjectCreate / ProjectUpdate fields: name, organization, portfolio, product_group, product, team, industry, portfolios (JSON), product_groups (JSON), alm_tool, alm_config (JSON)")

h2("9.2  VSM API  (/api/v1/vsm)")
make_table(
    ["Method", "Path", "Description"],
    [
        ["POST", "/{project_id}",          "Save new VSM snapshot for project (source, raw_data, vsm_data, summary, overrides)"],
        ["GET",  "/{project_id}",          "Get latest VSM snapshot for project"],
        ["PUT",  "/{project_id}",          "Update existing snapshot with new overrides"],
        ["GET",  "/{project_id}/metrics",  "Get computed metrics from latest snapshot"],
    ],
    col_widths=[0.7, 1.6, 4.2]
)

h2("9.3  Agents API  (/api/v1/agents)")
make_table(
    ["Method", "Path", "Description"],
    [
        ["POST", "/run-analysis/{project_id}",  "Trigger full 7-agent pipeline; returns {run_id} immediately"],
        ["GET",  "/status/{run_id}",             "Poll pipeline status: {status, completed_at, agents_run[]}"],
        ["GET",  "/result/{project_id}",         "Get latest completed analysis result (full JSON)"],
        ["GET",  "/history/{project_id}",        "List all analysis runs for project"],
        ["POST", "/alm/{project_id}",            "Run ALM Connector only"],
        ["POST", "/vsm/{project_id}",            "Run VSM Analyzer only"],
        ["POST", "/bottlenecks/{project_id}",    "Run Bottleneck Analyzer only"],
        ["POST", "/improvements/{project_id}",   "Run Improvement Generator only"],
        ["POST", "/future-state/{project_id}",   "Run Future State Designer only"],
        ["POST", "/business-case/{project_id}",  "Run Business Case Builder only"],
        ["POST", "/playbook/{project_id}",       "Run Playbook Contextualizer (on-demand)"],
    ],
    col_widths=[0.7, 2.2, 3.6]
)

h2("9.4  Settings API  (/api/v1/settings)")
make_table(
    ["Method", "Path", "Description"],
    [
        ["GET",  "/status",           "Platform status: LLM availability, ALM connectivity, last run"],
        ["GET",  "/llm",              "Get current LLM configuration (keys masked)"],
        ["POST", "/llm",              "Save LLM configuration to platform_settings"],
        ["POST", "/llm/test",         "Test LLM connection with stored credentials"],
        ["GET",  "/alm",              "Get ALM configuration (token masked)"],
        ["POST", "/alm",              "Save ALM configuration"],
        ["POST", "/alm/test",         "Test ALM connection"],
        ["GET",  "/schedule",         "Get pipeline schedule configuration"],
        ["POST", "/schedule",         "Save schedule configuration (dynamically reconfigures APScheduler job)"],
        ["POST", "/schedule/trigger", "Manually trigger pipeline run immediately"],
    ],
    col_widths=[0.7, 1.6, 4.2]
)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 10. SECURITY, CONFIGURATION & DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════
h1("10. Security, Configuration & Deployment")

h2("10.1  Credential Management")
body("STUMP uses a two-layer credential management approach:")
bullet("Layer 1: .env file — database URL and any bootstrap values (not used for LLM/ALM in production)")
bullet("Layer 2: platform_settings table — LLM API keys, ALM tokens, schedule config stored in DB and editable via the Settings UI without service restart")
body("Security considerations:")
bullet("ALM tokens stored as plain text in DB — recommend encryption at rest using PostgreSQL pgcrypto for production deployments")
bullet("LLM API keys exposed to backend process only — never sent to frontend (masked in GET /settings/llm response)")
bullet("CORS restricted to known localhost origins — update fastapi.middleware.cors for production domains")

h2("10.2  Environment Variables (.env)")
make_table(
    ["Variable",                "Required", "Description"],
    [
        ["DATABASE_URL",              "Yes",  "PostgreSQL connection: postgresql+asyncpg://user@host:5432/db"],
        ["AZURE_OPENAI_API_KEY",      "No",   "Azure OpenAI API key (overrides platform_settings)"],
        ["AZURE_OPENAI_ENDPOINT",     "No",   "Azure OpenAI endpoint URL"],
        ["AZURE_OPENAI_DEPLOYMENT",   "No",   "Deployment name (e.g. gpt-4o)"],
        ["AZURE_OPENAI_API_VERSION",  "No",   "API version (e.g. 2024-02-15-preview)"],
        ["OPENAI_API_KEY",            "No",   "Standard OpenAI API key (fallback)"],
        ["JIRA_URL",                  "No",   "Jira Cloud base URL"],
        ["JIRA_USERNAME",             "No",   "Jira username (email)"],
        ["JIRA_API_TOKEN",            "No",   "Jira API token"],
        ["ADO_ORG_URL",               "No",   "Azure DevOps organisation URL"],
        ["ADO_PAT",                   "No",   "Azure DevOps Personal Access Token"],
    ],
    col_widths=[2.2, 0.8, 3.5]
)

h2("10.3  Startup Sequence")
numbered("FastAPI lifespan() called on server start")
numbered("Database connection pool created (asyncpg); Base.metadata.create_all() runs (creates tables if not exist)")
numbered("Platform settings loaded from DB; LLM factory initialised")
numbered("APScheduler started; existing schedule job loaded from platform_settings if schedule_enabled=true")
numbered("All 11 routers mounted; CORS middleware applied")
numbered("Server ready on port 8001 (configurable)")

h2("10.4  Ports & Services")
make_table(
    ["Service", "Port", "Notes"],
    [
        ["Frontend (Vite dev server)",    "3001", "npm run dev in /frontend"],
        ["Backend (Uvicorn)",             "8001", "python -m uvicorn backend.main:app --reload --port 8001"],
        ["PostgreSQL",                    "5432", "Default PostgreSQL port; database: stump_db"],
        ["Swagger UI",                    "8001", "http://localhost:8001/docs"],
    ],
    col_widths=[2.2, 0.8, 3.5]
)

h2("10.5  Running the Platform")
h4("Prerequisites")
bullet("Python 3.11+ with pip")
bullet("Node.js 18+ with npm")
bullet("PostgreSQL 15+ (Postgres.app recommended on macOS)")
h4("Backend Startup")
body("From project root with virtual environment active:")
callout("cd /path/to/pdlc-vsm-platform", MGRAY)
callout("python -m venv backend/venv && source backend/venv/bin/activate", MGRAY)
callout("pip install -r backend/requirements.txt", MGRAY)
callout("python -m uvicorn backend.main:app --reload --port 8001", MGRAY)
h4("Frontend Startup")
callout("cd frontend && npm install && npm run dev", MGRAY)
h4("Database Migration (SQLite → PostgreSQL)")
callout("python migrate_sqlite_to_postgres.py  # one-time migration script", MGRAY)

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 11. GLOSSARY
# ═══════════════════════════════════════════════════════════════════════════════
h1("11. Glossary")
make_table(
    ["Term", "Definition"],
    [
        ["ALM",                "Application Lifecycle Management — tools (Jira, Azure DevOps) that track work items through the SDLC"],
        ["APScheduler",        "Advanced Python Scheduler — async job scheduler used for automated pipeline runs"],
        ["DORA",               "DevOps Research & Assessment — framework defining four software delivery performance metrics: Deployment Frequency, Lead Time for Change, Change Failure Rate, MTTR"],
        ["FE%",                "Flow Efficiency % — proportion of total lead time spent on value-adding work: PT / (PT + WT) × 100"],
        ["LangGraph",          "Python framework from LangChain for building stateful multi-agent workflows as directed graphs"],
        ["Lead Time",          "Total elapsed time from work item creation to production deployment (includes all PT and WT)"],
        ["LT for Change",      "DORA metric: time from code commit to production deployment"],
        ["Lean VSM",           "Lean Value Stream Mapping — manufacturing process analysis technique applied to software delivery"],
        ["MTTR",               "Mean Time to Recovery — average time to restore service after a production incident"],
        ["Option A",           "STUMP transformation scenario: AI as assistants and co-pilots (40% automation, all human roles retained)"],
        ["Option B",           "STUMP transformation scenario: selective autonomous agents (65% automation, 5 core human roles)"],
        ["Option C",           "STUMP transformation scenario: agent-first orchestration (85% automation, human role = oversee/review/approve only)"],
        ["PDLC",               "Product Development Lifecycle — the end-to-end process from product backlog to production monitoring"],
        ["Process Time (PT)",  "Time actively spent working on a task (value-adding time)"],
        ["RAG",                "Retrieval-Augmented Generation — technique to ground LLM responses in specific documents from a knowledge base"],
        ["STUMP",              "Strategic Transformation Unified Mapping Platform — the platform described in this document"],
        ["VSM",                "Value Stream Map — visual representation of the flow of work, materials and information through a process"],
        ["Wait Time (WT)",     "Time a task spends queued, blocked, or waiting (non-value-adding time)"],
        ["WIP",                "Work in Progress — count of tasks simultaneously in an active (non-complete) state"],
    ],
    col_widths=[1.6, 4.9]
)

# ── Footer ─────────────────────────────────────────────────────────────────────
doc.add_paragraph()
p_end = doc.add_paragraph()
p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_end = p_end.add_run("— End of Document —")
r_end.font.size  = Pt(10)
r_end.font.italic = True
r_end.font.color.rgb = MGRAY

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/Users/125066/projects/pdlc-vsm-platform/STUMP-Platform-Functional-Tech-Spec.docx"
doc.save(out)
print(f"Saved → {out}")
