# STUMP — Detailed Step-by-Step Demo Guide
## US Bank | Team Phoenix | Payments & Transfers Division

**Purpose:** Complete presenter script for end-to-end platform demo with exact talking tracks, data to enter, and expected outputs for every action.
**Scenario:** US Bank's Payments & Transfers team (Team Phoenix) — 42-day lead time, 8.1% flow efficiency, bi-weekly deployments, 12% CFR, 2.3-day MTTR. We map current-state PDLC waste, assess DORA performance, analyse bottlenecks, model three future-state options, and produce a board-ready business case.

**Platform URL:** http://localhost:3001
**Backend URL:** http://localhost:8001
**Estimated runtime:** 45–60 minutes (full) | 20–25 minutes (exec highlight: Steps 3 → 5 → 7 → 8)

---

## PRE-DEMO CHECKLIST

Run through this checklist 10 minutes before the demo starts.

```bash
# 1. Start backend
cd /Users/125066/projects/pdlc-vsm-platform
source backend/venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8001

# 2. Start frontend (new terminal tab)
cd /Users/125066/projects/pdlc-vsm-platform/frontend
npm run dev
# Confirm: "Local: http://localhost:3001"

# 3. Verify health
curl http://localhost:8001/health
# Expected: {"status":"ok"}
```

**Browser setup:**
- Open http://localhost:3001 in Chrome (full screen, 1920×1080 or similar)
- Open this guide in a second monitor or window
- Close all other browser tabs (avoid notification interruptions)
- Set browser zoom to 90% for maximum content visibility
- Have the CSV file saved to Desktop (contents in Step 1 below)

**Files to prepare before demo:**
- `usbank-sprint-data.csv` — save to Desktop (full contents in Step 1)
- `usbank-devops-assessment-2025.txt` — save to Desktop (contents in Step 9)
- `usbank-team-phoenix-charter.txt` — save to Desktop (contents in Step 9)
- `team-phoenix-retrospective-q4-2025.txt` — save to Desktop (contents in Step 9)
- `usbank-compliance-framework.txt` — save to Desktop (contents in Step 9)
- `usbank-architecture-standards.txt` — save to Desktop (contents in Step 9)
- `payments-dora-benchmarks.txt` — save to Desktop (contents in Step 9)
- `usbank-okr-2026.txt` — save to Desktop (contents in Step 9)

---

## WORKFLOW OVERVIEW

```
Step 1: ALM Connect          → Project setup + CSV data upload (8 min)
Step 2: DORA Assessment      → Configure data sources + score 4 DORA dimensions (7 min)
Step 3: Current State VSM    → Review 7-phase value stream map (6 min)
Step 4: VSM Editor           → Drill into phases, edit metrics (4 min)
Step 5: Bottleneck Analysis  → AI-identified waste and root causes (5 min)
Step 6: Improvements         → Prioritised AI improvement recommendations (5 min)
Step 7: Future State VSM     → Compare Options A / B / C (ADLC) (8 min)
Step 8: Business Case        → Financial model + ROI + payback (7 min)
Step 9: Playbook Context     → Upload documents for AI playbook generation (5 min)
```

---

## OPENING FRAMING (2 minutes — before touching the screen)

Deliver this before navigating to the platform:

> "Most engineering organisations have never measured their product delivery lifecycle end-to-end. They track velocity and sprint points, but they have no idea where the time is actually going — which phases are burning days waiting for approvals, which activities are absorbing the most human effort, and where AI could compress that timeline by 60–80%. This platform answers those questions with data, and then gives you three investment-ready options to fix it — each with a specific ROI, payback period, and 90-day implementation roadmap."

> "Today we're running this for Team Phoenix at US Bank — the Payments & Transfers engineering team. They're a Medium DORA performer. Their current lead time from feature concept to production is 42 days. Their flow efficiency — the percentage of that time spent on actual productive work — is 8.1%. That means 91.9% of the time a feature spends in their pipeline is pure waste: waiting, queuing, re-work loops, approval gates. Let's make that visible."

**Pause. Let that number land. Then open the browser.**

---

## STEP 1 — ALM Connect
**Page:** http://localhost:3001/alm-connect
**Time:** 8 minutes
**Story:** "First, we tell the platform who we are and where our data lives."

### What You'll See on Screen

The ALM Connect page opens with a two-panel layout: a **Project Setup** form on the left and an **ALM Data Source** configuration panel on the right. The left panel has 6 form fields. The right panel shows a grid of ALM tool tiles (Jira, GitHub, Azure DevOps, CSV File Upload, Linear, Rally).

A progress indicator at the top shows: `1. Project Setup → 2. Connect ALM → 3. Data Preview → 4. VSM`.

---

### Sub-step 1a: Project Setup Form

**Talking track:**

> "We start by telling the platform who this team is. Every field feeds into the AI context — the industry selector, for example, activates banking-specific DORA benchmarks and PCI-DSS compliance patterns in the bottleneck and improvement agents."

**Type these exact values into the Project Setup form:**

| Field | Exact Value to Enter |
|-------|---------------------|
| Project Name | `US Bank — Digital Banking Platform` |
| Organization | `US Bank` |
| Portfolio | `Digital Banking` |
| Product Group | `Payments & Transfers` |
| Team Name | `Team Phoenix` |
| Industry | `Financial Services — Banking` |

**What you'll see after filling the form:** Each field shows a green checkmark as you tab out. The Industry dropdown, when set to "Financial Services — Banking", triggers a subtle indicator: `Banking benchmarks loaded — DORA calibration active`.

Click **"Next: Connect ALM Tool →"** (blue button, bottom right of left panel).

**Transition:** "Now the platform asks where our delivery data lives."

---

### Sub-step 1b: ALM Data Source — CSV Upload

**Talking track:**

> "In a real engagement, we'd connect directly to Jira or GitHub via API. For this demo, we're using a CSV export from Team Phoenix's Jira instance — 25 work items from their last three sprints, spanning all 7 PDLC phases."

**What you'll see on screen:** The right panel is now active. Six tool tiles are visible: Jira (blue), GitHub (black), Azure DevOps (purple), CSV File Upload (grey), Linear (indigo), Rally (orange). Each tile has a connect button and a brief description.

Click the **"CSV File Upload"** tile. It expands to show a file drop zone with the text: *"Drop your CSV here or click to browse. Supported formats: Jira export, GitHub Issues, Azure DevOps, or custom format."*

Click **"Browse"** and select `usbank-sprint-data.csv` from your Desktop.

---

### The CSV File — Full Content

**Save this as `usbank-sprint-data.csv` on your Desktop before the demo.**

```csv
ticket_id,type,title,sprint,status,story_points,cycle_time_days,wait_time_days,process_time_hours,phase,assignee,created_date,completed_date
USB-2401,Epic,Real-time Payment Processing Engine,Sprint-24,Done,21,18,14,32,Architecture & UX,Sarah Chen,2025-01-05,2025-01-23
USB-2402,Story,API Gateway Rate Limiting,Sprint-24,Done,8,12,9,24,Continuous Integration,James Wright,2025-01-05,2025-01-17
USB-2403,Story,Payment Fraud Detection Rules Engine,Sprint-24,Done,13,15,11,28,Architecture & UX,Marcus Lee,2025-01-06,2025-01-21
USB-2404,Bug,Fix: Duplicate Transaction Processing on Retry,Sprint-24,Done,3,5,3,8,Code Management,Priya Sharma,2025-01-07,2025-01-12
USB-2405,Task,Update PCI-DSS Compliance Evidence Package,Sprint-24,Done,2,8,7,6,Continuous Testing,Rachel Kim,2025-01-08,2025-01-16
USB-2406,Story,OSKO Instant Payment Integration,Sprint-25,Done,13,22,17,40,Architecture & UX,Sarah Chen,2025-01-20,2025-02-11
USB-2407,Story,Real-time FX Rate Feed Integration,Sprint-25,Done,8,14,10,22,Code Management,James Wright,2025-01-20,2025-02-03
USB-2408,Story,Payment Limit Rule Engine — Customer Tier Logic,Sprint-25,Done,5,10,7,16,Backlog & Roadmap,Marcus Lee,2025-01-21,2025-01-31
USB-2409,Bug,Fix: Timezone Error in Scheduled Transfers,Sprint-25,Done,3,7,5,10,Code Management,Carlos Mendez,2025-01-22,2025-01-29
USB-2410,Epic,Mobile Payments Wallet Integration,Sprint-25,Done,21,25,19,44,Architecture & UX,Sophie Wang,2025-01-22,2025-02-16
USB-2411,Story,Push Notification for Payment Confirmation,Sprint-25,Done,5,9,7,14,Continuous Delivery,Priya Sharma,2025-01-23,2025-02-01
USB-2412,Task,Configure GitHub Actions — Payment Service Pipeline,Sprint-25,Done,2,6,4,8,Continuous Integration,Raj Patel,2025-01-24,2025-01-30
USB-2413,Story,Batch Payment File Processing — ISO 20022,Sprint-26,Done,13,19,15,32,Architecture & UX,Marcus Lee,2025-02-03,2025-02-22
USB-2414,Story,Payment Status Webhook — Partner Banks,Sprint-26,Done,8,13,10,20,Code Management,James Wright,2025-02-03,2025-02-16
USB-2415,Bug,Fix: CAB Submission Form Validation Error,Sprint-26,Done,2,4,3,6,Continuous Delivery,Rachel Kim,2025-02-04,2025-02-08
USB-2416,Story,Account Statement PDF Export — Accessibility,Sprint-26,Done,5,11,8,16,Continuous Testing,Sophie Wang,2025-02-05,2025-02-16
USB-2417,Story,Two-Factor Auth Upgrade — TOTP Standard,Sprint-26,Done,8,16,12,26,Architecture & UX,Sarah Chen,2025-02-06,2025-02-22
USB-2418,Task,SonarQube Quality Gate Threshold Review,Sprint-26,Done,1,3,2,4,Continuous Integration,Raj Patel,2025-02-06,2025-02-09
USB-2419,Story,Payment Dispute Self-Service Portal,Sprint-26,In Progress,13,20,15,34,Backlog & Roadmap,Priya Sharma,2025-02-10,
USB-2420,Bug,Fix: Intermittent Timeout — High-Volume Transfer,Sprint-26,Done,5,9,7,14,Monitoring & Feedback,Carlos Mendez,2025-02-11,2025-02-20
USB-2421,Story,Merchant Category Code Enrichment,Sprint-27,Done,8,12,9,18,Code Management,James Wright,2025-02-17,2025-02-29
USB-2422,Story,Datadog SLO Dashboard — Payments API,Sprint-27,Done,5,8,6,12,Monitoring & Feedback,Raj Patel,2025-02-17,2025-02-25
USB-2423,Epic,Open Banking API — CDR Compliance,Sprint-27,In Progress,21,24,18,42,Architecture & UX,Marcus Lee,2025-02-18,
USB-2424,Story,Automated Regression Suite — NPP Payments,Sprint-27,Done,8,14,11,22,Continuous Testing,Rachel Kim,2025-02-18,2025-03-03
USB-2425,Task,Liquibase Migration Script — Payment Schema v3.1,Sprint-27,Done,2,5,4,8,Continuous Integration,Carlos Mendez,2025-02-19,2025-02-24
```

**What you'll see after uploading:** The platform shows a parsing progress bar (1–2 seconds), then a **Data Preview** panel appears below the upload zone:

```
Parsed: 25 tickets | 7 phases detected | Date range: Jan 5 – Mar 3, 2025
Avg Cycle Time: 12.4 days | Avg Wait Time: 9.5 days | Avg Process Time: 20.8 hrs
Flow Efficiency: 8.1% | Estimated Lead Time: 42.3 days
```

**Talking track at the data preview:**

> "The platform has parsed all 25 tickets and automatically detected all 7 PDLC phases. Notice the headline number: 8.1% flow efficiency. That means for every hour Team Phoenix spends on productive work, there are 11.3 hours of pure waiting. Before we dive into where exactly that time is going, let's layer in DORA — the industry benchmark that tells us whether this is an outlier or industry norm."

