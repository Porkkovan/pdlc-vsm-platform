"""
Build PDLC VSM Platform — Option A & B Demo Deck (PowerPoint)
White background, step-by-step instructions, talking points + data per slide.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Palette ────────────────────────────────────────────────────────────────
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
BLACK      = RGBColor(0x1A, 0x1A, 0x2E)
DARK_GRAY  = RGBColor(0x37, 0x37, 0x37)
MID_GRAY   = RGBColor(0x64, 0x74, 0x8B)
LIGHT_GRAY = RGBColor(0xF1, 0xF5, 0xF9)
RULE_GRAY  = RGBColor(0xE2, 0xE8, 0xF0)

BLUE_DARK  = RGBColor(0x1E, 0x40, 0xAF)   # deep blue – Option A accent
BLUE_MED   = RGBColor(0x25, 0x63, 0xEB)
BLUE_LIGHT = RGBColor(0xDB, 0xEA, 0xFE)

PURPLE_DARK  = RGBColor(0x5B, 0x21, 0xB6) # deep purple – Option B accent
PURPLE_MED   = RGBColor(0x7C, 0x3A, 0xED)
PURPLE_LIGHT = RGBColor(0xED, 0xE9, 0xFE)

GREEN_DARK  = RGBColor(0x14, 0x53, 0x2D)
GREEN_MED   = RGBColor(0x16, 0xA3, 0x4A)
GREEN_LIGHT = RGBColor(0xDC, 0xFC, 0xE7)

AMBER_DARK  = RGBColor(0x92, 0x40, 0x0E)
AMBER_MED   = RGBColor(0xD9, 0x77, 0x06)
AMBER_LIGHT = RGBColor(0xFE, 0xF3, 0xC7)

RED_DARK    = RGBColor(0x7F, 0x1D, 0x1D)
RED_MED     = RGBColor(0xDC, 0x26, 0x26)
RED_LIGHT   = RGBColor(0xFE, 0xE2, 0xE2)

# ── Slide dimensions (Widescreen 16:9) ────────────────────────────────────
W = Inches(13.33)
H = Inches(7.5)


def prs_new():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs


def blank_layout(prs):
    return prs.slide_layouts[6]   # completely blank


# ── Low-level helpers ──────────────────────────────────────────────────────

def add_rect(slide, left, top, width, height, fill_rgb, opacity=None, rounding=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)   # MSO_SHAPE_TYPE.RECTANGLE = 1
    shape.line.fill.background()
    shape.line.width = 0
    if fill_rgb is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=14, bold=False, italic=False,
             color=BLACK, align=PP_ALIGN.LEFT,
             wrap=True, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_para(tf, text, font_size=11, bold=False, italic=False,
             color=DARK_GRAY, align=PP_ALIGN.LEFT, space_before=0,
             font_name="Calibri"):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return p


def add_textbox_multiline(slide, lines, left, top, width, height,
                          base_size=11, base_color=DARK_GRAY,
                          base_bold=False, wrap=True,
                          font_name="Calibri"):
    """lines = list of (text, size, bold, italic, color, align, space_before)"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    first = True
    for item in lines:
        if isinstance(item, str):
            item = (item, base_size, base_bold, False, base_color, PP_ALIGN.LEFT, 0)
        text, size, bold, italic, color, align, space_before = item
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(space_before)
        run = p.add_run()
        run.text = text
        run.font.name = font_name
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
    return txBox


def h_rule(slide, top, left=Inches(0.45), width=Inches(12.4), color=RULE_GRAY):
    add_rect(slide, left, top, width, Pt(1.5), color)


def add_badge(slide, text, left, top, width=Inches(1.5), height=Inches(0.32),
              bg=BLUE_LIGHT, fg=BLUE_DARK, font_size=9, bold=True):
    add_rect(slide, left, top, width, height, bg)
    add_text(slide, text, left, top, width, height,
             font_size=font_size, bold=bold, color=fg,
             align=PP_ALIGN.CENTER)


def add_step_circle(slide, number, left, top, size=Inches(0.38),
                    bg=BLUE_MED, fg=WHITE):
    add_rect(slide, left, top, size, size, bg)
    add_text(slide, str(number), left, top, size, size,
             font_size=13, bold=True, color=fg, align=PP_ALIGN.CENTER)


def add_stat_box(slide, value, label, left, top,
                 width=Inches(1.9), height=Inches(0.95),
                 value_color=BLUE_DARK, bg=BLUE_LIGHT):
    add_rect(slide, left, top, width, height, bg)
    add_text(slide, value, left, top + Inches(0.06), width, Inches(0.48),
             font_size=20, bold=True, color=value_color, align=PP_ALIGN.CENTER)
    add_text(slide, label, left, top + Inches(0.52), width, Inches(0.38),
             font_size=9, bold=False, color=MID_GRAY, align=PP_ALIGN.CENTER)


def add_arrow_right(slide, left, top, length=Inches(0.35), voffset=Inches(0.12)):
    """Simple right-arrow using a narrow rect + triangle approximation via text."""
    add_text(slide, "→", left, top + voffset, length, Inches(0.35),
             font_size=18, bold=True, color=MID_GRAY, align=PP_ALIGN.CENTER)


# ── Slide header (consistent across all slides) ────────────────────────────

def slide_header(slide, title, subtitle=None, accent=BLUE_DARK,
                 badge_text=None, badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 slide_num=None, total_slides=None):
    # Top accent bar
    add_rect(slide, 0, 0, W, Inches(0.06), accent)
    # Title
    add_text(slide, title,
             Inches(0.45), Inches(0.18), Inches(11.0), Inches(0.55),
             font_size=22, bold=True, color=BLACK)
    # Subtitle
    if subtitle:
        add_text(slide, subtitle,
                 Inches(0.45), Inches(0.70), Inches(10.0), Inches(0.38),
                 font_size=12, bold=False, color=MID_GRAY)
    # Badge
    if badge_text:
        add_badge(slide, badge_text, Inches(10.7), Inches(0.22),
                  width=Inches(2.2), height=Inches(0.32),
                  bg=badge_bg, fg=badge_fg, font_size=9, bold=True)
    # Slide number
    if slide_num and total_slides:
        add_text(slide, f"{slide_num} / {total_slides}",
                 Inches(12.5), Inches(0.22), Inches(0.8), Inches(0.28),
                 font_size=8, color=MID_GRAY, align=PP_ALIGN.RIGHT)
    # Rule under header
    h_rule(slide, Inches(1.05))


def talking_points_panel(slide, points, left=Inches(8.85), top=Inches(1.18),
                         width=Inches(4.05), height=Inches(5.85),
                         accent=BLUE_DARK, title="Talking Points"):
    """Right-side talking points panel."""
    add_rect(slide, left, top, width, height, LIGHT_GRAY)
    add_rect(slide, left, top, width, Inches(0.34), accent)
    add_text(slide, f"  {title}",
             left, top, width, Inches(0.34),
             font_size=9, bold=True, color=WHITE)
    y = top + Inches(0.42)
    remaining = height - Inches(0.42)
    tb = slide.shapes.add_textbox(left + Inches(0.14), y,
                                  width - Inches(0.28), remaining - Inches(0.15))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for pt in points:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
            p.space_before = Pt(4)
        run = p.add_run()
        run.text = f"• {pt}"
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = DARK_GRAY


def screen_label(slide, url_path, left=Inches(0.45), top=Inches(1.12)):
    add_text(slide, f"  Screen:  localhost:3001{url_path}",
             left, top, Inches(6.5), Inches(0.28),
             font_size=8, bold=False, color=MID_GRAY, italic=True)


# ══════════════════════════════════════════════════════════════════════════
#  SLIDE BUILDERS
# ══════════════════════════════════════════════════════════════════════════

