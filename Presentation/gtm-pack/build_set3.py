"""
GTM Pack — Set 3: Scale Implementation Pack
Generates 14 files for enterprise-wide rollout.
"""
import os
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

OUT = os.path.join(os.path.dirname(__file__), "set3-scale-implementation-pack")
os.makedirs(OUT, exist_ok=True)

# ─── Colors ──────────────────────────────────────────────────────────────────
DARK_BLUE  = RGBColor(0x0F, 0x2D, 0x5E)
MED_BLUE   = RGBColor(0x25, 0x63, 0xEB)
LIGHT_BLUE = RGBColor(0xDB, 0xEA, 0xFE)
ACCENT     = RGBColor(0x0D, 0x94, 0x88)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT  = RGBColor(0x1E, 0x29, 0x3B)

DNAVY  = DRGBColor(0x0F, 0x2D, 0x5E)
DBLUE  = DRGBColor(0x25, 0x63, 0xEB)
DTEAL  = DRGBColor(0x0D, 0x94, 0x88)
DWHT   = DRGBColor(0xFF, 0xFF, 0xFF)

# ─── PPTX Helpers ────────────────────────────────────────────────────────────
def new_prs():
    prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
    return prs

def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def rect(slide, x, y, w, h, fill=None, line=None):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid(); shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line; shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def txtbox(slide, text, x, y, w, h, size=12, bold=False, color=None, align=PP_ALIGN.LEFT, italic=False, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.word_wrap = wrap
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size = Pt(size); run.font.bold = bold; run.font.italic = italic
    run.font.color.rgb = color or DARK_TEXT
    return tb

def header_bar(slide, title, subtitle=None):
    rect(slide, 0, 0, 13.33, 1.1, fill=DARK_BLUE)
    txtbox(slide, title, 0.4, 0.12, 10, 0.55, size=24, bold=True, color=WHITE)
    if subtitle:
        txtbox(slide, subtitle, 0.4, 0.65, 10, 0.38, size=12, color=RGBColor(0xBF,0xDB,0xFE))

def stat_box(slide, x, y, w, h, value, label, bg=MED_BLUE):
    rect(slide, x, y, w, h, fill=bg)
    txtbox(slide, value, x, y+0.08, w, h*0.55, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txtbox(slide, label, x, y+h*0.52, w, h*0.45, size=9, color=WHITE, align=PP_ALIGN.CENTER)

# ─── DOCX Helpers ────────────────────────────────────────────────────────────
def new_doc():
    d = Document()
    for s in d.styles:
        try:
            if hasattr(s,'font'): s.font.name = "Calibri"
        except: pass
    sec = d.sections[0]
    sec.top_margin = Cm(2); sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
    return d

def sf(run, size, bold=False, italic=False, color=None):
    run.font.name="Calibri"; run.font.size=DPt(size)
    run.font.bold=bold; run.font.italic=italic
    if color: run.font.color.rgb=color

def h1(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(14); p.paragraph_format.space_after=DPt(4)
    r=p.add_run(text); sf(r,16,bold=True,color=DNAVY); return p

def h2(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(10); p.paragraph_format.space_after=DPt(3)
    r=p.add_run(text); sf(r,13,bold=True,color=DBLUE); return p

def h3(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(8); p.paragraph_format.space_after=DPt(2)
    r=p.add_run(text); sf(r,11,bold=True,color=DNAVY); return p

def body(doc, text, italic=False, color=None):
    p=doc.add_paragraph(); p.paragraph_format.space_after=DPt(4)
    r=p.add_run(text); sf(r,10.5,italic=italic,color=color); return p

def bul(doc, text, level=0):
    p=doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent=DPt(18+level*18)
    p.paragraph_format.space_after=DPt(2)
    r=p.add_run(text); sf(r,10.5); return p

def num(doc, text):
    p=doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after=DPt(2)
    r=p.add_run(text); sf(r,10.5); return p

def tbl(doc, headers, rows, col_widths=None):
    t=doc.add_table(rows=1+len(rows),cols=len(headers))
    t.style="Table Grid"; t.alignment=WD_TABLE_ALIGNMENT.LEFT
    for i,h in enumerate(headers):
        cell=t.rows[0].cells[i]
        tc=cell._tc; tcPr=tc.get_or_add_tcPr()
        shd=OxmlElement('w:shd')
        shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto')
        shd.set(qn('w:fill'),'0F2D5E'); tcPr.append(shd)
        p2=cell.paragraphs[0]; p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
        r2=p2.add_run(h); sf(r2,9.5,bold=True,color=DWHT)
    for ri,row in enumerate(rows):
        for ci,val in enumerate(row):
            cell=t.rows[ri+1].cells[ci]
            if ri%2==0:
                tc=cell._tc; tcPr=tc.get_or_add_tcPr()
                shd=OxmlElement('w:shd')
                shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto')
                shd.set(qn('w:fill'),'EFF6FF'); tcPr.append(shd)
            p2=cell.paragraphs[0]
            r2=p2.add_run(str(val)); sf(r2,9.5)
    if col_widths:
        for i,w in enumerate(col_widths):
            for row in t.rows:
                row.cells[i].width=DInches(w)
    doc.add_paragraph()
    return t

def divider(doc):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(6); p.paragraph_format.space_after=DPt(6)
    pPr=p._p.get_or_add_pPr()
    pBdr=OxmlElement('w:pBdr')
    bottom=OxmlElement('w:bottom')
    bottom.set(qn('w:val'),'single'); bottom.set(qn('w:sz'),'6')
    bottom.set(qn('w:space'),'1'); bottom.set(qn('w:color'),'2563EB')
    pBdr.append(bottom); pPr.append(pBdr)

def callout(doc, text, color_fill="DBEAFE"):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(6); p.paragraph_format.space_after=DPt(6)
    p.paragraph_format.left_indent=DPt(24); p.paragraph_format.right_indent=DPt(24)
    pPr=p._p.get_or_add_pPr()
    shd=OxmlElement('w:shd'); shd.set(qn('w:val'),'clear')
    shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),color_fill)
    pPr.append(shd)
    r=p.add_run(text); sf(r,10.5,italic=True,color=DNAVY)

def cover_page(doc, title, subtitle, doc_num, version="v1.0"):
    p=doc.add_paragraph(); p.paragraph_format.space_before=DPt(60)
    r=p.add_run("PDLC VSM Platform"); sf(r,13,bold=True,color=DBLUE)
    p=doc.add_paragraph()
    r=p.add_run("GTM Pack — Set 3: Scale Implementation Pack"); sf(r,11,color=DNAVY)
    doc.add_paragraph()
    p=doc.add_paragraph()
    r=p.add_run(title); sf(r,22,bold=True,color=DNAVY)
    p=doc.add_paragraph()
    r=p.add_run(subtitle); sf(r,12,italic=True,color=DBLUE)
    doc.add_paragraph(); doc.add_paragraph()
    divider(doc)
    tbl(doc,["Document","Version","Date","Classification"],
        [[doc_num,version,"March 2026","Commercial Confidential"]])
    doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 23 — Platform Methodology Guide
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 23-platform-methodology-guide.docx...")
d=new_doc()
cover_page(d,"Platform Methodology Guide","The Science Behind AI-Powered Value Stream Intelligence","DOC-SET3-23")
h1(d,"Introduction")
body(d,"This guide explains the methodology underpinning the PDLC VSM Platform — how data is collected, how each AI agent operates, the metrics it computes, and the academic and industry foundations behind each approach. It is intended for technical practitioners, delivery leads, and data-literate executives who want to understand the 'how' behind the platform's outputs.")

h1(d,"1. Value Stream Mapping Methodology")
h2(d,"1.1 Data Collection Approach")
body(d,"The platform ingests data from Application Lifecycle Management (ALM) tools — primarily Jira and Azure DevOps. The core data model requires: Issue Key, Status, Created Date, Resolved Date, Issue Type, and Sprint. Optional fields (Story Points, Priority, Epic) enhance analysis depth.")
h2(d,"1.2 PDLC Phase Mapping")
body(d,"Each ticket is assigned to one of 7 PDLC phases based on its status history and workflow transitions:")
tbl(d,["PDLC Phase","Typical Jira Statuses","Measurement"],
    [
        ["Requirements","Open, Backlog, To Do","Created → In Analysis date delta"],
        ["Design & Architecture","In Analysis, Architecture Review","In Analysis → Development delta"],
        ["Development","In Progress, In Development","In Development → Code Review delta"],
        ["Code Review & Merge","In Review, Peer Review, Code Review","Code Review → QA Ready delta"],
        ["Continuous Testing","In QA, Testing, SIT, UAT","QA → Done (test phases) delta"],
        ["Deployment Prep","Deploy Ready, Staging, Release Candidate","Staging → Production delta"],
        ["Release & Operations","Released, Done, Closed","Production timestamp"],
    ],col_widths=[2.0,2.8,3.7])
h2(d,"1.3 Lead Time and Flow Efficiency Formulas")
callout(d,"Lead Time (LT) = Sum of all phase durations from ticket creation to resolution (calendar days)\nProcess Time (PT) = Sum of active work phases only (phases where humans are actively working)\nWait Time (WT) = LT − PT (time in queues, approvals, and blocking states)\nFlow Efficiency (FE) = PT ÷ LT × 100%\nSector Benchmark: FE averages 17.8% in Financial Services (DORA State of DevOps 2024)")

h1(d,"2. DORA Assessment Methodology")
h2(d,"2.1 Framework Overview")
body(d,"The platform implements the DORA (DevOps Research and Assessment) framework as developed by Google Cloud and the DORA research team. The framework measures four key metrics — Deployment Frequency, Lead Time for Changes, Time to Restore Service (MTTR), and Change Failure Rate — and extends them into four capability dimensions assessed via 73 questions.")
h2(d,"2.2 Scoring Model")
tbl(d,["Dimension","Questions","Weight","Band Thresholds"],
    [
        ["Continuous Integration","19","25%","CRAWL <1.5 / WALK 1.5–3.0 / RUN 3.0–4.5 / FLY >4.5"],
        ["Continuous Deployment","18","25%","CRAWL <1.5 / WALK 1.5–3.0 / RUN 3.0–4.5 / FLY >4.5"],
        ["Continuous Testing","19","25%","CRAWL <1.5 / WALK 1.5–3.0 / RUN 3.0–4.5 / FLY >4.5"],
        ["Culture & Process","17","25%","CRAWL <1.5 / WALK 1.5–3.0 / RUN 3.0–4.5 / FLY >4.5"],
    ],col_widths=[2.0,1.2,1.2,4.5])
h2(d,"2.3 Data Source Integration")
body(d,"DORA scores are derived from 4 configured data sources: Jira (change failure rate, lead time proxies), Confluence (deployment frequency, runbook quality), SonarQube (code quality, test coverage), and GitHub (PR cycle time, deployment frequency). Manual override is available for any score via the platform UI.")

h1(d,"3. Bottleneck Analysis Methodology")
h2(d,"3.1 Bottleneck Identification Algorithm")
body(d,"The Bottleneck Analyzer agent applies a multi-factor scoring model to identify constraints in the value stream. Each potential bottleneck is scored on four dimensions:")
tbl(d,["Factor","Weight","Definition"],
    [
        ["Wait Time Magnitude","35%","Total wait hours in this phase per 100 tickets"],
        ["Flow Efficiency Delta","25%","Phase FE vs. sector benchmark FE for same phase"],
        ["Frequency","20%","% of tickets affected by this type of delay"],
        ["Benchmark Gap","20%","Phase LT vs. top-quartile peer benchmark for same phase"],
    ],col_widths=[2.5,1.2,5.0])
h2(d,"3.2 Severity Classification")
tbl(d,["Severity","Score Range","Annual Waste Threshold","Executive Escalation"],
    [
        ["Critical","80–100","≥200 hours / year","Required — present to CTO"],
        ["High","60–79","100–200 hours / year","Recommended — present to VP Eng"],
        ["Medium","40–59","50–100 hours / year","Team Lead level"],
        ["Low","<40","<50 hours / year","Engineering team discretion"],
    ],col_widths=[1.5,1.5,2.5,3.5])

h1(d,"4. Improvement Generation Methodology")
h2(d,"4.1 AI Improvement Matching")
body(d,"The Improvement Generator agent maps each bottleneck to a catalogue of 47 AI-native improvement initiatives, scored by: ROI multiplier (data from sector implementations), effort estimate (story points and calendar weeks), dependency mapping (which improvements unlock others), and DORA impact (which DORA dimensions each improvement addresses).")
h2(d,"4.2 ROI Estimation Model")
callout(d,"ROI = (Annual Waste Hours Recovered × Blended Engineering Hourly Rate × Recovery %) ÷ Implementation Cost\nDefault assumptions: $120/hr blended rate (FTE + overhead), 80% of projected waste recovered in Year 1, 95% in Year 2+. Implementation cost sourced from sector benchmarks for each initiative type.")
h2(d,"4.3 Roadmap Horizon Definition")
tbl(d,["Horizon","Timeline","Selection Criteria"],
    [
        ["Quick Win","0–90 days","Effort ≤8 weeks, ROI ≥2×, no external dependency, DORA impact immediate"],
        ["Medium-Term","3–6 months","Effort 2–4 months, ROI ≥3×, 1–2 dependencies, team-level decision"],
        ["Strategic","6–12 months","Effort 4–12 months, ROI ≥4×, cross-team or platform change required"],
    ],col_widths=[1.8,1.8,5.4])

h1(d,"5. Business Case Methodology")
h2(d,"5.1 Financial Model")
body(d,"The Business Case Builder agent constructs a full 5-year financial model for each of 3 scenarios (Conservative, Expected, Optimistic). The model includes:")
for item in ["Implementation costs (platform licence, consulting, internal effort, change management)","Annual benefits: engineering time recovered, incident reduction, faster time-to-market revenue uplift","DORA improvement multiplier: each DORA band improvement adds estimated 15–25% productivity gain","NPV at 10% discount rate, payback period, 5-year ROI"]:
    bul(d,item)
h2(d,"5.2 Scenario Assumptions")
tbl(d,["Parameter","Conservative","Expected","Optimistic"],
    [
        ["Waste recovery rate","50%","70%","90%"],
        ["DORA band improvement","0.5 bands","1.0 bands","1.5 bands"],
        ["Implementation speed","18 months","12 months","9 months"],
        ["Benefit realisation lag","6 months","4 months","3 months"],
        ["Risk contingency","25%","15%","5%"],
    ],col_widths=[2.8,1.8,1.8,1.8])

d.save(os.path.join(OUT,"23-platform-methodology-guide.docx"))
print("  ✓ Saved: 23-platform-methodology-guide.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 24 — Governance Model
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 24-governance-model.docx...")
d=new_doc()
cover_page(d,"Enterprise Governance Model","Operating Model for PDLC VSM Platform at Scale","DOC-SET3-24")
h1(d,"Purpose")
body(d,"This document defines the governance model for operating the PDLC VSM Platform at enterprise scale — across multiple teams, portfolios, and geographies. It covers decision rights, data governance, platform administration, insight quality standards, and executive reporting.")

h1(d,"Governance Structure")
h2(d,"Steering Committee (Monthly)")
tbl(d,["Role","Title","Responsibility"],
    [
        ["Executive Sponsor","CTO / CDO","Overall programme accountability; investment decisions"],
        ["Platform Owner","VP Engineering / DevOps Lead","Platform strategy, roadmap, and benefit realisation"],
        ["Data Governance Lead","Head of Data / CISO","Data access, privacy, quality, and audit standards"],
        ["Finance Lead","CFO delegate","ROI tracking, benefits realisation, budget oversight"],
        ["Change Management Lead","HR / Transformation Lead","Organisational change, adoption, and training"],
        ["Portfolio Representatives","Product Group Leads (×3–5)","Team-level reporting, escalation, and feedback"],
    ],col_widths=[2.0,2.5,5.0])

h2(d,"Platform Administration Team (Weekly)")
tbl(d,["Role","Responsibility","FTE Required"],
    [
        ["Platform Administrator","Day-to-day platform operations, user management, agent runs","0.5 FTE"],
        ["Data Integration Lead","ALM connector maintenance, data quality monitoring","0.25 FTE"],
        ["Insight Analyst","Results validation, executive reporting, benchmark updates","0.5 FTE"],
        ["Security & Compliance","Audit log review, access control, data governance adherence","0.1 FTE"],
    ],col_widths=[2.5,4.0,2.0])

h1(d,"Data Governance Policy")
h2(d,"Data Classification")
tbl(d,["Data Type","Classification","Retention","Access"],
    [
        ["ALM ticket data (anonymised)","Confidential","2 years","Platform admins + analysts"],
        ["ALM ticket data (with names)","Restricted","90 days","Platform admins only"],
        ["AI analysis outputs","Internal","3 years","Platform users + executives"],
        ["Audit logs","Confidential","5 years","Platform admins + compliance"],
        ["Benchmark database","Internal","Indefinite","All platform users"],
        ["Business case models","Restricted","5 years","Finance + executive sponsors"],
    ],col_widths=[2.5,1.5,1.5,3.0])

h2(d,"Data Quality Standards")
for standard in [
    "ALM data must have ≥85% resolved dates populated for VSM accuracy to be within ±10%",
    "New ticket data must be validated within 5 business days of each sprint close",
    "DORA source connections must be verified green at the start of each monthly governance cycle",
    "Any manual override must be documented with a rationale in the platform notes field",
    "Benchmark database refreshed quarterly from published DORA, Gartner, and IDC sources",
]:
    bul(d,standard)

h1(d,"Insight Quality Gates")
tbl(d,["Gate","Trigger","Reviewer","Standard","Action if Failed"],
    [
        ["G1: Data Quality","Monthly","Data Integration Lead","≥85% date completeness","Data remediation sprint before analysis run"],
        ["G2: Agent Run Validation","Post-run","Insight Analyst","VSM within ±10% of prior baseline","Manual override and re-run"],
        ["G3: Bottleneck Review","Pre-readout","Eng SME","Top 3 bottlenecks validated by engineer","Adjust confidence, add caveat to readout"],
        ["G4: Business Case Review","Pre-CFO","Finance Lead","ROI assumptions signed off by Finance","Revise assumptions, re-generate"],
        ["G5: Executive Readout","Pre-board","Executive Sponsor","Deck reviewed and approved by sponsor","Revise deck, re-brief"],
    ],col_widths=[1.5,1.8,1.8,2.3,2.1])

h1(d,"Reporting Cadence")
tbl(d,["Report","Frequency","Audience","Format","Owner"],
    [
        ["Team VSM Dashboard","Always-on","Team Leads","Platform (live)","Platform Admin"],
        ["Portfolio Flow Efficiency Scorecard","Weekly","VP Eng / Head of DevOps","Platform + email","Insight Analyst"],
        ["DORA Maturity Trend Report","Monthly","CTO + Portfolio Leads","Platform + PDF","Insight Analyst"],
        ["Benefits Realisation Report","Monthly","CFO + Executive Sponsor","Word / PDF","Finance Lead"],
        ["Executive Steering Report","Monthly","Steering Committee","Slide deck (8 slides)","Platform Owner"],
        ["Annual ROI Review","Annual","Board / ELT","Slide deck (15 slides)","Executive Sponsor"],
    ],col_widths=[2.5,1.5,2.0,2.0,1.5])

d.save(os.path.join(OUT,"24-governance-model.docx"))
print("  ✓ Saved: 24-governance-model.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 25 — Change Management Plan
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 25-change-management-plan.docx...")
d=new_doc()
cover_page(d,"Change Management Plan","Managing Organisational Change for Enterprise Platform Adoption","DOC-SET3-25")
h1(d,"Overview")
body(d,"Deploying the PDLC VSM Platform at enterprise scale is as much an organisational change as a technical implementation. This plan addresses the human side of the transformation: stakeholder alignment, resistance management, capability building, and embedding continuous improvement as a cultural norm.")

h1(d,"Stakeholder Analysis")
tbl(d,["Stakeholder Group","Count","Current Attitude","Desired Attitude","Key Concern","Engagement Strategy"],
    [
        ["Engineering Leads","5–20","Skeptical / Curious","Champion","'Will this expose my team's performance?'","1:1 briefings; show anonymisation; quick win wins them over"],
        ["Senior Engineers","20–100","Resistant","Supportive","'More process overhead'","Show automation angle; time savings demo; involve in validation"],
        ["QA Engineers","10–50","Interested","Champion","'Will AI replace our testing role?'","Position as AI-augmented; show bottleneck focus on process not people"],
        ["DevOps Engineers","5–20","Very Interested","Champion","'Finally — data to justify what we've been saying'","Early access; involve in DORA configuration; make them advocates"],
        ["Product Managers","10–30","Curious","Supportive","'More visibility into engineering delays'","Show business case builder; give access to future state scenarios"],
        ["CTO / VP Eng","1–3","Supportive","Sponsor","'Needs to show ROI to board'","Business case focus; board deck; personal briefing before ELT"],
        ["CFO","1","Skeptical","Approver","'Are the savings real and auditable?'","Evidence protocol; conservative scenario; reference call"],
        ["Delivery / PMO","3–10","Curious","Champion","'How does this fit our existing PMO tools?'","Show action plan integration; governance model alignment"],
    ],col_widths=[1.8,0.8,1.5,1.3,2.0,2.1])

h1(d,"Resistance Management")
h2(d,"Common Resistance Patterns and Responses")
for pattern, response in [
    ("'This is just another dashboard that will be ignored in 6 months'",
     "Show action plan tracker with owner accountability. Invite the skeptic to be a named action plan owner — skin in the game changes behaviour."),
    ("'The AI doesn't understand our unique context'",
     "Demonstrate manual override capability. Show that every AI score can be adjusted and the context notes field. The AI is a starting point, not a judgement."),
    ("'Our Jira data is too messy for this'",
     "Show data quality scorecard. Run a 100-ticket sample analysis in the kick-off meeting. Messy data is universal — the heuristic LT fills gaps."),
    ("'We already know what the bottlenecks are — we don't need AI to tell us'",
     "Agree! Then say: 'Great — let's see if the data agrees with you. And then let's put a dollar figure on each one so we can prioritise.' The financial quantification is always new."),
    ("'What about GDPR / data privacy?'",
     "On-prem deployment option. Ticket anonymisation (names replaced with role codes before analysis). Data stays inside the corporate network. No data sent to third parties (AI runs locally or via private API)."),
]:
    h3(d,f"Resistance: {pattern}")
    body(d,f"Response: {response}",italic=False)

h1(d,"Capability Building Plan")
tbl(d,["Audience","Training Module","Duration","Format","Certification"],
    [
        ["Platform Administrators","Full platform setup and operation","8 hours","Instructor-led + lab","Platform Admin Cert"],
        ["Engineering Leads","VSM interpretation + action planning","4 hours","Workshop","VSM Practitioner"],
        ["Insight Analysts","AI output validation + reporting","4 hours","Workshop","Insight Analyst Cert"],
        ["Executive Sponsors","Business case interpretation + board briefing","1 hour","Briefing session","None"],
        ["All Platform Users","Platform navigation (self-paced)","1 hour","eLearning (LMS)","None"],
    ],col_widths=[2.0,2.5,1.2,2.0,2.0])

h1(d,"30/60/90 Day Adoption Plan")
tbl(d,["Day","Milestone","Success Indicator"],
    [
        ["Day 1–7","Platform live, first team onboarded","VSM dashboard visible to team lead"],
        ["Day 7–14","First AI run completed and validated","Bottleneck list reviewed by Eng SME"],
        ["Day 14–30","All Day-30 quick wins identified and assigned","≥3 action plan items with named owners"],
        ["Day 30","First 30-day check-in: LT delta measured","LT delta visible in platform (baseline vs. current)"],
        ["Day 30–60","2nd and 3rd teams onboarded","Portfolio view shows 3 teams"],
        ["Day 60","First Portfolio Report to VP Eng","Report distributed and reviewed"],
        ["Day 60–90","First Quick Win implementation complete","LT reduction of ≥10% measured in platform"],
        ["Day 90","90-day ROI review to ELT","ROI tracking report presented; Scale Phase 2 decision"],
    ],col_widths=[1.2,3.8,3.5])

d.save(os.path.join(OUT,"25-change-management-plan.docx"))
print("  ✓ Saved: 25-change-management-plan.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 26 — Platform Configuration Playbook
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 26-platform-configuration-playbook.docx...")
d=new_doc()
cover_page(d,"Platform Configuration Playbook","Technical Configuration Reference for Multi-Team Deployments","DOC-SET3-26")
h1(d,"Overview")
body(d,"This playbook provides the definitive technical reference for configuring the PDLC VSM Platform for multi-team, multi-portfolio deployments. It covers environment setup, database scaling, ALM connector configuration, DORA source management, and platform customisation.")

h1(d,"Environment Architecture")
h2(d,"Deployment Options")
tbl(d,["Option","Infrastructure","Best For","Scaling Limit"],
    [
        ["Local (Laptop)","SQLite + localhost","Pilot only (1 team, <5K tickets)","1 team"],
        ["Cloud VM (Single)","PostgreSQL + single VM","Small scale (3–5 teams, <50K tickets)","5 teams"],
        ["Cloud VM (Load Balanced)","PostgreSQL + 2+ VMs behind LB","Mid scale (10–20 teams)","20 teams"],
        ["Container (Kubernetes)","PostgreSQL (managed) + K8s","Enterprise (20+ teams, >500K tickets)","Unlimited"],
    ],col_widths=[2.0,2.5,2.5,1.5])

h2(d,"Environment Variables")
tbl(d,["Variable","Required","Default","Description"],
    [
        ["OPENAI_API_KEY","Yes","None","OpenAI or Anthropic Claude API key for AI agents"],
        ["DATABASE_URL","Yes","sqlite:///./pdlc.db","PostgreSQL: postgresql+asyncpg://user:pass@host/db"],
        ["SECRET_KEY","Yes","None","JWT secret — generate: openssl rand -hex 32"],
        ["BACKEND_PORT","No","8001","Port for FastAPI backend"],
        ["FRONTEND_PORT","No","3001","Port for React frontend (set in vite.config.js)"],
        ["MAX_TICKET_BATCH","No","1000","Tickets processed per AI agent batch"],
        ["AGENT_TIMEOUT","No","300","AI agent timeout in seconds"],
        ["LOG_LEVEL","No","INFO","Logging level: DEBUG / INFO / WARNING / ERROR"],
    ],col_widths=[2.2,1.0,2.0,3.3])

h2(d,"Database Setup (PostgreSQL)")
for step, cmd in [
    ("Create database user", "CREATE USER pdlc_user WITH PASSWORD 'secure_password' SUPERUSER;"),
    ("Create database", "CREATE DATABASE pdlc_db OWNER pdlc_user;"),
    ("Run migrations", "alembic upgrade head"),
    ("Verify tables", "\\dt (should show 12 tables including vsm_snapshots, analysis_runs, devops_assessments)"),
    ("Create first admin user", "POST /admin/users with {email, password, role: 'admin'}"),
]:
    h3(d,step); body(d,cmd,color=DBLUE)

h1(d,"Multi-Team Project Configuration")
body(d,"Each team in the platform is represented as a Project. Projects are the primary isolation boundary — each project has its own ALM connection, VSM data, DORA assessment, and analysis runs.")
h2(d,"Creating Projects at Scale")
tbl(d,["Field","Required","Notes"],
    [
        ["Project Name","Yes","Use format: [Portfolio]-[Team] e.g., Payments-Phoenix"],
        ["Portfolio Label","Yes","Groups teams in the portfolio view"],
        ["Product Group","Yes","Used for business case aggregation"],
        ["Industry","No","Defaults to Financial Services; affects benchmark selection"],
        ["ALM Source","Yes","One per project; configure via /alm-connect"],
        ["DORA Sources","No","Up to 4; adds depth to DORA scoring"],
        ["Notes","No","Free text — use for team context (tech stack, Agile maturity, etc.)"],
    ],col_widths=[2.0,1.2,5.3])

h1(d,"ALM Connector Configuration")
h2(d,"Jira Cloud Configuration")
for step, detail in [
    ("Generate API Token","Jira Settings > Security > API Tokens > Create Token. Scope: read access to all projects"),
    ("CSV Export","Jira > Issues > Advanced Search > Export > CSV (Current Fields). Include all 12 required fields."),
    ("Upload to Platform","Platform > ALM Connect > Upload CSV. Platform validates all required fields on upload."),
    ("Field Mapping","Platform auto-maps standard Jira field names. Custom fields: use 'Field Mapping' tab to assign."),
    ("Phase Configuration","Platform > ALM Connect > Phase Config. Map each workflow status to a PDLC phase. Review auto-mapping before saving."),
]:
    h3(d,step); body(d,detail)

h2(d,"Azure DevOps Configuration")
for step, detail in [
    ("Generate PAT","ADO > User Settings > Personal Access Tokens. Scope: Work Items (Read), Analytics (Read)"),
    ("Export Work Items","ADO > Boards > Work Items > Column Options (add all 12 fields) > Export to CSV"),
    ("Status Mapping","ADO uses 'State' not 'Status'. Common mapping: New→Requirements, Active→Development, Resolved→Testing, Closed→Done"),
]:
    h3(d,step); body(d,detail)

h1(d,"Performance Tuning")
tbl(d,["Scenario","Issue","Recommended Fix"],
    [
        ["Large ticket sets (>50K)","Agent run times >15 min","Increase MAX_TICKET_BATCH to 2000; use PostgreSQL connection pooling"],
        ["Slow dashboard load","Portfolio view loading >5s","Add PostgreSQL index on vsm_snapshots.project_id, created_at"],
        ["Agent timeout errors","Timeout at >300s","Increase AGENT_TIMEOUT; check OpenAI API rate limits"],
        ["Memory errors on large runs","OOM on 100K+ tickets","Enable streaming mode in agent config; add 4GB RAM to VM"],
        ["DORA run failing on Sonar","Connection timeout","Check SonarQube firewall rules; use SonarQube token not password"],
    ],col_widths=[2.0,2.5,4.0])

d.save(os.path.join(OUT,"26-platform-configuration-playbook.docx"))
print("  ✓ Saved: 26-platform-configuration-playbook.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 27 — Integration Architecture Guide
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 27-integration-architecture-guide.docx...")
d=new_doc()
cover_page(d,"Integration Architecture Guide","Connecting PDLC VSM Platform to Enterprise Toolchains","DOC-SET3-27")
h1(d,"Overview")
body(d,"This guide describes the integration architecture for connecting the PDLC VSM Platform to enterprise toolchains. It covers inbound data integrations (ALM, DORA sources), outbound reporting integrations (BI tools, dashboards), webhook notifications, and API reference for custom integrations.")

h1(d,"Integration Catalogue")
tbl(d,["Integration","Direction","Type","Data Exchanged","Status"],
    [
        ["Jira Cloud / Server","Inbound","REST API + CSV","Ticket data, status history, sprints","Supported"],
        ["Azure DevOps","Inbound","REST API + CSV","Work items, iterations, pipelines","Supported"],
        ["Confluence","Inbound","REST API","Pages for DORA evidence","Supported"],
        ["SonarQube","Inbound","REST API","Code quality, coverage metrics","Supported"],
        ["GitHub","Inbound","REST API","PR cycle time, deployment frequency","Supported"],
        ["GitLab","Inbound","REST API","Merge requests, pipeline metrics","Planned"],
        ["Jenkins","Inbound","Webhook","Build frequency, MTTR proxies","Planned"],
        ["ServiceNow","Inbound","REST API","Change records, incident MTTR","Roadmap"],
        ["Power BI","Outbound","REST API / CSV export","VSM metrics, bottleneck data","Supported"],
        ["Tableau","Outbound","REST API / CSV export","All platform metrics","Supported"],
        ["Slack","Outbound","Webhook","Analysis complete notifications","Supported"],
        ["Microsoft Teams","Outbound","Webhook","Analysis complete notifications","Supported"],
        ["JIRA (write-back)","Bidirectional","REST API","Action plan items → Jira tasks","Planned"],
    ],col_widths=[2.0,1.2,1.5,2.8,1.5])

h1(d,"API Reference")
h2(d,"Core Endpoints")
tbl(d,["Method","Endpoint","Description","Auth"],
    [
        ["GET","/health","Platform health check","None"],
        ["POST","/projects","Create new project","Bearer token"],
        ["GET","/projects/{id}","Get project details","Bearer token"],
        ["POST","/agents/run-analysis/{project_id}","Trigger full AI pipeline","Bearer token"],
        ["GET","/agents/result/{project_id}","Get latest analysis result","Bearer token"],
        ["GET","/devops-maturity/assessments/{id}","Get DORA assessment","Bearer token"],
        ["POST","/devops-maturity/assessments/{id}/run","Run DORA assessment","Bearer token"],
        ["GET","/devops-maturity/assessments/{id}/action-items","Get action plan","Bearer token"],
        ["PATCH","/devops-maturity/assessments/{id}/action-items/{item_id}","Update action item","Bearer token"],
    ],col_widths=[1.0,3.5,2.5,1.5])

h2(d,"Webhook Notifications")
body(d,"Configure outbound webhooks via Platform Settings > Integrations > Webhooks. Supported events:")
tbl(d,["Event","Payload Fields","Typical Use"],
    [
        ["analysis.complete","project_id, run_id, lead_time, flow_efficiency, bottleneck_count","Trigger Slack/Teams notification"],
        ["analysis.failed","project_id, run_id, error_message","Alert PagerDuty / OpsGenie"],
        ["action_item.status_changed","item_id, old_status, new_status, owner","Update Jira task status"],
        ["dora.assessment.complete","assessment_id, overall_score, band","Trigger monthly report"],
    ],col_widths=[2.5,3.5,2.5])

h1(d,"Power BI Integration")
body(d,"The platform exposes a read-only REST API for BI tool integration. Power BI users can connect via 'Web Data Source' using the following steps:")
for step in [
    "Power BI Desktop > Get Data > Web",
    "URL: http://[platform-host]:8001/agents/result/[project_id]",
    "Authentication: Bearer token (generate via Platform Settings > API Keys)",
    "Transform: The JSON response contains vsm_data, bottlenecks, and improvements arrays",
    "Schedule refresh: Set to daily for always-current dashboards",
    "Recommended visuals: Bar chart (phase LT), Gauge (flow efficiency vs. benchmark), Table (bottleneck list)",
]:
    num(d,step)

d.save(os.path.join(OUT,"27-integration-architecture-guide.docx"))
print("  ✓ Saved: 27-integration-architecture-guide.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 28 — Training Curriculum (Scale)
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 28-scale-training-curriculum.docx...")
d=new_doc()
cover_page(d,"Scale Training Curriculum","Capability Building Programme for Enterprise Platform Adoption","DOC-SET3-28")
h1(d,"Programme Overview")
body(d,"This curriculum defines the training programme for enterprise-scale PDLC VSM Platform adoption. It is structured in four tracks, each targeting a different audience. All tracks use a combination of instructor-led workshops, self-paced eLearning, and hands-on lab exercises.")
tbl(d,["Track","Audience","Duration","Certification","Frequency"],
    [
        ["Track 1: Platform Administrator","IT / Platform Ops","8 hours","Platform Admin Cert","Once (at onboarding)"],
        ["Track 2: VSM Practitioner","Engineering Leads, Delivery Leads","4 hours","VSM Practitioner Cert","Once + annual refresh"],
        ["Track 3: Insight Analyst","Data Analysts, PMO","4 hours","Insight Analyst Cert","Once + annual refresh"],
        ["Track 4: Executive Briefing","CTO, VP Eng, CFO","1 hour","None","Once + annual update"],
    ],col_widths=[2.0,2.5,1.5,2.0,1.5])

h1(d,"Track 1: Platform Administrator (8 Hours)")
modules = [
    ("Module 1.1: Platform Architecture (1h)", [
        "PDLC VSM Platform architecture: frontend, backend, database, AI agents",
        "Component overview: 8 LangGraph agents and their data flow",
        "Deployment options: local, cloud VM, Kubernetes",
        "Environment variables and configuration files",
        "Lab: deploy platform locally and run health check",
    ]),
    ("Module 1.2: Project and User Management (1h)", [
        "Creating and configuring projects (teams)",
        "User roles: Admin, Analyst, Viewer",
        "API key management and token rotation",
        "Multi-team portfolio configuration",
        "Lab: create 3 test projects and assign users",
    ]),
    ("Module 1.3: ALM Connector Configuration (2h)", [
        "Jira Cloud: API token setup, CSV export, field mapping, phase configuration",
        "Azure DevOps: PAT setup, work item export, status mapping",
        "Data quality standards: required fields, date format, minimum ticket count",
        "Data quality scorecard: interpreting and resolving issues",
        "Lab: configure Jira connector for test project; validate VSM output",
    ]),
    ("Module 1.4: DORA Source Management (2h)", [
        "Configuring all 4 DORA sources: Jira, Confluence, SonarQube, GitHub",
        "Connection testing and troubleshooting",
        "Source weighting and manual override procedures",
        "Lab: configure all 4 sources and run DORA assessment",
    ]),
    ("Module 1.5: Monitoring and Maintenance (1h)", [
        "Platform health monitoring: /health endpoint, log monitoring",
        "Database backup and restore procedures",
        "Handling failed agent runs: logs, retry, escalation",
        "Security: access control review, token rotation schedule",
        "Lab: simulate agent failure and recover using runbook",
    ]),
    ("Module 1.6: Certification Assessment (1h)", [
        "20-question written assessment (pass mark: 75%)",
        "Practical lab: configure a complete project from scratch",
        "Issue certificate: Platform Admin Cert v1.0",
    ]),
]
for mod_title, items in modules:
    h2(d,mod_title)
    for item in items: bul(d,item)

h1(d,"Track 2: VSM Practitioner (4 Hours)")
for mod_title, items in [
    ("Module 2.1: VSM Fundamentals (1h)", [
        "Value stream mapping: origin, purpose, and modern application",
        "Lead time, flow efficiency, process time, wait time — definitions and formulas",
        "The 7 PDLC phases: what they measure and how to interpret phase-level data",
        "Reading the Current State VSM dashboard: what to look for first",
    ]),
    ("Module 2.2: DORA Framework (1h)", [
        "DORA's four key metrics: Deployment Frequency, LT for Changes, MTTR, Change Failure Rate",
        "Four capability dimensions and 73 questions",
        "Reading DORA scores: band classification, dimension breakdown, gap analysis",
        "Connecting DORA scores to VSM bottlenecks",
    ]),
    ("Module 2.3: Interpreting AI Outputs (1h)", [
        "Bottleneck analysis: severity scoring, root cause labels, benchmark comparison",
        "Improvement roadmap: ROI interpretation, effort estimates, dependencies",
        "Business case: scenario selection, NPV, payback — what to show the CFO",
        "Evidence protocol: citing AI outputs in executive presentations",
    ]),
    ("Module 2.4: Action Planning and Tracking (1h)", [
        "Creating and managing action plan items in the platform",
        "Setting owners, target dates, and effort estimates",
        "Tracking improvement progress: LT and FE delta over time",
        "Monthly review process: what to present to VP Eng",
        "Certification: 15-question assessment (pass: 80%)",
    ]),
]:
    h2(d,mod_title)
    for item in items: bul(d,item)

h1(d,"Track 3: Insight Analyst (4 Hours)")
for mod_title, items in [
    ("Module 3.1: Data Validation (1.5h)", [
        "VSM accuracy validation: 20-ticket manual audit process",
        "Bottleneck validation: engineering SME review protocol",
        "AI evidence classification: Class 1/2/3/4 and citation standards",
        "Lab: validate a sample VSM output using the 20-ticket audit method",
    ]),
    ("Module 3.2: Reporting (1.5h)", [
        "Platform exports: PDF, CSV, PPT generation",
        "Power BI / Tableau integration: API connection setup",
        "Executive reporting templates: weekly scorecard, monthly DORA report",
        "Benefits realisation tracking: setting up the quarterly ROI report",
    ]),
    ("Module 3.3: Certification (1h)", [
        "15-question practical assessment",
        "Lab: produce a complete portfolio report for 3 teams",
        "Issue certificate: Insight Analyst Cert v1.0",
    ]),
]:
    h2(d,mod_title)
    for item in items: bul(d,item)

d.save(os.path.join(OUT,"28-scale-training-curriculum.docx"))
print("  ✓ Saved: 28-scale-training-curriculum.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 29 — Adoption Playbook
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 29-adoption-playbook.docx...")
d=new_doc()
cover_page(d,"Adoption Playbook","Driving Platform Usage and Embedding Continuous Improvement","DOC-SET3-29")
h1(d,"Adoption Framework")
body(d,"Platform adoption is measured across three dimensions: breadth (how many teams use it), depth (how frequently it's used), and impact (whether insights drive real improvement actions). This playbook provides tactics for each dimension.")

h1(d,"Breadth: Expanding Team Coverage")
h2(d,"Team Onboarding Wave Model")
body(d,"Roll out in waves of 3–5 teams to allow learnings from each wave to improve the next:")
tbl(d,["Wave","Teams","Duration","Success Gate"],
    [
        ["Wave 0 (Pilot)","1 team","8 weeks","VSM validated, bottleneck list approved, sponsor satisfied"],
        ["Wave 1","3–5 teams","4–6 weeks","All teams have VSM dashboards; portfolio view live"],
        ["Wave 2","5–10 teams","6–8 weeks","Monthly portfolio report running; 3+ Quick Wins in flight"],
        ["Wave 3","All remaining","8–12 weeks","Enterprise benchmark live; annual ROI review scheduled"],
    ],col_widths=[1.5,1.5,1.8,4.7])

h2(d,"Team Lead Engagement Tactics")
for tactic in [
    "Executive mandate: Sponsor sends all-hands email introducing platform and why it matters",
    "Peer reference: Wave 0 team lead presents results at engineering all-hands (15 min)",
    "WIIFM framing: 'This makes your team's invisible work visible — and gives you the data to get more resources'",
    "Low-effort onboarding: Pilot Lead configures first project; team lead only needs 2 hours",
    "Quick Win win: Ensure every team has a Quick Win in their action plan within 30 days of onboarding",
]:
    bul(d,tactic)

h1(d,"Depth: Increasing Usage Frequency")
h2(d,"Usage KPIs")
tbl(d,["KPI","Target (Month 3)","Target (Month 6)","Target (Month 12)","Measurement"],
    [
        ["Teams with VSM data loaded","50% of target teams","80%","100%","Platform admin report"],
        ["Monthly active users (MAU)","10+ per team","15+ per team","20+ per team","Platform analytics"],
        ["Analysis runs per team per month","1","2","4","Platform analytics"],
        ["Action plan items with owners","≥10 per team","≥20 per team","≥30 per team","Platform action plan"],
        ["Quick Wins completed","1 per team","3 per team","5 per team","Platform action plan"],
    ],col_widths=[3.0,1.5,1.5,1.5,2.0])

h2(d,"Engagement Tactics")
for tactic in [
    "Monthly league table: publish VSM flow efficiency ranking across teams (gamification)",
    "Improvement trophy: quarterly award for team with most Quick Wins completed",
    "Platform office hours: weekly 30-min open session for questions and demos",
    "Newsletter: monthly '3 Things the AI Found This Month' sent to all team leads",
    "Executive visibility: CTO references platform data in engineering all-hands — creates pull",
]:
    bul(d,tactic)

h1(d,"Impact: Turning Insights into Improvements")
h2(d,"Insight-to-Action Conversion Rate")
body(d,"Target: 60% of bottleneck insights converted to action plan items within 30 days. Track in platform via 'Bottlenecks without action plan items' dashboard widget (available in Platform > Settings > Widgets).")
h2(d,"Improvement Sprint Cadence")
for item in [
    "Every sprint: team lead reviews 'Action Plan' tab — updates status of in-flight items",
    "Every sprint review: one action plan item presented as 'improvement story' alongside feature stories",
    "Monthly: Insight Analyst runs 'LT delta report' — shows improvement in lead time vs. baseline",
    "Quarterly: ELT receives benefits realisation report — AI platform $ value vs. investment to date",
]:
    bul(d,item)

h1(d,"Sustaining Adoption at 12 Months")
for risk, response in [
    ("Platform fatigue (users stop checking)","Automate weekly email digest with top insight from each team's VSM"),
    ("Data staleness (ALM data not refreshed)","Automate monthly data refresh reminder; set up CI/CD hook to trigger on sprint close"),
    ("No visible improvements (action plan stalls)","Monthly 'improvement debt' report to sponsors; escalate if >60 days without completion"),
    ("Key champion leaves","Succession planning: always have 2 trained practitioners per team; cross-train backup admin"),
    ("Platform not updated","Schedule quarterly platform update window; Pilot Lead sends release notes"),
]:
    h3(d,f"Risk: {risk}"); body(d,f"Response: {response}")

d.save(os.path.join(OUT,"29-adoption-playbook.docx"))
print("  ✓ Saved: 29-adoption-playbook.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 30 — QA Framework
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 30-qa-framework.docx...")
d=new_doc()
cover_page(d,"Quality Assurance Framework","Standards for Data Quality, AI Output Quality, and Platform Reliability","DOC-SET3-30")
h1(d,"Purpose")
body(d,"This QA Framework defines the quality standards, testing procedures, and validation protocols for the PDLC VSM Platform at enterprise scale. It covers three quality domains: data quality (ALM inputs), AI output quality (agent results), and platform reliability (uptime and performance).")

h1(d,"Domain 1: Data Quality")
h2(d,"Data Quality Dimensions")
tbl(d,["Dimension","Definition","Minimum Standard","Measurement Method"],
    [
        ["Completeness","% of required fields populated","≥85% resolved dates","Automated: /data-quality/report"],
        ["Accuracy","Lead time within ±10% of manual audit","±10% on 20-ticket sample","Manual: quarterly audit"],
        ["Timeliness","Data loaded within 5 days of sprint close","≤5 business days","Platform: last-updated timestamp"],
        ["Consistency","Status values map to valid PDLC phases","0 unmapped statuses","Platform: field mapping validator"],
        ["Volume","Sufficient ticket count for statistical significance","≥500 tickets per team","Automated: ticket count check"],
    ],col_widths=[1.8,2.5,2.0,2.2])

h2(d,"Data Quality Remediation Procedures")
tbl(d,["Issue","Threshold","Action","Owner"],
    [
        ["Missing resolved dates",">15%","Export with status history; use transition dates","Data Integration Lead"],
        ["Unmapped statuses",">5 statuses","Update phase config; re-run VSM","Platform Admin"],
        ["Ticket count below minimum","<500 tickets","Extend date range; add sub-tasks if excluded","Data Integration Lead"],
        ["Duplicate tickets",">1% duplication","Run de-duplication script (provided)","Platform Admin"],
        ["Future dates in resolved","Any occurrence","Data cleanse before upload","Data Integration Lead"],
    ],col_widths=[2.5,1.5,3.0,1.5])

h1(d,"Domain 2: AI Output Quality")
h2(d,"Agent Output Validation Tests")
tbl(d,["Agent","Test","Pass Criterion","Frequency"],
    [
        ["VSM Analyzer","Lead time plausibility check","LT between 1 and 180 days","Every run"],
        ["VSM Analyzer","FE sanity check","FE between 1% and 95%","Every run"],
        ["Benchmark Agent","Benchmark count","≥8 competitor data points","Every run"],
        ["Bottleneck Analyzer","Bottleneck count","≥1 bottleneck per phase","Every run"],
        ["Improvement Generator","ROI range check","All ROI estimates between 0.5× and 20×","Every run"],
        ["Business Case Builder","Payback plausibility","Payback between 3 months and 10 years","Every run"],
        ["DORA Agent","Score range","All scores between 0 and 5","Every run"],
        ["All agents","Execution time","<10 minutes for <10K tickets","Every run"],
    ],col_widths=[2.0,2.8,2.5,1.2])

h2(d,"Human Validation Protocol")
for step in [
    "VSM accuracy: engineering SME selects 20 tickets and manually computes lead time — compares to platform output. Acceptable tolerance: ±10%.",
    "Bottleneck validation: engineering SME reviews top 3 bottlenecks — confirms they reflect real team experience. Document agreement/disagreement with rationale.",
    "Business case review: Finance Lead reviews revenue uplift assumptions and implementation cost estimates. Signs off within 5 business days of run completion.",
    "Executive readout review: Sponsor reviews draft deck 48 hours before delivery. Approves or requests amendments.",
]:
    num(d,step)

h1(d,"Domain 3: Platform Reliability")
h2(d,"SLA Targets")
tbl(d,["Metric","Target","Measurement","Escalation"],
    [
        ["Platform uptime","99.5% monthly","Automated health check every 5 min","Alert on 3 consecutive failures"],
        ["Agent run success rate","≥95% of runs complete without error","Platform analytics","Alert if <90% in any week"],
        ["Dashboard load time","<3 seconds (P95)","Browser performance monitoring","Alert if >5s sustained"],
        ["API response time","<500ms (P95) for GET endpoints","API monitoring","Alert if >2s sustained"],
        ["Data refresh latency","<24h from ALM data upload to VSM update","Automated check","Alert if >48h"],
    ],col_widths=[2.2,1.8,2.5,2.0])

h2(d,"Incident Classification")
tbl(d,["Severity","Definition","Response Time","Resolution Time","Notification"],
    [
        ["P1 — Critical","Platform completely unavailable","15 minutes","4 hours","Sponsor + Admin immediate"],
        ["P2 — High","AI agents failing for >50% of runs","1 hour","8 hours","Admin + Team Leads"],
        ["P3 — Medium","Single agent failing; data quality degraded","4 hours","24 hours","Admin"],
        ["P4 — Low","UI issue; non-critical feature","Next business day","5 business days","Admin"],
    ],col_widths=[2.0,2.5,1.5,1.8,1.7])

d.save(os.path.join(OUT,"30-qa-framework.docx"))
print("  ✓ Saved: 30-qa-framework.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 31 — Benefits Tracker Template
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 31-benefits-tracker-template.docx...")
d=new_doc()
cover_page(d,"Benefits Tracker Template","Measuring and Reporting ROI from PDLC VSM Platform Improvements","DOC-SET3-31")
h1(d,"Purpose")
body(d,"The Benefits Tracker is the definitive record of value delivered by the PDLC VSM Platform programme. It links each improvement initiative in the action plan to a quantified financial benefit, measured against the baseline established at the start of the pilot. Updated monthly by the Insight Analyst and reviewed quarterly by the CFO.")
callout(d,"Target: 100% of action plan items with a completed status must have a measured benefit recorded within 30 days of completion.")

h1(d,"Baseline Metrics (Complete at Pilot End)")
tbl(d,["Metric","Baseline Value","Source","Date","Analyst"],
    [
        ["Overall Lead Time (days)", "", "VSM Analyzer — Pilot Run", "", ""],
        ["Flow Efficiency (%)", "", "VSM Analyzer — Pilot Run", "", ""],
        ["Process Time (hours/feature)", "", "VSM Analyzer — Pilot Run", "", ""],
        ["Wait Time (hours/feature)", "", "VSM Analyzer — Pilot Run", "", ""],
        ["DORA Overall Score (/5.0)", "", "DORA Assessment — Pilot Run", "", ""],
        ["DORA Band", "", "DORA Assessment — Pilot Run", "", ""],
        ["Annual Savings Identified ($)", "", "Business Case Builder", "", ""],
        ["Expected ROI (×)", "", "Business Case Builder", "", ""],
        ["Number of Critical Bottlenecks", "", "Bottleneck Analyzer", "", ""],
    ],col_widths=[3.0,1.5,2.5,1.0,1.5])

h1(d,"Improvement Benefit Register")
tbl(d,["Item ID","Improvement Title","Horizon","Team","Owner","Target Date","Completed","Baseline (h/feature)","Actual (h/feature)","Reduction","$ Value Realised"],
    [
        ["IMP-001","[Initiative 1]","Quick Win","[Team]","[Owner]","[Date]","","[Xh]","[Xh]","[X%]","$[X,XXX]"],
        ["IMP-002","[Initiative 2]","Quick Win","[Team]","[Owner]","[Date]","","[Xh]","[Xh]","[X%]","$[X,XXX]"],
        ["IMP-003","[Initiative 3]","Medium","[Team]","[Owner]","[Date]","","[Xh]","[Xh]","[X%]","$[X,XXX]"],
        ["IMP-004","[Initiative 4]","Medium","[Team]","[Owner]","[Date]","","[Xh]","[Xh]","[X%]","$[X,XXX]"],
        ["IMP-005","[Initiative 5]","Strategic","[Team]","[Owner]","[Date]","","[Xh]","[Xh]","[X%]","$[X,XXX]"],
    ],col_widths=[0.8,2.0,0.9,0.8,0.9,0.8,0.9,1.0,1.0,0.8,1.0])

h1(d,"Quarterly ROI Summary")
tbl(d,["Quarter","Cumulative Investment","Cumulative Benefits","Cumulative ROI","Initiatives Complete","LT Improvement","FE Improvement"],
    [
        ["Q1 (Pilot)","$150K","$[X]","[X.X]×","[X]","Baseline","Baseline"],
        ["Q2","$[X]","$[X]","[X.X]×","[X]","[−X] days","[+X]%"],
        ["Q3","$[X]","$[X]","[X.X]×","[X]","[−X] days","[+X]%"],
        ["Q4","$[X]","$[X]","[X.X]×","[X]","[−X] days","[+X]%"],
        ["Year 2 Q1","$[X]","$[X]","[X.X]×","[X]","[−X] days","[+X]%"],
    ],col_widths=[1.5,1.8,1.5,1.3,1.3,1.3,1.3])

h1(d,"Measurement Methodology")
h2(d,"How to Measure Lead Time Improvement")
for step in [
    "Run Platform Analysis > Run Full Analysis at the start of each quarter (creates new VSM snapshot)",
    "Navigate to Current State VSM — compare 'Current' LT with the Baseline LT from the Benefits Tracker",
    "Record the delta in the Quarterly ROI Summary table above",
    "If LT has increased: investigate using the Bottleneck Analyzer — new bottleneck may have emerged",
]:
    num(d,step)

h2(d,"How to Calculate $ Value of LT Reduction")
callout(d,"$ Value = (LT Reduction in Days ÷ Original LT in Days) × Annual Engineering Cost × Flow Efficiency Multiplier\nExample: 10-day reduction ÷ 42-day baseline × $5M annual team cost × 1.15 FE multiplier = $1.37M annual value\nUse actual team engineering cost from Finance. Default blended rate: $120/hr × 2,080hrs × team size.")

d.save(os.path.join(OUT,"31-benefits-tracker-template.docx"))
print("  ✓ Saved: 31-benefits-tracker-template.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 32 — Enterprise Scaling Playbook (PPT)
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 32-enterprise-scaling-playbook.pptx...")
prs=new_prs()

# Slide 1: Cover
sl=blank(prs)
rect(sl,0,0,13.33,7.5,fill=DARK_BLUE)
rect(sl,0,5.2,13.33,2.3,fill=MED_BLUE)
txtbox(sl,"PDLC VSM Platform",0.8,0.5,11,0.5,size=15,color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl,"Enterprise Scaling Playbook",0.8,1.1,11,0.8,size=30,bold=True,color=WHITE)
txtbox(sl,"From 1 Team to 100 Teams — The Repeatable Playbook for Organisation-Wide Value Stream Intelligence",0.8,2.1,11,0.7,size=14,color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl,"Set 3: Scale Implementation Pack  |  March 2026  |  Commercial Confidential",0.8,5.6,11,0.5,size=12,color=WHITE)

# Slide 2: Why Scale
sl=blank(prs)
header_bar(sl,"Why Scale Matters","The ROI Compounds Non-Linearly with Each Team Added")
for i,(v,l) in enumerate([("1 team","$1.2M/yr value"),("5 teams","$5.4M/yr value"),("15 teams","$14M/yr value"),("Org-wide","$25M+ /yr value")]):
    x=0.5+i*3.1
    rect(sl,x,1.2,2.7,1.8,fill=DARK_BLUE if i<3 else MED_BLUE)
    txtbox(sl,v,x,1.2,2.7,0.7,size=16,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,l,x,1.95,2.7,0.7,size=13,color=WHITE,align=PP_ALIGN.CENTER)
insights = [
    "Infrastructure cost is fixed — each additional team adds ~$30K in value for ~$5K incremental cost",
    "Cross-team benchmarking becomes possible at 5+ teams — revealing systemic vs. team-specific issues",
    "Organisation-wide DORA benchmark enables board-level transformation narrative",
    "Action plan network effects: Quick Wins in one team become templates for all teams",
]
for i,insight in enumerate(insights):
    txtbox(sl,f"• {insight}",0.5,3.3+i*0.75,12.3,0.65,size=10,color=DARK_TEXT)

# Slide 3: Wave Model
sl=blank(prs)
header_bar(sl,"Wave-Based Rollout Model","Controlled Expansion with Value Gates at Each Wave")
waves=[("Wave 0\nPilot","1 team\n8 weeks","$150K","Validated VSM\n+ Sponsor endorsement"),
       ("Wave 1\n3–5 Teams","4–6 weeks\nper team","$300–500K","Portfolio view live\n+ 1 Quick Win per team"),
       ("Wave 2\n10–15 Teams","6–8 weeks\nper batch","$800K–1.2M","Monthly ELT report\n+ 3+ Quick Wins in flight"),
       ("Wave 3\nAll Teams","8–12 weeks\nper batch","$2–3M","Org benchmark\n+ Annual ROI review")]
for i,(label,timing,invest,gate) in enumerate(waves):
    x=0.3+i*3.25
    rect(sl,x,1.2,3.0,0.65,fill=DARK_BLUE)
    txtbox(sl,label,x,1.2,3.0,0.65,size=12,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    rect(sl,x,1.85,3.0,4.05,fill=LIGHT_BLUE)
    txtbox(sl,f"Timeline:\n{timing}",x+0.1,1.95,2.8,0.8,size=10,color=DARK_TEXT)
    txtbox(sl,f"Investment:\n{invest}",x+0.1,2.85,2.8,0.8,size=10,color=DARK_TEXT)
    txtbox(sl,f"Value Gate:\n{gate}",x+0.1,3.75,2.8,1.0,size=10,color=DARK_TEXT)

# Slide 4: 18-Month Roadmap
sl=blank(prs)
header_bar(sl,"18-Month Scale Roadmap","Milestones, Value Gates, and Expected Outcomes")
milestones=[
    ("Month 1–2","Pilot complete\nWave 1 kick-off"),
    ("Month 3–4","5 teams live\nPortfolio VSM"),
    ("Month 5–6","First ROI\nrealisation report"),
    ("Month 7–9","10–15 teams\nELT dashboard"),
    ("Month 10–12","20+ teams\nOrg benchmark"),
    ("Month 13–18","All teams\nAnnual ROI review"),
]
for i,(m,txt) in enumerate(milestones):
    x=0.3+i*2.18
    rect(sl,x,1.2,1.9,0.45,fill=DARK_BLUE)
    txtbox(sl,m,x,1.2,1.9,0.45,size=9,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    rect(sl,x,1.65,1.9,2.5,fill=LIGHT_BLUE)
    txtbox(sl,txt,x+0.05,1.75,1.8,2.2,size=10,color=DARK_TEXT,wrap=True)
txtbox(sl,"Expected Cumulative Value: $1.2M (Month 3) → $5.4M (Month 6) → $14M (Month 12) → $25M+ (Month 18)",0.3,4.4,12.7,0.5,size=10,bold=True,color=MED_BLUE,align=PP_ALIGN.CENTER)

# Slide 5: Success Factors
sl=blank(prs)
header_bar(sl,"Critical Success Factors","What Separates 4× from 12× ROI at Enterprise Scale")
factors=[
    ("Executive Mandate","CTO actively references platform in all-hands. Creates pull — teams want to be on it."),
    ("Quick Wins First","Every team gets a Quick Win in the action plan within 30 days. Builds credibility fast."),
    ("Insight Analyst Role","Dedicated 0.5 FTE validates outputs, produces reports, tracks benefits. Don't skip this."),
    ("Data Quality Discipline","Monthly data refresh cadence. Teams that skip data refresh lose momentum fast."),
    ("Continuous Improvement Loop","Sprint reviews include action plan items. VSM becomes part of the rhythm, not a one-off."),
]
for i,(title,detail) in enumerate(factors):
    y=1.25+i*1.1
    rect(sl,0.3,y,0.5,0.8,fill=MED_BLUE)
    txtbox(sl,str(i+1),0.3,y,0.5,0.8,size=16,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,title,0.95,y+0.05,2.5,0.7,size=12,bold=True,color=DARK_BLUE)
    txtbox(sl,detail,3.5,y+0.05,9.5,0.7,size=10,color=DARK_TEXT)

prs.save(os.path.join(OUT,"32-enterprise-scaling-playbook.pptx"))
print("  ✓ Saved: 32-enterprise-scaling-playbook.pptx")


# ═══════════════════════════════════════════════════════════════════════════════
# 33 — ELT Executive Dashboard Briefing
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 33-elt-executive-dashboard-briefing.pptx...")
prs=new_prs()

# Slide 1: Cover
sl=blank(prs)
rect(sl,0,0,13.33,7.5,fill=DARK_BLUE)
rect(sl,0,5.2,13.33,2.3,fill=MED_BLUE)
txtbox(sl,"[ORGANISATION NAME]",0.8,0.5,11,0.5,size=16,color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl,"Software Delivery Intelligence",0.8,1.1,11,0.8,size=28,bold=True,color=WHITE)
txtbox(sl,"Monthly ELT Briefing — PDLC VSM Platform",0.8,2.0,11,0.6,size=16,color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl,"[MONTH YEAR]  |  Confidential",0.8,5.6,11,0.5,size=13,color=WHITE)

# Slide 2: Organisation-Wide Scorecard
sl=blank(prs)
header_bar(sl,"Organisation-Wide Delivery Scorecard","[Month Year] — [X] Teams Measured")
for i,(v,l,bg) in enumerate([
    ("[XX] days","Avg Lead Time\nvs. [XX] baseline",DARK_BLUE),
    ("[X]%","Avg Flow Efficiency\nvs. [X]% baseline",MED_BLUE),
    ("[X.X]/5","DORA Score\nvs. [X.X] baseline",DARK_BLUE),
    ("$[X.X]M","Benefits Realised\nYear-to-date",MED_BLUE),
]):
    stat_box(sl,0.5+i*3.2,1.3,2.8,1.5,v,l,bg)
txtbox(sl,"Month-on-month: Lead Time [▼/▲X days]  |  Flow Efficiency [▼/▲X%]  |  DORA Score [▼/▲X.X]  |  Quick Wins Complete [X of X]",0.5,3.0,12.3,0.5,size=10,bold=True,color=MED_BLUE,align=PP_ALIGN.CENTER)
txtbox(sl,"Team",0.4,3.65,1.5,0.4,size=9,bold=True,color=DARK_TEXT)
for j,col in enumerate(["LT (days)","FE (%)","DORA","QWs Done","Status"]):
    txtbox(sl,col,2.0+j*2.1,3.65,1.8,0.4,size=9,bold=True,color=DARK_TEXT)
for i,team in enumerate(["[Team 1]","[Team 2]","[Team 3]","[Team 4]","[Team 5]"]):
    y=4.1+i*0.5
    rect(sl,0.4,y,12.8,0.45,fill=LIGHT_BLUE if i%2==0 else WHITE)
    txtbox(sl,team,0.4,y,1.5,0.42,size=9,color=DARK_TEXT)
    for j,val in enumerate(["[X]","[X]%","[X.X]","[X]/[X]","[✓/○]"]):
        txtbox(sl,val,2.0+j*2.1,y,1.8,0.42,size=9,color=DARK_TEXT)

# Slide 3: Top Insights This Month
sl=blank(prs)
header_bar(sl,"Top 3 AI Insights This Month","Actions Required from ELT")
for i,(insight,action,owner) in enumerate([
    ("[Team X] Phase 5 wait time increased +40h vs. last month — new UAT dependency detected",
     "Approve AI UAT Assistant Quick Win ($45K, 6-week delivery)",
     "[CTO / VP Eng]"),
    ("[Team Y] DORA band dropped from WALK to CRAWL on Continuous Testing — coverage fell to 34%",
     "Schedule sprint to address test coverage; assign dedicated QA sprint",
     "[VP Eng]"),
    ("Portfolio-wide: Architecture Review Gate is the #1 bottleneck across 4 of 5 teams (172h average WT)",
     "Initiate Architecture Review Streamlining programme (included in Option B business case)",
     "[CTO]"),
]):
    y=1.3+i*1.9
    rect(sl,0.3,y,0.5,1.6,fill=MED_BLUE)
    txtbox(sl,str(i+1),0.3,y,0.5,1.6,size=18,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,f"Finding: {insight}",1.0,y+0.05,11.8,0.65,size=11,bold=True,color=DARK_TEXT)
    txtbox(sl,f"Action: {action}",1.0,y+0.75,11.8,0.5,size=10,color=DARK_TEXT)
    txtbox(sl,f"Owner: {owner}",1.0,y+1.3,11.8,0.4,size=9,italic=True,color=MED_BLUE)

prs.save(os.path.join(OUT,"33-elt-executive-dashboard-briefing.pptx"))
print("  ✓ Saved: 33-elt-executive-dashboard-briefing.pptx")


# ═══════════════════════════════════════════════════════════════════════════════
# 34 — Annual ROI Review Deck
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 34-annual-roi-review-deck.pptx...")
prs=new_prs()

# Slide 1
sl=blank(prs)
rect(sl,0,0,13.33,7.5,fill=DARK_BLUE)
rect(sl,0,5.2,13.33,2.3,fill=MED_BLUE)
txtbox(sl,"[ORGANISATION NAME]",0.8,0.4,11,0.5,size=16,color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl,"Year 1 ROI Review",0.8,1.0,11,0.9,size=32,bold=True,color=WHITE)
txtbox(sl,"PDLC VSM Platform — Board / ELT Annual Review",0.8,2.1,11,0.6,size=16,color=RGBColor(0xBF,0xDB,0xFE))
txtbox(sl,"[YEAR]  |  Board Confidential",0.8,5.6,11,0.5,size=13,color=WHITE)

# Slide 2: Executive Summary
sl=blank(prs)
header_bar(sl,"Year 1 Executive Summary","From Baseline to Transformation — 12 Months of AI-Powered Flow Intelligence")
for i,(v,l) in enumerate([("[X.X]×","Year 1 ROI\nvs. [X.X]× target"),("[−X] days","Lead Time Reduction\nfrom [XX] to [XX] days"),("+[X]%","Flow Efficiency\nfrom [X]% to [X]%")]):
    stat_box(sl,0.4+i*4.3,1.25,4.0,1.6,v,l,DARK_BLUE if i%2==0 else MED_BLUE)
findings = [
    "[$X.XM] total savings realised vs. [$X.XM] investment — [X.X]× actual ROI",
    "[X] teams measured across [X] portfolios — [X]% of engineering headcount covered",
    "[X] Quick Wins completed — average lead time reduction [X] days per team",
    "DORA average improved from [X.X] to [X.X] (WALK → RUN band for [X] teams)",
    "Business case for Year 2: expand to [X] teams, target [$XM] additional savings",
]
for i,finding in enumerate(findings):
    txtbox(sl,f"• {finding}",0.5,3.1+i*0.6,12.3,0.55,size=10,color=DARK_TEXT)

# Slide 3: Financial Summary
sl=blank(prs)
header_bar(sl,"Financial Summary","Planned vs. Actual — Year 1 Investment and Returns")
tbl2=[["Investment","Planned ($K)","Actual ($K)","Variance"],
      ["Platform licence","[X]","[X]","[±X]"],
      ["Consulting / Pilot Lead","[X]","[X]","[±X]"],
      ["Internal effort (eng + PM)","[X]","[X]","[±X]"],
      ["Training and change mgmt","[X]","[X]","[±X]"],
      ["Total Investment","$[X,XXX]K","$[X,XXX]K","[±X]K"],
      ["","","",""],
      ["Benefits","Planned ($K)","Actual ($K)","Variance"],
      ["Engineering time recovered","[X]","[X]","[±X]"],
      ["Incident reduction","[X]","[X]","[±X]"],
      ["Time-to-market uplift","[X]","[X]","[±X]"],
      ["Total Benefits","$[X,XXX]K","$[X,XXX]K","[±X]K"],
      ["Net ROI","[X.X]×","[X.X]×","[±X.X]×"]]
t=sl.shapes.add_table(len(tbl2),4,Inches(0.4),Inches(1.2),Inches(12.5),Inches(5.5)).table
for ri,row in enumerate(tbl2):
    for ci,val in enumerate(row):
        cell=t.cell(ri,ci)
        cell.text=val
        for para in cell.text_frame.paragraphs:
            for run in para.runs:
                run.font.name="Calibri"; run.font.size=Pt(10)
                if ri in [0,7] or val in ["Total Investment","Total Benefits","Net ROI"]:
                    run.font.bold=True

# Slide 4: Year 2 Recommendation
sl=blank(prs)
header_bar(sl,"Year 2 Recommendation","Expand from [X] to [X] Teams — Target $[XM] Additional Value")
rect(sl,0.3,1.2,12.7,0.6,fill=DARK_BLUE)
txtbox(sl,"Recommendation: Approve Year 2 Scale Investment of $[X.XM] to expand platform coverage to [X] teams and unlock $[XM] additional annual savings",0.4,1.25,12.5,0.5,size=12,bold=True,color=WHITE)
for i,(phase,teams,invest,savings,timeline) in enumerate([
    ("Phase 2a","[X] additional teams","$[X]K","$[X.X]M","Q1–Q2"),
    ("Phase 2b","[X] additional teams","$[X]K","$[X.X]M","Q2–Q3"),
    ("Phase 2c","All remaining teams","$[X]K","$[X.X]M","Q3–Q4"),
]):
    x=0.4+i*4.3
    rect(sl,x,2.1,4.0,4.5,fill=LIGHT_BLUE)
    rect(sl,x,2.1,4.0,0.5,fill=MED_BLUE)
    txtbox(sl,phase,x,2.1,4.0,0.5,size=13,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    for j,(label,val) in enumerate([("Teams",teams),("Investment",invest),("Expected Savings",savings),("Timeline",timeline)]):
        txtbox(sl,label,x+0.2,2.75+j*0.82,1.8,0.4,size=9,color=DARK_TEXT)
        txtbox(sl,val,x+2.0,2.75+j*0.82,1.8,0.5,size=12,bold=True,color=DARK_BLUE)
txtbox(sl,"Board Resolution Required: Approve Year 2 budget allocation of $[X.XM] for PDLC VSM Platform scale expansion",0.4,6.8,12.5,0.5,size=10,italic=True,color=MED_BLUE,align=PP_ALIGN.CENTER)

prs.save(os.path.join(OUT,"34-annual-roi-review-deck.pptx"))
print("  ✓ Saved: 34-annual-roi-review-deck.pptx")


# ═══════════════════════════════════════════════════════════════════════════════
# 35 — Competitive Differentiation Briefing
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 35-competitive-differentiation-briefing.docx...")
d=new_doc()
cover_page(d,"Competitive Differentiation Briefing","How PDLC VSM Platform Compares to Alternatives","DOC-SET3-35")
h1(d,"Market Context")
body(d,"The software delivery intelligence market is growing rapidly as organisations seek to quantify and optimise their engineering throughput. The PDLC VSM Platform operates at the intersection of three established categories: Value Stream Management (VSM), DORA Metrics Tooling, and AI-powered DevOps Intelligence.")

h1(d,"Competitive Landscape")
tbl(d,["Category","Typical Players","PDLC VSM Advantage"],
    [
        ["VSM Platforms","Tasktop (Planview), ConnectALL, Faros AI","7-agent AI pipeline vs. manual VSM; business case builder built-in"],
        ["DORA Metrics Tools","DORA DevOps Quick Check, LinearB, Cortex","73-question deep assessment vs. 4-metric snapshot; links DORA → VSM → action plan"],
        ["AI DevOps Intelligence","Harness AI, Waydev, Swarmia","Full LangGraph agent graph vs. single-agent dashboards; open-source extensible"],
        ["Management Consultants","McKinsey, Deloitte, Accenture","Fraction of the cost ($150K vs. $500K–$2M); continuous vs. one-off; client owns the data"],
        ["Spreadsheet / DIY","Excel, Notion, Confluence","Automated ALM ingestion; 8 AI agents vs. manual analysis; 4-minute run vs. 3-month project"],
    ],col_widths=[2.0,2.5,5.0])

h1(d,"Head-to-Head: PDLC VSM vs. Planview Tasktop")
tbl(d,["Feature","PDLC VSM Platform","Planview Tasktop"],
    [
        ["VSM Methodology","7-phase PDLC model, AI-computed","Manual value stream definition"],
        ["AI Agents","8 LangGraph agents, full pipeline","Limited AI; primarily connectors"],
        ["DORA Assessment","73 questions, automated","Not included"],
        ["Business Case Builder","Automated, 3 scenarios, NPV/ROI","Manual; requires consulting overlay"],
        ["Action Plan","Built-in tracker with AI suggestions","Separate tool or manual"],
        ["Time to Value","4–8 minutes for first VSM","Weeks of configuration"],
        ["Pricing","$150K pilot; POA scale","$500K+ enterprise licence"],
        ["Deployment","Cloud or on-prem, <1 day setup","Enterprise deployment, weeks"],
        ["Open Source","Core platform open-source","Proprietary"],
    ],col_widths=[3.0,3.5,3.0])

h1(d,"Objection Handling: 'We Already Have a Tool'")
for existing, response in [
    ("Jira Dashboards",
     "'Jira shows you ticket counts and sprint velocity — it doesn't show you lead time, flow efficiency, or what's costing you money. PDLC VSM uses your Jira data to answer the question Jira can't: how much of the time is your team actually working?'"),
    ("Atlassian Analytics / Advanced Roadmaps",
     "'Advanced Roadmaps is a planning tool. PDLC VSM is a diagnostic tool. They're complementary — we import from Jira and add AI analysis on top.'"),
    ("LinearB / Swarmia",
     "'LinearB tracks DORA metrics. We track DORA metrics AND value stream waste AND generate a board-ready business case with a click. It's the difference between a speedometer and a full diagnostic.'"),
    ("Custom Power BI Dashboard",
     "'Custom dashboards require ongoing maintenance and don't include AI-generated bottleneck analysis or improvement recommendations. PDLC VSM gives you the AI layer on top of your existing data.'"),
]:
    h3(d,f"If they have: {existing}")
    body(d,response,italic=True)

d.save(os.path.join(OUT,"35-competitive-differentiation-briefing.docx"))
print("  ✓ Saved: 35-competitive-differentiation-briefing.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# 36 — Master Index for All 3 Sets
# ═══════════════════════════════════════════════════════════════════════════════
print("Building 00-MASTER-INDEX.docx...")
d=new_doc()
p=d.add_paragraph(); p.paragraph_format.space_before=DPt(30)
r=p.add_run("PDLC VSM Platform"); sf(r,16,bold=True,color=DBLUE)
p=d.add_paragraph()
r=p.add_run("GTM Pack — Complete Master Index"); sf(r,22,bold=True,color=DNAVY)
p=d.add_paragraph()
r=p.add_run("All 36 documents across 3 sets — CXO GTM, Pilot Engagement, and Scale Implementation"); sf(r,12,italic=True,color=DBLUE)
d.add_paragraph(); divider(d)
tbl(d,["Set","File","Title","Format","Audience"],
    [
        # Set 1
        ["Set 1","01-cxo-pitch-deck.pptx","CXO Pitch Deck (18 slides)","PPTX","CTO, CDO, COO"],
        ["Set 1","01b-offering-slide.pptx","Offering Overview Slide","PPTX","CXO meeting opening"],
        ["Set 1","02-cxo-question-bank.docx","CXO Discovery Question Bank","DOCX","Account Executive"],
        ["Set 1","03-service-brief-one-pager.docx","Service Brief One-Pager","DOCX","Leave-behind"],
        ["Set 1","04-thought-leadership-whitepaper.docx","Thought Leadership Whitepaper","DOCX","CTO / VP Eng"],
        ["Set 1","05-roi-calculator-guide.docx","ROI Calculator Guide","DOCX","CFO / Finance"],
        ["Set 1","06-industry-benchmark-report.docx","Industry Benchmark Report","DOCX","CTO / Head of DevOps"],
        ["Set 1","07-case-study-usbank.docx","Case Study: US Bank","DOCX","All audiences"],
        ["Set 1","08-commercial-model-pricing.docx","Commercial Model & Pricing","DOCX","Procurement / Finance"],
        ["Set 1","09-engagement-model-overview.docx","Engagement Model Overview","DOCX","Client PM / Sponsor"],
        ["Set 1","10-demo-script-guide.docx","Demo Script & Guide","DOCX","Sales / Pilot Lead"],
        # Set 2
        ["Set 2","11-pilot-proposal-template.docx","Pilot Proposal Template","DOCX","Sponsor / Procurement"],
        ["Set 2","12-project-charter.docx","Project Charter","DOCX","All stakeholders"],
        ["Set 2","13-pilot-delivery-runbook.docx","Pilot Delivery Runbook","DOCX","Pilot Lead"],
        ["Set 2","14-raci-matrix.docx","RACI Matrix","DOCX","Project team"],
        ["Set 2","15-pilot-findings-readout.pptx","Pilot Findings Readout (8 slides)","PPTX","ELT / Board"],
        ["Set 2","16-discovery-questionnaire.docx","Discovery Questionnaire","DOCX","Client PM (pre-kick-off)"],
        ["Set 2","17-kickoff-meeting-guide.docx","Kick-off Meeting Guide","DOCX","Pilot Lead"],
        ["Set 2","18-ai-evidence-protocol.docx","AI Evidence Protocol","DOCX","Insight Analyst / Legal"],
        ["Set 2","19-risk-register.docx","Risk Register","DOCX","Pilot Lead / PM"],
        ["Set 2","20-pilot-success-scorecard.docx","Pilot Success Scorecard","DOCX","Pilot Lead + Client PM"],
        ["Set 2","21-pilot-to-scale-framework.docx","Pilot-to-Scale Framework","DOCX","Sponsor / CTO"],
        ["Set 2","22-scale-proposal-deck.pptx","Scale Proposal Deck (5 slides)","PPTX","ELT / Sponsor"],
        # Set 3
        ["Set 3","23-platform-methodology-guide.docx","Platform Methodology Guide","DOCX","Technical practitioners"],
        ["Set 3","24-governance-model.docx","Enterprise Governance Model","DOCX","CTO / Data Governance"],
        ["Set 3","25-change-management-plan.docx","Change Management Plan","DOCX","HR / Transformation"],
        ["Set 3","26-platform-configuration-playbook.docx","Platform Configuration Playbook","DOCX","Platform Admins"],
        ["Set 3","27-integration-architecture-guide.docx","Integration Architecture Guide","DOCX","IT Architects"],
        ["Set 3","28-scale-training-curriculum.docx","Scale Training Curriculum","DOCX","L&D / Platform Admins"],
        ["Set 3","29-adoption-playbook.docx","Adoption Playbook","DOCX","Programme Lead"],
        ["Set 3","30-qa-framework.docx","QA Framework","DOCX","Insight Analyst / QA"],
        ["Set 3","31-benefits-tracker-template.docx","Benefits Tracker Template","DOCX","Finance / CFO"],
        ["Set 3","32-enterprise-scaling-playbook.pptx","Enterprise Scaling Playbook (5 slides)","PPTX","ELT / Sponsor"],
        ["Set 3","33-elt-executive-dashboard-briefing.pptx","ELT Dashboard Briefing (3 slides)","PPTX","ELT Monthly"],
        ["Set 3","34-annual-roi-review-deck.pptx","Annual ROI Review Deck (4 slides)","PPTX","Board / ELT Annual"],
        ["Set 3","35-competitive-differentiation-briefing.docx","Competitive Differentiation Briefing","DOCX","Sales / Pilot Lead"],
    ],col_widths=[0.8,3.2,2.5,0.8,2.2])

d.add_page_break()
h1(d,"GTM Pack Usage Guide")
h2(d,"When to Use Each Set")
tbl(d,["Scenario","Recommended Documents"],
    [
        ["First meeting with CTO (cold outreach)","Set 1: 01-cxo-pitch-deck, 03-service-brief-one-pager"],
        ["CXO discovery call (30 min)","Set 1: 02-cxo-question-bank, 04-thought-leadership-whitepaper"],
        ["CFO meeting (business case focus)","Set 1: 05-roi-calculator-guide, 07-case-study-usbank"],
        ["Competitive evaluation","Set 3: 35-competitive-differentiation-briefing"],
        ["Proposal submission","Set 2: 11-pilot-proposal-template, 12-project-charter"],
        ["Kick-off meeting","Set 2: 13-pilot-delivery-runbook, 14-raci-matrix, 16-discovery-questionnaire, 17-kickoff-meeting-guide"],
        ["Executive readout (pilot end)","Set 2: 15-pilot-findings-readout, 18-ai-evidence-protocol"],
        ["Scale proposal","Set 2: 21-pilot-to-scale-framework, 22-scale-proposal-deck"],
        ["Enterprise deployment","Set 3: 23 through 31 (full set)"],
        ["Annual board review","Set 3: 34-annual-roi-review-deck, 31-benefits-tracker-template"],
    ],col_widths=[3.5,6.0])

d.save(os.path.join(OUT,"00-MASTER-INDEX.docx"))
print("  ✓ Saved: 00-MASTER-INDEX.docx")


# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════
files=sorted(os.listdir(OUT))
print(f"\n✓ All Set 3 files complete. {len(files)} files in {OUT}:")
for f in files:
    size=os.path.getsize(os.path.join(OUT,f))
    print(f"  {f} ({size//1024}KB)")