> "In banking, 10–15% flow efficiency is unfortunately typical. Elite-performing teams in financial services — the top 5% — run at 35–45%. Our job today is to show what it would take to get Team Phoenix into that elite band."

Click **"Apply to VSM →"** (green button at bottom of data preview panel).

**Wow moment:** The flow efficiency gauge animates from 0 to 8.1%, with the needle sitting deep in the red zone. A tooltip appears: *"Industry median for Financial Services: 12.3%. Elite benchmark: 38%."*

**Transition to Step 2:** "Now let's calibrate our DORA baseline. This is what tells the AI whether Team Phoenix's 8.1% is caused by governance constraints, technical debt, or team maturity — because the fix is different for each."

---

## STEP 2 — DORA Assessment
**Page:** http://localhost:3001/dora-assessment
**Time:** 7 minutes
**Story:** "DORA is the industry's gold standard for software delivery performance — 33,000 organisations, 9 years of data. We use it to baseline Team Phoenix and calibrate every metric in the VSM."

### What You'll See on Screen

The DORA Assessment page has three sections visible in the top navigation: **Data Sources**, **Assessment**, and **Results**. You are on the **Data Sources** tab by default.

The page shows a grid of 4 source type cards: **Repository** (GitHub/GitLab icon), **Project Management** (Jira/Linear icon), **Monitoring** (Splunk/Datadog icon), **Code Quality** (SonarQube icon). Each card has an "+ Add Source" button.

A banner at the top reads: *"Connect your data sources to enable AI-assisted DORA scoring. You can also complete the assessment manually."*

---

### Sub-step 2a: Configure Data Sources

**Talking track:**

> "In a real engagement, we connect directly to the team's toolchain. The AI reads deployment frequency from GitHub, incident data from PagerDuty, and code quality signals from SonarQube — and produces an evidence-backed DORA score. Let me show you the four sources we'd wire up for Team Phoenix."

**Add Source 1 — Repository (GitHub):**

Click **"+ Add Source"** under the Repository card. A modal appears with fields:

| Field | Value to Enter |
|-------|---------------|
| Source Type | `GitHub` |
| URL | `https://github.com/usbank/payments-api` |
| Label | `Payments API Repository` |

Click **"Save Source"**. The card shows a green "Connected" badge and the label "Payments API Repository".

**Add Source 2 — Project Management (Jira):**

Click **"+ Add Source"** under Project Management:

| Field | Value to Enter |
|-------|---------------|
| Source Type | `Jira` |
| URL | `https://usbank.atlassian.net/jira/software/projects/PAY` |
| Label | `Payments Jira Board` |

Click **"Save Source"**.

**Add Source 3 — Monitoring (Splunk):**

Click **"+ Add Source"** under Monitoring:

| Field | Value to Enter |
|-------|---------------|
| Source Type | `Splunk` |
| URL | `https://usbank.splunk.com/en-US/app/payments` |
| Label | `Production Monitoring` |

Click **"Save Source"**.

**Add Source 4 — Code Quality (SonarQube):**

Click **"+ Add Source"** under Code Quality:

| Field | Value to Enter |
|-------|---------------|
| Source Type | `SonarQube` |
| URL | `https://sonarqube.usbank.com/dashboard?id=payments-api` |
| Label | `Code Quality Dashboard` |

Click **"Save Source"**.

**What you'll see:** All four source cards now show green "Connected" badges. A summary bar appears: *"4 sources configured — AI scoring available."*

Click the **"Assessment"** tab.

---

### Sub-step 2b: DORA Metric Scoring

**Talking track:**

> "The Assessment tab has 73 questions across four dimensions. In practice, the AI pre-fills this from the connected data sources and we review for accuracy. For demo purposes, I'll show you the key questions in each dimension and the scores that reflect Team Phoenix's actual performance."

**What you'll see:** Four accordion sections: Cultural Practices, Measurement & Visibility, Process & Governance, Technical Practices. Each expands to reveal 15–20 questions on a 1–5 scale (radio buttons or sliders). A progress bar at the top shows completion percentage.

**Expand Cultural Practices — enter these 5 key responses:**

| Question | Score | Notes |
|----------|-------|-------|
| "Team has psychological safety to report failures without blame" | 4 | Strong — post-mortems are blameless |
| "Leadership actively sponsors engineering improvement" | 4 | CTO is active champion |
| "Team experiments with new practices regularly" | 3 | Some experimentation; GitHub Copilot rollout example |
| "Failures are used as learning opportunities" | 3 | Post-mortems monthly but findings rarely actioned |
| "Cross-functional collaboration is smooth and low-friction" | 2 | CISO and ARB dependencies cause friction |

**Expand Measurement & Visibility — enter these 5 key responses:**

| Question | Score | Notes |
|----------|-------|-------|
| "Team tracks deployment frequency with tooling" | 3 | Tracked in ServiceNow but manual |
| "Lead time for changes is measured and visible" | 2 | Not consistently measured |
| "Change failure rate is tracked and reported" | 3 | Incident log in Jira |
| "MTTR is tracked from detection to resolution" | 2 | PagerDuty has data; not reviewed in retrospectives |
| "Flow efficiency is measured across the PDLC" | 1 | Not measured — this is the first time |

**Expand Process & Governance — enter these 5 key responses:**

| Question | Score | Notes |
|----------|-------|-------|
| "Deployment process is well-documented and repeatable" | 3 | Runbooks exist; some manual steps |
| "Change approval process is proportionate to risk" | 1 | All changes go through full CAB regardless of risk |
| "Rollback procedures are automated and tested" | 2 | Partially — DB migrations lack rollback scripts |
| "Release cadence is predictable and scheduled" | 3 | Wednesday releases — predictable but infrequent |
| "Testing gates are automated and don't require manual scheduling" | 2 | Pen-test and UAT still manual/scheduled |

**Expand Technical Practices — enter these 5 key responses:**

| Question | Score | Notes |
|----------|-------|-------|
| "CI pipeline runs on every commit and is under 10 minutes" | 2 | 24-minute build — over target |
| "Test coverage meets or exceeds 80% threshold" | 2 | 62% — SonarQube gate currently bypassed |
| "Infrastructure is managed as code (IaC)" | 2 | 45% IaC; 55% still manual |
| "Secrets management follows zero-trust principles" | 4 | Azure Key Vault in place |
| "Feature flags enable deployment decoupled from release" | 2 | Some feature flags; not systematic |

Click **"Calculate DORA Score"** (blue button, bottom of page).

---

### Sub-step 2c: DORA Results

**What you'll see:** The Results tab animates into view with four gauge charts, one per DORA dimension, and an overall maturity band indicator.

**Expected AI Output — DORA Scores:**

| DORA Metric | Current Value | Score | Band |
|-------------|--------------|-------|------|
| Deployment Frequency | Bi-weekly (every 2 weeks) | 2.1 / 5 | Medium |
| Lead Time for Changes | 42 days | 1.8 / 5 | Low-Medium |
| Change Failure Rate | 12% | 2.0 / 5 | Medium |
| Mean Time to Restore | 2.3 days (55.2 hours) | 1.9 / 5 | Medium |
| **Overall DORA Maturity** | **WALK** | **2.0 / 5** | **Medium** |

Below the gauges, the AI renders a **findings panel** with three callout boxes:

**Critical Finding (red):**
*"Deployment Frequency is the primary bottleneck. The Change Advisory Board (CAB) process requires bi-weekly scheduling with 48-hour advance notice, forcing all changes — regardless of risk level — into fortnightly release batches. This single governance constraint is responsible for an estimated 13–16 days of avoidable lead time per feature."*

**High Finding (amber):**
*"Test coverage at 62% is 18 points below the 80% quality gate. The SonarQube gate is currently bypassed via annotation, creating compliance debt. Any PCI-DSS audit would flag this as a control weakness. Fixing this is a prerequisite for implementing automated risk-based deployment."*

**Observation (blue):**
*"GitHub Copilot is licensed for 100 seats but only 34 are active (34% adoption). Teams using Copilot report 20–30% reduction in coding time. Activating the remaining 66 seats and providing structured onboarding represents an immediate, low-cost productivity gain with existing budget."*

**Talking track at results:**

> "WALK maturity means Team Phoenix is doing the basics right — they have CI/CD pipelines, automated testing, monitoring. But they're being held back by governance constraints, not technical capability. The CAB gate, the Wednesday-only release window, the mandatory external pen-test for all PCI-DSS scope changes — these are process decisions, not technology limitations. That's actually good news, because process changes are faster and cheaper than technology re-platforming."

> "The 2.3-day MTTR is the metric I'd flag to the CISO. When something goes wrong in payments, the team takes 55 hours on average to restore service. The main driver is the DBA team's business-hours-only availability — database incidents wait overnight. That's a risk posture issue, not an engineering issue."

Click **"Apply DORA Calibration to VSM →"** (green button, bottom right).

**What happens:** A loading spinner appears for 2–3 seconds with the text: *"Calibrating VSM metrics to DORA Medium/Walk baseline..."* Then the platform navigates to the Current State VSM.

**Wow moment:** The DORA maturity band indicator — a horizontal bar showing CRAWL → WALK → RUN → FLY — highlights "WALK" in amber with an animated pulse. The label reads: *"Team Phoenix is a WALK-stage performer. The gap to RUN requires solving 3 key constraints. The gap to FLY requires the AI-Driven Lifecycle."*

**Transition:** "Now let's see exactly where Team Phoenix's 42 days goes. The VSM is going to make this very concrete."

---

## STEP 3 — Current State VSM
**Page:** http://localhost:3001/vsm-current
**Time:** 6 minutes
**Story:** "Here's the current state value stream map — 7 phases, 36 activities, and a very clear picture of where the waste lives."

### What You'll See on Screen

The Current State VSM page renders a horizontal swimlane diagram. Seven phase boxes are displayed left to right, each containing:
- Phase name and number
- A process time (PT) bar in blue
- A wait time (WT) bar in red/orange
- A flow efficiency (FE%) badge
- Connector arrows between phases showing the flow

At the bottom of the diagram, a summary bar shows:
- Total Lead Time: **42 days**
- Total Process Time: **130 hours**
- Total Wait Time: **600 hours**
- Overall Flow Efficiency: **17.8%**

A **DORA Calibration Applied** green badge appears in the top right: *"Metrics calibrated to WALK/Medium baseline."*

---

### Walk Through Each Phase

**Talking track — use this script as you point to each phase:**

**Phase 1 — Backlog & Roadmap:**

> "Phase 1 — Backlog and Roadmap. 25 hours of process time, 72 hours of wait time. Flow efficiency 25.8%. The main culprit here is quarterly OKR alignment — features sit in the backlog for weeks waiting for the next planning cycle. And when requirements do reach the team, they're often incomplete, triggering re-refinement loops."

**Phase 2 — Architecture & UX:**

> "Phase 2 is where things get expensive. 36 hours of process time — architecture design, API contracts, UX prototyping. But 176 hours of wait time — over 7 days. The Architecture Review Board meets fortnightly. Miss the meeting and you wait two weeks. On top of that, any feature touching PCI-DSS scope requires a CISO security review with a 40-hour SLA. That's before a single line of code is written."

**Phase 3 — Code Management:**

> "Phase 3 — Code Management. This is actually the healthiest phase. 13 hours of process time, 18 hours of wait time. 41.9% flow efficiency — their best phase. But notice the 18-hour wait: that's the PR review queue. Average PR size is 850 lines, and only two senior engineers can approve payments-related code. Quick win available here."

**Phase 4 — Continuous Integration:**

> "Phase 4 — CI. Low process time, low wait time. 42.9% flow efficiency — good. But there's a hidden problem: the CI build takes 24 minutes when the elite benchmark is under 10. And the SAST gate fails 23% of first-run PRs, sending work back to Phase 3. It's a small number but it compounds across the pipeline."

**Phase 5 — Continuous Testing:**

> "Phase 5 — and here's where the pipeline breaks. 31 hours of process time, 240 hours of wait time. 11.4% flow efficiency. Two contributors: first, sequential test execution — their Selenium regression suite runs end-to-end with no parallelism, taking 4 hours when it could take 45 minutes. Second, and this is the killer — the mandatory external penetration test for all PCI-DSS scope changes. Zero hours of process time, 40 hours of wait time. An external security vendor. You can't speed that up without changing the process."

