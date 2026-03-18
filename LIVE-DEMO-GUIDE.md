# PDLC VSM Platform — Live Demo Guide
## US Bank | Team Phoenix | Payments & Transfers

**Purpose:** Step-by-step script for presenting the full platform end-to-end.
**Scenario:** US Bank's Payments & Transfers team (Team Phoenix) — a Medium DORA performer in a regulated banking environment. We map their current-state PDLC waste, assess DORA performance, analyse bottlenecks, then model three future-state transformation options culminating in an AI-Driven Lifecycle (Option C / ADLC).

**Platform URL:** http://localhost:3001
**Estimated demo runtime:** 35–45 minutes (full) | 15–20 minutes (exec highlight)

---

## Before You Start

1. Ensure the platform is running: `cd /Users/125066/projects/pdlc-vsm-platform && source backend/venv/bin/activate && python -m uvicorn backend.main:app --reload --port 8001` (backend) and `cd frontend && npm run dev` (frontend :3001)
2. Open a fresh browser tab to http://localhost:3001
3. Have this guide open in a second window for copy-paste
4. Have the synthetic document files ready (contents below in each step)

---

## WORKFLOW OVERVIEW

```
Step 1: ALM Connect          → Set up project + connect data source
Step 2: DORA Assessment      → Score 4 DORA dimensions + AI auto-scoring
Step 3: Current State VSM    → Review current-state value stream map
Step 4: VSM Editor           → Drill into phase metrics
Step 5: Bottleneck Analysis  → AI-identified waste and root causes
Step 6: Improvements         → Prioritised AI improvement actions
Step 7: Future State VSM     → Compare Options A / B / C (ADLC)
Step 8: Business Case        → Financial model + ROI
Step 9: Playbook Context     → Upload context docs for AI playbook generation
```

---

## STEP 1 — ALM Connect

**Page:** http://localhost:3001/alm-connect
**Story:** "First, we tell the platform who we are and where our data lives."

### Sub-step 1a: Project Setup

Enter these exact values in the Project Setup form:

| Field | Value to Enter |
|-------|---------------|
| Project Name | `US Bank — Digital Banking Platform` |
| Organization | `US Bank` |
| Portfolio | `Digital Banking` |
| Product Group | `Payments & Transfers` |
| Product Team | `Team Phoenix` |
| Industry | `Banking & Financial Services` |

Click **"Next: Connect ALM Tool →"**

### Sub-step 1b: ALM Connection

**Option A — Live Jira connection (if demo env has Jira):**

Click the **🔵 Jira** tile, then enter:

| Field | Value |
|-------|-------|
| Instance URL | `https://usbank-digital.atlassian.net` |
| Username / Email | `phoenix-svc@usbank.com` |
| API Token | `ATATTxxxxxxxxxxxxxxx` *(use real token or leave for demo)* |
| Project Key | `PHOE` |

Click **"🔌 Test Connection"** → if demo env doesn't have Jira access, proceed to Option B.

**Option B — CSV Upload (recommended for demo):**

Click the **📄 CSV / Manual** tile.

A message will appear: *"You can manually enter metrics in the VSM Editor, or upload a CSV."*

Click **"📥 Fetch & Map to VSM →"** — the platform will use sample data and display the Data Preview.

**Alternatively — use the synthetic CSV file below.** Save it as `team-phoenix-jira-export.csv` and reference it:

```csv
phase,activity,process_time_hrs,wait_time_hrs,lead_time_days,cycle_time_hrs,team,tool,notes
Backlog & Roadmap,Product Discovery & OKR Alignment,8,24,4.0,32,Product Owner,Confluence,"Quarterly OKR alignment session + stakeholder interviews"
Backlog & Roadmap,Feature Definition & User Stories,12,16,3.5,28,Product Owner + BA,Jira,"Story writing + acceptance criteria. Avg 2.5 review cycles."
Backlog & Roadmap,Backlog Grooming & Estimation,6,16,2.8,22,Team Phoenix,Jira,"Bi-weekly grooming. Multiple re-estimation cycles due to unclear requirements."
Backlog & Roadmap,Sprint Planning,5,16,2.7,21,Team Phoenix,Jira,"Sprint planning blocked by unresolved dependencies from architecture review."
Architecture & UX Design,Architecture Review Board,8,72,10.0,80,Principal Architect,Confluence,"ARB meets fortnightly. Average queue time: 72 hours to get slot."
Architecture & UX Design,API Contract Design,12,40,6.5,52,Tech Lead,Confluence + Postman,"API design review requires approval from Integration team (separate team)."
Architecture & UX Design,UX Design & Prototyping,16,24,5.0,40,UX Designer,Figma,"Prototype review loops. Average 3 revision cycles per feature."
Architecture & UX Design,Security Architecture Review,8,40,6.0,48,CISO Team,Jira,  "PCI-DSS compliance review. CISO team has 40-hour SLA from request."
Code Management,Feature Development,8,4,1.5,12,Dev Team (3),GitHub,"Active coding time only. Well-understood work."
Code Management,Code Review & PR Approval,4,18,2.8,22,Senior Engineers,GitHub,"Requires 2 senior approvals. Median wait: 18 hours. PR size avg 847 lines."
Code Management,Branch Merge & Conflict Resolution,1,4,0.6,5,Dev Team,GitHub,"Merge conflicts common due to long-lived feature branches."
Continuous Integration,CI Pipeline Execution,0.4,0.1,0.06,0.5,DevOps (Automated),GitHub Actions,"Build + unit test. Avg 24 min. Dependency download ~12 min of that."
Continuous Integration,Static Analysis & SAST,0.3,0.2,0.06,0.5,DevOps (Automated),SonarQube,"Code quality gate. Fails ~23% of first-run PRs, triggering re-work loop."
Continuous Integration,Build Artefact Publishing,0.2,0.1,0.04,0.3,DevOps (Automated),JFrog Artifactory,"Artefact versioning and registry push."
Continuous Integration,Environment Promotion (Dev→SIT),0.5,6,0.8,6.5,DevOps,Kubernetes / Helm,"Kubernetes deployment to SIT. Avg 6-hour promotion queue due to shared SIT cluster."
Continuous Testing,Automated Regression Test Suite,4,8,1.5,12,QA Automation,Selenium / JUnit,"62% test coverage. Sequential execution — no parallelism."
Continuous Testing,Manual SIT Testing,16,12,3.5,28,QA Team (4),Jira,"Manual testing of complex payment flows. Required for PCI-DSS compliance evidence."
Continuous Testing,Performance / Load Testing,6,8,1.75,14,Performance Team,JMeter,"Separate performance team. Request-based queue. Avg 8-hour wait for slot."
Continuous Testing,Penetration Testing (PCI-DSS),0,40,5.2,40,External Security Team,Manual,"Mandatory for any feature in PCI-DSS scope. External vendor. 5.2-day avg turnaround."
Continuous Testing,UAT Sign-off,8,20,3.5,28,Business Analyst + PO,Jira,"Business stakeholder UAT. Sign-off required before CAB submission."
Continuous Delivery,CAB Submission & Review,2,48,6.0,50,Release Manager,ServiceNow,"Change Advisory Board. Requires 48h notice. VP-level sign-off from 3 approvers."
Continuous Delivery,Pre-Production Smoke Test,2,8,1.25,10,DevOps + QA,Automated + Manual,"Smoke test in pre-prod. Manual verification of critical payment paths."
Continuous Delivery,Production Deployment,0.5,80,10,80.5,Release Team,Kubernetes,"Wed release window only. Blackout Thu–Mon. 80-hour average wait for next window."
Continuous Delivery,Post-Deployment Verification,1,8,1.1,9,DevOps,Datadog,"Monitoring checks. Manual sign-off from Release Manager."
Monitoring & Feedback,Incident Detection & Alerting,0,3,0.4,3,DevOps (Automated),PagerDuty,"MTTD: 3 hours average. Alert fatigue issue — 340 false positives/month."
Monitoring & Feedback,Incident Triage & Root Cause,2,8,1.25,10,On-call Engineers,PagerDuty + Datadog,"Manual log analysis. No AI-assisted RCA."
Monitoring & Feedback,Incident Resolution & Hotfix,4,46,6.2,50,Dev Team + DBA,GitHub + PagerDuty,"DBA team only available Mon–Fri 8am–6pm. DB incidents wait for next-day coverage."
Monitoring & Feedback,Post-Mortem & Feedback Loop,2,8,1.25,10,Team Phoenix,Confluence,"Monthly post-mortem. Findings rarely fed back into backlog systematically."
```

