"""
Build: US Bank — Case Study Document (Word)
Output: US-Bank-PDLC-VSM-Case-Study.docx
Consulting case study format: Challenge → Approach → Solution → Results
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Colours ────────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0F, 0x2D, 0x5E)
BLUE   = RGBColor(0x25, 0x63, 0xEB)
TEAL   = RGBColor(0x0D, 0x94, 0x88)
AMBER  = RGBColor(0xD9, 0x77, 0x06)
RED    = RGBColor(0xDC, 0x26, 0x26)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
GRAY   = RGBColor(0x4B, 0x55, 0x63)
DGRAY  = RGBColor(0x37, 0x41, 0x51)
LGRAY  = RGBColor(0xF3, 0xF4, 0xF6)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

doc = Document()

section = doc.sections[0]
section.page_width    = Inches(8.5)
section.page_height   = Inches(11)
section.left_margin   = Inches(1.0)
section.right_margin  = Inches(1.0)
section.top_margin    = Inches(0.9)
section.bottom_margin = Inches(0.9)

# ── Helpers ────────────────────────────────────────────────────────────────────
def sfont(run, name='Calibri', size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color: run.font.color.rgb = color

def h1(text, color=NAVY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run(text)
    sfont(r, size=20, bold=True, color=color)
    return p

def h2(text, color=BLUE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    sfont(r, size=13, bold=True, color=color)
    return p

def h3(text, color=TEAL):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    sfont(r, size=11, bold=True, color=color)
    return p

def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run(text)
    sfont(r, size=11, color=GRAY)
    return p

def body_mixed(parts):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    for text, bold, color in parts:
        r = p.add_run(text)
        sfont(r, size=11, bold=bold, color=color or GRAY)
    return p

def callout(label, value, note='', lc=TEAL, vc=NAVY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Inches(0.4)
    r1 = p.add_run(f'{label}  ')
    sfont(r1, size=10, bold=True, color=lc)
    r2 = p.add_run(value)
    sfont(r2, size=14, bold=True, color=vc)
    if note:
        r3 = p.add_run(f'  {note}')
        sfont(r3, size=10, italic=True, color=GRAY)
    return p

def pull_quote(text, source=''):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.5)
    p.paragraph_format.right_indent = Inches(0.5)
    r = p.add_run(f'"{text}"')
    sfont(r, size=12, italic=True, color=BLUE)
    if source:
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.5)
        p2.paragraph_format.space_after = Pt(8)
        r2 = p2.add_run(f'— {source}')
        sfont(r2, size=10, bold=True, color=GRAY)
    return p

def bullet(text, prefix='', indent=0.3):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.space_after = Pt(3)
    if prefix:
        r1 = p.add_run(prefix + ' ')
        sfont(r1, size=11, bold=True, color=NAVY)
    r2 = p.add_run(text)
    sfont(r2, size=11, color=GRAY)
    return p

def add_tbl_row(table, cells, header=False):
    row = table.add_row()
    for i, txt in enumerate(cells):
        cell = row.cells[i]
        cell.text = txt
        for para in cell.paragraphs:
            for run in para.runs:
                sfont(run, size=10, bold=header, color=WHITE if header else GRAY)
        if header:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), '0F2D5E')
            shd.set(qn('w:val'), 'clear')
            tcPr.append(shd)
    return row

def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run('─' * 95)
    sfont(r, size=8, color=RGBColor(0xD1, 0xD5, 0xDB))

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(20)
r = p.add_run('CASE STUDY')
sfont(r, size=13, bold=True, color=TEAL)
p.alignment = WD_ALIGN_PARAGRAPH.LEFT

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
r = p.add_run('US Bank — Payments & Transfers')
sfont(r, size=28, bold=True, color=NAVY)

p = doc.add_paragraph()
r = p.add_run('Team Phoenix: Transforming a Regulated Bank\'s Software Delivery\nfrom Medium DORA Performer to AI-Driven Elite')
sfont(r, size=16, italic=True, color=BLUE)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(8)
r = p.add_run('─' * 70)
sfont(r, size=9, color=RGBColor(0xD1, 0xD5, 0xDB))

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
r = p.add_run('PDLC VSM Platform  ·  LangGraph AI Agents  ·  Financial Services  ·  March 2026')
sfont(r, size=11, color=GRAY)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
# QUICK FACTS SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
h1('At a Glance')

tbl_facts = doc.add_table(rows=1, cols=2)
tbl_facts.style = 'Table Grid'
add_tbl_row(tbl_facts, ['ORGANISATION PROFILE', 'OUTCOME SNAPSHOT'], header=True)
r2 = tbl_facts.add_row()
r2.cells[0].text = (
    'Organisation: US Bank (Tier 1 US Financial Institution)\n'
    'Division: Digital Banking\n'
    'Team: Team Phoenix — 12 engineers\n'
    'Product Group: Payments & Transfers\n'
    'Portfolio: Digital Banking\n'
    'Tech Stack: Java / Spring Boot, React 18, Azure Kubernetes, GitHub Actions\n'
    'Compliance: PCI-DSS Level 1, SOC 2 Type II, APRA CPS 234, ISO 27001\n'
    'Analysis Period: Q3–Q4 2025 (26 weeks, 392 deployments)\n'
    'Tooling: PDLC VSM Platform + LangGraph 8 AI Agents'
)
r2.cells[1].text = (
    'Lead Time: 42 days → 10 days (Option B) / 3 days (Option C)\n'
    'Flow Efficiency: 8.1% → 44% (Option B) / 62% (Option C)\n'
    'DORA Band: Medium → High/Elite (Option B) / Elite (Option C)\n'
    'Deploy Frequency: 1×/week → Daily (B) / Continuous (C)\n'
    'Change Failure Rate: 12% → 5% (B) / 3% (C)\n'
    'MTTR: 2.3 days → 4 hours (B) / 1 hour (C)\n'
    'Net Annual ROI: $660K (Option B) / $1.1M (Option C)\n'
    'Payback Period: 7–9 months (Option B)'
)
for cell in r2.cells:
    for para in cell.paragraphs:
        for run in para.runs:
            sfont(run, size=10, color=GRAY)

doc.add_paragraph()
divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: CLIENT CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
h1('1. Client Challenge')

h2('The Visible Problem — and the Hidden One')
body('By Q4 2025, US Bank\'s Payments & Transfers team (Team Phoenix) was delivering solid results on the metrics that internal stakeholders could see: 47 features shipped in Q4, sprint velocity trending upward, GitHub Copilot adoption at 34% and growing. The engineering organisation was performing well by conventional software delivery standards.')

body('But a parallel competitive reality was accelerating. The digital payments market — where US Bank competes directly with Wise, Revolut, PayPal, and a new generation of embedded payments challengers — had moved to a continuous delivery cadence. Challenger banks were shipping payment experiences multiple times per day. US Bank was shipping once per week. That is not a marginal speed difference. It is a structural competitive disadvantage that compounds every week it persists.')

body('The challenge was not to fix an obvious underperformance. It was to make visible a structural inefficiency that was invisible to existing metrics, and then quantify its business cost with enough precision to justify a transformation investment.')

h2('The Regulatory Complexity Layer')
body('US Bank\'s engineering environment carries a compliance burden that most fintechs do not: PCI-DSS Level 1, SOC 2 Type II, APRA CPS 234, and ISO 27001. These frameworks are not optional — they are the operating environment. Any transformation approach that ignores or conflicts with compliance requirements will fail at the governance layer.')

body('The risk in many AI-driven transformation programmes is that they are designed for greenfield environments and require significant adaptation for regulated industries. Team Phoenix\'s challenge required a solution that could achieve Elite DORA performance while operating within — or intelligently restructuring — the compliance framework.')

h2('Specific Pain Points Identified by Team Phoenix')
bullet('42-day average lead time from feature commit to production', 'Lead time:')
bullet('8.1% flow efficiency — 91.9% of cycle time is non-value-adding wait', 'Flow efficiency:')
bullet('12% change failure rate — $8.5M annual cost from deployment-related incidents', 'Quality:')
bullet('2.3-day mean time to restore — DBA availability gap compounds incident duration', 'Reliability:')
bullet('GitHub Copilot at 34% adoption despite 100 licensed seats — no formal enablement program', 'AI adoption:')
bullet('Wednesday-only release window driven by CAB governance — not technical limitation', 'Governance:')
bullet('Mandatory 5.2-day pen-testing gate for all PCI-DSS scope changes regardless of risk level', 'Compliance:')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: APPROACH
# ══════════════════════════════════════════════════════════════════════════════
h1('2. Approach')

h2('The PDLC VSM Platform Methodology')
body('The transformation engagement was structured around the PDLC VSM Platform — a purpose-built AI-powered value stream mapping and transformation planning system designed specifically for product delivery organisations. The platform uses eight LangGraph AI agents to automate the analysis, scoring, and recommendation generation that would otherwise require weeks of consulting engagement.')

body('The methodology follows a six-step discovery-to-recommendation cycle:')
bullet('Data ingestion from live ALM systems (Jira, GitHub, Azure DevOps) — no survey-based estimation', '1. Connect:')
bullet('AI-powered DORA metric scoring with source document evidence and human validation layer', '2. Assess:')
bullet('Activity-level VSM construction showing process time, wait time, and flow efficiency per phase', '3. Map:')
bullet('AI bottleneck analysis ranked by composite impact score (wait time saved × business impact)', '4. Analyse:')
bullet('Three future-state transformation options modelled with distinct activities and VSM metrics per option', '5. Model:')
bullet('Financial business case and sprint-by-sprint implementation roadmap generated automatically', '6. Plan:')

h2('Phase 1: Current State Discovery (Days 1–5)')
body('The PDLC VSM Platform connected to Team Phoenix\'s Jira instance (project key PHOE) and ingested 26 weeks of cycle time data covering 392 production deployments. The AI agents mapped each work item to 28 activity types across 7 PDLC phases, computing process time, wait time, lead time, and flow efficiency at activity granularity.')

body('Simultaneously, the DORA Assessment module analysed data from GitHub Actions deployment logs, PagerDuty incident analytics, the Production Incident Log, and CISO Policy documents. Each DORA metric was scored against benchmark data with three supporting source findings, a root cause explanation, and a gap analysis. Jennifer Zhao (Product Owner) reviewed each AI-suggested score, verified the evidence, and accepted or overrode each value before the calibration was applied to the VSM.')

pull_quote(
    'We spent three months in a previous engagement trying to get accurate baseline metrics. The platform gave us a validated baseline with source evidence in two days. The DORA calibration step was the moment the team stopped arguing about whether the data was right and started asking what to do about it.',
    'Jennifer Zhao, Product Owner, Team Phoenix'
)

h2('Phase 2: Future State Modelling (Days 6–10)')
body('Unlike traditional VSM tools that scale current-state metrics by improvement factors, the PDLC VSM Platform models each transformation option with completely distinct activity definitions. Option A, Option B, and Option C each have their own set of phase-level activities with independent process times, wait times, activity types (human/hybrid/agent/oversight), assigned roles, and AI agent assignments.')

body('This activity-level differentiation is critical for communicating the nature of the transformation. In Option A, a human developer writes code and a human senior engineer reviews it — the AI assists. In Option B, an AI agent pre-reviews the PR and the human reviewer sees only the AI-flagged items. In Option C, the code is generated by an agent swarm and the Product Builder reviews the agent\'s quality report at a checkpoint. These are not the same process at different speeds — they are fundamentally different processes.')

body('Option C specifically was modelled as an ADLC (AI-Driven Lifecycle) based on the BMAD approach (Build, Measure, Automate, Deploy), with only two human roles: Product Definer and Product Builder. All seven PDLC phases were replaced by seven AI capability domains, with 26 of 28 activities classified as agent-driven and only 2 oversight checkpoints requiring human engagement.')

h2('Phase 3: Validation and Business Case (Days 11–15)')
body('The Playbook Context module enriched the AI\'s understanding of Team Phoenix\'s specific environment before generating the implementation playbook. Seven context sections were completed covering team profile, technology stack (Azure, GitHub Actions, Java/Spring Boot, Datadog, PagerDuty), budget and procurement constraints ($500K–$1M approved, 4–8 week procurement cycle), security and compliance requirements (PCI-DSS Level 1 data residency, enterprise-only AI policy), culture and change readiness (Performing team maturity, active CTO sponsorship), ways of working (2-week Scrum, current weekly deployments), and stakeholder context (known concerns from CISO and Engineering VP about AI compliance risk).')

body('Seven supporting documents were uploaded for additional context: the Team Phoenix org chart, Engineering Standards v2.4, Tool & Licence Inventory (revealing 66 unused Copilot seats), CISO Security & Compliance Policy v3.2, 2026 OKRs, Q3–Q4 2025 DORA Metrics Report, and Sprint 24–25 Retrospective Notes.')

body('The retrospective notes proved particularly valuable: they independently corroborated the VSM\'s bottleneck rankings. PR review wait, the pen-testing gate, and the Wednesday release window were listed as top pain points in four consecutive retrospectives — providing human confirmation of AI-derived findings and accelerating stakeholder buy-in.')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: SOLUTION
# ══════════════════════════════════════════════════════════════════════════════
h1('3. Solution — Three Transformation Options')

h2('Option A: Augmented PDLC')
body('Recommendation for teams seeking quick wins and manageable risk. Preserves the existing PDLC architecture while layering AI assistance at the activity level. Achieves High Performer DORA status within 6–12 months.')

h3('Key Interventions')
bullet('GitHub Copilot Enterprise activation (100% of 12 seats) with formal training — use existing unused 66 seats', 'Immediate:')
bullet('AI-powered PR pre-review — cuts review cycle time from 18h to 6h without changing approval policy', 'Phase 3:')
bullet('Build caching + parallel test execution — build time from 24min to 8min', 'Phase 4:')
bullet('DB migration rollback script automation — CFR reduction from 12% to 8%', 'Phase 5:')
bullet('Risk-tiered change model proposal to CAB — eliminates full CAB review for ~70% of changes', 'Phase 6:')

body_mixed([('VSM Impact: ', True, NAVY), ('PT 130h→65h  |  WT 600h→155h  |  FE 8.1%→30%  |  Lead Time 42→18 days  |  ROI $340K/yr', False, GRAY)])

h2('Option B: Automated PDLC (Recommended Starting Point)')
body('Recommendation for teams ready for a genuine transformation. Major delivery phases shift from human-executed to AI-executed with human supervision. Achieves High/Elite DORA boundary within 12–18 months.')

h3('Key Interventions')
bullet('DAST/SAST AI scanner integrated into CI pipeline — replaces external pen-test for 70% of changes', 'Phase 5:')
bullet('Automated regression suite: Selenium→Playwright + parallel execution + AI-generated test cases', 'Phase 5:')
bullet('Risk-tiered CAB model live — low-risk changes bypass Tuesday CAB, deploy any day', 'Phase 6:')
bullet('Deployment agent: automated Kubernetes rollout, smoke tests, automated rollback', 'Phase 6:')
bullet('AIOps: automated incident detection, root cause analysis, remediation runbooks for top-10 incident types', 'Phase 7:')
bullet('PagerDuty alert correlation — false positive rate from 18% to <5%', 'Phase 7:')

body_mixed([('VSM Impact: ', True, NAVY), ('PT 130h→30h  |  WT 600h→38h  |  FE 8.1%→44%  |  Lead Time 42→10 days  |  ROI $660K/yr', False, GRAY)])

h2('Option C: ADLC — AI-Driven Lifecycle (North Star, BMAD Approach)')
body('The most ambitious transformation option. Replaces the sequential PDLC lifecycle with a seven-phase AI-Driven Lifecycle based on the BMAD approach. Two human roles (Product Definer, Product Builder) supervise 26 AI agent activities. Achieves Elite DORA performance within 18–24 months.')

h3('The ADLC Agent Architecture')
tbl_adlc = doc.add_table(rows=1, cols=5)
tbl_adlc.style = 'Table Grid'
add_tbl_row(tbl_adlc, ['ADLC Phase', 'Human Role', 'Agent(s)', 'PT', 'WT'], header=True)
adlc = [
    ['1. Intent & Outcome Definition',      'Product Definer',    'Intent Parser Agent',        '1h',   '0h'],
    ['2. Autonomous Architecture & Design', 'Product Builder',    'Architecture Agent',          '1.5h', '0.5h'],
    ['3. Agentic Code Generation',          'Product Builder',    'Code Gen Swarm (4 agents)',   '2.5h', '0.5h'],
    ['4. Autonomous Integration Pipeline',  'Automated',          'CI Orchestrator Agent',       '0.5h', '0h'],
    ['5. Continuous Quality Intelligence',  'Product Builder',    'QA Intelligence Agent',       '1h',   '0.5h'],
    ['6. Zero-Touch Delivery',              'Product Builder',    'Deployment Agent',            '0.5h', '1h'],
    ['7. AIOps & Continuous Learning',      'Escalation only',    'AIOps Agent',                 '1h',   '2.5h'],
    ['TOTALS',                              '2 roles',            '26 of 28 activities (agent)', '8h',   '5h'],
]
for r in adlc:
    add_tbl_row(tbl_adlc, r)

doc.add_paragraph()
body_mixed([('VSM Impact: ', True, NAVY), ('PT 130h→8h  |  WT 600h→5h  |  FE 8.1%→62%  |  Lead Time 42→3 days  |  ROI $1.1M/yr', False, GRAY)])

divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: RESULTS & IMPACT
# ══════════════════════════════════════════════════════════════════════════════
h1('4. Projected Results & Business Impact')

h2('Quantified Outcomes by Option')

tbl_res = doc.add_table(rows=1, cols=5)
tbl_res.style = 'Table Grid'
add_tbl_row(tbl_res, ['KPI', 'Baseline', 'Option A', 'Option B', 'Option C'], header=True)
res_data = [
    ['Lead Time (days)',              '42',    '18',     '10',     '3'],
    ['Flow Efficiency (%)',           '8.1',   '30',     '44',     '62'],
    ['Process Time (hrs)',            '130',   '65',     '30',     '8'],
    ['Wait Time (hrs)',               '600',   '155',    '38',     '5'],
    ['Deploy Frequency',              '1×/wk', '3×/wk', 'Daily',  'Continuous'],
    ['DORA Band',                     'Medium','High',   'High/Elite','Elite'],
    ['Change Failure Rate (%)',        '12',    '8',      '5',      '3'],
    ['MTTR',                          '2.3d',  '18h',    '4h',     '1h'],
    ['Agent Activities (of 28)',       '0',     '8',      '18',     '26'],
    ['Est. Net Annual ROI',            '—',     '$340K',  '$660K',  '$1.1M'],
    ['Est. Payback Period',            '—',     '10mo',   '7–9mo',  '8–10mo'],
]
for r in res_data:
    add_tbl_row(tbl_res, r)

doc.add_paragraph()

h2('Financial Impact Model (Option B)')
body('Option B was selected as the primary recommendation for US Bank given the regulatory environment, team maturity, and 12–18 month implementation horizon. The financial model is conservative and excludes strategic/revenue upside.')

tbl_fin = doc.add_table(rows=1, cols=3)
tbl_fin.style = 'Table Grid'
add_tbl_row(tbl_fin, ['Category', 'Annual Value', 'Basis'], header=True)
fin = [
    ['Engineering capacity recovered (WT reduction)',    '$780,000', '36% of $2.16M team cost'],
    ['Incident cost reduction (CFR 12%→5%)',             '$630,000', '33 fewer incidents × $180K/inc'],
    ['MTTR improvement (2.3 days → 4 hours)',            '$480,000', 'Reduced customer impact + DBA time'],
    ['GROSS ANNUAL BENEFIT',                             '$1,890,000',''],
    ['AI tooling investment',                            '($180,000)','DAST/SAST, AIOps, licences'],
    ['Implementation effort (internal)',                 '($180,000)','~2 sprint team capacity'],
    ['Training & change management',                     '($90,000)', 'Copilot, WoW, upskilling'],
    ['TOTAL INVESTMENT',                                 '($450,000)',''],
    ['NET ANNUAL BENEFIT',                               '$660,000',  'Conservative estimate'],
    ['PAYBACK PERIOD',                                   '7–9 months','From first sprint'],
    ['3-YEAR NPV',                                       '~$1.6M',    'At 8% discount rate'],
]
for r in fin:
    add_tbl_row(tbl_fin, r)

doc.add_paragraph()

h2('Strategic Impact Beyond the Financial Model')
body('The financial model captures recoverable capacity and incident cost reduction. It does not capture:')
bullet('Revenue acceleration: 4× faster delivery means 4× more payment feature experiments per year. In a market where first-mover advantage on payment UX is measurable in customer acquisition, the compounding value of 4× delivery speed significantly exceeds the cost savings model.', 'Revenue:')
bullet('Compliance automation: Option B\'s DAST/SAST integration generates machine-readable evidence for PCI-DSS controls. Automated audit evidence generation reduces the annual compliance attestation effort from weeks to hours.', 'Compliance:')
bullet('Talent retention: Sprint retrospectives identified process frustration as a key engagement risk. Engineers working in a high-flow, AI-augmented environment have measurably higher satisfaction scores than those spending 40% of their time in review queues and approval gates.', 'Talent:')
bullet('Risk reduction: A 5% change failure rate vs. 12% means 56 fewer deployment-related incidents per year. Beyond financial cost, each incident carries regulatory reporting risk under APRA CPS 234 (72-hour notification threshold).', 'Risk:')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: IMPLEMENTATION ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
h1('5. Implementation Roadmap')

h2('Option B Path — 20 Sprint Journey')

h3('Foundation Layer: Sprints 1–4 (Weeks 1–8)')
body('Objectives: Activate existing assets, eliminate the highest-leverage low-risk bottlenecks, establish AI-assisted review baseline.')
bullet('Sprint 1: GitHub Copilot 100% activation + PR description template → review cycle 18h → 12h')
bullet('Sprint 2: Build caching + parallel tests → build time 24min → 8min; DB rollback script library')
bullet('Sprint 3: CAB risk-tier proposal + ARB self-service catalogue for standard patterns')
bullet('Sprint 4: Test coverage sprint (62%→70%), SonarQube quality gate enforcement restored')

h3('Automation Layer: Sprints 5–10 (Weeks 9–20)')
body('Objectives: AI agents enter the delivery pipeline; testing and deployment begin shifting to agent-managed workflows.')
bullet('Sprint 5: DAST/SAST into CI pipeline; CAB risk-tier model goes live (low-risk bypass)')
bullet('Sprint 6: Playwright migration + parallel execution → test suite 2h → 40min')
bullet('Sprint 7: PagerDuty alert correlation → false positive rate 18% → <5%')
bullet('Sprint 8: AIOps runbooks for top-10 recurring incident types → MTTR 2.3d → 18h')
bullet('Sprint 9: Rolling 6-week OKR cycles replace quarterly planning')
bullet('Sprint 10: IaC expansion 45% → 70%; Oracle→Azure SQL migration begins')

h3('Continuous Improvement Layer: Sprints 11–20 (Weeks 21–40)')
body('Objectives: Complete Option B state; optionally begin Option C agent pilot on lower-risk product.')
bullet('Sprint 11–12: Deployment agent pilot — automated Kubernetes rollout + smoke tests')
bullet('Sprint 13–14: Full Option B state achieved — performance benchmarking vs. DORA targets')
bullet('Sprint 15–20: Option C pilot on non-CDE product group — LangGraph agent swarm, Product Definer/Builder role piloting')

divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: KEY LEARNINGS
# ══════════════════════════════════════════════════════════════════════════════
h1('6. Key Learnings & Applicability')

h2('What Made This Engagement Different')

h3('Data-grounded transformation, not hypothesis-led')
body('Every bottleneck, every metric, every recommendation in this engagement is traceable to a specific data source with a quoted finding. This is not a strength of the consulting methodology — it is a capability of the platform. AI agents that can read source documents and produce evidence-graded scores change the dynamics of stakeholder alignment. The sprint retrospective notes independently corroborated the top three VSM bottlenecks. That convergence of AI analysis and human testimony is more persuasive than either alone.')

h3('Human validation as the accountability layer')
body('The DORA auto-scoring model does not bypass the human. It accelerates and informs the human. Product Owner Jennifer Zhao reviewed each AI-suggested metric score against the cited source document and made the final call. This is the right architecture for AI-assisted decision-making in regulated environments: AI handles data aggregation, pattern recognition, and evidence presentation; humans hold accountability for the conclusions and their implications.')

h3('Compliance and transformation are not opposites')
body('The PDLC VSM Platform\'s model for addressing PCI-DSS compliance constraints demonstrates a principle that applies across regulated industries: compliance requirements specify what must be controlled, not how it must be controlled. A human penetration tester and an AI-powered DAST scanner can both satisfy a PCI-DSS control — but the AI scanner can do it in 5 minutes for 70% of changes, preserving the external pen-test for the 30% of changes where its depth is genuinely needed. Intelligent compliance implementation is not regulatory arbitrage; it is using the right control at the right risk level.')

h3('The ADLC is a destination, not a disruption')
body('Option C — the AI-Driven Lifecycle — is a genuine reimagining of software creation. But the path to it is incremental, not revolutionary. Teams that attempt to jump directly to Option C without the foundations of Option A and B are likely to struggle. The roadmap is designed as a capability staircase: each option builds the technical and cultural infrastructure that the next option requires.')

h2('Applicability to Other Financial Services Organisations')
body('The patterns identified in Team Phoenix\'s VSM are not unique to US Bank. They represent the systemic bottlenecks of regulated financial services engineering:')
bullet('CAB governance gates that were designed for quarterly software releases operating in a weekly deployment environment')
bullet('Compliance frameworks that prescribe controls without differentiating by risk level, creating uniform queues for heterogeneous risk')
bullet('Shared services silos (DBA, Security, Architecture) operating at business-hours availability in a continuous delivery environment')
bullet('AI tool licencing ahead of AI enablement investment — resulting in unused capacity and slow adoption curves')
body('Any financial services organisation with a delivery team scoring Medium or Low on DORA will find material parallels with Team Phoenix\'s VSM. The specific numbers will differ. The structural patterns will not.')

divider()

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12)
r = p.add_run('PDLC VSM Platform  ·  Case Study v1.0  ·  March 2026\nUS Bank / Team Phoenix / Payments & Transfers')
sfont(r, size=9, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.save('US-Bank-PDLC-VSM-Case-Study.docx')
print('✅  US-Bank-PDLC-VSM-Case-Study.docx created')