**Phase 6 — Continuous Delivery:**

> "Phase 6 — Continuous Delivery. 12 hours of process time, 56 hours of wait time. 17.6% flow efficiency. The CAB gate — Change Advisory Board — requires 48 hours advance notice and sign-off from the CTO, CISO, and Release Manager. But here's the thing: the CAB meets bi-weekly. So the actual average wait is closer to 5–7 days depending on where you are in the cycle."

**Phase 7 — Monitoring & Feedback:**

> "Phase 7 — Monitoring and Feedback. 7 hours of process time, 30 hours of wait time. 18.9% flow efficiency. MTTR of 55 hours — because database incidents can only be resolved by the DBA team, who are available Monday to Friday, 8am to 6pm. A P1 payment incident at 5pm Friday waits until Monday morning. For a regulated bank, that's an unacceptable risk posture."

**Present the full summary table:**

| Phase | PT (hrs) | WT (hrs) | FE% | Primary Bottleneck |
|-------|----------|----------|-----|-------------------|
| 1. Backlog & Roadmap | 25 | 72 | 25.8% | Quarterly planning cadence |
| 2. Architecture & UX | 36 | 176 | 17.0% | ARB queue + CISO review |
| 3. Code Management | 13 | 18 | 41.9% | PR review wait (18h median) |
| 4. Continuous Integration | 6 | 8 | 42.9% | 24-min build + SAST failures |
| 5. Continuous Testing | 31 | 240 | 11.4% | Pen-test gate + sequential testing |
| 6. Continuous Delivery | 12 | 56 | 17.6% | CAB gate + bi-weekly release |
| 7. Monitoring & Feedback | 7 | 30 | 18.9% | DBA availability gap |
| **TOTAL** | **130** | **600** | **17.8%** | |

**Wow moment — point to the Phase 5 wait bar:**

> "That red bar for Phase 5 is 240 hours. Ten working days. Just waiting. The actual testing work takes 31 hours. This is what 11.4% flow efficiency looks like — for every hour of testing work, the feature waits for 7.7 hours. Our benchmark for elite banking teams is 35% flow efficiency in this phase. The gap is 8 AI improvement actions, which we'll see in Step 6."

**Transition:** "Let me show you the VSM Editor — where we can drill into any individual activity and see exactly what's driving these numbers."

---

## STEP 4 — VSM Editor
**Page:** http://localhost:3001/vsm-editor
**Time:** 4 minutes
**Story:** "The VSM Editor gives us activity-level granularity. We can see every work step, edit the metrics as we gather better data, and watch the flow efficiency recalculate in real time."

### What You'll See on Screen

The VSM Editor displays all 7 phases as collapsible accordion rows. Each phase header shows: phase name, total PT, total WT, and FE% badge. The phases are collapsed by default.

A **"Edit Mode"** toggle is visible in the top right (currently off). An **"Add Activity"** button sits next to each phase header.

---

### Sub-step 4a: Expand Phase 5 (Continuous Testing)

Click the **Phase 5: Continuous Testing** row to expand it.

**What you'll see:** Five activity rows appear:

| Activity | Type | PT (hrs) | WT (hrs) | Owner | Tool |
|----------|------|----------|----------|-------|------|
| Automated Regression Test Suite | Automated | 4 | 8 | QA Automation | Selenium / JUnit |
| Manual SIT Testing | Manual | 16 | 12 | QA Team (4) | Jira |
| Performance / Load Testing | Manual | 6 | 8 | Performance Team | JMeter |
| Penetration Testing (PCI-DSS) | External | 0 | 168 | External Vendor | Manual |
| UAT Sign-off | Manual | 8 | 44 | BA + PO | Jira |

**Talking track:**

> "Look at Penetration Testing. Zero hours of process time — the team does nothing. But 168 hours of wait time — seven calendar days — waiting for an external security vendor to schedule and complete the test. And this happens for every single change that touches PCI-DSS scope. Now look at UAT — 44 hours of wait time just getting business stakeholders to review and sign off."

> "The combined wait for testing is 240 hours. The process work is 34 hours. If we can automate the pen-test routing — using AI-assisted DAST/SAST to assess risk level and only escalate high-risk changes to the external vendor — and use an AI UAT assistant to generate test scenarios and pre-validate acceptance criteria, we can reduce this phase's wait time by 80%."

---

### Sub-step 4b: Edit an Activity — AI UAT Simulation

**Talking track:**

> "Let me show you how we'd model the impact of the AI UAT Assistant improvement. Toggle Edit Mode on."

Click the **"Edit Mode"** toggle (top right). The toggle turns blue and a pencil icon appears on each activity row.

Click the **pencil icon** on "UAT Sign-off". An inline edit form appears with the current values pre-filled:

| Field | Current Value | New Value to Enter |
|-------|--------------|-------------------|
| Process Time (hrs) | 8 | `8` (unchanged) |
| Wait Time (hrs) | 44 | `8` |
| Activity Type | Manual | `AI-Assisted` |
| Notes | Business stakeholder UAT | `AI UAT Assistant pre-validates acceptance criteria; human approves` |

**What you'll see as you change Wait Time from 44 to 8:**

The Phase 5 flow efficiency badge updates in real time:
- Before edit: FE = 11.4%
- After edit: FE = **16.2%** (animated counter)

The overall VSM summary bar at the bottom also updates:
- Lead Time: 42 days → **38.5 days** (animated)
- Flow Efficiency: 17.8% → **19.1%** (animated)

Click **"Save Activity"**.

**Talking track:**

> "One activity edit — changing UAT wait time from 44 hours to 8 hours — and we've already moved the overall lead time by 3.5 days. The VSM editor lets consultants model improvements in real time, during the workshop. You can have a live conversation with the team, agree on what's achievable, and watch the impact update immediately."

**Wow moment:** Point to the real-time recalculation. "This is a live financial model. Every number the client gives us feeds directly into the ROI calculation in Step 8. We're not working from a spreadsheet — this is a connected analytical system."

Click the **"Edit Mode"** toggle again to turn it off. Revert the UAT wait time to 44 (for clean demo continuity) by clicking the pencil icon again and restoring the original value.

**Transition:** "Now let's let the AI do its work. The Bottleneck Analysis agent has analysed all 36 activities across 7 phases and ranked the waste by business impact."

---

## STEP 5 — Bottleneck Analysis
**Page:** http://localhost:3001/bottlenecks
**Time:** 5 minutes
**Story:** "This is where AI earns its keep. The bottleneck agent has processed the full VSM, your DORA scores, the CSV ticket data, and the industry benchmarks — and ranked every source of waste by its impact on lead time and flow efficiency."

### What You'll See on Screen

The Bottleneck Analysis page shows a ranked list of bottleneck cards on the left and a visual "waste heat map" on the right — a treemap where cell size represents wait time and colour represents severity (red = critical, amber = high, blue = medium).

At the top, a summary banner reads:
*"5 bottlenecks identified | 464 hours of recoverable wait time | Estimated lead time reduction if all addressed: 28.5 days"*

An **"Analysis Method"** indicator shows: *"AI Agent analysis — DORA-calibrated | 36 activities across 7 phases | Banking benchmarks applied"*

---

### Walk Through Each Bottleneck

**Bottleneck 1 — Critical (red badge):**

**Card shows:**
```
#1 CRITICAL — Manual SIT/UAT/Pen-test Signoff
Phase: Continuous Testing (Phase 5)
Wait Time Impact: 240 hours
% of Total Wait: 40.0%
Root Cause: Manual test environment setup, no parallel execution,
            test data dependency, external vendor scheduling for pen-test
Banking Benchmark: Top quartile teams: 28h wait | Your team: 240h wait
Gap to Benchmark: 212 hours (8.5× above benchmark)
```

**Talking track:**

> "Bottleneck one — Manual Testing Signoff — is 40% of Team Phoenix's total wait time on its own. Nearly half the pipeline waste lives in a single phase. The root causes are threefold: sequential test execution when parallelism is available, external pen-test scheduling that the team has no control over, and test data setup that's done manually before each cycle. Each has a different fix, and the AI has modelled the impact of each separately."

**Bottleneck 2 — Critical (red badge):**

**Card shows:**
```
#2 CRITICAL — Architecture Review Gate
Phase: Architecture & UX (Phase 2)
Wait Time Impact: 96 hours (of 176h total phase wait)
% of Total Wait: 16.0%
Root Cause: Sequential design reviews, fortnightly ARB cadence,
            3-day advance scheduling required, no self-service for standard patterns
Banking Benchmark: Top quartile teams: 24h wait | Your team: 96h wait
Gap to Benchmark: 72 hours (4× above benchmark)
```

**Talking track:**

> "The Architecture Review Board bottleneck is a classic governance pattern in banks. It exists for good reason — you don't want architects unilaterally making platform decisions. But the ARB was designed for a world where changes were big, infrequent, and risky. With smaller, more frequent changes, the ARB becomes a bottleneck that creates exactly the big-batch release behaviour it was trying to prevent."

**Bottleneck 3 — High (amber badge):**

**Card shows:**
```
#3 HIGH — Release Approval / CAB Gate
Phase: Continuous Delivery (Phase 6)
Wait Time Impact: 56 hours
% of Total Wait: 9.3%
Root Cause: Change Advisory Board bi-weekly cadence, 48-hour advance notice,
            manual risk assessment, VP-level sign-off from 3 approvers
Banking Benchmark: Top quartile teams: 8h wait | Your team: 56h wait
Gap to Benchmark: 48 hours (7× above benchmark)
```

**Talking track:**

> "The CAB gate is number 3 by wait time, but arguably number 1 by strategic impact. This is the process change that unlocks continuous delivery. Moving from a bi-weekly CAB to a risk-tiered model — where low-risk changes deploy automatically with evidence generated by the pipeline, and only high-risk changes go to CAB — is the single highest-leverage governance change available."

**Bottleneck 4 — High (amber badge):**

**Card shows:**
```
#4 HIGH — Feature Refinement Loop
Phase: Backlog & Roadmap (Phase 1)
Wait Time Impact: 48 hours
% of Total Wait: 8.0%
Root Cause: Incomplete requirements reaching development,
            stakeholder alignment delays, quarterly cadence forcing
            large batch planning rather than continuous refinement
Banking Benchmark: Top quartile teams: 16h wait | Your team: 48h wait
Gap to Benchmark: 32 hours (3× above benchmark)
```

**Bottleneck 5 — Medium (blue badge):**

**Card shows:**
```
#5 MEDIUM — Peer Code Review Queue
Phase: Code Management (Phase 3)
Wait Time Impact: 18 hours
% of Total Wait: 3.0%
Root Cause: Average PR size 850 lines (target: <400 lines),
            bottlenecked on 2 senior reviewers for payments code,
            no AI pre-review to reduce human review burden
Banking Benchmark: Top quartile teams: 4h wait | Your team: 18h wait
Gap to Benchmark: 14 hours (4.5× above benchmark)
```

**Full bottleneck summary table:**

| # | Bottleneck | Phase | WT Impact | Severity | Gap to Benchmark |
|---|-----------|-------|-----------|----------|-----------------|
| 1 | Manual SIT/UAT/Pen-test Signoff | Testing | 240h | Critical | 8.5× |
| 2 | Architecture Review Gate | Architecture & UX | 96h | Critical | 4× |
| 3 | Release Approval / CAB Gate | Continuous Delivery | 56h | High | 7× |
| 4 | Feature Refinement Loop | Backlog & Roadmap | 48h | High | 3× |
| 5 | Peer Code Review Queue | Code Management | 18h | Medium | 4.5× |

**Wow moment — point to the treemap:**

> "The treemap makes this unmistakeable. The giant red cell is Phase 5 testing — that's 240 hours of wait time represented visually. A junior engineer looking at this for the first time immediately knows where to focus. You don't need a consulting report to see this — the data speaks for itself."

**Transition:** "So we know exactly what's broken. Now let's look at what AI recommends we do about it — ranked by impact-to-effort ratio."

---

## STEP 6 — Improvements
**Page:** http://localhost:3001/improvements
**Time:** 5 minutes
**Story:** "The Improvements agent has generated 8 prioritised recommendations. Each one is ranked by impact-to-effort ratio, includes an effort estimate, a timeline, and a projected ROI multiplier."

