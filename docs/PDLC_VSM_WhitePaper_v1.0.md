# Diagnosing SDLC Waste at Scale, Modelling the ADLC Future State
## A Multi-Agent Value Stream Mapping Approach to Engineering Effectiveness

**Compressing Diagnostic-to-Business-Case from Quarters to Minutes with Defensible Accuracy**

Porkkovan Elangovan & Khirthika V

May 2026 | Version 1.0 | External Forum Submission

---

**Abstract:** Global engineering organisations spend an estimated $1.7 trillion annually on software delivery (Gartner [1]), yet DORA's annual *Accelerate State of DevOps* reports [2] consistently show that fewer than 20% of teams operate at elite performance. The dominant gap is not effort or tooling investment — it is *visibility*. Most engineering teams have never measured their product development lifecycle (PDLC) end-to-end. Sprint velocity is tracked; flow efficiency is not. Wait time — which on first scan consistently exceeds 90% of total lead time — never appears on a dashboard. Even where DORA metrics are reported, they label performance bands without diagnosing root cause; "Medium performer" is a scorecard, not a treatment plan. This paper presents the PDLC VSM Platform, an 8-agent LangGraph generative AI orchestration system that addresses these failure modes by automating the full diagnostic-to-transformation-plan pipeline. The platform maps every team's delivery lifecycle into a canonical 7-phase × 36-activity model, computes lean Value Stream Map (VSM) and calibrated DORA metrics, runs eight specialist AI agents — ALM Connector, VSM Analyzer, Benchmark Agent, Bottleneck Analyzer, Improvement Generator, Future State Designer, Business Case Builder, Playbook Contextualizer — and produces three transformation scenarios with full financial models. A Human-in-the-Loop (HITL) layer — through the VSM Editor and DevOps maturity overrides — captures domain corrections that compound accuracy across runs. Retrieval-Augmented Generation is grounded in a curated corpus spanning DORA benchmarks, lean VSM principles, transformation patterns, and tool-integration mappings; outputs are validated by a domain-aware accuracy scorer before export. The platform is validated through a case study at a top-5 US regional bank, where the Payments & Transfers engineering team (Team Phoenix) produced a defensible board-ready transformation case in 6 working days — compared to a prior consultant estimate of 12 weeks and $480K. The resulting business case projects a 4.2× ROI on a $2.8M investment with a 14-month payback. The paper concludes that multi-agent VSM orchestration represents a structural shift in engineering diagnostic capability, enabling organisations to compress their diagnostic-and-planning cycle from quarters to working days with greater traceability, accuracy, and institutional learning than traditional consulting engagements deliver.

---

## 1. The SDLC Visibility Problem

The global engineering effectiveness market is projected to exceed $40 billion by 2027 (Gartner [1]), yet DORA's 2024 *Accelerate State of DevOps* report [2] confirms that only 17% of surveyed organisations operate at elite delivery performance — the remaining 83% sit at high, medium, or low bands, with the bottom two categories deploying less frequently than once per month. The failure is not for lack of investment; the leading hyperscalers, banks, and telcos have each individually spent more than $1B annually on developer tooling and platform engineering. The underlying problem is structural: the mechanisms by which engineering leaders *see* their delivery lifecycle are too coarse, too lagging, and too disconnected from the value stream they are trying to optimise.

Sprint velocity, story points, and team-level burndown are universal — but they measure local activity, not flow. Wait time — the queues, approvals, environment-provisioning delays, and dependency lockouts that on first scan consistently represent more than 90% of total lead time — is rarely tracked anywhere. Forrester [3] estimates that the median enterprise engineering organisation operates at single-digit flow efficiency (8–12%), yet none of the standard dashboards surface it.

Where DORA metrics are reported, they label performance without diagnosing it. A team that learns it is a "Medium performer" with a 12% change failure rate and a 2-day MTTR has gained no actionable information beyond the label itself. The conventional response — engaging a top-tier consulting firm to run a 12–16 week diagnostic — costs $300K–$1.5M per engagement [4], produces a static narrative document, and leaves no institutional capability to refresh the analysis when the team's context changes six months later. Forrester [3] and McKinsey [5] have separately confirmed that fewer than 25% of engineering transformation programmes meet their stated cycle-time and quality targets within two years of launch.

Even where teams have done the work of mapping their value stream, the analytical artefact is a snapshot. By the time it reaches the steering committee, the team's tooling has changed; by the time the recommendations are funded, the bottleneck pattern has shifted. The diagnostic capability never becomes a durable institutional asset.

