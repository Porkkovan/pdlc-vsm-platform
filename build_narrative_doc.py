"""
Build: US Bank — Detailed Narrative POV (Word Document)
Output: US-Bank-PDLC-VSM-Narrative-POV.docx
Storytelling format — takes reader through the full transformation journey
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── Colour palette ─────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0F, 0x2D, 0x5E)
BLUE   = RGBColor(0x25, 0x63, 0xEB)
TEAL   = RGBColor(0x0D, 0x94, 0x88)
AMBER  = RGBColor(0xD9, 0x77, 0x06)
RED    = RGBColor(0xDC, 0x26, 0x26)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
GRAY   = RGBColor(0x4B, 0x55, 0x63)
LGRAY  = RGBColor(0xF3, 0xF4, 0xF6)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

doc = Document()

# ── Page setup ─────────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Inches(8.5)
section.page_height = Inches(11)
section.left_margin   = Inches(1.1)
section.right_margin  = Inches(1.1)
section.top_margin    = Inches(1.0)
section.bottom_margin = Inches(1.0)

# ── Style helpers ──────────────────────────────────────────────────────────────
def set_font(run, name='Calibri', size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def heading1(text, color=NAVY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    set_font(run, size=18, bold=True, color=color)
    return p

def heading2(text, color=BLUE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    set_font(run, size=14, bold=True, color=color)
    return p

def heading3(text, color=TEAL):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    run = p.add_run(text)
    set_font(run, size=12, bold=True, color=color)
    return p

def body(text, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(6)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run(text)
    set_font(run, size=11, color=GRAY)
    return p

def body_bold_inline(parts):
    """parts = list of (text, bold) tuples"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(6)
    for text, bold in parts:
        run = p.add_run(text)
        set_font(run, size=11, bold=bold, color=GRAY)
    return p

def quote_block(text, attribution=''):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(8)
    p.paragraph_format.left_indent  = Inches(0.4)
    p.paragraph_format.right_indent = Inches(0.4)
    run = p.add_run(f'"{text}"')
    set_font(run, size=12, italic=True, color=BLUE)
    if attribution:
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.4)
        p2.paragraph_format.space_after = Pt(8)
        run2 = p2.add_run(f'— {attribution}')
        set_font(run2, size=10, bold=True, color=GRAY)
    return p

def bullet(text, bold_prefix='', indent=0.3):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent  = Inches(indent)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix + ' ')
        set_font(r1, size=11, bold=True, color=NAVY)
    r2 = p.add_run(text)
    set_font(r2, size=11, color=GRAY)
    return p

def metric_row(label, value, note='', value_color=BLUE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    p.paragraph_format.left_indent  = Inches(0.3)
    r1 = p.add_run(f'{label}: ')
    set_font(r1, size=11, bold=True, color=NAVY)
    r2 = p.add_run(value)
    set_font(r2, size=11, bold=True, color=value_color)
    if note:
        r3 = p.add_run(f'  — {note}')
        set_font(r3, size=10, italic=True, color=GRAY)
    return p

def divider():
    p = doc.add_paragraph('─' * 90)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    run = p.runs[0]
    set_font(run, size=8, color=RGBColor(0xD1, 0xD5, 0xDB))
    return p

def add_table_row(table, cells, bold=False, header=False, bg=None):
    row = table.add_row()
    for i, cell_text in enumerate(cells):
        cell = row.cells[i]
        cell.text = cell_text
        for para in cell.paragraphs:
            for run in para.runs:
                set_font(run, size=10, bold=bold or header,
                         color=WHITE if header else GRAY)
        if header or bg:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), '0F2D5E' if header else ('EFF6FF' if not bg else bg))
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)
    return row