### What You'll See on Screen

The Improvements page shows 8 recommendation cards arranged in a ranked list. Each card has:
- A rank number (1–8) and title
- An **impact badge** (colour-coded: green = Quick Win, blue = Strategic, purple = Transformational)
- Projected wait time reduction (hours)
- Effort reduction percentage
- ROI multiplier
- A "Learn More" expand button
- A checkbox to include in the Future State model

A **filter bar** at the top allows filtering by: All | Quick Wins | Strategic | Transformational | Phase

A **"Total Projected Impact"** banner at the top updates as you check/uncheck items:
*"8 improvements selected | Combined WT reduction: 464h | Lead time impact: −28.5 days | Blended ROI: 2.5×"*

---

### Walk Through Key Improvements

**Improvement 1 — AI UAT Assistant:**

> "Number one — the AI UAT Assistant. This is the highest-impact, quickest-win recommendation in the set. It deploys an AI agent that reads the acceptance criteria from Jira, generates test scenarios, executes them against a test environment, and presents a structured pass/fail report to the business analyst. The BA still approves — but instead of spending 44 hours scheduling and waiting for stakeholder reviews, they spend 1 hour reviewing a pre-validated report."

**Card details:**
```
#1  AI UAT Assistant                                    [Quick Win ✓]
    Phase: Continuous Testing
    Current WT: 240h → Target WT: 48h   Reduction: 192h (80%)
    Effort Reduction: 80%
    ROI Multiple: 3.2×
    Timeline: Sprint 1–2 (2–4 weeks)
    Prerequisite: Azure OpenAI API access (already licensed)
```

**Improvement 2 — AI Release Manager:**

> "Number two — AI Release Manager. This addresses the CAB gate bottleneck. The AI analyses each proposed change: reads the diff, checks against known risk patterns, evaluates test coverage, reviews compliance flags — and produces a risk assessment score in minutes. Low-risk changes go through automatically. High-risk changes still go to CAB, but now with a pre-built risk dossier. CAB review time drops from 56 hours to 14 hours average."

**Card details:**
```
#2  AI Release Manager                                  [Strategic]
    Phase: Continuous Delivery
    Current WT: 56h → Target WT: 14h    Reduction: 42h (75%)
    Effort Reduction: 60%
    ROI Multiple: 2.8×
    Timeline: Sprint 3–6 (6–12 weeks)
    Prerequisite: ServiceNow API integration
```

**Improvement 3 — AI Design Reviewer:**

> "Number three targets the Architecture Review Board. An AI design reviewer analyses proposed architecture changes against US Bank's documented standards — API design patterns, security requirements, PCI-DSS constraints, cloud platform guidelines — and produces a pre-review assessment. Standard patterns that conform to existing standards self-approve. Novel patterns get flagged for ARB with a detailed analysis that cuts the review meeting time from 2 hours to 30 minutes."

**Card details:**
```
#3  AI Design Reviewer                                  [Strategic]
    Phase: Architecture & UX
    Current WT: 96h → Target WT: 32h    Reduction: 64h (67%)
    Effort Reduction: 40%
    ROI Multiple: 2.1×
    Timeline: Sprint 4–8 (8–16 weeks)
    Prerequisite: Architecture standards documented in knowledge base
```

**Improvement 4 — ReviewAgent (Code Review):**

> "Number four is the one engineers love most. ReviewAgent is an AI code reviewer that analyses every PR before a human opens it. It flags obvious issues — security anti-patterns, missing test coverage, performance problems, naming conventions — so the human reviewer spends time on architectural decisions, not lint errors. PR review wait drops from 18 hours to 5 hours."

**Card details:**
```
#4  ReviewAgent (Code Review)                           [Quick Win ✓]
    Phase: Code Management
    Current WT: 18h → Target WT: 5h     Reduction: 13h (72%)
    Effort Reduction: 40%
    ROI Multiple: 1.9×
    Timeline: Sprint 1 (1–2 weeks)
    Prerequisite: GitHub Copilot Enterprise (already licensed — 100 seats)
```

**Improvement 5 — AI Requirements Analyst:**

> "Number five targets the backlog refinement loop. The AI Requirements Analyst reads draft feature requirements, cross-references them against existing API contracts, data models, and business rules, and identifies gaps before they reach the development team. It reduces the re-refinement loop from 48 hours of back-and-forth to a single structured requirements document that the team can execute against."

**Card details:**
```
#5  AI Requirements Analyst                             [Quick Win ✓]
    Phase: Backlog & Roadmap
    Current WT: 48h → Target WT: 12h    Reduction: 36h (75%)
    Effort Reduction: 65%
    ROI Multiple: 2.4×
    Timeline: Sprint 2–3 (4–6 weeks)
    Prerequisite: Confluence API integration + requirements templates
```

**Improvement 6 — AI Pipeline Orchestrator:**

```
#6  AI Pipeline Orchestrator                            [Strategic]
    Phase: Continuous Integration
    Current PT: 6h → Target PT: 2h      Reduction: 4h PT (67%)
    Effort Reduction: 30%
    ROI Multiple: 1.7×
    Timeline: Sprint 3–5 (6–10 weeks)
```

**Improvement 7 — AI Observability Agent:**

```
#7  AI Observability Agent                              [Strategic]
    Phase: Monitoring & Feedback
    Current WT: 30h → Target WT: 8h     Reduction: 22h (73%)
    Effort Reduction: 50%
    ROI Multiple: 2.2×
    Timeline: Sprint 5–8 (10–16 weeks)
```

**Improvement 8 — AI Backlog Prioritiser:**

```
#8  AI Backlog Prioritiser                              [Strategic]
    Phase: Backlog & Roadmap
    Current WT: 72h → Target WT: 24h    Reduction: 48h (67%)
    Effort Reduction: 45%
    ROI Multiple: 2.0×
    Timeline: Sprint 3–4 (6–8 weeks)
```

**Talking track — summary:**

> "Eight improvements. Three are Quick Wins — items we can implement in the first four weeks using tooling Team Phoenix already has licensed. The remaining five are strategic investments spanning 6–16 weeks. Combined, they recover 464 hours of wait time — more than 19 working days — from the pipeline. We'll see exactly what that does to the lead time in the Future State VSM."

**Wow moment:** Click **"Select All"** to check all 8 improvements. The Total Projected Impact banner updates:

*"All 8 improvements selected | Combined WT reduction: 464h | Lead time reduction: −28.5 days | New projected lead time: 13.5 days | New flow efficiency: 61% | Blended ROI: 2.5×"*

> "Thirteen and a half days. That's Option B in the Future State VSM. Let me show you the full transformation model."

**Transition:** "Click 'View Future State →' to see what Team Phoenix's pipeline looks like after these improvements are implemented."

---

## STEP 7 — Future State VSM
**Page:** http://localhost:3001/vsm-future
**Time:** 8 minutes
**Story:** "We've modelled three transformation paths. Option A is the 6-month augmentation play. Option B is the 12–18 month transformation. Option C — the ADLC — is the 2-year north star. Let me walk you through each."

### What You'll See on Screen

The Future State VSM page has three tabs: **Option A**, **Option B**, **Option C (ADLC)**. A fourth tab shows **"Compare All"**.

At the top, a **current state comparison bar** is always visible:
```
Current State: LT 42 days | PT 130h | WT 600h | FE 8.1%
```

Click **"Compare All"** tab first.

---

### Sub-step 7a: Options Overview (Compare All Tab)

**What you'll see:** A four-column comparison table with Current State, Option A, Option B, Option C.

| Metric | Current State | Option A | Option B | Option C (ADLC) |
|--------|--------------|----------|----------|-----------------|
| Lead Time | 42 days | 18 days | 8 days | 3 days |
| Flow Efficiency | 8.1% | 42% | 61% | 78% |
| Process Time | 130h | 68h | 32h | 12h |
| Wait Time | 600h | 92h | 38h | 8h |
| Investment Range | — | $1.2M–$1.8M | $2.5M–$3.5M | $4M–$6M |
| Timeline | — | 6–9 months | 12–18 months | 18–24 months |
| AI Agent Activities | 0/36 | 8/36 | 22/36 | 34/36 |

**Talking track:**

> "Three options, three investment levels, three transformation timelines. Option A is augmentation — we layer AI assistance onto the existing PDLC without changing the fundamental structure. Lead time halves to 18 days. Option B is transformation — we rebuild the testing and delivery process around AI-first principles. Lead time drops to 8 days, flow efficiency triples. Option C — the ADLC — is the north star: an AI-Driven Lifecycle where agents handle 34 of 36 activities autonomously and humans hold the oversight and approval roles."

---

### Sub-step 7b: Option A — AI Augmentation (Conservative)

Click the **"Option A"** tab.

**What you'll see:** The 7 phases are rendered with their new metrics. Phase bars are noticeably shorter than the current state. A legend shows activity types: blue = Human, purple = AI-Assisted, orange = Agent, green = Automated.

**Option A Phase Metrics:**

| Phase | PT (hrs) | WT (hrs) | FE% | Key Change |
|-------|----------|----------|-----|-----------|
| 1. Backlog & Roadmap | 20 | 24 | 45% | AI Backlog Prioritiser + Requirements Analyst |
| 2. Architecture & UX | 30 | 32 | 48% | AI Design Reviewer (standard patterns self-approve) |
| 3. Code Management | 10 | 5 | 67% | ReviewAgent pre-review |
| 4. Continuous Integration | 4 | 4 | 50% | Parallel test execution |
| 5. Continuous Testing | 20 | 14 | 59% | AI UAT Assistant + parallel regression |
| 6. Continuous Delivery | 8 | 8 | 50% | AI Release Manager (risk-tiered approval) |
| 7. Monitoring & Feedback | 5 | 5 | 50% | AI Observability Agent |
| **TOTAL** | **97h** | **92h** | **51%** | |

**Talking track:**

> "Option A keeps the 7 PDLC phases intact — every governance gate still exists, every human approval is preserved. But AI assistance compresses the time within each phase. The Architecture Review Board still meets — but the AI pre-analysis means the agenda is already structured and standard items are pre-approved. CAB still convenes — but the AI risk assessment means the meeting is 30 minutes instead of 3 hours, and fewer changes need to attend. This is the path for organisations where governance constraints are fixed and non-negotiable."

> "Investment: $1.2–1.8M over 6–9 months. Lead time: 18 days. Flow efficiency: 42%. For a banking organisation that's cautious about AI, this is the entry point — incremental, reversible, fully auditable."

---

### Sub-step 7c: Option B — Hybrid Intelligence (Recommended)

Click the **"Option B"** tab.

**What you'll see:** Phase bars are significantly shorter. Several activities now show orange "Agent" badges — these are fully AI-driven steps. A sidebar shows the implementation timeline with 4 quarterly milestones.

**Option B Phase Metrics:**

| Phase | PT (hrs) | WT (hrs) | FE% | Key Change |
|-------|----------|----------|-----|-----------|
| 1. Backlog & Roadmap | 12 | 8 | 60% | AI Requirements Analyst autonomous; human approves scope |
| 2. Architecture & UX | 18 | 14 | 56% | AI Design Reviewer autonomous for standard; ARB for novel |
| 3. Code Management | 8 | 4 | 67% | ReviewAgent + PR size limits enforced (< 400 lines) |
| 4. Continuous Integration | 2 | 2 | 50% | AI Pipeline Orchestrator + incremental builds |
| 5. Continuous Testing | 8 | 4 | 67% | AI-driven DAST/SAST replaces pen-test for 70% of changes |
| 6. Continuous Delivery | 6 | 4 | 60% | Continuous delivery with automated compliance evidence |
| 7. Monitoring & Feedback | 4 | 2 | 67% | AIOps auto-remediation for known incident types |
| **TOTAL** | **58h** | **38h** | **60%** | |

**Talking track — this is the recommendation pitch:**

> "Option B is our recommended path for Team Phoenix. Here's what changes: the testing phase is rebuilt around AI-first principles. Instead of routing every PCI-DSS scope change to an external pen-test vendor, the AI performs continuous DAST scanning in the pipeline, risk-scores each change, and only escalates genuinely high-risk changes to the external vendor. For 70% of changes, the pen-test gate disappears entirely."

