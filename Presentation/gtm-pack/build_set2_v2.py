"""GTM Pack Set 2 v2 — Offering-Centric Pilot Engagement Pack"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gtm_model_2026 as M  # shared 2026 narrative
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from docx import Document
from docx.shared import Pt as DPt, RGBColor as DRGBColor, Inches as DInches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.join(os.path.dirname(__file__), "set2-v2")
os.makedirs(OUT, exist_ok=True)

NAVY=RGBColor(0x0F,0x2D,0x5E); BLUE=RGBColor(0x25,0x63,0xEB)
STEEL=RGBColor(0x1E,0x40,0x8A); PALE=RGBColor(0xDB,0xEA,0xFE)
WHITE=RGBColor(0xFF,0xFF,0xFF); TEXT=RGBColor(0x1E,0x29,0x3B)
LBLUE=RGBColor(0x93,0xC5,0xFD); GHOST=RGBColor(0xEF,0xF6,0xFF)
OPT_A=RGBColor(0x1E,0x40,0x8A); OPT_B=RGBColor(0x25,0x63,0xEB); OPT_C=RGBColor(0x0F,0x2D,0x5E)

DNAVY=DRGBColor(0x0F,0x2D,0x5E); DBLUE=DRGBColor(0x25,0x63,0xEB)
DSTEEL=DRGBColor(0x1E,0x40,0x8A); DWHT=DRGBColor(0xFF,0xFF,0xFF)
DTEXT=DRGBColor(0x1E,0x29,0x3B)

# ── PPTX helpers ──────────────────────────────────────────────────────────────
def new_prs():
    p=Presentation(); p.slide_width=Inches(13.33); p.slide_height=Inches(7.5); return p
def blank(p): return p.slides.add_slide(p.slide_layouts[6])
def R(sl,x,y,w,h,fill=None):
    sh=sl.shapes.add_shape(1,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.line.fill.background()
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb=fill
    else: sh.fill.background()
    return sh
def T(sl,text,x,y,w,h,size=11,bold=False,italic=False,color=None,align=PP_ALIGN.LEFT,wrap=True):
    tb=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tb.word_wrap=wrap; tf=tb.text_frame; tf.word_wrap=wrap
    p=tf.paragraphs[0]; p.alignment=align
    run=p.add_run(); run.text=text; run.font.size=Pt(size)
    run.font.bold=bold; run.font.italic=italic; run.font.name="Calibri"
    run.font.color.rgb=color or TEXT; return tb
def stat(sl,x,y,w,h,val,lbl,bg=BLUE):
    R(sl,x,y,w,h,fill=bg)
    T(sl,val,x,y+0.06,w,h*0.52,size=22,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,lbl,x,y+h*0.52,w,h*0.46,size=8.5,color=WHITE,align=PP_ALIGN.CENTER,wrap=True)
def hdr(sl,title,sub=None):
    R(sl,0,0,13.33,1.05,fill=NAVY)
    T(sl,title,0.4,0.1,10,0.55,size=22,bold=True,color=WHITE)
    if sub: T(sl,sub,0.4,0.62,10,0.38,size=11,color=RGBColor(0xBF,0xDB,0xFE))

# ── DOCX helpers ──────────────────────────────────────────────────────────────
def new_doc():
    d=Document()
    for s in d.styles:
        try:
            if hasattr(s,'font'): s.font.name="Calibri"
        except: pass
    sec=d.sections[0]; sec.top_margin=Cm(2); sec.bottom_margin=Cm(2)
    sec.left_margin=Cm(2.5); sec.right_margin=Cm(2.5); return d
def sf(run,size,bold=False,italic=False,color=None):
    run.font.name="Calibri"; run.font.size=DPt(size)
    run.font.bold=bold; run.font.italic=italic
    if color: run.font.color.rgb=color
def h1(doc,text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(14); p.paragraph_format.space_after=DPt(4)
    r=p.add_run(text); sf(r,16,bold=True,color=DNAVY); return p
def h2(doc,text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(10); p.paragraph_format.space_after=DPt(3)
    r=p.add_run(text); sf(r,13,bold=True,color=DBLUE); return p
def h3(doc,text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(8); p.paragraph_format.space_after=DPt(2)
    r=p.add_run(text); sf(r,11,bold=True,color=DNAVY); return p
def body(doc,text,italic=False,color=None):
    p=doc.add_paragraph(); p.paragraph_format.space_after=DPt(4)
    r=p.add_run(text); sf(r,10.5,italic=italic,color=color); return p
def bul(doc,text):
    p=doc.add_paragraph(style="List Bullet"); p.paragraph_format.space_after=DPt(2)
    r=p.add_run(text); sf(r,10.5); return p
def num(doc,text):
    p=doc.add_paragraph(style="List Number"); p.paragraph_format.space_after=DPt(2)
    r=p.add_run(text); sf(r,10.5); return p
def tbl(doc,headers,rows,col_widths=None):
    t=doc.add_table(rows=1+len(rows),cols=len(headers))
    t.style="Table Grid"; t.alignment=WD_TABLE_ALIGNMENT.LEFT
    for i,h in enumerate(headers):
        cell=t.rows[0].cells[i]
        tc=cell._tc; tcPr=tc.get_or_add_tcPr()
        shd=OxmlElement('w:shd'); shd.set(qn('w:val'),'clear')
        shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'0F2D5E'); tcPr.append(shd)
        p2=cell.paragraphs[0]; p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
        r2=p2.add_run(h); sf(r2,9.5,bold=True,color=DWHT)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            cell=t.rows[ri+1].cells[ci]
            if ri%2==0:
                tc=cell._tc; tcPr=tc.get_or_add_tcPr()
                shd=OxmlElement('w:shd'); shd.set(qn('w:val'),'clear')
                shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'EFF6FF'); tcPr.append(shd)
            p2=cell.paragraphs[0]; r2=p2.add_run(str(val)); sf(r2,9.5)
    if col_widths:
        for i,w in enumerate(col_widths):
            for row in t.rows: row.cells[i].width=DInches(w)
    doc.add_paragraph(); return t
def divider(doc):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(6); p.paragraph_format.space_after=DPt(6)
    pPr=p._p.get_or_add_pPr(); pBdr=OxmlElement('w:pBdr')
    bottom=OxmlElement('w:bottom'); bottom.set(qn('w:val'),'single')
    bottom.set(qn('w:sz'),'6'); bottom.set(qn('w:space'),'1'); bottom.set(qn('w:color'),'2563EB')
    pBdr.append(bottom); pPr.append(pBdr)
def callout(doc,text,fill="DBEAFE"):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(6); p.paragraph_format.space_after=DPt(6)
    p.paragraph_format.left_indent=DPt(24); p.paragraph_format.right_indent=DPt(24)
    pPr=p._p.get_or_add_pPr(); shd=OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),fill); pPr.append(shd)
    r=p.add_run(text); sf(r,10.5,italic=True,color=DNAVY)
def cover(doc,title,subtitle,docnum,version="v2.0"):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(60)
    r=p.add_run("AI-Powered PDLC Transformation"); sf(r,13,bold=True,color=DBLUE)
    p=doc.add_paragraph(); r=p.add_run("GTM Pack — Set 2: Pilot Engagement Pack"); sf(r,11,color=DNAVY)
    doc.add_paragraph()
    p=doc.add_paragraph(); r=p.add_run(title); sf(r,22,bold=True,color=DNAVY)
    p=doc.add_paragraph(); r=p.add_run(subtitle); sf(r,12,italic=True,color=DBLUE)
    doc.add_paragraph(); doc.add_paragraph(); divider(doc)
    tbl(doc,["Document","Version","Date","Classification"],[[docnum,version,"March 2026","Commercial Confidential"]])
    doc.add_page_break()

OFFERING = "AI-Powered PDLC Transformation"
PROOF = "US Bank / Team Phoenix: 42→8 days LT, 17.8%→61% FE, $3M investment, $8.4M/yr benefit, 4.2× ROI, $31.2M 5-year NPV (Option B)"

# ═══════════════════════════════════════════════════════════════════════════════
# 11 — Pilot Proposal Template
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 11-pilot-proposal-template.docx...")
d=new_doc()
cover(d,"Pilot Proposal Template","Phase 1 (Diagnose): AI-Powered PDLC Transformation Engagement","DOC-SET2-11")
h1(d,"Executive Summary")
body(d,"This proposal outlines Phase 1 — Diagnose — of the AI-Powered PDLC Transformation engagement. In 8 weeks, we will quantify your software delivery waste, identify the top 5 bottlenecks by speed, productivity, and quality impact, and deliver a board-ready business case for each of three AI transformation pathways. At the end of Phase 1, you will have everything you need to make an evidence-based investment decision — not a consultant's opinion, but your own data, independently validated.")
callout(d,"This is not a platform sale. It is a consulting engagement. The STUMP is the tool we use to run the diagnosis 5× faster and more accurately than traditional methods. You own the outputs. The insights are yours.")
divider(d)

h1(d,"What Phase 1 Delivers")
body(d,"Phase 1 (Diagnose) is the first of three phases in the AI-Powered PDLC Transformation offering:")
tbl(d,["Phase","Name","Duration","Key Output"],
    [["Phase 1","Diagnose","8 weeks","VSM + DORA + Bottleneck Impact Report + Business Case for 3 Options"],
     ["Phase 2","Design","Concurrent with Phase 1 end","Option selection + Playbook design + Governance model"],
     ["Phase 3","Deliver","Option A: 3–6 months / B: 12–18 months / C: 18–36 months","Implementation + Benefits realisation"]],
    col_widths=[1.0,1.5,2.0,5.0])
body(d,"Phase 1 includes a full Phase 2 design output — at the end of 8 weeks you receive the current state diagnosis AND a board-ready business case for all three AI transformation options. You choose which option to implement in Phase 3.")

h2(d,"Phase 1 Deliverables in Detail")
tbl(d,["Deliverable","Description","Audience","Week"],
    [["D1: Current State VSM Dashboard","AI-generated value stream map: lead time, flow efficiency, process time, and wait time per PDLC phase. Benchmarked against 12 sector peers.","Engineering + CTO","Week 3"],
     ["D2: DORA Assessment","73-question assessment across 4 dimensions. Band classification. Gap analysis against sector leaders.","Engineering + CTO","Week 4"],
     ["D3: Bottleneck Impact Report","Top 5 bottlenecks with annual waste cost (speed / productivity / quality framing). Root cause and peer benchmark.","CTO + VP Eng","Week 4"],
     ["D4: Three-Option Business Case","Option A (AI-Augmented), Option B (Agents+Gates), Option C (Fully Agentic) — ROI, payback, NPV for each.","CFO + CEO","Week 6"],
     ["D5: Legacy Modernisation Assessment","Knowledge Graph readiness score per legacy application. Modernisation strategy per system (replatform / reengineer / decompose). Integrated into transformation roadmap.","CTO + Arch","Week 4"],
     ["D6: Operations Intelligence Report","AIOps maturity score (Reactive → Proactive → Predictive → Autonomous). Operations metrics baseline. Phase 7 deep-dive activities.","Head of Ops","Week 5"],
     ["D7: Transformation Readiness Score","5-dimension readiness assessment (culture, process, technology, data, governance). Role evolution mapping. Change management plan.","HR + CTO","Week 6"],
     ["D8: Governance & Responsible AI Scorecard","Agent accountability matrix. Guardrail configuration. Responsible AI scorecard (transparency, accountability, fairness, security).","CRO + Compliance","Week 6"],
     ["D9: Three-Option Business Case","Option A (AI-Augmented), Option B (Agents+Gates), Option C (Fully Agentic) — ROI, payback, NPV for each.","CFO + CEO","Week 6"],
     ["D10: Option B Playbook Outline","Week-by-week implementation plan for the recommended option (tailored to your bottleneck data).","Programme team","Week 7"],
     ["D11: Executive Readout Deck","15-slide board-ready deck: current state + 3 options + recommendation + next steps.","Board / ELT","Week 8"],
     ["D12: Action Plan (30+ items)","Live in platform: Quick Wins, medium-term, and strategic items with owners and effort estimates. Includes AI Assurance gates.","Team Lead","Week 7"],
     ["D13: Knowledge Transfer","60-min session: platform admin trained; all 21 modules accessible 12 months post-engagement.","Platform Admin","Week 8"]],
    col_widths=[2.2,3.2,2.0,1.0])

divider(d)
h1(d,"The Three Transformation Options — What You Are Choosing Between")
body(d,"Phase 1 produces a business case for all three options. The choice is yours — based on your risk appetite, investment capacity, and transformation ambition.")
tbl(d,["","Option A: AI-Augmented","Option B: Agents + Gates ★","Option C: Fully Agentic"],
    [["Human Role","In the Loop","On the Loop","Above the Loop"],
     ["What changes","AI tools added to each phase","AI agents execute; humans gate","AI end-to-end; humans set strategy"],
     ["Investment","$350–600K","$1.2–2.0M","$3.0–5.0M"],
     ["Annual Benefit","~$2.1M","~$5.5M","$18–30M"],
     ["ROI","2–3×","4–6×","8–12×"],
     ["Payback","6–9 months","10–14 months","14–20 months"],
     ["Speed improvement","+25%","+55%","+75%"],
     ["Productivity improvement","+20%","+50%","+75%"],
     ["Quality improvement","+15%","+35%","+60%"],
     ["Risk","Low","Medium","Medium–High"],
     ["Best for","Risk-averse, regulated teams","Most FS organisations","Digital leaders, greenfield"]],
    col_widths=[2.0,2.8,2.8,2.8])
callout(d,"★ Option B (AI Agents + Human Gates) is recommended for most Financial Services organisations. Best risk-adjusted ROI. Achievable within 12–18 months. Board-approvable investment. US Bank proof: 4.2× ROI, 14-month payback, $31.2M 5-year NPV.")

divider(d)
h1(d,"Commercial Terms")
tbl(d,["Item","Detail"],
    [["Engagement","Phase 1: Diagnose — AI-Powered PDLC Transformation"],
     ["Duration","8 weeks from kick-off"],
     ["Investment","$150,000 (fixed fee)"],
     ["Savings Guarantee","Full refund if we do not identify ≥$500K annual savings"],
     ["Phase 3 pricing","Option A: $350–600K | Option B: $1.2–2.0M | Option C: $3.0–5.0M (outcome-linked)"],
     ["Post-engagement","30-day named support; platform access for 12 months post-engagement"]],
    col_widths=[2.5,7.0])
doc_sign_lines=["Project Sponsor Signature: ___________________________   Date: _______________","Client Project Lead: ___________________________   Date: _______________"]
for l in doc_sign_lines: body(d,l)
h2(d, "How the pilot is framed (2026 model)")
body(d, "The pilot establishes your current maturity level on the L1–L5 ladder, the Target State (North-Star level) and a candidate delivery platform, then sizes the first interim step.")
for lv in M.LADDER:
    bul(d, f"{lv['level']} — {lv['name']}: {lv['summary']}")
body(d, "The business case is a DORA J-Curve (cost-only): up-front investment and a tuition-cost dip, then net savings that grow sprint-on-sprint to breakeven. Ongoing cost is platform-aware and includes agent/token spend. " + M.JCURVE["exclusion"])
d.save(os.path.join(OUT,"11-pilot-proposal-template.docx")); print("  ✓ 11")

# ═══════════════════════════════════════════════════════════════════════════════
# 12 — Project Charter
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 12-project-charter.docx...")
d=new_doc()
cover(d,"Project Charter","AI-Powered PDLC Transformation — Phase 1: Diagnose","DOC-SET2-12")
h1(d,"Project Overview")
tbl(d,["Field","Value"],
    [["Project Name","AI-Powered PDLC Transformation — Phase 1: Diagnose"],
     ["Offering","AI-Powered PDLC Transformation (3-phase consulting engagement)"],
     ["Phase Scope","Phase 1 only — Diagnose. Phases 2 (Design) and 3 (Deliver) are follow-on."],
     ["Client Organisation","[CLIENT NAME]"],
     ["Project Sponsor","[SPONSOR NAME], [TITLE]"],
     ["Pilot Lead (our team)","[PILOT LEAD NAME]"],
     ["Client Project Lead","[CLIENT LEAD NAME], [TITLE]"],
     ["Duration","8 weeks from kick-off"],
     ["Investment","$150,000 (fixed fee)"],
     ["Classification","Commercial Confidential"]],col_widths=[2.5,7.0])

h1(d,"Phase 1 Objectives")
for obj in [
    "Quantify current state software delivery lead time and flow efficiency using the client's ALM data",
    "Identify the top 5 value stream bottlenecks with speed, productivity, and quality impact scores",
    "Benchmark the client's PDLC performance against 12 sector peers",
    "Conduct a 73-question DORA maturity assessment across 4 dimensions",
    "Model all three AI transformation options (A/B/C) against the client's actual data",
    "Produce a board-ready business case for each option (ROI, payback, NPV)",
    "Recommend the optimal option based on client's risk appetite and investment capacity",
    "Deliver a playbook outline for the recommended option",
    "Transfer platform capability to the client team",
]:
    num(d,obj)

callout(d,"Phase 1 Gate: At the end of Week 8, the client will have enough evidence to make an informed decision about which AI transformation option (A, B, or C) to proceed with. This is the Phase 1 exit gate.")

h1(d,"Scope")
h2(d,"In Scope — Phase 1")
for item in [
    "One ALM data source (Jira or Azure DevOps), one product group",
    "AI-generated Current State VSM: 7 PDLC phases, all metrics",
    "DORA assessment: 73 questions across 4 dimensions, 4 data sources",
    "Top 5 bottleneck analysis with annual waste cost and peer benchmarks",
    "Three-option business case: Option A (AI-Augmented), B (Agents+Gates), C (Fully Agentic)",
    "Recommendation with rationale and risk assessment",
    "Playbook outline for recommended option (week-by-week, high level)",
    "Executive readout deck (15 slides, board-ready)",
    "Action plan (25+ items in platform)",
    "Knowledge transfer (60 minutes) and 30-day post-engagement support",
]:
    bul(d,item)

h2(d,"Out of Scope — Phase 1 (Covered in Phase 3)")
for item in [
    "Implementation of any AI agent or improvement initiative",
    "Detailed week-by-week playbook (produced in Phase 3 kick-off)",
    "Change management programme (Phase 3)",
    "Benefits realisation tracking (Phase 3)",
    "More than one product group",
]:
    bul(d,item)

h1(d,"Success Criteria — Phase 1")
tbl(d,["Success Criterion","Measure","Target"],
    [["VSM accuracy","Lead time within ±10% of manual audit","Validated by client engineer"],
     ["Bottleneck quality","Top 3 bottlenecks validated by client SME","Engineer confirms accuracy"],
     ["Business case quality","CFO readability score","≥4/5 from sponsor"],
     ["Option recommendation","Sponsor endorses recommended option","Written endorsement"],
     ["Savings identification","Annual savings opportunity identified","≥$500,000"],
     ["Phase 3 decision","Client actively considering Phase 3","Verbal or written intent to proceed"]],
    col_widths=[3.0,2.5,4.0])
d.save(os.path.join(OUT,"12-project-charter.docx")); print("  ✓ 12")

# ═══════════════════════════════════════════════════════════════════════════════
# 13 — Pilot Delivery Runbook
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 13-pilot-delivery-runbook.docx...")
d=new_doc()
cover(d,"Pilot Delivery Runbook","Phase 1 (Diagnose) Delivery Guide for Transformation Leads","DOC-SET2-13")
h1(d,"Purpose")
body(d,"This runbook guides the Transformation Lead through every step of Phase 1 (Diagnose) of the AI-Powered PDLC Transformation engagement. Phase 1 ends with two outputs: a current state diagnosis AND a board-ready business case for all three AI transformation options. Both are required for the Phase 1 exit gate.")
callout(d,"Phase 1 ends when the client can answer: 'What is our current state?' and 'Which option (A/B/C) should we implement in Phase 3?' — with evidence for both.")

h1(d,"Week-by-Week Delivery Plan")
weeks=[
    ("Week 1–2","Data Onboarding + Platform Setup",
     [("Deploy platform","Install backend + frontend. Configure .env. Run alembic migrations. Verify health endpoint."),
      ("ALM connector","Load Jira/ADO export. Validate 12 required fields. Verify phase mapping."),
      ("Kick-off meeting","Run 90-min kick-off (see Kick-off Guide). Preview the 3 transformation options. Confirm data access."),
      ("DORA sources","Configure 4 sources: Jira, Confluence, SonarQube, GitHub. Test connections.")]),
    ("Week 3–4","AI Analysis + Bottleneck Report",
     [("Run full pipeline","Platform > Analysis > Run Full Analysis. 8 agents across 21 modules, 5–10 minutes."),
      ("Validate VSM accuracy","20-ticket manual audit. LT within ±10% = pass."),
      ("Review DORA results","Check scores. Override if any source failed. Calculate band."),
      ("Bottleneck report","Review top 5 bottlenecks. Map to speed / productivity / quality dimensions. Calculate annual waste cost.")]),
    ("Week 5–6","Option Design Workshop + Business Case",
     [("3-option modelling","Using bottleneck data + DORA scores, model ROI for Option A, B, and C. Show conservative/expected/optimistic for each."),
      ("Option Design Workshop (90 min)","Facilitated session with sponsor and client leads. Present current state. Walk through 3 options. Initial alignment on preferred option. See workshop guide below."),
      ("Business case draft","Build financial model per option. Investment, annual benefit, ROI, payback, NPV. Validate assumptions with Finance."),
      ("Recommendation","Based on DORA score, bottleneck severity, client risk appetite: state recommended option with rationale.")]),
    ("Week 7–8","Playbook + Readout + Handover",
     [("Playbook outline","For recommended option: 3-horizon structure (QW/Medium/Strategic). Top 5 actions per horizon. Named owners if possible."),
      ("Executive readout deck","15 slides: current state + 3 options + recommendation + playbook. Use 01-cxo-pitch-deck-v2 as template."),
      ("Action plan","Load 25+ items into platform. Owners, dates, effort estimates."),
      ("Executive readout delivery","60-min session with ELT. Present current state, 3 options, recommended option."),
      ("Knowledge transfer","60-min: platform admin trained. Exports demonstrated. 30-day support activated.")]),
]
for week, title, steps in weeks:
    h2(d,f"{week}: {title}")
    for step_name, detail in steps:
        h3(d,step_name); body(d,detail)

h1(d,"Option Design Workshop Guide (Week 6)")
body(d,"This 90-minute facilitated session is the pivotal moment in Phase 1. The goal is not to sell Option B — it is to help the client understand the three pathways and identify which aligns with their organisation.")
tbl(d,["Time","Activity","Facilitation Note"],
    [["0:00–0:15","Current state recap: VSM + bottleneck cost","Show the $ impact. Let the data speak. Do not editorialize."],
     ["0:15–0:35","Walk through the 3 options","Use the options slide (Slide 6 of CXO deck). Show metrics for each. Answer questions."],
     ["0:35–0:50","Business case comparison","Show the side-by-side ROI table. Highlight Option B as recommended but not required."],
     ["0:50–1:10","Client discussion: which option aligns?","Ask: 'Based on your risk appetite and investment capacity, which pathway resonates?' Capture preferences."],
     ["1:10–1:20","Playbook preview for preferred option","Show what implementation looks like for the option they lean toward."],
     ["1:20–1:30","Next steps: Phase 3 decision timeline","Agree date for option confirmation. Set Phase 3 kick-off target."]],
    col_widths=[1.2,3.5,4.8])
callout(d,"If the client cannot commit to an option in Week 6, that is fine. Phase 1 still delivers. The readout (Week 8) is the decision point — not the workshop. The workshop is about building understanding.")
d.save(os.path.join(OUT,"13-pilot-delivery-runbook.docx")); print("  ✓ 13")

# ═══════════════════════════════════════════════════════════════════════════════
# 14 — RACI Matrix
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 14-raci-matrix.docx...")
d=new_doc()
cover(d,"RACI Matrix","Roles and Responsibilities — AI-Powered PDLC Transformation Phase 1","DOC-SET2-14")
h1(d,"RACI Key")
tbl(d,["Code","Meaning"],
    [["R","Responsible — does the work"],["A","Accountable — owns the outcome"],
     ["C","Consulted — input required"],["I","Informed — notified of outcome"]])

h1(d,"Phase 1 RACI by Activity")
tbl(d,["Activity","Transform'n Lead","Analyst","Client PM","Client IT","Eng SME","Sponsor"],
    [["Contract + SOW sign-off","C","I","C","I","I","A/R"],
     ["Kick-off meeting facilitation","A/R","C","I","I","I","I"],
     ["Preview: 3 AI transformation options","A/R","C","I","I","C","I"],
     ["ALM data export","C","I","A","R","C","I"],
     ["Platform deployment","A/R","C","I","R","I","I"],
     ["DORA source configuration","A/R","C","I","C","C","I"],
     ["AI pipeline execution (Phase 1 agents)","A/R","C","I","I","I","I"],
     ["VSM accuracy validation","C","I","A","I","R","I"],
     ["Bottleneck review (speed/productivity/quality)","C","I","A","I","R","I"],
     ["Option Design Workshop facilitation","A/R","C","C","I","C","I"],
     ["Option A/B/C selection","C","C","C","I","C","A/R"],
     ["Business case (3-option) review","C","I","A","I","I","R"],
     ["Business case CFO presentation","C","I","C","I","I","A/R"],
     ["Executive readout preparation","A/R","R","C","I","I","C"],
     ["Executive readout delivery","A/R","C","C","I","I","I"],
     ["Phase 3 option decision","C","I","C","I","C","A/R"],
     ["Phase 3 programme kick-off approval","C","I","C","I","I","A/R"],
     ["Knowledge transfer delivery","A/R","R","C","R","C","I"],
     ["Post-Phase 1 support","A/R","R","I","C","I","I"]],
    col_widths=[3.0,0.9,0.9,0.9,0.9,0.9,0.9])

h1(d,"Key Decision Points Requiring Sponsor Accountability")
for item in [
    "Option A/B/C selection — this is the most consequential decision of Phase 1. Sponsor owns it.",
    "Business case CFO endorsement — Finance sign-off before Phase 3 investment is approved.",
    "Phase 3 programme kick-off — formal approval to proceed with the chosen option.",
]:
    bul(d,item)
d.save(os.path.join(OUT,"14-raci-matrix.docx")); print("  ✓ 14")

# ═══════════════════════════════════════════════════════════════════════════════
# 15 — Pilot Findings Readout (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 15-pilot-findings-readout.pptx...")
prs=new_prs()

# Slide 1: Cover
sl=blank(prs)
R(sl,0,0,13.33,7.5,fill=NAVY)
R(sl,0,4.8,13.33,2.7,fill=BLUE)
T(sl,"[CLIENT NAME]",1.0,0.55,11,0.45,size=14,color=RGBColor(0xBF,0xDB,0xFE))
T(sl,"AI-Powered PDLC Transformation",1.0,1.1,11,0.75,size=26,bold=True,color=WHITE)
T(sl,"Phase 1 Complete: Diagnose",1.0,1.95,11,0.55,size=18,color=RGBColor(0xBF,0xDB,0xFE))
T(sl,"Current State Findings + Three Transformation Options + Recommendation",1.0,2.65,10,0.6,size=12,italic=True,color=RGBColor(0x93,0xC5,0xFD))
T(sl,"[DATE]  |  Confidential",1.0,5.2,11,0.45,size=13,color=WHITE)
T(sl,"Accelerated by the STUMP",1.0,5.72,11,0.35,size=10,color=RGBColor(0xBF,0xDB,0xFE))

# Slide 2: Current State VSM
sl=blank(prs)
hdr(sl,"Phase 1: Current State Value Stream Map","[TEAM NAME] — Your PDLC performance, benchmarked")
phases=[("Requirements","PT:[X]h\nWT:[X]h\nFE:[X]%"),("Design &\nArch","PT:[X]h\nWT:[X]h\nFE:[X]%"),
        ("Development","PT:[X]h\nWT:[X]h\nFE:[X]%"),("Code\nReview","PT:[X]h\nWT:[X]h\nFE:[X]%"),
        ("Testing","PT:[X]h\nWT:[X]h\nFE:[X]%"),("Deploy\nPrep","PT:[X]h\nWT:[X]h\nFE:[X]%"),
        ("Release","PT:[X]h\nWT:[X]h\nFE:[X]%")]
for i,(ph,metrics) in enumerate(phases):
    x=0.25+i*1.84
    col=RGBColor(0xEF,0x44,0x44) if i in [4,5] else (STEEL if i in [0,1] else NAVY)
    R(sl,x,1.15,1.72,0.6,fill=col); T(sl,ph,x,1.15,1.72,0.6,size=8.5,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    R(sl,x,1.75,1.72,0.9,fill=GHOST); T(sl,metrics,x+0.05,1.78,1.62,0.84,size=8,color=TEXT)
T(sl,"TOTAL LEAD TIME: [XX] DAYS  |  FLOW EFFICIENCY: [X]%  |  SECTOR AVG: 28 DAYS / 22%",
  0.25,2.78,12.6,0.4,size=10,bold=True,color=NAVY,align=PP_ALIGN.CENTER)
T(sl,"RED = Flow Efficiency < 15% (critical waste zone)  |  Source: [X,XXX] Jira tickets, [DATE RANGE]",
  0.25,3.24,12.6,0.32,size=9,color=RGBColor(0xEF,0x44,0x44))
for i,(dim,detail) in enumerate([("SPEED","[XX]% of LT is queue time — actual delivery work is [X]%"),
                                   ("PRODUCTIVITY","$[X.XM]/yr in engineering time waiting in queues"),
                                   ("QUALITY","Testing FE=[X]% — 89% scheduling overhead, not testing")]):
    R(sl,0.25+i*4.36,3.75,4.15,0.35,fill=NAVY)
    T(sl,dim,0.25+i*4.36,3.75,4.15,0.35,size=10,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,detail,0.35+i*4.36,4.15,4.0,0.4,size=9.5,color=TEXT)

# Slide 3: Bottleneck Scorecard
sl=blank(prs)
hdr(sl,"Top 5 Bottlenecks — Speed, Productivity & Quality Impact","Quantified annual waste with peer benchmark gaps")
for i,(name,sev,dim,waste,bench) in enumerate([
    ("[Bottleneck 1]","Critical","Speed + Quality","[XXX]h/feature | $[X.XM]/yr","Peer avg: [X]h | Gap: [X]h"),
    ("[Bottleneck 2]","Critical","Speed + Productivity","[XXX]h/feature | $[X]K/yr","Peer avg: [X]h | Gap: [X]h"),
    ("[Bottleneck 3]","High","Speed","[XX]h/feature | $[X]K/yr","Peer avg: [X]h | Gap: [X]h"),
    ("[Bottleneck 4]","High","Productivity","[XX]h/feature | $[X]K/yr","Peer avg: [X]h | Gap: [X]h"),
    ("[Bottleneck 5]","Medium","Quality","[XX]h/feature | $[X]K/yr","Peer avg: [X]h | Gap: [X]h"),
]):
    y=1.18+i*1.08
    sc=RGBColor(0xEF,0x44,0x44) if sev=="Critical" else (RGBColor(0xF9,0x73,0x16) if sev=="High" else BLUE)
    R(sl,0.25,y,0.12,0.9,fill=sc)
    T(sl,name,0.5,y+0.06,3.8,0.45,size=11,bold=True,color=TEXT)
    T(sl,f"Impact: {dim}",0.5,y+0.56,2.5,0.32,size=9,color=STEEL)
    T(sl,sev,4.5,y+0.12,1.2,0.45,size=10,bold=True,color=sc,align=PP_ALIGN.CENTER)
    T(sl,waste,5.9,y+0.12,2.8,0.45,size=11,bold=True,color=NAVY,align=PP_ALIGN.CENTER)
    T(sl,bench,8.9,y+0.12,4.2,0.8,size=9,italic=True,color=STEEL,wrap=True)
R(sl,0,6.65,13.33,0.85,fill=NAVY)
T(sl,"Total identified waste: $[X.XM]/yr  |  All five bottlenecks are addressable through Options A, B, or C below",
  0.4,6.7,12.5,0.75,size=10,bold=True,color=WHITE,wrap=True)

# Slide 4: Three AI Transformation Options
sl=blank(prs)
R(sl,0,0,13.33,7.5,fill=RGBColor(0xF8,0xFA,0xFF))
R(sl,0,0,13.33,0.72,fill=NAVY)
T(sl,"Phase 1 Finding: Three AI Transformation Pathways for [CLIENT NAME]",0.4,0.08,12,0.4,size=18,bold=True,color=WHITE)
T(sl,"Each option modelled on your actual bottleneck data and DORA scores",0.4,0.48,12,0.22,size=10,italic=True,color=RGBColor(0xBF,0xDB,0xFE))
OW=4.33
for i,(col,lbl,sub,points,outcome) in enumerate([
    (OPT_A,"OPTION A","AI-Augmented\n(Human In the Loop)",
     ["AI tools at every PDLC phase","Humans retain all decisions","No process redesign","Adopt in 30–60 days/phase","Investment: $350–600K","ROI: 2–3×  |  Payback: 6–9m"],
     "Speed +25% · Productivity +20% · Quality +15%"),
    (OPT_B,"OPTION B ★","Agents + Human Gates\n(Human On the Loop)",
     ["AI agents execute tasks","Humans approve at defined gates","Process redesign: 3–6 months","40–60% effort reduction","Investment: $1.2–2.0M","ROI: 4–6×  |  Payback: 10–14m"],
     "Speed +55% · Productivity +50% · Quality +35%"),
    (OPT_C,"OPTION C","Fully Agentic\n(Human Above the Loop)",
     ["AI owns PDLC end-to-end","Humans set strategy + review exceptions","Full operating model change","70–80% effort reduction","Investment: $3.0–5.0M","ROI: 8–12×  |  Payback: 14–20m"],
     "Speed +75% · Productivity +75% · Quality +60%"),
]):
    x=i*(OW+0.02)
    R(sl,x,0.72,OW,0.52,fill=col)
    T(sl,lbl,x,0.72,OW,0.32,size=12,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,sub,x,1.04,OW,0.22,size=8.5,italic=True,color=WHITE,align=PP_ALIGN.CENTER)
    R(sl,x,1.24,OW,5.52,fill=GHOST)
    for j,pt in enumerate(points):
        T(sl,f"• {pt}",x+0.12,1.35+j*0.58,OW-0.24,0.52,size=9.5,color=TEXT,wrap=True)
    R(sl,x,6.76,OW,0.74,fill=col)
    T(sl,outcome,x+0.1,6.8,OW-0.2,0.66,size=9.5,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
T(sl,"★ Modelled on your data — see Business Case slide for [CLIENT NAME] specific ROI",
  0.25,7.54,12.8,0.3,size=8.5,italic=True,color=NAVY)

# Slide 5: Option B Recommended
sl=blank(prs)
hdr(sl,"Our Recommendation: Option B — AI Agents + Human Gates","Why this is the right pathway for [CLIENT NAME]")
T(sl,"Based on your DORA score of [X.X]/5.0 (WALK band), your top bottleneck profile, and your stated investment capacity, Option B offers the best risk-adjusted return.",
  0.5,1.15,12.3,0.52,size=11,italic=True,color=STEEL)
reasons=[
    ("Your DORA profile supports it","WALK band = sufficient CI/CD foundation for agent automation. CRAWL would require Option A first."),
    ("Your bottleneck profile is ideal","[Bottleneck 1] and [Bottleneck 2] are both directly solved by AI agents with human approval gates."),
    ("Investment is board-approvable","$1.2–2.0M is within VP/CTO approval threshold at most FS organisations — no board vote required."),
    ("Sector proof point","US Bank: same Option B profile. 4.2× ROI, 14-month payback. 42→8 day lead time."),
    ("Lower risk than Option C","Human gates provide the safety net during transition. No full operating model disruption."),
]
for i,(title,detail) in enumerate(reasons):
    y=1.78+i*0.95
    R(sl,0.25,y,0.45,0.75,fill=BLUE)
    T(sl,str(i+1),0.25,y,0.45,0.75,size=16,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,title,0.85,y+0.08,3.5,0.35,size=11,bold=True,color=NAVY)
    T(sl,detail,0.85,y+0.45,12.1,0.4,size=10,color=TEXT,wrap=True)

# Slide 6: Business Case
sl=blank(prs)
hdr(sl,"Business Case — Three Options on Your Data","[CLIENT NAME] specific ROI modelling — conservative / expected / optimistic")
for i,(col,lbl,invest,benefit,roi,payback,npv) in enumerate([
    (OPT_A,"Option A\nAI-Augmented","$350–600K","~$2.1M/yr","2–3×","6–9 months","$8–10M NPV"),
    (OPT_B,"Option B ★\nAgents + Gates","$1.2–2.0M","~$5.5M/yr","4–6×","10–14 months","$28–35M NPV"),
    (OPT_C,"Option C\nFully Agentic","$3.0–5.0M","$18–30M/yr","8–12×","14–20 months","$80–130M NPV"),
]):
    x=0.4+i*4.3
    R(sl,x,1.1,4.0,0.65,fill=col)
    T(sl,lbl,x,1.1,4.0,0.65,size=12,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    for j,(metric,val) in enumerate([("Investment",invest),("Annual Benefit",benefit),("ROI",roi),("Payback",payback),("5-Yr NPV",npv)]):
        R(sl,x,1.8+j*0.95,4.0,0.9,fill=GHOST if j%2==0 else RGBColor(0xFF,0xFF,0xFF))
        T(sl,metric,x+0.15,1.85+j*0.95,2.0,0.38,size=9,color=TEXT)
        T(sl,val,x+2.1,1.85+j*0.95,1.75,0.5,size=12,bold=True,color=col)
R(sl,0,6.65,13.33,0.85,fill=NAVY)
T(sl,"★ Option B recommended. $1.2–2.0M investment → $5.5M/yr → 4.2× ROI → 14-month payback. Sector-proven.",
  0.4,6.7,12.5,0.75,size=10,bold=True,color=WHITE,wrap=True)

# Slide 7: Phase 3 Playbook Overview
sl=blank(prs)
hdr(sl,"Phase 3: Deliver — Option B Implementation Playbook","If Option B is selected: week-by-week from approval to first ROI")
horizons=[
    (NAVY,"QUICK WINS\n0–90 Days","Investment: ~$350K\n→ $1.4M/yr benefit",
     ["Deploy AI agent for [Bottleneck 1]","Automate [Bottleneck 2] gate","First VSM re-run: validate LT reduction","Expected: LT −10 days, FE +10%"]),
    (STEEL,"MEDIUM-TERM\n3–6 Months","Investment: ~$600K\n→ $2.1M incremental",
     ["Add agents for 2 further phases","Redesign human approval gates","Process change + training","Expected: LT −15 days, FE +20%"]),
    (BLUE,"STRATEGIC\n6–12 Months","Investment: ~$1.0M\n→ $2.0M incremental",
     ["Full agent orchestration: all 7 phases","Governance model + DORA uplift","Benefits realisation vs. business case","Expected: LT −[X]d total, FE +[X]%"]),
]
PW=4.05
for i,(col,lbl,invest,bullets) in enumerate(horizons):
    x=0.22+i*(PW+0.12)
    R(sl,x,1.15,PW,0.72,fill=col)
    T(sl,lbl,x+0.14,1.17,PW-0.28,0.45,size=13,bold=True,color=WHITE)
    T(sl,invest,x+0.14,1.62,PW-0.28,0.22,size=8.5,color=RGBColor(0xBF,0xDB,0xFE))
    R(sl,x,1.87,PW,4.0,fill=GHOST)
    for j,b in enumerate(bullets): T(sl,f"• {b}",x+0.16,1.98+j*0.62,PW-0.32,0.58,size=10,color=TEXT,wrap=True)

# Slide 8: Next Steps
sl=blank(prs)
hdr(sl,"Recommended Next Steps","From Phase 1 complete to Phase 3 in motion")
for i,(t,action) in enumerate([
    ("THIS WEEK","Select preferred option (A, B, or C) based on today's readout. Confirm executive sponsor."),
    ("WEEK +1","Share business case with CFO. Obtain budget approval or escalation path."),
    ("WEEK +2","Confirm Phase 3 SOW. Identify transformation programme owner."),
    ("WEEK +3","Phase 3 kick-off: stand up cross-functional pod (Eng + Product + DevOps)."),
    ("MONTH +1","First Quick Win deployment. Platform begins tracking LT and FE improvement."),
    ("MONTH +3","30-day ROI review: first measured LT improvement vs. baseline. Report to ELT."),
    ("MONTH +12","Full Option B complete: [XX]-day LT, [X]% FE. Annual ROI review."),
]):
    y=1.25+i*0.82
    R(sl,0.25,y,1.5,0.65,fill=NAVY if i<3 else (STEEL if i<5 else BLUE))
    T(sl,t,0.28,y+0.1,1.44,0.45,size=10,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,action,1.9,y+0.1,11.0,0.52,size=10.5,color=TEXT,wrap=True)
R(sl,0,7.0,13.33,0.5,fill=BLUE)
T(sl,"Contact: [TRANSFORMATION LEAD NAME]  |  [email]  |  AI-Powered PDLC Transformation",
  0.4,7.05,12.5,0.42,size=11,color=WHITE,align=PP_ALIGN.CENTER)

# New slide: J-Curve trajectory + 3-perspective dashboard
sl = blank(prs)
hdr(sl, "Pilot ROI on the J-Curve", "Investment → tuition-cost dip → breakeven → compounding savings (cost-only)")
for i,(ph,desc) in enumerate(M.JCURVE["phases"]):
    x=0.4+i*3.18; col=[STEEL,RGBColor(0x64,0x74,0x8B),BLUE,NAVY][i]
    R(sl,x,1.3,3.0,0.55,fill=col); T(sl,ph,x+0.1,1.35,2.8,0.46,size=11.5,bold=True,color=WHITE)
    R(sl,x,1.85,3.0,2.1,fill=GHOST); T(sl,desc,x+0.1,1.93,2.8,1.95,size=9.5,color=TEXT)
R(sl,0,4.2,13.33,0.95,fill=PALE)
T(sl,"Ongoing cost is platform-aware and includes agent/token spend. "+M.JCURVE["exclusion"],0.5,4.3,12.4,0.8,size=10.5,color=TEXT)
R(sl,0,5.3,13.33,0.5,fill=NAVY)
T(sl,"Measured on the 3-perspective Outcome Dashboard: "+" · ".join(p["name"] for p in M.OUTCOME_PERSPECTIVES),0.5,5.36,12.4,0.4,size=12,bold=True,color=WHITE)
# New slide: Target State + interim path
sl = blank(prs)
hdr(sl, "From Pilot to Target State", "Current level → interim steps → North-Star, on your chosen platform")
LW=(13.33-0.5*2-0.12*4)/5
for i,lv in enumerate(M.LADDER):
    x=0.5+i*(LW+0.12); col=[STEEL,BLUE,STEEL,BLUE,NAVY][i]
    R(sl,x,1.3,LW,0.6,fill=col); T(sl,f"{lv['level']} {lv['name']}",x+0.06,1.34,LW-0.12,0.52,size=9,bold=True,color=WHITE)
    R(sl,x,1.9,LW,2.6,fill=GHOST); T(sl,lv["summary"],x+0.08,1.98,LW-0.16,2.0,size=8.6,color=TEXT)
    T(sl,lv["option"],x+0.08,4.05,LW-0.16,0.4,size=8,bold=True,color=STEEL)
T(sl,"Platforms: "+" · ".join(p["name"] for p in M.PLATFORMS),0.5,4.75,12.4,0.5,size=10.5,bold=True,color=NAVY)
prs.save(os.path.join(OUT,"15-pilot-findings-readout.pptx")); print("  ✓ 15")

# ═══════════════════════════════════════════════════════════════════════════════
# 16 — Discovery Questionnaire
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 16-discovery-questionnaire.docx...")
d=new_doc()
cover(d,"Discovery Questionnaire","Pre-Engagement Discovery: Understanding Your PDLC and Transformation Ambition","DOC-SET2-16")
body(d,"Instructions: Complete Sections 1–8 before the kick-off meeting. Section 5 (Transformation Ambition) shapes which of the three AI transformation options is right for you; Section 6 covers legacy application context; Section 7 covers Responsible AI governance readiness; Section 8 covers your organisation structure. Estimated time: 45–60 minutes.")
callout(d,"Your answers to this questionnaire shape the Phase 1 diagnosis focus AND inform our initial view on which transformation option (A, B, or C) is likely to be the best fit. There are no wrong answers.")
divider(d)

sections=[
    ("Section 1: Organisation and Delivery Context",[
        ("Organisation name",""),
        ("Industry sector","e.g., Financial Services, Healthcare, Retail, Government"),
        ("Team name and size","The team participating in Phase 1"),
        ("Product / system being measured","Brief description"),
        ("Current average lead time (estimate)","Days from ticket creation to production — even a rough estimate"),
        ("How do you currently measure flow efficiency?","e.g., sprint velocity, cycle time, or 'we don't yet'"),
    ]),
    ("Section 2: ALM and Data",[
        ("ALM system","Jira Cloud / Jira Server / Azure DevOps / Other"),
        ("Approximate ticket count available","Last 12–18 months"),
        ("Sprint cadence","e.g., 2-week sprints, Kanban"),
        ("Known data quality issues","Missing resolved dates? Inconsistent statuses?"),
    ]),
    ("Section 3: DORA and Engineering Maturity",[
        ("Current deployment frequency","How often do you deploy to production?"),
        ("MTTR (estimate)","How long does it take to restore service after an incident?"),
        ("Automated test coverage estimate","% of code covered by automated tests"),
        ("CI/CD maturity (1–5 self-score)","1=no CI/CD, 5=fully automated pipeline"),
    ]),
    ("Section 4: Known Pain Points",[
        ("Top 3 bottlenecks you already know about","What slows you down most?"),
        ("Which PDLC phase takes longest? Why?","Your view before the AI analysis"),
        ("Annual cost estimate of delivery delays","Even a rough figure helps us frame the ROI"),
    ]),
    ("Section 5: AI Transformation Ambition",[
        ("What is your organisation's risk appetite for AI-led process automation?","Low (prefer human control), Medium (comfortable with AI+gates), High (want full automation)"),
        ("Have you discussed the three AI transformation pathways internally?","Option A (Augment), Option B (Agents+Gates), Option C (Fully Agentic)?"),
        ("Which option resonates most at this stage?","Even an initial lean helps us tailor the Phase 1 analysis"),
        ("What's your target transformation timeline?","Quick Wins in 90 days? Full transformation in 12 months? 18–36 months?"),
        ("What investment envelope are you working within?","Helps us focus the business case modelling on the right option"),
        ("Who would be the transformation executive sponsor?","The person accountable for Phase 3 investment and programme outcomes"),
        ("What does 'success' look like for you in 12 months?","One sentence — your definition of a successful transformation"),
    ]),
    ("Section 6: Legacy & Technical Modernisation",[
        ("How many legacy applications are in scope for the transformation?","Rough count — e.g., 3 monoliths, 12 microservices, 2 mainframe systems"),
        ("What is the approximate age and tech stack of your oldest critical system?","e.g., 15-year-old Java monolith, COBOL mainframe"),
        ("Do you have API documentation for these legacy systems?","Yes / Partial / No — this affects Knowledge Graph readiness scoring"),
        ("What is your current test coverage on legacy systems?","Even a rough estimate is useful"),
        ("Has a strangler-fig or replatforming strategy been attempted before?","If yes, what happened?"),
    ]),
    ("Section 7: Governance and Responsible AI Readiness",[
        ("Do you have an AI ethics policy or Responsible AI framework in place?","Yes / In development / No — we will use STUMP's framework as the baseline if not"),
        ("Which regulatory frameworks apply to your AI deployments?","e.g., DORA (EU), FCA AI governance principles, ISO 42001, EU AI Act"),
        ("Who owns AI governance in your organisation?","Role or team accountable for AI ethics and audit"),
        ("Are there existing gates or approval processes that AI agents must operate within?","e.g., Change Advisory Board, security sign-off, legal review"),
        ("What is your organisation's Responsible AI maturity? (1–5 self-score)","1=no framework, 5=certified and audited framework in production"),
    ]),
    ("Section 8: Organisation Structure & Team Context",[
        ("What is your organisation's portfolio/product group hierarchy?","e.g., Organisation > Portfolio > Product Group > Product > Team — how many levels exist?"),
        ("How many teams are in scope for Phase 1?","Phase 1 typically covers 1–3 teams"),
        ("Are all teams using the same ALM tool?","Jira / ADO / Rally — or a mix?"),
        ("Are there shared services teams whose data should be included?","e.g., Platform Engineering, Site Reliability Engineering"),
    ]),
]
for sec_title, questions in sections:
    h1(d,sec_title)
    for i,(q,hint) in enumerate(questions):
        h3(d,f"{i+1}. {q}")
        if hint: body(d,f"Guidance: {hint}",italic=True,color=DBLUE)
        body(d,"Answer: ___________________________________________________________________________")
    divider(d)
d.save(os.path.join(OUT,"16-discovery-questionnaire.docx")); print("  ✓ 16")

# ═══════════════════════════════════════════════════════════════════════════════
# 17 — Kick-off Meeting Guide
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 17-kickoff-meeting-guide.docx...")
d=new_doc()
cover(d,"Kick-off Meeting Guide","Phase 1 (Diagnose) Kick-off — Facilitator's Guide","DOC-SET2-17")
h1(d,"Meeting Purpose")
body(d,"The Phase 1 kick-off has two goals: (1) align all stakeholders on what Phase 1 will deliver and how, and (2) begin building the client's intuition for the three AI transformation options so that the Option Design Workshop in Week 6 is a decision, not an introduction.")
callout(d,"Close the kick-off with this question: 'At the end of 8 weeks, you'll have your current state quantified and a business case for three AI transformation pathways. Our job today is to make sure we capture your data correctly and start building your understanding of the options. Any questions before we begin?'")
tbl(d,["Attribute","Value"],
    [["Duration","90 minutes"],
     ["Format","In-person or video call — screen-share required for platform demo"],
     ["Attendees","Sponsor, Client PM, Platform Admin (IT), Engineering SME (1–2), Transformation Lead, Analyst"],
     ["Key output","Aligned on Phase 1 scope; initial option awareness established; data extract planned"]],
    col_widths=[2.5,7.0])

h1(d,"Detailed Agenda")
agenda=[
    ("0:00–0:05","Welcome and Introductions","Transformation Lead",
     "Name + role around the table. Confirm 90-min format."),
    ("0:05–0:15","Phase 1 Objectives and What You'll Receive","Transformation Lead",
     "Walk through 8 deliverables. Confirm client understands Phase 1 ends with a business case for 3 options, not just a report."),
    ("0:15–0:30","The AI-Powered PDLC Transformation Offering Overview","Transformation Lead",
     "Use the offering slide (01b-offering-slide-v2). Walk through Diagnose/Design/Deliver. Show the 3 options at a high level. Say: 'We'll spend 8 weeks gathering your data so you can make an informed choice between these pathways.'"),
    ("0:30–0:45","Platform Live Demo — 5-Screen Walkthrough","Transformation Lead",
     "ALM Connect → VSM → DORA → Bottlenecks → Business Case. Use US Bank data. Say: 'This is what Phase 1 produces for your team.' Pause after each screen for questions."),
    ("0:45–1:00","Data Requirements Review","Transformation Lead + Client IT",
     "Walk through ALM export checklist field-by-field. Confirm Jira/ADO access. Set delivery date for first extract."),
    ("1:00–1:10","DORA Source Configuration","Transformation Lead + Eng SME",
     "Confirm 4 DORA sources. Client IT sets up read-only tokens this week."),
    ("1:10–1:20","Timeline and Milestones","Transformation Lead",
     "Walk through week-by-week plan. Highlight Week 6 Option Design Workshop. Confirm executive readout date (Week 8). Schedule weekly status calls."),
    ("1:20–1:30","Initial Transformation Ambition Discussion","Transformation Lead",
     "Ask: 'Section 5 of your discovery questionnaire — which option resonated with you at this stage?' No commitment required. Just builds awareness."),
]
for time,title,owner,detail in agenda:
    h2(d,f"{time} — {title}")
    body(d,f"Owner: {owner}",italic=True,color=DBLUE); body(d,detail)

h1(d,"Post-Kick-off Actions (Transformation Lead — within 24 hours)")
for item in [
    "Send meeting notes with action log (data extract date, DORA token setup, weekly call schedule)",
    "Send the three-option overview (one-pager) as a leave-behind — plant the seed for option selection",
    "Send ALM export template (CSV field spec)",
    "Confirm Week 6 Option Design Workshop in calendar",
    "Confirm Week 8 Executive Readout in sponsor's calendar",
]:
    bul(d,item)
d.save(os.path.join(OUT,"17-kickoff-meeting-guide.docx")); print("  ✓ 17")

# ═══════════════════════════════════════════════════════════════════════════════
# 18 — AI Evidence Protocol
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 18-ai-evidence-protocol.docx...")
d=new_doc()
cover(d,"AI Evidence Protocol","Standards for Phase 1 Outputs and the Option Recommendation","DOC-SET2-18")
h1(d,"Purpose")
body(d,"This protocol establishes evidence standards for all outputs produced during Phase 1 (Diagnose) of the AI-Powered PDLC Transformation engagement. It covers the quality standards for the current state diagnosis AND the evidence required to make a credible option recommendation (A, B, or C) to the client.")
callout(d,"Principle: The option recommendation must be grounded in the client's own data — not our preference, not a vendor's pitch. Every recommendation must be traceable to the Phase 1 findings.")

h1(d,"Part 1: Phase 1 Diagnosis Evidence Standards")
h2(d,"Evidence Classification (from Diagnosis)")
tbl(d,["Class","Label","Definition","Requires"],
    [["Class 1","Data-Derived","Directly computed from client ALM data","Source ticket count, date range, field map"],
     ["Class 2","AI-Inferred","AI agent output, confidence ≥0.8","Agent name, confidence score, validation step"],
     ["Class 3","Benchmark-Grounded","Comparison to published or platform benchmark","Source, publication year, peer set definition"],
     ["Class 4","Heuristic Estimate","AI estimate where data is sparse (confidence <0.8)","Disclosure + caveat in readout"]],
    col_widths=[1.0,1.8,3.7,3.0])

h1(d,"Part 2: Option Recommendation Evidence Standards")
body(d,"The option recommendation (A, B, or C) must be supported by four independent evidence inputs. All four must be documented before presenting the recommendation to the executive sponsor.")
tbl(d,["Evidence Input","Description","Minimum Standard","Source"],
    [["DORA Score","Client's overall DORA maturity score","DORA assessment complete; all 4 sources green","Platform: DORA Agent output"],
     ["Bottleneck Profile","Severity and type of top 5 bottlenecks","≥3 validated by client engineer","Bottleneck Analyzer + SME sign-off"],
     ["ROI Modelling","Full business case for all 3 options","Conservative / expected / optimistic per option","Business Case Builder + Finance review"],
     ["Client Risk Appetite","Stated preference from discovery + workshop","Discovery Q5 + Option Design Workshop notes","Documented client statement"]],
    col_widths=[2.0,2.8,2.5,2.2])

h2(d,"Option Recommendation Criteria")
tbl(d,["Recommend","If DORA Score","If Top Bottleneck Profile","If Client Risk Appetite","If Investment Envelope"],
    [["Option A","<1.5 (CRAWL)","Mostly process/culture gaps","Low — prefers human control","<$600K"],
     ["Option B","1.5–3.5 (WALK/RUN)","Agent-automatable bottlenecks dominant","Medium — comfortable with AI+gates","$1–3M"],
     ["Option C",">3.5 (RUN/FLY)","CI/CD + automation already mature","High — wants full autonomy",">$3M"]],
    col_widths=[1.5,1.8,2.8,2.5,2.0])
callout(d,"If the evidence is mixed (e.g., DORA score suggests Option B but investment envelope suggests Option A), present this transparently in the readout. Never force a recommendation that isn't supported by the evidence.")
d.save(os.path.join(OUT,"18-ai-evidence-protocol.docx")); print("  ✓ 18")

# ═══════════════════════════════════════════════════════════════════════════════
# 19 — Risk Register
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 19-risk-register.docx...")
d=new_doc()
cover(d,"Risk Register","Phase 1 Engagement Risk Identification and Mitigation","DOC-SET2-19")
h1(d,"Risk Register")
tbl(d,["ID","Risk","Category","Likelihood (1-5)","Impact (1-5)","Rating","Mitigation","Owner"],
    [["R01","ALM data export blocked by IT","Data","3","5","High","On-prem option; data NDA; IT pre-engagement","Client PM"],
     ["R02","Data quality too poor for VSM (>40% missing dates)","Data","3","4","High","Heuristic LT; data remediation sprint","Transform. Lead"],
     ["R03","Client selects Option C without meeting Option B prerequisites","Option Design","2","5","High","DORA prerequisite gate; phased assessment recommendation","Transform. Lead"],
     ["R04","Business case for chosen option rejected by CFO","Commercial","2","5","High","3-scenario modelling (conservative/expected/optimistic); Finance pre-read","Sponsor"],
     ["R05","Scope creep: client requests Phase 3 work during Phase 1","Scope","4","3","Medium","Clear phase gate in charter; change control process","Transform. Lead"],
     ["R06","Option Design Workshop: client cannot align on option","Decision","3","3","Medium","Options paper left after workshop; readout is decision point, not workshop","Sponsor"],
     ["R07","Key client stakeholder unavailable","Resource","3","3","Medium","Async review via platform; 1h max per week for client team","Client PM"],
     ["R08","AI agent produces inaccurate bottleneck scores","AI","2","3","Medium","Manual override + SME validation in Week 5-6","Transform. Lead"],
     ["R09","Executive readout postponed — no decision on option","Commercial","2","4","Medium","30-day post-Phase 1 support covers rescheduling","Client PM"],
     ["R10","Savings guarantee triggered — refund required","Commercial","1","5","Medium","Pre-qualification: requires >500K savings identifiable from data volume","Transform. Lead"]],
    col_widths=[0.5,2.5,1.2,0.8,0.8,0.8,2.5,1.0])
d.save(os.path.join(OUT,"19-risk-register.docx")); print("  ✓ 19")

# ═══════════════════════════════════════════════════════════════════════════════
# 20 — Pilot Success Scorecard
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 20-pilot-success-scorecard.docx...")
d=new_doc()
cover(d,"Phase 1 Success Scorecard","Measuring the Quality of the Diagnose Phase — Gate to Phase 3","DOC-SET2-20")
h1(d,"Purpose")
body(d,"The Phase 1 Success Scorecard measures the quality and completeness of the Diagnose phase. It is completed jointly by the Transformation Lead and Client PM at the end of Week 8 and serves as the primary evidence for proceeding to Phase 3 (Deliver).")
callout(d,"Phase 1 is successful when the client can say: 'I understand my current state, I understand the three options, and I know which one I want to implement.' The scorecard measures whether we've delivered enough evidence for that decision.")

for dim,max_pts,criteria in [
    ("Dimension 1: Technical Delivery",25,
     [("ALM data loaded and validated","5","5=100%; 3=≥80%; 1=<80%"),
      ("All 8 agents executed successfully","5","5=all 8; 3=6–7; 1=<6 — modules: 21 total"),
      ("VSM accuracy validated by client","5","5=±5%; 3=±10%; 1=>±10%"),
      ("DORA sources connected","5","5=all 4; 3=3; 1=<3"),
      ("Platform uptime","5","5=100%; 3=≥99%; 1=<99%")]),
    ("Dimension 2: Diagnosis Quality",25,
     [("Bottlenecks identified (≥3 with speed/productivity/quality scoring)","5","5=≥5; 3=3–4; 1=<3"),
      ("Annual waste cost quantified per bottleneck","5","5=all 5 costed; 3=3–4; 1=<3"),
      ("Client SME validates top 3 bottlenecks","5","5=all 3; 3=2; 1=<2"),
      ("Benchmark comparisons for all 5 bottlenecks","5","5=all; 3=3–4; 1=<3"),
      ("DORA gap analysis complete","5","5=full; 3=partial; 1=incomplete")]),
    ("Dimension 3: Option Design Quality",25,
     [("All 3 options modelled on client's actual data","5","5=A/B/C all modelled; 1=any missing"),
      ("Business case reviewed by Finance","5","5=signed off; 3=reviewed not approved; 1=not reviewed"),
      ("Option selected or actively under consideration","5","5=selected; 3=in discussion; 1=no progress"),
      ("Sponsor endorses recommendation","5","5=endorsed; 3=supportive; 1=not reviewed"),
      ("Playbook outline produced for chosen option","5","5=complete; 3=draft; 1=not done")]),
    ("Dimension 4: Client Readiness for Phase 3",25,
     [("Platform admin trained","5","5=certified; 3=trained; 1=not trained"),
      ("Action plan (25+ items) in platform with owners","5","5=≥25 with owners; 3=15–24; 1=<15"),
      ("Phase 3 timeline agreed in principle","5","5=date set; 3=in discussion; 1=not discussed"),
      ("Client confidence in Phase 3 (1–5)","5","5=4–5/5; 3=3/5; 1=≤2/5"),
      ("Executive readout delivered and well-received","5","5=sponsor satisfied; 3=further questions; 1=rejected")]),
]:
    h2(d,f"{dim} (Max: {max_pts} points)")
    tbl(d,["Criterion","Max","Scoring Guide","Score"],
        [[c,m,g,""] for c,m,g in criteria],col_widths=[3.5,0.8,3.5,1.0])

h1(d,"Summary and Phase 3 Gate")
tbl(d,["Dimension","Max","Score","% of Max"],
    [["Technical Delivery","25","",""],
     ["Diagnosis Quality","25","",""],
     ["Option Design Quality","25","",""],
     ["Client Readiness for Phase 3","25","",""],
     ["TOTAL","100","",""]],col_widths=[3.5,1.5,2.0,2.0])
tbl(d,["Score","Recommendation","Next Step"],
    [["85–100","Proceed to Phase 3 — Strongly Recommended","Present Phase 3 SOW within 1 week"],
     ["70–84","Proceed with Conditions","Address 1–2 gaps; re-confirm option within 2 weeks"],
     ["55–69","Phase 1 Extension","2-week extension to complete option design; re-score"],
     ["<55","Savings Guarantee Review","Invoke refund clause or negotiate remediation"]],
    col_widths=[1.5,3.0,5.0])
d.save(os.path.join(OUT,"20-pilot-success-scorecard.docx")); print("  ✓ 20")

# ═══════════════════════════════════════════════════════════════════════════════
# 21 — Pilot-to-Scale Framework
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 21-pilot-to-scale-framework.docx...")
d=new_doc()
cover(d,"Transformation Progression Framework","From Phase 1 Diagnose to Enterprise-Wide AI-Native Delivery","DOC-SET2-21")
h1(d,"Overview")
body(d,"The AI-Powered PDLC Transformation is a three-phase consulting offering. 'Scaling' has two dimensions: (1) progressing along the option pathway (Option A → B → C as maturity grows), and (2) expanding across teams (more teams going through the Diagnose → Deliver cycle).")
callout(d,"Most organisations start at Option B (or Option A if DORA is immature), achieve ROI within 12–18 months, then progress to Option C. Simultaneously, they expand the offering to additional teams — each team adds ~65% of the ROI of the first team due to shared infrastructure.")

h1(d,"The Option Progression Pathway")
tbl(d,["Option","Human Role","Typical Entry Criteria","Typical Duration","ROI","Next Step"],
    [["Option A","In the Loop","DORA < 1.5 or very risk-averse org","3–6 months","2–3×","Achieve Option A outcomes → proceed to B"],
     ["Option B ★","On the Loop","DORA 1.5–3.5, moderate risk appetite","12–18 months","4–6×","Achieve Option B outcomes → option to proceed to C"],
     ["Option C","Above the Loop","DORA > 3.5, CI/CD mature, high risk appetite","18–36 months","8–12×","Sustain and expand across all teams"]],
    col_widths=[1.2,1.5,2.8,2.0,1.0,2.5])

h1(d,"The Team Expansion Model")
tbl(d,["Horizon","Phase","Scope","Investment","Cumulative ROI"],
    [["H0","Phase 1 Pilot","1 team — Diagnose + Option Design","$150K","Business case established"],
     ["H1","Phase 3 — QW","1 team — Quick Wins (Option B tier)","$350–600K","First $ savings realised"],
     ["H2","Phase 3 — Full","1 team — Full Option B implementation","$1.2–2.0M","4–6× ROI on 1 team"],
     ["H3","Expand","3–5 teams — Diagnose + Option B","$400K per team","Value compounds per team"],
     ["H4","Enterprise","All teams — Option B/C","$2–5M programme","8–12× at enterprise scale"]],
    col_widths=[1.0,1.8,2.8,2.0,2.5])

h1(d,"Value Scaling Example")
tbl(d,["Teams","Option Level","Annual Savings","Investment","ROI"],
    [["1","Option B","$5.5M","$1.5M","~4×"],
     ["3","Option B","$14M","$3.5M","~5×"],
     ["10","Option B","$40M","$10M","~6×"],
     ["10","Option B → C","$60–80M","$15M","~6–8×"],
     ["20+","Option C","$120M+","$25M","~8–10×"]],
    col_widths=[1.5,2.0,2.5,2.0,1.5])
callout(d,"Infrastructure cost is fixed after the first team. Each additional team adds approximately $30K in platform cost and $150K in delivery cost — against ~$3.5M in annual savings at Option B. The economics improve with every team added.")
d.save(os.path.join(OUT,"21-pilot-to-scale-framework.docx")); print("  ✓ 21")

# ═══════════════════════════════════════════════════════════════════════════════
# 22 — Scale Proposal Deck (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 22-scale-proposal-deck.pptx...")
prs=new_prs()

sl=blank(prs)
R(sl,0,0,13.33,7.5,fill=NAVY); R(sl,0,5.0,13.33,2.5,fill=BLUE)
T(sl,"[CLIENT NAME]",1.0,0.5,11,0.5,size=16,color=RGBColor(0xBF,0xDB,0xFE))
T(sl,"AI-Powered PDLC Transformation",1.0,1.05,11,0.7,size=24,bold=True,color=WHITE)
T(sl,"Phase 3: Deliver — Full Programme Proposal",1.0,1.85,11,0.55,size=17,color=RGBColor(0xBF,0xDB,0xFE))
T(sl,"Building on Phase 1 findings — [X.X]× ROI identified, [OPTION X] selected",1.0,2.55,10,0.5,size=12,italic=True,color=LBLUE)
T(sl,"[DATE]  |  Commercial Confidential",1.0,5.5,11,0.45,size=13,color=WHITE)

sl=blank(prs)
hdr(sl,"Phase 1 Results — What We Diagnosed","The evidence base for your Phase 3 investment decision")
for i,(v,l,bg) in enumerate([("[XX] days","Your Current Lead Time",NAVY),("[X]%","Your Flow Efficiency",STEEL),
                               ("$[X.XM]/yr","Annual Waste Identified",BLUE),("[X] selected","Transformation Option",NAVY)]):
    stat(sl,0.5+i*3.2,1.3,2.8,1.5,v,l,bg)
T(sl,"Phase 1 diagnosis confirmed: [OPTION X] is the recommended pathway for [CLIENT NAME] based on DORA score [X.X], bottleneck profile, and investment envelope.",
  0.5,3.0,12.3,0.55,size=11,italic=True,color=STEEL)
for i,item in enumerate(["Top bottleneck: [Bottleneck 1] — $[X.XM]/yr waste, directly addressable by AI agent","DORA band: [BAND] — [suitable/requires] for [option] implementation","Business case endorsed by [SPONSOR NAME] — [Option X] ROI: [X.X]×, payback: [X] months"]):
    T(sl,f"• {item}",0.5,3.7+i*0.55,12.3,0.5,size=10.5,color=TEXT)

sl=blank(prs)
hdr(sl,"Phase 3 Programme — [OPTION X] Implementation","Week-by-week from approval to full transformation")
for i,(col,lbl,invest,items) in enumerate([
    (NAVY,"QUICK WINS\n0–90 Days","~$[X]K → $[X.X]M/yr",
     ["Deploy AI agent: [Bottleneck 1]","Automate [Bottleneck 2] gate","First VSM re-run: validate LT reduction","Expected: LT −[X]d, FE +[X]%"]),
    (STEEL,"MEDIUM-TERM\n3–6 Months","~$[X]K → $[X.X]M incremental",
     ["Add agents for [X] further phases","Redesign approval gates","Process change + training","Expected: LT −[X]d total, FE +[X]%"]),
    (BLUE,"STRATEGIC\n6–12 Months","~$[X]K → $[X.X]M incremental",
     ["Full agent orchestration","Governance model + DORA uplift","Benefits realisation vs. BC","Expected: LT [X]d, FE [X]%"]),
]):
    x=0.22+i*4.37; PW=4.18
    R(sl,x,1.15,PW,0.72,fill=col)
    T(sl,lbl,x+0.14,1.17,PW-0.28,0.45,size=13,bold=True,color=WHITE)
    T(sl,invest,x+0.14,1.62,PW-0.28,0.22,size=8.5,color=RGBColor(0xBF,0xDB,0xFE))
    R(sl,x,1.87,PW,4.5,fill=GHOST)
    for j,b in enumerate(items): T(sl,f"• {b}",x+0.16,1.98+j*0.75,PW-0.32,0.7,size=10.5,color=TEXT,wrap=True)

sl=blank(prs)
hdr(sl,"Value Scaling — Expanding the Transformation","Each additional team adds ~65% of the first team's ROI")
for i,(teams,invest,savings,roi) in enumerate([
    ("1 team (current)","$[X.X]M","$[X.X]M/yr","[X.X]×"),
    ("3 teams","$[X.X]M","$[X.X]M/yr","[X.X]×"),
    ("10 teams","$[X.X]M","$[X.X]M/yr","[X.X]×"),
]):
    x=0.4+i*4.3
    R(sl,x,1.2,4.0,4.5,fill=GHOST)
    R(sl,x,1.2,4.0,0.55,fill=NAVY if i==0 else (STEEL if i==1 else BLUE))
    T(sl,teams,x,1.2,4.0,0.55,size=13,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    for j,(m,v) in enumerate([("Investment",invest),("Annual Savings",savings),("ROI",roi)]):
        T(sl,m,x+0.2,1.9+j*1.0,1.8,0.4,size=9,color=TEXT)
        T(sl,v,x+2.0,1.9+j*1.0,1.8,0.7,size=16,bold=True,color=NAVY if i==0 else (STEEL if i==1 else BLUE))
T(sl,"Fixed infrastructure cost + increasing savings per team = compounding returns. Most clients expand to 3–5 teams within 12 months of completing Phase 3 for Team 1.",
  0.4,5.95,12.5,0.7,size=10,italic=True,color=TEXT,wrap=True)

sl=blank(prs)
hdr(sl,"Recommended Next Steps","Phase 3 starts here — three actions this week")
for i,(t,action,owner) in enumerate([
    ("1","Confirm [OPTION X] as the Phase 3 pathway and obtain budget approval from CFO","[SPONSOR]"),
    ("2","Identify transformation programme owner and cross-functional pod (Eng + Product + DevOps)","[CLIENT PM]"),
    ("3","Schedule Phase 3 kick-off — Transformation Lead to prepare team-specific playbook","[TRANSFORMATION LEAD]"),
]):
    y=1.4+i*1.8
    R(sl,0.4,y,0.7,0.7,fill=BLUE)
    T(sl,t,0.4,y,0.7,0.7,size=20,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,action,1.3,y+0.05,9.5,0.6,size=12,bold=True,color=TEXT)
    T(sl,f"Owner: {owner}",1.3,y+0.68,9.5,0.4,size=10,italic=True,color=STEEL)
R(sl,0.4,6.65,12.5,0.7,fill=NAVY)
T(sl,"AI-Powered PDLC Transformation — Phase 3 Deliver | Contact: [TRANSFORMATION LEAD] | [email]",
  0.5,6.7,12.3,0.6,size=10.5,color=WHITE,align=PP_ALIGN.CENTER)

# New slide: scaling on the J-Curve at portfolio scale
sl = blank(prs)
hdr(sl, "Scaling the Business Case", "Why the J-Curve turns strongly positive at portfolio scale")
T(sl,"A single team funds only its share of the platform (token + platform-engineering team). Shared platform cost is fixed while "
     "savings scale with every pod adopted — so the programme crosses breakeven sooner and compounds as you scale from 1 → many teams.",
  0.5,1.25,12.3,0.9,size=13,italic=True,color=STEEL)
for i,(ph,desc) in enumerate(M.JCURVE["phases"]):
    x=0.4+i*3.18; col=[STEEL,RGBColor(0x64,0x74,0x8B),BLUE,NAVY][i]
    R(sl,x,2.3,3.0,0.55,fill=col); T(sl,ph,x+0.1,2.35,2.8,0.46,size=11,bold=True,color=WHITE)
    R(sl,x,2.85,3.0,2.0,fill=GHOST); T(sl,desc,x+0.1,2.93,2.8,1.85,size=9.5,color=TEXT)
R(sl,0,5.1,13.33,0.95,fill=NAVY)
T(sl,M.JCURVE["roi_formula"],0.5,5.2,12.4,0.8,size=11.5,bold=True,color=WHITE)
prs.save(os.path.join(OUT,"22-scale-proposal-deck.pptx")); print("  ✓ 22")

files=sorted(os.listdir(OUT))
print(f"\n✓ All Set 2 v2 files complete — {len(files)} files in {OUT}")
for f in files:
    sz=os.path.getsize(os.path.join(OUT,f))
    print(f"  {f} ({sz//1024}KB)")
