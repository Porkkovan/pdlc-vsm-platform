# PDLC VSM Platform — User Guide
**Engineering Effectiveness Programme · Powered by Cognizant**

---

## Table of Contents

1. [What Is This Platform?](#1-what-is-this-platform)
2. [Who Uses It — Roles & Permissions](#2-who-uses-it--roles--permissions)
3. [Navigating the Platform](#3-navigating-the-platform)
4. [Key Concepts You Need to Know](#4-key-concepts-you-need-to-know)
5. [Module Guides](#5-module-guides)
   - 5.1 [Executive Dashboard](#51-executive-dashboard)
   - 5.2 [ALM Connect](#52-alm-connect)
   - 5.3 [Current State VSM](#53-current-state-vsm)
   - 5.4 [VSM Editor](#54-vsm-editor)
   - 5.5 [DORA Assessment](#55-dora-assessment)
   - 5.6 [DevOps Maturity](#56-devops-maturity)
   - 5.7 [Bottlenecks](#57-bottlenecks)
   - 5.8 [Improvements](#58-improvements)
   - 5.9 [Future State](#59-future-state)
   - 5.10 [Business Case](#510-business-case)
   - 5.11 [Playbook Context](#511-playbook-context)
   - 5.12 [Recommendations & Accuracy](#512-recommendations--accuracy)
   - 5.13 [Settings](#513-settings)
   - 5.14 [Reference Pages](#514-reference-pages)
6. [End-to-End Workflows](#6-end-to-end-workflows)
   - 6.1 [Onboarding a New Project](#61-onboarding-a-new-project)
   - 6.2 [Running a Full Analysis Pipeline](#62-running-a-full-analysis-pipeline)
   - 6.3 [Completing a DevOps Maturity Assessment](#63-completing-a-devops-maturity-assessment)
   - 6.4 [Preparing a Board-Ready Business Case](#64-preparing-a-board-ready-business-case)
7. [Glossary](#7-glossary)
8. [FAQs](#8-faqs)

---

## 1. What Is This Platform?

The **PDLC VSM Platform** is the engineering effectiveness command centre for measuring, diagnosing, and transforming a team's product delivery lifecycle (PDLC). It maps the lifecycle into **7 phases × 36 activities**, computes lean Value Stream Map (VSM) and DORA metrics, and uses an 8-agent AI pipeline to identify bottlenecks, propose ROI-quantified improvements, and design three modernisation scenarios with board-ready business cases.

It gives every stakeholder in the transformation a single place to:

- **Connect to ALM tools** (Jira, Azure DevOps, GitHub, Linear, ServiceNow) or upload CSV data
- **Build a current-state VSM** for the team across all 7 PDLC phases
- **Score the team** against the four DORA metrics and the 73-question DevOps maturity model
- **Identify bottlenecks** and waste — backed by AI root-cause analysis and industry benchmarks
- **Generate prioritised improvements** with expected process-time / wait-time reductions and ROI
- **Model three transformation scenarios** — Option A (Augmented Human), Option B (Hybrid), Option C (AI-First / ADLC)
- **Produce a complete business case** for each option — investment range, ROI multiple, payback timeline
- **Contextualise an implementation playbook** from the team's tech stack, methodology, and compliance constraints

Think of it as the **engineering effectiveness diagnostic and transformation planner** for any product delivery team — the place where measurement, analysis, and modernisation come together in one defensible artefact.

---

## 2. Who Uses It — Roles & Permissions

There are four roles on the platform. Your role determines what you can see and do.

### Platform Admin
**Who:** Engineering Effectiveness lead, Platform Owner, Transformation Programme Director

The highest access level. Platform Admins manage projects, LLM/ALM credentials, scheduling, and the seed-data harness.

| Can do | Examples |
|---|---|
| Create, edit, and delete projects | Onboard a new team; rename a portfolio |
| Configure LLM credentials | Switch the platform from OpenAI fallback to Azure OpenAI |
| Configure ALM credentials | Add a new Jira instance or rotate an Azure DevOps PAT |
| Configure pipeline schedule | Set weekly auto-runs for all production-tracked projects |
| Seed demo analyses | Load the US Bank "Team Phoenix" demo result for a presentation |
| View all audit history | See who triggered which run and when |
| Manage scheduled runs | Pause, resume, or change cadence for a project's auto-runs |

---

### Engineering Lead
**Who:** Head of Engineering, Engineering Manager, Delivery Manager, Lead Architect

Engineering Leads have full read/write access within **their own portfolio or product group** and read-only access to other portfolios. They are the key approvers for transformation business cases.

| Can do | Examples |
|---|---|
| Create and edit projects in their portfolio | Add a new team under Payments & Transfers |
| Trigger pipeline runs | Run the full analysis after refreshing the VSM with ALM data |
| Override AI outputs | Adjust a bottleneck's root-cause text after a workshop |
| Approve a transformation scenario | Sign off Option B (Hybrid) for the next quarter |
| Sign off DevOps maturity scores | Approve the assessment result before it goes to the steering committee |
| Configure team-specific overrides | Add a custom ALM filter for the team's Jira board |

---

### Analyst
**Who:** Transformation consultant, DevOps practitioner, value-stream analyst, agile coach

Analysts work across portfolios but cannot approve business cases or change platform configuration. They do the day-to-day data work — building VSMs, running assessments, running the pipeline, and reviewing results.

| Can do | Examples |
|---|---|
| Build and edit VSMs (any project) | Upload CSV ALM data; refine phase-level PT/WT estimates |
| Run individual agents | Re-run the Bottleneck Analyzer after a VSM update |
| Score DevOps maturity manually | Override an AI-scored question after a team interview |
| Generate playbook context | Upload supporting docs and generate a tailored implementation plan |
| Export reports | Excel export of bottlenecks and improvements |

---

### Viewer
**Who:** Executive sponsor, Auditor, Steering committee member

Read-only access across the entire platform. Viewers see all data but cannot trigger runs or make changes.

| Can see | Examples |
|---|---|
| Executive Dashboard | Cross-project KPI summary and trend lines |
| All projects' VSMs and analyses | Latest current-state and future-state for every team |
| All DevOps maturity scores | Cultural / Measurement / Process / Technical scores per team |
| All business cases | Investment, ROI, payback per scenario across the portfolio |
| Audit trail | Who ran what and when |

---

### Quick Permissions Reference

| Action | Platform Admin | Engineering Lead | Analyst | Viewer |
|---|---|---|---|---|
| View all modules | ✅ | ✅ | ✅ | ✅ |
| Create a project | ✅ | ✅ | ❌ | ❌ |
| Edit project | ✅ | ✅ (own portfolio) | ❌ | ❌ |
| Delete project | ✅ | ❌ | ❌ | ❌ |
| Build/edit VSM | ✅ | ✅ | ✅ | ❌ |
| Run full pipeline | ✅ | ✅ | ✅ | ❌ |
| Run individual agent | ✅ | ✅ | ✅ | ❌ |
| Configure LLM keys | ✅ | ❌ | ❌ | ❌ |
| Configure ALM credentials | ✅ | ❌ | ❌ | ❌ |
| Configure schedule | ✅ | ❌ | ❌ | ❌ |
| Approve business case | ✅ | ✅ (own portfolio) | ❌ | ❌ |
| Export reports | ✅ | ✅ | ✅ | ❌ |

---

## 3. Navigating the Platform

### Sidebar Navigation

The left-hand sidebar gives you access to all modules. It is organised into five sections:

```
OVERVIEW
  Executive Dashboard         — KPI summary across all projects

ONBOARDING & DATA
  ALM Connect                 — Configure connections to Jira/ADO/GitHub/Linear/ServiceNow or upload CSV
  Current State VSM           — Read-only canonical 7-phase value stream map
  VSM Editor                  — Drill into phase metrics; edit PT/WT/overrides

MATURITY
  DORA Assessment             — Score against the four DORA key metrics
  DevOps Maturity             — Score the 73-question assessment
  Transformation Readiness    — Composite readiness score across cultural/measurement/process/technical

ANALYSIS RESULTS
  Bottlenecks                 — AI-identified waste, root causes, business impact
  Improvements                — ROI-ranked improvement actions
  Future State                — Three transformation scenarios (Option A / B / C)
  Business Case               — Financial models, ROI, payback per scenario
  Recommendations             — Cross-cutting actions surfaced by the pipeline

AGENTS & QUALITY
  Agents                      — Pipeline run history, status, individual agent triggers
  Accuracy Score              — Agent output quality scoring against PDLC domain rules
  Playbook Context            — Generate team-tailored implementation playbook

CONFIGURATION
  Settings                    — LLM credentials, ALM credentials, scheduled runs

REFERENCE
  Governance                  — How to govern AI agent outputs in production
  Operations Intelligence     — Observability and incident response patterns
  Legacy Modernisation        — Patterns for legacy stack modernisation
  AI Assurance                — Assurance, compliance, and audit patterns
  Roles & Slides              — Stakeholder briefing slide content
  Glossary                    — Definitions of every term used in the platform
```

### Project Selector

At the top of the sidebar you will see a **Project** dropdown. This filters the entire platform to the data of one project (team). Most modules require a project to be selected; the Executive Dashboard is the exception (it aggregates across all projects).

> **Tip:** Engineering Leads will automatically see their first portfolio's project pre-selected. Platform Admins default to the most-recently-edited project.

---

## 4. Key Concepts You Need to Know

### 4.1 The 7-Phase × 36-Activity PDLC Model

Every team's delivery lifecycle is mapped to the same canonical taxonomy so that benchmarks, improvements, and scenarios compare like-for-like. The phases:

| # | Phase | Activities | Typical Waste Types |
|---|---|---|---|
| 1 | Backlog & Roadmap | 5 | Over-processing, rework cycles, approval queues |
| 2 | Architecture & UX Design | 4 | Design-review queues, sequential handoffs |
| 3 | Code Management | 5 | Code-review wait, branch conflicts, merge rework |
| 4 | Continuous Integration | 4 | Build duration, dependency download, pipeline queue |
| 5 | Continuous Testing | 9 | Env setup wait, test data, manual testing, compliance |
| 6 | Continuous Delivery | 5 | CAB approvals, release windows, manual smoke testing |
| 7 | Monitoring & Feedback | 4 | MTTD, incident triage, on-call coverage gaps |

Each activity has industry-benchmark **Process Time (PT)**, **Wait Time (WT)**, and **Flow Efficiency (FE)** drawn from a corpus of value-stream observations across financial services, healthcare, retail, energy, and technology sectors.

---

### 4.2 The Four DORA Metrics

The platform calibrates four industry-standard delivery metrics from the VSM data:

| Metric | Definition | Elite Target |
|---|---|---|
| **Deployment Frequency** | How often the team deploys to production | Multiple times per day |
| **Lead Time for Changes** | Time from code commit to running in production | Less than one hour |
| **Change Failure Rate (CFR)** | % of deployments that cause a production failure | 0 – 15% |
| **Mean Time to Recovery (MTTR)** | Time to recover from a production incident | Less than one hour |

Performance bands map to the published DORA report: **Elite, High, Medium, Low**.

---

### 4.3 Lean VSM Metrics

The platform speaks the language of lean manufacturing applied to software:

| Metric | Symbol | Definition |
|---|---|---|
| **Process Time** | PT | Active, value-adding work time on an activity |
| **Wait Time** | WT | Idle / queue / approval time between value-adding activities |
| **Lead Time** | LT | Total elapsed calendar time from start to finish (PT + WT) |
| **Flow Efficiency** | FE | PT ÷ (PT + WT) × 100% — the fraction of lead time that is actually productive |
| **Cycle Time** | CT | Repeat-of-itself time for a recurring activity (often synonymous with LT) |
| **Throughput** | TP | Items delivered per unit time |
| **Work in Progress** | WIP | Count of items currently being worked on |

Industry-leading teams operate at FE ≥ 40%. World-class delivery hits 65%+. Most organisations measure under 10% on first scan.

---

### 4.4 DevOps Maturity Bands

The platform's 73-question maturity assessment scores each question 1–10 across four dimensions (Cultural, Measurement, Process, Technical) and maps the result into one of five maturity bands:

| Score | Band | Description |
|---|---|---|
| 1–2 | **PRE-CRAWL** | Ad hoc, no consistent practice |
| 3–4 | **CRAWL** | Practice exists but inconsistent |
| 5–6 | **WALK** | Practised consistently within teams |
| 7–8 | **RUN** | Systematised; measured; improving |
| 9–10 | **FLY** | Industry-leading; outcome-driven; predictive |

---

### 4.5 The Three Transformation Scenarios

For every team, the Future State Designer agent models three modernisation scenarios:

| Scenario | Label | What It Means | Typical Time-to-Value |
|---|---|---|---|
| **Option A** | Augmented Human | AI tools augment existing humans (Copilots, observability, test gen) | 3–6 months |
| **Option B** | Hybrid | AI agents handle bounded tasks autonomously; humans review & escalate | 6–12 months |
| **Option C** | AI-First / ADLC | Agent Delivery Lifecycle: agents author, review, deploy with policy guardrails | 12–24 months |

Each scenario produces its own future-state VSM, its own business case, and its own implementation roadmap. The platform does not pre-pick a winner — the Engineering Lead and sponsor compare and choose.

---

### 4.6 Source of VSM Data

A VSM snapshot has one of three sources:

| Source | Meaning |
|---|---|
| **alm** | Auto-extracted from an ALM tool (Jira/ADO/GitHub/Linear/ServiceNow) |
| **manual** | Hand-entered by an analyst |
| **sample** | Synthetic demo data generated by the platform — clearly badged in the UI |

Snapshots are immutable except for the `overrides` field; re-fetching from ALM creates a new snapshot row so trend reporting is preserved.

---

### 4.7 Pipeline Run Status

A pipeline run moves through these statuses:

```
pending     → row created; LangGraph not yet started
   ↓
running     → orchestrator iterating node-by-node
   ↓
complete    → all nodes succeeded; result populated
   ↓
failed      → at least one terminal node raised; partial state preserved + error text recorded
```

The UI shows a live status badge and a per-agent progress checklist while the run is in progress (5-second polling cadence).

---

## 5. Module Guides

---

### 5.1 Executive Dashboard

**Who uses it:** All roles — particularly Platform Admins, Engineering Leads, and Viewers
**Access:** All roles

The Dashboard gives a single-screen view of engineering effectiveness across all projects. It has two tabs.

#### Overview Tab

**Total Projects & Health**
Count of all logged projects with a colour-coded bar breaking down how many are at each maturity band (PRE-CRAWL through FLY) based on their latest DevOps maturity assessment.

**DORA Performance**
A 2×2 quadrant chart showing where each project sits on the four DORA metrics — useful for identifying outliers (e.g. a team that deploys frequently but has high CFR).

**Flow Efficiency Distribution**
Histogram of FE scores across all projects, with the world-class threshold (40%) and elite threshold (65%) marked. Most projects cluster in the 5–15% range on first scan.

**Transformation Pipeline**
Tracks which projects have a pending / in-progress / approved transformation scenario, and the aggregated estimated ROI of approved scenarios.

#### Deep Dive Tab

Provides expanded analytics: per-portfolio breakdown, source-of-truth distribution (alm vs manual vs sample), top-10 bottlenecks by frequency across all projects, and a leaderboard of "most improved this quarter" projects.

---

### 5.2 ALM Connect

**Who uses it:** Platform Admins (initial setup), Engineering Leads, Analysts (per-project)
**Access:** Platform Admin and Engineering Lead full; Analyst restricted to fetch-only

The ALM Connect module is the entry point for getting team data into the platform. There are two paths:

#### Path A — Connect to an ALM tool

Click **"Add Connection"** and select a tool:

- **Jira** — server URL, username (email), API token, project key, board ID, JQL filters
- **Azure DevOps** — organisation URL, PAT, project, area path
- **GitHub** — organisation, PAT, repositories, label filters
- **Linear** — workspace, API key, team
- **ServiceNow** — instance URL, OAuth credentials, table

Click **"Test Connection"** to verify the credentials work. A green badge confirms reachability and a sample of pulled records appears.

Click **"Fetch Data"** to pull a configurable date range (default: last 90 days). The platform translates raw issues / work items into the canonical VSM format and creates a new snapshot under this project.

#### Path B — Upload CSV

If your team's ALM data is not directly accessible, export it to CSV with these columns:

```
ticket_id, type, title, sprint, status, story_points,
cycle_time_days, wait_time_days, process_time_hours, phase,
assignee, created_date, completed_date
```

Click **"Upload CSV"**, drop the file in, map any non-standard column names, and the platform will infer phase mappings (e.g., "Architecture & UX" → Phase 2). A preview of the imported records is shown before confirmation.

> **Tip:** A clean CSV of 25–50 work items spanning the last 2–3 sprints is enough to build a meaningful first VSM. The platform handles larger uploads, but the marginal value drops off after 200 items.

---

### 5.3 Current State VSM

**Who uses it:** All roles
**Access:** All roles (read-only)

The Current State VSM is the **read-only canonical view** of the team's value stream — 7 phases laid out left-to-right, with each activity within a phase shown as a tile.

Each tile shows:
- Activity name
- Current PT (hours)
- Current WT (hours)
- FE % (colour-coded: red < 20%, amber 20–40%, green > 40%)
- Industry benchmark badge (best / median / behind)

Hover over a tile for a tooltip with the canonical benchmarks and the % gap.

#### Aggregate Banner

At the top of the page, three large counters show:
- **Total Lead Time** (days) — sum of all phase LTs
- **Aggregate FE** — weighted average across all phases
- **Bottleneck Phase** — the phase contributing the most wait time

#### Source Badge

In the top-right corner the source badge says **alm**, **manual**, or **sample**, followed by the snapshot's created-at timestamp. Older snapshots can be browsed from the Settings → History panel.

---

### 5.4 VSM Editor

**Who uses it:** Analysts and Engineering Leads adjusting the VSM after a workshop
**Access:** All roles (Viewers read-only)

The Editor exposes a drill-down panel for each phase. Click a phase column header to open it; you'll see:

- All activities in that phase
- For each activity: editable PT (hours), editable WT (hours), source (alm / manual / sample), notes
- "Per-activity benchmark" panel comparing the team's numbers to industry p50 and p75

When you change a value, the platform recomputes FE in real time and re-renders the parent phase's aggregate. Click **"Save Overrides"** to persist the changes — the original snapshot is preserved; only the `overrides` JSON is updated.

> **Best practice:** Run an editing workshop with the team after the first ALM pull. Spending 30 minutes adjusting wait-time estimates with the engineers in the room dramatically improves the platform's downstream analysis quality.

---

### 5.5 DORA Assessment

**Who uses it:** Analysts and Engineering Leads
**Access:** All roles (Viewers read-only)

The DORA Assessment module surfaces the four key metrics for the project alongside their performance band and a derivation trail.

For each of the four metrics, you'll see:
- **Current value** (e.g. "Bi-weekly", "42 days", "12%", "2.3 days")
- **Band** — Elite / High / Medium / Low
- **Derivation** — which phase metrics fed the calibration
- **Gap to next band** — what would need to change to advance

#### Manual Override

If your team has direct production telemetry (e.g. CI/CD pipeline data from Jenkins) that is more authoritative than the platform's calibration, you can manually override any of the four metrics. The override is timestamped and shown alongside the calibrated value for transparency.

---

### 5.6 DevOps Maturity

**Who uses it:** Analysts (score), Engineering Leads (approve)
**Access:** All roles (Viewers read-only)

The DevOps Maturity module captures a **73-question assessment** across four dimensions (Cultural 9Q, Measurement 11Q, Process 9Q, Technical 14Q + extra competencies).

#### Creating an Assessment

Click **"New Assessment"** and set:
- Project (or link to a portfolio / product group at higher level)
- Team name and industry
- Data sources — which connected systems should the AI use as evidence? (Jira, ADO, GitHub, GitLab, Jenkins, CircleCI, Datadog, Splunk, SonarQube, ServiceNow)
- Notes — any context the AI should know

Click **"Run AI Scoring"** to have the platform score every question automatically based on connected data sources and the team context. The run takes 60–90 seconds.

#### Reviewing AI Scores

For each question, you see the AI-suggested score (1–10), an evidence-backed explanation, and the maturity band. Click any question to:

- View the AI's reasoning and the data sources it relied on
- Override the score with your own (a note explaining the override is required)
- Mark the question as **N/A** for this team (e.g., compliance question that doesn't apply to internal tooling)

#### Action Items

When a question is scored below the team's target level, the platform auto-creates an action item in the **Action Items** panel:

- Title (e.g., "Adopt trunk-based development")
- Description and current/target scores
- Suggested actions (the AI proposes 2–4 specific steps)
- Responsible role
- Target date
- Effort estimate (S / M / L)

Engineering Leads assign each action to an owner and track status (Open / In Progress / Done / Deferred).

#### VSM Input Export

When the assessment is complete, click **"Export to VSM"** — the findings will enrich the next VSM analysis run with contextual notes. For example, a low Technical score on "feature flag coverage" will cause the Bottleneck Analyzer to consider release-process bottlenecks more heavily.

---

### 5.7 Bottlenecks

**Who uses it:** All roles
**Access:** All roles (analysts can override AI text post-workshop)

The Bottlenecks module shows the AI-identified waste in the team's value stream. Each bottleneck card shows:

- **Phase + activity** affected
- **Waste type** (e.g. Approval delay, Hand-off queue, Manual rework, Environment wait)
- **Root causes** — 2–4 root causes ranked by likelihood
- **Contributing factors** — environmental factors (e.g., "regulated environment", "no automated risk scoring")
- **Current PT / WT** vs **industry p50** benchmark
- **FE impact** — % FE lost to this bottleneck
- **Business impact** — plain-English consequence (e.g. "Bi-weekly release cadence vs daily target")
- **Linked improvements** — quick-link buttons to the improvement actions that address this bottleneck

Click any card to expand it for the full reasoning trace and supporting evidence drawn from the RAG knowledge base.

#### Filtering and Sorting

Filter by phase, waste type, or business-impact severity. Sort by FE-impact or by linked-improvement count.

---

### 5.8 Improvements

**Who uses it:** All roles
**Access:** All roles

The Improvements module is the AI's recommended action register, ranked by ROI × confidence. Each improvement card shows:

- **Title and category** (e.g. "Continuous Delivery → Automated change risk scoring")
- **Problem** (one sentence)
- **Improvement** (the proposed change)
- **Suggested agent** (which capability would deliver it, e.g. "ChangeRisk Agent")
- **Type** — AI Automation / GenAI Agent / Tooling / Process change
- **Expected PT reduction %** and **Expected WT reduction %**
- **Time to value** (weeks)
- **ROI multiple**
- **Effort** (S / M / L)

#### Adding Custom Improvements

Click **"Add Improvement"** to capture an action that the AI didn't surface — typically items raised in a workshop. Custom improvements are clearly badged and contribute to the rolled-up business case the same way as AI-generated ones.

#### Selecting for Roadmap

Each card has a **"Add to roadmap"** checkbox. Selected improvements become inputs to the Business Case module and are bundled into the chosen future-state scenario.

---

### 5.9 Future State

**Who uses it:** All roles
**Access:** All roles (Engineering Leads approve)

The Future State module compares the three transformation scenarios — Option A (Augmented Human), Option B (Hybrid), Option C (AI-First / ADLC) — side-by-side.

For each scenario you see:

- **Future-state VSM** — per-phase PT/WT/FE after transformation
- **Lead time** (days) — total
- **Deployment frequency** — projected post-transformation
- **CFR / MTTR** — projected
- **Aggregate FE** — projected
- **Key changes per phase** — what specifically changes (e.g. "Phase 5 introduces automated test environment provisioning, removing 14h of wait per cycle")

#### Scenario Comparison Chart

A grouped bar chart shows current vs Option A vs Option B vs Option C across the key DORA + lean VSM metrics. This is the chart most often shown to executive sponsors.

#### Approving a Scenario

Engineering Leads can click **"Approve Scenario"** on Option A, B, or C. The approved scenario becomes the input to the Playbook Context module and the Business Case is locked to that scenario for stakeholder distribution.

---

### 5.10 Business Case

**Who uses it:** Engineering Leads and Platform Admins (assemble); all roles (view)
**Access:** All roles

The Business Case module produces a board-ready financial model for the approved scenario (or for all three if no approval is yet recorded).

For each scenario you see:

- **Investment range** — low / expected / high case in USD
- **ROI timeline** — month-by-month breakdown (year 1, year 2, year 3)
- **ROI multiple** — e.g. 4.2x
- **Payback months** — months to break-even on the investment
- **Realised benefit composition** — % attributable to PT reduction, WT reduction, defect reduction, etc.

#### Sensitivity Analysis

Slide the three sensitivity dials to see how the ROI shifts under different assumptions:
- **Adoption rate** (slow / planned / fast)
- **LLM cost trajectory** (flat / declining / spike)
- **Team retention** (stable / 10% attrition / 20% attrition)

The dials change the curves in the ROI timeline chart in real time.

#### Export

Click **"Export"** to download:
- **Excel** — full financial model with sensitivity tables
- **PPTX** — board-deck-ready slide pack
- **PDF** — printable single-page summary

---

### 5.11 Playbook Context

**Who uses it:** Analysts and Engineering Leads
**Access:** All roles

The Playbook Context module generates a team-tailored implementation plan from the approved scenario plus the team's tech stack, methodology, cloud platform, and compliance constraints.

#### Inputs

In the input panel, set:
- **Tech stack** — language, frameworks, key libraries
- **Team size** and **methodology** (Scrum / Kanban / SAFe / XP)
- **Cloud platform** (Azure / AWS / GCP / on-prem)
- **Compliance constraints** (PCI-DSS / HIPAA / SOX / Dodd-Frank / SOC 2 / none)

#### Document Upload

Drop in any supporting documents — current architecture diagrams, runbooks, sprint retrospectives, prior consultant reports. The platform extracts the relevant passages and grounds the playbook in your team's actual reality, not generic best practice.

#### Generated Playbook

Click **"Generate"** and within 30–60 seconds you'll receive a structured playbook:

- **Phase 1 (Weeks 1–4)** — Foundation
- **Phase 2 (Weeks 5–12)** — Pilot
- **Phase 3 (Weeks 13–26)** — Scale
- **Phase 4 (Weeks 27+)** — Continuous improvement

For each phase: specific milestones, dependencies, risk register, success criteria, and the suggested ownership map.

Export the playbook to Markdown or PDF for distribution.

---

### 5.12 Recommendations & Accuracy

**Recommendations:**
The Recommendations module surfaces cross-cutting actions raised by the pipeline that don't fit cleanly into a single bottleneck or improvement — typically organisational changes (e.g. "Move CAB from Wednesdays-only to event-driven") or platform investments (e.g. "Adopt centralised feature-flag service").

**Accuracy Score:**
The Accuracy Score module scores each completed pipeline run against the platform's domain validation rules. The score appears as a badge alongside the run in the Agents history.

Validation dimensions:
- Schema adherence
- PDLC phase/activity ID validity
- Numerical bounds
- RAG hit quality
- Domain coherence (future FE > current FE for the majority of phases)
- Business case sanity (payback 3–60 months, etc.)

Runs scoring below 80 are flagged for human review before export. Click the score to see the per-dimension breakdown and which agent contributed the most weight to the deduction.

---

### 5.13 Settings

**Who uses it:** Platform Admins only
**Access:** Platform Admin

The Settings page is the configuration hub. It has three sections.

#### LLM Configuration

- **Provider** — Azure OpenAI (preferred) / OpenAI / None (rule-based fallback)
- **API key / endpoint / deployment name**
- **Model** — gpt-4o (recommended) / gpt-4o-mini (faster, lower cost)
- **API version**

Click **"Test"** to validate the configuration with a single inference call. The platform never displays the saved key back to the UI — only "configured" or "missing".

#### ALM Credentials

Add credentials for each ALM tool you connect to. Credentials are persisted encrypted in the `platform_settings` table and re-used by the ALM Connect module. Rotating a credential takes effect on the next pipeline run.

#### Schedule

- **Enabled** — toggle
- **Frequency** — weekly / daily / monthly
- **Day of week** (for weekly) or **Day of month** (for monthly)
- **Hour of day** (24h, local platform timezone)

When enabled, the platform automatically runs the full pipeline for every project flagged as `auto_run = true` at the configured cadence.

---

### 5.14 Reference Pages

These pages provide background context and are read-only for most users.

| Page | What It Shows |
|---|---|
| **Governance** | How to govern AI agent outputs in production — guardrails, accuracy thresholds, escalation patterns |
| **Operations Intelligence** | Observability stack patterns and incident-response playbooks for agent-driven systems |
| **Legacy Modernisation** | Patterns for modernising legacy stacks (mainframe, monolithic Java, classic .NET) toward AI-native |
| **AI Assurance** | Assurance, compliance, and audit patterns — what regulators expect; what evidence to retain |
| **Roles & Slides** | Stakeholder-ready briefing slides explaining the platform and the transformation journey |
| **Glossary** | Definitions of every metric, scenario, agent, and concept used in the platform |

---

## 6. End-to-End Workflows

---

### 6.1 Onboarding a New Project

**Time required:** 30–45 minutes
**Who does it:** Platform Admin or Engineering Lead

1. Open the **Project Selector** in the sidebar and click **"+ New Project"**.
2. Fill in the organisational hierarchy: organisation, portfolio, product group, product, team, industry.
3. Select an **ALM tool** (or leave blank to use manual / CSV).
4. Open **ALM Connect**. Click **"Test Connection"** to verify reachability, then **"Fetch Data"** to pull the last 90 days of work items.
5. Open **Current State VSM** to verify the platform interpreted the data correctly. If something looks off, jump to **VSM Editor** and adjust.
6. Optionally, run a **DORA Assessment** to cross-check the calibrated values against your team's known production telemetry.

The project is now ready for analysis. Move to workflow 6.2.

---

### 6.2 Running a Full Analysis Pipeline

**Time required:** 5 minutes (configuration) + 2–3 minutes (pipeline runtime)
**Who does it:** Engineering Lead or Analyst

1. With a project selected, open the **Agents** page.
2. Click **"Run Full Analysis"**.
3. The platform creates a new run row (status: pending → running) and shows a live progress checklist.
4. Watch each agent complete in turn — typically:
   - `alm_connector` (5s)
   - `vsm_analyzer` (15s)
   - `benchmark_agent` (5s)
   - `bottleneck_analyzer` (30s, LLM call)
   - `improvement_generator` (45s, LLM call)
   - `future_state_designer` (60s, three LLM calls)
   - `business_case_builder` (30s)
5. When the run reaches status: complete, the Accuracy Score appears as a badge.
6. Jump to **Bottlenecks**, **Improvements**, **Future State**, and **Business Case** pages to review results.
7. If a run scored below 80 on Accuracy, click into the breakdown and consider re-running with refreshed VSM data (often an outdated snapshot is the cause).

> **Best practice:** Run the full pipeline at least once a quarter per project. Weekly cadence is appropriate during active transformation; monthly is sufficient steady-state.

---

### 6.3 Completing a DevOps Maturity Assessment

**Time required:** 90 minutes (AI scoring + review) or 4–6 hours (full manual)
**Who does it:** Analyst (score), Engineering Lead (approve)

1. Open **DevOps Maturity** and click **"New Assessment"**.
2. Set the project, team name, industry, and which data sources the AI should use as evidence.
3. Add a short Notes paragraph describing the team's recent context (e.g., "Team has just rolled out trunk-based development; CI pipeline rewrite in flight").
4. Click **"Run AI Scoring"** and wait 60–90 seconds.
5. Review each of the 73 questions:
   - Accept the AI's score if it aligns with reality
   - Override with a note if you disagree
   - Mark N/A if the question doesn't apply
6. As you complete each dimension, the band badge updates live.
7. Review the auto-generated **Action Items** panel. Assign each open item to a responsible owner and a target date.
8. Engineering Lead clicks **"Approve"** to lock the assessment.
9. Click **"Export to VSM"** so the findings enrich the next pipeline run.

---

### 6.4 Preparing a Board-Ready Business Case

**Time required:** 60–90 minutes
**Who does it:** Engineering Lead with Analyst support

1. Confirm a full pipeline run has completed within the last week (run 6.2 if stale).
2. Open **Future State** and compare Options A, B, C side-by-side. Discuss with the team — which scenario is right for this moment? (Hint: regulated, change-averse teams often start with A or B even if C has higher ROI.)
3. Click **"Approve Scenario"** on the chosen option.
4. Open **Business Case** for the approved scenario.
5. Run the **Sensitivity Analysis** dials and capture screenshots of optimistic / expected / pessimistic outcomes.
6. Click **"Export PPTX"** to download the slide pack.
7. Open **Playbook Context** and fill in the team's tech stack, methodology, cloud, and compliance details. Upload any supporting documents (current arch, retro notes).
8. Click **"Generate Playbook"** and download the markdown.
9. Assemble the deck: cover slide → current state diagnosis (bottlenecks page screenshot) → future state vision (scenario comparison) → business case → implementation playbook → ask.
10. Schedule the steering committee review.

---

## 7. Glossary

| Term | Definition |
|---|---|
| **ADLC** | Agent Delivery Lifecycle — an AI-first software development model where AI agents author, review, and deploy with policy guardrails |
| **ALM** | Application Lifecycle Management — collective term for Jira, Azure DevOps, GitHub, Linear, ServiceNow, etc. |
| **Bottleneck** | A phase or activity where wait time, manual effort, or defects significantly drag down flow efficiency |
| **CAB** | Change Advisory Board — a manual change-approval gate, common in regulated environments and often the largest single source of wait time |
| **CFR** | Change Failure Rate — % of deployments that result in a degraded service or rollback |
| **DORA** | DevOps Research and Assessment — the four-metric framework (Deployment Frequency, Lead Time, CFR, MTTR) used as the industry-standard delivery benchmark |
| **DORA Elite** | Top-performing band: multiple deploys/day, <1h lead time, <15% CFR, <1h MTTR |
| **Flow Efficiency (FE)** | Process Time ÷ Lead Time × 100% — the fraction of total lead time that is actually productive |
| **Future State VSM** | A modelled VSM showing PT/WT/FE after a specified transformation scenario is implemented |
| **Improvement** | A platform-recommended action that reduces PT, WT, or defect rate in one or more phases |
| **Lean VSM** | Value Stream Map drawn with lean-manufacturing semantics: explicit PT vs WT for each step, surfacing waste |
| **Lead Time (LT)** | Total elapsed calendar time from start to finish (PT + WT) |
| **LangGraph** | The state-graph orchestration framework used by the platform's 8-agent pipeline |
| **MTTR** | Mean Time To Recovery (sometimes "Mean Time To Restore") — average time from incident detection to service restoration |
| **Option A / B / C** | The three canonical transformation scenarios: Augmented Human / Hybrid / AI-First (ADLC) |
| **Overrides** | Hand-edited values that supersede the AI- or ALM-derived numbers in a VSM snapshot |
| **PDLC** | Product Development Lifecycle — the 7-phase × 36-activity model used throughout the platform |
| **Phase** | One of the 7 PDLC phases: Backlog & Roadmap → Architecture & UX Design → Code Management → CI → CT → CD → Monitoring & Feedback |
| **Pipeline Run** | One end-to-end execution of the 8-agent LangGraph pipeline for a project |
| **Process Time (PT)** | Active, value-adding work time on an activity (hours) |
| **RAG** | Retrieval-Augmented Generation — the BM25-based document retrieval that grounds the AI agents in domain knowledge |
| **Scenario** | One of Option A, Option B, or Option C — a complete transformation model with future-state VSM and business case |
| **Snapshot** | An immutable VSM record at a point in time; the source is one of alm / manual / sample |
| **Source: alm / manual / sample** | How a snapshot was created — auto-extracted, hand-entered, or synthetic demo |
| **VSM** | Value Stream Map — a visual model of a delivery process showing PT, WT, FE for each step |
| **Wait Time (WT)** | Idle / queue / approval time between value-adding activities (hours) |

---

## 8. FAQs

**Q: We don't have a Jira / ADO account that the platform can reach. Can we still use it?**
A: Yes. Use the CSV path in ALM Connect. Export your team's work items to CSV with the required columns (ticket_id, type, phase, etc.) and upload. The platform builds the VSM from the CSV the same way it would from a live ALM pull.

---

**Q: How accurate is the AI-generated bottleneck analysis?**
A: The platform's Accuracy Score (visible in the Agents page) tells you per-run quality. Runs above 80 are generally trustworthy; below 80 indicates a missing or inconsistent input (most often a stale VSM snapshot or unmapped activities). Even high-scoring runs benefit from a 30-minute review-with-engineers session before being presented externally.

---

**Q: What's the difference between Option B and Option C?**
A: **Option B (Hybrid)** keeps humans in the loop for review/escalation — AI handles bounded, well-defined tasks autonomously, but humans approve outcomes before downstream effects. **Option C (AI-First / ADLC)** removes humans from the inner loop for routine work; AI authors, reviews, and deploys with policy guardrails, and humans intervene only on exceptions and policy. Most regulated teams (banking, healthcare) start with B and migrate to C over 12–24 months.

---

**Q: Can I edit the bottleneck text after the pipeline runs?**
A: Yes. Analysts and above can override any AI-generated text in the Bottlenecks page. The original AI text is preserved in the run history for traceability. Use overrides after a workshop with the team to capture nuance the AI missed.

---

**Q: My pipeline run failed at the `improvement_generator` step. What now?**
A: Open the run in the Agents history. The error column shows the exception text. Most common causes:
- LLM rate limit (try again, or contact Platform Admin to bump the quota)
- Cost cap hit (Platform Admin can raise it in Settings)
- Schema validation failed (usually a malformed VSM snapshot — re-pull or edit the VSM)
You can also re-run just the failed agent from the same page, without restarting the whole pipeline.

---

**Q: How do we get the platform to use our own DORA telemetry instead of its calibrated estimates?**
A: In the DORA Assessment page, use the Manual Override fields. Enter your authoritative values (e.g. from your CD pipeline telemetry) and they will be used throughout the platform — Future State projections will start from your real numbers.

---

**Q: Why are there always three scenarios? Can I add a fourth?**
A: Three scenarios is the canonical model the platform was designed around — Augmented Human, Hybrid, AI-First. Adding a fourth would require a code change. In practice teams use the existing three by tuning the "approve" reasoning (e.g., "We approve Option B-modified, deferring the CAB-removal item to phase 3"). Custom-named variants are on the roadmap.

---

**Q: How long does a full pipeline run take?**
A: Typically 2–3 minutes when LLM is available. Rule-based fallback (no LLM key) runs in under 30 seconds but produces more generic output. Slower runs (5+ minutes) usually indicate LLM rate-limiting; check the Settings page for cost cap and provider configuration.

---

**Q: I want to share a future-state deck with my exec sponsor who doesn't have platform access. How?**
A: Use the **Export PPTX** button on the Business Case page. It produces a board-ready deck (cover, current state, future state, business case, ask) you can email directly. For a richer artefact, also export the Playbook Context output as PDF and include it as an appendix.

---

**Q: How often should we re-run the pipeline?**
A: At minimum once a quarter to refresh the diagnosis. During active transformation (weeks 1–12 of a programme), weekly cadence lets you see the impact of changes. Once the team is in steady-state, monthly is enough.

---

**Q: What does the Accuracy Score actually measure?**
A: It evaluates each agent's output against domain rules: schema adherence, valid phase/activity IDs, numerical bounds (FE between 0–100, PT/WT non-negative), RAG retrieval relevance, domain coherence (future FE > current FE for most phases), and business case sanity (payback 3–60 months). Below 80 is a signal to inspect — usually the issue is upstream data, not the AI.

---

**Q: Can the platform run offline / without LLM access?**
A: Yes, with reduced fidelity. With no LLM configured, every agent falls back to a rule-based path that uses pre-curated catalogues (IMPROVEMENT_CATALOGUE, SCENARIOS, BUSINESS_CASES, DORA_ELITE). The output is coherent and pipeline-valid but less specific to your team's nuance. The UI shows a "Rule-based output" badge so users know.

---

**Q: Where do the industry benchmarks come from?**
A: They're embedded in `pdlc_data.py` — derived from a corpus of value-stream observations across financial services, healthcare, retail, energy, and technology sectors plus published DORA report data. Benchmarks are versioned with the platform release; update history is in the changelog.

---

*Document prepared by Cognizant Engineering Effectiveness Programme Team · May 2026*
*For platform support, contact your Platform Admin or raise a request through the programme's Teams channel.*