### Sub-step 1c: Data Preview

The platform shows:
- **Avg Lead Time:** 42.5 days
- **Flow Efficiency:** 8.1%
- **Total Effort:** 94 hrs

Click **"View Current State VSM →"**

**Demo talking point:** *"8.1% flow efficiency means 91.9% of the time a feature spends in our pipeline is pure waste — waiting, queuing, re-work loops. The industry average for banking is 10–15%. Elite performers hit 40%+."*

---

## STEP 2 — DORA Assessment

**Page:** http://localhost:3001/dora-assessment
**Story:** "Now we layer in DORA metrics — the industry's gold standard for software delivery performance."

### Option A — Use the AI Demo Loader (fastest for demo)

Click the **"⚡ Load US Bank Demo Data"** button at the top of the page.

This instantly pre-fills all 10 metrics AND loads the AI Auto-Score notes with sources and root causes for each metric.

Then click **"🤖 Show AI Notes"** to expand the AI analysis panel.

### Option B — Manual Entry (for live/real-data walkthrough)

Enter these values manually:

#### Section 1: Core 4 DORA Metrics

| Metric | Value | DORA Band |
|--------|-------|-----------|
| Deployment Frequency | `Once per week` | Medium |
| Lead Time for Changes | `1–2 weeks` | Medium |
| Change Failure Rate | `12` (%) | Medium |
| Mean Time to Restore | `1–7 days` | Medium |

#### Section 2: Extended Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Avg CI Build Duration | `24` minutes | Above elite benchmark of <10 min |
| Code Review Cycle Time | `18` hours | Median PR-open to merge-approved |
| Automated Test Coverage | `62` % | Below 80% quality gate target |
| Mean Time to Detect (MTTD) | `3` hours | Alert fatigue causing false positives |
| % Tests Automated | `55` % | Still 45% manual |
| Infra Automation (IaC) | `45` % | Legacy monolith partially migrated |

**Expected result:** Profile = **Medium Performer** (amber badge)
**VSM Recommendation:** Option A or B
**Priority Phases:** Testing (5), Release (6), Code Review (3)

### AI Auto-Score Notes Walkthrough

After loading demo data, expand the **AI Analysis** panel and walk through each metric note:

**Deployment Frequency note — say:**
*"AI pulled this from the Jira Release Tracker and the CAB Meeting Schedule. Confidence: 88%. The root cause isn't technical — it's the Change Advisory Board governance gate. Every deployment requires 48-hour advance notice and sign-off from the CTO, CISO, and Release Manager."*

**Change Failure Rate note — say:**
*"94% confidence — our most reliable score. 12% failure rate comes directly from the Incident Log: 47 deployment failures out of 392 total. The AI traces the root cause to database migration scripts — 61% of failures. Click Accept."*

For each metric, click **"✓ Accept"** to validate the AI's suggestion.

Once all 4 core metrics are accepted:
- Click **"✅ Accept All"** for extended metrics
- A green validation banner appears: *"7/7 validated — ready to calibrate VSM"*
- Click **"Apply DORA Calibration to VSM →"**

**Demo talking point:** *"This is the human validation step. The AI scores against evidence, shows you the source document and finding, explains the root cause — but you make the final call. This ensures the transformation roadmap is grounded in your actual data, not AI assumptions."*

---

## STEP 3 — Current State VSM

**Page:** http://localhost:3001/current-vsm
**Story:** "Here's the current state value stream map for Team Phoenix's Payments & Transfers product."

### What to Point Out

Walk through each phase left to right:

| Phase | PT (hrs) | WT (hrs) | FE | Key Bottleneck |
|-------|----------|----------|----|----------------|
| 1. Backlog & Roadmap | 31 | 72 | 30% | Quarterly planning cadence |
| 2. Architecture & UX | 36 | 176 | 17% | ARB queue + PCI-DSS review |
| 3. Code Management | 13 | 18 | 42% | PR review wait (18h median) |
| 4. CI | 2 | 6.5 | 24% | 24-min build + SIT queue |
| 5. Testing | 34 | 88 | 28% | Pen-test gate (5.2 days) |
| 6. Delivery | 8 | 144 | 5% | CAB + Wed-only release window |
| 7. Monitoring | 6 | 96 | 6% | 2.3-day MTTR, DBA availability |

**Total — Current State:**
- Process Time: 130 hrs
- Wait Time: 600 hrs
- Lead Time: ~42 days
- Flow Efficiency: 8.1%

**Demo talking point:** *"Phase 6 — Continuous Delivery — has a 5% flow efficiency. That means for every 1 hour of actual deployment work, the feature sits waiting for 19 hours. The Wednesday-only release window is the biggest single contributor to lead time in the entire pipeline."*

---

## STEP 4 — VSM Editor

**Page:** http://localhost:3001/vsm-editor
**Story:** "The VSM Editor lets us drill into any phase and see the individual activities."

### What to Click