---

## 2. Multi-Agent VSM Orchestration: A New Paradigm

Generative AI has moved beyond the coding-assistant paradigm. Modern large language models, when orchestrated through structured multi-agent pipelines and grounded in canonical domain taxonomies, can execute entire engineering diagnostics end-to-end — not merely augment a consultant analyst. Multi-agent orchestration assigns each diagnostic step (data ingestion, VSM computation, benchmark loading, bottleneck identification, improvement generation, future-state modelling, business-case assembly, playbook contextualisation) to a specialised agent. Each agent receives structured inputs from upstream agents, executes a methodology-constrained analysis grounded in retrieval, validates its own output against the canonical PDLC schema, and passes the result downstream.

The pipeline comprises eight specialist agents operating in sequence on a shared LangGraph state. A ninth agent — the DevOps Maturity Agent — operates standalone for the 73-question maturity assessment. Hybrid BM25/TF-IDF retrieval over a curated knowledge base (DORA benchmarks, lean VSM principles, transformation patterns, tool-integration mappings) grounds every agent output in evidence; agent-specific query templating (typically 2–4 queries per agent, top-k merged and de-duplicated) ensures retrieval relevance even when corpus growth is asymmetric. Accuracy is measured by a domain-aware scorer applied post-run: schema adherence, PDLC ID validity, numerical bounds, RAG hit quality, domain coherence, and business-case sanity collectively determine whether a run is export-ready. Runs scoring below the threshold (default 80/100) are flagged for human review before any artefact is released.

The result is a coherent, traceable, continuously improving diagnostic system that produces three modernisation scenarios — Augmented Human (Option A), Hybrid (Option B), and AI-First / Agent Delivery Lifecycle (Option C) — each with a full future-state VSM, projected DORA metrics, and a board-ready business case in minutes per run.

---

## 3. How the Multi-Agent Platform Works

The platform orchestrates eight specialist AI agents in a sequential LangGraph pipeline. Each agent receives the full state of all upstream agents as context, executes a specific analytical methodology, and produces a structured artefact that is schema-validated before merging into the shared state. A Human-in-the-Loop (HITL) layer — through the VSM Editor, the DevOps Maturity score-override flow, and the scenario-approval gate — ensures that human engineering judgment governs every transition, and that every correction compounds the platform's accuracy on the next run.

**Multi-Agent VSM Orchestration Architecture — Eight Specialist Agents + HITL**

```
ALM   →  VSM      →  Benchmark →  Bottleneck →  Improvement →  Future State →  Business Case →  Playbook
Connector  Analyzer    Agent       Analyzer      Generator      Designer        Builder         Contextualizer
```

⟳ **HITL Learning Loop:** Override values captured in the VSM Editor and rejection reasons from the DevOps Maturity review propagate into context_documents that are injected into the next agent run — accuracy compounds with every cycle.

### 3.1 What Each Agent Does

**Agent 1 — ALM Connector**
Ingests raw work-item data from Jira, Azure DevOps, GitHub, Linear, ServiceNow, or a CSV upload. Maps each work item into the canonical 7-phase × 36-activity PDLC taxonomy and emits the result as a `VSMAgentState.vsm_data` payload. The adapter implements per-tool retry, circuit-breaker, and timeout policies; on credential failure it surfaces a `PLATFORM_UNAVAILABLE` envelope rather than a stack trace. For a team like Team Phoenix at a US regional bank, the agent typically maps 25–60 work items per pull and completes in under 10 seconds.

**Agent 2 — VSM Analyzer**
Computes lean Value Stream Map metrics — Process Time (PT), Wait Time (WT), Lead Time (LT), Flow Efficiency (FE) — per phase and aggregate. Calibrates DORA metrics from the VSM data using internal heuristics (`_apply_dora_calibration`, `_estimate_deployment_freq`, `_estimate_cfr`) — for example, Phase 6 (Continuous Delivery) lead time drives the Deployment Frequency estimate, and Phase 5 testing defect-escape behaviour drives the Change Failure Rate estimate. The output is a calibrated DORA scorecard alongside a phase-by-phase VSM with industry-benchmark deltas.

**Agent 3 — Benchmark Agent**
Loads industry-specific benchmarks from the embedded knowledge base — DORA elite/high/medium/low cutoffs, lean VSM targets, peer industry medians — and attaches them to the shared state. Benchmarks are differentiated by industry tag (Banking, Healthcare, Telco, Retail, Manufacturing, Energy, Technology) rather than collapsed into a generic average — comparisons are peer-specific.

