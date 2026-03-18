"""
Build: US Bank — Narrative POV + Case Study Combined Presentation
Output: US-Bank-PDLC-VSM-POV-Deck.pptx
~40 slides | Navy/Blue/Teal palette | Storytelling + Case Study
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ─── PALETTE ──────────────────────────────────────────────────────────────────
NAVY      = RGBColor(0x0F, 0x2D, 0x5E)
BLUE      = RGBColor(0x25, 0x63, 0xEB)
TEAL      = RGBColor(0x0D, 0x94, 0x88)
AMBER     = RGBColor(0xD9, 0x77, 0x06)
RED       = RGBColor(0xDC, 0x26, 0x26)
GREEN     = RGBColor(0x16, 0xA3, 0x4A)
LTBLUE    = RGBColor(0xDB, 0xEA, 0xFE)
LTGREEN   = RGBColor(0xDC, 0xFC, 0xE7)
LTAMBER   = RGBColor(0xFE, 0xF3, 0xC7)
LTTEAL    = RGBColor(0xCC, 0xFB, 0xF1)
LTRED     = RGBColor(0xFE, 0xE2, 0xE2)
GRAY50    = RGBColor(0xF9, 0xFA, 0xFB)
GRAY100   = RGBColor(0xF3, 0xF4, 0xF6)
GRAY200   = RGBColor(0xE5, 0xE7, 0xEB)
GRAY600   = RGBColor(0x4B, 0x55, 0x63)
GRAY700   = RGBColor(0x37, 0x41, 0x51)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
BLACK     = RGBColor(0x00, 0x00, 0x00)

W = Inches(13.333)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ─── CORE HELPERS ─────────────────────────────────────────────────────────────
def slide(): return prs.slides.add_slide(BLANK)

def rect(s, x, y, w, h, fill=WHITE):
    sh = s.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.line.fill.background()
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    return sh

def txt(s, text, x, y, w, h, size=14, bold=False, color=GRAY700,
        align=PP_ALIGN.LEFT, italic=False, wrap=True):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    r  = p.add_run()
    r.text = text
    r.font.name  = 'Calibri'
    r.font.size  = Pt(size)
    r.font.bold  = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb

def txt2(s, text, x, y, w, h, size=14, bold=False, color=GRAY700,
         align=PP_ALIGN.LEFT, italic=False):
    """multi-line text — split on newline"""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.name  = 'Calibri'
        r.font.size  = Pt(size)
        r.font.bold  = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb

def add_label(s, label, value, x, y, w=2.6, label_color=TEAL, value_color=NAVY,
              label_size=10, value_size=22):
    txt(s, label, x, y, w, 0.3, size=label_size, bold=True, color=label_color)
    txt(s, value, x, y+0.28, w, 0.5, size=value_size, bold=True, color=value_color)

def metric_box(s, label, value, note, x, y, w=2.8, h=1.4, bg=LTBLUE,
               vc=NAVY, lc=TEAL):
    rect(s, x, y, w, h, fill=bg)
    txt(s, label, x+0.15, y+0.1,  w-0.3, 0.3, size=10, bold=True, color=lc)
    txt(s, value, x+0.15, y+0.35, w-0.3, 0.55, size=22, bold=True, color=vc)
    txt(s, note,  x+0.15, y+0.92, w-0.3, 0.35, size=9,  italic=True, color=GRAY600)

def section_divider(title, subtitle='', bg=NAVY):
    s = slide()
    rect(s, 0, 0, 13.333, 7.5, fill=bg)
    txt(s, title, 0.8, 2.6, 11.7, 1.2, size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    if subtitle:
        txt(s, subtitle, 0.8, 3.9, 11.7, 0.7, size=18, color=RGBColor(0xBF,0xDB,0xFF),
            align=PP_ALIGN.CENTER)
    return s

def header_bar(s, title, subtitle='', bar_color=NAVY):
    rect(s, 0, 0, 13.333, 1.1, fill=bar_color)
    txt(s, title, 0.4, 0.12, 10, 0.5, size=20, bold=True, color=WHITE)
    if subtitle:
        txt(s, subtitle, 0.4, 0.62, 12, 0.38, size=12, color=RGBColor(0xBF,0xDB,0xFF), italic=True)
    rect(s, 0, 1.1, 13.333, 6.4, fill=WHITE)
    return s

def footer(s, text='PDLC VSM Platform  ·  US Bank / Team Phoenix  ·  March 2026'):
    rect(s, 0, 7.2, 13.333, 0.3, fill=GRAY100)
    txt(s, text, 0.3, 7.22, 12.5, 0.25, size=8, color=GRAY600)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE / COVER
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
rect(s, 0, 0, 13.333, 7.5, fill=NAVY)
rect(s, 0, 5.2, 13.333, 2.3, fill=BLUE)
rect(s, 0.5, 0.4, 0.15, 6.5, fill=TEAL)  # accent bar
txt(s, 'US BANK — PAYMENTS & TRANSFERS',   0.9, 0.8,  12, 0.55, size=16, bold=True, color=TEAL)
txt(s, 'From Medium DORA Performer',        0.9, 1.45, 12, 0.9,  size=38, bold=True, color=WHITE)
txt(s, 'to AI-Driven Delivery Excellence',  0.9, 2.35, 12, 0.9,  size=38, bold=True, color=WHITE)
txt(s, 'Team Phoenix · Payments & Transfers · Digital Banking Division',
    0.9, 3.4, 12, 0.45, size=14, color=RGBColor(0xBF,0xDB,0xFF))
txt(s, 'TRANSFORMATION NARRATIVE & CASE STUDY', 0.9, 5.4, 10, 0.5, size=14, bold=True, color=WHITE)
txt(s, 'PDLC VSM Platform  ·  LangGraph AI Agents  ·  March 2026',
    0.9, 5.95, 10, 0.38, size=12, color=LTBLUE)
txt(s, 'CONFIDENTIAL', 9.5, 6.9, 3.5, 0.38, size=10, italic=True, color=LTBLUE, align=PP_ALIGN.RIGHT)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE STORY IN ONE PAGE
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'The Story in One Slide', 'US Bank Team Phoenix — 26-week transformation analysis', NAVY)
rect(s, 0, 1.1, 13.333, 6.4, fill=WHITE)

# 5 story boxes
stories = [
    ('1  DISCOVER',   'NAVY', '42-day lead time\n8.1% flow efficiency\n28 activities mapped\n392 deployments analysed', LTBLUE, NAVY),
    ('2  ASSESS',     'TEAL', 'DORA: Medium Performer\n12% change fail rate\n2.3-day MTTR\nAI-scored with evidence', LTTEAL, TEAL),
    ('3  ANALYSE',    'BLUE', '8 critical bottlenecks\n#1: CAB + Wed window\n#2: PCI-DSS pen-test\nAI root-cause mapped', LTBLUE, BLUE),
    ('4  MODEL',      'AMBE', 'Option A: 18d → High\nOption B: 10d → Elite\nOption C ADLC: 3d\nPer-option activities', LTAMBER, AMBER),
    ('5  TRANSFORM',  'GREE', '$660K net ROI/yr\n7-mo payback (Opt B)\n$1.1M/yr (Option C)\nElite DORA in 24mo', LTGREEN, GREEN),
]
colors_fill = [LTBLUE, LTTEAL, LTBLUE, LTAMBER, LTGREEN]
colors_head = [NAVY,   TEAL,   BLUE,   AMBER,    GREEN]
colors_lbl  = [BLUE,   TEAL,   BLUE,   AMBER,    GREEN]

for i, (label, _, body_text, bg, hc) in enumerate(stories):
    bx = 0.35 + i * 2.6
    rect(s, bx, 1.35, 2.35, 4.8, fill=bg)
    txt(s, label, bx+0.1, 1.45, 2.15, 0.42, size=13, bold=True, color=hc)
    txt2(s, body_text, bx+0.1, 1.95, 2.15, 3.8, size=12, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION BREAK: NARRATIVE POV
# ══════════════════════════════════════════════════════════════════════════════
section_divider('PART 1: THE TRANSFORMATION NARRATIVE',
                'A story of structural waste, AI-driven discovery, and three futures')

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — WHO IS TEAM PHOENIX?
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Who Is Team Phoenix?', 'US Bank · Digital Banking Division · Payments & Transfers', NAVY)

rect(s, 0.35, 1.25, 5.8, 5.7, fill=GRAY50)
txt(s, 'THE TEAM', 0.55, 1.4, 5.4, 0.35, size=11, bold=True, color=TEAL)
lines = [
    '12 engineers | Minneapolis HQ',
    'Product Owner: Jennifer Zhao',
    'Architect: Marcus Thompson',
    'Stack: Java/Spring Boot, React 18, AKS',
    'CI/CD: GitHub Actions + Jira',
    'Monitoring: Datadog + PagerDuty',
    '',
    'Compliance: PCI-DSS L1, SOC2 T2',
    'AI Licences: Copilot Enterprise (100 seats,',
    '             34 active — 66 unused)',
]
txt2(s, '\n'.join(lines), 0.55, 1.82, 5.4, 4.8, size=12, color=GRAY700)

rect(s, 6.55, 1.25, 6.4, 5.7, fill=LTBLUE)
txt(s, 'THE CHALLENGE', 6.75, 1.4, 6.0, 0.35, size=11, bold=True, color=BLUE)
challenges = [
    '→  42-day avg lead time (feature→production)',
    '→  8.1% flow efficiency (91.9% wait time)',
    '→  12% change failure rate',
    '→  2.3-day mean time to restore',
    '→  Weekly deployments vs fintechs: daily',
    '',
    '→  Wednesday-only release window (CAB)',
    '→  5.2-day mandatory pen-test gate (PCI-DSS)',
    '→  18h median PR code review wait',
    '→  No AI-assisted incident response',
]
txt2(s, '\n'.join(challenges), 6.75, 1.82, 6.0, 4.8, size=12, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — THE HIDDEN WASTE
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'The Hidden Waste — 91.9% of Your Pipeline Is Queue Time', '', NAVY)

# Big number
rect(s, 0.35, 1.3, 4.5, 4.6, fill=LTRED)
txt(s, '91.9%', 0.4, 1.6, 4.4, 2.0, size=72, bold=True, color=RED, align=PP_ALIGN.CENTER)
txt(s, 'of feature lead time is', 0.4, 3.6, 4.4, 0.45, size=14, color=GRAY700, align=PP_ALIGN.CENTER)
txt(s, 'NON-VALUE-ADDING WAIT', 0.4, 4.05, 4.4, 0.5, size=16, bold=True, color=RED, align=PP_ALIGN.CENTER)
txt(s, '730 hours per feature cycle | 59 hours of actual work', 0.4, 4.6, 4.4, 0.35, size=10, italic=True, color=GRAY600, align=PP_ALIGN.CENTER)

# Wait time sources
rect(s, 5.2, 1.3, 7.75, 4.6, fill=WHITE)
txt(s, 'WHERE THE 671 HOURS OF WAIT COME FROM', 5.3, 1.35, 7.5, 0.35, size=11, bold=True, color=NAVY)
waits = [
    ('Architecture Review Board queue',    '72h',  RED),
    ('CAB submission + Wednesday window',   '128h', RED),
    ('PCI-DSS penetration test gate',       '40h',  RED),
    ('PR code review wait',                 '18h',  AMBER),
    ('Sequential test execution',           '28h',  AMBER),
    ('DBA on-call gap (after-hours)',        '46h',  AMBER),
    ('Quarterly planning / grooming',       '72h',  AMBER),
    ('SIT environment promotion queue',     '6h',   TEAL),
    ('Build dependency download',           '12h',  TEAL),
    ('Other approval queues',               '249h', GRAY600),
]
for i, (label, val, vc) in enumerate(waits):
    yy = 1.85 + i * 0.42
    txt(s, f'• {label}', 5.3, yy, 5.8, 0.35, size=11, color=GRAY700)
    txt(s, val, 11.1, yy, 1.6, 0.35, size=12, bold=True, color=vc, align=PP_ALIGN.RIGHT)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — CURRENT STATE VSM SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Current State Value Stream Map — Team Phoenix', 'Phase-by-phase PT, WT, and Flow Efficiency', TEAL)

phases = [
    ('1\nBacklog\n& Roadmap',      '31h',  '72h',  '30%', RED),
    ('2\nArchitecture\n& UX',       '36h',  '176h', '17%', RED),
    ('3\nCode\nManagement',         '13h',  '18h',  '42%', AMBER),
    ('4\nContinuous\nIntegration',  '2h',   '6.5h', '24%', AMBER),
    ('5\nContinuous\nTesting',      '34h',  '88h',  '28%', AMBER),
    ('6\nContinuous\nDelivery',     '8h',   '144h', '5%',  RED),
    ('7\nMonitoring\n& Feedback',   '6h',   '96h',  '6%',  RED),
]

for i, (name, pt, wt, fe, fe_color) in enumerate(phases):
    bx = 0.3 + i * 1.87
    rect(s, bx, 1.25, 1.7, 4.2, fill=GRAY100)
    txt2(s, name, bx+0.08, 1.32, 1.54, 0.9, size=9, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    rect(s, bx+0.08, 2.3,  1.54, 0.52, fill=LTBLUE)
    txt(s, 'PT', bx+0.12, 2.33, 0.5, 0.25, size=8, color=BLUE)
    txt(s, pt,   bx+0.12, 2.55, 1.3, 0.28, size=13, bold=True, color=NAVY)
    rect(s, bx+0.08, 2.88, 1.54, 0.52, fill=LTRED)
    txt(s, 'WT', bx+0.12, 2.9,  0.5, 0.25, size=8, color=RED)
    txt(s, wt,   bx+0.12, 3.12, 1.3, 0.28, size=13, bold=True, color=RED)
    rect(s, bx+0.08, 3.46, 1.54, 0.7, fill=LTAMBER if fe_color == AMBER else LTRED)
    txt(s, 'FE', bx+0.12, 3.5,  0.5, 0.25, size=8, color=AMBER if fe_color==AMBER else RED)
    txt(s, fe,   bx+0.12, 3.72, 1.3, 0.38, size=16, bold=True, color=fe_color)

# Summary boxes
rect(s, 0.3, 5.65, 4.0, 1.5, fill=NAVY)
txt(s, 'TOTAL PROCESS TIME', 0.45, 5.72, 3.7, 0.3, size=10, bold=True, color=TEAL)
txt(s, '130 hours', 0.45, 6.05, 3.7, 0.6, size=22, bold=True, color=WHITE)

rect(s, 4.6, 5.65, 4.0, 1.5, fill=RED)
txt(s, 'TOTAL WAIT TIME', 4.75, 5.72, 3.7, 0.3, size=10, bold=True, color=WHITE)
txt(s, '600 hours', 4.75, 6.05, 3.7, 0.6, size=22, bold=True, color=WHITE)

rect(s, 8.9, 5.65, 4.1, 1.5, fill=AMBER)
txt(s, 'FLOW EFFICIENCY', 9.05, 5.72, 3.8, 0.3, size=10, bold=True, color=WHITE)
txt(s, '8.1%  (target: 40%+)', 9.05, 6.05, 3.8, 0.6, size=20, bold=True, color=WHITE)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — DORA ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'DORA Assessment — AI Auto-Scored from Source Evidence', 'Evidence-graded scoring with human validation layer', BLUE)

# 4 DORA metric boxes
dora_metrics = [
    ('DEPLOYMENT\nFREQUENCY', 'Once per week', 'MEDIUM', 'CAB gate prevents daily deploy. 47 prod deploys Q4 2025.', AMBER, LTAMBER),
    ('LEAD TIME\nFOR CHANGES', '1–2 weeks', 'MEDIUM', 'Pen-test gate (PCI-DSS): 5.2 days. Median: 9.4 working days.', AMBER, LTAMBER),
    ('CHANGE\nFAILURE RATE', '12%', 'MEDIUM', '47/392 deployments failed. DB migration failures = 61%.', AMBER, LTAMBER),
    ('MEAN TIME\nTO RESTORE', '1–7 days', 'MEDIUM', 'P50: 2.3 days. DBA off-hours gap. Manual RCA process.', AMBER, LTAMBER),
]
for i, (title, val, band, note, hc, bg) in enumerate(dora_metrics):
    bx = 0.3 + i * 3.2
    rect(s, bx, 1.25, 2.95, 3.5, fill=bg)
    txt2(s, title, bx+0.12, 1.33, 2.71, 0.58, size=11, bold=True, color=hc, align=PP_ALIGN.CENTER)
    txt(s, val,  bx+0.12, 1.98, 2.71, 0.65, size=24, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    rect(s, bx+0.3, 2.68, 2.35, 0.38, fill=hc)
    txt(s, band, bx+0.3, 2.73, 2.35, 0.3, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt2(s, note, bx+0.12, 3.15, 2.71, 1.45, size=10, italic=True, color=GRAY700)

# AI source validation panel
rect(s, 0.3, 4.95, 12.73, 2.25, fill=LTBLUE)
txt(s, 'AI AUTO-SCORE VALIDATION MODEL', 0.5, 5.02, 8.0, 0.32, size=11, bold=True, color=NAVY)
ai_pts = [
    'Every metric scored against 2–3 source documents with specific quoted findings',
    'Confidence % based on source document completeness and data recency',
    'Root cause analysis: structural explanation of why the metric is at this level',
    'Gap analysis: comparison to DORA 2024 benchmark bands for financial services',
    'Human validation: Product Owner reviews, accepts or overrides each score before VSM calibration',
]
for i, pt in enumerate(ai_pts):
    yy = 5.4 + i * 0.32
    txt(s, f'✓  {pt}', 0.5, yy, 12.3, 0.3, size=10, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — THE 8 BOTTLENECKS
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'The 8 Critical Bottlenecks — Where the Waste Actually Lives', 'AI analysis ranked by composite impact: wait time saved × business cost', RED)

bns = [
    ('#1  CAB Gate + Wednesday Window',  'Phase 6', '128h WT saved', 'CRITICAL', RED),
    ('#2  PCI-DSS Pen-Test Gate',         'Phase 5', '40h WT saved',  'CRITICAL', RED),
    ('#3  Architecture Review Board',     'Phase 2', '72h WT saved',  'HIGH',     AMBER),
    ('#4  PR Code Review Wait (18h)',     'Phase 3', '12h per PR',    'HIGH',     AMBER),
    ('#5  Sequential Test Execution',     'Phase 5', '28h saved',     'HIGH',     AMBER),
    ('#6  CI Build — No Caching (24min)', 'Phase 4', '14 min/build',  'MEDIUM',   TEAL),
    ('#7  DBA Availability Gap',          'Phase 7', '24h per inc.',  'HIGH',     AMBER),
    ('#8  Quarterly Planning Cadence',    'Phase 1', '48h per cycle', 'MEDIUM',   TEAL),
]
for i, (bn, ph, impact, sev, sc) in enumerate(bns):
    col = i % 2
    row = i // 2
    bx = 0.3 + col * 6.55
    by = 1.3 + row * 1.45
    rect(s, bx, by, 6.2, 1.32, fill=GRAY50)
    txt(s, bn,     bx+0.15, by+0.08, 4.5,  0.38, size=12, bold=True, color=NAVY)
    txt(s, ph,     bx+0.15, by+0.5,  1.5,  0.3,  size=10, color=GRAY600)
    txt(s, impact, bx+1.85, by+0.5,  2.5,  0.3,  size=10, bold=True, color=sc)
    rect(s, bx+5.1, by+0.08, 0.95, 0.32, fill=sc)
    txt(s, sev, bx+5.1, by+0.1, 0.9, 0.28, size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — THE TWO BIGGEST BOTTLENECKS DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'The Two Critical Bottlenecks — Root Cause Analysis', 'AI-diagnosed from CAB records, CISO policy, and deployment logs', NAVY)

rect(s, 0.3, 1.25, 6.1, 5.8, fill=LTRED)
txt(s, '#1  CAB GATE + WEDNESDAY RELEASE WINDOW', 0.5, 1.35, 5.7, 0.4, size=12, bold=True, color=RED)
txt(s, '128h wait per feature', 0.5, 1.8, 5.7, 0.5, size=20, bold=True, color=NAVY)
cab_body = [
    'Root cause: Not a technical limitation.',
    'The CAB meets every Tuesday 2pm. All changes',
    'require 48h advance submission + sign-off from',
    'CTO, CISO, and Release Manager.',
    '',
    'Result: Wednesday 10pm–2am is the ONLY',
    'deployment window. Every feature waits.',
    '',
    'Solution: Risk-tiered deployment model',
    '→ Standard (low-risk): pre-approved, deploy any day',
    '→ Normal: Tuesday CAB as today',
    '→ Emergency: expedited 2-approver path',
    '',
    'Impact: Eliminates 128h wait for ~70% of deploys.',
]
txt2(s, '\n'.join(cab_body), 0.5, 2.4, 5.7, 4.5, size=11, color=GRAY700)

rect(s, 6.8, 1.25, 6.2, 5.8, fill=LTAMBER)
txt(s, '#2  PCI-DSS PENETRATION TEST GATE', 7.0, 1.35, 5.8, 0.4, size=12, bold=True, color=AMBER)
txt(s, '40h wait per feature (5.2 days)', 7.0, 1.8, 5.8, 0.5, size=20, bold=True, color=NAVY)
pen_body = [
    'Root cause: CISO Policy v3.2 mandates external',
    'pen-testing for ALL CDE changes — regardless of',
    'risk level. SecureWorks SLA: 5 business days.',
    '',
    'Team Phoenix Payments = 100% PCI-DSS scope.',
    'Every feature goes through this gate.',
    '',
    'Solution: AI-powered DAST/SAST in CI pipeline',
    '→ Low-risk changes: AI scanner in <5 min',
    '→ High-risk changes: external pen-test as now',
    '→ Risk classification: automated by AI agent',
    '',
    'Impact: Eliminates 5.2-day wait for ~70% of',
    'deployments while maintaining full compliance.',
]
txt2(s, '\n'.join(pen_body), 7.0, 2.4, 5.8, 4.5, size=11, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION BREAK: THREE FUTURES
# ══════════════════════════════════════════════════════════════════════════════
section_divider('THE THREE FUTURES', 'Option A · Option B · Option C (ADLC)', BLUE)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — THREE OPTIONS OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Three Transformation Options — The Choice Is About Speed', 'All three options measured at activity level with distinct VSM metrics per phase', NAVY)

headers = ['', 'CURRENT STATE', 'OPTION A\nAugmented PDLC', 'OPTION B\nAutomated PDLC', 'OPTION C\nADLC (AI-Driven)']
widths  = [2.5, 2.2, 2.3, 2.3, 2.4]
colors  = [NAVY, GRAY600, BLUE, TEAL, GREEN]
xs      = [0.3, 2.85, 5.1, 7.45, 9.8]

for i, (h, c, x) in enumerate(zip(headers, colors, xs)):
    rect(s, x, 1.25, widths[i]-0.05, 0.75, fill=c)
    txt2(s, h, x+0.08, 1.3, widths[i]-0.18, 0.65, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows_data = [
    ('Lead Time',         '42 days',    '18 days',   '10 days',  '3 days'),
    ('Flow Efficiency',   '8.1%',       '30%',       '44%',      '62%'),
    ('Process Time',      '130 hours',  '65 hours',  '30 hours', '8 hours'),
    ('Wait Time',         '600 hours',  '155 hours', '38 hours', '5 hours'),
    ('DORA Band',         'Medium',     'High',      'High/Elite','Elite'),
    ('Deploy Frequency',  '1×/week',    '3×/week',   'Daily',    'Continuous'),
    ('Change Fail Rate',  '12%',        '8%',        '5%',       '3%'),
    ('MTTR',              '2.3 days',   '18 hours',  '4 hours',  '1 hour'),
    ('Agent Activities',  '0 of 28',    '8 of 28',   '18 of 28', '26 of 28'),
    ('Est. Net ROI/yr',   '—',          '$340K',     '$660K',    '$1.1M'),
]
row_colors  = [WHITE, GRAY50, WHITE, GRAY50, WHITE, GRAY50, WHITE, GRAY50, WHITE, GRAY50]
val_colors  = [GRAY700, GRAY700, BLUE, GREEN]

for ri, (rdata, rbg) in enumerate(zip(rows_data, row_colors)):
    ry = 2.1 + ri * 0.48
    for ci, (val, x) in enumerate(zip(rdata, xs)):
        rect(s, x, ry, widths[ci]-0.05, 0.46, fill=rbg if ci > 0 else GRAY100)
        vc = NAVY if ci == 0 else (GRAY600 if ci == 1 else [BLUE, TEAL, GREEN][ci-2])
        txt(s, val, x+0.08, ry+0.08, widths[ci]-0.18, 0.3, size=11, bold=(ci==0),
            color=vc if ci > 0 else NAVY)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — OPTION A DETAIL
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Option A — Augmented PDLC', '6–12 months | AI augments human effort | DORA: Medium → High', BLUE)

rect(s, 0.3, 1.25, 4.5, 5.8, fill=LTBLUE)
txt(s, 'WHAT CHANGES', 0.5, 1.35, 4.1, 0.32, size=11, bold=True, color=BLUE)
opt_a_changes = [
    'Phase 1:  Continuous OKR cycles begin',
    'Phase 2:  ARB self-service catalogue',
    'Phase 3:  GitHub Copilot 100% + AI PR review',
    '          PR wait: 18h → 6h',
    'Phase 4:  Build caching + parallel tests',
    '          Build: 24min → 8min',
    'Phase 5:  Automated regression upgrade',
    '          DB rollback scripts automated',
    'Phase 6:  CAB risk-tier model proposed',
    'Phase 7:  Basic alert correlation',
]
txt2(s, '\n'.join(opt_a_changes), 0.5, 1.75, 4.1, 5.0, size=11, color=GRAY700)

rect(s, 5.15, 1.25, 4.3, 5.8, fill=GRAY50)
txt(s, 'ACTIVITY EXAMPLE: PHASE 3', 5.35, 1.35, 3.9, 0.32, size=11, bold=True, color=NAVY)
acts_a = [
    ('Copilot-assisted coding',  'HYBRID', BLUE,  '6h PT  0h WT'),
    ('AI PR description gen',    'HYBRID', BLUE,  '0.3h PT  0h WT'),
    ('AI PR pre-review',         'AGENT',  GREEN, '0.5h PT  0h WT'),
    ('Senior engineer review',   'HUMAN',  NAVY,  '2h PT  6h WT'),
    ('Merge + conflict check',   'HYBRID', BLUE,  '0.5h PT  0.5h WT'),
]
for i, (act, typ, tc, metrics) in enumerate(acts_a):
    by = 1.82 + i * 0.88
    rect(s, 5.35, by, 3.9, 0.78, fill=WHITE)
    txt(s, act, 5.5, by+0.06, 2.5, 0.3, size=10, bold=True, color=GRAY700)
    rect(s, 7.85, by+0.06, 1.2, 0.22, fill=tc)
    txt(s, typ, 7.85, by+0.08, 1.2, 0.2, size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, metrics, 5.5, by+0.42, 3.6, 0.25, size=9, italic=True, color=GRAY600)

# Metrics
for i, (label, val, bg) in enumerate([
    ('Lead Time', '18 days', LTBLUE),
    ('FE',        '30%',     LTBLUE),
    ('ROI/yr',    '$340K',   LTGREEN),
]):
    bx = 9.8 + i * 1.1
    rect(s, 9.65, 1.25 + i * 2.0, 3.3, 1.7, fill=bg)
    txt(s, label, 9.82, 1.38 + i * 2.0, 3.0, 0.35, size=10, bold=True, color=TEAL)
    txt(s, val,   9.82, 1.72 + i * 2.0, 3.0, 0.65, size=26, bold=True, color=NAVY)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — OPTION B DETAIL
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Option B — Automated PDLC (Recommended)', '12–18 months | AI agents run delivery pipeline | DORA: High/Elite', TEAL)

rect(s, 0.3, 1.25, 4.5, 5.8, fill=LTTEAL)
txt(s, 'WHAT CHANGES', 0.5, 1.35, 4.1, 0.32, size=11, bold=True, color=TEAL)
opt_b_changes = [
    'Phase 5:  DAST/SAST replaces pen-test gate',
    '          (70% of features skip 5.2-day queue)',
    '          Parallel test execution',
    '          AI-generated test cases',
    'Phase 6:  CAB risk-tier model LIVE',
    '          Deploy any day (low-risk auto-approved)',
    '          Deployment agent: deploy + rollback',
    'Phase 7:  AIOps: auto RCA + runbooks',
    '          MTTR: 2.3 days → 4 hours',
    '          False positives: 18% → <5%',
]
txt2(s, '\n'.join(opt_b_changes), 0.5, 1.75, 4.1, 5.0, size=11, color=GRAY700)

rect(s, 5.15, 1.25, 4.3, 5.8, fill=GRAY50)
txt(s, 'ACTIVITY EXAMPLE: PHASE 5', 5.35, 1.35, 3.9, 0.32, size=11, bold=True, color=NAVY)
acts_b = [
    ('AI DAST/SAST scanner',       'AGENT',    GREEN, '0.5h PT  0h WT'),
    ('AI regression suite (parallel)','AGENT', GREEN, '0.5h PT  0h WT'),
    ('Performance load test agent', 'AGENT',   GREEN, '0.5h PT  0h WT'),
    ('AI risk scoring engine',      'AGENT',   GREEN, '0.3h PT  0h WT'),
    ('Human override (high-risk)',  'OVERSIGHT',AMBER,'0.5h PT  1h WT only'),
]
for i, (act, typ, tc, metrics) in enumerate(acts_b):
    by = 1.82 + i * 0.88
    rect(s, 5.35, by, 3.9, 0.78, fill=WHITE)
    txt(s, act, 5.5, by+0.06, 2.5, 0.3, size=10, bold=True, color=GRAY700)
    rect(s, 7.85, by+0.06, 1.2, 0.22, fill=tc)
    txt(s, typ, 7.85, by+0.08, 1.2, 0.2, size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, metrics, 5.5, by+0.42, 3.6, 0.25, size=9, italic=True, color=GRAY600)

# Metrics
for i, (label, val, bg, vc) in enumerate([
    ('Lead Time', '10 days', LTTEAL, NAVY),
    ('FE',        '44%',     LTTEAL, TEAL),
    ('ROI/yr',    '$660K',   LTGREEN, GREEN),
]):
    rect(s, 9.65, 1.25 + i * 2.0, 3.3, 1.7, fill=bg)
    txt(s, label, 9.82, 1.38 + i * 2.0, 3.0, 0.35, size=10, bold=True, color=TEAL)
    txt(s, val,   9.82, 1.72 + i * 2.0, 3.0, 0.65, size=26, bold=True, color=vc)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — OPTION C ADLC
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Option C — ADLC: AI-Driven Lifecycle (BMAD Approach)', '18–24 months | 2 human roles | 26 of 28 activities agent-driven | Elite DORA', GREEN)

rect(s, 0.3, 1.25, 13.0, 0.62, fill=NAVY)
txt(s, 'The BMAD Philosophy: Build → Measure → Automate → Deploy', 0.5, 1.3, 8.0, 0.38, size=12, bold=True, color=WHITE)
txt(s, 'Two Human Roles Only: Product Definer (sets intent) + Product Builder (supervises + holds production gate)',
    0.5, 1.53, 12.5, 0.3, size=10, italic=True, color=LTBLUE)

adlc_phases = [
    ('1\nIntent &\nOutcome\nDefinition',    'PD',   '1h / 0h',   GREEN),
    ('2\nAutonomous\nArchitecture\n& Design','PB',  '1.5h / 0.5h',GREEN),
    ('3\nAgentic\nCode\nGeneration',         'PB',  '2.5h / 0.5h',GREEN),
    ('4\nAutonomous\nIntegration\nPipeline', 'AUTO','0.5h / 0h',  GREEN),
    ('5\nQuality\nIntelligence',             'PB',  '1h / 0.5h',  GREEN),
    ('6\nZero-Touch\nDelivery',              'PB',  '0.5h / 1h',  GREEN),
    ('7\nAIOps &\nLearning',                 'ESC', '1h / 2.5h',  GREEN),
]
role_labels = {'PD': ('Product\nDefiner', BLUE), 'PB': ('Product\nBuilder', TEAL),
               'AUTO': ('Automated', GREEN), 'ESC': ('Escalation', AMBER)}

for i, (name, role, timing, bc) in enumerate(adlc_phases):
    bx = 0.3 + i * 1.87
    rect(s, bx, 2.05, 1.7, 4.2, fill=LTGREEN)
    txt2(s, name, bx+0.08, 2.12, 1.54, 0.95, size=8, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    rl, rc = role_labels[role]
    rect(s, bx+0.08, 3.12, 1.54, 0.52, fill=rc)
    txt2(s, rl, bx+0.08, 3.14, 1.54, 0.46, size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt2(s, f'PT/WT\n{timing}', bx+0.08, 3.7, 1.54, 0.7, size=9, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    # mostly agent indicator
    if role != 'PD':
        rect(s, bx+0.08, 4.48, 1.54, 0.3, fill=GREEN)
        txt(s, '🤖 Agent-driven', bx+0.08, 4.5, 1.54, 0.26, size=8, color=WHITE, align=PP_ALIGN.CENTER)

# ADLC summary metrics
for i, (label, val, bg, vc) in enumerate([
    ('PT (total)',   '8 hours',    LTGREEN, GREEN),
    ('WT (total)',   '5 hours',    LTGREEN, GREEN),
    ('Lead Time',   '~3 days',    LTGREEN, NAVY),
    ('Flow Eff.',   '62%',        LTGREEN, GREEN),
]):
    bx = 0.3 + i * 3.2
    rect(s, bx, 6.45, 3.0, 0.85, fill=bg)
    txt(s, label, bx+0.15, 6.52, 2.7, 0.28, size=10, bold=True, color=TEAL)
    txt(s, val,   bx+0.15, 6.77, 2.7, 0.45, size=18, bold=True, color=vc)

rect(s, 12.85, 6.45, 0.2, 0.85, fill=WHITE)  # padding

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — ADLC PHASE 3 DRILL DOWN
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'ADLC Deep Dive — Phase 3: Agentic Code Generation', 'From 13h PT + 18h WT (current) to 2.5h PT + 0.5h WT', GREEN)

txt(s, 'CURRENT STATE (Phase 3 — Code Management)', 0.3, 1.32, 6.5, 0.32, size=11, bold=True, color=RED)
current_acts = [
    ('Feature Development',          '8h PT', '4h WT',  'Human'),
    ('Code Review & PR Approval',     '4h PT', '18h WT', 'Human'),
    ('Branch Merge & Conflict Res.',  '1h PT', '4h WT',  'Human'),
]
for i, (act, pt, wt, role) in enumerate(current_acts):
    by = 1.72 + i * 1.08
    rect(s, 0.3, by, 6.1, 0.98, fill=LTRED)
    txt(s, act, 0.48, by+0.08, 4.0, 0.35, size=11, bold=True, color=GRAY700)
    txt(s, f'{pt} | {wt} | {role}', 0.48, by+0.52, 4.5, 0.3, size=10, italic=True, color=RED)

txt(s, 'Total: 13h PT + 22h WT = FE 37%', 0.3, 4.98, 6.1, 0.38, size=12, bold=True, color=RED)

rect(s, 6.65, 1.25, 0.05, 5.8, fill=GRAY200)  # divider

txt(s, 'ADLC STATE (Phase 3 — Agentic Code Generation)', 7.0, 1.32, 6.0, 0.32, size=11, bold=True, color=GREEN)
adlc_acts = [
    ('Intent parsing agent',        '0.5h PT', '0h WT',  '🤖 Agent'),
    ('Multi-agent code generation', '1.5h PT', '0h WT',  '🤖 Agent'),
    ('AI peer review & refactor',   '0.5h PT', '0h WT',  '🤖 Agent'),
    ('PB quality gate (oversight)', '0.5h PT', '0.5h WT','👁 Product Builder'),
]
for i, (act, pt, wt, role) in enumerate(adlc_acts):
    by = 1.72 + i * 1.08
    rect(s, 7.0, by, 6.1, 0.98, fill=LTGREEN)
    txt(s, act, 7.18, by+0.08, 4.2, 0.35, size=11, bold=True, color=GRAY700)
    txt(s, f'{pt} | {wt} | {role}', 7.18, by+0.52, 5.7, 0.3, size=10, italic=True, color=GREEN)

txt(s, 'Total: 3h PT + 0.5h WT = FE 86%  (2.4h → 3.5h → DONE)', 7.0, 4.98, 6.0, 0.38, size=12, bold=True, color=GREEN)

txt(s, '"No PR review queue. No senior engineer availability gate.\nFrom intent to code-ready: 3 hours."',
    0.3, 5.5, 12.8, 0.7, size=14, italic=True, color=BLUE, align=PP_ALIGN.CENTER)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION BREAK: CASE STUDY
# ══════════════════════════════════════════════════════════════════════════════
section_divider('PART 2: THE CASE STUDY', 'Challenge · Approach · Solution · Results · Learnings', TEAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — CASE STUDY: CLIENT CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Case Study: Client Challenge', 'US Bank / Team Phoenix — the problem beneath the performance', NAVY)

rect(s, 0.3, 1.25, 6.0, 5.8, fill=GRAY50)
txt(s, 'THE VISIBLE PICTURE', 0.5, 1.35, 5.6, 0.32, size=11, bold=True, color=TEAL)
visible = [
    '✅  47 features shipped in Q4 2025 — best quarter',
    '✅  Sprint velocity trending upward',
    '✅  GitHub Copilot at 34% adoption and growing',
    '✅  Strong engineering team — experienced, motivated',
    '✅  Compliance maintained — zero regulatory incidents',
]
txt2(s, '\n\n'.join(visible), 0.5, 1.75, 5.6, 3.5, size=11, color=GRAY700)
txt(s, '"By every internal dashboard, the team looks healthy."', 0.5, 5.3, 5.6, 0.55,
    size=12, italic=True, color=BLUE)

rect(s, 6.65, 1.25, 6.3, 5.8, fill=LTRED)
txt(s, 'THE HIDDEN REALITY', 6.85, 1.35, 5.9, 0.32, size=11, bold=True, color=RED)
hidden = [
    '❌  42-day lead time: 10× slower than elite benchmark',
    '❌  8.1% flow efficiency — 91.9% waste',
    '❌  $8.5M/yr incident cost from 12% change failures',
    '❌  Fintechs deploying 50× more frequently',
    '❌  66 Copilot seats unused — $2,574/mo wasted',
    '❌  Compliance processes protecting Q3 risks in Q4 environment',
]
txt2(s, '\n\n'.join(hidden), 6.85, 1.75, 5.9, 3.8, size=11, color=GRAY700)
txt(s, '"The dashboards were measuring the wrong things."', 6.85, 5.8, 5.9, 0.55,
    size=12, italic=True, color=RED)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — CASE STUDY: APPROACH
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Case Study: Approach — The PDLC VSM Platform Methodology', 'AI-powered discovery, scoring, and recommendation in 15 days', BLUE)

steps = [
    ('1', 'CONNECT', 'Ingest 26 weeks of Jira cycle time data. Map 28 activities across 7 PDLC phases. No surveys — actual measurements from production systems.', BLUE, LTBLUE),
    ('2', 'ASSESS',  'DORA auto-scoring from source documents: Jira reports, GitHub logs, PagerDuty analytics, CISO policy. Human validation layer: PO reviews each score.', TEAL, LTTEAL),
    ('3', 'MAP',     'Activity-level VSM: process time, wait time, flow efficiency per activity (not just phase). 8.1% FE revealed — invisible to prior tooling.', GREEN, LTGREEN),
    ('4', 'ANALYSE', '8 bottlenecks ranked by AI. CAB gate and pen-test gate identified as critical. Root causes traced to source documents.', AMBER, LTAMBER),
    ('5', 'MODEL',   'Three future state options with DISTINCT activities per phase. Option C modelled as ADLC — 7 AI capability domains replace 7 PDLC phases.', BLUE, LTBLUE),
    ('6', 'PLAN',    'Business case + 20-sprint implementation roadmap. Playbook Context enriched with 7 org documents for AI-generated implementation guide.', NAVY, GRAY100),
]
for i, (num, title, body_text, hc, bg) in enumerate(steps):
    col = i % 3
    row = i // 3
    bx = 0.3 + col * 4.35
    by = 1.3 + row * 2.75
    rect(s, bx, by, 4.1, 2.55, fill=bg)
    rect(s, bx, by, 0.55, 2.55, fill=hc)
    txt(s, num, bx+0.05, by+0.85, 0.45, 0.7, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, title, bx+0.65, by+0.1, 3.3, 0.4, size=13, bold=True, color=hc)
    txt2(s, body_text, bx+0.65, by+0.55, 3.3, 1.8, size=10, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — CASE STUDY: AI VALIDATION MODEL
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Case Study: The AI Auto-Score Validation Model', 'Every recommendation is grounded in evidence — humans hold accountability', BLUE)

# Left: how it works
rect(s, 0.3, 1.25, 6.2, 5.8, fill=GRAY50)
txt(s, 'HOW THE AI VALIDATION MODEL WORKS', 0.5, 1.35, 5.8, 0.32, size=11, bold=True, color=NAVY)
steps_ai = [
    ('Data Ingestion',   'AI agents read source docs: Jira, GitHub, PagerDuty, CISO policy files'),
    ('Score Generation', 'Each DORA metric scored with: suggested value + confidence % + 2–3 source quotes'),
    ('Root Cause',       'Structural explanation: WHY is the metric at this level? Not just what.'),
    ('Gap Analysis',     'Comparison to DORA 2024 financial services benchmarks (36,000 practitioners)'),
    ('Human Review',     'Product Owner reviews source, challenges AI, accepts or overrides each score'),
    ('VSM Calibration',  'DORA-derived wait times applied to VSM phases — grounded in evidence'),
]
for i, (step_t, step_b) in enumerate(steps_ai):
    by = 1.82 + i * 0.86
    rect(s, 0.48, by, 5.82, 0.76, fill=WHITE)
    txt(s, f'Step {i+1}: {step_t}', 0.62, by+0.06, 5.5, 0.3, size=10, bold=True, color=BLUE)
    txt(s, step_b, 0.62, by+0.38, 5.5, 0.32, size=10, color=GRAY700)

# Right: example note
rect(s, 6.85, 1.25, 6.1, 5.8, fill=LTBLUE)
txt(s, 'EXAMPLE: CHANGE FAILURE RATE SCORE', 6.98, 1.35, 5.85, 0.32, size=11, bold=True, color=NAVY)

rect(s, 6.98, 1.77, 5.85, 0.52, fill=AMBER)
txt(s, 'AI SUGGESTED VALUE: 12%   (Confidence: 94%)', 7.1, 1.82, 5.6, 0.38, size=12, bold=True, color=WHITE)

txt(s, 'SOURCE DOCUMENTS:', 6.98, 2.4, 5.85, 0.3, size=10, bold=True, color=NAVY)
sources = [
    'Incident Log Q3–Q4 2025: "47 deployment incidents out of 392 deployments = 12.0% CFR"',
    'PagerDuty Report 2025: "61% of failures caused by DB migration scripts failing in production"',
    'SonarQube History: "Coverage below 60% threshold 23 times — correlating with 71% of defects"',
]
for i, src in enumerate(sources):
    txt2(s, f'• {src}', 6.98, 2.78 + i * 0.7, 5.85, 0.62, size=9, italic=True, color=GRAY700)

txt(s, 'ROOT CAUSE:', 6.98, 4.9, 5.85, 0.3, size=10, bold=True, color=RED)
txt2(s, '12% CFR driven by: (1) DB migration failures (29/47 incidents) — no automated rollback scripts. (2) 38% of code untested. (3) 14 SIT/prod config parity gaps.',
    6.98, 5.22, 5.85, 0.9, size=10, color=GRAY700)

rect(s, 6.98, 6.25, 2.7, 0.6, fill=GREEN)
txt(s, '✓ ACCEPT', 7.1, 6.35, 2.5, 0.36, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
rect(s, 9.85, 6.25, 2.85, 0.6, fill=GRAY200)
txt(s, '✎ OVERRIDE', 9.97, 6.35, 2.6, 0.36, size=14, bold=True, color=GRAY700, align=PP_ALIGN.CENTER)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — CASE STUDY: BUSINESS CASE
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Case Study: Business Case — Option B (Recommended)', 'Conservative financial model — excludes strategic and revenue upside', TEAL)

# Option B waterfall
rect(s, 0.3, 1.25, 8.2, 5.8, fill=GRAY50)
txt(s, 'OPTION B FINANCIAL MODEL (ANNUAL)', 0.5, 1.35, 7.8, 0.32, size=11, bold=True, color=NAVY)
fin_items = [
    ('Engineering capacity recovered (36% WT reduction)', '+$780,000', GREEN),
    ('Incident cost reduction (CFR 12%→5%, 33 fewer incidents)', '+$630,000', GREEN),
    ('MTTR improvement (2.3d→4h, reduced customer impact)', '+$480,000', GREEN),
    ('GROSS ANNUAL BENEFIT',                                  '+$1,890,000', GREEN),
    ('AI tooling investment (DAST/SAST, AIOps, licences)',    '−$180,000', RED),
    ('Implementation effort (internal sprint capacity)',       '−$180,000', RED),
    ('Training & change management',                          '−$90,000',  RED),
    ('TOTAL INVESTMENT',                                      '−$450,000', RED),
    ('NET ANNUAL BENEFIT',                                    '$660,000',  TEAL),
    ('PAYBACK PERIOD',                                        '7–9 months',TEAL),
    ('3-YEAR NPV (8% discount)',                              '~$1.6M',    TEAL),
]
for i, (label, val, vc) in enumerate(fin_items):
    by = 1.82 + i * 0.46
    bg = GRAY100 if i % 2 == 0 else WHITE
    if label.startswith('GROSS') or label.startswith('TOTAL') or label.startswith('NET'):
        bg = LTBLUE if vc == TEAL else (LTRED if vc == RED else LTGREEN)
    rect(s, 0.48, by, 7.84, 0.42, fill=bg)
    txt(s, label, 0.62, by+0.06, 5.8, 0.3, size=10, bold=label.isupper(), color=GRAY700)
    txt(s, val, 5.85, by+0.06, 2.35, 0.3, size=11, bold=True, color=vc, align=PP_ALIGN.RIGHT)

# Strategic upside
rect(s, 8.85, 1.25, 4.1, 5.8, fill=LTBLUE)
txt(s, 'BEYOND THE NUMBERS', 9.0, 1.35, 3.8, 0.32, size=11, bold=True, color=NAVY)
upside = [
    ('Revenue acceleration', '4× faster → 4× more experiments/yr. Payment feature first-mover advantage is measurable in customer acquisition.'),
    ('Compliance automation', 'DAST/SAST generates PCI-DSS evidence automatically. Annual attestation effort: weeks → hours.'),
    ('Talent retention', 'Engineers in high-flow AI environments have measurably higher satisfaction than those in queue-dominated processes.'),
    ('Risk reduction', '56 fewer incidents/yr. Fewer APRA CPS 234 notification triggers. Lower regulatory exposure.'),
]
for i, (title, desc) in enumerate(upside):
    by = 1.82 + i * 1.3
    txt(s, title, 9.0, by, 3.8, 0.3, size=10, bold=True, color=TEAL)
    txt2(s, desc, 9.0, by+0.33, 3.8, 0.85, size=10, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 18 — IMPLEMENTATION ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Implementation Roadmap — 20-Sprint Journey to Option B (+ C Path)', 'Sprint 1–4: Foundation | 5–10: Automation | 11–20: AI-Native', NAVY)

layers = [
    ('Foundation Layer\nSprints 1–4 (Weeks 1–8)', BLUE, LTBLUE, [
        'S1: Copilot 100% activation + AI PR review → PR wait 18h→6h',
        'S2: Build caching + parallel tests → 24min→8min build',
        'S3: CAB risk-tier proposal + ARB self-service catalogue',
        'S4: Test coverage sprint (62%→70%), quality gate restored',
    ]),
    ('Automation Layer\nSprints 5–10 (Weeks 9–20)', TEAL, LTTEAL, [
        'S5: DAST/SAST in CI pipeline; CAB risk-tier model LIVE',
        'S6: Playwright migration + parallel execution (suite 2h→40min)',
        'S7: PagerDuty alert correlation (false +ve 18%→<5%)',
        'S8: AIOps runbooks for top-10 incident types',
        'S9: Rolling 6-week OKR planning replaces quarterly',
        'S10: IaC 45%→70%, Oracle→Azure SQL migration begins',
    ]),
    ('AI-Native Layer\nSprints 11–20 (Weeks 21–40) — Option C Path', GREEN, LTGREEN, [
        'S11–12: LangGraph agent framework pilot (non-CDE product)',
        'S13–14: Full Option B achieved — DORA benchmarking',
        'S15–16: Code generation agent swarm pilot',
        'S17–18: Deployment agent + Zero-Touch Delivery',
        'S19–20: Full ADLC state — Elite DORA performance achieved',
    ]),
]

bx_positions = [0.3, 4.6, 8.9]
for i, (title, hc, bg, sprints) in enumerate(layers):
    bx = bx_positions[i]
    rect(s, bx, 1.25, 4.05, 5.8, fill=bg)
    rect(s, bx, 1.25, 4.05, 0.72, fill=hc)
    txt2(s, title, bx+0.15, 1.3, 3.75, 0.65, size=10, bold=True, color=WHITE)
    for j, sprint in enumerate(sprints):
        txt(s, f'→ {sprint}', bx+0.15, 2.08 + j * 0.7, 3.75, 0.62, size=9.5, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 19 — KEY LEARNINGS
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Case Study: Key Learnings & Applicability', 'What made this engagement different — and what applies to your organisation', NAVY)

learnings = [
    ('Data-grounded, not hypothesis-led',
     'Every bottleneck and recommendation is traceable to a source document with a quoted finding. Sprint retrospectives independently corroborated the VSM\'s top 3 bottlenecks — converging AI analysis and human testimony.',
     LTBLUE, BLUE),
    ('Human validation is the accountability layer',
     'The AI accelerates and informs — it does not replace the human decision. Product Owner reviewed each DORA score against evidence and made the final call. This is the right architecture for regulated environments.',
     LTTEAL, TEAL),
    ('Compliance and transformation are not opposites',
     'PCI-DSS mandates what must be controlled, not how. AI-powered DAST satisfies the control in 5 min for 70% of changes. Intelligent compliance is not regulatory arbitrage — it\'s applying the right control at the right risk level.',
     LTGREEN, GREEN),
    ('ADLC is a destination, not a disruption',
     'Option C is not a revolution — it is the top of a capability staircase. Each option builds the technical and cultural foundation the next option requires. Teams that skip foundations struggle with Option C.',
     LTAMBER, AMBER),
]
for i, (title, body_text, bg, hc) in enumerate(learnings):
    col = i % 2
    row = i // 2
    bx = 0.3 + col * 6.55
    by = 1.3 + row * 2.9
    rect(s, bx, by, 6.2, 2.7, fill=bg)
    txt(s, title, bx+0.2, by+0.12, 5.8, 0.38, size=12, bold=True, color=hc)
    txt2(s, body_text, bx+0.2, by+0.58, 5.8, 1.95, size=11, color=GRAY700)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 20 — APPLICABILITY TO OTHER FI ORGS
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
header_bar(s, 'Applicability — The Team Phoenix Patterns Are Not Unique', 'These structural bottlenecks appear in every regulated financial services engineering team', NAVY)

txt(s, 'The 4 Universal Patterns of Regulated Financial Services Engineering Waste', 0.3, 1.3, 12.7, 0.4, size=14, bold=True, color=NAVY)

patterns = [
    ('CAB governance gates designed for quarterly releases operating in a weekly delivery world',
     'The CAB risk-model does not differentiate by change risk — uniform governance for heterogeneous risk creates uniform queues.'),
    ('Compliance frameworks prescribing controls without risk-tiering',
     'Pen-tests, security reviews, and change gates apply equally to high-risk and low-risk changes. AI-assisted risk tiering can solve this without reducing compliance rigour.'),
    ('Shared services silos (DBA, Security, Architecture) at business-hours availability in a continuous delivery environment',
     'The 2.3-day MTTR is not an engineering failure — it is an organisational design issue. 24/7 AIOps remediates this structurally.'),
    ('AI tool licencing ahead of AI enablement investment',
     '66 Copilot seats unused. Tool adoption is 10% of the value — the other 90% is embedding AI into workflow, training teams, and creating the cultural permission to use it.'),
]
for i, (title, desc) in enumerate(patterns):
    col = i % 2
    row = i // 2
    bx = 0.3 + col * 6.5
    by = 1.85 + row * 2.5
    rect(s, bx, by, 6.15, 2.3, fill=GRAY50)
    rect(s, bx, by, 0.08, 2.3, fill=NAVY)
    txt(s, f'Pattern {i+1}: {title}', bx+0.2, by+0.1, 5.85, 0.5, size=11, bold=True, color=NAVY)
    txt2(s, desc, bx+0.2, by+0.7, 5.85, 1.45, size=11, color=GRAY700)

txt(s, '"Any financial services team scoring Medium or Low on DORA will find material parallels. The numbers differ. The structural patterns do not."',
    0.3, 6.95, 12.7, 0.42, size=12, italic=True, color=BLUE, align=PP_ALIGN.CENTER)

footer(s)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 21 — THE INVITATION / CALL TO ACTION
# ══════════════════════════════════════════════════════════════════════════════
s = slide()
rect(s, 0, 0, 13.333, 7.5, fill=NAVY)
rect(s, 0, 0, 0.3, 7.5, fill=TEAL)

txt(s, 'THE INVITATION', 0.7, 0.7, 12.0, 0.55, size=16, bold=True, color=TEAL)
txt(s, 'The question is no longer whether to transform.', 0.7, 1.4, 12.0, 0.75, size=26, bold=True, color=WHITE)
txt(s, 'The question is which option you start with — and how fast.', 0.7, 2.2, 12.0, 0.75, size=26, bold=True, color=WHITE)

rect(s, 0.7, 3.15, 3.7, 1.5, fill=BLUE)
txt(s, 'OPTION A', 0.85, 3.22, 3.4, 0.38, size=13, bold=True, color=TEAL)
txt(s, '6–12 months', 0.85, 3.62, 3.4, 0.38, size=13, color=WHITE)
txt(s, 'High Performer', 0.85, 4.02, 3.4, 0.38, size=13, bold=True, color=LTBLUE)

rect(s, 4.8, 3.15, 3.7, 1.5, fill=TEAL)
txt(s, 'OPTION B ★', 4.95, 3.22, 3.4, 0.38, size=13, bold=True, color=WHITE)
txt(s, '12–18 months', 4.95, 3.62, 3.4, 0.38, size=13, color=WHITE)
txt(s, 'High/Elite | $660K ROI', 4.95, 4.02, 3.4, 0.38, size=13, bold=True, color=LTBLUE)

rect(s, 8.9, 3.15, 4.1, 1.5, fill=GREEN)
txt(s, 'OPTION C — ADLC', 9.05, 3.22, 3.8, 0.38, size=13, bold=True, color=WHITE)
txt(s, '18–24 months', 9.05, 3.62, 3.8, 0.38, size=13, color=WHITE)
txt(s, 'Elite | 3-day lead time', 9.05, 4.02, 3.8, 0.38, size=13, bold=True, color=WHITE)

txt(s, 'PDLC VSM Platform  ·  US Bank / Team Phoenix  ·  March 2026  ·  Confidential',
    0.7, 7.05, 12.0, 0.32, size=11, color=RGBColor(0x93,0xC5,0xFD), align=PP_ALIGN.CENTER)

# ── Save ───────────────────────────────────────────────────────────────────────
prs.save('US-Bank-PDLC-VSM-POV-Deck.pptx')
print('✅  US-Bank-PDLC-VSM-POV-Deck.pptx created (21 slides)')