1. Click on **"Phase 6: Continuous Delivery"** to expand it
2. Show the activity breakdown:
   - CAB Submission: 2h PT / 48h WT
   - Pre-Prod Smoke Test: 2h PT / 8h WT
   - Production Deployment: 0.5h PT / 80h WT ← highlight this
   - Post-Deploy Verification: 1h PT / 8h WT

3. Click the **edit icon** on "Production Deployment" and narrate:
   *"80 hours of wait time — that's the Wednesday release window. The actual deployment takes 30 minutes but waits 3+ days for the next window. This is the single highest-impact item to fix."*

4. Show Phase 5 (Testing):
   - Pen-test gate: 0h PT / 40h WT
   *"Zero hours of process time. Purely waiting for an external vendor. AI-assisted DAST scanning could replace this for lower-risk changes."*

---

## STEP 5 — Bottleneck Analysis

**Page:** http://localhost:3001/bottlenecks
**Story:** "AI analysis of the 8 highest-impact bottlenecks ranked by business impact."

### Key Bottlenecks to Highlight

| Rank | Bottleneck | WT Saved | Severity |
|------|-----------|---------|---------|
| 1 | CAB/Release Window Gate (Phase 6) | 128h | Critical |
| 2 | Mandatory Pen-Testing Gate (Phase 5) | 40h | Critical |
| 3 | Architecture Review Board Queue (Phase 2) | 72h | High |
| 4 | PR Code Review Wait (Phase 3) | 18h | High |
| 5 | CI Build Duration (Phase 4) | 16h | Medium |
| 6 | Sequential Test Execution (Phase 5) | 28h | High |
| 7 | DBA Availability Gap (Phase 7) | 24h | High |
| 8 | Quarterly Planning Cadence (Phase 1) | 48h | Medium |

**Demo talking point on #1:**
*"If we solve just the CAB gate — implementing a risk-tiered deployment model with automated change assessment — we reduce lead time by ~13 days. That's the single highest-leverage intervention."*

**Demo talking point on #2:**
*"The pen-testing gate is mandatory for PCI-DSS. But it only needs to be mandatory for high-risk changes. AI-assisted DAST + SAST in the pipeline can assess risk level and route low-risk changes past the external pen-test — eliminating 5.2 days for ~70% of deployments."*

---

## STEP 6 — Improvements

**Page:** http://localhost:3001/improvements
**Story:** "The AI has generated 8 prioritised improvement actions, ordered by impact-to-effort ratio."

### Top 8 Improvements

| # | Improvement | Timeline | Impact |
|---|------------|----------|--------|
| 1 | Risk-tiered deployment model (eliminate CAB for low-risk) | Sprint 1–2 | Lead time −13 days |
| 2 | AI-assisted DAST/SAST replacing pen-test gate | Sprint 3–4 | Lead time −5 days |
| 3 | GitHub Copilot + AI PR reviewer for code review | Sprint 1 | PR wait −12h |
| 4 | Build caching + parallel test execution | Sprint 2 | Build time −14 min |
| 5 | ARB self-service for standard patterns | Sprint 3–4 | ARB wait −48h |
| 6 | Automated DB migration testing + rollback scripts | Sprint 2–3 | CFR −6% |
| 7 | AIOps incident detection + runbook automation | Sprint 5–6 | MTTR −1.8 days |
| 8 | Continuous planning (quarterly → rolling 6-week) | Sprint 3 | Planning WT −40% |

---

## STEP 7 — Future State VSM

**Page:** http://localhost:3001/future-state
**Story:** "We've modelled three transformation options. Let's compare them."

### Overview Comparison (click "All Options" tab)

| Metric | Current | Option A | Option B | Option C (ADLC) |
|--------|---------|---------|---------|-----------------|
| Lead Time | ~42 days | ~18 days | ~10 days | ~3 days |
| Flow Efficiency | 8.1% | ~30% | ~44% | ~62% |
| Process Time | 130h | 65h | 30h | 8h |
| Wait Time | 600h | 155h | 38h | 5h |
| Agent Activities | 0 | 8 | 18 | 26 of 28 |

### Option A — Augmented PDLC

Click the **"Option A"** tab.

*"Option A is the 6–12 month incremental path. We keep all 7 PDLC phases but layer in AI augmentation at the activity level. Engineers still own every decision — AI assists."*

**Click Phase 3 (Code Management) to expand activities:**
- GitHub Copilot: AI-assisted coding (type: hybrid)
- AI PR Reviewer: automated pre-review (type: agent)
- Human approval: engineer still approves (type: human)

**Key metrics for Phase 3:** PT: 8h, WT: 6h, FE: 57%
*"PR review drops from 18h to 6h wait because AI pre-reviews the PR and flags issues before the human reviewer even opens it."*

### Option B — Automated PDLC

Click the **"Option B"** tab.

*"Option B is the 12–18 month transformation. Testing and delivery are largely automated. The deployment model shifts from weekly CAB batches to continuous delivery with automated risk gates."*

**Click Phase 5 (Continuous Testing) to expand:**
- AI DAST/SAST scanner (agent)
- Automated regression (agent)
- Risk scoring engine (agent)
- Human override for high-risk only (oversight)

**Key metrics for Phase 5:** PT: 3h, WT: 2h, FE: 60%
*"Pen-test gate is gone for 70% of changes. AI risk-scores each deployment and only routes high-risk ones to manual review."*

### Option C — ADLC (AI-Driven Lifecycle, BMAD Approach)

Click the **"Option C"** tab.

*"Option C is the 18–24 month north star: the AI-Driven Lifecycle. Two human roles exist: Product Definer who sets vision and OKRs, and Product Builder who supervises agent orchestration and holds the production approval gate."*

**Point out the ADLC banner:**
*"This uses the BMAD approach — Build, Measure, Automate, Deploy — where agent swarms handle end-to-end delivery. The 7 traditional PDLC phases are replaced by 7 AI capabilities."*

**Walk through each ADLC phase:**

| ADLC Phase | What Happens | Human Role |
|-----------|-------------|----------|
| 1. Intent & Outcome Definition | Product Definer sets OKRs + acceptance criteria | Product Definer (human) |
| 2. Autonomous Architecture & Design | Architecture agent generates design, API contracts, security model | Product Builder reviews |
| 3. Agentic Code Generation | Code generation agents write, test, refactor in parallel | Product Builder oversight |
| 4. Autonomous Integration Pipeline | CI/CD agents handle build, test, security scan, deployment | Automated |
| 5. Continuous Quality Intelligence | QA agents run comprehensive coverage, generate quality report | Product Builder approves |
| 6. Zero-Touch Delivery | Deployment agents manage release, rollback, smoke tests | Product Builder holds prod gate |
| 7. AIOps & Continuous Learning | AIOps agents detect, diagnose, fix, learn | Escalation to Product Builder |

