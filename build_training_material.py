"""
Build: PDLC VSM Platform Training Material — Word Document
Output: PDLC-VSM-Platform-Training-Material.docx
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY  = RGBColor(0x0F, 0x2D, 0x5E)
BLUE  = RGBColor(0x25, 0x63, 0xEB)
TEAL  = RGBColor(0x0D, 0x94, 0x88)
AMBER = RGBColor(0xD9, 0x77, 0x06)
RED   = RGBColor(0xDC, 0x26, 0x26)
GREEN = RGBColor(0x16, 0xA3, 0x4A)
GRAY  = RGBColor(0x4B, 0x55, 0x63)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

doc = Document()
section = doc.sections[0]
section.page_width    = Inches(8.5)
section.page_height   = Inches(11)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)
section.top_margin    = Inches(0.9)
section.bottom_margin = Inches(0.9)


def sf(run, size=11, bold=False, italic=False, color=None, name='Calibri'):
    run.font.name   = name
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color


def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(22)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run(text)
    sf(r, size=20, bold=True, color=NAVY)
    return p


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    sf(r, size=14, bold=True, color=BLUE)
    return p


def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    sf(r, size=12, bold=True, color=TEAL)
    return p


def body(text, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    sf(r, size=10.5, italic=italic)
    return p


def bullet(text, level=0, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.3 + level * 0.25)
    p.paragraph_format.space_after = Pt(2)
    if bold_prefix:
        rb = p.add_run(bold_prefix + ": ")
        sf(rb, size=10.5, bold=True)
        r = p.add_run(text)
        sf(r, size=10.5)
    else:
        r = p.add_run(text)
        sf(r, size=10.5)
    return p


def numbered(text, level=0):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.left_indent = Inches(0.3 + level * 0.25)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    sf(r, size=10.5)
    return p


def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '0F2D5E')
    pBdr.append(bottom)
    pPr.append(pBdr)


def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)


def add_table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    hrow = t.rows[0]
    for i, h in enumerate(headers):
        cell = hrow.cells[i]
        set_cell_bg(cell, '0F2D5E')
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        sf(r, size=9.5, bold=True, color=WHITE)
    for row_data in rows:
        row = t.add_row()
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            p = cell.paragraphs[0]
            r = p.add_run(str(val))
            sf(r, size=9.5)
    if col_widths:
        for row in t.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return t


def callout_box(title, lines, color=AMBER):
    hex_map = {
        AMBER: 'FEF3C7',
        TEAL:  'CCFBF1',
        RED:   'FEE2E2',
        GREEN: 'DCFCE7',
        BLUE:  'DBEAFE',
    }
    fill = hex_map.get(color, 'FEF3C7')
    t = doc.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    cell = t.rows[0].cells[0]
    set_cell_bg(cell, fill)
    p = cell.paragraphs[0]
    r = p.add_run(title + "  ")
    sf(r, size=10, bold=True, color=color)
    if isinstance(lines, str):
        lines = [lines]
    for line in lines:
        p2 = cell.add_paragraph()
        r2 = p2.add_run(line)
        sf(r2, size=10)
    doc.add_paragraph()


def page_break():
    doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(60)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("PDLC VSM PLATFORM")
sf(r, size=28, bold=True, color=NAVY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Practitioner Training Guide")
sf(r, size=20, bold=True, color=BLUE)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("From Baseline Measurement to AI Transformation Planning")
sf(r, size=12, italic=True, color=GRAY)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("v1.0  |  March 2026  |  9 Modules  |  Certification Quiz Included")
sf(r, size=10, color=GRAY)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Audience: Platform Users · Product Engineers · VSM Practitioners · DevOps Coaches")
sf(r, size=10, italic=True, color=GRAY)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 0 — INTRODUCTION
# ═══════════════════════════════════════════════════════════════════
h1("Module 0 — Introduction & Foundations")
body("Before diving into the platform, this module establishes the foundational concepts "
     "that underpin everything you will do. Lean VSM, DORA metrics, and the PDLC framework "
     "are the language of the platform — fluency here will make all 9 modules faster to learn.")

h2("What is the PDLC VSM Platform?")
body("The PDLC VSM Platform is an AI-powered tool that helps engineering organisations measure, "
     "analyse, and transform their Product Development Lifecycle. It does three things:")
bullet("Measures: ingests ALM ticket data and DORA metrics to produce a quantified current-state value stream map")
bullet("Analyses: 8 LangGraph AI agents identify bottlenecks, match improvements, and model future states")
bullet("Transforms: generates a personalised, compliance-aware implementation playbook with business case justification")

h2("The 8 AI Agents")
add_table(
    ["Agent",                    "Role",                                                "Output"],
    [
        ["ALM Connector",            "Ingests and maps ticket data to PDLC phases",          "VSM phase data (PT, WT per phase)"],
        ["VSM Analyzer",             "Computes lean metrics: FE%, LT, PT, WT",               "Metrics + executive narrative"],
        ["Benchmark Agent",          "Compares team metrics to industry benchmarks",          "Benchmark gap analysis"],
        ["Bottleneck Analyzer",      "Identifies and ranks flow impediments",                 "5–10 bottleneck cards with root causes"],
        ["Improvement Generator",    "Maps AI agents to each bottleneck",                    "36-agent improvement catalogue"],
        ["Future State Designer",    "Models Options A, B, C transformation scenarios",      "3 future-state VSMs with narratives"],
        ["Business Case Builder",    "Generates financial model for each scenario",           "ROI, payback, NPV per option"],
        ["Playbook Contextualizer",  "Personalises implementation guide from uploaded docs",  "AI playbook with 90-day sprint plan"],
    ],
    col_widths=[1.7, 3.0, 1.8]
)

h2("Learning Objectives by Module")
add_table(
    ["Module",  "Learning Outcome",                                              "Skill Level",   "Time"],
    [
        ["0 — Intro",        "Explain VSM, DORA, FE% formula and why they matter",           "Foundation",    "30 min"],
        ["1 — ALM Connect",  "Connect a data source and create a project",                   "Practitioner",  "20 min"],
        ["2 — DORA",         "Configure multi-source assessment and interpret DORA scores",  "Practitioner",  "30 min"],
        ["3 — Current VSM",  "Read and analyse a current-state value stream map",            "Practitioner",  "25 min"],
        ["4 — VSM Editor",   "Override metrics and model targeted improvements",             "Intermediate",  "20 min"],
        ["5 — Bottlenecks",  "Interpret AI bottleneck cards and lean waste categories",      "Intermediate",  "25 min"],
        ["6 — Improvements", "Filter and prioritise the AI improvement catalogue",           "Intermediate",  "30 min"],
        ["7 — Future State", "Compare transformation scenarios and present trade-offs",      "Advanced",      "30 min"],
        ["8 — Business Case","Build the financial model and present ROI to finance",         "Advanced",      "25 min"],
        ["9 — Playbook",     "Upload context and interpret a personalised implementation guide","Advanced",   "20 min"],
    ],
    col_widths=[1.5, 3.0, 1.1, 0.7]
)

h2("Prerequisites")
bullet("Basic understanding of Agile / Scrum delivery (sprints, user stories, epics)")
bullet("Familiarity with your organisation's ALM tool (Jira, Azure DevOps, or similar)")
bullet("Awareness of DevOps concepts: CI/CD, deployments, production monitoring")
body("No prior knowledge of Lean VSM, DORA metrics, or AI/ML is required — this guide covers everything.", italic=True)

page_break()

# ═══════════════════════════════════════════════════════════════════
# LEAN VSM FUNDAMENTALS
# ═══════════════════════════════════════════════════════════════════
h2("Lean VSM Fundamentals")

h3("What is a Value Stream Map?")
body("A Value Stream Map (VSM) is a visual tool from Lean manufacturing adapted for software delivery. "
     "It shows every step required to take a customer request from idea to production, making waste visible. "
     "In the PDLC context, a value stream runs from Backlog & Roadmap (idea) through to Monitoring & Feedback (live).")

h3("The Three Core Metrics")
add_table(
    ["Metric",             "Symbol", "Formula",                     "Unit",  "What It Tells You"],
    [
        ["Process Time",       "PT",     "Sum of active work hours",     "Hours", "How much real work is being done"],
        ["Wait Time",          "WT",     "Sum of blocked / queued hours","Hours", "How much waste exists in the flow"],
        ["Flow Efficiency",    "FE%",    "PT / (PT + WT) × 100",         "%",     "What % of lead time is value-adding"],
    ],
    col_widths=[1.4, 0.7, 2.0, 0.6, 1.8]
)

body("World-class software teams achieve 40%+ flow efficiency. "
     "Most financial services teams operate at 8–18% — meaning over 80% of lead time is pure waste.")

callout_box("Key Insight", [
    "If your team's lead time is 42 days and FE% is 17.8%, only 7.5 days of actual work is happening.",
    "The other 34.5 days are spent waiting, queued, or blocked. That is the transformation opportunity.",
], color=TEAL)

h3("The 7 PDLC Phases")
add_table(
    ["#", "Phase",                   "What Happens Here",                                       "Value or Waste?"],
    [
        ["1", "Backlog & Roadmap",       "Epic writing, feature prioritisation, roadmap planning",    "Value — if lean; waste if over-planned"],
        ["2", "Architecture & UX",       "Technical design, UX research, architecture decisions",     "Value — if time-boxed; waste if sequential review"],
        ["3", "Code Management",         "Feature coding, peer code review, merge to trunk",           "Value — coding; waste — review queue wait"],
        ["4", "Continuous Integration",  "Build, unit test, static analysis, SAST",                   "Value — fast CI; waste — long queues/flaky tests"],
        ["5", "Continuous Testing",      "SIT, UAT, NF testing, environment provisioning",             "Value — testing; waste — manual setup/waiting"],
        ["6", "Continuous Delivery",     "Release packaging, change approval, deployment",             "Value — deploy; waste — CAB/change freeze wait"],
        ["7", "Monitoring & Feedback",   "Production monitoring, incident response, feedback capture", "Value — insight; waste — alert noise/manual triage"],
    ],
    col_widths=[0.3, 1.5, 3.0, 1.7]
)

h3("The DOWNTIME Waste Framework")
body("Use DOWNTIME to classify the type of waste at each bottleneck:")
add_table(
    ["Letter", "Waste",            "Software Delivery Example"],
    [
        ["D",  "Defects",          "Production bugs, failed deployments, rework cycles"],
        ["O",  "Overproduction",   "Over-engineered features, unused APIs, premature optimisation"],
        ["W",  "Waiting",          "Awaiting approvals, blocked tickets, deployment queue"],
        ["N",  "Non-used Talent",  "Manual tasks that could be automated; senior engineers doing admin"],
        ["T",  "Transport",        "Excessive handoffs, too many ticket state transitions"],
        ["I",  "Inventory",        "WIP backlog, untested features, open PRs sitting unreviewed"],
        ["M",  "Motion",           "Context-switching, unnecessary meetings, tool-hopping"],
        ["E",  "Extra Processing", "Redundant approvals, duplicate documentation, gold-plating"],
    ],
    col_widths=[0.6, 1.5, 4.4]
)

h3("DORA — The 4 Key Metrics")
add_table(
    ["DORA Metric",             "What It Measures",                          "Elite Target",       "Low Benchmark"],
    [
        ["Deployment Frequency",    "How often you deploy to production",         "Multiple per day",   "< 1 per month"],
        ["Lead Time for Changes",   "Idea → production elapsed time",             "< 1 hour",           "> 6 months"],
        ["Change Failure Rate",     "% of deployments causing an incident",       "< 5%",               "> 15%"],
        ["Mean Time To Recover",    "Average time to restore after incident",     "< 1 hour",           "> 1 week"],
    ],
    col_widths=[1.8, 2.4, 1.3, 1.3]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 1
# ═══════════════════════════════════════════════════════════════════
h1("Module 1 — ALM Connect")
body("Learning time: ~20 minutes  |  Page: http://localhost:3001/alm-connect")
divider()

h2("Learning Objectives")
bullet("Navigate to the ALM Connect page and create a new project")
bullet("Configure a CSV data source and upload a sample file")
bullet("Verify that data has been mapped correctly to PDLC phases")
bullet("Understand what data fields map to which VSM metrics")

h2("Concept: What is ALM Data?")
body("ALM (Application Lifecycle Management) data is the record of work your team has done — every "
     "user story, bug, epic, and task tracked in tools like Jira or Azure DevOps. "
     "The platform reads this data to calculate how long work items spend in each PDLC phase, "
     "producing the raw time measurements for your current-state VSM.")

h3("How Tickets Map to VSM Phases")
add_table(
    ["Ticket Type / Label",     "Maps to PDLC Phase",        "Key Field Used"],
    [
        ["Epic, Roadmap item",      "Phase 1 — Backlog & Roadmap", "ticket type = Epic"],
        ["Architecture, ADR, Design","Phase 2 — Architecture & UX", "label contains 'design' or 'architecture'"],
        ["Story, Feature, Dev task", "Phase 3 — Code Management",  "ticket type = Story, status = In Dev"],
        ["Build, CI, Pipeline",     "Phase 4 — CI",               "label contains 'ci', 'build', 'pipeline'"],
        ["Test, QA, UAT, SIT",      "Phase 5 — Continuous Testing","label contains 'test', 'qa', 'uat', 'sit'"],
        ["Release, Deploy, CD",     "Phase 6 — Continuous Delivery","label contains 'release', 'deploy'"],
        ["Monitor, Alert, Incident","Phase 7 — Monitoring",        "label contains 'monitor', 'incident'"],
    ],
    col_widths=[2.0, 2.0, 2.5]
)

h2("Hands-On Exercise 1.1: Create a Project and Upload Data")

numbered("Navigate to http://localhost:3001/alm-connect")
numbered("Click 'New Project' in the top-right of the Project Setup panel")
numbered("Fill in the Project Setup form with your team's details (see field guidance in User Guide Step 1)")
numbered("Under 'ALM Data Source', select 'CSV File Upload' from the tool dropdown")
numbered("Click 'Choose File' and select your exported CSV file (UTF-8 encoding required)")
numbered("Click 'Fetch & Map Data' — a spinner confirms processing")
numbered("Review the Data Preview table: verify ticket count, phase distribution, and date range")
numbered("Click 'Save & Continue' to create the project and proceed to DORA Assessment")

callout_box("⚠️ Common Mistakes", [
    "1. Phase column missing: if your CSV has no 'phase' column, use labels like 'uat', 'deploy' in ticket titles.",
    "2. Wrong date format: dates must be YYYY-MM-DD. Excel sometimes exports MM/DD/YYYY — convert first.",
    "3. Zero wait time: if wait_time_days column is absent, the platform estimates WT from cycle time. Add it for accuracy.",
], color=RED)

h2("Knowledge Check — Module 1")
add_table(
    ["#", "Question",                                                                "Answer"],
    [
        ["1", "What is the minimum set of CSV columns required to create a project?", "ticket_id, type, status, cycle_time_days"],
        ["2", "Which PDLC phase does a ticket labelled 'uat' map to?",               "Phase 5 — Continuous Testing"],
        ["3", "Where can you verify that phase mapping was correct after upload?",    "In the Data Preview table (phase distribution row)"],
    ],
    col_widths=[0.3, 3.8, 2.4]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 2
# ═══════════════════════════════════════════════════════════════════
h1("Module 2 — DORA Assessment")
body("Learning time: ~30 minutes  |  Page: http://localhost:3001/dora-assessment")
divider()

h2("Learning Objectives")
bullet("Explain the 4 DORA dimensions and what each measures")
bullet("Configure at least 2 data sources and trigger AI auto-scoring")
bullet("Interpret DORA scores and identify the weakest dimension")
bullet("Explain how DORA calibration values adjust the VSM in the next step")

h2("Concept: The 4 DORA Dimensions")
add_table(
    ["Dimension",               "Questions", "Focus",                                              "Scoring Signals"],
    [
        ["Cultural Practices",      "18",   "Psychological safety, team autonomy, learning culture","Survey / workshop responses (manual)"],
        ["Measurement & Monitoring","20",   "Observability, alerting, SLO coverage, dashboards",   "Splunk, Datadog, Dynatrace, Grafana"],
        ["Process & Flow",          "18",   "Sprint cadence, WIP limits, deployment process",      "Jira, Azure DevOps, GitHub Actions"],
        ["Technical Practices",     "17",   "CI/CD maturity, test automation %, security gates",   "GitHub, Jenkins, SonarQube, Snyk"],
    ],
    col_widths=[1.8, 0.9, 2.8, 2.0]
)

h2("Concept: From DORA Scores to VSM Calibration")
body("DORA scores are not just a report card — they directly adjust your VSM metrics. "
     "Here is how each DORA metric calibrates a VSM phase:")
add_table(
    ["DORA Metric",         "Measures",                    "Calibrates VSM Phase",   "Calibration Field"],
    [
        ["Lead Time for Change", "Idea → production elapsed time","Phases 3–6 proportionally", "phases3to6_lt_days"],
        ["Deployment Frequency", "How often code ships",          "Phase 6 WT",                "phase6_wt"],
        ["Change Failure Rate",  "% of deployments causing incidents","Phase 5 PT (rework)",  "phase5_rework_factor"],
        ["MTTR",                 "Time to recover from incidents",  "Phase 7 WT",              "phase7_wt"],
    ],
    col_widths=[1.7, 2.2, 1.8, 1.8]
)

h2("Hands-On Exercise 2.1: Configure Data Sources")
numbered("On the DORA Assessment page, click '+ Add Source'")
numbered("Select source type: GitHub")
numbered("Enter your repository URL: e.g. https://github.com/yourorg/payments-api")
numbered("Enter a label: 'Payments API Repository'")
numbered("Click 'Save Source' — a green tick confirms the source is added")
numbered("Repeat to add a Jira source with your board URL")
numbered("Click 'Run AI Assessment' to trigger auto-scoring across all 73 questions")

h2("Hands-On Exercise 2.2: Review and Override Scores")
numbered("Review the dimension score cards (1–5 scale for each of 4 dimensions)")
numbered("Click on the 'Cultural Practices' dimension to expand the 18 questions")
numbered("For any question where AI could not auto-score (shown as '?' icon), enter a manual score")
numbered("Use the scoring scale: 1 = Initial (ad hoc), 3 = Defined, 5 = Optimising")
numbered("Click 'Save Responses' — the dimension score updates in real time")
numbered("Note the DORA Band badge at the top: Elite / High / Medium / Low")

h2("Interpreting Your DORA Results")
body("Once scoring is complete, check these three things:")
bullet("Overall Band — this tells you your team's global maturity (aim for High or Elite)")
bullet("Weakest Dimension — the lowest-scoring dimension is where most transformation effort should focus")
bullet("Calibration Values — scroll to the 'VSM Calibration Export' panel to see the 5 values generated")

callout_box("💡 Tip — Cultural Practices Scoring", [
    "Cultural Practices cannot be auto-scored from tool data — it requires human judgement.",
    "Best practice: run a 30-minute team workshop to score these 18 questions by consensus.",
    "Consensus scoring is more accurate and builds team alignment on the improvement journey.",
], color=TEAL)

h2("Knowledge Check — Module 2")
add_table(
    ["#", "Question",                                                              "Answer"],
    [
        ["1", "Which DORA dimension cannot be auto-scored from tool data?",        "Cultural Practices — requires manual / survey input"],
        ["2", "What does a Change Failure Rate of 12% indicate?",                  "Medium band — above the 10% High threshold, below 15% Low threshold"],
        ["3", "Which VSM phase does MTTR calibrate?",                              "Phase 7 — Monitoring & Feedback (wait time)"],
        ["4", "A team scores 1.8/5 on Technical Practices. What should they do?", "Prioritise CI/CD maturity, test automation, and security gate improvements"],
    ],
    col_widths=[0.3, 3.5, 2.7]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 3
# ═══════════════════════════════════════════════════════════════════
h1("Module 3 — Current State VSM")
body("Learning time: ~25 minutes  |  Page: http://localhost:3001/vsm-current")
divider()

h2("Learning Objectives")
bullet("Read and interpret a current-state VSM with all 7 PDLC phases")
bullet("Calculate FE% for any phase given PT and WT values")
bullet("Identify the top 3 waste areas from a VSM by inspection")
bullet("Compare team metrics to industry benchmarks")

h2("Concept: Reading the VSM Diagram")
body("The current-state VSM displays as a horizontal swimlane with 7 phase cards. "
     "Each phase card shows: Process Time (hours), Wait Time (hours), Flow Efficiency (%), "
     "and a colour-coded FE bar. Below the phases, a timeline bar shows total lead time in days.")

h3("Colour Coding")
bullet("Green phase bar (FE > 35%) — relatively efficient; not a priority for improvement")
bullet("Amber phase bar (FE 15–35%) — moderate waste; monitor and include in improvement planning")
bullet("Red phase bar (FE < 15%) — significant waste; prioritise for transformation immediately")

h2("Worked Example — US Bank / Team Phoenix")
body("Use this worked example to practise reading a VSM:")
add_table(
    ["Phase",                  "PT (h)", "WT (h)", "FE%",  "Colour", "Observation"],
    [
        ["Backlog & Roadmap",      "25",  "72",   "25.8", "Amber",  "Stakeholder alignment delays; moderate waste"],
        ["Architecture & UX",      "36",  "176",  "17.0", "Red",    "Sequential design reviews cause 176h wait"],
        ["Code Management",        "13",  "18",   "41.9", "Green",  "Efficient — small PRs, fast review cycle"],
        ["Continuous Integration", "6",   "8",    "42.9", "Green",  "CI pipeline is fast and stable"],
        ["Continuous Testing",     "31",  "240",  "11.4", "Red",    "CRITICAL — manual UAT + SIT = 240h wait"],
        ["Continuous Delivery",    "12",  "56",   "17.6", "Red",    "CAB approval adding 56h deployment queue"],
        ["Monitoring & Feedback",  "7",   "30",   "18.9", "Amber",  "Alert noise causing delayed triage"],
        ["TOTAL",                  "130", "600",  "17.8", "Red",    "80%+ of lead time is non-value-adding waste"],
    ],
    col_widths=[1.7, 0.6, 0.6, 0.6, 0.7, 2.3]
)

h2("Hands-On Exercise 3.1: Analyse Your Current State")
numbered("On the Current State VSM page, identify the 3 phases with the lowest FE% (red bars)")
numbered("For each red phase, note the WT value — this is the waste volume to eliminate")
numbered("Calculate: what would overall FE% be if Phase 5 WT dropped from 240h to 48h?")
numbered("Check the Benchmark Comparison panel — how does your FE% compare to industry median?")
numbered("Note the top gap (largest delta between your metric and the Elite benchmark)")

callout_box("Practice Calculation", [
    "Given: Phase 5 current PT=31h, WT=240h. What is the new FE% if WT drops to 48h?",
    "Answer: New FE% = 31 / (31 + 48) × 100 = 31 / 79 × 100 = 39.2%",
    "Impact: Phase 5 moves from Red (11.4%) to approaching Green (39.2%)",
], color=AMBER)

h2("Knowledge Check — Module 3")
add_table(
    ["#", "Question",                                                       "Answer"],
    [
        ["1", "A phase has PT=20h and WT=60h. What is FE%?",               "20/(20+60)×100 = 25%  (Amber band)"],
        ["2", "Which phase in the US Bank example is the biggest bottleneck?","Phase 5 — Continuous Testing (WT=240h, FE=11.4%)"],
        ["3", "What does a green FE% bar tell you?",                        "Phase is relatively efficient (>35%) — not a priority"],
    ],
    col_widths=[0.3, 3.2, 3.0]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 4
# ═══════════════════════════════════════════════════════════════════
h1("Module 4 — VSM Editor")
body("Learning time: ~20 minutes  |  Page: http://localhost:3001/vsm-editor")
divider()

h2("Learning Objectives")
bullet("Navigate to the VSM Editor and select a phase for editing")
bullet("Override a phase-level wait time and observe FE% recalculation")
bullet("Drill into activity-level metrics within a phase")
bullet("Explain the difference between actual data and override data")

h2("Concept: What Overrides Do")
body("Overrides allow you to model 'what-if' scenarios without changing the source data. "
     "They answer the question: 'If we deployed the AI UAT Assistant and reduced Phase 5 "
     "wait time by 80%, what would our overall lead time become?' "
     "Overrides are clearly labelled with a blue badge so stakeholders can distinguish actual vs. modelled data.")

h2("Hands-On Exercise 4.1: Edit Phase 5 — Continuous Testing")
numbered("On the VSM Editor page, click on Phase 5 card (Continuous Testing)")
numbered("The phase expands to show 6 activities with individual PT and WT values")
numbered("Locate 'Manual SIT Execution' — current WT = 120h")
numbered("Click the edit icon (pencil) next to WT value '120'")
numbered("Type '24' (an 80% reduction modelling AI test automation deployment)")
numbered("Observe real-time recalculation: Phase 5 FE% updates from 11.4% → ~31%")
numbered("Locate 'Manual UAT / NF Signoff' — current WT = 80h")
numbered("Edit to '16' (80% reduction from AI UAT Assistant)")
numbered("Observe overall FE% in the summary panel update from 17.8% → ~28%")
numbered("Click 'Save Overrides' — a blue badge appears on Phase 5 card")

h3("Interpreting the Before / After Comparison")
body("The editor shows a split view once overrides are applied:")
bullet("Left column: actual values from ALM data (grey background)")
bullet("Right column: overridden values used in modelling (blue background)")
bullet("Delta row: absolute change in PT, WT, and FE%")
bullet("Summary panel: updated total LT and overall FE% with override applied")

h2("Knowledge Check — Module 4")
add_table(
    ["#", "Question",                                                                      "Answer"],
    [
        ["1", "How do you undo an override you applied to Phase 6 WT?",                    "Click the reset (↺) icon next to the overridden field"],
        ["2", "If you override Phase 5 WT from 240h to 48h, does Phase 5 FE% increase or decrease?","Increase — less wait relative to process time = higher FE%"],
    ],
    col_widths=[0.3, 3.8, 2.4]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 5
# ═══════════════════════════════════════════════════════════════════
h1("Module 5 — Bottleneck Analysis")
body("Learning time: ~25 minutes  |  Page: http://localhost:3001/bottlenecks")
divider()

h2("Learning Objectives")
bullet("Trigger the AI bottleneck analysis and explain what it does")
bullet("Read a bottleneck card and extract the key information from each field")
bullet("Classify a bottleneck by DOWNTIME waste category")
bullet("Explain the severity thresholds and how to prioritise the response")

h2("Concept: How the AI Detects Bottlenecks")
body("The bottleneck detection works in 5 automated steps:")
numbered("Calculate WT/PT ratio for every activity across all 7 phases")
numbered("Compare each activity's WT against phase-specific benchmarks from the knowledge base")
numbered("Assess each phase's FE% against industry median for your sector")
numbered("Score each potential bottleneck: Severity = WT × (1 − FE%) × benchmark_gap_factor")
numbered("Generate a root cause narrative using LLM (or deterministic rule-based if no API key)")

h2("Hands-On Exercise 5.1: Run and Read Bottleneck Analysis")
numbered("On the Bottleneck Analysis page, click 'Run AI Analysis'")
numbered("Wait for the spinner to complete (typically 15–30 seconds)")
numbered("Review the bottleneck cards — they are sorted by severity (Critical first)")
numbered("Click on the top Critical bottleneck to expand it")
numbered("Read each field: Phase, Activity, Severity, WT, PT, FE%, Root Cause, Lean Waste Type")
numbered("Note the Competitor Insight banner — it shows what a similar organisation achieved")
numbered("Answer: What lean waste type is the top bottleneck? (Check DOWNTIME reference)")

h3("Expected Output for US Bank / Team Phoenix")
add_table(
    ["Severity",  "Phase",  "Activity",                     "WT",    "Root Cause Summary"],
    [
        ["Critical",  "5",    "Manual SIT / UAT Execution",   "240h",  "No parallel execution, manual env setup, test data dependency"],
        ["Critical",  "2",    "Architecture Review Gate",     "176h",  "Sequential reviews, 3-day advance scheduling, limited reviewers"],
        ["High",      "6",    "Release Approval / CAB Gate",  "56h",   "72-hour advance CAB notice, manual risk assessment"],
        ["High",      "1",    "Feature Refinement Loop",      "48h",   "Incomplete requirements, stakeholder availability gaps"],
        ["Medium",    "3",    "Peer Code Review Queue",       "18h",   "Average PR size 850 lines, 2 senior reviewer bottleneck"],
    ],
    col_widths=[0.8, 0.5, 2.2, 0.7, 2.3]
)

h2("Knowledge Check — Module 5")
add_table(
    ["#", "Question",                                                             "Answer"],
    [
        ["1", "What is the severity threshold for a 'Critical' bottleneck?",      "WT > 150h OR FE% < 10%"],
        ["2", "A bottleneck with WT=240h, PT=31h is which lean waste type?",      "Waiting (W) — time blocked awaiting environment, approval, or input"],
        ["3", "What action does a High severity bottleneck require?",             "Include in next quarter transformation planning"],
    ],
    col_widths=[0.3, 3.5, 2.7]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 6
# ═══════════════════════════════════════════════════════════════════
h1("Module 6 — Improvements")
body("Learning time: ~30 minutes  |  Page: http://localhost:3001/improvements")
divider()

h2("Learning Objectives")
bullet("Navigate the AI improvement catalogue and apply filters")
bullet("Read an improvement card and extract effort/wait reduction data")
bullet("Identify Quick Wins vs. long-horizon improvements")
bullet("Explain how ROI is calculated and what the default assumptions are")

h2("Concept: The 36-Agent Catalogue")
body("The AI improvement catalogue contains 36 pre-mapped solutions spanning all 7 PDLC phases. "
     "Each solution is an AI agent, automation, or GenAI capability that has been validated against "
     "real-world deployments by industry peers. The catalogue includes competitor evidence showing "
     "what similar organisations have achieved when deploying each agent.")

h2("Hands-On Exercise 6.1: Filter and Prioritise Improvements")
numbered("On the Improvements page, toggle 'Quick Wins Only' to ON")
numbered("Observe that the catalogue filters to improvements deliverable in <90 days")
numbered("Sort by ROI (descending) — identify the top 3 Quick Wins by ROI")
numbered("Click on 'AI UAT Assistant' card to expand it")
numbered("Note: Effort Reduction 80%, Wait Reduction 80%, ROI 3.2×, Quick Win ✓")
numbered("Read the Competitor Insight: 'Humana reduced UAT wait by 78% with AI test automation in 6 months'")
numbered("Toggle Quick Wins OFF and sort by Wait Reduction — identify the single biggest WT reduction")
numbered("Note which phase that improvement is in — is it the same as your top bottleneck?")

h2("Hands-On Exercise 6.2: Build a Prioritisation List")
body("Using the filters, build a prioritised shortlist of improvements in this order:")
numbered("Quick Wins with ROI > 2× (deploy in months 1–3)")
numbered("High WT reduction improvements in Critical bottleneck phases (deploy months 4–9)")
numbered("Strategic improvements (long-horizon, high investment, high return) (months 10–18)")

h3("Improvement Cards — Key Fields Explained")
add_table(
    ["Field",             "What It Means",                                         "Typical Range"],
    [
        ["Effort Reduction %",  "% reduction in active work time (FTE hours freed)",  "30–80%"],
        ["Wait Reduction %",    "% reduction in wait time for the activity",           "40–90%"],
        ["ROI Estimate",        "Annual benefit / total implementation cost",          "1.7× – 5.5×"],
        ["Quick Win",           "Deliverable and measurable in <90 days",              "~40% of catalogue"],
        ["Agent Type",          "GenAI / Agentic AI / Automation / HITL",             "Mix across catalogue"],
    ],
    col_widths=[1.5, 3.0, 1.5]
)

callout_box("💡 Using Competitor Insights in Presentations", [
    "Every improvement card with a 'Competitor Insight' banner contains a real benchmark from a peer organisation.",
    "Use these as proof points in executive presentations: 'JPMorgan automated 70% of standard change approvals.'",
    "This turns your business case from internal opinion into external validation.",
], color=TEAL)

h2("Knowledge Check — Module 6")
add_table(
    ["#", "Question",                                                              "Answer"],
    [
        ["1", "What defines a Quick Win improvement?",                             "Deliverable and measurable in less than 90 days"],
        ["2", "An improvement shows Wait Reduction 80% for Phase 5 (WT=240h). What is the new WT?","48 hours (80% of 240 = 192h reduction; 240-192 = 48h)"],
        ["3", "What is the default FTE salary assumption in the ROI calculation?", "$120,000 per year (fully loaded)"],
        ["4", "How do you find improvements specific to Phase 6 only?",            "Use the Phase filter and select 'Continuous Delivery'"],
    ],
    col_widths=[0.3, 3.5, 2.7]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 7
# ═══════════════════════════════════════════════════════════════════
h1("Module 7 — Future State VSM")
body("Learning time: ~30 minutes  |  Page: http://localhost:3001/vsm-future")
divider()

h2("Learning Objectives")
bullet("Compare the three transformation options on key metrics")
bullet("Read the AI narrative for each option and identify key claims")
bullet("Select an appropriate option based on given constraints (budget, risk, timeline)")
bullet("Present the future state comparison to a specific executive audience")

h2("Concept: Three Horizons of Transformation")
add_table(
    ["Attribute",             "Option A — AI Augment",    "Option B — Hybrid Intel",  "Option C — ADLC"],
    [
        ["Horizon",               "12 months",                "18 months",                "24–36 months"],
        ["Agents Deployed",       "8",                        "15",                       "22+"],
        ["Flow Efficiency",       "~42%",                     "~61%",                     "~78%"],
        ["Lead Time Reduction",   "~57%",                     "~81%",                     "~93%"],
        ["Investment",            "$1.2M – $1.8M",            "$2.5M – $3.5M",            "$4M – $6M"],
        ["Risk Level",            "Low",                      "Medium",                   "High"],
        ["Team Change",           "Augmentation only",        "Hybrid human + AI",        "AI-first, 2 human roles"],
        ["Best For",              "Budget <$2M, low risk",    "Balanced transformation",  "Full mandate, high appetite"],
    ],
    col_widths=[1.8, 1.7, 1.8, 1.2]
)

h2("Hands-On Exercise 7.1: Compare All Three Options")
numbered("On the Future State VSM page, click the 'Option A' tab")
numbered("Read the AI narrative — note the lead time claim (days) and FE% claim")
numbered("Click 'Option B' — compare: what additional agents are deployed vs. Option A?")
numbered("Click 'Option C' — which phases benefit most from the additional agents?")
numbered("Use the phase comparison table: identify which phase shows the biggest FE% improvement in Option C")
numbered("Answer the scenario: 'Budget is $2M and risk appetite is low — which option do you recommend and why?'")

h2("Scenario-Based Decision Framework")
add_table(
    ["Constraint",               "Option A",     "Option B",      "Option C"],
    [
        ["Budget < $2M",             "✓ Recommended","Not feasible",  "Not feasible"],
        ["Budget $2M–$4M",           "Under-invest", "✓ Recommended", "Not feasible"],
        ["Budget > $4M",             "Under-invest", "Possible",      "✓ Recommended"],
        ["Timeline < 12 months",     "✓ Possible",   "Too long",      "Too long"],
        ["Low risk appetite",        "✓ Best fit",   "Acceptable",    "Not recommended"],
        ["DORA Elite target",        "Unlikely",     "Possible",      "✓ Required"],
        ["Regulatory environment",   "✓ Easiest",    "Manageable",    "Complex compliance"],
    ],
    col_widths=[2.4, 1.2, 1.2, 1.7]
)

h2("Knowledge Check — Module 7")
add_table(
    ["#", "Question",                                                                 "Answer"],
    [
        ["1", "Which option achieves DORA Elite performance?",                        "Option C — ADLC (22+ agents, ~78% FE)"],
        ["2", "A regulated FSI team has $3M budget and medium risk appetite. Which option?","Option B — Hybrid Intelligence"],
        ["3", "What is the lead time reduction (%) for Option B on a 42-day baseline?","81% — from 42 days to ~8 days"],
    ],
    col_widths=[0.3, 3.8, 2.4]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 8
# ═══════════════════════════════════════════════════════════════════
h1("Module 8 — Business Case")
body("Learning time: ~25 minutes  |  Page: http://localhost:3001/business-case")
divider()

h2("Learning Objectives")
bullet("Identify the 5 benefit streams that compose the financial model")
bullet("Customise 3 financial assumptions and observe the impact on ROI")
bullet("Read the executive summary, investment breakdown, and payback metric")
bullet("Explain the difference between conservative, base, and optimistic scenarios")

h2("The 5 Benefit Streams")
add_table(
    ["Stream",               "What It Captures",                                      "Key Input Assumption"],
    [
        ["Labour Savings",       "FTE time freed by automation — redeployable to value work","FTE salary + team size"],
        ["Quality Improvement",  "Value of defects eliminated and rework removed",           "Defect cost per incident"],
        ["Speed-to-Market",      "Revenue enabled by delivering features faster",            "Revenue at risk per day"],
        ["Risk Reduction",       "Compliance fine and production incident avoidance",         "Compliance fine exposure"],
        ["Platform Cost Avoidance","Legacy tool and cloud cost savings from rationalisation","Monthly infra cost"],
    ],
    col_widths=[1.7, 2.8, 2.0]
)

h2("Hands-On Exercise 8.1: Review Option B Business Case")
numbered("On the Business Case page, ensure Option B is selected")
numbered("Review the Executive Summary box: note ROI multiple, investment range, and payback period")
numbered("Scroll to Investment Breakdown — identify the largest cost category")
numbered("Scroll to Benefits Waterfall — which benefit stream contributes most to Year 1 benefits?")
numbered("Change the 'Revenue at Risk (daily)' assumption from $500K to $1M")
numbered("Observe: Year 1 benefits increase; ROI multiple increases; payback shortens")
numbered("Toggle to 'Conservative' scenario — observe the ±25% adjustment on benefits")
numbered("Write down: ROI multiple (Base), ROI multiple (Conservative), and payback (Base)")

h3("US Bank Option B — Reference Numbers")
add_table(
    ["Metric",                "Conservative",   "Base",     "Optimistic"],
    [
        ["Investment (total)",    "$3.5M",          "$3.0M",    "$2.5M"],
        ["Year 1 Benefits",       "$2.7M",          "$3.6M",    "$4.5M"],
        ["Year 2 Benefits",       "$6.3M",          "$8.4M",    "$10.5M"],
        ["Year 3 Benefits",       "$9.1M",          "$12.1M",   "$15.1M"],
        ["ROI Multiple (3yr)",    "3.1×",           "4.2×",     "5.6×"],
        ["Payback Period",        "18 months",      "14 months","11 months"],
        ["5-Year NPV",            "$21.4M",         "$31.2M",   "$44.0M"],
    ],
    col_widths=[2.0, 1.5, 1.5, 1.5]
)

h2("Knowledge Check — Module 8")
add_table(
    ["#", "Question",                                                                      "Answer"],
    [
        ["1", "What is the default FTE salary assumption in the financial model?",         "$120,000 per year (fully loaded)"],
        ["2", "Which benefit stream is typically largest for a regulated bank?",           "Labour Savings — large teams, high compliance overhead"],
        ["3", "Conservative scenario applies what adjustment to base benefits?",           "−25% to all benefit streams; +15% cost overrun assumed"],
    ],
    col_widths=[0.3, 3.5, 2.7]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# MODULE 9
# ═══════════════════════════════════════════════════════════════════
h1("Module 9 — Playbook Context")
body("Learning time: ~20 minutes  |  Page: http://localhost:3001/playbook")
divider()

h2("Learning Objectives")
bullet("Explain what RAG (Retrieval-Augmented Generation) does in the platform")
bullet("Upload 3 context documents and explain what each contributes to the playbook")
bullet("Add 2 knowledge base URLs and explain their purpose")
bullet("Identify the 5 sections of the generated playbook and describe each")

h2("Concept: Why Context Matters")
body("Without context documents, the playbook is generic — useful but not specific to your team. "
     "With a compliance framework uploaded, the playbook adds FFIEC/SOX approval gates. "
     "With the team charter uploaded, it uses your team members' names and acknowledges your org structure. "
     "The AI uses RAG (Retrieval-Augmented Generation) to embed and retrieve the most relevant passages "
     "from each document when generating each section of the playbook.")

h2("Document Priority Guide")
add_table(
    ["Document",                 "Priority",  "Impact on Playbook"],
    [
        ["Team Charter",             "High",      "Personalises roles, uses team names, reflects actual structure"],
        ["DevOps Maturity Report",   "High",      "Grounds recommendations in current capability baseline"],
        ["Compliance Framework",     "High (regulated)","Adds regulatory gates, audit requirements, HITL checkpoints"],
        ["Architecture Standards",   "High",      "Aligns integration patterns to existing API/security standards"],
        ["Sprint Retrospectives",    "Recommended","References known team pain points and avoids past failures"],
        ["OKR / Strategy Doc",       "Recommended","Links initiatives to strategic objectives by name"],
        ["DORA Benchmark Report",    "Recommended","Calibrates targets to sector norms vs. generic percentiles"],
    ],
    col_widths=[2.0, 1.0, 3.5]
)

h2("Hands-On Exercise 9.1: Upload and Generate Playbook")
numbered("On the Playbook Context page, click 'Upload Document'")
numbered("Upload your team charter (TXT or DOCX format, <10MB)")
numbered("Select category: 'Team Context' from the dropdown")
numbered("Click '+ Add URL' and paste the DORA 2024 Report URL")
numbered("Select scenario: 'Option B — Hybrid Intelligence'")
numbered("Toggle 'Regulated Environment' to ON (for FSI/Healthcare teams)")
numbered("Click 'Generate Playbook' — this takes 1–3 minutes")
numbered("Review the playbook structure: Executive Summary → Phase Roadmap → Agent Guide → Change Management → 90-Day Sprint")

h2("Reading the Playbook Output")
add_table(
    ["Section",                 "What It Contains",                                      "Audience"],
    [
        ["Executive Summary",       "Top 5 initiatives, investment recap, decision rationale", "CTO / CPO"],
        ["Phase-by-Phase Roadmap",  "Per-phase: current state, target, steps, KPIs, timeline", "Programme Manager"],
        ["Agent Implementation Guide","Per-agent: prerequisites, integration guide, success metrics","Engineering Lead"],
        ["Change Management Plan",  "Stakeholder impacts, communication plan, training needs",  "HR / Change Lead"],
        ["First 90 Days Sprint Plan","Weeks 1–12: foundation, quick wins, measure and expand",  "Scrum Master / Delivery Lead"],
    ],
    col_widths=[1.8, 3.2, 1.5]
)

h2("Knowledge Check — Module 9")
add_table(
    ["#", "Question",                                                              "Answer"],
    [
        ["1", "What does RAG stand for and why does it matter here?",              "Retrieval-Augmented Generation — makes AI output specific to your uploaded documents"],
        ["2", "Which document most changes the playbook for a regulated bank?",    "Compliance Framework — adds HITL gates, audit trails, regulatory approval steps"],
        ["3", "What does the First 90 Days Sprint Plan cover?",                   "Foundation (wks 1–4), Quick Wins (wks 5–8), Measure and expand (wks 9–12)"],
    ],
    col_widths=[0.3, 3.5, 2.7]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# CERTIFICATION QUIZ
# ═══════════════════════════════════════════════════════════════════
h1("Certification Quiz — PDLC VSM Practitioner")
body("Pass mark: 16 / 20 (80%)  |  Estimated time: 20 minutes  |  Open-book allowed")
divider()

questions = [
    ("What does FE% stand for and how is it calculated?",
     "A) Flow Efficiency = WT / (PT + WT) × 100  "
     "B) Flow Efficiency = PT / (PT + WT) × 100  "
     "C) Flow Efficiency = LT / PT × 100  "
     "D) Flow Efficiency = PT / LT",
     "B"),
    ("A team has PT=40h and WT=160h across all phases. What is their overall FE%?",
     "A) 15%   B) 20%   C) 25%   D) 40%",
     "B — 40/(40+160)×100 = 20%"),
    ("Which DORA dimension requires manual scoring and cannot be auto-scored from tool data?",
     "A) Measurement & Monitoring  "
     "B) Process & Flow  "
     "C) Cultural Practices  "
     "D) Technical Practices",
     "C"),
    ("What does a Change Failure Rate of 12% indicate about a team's DORA maturity band?",
     "A) Elite   B) High   C) Medium   D) Low",
     "C — Medium band (10–15% CFR)"),
    ("Which lean waste type best describes a bottleneck where UAT wait = 240h due to manual test setup?",
     "A) Defects   B) Overproduction   C) Waiting   D) Inventory",
     "C — Waiting (W in DOWNTIME)"),
    ("What is the primary purpose of VSM Editor overrides?",
     "A) Permanently change ALM ticket data  "
     "B) Model what-if scenarios without modifying source data  "
     "C) Delete phases from the VSM  "
     "D) Auto-run the full AI pipeline",
     "B"),
    ("How does the platform use DORA calibration values?",
     "A) They replace the ALM CSV data entirely  "
     "B) They adjust VSM phase PT/WT to reflect DORA performance  "
     "C) They are only used in the Business Case  "
     "D) They override the improvement catalogue",
     "B"),
    ("A bottleneck has WT=80h and FE%=18%. What severity level does it receive?",
     "A) Critical   B) High   C) Medium   D) Low",
     "B — High (WT 50–150h AND FE 10–20%)"),
    ("Which Future State option is recommended for a team with budget $3M and medium risk appetite?",
     "A) Option A   B) Option B   C) Option C   D) No option fits",
     "B — Option B Hybrid Intelligence"),
    ("What does 'Quick Win' mean in the Improvements catalogue?",
     "A) The improvement costs < $100K  "
     "B) The improvement delivers measurable results in < 90 days  "
     "C) The improvement reduces WT by > 50%  "
     "D) The improvement requires no integration work",
     "B"),
    ("Which benefit stream captures the value of features reaching market faster?",
     "A) Labour Savings  "
     "B) Quality Improvement  "
     "C) Speed-to-Market  "
     "D) Risk Reduction",
     "C"),
    ("What does uploading a Compliance Framework document do to the generated playbook?",
     "A) Nothing — it is only used in the Business Case  "
     "B) Adds regulatory gates, HITL checkpoints, and audit trail requirements  "
     "C) Replaces the generic agent recommendations with compliance tools  "
     "D) Disables Option C as a valid future state",
     "B"),
    ("In the 7-phase PDLC, which phase typically has the highest wait time in regulated industries?",
     "A) Phase 1 — Backlog   B) Phase 3 — Code   C) Phase 5 — Testing   D) Phase 7 — Monitoring",
     "C — Phase 5 Continuous Testing (manual UAT/SIT in regulated environments)"),
    ("What is the formula for Lead Time (LT) given PT and WT in hours?",
     "A) LT = PT + WT  "
     "B) LT = (PT + WT) / 8  "
     "C) LT = PT × WT  "
     "D) LT = WT / 8",
     "B — converts hours to working days (8h/day)"),
    ("Which agent type provides the highest WT reduction percentage?",
     "A) GenAI (30–50%)  "
     "B) Agentic AI (50–80%)  "
     "C) Full Automation (70–90%)  "
     "D) Human-in-the-Loop (20–40%)",
     "C — Full Automation: 70–90% WT reduction"),
    ("What is the payback period for Option B (Base scenario) in the US Bank example?",
     "A) 8 months   B) 14 months   C) 21 months   D) 27 months",
     "B — 14 months"),
    ("How many AI agents does the platform's 8-agent LangGraph pipeline include?",
     "A) 6   B) 7   C) 8   D) 10",
     "C — 8 agents: ALM Connector, VSM Analyzer, Benchmark, Bottleneck, Improvement, Future State, Business Case, Playbook"),
    ("What is the recommended FE% target for a world-class software delivery team?",
     "A) > 20%   B) > 30%   C) > 40%   D) > 60%",
     "C — > 40% is the world-class benchmark"),
    ("Which module's output directly calibrates the VSM phase metrics?",
     "A) Module 1 — ALM Connect  "
     "B) Module 2 — DORA Assessment  "
     "C) Module 4 — VSM Editor  "
     "D) Module 6 — Improvements",
     "B — DORA Assessment generates calibration values applied to VSM"),
    ("A team uploads a team charter and sprint retrospectives to the Playbook Context. What changes?",
     "A) The ROI calculation uses team-specific salary data  "
     "B) The playbook uses team member names and avoids solutions that previously failed  "
     "C) The future state FE% targets increase  "
     "D) The DORA assessment re-runs automatically",
     "B"),
]

for i, (q, options, answer) in enumerate(questions, 1):
    h3(f"Question {i}")
    body(q)
    body(options, italic=True)
    doc.add_paragraph()

page_break()

h2("Answer Key")
answer_data = [(str(i+1), questions[i][0][:50]+"...", questions[i][2]) for i in range(20)]
add_table(
    ["Q#", "Topic", "Correct Answer"],
    answer_data,
    col_widths=[0.4, 3.8, 2.3]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# APPENDIX A — VSM REFERENCE CARD
# ═══════════════════════════════════════════════════════════════════
h1("Appendix A — Lean VSM Reference Card")

h2("Formulas")
add_table(
    ["Metric",          "Formula",                         "Unit"],
    [
        ["Flow Efficiency", "PT / (PT + WT) × 100",            "%"],
        ["Lead Time",       "(PT + WT) / 8",                   "Days"],
        ["WT/PT Ratio",     "WT / PT",                         "Ratio"],
        ["Phase LT",        "(Phase PT + Phase WT) / 8",       "Days"],
        ["ROI",             "Total Benefits / Total Investment","Multiple"],
        ["Payback Month",   "Investment / Monthly Benefit",     "Months"],
    ],
    col_widths=[1.7, 2.8, 1.0]
)

h2("FE% Band Colours")
add_table(
    ["Colour", "FE% Range", "Meaning",              "Action"],
    [
        ["Green",  "> 35%",    "Efficient",             "Monitor; not a priority"],
        ["Amber",  "15–35%",   "Moderate waste",        "Include in quarterly planning"],
        ["Red",    "< 15%",    "Critical waste",        "Address in next 90 days"],
    ],
    col_widths=[0.8, 1.0, 1.5, 3.2]
)

h2("Appendix B — AI Agent Catalogue Summary")
add_table(
    ["Phase", "Agent",                    "Typical WT Reduction", "Typical Effort Reduction"],
    [
        ["1",  "AI Backlog Prioritiser",     "35–50%",  "30–45%"],
        ["1",  "AI Epic Decomposer",         "25–40%",  "50–65%"],
        ["1",  "AI Roadmap Planner",         "30–45%",  "40–55%"],
        ["2",  "AI Design Reviewer",         "50–65%",  "35–45%"],
        ["2",  "AI ADR Generator",           "40–55%",  "60–75%"],
        ["3",  "ReviewAgent",               "65–75%",  "35–45%"],
        ["3",  "AI PR Summariser",           "30–50%",  "25–35%"],
        ["4",  "AI Build Optimiser",         "40–60%",  "20–30%"],
        ["4",  "AI Pipeline Orchestrator",   "55–70%",  "30–40%"],
        ["5",  "AI UAT Assistant",           "75–85%",  "75–85%"],
        ["5",  "AI Test Generator",          "60–75%",  "65–80%"],
        ["5",  "AI Perf Analyser",           "55–70%",  "70–80%"],
        ["5",  "AI Test Data Manager",       "50–65%",  "60–75%"],
        ["6",  "AI Release Manager",         "60–70%",  "55–65%"],
        ["6",  "AI Change Risk Assessor",    "65–75%",  "50–60%"],
        ["7",  "AI Observability Agent",     "55–70%",  "45–60%"],
        ["7",  "AI Incident Classifier",     "50–65%",  "40–55%"],
        ["X",  "AI VSM Analyser",            "N/A",     "80–90%"],
        ["X",  "AI Requirements Analyst",   "40–55%",  "55–70%"],
        ["X",  "AI Coach",                  "N/A",     "25–35%"],
    ],
    col_widths=[0.5, 2.2, 1.7, 1.7]
)

h2("Appendix C — Glossary")
terms = [
    ("ADLC",    "AI-Driven Lifecycle — Option C: AI agents replace most manual PDLC gates"),
    ("ALM",     "Application Lifecycle Management — Jira, Azure DevOps, Rally"),
    ("DORA",    "DevOps Research & Assessment — 4-metric software delivery performance framework"),
    ("FE%",     "Flow Efficiency — PT / (PT+WT) × 100. World-class = >40%"),
    ("GenAI",   "Generative AI — LLM-based agents that produce code, text, or test cases"),
    ("HITL",    "Human-in-the-Loop — AI-assisted decision where human retains final approval"),
    ("LangGraph","Framework for building multi-agent AI pipelines (used by this platform)"),
    ("Lead Time","(PT + WT) / 8 — total calendar days from ticket creation to production"),
    ("MTTR",    "Mean Time To Recover — DORA metric: avg hours to restore after production incident"),
    ("PDLC",    "Product Development Lifecycle — 7-phase flow from ideation to monitoring"),
    ("RAG",     "Retrieval-Augmented Generation — AI using uploaded documents to personalise output"),
    ("ROI",     "Return on Investment — total benefits / total investment cost"),
    ("SAST",    "Static Application Security Testing — automated code vulnerability scanning"),
    ("UAT",     "User Acceptance Testing — business validation that a feature meets requirements"),
    ("VSM",     "Value Stream Map — visual map of all PDLC steps showing PT, WT, and FE%"),
    ("Wait Time","Hours a work item is blocked, queued, or waiting — non-value-adding time"),
]

add_table(
    ["Term", "Definition"],
    terms,
    col_widths=[1.3, 5.2]
)

# SAVE
output = "PDLC-VSM-Platform-Training-Material.docx"
doc.save(output)
print(f"✓ Saved: {output}")
