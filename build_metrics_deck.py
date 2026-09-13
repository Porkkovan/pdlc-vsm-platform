"""
STUMP — Metrics & Measurement Framework
Appended slides covering:
  • AI Adoption metrics
  • PDLC Performance metrics (lead time, cycle time, flow efficiency, DORA)
  • Formula · Data Needed · Data Sources · Capture · Calculate · Display
  • Option A → B → C progression targets
  • Data architecture & monitoring dashboard approach
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x00, 0x00, 0x48)
BLUE   = RGBColor(0x2F, 0x78, 0xC4)
TEAL   = RGBColor(0x06, 0xC7, 0xCC)
PURPLE = RGBColor(0x2E, 0x30, 0x8E)
LBLUE  = RGBColor(0x92, 0xBB, 0xE6)
LTEAL  = RGBColor(0xB3, 0xF0, 0xF2)
LNAVY  = RGBColor(0xD7, 0xE8, 0xF9)
LPURP  = RGBColor(0xE8, 0xE8, 0xF8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
OFFWH  = RGBColor(0xF4, 0xF7, 0xFF)
LGRAY  = RGBColor(0xF3, 0xF4, 0xF6)
DGRAY  = RGBColor(0x1F, 0x29, 0x37)
MGRAY  = RGBColor(0x6B, 0x72, 0x80)
GREENA = RGBColor(0x05, 0x7A, 0x55)
AMBER  = RGBColor(0xB4, 0x5A, 0x09)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation("/Users/125066/Library/CloudStorage/OneDrive-Cognizant/Clients/US Bank/New Initiatives/US Bank 2026/STUMP-PDLC-Options-A-B-C.pptx")
BLANK = prs.slide_layouts[6]

# ── Primitives ────────────────────────────────────────────────────────────────
def R(sl, x, y, w, h, fill=None, line=None, lw=Pt(0.6)):
    s = sl.shapes.add_shape(1, x, y, w, h)
    if fill: s.fill.solid(); s.fill.fore_color.rgb = fill
    else: s.fill.background()
    if line: s.line.color.rgb = line; s.line.width = lw
    else: s.line.fill.background()
    return s

def T(sl, text, x, y, w, h, size=Pt(9), bold=False,
      color=DGRAY, align=PP_ALIGN.LEFT, italic=False):
    b  = sl.shapes.add_textbox(x, y, w, h)
    tf = b.text_frame; tf.word_wrap = True
    p  = tf.paragraphs[0]; p.alignment = align
    r  = p.add_run(); r.text = text
    r.font.size = size; r.font.bold = bold
    r.font.color.rgb = color; r.font.italic = italic
    return b

def header(sl, title, subtitle=None, accent=NAVY):
    R(sl, 0, 0, W, H, fill=WHITE)
    R(sl, 0, 0, W, Inches(1.0), fill=NAVY)
    R(sl, 0, 0, Inches(0.1), Inches(1.0), fill=accent)
    T(sl, title,   Inches(0.26), Inches(0.1),  Inches(11), Inches(0.5),
      size=Pt(21), bold=True, color=WHITE)
    if subtitle:
        T(sl, subtitle, Inches(0.26), Inches(0.6), Inches(11), Inches(0.32),
          size=Pt(10), color=LBLUE, italic=True)
    R(sl, 0, Inches(1.0), W, Inches(0.03), fill=accent)

def footer(sl, pg=""):
    R(sl, 0, H-Inches(0.26), W, Inches(0.26), fill=NAVY)
    T(sl, "STUMP  ·  Metrics & Measurement Framework  ·  © 2026 Cognizant  ·  Confidential",
      Inches(0.2), H-Inches(0.24), Inches(11), Inches(0.22), size=Pt(7.5), color=LBLUE)
    if pg:
        T(sl, pg, Inches(12.8), H-Inches(0.24), Inches(0.4), Inches(0.22),
          size=Pt(7.5), color=LBLUE, align=PP_ALIGN.RIGHT)

def section_box(sl, x, y, w, h, title, title_bg=NAVY):
    R(sl, x, y, w, h, fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF))
    R(sl, x, y, w, Inches(0.28), fill=title_bg)
    T(sl, title, x+Inches(0.1), y+Inches(0.05), w-Inches(0.14), Inches(0.2),
      size=Pt(8.5), bold=True, color=WHITE)

def label_val(sl, label, val, x, y, w, lw=Inches(1.3), size=Pt(8.5)):
    T(sl, label, x, y, lw, Inches(0.2), size=size, bold=True, color=NAVY)
    T(sl, val,   x+lw, y, w-lw-Inches(0.05), Inches(0.2), size=size, color=DGRAY)

def pill(sl, text, x, y, bg=BLUE, fg=WHITE, pw=None):
    pw = pw or Inches(0.7 + len(text)*0.055)
    R(sl, x, y, pw, Inches(0.19), fill=bg)
    T(sl, text, x+Inches(0.04), y+Inches(0.02), pw-Inches(0.06), Inches(0.16),
      size=Pt(7), bold=True, color=fg)
    return pw

def bullet_lines(sl, items, x, y, w, size=Pt(8.5), color=DGRAY, spacing=Inches(0.225)):
    for i, item in enumerate(items):
        iy = y + i*spacing
        R(sl, x+Inches(0.04), iy+Inches(0.07), Inches(0.05), Inches(0.05), fill=BLUE)
        T(sl, item, x+Inches(0.14), iy, w-Inches(0.14), spacing,
          size=size, color=color)

def formula_box(sl, formula, x, y, w, h=Inches(0.3)):
    R(sl, x, y, w, h, fill=RGBColor(0xEF,0xF6,0xFF), line=BLUE, lw=Pt(0.75))
    T(sl, formula, x+Inches(0.1), y+Inches(0.04), w-Inches(0.14), h-Inches(0.06),
      size=Pt(8.5), bold=True, color=NAVY, align=PP_ALIGN.LEFT)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE M1 — Framework Overview
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
header(sl, "Metrics & Measurement Framework",
       "Two perspectives — AI Adoption + PDLC Performance — tracked from Option A through Option C", TEAL)
footer(sl, "M1")

# Two perspective panels
for ci, (title, bg, icon, desc, metrics) in enumerate([
    ("Perspective 1 — AI Adoption",  NAVY,
     "How deeply and effectively are AI assistants/agents being used?",
     "Measures whether humans are actually using and trusting AI systems",
     ["Agent Utilisation Rate", "AI Acceptance Rate", "Human Override Rate",
      "Time Saved per Agent", "Phase Coverage %", "Agent Throughput",
      "AI-Assisted PR Rate", "ROI per Agent Deployed"]),
    ("Perspective 2 — PDLC Performance", PURPLE,
     "Is AI improving delivery speed, quality and flow?",
     "Measures whether AI is actually moving the needle on engineering metrics",
     ["Lead Time (idea → production)", "Cycle Time (start → deploy)",
      "Flow Efficiency %", "Work in Progress (WIP)",
      "Deployment Frequency", "Change Failure Rate (CFR)",
      "Mean Time to Recovery (MTTR)", "Throughput (items/sprint)"]),
]):
    x = Inches(0.2) + ci * Inches(6.6)
    R(sl, x, Inches(1.1), Inches(6.42), Inches(5.88),
      fill=OFFWH, line=RGBColor(0xC5,0xD8,0xEF))
    R(sl, x, Inches(1.1), Inches(6.42), Inches(0.38), fill=bg)
    T(sl, title, x+Inches(0.12), Inches(1.14), Inches(6.2), Inches(0.3),
      size=Pt(11), bold=True, color=WHITE)
    T(sl, icon, x+Inches(0.12), Inches(1.52), Inches(6.2), Inches(0.22),
      size=Pt(9), bold=True, color=bg)
    T(sl, desc, x+Inches(0.12), Inches(1.76), Inches(6.2), Inches(0.22),
      size=Pt(8.5), color=MGRAY, italic=True)
    for mi, m in enumerate(metrics):
        my = Inches(2.06) + mi * Inches(0.42)
        R(sl, x+Inches(0.12), my, Inches(6.1), Inches(0.35),
          fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.4))
        R(sl, x+Inches(0.12), my, Inches(0.07), Inches(0.35), fill=bg)
        T(sl, m, x+Inches(0.25), my+Inches(0.07), Inches(5.75), Inches(0.24),
          size=Pt(9), color=DGRAY)

# Measurement cadence strip
R(sl, Inches(0.2), Inches(7.0), W-Inches(0.4), Inches(0.22), fill=NAVY)
for ci2, (lbl, val) in enumerate([
    ("Cadence:", "Daily automated collection  ·  Weekly aggregation  ·  Sprint review  ·  Monthly executive report"),
    ("Tools:", "Jira  ·  GitHub  ·  CI/CD pipeline  ·  Agent telemetry  ·  STUMP dashboard"),
]):
    T(sl, lbl, Inches(0.34)+ci2*Inches(5.8), Inches(7.02), Inches(0.7), Inches(0.18),
      size=Pt(7.5), bold=True, color=TEAL)
    T(sl, val,  Inches(1.08)+ci2*Inches(5.8), Inches(7.02), Inches(5.6), Inches(0.18),
      size=Pt(7.5), color=WHITE)

# ═══════════════════════════════════════════════════════════════════════════════
# Helper: full metric deep-dive card (2 per slide)
# ═══════════════════════════════════════════════════════════════════════════════
def metric_card(sl, x, y, w, h, m):
    R(sl, x, y, w, h, fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF))
    # Name bar
    R(sl, x, y, w, Inches(0.46), fill=m["color"])
    T(sl, m["name"], x+Inches(0.12), y+Inches(0.09), w-Inches(0.16), Inches(0.32),
      size=Pt(12), bold=True, color=WHITE)
    # Tagline
    T(sl, m["tagline"], x+Inches(0.12), y+Inches(0.50), w-Inches(0.16), Inches(0.30),
      size=Pt(10), color=MGRAY, italic=True)
    # Formula box
    R(sl, x+Inches(0.12), y+Inches(0.84), w-Inches(0.24), Inches(0.38),
      fill=RGBColor(0xEF,0xF6,0xFF), line=BLUE, lw=Pt(0.75))
    T(sl, "Formula:  " + m["formula"],
      x+Inches(0.22), y+Inches(0.90), w-Inches(0.30), Inches(0.30),
      size=Pt(9.5), bold=True, color=NAVY)
    # Three-column layout — distribute remaining height evenly across 4 bullet items
    col_w = (w - Inches(0.30)) / 3
    col_xs = [x+Inches(0.12),
              x+Inches(0.12) + col_w + Inches(0.03),
              x+Inches(0.12) + (col_w + Inches(0.03))*2]
    col_y  = y + Inches(1.30)
    # Leave 0.76" at bottom for targets (0.34") + sources (0.32") + gaps
    col_h  = h - Inches(1.30) - Inches(0.76)
    item_spacing = (col_h - Inches(0.32)) / 4   # 4 items fill the column height
    labels   = ["Data Needed", "Capture Approach", "Calculate & Display"]
    contents = [m["data_needed"], m["capture"], m["calculate_display"]]
    col_colors = [NAVY, RGBColor(0x06,0x5F,0x46), PURPLE]
    for ci3, (lbl, items, cc) in enumerate(zip(labels, contents, col_colors)):
        cx = col_xs[ci3]
        R(sl, cx, col_y, col_w, col_h, fill=OFFWH, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.4))
        R(sl, cx, col_y, col_w, Inches(0.28), fill=cc)
        T(sl, lbl, cx+Inches(0.08), col_y+Inches(0.05), col_w-Inches(0.12), Inches(0.20),
          size=Pt(9), bold=True, color=WHITE)
        for ii, item in enumerate(items[:4]):
            iy2 = col_y + Inches(0.32) + ii * item_spacing
            R(sl, cx+Inches(0.10), iy2+Inches(0.12), Inches(0.06), Inches(0.06), fill=cc)
            T(sl, item, cx+Inches(0.22), iy2+Inches(0.02),
              col_w-Inches(0.28), item_spacing-Inches(0.06),
              size=Pt(9.5), color=DGRAY)
    # Option targets — sits just below the columns
    oty = y + h - Inches(0.72)
    for oi, (opt, tv, oc) in enumerate([
        ("A", m["option_targets"]["A"], BLUE),
        ("B", m["option_targets"]["B"], PURPLE),
        ("C", m["option_targets"]["C"], GREENA),
    ]):
        ox2 = x + Inches(0.12) + oi * ((w-Inches(0.24))/3)
        R(sl, ox2, oty, (w-Inches(0.24))/3 - Inches(0.04), Inches(0.32), fill=oc)
        T(sl, f"Opt {opt}: {tv}",
          ox2+Inches(0.07), oty+Inches(0.07),
          (w-Inches(0.24))/3 - Inches(0.14), Inches(0.22),
          size=Pt(9), bold=True, color=WHITE)
    # Data sources pills
    py2 = y + h - Inches(0.36)
    R(sl, x+Inches(0.12), py2, w-Inches(0.24), Inches(0.30),
      fill=LGRAY, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.4))
    T(sl, "Sources:", x+Inches(0.18), py2+Inches(0.07), Inches(0.65), Inches(0.18),
      size=Pt(8.5), bold=True, color=NAVY)
    px2 = x + Inches(0.88)
    for src, sc in m["data_sources"]:
        pw2 = pill(sl, src, px2, py2+Inches(0.06), bg=sc)
        px2 += pw2 + Inches(0.07)

# ═══════════════════════════════════════════════════════════════════════════════
# AI Adoption Metrics data
# ═══════════════════════════════════════════════════════════════════════════════
ADOPT_METRICS = [
  {
    "name":    "Agent Utilisation Rate",
    "tagline": "% of PDLC activities where an AI agent/assistant was actively involved",
    "formula": "(Activities with AI involvement ÷ Total PDLC activities) × 100",
    "color":   NAVY,
    "data_needed":  ["Work item count per phase from ALM", "AI agent execution logs per activity",
                     "Phase-activity mapping config", "Sprint/release boundary timestamps"],
    "capture":      ["Instrument agent service to log each invocation with phase_id + activity_id",
                     "Pull total work-item count from Jira/ADO per sprint",
                     "Store in STUMP AnalysisRun.agents_run JSON per execution",
                     "Aggregate weekly via APScheduler pipeline"],
    "calculate_display": ["Calc: SUM(ai_invocations per phase) / SUM(total_activities) × 100",
                          "Chart: Stacked bar — AI-handled vs manual per phase",
                          "Alert: < 30 % in any active phase triggers low-adoption warning",
                          "Review: Sprint retrospective scorecard widget"],
    "data_sources": [("Jira/ADO", NAVY), ("Agent Logs", BLUE), ("STUMP DB", PURPLE)],
    "option_targets": {"A": "30–50 %", "B": "60–75 %", "C": "85–95 %"},
  },
  {
    "name":    "AI Acceptance Rate",
    "tagline": "% of AI-generated outputs accepted or merged by humans without major revision",
    "formula": "(AI outputs accepted as-is or minor edits ÷ Total AI outputs generated) × 100",
    "color":   BLUE,
    "data_needed":  ["PR merge status and review comments from GitHub/GitLab",
                     "AI suggestion logs from Copilot / LLM APIs",
                     "Code review tool delta metrics (lines changed post-AI)",
                     "Acceptance event from agent feedback endpoint"],
    "capture":      ["GitHub webhook on PR merge — tag PRs with ai_assisted label",
                     "Compare diff size before/after AI suggestion acceptance",
                     "Agent service records accept/reject events in ActivityMetric table",
                     "Weekly rollup via STUMP /api/v1/accuracy endpoint"],
    "calculate_display": ["Calc: COUNT(accepted_PRs with ai_label) / COUNT(all ai_PRs) × 100",
                          "Chart: Trend line per agent over rolling 4 sprints",
                          "Alert: Acceptance rate < 60 % triggers quality review",
                          "Display: Per-agent scorecard on AI Agents page"],
    "data_sources": [("GitHub/GitLab", NAVY), ("Copilot API", BLUE), ("LLM Logs", TEAL)],
    "option_targets": {"A": "55–70 %", "B": "70–85 %", "C": "88–95 %"},
  },
  {
    "name":    "Human Override Rate",
    "tagline": "% of AI decisions / suggestions that humans reversed or rejected",
    "formula": "(Human overrides of AI output ÷ Total AI decisions made) × 100",
    "color":   PURPLE,
    "data_needed":  ["Override / rejection events from code review tooling",
                     "Playbook action items marked 'overridden' by team leads",
                     "Agent output revision history from STUMP analysis runs",
                     "Manual correction logs from VSM Editor overrides"],
    "capture":      ["Log every override event in AssessmentActionItem.status = 'Overridden'",
                     "Track VSMSnapshot.overrides JSON for manual corrections",
                     "GitHub label ai_overridden applied by reviewers in PR comments",
                     "STUMP /api/v1/accuracy feedback form captures override reason"],
    "calculate_display": ["Calc: COUNT(override_events) / COUNT(ai_decisions) × 100",
                          "Chart: Heatmap by phase — which phases have highest override rates",
                          "Alert: Override rate > 30 % in any phase → retrain / recalibrate agent",
                          "Display: Accuracy & RAG page override breakdown table"],
    "data_sources": [("STUMP DB", PURPLE), ("GitHub", NAVY), ("VSM Editor", BLUE)],
    "option_targets": {"A": "< 35 %", "B": "< 20 %", "C": "< 10 %"},
  },
  {
    "name":    "Time Saved per Agent (hours/sprint)",
    "tagline": "Actual engineering hours saved per AI agent per sprint vs. manual baseline",
    "formula": "(Manual effort baseline hrs − Actual effort with AI hrs) per sprint, per agent",
    "color":   GREENA,
    "data_needed":  ["Story point / time estimates before AI from Jira",
                     "Actual time-logged data (Jira worklogs or time-tracking tool)",
                     "Per-phase manual benchmark (from initial VSM baseline run)",
                     "Sprint velocity data — story points completed"],
    "capture":      ["Establish manual baseline in Sprint 1 before any AI agent is live",
                     "Log Jira worklog hours per story each sprint post-AI deployment",
                     "Compare: estimate_hrs × normalisation_factor vs actual_logged_hrs",
                     "Store delta in ActivityMetric.process_time per phase per sprint"],
    "calculate_display": ["Calc: SUM(baseline_PT − actual_PT) across agent's activities",
                          "Chart: Bar chart — hours saved per agent, sprint-over-sprint trend",
                          "KPI card: Total hrs saved this sprint on Dashboard page",
                          "Alert: Saved hours declining 2+ sprints triggers agent health review"],
    "data_sources": [("Jira Worklogs", NAVY), ("VSM Baseline", BLUE), ("STUMP DB", PURPLE)],
    "option_targets": {"A": "2–8 hrs/agent", "B": "8–20 hrs/agent", "C": "20–40 hrs/agent"},
  },
  {
    "name":    "AI Phase Coverage %",
    "tagline": "% of the 7 PDLC phases that have at least one active AI agent/assistant",
    "formula": "(PDLC phases with ≥ 1 active AI agent ÷ 7 total phases) × 100",
    "color":   RGBColor(0x0A, 0x5C, 0x8A),
    "data_needed":  ["Active agent list per phase from STUMP agent registry",
                     "Phase-agent mapping from LangGraph orchestrator config",
                     "Agent status (GA / Pilot / PoC) per phase from platform settings",
                     "Sprint release plan showing when each agent goes live"],
    "capture":      ["STUMP /api/v1/agents returns agent-phase mapping — query per sprint",
                     "Tag each AnalysisRun with phases_covered list in result JSON",
                     "APScheduler weekly run computes coverage and stores in PlatformSettings",
                     "Manual update when new agent phases are activated"],
    "calculate_display": ["Calc: COUNT(DISTINCT phase_id in active_agents) / 7 × 100",
                          "Chart: Radar/spider chart — 7-axis with fill showing coverage",
                          "Target: 4/7 phases covered by Option A; 7/7 by Option C",
                          "Display: Dashboard page phase coverage ring chart"],
    "data_sources": [("STUMP Agent Service", BLUE), ("LangGraph Config", PURPLE)],
    "option_targets": {"A": "4 / 7 phases", "B": "6 / 7 phases", "C": "7 / 7 phases"},
  },
  {
    "name":    "Agent ROI Multiple",
    "tagline": "Return on investment per deployed agent — value delivered vs. cost of running it",
    "formula": "(Annual value delivered by agent £ ÷ Annual cost of agent deployment £)",
    "color":   AMBER,
    "data_needed":  ["Engineering salary cost per hour for manual equivalent tasks",
                     "Time saved per agent per sprint (from Time Saved metric above)",
                     "Agent operational cost: LLM API cost + infra + maintenance hours",
                     "Defects prevented count and estimated cost per defect"],
    "capture":      ["Pull LLM API usage from Azure OpenAI billing dashboard monthly",
                     "Calculate value: time_saved_hrs × avg_eng_rate × 52 sprints/year",
                     "Track defects prevented via Quality Assurance report delta",
                     "Store ROI calculation results in STUMP business_cases result JSON"],
    "calculate_display": ["Calc: (time_saved_value + defect_saving) / (llm_cost + eng_cost)",
                          "Chart: ROI waterfall chart per agent on Business Case page",
                          "KPI: ROI multiple displayed on AI Agents monitor page per agent",
                          "Alert: ROI < 1.5× triggers cost-benefit review for that agent"],
    "data_sources": [("Azure OAI Billing", AMBER), ("HR Cost Data", NAVY), ("STUMP DB", PURPLE)],
    "option_targets": {"A": "1.5 – 3×", "B": "3 – 4.5×", "C": "4.5 – 6×"},
  },
]

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDES M2–M4 — AI Adoption Metric Deep-Dives (2 per slide)
# ═══════════════════════════════════════════════════════════════════════════════
ADOPT_PAIRS = [(0,1), (2,3), (4,5)]
ADOPT_SUBTITLES = [
    "Agent Utilisation Rate  ·  AI Acceptance Rate",
    "Human Override Rate  ·  Time Saved per Agent",
    "Phase Coverage  ·  Agent ROI Multiple",
]
for pg_idx, (i, j) in enumerate(ADOPT_PAIRS):
    sl = prs.slides.add_slide(BLANK)
    header(sl, "AI Adoption Metrics — Deep Dive",
           ADOPT_SUBTITLES[pg_idx], BLUE)
    footer(sl, f"M{pg_idx+2}")
    cw = Inches(6.45); ch = Inches(6.0)
    metric_card(sl, Inches(0.15), Inches(1.1), cw, ch, ADOPT_METRICS[i])
    metric_card(sl, Inches(6.73), Inches(1.1), cw, ch, ADOPT_METRICS[j])

# ═══════════════════════════════════════════════════════════════════════════════
# PDLC Performance Metrics data
# ═══════════════════════════════════════════════════════════════════════════════
PDLC_METRICS = [
  {
    "name":    "Lead Time (Idea → Production)",
    "tagline": "Total elapsed time from a feature request being raised to it being live in production",
    "formula": "Deploy_timestamp − Feature_request_created_timestamp  (calendar days)",
    "color":   NAVY,
    "data_needed":  ["Work item creation date from Jira/ADO (feature request timestamp)",
                     "Production deployment timestamp from CI/CD pipeline logs",
                     "Release/tag event from GitHub/GitLab release API",
                     "Feature-to-deployment traceability link in ALM"],
    "capture":      ["Jira webhook on issue_created → store created_at in STUMP VSMSnapshot",
                     "CI/CD webhook on deployment_success → store deploy_at per feature ID",
                     "Link Jira issue ID to GitHub PR and deployment tag via branch naming",
                     "STUMP ALM Connector agent computes LT per phase on each run"],
    "calculate_display": ["Calc: AVG(deploy_date − created_date) across all features in sprint",
                          "Chart: Box-plot showing LT distribution; p50 / p90 trend line",
                          "DORA band: Elite < 1 day; High < 1 week; Medium < 1 month",
                          "Display: Current VSM page — per-phase LT heat strip + total LT KPI"],
    "data_sources": [("Jira/ADO", NAVY), ("CI/CD Logs", BLUE), ("GitHub Tags", GREENA)],
    "option_targets": {"A": "21 – 28 days", "B": "10 – 14 days", "C": "3 – 7 days"},
  },
  {
    "name":    "Cycle Time (Dev Start → Deploy)",
    "tagline": "Time from a developer picking up a task to the code reaching production",
    "formula": "Deploy_timestamp − In-Progress_status_timestamp  (working hours)",
    "color":   BLUE,
    "data_needed":  ["In-Progress status transition timestamp from Jira/ADO history",
                     "Production deploy event timestamp from CI/CD pipeline",
                     "PR open and merge timestamps from GitHub",
                     "Code review start / approval timestamps"],
    "capture":      ["Jira issue changelog API — filter status change to 'In Progress'",
                     "GitHub PR events API — pr.created_at and pr.merged_at per feature",
                     "CI/CD deployment event webhook → log to STUMP AnalysisRun",
                     "STUMP VSM Analyzer computes per-phase cycle time on each pipeline run"],
    "calculate_display": ["Calc: AVG(deploy_at − in_progress_at) per sprint",
                          "Chart: Scatter plot — individual items plotted; percentile lines",
                          "Target: Reduce p85 cycle time sprint-over-sprint by ≥ 10 %",
                          "Display: Bottlenecks page — per-phase wait-time breakdown bar"],
    "data_sources": [("Jira History", NAVY), ("GitHub PRs", BLUE), ("CI/CD", GREENA)],
    "option_targets": {"A": "7 – 14 days", "B": "3 – 7 days", "C": "< 2 days"},
  },
  {
    "name":    "Flow Efficiency %",
    "tagline": "Proportion of total lead time spent on value-adding work vs. waiting",
    "formula": "(Total Process Time ÷ Total Lead Time) × 100   [PT / (PT + WT) × 100]",
    "color":   TEAL,
    "data_needed":  ["Process time (active work time) per phase from ALM worklogs",
                     "Wait time (queue / blocked time) per phase from status timestamps",
                     "Phase boundary definitions aligned to VSM Editor config",
                     "DORA calibration overrides (code review wait, build wait)"],
    "capture":      ["STUMP VSM Analyzer computes PT and WT per phase from ALM data",
                     "Jira time-in-status report for WT; worklog for PT per phase",
                     "DORA Assessment page captures code_review_wait and build_duration",
                     "Store per-phase PT/WT in VSMSnapshot.vsm_data JSON each sprint"],
    "calculate_display": ["Calc: SUM(PT across 7 phases) / SUM(PT + WT across 7 phases) × 100",
                          "Chart: Stacked bar — PT (blue) vs WT (grey) per phase; FE% overlay",
                          "Lean target: FE > 40 % = Efficient; < 15 % = Critical",
                          "Display: Current State VSM page — phase-by-phase FE% heat strip"],
    "data_sources": [("Jira Worklogs", NAVY), ("VSM Analyzer", BLUE), ("DORA Calibration", TEAL)],
    "option_targets": {"A": "18 – 28 %", "B": "32 – 45 %", "C": "50 – 65 %"},
  },
  {
    "name":    "Work in Progress (WIP)",
    "tagline": "Number of work items simultaneously in an active (not done, not backlog) state",
    "formula": "COUNT(items where status ∈ {In Progress, In Review, Blocked, In Test})",
    "color":   PURPLE,
    "data_needed":  ["Real-time work item statuses from Jira/ADO board",
                     "Team size and WIP limit policy from Settings page",
                     "Age of each in-progress item (days since In-Progress transition)",
                     "Blocked item count and blocker category"],
    "capture":      ["Jira/ADO Board API — poll active status counts daily via APScheduler",
                     "Store daily WIP snapshot in ActivityMetric table per phase",
                     "Flag items aged > sprint_length as Aged WIP",
                     "STUMP Operations Intelligence page displays real-time WIP"],
    "calculate_display": ["Calc: COUNT(active_status_items) per team per day",
                          "Chart: WIP trend line + WIP limit rule line per sprint",
                          "Little's Law: Throughput = WIP ÷ Cycle Time (validate consistency)",
                          "Alert: WIP > team_wip_limit triggers bottleneck notification"],
    "data_sources": [("Jira/ADO Board", NAVY), ("STUMP Scheduler", BLUE)],
    "option_targets": {"A": "WIP ≤ 2× team size", "B": "WIP ≤ 1.5×", "C": "WIP ≤ 1×"},
  },
  {
    "name":    "Deployment Frequency",
    "tagline": "How often code is successfully deployed to production per time period",
    "formula": "COUNT(successful production deployments) ÷ Time period (week / day)",
    "color":   GREENA,
    "data_needed":  ["Successful production deployment events from CI/CD pipeline",
                     "Environment tags (prod vs staging) from deployment config",
                     "Rollback events (to exclude from successful count)",
                     "Release cadence config from platform Settings"],
    "capture":      ["CI/CD webhook → POST to STUMP /api/v1/alm on each prod deployment",
                     "GitHub Release API — count tags published to main/prod branch",
                     "Store deployment event in AnalysisRun with trigger='deployment'",
                     "STUMP DORA Assessment page captures and calibrates this value"],
    "calculate_display": ["Calc: COUNT(prod_deployments) / days_in_period",
                          "DORA bands: Elite = multiple/day; High = daily; Medium = weekly",
                          "Chart: Deployment frequency bar per week; DORA band colour overlay",
                          "Display: Dashboard KPI card + DORA Assessment page trend chart"],
    "data_sources": [("CI/CD Pipeline", GREENA), ("GitHub Releases", NAVY), ("DORA Assessment", BLUE)],
    "option_targets": {"A": "Weekly", "B": "Daily", "C": "Multiple / day"},
  },
  {
    "name":    "Change Failure Rate (CFR) & MTTR",
    "tagline": "CFR: % of deployments causing incidents.  MTTR: avg time to restore service after failure",
    "formula": "CFR = (Failed deploys ÷ Total deploys) × 100  |  MTTR = AVG(restore_time − incident_time)",
    "color":   AMBER,
    "data_needed":  ["Deployment success/failure status from CI/CD pipeline",
                     "Incident creation and resolution timestamps from ServiceNow/PagerDuty",
                     "Deployment-to-incident correlation (deployment_id → incident_id)",
                     "Rollback event count and duration from release tooling"],
    "capture":      ["CI/CD post-deploy health check — classify deploy as success/failure",
                     "ServiceNow/PagerDuty webhook → POST incident events to STUMP",
                     "Correlate by: incident created within 24h of deployment_id",
                     "STUMP Risk Assistant agent flags deployment-correlated incidents"],
    "calculate_display": ["CFR Calc: COUNT(failed_deploys) / COUNT(total_deploys) × 100",
                          "MTTR Calc: AVG(resolved_at − created_at) for deployment incidents",
                          "DORA bands — CFR: Elite < 5 %; High < 10 %. MTTR: Elite < 1h",
                          "Display: Dashboard DORA KPI panel; Governance page risk heatmap"],
    "data_sources": [("CI/CD Pipeline", AMBER), ("ServiceNow/PD", NAVY), ("Risk Assistant", PURPLE)],
    "option_targets": {"A": "CFR < 15 % / MTTR < 4h", "B": "CFR < 8 % / MTTR < 2h", "C": "CFR < 5 % / MTTR < 1h"},
  },
]

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDES M5–M7 — PDLC Performance Metric Deep-Dives
# ═══════════════════════════════════════════════════════════════════════════════
PDLC_PAIRS = [(0,1), (2,3), (4,5)]
PDLC_SUBTITLES = [
    "Lead Time (Idea → Production)  ·  Cycle Time (Dev Start → Deploy)",
    "Flow Efficiency %  ·  Work in Progress (WIP)",
    "Deployment Frequency  ·  Change Failure Rate & MTTR",
]
for pg_idx, (i, j) in enumerate(PDLC_PAIRS):
    sl = prs.slides.add_slide(BLANK)
    header(sl, "PDLC Performance Metrics — Deep Dive",
           PDLC_SUBTITLES[pg_idx], PURPLE)
    footer(sl, f"M{pg_idx+5}")
    cw = Inches(6.45); ch = Inches(6.0)
    metric_card(sl, Inches(0.15), Inches(1.1), cw, ch, PDLC_METRICS[i])
    metric_card(sl, Inches(6.73), Inches(1.1), cw, ch, PDLC_METRICS[j])

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE M8 — Data Collection Architecture
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
header(sl, "Data Collection Architecture",
       "How metrics data flows from source systems through STUMP to dashboards", TEAL)
footer(sl, "M8")

# Three-layer diagram: Sources → STUMP → Outputs
layers = [
    ("DATA SOURCES", NAVY, Inches(0.15), [
        ("Jira / Azure DevOps",    "Work items, status history, worklogs, sprint data"),
        ("GitHub / GitLab",        "PR events, merge times, deployment tags, commit frequency"),
        ("CI/CD Pipeline",         "Build results, deploy events, rollback flags, durations"),
        ("ServiceNow / PagerDuty", "Incident timestamps, severity, resolution events"),
        ("Azure OpenAI Billing",   "LLM API call counts, token usage, cost per agent"),
        ("STUMP Agent Telemetry",  "Agent invocations, accept/reject events, phase coverage"),
    ]),
    ("STUMP PROCESSING", BLUE, Inches(4.72), [
        ("ALM Connector Agent",    "Fetches & normalises work item data per PDLC phase"),
        ("VSM Analyzer Agent",     "Computes PT, WT, LT, FE % with DORA calibration"),
        ("APScheduler Pipeline",   "Automated nightly/weekly metric collection runs"),
        ("ActivityMetric Table",   "Persists per-phase, per-sprint metric snapshots"),
        ("AnalysisRun Store",      "Full pipeline results with agent-level metadata"),
        ("Accuracy Feedback Loop", "User-calibrated override capture via /api/v1/accuracy"),
    ]),
    ("OUTPUTS & MONITORING", PURPLE, Inches(9.29), [
        ("STUMP Dashboard",        "KPI cards: Lead Time, FE %, Deployment Freq, WIP"),
        ("Current State VSM Page", "Phase heat-strip: PT, WT, FE % per phase"),
        ("AI Agents Monitor Page", "Per-agent: utilisation, acceptance rate, ROI, savings"),
        ("DORA Assessment Page",   "DORA band classification: Elite / High / Medium / Low"),
        ("Governance Page",        "Risk heatmap, CFR trend, MTTR trend"),
        ("Excel / PDF Export",     "Downloadable sprint metrics report for stakeholders"),
    ]),
]

bw2 = Inches(4.24); bh2 = Inches(5.72); by2 = Inches(1.1)
for lbl, col_, lx2, items in layers:
    R(sl, lx2, by2, bw2, bh2, fill=OFFWH, line=RGBColor(0xC5,0xD8,0xEF))
    R(sl, lx2, by2, bw2, Inches(0.3), fill=col_)
    T(sl, lbl, lx2+Inches(0.12), by2+Inches(0.06), bw2-Inches(0.18), Inches(0.22),
      size=Pt(9.5), bold=True, color=WHITE)
    for ri2, (name, desc) in enumerate(items):
        ry2 = by2 + Inches(0.42) + ri2 * Inches(0.87)
        R(sl, lx2+Inches(0.1), ry2, bw2-Inches(0.2), Inches(0.82),
          fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.4))
        R(sl, lx2+Inches(0.1), ry2, Inches(0.08), Inches(0.82), fill=col_)
        T(sl, name, lx2+Inches(0.24), ry2+Inches(0.07), bw2-Inches(0.36), Inches(0.24),
          size=Pt(9), bold=True, color=col_)
        T(sl, desc, lx2+Inches(0.24), ry2+Inches(0.34), bw2-Inches(0.36), Inches(0.44),
          size=Pt(8.5), color=DGRAY)

# Arrows between layers
for ax in [Inches(4.39), Inches(8.96)]:
    for ay_off in [Inches(0.42), Inches(0.88), Inches(1.34)]:
        pass
T(sl, "→", Inches(4.41), Inches(3.8), Inches(0.32), Inches(0.4),
  size=Pt(22), bold=True, color=BLUE, align=PP_ALIGN.CENTER)
T(sl, "Webhooks\nAPI Polling\nAgent Events", Inches(4.38), Inches(4.28), Inches(0.38), Inches(0.55),
  size=Pt(7), color=MGRAY, align=PP_ALIGN.CENTER)
T(sl, "→", Inches(8.98), Inches(3.8), Inches(0.32), Inches(0.4),
  size=Pt(22), bold=True, color=PURPLE, align=PP_ALIGN.CENTER)
T(sl, "REST API\nPostgres\nExport", Inches(8.95), Inches(4.28), Inches(0.38), Inches(0.55),
  size=Pt(7), color=MGRAY, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE M9 — Option A → B → C Progression Matrix
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
header(sl, "Option A → B → C Progression Matrix",
       "How each metric should evolve as AI adoption deepens across the PDLC", NAVY)
footer(sl, "M9")

# Table header
col_widths = [Inches(2.5), Inches(0.9), Inches(2.3), Inches(2.3), Inches(2.3), Inches(2.3)]
col_xs3 = [Inches(0.15)]
for cw3 in col_widths[:-1]:
    col_xs3.append(col_xs3[-1] + cw3)

hdr_cols = ["Metric", "Perspective", "Option A\n(Augmented Human)", "Option B\n(Hybrid Agents)", "Option C\n(AI-First)", "Measurement\nSource"]
hdr_colors = [NAVY, NAVY, RGBColor(0x00,0x00,0x78), PURPLE, RGBColor(0x03,0x50,0x4F), MGRAY]
hy3 = Inches(1.1)
for ci4, (hdr_txt, hdr_col) in enumerate(zip(hdr_cols, hdr_colors)):
    R(sl, col_xs3[ci4], hy3, col_widths[ci4], Inches(0.44), fill=hdr_col)
    T(sl, hdr_txt, col_xs3[ci4]+Inches(0.08), hy3+Inches(0.05),
      col_widths[ci4]-Inches(0.1), Inches(0.36),
      size=Pt(8.5), bold=True, color=WHITE, align=PP_ALIGN.CENTER)

matrix_rows = [
    # (Metric, Perspective, Opt-A, Opt-B, Opt-C, Source)
    ("Agent Utilisation Rate",    "Adoption",     "30–50 %",              "60–75 %",             "85–95 %",             "Agent Logs / STUMP"),
    ("AI Acceptance Rate",        "Adoption",     "55–70 %",              "70–85 %",             "88–95 %",             "GitHub / LLM API"),
    ("Human Override Rate",       "Adoption",     "< 35 %",               "< 20 %",              "< 10 %",              "STUMP / GitHub"),
    ("Time Saved / Agent / Sprint","Adoption",    "2–8 hrs",              "8–20 hrs",            "20–40 hrs",           "Jira Worklogs"),
    ("Agent ROI Multiple",        "Adoption",     "1.5–3×",               "3–4.5×",              "4.5–6×",              "Billing + HR Cost"),
    ("Lead Time",                 "PDLC Perf.",   "21–28 days",           "10–14 days",          "3–7 days",            "Jira + CI/CD"),
    ("Cycle Time",                "PDLC Perf.",   "7–14 days",            "3–7 days",            "< 2 days",            "GitHub PRs"),
    ("Flow Efficiency %",         "PDLC Perf.",   "18–28 %",              "32–45 %",             "50–65 %",             "VSM Analyzer"),
    ("WIP",                       "PDLC Perf.",   "≤ 2× team size",       "≤ 1.5× team size",    "≤ 1× team size",      "Jira Board"),
    ("Deployment Frequency",      "PDLC Perf.",   "Weekly",               "Daily",               "Multiple / day",      "CI/CD Pipeline"),
    ("Change Failure Rate",       "PDLC Perf.",   "< 15 %",               "< 8 %",               "< 5 %",               "CI/CD + Incidents"),
    ("MTTR",                      "PDLC Perf.",   "< 4 hours",            "< 2 hours",           "< 1 hour",            "ServiceNow / PD"),
]

row_h3 = Inches(0.415)
persp_colors = {"Adoption": RGBColor(0xDB,0xEA,0xFE), "PDLC Perf.": RGBColor(0xE8,0xE8,0xF8)}
opt_colors = [RGBColor(0xEF,0xF6,0xFF), RGBColor(0xF3,0xF0,0xFF), RGBColor(0xEC,0xFD,0xF3)]
for ri3, row3 in enumerate(matrix_rows):
    ry3 = hy3 + Inches(0.44) + ri3 * row_h3
    bg3 = WHITE if ri3 % 2 == 0 else RGBColor(0xF8,0xF9,0xFF)
    for ci4 in range(6):
        cell_bg = bg3
        if ci4 == 1: cell_bg = persp_colors.get(row3[1], bg3)
        if ci4 in (2,3,4): cell_bg = opt_colors[ci4-2]
        R(sl, col_xs3[ci4], ry3, col_widths[ci4], row_h3,
          fill=cell_bg, line=RGBColor(0xC5,0xD8,0xEF), lw=Pt(0.4))
        bold3 = (ci4 == 0)
        col3 = NAVY if ci4 == 0 else DGRAY
        T(sl, row3[ci4], col_xs3[ci4]+Inches(0.08), ry3+Inches(0.1),
          col_widths[ci4]-Inches(0.1), row_h3-Inches(0.08),
          size=Pt(8.5), bold=bold3, color=col3, align=PP_ALIGN.CENTER if ci4 > 0 else PP_ALIGN.LEFT)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE M10 — Illustrative Dashboard Views + Inference Points
#   All bar heights pre-computed in plain Python floats (inches) then Inches()
#   converted — avoids Emu * float arithmetic that produces near-zero values.
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
header(sl, "Monitoring Dashboard  —  Illustrative Views & Inference Points",
       "AI Adoption perspective  ·  PDLC Performance perspective  ·  Key inference & action points per view",
       PURPLE)
footer(sl, "M10")

# ── All layout in plain Python float inches — converted via Inches() only at draw ──
PW_F  = 6.45;  PH_F  = 6.02;  PY_F  = 1.08
PXL_F = 0.14;  PXR_F = 6.74
CW_F  = PW_F - 0.24   # inner chart width = 6.21"

# Phase labels & data
PH_SHORT  = ["Ph1\nDisc", "Ph2\nArch", "Ph3\nDev", "Ph4\nBld", "Ph5\nTest", "Ph6\nDep", "Ph7\nOps"]
UTIL_PCT  = [38, 28, 52, 46, 42, 22, 18]        # AI utilisation % per phase
SPRINT_ACC = [56, 61, 65, 68, 71, 72]            # AI acceptance % sprints 1-6
PHASE_PT  = [2.0, 3.5, 5.0, 1.5, 2.5, 0.8, 1.2] # process time (days) per phase
PHASE_WT  = [4.0, 5.0, 4.0, 2.5, 5.5, 1.2, 2.3] # wait time (days) per phase

# ── helper: draw one bar given plain-float geometry ───────────────────────────
def bar(slide, x_f, y_f, w_f, h_f, fill_color, lbl=None, lbl_color=DGRAY):
    """Draw a bar at plain-float inch co-ords; skip if height ≤ 0."""
    if h_f <= 0:
        return
    R(slide, Inches(x_f), Inches(y_f), Inches(w_f), Inches(h_f), fill=fill_color)
    if lbl:
        T(slide, lbl, Inches(x_f), Inches(y_f - 0.17), Inches(w_f), Inches(0.15),
          size=Pt(7), bold=True, color=lbl_color, align=PP_ALIGN.CENTER)

# ── outer panel shells ─────────────────────────────────────────────────────────
for px_f, ptitle, pcol in [
    (PXL_F, "AI Adoption Dashboard  —  Illustrative  (Option A baseline)",    NAVY),
    (PXR_F, "PDLC Performance Dashboard  —  Illustrative  (Option A baseline)", PURPLE),
]:
    R(sl, Inches(px_f), Inches(PY_F), Inches(PW_F), Inches(PH_F),
      fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF))
    R(sl, Inches(px_f), Inches(PY_F), Inches(PW_F), Inches(0.32), fill=pcol)
    T(sl, ptitle, Inches(px_f+0.10), Inches(PY_F+0.07),
      Inches(PW_F-0.14), Inches(0.22), size=Pt(9), bold=True, color=WHITE)

# ── KPI tiles helper ───────────────────────────────────────────────────────────
TILE_W_F = (PW_F - 0.24) / 4   # ≈ 1.553" per tile (pure float)

def kpi_tiles(slide, px_f, kpis):
    for ki, (kname, kval, kdelta, kc) in enumerate(kpis):
        kx_f = px_f + 0.12 + ki * TILE_W_F
        ky_f = PY_F + 0.36
        R(slide, Inches(kx_f), Inches(ky_f), Inches(TILE_W_F-0.04), Inches(0.84),
          fill=WHITE, line=RGBColor(0xC5,0xD8,0xEF))
        R(slide, Inches(kx_f), Inches(ky_f), Inches(TILE_W_F-0.04), Inches(0.12), fill=kc)
        T(slide, kname, Inches(kx_f+0.04), Inches(ky_f+0.16), Inches(TILE_W_F-0.10), Inches(0.26),
          size=Pt(7), bold=True, color=NAVY, align=PP_ALIGN.CENTER)
        T(slide, kval, Inches(kx_f+0.04), Inches(ky_f+0.44), Inches(TILE_W_F-0.10), Inches(0.26),
          size=Pt(14), bold=True, color=kc, align=PP_ALIGN.CENTER)
        T(slide, kdelta, Inches(kx_f+TILE_W_F-0.38), Inches(ky_f+0.67), Inches(0.36), Inches(0.14),
          size=Pt(7), color=GREENA, bold=True)

kpi_tiles(sl, PXL_F, [
    ("Agent\nUtilisation", "48%",   "+12pt", NAVY),
    ("AI Acceptance\nRate","72%",   "+8pt",  BLUE),
    ("Override\nRate",      "18%",  "−7pt",  GREENA),
    ("Time Saved\n/Sprint","94 hrs","+22h",  TEAL),
])
kpi_tiles(sl, PXR_F, [
    ("Lead\nTime",    "18 days", "↓ 32%",  NAVY),
    ("Flow\nEff. %",  "24%",     "↑ 6pt",   TEAL),
    ("Deploy\nFreq.", "2×/wk",   "↑ vs 1×", BLUE),
    ("WIP",           "14",      "↓ 4",     GREENA),
])

# ════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — BAR CHART 1: Utilisation % by phase
# ════════════════════════════════════════════════════════════════════════════
CHT1_X = PXL_F + 0.12;  CHT1_Y = PY_F + 1.28;  CHT1_H = 1.72

R(sl, Inches(CHT1_X), Inches(CHT1_Y), Inches(CW_F), Inches(CHT1_H),
  fill=RGBColor(0xF2,0xF6,0xFF), line=RGBColor(0xC5,0xD8,0xEF))
R(sl, Inches(CHT1_X), Inches(CHT1_Y), Inches(CW_F), Inches(0.22), fill=NAVY)
T(sl, "Agent Utilisation Rate by PDLC Phase  (% activities AI-assisted)  |  Target: 40%",
  Inches(CHT1_X+0.08), Inches(CHT1_Y+0.04), Inches(CW_F-0.12), Inches(0.16),
  size=Pt(7.5), bold=True, color=WHITE)

# Pre-compute bar geometry (pure float inches)
MAX_BAR_H1 = 1.10   # max bar height in inches
BAR_BTM1   = CHT1_Y + 0.22 + 0.16 + MAX_BAR_H1   # = CHT1_Y + 1.48
BAR_W1     = (CW_F - 0.20) / 7                     # ≈ 0.859"

for bi, (u, lbl) in enumerate(zip(UTIL_PCT, PH_SHORT)):
    bh_f = MAX_BAR_H1 * u / 100          # pure float
    bx_f = CHT1_X + 0.10 + bi * BAR_W1
    by_f = BAR_BTM1 - bh_f
    bc   = BLUE if u >= 40 else (LBLUE if u >= 26 else RGBColor(0xBB,0xCC,0xEE))
    bar(sl, bx_f+0.06, by_f, BAR_W1-0.12, bh_f, bc, lbl=f"{u}%")
    T(sl, lbl, Inches(bx_f), Inches(BAR_BTM1+0.02), Inches(BAR_W1), Inches(0.20),
      size=Pt(6), color=MGRAY, align=PP_ALIGN.CENTER)

# 40% target dashed line — label on RIGHT side to avoid overlap with Ph1 bar label
TGT1_Y = BAR_BTM1 - MAX_BAR_H1 * 0.40
R(sl, Inches(CHT1_X+0.10), Inches(TGT1_Y), Inches(CW_F-0.20), Inches(0.014), fill=AMBER)
T(sl, "← 40% target", Inches(CHT1_X + CW_F - 0.92), Inches(TGT1_Y - 0.15),
  Inches(0.88), Inches(0.14), size=Pt(6.5), color=AMBER, bold=True)

# ════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — BAR CHART 2: AI Acceptance Rate trend (6 sprints)
# ════════════════════════════════════════════════════════════════════════════
SPK_X = PXL_F + 0.12;  SPK_Y = PY_F + 3.06;  SPK_H = 0.80

R(sl, Inches(SPK_X), Inches(SPK_Y), Inches(CW_F), Inches(SPK_H),
  fill=RGBColor(0xF2,0xF6,0xFF), line=RGBColor(0xC5,0xD8,0xEF))
R(sl, Inches(SPK_X), Inches(SPK_Y), Inches(CW_F), Inches(0.20), fill=BLUE)
T(sl, "AI Acceptance Rate — 6-sprint trend  ·  Target: 85% by Option B",
  Inches(SPK_X+0.08), Inches(SPK_Y+0.03), Inches(CW_F-0.10), Inches(0.16),
  size=Pt(7.5), bold=True, color=WHITE)

MAX_BAR_H2 = 0.34   # reduced so sprint labels fit inside box
SPK_BTM    = SPK_Y + 0.22 + 0.08 + MAX_BAR_H2   # = SPK_Y + 0.64
SPK_BW     = (CW_F - 0.20) / 6                   # ≈ 1.002"

for si, acc in enumerate(SPRINT_ACC):
    bh_f = MAX_BAR_H2 * acc / 100
    bx_f = SPK_X + 0.10 + si * SPK_BW
    by_f = SPK_BTM - bh_f
    bc   = BLUE if acc >= 70 else LBLUE
    bar(sl, bx_f+0.08, by_f, SPK_BW-0.16, bh_f, bc)
    # sprint label below bar, with enough room inside the box
    T(sl, f"S{si+1}  {acc}%", Inches(bx_f), Inches(SPK_BTM+0.02),
      Inches(SPK_BW), Inches(0.14), size=Pt(6.5), color=MGRAY, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — Inference points (AI Adoption)
# ════════════════════════════════════════════════════════════════════════════
IH1_Y = PY_F + 3.92
R(sl, Inches(PXL_F+0.12), Inches(IH1_Y), Inches(PW_F-0.24), Inches(0.24), fill=NAVY)
T(sl, "Inference & Action Points  —  AI Adoption",
  Inches(PXL_F+0.22), Inches(IH1_Y+0.05), Inches(PW_F-0.30), Inches(0.17),
  size=Pt(8.5), bold=True, color=WHITE)
for ii, (txt, ic) in enumerate([
    ("Ph3 Development leads at 52% — CodeGen & Review agents well adopted. "
     "Prioritise Ph6 Deploy (22%) as next activation sprint; target 40%+ for Opt B.",  BLUE),
    ("Acceptance rate growing +4.2 pts/sprint (56%→72%) — on track to reach "
     "85% (Option B target) in ~3 sprints. Consistent quality improvement trend.",     GREENA),
    ("Override rate 18% in QA exceeds <10% target. Prompt recalibration needed "
     "using last 3-sprint rejection reason logs from STUMP Accuracy page.",            AMBER),
    ("Ph7 Ops utilisation 18% — Risk & Monitor agents not yet activated. "
     "Enablement sprint needed before Option B transition is declared.",                NAVY),
]):
    iy = IH1_Y + 0.30 + ii * 0.42
    R(sl, Inches(PXL_F+0.12), Inches(iy), Inches(0.05), Inches(0.34), fill=ic)
    T(sl, txt, Inches(PXL_F+0.22), Inches(iy+0.02),
      Inches(PW_F-0.34), Inches(0.36), size=Pt(8), color=DGRAY)

# ════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — BAR CHART 3: Stacked PT + WT per phase (flow efficiency)
# ════════════════════════════════════════════════════════════════════════════
CHT3_X = PXR_F + 0.12;  CHT3_Y = PY_F + 1.28;  CHT3_H = 1.72
MAX_TOT  = max(p+w for p,w in zip(PHASE_PT, PHASE_WT))   # 9.0

R(sl, Inches(CHT3_X), Inches(CHT3_Y), Inches(CW_F), Inches(CHT3_H),
  fill=RGBColor(0xF2,0xF6,0xFF), line=RGBColor(0xC5,0xD8,0xEF))
R(sl, Inches(CHT3_X), Inches(CHT3_Y), Inches(CW_F), Inches(0.22), fill=PURPLE)
T(sl, "Flow Efficiency by Phase  —  Process Time (blue) vs Wait Time (grey)  (days)",
  Inches(CHT3_X+0.08), Inches(CHT3_Y+0.04), Inches(CW_F-0.12), Inches(0.16),
  size=Pt(7.5), bold=True, color=WHITE)

MAX_BAR_H3 = 1.10
BAR_BTM3   = CHT3_Y + 0.22 + 0.16 + MAX_BAR_H3
BAR_W3     = (CW_F - 0.20) / 7

for bi, (pt, wt) in enumerate(zip(PHASE_PT, PHASE_WT)):
    tot   = pt + wt
    wt_h  = MAX_BAR_H3 * wt / MAX_TOT     # wait time bar height (grey)
    pt_h  = MAX_BAR_H3 * pt / MAX_TOT     # process time bar height (blue)
    bx_f  = CHT3_X + 0.10 + bi * BAR_W3
    # grey (wait) bar — sits below blue
    bar(sl, bx_f+0.06, BAR_BTM3-wt_h-pt_h, BAR_W3-0.12, wt_h, RGBColor(0xAA,0xAA,0xCC))
    # blue (process) bar — sits on top
    bar(sl, bx_f+0.06, BAR_BTM3-pt_h,       BAR_W3-0.12, pt_h, BLUE)
    fe  = round(pt / tot * 100)
    fc  = GREENA if fe >= 35 else (AMBER if fe >= 22 else RGBColor(0xCC,0x44,0x44))
    # Clamp FE label so it never rises above the bar-area top
    fe_label_y = max(CHT3_Y + 0.28, BAR_BTM3 - wt_h - pt_h - 0.18)
    T(sl, f"FE\n{fe}%", Inches(bx_f), Inches(fe_label_y),
      Inches(BAR_W3), Inches(0.20), size=Pt(6.5), bold=True, color=fc, align=PP_ALIGN.CENTER)
    T(sl, PH_SHORT[bi], Inches(bx_f), Inches(BAR_BTM3+0.02),
      Inches(BAR_W3), Inches(0.18), size=Pt(6), color=MGRAY, align=PP_ALIGN.CENTER)
# Legend removed — title bar already reads "blue vs grey"; avoids overlap with axis labels

# ════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — DORA band strip with current/target markers
# ════════════════════════════════════════════════════════════════════════════
DRA_X = PXR_F + 0.12;  DRA_Y = PY_F + 3.06;  DRA_H = 0.80
DRA_BW = (CW_F - 0.16) / 4   # band width ≈ 1.513"

R(sl, Inches(DRA_X), Inches(DRA_Y), Inches(CW_F), Inches(DRA_H),
  fill=RGBColor(0xF2,0xF6,0xFF), line=RGBColor(0xC5,0xD8,0xEF))
R(sl, Inches(DRA_X), Inches(DRA_Y), Inches(CW_F), Inches(0.20), fill=PURPLE)
T(sl, "DORA Band Positioning  —  Current state vs Option B & C targets",
  Inches(DRA_X+0.08), Inches(DRA_Y+0.03), Inches(CW_F-0.10), Inches(0.16),
  size=Pt(7.5), bold=True, color=WHITE)

for di, (dlbl, dc, ddesc, marker, mc) in enumerate([
    ("Low",    RGBColor(0xCC,0x44,0x44), "LT>6m  Monthly deploys",  None,           None),
    ("Medium", AMBER,                    "LT 1w–6m  Weekly deploys", "◀ Now (Opt A)", AMBER),
    ("High",   BLUE,                     "LT 1d–1wk  Daily deploys", "▲ Opt B target",BLUE),
    ("Elite",  GREENA,                   "LT<1d  Multiple/day",      "★ Opt C target", GREENA),
]):
    dbx = DRA_X + 0.08 + di * DRA_BW
    R(sl, Inches(dbx), Inches(DRA_Y+0.22), Inches(DRA_BW-0.04), Inches(0.40), fill=dc)
    T(sl, dlbl, Inches(dbx+0.04), Inches(DRA_Y+0.25), Inches(DRA_BW-0.10), Inches(0.16),
      size=Pt(8), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, ddesc, Inches(dbx+0.04), Inches(DRA_Y+0.42), Inches(DRA_BW-0.10), Inches(0.16),
      size=Pt(6), color=WHITE, align=PP_ALIGN.CENTER)
    if marker:
        T(sl, marker, Inches(dbx), Inches(DRA_Y+0.63), Inches(DRA_BW-0.04), Inches(0.14),
          size=Pt(6.5), bold=True, color=mc, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — Inference points (PDLC Performance)
# ════════════════════════════════════════════════════════════════════════════
IH2_Y = PY_F + 3.92
R(sl, Inches(PXR_F+0.12), Inches(IH2_Y), Inches(PW_F-0.24), Inches(0.24), fill=PURPLE)
T(sl, "Inference & Action Points  —  PDLC Performance",
  Inches(PXR_F+0.22), Inches(IH2_Y+0.05), Inches(PW_F-0.30), Inches(0.17),
  size=Pt(8.5), bold=True, color=WHITE)
for ii, (txt, ic) in enumerate([
    ("Lead time reduced 32% (26→18 days) since AI in Dev & Build. Ph3 cycle time "
     "9→5 days. Ph2 Architecture wait (5 days) is the next improvement target.",    TEAL),
    ("Flow efficiency 24% overall; Ph5 Test wait is highest at 5.5 days. QA "
     "Orchestrator agent (Option B) directly cuts this — FE projected to 38%+.",   AMBER),
    ("Deploy freq 2×/week approaching DORA 'High' band. Release Gate & Deploy "
     "agents (Option B) projected to reach daily cadence by sprint 6.",             BLUE),
    ("CFR at 12% (DORA Medium). As CodeGen matures, target <8% (Option B) via "
     "automated pre-merge AI review and automated quality gate enforcement.",        NAVY),
]):
    iy = IH2_Y + 0.30 + ii * 0.42
    R(sl, Inches(PXR_F+0.12), Inches(iy), Inches(0.05), Inches(0.34), fill=ic)
    T(sl, txt, Inches(PXR_F+0.22), Inches(iy+0.02),
      Inches(PW_F-0.34), Inches(0.36), size=Pt(8), color=DGRAY)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE M11 — Productivity: Measurement, Formula & Automated Data Collection
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
header(sl, "Productivity — Measurement, Formula & Automated Data Collection",
       "Story Points → Effort → Cost  ·  Zero-touch data capture via STUMP ALM Connector", TEAL)
footer(sl, "M11")

# ── Layout constants (all float inches) ──────────────────────────────────────
LM11  = 0.15
CY11  = 1.08
CW1_  = 4.15;  CX1_ = LM11
CW2_  = 4.15;  CX2_ = CX1_ + CW1_ + 0.10
CW3_  = 4.44;  CX3_ = CX2_ + CW2_ + 0.10   # total span ≈ 13.09"

# ── Definition strip ──────────────────────────────────────────────────────────
STRIP_H_ = 0.42
R(sl, Inches(LM11), Inches(CY11), Inches(13.03), Inches(STRIP_H_),
  fill=RGBColor(0xE8,0xF0,0xFB), line=BLUE, lw=Pt(0.5))
strip_defs = [
    ("DEFINITION",   "Productivity  =  Value Delivered  ÷  Capacity Consumed",        NAVY),
    ("PRIMARY UNIT", "Story Points Delivered per Person-Sprint  (calibrated per team)", BLUE),
    ("QUALITY ADJ.", "Multiply × (1 − Change Failure Rate)  to exclude rework waste",  PURPLE),
]
SW_ = 13.03 / 3
for si, (lbl, val, col) in enumerate(strip_defs):
    sx = LM11 + si * SW_
    if si > 0:
        R(sl, Inches(sx - 0.01), Inches(CY11+0.06), Inches(0.015),
          Inches(STRIP_H_-0.12), fill=MGRAY)
    T(sl, lbl, Inches(sx+0.12), Inches(CY11+0.08), Inches(1.08), Inches(0.16),
      size=Pt(7), bold=True, color=col)
    T(sl, val, Inches(sx+1.24), Inches(CY11+0.06), Inches(SW_-1.28), Inches(0.30),
      size=Pt(8), color=DGRAY)

# ── Column boxes ──────────────────────────────────────────────────────────────
COL_TOP_ = CY11 + STRIP_H_ + 0.08   # = 1.58"
COL_BOT_ = 6.55
COL_H_   = COL_BOT_ - COL_TOP_      # = 4.97"
for cx_, cw_, ctitle_, cbg_ in [
    (CX1_, CW1_, "FORMULAS & KEY DIMENSIONS",         NAVY),
    (CX2_, CW2_, "STORY POINTS  →  EFFORT  →  COST",  BLUE),
    (CX3_, CW3_, "WORKED EXAMPLE  —  6-Person Sprint", PURPLE),
]:
    R(sl, Inches(cx_), Inches(COL_TOP_), Inches(cw_), Inches(COL_H_),
      fill=RGBColor(0xF9,0xFB,0xFF), line=RGBColor(0xC5,0xD8,0xEF))
    R(sl, Inches(cx_), Inches(COL_TOP_), Inches(cw_), Inches(0.28), fill=cbg_)
    T(sl, ctitle_, Inches(cx_+0.10), Inches(COL_TOP_+0.05),
      Inches(cw_-0.14), Inches(0.20), size=Pt(8.5), bold=True, color=WHITE)

# ── COL 1: Formulas & Dimensions ─────────────────────────────────────────────
Y1_ = COL_TOP_ + 0.34
FSTEP_ = 0.57
formulas_m11 = [
    ("Primary Productivity",
     "Productivity  =  SP Delivered  ÷  Capacity (person-days)"),
    ("Normalised Velocity",
     "Team Velocity  =  SP / Sprint   [rolling 3-sprint average]"),
    ("Quality-Adjusted",
     "Adj. Productivity  =  SP × (1 – CFR)  ÷  Capacity"),
    ("Productivity Index  (vs Baseline)",
     "Prod. Index  =  (Current SP/day  ÷  Baseline SP/day) × 100"),
]
for fi, (fname_, ftext_) in enumerate(formulas_m11):
    fy_ = Y1_ + fi * FSTEP_
    T(sl, fname_, Inches(CX1_+0.12), Inches(fy_), Inches(CW1_-0.18), Inches(0.18),
      size=Pt(8), bold=True, color=NAVY)
    formula_box(sl, ftext_, Inches(CX1_+0.08), Inches(fy_+0.19),
                Inches(CW1_-0.16), Inches(0.28))

DIM_Y_ = Y1_ + len(formulas_m11) * FSTEP_ + 0.12
T(sl, "KEY DIMENSIONS", Inches(CX1_+0.12), Inches(DIM_Y_),
  Inches(CW1_-0.18), Inches(0.18), size=Pt(7.5), bold=True, color=TEAL)
dim_bullets_ = [
    "Numerator  →  SP with status 'Done' / 'Accepted' at sprint close",
    "Denominator  →  team_size × sprint_days × utilisation % (default 0.8)",
    "CFR  →  prod bugs ÷ items deployed  (trailing 30-day window)",
    "Baseline  →  12-sprint rolling avg captured before AI enablement",
    "Outlier filter  →  stories > 3× team median SP auto-excluded",
]
bullet_lines(sl, dim_bullets_, Inches(CX1_+0.06), Inches(DIM_Y_+0.22),
             Inches(CW1_-0.12), size=Pt(7.5), spacing=Inches(0.215))

# ── COL 2: SP → Effort → Cost chain ──────────────────────────────────────────
Y2_      = COL_TOP_ + 0.34
SBOX_H_  = 0.90
SGAP_    = 0.10
chain_m11 = [
    ("STEP 1  —  CALIBRATE  SP RATE",
     "SP Rate (days/SP)  =  avg Effort Logged ÷ SP Accepted\n"
     "Computed from 6-sprint rolling window via Jira time logs.\n"
     "Typical range: 0.3 – 0.8 days/SP;  recalibrates quarterly.",
     TEAL),
    ("STEP 2  —  SP  →  EFFORT",
     "Effort (person-days)  =  SP Delivered × SP Rate\n"
     "Example:  72 SP  ×  0.5 days/SP  =  36 person-days\n"
     "Represents productive capacity actually consumed.",
     BLUE),
    ("STEP 3  —  EFFORT  →  COST",
     "Cost ($)  =  Effort (days)  ×  Blended Daily Rate\n"
     "Example:  36 days  ×  $800/day  =  $28,800\n"
     "Blended rate from Finance/HR feed or manual config.",
     PURPLE),
    ("STEP 4  —  UNIT ECONOMICS",
     "Cost per SP  =  Total Cost  ÷  SP Delivered\n"
     "Example:  $28,800  ÷  72 SP  =  $400 / Story Point\n"
     "Track sprint-over-sprint to quantify AI efficiency gain.",
     NAVY),
]
for si, (stitle_, sbody_, scol_) in enumerate(chain_m11):
    sy_ = Y2_ + si * (SBOX_H_ + SGAP_)
    if si > 0:
        ax_ = CX2_ + CW2_ / 2 - 0.07
        R(sl, Inches(ax_), Inches(sy_ - SGAP_ + 0.01),
          Inches(0.14), Inches(SGAP_ - 0.01), fill=MGRAY)
    R(sl, Inches(CX2_+0.08), Inches(sy_), Inches(CW2_-0.16), Inches(SBOX_H_),
      fill=RGBColor(0xF2,0xF7,0xFF), line=scol_, lw=Pt(0.75))
    R(sl, Inches(CX2_+0.08), Inches(sy_), Inches(CW2_-0.16), Inches(0.24), fill=scol_)
    T(sl, stitle_, Inches(CX2_+0.18), Inches(sy_+0.04),
      Inches(CW2_-0.28), Inches(0.18), size=Pt(7.5), bold=True, color=WHITE)
    T(sl, sbody_, Inches(CX2_+0.14), Inches(sy_+0.28),
      Inches(CW2_-0.24), Inches(0.58), size=Pt(8), color=DGRAY)

NOTE_Y2_ = Y2_ + len(chain_m11) * (SBOX_H_ + SGAP_) + 0.04
R(sl, Inches(CX2_+0.08), Inches(NOTE_Y2_), Inches(CW2_-0.16), Inches(0.38),
  fill=RGBColor(0xFF,0xF8,0xE8), line=AMBER, lw=Pt(0.6))
T(sl, "All inputs (SP, effort logs, sprint dates) are pulled automatically from Jira / ADO "
       "by the STUMP ALM Connector — no manual data entry at any step.",
  Inches(CX2_+0.14), Inches(NOTE_Y2_+0.07),
  Inches(CW2_-0.24), Inches(0.28), size=Pt(7.5), italic=True, color=AMBER)

# ── COL 3: Worked Example ─────────────────────────────────────────────────────
Y3_ = COL_TOP_ + 0.34
T(sl, "INPUTS  (Sprint 8  ·  Team Alpha)", Inches(CX3_+0.12), Inches(Y3_),
  Inches(CW3_-0.18), Inches(0.18), size=Pt(8), bold=True, color=NAVY)
input_rows_m11 = [
    ("Team size",      "6 engineers"),
    ("Sprint length",  "10 working days"),
    ("Utilisation %",  "80%  (focus factor)"),
    ("Capacity",       "6 × 10 × 0.8  =  48 person-days"),
    ("SP Rate",        "0.5 days/SP  (6-sprint calibration)"),
    ("Blended rate",   "$800 / person-day"),
    ("SP Delivered",   "72 SP  (Done + Accepted at close)"),
]
for ri, (lbl_, val_) in enumerate(input_rows_m11):
    ry_ = Y3_ + 0.22 + ri * 0.24
    ibg_ = RGBColor(0xEF,0xF5,0xFF) if ri % 2 == 0 else WHITE
    R(sl, Inches(CX3_+0.08), Inches(ry_), Inches(CW3_-0.16), Inches(0.22), fill=ibg_)
    T(sl, lbl_, Inches(CX3_+0.14), Inches(ry_+0.03), Inches(1.80), Inches(0.17),
      size=Pt(7.5), bold=True, color=NAVY)
    T(sl, val_, Inches(CX3_+1.96), Inches(ry_+0.03), Inches(CW3_-2.06), Inches(0.17),
      size=Pt(7.5), color=DGRAY)

RES_TOP_ = Y3_ + 0.22 + len(input_rows_m11) * 0.24 + 0.12
T(sl, "CALCULATED RESULTS", Inches(CX3_+0.12), Inches(RES_TOP_),
  Inches(CW3_-0.18), Inches(0.18), size=Pt(8), bold=True, color=GREENA)
results_m11 = [
    ("Productivity",  "72 ÷ 48  =  1.5 SP / person-day",               BLUE),
    ("Effort used",   "72 × 0.5  =  36 person-days",                   BLUE),
    ("Sprint cost",   "36 × $800  =  $28,800",                         BLUE),
    ("Cost / SP",     "$28,800 ÷ 72  =  $400 / Story Point",           PURPLE),
    ("vs Baseline",   "+20% gain  (prev. 60 SP  @  $500/SP)  ↑",       GREENA),
]
for ri, (lbl_, val_, rc_) in enumerate(results_m11):
    ry_ = RES_TOP_ + 0.22 + ri * 0.27
    R(sl, Inches(CX3_+0.08), Inches(ry_), Inches(0.04), Inches(0.20), fill=rc_)
    T(sl, lbl_, Inches(CX3_+0.16), Inches(ry_+0.03), Inches(1.60), Inches(0.18),
      size=Pt(8), bold=True, color=rc_)
    T(sl, val_, Inches(CX3_+1.80), Inches(ry_+0.03), Inches(CW3_-1.88), Inches(0.18),
      size=Pt(8), bold=(ri == len(results_m11)-1), color=DGRAY)

# ── Automated Collection Pipeline ────────────────────────────────────────────
PIPE_Y_ = COL_BOT_ + 0.06
PIPE_H_ = 0.60
R(sl, Inches(LM11), Inches(PIPE_Y_), Inches(13.03), Inches(PIPE_H_),
  fill=RGBColor(0xF0,0xF5,0xFF), line=RGBColor(0xC5,0xD8,0xEF))
T(sl, "AUTOMATED DATA COLLECTION PIPELINE  —  Zero Manual Entry  ·  Outlier Detection  ·  Full Audit Trail",
  Inches(LM11+0.10), Inches(PIPE_Y_+0.05), Inches(7.50), Inches(0.18),
  size=Pt(7.5), bold=True, color=NAVY)

pipe_nodes_m11 = [
    ("Jira / ADO",      "Sprint close\ntrigger",        NAVY),
    ("ALM Connector",   "Webhook +\nbatch pull",         BLUE),
    ("VSM Analyser",    "Cycle time &\nlead time calc",  TEAL),
    ("Metrics Engine",  "Prod., cost &\ntrend compute",  PURPLE),
    ("Dashboard",       "Live charts,\nalerts & export", GREENA),
]
NW_     = (13.03 - 0.20 - 7.60) / 5   # ≈ 1.05" per node in right half... too narrow

# Span the full width instead
NW_ = (13.03 - 0.30) / 5   # ≈ 2.55" per node
for pi, (nname_, ndesc_, ncol_) in enumerate(pipe_nodes_m11):
    nx_ = LM11 + 0.15 + pi * NW_
    if pi > 0:
        R(sl, Inches(nx_ - 0.10), Inches(PIPE_Y_ + PIPE_H_/2 - 0.03),
          Inches(0.12), Inches(0.06), fill=MGRAY)
    R(sl, Inches(nx_+0.06), Inches(PIPE_Y_+0.26),
      Inches(NW_-0.16), Inches(PIPE_H_-0.34), fill=ncol_)
    T(sl, nname_, Inches(nx_+0.06), Inches(PIPE_Y_+0.27),
      Inches(NW_-0.16), Inches(0.15), size=Pt(7.5), bold=True,
      color=WHITE, align=PP_ALIGN.CENTER)
    T(sl, ndesc_, Inches(nx_+0.06), Inches(PIPE_Y_+0.41),
      Inches(NW_-0.16), Inches(0.18), size=Pt(6.5),
      color=WHITE, align=PP_ALIGN.CENTER)

out = "/Users/125066/Library/CloudStorage/OneDrive-Cognizant/Clients/US Bank/New Initiatives/US Bank 2026/STUMP-PDLC-Options-A-B-C.pptx"
prs.save(out)
print(f"Saved  →  {out}  ({len(prs.slides)} slides total)")
