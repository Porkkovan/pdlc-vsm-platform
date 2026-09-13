"""
GTM Pack — Set 2: Pilot Engagement Pack
Generates 12 files for running a paid pilot engagement.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from docx import Document
from docx.shared import Pt as DPt, RGBColor as DRGBColor, Inches as DInches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

OUT = os.path.join(os.path.dirname(__file__), "set2-pilot-engagement-pack")
os.makedirs(OUT, exist_ok=True)

# ─── Colors ──────────────────────────────────────────────────────────────────
DARK_BLUE  = RGBColor(0x0F, 0x2D, 0x5E)
MED_BLUE   = RGBColor(0x25, 0x63, 0xEB)
LIGHT_BLUE = RGBColor(0xDB, 0xEA, 0xFE)
ACCENT     = RGBColor(0x0D, 0x94, 0x88)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT  = RGBColor(0x1E, 0x29, 0x3B)
GRAY       = RGBColor(0xE2, 0xE8, 0xF0)

# Doc colors
DNAVY  = DRGBColor(0x0F, 0x2D, 0x5E)
DBLUE  = DRGBColor(0x25, 0x63, 0xEB)
DTEAL  = DRGBColor(0x0D, 0x94, 0x88)
DLIGHT = DRGBColor(0xDB, 0xEA, 0xFE)
DWHT   = DRGBColor(0xFF, 0xFF, 0xFF)
DGRAY  = DRGBColor(0xE2, 0xE8, 0xF0)

# ─── PPTX Helpers ────────────────────────────────────────────────────────────
def new_prs():
    prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
    return prs

def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def rect(slide, x, y, w, h, fill=None, line=None):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid(); shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line; shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def txtbox(slide, text, x, y, w, h, size=12, bold=False, color=None, align=PP_ALIGN.LEFT, italic=False, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.word_wrap = wrap
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size = Pt(size); run.font.bold = bold; run.font.italic = italic
    run.font.color.rgb = color or DARK_TEXT
    return tb

def header_bar(slide, title, subtitle=None):
    rect(slide, 0, 0, 13.33, 1.1, fill=DARK_BLUE)
    txtbox(slide, title, 0.4, 0.12, 10, 0.55, size=24, bold=True, color=WHITE)
    if subtitle:
        txtbox(slide, subtitle, 0.4, 0.65, 10, 0.38, size=12, color=RGBColor(0xBF,0xDB,0xFE))

def stat_box(slide, x, y, w, h, value, label, bg=MED_BLUE):
    rect(slide, x, y, w, h, fill=bg)
    txtbox(slide, value, x, y+0.08, w, h*0.55, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(slide, label, x, y+h*0.52, w, h*0.45, size=9, color=WHITE, align=PP_ALIGN.CENTER)

def accent_box(slide, x, y, w, h, title, body_text):
    rect(slide, x, y, w, 0.3, fill=MED_BLUE)
    txtbox(slide, title, x+0.05, y+0.02, w-0.1, 0.28, size=10, bold=True, color=WHITE)
    rect(slide, x, y+0.3, w, h-0.3, fill=LIGHT_BLUE)
    txtbox(slide, body_text, x+0.08, y+0.35, w-0.16, h-0.45, size=9, color=DARK_TEXT, wrap=True)

# ─── DOCX Helpers ────────────────────────────────────────────────────────────
def new_doc(title=""):
    d = Document()
    for s in d.styles:
        try:
            if hasattr(s,'font'):
                s.font.name = "Calibri"
        except: pass
    sec = d.sections[0]
    sec.top_margin = Cm(2); sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
    return d

def sf(run, size, bold=False, italic=False, color=None):
    run.font.name = "Calibri"; run.font.size = DPt(size)
    run.font.bold = bold; run.font.italic = italic
    if color: run.font.color.rgb = color

def h1(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = DPt(14); p.paragraph_format.space_after = DPt(4)
    r = p.add_run(text); sf(r, 16, bold=True, color=DNAVY); return p

def h2(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = DPt(10); p.paragraph_format.space_after = DPt(3)
    r = p.add_run(text); sf(r, 13, bold=True, color=DBLUE); return p

def h3(doc, text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = DPt(8); p.paragraph_format.space_after = DPt(2)
    r = p.add_run(text); sf(r, 11, bold=True, color=DNAVY); return p

def body(doc, text, italic=False, color=None):
    p = doc.add_paragraph(); p.paragraph_format.space_after = DPt(4)
    r = p.add_run(text); sf(r, 10.5, italic=italic, color=color); return p

def bul(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = DPt(18 + level*18)
    p.paragraph_format.space_after = DPt(2)
    r = p.add_run(text); sf(r, 10.5); return p

def num(doc, text, level=0):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = DPt(18 + level*18)
    p.paragraph_format.space_after = DPt(2)
    r = p.add_run(text); sf(r, 10.5); return p

def tbl(doc, headers, rows, col_widths=None):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.LEFT
    # Header row
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        tc = cell._tc; tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto')
        shd.set(qn('w:fill'),'0F2D5E'); tcPr.append(shd)
        p2 = cell.paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run(h); sf(r2, 9.5, bold=True, color=DWHT)
    # Data rows
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.rows[ri+1].cells[ci]
            if ri % 2 == 0:
                tc = cell._tc; tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto')
                shd.set(qn('w:fill'),'EFF6FF'); tcPr.append(shd)
            p2 = cell.paragraphs[0]
            r2 = p2.add_run(str(val)); sf(r2, 9.5)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in t.rows:
                row.cells[i].width = DInches(w)
    doc.add_paragraph()
    return t

def divider(doc):
    p = doc.add_paragraph(); p.paragraph_format.space_before = DPt(6); p.paragraph_format.space_after = DPt(6)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'),'single'); bottom.set(qn('w:sz'),'6')
    bottom.set(qn('w:space'),'1'); bottom.set(qn('w:color'),'2563EB')
    pBdr.append(bottom); pPr.append(pBdr)

def callout(doc, text, color_fill="DBEAFE"):
    p = doc.add_paragraph(); p.paragraph_format.space_before = DPt(6); p.paragraph_format.space_after = DPt(6)
    p.paragraph_format.left_indent = DPt(24); p.paragraph_format.right_indent = DPt(24)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear')
    shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),color_fill)
    pPr.append(shd)
    r = p.add_run(text); sf(r, 10.5, italic=True, color=DNAVY)

def set_bg(doc, hex_color="EFF6FF"):
    body_el = doc.element.body
    sectPr = body_el.get_or_add_sectPr()

def cover_page(doc, title, subtitle, doc_number, version="v1.0"):
    p = doc.add_paragraph(); p.paragraph_format.space_before = DPt(60)
    r = p.add_run("PDLC VSM Platform"); sf(r, 13, bold=True, color=DBLUE)
    p = doc.add_paragraph()
    r = p.add_run("GTM Pack — Set 2: Pilot Engagement Pack"); sf(r, 11, color=DNAVY)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(title); sf(r, 22, bold=True, color=DNAVY)
    p = doc.add_paragraph()
    r = p.add_run(subtitle); sf(r, 12, italic=True, color=DBLUE)
    doc.add_paragraph(); doc.add_paragraph()
    divider(doc)
    tbl(doc, ["Document", "Version", "Date", "Classification"],
        [[doc_number, version, "March 2026", "Commercial Confidential"]])
    doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 11 — Pilot Proposal Template
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 11-pilot-proposal-template.docx...")
d = new_doc()
cover_page(d,"Pilot Proposal Template","AI-Powered PDLC Value Stream Analysis — Paid Pilot","DOC-SET2-11")
h1(d,"Executive Summary")
body(d,"This proposal outlines a structured 8-week paid pilot engagement to quantify your software delivery lead time, identify the top 3–5 value stream bottlenecks, and produce a board-ready business case for AI-assisted flow improvement. The pilot is designed to be low-risk, high-speed, and independently verifiable.")
callout(d,"Investment: $150,000 fixed fee  |  Duration: 8 weeks  |  Risk: Full-refund guarantee if savings < $500K/year identified")
divider(d)

h1(d,"Business Context")
h2(d,"The Problem We Are Solving")
for item in [
    "Average financial services delivery lead time: 34–47 days per feature",
    "Flow efficiency (actual work vs. queue time) averages 17.8% in your sector — 82% of time is waste",
    "Manual bottleneck identification takes 3–6 months of consultant time",
    "Business cases for DevOps investment lack quantified ROI — causing approval delays",
    "DORA benchmark gap analysis requires specialist expertise and months of data collection",
]:
    bul(d, item)

h2(d,"What Changes After the Pilot")
for item in [
    "Real-time VSM dashboard from your existing Jira / Azure DevOps data — no new tooling required",
    "Top 5 bottlenecks identified with hours of waste per quarter, root cause, and industry benchmark comparison",
    "AI-generated improvement roadmap: 12 Quick Wins (90-day), 8 Medium-term (6-month), 5 Strategic (12-month)",
    "Board-ready business case: ROI, payback period, NPV, and scenario modelling",
    "DORA maturity assessment: current band, target band, and a 73-question gap analysis",
]:
    bul(d, item)

divider(d)
h1(d,"Scope of Work")
h2(d,"Phase 1: Data Onboarding (Weeks 1–2)")
tbl(d, ["Activity", "Owner", "Output", "Effort"],
    [
        ["Jira / ADO export configuration", "Client IT + Pilot Lead", "CSV data file (25+ fields)", "2 hours client"],
        ["Platform deployment (cloud or on-prem)", "Pilot Lead", "Running instance on client infra", "1 day"],
        ["ALM connector configuration", "Pilot Lead", "Phase mapping validated", "4 hours"],
        ["Data quality review", "Pilot Lead + Client", "Data quality scorecard", "2 hours client"],
        ["DORA source configuration", "Client Team Lead", "4 data sources configured", "3 hours client"],
    ],
    col_widths=[2.8, 1.8, 2.4, 1.4])

h2(d,"Phase 2: AI Analysis (Weeks 3–4)")
tbl(d, ["Agent", "Input", "Output", "Duration"],
    [
        ["VSM Analyzer", "ALM export (2,847+ tickets)", "Current state VSM: LT, FE, WT by phase", "Automated"],
        ["DORA Assessment Agent", "4 configured sources", "73-question gap score, band assignment", "Automated"],
        ["Benchmark Agent", "VSM + DORA scores", "Peer comparison across 12 competitors", "Automated"],
        ["Bottleneck Analyzer", "VSM + DORA + benchmarks", "Top 5 bottlenecks with severity scores", "Automated"],
        ["Improvement Generator", "All above", "25–35 ranked AI improvement initiatives", "Automated"],
        ["Future State Designer", "All above", "3 future-state scenarios (Option A/B/C)", "Automated"],
        ["Business Case Builder", "Future state scenarios", "3 scenarios × ROI / payback / NPV", "Automated"],
    ],
    col_widths=[2.0, 2.5, 2.5, 1.4])

h2(d,"Phase 3: Validation & Calibration (Weeks 5–6)")
for item in [
    "Stakeholder review session: Pilot Lead presents AI findings to client team lead and 2 engineers",
    "Manual override capability: client team adjusts any AI score via the platform UI",
    "Benchmark calibration: DORA weights adjusted based on team's self-assessment",
    "Business case scenario selection: client selects preferred investment option for CFO presentation",
]:
    bul(d, item)

h2(d,"Phase 4: Delivery & Readout (Weeks 7–8)")
for item in [
    "Executive readout deck (PPT): 15 slides, board-ready, with your organisation's branding guidelines applied",
    "Action plan in the platform: 25+ items with owner, target date, effort estimate, and status tracking",
    "Playbook contextualisation: 3 AI-tailored implementation playbooks (one per scenario)",
    "Platform handover: client team trained, login credentials set up, 30-day post-pilot support included",
]:
    bul(d, item)

divider(d)
h1(d,"Deliverables Summary")
tbl(d, ["#", "Deliverable", "Format", "Audience", "Date"],
    [
        ["D1", "Current State VSM Dashboard", "Platform (live)", "Engineering team", "Week 3"],
        ["D2", "DORA Assessment Report", "Platform + PDF export", "Engineering + CTO", "Week 4"],
        ["D3", "Top 5 Bottleneck Analysis", "Platform + slide deck", "CTO + VP Eng", "Week 4"],
        ["D4", "AI Improvement Roadmap", "Platform + PDF export", "CTO + VP Eng", "Week 5"],
        ["D5", "Business Case (3 scenarios)", "Platform + slide deck", "CFO + CEO", "Week 6"],
        ["D6", "Executive Readout Deck", "PowerPoint (15 slides)", "Board / ELT", "Week 8"],
        ["D7", "Action Plan (25+ items)", "Platform (live)", "Team Lead", "Week 7"],
        ["D8", "Implementation Playbooks (×3)", "Platform + PDF export", "Programme team", "Week 8"],
        ["D9", "Knowledge transfer session", "60-min live session", "Platform Admin", "Week 8"],
    ],
    col_widths=[0.4, 2.5, 1.8, 1.8, 1.0])

divider(d)
h1(d,"Commercial Terms")
h2(d,"Pricing")
tbl(d, ["Item", "Description", "Price"],
    [
        ["Pilot Fixed Fee", "Full 8-week engagement as scoped above", "$150,000"],
        ["Success Guarantee", "Full refund if < $500K annual savings identified", "Included"],
        ["Post-Pilot Support", "30-day named support contact", "Included"],
        ["Scale Licence (optional)", "Full platform licence post-pilot", "POA"],
    ],
    col_widths=[2.5, 4.5, 1.5])

h2(d,"Risk Mitigation")
tbl(d, ["Risk", "Likelihood", "Mitigation"],
    [
        ["ALM data quality issues", "Medium", "Data quality scorecard in Week 1; 2-week remediation window"],
        ["Stakeholder availability", "Low", "Asynchronous review via platform; 1h max per week for client team"],
        ["Data privacy concerns", "Low", "On-prem deployment option; anonymisation scripts provided"],
        ["Platform performance", "Low", "Handles 100K+ tickets; horizontal scaling available"],
        ["Findings inconclusive", "Very Low", "Guaranteed: ≥3 bottlenecks or full refund"],
    ],
    col_widths=[2.5, 1.5, 4.5])

callout(d,"Success Condition: We guarantee identification of ≥3 material bottlenecks and a minimum $500,000 annual savings opportunity. If not achieved, 100% fee refund — no questions asked.")
d.add_paragraph()
body(d,"Authorised by: ___________________________   Date: _______________")
body(d,"Client: ___________________________   Title: _______________")
d.save(os.path.join(OUT,"11-pilot-proposal-template.docx"))
print("  ✓ Saved: 11-pilot-proposal-template.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 12 — Project Charter
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 12-project-charter.docx...")
d = new_doc()
cover_page(d,"Project Charter","AI-Powered PDLC VSM Pilot Engagement","DOC-SET2-12")
h1(d,"Project Overview")
tbl(d, ["Field", "Value"],
    [
        ["Project Name", "PDLC VSM Platform — AI Pilot Engagement"],
        ["Client Organisation", "[CLIENT NAME]"],
        ["Project Sponsor", "[SPONSOR NAME], [TITLE]"],
        ["Project Manager (Pilot Lead)", "[PILOT LEAD NAME]"],
        ["Client Project Lead", "[CLIENT LEAD NAME], [TITLE]"],
        ["Start Date", "[START DATE]"],
        ["End Date", "[START DATE + 8 weeks]"],
        ["Budget", "$150,000 (fixed fee)"],
        ["Classification", "Commercial Confidential"],
    ], col_widths=[2.5, 5.5])

h1(d,"Project Objectives")
for obj in [
    "Quantify the current state software delivery lead time and flow efficiency using the client's existing ALM data",
    "Identify the top 3–5 value stream bottlenecks with quantified waste hours and peer benchmark comparisons",
    "Generate a ranked AI improvement roadmap (Quick Wins / Medium-term / Strategic) with ROI estimates",
    "Produce a board-ready business case across three investment scenarios (Conservative / Expected / Optimistic)",
    "Conduct a 73-question DORA maturity assessment across Continuous Integration, Deployment, Testing, and Culture dimensions",
    "Transfer platform capability to the client team via training and documentation",
]:
    num(d, obj)

h1(d,"Scope")
h2(d,"In Scope")
for item in [
    "One ALM data source (Jira or Azure DevOps)",
    "One product group / team (up to 5,000 tickets, 18 months history)",
    "Four DORA data sources (Jira, Confluence, Sonar, GitHub)",
    "Eight AI agent runs (VSM Analyzer, DORA Assessment, Benchmark, Bottleneck, Improvement, Future State, Business Case, Playbook)",
    "One executive readout deck (15 slides, client-branded)",
    "One action plan (up to 30 items)",
    "Three implementation playbooks (one per future-state scenario)",
    "One knowledge transfer session (60 minutes)",
    "30-day post-pilot support (email, named contact)",
]:
    bul(d, item)

h2(d,"Out of Scope")
for item in [
    "Implementation of any improvement initiative (delivery is separate engagement)",
    "Integration with ITSM, monitoring, or CI/CD tooling",
    "More than one product group per pilot",
    "Custom AI agent development",
    "Data migration or ALM re-configuration",
]:
    bul(d, item)

h1(d,"Governance")
h2(d,"Roles and Responsibilities")
tbl(d, ["Role", "Name", "Responsibility", "Availability"],
    [
        ["Project Sponsor", "[SPONSOR]", "Overall approval, executive access", "2h/week"],
        ["Client Project Lead", "[LEAD]", "Data access, stakeholder coordination", "4h/week"],
        ["Platform Administrator", "[ADMIN]", "Platform setup, IT access", "8h Week 1"],
        ["Engineering SME (×2)", "[NAMES]", "Data validation, VSM review", "2h/week"],
        ["Pilot Lead (our team)", "[PILOT LEAD]", "Platform configuration, analysis", "Full-time"],
        ["Delivery Analyst", "[ANALYST]", "QA, documentation, reporting", "Full-time"],
    ], col_widths=[2.0, 1.8, 3.2, 1.4])

h2(d,"Meetings")
tbl(d, ["Meeting", "Frequency", "Duration", "Attendees", "Purpose"],
    [
        ["Project Kick-off", "Week 1 (once)", "90 min", "All stakeholders", "Alignment, platform demo, data planning"],
        ["Weekly Status", "Weekly (Weeks 2–7)", "30 min", "Project Leads", "Progress, risks, actions"],
        ["Phase Review", "End of each phase", "60 min", "Sponsor + Leads", "Deliverable sign-off"],
        ["Executive Readout", "Week 8", "60 min", "ELT / Board", "Final findings + next steps"],
    ], col_widths=[2.0, 1.6, 1.2, 1.8, 2.8])

h1(d,"Success Criteria")
tbl(d, ["Criterion", "Measure", "Target"],
    [
        ["Data onboarding", "ALM tickets loaded and mapped", "100% of target ticket set"],
        ["VSM accuracy", "Lead time within ±10% of manual audit", "Validated by client engineer"],
        ["Bottleneck identification", "Number of bottlenecks found", "Minimum 3 critical/high"],
        ["Savings identification", "Annual savings opportunity", "Minimum $500,000"],
        ["Business case quality", "CFO readability score (1-5)", "Score ≥4 from sponsor"],
        ["Training completion", "Platform admin certified", "100% of named admins"],
    ], col_widths=[2.5, 2.5, 3.5])

h1(d,"Change Control")
body(d,"Any change to scope, budget, or timeline requires a Change Request signed by both the Project Sponsor and Pilot Lead. Changes to deliverables require 5 business days' notice. Out-of-scope work will be quoted separately before commencement.")
d.add_paragraph()
body(d,"Project Sponsor Signature: ___________________________   Date: _______________")
body(d,"Pilot Lead Signature: ___________________________   Date: _______________")
d.save(os.path.join(OUT,"12-project-charter.docx"))
print("  ✓ Saved: 12-project-charter.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 13 — Pilot Delivery Runbook
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 13-pilot-delivery-runbook.docx...")
d = new_doc()
cover_page(d,"Pilot Delivery Runbook","Step-by-Step Configuration and Execution Guide for Pilot Leads","DOC-SET2-13")
h1(d,"Purpose")
body(d,"This runbook is the definitive reference for the Pilot Lead executing a PDLC VSM Platform pilot engagement. It covers every technical and process step from contract signature to executive readout. Follow each step in sequence; do not skip steps without documented justification.")
callout(d,"Runbook Version: 1.0  |  Platform Version: 1.0  |  Last Updated: March 2026  |  Owner: Delivery Practice Lead")

h1(d,"Pre-Engagement Checklist (T-5 Business Days)")
for item in [
    "Contract signed and purchase order received",
    "Kick-off meeting scheduled (90 min, all stakeholders)",
    "Data sharing agreement / NDA executed",
    "Deployment mode confirmed: Cloud (SaaS) or On-premises",
    "Client IT contact name and email obtained",
    "ALM system confirmed: Jira Cloud / Jira Server / Azure DevOps",
    "Client GitHub / ADO token scope confirmed (read-only minimum)",
    "Platform licence key generated and tested",
    "Pilot Lead laptop: Python 3.11+, Node 18+, Docker (for on-prem option)",
]:
    bul(d, item)

h1(d,"Week 1: Kick-off and Data Onboarding")
h2(d,"Day 1 — Kick-off Meeting Agenda")
tbl(d, ["Time", "Topic", "Owner", "Materials"],
    [
        ["0:00–0:15", "Welcome and introductions", "Pilot Lead", "Agenda slide"],
        ["0:15–0:30", "Platform live demo (5-screen walkthrough)", "Pilot Lead", "Laptop, 3001/8001"],
        ["0:30–0:45", "Data requirements: ALM export fields", "Pilot Lead + Client IT", "Data spec sheet"],
        ["0:45–1:00", "DORA source configuration walkthrough", "Pilot Lead", "Platform UI"],
        ["1:00–1:15", "Pilot timeline and milestone review", "Pilot Lead", "Project charter"],
        ["1:15–1:30", "Q&A and next steps", "All", "Action log"],
    ], col_widths=[1.2, 2.8, 2.0, 2.4])

h2(d,"Day 2–3 — Platform Deployment")
for step, detail in [
    ("Clone repository", "git clone https://github.com/[org]/pdlc-vsm-platform.git && cd pdlc-vsm-platform"),
    ("Create .env file", "Copy .env.example, set OPENAI_API_KEY, DATABASE_URL, SECRET_KEY"),
    ("Install backend", "python3 -m venv backend/venv && source backend/venv/bin/activate && pip install -r backend/requirements.txt"),
    ("Run migrations", "alembic upgrade head (creates 12 tables in SQLite or PostgreSQL)"),
    ("Install frontend", "cd frontend && npm install && cd .."),
    ("Start backend", "uvicorn backend.main:app --reload --port 8001"),
    ("Start frontend", "cd frontend && npm run dev (runs on :3001)"),
    ("Verify health", "curl http://localhost:8001/health — should return {status: ok}"),
]:
    h3(d, step); body(d, detail)

h2(d,"Day 3–5 — ALM Data Onboarding")
body(d,"Request the following fields from the client's Jira / ADO export:")
tbl(d, ["Field", "Jira Field Name", "ADO Field Name", "Required?"],
    [
        ["Issue Key", "Issue Key", "Work Item ID", "Yes"],
        ["Issue Type", "Issue Type", "Work Item Type", "Yes"],
        ["Summary/Title", "Summary", "Title", "Yes"],
        ["Status", "Status", "State", "Yes"],
        ["Created Date", "Created", "Created Date", "Yes"],
        ["Resolved Date", "Resolved", "Closed Date", "Yes"],
        ["Sprint", "Sprint", "Iteration Path", "Yes"],
        ["Story Points", "Story Points", "Story Points", "Recommended"],
        ["Priority", "Priority", "Priority", "Recommended"],
        ["Epic Link", "Epic Link", "Epic", "Recommended"],
        ["Assignee", "Assignee", "Assigned To", "Optional"],
        ["Component", "Component", "Area Path", "Optional"],
    ], col_widths=[2.0, 1.8, 1.8, 1.2])

h1(d,"Week 2: DORA Assessment Configuration")
for source, steps in [
    ("Jira", ["Navigate to Platform > DORA Assessment > Configure Sources", "Select source type: Jira", "Enter Jira base URL (e.g., https://yourcompany.atlassian.net)", "Enter Jira API token (read-only scope)", "Click 'Test Connection' — green tick required", "Save source as 'Jira-DORA'"]),
    ("Confluence", ["Select source type: Confluence", "Enter Confluence base URL", "Enter API token (same as Jira if Atlassian Cloud)", "Save source as 'Confluence-DORA'"]),
    ("SonarQube", ["Select source type: SonarQube", "Enter SonarQube server URL and project key", "Enter SonarQube token (read-only)", "Save source as 'Sonar-DORA'"]),
    ("GitHub", ["Select source type: GitHub", "Enter repository URL (format: https://github.com/org/repo)", "Enter Personal Access Token (repo: read scope)", "Save source as 'GitHub-DORA'"]),
]:
    h3(d, f"Configuring {source}")
    for s in steps: bul(d, s)

h1(d,"Week 3–4: AI Agent Execution")
h2(d,"Running the Full Pipeline")
body(d,"Navigate to Platform > Analysis > Run Full Analysis. Click the blue 'Run Full Analysis' button. The 8-agent pipeline executes in order and typically completes in 4–8 minutes depending on ticket volume.")
tbl(d, ["Agent", "Expected Duration", "Output Location", "Validation Check"],
    [
        ["VSM Analyzer", "60–90 seconds", "Current State VSM page", "Lead time within ±10% of manual estimate"],
        ["Benchmark Agent", "30–45 seconds", "Bottleneck page (benchmarks column)", "≥8 competitors shown"],
        ["Bottleneck Analyzer", "45–60 seconds", "Bottlenecks page", "≥3 bottlenecks with severity scores"],
        ["Improvement Generator", "90–120 seconds", "Improvements page", "25–40 items with ROI estimates"],
        ["Future State Designer", "60–90 seconds", "Future State page", "3 scenarios (A/B/C) with metrics"],
        ["Business Case Builder", "45–60 seconds", "Business Case page", "3 scenarios with payback period"],
        ["Playbook Contextualizer", "30–45 seconds", "Implementation Playbook page", "3 playbooks with 8 phases each"],
    ], col_widths=[2.0, 1.8, 2.2, 2.8])

h2(d,"Troubleshooting Common Issues")
tbl(d, ["Issue", "Symptom", "Fix"],
    [
        ["VSM shows zero lead time", "All LT values = 0", "Check ALM CSV date format (YYYY-MM-DD required)"],
        ["DORA agent fails", "Status = failed", "Check API token scope — needs read access to all 4 sources"],
        ["Bottleneck count < 3", "Only 1–2 bottlenecks", "Check ticket count — needs ≥500 tickets; add more sprints"],
        ["Business case ROI < 1×", "ROI shows 0.8×", "Check DORA scores — manual override if scores too low"],
        ["Pipeline stalls at agent 4", "Running status for >10min", "Restart backend; check logs: uvicorn output in terminal"],
    ], col_widths=[2.2, 2.2, 4.0])

h1(d,"Week 5–6: Validation and Calibration")
h2(d,"Client Review Session Agenda (60 min)")
tbl(d, ["Time", "Activity", "Facilitator"],
    [
        ["0:00–0:10", "VSM review: confirm lead times are representative", "Client engineer + Pilot Lead"],
        ["0:10–0:25", "Bottleneck walkthrough: are these the known pain points?", "Client team lead + Pilot Lead"],
        ["0:25–0:40", "Improvement scoring: adjust priorities and effort estimates", "Client team lead"],
        ["0:40–0:55", "Business case scenario selection for executive readout", "Sponsor + Pilot Lead"],
        ["0:55–1:00", "Actions: overrides to apply, final readout prep", "Pilot Lead"],
    ], col_widths=[1.2, 4.0, 3.2])

h1(d,"Week 7–8: Readout Preparation and Delivery")
for item in [
    "Export executive deck: Platform > Business Case > Export PPT (15-slide deck generated automatically)",
    "Apply client branding: update logo placeholder on slides 1, 2, 18 — do not change font or layout",
    "Brief sponsor: 30-min pre-read session — confirm CFO message and scenario selection",
    "Rehearse: full 15-minute run-through with Delivery Analyst playing devil's advocate",
    "Deliver readout: screen-share from laptop; have backup screenshots on second screen",
    "Capture actions: note all follow-up questions and add to action plan in platform",
    "Send post-readout summary: email within 24 hours — deck attached, next steps listed",
    "Complete knowledge transfer: 60-min session with platform administrator",
]:
    num(d, item)

d.save(os.path.join(OUT,"13-pilot-delivery-runbook.docx"))
print("  ✓ Saved: 13-pilot-delivery-runbook.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 14 — RACI Matrix
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 14-raci-matrix.docx...")
d = new_doc()
cover_page(d,"RACI Matrix","Roles, Accountability, and Consultation Framework for Pilot Delivery","DOC-SET2-14")
h1(d,"RACI Key")
tbl(d, ["Code", "Meaning", "Obligation"],
    [
        ["R", "Responsible", "Does the work; completes the task"],
        ["A", "Accountable", "Owns the outcome; final decision authority"],
        ["C", "Consulted", "Input required before work proceeds"],
        ["I", "Informed", "Notified when work is complete or decisions made"],
        ["-", "Not Involved", "No role in this activity"],
    ], col_widths=[1.0, 1.8, 5.5])

h1(d,"RACI by Activity")
tbl(d, ["Activity", "Pilot Lead", "Delivery Analyst", "Client PM", "Client IT", "Eng SME", "Sponsor"],
    [
        ["Contract & SOW sign-off", "C", "I", "C", "I", "I", "A/R"],
        ["Kick-off meeting facilitation", "A/R", "C", "I", "I", "I", "I"],
        ["ALM data export", "C", "I", "A", "R", "C", "I"],
        ["Platform deployment", "A/R", "C", "I", "R", "I", "I"],
        ["DORA source configuration", "A/R", "C", "I", "C", "C", "I"],
        ["AI pipeline execution", "A/R", "C", "I", "I", "I", "I"],
        ["VSM accuracy validation", "C", "I", "A", "I", "R", "I"],
        ["Bottleneck review", "C", "I", "A", "I", "R", "I"],
        ["Business case scenario selection", "C", "I", "C", "I", "I", "A/R"],
        ["Executive deck preparation", "A/R", "R", "C", "I", "I", "C"],
        ["Executive readout delivery", "A/R", "C", "C", "I", "I", "I"],
        ["Action plan setup in platform", "A/R", "R", "C", "I", "I", "I"],
        ["Knowledge transfer session", "A/R", "R", "C", "R", "C", "I"],
        ["Post-pilot support", "A/R", "R", "I", "C", "I", "I"],
        ["Scale licence commercial discussion", "C", "I", "A/R", "I", "I", "C"],
    ],
    col_widths=[2.8, 0.9, 1.1, 0.9, 0.9, 0.9, 0.9])

h1(d,"Escalation Path")
tbl(d, ["Issue Type", "First Contact", "Escalation 1", "Escalation 2", "SLA"],
    [
        ["Technical (platform)", "Pilot Lead", "Delivery Practice Lead", "CTO", "4h response / 24h resolution"],
        ["Data quality", "Client IT", "Client PM", "Sponsor", "48h for data remediation"],
        ["Scope change request", "Client PM", "Pilot Lead", "Sponsor + Partner", "5 business days"],
        ["Commercial dispute", "Client PM", "Pilot Lead", "Accounts + Legal", "10 business days"],
        ["Critical blocker", "Pilot Lead", "Sponsor (both sides)", "CEO / CTO", "Same-day escalation"],
    ], col_widths=[2.0, 1.8, 1.8, 1.8, 2.0])

d.save(os.path.join(OUT,"14-raci-matrix.docx"))
print("  ✓ Saved: 14-raci-matrix.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 15 — Pilot Findings Readout Deck (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 15-pilot-findings-readout.pptx...")
prs = new_prs()

# Slide 1: Cover
sl = blank(prs)
rect(sl, 0, 0, 13.33, 7.5, fill=DARK_BLUE)
rect(sl, 0, 4.5, 13.33, 3.0, fill=MED_BLUE)
txtbox(sl, "[CLIENT NAME]", 1.0, 0.6, 11, 0.5, size=16, color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl, "AI-Powered PDLC Value Stream Analysis", 1.0, 1.2, 11, 0.8, size=28, bold=True, color=WHITE)
txtbox(sl, "Pilot Engagement — Executive Readout", 1.0, 2.1, 11, 0.6, size=18, color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl, "[DATE]  |  Confidential", 1.0, 5.0, 11, 0.5, size=14, color=WHITE)
txtbox(sl, "PDLC VSM Platform  |  Powered by LangGraph + Claude", 1.0, 5.6, 11, 0.4, size=11, color=RGBColor(0xBF,0xDB,0xFE))

# Slide 2: Executive Summary
sl = blank(prs)
header_bar(sl, "Executive Summary", "8-Week Pilot: What We Found and What It Means")
for i, (stat, label) in enumerate([
    ("[XX] days","Current Lead Time"),("17–22%","Flow Efficiency"),("5","Bottlenecks Found"),("$[X]M/yr","Savings Identified")
]):
    stat_box(sl, 0.5 + i*3.2, 1.3, 2.8, 1.5, stat, label)
for i, finding in enumerate([
    "Phase 5 (Testing) accounts for [XX]% of total queue time — manual SIT/UAT is the #1 blocker",
    "Architecture review gate adds [XX] hours per feature — a 3-day invisible delay per sprint",
    "DORA band: WALK (2.1/5.0) — deployment frequency and MTTR both below sector average",
    "Peer benchmark gap: [COMPETITOR] achieves [X]× better flow efficiency on same tech stack",
    "Conservative scenario: $[X]M investment, [X]× ROI, [XX]-month payback — board-approvable"
]):
    txtbox(sl, f"{i+1}. {finding}", 0.4, 3.0+i*0.72, 12.5, 0.65, size=11, color=DARK_TEXT)

# Slide 3: Current State VSM
sl = blank(prs)
header_bar(sl, "Current State Value Stream Map", "[TEAM NAME] — [X]-Day Lead Time Baseline")
phases = ["Requirements","Design & Architecture","Development","Code Review & Merge","Continuous Testing","Deployment Prep","Release & Ops"]
for i, ph in enumerate(phases):
    x = 0.3 + i * 1.85
    col = RGBColor(0xEF,0x44,0x44) if i in [4,5] else MED_BLUE if i in [0,2] else DARK_BLUE
    rect(sl, x, 1.2, 1.7, 0.6, fill=col)
    txtbox(sl, ph, x, 1.2, 1.7, 0.6, size=7.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, f"PT: [X]h\nWT: [X]h\nFE: [X]%", x, 1.85, 1.7, 0.8, size=8, color=DARK_TEXT)
rect(sl, 0.3, 2.85, 12.7, 0.05, fill=DARK_BLUE)
txtbox(sl, "→ TOTAL LEAD TIME: [XX] DAYS  |  FLOW EFFICIENCY: [X]%  |  PROCESS TIME: [X]h  |  WAIT TIME: [X]h", 0.3, 3.0, 12.7, 0.5, size=10, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
txtbox(sl, "■ Phases in RED = Flow Efficiency < 15% (critical waste zones — immediate focus required)", 0.5, 3.65, 12.3, 0.4, size=9, color=RGBColor(0xEF,0x44,0x44))
txtbox(sl, "Source: [X,XXX] Jira tickets from [X] sprints ([MONTH YEAR]–[MONTH YEAR])  |  AI-validated by VSM Analyzer agent", 0.5, 4.15, 12.3, 0.4, size=9, color=DARK_TEXT, italic=True)

# Slide 4: DORA Assessment
sl = blank(prs)
header_bar(sl, "DORA Maturity Assessment", "73-Question Gap Analysis — [TEAM NAME]")
dims = ["Continuous\nIntegration","Continuous\nDeployment","Continuous\nTesting","Culture &\nProcess"]
scores = ["[X.X]/5.0","[X.X]/5.0","[X.X]/5.0","[X.X]/5.0"]
bands = ["WALK","WALK","CRAWL","WALK"]
cols = [MED_BLUE, DARK_BLUE, RGBColor(0xEF,0x44,0x44), MED_BLUE]
for i, (dim, sc, band, col) in enumerate(zip(dims, scores, bands, cols)):
    x = 0.5 + i * 3.1
    rect(sl, x, 1.2, 2.7, 2.0, fill=col)
    txtbox(sl, dim, x, 1.2, 2.7, 0.6, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, sc, x, 1.8, 2.7, 0.7, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, f"Band: {band}", x, 2.55, 2.7, 0.5, size=11, color=WHITE, align=PP_ALIGN.CENTER)
txtbox(sl, "Overall DORA Band: WALK  |  Overall Score: [X.X] / 5.0  |  Sector Average: 2.8 / 5.0", 0.5, 3.4, 12.3, 0.5, size=12, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
for item in ["Top gap: Automated testing coverage [X]% vs sector target 75%","Second gap: Deployment frequency [bi-weekly] vs sector leader [daily]","Third gap: MTTR [X] hours vs sector leader [2 hours]"]:
    txtbox(sl, f"• {item}", 0.5, 4.05 + ["Top","Second","Third"].index(item.split()[0].rstrip(':')) * 0.45, 12.3, 0.4, size=10, color=DARK_TEXT)

# Slide 5: Top 5 Bottlenecks
sl = blank(prs)
header_bar(sl, "Top 5 Bottlenecks Identified", "Ranked by Annual Waste Hours — Root Cause + Benchmark Gap")
bottlenecks = [
    ("[Bottleneck 1]", "Critical", "[Phase X]", "[XXX]h/feature", "[$X.XM/yr]"),
    ("[Bottleneck 2]", "Critical", "[Phase X]", "[XXX]h/feature", "[$X.XM/yr]"),
    ("[Bottleneck 3]", "High", "[Phase X]", "[XX]h/feature", "[$X.XM/yr]"),
    ("[Bottleneck 4]", "High", "[Phase X]", "[XX]h/feature", "[$XXXk/yr]"),
    ("[Bottleneck 5]", "Medium", "[Phase X]", "[XX]h/feature", "[$XXXk/yr]"),
]
for i, (name, sev, phase, waste, cost) in enumerate(bottlenecks):
    y = 1.2 + i * 1.1
    col = RGBColor(0xEF,0x44,0x44) if sev=="Critical" else RGBColor(0xF9,0x73,0x16) if sev=="High" else MED_BLUE
    rect(sl, 0.3, y, 0.1, 0.8, fill=col)
    txtbox(sl, name, 0.5, y+0.05, 4.5, 0.7, size=11, bold=True, color=DARK_TEXT)
    txtbox(sl, f"Phase: {phase}", 5.2, y+0.05, 2.0, 0.35, size=9, color=DARK_TEXT)
    txtbox(sl, f"Waste: {waste}", 5.2, y+0.4, 2.0, 0.35, size=9, color=DARK_TEXT)
    txtbox(sl, f"{sev}", 7.3, y+0.1, 1.2, 0.55, size=10, bold=True, color=col, align=PP_ALIGN.CENTER)
    txtbox(sl, cost, 8.7, y+0.1, 1.8, 0.55, size=12, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
    txtbox(sl, "Annual Savings Potential", 10.6, y+0.1, 2.4, 0.55, size=8, color=DARK_TEXT)

# Slide 6: Improvement Roadmap
sl = blank(prs)
header_bar(sl, "AI Improvement Roadmap", "[XX] Initiatives Across 3 Horizons — Ranked by ROI")
for x, title, count, roi, col in [
    (0.3, "Quick Wins\n0–90 Days", "[X] initiatives", "Avg ROI: [X.X]×", MED_BLUE),
    (4.6, "Medium-Term\n3–6 Months", "[X] initiatives", "Avg ROI: [X.X]×", DARK_BLUE),
    (8.9, "Strategic\n6–12 Months", "[X] initiatives", "Avg ROI: [X.X]×", ACCENT),
]:
    rect(sl, x, 1.2, 4.0, 4.8, fill=col)
    txtbox(sl, title, x, 1.3, 4.0, 0.8, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, count, x, 2.1, 4.0, 0.5, size=12, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, roi, x, 2.7, 4.0, 0.5, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for j in range(3):
        txtbox(sl, f"• [Initiative {j+1}]", x+0.15, 3.3+j*0.6, 3.7, 0.5, size=10, color=WHITE)
txtbox(sl, "■ Total: [XX] initiatives  |  Combined potential: $[X.X]M–$[X.X]M annual savings  |  [XX]% Quick Win deliverable within 90 days", 0.3, 6.25, 12.7, 0.5, size=9, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)

# Slide 7: Business Case Scenarios
sl = blank(prs)
header_bar(sl, "Business Case — 3 Investment Scenarios", "Conservative / Expected / Optimistic — [SPONSOR NAME] Review")
scenarios = [
    ("Option A\nConservative", "$[X.X]M", "$[X.X]M/yr", "[X.X]×", "[XX] months", "[X]-year NPV: $[X.X]M"),
    ("Option B\nExpected ★", "$[X.X]M", "$[X.X]M/yr", "[X.X]×", "[XX] months", "[X]-year NPV: $[X.X]M"),
    ("Option C\nOptimistic", "$[X.X]M", "$[X.X]M/yr", "[X.X]×", "[XX] months", "[X]-year NPV: $[X.X]M"),
]
for i, (label, invest, benefit, roi, payback, npv) in enumerate(scenarios):
    x = 0.4 + i * 4.3
    col = MED_BLUE if i==1 else DARK_BLUE
    rect(sl, x, 1.1, 4.0, 5.5, fill=LIGHT_BLUE if i!=1 else RGBColor(0xDB,0xEA,0xFE))
    rect(sl, x, 1.1, 4.0, 0.7, fill=col)
    txtbox(sl, label, x, 1.1, 4.0, 0.7, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for j, (metric, val) in enumerate([("Investment", invest),("Annual Benefits", benefit),("ROI", roi),("Payback", payback),(npv.split(":")[0], npv.split(":")[1].strip())]):
        txtbox(sl, metric, x+0.2, 1.95+j*0.88, 1.8, 0.4, size=9, color=DARK_TEXT)
        txtbox(sl, val, x+2.0, 1.95+j*0.88, 1.7, 0.5, size=13, bold=True, color=col, align=PP_ALIGN.RIGHT)
if True:
    txtbox(sl, "★ Recommended: Option B delivers optimal risk-adjusted return aligned with sector peer performance", 0.4, 6.85, 12.5, 0.45, size=9, italic=True, color=DARK_BLUE)

# Slide 8: Recommended Next Steps
sl = blank(prs)
header_bar(sl, "Recommended Next Steps", "From Pilot to Transformation — 90-Day Action Plan")
steps = [
    ("1", "Week 1–2: Select preferred scenario (Option A/B/C) and obtain board / ELT approval for investment"),
    ("2", "Week 2–3: Assign transformation programme owner and stand up cross-functional pod (Eng + Product + DevOps)"),
    ("3", "Week 3–6: Begin Quick Wins implementation — 3 parallel workstreams, Pilot Lead as technical advisor"),
    ("4", "Week 4: Configure PDLC VSM Platform action plan tracker — all 30 items with owners and target dates"),
    ("5", "Week 6: First 30-day benefit review — platform auto-tracks LT and FE improvements vs. baseline"),
    ("6", "Week 8: Scale licence configuration — expand to second team / product group"),
    ("7", "Week 12: 90-day progress readout to ELT — platform generates updated VSM, bottleneck delta, ROI tracking"),
]
for item, text in steps:
    y = 1.2 + int(item) * 0.72
    rect(sl, 0.3, y, 0.55, 0.55, fill=MED_BLUE)
    txtbox(sl, item, 0.3, y, 0.55, 0.55, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, text, 1.0, y+0.05, 11.8, 0.5, size=10, color=DARK_TEXT)

prs.save(os.path.join(OUT,"15-pilot-findings-readout.pptx"))
print("  ✓ Saved: 15-pilot-findings-readout.pptx")


# ═══════════════════════════════════════════════════════════════════════════════
# 16 — Discovery Questionnaire
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 16-discovery-questionnaire.docx...")
d = new_doc()
cover_page(d,"Discovery Questionnaire","Pre-Pilot Discovery: Understanding Your Software Delivery Context","DOC-SET2-16")
body(d,"Instructions: Complete Sections 1–4 before the kick-off meeting. Section 5 is optional but highly recommended. Estimated time: 30–45 minutes. Return to Pilot Lead at least 2 business days before kick-off.")
divider(d)

sections = [
    ("Organisation and Team Context", [
        ("Organisation name", "Full legal name or trading name"),
        ("Industry sector", "e.g., Financial Services, Healthcare, Retail, Government"),
        ("Number of employees (engineering org)", "e.g., 50, 200, 2,000"),
        ("Team name", "The team participating in the pilot"),
        ("Number of engineers in pilot team", "Including QA, DevOps, and data engineers"),
        ("Product/system being measured", "Brief description of the product or platform"),
        ("Product criticality", "e.g., Revenue-generating, Internal tooling, Customer-facing, Regulatory"),
        ("Executive sponsor name and title", "The senior leader sponsoring this engagement"),
    ]),
    ("ALM and Data", [
        ("ALM system", "Jira Cloud / Jira Server / Azure DevOps / Other (specify)"),
        ("Jira/ADO URL", "e.g., https://yourcompany.atlassian.net"),
        ("Project key(s)", "e.g., PAYMENT, LENDING, PLATFORM"),
        ("Date range available", "How many months of historical data? e.g., 18 months"),
        ("Approximate ticket count", "Total issues in the date range for this team"),
        ("Ticket types in use", "e.g., Story, Bug, Task, Epic, Sub-task — which are meaningful?"),
        ("Sprint cadence", "e.g., 2-week sprints, Kanban, 3-week sprints"),
        ("Story points used?", "Yes / No — if yes, are they consistently estimated?"),
        ("Known data quality issues", "Missing resolved dates? Inconsistent statuses? Unresolved old tickets?"),
    ]),
    ("DORA Sources", [
        ("Confluence / Wiki URL", "For change advisory board records, runbooks, deployment guides"),
        ("SonarQube URL", "Code quality and coverage reporting"),
        ("GitHub repository URL", "Primary codebase — for PR cycle time and deployment frequency"),
        ("Additional sources", "Any other tooling: Jenkins, ArgoCD, Datadog, PagerDuty, etc."),
        ("Recent deployment frequency", "How often do you deploy to production? Daily / Weekly / Bi-weekly / Monthly"),
        ("Recent MTTR", "Average time to restore service after an incident (hours)"),
        ("Recent change failure rate", "% of changes that cause a production incident or rollback"),
    ]),
    ("Known Pain Points (Self-Reported)", [
        ("Top 3 delivery bottlenecks you already know about", "Based on your experience — what slows you down most?"),
        ("Longest phase in your delivery cycle", "Which phase takes the most calendar time? Why?"),
        ("Most common reason for sprint scope changes", "e.g., late requirements, tech debt, test failures"),
        ("Recent incident that delayed a release", "Describe briefly — what type of issue caused it?"),
        ("What does 'done' look like for a feature?", "e.g., Deployed to prod, passed UAT, signed off by product owner"),
        ("What would make the biggest difference to your team's velocity?", "One sentence — your view before AI analysis"),
    ]),
    ("Executive Stakeholders (Optional)", [
        ("CFO name and reporting line", "Who will review the business case?"),
        ("CTO name and reporting line", "Who will approve the technology strategy?"),
        ("Board reporting cadence", "How often does engineering performance get reported to the board?"),
        ("Existing improvement programmes", "Any active DevOps, Agile, or cloud transformation programmes?"),
        ("Budget approval threshold", "What investment level requires board approval vs. ELT approval?"),
    ]),
]
for sec_title, questions in sections:
    h1(d, sec_title)
    for i, (q, hint) in enumerate(questions):
        h3(d, f"{i+1}. {q}")
        body(d, f"Guidance: {hint}", italic=True, color=DBLUE)
        body(d, "Answer: ___________________________________________________________________________")
        body(d, "")
    divider(d)

d.save(os.path.join(OUT,"16-discovery-questionnaire.docx"))
print("  ✓ Saved: 16-discovery-questionnaire.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 17 — Kick-off Meeting Guide
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 17-kickoff-meeting-guide.docx...")
d = new_doc()
cover_page(d,"Kick-off Meeting Guide","Facilitator's Guide for the 90-Minute Pilot Kick-off Meeting","DOC-SET2-17")
h1(d,"Meeting Purpose")
body(d,"The kick-off meeting sets the foundation for a successful pilot. It aligns all stakeholders on objectives, establishes trust through a live platform demonstration, resolves data access questions, and confirms the 8-week delivery plan. A well-run kick-off prevents 80% of mid-pilot issues.")
tbl(d, ["Attribute", "Value"],
    [
        ["Duration", "90 minutes (can be compressed to 60 min for senior audiences)"],
        ["Format", "In-person or video call — screen-share required for platform demo"],
        ["Attendees", "Sponsor, Client PM, Platform Admin (IT), Engineering SME (1–2), Pilot Lead, Delivery Analyst"],
        ["Pre-reads", "Pilot Proposal, Project Charter, Discovery Questionnaire responses"],
        ["Materials needed", "Laptop with platform running, printed charter, slide deck (optional)"],
    ], col_widths=[2.5, 6.0])

h1(d,"Detailed Agenda")
agenda = [
    ("0:00–0:05", "Welcome and Housekeeping", "Pilot Lead",
     "Welcome, introductions (name + role), confirm 90 min, parking lot for off-topic items."),
    ("0:05–0:15", "Pilot Objectives and Success Criteria", "Pilot Lead",
     'Walk through the 4 objectives from the charter. Ask: "Is there anything critical we\'ve missed?" Capture additions to scope in the parking lot. Confirm the savings guarantee.'),
    ("0:15–0:35", "Platform Live Demonstration", "Pilot Lead",
     "Run the 5-screen demo: ALM Connect → Current State VSM → DORA Assessment → Bottlenecks → Business Case. Use US Bank / Team Phoenix pre-loaded data. Pause after each screen for questions. Do NOT let this run over 20 minutes."),
    ("0:35–0:50", "Data Requirements Review", "Pilot Lead + Client IT",
     "Walk through the ALM export checklist field-by-field. Confirm: Jira/ADO access, API token scope, date range. Review discovery questionnaire responses. Flag any data quality risks. Set delivery date for first data extract."),
    ("0:50–1:05", "DORA Source Configuration", "Pilot Lead + Eng SME",
     "Review the 4 DORA sources. Confirm URLs, token types, and access levels. Client IT sets up read-only service accounts during Week 1. Target: all 4 sources green by end of Week 2."),
    ("1:05–1:15", "8-Week Timeline Walk-through", "Pilot Lead",
     "Present the Gantt chart (Week 1–8). Confirm key dates: data extract, phase reviews, executive readout. Add client PTO or blackout dates. Confirm meeting cadence (weekly 30-min status check)."),
    ("1:15–1:25", "Governance and Escalation", "Pilot Lead",
     "Review RACI matrix highlights. Confirm the escalation path. Agree on communication channel (email or Teams/Slack). Confirm change control process."),
    ("1:25–1:30", "Parking Lot and Actions", "Pilot Lead",
     "Review parking lot items — assign owners and due dates. Capture in action log. Send within 24 hours of meeting."),
]
for time, title, owner, detail in agenda:
    h2(d, f"{time} — {title}")
    body(d, f"Owner: {owner}", italic=True, color=DBLUE)
    body(d, detail)

h1(d,"Post-Meeting Actions (Pilot Lead — within 24 hours)")
for item in [
    "Send meeting notes with action log (names, owners, due dates)",
    "Upload Project Charter to shared folder / SharePoint",
    "Schedule all 8 weekly status calls",
    "Send data extract template to client IT (CSV format with 12 required fields)",
    "Send DORA source configuration guide (with screenshots)",
    "Create project channel in Teams / Slack",
    "Confirm first data extract date in writing",
]:
    bul(d, item)

h1(d,"Common Kick-off Issues and Responses")
tbl(d, ["Issue", "Response"],
    [
        ["'We can't export Jira data — IT policy'", "Offer on-prem deployment + data anonymisation script. Escalate to sponsor if blocked."],
        ["'Our data quality is poor — lots of missing resolved dates'", "2-week data remediation window in scope. Use heuristic LT for tickets missing dates."],
        ["'Can we include 3 teams, not 1?'", "Scope creep — park it. Multi-team is Scale Pack scope. Note for upsell."],
        ["'We already know what the bottlenecks are'", "AI quantification + financial impact is the value. Say: 'Let's see if the data agrees with you — and put a dollar figure on it.'"],
        ["'Is the AI accurate?'", "Show validation step (Week 5-6 manual override). Platform shows confidence intervals."],
        ["'Who else has done this?'", "Reference US Bank case study — 42-day → 8-day LT, 4.2× ROI. Offer reference call."],
    ], col_widths=[3.0, 6.5])

d.save(os.path.join(OUT,"17-kickoff-meeting-guide.docx"))
print("  ✓ Saved: 17-kickoff-meeting-guide.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 18 — AI Evidence Protocol
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 18-ai-evidence-protocol.docx...")
d = new_doc()
cover_page(d,"AI Evidence Protocol","Standards for Validating, Citing, and Auditing AI Agent Outputs","DOC-SET2-18")
h1(d,"Purpose")
body(d,"This protocol establishes the standards for validating, citing, and auditing all outputs produced by PDLC VSM Platform AI agents. It ensures that findings presented to executive stakeholders are defensible, traceable to source data, and appropriately caveated where AI confidence is lower.")
callout(d,"Principle: Every material finding must be traceable to either (a) the client's own ALM data, (b) a published industry benchmark, or (c) a peer-validated AI inference with confidence score ≥ 0.7.")

h1(d,"Evidence Classification")
tbl(d, ["Class", "Label", "Definition", "Requires"],
    [
        ["Class 1", "Data-Derived", "Directly computed from client ALM data with no AI inference", "Source ticket count, date range"],
        ["Class 2", "AI-Inferred", "AI agent output with high confidence (≥0.8)", "Confidence score, source agent"],
        ["Class 3", "Benchmark-Grounded", "Comparison to published or platform benchmark database", "Benchmark source, date"],
        ["Class 4", "Heuristic Estimate", "AI estimate where data is sparse or ambiguous (confidence <0.8)", "Caveated disclosure in readout"],
    ], col_widths=[1.0, 1.8, 3.7, 3.0])

h1(d,"Agent Output Standards")
for agent, outputs, class_label, validation in [
    ("VSM Analyzer", "Lead time, flow efficiency, process time, wait time per phase",
     "Class 1 (data-derived)", "Verify total LT within ±10% of manual ticket audit on 20 random samples"),
    ("Benchmark Agent", "Peer comparisons, sector averages, competitor metrics",
     "Class 3 (benchmark-grounded)", "Benchmark database updated quarterly; sources cited in tooltip"),
    ("Bottleneck Analyzer", "Bottleneck severity scores, root cause labels, waste hours",
     "Class 2 (AI-inferred)", "Client engineering SME reviews and validates before readout"),
    ("Improvement Generator", "ROI estimates, effort estimates, initiative titles",
     "Class 2/3 (AI-inferred + benchmarks)", "ROI band (not point estimate) cited; assumes sector average implementation cost"),
    ("Future State Designer", "Target LT, FE, WT for each scenario",
     "Class 2/3", "Projected metrics show conservative/expected/optimistic bands"),
    ("Business Case Builder", "NPV, payback period, benefit breakdown",
     "Class 2/3 + Class 1 for baseline", "CFO review uses expected scenario only; conservative shown for risk adjustment"),
    ("DORA Assessment Agent", "Maturity scores, band assignment, gap analysis",
     "Class 1/2 (data + AI)", "73 questions; manual override available for any score"),
]:
    h2(d, agent)
    tbl(d, ["Attribute", "Value"],
        [["Outputs", outputs], ["Evidence Class", class_label], ["Validation Method", validation]],
        col_widths=[2.0, 6.5])

h1(d,"Citation Standards for Executive Readouts")
h2(d,"What Must Be Cited")
for item in [
    "Any statistic presented to CFO, CEO, or Board: class, source, and confidence level",
    "All benchmark comparisons: name of benchmark database or published report, year",
    "All ROI / NPV / payback figures: assumptions stated in footnote or slide notes",
    "All peer comparisons: anonymised if confidential, or cited if from public report",
]:
    bul(d, item)

h2(d,"Citation Format (Slide Footnote)")
callout(d,'Example: "Lead time: 42 days [Class 1 — 2,847 Jira tickets, Jan 2024–Dec 2024]. Bottleneck: Manual SIT/UAT [Class 2 — Bottleneck Analyzer, confidence: 0.87]. Benchmark: Sector avg 28 days [Class 3 — DORA State of DevOps 2024]."')

h1(d,"Audit Trail")
body(d,"Every AI analysis run generates an audit log stored in the platform database. The log includes:")
for item in [
    "Run ID (UUID) — unique identifier for the analysis run",
    "Timestamp — UTC timestamp of agent execution",
    "Input data hash — SHA-256 of the ALM data file used",
    "Agent outputs — full JSON output for each agent (stored in AnalysisRun table)",
    "Manual overrides — timestamped record of any client-modified scores",
    "Confidence scores — per-agent confidence metadata",
]:
    bul(d, item)
body(d,"Audit logs are retained for 12 months and can be exported from the platform as a PDF audit pack.")

h1(d,"Disclosure Requirements")
callout(d,"Mandatory Disclosure: All outputs must include the following statement when presented to external stakeholders: 'Analysis produced by AI agents using client-provided ALM data and published industry benchmarks. All material findings have been validated by the client engineering team. Point estimates represent expected-case scenarios; conservative and optimistic ranges available in the platform.'")

d.save(os.path.join(OUT,"18-ai-evidence-protocol.docx"))
print("  ✓ Saved: 18-ai-evidence-protocol.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 19 — Risk Register
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 19-risk-register.docx...")
d = new_doc()
cover_page(d,"Risk Register","Pilot Engagement Risk Identification and Mitigation Plan","DOC-SET2-19")
h1(d,"Risk Rating Scale")
tbl(d, ["Rating", "Likelihood", "Impact", "Response Required"],
    [
        ["Critical (16–25)", "Very Likely (5) × Major Impact (4–5)", "5 = >$1M impact or engagement failure", "Immediate escalation + contingency plan"],
        ["High (9–15)", "Likely (4) × Significant (3–4)", "4 = Significant delay or scope reduction", "Weekly monitoring + mitigation action"],
        ["Medium (5–8)", "Possible (3) × Moderate (2–3)", "3 = Minor delay, manageable", "Fortnightly review"],
        ["Low (1–4)", "Unlikely (1–2) × Minor (1–2)", "1–2 = Negligible impact", "Monitor only"],
    ], col_widths=[2.0, 2.5, 2.5, 2.5])

h1(d,"Risk Register")
tbl(d, ["ID", "Risk Description", "Category", "L", "I", "Rating", "Mitigation", "Owner", "Status"],
    [
        ["R01", "ALM data export blocked by IT security policy or data governance", "Data", "3", "5", "High", "Pre-engage IT lead; offer on-prem option; data NDA", "Client PM", "Open"],
        ["R02", "Data quality too poor for meaningful VSM (>40% missing resolved dates)", "Data", "3", "4", "High", "Data quality scorecard Week 1; heuristic LT for sparse data", "Pilot Lead", "Open"],
        ["R03", "Key client stakeholder unavailable during critical phases", "Resource", "3", "3", "Medium", "Async review via platform; recorded demo as fallback", "Client PM", "Open"],
        ["R04", "Platform performance degrades with large ticket volumes (>50K)", "Technical", "2", "4", "Medium", "Load test before engagement; horizontal scaling available", "Pilot Lead", "Open"],
        ["R05", "AI agent produces inaccurate bottleneck scores (false negatives)", "AI", "2", "3", "Medium", "Manual override in Week 5-6; client SME validation step", "Pilot Lead", "Open"],
        ["R06", "Executive readout postponed or cancelled", "Commercial", "2", "4", "Medium", "30-day post-pilot support covers rescheduling; async deck delivery", "Client PM", "Open"],
        ["R07", "Competitor platform already in use; findings challenged", "Commercial", "2", "3", "Medium", "Evidence protocol citations; offer parallel run comparison", "Pilot Lead", "Open"],
        ["R08", "OpenAI/Claude API outage during agent execution", "Technical", "1", "3", "Low", "Retry logic built into agents; 48h window for re-run", "Pilot Lead", "Open"],
        ["R09", "Scope creep: client requests additional teams / data sources", "Scope", "4", "2", "Medium", "RACI + change control process; park additional scope for Scale Pack", "Pilot Lead", "Open"],
        ["R10", "Business case rejected by CFO — ROI not credible", "Commercial", "2", "5", "High", "Evidence protocol citations; show conservative scenario; offer reference call", "Sponsor", "Open"],
        ["R11", "Data privacy or GDPR concern raised mid-engagement", "Legal", "2", "4", "Medium", "Anonymisation scripts; on-prem option; DPA in contract", "Client PM", "Open"],
        ["R12", "Savings guarantee triggered — refund required", "Commercial", "1", "5", "Medium", "Pre-qualification in discovery; requires >3 critical bottlenecks to proceed", "Pilot Lead", "Open"],
    ],
    col_widths=[0.5, 2.8, 1.0, 0.3, 0.3, 0.7, 2.5, 1.0, 0.6])

h1(d,"Risk Review Schedule")
tbl(d, ["Week", "Activity", "Owner"],
    [
        ["Week 1", "Initial risk register review with Client PM at kick-off", "Pilot Lead"],
        ["Weekly", "Risk status update in weekly status call", "Pilot Lead"],
        ["Week 4", "Mid-point risk review — update ratings after AI run", "Pilot Lead + Client PM"],
        ["Week 7", "Pre-readout risk review — flag any unresolved risks", "Pilot Lead + Sponsor"],
        ["Week 8", "Closeout risk review — confirm all risks closed or handed over", "Pilot Lead"],
    ], col_widths=[1.2, 5.0, 2.3])

d.save(os.path.join(OUT,"19-risk-register.docx"))
print("  ✓ Saved: 19-risk-register.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 20 — Pilot Success Scorecard
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 20-pilot-success-scorecard.docx...")
d = new_doc()
cover_page(d,"Pilot Success Scorecard","Measuring and Demonstrating Pilot Value — Gate Criteria for Scale Recommendation","DOC-SET2-20")
h1(d,"Purpose")
body(d,"The Pilot Success Scorecard provides an objective, data-driven mechanism to measure the value delivered during the 8-week pilot. It is completed jointly by the Pilot Lead and Client PM at the end of Week 8 and serves as the primary input to the scale recommendation decision.")

h1(d,"Scorecard Dimensions")
h2(d,"Dimension 1: Technical Delivery (25 points)")
tbl(d, ["Criterion", "Max Points", "Scoring Guide", "Score Achieved"],
    [
        ["ALM data loaded and validated", "5", "5=100% tickets loaded; 3=≥80%; 1=<80%", ""],
        ["All 8 agents executed successfully", "5", "5=all 8 green; 3=6–7; 1=<6", ""],
        ["VSM accuracy validated by client", "5", "5=within ±5%; 3=within ±10%; 1=>±10%", ""],
        ["DORA sources all connected", "5", "5=all 4; 3=3 sources; 1=<3", ""],
        ["Platform uptime during engagement", "5", "5=100%; 3=≥99%; 1=<99%", ""],
    ], col_widths=[3.0, 1.2, 3.5, 1.5])

h2(d,"Dimension 2: Analysis Quality (25 points)")
tbl(d, ["Criterion", "Max Points", "Scoring Guide", "Score Achieved"],
    [
        ["Bottlenecks identified (≥3)", "5", "5=≥5 bottlenecks; 3=3–4; 1=<3", ""],
        ["Savings opportunity identified (≥$500K)", "5", "5=≥$1M; 3=$500K–$1M; 1=<$500K", ""],
        ["Client SME validates top 3 bottlenecks", "5", "5=all 3 validated; 3=2 of 3; 1=1 or 0", ""],
        ["Business case CFO-ready (sponsor rating)", "5", "5=4–5/5; 3=3/5; 1=≤2/5", ""],
        ["Improvement roadmap completeness", "5", "5=≥25 items; 3=15–24; 1=<15", ""],
    ], col_widths=[3.0, 1.2, 3.5, 1.5])

h2(d,"Dimension 3: Commercial Value (25 points)")
tbl(d, ["Criterion", "Max Points", "Scoring Guide", "Score Achieved"],
    [
        ["ROI multiple (expected scenario)", "5", "5=≥4×; 3=2–4×; 1=<2×", ""],
        ["Payback period", "5", "5=≤12 months; 3=12–18 months; 1=>18 months", ""],
        ["Executive sponsor NPS (0–10)", "5", "5=9–10; 3=7–8; 1=≤6", ""],
        ["Scale discussion initiated", "5", "5=licence agreed; 3=discussion in progress; 1=no discussion", ""],
        ["Reference willingness (client)", "5", "5=case study agreed; 3=reference call agreed; 1=declined", ""],
    ], col_widths=[3.0, 1.2, 3.5, 1.5])

h2(d,"Dimension 4: Knowledge Transfer (25 points)")
tbl(d, ["Criterion", "Max Points", "Scoring Guide", "Score Achieved"],
    [
        ["Platform admin trained and certified", "5", "5=certified; 3=trained, not certified; 1=not trained", ""],
        ["Action plan set up in platform", "5", "5=≥25 items with owners; 3=15–24; 1=<15", ""],
        ["Post-pilot support activated", "5", "5=all contacts set up; 3=partial; 1=not set up", ""],
        ["Client team confidence (self-reported, 1–5)", "5", "5=4–5/5; 3=3/5; 1=≤2/5", ""],
        ["Documentation handover complete", "5", "5=all docs in shared folder; 3=partial; 1=not done", ""],
    ], col_widths=[3.0, 1.2, 3.5, 1.5])

h1(d,"Summary Scorecard")
tbl(d, ["Dimension", "Max Score", "Score Achieved", "% of Max"],
    [
        ["Technical Delivery", "25", "", ""],
        ["Analysis Quality", "25", "", ""],
        ["Commercial Value", "25", "", ""],
        ["Knowledge Transfer", "25", "", ""],
        ["TOTAL", "100", "", ""],
    ], col_widths=[3.5, 1.5, 2.0, 2.0])

h1(d,"Scale Recommendation Gate")
tbl(d, ["Score", "Recommendation", "Next Step"],
    [
        ["85–100", "Scale — Strongly Recommended", "Present scale proposal within 1 week"],
        ["70–84", "Scale — Recommended with Conditions", "Address 1–2 gaps before scale proposal"],
        ["55–69", "Pilot Extension Recommended", "2-week extension to address gaps; re-score"],
        ["<55", "Savings Guarantee Review", "Invoke refund clause or negotiate remediation plan"],
    ], col_widths=[1.5, 3.0, 5.0])

body(d,"")
body(d,"Scorecard completed by: ___________________________   Date: _______________")
body(d,"Client PM signature: ___________________________   Date: _______________")
body(d,"Pilot Lead signature: ___________________________   Date: _______________")
d.save(os.path.join(OUT,"20-pilot-success-scorecard.docx"))
print("  ✓ Saved: 20-pilot-success-scorecard.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 21 — Pilot-to-Scale Framework
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 21-pilot-to-scale-framework.docx...")
d = new_doc()
cover_page(d,"Pilot-to-Scale Framework","From Single-Team Pilot to Enterprise-Wide Value Stream Intelligence","DOC-SET2-21")
h1(d,"Overview")
body(d,"The Pilot-to-Scale Framework defines the pathway from a single-team paid pilot to a full enterprise deployment of the PDLC VSM Platform. It is structured in three horizons, each building on the foundation of the previous, and is designed to maximise value capture while managing organisational change at an appropriate pace.")
callout(d,"Typical timeline: Pilot (8 weeks) → Scale Phase 1 (3 months) → Scale Phase 2 (6 months) → Enterprise (12 months). ROI scales non-linearly: each additional team added generates approximately 65% of the ROI of the first team due to shared infrastructure and institutional knowledge.")

h1(d,"Horizon Model")
tbl(d, ["Horizon", "Label", "Duration", "Scope", "Investment", "Typical ROI"],
    [
        ["H0", "Pilot", "8 weeks", "1 team, 1 product group", "$150K", "3–5× (annualised)"],
        ["H1", "Scale Phase 1", "3 months", "3–5 teams, 1 portfolio", "$300–500K", "4–6×"],
        ["H2", "Scale Phase 2", "6 months", "10–20 teams, 2–3 portfolios", "$800K–1.2M", "5–8×"],
        ["H3", "Enterprise", "12 months", "All teams, org-wide benchmarking", "$2–3M", "6–10×"],
    ], col_widths=[0.8, 1.5, 1.5, 2.5, 1.7, 1.5])

h1(d,"Scale Readiness Criteria")
h2(d,"Minimum Criteria to Proceed to Scale Phase 1")
for item in [
    "Pilot Success Scorecard total ≥ 70 points",
    "At least 1 senior stakeholder (CTO or VP Eng) has seen the executive readout",
    "At least 1 bottleneck remediation has been approved by the sponsor",
    "Platform administrator is certified and active",
    "Scale licence commercial terms agreed (or under negotiation)",
]:
    bul(d, item)

h2(d,"Recommended Criteria (accelerate timeline if met)")
for item in [
    "Pilot scorecard ≥ 85 points",
    "CFO has seen and endorsed the business case",
    "Second team lead has expressed interest (internal pull)",
    "Reference case study agreed for publication",
    "Quick Win implementation started within pilot window",
]:
    bul(d, item)

h1(d,"Scale Phase 1: Portfolio Expansion (3 Months)")
tbl(d, ["Month", "Activity", "Output"],
    [
        ["Month 1", "Onboard 2 additional teams (same product group)", "3 team VSM baselines"],
        ["Month 1", "Enable portfolio-level aggregation view", "Portfolio VSM dashboard"],
        ["Month 2", "Run DORA assessment for all 3 teams", "Portfolio DORA scorecard"],
        ["Month 2", "Comparative bottleneck analysis (team vs. portfolio)", "Cross-team insight report"],
        ["Month 3", "Portfolio business case (aggregate ROI)", "CFO presentation deck"],
        ["Month 3", "Quick Wins review: measure LT and FE improvement", "First ROI realisation report"],
    ], col_widths=[1.2, 3.8, 3.5])

h1(d,"Scale Phase 2: Enterprise Expansion (6 Months)")
tbl(d, ["Quarter", "Activity", "Output"],
    [
        ["Q1", "Onboard 5–10 additional teams across 2 portfolios", "Multi-portfolio VSM view"],
        ["Q1", "Centralised benchmark database: org benchmarks vs. sector", "Org benchmark report"],
        ["Q2", "AI-assisted transformation programme office", "PMO dashboard in platform"],
        ["Q2", "Integrate with ITSM (ServiceNow / Jira) for change tracking", "Automated improvement tracking"],
        ["Q2", "Executive dashboard: ELT-level flow efficiency KPIs", "ELT monthly briefing pack"],
        ["Q3", "Benefits realisation tracking vs. business case", "Benefits tracker (automated)"],
        ["Q3", "Competency uplift programme: platform certification for all leads", "Certified practitioner cohort"],
    ], col_widths=[1.2, 3.8, 3.5])

h1(d,"Value Scaling Model")
tbl(d, ["Teams", "Annualised Savings (Expected)", "Platform Investment", "Net Value", "ROI"],
    [
        ["1 (Pilot)", "$1.2–1.8M", "$150K", "$1.1–1.65M", "3–5×"],
        ["3 (Phase 1)", "$3.2–4.5M", "$400K", "$2.8–4.1M", "5–8×"],
        ["10 (Phase 2)", "$9–14M", "$900K", "$8.1–13.1M", "7–10×"],
        ["20+ (Enterprise)", "$18–30M", "$1.8M", "$16.2–28.2M", "8–12×"],
    ], col_widths=[1.5, 2.5, 2.0, 2.0, 1.5])
callout(d,"Note: Savings estimates based on sector benchmarks and US Bank pilot data. Actual savings vary by organisation size, current maturity, and implementation speed. All figures are expected-case; conservative scenario is approximately 65% of expected.")

d.save(os.path.join(OUT,"21-pilot-to-scale-framework.docx"))
print("  ✓ Saved: 21-pilot-to-scale-framework.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 22 — Scale Proposal Template (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 22-scale-proposal-deck.pptx...")
prs = new_prs()

# Slide 1: Cover
sl = blank(prs)
rect(sl, 0, 0, 13.33, 7.5, fill=DARK_BLUE)
rect(sl, 0, 5.0, 13.33, 2.5, fill=MED_BLUE)
txtbox(sl, "[CLIENT NAME]", 1.0, 0.5, 11, 0.5, size=16, color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl, "From Pilot to Enterprise:", 1.0, 1.1, 11, 0.6, size=18, color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl, "PDLC VSM Platform Scale Proposal", 1.0, 1.7, 11, 0.8, size=28, bold=True, color=WHITE)
txtbox(sl, "Building on [X]× ROI Delivered in Pilot — [X] Teams → [X] Teams in 12 Months", 1.0, 2.6, 11, 0.6, size=14, color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl, "[DATE]  |  Commercial Confidential", 1.0, 5.4, 11, 0.5, size=13, color=WHITE)

# Slide 2: Pilot Results Summary
sl = blank(prs)
header_bar(sl, "What the Pilot Delivered", "8-Week Results — Building the Case for Scale")
for i, (v, l) in enumerate([("[X.X]×","ROI Achieved"),("[X] days","Lead Time Reduction"),("$[X.X]M","Annual Savings Found"),("[X]/100","Pilot Score")]):
    stat_box(sl, 0.5+i*3.2, 1.3, 2.8, 1.5, v, l)
txtbox(sl, "Key Finding 1: [Top bottleneck] eliminated — [X]h waste per feature recovered", 0.5, 3.1, 12.3, 0.5, size=11, color=DARK_TEXT)
txtbox(sl, "Key Finding 2: DORA band improved from CRAWL → WALK on Continuous Testing dimension", 0.5, 3.7, 12.3, 0.5, size=11, color=DARK_TEXT)
txtbox(sl, "Key Finding 3: Business case validated by [SPONSOR NAME] — [X]× ROI approved for scale", 0.5, 4.3, 12.3, 0.5, size=11, color=DARK_TEXT)
txtbox(sl, "Sponsor Quote: '[Insert sponsor quote about pilot value]' — [Name], [Title]", 0.5, 5.1, 12.3, 0.6, size=11, italic=True, color=MED_BLUE)

# Slide 3: Scale Investment Summary
sl = blank(prs)
header_bar(sl, "Scale Investment — 3 Options", "Choosing the Right Scale Velocity for Your Organisation")
for i, (label, teams, invest, roi, timeline) in enumerate([
    ("Phase 1\nConservative", "3–5 teams\n1 portfolio", "$300–400K\nfirst year", "4–6× ROI", "3 months"),
    ("Phase 1+2\nRecommended ★", "10–15 teams\n2–3 portfolios", "$800K–1.0M\nover 9 months", "6–8× ROI", "9 months"),
    ("Enterprise\nFull Scale", "All teams\norg-wide", "$2–2.5M\nover 18 months", "8–12× ROI", "18 months"),
]):
    x = 0.4 + i*4.3
    col = MED_BLUE if i==1 else DARK_BLUE
    rect(sl, x, 1.1, 4.0, 5.5, fill=LIGHT_BLUE if i!=1 else RGBColor(0xDB,0xEA,0xFE))
    rect(sl, x, 1.1, 4.0, 0.65, fill=col)
    txtbox(sl, label, x, 1.1, 4.0, 0.65, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for j, (m, v) in enumerate([("Teams", teams),("Investment", invest),("Expected ROI", roi),("Timeline", timeline)]):
        txtbox(sl, m, x+0.15, 1.9+j*1.0, 1.5, 0.4, size=9, color=DARK_TEXT)
        txtbox(sl, v, x+1.7, 1.9+j*1.0, 2.1, 0.8, size=11, bold=True, color=col)

# Slide 4: 12-Month Roadmap
sl = blank(prs)
header_bar(sl, "12-Month Scale Roadmap", "Phased Implementation — Value at Every Quarter")
quarters = [("Q1","Months 1–3","Onboard 3–5 teams\nPortfolio VSM live\nFirst quick wins"),
            ("Q2","Months 4–6","DORA for all teams\nCross-team benchmarks\nROI realisation report"),
            ("Q3","Months 7–9","10–15 teams live\nELT dashboard\nTransformation PMO"),
            ("Q4","Months 10–12","Enterprise benchmark\nAnnual ROI review\nScale licence renewal")]
for i, (q, months, items) in enumerate(quarters):
    x = 0.4 + i*3.2
    rect(sl, x, 1.2, 3.0, 0.5, fill=DARK_BLUE)
    txtbox(sl, q, x, 1.2, 3.0, 0.5, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, months, x, 1.75, 3.0, 0.4, size=9, color=DARK_TEXT, align=PP_ALIGN.CENTER)
    rect(sl, x, 2.2, 3.0, 3.5, fill=LIGHT_BLUE)
    txtbox(sl, items, x+0.1, 2.3, 2.8, 3.2, size=10, color=DARK_TEXT, wrap=True)

# Slide 5: Next Steps
sl = blank(prs)
header_bar(sl, "Recommended Next Steps", "3 Actions in 3 Weeks to Activate Scale")
for i, (step, action, owner, date) in enumerate([
    ("1", "Select scale option (Phase 1 / 1+2 / Enterprise) and confirm budget envelope", "[SPONSOR]", "By [DATE]"),
    ("2", "Identify 2–4 additional teams for Phase 1 onboarding — team leads to join discovery call", "[CLIENT PM]", "By [DATE+1wk]"),
    ("3", "Schedule Scale Kick-off meeting — Pilot Lead to prepare onboarding pack for each team", "[PILOT LEAD]", "By [DATE+2wk]"),
]):
    y = 1.4 + i*1.6
    rect(sl, 0.4, y, 0.7, 0.7, fill=MED_BLUE)
    txtbox(sl, step, 0.4, y, 0.7, 0.7, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(sl, action, 1.3, y+0.05, 9.5, 0.6, size=12, bold=True, color=DARK_TEXT)
    txtbox(sl, f"Owner: {owner}  |  Target: {date}", 1.3, y+0.65, 9.5, 0.4, size=10, color=MED_BLUE)
txtbox(sl, "Contact: [PILOT LEAD]  |  [email]  |  PDLC VSM Platform — pdlc-vsm.io", 0.4, 6.7, 12.5, 0.5, size=11, color=DARK_TEXT, align=PP_ALIGN.CENTER)

prs.save(os.path.join(OUT,"22-scale-proposal-deck.pptx"))
print("  ✓ Saved: 22-scale-proposal-deck.pptx")


# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════
files = sorted(os.listdir(OUT))
print(f"\n✓ All Set 2 files complete. {len(files)} files in {OUT}:")
for f in files:
    size = os.path.getsize(os.path.join(OUT,f))
    print(f"  {f} ({size//1024}KB)")
