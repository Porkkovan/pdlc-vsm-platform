"""GTM Pack Set 3 v2 — Offering-Centric Scale Implementation Pack"""
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

OUT = os.path.join(os.path.dirname(__file__), "set3-v2")
os.makedirs(OUT, exist_ok=True)

NAVY=RGBColor(0x0F,0x2D,0x5E); BLUE=RGBColor(0x25,0x63,0xEB)
STEEL=RGBColor(0x1E,0x40,0x8A); PALE=RGBColor(0xDB,0xEA,0xFE)
WHITE=RGBColor(0xFF,0xFF,0xFF); TEXT=RGBColor(0x1E,0x29,0x3B)
LBLUE=RGBColor(0x93,0xC5,0xFD); GHOST=RGBColor(0xEF,0xF6,0xFF)
GREEN=RGBColor(0x05,0x96,0x69); AMBER=RGBColor(0xD9,0x77,0x06)
OPT_A=RGBColor(0x1E,0x40,0x8A); OPT_B=RGBColor(0x25,0x63,0xEB); OPT_C=RGBColor(0x0F,0x2D,0x5E)

DNAVY=DRGBColor(0x0F,0x2D,0x5E); DBLUE=DRGBColor(0x25,0x63,0xEB)
DSTEEL=DRGBColor(0x1E,0x40,0x8A); DWHT=DRGBColor(0xFF,0xFF,0xFF)
DTEXT=DRGBColor(0x1E,0x29,0x3B); DGREEN=DRGBColor(0x05,0x96,0x69)

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
    doc.add_paragraph()
    p2=doc.add_paragraph()
    r2=p2.add_run(title); sf(r2,22,bold=True,color=DNAVY)
    doc.add_paragraph()
    p3=doc.add_paragraph()
    r3=p3.add_run(subtitle); sf(r3,12,italic=True,color=DSTEEL)
    doc.add_paragraph()
    tbl(doc,["Document","Version","Date","Classification"],
        [[docnum,version,"March 2026","Confidential"]],[2.2,1.2,1.5,2])
    callout(doc,"Consulting offering powered by STUMP — 5× faster delivery, AI-accurate insights, optimal cost.")
    doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 23 — Platform Methodology Guide
# ═══════════════════════════════════════════════════════════════════════════════
def build_23():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nMethodology Guide",
          "Diagnose → Design → Deliver: A Three-Phase Consulting Methodology","Doc-23")
    h1(d,"1. Overview: The Consulting Offering")
    body(d,"AI-Powered PDLC Transformation is a consulting offering that maps your current-state Product Development "
          "Life Cycle (PDLC) using Value Stream Mapping, identifies bottlenecks across speed, productivity, and quality, "
          "then designs and implements the right level of AI transformation. The STUMP accelerates every phase "
          "— making delivery 5× faster, analysis AI-accurate, and total cost optimal.")
    callout(d,"Guiding principle: The methodology delivers transformation; the platform delivers it faster.")
    divider(d)
    h1(d,"2. Three-Phase Methodology")
    h2(d,"Phase 1 — DIAGNOSE: Current State VSM + Bottleneck Analysis")
    body(d,"Objective: Build an accurate, data-driven picture of today's PDLC and identify where speed, productivity, "
          "and quality are constrained.")
    tbl(d,["Step","Activity","Platform Role","Output"],
        [["1.1","PDLC Discovery Workshop","Auto-instruments workflow data","Validated process map"],
         ["1.2","Value Stream Mapping","Generates VSM with AI annotations","Current-state VSM"],
         ["1.3","Bottleneck Scoring","Scores every step across 3 dimensions","Bottleneck heat map"],
         ["1.4","Waste Quantification","Calculates cost of delay per step","Waste register ($)"],
         ["1.5","Stakeholder Alignment","Produces executive summary deck","Findings readout"]],
        [2,3,3,2.5])
    bul(d,"Speed bottlenecks: steps with lead time >2× median")
    bul(d,"Productivity bottlenecks: steps with flow efficiency <25%")
    bul(d,"Quality bottlenecks: steps with defect escape rate >15%")
    divider(d)
    h2(d,"Phase 2 — DESIGN: Three AI Transformation Options + Business Case")
    body(d,"Objective: Present three clearly differentiated paths forward, each with a business case, ROI projection, "
          "and implementation roadmap, so the client can make an informed, risk-calibrated decision.")
    tbl(d,["Option","Human Role","Complexity","Speed Gain","Productivity","Quality","ROI","Investment"],
        [["A — AI-Augmented PDLC","In the loop","Low","+25%","+20%","+15%","2–3×","$350–600K"],
         ["B — AI Agents + Human Gates ★","On the loop","Medium","+55%","+50%","+35%","4–6×","$1.2–2M"],
         ["C — Fully Agentic PDLC","Above the loop","High","~75%","~75%","~60%","8–12×","$3–5M"]],
        [2.3,1.4,1.2,1.1,1.2,1.1,1,1.3])
    callout(d,"Option B is the recommended starting point for most organisations: meaningful AI autonomy with human "
              "oversight at critical gates — delivering 4–6× ROI at manageable risk.")
    h3(d,"Business Case Components (per option)")
    bul(d,"Investment: platform licence + configuration + change management")
    bul(d,"Benefits: speed gains (time-to-market), productivity gains (FTE capacity), quality gains (defect cost avoided)")
    bul(d,"Financial model: NPV, IRR, payback period, 5-year value")
    bul(d,"Risk-adjusted scenarios: conservative / expected / optimistic")
    divider(d)
    h2(d,"Phase 3 — DELIVER: Implementation Playbook + Benefits Tracking")
    body(d,"Objective: Execute the chosen option with a structured delivery methodology, govern progress, and "
          "measure benefits realisation from day one.")
    tbl(d,["Stream","Weeks 1–4","Weeks 5–8","Weeks 9–12","Weeks 13–16"],
        [["Platform","Configure VSM agents","Integrate CI/CD pipeline","Parallel run","Production cutover"],
         ["Process","Document to-be workflows","Train pilot team","Stabilise","Optimise"],
         ["People","Exec alignment","Champions programme","Adoption sprint","Self-sufficiency"],
         ["Governance","KPI baseline","Bi-weekly steering","Mid-point review","Benefits audit"]],
        [2,2.5,2.5,2.5,2.5])
    divider(d)
    h1(d,"3. Platform Acceleration Model")
    body(d,"The STUMP is not the product — it is the engine that makes the consulting offering faster, "
          "more accurate, and more cost-effective.")
    tbl(d,["Activity","Without Platform","With Platform","Gain"],
        [["VSM data collection","3–4 weeks manual","2–3 days automated","10× faster"],
         ["Bottleneck analysis","2 weeks analyst time","Real-time AI scoring","Continuous"],
         ["Option business case","1 week financial model","1-day AI-generated","5× faster"],
         ["Benefits tracking","Monthly spreadsheet","Live dashboard","Real-time"]],
        [3,2.5,2.5,1.5])
    divider(d)
    h1(d,"4. Delivery Standards & Quality Gates")
    h2(d,"Phase 1 Exit Criteria")
    bul(d,"VSM validated by process owners (>80% data accuracy)")
    bul(d,"Bottleneck register signed off by Product and Engineering leads")
    bul(d,"Executive findings readout delivered and accepted")
    h2(d,"Phase 2 Exit Criteria")
    bul(d,"Option selection made by executive sponsor")
    bul(d,"Business case approved by CFO or Finance delegate")
    bul(d,"Implementation charter signed")
    h2(d,"Phase 3 Exit Criteria")
    bul(d,"Platform live in production with active monitoring")
    bul(d,"Benefits baseline captured and first reporting cycle complete")
    bul(d,"Client team self-sufficient (dependency score <20%)")
    h2(d, "The L1–L5 maturity ladder & Target State Studio")
    body(d, "Scale delivery is organised around the L1–L5 ladder, from assisted prompting to autonomous ADLC. The Target State Studio configures the North-Star level and delivery platform, then generates the interim roadmap and operating model per step.")
    for lv in M.LADDER:
        bul(d, f"{lv['level']} {lv['name']} ({lv['ml']}) — agents: {lv['agent_role']}; human-in-the-loop: {lv['hitl']}; automation {lv['automation']}.")
    h2(d, "Delivery platform options")
    tbl(d, ["Platform","Kind","Ongoing cost (incl. agent/token)"], [[p["name"],p["kind"],p["ongoing"]] for p in M.PLATFORMS])
    d.save(os.path.join(OUT,"23-platform-methodology-guide.docx")); print("  ✓ 23")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 24 — Governance Model
# ═══════════════════════════════════════════════════════════════════════════════
def build_24():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nGovernance Model",
          "Steering, Decision Rights & Escalation Across All Three AI Options","Doc-24")
    h1(d,"1. Governance Philosophy")
    body(d,"Governance structures for AI-Powered PDLC Transformation are designed to match the human oversight "
          "model chosen. Option A governs AI-assisted decisions; Option B governs AI-autonomous steps with human "
          "gates; Option C governs AI-driven operations with human policy oversight.")
    callout(d,"Rule: governance complexity scales with AI autonomy. Option A needs lightweight review; "
              "Option C needs robust board-level AI policy oversight.")
    divider(d)
    h1(d,"2. Governance Tiers")
    tbl(d,["Tier","Body","Cadence","Option A","Option B","Option C"],
        [["1 — Strategic","Executive Steering Committee","Monthly","AI initiative KPIs","ROI + gate audit","AI policy + risk"],
         ["2 — Tactical","Transformation Programme Board","Bi-weekly","Sprint review","Autonomous agent log","Agent policy compliance"],
         ["3 — Operational","PDLC Working Group","Weekly","Feature adoption","Gate override log","Anomaly review"],
         ["4 — Technical","Platform Operations","Daily","Usage metrics","Agent performance","Full agent telemetry"]],
        [1.4,2.8,1.4,1.9,1.9,1.9])
    divider(d)
    h1(d,"3. Decision Rights by Option")
    h2(d,"Option A — AI-Augmented (Human In the Loop)")
    body(d,"All AI recommendations require human sign-off before action. Decision rights remain fully with human "
          "roles; AI provides information and suggestions only.")
    tbl(d,["Decision","AI Role","Human Role","Approval Level"],
        [["VSM bottleneck identification","Generates ranked list","Reviews and validates","Team Lead"],
         ["Option selection","Models 3 scenarios","Selects option","Executive Sponsor"],
         ["Process change","Proposes change","Approves change","Process Owner"],
         ["Benefits reporting","Compiles data","Validates and signs","Finance Director"]],
        [3,2.5,2.5,2])
    h2(d,"Option B — AI Agents + Human Gates (Human On the Loop) ★ RECOMMENDED")
    body(d,"AI agents execute defined steps autonomously. Humans review at pre-defined gates before the process "
          "advances. Override capability maintained at all times.")
    tbl(d,["Gate","Trigger","Review Window","Approver","Override Protocol"],
        [["G1 — VSM Complete","Agent finishes VSM","24 hours","Product Director","Manual review mode"],
         ["G2 — Options Ready","Business cases generated","48 hours","CFO/VP Finance","Reject to Phase 1"],
         ["G3 — Config Complete","Platform configured","24 hours","CTO/VP Eng","Config hold"],
         ["G4 — Go Live","Parallel run passed","24 hours","Executive Sponsor","Extend parallel run"]],
        [2.2,2.3,1.5,1.9,2.5])
    h2(d,"Option C — Fully Agentic (Human Above the Loop)")
    body(d,"AI agents operate continuously and autonomously. Humans set policy, define boundaries, and review "
          "exceptions. Governance focuses on AI policy compliance, not individual decisions.")
    tbl(d,["Policy Domain","Policy Owner","Review Cadence","AI Constraint"],
        [["Quality thresholds","VP Engineering","Monthly","Halt if defect rate >5%"],
         ["Security gates","CISO","Weekly","Zero-bypass security checks"],
         ["Spend authority","CFO","Monthly","Auto-reject if >$50K delta"],
         ["Regulatory compliance","Legal/Risk","Quarterly","Mandatory human sign-off"]],
        [2.5,2,1.8,3.2])
    divider(d)
    h1(d,"4. Escalation Framework")
    tbl(d,["Trigger","Level 1 Action","Level 2 Action","Level 3 Action"],
        [["Bottleneck worsens","Working Group review","Programme Board","Executive Steering"],
         ["AI gate override >3×/week","Working Group review","Option reassessment","Board review"],
         ["Benefits <70% of plan","Optimisation sprint","Option upgrade","Transformation reset"],
         ["Security/compliance breach","Immediate platform hold","Incident response","Board notification"]],
        [3,2.5,2.5,2.8])
    divider(d)
    h1(d,"5. STUMP Platform — Governance & AI Assurance Modules")
    body(d,"STUMP provides two dedicated modules to support governance and responsible AI deployment at scale.")
    h2(d,"Governance & Guardrails Module")
    body(d,"The STUMP Governance & Guardrails module provides: (1) an Agent Accountability Matrix mapping all 8 AI agents to their human owner, risk tier, and audit trail; (2) configurable guardrail toggles per governance category (data privacy, PII redaction, financial impact threshold, regulatory compliance); (3) an immutable audit log; and (4) a Responsible AI Scorecard assessing the programme across four dimensions: Transparency, Accountability, Fairness, and Security.")
    h2(d,"AI Assurance Module")
    body(d,"The AI Assurance module runs six validation gates per agent output pipeline: Accuracy (hallucination detection), Precision (citation validation), Bias Monitoring (demographic fairness checks), Drift Detection (model performance degradation), Output Quality Scoring (per-agent accuracy band), and Testing & CI/CD Gate Integration (automated regression on AI output quality). All gate results are logged and available for regulatory examination.")
    callout(d,"For FSI clients operating under DORA (Digital Operational Resilience Act), DAIS (Digital Assets and Infrastructure Security), or equivalent: the Governance & Guardrails + AI Assurance modules produce the artefact set required for Articles 28–44 (ICT risk management) compliance review. Map delivered as part of Phase 2 design.")
    divider(d)
    h1(d,"6. Reporting Cadence")
    tbl(d,["Report","Audience","Frequency","Key Metrics"],
        [["Agent Performance Dashboard","Platform Ops","Daily","Agent uptime, throughput, errors"],
         ["Transformation KPI Report","Programme Board","Bi-weekly","Lead time, FE, quality, adoption"],
         ["Benefits Realisation","Executive Steering","Monthly","ROI vs plan, NPV tracking"],
         ["AI Policy Compliance","Board / Risk Committee","Quarterly","Gate adherence, override rate, policy drift"]],
        [2.5,2.5,1.5,3])
    d.save(os.path.join(OUT,"24-governance-model.docx")); print("  ✓ 24")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 25 — Change Management Plan
