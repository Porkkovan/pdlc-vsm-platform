// ─── Transformation Roadmap — shared across FutureStatePage + BusinessCasePage ─

export const LANE_STYLE = {
  org:       { label: '👥 People & Org',       bg: 'bg-blue-50',   border: 'border-blue-200',   badge: 'bg-blue-600',   text: 'text-blue-800',   dot: 'bg-blue-500' },
  tools:     { label: '🛠️ Tools & Platform',   bg: 'bg-purple-50', border: 'border-purple-200', badge: 'bg-purple-600', text: 'text-purple-800', dot: 'bg-purple-500' },
  devsecops: { label: '🔒 DevSecOps',           bg: 'bg-red-50',    border: 'border-red-200',    badge: 'bg-red-600',    text: 'text-red-800',    dot: 'bg-red-500' },
  aiops:     { label: '🤖 AIOps',               bg: 'bg-indigo-50', border: 'border-indigo-200', badge: 'bg-indigo-600', text: 'text-indigo-800', dot: 'bg-indigo-500' },
  measure:   { label: '📊 Measure & Validate',  bg: 'bg-teal-50',   border: 'border-teal-200',   badge: 'bg-teal-600',   text: 'text-teal-800',   dot: 'bg-teal-500' },
}

export const PHASE_COLOR = {
  blue:   'bg-blue-600',   green:  'bg-green-600', amber: 'bg-amber-500',
  purple: 'bg-purple-600', teal:   'bg-teal-600',  red:   'bg-red-600',
}