def slide_cover(prs):
    slide = prs.slides.add_slide(blank_layout(prs))
    # Full-width top band
    add_rect(slide, 0, 0, W, Inches(0.55), BLUE_DARK)
    # Left accent bar
    add_rect(slide, 0, 0, Inches(0.18), H, BLUE_DARK)
    # Platform label
    add_text(slide, "PDLC VSM PLATFORM",
             Inches(0.55), Inches(1.4), Inches(12.0), Inches(0.5),
             font_size=13, bold=True, color=BLUE_MED, align=PP_ALIGN.CENTER)
    # Main title
    add_text(slide, "Option A & Option B",
             Inches(0.55), Inches(2.0), Inches(12.0), Inches(1.0),
             font_size=38, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
    add_text(slide, "Senior Leadership Demo — Step-by-Step Guide",
             Inches(0.55), Inches(3.0), Inches(12.0), Inches(0.55),
             font_size=20, bold=False, color=DARK_GRAY, align=PP_ALIGN.CENTER)
    h_rule(slide, Inches(3.62), left=Inches(2.5), width=Inches(8.3), color=RULE_GRAY)
    # Scenario badges
    add_badge(slide, "Option A — AI-Assisted (40% Automation)",
              Inches(2.0), Inches(3.85), width=Inches(4.0), height=Inches(0.40),
              bg=BLUE_LIGHT, fg=BLUE_DARK, font_size=11, bold=True)
    add_badge(slide, "Option B — Hybrid AI (65% Automation)",
              Inches(7.3), Inches(3.85), width=Inches(4.0), height=Inches(0.40),
              bg=PURPLE_LIGHT, fg=PURPLE_DARK, font_size=11, bold=True)
    # Meta row
    add_text(slide,
             "Demo Duration: 25–35 min     |     Fast-Track: 15 min     |     Audience: CTO · CPO · VP Engineering · CFO",
             Inches(0.55), Inches(4.65), Inches(12.0), Inches(0.35),
             font_size=10, color=MID_GRAY, align=PP_ALIGN.CENTER)
    # URL
    add_text(slide, "http://localhost:3001",
             Inches(0.55), Inches(5.1), Inches(12.0), Inches(0.3),
             font_size=9, color=MID_GRAY, align=PP_ALIGN.CENTER, italic=True)
    # Footer band
    add_rect(slide, 0, H - Inches(0.45), W, Inches(0.45), LIGHT_GRAY)
    add_text(slide, "7 PDLC Phases  ·  36 Activities  ·  8 LangGraph Agents  ·  3 Future State Scenarios",
             Inches(0.55), H - Inches(0.4), Inches(12.0), Inches(0.38),
             font_size=9, color=MID_GRAY, align=PP_ALIGN.CENTER)


def slide_agenda(prs, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Demo Agenda & Flow", "8 steps — shared foundation then scenario branch",
                 slide_num=2, total_slides=total)

    steps_shared = [
        ("1", "Dashboard",          "Team context, workflow overview",    "3 min",  BLUE_MED),
        ("2", "DORA Assessment",    "Baseline engineering performance",   "3 min",  BLUE_MED),
        ("3", "Current State VSM",  "Where time actually goes today",     "4 min",  BLUE_MED),
        ("4", "Bottleneck Analysis","Critical flow blockers identified",  "3 min",  BLUE_MED),
    ]
    steps_branch = [
        ("5A", "Future State — A",  "AI-Assisted scenario metrics",      "4 min",  BLUE_DARK),
        ("5B", "Future State — B",  "Hybrid AI scenario metrics",        "4 min",  PURPLE_DARK),
        ("6A", "Business Case — A", "2.8× ROI · 14-month payback",       "4 min",  BLUE_DARK),
        ("6B", "Business Case — B", "3.8× ROI · 11-month payback",       "4 min",  PURPLE_DARK),
        ("7",  "Playbook",          "Personalised 90-day action plan",    "3 min",  GREEN_MED),
    ]

    add_text(slide, "SHARED FOUNDATION  (steps 1–4)",
             Inches(0.45), Inches(1.22), Inches(8.2), Inches(0.3),
             font_size=9, bold=True, color=BLUE_DARK)
    y = Inches(1.52)
    for (num, title, desc, dur, col) in steps_shared:
        add_rect(slide, Inches(0.45), y, Inches(8.2), Inches(0.52), LIGHT_GRAY)
        add_rect(slide, Inches(0.45), y, Inches(0.42), Inches(0.52), col)
        add_text(slide, num, Inches(0.45), y, Inches(0.42), Inches(0.52),
                 font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, title, Inches(0.95), y + Inches(0.04), Inches(4.0), Inches(0.26),
                 font_size=11, bold=True, color=BLACK)
        add_text(slide, desc, Inches(0.95), y + Inches(0.27), Inches(4.8), Inches(0.22),
                 font_size=9, color=MID_GRAY)
        add_text(slide, dur, Inches(7.6), y + Inches(0.12), Inches(1.0), Inches(0.28),
                 font_size=10, bold=True, color=col, align=PP_ALIGN.RIGHT)
        y += Inches(0.60)

    add_text(slide, "SCENARIO BRANCH  (steps 5–7)",
             Inches(0.45), y + Inches(0.1), Inches(8.2), Inches(0.3),
             font_size=9, bold=True, color=MID_GRAY)
    y += Inches(0.42)
    for (num, title, desc, dur, col) in steps_branch:
        bg = BLUE_LIGHT if col == BLUE_DARK else (PURPLE_LIGHT if col == PURPLE_DARK else GREEN_LIGHT)
        add_rect(slide, Inches(0.45), y, Inches(8.2), Inches(0.50), bg)
        add_rect(slide, Inches(0.45), y, Inches(0.42), Inches(0.50), col)
        add_text(slide, num, Inches(0.45), y, Inches(0.42), Inches(0.50),
                 font_size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, title, Inches(0.95), y + Inches(0.03), Inches(4.0), Inches(0.24),
                 font_size=10, bold=True, color=BLACK)
        add_text(slide, desc, Inches(0.95), y + Inches(0.26), Inches(4.8), Inches(0.20),
                 font_size=9, color=MID_GRAY)
        add_text(slide, dur, Inches(7.6), y + Inches(0.12), Inches(1.0), Inches(0.25),
                 font_size=10, bold=True, color=col, align=PP_ALIGN.RIGHT)
        y += Inches(0.57)

    # Right summary panel
    add_rect(slide, Inches(8.9), Inches(1.22), Inches(4.0), Inches(5.8), LIGHT_GRAY)
    add_rect(slide, Inches(8.9), Inches(1.22), Inches(4.0), Inches(0.34), BLUE_DARK)
    add_text(slide, "  Fast-Track Path (15 min)",
             Inches(8.9), Inches(1.22), Inches(4.0), Inches(0.34),
             font_size=9, bold=True, color=WHITE)
    ft_lines = [
        ("Skip steps 1–2. Start at:", 10, True, False, BLACK, PP_ALIGN.LEFT, 6),
        ("Step 3 → Current State VSM", 10, False, False, DARK_GRAY, PP_ALIGN.LEFT, 4),
        ("Step 5 → Future State (A or B)", 10, False, False, DARK_GRAY, PP_ALIGN.LEFT, 2),
        ("Step 6 → Business Case", 10, False, False, DARK_GRAY, PP_ALIGN.LEFT, 2),
        ("Step 7 → Playbook", 10, False, False, DARK_GRAY, PP_ALIGN.LEFT, 2),
        ("", 6, False, False, DARK_GRAY, PP_ALIGN.LEFT, 4),
        ("Pre-Demo Checklist:", 10, True, False, BLACK, PP_ALIGN.LEFT, 6),
        ("✓  Backend running on :8001", 9, False, False, GREEN_MED, PP_ALIGN.LEFT, 3),
        ("✓  Frontend running on :3001", 9, False, False, GREEN_MED, PP_ALIGN.LEFT, 3),
        ("✓  DORA set to Medium Performer", 9, False, False, GREEN_MED, PP_ALIGN.LEFT, 3),
        ("✓  VSM Level = Feature Level", 9, False, False, GREEN_MED, PP_ALIGN.LEFT, 3),
        ("✓  Future State default = Option A", 9, False, False, GREEN_MED, PP_ALIGN.LEFT, 3),
        ("✓  Playbook: org/team pre-filled", 9, False, False, GREEN_MED, PP_ALIGN.LEFT, 3),
        ("", 6, False, False, DARK_GRAY, PP_ALIGN.LEFT, 4),
        ("Opening statement:", 10, True, False, BLACK, PP_ALIGN.LEFT, 6),
        ('"90% of your feature lead time is waste. Most teams have never measured where it actually goes. This platform changes that."',
         9, False, True, DARK_GRAY, PP_ALIGN.LEFT, 3),
    ]
    add_textbox_multiline(slide, ft_lines,
                          Inches(9.05), Inches(1.6), Inches(3.75), Inches(5.3))


def slide_step1_dashboard(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 1 — Dashboard",
                 "Set team context and orient the audience to the platform workflow",
                 badge_text="SHARED STEP  (both scenarios)", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 slide_num=n, total_slides=total)
    screen_label(slide, "/dashboard")

    # Step-by-step actions
    actions = [
        ("Navigate to Dashboard", "Open http://localhost:3001 — you land on the Dashboard page automatically."),
        ("Set Team Context", "Click Edit in the Team Context card. Fill in: Organisation, Portfolio, Product Group, Team name. Click 'Save & Persist'. This persists to the backend database."),
        ("Set VSM Level", "In the VSM Analysis Level card (top-right), select 'Feature Level'. Show the stats update: 7 Phases, 36 Activities, Lead Time 30–50 days."),
        ("Walk the Workflow Steps", "Point to the 8-step workflow card. Read each step aloud. 'We will walk every one of these steps in the next 25 minutes.'"),
        ("Show Future State Scenarios", "Scroll to the 3 Future State Scenarios cards at the bottom — briefly show Option A / B / C improvement %s before going further."),
    ]

    y = Inches(1.18)
    for i, (title, detail) in enumerate(actions):
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.72), LIGHT_GRAY)
        add_step_circle(slide, i + 1, Inches(0.5), y + Inches(0.17), bg=BLUE_MED)
        add_text(slide, title, Inches(1.0), y + Inches(0.05), Inches(7.65), Inches(0.26),
                 font_size=11, bold=True, color=BLACK)
        add_text(slide, detail, Inches(1.0), y + Inches(0.3), Inches(7.65), Inches(0.36),
                 font_size=9.5, color=DARK_GRAY)
        y += Inches(0.82)

    talking_points_panel(slide, [
        "The platform covers the complete PDLC — 7 phases, 36 activities, from backlog to production monitoring.",
        "Feature Level = full 42.5-day lead time story. User Story Level = dev-test-deploy cycle only (8.5 days). Keep Feature Level on for this demo.",
        "Option A = AI agents assist all 8 human roles. No role changes. 40% automation. Fastest to deploy (6–10 weeks).",
        "Option B = 65% automation, 5 human roles. Higher ROI but requires custom agent development (12–16 weeks).",
        "The 8-step workflow is the narrative thread for the entire demo — reference it before each new screen.",
        "Pause here to ask: 'Does your team currently measure Flow Efficiency?' Answer is almost always no — this sets up the impact of slide 3.",
    ], accent=BLUE_DARK)