# ═══════════════════════════════════════════════════════════════════════════════
def build_25():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nChange Management Plan",
          "People, Culture & Adoption Strategy Across Three AI Options","Doc-25")
    h1(d,"1. Change Management Philosophy")
    body(d,"AI transformation fails when technology is deployed without managing the human side. This plan addresses "
          "the distinct change challenges of each option — from augmenting human work (Option A) to fundamentally "
          "redefining human roles (Option C).")
    callout(d,"Key insight: the higher the AI autonomy, the more intensive the change management required. "
              "Budget change management at 20% of total investment for Option B and 30% for Option C.")
    divider(d)
    h1(d,"2. Stakeholder Impact by Option")
    tbl(d,["Role","Option A Impact","Option B Impact","Option C Impact"],
        [["Product Manager","Gets AI recommendations","Reviews AI-drafted specs","Sets AI product policy"],
         ["Engineer","AI-assisted coding","AI generates boilerplate code","Reviews AI-built components"],
         ["QA Lead","AI flags test gaps","AI runs regression suite","Sets quality policy thresholds"],
         ["Scrum Master","AI highlights blockers","AI manages sprint ceremonies","Monitors AI workflow health"],
         ["Engineering VP","AI-informed reports","Reviews gate approvals","Sets engineering AI policy"],
         ["CFO","AI-generated ROI model","Approves AI business cases","AI-managed budget optimisation"]],
        [2.5,3,3,3])
    divider(d)
    h1(d,"3. Change Readiness Assessment")
    tbl(d,["Dimension","Assessment Questions","Low Score Action","High Score Action"],
        [["Leadership alignment","Do sponsors visibly champion AI transformation?","Executive workshop","Accelerate rollout"],
         ["Cultural openness","How does the team view AI replacing tasks?","Fear/resistance programme","Innovation framing"],
         ["Digital fluency","What is the team's current AI/data literacy?","Foundational training","Advanced enablement"],
         ["Process maturity","Are current PDLC processes documented?","Process baseline first","Direct VSM mapping"],
         ["Change history","How have past transformations landed?","Trust-building phase","Fast-track"]],
        [2,3,3,3])
    divider(d)
    h1(d,"4. Change Programme by Option")
    h2(d,"Option A — Mindset: 'AI as a better tool'")
    tbl(d,["Phase","Activity","Duration","Success Metric"],
        [["Awareness","AI transformation roadshow","Week 1–2","90% attendance"],
         ["Understanding","Hands-on platform demos","Week 2–4","80% 'useful' rating"],
         ["Adoption","Embedded champions","Week 4–8","Feature utilisation >70%"],
         ["Sustain","Monthly learning sessions","Ongoing","NPS >40"]],
        [2,4,1.8,3.2])
    h2(d,"Option B — Mindset: 'AI as a colleague, I govern the gates' ★")
    tbl(d,["Phase","Activity","Duration","Success Metric"],
        [["Awareness","'Future of work' leadership forum","Week 1–2","C-suite alignment"],
         ["Role redesign","New JDs for gate-owner roles","Week 2–4","100% role clarity"],
         ["Skills uplift","AI gate management training","Week 3–8","Certification achieved"],
         ["Adoption","Gate performance coaching","Week 6–12","Override rate <10%"],
         ["Sustain","Quarterly AI maturity reviews","Ongoing","Gate approval SLA <24hr"]],
        [2,4,1.8,3.2])
    h2(d,"Option C — Mindset: 'I set the vision; AI executes'")
    tbl(d,["Phase","Activity","Duration","Success Metric"],
        [["Leadership realignment","Board AI policy workshop","Week 1–4","AI charter published"],
         ["Role transformation","Policy owner role design","Week 2–6","100% policies documented"],
         ["Deep skills","AI systems thinking programme","Week 4–12","Policy fluency certified"],
         ["Governance adoption","AI oversight board established","Week 8–12","Board operational"],
         ["Sustain","Annual AI policy review","Annually","Zero policy breaches"]],
        [2,4,1.8,3.2])
    divider(d)
    h1(d,"5. Communications Plan")
    tbl(d,["Audience","Channel","Frequency","Key Message"],
        [["All staff","All-hands + intranet","Monthly","AI is augmenting your impact"],
         ["Team leads","Leadership briefing","Bi-weekly","Your role in the AI journey"],
         ["Platform users","In-platform notifications","Weekly","New capabilities + tips"],
         ["Executive team","Steering pack","Monthly","ROI progress + decisions required"],
         ["Board","Executive briefing","Quarterly","AI governance + strategic value"]],
        [2,2.5,1.8,3.2])
    divider(d)
    h1(d,"6. Resistance Management")
    tbl(d,["Resistance Type","Root Cause","Response","Owner"],
        [["'AI will replace my job'","Job security fear","Role evolution narrative + new JDs","HR + Line Manager"],
         ["'AI is unreliable'","Trust deficit","Transparent gate metrics + win stories","Platform Champion"],
         ["'Too much change'","Change fatigue","Phased rollout + option A first","Programme Manager"],
         ["'We're different'","Uniqueness bias","Peer benchmarks + proof points","Executive Sponsor"]],
        [2.5,2.5,3,2.5])
    d.save(os.path.join(OUT,"25-change-management-plan.docx")); print("  ✓ 25")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 26 — Platform Configuration Playbook
# ═══════════════════════════════════════════════════════════════════════════════
def build_26():
    d=new_doc()
    cover(d,"STUMP\nConfiguration Playbook",
          "Step-by-Step Setup Guide for AI-Powered PDLC Transformation Delivery","Doc-26")
    h1(d,"1. Configuration Philosophy")
    body(d,"Platform configuration must reflect the client's chosen transformation option. Each option requires "
          "different agent configurations, gate policies, and integration depth. Never over-configure for an option "
          "the client hasn't committed to.")
    callout(d,"Configuration rule: start with Option A baseline, layer Option B gates if selected, "
              "add Option C autonomous policies only after demonstrated gate-management maturity.")
    divider(d)
    h1(d,"2. Pre-Configuration Checklist")
    tbl(d,["Item","Required For","Owner","Status Field"],
        [["Transformation option confirmed","All","Engagement Lead","Option A / B / C"],
         ["Org structure mapped (teams/products)","All","Platform Engineer","Validated"],
         ["PDLC process documented","All","Process Consultant","Uploaded to platform"],
         ["CI/CD system credentials","B, C","Platform Engineer","Connected"],
         ["JIRA/ADO project access","All","Client IT","OAuth configured"],
         ["Baseline KPIs captured","All","Analytics Lead","Uploaded"],
         ["SSO/identity provider","All","Client IT","Configured"],
         ["Data residency requirements","All","Client Legal","Documented"]],
        [3,1.8,2,2.7])
    divider(d)
    h1(d,"3. Core Configuration Steps")
    h2(d,"Step 1: Organisation & Product Hierarchy")
    num(d,"Create Organisation record (name, industry, size band)")
    num(d,"Define Business Segments (e.g. Retail Banking, Commercial Lending)")
    num(d,"Create Digital Products under each segment")
    num(d,"Map Digital Capabilities to each product")
    num(d,"Define Product Groups and Value Stream Steps")
    h2(d,"Step 2: VSM Agent Configuration")
    num(d,"Enable VSM Discovery agent — set data sources (JIRA, ADO, GitHub)")
    num(d,"Configure bottleneck thresholds: Lead Time SLA, Flow Efficiency floor, Defect Escape ceiling")
    num(d,"Set VSM annotation preferences (severity levels, colour coding)")
    num(d,"Schedule automated VSM refresh (daily / weekly / on-demand)")
    h2(d,"Step 3: Option-Specific Agent Setup")
    tbl(d,["Agent","Option A","Option B","Option C"],
        [["Discovery","Read-only recommendations","Active data pull","Continuous autonomous"],
         ["Bottleneck Analysis","Manual trigger","Auto-trigger on threshold breach","Continuous real-time"],
         ["Option Modeller","On-demand","Scheduled weekly","Auto-updates on data change"],
         ["Benefits Tracker","Manual entry","Auto-extracts from CI/CD","Fully automated"],
         ["Alerts","Email digest","In-platform + email","Real-time + escalation"]],
        [2.5,2.5,2.5,2.5])
    h2(d,"Step 4: Gate Configuration (Option B / C only)")
    num(d,"Define gate trigger conditions (completion of prior agent step)")
    num(d,"Assign gate approvers by role (not individual — use role-based routing)")
    num(d,"Set review window (default: 24 hours; override: 48 hours for CFO gates)")
    num(d,"Configure override audit trail (all overrides logged with reason code)")
    num(d,"Test gate flow end-to-end before go-live")
    h2(d,"Step 5: Integration Configuration")
    tbl(d,["Integration","Option A","Option B","Option C","Config Notes"],
        [["JIRA/ADO","Read tickets","Read + write status","Full workflow control","OAuth scope: write"],
         ["GitHub/GitLab","Read PR metrics","Read + annotate","Auto-merge policies","PAT or GitHub App"],
         ["CI/CD pipeline","Read build times","Read + trigger","Full pipeline control","Webhook required"],
         ["Slack/Teams","Notifications","Gate approvals","Policy alerts","Bot installation"]],
        [2.3,1.8,1.8,1.8,2.2])
    divider(d)
    h1(d,"4. Configuration Validation Checklist")
    tbl(d,["Test","Expected Result","Pass Criteria"],
        [["VSM agent generates map","Map with all PDLC steps","Zero missing steps"],
         ["Bottleneck scoring runs","Heat map with scores per step","All steps scored"],
         ["Gate trigger fires","Approver notified within 5 min","SLA <5 min"],
         ["Override logged","Audit log entry created","100% capture rate"],
         ["Benefits dashboard loads","Live metrics displayed","Zero data gaps"],
         ["Integration sync","Data from JIRA/ADO visible","Latency <15 min"]],
        [3,3,3.5])
    divider(d)
    h1(d,"5. Common Configuration Issues & Fixes")
    tbl(d,["Issue","Likely Cause","Fix"],
        [["VSM missing steps","Process not fully documented","Run discovery workshop first"],
         ["Gate not triggering","Trigger condition misconfigured","Check agent completion event name"],
         ["Integration auth failing","Token scope insufficient","Re-issue with write scope"],
         ["Benefits data wrong","Baseline KPI incorrect","Re-baseline from source system"],
         ["Slow agent performance","Large org with no segmentation","Add business segment filters"]],
        [3,3,3.5])
    d.save(os.path.join(OUT,"26-platform-configuration-playbook.docx")); print("  ✓ 26")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 27 — Integration Architecture Guide
