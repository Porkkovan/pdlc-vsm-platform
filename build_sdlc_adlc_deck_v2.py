"""
Build: SDLC to ADLC Consulting Offering Deck — Refined v2
Output: SDLC-to-ADLC-Refined-v2.pptx

Refined with latest STUMP platform capabilities:
  - 24 pages, 13 backend agents, 7 platform choices
  - L1–L5 maturity ladder with ML bands
  - Full 21-agent fleet for Option C
  - 8 token optimisation levers
  - Outcome Dashboard with 3 perspectives
  - Target State Studio with 4-step wizard
  - Frontier Pod model (1–3 FTE + agents)

Uses the same Cognizant Navy/Blue color palette as the original deck.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import copy

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Colour palette (matching original Cognizant theme) ────────────────────────
NAVY      = RGBColor(0x0F, 0x2D, 0x5E)
DEEP_NAVY = RGBColor(0x0C, 0x2A, 0x55)
BLUE      = RGBColor(0x25, 0x63, 0xEB)
SKY       = RGBColor(0x02, 0x84, 0xC7)
TEAL      = RGBColor(0x05, 0x96, 0x69)
GREEN     = RGBColor(0x10, 0xB9, 0x81)
AMBER     = RGBColor(0xF9, 0x73, 0x16)
RED       = RGBColor(0xEF, 0x44, 0x44)
VIOLET    = RGBColor(0x4F, 0x46, 0xE5)
PURPLE    = RGBColor(0x93, 0x33, 0xEA)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY     = RGBColor(0xE2, 0xE8, 0xF0)
GRAY      = RGBColor(0x64, 0x74, 0x8B)
DGRAY     = RGBColor(0x33, 0x41, 0x55)
SLATE     = RGBColor(0x1E, 0x29, 0x3B)
LIGHT_BLUE = RGBColor(0xEF, 0xF6, 0xFF)
PALE_BLUE  = RGBColor(0xBF, 0xDB, 0xFE)

# ── Helpers ───────────────────────────────────────────────────────────────────
def add_slide():
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)

def add_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, fill=None, line=None, line_w=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    if line:
        shape.line.fill.solid()
        shape.line.color.rgb = line
        shape.line.width = line_w or Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_rounded_rect(slide, left, top, width, height, fill=None, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.fill.solid()
        shape.line.color.rgb = line
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, size=12, bold=False, color=DGRAY, align=PP_ALIGN.LEFT, font='Calibri'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font
    p.alignment = align
    return txBox

def add_rich_text(slide, left, top, width, height, parts, align=PP_ALIGN.LEFT, spacing=Pt(2)):
    """parts = list of (text, size, bold, color) tuples"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing:
        p.space_after = spacing
    for i, (text, size, bold, color) in enumerate(parts):
        run = p.add_run() if i > 0 else (p.runs[0] if p.runs else p.add_run())
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = 'Calibri'
    return txBox

def add_bullet_box(slide, left, top, width, height, bullets, size=11, color=DGRAY, bold_prefix=False, bullet_color=None):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(3)
        p.level = 0
        if isinstance(b, tuple) and bold_prefix:
            run1 = p.add_run()
            run1.text = b[0] + '  '
            run1.font.size = Pt(size)
            run1.font.bold = True
            run1.font.color.rgb = bullet_color or NAVY
            run1.font.name = 'Calibri'
            run2 = p.add_run()
            run2.text = b[1]
            run2.font.size = Pt(size)
            run2.font.bold = False
            run2.font.color.rgb = color
            run2.font.name = 'Calibri'
        else:
            run = p.add_run()
            run.text = f'• {b}'
            run.font.size = Pt(size)
            run.font.color.rgb = color
            run.font.name = 'Calibri'
    return txBox

def add_metric_card(slide, left, top, width, height, value, label, fill=LIGHT_BLUE, value_color=NAVY, label_color=GRAY):
    shape = add_rounded_rect(slide, left, top, width, height, fill=fill)
    add_text(slide, left, top + Inches(0.15), width, Inches(0.4), value, size=22, bold=True, color=value_color, align=PP_ALIGN.CENTER)
    add_text(slide, left, top + Inches(0.55), width, Inches(0.3), label, size=9, color=label_color, align=PP_ALIGN.CENTER)
    return shape

def footer(slide, text='STUMP Platform  |  SDLC to ADLC Transformation  |  Confidential'):
    add_text(slide, Inches(0.5), Inches(7.0), Inches(12), Inches(0.3), text, size=8, color=GRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, NAVY)
add_text(s, Inches(1), Inches(1.2), Inches(11), Inches(0.4), 'SDLC to ADLC', size=16, bold=True, color=SKY, align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(1.7), Inches(11), Inches(1.0), 'AI-Driven Lifecycle\nTransformation', size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, Inches(1), Inches(3.2), Inches(11), Inches(0.6), 'From 42-Day Lead Times to Continuous Delivery — Powered by the STUMP Multi-Agent Platform', size=14, color=PALE_BLUE, align=PP_ALIGN.CENTER)

# Platform stats
stats = [('24', 'Platform Pages'), ('13', 'AI Agents'), ('7', 'PDLC Phases'), ('36', 'Activities Mapped'), ('7', 'Platform Choices'), ('5', 'Maturity Levels')]
sx = Inches(1.5)
for val, lbl in stats:
    add_metric_card(s, sx, Inches(4.2), Inches(1.5), Inches(0.9), val, lbl, fill=RGBColor(0x1E, 0x40, 0x8A), value_color=WHITE, label_color=PALE_BLUE)
    sx += Inches(1.75)

