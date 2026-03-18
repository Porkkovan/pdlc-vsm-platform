"""
Build: PDLC VSM Platform User Reference Guide — Word Document
Output: PDLC-VSM-Platform-User-Guide.docx
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
LGRAY = RGBColor(0xF3, 0xF4, 0xF6)

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
    p.paragraph_format.left_indent  = Inches(0.3 + level * 0.25)
    p.paragraph_format.space_after  = Pt(2)
    if bold_prefix:
        rb = p.add_run(bold_prefix + ": ")
        sf(rb, size=10.5, bold=True)
        r = p.add_run(text)
        sf(r, size=10.5)
    else:
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
    bottom.set(qn('w:color'), '2563EB')
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
p.paragraph_format.space_after  = Pt(6)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("PDLC VSM PLATFORM")
sf(r, size=28, bold=True, color=NAVY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("User Reference Guide")
sf(r, size=18, bold=True, color=BLUE)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("End-to-End Workflow — Inputs, Outputs & Interpretation")
sf(r, size=12, italic=True, color=GRAY)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("v1.0  |  March 2026")
sf(r, size=10, color=GRAY)

page_break()

# ═══════════════════════════════════════════════════════════════════
# HOW TO USE THIS GUIDE
# ═══════════════════════════════════════════════════════════════════
h1("How to Use This Guide")
body("This is a reference guide — keep it open while working in the platform. "
     "Each section maps to one platform page and answers: What do I enter here? "
     "Where does that input come from? What will the platform produce? How do I interpret the output?")

callout_box("Icon Legend", [
    "📥  INPUT — data, fields, or files you provide to the platform",
    "📤  OUTPUT — what the platform generates or displays",
    "⚙️   HOW IT WORKS — brief explanation of the underlying logic",
    "💡  TIP — best-practice advice",
    "⚠️   IMPORTANT — warnings about common mistakes",
], color=TEAL)

h2("The 9-Step Workflow")
body("The platform guides you through a structured journey from raw ALM data to an AI-powered transformation roadmap:")

add_table(
    ["Step", "Page", "Purpose", "Output"],
    [
        ["1", "ALM Connect",       "Connect data source, set project metadata",     "VSM snapshot (7 phases)"],
        ["2", "DORA Assessment",   "Score 4 DORA dimensions via AI + manual input", "DORA scores + VSM calibration values"],
        ["3", "Current State VSM", "View flow efficiency across 7 PDLC phases",     "Baseline VSM metrics"],
        ["4", "VSM Editor",        "Override phase/activity metrics for modelling", "What-if scenario overrides"],
        ["5", "Bottleneck Analysis","AI identifies top flow impediments",            "5-10 prioritised bottlenecks"],
        ["6", "Improvements",      "AI maps improvements to bottlenecks",           "36-agent improvement catalogue"],
        ["7", "Future State VSM",  "Model 3 transformation scenarios (A / B / C)",  "Future state metrics + AI narrative"],
        ["8", "Business Case",     "Financial model: ROI, payback, NPV",            "Investment proposal document"],
        ["9", "Playbook Context",  "Upload docs + URLs for personalised playbook",  "AI-generated implementation guide"],
    ],
    col_widths=[0.4, 1.3, 2.5, 2.3]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 1 — ALM CONNECT
# ═══════════════════════════════════════════════════════════════════
h1("Step 1 — ALM Connect")
body("URL: http://localhost:3001/alm-connect  |  Estimated time: 10–15 minutes")
divider()

h2("Purpose")
body("Set up your project and connect the platform to your team's ALM/ticketing system. "
     "This is the foundation — all subsequent VSM analysis derives from the data ingested here. "
     "You can connect Jira, Azure DevOps, Rally, or upload a CSV export.")

h2("📥 Input — Project Setup Form")
add_table(
    ["Field", "Description", "Source of Input", "Example Value", "Required?"],
    [
        ["Project Name",  "Unique name for this VSM project",         "Create descriptive name",     "US Bank — Digital Banking Platform", "Yes"],
        ["Organization",  "Parent company or organisation name",      "Your company name",            "US Bank",                            "Yes"],
        ["Portfolio",     "Business portfolio this team belongs to",  "Org structure / PMO",          "Digital Banking",                    "Yes"],
        ["Product Group", "Product or system being analysed",         "Team's product name",          "Payments & Transfers",               "Yes"],
        ["Team Name",     "Scrum / engineering team name",            "Team's own name",              "Team Phoenix",                       "Yes"],
        ["Industry",      "Industry vertical",                        "Select from dropdown",         "Financial Services — Banking",       "Yes"],
    ],
    col_widths=[1.2, 1.8, 1.6, 1.8, 0.8]
)

h2("📥 Input — ALM Data Source")
add_table(
    ["Source Type",    "Connects To",                    "Data Extracted",                        "Auth Needed"],
    [
        ["Jira CSV Export",       "Jira Software / Jira Cloud",  "Tickets, sprints, cycle times, labels",  "None (file upload)"],
        ["Azure DevOps Export",   "Azure Boards",                 "Work items, iterations, states",         "None (file upload)"],
        ["CSV Upload",            "Any tool with CSV export",     "Configurable columns",                   "None (file upload)"],
        ["ServiceNow Export",     "ServiceNow ITSM",              "Changes, incidents, stories",            "None (file upload)"],
        ["Manual Entry",          "Platform form",                "Directly entered phase PT/WT",           "None"],
    ],
    col_widths=[1.5, 1.8, 2.3, 1.5]
)

h3("CSV Upload Format")
body("When using CSV Upload, your file must contain at minimum: ticket_id, type, status, and cycle_time_days. "
     "All other columns are optional but improve mapping accuracy.")
add_table(
    ["Column",              "Data Type", "Description",                        "Example",       "Required?"],
    [
        ["ticket_id",           "String",  "Unique ticket identifier",            "USB-2401",      "Yes"],
        ["type",                "Enum",    "Epic / Story / Bug / Task / Spike",   "Story",         "Yes"],
        ["title",               "String",  "Short description of work item",      "API Rate Limit","Yes"],
        ["sprint",              "String",  "Sprint or iteration identifier",      "Sprint-24",     "No"],
        ["status",              "Enum",    "Done / In Progress / To Do / Blocked","Done",          "Yes"],
        ["story_points",        "Integer", "Estimation points",                   "8",             "No"],
        ["cycle_time_days",     "Float",   "Total elapsed time ticket was open",  "12.5",          "Yes"],
        ["wait_time_days",      "Float",   "Time spent blocked / not in progress","9.0",           "No"],
        ["process_time_hours",  "Float",   "Active work hours only",              "24.0",          "No"],
        ["phase",               "String",  "PDLC phase (exact name)",             "Continuous Integration", "No"],
        ["assignee",            "String",  "Team member name",                    "James Wright",  "No"],
        ["created_date",        "Date",    "YYYY-MM-DD ticket creation date",     "2025-01-05",    "No"],
        ["completed_date",      "Date",    "YYYY-MM-DD ticket completion date",   "2025-01-17",    "No"],
    ],
    col_widths=[1.5, 0.9, 2.2, 1.5, 0.9]
)

callout_box("💡 Phase Name Mapping", [
    "If the 'phase' column is absent or blank, the platform auto-maps tickets to PDLC phases using ticket type and labels.",
    "Use these exact phase names for best results: Backlog & Roadmap, Architecture & UX, Code Management,",
    "Continuous Integration, Continuous Testing, Continuous Delivery, Monitoring & Feedback",
], color=TEAL)

h2("📤 Output — After Successful Connection")
bullet("Project record created with a unique Project ID (shown in header)")
bullet("Data preview table: ticket count, phase distribution, average cycle time")
bullet("ALM summary card: tool type, tickets ingested, date range covered")
bullet("Phase mapping preview: how tickets were bucketed across 7 PDLC phases")
bullet("VSM snapshot saved — ready for Current State VSM view")

h2("What Happens Next")
body("The platform automatically maps ticket data to the 7 PDLC phases and saves a VSM snapshot. "
     "Proceed to Step 2 (DORA Assessment) to calibrate phase metrics with your DORA performance data, "
     "or skip directly to Step 3 (Current State VSM) to view the baseline map.")

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 2 — DORA ASSESSMENT
# ═══════════════════════════════════════════════════════════════════
h1("Step 2 — DORA Assessment")
body("URL: http://localhost:3001/dora-assessment  |  Estimated time: 20–30 minutes")
divider()

h2("Purpose")
body("Score your team across 73 questions in 4 DORA dimensions. The AI pulls signals from connected data "
     "sources and auto-scores where possible, allowing manual override for qualitative dimensions. "
     "DORA scores generate calibration values that adjust VSM phase metrics for greater accuracy.")

h2("The 4 DORA Dimensions")
add_table(
    ["Dimension",               "# Questions", "What It Measures",                                   "Key Data Sources"],
    [
        ["Cultural Practices",      "18",  "Team autonomy, psychological safety, learning culture",   "Workshop / survey responses"],
        ["Measurement & Monitoring","20",  "Observability, alerting, SLO/SLA coverage, dashboards",  "Splunk, Datadog, Dynatrace, Grafana"],
        ["Process & Flow",          "18",  "Sprint cadence, WIP limits, deployment process, reviews", "Jira, Azure DevOps, GitHub Actions"],
        ["Technical Practices",     "17",  "CI/CD maturity, test automation %, code quality, security","GitHub, Jenkins, SonarQube, Snyk"],
    ],
    col_widths=[1.7, 0.9, 2.8, 2.1]
)

h2("📥 Input — Data Sources")
body("Add one or more data sources. The platform fetches metrics from each source to auto-score relevant questions.")
add_table(
    ["Source Type",  "URL Format",                                    "Metrics Auto-Scored"],
    [
        ["GitHub / GitLab / Bitbucket", "https://github.com/org/repo",              "PR size, review time, commit freq, coverage"],
        ["Jira",                         "https://org.atlassian.net/jira/projects/X", "Sprint velocity, cycle time, defect rate, WIP"],
        ["Splunk",                       "https://org.splunk.com/en-US/app/name",    "Alert volume, MTTR, deployment events"],
        ["SonarQube",                    "https://sonarqube.org/dashboard?id=X",     "Code coverage, technical debt, code smells"],
        ["PagerDuty",                    "https://app.pagerduty.com/services/XXX",   "Incident rate, MTTR, escalation rate"],
        ["Jenkins / GitHub Actions",     "https://jenkins.org/job/pipeline",         "Build success rate, build duration, frequency"],
        ["Confluence",                   "https://org.atlassian.net/wiki/spaces/X",  "Documentation coverage, runbook freshness"],
        ["Dynatrace",                    "https://env.live.dynatrace.com",           "SLO compliance, error rate, response time"],
    ],
    col_widths=[1.8, 2.5, 2.2]
)

h2("📥 Input — Manual Scoring Scale")
add_table(
    ["Score", "Label",      "Description",                                 "Example"],
    [
        ["1",  "Initial",   "Ad hoc, no defined process",                  "Deployments are manual, undocumented"],
        ["2",  "Managed",   "Some process exists but inconsistently applied","CI exists but not enforced on all branches"],
        ["3",  "Defined",   "Standardised and documented process",         "All PRs require CI green before merge"],
        ["4",  "Measured",  "Metrics tracked and reviewed regularly",      "Deployment frequency tracked in dashboard"],
        ["5",  "Optimising","Continuous improvement loop active",          "AI-driven auto-healing pipelines"],
    ],
    col_widths=[0.6, 1.0, 2.8, 2.1]
)

h2("📤 Output — DORA Score Report")
add_table(
    ["Output Field",               "Description",                                          "How to Use"],
    [
        ["Maturity Band",           "Elite / High / Medium / Low — overall classification","Compare to peers; set target band"],
        ["Dimension Scores (×4)",   "1–5 score per dimension",                             "Identify weakest dimension for focus"],
        ["73 Question Scores",      "Individual AI or manual score per question",          "Drill into specific capability gaps"],
        ["Benchmark Gap Table",     "Current vs. Elite / High targets per metric",         "Prioritise largest gaps"],
        ["phase3_wt",               "Code review wait time (hours) → Phase 3",            "Applied automatically to VSM Phase 3"],
        ["phase4_pt",               "CI build duration (hours) → Phase 4",                "Applied automatically to VSM Phase 4"],
        ["phase5_rework_factor",    "CFR-derived rework multiplier → Phase 5 PT",         "Applied automatically to VSM Phase 5"],
        ["phase6_wt",               "Deploy pipeline wait (hours) → Phase 6",             "Applied automatically to VSM Phase 6"],
        ["phase7_wt",               "MTTR (hours) → Phase 7",                             "Applied automatically to VSM Phase 7"],
        ["Top Action Items",        "3 AI-generated improvement actions per dimension",    "Feed into Step 6 (Improvements)"],
    ],
    col_widths=[1.8, 2.8, 1.9]
)

h2("DORA Band Reference")
add_table(
    ["Band",   "Deploy Freq",         "Lead Time",      "Change Failure Rate", "MTTR",     "Typical FE%"],
    [
        ["Elite",  "Multiple / day",      "< 1 hour",       "< 5%",                "< 1 hour", "> 40%"],
        ["High",   "Daily – weekly",      "1 day – 1 week", "5 – 10%",             "< 1 day",  "25 – 40%"],
        ["Medium", "Weekly – monthly",    "1 – 4 weeks",    "10 – 15%",            "1 – 7 days","15 – 25%"],
        ["Low",    "Less than monthly",   "> 1 month",      "> 15%",               "> 1 week", "< 15%"],
    ],
    col_widths=[0.7, 1.4, 1.3, 1.5, 1.0, 1.1]
)

callout_box("⚠️ Important", [
    "Always run DORA Assessment BEFORE viewing the Current State VSM. The calibration values",
    "generated here adjust phase metrics to reflect your team's actual DORA performance,",
    "producing a more accurate baseline than CSV data alone.",
], color=RED)

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 3 — CURRENT STATE VSM
# ═══════════════════════════════════════════════════════════════════
h1("Step 3 — Current State VSM")
body("URL: http://localhost:3001/vsm-current  |  Estimated time: 10–15 minutes to review")
divider()

h2("Purpose")
body("View the complete current-state value stream map — the picture of how work flows from idea to "
     "production across all 7 PDLC phases. Shows where time is spent on value-adding work (process time) "
     "versus waste (wait time) and where flow efficiency breaks down.")

h2("Reading the VSM — Visual Elements")
add_table(
    ["Visual Element",      "What It Represents",                       "How to Interpret"],
    [
        ["Phase card",          "One of the 7 PDLC phases",                 "Shows PT, WT, FE%, activity count"],
        ["FE% colour bar",      "Flow efficiency indicator per phase",      "Green >35%  |  Amber 15–35%  |  Red <15%"],
        ["Wait time arrow",     "Non-value-adding time between/within phases","Width proportional to hours of waste"],
        ["Process time bar",    "Active, value-adding work time",           "Blue fill — want this to dominate"],
        ["Timeline bar",        "Total lead time breakdown across phases",  "Bottom of diagram — key exec metric"],
        ["Summary metrics panel","Aggregate totals: PT, WT, LT, FE%",      "Top-right — first number executives ask for"],
    ],
    col_widths=[1.5, 2.4, 2.6]
)

h2("Key Metrics — Definitions & Formulas")
add_table(
    ["Metric",              "Formula",                        "Unit",   "What It Means",                     "World-Class Target"],
    [
        ["Process Time (PT)",   "Sum of active work hours",        "Hours",  "Value-adding time — work being done",    "Maximise"],
        ["Wait Time (WT)",      "Sum of non-active blocked time",  "Hours",  "Waste — blocked, waiting, queued",       "Minimise (<20% of LT)"],
        ["Lead Time (LT)",      "(PT + WT) / 8",                   "Days",   "Total elapsed calendar days",            "< 1 day (Elite)"],
        ["Flow Efficiency (FE%)","PT / (PT + WT) × 100",           "%",      "% of lead time spent on value work",     "> 40%"],
    ],
    col_widths=[1.5, 1.9, 0.6, 2.3, 1.2]
)

h2("The 7 PDLC Phases — Reference")
add_table(
    ["#", "Phase",                   "Description",                                         "Typical PT",  "Typical WT",  "Key WT Drivers"],
    [
        ["1", "Backlog & Roadmap",       "Ideation, epic writing, prioritisation, roadmap planning",   "20–40h", "40–120h",  "Stakeholder alignment, RAG reviews"],
        ["2", "Architecture & UX",       "Technical design, UX research, ADRs, design review",         "30–60h", "80–200h",  "Sequential reviews, limited availability"],
        ["3", "Code Management",         "Feature branch dev, peer code review, merge to trunk",        "10–20h", "10–30h",   "Large PR sizes, senior reviewer bottleneck"],
        ["4", "Continuous Integration",  "Build, unit test, static analysis, SAST scan",                "2–6h",   "4–12h",    "Build queue depth, flaky tests"],
        ["5", "Continuous Testing",      "SIT, UAT, NF testing, environment provisioning",              "20–50h", "100–300h", "Manual execution, environment setup, test data"],
        ["6", "Continuous Delivery",     "Release packaging, deployment pipeline, change approval",     "5–15h",  "20–80h",   "CAB approval, change freeze windows"],
        ["7", "Monitoring & Feedback",   "Production monitoring, incident response, feedback loops",    "4–10h",  "10–40h",   "Alert noise, incident triage delay"],
    ],
    col_widths=[0.3, 1.5, 2.2, 0.8, 0.8, 1.9]
)

h2("Benchmark Comparison Panel")
body("The right-side panel compares your current metrics against three benchmarks:")
bullet("Industry Median — typical for your sector (Financial Services, Healthcare, etc.)")
bullet("DORA High — performance expected of a High-band team")
bullet("DORA Elite — world-class performance targets")
body("Use the gap column (shown in red) to identify which phases are furthest from benchmark. "
     "These gaps directly feed into the Bottleneck Analysis prioritisation.")

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 4 — VSM EDITOR
# ═══════════════════════════════════════════════════════════════════
h1("Step 4 — VSM Editor")
body("URL: http://localhost:3001/vsm-editor  |  Estimated time: 10–20 minutes")
divider()

h2("Purpose")
body("Manually adjust phase and activity-level metrics to model 'what-if' scenarios. "
     "For example: 'What happens to overall flow efficiency if we reduce UAT wait time by 80% using AI test automation?' "
     "Overrides layer on top of ALM data without modifying the source data.")

h2("When to Use Overrides")
bullet("To model the impact of a specific improvement before committing to it")
bullet("To apply pilot results: e.g. 'our CI automation pilot reduced build wait from 8h to 1h'")
bullet("To correct metrics when ALM data is incomplete or inaccurate")
bullet("To show stakeholders a targeted 'micro future state' for a single phase")

h2("📥 Input — Override Fields")
add_table(
    ["Field",                 "What to Enter",                "Source of the Number",          "Example"],
    [
        ["Phase PT override",     "New process time (hours)",     "Pilot data or benchmark",       "48"],
        ["Phase WT override",     "New wait time (hours)",        "Pilot data or improvement ROI", "48"],
        ["Activity WT override",  "Wait time for one activity",   "Specific improvement target",   "8"],
        ["Activity PT override",  "Process time for one activity","Automation efficiency data",     "2"],
    ],
    col_widths=[1.7, 1.8, 2.2, 0.8]
)

h3("Phase 5 — Activity Breakdown Example")
add_table(
    ["Activity",                    "Default PT", "Default WT", "Notes"],
    [
        ["Test Planning & Preparation", "8h",  "16h",  "Sprint planning overhead"],
        ["Manual SIT Execution",        "12h", "120h", "Biggest bottleneck — manual env setup, no parallelism"],
        ["Manual UAT / NF Signoff",     "8h",  "80h",  "Business stakeholder scheduling constraint"],
        ["Automated Regression",        "6h",  "8h",   "Relatively efficient already"],
        ["Test Defect Triage",          "4h",  "16h",  "Dev team context-switching cost"],
        ["Test Report & Sign-off",      "2h",  "0h",   "Lightweight gate"],
    ],
    col_widths=[2.2, 0.9, 0.9, 2.5]
)

h2("📤 Output")
bullet("Real-time FE% recalculation after every edit (no save required)")
bullet("Before / After comparison panel for the edited phase")
bullet("Blue 'Override' badge on any phase with active overrides")
bullet("Updated total lead time and overall FE% in the summary panel")
bullet("Overrides auto-saved to the VSM snapshot and carry through to all downstream steps")

callout_box("💡 Tip — Undoing Overrides", [
    "Click the reset icon (↺) next to any overridden field to restore the original ALM value.",
    "Overrides are clearly labelled so stakeholders can distinguish actual vs. modelled data.",
], color=TEAL)

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 5 — BOTTLENECK ANALYSIS
# ═══════════════════════════════════════════════════════════════════
h1("Step 5 — Bottleneck Analysis")
body("URL: http://localhost:3001/bottlenecks  |  Estimated time: 5 minutes (AI runs automatically)")
divider()

h2("Purpose")
body("The AI analyses your VSM data to identify the top flow impediments — the specific activities causing "
     "the most waste. Each bottleneck includes severity rating, root cause explanation, lean waste classification, "
     "benchmark comparison, and competitor insights.")

h2("⚙️ How the AI Identifies Bottlenecks")
body("The bottleneck detection algorithm works in 5 steps:")
bullet("1. Calculate WT/PT ratio for every activity (high ratio = potential bottleneck)", level=0)
bullet("2. Compare activity WT against PDLC phase benchmarks from the knowledge base", level=0)
bullet("3. Assess phase FE% against industry median for your sector", level=0)
bullet("4. Compute severity: WT × (1 − FE%) × benchmark_gap_factor", level=0)
bullet("5. Generate root cause narrative (AI-generated or rule-based fallback)", level=0)

h2("📤 Output — Bottleneck Card Fields")
add_table(
    ["Field",             "Description",                                  "What to Look For"],
    [
        ["Phase",             "Which PDLC phase the bottleneck is in",        "Shows where in the flow the issue sits"],
        ["Activity",          "Specific activity within the phase",           "The exact process to target for improvement"],
        ["Severity",          "Critical / High / Medium / Low",               "Critical = address in next 90 days"],
        ["Wait Time",         "Hours of wait at this activity",               "Raw waste volume — input for ROI calc"],
        ["Process Time",      "Hours of active work at this activity",        "Numerator in the FE% fraction"],
        ["Flow Efficiency",   "PT / (PT + WT) × 100 for this activity",      "< 20% signals significant waste"],
        ["Root Cause",        "AI-generated explanation of why waste occurs", "Drives which type of agent to apply"],
        ["Lean Waste Type",   "DOWNTIME category (Waiting, Defects, etc.)",  "Frames the solution approach"],
        ["Benchmark Gap",     "How far below industry median this activity is","Quantifies improvement opportunity"],
        ["Competitor Insight","What similar organisations have achieved",     "Use as business case ammunition"],
    ],
    col_widths=[1.3, 2.2, 3.0]
)

h2("Severity Thresholds")
add_table(
    ["Severity", "WT Threshold",       "FE% Threshold", "Recommended Response"],
    [
        ["Critical", "> 150 hours OR",     "< 10%",         "Address within next 90 days — Quick Win focus"],
        ["High",     "50 – 150 hours OR",  "10 – 20%",      "Include in next quarter transformation planning"],
        ["Medium",   "20 – 50 hours OR",   "20 – 35%",      "Include in next half planning cycle"],
        ["Low",      "< 20 hours AND",     "> 35%",         "Monitor; address opportunistically"],
    ],
    col_widths=[0.9, 1.6, 1.3, 2.7]
)

h2("Lean Waste (DOWNTIME) Reference")
add_table(
    ["Letter", "Waste Type",        "Software Delivery Example",                  "Typical PDLC Phase"],
    [
        ["D",  "Defects",           "Production bugs, failed deployments, rework","Phase 5 — Testing"],
        ["O",  "Overproduction",    "Over-engineered features, unused APIs",      "Phase 1 — Backlog"],
        ["W",  "Waiting",           "Awaiting approvals, blocked tickets, queues","Phase 5, 6 — Testing/Delivery"],
        ["N",  "Non-used Talent",   "Manual tasks that could be automated",       "All phases"],
        ["T",  "Transport",         "Excessive ticket state transitions, handoffs","Phase 2, 3 — Architecture/Code"],
        ["I",  "Inventory",         "WIP backlog, untested features, open PRs",   "Phase 3 — Code Management"],
        ["M",  "Motion",            "Context-switching, tool-hopping, meetings",  "All phases"],
        ["E",  "Extra Processing",  "Redundant approvals, duplicate documentation","Phase 6 — Delivery"],
    ],
    col_widths=[0.6, 1.5, 2.6, 1.8]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 6 — IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════════
h1("Step 6 — Improvements")
body("URL: http://localhost:3001/improvements  |  Estimated time: 15 minutes to review and filter")
divider()

h2("Purpose")
body("The AI matches each identified bottleneck to the most appropriate AI agents and automation solutions "
     "from a catalogue of 36 pre-mapped improvements. Each recommendation shows effort reduction %, "
     "wait time reduction %, ROI estimate, and implementation hints including competitor evidence.")

h2("📥 Input — Available Filters")
add_table(
    ["Filter",          "Options",                                    "Purpose"],
    [
        ["Quick Wins",      "Yes / No toggle",                            "Show only improvements deliverable in <90 days"],
        ["Phase",           "Multi-select: any of 7 PDLC phases",         "Focus on one phase at a time"],
        ["Agent Type",      "GenAI / Agentic AI / Automation / HITL",    "Filter by technology complexity"],
        ["Min ROI",         "Slider: 1× – 5×",                           "Show only improvements above ROI threshold"],
        ["Source",          "Catalogue / Custom / Competitor",            "Catalogue = pre-validated benchmarks"],
    ],
    col_widths=[1.2, 2.2, 3.1]
)

h2("📤 Output — Improvement Card Fields")
add_table(
    ["Field",               "Description",                                        "Source",                     "How to Use"],
    [
        ["Activity",            "The bottleneck activity being addressed",            "From Step 5",                "Confirms linkage to identified waste"],
        ["Agent Name",          "Name of the AI agent or solution",                  "AI improvement catalogue",   "The solution to implement"],
        ["Agent Type",          "GenAI / Agentic AI / Automation / HITL",           "Catalogue classification",   "Informs build vs. buy decision"],
        ["Source",              "Catalogue / Custom / Competitor insight",           "Recommendation origin",      "Catalogue = pre-validated"],
        ["Effort Reduction %",  "% reduction in process time (FTE time saved)",      "Catalogue benchmarks",       "Input to capacity planning"],
        ["Wait Reduction %",    "% reduction in wait time for this activity",        "Catalogue benchmarks",       "Key driver of lead time improvement"],
        ["ROI Estimate",        "Return on investment multiple (e.g. 3.2×)",         "Financial model",            "Business case input"],
        ["Quick Win",           "✓ = deliverable in <90 days",                      "Complexity assessment",      "Prioritise for early momentum"],
        ["Competitor Insight",  "What similar teams have achieved",                  "Industry benchmarks DB",     "Use in executive presentations"],
        ["GenAI Recommendation","Specific prompt engineering or tool recommendation","LLM output",                 "Implementation starting point"],
    ],
    col_widths=[1.4, 2.0, 1.5, 1.6]
)

h2("The 36-Agent Catalogue — by Phase")
add_table(
    ["Phase", "Agents Available"],
    [
        ["Phase 1 — Backlog & Roadmap",      "AI Backlog Prioritiser, AI Epic Decomposer, AI Roadmap Planner, AI OKR Tracker"],
        ["Phase 2 — Architecture & UX",      "AI Design Reviewer, AI ADR Generator, AI UX Researcher, AI Tech Debt Analyser"],
        ["Phase 3 — Code Management",        "ReviewAgent, AI PR Summariser, AI Merge Conflict Resolver, AI Security Scanner"],
        ["Phase 4 — Continuous Integration", "AI Build Optimiser, AI Flaky Test Detector, AI Pipeline Orchestrator, AI SAST Analyser"],
        ["Phase 5 — Continuous Testing",     "AI UAT Assistant, AI Test Generator, AI Perf Analyser, AI Test Data Manager, AI NF Tester, AI Regression Selector"],
        ["Phase 6 — Continuous Delivery",    "AI Release Manager, AI Change Risk Assessor, AI Deployment Validator, AI Rollback Controller"],
        ["Phase 7 — Monitoring & Feedback",  "AI Observability Agent, AI Incident Classifier, AI Post-Incident Reviewer, AI SLO Manager"],
        ["Cross-Cutting",                    "AI VSM Analyser, AI Coach, AI Requirements Analyst, FeatureGen, AI Velocity Predictor, AI Cost Optimiser"],
    ],
    col_widths=[2.2, 4.3]
)

h2("ROI Calculation Method")
body("The platform uses this formula to estimate ROI:")
bullet("Annual Benefit = (FTE count × avg salary × effort_reduction% × phase_time%)")
bullet("             + (defects_reduced × defect_cost)")
bullet("             + (revenue_at_risk_per_day × LT_reduction_days)")
bullet("ROI = Annual Benefit / (Implementation Cost + Annual Licence Cost)")
body("Default assumptions: FTE salary $120K, defect cost $15K, revenue at risk $500K/day. "
     "These are editable in platform Settings and in the Business Case step.")

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 7 — FUTURE STATE VSM
# ═══════════════════════════════════════════════════════════════════
h1("Step 7 — Future State VSM")
body("URL: http://localhost:3001/vsm-future  |  Estimated time: 15 minutes to review all options")
divider()

h2("Purpose")
body("Model three transformation scenarios — Option A (conservative augmentation), Option B (hybrid intelligence), "
     "and Option C (AI-Driven Lifecycle / ADLC) — showing what the value stream looks like after implementing "
     "selected improvements. Enables trade-off comparison across investment, risk, and lead time reduction.")

h2("The Three Transformation Options")
add_table(
    ["Attribute",             "Option A — AI Augment",    "Option B — Hybrid Intel",  "Option C — ADLC"],
    [
        ["Horizon",               "12 months",                "18 months",                "24–36 months"],
        ["AI Agents Deployed",    "8",                        "15",                       "22+"],
        ["Flow Efficiency",       "~42%",                     "~61%",                     "~78%"],
        ["Lead Time Reduction",   "~57%",                     "~81%",                     "~93%"],
        ["Investment Range",      "$1.2M – $1.8M",            "$2.5M – $3.5M",            "$4M – $6M"],
        ["Risk Level",            "Low",                      "Medium",                   "High"],
        ["Team Change",           "Augmentation only",        "Hybrid human + AI",        "AI-first, 2 human roles"],
        ["DORA Target Band",      "High",                     "High → Elite",             "Elite"],
        ["Best For",              "Budget <$2M, low risk",    "Balanced transformation",  "Full transformation mandate"],
    ],
    col_widths=[1.8, 1.7, 1.8, 1.2]
)

h2("📤 Output — Per Option")
add_table(
    ["Output Field",           "Description",                                          "Use For"],
    [
        ["Future State VSM",       "Phase-by-phase FE%, PT, WT after improvements",       "Show the 'after' picture visually"],
        ["FE% per Phase",          "New flow efficiency for each of 7 phases",            "Identify which phases improve most"],
        ["Lead Time (days)",       "New total lead time in calendar days",                "Key exec metric — days to market"],
        ["AI Narrative",           "LLM-generated description of the transformation",     "Use verbatim in board presentations"],
        ["Agents Deployed",        "List of AI agents applied in this scenario",          "Feeds into implementation planning"],
        ["Investment Range",       "Estimated cost bracket for the scenario",             "First input to business case"],
        ["Risk Summary",           "Top 3 risk factors for this scenario",                "Inform risk register"],
        ["Phase Comparison Table", "Side-by-side current vs. future per phase",          "Show improvement per phase to engineers"],
    ],
    col_widths=[1.7, 2.6, 2.2]
)

h2("How Improvements Drive the Future State")
body("The future state is calculated by applying the wait_reduction% and effort_reduction% from each selected "
     "improvement card (Step 6) to the corresponding phase activities:")
bullet("GenAI agents: typically 30–50% WT reduction")
bullet("Agentic AI agents: 50–80% WT reduction")
bullet("Full automation: 70–90% WT reduction")
bullet("Human-in-the-Loop (HITL): 20–40% WT reduction (still requires human decision)")

h2("Talking to Executives About Future State")
add_table(
    ["Audience",       "Key Message",                                                       "Lead With"],
    [
        ["CTO",            "Option B deploys 15 AI agents reducing lead time by 81% in 18 months","Technical roadmap and agent architecture"],
        ["CFO",            "Option B delivers 4.2× ROI with 14-month payback on $3M investment", "ROI multiple and payback period"],
        ["Eng Manager",    "Option A Quick Wins reduce UAT wait by 80% in <90 days",             "Specific bottleneck elimination"],
        ["Product VP",     "Option B halves time-to-market from 42 days to 8 days",              "Speed-to-market competitive impact"],
    ],
    col_widths=[1.1, 3.6, 1.8]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 8 — BUSINESS CASE
# ═══════════════════════════════════════════════════════════════════
h1("Step 8 — Business Case")
body("URL: http://localhost:3001/business-case  |  Estimated time: 20 minutes to review and customise")
divider()

h2("Purpose")
body("Generate a detailed financial model for the selected transformation scenario. "
     "Quantifies investment, benefits across 5 streams, ROI multiple, payback period, and 5-year NPV. "
     "Designed to be shared directly with CFO and finance stakeholders.")

h2("📥 Input — Financial Assumptions")
add_table(
    ["Assumption",                     "Default Value",       "How to Customise",               "Impact on Model"],
    [
        ["Average FTE fully-loaded cost",  "$120,000 / year",     "Platform Settings",               "Labour savings calculation"],
        ["Team size",                       "From project metadata","Auto-populated from Step 1",      "Scale of savings"],
        ["Product revenue at risk (daily)", "$500,000",            "Business Case form input",         "Speed-to-market benefit"],
        ["Defect cost per incident",        "$15,000",             "Business Case form input",         "Quality improvement benefit"],
        ["Compliance fine risk (annual)",   "$2,000,000",          "Business Case form input",         "Risk reduction benefit"],
        ["Cloud/infra cost (monthly)",      "$50,000",             "Business Case form input",         "Platform cost avoidance"],
        ["Implementation cost multiplier",  "1.0×",               "Regional / complexity factor",     "Total investment"],
        ["Annual licence cost",             "$200,000",            "Per contract / pricing sheet",     "Ongoing cost"],
        ["NPV discount rate",               "8%",                  "Finance team input",               "5-year NPV"],
        ["Benefits start month",            "Month 6",             "Based on implementation timeline", "Payback calculation"],
        ["Year 1 benefits ramp",            "60% of full run-rate","Linear ramp assumption",           "Year 1 cash flow"],
        ["Scenario",                        "Base",                "Toggle: Conservative / Base / Optimistic","±25% on benefits"],
    ],
    col_widths=[2.2, 1.3, 1.8, 2.2]
)

h2("📤 Output — Business Case Report Sections")
h3("1. Executive Summary Box")
bullet("Recommended option and rationale")
bullet("Investment range (low–high bracket)")
bullet("ROI multiple (e.g. 4.2×)")
bullet("Payback period in months")
bullet("AI-generated one-paragraph executive narrative")

h3("2. Investment Breakdown Table")
bullet("Licensing costs — Year 1 and ongoing annual")
bullet("Implementation costs — platform integration, configuration, testing")
bullet("Change management and training — workshops, communications, enablement")
bullet("Infrastructure / cloud delta — net new costs for AI workloads")
bullet("Total Year 1 investment (midpoint of range)")

h3("3. Benefits by Stream (5 categories)")
add_table(
    ["Benefit Stream",         "Description",                                     "Typical Annual Range"],
    [
        ["Labour Savings",         "FTE time freed by automation — redeployable",    "$1M – $5M"],
        ["Quality Improvement",    "Defect reduction value and rework elimination",  "$500K – $2M"],
        ["Speed-to-Market",        "Revenue enabled by faster feature delivery",     "$1M – $8M"],
        ["Risk Reduction",         "Compliance incident and fine avoidance",         "$500K – $2M"],
        ["Platform Cost Avoidance","Legacy tool rationalisation and cloud savings",  "$200K – $1M"],
    ],
    col_widths=[1.8, 3.0, 1.7]
)

h3("4. Financial Summary Metrics")
add_table(
    ["Metric",             "Definition",                                                     "Where Used"],
    [
        ["ROI Multiple",       "Total 3-year benefits / Total 3-year investment",                "Board presentation"],
        ["Payback Period",     "Month in which cumulative benefits exceed cumulative investment", "CFO decision gate"],
        ["5-Year NPV",         "Net Present Value at discount rate (default 8%)",               "Finance committee approval"],
        ["Year 1 Benefits",    "First 12-month benefits (ramped)",                               "Budget cycle justification"],
        ["IRR",                "Internal Rate of Return for the investment",                     "Portfolio prioritisation"],
    ],
    col_widths=[1.5, 3.2, 1.8]
)

h3("5. Risk-Adjusted Scenarios")
bullet("Conservative (−25%): pessimistic benefits, 15% cost overrun assumed")
bullet("Base: as modelled with standard assumptions")
bullet("Optimistic (+25%): stretch benefits, on-time and on-budget delivery")

callout_box("💡 Exporting the Business Case", [
    "Use the 'Export PDF' button to generate a print-ready version for finance review.",
    "The executive summary text is AI-generated — edit it before sharing if needed.",
    "For the investment committee, pair the Business Case with the Option B Future State VSM slide.",
], color=TEAL)

page_break()

# ═══════════════════════════════════════════════════════════════════
# STEP 9 — PLAYBOOK CONTEXT
# ═══════════════════════════════════════════════════════════════════
h1("Step 9 — Playbook Context")
body("URL: http://localhost:3001/playbook  |  Estimated time: 15–20 minutes to upload context")
divider()

h2("Purpose")
body("Upload team-specific context documents and knowledge base URLs so the AI generates a personalised, "
     "compliance-aware implementation playbook — not a generic template. The more relevant context "
     "provided, the more specific and actionable the output.")

h2("📥 Input — Documents to Upload")
add_table(
    ["Document Type",           "Format",         "Purpose in Playbook",                        "Example Filename",                  "Priority"],
    [
        ["Team Charter",            "PDF/DOCX/TXT",   "Team structure, roles, responsibilities",    "team-phoenix-charter.txt",          "High"],
        ["DevOps Maturity Report",  "PDF/DOCX",       "Current capabilities and baseline",          "devops-assessment-q1-2025.pdf",     "High"],
        ["Compliance Framework",    "PDF/DOCX/TXT",   "Regulatory constraints on automation",       "ffiec-compliance-requirements.txt", "High (regulated)"],
        ["Architecture Standards",  "DOCX/TXT",       "API/security standards to follow",           "architecture-standards-v2.docx",    "High"],
        ["Sprint Retrospectives",   "TXT/DOCX",       "Team pain points and cultural signals",      "team-retro-q4-2025.txt",            "Recommended"],
        ["OKR / Strategy Doc",      "DOCX/TXT",       "Strategic alignment context",                "usbank-okr-2026.txt",               "Recommended"],
        ["DORA Benchmarks",         "PDF/TXT",        "Industry comparison data",                   "dora-report-2024.pdf",              "Recommended"],
        ["Previous Roadmaps",       "DOCX/PPT",       "What has / has not worked before",           "transformation-roadmap-2024.docx",  "Optional"],
        ["Job Descriptions",        "TXT",            "Skills available in team",                   "engineering-jd-2025.txt",           "Optional"],
    ],
    col_widths=[1.5, 0.9, 2.0, 2.0, 0.9]
)

h2("📥 Input — Knowledge Base URLs")
add_table(
    ["URL Purpose",                "What to Provide",                            "Playbook Uses It For"],
    [
        ["DORA Research",              "dora.dev/research/2024 URL",                 "Benchmark calibration and targets"],
        ["Methodology frameworks",     "Lean, SAFe, LeSS, or Scrum guide URLs",      "Methodology-specific recommendations"],
        ["Regulatory standards",       "FFIEC, PCI DSS, HIPAA, SOX links",           "Compliance-aware implementation steps"],
        ["Tool documentation",         "GitHub Actions, Jenkins, Jira admin guides",  "Integration and configuration specifics"],
        ["Industry case studies",      "Analyst reports, conference talks",           "Competitor benchmark evidence"],
        ["Architecture references",    "Cloud provider well-architected guides",      "Technical architecture recommendations"],
    ],
    col_widths=[1.7, 2.3, 2.5]
)

h2("📥 Input — Playbook Configuration")
add_table(
    ["Setting",             "Options",                                "Recommendation"],
    [
        ["Scenario",            "Option A / B / C",                       "Match your Business Case decision"],
        ["Regulatory Context",  "Regulated / Non-regulated",              "Always select Regulated for FSI/Healthcare"],
        ["Focus Areas",         "Phase 5 only / Phase 6 only / All",      "Select your Critical bottleneck phases"],
        ["Output Format",       "Roadmap / Sprint Plan / Executive Brief", "Roadmap for programme managers; Executive for CXO"],
    ],
    col_widths=[1.4, 2.4, 2.7]
)

h2("📤 Output — Playbook Structure")
h3("1. Executive Summary")
bullet("Scenario selected with rationale for the choice")
bullet("Top 5 transformation initiatives with estimated timelines")
bullet("Investment and ROI recap from Business Case")

h3("2. Phase-by-Phase Roadmap (for each of 7 phases)")
bullet("Current state: FE%, key bottlenecks, root causes")
bullet("Target state: FE% goal, agents to deploy, expected metrics")
bullet("Implementation steps: numbered, specific to your context")
bullet("Success metrics: measurable KPIs for each phase")
bullet("Timeline: quarter-by-quarter delivery plan")

h3("3. Agent Implementation Guide (per recommended agent)")
bullet("What it does and prerequisites (tools, APIs, skills needed)")
bullet("Integration guide: step-by-step connection to existing toolchain")
bullet("Effort estimate for implementation (person-days)")
bullet("How to measure success: leading and lagging indicators")

h3("4. Change Management Plan")
bullet("Stakeholder impact assessment by role")
bullet("Communication plan: messages, channels, timing")
bullet("Training requirements per engineering role")
bullet("Resistance factors and mitigation strategies")

h3("5. First 90 Days Sprint Plan")
bullet("Weeks 1–4: Foundation — infrastructure, access provisioning, team training")
bullet("Weeks 5–8: Quick Wins — deploy first 2–3 agents, measure baseline")
bullet("Weeks 9–12: Measure, learn, and expand to next 3–4 agents")

h2("How Context Changes the Playbook")
add_table(
    ["Document Uploaded",        "What Changes in the Playbook"],
    [
        ["Compliance framework",     "Adds HITL gates, audit trail requirements, regulatory sign-off steps"],
        ["Architecture standards",   "Aligns agent integration patterns to your existing API and security standards"],
        ["Team charter",             "Personalises role assignments, uses team member names"],
        ["Sprint retrospectives",    "References known pain points, avoids solutions that have previously failed"],
        ["DORA benchmarks",          "Calibrates targets to sector-specific norms rather than generic percentiles"],
        ["OKR document",             "Links each transformation initiative to a strategic objective"],
    ],
    col_widths=[1.8, 4.7]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# APPENDIX A — METRICS QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════
h1("Appendix A — Metrics Quick Reference")

h2("Core VSM Formulas")
add_table(
    ["Metric",              "Formula",                           "Unit"],
    [
        ["Flow Efficiency",     "PT / (PT + WT) × 100",              "%"],
        ["Lead Time",           "(PT + WT) / 8",                     "Days"],
        ["Process Time",        "Sum of all active work hours",       "Hours"],
        ["Wait Time",           "Sum of all blocked / queued hours",  "Hours"],
        ["WT/PT Ratio",         "WT / PT",                           "Ratio (lower = better)"],
        ["Phase FE%",           "Phase PT / (Phase PT + Phase WT) × 100", "%"],
    ],
    col_widths=[1.8, 2.8, 1.0]
)

h2("DORA Benchmarks — Financial Services")
add_table(
    ["Metric",                "Low",        "Medium",      "High",        "Elite"],
    [
        ["Deployment Frequency",  "< 1/month",  "1/week–1/month","Daily–weekly", "Multiple/day"],
        ["Lead Time for Change",  "> 6 months", "1–6 months",  "1 day–1 week", "< 1 hour"],
        ["Change Failure Rate",   "> 15%",      "10–15%",      "5–10%",        "< 5%"],
        ["MTTR",                  "> 1 week",   "1 day–1 week","< 1 day",      "< 1 hour"],
    ],
    col_widths=[1.8, 1.2, 1.3, 1.3, 1.3]
)

h2("Flow Efficiency Benchmarks by Industry")
add_table(
    ["Industry",          "Typical FE%", "World-Class FE%", "Notes"],
    [
        ["Financial Services",  "8–18%",   "35–45%",  "Regulatory approval gates depress FE; automate governance"],
        ["Healthcare / HIPAA",  "6–15%",   "30–40%",  "Compliance testing elongates Phase 5 and 6"],
        ["Retail / eCommerce",  "18–28%",  "45–60%",  "Fewer regulatory gates; higher automation opportunity"],
        ["Telecoms",            "10–20%",  "38–50%",  "Network change freezes add Phase 6 wait"],
        ["SaaS / Tech",         "20–35%",  "55–75%",  "CI/CD maturity highest; closest to Elite benchmarks"],
    ],
    col_widths=[1.7, 1.1, 1.3, 2.9]
)

page_break()

# ═══════════════════════════════════════════════════════════════════
# APPENDIX B — FREQUENTLY ASKED QUESTIONS
# ═══════════════════════════════════════════════════════════════════
h1("Appendix B — Frequently Asked Questions")

faqs = [
    ("Can I run the platform without a DORA Assessment?",
     "Yes — you can skip to Current State VSM directly after ALM Connect. "
     "However, without DORA calibration the VSM metrics will be based purely on ALM ticket data "
     "and may not accurately reflect your actual phase performance. Run DORA Assessment first for best results."),

    ("What if my CSV has no 'phase' column?",
     "The platform uses auto-mapping: it infers the PDLC phase from ticket type, labels, and workflow states. "
     "Jira tickets labelled 'architecture', 'design review' are mapped to Phase 2; CI/build tickets to Phase 4, etc. "
     "Review the phase distribution in the data preview and correct any obvious mis-mappings."),

    ("How long does the full AI analysis pipeline take?",
     "The full 8-agent pipeline typically completes in 2–5 minutes depending on VSM complexity. "
     "Individual agents (bottleneck, improvement, future state) run in under 60 seconds each. "
     "Progress is shown in the status bar. Without an OpenAI API key, rule-based fallbacks run instantly."),

    ("Can I have multiple projects for the same team?",
     "Yes — each project is independent. You can create quarterly snapshots for the same team "
     "to track maturity improvement over time. Name them consistently: e.g. 'Team Phoenix — Q1 2026'."),

    ("Why are my improvement ROI estimates different from what we expected?",
     "ROI is based on default assumptions (FTE salary $120K, defect cost $15K). "
     "Customise these in the Business Case step to match your actual costs. "
     "The effort/wait reduction percentages are catalogue benchmarks — adjust them to match your pilot evidence."),

    ("What does 'Quick Win' mean in Improvements?",
     "A Quick Win is an improvement that can be implemented and show measurable results in under 90 days. "
     "This typically means: low integration complexity, agent available off-the-shelf, no major change management required. "
     "Use Quick Wins to build momentum before longer horizon Option B/C initiatives."),

    ("Can I compare two different teams in the same view?",
     "Not currently — the platform is single-project per session. "
     "To compare teams, open separate browser tabs with different project IDs. "
     "Multi-team portfolio view is on the product roadmap."),

    ("Why is my Future State FE% lower than expected?",
     "Check that your VSM Editor overrides are saved (blue badge visible on phase cards). "
     "Also verify that improvements were not filtered out before running Future State analysis. "
     "The future state uses all active improvements by default — if filters are applied they narrow the input."),

    ("The bottleneck analysis returned 0 results — what went wrong?",
     "This usually means the VSM snapshot has no phase data. "
     "Verify that the Current State VSM shows 7 phases with non-zero PT and WT values. "
     "If all WT values are 0, the CSV data lacked wait_time_days — re-upload with wait time included."),

    ("How do I reset a project to start over?",
     "Navigate to ALM Connect, select the project, and click 'Reset Data'. "
     "This clears VSM snapshots and analysis runs but retains the project metadata. "
     "To delete the project entirely, use the project settings menu (gear icon in the header)."),
]

for q, a in faqs:
    h3(q)
    body(a)

page_break()

# ═══════════════════════════════════════════════════════════════════
# APPENDIX C — GLOSSARY
# ═══════════════════════════════════════════════════════════════════
h1("Appendix C — Glossary")

terms = [
    ("ADLC",           "AI-Driven Lifecycle — Option C transformation scenario where AI agents replace most manual PDLC gates"),
    ("ALM",            "Application Lifecycle Management — tools like Jira, Azure DevOps, Rally that track work items"),
    ("Agentic AI",     "AI that can take sequences of actions autonomously to complete multi-step tasks (e.g. AI Release Manager)"),
    ("Bottleneck",     "A specific activity where wait time significantly exceeds process time, impeding flow"),
    ("CAB",            "Change Advisory Board — governance committee that approves production changes; a common Phase 6 bottleneck"),
    ("CFR",            "Change Failure Rate — % of deployments that cause a production incident (DORA metric)"),
    ("Cycle Time",     "Total elapsed time from ticket creation to completion (includes all wait and process time)"),
    ("DORA",           "DevOps Research & Assessment — framework measuring software delivery performance across 4 metrics"),
    ("DOWNTIME",       "Lean waste mnemonic: Defects, Overproduction, Waiting, Non-used talent, Transport, Inventory, Motion, Extra processing"),
    ("FE%",            "Flow Efficiency — ratio of value-adding process time to total lead time, expressed as a percentage"),
    ("GenAI",          "Generative AI — AI that produces content (code, text, tests) from prompts; typically LLM-based"),
    ("HITL",           "Human-in-the-Loop — AI-assisted decision where a human retains final approval authority"),
    ("KPI",            "Key Performance Indicator — measurable metric used to evaluate progress against a target"),
    ("LangGraph",      "Open-source framework for building multi-agent AI pipelines; used by this platform's 8-agent orchestrator"),
    ("Lead Time",      "Total calendar days from work item creation to production deployment"),
    ("LT",             "Lead Time — see above"),
    ("MTTR",           "Mean Time To Recover — average time to restore service after a production incident (DORA metric)"),
    ("NPV",            "Net Present Value — present value of future cash flows discounted at a specified rate"),
    ("PDLC",           "Product Development Lifecycle — the end-to-end process from ideation to production monitoring"),
    ("Process Time",   "Hours of active, value-adding work performed on a ticket or feature (no waiting)"),
    ("PT",             "Process Time — see above"),
    ("Quick Win",      "An improvement deliverable and measurable in under 90 days with low implementation complexity"),
    ("RAG",            "Retrieval-Augmented Generation — AI technique that enhances LLM responses with retrieved knowledge"),
    ("ROI",            "Return on Investment — ratio of net benefit to total investment cost"),
    ("SAST",           "Static Application Security Testing — automated code analysis for security vulnerabilities"),
    ("SIT",            "System Integration Testing — formal testing of integrated system components before UAT"),
    ("SLO",            "Service Level Objective — agreed target for a service reliability metric"),
    ("UAT",            "User Acceptance Testing — business-facing validation that a feature meets requirements"),
    ("VSM",            "Value Stream Map — visual representation of all steps required to deliver value to a customer"),
    ("Wait Time",      "Hours spent blocked, queued, or waiting for an input — non-value-adding time"),
    ("WT",             "Wait Time — see above"),
]

add_table(
    ["Term", "Definition"],
    terms,
    col_widths=[1.5, 5.0]
)

# SAVE
output = "PDLC-VSM-Platform-User-Guide.docx"
doc.save(output)
print(f"✓ Saved: {output}")