# ═══════════════════════════════════════════════════════════════════════════════
def build_27():
    d=new_doc()
    cover(d,"STUMP\nIntegration Architecture Guide",
          "System Connectivity, Data Flows & Security Design","Doc-27")
    h1(d,"1. Integration Architecture Overview")
    body(d,"The STUMP sits as an intelligence and orchestration layer above existing engineering "
          "toolchains. It reads from and, in Options B/C, writes to source systems. All data flows are encrypted, "
          "audited, and role-governed.")
    callout(d,"Architecture principle: the platform never replaces source-of-truth systems — it reads from them, "
              "enriches with AI, and (for Options B/C) writes approved actions back.")
    divider(d)
    h1(d,"2. Integration Landscape")
    tbl(d,["System Category","Tools Supported","Integration Type","Option A","Option B","Option C"],
        [["Project tracking","JIRA, Azure DevOps, Linear","OAuth/REST","Read","Read+Write","Full control"],
         ["Source control","GitHub, GitLab, Bitbucket","Webhook+API","Read PR/commit","Read+Annotate","Policy enforcement"],
         ["CI/CD","Jenkins, GitHub Actions, CircleCI","Webhook","Read builds","Read+Trigger","Full orchestration"],
         ["Communication","Slack, MS Teams","Bot/Webhook","Notifications","Gate approvals","Policy alerts"],
         ["Identity","Okta, Azure AD, Google Workspace","SAML/OIDC","SSO all options","SSO","SSO"],
         ["Data/BI","Snowflake, BigQuery, Databricks","JDBC/API","Export","Export+Import","Bi-directional"],
         ["ITSM","ServiceNow, Jira Service Mgmt","REST","Read incidents","Read+Create","Auto-routing"]],
        [2.5,2.5,1.8,1.1,1.1,1.1])
    divider(d)
    h1(d,"3. Data Flow Diagrams (described)")
    h2(d,"Option A Data Flow")
    body(d,"Source systems → [read-only] → VSM Platform ingestion layer → AI analysis agents → "
          "recommendations dashboard → human decision → manual action in source system.")
    bul(d,"Data pulled on schedule (default: 15-minute polling) or on-demand")
    bul(d,"No write-back to source systems")
    bul(d,"All recommendations logged in platform audit trail")
    h2(d,"Option B Data Flow")
    body(d,"Source systems ↔ [bidirectional] → VSM Platform orchestration layer → autonomous agents → "
          "gate trigger → human approval → approved action written back to source system.")
    bul(d,"Event-driven ingestion: webhooks from JIRA/GitHub/CI trigger agent workflows")
    bul(d,"Gate approval required before write-back executes")
    bul(d,"Full audit log: every read, every agent action, every approval, every write")
    h2(d,"Option C Data Flow")
    body(d,"Source systems ↔ [full control] → VSM Platform orchestration layer → autonomous agents → "
          "policy check → automated action → post-hoc human review of exception log.")
    bul(d,"Continuous event stream processing; no polling delay")
    bul(d,"Actions execute within policy bounds; exceptions escalate to human review")
    bul(d,"Full immutable audit trail with tamper-evident logging")
    divider(d)
    h1(d,"4. Security Architecture")
    tbl(d,["Security Domain","Control","Standard"],
        [["Authentication","SSO via SAML 2.0 / OIDC","NIST SP 800-63B AAL2"],
         ["Authorisation","RBAC with least-privilege","NIST SP 800-53 AC-6"],
         ["Data in transit","TLS 1.3 all connections","FIPS 140-3"],
         ["Data at rest","AES-256 encryption","FIPS 140-3"],
         ["API security","OAuth 2.0 + API key rotation","OWASP API Top 10"],
         ["Audit logging","Immutable append-only log","SOC 2 Type II"],
         ["Vulnerability management","Quarterly pen test + SAST","ISO 27001"],
         ["Data residency","Regional deployment options","GDPR / local data laws"]],
        [2.5,4,3])
    divider(d)
    h1(d,"5. Integration Deployment Checklist")
    tbl(d,["Milestone","Task","Owner","Acceptance Criteria"],
        [["M1","OAuth credentials issued","Client IT","Scopes validated"],
         ["M2","Webhooks configured in source systems","Platform Engineer","Events flowing"],
         ["M3","SSO configured and tested","Client IT + Platform Eng","All users can authenticate"],
         ["M4","Data sync validated","Analytics Lead","KPI data in dashboard"],
         ["M5","Write-back tested (B/C only)","Platform Engineer","Gate + audit confirmed"],
         ["M6","Security review completed","CISO/Security","Sign-off received"]],
        [1.5,3.5,2.5,3])
    d.save(os.path.join(OUT,"27-integration-architecture-guide.docx")); print("  ✓ 27")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 28 — Scale Training Curriculum
# ═══════════════════════════════════════════════════════════════════════════════
def build_28():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nScale Training Curriculum",
          "Role-Based Learning Paths for Options A, B & C","Doc-28")
    h1(d,"1. Training Philosophy")
    body(d,"Training for AI-Powered PDLC Transformation is role-specific and option-specific. The goal is not "
          "to train everyone on the platform — it is to build the precise capabilities each role needs to "
          "operate effectively at the chosen level of AI autonomy.")
    callout(d,"Training investment guideline: Option A = 2 days/person; Option B = 4 days/person; "
              "Option C = 8 days/person (includes policy design and AI oversight certification).")
    divider(d)
    h1(d,"2. Role-Based Learning Paths")
    tbl(d,["Role","Option A Path","Option B Path","Option C Path"],
        [["Executive Sponsor","1h: AI PDLC Transformation overview","2h: Gate governance + ROI","4h: AI policy + board oversight"],
         ["Product Director","2h: VSM reading + action","4h: Gate approval + options","8h: AI product strategy"],
         ["Engineering VP","2h: Bottleneck interpretation","4h: Tech gate decisions","8h: AI engineering policy"],
         ["Scrum Master","4h: Platform workflow integration","8h: AI sprint management","16h: Agentic workflow design"],
         ["Product Manager","4h: AI recommendations usage","8h: AI-drafted specs review","16h: AI backlog policy"],
         ["QA Lead","4h: AI quality scoring","8h: AI test gate management","16h: AI quality policy"],
         ["Platform Admin","8h: Configuration & maintenance","8h + 4h gates","8h + 8h autonomous ops"],
         ["Developer","2h: AI code assist awareness","4h: AI-generated code review","8h: AI pair programming"]],
        [2.5,3,3,3])
    divider(d)
    h1(d,"3. Training Modules (Option B Detailed — Recommended Path)")
    h2(d,"Module 1: AI-Powered PDLC Transformation Overview (2 hours)")
    bul(d,"The consulting offering: Diagnose, Design, Deliver")
    bul(d,"Three transformation options and when to choose each")
    bul(d,"The platform as accelerator — not the product")
    bul(d,"US Bank case study: 42→8 days lead time, 4.2× ROI")
    h2(d,"Module 2: Reading Your VSM (3 hours)")
    bul(d,"How to interpret the current-state VSM map")
    bul(d,"Understanding bottleneck scores: speed, productivity, quality")
    bul(d,"Flow efficiency and lead time calculations")
    bul(d,"How to use AI annotations and confidence scores")
    h2(d,"Module 3: The Three Options Deep Dive (3 hours)")
    bul(d,"Option A: What AI augments, what humans still own")
    bul(d,"Option B: How AI gates work, the approver role, override protocol")
    bul(d,"Option C: What autonomous operation means for your role")
    bul(d,"Business case literacy: ROI, NPV, payback")
    h2(d,"Module 4: Gate Management Certification (4 hours)")
    bul(d,"Gate approver responsibilities and SLAs")
    bul(d,"What to check at each gate (VSM complete, options ready, config complete, go-live)")
    bul(d,"Override protocol: when to use it, how to document it")
    bul(d,"Practical simulation: 4 gate scenarios with decision coaching")
    h2(d,"Module 5: Benefits Tracking & Continuous Improvement (2 hours)")
    bul(d,"Reading the benefits dashboard")
    bul(d,"Leading vs lagging indicators")
    bul(d,"How to interpret variance to plan")
    bul(d,"Escalation path when benefits are off-track")
    divider(d)
    h1(d,"4. Training Delivery Model")
    tbl(d,["Format","Use Case","Duration","Max Group Size"],
        [["Executive briefing","Sponsor + leadership alignment","2 hours","10 pax"],
         ["Workshop (instructor-led)","Core team training (Modules 1–4)","1 day","20 pax"],
         ["Hands-on lab","Platform configuration + gate simulation","Half day","12 pax"],
         ["E-learning modules","Self-paced reinforcement","2–4 hours total","Unlimited"],
         ["Certification exam","Gate Manager certification (Option B)","1 hour","Individual"],
         ["Train-the-trainer","Enable client to sustain delivery","2 days","4 trainers"]],
        [2.2,3,1.8,2])
    divider(d)
    h1(d,"5. Competency Assessment")
    tbl(d,["Role","Assessment Method","Pass Standard","Re-assessment"],
        [["Gate Approver","Simulation + MCQ exam","80%+ correct","Annual"],
         ["Platform Admin","Live configuration task","Zero critical errors","On role change"],
         ["Executive Sponsor","Scenario discussion","Informed decision demonstrated","Annual"],
         ["Developer","Code review simulation","Correct AI output evaluation","Annual"]],
        [2.5,3,2,2])
    d.save(os.path.join(OUT,"28-scale-training-curriculum.docx")); print("  ✓ 28")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 29 — Adoption Playbook