**Click Phase 3 (Agentic Code Generation) to expand activities:**
- Intent parsing agent (🤖 agent, 0.5h PT, 0h WT)
- Multi-agent code generation (🤖 agent, 1.5h PT, 0h WT)
- AI peer review & refactor (🤖 agent, 0.5h PT, 0h WT)
- Product Builder quality gate (👁 oversight, 0.5h PT, 0.5h WT) ← only human touch

*"The only wait time is Product Builder's oversight review. No approval queues. No ARB. No CAB. From intent to code-ready: 3 hours."*

**ADLC Total:**
- 8 hours process time (vs 130h current)
- 5 hours wait time (vs 600h current)
- 62% flow efficiency (vs 8.1% current)
- 26 of 28 activities are agent-driven

---

## STEP 8 — Business Case

**Page:** http://localhost:3001/business-case
**Story:** "The financial model quantifies the ROI of the transformation."

### Key Numbers to Highlight

*(Based on Option B — recommended for most organizations)*

| Metric | Value |
|--------|-------|
| Team Size | 12 engineers |
| Avg Fully-Loaded Cost | $180,000 / person / year |
| Annual Engineering Cost | $2.16M |
| Current Waste (% of time) | 91.9% |
| **Recoverable Capacity (Option B)** | **~36% → ~$780K/year** |
| Estimated Tool Investment | $120K / year |
| Net Annual Benefit | **~$660K** |
| Estimated Payback Period | **7–9 months** |
| 3-Year NPV | **~$1.6M** |

*"Beyond the cost savings — the real business case is speed to market. Payments features currently take 42 days from concept to production. With Option B, that's 10 days. With Option C, it's 3 days. In payments, speed is competitive advantage."*

**Risk Context:**
*"For a regulated bank, we're not recommending 'move fast and break things.' Option B includes automated compliance evidence generation — every deployment produces an audit trail that satisfies PCI-DSS requirements automatically. The compliance burden goes down as delivery speed goes up."*

---

## STEP 9 — Playbook Context

**Page:** http://localhost:3001/playbook
**Story:** "Finally, we give the AI the context it needs to generate a bespoke implementation playbook."

### Section 1: Team Profile

| Field | Value |
|-------|-------|
| Team Name | `Team Phoenix` |
| Organisation | `US Bank` |
| Portfolio | `Digital Banking` |
| Product Group | `Payments & Transfers` |
| Team Size | `12` |
| Current Roles | `Product Owner, 3× Backend Dev (Java/Spring), 2× Frontend Dev (React), QA Lead, 2× QA Engineer, DevOps Engineer, Solution Architect, Business Analyst` |
| Seniority Mix | `Mixed (2–5yr avg)` |
| Industry | `Banking & Financial Services` |

### Section 2: Technology Stack

| Field | Value |
|-------|-------|
| Source Control | `GitHub Enterprise` |
| CI/CD Platform | `GitHub Actions` |
| Cloud Platform | `Microsoft Azure` |
| ALM / Project Tool | `Jira` |
| Primary Languages | `Java / Spring Boot, React 18, Python (data pipelines)` |
| Monitoring / Observability | `Datadog, PagerDuty, Splunk` |
| Testing Tools | `Selenium, JUnit 5, Postman, JMeter` |
| Existing AI Licences | `GitHub Copilot Enterprise (100 seats), Azure OpenAI API (accessed via Azure)` |

### Section 3: Budget & Procurement

| Field | Value |
|-------|-------|
| Budget Available | `$500K–$1M` |
| Procurement Complexity | `Complex (4–8 weeks — committee)` |
| Hard Deadline | `Must demonstrate measurable lead time reduction before Q2 2026 budget review` |
| Unused Licence Capacity | `GitHub Copilot: 100 seats licensed, only 34 currently active` |

### Section 4: Security & Compliance

| Field | Value |
|-------|-------|
| Compliance Frameworks | `PCI-DSS Level 1, SOC 2 Type II, APRA CPS 234, ISO 27001` |
| Change Approval Process | `Full enterprise CAB (bi-weekly)` |
| Data Residency | `National (same country only)` |
| AI / LLM Data Policy | `Enterprise-only (Microsoft/Google/AWS)` |

### Section 5: Org Culture & Change Readiness

| Field | Value |
|-------|-------|
| Team Maturity | `Performing (high trust, predictable delivery)` |
| Previous AI Attempts | `Partial adoption (some tools in use)` |
| Detail on Previous Attempts | `GitHub Copilot rolled out 6 months ago. Adoption is 34% of licensed seats. Engineers using it report 20–30% productivity improvement in coding tasks. Resistance from 2 senior engineers who feel AI-generated code lacks quality. No formal training program ran at rollout.` |
| Leadership Sponsorship | `Active champion (senior leader publicly backing this)` |
| Training Time Available | `2–4 hrs/week` |
| Change Management Support | `Scrum Master / Agile Coach available` |

### Section 6: Ways of Working

| Field | Value |
|-------|-------|
| Development Methodology | `Scrum` |
| Sprint Length | `2 weeks` |
| Current Deployment Frequency | `Weekly` |
| Release / Change Process | `Manual CAB approval required` |
| Current Ceremonies | `Daily standup (15 min), bi-weekly sprint review, bi-weekly retrospective, quarterly OKR check-in, monthly architecture forum` |

### Section 7: Stakeholder Context

| Field | Value |
|-------|-------|
| Key Sponsors | `CTO (Michael Chen), Head of Digital Banking (Sarah Williams), CISO (James Okonkwo)` |
| Known Concerns | `"AI will create compliance risk" (CISO concern), "GitHub Copilot hallucinations in production code" (Engineering VP concern), "Previous automation initiatives created technical debt" (Architect concern)` |
| Success Criteria | `Must reduce mean lead time from 42 days to <20 days within 6 months. Must not increase change failure rate. Must produce audit-ready compliance evidence automatically. ROI demonstrated before Q2 2026 budget cycle.` |

---

## DOCUMENTS TO UPLOAD

For maximum playbook accuracy, paste these synthetic documents into each document section.

### Document 1: Org Chart / Team Roster

**Section:** "Org Chart / Team Roster" → paste the text below