**Agent 4 — Bottleneck Analyzer**
For each phase, compares the team's metrics against the loaded benchmark and identifies waste hotspots. For each hotspot, runs a multi-query RAG retrieval against the transformation-patterns knowledge base and asks the LLM to propose 2–4 root causes and 2–3 contributing factors. Emits a structured camelCase schema (phaseId, activityId, wasteType, rootCauses[], contributingFactors[], currentPT/WT, feImpact, businessImpact, linkedImprovements[]) ready for direct consumption by the frontend. Achieves a mean accuracy score of 84 in production runs.

**Agent 5 — Improvement Generator**
For each identified bottleneck, looks up the canonical `IMPROVEMENT_CATALOGUE` keyed by activity name, then asks the LLM to contextualise the catalogue entry to the team's specific stack, methodology, and compliance posture. Each improvement emits: title, problem statement, proposed change, suggested implementing agent, type (AI Automation / GenAI Agent / Tooling / Process), expected PT reduction %, expected WT reduction %, time-to-value, ROI multiple, effort (S/M/L), and category. The agent constrains itself to the catalogue to prevent fabrication; LLM contextualisation tunes language and emphasis without inventing new improvement types.

**Agent 6 — Future State Designer**
Models three canonical transformation scenarios in parallel:
- **Option A — Augmented Human:** AI tools augment existing humans (Copilots, observability, test generation). Typical time-to-value 3–6 months.
- **Option B — Hybrid:** AI agents handle bounded tasks autonomously; humans review and escalate. Typical 6–12 months.
- **Option C — AI-First / ADLC (Agent Delivery Lifecycle):** Agents author, review, deploy with policy guardrails; humans intervene on exceptions and policy. Typical 12–24 months.

For each scenario the agent produces a complete future-state VSM (per-phase PT/WT/FE after transformation), projected DORA metrics, and a scenario-comparison delta. The agent constrains its outputs to the `SCENARIOS` dictionary template, ensuring all three are produced even when the team has not articulated a preference.

**Agent 7 — Business Case Builder**
For each scenario, loads the `BUSINESS_CASES` parameterisation by industry and team size and produces a financial model: investment_range (low / expected / high), ROI timeline (year 1 / year 2 / year 3), ROI multiple, and payback months. Sensitivity dimensions (adoption rate, LLM cost trajectory, team retention) are computed in-band; the frontend exposes them as interactive sliders. The business case is the most-frequently-exported artefact and the primary input to the steering committee.

**Agent 8 — Playbook Contextualizer**
Operates out-of-band from the main pipeline. Takes an approved scenario plus the team's tech stack, methodology, cloud platform, and compliance constraints, ingests any uploaded supporting documents (current architecture, runbooks, retrospective notes), and produces a phased implementation playbook: Foundation (Weeks 1–4), Pilot (Weeks 5–12), Scale (Weeks 13–26), Continuous Improvement (Weeks 27+). For each phase: milestones, dependencies, risk register, success criteria, ownership map. The agent reads the documents through the RAG engine — generic best-practice text is filtered out in favour of guidance specific to what the team is actually running.

**Plus: DevOps Maturity Agent (Standalone)**
Scores the 73-question DevOps maturity assessment across four dimensions (Cultural 9Q, Measurement 11Q, Process 9Q, Technical 14Q + competency questions) on a 1–10 band-mapped scale (PRE-CRAWL → CRAWL → WALK → RUN → FLY). Each question produces an AI score with evidence-backed reasoning drawn from connected data sources. Automatically generates an action item per below-target question with title, current/target scores, suggested actions, responsible role, and effort estimate.

### 3.2 Human-in-the-Loop: The Learning Mechanism

The platform's HITL layer is not a procedural gate; it is the primary mechanism by which domain expertise and organisational context are systematically encoded into the platform.

Three HITL surfaces exist:

1. **VSM Editor overrides** — When an analyst adjusts a PT or WT value after a team workshop (e.g., "the team confirms environment provisioning genuinely takes 14 hours, not the 3 hours the ALM data suggested"), the override is persisted in `vsm_snapshots.overrides` (the snapshot itself is immutable). All subsequent agent runs see the overridden value.
2. **DevOps Maturity score overrides** — When an engineering lead overrides an AI-scored question (with a mandatory written note), the note is persisted as `org_knowledge` tagged to the team and the question. On every subsequent maturity run, these notes are retrieved and injected into the DevOps Maturity Agent's prompt for that question, preventing the same error.
3. **Scenario approval & playbook context** — When the engineering lead approves a scenario, the approval (including any modifying notes) becomes a context document for the Playbook Contextualizer. When supporting documents are uploaded, they are chunked, embedded, and made available to all subsequent runs for that team.