export const TRANSFORMATION_ROADMAP = {
  'option-a': {
    duration: '6–10 weeks', humanModel: 'Human-Led + AI Augmented',
    phases: [
      {
        range: 'Week 1', name: 'Foundation', color: 'blue',
        org:       ['Run AI skills gap survey across all PDLC roles', 'Nominate AI Champion (senior dev, 10% time)', 'Team kickoff: share VSM baseline, agree success metrics'],
        tools:     ['Activate GitHub Copilot Enterprise for all developers', 'Configure content exclusions for PII and secrets', 'Audit CI/CD pipeline — document all manual steps to automate'],
        devsecops: ['Enable GitHub Secret Scanning + Dependabot on all repos', 'Enable Push Protection (blocks credential commits)'],
        aiops:     [],
        measure:   ['Run baseline VSM on this platform — capture PT, WT, LT, FE BEFORE any tool goes live'],
      },
      {
        range: 'Week 2–3', name: 'Quick Wins', color: 'green',
        org:       ['Redefine JDs: add "AI output quality review" to all developer roles', 'Update Definition of Done — add AI review checkpoint for code and tests'],
        tools:     ['Deploy ReviewAgent / Copilot code review on all PRs', 'Enable Jira AI backlog health + sprint suggestions for PO', 'Configure AI BDD scenario suggestions for QA team (ScenarioGen)'],
        devsecops: ['Integrate Snyk / Semgrep SAST into CI pipeline (advisory mode week 1, blocking week 2)', 'Wire Snyk → Jira: Critical/High auto-creates ticket'],
        aiops:     [],
        measure:   ['Measure code review turnaround time (baseline vs Copilot-assisted)'],
      },
      {
        range: 'Week 3–6', name: 'Core AI Tools', color: 'amber',
        org:       ['Establish lightweight AI CoE: Acceptable Use Policy, tool register, monthly review cadence', 'Update sprint ceremony guides: AI-assisted refinement, planning, retro'],
        tools:     ['Deploy AI performance test analyzer (QA)', 'Deploy DataGen / Faker for synthetic test data in CI pipeline', 'Enable AI-generated IaC templates + Secure-by-Design validation (Checkov)', 'Integrate AI APM platform trial (Dynatrace Davis AI or Datadog AI)'],
        devsecops: ['Switch SAST to blocking mode for Critical/High findings', 'IaC security scan live in every CI pipeline run'],
        aiops:     ['Deploy AI APM — allow 1-week baseline learning, no alerts yet', 'Configure top 3 auto-remediation runbooks (pod restart, cache flush, DB pool)'],
        measure:   ['Track test authoring time vs AI-assisted baseline', 'Monitor SAST false positive rate — tune to < 20%'],
      },
      {
        range: 'Week 6–8', name: 'Embed & Adopt', color: 'purple',
        org:       ['Half-day AI collaboration workshop for all personas', 'Each persona creates 3 reusable prompts → shared team prompt library', 'Update OKRs: include lead time and flow efficiency targets'],
        tools:     ['Configure AI-driven incident routing (low-severity incidents first)', 'AI APM alerts enabled — suppress legacy alerts during transition'],
        devsecops: ['Automated compliance evidence collection pipeline live (test results, SAST, approvals → S3)', 'AI Release Manager evaluating low-risk releases (advisory mode)'],
        aiops:     ['AI APM fully routing alerts — legacy alert suppression active', 'Configure NLP incident classifier (train on last 6 months incidents)'],
        measure:   ['Mid-point VSM snapshot — compare PT/WT/FE to baseline', 'Measure AI tool adoption rate per persona'],
      },
      {
        range: 'Week 8–10', name: 'Measure & Report', color: 'teal',
        org:       ['AI Adoption Retrospective: what worked, what had low adoption, top 3 tuning actions', 'Assess readiness for Option B upgrade'],
        tools:     ['All 5 core tools operating — Copilot, ReviewAgent, ScenarioGen, DataGen, AI APM', 'Team prompt library curated and in use'],
        devsecops: ['SAST running on 100% of PRs — FP rate confirmed < 20%', 'Compliance evidence archive: automated capture every deployment'],
        aiops:     ['AI APM primary for all alert routing — legacy removed', 'Telemetry Sentinel: first production signal → backlog ticket generated'],
        measure:   ['Full VSM re-run vs baseline (target: -35% PT, -55% WT, +10 pts FE)', 'ROI calculation: (saved hours × rate) / tool cost — target 2.8× annualised', 'Publish team case study — outcomes, lessons, next steps'],
      },
    ]
  },
  'option-b': {
    duration: '12–16 weeks', humanModel: 'Hybrid: 5 Core Roles + 21 Assistive Agents (← on-demand)',
    phases: [
      {
        range: 'Week 1–2', name: 'Architecture & Design', color: 'blue',
        org:       ['Design 5-role operating model (PO, Tech Lead, Developer, QA Lead, DevOps)', 'Hold 1-to-1 role transition conversations — no surprises', 'Establish AI Agent Operations rituals (daily 15-min health check, weekly review)', 'Select and configure consolidated ALM platform (Jira AI / Linear)'],
        tools:     ['Design LangGraph StateGraph architecture for 21 agents — inputs, outputs, state schema, handoff triggers', 'Set up Python env: langgraph, langchain, langchain-openai', 'Configure Azure OpenAI connection (endpoint, API key, deployment name)', 'Register MCP tool definitions for GitHub, Jira, Azure DevOps'],
        devsecops: ['Run Option A DevSecOps baseline (SAST, Secret Scanning, Dependabot) if not already live'],
        aiops:     [],
        measure:   ['Capture VSM baseline if not already done (Week 1 action — no baseline = no ROI evidence)'],
      },
      {
        range: 'Week 2–6', name: 'Agent Build Sprints', color: 'green',
        org:       ['Sprint A (Wk 2–3): team operates alongside agents — shadow mode begins', 'All agents must pass 50-item quality gate before production promotion', 'Agent Ops team: agent registry live with SLOs per agent'],
        tools:     ['Sprint A: Build FeatureGen Agent (feature intent → stories + ACs) — deploy staging', 'Sprint A: Build StoryGen Agent + ReviewAgent (PR diff → structured findings)', 'Sprint B: Build QA Orchestrator + DataGen Agent (schema → synthetic PII-safe data)', 'Sprint C: Build AI Release Manager (quality + security + performance gate validation)', 'Sprint C: Build Compliance-as-Code Orchestrator (GDPR, DORA, Basel III rules in OPA)', 'Build MCP tool integrations: GitHub API, Jira API, Snyk, Azure DevOps'],
        devsecops: ['Design Secure-by-Design Architect agent: load CISO-approved policy library', 'Encode GDPR rules in OPA: PII in logs, consent check, data retention', 'Encode DORA rules: change failure rate < 5%, recovery time SLA'],
        aiops:     ['Design self-healing CI/CD: build failure telemetry export to Datadog', 'Build ML failure predictor on 6 months build history'],
        measure:   ['Track agent quality gate results per sprint — require 80% acceptance before promotion'],
      },
      {
        range: 'Week 6–10', name: 'Integration & Parallel Run', color: 'amber',
        org:       ['Deploy all 21 agents in shadow mode — agents run alongside humans, humans still decide', 'Document human-AI handoff protocol for each PDLC phase (swim-lane diagrams)', 'Team transitions to 5-role model from Sprint 7 — 1-day onboarding per new role', 'Agent Ops: daily quality score monitoring; tuning sprint triggered if acceptance < 80%'],
        tools:     ['FeatureGen + StoryGen live in shadow mode — compare vs manual PO output', 'ReviewAgent live — developer reviews AI findings (not full diff)', 'QA Orchestrator + DataGen live — QA Lead approves scenario list before run', 'AI Release Manager live in advisory mode — Tech Lead reviews gate decisions'],
        devsecops: ['Secure-by-Design Architect: deploy to CI pipeline in warn-only mode — measure FP rate', 'Compliance-as-Code Orchestrator: validate against last 3 months commit history (baseline check)'],
        aiops:     ['Self-healing CI/CD in advisory mode — log predicted failures, compare to actuals', 'AIOps platform trial (Dynatrace Davis AI) — 2-week learning baseline period'],
        measure:   ['2-week parallel run comparison: agent output vs human output — measure delta', 'Track: story writing time, code review turnaround, test provisioning time'],
      },
      {
        range: 'Week 10–13', name: 'Compliance Agent Setup', color: 'red',
        org:       ['CISO briefing on Secure-by-Design Architect and Compliance-as-Code Orchestrator — get sign-off', 'MRO (Model Risk Officer) review: MRM Agent parameters, kill-switch procedure', 'Governance Controller architecture approved by CTO + CCO'],
        tools:     ['Secure-by-Design Architect: switch from warn to blocking mode (Critical/High violations)', 'MRM Agent: configure model registry, drift thresholds, kill-switch parameters', 'Multi-Agent Governance Controller: test agent handoff protocols, validate bypass detection', 'Telemetry Sentinel: configure Business Risk Score thresholds, connect governance dashboard'],
        devsecops: ['Secure-by-Design Architect: CISO reviews and approves policy library (all rules)', 'Compliance-as-Code Orchestrator: full GDPR, DORA, Basel III ruleset validated — blocking mode', 'Compliance evidence pipeline: every deployment archives to S3/Azure Blob (7-year retention)', 'MRM Agent connected to all model versioning pipelines — kill-switch tested in staging'],
        aiops:     ['Telemetry Sentinel signal rules configured — first auto-Jira ticket generated', 'AIOps platform: alert baseline complete — switch from legacy alerts to AI routing'],
        measure:   ['Compliance coverage baseline: confirm 100% of commits checked against ruleset', 'Run 3 incident simulations to validate Governance Controller bypass detection'],
      },
      {
        range: 'Week 13–16', name: 'Full Deployment', color: 'purple',
        org:       ['Remove shadow mode — 21 agents are primary for all target activities', 'Agent Ops: production SLOs enforced (acceptance ≥ 80%, p95 < 30s, zero silent failures)', 'Set override authority levels: Tech Lead can pause any agent; CISO for compliance agents'],
        tools:     ['All 21 agents operating as primary (not shadow) across all 7 PDLC phases', 'AI-native ALM fully adopted — AI sprint summaries, velocity predictions, risk flags on blocked items', 'Self-healing CI/CD live — ML failure prediction preventing 30–40% of failures'],
        devsecops: ['All 4 DevSecOps agents live in production: Secure-by-Design, Compliance-as-Code, MRM, Governance Controller', 'Zero manual CAB approvals for low-risk releases (AI Release Manager auto-approving ≥ 70%)', 'Audit evidence: automated for every release — compliance team in exception-only mode'],
        aiops:     ['AIOps platform live — all production alerts managed, L1 incidents auto-resolved', 'Telemetry Sentinel: production signals → Jira backlog automation live', 'Predictive scaling active — KEDA/AWS Predictive Scaling enabled'],
        measure:   ['Agent Ops dashboard live — all 21 agents tracked against SLOs daily', 'Deployment frequency tracked (target: daily vs weekly baseline)'],
      },
      {
        range: 'Week 16–18', name: 'Optimise & Report', color: 'teal',
        org:       ['Run AI Adoption Retrospective — identify 2 lowest-performing agents for tuning sprint', 'Assess Option C feasibility — present to leadership'],
        tools:     ['Tune 2 lowest-quality agents based on 6 weeks production output data', 'Prompt engineering review: update system prompts for agents below 85% acceptance'],
        devsecops: ['Compliance audit simulation: confirm evidence archive maps 100% to requirements', 'Security debt review: confirm zero High/Critical vulnerabilities merged in last 8 weeks'],
        aiops:     ['AIOps review: confirm alert volume < 20/day actionable (was 200/day)', 'Telemetry Sentinel: confirm ≥ 15% of sprint work originating from production signals'],
        measure:   ['Full VSM re-measurement vs baseline (target: -55% PT, -72% WT, +15 pts FE)', 'ROI calculation vs 3.8× target — include compliance automation savings ($150–300K)', 'Publish team case study — share with leadership, initiate Option C conversation'],
      },
    ]
  },
  'option-c': {
    duration: '20–26 weeks', humanModel: 'AI-First: Product Definer + Product Builder + 21 Autonomous Agents (⚙)',
    phases: [
      {
        range: 'Week 1–4', name: 'Design & Approval', color: 'blue',
        org:       ['Design 2-role operating model: Definer (outcome-setting) + Builder (agent supervision)', 'Write job descriptions, decision rights, escalation protocols for both roles', 'All-hands briefing: explain transformation, transition paths, reskilling support — no surprises', 'Prepare board briefing: operating model, investment, regulatory approach, workforce transition plan'],
        tools:     ['Design all 21 agent specifications: inputs, outputs, LLM prompts, retrieval sources, handoff triggers', 'Select orchestration tech: LangGraph StateGraph (recommended) + LangChain + Azure OpenAI', 'Design STUMP Platform infrastructure: Azure Container Apps, Service Bus, Cosmos DB, Key Vault', 'Design AI-native ADLC pipeline: every phase has AI quality gate, no human approval for low-risk deploys'],
        devsecops: ['Design Governance Agent Stack: Secure-by-Design + Compliance-as-Code + MRM + Governance Controller', 'Define MRM Agent risk parameters with MRO — drift thresholds, explainability floor, kill-switch criteria', 'Governance architecture signed off by CTO + CCO before any build begins'],
        aiops:     ['Design fully autonomous AIOps architecture — define Sev-1 escalation criteria (only Sev-1 to human)', 'Design AI Incident Commander: Sev-1 pre-diagnosis pack format, escalation flow, PIR generator'],
        measure:   ['Capture VSM baseline (feature + user story level) — locked as immutable benchmark', 'Board resolution: approve 2-role model, STUMP Platform, $3.5M budget, workforce transition plan'],
      },
      {
        range: 'Week 4–12', name: 'Platform & Agent Build', color: 'green',
        org:       ['Reskilling sprint: Product Definer candidate — 3-week outcome brief writing programme', 'Reskilling sprint: Product Builder candidate — 4-week STUMP platform operations + prompt engineering', 'Workforce transition mapping: every team member has a documented transition path by Week 8'],
        tools:     ['Month 2 (Wk 4–8): Build 8 core agents — DiscoveryAgent, FeatureGen, StoryGen, CodeGen, ReviewAgent, QA Orchestrator, DataGen, AI SAST', 'Month 2–3 (Wk 6–10): Build LangGraph StateGraph orchestration layer + Governance Controller + AI-native ALM', 'Month 3 (Wk 10–12): Build remaining agents — AI Release Manager, Deploy Agent, IncidentAgent, Telemetry Sentinel, AIOps stack', '⚙ All agents use STUMP platform-managed mode (not on-demand)', 'E2E integration test: submit outcome brief → agents deliver deployment-ready build in staging'],
        devsecops: ['Build Secure-by-Design Architect (⚙ autonomous): load CISO-approved 120+ rule OPA library', 'Build Compliance-as-Code Orchestrator (⚙): full GDPR, DORA, Basel III ruleset in OPA', 'Build MRM Agent (⚙): continuous drift monitoring, SHAP explainability, autonomous kill-switch', 'Wire all 4 governance agents into StateGraph — every deployment gate must pass all four', 'Compliance evidence pipeline: immutable Azure Blob archive on every deployment'],
        aiops:     ['Build AI Incident Commander: NLP classifier, auto-remediation playbooks, status page updater, PIR generator', 'Build STUMP AIOps stack: OpenTelemetry auto-instrumentation, Dynatrace integration, self-healing K8s operator', 'Build predictive scaling: ML model trained on 12 months traffic + US Bank calendar signals', 'Build customer intent detection: NLP signal clustering from support tickets, usage analytics, app ratings'],
        measure:   ['E2E staging simulation must pass before pilot approval: outcome brief → deployed feature', 'All 21 agents registered in Agent Ops registry with SLOs defined'],
      },
      {
        range: 'Week 10–14', name: 'Compliance Baseline', color: 'red',
        org:       ['CCO + CISO formal sign-off on: data scope, compliance architecture, governance controller design', 'Regulatory engagement: OCC/FDIC notification of autonomous AI deployment (initiate before go-live)', 'STUMP Platform security review by external assessor (penetration test + architecture review)'],
        tools:     ['MRM Agent: generate baseline explainability reports for ALL production models entering scope', 'Compliance-as-Code: validate full ruleset against last 3 months of commit history — fix all gaps', 'Secure-by-Design: IaC baseline approved by CISO — all new IaC auto-validated from this point'],
        devsecops: ['Compliance-as-Code: full GDPR, DORA, Basel III ruleset validated — switch to blocking mode', 'MRM Agent: all model risk parameters locked, kill-switch tested in staging (must fire in < 30 seconds)', 'Governance Controller: bypass detection tested — confirm no agent can execute without approval', 'Telemetry Sentinel: Business Risk Score thresholds calibrated with governance board'],
        aiops:     ['AI Incident Commander: run 5 incident simulations — validate Sev-1 escalation, Sev-2 auto-resolution', 'AIOps stack: 2-week baseline learning period in staging (do not change rules during this period)'],
        measure:   ['Compliance audit simulation: map every compliance artefact to regulatory requirement', 'Governance Controller: confirm 100% of agent transitions logged to immutable audit trail'],
      },
      {
        range: 'Week 14–20', name: 'Pilot (Mandatory)', color: 'amber',
        org:       ['Product Definer + Product Builder take ownership — operate in parallel with existing team', 'First 3 weeks: manual review of ALL agent outputs. Approve or reject. Rejection reason fed back to agent context', 'Role transition formally begins: team members move to confirmed transition paths', 'Agent Ops: Product Builder monitors quality scores daily — any agent below 80% triggers tuning sprint'],
        tools:     ['All 21 agents running in pilot mode: STUMP orchestrates full ADLC for new user stories', '⚙ Autonomous ADLC pipeline live: outcome brief → Code Generator → CI → Test → Deploy → Definer approval', 'AI-native ALM: STUMP auto-creates work items from FeatureGen output — no human Jira tickets', 'Customer intent detection active: weekly intelligence digest to Product Definer'],
        devsecops: ['All 4 governance agents (⚙): validated on every pilot deployment', 'MRM Agent: continuous monitoring of all production models during pilot — kill-switch on standby', 'Parallel manual security review for 6 weeks — only switch to agent-only after 3 clean independent audits', 'Compliance evidence: confirm automated evidence collection is complete for every pilot deployment'],
        aiops:     ['AI Incident Commander: Sev-2 and below handled autonomously during pilot — Product Builder reviews all actions', 'Self-healing infrastructure: predictive scaling active, auto-remediation playbooks validated on real incidents', 'Telemetry Sentinel: production signals → outcome brief hypothesis queue active'],
        measure:   ['Weekly acceptance rate tracking per agent — must reach 80%+ for 2 consecutive weeks to exit pilot', 'Compare pilot ADLC throughput vs legacy: user story lead time target < 1 day (non-regulated)', 'Validate: all 5 governance agents SOC2, GDPR, Basel III compliant'],
      },
      {
        range: 'Week 20–26', name: 'Full Transition', color: 'purple',
        org:       ['Remove manual oversight from all workflows with ≥ 80% sustained acceptance rate', 'Complete 2-role transition: Product Definer + Product Builder only', 'All workforce transitions executed: confirmed placements, reskilling completions, severance where applicable', 'Board update: transition complete, operating model live, compliance confirmed'],
        tools:     ['⚙ All 21 agents fully autonomous (platform-managed, not on-demand)', 'Agent auto-escalates if output confidence < 70% — Product Builder review triggered', 'Real-time customer intent detection feeding directly into Product Definer weekly outcome briefs', 'AI-native ALM only: Jira retained as read-only compliance mirror, no manual tickets'],
        devsecops: ['Autonomous DevSecOps fully live: zero manual approvals in security, compliance, or IaC pipeline', 'Security debt: confirmed eliminated (Secure-by-Design has blocked all violations since Week 10)', 'MRM Agent: all production models in continuous governance — SR 11-7 compliance documented and auditor-ready'],
        aiops:     ['Fully autonomous AIOps: zero L1/L2 human intervention (Sev-1 only to Product Builder)', 'Self-healing + self-scaling infrastructure: predictive scaling handling all known calendar events', 'AI Incident Commander: Sev-1 pre-diagnosis pack delivered < 2 min from detection'],
        measure:   ['Confirm all 21 agents within SLO 95%+ of the time', 'Deployment frequency: multiple per day confirmed (was weekly)'],
      },
      {
        range: 'Week 26–28', name: 'Stabilise & Scale', color: 'teal',
        org:       ['Document complete STUMP Platform operating playbook — prompts, orchestration routes, quality gates, tuning parameters', 'Scale-out plan: which team is next? Replication cost, timeline, playbook modifications needed', 'Brief leadership on replication roadmap — board approves next team onboarding'],
        tools:     ['Tune any agents below 85% acceptance based on 8 weeks production data', 'Publish agent configuration playbook for next team replication'],
        devsecops: ['External audit: confirm Compliance-as-Code evidence is audit-ready for SOC2, GDPR, Basel III', 'Publish STUMP Platform security architecture document for CISO/regulatory reference'],
        aiops:     ['AIOps review: confirm L1/L2 human intervention at zero, alert volume < 5/day actionable', 'Telemetry Sentinel: confirm ≥ 40% of outcome briefs originating from live customer signals'],
        measure:   ['Full VSM re-measurement vs baseline (target: -70% PT, -88% WT, +24 pts FE)', 'ROI calculation vs 5.5× target — include compliance automation savings ($300–600K) + security incident reduction', 'Publish internal case study with full metrics, timeline, lessons, agent architecture overview', 'Board presentation: ROI confirmed, scale-out plan approved'],
      },
    ]
  }
}