def slide_step2_dora(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 2 — DORA Assessment",
                 "Establish the engineering performance baseline before mapping the value stream",
                 badge_text="SHARED STEP  (both scenarios)", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 slide_num=n, total_slides=total)
    screen_label(slide, "/dora-assessment")

    actions = [
        ("Navigate to DORA Assessment", "Click 'DORA Assessment' in the sidebar (Setup & Data group)."),
        ("Explain DORA", "DORA = 4 metrics from Google's State of DevOps research. Covers 33,000+ organisations globally. It tells us whether today's baseline is realistic for this team."),
        ("Set Medium Performer values", "Deployment Frequency: 'Once per week'  |  Lead Time for Changes: '1–2 weeks'  |  Change Failure Rate: 15%  |  MTTR: '1–7 days'"),
        ("Watch the band update", "Point to the Elite / High / Medium / Low indicator — it updates live. 'Medium Performer' banner appears."),
        ("Show VSM Calibration", "Scroll down to the VSM Calibration section — show how DORA scores adjust the Phase 5 (Testing) and Phase 6 (Delivery) wait times. Click 'Apply Calibration to VSM'."),
        ("Proceed", "Click 'Continue to VSM Analysis →' or navigate to Current State VSM in the sidebar."),
    ]

    # DORA benchmark data boxes
    stats = [
        ("Elite", "Top 18%\nof orgs", GREEN_MED, GREEN_LIGHT),
        ("High", "27%\nof orgs", BLUE_MED, BLUE_LIGHT),
        ("Medium", "42%\nof orgs", AMBER_MED, AMBER_LIGHT),
        ("Low", "13%\nof orgs", RED_MED, RED_LIGHT),
    ]
    sx = Inches(0.45)
    for (label, val, col, bg) in stats:
        add_rect(slide, sx, Inches(1.18), Inches(1.85), Inches(0.80), bg)
        add_text(slide, label, sx, Inches(1.22), Inches(1.85), Inches(0.35),
                 font_size=13, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_text(slide, val, sx, Inches(1.52), Inches(1.85), Inches(0.42),
                 font_size=9, color=MID_GRAY, align=PP_ALIGN.CENTER)
        sx += Inches(1.95)

    y = Inches(2.12)
    for i, (title, detail) in enumerate(actions):
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.69), LIGHT_GRAY)
        add_step_circle(slide, i + 1, Inches(0.5), y + Inches(0.16), bg=BLUE_MED)
        add_text(slide, title, Inches(1.0), y + Inches(0.04), Inches(7.65), Inches(0.26),
                 font_size=11, bold=True, color=BLACK)
        add_text(slide, detail, Inches(1.0), y + Inches(0.30), Inches(7.65), Inches(0.34),
                 font_size=9.5, color=DARK_GRAY)
        y += Inches(0.78)

    talking_points_panel(slide, [
        "DORA bands: Only 18% of organisations are Elite. The majority (42%) are Medium.",
        "The throughput gap between Elite and Low performers is ~1,460× — not a typo. Elite teams deploy thousands of times per day; Low performers deploy once every 6+ months.",
        "When you input Medium Performer values, the VSM calibration adjusts Phase 5 (Testing) wait times upward and Phase 3 (Code) wait times to reflect code review queues. This makes every metric that follows specific to their team's real performance.",
        "Key stat to land: 'Elite performers have 7× lower change failure rates AND deploy 208× more frequently. This is not about working harder — it's about removing the waiting time from the system.'",
        "If the audience pushes back on data quality: 'Connect your Jira or Azure DevOps in Step 1 (ALM Connect) and every metric in this DORA assessment is automatically replaced with your actual cycle time data.'",
    ], accent=BLUE_DARK)