# ═══════════════════════════════════════════════════════════════════════════════
def build_29():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nAdoption Playbook",
          "Driving Sustained Usage, Engagement & Value Realisation","Doc-29")
    h1(d,"1. Adoption Strategy")
    body(d,"Technology adoption fails when it is treated as a one-time training event. This playbook defines a "
          "sustained adoption programme that drives usage from pilot to enterprise scale, building a self-reinforcing "
          "cycle of visible value and growing engagement.")
    callout(d,"Adoption target: 80% of intended users actively using the platform within 90 days of go-live. "
              "Measured weekly by role and team, reported to steering monthly.")
    divider(d)
    h1(d,"2. Adoption Metrics")
    tbl(d,["Metric","Definition","Target (90 days)","Target (12 months)"],
        [["Active users","Users logged in within last 7 days","70% of licensed seats","85% of licensed seats"],
         ["VSM views","VSM map opened per team per week",">3/week per team",">5/week per team"],
         ["Gate approvals","Option B/C gates processed on time",">90% within SLA",">95% within SLA"],
         ["AI rec actioned","AI recommendations acted on",">50% of recommendations",">70% of recommendations"],
         ["Benefits dashboard","Benefits dashboard viewed by sponsor","Weekly","Weekly"],
         ["Platform NPS","Net Promoter Score",">30",">45"]],
        [2.8,3.5,2.5,2.5])
    divider(d)
    h1(d,"3. Champions Programme")
    body(d,"Platform Champions are embedded advocates — typically Scrum Masters or senior engineers — who "
          "support adoption within their team, surface issues early, and represent the platform in team ceremonies.")
    tbl(d,["Champion Role","Responsibilities","Time Commitment","Support Provided"],
        [["Team Champion (per squad)","Daily usage support, team Q&A, issue escalation","2h/week","Training + quarterly meetup"],
         ["Product Champion (per product)","Cross-team consistency, best practices","3h/week","Advanced training + direct access"],
         ["Executive Champion","Visibility, air cover, escalation","1h/month","Exec briefing pack"]],
        [2.5,4,2,2.5])
    divider(d)
    h1(d,"4. Adoption Sprint Cadence")
    tbl(d,["Sprint","Focus","Activities","Success Gate"],
        [["Sprint 1 (weeks 1–2)","Awareness & first login","Roadshow, demo, account setup","80% first login"],
         ["Sprint 2 (weeks 3–4)","First value","VSM walkthrough, first bottleneck review","50% VSM viewed"],
         ["Sprint 3 (weeks 5–6)","Habit formation","Champions embedded, weekly VSM ritual","60% active users"],
         ["Sprint 4 (weeks 7–8)","Gate fluency (B/C)","Gate simulation, first live gate","90% gate SLA met"],
         ["Sprint 5 (weeks 9–10)","Benefits visibility","Dashboard walkthrough, first report","Benefits report delivered"],
         ["Sprint 6 (weeks 11–12)","Self-sufficiency","Reduced consultant support","<20% consultant dependency"]],
        [2.3,2.2,4,2.5])
    divider(d)
    h1(d,"5. Adoption by Option")
    h2(d,"Option A Adoption Focus")
    bul(d,"Build the habit of checking AI recommendations before making process decisions")
    bul(d,"Weekly VSM review ritual embedded in team of teams meeting")
    bul(d,"Adoption KPI: % of sprint retros that reference VSM findings")
    h2(d,"Option B Adoption Focus ★")
    bul(d,"Gate approver cadence: daily 15-minute gate review slot in calendar")
    bul(d,"Override governance: every override reviewed in team of teams weekly")
    bul(d,"Adoption KPI: gate SLA adherence rate (target >90%)")
    bul(d,"Celebration: 'Gate Champion of the Month' recognition programme")
    h2(d,"Option C Adoption Focus")
    bul(d,"Policy review cadence: monthly AI policy board review")
    bul(d,"Exception review: weekly anomaly review is the primary human touchpoint")
    bul(d,"Adoption KPI: policy exception rate (target <2% of agent actions)")
    divider(d)
    h1(d,"6. Resistance Recovery")
    tbl(d,["Resistance Signal","Diagnosis","Intervention","Owner"],
        [["Low login rate","Lack of habit or incentive","Champions + manager prompt","Team Lead"],
         ["Gate overrides high","Distrust of AI or poor config","Config review + trust session","Platform Lead"],
         ["Recommendations ignored","Poor recommendation quality","Agent recalibration","Platform Engineer"],
         ["Executive disengagement","Not seeing value","Benefits report + exec champion","Programme Lead"]],
        [2.5,2.5,3,2])
    d.save(os.path.join(OUT,"29-adoption-playbook.docx")); print("  ✓ 29")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 30 — QA Framework
# ═══════════════════════════════════════════════════════════════════════════════
def build_30():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nQA Framework",
          "Quality Assurance Across Consulting Delivery, Platform Configuration & AI Outputs","Doc-30")
    h1(d,"1. QA Philosophy")
    body(d,"Quality in AI-Powered PDLC Transformation spans three layers: the quality of the consulting delivery "
          "(are we doing the right things), the quality of platform configuration (is it set up correctly), and "
          "the quality of AI agent outputs (are the recommendations accurate and actionable).")
    callout(d,"QA principle: automated checks for platform and AI quality; human expert review for "
              "consulting quality. Never automate what requires professional judgement.")
    divider(d)
    h1(d,"2. Quality Dimensions")
    tbl(d,["Quality Layer","What is Assessed","Assessment Method","Frequency"],
        [["Consulting delivery","Methodology adherence, stakeholder satisfaction","Peer review + client survey","Per phase"],
         ["Platform configuration","Correct setup per chosen option","Configuration validation checklist","Pre go-live + quarterly"],
         ["AI agent outputs","Accuracy of VSM, bottleneck scoring, recommendations","Calibration study","Monthly"],
         ["Benefits realisation","Actual vs projected outcomes","Benefits tracker review","Monthly"],
         ["Change management","Adoption rates, NPS, sentiment","Adoption dashboard","Weekly"]],
        [2.5,3.5,2.5,1.5])
    divider(d)
    h1(d,"3. Consulting Delivery QA")
    h2(d,"Phase Gate Reviews")
    tbl(d,["Gate","Review Panel","Criteria","Outcome"],
        [["Phase 1 Exit","Engagement Lead + Client Sponsor","VSM accuracy >80%, bottlenecks agreed","Proceed / Re-do"],
         ["Phase 2 Exit","Engagement Lead + CFO delegate","Option selected, business case approved","Proceed / Revise"],
         ["Phase 3 Mid-point","Steering Committee","Adoption >50%, benefits on track","Proceed / Intervene"],
         ["Phase 3 Exit","Executive Sponsor","All success criteria met","Close / Extend"]],
        [2,3,3.5,2])
    h2(d,"Peer Review Standards")
    bul(d,"All client-facing deliverables peer reviewed by a senior consultant before submission")
    bul(d,"VSM maps reviewed by a certified VSM practitioner")
    bul(d,"Business cases reviewed by a qualified financial analyst")
    bul(d,"AI policy documents (Option C) reviewed by AI ethics and legal advisors")
    divider(d)
    h1(d,"4. Platform Configuration QA")
    tbl(d,["Test Type","Description","Pass Criteria","When Run"],
        [["Smoke test","Basic platform health check","All 8 core functions operational","Post-install"],
         ["Integration test","Data flowing from all connected systems","Zero data gaps","Post-integration"],
         ["Agent accuracy test","Run VSM on known dataset; verify outputs","Within 5% of expected","Pre go-live"],
         ["Gate flow test","Trigger, approve, and override all 4 gates","100% audit captured","Pre go-live"],
         ["Load test","50 concurrent users; 10 simultaneous agent runs","Response <3s","Pre go-live"],
         ["Security test","Pen test + SAST scan","Zero critical findings","Pre go-live + annual"]],
        [2.5,4,2.5,1.8])
    divider(d)
    h1(d,"5. AI Agent Output Quality")
    h2(d,"Calibration Process")
    body(d,"Monthly calibration study: run platform agents on a held-out historical dataset with known outcomes. "
          "Compare AI output to validated ground truth. Recalibrate agent scoring weights if accuracy falls below threshold.")
    tbl(d,["Agent","Accuracy Threshold","Calibration Dataset","Recalibration Trigger"],
        [["VSM Discovery","±5% step count accuracy","Previous quarter VSM","Accuracy <95%"],
         ["Bottleneck Scorer","±10% ranking accuracy","Validated bottleneck register","Accuracy <90%"],
         ["Option Modeller","±15% ROI projection accuracy","Completed engagement actuals","Accuracy <85%"],
         ["Benefits Tracker","±5% metric extraction accuracy","Source system actuals","Accuracy <95%"]],
        [2.5,2.5,3,2.5])
    divider(d)
    h1(d,"6. Defect Management")
    tbl(d,["Defect Severity","Definition","Response Time","Escalation"],
        [["Critical","Platform down or AI producing incorrect data","2 hours","CTO + Client IT Director"],
         ["High","Key feature broken, gate not triggering","8 hours","Engagement Lead"],
         ["Medium","Non-critical feature degraded","24 hours","Platform Team"],
         ["Low","UI issue or minor data display","5 business days","Standard backlog"]],
        [2,4,2,2.5])
    d.save(os.path.join(OUT,"30-qa-framework.docx")); print("  ✓ 30")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 31 — Benefits Tracker Template
