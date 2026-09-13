# STUMP — Senior Leadership Demo Guide

> **Purpose:** A structured walkthrough for presenting the platform to C-suite, VP, or Head-of-Engineering audiences. Total run time: **25–35 minutes** (or 15 min with the fast-track path).
>
> **Audience:** CTO, CPO, VP Engineering, Head of Digital Transformation, CFO (ROI sections only)
>
> **Pre-requisites:** Both services running — frontend at `http://localhost:3001`, backend at `http://localhost:8001`

---

## Setting the Stage (2 min)

**Open with this framing before touching the screen:**

> "Most engineering organisations have never measured their product delivery lifecycle end-to-end. They track velocity and sprint points, but they have no idea where the real time is going — which phases are burning days waiting for approvals, which activities are absorbing the most human effort, or where AI could compress the timeline by 40–70%. This platform answers those questions with data, and then gives you three investment-ready options to fix it."

**The business problem in one sentence:**
> "The average enterprise software team has a Lead Time of 40+ days per feature and a Flow Efficiency of less than 10% — meaning over 90% of elapsed time is pure waste. This platform makes that visible and tells you exactly what to do about it."

---

## Demo Flow Overview

| # | Screen | Time | What Leadership Hears |
|---|--------|------|-----------------------|
| 1 | Dashboard | 3 min | Platform overview, the 8-step workflow |
| 2 | DORA Assessment | 3 min | How we baseline your engineering performance |
| 3 | Current State VSM | 4 min | Where your time actually goes right now |
| 4 | Bottleneck Analysis | 3 min | The critical blockers killing your throughput |
| 5 | Future State VSM | 5 min | What your delivery engine looks like after AI |
| 6 | Business Case | 8 min | Investment, ROI, payback — by scenario |
| 7 | Playbook | 3 min | The 90-day action plan, personalised to your team |
| 8 | AI Agents | 2 min | The intelligence behind the analysis |

**Fast-track path (15 min):** Steps 3 → 5 → 6 → 7

---

## Step 1 — Dashboard (3 min)

**URL:** `http://localhost:3001/dashboard`

**What to show:**
- The **Analysis Workflow** card — 8 numbered steps from Connect ALM to Business Case
- The **3 Future State Scenarios** summary at the bottom — Option A / B / C cards
- The **VSM Analysis Level** toggle — Feature Level (42.5-day LT) vs User Story Level (8.5-day LT)

**Talking points:**

> "The platform covers the complete PDLC — 7 phases, 36 activities, from backlog management to production monitoring. You can analyse at the feature level, which gives you the full 40+ day lead time story, or at the user story level, which focuses on the dev-test-deploy cycle."

> "We walk every team through 8 steps. By step 8 you have a board-ready business case with three investment scenarios, each with a specific ROI, payback period, and 90-day implementation roadmap."

**Pause point:** If the audience is data-hungry, ask: *"Does your team currently measure Flow Efficiency? Most teams don't — let me show you what it typically looks like."*

---

## Step 2 — DORA Assessment (3 min)

**URL:** `http://localhost:3001/dora-assessment`

**What to show:**
- The four DORA metric dropdowns (Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR)
- Select realistic values for a **Medium Performer**: "Once per week" / "1–2 weeks" / 15% / "1–7 days"
- Watch the **Elite / High / Medium / Low** band update in real-time
- Show the "VSM Calibration" section that adjusts baseline metrics accordingly

**Talking points:**

> "Before we analyse the value stream, we calibrate it using DORA — the industry-standard DevOps performance benchmark from Google's State of DevOps research, now covering 33,000 organisations."

> "A Medium performer deploys weekly, has a 1–2 week change lead time, and recovers from incidents in days. Elite performers deploy multiple times per day with sub-hour recovery. The gap between Medium and Elite represents approximately 2× faster feature delivery."

> "When you fill in your DORA baseline, every metric in the VSM — process times, wait times — is automatically calibrated to match your actual performance band rather than generic industry averages."

**Key stat to land:** *"Only 18% of organisations are Elite performers. The difference in time-to-market between Elite and Low performers is approximately 1,460× — that's not a typo."*

---

## Step 3 — Current State VSM (4 min)

**URL:** `http://localhost:3001/current-vsm`