def slide_step3_vsm(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 3 — Current State Value Stream Map",
                 "Show the audience where their time actually goes — the 'before' picture",
                 badge_text="SHARED STEP  (both scenarios)", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 slide_num=n, total_slides=total)
    screen_label(slide, "/current-vsm")

    # Baseline metrics
    metrics = [
        ("100 hrs", "Process Time", BLUE_DARK, BLUE_LIGHT),
        ("536 hrs", "Wait Time", RED_MED, RED_LIGHT),
        ("42.5 days", "Lead Time", DARK_GRAY, LIGHT_GRAY),
        ("8.1%", "Flow Efficiency", AMBER_MED, AMBER_LIGHT),
    ]
    mx = Inches(0.45)
    for (val, lbl, col, bg) in metrics:
        add_stat_box(slide, val, lbl, mx, Inches(1.18),
                     value_color=col, bg=bg)
        mx += Inches(2.02)

    actions = [
        ("Open Visual Flow tab", "The default tab shows the horizontal VSM diagram. 7 phase cards connected by arrows. Point to Phase 5 (Continuous Testing) — orange border = bottleneck."),
        ("Read the KPI summary", "Point to the 4 metric cards below the diagram. '100 hours of actual work against 536 hours of waiting. Flow Efficiency is 8.1%.'"),
        ("Switch to Flow Bars tab", "Shows PT vs WT ratio as horizontal bars per phase. Phase 5 is almost entirely red. Phase 6 (Delivery) is also mostly red."),
        ("Switch to Phases tab", "Expand Phase 5 — Continuous Testing. Show each activity, its effort and wait range, the AI opportunity description, and the assigned agent."),
        ("Click 'Run AI Analysis'", "Shows the VSM Analyzer agent running. Even in demo mode, the output prepopulates Bottleneck Analysis on the next screen."),
    ]

    y = Inches(2.18)
    for i, (title, detail) in enumerate(actions):
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.69), LIGHT_GRAY)
        add_step_circle(slide, i + 1, Inches(0.5), y + Inches(0.16), bg=BLUE_MED)
        add_text(slide, title, Inches(1.0), y + Inches(0.04), Inches(7.65), Inches(0.26),
                 font_size=11, bold=True, color=BLACK)
        add_text(slide, detail, Inches(1.0), y + Inches(0.30), Inches(7.65), Inches(0.34),
                 font_size=9.5, color=DARK_GRAY)
        y += Inches(0.78)

    talking_points_panel(slide, [
        "The headline stat: 8.1% Flow Efficiency. 'For every day your team is actively working on a feature, they're waiting for 12 days.'",
        "World-class teams achieve 40%+ flow efficiency. Enterprise average is 10–15%. Government and regulated industries often under 5%.",
        "Phase 5 — Continuous Testing — is the dominant bottleneck in 94% of enterprise software organisations (Gartner 2024). It has the longest effort AND the longest wait.",
        "Phase 6 — Continuous Delivery — adds another 1–5 days of wait from CAB / release gate scheduling. This is a governance problem, not a technology problem — AI can fix it.",
        "The visual flow diagram is the single most impactful screen in the demo. It makes visible what no sprint board ever shows: the queue between the work.",
        "Power move: if the audience has brought their own data, ask them their current Lead Time. Then show how their number maps onto the chart.",
    ], accent=BLUE_DARK)


def slide_step4_bottlenecks(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 4 — Bottleneck Analysis",
                 "AI identifies the 8 critical flow blockers — with impact and severity ratings",
                 badge_text="SHARED STEP  (both scenarios)", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 slide_num=n, total_slides=total)
    screen_label(slide, "/bottlenecks")

    # Bottleneck summary stats
    stats2 = [
        ("2", "Critical", RED_MED, RED_LIGHT),
        ("3", "High", AMBER_MED, AMBER_LIGHT),
        ("3", "Medium", BLUE_MED, BLUE_LIGHT),
        ("6/8", "In Testing &\nDelivery", DARK_GRAY, LIGHT_GRAY),
    ]
    sx = Inches(0.45)
    for (val, lbl, col, bg) in stats2:
        add_stat_box(slide, val, lbl, sx, Inches(1.18),
                     width=Inches(1.85), height=Inches(0.88),
                     value_color=col, bg=bg)
        sx += Inches(1.95)

    bottlenecks = [
        ("CRITICAL", "Phase 5", "Automated Performance Testing",    "16–40 hrs effort", RED_MED, RED_LIGHT),
        ("CRITICAL", "Phase 5", "Manual SIT / UAT / NF Sign-off",   "2–5 days wait",    RED_MED, RED_LIGHT),
        ("HIGH",     "Phase 3", "Peer Code Review",                  "4–24 hrs wait",    AMBER_MED, AMBER_LIGHT),
        ("HIGH",     "Phase 5", "Test Data Generation / Management", "4–16 hrs wait",    AMBER_MED, AMBER_LIGHT),
        ("HIGH",     "Phase 6", "Release Gates / CAB Approvals",     "1–5 days wait",    AMBER_MED, AMBER_LIGHT),
    ]

    y = Inches(2.2)
    for (sev, phase, activity, impact, col, bg) in bottlenecks:
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.54), bg)
        add_badge(slide, sev, Inches(0.48), y + Inches(0.11),
                  width=Inches(0.85), height=Inches(0.26),
                  bg=col, fg=WHITE, font_size=8, bold=True)
        add_text(slide, phase, Inches(1.4), y + Inches(0.05), Inches(1.0), Inches(0.22),
                 font_size=8, color=MID_GRAY, bold=False)
        add_text(slide, activity, Inches(1.4), y + Inches(0.24), Inches(4.9), Inches(0.24),
                 font_size=10, bold=True, color=BLACK)
        add_text(slide, impact, Inches(6.45), y + Inches(0.15), Inches(2.2), Inches(0.26),
                 font_size=9.5, bold=True, color=col, align=PP_ALIGN.RIGHT)
        y += Inches(0.62)

    actions_text = ("Navigate to /bottlenecks  →  Click 'Critical' filter  →  Walk the top 2 cards  →  Scroll to Phase Heatmap  →  'Phase 5 is red — this is where we focus first.'")
    add_rect(slide, Inches(0.45), y + Inches(0.08), Inches(8.25), Inches(0.44), BLUE_LIGHT)
    add_text(slide, "Demo Action:  " + actions_text,
             Inches(0.55), y + Inches(0.10), Inches(8.1), Inches(0.40),
             font_size=9, color=BLUE_DARK, bold=False)

    talking_points_panel(slide, [
        "Critical #1 — Performance Testing: 16–40 hours manual effort. AI performance analyzers (e.g. Dynatrace Davis AI) auto-detect regressions and correlate with code changes. Effort drops to 4–8 hours.",
        "Critical #2 — Manual UAT Sign-off: 2–5 day wait. AI UAT Assistant consolidates results and risk-scores readiness. Same-day exception-based sign-off replaces the 5-day queue.",
        "High — Code Review: 4–24 hour wait on reviewer availability. ReviewAgent provides instant diff analysis. Human reviewer focuses on architecture and business logic only.",
        "High — Release Gates: 1–5 day CAB scheduling wait. AI Release Manager auto-validates all release criteria and generates compliance evidence. Enables continuous deployment.",
        "6 of 8 bottlenecks are in Testing and Delivery phases — this is a deliberate pattern. The quality and governance layers are where enterprise organisations accumulate the most waste.",
        "The heatmap is board-ready. Show it as the 'executive summary' of the analysis — one view, which phases are green vs red.",
    ], accent=RED_MED, title="Talking Points")