add_text(s, Inches(1), Inches(5.8), Inches(11), Inches(0.4), 'Cognizant  ·  Confidential  ·  2026', size=12, color=GRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THREE-PHASE CONSULTING OFFERING
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Our Consulting Offering', size=24, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'Three phases — from diagnosis to transformation in motion', size=12, color=GRAY)

phases = [
    ('PHASE 1\nDIAGNOSE', '2–4 weeks', BLUE, [
        'AI-generated Current State VSM from your Jira / ADO data',
        'Lead time, flow efficiency & waste quantified per PDLC phase',
        'Top 5 bottlenecks: speed / productivity / quality impact scored',
        'DORA assessment + DevOps maturity scoring (73 questions)',
        'Sector benchmark comparison (12 peer organisations)',
    ], 'VSM Dashboard + Bottleneck Impact Report + DORA Baseline'),
    ('PHASE 2\nDESIGN', '2–3 weeks', TEAL, [
        'Three AI transformation options modelled on your actual data',
        'Option A: AI-Augmented  |  Option B: Hybrid  |  Option C: AI-Native',
        'Business case: editable cost model with 8 token optimisation levers',
        'Target State Studio: L1–L5 maturity path with interim roadmap',
        '7 platform choices compared (Homegrown, STUMP, BMAD, Copilot, Devin, Cursor, Flowsource)',
    ], 'Options Paper + Business Case (3 scenarios) + Target State Roadmap'),
    ('PHASE 3\nDELIVER', 'Ongoing', VIOLET, [
        'Week-by-week implementation playbook for chosen option',
        'Outcome Dashboard: AI Adoption, PDLC Performance, AI Ops perspectives',
        'Productivity economics: SP → Effort → Cost chain with J-Curve modelling',
        'Governance & AI Assurance framework with guardrails',
        'Continuous DORA maturity improvement programme',
    ], 'Playbook + Governance Model + Live Outcome Dashboard'),
]

px = Inches(0.5)
for title, duration, color, bullets, deliverable in phases:
    add_rounded_rect(s, px, Inches(1.3), Inches(3.9), Inches(5.2), fill=None, line=color)
    add_rect(s, px, Inches(1.3), Inches(3.9), Inches(0.9), fill=color)
    add_text(s, px + Inches(0.2), Inches(1.35), Inches(2.5), Inches(0.7), title, size=14, bold=True, color=WHITE)
    add_text(s, px + Inches(2.5), Inches(1.35), Inches(1.2), Inches(0.4), duration, size=10, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
    add_bullet_box(s, px + Inches(0.15), Inches(2.35), Inches(3.6), Inches(3.0), bullets, size=10, color=DGRAY)
    add_rounded_rect(s, px + Inches(0.1), Inches(5.5), Inches(3.7), Inches(0.8), fill=LIGHT_BLUE)
    add_text(s, px + Inches(0.2), Inches(5.55), Inches(3.5), Inches(0.7), f'Deliverable: {deliverable}', size=9, bold=True, color=NAVY)
    px += Inches(4.15)

add_text(s, Inches(0.5), Inches(6.6), Inches(12), Inches(0.4),
    'Platform Advantage:  STUMP compresses Phase 1 from 3 months → 2 weeks, Phase 2 from 6 weeks → 3 weeks, and makes Phase 3 continuous — turning a one-off consulting project into a live operating capability.',
    size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — ADLC MATURITY ROADMAP L1–L5
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'ADLC Maturity Roadmap — L1 to L5', size=24, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'Continuous delivery transformation — from assisted prompting to autonomous ADLC', size=12, color=GRAY)

levels = [
    ('L1', 'Assisted\nPrompting', 'ML1 — Foundation', '20%', 'none', 'all',
     ['Dev & Testing only', '8 human roles retained', 'AI suggests; humans do the work'],
     PALE_BLUE, BLUE),
    ('L2', 'Agent\nCo-pilots', 'ML2 — Augmentation', '40%', 'assistant', 'all',
     ['5 of 7 phases covered', '7 human roles retained', 'Agents draft; humans approve all'],
     PALE_BLUE, BLUE),
    ('L3', 'Supervised\nIndependent', 'ML3 — Automation', '62%', 'independent', 'exceptions',
     ['6 of 7 phases covered', '5 human roles retained', 'Multi-agent hand-offs begin'],
     RGBColor(0xD1, 0xFA, 0xE5), TEAL),
    ('L4', 'Orchestrated\nAgents', 'ML4 — Transformation', '78%', 'orchestrated', 'gates',
     ['All 7 phases covered', '4 roles: Definer + Builder + Arch + Gov', 'Autonomous agent coordination'],
     RGBColor(0xD1, 0xFA, 0xE5), TEAL),
    ('L5', 'Autonomous\nADLC', 'ML5 — Reinvention', '90%', 'orchestrated', 'strategic',
     ['All 7 phases — full fleet', '3 roles: Definer + Builder + Arch', 'Human strategic oversight only'],
     RGBColor(0xFE, 0xF3, 0xC7), AMBER),
]

lx = Inches(0.3)
for lid, label, ml, auto, agent_role, hitl, bullets, fill, accent in levels:
    w = Inches(2.45)
    add_rounded_rect(s, lx, Inches(1.4), w, Inches(5.0), fill=fill, line=accent)
    # Level badge
    add_rounded_rect(s, lx + Inches(0.1), Inches(1.5), Inches(0.6), Inches(0.45), fill=accent)
    add_text(s, lx + Inches(0.1), Inches(1.52), Inches(0.6), Inches(0.4), lid, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, lx + Inches(0.8), Inches(1.5), Inches(1.5), Inches(0.5), label, size=12, bold=True, color=NAVY)
    # ML band
    add_text(s, lx + Inches(0.1), Inches(2.1), w - Inches(0.2), Inches(0.3), ml, size=9, bold=True, color=accent, align=PP_ALIGN.CENTER)
    # Automation bar
    auto_num = int(auto.replace('%', ''))
    add_rect(s, lx + Inches(0.15), Inches(2.45), w - Inches(0.3), Inches(0.2), fill=LGRAY)
    add_rect(s, lx + Inches(0.15), Inches(2.45), Inches((w.inches - 0.3) * auto_num / 100), Inches(0.2), fill=accent)
    add_text(s, lx + Inches(0.1), Inches(2.65), w - Inches(0.2), Inches(0.25), f'Automation: {auto}', size=9, bold=True, color=accent, align=PP_ALIGN.CENTER)
    # Agent role + HITL
    add_text(s, lx + Inches(0.1), Inches(2.95), w - Inches(0.2), Inches(0.2), f'Agent role: {agent_role}', size=8, color=GRAY, align=PP_ALIGN.CENTER)
    add_text(s, lx + Inches(0.1), Inches(3.15), w - Inches(0.2), Inches(0.2), f'HITL: {hitl}', size=8, color=GRAY, align=PP_ALIGN.CENTER)
    # Bullets
    add_bullet_box(s, lx + Inches(0.1), Inches(3.5), w - Inches(0.2), Inches(2.5), bullets, size=9, color=DGRAY)
    lx += Inches(2.55)

add_text(s, Inches(0.5), Inches(6.6), Inches(12), Inches(0.3),
    'As you climb L1 → L5, the team mix inverts: from 95% human / 5% tools to 15% human / 85% agents. Target State Studio auto-generates the interim roadmap with business case per step.',
    size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — CURRENT STATE VSM (PHASE 1 DIAGNOSE)
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Phase 1: Diagnose — Current State Value Stream Map', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'From ALM data to board-ready baseline in 2 weeks, not 3 months', size=12, color=GRAY)

vsm_phases = [
    ('Requirements',    '24h', '108h', '18%', RED),
    ('Design &\nArch',  '31h', '176h', '15%', RED),
    ('Development',      '62h',  '48h', '56%', TEAL),
    ('Code Review',      '16h',  '32h', '33%', BLUE),
    ('Cont. Testing',    '31h', '240h', '11%', RED),
    ('Deploy Prep',       '8h',  '88h',  '8%', RED),
    ('Release &\nOps',   '6h',  '32h', '16%', AMBER),
]

vx = Inches(0.3)
for name, pt, wt, fe, color in vsm_phases:
    w = Inches(1.72)
    add_rounded_rect(s, vx, Inches(1.3), w, Inches(2.5), fill=None, line=color)
    add_rect(s, vx, Inches(1.3), w, Inches(0.5), fill=color)
    add_text(s, vx + Inches(0.05), Inches(1.32), w - Inches(0.1), Inches(0.45), name, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, vx + Inches(0.05), Inches(1.9), w - Inches(0.1), Inches(0.5),
        f'PT: {pt}\nWT: {wt}\nFE: {fe}', size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    vx += Inches(1.82)

add_rect(s, Inches(0.3), Inches(4.0), Inches(12.6), Inches(0.5), fill=NAVY)
add_text(s, Inches(0.5), Inches(4.02), Inches(12), Inches(0.45),
    'TOTAL LEAD TIME: 42 DAYS  |  FLOW EFFICIENCY: 17.8%  |  PROCESS TIME: 178h  |  WAIT TIME: 724h',
    size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Bottleneck dimensions
dims = [
    ('SPEED', [
        'Manual SIT/UAT: 240h wait per feature = 30 days additional LT',
        'Architecture Review Gate: 176h wait = 22 days per feature',
        'Combined: 48% of total lead time is two bottlenecks',
    ]),
    ('PRODUCTIVITY', [
        'Dev teams blocked 30% of sprint time waiting for test environments',
        'Peer review queue averages 4 days — bottleneck for 78% of tickets',
        '$2.1M/yr in engineering time sitting in queues',
    ]),
    ('QUALITY', [
        'Testing phase FE = 11% — 89% is scheduling overhead',
        'Late defect discovery costs 5–10× more than early catch',
        'Only 42% automated test coverage — critical risk exposure',
    ]),
]

dx = Inches(0.5)
for title, bullets in dims:
    add_text(s, dx, Inches(4.7), Inches(3.8), Inches(0.3), title, size=12, bold=True, color=NAVY)
    add_bullet_box(s, dx, Inches(5.05), Inches(3.8), Inches(1.5), bullets, size=9, color=DGRAY)
    dx += Inches(4.2)

footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — TOP 5 BOTTLENECKS
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Top 5 Bottlenecks — Speed, Productivity & Quality Impact', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'Ranked by annual waste cost — with peer benchmark gap', size=12, color=GRAY)

bottlenecks = [
    ('Manual SIT / UAT (Phase 5)', 'Speed + Quality', 'Critical', '240h WT/feature  |  $1.4M/yr',
     'Peer benchmark: 48h WT  |  Gap: 192h', RED),
    ('Architecture Review Gate (Phase 2)', 'Speed + Productivity', 'Critical', '176h WT/feature  |  $960K/yr',
     'Peer benchmark: 24h WT  |  Gap: 152h', RED),
    ('CAB Release Approval (Phase 6)', 'Speed', 'High', '88h WT/feature  |  $480K/yr',
     'Peer benchmark: 8h WT  |  Gap: 80h', AMBER),
    ('Peer Code Review Queue (Phase 4)', 'Productivity', 'High', '32h WT/feature  |  $175K/yr',
     'Peer benchmark: 12h WT  |  Gap: 20h', AMBER),
    ('Test Environment Provisioning (Phase 5)', 'Productivity + Quality', 'Medium', '24h WT/feature  |  $130K/yr',
     'Peer benchmark: 1h WT  |  Gap: 23h', BLUE),
]

by = Inches(1.3)
for name, impact, severity, metric, benchmark, color in bottlenecks:
    add_rounded_rect(s, Inches(0.5), by, Inches(12.3), Inches(0.95), fill=None, line=color)
    add_text(s, Inches(0.7), by + Inches(0.05), Inches(5), Inches(0.35), name, size=13, bold=True, color=NAVY)
    add_text(s, Inches(0.7), by + Inches(0.4), Inches(3), Inches(0.2), f'Impact: {impact}', size=9, color=GRAY)
    # Severity badge
    add_rounded_rect(s, Inches(6.5), by + Inches(0.15), Inches(1.0), Inches(0.35), fill=color)
    add_text(s, Inches(6.5), by + Inches(0.17), Inches(1.0), Inches(0.3), severity, size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, Inches(8), by + Inches(0.1), Inches(4.5), Inches(0.3), metric, size=11, bold=True, color=NAVY)
    add_text(s, Inches(8), by + Inches(0.5), Inches(4.5), Inches(0.3), benchmark, size=9, color=GRAY)
    by += Inches(1.05)

add_rect(s, Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.45), fill=NAVY)
add_text(s, Inches(0.7), Inches(6.62), Inches(12), Inches(0.4),
    'Total identified waste:  $3.1M/yr  |  Fully recoverable with Options A–C  |  Partial recovery in 90 days with Quick Wins',
    size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — THREE TRANSFORMATION OPTIONS
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Phase 2: Design — Three AI Transformation Pathways', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'Choose the pathway that matches your risk appetite, investment capacity, and transformation ambition', size=11, color=GRAY)

options = [
    ('OPTION A', 'AI-Augmented PDLC', 'Human IN the Loop', BLUE, '40%', '35%', '55%', '8', '16', [
        'AI copilots embedded in each phase',
        'All 8 human roles retained — AI assists, humans decide',
        'No process redesign required',
        'Investment: $300K–$600K',
        'ROI: 2.5–3×  |  Payback: 6–9 months',
    ], 'Speed +25% · Productivity +20% · Quality +15%'),
    ('OPTION B ★', 'AI Agents + Human Gates', 'Human ON the Loop', TEAL, '50%', '45%', '60%', '~4.7', '11', [
        'AI agents execute; humans approve at gates',
        '4 dedicated + 0.7 fractional FTE per pod',
        '40–60% effort reduction possible',
        'Investment: $1.2M–$2.0M',
        'ROI: 4–6×  |  Payback: 10–14 months',
    ], 'Speed +55% · Productivity +50% · Quality +35%'),
    ('OPTION C', 'AI-Native ADLC', 'Human ABOVE the Loop', VIOLET, '90%', '70%', '88%', '2.2', '21', [
        'Full 21-agent fleet runs PDLC end-to-end',
        'Product Definer + Product Builder + Architect only',
        '7 platform choices (Homegrown, STUMP, BMAD, etc.)',
        'Investment: $3.0M–$5.0M',
        'ROI: 8–12×  |  Payback: 14–20 months',
    ], 'Speed +80% · Productivity +75% · Quality +60%'),
]

ox = Inches(0.3)
for title, subtitle, hitl, color, auto, pt_r, wt_r, fte, agents, bullets, impact in options:
    w = Inches(4.1)
    add_rounded_rect(s, ox, Inches(1.3), w, Inches(5.2), fill=None, line=color)
    add_rect(s, ox, Inches(1.3), w, Inches(0.75), fill=color)
    add_text(s, ox + Inches(0.15), Inches(1.32), w - Inches(0.3), Inches(0.3), title, size=14, bold=True, color=WHITE)
    add_text(s, ox + Inches(0.15), Inches(1.62), w - Inches(0.3), Inches(0.3), subtitle, size=10, color=WHITE)
    add_text(s, ox + Inches(0.15), Inches(2.15), w - Inches(0.3), Inches(0.25), hitl, size=10, bold=True, color=color, align=PP_ALIGN.CENTER)
    # Metrics row
    metrics = [(f'{auto}', 'Automation'), (f'{fte} FTE', 'Per Pod'), (f'{agents}', 'Agents')]
    mx = ox + Inches(0.15)
    for val, lbl in metrics:
        add_metric_card(s, mx, Inches(2.5), Inches(1.15), Inches(0.65), val, lbl, fill=LIGHT_BLUE, value_color=color, label_color=GRAY)
        mx += Inches(1.25)
    add_bullet_box(s, ox + Inches(0.1), Inches(3.35), w - Inches(0.2), Inches(2.2), bullets, size=9.5, color=DGRAY)
    # Impact bar
    add_rect(s, ox, Inches(5.9), w, Inches(0.45), fill=color)
    add_text(s, ox + Inches(0.1), Inches(5.92), w - Inches(0.2), Inches(0.4), impact, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    ox += Inches(4.35)

footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — OPTION B DETAIL (RECOMMENDED)
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Option B: AI Agents with Human Gates — Human ON the Loop ★', size=22, bold=True, color=TEAL)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'AI executes tasks; engineered approval gates keep humans accountable — without slowing delivery', size=11, color=GRAY)

agents_b = [
    ('Requirements Agent', 'Auto-generates acceptance criteria, user stories, and DoD', 'Product Owner approves before dev starts', BLUE),
    ('Architecture Agent', 'Automated risk scoring + dependency mapping + ADR draft', 'Architect reviews flag list (not full doc)', BLUE),
    ('Development Agents', 'AI writes boilerplate; human engineers own logic + decisions', 'Code review of AI-generated sections', TEAL),
    ('QA Agent', 'AI generates and runs full regression suite; raises defects', 'Engineer validates Critical/High defects only', TEAL),
    ('Release Agent', 'AI assembles release package + change record + rollback plan', 'Change Manager approves risk score > threshold', VIOLET),
    ('Ops Agent', 'AI monitors, correlates incidents, auto-remediates known issues', 'SRE reviews auto-remediation above P2', VIOLET),
]

ay = Inches(1.3)
for name, what, gate, color in agents_b:
    add_rounded_rect(s, Inches(0.5), ay, Inches(5.8), Inches(0.82), fill=None, line=color)
    add_text(s, Inches(0.7), ay + Inches(0.05), Inches(2), Inches(0.3), name, size=11, bold=True, color=NAVY)
    add_text(s, Inches(0.7), ay + Inches(0.35), Inches(5.2), Inches(0.2), what, size=9, color=GRAY)
    add_text(s, Inches(0.7), ay + Inches(0.55), Inches(5.2), Inches(0.2), f'Human gate: {gate}', size=9, bold=True, color=color)
    ay += Inches(0.88)

# Business case summary on right
add_rounded_rect(s, Inches(6.8), Inches(1.3), Inches(5.8), Inches(5.0), fill=LIGHT_BLUE, line=TEAL)
add_text(s, Inches(7.0), Inches(1.4), Inches(5.4), Inches(0.35), 'Option B Business Case Summary', size=14, bold=True, color=NAVY)

bc_items = [
    ('Investment', '$1.2–2.0M', 'One-time migration'),
    ('People per pod', '~4.7 FTE', '4 dedicated + 0.7 fractional'),
    ('Annual savings', '$5.5M portfolio', 'vs current state'),
    ('ROI Multiple', '4–6×', 'Risk-adjusted'),
    ('Payback', '10–14 months', 'From business case approval'),
    ('5-Year NPV', '$28–35M', 'Conservative estimate'),
    ('FE improvement', '17% → 45%', 'Flow efficiency'),
    ('Lead Time', '42 → 18 days', '57% reduction'),
    ('DORA', '+1.0–1.5 levels', 'Band improvement'),
    ('Token cost', '$8K–$18K/mo', 'Per pod LLM spend'),
]

bcy = Inches(1.85)
for label, value, note in bc_items:
    add_text(s, Inches(7.1), bcy, Inches(2.2), Inches(0.22), label, size=9, bold=True, color=NAVY)
    add_text(s, Inches(9.3), bcy, Inches(1.5), Inches(0.22), value, size=10, bold=True, color=TEAL)
    add_text(s, Inches(10.8), bcy, Inches(1.5), Inches(0.22), note, size=8, color=GRAY)
    bcy += Inches(0.32)

footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — OPTION C DETAIL + PLATFORM CHOICES
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Option C: AI-Native ADLC — Full 21-Agent Fleet', size=22, bold=True, color=VIOLET)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'Humans set objectives and govern. AI agents own execution end-to-end. 7 platform choices.', size=11, color=GRAY)

# Agent fleet by phase
fleet = [
    ('Discovery', ['Define Agent', 'Roadmap Agent'], BLUE),
    ('Design', ['Architecture Agent', 'UX/Design Agent', 'DesignDoc Agent'], BLUE),
    ('Development', ['CodeGen Agent', 'TestGen Agent', 'Review Agent'], TEAL),
    ('CI/CD', ['Build Agent', 'Security Agent', 'Deploy Agent'], TEAL),
    ('Testing', ['QA Orchestrator', 'Performance Agent', 'DataGen Agent'], GREEN),
    ('Delivery', ['IaC Agent', 'Release Agent'], VIOLET),
    ('Ops & Gov', ['APM Agent', 'Incident Agent', 'Feedback Agent', 'Compliance Agent', 'MRM Agent', 'Governance Controller'], PURPLE),
]

fx = Inches(0.3)
for phase, agents_list, color in fleet:
    h = Inches(0.25 + len(agents_list) * 0.22)
    add_rounded_rect(s, fx, Inches(1.3), Inches(1.7), h, fill=None, line=color)
    add_text(s, fx + Inches(0.05), Inches(1.32), Inches(1.6), Inches(0.22), phase, size=8, bold=True, color=color)
    for i, agent in enumerate(agents_list):
        add_text(s, fx + Inches(0.1), Inches(1.55) + Inches(i * 0.22), Inches(1.5), Inches(0.2), f'• {agent}', size=7.5, color=DGRAY)
    fx += Inches(1.8)

# 7 Platform choices
add_text(s, Inches(0.5), Inches(3.8), Inches(12), Inches(0.35), '7 Platform Delivery Choices for Option C', size=14, bold=True, color=NAVY)

platforms = [
    ('Homegrown', '26 wks', '6–8 team', 'Full control, no lock-in', NAVY),
    ('STUMP', '18 wks', '2–3 team', 'Pre-wired, fastest path', SKY),
    ('BMAD', '22 wks', '4–5 team', 'Open-source, LLM-agnostic', TEAL),
    ('Copilot WS', '16 wks', '2 team', 'Vendor-managed, fast', BLUE),
    ('Devin', '16 wks', '2–3 team', 'Autonomous SWE agent', VIOLET),
    ('Cursor', '20 wks', '2–3 team', 'AI-native IDE', PURPLE),
    ('Flowsource', '16 wks', '2–4 client', 'Cognizant managed', AMBER),
]

px = Inches(0.3)
for name, timeline, team, tagline, color in platforms:
    add_rounded_rect(s, px, Inches(4.25), Inches(1.7), Inches(2.0), fill=None, line=color)
    add_rect(s, px, Inches(4.25), Inches(1.7), Inches(0.4), fill=color)
    add_text(s, px + Inches(0.05), Inches(4.27), Inches(1.6), Inches(0.35), name, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, px + Inches(0.05), Inches(4.75), Inches(1.6), Inches(0.2), timeline, size=10, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text(s, px + Inches(0.05), Inches(5.0), Inches(1.6), Inches(0.2), team, size=8, color=GRAY, align=PP_ALIGN.CENTER)
    add_text(s, px + Inches(0.05), Inches(5.3), Inches(1.6), Inches(0.7), tagline, size=8, color=DGRAY, align=PP_ALIGN.CENTER)
    px += Inches(1.82)

footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — BUSINESS CASE COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Business Case Comparison — Three Options', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'All three options modelled on your actual ALM data and DORA scores. Editable cost model with 8 token optimisation levers.', size=11, color=GRAY)

headers = ['METRIC', 'OPTION A\nAI-Augmented', 'OPTION B ★\nAgents + Gates', 'OPTION C\nAI-Native']
rows = [
    ['Investment',           '$350–600K',    '$1.2–2.0M',    '$3.0–5.0M'],
    ['Annual Benefit',       '$2.1M',        '$5.5M',         '$18–30M'],
    ['ROI Multiple',         '2.5–3×',      '4–6×',         '8–12×'],
    ['Payback Period',       '6–9 months',  '10–14 months', '14–20 months'],
    ['5-Year NPV',           '$9–11M',      '$28–35M',      '$80–130M'],
    ['Lead Time Reduction',  '25–35%',      '55–70%',       '80–95%'],
    ['Flow Efficiency',      '30%',          '45%',           '75–85%'],
    ['FTE per Pod',          '8 (all roles)','~4.7',        '~2.2'],
    ['Agent Count',          '16',            '11',            '21'],
    ['Automation',           '40%',           '50%',           '90%'],
    ['DORA Improvement',     '+0.5 levels', '+1.0–1.5',    '+2.0 levels'],
    ['Deploy Frequency',     '3×/week',     'Daily',         'Continuous'],
    ['Token Cost (monthly)', '$2K–$5K',     '$8K–$18K',    '$20K–$45K'],
    ['Risk Level',           'LOW',           'MEDIUM',        'HIGH'],
]

# Table rendering
col_w = [Inches(2.2), Inches(2.5), Inches(2.5), Inches(2.5)]
col_x = [Inches(1.8)]
for i in range(3):
    col_x.append(col_x[-1] + col_w[i + 1] + Inches(0.15))

# Headers
for i, (hdr, cx, cw) in enumerate(zip(headers, [Inches(0.5)] + col_x[1:], col_w)):
    color = NAVY if i == 0 else [BLUE, TEAL, VIOLET][i - 1]
    add_rect(s, cx, Inches(1.3), cw, Inches(0.55), fill=color)
    add_text(s, cx + Inches(0.1), Inches(1.32), cw - Inches(0.2), Inches(0.5), hdr, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT)

# Rows
ry = Inches(1.9)
for ri, row in enumerate(rows):
    bg = LIGHT_BLUE if ri % 2 == 0 else None
    for ci, (val, cx, cw) in enumerate(zip(row, [Inches(0.5)] + col_x[1:], col_w)):
        if bg:
            add_rect(s, cx, ry, cw, Inches(0.3), fill=bg)
        add_text(s, cx + Inches(0.1), ry, cw - Inches(0.2), Inches(0.28), val,
                 size=9, bold=(ci == 0), color=NAVY if ci == 0 else DGRAY,
                 align=PP_ALIGN.CENTER if ci > 0 else PP_ALIGN.LEFT)
    ry += Inches(0.3)

add_text(s, Inches(0.5), Inches(6.6), Inches(12), Inches(0.4),
    'All figures from the STUMP Business Case Builder agent. The cost model is fully editable per-project with line-level overrides, custom lines, and 8 LLM token optimisation levers (model tiering, caching, batch API, PTU, prompt compression, rule-based pre-filter, agent consolidation, fine-tuned OSS).',
    size=9, color=GRAY, align=PP_ALIGN.CENTER)
footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — STUMP PLATFORM CAPABILITIES
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'STUMP Platform — Full Capability Map', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), '24 pages, 13 AI agents, 11 routers — the complete multi-agent PDLC transformation platform', size=11, color=GRAY)

groups = [
    ('Overview', ['Dashboard — Project summary & KPIs', 'Outcome Dashboard — 3 perspectives, J-Curve, productivity economics'], SKY),
    ('Setup & Data', ['ALM Connect — Jira / ADO integration', 'DORA Assessment — 4 DORA metrics', 'DevOps Maturity — 73-question assessment', 'Legacy Modernisation — System analysis', 'VSM Editor — Override metrics'], BLUE),
    ('Current State', ['Current State VSM — 7 phases, 36 activities', 'Bottleneck Analysis — Speed / Productivity / Quality', 'Improvements — AI agent recommendations per bottleneck', 'Operations Intelligence — Operational monitoring'], TEAL),
    ('Future State', ['Target State Studio — 4-step wizard, L1–L5 path', 'Future State VSM — Options A / B / C with per-phase metrics', 'Business Case — Editable cost model, 7 platforms, 8 token levers', 'Transformation Readiness — Readiness scoring'], VIOLET),
    ('AI Insights', ['Accuracy & RAG — 8-step pipeline scoring (A+ to F)', 'Recommendations — Consolidated AI recommendations', 'AI Agents — Agent catalog & monitoring', 'Playbook — Personalised implementation playbook', 'Role Responsibilities — Role-based slides'], PURPLE),
    ('Governance', ['Governance & Guardrails — Framework & policies', 'AI Assurance — Model risk & assurance'], AMBER),
]

gx = Inches(0.3)
for gname, pages, color in groups:
    w = Inches(2.0)
    h = Inches(0.3 + len(pages) * 0.32)
    add_rounded_rect(s, gx, Inches(1.3), w, min(h, Inches(5.1)), fill=None, line=color)
    add_rect(s, gx, Inches(1.3), w, Inches(0.35), fill=color)
    add_text(s, gx + Inches(0.05), Inches(1.32), w - Inches(0.1), Inches(0.3), gname, size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for i, page in enumerate(pages):
        add_text(s, gx + Inches(0.05), Inches(1.72) + Inches(i * 0.32), w - Inches(0.1), Inches(0.3), f'• {page}', size=7, color=DGRAY)
    gx += Inches(2.12)

# Backend agents
add_text(s, Inches(0.5), Inches(5.1), Inches(12), Inches(0.35), 'Backend AI Agents (LangGraph Pipeline)', size=13, bold=True, color=NAVY)
agent_names = [
    'ALM Connector', 'VSM Analyzer', 'Benchmark Agent', 'Bottleneck Analyzer',
    'Improvement Generator', 'Future State Designer', 'Business Case Builder',
    'Accuracy Scorer', 'Playbook Contextualizer', 'DevOps Maturity Agent',
    'Target State (catalog + compare + roadmap + progress)', 'Outcome Metrics (6 modules)', 'RAG Engine',
]
ax = Inches(0.5)
ay = Inches(5.5)
for i, aname in enumerate(agent_names):
    w = Inches(2.3) if len(aname) > 20 else Inches(1.8)
    add_rounded_rect(s, ax, ay, w, Inches(0.3), fill=LIGHT_BLUE, line=BLUE)
    add_text(s, ax + Inches(0.05), ay + Inches(0.02), w - Inches(0.1), Inches(0.25), aname, size=7.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    ax += w + Inches(0.1)
    if ax > Inches(11):
        ax = Inches(0.5)
        ay += Inches(0.38)

footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — IMPLEMENTATION PLAYBOOK
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'Implementation Playbook — Option B (Recommended)', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'Week-by-week programme from business case approval to first Quick Win — AI-generated, grounded in your VSM data', size=11, color=GRAY)

playbook = [
    ('QUICK WINS', '0–90 Days', '$350K → $1.4M/yr', TEAL, [
        'Deploy AI UAT Agent — eliminate 192h/feature testing queue',
        'Implement AI Architecture Review Board — reduce 152h gate to 24h',
        'AI Release Risk Classifier — CAB approval automated for 85%',
        'First VSM re-run: validate 10-day lead time reduction',
        'Expected: LT 42 → 32 days, FE 17% → 28%',
    ]),
    ('MEDIUM-TERM', '3–6 Months', '$600K → $2.1M/yr', BLUE, [
        'AI Development Agents — code review automation for boilerplate',
        'Requirements Agent — auto-generate AC from PRDs',
        'Ops Agent — 24/7 monitoring + auto-remediation',
        'Process redesign: define human gates at phase boundaries',
        'Expected: LT 32 → 18 days, FE 28% → 45%',
    ]),
    ('STRATEGIC', '6–12 Months', '$1.0M → $2.0M/yr', VIOLET, [
        'Full agent orchestration across all 7 PDLC phases',
        'Human gate governance model: defined approval thresholds',
        'DORA maturity: WALK → RUN (score 2.1 → 3.5)',
        'Outcome Dashboard live with all 3 perspectives + productivity economics',
        'Expected: LT 18 → 8 days, FE 45% → 61%',
    ]),
]

px = Inches(0.3)
for title, timeframe, invest, color, bullets in playbook:
    w = Inches(4.1)
    add_rounded_rect(s, px, Inches(1.3), w, Inches(5.0), fill=None, line=color)
    add_rect(s, px, Inches(1.3), w, Inches(0.7), fill=color)
    add_text(s, px + Inches(0.15), Inches(1.32), Inches(2.5), Inches(0.3), title, size=14, bold=True, color=WHITE)
    add_text(s, px + Inches(0.15), Inches(1.62), Inches(2.5), Inches(0.25), timeframe, size=10, color=WHITE)
    add_text(s, px + Inches(2.5), Inches(1.35), Inches(1.4), Inches(0.3), invest, size=9, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
    add_bullet_box(s, px + Inches(0.1), Inches(2.2), w - Inches(0.2), Inches(3.5), bullets, size=10, color=DGRAY)
    px += Inches(4.35)

add_text(s, Inches(0.5), Inches(6.5), Inches(12), Inches(0.5),
    'Full playbook with week-by-week actions, owners, and expected metrics is generated by the STUMP Playbook Contextualizer agent from your Jira data and team context. No generic templates — every action is grounded in your actual bottleneck data.',
    size=9, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — FRONTIER POD MODEL
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
add_bg(s, WHITE)
add_text(s, Inches(0.5), Inches(0.3), Inches(12), Inches(0.5), 'The Frontier Pod — Post-ADLC Operating Model', size=22, bold=True, color=NAVY)
add_text(s, Inches(0.5), Inches(0.8), Inches(10), Inches(0.3), 'When ADLC is achieved: 1–3 FTE per pod, 80%+ digital workforce, every FTE a Frontier Engineer', size=11, color=GRAY)

# Human roles
roles = [
    ('Product Definer', '1 FTE', 'Frames the problem, sets OKRs, directs Define Agent, owns customer outcome', BLUE),
    ('Product Builder', '1 FTE', 'Directs Dev/QA/Deploy agents, reviews code, clears exceptions, owns ops', TEAL),
    ('Frontier Principal', '0.2 FTE\n(shared)', 'Architecture policy, governs fleet, dual mastery, earned not assigned', AMBER),
]

ry = Inches(1.3)
for name, fte, desc, color in roles:
    add_rounded_rect(s, Inches(0.5), ry, Inches(5.5), Inches(0.85), fill=None, line=color)
    add_rounded_rect(s, Inches(0.6), ry + Inches(0.1), Inches(0.6), Inches(0.6), fill=color)
    add_text(s, Inches(0.6), ry + Inches(0.15), Inches(0.6), Inches(0.5), '👤', size=18, align=PP_ALIGN.CENTER, color=WHITE)
    add_text(s, Inches(1.4), ry + Inches(0.08), Inches(2.5), Inches(0.3), name, size=12, bold=True, color=NAVY)
    add_text(s, Inches(4.3), ry + Inches(0.08), Inches(1.5), Inches(0.3), fte, size=10, bold=True, color=color, align=PP_ALIGN.RIGHT)
    add_text(s, Inches(1.4), ry + Inches(0.42), Inches(4.3), Inches(0.35), desc, size=9, color=GRAY)
    ry += Inches(0.92)

# Arrow
add_text(s, Inches(6.2), Inches(2.2), Inches(0.5), Inches(0.5), '→', size=28, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

# Agent fleet
add_rounded_rect(s, Inches(6.8), Inches(1.3), Inches(6.0), Inches(2.6), fill=RGBColor(0xEC, 0xFD, 0xF5), line=TEAL)
add_text(s, Inches(7.0), Inches(1.4), Inches(5.5), Inches(0.3), '🤖  Digital Workforce — 21 Agents', size=13, bold=True, color=NAVY)

fleet_summary = [
    ('Discovery & Design', '5 agents'),
    ('Development', '3 agents'),
    ('CI/CD & Testing', '6 agents'),
    ('Delivery & Ops', '4 agents'),
    ('Governance', '3 agents'),
]

fy = Inches(1.8)
for phase, count in fleet_summary:
    add_text(s, Inches(7.1), fy, Inches(3.5), Inches(0.22), phase, size=9, color=DGRAY)
    add_text(s, Inches(10.5), fy, Inches(1.5), Inches(0.22), count, size=9, bold=True, color=TEAL, align=PP_ALIGN.RIGHT)
    fy += Inches(0.28)

# Impact metrics
impact_cards = [
    ('97%', 'Team Reduction'),
    ('85%', 'Digital Workforce'),
    ('$400/SP', 'Cost per SP'),
    ('75%', 'Flow Efficiency'),
    ('3 days', 'Lead Time'),
    ('4.4×', 'Revenue/FTE'),
]

cx = Inches(0.5)
for val, label in impact_cards:
    add_metric_card(s, cx, Inches(4.3), Inches(1.8), Inches(0.85), val, label, fill=LIGHT_BLUE, value_color=NAVY)
    cx += Inches(2.05)

# New literacy
add_text(s, Inches(0.5), Inches(5.5), Inches(12), Inches(0.3), 'The New Literacy — No Programming Language Required', size=13, bold=True, color=NAVY)

literacy = [
    ('1. Understand', 'Deep domain knowledge is your moat. The bridge from AI to production value is built by people who understand the business.'),
    ('2. Direct', 'Prompting is the new management. The quality of agent output is proportional to the quality of your direction.'),
    ('3. Judge', 'Know what "good" looks like. Spot when the machine is confidently wrong. Own the outcome.'),
]

lx = Inches(0.5)
for title, desc in literacy:
    add_rounded_rect(s, lx, Inches(5.9), Inches(3.8), Inches(0.7), fill=RGBColor(0xF5, 0xF3, 0xFF), line=VIOLET)
    add_text(s, lx + Inches(0.1), Inches(5.92), Inches(3.6), Inches(0.25), title, size=10, bold=True, color=VIOLET)
    add_text(s, lx + Inches(0.1), Inches(6.2), Inches(3.6), Inches(0.35), desc, size=8, color=DGRAY)
    lx += Inches(4.1)

footer(s)


# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════
OUTPUT = 'SDLC-to-ADLC-Refined-v2.pptx'
prs.save(OUTPUT)
print(f'\n✅  Saved: {OUTPUT}')
print(f'   12 slides — same Cognizant Navy/Blue palette')
print(f'   Updated with latest STUMP platform: 24 pages, 13 agents, 7 platforms')
print(f'   New slides: L1-L5 maturity, 7 platform choices, Frontier Pod model')