```
US BANK — TEAM PHOENIX ROSTER
Digital Banking Division | Payments & Transfers Product Group
Date: January 2026

REPORTING STRUCTURE:
Head of Digital Banking: Sarah Williams (VP)
  └── Engineering Manager: David Park
        ├── Team Phoenix (Reports to David Park)
        │     ├── Product Owner: Jennifer Zhao
        │     ├── Solution Architect: Marcus Thompson
        │     ├── Business Analyst: Rachel Kim
        │     ├── Scrum Master: Tom Bradley
        │     ├── Backend Developer (Senior): James Liu [GitHub Copilot active]
        │     ├── Backend Developer (Mid): Aisha Obi [GitHub Copilot inactive]
        │     ├── Backend Developer (Mid): Carlos Mendez [GitHub Copilot active]
        │     ├── Frontend Developer (Senior): Sophie Wang [GitHub Copilot active]
        │     ├── Frontend Developer (Mid): Priya Sharma [GitHub Copilot inactive]
        │     ├── QA Lead: Kevin O'Brien
        │     ├── QA Engineer: Laura Chen
        │     └── DevOps Engineer: Raj Patel [GitHub Copilot active]
  └── CISO Office (dotted line for security reviews): James Okonkwo
  └── DBA Team (shared services, not dedicated): Maria Gonzalez (Lead DBA)
  └── Architecture Review Board: Principal Architect Robert Stern (fortnightly rotation)

HEADCOUNT: 12 dedicated + 3 shared services (DBA, Security, ARB)
LOCATION: Minneapolis HQ (in-person Mon/Tue, remote Wed–Fri)
TIMEZONE: Central Time (US)
```

---

### Document 2: Engineering Standards / Tech Playbook

**Section:** "Engineering Standards / Tech Playbook" → paste the text below

```
US BANK DIGITAL BANKING — ENGINEERING STANDARDS v2.4
Payments & Transfers | Effective: January 2026

1. SOURCE CONTROL
   - All code in GitHub Enterprise (github.enterprise.usbank.com)
   - Branch strategy: GitFlow (main, develop, feature/*, hotfix/*)
   - Branch protection: main requires 2 approvals, CI passing, no direct push
   - PR size target: < 400 lines (currently averaging 847 — known gap)
   - Commit signing: GPG required for all production-branch commits

2. CI/CD PIPELINE (GitHub Actions)
   - All PRs trigger: lint → build → unit tests → SAST (SonarQube)
   - SonarQube quality gate: 80% coverage required (currently 62% — red gate)
   - Artefact registry: JFrog Artifactory (usbank.jfrog.io)
   - Container registry: Azure Container Registry
   - Deployment: Kubernetes (AKS) via Helm charts
   - Environments: dev → SIT → UAT → pre-prod → prod

3. TESTING STANDARDS
   - Unit test framework: JUnit 5 (Java), Jest (React)
   - Integration tests: Spring Boot Test + Testcontainers
   - E2E automation: Selenium Grid (legacy) — migration to Playwright in Q2 2026
   - Performance: JMeter (load tests required for any API handling > 1000 TPS)
   - Security: OWASP ZAP (automated), external pen-test for PCI-DSS scope changes

4. SECURITY REQUIREMENTS
   - All APIs require OAuth 2.0 / JWT authentication
   - Secrets management: Azure Key Vault (no secrets in code or environment variables)
   - SAST tool: SonarQube Enterprise (payment module rules enabled)
   - Dependency scanning: GitHub Dependabot + Snyk
   - Container scanning: Trivy (integrated in CI pipeline)
   - PCI-DSS scope changes: mandatory CISO review + external pen-test

5. CLOUD & INFRASTRUCTURE (Azure)
   - Cloud: Microsoft Azure (AustraliaEast region primary, AustraliaSoutheast DR)
   - IaC: Terraform 1.6+ (45% of infrastructure — legacy components still manual)
   - Kubernetes: AKS 1.28, GitOps via Flux v2
   - Databases: Azure SQL (primary), Azure Cache for Redis, Azure Service Bus
   - Monitoring: Datadog (APM + Infrastructure), Splunk (SIEM + Audit logs)
   - On-call: PagerDuty (L1 DevOps, L2 Dev, L3 DBA/Specialist)

6. OBSERVABILITY STANDARDS
   - All services: structured logging (JSON), correlation IDs, distributed tracing
   - SLOs: Payment API availability 99.95% | P99 latency < 200ms
   - Alerting: PagerDuty (P1/P2 auto-page), Datadog monitors for SLO breach
   - Dashboard: Datadog team dashboards required for all new services

7. KNOWN TECHNICAL DEBT (high priority)
   - Legacy Oracle DB (payments_core schema): 3.2M lines, partially migrated to Azure SQL
   - DB migration tooling: Liquibase in use but rollback scripts missing for 34% of changesets
   - Test coverage gap: 62% vs 80% standard (SonarQube gate currently bypassed with annotation)
   - Monorepo rebuild: full rebuild triggered on any change (incremental build not configured)
   - Remaining manual infra: 55% of SIT environment still manually provisioned

8. AI TOOL USAGE POLICY
   - GitHub Copilot Enterprise: approved for all code suggestion use
   - Azure OpenAI API: approved for internal tooling and automation
   - Data restriction: no customer PII or PCI-DSS cardholder data may be sent to any AI API
   - Code review: AI-generated code subject to same review standards as human code
   - Logging: all AI-assisted changes must be noted in PR description
```

---

### Document 3: Tool & Licence Inventory

**Section:** "Tool & Licence Inventory" → paste the text below

```
US BANK DIGITAL BANKING — TOOL & LICENCE INVENTORY
Team Phoenix | Payments & Transfers | January 2026

DEVELOPMENT TOOLS
Tool                    | Vendor     | Licences | Active | Monthly Cost | Contract End
GitHub Enterprise       | GitHub     | 500      | 487    | $22,000      | Dec 2026
GitHub Copilot Ent      | GitHub     | 100      | 34     | $3,900       | Dec 2026
JetBrains All Products  | JetBrains  | 15       | 12     | $1,200       | Jun 2026
VS Code (OSS)           | Microsoft  | -        | -      | $0           | -

ALM & PROJECT
Jira Software Cloud     | Atlassian  | 50       | 47     | $4,700       | Mar 2026
Confluence Cloud        | Atlassian  | 50       | 45     | $2,300       | Mar 2026
Miro                    | Miro       | 20       | 16     | $1,600       | Dec 2026

CI/CD & DEVOPS
GitHub Actions          | GitHub     | Included | -      | Included     | Dec 2026
JFrog Artifactory       | JFrog      | Enterprise| -     | $8,400/mo    | Jun 2026
SonarQube Enterprise    | Sonar      | Enterprise| -     | $6,200/mo    | Sep 2026
Azure Kubernetes (AKS)  | Microsoft  | Pay-as-go | -     | ~$12,000/mo  | -
Terraform Enterprise    | HashiCorp  | 50 users | 8      | $3,500/mo    | Dec 2026
Helm                    | CNCF (OSS) | -        | -      | $0           | -

TESTING
Selenium Grid           | OSS        | -        | -      | $0           | -
JMeter                  | Apache OSS | -        | -      | $0           | -
Postman                 | Postman    | 15       | 14     | $900/mo      | Jun 2026
Snyk                    | Snyk       | Enterprise| -     | $4,200/mo    | Dec 2026

MONITORING & SECURITY
Datadog                 | Datadog    | Pro 15   | 15     | $8,100/mo    | Jun 2026
PagerDuty               | PagerDuty  | 20       | 18     | $2,400/mo    | Sep 2026
Splunk Enterprise SIEM  | Splunk     | Enterprise| -     | $15,000/mo   | Dec 2026
OWASP ZAP               | OWASP OSS  | -        | -      | $0           | -

AI & AUTOMATION
Azure OpenAI API        | Microsoft  | Pay-as-go | -     | ~$1,200/mo   | -
GitHub Copilot Ent      | GitHub     | 100      | 34     | $3,900/mo    | Dec 2026
(NOTE: 66 unused Copilot seats — $2,574/mo unrecovered capacity)

UNUSED / UNDERUTILISED CAPACITY:
- 66 unused GitHub Copilot Enterprise seats ($2,574/mo waste)
- Terraform Enterprise: 50 seats licensed, only 8 active
- Miro: 4 unused seats
- JetBrains: 3 unused seats
```