def slide_step5a_future(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 5A — Future State VSM: Option A",
                 "AI-Assisted Transformation — 40% automation, all 8 human roles retained",
                 badge_text="OPTION A — AI-ASSISTED", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 accent=BLUE_DARK, slide_num=n, total_slides=total)
    screen_label(slide, "/future-state  (select Option A)")

    # Before / after metrics
    add_text(slide, "BEFORE (Current State)",
             Inches(0.45), Inches(1.18), Inches(3.8), Inches(0.28),
             font_size=9, bold=True, color=MID_GRAY)
    add_text(slide, "OPTION A — After",
             Inches(4.45), Inches(1.18), Inches(3.8), Inches(0.28),
             font_size=9, bold=True, color=BLUE_DARK)

    before = [("42.5 days", "Lead Time"), ("8.1%", "Flow Eff."), ("536 hrs", "Wait Time"), ("100 hrs", "Process Time")]
    after  = [("25.5 days", "Lead Time", "−40%"), ("16.2%", "Flow Eff.", "+100%"), ("238 hrs", "Wait Time", "−56%"), ("65 hrs", "Process Time", "−35%")]

    bx = Inches(0.45)
    for (val, lbl) in before:
        add_stat_box(slide, val, lbl, bx, Inches(1.48), width=Inches(0.88), height=Inches(0.80),
                     value_color=MID_GRAY, bg=LIGHT_GRAY)
        bx += Inches(0.95)

    ax = Inches(4.45)
    for (val, lbl, delta) in after:
        add_stat_box(slide, val, lbl, ax, Inches(1.48), width=Inches(0.88), height=Inches(0.80),
                     value_color=BLUE_DARK, bg=BLUE_LIGHT)
        add_text(slide, delta, ax, Inches(2.26), Inches(0.88), Inches(0.22),
                 font_size=8, bold=True, color=GREEN_MED, align=PP_ALIGN.CENTER)
        ax += Inches(0.95)

    add_text(slide, "→", Inches(3.55), Inches(1.72), Inches(0.75), Inches(0.35),
             font_size=22, bold=True, color=BLUE_DARK, align=PP_ALIGN.CENTER)

    actions = [
        ("Navigate to Future State", "Click 'Future State VSM' in the sidebar. Ensure 'Option A' tab is selected (blue tab, top of page)."),
        ("Show the Visual Flow", "The VSM diagram now shows AI Agent labels on relevant phase cards. Point to green-bordered phases — these have active AI agents assigned."),
        ("Read the improvement metrics", "Lead Time: 42.5 → 25.5 days (−40%). Flow Efficiency: 8.1% → 16.2% (doubles). Process Time: −35%. Wait Time: −56%."),
        ("Show Option A agents", "16 AI agents deployed alongside all 8 human roles: FeatureGen, StoryGen, CodeGen, ReviewAgent, DataGen, TestGen, AI UAT Assistant, AI Release Manager, and more."),
        ("Switch to Table view", "Click 'Table' to show per-activity PT and WT before/after. Highlight Automated Performance Testing: 28 hrs → 6 hrs. UAT Sign-off: 3 days → 0.5 days."),
    ]

    y = Inches(2.45)
    for i, (title, detail) in enumerate(actions):
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.66), LIGHT_GRAY)
        add_step_circle(slide, i + 1, Inches(0.5), y + Inches(0.15), bg=BLUE_MED)
        add_text(slide, title, Inches(1.0), y + Inches(0.03), Inches(7.65), Inches(0.24),
                 font_size=10.5, bold=True, color=BLACK)
        add_text(slide, detail, Inches(1.0), y + Inches(0.27), Inches(7.65), Inches(0.34),
                 font_size=9.5, color=DARK_GRAY)
        y += Inches(0.76)

    talking_points_panel(slide, [
        "Option A = the 'safe start'. Every human role is retained. No retrenchments. No org restructure. 16 AI agents placed alongside every person in the PDLC.",
        "Lead time 42.5 → 25.5 days = 17 fewer days per feature. For a team delivering 20 features per quarter, that's 340 person-days of wait time eliminated every quarter.",
        "Flow Efficiency doubles from 8.1% to 16.2%. Still well below world-class (40%+) — Option A is the first step, not the destination.",
        "The 16 agents cover every phase. CodeGen (GitHub Copilot) in Phase 3. ReviewAgent instant diff analysis. DataGen for synthetic test data. AI UAT Assistant for same-day sign-off.",
        "Key message: 'Option A is achievable in 6–10 weeks at the team level. SaaS tools go live in days. Training is 10–15 people. No cross-org procurement required.'",
        "Industry reference: GitHub Copilot deployed to 500 Salesforce developers in 3 weeks. 35% reduction in coding time validated across 10+ enterprise deployments.",
    ], accent=BLUE_DARK)


def slide_step5b_future(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 5B — Future State VSM: Option B",
                 "Hybrid AI Transformation — 65% automation, 5 core human roles",
                 badge_text="OPTION B — HYBRID AI", badge_bg=PURPLE_LIGHT, badge_fg=PURPLE_DARK,
                 accent=PURPLE_DARK, slide_num=n, total_slides=total)
    screen_label(slide, "/future-state  (select Option B)")

    before = [("42.5 days", "Lead Time"), ("8.1%", "Flow Eff."), ("536 hrs", "Wait Time"), ("100 hrs", "Process Time")]
    after  = [("19.1 days", "Lead Time", "−55%"), ("22.3%", "Flow Eff.", "+175%"), ("160 hrs", "Wait Time", "−70%"), ("45 hrs", "Process Time", "−55%")]

    add_text(slide, "BEFORE (Current State)",
             Inches(0.45), Inches(1.18), Inches(3.8), Inches(0.28),
             font_size=9, bold=True, color=MID_GRAY)
    add_text(slide, "OPTION B — After",
             Inches(4.45), Inches(1.18), Inches(3.8), Inches(0.28),
             font_size=9, bold=True, color=PURPLE_DARK)

    bx = Inches(0.45)
    for (val, lbl) in before:
        add_stat_box(slide, val, lbl, bx, Inches(1.48), width=Inches(0.88), height=Inches(0.80),
                     value_color=MID_GRAY, bg=LIGHT_GRAY)
        bx += Inches(0.95)

    ax = Inches(4.45)
    for (val, lbl, delta) in after:
        add_rect(slide, ax, Inches(1.48), Inches(0.88), Inches(0.80), PURPLE_LIGHT)
        add_text(slide, val, ax, Inches(1.52), Inches(0.88), Inches(0.42),
                 font_size=17, bold=True, color=PURPLE_DARK, align=PP_ALIGN.CENTER)
        add_text(slide, lbl, ax, Inches(1.88), Inches(0.88), Inches(0.30),
                 font_size=8, color=MID_GRAY, align=PP_ALIGN.CENTER)
        add_text(slide, delta, ax, Inches(2.26), Inches(0.88), Inches(0.22),
                 font_size=8, bold=True, color=GREEN_MED, align=PP_ALIGN.CENTER)
        ax += Inches(0.95)

    add_text(slide, "→", Inches(3.55), Inches(1.72), Inches(0.75), Inches(0.35),
             font_size=22, bold=True, color=PURPLE_DARK, align=PP_ALIGN.CENTER)

    # Role consolidation visual
    add_rect(slide, Inches(0.45), Inches(2.42), Inches(8.25), Inches(0.34), PURPLE_LIGHT)
    add_text(slide,
             "Role consolidation: 8 roles  →  5 roles   |   Product Owner · Tech Lead · Developer · QA Lead · DevOps",
             Inches(0.55), Inches(2.44), Inches(8.05), Inches(0.30),
             font_size=9.5, bold=False, color=PURPLE_DARK)

    actions = [
        ("Select Option B tab", "Click the 'Option B' tab (purple) on the Future State VSM page. Metrics update immediately."),
        ("Read the metric improvements", "Lead Time: 42.5 → 19.1 days (−55%). Flow Efficiency: 8.1% → 22.3% (+175%). Process Time halved. Wait Time reduced 70%."),
        ("Show role consolidation", "Point to the role summary banner: 8 roles consolidate to 5. 'The BA, UX Designer, and separate DevOps specialist roles are absorbed by agents.'"),
        ("Show 7 key AI agents", "FeatureGen · CodeGen · TestGen · AI Test Execution · AI Deployment Agent · AI APM · IncidentAgent. These 7 agents do the work of 3 eliminated roles."),
        ("Compare A vs B", "Use the scenario tabs to toggle A → B side by side. 'Option B delivers 15% more lead time improvement and 75% more flow efficiency gain than Option A, at roughly 1.5× the investment.'"),
    ]

    y = Inches(2.90)
    for i, (title, detail) in enumerate(actions):
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.66), LIGHT_GRAY)
        add_step_circle(slide, i + 1, Inches(0.5), y + Inches(0.15), bg=PURPLE_MED)
        add_text(slide, title, Inches(1.0), y + Inches(0.03), Inches(7.65), Inches(0.24),
                 font_size=10.5, bold=True, color=BLACK)
        add_text(slide, detail, Inches(1.0), y + Inches(0.27), Inches(7.65), Inches(0.34),
                 font_size=9.5, color=DARK_GRAY)
        y += Inches(0.76)

    talking_points_panel(slide, [
        "Option B = the strongest ROI at 3.8×. It eliminates the highest-cost human touch points in the PDLC — manual UAT, test data management, CAB gating — and replaces them with AI agents.",
        "Role consolidation from 8 to 5 is the source of the additional ROI. 3 roles absorbed by agents = $300K–$600K annual saving per product team at enterprise rates.",
        "7 custom AI agents. These are LangGraph agents — the same architecture as this platform. Build time: 4–8 weeks. Stripe deployed equivalent tooling in 8 weeks.",
        "Flow Efficiency 22.3% is approaching world-class territory. Teams at this level compete on delivery speed, not on headcount.",
        "Lead time 19.1 days = 2.5× faster than current state. For software-defined competitive advantages (e.g. banking, insurance, fintech) this is the difference between winning and losing market share.",
        "Option B requires executive sponsorship for the role restructuring. The Business Case (next screen) includes the full org change management plan.",
    ], accent=PURPLE_DARK)