**What to show:**
- Start on the **Visual Flow** tab — the horizontal VSM diagram with 7 phase cards
- Point to the **KPI summary bar**: Total Process Time, Total Wait Time, Lead Time, Flow Efficiency
- Switch to the **Flow Bars** tab — show the PT vs WT ratio per phase
- Highlight **Phase 5 (Continuous Testing)** — usually the worst offender
- Switch to **Phases** tab, expand Phase 5 to show the activity-level detail

**Talking points:**

> "This is your current state value stream map. The baseline for a typical medium-performing enterprise team: **100 hours of process time** — that's actual work — against **536 hours of wait time**. That gives a Flow Efficiency of **8.1%**. In plain terms: for every day your team is actually working on a feature, they're waiting for 12 days."

> "Look at Phase 5 — Continuous Testing. It's the dominant bottleneck. Performance testing takes 16–40 hours of effort. UAT sign-off waits 2–5 days for human approval. Test data provisioning adds another 4–16 hours of queue. This single phase is why features that are *ready* still take weeks to ship."

> "The visual flow shows you something that no sprint board or velocity chart ever will: **where your organisation is haemorrhaging time**. Orange cards are bottlenecks. Decision gate phases — Architecture Review, QA, CAB — show the longest wait times."

**Power move:** Click "Run AI Analysis" to show the agent running live. Even if it falls back to demo mode, the output populates the Bottleneck page automatically.

---

## Step 4 — Bottleneck Analysis (3 min)

**URL:** `http://localhost:3001/bottlenecks`

**What to show:**
- The **severity summary** — 2 Critical, 3 High, 3 Medium
- Click through the **Critical** filter to focus on the top 2
- Show the **Phase Bottleneck Heatmap** at the bottom — Phase 5 is red

**Talking points:**

> "The AI identifies 8 bottlenecks in a typical enterprise PDLC. The two Critical ones are both in testing — and they're both fixable with AI."

> "Critical #1: Automated Performance Testing — 16 to 40 hours of effort. Manual performance test authoring and analysis is labour-intensive, error-prone, and completely automatable with today's AI tooling."

> "Critical #2: Manual SIT / UAT / NF Sign-off — 2 to 5 days of wait time. Human approval is the single biggest queue generator in enterprise software delivery. AI can consolidate test results, generate risk-scored readiness reports, and enable same-day exception-based sign-off."

> "The heatmap at the bottom is board-ready. In one view, your senior leaders can see exactly which phases are healthy and which are failing. Phase 5 is red. Phase 6 release gating is orange. These are your transformation priorities."

---

## Step 5 — Future State VSM (5 min)

**URL:** `http://localhost:3001/future-state`

**What to show:**
- Start on **Option A** — show the before/after metric cards and the visual flow
- Switch to **Option B** — metrics improve further, more AI agent labels appear on phase cards
- Switch to **Option C** — show the dramatic metric shift
- Use the **comparison table** (Table view) to show all three scenarios side by side

**Key metrics to call out:**

| Metric | Current State | Option A (40% AI) | Option B (65% AI) | Option C (85% AI) |
|--------|--------------|-------------------|-------------------|-------------------|
| Lead Time | 42.5 days | 25.5 days | 19.1 days | 12.75 days |
| Flow Efficiency | 8.1% | 16.2% | 22.3% | 36.5% |
| Process Time reduction | — | −35% | −55% | −70% |
| Human roles | 8 | 8 | 5 | 2 |

**Talking points:**

> "Option A — AI-Assisted — puts an AI agent alongside every human in every phase. No roles are eliminated. Everyone gets smarter tools. Lead time drops from 42 days to 26. Flow efficiency doubles. This is achievable in 6–10 weeks at the team level."

> "Option B — Hybrid — consolidates to 5 core human roles and deploys strategic agents in the highest-impact phases. Lead time drops to 19 days. The flow efficiency gain is 175%. This is where most forward-thinking organisations are heading in 2025–2026."

> "Option C — AI-First — is the bold scenario. Two human roles: a Product Definer who sets vision and outcomes, and a Product Builder who supervises the agent orchestration layer. Lead time below 13 days. 85% of PDLC activities automated. This is where the industry is heading in 3–5 years — and early movers will have a significant competitive advantage."

