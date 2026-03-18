"""
Build: Live Demo Guide — Word Document
Output: US-Bank-Live-Demo-Guide.docx
Converts the LIVE-DEMO-GUIDE.md into a formatted Word document
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY   = RGBColor(0x0F, 0x2D, 0x5E)
BLUE   = RGBColor(0x25, 0x63, 0xEB)
TEAL   = RGBColor(0x0D, 0x94, 0x88)
AMBER  = RGBColor(0xD9, 0x77, 0x06)
RED    = RGBColor(0xDC, 0x26, 0x26)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
GRAY   = RGBColor(0x4B, 0x55, 0x63)
DGRAY  = RGBColor(0x37, 0x41, 0x51)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

doc = Document()
section = doc.sections[0]
section.page_width    = Inches(8.5)
section.page_height   = Inches(11)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)
section.top_margin    = Inches(0.9)
section.bottom_margin = Inches(0.9)

def sf(run, size=11, bold=False, italic=False, color=None, name='Calibri'):
    run.font.name  = name
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    if color: run.font.color.rgb = color

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
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

def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(5)
    r = p.add_run(text)
    sf(r, size=11, color=GRAY)
    return p

def instruction_box(text):
    """Light blue box for presenter instructions"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.3)
    p.paragraph_format.right_indent = Inches(0.3)
    r = p.add_run(text)
    sf(r, size=11, italic=True, color=BLUE)
    return p

def talking_point(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.3)
    r1 = p.add_run('TALKING POINT:  ')
    sf(r1, size=10, bold=True, color=GREEN)
    r2 = p.add_run(text)
    sf(r2, size=11, italic=True, color=DGRAY)
    return p

def bullet(text, bold_prefix=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix + ' ')
        sf(r1, size=11, bold=True, color=NAVY)
    r2 = p.add_run(text)
    sf(r2, size=11, color=GRAY)
    return p

def code_block(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.4)
    r = p.add_run(text)
    sf(r, size=9, name='Courier New', color=RGBColor(0x1E, 0x40, 0xAF))
    return p

def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run('─' * 95)
    sf(r, size=8, color=RGBColor(0xD1, 0xD5, 0xDB))

