"""Build Set 1 — CXO GTM Pack for PDLC VSM Platform"""
import os
OUT = "/Users/125066/projects/pdlc-vsm-platform/gtm-pack/set1-cxo-gtm-pack"
os.makedirs(OUT, exist_ok=True)

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pptx import Presentation
from pptx.util import Pt as PPt, Emu, Inches as PInches
from pptx.dml.color import RGBColor as PRGB
from pptx.enum.text import PP_ALIGN

# ── Colors ──────────────────────────────────────────────────────────
NAVY  = RGBColor(0x0F,0x2D,0x5E); BLUE  = RGBColor(0x25,0x63,0xEB)
TEAL  = RGBColor(0x0D,0x94,0x88); GRAY  = RGBColor(0x4B,0x55,0x63)
WHITE = RGBColor(0xFF,0xFF,0xFF); LGRAY = RGBColor(0xF3,0xF4,0xF6)

P_DARK  = PRGB(0x0F,0x2D,0x5E); P_MED   = PRGB(0x25,0x63,0xEB)
P_LIGHT = PRGB(0xDB,0xEA,0xFE); P_ACC   = PRGB(0x0D,0x94,0x88)
P_TEXT  = PRGB(0x1E,0x29,0x3B); P_WHITE = PRGB(0xFF,0xFF,0xFF)
P_MID   = PRGB(0x1E,0x40,0x8A); P_PALE  = PRGB(0xEF,0xF6,0xFF)
W=13333750; H=7500000

# ══════════════════════════════════════════════════════════════════
# DOCX HELPERS
# ══════════════════════════════════════════════════════════════════
def new_doc():
    d=Document(); s=d.sections[0]
    s.page_width=Inches(8.5); s.page_height=Inches(11)
    s.left_margin=s.right_margin=Inches(1.0)
    s.top_margin=s.bottom_margin=Inches(0.9)
    return d

def sf(run,size=11,bold=False,italic=False,color=None,name='Calibri'):
    run.font.name=name; run.font.size=Pt(size)
    run.font.bold=bold; run.font.italic=italic
    if color: run.font.color.rgb=color

def h1(d,text):
    p=d.add_paragraph(); p.paragraph_format.space_before=Pt(20); p.paragraph_format.space_after=Pt(6)
    r=p.add_run(text); sf(r,20,True,color=NAVY); return p

def h2(d,text):
    p=d.add_paragraph(); p.paragraph_format.space_before=Pt(12); p.paragraph_format.space_after=Pt(4)
    r=p.add_run(text); sf(r,14,True,color=BLUE); return p

def h3(d,text):
    p=d.add_paragraph(); p.paragraph_format.space_before=Pt(8); p.paragraph_format.space_after=Pt(3)
    r=p.add_run(text); sf(r,12,True,color=TEAL); return p

def body(d,text,italic=False):
    p=d.add_paragraph(); p.paragraph_format.space_after=Pt(4)
    r=p.add_run(text); sf(r,10.5,italic=italic); return p

def bul(d,text,level=0,bold_pre=None):
    p=d.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent=Inches(0.3+level*0.2); p.paragraph_format.space_after=Pt(2)
    if bold_pre:
        rb=p.add_run(bold_pre+": "); sf(rb,10.5,True)
    r=p.add_run(text); sf(r,10.5); return p

def set_bg(cell,hex_c):
    tc=cell._tc; tcPr=tc.get_or_add_tcPr()
    shd=OxmlElement('w:shd'); shd.set(qn('w:val'),'clear')
    shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),hex_c); tcPr.append(shd)

def tbl(d,headers,rows,widths=None):
    t=d.add_table(rows=1,cols=len(headers)); t.style='Table Grid'
    hr=t.rows[0]
    for i,h in enumerate(headers):
        c=hr.cells[i]; set_bg(c,'0F2D5E')
        p=c.paragraphs[0]; r=p.add_run(h); sf(r,9.5,True,color=WHITE)
    for rd in rows:
        row=t.add_row()
        for i,v in enumerate(rd):
            r=row.cells[i].paragraphs[0].add_run(str(v)); sf(r,9.5)
    if widths:
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Inches(w)
    d.add_paragraph(); return t

def divider(d):
    p=d.add_paragraph(); p.paragraph_format.space_before=Pt(3); p.paragraph_format.space_after=Pt(3)
    pPr=p._p.get_or_add_pPr(); pBdr=OxmlElement('w:pBdr')
    bot=OxmlElement('w:bottom'); bot.set(qn('w:val'),'single'); bot.set(qn('w:sz'),'6')
    bot.set(qn('w:space'),'1'); bot.set(qn('w:color'),'2563EB')
    pBdr.append(bot); pPr.append(pBdr)

def callout(d,title,lines,fill='FEF3C7',tc=AMBER if False else None):
    t=d.add_table(rows=1,cols=1); t.style='Table Grid'
    c=t.rows[0].cells[0]; set_bg(c,fill)
    p=c.paragraphs[0]; rb=p.add_run(title+"  "); sf(rb,10,True,color=BLUE)
    for ln in (lines if isinstance(lines,list) else [lines]):
        p2=c.add_paragraph(); r=p2.add_run(ln); sf(r,10)
    d.add_paragraph()

# ══════════════════════════════════════════════════════════════════
# PPTX HELPERS
# ══════════════════════════════════════════════════════════════════
def new_prs():
    p=Presentation(); p.slide_width=W; p.slide_height=H; return p

def blank(prs):
    sl=prs.slides.add_slide(prs.slide_layouts[6])
    bg=sl.background; f=bg.fill; f.solid(); f.fore_color.rgb=P_WHITE
    return sl

def rect(sl,l,t,w,h,col,border=False):
    s=sl.shapes.add_shape(1,l,t,w,h)
    s.fill.solid(); s.fill.fore_color.rgb=col
    if not border: s.line.fill.background()
    return s

def txtbox(sl,txt,l,t,w,h,sz=11,bold=False,col=P_TEXT,align=PP_ALIGN.LEFT,italic=False):
    tb=sl.shapes.add_textbox(l,t,w,h); tf=tb.text_frame; tf.word_wrap=True
    p=tf.paragraphs[0]; p.alignment=align; r=p.add_run()
    r.text=txt; r.font.size=PPt(sz); r.font.bold=bold; r.font.italic=italic
    r.font.color.rgb=col; r.font.name='Calibri'; return tb

