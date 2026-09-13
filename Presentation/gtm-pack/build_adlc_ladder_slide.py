"""
ADLC Maturity Ladder — L1 → L5 (reaching the Autonomous Development Lifecycle).
Two slides, white background, blue shades only.
  Slide 1: behaviour + team mix (human vs digital) at each level.
  Slide 2: the approach to get to L5.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adlc-ladder")
os.makedirs(OUT, exist_ok=True)

# ── Blue-only palette ────────────────────────────────────────────────────────
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
L1C   = RGBColor(0xBF, 0xDB, 0xFE)   # lightest blue
L2C   = RGBColor(0x93, 0xC5, 0xFD)
L3C   = RGBColor(0x60, 0xA5, 0xFA)
L4C   = RGBColor(0x25, 0x63, 0xEB)
L5C   = RGBColor(0x0F, 0x2D, 0x5E)   # navy
LEVELC = [L1C, L2C, L3C, L4C, L5C]
NAVY  = RGBColor(0x0F, 0x2D, 0x5E)
STEEL = RGBColor(0x1E, 0x40, 0x8A)   # human bar
DIGI  = RGBColor(0x60, 0xA5, 0xFA)   # digital bar
PALE  = RGBColor(0xEF, 0xF6, 0xFF)   # ghost blue panel
PALE2 = RGBColor(0xDB, 0xEA, 0xFE)
INK   = RGBColor(0x1E, 0x29, 0x3B)   # near-black text
SOFT  = RGBColor(0x47, 0x55, 0x69)   # soft grey-blue text


def prs():
    p = Presentation(); p.slide_width = Inches(13.33); p.slide_height = Inches(7.5)
    return p

def blank(p):
    s = p.slides.add_slide(p.slide_layouts[6])
    # explicit white background
    s.background.fill.solid(); s.background.fill.fore_color.rgb = WHITE
    return s

def R(sl, x, y, w, h, fill=None, line=None, lw=0.75, rounded=False):
    shp = sl.shapes.add_shape(5 if rounded else 1, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(lw)
    return shp

def T(sl, text, x, y, w, h, size=11, bold=False, color=INK, align=PP_ALIGN.LEFT,
      anchor=MSO_ANCHOR.TOP, italic=False, wrap=True, spacing=1.0):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Pt(2); tf.margin_top = tf.margin_bottom = Pt(1)
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = line
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic
        f.color.rgb = color; f.name = "Calibri"
    return tb

def title_band(sl, title, sub):
    T(sl, title, 0.5, 0.32, 12.3, 0.55, size=26, bold=True, color=NAVY)
    T(sl, sub, 0.5, 0.92, 12.3, 0.38, size=13, color=L4C, italic=True)
    R(sl, 0.5, 1.34, 12.33, 0.03, fill=L3C)


# ── Ladder data (behaviour + human vs digital team mix) ──────────────────────
LADDER = [
    {"lvl": "L1", "name": "Assisted Prompting", "ml": "ML1 · Foundation",
     "behaviour": "Humans do the work; AI assists via simple prompting in a few phases (mainly Dev & Test).",
     "posture": "AI tools · no agents", "hitl": "Every output human-led",
     "humans": 9, "agents": 2, "digital": 20,
     "roles": "Full team: PO, BA, Architect, Devs, QA, Scrum, DevOps"},
    {"lvl": "L2", "name": "Agent Co-pilots", "ml": "ML2 · Augmentation",
     "behaviour": "Assistive/companion agents across most phases draft work; humans review and approve everything.",
     "posture": "Assistant agents", "hitl": "All outputs reviewed",
     "humans": 8, "agents": 6, "digital": 40,
     "roles": "Full team, AI-augmented (Option A)"},
    {"lvl": "L3", "name": "Supervised Independent", "ml": "ML3 · Automation",
     "behaviour": "Agents act independently on standard cases and interact; humans handle exceptions & quality gates.",
     "posture": "Independent agents", "hitl": "Exceptions only",
     "humans": 6, "agents": 12, "digital": 62,
     "roles": "PO, Architect (incl. risk), Tech Lead, QA Lead, Compliance"},
    {"lvl": "L4", "name": "Orchestrated Agents", "ml": "ML4 · Transformation",
     "behaviour": "Most phases agent-run with multi-agent orchestration end-to-end; humans govern & escalate.",
     "posture": "Orchestrated agents", "hitl": "Gate & govern",
     "humans": 4, "agents": 18, "digital": 78,
     "roles": "Product Definer, Product Builder, Architect (incl. risk), AI Governance"},
    {"lvl": "L5", "name": "Autonomous ADLC", "ml": "ML5 · Reinvention",
     "behaviour": "Fully orchestrated autonomous Agentic Development Lifecycle. Humans set intent, review & approve only.",
     "posture": "Autonomous orchestration", "hitl": "Strategic only",
     "humans": 3, "agents": 21, "digital": 90,
     "roles": "Product Definer · Product Builder · Architect (incl. risk)"},
]

deck = prs()

# ══ SLIDE 1 — the ladder ═════════════════════════════════════════════════════
sl = blank(deck)
title_band(sl, "From L1 to L5 — Reaching the Autonomous Development Lifecycle (ADLC)",
           "Behaviour and team mix (human vs digital) at each maturity level  ·  AI adoption deepens left → right")

# rising arrow strip behind columns
n = len(LADDER)
gap = 0.18
cw = (12.33 - gap * (n - 1)) / n
x0 = 0.5
top = 1.62
colH = 4.95

for i, lv in enumerate(LADDER):
    x = x0 + i * (cw + gap)
    col = LEVELC[i]
    dark = i >= 2          # white text on L3–L5
    txtcol = WHITE if dark else NAVY
    # header
    R(sl, x, top, cw, 0.92, fill=col)
    T(sl, lv["lvl"], x + 0.12, top + 0.06, cw - 0.24, 0.34, size=18, bold=True, color=txtcol)
    T(sl, lv["name"], x + 0.12, top + 0.42, cw - 0.24, 0.46, size=11, bold=True, color=txtcol, wrap=True)
    # body panel
    by = top + 0.92
    R(sl, x, by, cw, colH - 0.92, fill=PALE if i % 2 == 0 else PALE2)
    T(sl, lv["ml"], x + 0.12, by + 0.08, cw - 0.24, 0.26, size=9, bold=True, color=L4C)
    # behaviour
    T(sl, "BEHAVIOUR", x + 0.12, by + 0.36, cw - 0.24, 0.2, size=7.5, bold=True, color=SOFT)
    T(sl, lv["behaviour"], x + 0.12, by + 0.56, cw - 0.24, 1.25, size=9, color=INK, spacing=1.02)
    # posture + HITL
    T(sl, f"Agents: {lv['posture']}\nHuman-in-loop: {lv['hitl']}", x + 0.12, by + 1.78, cw - 0.24, 0.6,
      size=8.3, color=STEEL)
    # team mix bar (human vs digital)
    T(sl, "TEAM MIX  (human vs digital)", x + 0.12, by + 2.42, cw - 0.24, 0.2, size=7.5, bold=True, color=SOFT)
    barx, bary, barw, barh = x + 0.12, by + 2.66, cw - 0.24, 0.26
    dw = barw * lv["digital"] / 100.0
    R(sl, barx, bary, barw - dw, barh, fill=STEEL)          # human (left)
    R(sl, barx + (barw - dw), bary, dw, barh, fill=DIGI)    # digital (right)
    T(sl, f"{100 - lv['digital']}% human", barx, bary + 0.28, barw, 0.2, size=7.5, bold=True, color=STEEL)
    T(sl, f"{lv['digital']}% digital", barx, bary + 0.28, barw, 0.2, size=7.5, bold=True, color=L4C, align=PP_ALIGN.RIGHT)
    # counts
    T(sl, f"~{lv['humans']} humans  ·  {lv['agents']} agents", x + 0.12, by + 3.2, cw - 0.24, 0.24,
      size=9, bold=True, color=NAVY)
    # human roles retained
    R(sl, x, by + 3.5, cw, colH - 0.92 - 3.5, fill=col)
    T(sl, "Humans retained", x + 0.12, by + 3.54, cw - 0.24, 0.2, size=7.5, bold=True,
      color=WHITE if dark else NAVY)
    T(sl, lv["roles"], x + 0.12, by + 3.74, cw - 0.24, 0.62, size=8, color=WHITE if dark else NAVY, spacing=1.0)

# legend + footer
ly = top + colH + 0.12
R(sl, 0.5, ly + 0.03, 0.3, 0.18, fill=STEEL); T(sl, "Human", 0.84, ly, 1.2, 0.24, size=10, color=INK)
R(sl, 2.0, ly + 0.03, 0.3, 0.18, fill=DIGI);  T(sl, "Digital (agents)", 2.34, ly, 2.2, 0.24, size=10, color=INK)
T(sl, "As you climb L1→L5, behaviour shifts from human-led to agent-orchestrated and the team mix inverts — "
      "from ~9 humans : 2 tools to 3 humans : 21 autonomous agents.",
  5.0, ly, 7.8, 0.5, size=10.5, italic=True, color=L4C, wrap=True)


# ══ SLIDE 2 — approach to reach L5 ═══════════════════════════════════════════
sl = blank(deck)
title_band(sl, "The Approach to Reach L5 (ADLC)",
           "Diagnose → choose target & platform → phase the climb → fund it → measure & progress")

steps = [
    ("1", "Diagnose current level",
     "Auto-derive today's level (often L0–L1) from your value-stream data — no manual scoring."),
    ("2", "Define the North-Star + platform",
     "Pick the target level (typically L4–L5) and the delivery platform: home-grown, COTS, or service-provider."),
    ("3", "Phase the climb",
     "Go in one move, or via 1–2 interim stops sized to maturity & risk appetite — e.g. L1 → L3 → L5."),
    ("4", "Fund it on the J-Curve",
     "Cost-only business case: up-front investment + a learning/verification dip, then savings that grow to breakeven."),
    ("5", "Execute & measure",
     "Run each interim step; track adoption, performance & AI-ops on the Outcome Dashboard; progress vs target."),
]
# big horizontal step ribbon
sx, sy, sh = 0.5, 1.7, 1.55
sw = (12.33 - 0.16 * (len(steps) - 1)) / len(steps)
for i, (num, head, desc) in enumerate(steps):
    x = sx + i * (sw + 0.16)
    col = LEVELC[i]
    dark = i >= 2
    tc = WHITE if dark else NAVY
    R(sl, x, sy, sw, sh, fill=col)
    R(sl, x + 0.14, sy + 0.14, 0.5, 0.5, fill=WHITE if dark else NAVY)
    T(sl, num, x + 0.14, sy + 0.18, 0.5, 0.42, size=20, bold=True,
      color=col if dark else WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    T(sl, head, x + 0.12, sy + 0.7, sw - 0.24, 0.46, size=11, bold=True, color=tc, wrap=True)
    T(sl, desc, x + 0.12, sy + 1.14, sw - 0.24, 0.36, size=8.2, color=tc, wrap=True)
    if i < len(steps) - 1:
        T(sl, "›", x + sw - 0.02, sy + 0.5, 0.18, 0.5, size=22, bold=True, color=L3C)

# the climb visual — levels as ascending blocks
cy = 3.7
T(sl, "The climb — humans direct, agents do the work (team mix inverts as autonomy rises)",
  0.5, cy - 0.1, 12.33, 0.3, size=11, bold=True, color=NAVY)
bx, bw = 0.5, 12.33 / 5
maxh = 2.05
for i, lv in enumerate(LADDER):
    x = bx + i * bw
    h = 0.6 + (maxh - 0.6) * i / 4.0
    y = cy + 0.4 + (maxh - h)
    col = LEVELC[i]
    R(sl, x + 0.3, y, bw - 0.6, h, fill=col)
    dark = i >= 2
    T(sl, lv["lvl"], x + 0.3, y + 0.06, bw - 0.6, 0.3, size=14, bold=True,
      color=WHITE if dark else NAVY, align=PP_ALIGN.CENTER)
    T(sl, lv["name"], x + 0.3, y + 0.36, bw - 0.6, 0.5, size=8.5, bold=True,
      color=WHITE if dark else NAVY, align=PP_ALIGN.CENTER, wrap=True)
    T(sl, f"{100 - lv['digital']}%H · {lv['digital']}%D", x + 0.3, y + h - 0.28, bw - 0.6, 0.24,
      size=8, bold=True, color=WHITE if dark else STEEL, align=PP_ALIGN.CENTER)
    T(sl, f"~{lv['humans']}:{lv['agents']}", x + 0.3, cy + 0.4 + maxh + 0.06, bw - 0.6, 0.24,
      size=9, color=SOFT, align=PP_ALIGN.CENTER)

# footer band
R(sl, 0.5, 6.78, 12.33, 0.5, fill=NAVY)
T(sl, "L5 = Autonomous ADLC: agents own end-to-end execution under orchestration; humans = Product Definer, "
      "Product Builder & Architect (incl. risk) setting intent, reviewing and approving.",
  0.66, 6.84, 12.0, 0.42, size=10.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)

path = os.path.join(OUT, "ADLC-L1-to-L5-ladder.pptx")
deck.save(path)
print("✓ Saved:", path, "(2 slides)")