def slide_step6a_biz(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 6A — Business Case: Option A",
                 "2.8× ROI · $800K–$1.5M investment · 14-month payback",
                 badge_text="OPTION A — AI-ASSISTED", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 accent=BLUE_DARK, slide_num=n, total_slides=total)
    screen_label(slide, "/business-case  (select Option A tab)")

    # Financial summary boxes
    fin = [
        ("$800K–$1.5M", "Total Investment", AMBER_MED, AMBER_LIGHT),
        ("$1.3M–$2.0M", "Annual Benefits", GREEN_MED, GREEN_LIGHT),
        ("2.8×",        "ROI Multiple",    BLUE_DARK, BLUE_LIGHT),
        ("14 months",   "Payback Period",  PURPLE_MED, PURPLE_LIGHT),
    ]
    fx = Inches(0.45)
    for (val, lbl, col, bg) in fin:
        add_stat_box(slide, val, lbl, fx, Inches(1.18),
                     width=Inches(1.95), height=Inches(0.88),
                     value_color=col, bg=bg)
        fx += Inches(2.07)

    # Investment breakdown
    add_text(slide, "INVESTMENT BREAKDOWN",
             Inches(0.45), Inches(2.20), Inches(4.0), Inches(0.24),
             font_size=8, bold=True, color=MID_GRAY)
    inv = [
        ("AI Tools & IDE Plugins",        "$250K – $400K"),
        ("Infrastructure (GPU, API costs)","$100K – $200K"),
        ("Implementation & Integration",   "$300K – $600K"),
        ("Training (all PDLC personas)",   "$100K – $200K"),
        ("Change Management",              "$100K – $150K"),
    ]
    y = Inches(2.46)
    for lbl, val in inv:
        add_rect(slide, Inches(0.45), y, Inches(4.05), Inches(0.38), LIGHT_GRAY)
        add_text(slide, lbl, Inches(0.55), y + Inches(0.08), Inches(2.75), Inches(0.24),
                 font_size=9, color=DARK_GRAY)
        add_text(slide, val, Inches(3.3), y + Inches(0.08), Inches(1.15), Inches(0.24),
                 font_size=9, bold=True, color=AMBER_DARK, align=PP_ALIGN.RIGHT)
        y += Inches(0.44)

    # Annual benefits
    add_text(slide, "ANNUAL BENEFITS",
             Inches(4.65), Inches(2.20), Inches(4.0), Inches(0.24),
             font_size=8, bold=True, color=MID_GRAY)
    ben = [
        ("Time-to-Market Improvement", "$600K – $900K"),
        ("Productivity Gains (35% effort↓)", "$400K – $600K"),
        ("Quality Improvement",         "$200K – $300K"),
        ("Operational Savings",         "$100K – $150K"),
    ]
    y = Inches(2.46)
    for lbl, val in ben:
        add_rect(slide, Inches(4.65), y, Inches(4.0), Inches(0.38), GREEN_LIGHT)
        add_text(slide, lbl, Inches(4.75), y + Inches(0.08), Inches(2.6), Inches(0.24),
                 font_size=9, color=DARK_GRAY)
        add_text(slide, val, Inches(7.38), y + Inches(0.08), Inches(1.2), Inches(0.24),
                 font_size=9, bold=True, color=GREEN_DARK, align=PP_ALIGN.RIGHT)
        y += Inches(0.44)

    # Implementation timeline summary
    add_text(slide, "TEAM-LEVEL IMPLEMENTATION:  6–10 WEEKS",
             Inches(0.45), Inches(4.64), Inches(8.25), Inches(0.28),
             font_size=9, bold=True, color=BLUE_DARK)
    timeline = [
        ("Wk 1", "Foundation", "Baseline VSM, procure Copilot, agree AI goals"),
        ("Wk 2–3", "Quick Wins", "ReviewAgent, ML SAST, AI backlog plugin live"),
        ("Wk 3–6", "Core Tools", "AI performance analyzer, APM, IaC agent"),
        ("Wk 6–8", "Embed", "2-day workshop, update DoD, prompt playbook"),
        ("Wk 8–10", "Measure", "Re-run VSM, calculate actual ROI vs 2.8× target"),
    ]
    tx = Inches(0.45)
    for (wk, phase, desc) in timeline:
        add_rect(slide, tx, Inches(4.95), Inches(1.55), Inches(1.82), BLUE_LIGHT)
        add_text(slide, wk, tx + Inches(0.05), Inches(4.98), Inches(1.45), Inches(0.25),
                 font_size=8, bold=True, color=BLUE_DARK)
        add_text(slide, phase, tx + Inches(0.05), Inches(5.22), Inches(1.45), Inches(0.25),
                 font_size=10, bold=True, color=BLUE_DARK)
        add_text(slide, desc, tx + Inches(0.05), Inches(5.48), Inches(1.45), Inches(0.72),
                 font_size=7.5, color=DARK_GRAY)
        tx += Inches(1.64)

    talking_points_panel(slide, [
        "Investment $800K–$1.5M is primarily SaaS tool licences and integration work. No major infrastructure build required for Option A.",
        "14-month payback = within a single financial year's horizon for most organisations. Ask: 'What's your current budget cycle?'",
        "Annual benefit driver #1 is time-to-market: 17 fewer days per feature × feature delivery volume × business value per feature. For a fintech team releasing 20 features/quarter, each day earlier = measurable revenue.",
        "Training cost ($100K–$200K) covers 10–15 people. Industry benchmark: GitHub Copilot enterprise rollout averages $500/developer/year in licence + $2,000/developer in onboarding. ROI positive within 6 weeks.",
        "The implementation timeline is team-level. Enterprise-wide rollout is 12–18 months and is covered in the 'Enterprise Timeline' tab of the Business Case screen.",
        "For the CFO: 'The NPV model underpinning the 2.8× figure uses a 20% discount rate and conservative benefit estimates. We can adjust all assumptions to match your cost structure.'",
    ], accent=BLUE_DARK)