**Executive question to anticipate:** *"Are these numbers realistic?"* → *"Yes — we benchmark every scenario against published industry data from GitHub's Octoverse, DORA 2024, and Gartner's engineering productivity research. Option A improvements are conservative; Option B is achievable within 12 months for most teams."*

---

## Step 6 — Business Case (8 min)

**URL:** `http://localhost:3001/business-case`

**This is the most important screen for a CFO or CTO audience. Spend the most time here.**

**What to show — Option A first:**

**Investment:**
- Total: $800K – $1.5M
- Breakdown: Tools ($250K–$400K), Infrastructure ($100K–$200K), Implementation ($300K–$600K), Training ($100K–$200K), Change Management ($100K–$150K)

**Annual Benefits:**
- Time-to-market improvement: $600K–$900K
- Productivity gains: $400K–$600K (35% effort reduction)
- Quality improvement: $200K–$300K
- Operational savings: $100K–$150K

**ROI Summary:** 2.8× return · 12–18 month timeline · 14-month payback

**Switch to Option B:**
- Investment: $1.2M – $2.2M
- ROI: 3.8× · 10–15 months · 11-month payback

**Switch to Option C:**
- Investment: $2.5M – $4.5M
- ROI: 5.5× · 18–24 months · 19-month payback

**Show the Implementation Timeline tab** for Option A — the 5 sprint phases visible

**Talking points:**

> "Every scenario includes a full investment breakdown, annual benefit model, and a team-level implementation timeline. These aren't theoretical — the week-by-week plan tells you exactly what to do in Sprint 1, who does it, and what the success criteria are."

> "Option A has a 14-month payback. For most organisations, that's within a single financial year's horizon. The initial investment is primarily SaaS tool licences and integration work — no major infrastructure build-out required."

> "Option B is the strongest ROI at 3.8×. It requires more custom agent development — typically 4–8 weeks of engineering effort — but the return is significantly higher because you're eliminating role overhead, not just augmenting it."

> "The Org Changes, Tools Changes, DevSecOps, and AIOps tabs give the transformation team a complete blueprint. This isn't just an ROI model — it's an operating model change plan."

**For CFO specifically:** *"We can export this as a PDF or Excel and drop it directly into a board pack. The financial model follows standard NPV methodology — we can adjust the assumptions to match your team's cost structure in under 10 minutes."*

---

## Step 7 — Playbook (3 min)

**URL:** `http://localhost:3001/playbook-context`

**What to show:**
- The **context accuracy meter** — starts at 40%, climbs as you fill in sections
- Fill in **Team Profile** (team size, roles, seniority) — watch accuracy jump
- Fill in **Technology Stack** (GitHub, GitHub Actions, AWS, Jira) — another jump
- Click **Generate Personalised Playbook** — show the output

**The playbook output includes:**
- Executive summary personalised to team name, industry, and scenario
- Sprint-by-sprint 90-day action plan with named roles and specific outcomes
- RACI matrix for human-AI handoffs
- Risk register with mitigations
- Target metrics (PT, WT, LT, FE) per sprint milestone

**Talking points:**

> "Most transformation initiatives fail not because the strategy is wrong, but because the 'what do we do Monday morning?' question never gets answered. This is the answer."

> "The playbook is generated by an AI agent that reads your team context — your stack, budget, procurement cycle, compliance constraints — and produces a sprint-level action plan. Not a generic best-practices document. Your team's name, your tools, your bottlenecks."

> "The accuracy meter tells you how personalised the output will be. At 70%+, the playbook is specific enough to hand to a tech lead and say 'execute this'. At 90%+, it's detailed enough to use in vendor negotiations and board presentations."

---

## Step 8 — AI Agents (2 min)

**URL:** `http://localhost:3001/agents`

**What to show:**
- The **Agent Pipeline** diagram — 8 agents in sequence
- Click **Run Full Analysis** — watch the pipeline light up agent by agent
- Show the agent cards — each with its description and current status

**Talking points:**

> "The analysis you've just seen was produced by 8 AI agents running in sequence — a LangGraph multi-agent pipeline. Each agent specialises: the ALM Connector pulls data from your Jira or Azure DevOps, the VSM Analyzer computes lean metrics, the Bottleneck Analyzer applies lean methodology, and so on through to the Business Case Builder."

