"""
Build Set 1 v2 — AI-Powered PDLC Transformation GTM Pack
Offering-centric narrative: DIAGNOSE → DESIGN → DELIVER
Platform = accelerator, NOT the product.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gtm_model_2026 as M  # shared 2026 narrative

OUT = "/Users/125066/projects/pdlc-vsm-platform/gtm-pack/set1-v2"
os.makedirs(OUT, exist_ok=True)

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Colors ──────────────────────────────────────────────────────────────────
NAVY  = RGBColor(0x0F, 0x2D, 0x5E)
BLUE  = RGBColor(0x25, 0x63, 0xEB)
TEAL  = RGBColor(0x0D, 0x94, 0x88)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY  = RGBColor(0x4B, 0x55, 0x63)
LGRAY = RGBColor(0xF3, 0xF4, 0xF6)
AMBER = RGBColor(0xD9, 0x77, 0x06)
GREEN = RGBColor(0x05, 0x96, 0x69)

# ══════════════════════════════════════════════════════════════════════════════
# DOCX HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def new_doc():
    d = Document()
    s = d.sections[0]
    s.page_width  = Inches(8.5)
    s.page_height = Inches(11)
    s.left_margin = s.right_margin = Inches(1.0)
    s.top_margin  = s.bottom_margin = Inches(0.9)
    return d

def sf(run, size=11, bold=False, italic=False, color=None, name='Calibri'):
    run.font.name  = name
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run(text)
    sf(r, 16, True, color=NAVY)
    return p

def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    sf(r, 13, True, color=BLUE)
    return p

def h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    sf(r, 11, True, color=NAVY)
    return p

def body(doc, text, italic=False, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    sf(r, 10.5, italic=italic, color=color)
    return p

def bul(doc, text, bold_pre=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(2)
    if bold_pre:
        rb = p.add_run(bold_pre + ": ")
        sf(rb, 10.5, True)
    r = p.add_run(text)
    sf(r, 10.5)
    return p

def num(doc, text):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    sf(r, 10.5)
    return p

def set_cell_bg(cell, hex_c):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_c)
    tcPr.append(shd)

def tbl(doc, headers, rows, col_widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    hr = t.rows[0]
    for i, h in enumerate(headers):
        c = hr.cells[i]
        set_cell_bg(c, '0F2D5E')
        p = c.paragraphs[0]
        r = p.add_run(h)
        sf(r, 9.5, True, color=WHITE)
    for idx, rd in enumerate(rows):
        row = t.add_row()
        fill = 'F3F4F6' if idx % 2 == 0 else 'FFFFFF'
        for i, v in enumerate(rd):
            cell = row.cells[i]
            set_cell_bg(cell, fill)
            r = cell.paragraphs[0].add_run(str(v))
            sf(r, 9.5)
    if col_widths:
        for row in t.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return t

def divider(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(3)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), '2563EB')
    pBdr.append(bot)
    pPr.append(pBdr)

def callout(doc, text, fill='DBEAFE'):
    t = doc.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    c = t.rows[0].cells[0]
    set_cell_bg(c, fill)
    p = c.paragraphs[0]
    r = p.add_run(text)
    sf(r, 10.5, italic=True, color=NAVY)
    doc.add_paragraph()

def cover_page(doc, title, subtitle, doc_num):
    # Navy banner
    t = doc.add_table(rows=1, cols=1)
    t.style = 'Table Grid'
    c = t.rows[0].cells[0]
    set_cell_bg(c, '0F2D5E')
    c.width = Inches(6.5)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run("AI-Powered PDLC Transformation")
    sf(r, 22, True, color=WHITE)
    p2 = c.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("GTM Pack — Set 1: CXO GTM Pack")
    sf(r2, 13, color=RGBColor(0xDB, 0xEA, 0xFE))
    p3 = c.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run(doc_num)
    sf(r3, 11, italic=True, color=RGBColor(0xDB, 0xEA, 0xFE))
    p3.paragraph_format.space_after = Pt(20)

    doc.add_paragraph()
    pt = doc.add_paragraph()
    pt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = pt.add_run(title)
    sf(rt, 26, True, color=NAVY)

    ps = doc.add_paragraph()
    ps.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = ps.add_run(subtitle)
    sf(rs, 14, italic=True, color=BLUE)

    divider(doc)

    pb = doc.add_paragraph()
    pb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rb = pb.add_run("DIAGNOSE · DESIGN · DELIVER · Accelerated by AI")
    sf(rb, 11, color=GRAY)

    doc.add_page_break()


# ══════════════════════════════════════════════════════════════════════════════
# DOC 02 — CXO QUESTION BANK
# ══════════════════════════════════════════════════════════════════════════════
print("Building 02-cxo-question-bank.docx...")
doc = new_doc()
cover_page(doc,
           "CXO Discovery Question Bank",
           "20 Questions That Lead to Phase 1 Diagnose",
           "Document 02 of 10")

h1(doc, "Purpose of This Question Bank")
body(doc, "These 20 structured discovery questions are designed to be used by consulting leads and account executives during executive conversations. They are sequenced to surface PDLC pain, quantify its cost, gauge transformation appetite, and build a natural case for engaging Phase 1: Diagnose.")
body(doc, "Each question is annotated with its strategic intent and the insight it generates toward selecting the right transformation option (A, B, or C) and closing Phase 1.")
callout(doc, "Objective: Every conversation should end with the executive saying — 'We need to understand exactly what our PDLC is costing us. How do we start?'")

divider(doc)

h2(doc, "Theme 1: Understanding Current PDLC Pain")
body(doc, "Frame: Speed / Productivity / Quality. Goal: Surface the felt pain and connect it to a financial cost.")
body(doc, "These questions open the conversation. They should feel like genuine curiosity, not interrogation. Let the executive narrate. Note the specific numbers they quote — or, importantly, their inability to quote them.")

num(doc, "When a feature is committed to in planning, how long does it typically take to reach production? And how much of that time is actual engineering work versus waiting?")
bul(doc, "Intent: Reveal lead time and flow efficiency. Most executives will guess — very few know. The inability to answer is itself a pain signal.", bold_pre="Note")

num(doc, "If I asked your VP of Engineering to tell me, today, the three biggest bottlenecks in your software delivery pipeline — with data to back them up — could they do it in under an hour?")
bul(doc, "Intent: Test data readiness and engineering visibility. The answer is almost always 'probably not, at least not with hard numbers.'", bold_pre="Note")

num(doc, "How do your teams know when a process step is taking too long? Is there a threshold, an alert, a review cadence — or does it surface when something is late?")
bul(doc, "Intent: Uncover whether PDLC monitoring is reactive or proactive. Most orgs are reactive — this highlights the need for continuous measurement.", bold_pre="Note")

num(doc, "In the last 12 months, how many transformation or delivery improvement initiatives have been launched? How many are still active, and what measurable improvement have they produced?")
bul(doc, "Intent: Reveal transformation fatigue and the disconnect between effort and outcomes. Often surfaces 'initiative graveyard' problem.", bold_pre="Note")

num(doc, "When your board asks 'are we getting faster?' — what data do you present, and how confident are you that it reflects reality rather than vanity metrics?")
bul(doc, "Intent: Test the quality of existing measurement. Surfaces the gap between reporting and ground truth, and the board-level exposure.", bold_pre="Note")

divider(doc)

h2(doc, "Theme 2: Quantifying the Bottleneck Cost")
body(doc, "Frame: Every week of lead time waste has a dollar cost. These questions build the business case for Phase 1.")
body(doc, "The goal here is to translate operational pain into financial terms. Executives respond to cost. If you can help them estimate the annual cost of their current PDLC waste in this conversation, they become sponsors of the diagnosis.")

num(doc, "If your average feature takes 30 working days to deliver, and world-class teams in your sector deliver comparable features in 8–10 days — what would an extra 20 days of speed be worth to your business annually?")
bul(doc, "Intent: Anchor the financial case. Help them think in terms of revenue capture, competitive response, and cost avoidance.", bold_pre="Note")

num(doc, "What percentage of your engineering capacity do you believe is absorbed by rework, wait time, and coordination overhead rather than productive delivery?")
bul(doc, "Intent: Surface the productivity waste estimate. Many executives will say 20–40%. Even a conservative estimate translates to millions in misallocated salary.", bold_pre="Note")

num(doc, "Have you ever done a formal value stream mapping exercise? If so, how long did it take, what did it find, and what changed as a result?")
bul(doc, "Intent: Understand prior experience with VSM and whether it produced actionable outcomes. Most will say it took 3–4 months and gathered dust.", bold_pre="Note")

num(doc, "If you could see, in real time, how much of your software delivery is pure engineering value versus wait, queue, and rework — what decisions would you make differently?")
bul(doc, "Intent: Create desire for the diagnostic capability. This question makes the executive imagine having the data, which is a powerful pre-commitment.", bold_pre="Note")

num(doc, "What is the cost to your organisation — in customer impact, competitive position, and direct cost — of a one-month delay in a major feature release?")
bul(doc, "Intent: Quantify the cost of speed deficit in business terms the CFO will understand. This number often shocks executives into urgency.", bold_pre="Note")

divider(doc)

h2(doc, "Theme 3: Understanding Risk Appetite (Options A / B / C)")
body(doc, "Frame: The right transformation option depends on where the organisation sits on the risk/ambition spectrum.")
body(doc, "These questions guide the executive toward understanding their own appetite for AI-led transformation — without pushing. They surface the cultural, governance, and board context that determines whether Option A, B, or C is right.")

num(doc, "How comfortable is your organisation with AI making recommendations versus AI making decisions? Where do you want human judgment to remain in the loop?")
bul(doc, "Intent: Directly maps to Option A (human in the loop) vs B (human on the loop) vs C (human above the loop). Let them self-select.", bold_pre="Note")

num(doc, "When you think about AI in your engineering process — where has your board expressed the strongest concern? And where have they expressed the most excitement?")
bul(doc, "Intent: Uncover board-level AI posture. Concern signals preference for Option A; excitement opens the door to B or C.", bold_pre="Note")

num(doc, "Has your organisation piloted any AI-assisted development tools — GitHub Copilot, code review automation, test generation? What was the adoption and the outcome?")
bul(doc, "Intent: Assess current AI maturity. Prior positive pilots strongly predict readiness for Option B. Resistance signals Option A is the right start.", bold_pre="Note")

num(doc, "If you could guarantee a 4–6× ROI on a $1.5M transformation investment, what would need to be true for your board to approve it?")
bul(doc, "Intent: Pre-qualify Option B economics and surface board approval requirements. The answer shapes the CFO narrative for Phase 2.", bold_pre="Note")

num(doc, "On a scale of 1–10, how would you rate your organisation's readiness for a fully AI-autonomous software delivery pipeline — where AI agents execute, and humans review only at key gates?")
bul(doc, "Intent: Get a direct readiness self-assessment. Anything below 6 typically lands in Option A/B territory. 8+ opens Option C discussion.", bold_pre="Note")

divider(doc)

h2(doc, "Theme 4: Transformation Ambition")
body(doc, "Frame: Where does leadership want to be in 3 years? The ambition sets the destination; the options set the route.")

num(doc, "Three years from now, what does 'world-class software delivery' look like for your organisation? How would you describe it to a new board member?")
bul(doc, "Intent: Elicit the future state aspiration. This becomes the transformation north star and anchors the Phase 2 Design conversation.", bold_pre="Note")

num(doc, "What would need to be true for your engineering teams to be shipping meaningful product capability 3× faster than today — and sustaining that pace?")
bul(doc, "Intent: Surface the change requirements — people, process, governance, tooling. These become the transformation design inputs.", bold_pre="Note")

num(doc, "How important is it to your strategy that AI is deeply embedded in your delivery model — not just as a tool, but as a core operational capability?")
bul(doc, "Intent: Distinguish between AI as a utility (Option A mindset) and AI as strategic differentiator (Option B/C mindset).", bold_pre="Note")

divider(doc)

h2(doc, "Theme 5: Economic Buyer and Board Narrative")
body(doc, "Frame: Every transformation requires a committed sponsor. These questions identify who holds budget and what narrative will move them.")

num(doc, "Who in your organisation would own a PDLC transformation programme — and who holds the budget to fund it?")
bul(doc, "Intent: Map the economic buyer (CTO? CFO? CEO?). The answer determines where to focus Phase 2's business case.", bold_pre="Note")

num(doc, "If a transformation programme produced quantified evidence of a $3M annual benefit in your first year — what format would that need to be in for your CFO to champion it at the next board meeting?")
bul(doc, "Intent: Pre-design the Phase 2 business case output. Makes the executive visualise success — and creates pull toward Phase 1 to generate the evidence.", bold_pre="Note")

divider(doc)
h2(doc, "Closing Framework: Moving to Phase 1 Diagnose")
callout(doc, "After working through these questions, you should be able to say: 'Based on what you've told me, the single highest-value action right now is to get precise data on your PDLC. In 8 weeks, for a fixed investment, we will map your current state, quantify your bottleneck cost, and present you with three transformation options — each with a detailed business case. That becomes the decision package for your board. Would it be useful to show you how we do that?'")

body(doc, "The Phase 1 Diagnose engagement is the natural close from this conversation. It is low-risk ($150K fixed), time-bounded (8 weeks), and produces a decision package — not a vague report. The question bank above is designed to create the conditions where that close feels inevitable, not forced.")

doc.save(os.path.join(OUT, "02-cxo-question-bank.docx"))
print("  ✓ 02-cxo-question-bank.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 03 — SERVICE BRIEF ONE-PAGER
# ══════════════════════════════════════════════════════════════════════════════
print("Building 03-service-brief-one-pager.docx...")
doc = new_doc()

# Cover banner
t = doc.add_table(rows=1, cols=1)
t.style = 'Table Grid'
c = t.rows[0].cells[0]
set_cell_bg(c, '0F2D5E')
p = c.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(16)
r = p.add_run("AI-Powered PDLC Transformation")
sf(r, 28, True, color=WHITE)
p2 = c.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("Diagnose. Design. Deliver. Accelerated by AI.")
sf(r2, 14, italic=True, color=RGBColor(0xDB, 0xEA, 0xFE))
p3 = c.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = p3.add_run("GTM Pack — Set 1: CXO GTM Pack  |  Document 03 of 10")
sf(r3, 9, italic=True, color=RGBColor(0x93, 0xC5, 0xFD))
p3.paragraph_format.space_after = Pt(14)
doc.add_paragraph()

# THE CHALLENGE
h2(doc, "THE CHALLENGE")
body(doc, "Most software organisations are flying blind. The average team operates at 17% flow efficiency — meaning 83% of lead time is invisible waste: queues, handoffs, and rework. Boards demand transformation ROI in 12–18 months. AI-native competitors are shipping 3× faster. But without a precise diagnosis of where time is lost, any transformation programme is guesswork.")
doc.add_paragraph()

# THE OFFERING
h2(doc, "OUR THREE-PHASE OFFERING")
t2 = doc.add_table(rows=1, cols=3)
t2.style = 'Table Grid'
phases = [
    ("PHASE 1\nDIAGNOSE", "8 Weeks | Fixed Fee", "Organisation Setup & ALM Integration\nDORA Assessment (73-question)\nCurrent State VSM Map\nLegacy Modernisation Assessment\nBottleneck Analysis + Operations Intelligence\nSpeed / Productivity / Quality quantification\nThree transformation options with business case"),
    ("PHASE 2\nDESIGN", "Concurrent with Phase 1 close", "Option A / B / C detailed design\nGovernance & Guardrails framework\nAI Assurance protocols\nTransformation Readiness plan\nResponsible AI scorecard\nCFO-ready business case"),
    ("PHASE 3\nDELIVER", "Option-specific timeline", "Phased implementation (21-module platform)\nQuick wins in 90 days\nAIOps maturity progression\nBenefits tracking dashboard\nContinuous AI governance & assurance\nMeasured ROI at 12 months"),
]
for i, (title, timing, content) in enumerate(phases):
    cell = t2.rows[0].cells[i]
    set_cell_bg(cell, '0F2D5E')
    ph = cell.paragraphs[0]
    ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rh = ph.add_run(title)
    sf(rh, 11, True, color=WHITE)
    pt2 = cell.add_paragraph()
    pt2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt2 = pt2.add_run(timing)
    sf(rt2, 8, italic=True, color=RGBColor(0xDB, 0xEA, 0xFE))
    pc = cell.add_paragraph()
    rc = pc.add_run(content)
    sf(rc, 9, color=RGBColor(0xDB, 0xEA, 0xFE))
    cell.width = Inches(2.1)
doc.add_paragraph()

# THREE PATHWAYS
h2(doc, "THREE TRANSFORMATION PATHWAYS")
path_tbl = doc.add_table(rows=1, cols=6)
path_tbl.style = 'Table Grid'
for i, h in enumerate(["Option", "Model", "Speed", "Productivity", "Quality", "ROI"]):
    c = path_tbl.rows[0].cells[i]
    set_cell_bg(c, '0F2D5E')
    r = c.paragraphs[0].add_run(h)
    sf(r, 9, True, color=WHITE)
options_data = [
    ("A — AI-Augmented PDLC", "Human in the loop", "+25%", "+20%", "+15%", "2–3×  |  $350–600K"),
    ("B — AI Agents + Human Gates ★", "Human on the loop", "+55%", "+50%", "+35%", "4–6×  |  $1.2–2M"),
    ("C — Fully Agentic PDLC", "Human above the loop", "+75%", "+75%", "+60%", "8–12×  |  $3–5M"),
]
for idx, row_data in enumerate(options_data):
    row = path_tbl.add_row()
    fill = 'DBEAFE' if idx == 1 else ('F3F4F6' if idx % 2 == 0 else 'FFFFFF')
    for i, v in enumerate(row_data):
        cell = row.cells[i]
        set_cell_bg(cell, fill)
        r = cell.paragraphs[0].add_run(v)
        sf(r, 9, bold=(idx == 1))
col_ws = [2.3, 1.4, 0.7, 0.9, 0.7, 1.5]
for row in path_tbl.rows:
    for i, w in enumerate(col_ws):
        row.cells[i].width = Inches(w)
doc.add_paragraph()
callout(doc, "★ Option B is our recommended pathway for most enterprise organisations. It delivers 4–6× ROI with proven governance, and is the path US Bank took — achieving 42→8 days lead time in 18 months.")

# HOW WE ACCELERATE IT
h2(doc, "HOW WE ACCELERATE IT — The Platform Advantage")
body(doc, "The AI-Powered PDLC Transformation offering is delivered with the support of our proprietary STUMP (Strategic Transformation Unified Mapping Platform) — an AI-native accelerator that compresses what traditionally takes 3 months into 2 weeks. STUMP provides 21 integrated modules across 7 capability groups: Setup & Data (Organisation Setup, ALM Connect, DORA Assessment, DevOps Maturity, Legacy Modernisation, VSM Editor), Current State Analysis (Current State VSM, Bottleneck Analysis, Improvements, Operations Intelligence), Future State Design (Future State VSM, Business Case, Transformation Readiness), AI Insights (Accuracy & RAG, Recommendations, AI Agents, Playbook), and Governance & Assurance (Governance & Guardrails, AI Assurance).")
bul(doc, "Current State VSM generated automatically from ALM data (Jira, Azure DevOps, Rally)", bold_pre="5× faster diagnosis")
bul(doc, "AI-driven bottleneck identification benchmarked against 500+ financial services teams", bold_pre="AI-accurate insight")
bul(doc, "Business case with ROI, NPV, and payback generated in hours, not weeks", bold_pre="CFO-ready output")
bul(doc, "Platform delivers the evidence; our consultants deliver the strategy and change", bold_pre="Optimal economics")
body(doc, "The platform is not the product. It is what makes our consulting offering faster, more accurate, and more cost-effective than any alternative.")

# PROOF
h2(doc, "PROOF POINT — US Bank / Team Phoenix")
callout(doc, "42 → 8 days lead time  |  17.8% → 61% Flow Efficiency  |  $3M investment  |  $8.4M/yr benefit  |  4.2× ROI  |  14-month payback  |  $31.2M 5-year NPV\n\n'The diagnosis made the business case. The platform made the diagnosis possible in 2 weeks, not 3 months.' — CTO, US Bank Digital", fill='F0FDF4')

# Footer
divider(doc)
footer_p = doc.add_paragraph()
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_f = footer_p.add_run("AI-Powered PDLC Transformation  |  Confidential  |  contact@stump-platform.ai  |  www.stump-platform.ai")
sf(r_f, 8, color=GRAY)

doc.save(os.path.join(OUT, "03-service-brief-one-pager.docx"))
print("  ✓ 03-service-brief-one-pager.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 04 — THOUGHT LEADERSHIP WHITEPAPER
# ══════════════════════════════════════════════════════════════════════════════
print("Building 04-thought-leadership-whitepaper.docx...")
doc = new_doc()
cover_page(doc,
           "The Agentic PDLC: From Value Stream Diagnosis to AI-Native Software Delivery",
           "A Strategic Whitepaper for Technology and Transformation Leaders",
           "Document 04 of 10")

h2(doc, "Executive Summary")
body(doc, "Software delivery is the new factory floor. Like manufacturing before it, the difference between leaders and laggards is not talent or investment — it is the precision with which they understand and optimise their delivery system. The average enterprise software team operates at 17% flow efficiency. World-class teams operate at 40%+. The gap represents billions of dollars in wasted engineering capacity and delayed revenue capture.")
body(doc, "This whitepaper argues that the path to AI-native software delivery is not a single leap but a deliberate progression — one that begins with an accurate diagnosis of the current state value stream, and moves through three transformation options of increasing autonomy and return. We call this the AI-Powered PDLC Transformation — a three-phase consulting offering that takes organisations from Diagnose to Design to Deliver, with AI acceleration at every stage.")
body(doc, "The evidence is unambiguous: organisations that begin with a rigorous current state diagnosis — quantifying speed, productivity, and quality waste at the process level — achieve transformation outcomes 3× more consistently than those that begin with tooling or technology decisions. This paper lays out why, and how.")
divider(doc)

h1(doc, "Section 1: The Hidden Cost of Your PDLC")
h2(doc, "Speed Waste: The Lead Time Tax")
body(doc, "Lead time — the elapsed time from feature commitment to production deployment — is the primary clock of competitive advantage in digital product delivery. Yet for most enterprises, the majority of lead time is not engineering time. It is queue time: waiting for approvals, waiting for environments, waiting for code review, waiting for test capacity.")
body(doc, "Benchmarking data across 500+ enterprise software teams in financial services, insurance, and telecoms reveals:")
bul(doc, "Average lead time: 28–42 business days")
bul(doc, "Median flow efficiency (value-adding time as % of lead time): 17%")
bul(doc, "World-class flow efficiency: 40%+ (achieved by top-quartile teams)")
bul(doc, "Implication: 83 cents of every dollar of engineering time is consumed by non-value-adding activity")
body(doc, "For a 200-engineer organisation spending $40M/year on engineering capacity, this implies $33M in annual waste — not from poor engineering, but from an unmeasured and unmanaged delivery system.")

h2(doc, "Productivity Waste: The Rework Tax")
body(doc, "Rework is the least visible and most expensive form of waste in software delivery. When requirements are misunderstood at the start of a sprint, the cost is not one sprint — it is the compounding cost of late-stage discovery, test failure, and deployment rollback. Studies of enterprise software teams consistently find:")
bul(doc, "15–30% of sprint capacity consumed by rework and defect resolution")
bul(doc, "Average cost of a production defect: 6× the cost of a pre-sprint defect")
bul(doc, "Correlation between low flow efficiency and high defect escape rate: r = 0.73 across 200+ teams studied")
body(doc, "Productivity waste is not an engineering problem. It is a system design problem — one that can only be addressed once the system is visible.")

h2(doc, "Quality Waste: The Technical Debt Compound")
body(doc, "Quality waste operates on a longer time horizon than speed or productivity waste, which is why it is the last to be addressed — and the most expensive when it is. Organisations with flow efficiency below 20% accumulate technical debt at rates that measurably slow future delivery. The compounding effect is:")
bul(doc, "Every 10% reduction in flow efficiency correlates with a 12% reduction in feature throughput within 18 months")
bul(doc, "Teams below 15% FE spend 40%+ of capacity on maintenance and incident response within 2 years")
bul(doc, "Quality deficits are the leading predictor of CTO-level escalation and transformation urgency")
divider(doc)

h1(doc, "Section 2: Current State VSM — What the Data Actually Shows")
h2(doc, "Why Value Stream Mapping Works")
body(doc, "Value Stream Mapping (VSM) was designed for manufacturing in the 1990s. Applied to software delivery, it provides something that no DORA metric dashboard, no sprint velocity chart, and no agile maturity assessment can provide: a system-level view of where time goes and why.")
body(doc, "A current state VSM for a software delivery pipeline captures:")
bul(doc, "Process steps from feature commit to production deployment")
bul(doc, "Lead time and process time at each step (from ALM data, not self-report)")
bul(doc, "Queue time between steps (the most revealing measure)")
bul(doc, "Flow efficiency at each step and end-to-end")
bul(doc, "Defect rate and rework loops by stage")
body(doc, "When this data is extracted automatically from existing ALM tools (Jira, Azure DevOps, Rally) and rendered as a VSM, the picture it reveals is almost always surprising — even to experienced CTOs.")

h2(doc, "What Teams Discover in Phase 1 Diagnose")
body(doc, "Across 40+ diagnostic engagements using the AI-Powered PDLC Transformation methodology, the following patterns emerge consistently:")
bul(doc, "The largest queue is almost never where leadership expects it. In 72% of cases, the primary bottleneck is a handoff step — not a capability gap.")
bul(doc, "Flow efficiency is lower than internal estimates in 89% of cases. The average gap between estimated and actual FE is 18 percentage points.")
bul(doc, "The financial case for transformation is always larger than pre-diagnosis estimates. Average bottleneck cost quantified in Phase 1: $4.7M/year.")
bul(doc, "The AI agents that generate the VSM identify 2–3 bottlenecks that no prior assessment had surfaced. This is not because prior assessments were poorly executed — it is because the data was never integrated at this level.")

h2(doc, "Why the Diagnosis Matters Before the Design")
callout(doc, "A transformation programme that begins with technology selection before diagnosis is analogous to prescribing surgery without imaging. The most common cause of transformation failure is not poor execution — it is treating the wrong bottleneck.")
body(doc, "The Phase 1 Diagnose engagement produces a current state VSM that is evidence-based, data-derived, and benchmarked. It becomes the single source of truth for the transformation design — and, crucially, the foundation of the financial case that wins board approval.")
divider(doc)

h1(doc, "Section 3: Three Pathways to AI-Native Delivery")
body(doc, "Not all organisations are ready for the same transformation. Our Three-Option framework is designed to match transformation ambition to organisational readiness, risk appetite, and investment capacity. Each option delivers measurable ROI; the choice is about pace, depth, and governance model.")

h2(doc, "Option A — AI-Augmented PDLC: Human In the Loop")
body(doc, "Option A introduces AI tools and automation to assist engineering teams at key stages of the PDLC — without removing human decision-making authority at any point. AI makes recommendations; humans act.")
bul(doc, "Investment range: $350,000–$600,000")
bul(doc, "Expected ROI: 2–3× over 24 months")
bul(doc, "Speed improvement: +25% reduction in lead time")
bul(doc, "Productivity improvement: +20% engineering throughput increase")
bul(doc, "Quality improvement: +15% defect escape rate reduction")
bul(doc, "Governance model: Human in the loop — every AI recommendation is reviewed before action")
body(doc, "Option A is the right choice for organisations with early AI maturity, strong compliance requirements, or board-level caution around autonomous systems. It delivers meaningful ROI while building the muscle and confidence required for Option B.")

h2(doc, "Option B — AI Agents + Human Gates: Human On the Loop ★ RECOMMENDED")
body(doc, "Option B deploys AI agents to execute defined process steps autonomously, with human review and approval required only at strategic gates. This is the model that delivers the best balance of return, risk, and governance for most enterprise organisations.")
bul(doc, "Investment range: $1,200,000–$2,000,000")
bul(doc, "Expected ROI: 4–6× over 24 months")
bul(doc, "Speed improvement: +55% reduction in lead time")
bul(doc, "Productivity improvement: +50% engineering throughput increase")
bul(doc, "Quality improvement: +35% defect escape rate reduction")
bul(doc, "Governance model: Human on the loop — AI executes, humans approve at defined gates")
callout(doc, "Option B is our recommended pathway for most enterprise organisations. It is the model that US Bank / Team Phoenix adopted — achieving 42→8 days lead time, $8.4M/year in measurable benefit, and a 4.2× ROI at 14-month payback.")

h2(doc, "Option C — Fully Agentic PDLC: Human Above the Loop")
body(doc, "Option C represents the leading edge of AI-native delivery. AI agents run the end-to-end PDLC autonomously. Humans operate at the strategic level — setting goals, reviewing outcomes, and intervening only at exception.")
bul(doc, "Investment range: $3,000,000–$5,000,000")
bul(doc, "Expected ROI: 8–12× over 36 months")
bul(doc, "Speed improvement: +75% reduction in lead time")
bul(doc, "Productivity improvement: +75% engineering throughput increase")
bul(doc, "Quality improvement: +60% defect escape rate reduction")
bul(doc, "Governance model: Human above the loop — AI operates autonomously within defined parameters")
body(doc, "Option C is appropriate for organisations with high AI maturity, product-led delivery models, and boards that view AI autonomy as a strategic differentiator. It requires the foundations built in Options A and B — or an accelerated path with intensive change management.")
divider(doc)

h1(doc, "Section 4: The Business Case Framework")
body(doc, "Every transformation option produces a quantified business case in Phase 1. The framework is consistent across options, making the choice between A, B, and C a clear financial decision — not a philosophical one.")

h2(doc, "The Bottleneck Cost Formula")
body(doc, "The business case begins with the bottleneck cost — the annual financial value of the waste identified in the current state VSM:")
callout(doc, "Bottleneck Cost = (Lead Time Waste Hours × Engineering Cost Rate) + (Rework Hours × Engineering Cost Rate) + Revenue Delay Cost\n\nRevenue Delay Cost = (Monthly Recurring Revenue at Risk) × (Avg. Delay Weeks / 52)")
body(doc, "For a 200-engineer team with a $200K fully-loaded annual cost and a 42-day average lead time with 17% FE, the bottleneck cost typically exceeds $8M per year. This is the numerator of the business case.")

h2(doc, "ROI Model by Option")
tbl(doc,
    ["", "Option A", "Option B ★", "Option C"],
    [
        ["Investment", "$350–600K", "$1.2–2M", "$3–5M"],
        ["Annual Benefit (Year 1)", "$700K–1.2M", "$4.8–8M", "$12–20M"],
        ["Payback Period", "18–24 months", "10–16 months", "12–24 months"],
        ["5-Year NPV", "$2–4M", "$18–35M", "$45–80M"],
        ["ROI Multiple", "2–3×", "4–6×", "8–12×"],
    ],
    col_widths=[1.8, 1.4, 1.6, 1.4]
)

h2(doc, "US Bank Reference Model")
body(doc, "US Bank / Team Phoenix provides the most complete public example of the Option B business case in financial services:")
tbl(doc,
    ["Metric", "Before", "After", "Impact"],
    [
        ["Lead Time", "42 business days", "8 business days", "81% reduction"],
        ["Flow Efficiency", "17.8%", "61%", "+43.2 pp"],
        ["Investment", "—", "$3.0M", "Option B"],
        ["Annual Benefit", "—", "$8.4M/year", "Measured"],
        ["ROI", "—", "4.2×", "14-month payback"],
        ["5-Year NPV", "—", "$31.2M", "Conservative estimate"],
    ],
    col_widths=[1.8, 1.4, 1.4, 1.6]
)
divider(doc)

h1(doc, "Section 5: Implementation — From Quick Wins to Full Autonomy")
h2(doc, "Phase 3 Deliver: The Three Horizons")
body(doc, "Implementation is sequenced across three horizons, regardless of which option is selected. This structure ensures early value realisation, stakeholder confidence, and sustainable capability building.")

h3(doc, "Horizon 1: Quick Wins (0–90 Days)")
body(doc, "Eliminate the most costly bottlenecks identified in Phase 1 without waiting for the full transformation to be complete. Typical quick wins include:")
bul(doc, "Automated queue monitoring and escalation alerts at top-3 bottleneck steps")
bul(doc, "Code review automation reducing review cycle from 5 days to same-day")
bul(doc, "Environment provisioning automation eliminating the most common 3–5 day wait")
bul(doc, "Sprint planning AI assistance reducing planning waste by 30%")
body(doc, "Horizon 1 typically delivers 15–25% of the total programme benefit within 90 days — creating proof points for board reporting and stakeholder confidence.")

h3(doc, "Horizon 2: Core Transformation (90 Days–12 Months)")
body(doc, "Deploy the core AI agents and automation corresponding to the selected option. Establish governance gates (Option B) or automation frameworks (Option C). Measure and report benefits against the Phase 1 baseline.")

h3(doc, "Horizon 3: Optimisation and Scale (12–24 Months)")
body(doc, "Extend the transformation across additional teams, products, or business units. Optimise agent performance based on 12 months of operational data. Prepare the foundations for the next option tier if appetite has grown.")
divider(doc)

h1(doc, "Section 6: The Role of AI-Accelerated Diagnosis in Reducing Transformation Risk")
h2(doc, "Why Diagnosis is the Risk-Reduction Strategy")
body(doc, "The single most reliable predictor of transformation programme failure is beginning with a solution before understanding the problem at the required level of precision. The Phase 1 Diagnose engagement — and the AI-powered platform that accelerates it — is fundamentally a risk-reduction investment.")
body(doc, "By compressing a 3-month VSM process into 8 weeks (including analysis and option design), the platform allows organisations to:")
bul(doc, "Test assumptions about where waste lives before committing transformation investment")
bul(doc, "Build the financial case with data, not estimates, before board approval")
bul(doc, "Identify the right option (A, B, or C) based on evidence rather than aspiration")
bul(doc, "Establish a quantified baseline against which transformation benefits can be measured")

h2(doc, "The 5× Acceleration Advantage")
body(doc, "Traditional current state VSM for an enterprise software team requires: workshops (3–5 days), manual data extraction (2–4 weeks), analysis (4–6 weeks), and report production (2–3 weeks). Total: 10–14 weeks minimum.")
body(doc, "The STUMP accelerates this to:")
bul(doc, "ALM data connection and extraction: 2–3 days (automated API integration)")
bul(doc, "Current state VSM generation: same day (AI agents, not manual analysis)")
bul(doc, "Bottleneck identification and quantification: 1–2 days")
bul(doc, "Option design and business case: 1 week")
bul(doc, "Total: 2–3 weeks of elapsed time")
callout(doc, "The platform does not replace consulting judgement — it eliminates the data wrangling that historically consumed 80% of a transformation analyst's time. Our consultants spend their time on strategy, change management, and client relationships. The platform handles the analysis.")
divider(doc)

h1(doc, "Conclusion and Call to Action")
body(doc, "The AI-Powered PDLC Transformation offering is built on a simple thesis: organisations that understand their delivery system precisely — and make transformation decisions based on evidence rather than opinion — achieve materially better outcomes. The data across 40+ engagements supports this thesis consistently.")
body(doc, "The path from where you are to AI-native software delivery runs through three phases: Diagnose, Design, and Deliver. It begins with a fixed-fee, time-bounded engagement that produces the evidence base for every decision that follows. It is the lowest-risk, highest-clarity way to start a transformation programme.")
body(doc, "The question is not whether to transform your PDLC. Your competitors are already doing it. The question is whether to begin with evidence or intuition.")
callout(doc, "The next step is Phase 1: Diagnose. In 8 weeks, for a fixed investment of $150,000, we will map your current state, quantify your bottleneck cost, and present you with three transformation options — each with a detailed business case ready for your board. Contact us to scope your engagement.")

h1(doc, "From Three Options to a Maturity Ladder + Target State")
body(doc, "The three options remain the simplest way to frame the choice, but in practice they are points on a continuous L1–L5 maturity ladder — from assisted prompting to a fully autonomous Agentic Development Lifecycle (ADLC). Option A maps to L2 (agent co-pilots), Option B to L3–L4 (supervised independent → orchestrated agents), and Option C to L5 (autonomous ADLC, the North Star).")
for lv in M.LADDER:
    bul(doc, f"{lv['name']} ({lv['ml']}) — {lv['summary']}", bold_pre=lv['level'])
body(doc, "Rather than picking a single option in the abstract, organisations now define a Target State (North-Star level) and a delivery platform, then receive an auto-generated interim roadmap — go in one move, or via one or two interim steps sized to current maturity and risk appetite.")
h2(doc, "Choosing the delivery platform")
body(doc, "The target ADLC can be delivered on different platforms. Home-grown gives maximum control and best economics at scale; COTS (e.g. GitHub Copilot Workspace, Devin, Cursor, the open BMAD method) is fastest to adopt; a service-provider platform such as Cognizant Flowsource offers pre-integrated, managed delivery. Each carries a different ongoing cost profile — including agent/token spend.")
tbl(doc, ["Platform", "Kind", "Best for", "Ongoing cost"],
    [[p["name"], p["kind"], p["pros"], p["ongoing"]] for p in M.PLATFORMS])
h2(doc, "The business case: a DORA J-Curve, not a flat multiple")
body(doc, "Following DORA's 2026 ROI of AI-assisted software development research, we model value as a J-Curve: an up-front investment and an initial productivity dip (the learning curve and verification tax of reviewing AI output), followed by net savings that grow sprint-on-sprint and cross a breakeven point. We deliberately exclude business-growth/feature-revenue, counting only engineering cost-efficiency and reinvested capacity.")
for ph, desc in M.JCURVE["phases"]:
    bul(doc, desc, bold_pre=ph)
callout(doc, M.JCURVE["roi_formula"] + "  " + M.JCURVE["exclusion"])
h2(doc, "Measuring it: the three-perspective Outcome Dashboard")
body(doc, "Progress is tracked continuously across three perspectives — AI Adoption, PDLC Performance (outcomes), and AI Ops & Assurance — computed from live data with per-chart inferences and action points.")
for p in M.OUTCOME_PERSPECTIVES:
    bul(doc, p["blurb"] + "  Metrics: " + ", ".join(p["metrics"][:5]) + ".", bold_pre=p["name"])

doc.save(os.path.join(OUT, "04-thought-leadership-whitepaper.docx"))
print("  ✓ 04-thought-leadership-whitepaper.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 05 — ROI CALCULATOR GUIDE
# ══════════════════════════════════════════════════════════════════════════════
print("Building 05-roi-calculator-guide.docx...")
doc = new_doc()
cover_page(doc,
           "ROI Calculator & Business Case Guide",
           "Three-Option Framework: Quantify Your Transformation Return",
           "Document 05 of 10")

h1(doc, "How to Use This Guide")
body(doc, "This guide is designed to help you estimate the return on investment for each of the three AI-Powered PDLC Transformation options before committing to Phase 1. Use it to build a preliminary business case for internal sponsorship, or to frame the financial conversation with your CFO.")
body(doc, "The guide follows four steps: baseline your current state, identify your bottleneck cost, calculate expected returns for each option, and review the US Bank worked example.")
callout(doc, "Important: These worksheets use your estimates. Phase 1 Diagnose will produce the precise, data-derived numbers. The purpose of this guide is to demonstrate the scale of opportunity — not to replace the diagnostic.")
divider(doc)

h1(doc, "Step 1: Baseline Your Current State")
body(doc, "Complete the following fields with your best estimates. Estimates are acceptable at this stage — Phase 1 will replace them with measured data.")

h2(doc, "Delivery Metrics")
tbl(doc,
    ["Metric", "Your Estimate", "Industry Average", "World-Class"],
    [
        ["Average feature lead time (business days)", "_____ days", "28–42 days", "8–12 days"],
        ["Estimated flow efficiency (%)", "_____%", "17%", "40%+"],
        ["Number of engineering FTEs", "_____", "—", "—"],
        ["Average fully-loaded FTE cost per year ($)", "$_____", "$150–250K", "—"],
        ["Average defect escape rate (% to production)", "_____%", "18–25%", "< 5%"],
        ["Average rework as % of sprint capacity", "_____%", "20–30%", "< 8%"],
    ],
    col_widths=[2.4, 1.5, 1.5, 1.3]
)

h2(doc, "Revenue Impact Metrics")
tbl(doc,
    ["Metric", "Your Estimate"],
    [
        ["Monthly revenue attributable to digital products ($)", "$_____"],
        ["Average delay to revenue from late feature delivery (weeks)", "_____ weeks"],
        ["Estimated annual revenue at risk from slow delivery ($)", "$_____"],
    ],
    col_widths=[3.5, 2.7]
)
divider(doc)

h1(doc, "Step 2: Calculate Your Bottleneck Cost")
h2(doc, "The Bottleneck Cost Formula")
callout(doc, "Annual Bottleneck Cost = Engineering Waste Cost + Rework Cost + Revenue Delay Cost\n\n  Engineering Waste Cost = FTEs × Annual FTE Cost × (1 − Flow Efficiency %)\n  Rework Cost            = FTEs × Annual FTE Cost × Rework %\n  Revenue Delay Cost     = (Monthly Revenue at Risk) × (Avg. Delay Weeks / 52) × 12")

h2(doc, "Your Calculation Worksheet")
tbl(doc,
    ["Component", "Formula", "Your Calculation", "Result"],
    [
        ["Engineering Waste Cost", "FTEs × Cost × (1 − FE%)", "_____ × $_____ × (1 − _____%)", "$_____"],
        ["Rework Cost", "FTEs × Cost × Rework%", "_____ × $_____ × _____%", "$_____"],
        ["Revenue Delay Cost", "(MRR × Delay Wks / 52) × 12", "($_____ × _____ / 52) × 12", "$_____"],
        ["TOTAL ANNUAL BOTTLENECK COST", "", "", "$_____"],
    ],
    col_widths=[1.8, 2.0, 1.8, 1.6]
)
body(doc, "This total is the annual value that your transformation programme will capture. It is also the denominator of the ROI calculation and the foundation of the business case you will present to your CFO.")
divider(doc)

h1(doc, "Step 3: Calculate ROI by Option")
body(doc, "Use your bottleneck cost figure from Step 2 to complete the ROI worksheet for each option. Review the metric improvements and apply them to estimate your annual benefit.")

h2(doc, "Option A ROI Worksheet — AI-Augmented PDLC")
callout(doc, "Option A: Human in the Loop | Speed +25% | Productivity +20% | Quality +15% | Investment $350–600K", fill='F3F4F6')
tbl(doc,
    ["Item", "Formula / Input", "Your Calculation"],
    [
        ["Speed benefit (lead time reduction)", "Bottleneck Cost × 25%", "$_____ × 0.25 = $_____"],
        ["Productivity benefit (throughput gain)", "Bottleneck Cost × 20%", "$_____ × 0.20 = $_____"],
        ["Quality benefit (rework reduction)", "Bottleneck Cost × 15%", "$_____ × 0.15 = $_____"],
        ["Total Annual Benefit (Year 1)", "Sum of above", "$_____"],
        ["Investment (midpoint: $475K)", "$475,000", "$475,000"],
        ["Year 1 Net Benefit", "Benefit − Investment", "$_____"],
        ["Payback Period (months)", "Investment / (Benefit/12)", "_____ months"],
        ["ROI Multiple (2-year)", "(2-yr Benefit − Investment) / Investment", "_____ ×"],
    ],
    col_widths=[2.2, 2.1, 1.9]
)

h2(doc, "Option B ROI Worksheet — AI Agents + Human Gates ★ RECOMMENDED")
callout(doc, "Option B: Human on the Loop | Speed +55% | Productivity +50% | Quality +35% | Investment $1.2–2M", fill='DBEAFE')
tbl(doc,
    ["Item", "Formula / Input", "Your Calculation"],
    [
        ["Speed benefit (lead time reduction)", "Bottleneck Cost × 55%", "$_____ × 0.55 = $_____"],
        ["Productivity benefit (throughput gain)", "Bottleneck Cost × 50%", "$_____ × 0.50 = $_____"],
        ["Quality benefit (rework reduction)", "Bottleneck Cost × 35%", "$_____ × 0.35 = $_____"],
        ["Total Annual Benefit (Year 1)", "Sum of above", "$_____"],
        ["Investment (midpoint: $1.6M)", "$1,600,000", "$1,600,000"],
        ["Year 1 Net Benefit", "Benefit − Investment", "$_____"],
        ["Payback Period (months)", "Investment / (Benefit/12)", "_____ months"],
        ["ROI Multiple (2-year)", "(2-yr Benefit − Investment) / Investment", "_____ ×"],
    ],
    col_widths=[2.2, 2.1, 1.9]
)

h2(doc, "Option C ROI Worksheet — Fully Agentic PDLC")
callout(doc, "Option C: Human above the Loop | Speed +75% | Productivity +75% | Quality +60% | Investment $3–5M", fill='F3F4F6')
tbl(doc,
    ["Item", "Formula / Input", "Your Calculation"],
    [
        ["Speed benefit (lead time reduction)", "Bottleneck Cost × 75%", "$_____ × 0.75 = $_____"],
        ["Productivity benefit (throughput gain)", "Bottleneck Cost × 75%", "$_____ × 0.75 = $_____"],
        ["Quality benefit (rework reduction)", "Bottleneck Cost × 60%", "$_____ × 0.60 = $_____"],
        ["Total Annual Benefit (Year 1)", "Sum of above", "$_____"],
        ["Investment (midpoint: $4M)", "$4,000,000", "$4,000,000"],
        ["Year 1 Net Benefit", "Benefit − Investment", "$_____"],
        ["Payback Period (months)", "Investment / (Benefit/12)", "_____ months"],
        ["ROI Multiple (3-year)", "(3-yr Benefit − Investment) / Investment", "_____ ×"],
    ],
    col_widths=[2.2, 2.1, 1.9]
)
divider(doc)

h1(doc, "Step 4: Worked Example — US Bank / Team Phoenix")
body(doc, "US Bank's Team Phoenix engaged the AI-Powered PDLC Transformation offering in Year 1. Here is how the business case was constructed — across all three options — before selecting Option B.")

h2(doc, "US Bank Baseline (Phase 1 Output)")
tbl(doc,
    ["Metric", "Measured Value"],
    [
        ["Engineering FTEs", "180"],
        ["Average fully-loaded FTE cost", "$220,000/year"],
        ["Measured lead time", "42 business days"],
        ["Measured flow efficiency", "17.8%"],
        ["Measured rework as % of sprint", "24%"],
        ["Monthly revenue at risk", "$3.2M"],
        ["Average feature delay", "3.5 weeks"],
    ],
    col_widths=[3.0, 3.2]
)

h2(doc, "US Bank Bottleneck Cost Calculation")
tbl(doc,
    ["Component", "Calculation", "Amount"],
    [
        ["Engineering Waste Cost", "180 × $220K × (1 − 17.8%)", "$32.5M × 82.2% = $4.2M/yr"],
        ["Rework Cost", "180 × $220K × 24%", "$9.5M/yr"],
        ["Revenue Delay Cost", "($3.2M × 3.5 / 52) × 12", "$2.6M/yr"],
        ["TOTAL ANNUAL BOTTLENECK COST", "", "$16.3M/yr (est.)"],
    ],
    col_widths=[2.2, 2.4, 1.6]
)

h2(doc, "US Bank Option Comparison (Pre-Selection)")
tbl(doc,
    ["", "Option A", "Option B ★ Selected", "Option C"],
    [
        ["Investment", "$475K", "$1.6M", "$4M"],
        ["Annual Benefit Estimate", "$2.1M", "$6.5M", "$9.8M"],
        ["Payback (months)", "27", "14", "22"],
        ["2-Year ROI", "3.4×", "6.1×", "3.9×"],
    ],
    col_widths=[1.8, 1.5, 1.8, 1.5]
)
body(doc, "Option B was selected because it delivered the strongest 2-year ROI (6.1×) at a manageable investment level, with a governance model that matched US Bank's risk appetite. Actual measured results: $8.4M/year benefit, 4.2× ROI, 14-month payback, $31.2M 5-year NPV.")
divider(doc)

h1(doc, "How the Platform Accelerates Step 1 (The Diagnosis)")
body(doc, "The numbers in this guide are estimates. Phase 1 Diagnose replaces every estimate with a measured value, derived from your actual ALM data. The STUMP makes this possible in 2 weeks instead of 3 months.")
bul(doc, "Lead time: extracted directly from Jira, Azure DevOps, or Rally — no surveys, no self-report")
bul(doc, "Flow efficiency: calculated from ticket timestamps across every process step")
bul(doc, "Rework rate: identified from defect re-open patterns and sprint carry-over data")
bul(doc, "Revenue delay: modelled from release calendar and product revenue attribution")
callout(doc, "The diagnosis is not a cost — it is an investment that replaces guesswork with evidence. Every dollar of Phase 1 investment reduces the risk of misallocating the 10–100× larger Phase 3 programme budget.")

h1(doc, "DORA J-Curve Worksheet (cost-only) — the refined model")
body(doc, "Flat ROI multiples are useful headlines, but the defensible business case is a J-Curve. " + M.JCURVE["headline"])
h2(doc, "Step 1 — Investment (hard costs)")
body(doc, M.JCURVE["investment_formula"])
bul(doc, "Licences + agent/token usage + enablement/training + AI infrastructure, × staff.", bold_pre="Direct hard cost")
bul(doc, "Staff × salary × productivity-drop% × duration (DORA sample: 15% over 3 months).", bold_pre="J-Curve tuition cost")
h2(doc, "Step 2 — Ongoing cost is platform-aware (includes agent/token)")
body(doc, M.JCURVE["ongoing_note"])
tbl(doc, ["Platform", "Ongoing cost profile"], [[p["name"], p["ongoing"]] for p in M.PLATFORMS])
h2(doc, "Step 3 — Value (cost-only) and ROI")
body(doc, M.JCURVE["roi_formula"])
callout(doc, M.JCURVE["exclusion"])
h2(doc, "Step 4 — Productivity economics that feed the model")
body(doc, "Value is grounded in the Story-Points→Effort→Cost chain: " + M.PRODUCTIVITY["chain"] + ".")
for f in M.PRODUCTIVITY["formulas"]:
    bul(doc, f)
body(doc, M.PRODUCTIVITY["note"])
callout(doc, "Read sprint-on-sprint: net savings start negative through the dip, then grow and cross breakeven. " + M.JCURVE["dora_defaults"] + " All levers are editable per engagement.")

doc.save(os.path.join(OUT, "05-roi-calculator-guide.docx"))
print("  ✓ 05-roi-calculator-guide.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 06 — INDUSTRY BENCHMARK REPORT
# ══════════════════════════════════════════════════════════════════════════════
print("Building 06-industry-benchmark-report.docx...")
doc = new_doc()
cover_page(doc,
           "PDLC Maturity & AI Transformation Readiness",
           "Financial Services Benchmark Report 2025",
           "Document 06 of 10")

h1(doc, "About This Report")
body(doc, "This benchmark report synthesises PDLC performance data from 500+ enterprise software teams in financial services, insurance, and banking — segmented by AI transformation maturity. It is designed to help technology and transformation leaders understand where their organisation sits on the transformation spectrum, what the leaders in their peer group are doing differently, and how the diagnostic phase of the AI-Powered PDLC Transformation offering compares their position against these benchmarks in real time.")
body(doc, "Data sources: anonymised ALM telemetry, DORA survey data, consulting engagement baselines, and published industry research (State of DevOps Report, DORA Accelerate, Forrester Wave). All figures represent financial services sector data unless otherwise noted.")
divider(doc)

h1(doc, "Section 1: Sector Benchmarks — PDLC Performance by Metric")
h2(doc, "Lead Time (Feature Commit to Production Deployment)")
tbl(doc,
    ["Segment", "Bottom Quartile", "Median", "Top Quartile", "World-Class (Top 5%)"],
    [
        ["Retail Banking", "60+ days", "38 days", "22 days", "8–10 days"],
        ["Insurance", "55+ days", "42 days", "28 days", "10–14 days"],
        ["Capital Markets", "70+ days", "45 days", "25 days", "9–12 days"],
        ["Payments / Fintech", "30+ days", "18 days", "10 days", "4–6 days"],
        ["Wealth Management", "65+ days", "44 days", "30 days", "12–16 days"],
    ],
    col_widths=[1.7, 1.2, 1.0, 1.2, 1.8]
)

h2(doc, "Flow Efficiency (%)")
tbl(doc,
    ["Segment", "Bottom Quartile", "Median", "Top Quartile", "World-Class"],
    [
        ["Retail Banking", "< 8%", "14%", "28%", "40–55%"],
        ["Insurance", "< 7%", "12%", "24%", "38–50%"],
        ["Capital Markets", "< 6%", "11%", "22%", "35–48%"],
        ["Payments / Fintech", "< 15%", "24%", "40%", "55–70%"],
        ["Wealth Management", "< 7%", "13%", "25%", "38–52%"],
    ],
    col_widths=[1.7, 1.2, 1.0, 1.2, 1.8]
)

h2(doc, "DORA Performance Distribution (Financial Services)")
tbl(doc,
    ["DORA Level", "% of FS Teams", "Deployment Frequency", "MTTR", "Change Failure Rate"],
    [
        ["Elite", "8%", "Multiple/day", "< 1 hour", "< 5%"],
        ["High", "22%", "Weekly–daily", "< 1 day", "5–10%"],
        ["Medium", "41%", "Monthly–weekly", "1 day–1 week", "10–15%"],
        ["Low", "29%", "Monthly or less", "> 1 week", "> 15%"],
    ],
    col_widths=[1.3, 1.3, 1.5, 1.2, 1.5]
)
body(doc, "Note: 71% of financial services teams operate at Medium or Low DORA performance. This is the primary driver of PDLC transformation urgency in the sector.")
divider(doc)

h1(doc, "Section 2: Benchmarks by AI Transformation Maturity")
body(doc, "The most significant performance differentiator in the 2025 benchmark data is not team size, budget, or tooling — it is AI transformation maturity. We segment teams into four maturity levels based on their adoption of AI in the PDLC.")

h2(doc, "Maturity Level Definitions")
tbl(doc,
    ["Level", "Description", "% of FS Teams"],
    [
        ["Level 0 — Pre-Augment", "No structured AI in the PDLC. Manual processes, siloed tools, no VSM.", "38%"],
        ["Level 1 — AI-Augmented (Option A)", "AI tools assist at isolated steps. Copilot, AI code review, basic automation.", "34%"],
        ["Level 2 — Agent + Gates (Option B)", "AI agents execute process steps. Human approval at strategic gates.", "22%"],
        ["Level 3 — Agentic (Option C)", "AI runs end-to-end PDLC. Humans set direction and review outcomes.", "6%"],
    ],
    col_widths=[2.0, 3.2, 1.0]
)

h2(doc, "Performance by Maturity Level")
tbl(doc,
    ["Metric", "Level 0", "Level 1 (A)", "Level 2 (B)", "Level 3 (C)"],
    [
        ["Median Lead Time", "42 days", "31 days", "19 days", "10 days"],
        ["Median Flow Efficiency", "14%", "21%", "38%", "59%"],
        ["Median Defect Escape Rate", "22%", "16%", "10%", "4%"],
        ["Median Engineering Throughput (features/team/quarter)", "8", "12", "18", "28"],
        ["Median DORA Level", "Low", "Medium", "High", "Elite"],
        ["Avg. Annual Cost of PDLC Waste (200 FTE baseline)", "$14M", "$9M", "$4M", "$1.5M"],
    ],
    col_widths=[2.5, 0.9, 1.0, 1.0, 1.0]
)
callout(doc, "Moving from Level 0 to Level 2 (Option B) reduces annual PDLC waste cost by an estimated $10M for a 200-FTE engineering organisation — while improving throughput by 125% and cutting lead time by 55%.")
divider(doc)

h1(doc, "Section 3: Where Does Your Organisation Sit?")
body(doc, "Use the following assessment to estimate your current maturity level. Honest self-assessment at this stage enables more accurate business case modelling in Phase 1.")

h2(doc, "Rapid Maturity Self-Assessment")
tbl(doc,
    ["Question", "Yes (+1)", "Partial (+0.5)", "No (0)"],
    [
        ["Can you state your current average lead time with data?", "☐", "☐", "☐"],
        ["Can you state your current flow efficiency with data?", "☐", "☐", "☐"],
        ["Do you have AI tools deployed at 3+ steps in the PDLC?", "☐", "☐", "☐"],
        ["Do AI agents execute any PDLC steps autonomously?", "☐", "☐", "☐"],
        ["Do you have a current state VSM updated in the last 6 months?", "☐", "☐", "☐"],
        ["Can you quantify your bottleneck cost in dollars?", "☐", "☐", "☐"],
        ["Do your DORA metrics link directly to business outcomes?", "☐", "☐", "☐"],
        ["Is your board aligned on a specific transformation investment?", "☐", "☐", "☐"],
    ],
    col_widths=[3.2, 1.0, 1.0, 0.8]
)
body(doc, "Score interpretation: 0–2 = Level 0 (Pre-Augment) | 2.5–4 = Level 1 (Option A ready) | 4.5–6 = Level 2 (Option B ready) | 6.5–8 = Level 3 (Option C ready)")
body(doc, "Note: Score below 2 on the first two questions (data availability) is a strong signal that Phase 1 Diagnose is the critical first action — regardless of transformation ambition level.")
divider(doc)

h1(doc, "Section 4: What Leaders Are Doing Differently")
body(doc, "Teams operating at Level 2 (Option B) and Level 3 (Option C) share five characteristics that distinguish them from the median in our benchmark dataset:")

h2(doc, "Characteristic 1: They Started With a Diagnosis")
body(doc, "95% of Level 2+ teams completed a formal current state VSM before making any transformation technology investment. The diagnosis was the first project, not an afterthought. This gave them a precise understanding of which bottlenecks to address — and which proposed solutions would have been expensive distractions.")

h2(doc, "Characteristic 2: They Built the Business Case From Data")
body(doc, "Level 2+ teams presented their boards with ROI projections grounded in measured bottleneck costs — not vendor projections or industry averages. The data came from the diagnostic phase. In 87% of cases, the board-approved investment was larger than the initial proposal, because the data made the opportunity larger than anyone had estimated.")

h2(doc, "Characteristic 3: They Chose the Right Governance Model Early")
body(doc, "The most common cause of failed Option B programmes is under-investing in governance design — specifically, the definition of which decisions AI agents can make autonomously and which require human gate approval. Level 2+ leaders defined this architecture before deployment, not after the first governance incident.")

h2(doc, "Characteristic 4: They Measured Benefits From Day 1")
body(doc, "Level 2+ organisations established a measurement framework in Phase 1 and tracked benefits from the first deployment. This created a feedback loop that accelerated optimisation and provided the board reporting that sustained programme support through difficult periods.")

h2(doc, "Characteristic 5: They Used Phase 1 to Build Internal Alignment")
body(doc, "The Phase 1 diagnostic was not just a data exercise — it was a change management tool. By involving engineering leads, product leaders, and finance in the diagnosis, Level 2+ organisations arrived at Phase 3 with a coalition of informed sponsors, not passive recipients of a plan.")
divider(doc)

h1(doc, "Section 5: How the Diagnosis Reveals Your Benchmark Gap")
body(doc, "The STUMP, deployed in Phase 1 Diagnose, generates your organisation's performance benchmarks in real time — overlaid against sector peers at each maturity level. This means that at the end of the 8-week diagnostic, you will know:")
bul(doc, "Your actual lead time vs. sector median, top quartile, and world-class")
bul(doc, "Your actual flow efficiency vs. sector median and Level 2/3 peers")
bul(doc, "Your DORA performance level and the gap to the next level")
bul(doc, "The estimated annual cost of your benchmark gap in dollars")
bul(doc, "The specific process steps driving the largest gap vs. peers")
callout(doc, "US Bank / Team Phoenix entered Phase 1 at Level 0 (42-day lead time, 17.8% FE, no structured VSM). The diagnostic revealed they were operating 34 days slower than top-quartile peers — at an annual cost of $8.4M. This single number moved the CFO from sceptic to sponsor.")

doc.save(os.path.join(OUT, "06-industry-benchmark-report.docx"))
print("  ✓ 06-industry-benchmark-report.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 07 — CASE STUDY: US BANK
# ══════════════════════════════════════════════════════════════════════════════
print("Building 07-case-study-usbank.docx...")
doc = new_doc()
cover_page(doc,
           "Case Study: US Bank / Team Phoenix",
           "From 42-Day Lead Time to 8 Days — An AI-Powered PDLC Transformation",
           "Document 07 of 10")

# Client snapshot
t = doc.add_table(rows=1, cols=4)
t.style = 'Table Grid'
for cell, (label, val) in zip(t.rows[0].cells, [
    ("Industry", "Retail Banking (US)"),
    ("Team Size", "180 Engineers"),
    ("Starting Lead Time", "42 Business Days"),
    ("Starting Flow Efficiency", "17.8%"),
]):
    set_cell_bg(cell, '0F2D5E')
    ph = cell.paragraphs[0]
    ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rl = ph.add_run(label + "\n")
    sf(rl, 9, True, color=WHITE)
    rv = ph.add_run(val)
    sf(rv, 11, True, color=RGBColor(0xDB, 0xEA, 0xFE))
    ph.paragraph_format.space_before = Pt(6)
    ph.paragraph_format.space_after = Pt(6)
doc.add_paragraph()

h1(doc, "The Challenge")
body(doc, "US Bank's Team Phoenix was responsible for a core digital lending platform serving 2.4 million retail customers. Despite significant investment in agile transformation over the preceding three years, the team's software delivery performance had plateaued — and in some measures, regressed.")
body(doc, "The symptoms were visible: features committed in Q1 planning routinely shipped in Q2 or Q3. Sprint velocity looked stable, but customer outcomes — measured in time-to-market for new lending products — had not improved. The CTO described it as 'running faster on a treadmill.'")

h2(doc, "The Presenting Problem")
bul(doc, "Average lead time: 42 business days (8.5 weeks from commit to production)")
bul(doc, "Flow efficiency: 17.8% (only 17.8% of elapsed time was active engineering work)")
bul(doc, "DORA level: Medium (weekly deployments, 3-day MTTR, 14% change failure rate)")
bul(doc, "Defect escape rate: 19% of changes required post-production hotfix within 30 days")
bul(doc, "Engineering morale: bottom-quartile on internal engagement survey; 'too much waiting, not enough building'")
body(doc, "Three prior transformation initiatives had been launched in five years. Each produced a playbook. None had produced a measurable reduction in lead time. The organisation had transformation fatigue and a board that was sceptical of further investment without evidence of a different approach.")
callout(doc, "The critical gap: No prior initiative had ever quantified exactly where the 42 days were being consumed. The organisation had opinions about its bottlenecks. It had no data.", fill='FEF3C7')
divider(doc)

h1(doc, "Phase 1: DIAGNOSE")
h2(doc, "What the VSM Revealed")
body(doc, "The Phase 1 Diagnose engagement began with an 8-week fixed-fee engagement. The STUMP connected to Team Phoenix's Jira and Azure DevOps environments within 48 hours, extracting 18 months of ticket telemetry covering 2,400 features, 14,000 pull requests, and 8,700 deployments.")
body(doc, "The current state VSM, generated by the platform's AI agents, revealed a picture that surprised even the most experienced engineers on the team:")

h3(doc, "Where the 42 Days Were Going")
tbl(doc,
    ["Process Step", "Process Time", "Lead Time (incl. queue)", "Flow Efficiency", "Primary Waste Type"],
    [
        ["Requirements & Acceptance Criteria", "2.5 days", "8.5 days", "29%", "Waiting for product review"],
        ["Development", "5.0 days", "9.0 days", "56%", "Context switching (multi-sprint features)"],
        ["Code Review", "0.5 days", "6.0 days", "8%", "Queue: 4 reviewers, 200+ PRs/week"],
        ["QA / Testing", "1.5 days", "11.0 days", "14%", "Environment availability"],
        ["Security & Compliance Review", "1.0 day", "5.5 days", "18%", "Manual review process, no automation"],
        ["Deployment / Release", "0.25 days", "2.0 days", "13%", "Change approval board — fortnightly cadence"],
        ["TOTAL", "10.75 days", "42.0 days", "25.6%*", "*Actual measured FE = 17.8%"],
    ],
    col_widths=[1.8, 1.1, 1.4, 1.1, 1.8]
)
body(doc, "The data revealed three critical findings:")
bul(doc, "Code Review was the primary bottleneck: 4 days of queue time for 30 minutes of actual review. The team had assumed Development was the constraint.", bold_pre="Finding 1")
bul(doc, "The Change Approval Board's fortnightly cadence was adding an average of 1.5 weeks of queue time to every deployment — invisible in sprint metrics but visible in lead time.", bold_pre="Finding 2")
bul(doc, "Security & Compliance Review had 82% queue time. A pre-review automation tool could eliminate 60% of this step's elapsed time without reducing compliance rigour.", bold_pre="Finding 3")

h2(doc, "Speed, Productivity, and Quality — Quantified")
tbl(doc,
    ["Dimension", "Finding", "Annual Cost Estimate"],
    [
        ["Speed", "31.25 days of the 42-day LT is pure queue/wait. At $220K/FTE, this represents $5.2M/yr in misallocated capacity.", "$5.2M/year"],
        ["Productivity", "24% of sprint capacity consumed by rework and defect resolution. Equivalent to 43 FTEs delivering zero customer value.", "$9.5M/year (rework)"],
        ["Quality", "19% defect escape rate driving $1.2M/year in production incident costs and 8% developer time on hotfix.", "$1.2M/year"],
        ["TOTAL BOTTLENECK COST", "", "$15.9M/year (measured)"],
    ],
    col_widths=[1.2, 4.0, 1.0]
)
callout(doc, "'When we saw $15.9 million on a slide — measured from our own data, not an estimate — the CFO leaned forward. That was the moment the conversation changed.' — VP Engineering, US Bank Team Phoenix")
divider(doc)

h1(doc, "Phase 2: DESIGN")
h2(doc, "Three Options Presented to the Leadership Team")
body(doc, "At the Phase 1 close, the consulting team presented all three transformation options to the US Bank executive team, including the CTO, CFO, and Chief Risk Officer. Each option was evaluated against the measured bottleneck cost of $15.9M/year.")

tbl(doc,
    ["", "Option A", "Option B ★", "Option C"],
    [
        ["Model", "Human in the loop", "Human on the loop", "Human above the loop"],
        ["Investment", "$475K", "$1.6M", "$4.0M"],
        ["Annual Benefit (Est.)", "$2.4M", "$8.4M", "$12.2M"],
        ["Payback", "24 months", "14 months", "22 months"],
        ["2-Year ROI", "2.9×", "5.8×", "3.8×"],
        ["Risk Level", "Low", "Medium", "High"],
        ["Governance Fit", "Strong (conservative posture)", "Strong (audit-grade gates)", "Requires regulatory approval"],
    ],
    col_widths=[1.6, 1.3, 1.6, 1.3]
)

h2(doc, "Why Option B Was Selected")
body(doc, "The CRO's primary concern was regulatory: any autonomous AI action in the PDLC needed to be auditable. Option B's governance model — AI agents execute, humans approve at defined gates — was designed to meet this requirement. The audit trail generated at each gate provided the evidence chain required for internal audit and regulatory examination.")
body(doc, "The CFO's primary concern was payback: at 14 months, Option B returned investment faster than Option A (24 months) while delivering materially higher annual benefit. The 5.8× 2-year ROI was the strongest in the option set for US Bank's specific bottleneck cost profile.")
body(doc, "The CTO's primary concern was adoption: Option B's human-on-the-loop model was close enough to current practice that engineering teams could adopt it without a culture shock. Option C, in the CTO's view, was 'where we want to be in 5 years, not 18 months.'")
callout(doc, "The business case was approved by the US Bank board in a single session. The CFO later noted: 'We have never gone into a transformation approval with this level of financial evidence. The diagnosis made it easy.'")
divider(doc)

h1(doc, "Phase 3: DELIVER")
h2(doc, "Implementation Timeline")
tbl(doc,
    ["Phase", "Timeline", "Key Actions", "Benefit Realised"],
    [
        ["Quick Wins", "Months 1–3", "Code review automation; CAB cadence moved to weekly; security pre-scan automation", "LT: 42→28 days; FE: 17.8%→29%"],
        ["Core Deployment", "Months 4–9", "AI agents deployed across 5 PDLC steps; gate governance implemented; team training", "LT: 28→15 days; FE: 29%→47%"],
        ["Optimisation", "Months 10–18", "Agent tuning; scale to 3 additional teams; benefits reporting to board quarterly", "LT: 15→8 days; FE: 47%→61%"],
    ],
    col_widths=[1.2, 1.0, 2.8, 1.8]
)

h2(doc, "Benefits Realised at 18 Months")
tbl(doc,
    ["Metric", "Before", "After 18 Months", "Improvement"],
    [
        ["Lead Time", "42 business days", "8 business days", "81% reduction"],
        ["Flow Efficiency", "17.8%", "61.0%", "+43.2 percentage points"],
        ["Defect Escape Rate", "19%", "7%", "−63% relative"],
        ["Engineering Throughput", "8 features/team/quarter", "21 features/team/quarter", "+163%"],
        ["DORA Level", "Medium", "Elite", "2-level improvement"],
        ["Annual Benefit (Measured)", "—", "$8.4M/year", "vs. $8.4M estimate"],
        ["ROI", "—", "4.2×", "14-month payback"],
        ["5-Year NPV", "—", "$31.2M", "Conservative (no scale-up)"],
    ],
    col_widths=[1.8, 1.3, 1.5, 1.6]
)

h2(doc, "Key Lessons")
callout(doc, "Lesson 1: The diagnosis made the business case. Without the $15.9M bottleneck cost figure — derived from their own data — the board would not have approved the investment. The business case was not our estimate; it was their measurement.", fill='F0FDF4')
callout(doc, "Lesson 2: The platform made the diagnosis possible in 2 weeks, not 3 months. A traditional VSM exercise at US Bank's scale would have taken 12–14 weeks and cost as much as the entire Phase 1 engagement. The platform compressed this to the first 2 weeks of the engagement.", fill='F0FDF4')
callout(doc, "Lesson 3: Starting with the right option mattered more than starting fast. Option A would have delivered $2.4M/year — significant, but far short of the $8.4M Option B achieved. Choosing the right transformation pathway, grounded in the measured business case, was worth more than any individual technical decision.", fill='F0FDF4')

h1(doc, "Reframed on the J-Curve — and where it sits on the ladder")
body(doc, f"{M.USBANK['team']} targeted {M.USBANK['target']} on a {M.USBANK['platform']} platform — the home-grown ADLC baseline. "
          f"Lead time moved {M.USBANK['lead_time']} and flow efficiency {M.USBANK['flow_eff']}. {M.USBANK['note']}")
for ph, desc in M.JCURVE["phases"]:
    bul(doc, desc, bold_pre=ph)
body(doc, "Crucially, the home-grown platform carries a standing platform-engineering team and agent/token cost. Those are shared across pods, so the programme is net-negative for a single team early on and turns strongly positive at portfolio scale — exactly the J-Curve dynamic leaders must budget for rather than mistake for failure.")
h2(doc, "Measured continuously")
body(doc, "Throughout, progress was tracked on the three-perspective Outcome Dashboard (AI Adoption · PDLC Performance · AI Ops & Assurance), with the productivity saving expressed as one reconciled figure in three units — person-days saved = dollars saved = story points of freed capacity.")

doc.save(os.path.join(OUT, "07-case-study-usbank.docx"))
print("  ✓ 07-case-study-usbank.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 08 — COMMERCIAL MODEL & PRICING
# ══════════════════════════════════════════════════════════════════════════════
print("Building 08-commercial-model-pricing.docx...")
doc = new_doc()
cover_page(doc,
           "Commercial Model & Pricing Guide",
           "AI-Powered PDLC Transformation — Three-Option Fee Structure",
           "Document 08 of 10")

h1(doc, "Commercial Philosophy")
body(doc, "The AI-Powered PDLC Transformation commercial model is designed around three principles: predictability for the client (fixed fees where possible), alignment of interests (outcome-linked pricing), and confidence to invest (savings guarantee on Phase 1).")
body(doc, "The model separates the low-risk entry point (Phase 1 Diagnose at $150K fixed) from the transformation investment (Phase 3 Deliver, sized to option and organisation). This allows clients to validate the opportunity and the evidence before committing to the larger programme.")
callout(doc, "No client should commit to a Phase 3 programme without completing Phase 1. The diagnosis is not a prelude to the real engagement — it IS the first investment that pays for itself.")
divider(doc)

h1(doc, "Phase 1: Diagnose — Fixed Fee Engagement")
h2(doc, "What Is Included")
tbl(doc,
    ["Deliverable", "Description", "Format"],
    [
        ["ALM Data Connection", "Automated integration with Jira, Azure DevOps, or Rally. Historical data extraction (12–18 months).", "Platform-enabled"],
        ["Current State VSM", "AI-generated value stream map showing lead time, process time, queue time, and flow efficiency at each step.", "Visual + data export"],
        ["Bottleneck Analysis", "AI-prioritised bottleneck list with quantified cost impact per bottleneck.", "Ranked report + dashboard"],
        ["Speed/Productivity/Quality Quantification", "Measured baseline across three dimensions, benchmarked vs. sector peers.", "Benchmark report"],
        ["Three-Option Business Case", "Detailed business case for Options A, B, and C — investment, annual benefit, payback, NPV.", "CFO-ready document"],
        ["Executive Presentation", "Board-ready summary presentation with data, options, and recommended next step.", "PowerPoint + facilitation"],
    ],
    col_widths=[1.8, 3.0, 1.4]
)

h2(doc, "Phase 1 Fee Structure")
tbl(doc,
    ["Item", "Detail"],
    [
        ["Fixed Fee", "$150,000 (all-inclusive, no variable components)"],
        ["Duration", "8 weeks from signed engagement letter to executive presentation"],
        ["Payment Schedule", "50% on signature; 50% on delivery of executive presentation"],
        ["Savings Guarantee", "If Phase 1 does not identify at least $500K in annual bottleneck savings, the second payment is waived"],
        ["What Is NOT Included", "ALM access credentials (client provides); stakeholder interview time (client-side); data privacy/legal review"],
        ["Phase 2 Design", "Included in Phase 1 fee — business case for all 3 options is part of the Phase 1 deliverable"],
    ],
    col_widths=[2.0, 4.2]
)
callout(doc, "The $500K savings guarantee is the right offer because Phase 1 consistently identifies $2–15M in annual bottleneck cost. No client has ever triggered the guarantee. It exists to eliminate risk aversion at the entry point.")
divider(doc)

h1(doc, "Phase 3: Deliver — Three-Option Fee Structure")
body(doc, "Phase 3 fees are determined by the selected transformation option. All three options include: implementation consulting, AI agent deployment and configuration, governance design, change management, and benefits tracking framework. Platform licensing is included for the programme duration.")

h2(doc, "Option A — AI-Augmented PDLC: Human In the Loop")
tbl(doc,
    ["Component", "Range", "Detail"],
    [
        ["Programme Consulting Fees", "$250,000–$450,000", "Implementation consulting, team coaching, governance design"],
        ["AI Tool Licensing & Configuration", "$50,000–$100,000", "Tool selection, licensing, integration, configuration"],
        ["Change Management & Training", "$50,000–$50,000", "Adoption programme, team training, executive alignment"],
        ["TOTAL INVESTMENT RANGE", "$350,000–$600,000", "Inclusive 24-month programme"],
        ["Expected Annual Benefit", "$700K–$1.2M/year", "Speed +25%, Productivity +20%, Quality +15%"],
        ["At-Risk Component (30%)", "$105K–$180K", "Released on measured ROI at 12 months"],
        ["ROI Multiple", "2–3×", "24-month horizon"],
    ],
    col_widths=[2.2, 1.5, 2.5]
)

h2(doc, "Option B — AI Agents + Human Gates: Human On the Loop ★")
tbl(doc,
    ["Component", "Range", "Detail"],
    [
        ["Programme Consulting Fees", "$750,000–$1,200,000", "Implementation, agent configuration, governance architecture"],
        ["AI Agent Deployment & Integration", "$250,000–$450,000", "LangGraph agents, ALM integration, gate automation"],
        ["Governance Design & Audit Framework", "$100,000–$200,000", "Gate definitions, audit trail, regulatory alignment"],
        ["Change Management & Training", "$100,000–$150,000", "Adoption programme, change coaching, exec reporting"],
        ["TOTAL INVESTMENT RANGE", "$1,200,000–$2,000,000", "Inclusive 24-month programme"],
        ["Expected Annual Benefit", "$4.8M–$8M/year", "Speed +55%, Productivity +50%, Quality +35%"],
        ["At-Risk Component (30%)", "$360K–$600K", "Released on measured ROI at 12 months"],
        ["ROI Multiple", "4–6×", "24-month horizon"],
    ],
    col_widths=[2.2, 1.5, 2.5]
)

h2(doc, "Option C — Fully Agentic PDLC: Human Above the Loop")
tbl(doc,
    ["Component", "Range", "Detail"],
    [
        ["Programme Consulting Fees", "$1,500,000–$2,500,000", "Deep transformation, agentic architecture, change at scale"],
        ["Agentic Platform & Integration", "$800,000–$1,500,000", "Full autonomous pipeline, orchestration, monitoring"],
        ["Governance, Risk & Compliance Framework", "$400,000–$700,000", "Regulatory design, risk controls, audit architecture"],
        ["Change Management & Capability Build", "$300,000–$300,000", "Operating model redesign, capability transfer, board reporting"],
        ["TOTAL INVESTMENT RANGE", "$3,000,000–$5,000,000", "Inclusive 36-month programme"],
        ["Expected Annual Benefit", "$12M–$20M/year", "Speed +75%, Productivity +75%, Quality +60%"],
        ["At-Risk Component (30%)", "$900K–$1.5M", "Released on measured ROI at 18 months"],
        ["ROI Multiple", "8–12×", "36-month horizon"],
    ],
    col_widths=[2.2, 1.5, 2.5]
)
divider(doc)

h1(doc, "Outcome-Linked Pricing: The At-Risk Component")
body(doc, "All three options include a 30% at-risk component tied to measured ROI outcomes. This structure aligns consulting incentives with client outcomes and demonstrates confidence in the offering's delivery.")
tbl(doc,
    ["At-Risk Mechanism", "Detail"],
    [
        ["At-Risk Amount", "30% of total programme fee held in escrow"],
        ["Release Trigger", "Measured ROI equal to or exceeding the projected ROI multiple at the defined measurement date"],
        ["Measurement Method", "Lead time, flow efficiency, and throughput measured from ALM data (same source as Phase 1 baseline)"],
        ["Measurement Date", "Option A/B: 12 months post-deployment start. Option C: 18 months."],
        ["If Target Not Met", "At-risk amount is returned to client. Consulting team continues engagement at cost to diagnose and remediate."],
        ["Track Record", "At-risk component has been retained in 100% of completed engagements to date."],
    ],
    col_widths=[2.2, 4.0]
)
callout(doc, "The at-risk component is not a marketing device — it is a structural commitment. We retain 30% of our fee only if we deliver the measured ROI we promised. This is why the Phase 1 diagnosis is non-negotiable: we will not accept a programme we cannot measure.")
divider(doc)

h1(doc, "Full Programme Summary")
tbl(doc,
    ["", "Phase 1 Diagnose", "Phase 3 — Option A", "Phase 3 — Option B ★", "Phase 3 — Option C"],
    [
        ["Fee", "$150,000 fixed", "$350–600K", "$1.2–2M", "$3–5M"],
        ["Duration", "8 weeks", "18–24 months", "18–24 months", "24–36 months"],
        ["Payment", "50/50 on delivery", "Milestone-based", "Milestone-based", "Milestone-based"],
        ["At-Risk", "Savings guarantee", "30% of fee", "30% of fee", "30% of fee"],
        ["Annual Benefit", "Business case only", "$700K–$1.2M", "$4.8–$8M", "$12–$20M"],
        ["ROI", "—", "2–3×", "4–6×", "8–12×"],
        ["Platform Included", "Yes", "Yes", "Yes", "Yes"],
    ],
    col_widths=[1.5, 1.3, 1.3, 1.5, 1.3]
)

doc.save(os.path.join(OUT, "08-commercial-model-pricing.docx"))
print("  ✓ 08-commercial-model-pricing.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 09 — ENGAGEMENT MODEL OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
print("Building 09-engagement-model-overview.docx...")
doc = new_doc()
cover_page(doc,
           "Engagement Model Overview",
           "Three-Phase Delivery: Diagnose, Design, Deliver",
           "Document 09 of 10")

h1(doc, "Overview: The Three-Phase Engagement Architecture")
body(doc, "The AI-Powered PDLC Transformation engagement is structured in three phases that flow in sequence but overlap at their boundaries. Each phase has a defined scope, deliverable set, and success gate before the next phase begins. The design ensures that every programme starts with evidence, every design is grounded in data, and every delivery is measured against a defined baseline.")
callout(doc, "Phase 1 → Phase 2 → Phase 3 is not a waterfall. Phase 2 Design begins in the final 2 weeks of Phase 1 Diagnose, and Phase 3 quick wins begin in the first month of Phase 3 — before the full programme is deployed. The model is designed for momentum, not sequential gating.")
divider(doc)

h1(doc, "Phase 1: DIAGNOSE — 8 Weeks")
h2(doc, "What Happens")
tbl(doc,
    ["Week", "Activity", "Platform Role", "Client Requirement"],
    [
        ["1", "ALM data connection; historical data extraction; team onboarding", "Automated API integration with Jira / ADO / Rally", "Provide ALM admin credentials; 2-hour onboarding session"],
        ["2", "Current state VSM generation; preliminary bottleneck identification", "AI agents generate VSM from ticket telemetry", "Engineering lead review of VSM draft (2 hours)"],
        ["3–4", "Bottleneck deep-dive; speed/productivity/quality quantification; benchmark overlay", "AI analysis; benchmark comparison against 500+ FS peers", "2 x 90-min workshops with engineering and product leads"],
        ["5–6", "Three-option business case development; ROI modelling; payback and NPV calculation", "Financial model generation; scenario analysis", "Finance business partner input (4 hours)"],
        ["7", "Executive presentation preparation; board narrative development", "Slide generation support; data visualisation", "CTO/CFO review of draft presentation (2 hours)"],
        ["8", "Executive presentation and decision session; option selection gate", "Live dashboard demonstration", "Full leadership team (CTO, CFO, CRO minimum)"],
    ],
    col_widths=[0.5, 1.8, 2.0, 2.0]
)

h2(doc, "Phase 1 Deliverables")
bul(doc, "Current State VSM (visual + data export) — the single source of truth for the transformation")
bul(doc, "Bottleneck Register — prioritised list with cost impact per bottleneck")
bul(doc, "Speed / Productivity / Quality Dashboard — benchmarked against sector peers")
bul(doc, "Three-Option Business Case — investment, benefit, ROI, payback, NPV for each option")
bul(doc, "Executive Presentation — board-ready summary with recommendation")
bul(doc, "Phase 1 Sign-Off Gate — leadership team agreement on which option to proceed with")

h2(doc, "What 'Success' Looks Like at the Phase 1 Gate")
callout(doc, "Success at Phase 1: Leadership team has seen the data, understands the bottleneck cost, has reviewed three credible options with business cases, and has selected an option to proceed with. The CFO has signed off on the investment. The CTO has named a programme owner.")
divider(doc)

h1(doc, "Phase 2: DESIGN — Concurrent With Phase 1 Close")
h2(doc, "What Happens")
body(doc, "Phase 2 Design begins in Week 6 of Phase 1, running concurrently with business case finalisation. This overlap ensures that when the executive presentation occurs in Week 8, the selected option already has a high-level design in progress — enabling Phase 3 to begin immediately after approval.")

tbl(doc,
    ["Design Track", "Activity", "Timing", "Owner"],
    [
        ["Option Architecture", "Design the technical architecture for the selected option; identify AI agents/tools required", "Weeks 6–10", "Lead architect + CTO"],
        ["Governance Design", "Define gate structure (Option B); autonomy boundaries; audit requirements (Option C)", "Weeks 7–10", "Risk lead + CRO"],
        ["Transformation Playbook", "Detailed implementation plan: sequence, milestones, team responsibilities, dependencies", "Weeks 8–12", "Programme lead + Engineering"],
        ["Change Management Plan", "Stakeholder map; change narrative; adoption strategy; training plan", "Weeks 8–12", "Change lead + HR"],
        ["Benefits Tracking Framework", "Define KPIs; measurement cadence; reporting format; board reporting template", "Weeks 9–12", "Analytics lead + Finance"],
    ],
    col_widths=[1.7, 2.2, 1.1, 1.8]
)

h2(doc, "Phase 2 Deliverables")
bul(doc, "Option Design Document — detailed architecture, agent configuration, integration design")
bul(doc, "Governance Framework — gate definitions, approval workflows, audit trail specification")
bul(doc, "Implementation Playbook — phased plan with milestones, owners, and dependencies")
bul(doc, "Change Management Plan — adoption strategy, stakeholder engagement, training schedule")
bul(doc, "Benefits Tracking Framework — KPIs, measurement cadence, board reporting template")
bul(doc, "Phase 2 Sign-Off Gate — leadership team review and approval of playbook before Phase 3 kickoff")

h2(doc, "What 'Success' Looks Like at the Phase 2 Gate")
callout(doc, "Success at Phase 2: The organisation has a clear, detailed plan for Phase 3. Every stakeholder knows their role. The governance model is agreed. The first 90-day quick wins are identified and resourced. The measurement framework is live. Phase 3 can begin immediately.")
divider(doc)

h1(doc, "Phase 3: DELIVER — Option-Specific Timeline")
h2(doc, "The Three Delivery Horizons")
tbl(doc,
    ["Horizon", "Timeline", "Option A", "Option B", "Option C"],
    [
        ["H1: Quick Wins", "Months 1–3", "AI tools at 2 top bottlenecks; 15% LT reduction", "AI agents at top 2 steps; gates configured; 20% LT reduction", "Autonomous pipeline for 1 product team; 25% LT reduction"],
        ["H2: Core", "Months 4–12", "AI tools across all steps; coaching programme", "AI agents across 5 steps; all gates live; measurement running", "Full autonomous pipeline; human-above governance deployed"],
        ["H3: Scale & Optimise", "Months 13–24+", "Extend to 2–3 additional teams; measure + tune", "Scale to additional teams; optimise agent performance", "Scale to org-wide; prepare Option C extension path"],
    ],
    col_widths=[1.1, 1.1, 1.5, 1.7, 1.8]
)

h2(doc, "Platform Role in Each Phase")
tbl(doc,
    ["Phase", "Platform Function", "Value Delivered"],
    [
        ["Phase 1 Diagnose", "ALM data extraction; AI-generated VSM; bottleneck analysis; benchmark overlay; business case generation", "3-month process in 2 weeks; evidence-based baseline; CFO-ready business case"],
        ["Phase 2 Design", "Design validation; architecture review; benefits model update; governance gate configuration", "Design validated against real data; gates configured before deployment"],
        ["Phase 3 Deliver", "Continuous measurement; benefits tracking; agent performance monitoring; board reporting dashboard", "Real-time evidence of benefit realisation; early warning on slippage; board confidence"],
    ],
    col_widths=[1.3, 2.8, 2.1]
)

h2(doc, "Client Responsibilities Per Phase")
tbl(doc,
    ["Phase", "Client Must Provide", "Estimated Effort"],
    [
        ["Phase 1 Diagnose", "ALM admin access; 2–4 senior engineering stakeholders; finance business partner (4 hrs); executive team for Week 8 presentation", "~20 hours total client time"],
        ["Phase 2 Design", "CTO/CRO engagement on governance design; programme owner nominated; change management resource allocated", "~40 hours total client time"],
        ["Phase 3 Deliver", "Programme owner (0.5 FTE); engineering team engagement for each deployment; executive sponsor for quarterly reviews; finance for benefits sign-off", "~0.5–1.0 FTE ongoing"],
    ],
    col_widths=[1.3, 3.2, 1.7]
)
divider(doc)

h1(doc, "How the Platform Makes Each Phase Faster and Evidence-Based")
h2(doc, "The 5× Acceleration Principle")
body(doc, "Every phase of the engagement is accelerated by the STUMP. The platform is not a software product being licensed — it is an operational capability that is deployed in service of the consulting programme. Clients do not need to buy, implement, or maintain the platform: it runs as part of the engagement.")
bul(doc, "Phase 1 is 5× faster because VSM generation is automated from ALM data. No manual data wrangling. No workshop transcription. No consultant estimates.", bold_pre="Phase 1")
bul(doc, "Phase 2 is more accurate because design decisions are validated against the measured baseline. The design is anchored to real data, not assumptions.", bold_pre="Phase 2")
bul(doc, "Phase 3 benefits are visible in real time. The platform's measurement dashboard gives the executive team live visibility of benefit realisation — no waiting for quarterly reviews to know if the programme is working.", bold_pre="Phase 3")
callout(doc, "The platform is the accelerator. The consulting team is the strategy, the change, and the accountability. Together, they deliver transformation outcomes that neither could achieve independently.")

doc.save(os.path.join(OUT, "09-engagement-model-overview.docx"))
print("  ✓ 09-engagement-model-overview.docx")


# ══════════════════════════════════════════════════════════════════════════════
# DOC 10 — DEMO SCRIPT GUIDE
# ══════════════════════════════════════════════════════════════════════════════
print("Building 10-demo-script-guide.docx...")
doc = new_doc()
cover_page(doc,
           "Offering Demo Script & Facilitation Guide",
           "Selling AI-Powered PDLC Transformation Using the Platform as Evidence",
           "Document 10 of 10")

h1(doc, "Purpose and Philosophy of This Demo")
body(doc, "This is NOT a platform demo. The goal is not to show the software. The goal is to sell the consulting offering — 'AI-Powered PDLC Transformation: Diagnose. Design. Deliver.' — using the platform as live evidence that the diagnosis is real, fast, and evidence-based.")
callout(doc, "Frame for the room before you begin: 'What we're going to show you today is not software. We're going to show you what your PDLC actually looks like — and what the financial case for transforming it is. The platform is how we gather that evidence. It's our accelerator, not the product we're selling you.'")
body(doc, "The demo should take 45–60 minutes. It should be run with a pre-loaded dataset (ideally a sanitised client dataset or the US Bank reference case). At the end, the close is: 'We can have this showing YOUR data — from YOUR teams — in 2 weeks.'")
divider(doc)

h1(doc, "Pre-Demo Setup")
h2(doc, "What to Prepare")
bul(doc, "Pre-load US Bank / Team Phoenix dataset (or client-specific data if available)")
bul(doc, "Confirm ALM connection is live and VSM is pre-generated (do not run live generation in demo)")
bul(doc, "Have the Option B business case pre-calculated and ready to display")
bul(doc, "Prepare 3 printed one-pagers: the Service Brief (Doc 03), the ROI Calculator (Doc 05), and the Case Study (Doc 07)")
bul(doc, "Know the client's approximate: team size, tech stack (Jira/ADO/Rally), and whether they have attempted a VSM before")

h2(doc, "Know Before You Enter the Room")
tbl(doc,
    ["Question", "Why It Matters"],
    [
        ["What is their approximate lead time (if known)?", "Anchor the opening hook to a number close to theirs"],
        ["Have they done a VSM before?", "If yes: 'How long did it take, and what changed?' If no: 'Then this will be the first time you've seen this.'"],
        ["Who is in the room (CTO? CFO? Both?)", "CTO: lean into speed/quality. CFO: lean into ROI/payback. Both: start with the bottleneck cost."],
        ["What transformation initiatives have they run?", "Acknowledge prior effort; position the offering as the missing diagnosis layer."],
        ["Are they already using AI tools (Copilot, etc.)?", "If yes: 'Good — that's Option A today. Let's show you what Option B looks like.'"],
    ],
    col_widths=[2.5, 3.7]
)
divider(doc)

h1(doc, "Demo Arc — Step by Step")

h2(doc, "Step 1: The Opening Hook (5 minutes)")
h3(doc, "Opening Question — Word for Word")
callout(doc, "SCRIPT: 'Before I show you anything, I want to ask you one question. Of the last 10 features your teams shipped — how many days, on average, did it take from the moment they were committed in planning to the moment they were live in production? And of those days — what percentage do you think was actual engineering work, versus waiting?'\n\n[Pause. Let them answer. Do not fill the silence.]\n\nScript continue: 'Thank you. Whatever number you gave me — I can almost guarantee the real answer is lower than you think. The average across 500 financial services teams we've worked with is 17%. Seventeen cents of every engineering dollar is doing real work. The rest is waiting. Let me show you what that looks like — in a real team's data.'")

h3(doc, "Presenter Notes — Opening Hook")
bul(doc, "The question surfaces both a number and a feeling. Most executives give a guess, not a measurement — and they know it. That gap between 'I think' and 'I know' is the entry point.")
bul(doc, "If they say they don't know, that IS the answer: 'That's exactly the problem we're going to solve in Phase 1.'")
bul(doc, "If they give a confident number, probe: 'Is that from ALM data or from reporting?' Confident executives often have inflated estimates.")

h2(doc, "Step 2: Show the Current State VSM (10 minutes)")
h3(doc, "Script")
callout(doc, "SCRIPT: 'This is a current state value stream map for Team Phoenix at US Bank. Every data point you're about to see was extracted automatically from their Jira environment — no surveys, no workshops, no consultants spending weeks in spreadsheets. Our platform connected to their data on Monday. By Wednesday, this map existed.\n\n[Point to VSM on screen.]\n\nLook at this step here — Code Review. Thirty minutes of actual review time. Six days of lead time. Why? Queue. At peak volume, 200 pull requests a week flowing to 4 reviewers. The work isn't slow. The queue is unmanaged.\n\n[Point to Change Approval Board step.]\n\nAnd here — Change Approval Board. Meeting fortnightly. Every deployment waits an average of 1.5 weeks just for the CAB. Not for a security reason. Not for a compliance reason. For a calendar reason.\n\nThis is what 42 days looks like. And the team knew it felt slow — but they did not know it was a $15.9M problem. Not until we showed them this.'")

h3(doc, "Presenter Notes — VSM Section")
bul(doc, "Point to specific steps, not the whole map. The bottleneck steps are more compelling than the overview.")
bul(doc, "The '30 minutes of work, 6 days of waiting' contrast is the single most impactful data point in the demo. Pause on it.")
bul(doc, "Expected interruption: 'How do you know it was a calendar reason?' Answer: 'The data shows a bi-weekly spike in deployment lag that correlates exactly with the CAB meeting schedule. The platform identifies this pattern automatically.'")

h2(doc, "Step 3: Reveal the Bottleneck Cost (10 minutes)")
h3(doc, "Script")
callout(doc, "SCRIPT: 'Let me show you what we call the bottleneck cost. This is what Team Phoenix's PDLC waste was costing them, in dollars, per year — before transformation.\n\n[Show bottleneck cost dashboard.]\n\n$5.2 million in engineering capacity consumed by queue time. $9.5 million in rework. $1.2 million in production incidents. Fifteen point nine million dollars a year — not from bad engineering, but from an unmanaged delivery system.\n\nWhen the CFO saw this slide — built from their own Jira data, not our estimates — he said: 'We have never gone into a transformation approval with this level of financial evidence.'\n\nHere's the question I want to ask you: what do you think YOUR number is?'")

h3(doc, "Presenter Notes — Bottleneck Cost")
bul(doc, "The line 'built from their own Jira data, not our estimates' is critical. Repeat it if needed.")
bul(doc, "Let the question — 'what do you think YOUR number is?' — sit for a moment. It creates personal ownership of the problem.")
bul(doc, "If they engage with a number: 'That's what Phase 1 is for — to measure it precisely so we can build your business case from your data, not from benchmarks.'")

h2(doc, "Step 4: Introduce the Three Options (10 minutes)")
h3(doc, "Script")
callout(doc, "SCRIPT: 'Now — here is where most transformation conversations go wrong. Someone shows you a bottleneck, then immediately pitches you a solution. We do the opposite. We show you three options, each with a different level of AI autonomy, a different investment, and a different return. And then we help you choose.\n\n[Show three-option comparison table.]\n\nOption A is AI tools assisting your teams. Humans make every decision. ROI of 2–3×. Good starting point for organisations building AI confidence.\n\nOption B — this is what US Bank chose — is AI agents executing defined steps, humans approving at strategic gates. Human on the loop. ROI of 4–6×. This is the sweet spot for most enterprise organisations: meaningful autonomy, audit-grade governance.\n\nOption C is fully agentic. AI runs the end-to-end pipeline. Humans set direction and review outcomes. ROI of 8–12×. For organisations ready to make AI a strategic differentiator — not just a productivity tool.\n\nUS Bank chose Option B. At 14-month payback and 4.2× ROI, it was the right call for their risk appetite and investment envelope. But for some of the clients we work with, Option C is the right answer. That's what Phase 1 tells us — with data.'")

h3(doc, "Presenter Notes — Three Options")
bul(doc, "Let the client self-identify which option feels right. Watch body language. The option they lean toward is the one to probe on risk appetite.")
bul(doc, "Option B is recommended but do not oversell it. If they are clearly ready for Option C, position it as the more ambitious path.")
bul(doc, "If they ask 'which one would you recommend for us?' — answer: 'That depends on what Phase 1 shows. What I can tell you is that in 89% of cases, the data leads to Option B or C — rarely A. But let the diagnosis guide it, not intuition.'")

h2(doc, "Step 5: Show the Business Case (10 minutes)")
h3(doc, "Script")
callout(doc, "SCRIPT: 'Here is the business case we presented to the US Bank board. This is the document that went to the CFO and the CTO — not a consultant deck, a financial model built from their own data.\n\n[Show business case.]\n\n$3 million investment. $8.4 million per year in measured benefit. 14-month payback. $31.2 million 5-year NPV.\n\nThe board approved it in a single session. Not because the presentation was compelling — because the data was irrefutable. It was their data.\n\nIn 8 weeks, for $150,000, we will produce a business case like this for your organisation. Built from your ALM data. Benchmarked against your sector peers. With your CFO's inputs on investment appetite. That business case is what goes to your board. We make the case; you make the decision.'")

h3(doc, "Presenter Notes — Business Case")
bul(doc, "The '$150K for a $15M business case' framing is extremely powerful. Make it explicit: 'That's a 100-to-1 ratio on Phase 1 investment to opportunity identified.'")
bul(doc, "Have the ROI Calculator (Doc 05) ready to hand out at this point. Invite them to estimate their own number during Phase 1 scoping.")

h2(doc, "Step 5a: Show Governance, Legacy & AI Assurance (5 minutes)")
h3(doc, "Script")
callout(doc, "SCRIPT: 'Before we talk about the business case, I want to show you three capabilities that differentiate this platform from anything else in this space — because they address the three questions every CTO and CRO ask before approving a transformation programme.\n\n[Show Governance & Guardrails module.]\n\nFirst — governance. Every AI agent in Phase 2 and 3 operates within a configurable guardrail framework. You can see here the accountability matrix, the toggle controls, and the full audit log. This is what satisfies your internal audit team and, for FSI clients, the regulatory examiners.\n\n[Show Legacy Modernisation module.]\n\nSecond — legacy. The single biggest barrier to transformation is brownfield complexity. This module assesses every legacy application for Knowledge Graph readiness, generates a modernisation strategy — replatform, reengineer, or decompose — and builds it into the overall transformation plan. You do not have to choose between transforming and managing legacy.\n\n[Show AI Assurance module.]\n\nThird — AI assurance. Every AI agent output is validated through a six-gate quality framework: hallucination rate, citation accuracy, bias monitoring, and drift detection. This is not optional governance theatre. It is how we guarantee the outputs that go to your board are defensible.'")

h3(doc, "Presenter Notes — Governance & New Modules")
bul(doc, "These three modules are the answer to 'what about compliance?' and 'what about our legacy systems?' — the two most common reasons transformation programmes stall.")
bul(doc, "The AI Assurance module is particularly powerful with regulated-industry audiences (banking, healthcare, insurance). Position it as your answer to the responsible AI mandate.")
bul(doc, "If they ask about DORA (Digital Operational Resilience Act for EU FSI): 'The Governance & Guardrails module is designed to produce the audit artefacts required under DORA Article 28-44. Your compliance team can map directly from this module to their regulatory obligations.'")

h2(doc, "Step 6: The Close (5 minutes)")
h3(doc, "Closing Script — Word for Word")
callout(doc, "SCRIPT: 'Everything you've seen today — the VSM, the bottleneck cost, the business case — took our platform 2 weeks to produce for US Bank. Not 3 months. Not a team of analysts. 2 weeks from data connection to executive presentation.\n\nHere is what I'm proposing. In 8 weeks, for a fixed fee of $150,000, we connect to your ALM environment, generate your current state VSM, quantify your bottleneck cost, and present you with three transformation options — each with a business case ready for your board. If we don't identify at least $500,000 in annual savings, you don't pay the second half.\n\nWe can have this showing YOUR data — from YOUR teams — starting in two weeks.\n\nWho do we need to involve to scope that engagement?'")

h3(doc, "Presenter Notes — The Close")
bul(doc, "The close is a question, not a statement. 'Who do we need to involve?' moves to next steps without requiring a yes/no decision.")
bul(doc, "The $500K savings guarantee removes the last barrier. Do not over-explain it — state it once, clearly.")
bul(doc, "If they say 'we need to think about it' — offer to send the Service Brief (Doc 03) and schedule a follow-up with the CFO.")
divider(doc)

h1(doc, "Expected Questions and Objection Handling")
h2(doc, "Objection: 'We've done value stream mapping before and it took 4 months and produced nothing actionable.'")
callout(doc, "RESPONSE: 'I hear this often, and I understand the scepticism. Traditional VSM is a workshop process — it takes months because the data collection is manual, and the output is often too high-level to drive decisions. What we do is different: the VSM is generated from your ALM data in 48 hours, which means every number is real and traceable. The reason prior VSMs produced nothing actionable is usually that they were based on estimates rather than measurements. Ours are not.'")

h2(doc, "Objection: 'Our engineers are already using Copilot / GitHub AI tools — we're already doing this.'")
callout(doc, "RESPONSE: 'Good — that means you're already at Option A. What we'd show you in Phase 1 is whether those tools are actually moving your lead time and flow efficiency metrics at the system level. Most organisations that have adopted AI tools at the team level see local productivity gains but flat or even increasing lead time — because the bottleneck has shifted to a different step. The diagnosis tells you where the next constraint is. That's the foundation for Option B.'")

h2(doc, "Objection: '$150K is expensive for a diagnostic.'")
callout(doc, "RESPONSE: 'Let me offer a different frame. If your bottleneck cost is $8 million per year — which is roughly the median for a 150+ FTE engineering team in your sector — then $150K is less than 2% of the annual cost of the problem you're already paying. And if we don't find at least $500K in annual savings, the second payment is waived. The diagnostic does not add cost to your transformation. It reduces the risk of misallocating the programme budget on the wrong bottleneck.'")

h2(doc, "Objection: 'How do we know the AI agents in Option B are compliant with our audit requirements?'")
callout(doc, "RESPONSE: 'This is the right question — and it's exactly what the governance design in Phase 2 is built around. Option B's model is explicitly designed for environments with audit and regulatory requirements: AI agents execute, humans approve at defined gates, and every action is logged with a full audit trail. US Bank's Chief Risk Officer signed off on this architecture specifically because it met their internal audit requirements. In Phase 1, we include a governance fit assessment as part of the three-option business case.'")

h2(doc, "Objection: 'What happens if the transformation programme doesn't deliver?'")
callout(doc, "RESPONSE: 'Every programme includes a 30% at-risk component tied to measured outcomes. If we don't hit the projected ROI at 12 months, 30% of our fee is returned. We have never triggered that clause — but it exists because we want to share the outcome risk, not just the opportunity. And the measurement comes from the same data source as the Phase 1 baseline, so there is no ambiguity about whether the target was hit.'")

h2(doc, "Objection: 'We have significant legacy systems — this sounds like it only works for greenfield teams.'")
callout(doc, "RESPONSE: 'The Legacy Modernisation module is built specifically for brownfield environments. Before any AI agent is deployed, the platform performs a Knowledge Graph readiness assessment on your existing application portfolio — scoring each system for coupling, testability, API surface, and documentation. The output is a per-application modernisation strategy: which systems should be replatformed, which reengineered, and which are candidates for agentic decomposition. The transformation plan is built around your reality, not an assumed greenfield state. Typically, 20% of legacy systems are transformation blockers — the platform identifies them in Phase 1 so you are never surprised in Phase 3.'")

h2(doc, "Objection: 'What about Responsible AI — how do we satisfy our ethics board and regulators?'")
callout(doc, "RESPONSE: 'STUMP includes a dedicated Governance & Guardrails module and an AI Assurance module built around four dimensions of responsible AI: transparency, accountability, fairness, and security. Every agent has a named human owner, a defined risk classification, and an audit trail. The AI Assurance module runs six validation gates per agent output — including hallucination rate monitoring, bias detection, and citation accuracy. For FSI clients: this architecture maps directly to DORA Article 28-44 compliance obligations. We include a Responsible AI scorecard in Phase 1 so your ethics and compliance teams see the governance framework before Phase 2 begins.'")

h2(doc, "Objection: 'How do you handle the human impact — people are worried about their roles?'")
callout(doc, "RESPONSE: 'The Transformation Readiness module addresses this directly. It does two things. First, it assesses organisational readiness across five dimensions — culture, process, technology, data, and governance — before Phase 3 begins, so we know where the change resistance will be highest. Second, it models the role evolution for each of the seven PDLC phases: from current human roles, through AI-augmented roles in Options A/B, to autonomous-supervised roles in Option C. Most teams discover that AI eliminates the tasks engineers hate most — manual testing, repetitive code review, meeting scheduling — and creates capacity for the design and architecture work engineers value most. That story, told with data from your own team, is the most effective change management asset we produce.'")

divider(doc)
h1(doc, "Leave-Behinds")
body(doc, "At the end of the demo, leave the following printed documents:")
num(doc, "Service Brief One-Pager (Doc 03) — the offering in one page")
num(doc, "ROI Calculator Guide (Doc 05) — let them estimate their own number")
num(doc, "Case Study: US Bank (Doc 07) — the proof point they can share internally")
body(doc, "Follow up within 24 hours with a scoping meeting invitation. The scoping meeting should involve the economic buyer (CTO or CFO) and should be 45 minutes. Its output is a signed Phase 1 engagement letter.")
callout(doc, "Final note for the presenter: The demo works when you are genuinely curious about the client's situation. The opening question, the bottleneck cost reveal, and the close are all designed to create dialogue — not to deliver a monologue. The best demos are 40% presenter, 60% client talking about their pain. That is when the close is inevitable.")

doc.save(os.path.join(OUT, "10-demo-script-guide.docx"))
print("  ✓ 10-demo-script-guide.docx")


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
print()
print("=" * 65)
print("  AI-Powered PDLC Transformation — GTM Pack Set 1 v2")
print("  All 10 documents generated successfully")
print("=" * 65)
files = [
    ("02", "cxo-question-bank.docx",         "20 discovery questions → Phase 1 Diagnose"),
    ("03", "service-brief-one-pager.docx",    "1-page offering brief (DIAGNOSE·DESIGN·DELIVER)"),
    ("04", "thought-leadership-whitepaper.docx", "8-section whitepaper: Agentic PDLC"),
    ("05", "roi-calculator-guide.docx",        "Three-option ROI worksheets + US Bank worked example"),
    ("06", "industry-benchmark-report.docx",   "Sector benchmarks by maturity level (Level 0–3)"),
    ("07", "case-study-usbank.docx",           "Case study: DIAGNOSE/DESIGN/DELIVER structure"),
    ("08", "commercial-model-pricing.docx",    "Three-option fee structure + at-risk model"),
    ("09", "engagement-model-overview.docx",   "Phase-by-phase engagement architecture"),
    ("10", "demo-script-guide.docx",           "Word-for-word demo script + objection handling"),
]
for num_s, name, desc in files:
    path = os.path.join(OUT, f"{num_s}-{name}")
    size = os.path.getsize(path) // 1024
    print(f"  {num_s}  {name:<38} {size:>4} KB  —  {desc}")
print()
print(f"  Output directory: {OUT}")
print("=" * 65)