---

### Document 4: Security & Compliance Policy

**Section:** "Security & Compliance Policy" → paste the text below

```
US BANK DIGITAL BANKING — SECURITY & COMPLIANCE POLICY v3.2
Payments & Transfers | CISO Office Approved | September 2025

1. REGULATORY FRAMEWORKS IN SCOPE
   1.1 PCI-DSS Level 1 — Payment Card Industry Data Security Standard
       - All features in cardholder data environment (CDE) require security review
       - Mandatory external penetration testing for any change to CDE components
       - Pen-test SLA: 5 business days (external vendor: SecureWorks)
       - Annual compliance audit: January each year
   1.2 SOC 2 Type II
       - Controls assessed annually by KPMG
       - Continuous control monitoring required for Trust Services Criteria
   1.3 APRA CPS 234 (Information Security)
       - Incident notification to APRA within 72 hours for material incidents
       - Third-party service provider risk assessments annually
   1.4 ISO 27001
       - ISMS certification maintained — annual re-certification

2. CHANGE MANAGEMENT REQUIREMENTS
   2.1 All production changes require Change Advisory Board (CAB) approval
       - CAB meets every Tuesday 2:00pm Central Time
       - Submission deadline: Monday 9:00am (48 hours prior)
       - Approval required from: CTO, CISO, Release Manager
       - Emergency changes: CTO + CISO approval via ServiceNow emergency flow
   2.2 Change categories:
       - Standard (pre-approved, low risk): CAB notification only, can deploy same-day
       - Normal (moderate risk): Full CAB review, deploy in next window
       - Emergency (P1 incident response): Emergency CAB, 2-approver expedited

3. AI / LLM DATA HANDLING POLICY
   3.1 Approved AI tools: GitHub Copilot Enterprise, Azure OpenAI (via Azure)
   3.2 Data restrictions:
       - PCI-DSS cardholder data (CHD): MUST NOT be sent to any AI API
       - Personally Identifiable Information (PII): Anonymisation required before AI processing
       - Internal source code: Permitted for GitHub Copilot (Enterprise tier with data isolation)
       - Production data: Not permitted in development/test environments
   3.3 AI code review: All AI-generated code subject to standard review process
   3.4 Model training: No customer data may be used to fine-tune external models

4. DEPLOYMENT WINDOWS
   - Production deployments: Wednesday 10:00pm – Thursday 2:00am Central Time only
   - Blackout periods: Thursday 2:00am – Monday 10:00pm (no production changes)
   - Exception: P1 incidents only, with emergency CAB approval
   - Q4 freeze period: November 15 – January 5 (no non-critical changes)

5. SECURITY SCANNING REQUIREMENTS
   5.1 All PRs must pass: SonarQube SAST, Snyk dependency scan, Trivy container scan
   5.2 DAST (dynamic scanning): Required for any API changes in PCI-DSS scope
       - Current tooling: OWASP ZAP (manual configuration, not in CI pipeline)
   5.3 Secrets scanning: GitHub Advanced Security (ghas) enabled on all repos

6. INCIDENT MANAGEMENT
   6.1 Severity levels:
       - P1: Payment processing failure or CHD breach (MTTR target: 4 hours)
       - P2: Degraded payment performance > 10% error rate (MTTR target: 1 day)
       - P3: Non-payment feature issues (MTTR target: 1 week)
   6.2 On-call coverage: DevOps 24/7, Dev team on-call rotation, DBA Mon–Fri 8am–6pm
   6.3 Post-mortem: Required for all P1 and P2 incidents within 5 business days
```

---

### Document 5: Annual OKRs / Strategic Goals

**Section:** "Annual OKRs / Strategic Goals" → paste the text below

```
US BANK DIGITAL BANKING — 2026 OBJECTIVES & KEY RESULTS
Team Phoenix | Payments & Transfers | Q1 2026

COMPANY OBJECTIVES (from Board)
OBJ-C1: Grow digital payment transaction volume by 25% in 2026
OBJ-C2: Achieve top-3 NPS ranking in consumer banking by Q3 2026
OBJ-C3: Reduce technology operating cost by 12% while increasing delivery velocity

DIGITAL BANKING DIVISION OBJECTIVES
OBJ-D1: Accelerate Payments & Transfers feature delivery
  KR1: Reduce mean lead time from 42 days to 20 days by Q3 2026
  KR2: Increase deployment frequency from weekly to 3× per week by Q4 2026
  KR3: Achieve DORA "High Performer" rating by Q4 2026

OBJ-D2: Improve platform reliability for payment processing
  KR1: Reduce mean time to restore (MTTR) from 2.3 days to < 8 hours by Q3 2026
  KR2: Reduce change failure rate from 12% to < 7% by Q3 2026
  KR3: Achieve 99.97% payment API availability (up from 99.94%)

OBJ-D3: Activate AI-assisted engineering at scale
  KR1: Increase GitHub Copilot adoption from 34% to 85% of engineering team by Q2 2026
  KR2: Reduce code review cycle time from 18 hours to 6 hours by Q2 2026
  KR3: Automate 90%+ of regression testing for standard payment flows by Q3 2026

OBJ-D4: Modernise infrastructure and reduce technical debt
  KR1: Complete Oracle → Azure SQL migration for payments_core by Q4 2026
  KR2: Increase infrastructure automation (IaC) from 45% to 80% by Q4 2026
  KR3: Increase automated test coverage from 62% to 80% by Q2 2026

TEAM PHOENIX SPECIFIC OKRs (Q1 2026)
OBJ-T1: Launch Real-Time Payment (RTP) enhancements
  KR1: Deliver 3 RTP features in Q1 (vs 2 in Q4 2025)
  KR2: RTP feature lead time < 15 days per feature

OBJ-T2: Technical debt reduction
  KR1: Write rollback scripts for top-50 Liquibase changesets by end of Q1
  KR2: Increase test coverage from 62% to 70% by end of Q1

OBJ-T3: AI adoption
  KR1: 100% of team trained on GitHub Copilot Enterprise features by Jan 31
  KR2: All new PRs include Copilot usage note in PR description by Feb 15
```

