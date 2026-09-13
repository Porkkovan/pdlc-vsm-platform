"""
Build: Frontier Professional — Post-ADLC Future State POV (Word Document)
Output: Frontier-Professional-Post-ADLC-POV.docx

Business-friendly, narrative/storytelling style.
Written for non-technology audiences — CxOs, business leaders, board members.
No jargon. Story-driven. Human-centred.

Based on "Becoming a Frontier Professional" by Porkkovan Elangovan & Khirthika V.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Colour palette ─────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x0F, 0x2D, 0x5E)
BLUE    = RGBColor(0x25, 0x63, 0xEB)
TEAL    = RGBColor(0x0D, 0x94, 0x88)
AMBER   = RGBColor(0xD9, 0x77, 0x06)
RED     = RGBColor(0xDC, 0x26, 0x26)
GREEN   = RGBColor(0x16, 0xA3, 0x4A)
EMERALD = RGBColor(0x05, 0x96, 0x69)
VIOLET  = RGBColor(0x7C, 0x3A, 0xED)
GRAY    = RGBColor(0x4B, 0x55, 0x63)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)

doc = Document()

# ── Page setup ─────────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width    = Inches(8.5)
section.page_height   = Inches(11)
section.left_margin   = Inches(1.2)
section.right_margin  = Inches(1.2)
section.top_margin    = Inches(1.0)
section.bottom_margin = Inches(1.0)

# ── Style helpers ──────────────────────────────────────────────────────────────
def sf(run, name='Calibri', size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def h1(text, color=NAVY):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after  = Pt(8)
    r = p.add_run(text)
    sf(r, size=20, bold=True, color=color)
    return p

def h2(text, color=BLUE):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    sf(r, size=14, bold=True, color=color)
    return p

def h3(text, color=TEAL):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    sf(r, size=12, bold=True, color=color)
    return p

def para(text, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(8)
    p.paragraph_format.line_spacing = Pt(16)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(text)
    sf(r, size=11.5, color=GRAY)
    return p

def quote(text, who=''):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(10)
    p.paragraph_format.left_indent  = Inches(0.5)
    p.paragraph_format.right_indent = Inches(0.5)
    r = p.add_run(f'“{text}”')
    sf(r, size=13, italic=True, color=BLUE)
    if who:
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.5)
        p2.paragraph_format.space_after = Pt(10)
        r2 = p2.add_run(f'— {who}')
        sf(r2, size=10, bold=True, color=GRAY)

def bullet(text, bold_prefix='', indent=0.35):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent  = Inches(indent)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(4)
    if bold_prefix:
        r1 = p.add_run(bold_prefix + '  ')
        sf(r1, size=11, bold=True, color=NAVY)
    r2 = p.add_run(text)
    sf(r2, size=11, color=GRAY)

def divider():
    p = doc.add_paragraph('─' * 85)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    sf(p.runs[0], size=8, color=RGBColor(0xD1, 0xD5, 0xDB))

def cell_shade(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    shd.set(qn('w:val'), 'clear')
    tcPr.append(shd)

def table(headers, rows, widths=None, hdr_bg='0F2D5E', alt_bg='EFF6FF'):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    hr = t.rows[0]
    for i, h in enumerate(headers):
        c = hr.cells[i]; c.text = h
        for p in c.paragraphs:
            for r in p.runs: sf(r, size=10, bold=True, color=WHITE)
        cell_shade(c, hdr_bg)
    for ri, rd in enumerate(rows):
        row = t.add_row()
        for ci, v in enumerate(rd):
            c = row.cells[ci]; c.text = v
            for p in c.paragraphs:
                for r in p.runs: sf(r, size=10, color=GRAY)
            if ri % 2 == 1: cell_shade(c, alt_bg)
    if widths:
        for row in t.rows:
            for ci, w in enumerate(widths):
                row.cells[ci].width = Inches(w)
    return t


# ══════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(70)
r = p.add_run('THE FUTURE STATE OF'); sf(r, size=14, bold=True, color=TEAL)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(2)
r = p.add_run('IT Service Partners'); sf(r, size=34, bold=True, color=NAVY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
r = p.add_run('When Every Professional Becomes a Frontier Engineer'); sf(r, size=16, italic=True, color=BLUE)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(20)
r = p.add_run('─' * 50); sf(r, size=10, color=RGBColor(0xD1, 0xD5, 0xDB))
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(14)
r = p.add_run(
    'A point of view on what happens after the AI-Driven Lifecycle is achieved:\n'
    'small pods of 1–3 people, amplified by tireless digital agents,\n'
    'delivering what once took a hundred.'
)
sf(r, size=12, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(20)
r = p.add_run('─' * 50); sf(r, size=10, color=RGBColor(0xD1, 0xD5, 0xDB))
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
r = p.add_run('Based on “Becoming a Frontier Professional”'); sf(r, size=11, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph()
r = p.add_run('Porkkovan Elangovan  &  Khirthika V'); sf(r, size=11, bold=True, color=NAVY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(20)
r = p.add_run('July 2026  ·  Confidential'); sf(r, size=10, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  THE STORY BEGINS
# ══════════════════════════════════════════════════════════════════════════════

h1('Imagine This')

para(
    'Imagine describing the outcome you want — and a small pod of two or three '
    'people, amplified by tireless digital agents, turning it into a working product '
    'and running it for you. Not in six months. In days.'
)

para(
    'You are not replaced by the machine. You are promoted above it.'
)

para(
    'This is not science fiction. This is what the technology services industry '
    'looks like when the AI-Driven Lifecycle — what we call ADLC — is '
    'fully achieved. It is the destination at the end of the transformation journey '
    'that many organisations have already started.'
)

para(
    'This document tells that story: what changes, what it means for your people, '
    'your clients, and your business model — and what to do next.'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  1. THE WORLD WE KNOW
# ══════════════════════════════════════════════════════════════════════════════

h1('The World We Know')

para(
    'Today, delivering a new capability for a client — say, a loan pre-approval '
    'feature for a bank, or a claims-processing update for an insurer — looks '
    'something like this:'
)

para(
    'A business analyst writes the requirements. An architect designs the solution. '
    'A team of developers builds it. A separate team tests it. Another team packages '
    'and deploys it. A support team monitors it. Along the way, there are handoff '
    'meetings, approval queues, waiting periods, and coordination overhead.'
)

para(
    'A typical engagement involves 50 to 150 people. The feature takes 3 to 6 months '
    'to reach the customer. And here is the uncomfortable truth: when you measure the '
    'actual productive work versus the total elapsed time, only 5 to 12 percent of '
    'the time is spent doing useful work. The rest is waiting — waiting for '
    'approvals, waiting for environments, waiting for the next team in the chain to '
    'pick up what you put down.'
)

para(
    'The cost? Roughly $2,500 to $4,000 per unit of delivered work. The client pays '
    'for time, not outcomes. And every time you get more efficient, your revenue '
    'actually goes down — because you are selling hours, not results.'
)

quote(
    'For five hundred years, every century has brought an evolution — and each time, '
    'the organisations that adapted survived, while those that didn’t became history.',
    'From “Becoming a Frontier Professional”'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  2. THE WORLD THAT IS COMING
# ══════════════════════════════════════════════════════════════════════════════

h1('The World That Is Coming')

para(
    'Now imagine the same loan pre-approval feature — but delivered by a pod of '
    'two people and twenty-one digital agents.'
)

para(
    'The first person — let’s call her Priya — is the Product Definer. She '
    'understands the business problem deeply. She frames the outcome: “Customers '
    'should be able to get a loan decision in under 60 seconds, with zero manual '
    'underwriting for standard cases.” She sets the success measures. Then she directs '
    'an agent to draft the detailed specification, the test scenarios, and the user '
    'stories. She reviews and refines — but the agent does the heavy drafting in '
    'minutes, not days.'
)

para(
    'The second person — Arjun — is the Product Builder. He directs a fleet of '
    'agents to design the architecture, generate the code, write the tests, build the '
    'deployment pipeline, and ship it to production. Each agent is specialised: one '
    'writes code, another writes tests, another scans for security issues, another '
    'deploys. Arjun doesn’t write code line by line — he reviews what the agents '
    'produce, corrects what needs correcting, and makes the calls that no machine can '
    'make: trade-offs, risk decisions, and quality judgements.'
)

para(
    'A third person — Meera, a Frontier Principal — is shared across four pods. '
    'She sets the architecture standards, governs quality, and steps in when any '
    'pod hits a truly novel problem. Her designation is earned, not assigned — she '
    'has mastered both building and operating.'
)

para(
    'The feature ships in three days. Not three months. Three days.'
)

h2('What Just Happened?')

para(
    'Priya and Arjun didn’t work harder. They didn’t pull all-nighters. They '
    'directed and governed while their agents executed. Eighty-five percent of the '
    'actual work — the typing, the testing, the building, the deploying — was '
    'done by agents. The humans brought what agents cannot: business understanding, '
    'judgement, and accountability.'
)

para(
    'This is what we call a Frontier Pod. And every person in it is a Frontier '
    'Professional.'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  3. WHAT IS A FRONTIER PROFESSIONAL?
# ══════════════════════════════════════════════════════════════════════════════

h1('What Is a Frontier Professional?')

para(
    'Anyone, in any role, can grow into a Frontier Professional. You don’t need '
    'to be a programmer. A developer can become one. So can a tester, a consultant, '
    'an analyst, or someone in finance, HR, or procurement. The path is the same — '
    'only the domain changes.'
)

h2('The Journey — Four Stages')

para(
    'Think of it as a ladder. You start from wherever you are today, and you climb — '
    'one stage at a time.'
)

table(
    ['Stage', 'What It Looks Like', 'Your Relationship with Agents'],
    [
        ['Stage 0\nYour role today',
         'You do the work by hand. Your capacity is capped by your own hours.',
         'No agents. Tools are passive — spreadsheets, email, manual processes.'],
        ['Stage 1\nAgent-Assisted',
         'You pick one repetitive task and hand it to an agent. You review and approve its output.',
         'You direct agents. They draft; you decide.'],
        ['Stage 2\nFrontier Engineer\nor Operator',
         'You work in a pod of 1–3 people. Agents handle 80% of the work. You own the outcome end-to-end.',
         'You orchestrate agents. They execute the full lifecycle — build, test, deploy, monitor.'],
        ['Stage 3\nFrontier Principal',
         'You have mastered both building and operating. You are shared across 3–5 pods as the strategic anchor.',
         'You govern agents across multiple pods. You set the standards that all agents follow.'],
    ],
    widths=[1.2, 2.5, 2.5],
)

para(
    'It leads to two archetypes: the Frontier Engineer, who builds and deploys '
    'AI-native systems; and the Frontier Operator, who runs and governs AI-enabled '
    'operations. Master both, and you earn the Frontier Principal designation.'
)

h2('Six Principles That Anchor the Model')

para(
    'The Frontier model is built on six principles. They are worth stating because '
    'they represent a fundamental shift in how we think about professional work:'
)

bullet(
    'Blend business, design, engineering, and operations in one person. No more '
    '“I’m just the developer” or “that’s not my job.”',
    'Interdisciplinary capability.'
)
bullet(
    'Every effort ties to a measurable outcome for the customer or the business. '
    'If you cannot explain how your work creates value, it shouldn’t be done.',
    'Direct linkage to customer value.'
)
bullet(
    'Working alongside agents is as routine as using email. It’s not an innovation '
    'project — it’s how work gets done.',
    'Agents as routine.'
)
bullet(
    'You own the outcome from problem to running solution. Not your piece of it — '
    'all of it.',
    'End-to-end accountability.'
)
bullet(
    'Small 1–3 person pods, not large handoff chains. The pod is you, multiplied, '
    'with agents doing the execution.',
    'The pod is the unit of delivery.'
)
bullet(
    'The client sees one team, one front door. Not a matrix of roles and escalation paths.',
    'One unified experience for the client.'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  4. THE NEW LITERACY
# ══════════════════════════════════════════════════════════════════════════════

h1('The New Literacy')

para(
    'Here is the good news: unlike every previous technology shift, there is no '
    'programming language to learn. No Java. No .NET. No Python.'
)

para(
    'The new literacy is more human. It is three things:'
)

h3('1. Understand the problem — deeply')
para(
    'The AI models are not the hard part anymore. What’s hard is building the bridge '
    'from a model to real enterprise value: the workflows, the controls, the '
    'guardrails, the trust, the context, the institutional knowledge. That bridge is '
    'built by people who understand the domain. A Frontier Engineer who understands '
    'lending will outperform one who doesn’t — no matter how good the agents are.',
    indent=0.3,
)

h3('2. Direct the agents')
para(
    'Prompting is the new management. Just as a good manager gives clear direction, '
    'provides context, and sets expectations — a good Frontier Professional gives '
    'clear direction to agents. The quality of what the agents produce is directly '
    'proportional to the quality of the direction you give them.',
    indent=0.3,
)

h3('3. Bring your judgement')
para(
    'The agents do the heavy lifting. What you bring — and keep growing — is the '
    'judgement to know what “good” looks like, the instinct to spot when the machine '
    'is confidently wrong, and the governance to own the outcome. That is the real craft.',
    indent=0.3,
)

quote(
    'Being an AI builder is not something we add on top of how we are organised '
    '— it is how we are organised.',
    'Ravi Kumar S, CEO, Cognizant'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  5. INSIDE THE POD — HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════════

h1('Inside the Pod — How It Works')

para(
    'Let’s open up the pod and see what’s inside. A typical Frontier Pod has two '
    'to three people and a fleet of fifteen to twenty-one specialised agents. The '
    'humans make up about 15% of the workforce; the agents make up the other 85%.'
)

h2('The People')

para(
    'Product Definer (1 person) — Understands the business problem. Sets the '
    '“what” and the “why.” Directs an agent to draft the specifications, then '
    'reviews and refines. Owns the customer outcome — every feature maps to a '
    'measurable result.'
)

para(
    'Product Builder (1 person) — Directs the fleet of building, testing, and '
    'deployment agents. Reviews what they produce. Clears the exceptions that agents '
    'escalate. Owns the quality and the operations — from code to production.'
)

para(
    'Frontier Principal (shared across 3–5 pods, roughly 0.2–0.3 of their time '
    'per pod) — Sets the standards. Governs quality across the fleet. Steps in '
    'for truly novel problems. Earned, not assigned.'
)

h2('The Agents')

para(
    'Think of the agents as a team of tireless specialists. Each one is expert in '
    'a narrow area — and together they cover the entire lifecycle from idea to '
    'running product. The humans don’t need to know how each agent works internally; '
    'they need to know what to ask for and how to judge the output.'
)

para('Here is the fleet, organised by what they do:')

table(
    ['What Needs Doing', 'Agent Name', 'What the Agent Does'],
    [
        ['Define the work',        'Define Agent',       'Drafts specifications, test scenarios, and user stories from the Product Definer’s direction'],
        ['Design the solution',    'Architecture Agent', 'Recommends technical approaches and designs the blueprint'],
        ['Design the experience',  'UX/Design Agent',    'Creates screen layouts and user interface designs from requirements'],
        ['Write the software',     'CodeGen Agent',      'Generates the actual working software — screens, services, data models'],
        ['Write the tests',        'TestGen Agent',      'Creates comprehensive quality checks, covering normal cases and edge cases'],
        ['Review the quality',     'Review Agent',       'Examines all work for defects, security issues, and quality standards'],
        ['Check security',         'Security Agent',     'Continuously scans for vulnerabilities with very low false alarms'],
        ['Build the package',      'Build Agent',        'Compiles and packages everything, optimised for speed'],
        ['Deploy to customers',    'Deploy Agent',       'Releases gradually to customers with automatic rollback if issues arise'],
        ['Coordinate testing',     'QA Orchestrator',    'Selects the right tests to run and executes them in parallel'],
        ['Test performance',       'Performance Agent',  'Simulates real-world load to ensure the product handles peak demand'],
        ['Generate test data',     'DataGen Agent',      'Creates realistic, privacy-safe data for testing purposes'],
        ['Manage infrastructure',  'IaC Agent',          'Generates and validates the cloud infrastructure configuration'],
        ['Manage releases',        'Release Agent',      'Scores release readiness and auto-generates release documentation'],
        ['Monitor production',     'APM Agent',          'Watches the live product for issues and correlates problems with recent changes'],
        ['Handle incidents',       'Incident Agent',     'Categorises issues, routes them, and drafts root-cause analysis'],
        ['Analyse feedback',       'Feedback Agent',     'Distils customer feedback, support tickets, and usage data into actionable insights'],
        ['Check compliance',       'Compliance Agent',   'Validates every change against regulatory requirements in real time'],
        ['Manage model risk',      'MRM Agent',          'Monitors AI model behaviour, detects drift, and triggers safety measures'],
        ['Monitor agent health',   'Telemetry Sentinel', 'Translates agent performance data into business risk indicators'],
        ['Govern the fleet',       'Governance Controller', 'Ensures no agent bypasses safety or compliance rules — the “agent of agents”'],
    ],
    widths=[1.4, 1.3, 3.5],
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  6. HOW IT PLAYS OUT — THREE STORIES
# ══════════════════════════════════════════════════════════════════════════════

h1('How It Plays Out — Three Stories')

para(
    'The best way to understand the Frontier model is to see it in action. Here are '
    'three stories — each showing a different type of professional, in a different '
    'industry, at a different point on the journey.'
)

# ── Story 1 ──

h2('Story 1: Priya — Instant Loan Pre-Approval (Banking)')

para(
    'Priya is a Product Definer at a banking client. The bank wants to offer instant '
    'loan pre-approval — customers get a decision in under 60 seconds instead of '
    'waiting days.'
)

para(
    'In the old world, this would be a 10-week project with 30 people: analysts, '
    'architects, developers, testers, deployment engineers, and a release manager. '
    'Multiple handoffs, weekly status meetings, and a 2-week testing cycle at the end.'
)

para(
    'In Priya’s pod, it goes like this:'
)

para(
    'Morning: Priya frames the outcome and directs her Define Agent to draft the '
    'specification. Within an hour, she has a complete spec, test scenarios, and '
    'twelve user stories. She reviews, adjusts two edge cases, and approves.',
    indent=0.3,
)

para(
    'Midday: Arjun, the Product Builder, directs the Architecture Agent and CodeGen '
    'Agent. By lunch, the solution design is complete and the first working code is '
    'generated. Arjun reviews the architecture decision and the code quality, makes '
    'three corrections, and moves on.',
    indent=0.3,
)

para(
    'Afternoon: TestGen Agent writes tests covering 95% of scenarios. QA Orchestrator '
    'runs them all in parallel. Performance Agent simulates 10,000 concurrent users. '
    'Security Agent scans everything. All automated. Arjun reviews the results — '
    'two edge cases need attention. He fixes them.',
    indent=0.3,
)

para(
    'Day 2: Deploy Agent ships to production with a gradual rollout. Release Agent '
    'auto-generates release notes. APM Agent monitors. Everything is green.',
    indent=0.3,
)

para(
    'Day 3: First customers are using the feature. Feedback Agent synthesises early '
    'usage data. Priya reviews — approval rates are tracking to target. Done.',
    indent=0.3,
)

h3('The numbers')
bullet('Two people, three days. Not thirty people, ten weeks.', indent=0.5)
bullet('Cost: roughly $6,000. Not $400,000.', indent=0.5)
bullet('Test coverage: 95%. Not 45%.', indent=0.5)
bullet('Security vulnerabilities at release: zero. Not “we’ll fix them in the next sprint.”', indent=0.5)

divider()

# ── Story 2 ──

h2('Story 2: Kavitha — Autonomous Month-End Close (Finance)')

para(
    'Kavitha is a finance analyst at a large corporation. Every month, she and her '
    'team spend six days reconciling ledgers, chasing variances, investigating breaks, '
    'and building the month-end close report. It’s manual, error-prone, and exhausting.'
)

para(
    'Kavitha doesn’t write code. She never has. But she follows the same four-stage '
    'journey:'
)

para(
    'Stage 0 (today): She does everything by hand — pulls data from multiple systems '
    'into spreadsheets, matches entries line by line, investigates every discrepancy '
    'through emails and calls.',
    indent=0.3,
)

para(
    'Stage 1 (agent-assisted): She directs agents to pull and normalise the data, '
    'auto-reconcile the straightforward matches, and draft the commentary. She reviews '
    'and approves.',
    indent=0.3,
)

para(
    'Stage 2 (Frontier Operator): Kavitha defines the operating model for an '
    '“autonomous month-end close.” She sets the policies, the controls, the KPIs. '
    'Agents run the entire process end-to-end. Kavitha governs by exception — she '
    'only gets involved when something breaks or a threshold is crossed.',
    indent=0.3,
)

h3('The transformation')

table(
    ['Step', 'Before (Manual)', 'After (Frontier Operator)'],
    [
        ['Pull the data',        'Exports from many systems, by hand',                   'Agents ingest and normalise automatically'],
        ['Reconcile',            'Line-by-line manual matching',                         'Agents auto-match 97% of entries; only exceptions surface'],
        ['Investigate breaks',   'Emails, calls, manual digging',                        'Agents detect, investigate, and propose adjustments'],
        ['Report and close',     'Hand-built report, error-prone — 6 days',         'Auto-generated with full audit trail — same day'],
        ['Kavitha’s role',  'Doer — processes every line',                     'Governor — sets policy, owns controls, clears exceptions'],
    ],
    widths=[1.3, 2.2, 2.7],
)

para(
    'Kavitha is not a technologist. She is a finance professional who learned to '
    'direct agents. That’s the point: the ladder is open to everyone.'
)

divider()

# ── Story 3 ──

h2('Story 3: Rajan — Self-Service Policy Endorsements (Insurance)')

para(
    'Rajan’s pod is asked to build a self-service policy endorsement flow for an '
    'insurance client. In the traditional model, this is an 8-week, 20-person effort.'
)

para(
    'Rajan’s pod delivers it in 5 days, with 92% test coverage and a clean security '
    'scan — zero critical findings. The change-failure rate is under 5%, compared to '
    'the industry average of 15–30%.'
)

para(
    'More importantly: the client paid for the capability, not for 20 people’s time. '
    'The cost was a fraction. The quality was higher. And the pod has already moved '
    'on to the next capability.'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  7. THE BEFORE-AND-AFTER — IN NUMBERS
# ══════════════════════════════════════════════════════════════════════════════

h1('The Before-and-After — In Numbers')

para(
    'Stories are compelling. Numbers make them real. Here is what changes when the '
    'Frontier Pod model replaces the traditional IT services model:'
)

table(
    ['What We Measure', 'Traditional Model', 'Frontier Pod Model', 'The Change'],
    [
        ['People per engagement',        '50–150',               '2–3 per pod',            '↓ 97%'],
        ['Workforce mix',                '95% human / 5% tools',     '15% human / 85% agents',     'Inverted'],
        ['Time to first customer value', '3–6 months',           '1–2 weeks',              '↓ 95%'],
        ['Cost per unit of work',        '$2,500–$4,000',        '$200–$600',              '↓ 85–90%'],
        ['Productive work vs waiting',   '5–12%',               '65–85%',                 '↑ 7–10×'],
        ['Release frequency',           'Monthly or quarterly',      'Multiple times per day',      '↑ 60×+'],
        ['Time from code to customer',   '2–8 weeks',           '1–3 days',               '↓ 90–95%'],
        ['Things that break after release','15–30%',            'Under 3%',                    '↓ 80–90%'],
        ['Recovery when things break',   '4–24 hours',          'Under 30 minutes',            '↓ 90%+'],
        ['Quality coverage',             '40–65%',              '92–98%',                  '↑ 2×'],
        ['Security issues at release',   '5–15 serious issues', 'Zero serious issues',         'Eliminated'],
        ['Client value per dollar spent','$0.08–$0.12',        '$0.60–$0.80',            '↑ 7×'],
        ['Revenue per person (monthly)', '$16K',                     '$70K',                        '↑ 4.4×'],
    ],
    widths=[1.6, 1.3, 1.3, 0.8],
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  8. WHAT THIS MEANS FOR SERVICE PARTNERS
# ══════════════════════════════════════════════════════════════════════════════

h1('What This Means for Service Partners')

para(
    'If you run or work in a technology services company, the Frontier Pod model '
    'changes everything about how your business works. Not just the technology — '
    'the economics, the talent model, the client relationship, and the competitive '
    'landscape.'
)

h2('The Business Model Shifts')

h3('From selling time to selling outcomes')
para(
    'Today, most service partners bill by the hour or by the person-month. Revenue '
    'scales linearly with headcount: more people, more revenue. But here’s the '
    'paradox: every efficiency improvement you make reduces your revenue, because '
    'you are selling effort, not results.',
    indent=0.2,
)

para(
    'In the Frontier model, you sell outcomes. The client pays for a capability '
    'delivered — a working feature, an automated process, a running operation. '
    'Your efficiency improvements increase your margin instead of reducing your '
    'revenue. A pod that delivers faster is more profitable, not less.',
    indent=0.2,
)

h3('The economics, side by side')

table(
    ['', 'Traditional Model', 'Frontier Pod Model'],
    [
        ['What you sell',           'People’s time',                                 'Outcomes delivered'],
        ['Typical team size',       '80 people per engagement',                          '2–3 people per pod'],
        ['Monthly revenue',         '$1.28M (80 people × $800/day)',                 '$175K per pod'],
        ['But throughput is…', '1× (baseline)',                                 '10–20× per person'],
        ['Gross margin',            '18–25%',                                        '40–55%'],
        ['Revenue per person',      '$16K/month',                                        '$70K/month'],
        ['Value the client gets',   '$0.08–$0.12 per dollar',                       '$0.60–$0.80 per dollar'],
        ['How you scale',           'Hire more people',                                  'Add more pods (each amplified by agents)'],
    ],
    widths=[1.4, 2.2, 2.6],
)

h2('The Talent Model Shifts')

para(
    'The traditional services model is a pyramid: many juniors at the base, a few '
    'seniors at the top. Juniors do the volume work; seniors provide oversight.'
)

para(
    'The Frontier model is a diamond. Everyone is at Frontier level — Stage 2 or '
    'above. The volume work is done by agents, not juniors. The humans provide '
    'direction, judgement, and governance. There is no “junior developer who '
    'hand-codes screens.” There is a Frontier Engineer who directs agents to build '
    'and ships end-to-end.'
)

para(
    'This means fewer people, but each person is far more valuable. Revenue per '
    'person grows from $16K/month to $70K/month — a 4.4× increase. The '
    'professional is no longer a cost line to be minimised; they are a capability '
    'multiplier.'
)

h2('The Client Relationship Shifts')

para(
    'Today, clients often see their service partner as an “extended headcount '
    'provider.” The relationship is transactional: I give you requirements, you '
    'give me people, I pay by the month.'
)

para(
    'In the Frontier model, the client sees a pod — a small, accountable team '
    'that owns the outcome end-to-end. One front door. One relationship. No '
    'escalation paths through three layers of management. The client pays for '
    'what they get, not for how many people it took. And they get it in days, '
    'not months.'
)

para(
    'This is the shift from vendor to partner — a word that has been overused but, '
    'in the Frontier model, finally earns its meaning.'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  9. AT SCALE — THE PORTFOLIO VIEW
# ══════════════════════════════════════════════════════════════════════════════

h1('At Scale — What the Numbers Look Like')

para(
    'Let’s zoom out. Imagine a service partner that has scaled the Frontier model '
    'to 100 concurrent pods across 20 clients.'
)

bullet('250 Frontier Engineers (100 pods at 2.5 people average)', indent=0.5)
bullet('2,100 agents (100 pods at 21 agents each)', indent=0.5)
bullet('$17.5 million in monthly revenue (100 pods at $175K each)', indent=0.5)
bullet('$210 million in annual revenue — from 250 people', indent=0.5)

para(
    'In the traditional model, generating equivalent throughput would require roughly '
    '8,000 to 13,000 people. The Frontier model achieves the same output with 250 '
    'people and 2,100 agents — a 30 to 50 times leverage ratio.'
)

para(
    'Revenue per person: $840,000 per year. Compared to $192,000 per year in the '
    'traditional model. That is a 4.4× improvement in the most important metric '
    'a services business has.'
)

para(
    'And here is the compounding effect: every pod run generates data that improves '
    'the agents. Better agents mean less human intervention. Less intervention means '
    'each person can oversee more pods. The flywheel spins faster the longer you run it.'
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  10. WHAT CHANGES FOR EVERYONE
# ══════════════════════════════════════════════════════════════════════════════

h1('What Changes for Everyone')

h2('For the Professional')

para(
    'Your influence is no longer capped by your own hours. It is multiplied by how '
    'well you direct agents and a pod — a step-change in leverage and a richer, '
    'more durable career.'
)

table(
    ['', 'Before', 'After'],
    [
        ['Your influence',     'Capped by your hours',                            'Multiplied by your direction of agents'],
        ['Your career',        'Role-specific, vulnerable to automation',         'Interdisciplinary, grows more valuable with AI'],
        ['Your scope',         'One task in a handoff chain',                     'End-to-end — problem to running solution'],
        ['Your daily work',    'Repetitive execution, burnout risk',             'Strategic direction, judgement, governance'],
        ['Your earning power', 'Linear with hours worked',                       'Scales with outcomes delivered'],
    ],
    widths=[1.2, 2.2, 2.8],
)

h2('For the Organisation')

table(
    ['', 'Before', 'After'],
    [
        ['Handoffs',              '8–12 per feature lifecycle',            'Zero — one owner, one pod'],
        ['Time to value',         'Months',                                     'Days'],
        ['How work gets done',    'People do it, management supervises',        'Agents do it, people govern by exception'],
        ['Revenue per person',    '$16K/month',                                 '$70K/month'],
        ['Client satisfaction',   'SLAs and escalation metrics',                'Outcomes delivered'],
    ],
    widths=[1.5, 2.2, 2.5],
)

h2('For the Client')

table(
    ['', 'Before', 'After'],
    [
        ['Annual cost',          '$1.2M+ per team',                             '$200K–$400K per pod'],
        ['Speed',                 'Quarterly releases',                         'Continuous — multiple per day'],
        ['Quality',               '40–65% tested, 15–30% failures',   '95%+ tested, under 3% failures'],
        ['Transparency',          'Monthly status reports',                     'Real-time dashboards, full audit trail'],
        ['Security',              'Periodic audits',                             'Continuous, zero critical issues at release'],
        ['Knowledge risk',        'Locked in people’s heads',              'Encoded in agents — portable and auditable'],
    ],
    widths=[1.3, 2.2, 2.7],
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  11. WHAT TO DO NEXT
# ══════════════════════════════════════════════════════════════════════════════

h1('What To Do Next')

para(
    'This shift doesn’t happen overnight. It mirrors the same staged journey that '
    'every individual takes — Stage 0 to Stage 3 — but at the organisational level. '
    'Here are the concrete next steps, organised in three horizons.'
)

h2('Now — Build the Foundation (Q1–Q2)', color=BLUE)

h3('1. Start the Academy')
para(
    'Train your first 500 professionals on the Frontier journey. Everyone picks one '
    'repetitive task from their current role and hands it to an agent. That is '
    'Stage 1 — and it creates the talent pipeline for everything that follows. '
    'Without this, the rest doesn’t work.',
    indent=0.3,
)

h3('2. Assess Yourself First')
para(
    'Use the STUMP platform to map your own delivery process. Measure where time goes '
    'today. Identify the bottlenecks. Baseline your metrics. This gives you credibility '
    'when you take it to clients: “We transformed ourselves first.”',
    indent=0.3,
)

h3('3. Build the Agent Library')
para(
    'Create a set of reusable agents that any pod can pick from. Don’t build agents '
    'per project — build them as a shared capability. Think of it like a library of '
    'tireless specialists that any team can draw on.',
    indent=0.3,
)

h3('4. Run 3–5 Pilot Pods')
para(
    'Pick a few client engagements and pilot the pod model. Start with the hybrid stage '
    '(50% automation, humans still in many roles) before going to full autonomy. Generate '
    'proof points and stories you can tell.',
    indent=0.3,
)

h2('Next — Scale the Model (Q3–Q4)', color=EMERALD)

h3('5. Graduate Your First 100 Frontier Engineers')
para(
    'Move people from Stage 1 (agent-assisted) to Stage 2 (Frontier Engineer or '
    'Operator). Each graduate owns a pod and delivers end-to-end. Your service capacity '
    'grows tenfold with one-tenth the headcount per engagement.',
    indent=0.3,
)

h3('6. Launch Outcome-Based Pricing')
para(
    'Move from billing by the hour to billing by the outcome. Price per capability '
    'delivered, not per person-day. Your margins improve from 20% to 45% or better, '
    'while the client’s costs drop 60–70%.',
    indent=0.3,
)

h3('7. Package It as a Service')
para(
    'Combine the assessment platform with the Frontier pod deployment into a turnkey '
    'offering: Assess, Transform, Operate — in 90 days. This creates a repeatable '
    'go-to-market motion that you can scale across industries.',
    indent=0.3,
)

h3('8. Build the Governance Layer')
para(
    'Deploy the governance agents (compliance checking, model risk management, agent '
    'oversight) across all pods. This is mandatory for regulated industries — banking, '
    'insurance, healthcare — and unlocks the largest clients.',
    indent=0.3,
)

h2('Future — Reinvent the Industry (Year 2+)', color=AMBER)

h3('9. Certify Frontier Principals')
para(
    'Identify your best people — those who have mastered both building and operating '
    '— and certify them as Frontier Principals. They become the strategic anchors '
    'across your pod fleet. This is the rarest, highest-value talent tier in the industry.',
    indent=0.3,
)

h3('10. Scale to 100+ Pods')
para(
    '100 concurrent pods, 20+ clients, 250 Frontier Engineers, 2,100 agents. Revenue '
    'per person grows 4–5× versus the traditional model. The flywheel compounds '
    '— every pod run improves the agents, which reduces human intervention, which '
    'enables more pods per person.',
    indent=0.3,
)

h3('11. Build Industry-Specific Pod Templates')
para(
    'Pre-configure agent fleets for specific industries: banking (lending, payments, '
    'compliance), insurance (claims, underwriting), telecom (network, customer '
    'experience). Time to deploy a new pod drops from weeks to days. '
    'Pod-as-a-product.',
    indent=0.3,
)

h3('12. The Continuous Improvement Flywheel')
para(
    'Every pod run generates data. That data improves agent accuracy. Better accuracy '
    'reduces human intervention. Less intervention means each person can oversee more '
    'pods. More pods means more data. The cycle compounds.',
    indent=0.3,
)

doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
#  12. CLOSING
# ══════════════════════════════════════════════════════════════════════════════

h1('The Ladder Is Open')

para(
    'The shift to the Frontier Pod model is the most significant structural change '
    'in technology services since the offshoring wave of the 2000s. But unlike that '
    'shift, which was about finding cheaper labour, this one is about amplifying human '
    'judgement with machine execution.'
)

para(
    'The gap between AI capability and real enterprise value is not getting narrower '
    '— it is getting wider. The models are racing ahead, but the bridge to production '
    'value (the workflows, the controls, the guardrails, the trust, the context, the '
    'institutional knowledge) is built by people. Frontier Professionals. Working '
    'in pods. Amplified by agents.'
)

para(
    'The organisations that act now — training their people, building their agent '
    'libraries, piloting pods, shifting to outcome-based pricing — will own the '
    'next era of technology services.'
)

para(
    'Those that wait will find themselves competing for shrinking hourly-billing '
    'contracts in a market that has moved to outcomes.'
)

quote(
    'As a systems integrator, we either become an AI builder or become history. And '
    'a technology partner’s success is simply the sum of its people’s: if each of us '
    'makes the shift, the organisation thrives.',
    'From “Becoming a Frontier Professional”'
)

para('')  # spacer

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('The ladder is open.')
sf(r, size=16, bold=True, color=NAVY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(4)
r = p.add_run('The only question is when you start climbing.')
sf(r, size=14, italic=True, color=BLUE)

divider()

# Attribution
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(14)
r = p.add_run(
    'This document is based on “Becoming a Frontier Professional” by '
    'Porkkovan Elangovan and Khirthika V. An internal point of view. The journey, '
    'characters, and figures are illustrative; archetypes, principles, and pathways '
    'follow the Frontier operating-model design. Outcomes depend on adoption maturity '
    'and governance.'
)
sf(r, size=9, italic=True, color=GRAY)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER


# ── Save ──────────────────────────────────────────────────────────────────────
OUTPUT = 'Frontier-Professional-Post-ADLC-POV.docx'
doc.save(OUTPUT)
print(f'\n✅  Saved: {OUTPUT}')
print(f'   12 sections, narrative/storytelling format')
print(f'   Business-friendly — no jargon, story-driven, human-centred')
print(f'   Covers: The Shift, Frontier Framework, Pod Model, Stories,')
print(f'           Economics, Impact, Next Steps, Scale Portfolio')