> "Continuous delivery replaces the bi-weekly CAB batching. Low-risk changes — the AI has classified them — deploy through an automated pipeline that generates compliance evidence automatically. High-risk changes still go through a governance review, but the review is evidence-backed, structured, and takes 30 minutes instead of 2 days."

> "The result: 8-day lead time. 61% flow efficiency. DORA band moves from WALK to RUN. Investment: $2.5–3.5M over 12–18 months. And crucially — compliance evidence quality goes up, not down, because it's generated systematically rather than assembled manually before each CAB meeting."

---

### Sub-step 7d: Option C — ADLC (AI-Driven Lifecycle)

Click the **"Option C"** tab.

**What you'll see:** The 7 traditional PDLC phases are replaced by 7 ADLC capability cards with different names. The human/AI activity breakdown shows 34/36 activities as agent-driven (orange) and only 2 as human oversight (green). The phase bar chart is almost entirely orange.

**ADLC Phase Structure:**

| ADLC Capability | Equivalent PDLC Phase | PT (hrs) | WT (hrs) | FE% |
|----------------|----------------------|----------|----------|-----|
| 1. Intent & Outcome Definition | Backlog & Roadmap | 3 | 1 | 75% |
| 2. Autonomous Architecture & Design | Architecture & UX | 2 | 1 | 67% |
| 3. Agentic Code Generation | Code Management | 2 | 1 | 67% |
| 4. Autonomous Integration Pipeline | Continuous Integration | 1 | 1 | 50% |
| 5. Continuous Quality Intelligence | Continuous Testing | 2 | 2 | 50% |
| 6. Zero-Touch Delivery | Continuous Delivery | 1 | 1 | 50% |
| 7. AIOps & Continuous Learning | Monitoring & Feedback | 1 | 1 | 50% |
| **TOTAL** | | **12h** | **8h** | **60%** |

**Talking track:**

> "Option C is the north star — the AI-Driven Lifecycle. The 7 PDLC phases haven't been automated, they've been restructured. In this model, two human roles exist: the Product Definer, who sets vision, OKRs, and acceptance criteria, and the Product Builder, who supervises the agent orchestration and holds the production approval gate."

> "The ADLC phases are: Intent Definition — a human describes what needs to be built and why. Autonomous Architecture — an architecture agent designs the solution, generates API contracts, and validates against security and compliance standards. Agentic Code Generation — code generation agents write, test, and refactor in parallel. Autonomous Integration — CI/CD agents handle build, test, scan, and environment promotion. Continuous Quality Intelligence — QA agents run comprehensive coverage and generate a quality intelligence report. Zero-Touch Delivery — deployment agents manage the release, with the Product Builder holding a single production gate. AIOps — agents detect, diagnose, and remediate — escalating only genuinely novel incidents to the human."

> "Lead time: 3 days. Flow efficiency: 78%. The entire pipeline compresses from 42 days of human-gated batch processing to 3 days of supervised autonomous delivery. This isn't science fiction — the technology exists today. The constraint is organisational readiness, governance frameworks, and change management. Timeline: 18–24 months. Investment: $4–6M."

**Wow moment — point to the comparison bar:**

> "Three days versus 42 days. 78% flow efficiency versus 8.1%. The same team, the same product, the same payments domain — but with a fundamentally different operating model. That's the decision the business case is quantifying."

**Transition:** "Let me show you the financial model that sits behind these options."

---

## STEP 8 — Business Case
**Page:** http://localhost:3001/business-case
**Time:** 7 minutes
**Story:** "The Business Case page translates the transformation options into financial terms — ROI, payback period, NPV, and risk-adjusted projections."

### What You'll See on Screen

The Business Case page has three sections:
1. **Cost of Current State** — quantifying the waste Team Phoenix is experiencing today
2. **Investment & Returns by Option** — three-column comparison (Option A / B / C)
3. **Recommended Scenario** — detailed financial model for Option B with NPV waterfall chart

A **team configuration panel** on the left shows pre-filled parameters:
- Team Size: 12 engineers
- Avg Fully-Loaded Cost: $180,000/person/year
- Annual Engineering Spend: $2.16M
- Current Flow Efficiency: 8.1%
- Target Flow Efficiency (Option B): 61%

---

### Sub-step 8a: Cost of Current State

**Talking track:**

> "Before we talk about investment, let's quantify what the current state is costing. Team Phoenix has 12 engineers at an average fully-loaded cost of $180,000 per person per year — that's $2.16 million in annual engineering spend. Their flow efficiency is 8.1%. That means 91.9% of their time — $1.98 million — is spent waiting, in approval queues, in re-work loops, not delivering customer value."

> "Now, not all of that is recoverable — some waiting is coordination overhead that will always exist. But with Option B, we're projecting flow efficiency of 61%. The recoverable capacity improvement — from 8.1% to 61% — represents a shift from $175K of productive capacity per year per engineer to $1.1M. Across 12 engineers, that's $8.4M in annual productive capacity gained."

**What you'll see on screen — Cost of Current State card:**

```
Annual Engineering Spend:        $2,160,000
Current Productive Capacity:     $175,176  (8.1% of spend)
Current Waste Cost:              $1,984,824  (91.9% of spend)

Recoverable Capacity (Option B): $8,416,800  (61% FE applied)
Net Annual Benefit (Option B):   $8,416,800 − current baseline
```

---

### Sub-step 8b: Investment vs Returns — Option B (Recommended)

Click the **"Option B"** column to expand it.

**Talking track:**

> "For Option B — our recommended scenario — the financial model looks like this."

**What you'll see — Option B Financial Model:**

| Financial Metric | Value |
|-----------------|-------|
| Total Investment | $2.5M–$3.5M (use $3.0M midpoint) |
| Annual Benefit (Year 1) | $4.2M (ramp — partial year) |
| Annual Benefit (Year 2+) | $8.4M (full run rate) |
| ROI Multiple | 4.2× (over 3 years) |
| Payback Period | 14 months |
| 3-Year NPV (8% discount) | $18.7M |
| 5-Year NPV (8% discount) | $31.2M |

**Breakdown of the $8.4M annual benefit:**

| Benefit Category | Amount | Basis |
|----------------|--------|-------|
| Engineering capacity recovered (FE improvement) | $5.1M | 52.9 pp FE improvement × $2.16M spend |
| Faster time-to-market (revenue acceleration) | $2.1M | 34-day LT reduction × avg feature revenue $62K/feature × 34 features/year |
| Incident cost reduction (MTTR improvement) | $0.8M | MTTR 55h→12h × avg P1 cost $145K × 5.5 P1s/year |
| Compliance audit cost reduction | $0.4M | Automated evidence generation replacing manual audit prep |
| **Total Annual Benefit** | **$8.4M** | |

**Talking track:**

> "The biggest component is engineering capacity — the direct productivity gain from improved flow efficiency. But the second-biggest is time-to-market acceleration. Payments is a competitive market — every day a feature is delayed is a day competitors can capture market share. At $62,000 average revenue per payments feature and 34 features per year, compressing lead time from 42 to 8 days adds $2.1 million in annual revenue acceleration."

> "And the payback is 14 months. That's within a single budget cycle. By the time the Q2 2026 budget review happens, Team Phoenix will have demonstrated measurable lead time reduction and the financial return will be visible."

---

### Sub-step 8c: Risk-Adjusted Scenarios

**Talking track:**

> "We always present three scenarios — conservative, expected, and optimistic — so the CFO can stress-test the model."

**What you'll see — Scenario Bands:**

| Scenario | ROI | Annual Benefit | Payback |
|----------|-----|---------------|---------|
| Conservative (adoption 60%, 70% of projected FE) | 2.1× | $4.8M | 22 months |
| Expected (adoption 80%, 90% of projected FE) | 4.2× | $8.4M | 14 months |
| Optimistic (adoption 95%, full FE realised) | 5.8× | $11.2M | 10 months |

**Talking track:**

> "Even in the conservative scenario — where adoption is slower than expected and the flow efficiency improvement is 70% of what we've modelled — the ROI is 2.1× and payback is under 2 years. For a $3M investment in a regulated bank, that's a compelling risk-adjusted return."

**Wow moment — point to the NPV waterfall chart:**

> "The 5-year NPV of $31.2 million — on a $3 million investment. This isn't a cost centre initiative. This is a strategic investment in competitive capacity. The question isn't whether to do this — the question is which option and how fast."

**Transition:** "The final step is giving the AI the organisational context it needs to generate a bespoke implementation playbook — not a generic roadmap, but one that reflects Team Phoenix's specific tech stack, compliance requirements, team composition, and stakeholder concerns."

---

## STEP 9 — Playbook Context
**Page:** http://localhost:3001/playbook
**Time:** 5 minutes
**Story:** "The Playbook agent generates a 90-day implementation roadmap tailored to Team Phoenix. The more context we give it, the more specific and actionable the output."

### What You'll See on Screen

The Playbook Context page has two panels:
- **Left panel:** A document upload area with 7 labelled document slots (drag-and-drop or paste text)
- **Right panel:** A URL ingestion panel with a text field for pasting links and a "Fetch & Embed" button

Below both panels, a **"Generate Playbook"** button (large, blue) is disabled until at least one document or URL has been added.

A status bar shows: *"0 documents | 0 URLs | Context score: 0% — Add at least 3 sources for meaningful playbook generation."*

---

### Sub-step 9a: Upload the 7 Documents

For each document below, click the corresponding slot on the left panel, paste the content, and click "Save".

---

**Document 1: `usbank-devops-assessment-2025.txt`**

Click the **"DevOps Assessment"** document slot and paste:

```
US BANK — DIGITAL BANKING DEVOPS MATURITY ASSESSMENT
Team Phoenix | Payments & Transfers Division
Assessment Date: January 2026
Assessor: External Consulting Review + Engineering Manager (David Park)

EXECUTIVE SUMMARY
Team Phoenix is assessed as a WALK-stage DevOps performer with targeted areas of strength
in source control and security, and significant improvement opportunities in deployment
automation, testing maturity, and release governance.

DIMENSION SCORES (1–5 scale)

1. SOURCE CONTROL & COLLABORATION: 3.8/5
   - Strengths: GitFlow enforced, branch protection on main, GPG commit signing
   - Gaps: Avg PR size 847 lines vs 400-line target; long-lived feature branches
   - Evidence: GitHub repository analytics, PR merge history Q4 2025

2. CI/CD PIPELINE: 2.4/5
   - Strengths: All PRs trigger CI; Kubernetes deployment automated
   - Gaps: 24-min build time (target <10 min); 23% SAST first-fail rate; SonarQube gate
     bypassed (62% coverage vs 80% gate); no incremental build configured
   - Evidence: GitHub Actions run logs, SonarQube project dashboard

3. TESTING MATURITY: 2.1/5
   - Strengths: JUnit 5 framework in use; some Testcontainers integration tests
   - Gaps: 62% coverage; Selenium regression sequential (no parallelism); manual SIT
     still required for PCI-DSS evidence; external pen-test for all scope changes
   - Evidence: SonarQube coverage reports, QA test execution logs

4. DEPLOYMENT & RELEASE: 1.8/5
   - Strengths: Kubernetes deployment automated via Helm; pre-prod smoke test exists
   - Gaps: Bi-weekly CAB mandatory for all changes; Wednesday-only release window;
     no risk-tiered deployment model; manual rollback for DB migrations
   - Evidence: ServiceNow CAB records, release calendar 2025

5. MONITORING & OBSERVABILITY: 3.2/5
   - Strengths: Datadog APM + infrastructure monitoring; PagerDuty on-call; SLOs defined
   - Gaps: 340 false positive alerts/month (alert fatigue); no AIOps; DBA team
     availability gap creating MTTR risk; manual root cause analysis
   - Evidence: Datadog dashboard, PagerDuty incident report Q4 2025

6. SECURITY & COMPLIANCE: 3.5/5
   - Strengths: Azure Key Vault for secrets; SAST/DAST in pipeline; Dependabot active
   - Gaps: Manual compliance evidence for CAB; external pen-test not risk-tiered;
     45% IaC coverage (55% manual infra)
   - Evidence: CISO review Q3 2025, Trivy scan reports

OVERALL MATURITY: 2.8/5 (WALK stage)
RECOMMENDED NEXT BAND: RUN (target by Q4 2026)
KEY BLOCKERS: Release governance, test automation coverage, build performance
```