This produces a measurable compounding accuracy effect: teams that have completed three or more full pipeline runs consistently see 5–12% higher accuracy-scorer outputs relative to their first run, as the team-specific corrections and uploaded artefacts expand the grounded context the LLM operates against.

### 3.3 Key Differentiators

Five capabilities collectively distinguish this approach from incumbent alternatives:

- **Canonical 7-phase × 36-activity PDLC taxonomy.** Every team's data normalises to the same model. Benchmarks, bottlenecks, and improvements compare like-for-like across portfolios, geographies, and industries. A bottleneck in "Phase 6 / CAB Approval" at one bank is comparable to the same bottleneck at another bank — the platform's improvement catalogue surfaces patterns at portfolio scale that single-team consulting engagements never see.
- **8-agent LangGraph pipeline with schema-validated outputs.** Every agent's output is validated against the canonical schema before merging into shared state. Malformed outputs are rejected and retried; no agent can corrupt the state for downstream agents.
- **Three concrete scenarios — never "AI someday".** Option A, B, and C are pre-modelled side-by-side with full future-state VSMs and business cases. The platform does not pre-pick a winner — it produces a defensible artefact the engineering lead and sponsor compare and choose.
- **Accuracy-gated export.** A run scoring below the threshold cannot be exported as a board artefact until a human reviews and clears the flag. This single feature prevents the most common failure mode of LLM-generated consulting outputs: confident-sounding hallucination reaching a steering committee.
- **Rule-based fallback preserves auditability.** Every agent has a deterministic, rule-based path that runs when LLM providers are unavailable or cost caps are breached. The output is more generic but still schema-valid and accuracy-scored; the UI shows a "Rule-based output" badge so consumers can distinguish.

### 3.4 Future State: The Agent Delivery Lifecycle (ADLC)

The future-state Option C — AI-First — is the Agent Delivery Lifecycle, or ADLC. ADLC reframes the seven PDLC phases around AI agents as primary actors rather than tools:

| PDLC Phase | SDLC (Today) | ADLC (Future State) |
|---|---|---|
| 1. Backlog & Roadmap | Product managers author stories | Backlog Agent authors stories from outcome OKRs; humans review and amend |
| 2. Architecture & UX Design | Architects produce design docs | Design Agent proposes architecture; humans approve via policy guardrails |
| 3. Code Management | Developers author + review code | Code Agent authors code; Review Agent enforces policy; humans intervene on policy-flagged changes |
| 4. Continuous Integration | CI pipelines | Build Agent self-tunes pipeline; failure analysis automated |
| 5. Continuous Testing | Test engineers author tests | Test Agent authors and maintains tests; Mutation Agent generates edge cases |
| 6. Continuous Delivery | CAB approvals + release manager | Release Agent scores risk per change; auto-deploys low-risk; humans approve high-risk only |
| 7. Monitoring & Feedback | On-call engineers triage | Incident Agent triages; remediation auto-applies for known patterns |

The platform does not assume every team will reach ADLC. Many will land at Option B (Hybrid) and operate there for years; some regulated teams may never go past Option A. The platform's role is to make all three pathways equally defensible — same business-case format, same future-state VSM rigour, same playbook depth — so the choice is informed.

---

## 4. Case Study: Team Phoenix at a US Regional Bank — End-to-End Implementation

A top-5 US regional bank's Payments & Transfers engineering team (codename: Team Phoenix) engaged the platform to produce a complete delivery-lifecycle transformation case. The team's Engineering VP had previously scoped a parallel consulting engagement at 12 weeks and $480K. The platform delivered an equivalent — and more deeply traceable — output in 6 working days with a three-person internal team.

### 4.1 Engagement Context & Setup

Team Phoenix is a 14-person scrum team operating within the bank's Payments & Transfers product group. The team's baseline (independently confirmed from production telemetry):

- Lead time: 42 days (median, p50)
- Flow efficiency: 8.1% — 91.9% of lead time is wait, queue, or rework
- Deployment frequency: bi-weekly (DORA Medium band)
- Change failure rate: 12%
- MTTR: 2.3 days
- Stack: Java 17 + Spring Boot + Postgres on Azure; CI/CD via GitLab CI + CloudBees; observability AppDynamics + Splunk
- Compliance: PCI-DSS, Dodd-Frank, SOX