---

### Document 6: DORA Metrics Report

**Section:** "DORA Metrics Report" → paste the text below

```
US BANK TEAM PHOENIX — DORA METRICS REPORT
Q3–Q4 2025 | Generated: January 2026

EXECUTIVE SUMMARY
Team Phoenix is classified as a MEDIUM DORA performer based on Q3–Q4 2025 data.
Benchmark source: DORA Accelerate State of DevOps Report 2024 (financial services cohort).

CORE 4 DORA METRICS

1. DEPLOYMENT FREQUENCY: Once per week (Medium)
   - Data source: GitHub Actions deployment logs + Jira release tracker
   - Q3 2025: 36 production deployments over 13 weeks = 2.8/week average
   - Q4 2025: 47 production deployments over 13 weeks = 3.6/week average
   - All deployments batched into Wednesday release window (10pm–2am Central)
   - Constraint: CAB approval process prevents ad-hoc deployments
   - DORA benchmark: Elite = multiple/day | High = weekly | Medium = monthly | Low = <6 months

2. LEAD TIME FOR CHANGES: 1–2 weeks (Medium)
   - Data source: Jira cycle time reports + GitHub commit-to-deploy tracking
   - Median commit-to-production: 9.4 working days (P50)
   - 90th percentile: 18.2 working days (P90)
   - Lead time breakdown:
     * Development: 2.1 days
     * Code review wait: 2.3 days
     * CI/CD pipeline: 0.5 days
     * Mandatory pen-testing (PCI-DSS): 5.2 days
     * CAB approval + deployment window: 3.4 days
   - Primary bottleneck: PCI-DSS pen-testing gate

3. CHANGE FAILURE RATE: 12% (Medium)
   - Data source: PagerDuty incident log + post-mortem database
   - Q3–Q4 combined: 47 deployment-related incidents / 392 total deployments
   - Root cause breakdown:
     * Database migration failures: 29 incidents (61%)
     * Environment parity gaps (SIT vs prod): 11 incidents (23%)
     * Insufficient test coverage: 7 incidents (15%)
   - Cost per incident: ~$180,000 (incident response + remediation + customer impact)
   - Annual cost of failures: ~$8.5M

4. MEAN TIME TO RESTORE (MTTR): 1–7 days (Medium)
   - Data source: PagerDuty MTTR analytics + incident post-mortem database
   - P50 MTTR: 2.3 calendar days
   - P90 MTTR: 6.1 calendar days
   - P10 MTTR (fast resolutions): 4.2 hours
   - By incident type:
     * Application bugs: 18.4 hours median
     * Database incidents: 4.7 days median (DBA availability constraint)
     * Infrastructure issues: 2.1 hours median
   - 34% of incidents required cross-team escalation (+18.4 hours average)

EXTENDED METRICS

5. CI BUILD DURATION: 24 minutes average (Above target of < 10 minutes)
   - 12 of 24 minutes is dependency resolution (no build caching)
   - P90 build time: 41 minutes
   - Failed builds add 8.4 minutes for retry

6. CODE REVIEW CYCLE TIME: 18 hours median
   - P90: 34 hours
   - Requires 2 senior engineer approvals
   - Average PR size: 847 lines changed
   - PR review flagged as top flow blocker in 4 consecutive retrospectives

7. AUTOMATED TEST COVERAGE: 62%
   - Target: 80% (SonarQube quality gate — currently annotated to bypass)
   - 38% of code paths untested
   - Manual testing required for complex payment flows

8. MEAN TIME TO DETECT (MTTD): 3 hours
   - PagerDuty alert volume: 1,847 alerts/month
   - False positive rate: 18% (340 false positives/month causing alert fatigue)
   - Customer-reported incidents: 23% detected by customers before monitoring

DORA PERFORMER CLASSIFICATION: MEDIUM
BENCHMARK COMPARISON (Financial Services cohort, DORA 2024):
  - Elite: 8% of financial services organisations
  - High: 23%
  - Medium: 41% (Team Phoenix sits here)
  - Low: 28%

IMPROVEMENT TARGETS (to reach High Performer):
  - Deployment Frequency: Once/week → 3-4×/week
  - Lead Time: 9.4 days → 3-5 days
  - Change Failure Rate: 12% → < 7%
  - MTTR: 2.3 days → < 1 day
```

---

### Document 7: Sprint Retrospective Notes (Last 2 Sprints)

**Section:** "Sprint Retrospective Notes (last 2)" → paste the text below