---

**Document 2: `usbank-team-phoenix-charter.txt`**

```
US BANK — TEAM PHOENIX TEAM CHARTER
Payments & Transfers | Digital Banking Division
Effective: January 2026 | Version 2.1

TEAM IDENTITY
Name: Team Phoenix
Mission: Deliver world-class payment and transfer capabilities that enable US Bank
customers to move money with confidence, speed, and security.
Product: Digital Payments Platform — covering peer-to-peer, bill pay, international
transfers, real-time payments (NPP/OSKO), and open banking (CDR compliance)

TEAM COMPOSITION (12 dedicated + 3 shared services)
Product Owner: Jennifer Zhao (5 years PO experience; previously at ANZ Bank)
Solution Architect: Marcus Thompson (12 years; Azure certified; PCI-DSS specialist)
Business Analyst: Rachel Kim (4 years; payments domain expert)
Scrum Master / Agile Coach: Tom Bradley (3 years; SAFe certified)
Backend Dev (Senior): James Liu (8 years; Java/Spring Boot; GitHub Copilot active)
Backend Dev (Mid): Aisha Obi (3 years; Java/Spring Boot; GitHub Copilot not active)
Backend Dev (Mid): Carlos Mendez (4 years; Java/Spring Boot + Python; Copilot active)
Frontend Dev (Senior): Sophie Wang (6 years; React 18; GitHub Copilot active)
Frontend Dev (Mid): Priya Sharma (2 years; React; Copilot not active)
QA Lead: Kevin O'Brien (7 years; Selenium + JUnit; manual testing specialist)
QA Engineer: Laura Chen (3 years; test automation; learning Playwright)
DevOps Engineer: Raj Patel (5 years; Kubernetes + GitHub Actions; Copilot active)

SHARED SERVICES (not dedicated)
DBA Team: Maria Gonzalez (Lead DBA) — shared across 6 teams; business hours only
CISO / Security: James Okonkwo — PCI-DSS compliance owner; 40h SLA for reviews
Architecture Review Board: Robert Stern (Principal Architect) — fortnightly rotation

WAYS OF WORKING
Methodology: Scrum
Sprint Length: 2 weeks
Ceremonies: Daily standup (15 min, 9:15am CT), bi-weekly sprint review (Friday 3pm),
            bi-weekly retrospective (Friday 4pm), quarterly OKR check-in,
            monthly architecture forum (first Tuesday), bi-weekly CAB attendance
Deployment Window: Wednesdays only (production deployment); 8am–2pm CT
Location: Minneapolis HQ — in-person Monday/Tuesday, remote Wednesday–Friday

TEAM GOALS 2026
- Reduce feature lead time from 42 days to <20 days by Q2 2026
- Increase deployment frequency from bi-weekly to weekly by Q3 2026
- Achieve 80%+ automated test coverage by Q4 2026
- Deliver 3 major platform features: CDR Open Banking, Real-time FX, Payment Wallet

KNOWN CONSTRAINTS
- All production changes require CAB approval (IT Risk Management policy)
- PCI-DSS scope changes require CISO review and external pen-test (Tier 1 requirement)
- AI/LLM tools: only enterprise-approved providers (Microsoft Azure OpenAI, Google Vertex)
- No customer PII or cardholder data may be transmitted to any external AI API
- Data residency: all data must remain within Australia (sovereignty requirement)

TEAM RETROSPECTIVE THEMES (recurring Q4 2025)
- "We spend more time in meetings and approval queues than writing code"
- "Test data setup takes longer than the actual testing"
- "PR reviews block us — only James and Marcus can approve payments code"
- "The CAB process doesn't distinguish between a minor config change and a major release"
- "We've had Copilot for 6 months and nobody showed us how to use it properly"
```

---

**Document 3: `team-phoenix-retrospective-q4-2025.txt`**

```
TEAM PHOENIX — Q4 2025 SPRINT RETROSPECTIVE SUMMARY
Sprints 22–27 | October–December 2025
Facilitated by: Tom Bradley (Scrum Master)

WHAT WENT WELL
- Zero production incidents in October (personal best for the team)
- Real-time payment processing engine (USB-2401) delivered on time — Marcus's
  architecture design was excellent and ARB pre-approved it quickly
- James and Sophie's pairing on the Mobile Wallet frontend significantly reduced
  the number of PR review cycles
- Raj's Kubernetes migration work has made deployments more reliable
- Team morale high — NPS score 8.2/10 in team health check

WHAT NEEDS IMPROVEMENT

1. APPROVAL GATES ARE KILLING OUR FLOW
   - Average: 3 working days lost per sprint waiting for ARB slot
   - CAB submission prep (writing the change request) takes 2–4 hours that adds
     no customer value
   - "We deploy on Wednesdays or not at all" — several high-urgency bug fixes
     delayed by 5+ days waiting for the Wednesday window
   - Action agreed: Jennifer to raise with Engineering Manager for escalation to CTO

2. TEST DATA IS A MANUAL NIGHTMARE
   - QA team spends 30–40% of testing effort setting up test data (synthetic card
     numbers, account numbers, transaction histories)
   - Test data environment is shared across 3 teams — conflicts and data corruption
     events 4× this quarter
   - Action: Raj to investigate Testcontainers for isolated test databases in Q1 2026

3. GITHUB COPILOT IS UNDERUSED
   - 6 of 8 engineers who have Copilot active said it "saves time every day"
   - Aisha and Priya don't have Copilot activated — "nobody set it up for us"
   - Kevin (QA Lead) asked "can Copilot write test cases?" — no one knew
   - Action: James to run a 2-hour Copilot enablement session in Sprint 28

4. PR REVIEWS ARE A BOTTLENECK
   - Median PR wait time: 18 hours
   - "James and Marcus are the only ones who can review payments-critical code"
   - PRs are too large — average 847 lines (discussed 4× in retrospectives, no change)
   - Action: Team agreed to enforce 400-line PR limit from Sprint 28

5. REQUIREMENTS ARRIVE INCOMPLETE
   - 6 stories in Q4 required mid-sprint scope clarification
   - Business stakeholders hard to reach during sprint for questions
   - "We write the acceptance criteria ourselves and hope BA agrees"
   - Action: Rachel and Jennifer to introduce story readiness checklist before sprint

METRICS Q4 2025
Velocity: 42 points/sprint avg (range: 38–47)
Sprint Goal Achievement: 71% (5 of 7 sprints achieved goal)
Bugs in Production: 3 (all minor, zero P1)
Deployment Frequency: Bi-weekly (every sprint review Wednesday)
Stories Completed On Time: 68%

TEAM HAPPINESS SCORE: 7.8/10 (up from 7.1 in Q3)
TOP REQUESTED IMPROVEMENT: "Fix the CAB process" (mentioned by 9 of 12 team members)
```

---

**Document 4: `usbank-compliance-framework.txt`**

```
US BANK DIGITAL BANKING — COMPLIANCE FRAMEWORK SUMMARY
Payments & Transfers | Technology Compliance | January 2026

APPLICABLE REGULATORY FRAMEWORKS

1. PCI-DSS LEVEL 1 (Payment Card Industry Data Security Standard)
   Scope: All systems that store, process, or transmit cardholder data
   Key Requirements for Software Delivery:
   - Requirement 6.3: All code changes must go through a formal change control process
   - Requirement 6.4: Development/test environments must be separate from production
   - Requirement 6.5: All code must be reviewed by someone other than the author
   - Requirement 11.3: Penetration testing required at least annually AND after
     significant infrastructure or application changes
   - Requirement 12.3: Targeted risk analysis for any technology in scope

   Impact on Team Phoenix:
   - External pen-test mandatory for features touching payment processing code
   - CAB process is our Requirement 6.3 change control implementation
   - Separate dev/SIT/UAT/pre-prod/prod environments required (in place)
   - All code reviewed by second engineer (PR approval policy enforces this)

   AI Adoption Considerations:
   - AI-generated code is subject to the same PCI-DSS controls as human-written code
   - AI review tools (e.g., GitHub Copilot suggestions) must be audited in PR history
   - Automated DAST/SAST can SUPPLEMENT but not REPLACE pen-test for PCI-DSS scope
     (however: risk-tiered approach may reduce scope of external pen-test)
   - Compliance evidence generated by AI tools is acceptable if it meets the same
     documentary standards as manually produced evidence

2. SOX (Sarbanes-Oxley Act — IT General Controls)
   Scope: Financial reporting systems; change management controls
   Key Requirements:
   - IT change management must demonstrate: authorization, testing, approval before deploy
   - Segregation of duties: developer who writes code cannot approve own code to production
   - Audit trail: all production changes must be traceable with approval records

   Impact on Team Phoenix:
   - CAB process also satisfies SOX IT-GC change management requirement
   - Two-approver PR policy satisfies segregation of duties for code changes
   - Deployment audit trail in ServiceNow + GitHub required

3. FFIEC CYBERSECURITY GUIDELINES
   Scope: Financial institutions — technology risk management
   Key Requirements:
   - Risk-based approach to change management (supports risk-tiered deployment model)
   - Vendor risk management for third-party tools and AI providers
   - Incident response: MTTR targets for production incidents
   - Business continuity: RTO/RPO requirements for critical payment systems

   Opportunity: FFIEC explicitly supports risk-based approach — provides regulatory
   basis for implementing risk-tiered deployment (replacing uniform CAB with
   evidence-based risk classification).

CHANGE MANAGEMENT POLICY (internal)
   - All production changes: CAB approval required (bi-weekly meeting)
   - Emergency changes: ECAB (Emergency CAB) within 4 hours — 2 approvers required
   - Standard changes (pre-approved patterns): listed in standard change register
     Current standard changes: Kubernetes config updates, SSL certificate renewal,
     scheduled batch job parameter changes (17 approved patterns)
   - Normal changes (all other): full CAB with 48-hour advance notice

AI DEPLOYMENT PATHWAY (approved January 2026)
   - AI tools within Microsoft Azure ecosystem: pre-approved for use
   - GitHub Copilot Enterprise: approved — code suggestions only, not autonomous commit
   - External AI APIs (OpenAI direct, Anthropic): NOT approved for production use
   - AI-generated compliance evidence: acceptable with human review and sign-off
   - AI-driven deployment decisions: requires governance framework sign-off (in progress)
```

---

**Document 5: `usbank-architecture-standards.txt`**