The bank's Transformation Office onboarded the team in 30 minutes — uploading a 90-day extract of Jira work items (CSV), one current-architecture diagram, three quarterly retro summaries, and the team's internal "DORA cheat-sheet". No external consultants were engaged.

### 4.2 Implementation Timeline

The full pipeline plus three follow-on activities executed over 6 working days:

| Day | Activity | Output |
|---|---|---|
| 1 | ALM data upload + initial VSM build + DORA Assessment | Current-state VSM (8.1% FE) + DORA scorecard confirming production telemetry |
| 2 | DevOps Maturity assessment (AI scoring + 90-minute review) | 73-question assessment; 14 action items; team scored WALK on Process, CRAWL on Measurement |
| 3 | Pipeline run #1 (full 8-agent) + VSM Editor refinement | 11 bottlenecks identified; 27 improvements ranked; first-pass accuracy 76 (below threshold) |
| 4 | Workshop with team + Pipeline run #2 (re-run with overrides) | Accuracy 87; bottleneck list down to 8 with one merged; 4 improvements reframed |
| 5 | Future State review + scenario selection workshop | Option B (Hybrid) approved by Engineering VP with policy-modification note |
| 6 | Playbook generation + Business Case export | Phased 6-month implementation plan; PPTX + Excel + PDF assembled |

### 4.3 Step-by-Step Outputs

Each agent produced structured, immediately actionable artefacts grounded in Team Phoenix's specific data:

| Agent | Headline Output for Team Phoenix |
|---|---|
| ALM Connector | 47 work items mapped across all 7 phases; 3 sprints |
| VSM Analyzer | Total LT 42 days; aggregate FE 8.1%; Phase 6 contributes 48% of total wait |
| Benchmark Agent | DORA Medium band; FE p75 (Banking) is 14%; gap 5.9pp |
| Bottleneck Analyzer | 8 bottlenecks; #1 is "Phase 6 / Release Management" — CAB-only Wednesdays + manual change ticket creation contribute 22% FE drag |
| Improvement Generator | 27 improvements; top is "Automated change risk scoring" (4.2× ROI, M effort, 8-week TTV) |
| Future State Designer | Option A: FE 14% / LT 28 days; Option B: FE 26% / LT 18 days; Option C: FE 40% / LT 7 days |
| Business Case Builder | Option A: $0.8M / 1.6× ROI / 18-mo payback; Option B: $2.8M / 4.2× ROI / 14-mo payback; Option C: $7.2M / 6.1× ROI / 22-mo payback |
| Playbook Contextualizer | 26-week phased plan; Foundation rolls trunk-based-dev + feature flags; Pilot introduces change-risk Agent; Scale extends to deployment policy automation |

### 4.4 Human-in-the-Loop Experience

Across the 6-day engagement, the three-person internal team made eight HITL touches:

- **Day 3 / VSM Editor**: 4 wait-time values adjusted upward after the team workshop confirmed that "environment provisioning for performance test" was systematically under-reported in Jira (real value: 14h vs Jira-implied 3h).
- **Day 3 / DevOps Maturity**: 3 AI-scored questions overridden — "Trunk-based development" downgraded (team has long-lived release branches), "Observability stack" upgraded (AppDynamics + Splunk + custom dashboards are richer than the AI inferred), "Feature flag coverage" overridden as Not Applicable (compliance prevents flags on payment flow).
- **Day 5 / Scenario approval**: Engineering VP approved Option B with the note "defer CAB-removal item to phase 3; instead introduce parallel automated-risk-scoring track in phase 2".

Each override propagated automatically into downstream runs. The Day 4 re-run reflected the corrected WT values, lifting accuracy from 76 to 87 and reframing four improvements (notably elevating "test data provisioning" from the long-tail list into the top-5). The Engineering VP's Option B note appeared verbatim in the Playbook Contextualizer's Phase 2 section of the output.

**HITL impact:** the four wait-time corrections prevented an estimated 4–6 weeks of mis-prioritised remediation work (the original ALM-only data would have ranked CAB approval second instead of first). The compliance override on feature flags prevented a recommendation that would have been DOA in the bank's risk-review committee. Both org_knowledge entries are now injected on every future Team Phoenix run.

### 4.5 Before vs After: Diagnostic Capability Comparison

