"""
PDLC System Landscape — Option A / B / C
Three slides recreating the original US Bank PDLC view with:
  - PDLC phases & activities row inserted between Personas and AI Systems
  - Option A: AI as Assistants / Co-Pilots
  - Option B: Selective Autonomous Agents
  - Option C: Agent-First Orchestration (humans oversee only)
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

# ── Palette (US Bank / STUMP brand) ──────────────────────────────────────────
NAVY    = RGBColor(0x00, 0x00, 0x48)
BLUE    = RGBColor(0x2F, 0x78, 0xC4)
TEAL    = RGBColor(0x06, 0xC7, 0xCC)
PURPLE  = RGBColor(0x2E, 0x30, 0x8E)
LBLUE   = RGBColor(0x92, 0xBB, 0xE6)
LPURP   = RGBColor(0x73, 0x73, 0xD8)
LTEAL   = RGBColor(0xB3, 0xF0, 0xF2)
LNAVY   = RGBColor(0xD7, 0xE8, 0xF9)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
OFFWH   = RGBColor(0xF8, 0xF9, 0xFF)
LGRAY   = RGBColor(0xF3, 0xF4, 0xF6)
DGRAY   = RGBColor(0x1F, 0x29, 0x37)
MGRAY   = RGBColor(0x6B, 0x72, 0x80)
GREENA  = RGBColor(0x05, 0x7A, 0x55)   # GA badge
AMBER   = RGBColor(0xB4, 0x5A, 0x09)   # Pilot badge
REDPOC  = RGBColor(0x9B, 0x1C, 0x1C)   # PoC badge
AUTOGRN = RGBColor(0x05, 0x7A, 0x55)   # Autonomous badge

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ── Grid constants ────────────────────────────────────────────────────────────
LM  = Inches(0.14)           # left margin
LW  = Inches(0.82)           # label column width
CW  = Inches(1.757)          # phase column width  (7 cols)
GAP = Inches(0.0)            # gap between columns (0 = flush)
# Phase column X start positions
PX  = [LM + LW + i * CW for i in range(7)]
# Inner padding inside each cell
IP  = Inches(0.07)

# ── Row Y positions & heights ─────────────────────────────────────────────────
Y_TITLE   = Inches(0.00);  H_TITLE   = Inches(0.40)
Y_BANNER  = Inches(0.40);  H_BANNER  = Inches(0.26)
Y_PHDR    = Inches(0.66);  H_PHDR    = Inches(0.32)   # phase name headers
Y_PER     = Inches(0.98);  H_PER     = Inches(1.02)   # Personas row
Y_PDLC    = Inches(2.00);  H_PDLC    = Inches(0.88)   # PDLC activities row (NEW)
Y_AI      = Inches(2.88)                                # AI Systems row (height varies)
Y_TGT     = Inches(4.88);  H_TGT     = Inches(0.82)   # Target Systems row
Y_PLAT    = Inches(5.74);  H_PLAT    = Inches(0.55)   # Platforms legend
Y_FOOT    = Inches(7.22);  H_FOOT    = Inches(0.28)

H_AI_A = Inches(2.00)
H_AI_B = Inches(2.00)
H_AI_C = Inches(2.00)

# ── Helpers ───────────────────────────────────────────────────────────────────

def R(sl, x, y, w, h, fill=None, line=None, lw=Pt(0.5)):
    s = sl.shapes.add_shape(1, x, y, w, h)
    s.fill.solid() if fill else s.fill.background()
    if fill: s.fill.fore_color.rgb = fill
    if line: s.line.color.rgb = line; s.line.width = lw
    else: s.line.fill.background()
    return s

def T(sl, text, x, y, w, h, size=Pt(8), bold=False, color=DGRAY,
      align=PP_ALIGN.LEFT, italic=False, wrap=True):
    b  = sl.shapes.add_textbox(x, y, w, h)
    tf = b.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    r  = p.add_run()
    r.text = text
    r.font.size   = size
    r.font.bold   = bold
    r.font.color.rgb = color
    r.font.italic = italic
    return b

def chip(sl, text, x, y, w, h=Inches(0.22),
         bg=LNAVY, fg=NAVY, size=Pt(7.5), bold=False):
    """Small rounded-feel chip."""
    R(sl, x, y, w, h, fill=bg, line=RGBColor(
        max(bg.red-30,0), max(bg.green-30,0), max(bg.blue-30,0)), lw=Pt(0.4))
    T(sl, text, x + Inches(0.04), y + Inches(0.02),
      w - Inches(0.06), h - Inches(0.04),
      size=size, bold=bold, color=fg, align=PP_ALIGN.LEFT)

def badge(sl, label, x, y, bg, fg=WHITE):
    """Tiny status badge pill."""
    R(sl, x, y, Inches(0.38), Inches(0.16), fill=bg)
    T(sl, label, x, y, Inches(0.38), Inches(0.16),
      size=Pt(6), bold=True, color=fg, align=PP_ALIGN.CENTER)

def row_label(sl, text, y, h, bg=NAVY):
    """Left-side section row label."""
    R(sl, LM, y, LW, h, fill=bg)
    T(sl, text, LM + Inches(0.04), y + Inches(0.04),
      LW - Inches(0.06), h - Inches(0.06),
      size=Pt(7.5), bold=True, color=WHITE, align=PP_ALIGN.LEFT)

def col_dividers(sl, y, h, light=True):
    """Vertical dividers between phase columns."""
    for i in range(1, 7):
        lx = PX[i]
        c = RGBColor(0xC5,0xD8,0xEF) if light else RGBColor(0x20,0x20,0x60)
        R(sl, lx, y, Inches(0.015), h, fill=c)

# ── PDLC Phase definitions ────────────────────────────────────────────────────
PHASES = [
    ("1", "Discovery &\nPlanning"),
    ("2", "Architecture\n& Design"),
    ("3", "Development"),
    ("4", "Build &\nCI/CD"),
    ("5", "Test &\nQA"),
    ("6", "Release &\nDeploy"),
    ("7", "Operate &\nMonitor"),
]

PHASE_ACTIVITIES = [
    ["Feature Definition", "Backlog Grooming", "Sprint Planning"],
    ["System Design", "UI/UX Wireframes", "Tech Spikes"],
    ["Feature Coding", "Code Review", "PR Management"],
    ["Build Automation", "Unit Testing", "Code Quality Scan"],
    ["Integration Testing", "UAT", "Regression Testing"],
    ["Release Gate Review", "Deployment", "Change Approval"],
    ["System Monitoring", "Incident Response", "Compliance Review"],
]

PERSONAS_PER_PHASE = [
    [("Product Manager", "Requirements"), ("Agilist", "Sprint Planning")],
    [("Designer", "UI/UX"), ("Product Manager", "Sign-off")],
    [("Engineer", "Builds Code")],
    [("Engineer", "Builds Code")],
    [("Engineer", "Validates"), ("Agilist", "Acceptance")],
    [("Engineer", "Deploys"), ("Risk Manager", "Approval")],
    [("Risk Manager", "Compliance"), ("Engineer", "On-Call")],
]

TARGET_PER_PHASE = [
    ["Jira", "Confluence"],
    ["Figma", "ShieldDocs"],
    ["GitLab", "Shield UI"],
    ["PipelineCli", "DevContainers"],
    ["PractiTest", "BrowserStack"],
    ["AppSec", "CloudBees"],
    ["Archer", "Risk Database"],
]

PLATFORMS = [
    ("GitHub Copilot", "Module: GPT, Claude, Gemini · MCP · Agents · Skills"),
    ("Azure Open AI", "Module: GPT · Services: Azure AI Search, AI Foundry, LangChain, MCP"),
]

# ── AI Systems per option ─────────────────────────────────────────────────────
# Each entry: (agent_name, badge_text, bg_color, text_color)
_GA  = (GREENA, WHITE)
_PIL = (AMBER,  WHITE)
_POC = (REDPOC, WHITE)

ASSIST_CHIP = RGBColor(0xDB,0xEA,0xFE)   # light blue — assistant mode
AUTO_CHIP   = RGBColor(0xD1,0xFA,0xEA)   # light green — autonomous
ORCH_CHIP   = RGBColor(0xED,0xE9,0xFE)   # light purple — orchestrated agent

AI_A = [   # Option A — Co-Pilot / Assistant mode
    [("Backlog Assistant",    "GA",    ASSIST_CHIP, NAVY),
     ("USB Docs",             "GA",    ASSIST_CHIP, NAVY)],
    [("Figma AI",             "Pilot", ASSIST_CHIP, NAVY),
     ("UX Design Coder MCP",  "Pilot", ASSIST_CHIP, NAVY)],
    [("Code Review Asst.",    "GA",    ASSIST_CHIP, NAVY),
     ("Prompt Library",       "GA",    ASSIST_CHIP, NAVY),
     ("DevBridge",            "GA",    ASSIST_CHIP, NAVY)],
    [("PipelineIQ",           "Pilot", ASSIST_CHIP, NAVY)],
    [("QA Suite",             "GA",    ASSIST_CHIP, NAVY),
     ("Smart Tester",         "Pilot", ASSIST_CHIP, NAVY),
     ("Playwright MCP",       "Pilot", ASSIST_CHIP, NAVY)],
    [("ConsoleBot",           "PoC",   ASSIST_CHIP, NAVY),
     ("RenovateBot",          "Pilot", ASSIST_CHIP, NAVY)],
    [("Risk Assistant",       "Pilot", ASSIST_CHIP, NAVY)],
]

AI_B = [   # Option B — Selective Autonomous Agents
    [("Smart Backlog Agent",  "AUTO",  AUTO_CHIP,   GREENA),
     ("USB Docs",             "ASSIST",ASSIST_CHIP, NAVY)],
    [("UX Design Agent",      "AUTO",  AUTO_CHIP,   GREENA),
     ("Design Review Agent",  "AUTO",  AUTO_CHIP,   GREENA)],
    [("CodeGen Agent",        "AUTO",  AUTO_CHIP,   GREENA),
     ("Code Review Agent",    "AUTO",  AUTO_CHIP,   GREENA),
     ("Prompt Library",       "ASSIST",ASSIST_CHIP, NAVY)],
    [("Pipeline Agent",       "AUTO",  AUTO_CHIP,   GREENA)],
    [("QA Orchestrator",      "AUTO",  AUTO_CHIP,   GREENA),
     ("Playwright Agent",     "AUTO",  AUTO_CHIP,   GREENA),
     ("Smart Tester",         "ASSIST",ASSIST_CHIP, NAVY)],
    [("Release Manager Agent","AUTO",  AUTO_CHIP,   GREENA),
     ("RenovateBot",          "ASSIST",ASSIST_CHIP, NAVY)],
    [("Risk & Compliance Agt","AUTO",  AUTO_CHIP,   GREENA)],
]

AI_C = [   # Option C — Agent-First Orchestration
    [("Discovery Agent",      "AGENT", ORCH_CHIP, PURPLE),
     ("Backlog Agent",        "AGENT", ORCH_CHIP, PURPLE),
     ("Sprint Agent",         "AGENT", ORCH_CHIP, PURPLE)],
    [("Architecture Agent",   "AGENT", ORCH_CHIP, PURPLE),
     ("UI/UX Agent",          "AGENT", ORCH_CHIP, PURPLE),
     ("Design Review Agent",  "AGENT", ORCH_CHIP, PURPLE)],
    [("Code Generator",       "AGENT", ORCH_CHIP, PURPLE),
     ("Code Reviewer",        "AGENT", ORCH_CHIP, PURPLE),
     ("Tech Debt Agent",      "AGENT", ORCH_CHIP, PURPLE)],
    [("Build Agent",          "AGENT", ORCH_CHIP, PURPLE),
     ("Test Runner Agent",    "AGENT", ORCH_CHIP, PURPLE),
     ("Quality Gate Agent",   "AGENT", ORCH_CHIP, PURPLE)],
    [("QA Orchestrator",      "AGENT", ORCH_CHIP, PURPLE),
     ("UAT Agent",            "AGENT", ORCH_CHIP, PURPLE),
     ("Security Scanner",     "AGENT", ORCH_CHIP, PURPLE)],
    [("Release Gate Agent",   "AGENT", ORCH_CHIP, PURPLE),
     ("Deploy Agent",         "AGENT", ORCH_CHIP, PURPLE),
     ("Rollback Agent",       "AGENT", ORCH_CHIP, PURPLE)],
    [("Monitor Agent",        "AGENT", ORCH_CHIP, PURPLE),
     ("Incident Triage Agt",  "AGENT", ORCH_CHIP, PURPLE),
     ("Compliance Agent",     "AGENT", ORCH_CHIP, PURPLE)],
]

BADGE_COLORS = {
    "GA":     (GREENA, WHITE),
    "Pilot":  (AMBER,  WHITE),
    "PoC":    (REDPOC, WHITE),
    "AUTO":   (GREENA, WHITE),
    "ASSIST": (BLUE,   WHITE),
    "AGENT":  (PURPLE, WHITE),
}

# ── Slide builder ─────────────────────────────────────────────────────────────

def make_slide(option_letter, option_title, option_subtitle,
               ai_data, banner_color, option_accent,
               show_orchestration=False):

    sl = prs.slides.add_slide(BLANK)

    # ── Background ────────────────────────────────────────────────────────────
    R(sl, 0, 0, W, H, fill=WHITE)

    # ── Title bar ─────────────────────────────────────────────────────────────
    R(sl, 0, Y_TITLE, W, H_TITLE, fill=NAVY)
    R(sl, 0, Y_TITLE, Inches(0.1), H_TITLE, fill=TEAL)
    T(sl, "PDLC System Landscape",
      Inches(0.22), Y_TITLE + Inches(0.06),
      Inches(6), Inches(0.28),
      size=Pt(16), bold=True, color=WHITE)
    T(sl, "Personas  ·  PDLC Activities  ·  AI Systems  ·  Target Systems",
      Inches(0.22), Y_TITLE + Inches(0.24),
      Inches(7), Inches(0.14),
      size=Pt(8), color=LBLUE)
    T(sl, "PDLC System Landscape  |  Generated 2026-04",
      Inches(10.5), Y_TITLE + Inches(0.13),
      Inches(2.7), Inches(0.14),
      size=Pt(7), color=LBLUE, align=PP_ALIGN.RIGHT)

    # ── Option banner ─────────────────────────────────────────────────────────
    R(sl, 0, Y_BANNER, W, H_BANNER, fill=banner_color)
    T(sl, option_title,
      Inches(0.22), Y_BANNER + Inches(0.04),
      Inches(8), Inches(0.2),
      size=Pt(10), bold=True, color=WHITE)
    T(sl, option_subtitle,
      Inches(8.5), Y_BANNER + Inches(0.05),
      Inches(4.7), Inches(0.18),
      size=Pt(8.5), color=WHITE, italic=True, align=PP_ALIGN.RIGHT)

    # ── Phase column headers ──────────────────────────────────────────────────
    R(sl, LM + LW, Y_PHDR, W - LM - LW - Inches(0.14),
      H_PHDR, fill=NAVY)
    # label stub
    R(sl, LM, Y_PHDR, LW, H_PHDR, fill=NAVY)
    T(sl, "PHASE", LM + Inches(0.04), Y_PHDR + Inches(0.08),
      LW - Inches(0.06), Inches(0.18),
      size=Pt(7), bold=True, color=LBLUE)

    PHASE_HEADER_COLORS = [
        RGBColor(0x00,0x00,0x48),  # Ph1 navy
        RGBColor(0x2E,0x30,0x8E),  # Ph2 purple
        RGBColor(0x2F,0x78,0xC4),  # Ph3 blue
        RGBColor(0x0A,0x5C,0x8A),  # Ph4 dark teal-blue
        RGBColor(0x2E,0x30,0x8E),  # Ph5 purple
        RGBColor(0x2F,0x78,0xC4),  # Ph6 blue
        RGBColor(0x04,0x8A,0x8E),  # Ph7 teal
    ]
    for i, (num, name) in enumerate(PHASES):
        x = PX[i] + Inches(0.02)
        R(sl, PX[i], Y_PHDR, CW - Inches(0.02), H_PHDR, fill=PHASE_HEADER_COLORS[i])
        T(sl, f"Ph{num}  {name}",
          x + IP, Y_PHDR + Inches(0.04),
          CW - IP*2 - Inches(0.04), H_PHDR - Inches(0.06),
          size=Pt(7.5), bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # ── PERSONAS row ──────────────────────────────────────────────────────────
    R(sl, LM, Y_PER, W - LM - Inches(0.14), H_PER,
      fill=RGBColor(0xEB,0xF3,0xFD), line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.5))
    col_dividers(sl, Y_PER, H_PER)
    row_label(sl, "PERSONAS", Y_PER, H_PER, bg=NAVY)

    for i, personas in enumerate(PERSONAS_PER_PHASE):
        x = PX[i]
        for pi, (pname, prole) in enumerate(personas):
            cy = Y_PER + IP + pi * Inches(0.44)
            R(sl, x + IP, cy, CW - IP*2, Inches(0.40),
              fill=WHITE, line=LBLUE, lw=Pt(0.5))
            R(sl, x + IP, cy, CW - IP*2, Inches(0.17), fill=NAVY)
            T(sl, pname, x + IP + Inches(0.04), cy + Inches(0.02),
              CW - IP*2 - Inches(0.06), Inches(0.14),
              size=Pt(7.5), bold=True, color=WHITE)
            T(sl, prole, x + IP + Inches(0.04), cy + Inches(0.19),
              CW - IP*2 - Inches(0.06), Inches(0.18),
              size=Pt(7), color=MGRAY)

    # ── PDLC ACTIVITIES row (NEW) ─────────────────────────────────────────────
    R(sl, LM, Y_PDLC, W - LM - Inches(0.14), H_PDLC,
      fill=RGBColor(0xF0,0xF4,0xFF), line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.5))
    col_dividers(sl, Y_PDLC, H_PDLC)
    row_label(sl, "PDLC\nACTIVITIES", Y_PDLC, H_PDLC,
              bg=RGBColor(0x1D,0x44,0x8A))

    for i, acts in enumerate(PHASE_ACTIVITIES):
        x = PX[i]
        for ai_idx, act in enumerate(acts):
            ay = Y_PDLC + IP + ai_idx * Inches(0.26)
            # small bullet dot
            R(sl, x + IP + Inches(0.02), ay + Inches(0.09),
              Inches(0.05), Inches(0.05), fill=BLUE)
            T(sl, act,
              x + IP + Inches(0.1), ay + Inches(0.02),
              CW - IP*2 - Inches(0.1), Inches(0.24),
              size=Pt(7.5), color=DGRAY)

    # ── AI SYSTEMS row ────────────────────────────────────────────────────────
    H_AI = H_AI_A   # same height for all options
    ai_bg = {
        "A": RGBColor(0xEB,0xF3,0xFD),
        "B": RGBColor(0xEC,0xFD,0xF3),
        "C": RGBColor(0xF3,0xF0,0xFF),
    }[option_letter]
    R(sl, LM, Y_AI, W - LM - Inches(0.14), H_AI,
      fill=ai_bg, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.5))
    col_dividers(sl, Y_AI, H_AI)

    ai_label_color = {
        "A": NAVY, "B": RGBColor(0x06,0x5F,0x46), "C": PURPLE
    }[option_letter]
    row_label(sl, "AI\nSYSTEMS", Y_AI, H_AI, bg=ai_label_color)

    # For Option C — "OVERSEE · REVIEW · APPROVE" human oversight strip
    if show_orchestration:
        R(sl, LM + LW, Y_AI, W - LM - LW - Inches(0.14), Inches(0.22),
          fill=RGBColor(0xF9,0xF0,0xFF), line=PURPLE, lw=Pt(0.5))
        T(sl, "👤  Human Role:  OVERSEE  ·  REVIEW  ·  APPROVE  only",
          LM + LW + Inches(0.1), Y_AI + Inches(0.04),
          W - LM - LW - Inches(0.3), Inches(0.18),
          size=Pt(7.5), bold=True, color=PURPLE, align=PP_ALIGN.CENTER)
        agent_y_offset = Inches(0.26)
    else:
        agent_y_offset = Inches(0.06)

    for i, agents in enumerate(ai_data):
        x = PX[i]
        for ag_idx, (aname, abadge, abg, afg) in enumerate(agents):
            ay = Y_AI + agent_y_offset + ag_idx * Inches(0.54)
            # chip background
            R(sl, x + IP, ay, CW - IP*2, Inches(0.50),
              fill=abg, line=RGBColor(
                  max(abg[0]-25,0), max(abg[1]-25,0), max(abg[2]-25,0)),
              lw=Pt(0.4))
            # badge strip top
            bc, bfg = BADGE_COLORS.get(abadge, (MGRAY, WHITE))
            R(sl, x + IP, ay, CW - IP*2, Inches(0.16), fill=bc)
            T(sl, abadge, x + IP + Inches(0.02), ay + Inches(0.02),
              Inches(0.5), Inches(0.13),
              size=Pt(6), bold=True, color=bfg)
            # agent name
            T(sl, aname, x + IP + Inches(0.04), ay + Inches(0.17),
              CW - IP*2 - Inches(0.06), Inches(0.30),
              size=Pt(7.5), bold=True, color=afg)

    # Option C orchestration arrows between phases
    if show_orchestration:
        arrow_y = Y_AI + H_AI - Inches(0.22)
        for i in range(6):
            ax = PX[i] + CW - Inches(0.04)
            R(sl, ax, arrow_y, Inches(0.14), Inches(0.16),
              fill=PURPLE)
            T(sl, "→", ax, arrow_y,
              Inches(0.14), Inches(0.16),
              size=Pt(9), bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # ── TARGET SYSTEMS row ────────────────────────────────────────────────────
    R(sl, LM, Y_TGT, W - LM - Inches(0.14), H_TGT,
      fill=RGBColor(0xF8,0xF8,0xFC), line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.5))
    col_dividers(sl, Y_TGT, H_TGT)
    row_label(sl, "TARGET\nSYSTEMS", Y_TGT, H_TGT, bg=MGRAY)

    for i, tools in enumerate(TARGET_PER_PHASE):
        x = PX[i]
        for ti, tool in enumerate(tools):
            ty = Y_TGT + IP + ti * Inches(0.36)
            R(sl, x + IP, ty, CW - IP*2, Inches(0.30),
              fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.4))
            T(sl, tool, x + IP + Inches(0.06), ty + Inches(0.07),
              CW - IP*2 - Inches(0.08), Inches(0.18),
              size=Pt(7.5), color=DGRAY, bold=False)

    # ── PLATFORMS legend ──────────────────────────────────────────────────────
    R(sl, LM, Y_PLAT, W - LM - Inches(0.14), H_PLAT,
      fill=OFFWH, line=LBLUE, lw=Pt(0.5))
    T(sl, "PLATFORMS",
      LM + Inches(0.08), Y_PLAT + Inches(0.05),
      Inches(0.9), Inches(0.18),
      size=Pt(7.5), bold=True, color=NAVY)

    for pi, (pname, pdesc) in enumerate(PLATFORMS):
        px2 = LM + Inches(1.05) + pi * Inches(5.8)
        R(sl, px2, Y_PLAT + Inches(0.06),
          Inches(5.6), Inches(0.42),
          fill=WHITE, line=LBLUE, lw=Pt(0.5))
        R(sl, px2, Y_PLAT + Inches(0.06),
          Inches(5.6), Inches(0.16), fill=NAVY)
        T(sl, pname, px2 + Inches(0.08), Y_PLAT + Inches(0.07),
          Inches(5.4), Inches(0.14),
          size=Pt(7.5), bold=True, color=WHITE)
        T(sl, pdesc, px2 + Inches(0.08), Y_PLAT + Inches(0.23),
          Inches(5.4), Inches(0.22),
          size=Pt(7), color=MGRAY)

    # ── LEGEND strip — separate row below PLATFORMS, no overlap ─────────────────
    if option_letter == "A":
        legend = [("GA", GREENA, "Generally Available"),
                  ("Pilot", AMBER, "Pilot Stage"),
                  ("PoC", REDPOC, "Proof of Concept")]
    elif option_letter == "B":
        legend = [("AUTO", GREENA, "Autonomous Agent"),
                  ("ASSIST", BLUE, "Co-Pilot / Assist")]
    else:
        legend = [("AGENT", PURPLE, "Autonomous — Orchestrated"),
                  ("→", PURPLE, "Inter-agent handoff")]

    Y_LEG = Inches(6.34);  H_LEG = Inches(0.24)
    R(sl, LM, Y_LEG, W - LM - Inches(0.14), H_LEG,
      fill=RGBColor(0xF8,0xF9,0xFF), line=LBLUE, lw=Pt(0.4))
    T(sl, "LEGEND:", LM+Inches(0.08), Y_LEG+Inches(0.05),
      Inches(0.65), H_LEG-Inches(0.06), size=Pt(7.5), bold=True, color=NAVY)
    lx_start = LM + Inches(0.82)
    for li, (lbl, lc, ldesc) in enumerate(legend):
        lx2 = lx_start + li * Inches(2.6)
        R(sl, lx2, Y_LEG+Inches(0.05), Inches(0.40), Inches(0.14), fill=lc)
        T(sl, f"{lbl} = {ldesc}", lx2+Inches(0.46), Y_LEG+Inches(0.05),
          Inches(2.1), Inches(0.14), size=Pt(7.5), color=DGRAY)

    # ── Footer ────────────────────────────────────────────────────────────────
    R(sl, 0, Y_FOOT, W, H_FOOT, fill=NAVY)
    T(sl, "© 2026 Cognizant  ·  US Bank PDLC AI Transformation  ·  Confidential",
      Inches(0.2), Y_FOOT + Inches(0.07),
      Inches(8), Inches(0.16),
      size=Pt(7), color=LBLUE)
    T(sl, f"STUMP Platform  ·  Option {option_letter}",
      Inches(11.5), Y_FOOT + Inches(0.07),
      Inches(1.7), Inches(0.16),
      size=Pt(7), color=LBLUE, align=PP_ALIGN.RIGHT)

# ═══════════════════════════════════════════════════════════════════════════════
# Build three slides
# ═══════════════════════════════════════════════════════════════════════════════

make_slide(
    "A",
    "Option A  —  Augmented Human  (AI as Assistants & Co-Pilots)",
    "16 AI assistants support each persona  ·  Human remains the primary actor in every phase",
    AI_A,
    banner_color = RGBColor(0x00, 0x00, 0x78),
    option_accent = BLUE,
    show_orchestration = False,
)

make_slide(
    "B",
    "Option B  —  Hybrid  (Selective Autonomous Agents)",
    "12 agents independently deliver key phase outputs  ·  Humans focus on design, decisions & exceptions",
    AI_B,
    banner_color = RGBColor(0x2E, 0x30, 0x8E),
    option_accent = PURPLE,
    show_orchestration = False,
)

make_slide(
    "C",
    "Option C  —  AI-First  (Orchestrated Agent Pipeline)",
    "22 agents orchestrate full PDLC end-to-end  ·  Humans oversee, review and approve only",
    AI_C,
    banner_color = RGBColor(0x03, 0x50, 0x4F),
    option_accent = TEAL,
    show_orchestration = True,
)

out = "/Users/125066/Library/CloudStorage/OneDrive-Cognizant/Clients/US Bank/New Initiatives/US Bank 2026/STUMP-PDLC-Options-A-B-C.pptx"
prs.save(out)
print(f"Saved  →  {out}")