```
US BANK DIGITAL BANKING — ARCHITECTURE & API STANDARDS
Version 2.4 | Payments & Transfers | January 2026

1. API DESIGN STANDARDS
   Protocol: RESTful HTTP/1.1 + HTTP/2 for streaming; GraphQL for internal BFF
   Authentication: OAuth 2.0 with JWT (RS256 signing); PKCE for public clients
   Versioning: URI versioning (/api/v1/, /api/v2/) — breaking changes require new version
   Documentation: OpenAPI 3.1 spec required for all APIs; Swagger UI auto-generated
   Rate limiting: All public APIs rate-limited (default: 100 req/min per client)
   Idempotency: All payment mutation endpoints must support idempotency keys
   Error format: RFC 7807 (Problem Details for HTTP APIs) — machine-readable errors

2. SECURITY ARCHITECTURE
   Secrets: Azure Key Vault (mandatory — no secrets in code, env vars, or config files)
   Network: All service-to-service via Azure Private Link; no public internet for internal
   Encryption: TLS 1.3 minimum for all traffic; AES-256 for data at rest
   PCI-DSS zone: Payment processing services in dedicated AKS namespace with network policy
   SAST: SonarQube Enterprise (payment-specific ruleset active)
   DAST: OWASP ZAP (pipeline); external pen-test for PCI-DSS scope changes
   Dependency scanning: GitHub Dependabot (weekly) + Snyk (real-time)
   Container security: Trivy scanning on all images; base images from approved registry only

3. CLOUD ARCHITECTURE (Azure)
   Region: AustraliaEast (primary); AustraliaSoutheast (disaster recovery)
   Kubernetes: AKS 1.28; GitOps via Flux v2; namespaces per environment
   Compute: Azure Container Instances (batch); AKS (APIs and services)
   Database: Azure SQL (OLTP); Azure Cache for Redis (session + rate limiting)
   Messaging: Azure Service Bus (async events); Azure Event Hub (high-throughput streaming)
   Storage: Azure Blob Storage (documents, audit logs); Azure Data Lake (analytics)
   Monitoring: Datadog (APM, infrastructure, RUM); Splunk (SIEM, compliance logs)
   CDN: Azure Front Door (global routing + DDoS protection)

4. APPROVED AI/ML TOOLS AND CONSTRAINTS
   Azure OpenAI Service: Approved — GPT-4o for internal tooling and automation
   GitHub Copilot Enterprise: Approved — code assistance only
   Azure ML: Approved — model training and serving for internal models
   Data constraints:
     - No cardholder data (PAN, CVV, expiry) to any AI service
     - No customer PII to external AI APIs
     - Synthetic/anonymised data only for AI training and testing

5. STANDARD ARCHITECTURE PATTERNS (ARB pre-approved)
   - Microservices with Azure Service Bus event-driven integration
   - API Gateway pattern using Azure API Management
   - CQRS for read/write separation on high-traffic payment services
   - Saga pattern for distributed payment transactions
   - Circuit breaker pattern (Polly) for external service resilience
   - Event sourcing for audit-critical payment state changes
   - Feature flags via Azure App Configuration (LaunchDarkly alternative)

6. KNOWN TECHNICAL DEBT (priority list)
   HIGH: Oracle legacy DB (payments_core) — 3.2M lines; partial Azure SQL migration
   HIGH: Selenium E2E (legacy) — migration to Playwright approved, Q2 2026
   HIGH: 62% test coverage — SonarQube gate bypassed; plan to close gap by Q3 2026
   MEDIUM: Monorepo full rebuild on any change — incremental build not configured
   MEDIUM: 55% of SIT environment manually provisioned — IaC target: 90% by Q4 2026
   LOW: Mixed API versioning approaches in legacy payment services
```

---

**Document 6: `payments-dora-benchmarks.txt`**

```
DORA INDUSTRY BENCHMARKS — FINANCIAL SERVICES & BANKING
Source: DORA 2024 State of DevOps Report + Fintech/Banking sector supplements
Compiled: January 2026

BANKING SECTOR DORA DISTRIBUTION (2024 data, n=2,847 banking organisations)

DEPLOYMENT FREQUENCY
Elite (top 5%):     Multiple deploys per day
High (next 20%):    Once per day to once per week
Medium (next 50%):  Once per week to once per month
Low (bottom 25%):   Less than once per month or on demand
Banking sector median: Once per week (Medium band)
Team Phoenix current:  Bi-weekly (lower Medium band)
Top quartile banking:  3–5 deployments per week

LEAD TIME FOR CHANGES
Elite (top 5%):     < 1 hour
High (next 20%):    1 hour to 1 week
Medium (next 50%):  1 week to 1 month
Low (bottom 25%):   1–6 months
Banking sector median: 18 days
Team Phoenix current:  42 days (below banking median)
Top quartile banking:  3–8 days

CHANGE FAILURE RATE
Elite (top 5%):     0–2%
High (next 20%):    2–5%
Medium (next 50%):  5–15%
Low (bottom 25%):   16–30%+
Banking sector median: 8%
Team Phoenix current:  12% (above banking median)
Top quartile banking:  < 3%

MEAN TIME TO RESTORE
Elite (top 5%):     < 1 hour
High (next 20%):    < 1 day
Medium (next 50%):  1–7 days
Low (bottom 25%):   1 week to 1 month
Banking sector median: 18 hours
Team Phoenix current:  55.2 hours (above banking median)
Top quartile banking:  < 4 hours

FLOW EFFICIENCY BENCHMARKS (banking sector)
Bottom quartile:    < 5%
Median:             10–15%
Top quartile:       25–35%
Elite (top 5%):     40–55%
Team Phoenix current: 8.1% (below banking median)

AI ADOPTION IMPACT DATA (banking teams using AI-assisted development, 2024)
Deployment frequency improvement: +2.3× (median) after AI tool adoption
Lead time reduction: -42% (median) within 12 months of comprehensive AI adoption
Change failure rate: -1.8 pp improvement (AI code review reduces defect injection)
MTTR improvement: -55% (AI-assisted incident diagnosis and runbook automation)
Test coverage improvement: +18 pp (AI test generation, teams >80% coverage)

REGULATORY COMPLIANCE FINDINGS
- 73% of banking teams cite compliance/governance as primary barrier to higher deployment frequency
- Teams using risk-tiered change management (vs uniform CAB): 3.1× higher deployment frequency
- Automated compliance evidence generation: adopted by 34% of elite banking teams in 2024
- PCI-DSS + AI-driven DAST: 89% of elite banking teams now use AI-assisted security scanning

PEER BENCHMARKS — COMPARABLE BANKING TEAMS
ANZ Digital Banking (published case study):
  Before: 35-day LT, 9% FE, weekly deploy | After (18 months): 7-day LT, 58% FE, daily deploy
  Key actions: Risk-tiered CAB, parallel test execution, AI PR review, feature flags

Commonwealth Bank Group Technology:
  Published: Moved from bi-weekly to daily deployment on core banking in 14 months
  Key actions: Platform engineering team, internal developer portal, automated security gates

HSBC Technology (2023 case study):
  Before: 28-day LT, 12% FE | After (12 months): 6-day LT, 49% FE
  Key actions: Automated change classification, AI-assisted testing, continuous delivery pipeline
```

---

**Document 7: `usbank-okr-2026.txt`**

```
US BANK DIGITAL BANKING — OKRs 2026
Team Phoenix | Payments & Transfers
Owner: Jennifer Zhao (Product Owner) | Approved: Sarah Williams (VP Digital Banking)

OBJECTIVE 1: ACCELERATE PAYMENT FEATURE DELIVERY
Rationale: Competitive pressure from neobanks (Up Bank, Wise, Revolut) on speed of
feature delivery. Customer research shows 34% of customers consider switching due to
feature lag vs competitors. Priority: Critical.

Key Result 1.1: Reduce mean lead time from 42 days to <20 days by Q2 2026
  Current: 42 days | Target: <20 days | Method: AI-assisted development workflow
  Progress checkpoints: <35 days by end Q1 | <25 days by mid Q2 | <20 days by end Q2

Key Result 1.2: Increase deployment frequency from bi-weekly to weekly by Q3 2026
  Current: Every 2 weeks | Target: Every week (52/year) | Method: Risk-tiered CAB
  Progress checkpoints: 3-week cadence by end Q1 | weekly by Q3

Key Result 1.3: Ship 3 platform-defining features by Q4 2026
  Feature A: CDR Open Banking API (regulatory requirement — mandatory by July 2026)
  Feature B: Real-time FX Rate Feed with live pricing (competitive priority)
  Feature C: Integrated Payment Wallet with biometric auth (strategic priority)

OBJECTIVE 2: ELEVATE ENGINEERING QUALITY & RELIABILITY
Rationale: 12% change failure rate is above peer benchmark (8%). 3 production incidents
in Q4 2025, each causing customer-facing payment delays. Regulatory scrutiny increasing.

Key Result 2.1: Reduce change failure rate from 12% to <5% by Q4 2026
  Current: 12% | Target: <5% | Method: AI code review, automated DB migration testing

Key Result 2.2: Increase automated test coverage from 62% to 80%+ by Q3 2026
  Current: 62% | Target: 80% | Method: AI test generation, dedicated sprint allocation

Key Result 2.3: Reduce MTTR from 55 hours to <8 hours by Q4 2026
  Current: 55h | Target: <8h | Method: AIOps, extended DBA on-call, runbook automation

OBJECTIVE 3: SCALE AI-ASSISTED DEVELOPMENT CAPABILITY
Rationale: GitHub Copilot is licensed for 100 seats; only 34 active. Teams using Copilot
report 20–30% productivity gain. Scaling adoption is lowest-cost, fastest-return action.

Key Result 3.1: Achieve 90%+ GitHub Copilot active usage by Q1 2026
  Current: 34/100 active | Target: 90/100 | Method: Enablement session, pair programming

Key Result 3.2: Implement AI-assisted code review (ReviewAgent) by Q2 2026
  Current: Manual PR review only | Target: AI pre-review on all PRs

Key Result 3.3: Deploy AI Requirements Analyst pilot by Q2 2026
  Current: Manual requirements process | Target: AI-assisted requirements validation

OBJECTIVE 4: DEMONSTRATE MEASURABLE ROI BEFORE Q2 BUDGET REVIEW
Rationale: Capital allocation for Option B transformation requires evidence from Option A
quick wins. Finance requires demonstrated ROI before committing $2.5M+ investment.

Key Result 4.1: Quick wins (3 AI improvements) showing measurable LT reduction by Q2
Key Result 4.2: Board-ready business case with 3-year NPV by March 2026
Key Result 4.3: Pilot team (Team Phoenix) results published as internal case study by Q2
```

---

### Sub-step 9b: Add the 9 URLs

**Talking track:**

> "The URL ingestion panel lets us add public research, industry frameworks, and vendor documentation. The AI fetches each URL, chunks the content, and embeds it into the playbook knowledge base alongside the documents we've uploaded."

In the right panel, paste each URL one at a time into the URL field and click **"Fetch & Embed"**. Wait for the green confirmation tick before adding the next.

| # | URL | Label (auto-detected or type) |
|---|-----|-------------------------------|
| 1 | `https://dora.dev/research/2024/dora-report/` | DORA 2024 State of DevOps Report |
| 2 | `https://cloud.google.com/devops/state-of-devops` | Google Cloud DevOps Benchmarks |
| 3 | `https://www.finops.org/framework/` | FinOps Framework |
| 4 | `https://www.ffiec.gov/cyberresourcesguidance.htm` | FFIEC Cybersecurity Guidelines |
| 5 | `https://www.pcistandards.org/assessors-and-solutions/` | PCI DSS Compliance |
| 6 | `https://martinfowler.com/articles/continuousIntegration.html` | CI/CD Best Practices |
| 7 | `https://www.lean.org/explore-lean/what-is-lean/` | Lean Methodology |
| 8 | `https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-top-trends-in-tech` | McKinsey Tech Trends |
| 9 | `https://www.gartner.com/en/documents/platform-engineering` | Gartner Platform Engineering |

**What you'll see after each fetch:** A progress spinner (1–3 seconds), then a green checkmark with: *"Fetched — 847 words embedded."*

**Status bar after all sources added:**
*"7 documents | 9 URLs | Context score: 94% — Excellent. Playbook will be highly personalised."*

---

### Sub-step 9c: Generate the Playbook

**Talking track:**

> "We now have 16 knowledge sources — 7 internal US Bank documents covering team composition, tech stack, compliance requirements, and strategic OKRs, plus 9 industry reference sources including the DORA 2024 report, FFIEC guidelines, and McKinsey research. The playbook agent uses all of this to generate a recommendation that is specific to Team Phoenix — not a generic best-practices document."

Click **"Generate Playbook"** (large blue button).

**What you'll see:** A loading animation with the text: *"Playbook agent running... Analysing 16 sources... Generating 90-day roadmap... Personalising to Team Phoenix..."* (approximately 5–8 seconds).

**Expected AI Output — Playbook Summary:**

The page renders a structured playbook with five sections:

**Section 1: Executive Summary (1 paragraph)**
The AI generates a paragraph referencing the specific team name, the specific metrics, the specific compliance constraints, and the specific OKRs. It will mention PCI-DSS, the CAB process, the GitHub Copilot underutilisation, and the Q2 2026 budget deadline.

**Section 2: 90-Day Sprint Roadmap**