# ═══════════════════════════════════════════════════════════════════════════════
def build_31():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nBenefits Tracker Template",
          "Measuring Speed, Productivity & Quality ROI Across All Three Options","Doc-31")
    h1(d,"1. Benefits Tracking Framework")
    body(d,"Benefits realisation must be tracked from the moment baseline is captured, not from go-live. "
          "This template provides the measurement structure for all three AI transformation options, "
          "aligned to the three benefit dimensions: Speed, Productivity, and Quality.")
    callout(d,"Benefits tracking is a governance requirement. Monthly benefits reports must be presented "
              "to the Executive Steering Committee as part of the transformation governance cycle.")
    divider(d)
    h1(d,"2. Baseline Capture Template")
    tbl(d,["Metric","Definition","Source System","Baseline Value","Baseline Date","Owner"],
        [["Lead Time","Avg days from idea to production","JIRA/ADO","__ days","__/__/__","Product Director"],
         ["Flow Efficiency","% of lead time that is active work","VSM Platform","__ %","__/__/__","Scrum Master"],
         ["Deployment Frequency","Deployments per team per week","CI/CD system","__ /week","__/__/__","Engineering VP"],
         ["Defect Escape Rate","% defects found post-release","ITSM / monitoring","__ %","__/__/__","QA Lead"],
         ["Feature Cycle Time","Avg days from commit to production","GitHub/GitLab","__ days","__/__/__","Engineering VP"],
         ["Team Productivity Index","Story points / sprint / team","JIRA/ADO","__ pts","__/__/__","Scrum Master"]],
        [2,2.5,2,1.5,1.5,1.5])
    divider(d)
    h1(d,"3. Target Setting by Option")
    tbl(d,["Metric","Baseline","Option A Target","Option B Target","Option C Target"],
        [["Lead Time","Org baseline","−25%","−55%","−75%"],
         ["Flow Efficiency","Org baseline","+20%","+50%","+75%"],
         ["Deployment Frequency","Org baseline","+25%","+50%","+100%"],
         ["Defect Escape Rate","Org baseline","−15%","−35%","−60%"],
         ["Feature Cycle Time","Org baseline","−20%","−50%","−70%"],
         ["Team Productivity","Org baseline","+20%","+50%","+75%"]],
        [2.5,2,2,2,2])
    divider(d)
    h1(d,"4. Monthly Tracking Table")
    tbl(d,["Metric","Baseline","Month 1","Month 2","Month 3","Month 6","Month 12","Target","Status"],
        [["Lead Time (days)","__","","","","","","",""],
         ["Flow Efficiency (%)","__","","","","","","",""],
         ["Deploy Frequency (/wk)","__","","","","","","",""],
         ["Defect Escape Rate (%)","__","","","","","","",""],
         ["Feature Cycle Time (d)","__","","","","","","",""],
         ["Productivity Index (pts)","__","","","","","","",""]],
        [2.5,1.2,1,1,1,1,1,1.2,1])
    divider(d)
    h1(d,"5. Financial Benefits Tracker")
    tbl(d,["Benefit Stream","Calculation Method","Plan ($K)","Actual ($K)","Variance","Notes"],
        [["Speed — time-to-market","Revenue per day × lead time saved","__","","",""],
         ["Productivity — FTE capacity","FTE cost × efficiency gain","__","","",""],
         ["Quality — defect cost avoided","Avg defect cost × escape rate reduction","__","","",""],
         ["Total Annual Benefit","Sum of above","__","","",""],
         ["Platform Investment","Licence + config + change mgmt","__","","",""],
         ["Net Annual Benefit","Total benefit − investment","__","","",""],
         ["Cumulative ROI","Net benefit / investment","__x","","",""]],
        [3,3,1.3,1.3,1.3,1.3])
    divider(d)
    h1(d,"6. Benefits RAG Status")
    tbl(d,["Metric","Status","Trend","Action Required"],
        [["Lead Time","  ","  ",""],
         ["Flow Efficiency","  ","  ",""],
         ["Deployment Frequency","  ","  ",""],
         ["Defect Escape Rate","  ","  ",""],
         ["Financial ROI","  ","  ",""]],
        [2.5,1.5,1.5,4])
    body(d,"RAG Key: Green = on/ahead of plan | Amber = within 10% of plan | Red = >10% behind plan",italic=True,color=DSTEEL)
    divider(d)
    h1(d,"7. US Bank Benchmark Reference")
    callout(d,"US Bank (Team Phoenix) — Option B implementation: Lead Time 42→8 days (−81%), "
              "Flow Efficiency 17.8%→61% (+243%), $3M investment, $8.4M/year benefit, "
              "4.2× ROI, 14-month payback, $31.2M 5-year NPV.")
    h2(d, "Tracked on the 3-perspective Outcome Dashboard")
    body(d, "Benefits are tracked continuously across three perspectives, computed from live data with per-chart inferences. " + M.OUTCOME_SOURCES)
    for p in M.OUTCOME_PERSPECTIVES:
        bul(d, f"{p['name']} — {p['blurb']} Metrics: " + ", ".join(p["metrics"]) + ".")
    h2(d, "ROI is read on the J-Curve (cost-only)")
    body(d, M.JCURVE["headline"] + " " + M.JCURVE["roi_formula"])
    for ph, desc in M.JCURVE["phases"]:
        bul(d, f"{ph}: {desc}")
    callout(d, "Ongoing cost is platform-aware and includes agent/token spend. " + M.JCURVE["exclusion"])
    h2(d, "Productivity economics")
    for f in M.PRODUCTIVITY["formulas"]:
        bul(d, f)
    d.save(os.path.join(OUT,"31-benefits-tracker-template.docx")); print("  ✓ 31")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 32 — Enterprise Scaling Playbook (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
def build_32():
    prs=new_prs()
    # Slide 1 — Cover
    sl=blank(prs); R(sl,0,0,13.33,7.5,fill=NAVY)
    T(sl,"AI-POWERED PDLC TRANSFORMATION",0.6,1.5,12,0.6,size=13,bold=True,color=LBLUE,align=PP_ALIGN.CENTER)
    T(sl,"Enterprise Scaling Playbook",0.6,2.2,12,0.9,size=36,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,"From Pilot to Enterprise-Wide Transformation",0.6,3.2,12,0.5,size=16,color=LBLUE,align=PP_ALIGN.CENTER)
    T(sl,"CONFIDENTIAL  |  March 2026",0.6,6.5,12,0.4,size=11,color=PALE,align=PP_ALIGN.CENTER)
    # Slide 2 — Scaling Philosophy
    sl=blank(prs); hdr(sl,"Scaling Philosophy","One offering. Three options. Enterprise-wide transformation at the right pace.")
    T(sl,"The AI-Powered PDLC Transformation consulting offering is designed to scale from a single pilot team to "
         "an enterprise-wide deployment — without a big-bang change programme. The platform's modular architecture "
         "and option-based model allow organisations to start where they are, prove value fast, and scale with confidence.",
      0.4,1.2,12.5,1.2,size=11,color=TEXT,wrap=True)
    R(sl,0.4,2.6,3.9,3.4,fill=GHOST)
    T(sl,"WAVE 1\nPilot",0.4,2.65,3.9,0.5,size=13,bold=True,color=OPT_A,align=PP_ALIGN.CENTER)
    T(sl,"1–2 teams\n1 product\n12 weeks\nOption A or B",0.4,3.2,3.9,1.5,size=10.5,color=TEXT,align=PP_ALIGN.CENTER)
    T(sl,"Prove: faster delivery, visible ROI",0.4,4.5,3.9,0.5,size=9,italic=True,color=OPT_A,align=PP_ALIGN.CENTER)
    R(sl,4.5,2.6,3.9,3.4,fill=RGBColor(0xEB,0xF4,0xFF))
    T(sl,"WAVE 2\nDivision Scale",4.5,2.65,3.9,0.5,size=13,bold=True,color=OPT_B,align=PP_ALIGN.CENTER)
    T(sl,"5–10 teams\n2–4 products\n6 months\nOption B standard",4.5,3.2,3.9,1.5,size=10.5,color=TEXT,align=PP_ALIGN.CENTER)
    T(sl,"Prove: consistent ROI at scale",4.5,4.5,3.9,0.5,size=9,italic=True,color=OPT_B,align=PP_ALIGN.CENTER)
    R(sl,8.6,2.6,4.3,3.4,fill=RGBColor(0xDB,0xEA,0xFE))
    T(sl,"WAVE 3\nEnterprise",8.6,2.65,4.3,0.5,size=13,bold=True,color=OPT_C,align=PP_ALIGN.CENTER)
    T(sl,"All teams\nAll products\n12 months\nOption B/C enterprise",8.6,3.2,4.3,1.5,size=10.5,color=TEXT,align=PP_ALIGN.CENTER)
    T(sl,"Prove: enterprise transformation",8.6,4.5,4.3,0.5,size=9,italic=True,color=OPT_C,align=PP_ALIGN.CENTER)
    T(sl,"→ Each wave requires a go/no-go gate based on benefits realisation from the prior wave.",
      0.4,6.3,12.5,0.5,size=10,italic=True,color=STEEL)
    # Slide 3 — Wave 1: Pilot Scaling Criteria
    sl=blank(prs); hdr(sl,"Wave 1 → Wave 2 Scale Criteria","Pilot success gates before division rollout")
    T(sl,"Scale from pilot to division only when ALL three gates pass:",0.4,1.2,12.5,0.5,size=12,bold=True,color=NAVY)
    gates=[("SPEED GATE","Lead time reduction >30% vs baseline","4.2×","US Bank pilot result"),
           ("PRODUCTIVITY GATE","Flow efficiency improvement >20%","61%","US Bank achieved"),
           ("ROI GATE","Net benefit >1.5× investment at 6 months","4.2× ROI","14-month payback")]
    for i,(g,desc,stat_val,note) in enumerate(gates):
        R(sl,0.4,2.0+i*1.5,12.5,1.3,fill=GHOST if i%2==0 else RGBColor(0xEB,0xF4,0xFF))
        T(sl,g,0.6,2.1+i*1.5,2.8,0.5,size=11,bold=True,color=NAVY)
        T(sl,desc,3.5,2.1+i*1.5,6.5,0.8,size=10.5,color=TEXT,wrap=True)
        R(sl,10.2,2.05+i*1.5,2.3,1.1,fill=BLUE)
        T(sl,stat_val,10.2,2.1+i*1.5,2.3,0.55,size=18,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
        T(sl,note,10.2,2.6+i*1.5,2.3,0.45,size=8,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,"If any gate fails: run an optimisation sprint before scaling. Do not accelerate past a failing gate.",
      0.4,6.7,12.5,0.4,size=10,italic=True,color=STEEL)
    # Slide 4 — Wave 2: Division Scaling Model
    sl=blank(prs); hdr(sl,"Wave 2: Division Scaling Model","Option B standard across 5–10 teams")
    T(sl,"DIVISION SCALE STRUCTURE",0.4,1.2,12.5,0.4,size=11,bold=True,color=NAVY)
    div_rows=[("Division CTO","AI Transformation Lead","Sets AI policy, owns gate governance"),
              ("Product Directors (2–4)","Product AI Champions","Gate approval owners per product"),
              ("Engineering VPs (2–4)","Engineering AI Leads","Technical gate approvers"),
              ("Scrum Masters (5–10)","Team Champions","Daily adoption, first-line support")]
    for i,(role,new_role,responsibility) in enumerate(div_rows):
        R(sl,0.4,1.7+i*1.1,12.5,0.95,fill=GHOST if i%2==0 else RGBColor(0xEB,0xF4,0xFF))
        T(sl,role,0.6,1.8+i*1.1,3,0.7,size=10.5,bold=True,color=NAVY)
        T(sl,new_role,3.7,1.8+i*1.1,3,0.7,size=10.5,color=OPT_B)
        T(sl,responsibility,6.8,1.8+i*1.1,6,0.7,size=10,color=TEXT,wrap=True)
    T(sl,"DIVISION SCALE COMMERCIAL",0.4,6.0,12.5,0.4,size=11,bold=True,color=NAVY)
    for i,(label,val) in enumerate([("Platform licences","5–10 team seats @ $X/seat/yr"),
                                     ("Change mgmt uplift","20% of total investment"),
                                     ("Expected ROI","4–6× within 18 months")]):
        T(sl,f"• {label}: {val}",0.6,6.45+i*0.35,12,0.35,size=10.5,color=TEXT)
    # Slide 5 — Wave 3: Enterprise Architecture
    sl=blank(prs); hdr(sl,"Wave 3: Enterprise Architecture","Option B/C enterprise-wide deployment")
    for i,(title,content,bg) in enumerate([
        ("ENTERPRISE PLATFORM\nARCHITECTURE",
         "• Centralised STUMP instance\n• Multi-tenant: org → division → team hierarchy\n• Federated governance: enterprise policy + local execution\n• Single SSO, RBAC, audit log",
         OPT_C),
        ("ENTERPRISE AI\nOPERATING MODEL",
         "• AI Centre of Excellence owns platform + methodology\n• Division AI Leads execute\n• Team AI Champions sustain\n• Board AI Committee sets policy (Option C)",
         OPT_B),
        ("ENTERPRISE\nROI MODEL",
         "• Option B enterprise: 4–6× ROI, $5–15M investment\n• Option C enterprise: 8–12× ROI, $15–30M investment\n• Payback: 12–18 months (Option B), 18–30 months (Option C)\n• 5-year NPV: $25–75M depending on scale",
         STEEL)]):
        R(sl,0.4+i*4.3,1.2,4.1,5.9,fill=bg)
        T(sl,title,0.5+i*4.3,1.35,4,0.7,size=12,bold=True,color=WHITE,align=PP_ALIGN.CENTER,wrap=True)
        T(sl,content,0.5+i*4.3,2.2,4,4.6,size=10,color=WHITE,wrap=True)
    # Slide 6 — Scaling Risks & Mitigations
    sl=blank(prs); hdr(sl,"Scaling Risks & Mitigations","Common failure modes in enterprise AI transformation")
    risks=[("Scaling before value proven","Premature scaling","Run benefits gate before each wave"),
           ("Change management under-resourced","Adoption collapse","Budget 20–30% of investment for change"),
           ("Governance not scaled","Ungoverned AI autonomy","Stand up governance tier before scaling"),
           ("Configuration debt accumulates","Platform instability","Quarterly configuration review mandatory"),
           ("Champions programme lapses","Adoption regression","Champions programme is permanent, not one-time")]
    T(sl,"Risk",0.4,1.1,3,0.35,size=10.5,bold=True,color=NAVY)
    T(sl,"Type",3.5,1.1,3,0.35,size=10.5,bold=True,color=NAVY)
    T(sl,"Mitigation",6.6,1.1,6.3,0.35,size=10.5,bold=True,color=NAVY)
    for i,(risk,rtype,mit) in enumerate(risks):
        R(sl,0.4,1.5+i*1.0,12.5,0.9,fill=GHOST if i%2==0 else RGBColor(0xEB,0xF4,0xFF))
        T(sl,risk,0.6,1.6+i*1.0,2.8,0.7,size=10,color=TEXT,wrap=True)
        T(sl,rtype,3.5,1.6+i*1.0,2.9,0.7,size=10,color=AMBER,bold=True,wrap=True)
        T(sl,mit,6.6,1.6+i*1.0,6.2,0.7,size=10,color=TEXT,wrap=True)
    prs.save(os.path.join(OUT,"32-enterprise-scaling-playbook.pptx")); print("  ✓ 32")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 33 — ELT Executive Dashboard Briefing (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
def build_33():
    prs=new_prs()
    # Slide 1 — Cover
    sl=blank(prs); R(sl,0,0,13.33,7.5,fill=NAVY)
    T(sl,"AI-POWERED PDLC TRANSFORMATION",0.6,1.5,12,0.6,size=13,bold=True,color=LBLUE,align=PP_ALIGN.CENTER)
    T(sl,"ELT Executive Dashboard Briefing",0.6,2.2,12,0.9,size=34,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,"Transformation Status | Benefits Realisation | Strategic Decisions",0.6,3.2,12,0.5,size=15,color=LBLUE,align=PP_ALIGN.CENTER)
    T(sl,"MONTHLY EXECUTIVE BRIEFING  |  March 2026",0.6,6.5,12,0.4,size=11,color=PALE,align=PP_ALIGN.CENTER)
    # Slide 2 — Transformation Scorecard
    sl=blank(prs); hdr(sl,"Transformation Scorecard","Overall programme status at a glance")
    T(sl,"CURRENT OPTION SELECTED:",0.4,1.15,5,0.4,size=10.5,bold=True,color=NAVY)
    T(sl,"Option B — AI Agents + Human Gates ★",5.5,1.15,7,0.4,size=10.5,bold=True,color=OPT_B)
    for i,(val,lbl,bg) in enumerate([("−34%","Lead Time vs Baseline",NAVY),
                                       ("+41%","Flow Efficiency",OPT_B),
                                       ("+38%","Team Productivity",STEEL),
                                       ("3.1×","ROI vs Plan (4–6× target)",GREEN)]):
        stat(sl,0.4+i*3.2,1.65,3.0,1.6,val,lbl,bg=bg)
    T(sl,"TRANSFORMATION PHASE STATUS",0.4,3.4,12.5,0.4,size=11,bold=True,color=NAVY)
    for i,(phase,status,detail) in enumerate([
        ("Phase 1 — DIAGNOSE","COMPLETE ✓","VSM mapped, bottlenecks agreed, findings accepted"),
        ("Phase 2 — DESIGN","COMPLETE ✓","Option B selected, business case approved by CFO"),
        ("Phase 3 — DELIVER","IN PROGRESS →","Week 8 of 16 — platform live, adoption at 62%")]):
        R(sl,0.4,3.85+i*0.95,12.5,0.85,fill=GHOST if i%2==0 else RGBColor(0xEB,0xF4,0xFF))
        T(sl,phase,0.6,3.95+i*0.95,3.5,0.65,size=10.5,bold=True,color=NAVY)
        T(sl,status,4.2,3.95+i*0.95,2.5,0.65,size=10.5,bold=True,color=GREEN if "COMPLETE" in status else OPT_B)
        T(sl,detail,6.9,3.95+i*0.95,5.8,0.65,size=10,color=TEXT,wrap=True)
    # Slide 3 — Benefits Dashboard
    sl=blank(prs); hdr(sl,"Benefits Dashboard","Speed, Productivity & Quality ROI — Month 8")
    T(sl,"SPEED BENEFITS",0.4,1.2,4,0.4,size=11,bold=True,color=NAVY)
    T(sl,"PRODUCTIVITY BENEFITS",4.5,1.2,4,0.4,size=11,bold=True,color=NAVY)
    T(sl,"QUALITY BENEFITS",8.9,1.2,4,0.4,size=11,bold=True,color=NAVY)
    for i,(val,lbl,x,bg) in enumerate([
        ("28d → 18d","Lead Time",0.4,NAVY),
        ("21%","Flow Eff. Gain",0.4,STEEL),
        ("+2.1×","Deploy Freq.",0.4,OPT_B),
        ("+31%","Productivity",4.5,OPT_B),
        ("+28%","Story Throughput",4.5,NAVY),
        ("62%","Active Users",4.5,STEEL),
        ("−22%","Defect Escape",8.9,OPT_B),
        ("+18%","Test Coverage",8.9,NAVY),
        ("−$1.4M","Defect Cost YTD",8.9,STEEL)]):
        col_i=i%3; row_i=i//3
        bx=x+col_i*0; by=1.7+row_i*1.2
        if col_i==0: bx=0.4
        elif col_i==1: bx=4.5
        else: bx=8.9
        R(sl,bx,by,3.9,1.0,fill=bg)
        T(sl,val,bx,by+0.05,3.9,0.55,size=18,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
        T(sl,lbl,bx,by+0.58,3.9,0.35,size=9,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,"FINANCIAL SUMMARY",0.4,5.3,12.5,0.4,size=11,bold=True,color=NAVY)
    for i,(label,val) in enumerate([("Investment to date","$1.1M of $1.6M total"),
                                     ("Benefits realised YTD","$2.3M (139% of plan)"),
                                     ("Annualised ROI run-rate","4.8× (plan: 4–6×)"),
                                     ("Forecast 5-year NPV","$28.4M (plan: $25–35M)")]):
        T(sl,f"• {label}: {val}",0.6+6.5*(i//2),5.75+(i%2)*0.45,6,0.4,size=10.5,color=TEXT)
    # Slide 4 — Gate Governance Status
    sl=blank(prs); hdr(sl,"Gate Governance Status","AI agent gate performance — Option B programme")
    T(sl,"GATE PERFORMANCE (LAST 30 DAYS)",0.4,1.15,12.5,0.4,size=11,bold=True,color=NAVY)
    for i,(gate,approvals,overrides,sla,trend) in enumerate([
        ("G1 — VSM Complete","12 of 12","0","100% within 24h","Green"),
        ("G2 — Options Ready","4 of 4","1","75% within 48h","Amber"),
        ("G3 — Config Complete","3 of 3","0","100% within 24h","Green"),
        ("G4 — Go Live","1 of 1","0","100% within 24h","Green")]):
        R(sl,0.4,1.6+i*1.1,12.5,0.95,fill=GHOST if i%2==0 else RGBColor(0xEB,0xF4,0xFF))
        T(sl,gate,0.6,1.7+i*1.1,3,0.75,size=10.5,bold=True,color=NAVY)
        T(sl,approvals,3.7,1.7+i*1.1,2.5,0.75,size=10.5,color=GREEN,align=PP_ALIGN.CENTER)
        T(sl,overrides,6.3,1.7+i*1.1,1.8,0.75,size=10.5,color=AMBER if overrides!="0" else TEXT,align=PP_ALIGN.CENTER)
        T(sl,sla,8.2,1.7+i*1.1,2.5,0.75,size=10.5,color=AMBER if "75%" in sla else TEXT)
        R(sl,11.0,1.75+i*1.1,1.5,0.65,fill=GREEN if trend=="Green" else AMBER)
        T(sl,trend,11.0,1.8+i*1.1,1.5,0.5,size=9,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,"Gate G2 override: CFO requested revised sensitivity analysis before approving Option B business case. "
         "Completed within 48h. No impact to programme timeline.",
      0.4,6.1,12.5,0.65,size=10,italic=True,color=STEEL,wrap=True)
    # Slide 5 — Decisions Required
    sl=blank(prs); hdr(sl,"Decisions Required","Items requiring Executive Steering Committee action")
    decisions=[("Option Upgrade Assessment","Review readiness to move from Option B to Option C for the Digital Lending product group","CFO + CTO","30 April 2026","High"),
               ("Wave 2 Scale Approval","Approve division-wide rollout to Commercial Banking (5 additional teams)","Executive Sponsor","15 April 2026","High"),
               ("Champions Programme Budget","Approve $180K annual budget for ongoing champions programme","CFO","15 April 2026","Medium")]
    for i,(dec,detail,owner,deadline,priority) in enumerate(decisions):
        R(sl,0.4,1.2+i*1.8,12.5,1.65,fill=GHOST if i%2==0 else RGBColor(0xEB,0xF4,0xFF))
        T(sl,f"DECISION {i+1}: {dec}",0.6,1.3+i*1.8,8.5,0.45,size=11,bold=True,color=NAVY)
        T(sl,detail,0.6,1.75+i*1.8,8.5,0.7,size=10,color=TEXT,wrap=True)
        R(sl,9.3,1.3+i*1.8,3.3,1.4,fill=OPT_B if priority=="High" else STEEL)
        T(sl,f"Owner: {owner}",9.4,1.38+i*1.8,3.1,0.45,size=9,bold=True,color=WHITE)
        T(sl,f"By: {deadline}",9.4,1.75+i*1.8,3.1,0.35,size=9,color=PALE)
    sl = blank(prs)
    hdr(sl, "Outcome Dashboard — Executive View", "Three monitoring perspectives, always-on")
    PVW=(13.33-0.4*2-0.12*2)/3
    for i,p in enumerate(M.OUTCOME_PERSPECTIVES):
        x=0.4+i*(PVW+0.12); col=[NAVY,BLUE,STEEL][i]
        R(sl,x,1.3,PVW,0.6,fill=col); T(sl,p["name"],x+0.1,1.36,PVW-0.2,0.5,size=13,bold=True,color=WHITE)
        R(sl,x,1.9,PVW,3.5,fill=GHOST); T(sl,p["blurb"],x+0.1,1.98,PVW-0.2,0.7,size=10,italic=True,color=STEEL)
        for j,mtr in enumerate(p["metrics"]):
            T(sl,f"• {mtr}",x+0.12,2.66+j*0.34,PVW-0.24,0.32,size=9.5,color=TEXT)
    R(sl,0,5.6,13.33,1.0,fill=NAVY)
    T(sl,"ROI is read on the J-Curve (cost-only): investment → tuition-cost dip → breakeven → compounding savings. "+M.JCURVE["exclusion"],0.5,5.7,12.4,0.85,size=11,color=WHITE)
    prs.save(os.path.join(OUT,"33-elt-executive-dashboard-briefing.pptx")); print("  ✓ 33")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 34 — Annual ROI Review Deck (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
def build_34():
    prs=new_prs()
    # Slide 1 — Cover
    sl=blank(prs); R(sl,0,0,13.33,7.5,fill=NAVY)
    T(sl,"AI-POWERED PDLC TRANSFORMATION",0.6,1.5,12,0.6,size=13,bold=True,color=LBLUE,align=PP_ALIGN.CENTER)
    T(sl,"Annual ROI Review",0.6,2.2,12,0.9,size=38,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    T(sl,"Year 1 Benefits Realisation & Year 2 Investment Decision",0.6,3.2,12,0.5,size=15,color=LBLUE,align=PP_ALIGN.CENTER)
    T(sl,"ANNUAL REVIEW  |  March 2026",0.6,6.5,12,0.4,size=11,color=PALE,align=PP_ALIGN.CENTER)
    # Slide 2 — Year 1 at a Glance
    sl=blank(prs); hdr(sl,"Year 1 at a Glance","Transformation progress and financial outcomes")
    T(sl,"OPTION B — AI AGENTS + HUMAN GATES  |  Full Year 1",0.4,1.15,12.5,0.4,size=11,bold=True,color=OPT_B)
    for i,(val,lbl,bg) in enumerate([("−48%","Lead Time vs Baseline",NAVY),
                                       ("+52%","Flow Efficiency",OPT_B),
                                       ("+47%","Team Productivity",STEEL),
                                       ("4.8×","Annual ROI Achieved",GREEN)]):
        stat(sl,0.4+i*3.2,1.65,3.0,1.6,val,lbl,bg=bg)
    T(sl,"YEAR 1 FINANCIAL SUMMARY",0.4,3.45,12.5,0.4,size=11,bold=True,color=NAVY)
    fin_rows=[("Total Investment Year 1","$1.6M","$1.6M","On budget"),
              ("Total Benefits Realised","$7.7M","$6.4–9.6M","Above plan midpoint"),
              ("Net Benefit Year 1","$6.1M","$4.8–8.0M","Above plan"),
              ("ROI Year 1","4.8×","4–6× target","Within range"),
              ("Payback Period","14 months","12–18 months","On track"),
              ("5-Year NPV (projected)","$31.2M","$25–40M","On track")]
    for i,(metric,actual,plan,status) in enumerate(fin_rows):
        R(sl,0.4,3.9+i*0.52,12.5,0.48,fill=GHOST if i%2==0 else WHITE)
        T(sl,metric,0.6,3.95+i*0.52,4,0.4,size=10,color=TEXT)
        T(sl,actual,4.7,3.95+i*0.52,2.5,0.4,size=10,bold=True,color=OPT_B,align=PP_ALIGN.CENTER)
        T(sl,plan,7.3,3.95+i*0.52,3.0,0.4,size=10,color=STEEL,align=PP_ALIGN.CENTER)
        T(sl,status,10.5,3.95+i*0.52,2.4,0.4,size=10,color=GREEN if "Above" in status or "On" in status else AMBER)
    # Slide 3 — Benefits Deep Dive
    sl=blank(prs); hdr(sl,"Year 1 Benefits Deep Dive","Speed, Productivity & Quality — actual vs plan")
    cols=["Benefit Stream","Baseline","Year 1 Actual","Year 1 Plan","vs Plan","Year 2 Target"]
    rows=[["Lead Time","42 days","22 days","25 days","+3d better","8 days"],
          ["Flow Efficiency","17.8%","52%","45%","+7pp better","65%"],
          ["Deploy Frequency","1.2/wk","2.8/wk","2.5/wk","+0.3 better","4/wk"],
          ["Defect Escape Rate","22%","14%","15%","−1pp better","8%"],
          ["Team Productivity","100 baseline","147 index","140 index","+7 better","175 index"],
          ["$M Benefits Realised","—","$7.7M","$6.4M","+$1.3M","$11.2M"]]
    tbl_y=1.2
    t_sl=prs.slides[-1]
    # Use a simple text table representation in pptx
    T(sl,cols[0],0.4,tbl_y,2.5,0.4,size=9.5,bold=True,color=WHITE); R(sl,0.4,tbl_y,2.5,0.4,fill=NAVY)
    T(sl,cols[1],2.95,tbl_y,1.5,0.4,size=9.5,bold=True,color=WHITE); R(sl,2.95,tbl_y,1.5,0.4,fill=NAVY)
    T(sl,cols[2],4.5,tbl_y,2,0.4,size=9.5,bold=True,color=WHITE); R(sl,4.5,tbl_y,2,0.4,fill=NAVY)
    T(sl,cols[3],6.55,tbl_y,1.8,0.4,size=9.5,bold=True,color=WHITE); R(sl,6.55,tbl_y,1.8,0.4,fill=NAVY)
    T(sl,cols[4],8.4,tbl_y,1.8,0.4,size=9.5,bold=True,color=WHITE); R(sl,8.4,tbl_y,1.8,0.4,fill=NAVY)
    T(sl,cols[5],10.25,tbl_y,2.7,0.4,size=9.5,bold=True,color=WHITE); R(sl,10.25,tbl_y,2.7,0.4,fill=NAVY)
    for i,row in enumerate(rows):
        bg=GHOST if i%2==0 else WHITE
        R(sl,0.4,1.65+i*0.78,12.55,0.73,fill=bg)
        T(sl,row[0],0.4,1.7+i*0.78,2.5,0.6,size=10,bold=True,color=NAVY)
        T(sl,row[1],2.95,1.7+i*0.78,1.5,0.6,size=10,color=STEEL,align=PP_ALIGN.CENTER)
        T(sl,row[2],4.5,1.7+i*0.78,2.0,0.6,size=10,bold=True,color=OPT_B,align=PP_ALIGN.CENTER)
        T(sl,row[3],6.55,1.7+i*0.78,1.8,0.6,size=10,color=TEXT,align=PP_ALIGN.CENTER)
        T(sl,row[4],8.4,1.7+i*0.78,1.8,0.6,size=10,bold=True,color=GREEN,align=PP_ALIGN.CENTER)
        T(sl,row[5],10.25,1.7+i*0.78,2.7,0.6,size=10,bold=True,color=OPT_C,align=PP_ALIGN.CENTER)
    # Slide 4 — Year 2 Investment Options
    sl=blank(prs); hdr(sl,"Year 2 Investment Decision","Three paths forward — choose your ambition level")
    T(sl,"Based on Year 1 results (4.8× ROI, 14-month payback), three Year 2 investment paths are recommended:",
      0.4,1.15,12.5,0.5,size=11,color=TEXT,wrap=True)
    paths=[("PATH A\nConsolidate & Optimise",OPT_A,
            "• Stay at Option B\n• Extend to 2 additional divisions\n• Deepen gate governance\n• Investment: +$600K\n• Expected ROI: 5–6×\n• Net new benefit: +$3.2M/yr",
            "Lowest risk\nHighest certainty"),
           ("PATH B\nScale & Upgrade ★",OPT_B,
            "• Migrate lead product to Option C\n• Scale Option B to all divisions\n• Establish AI Centre of Excellence\n• Investment: +$2.2M\n• Expected ROI: 6–8×\n• Net new benefit: +$8.5M/yr",
            "Recommended\nBalanced risk/reward"),
           ("PATH C\nFull Transformation",OPT_C,
            "• Migrate all products to Option C\n• Full agentic PDLC enterprise-wide\n• Board AI governance established\n• Investment: +$5.5M\n• Expected ROI: 8–12×\n• Net new benefit: +$18M/yr",
            "Highest reward\nHighest change management")]
    for i,(title,col,content,tag) in enumerate(paths):
        R(sl,0.4+i*4.3,1.75,4.1,5.35,fill=col)
        T(sl,title,0.5+i*4.3,1.88,4,0.65,size=13,bold=True,color=WHITE,align=PP_ALIGN.CENTER,wrap=True)
        T(sl,content,0.5+i*4.3,2.65,4,3.8,size=10,color=WHITE,wrap=True)
        R(sl,0.4+i*4.3,6.65,4.1,0.55,fill=RGBColor(0x1E,0x29,0x3B))
        T(sl,tag,0.5+i*4.3,6.7,4,0.45,size=9,color=PALE,italic=True,align=PP_ALIGN.CENTER,wrap=True)
    # Slide 5 — Recommendation & Next Steps
    sl=blank(prs); hdr(sl,"Recommendation & Next Steps","Year 2 investment recommendation")
    R(sl,0.4,1.2,12.5,1.8,fill=RGBColor(0xEB,0xF4,0xFF))
    T(sl,"RECOMMENDED: PATH B — Scale & Upgrade",0.6,1.3,12,0.55,size=16,bold=True,color=OPT_B,align=PP_ALIGN.CENTER)
    T(sl,"Year 1 results prove the model. Year 2 should simultaneously scale the proven Option B model enterprise-wide "
         "AND migrate the highest-value product to Option C — building the data and governance foundation for full "
         "agentic transformation in Year 3.",0.6,1.85,12,0.9,size=11,color=NAVY,wrap=True,align=PP_ALIGN.CENTER)
    T(sl,"NEXT STEPS",0.4,3.15,12.5,0.4,size=11,bold=True,color=NAVY)
    steps=[("Week 1","CFO approves Path B Year 2 budget ($2.2M)","CFO"),
           ("Week 2","CTO confirms Option C migration candidate","CTO"),
           ("Week 3","Engagement team scopes Wave 2 rollout plan","Engagement Lead"),
           ("Week 4","AI Centre of Excellence charter drafted","CTO + HR"),
           ("Week 6","Wave 2 kick-off with all division product directors","Executive Sponsor")]
    for i,(when,action,owner) in enumerate(steps):
        R(sl,0.4,3.6+i*0.68,12.5,0.62,fill=GHOST if i%2==0 else WHITE)
        R(sl,0.4,3.65+i*0.68,1.3,0.52,fill=OPT_B)
        T(sl,when,0.4,3.68+i*0.68,1.3,0.42,size=10,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
        T(sl,action,1.8,3.68+i*0.68,8.5,0.42,size=10,color=TEXT,wrap=True)
        T(sl,owner,10.5,3.68+i*0.68,2.4,0.42,size=10,bold=True,color=OPT_B,align=PP_ALIGN.CENTER)
    sl = blank(prs)
    hdr(sl, "Annual ROI on the J-Curve", "12 months on — investment, breakeven and compounding savings (cost-only)")
    for i,(ph,desc) in enumerate(M.JCURVE["phases"]):
        x=0.4+i*3.18; col=[STEEL,RGBColor(0x64,0x74,0x8B),BLUE,NAVY][i]
        R(sl,x,1.3,3.0,0.55,fill=col); T(sl,ph,x+0.1,1.35,2.8,0.46,size=11.5,bold=True,color=WHITE)
        R(sl,x,1.85,3.0,2.1,fill=GHOST); T(sl,desc,x+0.1,1.93,2.8,1.95,size=9.5,color=TEXT)
    R(sl,0,4.25,13.33,0.95,fill=PALE)
    T(sl,M.JCURVE["roi_formula"]+"  "+M.JCURVE["ongoing_note"],0.5,4.33,12.4,0.82,size=10,color=TEXT)
    R(sl,0,5.35,13.33,0.55,fill=NAVY)
    T(sl,"At portfolio scale the shared platform cost is fixed while savings scale with every pod — ROI compounds year over year.",0.5,5.42,12.4,0.45,size=11.5,bold=True,color=WHITE)
    prs.save(os.path.join(OUT,"34-annual-roi-review-deck.pptx")); print("  ✓ 34")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 35 — Competitive Differentiation Briefing
# ═══════════════════════════════════════════════════════════════════════════════
def build_35():
    d=new_doc()
    cover(d,"AI-Powered PDLC Transformation\nCompetitive Differentiation Briefing",
          "Why Our Three-Option Offering Wins — Market Positioning & Battlecard","Doc-35")
    h1(d,"1. Market Context")
    body(d,"The enterprise AI transformation market is crowded with point solutions — AI coding tools, agile "
          "analytics platforms, and DevOps intelligence products. None offers what AI-Powered PDLC Transformation "
          "delivers: a structured consulting methodology with three clearly differentiated transformation options, "
          "accelerated end-to-end by the STUMP.")
    callout(d,"Our differentiation: we don't sell software — we sell transformation outcomes. "
              "The platform makes our consulting 5× faster and measurably more accurate.")
    divider(d)
    h1(d,"2. Competitive Landscape")
    tbl(d,["Competitor Category","Examples","What They Offer","What They Don't Offer"],
        [["AI DevOps platforms","LinearB, Swarmia, Waydev","Engineering metrics dashboard","Consulting methodology, transformation options, business case"],
         ["VSM tools","Tasktop (Planview), ConnectALL","Value stream visualisation","AI agents, transformation options, ROI methodology"],
         ["Agile coaching platforms","Scaled Agile, Agility Health","Agile maturity assessments","AI autonomy levels, PDLC transformation offering"],
         ["Big 4 consulting","McKinsey QuantumBlack, Accenture SynOps","AI transformation consulting","Consistent platform, repeatable delivery, transparent pricing"],
         ["AI coding tools","GitHub Copilot, Cursor, Devin","Developer productivity","End-to-end PDLC transformation, VSM, business case methodology"]],
        [2.5,2.5,3,3])
    divider(d)
    h1(d,"3. Our Unique Differentiation")
    tbl(d,["Differentiator","Our Offering","Best Alternative","Advantage"],
        [["Structured methodology","3-phase Diagnose/Design/Deliver","Ad hoc consulting","Repeatable, scalable, certifiable"],
         ["Three AI options","A/B/C with clear ROI/risk profile","One-size-fits-all","Client chooses right risk level"],
         ["Platform acceleration","STUMP: 5× faster","Manual delivery","Speed + margin advantage"],
         ["Business case rigour","Bottleneck-to-ROI model per option","Generic ROI estimates","CFO-grade financial models"],
         ["Proof points","US Bank: 4.2× ROI, 14-month payback","Case study library","Live reference, auditable"],
         ["Human oversight model","Explicit in/on/above the loop","Implied or undefined","Trust and governance clarity"],
         ["Benefits tracking","Built-in platform benefits dashboard","Separate analytics tool","Accountability built in"]],
        [2.5,2.5,2.5,2.5])
    divider(d)
    h1(d,"4. Battlecard: Key Objections & Responses")
    tbl(d,["Objection","Root Concern","Our Response","Proof Point"],
        [["'We already use GitHub Copilot'","Point solution vs methodology","Copilot improves coding; we transform the end-to-end PDLC — 10% of the value lives in coding","US Bank: 80% of lead time reduction was in non-coding steps"],
         ["'McKinsey is doing our AI strategy'","Established relationship","Strategy is Phase 2; we deliver Phases 1–3 with a platform — strategy without execution is a deck","Our clients implement in 12 weeks; strategy engagements average 18 months"],
         ["'We'll build this ourselves'","Build vs buy","Building a VSM platform + AI agents takes 18–24 months and $3–5M — before any benefit","Option B ROI: 4–6× in 12 months; build cost equivalent to 5 years of licence fees"],
         ["'AI isn't ready for autonomous PDLC'","Risk concern","That's exactly why we offer Option A and B first — prove value before committing to Option C","90% of clients start at Option A/B; 60% upgrade to higher option within 18 months"],
         ["'ROI is hard to measure'","Accountability fear","Benefits are pre-defined, baselined, and tracked automatically by the platform — not a consulting estimate","Benefits dashboard is client-owned; no vendor manipulation of numbers"]],
        [2.5,2,3.5,3])
    divider(d)
    h1(d,"5. Win Themes by Buyer Type")
    tbl(d,["Buyer","Primary Win Theme","Key Message","Proof Metric"],
        [["CEO / COO","Strategic transformation","AI is reshaping PDLC — the question is how fast you move","Competitors deploying Option C gaining 75% speed advantage"],
         ["CFO","ROI clarity and accountability","Three options, three clear business cases, platform-tracked benefits","4.2× ROI, 14-month payback (auditable)"],
         ["CTO / VP Engineering","Technical credibility","Platform integrates with your existing stack — no rip-and-replace","Option B live in 12 weeks on JIRA + GitHub + Jenkins"],
         ["CISO / Risk","Governance and oversight","Explicit human oversight model at every AI autonomy level","SOC 2 Type II, immutable audit log, override capability always on"],
         ["Head of Product","Outcome focus","Faster features to market — without burning your team","Lead time −55% (Option B); feature throughput +50%"]],
        [2,2.5,3.5,2.5])
    divider(d)
    h1(d,"6. Pricing Positioning")
    tbl(d,["Option","Investment Range","vs Best Alternative","Value Multiple"],
        [["Option A — AI-Augmented","$350–600K","$800K+ for equivalent consulting","2× better value"],
         ["Option B — AI Agents + Gates ★","$1.2–2M","$3–5M for Big 4 equivalent","2.5× better value"],
         ["Option C — Fully Agentic","$3–5M","Not available elsewhere","Unique to market"]],
        [2.5,2.5,3.5,2])
    callout(d,"Pricing anchor: always lead with ROI, not licence cost. $1.6M investment generating $7.7M "
              "Year 1 benefit is not a cost conversation — it is a return on strategic investment.")
    d.save(os.path.join(OUT,"35-competitive-differentiation-briefing.docx")); print("  ✓ 35")

# ═══════════════════════════════════════════════════════════════════════════════
# Doc 00 — MASTER INDEX
# ═══════════════════════════════════════════════════════════════════════════════
def build_index():
    d=new_doc()
    p=d.add_paragraph(); p.paragraph_format.space_before=DPt(40)
    r=p.add_run("AI-POWERED PDLC TRANSFORMATION"); sf(r,14,bold=True,color=DBLUE)
    p2=d.add_paragraph()
    r2=p2.add_run("Complete GTM Pack — Master Index"); sf(r2,24,bold=True,color=DNAVY)
    d.add_paragraph()
    callout(d,"Three-set GTM Pack: Set 1 (CXO & Demand Gen), Set 2 (Pilot Engagement), Set 3 (Scale Implementation). "
              "All documents aligned to the Diagnose → Design → Deliver methodology with Options A, B, C.")
    d.add_page_break()
    h1(d,"SET 1 — CXO & Demand Generation Pack")
    body(d,"Purpose: Generate executive awareness, create demand, and qualify opportunities at the CXO level.",italic=True)
    tbl(d,["Doc","File","Purpose","Audience","Format"],
        [["01","01-cxo-pitch-deck-v2.pptx","15-slide offering-centric CXO pitch","C-Suite","PPTX"],
         ["01b","01b-offering-slide-v2.pptx","One-slide offering summary","CXO / conference","PPTX"],
         ["02","02-cxo-question-bank.docx","41 discovery questions across 3 phases","Sales / Consulting","DOCX"],
         ["03","03-service-brief.docx","2-page offering overview","CXO / ELT","DOCX"],
         ["04","04-whitepaper.docx","Thought leadership: PDLC AI transformation","CXO / VP","DOCX"],
         ["05","05-roi-calculator.docx","3-option ROI calculator with scenarios","CFO / Finance","DOCX"],
         ["06","06-benchmark-report.docx","Industry benchmarks across 3 AI options","VP Engineering","DOCX"],
         ["07","07-case-study-usbank.docx","US Bank 4.2× ROI case study","All buyers","DOCX"],
         ["08","08-commercial-model.docx","3-option pricing & commercial structures","CFO / Procurement","DOCX"],
         ["09","09-engagement-model.docx","Delivery model & team structure","VP / Director","DOCX"],
         ["10","10-demo-script.docx","Platform demo script (offering-led)","Sales / Consulting","DOCX"]],
        [0.5,3.2,3.5,2,0.8])
    d.add_page_break()
    h1(d,"SET 2 — Pilot Engagement Pack")
    body(d,"Purpose: Run a structured 12-week pilot engagement from discovery through findings readout.",italic=True)
    tbl(d,["Doc","File","Purpose","Audience","Format"],
        [["11","11-pilot-proposal-template.docx","Pilot proposal with 3-option scoping","Client Exec","DOCX"],
         ["12","12-project-charter.docx","Engagement charter: scope, governance, success","Steering Comm.","DOCX"],
         ["13","13-pilot-delivery-runbook.docx","Week-by-week delivery guide","Delivery Team","DOCX"],
         ["14","14-raci-matrix.docx","Responsibilities across 3 phases & options","All stakeholders","DOCX"],
         ["15","15-pilot-findings-readout.pptx","Findings & options presentation deck","Executive Sponsor","PPTX"],
         ["16","16-discovery-questionnaire.docx","Structured discovery: speed/productivity/quality","Consulting Lead","DOCX"],
         ["17","17-kickoff-meeting-guide.docx","Day-1 kickoff agenda & facilitation guide","Programme Lead","DOCX"],
         ["18","18-ai-evidence-protocol.docx","Data collection for AI transformation readiness","Analytics Lead","DOCX"],
         ["19","19-risk-register.docx","Risks across 3 transformation options","PM / Risk Lead","DOCX"],
         ["20","20-pilot-success-scorecard.docx","KPI scorecard for pilot evaluation","Steering Comm.","DOCX"],
         ["21","21-pilot-to-scale-framework.docx","Decision framework: pilot → scale","Executive Sponsor","DOCX"],
         ["22","22-scale-proposal-deck.pptx","Scale investment proposal deck","C-Suite","PPTX"]],
        [0.5,3.2,3.5,2,0.8])
    d.add_page_break()
    h1(d,"SET 3 — Scale Implementation Pack")
    body(d,"Purpose: Govern, configure, train, and sustain enterprise-wide AI PDLC transformation.",italic=True)
    tbl(d,["Doc","File","Purpose","Audience","Format"],
        [["23","23-platform-methodology-guide.docx","3-phase consulting methodology","Delivery Team","DOCX"],
         ["24","24-governance-model.docx","Governance tiers & decision rights by option","Exec / Programme","DOCX"],
         ["25","25-change-management-plan.docx","People & adoption strategy by option","HR / Change Lead","DOCX"],
         ["26","26-platform-configuration-playbook.docx","Platform setup guide by option","Platform Engineer","DOCX"],
         ["27","27-integration-architecture-guide.docx","System connectivity & security","CTO / IT Director","DOCX"],
         ["28","28-scale-training-curriculum.docx","Role-based training by option","L&D / Champions","DOCX"],
         ["29","29-adoption-playbook.docx","Sustained adoption programme","Champions / PM","DOCX"],
         ["30","30-qa-framework.docx","Quality assurance across delivery & AI","QA Lead","DOCX"],
         ["31","31-benefits-tracker-template.docx","Benefits measurement template by option","Finance / Exec","DOCX"],
         ["32","32-enterprise-scaling-playbook.pptx","3-wave enterprise scaling model","Executive Sponsor","PPTX"],
         ["33","33-elt-executive-dashboard-briefing.pptx","Monthly ELT dashboard deck","C-Suite","PPTX"],
         ["34","34-annual-roi-review-deck.pptx","Annual ROI review & Year 2 decision","C-Suite / CFO","PPTX"],
         ["35","35-competitive-differentiation-briefing.docx","Battlecard & win themes","Sales / Consulting","DOCX"]],
        [0.5,3.5,3.2,2,0.8])
    d.add_page_break()
    h1(d,"The Consulting Offering in One Paragraph")
    callout(d,"AI-Powered PDLC Transformation is a consulting offering that diagnoses your current-state product "
              "development process using Value Stream Mapping, identifies where speed, productivity, and quality are "
              "constrained, and then designs and implements the right level of AI transformation — from AI-augmented "
              "tools (Option A) to AI agents with human gates (Option B) to fully autonomous AI operations (Option C). "
              "Every phase is delivered faster, more accurately, and at lower cost because the STUMP "
              "automates what would otherwise take months of manual analysis. Clients like US Bank achieved 4.2× ROI "
              "and a 42-day to 8-day lead time reduction within 14 months. The platform is not the product — "
              "the transformation is.",fill="EFF6FF")
    h2(d, "2026 refresh — what changed across the pack")
    body(d, "All three sets are aligned to the refreshed PDLC VSM platform:")
    bul(d, "Options A/B/C are now mapped onto the L1–L5 maturity ladder (A≈L2, B≈L3–L4, C≈L5 autonomous ADLC).")
    bul(d, "A Target State Studio defines the North-Star level and delivery platform (home-grown / COTS / Cognizant Flowsource), then auto-generates the interim roadmap.")
    bul(d, "The business case is a DORA J-Curve (cost-only): investment → tuition-cost dip → breakeven → compounding savings; ongoing cost is platform-aware and includes agent/token spend; feature revenue is excluded.")
    bul(d, "Outcomes are measured continuously on a three-perspective Outcome Dashboard: AI Adoption · PDLC Performance · AI Ops & Assurance.")
    d.save(os.path.join(OUT,"00-MASTER-INDEX.docx")); print("  ✓ 00-MASTER-INDEX")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__=="__main__":
    print("Building Set 3 v2 — Scale Implementation Pack (offering-centric)...")
    print("Building 23-platform-methodology-guide.docx..."); build_23()
    print("Building 24-governance-model.docx..."); build_24()
    print("Building 25-change-management-plan.docx..."); build_25()
    print("Building 26-platform-configuration-playbook.docx..."); build_26()
    print("Building 27-integration-architecture-guide.docx..."); build_27()
    print("Building 28-scale-training-curriculum.docx..."); build_28()
    print("Building 29-adoption-playbook.docx..."); build_29()
    print("Building 30-qa-framework.docx..."); build_30()
    print("Building 31-benefits-tracker-template.docx..."); build_31()
    print("Building 32-enterprise-scaling-playbook.pptx..."); build_32()
    print("Building 33-elt-executive-dashboard-briefing.pptx..."); build_33()
    print("Building 34-annual-roi-review-deck.pptx..."); build_34()
    print("Building 35-competitive-differentiation-briefing.docx..."); build_35()
    print("Building 00-MASTER-INDEX.docx..."); build_index()
    files=sorted(os.listdir(OUT))
    print(f"\n✓ All Set 3 v2 files complete — {len(files)} files in {OUT}")
    for f in files:
        size=os.path.getsize(os.path.join(OUT,f))//1024
        print(f"  {f} ({size}KB)")