def slide_step6b_biz(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 6B — Business Case: Option B",
                 "3.8× ROI · $1.2M–$2.2M investment · 11-month payback",
                 badge_text="OPTION B — HYBRID AI", badge_bg=PURPLE_LIGHT, badge_fg=PURPLE_DARK,
                 accent=PURPLE_DARK, slide_num=n, total_slides=total)
    screen_label(slide, "/business-case  (select Option B tab)")

    fin = [
        ("$1.2M–$2.2M", "Total Investment", AMBER_MED, AMBER_LIGHT),
        ("$2.0M–$3.2M", "Annual Benefits",  GREEN_MED, GREEN_LIGHT),
        ("3.8×",         "ROI Multiple",    PURPLE_DARK, PURPLE_LIGHT),
        ("11 months",    "Payback Period",  PURPLE_MED, PURPLE_LIGHT),
    ]
    fx = Inches(0.45)
    for (val, lbl, col, bg) in fin:
        add_stat_box(slide, val, lbl, fx, Inches(1.18),
                     width=Inches(1.95), height=Inches(0.88),
                     value_color=col, bg=bg)
        fx += Inches(2.07)

    inv = [
        ("AI Tools & Platforms (selective)", "$400K – $700K"),
        ("Infrastructure (dedicated compute)", "$200K – $350K"),
        ("Custom Agent Development",          "$400K – $800K"),
        ("Training (5 retained roles)",        "$100K – $200K"),
        ("Change Mgmt (role restructuring)",   "$150K – $200K"),
    ]
    add_text(slide, "INVESTMENT BREAKDOWN",
             Inches(0.45), Inches(2.20), Inches(4.0), Inches(0.24),
             font_size=8, bold=True, color=MID_GRAY)
    y = Inches(2.46)
    for lbl, val in inv:
        add_rect(slide, Inches(0.45), y, Inches(4.05), Inches(0.38), LIGHT_GRAY)
        add_text(slide, lbl, Inches(0.55), y + Inches(0.08), Inches(2.75), Inches(0.24),
                 font_size=9, color=DARK_GRAY)
        add_text(slide, val, Inches(3.3), y + Inches(0.08), Inches(1.15), Inches(0.24),
                 font_size=9, bold=True, color=AMBER_DARK, align=PP_ALIGN.RIGHT)
        y += Inches(0.44)

    ben = [
        ("Time-to-Market (55% faster)",     "$900K – $1.4M"),
        ("Productivity (55% effort↓)",       "$600K – $900K"),
        ("Quality (AI quality gates)",       "$300K – $500K"),
        ("Operational Savings (AIOps)",      "$200K – $350K"),
    ]
    add_text(slide, "ANNUAL BENEFITS",
             Inches(4.65), Inches(2.20), Inches(4.0), Inches(0.24),
             font_size=8, bold=True, color=MID_GRAY)
    y = Inches(2.46)
    for lbl, val in ben:
        add_rect(slide, Inches(4.65), y, Inches(4.0), Inches(0.38), GREEN_LIGHT)
        add_text(slide, lbl, Inches(4.75), y + Inches(0.08), Inches(2.6), Inches(0.24),
                 font_size=9, color=DARK_GRAY)
        add_text(slide, val, Inches(7.38), y + Inches(0.08), Inches(1.2), Inches(0.24),
                 font_size=9, bold=True, color=GREEN_DARK, align=PP_ALIGN.RIGHT)
        y += Inches(0.44)

    # Org changes
    add_text(slide, "ORGANISATION CHANGES (OPTION B)",
             Inches(0.45), Inches(4.64), Inches(8.25), Inches(0.28),
             font_size=9, bold=True, color=PURPLE_DARK)
    org_items = [
        "Consolidate 8+ roles to 5 core roles: Product Owner, Tech Lead, Developer, QA Lead, DevOps",
        "Establish AI Agent Operations team to manage and tune agents (new function)",
        "Redesign performance metrics to measure human-AI team output, not individual velocity",
        "Executive sponsorship program required — board visibility for transformation governance",
    ]
    y = Inches(4.95)
    for item in org_items:
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.35), PURPLE_LIGHT)
        add_text(slide, f"  •  {item}", Inches(0.45), y + Inches(0.05), Inches(8.15), Inches(0.28),
                 font_size=9, color=PURPLE_DARK)
        y += Inches(0.40)

    talking_points_panel(slide, [
        "Option B is the strongest ROI at 3.8× — because it eliminates role overhead, not just augments it. 3 roles removed × enterprise labour cost = $300K–$600K annual saving per team.",
        "11-month payback is shorter than Option A despite 50% higher investment — because annual benefits are proportionally much larger.",
        "Custom LangGraph agent development: 4–8 weeks per agent × 7 agents = 12–16 weeks total. Stripe reference: equivalent custom tooling deployed in 8 weeks by a team of 3 engineers.",
        "The 'AI Agent Operations' function is a new role. Typically 1–2 people per product team. They monitor agent output quality, manage prompt updates, and escalate novel failure modes. This is the new DevOps.",
        "Option B requires board-level visibility because it's an operating model change, not a tool purchase. Prepare the exec team for this before the demo if possible.",
        "Compare A vs B on one screen: 'Option A is the right start. Option B is where you want to be in 12 months. The business case gives you both for a board decision.'",
    ], accent=PURPLE_DARK)


def slide_step7_playbook(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Step 7 — Personalised 90-Day Playbook",
                 "AI-generated implementation roadmap specific to your team, stack, and constraints",
                 badge_text="SHARED STEP  (both scenarios)", badge_bg=GREEN_LIGHT, badge_fg=GREEN_DARK,
                 accent=GREEN_MED, slide_num=n, total_slides=total)
    screen_label(slide, "/playbook-context")

    actions = [
        ("Open Playbook Context", "Click 'Playbook' in the sidebar (AI Insights group). The Accuracy Meter starts at 40%."),
        ("Fill Team Profile", "Enter: Team Name, Organisation, Portfolio, Team Size (e.g. 12), Roles (Product Owner, 2× Dev, QA, DevOps, BA, Scrum Master), Seniority: Mixed. Watch accuracy jump to ~55%."),
        ("Fill Technology Stack", "Source Control: GitHub. CI/CD: GitHub Actions. Cloud: AWS. ALM: Jira. Monitoring: Datadog. Testing: Jest + Playwright. AI Licences: GitHub Copilot (if applicable). Accuracy ~67%."),
        ("Add Budget & Timeline", "Select budget tier and procurement complexity. Enter any hard deadline constraint. Accuracy reaches 70%+."),
        ("Click Generate Playbook", "Click the 'Generate Personalised Playbook' button. The AI agent runs and outputs the playbook below (10–15 seconds)."),
        ("Walk the Playbook output", "Show: Executive Summary (team-specific). Sprint Plan (named roles, specific outcomes per sprint). RACI. Risk Register. Target Metrics milestones."),
    ]

    y = Inches(1.18)
    for i, (title, detail) in enumerate(actions):
        add_rect(slide, Inches(0.45), y, Inches(8.25), Inches(0.72), LIGHT_GRAY)
        add_step_circle(slide, i + 1, Inches(0.5), y + Inches(0.17), bg=GREEN_MED)
        add_text(slide, title, Inches(1.0), y + Inches(0.04), Inches(7.65), Inches(0.28),
                 font_size=11, bold=True, color=BLACK)
        add_text(slide, detail, Inches(1.0), y + Inches(0.32), Inches(7.65), Inches(0.34),
                 font_size=9.5, color=DARK_GRAY)
        y += Inches(0.83)

    talking_points_panel(slide, [
        "The accuracy meter is the hook: 'Most transformation decks give you a generic roadmap. This platform generates a roadmap with your team's name, your tools, and your compliance constraints. The meter tells you how personalised the output is.'",
        "At 70%+ accuracy, the playbook is specific enough to hand to a tech lead and say 'execute this.' At 90%+, it's usable in vendor negotiations and board papers.",
        "The sprint plan names who does what: 'Product Owner: review AI-generated feature specs. DevOps Engineer: audit CI/CD pipelines in GitHub Actions. Compliance Officer: map APRA/PCI-DSS requirements to DevSecOps.' Not generic roles — your people.",
        "The RACI covers every human-AI handoff: who owns the decision, who reviews the AI output, who is accountable for quality gates. This is what most AI adoption programs miss.",
        "Closing line: 'The playbook is the answer to the Monday morning question — what do we do first? It removes the implementation risk that kills most transformation programs.'",
        "Final CTA: 'Connect your ALM tool, run the full agent analysis with your real data, and you have a board-ready transformation business case in under 3 hours.'",
    ], accent=GREEN_MED, title="Talking Points")