def add_tbl_row(table, cells, header=False, alt=False):
    row = table.add_row()
    for i, txt in enumerate(cells):
        cell = row.cells[i]
        cell.text = txt
        for para in cell.paragraphs:
            for run in para.runs:
                sf(run, size=10, bold=header, color=WHITE if header else GRAY)
        if header:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), '0F2D5E')
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)
        elif alt:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), 'EFF6FF')
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)
    return row

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(30)
r = p.add_run('LIVE DEMO GUIDE')
sf(r, size=34, bold=True, color=NAVY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run('PDLC VSM Platform')
sf(r, size=22, bold=True, color=BLUE)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
r = p.add_run('US Bank  |  Team Phoenix  |  Payments & Transfers')
sf(r, size=16, color=TEAL)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
r = p.add_run('─' * 55)
sf(r, size=10, color=RGBColor(0xD1, 0xD5, 0xDB))
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(10)
lines = [
    ('Platform URL: ', True, NAVY),
    ('http://localhost:3001', False, BLUE),
    ('     Demo Duration: ', True, NAVY),
    ('35–45 min (full) | 15–20 min (exec highlight)', False, GRAY),
]
for text, bold, color in lines:
    r = p.add_run(text)
    sf(r, size=12, bold=bold, color=color)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
r = p.add_run('March 2026  ·  Confidential — Presenter Use Only')
sf(r, size=11, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
# BEFORE YOU START
# ══════════════════════════════════════════════════════════════════════════════
h1('Before You Start')

body('Ensure all services are running before the demo begins:')
code_block('# Start backend (terminal 1)')
code_block('cd /Users/125066/projects/pdlc-vsm-platform')
code_block('source backend/venv/bin/activate')
code_block('python -m uvicorn backend.main:app --reload --port 8001')
code_block('')
code_block('# Start frontend (terminal 2)')
code_block('cd frontend && npm run dev   # opens on :3001')

body('Open a fresh browser at http://localhost:3001. Have this guide in a second window for copy-paste. Prepare the CSV file and document texts below (each document is in its own section).')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1: ALM CONNECT
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 1 — ALM Connect')
instruction_box('Navigate to: http://localhost:3001/alm-connect')
body('Tell the story: "First, we tell the platform who we are and where our data lives."')

h2('Sub-Step 1a: Project Setup')
body('Enter these exact values in the Project Setup form:')

tbl = doc.add_table(rows=1, cols=2)
tbl.style = 'Table Grid'
add_tbl_row(tbl, ['Field', 'Value to Enter'], header=True)
ps = [
    ['Project Name',   'US Bank — Digital Banking Platform'],
    ['Organization',   'US Bank'],
    ['Portfolio',      'Digital Banking'],
    ['Product Group',  'Payments & Transfers'],
    ['Product Team',   'Team Phoenix'],
    ['Industry',       'Banking & Financial Services'],
]
for i, r in enumerate(ps):
    add_tbl_row(tbl, r, alt=(i % 2 == 0))
doc.add_paragraph()
body('Click "Next: Connect ALM Tool →"')

h2('Sub-Step 1b: ALM Connection')
h3('Option A — Live Jira Connection')
body('Click the 🔵 Jira tile, then enter:')
tbl2 = doc.add_table(rows=1, cols=2)
tbl2.style = 'Table Grid'
add_tbl_row(tbl2, ['Field', 'Value'], header=True)
jira = [
    ['Instance URL',       'https://usbank-digital.atlassian.net'],
    ['Username / Email',   'phoenix-svc@usbank.com'],
    ['API Token',          'ATATTxxxxxxxxxxxxxxx (use real token or demo mode)'],
    ['Project Key',        'PHOE'],
]
for i, r in enumerate(jira):
    add_tbl_row(tbl2, r, alt=(i % 2 == 0))
doc.add_paragraph()
body('Click "🔌 Test Connection". If the demo environment does not have Jira access, use Option B below.')

h3('Option B — CSV Upload (Recommended for Demo)')
body('Click the 📄 CSV / Manual tile. Click "📥 Fetch & Map to VSM →" — the platform will use sample data and display the Data Preview. Alternatively, save the CSV data below as team-phoenix-jira-export.csv.')

h2('Synthetic Jira Export CSV')
body('Save the following content as team-phoenix-jira-export.csv and reference it in the platform:')

csv_content = """phase,activity,process_time_hrs,wait_time_hrs,lead_time_days,cycle_time_hrs,team,tool,notes
Backlog & Roadmap,Product Discovery & OKR Alignment,8,24,4.0,32,Product Owner,Confluence,"Quarterly OKR alignment"
Backlog & Roadmap,Feature Definition & User Stories,12,16,3.5,28,Product Owner + BA,Jira,"Story writing + AC. Avg 2.5 review cycles."
Backlog & Roadmap,Backlog Grooming & Estimation,6,16,2.8,22,Team Phoenix,Jira,"Bi-weekly grooming. Multiple re-estimation cycles."
Backlog & Roadmap,Sprint Planning,5,16,2.7,21,Team Phoenix,Jira,"Blocked by unresolved dependencies."
Architecture & UX Design,Architecture Review Board,8,72,10.0,80,Principal Architect,Confluence,"ARB meets fortnightly. 72h queue."
Architecture & UX Design,API Contract Design,12,40,6.5,52,Tech Lead,Postman,"Requires Integration team approval."
Architecture & UX Design,UX Design & Prototyping,16,24,5.0,40,UX Designer,Figma,"3 revision cycles per feature avg."
Architecture & UX Design,Security Architecture Review,8,40,6.0,48,CISO Team,Jira,"PCI-DSS review. 40-hour CISO SLA."
Code Management,Feature Development,8,4,1.5,12,Dev Team (3),GitHub,"Active coding time. Well-understood work."
Code Management,Code Review & PR Approval,4,18,2.8,22,Senior Engineers,GitHub,"2 senior approvals required. 18h median. 847-line avg PR."
Code Management,Branch Merge & Conflict Resolution,1,4,0.6,5,Dev Team,GitHub,"Merge conflicts common — long-lived branches."
Continuous Integration,CI Pipeline Execution,0.4,0.1,0.06,0.5,DevOps (Automated),GitHub Actions,"24 min avg. 12 min = dependency download."
Continuous Integration,Static Analysis & SAST,0.3,0.2,0.06,0.5,DevOps (Automated),SonarQube,"Quality gate. 23% first-run failure rate."
Continuous Integration,Build Artefact Publishing,0.2,0.1,0.04,0.3,DevOps (Automated),JFrog Artifactory,"Artefact versioning and registry push."
Continuous Integration,Environment Promotion (Dev→SIT),0.5,6,0.8,6.5,DevOps,Kubernetes,"6h promotion queue. Shared SIT cluster."
Continuous Testing,Automated Regression Test Suite,4,8,1.5,12,QA Automation,Selenium,"62% coverage. Sequential execution."
Continuous Testing,Manual SIT Testing,16,12,3.5,28,QA Team (4),Jira,"Manual testing of complex payment flows."
Continuous Testing,Performance / Load Testing,6,8,1.75,14,Performance Team,JMeter,"Separate team. 8h queue for slot."
Continuous Testing,Penetration Testing (PCI-DSS),0,40,5.2,40,External Security Team,Manual,"Mandatory PCI-DSS. SecureWorks. 5.2-day avg."
Continuous Testing,UAT Sign-off,8,20,3.5,28,BA + PO,Jira,"Business stakeholder UAT sign-off."
Continuous Delivery,CAB Submission & Review,2,48,6.0,50,Release Manager,ServiceNow,"CAB meets Tuesday. 48h notice. 3 VP approvals."
Continuous Delivery,Pre-Production Smoke Test,2,8,1.25,10,DevOps + QA,Automated + Manual,"Manual verification of critical payment paths."
Continuous Delivery,Production Deployment,0.5,80,10,80.5,Release Team,Kubernetes,"Wed release window only. Blackout Thu–Mon."
Continuous Delivery,Post-Deployment Verification,1,8,1.1,9,DevOps,Datadog,"Manual sign-off from Release Manager."
Monitoring & Feedback,Incident Detection & Alerting,0,3,0.4,3,DevOps (Automated),PagerDuty,"MTTD 3h. 340 false positives/month."
Monitoring & Feedback,Incident Triage & Root Cause,2,8,1.25,10,On-call Engineers,PagerDuty + Datadog,"Manual log analysis. No AI-assisted RCA."
Monitoring & Feedback,Incident Resolution & Hotfix,4,46,6.2,50,Dev Team + DBA,GitHub + PagerDuty,"DBA: Mon–Fri 8am–6pm only. After-hours wait."
Monitoring & Feedback,Post-Mortem & Feedback Loop,2,8,1.25,10,Team Phoenix,Confluence,"Monthly post-mortem. Findings rarely fed back."""

for line in csv_content.strip().split('\n'):
    code_block(line)

h2('Sub-Step 1c: Data Preview')
body('The platform displays:')
tbl3 = doc.add_table(rows=1, cols=2)
tbl3.style = 'Table Grid'
add_tbl_row(tbl3, ['Metric', 'Value'], header=True)
dp = [['Avg Lead Time', '42.5 days'], ['Flow Efficiency', '8.1%'], ['Total Effort', '94 hrs']]
for r in dp: add_tbl_row(tbl3, r)
doc.add_paragraph()
body('Click "View Current State VSM →"')
talking_point('"8.1% flow efficiency means 91.9% of the time a feature spends in the pipeline is pure waste. The industry average for banking is 10–15%. Elite performers hit 40%+."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2: DORA ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 2 — DORA Assessment')
instruction_box('Navigate to: http://localhost:3001/dora-assessment')
body('"Now we layer in DORA metrics — the industry\'s gold standard for software delivery performance."')

h2('Option A — Use the AI Demo Loader (Fastest)')
body('Click the "⚡ Load US Bank Demo Data" button at the top of the page. This pre-fills all 10 metrics AND loads AI Auto-Score notes. Then click "🤖 Show AI Notes" to expand the analysis panel.')

h2('Option B — Manual Entry')
h3('Core 4 DORA Metrics')
tbl4 = doc.add_table(rows=1, cols=3)
tbl4.style = 'Table Grid'
add_tbl_row(tbl4, ['Metric', 'Value', 'DORA Band'], header=True)
dora = [
    ['Deployment Frequency',    'Once per week',  'Medium'],
    ['Lead Time for Changes',   '1–2 weeks',      'Medium'],
    ['Change Failure Rate',     '12 (%)',          'Medium'],
    ['Mean Time to Restore',    '1–7 days',        'Medium'],
]
for r in dora: add_tbl_row(tbl4, r)
doc.add_paragraph()

h3('Extended Metrics')
tbl5 = doc.add_table(rows=1, cols=3)
tbl5.style = 'Table Grid'
add_tbl_row(tbl5, ['Metric', 'Value', 'Notes'], header=True)
ext = [
    ['Avg CI Build Duration',     '24 minutes',  'Above elite benchmark of <10 min'],
    ['Code Review Cycle Time',    '18 hours',    'Median PR-open to merge-approved'],
    ['Automated Test Coverage',   '62 %',        'Below 80% quality gate target'],
    ['Mean Time to Detect (MTTD)','3 hours',     'Alert fatigue — false positives'],
    ['% Tests Automated',         '55 %',        '45% still manual'],
    ['Infra Automation (IaC)',     '45 %',        'Legacy monolith partially migrated'],
]
for r in ext: add_tbl_row(tbl5, r)
doc.add_paragraph()

body('Expected result: Profile = Medium Performer (amber badge). VSM Recommendation: Option A or B. Priority Phases: Testing (5), Release (6), Code Review (3).')

h2('AI Auto-Score Notes — Talking Points')

h3('Deployment Frequency (88% confidence)')
talking_point('"AI pulled this from the Jira Release Tracker and the CAB Meeting Schedule. The root cause isn\'t technical — it\'s the Change Advisory Board governance gate. Every deployment requires 48-hour advance notice and sign-off from the CTO, CISO, and Release Manager."')

h3('Change Failure Rate (94% confidence)')
talking_point('"94% confidence — our most reliable score. 12% failure rate: 47 deployment failures out of 392 total deployments. The AI traces the root cause to database migration scripts — 61% of failures. Click Accept."')

h3('Lead Time for Changes (91% confidence)')
talking_point('"The 9.4-day median breaks down as: Development 2.1d + Code Review 2.3d + CI/CD 0.5d + Mandatory PCI-DSS pen-testing 5.2d + CAB approval 3.4d. The pen-testing gate alone exceeds the High Performer lead time benchmark."')

h3('MTTR (82% confidence)')
talking_point('"2.3-day median MTTR driven by manual incident investigation, cross-team escalation, and DBA availability gaps. Friday evening DB incidents wait until Monday morning."')

body('After reviewing all notes: click "✅ Accept All", then "Apply DORA Calibration to VSM →".')
talking_point('"The AI scores against evidence, shows you the source document and finding, explains the root cause — but you make the final call. This ensures the roadmap is grounded in your actual data."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3: CURRENT STATE VSM
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 3 — Current State VSM')
instruction_box('Navigate to: http://localhost:3001/current-vsm')

h2('Phase-by-Phase Walkthrough')
tbl6 = doc.add_table(rows=1, cols=5)
tbl6.style = 'Table Grid'
add_tbl_row(tbl6, ['Phase', 'PT (hrs)', 'WT (hrs)', 'FE', 'Key Bottleneck'], header=True)
vsm = [
    ['1. Backlog & Roadmap',      '31',  '72',   '30%', 'Quarterly planning cadence'],
    ['2. Architecture & UX',      '36',  '176',  '17%', 'ARB queue + PCI-DSS review'],
    ['3. Code Management',        '13',  '18',   '42%', 'PR review wait 18h median'],
    ['4. CI',                     '2',   '6.5',  '24%', '24-min build + SIT queue'],
    ['5. Testing',                '34',  '88',   '28%', 'Pen-test gate 5.2 days'],
    ['6. Delivery',               '8',   '144',  '5%',  'CAB + Wed-only release window'],
    ['7. Monitoring',             '6',   '96',   '6%',  'MTTR 2.3 days, DBA hours'],
    ['TOTAL',                     '130', '600',  '8.1%',''],
]
for r in vsm: add_tbl_row(tbl6, r)
doc.add_paragraph()
talking_point('"Phase 6 — Continuous Delivery — has a 5% flow efficiency. For every 1 hour of actual deployment work, the feature sits waiting for 18 hours. The Wednesday-only release window is the biggest single contributor to lead time in the entire pipeline."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 4: VSM EDITOR
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 4 — VSM Editor')
instruction_box('Navigate to: http://localhost:3001/vsm-editor')

bullet('Click "Phase 6: Continuous Delivery" to expand it', 'Click:')
bullet('Show the activity breakdown — point to "Production Deployment: 0.5h PT / 80h WT"', 'Show:')
bullet('Click the edit icon on "Production Deployment"', 'Click:')
talking_point('"80 hours of wait time — that\'s the Wednesday release window. The actual deployment takes 30 minutes but waits 3+ days for the next window. This is the single highest-impact item to fix."')
bullet('Now show Phase 5 (Testing) — point to the pen-test gate: 0h PT / 40h WT', 'Then:')
talking_point('"Zero hours of process time. Purely waiting for an external vendor. AI-assisted DAST scanning could replace this for lower-risk changes."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 5: BOTTLENECK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 5 — Bottleneck Analysis')
instruction_box('Navigate to: http://localhost:3001/bottlenecks')

tbl7 = doc.add_table(rows=1, cols=4)
tbl7.style = 'Table Grid'
add_tbl_row(tbl7, ['Rank', 'Bottleneck', 'WT Saved', 'Severity'], header=True)
bns = [
    ['1', 'CAB/Release Window Gate (Phase 6)',       '128h', 'Critical'],
    ['2', 'Mandatory Pen-Testing Gate (Phase 5)',    '40h',  'Critical'],
    ['3', 'Architecture Review Board Queue (Ph 2)',  '72h',  'High'],
    ['4', 'PR Code Review Wait (Phase 3)',           '18h',  'High'],
    ['5', 'Sequential Test Execution (Phase 5)',     '28h',  'High'],
    ['6', 'CI Build Duration — No Caching (Ph 4)',   '14h',  'Medium'],
    ['7', 'DBA Availability Gap (Phase 7)',          '24h',  'High'],
    ['8', 'Quarterly Planning Cadence (Phase 1)',    '48h',  'Medium'],
]
for r in bns: add_tbl_row(tbl7, r)
doc.add_paragraph()
talking_point('"If we solve just the CAB gate — implementing a risk-tiered deployment model — we reduce lead time by ~13 days. That\'s the single highest-leverage intervention."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 6: IMPROVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 6 — Improvements')
instruction_box('Navigate to: http://localhost:3001/improvements')

tbl8 = doc.add_table(rows=1, cols=4)
tbl8.style = 'Table Grid'
add_tbl_row(tbl8, ['#', 'Improvement', 'Timeline', 'Impact'], header=True)
imps = [
    ['1', 'Risk-tiered deployment model (eliminate CAB for low-risk)', 'Sprint 1–2', 'Lead time −13 days'],
    ['2', 'AI-assisted DAST/SAST replacing pen-test gate',             'Sprint 3–4', 'Lead time −5 days'],
    ['3', 'GitHub Copilot + AI PR reviewer',                           'Sprint 1',   'PR wait −12h'],
    ['4', 'Build caching + parallel test execution',                   'Sprint 2',   'Build time −14 min'],
    ['5', 'ARB self-service for standard patterns',                    'Sprint 3–4', 'ARB wait −48h'],
    ['6', 'Automated DB migration testing + rollback scripts',         'Sprint 2–3', 'CFR −6%'],
    ['7', 'AIOps incident detection + runbook automation',             'Sprint 5–6', 'MTTR −1.8 days'],
    ['8', 'Continuous planning (quarterly → rolling 6-week)',          'Sprint 3',   'Planning WT −40%'],
]
for r in imps: add_tbl_row(tbl8, r)
doc.add_paragraph()

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 7: FUTURE STATE VSM
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 7 — Future State VSM')
instruction_box('Navigate to: http://localhost:3001/future-state')

h2('All Options Comparison')
tbl9 = doc.add_table(rows=1, cols=5)
tbl9.style = 'Table Grid'
add_tbl_row(tbl9, ['Metric', 'Current', 'Option A', 'Option B', 'Option C (ADLC)'], header=True)
comp = [
    ['Lead Time',          '~42 days', '~18 days', '~10 days', '~3 days'],
    ['Flow Efficiency',    '8.1%',     '~30%',     '~44%',     '~62%'],
    ['Process Time',       '130h',     '65h',      '30h',      '8h'],
    ['Wait Time',          '600h',     '155h',     '38h',      '5h'],
    ['Agent Activities',   '0',        '8',        '18',       '26 of 28'],
]
for r in comp: add_tbl_row(tbl9, r)
doc.add_paragraph()

h2('Option A — Augmented PDLC')
body('Click the "Option A" tab. "Option A is the 6–12 month incremental path. Engineers still own every decision — AI assists."')
body('Click Phase 3 (Code Management) to expand activities: GitHub Copilot coding (hybrid), AI PR Reviewer (agent), Human approval (human). Phase 3 metrics: PT 8h, WT 6h, FE 57%.')

h2('Option B — Automated PDLC')
body('Click the "Option B" tab. "Testing and delivery are largely automated. Deployment shifts from weekly CAB batches to continuous delivery with automated risk gates."')
body('Click Phase 5 (Testing) to expand: AI DAST/SAST scanner (agent), Automated regression (agent), Risk scoring engine (agent), Human override for high-risk only (oversight).')

h2('Option C — ADLC (AI-Driven Lifecycle, BMAD Approach)')
body('Click the "Option C" tab. Point out the ADLC banner at top.')
talking_point('"Two human roles: Product Definer sets vision and OKRs. Product Builder supervises agents and holds the production gate. Everything else is handled by an orchestrated agent swarm."')

h3('ADLC Phase Walkthrough')
tbl10 = doc.add_table(rows=1, cols=3)
tbl10.style = 'Table Grid'
add_tbl_row(tbl10, ['ADLC Phase', 'What Happens', 'Human Role'], header=True)
adlc_walk = [
    ['1. Intent & Outcome Definition',       'OKRs + acceptance criteria → agent task spec',    'Product Definer (human)'],
    ['2. Autonomous Architecture & Design',  'Architecture Agent generates design + API contracts', 'Product Builder reviews'],
    ['3. Agentic Code Generation',           'Code swarm writes, tests, refactors in parallel',  'Product Builder quality gate'],
    ['4. Autonomous Integration Pipeline',   'CI agents build, test, scan, publish',             'Automated — no human needed'],
    ['5. Continuous Quality Intelligence',   'QA agent: comprehensive coverage + quality report','Product Builder approves'],
    ['6. Zero-Touch Delivery',               'Deployment agent: deploy, smoke test, rollback',   'Product Builder production gate'],
    ['7. AIOps & Continuous Learning',       'Incident detect, RCA, remediate, learn',           'Escalation to Product Builder only'],
]
for r in adlc_walk: add_tbl_row(tbl10, r)
doc.add_paragraph()

body('Click Phase 3 (Agentic Code Generation) to expand. Show: Intent parsing (0.5h PT, 0h WT), Code generation (1.5h PT, 0h WT), AI peer review (0.5h PT, 0h WT), Product Builder gate (0.5h PT, 0.5h WT — only human touch).')
talking_point('"The only wait time is the Product Builder\'s oversight review. No approval queues. No ARB. No CAB. From intent to code-ready: 3 hours."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 8: BUSINESS CASE
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 8 — Business Case')
instruction_box('Navigate to: http://localhost:3001/business-case')

tbl11 = doc.add_table(rows=1, cols=2)
tbl11.style = 'Table Grid'
add_tbl_row(tbl11, ['Metric', 'Value'], header=True)
bc = [
    ['Team Size',                   '12 engineers'],
    ['Avg Fully-Loaded Cost',        '$180,000 / person / year'],
    ['Annual Engineering Cost',      '$2.16M'],
    ['Current Waste (% of time)',    '91.9%'],
    ['Recoverable Capacity (Opt B)', '~36% → $780K/year'],
    ['Estimated Tool Investment',    '$120K / year'],
    ['Net Annual Benefit',           '~$660K'],
    ['Estimated Payback Period',     '7–9 months'],
    ['3-Year NPV',                   '~$1.6M'],
]
for r in bc: add_tbl_row(tbl11, r)
doc.add_paragraph()
talking_point('"Beyond cost savings — the real business case is speed to market. Payment features currently take 42 days. With Option B: 10 days. With Option C: 3 days. In payments, speed is competitive advantage."')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 9: PLAYBOOK CONTEXT
# ══════════════════════════════════════════════════════════════════════════════
h1('STEP 9 — Playbook Context')
instruction_box('Navigate to: http://localhost:3001/playbook')

h2('Section 1: Team Profile')
tbl12 = doc.add_table(rows=1, cols=2)
tbl12.style = 'Table Grid'
add_tbl_row(tbl12, ['Field', 'Value'], header=True)
tp = [
    ['Team Name',        'Team Phoenix'],
    ['Organisation',     'US Bank'],
    ['Portfolio',        'Digital Banking'],
    ['Product Group',    'Payments & Transfers'],
    ['Team Size',        '12'],
    ['Current Roles',    'Product Owner, 3× Backend Dev (Java/Spring), 2× Frontend Dev (React), QA Lead, 2× QA Engineer, DevOps Engineer, Solution Architect, Business Analyst'],
    ['Seniority Mix',    'Mixed (2–5yr avg)'],
    ['Industry',         'Banking & Financial Services'],
]
for r in tp: add_tbl_row(tbl12, r)
doc.add_paragraph()

h2('Section 2: Technology Stack')
tbl13 = doc.add_table(rows=1, cols=2)
tbl13.style = 'Table Grid'
add_tbl_row(tbl13, ['Field', 'Value'], header=True)
ts = [
    ['Source Control',           'GitHub Enterprise'],
    ['CI/CD Platform',           'GitHub Actions'],
    ['Cloud Platform',           'Microsoft Azure'],
    ['ALM / Project Tool',       'Jira'],
    ['Primary Languages',        'Java / Spring Boot, React 18, Python (data pipelines)'],
    ['Monitoring / Observability','Datadog, PagerDuty, Splunk'],
    ['Testing Tools',            'Selenium, JUnit 5, Postman, JMeter'],
    ['Existing AI Licences',     'GitHub Copilot Enterprise (100 seats), Azure OpenAI API'],
]
for r in ts: add_tbl_row(tbl13, r)
doc.add_paragraph()

h2('Section 3: Budget & Procurement')
tbl14 = doc.add_table(rows=1, cols=2)
tbl14.style = 'Table Grid'
add_tbl_row(tbl14, ['Field', 'Value'], header=True)
bp = [
    ['Budget Available',         '$500K–$1M'],
    ['Procurement Complexity',   'Complex (4–8 weeks — committee)'],
    ['Hard Deadline',            'Must demonstrate measurable lead time reduction before Q2 2026 budget review'],
    ['Unused Licence Capacity',  'GitHub Copilot: 100 seats licensed, only 34 currently active'],
]
for r in bp: add_tbl_row(tbl14, r)
doc.add_paragraph()

h2('Section 4: Security & Compliance')
tbl15 = doc.add_table(rows=1, cols=2)
tbl15.style = 'Table Grid'
add_tbl_row(tbl15, ['Field', 'Value'], header=True)
sc = [
    ['Compliance Frameworks',  'PCI-DSS Level 1, SOC 2 Type II, APRA CPS 234, ISO 27001'],
    ['Change Approval Process','Full enterprise CAB (bi-weekly)'],
    ['Data Residency',         'National (same country only)'],
    ['AI / LLM Data Policy',   'Enterprise-only (Microsoft/Google/AWS)'],
]
for r in sc: add_tbl_row(tbl15, r)
doc.add_paragraph()

h2('Section 5: Org Culture & Change Readiness')
tbl16 = doc.add_table(rows=1, cols=2)
tbl16.style = 'Table Grid'
add_tbl_row(tbl16, ['Field', 'Value'], header=True)
cr = [
    ['Team Maturity',              'Performing (high trust, predictable delivery)'],
    ['Previous AI Attempts',       'Partial adoption (some tools in use)'],
    ['Detail on Previous Attempts','GitHub Copilot rolled out 6 months ago. Adoption: 34% of licensed seats. Engineers using it report 20–30% productivity improvement. Resistance from 2 senior engineers. No formal training program ran at rollout.'],
    ['Leadership Sponsorship',     'Active champion (senior leader publicly backing this)'],
    ['Training Time Available',    '2–4 hrs/week'],
    ['Change Management Support',  'Scrum Master / Agile Coach available'],
]
for r in cr: add_tbl_row(tbl16, r)
doc.add_paragraph()

h2('Section 6: Ways of Working')
tbl17 = doc.add_table(rows=1, cols=2)
tbl17.style = 'Table Grid'
add_tbl_row(tbl17, ['Field', 'Value'], header=True)
wow = [
    ['Development Methodology',    'Scrum'],
    ['Sprint Length',              '2 weeks'],
    ['Current Deploy Frequency',   'Weekly'],
    ['Release / Change Process',   'Manual CAB approval required'],
    ['Current Ceremonies',         'Daily standup (15 min), bi-weekly sprint review, bi-weekly retrospective, quarterly OKR check-in, monthly architecture forum'],
]
for r in wow: add_tbl_row(tbl17, r)
doc.add_paragraph()

h2('Section 7: Stakeholder Context')
tbl18 = doc.add_table(rows=1, cols=2)
tbl18.style = 'Table Grid'
add_tbl_row(tbl18, ['Field', 'Value'], header=True)
sk = [
    ['Key Sponsors',       'CTO (Michael Chen), Head of Digital Banking (Sarah Williams), CISO (James Okonkwo)'],
    ['Known Concerns',     '"AI will create compliance risk" (CISO), "GitHub Copilot hallucinations in production" (Engineering VP), "Previous automation created technical debt" (Architect)'],
    ['Success Criteria',   'Must reduce mean lead time from 42 days to <20 days within 6 months. Must not increase CFR. Must produce audit-ready compliance evidence automatically.'],
]
for r in sk: add_tbl_row(tbl18, r)
doc.add_paragraph()

divider()

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTS TO UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
h1('Documents to Upload — Full Content')
body('Paste the content of each document below into the corresponding document section of the Playbook Context page. Each document increases the AI playbook accuracy score.')

h2('Document 1: Org Chart / Team Roster')
instruction_box('Section: "Org Chart / Team Roster" — paste the following into the text area')
doc1_lines = [
    'US BANK — TEAM PHOENIX ROSTER',
    'Digital Banking Division | Payments & Transfers Product Group | Date: January 2026',
    '',
    'REPORTING STRUCTURE:',
    'Head of Digital Banking: Sarah Williams (VP)',
    '  └── Engineering Manager: David Park',
    '        ├── Team Phoenix (Reports to David Park)',
    '        │     ├── Product Owner: Jennifer Zhao',
    '        │     ├── Solution Architect: Marcus Thompson',
    '        │     ├── Business Analyst: Rachel Kim',
    '        │     ├── Scrum Master: Tom Bradley',
    '        │     ├── Backend Developer (Senior): James Liu [GitHub Copilot active]',
    '        │     ├── Backend Developer (Mid): Aisha Obi [GitHub Copilot inactive]',
    '        │     ├── Backend Developer (Mid): Carlos Mendez [GitHub Copilot active]',
    '        │     ├── Frontend Developer (Senior): Sophie Wang [GitHub Copilot active]',
    '        │     ├── Frontend Developer (Mid): Priya Sharma [GitHub Copilot inactive]',
    '        │     ├── QA Lead: Kevin O\'Brien',
    '        │     ├── QA Engineer: Laura Chen',
    '        │     └── DevOps Engineer: Raj Patel [GitHub Copilot active]',
    '  └── CISO Office (dotted line): James Okonkwo',
    '  └── DBA Team (shared services): Maria Gonzalez (Lead DBA)',
    '  └── Architecture Review Board: Robert Stern (fortnightly rotation)',
    '',
    'HEADCOUNT: 12 dedicated + 3 shared services (DBA, Security, ARB)',
    'LOCATION: Minneapolis HQ (in-person Mon/Tue, remote Wed-Fri)',
]
for line in doc1_lines:
    code_block(line)

h2('Document 2: Engineering Standards (excerpt key fields)')
instruction_box('Section: "Engineering Standards / Tech Playbook" — paste the following')
doc2_lines = [
    'US BANK DIGITAL BANKING — ENGINEERING STANDARDS v2.4',
    'Effective: January 2026',
    '',
    'SOURCE CONTROL: GitHub Enterprise | Branch: GitFlow | 2 approvals required',
    'CI/CD: GitHub Actions | SonarQube quality gate 80% (current: 62% — bypassed)',
    'CLOUD: Microsoft Azure (AKS, Azure SQL, Azure Service Bus, Azure Key Vault)',
    'IaC: Terraform 1.6+ (45% of infra automated)',
    'TESTING: JUnit 5, Selenium Grid (migrating Playwright Q2 2026), JMeter',
    'SECURITY: OAuth 2.0/JWT, Snyk, Trivy container scanning, OWASP ZAP (manual)',
    'OBSERVABILITY: Datadog (APM), Splunk (SIEM), PagerDuty (on-call)',
    '',
    'AI POLICY: GitHub Copilot Enterprise (approved). Azure OpenAI API (approved).',
    'RESTRICTION: No customer PII or PCI-DSS CHD to any AI API.',
    '',
    'KNOWN TECHNICAL DEBT:',
    '- Legacy Oracle DB: 3.2M lines, partial Azure SQL migration in progress',
    '- DB rollback scripts: missing for 34% of Liquibase changesets',
    '- Test coverage: 62% vs 80% standard (quality gate annotated to bypass)',
    '- Monorepo: full rebuild on any change (incremental build not configured)',
    '- Infra: 55% of SIT environment still manually provisioned',
]
for line in doc2_lines:
    code_block(line)

h2('Document 3: Tool & Licence Inventory (excerpt)')
instruction_box('Section: "Tool & Licence Inventory" — paste the following')
doc3_lines = [
    'US BANK TEAM PHOENIX — TOOL & LICENCE INVENTORY | January 2026',
    '',
    'GitHub Enterprise:        500 seats licensed, 487 active | $22,000/mo | Dec 2026',
    'GitHub Copilot Enterprise: 100 seats licensed, 34 active  | $3,900/mo  | Dec 2026',
    '  *** 66 UNUSED SEATS — $2,574/mo recoverable capacity ***',
    'Jira Software Cloud:      50 seats, 47 active | $4,700/mo | Mar 2026',
    'Confluence Cloud:         50 seats, 45 active | $2,300/mo | Mar 2026',
    'JFrog Artifactory:        Enterprise | $8,400/mo | Jun 2026',
    'SonarQube Enterprise:     Enterprise | $6,200/mo | Sep 2026',
    'Datadog Pro:              15 seats | $8,100/mo | Jun 2026',
    'PagerDuty:                20 seats, 18 active | $2,400/mo | Sep 2026',
    'Splunk SIEM:              Enterprise | $15,000/mo | Dec 2026',
    'Azure OpenAI API:         Pay-as-go | ~$1,200/mo',
    'Terraform Enterprise:     50 seats licensed, 8 active | $3,500/mo',
    '',
    'UNDERUTILISED: 66 Copilot seats, 42 Terraform seats, 4 Miro seats',
]
for line in doc3_lines:
    code_block(line)

h2('Documents 4–7 Summary')
body('For Documents 4–7, use the full content provided in the LIVE-DEMO-GUIDE.md file or copy from the relevant sections below. The full synthetic texts are available in the guide\'s document sections:')
bullet('Document 4: Security & Compliance Policy v3.2 — CISO-approved, PCI-DSS, CAB rules, AI data policy')
bullet('Document 5: Annual OKRs / Strategic Goals 2026 — lead time targets, DORA goals, Copilot adoption')
bullet('Document 6: DORA Metrics Report Q3–Q4 2025 — full data with source attribution')
bullet('Document 7: Sprint Retrospective Notes Sprints 24–25 — team pain points, action items')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# URLS TO PROVIDE
# ══════════════════════════════════════════════════════════════════════════════
h1('URLs to Provide')
body('Enter these URLs into URL fetch fields or document upload URL tabs to give the AI additional context:')
tbl19 = doc.add_table(rows=1, cols=3)
tbl19.style = 'Table Grid'
add_tbl_row(tbl19, ['Purpose', 'URL', 'What It Adds'], header=True)
urls = [
    ['DORA 2024 Report',           'https://dora.dev/research/2024/dora-report/',              'DORA benchmark bands for financial services'],
    ['DORA Metrics Guide',          'https://dora.dev/guides/dora-metrics-four-keys/',           'Metric definitions + scoring methodology'],
    ['GitHub Copilot Enterprise',   'https://docs.github.com/en/copilot/about-github-copilot/github-copilot-enterprise-overview', 'Tool capability context'],
    ['Azure OpenAI',                'https://learn.microsoft.com/en-us/azure/ai-services/openai/overview', 'AI deployment pattern context'],
    ['BMAD Method',                 'https://github.com/bmad-method/BMAD-METHOD',                'ADLC / Option C conceptual grounding'],
    ['GitHub Actions',              'https://docs.github.com/en/actions',                        'CI/CD capability baseline'],
    ['Terraform AzureRM',           'https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs', 'IaC automation context'],
]
for r in urls: add_tbl_row(tbl19, r)
doc.add_paragraph()

divider()

# ══════════════════════════════════════════════════════════════════════════════
# DEMO CHEAT SHEET
# ══════════════════════════════════════════════════════════════════════════════
h1('Demo Talking Track — Cheat Sheet')

h2('Quick Reference Numbers')
tbl20 = doc.add_table(rows=1, cols=5)
tbl20.style = 'Table Grid'
add_tbl_row(tbl20, ['Metric', 'Current', 'Option A', 'Option B', 'Option C'], header=True)
qr = [
    ['Lead Time',        '42 days',    '18 days',  '10 days',    '3 days'],
    ['Flow Efficiency',  '8.1%',       '30%',      '44%',        '62%'],
    ['DORA Band',        'Medium',     'High',     'High/Elite', 'Elite'],
    ['Deploy Freq',      '1×/week',    '3×/week',  'Daily',      'Continuous'],
    ['CFR',              '12%',        '8%',       '5%',         '3%'],
    ['MTTR',             '2.3 days',   '18 hours', '4 hours',    '1 hour'],
    ['Est. Net ROI/yr',  '—',          '$340K',    '$660K',      '$1.1M'],
]
for r in qr: add_tbl_row(tbl20, r)
doc.add_paragraph()

h2('Key Talking Points by Stage')
talking_point('Opening: "Team Phoenix delivers solid results on visible metrics. But the VSM reveals what dashboards hide: 91.9% of the time a feature spends in the pipeline is pure wait."')
talking_point('After DORA: "Medium performer — 41st percentile of financial services. Fintech competitors are deploying 50× faster. That gap compounds every week."')
talking_point('Showing Phase 6: "80 hours of wait time for a 30-minute deployment. The Wednesday release window is the single highest-impact item in the entire pipeline."')
talking_point('Before future state: "Option A gets us to High Performer. Option B puts us in the top 20% of financial services. Option C — the ADLC — makes us faster than most fintechs."')
talking_point('Option C close: "Two engineers. 26 AI agents. The future of software development is not replacing engineers — it\'s giving two engineers the leverage of twenty."')
talking_point('Business case close: "$660K net annual benefit. 7-month payback. The question is not whether to do this. The question is which option you start with."')

doc.add_paragraph()
p = doc.add_paragraph()
r = p.add_run('PDLC VSM Platform  ·  Live Demo Guide v1.0  ·  March 2026  ·  CONFIDENTIAL — Presenter Use Only')
sf(r, size=9, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.save('US-Bank-Live-Demo-Guide.docx')
print('✅  US-Bank-Live-Demo-Guide.docx created')