```
TEAM PHOENIX — SPRINT RETROSPECTIVE NOTES
Sprint 24 (Dec 2–13, 2025) and Sprint 25 (Dec 16–Jan 3, 2026)

=== SPRINT 24 RETROSPECTIVE — Dec 13, 2025 ===
Facilitator: Tom Bradley (Scrum Master)
Attendees: Full Team Phoenix (12 people)
Format: Start/Stop/Continue + Dot Voting

WHAT WENT WELL (Continue):
✅ Deployed 4 features in sprint — best velocity of Q4
✅ Real-time payment alert feature well-received in UAT
✅ James and Sophie's pair programming on the RTP API was highly effective
✅ Raj's new Helm chart reduced deployment config errors

WHAT DIDN'T GO WELL (Stop/Fix):
❌ [3 votes] PR reviews still blocking — waited 22 hours for James's review on Thursday
   → James flagged he's carrying 6 active PRs to review simultaneously
❌ [5 votes] Pen-testing gate delayed the payment limits feature by a full week
   → SecureWorks took 6 days (expected 5). Feature missed sprint by 1 day.
❌ [2 votes] SonarQube quality gate is blocking PRs — coverage dropped to 59% this sprint
   → Aisha's new service had no tests (time pressure). Gate was bypassed with annotation.
❌ [4 votes] Wednesday release window is a source of anxiety — pressure to batch everything
   → Carlos noted: "We merged 6 PRs in 2 days just to make the Wednesday window"

WHAT SHOULD WE START (Start):
💡 Use GitHub Copilot for PR descriptions — reduces reviewer effort (Jennifer's suggestion)
💡 Split large PRs — team agrees 400-line limit as soft target starting next sprint
💡 Investigate AI-assisted code review tools — reduce wait time

ACTION ITEMS:
1. Tom to book GitHub Copilot Enterprise training session (all 12 members) — Jan 10 [OWNER: Tom]
2. James + Marcus to define PR size guidelines for the team wiki [OWNER: James, Due: Dec 20]
3. Jennifer to raise risk-tiered deployment model with CAB chair [OWNER: Jennifer, Due: Jan 15]
4. Raj to investigate PR size enforcement via GitHub repo rules [OWNER: Raj, Due: Dec 20]

=== SPRINT 25 RETROSPECTIVE — Jan 3, 2026 ===
Facilitator: Tom Bradley (Scrum Master)
Attendees: Full Team Phoenix minus Carlos (holiday)
Format: 4Ls (Liked, Learned, Lacked, Longed For)

LIKED:
✅ GitHub Copilot training session (Jan 3) was excellent — 9/10 satisfaction
✅ New PR description template (from Copilot) is saving reviewers 15-20 min per PR
✅ DB rollback script template (created by Maria) prevented one incident this sprint
✅ Raj's Terraform module for SIT environment config saved 3 hours of DevOps time

LEARNED:
📖 Copilot generates better code with detailed comments in the function spec
📖 Incremental Terraform changes are much safer than full-state applies
📖 MTTD can be improved significantly with better alert correlation rules

LACKED:
❌ [6 votes] STILL waiting too long for CAB approvals — Jennifer's meeting with CAB was delayed
   → Risk-tiered model discussion pushed to Jan 20 CAB meeting
❌ [3 votes] Test coverage still low — 62%, need concrete plan to reach 80%
❌ [2 votes] DBA dependency for DB incidents — Priya's Friday incident waited until Monday
   → DBA (Maria) only available Mon–Fri business hours. Weekend incidents unresolved.
❌ [4 votes] Build time is frustrating — 40-minute build due to large dependency tree
   → Raj found Gradle build cache option — has a spike planned for Sprint 26

LONGED FOR:
💭 "I wish we could deploy when we're ready, not on Wednesdays" — repeated by 4 people
💭 "I wish AI could do the first pass on PRs — catch the easy stuff before I look at it"
💭 "I wish our tests ran in parallel — sequential Selenium suite takes 2 hours"
💭 "I wish the monitoring could tell me WHERE the problem is, not just that there is one"

SPRINT 25 VELOCITY: 38 story points (target: 42 — below target for 2nd sprint)
SPRINT 25 REASON FOR MISS: 1 feature blocked by CAB approval timing (4 points spillover)

OUTSTANDING RISKS IDENTIFIED IN RETROS:
- CAB gate process — escalation to Michael Chen (CTO) needed if Jan 20 meeting fails
- Test coverage gap — tech debt sprint planned for Sprint 28 (Feb 10–21)
- Build speed — Raj's Gradle cache spike in Sprint 26 (Jan 20–31)
- DBA availability — Tom to raise with David Park for 24/7 on-call rota review
```

---

### URLS TO PROVIDE

The following URLs can be entered into any URL fetch fields in the platform or document upload sections. These are realistic public references the platform can use as context:

| Purpose | URL | What It Adds |
|---------|-----|-------------|
| DORA 2024 Report | `https://dora.dev/research/2024/dora-report/` | DORA benchmark bands for financial services |
| DORA Metrics Guide | `https://dora.dev/guides/dora-metrics-four-keys/` | Metric definitions and scoring methodology |
| PCI-DSS v4.0 Summary | `https://www.pcisecuritystandards.org/document_library/` | Compliance requirements context |
| GitHub Copilot Ent Docs | `https://docs.github.com/en/copilot/about-github-copilot/github-copilot-enterprise-overview` | Tool capability context for playbook |
| Azure OpenAI Docs | `https://learn.microsoft.com/en-us/azure/ai-services/openai/overview` | AI deployment pattern context |
| LangChain Agents Docs | `https://python.langchain.com/docs/how_to/agent_executor/` | Agent orchestration reference for Option C |
| GitHub Actions Docs | `https://docs.github.com/en/actions` | CI/CD capability baseline |
| BMAD Method | `https://github.com/bmad-method/BMAD-METHOD` | ADLC / Option C conceptual grounding |
| Terraform AzureRM | `https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs` | IaC automation context |

---

## DEMO TALKING TRACK CHEAT SHEET

### Opening (2 minutes)
*"Today I'm going to show you how Team Phoenix at US Bank can map, quantify, and transform the hidden waste in their software delivery pipeline — using AI to do in 45 minutes what would normally take 3 months of consulting engagement."*

### Step 1 hook
*"Every digital bank competing with fintechs has the same problem: the core technology is modern, but the process wrapping it is still running at 2010 speed. Let's measure exactly where that time is going."*

### After DORA Assessment
*"Medium performer. That puts Team Phoenix in the 41st percentile of financial services. Not bad — but their fintech competitors? They're deploying 50 times a day. US Bank deploys once a week. That's a 50× delivery speed disadvantage."*

### After showing Current State VSM
*"8.1% flow efficiency. Picture a water pipe where 92% of the water is trapped in holding tanks before it reaches the customer. That's your software pipeline right now."*

### When showing Phase 6 (Delivery) wait time
*"80 hours. That single activity — waiting for the Wednesday release window — adds 3 days to every single feature. Every time. Forever. Until we fix it."*

### Before showing Future State options
*"The question isn't 'should we fix this?' The question is 'how fast do we want to go?' Option A gets us to High Performer. Option B puts us in the top 20% of financial services. Option C — the ADLC — makes us faster than most fintechs."*

### When showing Option C ADLC
*"Two human roles. Product Definer sets the intent. Product Builder supervises the agents and holds the production gate. Everything else — architecture, code, tests, deployment, monitoring — is handled by an orchestrated agent swarm. The future of software development isn't replacing engineers. It's giving two engineers the leverage of twenty."*

### Business Case close
*"$660K net annual benefit. 7-month payback. That's conservative — it doesn't count the revenue from shipping features 4× faster than competitors, or the compliance cost savings from automated audit evidence. The question isn't whether to do this. The question is: which option do you start with?"*

---

## QUICK REFERENCE — KEY NUMBERS

| Metric | Current | Option A | Option B | Option C |
|--------|---------|---------|---------|---------|
| Lead Time | 42 days | 18 days | 10 days | 3 days |
| Flow Efficiency | 8.1% | 30% | 44% | 62% |
| Deploy Frequency | 1×/week | 3×/week | Daily | Continuous |
| DORA Band | Medium | High | High/Elite | Elite |
| CFR | 12% | 8% | 5% | 3% |
| MTTR | 2.3 days | 18 hours | 4 hours | 1 hour |
| Team Effort Saved | — | ~35% | ~55% | ~72% |
| Est. Net ROI (Year 1) | — | $340K | $660K | $1.1M |

---

*Guide version: 1.0 | For PDLC VSM Platform v1.0 | US Bank / Team Phoenix demo scenario*
