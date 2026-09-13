"""
STUMP Platform Presentation Builder
White background · Blue shades · Clean typography
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Blue palette ──────────────────────────────────────────────────────────────
B900  = RGBColor(0x1E, 0x3A, 0x8A)   # deep navy-blue  – primary headings
B700  = RGBColor(0x1D, 0x4E, 0xD8)   # strong blue     – accents / icons
B500  = RGBColor(0x3B, 0x82, 0xF6)   # medium blue     – highlights
B300  = RGBColor(0x93, 0xC5, 0xFD)   # soft blue       – borders, dividers
B100  = RGBColor(0xDB, 0xEA, 0xFE)   # pale blue       – card backgrounds
B050  = RGBColor(0xEF, 0xF6, 0xFF)   # near-white blue – slide tints

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DGRAY = RGBColor(0x1F, 0x29, 0x37)   # primary body text
MGRAY = RGBColor(0x6B, 0x72, 0x80)   # secondary text
LGRAY = RGBColor(0xF3, 0xF4, 0xF6)   # light rule / alt rows

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ── Primitive helpers ─────────────────────────────────────────────────────────

def rect(slide, x, y, w, h, fill=None, line_rgb=None, line_w=Pt(0.75)):
    s = slide.shapes.add_shape(1, x, y, w, h)
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line_rgb:
        s.line.color.rgb = line_rgb; s.line.width = line_w
    else:
        s.line.fill.background()
    return s

def tb(slide, text, x, y, w, h,
       size=Pt(11), bold=False, color=DGRAY,
       align=PP_ALIGN.LEFT, italic=False):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf  = box.text_frame
    tf.word_wrap = True
    p   = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size   = size
    r.font.bold   = bold
    r.font.color.rgb = color
    r.font.italic = italic
    return box

def para(tf, text, size=Pt(10.5), bold=False, color=DGRAY,
         align=PP_ALIGN.LEFT, italic=False, space_before=Pt(2)):
    p = tf.add_paragraph()
    p.alignment     = align
    p.space_before  = space_before
    r = p.add_run()
    r.text = text
    r.font.size   = size
    r.font.bold   = bold
    r.font.color.rgb = color
    r.font.italic = italic
    return p

# ── Composite components ──────────────────────────────────────────────────────

def slide_header(slide, title, subtitle=None):
    """White slide with a blue top bar and optional subtitle."""
    rect(slide, 0, 0, W, H, fill=WHITE)
    # top bar
    rect(slide, 0, 0, W, Inches(1.05), fill=B900)
    # left accent stripe
    rect(slide, 0, 0, Inches(0.12), Inches(1.05), fill=B500)
    tb(slide, title,
       Inches(0.28), Inches(0.12), Inches(11), Inches(0.52),
       size=Pt(22), bold=True, color=WHITE)
    if subtitle:
        tb(slide, subtitle,
           Inches(0.28), Inches(0.63), Inches(11), Inches(0.32),
           size=Pt(10.5), color=B300, italic=True)
    # thin bottom rule on bar
    rect(slide, 0, Inches(1.05), W, Inches(0.03), fill=B500)

def slide_footer(slide, page_txt=""):
    rect(slide, 0, H - Inches(0.28), W, Inches(0.28), fill=B050)
    rect(slide, 0, H - Inches(0.28), W, Inches(0.02), fill=B300)
    tb(slide, "STUMP · Strategic Transformation Unified Mapping Platform · © 2026 Cognizant · Confidential",
       Inches(0.28), H - Inches(0.26), Inches(10), Inches(0.24),
       size=Pt(7.5), color=MGRAY)
    if page_txt:
        tb(slide, page_txt,
           Inches(12.5), H - Inches(0.26), Inches(0.7), Inches(0.24),
           size=Pt(7.5), color=MGRAY, align=PP_ALIGN.RIGHT)

def card_box(slide, x, y, w, h, header_text=None, header_color=B900):
    """White card with optional blue header bar."""
    rect(slide, x, y, w, h, fill=WHITE, line_rgb=B300, line_w=Pt(0.75))
    if header_text:
        rect(slide, x, y, w, Inches(0.34), fill=header_color)
        tb(slide, header_text,
           x + Inches(0.14), y + Inches(0.06), w - Inches(0.18), Inches(0.26),
           size=Pt(10), bold=True, color=WHITE)

def bullet_list(slide, items, x, y, w, h,
                size=Pt(10), color=DGRAY, bullet="▸  "):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf  = box.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
            p.space_before = Pt(3)
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = f"{bullet}{item}"
        r.font.size  = size
        r.font.color.rgb = color

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Cover
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, W, H, fill=WHITE)
# left accent panel
rect(sl, 0, 0, Inches(0.55), H, fill=B900)
rect(sl, Inches(0.55), 0, Inches(0.08), H, fill=B500)
# top rule
rect(sl, Inches(0.63), Inches(1.6), W - Inches(0.63), Inches(0.04), fill=B300)
# bottom rule
rect(sl, Inches(0.63), H - Inches(1.05), W - Inches(0.63), Inches(0.04), fill=B300)

tb(sl, "STUMP",
   Inches(0.9), Inches(1.75), Inches(11), Inches(1.3),
   size=Pt(68), bold=True, color=B900)
tb(sl, "Strategic Transformation Unified Mapping Platform",
   Inches(0.9), Inches(2.95), Inches(11.5), Inches(0.5),
   size=Pt(18), bold=False, color=B700)
tb(sl, "AI-Powered PDLC Value Stream Mapping & Digital Transformation Intelligence",
   Inches(0.9), Inches(3.52), Inches(11.5), Inches(0.42),
   size=Pt(13), color=MGRAY, italic=True)

# stat strip
stats_c = [
    ("8",    "AI Agents"),
    ("7",    "PDLC Phases"),
    ("3",    "Future-State Scenarios"),
    ("5.5×", "Max ROI Multiple"),
    ("88%",  "Max WT Reduction"),
]
sw = Inches(2.3)
for i, (val, lbl) in enumerate(stats_c):
    sx = Inches(0.9) + i * (sw + Inches(0.15))
    sy = Inches(4.2)
    rect(sl, sx, sy, sw, Inches(0.88), fill=B050, line_rgb=B300)
    tb(sl, val, sx, sy + Inches(0.05), sw, Inches(0.48),
       size=Pt(26), bold=True, color=B900, align=PP_ALIGN.CENTER)
    tb(sl, lbl, sx, sy + Inches(0.52), sw, Inches(0.3),
       size=Pt(9), color=MGRAY, align=PP_ALIGN.CENTER)

tb(sl, "Cognizant  ·  April 2026  ·  Confidential",
   Inches(0.9), H - Inches(0.9), Inches(6), Inches(0.3),
   size=Pt(10), color=MGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Agenda", "What this deck covers")
slide_footer(sl, "2")

items_ag = [
    ("01", "Platform Objectives",          "Problem, vision and six core capabilities"),
    ("02", "Expected Business Benefits",   "Quantified outcomes across three transformation options"),
    ("03", "Agent Roster & Orchestration", "8 AI agents, pipeline flow and shared state"),
    ("04", "Agent Deep-Dive",              "Objectives, inputs, outputs and logic per agent"),
    ("05", "Functional Architecture",      "Capabilities organised by domain layer"),
    ("06", "Technical Architecture",       "Stack, runtime and integration topology"),
    ("07", "Sequence Diagram",             "End-to-end request / response flow"),
    ("08", "How We Built STUMP",           "Methodology and five-phase build approach"),
    ("09", "Unique Differentiators",       "What makes STUMP stand apart"),
]

cw = Inches(3.92); ch = Inches(1.5); gap = Inches(0.14)
ox = Inches(0.28); oy = Inches(1.2)
for i, (num, ttl, desc) in enumerate(items_ag):
    col = i % 3; row = i // 3
    x = ox + col * (cw + gap)
    y = oy + row * (ch + Inches(0.1))
    rect(sl, x, y, cw, ch, fill=WHITE, line_rgb=B300)
    rect(sl, x, y, Inches(0.42), ch, fill=B900)
    tb(sl, num, x + Inches(0.04), y + Inches(0.55),
       Inches(0.36), Inches(0.38),
       size=Pt(14), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb(sl, ttl, x + Inches(0.52), y + Inches(0.12),
       cw - Inches(0.6), Inches(0.36),
       size=Pt(11), bold=True, color=B900)
    tb(sl, desc, x + Inches(0.52), y + Inches(0.52),
       cw - Inches(0.6), Inches(0.88),
       size=Pt(9.5), color=MGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Platform Objectives
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Platform Objectives", "What STUMP does and the problem it solves")
slide_footer(sl, "3")

# Problem | Vision — side by side
for xi, (lbl, body, bc) in enumerate([
    ("The Problem",
     "Software delivery teams operate with opaque value streams — they cannot see where time is lost, why flow efficiency is low, or which investments will yield the highest transformation ROI.",
     B700),
    ("The Vision",
     "STUMP gives every delivery team an AI-powered transformation co-pilot — mapping the current value stream, diagnosing root-cause bottlenecks and generating a board-ready business case in minutes.",
     B900),
]):
    x = Inches(0.28) + xi * Inches(6.55)
    rect(sl, x, Inches(1.2), Inches(6.35), Inches(1.18), fill=B050, line_rgb=B300)
    rect(sl, x, Inches(1.2), Inches(0.12), Inches(1.18), fill=bc)
    tb(sl, lbl, x + Inches(0.22), Inches(1.24), Inches(6.0), Inches(0.3),
       size=Pt(10.5), bold=True, color=bc)
    tb(sl, body, x + Inches(0.22), Inches(1.56), Inches(6.0), Inches(0.72),
       size=Pt(9.5), color=DGRAY)

# 6 objective cards
objectives = [
    ("Map Current State",
     "Auto-ingest ALM data (Jira / Azure DevOps) and render a live VSM with per-phase process time, wait time and flow efficiency."),
    ("Diagnose Bottlenecks",
     "AI agents identify 12+ bottlenecks, classify Lean waste type and deliver 5-Why root-cause analysis per activity."),
    ("Generate Improvements",
     "Prescribe AI-agent interventions per bottleneck with expected PT / WT reduction, ROI multiples and competitor benchmarks."),
    ("Design Future States",
     "Generate three transformation scenarios — Augmented Human, Hybrid, AI-First — with predicted DORA metrics."),
    ("Build the Business Case",
     "Investment vs. benefit analysis per scenario: $800K – $4.5M investment, 2.8× – 5.5× ROI, 12 – 22-month payback."),
    ("Personalise the Playbook",
     "Sprint-by-sprint implementation roadmap, RACI matrix, risks and quick wins tailored to team tools and context."),
]
ow = Inches(4.12); oh = Inches(1.52); ogap = Inches(0.14)
for i, (ttl, desc) in enumerate(objectives):
    col = i % 3; row = i // 2 if i < 3 else i // 2
    col = i % 3; row = i // 3
    x = Inches(0.28) + col * (ow + ogap)
    y = Inches(2.52) + row * (oh + Inches(0.1))
    rect(sl, x, y, ow, oh, fill=WHITE, line_rgb=B300)
    rect(sl, x, y, ow, Inches(0.32), fill=B700)
    tb(sl, ttl, x + Inches(0.14), y + Inches(0.05),
       ow - Inches(0.18), Inches(0.26),
       size=Pt(10), bold=True, color=WHITE)
    tb(sl, desc, x + Inches(0.14), y + Inches(0.38),
       ow - Inches(0.22), Inches(1.06),
       size=Pt(9.5), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Business Benefits
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Expected Business Benefits", "Quantified outcomes across three transformation options")
slide_footer(sl, "4")

# Column headers
cols_hdr = ["Metric", "Option A — Augmented Human", "Option B — Hybrid", "Option C — AI-First"]
col_w_list = [Inches(3.0), Inches(3.3), Inches(3.3), Inches(3.3)]
hx = [Inches(0.28), Inches(3.28), Inches(6.58), Inches(9.88)]
hy = Inches(1.22)
rect(sl, Inches(0.28), hy, sum(col_w_list) + Inches(0.0), Inches(0.4), fill=B900)
for x, cw2, lbl in zip(hx, col_w_list, cols_hdr):
    tb(sl, lbl, x + Inches(0.12), hy + Inches(0.08),
       cw2 - Inches(0.14), Inches(0.28),
       size=Pt(10), bold=True, color=WHITE)

rows_data = [
    ("Automation Level",          "40 %",               "65 %",               "85 %"),
    ("Lead Time Reduction",       "35 %",               "55 %",               "70 %"),
    ("Wait Time Reduction",       "55 %",               "72 %",               "88 %"),
    ("Flow Efficiency Gain",      "+ 20 – 25 pts",      "+ 30 – 40 pts",      "+ 45 – 55 pts"),
    ("Deployment Frequency",      "Weekly",             "Daily",              "Multiple / day"),
    ("Change Failure Rate",       "5 – 10 %",           "< 5 %",              "< 5 %"),
    ("AI Agents Deployed",        "16 agents",          "12 agents",          "22 agents"),
    ("Investment Range",          "$800K – $1.5M",      "$1.5M – $3M",        "$2.5M – $4.5M"),
    ("ROI Multiple",              "2.8 ×",              "4.2 ×",              "5.5 ×"),
    ("Payback Period",            "12 – 14 months",     "14 – 16 months",     "18 – 22 months"),
    ("Roles Affected",            "8 personas (assist)","5 core roles",       "2 strategic roles"),
]
row_h = Inches(0.44)
for ri, (metric, a, b, c) in enumerate(rows_data):
    ry = hy + Inches(0.4) + ri * row_h
    bg = WHITE if ri % 2 == 0 else B050
    rect(sl, Inches(0.28), ry, Inches(13.05), row_h, fill=bg, line_rgb=B100)
    for xi, val in zip(hx, [metric, a, b, c]):
        bold_ = (xi == hx[0])
        color_ = B900 if bold_ else DGRAY
        tb(sl, val, xi + Inches(0.12), ry + Inches(0.1),
           Inches(3.0), Inches(0.3),
           size=Pt(10), bold=bold_, color=color_)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Agent Roster & Orchestration
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Agent Roster & Orchestration Pipeline",
             "8 AI agents in a sequential LangGraph state machine")
slide_footer(sl, "5")

agents_info = [
    ("1", "ALM\nConnector",     "Ingest",   B900),
    ("2", "VSM\nAnalyzer",      "Analyse",  B700),
    ("3", "Benchmark\nAgent",   "Compare",  RGBColor(0x06,0x5F,0x46)),
    ("4", "Bottleneck\nAnalyzer","Diagnose", RGBColor(0xB4,0x5A,0x09)),
    ("5", "Improvement\nGenerator","Prescribe",RGBColor(0x4C,0x1D,0x95)),
    ("6", "Future State\nDesigner","Design", RGBColor(0x0E,0x47,0x8A)),
    ("7", "Business Case\nBuilder","Justify",RGBColor(0x7C,0x2D,0x12)),
    ("8", "Playbook\nContextualizer","Activate",RGBColor(0x06,0x4E,0x3B)),
]

bw = Inches(1.38); bh = Inches(1.52)
total_w = len(agents_info) * bw + (len(agents_info) - 1) * Inches(0.1)
start_x = (W - total_w) / 2
ay = Inches(1.35)

for i, (num, name, role, col_) in enumerate(agents_info):
    x = start_x + i * (bw + Inches(0.1))
    rect(sl, x, ay, bw, bh, fill=B050, line_rgb=B300)
    rect(sl, x, ay, bw, Inches(0.3), fill=col_)
    tb(sl, num, x + Inches(0.06), ay + Inches(0.04),
       Inches(0.24), Inches(0.24), size=Pt(8), bold=True, color=WHITE)
    tb(sl, name, x, ay + Inches(0.34), bw, Inches(0.72),
       size=Pt(10.5), bold=True, color=B900, align=PP_ALIGN.CENTER)
    rect(sl, x, ay + bh - Inches(0.28), bw, Inches(0.28), fill=col_)
    tb(sl, role, x, ay + bh - Inches(0.26), bw, Inches(0.24),
       size=Pt(8.5), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    if i < len(agents_info) - 1:
        ax_ = x + bw + Inches(0.01)
        tb(sl, "→", ax_, ay + Inches(0.55), Inches(0.1), Inches(0.36),
           size=Pt(14), bold=True, color=B500, align=PP_ALIGN.CENTER)

# Shared state bar
sy = Inches(3.0)
rect(sl, Inches(0.28), sy, W - Inches(0.56), Inches(0.34), fill=B900)
tb(sl, "Shared  VSMAgentState  { project_id  ·  alm_raw_data  ·  vsm_data  ·  metrics  ·  benchmarks  ·  bottlenecks  ·  improvements  ·  future_states  ·  business_cases  ·  status }",
   Inches(0.42), sy + Inches(0.05), W - Inches(0.84), Inches(0.26),
   size=Pt(8.5), bold=True, color=B300, align=PP_ALIGN.CENTER)

# 8 summary cards
summaries = [
    "Fetches Jira / Azure DevOps work items; maps to VSM phase metrics (PT, WT, LT, FE).",
    "Aggregates lean metrics; computes flow efficiency; applies DORA calibration overrides.",
    "Compares current state to DORA Elite, Gartner 2024 and industry P50 / P90 targets.",
    "Identifies 12+ bottlenecks with Lean waste classification and 5-Why root-cause evidence.",
    "Prescribes AI-agent interventions per bottleneck with ROI multiple and time-to-value.",
    "Generates 3 scenarios (40 % / 65 % / 85 % automation) with predicted DORA metrics.",
    "Produces investment vs. benefit analysis: $800K – $4.5M investment, 2.8× – 5.5× ROI.",
    "Builds sprint-by-sprint roadmap, RACI, risks and quick wins tailored to team context.",
]
sw2 = Inches(3.12); sh2 = Inches(1.16); sgap = Inches(0.1)
sy2 = Inches(3.48)
for i, desc in enumerate(summaries):
    col_ = i % 4; row_ = i // 4
    x = Inches(0.28) + col_ * (sw2 + sgap)
    y = sy2 + row_ * (sh2 + Inches(0.08))
    rect(sl, x, y, sw2, sh2, fill=WHITE, line_rgb=B300)
    rect(sl, x, y, sw2, Inches(0.3), fill=agents_info[i][3])
    tb(sl, f"{i+1}.  {agents_info[i][1].replace(chr(10), ' ')}",
       x + Inches(0.1), y + Inches(0.04), sw2 - Inches(0.14), Inches(0.26),
       size=Pt(8.5), bold=True, color=WHITE)
    tb(sl, desc, x + Inches(0.1), y + Inches(0.34),
       sw2 - Inches(0.16), Inches(0.76),
       size=Pt(8.5), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDES 6–13 — Agent Deep-Dive (one per agent)
# ═══════════════════════════════════════════════════════════════════════════════
agent_details = [
    {
        "num": "01", "name": "ALM Connector Agent",
        "color": B900,
        "objective": "Bridge ALM tools (Jira, Azure DevOps) to the VSM pipeline by fetching work-item cycle data and mapping it to 7 PDLC phases with per-phase lean metrics.",
        "inputs":  [
            "Project metadata — organisation, team, product name",
            "ALM config — {tool, URL, credentials}",
            "User-defined PT / WT overrides for manual calibration",
        ],
        "logic": [
            "Authenticates to Jira or Azure DevOps; deterministic sample data fallback",
            "Maps work items to 7 PDLC phase buckets using status / label rules",
            "Computes per-phase PT, WT, LT, FE from issue cycle times",
            "Applies user overrides before passing state downstream",
        ],
        "outputs": [
            "alm_raw_data — raw work items per phase",
            "vsm_data — { phases[ { phase_id, PT, WT, LT, FE, activities } ] }",
        ],
    },
    {
        "num": "02", "name": "VSM Analyzer Agent",
        "color": B700,
        "objective": "Compute aggregate lean VSM metrics from mapped phase data and apply DORA calibration to align theoretical metrics with measured delivery telemetry.",
        "inputs":  [
            "vsm_data — from ALM Connector",
            "dora_calibration — { code review wait, build duration, deploy wait, ops wait }",
        ],
        "logic": [
            "Aggregates PT / WT / LT across all 7 phases",
            "Calculates overall flow efficiency = PT ÷ (PT + WT) × 100",
            "Adjusts per-phase wait times using measured DORA values",
            "Estimates deployment frequency and CFR from VSM patterns",
            "LLM or rule-based narrative assessment of current state",
        ],
        "outputs": [
            "metrics — { total_PT, total_WT, total_LT_days, flow_efficiency, deploy_freq, CFR, MTTR }",
            "narrative — prose assessment of current-state performance",
        ],
    },
    {
        "num": "03", "name": "Benchmark Agent",
        "color": RGBColor(0x06,0x5F,0x46),
        "objective": "Load DORA Elite, Gartner 2024 and Lean VSM industry benchmarks and compute per-phase and overall performance gaps to prioritise improvement focus.",
        "inputs":  [
            "metrics — from VSM Analyzer",
        ],
        "logic": [
            "Hardcoded benchmark library — DORA Elite targets, Lean VSM P50 / P90, Gartner competitor data",
            "Computes gap between current and benchmark per phase (FE%, WT hours)",
            "Identifies phases furthest from industry targets for downstream prioritisation",
            "Provides overall LT target, competitor Q1 and DORA Elite reference points",
        ],
        "outputs": [
            "benchmarks — { phases { phase_id: { current_PT, benchmark_PT_p50, gap_FE_pct, gap_WT_hrs } } }",
            "benchmarks — { overall: { current_LT, target_LT, competitor_Q1, DORA_Elite } }",
        ],
    },
    {
        "num": "04", "name": "Bottleneck Analyzer Agent",
        "color": RGBColor(0xB4,0x5A,0x09),
        "objective": "Identify and enrich every flow bottleneck with Lean waste classification, 5-Why root causes, quantified business impact and linked improvements.",
        "inputs":  [
            "vsm_data — mapped VSM from ALM Connector",
            "benchmarks — industry benchmark gaps",
        ],
        "logic": [
            "Severity thresholds — WT ≥ 16h = Critical; WT > benchmark × 1.5 = High",
            "15+ pre-enriched PDLC activities with curated root causes and FE impact",
            "LLM deep-dives unknown activities via 5-Why chain-of-thought prompting",
            "Each bottleneck links to ≥ 1 downstream improvement recommendation",
        ],
        "outputs": [
            "bottlenecks — list of 12+ objects { id, phase, activity, severity, wasteType }",
            "Each bottleneck includes: rootCauses[5], businessImpact (quantified), feImpact, linkedImprovements",
        ],
    },
    {
        "num": "05", "name": "Improvement Generator Agent",
        "color": RGBColor(0x4C,0x1D,0x95),
        "objective": "Prescribe targeted AI-agent interventions for each bottleneck with expected PT / WT reductions, ROI multiples, implementation timelines and competitor evidence.",
        "inputs":  [
            "bottlenecks — enriched bottleneck list",
        ],
        "logic": [
            "15+ pre-catalogued interventions — FeatureGen, ReviewAgent, AI UAT, Release Manager, Incident Triage …",
            "ROI range 2.5× – 5.0× (ReviewAgent highest at 5.0×); time-to-value 2 – 8 weeks",
            "Competitor evidence — Meta, Netflix, Google measured outcomes cited per intervention",
            "LLM generates interventions for bottlenecks not in catalogue",
        ],
        "outputs": [
            "improvements — { id, agent, type, expectedPTReduction%, expectedWTReduction% }",
            "Each improvement includes: timeToValue, ROI, effort, bestPractices, competitorInsight",
        ],
    },
    {
        "num": "06", "name": "Future State Designer Agent",
        "color": RGBColor(0x0E,0x47,0x8A),
        "objective": "Generate three distinct future-state VSM scenarios representing progressive levels of AI automation across the full PDLC lifecycle.",
        "inputs":  [
            "metrics — current-state lean metrics",
        ],
        "logic": [
            "Option A — 40 % automation: 35 % PT / 55 % WT reduction, 16 agents, weekly deploy",
            "Option B — 65 % automation: 55 % PT / 72 % WT reduction, 12 agents, daily deploy",
            "Option C — 85 % automation: 70 % PT / 88 % WT reduction, 22 agents, multiple / day",
            "Testing phase (Phase 5) receives 1.2× WT bonus — largest bottleneck focus",
            "LLM generates inspiring scenario narratives when credentials available",
        ],
        "outputs": [
            "future_states — { option-a, option-b, option-c } with per-phase predicted metrics",
            "Each option includes DORA targets, automation level, org structure and agent count",
        ],
    },
    {
        "num": "07", "name": "Business Case Builder Agent",
        "color": RGBColor(0x7C,0x2D,0x12),
        "objective": "Produce a board-ready investment vs. benefit analysis for each future-state scenario with org, tooling, DevSecOps and AIOps change plans.",
        "inputs":  [
            "future_states — three scenario definitions",
        ],
        "logic": [
            "Investment breakdown — tools + infra + implementation + training + change management",
            "Annual benefits — TTM improvement + productivity + quality + operational savings",
            "ROI 2.8× (A) → 4.2× (B) → 5.5× (C); payback 12 – 22 months",
            "Enumerates org restructuring, AIOps and product-centric WoW changes per scenario",
        ],
        "outputs": [
            "business_cases — { option-a/b/c: investment, annual_benefits, ROI, payback_months }",
            "Each case includes: org_changes, tool_changes, devsecops_changes, aiops_changes, product_centric_changes",
        ],
    },
    {
        "num": "08", "name": "Playbook Contextualizer Agent",
        "color": RGBColor(0x06,0x4E,0x3B),
        "objective": "Generate a personalised, sprint-level implementation playbook grounded in the team's actual tools, roles, methodology and compliance constraints.",
        "inputs":  [
            "scenario_id — option-a / b / c",
            "team_context — { team_size, roles, tools, methodology, sprint_length, compliance }",
            "analysis_context — full pipeline results",
            "uploaded documents — org chart, OKRs, DORA report, engineering standards",
        ],
        "logic": [
            "References team's actual tool names (Jira, GitHub, CircleCI) in every action step",
            "Sizes effort estimates to team size; adapts cadence to team methodology",
            "Generates compliance-specific steps when frameworks (PCI, SOX, HIPAA) are provided",
            "Accuracy score (0 – 95 %) quantifies confidence based on context completeness",
        ],
        "outputs": [
            "playbook — { executive_summary, duration, sprint_plan[ sprint → actions → outcomes ] }",
            "Includes: target_metrics, RACI matrix, risks, quick_wins, document_gaps",
        ],
    },
]

for pg, ad in enumerate(agent_details, start=6):
    sl = prs.slides.add_slide(BLANK)
    slide_header(sl, f"Agent {ad['num']}  —  {ad['name']}", "Agent Deep-Dive")
    slide_footer(sl, str(pg))

    # Objective banner
    rect(sl, Inches(0.28), Inches(1.12), W - Inches(0.56), Inches(0.76), fill=B050, line_rgb=B300)
    rect(sl, Inches(0.28), Inches(1.12), Inches(0.1), Inches(0.76), fill=ad["color"])
    tb(sl, "Objective", Inches(0.48), Inches(1.15), Inches(1.8), Inches(0.26),
       size=Pt(9), bold=True, color=ad["color"])
    tb(sl, ad["objective"], Inches(0.48), Inches(1.42), W - Inches(0.85), Inches(0.4),
       size=Pt(10), color=DGRAY)

    # Three columns
    sections = [
        ("Inputs",                        ad["inputs"],  B900),
        ("Key Logic & Design Decisions",  ad["logic"],   B700),
        ("Outputs",                       ad["outputs"], RGBColor(0x06,0x5F,0x46)),
    ]
    cw3 = Inches(4.1); ch3 = Inches(4.5); gy3 = Inches(2.0)
    for ci, (hdr, items, hc) in enumerate(sections):
        x = Inches(0.28) + ci * (cw3 + Inches(0.14))
        rect(sl, x, gy3, cw3, ch3, fill=WHITE, line_rgb=B300)
        rect(sl, x, gy3, cw3, Inches(0.34), fill=hc)
        tb(sl, hdr, x + Inches(0.14), gy3 + Inches(0.07),
           cw3 - Inches(0.18), Inches(0.26),
           size=Pt(10), bold=True, color=WHITE)
        for bi, item in enumerate(items):
            iy = gy3 + Inches(0.46) + bi * Inches(0.8)
            rect(sl, x + Inches(0.14), iy + Inches(0.08),
                 Inches(0.06), Inches(0.06), fill=hc)
            tb(sl, item, x + Inches(0.26), iy,
               cw3 - Inches(0.36), Inches(0.76),
               size=Pt(9.5), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — Functional Architecture
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Functional Architecture", "Capabilities organised by domain layer")
slide_footer(sl, "14")

layers_func = [
    ("Presentation",    B900, [
        "Dashboard  ·  ALM Connect  ·  DORA Assessment  ·  DevOps Maturity  ·  VSM Editor",
        "Current State VSM  ·  Bottleneck Analysis  ·  Improvements  ·  Operations Intelligence",
        "Future State  ·  Business Case  ·  Transformation Readiness  ·  Governance",
        "AI Agents Monitor  ·  Playbook  ·  Accuracy & RAG  ·  AI Assurance  ·  Settings",
    ]),
    ("Orchestration",   B700, [
        "LangGraph multi-agent pipeline — 8 sequential agents sharing VSMAgentState",
        "APScheduler — scheduled weekly VSM runs with persistent configuration",
        "Background task execution — async FastAPI + SQLAlchemy non-blocking I/O",
        "Rule-based fallbacks — full capability without LLM credentials",
    ]),
    ("AI / ML Services",RGBColor(0x06,0x5F,0x46), [
        "Azure OpenAI GPT-4o / OpenAI API — narrative generation, 5-Why analysis, playbook enrichment",
        "Pre-built intelligence library — 15+ PDLC activity enrichments, benchmark and ROI catalogues",
        "DORA calibration engine — aligns theoretical VSM metrics to measured DORA values",
        "Accuracy feedback loop — user calibration scores to tune analysis confidence",
    ]),
    ("Integration",     RGBColor(0xB4,0x5A,0x09), [
        "Jira REST API  ·  Azure DevOps REST API — work item ingestion and cycle time extraction",
        "GitHub / GitLab — PR metrics and commit frequency for DevOps maturity scoring",
        "SonarQube — code quality and security scan result ingestion",
        "Excel / XLSX export — bottlenecks, improvements and playbook reports",
    ]),
    ("Data",            MGRAY, [
        "SQLite async (aiosqlite) — Projects, VSM Snapshots, Analysis Runs, DevOps Assessments",
        "PlatformSettings — key/value store for LLM credentials and schedule configuration",
        "ScheduledPipelineRuns — full audit trail of automated analysis executions",
        "AnalysisRun — complete JSON result blob persisted per pipeline execution",
    ]),
]

lh2 = Inches(1.05); ly2 = Inches(1.2)
for li, (lbl, col_, items) in enumerate(layers_func):
    y = ly2 + li * (lh2 + Inches(0.06))
    rect(sl, Inches(0.28), y, W - Inches(0.56), lh2,
         fill=WHITE, line_rgb=B100)
    rect(sl, Inches(0.28), y, Inches(0.1), lh2, fill=col_)
    tb(sl, lbl, Inches(0.44), y + Inches(0.32),
       Inches(1.55), Inches(0.32),
       size=Pt(10), bold=True, color=col_)
    for ii, item in enumerate(items):
        col2 = ii % 2; row2 = ii // 2
        ix = Inches(2.1) + col2 * Inches(5.4)
        iy = y + Inches(0.08) + row2 * Inches(0.46)
        tb(sl, f"•  {item}", ix, iy, Inches(5.3), Inches(0.44),
           size=Pt(9), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — Technical Architecture
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Technical Architecture", "Stack, runtime and integration topology")
slide_footer(sl, "15")

cols_tech = [
    ("Frontend",           B900, [
        ("Framework",   "React 18  +  Vite 5"),
        ("Routing",     "React Router 6"),
        ("Styling",     "Tailwind CSS 3  ·  Inter"),
        ("Charts",      "Recharts 2  ·  Chart.js"),
        ("HTTP client", "Axios"),
        ("Icons",       "Lucide React"),
        ("Export",      "XLSX  ·  jsPDF"),
        ("State",       "React Context API"),
        ("Dev port",    ":3001  (Vite HMR)"),
    ]),
    ("Backend API",        B700, [
        ("Framework",   "FastAPI 0.115  (async)"),
        ("ORM",         "SQLAlchemy 2.0  +  aiosqlite"),
        ("Validation",  "Pydantic v2"),
        ("AI pipeline", "LangGraph 0.2  +  LangChain 0.3"),
        ("LLM client",  "LangChain-OpenAI 0.2"),
        ("Scheduler",   "APScheduler 3.x"),
        ("ALM clients", "Jira SDK  ·  httpx"),
        ("Data tools",  "pandas  ·  openpyxl"),
        ("API port",    ":8001  ·  CORS → :3001"),
    ]),
    ("Infrastructure & Data", RGBColor(0x06,0x5F,0x46), [
        ("Database",    "SQLite  (file-based)"),
        ("Async I/O",   "Python asyncio  +  uvicorn"),
        ("LLM",         "Azure OpenAI GPT-4o  (optional)"),
        ("ALM",         "Jira Cloud  ·  Azure DevOps"),
        ("SCM",         "GitHub / GitLab"),
        ("Quality",     "SonarQube REST API"),
        ("Scheduling",  "APScheduler in-process"),
        ("Runtime",     "Python 3.13  ·  venv"),
        ("Deploy",      "Local dev  ·  Docker-ready"),
    ]),
]

cw4 = Inches(4.1); ch4 = Inches(5.62); gy4 = Inches(1.2)
for ci, (ttl, col_, rows_) in enumerate(cols_tech):
    x = Inches(0.28) + ci * (cw4 + Inches(0.14))
    rect(sl, x, gy4, cw4, ch4, fill=WHITE, line_rgb=B300)
    rect(sl, x, gy4, cw4, Inches(0.36), fill=col_)
    tb(sl, ttl, x + Inches(0.14), gy4 + Inches(0.08),
       cw4, Inches(0.26), size=Pt(11), bold=True, color=WHITE)
    for ri, (k, v) in enumerate(rows_):
        ry = gy4 + Inches(0.46) + ri * Inches(0.57)
        bg2 = WHITE if ri % 2 == 0 else B050
        rect(sl, x + Inches(0.08), ry, cw4 - Inches(0.16), Inches(0.52), fill=bg2)
        tb(sl, k, x + Inches(0.14), ry + Inches(0.1),
           Inches(1.2), Inches(0.32),
           size=Pt(9), bold=True, color=col_)
        tb(sl, v, x + Inches(1.38), ry + Inches(0.1),
           Inches(2.62), Inches(0.32),
           size=Pt(9), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — Sequence Diagram
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Sequence Diagram", "End-to-end request / response flow — single analysis run")
slide_footer(sl, "16")

actors_seq = ["User\n(Browser)", "React\nFrontend", "FastAPI\nBackend",
              "LangGraph\nOrchestrator", "ALM\n(Jira / ADO)",
              "OpenAI\nGPT-4o", "SQLite\nDB"]
actor_colors_seq = [B900, B700, B500,
                    RGBColor(0x4C,0x1D,0x95), RGBColor(0xB4,0x5A,0x09),
                    RGBColor(0x06,0x5F,0x46), MGRAY]
abw = Inches(1.54); abh = Inches(0.44)
spacing = (W - Inches(0.56) - len(actors_seq) * abw) / (len(actors_seq) - 1)
actor_cx = [Inches(0.28) + i * (abw + spacing) for i in range(len(actors_seq))]
top_y_seq = Inches(1.18)

for x, lbl, col_ in zip(actor_cx, actors_seq, actor_colors_seq):
    rect(sl, x, top_y_seq, abw, abh, fill=col_)
    tb(sl, lbl, x, top_y_seq + Inches(0.03), abw, abh,
       size=Pt(7.5), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    cx = x + abw / 2
    rect(sl, cx - Inches(0.01), top_y_seq + abh,
         Inches(0.02), Inches(5.0), fill=B100)

steps_seq = [
    (0, 1, "Configure project + ALM credentials",             Inches(1.78), False),
    (1, 2, "POST /api/v1/agents/{id}/run",                    Inches(2.1),  False),
    (2, 3, "run_full_analysis(project, alm_config)",          Inches(2.42), False),
    (3, 4, "fetch_work_items()",                              Inches(2.74), False),
    (4, 3, "← raw work items (Jira / ADO)",                   Inches(3.06), True),
    (3, 3, "vsm_analyzer  →  benchmark_agent  →  bottleneck_analyzer", Inches(3.38), False),
    (3, 5, "enrich_bottlenecks(5-Why prompt)",                Inches(3.7),  False),
    (5, 3, "← root causes + narratives",                      Inches(4.02), True),
    (3, 3, "improvement_generator  →  future_state  →  business_case", Inches(4.34), False),
    (3, 5, "playbook_contextualizer(team_context)",           Inches(4.66), False),
    (5, 3, "← sprint plan, RACI, quick wins",                 Inches(4.98), True),
    (3, 6, "persist AnalysisRun result",                      Inches(5.3),  False),
    (2, 1, "200 OK  +  run_id",                               Inches(5.62), True),
    (1, 0, "Render dashboard, bottlenecks, improvements",     Inches(5.94), True),
]

for frm, to, lbl, y, is_ret in steps_seq:
    x1 = actor_cx[frm] + abw / 2
    x2 = actor_cx[to]  + abw / 2
    col_arrow = MGRAY if is_ret else B700
    if x1 != x2:
        rect(sl, min(x1,x2), y, abs(x2-x1), Inches(0.018), fill=col_arrow)
        head = "◀" if x2 < x1 else "▶"
        hx = (x2 - Inches(0.1)) if x2 > x1 else (x2 + Inches(0.01))
        tb(sl, head, hx, y - Inches(0.07), Inches(0.14), Inches(0.16),
           size=Pt(7), color=col_arrow, align=PP_ALIGN.CENTER)
    mid = (min(x1,x2) + max(x1,x2)) / 2
    tb(sl, lbl, mid - Inches(0.9), y - Inches(0.22), Inches(1.8), Inches(0.2),
       size=Pt(7.5), color=col_arrow, italic=is_ret, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — How We Built STUMP
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "How We Built STUMP",
             "Design philosophy, architecture decisions and five-phase build approach")
slide_footer(sl, "17")

phases_build = [
    ("Phase 1", "Foundation",
     B900, [
         "FastAPI skeleton + SQLAlchemy async models",
         "VSMAgentState TypedDict — shared pipeline contract",
         "LangGraph graph compilation + health endpoint",
         "React + Vite scaffold with Tailwind design system",
     ]),
    ("Phase 2", "Data & ALM",
     B700, [
         "ALM Connector Agent — Jira + Azure DevOps clients",
         "VSM Editor — manual override UI for PT / WT",
         "DORA Assessment — calibration form + DB persistence",
         "VSM Snapshot storage — JSON blobs in SQLite",
     ]),
    ("Phase 3", "Intelligence",
     RGBColor(0x4C,0x1D,0x95), [
         "Benchmark library — DORA Elite, Gartner, Lean P50 / P90",
         "15+ pre-enriched bottleneck catalogue (curated knowledge)",
         "Improvement catalogue — 15 AI agent prescriptions + ROI",
         "LLM enrichment — LangChain-OpenAI for unknown activities",
     ]),
    ("Phase 4", "Transformation",
     RGBColor(0x06,0x5F,0x46), [
         "Future State Designer — 3 scenario generator + DORA targets",
         "Business Case Builder — investment vs. benefit model",
         "Playbook Contextualizer — team-personalised sprint planner",
         "Transformation Readiness — org change impact assessment",
     ]),
    ("Phase 5", "Productisation",
     RGBColor(0xB4,0x5A,0x09), [
         "APScheduler — automated weekly VSM pipeline",
         "DevOps Maturity — 73-question 4-dimension scoring agent",
         "Accuracy feedback loop — user calibration → confidence score",
         "Governance + AI Assurance — RACI, model cards, fairness",
     ]),
]

bw3 = Inches(2.46); bh3 = Inches(5.0); gy5 = Inches(1.2)
for i, (ph, ttl, col_, bullets) in enumerate(phases_build):
    x = Inches(0.28) + i * (bw3 + Inches(0.1))
    rect(sl, x, gy5, bw3, bh3, fill=WHITE, line_rgb=B300)
    rect(sl, x, gy5, bw3, Inches(0.54), fill=col_)
    tb(sl, ph, x + Inches(0.12), gy5 + Inches(0.06),
       bw3 - Inches(0.18), Inches(0.2),
       size=Pt(8.5), bold=True, color=WHITE)
    tb(sl, ttl, x + Inches(0.12), gy5 + Inches(0.26),
       bw3 - Inches(0.18), Inches(0.24),
       size=Pt(11), bold=True, color=WHITE)
    for bi, b in enumerate(bullets):
        by = gy5 + Inches(0.66) + bi * Inches(1.06)
        rect(sl, x + Inches(0.14), by + Inches(0.1),
             Inches(0.07), Inches(0.07), fill=col_)
        tb(sl, b, x + Inches(0.28), by,
           bw3 - Inches(0.38), Inches(1.0),
           size=Pt(9.5), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 18 — Unique Differentiators
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Unique Differentiators",
             "What makes STUMP stand apart from generic VSM tools")
slide_footer(sl, "18")

diffs = [
    ("01", "Pre-Computed Intelligence Library",
     "15+ PDLC activities carry curated root causes, quantified business impact, competitor benchmarks and ROI — zero LLM cost for known bottlenecks. Competitors surface generic waste; STUMP delivers board-ready evidence.",
     B900),
    ("02", "Three Automation Scenarios in One Run",
     "A single pipeline produces three coherent future states — Augmented Human (40 %), Hybrid (65 %), AI-First (85 %) — each with its own DORA targets, investment model and org restructuring plan.",
     B700),
    ("03", "DORA ↔ VSM Calibration Loop",
     "Unique calibration engine connects measured DORA metrics to VSM phase wait times, making the analysis accurate even before manual data entry. Bridges the gap between Lean VSM theory and real delivery telemetry.",
     RGBColor(0x06,0x5F,0x46)),
    ("04", "Team-Personalised Implementation Playbook",
     "Playbook Contextualizer uses the team's actual Jira project names, GitHub branches and CI/CD steps — not generic advice — with accuracy scored 0 – 95 % based on context completeness.",
     RGBColor(0x4C,0x1D,0x95)),
    ("05", "Hybrid AI Architecture",
     "LLM enrichment for novel bottlenecks; deterministic pre-built library for known ones. Full offline capability — 80 % of analyses require zero LLM calls. Accuracy score tells stakeholders exactly when to trust AI outputs.",
     RGBColor(0xB4,0x5A,0x09)),
    ("06", "End-to-End Transformation OS",
     "Ingestion → diagnosis → improvement → scenario design → business case → playbook → governance → AI assurance in a single platform, replacing 6 – 8 point solutions typically used across a transformation programme.",
     RGBColor(0x0E,0x47,0x8A)),
]

dw = Inches(6.14); dh = Inches(1.72); dgap = Inches(0.12)
for i, (num, ttl, desc, col_) in enumerate(diffs):
    row_ = i // 2; ci = i % 2
    x = Inches(0.28) + ci * (dw + dgap)
    y = Inches(1.2) + row_ * (dh + Inches(0.08))
    rect(sl, x, y, dw, dh, fill=WHITE, line_rgb=B300)
    rect(sl, x, y, dw, Inches(0.34), fill=col_)
    # number badge
    rect(sl, x + Inches(0.14), y + Inches(0.44),
         Inches(0.36), Inches(0.36), fill=B050, line_rgb=col_)
    tb(sl, num, x + Inches(0.14), y + Inches(0.44), Inches(0.36), Inches(0.36),
       size=Pt(9), bold=True, color=col_, align=PP_ALIGN.CENTER)
    tb(sl, ttl, x + Inches(0.14), y + Inches(0.06),
       dw - Inches(0.22), Inches(0.26),
       size=Pt(10.5), bold=True, color=WHITE)
    tb(sl, desc, x + Inches(0.58), y + Inches(0.42),
       dw - Inches(0.7), Inches(1.22),
       size=Pt(9.5), color=DGRAY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 19 — Closing
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
rect(sl, 0, 0, W, H, fill=WHITE)
rect(sl, 0, 0, Inches(0.1), H, fill=B900)
rect(sl, Inches(0.1), 0, Inches(0.06), H, fill=B500)
rect(sl, Inches(0.16), Inches(1.6), W - Inches(0.16), Inches(0.04), fill=B300)
rect(sl, Inches(0.16), H - Inches(1.1), W - Inches(0.16), Inches(0.04), fill=B300)

tb(sl, "STUMP",
   Inches(0.45), Inches(1.75), Inches(11), Inches(1.35),
   size=Pt(72), bold=True, color=B900)
tb(sl, "Transforming how teams see, measure and evolve their value streams.",
   Inches(0.45), Inches(2.95), Inches(11.5), Inches(0.52),
   size=Pt(17), color=B700, italic=True)
tb(sl, "One platform.  Eight agents.  End-to-end transformation intelligence.",
   Inches(0.45), Inches(3.52), Inches(11), Inches(0.38),
   size=Pt(12), color=MGRAY)

closing_stats = [
    ("8",    "AI Agents"),
    ("7",    "PDLC Phases"),
    ("3",    "Future Scenarios"),
    ("5.5×", "Max ROI"),
    ("88%",  "Max WT Reduction"),
    ("95%",  "Max Accuracy Score"),
]
ssw = Inches(1.96)
for i, (val, lbl) in enumerate(closing_stats):
    sx = Inches(0.45) + i * (ssw + Inches(0.12))
    sy = Inches(4.12)
    rect(sl, sx, sy, ssw, Inches(0.9), fill=B050, line_rgb=B300)
    tb(sl, val, sx, sy + Inches(0.06), ssw, Inches(0.52),
       size=Pt(26), bold=True, color=B900, align=PP_ALIGN.CENTER)
    tb(sl, lbl, sx, sy + Inches(0.58), ssw, Inches(0.28),
       size=Pt(9), color=MGRAY, align=PP_ALIGN.CENTER)

tb(sl, "© 2026 Cognizant  ·  Confidential  ·  STUMP v1.0",
   Inches(0.45), H - Inches(0.85), Inches(8), Inches(0.3),
   size=Pt(10), color=MGRAY)

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/Users/125066/projects/pdlc-vsm-platform/STUMP-Platform-Overview.pptx"
prs.save(out)
print(f"Saved  →  {out}")