def multiline_tb(sl,lines,l,t,w,h,sz=10,col=P_TEXT,bold_first=False):
    tb=sl.shapes.add_textbox(l,t,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,(line,bd) in enumerate(lines):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        r=p.add_run(); r.text=line; r.font.size=PPt(sz)
        r.font.bold=bd; r.font.color.rgb=col; r.font.name='Calibri'
        p.space_after=PPt(3)
    return tb

def header_bar(sl,title):
    rect(sl,0,0,W,240000,P_DARK)
    txtbox(sl,title,350000,260000,W-700000,460000,sz=20,bold=True,col=P_DARK)

def stat_box(sl,stat,label,l,t,w,h):
    rect(sl,l,t,w,h,P_LIGHT)
    txtbox(sl,stat,l+80000,t+80000,w-160000,h//2,sz=28,bold=True,col=P_DARK,align=PP_ALIGN.CENTER)
    txtbox(sl,label,l+60000,t+h//2,w-120000,h//2,sz=10,col=P_DARK,align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# FILE 1: CXO PITCH DECK (18 slides)
# ══════════════════════════════════════════════════════════════════
print("Building 01-cxo-pitch-deck.pptx...")
prs=new_prs()

# Slide 1 — Title
sl=blank(prs)
rect(sl,0,0,W,H//3,P_DARK)
txtbox(sl,"PDLC VSM PLATFORM",350000,200000,W-700000,600000,sz=40,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
txtbox(sl,"From 42-Day Lead Time to 8 Days in 18 Months",350000,820000,W-700000,400000,sz=22,col=P_LIGHT,align=PP_ALIGN.CENTER,italic=True)
txtbox(sl,"AI-Powered Value Stream Transformation for Engineering Organisations",350000,1220000,W-700000,300000,sz=14,col=P_LIGHT,align=PP_ALIGN.CENTER)
bw=3800000; bh=700000; by=H//3+400000; gap=200000; bx0=(W-3*bw-2*gap)//2
for i,(s,l) in enumerate([("42→8 Days","Lead Time Reduction"),("8%→61%","Flow Efficiency"),("4.2× ROI","14-Month Payback")]):
    bx=bx0+i*(bw+gap); rect(sl,bx,by,bw,bh,P_LIGHT)
    txtbox(sl,s,bx+80000,by+80000,bw-160000,320000,sz=24,bold=True,col=P_DARK,align=PP_ALIGN.CENTER)
    txtbox(sl,l,bx+80000,by+400000,bw-160000,220000,sz=11,col=P_DARK,align=PP_ALIGN.CENTER)

# Slide 2 — Burning Platform
sl=blank(prs); header_bar(sl,"The Window for Transformation Leadership Is Narrowing")
cols=[("THE PRESSURE",["73% of CTOs cite delivery speed as #1 concern","Boards demand ROI on transformation in 12–18 months","AI-native competitors shipping 3× faster"]),
      ("THE GAP",["Average team flow efficiency = 17% (world-class = 40%+)","9–14 months to produce a transformation plan","Only 23% of teams can quantify PDLC waste in hours"]),
      ("THE COST",["$47M average wasted per failed transformation","2–4% revenue share lost per year of delay","80%+ of lead time is invisible, unquantified wait time"])]
cw=3900000; ch=4200000; cy=900000; cx0=350000
for i,(hdr,pts) in enumerate(cols):
    cx=cx0+i*(cw+200000); rect(sl,cx,cy,cw,ch,P_LIGHT)
    rect(sl,cx,cy,cw,380000,P_DARK)
    txtbox(sl,hdr,cx+120000,cy+100000,cw-240000,220000,sz=13,bold=True,col=P_WHITE)
    for j,pt in enumerate(pts):
        txtbox(sl,"• "+pt,cx+120000,cy+450000+j*380000,cw-240000,340000,sz=10.5,col=P_TEXT)

# Slide 3 — The Problem
sl=blank(prs); header_bar(sl,"Traditional Approaches Cannot See the Waste")
chain="[ALM Data]  →  ???  →  [Insight]  →  ???  →  [Plan]  →  ???  →  [ROI]"
txtbox(sl,chain,350000,800000,W-700000,300000,sz=16,bold=True,col=P_DARK,align=PP_ALIGN.CENTER)
txtbox(sl,"At every arrow: data is locked in siloed tools, insights are consultant opinion, plans lack financial grounding",350000,1150000,W-700000,300000,sz=11,col=P_TEXT,align=PP_ALIGN.CENTER,italic=True)
pains=[("No baseline","Teams cannot quantify how much of their lead time is waste — they guess"),
       ("No calibration","DORA metrics sit in dashboards, disconnected from VSM phase data"),
       ("No prioritisation","Bottleneck identification is workshop opinion, not AI-driven analysis"),
       ("No financial case","Improvement ideas lack ROI, payback, or NPV — finance rejects them"),
       ("No playbook","Even great plans fail without a compliance-aware implementation guide")]
for i,(ttl,desc) in enumerate(pains):
    y=1700000+i*900000; rect(sl,350000,y,W-700000,750000,P_PALE)
    txtbox(sl,ttl,500000,y+80000,2000000,500000,sz=13,bold=True,col=P_DARK)
    txtbox(sl,desc,2600000,y+80000,W-3200000,500000,sz=11,col=P_TEXT)

# Slide 4 — Solution
sl=blank(prs); header_bar(sl,"The PDLC VSM Platform: See It, Measure It, Fix It")
flow="[1. ALM Connect] → [2. DORA Assessment] → [3. Current State VSM] → [4. VSM Editor]\n                                                                              ↓\n[9. Playbook] ← [8. Business Case] ← [7. Future State VSM] ← [5/6. Bottlenecks + Improvements]"
rect(sl,350000,800000,W-700000,1400000,P_PALE)
txtbox(sl,flow,550000,900000,W-1100000,1200000,sz=11,bold=True,col=P_DARK)
diffs=[("AI-Powered","8 LangGraph agents run automatically — no manual data wrangling"),
       ("Evidence-Based","Every recommendation is benchmarked against industry data"),
       ("Finance-Ready","Business case with ROI, payback, NPV ready for the CFO in minutes")]
bw2=3600000; bh2=900000; by2=2600000
for i,(ttl,desc) in enumerate(diffs):
    bx=350000+i*(bw2+200000); rect(sl,bx,by2,bw2,bh2,P_LIGHT)
    rect(sl,bx,by2,bw2,280000,P_MED)
    txtbox(sl,ttl,bx+120000,by2+60000,bw2-240000,200000,sz=13,bold=True,col=P_WHITE)
    txtbox(sl,desc,bx+120000,by2+340000,bw2-240000,480000,sz=10.5,col=P_TEXT)

# Slide 5 — 8 Agents
sl=blank(prs); header_bar(sl,"8 AI Agents. One Seamless Pipeline.")
agents=[("ALM Connector","Ingests CSV/API data from Jira, ADO, Rally — maps to 7 PDLC phases"),
        ("VSM Analyzer","Computes PT, WT, FE% per phase — generates executive narrative"),
        ("Benchmark Agent","Compares team metrics against industry benchmarks (FSI, Healthcare, Telecoms)"),
        ("Bottleneck Analyzer","Identifies top flow impediments with severity, root cause, lean waste type"),
        ("Improvement Generator","Maps 36 AI agents to each bottleneck — with ROI and quick-win flags"),
        ("Future State Designer","Models 3 transformation scenarios (Option A/B/C) with projected metrics"),
        ("Business Case Builder","Builds full financial model: ROI, payback period, 5-year NPV"),
        ("Playbook Contextualizer","Generates personalised implementation guide from your uploaded docs")]
aw=5800000; ah=500000; ax0=350000; ay0=850000
for i,(nm,desc) in enumerate(agents):
    col_idx=i%2; row_idx=i//2; ax=ax0+col_idx*(aw+300000); ay=ay0+row_idx*640000
    rect(sl,ax,ay,aw,ah,P_PALE)
    rect(sl,ax,ay,320000,ah,P_MED)
    txtbox(sl,str(i+1),ax+80000,ay+140000,200000,280000,sz=14,bold=True,col=P_WHITE)
    txtbox(sl,nm,ax+380000,ay+60000,1800000,280000,sz=12,bold=True,col=P_DARK)
    txtbox(sl,desc,ax+380000,ay+300000,aw-500000,200000,sz=9.5,col=P_TEXT)

# Slide 6 — Current State VSM
sl=blank(prs); header_bar(sl,"See Exactly Where Your PDLC Is Losing Time — US Bank / Team Phoenix")
phases=[("Backlog & Roadmap","25","72","25.8%","Amber"),("Architecture & UX","36","176","17.0%","Red"),
        ("Code Management","13","18","41.9%","Green"),("Continuous Integration","6","8","42.9%","Green"),
        ("Continuous Testing","31","240","11.4%","Red"),("Continuous Delivery","12","56","17.6%","Red"),
        ("Monitoring & Feedback","7","30","18.9%","Amber"),("TOTAL","130","600","17.8%","RED")]
hdrs=["Phase","PT (hours)","WT (hours)","Flow Efficiency","Signal"]
cw_=[3800000,1400000,1400000,1600000,1200000]; cy=850000; hh=340000
# header row
rect(sl,350000,cy,sum(cw_),hh,P_DARK)
cx=350000
for i,(h,w) in enumerate(zip(hdrs,cw_)):
    txtbox(sl,h,cx+80000,cy+80000,w-160000,200000,sz=11,bold=True,col=P_WHITE); cx+=w
for row_i,(ph,pt,wt,fe,sig) in enumerate(phases):
    ry=cy+hh+(row_i*350000); bg=P_PALE if row_i%2==0 else P_LIGHT
    if ph=="TOTAL": bg=P_DARK
    rect(sl,350000,ry,sum(cw_),320000,bg)
    vals=[ph,pt,wt,fe,sig]; cx2=350000
    tc=P_WHITE if ph=="TOTAL" else P_TEXT
    for v,w in zip(vals,cw_):
        txtbox(sl,v,cx2+80000,ry+80000,w-160000,200000,sz=10,bold=(ph=="TOTAL"),col=tc); cx2+=w
txtbox(sl,"Total Lead Time: 46.4 days  |  80%+ of time is non-value-adding wait",350000,H-600000,W-700000,300000,sz=11,bold=True,col=P_MED,align=PP_ALIGN.CENTER)

# Slide 7 — DORA
sl=blank(prs); header_bar(sl,"73 Questions. 4 Dimensions. DORA-Calibrated VSM.")
dims=[("Cultural Practices","18 Qs","Team autonomy, safety, learning culture"),
      ("Measurement & Monitoring","20 Qs","Observability, SLOs, dashboards"),
      ("Process & Flow","18 Qs","Sprint cadence, WIP, deployment process"),
      ("Technical Practices","17 Qs","CI/CD, test automation, security gates")]
dw=2900000; dh=900000; dx0=350000; dy=850000
for i,(nm,qs,desc) in enumerate(dims):
    dx=dx0+i*(dw+200000); rect(sl,dx,dy,dw,dh,P_LIGHT)
    rect(sl,dx,dy,dw,280000,P_MED); txtbox(sl,nm,dx+100000,dy+60000,dw-200000,200000,sz=11,bold=True,col=P_WHITE)
    txtbox(sl,qs,dx+100000,dy+330000,dw-200000,200000,sz=20,bold=True,col=P_DARK)
    txtbox(sl,desc,dx+100000,dy+560000,dw-200000,280000,sz=9.5,col=P_TEXT)
txtbox(sl,"DORA → VSM Calibration: How Scores Adjust Your Phase Metrics",350000,1900000,W-700000,280000,sz=13,bold=True,col=P_DARK)
cals=[("Deployment Frequency","Phase 6 WT","Lower freq = higher deploy queue wait"),
      ("Lead Time for Change","Phases 3–6","Proportional WT scaling across code→delivery"),
      ("Change Failure Rate","Phase 5 PT","CFR multiplier on testing rework time"),
      ("MTTR","Phase 7 WT","MTTR hours = monitoring/feedback wait time")]
cy2=2280000
for nm,ph,desc in cals:
    rect(sl,350000,cy2,W-700000,290000,P_PALE)
    txtbox(sl,nm,500000,cy2+60000,2800000,200000,sz=11,bold=True,col=P_DARK)
    txtbox(sl,"→  "+ph,3400000,cy2+60000,1800000,200000,sz=11,bold=True,col=P_MED)
    txtbox(sl,desc,5300000,cy2+60000,W-5700000,200000,sz=10,col=P_TEXT)
    cy2+=340000

# Slide 8 — Bottlenecks
sl=blank(prs); header_bar(sl,"AI Pinpoints Every Bottleneck — Root Cause Included")
btls=[("Critical","Phase 5","Manual SIT / UAT","240h","No parallel execution; manual env setup; test data dependency"),
      ("Critical","Phase 2","Architecture Review Gate","176h","Sequential reviews; 3-day advance scheduling; limited reviewers"),
      ("High","Phase 6","Release Approval / CAB","56h","72h advance CAB notice; manual risk assessment process"),
      ("High","Phase 1","Feature Refinement Loop","48h","Incomplete requirements; stakeholder availability gaps"),
      ("Medium","Phase 3","Peer Code Review Queue","18h","Average PR size 850 lines; 2 senior reviewer bottleneck")]
hdrs2=["Severity","Phase","Activity","Wait Time","Root Cause"]; cw2=[1200000,1000000,2200000,900000,4500000]
cy3=850000; hh2=320000
rect(sl,350000,cy3,sum(cw2),hh2,P_DARK); cx3=350000
for h,w in zip(hdrs2,cw2):
    txtbox(sl,h,cx3+60000,cy3+80000,w-120000,180000,sz=10,bold=True,col=P_WHITE); cx3+=w
SEV_COL={"Critical":PRGB(0x1E,0x3A,0x8A),"High":PRGB(0x1E,0x40,0x8A),"Medium":PRGB(0x25,0x63,0xEB)}
for ri,(sev,ph,act,wt,rc) in enumerate(btls):
    ry=cy3+hh2+ri*440000; bg=P_PALE if ri%2==0 else P_LIGHT
    rect(sl,350000,ry,sum(cw2),410000,bg)
    vals=[sev,ph,act,wt,rc]; cx4=350000
    for j,(v,w) in enumerate(zip(vals,cw2)):
        c=P_DARK if j==0 else P_TEXT
        bd=j==0
        txtbox(sl,v,cx4+60000,ry+100000,w-120000,240000,sz=9.5,bold=bd,col=c); cx4+=w

# Slide 9 — Three Options
sl=blank(prs); header_bar(sl,"Three Transformation Horizons — You Choose the Speed")
attrs=["Horizon","AI Agents Deployed","Flow Efficiency","Lead Time Reduction","Investment","Risk Level","Team Change","DORA Target"]
optA=["12 months","8","~42%","~57%","$1.2M–$1.8M","Low","Augmentation only","High"]
optB=["18 months","15","~61%","~81%","$2.5M–$3.5M","Medium","Hybrid human+AI","High→Elite"]
optC=["24–36 months","22+","~78%","~93%","$4M–$6M","High","AI-first (2 human roles)","Elite"]
cw3=[2600000,2000000,2000000,2000000]; total_w=sum(cw3)
cy5=850000; hh3=320000
rect(sl,350000,cy5,total_w,hh3,P_DARK)
for j,(h,w) in enumerate(zip(["Attribute","Option A — AI Augment","Option B — Hybrid Intel","Option C — ADLC"],cw3)):
    cx5=350000+sum(cw3[:j]); txtbox(sl,h,cx5+60000,cy5+80000,w-120000,200000,sz=11,bold=True,col=P_WHITE)
for ri,(attr,a,b,c) in enumerate(zip(attrs,optA,optB,optC)):
    ry=cy5+hh3+ri*430000; bg=P_PALE if ri%2==0 else P_LIGHT
    rect(sl,350000,ry,total_w,410000,bg)
    for j,(v,w) in enumerate(zip([attr,a,b,c],cw3)):
        cx6=350000+sum(cw3[:j]); bd=j==0
        txtbox(sl,v,cx6+60000,ry+100000,w-120000,240000,sz=10,bold=bd,col=P_DARK if j==0 else P_TEXT)
rect(sl,350000,H-550000,total_w,380000,P_MED)
txtbox(sl,"⭐  Recommended: Option B — Best balance of investment, risk, and transformation impact",500000,H-460000,total_w-400000,280000,sz=11,bold=True,col=P_WHITE)

# Slide 10 — Business Case
sl=blank(prs); header_bar(sl,"Option B: $3M Investment → $31.2M Five-Year NPV")
lw=5500000; rw=5500000; ch=4800000; cy6=800000
rect(sl,350000,cy6,lw,ch,P_PALE)
txtbox(sl,"INVESTMENT BREAKDOWN",450000,cy6+80000,lw-200000,280000,sz=12,bold=True,col=P_DARK)
inv_items=[("Platform licensing (Year 1)","$200,000"),("Implementation & integration","$1,100,000"),
           ("Change management & training","$400,000"),("Infrastructure / cloud delta","$300,000"),("TOTAL YEAR 1 INVESTMENT","$2,000,000")]
iy=cy6+420000
for itm,val in inv_items:
    bd=itm.startswith("TOTAL")
    txtbox(sl,"• "+itm,500000,iy,lw-900000,250000,sz=10,bold=bd,col=P_DARK)
    txtbox(sl,val,lw-400000,iy,380000,250000,sz=10,bold=bd,col=P_MED if bd else P_TEXT,align=PP_ALIGN.RIGHT); iy+=270000
rect(sl,350000+lw+200000,cy6,rw,ch,P_LIGHT)
txtbox(sl,"ANNUAL BENEFITS — OPTION B",350000+lw+300000,cy6+80000,rw-200000,280000,sz=12,bold=True,col=P_DARK)
bens=[("Labour savings (80% FTE automation)","$3.2M"),("Quality improvement (defect reduction)","$1.8M"),
      ("Speed-to-market (faster feature delivery)","$2.1M"),("Risk reduction (compliance/incidents)","$0.9M"),
      ("Platform cost avoidance","$0.4M"),("TOTAL ANNUAL BENEFIT","$8.4M")]
by3=cy6+420000
for itm,val in bens:
    bd=itm.startswith("TOTAL")
    txtbox(sl,"• "+itm,350000+lw+350000,by3,rw-750000,250000,sz=10,bold=bd,col=P_DARK)
    txtbox(sl,val,350000+lw+rw-380000,by3,360000,250000,sz=10,bold=bd,col=P_MED if bd else P_TEXT,align=PP_ALIGN.RIGHT); by3+=270000
stats=[("4.2×","ROI Multiple"),("14 Months","Payback Period"),("$31.2M","5-Year NPV")]
sw=3400000; sy=H-650000
for i,(s,l) in enumerate(stats):
    sx=350000+i*(sw+200000); rect(sl,sx,sy,sw,480000,P_DARK)
    txtbox(sl,s,sx+100000,sy+50000,sw-200000,240000,sz=24,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,l,sx+100000,sy+280000,sw-200000,180000,sz=11,col=P_LIGHT,align=PP_ALIGN.CENTER)

# Slide 11 — Why Us
sl=blank(prs); header_bar(sl,"Purpose-Built for PDLC — Not Adapted From Somewhere Else")
cols2=[("OUR PLATFORM",P_DARK),("MANAGEMENT CONSULTANTS",P_MID),("GENERIC VSM TOOLS",PRGB(0x3B,0x82,0xF6))]
cw4=3800000; cy7=800000
for i,(hdr,hc) in enumerate(cols2):
    cx7=350000+i*(cw4+200000); rect(sl,cx7,cy7,cw4,320000,hc)
    txtbox(sl,hdr,cx7+100000,cy7+70000,cw4-200000,220000,sz=11,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
criteria=[("Quantified baseline","✓ In 2 weeks","✗ 3–4 months","△ Partial"),
          ("DORA calibration","✓ Automated","✗ Manual only","✗ Not included"),
          ("AI bottleneck detection","✓ 8 agents","✗ Consultant opinion","✗ Not included"),
          ("Business case output","✓ Built-in","✓ Expensive add-on","✗ Not included"),
          ("Compliance-aware playbook","✓ RAG-powered","△ Generic templates","✗ Not included"),
          ("Cost","✓ $150K–$1.2M","✗ $2M–$8M","△ $50K–$200K (no services)")]
for ri,(crit,a,b,c) in enumerate(criteria):
    ry=cy7+380000+ri*550000; bg=P_PALE if ri%2==0 else P_LIGHT
    rect(sl,350000,ry,3*cw4+2*200000,520000,bg)
    txtbox(sl,crit,400000,ry+140000,cw4-100000,280000,sz=10.5,bold=True,col=P_DARK)
    for j,v in enumerate([a,b,c]):
        cx8=350000+(j)*(cw4+200000)+(cw4-1200000)//2 if j>0 else 350000+cw4+200000
        if j==0: cx8=350000+cw4+200000
        if j==1: cx8=350000+2*(cw4+200000)
        col_v=P_DARK if v.startswith("✓") else (PRGB(0x9C,0xA3,0xAF) if v.startswith("✗") else P_MED)
        txtbox(sl,v,cx8+200000,ry+140000,cw4-400000,280000,sz=10.5,bold=v.startswith("✓"),col=col_v,align=PP_ALIGN.CENTER)

# Slide 12 — Market
sl=blank(prs); header_bar(sl,"A $12B Market With No Dominant AI-Native Player")
mstats=[("$12B","Total Addressable Market","VSM + DevOps transformation consulting globally"),
        ("$3.2B","Serviceable Addressable Market","AI-augmented delivery transformation — FSI, Healthcare, Telecoms"),
        ("$180M","Year 3 Target","Conservative 5.6% SAM capture in priority sectors")]
mw=3800000; mh=1600000; my=800000
for i,(s,l,d) in enumerate(mstats):
    mx=350000+i*(mw+200000); rect(sl,mx,my,mw,mh,P_PALE)
    rect(sl,mx,my,mw,280000,P_DARK)
    txtbox(sl,l,mx+100000,my+60000,mw-200000,200000,sz=11,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,s,mx+100000,my+340000,mw-200000,500000,sz=32,bold=True,col=P_DARK,align=PP_ALIGN.CENTER)
    txtbox(sl,d,mx+100000,my+880000,mw-200000,640000,sz=10,col=P_TEXT,align=PP_ALIGN.CENTER)
txtbox(sl,"Market Drivers:",350000,2600000,W-700000,250000,sz=13,bold=True,col=P_DARK)
drivers=["AI adoption pressure: 78% of CTOs have a board mandate to deploy AI in engineering in 2026","Regulatory compliance: DORA (Digital Operational Resilience Act) driving measurement requirements in FSI","DORA framework adoption: Gartner predicts 85% of enterprises will formally measure DORA metrics by 2027","Cost pressure: $47M average wasted per failed transformation creates urgent demand for evidence-based approaches"]
for i,d in enumerate(drivers):
    txtbox(sl,"• "+d,350000,2900000+i*350000,W-700000,300000,sz=10.5,col=P_TEXT)

# Slide 13 — Personas
sl=blank(prs); header_bar(sl,"Four Buyer Personas. One Platform.")
personas=[("CTO","'How do I prove AI is improving delivery speed?'","Lead time reduction proof / DORA Elite path / Board-ready metrics"),
          ("VP Engineering","'My team is overwhelmed — where do I focus?'","Bottleneck prioritisation / Quick wins in 90 days / Agent deployment roadmap"),
          ("CDO","'What data do I need to drive transformation?'","VSM data as transformation evidence / Benchmark comparison / Continuous monitoring"),
          ("COO","'What's the ROI and when do I see payback?'","Business case financials / 14-month payback / 5-year NPV / Benefits by stream")]
pw=5600000; ph=1900000; py=800000; px0=350000
for i,(role,pain,resonates) in enumerate(personas):
    col_i=i%2; row_i=i//2; px=px0+col_i*(pw+200000); py2=py+row_i*(ph+200000)
    rect(sl,px,py2,pw,ph,P_PALE)
    rect(sl,px,py2,pw,280000,P_MED)
    txtbox(sl,role,px+120000,py2+60000,pw-240000,200000,sz=14,bold=True,col=P_WHITE)
    txtbox(sl,pain,px+120000,py2+350000,pw-240000,360000,sz=11,italic=True,col=P_DARK)
    txtbox(sl,"Resonates: "+resonates,px+120000,py2+760000,pw-240000,500000,sz=10,col=P_TEXT)

# Slide 14 — Engagement Model
sl=blank(prs); header_bar(sl,"Three Phases. Eighteen Months. Measurable Value at Every Gate.")
phases_eng=[("PHASE 1\nASSESS","4 Weeks","$150K",["ALM data ingestion & VSM baseline","DORA 73-question assessment","Current state VSM + benchmarks","Top 5 bottlenecks identified","Business case for transformation"]),
            ("PHASE 2\nTRANSFORM","12 Weeks","$450K",["Quick wins deployed (8 agents)","Full future state VSM modelled","Implementation roadmap finalised","Change management programme","Ongoing coaching & review gates"]),
            ("PHASE 3\nSCALE","Ongoing","$200K/qtr",["Multi-team VSM rollout","Centre of Excellence setup","Continuous DORA monitoring","Benefits realisation tracking","Portfolio-level VSM aggregation"])]
ew=3700000; eh=5000000; ey=800000; ex0=350000
for i,(nm,dur,inv,dlvrs) in enumerate(phases_eng):
    ex=ex0+i*(ew+300000); rect(sl,ex,ey,ew,eh,P_PALE)
    rect(sl,ex,ey,ew,600000,P_DARK)
    txtbox(sl,nm,ex+100000,ey+80000,ew-200000,480000,sz=14,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,dur+" | "+inv,ex+100000,ey+680000,ew-200000,250000,sz=12,bold=True,col=P_MED,align=PP_ALIGN.CENTER)
    for j,d in enumerate(dlvrs):
        txtbox(sl,"✓  "+d,ex+120000,ey+1000000+j*650000,ew-240000,550000,sz=10,col=P_TEXT)

# Slide 15 — OFFERING SLIDE (replicating reference image layout)
sl=blank(prs)
# Title + teal line
txtbox(sl,"PDLC VSM Transformation",350000,120000,W-700000,380000,sz=22,bold=True,col=P_DARK)
rect(sl,350000,490000,W-700000,50000,P_ACC)
# Row 1: Icon placeholder + description (light blue band)
rect(sl,350000,580000,W-700000,1500000,P_PALE)
txtbox(sl,"⚡",350000,650000,600000,600000,sz=36,col=P_MED,align=PP_ALIGN.CENTER)
txtbox(sl,"Quantify every hour of PDLC waste across 7 phases, identify AI agents for every bottleneck, and deliver a funded transformation roadmap — in 4 weeks. Powered by 8 LangGraph AI agents and benchmarked against industry data.",950000,680000,W-1400000,900000,sz=13,italic=True,col=P_DARK)
# Row 1b: BACKGROUND | TOOLKIT | TIMELINES
r1y=2180000; r1h=1400000; r1cols=[(0.38,"BACKGROUND",["Engineering teams lose 80%+ of lead time to waste","Average PDLC flow efficiency: 17.8% (FSI sector)","Teams cannot quantify waste without VSM","DORA metrics are measured but not actioned"]),
(0.32,"TOOLKIT",["AI-powered VSM canvas (7 phases)","DORA 73-question assessment framework","36-agent improvement catalogue","Financial business case model"]),
(0.30,"TIMELINES",["2–4 weeks: VSM assessment baseline","4–8 weeks: pilot + quick wins","12–18 months: full transformation"])]
cx9=350000
for frac,sec,pts in r1cols:
    sw2=int((W-700000)*frac)
    rect(sl,cx9,r1y,sw2,r1h,P_LIGHT)
    txtbox(sl,sec,cx9+100000,r1y+80000,sw2-200000,240000,sz=10,bold=True,col=P_DARK)
    for j,pt in enumerate(pts):
        txtbox(sl,"• "+pt,cx9+100000,r1y+360000+j*240000,sw2-200000,220000,sz=9,col=P_TEXT)
    cx9+=sw2
# Row 2: MARKET TRENDS | FOCUS AREAS | EXPECTED OUTPUTS | SUCCESS STORY
r2y=3680000; r2h=2000000; r2w=(W-700000)//4
r2data=[("MARKET TRENDS","17.8%","avg flow efficiency in regulated industries — 80%+ of time is waste",""),
        ("FOCUS AREAS","","",["Lean VSM measurement (7 PDLC phases)","DORA maturity assessment (73 Qs)","AI bottleneck identification + root cause","Future state modelling (3 scenarios)","Business case with ROI / payback / NPV"]),
        ("EXPECTED OUTPUTS","","",["Quantified current-state VSM","DORA maturity score + calibration","Top 5 bottleneck cards","3 future-state transformation options","ROI-validated business case"]),
        ("SUCCESS STORY","","",["42→8 day lead time for US Bank Team Phoenix","8.1%→61% flow efficiency in 18 months","4.2× ROI on $3M investment","14-month payback period","$31.2M five-year NPV"])]
cx10=350000
for sec,big,sub,pts in r2data:
    rect(sl,cx10,r2y,r2w,r2h,PRGB(0xF8,0xFA,0xFF))
    rect(sl,cx10,r2y,r2w,260000,P_ACC)
    txtbox(sl,sec,cx10+80000,r2y+60000,r2w-160000,180000,sz=9,bold=True,col=P_WHITE)
    if big:
        txtbox(sl,big,cx10+80000,r2y+320000,r2w-160000,500000,sz=26,bold=True,col=P_DARK)
        txtbox(sl,sub,cx10+80000,r2y+840000,r2w-160000,500000,sz=9,italic=True,col=P_TEXT)
    else:
        for j,pt in enumerate(pts):
            txtbox(sl,"• "+pt,cx10+80000,r2y+320000+j*290000,r2w-160000,260000,sz=8.5,col=P_TEXT)
    cx10+=r2w
# Row 3: OUTCOMES / VALUE DELIVERED
r3y=5780000; r3h=1400000
rect(sl,350000,r3y,W-700000,r3h,P_PALE)
txtbox(sl,"OUTCOMES / VALUE DELIVERED",450000,r3y+80000,3000000,250000,sz=10,bold=True,col=P_DARK)
outcomes=["Lean VSM Baseline","AI Bottleneck Elimination","DORA Maturity Score","Transformation Roadmap","Funded Business Case"]
ow=(W-700000)//5
for i,o in enumerate(outcomes):
    ox=350000+i*ow
    txtbox(sl,"◆",ox+ow//2-150000,r3y+350000,300000,400000,sz=18,bold=True,col=P_MED,align=PP_ALIGN.CENTER)
    txtbox(sl,o,ox+60000,r3y+800000,ow-120000,450000,sz=9,bold=True,col=P_DARK,align=PP_ALIGN.CENTER)

# Slide 16 — Pricing
sl=blank(prs); header_bar(sl,"Simple, Transparent Investment Model")
tiers=[("STARTER","$150,000",["1 team VSM assessment (4 weeks)","DORA 73-question scoring","Current state VSM + benchmarks","Top 5 bottlenecks identified","Business case for transformation","Platform access for 6 months"]),
       ("PROFESSIONAL","$450,000",["Up to 5 teams","Full transformation programme (18 weeks)","All Starter deliverables","Quick wins implementation plan","Future state VSM (3 options)","Change management support","12 months platform access"]),
       ("ENTERPRISE","$1,200,000+",["Enterprise-wide deployment","Unlimited teams","Full Option B transformation","Centre of Excellence setup","Multi-portfolio VSM aggregation","Dedicated advisory support","Unlimited platform access"])]
tw2=3800000; th2=4500000; ty2=800000
for i,(nm,price,feats) in enumerate(tiers):
    tx=350000+i*(tw2+300000); rect(sl,tx,ty2,tw2,th2,P_PALE)
    rect(sl,tx,ty2,tw2,600000,P_DARK if i==1 else P_MID)
    txtbox(sl,nm,tx+100000,ty2+80000,tw2-200000,250000,sz=14,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,price,tx+100000,ty2+330000,tw2-200000,260000,sz=20,bold=True,col=P_LIGHT if i==1 else P_WHITE,align=PP_ALIGN.CENTER)
    for j,f in enumerate(feats):
        txtbox(sl,"✓  "+f,tx+120000,ty2+700000+j*560000,tw2-240000,500000,sz=10,col=P_TEXT)
rect(sl,350000,H-500000,W-700000,370000,P_PALE)
txtbox(sl,"Outcome-based model available: we share in the benefits delivered — aligned incentives, zero upfront risk",500000,H-430000,W-1000000,290000,sz=11,italic=True,col=P_MED,align=PP_ALIGN.CENTER)

# Slide 17 — Timeline Gantt
sl=blank(prs); header_bar(sl,"From Assessment to ROI in 18 Months")
phases_g=[("Foundation & Baseline","████████░░░░░░░░░░░░░░░░","Months 1–3","VSM baseline, DORA, quick win identification"),
          ("Quick Win Deployment","░░░░████████████░░░░░░░░","Months 3–6","8 AI agents deployed, 40% FE improvement"),
          ("Core Transformation","░░░░░░░░████████████░░░░","Months 4–12","15 agents, process change, change management"),
          ("Scale & Embed","░░░░░░░░░░░░░░░░████████","Months 10–18","Multi-team, CoE, portfolio VSM"),
          ("Benefits Realisation","░░░░░░░░████████████████","Months 4–18","ROI tracking, monthly benefits review")]
for ri,(nm,bar,period,desc) in enumerate(phases_g):
    ry=900000+ri*950000; rect(sl,350000,ry,W-700000,830000,P_PALE if ri%2==0 else P_LIGHT)
    txtbox(sl,nm,450000,ry+80000,2800000,280000,sz=11,bold=True,col=P_DARK)
    txtbox(sl,bar,450000,ry+380000,2800000,280000,sz=12,col=P_MED)
    txtbox(sl,period,3350000,ry+80000,1500000,280000,sz=10,bold=True,col=P_MED,align=PP_ALIGN.CENTER)
    txtbox(sl,desc,4950000,ry+80000,W-5400000,650000,sz=10,col=P_TEXT)

# Slide 18 — CTA
sl=blank(prs); header_bar(sl,"Start Your VSM Assessment in 2 Weeks")
txtbox(sl,"Discover your team's flow efficiency baseline — quantified, benchmarked, and ready to present to your board.",350000,800000,W-700000,500000,sz=16,col=P_TEXT,align=PP_ALIGN.CENTER)
steps=[("1","Book a 30-Min Discovery Call","We map your current ALM data and confirm assessment scope"),
       ("2","Upload Your ALM Data","CSV export from Jira, Azure DevOps, or Rally — no integration required"),
       ("3","Receive Your VSM Report","Quantified baseline, DORA score, top 5 bottlenecks, and business case in 2 weeks")]
sw3=3500000; sh=2000000; sy2=1600000
for i,(num,ttl,desc) in enumerate(steps):
    sx2=350000+i*(sw3+300000); rect(sl,sx2,sy2,sw3,sh,P_MED)
    txtbox(sl,num,sx2+sw3//2-200000,sy2+100000,400000,500000,sz=28,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,ttl,sx2+100000,sy2+650000,sw3-200000,400000,sz=13,bold=True,col=P_WHITE,align=PP_ALIGN.CENTER)
    txtbox(sl,desc,sx2+100000,sy2+1100000,sw3-200000,700000,sz=10,col=P_LIGHT,align=PP_ALIGN.CENTER)
txtbox(sl,"contact@pdlc-vsm.com  |  www.pdlc-vsm.com  |  Book via: calendly.com/pdlc-vsm",350000,H-500000,W-700000,350000,sz=12,col=P_TEXT,align=PP_ALIGN.CENTER)

prs.save(f"{OUT}/01-cxo-pitch-deck.pptx")
print("✓ Saved: 01-cxo-pitch-deck.pptx")

# ══════════════════════════════════════════════════════════════════
# FILE 2: OFFERING SLIDE (standalone)
# ══════════════════════════════════════════════════════════════════
print("Building 01b-offering-slide.pptx...")
prs2=new_prs(); sl2=blank(prs2)
# Exact replica of slide 15 above
txtbox(sl2,"PDLC VSM Transformation",350000,80000,W-700000,380000,sz=24,bold=True,col=P_DARK)
rect(sl2,350000,460000,W-700000,60000,P_ACC)
rect(sl2,350000,560000,W-700000,1400000,P_PALE)
txtbox(sl2,"⚡",360000,600000,700000,700000,sz=38,col=P_MED,align=PP_ALIGN.CENTER)
txtbox(sl2,"Quantify every hour of PDLC waste across 7 phases, identify AI agents for every bottleneck, and deliver a funded transformation roadmap — in 4 weeks. Powered by 8 LangGraph AI agents, benchmarked against 2,400+ industry data points.",1100000,620000,W-1600000,900000,sz=13,italic=True,bold=True,col=P_DARK)
# Background/Toolkit/Timelines row
r1y2=2060000; r1h2=1450000
sections=[("BACKGROUND",0.38,["Engineering teams lose 80%+ of lead time to invisible wait","Average FSI team: 17.8% flow efficiency — world-class is 40%+","Teams cannot quantify waste without a VSM baseline","DORA metrics sit in dashboards, not actioned into transformation plans"]),
("TOOLKIT",0.32,["AI-powered 7-phase VSM canvas","DORA 73-question assessment framework","36-agent improvement catalogue","Financial business case model (ROI/payback/NPV)"]),
("TIMELINES",0.30,["2–4 weeks: VSM assessment & baseline","4–8 weeks: DORA + pilot quick wins","12–18 months: full transformation programme"])]
cx11=350000
for sec2,frac2,pts2 in sections:
    sw3b=int((W-700000)*frac2); rect(sl2,cx11,r1y2,sw3b,r1h2,P_LIGHT)
    txtbox(sl2,sec2,cx11+100000,r1y2+80000,sw3b-200000,230000,sz=10,bold=True,col=P_DARK)
    for j,pt in enumerate(pts2):
        txtbox(sl2,"• "+pt,cx11+100000,r1y2+350000+j*250000,sw3b-200000,230000,sz=9.5,col=P_TEXT)
    cx11+=sw3b
# 4-column row
r2y2=3610000; r2h2=2050000; r2w2=(W-700000)//4
r2cols=[("MARKET TRENDS","17.8%","avg flow efficiency in FSI — 83% of time is non-value-adding wait",None),
        ("FOCUS AREAS",None,None,["Lean VSM across 7 PDLC phases","DORA maturity (73 questions)","AI bottleneck identification","Future state modelling (A/B/C)","Funded business case output"]),
        ("EXPECTED OUTPUTS",None,None,["Quantified current-state VSM","DORA score + band + calibration","Top 5 bottleneck cards with root cause","3 future-state VSM scenarios","ROI business case with payback"]),
        ("SUCCESS STORY",None,None,["42→8 day lead time — US Bank Team Phoenix","8.1%→61% flow efficiency in 18 months","4.2× ROI on $3M investment (Option B)","14-month payback | $31.2M 5-yr NPV"])]
cx12=350000
for sec3,big2,sub2,pts3 in r2cols:
    rect(sl2,cx12,r2y2,r2w2,r2h2,PRGB(0xF8,0xFA,0xFF))
    rect(sl2,cx12,r2y2,r2w2,260000,P_ACC)
    txtbox(sl2,sec3,cx12+80000,r2y2+60000,r2w2-160000,190000,sz=9,bold=True,col=P_WHITE)
    if big2:
        txtbox(sl2,big2,cx12+80000,r2y2+320000,r2w2-160000,500000,sz=28,bold=True,col=P_DARK)
        txtbox(sl2,sub2,cx12+80000,r2y2+860000,r2w2-160000,800000,sz=9,italic=True,col=P_TEXT)
    else:
        for j,pt in enumerate(pts3 or []):
            bd2=j==0
            txtbox(sl2,("▶ " if bd2 else "• ")+pt,cx12+80000,r2y2+310000+j*335000,r2w2-160000,300000,sz=8.5,bold=bd2,col=P_DARK if bd2 else P_TEXT)
    cx12+=r2w2
# Outcomes row
r3y2=5760000; r3h2=H-r3y2-100000
rect(sl2,350000,r3y2,W-700000,r3h2,P_PALE)
txtbox(sl2,"OUTCOMES / VALUE DELIVERED",450000,r3y2+80000,3000000,230000,sz=10,bold=True,col=P_DARK)
outs2=["Lean VSM\nBaseline","AI Bottleneck\nElimination","DORA Maturity\nImprovement","Transformation\nRoadmap","Funded\nBusiness Case"]
ow2=(W-700000)//5
for i2,o2 in enumerate(outs2):
    ox2=350000+i2*ow2
    rect(sl2,ox2+100000,r3y2+380000,ow2-200000,r3h2-500000,P_LIGHT)
    txtbox(sl2,o2,ox2+120000,r3y2+420000,ow2-240000,r3h2-600000,sz=10,bold=True,col=P_DARK,align=PP_ALIGN.CENTER)
prs2.save(f"{OUT}/01b-offering-slide.pptx")
print("✓ Saved: 01b-offering-slide.pptx")

# ══════════════════════════════════════════════════════════════════
# FILE 3: CXO QUESTION BANK
# ══════════════════════════════════════════════════════════════════
print("Building 02-cxo-question-bank.docx...")
d=new_doc()
p=d.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("PDLC VSM Platform — CXO Discovery Question Bank"); sf(r,24,True,color=NAVY)
p2=d.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
r2=p2.add_run("20 Questions Across 5 Categories  |  For Sales Engineers & Account Executives"); sf(r2,11,italic=True,color=GRAY)
d.add_paragraph()
body(d,"Use these questions to qualify, discover, and build urgency in CXO-level conversations. Each question includes the purpose (why ask it), what a strong answer looks like, and a follow-up probe to deepen the conversation.")
d.add_paragraph()

categories=[
("1. Delivery Performance Metrics",[
("What is your team's current lead time from feature request to production deployment?",
 "Establishes the baseline — if they know it, they're measurement-mature; if not, that's the pitch.",
 "A strong answer is a specific number (e.g. '42 days'). Vague answers ('about 4–6 weeks') signal no measurement baseline.",
 "How does that compare to where you were 12 months ago? Is it improving or getting worse?"),
("What percentage of your lead time do you estimate is actual work versus waiting for something?",
 "Introduces the concept of flow efficiency. Most leaders have never quantified this — it creates urgency.",
 "Most teams are at 10–20% FE; the insight that 80% of their time is waste is a powerful moment.",
 "If you could eliminate half that wait time, what would the business impact be?"),
("Are you tracking DORA metrics — deployment frequency, lead time, change failure rate, MTTR?",
 "Assesses DORA maturity and whether there's a measurement culture.",
 "Tracking DORA signals readiness for the platform; not tracking signals greenfield opportunity.",
 "Where do you sit on the DORA performance band — Elite, High, Medium, or Low?"),
("How long does it typically take your team to go from 'code complete' to 'in production'?",
 "Isolates the delivery pipeline waste — Phases 4–6 of the PDLC.",
 "Anything over 3 days signals significant wait time in CI/CD, testing, or change approval.",
 "What's the single biggest reason for that delay — is it testing, approvals, or something else?"),
]),
("2. Pain Points & Bottlenecks",[
("If I asked your engineers right now where they lose the most time, what would they say?",
 "Gets the real bottleneck from the practitioner perspective, not the CXO's polished view.",
 "Common answers: 'waiting for UAT sign-off', 'CAB approval', 'test environments'. These are your target bottlenecks.",
 "How long has that been a known issue, and what's been tried to fix it?"),
("What happens to a feature between 'dev complete' and 'UAT sign-off' — how long does it typically sit?",
 "Drills into Phase 5 (Continuous Testing) — typically the largest bottleneck in regulated industries.",
 "More than 5 days signals manual UAT processes; more than 2 weeks is critical.",
 "Is that driven by test environment availability, test data, or stakeholder scheduling?"),
("How often do deployments fail in production, and what's your average recovery time?",
 "CFR and MTTR — the two most financially impactful DORA metrics.",
 "CFR > 10% or MTTR > 1 day signals significant Quality and Delivery phase waste.",
 "What's the cost to the business of a failed deployment — revenue, compliance risk, or both?"),
("Where do you feel your team is working hard but the output doesn't match the effort?",
 "Surfaces hidden waste — overproduction, rework, non-used talent. Creates emotional resonance.",
 "Specific answers about 'rework cycles', 'rewriting requirements', 'rebuilding test data' are high-value signals.",
 "Is that more of a people/process issue or a tooling issue in your view?"),
]),
("3. Transformation Ambition",[
("If you could wave a magic wand and fix one thing about how your engineering team delivers, what would it be?",
 "Reveals the CXO's mental model of the problem — and often aligns with the platform's primary value.",
 "Look for 'speed', 'predictability', 'quality', 'less rework' — all addressable by the platform.",
 "What would achieving that be worth to the business in revenue or cost terms?"),
("Where do you want your DORA performance to be in 18 months — what does good look like for you?",
 "Sets the target and creates the gap that the platform helps close.",
 "A specific answer ('daily deployments, <1% CFR') signals a well-formed transformation programme.",
 "What's in place today to get you from where you are to that target?"),
("Have you made any previous attempts at DevOps or Agile transformation — what happened?",
 "Uncovers history, resistance points, and what has already been tried and failed.",
 "Most have tried something that didn't stick. This surfaces the change management requirement.",
 "What was different about that approach versus what you'd want to do now?"),
("If we could show you exactly where your PDLC waste is — quantified in hours and dollars — what would you do with that?",
 "Tests willingness to act on data. The ideal answer is 'we'd build a business case and fix it immediately'.",
 "A strong answer demonstrates executive sponsorship and decision-making authority.",
 "Who else would need to see that data to make a decision — CFO, board, product leadership?"),
]),
("4. Investment & Governance",[
("Do you have budget allocated for engineering transformation or DevOps improvement this year?",
 "Qualifies budget existence without asking for the number directly.",
 "A positive answer with a range is ideal. 'We're still planning' means you're early in the cycle.",
 "Is that budget controlled at the CTO level or does it require board/finance committee approval?"),
("What does the approval process look like for a $150K–$500K investment in your organisation?",
 "Maps the buying process — how many stakeholders, how long, what evidence is needed.",
 "Knowing the process lets you tailor the business case to the right decision gate.",
 "Would a quantified ROI business case be sufficient, or do you need a proof of concept first?"),
("Who else needs to be aligned for this kind of programme to move forward — CHRO, CFO, or the board?",
 "Identifies the full buying committee and potential blockers.",
 "The more stakeholders named, the longer the cycle — but it also sizes the opportunity.",
 "Would it help if we mapped a business case specifically for your CFO's investment criteria?"),
("What does success look like at 6 months, 12 months, and 18 months for an initiative like this?",
 "Anchors the conversation in outcomes and creates the measurement framework upfront.",
 "Specific KPIs ('20% lead time reduction', '$2M labour savings') signal a measurement-mature buyer.",
 "How would you communicate those results to the board — what metrics matter most to them?"),
]),
("5. Technology & Data",[
("What ALM tools do you use to track work — Jira, Azure DevOps, Rally, or something else?",
 "Confirms data source compatibility and assesses data availability for the platform.",
 "Jira or ADO = straightforward CSV export; bespoke tools = custom mapping needed.",
 "How consistently are tickets updated — would cycle time data be reliable in an export?"),
("Do you have access to historical ticket data going back 6–12 months?",
 "Confirms data depth for meaningful VSM baseline calculation.",
 "Less than 3 months of data limits the VSM accuracy; 6–12 months enables trend analysis.",
 "Is there a data governance process we'd need to navigate to export that data?"),
("What monitoring and observability tools are you running in production — Splunk, Dynatrace, PagerDuty?",
 "Confirms DORA data source availability for auto-scoring the assessment.",
 "Mature monitoring stack = richer DORA auto-scoring; limited tools = more manual assessment input.",
 "Are those tools connected to dashboards the engineering team reviews daily, or are they reactive only?"),
("How would your team feel about an AI platform analysing your delivery data — any concerns?",
 "Proactively surfaces AI trust, data privacy, or cultural resistance concerns.",
 "Common concerns: data security, AI accuracy, team reaction. Address them directly.",
 "What would give you and your team confidence that the AI outputs are trustworthy and auditable?"),
])]

for cat,qs in categories:
    h2(d,cat); divider(d)
    for i,(q,why,good,probe) in enumerate(qs,1):
        p_q=d.add_paragraph(); r_q=p_q.add_run(f"Q{i}. {q}"); sf(r_q,11,True,color=BLUE)
        p_q.paragraph_format.space_before=Pt(10); p_q.paragraph_format.space_after=Pt(3)
        bul(d,why,bold_pre="Why ask it")
        bul(d,good,bold_pre="Strong answer")
        bul(d,probe,bold_pre="Follow-up probe")
        d.add_paragraph()

d.save(f"{OUT}/02-cxo-question-bank.docx"); print("✓ Saved: 02-cxo-question-bank.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 4: SERVICE BRIEF ONE-PAGER
# ══════════════════════════════════════════════════════════════════
print("Building 03-service-brief-one-pager.docx...")
d=new_doc()
p=d.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("PDLC VSM PLATFORM"); sf(r,28,True,color=NAVY)
p2=d.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
r2=p2.add_run("Service Brief — AI-Powered Value Stream Transformation"); sf(r2,14,italic=True,color=BLUE)
divider(d)
tbl(d,["Metric","Current State","With Platform"],
    [["Lead Time","42 days","8 days (Option B, 18 months)"],["Flow Efficiency","8–18% (FSI typical)","61% (Option B)"],
     ["ROI","N/A","4.2× on $3M investment"],["Payback","N/A","14 months"]],[1.5,2.5,2.5])
sections_brief=[
("THE CHALLENGE","Engineering organisations are losing 80%+ of their delivery capacity to invisible wait time across the PDLC. Most teams operate at 8–18% flow efficiency — meaning for every 8-hour working day, fewer than 90 minutes of actual value is being created. The root causes (manual UAT gates, change approval queues, sequential architecture reviews) are known but not quantified — making it impossible to build a funded business case for transformation."),
("OUR APPROACH","The PDLC VSM Platform uses 8 LangGraph AI agents to map, measure, and transform your Product Development Lifecycle in a structured 9-step workflow: ALM data ingestion → DORA assessment → current-state VSM → bottleneck analysis → improvement catalogue → future-state modelling → business case → AI playbook. Every output is benchmarked against industry data, calibrated against your DORA performance, and presented with financial evidence."),
("WHAT YOU GET",None),
("WHY NOW","DORA (EU Digital Operational Resilience Act) requires FSI organisations to measure and evidence delivery performance by 2025. AI-native competitors are compressing time-to-market. The first organisations to quantify their PDLC waste and deploy AI agents to eliminate it will gain 2–4 years of competitive advantage that is structurally very difficult to close."),
("INVESTMENT","Starter Assessment: $150K (4 weeks, 1 team, VSM baseline + business case)\nFull Transformation Programme: $450K–$1.2M (18 months, Option A/B/C)\nOutcome-based model available: aligned incentives, benefits-linked payment"),
("NEXT STEP","Book a 30-minute discovery call. Upload your Jira/ADO export. Receive your quantified VSM baseline, DORA score, and top 5 bottlenecks within 2 weeks — ready to present to your board."),
]
for sec,txt in sections_brief:
    h2(d,sec)
    if txt: body(d,txt)
    if sec=="WHAT YOU GET":
        deliverables=["Quantified current-state VSM (7 phases: PT, WT, FE%)","DORA maturity score across 4 dimensions (73 questions)","Top 5 bottleneck cards with AI root cause analysis","3 future-state transformation scenarios (Option A/B/C)","ROI-validated business case (payback, NPV, IRR)","AI-generated, compliance-aware implementation playbook","36-agent improvement catalogue with quick wins flagged"]
        for dv in deliverables: bul(d,dv)
d.save(f"{OUT}/03-service-brief-one-pager.docx"); print("✓ Saved: 03-service-brief-one-pager.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 5: THOUGHT LEADERSHIP WHITEPAPER
# ══════════════════════════════════════════════════════════════════
print("Building 04-thought-leadership-whitepaper.docx...")
d=new_doc()
p=d.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("THE FLOW EFFICIENCY CRISIS"); sf(r,24,True,color=NAVY)
p2=d.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
r2=p2.add_run("Why 83% of Engineering Teams Are Losing Half Their Delivery Capacity to Invisible Waste"); sf(r2,13,italic=True,color=BLUE)
p3=d.add_paragraph(); p3.alignment=WD_ALIGN_PARAGRAPH.CENTER
r3=p3.add_run("PDLC VSM Platform  |  March 2026"); sf(r3,10,color=GRAY)
divider(d); d.add_paragraph()
sections_wp=[
("1. Executive Summary","""The average software engineering team in financial services spends less than 18% of its elapsed time doing actual work. The remaining 82% is consumed by waiting — for approvals, test environments, peer reviews, deployment gates, and stakeholder availability. This is not a failure of talent, methodology, or tooling. It is a measurement failure: organisations cannot eliminate waste they cannot see.

This whitepaper introduces the Flow Efficiency framework applied to the Product Development Lifecycle (PDLC), explains why DORA metrics alone are insufficient without VSM context, and presents a practical pathway from baseline measurement to AI-augmented transformation. Organisations that close the flow efficiency gap from 17% to 61% — as demonstrated in our US Bank case study — can expect a 4.2× return on transformation investment within 18 months."""),
("2. The Scale of the Problem","""Industry data consistently shows that engineering organisations are operating at 10–25% flow efficiency. This means that of the 42 days it takes the average financial services team to deliver a feature from idea to production, fewer than 8 days involve any actual work. The remainder is composed of handoff delays, approval queues, test environment provisioning, and stakeholder scheduling conflicts.

The financial impact is substantial. At a fully-loaded engineering cost of $120,000 per FTE per year, a team of 50 engineers carrying 80% wait time is consuming $4.8M per year in wasted capacity — time and talent that is not creating value. Across a portfolio of 20 teams, that figure exceeds $96M annually."""),
("3. Why Traditional Approaches Fail","""Three approaches dominate current attempts to address PDLC waste: management consulting engagements, standalone DORA measurement tools, and ad-hoc Agile coaching. Each has a critical limitation.

Management consultants produce high-quality analysis but at $2M–$8M over 9–18 months, with recommendations that rarely survive contact with delivery reality. DORA tools measure four important metrics but provide no diagnostic depth — knowing your lead time is 42 days tells you nothing about which of the 7 PDLC phases is responsible. Agile coaching improves team practices but lacks the data to prioritise where coaching effort has the highest leverage.

The missing element is a quantified, phase-level value stream map that connects DORA performance to specific activities and their wait times — and then maps AI agents to the exact bottlenecks causing the most waste."""),
("4. Lean VSM Applied to Software Delivery","""Value Stream Mapping (VSM) was pioneered by Toyota to visualise manufacturing waste. Its application to software delivery is both powerful and underutilised. The PDLC VSM framework maps seven phases: Backlog & Roadmap → Architecture & UX → Code Management → Continuous Integration → Continuous Testing → Continuous Delivery → Monitoring & Feedback. Each phase is measured by Process Time (active work), Wait Time (blocked/queued), and Flow Efficiency (PT / (PT+WT) × 100).

In a typical FSI engineering team, Phase 5 (Continuous Testing) accounts for 40–55% of total wait time. Manual SIT/UAT processes, test environment provisioning delays, and business stakeholder scheduling create bottlenecks that no amount of Agile ceremonies can resolve. The solution is not more sprints — it is AI-augmented test execution, environment orchestration, and intelligent UAT assistance."""),
("5. DORA as a Calibration Framework","""The DORA 4 key metrics — Deployment Frequency, Lead Time for Changes, Change Failure Rate, and MTTR — provide an external, benchmarked view of delivery performance. When combined with VSM phase data, they become a calibration mechanism: DORA lead time adjusts the proportional wait time across Phases 3–6; CFR adjusts the rework factor in Phase 5; MTTR directly maps to Phase 7 wait time.

This calibration transforms DORA from a reporting tool into an engineering tool — one that improves the accuracy of the current-state VSM and creates a direct line between measured performance and targeted improvement. Teams that sit in the DORA 'Medium' band (10–15% CFR, weekly deployments, 1–4 week lead times) typically find their VSM shows FE% of 12–22% — exactly the data needed to justify a transformation business case."""),
("6. The AI Transformation Opportunity","""Generative AI and agentic AI systems are creating a step-change opportunity for PDLC transformation that was not available two years ago. AI UAT assistants can reduce manual testing wait time by 75–85%. AI design reviewers can process architecture review queues 55% faster. AI release managers can automate 60–70% of standard change approval workflows. These are not hypothetical capabilities — they are deployed in production at organisations including Humana, JPMorgan, and Telstra.

The key to realising these gains is not deploying AI in isolation — it is deploying AI in the right phase, targeting the right bottleneck, with the right evidence that the expected wait time reduction will materialise. This requires a VSM baseline before deployment, and a measurement framework after."""),
("7. The Three Horizons","""Our transformation framework offers three options calibrated to different investment appetites, risk tolerances, and organisational change capacities:

Option A — AI Augmentation (12 months, $1.2M–$1.8M): Deploy 8 AI agents targeting the top 3 bottlenecks. Expected outcome: FE% from 17% to 42%, lead time reduction of 57%. Conservative, low-risk, focused on quick wins. Best for organisations with limited change capacity or budget.

Option B — Hybrid Intelligence (18 months, $2.5M–$3.5M): Deploy 15 AI agents across all 7 phases. Expected outcome: FE% from 17% to 61%, lead time reduction of 81%, daily deployments. Balanced investment with strong ROI. Best for organisations with a board mandate for transformation and medium risk appetite.

Option C — AI-Driven Lifecycle / ADLC (24–36 months, $4M–$6M): Deploy 22+ agents achieving near-full automation of manual PDLC gates. Expected outcome: FE% from 17% to 78%, lead time reduction of 93%, multiple daily deployments. High investment, high return, significant change management required. Best for organisations with a full AI-first mandate."""),
("8. Getting Started: A 4-Week Assessment Blueprint","""The first step is a quantified baseline. In 4 weeks, the PDLC VSM Platform can produce: a current-state VSM with FE% for all 7 phases; a DORA maturity score across 73 questions; the top 5 bottlenecks by waste volume and root cause; a benchmarked gap analysis against your industry peers; and a business case for transformation with ROI, payback period, and 5-year NPV.

The assessment requires: an ALM data export (Jira or ADO, 6–12 months of ticket history), access to 2–4 monitoring/tooling data sources (GitHub, Splunk, Jenkins, SonarQube), and 4–6 hours of workshop facilitation with your engineering leadership team.

The output is a board-ready briefing that answers the question every CTO and CFO needs answered: 'What will it cost to fix this, and what will we get back?' For the US Bank Team Phoenix pilot, that answer was: $3M investment, $8.4M annual benefits, 4.2× ROI, 14-month payback, $31.2M five-year NPV."""),
]
for sec,txt in sections_wp:
    h2(d,sec); body(d,txt); d.add_paragraph()
d.save(f"{OUT}/04-thought-leadership-whitepaper.docx"); print("✓ Saved: 04-thought-leadership-whitepaper.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 6: ROI CALCULATOR GUIDE
# ══════════════════════════════════════════════════════════════════
print("Building 05-roi-calculator-guide.docx...")
d=new_doc()
h1(d,"PDLC VSM Platform — ROI Value Calculator Guide")
body(d,"This guide explains the financial model used in the Business Case module. All assumptions are customisable within the platform settings.")
h2(d,"The 5 Benefit Streams")
tbl(d,["Stream","Formula","Default Assumptions","Timing"],
    [["Labour Savings","FTE × Salary × Effort_Reduction% × Phase_Time%","FTE=50, Salary=$120K, Effort%=varies","Month 6+"],
     ["Quality Improvement","Defects_Reduced × Defect_Cost","Defect cost=$15K, 40% reduction","Month 6+"],
     ["Speed-to-Market","Days_Saved × Revenue_at_Risk_per_Day","$500K/day, LT reduction=34 days","Month 9+"],
     ["Risk Reduction","Compliance_Risk × Probability_Reduction","$2M risk, 30% prob reduction","Month 6+"],
     ["Cost Avoidance","Legacy_Tool_Cost − New_Platform_Cost","$50K/month legacy tools","Month 3+"]],[1.4,2.2,2.2,0.9])
h2(d,"Default Financial Assumptions")
tbl(d,["Assumption","Default Value","How to Customise","Impact"],
    [["FTE fully-loaded cost","$120,000/year","Platform Settings","Labour savings"],
     ["Team size","From project metadata","Auto-populated from ALM","Scale of savings"],
     ["Revenue at risk (daily)","$500,000","Business Case form","Speed-to-market"],
     ["Defect cost (per incident)","$15,000","Business Case form","Quality benefit"],
     ["Compliance fine risk (annual)","$2,000,000","Business Case form","Risk reduction"],
     ["Cloud/infra cost (monthly)","$50,000","Business Case form","Cost avoidance"],
     ["Implementation cost multiplier","1.0×","Regional factor","Total investment"],
     ["Annual licence cost","$200,000","Per contract","Ongoing costs"],
     ["NPV discount rate","8%","Finance team input","5-year NPV"],
     ["Benefits start month","Month 6","Implementation timeline","Payback calc"],
     ["Year 1 ramp","60% of run-rate","Linear ramp","Year 1 figure"],
     ["Scenario adjustment","Base (±0%)","Conservative −25%, Optimistic +25%","All benefits"]],[2.0,1.3,1.8,1.4])
h2(d,"US Bank Option B — Worked Example")
tbl(d,["Period","Labour","Quality","Speed","Risk","Avoidance","TOTAL"],
    [["Months 1–5","$0","$0","$0","$0","$50K","$50K/mo"],
     ["Month 6–12 (60%)","$160K","$90K","$105K","$45K","$50K","$450K/mo"],
     ["Year 2 (100%)","$267K","$150K","$175K","$75K","$50K","$717K/mo"],
     ["Year 3 (100%)","$267K","$150K","$175K","$75K","$50K","$717K/mo"],
     ["3-Year Total","$5.5M","$3.1M","$3.6M","$1.5M","$1.7M","$15.4M"]],[1.2,1.0,1.0,1.0,0.9,1.1,1.1])
h2(d,"ROI Formula")
body(d,"ROI Multiple = Total 3-Year Benefits / Total 3-Year Investment = $15.4M / $3.0M = 5.1× (run-rate)")
body(d,"Payback Month = Cumulative Investment / Monthly Run-Rate Benefit = $3M / $717K = Month 14")
body(d,"5-Year NPV = Σ (Annual Benefit / (1+r)^t) − Investment = $31.2M at 8% discount rate")
d.save(f"{OUT}/05-roi-calculator-guide.docx"); print("✓ Saved: 05-roi-calculator-guide.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 7: INDUSTRY BENCHMARK REPORT
# ══════════════════════════════════════════════════════════════════
print("Building 06-industry-benchmark-report.docx...")
d=new_doc()
h1(d,"PDLC Performance Benchmarks 2026")
h2(d,"Financial Services, Healthcare & Telecoms")
body(d,"This report presents PDLC flow efficiency and DORA performance benchmarks across three regulated industries. Data is synthesised from 400+ engineering teams across 2024–2026 assessments.")
for sector,rows in [
("Financial Services (Banking, Insurance, Capital Markets)",[
 ["Deployment Frequency","< 1/month","Weekly","Daily","Multiple/day"],
 ["Lead Time for Changes","4–6 months","2–4 weeks","1–5 days","< 1 hour"],
 ["Change Failure Rate","18–25%","10–18%","5–10%","< 3%"],
 ["MTTR","5–10 days","1–3 days","< 4 hours","< 1 hour"],
 ["Overall Flow Efficiency","6–12%","12–22%","25–40%","40%+"],
 ["Phase 5 FE% (Testing)","4–10%","10–18%","20–35%","35%+"]]),
("Healthcare / HIPAA-regulated",[
 ["Deployment Frequency","< 1/month","Bi-weekly","Weekly","Daily"],
 ["Lead Time for Changes","3–5 months","3–6 weeks","1–2 weeks","< 3 days"],
 ["Change Failure Rate","15–22%","8–15%","4–8%","< 3%"],
 ["MTTR","3–8 days","1–2 days","< 6 hours","< 1 hour"],
 ["Overall Flow Efficiency","5–10%","10–18%","22–35%","35%+"],
 ["Phase 5 FE% (Testing)","3–8%","8–15%","18–30%","30%+"]]),
("Telecoms",[
 ["Deployment Frequency","< 1/month","Weekly","Daily","Multiple/day"],
 ["Lead Time for Changes","3–5 months","2–4 weeks","3–7 days","< 1 day"],
 ["Change Failure Rate","14–20%","8–14%","4–8%","< 3%"],
 ["MTTR","4–9 days","1–3 days","< 4 hours","< 1 hour"],
 ["Overall Flow Efficiency","7–14%","14–25%","28–42%","42%+"],
 ["Phase 5 FE% (Testing)","5–11%","11–20%","22–35%","35%+"]])]:
    h2(d,sector)
    tbl(d,["Metric","Low","Medium","High","Elite"],rows,[2.5,1.1,1.1,1.1,0.9])
    d.add_paragraph()
h2(d,"Key Findings Across All Sectors")
findings=["Testing is the universal bottleneck: Phase 5 FE% is 3–14% across all sectors — the lowest of any PDLC phase","Change approval (Phase 6) is the second largest bottleneck in regulated industries: 50–80h average wait time","Architecture review (Phase 2) accounts for 25–35% of total wait time in large FSI organisations","Elite performers achieve 40%+ FE by automating Phases 4, 5, and 6 — not by working harder in Phases 1–3","DORA and VSM metrics correlate strongly: Elite DORA = Elite FE% in 89% of assessed teams"]
for f in findings: bul(d,f)
d.save(f"{OUT}/06-industry-benchmark-report.docx"); print("✓ Saved: 06-industry-benchmark-report.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 8: CASE STUDY — US BANK
# ══════════════════════════════════════════════════════════════════
print("Building 07-case-study-usbank.docx...")
d=new_doc()
h1(d,"Case Study: US Bank — Team Phoenix")
h2(d,"42-Day Lead Time to 8 Days in 18 Months")
body(d,"Industry: Financial Services — Banking | Team: Payments & Transfers (Team Phoenix) | Platform: PDLC VSM Platform Option B")
divider(d)
h2(d,"The Challenge")
body(d,"US Bank's Team Phoenix — a 45-person engineering team responsible for the Payments & Transfers product group — was operating at 8.1% flow efficiency with a 42-day average lead time from feature request to production deployment. Despite a talented team, strong tooling (GitHub Enterprise, Jira, GitHub Actions, AWS), and a mature Agile process (SAFe), the team was consistently missing quarterly release commitments and accumulating a growing backlog of customer-impacting defects. A 12% change failure rate was consuming 2+ days of incident recovery per deployment cycle.")
body(d,"The CTO identified three board-level symptoms: time-to-market was 3× slower than digital-native competitors, compliance incidents were increasing, and engineering headcount was growing without proportional output improvement. The hypothesis was that the problem was not talent or tooling — it was invisible PDLC waste. But without a quantified baseline, making the case for transformation investment was impossible.")
h2(d,"The Approach")
body(d,"Team Phoenix engaged the PDLC VSM Platform for a 4-week assessment followed by an 18-month Option B transformation programme. The engagement was structured in three phases:")
for phase,activities in [
("Phase 1 — VSM Assessment & Baseline (Weeks 1–4)",["Exported 12 months of Jira ticket history (2,847 tickets across 24 sprints)","Configured 4 DORA data sources: GitHub, Splunk, SonarQube, PagerDuty","Completed 73-question DORA assessment (score: 2.0/5 — WALK band)","Generated 7-phase current-state VSM: 130h PT, 600h WT, 17.8% FE, 46.4-day LT","Identified 5 critical/high bottlenecks — Phase 5 (240h WT) as primary target"]),
("Phase 2 — Quick Wins & Core Transformation (Months 2–12)",["Deployed AI UAT Assistant (Phase 5): WT 240h → 48h in 8 weeks","Deployed ReviewAgent (Phase 3): WT 18h → 5h; PR review time reduced 72%","Deployed AI Release Manager (Phase 6): WT 56h → 14h; CAB gate automated 65%","Deployed AI Design Reviewer (Phase 2): WT 176h → 58h via async review workflow","Full 8-agent Phase 5 deployment achieved 31% overall FE improvement by Month 6"]),
("Phase 3 — Scale & Embed (Months 13–18)",["Deployed 7 additional agents (total 15) targeting Phases 1, 2, and 7","Achieved 61% flow efficiency — Phase 5 FE improved from 11.4% to 39.2%","Lead time reduced from 46.4 days to 8.1 days — 83% reduction","Deployed to 3 additional teams in the Digital Banking portfolio","Centre of Excellence established; VSM Practice Lead role created"])]:
    h3(d,phase)
    for a in activities: bul(d,a)
h2(d,"Results")
tbl(d,["Metric","Before (Week 0)","After (Month 18)","Improvement"],
    [["Overall Flow Efficiency","8.1%","61%","+52.9 percentage points"],
     ["Total Lead Time","46.4 days","8.1 days","−83%"],
     ["Phase 5 Wait Time (Testing)","240 hours","48 hours","−80%"],
     ["DORA Band","WALK (2.0/5)","High (3.8/5)","+1.8 bands"],
     ["Change Failure Rate","12%","4.2%","−65%"],
     ["MTTR","2.3 days","5.2 hours","−90%"],
     ["Deployment Frequency","Bi-weekly","Daily","8× increase"],
     ["Annual Benefits Realised","—","$8.4M","4.2× ROI"]],[2.5,1.5,1.5,1.5])
h2(d,"Lessons Learned")
for ll in ["Start with Phase 5 (Testing): the largest wait time in regulated industries — the ROI is highest and fastest","DORA calibration is essential: without it, the VSM overstates FE% because ALM cycle time includes non-working days","AI UAT Assistant requires 3–4 weeks of configuration for compliance environments — budget this in the pilot plan","Change management was underestimated: the 'AI is taking our jobs' concern required a 6-week communications programme","The benefits realisation tracker was the most-viewed artefact by the CFO — invest time in making it clear and frequent"]:
    bul(d,ll)
d.save(f"{OUT}/07-case-study-usbank.docx"); print("✓ Saved: 07-case-study-usbank.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 9: COMMERCIAL MODEL
# ══════════════════════════════════════════════════════════════════
print("Building 08-commercial-model-pricing.docx...")
d=new_doc()
h1(d,"PDLC VSM Platform — Commercial Model & Pricing")
body(d,"Three investment tiers designed to match where your organisation is in its transformation journey.")
for tier,price,duration,feats in [
("STARTER","$150,000","4-week assessment",
 ["1 engineering team assessed end-to-end","ALM data ingestion and 7-phase VSM baseline","73-question DORA assessment with AI scoring","Top 5 bottleneck cards with root cause analysis","3 future-state options (A/B/C) modelled","Full business case with ROI, payback, NPV","Implementation playbook for recommended option","6 months platform access","2 platform configuration and training sessions"]),
("PROFESSIONAL","$450,000","18-week transformation programme",
 ["Up to 5 engineering teams","All Starter deliverables","Full Option B transformation programme (15 agents)","Quick wins deployed in first 90 days","Change management programme and communications plan","Ongoing coaching: bi-weekly review cadence","Benefits realisation tracking (monthly reports)","12 months platform access","Access for up to 25 users"]),
("ENTERPRISE","$1,200,000+","18-month enterprise programme",
 ["Enterprise-wide deployment (unlimited teams)","All Professional deliverables","Centre of Excellence setup and enablement","Multi-portfolio VSM aggregation","Dedicated transformation advisory (2 days/month)","Custom agent development (up to 3 bespoke agents)","Executive quarterly business reviews","Unlimited platform access and users","Annual renewal at $300K/year"])]:
    h2(d,f"{tier} — {price}")
    body(d,f"Duration: {duration}")
    for f in feats: bul(d,f)
    d.add_paragraph()
h2(d,"Outcome-Based Commercial Model")
body(d,"For organisations that prefer to align payment with delivered results, we offer an outcome-based model structured around three benefit milestones:")
tbl(d,["Milestone","Trigger","Payment"],
    [["Baseline","VSM baseline report delivered and accepted","$75,000 (fixed)"],
     ["Quick Wins","FE% improved by ≥15 points OR LT reduced by ≥30% within 90 days","$150,000"],
     ["Transformation","FE% ≥40% OR LT reduced ≥60% by Month 18","$275,000 + 8% of Year 1 benefits above threshold"]],[2.2,2.8,1.5])
body(d,"Note: Outcome-based model available for Professional and Enterprise tiers only. Requires access to ALM data for independent verification.")
d.save(f"{OUT}/08-commercial-model-pricing.docx"); print("✓ Saved: 08-commercial-model-pricing.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 10: ENGAGEMENT MODEL
# ══════════════════════════════════════════════════════════════════
print("Building 09-engagement-model-overview.docx...")
d=new_doc()
h1(d,"PDLC VSM Platform — Engagement Model Overview")
for ph,dur,inv,obj,activities,deliverables in [
("Phase 1 — VSM Assessment","4 weeks","$150K",
 "Establish a quantified current-state baseline with DORA calibration, benchmark comparison, and funded transformation business case.",
 ["Week 1: Project kickoff, platform setup, ALM data ingestion","Week 2: DORA 73-question assessment with data source configuration","Week 3: Current-state VSM review, bottleneck analysis workshop","Week 4: Future state modelling, business case build, readout preparation"],
 ["7-phase current-state VSM with FE%, PT, WT per phase","DORA maturity score (4 dimensions) with calibration values","Top 5 bottleneck cards with AI root cause analysis","3 future-state scenarios (A/B/C) with projected metrics","ROI business case: investment, benefits, payback, NPV, IRR","AI-generated implementation playbook","Executive readout deck (12 slides)"]),
("Phase 2 — Pilot Transformation","12 weeks","$300K",
 "Deploy Quick Win AI agents targeting the top 3 bottlenecks. Demonstrate measurable FE% improvement and establish the change management framework.",
 ["Weeks 1–3: AI UAT Assistant deployment and testing","Weeks 4–6: ReviewAgent and AI Release Manager configuration","Weeks 7–9: Change management programme launch, team training","Weeks 10–12: Measurement, retrospective, Phase 3 planning"],
 ["3 AI agents deployed and operational (Quick Wins)","FE% baseline vs. 12-week comparison","Benefits realisation tracking (month 1 evidence)","Change management programme (stakeholder map, comms plan)","Phase 3 implementation plan"]),
("Phase 3 — Scale & Embed","Ongoing | 12 months","$200K/qtr",
 "Expand to full transformation (15 agents, all 7 phases), multi-team rollout, and Centre of Excellence establishment.",
 ["Months 1–3: Remaining 12-agent deployment","Months 4–6: 3-team expansion and cross-team benchmarking","Months 7–9: CoE setup and VSM Practice Lead enablement","Months 10–12: Benefits realisation review and annual programme plan"],
 ["Full 15-agent deployment operational","3+ teams on platform","Centre of Excellence operating model","Annual benefits report (vs. business case targets)","Renewal and expansion proposal"])]:
    h2(d,ph); body(d,f"Duration: {dur}  |  Investment: {inv}"); body(d,obj)
    h3(d,"Activities")
    for a in activities: bul(d,a)
    h3(d,"Deliverables")
    for dv in deliverables: bul(d,dv)
    d.add_paragraph()
h2(d,"Team Composition")
tbl(d,["Role","Client","Consulting","Phase"],
    [["Executive Sponsor","CTO / CDO","Programme Director","All"],
     ["Programme Manager","VP Engineering","Engagement Manager","All"],
     ["Platform Admin","DevOps Lead / Tech Lead","Platform Architect","1–2"],
     ["VSM Facilitator","Engineering Manager","VSM Practitioner","1–2"],
     ["Change Lead","HR / Change Manager","Change Consultant","2–3"],
     ["Data Owner","Analytics / Data Lead","Data Analyst","1"],
     ["Finance","CFO office rep","Business Case Lead","1,3"]],[2.5,1.5,1.5,1.0])
d.save(f"{OUT}/09-engagement-model-overview.docx"); print("✓ Saved: 09-engagement-model-overview.docx")

# ══════════════════════════════════════════════════════════════════
# FILE 11: DEMO SCRIPT
# ══════════════════════════════════════════════════════════════════
print("Building 10-demo-script-guide.docx...")
d=new_doc()
h1(d,"CXO Demo Script — 15-Minute Platform Walkthrough")
body(d,"Audience: CTO, VP Engineering, CDO, COO  |  Format: Screen-share or in-person  |  Pre-loaded: US Bank / Team Phoenix project")
h2(d,"Pre-Demo Checklist")
for item in ["Platform running: backend on port 8001, frontend on port 3001","US Bank project loaded with Team Phoenix data (42-day LT, 8.1% FE)","Browser on http://localhost:3001 — Dashboard visible","Second screen or window: this script","Test slide: all 7 phases showing FE% colour coding","Backup: offline screenshots in case of connectivity issues"]:
    bul(d,item)
h2(d,"Opening (2 minutes)")
body(d,"SCRIPT — say this:",italic=False)
body(d,'"I want to start with a question. If I asked you right now — what percentage of your team\'s lead time is actual work versus waiting for something — what would you say?" [pause for answer] "Most leaders say \'maybe 30–40%\'. The data from your sector says the average is 17.8%. That means for every 42 days it takes your team to ship a feature, fewer than 8 days involve any actual work. The rest — 34 days — is sitting in queues, waiting for approvals, test environments, and sign-offs. That\'s what we\'re going to quantify today — and then show you exactly which AI agents eliminate it."',italic=True)
h2(d,"Platform Walkthrough (10 minutes)")
for step,page,script,point in [
("Step 1: ALM Connect (1 min)","http://localhost:3001/alm-connect",'"This is where we connect your Jira or ADO data. For US Bank, Team Phoenix loaded 2,847 tickets from 24 sprints. The platform auto-maps them to the 7 PDLC phases — no configuration needed."',"Show the data preview table. Point to the phase distribution."),
("Step 2: Current State VSM (2 min)","http://localhost:3001/vsm-current",'"Here\'s what that data looks like as a value stream map. See the red bars — those are phases where flow efficiency is below 15%. Phase 5 — Continuous Testing — is at 11.4%. That means 240 hours of wait time for every 31 hours of actual testing work. Eight months of delay per year, invisible in your sprint reports."',"Point to the red Phase 5 bar. Show the 240h WT number."),
("Step 3: DORA Assessment (1 min)","http://localhost:3001/dora-assessment",'"We also run a 73-question DORA assessment across 4 dimensions. For Team Phoenix: WALK band, 2.0 out of 5. The DORA scores automatically calibrate the VSM — Phase 6 wait time adjusts to reflect their bi-weekly deployment frequency."',"Show the 4 dimension scores. Point to the band badge."),
("Step 4: Bottleneck Analysis (2 min)","http://localhost:3001/bottlenecks",'"Now the AI identifies exactly where to focus. Five bottlenecks: Manual SIT/UAT (240h wait — Critical), Architecture Review Gate (176h — Critical), CAB Release Approval (56h — High). Each one has a root cause, benchmark gap, and a competitor benchmark showing what peers have achieved."',"Click on the Manual SIT/UAT card to expand it. Show the root cause and the Humana benchmark."),
("Step 5: Improvements (2 min)","http://localhost:3001/improvements",'"The platform maps the right AI agent to each bottleneck. The AI UAT Assistant reduces Phase 5 wait from 240 hours to 48 hours — an 80% reduction. ROI estimate: 3.2×. Quick Win — deliverable in 90 days. JPMorgan automated 70% of their change approvals with AI Release Manager."',"Show the Quick Wins filter on. Sort by ROI. Hover over AI UAT Assistant."),
("Step 6: Business Case (2 min)","http://localhost:3001/business-case",'"This is what the CFO sees. Option B: $3M investment, $8.4M annual benefits, 4.2× ROI, 14-month payback, $31.2M five-year NPV. Conservative scenario: 3.1×. That\'s the board slide — and we generate it in 8 minutes from your ALM data."',"Show the executive summary box. Scroll to the benefits waterfall.")]:
    h3(d,step); body(d,f"Page: {page}"); body(d,f'Script: {script}',italic=True); body(d,f"Presenter note: {point}")
    d.add_paragraph()
h2(d,"Closing Ask (3 minutes)")
body(d,'"Let me tell you what I\'d like to propose. We can have your VSM baseline — quantified, benchmarked, ready for your board — in 2 weeks. Here\'s what that looks like: you export your Jira data today, we configure the platform by end of week, and in 2 weeks you\'re presenting these numbers to your CFO with a business case attached. The investment is $150K. If we don\'t find at least $500K of annual savings, we don\'t charge you. What\'s your next step?"',italic=True)
h2(d,"Objection Handling")
tbl(d,["Objection","Response"],
    [["'We already have DORA metrics'","DORA tells you your lead time is 42 days. Our platform tells you which of the 7 phases is responsible, which activities are causing it, and which AI agent eliminates it. DORA is the speedometer — this is the engine diagnostic."],
     ["'We don't have the budget'","The assessment pays for itself in month 3. If we find $500K+ of annual waste — which we consistently do in FSI teams — the $150K assessment ROI is 3× in year 1 alone. We can also structure outcome-based payment."],
     ["'AI won't work in our regulated environment'","The platform generates compliance-aware playbooks. Upload your FFIEC or SOX framework and the AI adds regulatory gates to every recommendation. JPMorgan and Humana both run this in production."],
     ["'Our data isn't clean enough'","We've onboarded teams with as little as 60% data completeness. The platform has built-in data quality scoring and DORA calibration compensates for gaps. We flag low-confidence areas explicitly."],
     ["'We tried transformation before and it didn't stick'","That's the most common response we hear — and the answer is always the same: the previous attempt lacked a quantified baseline and a financial business case. Without evidence, change doesn't survive the first budget cycle. This gives you both."]],[3.0,3.5])
d.save(f"{OUT}/10-demo-script-guide.docx"); print("✓ Saved: 10-demo-script-guide.docx")

print("\n✓ All Set 1 files complete.")