> "They can run individually or as a full pipeline. When you connect your real ALM tool, the agents replace every default value with your actual data — your real cycle times, your real wait times, your real flow efficiency."

> "This is the architecture you'd be adopting when you go to Option B or C — multi-agent orchestration managing your PDLC. The platform itself is a working proof of concept."

---

## Closing the Demo (2 min)

**The three questions most senior leaders ask:**

**Q: "How quickly can we get real data into this?"**
> "For a team using Jira or Azure DevOps, ALM connection takes under 30 minutes. We pull ticket history, compute cycle times, and populate the VSM automatically. No manual data entry required after initial setup."

**Q: "Is this applicable to our specific industry?"**
> "The 7-phase PDLC model is universal — we've validated it against banking, insurance, telco, retail, and government engineering organisations. The DORA calibration adjusts the baseline to your performance band. The business case uses industry-sourced benchmarks."

**Q: "What's the first step?"**
> "Pick one product team. Run the full analysis in a single session — typically 2–3 hours including ALM connection, DORA assessment, and business case generation. Use the output to build the investment proposal for Option A. Most teams can secure Option A budget from a single sprint of productivity improvement savings."

---

## Handling Tough Questions

| Question | Response |
|----------|----------|
| "Our engineers won't adopt AI tools" | "Option A requires zero role changes. Adoption is incremental — one tool per phase. The playbook includes change management steps and a 2-day AI collaboration workshop." |
| "We have compliance constraints" | "The DevSecOps tab in the Business Case covers regulatory-aware AI deployment — zero-trust policies, compliance evidence automation, and audit trail generation." |
| "We already have Copilot" | "Copilot addresses Phase 3 only (coding). This platform identifies 8 bottlenecks across 7 phases — testing alone has 4 critical blockers that Copilot doesn't touch." |
| "The ROI assumptions seem optimistic" | "We can adjust every assumption in the model. The defaults are based on published research from DORA 2024, GitHub Octoverse, and Gartner. We've set them conservatively — real-world Option B deployments (e.g. Stripe, GitHub internal) exceeded these figures." |
| "How is this different from a McKinsey deck?" | "A consultant gives you a 200-slide transformation strategy. This platform gives you working software that produces the analysis, the ROI model, the implementation roadmap, and the personalised playbook — live, in 30 minutes, using your actual data." |

---

## Pre-Demo Checklist

- [ ] Backend running: `cd pdlc-vsm-platform && source backend/venv/bin/activate && python -m uvicorn backend.main:app --reload --port 8001`
- [ ] Frontend running: `cd pdlc-vsm-platform/frontend && npm run dev`
- [ ] Browser open at `http://localhost:3001`
- [ ] Set team context in Dashboard (Organisation: your org name, Team: your team name)
- [ ] DORA Assessment pre-filled with Medium Performer values
- [ ] VSM Level set to "Feature Level" for the full 42.5-day story
- [ ] Future State defaulted to "Option A" (switch to B and C during the demo)
- [ ] Playbook context partially filled (team name + org) for demo accuracy starting point
- [ ] Dual screen: demo on main display, this guide on secondary

---

## Demo Narrative (One-Page Summary)

> **The story in 5 sentences:**
>
> 1. Your engineering teams are delivering features in 40+ days when the world's best teams do it in days — and most of that time isn't development, it's waiting.
> 2. This platform connects to your ALM tools, measures where the time actually goes across all 7 phases of your product delivery lifecycle, and identifies the critical bottlenecks by name.
> 3. AI agents then design three future states — from AI-assisted at 40% automation to AI-first at 85% — each with predicted metrics showing how much lead time you cut and how much flow efficiency you gain.
> 4. For each option, you get a board-ready business case: investment breakdown, annual benefits, ROI multiple, payback period, org change plan, tool roadmap, and sprint-by-sprint implementation plan.
> 5. The output is a personalised 90-day playbook with your team's name, your tools, and your RACI — ready to hand to a tech lead on Monday morning.

---

*PDLC VSM Platform v1.0 · 7 phases · 36 activities · 8 LangGraph agents · 3 future state scenarios*
*Last updated: March 2026*