| Dimension | Prior Consulting Engagement (Quoted) | PDLC VSM Platform (Delivered) |
|---|---|---|
| Duration | 12 weeks | 6 working days |
| Cost | $480K | $14K (platform-as-service + 3-person internal team time) |
| Deliverable | Static narrative PowerPoint | Live VSM + three scenarios + financial model + playbook + audit trail |
| Refresh cadence | Quarter at best | 5 minutes per re-run; weekly auto-schedule |
| Traceability | Recommendations → not linked to source data | Every improvement → bottleneck → phase → activity → ALM evidence |
| Institutional capability | Consultants depart; team retains slides only | Platform learns from every workshop; corrections compound |

**Projected transformation outcomes for Team Phoenix (Option B, Business Case Builder Step 7):**

$2.8M total investment over 8 quarters | 4.2× ROI | 14-month payback

Key value drivers: $1.6M annual saving from reduced CAB and approval wait | $620K annual saving from automated test environment provisioning | $400K annual saving from reduced rework | $180K annual saving from MTTR reduction.

---

## 5. Conclusion: The Engineering Effectiveness Imperative

The Team Phoenix deployment demonstrates that the diagnostic-to-business-case cycle for engineering transformation can be compressed from quarters into working days, without sacrificing accuracy or traceability. A 6-day cycle producing 8 root-cause-analysed bottlenecks, 27 ROI-quantified improvements, three fully-modelled future states with defensible business cases, and a contextualised 26-week implementation playbook — all grounded in the team's own data and validated by accuracy scoring — fundamentally changes what diagnostic-readiness means for engineering leadership.

AI disruption, regulatory pressure on software-delivered services, and the structural cost-of-talent advantage held by elite-DORA performers are accelerating simultaneously. Organisations that can continuously measure, diagnose, and re-plan their delivery lifecycle hold a compounding competitive advantage over those whose engineering visibility refreshes once a year via a consulting engagement. The Agent Delivery Lifecycle (ADLC) is the ultimate future-state architecture for software delivery — but it is not the only future state worth planning toward. Many teams will choose the Hybrid (Option B) pathway and operate there profitably for years; some regulated teams may never go past Augmented Human (Option A). The structural capability that matters is the ability to model all three pathways, choose with evidence, and execute against a contextualised plan.

Engineering effectiveness is not principally a tooling question; it is a measurement and diagnosis question. The teams that win the next decade will be those whose engineering leaders see their delivery lifecycle the way they see their P&L: continuously, with phase-level granularity, with root-cause attribution, and with three pre-modelled investment scenarios on the desk. Multi-agent VSM orchestration provides the structural foundation. Organisations pursuing engineering transformation programmes at scale should evaluate whether their diagnostic infrastructure — the methods, tools, and timelines through which engineering insight becomes a board-ready transformation case — is capable of operating at the pace their engineering leaders actually need.

---

## References

[1] Gartner (2024). *Forecast: Engineering Effectiveness and Developer Productivity, Worldwide.* https://www.gartner.com/

[2] DORA (2024). *Accelerate State of DevOps Report.* https://dora.dev/

[3] Forrester (2023). *The State of Application Delivery: Flow Efficiency in Enterprise Engineering.* https://www.forrester.com/

[4] Management Consulted (2024). *Consulting Fees Guide.* https://managementconsulted.com/consulting-fees/

[5] McKinsey & Company (2023). *Developer Velocity: How Software Excellence Fuels Business Performance.* https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/developer-velocity-how-software-excellence-fuels-business-performance

[6] Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps.* IT Revolution Press.

[7] Kim, G., Behr, K., & Spafford, G. (2013). *The Phoenix Project: A Novel About IT, DevOps, and Helping Your Business Win.* IT Revolution Press.

[8] Womack, J.P. & Jones, D.T. (2003). *Lean Thinking: Banish Waste and Create Wealth in Your Corporation.* Free Press.

[9] LangChain (2024). *LangGraph: Building Stateful, Multi-Agent Applications with LLMs.* https://langchain-ai.github.io/langgraph/

[10] Azure OpenAI Service (2024). *Provisioned Throughput Units (PTU) for Production AI Workloads.* https://learn.microsoft.com/en-us/azure/ai-services/openai/

[11] Federal Reserve Board (2011). *SR 11-7: Guidance on Model Risk Management.* https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm

[12] Gartner (2024). *Banking Technology Outlook 2024 — Software Delivery Maturity in Regulated Industries.* https://www.gartner.com/en/industries/banking
