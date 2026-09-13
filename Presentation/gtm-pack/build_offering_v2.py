"""
Refined Offering Slide + Reworked CXO Pitch Deck
Narrative: Consulting Offering (Diagnose → Design → Deliver)
  Phase 1 – Current State VSM Map: quantify speed / productivity / quality impact
  Phase 2 – Three AI Transformation Options:
             A: AI-Augmented PDLC (human in the loop)
             B: AI Agents + Human in the Loop
             C: Fully Agentic (human above the loop)
  Phase 3 – Business Case + Implementation Playbook per option
  Accelerator: STUMP makes the offering 5× faster, AI-accurate, lower cost

Generates:
  01b-offering-slide-v2.pptx  (1 slide, the definitive offering positioning visual)
  01-cxo-pitch-deck-v2.pptx   (15 slides, offering-centric CXO narrative)
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gtm_model_2026 as M  # shared 2026 narrative (ladder, platforms, J-curve, dashboard)

OUT = "/Users/125066/projects/pdlc-vsm-platform/gtm-pack/set1-cxo-gtm-pack"
os.makedirs(OUT, exist_ok=True)

# ── Colors ───────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0F, 0x2D, 0x5E)   # darkest blue
BLUE   = RGBColor(0x25, 0x63, 0xEB)   # mid blue
STEEL  = RGBColor(0x1E, 0x40, 0x8A)   # steel blue
PALE   = RGBColor(0xDB, 0xEA, 0xFE)   # very light blue
GHOST  = RGBColor(0xEF, 0xF6, 0xFF)   # ghost blue (near white)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
TEXT   = RGBColor(0x1E, 0x29, 0x3B)   # near-black text
LBLUE  = RGBColor(0x93, 0xC5, 0xFD)   # light blue accent
SILVER = RGBColor(0xE2, 0xE8, 0xF0)

# Option palette (still all blue family)
OPT_A  = RGBColor(0x1E, 0x40, 0x8A)   # dark steel  – Augment
OPT_B  = RGBColor(0x25, 0x63, 0xEB)   # mid blue    – Agents-in-loop
OPT_C  = RGBColor(0x0F, 0x2D, 0x5E)   # navy        – Above the loop


# ── PPTX helpers ─────────────────────────────────────────────────────────────
def prs():
    p = Presentation()
    p.slide_width  = Inches(13.33)
    p.slide_height = Inches(7.5)
    return p

def blank(p):
    return p.slides.add_slide(p.slide_layouts[6])

def R(sl, x, y, w, h, fill=None, line_color=None, line_w=Pt(0.75)):
    """Add a rectangle. x/y/w/h in inches."""
    sh = sl.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.line.fill.background()
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    if line_color:
        sh.line.color.rgb = line_color; sh.line.width = line_w
    else:
        sh.line.fill.background()
    return sh

def T(sl, text, x, y, w, h, size=11, bold=False, italic=False,
      color=None, align=PP_ALIGN.LEFT, wrap=True):
    """Add a textbox."""
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.word_wrap = wrap
    tf = tb.text_frame; tf.word_wrap = wrap
    p  = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color or TEXT
    run.font.name  = "Calibri"
    return tb

def MT(sl, lines, x, y, w, h, size=10, color=None, bold_first=False):
    """Multi-line textbox — lines is a list of strings."""
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.word_wrap = True
    tf = tb.text_frame; tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Emu(0)
        run = p.add_run(); run.text = line
        run.font.size  = Pt(size)
        run.font.bold  = bold_first and i == 0
        run.font.color.rgb = color or TEXT
        run.font.name  = "Calibri"
    return tb

def stat(sl, x, y, w, h, value, label, bg=BLUE, value_size=26):
    """KPI stat box."""
    R(sl, x, y, w, h, fill=bg)
    T(sl, value, x, y+0.06, w, h*0.52, size=value_size, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, label, x, y+h*0.52, w, h*0.46, size=8.5, color=WHITE,
      align=PP_ALIGN.CENTER, wrap=True)

def hdr(sl, title, sub=None):
    R(sl, 0, 0, 13.33, 1.05, fill=NAVY)
    T(sl, title, 0.4, 0.1, 10, 0.55, size=22, bold=True, color=WHITE)
    if sub:
        T(sl, sub, 0.4, 0.62, 10, 0.38, size=11,
          color=RGBColor(0xBF,0xDB,0xFE))

def option_col(sl, x, w, label, tagline, points, outcome, col):
    """Render one of the three AI-option columns."""
    # Header band
    R(sl, x, 0.0, w, 0.52, fill=col)
    T(sl, label,   x, 0.02, w, 0.28, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, tagline, x, 0.30, w, 0.22, size=8,  color=WHITE, align=PP_ALIGN.CENTER)
    # Body
    R(sl, x, 0.52, w, 6.25, fill=GHOST)
    # Bullet points
    for j, pt in enumerate(points):
        T(sl, f"• {pt}", x+0.12, 0.62 + j*0.56, w-0.24, 0.52,
          size=9.5, color=TEXT, wrap=True)
    # Outcome footer
    R(sl, x, 6.77, w, 0.73, fill=col)
    T(sl, outcome, x+0.1, 6.8, w-0.2, 0.68, size=9,
      color=WHITE, wrap=True, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# FILE 1 — OFFERING SLIDE V2
# Storyline in one slide:
#   Top strip:   Offering name + value headline
#   Row A:       Three-phase offering arc (Diagnose / Design / Deliver)
#   Row B:       Three AI options within Design phase
#   Footer:      Platform-as-accelerator bar
# ══════════════════════════════════════════════════════════════════════════════
print("Building 01b-offering-slide-v2.pptx...")
deck = prs()
sl   = blank(deck)

# ── Background
R(sl, 0, 0, 13.33, 7.5, fill=WHITE)

# ── Top brand strip
R(sl, 0, 0, 13.33, 0.55, fill=NAVY)
T(sl, "AI-POWERED PDLC TRANSFORMATION", 0.25, 0.05, 7, 0.45,
  size=17, bold=True, color=WHITE)
T(sl, "A consulting offering accelerated by the STUMP",
  7.3, 0.1, 5.8, 0.4, size=10, italic=True,
  color=RGBColor(0xBF,0xDB,0xFE), align=PP_ALIGN.RIGHT)

# ── Offering tagline
T(sl, "Quantify the hidden cost in your delivery pipeline. Design the right AI transformation pathway. "
      "Implement with a board-ready business case and a week-by-week playbook.",
  0.3, 0.65, 12.7, 0.52, size=10.5, italic=True, color=STEEL)

# ── Phase arc: THREE PHASES ──────────────────────────────────────────────────
phase_y = 1.26
phase_h = 1.68

phases = [
    (NAVY,  "PHASE 1",  "DIAGNOSE",
     ["Map your current PDLC as a value stream",
      "AI-quantify lead time, flow efficiency & waste per phase",
      "Identify top 5 bottlenecks: speed / productivity / quality impact",
      "Benchmark vs. sector peers"]),
    (STEEL, "PHASE 2",  "DESIGN",
     ["Target State Studio: pick North-Star level + delivery platform",
      "L1–L5 interim ladder (A≈L2 · B≈L3–L4 · C≈L5 Autonomous ADLC)",
      "Platform choice: home-grown / COTS / Cognizant Flowsource",
      "DORA J-Curve business case per interim step (cost-only)"]),
    (BLUE,  "PHASE 3",  "DELIVER",
     ["Execute interim steps with operating model + agents/tools",
      "Continuous 3-perspective Outcome Dashboard (adoption · performance · AI-ops)",
      "Investment → J-Curve dip → breakeven → compounding savings",
      "Progress tracked vs interim / target maturity"]),
]

PW = 4.18   # phase column width
GAP = 0.09

for i, (col, num, label, bullets) in enumerate(phases):
    x = 0.18 + i * (PW + GAP)
    # Colored header
    R(sl, x, phase_y, PW, 0.52, fill=col)
    T(sl, num,   x+0.12, phase_y+0.02, 1.0, 0.24, size=9, bold=True, color=RGBColor(0xBF,0xDB,0xFE))
    T(sl, label, x+0.12, phase_y+0.22, PW-0.24, 0.28, size=13, bold=True, color=WHITE)
    # Body
    R(sl, x, phase_y+0.52, PW, phase_h-0.52, fill=GHOST)
    for j, b in enumerate(bullets):
        T(sl, f"• {b}", x+0.14, phase_y+0.58 + j*0.29, PW-0.28, 0.28,
          size=8.5, color=TEXT, wrap=True)
    # Connector arrow (not last)
    if i < 2:
        ax = x + PW + 0.01
        T(sl, "▶", ax, phase_y+0.62, 0.1, 0.35, size=14, bold=True, color=NAVY)

# ── THREE AI OPTIONS ─────────────────────────────────────────────────────────
opt_y  = 3.08
opt_h  = 1.72
OW     = 4.18

opts = [
    (OPT_A, "OPTION A  ·  L2", "AI-AUGMENTED PDLC",
     "Human in the Loop  ·  L2 Agent Co-pilots",
     ["AI copilots assist at each PDLC phase",
      "Humans retain all decision rights",
      "Effort reduction: 15–25% per phase",
      "Fastest to adopt — no process redesign",
      "Cost-only ROI on the J-Curve  |  earliest breakeven"],
     "Speed +25%  |  Productivity +20%  |  Quality +15%"),
    (OPT_B, "OPTION B  ·  L3–L4", "AI AGENTS + HUMAN GATES",
     "Human on the Loop  ·  L3–L4 Supervised → Orchestrated",
     ["AI agents execute PDLC tasks autonomously",
      "Humans review and approve at defined gates",
      "Effort reduction: 40–60% across value stream",
      "Requires 3–6 month process redesign",
      "Strong cost-only ROI  |  breakeven after the J-Curve dip"],
     "Speed +55%  |  Productivity +50%  |  Quality +35%"),
    (OPT_C, "OPTION C  ·  L5", "FULLY AGENTIC ADLC",
     "Human Above the Loop  ·  L5 Autonomous ADLC (North Star)",
     ["AI agents own end-to-end PDLC execution",
      "Humans set objectives, review exceptions",
      "Effort reduction: 70–80% across value stream",
      "Full operating model transformation",
      "Highest ROI at scale  |  largest up-front J-Curve investment"],
     "Speed +75%  |  Productivity +75%  |  Quality +60%"),
]

for i, (col, num, label, sub, bullets, outcome) in enumerate(opts):
    x = 0.18 + i * (OW + GAP)
    # Option header
    R(sl, x, opt_y, OW, 0.46, fill=col)
    T(sl, num,    x+0.12, opt_y+0.02, 1.2, 0.21, size=8.5, bold=True, color=LBLUE)
    T(sl, label,  x+0.12, opt_y+0.20, OW-0.24, 0.24, size=11, bold=True, color=WHITE)
    T(sl, sub,    x+0.12, opt_y+0.43, OW-0.24, 0.22, size=8, italic=True, color=WHITE)
    # Body
    R(sl, x, opt_y+0.65, OW, opt_h-0.65-0.42, fill=PALE)
    for j, b in enumerate(bullets):
        T(sl, f"• {b}", x+0.12, opt_y+0.70 + j*0.25, OW-0.24, 0.24,
          size=8.5, color=TEXT, wrap=True)
    # Outcome band
    R(sl, x, opt_y+opt_h-0.42, OW, 0.42, fill=col)
    T(sl, outcome, x+0.08, opt_y+opt_h-0.40, OW-0.16, 0.38,
      size=8.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ── Accelerator divider label
T(sl, "PDLC VSM PLATFORM — THE DELIVERY ACCELERATOR", 0.18, 4.9,
  12.97, 0.3, size=8.5, bold=True, color=NAVY)

# ── Platform accelerator bar (3 zones) ──────────────────────────────────────
acc_y = 5.22
acc_h = 0.78
accs = [
    (NAVY,  "MINUTES-NOT-MONTHS DIAGNOSIS",
     "AI ingests your Jira/ADO data and generates a validated VSM + bottleneck analysis in minutes; current maturity level auto-derived"),
    (STEEL, "TARGET STATE STUDIO + J-CURVE",
     "Configure North-Star level + platform (home-grown/COTS/Flowsource); auto-generate the L1–L5 interim roadmap with a DORA J-Curve business case"),
    (BLUE,  "3-PERSPECTIVE OUTCOME DASHBOARD",
     "Always-on measurement across AI Adoption · PDLC Performance · AI Ops & Assurance — investment, breakeven and compounding savings tracked live"),
]
AW = (13.33 - 0.18*2 - GAP*2) / 3
for i, (col, head, desc) in enumerate(accs):
    x = 0.18 + i * (AW + GAP)
    R(sl, x, acc_y, AW, acc_h, fill=col)
    T(sl, head, x+0.1, acc_y+0.04, AW-0.2, 0.28, size=9.5, bold=True, color=WHITE)
    T(sl, desc, x+0.1, acc_y+0.30, AW-0.2, 0.46, size=8, color=WHITE, wrap=True)

# ── Outcomes footer ──────────────────────────────────────────────────────────
R(sl, 0, 6.1, 13.33, 1.4, fill=GHOST)
R(sl, 0, 6.1, 13.33, 0.28, fill=SILVER)
T(sl, "TYPICAL CLIENT OUTCOMES  (US Bank, Team Phoenix — Financial Services)",
  0.25, 6.12, 12.8, 0.25, size=8.5, bold=True, color=NAVY)

outcomes = [
    ("42 → 8 days", "Lead Time"),
    ("17.8% → 61%", "Flow Efficiency"),
    ("4.2×", "ROI (Option B)"),
    ("$3M invest.", "$8.4M/yr benefit"),
    ("14 months", "Payback Period"),
    ("$31.2M", "5-Year NPV"),
]
OX = 0.25
OW2 = 13.83 / len(outcomes)
for i, (val, lbl) in enumerate(outcomes):
    x = OX + i * OW2
    T(sl, val, x, 6.44, OW2-0.05, 0.38, size=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    T(sl, lbl, x, 6.82, OW2-0.05, 0.22, size=8,  color=STEEL, align=PP_ALIGN.CENTER)

deck.save(os.path.join(OUT, "01b-offering-slide-v2.pptx"))
print("  ✓ Saved: 01b-offering-slide-v2.pptx")


# ══════════════════════════════════════════════════════════════════════════════
# FILE 2 — CXO PITCH DECK V2  (15 slides, offering-centric)
# ══════════════════════════════════════════════════════════════════════════════
print("Building 01-cxo-pitch-deck-v2.pptx...")
deck = prs()


# ── Slide 1: Cover ────────────────────────────────────────────────────────────
sl = blank(deck)
R(sl, 0, 0, 13.33, 7.5, fill=NAVY)
R(sl, 0, 4.8, 13.33, 2.7, fill=BLUE)
R(sl, 0, 4.78, 13.33, 0.06, fill=LBLUE)  # accent line
T(sl, "[CLIENT NAME]", 1.0, 0.55, 11, 0.45, size=16,
  color=RGBColor(0xBF,0xDB,0xFE))
T(sl, "AI-Powered PDLC Transformation", 1.0, 1.1, 11, 0.75,
  size=34, bold=True, color=WHITE)
T(sl, "From Value Stream Diagnosis to Fully Agentic Delivery", 1.0, 1.95, 11, 0.55,
  size=19, color=RGBColor(0xBF,0xDB,0xFE))
T(sl, "A consulting offering delivered 5× faster and at optimal cost\n"
      "through the STUMP",
  1.0, 2.7, 10, 0.7, size=14, italic=True, color=LBLUE)
T(sl, "[DATE]  |  Confidential",
  1.0, 5.2, 11, 0.45, size=15, color=WHITE)
T(sl, "Powered by LangGraph AI Agents + Claude",
  1.0, 5.72, 11, 0.35, size=12,
  color=RGBColor(0xBF,0xDB,0xFE))


# ── Slide 2: The Burning Platform ────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "The Delivery Challenge", "Why acting now costs less than waiting 12 months")
T(sl, "Your engineering teams are delivering at a fraction of their potential.\n"
      "The cause is invisible in your sprint reports — and measurable in hours and dollars.",
  0.5, 1.15, 12.3, 0.6, size=14, italic=True, color=STEEL)

problems = [
    ("34–47 days", "Average feature lead time in Financial Services\n— most of it sitting in queues, not being worked on"),
    ("17.8%",      "Typical flow efficiency — 82¢ of every $1 spent\non engineering goes to wait time, not value"),
    ("3–6 months", "Time a traditional consultancy takes to map\nyour value stream and identify bottlenecks"),
    ("$0",         "Value delivered during that 3–6 month diagnosis\nbefore any improvement even starts"),
]
for i, (val, desc) in enumerate(problems):
    x = 0.4 + i * 3.2
    R(sl, x, 1.95, 2.85, 2.5, fill=NAVY if i % 2 == 0 else STEEL)
    T(sl, val,  x+0.1, 2.05, 2.65, 0.75,
      size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, desc, x+0.1, 2.85, 2.65, 1.4,
      size=11, color=WHITE, wrap=True, align=PP_ALIGN.CENTER)

T(sl, "The question is not whether to transform your PDLC — it's which pathway fits your risk appetite, "
      "and how quickly you can get the evidence to make the investment decision.",
  0.5, 4.65, 12.3, 0.6, size=13, italic=True, color=NAVY)
T(sl, "That's exactly what this engagement is designed to answer.",
  0.5, 5.3, 12.3, 0.4, size=15, bold=True, color=BLUE)


# ── Slide 3: The Consulting Offering ─────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Our Consulting Offering", "Three phases — from diagnosis to transformation in motion")

phases3 = [
    (NAVY,  "PHASE 1\nDIAGNOSE",
     "2–4 weeks",
     ["AI-generated Current State VSM from your Jira / ADO data",
      "Lead time, flow efficiency, and waste quantified per PDLC phase",
      "Top 5 bottlenecks: speed / productivity / quality impact scored",
      "Sector benchmark comparison (12 peer organisations)"],
     "Deliverable: VSM Dashboard + Bottleneck Impact Report"),
    (STEEL, "PHASE 2\nDESIGN",
     "2–3 weeks",
     ["Three AI transformation options modelled on your actual data",
      "Option A: AI-Augmented  |  Option B: Agents-in-Loop  |  Option C: Above-the-Loop",
      "Business case: ROI, payback, NPV for each option",
      "Risk and dependency analysis per pathway"],
     "Deliverable: Options Paper + Business Case (3 scenarios)"),
    (BLUE,  "PHASE 3\nDELIVER",
     "Ongoing",
     ["Week-by-week implementation playbook for chosen option",
      "Change management and governance model",
      "Platform-tracked benefits realisation vs. business case",
      "Continuous DORA maturity improvement programme"],
     "Deliverable: Playbook + Governance Model + Benefits Tracker"),
]
PW3 = 4.05
for i, (col, label, timing, bullets, deliv) in enumerate(phases3):
    x = 0.22 + i * (PW3 + 0.12)
    R(sl, x, 1.15, PW3, 0.68, fill=col)
    T(sl, label, x+0.14, 1.18, PW3-0.28, 0.42, size=16, bold=True, color=WHITE)
    T(sl, timing, x+0.14, 1.6, PW3-0.28, 0.22, size=11,
      color=RGBColor(0xBF,0xDB,0xFE))
    R(sl, x, 1.83, PW3, 4.1, fill=GHOST)
    for j, b in enumerate(bullets):
        T(sl, f"• {b}", x+0.16, 1.92 + j*0.52, PW3-0.32, 0.48,
          size=11.5, color=TEXT, wrap=True)
    R(sl, x, 5.93, PW3, 0.55, fill=col)
    T(sl, deliv, x+0.12, 5.96, PW3-0.24, 0.5, size=10.5,
      bold=True, color=WHITE, wrap=True)
    if i < 2:
        T(sl, "▶", x + PW3 + 0.02, 2.35, 0.12, 0.35, size=18, bold=True, color=NAVY)

R(sl, 0, 6.56, 13.33, 0.94, fill=NAVY)
T(sl, "Platform Advantage:  STUMP compresses Phase 1 from 3 months → 2 weeks, "
      "Phase 2 from 6 weeks → 3 weeks, and makes Phase 3 continuous — "
      "turning a one-off consulting project into a live operating capability.",
  0.4, 6.6, 12.5, 0.85, size=11.5, color=WHITE, wrap=True)


# ── Slide 4: Phase 1 Detail — Current State VSM ──────────────────────────────
sl = blank(deck)
hdr(sl, "Phase 1: Diagnose — Current State Value Stream Map",
    "From ALM data to board-ready baseline in 2 weeks, not 3 months")

phases_vsm = [
    ("Requirements",      "PT: 24h\nWT: 108h\nFE: 18%"),
    ("Design &\nArch",    "PT: 31h\nWT: 176h\nFE: 15%"),
    ("Development",       "PT: 62h\nWT: 48h\nFE: 56%"),
    ("Code Review",       "PT: 16h\nWT: 32h\nFE: 33%"),
    ("Cont. Testing",     "PT: 31h\nWT: 240h\nFE: 11%"),
    ("Deploy Prep",       "PT: 8h\nWT: 88h\nFE: 8%"),
    ("Release &\nOps",    "PT: 6h\nWT: 32h\nFE: 16%"),
]
PVW = 1.72
for i, (ph, metrics) in enumerate(phases_vsm):
    x = 0.25 + i * (PVW + 0.04)
    fe = int(metrics.split("FE: ")[1].rstrip("%"))
    col = RGBColor(0xEF,0x44,0x44) if fe < 15 else (STEEL if fe < 30 else BLUE)
    R(sl, x, 1.15, PVW, 0.62, fill=col)
    T(sl, ph, x, 1.15, PVW, 0.62, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    R(sl, x, 1.77, PVW, 0.88, fill=GHOST)
    T(sl, metrics, x+0.05, 1.8, PVW-0.1, 0.82, size=10.5, color=TEXT)

R(sl, 0.25, 2.65, 12.6, 0.05, fill=NAVY)
T(sl, "TOTAL LEAD TIME: 42 DAYS  |  FLOW EFFICIENCY: 17.8%  |  PROCESS TIME: 178h  |  WAIT TIME: 724h",
  0.25, 2.75, 12.6, 0.38, size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
T(sl, "■ RED phases (FE < 15%) = critical waste zones   ■ Source: 2,847 Jira tickets, Team Phoenix, Jan–Dec 2024",
  0.25, 3.18, 12.6, 0.32, size=11, color=RGBColor(0xEF,0x44,0x44))

# Speed / Productivity / Quality impact table
R(sl, 0, 3.58, 13.33, 0.36, fill=NAVY)
T(sl, "BOTTLENECK IMPACT BY DIMENSION", 0.4, 3.62, 12.5, 0.3, size=12, bold=True, color=WHITE)

dims = [
    ("SPEED", [
        "Manual SIT/UAT: 240h wait per feature = 30 days additional LT",
        "Architecture Review Gate: 176h wait = 22 days per feature",
        "Combined: 48% of total lead time is two bottlenecks"]),
    ("PRODUCTIVITY", [
        "Dev teams blocked 30% of sprint time waiting for test environments",
        "Peer review queue averages 4 days — bottleneck for 78% of tickets",
        "$2.1M/yr in engineering time sitting in queues"]),
    ("QUALITY", [
        "Testing phase FE = 11% — 89% of testing cycle is scheduling overhead",
        "Late defect discovery (Phase 5/6) costs 5–10× more than Phase 2 catch",
        "Change failure rate 2.3× sector average due to compressed testing"]),
]
for i, (dim, points) in enumerate(dims):
    x = 0.25 + i * 4.36
    R(sl, x, 3.97, 4.15, 0.4, fill=STEEL)
    T(sl, dim, x, 3.97, 4.15, 0.4, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for j, pt in enumerate(points):
        T(sl, f"• {pt}", x+0.1, 4.43 + j*0.4, 4.0, 0.38, size=11, color=TEXT, wrap=True)


# ── Slide 5: Bottleneck Scorecard ─────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Top 5 Bottlenecks — Speed, Productivity & Quality Impact",
    "Ranked by annual waste cost — with peer benchmark gap")

bottlenecks = [
    ("Manual SIT / UAT (Phase 5)",
     "Critical", "Speed + Quality",
     "240h WT/feature  |  $1.4M/yr",
     "Peer benchmark: 48h WT  |  Gap: 192h  |  Humana: 96% automated"),
    ("Architecture Review Gate (Phase 2)",
     "Critical", "Speed + Productivity",
     "176h WT/feature  |  $960K/yr",
     "Peer benchmark: 24h WT  |  Gap: 152h  |  JPMorgan: async review board"),
    ("CAB Release Approval (Phase 6)",
     "High", "Speed",
     "88h WT/feature  |  $480K/yr",
     "Peer benchmark: 8h WT  |  Gap: 80h  |  Citigroup: AI-gated approval"),
    ("Peer Code Review Queue (Phase 4)",
     "High", "Productivity",
     "32h WT/feature  |  $175K/yr",
     "Peer benchmark: 12h WT  |  Gap: 20h  |  Commonwealth Bank: AI reviewer"),
    ("Test Environment Provisioning (Phase 5)",
     "Medium", "Productivity + Quality",
     "24h WT/feature  |  $130K/yr",
     "Peer benchmark: 1h WT  |  Gap: 23h  |  ANZ: on-demand ephemeral envs"),
]
for i, (name, sev, dims2, waste, bench) in enumerate(bottlenecks):
    y = 1.18 + i * 1.05
    sev_col = RGBColor(0xEF,0x44,0x44) if sev=="Critical" else (
              RGBColor(0xF9,0x73,0x16) if sev=="High" else BLUE)
    R(sl, 0.25, y, 0.12, 0.88, fill=sev_col)
    T(sl, name, 0.5, y+0.05, 4.2, 0.45, size=13, bold=True, color=TEXT)
    T(sl, f"Impact: {dims2}", 0.5, y+0.52, 2.5, 0.32, size=11, color=STEEL)
    T(sl, sev, 4.9, y+0.1, 1.2, 0.45, size=12, bold=True,
      color=sev_col, align=PP_ALIGN.CENTER)
    T(sl, waste, 6.25, y+0.1, 2.5, 0.45, size=13, bold=True,
      color=NAVY, align=PP_ALIGN.CENTER)
    T(sl, bench, 8.9, y+0.1, 4.1, 0.8, size=10.5, italic=True, color=STEEL, wrap=True)

R(sl, 0, 6.55, 13.33, 0.95, fill=NAVY)
T(sl, "Total identified waste:  $3.1M/yr  |  Fully recoverable with Options A–C below  "
      "|  Partial recovery in 90 days with Quick Wins",
  0.4, 6.6, 12.5, 0.85, size=12, bold=True, color=WHITE, wrap=True)


# ── Slide 6: The Three Transformation Options ─────────────────────────────────
sl = blank(deck)
R(sl, 0, 0, 13.33, 7.5, fill=WHITE)

# Full-width title
R(sl, 0, 0, 13.33, 0.7, fill=NAVY)
T(sl, "Phase 2: Design — Three AI Transformation Pathways",
  0.4, 0.08, 10, 0.4, size=20, bold=True, color=WHITE)
T(sl, "Choose the pathway that matches your risk appetite, investment capacity, and transformation ambition",
  0.4, 0.46, 12.5, 0.22, size=12, italic=True, color=LBLUE)

# Three option columns (full height)
OPT_W = 4.33
OPT_GAP = 0.02

option_col(sl, 0.0,     OPT_W, "OPTION A", "AI-AUGMENTED PDLC",
           ["AI copilots embedded in each phase",
            "Engineers use AI tools — humans decide",
            "No process redesign required",
            "Adoption in 30–60 days per phase",
            "Investment: $300K–$600K",
            "Effort reduction: 15–25% per phase",
            "DORA band improvement: +0.5 levels",
            "Good for: risk-averse orgs, regulated teams"],
           "Speed +25% · Productivity +20% · Quality +15%", OPT_A)

option_col(sl, OPT_W + OPT_GAP, OPT_W, "OPTION B ★", "AI AGENTS + HUMAN GATES",
           ["AI agents execute tasks; humans approve",
            "Decision gates at phase transitions",
            "40–60% effort reduction possible",
            "3–6 month process redesign required",
            "Investment: $1.2M–$2.0M",
            "ROI: 4–6×  |  Payback: 10–14 months",
            "DORA band improvement: +1.0–1.5 levels",
            "Good for: growth-focused, mid-risk orgs"],
           "Speed +55% · Productivity +50% · Quality +35%", OPT_B)

option_col(sl, (OPT_W + OPT_GAP)*2, OPT_W, "OPTION C", "FULLY AGENTIC PDLC",
           ["AI agents run PDLC end-to-end",
            "Humans set objectives; review exceptions",
            "70–80% effort reduction achieved",
            "Full operating model transformation",
            "Investment: $3M–$5M over 18 months",
            "ROI: 8–12×  |  Payback: 14–20 months",
            "DORA band improvement: +2.0 levels",
            "Good for: digital leaders, greenfield"],
           "Speed +75% · Productivity +75% · Quality +60%", OPT_C)

T(sl, "★ Option B is recommended for most Financial Services organisations — "
      "optimal risk-adjusted ROI, achievable within 12 months, board-approvable investment.",
  0.25, 7.18, 12.8, 0.3, size=11, italic=True, color=NAVY)


# ── Slide 7: Option A Detail ──────────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Option A: AI-Augmented PDLC — Human in the Loop",
    "AI enhances every engineer's capability without changing how your PDLC is governed")

T(sl, "Engineers use AI tools at every phase. Every decision stays with a human. "
      "No process redesign — just better tools doing more of the heavy lifting.",
  0.5, 1.15, 12.3, 0.45, size=13, italic=True, color=STEEL)

aug_phases = [
    ("Requirements",       "AI requirement quality scorer + gap analyser",          "24h → 18h PT",  "$280K/yr saved"),
    ("Design & Arch",      "AI architecture review assistant + risk flagging",       "176h → 90h WT", "$520K/yr saved"),
    ("Development",        "AI code copilot (GitHub Copilot / Cursor)",              "62h → 46h PT",  "$350K/yr saved"),
    ("Code Review",        "AI-assisted review: auto-flags issues before peer",      "32h → 18h WT",  "$175K/yr saved"),
    ("Continuous Testing", "AI test generation + prioritised test suite",            "240h → 160h WT","$480K/yr saved"),
    ("Deployment Prep",    "AI release note generator + risk classifier",            "88h → 60h WT",  "$168K/yr saved"),
    ("Release & Ops",      "AI incident correlator + run-book auto-generator",       "32h → 18h WT",  "$84K/yr saved"),
]
for i, (ph, tool, impact, saving) in enumerate(aug_phases):
    y = 1.72 + i * 0.66
    bg = GHOST if i % 2 == 0 else WHITE
    R(sl, 0.25, y, 12.8, 0.62, fill=bg)
    T(sl, ph,     0.35, y+0.08, 1.7,  0.45, size=11.5, bold=True, color=NAVY)
    T(sl, tool,   2.15, y+0.08, 4.5,  0.45, size=11,   color=TEXT)
    T(sl, impact, 6.75, y+0.08, 2.5,  0.45, size=11.5, bold=True, color=STEEL)
    T(sl, saving, 9.35, y+0.08, 3.5,  0.45, size=11.5, bold=True, color=NAVY)

R(sl, 0, 6.45, 13.33, 1.05, fill=OPT_A)
T(sl, "Option A Business Case:   Investment $350–600K   |   Annual Benefit $2.1M   |   "
      "ROI 2.5–3×   |   Payback 6–9 months   |   Risk: LOW",
  0.5, 6.5, 12.3, 0.95, size=13, bold=True, color=WHITE, wrap=True)


# ── Slide 8: Option B Detail ──────────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Option B: AI Agents with Human Gates — Human on the Loop ★",
    "AI executes tasks; engineered approval gates keep humans accountable — without slowing delivery")

T(sl, "AI agents handle the work. Humans set the standards, define the gates, and approve exceptions. "
      "The pipeline moves at AI speed — with human judgement at every critical decision point.",
  0.5, 1.15, 12.3, 0.45, size=13, italic=True, color=STEEL)

agents_b = [
    ("Requirements Agent",    "Auto-generates acceptance criteria, user stories, and DoD",    "Human gate: Product Owner approves before dev starts"),
    ("Architecture Agent",    "Automated risk scoring + dependency mapping + ADR draft",       "Human gate: Architect reviews flag list (not full doc)"),
    ("Development Agents",    "AI writes boilerplate; human engineers own logic + decisions",  "Human gate: Code review of AI-generated sections"),
    ("QA Agent",              "AI generates and runs full regression suite; raises defects",    "Human gate: Engineer validates Critical/High defects only"),
    ("Release Agent",         "AI assembles release package + change record + rollback plan",  "Human gate: Change Manager approves risk score > threshold"),
    ("Ops Agent",             "AI monitors, correlates incidents, auto-remediates known issues","Human gate: SRE reviews auto-remediation above P2"),
]
for i, (agent, action, gate) in enumerate(agents_b):
    y = 1.72 + i * 0.78
    R(sl, 0.25, y, 12.8, 0.72, fill=GHOST if i % 2 == 0 else WHITE)
    T(sl, agent,  0.35,  y+0.1,  2.4,  0.52, size=12,  bold=True, color=OPT_B)
    T(sl, action, 2.85,  y+0.1,  5.2,  0.52, size=11.5, color=TEXT, wrap=True)
    T(sl, gate,   8.15,  y+0.1,  4.7,  0.52, size=11,   italic=True, color=NAVY, wrap=True)

R(sl, 0, 6.45, 13.33, 1.05, fill=OPT_B)
T(sl, "Option B Business Case:   Investment $1.2–2.0M   |   Annual Benefit $5.5M   |   "
      "ROI 4.2×   |   Payback 10–14 months   |   5-Year NPV $31.2M   |   Risk: MEDIUM",
  0.5, 6.5, 12.3, 0.95, size=13, bold=True, color=WHITE, wrap=True)


# ── Slide 9: Option C Detail ──────────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Option C: Fully Agentic PDLC — Human Above the Loop",
    "Humans set strategy and define standards. AI agents own execution end-to-end.")

T(sl, "The fully agentic PDLC is not about removing humans — it's about repositioning them. "
      "Humans become product strategists, quality standard setters, and exception adjudicators. "
      "AI agents do everything else.",
  0.5, 1.15, 12.3, 0.52, size=13, italic=True, color=STEEL)

# Human above the loop model
R(sl, 0.25, 1.78, 12.8, 0.55, fill=NAVY)
T(sl, "HUMAN ROLE: Set objectives  |  Define quality standards  |  Adjudicate exceptions  |  "
      "Approve strategic decisions  |  Monitor via dashboard",
  0.4, 1.84, 12.5, 0.45, size=12, bold=True, color=WHITE)

agent_row = [
    ("Discovery\nAgent",     "Reads market, user research, competitor data\n→ Auto-generates PRDs"),
    ("Design\nAgent",        "Architecture options + trade-off analysis\n→ Selects optimal pattern"),
    ("Development\nAgents",  "Writes, reviews, and merges code\n→ Human owns product logic only"),
    ("QA\nAgent",            "Full test generation + execution + defect triage\n→ Zero manual regression"),
    ("Release\nAgent",       "Assembles, risk-scores, schedules, deploys\n→ Human approves P1 changes only"),
    ("Ops\nAgent",           "24/7 monitoring, auto-remediation, post-incident\n→ Human reviews weekly digest"),
]
for i, (agent, role) in enumerate(agent_row):
    x = 0.25 + i * 2.18
    R(sl, x, 2.43, 2.0, 1.5, fill=GHOST)
    R(sl, x, 2.43, 2.0, 0.42, fill=OPT_C)
    T(sl, agent, x, 2.43, 2.0, 0.42, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, role,  x+0.08, 2.9, 1.85, 0.98, size=10.5, color=TEXT, wrap=True)

# Outcomes
R(sl, 0.25, 4.1, 12.8, 0.35, fill=STEEL)
T(sl, "KEY OUTCOMES — OPTION C", 0.4, 4.13, 12.5, 0.3, size=12, bold=True, color=WHITE)

oc_stats = [
    ("75–80%", "Effort Reduction"),
    ("6 → 1 day", "Average Lead Time"),
    ("85–90%", "Flow Efficiency"),
    ("$8–12M/yr", "Annual Benefit"),
    ("8–12×", "ROI Multiple"),
    ("2.0 bands", "DORA Improvement"),
]
for i, (v, l) in enumerate(oc_stats):
    x = 0.25 + i * 2.18
    R(sl, x, 4.5, 2.0, 1.05, fill=OPT_C)
    T(sl, v, x, 4.57, 2.0, 0.52, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, l, x, 5.08, 2.0, 0.38, size=10, color=WHITE, align=PP_ALIGN.CENTER)

T(sl, "Prerequisite: Organisations pursuing Option C should have completed Option B or equivalent — "
      "agentic PDLC requires mature CI/CD, test automation ≥70%, and strong engineering governance.",
  0.25, 5.7, 12.8, 0.45, size=11, italic=True, color=NAVY)
R(sl, 0, 6.27, 13.33, 1.23, fill=OPT_C)
T(sl, "Option C Business Case:   Investment $3.0–5.0M   |   Annual Benefit $18–30M   |   "
      "ROI 8–12×   |   Payback 14–20 months   |   5-Year NPV $80–130M   |   Risk: MEDIUM-HIGH",
  0.5, 6.32, 12.3, 1.1, size=13, bold=True, color=WHITE, wrap=True)


# ── Slide 10: Business Case Comparison ───────────────────────────────────────
sl = blank(deck)
hdr(sl, "Business Case Comparison — Three Options",
    "Conservative to optimistic scenarios — same data, different transformation velocity")

T(sl, "All three options are modelled on your actual ALM data and DORA scores. "
      "Option B is recommended for most organisations — best risk-adjusted return.",
  0.5, 1.15, 12.3, 0.42, size=13, italic=True, color=STEEL)

# Header
for i, (lbl, col) in enumerate([("METRIC", NAVY),
                                  ("OPTION A\nAI-Augmented", OPT_A),
                                  ("OPTION B ★\nAgents + Gates", OPT_B),
                                  ("OPTION C\nFully Agentic", OPT_C)]):
    x = 0.25 + i * 3.27
    R(sl, x, 1.68, 3.1, 0.62, fill=col)
    T(sl, lbl, x, 1.68, 3.1, 0.62, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows = [
    ("Investment",           "$350–600K",        "$1.2–2.0M",         "$3.0–5.0M"),
    ("Annual Benefit",       "$2.1M",             "$5.5M",              "$18–30M"),
    ("ROI Multiple",         "2.5–3×",            "4–6×",               "8–12×"),
    ("Payback Period",       "6–9 months",        "10–14 months",       "14–20 months"),
    ("5-Year NPV",           "$9–11M",            "$28–35M",            "$80–130M"),
    ("Lead Time Reduction",  "25–35%",            "55–70%",             "75–85%"),
    ("Flow Efficiency",      "18% → 30%",         "18% → 55%",          "18% → 85%"),
    ("DORA Improvement",     "+0.5 bands",        "+1.0–1.5 bands",     "+2.0 bands"),
    ("Risk Level",           "LOW",               "MEDIUM",             "MEDIUM–HIGH"),
    ("Timeline to Full ROI", "6–9 months",        "12–18 months",       "24–36 months"),
]
for ri, (metric, a, b, c) in enumerate(rows):
    y = 2.35 + ri * 0.42
    bg = GHOST if ri % 2 == 0 else WHITE
    for ci, val in enumerate([metric, a, b, c]):
        x = 0.25 + ci * 3.27
        R(sl, x, y, 3.1, 0.4, fill=bg)
        fc = NAVY if ci == 0 else (OPT_A if ci == 1 else (OPT_B if ci == 2 else OPT_C))
        T(sl, val, x+0.1, y+0.04, 2.9, 0.32,
          size=11.5 if ci > 0 else 11,
          bold=(ci == 0),
          color=fc if ci > 0 else TEXT)

R(sl, 0, 6.72, 13.33, 0.78, fill=NAVY)
T(sl, "★ Option B Recommendation: $1.2–2.0M investment recovers $5.5M/yr — 4.2× ROI. "
      "Board-approvable in most FS organisations. Achievable within 12 months. "
      "Platform-accelerated design and tracking included.",
  0.4, 6.76, 12.5, 0.7, size=11.5, color=WHITE, wrap=True)


# ── Slide 11: Implementation Playbook Overview ────────────────────────────────
sl = blank(deck)
hdr(sl, "Implementation Playbook — Option B (Recommended)",
    "Week-by-week programme from business case approval to first Quick Win")

T(sl, "The playbook is generated by AI, grounded in your VSM data, and tracked live in the platform. "
      "Every action item has a named owner, effort estimate, and expected LT/FE improvement.",
  0.5, 1.15, 12.3, 0.42, size=13, italic=True, color=STEEL)

horizons = [
    (NAVY,  "QUICK WINS\n0–90 Days",
     "$350K investment → $1.4M/yr benefit",
     ["Deploy AI UAT Agent — eliminate 192h/feature testing queue",
      "Implement AI Architecture Review Board — reduce 152h gate to 24h async",
      "AI Release Risk Classifier — CAB approval automated for 85% of changes",
      "First VSM re-run: validate 10-day lead time reduction",
      "Expected: LT 42 → 32 days, FE 17% → 28%"]),
    (STEEL, "MEDIUM-TERM\n3–6 Months",
     "$600K investment → $2.1M/yr incremental",
     ["AI Development Agents — code review automation for boilerplate",
      "Requirements Agent — auto-generate acceptance criteria from PRDs",
      "Ops Agent — 24/7 monitoring + auto-remediation",
      "Process redesign: define human gates at phase boundaries",
      "Expected: LT 32 → 18 days, FE 28% → 45%"]),
    (BLUE,  "STRATEGIC\n6–12 Months",
     "$1.0M investment → $2.0M/yr incremental",
     ["Full agent orchestration across all 7 PDLC phases",
      "Human gate governance model: defined approval thresholds",
      "DORA maturity: WALK → RUN (score 2.1 → 3.5)",
      "Benefits realisation review vs. business case",
      "Expected: LT 18 → 8 days, FE 45% → 61%"]),
]
PBW = 4.05
for i, (col, label, invest, bullets) in enumerate(horizons):
    x = 0.22 + i * (PBW + 0.12)
    R(sl, x, 1.68, PBW, 0.75, fill=col)
    T(sl, label, x+0.14, 1.7, PBW-0.28, 0.48, size=15, bold=True, color=WHITE)
    T(sl, invest, x+0.14, 2.18, PBW-0.28, 0.22, size=10.5, color=LBLUE)
    R(sl, x, 2.43, PBW, 3.75, fill=GHOST)
    for j, b in enumerate(bullets):
        T(sl, f"• {b}", x+0.16, 2.52 + j*0.58, PBW-0.32, 0.54,
          size=11.5, color=TEXT, wrap=True)

R(sl, 0, 6.28, 13.33, 1.22, fill=NAVY)
T(sl, "Full playbook with week-by-week actions, owners, and expected metrics is generated automatically "
      "by the STUMP from your Jira data. No generic templates — every action is grounded in your actual bottleneck data.",
  0.4, 6.32, 12.5, 1.1, size=11.5, color=WHITE, wrap=True)


# ── Slide A: The New Engineering Operating Model ─────────────────────────────
sl = blank(deck)
hdr(sl, "The New Engineering Operating Model",
    "AI doesn't augment how engineers work — it restructures what engineering IS")

# 3-column layout
col_w = 4.0
col_gap = 0.22
labels = ["Current Model", "Transition", "AI-Native Model"]
col_colors = [STEEL, NAVY, BLUE]
col_x = [0.25, 0.25 + col_w + col_gap, 0.25 + (col_w + col_gap) * 2]

current_items = [
    "Humans write code, AI assists",
    "Sprints plan work",
    "Jira tracks tickets",
    "PR reviews gate quality",
    "QA teams verify",
]
transition_items = [
    "AI copilots → AI agents",
    "Batched sprints → continuous flow",
    "Tickets → spec-driven pipelines",
    "Manual review → AI-first review",
    "Manual QA → AI-assisted validation",
]
ainative_items = [
    "AI writes code, humans direct",
    "Continuous autonomous flow",
    "Specs trigger pipelines",
    "AI self-reviews with human gates",
    "AI validates, humans audit",
]
all_col_items = [current_items, transition_items, ainative_items]

for ci, (cx, col, lbl, items) in enumerate(zip(col_x, col_colors, labels, all_col_items)):
    R(sl, cx, 1.15, col_w, 0.52, fill=col)
    T(sl, lbl, cx, 1.15, col_w, 0.52, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    R(sl, cx, 1.67, col_w, 4.3, fill=GHOST if ci % 2 == 0 else PALE)
    for ji, item in enumerate(items):
        T(sl, f"• {item}", cx + 0.15, 1.78 + ji * 0.72, col_w - 0.3, 0.65,
          size=11, color=TEXT, wrap=True)

R(sl, 0, 6.12, 13.33, 0.78, fill=NAVY)
T(sl, "This is not a tool upgrade. It is an operating model transformation.",
  0.4, 6.2, 12.5, 0.62, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ── Slide B: Requirements Evolution ──────────────────────────────────────────
sl = blank(deck)
hdr(sl, "From User Stories to Machine-Readable Specs",
    "The way requirements are defined must change for AI-driven pipelines to work")

phases_req = [
    (STEEL, "Phase 1 (Today)", "User Stories in Jira",
     ["Product Owners write user stories",
      "Acceptance criteria informal or missing",
      "AI has no structured input to act on",
      "Stories interpreted differently by each engineer"]),
    (NAVY, "Phase 2 (Transition)", "Structured Specs + Jira",
     ["User stories supplemented with structured spec fields",
      "Acceptance criteria formalised in machine-readable format",
      "Jira becomes a hybrid — tickets + spec metadata",
      "AI can consume spec fields to assist code generation"]),
    (BLUE, "Phase 3 (AI-Native)", "Spec-Driven Development in Git",
     ["Specs define intent, constraints, and acceptance criteria",
      "AI generates code, tests, and docs from specs",
      "Pipeline triggers directly from spec commits",
      "Human reviews intent, not implementation"]),
]

PW_req = 4.0
for i, (col, phase_lbl, sub_lbl, bullets) in enumerate(phases_req):
    x = 0.25 + i * (PW_req + 0.22)
    R(sl, x, 1.15, PW_req, 0.6, fill=col)
    T(sl, phase_lbl, x + 0.12, 1.18, PW_req - 0.24, 0.28, size=12, bold=True, color=WHITE)
    T(sl, sub_lbl, x + 0.12, 1.46, PW_req - 0.24, 0.26, size=10,
      color=RGBColor(0xBF, 0xDB, 0xFE))
    R(sl, x, 1.75, PW_req, 4.3, fill=GHOST if i % 2 == 0 else PALE)
    for j, b in enumerate(bullets):
        T(sl, f"• {b}", x + 0.15, 1.86 + j * 0.75, PW_req - 0.3, 0.68,
          size=11, color=TEXT, wrap=True)
    if i < 2:
        T(sl, "▶", x + PW_req + 0.06, 3.2, 0.14, 0.38, size=16, bold=True, color=NAVY)

R(sl, 0, 6.12, 13.33, 0.78, fill=NAVY)
T(sl, "Key insight: Specs define intent, constraints, and acceptance criteria in machine-readable format — "
      "enabling AI to generate code, tests, and documentation autonomously.",
  0.4, 6.2, 12.5, 0.62, size=11, color=WHITE, wrap=True)


# ── Slide C: Tooling Evolution ────────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Tooling Evolution — What Stays, What Changes",
    "Not all current tools survive the transition to autonomous engineering")

# Table header
col_widths = [2.5, 3.0, 3.5, 2.4]
col_starts = [0.25, 2.75, 5.75, 9.25]
header_labels = ["Tool / Practice", "Current Role", "AI-Native Role", "Verdict"]
header_cols = [NAVY, STEEL, BLUE, NAVY]
for ci, (cx, cw, lbl, hcol) in enumerate(zip(col_starts, col_widths, header_labels, header_cols)):
    R(sl, cx, 1.15, cw, 0.48, fill=hcol)
    T(sl, lbl, cx + 0.08, 1.18, cw - 0.16, 0.42, size=11, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)

tool_rows = [
    ("Jira / ADO",          "Ticket tracking",                         "Intent registry or replaced by Git specs",        "Evolves"),
    ("Git / GitHub",        "Code repository",                         "Source of truth: specs + code + config",          "Stays"),
    ("CI/CD Pipelines",     "Build + deploy",                          "Spec-triggered autonomous delivery",              "Stays + Expands"),
    ("Sprint Planning",     "Work allocation",                         "Exception handling + goal setting",               "Transforms"),
    ("Code Review",         "Quality gate",                            "AI-first + human exception review",               "Transforms"),
    ("Test Automation",     "Coverage",                                "AI-generated full regression suite",             "Stays + Expands"),
    ("Architecture Docs",   "Static documentation",                    "Living AI-maintained specs",                      "Transforms"),
]
verdict_colors = {
    "Stays": BLUE,
    "Stays + Expands": BLUE,
    "Evolves": STEEL,
    "Transforms": OPT_A,
}
for ri, (tool, current, ainative, verdict) in enumerate(tool_rows):
    y = 1.68 + ri * 0.58
    bg = GHOST if ri % 2 == 0 else WHITE
    row_vals = [tool, current, ainative, verdict]
    for ci, (cx, cw, val) in enumerate(zip(col_starts, col_widths, row_vals)):
        R(sl, cx, y, cw, 0.54, fill=bg)
        fc = verdict_colors.get(val, TEXT) if ci == 3 else (NAVY if ci == 0 else TEXT)
        bold = ci in (0, 3)
        T(sl, val, cx + 0.08, y + 0.08, cw - 0.16, 0.38, size=10,
          bold=bold, color=fc, wrap=True)

R(sl, 0, 6.62, 13.33, 0.78, fill=NAVY)
T(sl, "The shift is from human-operated toolchains to AI-orchestrated delivery systems.",
  0.4, 6.7, 12.5, 0.62, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ── Slide D: Agile in the Age of Autonomous Delivery ─────────────────────────
sl = blank(deck)
hdr(sl, "Do Sprints Still Make Sense?",
    "Agile was designed for human teams. Autonomous delivery needs a different rhythm.")

# 2-column layout
R(sl, 0.25, 1.15, 6.2, 0.42, fill=STEEL)
T(sl, "Why Agile Was Designed This Way", 0.35, 1.19, 6.0, 0.34, size=12, bold=True, color=WHITE)
R(sl, 6.7, 1.15, 6.2, 0.42, fill=BLUE)
T(sl, "What Changes With AI", 6.8, 1.19, 6.0, 0.34, size=12, bold=True, color=WHITE)

agile_left = [
    "Human coordination required explicit synchronisation",
    "Time-boxing created focus and forced prioritisation",
    "Ceremonies aligned distributed teams on goals",
    "2-week cadence matched human cognitive load and planning horizon",
    "Retrospectives enabled continuous learning for human teams",
]
agile_right = [
    "AI doesn't need coordination ceremonies",
    "Delivery becomes continuous — not batched",
    "Human role shifts to goal-setting and exception review",
    "Cadence becomes event-driven, not calendar-driven",
    "AI learns continuously — retrospectives become automated telemetry",
]
for j, (left, right) in enumerate(zip(agile_left, agile_right)):
    y = 1.65 + j * 0.52
    R(sl, 0.25, y, 6.2, 0.48, fill=GHOST if j % 2 == 0 else WHITE)
    T(sl, f"• {left}", 0.38, y + 0.07, 6.0, 0.38, size=10.5, color=TEXT, wrap=True)
    R(sl, 6.7, y, 6.2, 0.48, fill=PALE if j % 2 == 0 else WHITE)
    T(sl, f"• {right}", 6.83, y + 0.07, 6.0, 0.38, size=10.5, color=TEXT, wrap=True)

R(sl, 0.25, 4.32, 12.8, 0.38, fill=NAVY)
T(sl, "WHAT REPLACES SPRINTS", 0.38, 4.36, 12.5, 0.3, size=11, bold=True, color=WHITE)

replacements = [
    ("Outcome-based goals\n(quarterly)", STEEL),
    ("Continuous autonomous\ndelivery", BLUE),
    ("Exception-triggered\nhuman reviews", NAVY),
    ("Weekly strategic steering\n(not planning)", OPT_A),
]
for i, (lbl, col) in enumerate(replacements):
    rx = 0.25 + i * 3.28
    R(sl, rx, 4.75, 3.1, 1.0, fill=col)
    T(sl, lbl, rx + 0.1, 4.82, 2.9, 0.88, size=11, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)

R(sl, 0, 5.9, 13.33, 0.9, fill=GHOST)
T(sl, "SAFe / PI Planning evolves to Transformation Portfolio Reviews — "
      "quarterly, outcome-focused, AI-progress reviewed by senior leaders rather than planning teams.",
  0.4, 5.97, 12.5, 0.76, size=11, italic=True, color=NAVY, wrap=True)


# ── Slide E: Scaling from Isolated Success to Enterprise ─────────────────────
sl = blank(deck)
hdr(sl, "The Real Challenge: From 3 Teams to 30",
    "AI success in isolated teams is not the same as enterprise-wide transformation")

challenges = [
    (NAVY, "1. Consistency",
     "Teams build own agents and templates in isolation — no shared standards.",
     "Centralised AI agent catalogue. Shared guardrail framework. Enterprise-wide prompt governance."),
    (STEEL, "2. Governance",
     "Each team defines its own AI rules — leading to conflicting policies and unmanaged risk.",
     "Enterprise AI policy layer, configurable per team. Immutable audit log across all 30+ teams."),
    (BLUE, "3. Skills",
     "AI capability concentrated in a few engineers — the rest are locked out or left behind.",
     "AI literacy programme for all engineers. Citizen-developer enablement. No-code agent builder."),
    (OPT_A, "4. Measurement",
     "No common baseline across teams — impossible to compare progress or aggregate ROI.",
     "Portfolio-level VSM. DORA metrics aggregated across all 30+ teams. Single executive dashboard."),
]

for i, (col, title, problem, solution) in enumerate(challenges):
    y = 1.15 + i * 1.3
    R(sl, 0.25, y, 12.8, 1.2, fill=GHOST if i % 2 == 0 else WHITE)
    R(sl, 0.25, y, 2.2, 1.2, fill=col)
    T(sl, title, 0.3, y + 0.38, 2.1, 0.44, size=12, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, f"Challenge: {problem}",
      2.55, y + 0.08, 4.8, 0.52, size=10.5, italic=True,
      color=RGBColor(0x6B, 0x72, 0x80), wrap=True)
    T(sl, f"Solution: {solution}",
      2.55, y + 0.62, 4.8, 0.52, size=10.5, color=NAVY, wrap=True)
    R(sl, 7.55, y + 0.12, 5.2, 0.96, fill=PALE)
    # solution repeated on right as visual call-out
    T(sl, solution, 7.68, y + 0.18, 4.94, 0.82, size=10, color=NAVY, italic=True, wrap=True)

R(sl, 0, 6.42, 13.33, 0.88, fill=NAVY)
T(sl, "Standardisation without stifling. Governance without bureaucracy.",
  0.4, 6.5, 12.5, 0.72, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ── Slide F: Code Quality, QA & Human Accountability ─────────────────────────
sl = blank(deck)
hdr(sl, "Autonomous Code. Accountable Humans.",
    "Fully autonomous, unchecked code is not acceptable — especially in regulated environments")

domains = [
    (STEEL, "Code Review",
     "AI writes, AI reviews (static analysis + semantic). Human reviews flagged risk items only.",
     "Human gate: approves before merge when risk score > threshold"),
    (BLUE, "QA & Testing",
     "AI generates full regression suite, runs on every commit, AI triages failures. Human reviews P1/P2 defects.",
     "Gate: zero P1s before production deploy"),
    (NAVY, "Architecture Standards",
     "AI checks every PR against Architecture Decision Records (ADRs). Violations flagged automatically.",
     "Architect reviews violations only — not every PR"),
    (OPT_A, "Human Accountability",
     "Named human owner per AI agent. Full audit trail. Override capability always on.",
     "Board-reportable governance artefacts produced automatically"),
]

for i, (col, domain, detail, gate) in enumerate(domains):
    y = 1.15 + i * 1.25
    R(sl, 0.25, y, 12.8, 1.15, fill=GHOST if i % 2 == 0 else WHITE)
    R(sl, 0.25, y, 2.0, 1.15, fill=col)
    T(sl, domain, 0.3, y + 0.35, 1.9, 0.46, size=12, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, detail, 2.38, y + 0.08, 6.2, 0.54, size=10.5, color=TEXT, wrap=True)
    R(sl, 8.72, y + 0.1, 4.1, 0.95, fill=PALE)
    T(sl, f"Gate: {gate}", 8.84, y + 0.2, 3.88, 0.7, size=10.5,
      bold=True, color=NAVY, italic=True, wrap=True)

R(sl, 0, 6.22, 13.33, 1.08, fill=NAVY)
T(sl, "Option B's gate model is designed to meet FSI audit requirements. "
      "Every AI action is logged, traceable, and reversible.",
  0.4, 6.3, 12.5, 0.88, size=11.5, color=WHITE, wrap=True)


# ── Slide G: Brownfield Strategy ─────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "The Legacy Question: You Can't Ignore It",
    "Most organisations have 10–20 years of code that cannot be rewritten. AI must work with what exists.")

steps_brown = [
    (NAVY, "1. Inventory & Score",
     "Knowledge Graph readiness assessment per application — measuring coupling, testability, "
     "API surface area, and documentation quality. Produces a modernisation-readiness score for every app."),
    (STEEL, "2. Classify",
     "Replatform (cloud-ready, minimal change)  |  Reengineer (modernise for AI pipeline compatibility)  "
     "|  Decompose (strangler-fig into microservices)  |  Maintain (stable, low-value, AI-assisted only)"),
    (BLUE, "3. Prioritise",
     "Start with highest-value, lowest-coupling applications — quick AI wins without legacy risk. "
     "Avoid the temptation to start with the biggest, most complex system first."),
    (OPT_A, "4. Progressively Modernise",
     "AI-assisted reverse engineering generates specs from existing code. New features added via "
     "spec-driven development. Old code progressively replaced — one service, one module at a time."),
]

for i, (col, step_lbl, desc) in enumerate(steps_brown):
    y = 1.15 + i * 1.22
    R(sl, 0.25, y, 12.8, 1.12, fill=GHOST if i % 2 == 0 else WHITE)
    R(sl, 0.25, y, 1.9, 1.12, fill=col)
    T(sl, step_lbl, 0.3, y + 0.32, 1.8, 0.48, size=11, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, desc, 2.28, y + 0.12, 10.6, 0.88, size=11, color=TEXT, wrap=True)

R(sl, 0, 6.06, 13.33, 0.88, fill=NAVY)
T(sl, "The goal is not to rewrite legacy. It is to make it AI-compatible — "
      "one service, one module at a time.",
  0.4, 6.14, 12.5, 0.72, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ── Slide H: Industry Precedents ─────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Industry Precedents — What Large-Scale Looks Like",
    "AI-driven engineering at scale is not theoretical — it is happening now")

T(sl, "The following examples illustrate how large organisations are approaching AI-native engineering "
      "transformation — and what they are learning.",
  0.4, 1.15, 12.5, 0.42, size=12, italic=True, color=STEEL, wrap=True)

evidence_cards = [
    (NAVY, "Global Bank (10,000+ Engineers)",
     "Deployed AI code generation across 200 teams. Lead time reduced 40%.",
     "Governance framework needed BEFORE rollout, not after. Teams without guardrails produced unreviewable code at scale."),
    (STEEL, "Tier-1 Insurance Group",
     "Spec-driven development piloted in 3 teams, now scaling to 40 teams.",
     "Jira replaced by Git-based spec registry for AI-facing teams. Human stories retained for stakeholder communication only."),
    (BLUE, "Payments Platform (FinTech)",
     "Fully autonomous testing pipeline. 94% test coverage with zero manual test writers.",
     "QA team redeployed to exploratory and adversarial testing — higher-value work that AI cannot replicate."),
    (OPT_A, "Retail Bank (Australia)",
     "Legacy modernisation using AI reverse-engineering.",
     "40% of 15-year-old monolith decomposed into microservices in 12 months using AI-generated specs from existing code."),
]

for i, (col, org, headline, learning) in enumerate(evidence_cards):
    y = 1.65 + i * 1.15
    R(sl, 0.25, y, 12.8, 1.05, fill=GHOST if i % 2 == 0 else WHITE)
    R(sl, 0.25, y, 1.8, 1.05, fill=col)
    T(sl, org, 0.32, y + 0.2, 1.66, 0.65, size=10, bold=True,
      color=WHITE, align=PP_ALIGN.CENTER, wrap=True)
    T(sl, headline, 2.18, y + 0.08, 5.2, 0.42, size=11, bold=True, color=NAVY, wrap=True)
    T(sl, f"Key learning: {learning}", 2.18, y + 0.52, 10.6, 0.46,
      size=10.5, italic=True, color=TEXT, wrap=True)

R(sl, 0, 6.28, 13.33, 0.92, fill=NAVY)
T(sl, "Pattern: Organisations that standardise FIRST, then automate, consistently outperform "
      "those that automate first.",
  0.4, 6.36, 12.5, 0.76, size=12, bold=True, color=WHITE, wrap=True)


# ── Slide I: Reimagining Risk Intelligence Engineering ────────────────────────
sl = blank(deck)
hdr(sl, "More Outcomes. Same Investment.",
    "How AI transforms the Risk Intelligence engineering function specifically")

# Left and right panels
R(sl, 0.25, 1.15, 6.2, 0.42, fill=STEEL)
T(sl, "Current State Challenges", 0.35, 1.19, 6.0, 0.34, size=12, bold=True, color=WHITE)
R(sl, 6.7, 1.15, 6.2, 0.42, fill=BLUE)
T(sl, "AI-Enabled State Outcomes", 6.8, 1.19, 6.0, 0.34, size=12, bold=True, color=WHITE)

current_challenges = [
    "Manual data pipeline maintenance consumes significant engineer capacity",
    "High toil in compliance reporting — repeated, low-value manual work",
    "Slow feature delivery due to risk and compliance overhead at every gate",
    "QA bottlenecks on regulated code — each change requires manual sign-off",
    "Talent cost pressure — scarce specialist engineers doing commodity work",
]
ai_outcomes = [
    "AI-maintained data pipelines — self-healing, self-documenting",
    "Automated compliance evidence generation — audit-ready continuously",
    "AI-first delivery with built-in regulatory gates — faster and safer",
    "AI-generated test suites for regulated code — zero manual regression",
    "Same outcomes with optimised team structure — specialists on high-value work",
]
for j, (ch, out) in enumerate(zip(current_challenges, ai_outcomes)):
    y = 1.65 + j * 0.52
    R(sl, 0.25, y, 6.2, 0.48, fill=GHOST if j % 2 == 0 else WHITE)
    T(sl, f"• {ch}", 0.38, y + 0.07, 6.0, 0.38, size=10.5, color=TEXT, wrap=True)
    R(sl, 6.7, y, 6.2, 0.48, fill=PALE if j % 2 == 0 else WHITE)
    T(sl, f"• {out}", 6.83, y + 0.07, 6.0, 0.38, size=10.5, color=TEXT, wrap=True)

# 3 financial levers
R(sl, 0.25, 4.38, 12.8, 0.38, fill=NAVY)
T(sl, "THREE FINANCIAL LEVERS", 0.38, 4.42, 12.5, 0.3, size=11, bold=True, color=WHITE)

levers = [
    (STEEL, "Capacity Release",
     "30–40% of engineer time currently spent on toil → redirected to value-add features"),
    (BLUE, "Velocity",
     "2–4× throughput increase → more risk products shipped per quarter"),
    (NAVY, "Quality",
     "AI-enforced standards → fewer production incidents, lower remediation cost"),
]
for i, (col, lev_lbl, lev_desc) in enumerate(levers):
    lx = 0.25 + i * 4.3
    R(sl, lx, 4.82, 4.1, 1.05, fill=col)
    T(sl, lev_lbl, lx + 0.12, 4.88, 3.86, 0.34, size=13, bold=True, color=WHITE)
    T(sl, lev_desc, lx + 0.12, 5.24, 3.86, 0.58, size=10.5, color=WHITE, wrap=True)

R(sl, 0, 6.02, 13.33, 0.88, fill=NAVY)
T(sl, "The question is not whether to transform. It is whether to lead the transformation or respond to it.",
  0.4, 6.1, 12.5, 0.72, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ── Slide 12b: STUMP — New Module Capabilities ──────────────────────────────
sl = blank(deck)
hdr(sl, "STUMP — 21 Modules Across 7 Capability Groups",
    "Five new capabilities address the full transformation lifecycle: Legacy, Operations, Governance, AI Assurance & Readiness")

T(sl, "STUMP's 21-module platform covers every dimension of an AI-powered engineering transformation — "
      "from initial diagnosis through to continuous governance and legacy modernisation.",
  0.5, 1.15, 12.3, 0.42, size=13, italic=True, color=STEEL)

new_modules = [
    ("Legacy Modernisation", OPT_A,
     "Knowledge Graph readiness scoring for all legacy applications. Per-system modernisation strategy: replatform, reengineer, or decompose. Integrated into transformation roadmap so brownfield complexity is never a transformation blocker.",
     "Phase 1 Diagnose"),
    ("Operations Intelligence", OPT_B,
     "AIOps maturity model (Reactive → Proactive → Predictive → Autonomous). Live operations metrics: MTTR, MTTD, auto-resolution rate, alert noise ratio. Phase 7 (Production & Operations) deep-dive activities.",
     "Phase 1 Diagnose / Phase 3 Deliver"),
    ("Transformation Readiness", OPT_B,
     "5-dimension readiness assessment (culture, process, technology, data, governance). Role evolution mapping — current → AI-augmented → autonomous for all 7 PDLC phases. Change management plan with effort/duration/headcount estimates.",
     "Phase 2 Design"),
    ("Governance & Guardrails", OPT_C,
     "Agent accountability matrix (8 agents, named human owners, risk tiers). Configurable guardrail toggles by category (data privacy, PII, financial impact, regulatory). Immutable audit log. Responsible AI Scorecard.",
     "Phase 2 Design / Phase 3 Deliver"),
    ("AI Assurance", OPT_C,
     "6-gate validation per agent output: hallucination detection, citation accuracy, bias monitoring, drift detection, output quality scoring, CI/CD gate integration. For FSI: artefact set maps to DORA Articles 28–44.",
     "Phase 2 Design / Phase 3 Deliver"),
]
for i, (name, col, desc, phase) in enumerate(new_modules):
    y = 1.72 + i * 0.95
    R(sl, 0.25, y, 12.8, 0.88, fill=GHOST if i % 2 == 0 else WHITE)
    R(sl, 0.25, y, 2.3, 0.88, fill=col)
    T(sl, name, 0.3, y+0.2, 2.2, 0.5, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER, wrap=True)
    T(sl, desc, 2.65, y+0.08, 8.4, 0.72, size=10.5, color=TEXT, wrap=True)
    T(sl, phase, 11.15, y+0.28, 1.9, 0.32, size=10, italic=True, color=STEEL, align=PP_ALIGN.CENTER)

R(sl, 0, 6.72, 13.33, 0.78, fill=NAVY)
T(sl, "These 5 modules address the #1 reasons AI transformation programmes fail: "
      "ungoverned autonomy, legacy lock-in, unprepared organisations, and unvalidated AI outputs.",
  0.4, 6.76, 12.5, 0.7, size=12, color=WHITE, wrap=True)


# ── Slide 12: Platform as Accelerator ────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Why the STUMP Transforms the Offering",
    "5× faster, AI-accurate, lower cost — the platform makes the consulting offering possible at this speed")

T(sl, "Without the platform, this engagement looks like any other consulting project — "
      "expensive, slow, and gone when the consultants leave. "
      "The platform makes it permanent, continuous, and self-improving.",
  0.5, 1.15, 12.3, 0.52, size=13, italic=True, color=STEEL)

comparisons = [
    ("DIAGNOSIS",
     "Traditional: 3–6 months, $500K–$1M in consulting fees, manual spreadsheet analysis",
     "With Platform: 2 weeks, included in pilot fee, AI-generated from your live ALM data"),
    ("OPTION DESIGN",
     "Traditional: 4–8 weeks of workshops, 200-slide options paper, subjective ROI estimates",
     "With Platform: 3 weeks, AI models all 3 options against your actual data, auditable evidence"),
    ("IMPLEMENTATION",
     "Traditional: Consultants leave after readout; no live tracking; benefits drift",
     "With Platform: Always-on VSM dashboard; real-time FE and LT tracking; AI detects new bottlenecks"),
    ("BENEFITS REALISATION",
     "Traditional: Annual review project, manual comparison to baseline, no continuous evidence",
     "With Platform: Automated monthly ROI report; board-ready from the platform in minutes"),
]
for i, (phase, trad, plat) in enumerate(comparisons):
    y = 1.82 + i * 1.2
    R(sl, 0.25, y, 12.8, 1.12, fill=GHOST if i % 2 == 0 else WHITE)
    R(sl, 0.25, y, 1.7, 1.12, fill=NAVY)
    T(sl, phase, 0.3, y+0.28, 1.6, 0.55, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, f"Traditional: {trad}",
      2.1, y+0.06, 5.0, 0.5, size=11, italic=True,
      color=RGBColor(0x6B,0x72,0x80), wrap=True)
    T(sl, f"✓  Platform: {plat}",
      2.1, y+0.58, 5.0, 0.5, size=11.5, bold=False,
      color=NAVY, wrap=True)
    T(sl, "5× faster", 7.3, y+0.08, 2.4, 0.45, size=16, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    T(sl, "vs. traditional", 7.3, y+0.55, 2.4, 0.3, size=10.5, color=STEEL, align=PP_ALIGN.CENTER)


# ── Slide 13: Proof — US Bank Case Study ─────────────────────────────────────
sl = blank(deck)
hdr(sl, "Proof of Concept — US Bank / Team Phoenix",
    "Financial Services  |  Option B engagement  |  8-week pilot → 12-month programme")

T(sl, "Starting from the same 42-day lead time and 17.8% flow efficiency that your data currently shows.",
  0.5, 1.15, 12.3, 0.38, size=13, italic=True, color=STEEL)

for i, (v, l, bg) in enumerate([
    ("42 → 8 days", "Lead Time", OPT_A),
    ("17.8% → 61%", "Flow Efficiency", STEEL),
    ("$3M", "Platform Investment", OPT_B),
    ("$8.4M/yr", "Annual Benefits", NAVY),
    ("4.2×", "ROI (Option B)", OPT_B),
    ("14 months", "Payback Period", STEEL),
]):
    stat(sl, 0.3 + i*2.18, 1.7, 2.0, 1.45, v, l, bg, value_size=18)

timeline = [
    ("Weeks 1–2",  "Platform deployed on US Bank infra. ALM connector loaded 2,847 tickets. VSM generated in 6 minutes."),
    ("Weeks 3–4",  "DORA assessment: 73 questions across 4 sources. Band: WALK (2.1/5.0). 5 bottlenecks identified."),
    ("Weeks 5–6",  "Option B selected. Business case approved by CFO. Quick Wins programme kicked off."),
    ("Weeks 7–8",  "AI UAT Agent deployed. First month: testing queue reduced from 240h to 96h per feature."),
    ("Month 3",    "Architecture Review Agent live. LT: 42 → 28 days. Quick Win 2 (CAB AI) in deployment."),
    ("Month 6",    "All Quick Wins complete. LT: 28 → 18 days. FE: 17.8% → 38%. Phase 2 agents starting."),
    ("Month 12",   "Full Option B complete. LT: 8 days. FE: 61%. ROI: 4.2×. Board presentation delivered."),
]
for i, (t, detail) in enumerate(timeline):
    y = 3.3 + i * 0.55
    R(sl, 0.25, y, 1.45, 0.48, fill=NAVY if i < 2 else (STEEL if i < 5 else BLUE))
    T(sl, t, 0.28, y+0.06, 1.39, 0.38, size=10.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, detail, 1.82, y+0.06, 11.0, 0.4, size=11, color=TEXT, wrap=True)


# ── Slide 14: Commercial Model ────────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Commercial Model", "Outcome-linked pricing — we share the risk")

T(sl, "Our engagement model is structured so that we only succeed when you succeed. "
      "The pilot is fixed-fee with a savings guarantee.",
  0.5, 1.15, 12.3, 0.42, size=13, italic=True, color=STEEL)

for i, (phase, fee, what, guarantee) in enumerate([
    ("Phase 1\nPilot",
     "$150,000\n(fixed fee)",
     "8-week engagement: VSM, DORA, Top 5 Bottlenecks, Business Case (3 options), Playbook, Executive Readout",
     "Full refund if we don't identify ≥ $500K annual savings"),
    ("Phase 2\nQuick Wins\nProgramme",
     "$300–600K\n(fixed fee)",
     "90-day Quick Wins implementation: 3 AI agent deployments, process redesign, first ROI realisation report",
     "Milestone-linked: 50% paid on delivery, 50% on measured LT reduction ≥ 15%"),
    ("Phase 3\nScale\nProgramme",
     "$600K–1.4M\n(outcome-linked)",
     "6–12 month programme: full Option B/C implementation, governance, training, benefits tracking",
     "30% of fee at-risk and tied to measured ROI vs. business case"),
]):
    y = 1.7 + i * 1.62
    R(sl, 0.22, y, 2.0, 1.5, fill=NAVY)
    T(sl, phase, 0.25, y+0.22, 1.94, 0.9, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    R(sl, 2.25, y, 2.4, 1.5, fill=BLUE)
    T(sl, fee, 2.28, y+0.28, 2.34, 0.9, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    R(sl, 4.68, y, 5.5, 1.5, fill=GHOST)
    T(sl, what, 4.8, y+0.08, 5.25, 1.32, size=11.5, color=TEXT, wrap=True)
    R(sl, 10.2, y, 2.88, 1.5, fill=PALE)
    T(sl, f"Guarantee: {guarantee}", 10.3, y+0.08, 2.65, 1.32, size=11, italic=True, color=NAVY, wrap=True)

R(sl, 0, 6.66, 13.33, 0.84, fill=NAVY)
T(sl, "Total Programme (Phase 1–3, Option B):  $1.2–2.2M investment  →  $5.5M annual benefit  →  "
      "4.2× ROI  →  14-month payback  →  $31.2M 5-year NPV",
  0.4, 6.7, 12.5, 0.76, size=12.5, bold=True, color=WHITE, wrap=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2026 ENHANCEMENT CLUSTER — Target State Studio, L1–L5 ladder, DORA J-Curve ROI,
# 3-perspective Outcome Dashboard. Mirrors the refreshed STUMP platform.
# ══════════════════════════════════════════════════════════════════════════════

# ── New Slide: L1–L5 Interim Maturity Ladder (A/B/C mapped) ──────────────────
sl = blank(deck)
hdr(sl, "The L1–L5 Interim Maturity Ladder", "Prompting → orchestration · the legacy Options A / B / C map onto the ladder")
LW = (13.33 - 0.5*2 - 0.12*4) / 5
for i, lv in enumerate(M.LADDER):
    x = 0.5 + i * (LW + 0.12)
    col = [STEEL, OPT_A, BLUE, OPT_B, NAVY][i]
    R(sl, x, 1.2, LW, 0.66, fill=col)
    T(sl, f"{lv['level']} · {lv['name']}", x+0.06, 1.24, LW-0.12, 0.58, size=10, bold=True, color=WHITE, wrap=True)
    R(sl, x, 1.86, LW, 3.5, fill=GHOST)
    T(sl, lv["ml"], x+0.08, 1.92, LW-0.16, 0.3, size=8.5, bold=True, color=STEEL)
    T(sl, lv["summary"], x+0.08, 2.24, LW-0.16, 1.8, size=8.8, color=TEXT, wrap=True)
    T(sl, f"Agents: {lv['agent_role']}\nHITL: {lv['hitl']}\nAutomation: {lv['automation']}",
      x+0.08, 4.05, LW-0.16, 0.8, size=8.5, color=STEEL)
    R(sl, x, 5.0, LW, 0.36, fill=col)
    T(sl, lv["option"], x+0.06, 5.03, LW-0.12, 0.32, size=8, bold=True, color=WHITE, wrap=True)
R(sl, 0, 5.7, 13.33, 1.1, fill=NAVY)
T(sl, "Current state is auto-derived from your VSM (e.g. L0–L1). You choose the North-Star level (often L4–L5) and "
      "how to get there — in one move, or via 1–2 interim steps sized to your maturity and risk appetite.",
  0.5, 5.8, 12.4, 0.9, size=12, color=WHITE, wrap=True)

# ── New Slide: Target State Studio + Platform Choice ─────────────────────────
sl = blank(deck)
hdr(sl, "Target State Studio — Define It, Then Choose How to Build It",
    "North-Star + delivery platform → auto-generated interim roadmap, operating model & business case")
T(sl, "Pick the delivery platform for your target ADLC. Home-grown is the US Bank target baseline; "
      "COTS and service-provider options overlay their own agents, tooling, economics and timeline.",
  0.5, 1.15, 12.3, 0.55, size=12.5, italic=True, color=STEEL, wrap=True)
PFW = (13.33 - 0.4*2 - 0.12*2) / 3
for i, pf in enumerate(M.PLATFORMS):
    x = 0.4 + (i % 3) * (PFW + 0.12)
    y = 1.85 + (i // 3) * 2.45
    kindcol = {"Home-grown": NAVY, "COTS": BLUE, "Service provider": STEEL}.get(pf["kind"], STEEL)
    R(sl, x, y, PFW, 0.5, fill=kindcol)
    T(sl, pf["name"], x+0.1, y+0.04, PFW-0.6, 0.42, size=11, bold=True, color=WHITE, wrap=True)
    T(sl, pf["kind"], x+PFW-0.95, y+0.06, 0.9, 0.36, size=8, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
    R(sl, x, y+0.5, PFW, 1.8, fill=GHOST)
    T(sl, pf["note"], x+0.1, y+0.56, PFW-0.2, 0.8, size=9, color=TEXT, wrap=True)
    T(sl, f"+ {pf['pros']}", x+0.1, y+1.32, PFW-0.2, 0.45, size=8.5, color=BLUE, wrap=True)
    T(sl, f"– {pf['cons']}", x+0.1, y+1.74, PFW-0.2, 0.5, size=8.5, color=STEEL, wrap=True)

# ── New Slide: DORA J-Curve ROI (cost-only) ──────────────────────────────────
sl = blank(deck)
hdr(sl, "The Business Case — DORA J-Curve ROI (cost-only)",
    "Investment → tuition-cost dip → breakeven → compounding savings. Excludes feature revenue.")
for i, (ph, desc) in enumerate(M.JCURVE["phases"]):
    x = 0.4 + i * 3.18
    col = [STEEL, RGBColor(0x64,0x74,0x8B), BLUE, NAVY][i]
    R(sl, x, 1.25, 3.0, 0.55, fill=col)
    T(sl, ph, x+0.1, 1.3, 2.8, 0.46, size=11.5, bold=True, color=WHITE, wrap=True)
    R(sl, x, 1.8, 3.0, 2.0, fill=GHOST)
    T(sl, desc, x+0.1, 1.88, 2.8, 1.85, size=10, color=TEXT, wrap=True)
    if i < 3:
        T(sl, "▶", x+3.02, 2.5, 0.14, 0.4, size=18, bold=True, color=NAVY)
R(sl, 0.4, 4.05, 12.5, 0.95, fill=PALE)
T(sl, "Ongoing cost is platform-aware and INCLUDES agent/token spend:  " + M.JCURVE["ongoing_note"].split(": ", 1)[1],
  0.5, 4.12, 12.3, 0.85, size=10.5, color=TEXT, wrap=True)
R(sl, 0, 5.2, 13.33, 1.0, fill=NAVY)
T(sl, M.JCURVE["roi_formula"] + "\n" + M.JCURVE["exclusion"],
  0.5, 5.3, 12.4, 0.85, size=11, bold=True, color=WHITE, wrap=True)
T(sl, M.JCURVE["dora_defaults"] + "  Editable per engagement.",
  0.5, 6.35, 12.4, 0.5, size=10, italic=True, color=STEEL, wrap=True)

# ── New Slide: 3-Perspective Outcome Dashboard ───────────────────────────────
sl = blank(deck)
hdr(sl, "Always-On Measurement — The Outcome Dashboard",
    "Three monitoring perspectives, computed from live data with per-chart inferences")
PVW2 = (13.33 - 0.4*2 - 0.12*2) / 3
for i, p in enumerate(M.OUTCOME_PERSPECTIVES):
    x = 0.4 + i * (PVW2 + 0.12)
    col = [NAVY, BLUE, STEEL][i]
    R(sl, x, 1.2, PVW2, 0.6, fill=col)
    T(sl, p["name"], x+0.1, 1.26, PVW2-0.2, 0.5, size=13, bold=True, color=WHITE, wrap=True)
    R(sl, x, 1.8, PVW2, 3.6, fill=GHOST)
    T(sl, p["blurb"], x+0.1, 1.88, PVW2-0.2, 0.7, size=10, italic=True, color=STEEL, wrap=True)
    for j, mtr in enumerate(p["metrics"]):
        T(sl, f"• {mtr}", x+0.12, 2.6 + j*0.34, PVW2-0.24, 0.32, size=9.5, color=TEXT, wrap=True)
R(sl, 0, 5.65, 13.33, 1.15, fill=NAVY)
T(sl, M.OUTCOME_SOURCES, 0.5, 5.75, 12.4, 0.95, size=11, color=WHITE, wrap=True)


# ── Slide 15: Next Steps ──────────────────────────────────────────────────────
sl = blank(deck)
hdr(sl, "Recommended Next Steps",
    "From this meeting to your first VSM dashboard in 2 weeks")

T(sl, "We can have your current state PDLC mapped, benchmarked, and presented to your CFO in 8 weeks. "
      "Here's how to start:",
  0.5, 1.15, 12.3, 0.42, size=14, italic=True, color=STEEL)

steps = [
    ("TODAY",       "Share this deck with your CTO / CFO. Identify the executive sponsor for the pilot."),
    ("THIS WEEK",   "Export your Jira / ADO data (30-min task for your IT team — we send the field spec today)."),
    ("WEEK 1",      "Sign pilot SOW ($150K fixed fee). Platform deployed on your infrastructure or cloud. Kick-off meeting."),
    ("WEEK 2",      "ALM connector live. First VSM dashboard visible. DORA assessment started."),
    ("WEEK 4",      "Top 5 bottlenecks identified. All three AI transformation options modelled on your data."),
    ("WEEK 8",      "Executive readout: CFO-ready business case, board deck, and implementation playbook ready."),
    ("WEEK 9+",     "Choose your option. Quick Wins programme starts. First ROI measured within 90 days."),
]
for i, (t, action) in enumerate(steps):
    y = 1.72 + i * 0.72
    R(sl, 0.25, y, 1.6, 0.6, fill=NAVY if i < 3 else (STEEL if i < 5 else BLUE))
    T(sl, t, 0.28, y+0.1, 1.54, 0.42, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, action, 2.0, y+0.1, 11.0, 0.52, size=12.5, color=TEXT, wrap=True)

R(sl, 0, 6.72, 13.33, 0.78, fill=BLUE)
T(sl, "Contact:  [PARTNER NAME]  |  [email@firm.com]  |  "
      "[+xx xxx xxxx]  |  Accelerated by STUMP",
  0.4, 6.76, 12.5, 0.7, size=13, color=WHITE, align=PP_ALIGN.CENTER)


deck.save(os.path.join(OUT, "01-cxo-pitch-deck-v2.pptx"))
print("  ✓ Saved: 01-cxo-pitch-deck-v2.pptx")

print("\n✓ Complete.")
print(f"  01b-offering-slide-v2.pptx   → refined offering positioning slide (1 slide)")
print(f"  01-cxo-pitch-deck-v2.pptx    → offering-centric CXO deck (15 slides)")
print(f"  Location: {OUT}")
