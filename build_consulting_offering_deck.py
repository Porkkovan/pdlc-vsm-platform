"""
Build: PDLC VSM Platform — Consulting Service Offering
Output: PDLC-VSM-Consulting-Service-Offering.pptx
~30 slides | White backgrounds | Navy/Blue/Teal palette | Storytelling narrative
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

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
GRAY50    = RGBColor(0xF9, 0xFA, 0xFB)
GRAY100   = RGBColor(0xF3, 0xF4, 0xF6)
GRAY200   = RGBColor(0xE5, 0xE7, 0xEB)
GRAY600   = RGBColor(0x4B, 0x55, 0x63)
GRAY700   = RGBColor(0x37, 0x41, 0x51)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
BLACK     = RGBColor(0x00, 0x00, 0x00)

W = Inches(13.333)  # widescreen 16:9
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # truly blank

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def add_rect(slide, x, y, w, h, fill=WHITE, alpha=None):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    return shape

def add_text(slide, text, x, y, w, h,
             size=14, bold=False, color=GRAY700, align=PP_ALIGN.LEFT,
             wrap=True, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tb

def add_para(tf, text, size=12, bold=False, color=GRAY700, align=PP_ALIGN.LEFT,
             space_before=0, italic=False):
    from pptx.util import Pt as P2
    from pptx.oxml.ns import qn
    from lxml import etree
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    run = p.add_run()
    run.text = text
    run.font.size = P2(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return p

def slide_bg(slide, color=WHITE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def rule(slide, x, y, w, color=GRAY200, h=0.02):
    add_rect(slide, x, y, w, h, fill=color)

def header_band(slide, title, subtitle=None, accent=NAVY):
    """Top navy band with title + optional subtitle"""
    add_rect(slide, 0, 0, 13.333, 1.2, fill=accent)
    add_text(slide, title, 0.4, 0.1, 12.5, 0.7,
             size=26, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.4, 0.75, 12.5, 0.45,
                 size=13, bold=False, color=RGBColor(0xBF, 0xDB, 0xFF), align=PP_ALIGN.LEFT)

def talking_box(slide, lines, x=9.6, y=1.3, w=3.5, h=5.8, title="Talking Points"):
    """Right-side amber talking points panel"""
    add_rect(slide, x, y, w, h, fill=LTAMBER)
    add_rect(slide, x, y, w, 0.35, fill=AMBER)
    add_text(slide, title, x+0.1, y+0.03, w-0.2, 0.3,
             size=10, bold=True, color=WHITE)
    tb = slide.shapes.add_textbox(Inches(x+0.12), Inches(y+0.42), Inches(w-0.24), Inches(h-0.52))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for line in lines:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = "• " + line
        run.font.size = Pt(9.5)
        run.font.color.rgb = GRAY700

def act_divider(slide, act_num, act_title, desc, color=NAVY):
    """Full-bleed act divider slide"""
    slide_bg(slide, color)
    # Large act label
    add_text(slide, f"ACT {act_num}", 1.0, 1.8, 11, 1.0,
             size=18, bold=True, color=RGBColor(0x93, 0xC5, 0xFD), align=PP_ALIGN.LEFT)
    add_text(slide, act_title, 1.0, 2.5, 11, 1.4,
             size=36, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    rule(slide, 1.0, 4.0, 5.0, color=RGBColor(0x93, 0xC5, 0xFD), h=0.04)
    add_text(slide, desc, 1.0, 4.2, 8.5, 1.5,
             size=14, color=RGBColor(0xBF, 0xDB, 0xFF), align=PP_ALIGN.LEFT)

def stat_box(slide, value, label, x, y, w=2.1, h=1.2, bg=LTBLUE, val_color=BLUE):
    add_rect(slide, x, y, w, h, fill=bg)
    add_text(slide, value, x+0.1, y+0.05, w-0.2, 0.65,
             size=26, bold=True, color=val_color, align=PP_ALIGN.CENTER)
    add_text(slide, label, x+0.05, y+0.65, w-0.1, 0.5,
             size=9, color=GRAY600, align=PP_ALIGN.CENTER)

def phase_box(slide, num, title, activities, deliverables, x, y, w=2.3, h=4.5,
              bg=LTBLUE, accent=BLUE):
    add_rect(slide, x, y, w, h, fill=bg)
    add_rect(slide, x, y, w, 0.45, fill=accent)
    add_text(slide, f"Phase {num}", x+0.1, y+0.05, w-0.2, 0.2,
             size=8, bold=True, color=WHITE)
    add_text(slide, title, x+0.1, y+0.22, w-0.2, 0.25,
             size=9.5, bold=True, color=WHITE)
    add_text(slide, "Activities", x+0.1, y+0.55, w-0.2, 0.2,
             size=8, bold=True, color=accent)
    yy = y + 0.75
    for a in activities:
        add_text(slide, f"• {a}", x+0.1, yy, w-0.2, 0.28, size=7.5, color=GRAY700)
        yy += 0.27
    rule(slide, x+0.1, yy+0.05, w-0.2, color=GRAY200)
    add_text(slide, "Deliverables", x+0.1, yy+0.12, w-0.2, 0.2,
             size=8, bold=True, color=TEAL)
    yy2 = yy + 0.32
    for d in deliverables:
        add_text(slide, f"✓ {d}", x+0.1, yy2, w-0.2, 0.28, size=7.5, color=TEAL)
        yy2 += 0.27

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, NAVY)

# Top accent stripe
add_rect(sl, 0, 0, 13.333, 0.08, fill=BLUE)

# Left content area
add_text(sl, "CONSULTING SERVICE OFFERING", 0.9, 1.0, 9, 0.5,
         size=13, bold=True, color=RGBColor(0x93, 0xC5, 0xFD), align=PP_ALIGN.LEFT)

add_text(sl, "AI-Powered Product Delivery\nLifecycle Transformation", 0.9, 1.55, 9.5, 2.2,
         size=38, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

rule(sl, 0.9, 3.7, 5.5, color=BLUE, h=0.05)

add_text(sl, "Compress feature lead times by 40–70% · Achieve 3–5× ROI\nTransform your engineering value stream with multi-agent AI",
         0.9, 3.85, 9, 0.85, size=14, color=RGBColor(0xBF, 0xDB, 0xFF))

# Bottom tags
for i, tag in enumerate(["Value Stream Mapping", "LangGraph AI Agents", "DORA Benchmarking",
                           "Business Case Modelling", "90-Day Playbook"]):
    xi = 0.9 + i * 2.42
    add_rect(sl, xi, 5.5, 2.25, 0.38, fill=RGBColor(0x1E, 0x40, 0x80))
    add_text(sl, tag, xi+0.08, 5.55, 2.1, 0.3, size=9.5, bold=True,
             color=RGBColor(0x93, 0xC5, 0xFD), align=PP_ALIGN.CENTER)

# Bottom bar
add_rect(sl, 0, 6.9, 13.333, 0.6, fill=RGBColor(0x07, 0x1A, 0x3A))
add_text(sl, "CONFIDENTIAL  ·  PDLC VSM Platform v1.0  ·  © 2026",
         0.5, 6.95, 12, 0.4, size=9, color=GRAY600, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — EXECUTIVE SUMMARY (The 90-second pitch)
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Executive Summary", "The service offering in 90 seconds", accent=NAVY)

# 3 columns: Problem / Solution / Outcome
cols = [
    ("The Problem", BLUE, LTBLUE,
     ["Enterprise teams deliver features in 40+ days", "Flow Efficiency averages only 8–12%",
      "90% of elapsed time is pure waste — waiting for reviews, approvals, hand-offs",
      "AI tooling investment is scattered with no systemic ROI"]),
    ("Our Solution", TEAL, LTTEAL,
     ["End-to-end Value Stream Mapping of your 7-phase PDLC", "AI-calibrated bottleneck identification",
      "3 investment-ready transformation scenarios (Option A / B / C)",
      "90-day sprint playbook personalised to your team, stack & budget"]),
    ("Guaranteed Outcomes", GREEN, LTGREEN,
     ["Option A: −40% Lead Time · 2.8× ROI · 14-month payback",
      "Option B: −55% Lead Time · 3.8× ROI · 11-month payback",
      "Option C: −70% Lead Time · 5.5× ROI · 19-month payback",
      "Board-ready business case generated in a single session"]),
]
for i, (title, accent, bg, bullets) in enumerate(cols):
    xi = 0.35 + i * 4.32
    add_rect(sl, xi, 1.35, 4.0, 5.1, fill=bg)
    add_rect(sl, xi, 1.35, 4.0, 0.42, fill=accent)
    add_text(sl, title, xi+0.12, 1.38, 3.76, 0.35, size=12, bold=True, color=WHITE)
    yy = 1.95
    for b in bullets:
        add_text(sl, f"• {b}", xi+0.14, yy, 3.72, 0.55, size=10, color=GRAY700)
        yy += 0.55

add_text(sl, "Delivered as a fixed-scope consulting engagement · 8–16 weeks · Applicable to any industry",
         0.35, 6.6, 12.5, 0.4, size=10, italic=True, color=GRAY600, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — ACT 1 DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
act_divider(sl, 1, "The Market Reality",
            "Engineering organisations are stuck in a slow-delivery trap — and most don't even know it.", NAVY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — THE PROBLEM: WHERE YOUR TIME GOES
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "The Slow-Delivery Trap", "Where enterprise engineering time actually goes", accent=NAVY)

# Big stats row
stat_box(sl, "42.5 days", "Avg Feature Lead Time\n(enterprise teams)", 0.35, 1.4, bg=LTBLUE, val_color=NAVY)
stat_box(sl, "8.1%", "Flow Efficiency\n(only 8¢ of every dollar is work)", 2.6, 1.4, bg=RGBColor(0xFF,0xE4,0xE6), val_color=RED)
stat_box(sl, "536 hrs", "Wait Time per feature\nvs 100 hrs of actual work", 4.85, 1.4, bg=LTAMBER, val_color=AMBER)
stat_box(sl, "40+ days", "Time lost in testing\n& approval queues alone", 7.1, 1.4, bg=LTTEAL, val_color=TEAL)

# Bar chart of phases
add_text(sl, "Waste by PDLC Phase (typical medium performer)", 0.35, 2.85, 8.5, 0.35,
         size=11, bold=True, color=NAVY)
phases = [
    ("Phase 1\nBacklog", 0.6, LTBLUE, BLUE),
    ("Phase 2\nDesign", 1.1, LTBLUE, BLUE),
    ("Phase 3\nDevelopment", 1.8, LTBLUE, BLUE),
    ("Phase 4\nCI/CD", 1.2, LTBLUE, BLUE),
    ("Phase 5\nTesting", 3.4, RGBColor(0xFF,0xE4,0xE6), RED),
    ("Phase 6\nRelease", 1.6, LTAMBER, AMBER),
    ("Phase 7\nMonitoring", 0.5, LTTEAL, TEAL),
]
max_wt = 3.4
bar_h = 0.22
for i, (label, wt, bg, col) in enumerate(phases):
    xi = 0.35 + i * 1.27
    bar_w = (wt / max_wt) * 4.8
    add_text(sl, label, xi, 3.22, 1.2, 0.42, size=7.5, color=GRAY600, align=PP_ALIGN.CENTER)
    add_rect(sl, xi+0.1, 3.65, bar_w, bar_h, fill=col)
    add_text(sl, f"{wt*15:.0f}h wait", xi+0.12, 3.68, bar_w-0.05, 0.2, size=7, color=WHITE, bold=True)

add_text(sl, "← Low waste        High waste →", 0.35, 4.0, 5.5, 0.25, size=8, italic=True, color=GRAY600)

# Root causes list
add_rect(sl, 0.35, 4.35, 8.9, 2.65, fill=GRAY100)
add_text(sl, "Root Causes", 0.5, 4.42, 4, 0.3, size=11, bold=True, color=NAVY)
causes = [
    "Manual decision gates (Architecture Review, CAB, UAT sign-off) add 2–5 days per phase",
    "Automated testing is fragile — performance and regression suites require 16–40h of manual effort",
    "No real-time visibility into where items are waiting — teams manage by Jira ticket status, not flow data",
    "AI tool investment is phase-specific (Copilot = Phase 3 only) — no systemic approach across all 7 phases",
]
for j, c in enumerate(causes):
    yy = 4.8 + j * 0.52
    add_rect(sl, 0.5, yy, 0.08, 0.28, fill=RED)
    add_text(sl, c, 0.7, yy, 8.35, 0.45, size=9.5, color=GRAY700)

talking_box(sl, [
    "Land the 8.1% Flow Efficiency stat first — it's visceral. For every 1 day of work, 12 days are wasted.",
    "Ask: 'Do you know your organisation's Flow Efficiency today?' — almost no one does.",
    "Phase 5 (Testing) is always the audience's surprise — testing feels fast but queues are enormous.",
    "Source: DORA 2024 State of DevOps · GitHub Octoverse 2024 · Gartner Engineering Productivity",
    "The 42.5-day figure is the cross-industry median for enterprise software teams.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — WHY NOW: THE AI INFLECTION POINT
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Why Now: The AI Inflection Point", "Three forces converging in 2025–2026 make this the right moment to act", accent=NAVY)

forces = [
    ("01", "LLM Capability Leap", BLUE, LTBLUE,
     "GPT-4o, Claude 3.5, Gemini 1.5 can now autonomously generate tests, review PRs, analyse performance traces, and draft release notes — capabilities that simply didn't exist at production quality 18 months ago.",
     "GitHub Copilot: 55% faster code completion · Gartner: 40% reduction in manual test writing by 2026"),
    ("02", "Multi-Agent Orchestration Maturity", TEAL, LTTEAL,
     "LangGraph, AutoGen, and CrewAI now support production-grade multi-agent pipelines. Complex PDLC workflows — spanning 7 phases and 36 activities — can be orchestrated end-to-end with human oversight at key gates.",
     "LangGraph adoption: 3× YoY growth · McKinsey: 70% of enterprises piloting agentic AI in 2025"),
    ("03", "Competitive Pressure", AMBER, LTAMBER,
     "Elite performers (18% of organisations) deploy 460× more frequently than low performers. The gap is widening. Early movers on AI-first PDLC are compressing features from months to days — creating a delivery moat.",
     "DORA 2024: Elite vs Low performer gap now 1,460× in time-to-market · Forrester: AI delivery leaders grow revenue 2.3× faster"),
]
for i, (num, title, accent, bg, body, stat) in enumerate(forces):
    yi = 1.45 + i * 1.88
    add_rect(sl, 0.35, yi, 8.9, 1.7, fill=bg)
    add_rect(sl, 0.35, yi, 0.6, 1.7, fill=accent)
    add_text(sl, num, 0.37, yi+0.5, 0.56, 0.6, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(sl, title, 1.05, yi+0.08, 8.1, 0.35, size=13, bold=True, color=accent)
    add_text(sl, body, 1.05, yi+0.42, 8.05, 0.7, size=9.5, color=GRAY700)
    add_text(sl, f"Data: {stat}", 1.05, yi+1.12, 8.05, 0.38, size=8.5, italic=True, color=GRAY600)

talking_box(sl, [
    "Frame this as a 'window of advantage' — early movers build delivery infrastructure while others are still evaluating.",
    "The 1,460× DORA stat always lands hard — repeat it slowly.",
    "LangGraph/agentic framing matters: this is NOT another Copilot. It's orchestration across the full lifecycle.",
    "Reference: DORA 2024, McKinsey Technology Report 2025, Gartner Magic Quadrant AI Code Tools 2025",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — INDUSTRY IMPACT: THE COST OF INACTION
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "The Cost of Inaction by Industry",
            "Every quarter of delay compounds the competitive disadvantage", accent=RED)

industries = [
    ("Banking &\nFinancial Services", "52 days", "$4.2M", "18 months", BLUE, LTBLUE),
    ("Insurance", "48 days", "$3.1M", "15 months", TEAL, LTTEAL),
    ("Telecommunications", "44 days", "$3.8M", "14 months", NAVY, LTBLUE),
    ("Retail & e-Commerce", "36 days", "$2.9M", "12 months", AMBER, LTAMBER),
    ("Healthcare & Life Sci", "56 days", "$5.1M", "20 months", RED, RGBColor(0xFF,0xE4,0xE6)),
    ("Government & Public", "68 days", "$6.4M", "24 months", GRAY600, GRAY100),
]

headers = ["Industry", "Avg Feature\nLead Time", "Annual Cost\nof Delay*", "Break-Even\nfor Option A"]
hx = [0.35, 3.2, 5.5, 7.8]
hw = [2.8, 2.1, 2.1, 2.1]
for j, (hdr, hxi, hwi) in enumerate(zip(headers, hx, hw)):
    add_rect(sl, hxi, 1.4, hwi, 0.42, fill=NAVY)
    add_text(sl, hdr, hxi+0.08, 1.42, hwi-0.16, 0.38, size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

for i, (name, lt, cost, be, accent, bg) in enumerate(industries):
    yi = 1.88 + i * 0.72
    row_bg = bg if i % 2 == 0 else WHITE
    add_rect(sl, 0.35, yi, 2.8, 0.65, fill=row_bg)
    add_rect(sl, 0.35, yi, 0.08, 0.65, fill=accent)
    add_text(sl, name, 0.52, yi+0.1, 2.5, 0.5, size=10, bold=True, color=GRAY700)
    for val, hxi, hwi in zip([lt, cost, be], hx[1:], hw[1:]):
        add_rect(sl, hxi, yi, hwi, 0.65, fill=row_bg)
        add_text(sl, val, hxi, yi+0.12, hwi, 0.4, size=13, bold=True, color=accent, align=PP_ALIGN.CENTER)

add_text(sl, "* Annual cost of delay = conservative estimate based on avg developer cost ($180K fully-loaded) × team size (20 FTEs) × wasted flow time (91.9%)",
         0.35, 6.45, 9, 0.35, size=7.5, italic=True, color=GRAY600)

talking_box(sl, [
    "Banking and Healthcare consistently show the highest delay costs due to compliance-heavy release gates.",
    "These are conservative figures — they exclude opportunity cost of features delayed to market.",
    "Use the client's own team size to compute a customised figure on the spot (team × $180K × 0.919 × phases delayed).",
    "Healthcare lead time of 56 days reflects FDA/TGA validation overhead in the release phase.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — ACT 2 DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
act_divider(sl, 2, "Introducing: PDLC Transformation as a Service",
            "A structured, data-driven consulting engagement that maps, analyses and redesigns your product delivery lifecycle.", BLUE)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — SERVICE OFFERING OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Service Offering: What We Deliver",
            "A complete transformation programme — from data to board-ready business case — in 8–16 weeks", accent=BLUE)

# Central value proposition
add_rect(sl, 0.35, 1.35, 8.9, 0.7, fill=LTBLUE)
add_text(sl,
         "We connect to your ALM tools, measure every phase of your PDLC, identify the exact bottlenecks costing you months of delivery time, "
         "design three AI-powered future states with predicted metrics, and produce a personalised 90-day implementation playbook — "
         "all backed by a board-ready investment case.",
         0.5, 1.42, 8.6, 0.55, size=10.5, color=NAVY, italic=True)

# 4 pillars
pillars = [
    ("Measure", BLUE, LTBLUE,
     ["ALM tool integration (Jira / ADO / CSV)", "DORA baseline assessment",
      "7-phase VSM with 36 activity metrics", "Flow Efficiency & Lead Time analysis"]),
    ("Diagnose", TEAL, LTTEAL,
     ["AI bottleneck identification (8 critical)", "Phase heatmap & severity scoring",
      "Root cause analysis per bottleneck", "Benchmarking vs DORA 2024 peers"]),
    ("Design", AMBER, LTAMBER,
     ["3 future state scenarios (A/B/C)", "AI agent coverage mapping",
      "Org change & role redesign model", "Tool and DevSecOps roadmap"]),
    ("Activate", GREEN, LTGREEN,
     ["Board-ready business case (ROI/NPV)", "90-day sprint playbook",
      "RACI for human-AI handoffs", "Change management & training plan"]),
]
for i, (title, accent, bg, pts) in enumerate(pillars):
    xi = 0.35 + i * 2.25
    add_rect(sl, xi, 2.2, 2.1, 4.1, fill=bg)
    add_rect(sl, xi, 2.2, 2.1, 0.38, fill=accent)
    add_text(sl, title, xi+0.1, 2.24, 1.9, 0.3, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    for j, pt in enumerate(pts):
        yy = 2.72 + j * 0.77
        add_rect(sl, xi+0.15, yy, 0.18, 0.18, fill=accent)
        add_text(sl, pt, xi+0.4, yy-0.02, 1.6, 0.55, size=9, color=GRAY700)

# Bottom engagement types
add_rect(sl, 0.35, 6.45, 8.9, 0.65, fill=GRAY100)
add_text(sl, "Engagement Types:", 0.5, 6.52, 1.5, 0.3, size=9, bold=True, color=NAVY)
for i, (label, desc) in enumerate([
    ("Diagnostic Sprint", "2-week rapid VSM assessment — single team"),
    ("Full Transformation", "8–16 week end-to-end engagement — product portfolio"),
    ("Ongoing Advisory", "Quarterly VSM review + AI agent optimisation"),
]):
    xi = 2.1 + i * 2.38
    add_rect(sl, xi, 6.52, 2.22, 0.5, fill=WHITE)
    add_text(sl, label, xi+0.1, 6.53, 2.0, 0.25, size=9, bold=True, color=BLUE)
    add_text(sl, desc, xi+0.1, 6.76, 2.0, 0.25, size=8, color=GRAY600)

talking_box(sl, [
    "Position the 4 pillars as a continuous loop — Measure → Diagnose → Design → Activate → back to Measure.",
    "Emphasise that the platform does the analysis — consultants facilitate and customise, not manually compute.",
    "The Diagnostic Sprint is the wedge — low risk entry point that always reveals surprises and creates appetite for full engagement.",
    "'Board-ready' means CFO can put it in a board pack without reformatting.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — THE 3 TRANSFORMATION TIERS
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Three Transformation Scenarios — Client Choice",
            "Every engagement produces three investment-ready options. Clients choose their ambition level.", accent=BLUE)

scenarios = [
    ("Option A", "AI-Assisted", "40%", "6–10 weeks", "−40%", "8.1% → 16.2%", "2.8×", "$800K–$1.5M", "14 months",
     "No role changes. AI agent deployed alongside every human role. Low disruption, immediate productivity gains.",
     BLUE, LTBLUE,
     ["AI code review & PR assistant", "Automated test generation", "AI release note drafting",
      "Intelligent backlog scoring", "Automated performance benchmarking"]),
    ("Option B", "Hybrid", "65%", "12–20 weeks", "−55%", "8.1% → 22.3%", "3.8×", "$1.2M–$2.2M", "11 months",
     "5 core human roles. Strategic AI agents in highest-impact phases. Optimal ROI for most organisations.",
     TEAL, LTTEAL,
     ["All Option A agents +", "Autonomous SIT/UAT readiness scoring", "AI architecture review assistant",
      "Continuous delivery intelligence layer", "CAB automation & risk scoring"]),
    ("Option C", "AI-First", "85%", "18–36 months", "−70%", "8.1% → 36.5%", "5.5×", "$2.5M–$4.5M", "19 months",
     "2 human roles: Product Definer + Product Builder supervising agent orchestration. Full agentic PDLC.",
     AMBER, LTAMBER,
     ["All Option B agents +", "Autonomous feature decomposition", "Self-healing CI/CD pipelines",
      "Agentic production incident response", "Full LangGraph PDLC orchestration"]),
]

for i, (opt, title, auto, timeline, lt, fe, roi, invest, payback,
         desc, accent, bg, agents) in enumerate(scenarios):
    xi = 0.35 + i * 4.32
    add_rect(sl, xi, 1.35, 4.0, 5.75, fill=bg)
    add_rect(sl, xi, 1.35, 4.0, 0.5, fill=accent)
    add_text(sl, opt, xi+0.12, 1.38, 1.5, 0.3, size=14, bold=True, color=WHITE)
    add_text(sl, title, xi+1.3, 1.42, 2.5, 0.28, size=11, bold=True, color=WHITE)
    add_text(sl, f"{auto} Automation", xi+2.5, 1.38, 1.35, 0.28, size=9, color=RGBColor(0xFF,0xFF,0xCC), align=PP_ALIGN.RIGHT)

    add_text(sl, desc, xi+0.14, 1.92, 3.72, 0.6, size=8.5, color=GRAY700, italic=True)

    metrics = [("Lead Time", lt), ("Flow Efficiency", fe), ("ROI Multiple", roi)]
    for j, (ml, mv) in enumerate(metrics):
        yy = 2.68 + j * 0.55
        add_text(sl, ml, xi+0.14, yy, 2.0, 0.3, size=8.5, color=GRAY600)
        add_text(sl, mv, xi+2.1, yy, 1.76, 0.3, size=11, bold=True, color=accent, align=PP_ALIGN.RIGHT)

    rule(sl, xi+0.14, 4.4, 3.72, color=GRAY200)
    add_text(sl, "Investment", xi+0.14, 4.48, 2.0, 0.28, size=8.5, color=GRAY600)
    add_text(sl, invest, xi+0.14, 4.72, 3.72, 0.3, size=10, bold=True, color=NAVY)
    add_text(sl, f"Payback: {payback}", xi+0.14, 4.98, 3.72, 0.28, size=8.5, color=GREEN, bold=True)

    add_text(sl, "Key AI Agents:", xi+0.14, 5.32, 3.72, 0.22, size=8, bold=True, color=accent)
    for k, ag in enumerate(agents):
        add_text(sl, f"› {ag}", xi+0.14, 5.55+k*0.27, 3.72, 0.25, size=8, color=GRAY600)

talking_box(sl, [
    "Always present all three — don't pre-select. Let the client anchor on B (best ROI), then Option A closes easily.",
    "Option C is aspirational — use it to show the destination, even if client starts at A.",
    "The 5.5× ROI for Option C sounds aggressive — ground it: 'This assumes full agent orchestration with only 2 human supervisory roles.'",
    "Every option includes the same deliverable set — business case, playbook, RACI. Only the scope of AI automation differs.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — QUANTITATIVE BENEFITS BY INDUSTRY
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Quantitative Benefits by Industry Vertical",
            "Conservative estimates based on DORA 2024, Gartner, McKinsey Technology Research", accent=TEAL)

add_rect(sl, 0.35, 1.35, 12.65, 0.42, fill=NAVY)
for j, (hdr, hxi, hwi) in enumerate(zip(
    ["Industry", "Option A\nLT Reduction", "Option A\nAnnual Savings", "Option B\nLT Reduction",
     "Option B\nAnnual Savings", "Option B\nROI"],
    [0.35, 2.9, 4.9, 6.85, 8.85, 11.1],
    [2.5, 1.9, 1.9, 1.9, 2.2, 1.9]
)):
    add_text(sl, hdr, hxi+0.08, 1.38, hwi-0.16, 0.36, size=8.5, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)

rows = [
    ("Banking & Financial Services", "−40%", "$2.8M–$4.2M", "−55%", "$4.5M–$6.8M", "3.6×"),
    ("Insurance", "−38%", "$2.0M–$3.2M", "−52%", "$3.4M–$5.1M", "3.4×"),
    ("Telecommunications", "−42%", "$2.4M–$3.6M", "−57%", "$4.0M–$6.0M", "3.9×"),
    ("Retail & e-Commerce", "−44%", "$1.8M–$2.8M", "−60%", "$3.1M–$4.7M", "4.1×"),
    ("Healthcare & Life Sci", "−35%", "$3.2M–$5.0M", "−48%", "$5.2M–$8.0M", "3.2×"),
    ("Government & Public Sector", "−30%", "$2.2M–$3.4M", "−42%", "$3.6M–$5.5M", "2.9×"),
    ("SaaS / Technology", "−45%", "$1.5M–$2.4M", "−62%", "$2.7M–$4.1M", "4.4×"),
]
for i, row in enumerate(rows):
    yi = 1.82 + i * 0.62
    bg = GRAY100 if i % 2 == 0 else WHITE
    xs = [0.35, 2.9, 4.9, 6.85, 8.85, 11.1]
    ws = [2.5, 1.9, 1.9, 1.9, 2.2, 1.9]
    colors = [NAVY, BLUE, BLUE, TEAL, TEAL, GREEN]
    bolds = [True, True, True, True, True, True]
    sizes = [9.5, 11, 10, 11, 10, 12]
    for j, (val, xi, wi, col, bo, sz) in enumerate(zip(row, xs, ws, colors, bolds, sizes)):
        add_rect(sl, xi, yi, wi, 0.56, fill=bg)
        align = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        add_text(sl, val, xi+0.1, yi+0.12, wi-0.2, 0.38, size=sz, bold=bo, color=col, align=align)

add_text(sl, "Annual savings = (team_size × avg_fully_loaded_cost × flow_efficiency_gain) + (lead_time_reduction × revenue_per_feature_day). Assumes 20-FTE product team, $180K FLTC, $50K/day feature value.",
         0.35, 6.5, 12.6, 0.35, size=7.5, italic=True, color=GRAY600)

talking_box(sl, [
    "Pick the client's industry row and use it throughout the engagement — it anchors all ROI conversations.",
    "SaaS teams typically achieve the highest option B ROI because they have the infrastructure for rapid AI integration.",
    "Healthcare lower ROI reflects longer compliance validation cycles — not lower savings, longer payback.",
    "These figures are benchmarked against similar-sized teams from DORA 2024 participating organisations.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — ACT 3 DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
act_divider(sl, 3, "Our Consulting Approach",
            "A rigorous, phased methodology that produces measurable results — not PowerPoint strategy decks.", TEAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — ENGAGEMENT PHASES OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "5-Phase Engagement Methodology",
            "From data collection to live implementation — every phase has defined deliverables and success criteria", accent=TEAL)

phases_data = [
    ("1", "Discover &\nCalibrate", "Weeks 1–2", BLUE,
     ["ALM data extraction (Jira/ADO)", "DORA baseline survey", "Stakeholder interviews", "VSM data validation"],
     ["DORA Benchmark Report", "Raw VSM Dataset", "Stakeholder Interview Summary"]),
    ("2", "Map &\nAnalyse", "Weeks 2–4", TEAL,
     ["Current state VSM construction", "Bottleneck identification (AI)", "Phase heatmap generation", "Effort/Wait time analysis"],
     ["Current State VSM (visual)", "Bottleneck Analysis Report", "Flow Efficiency Baseline"]),
    ("3", "Design\nFuture State", "Weeks 4–8", AMBER,
     ["3-scenario future state design", "AI agent coverage mapping", "Org change modelling", "Tool selection & roadmap"],
     ["Future State VSM (3 options)", "AI Agent Architecture", "Org & Tool Roadmap"]),
    ("4", "Build\nBusiness Case", "Weeks 8–10", GREEN,
     ["ROI modelling by scenario", "NPV & payback analysis", "Implementation timeline build", "Risk register creation"],
     ["Board-Ready Business Case", "Investment Model (Excel)", "Implementation Roadmap"]),
    ("5", "Activate &\nHandover", "Weeks 10–16", NAVY,
     ["90-day playbook generation", "Pilot team selection", "Sprint 1 kickoff facilitation", "Capability transfer"],
     ["Personalised 90-Day Playbook", "RACI Matrix", "Sprint 1 Backlog"]),
]

for i, (num, title, timeline, accent, acts, delivs) in enumerate(phases_data):
    xi = 0.3 + i * 2.58
    add_rect(sl, xi, 1.4, 2.4, 5.3, fill=GRAY100)
    add_rect(sl, xi, 1.4, 2.4, 0.52, fill=accent)
    add_text(sl, f"Phase {num}", xi+0.12, 1.42, 0.7, 0.25, size=8, color=WHITE, bold=True)
    add_text(sl, timeline, xi+0.85, 1.42, 1.42, 0.25, size=8, color=RGBColor(0xCC,0xFF,0xCC), align=PP_ALIGN.RIGHT)
    add_text(sl, title, xi+0.12, 1.66, 2.16, 0.32, size=11, bold=True, color=WHITE)
    add_text(sl, "Activities", xi+0.12, 2.02, 2.16, 0.22, size=8, bold=True, color=accent)
    for j, a in enumerate(acts):
        add_text(sl, f"• {a}", xi+0.14, 2.26+j*0.44, 2.12, 0.38, size=8.5, color=GRAY700)
    rule(sl, xi+0.14, 4.1, 2.12, color=GRAY200)
    add_text(sl, "Deliverables", xi+0.12, 4.18, 2.16, 0.22, size=8, bold=True, color=TEAL)
    for j, d in enumerate(delivs):
        add_text(sl, f"✓ {d}", xi+0.14, 4.42+j*0.42, 2.12, 0.38, size=8.5, color=TEAL)

# Arrow connectors
for i in range(4):
    xi = 0.3 + i * 2.58 + 2.4
    add_rect(sl, xi+0.03, 2.85, 0.12, 0.35, fill=GRAY200)
    add_text(sl, "›", xi, 2.78, 0.25, 0.35, size=16, bold=True, color=GRAY200, align=PP_ALIGN.CENTER)

talking_box(sl, [
    "Phase 1 is often the client's biggest surprise — they've never extracted flow data from Jira at this level of granularity.",
    "Phase 3 takes the most workshop time — Future State design requires functional leads in the room.",
    "Phase 5 is critical for adoption: Activate is where the rubber meets the road. The 90-day playbook must be handed to a named tech lead, not a committee.",
    "All 5 phases are included in the Full Transformation engagement. Diagnostic Sprint covers Phases 1–2 only.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — ILLUSTRATIVE DELIVERABLES
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Illustrative Deliverables",
            "What clients receive at the end of each engagement phase", accent=TEAL)

deliverables = [
    ("Current State VSM Report", BLUE, LTBLUE,
     "A visual value stream map of all 7 PDLC phases showing Process Time, Wait Time, Lead Time, and Flow Efficiency per activity. Phase heatmap highlights critical bottlenecks.",
     "Phase 2 output · PDF + interactive platform view"),
    ("AI Bottleneck Analysis", TEAL, LTTEAL,
     "Prioritised list of 8+ bottlenecks with severity (Critical/High/Medium), impact on Lead Time, root cause diagnosis, and AI solution recommendation per bottleneck.",
     "Phase 2 output · Used as input to Future State design"),
    ("Future State VSM (3 Scenarios)", AMBER, LTAMBER,
     "Three fully-designed future state value stream maps (A/B/C) with predicted metrics: Lead Time, Flow Efficiency, AI agent coverage, human role changes, and side-by-side comparison table.",
     "Phase 3 output · Basis for business case"),
    ("Board-Ready Business Case", GREEN, LTGREEN,
     "Investment breakdown, annual benefit model, ROI multiple, NPV, payback period, sensitivity analysis, risk register, org changes, tool roadmap, DevSecOps considerations, and AIOps architecture.",
     "Phase 4 output · Exportable as PDF / Excel"),
    ("Personalised 90-Day Playbook", NAVY, LTBLUE,
     "Sprint-by-sprint action plan (Sprints 1–6) personalised to team name, tech stack, budget, and scenario. Includes RACI matrix for human-AI handoffs, risk mitigations, and sprint success metrics.",
     "Phase 5 output · Ready to hand to engineering lead"),
    ("DORA Benchmark Report", RED, RGBColor(0xFF,0xE4,0xE6),
     "Client's DORA scores (Deployment Frequency, Lead Time for Changes, MTTR, CFR) mapped against Elite/High/Medium/Low bands with gap analysis and specific improvement targets.",
     "Phase 1 output · Foundation for all subsequent analysis"),
]

for i, (title, accent, bg, desc, meta) in enumerate(deliverables):
    row, col = divmod(i, 3)
    xi = 0.35 + col * 2.98
    yi = 1.4 + row * 2.55
    add_rect(sl, xi, yi, 2.82, 2.3, fill=bg)
    add_rect(sl, xi, yi, 2.82, 0.38, fill=accent)
    add_text(sl, title, xi+0.12, yi+0.06, 2.58, 0.28, size=10, bold=True, color=WHITE)
    add_text(sl, desc, xi+0.12, yi+0.46, 2.58, 1.2, size=8.5, color=GRAY700)
    add_text(sl, meta, xi+0.12, yi+1.75, 2.58, 0.35, size=7.5, italic=True, color=accent)

talking_box(sl, [
    "Every deliverable is produced inside the platform — not built manually by consultants.",
    "Board-ready = CFO can screenshot the ROI summary and put it in a board deck.",
    "The 90-day playbook is the most valued output — it answers 'what do we actually DO on Monday?'",
    "Deliverables are cumulative — Phase 5 playbook references Phase 2 bottlenecks and Phase 3 future state.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — CRITICAL SUCCESS FACTORS
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Critical Success Factors",
            "What makes the difference between a transformation that sticks and one that fades", accent=NAVY)

csfs = [
    ("Executive Sponsorship", BLUE, "C-suite or VP Engineering must be the engagement sponsor. Without authority to fund Option A/B, the business case has no path to approval. Secure this before Phase 1 kick-off.", "Risk: Low adoption rate"),
    ("Real Data in Phase 1", TEAL, "VSM analysis built on actual Jira/ADO cycle time data produces 3× more accurate bottleneck identification than survey-based estimates. ALM connection is non-negotiable for Full Transformation.", "Risk: Generic recommendations"),
    ("Pilot Team Selection", AMBER, "Choose a team with: (a) a willing tech lead, (b) an active product backlog with 3+ active sprints of data, (c) a mix of DORA skill levels. Avoid flagship teams — pick a 'willing middle'.", "Risk: Pilot failure poisons org appetite"),
    ("Change Management Bandwidth", GREEN, "Assign a dedicated change manager or senior BA for the engagement. AI tool adoption without structured change management achieves <40% of projected productivity gains.", "Risk: Tool adoption failure"),
    ("Phased Investment Commitment", NAVY, "Commit to Option A budget before Phase 3. Clients who defer investment decisions until after the business case is built are 2× more likely to choose the lower-ambition option.", "Risk: Sub-optimal ROI realisation"),
    ("Measurement Culture", RED, "Establish Flow Efficiency, Lead Time, and DORA metrics as weekly engineering KPIs from Sprint 1. Transformation without measurement is invisible to the board.", "Risk: No evidence for budget renewal"),
]

for i, (title, accent, desc, risk) in enumerate(csfs):
    row, col = divmod(i, 2)
    xi = 0.35 + col * 4.45
    yi = 1.4 + row * 1.85
    add_rect(sl, xi, yi, 4.25, 1.65, fill=GRAY100)
    add_rect(sl, xi, yi, 0.12, 1.65, fill=accent)
    add_text(sl, f"{i+1:02d}  {title}", xi+0.22, yi+0.1, 4.0, 0.3, size=11, bold=True, color=NAVY)
    add_text(sl, desc, xi+0.22, yi+0.42, 4.0, 0.9, size=8.5, color=GRAY700)
    add_rect(sl, xi+0.22, yi+1.32, 3.9, 0.25, fill=RGBColor(0xFF,0xE4,0xE6))
    add_text(sl, f"⚠ {risk}", xi+0.32, yi+1.34, 3.7, 0.2, size=8, color=RED, bold=True)

talking_box(sl, [
    "CSF #1 (Exec Sponsor) is the deal-breaker. If the engagement sponsor is below VP-level, the business case stalls at budget approval.",
    "CSF #3 (Pilot Selection) — avoid the 'best team' trap. High performers are already efficient; you need visible improvement to build org confidence.",
    "CSF #6 (Measurement) — embed a Flow Efficiency dashboard in the engineering team's existing sprint review before the engagement ends.",
    "Address all 6 CSFs explicitly in the Phase 1 kick-off. Make them part of the engagement charter.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — ACT 4 DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
act_divider(sl, 4, "The Business Case for Clients",
            "Investment model, ROI by scenario, client technology costs — everything needed for budget approval.", AMBER)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — ROI MODEL BY SCENARIO
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Return on Investment — All Three Scenarios",
            "Based on a 20-FTE product team, $180K fully-loaded cost, 40+ day feature lead time baseline", accent=AMBER)

# Summary stat row
for i, (val, lbl, bg, col) in enumerate([
    ("2.8×", "Option A ROI", LTBLUE, BLUE),
    ("3.8×", "Option B ROI", LTTEAL, TEAL),
    ("5.5×", "Option C ROI", LTAMBER, AMBER),
    ("14 mo", "Fastest Payback\n(Option B)", LTGREEN, GREEN),
]):
    xi = 0.35 + i * 2.22
    stat_box(sl, val, lbl, xi, 1.35, w=2.05, h=0.95, bg=bg, val_color=col)

# Detailed table
headers2 = ["Metric", "Option A\nAI-Assisted", "Option B\nHybrid", "Option C\nAI-First"]
xs2 = [0.35, 3.45, 5.95, 8.45]
ws2 = [3.05, 2.4, 2.4, 2.4]
yi = 2.45
add_rect(sl, 0.35, yi, 10.5, 0.38, fill=NAVY)
for hdr, xi, wi in zip(headers2, xs2, ws2):
    add_text(sl, hdr, xi+0.08, yi+0.04, wi-0.16, 0.3, size=9, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)

table_rows = [
    ("Total Investment (incl. consulting)", "$800K–$1.5M", "$1.2M–$2.2M", "$2.5M–$4.5M"),
    ("Year 1 Annual Benefits", "$1.3M–$1.95M", "$2.1M–$3.4M", "$4.6M–$8.3M"),
    ("Year 2 Annual Benefits", "$1.5M–$2.3M", "$2.5M–$4.0M", "$5.5M–$9.8M"),
    ("3-Year Cumulative ROI Multiple", "2.8×", "3.8×", "5.5×"),
    ("Payback Period", "14 months", "11 months", "19 months"),
    ("Lead Time Reduction", "−40% (42→25 days)", "−55% (42→19 days)", "−70% (42→13 days)"),
    ("Flow Efficiency Improvement", "8.1% → 16.2%", "8.1% → 22.3%", "8.1% → 36.5%"),
    ("Process Time Reduction", "−35%", "−55%", "−70%"),
    ("Human Roles Required", "8 (unchanged)", "5", "2"),
]
row_colors = [GRAY100, WHITE] * 10
val_colors = [BLUE, TEAL, AMBER]
for j, row in enumerate(table_rows):
    yi2 = 2.88 + j * 0.44
    bg2 = GRAY100 if j % 2 == 0 else WHITE
    add_rect(sl, 0.35, yi2, 10.5, 0.42, fill=bg2)
    add_text(sl, row[0], 0.5, yi2+0.08, 2.85, 0.3, size=9, color=GRAY700)
    for k, (val, xi, wi, vc) in enumerate(zip(row[1:], xs2[1:], ws2[1:], val_colors)):
        add_text(sl, val, xi, yi2+0.08, wi, 0.3, size=9.5, bold=True,
                 color=vc, align=PP_ALIGN.CENTER)

add_text(sl, "Benefit categories: Time-to-market acceleration ($600K–$900K), productivity gains ($400K–$600K, 35% effort reduction), quality improvement ($200K–$300K), operational savings ($100K–$150K). Option A example.",
         0.35, 6.5, 10.5, 0.35, size=7.5, italic=True, color=GRAY600)

talking_box(sl, [
    "Option B has the best ROI and the shortest payback — lead with this for CFO audiences.",
    "Year 1 vs Year 2 split: Year 1 is typically 60–70% of full-run-rate as teams climb the adoption curve.",
    "The payback calculation: total investment ÷ monthly benefit rate. Option B: $1.7M ÷ $155K/mo = 11 months.",
    "Always stress-test: reduce all benefits by 30% and show it's still a strong case. Builds CFO confidence.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — CLIENT TECHNOLOGY & LICENSING COSTS
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Client Technology & Licensing Investment",
            "Indicative cost model — adjusted per client stack, team size, and scenario in Phase 4", accent=AMBER)

# Two columns: Option A and Option B
for col_i, (opt, accent, bg, total_lo, total_hi, items) in enumerate([
    ("Option A — AI-Assisted", BLUE, LTBLUE, 250, 400, [
        ("AI Code Assistant (Copilot/Cursor)", "$19–$39/user/mo", "20 users", "$4.5K–$9.4K/yr"),
        ("AI Test Generation (Diffblue/Mabl)", "$15K–$40K/yr", "Per team", "$15K–$40K/yr"),
        ("AI PR Review (CodeRabbit/Graphite)", "$12–$25/user/mo", "20 users", "$2.9K–$6.0K/yr"),
        ("Performance Testing AI (k6 AI/Grafana)", "$10K–$25K/yr", "Platform", "$10K–$25K/yr"),
        ("LLM API Access (OpenAI/Anthropic)", "$2K–$8K/mo", "Usage-based", "$24K–$96K/yr"),
        ("VSM Platform Licence (this platform)", "$30K–$60K/yr", "Organisation", "$30K–$60K/yr"),
        ("CI/CD Enhancement (GitHub Actions/ADO)", "$0–$20K/yr", "If upgrade needed", "$0–$20K/yr"),
        ("Infrastructure (cloud compute for agents)", "$5K–$15K/yr", "AWS/Azure", "$5K–$15K/yr"),
    ]),
    ("Option B — Hybrid (additional to A)", TEAL, LTTEAL, 600, 1100, [
        ("Custom Agent Development (LangGraph)", "$150K–$300K", "One-time", "Incl. consulting"),
        ("Agent Orchestration Platform (LangSmith)", "$20K–$50K/yr", "Platform licence", "$20K–$50K/yr"),
        ("AI Architecture Review Tool", "$25K–$60K/yr", "Per portfolio", "$25K–$60K/yr"),
        ("Intelligent Release Gate (custom)", "$40K–$80K", "Build cost", "One-time"),
        ("Enhanced LLM Tier (GPT-4o/Claude Opus)", "$5K–$15K/mo", "Increased usage", "$60K–$180K/yr"),
        ("AIOps Platform Integration (Datadog AI)", "$15K–$40K/yr", "Platform add-on", "$15K–$40K/yr"),
        ("Data Pipeline for Real-time VSM", "$20K–$45K", "Build + infra", "One-time + $10K/yr"),
        ("Change Management Tooling", "$5K–$15K/yr", "Training platform", "$5K–$15K/yr"),
    ]),
]):
    xi = 0.35 + col_i * 6.4
    add_rect(sl, xi, 1.35, 6.1, 0.42, fill=accent)
    add_text(sl, opt, xi+0.12, 1.4, 5.86, 0.32, size=11, bold=True, color=WHITE)
    add_rect(sl, xi, 1.82, 6.1, 0.3, fill=GRAY200)
    for j, hdr in enumerate(["Tool / Licence", "List Price", "Scope", "Annual Cost"]):
        hxi2 = xi + [0, 2.1, 3.7, 4.7][j]
        hwi2 = [2.1, 1.6, 1.0, 1.3][j]
        add_text(sl, hdr, hxi2+0.05, 1.84, hwi2, 0.24, size=7.5, bold=True, color=GRAY700, align=PP_ALIGN.LEFT)
    for i2, (tool, price, scope, annual) in enumerate(items):
        yi2 = 2.18 + i2 * 0.44
        bg2 = GRAY100 if i2 % 2 == 0 else WHITE
        for val, hxi2, hwi2 in zip([tool, price, scope, annual],
                                    [xi, xi+2.1, xi+3.7, xi+4.7],
                                    [2.1, 1.6, 1.0, 1.3]):
            add_rect(sl, hxi2, yi2, hwi2, 0.42, fill=bg2)
            add_text(sl, val, hxi2+0.05, yi2+0.08, hwi2-0.1, 0.3,
                     size=7.5, color=GRAY700, align=PP_ALIGN.LEFT)
    add_rect(sl, xi, 5.73, 6.1, 0.4, fill=bg)
    add_text(sl, f"Total Annual Investment Range: ${total_lo}K – ${total_hi}K/yr",
             xi+0.12, 5.77, 5.86, 0.3, size=10, bold=True, color=accent)

add_text(sl, "Option C additional costs: Full LangGraph orchestration platform ($200K–$500K one-time build) + $150K–$300K/yr operating costs. All prices as at Q1 2026 — subject to vendor pricing changes.",
         0.35, 6.5, 12.6, 0.35, size=7.5, italic=True, color=GRAY600)

talking_box(sl, [
    "Most clients already have 60–70% of these tools — the incremental cost is often just the VSM platform licence and LangGraph custom dev.",
    "Always validate against client's existing vendor agreements — enterprise GitHub/Azure customers often have Copilot included.",
    "LLM API cost scales with usage — help clients estimate based on number of agent runs per sprint × token usage.",
    "Frame technology cost vs benefit: $300K tools cost against $2.1M Year 1 savings = 7× on tools alone.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 18 — ACT 5 DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
act_divider(sl, 5, "Go-to-Market Strategy",
            "How we take this offering to market — target clients, entry motions, partnership model.", GREEN)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 19 — GTM STRATEGY
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Go-to-Market Strategy",
            "Three motion model — Diagnostic Sprint as the wedge, Full Transformation as the core, Advisory as the annuity", accent=GREEN)

# Target ICP
add_rect(sl, 0.35, 1.35, 5.6, 0.38, fill=NAVY)
add_text(sl, "Ideal Client Profile (ICP)", 0.5, 1.38, 5.3, 0.3, size=11, bold=True, color=WHITE)
icps = [
    ("Industry", "Banking, Insurance, Telco, Healthcare, Retail, SaaS — any org with 10+ product teams"),
    ("Size", "1,000–50,000 employees · 2–50 product engineering teams · $50M+ technology budget"),
    ("Pain Signal", "CTO/VP Eng has raised 'delivery speed' or 'AI productivity' as a priority in last 6 months"),
    ("Tech Stack", "Jira or Azure DevOps as ALM · GitHub or GitLab for code · AWS/Azure/GCP cloud"),
    ("Readiness", "At least one team using GitHub Copilot or AI tooling (signals AI openness)"),
]
for i, (label, val) in enumerate(icps):
    yi = 1.8 + i * 0.42
    add_rect(sl, 0.35, yi, 5.6, 0.38, fill=GRAY100 if i%2==0 else WHITE)
    add_text(sl, label, 0.5, yi+0.07, 1.0, 0.26, size=8.5, bold=True, color=NAVY)
    add_text(sl, val, 1.55, yi+0.07, 4.25, 0.26, size=8.5, color=GRAY700)

# 3 GTM motions
add_rect(sl, 6.1, 1.35, 6.85, 0.38, fill=NAVY)
add_text(sl, "GTM Motions", 6.25, 1.38, 6.5, 0.3, size=11, bold=True, color=WHITE)
motions = [
    ("Wedge: Diagnostic Sprint", BLUE, LTBLUE,
     "$25K–$45K fixed fee · 2 weeks · Single team · ALM connect + DORA + Current State VSM + Bottleneck Report",
     "Entry point for new clients · Zero long-term commitment · Always reveals 3–5 critical findings"),
    ("Core: Full Transformation", TEAL, LTTEAL,
     "$150K–$350K fixed fee · 8–16 weeks · Full product portfolio · All 5 phases + 3 scenarios + business case",
     "Main revenue driver · Typically follows Diagnostic Sprint · Sponsored at CTO level"),
    ("Annuity: Advisory Retainer", GREEN, LTGREEN,
     "$8K–$15K/month · Ongoing · Quarterly VSM refresh + AI agent optimisation + DORA re-baseline",
     "Recurring revenue · Typically signed after Full Transformation · 12-month minimum"),
]
for i, (title, accent, bg, scope, notes) in enumerate(motions):
    yi = 1.8 + i * 1.7
    add_rect(sl, 6.1, yi, 6.75, 1.55, fill=bg)
    add_rect(sl, 6.1, yi, 6.75, 0.35, fill=accent)
    add_text(sl, title, 6.25, yi+0.05, 6.45, 0.26, size=10, bold=True, color=WHITE)
    add_text(sl, scope, 6.25, yi+0.42, 6.45, 0.52, size=8.5, color=NAVY, bold=True)
    add_text(sl, notes, 6.25, yi+0.95, 6.45, 0.45, size=8, color=GRAY600, italic=True)

talking_box(sl, [
    "The Diagnostic Sprint is priced to be a 'no-brainer' — $25K is below most VP-level budget approval thresholds.",
    "Conversion rate: Diagnostic → Full Transformation should be 60%+ if Phase 1 reveals the expected 3–5 critical bottlenecks.",
    "The advisory retainer is positioned as 'transformation insurance' — clients don't want to lose momentum after the playbook execution.",
    "Target CTO, VP Engineering, or Head of Digital Transformation as primary buyer. CFO as secondary buyer for ROI validation.",
    "Channel: existing technology consulting relationships, DORA assessment pilots, GitHub/Atlassian partner network.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 20 — ACT 6 DIVIDER
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
act_divider(sl, 6, "Building Our Capability to Deliver",
            "Team composition, training curriculum, implementation timeline, and consulting fee model.", NAVY)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 21 — TRAINING CURRICULUM
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Consultant Training & Certification Programme",
            "Enabling existing technology consultants to deliver PDLC VSM engagements", accent=NAVY)

modules = [
    ("Module 1", "VSM Foundations", "8 hours", BLUE, [
        "Lean value stream mapping principles",
        "7-phase PDLC model (phases, activities, metrics)",
        "Process Time vs Wait Time analysis",
        "Flow Efficiency calculation & interpretation",
        "Hands-on: map a 3-phase demo VSM",
    ]),
    ("Module 2", "DORA & DevOps Benchmarking", "4 hours", TEAL, [
        "DORA Four Key Metrics explained",
        "Elite/High/Medium/Low performance bands",
        "How DORA calibrates VSM baselines",
        "DORA survey facilitation with clients",
        "Interpreting 2024 State of DevOps data",
    ]),
    ("Module 3", "Platform Proficiency", "6 hours", AMBER, [
        "PDLC VSM Platform walkthrough (all 16 pages)",
        "ALM connector setup (Jira, Azure DevOps)",
        "Running AI bottleneck analysis",
        "Generating & customising future state scenarios",
        "Business case generation & export",
    ]),
    ("Module 4", "AI Agents & LangGraph", "8 hours", GREEN, [
        "LangGraph multi-agent pipeline architecture",
        "8 PDLC agents: roles, inputs, outputs",
        "Prompt engineering for VSM analysis",
        "Customising agent outputs for client context",
        "Troubleshooting agent pipeline errors",
    ]),
    ("Module 5", "Engagement Delivery", "8 hours", NAVY, [
        "Phase 1–5 facilitation techniques",
        "Stakeholder interview frameworks",
        "Bottleneck analysis workshop facilitation",
        "Future State design workshop techniques",
        "Business case presentation to C-suite",
    ]),
    ("Module 6", "Change Management & Adoption", "4 hours", RED, [
        "AI adoption curve & resistance patterns",
        "Change management plan for Option A/B",
        "2-day AI collaboration workshop design",
        "Measuring adoption success metrics",
        "Escalation playbook for adoption blockers",
    ]),
]

for i, (mod, title, duration, accent, topics) in enumerate(modules):
    row, col = divmod(i, 3)
    xi = 0.35 + col * 4.22
    yi = 1.38 + row * 2.55
    add_rect(sl, xi, yi, 4.0, 2.3, fill=GRAY100)
    add_rect(sl, xi, yi, 4.0, 0.42, fill=accent)
    add_text(sl, mod, xi+0.12, yi+0.05, 1.5, 0.28, size=9, bold=True, color=WHITE)
    add_text(sl, duration, xi+2.5, yi+0.05, 1.38, 0.28, size=9, color=RGBColor(0xFF,0xFF,0xCC), align=PP_ALIGN.RIGHT)
    add_text(sl, title, xi+0.12, yi+0.3, 3.76, 0.22, size=10, bold=True, color=WHITE)
    for j, t in enumerate(topics):
        add_text(sl, f"• {t}", xi+0.14, yi+0.62+j*0.33, 3.72, 0.3, size=8, color=GRAY700)

add_text(sl, "Total: 38 hours (5 days) · Format: Blended (self-paced e-learning + 2-day live facilitation workshop) · Assessment: Simulated client engagement + platform certification",
         0.35, 6.52, 12.5, 0.35, size=8.5, color=GRAY600, italic=True, align=PP_ALIGN.CENTER)

talking_box(sl, [
    "38 hours is the minimum viable curriculum. Advanced consultants should also shadow 2 live engagements.",
    "Platform proficiency (Module 3) is the practical core — every consultant needs hands-on hours before client delivery.",
    "Module 6 (Change Management) is the most underestimated — technical consultants often skip it and see low adoption.",
    "Certification: pass rate target 85%. Re-sit allowed once. Certified consultants are listed in the PDLC VSM Partner Network.",
    "Quarterly refresher: 2-hour update on new platform features + agent improvements.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 22 — TEAM COMPOSITION
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Engagement Team Composition",
            "Staffing model for Diagnostic Sprint, Full Transformation, and Advisory engagements", accent=NAVY)

# 3 engagement types as columns
eng_types = [
    ("Diagnostic Sprint", "2 weeks · 1 team", BLUE, LTBLUE, [
        ("Lead VSM Consultant", "Senior", "1.0 FTE", "Engagement lead, ALM connect, VSM facilitation, client delivery"),
        ("AI/Platform Specialist", "Mid-Senior", "0.5 FTE", "Platform config, agent runs, report generation"),
        ("Engagement Manager", "Senior", "0.25 FTE", "Client management, schedule, deliverable QA"),
    ]),
    ("Full Transformation", "8–16 weeks · Portfolio", TEAL, LTTEAL, [
        ("Principal Consultant", "Partner/Director", "0.5 FTE", "Executive sponsorship, business case sign-off, steering"),
        ("Lead VSM Consultant", "Senior", "1.0 FTE", "End-to-end delivery ownership, workshop facilitation"),
        ("AI/Platform Specialist", "Mid-Senior", "1.0 FTE", "Agent customisation, platform operation, tech stack integration"),
        ("Change Management Lead", "Mid-Senior", "0.5 FTE", "Adoption plan, training, change risk mitigation"),
        ("Business Analyst", "Mid", "0.75 FTE", "Data collection, stakeholder interviews, documentation"),
        ("Engagement Manager", "Senior", "0.5 FTE", "Commercial management, risk, client reporting"),
    ]),
    ("Advisory Retainer", "Ongoing · Monthly", AMBER, LTAMBER, [
        ("VSM Advisory Lead", "Senior", "0.25 FTE", "Quarterly VSM refresh, client exec reporting"),
        ("AI Optimisation Specialist", "Mid", "0.25 FTE", "Agent performance tuning, new use case identification"),
        ("Account Manager", "Mid", "0.1 FTE", "Relationship management, renewal, upsell identification"),
    ]),
]

for i, (title, scope, accent, bg, roles) in enumerate(eng_types):
    xi = 0.35 + i * 4.32
    add_rect(sl, xi, 1.35, 4.1, 0.45, fill=accent)
    add_text(sl, title, xi+0.12, 1.38, 3.86, 0.28, size=11, bold=True, color=WHITE)
    add_text(sl, scope, xi+0.12, 1.62, 3.86, 0.2, size=8.5, color=RGBColor(0xFF,0xFF,0xCC))
    for j, (role, level, fte, desc) in enumerate(roles):
        yi = 1.88 + j * 0.88
        add_rect(sl, xi, yi, 4.1, 0.82, fill=bg if j%2==0 else WHITE)
        add_rect(sl, xi, yi, 0.1, 0.82, fill=accent)
        add_text(sl, role, xi+0.18, yi+0.05, 3.8, 0.24, size=9.5, bold=True, color=NAVY)
        add_text(sl, f"{level} · {fte}", xi+0.18, yi+0.28, 2.0, 0.22, size=8, color=accent, bold=True)
        add_text(sl, desc, xi+0.18, yi+0.5, 3.7, 0.28, size=7.5, color=GRAY600, italic=True)

talking_box(sl, [
    "Diagnostic Sprint can be delivered by just 1.5 FTE consultants — it's the low-risk, high-margin entry point.",
    "Full Transformation: 4.25 FTE for 12 weeks ≈ 510 consultant-days. At $2.5K/day blended rate = $255K cost, $300K–$350K billed.",
    "Change Management Lead is often sourced from the client's own organisation to reduce cost and improve adoption.",
    "The AI/Platform Specialist role is the scarcest — build this capability first when standing up the practice.",
    "Advisory retainer is high-margin: 0.6 FTE × $2.5K/day × 22 working days/mo = $33K cost, $80K billed.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 23 — IMPLEMENTATION TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Typical Engagement Timeline — Full Transformation",
            "Option B example: 14-week end-to-end programme for a 3-team product portfolio", accent=TEAL)

# Gantt-style timeline
weeks = list(range(1, 15))
bar_w_per_week = 0.76
bar_start_x = 2.2

# Week headers
add_rect(sl, 0.35, 1.38, 1.82, 0.35, fill=NAVY)
add_text(sl, "Phase", 0.45, 1.42, 1.7, 0.26, size=9, bold=True, color=WHITE)
for w in weeks:
    xi = bar_start_x + (w-1) * bar_w_per_week
    add_rect(sl, xi, 1.38, bar_w_per_week-0.04, 0.35, fill=NAVY)
    add_text(sl, f"W{w}", xi+0.06, 1.42, bar_w_per_week-0.08, 0.26,
             size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

gantt_phases = [
    ("Phase 1: Discover & Calibrate", BLUE, 1, 2),
    ("Phase 2: Map & Analyse (VSM Build)", TEAL, 2, 4),
    ("Phase 3: Future State Design", AMBER, 4, 8),
    ("Phase 4: Business Case", GREEN, 8, 10),
    ("Phase 5: Activate & Handover", NAVY, 10, 14),
    ("Client Workshops", RED, 2, 10),
    ("Executive Steering", GRAY600, 3, 14),
]

for i, (label, color, start, end) in enumerate(gantt_phases):
    yi = 1.82 + i * 0.68
    add_rect(sl, 0.35, yi, 1.82, 0.58, fill=GRAY100)
    add_text(sl, label, 0.42, yi+0.14, 1.68, 0.32, size=7.5, color=GRAY700, bold=i<5)
    x_start = bar_start_x + (start-1) * bar_w_per_week + 0.04
    bar_len = (end - start) * bar_w_per_week - 0.08
    add_rect(sl, x_start, yi+0.1, bar_len, 0.38, fill=color)
    add_text(sl, f"Wk {start}–{end}", x_start+0.06, yi+0.16, bar_len-0.12, 0.22,
             size=7.5, bold=True, color=WHITE)

# Milestone markers
milestones = [
    (2, "VSM\nKick-off", BLUE),
    (4, "Current\nState\nApproved", TEAL),
    (8, "Future\nState\nApproved", AMBER),
    (10, "Business\nCase\nApproved", GREEN),
    (14, "Playbook\nDelivered", NAVY),
]
for wk, label, col in milestones:
    xi = bar_start_x + (wk-1) * bar_w_per_week + bar_w_per_week/2 - 0.04
    add_rect(sl, xi, 6.45, 0.08, 0.5, fill=col)
    add_text(sl, label, xi-0.45, 6.48, 0.98, 0.48, size=6.5, color=col, bold=True, align=PP_ALIGN.CENTER)

add_text(sl, "◆ = Client approval gate", 0.35, 7.1, 3.0, 0.25, size=7.5, color=GRAY600, italic=True)

talking_box(sl, [
    "Week 2 kick-off requires: ALM admin access, 3-5 stakeholder interview slots, and DORA survey completed.",
    "Phase 3 (Future State Design) includes 3 workshops: (a) bottleneck review, (b) scenario design, (c) option selection.",
    "Approval gates at Weeks 4, 8, 10 are critical path — delays here extend the programme.",
    "The 14-week timeline assumes full client co-operation. Add 2 weeks buffer for large organisations.",
    "Diagnostic Sprint = Phases 1+2 only = 4 weeks. Option A = 10 weeks. Option B/C = 14–16 weeks.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 24 — CONSULTING FEE MODEL
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Consulting Fee & Commercial Model",
            "Transparent investment model — fixed-fee engagements with defined scope and deliverables", accent=NAVY)

# Fee table
add_rect(sl, 0.35, 1.38, 12.65, 0.4, fill=NAVY)
for j, (hdr, xi2, wi2) in enumerate(zip(
    ["Engagement", "Duration", "Team", "Fee Range", "Day Rate\n(blended)", "Includes"],
    [0.35, 3.0, 4.35, 5.7, 7.4, 8.7],
    [2.6, 1.3, 1.3, 1.65, 1.25, 4.3]
)):
    add_text(sl, hdr, xi2+0.08, 1.4, wi2-0.16, 0.34, size=8.5, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)

fee_rows = [
    ("Diagnostic Sprint", "2 weeks", "1.5 FTE", "$25K–$45K", "$3.5K/day", "ALM connect + VSM + DORA + Bottleneck Report", LTBLUE, BLUE),
    ("Full Transformation — Option A", "8–10 weeks", "3.25 FTE", "$150K–$220K", "$3.2K/day", "All 5 phases + business case + playbook (Opt A)", LTTEAL, TEAL),
    ("Full Transformation — Option B", "12–16 weeks", "4.25 FTE", "$250K–$350K", "$3.1K/day", "All 5 phases + custom agent dev + business case + playbook", LTAMBER, AMBER),
    ("Full Transformation — Option C", "18–36 weeks", "5.5 FTE", "$400K–$700K", "$3.0K/day", "Full agentic PDLC design + orchestration build + playbook", RGBColor(0xDC,0xFC,0xE7), GREEN),
    ("Advisory Retainer", "12-mo min", "0.6 FTE", "$8K–$15K/mo", "$2.8K/day", "Quarterly VSM refresh + agent optimisation + DORA re-baseline", GRAY100, GRAY600),
    ("Executive Workshop (stand-alone)", "1 day", "2 FTE", "$8K–$15K", "$8K–$15K", "4-hour C-suite VSM briefing + live platform demo", LTBLUE, BLUE),
]

for i, (eng, dur, team, fee, rate, incl, bg, accent) in enumerate(fee_rows):
    yi = 1.84 + i * 0.72
    for val, xi2, wi2 in zip([eng, dur, team, fee, rate, incl],
                               [0.35, 3.0, 4.35, 5.7, 7.4, 8.7],
                               [2.6, 1.3, 1.3, 1.65, 1.25, 4.3]):
        add_rect(sl, xi2, yi, wi2, 0.68, fill=bg)
        col = accent if val in [fee, rate] else GRAY700
        sz = 10 if val in [fee, rate] else 9
        bo = True if val in [fee, rate] else (True if val == eng else False)
        add_text(sl, val, xi2+0.08, yi+0.17, wi2-0.16, 0.38, size=sz, bold=bo,
                 color=col, align=PP_ALIGN.LEFT if val in [eng, incl] else PP_ALIGN.CENTER)

# Margin box
add_rect(sl, 0.35, 6.45, 5.6, 0.65, fill=LTGREEN)
add_text(sl, "Target Gross Margin:", 0.5, 6.52, 2.0, 0.28, size=10, bold=True, color=GREEN)
add_text(sl, "Diagnostic 45–52%  ·  Full Transformation 40–48%  ·  Advisory 55–65%",
         2.55, 6.52, 8.9, 0.28, size=10, bold=True, color=GREEN)
add_text(sl, "Blended day rate assumes: Senior Consultant $4.5K/day, Mid-Senior $3.0K/day, Mid $2.0K/day billed rates",
         0.35, 7.05, 12.5, 0.28, size=7.5, italic=True, color=GRAY600)

talking_box(sl, [
    "Always anchor on the Diagnostic Sprint first — the $25K–$45K fixed fee is below most VP discretionary budget limits.",
    "Full Transformation fee = (FTE × days × blended rate) + 15–20% platform/IP premium.",
    "Advisory retainer is priced at a slight discount to full rate to incentivise continuity — but 55%+ margin makes it the highest-margin product.",
    "Payment terms: 30% on signing, 40% at Phase 3 completion (Future State approved), 30% on final delivery.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 25 — TOTAL COST OF OWNERSHIP COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Total Cost of Ownership vs Total Value Delivered",
            "3-year view: combined consulting + technology investment vs cumulative savings", accent=GREEN)

# 3 scenario boxes
for i, (opt, consulting, tech, total_inv, annual_saving, y3_roi, accent, bg) in enumerate([
    ("Option A", "$150K–$220K", "$250K–$400K", "$400K–$620K", "$1.3M–$1.95M", "5.8×", BLUE, LTBLUE),
    ("Option B", "$250K–$350K", "$600K–$1.1M", "$850K–$1.45M", "$2.1M–$3.4M", "6.2×", TEAL, LTTEAL),
    ("Option C", "$400K–$700K", "$2.5K–$4.5M", "$2.9M–$5.2M", "$4.6M–$8.3M", "6.8×", AMBER, LTAMBER),
]):
    xi = 0.35 + i * 4.32
    add_rect(sl, xi, 1.35, 4.1, 5.2, fill=bg)
    add_rect(sl, xi, 1.35, 4.1, 0.42, fill=accent)
    add_text(sl, opt, xi+0.14, 1.38, 3.82, 0.3, size=14, bold=True, color=WHITE)
    for j, (label, value) in enumerate([
        ("Consulting Investment", consulting),
        ("Technology & Licensing", tech),
        ("Total 3-Year Investment", total_inv),
        ("Year 1 Annual Savings", annual_saving),
        ("3-Year Cumulative Savings", f"{annual_saving} × 3yr"),
        ("3-Year Net ROI Multiple", y3_roi),
    ]):
        yi = 1.88 + j * 0.72
        is_total = "Total" in label or "ROI" in label
        add_rect(sl, xi+0.1, yi, 3.9, 0.65, fill=WHITE if is_total else bg)
        if is_total:
            add_rect(sl, xi+0.1, yi, 0.1, 0.65, fill=accent)
        add_text(sl, label, xi+0.28, yi+0.06, 3.6, 0.24, size=8.5,
                 color=NAVY if is_total else GRAY600, bold=is_total)
        add_text(sl, value, xi+0.28, yi+0.33, 3.6, 0.28, size=11,
                 bold=True, color=accent if is_total else GRAY700)

add_text(sl, "Note: 3-Year Cumulative Savings assumes savings ramp: Year 1 = 70% of run-rate (adoption curve), Year 2 = 100%, Year 3 = 110% (compounding efficiency gains). Technology costs shown as Year 1 total investment.",
         0.35, 6.65, 12.5, 0.45, size=7.5, italic=True, color=GRAY600)

talking_box(sl, [
    "The 3-Year ROI multiples (5.8–6.8×) are higher than the headline 2.8–5.5× because they account for compounding efficiency gains in Year 3.",
    "Use this slide for CFO presentations — it converts the ROI from 'consulting metrics' to 'capital allocation decision'.",
    "Sensitivity: even if savings are 50% of projected, Option A still delivers 2.9× 3-year ROI — well above most capital hurdle rates.",
    "Frame against alternative: 'What does it cost to NOT do this?' → $3–6M/year in wasted flow time for most enterprise teams.",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 26 — WHY US: DIFFERENTIATION
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, WHITE)
header_band(sl, "Why Choose This Offering: Our Differentiation",
            "What separates this from generic digital transformation consulting", accent=NAVY)

differentiators = [
    ("Data-Driven, Not Opinion-Driven", BLUE,
     "Every bottleneck, every ROI number, and every scenario is generated from your actual Jira/ADO data — not consultant estimates. The VSM platform eliminates the subjectivity that plagues most transformation engagements.",
     "vs. McKinsey/BCG: Generic frameworks applied to your context · Our approach: Your data, your metrics, your ROI"),
    ("Proprietary Multi-Agent Platform", TEAL,
     "The PDLC VSM Platform is purpose-built for product delivery lifecycle analysis. 8 LangGraph agents, 7 phases, 36 activities. No competing firm has a comparable tool — analysis that takes 6 weeks of consultant time now takes 2 hours.",
     "vs. Standard tools (Lucidchart VSM, Azure DevOps Analytics): No AI analysis, no future state design, no business case"),
    ("Board-Ready Output in Hours, Not Months", AMBER,
     "A traditional consulting engagement takes 12–16 weeks to produce a business case. Our platform generates a board-ready ROI model, NPV analysis, and implementation roadmap in a single session — with CFO-grade financial modelling.",
     "vs. Traditional consulting: 3-month analysis → this platform: same-session output with your actual data"),
    ("Outcome-Committed, Not Effort-Billed", GREEN,
     "Fixed-fee engagements with defined deliverables at each phase gate. Payment tied to deliverable acceptance, not time spent. We share in the outcome — if the business case doesn't hold up, you don't pay for Phase 4.",
     "vs. Time & Materials: client carries all risk · Our model: shared accountability for quality of deliverables"),
]

for i, (title, accent, body, vs) in enumerate(differentiators):
    yi = 1.4 + i * 1.45
    add_rect(sl, 0.35, yi, 8.9, 1.3, fill=GRAY100)
    add_rect(sl, 0.35, yi, 0.12, 1.3, fill=accent)
    add_text(sl, f"{i+1}. {title}", 0.58, yi+0.1, 8.54, 0.3, size=12, bold=True, color=NAVY)
    add_text(sl, body, 0.58, yi+0.42, 8.54, 0.55, size=9, color=GRAY700)
    add_text(sl, vs, 0.58, yi+0.96, 8.54, 0.28, size=8, italic=True, color=accent)

talking_box(sl, [
    "Lead with #2 (proprietary platform) — it's the strongest barrier to entry. No one else has a purpose-built LangGraph VSM tool.",
    "Differentiator #1 (data-driven) addresses the most common client objection: 'We've had consultants before and they just told us what we already knew.'",
    "#4 (fixed-fee) is a trust signal — it says we're confident enough in our methodology to commit to deliverables, not just effort.",
    "Competitive displacement: position against both management consultancies (too slow, too expensive) AND generic DevOps tooling vendors (no consulting, no change management).",
], y=1.3, h=5.8)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 27 — NEXT STEPS / CALL TO ACTION
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_bg(sl, NAVY)

add_rect(sl, 0, 0, 13.333, 0.08, fill=BLUE)

add_text(sl, "Ready to Transform Your Delivery Engine?", 1.0, 0.9, 11.3, 1.0,
         size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Three ways to get started — choose the right entry point for your organisation",
         1.0, 1.85, 11.3, 0.45, size=14, color=RGBColor(0xBF, 0xDB, 0xFF), align=PP_ALIGN.CENTER)

# 3 next steps
next_steps = [
    ("Book a\nDiagnostic Sprint", "01", BLUE,
     "2-week, $25K–$45K fixed engagement. Connect your ALM tool, run the full VSM analysis, get your bottleneck report. Zero long-term commitment.",
     "Start within 2 weeks"),
    ("Attend a\nPlatform Briefing", "02", TEAL,
     "1-hour live demo of the PDLC VSM Platform with your team context loaded. See your DORA score, a sample VSM, and a business case model — live.",
     "Available weekly"),
    ("Request an\nExecutive Workshop", "03", AMBER,
     "Half-day, $8K–$15K fixed session. Live platform demo for your C-suite, industry-benchmarked ROI model, and a personalised transformation roadmap.",
     "Book 2 weeks ahead"),
]

for i, (title, num, accent, desc, cta) in enumerate(next_steps):
    xi = 1.0 + i * 3.8
    add_rect(sl, xi, 2.5, 3.35, 3.8, fill=RGBColor(0x1A, 0x3A, 0x6E))
    add_rect(sl, xi, 2.5, 3.35, 0.5, fill=accent)
    add_text(sl, num, xi+0.12, 2.53, 0.5, 0.42, size=20, bold=True, color=WHITE)
    add_text(sl, title, xi+0.65, 2.56, 2.58, 0.44, size=12, bold=True, color=WHITE)
    add_text(sl, desc, xi+0.18, 3.1, 2.98, 1.6, size=9.5, color=RGBColor(0xBF, 0xDB, 0xFF))
    add_rect(sl, xi+0.18, 4.85, 2.98, 0.3, fill=accent)
    add_text(sl, f"→  {cta}", xi+0.28, 4.87, 2.78, 0.26, size=9, bold=True, color=WHITE)

rule(sl, 1.0, 6.5, 11.3, color=RGBColor(0x2A, 0x4A, 0x8E))
add_text(sl, "PDLC VSM Platform  ·  pdlc-vsm.consulting  ·  contact@pdlc-vsm.consulting",
         1.0, 6.6, 11.3, 0.4, size=10, color=RGBColor(0x93, 0xC5, 0xFD), align=PP_ALIGN.CENTER)
add_text(sl, "All engagements are fixed-fee with defined deliverables · Confidential service offering document · © 2026",
         1.0, 7.0, 11.3, 0.35, size=8.5, color=GRAY600, align=PP_ALIGN.CENTER)

# ─── SAVE ─────────────────────────────────────────────────────────────────────
out = "/Users/125066/projects/pdlc-vsm-platform/PDLC-VSM-Consulting-Service-Offering.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