| Sprint | Focus | Key Deliverables |
|--------|-------|-----------------|
| Sprint 28–29 (Weeks 1–4) | Foundation | GitHub Copilot enablement (all 12 team members); PR size policy enforcement (<400 lines); ReviewAgent pilot |
| Sprint 30–31 (Weeks 5–8) | Quick Wins | AI Requirements Analyst pilot; Parallel test execution in Selenium; Testcontainers for test data isolation |
| Sprint 32–33 (Weeks 9–12) | Governance Reform | Risk-tiered CAB proposal to CTO; AI UAT Assistant pilot; Standard change register expansion |

**Section 3: Stakeholder Communication Plan**
The AI generates specific talking points for each named stakeholder from the charter: CTO Michael Chen (ROI and risk focus), Head of Digital Banking Sarah Williams (competitive urgency), CISO James Okonkwo (compliance enhancement, not risk), Engineering Manager David Park (team capability building).

**Section 4: Risk Mitigation**
The AI identifies the top 3 risks specific to Team Phoenix and generates mitigation plans — referencing the CISO's AI compliance concern, the engineering VP's GitHub Copilot hallucination concern, and the architect's technical debt concern from the charter document.

**Section 5: Success Metrics & Checkpoints**
The AI generates a measurement framework aligned to the OKRs — specific targets per quarter, measurement methods (GitHub Actions, Datadog, Jira), and the milestone for the Q2 2026 budget review.

**Talking track at the generated playbook:**

> "This is not a generic DevOps transformation template. Look at Section 3 — the AI has named James Okonkwo as the CISO and suggested specific talking points about how AI-driven DAST scanning enhances, rather than bypasses, PCI-DSS compliance evidence — because it read the compliance framework document we uploaded. In Section 4, it has specifically flagged GitHub Copilot hallucinations as a risk and recommended a code review checklist — because that concern appeared in the team charter."

> "This is what happens when you combine process analysis, financial modelling, and contextual AI generation in a single integrated platform. The client leaves this session with a specific 90-day roadmap, a board-ready business case, and a compliance-aware implementation plan — in under an hour."

**Wow moment — point to the stakeholder section:**

> "The fact that the AI found James Okonkwo's name in the team charter, identified him as the CISO, cross-referenced his known concern about AI compliance risk from the stakeholder section, and then generated a specific mitigation message tailored to a CISO's perspective — that is AI working at consulting-grade context depth."

---

## DEMO CLOSE — SUMMARY CLOSE (2 minutes)

Navigate back to http://localhost:3001 (or any summary page available).

**Closing talking track:**

> "Let me bring it back to where we started. Team Phoenix — 42-day lead time, 8.1% flow efficiency. By the end of this session, we've mapped every phase of their pipeline, benchmarked them against 33,000 organisations, identified the 5 highest-impact bottlenecks with root causes, generated 8 prioritised AI recommendations, modelled three transformation futures, built the financial case for the recommended option — and produced a personalised 90-day playbook grounded in their team structure, compliance constraints, and strategic OKRs."

> "In a traditional consulting engagement, this analysis takes 8–12 weeks and costs $400–800K. This platform produces a first-pass version of the same output in under an hour, with the same rigour and specificity. The consultant's role shifts from data gathering and analysis to validation, facilitation, and implementation support — which is where consulting creates the most value."

> "The question for Team Phoenix — and for your team — is: which path? Option A at $1.2–1.8M, reaching 18-day lead time in 6 months. Option B at $2.5–3.5M, reaching 8-day lead time in 12–18 months. Or Option C — the ADLC north star at $4–6M, reaching 3-day lead time in 2 years. The data is in front of you. What does your team need to decide?"

**Stop. Let the question sit.**

---

## APPENDIX A — QUICK REFERENCE CHEAT SHEET

### URLs
| Step | URL |
|------|-----|
| ALM Connect | http://localhost:3001/alm-connect |
| DORA Assessment | http://localhost:3001/dora-assessment |
| Current State VSM | http://localhost:3001/vsm-current |
| VSM Editor | http://localhost:3001/vsm-editor |
| Bottleneck Analysis | http://localhost:3001/bottlenecks |
| Improvements | http://localhost:3001/improvements |
| Future State VSM | http://localhost:3001/vsm-future |
| Business Case | http://localhost:3001/business-case |
| Playbook Context | http://localhost:3001/playbook |
| Dashboard | http://localhost:3001/dashboard |

### Key Numbers to Know by Heart
| Metric | Current | Option A | Option B | Option C |
|--------|---------|----------|----------|----------|
| Lead Time | 42 days | 18 days | 8 days | 3 days |
| Flow Efficiency | 8.1% | 42% | 61% | 78% |
| DORA Band | WALK (2.0) | RUN | RUN+ | FLY |
| Investment | — | $1.2–1.8M | $2.5–3.5M | $4–6M |
| ROI | — | 2.1× | 4.2× | 5.8× |
| Payback | — | 18 months | 14 months | 20 months |
| 5-yr NPV | — | $12.1M | $31.2M | $49.4M |

### Current State VSM — Phase by Phase
| Phase | PT | WT | FE% |
|-------|----|----|-----|
| 1. Backlog & Roadmap | 25h | 72h | 25.8% |
| 2. Architecture & UX | 36h | 176h | 17.0% |
| 3. Code Management | 13h | 18h | 41.9% |
| 4. Continuous Integration | 6h | 8h | 42.9% |
| 5. Continuous Testing | 31h | 240h | 11.4% |
| 6. Continuous Delivery | 12h | 56h | 17.6% |
| 7. Monitoring & Feedback | 7h | 30h | 18.9% |
| **TOTAL** | **130h** | **600h** | **17.8%** |

### DORA Scores
| Dimension | Score | Band |
|-----------|-------|------|
| Deployment Frequency | 2.1/5 | Medium |
| Lead Time for Changes | 1.8/5 | Low-Medium |
| Change Failure Rate | 2.0/5 | Medium |
| MTTR | 1.9/5 | Medium |
| Overall | 2.0/5 | WALK |

### Top 5 Bottlenecks
| # | Name | Wait Time | Severity |
|---|------|-----------|----------|
| 1 | Manual SIT/UAT/Pen-test | 240h | Critical |
| 2 | Architecture Review Gate | 96h | Critical |
| 3 | CAB Release Gate | 56h | High |
| 4 | Feature Refinement Loop | 48h | High |
| 5 | PR Code Review Queue | 18h | Medium |

### Top 3 Quick Wins (implement in Sprint 1–2)
1. **ReviewAgent** — PR review wait: 18h → 5h | Uses existing GitHub Copilot licence
2. **AI UAT Assistant** — UAT wait: 240h → 48h | Uses Azure OpenAI (already licensed)
3. **AI Requirements Analyst** — Backlog wait: 48h → 12h | Uses Confluence API

### Team Phoenix Stakeholders
| Name | Role | Key Concern |
|------|------|------------|
| Michael Chen | CTO | ROI, strategic direction |
| Sarah Williams | VP Digital Banking | Competitive urgency, speed to market |
| James Okonkwo | CISO | AI compliance risk, PCI-DSS |
| David Park | Engineering Manager | Team capability, change fatigue |
| Jennifer Zhao | Product Owner | Feature delivery speed, OKR achievement |

### Common Objections & Responses

**"AI-generated code will create compliance risk."**
> "Every AI-generated suggestion goes through the same two-engineer review and SonarQube gate as human code. In fact, the AI review step catches security anti-patterns before they reach the human reviewer — CFR typically falls when AI review is added, not rises. And automated compliance evidence generation means the audit trail is more complete and systematic than what's produced manually today."

**"We tried GitHub Copilot and it hallucinated in production code."**
> "GitHub Copilot suggestions are code recommendations, not autonomous commits. The PR review process — which the platform strengthens, not weakens — is the control that catches quality issues. Teams that see hallucinations in production typically have weak PR review practices or insufficient test coverage. Both of those are addressed in the improvement roadmap."

**"This is too much change for the team to absorb."**
> "Option A requires three changes in six months: activate Copilot for all team members, implement ReviewAgent pre-review, and pilot the AI Requirements Analyst. Three changes. The team is already using Copilot — 34% adoption — and the retrospective shows they want it extended. This is evolutionary, not revolutionary."

**"We're in the middle of a major delivery cycle — the timing isn't right."**
> "The Quick Wins are designed to run alongside existing delivery, not interrupt it. ReviewAgent can be added to the GitHub Actions workflow in a single sprint without changing any team ceremony or process. The biggest time investment is the Copilot enablement session — James has already offered to run a 2-hour session in Sprint 28. The data shows that teams who implement during active delivery cycles get adoption faster because they can see the value immediately."

**"How accurate is the ROI model?"**
> "The conservative scenario — which assumes 60% adoption and 70% of the projected flow efficiency improvement — still delivers 2.1× ROI with a 22-month payback. We've stress-tested the model with three scenarios because we know these projections are directional, not precise. The ANZ Digital Banking case study achieved comparable results within the expected range. We'd recommend a 3-month Quick Wins pilot with a defined measurement protocol before committing to Option B investment — the pilot cost is under $200K and gives you real data before the board-level decision."

---

## APPENDIX B — TIMING GUIDE

### Full Demo (45–60 minutes)
| Step | Content | Time |
|------|---------|------|
| Opening framing | Scene-setting before screen | 2 min |
| Step 1: ALM Connect | Form + CSV upload + data preview | 8 min |
| Step 2: DORA Assessment | Sources + scoring + results | 7 min |
| Step 3: Current State VSM | Phase walk-through | 6 min |
| Step 4: VSM Editor | Phase 5 drill-down + live edit | 4 min |
| Step 5: Bottleneck Analysis | Top 5 bottlenecks | 5 min |
| Step 6: Improvements | Top 8 recommendations | 5 min |
| Step 7: Future State VSM | Options A / B / C walk-through | 8 min |
| Step 8: Business Case | Financial model + ROI | 7 min |
| Step 9: Playbook Context | Doc upload + URL ingestion + generate | 5 min |
| Demo close | Summary close + question | 2 min |
| **Total** | | **59 min** |

### Executive Highlight (20–25 minutes)
| Step | Content | Time |
|------|---------|------|
| Opening framing | Scene-setting | 2 min |
| Step 3: Current State VSM | Phase summary + key bottlenecks | 5 min |
| Step 5: Bottleneck Analysis | Top 3 bottlenecks only | 3 min |
| Step 7: Future State VSM | Option B focus + Option C vision | 6 min |
| Step 8: Business Case | ROI + payback + NPV only | 5 min |
| Demo close | Summary + question | 2 min |
| **Total** | | **23 min** |

### CFO / Finance Audience (15 minutes)
| Step | Content | Time |
|------|---------|------|
| Opening | "91.9% of your engineering spend is waste" | 2 min |
| Step 3: Current State VSM | Flow efficiency visual only | 2 min |
| Step 8: Business Case | Full financial model deep dive | 8 min |
| Demo close | Three scenarios + question | 3 min |
| **Total** | | **15 min** |

---

## APPENDIX C — TROUBLESHOOTING

### Backend not responding (http://localhost:8001 returns error)
```bash
cd /Users/125066/projects/pdlc-vsm-platform
source backend/venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8001
```
Check: `curl http://localhost:8001/health` should return `{"status":"ok"}`

### Frontend not loading (http://localhost:3001 blank or error)
```bash
cd /Users/125066/projects/pdlc-vsm-platform/frontend
npm run dev
```
If port conflict: `lsof -ti:3001 | xargs kill -9` then retry.

### CSV upload fails to parse
- Ensure file is saved as UTF-8 encoded CSV (not UTF-16 or Excel format)
- Check for special characters in the `title` column — wrap in quotes if needed
- Verify the header row matches exactly (case-sensitive field names)

### DORA scores don't update
- Ensure all 4 core metric dropdowns have a selection before clicking "Calculate"
- If page is frozen, hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### Playbook generation hangs
- Check backend terminal for error output
- Verify OPENAI_API_KEY is set in backend environment (if AI generation is live)
- If no API key: platform should fall back to rule-based playbook generation

### Port already in use
```bash
# Kill whatever is on port 8001
lsof -ti:8001 | xargs kill -9
# Kill whatever is on port 3001
lsof -ti:3001 | xargs kill -9
```

---

*Guide version: 2.0 | Scenario: US Bank — Team Phoenix — Payments & Transfers | Platform: PDLC VSM Platform v1.0 | Created: March 2026*