def slide_objections(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Handling Tough Questions",
                 "Pre-prepared responses to the most common senior leadership objections",
                 badge_text="DEMO PREP", badge_bg=LIGHT_GRAY, badge_fg=DARK_GRAY,
                 accent=DARK_GRAY, slide_num=n, total_slides=total)

    objections = [
        (
            "\"Our engineers won't adopt AI tools\"",
            "Option A requires zero role changes. Adoption is incremental — one tool per phase, starting with GitHub Copilot. The playbook includes a 2-day AI collaboration workshop and change management sprints.",
        ),
        (
            "\"We have APRA / PCI-DSS / ISO 27001 compliance constraints\"",
            "The Business Case DevSecOps tab covers regulatory-aware AI: zero-trust policies, compliance evidence automation, AI-generated audit trails. The playbook compliance section maps your specific framework.",
        ),
        (
            "\"We already have GitHub Copilot\"",
            "Copilot addresses Phase 3 only (coding). Option A adds agents to all 7 phases. Testing alone has 4 critical bottlenecks Copilot doesn't touch — UAT, DAST, DataGen, performance testing.",
        ),
        (
            "\"The ROI numbers seem optimistic\"",
            "Defaults are sourced from DORA 2024, GitHub Octoverse, and Gartner. They are conservative — real Option B deployments (Stripe, GitHub internal) exceeded 4× ROI. All assumptions are adjustable in the model.",
        ),
        (
            "\"How quickly can we get our real data in?\"",
            "Jira or Azure DevOps ALM connection takes under 30 minutes. The system pulls ticket history and auto-computes cycle times. No manual data entry after initial setup.",
        ),
        (
            "\"How is this different from a consultant's deck?\"",
            "A consultant gives you a 200-slide strategy. This platform produces the analysis, the ROI model, the implementation roadmap, and the personalised playbook — live, in 30 minutes, using your actual data.",
        ),
    ]

    cols = [Inches(0.45), Inches(4.65)]
    y_starts = [Inches(1.18), Inches(1.18)]

    for i, (q, a) in enumerate(objections):
        col = cols[i % 2]
        y   = y_starts[i % 2]
        h = Inches(1.05)
        add_rect(slide, col, y, Inches(4.05), h, LIGHT_GRAY)
        add_rect(slide, col, y, Inches(4.05), Inches(0.30), DARK_GRAY)
        add_text(slide, q, col + Inches(0.08), y + Inches(0.04), Inches(3.88), Inches(0.24),
                 font_size=8.5, bold=True, color=WHITE)
        add_text(slide, a, col + Inches(0.08), y + Inches(0.35), Inches(3.88), Inches(0.65),
                 font_size=9, color=DARK_GRAY)
        y_starts[i % 2] += h + Inches(0.14)


def slide_closing(prs, n, total):
    slide = prs.slides.add_slide(blank_layout(prs))
    slide_header(slide, "Closing — The One-Page Narrative",
                 "The 5-sentence story to open or close with",
                 badge_text="DEMO CLOSE", badge_bg=BLUE_LIGHT, badge_fg=BLUE_DARK,
                 accent=BLUE_DARK, slide_num=n, total_slides=total)

    sentences = [
        ("1", "The Problem",
         "Your engineering teams deliver features in 40+ days when world-class teams do it in days — and over 90% of that time isn't development, it's waiting."),
        ("2", "The Diagnosis",
         "This platform connects to your ALM tools, measures where the time actually goes across all 7 PDLC phases, and identifies the critical bottlenecks by name."),
        ("3", "The Solution",
         "AI agents design three future states — Option A (40% automation) to Option C (85%) — each with predicted lead time, flow efficiency, and process time improvements."),
        ("4", "The Business Case",
         "For each option: investment breakdown, annual benefits, ROI multiple, payback period, org change plan, tool roadmap, and sprint-by-sprint implementation plan."),
        ("5", "The Action",
         "A personalised 90-day playbook with your team name, your tools, and your RACI — ready to hand to a tech lead on Monday morning."),
    ]

    y = Inches(1.22)
    for (num, label, text) in sentences:
        add_rect(slide, Inches(0.45), y, Inches(11.5), Inches(0.86), LIGHT_GRAY)
        add_rect(slide, Inches(0.45), y, Inches(0.42), Inches(0.86), BLUE_DARK)
        add_text(slide, num, Inches(0.45), y + Inches(0.15), Inches(0.42), Inches(0.42),
                 font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, label, Inches(0.96), y + Inches(0.06), Inches(2.0), Inches(0.26),
                 font_size=10, bold=True, color=BLUE_DARK)
        add_text(slide, text, Inches(0.96), y + Inches(0.30), Inches(10.9), Inches(0.50),
                 font_size=10.5, color=DARK_GRAY)
        y += Inches(0.98)

    # Three questions
    add_rect(slide, Inches(0.45), y + Inches(0.1), Inches(11.5), Inches(0.28), BLUE_DARK)
    add_text(slide, "  The 3 questions every leader asks — and your answers",
             Inches(0.45), y + Inches(0.1), Inches(11.5), Inches(0.28),
             font_size=9, bold=True, color=WHITE)
    qs = [
        ("\"How quickly can we get real data in?\"",
         "Jira/ADO: under 30 min. Pulls ticket history, computes cycle times automatically."),
        ("\"Is this relevant to our industry?\"",
         "Yes — PDLC model validated in banking, telco, insurance, government. DORA calibration adjusts to your performance band."),
        ("\"What's the first step?\"",
         "Pick one product team. Run full analysis in a 2–3 hour session. Use the output to build the Option A investment proposal."),
    ]
    qx = Inches(0.45)
    qy = y + Inches(0.44)
    for (q, a) in qs:
        add_rect(slide, qx, qy, Inches(3.72), Inches(0.78), BLUE_LIGHT)
        add_text(slide, q, qx + Inches(0.08), qy + Inches(0.04), Inches(3.58), Inches(0.30),
                 font_size=9, bold=True, color=BLUE_DARK)
        add_text(slide, a, qx + Inches(0.08), qy + Inches(0.34), Inches(3.58), Inches(0.40),
                 font_size=8.5, color=DARK_GRAY)
        qx += Inches(3.88)


# ══════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ══════════════════════════════════════════════════════════════════════════

def build():
    prs = prs_new()
    TOTAL = 11

    slide_cover(prs)
    slide_agenda(prs, TOTAL)
    slide_step1_dashboard(prs, 3, TOTAL)
    slide_step2_dora(prs, 4, TOTAL)
    slide_step3_vsm(prs, 5, TOTAL)
    slide_step4_bottlenecks(prs, 6, TOTAL)
    slide_step5a_future(prs, 7, TOTAL)
    slide_step5b_future(prs, 8, TOTAL)
    slide_step6a_biz(prs, 9, TOTAL)
    slide_step6b_biz(prs, 10, TOTAL)
    slide_step7_playbook(prs, 11, TOTAL)
    slide_objections(prs, 12, TOTAL)
    slide_closing(prs, 13, TOTAL)

    out = "/Users/125066/projects/pdlc-vsm-platform/PDLC-VSM-Demo-Guide-Option-A-B.pptx"
    prs.save(out)
    print(f"Saved → {out}")
    return out


if __name__ == "__main__":
    build()