# ══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(40)
run = p.add_run('US BANK')
set_font(run, size=36, bold=True, color=NAVY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
run = p.add_run('Payments & Transfers — Team Phoenix')
set_font(run, size=18, color=TEAL)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
run = p.add_run('TRANSFORMATION NARRATIVE')
set_font(run, size=28, bold=True, color=BLUE)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
run = p.add_run('From 42-Day Lead Times to an AI-Driven Lifecycle')
set_font(run, size=16, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
run = p.add_run('─' * 60)
set_font(run, size=10, color=RGBColor(0xD1, 0xD5, 0xDB))
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
run = p.add_run('PDLC VSM Platform  ·  Powered by LangGraph AI Agents  ·  March 2026')
set_font(run, size=11, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTIVE SNAPSHOT
# ══════════════════════════════════════════════════════════════════════════════

heading1('Executive Snapshot')
body('What follows is the complete story of how Team Phoenix — US Bank\'s Payments & Transfers product team — used the PDLC VSM Platform to measure, quantify, and chart a path through three transformation options, culminating in a radical reimagining of their entire delivery process as an AI-Driven Lifecycle (ADLC).')

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
run = p.add_run('THE NUMBERS IN 30 SECONDS')
set_font(run, size=12, bold=True, color=NAVY)

tbl = doc.add_table(rows=1, cols=5)
tbl.style = 'Table Grid'
add_table_row(tbl, ['Metric', 'Current State', 'Option A', 'Option B', 'Option C (ADLC)'], header=True)
rows = [
    ['Lead Time',          '42 days',   '18 days',  '10 days',  '3 days'],
    ['Flow Efficiency',    '8.1%',      '30%',      '44%',      '62%'],
    ['DORA Band',          'Medium',    'High',     'High/Elite','Elite'],
    ['Deploy Frequency',   '1×/week',   '3×/week',  'Daily',    'Continuous'],
    ['Change Fail Rate',   '12%',       '8%',       '5%',       '3%'],
    ['MTTR',               '2.3 days',  '18 hours', '4 hours',  '1 hour'],
    ['Annual ROI (est.)',  '—',         '$340K',    '$660K',    '$1.1M'],
]
for r in rows:
    add_table_row(tbl, r)

doc.add_paragraph()
divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 1: THE ORGANISATION AND ITS PROBLEM
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 1: The Organisation and Its Problem')

heading2('Who Is Team Phoenix?')
body('Team Phoenix is US Bank\'s twelve-person product engineering team responsible for the Payments & Transfers product group within the Digital Banking portfolio. Led by Product Owner Jennifer Zhao and supported by Solution Architect Marcus Thompson, the team sits at the intersection of two powerful forces: the regulatory weight of a Tier 1 financial institution and the competitive pressure of a fintech landscape that ships new payment experiences daily.')

body('The team is not underperforming by conventional measures. They delivered 47 features to production in Q4 2025 — their best quarter. Engineers are experienced, motivated, and increasingly equipped with modern tools including GitHub Copilot Enterprise. By most internal dashboards, Team Phoenix looks healthy.')

body('But the dashboards are measuring the wrong things.')

heading2('The Hidden Problem: 91.9% of Time Is Waste')
body('When PDLC VSM analysis maps the flow of a single feature from idea to production, a startling picture emerges. Of the 730 hours from first sprint planning session to final production deployment, only 59 hours involve anyone actually working on the feature. The remaining 671 hours — 91.9% of elapsed time — are spent waiting.')

body_bold_inline([
    ('Waiting ', True), ('for the Architecture Review Board to schedule a slot. ', False),
    ('Waiting ', True), ('for two senior engineers to review a pull request. ', False),
    ('Waiting ', True), ('for an external security vendor to complete a PCI-DSS penetration test. ', False),
    ('Waiting ', True), ('for the Wednesday release window. ', False),
    ('Waiting ', True), ('for the Change Advisory Board to approve a deployment. ', False),
])

body('None of these waits are failures of professionalism or engineering excellence. They are the accumulated weight of governance processes, organisational silos, manual handoffs, and risk-management frameworks built for a world where software changed quarterly, not daily. The problem is structural. And it is invisible to every dashboard the team currently runs.')

quote_block(
    'We knew something was wrong — features that felt like they should take two weeks were taking eight. But we couldn\'t point to a single cause. It was death by a thousand queues.',
    'Jennifer Zhao, Product Owner, Team Phoenix'
)

heading2('The Competitive Context')
body('While Team Phoenix deploys once per week, their fintech competitors — Wise, Revolut, and newer challenger banks — deploy multiple times per day. That is not a 7× difference in delivery speed. It is a 50× difference in the rate at which competitors can respond to customers, correct mistakes, and ship differentiating features.')

body('In payments specifically, speed is not a nice-to-have. It is the competitive moat. A bank that can ship a new payment experience in 3 days can test, learn, and iterate 14 times before a bank on a 42-day cycle ships its first version. That compounding advantage, multiplied across hundreds of features per year, is how market share moves in digital banking.')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 2: THE DISCOVERY — MAPPING THE VALUE STREAM
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 2: The Discovery — Mapping the Value Stream')

heading2('Step 1: Connecting the Data Sources')
body('The PDLC VSM Platform begins not with hypotheses but with data. Team Phoenix\'s Jira instance — usbank-digital.atlassian.net, project key PHOE — contains the actual cycle time record of 392 production deployments over the past 26 weeks. When the platform ingests this data, it maps each work item to one of seven PDLC phases and computes process time, wait time, and lead time at activity granularity.')

body('The platform\'s ALM integration maps 28 tracked activity types across the PDLC lifecycle. For Team Phoenix, this produces a 7-phase, 28-activity value stream map populated with real measurements — not estimates, not survey responses, not what the team thinks is happening, but what is actually happening.')

heading2('The Current State VSM — Phase by Phase')

tbl2 = doc.add_table(rows=1, cols=5)
tbl2.style = 'Table Grid'
add_table_row(tbl2, ['Phase', 'Process Time', 'Wait Time', 'Flow Efficiency', 'Primary Bottleneck'], header=True)
phase_data = [
    ['1. Backlog & Roadmap',      '31h', '72h',  '30%', 'Quarterly planning cadence; dependency queues'],
    ['2. Architecture & UX',      '36h', '176h', '17%', 'ARB queue (72h wait) + PCI-DSS security review'],
    ['3. Code Management',        '13h', '18h',  '42%', 'PR review wait: 18h median, 847-line avg PR'],
    ['4. Continuous Integration', '2h',  '6.5h', '24%', '24-min build + shared SIT cluster queue'],
    ['5. Continuous Testing',     '34h', '88h',  '28%', 'External pen-test gate: 5.2 days mandatory'],
    ['6. Continuous Delivery',    '8h',  '144h', '5%',  'CAB gate + Wednesday-only release window'],
    ['7. Monitoring & Feedback',  '6h',  '96h',  '6%',  'MTTR 2.3 days; DBA Mon–Fri hours only'],
    ['TOTAL',                     '130h','600h', '8.1%',''],
]
for r in phase_data:
    add_table_row(tbl2, r)

doc.add_paragraph()

body('Two phases stand out as catastrophically inefficient. Phase 6 — Continuous Delivery — has a 5% flow efficiency. For every 1 hour of real deployment work, the feature sits in a queue for 18 hours. The primary driver is the Wednesday 10pm release window: Team Phoenix can only deploy to production once per week, creating a batching dynamic where 6–8 features are compressed together into a single high-stakes release event.')

body('Phase 7 — Monitoring & Feedback — has a 6% flow efficiency. When a production incident occurs after 6pm or over the weekend, the organisation has no database administrator available. DB-related incidents — which represent 61% of post-deployment failures — wait for next-business-day DBA availability, driving the 2.3-day median MTTR.')

heading2('The Insight the Dashboards Cannot Show')
body('Traditional project metrics measure throughput: story points delivered, features shipped, sprint velocity. These metrics were all green for Team Phoenix in Q4 2025. But the VSM reveals that the team\'s actual productive output — the hours of real value-adding work — represents only 8.1% of the time the organisation is paying for. The other 91.9% is organisational drag.')

quote_block(
    'It\'s not that the engineers aren\'t working hard. They absolutely are. The VSM shows you that the system they\'re working inside is working against them — absorbing their effort in queues, gates, and handoffs.',
    'Marcus Thompson, Solution Architect, Team Phoenix'
)

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 3: DORA — QUANTIFYING DELIVERY PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 3: DORA — Quantifying Delivery Performance')

heading2('The Four Dimensions of Software Delivery Health')
body('The DORA (DevOps Research and Assessment) framework provides the industry\'s most validated model for measuring software delivery performance. The four core metrics — Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore — together define whether a team is an Elite, High, Medium, or Low performer. DORA\'s 2024 research analysed over 36,000 technology professionals globally.')

body('The PDLC VSM Platform\'s DORA Assessment module does not ask engineers to self-report these metrics. Instead, it ingests data from the same sources the metrics actually live in — Jira cycle time reports, GitHub Actions deployment logs, PagerDuty incident analytics, and CISO audit records — and applies AI analysis to score each dimension against published benchmarks with documented evidence and root cause explanation.')

heading2('Team Phoenix DORA Assessment Results')

heading3('Deployment Frequency: Once Per Week (Medium)')
body('Data sources: GitHub Actions deployment logs (47 prod deploys in Q4 2025) and CAB Meeting Schedule 2025. AI confidence: 88%.')
body('Root cause: US Bank\'s Change Advisory Board (CAB) meets every Tuesday at 2pm. All production changes require 48-hour advance submission with sign-off from the CTO, CISO, and Release Manager. The result is a weekly deployment cadence — not because the engineering team cannot deploy more frequently (they technically could deploy daily), but because the governance structure prevents it. The Wednesday 10pm release window is the only approved production deployment slot.')
body('Gap: Elite performers deploy multiple times per day. Team Phoenix\'s weekly cadence means a bug discovered on a Thursday must wait 6 days for the next deployment window. Fintechs fix the same bug in hours.')

heading3('Lead Time for Changes: 1–2 Weeks (Medium)')
body('Data sources: Jira Cycle Time Report — Team Phoenix Q3–Q4 2025 (median 9.4 working days) and CISO Compliance Policy v3.2. AI confidence: 91%.')
body('Root cause: The 9.4-day median lead time decomposes as: Development (2.1 days) + Code Review Wait (2.3 days) + CI/CD Pipeline (0.5 days) + Mandatory PCI-DSS Pen-Testing (5.2 days) + CAB Approval (3.4 days). The dominant bottleneck for features in PCI-DSS scope — which includes all Payments & Transfers functionality — is the external penetration testing gate, mandated by CISO Policy v3.2 and fulfilled by SecureWorks with a 5-business-day SLA.')
body('Gap: High performers achieve 1–7 day lead times. Team Phoenix\'s pen-testing gate alone can exceed that. The CISO policy requires this gate for any change to CDE components — but does not distinguish between a high-risk schema change and a low-risk UI colour update, both of which go through the same 5-day queue.')

heading3('Change Failure Rate: 12% (Medium)')
body('Data sources: Incident Log Q3–Q4 2025 (47 deployment-related incidents / 392 deployments) and PagerDuty Incident Report 2025. AI confidence: 94%.')
body('Root cause: US Bank\'s 12% change failure rate traces to three compounding causes. First, database migration failures account for 61% of incidents — legacy Oracle DB schema changes lack automated rollback scripts, so when a migration fails in production (due to data type incompatibilities or timing constraints), manual recovery is required. Second, a test coverage gap: SonarQube quality gates require 80% coverage, but Team Phoenix\'s 62% actual coverage means 38% of code paths are untested. Engineers have been annotating the quality gate to bypass it under sprint pressure. Third, environment parity gaps between SIT and production (14 configuration parameters differ) cause integration failures that only surface in prod.')
body('Financial impact: Each failure costs approximately $180,000 in incident response, remediation, and customer trust. At 47 failures per year, the annual cost of Team Phoenix\'s change failure rate is approximately $8.5 million.')

heading3('Mean Time to Restore: 1–7 Days (Medium)')
body('Data sources: PagerDuty MTTR Analytics 2025 (P50: 2.3 calendar days) and Incident Post-Mortem Database 2025. AI confidence: 82%.')
body('Root cause: The 2.3-day median MTTR combines four failure modes. First, manual incident investigation: with no AI-assisted root cause analysis, engineers spend 4–8 hours manually correlating logs and dashboards before identifying the source of a failure. Second, 34% of incidents require cross-team escalation, adding an average of 18.4 hours. Third, the DBA availability gap: database incidents — the most common failure type — wait for business-hours DBA coverage, which means Friday evening incidents resolve Monday morning. Fourth, no automated remediation runbooks exist: every incident requires manual intervention regardless of whether it has occurred before.')

heading2('The AI Auto-Score Validation Model')
body('A critical innovation in the PDLC VSM Platform\'s DORA module is the human validation layer. Rather than presenting a score and asking the team to accept it, the platform presents each AI-suggested metric alongside the specific source document it was derived from, the exact finding (quoted text), a confidence percentage, and a structured root cause and gap analysis.')

body('Team Phoenix\'s assessment session used this model as follows: the AI suggested "12% Change Failure Rate" and supported it with the finding "47 deployment-related incidents out of 392 total deployments" from the Production Incident Log. Jennifer Zhao could read the source, verify the finding, challenge the interpretation, or override the value before accepting. When all four core metrics were validated, the platform applied the DORA calibration to the VSM — adjusting wait times across phases based on the measured scores — ensuring the baseline model is grounded in evidence, not assumption.')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 4: BOTTLENECK ANALYSIS — WHERE THE WASTE LIVES
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 4: Bottleneck Analysis — Where the Waste Lives')

heading2('The Eight Critical Constraints')
body('AI analysis of the value stream map identifies and ranks bottlenecks by a composite score of wait time saved, business impact, and interconnection with other bottlenecks. The following eight constraints account for approximately 85% of Team Phoenix\'s total wait time.')

tbl3 = doc.add_table(rows=1, cols=4)
tbl3.style = 'Table Grid'
add_table_row(tbl3, ['Rank', 'Bottleneck', 'Wait Time Saved', 'Severity'], header=True)
bn_data = [
    ['1', 'CAB Gate + Wednesday Release Window (Phase 6)',    '128h per feature',    'Critical'],
    ['2', 'Mandatory Pen-Testing Gate — PCI-DSS (Phase 5)',   '40h per feature',     'Critical'],
    ['3', 'Architecture Review Board Queue (Phase 2)',         '72h per ARB item',    'High'],
    ['4', 'PR Code Review Wait — 18h Median (Phase 3)',        '12h per PR',          'High'],
    ['5', 'Sequential Test Execution — No Parallelism (Ph 5)', '28h per test cycle',  'High'],
    ['6', 'CI Build Duration — 24 min, No Caching (Phase 4)', '14 min per build',    'Medium'],
    ['7', 'DBA Availability Gap — Incidents (Phase 7)',        '24h per DB incident', 'High'],
    ['8', 'Quarterly Planning Cadence (Phase 1)',              '48h per cycle',       'Medium'],
]
for r in bn_data:
    add_table_row(tbl3, r)

doc.add_paragraph()

heading2('The CAB Gate: A Risk Management Tool Becoming a Delivery Constraint')
body('Bottleneck #1 is the most consequential because it is both the largest individual contributor to lead time and the most systemic in its effect. The Change Advisory Board exists to manage risk — and in a regulated bank, that mandate is legitimate. The problem is not the CAB\'s existence but its undifferentiated application.')

body('Every production change — whether a critical security patch or a button label update — goes through the same Tuesday CAB meeting, the same 48-hour submission window, the same three-approver sign-off, and the same Wednesday deployment window. This risk-management uniformity is precisely what creates the 128-hour wait time premium on every feature. A risk-tiered deployment model — where standard low-risk changes are pre-approved and only high-risk changes require full CAB review — could eliminate this bottleneck for approximately 70% of deployments while maintaining full governance compliance for the 30% of changes that genuinely need it.')

heading2('The Pen-Testing Gate: Compliance Without Intelligence')
body('The PCI-DSS penetration testing gate is non-negotiable in its mandate but entirely negotiable in its implementation. CISO Policy v3.2 requires penetration testing for changes to CDE components — but the policy does not specify that this must be manual external testing for every change, regardless of risk profile.')

body('AI-assisted DAST (Dynamic Application Security Testing) and SAST (Static Application Security Testing) tools, integrated into the CI/CD pipeline, can assess the risk profile of each change and generate evidence-grade security reports for low-risk modifications within the CI build itself — in under 5 minutes. External pen-testing would still be required for high-risk changes, but the 70% of changes that are low-risk could bypass the 5.2-day external queue. This does not reduce compliance; it intelligently applies compliance effort where it adds value.')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 5: THE THREE FUTURES
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 5: The Three Futures — Transformation Options for Team Phoenix')

heading2('Option A: Augmented PDLC (6–12 months)')
body('Option A preserves the architecture of the existing seven-phase PDLC lifecycle. Engineers still own every decision, every approval, and every handoff. What changes is the tooling layer: AI augments human effort at the activity level, reducing the time each activity takes and improving its quality.')

body('In Phase 3 (Code Management), GitHub Copilot Enterprise generates PR descriptions, pre-reviews PRs for obvious issues and security flags, and proposes test cases — reducing the cognitive load on senior reviewers and shrinking the median review time from 18 hours to 6 hours. In Phase 4 (CI), build caching eliminates the 12-minute dependency download from every build, cutting the 24-minute build to 8 minutes. Parallel test execution reduces the sequential test suite from 2 hours to 40 minutes.')

body('Option A\'s transformation across all phases:')
metric_row('Process Time', '130h → 65h', '50% reduction', GREEN)
metric_row('Wait Time', '600h → 155h', '74% reduction', GREEN)
metric_row('Flow Efficiency', '8.1% → 30%', '+270% improvement', GREEN)
metric_row('Lead Time', '42 days → 18 days', 'High Performer territory', BLUE)
metric_row('DORA Band', 'Medium → High', '', BLUE)
metric_row('Estimated Net Annual ROI', '$340K', 'after $120K tool investment', GREEN)

heading2('Option B: Automated PDLC (12–18 months)')
body('Option B goes further: major phases of the delivery pipeline shift from human-executed to AI-executed. Testing, deployment, and monitoring move from "humans run tools" to "agents run pipelines, humans supervise outcomes." The CAB gate is replaced by an automated risk-scoring engine. The pen-testing gate is replaced by integrated DAST/SAST for 70% of deployments. The Wednesday release window is replaced by continuous delivery with automated smoke tests and human approval only for high-risk changes.')

body('In Phase 5 (Continuous Testing), four agent activities replace the manual testing and pen-test pipeline:')
bullet('AI DAST/SAST Scanner — assesses security risk profile, runs in CI pipeline (<5 min)', 'Agent:')
bullet('Automated Regression Suite — parallel execution, 90%+ coverage, AI-generated test cases', 'Agent:')
bullet('Risk Scoring Engine — classifies each deployment as standard/elevated/high-risk', 'Agent:')
bullet('Human Override — Product Owner or QA Lead reviews AI risk classification for elevated/high-risk only', 'Oversight:')

body('In Phase 6 (Continuous Delivery), the release process shifts to a deployment agent that monitors infrastructure health, executes Kubernetes rollouts, runs smoke tests, and triggers automated rollback if SLO thresholds are breached — with human approval required only for high-risk deployments.')

body('Option B\'s transformation:')
metric_row('Process Time', '130h → 30h', '77% reduction', GREEN)
metric_row('Wait Time', '600h → 38h', '94% reduction', GREEN)
metric_row('Flow Efficiency', '8.1% → 44%', '+443% improvement', GREEN)
metric_row('Lead Time', '42 days → 10 days', 'High/Elite boundary', BLUE)
metric_row('DORA Band', 'Medium → High/Elite', '', BLUE)
metric_row('Estimated Net Annual ROI', '$660K', 'after $180K tool investment', GREEN)

heading2('Option C: ADLC — AI-Driven Lifecycle, BMAD Approach (18–24 months)')
body('Option C is the north star. It does not augment the existing lifecycle or automate its phases. It replaces the lifecycle itself with a fundamentally different model of software creation — one designed from first principles around AI agent orchestration rather than human sequential task execution.')

body('The ADLC model is grounded in the BMAD approach (Build, Measure, Automate, Deploy), which posits that a fully AI-orchestrated delivery pipeline requires only two human roles: the Product Definer, who sets the vision, OKRs, and acceptance criteria; and the Product Builder, who supervises agent orchestration and holds the final production approval gate.')

body('The seven PDLC phases are replaced by seven AI capability domains:')

tbl4 = doc.add_table(rows=1, cols=4)
tbl4.style = 'Table Grid'
add_table_row(tbl4, ['ADLC Phase', 'AI Capability', 'Human Role', 'Key Agent'], header=True)
adlc_data = [
    ['1. Intent & Outcome Definition',       'OKR parsing, acceptance criteria generation',      'Product Definer (sets intent)',          'Intent Agent'],
    ['2. Autonomous Architecture & Design',  'Architecture generation, API contracts, security', 'Product Builder (reviews design)',       'Architecture Agent'],
    ['3. Agentic Code Generation',           'Multi-agent parallel code synthesis, self-test',   'Product Builder (quality gate)',         'Code Generation Swarm'],
    ['4. Autonomous Integration Pipeline',   'Build, test, DAST/SAST, artefact publishing',      'Automated (no human needed)',            'CI Orchestrator Agent'],
    ['5. Continuous Quality Intelligence',   'Comprehensive coverage, regression, performance',  'Product Builder (quality approval)',     'QA Intelligence Agent'],
    ['6. Zero-Touch Delivery',               'Risk scoring, deployment, smoke tests, rollback',  'Product Builder (production gate)',      'Deployment Agent'],
    ['7. AIOps & Continuous Learning',       'Incident detection, RCA, remediation, learning',   'Escalation to Product Builder only',     'AIOps Agent'],
]
for r in adlc_data:
    add_table_row(tbl4, r)

doc.add_paragraph()
body('The ADLC model achieves metrics that are difficult to comprehend against the current state baseline:')
metric_row('Process Time', '130h → 8h', '94% reduction', GREEN)
metric_row('Wait Time', '600h → 5h', '99% reduction', GREEN)
metric_row('Flow Efficiency', '8.1% → 62%', '+665% improvement', GREEN)
metric_row('Lead Time', '42 days → 3 days', 'Elite Performer', BLUE)
metric_row('Agent Activities', '0 of 28 → 26 of 28', '2 human oversight points remain', TEAL)
metric_row('DORA Band', 'Medium → Elite', '', GREEN)
metric_row('Estimated Net Annual ROI', '$1.1M', 'after $220K tool investment', GREEN)

quote_block(
    'The most important thing to understand about Option C is what it is not. It is not replacing engineers with AI. It is giving two engineers the leverage of twenty — where those twenty are AI agents that never sleep, never have a PR review queue, and never wait for a Wednesday release window.',
    'PDLC VSM Platform — Future State Analysis'
)

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 6: THE BUSINESS CASE
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 6: The Business Case — Making the Numbers Undeniable')

heading2('The Cost of the Current State')
body('US Bank\'s Payments & Transfers team carries a fully-loaded engineering cost of approximately $180,000 per person per year. With 12 engineers, the annual engineering investment is $2.16 million. Against an 8.1% flow efficiency, 91.9% of that investment — $1.99 million — is being paid while the team is blocked by queues, waiting for approvals, or consuming capacity in rework and incident response.')

body('This is not a statement about team performance. It is a statement about organisational system design. The engineers are working hard. The system they work inside is absorbing their effort.')

body('Additional current-state costs:')
bullet('Change failure incidents: $8.5M/year (47 incidents × $180K average cost)', 'Direct cost:')
bullet('MTTR-related customer impact: Estimated $3.2M/year based on 2.3-day average outage duration across payment services', 'Customer impact:')
bullet('Competitive lag: Unquantifiable but material — fintechs shipping 50× faster are capturing new payment use cases before US Bank can respond', 'Strategic cost:')

heading2('Option B Investment vs Return (Recommended Starting Point)')
body('Option B represents the highest confidence ROI for a regulated financial institution in the 12–18 month horizon. It is ambitious enough to achieve meaningful competitive improvement without requiring the cultural and structural transformation that Option C demands.')

tbl5 = doc.add_table(rows=1, cols=3)
tbl5.style = 'Table Grid'
add_table_row(tbl5, ['Cost/Benefit Category', 'Annual Amount', 'Notes'], header=True)
bc_data = [
    ['Engineering capacity recovered (36% of $2.16M)', '$780,000', 'Freed from wait-time waste'],
    ['Incident cost reduction (CFR 12%→5%)', '$630,000', 'Fewer failures × $180K avg cost'],
    ['MTTR improvement value (2.3d → 4h)', '$480,000', 'Reduced customer impact + DBA time'],
    ['TOTAL GROSS ANNUAL BENEFIT', '$1,890,000', ''],
    ['AI tooling investment (DAST/SAST, AIOps, etc.)', '($180,000)', 'New tools + licences'],
    ['Implementation effort (internal)',                '($180,000)', 'Estimated 2-sprint team time'],
    ['Training & change management',                    '($90,000)',  'Copilot training, WoW changes'],
    ['TOTAL ANNUAL INVESTMENT',                         '($450,000)', ''],
    ['NET ANNUAL BENEFIT',                              '$660,000',   'Conservative estimate'],
    ['PAYBACK PERIOD',                                  '7–9 months', 'From first sprint investment'],
    ['3-YEAR NPV',                                      '~$1.6M',     'At 8% discount rate'],
]
for r in bc_data:
    add_table_row(tbl5, r)

doc.add_paragraph()

heading2('The Strategic Case Beyond the Numbers')
body('The financial case for Option B is strong on its own. But the strategic case is stronger. In the 12 months it would take Team Phoenix to complete Option B, their fintech competitors will have shipped approximately 2,000 new features (assuming daily deployment and 2-week lead times). US Bank will have shipped approximately 120. Every month of delay compounds this gap.')

body('The payments landscape is not static. Regulatory frameworks (NPP, Real-Time Payments, ISO 20022) are creating new infrastructure requirements. Consumer expectations for instant, intelligent payment experiences are being set by challengers, not incumbents. The bank that achieves Elite DORA performance in payments will be materially better positioned than the bank that does not — and the gap between them will be visible to customers long before it is visible to internal metrics dashboards.')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 7: THE IMPLEMENTATION JOURNEY
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 7: The Implementation Journey — A Sprint-by-Sprint Roadmap')

heading2('Foundation Sprints (Sprints 1–4, Weeks 1–8)')
body('The foundation layer addresses the highest-leverage, lowest-risk interventions first. These are actions that either use already-licensed tools (GitHub Copilot Enterprise has 66 unused seats) or require process changes rather than new procurement.')

bullet('GitHub Copilot Enterprise activation across all 12 team members — 66 seats available, no additional cost', 'Sprint 1:')
bullet('AI PR reviewer setup (GitHub Copilot code review) — target: PR review wait from 18h → 6h', 'Sprint 1:')
bullet('Build caching + parallel test execution — target: build time from 24min → 8min', 'Sprint 2:')
bullet('DB rollback script authoring for top-50 Liquibase changesets — target: CFR from 12% → 9%', 'Sprint 2:')
bullet('Risk-tiered change model proposal to CAB — define Standard/Normal/Emergency categories', 'Sprint 3:')
bullet('ARB self-service catalogue for standard architecture patterns — reduce ARB queue from 72h → 24h', 'Sprint 4:')
bullet('Test coverage improvement sprint — target: 62% → 70% coverage', 'Sprint 4:')

heading2('Automation Sprints (Sprints 5–10, Weeks 9–20)')
body('The automation layer integrates AI agents into the delivery pipeline. This is where process changes (Sprint 3\'s CAB risk-tiering) are implemented in tooling and where automated testing replaces manual testing phases.')

bullet('DAST/SAST integration into CI pipeline (OWASP ZAP → automated, AI risk scoring)', 'Sprint 5:')
bullet('Risk-tiered CAB model goes live — low-risk changes bypass Tuesday CAB meeting', 'Sprint 5:')
bullet('Automated regression suite upgrade — Selenium → Playwright + parallel execution', 'Sprint 6:')
bullet('PagerDuty + Datadog alert correlation — reduce false positive rate from 18% to < 5%', 'Sprint 7:')
bullet('AIOps runbook automation — automate remediation for top-10 recurring incident types', 'Sprint 8:')
bullet('Continuous planning rollout — quarterly → rolling 6-week OKR cycles', 'Sprint 9:')
bullet('IaC coverage expansion — 45% → 70% infrastructure automation (Terraform)', 'Sprint 10:')

heading2('AI-Native Sprints (Sprints 11–20, Weeks 21–40) — Option C Path')
body('For organisations choosing the ADLC path, Sprints 11–20 implement the agent orchestration layer that transforms the PDLC pipeline into an AI-Driven Lifecycle. This phase requires the deepest structural change — roles are reoriented, processes are redesigned, and the relationship between human engineers and AI agents is fundamentally redefined.')

bullet('LangGraph agent framework deployment — architecture + code generation agents piloted on a non-CDE product', 'Sprints 11–12:')
bullet('Product Definer role training — Jennifer Zhao and team learning intent specification for AI agents', 'Sprint 13:')
bullet('Autonomous integration pipeline — agent-driven CI/CD replaces GitHub Actions manual workflows', 'Sprints 14–15:')
bullet('Continuous Quality Intelligence agent — AI QA coverage, defect prediction, quality reporting', 'Sprints 16–17:')
bullet('Zero-Touch Delivery — deployment agent with automated risk scoring and rollback', 'Sprints 18–19:')
bullet('AIOps full deployment — incident detection, root cause analysis, and remediation automation', 'Sprint 20:')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 8: LOOKING FORWARD
# ══════════════════════════════════════════════════════════════════════════════

heading1('Chapter 8: Looking Forward — What Does Team Phoenix Look Like in 24 Months?')

heading2('The ADLC-Enabled Team Phoenix')
body('In the Option C future state, Team Phoenix has transformed from a twelve-person delivery team running a sequential PDLC pipeline to a two-role AI orchestration unit supported by 26 specialised AI agents handling end-to-end software delivery.')

body('Jennifer Zhao, as Product Definer, begins each feature cycle by specifying intent — the OKR, the acceptance criteria, the business context — in a structured format that the Intent Agent parses into task specifications for the agent swarm. Within 8 hours of intent specification, the Architecture Agent has generated a design proposal, the Code Generation swarm has produced an initial implementation, and the QA Intelligence Agent has run comprehensive testing. Marcus Thompson, as Product Builder, reviews the agent-generated output at three checkpoints: architecture review, quality approval, and production gate.')

body('The entire process — from Jennifer\'s intent specification to Marcus\'s production approval — takes an average of 3 days. For straightforward features, it takes 6 hours.')

heading2('What Happens to the Team?')
body('The natural question any engineering team asks about the ADLC vision is: what happens to the other 10 members of the team? The answer is expansion, not reduction.')

body('The engineers currently spending their time in PR review queues, waiting for CAB approvals, manually running test suites, and triaging false-positive PagerDuty alerts are freed to do the work that AI agents cannot: deep domain expertise application, complex stakeholder engagement, architectural decision-making at the edge of the organisation\'s knowledge, and building the next generation of AI-native capabilities.')

body('In practice, banks that achieve Elite DORA performance do not reduce their engineering teams — they redirect them. The capacity freed from process friction becomes the capacity to build more things faster. The pipeline expands. Competitive advantage compounds.')

heading2('The Invitation')
quote_block(
    'Team Phoenix\'s story is not unique to US Bank. Every product team in every regulated industry is carrying the same 91.9% waste — it just looks different in every organisation. The VSM makes it visible. The DORA assessment makes it measurable. The three transformation options make it actionable. The question is no longer whether to transform. The question is which option you start with — and how fast.',
    'PDLC VSM Platform — Transformation Summary'
)

doc.add_paragraph()
divider()

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12)
run = p.add_run('PDLC VSM Platform  ·  Narrative POV v1.0  ·  March 2026  ·  US Bank / Team Phoenix')
set_font(run, size=9, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ── Save ───────────────────────────────────────────────────────────────────────
doc.save('US-Bank-PDLC-VSM-Narrative-POV.docx')
print('✅  US-Bank-PDLC-VSM-Narrative-POV.docx created')
