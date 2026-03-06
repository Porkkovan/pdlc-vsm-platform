import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'

// ─── Business Case Data ──────────────────────────────────────────────────────
const BUSINESS_CASES = {
  'option-a': {
    investmentRange: '$800K – $1.5M', roiTimeline: '12–18 months', roiMultiple: '2.8×', paybackPeriod: '14 months',
    investment: {
      tools: '$250K–$400K (AI tools, IDE plugins, platform licenses)',
      infrastructure: '$100K–$200K (GPU compute, vector DBs, API costs)',
      implementation: '$300K–$600K (integration, prompt engineering, testing)',
      training: '$100K–$200K (upskilling all PDLC personas)',
      change: '$100K–$150K (org change management, communications)'
    },
    annualBenefits: {
      ttmImprovement: '$600K–$900K (faster feature delivery, competitive advantage)',
      productivityGains: '$400K–$600K (35% effort reduction across team)',
      qualityImprovement: '$200K–$300K (fewer defects, less rework)',
      operationalSavings: '$100K–$150K (automated testing, deployments)'
    },
    orgChanges: ['Upskill all PDLC personas in AI tool collaboration','Redefine roles to include AI supervision and prompt engineering','Establish AI Centre of Excellence (CoE) for governance','Update ways of working guides for human-AI collaboration','Introduce AI literacy training (mandatory for all roles)'],
    toolsChanges: ['Jira / ADO: Add AI-powered backlog management plugins','GitHub: Deploy Copilot Enterprise for all developers','Testing: Upgrade to AI-enhanced test frameworks','CI/CD: Integrate ML-based build optimizers and SAST tools','Monitoring: Deploy AI APM (Dynatrace Davis AI or Datadog AI)'],
    devSecOps: ['Shift-left security with AI-assisted SAST/DAST in every PR','AI-generated IaC templates with security policy validation','Automated compliance evidence collection for audit trails','AI-powered secret scanning and dependency vulnerability alerts'],
    aiOps: ['AI-driven anomaly detection and auto-remediation','Predictive scaling based on ML traffic patterns','Automated incident routing with NLP-based categorization','Continuous feedback loop: production insights → backlog prioritization'],
    productCentricChanges: ['Reorganize from project to persistent product teams','OKRs tied to product outcomes, not delivery velocity','Quarterly business review cadence with AI-generated insights','Customer feedback integrated into product roadmap via AI']
  },
  'option-b': {
    investmentRange: '$1.2M – $2.2M', roiTimeline: '10–15 months', roiMultiple: '3.8×', paybackPeriod: '11 months',
    investment: {
      tools: '$400K–$700K (selective AI platforms for key phases)',
      infrastructure: '$200K–$350K (dedicated AI compute, model hosting)',
      implementation: '$400K–$800K (deep integrations, custom agent development)',
      training: '$100K–$200K (focused training for remaining human roles)',
      change: '$150K–$200K (significant role restructuring support)'
    },
    annualBenefits: {
      ttmImprovement: '$900K–$1.4M (55% faster delivery)',
      productivityGains: '$600K–$900K (55% effort reduction)',
      qualityImprovement: '$300K–$500K (AI-driven quality gates)',
      operationalSavings: '$200K–$350K (automated ops and monitoring)'
    },
    orgChanges: ['Consolidate 8+ roles to 5 core roles (Product Owner, Tech Lead, Developer, QA Lead, DevOps)','Establish clear human-AI handoff protocols per phase','Create AI Agent Operations team to manage and tune agents','Redesign performance metrics to measure AI-human team output','Executive sponsorship program for transformation governance'],
    toolsChanges: ['Consolidate ALM tools to 1–2 AI-native platforms','Deploy custom LangChain/LangGraph agent orchestration layer','Replace manual test scripting with AI-generated test suites','Implement GitOps-native CI/CD with AI release gating','Unify observability into AI-powered single-pane-of-glass'],
    devSecOps: ['Zero-trust security model enforced by AI policy agents','AI-generated runbooks updated automatically after incidents','Continuous compliance validation with AI audit agents','ML-based threat modeling integrated into architecture reviews'],
    aiOps: ['Self-healing pipelines with AI-driven failure prediction','AIOps platform managing all production alerts and responses','Automated capacity planning using ML forecasting','AI-powered post-incident learning and backlog integration'],
    productCentricChanges: ['Product teams own full value stream from ideation to production','Eliminate hand-offs between dev, test, and ops teams','Continuous product discovery embedded in product team rituals','AI-generated product performance dashboards for stakeholders']
  },
  'option-c': {
    investmentRange: '$2.5M – $4.5M', roiTimeline: '18–24 months', roiMultiple: '5.5×', paybackPeriod: '19 months',
    investment: {
      tools: '$800K–$1.5M (comprehensive AI platform stack)',
      infrastructure: '$500K–$900K (enterprise AI compute, model fine-tuning)',
      implementation: '$800K–$1.5M (end-to-end agent development and orchestration)',
      training: '$200K–$300K (Product Definer + Product Builder intensive training)',
      change: '$300K–$500K (major org transformation support)'
    },
    annualBenefits: {
      ttmImprovement: '$1.8M–$2.8M (70% faster delivery, market leadership)',
      productivityGains: '$1.2M–$1.8M (70% effort reduction)',
      qualityImprovement: '$500K–$800K (AI quality gates, zero manual rework)',
      operationalSavings: '$400K–$700K (fully autonomous ops)'
    },
    orgChanges: ['Restructure entire PDLC workforce to 2 human roles only','Product Definer: sets vision, outcomes, and acceptance criteria','Product Builder: supervises agent orchestration and quality gates','Major workforce transition plan with reskilling/redeployment','New operating model approval at board level required','External change management firm engagement recommended'],
    toolsChanges: ['Custom AI-native product engineering platform (greenfield or heavily modified existing)','Multi-agent orchestration layer (LangGraph / AutoGen / custom)','AI-native ALM replacing traditional Jira/ADO','Fully automated CI/CD/CD with AI-driven decisions at every gate','Integrated AI product analytics replacing manual reporting'],
    devSecOps: ['Fully AI-managed DevSecOps pipeline from code to production','AI security agents continuously monitoring and auto-remediating','Autonomous compliance management with human oversight only for exceptions','AI-generated architecture decision records (ADRs) and security reviews'],
    aiOps: ['Fully autonomous AIOps — zero Level 1 / Level 2 human intervention','AI-driven capacity, performance, and cost optimization continuously','Self-healing, self-scaling, self-documenting production systems','AI incident commander with human escalation only for critical events'],
    productCentricChanges: ['Abolish traditional SDLC phases — continuous product evolution model','Product Definer sets weekly outcomes; agents execute autonomously','Real-time product performance feeding back to AI roadmap prioritization','Customer intent detection via AI — feature ideas generated proactively']
  }
}

// ─── Implementation Timelines (team-level) ───────────────────────────────────
const IMPLEMENTATION_TIMELINES = {
  'option-a': {
    teamDuration: '6–10 weeks',
    enterpriseDuration: '12–18 months',
    teamNote: 'SaaS AI tools go live in days; team training is 10–15 people; no cross-org procurement needed. Industry ref: GitHub Copilot deployed to 500 developers at Salesforce in 3 weeks.',
    phases: [
      { name: 'Foundation', range: 'Week 1', color: 'blue', milestones: ['Team kickoff — agree AI adoption goals and VSM success metrics','Run baseline VSM measurement (PT, WT, LT, FE) using this platform','Procure/enable GitHub Copilot Enterprise for all developers','Define AI output review checkpoints in Definition of Done'] },
      { name: 'Quick Wins', range: 'Week 2–3', color: 'green', milestones: ['Deploy ReviewAgent / Copilot for AI-augmented code review','Integrate ML-powered SAST (Semgrep / Snyk) into every PR pipeline','Enable AI backlog management plugin in Jira / ADO','Configure AI-generated BDD scenario suggestions for QA team'] },
      { name: 'Core Tools', range: 'Week 3–6', color: 'amber', milestones: ['Deploy AI performance test analyzer (target: 75% authoring time reduction)','Integrate AI APM platform (Dynatrace Davis AI or Datadog AI)','Configure AI-driven incident routing and auto-remediation rules','AI-generated IaC templates with security policy validation live'] },
      { name: 'Embed & Adopt', range: 'Week 6–8', color: 'purple', milestones: ['2-day AI collaboration workshop for all PDLC personas','Update sprint ceremonies: AI-assisted planning, AI retrospective data','Build team prompt engineering playbook with reusable templates','Update Definition of Done to include AI output review step'] },
      { name: 'Measure & Report', range: 'Week 8–10', color: 'teal', milestones: ['Re-run VSM measurement — compare to baseline (target: -35% PT, -55% WT)','Calculate actual ROI vs 2.8× target; present to stakeholders','Retrospective: identify which agents delivered most value','Assess readiness for Option B upgrade'] }
    ]
  },
  'option-b': {
    teamDuration: '12–16 weeks',
    enterpriseDuration: '10–15 months',
    teamNote: 'Custom LangGraph agents take 4–8 weeks to build and test. Role restructuring at team level = 1–2 sprints. Industry ref: Stripe deployed custom AI developer tooling in 8 weeks.',
    phases: [
      { name: 'Architecture', range: 'Week 1–2', color: 'blue', milestones: ['Design LangGraph agent orchestration architecture for 5 core agents','Define 5-role operating model and individual transition conversations','Select consolidated ALM (Jira AI / Linear / Shortcut) and configure','Establish AI Agent Operations responsibilities within the team'] },
      { name: 'Agent Build', range: 'Week 2–6', color: 'green', milestones: ['Sprint A: Build FeatureGen Agent + ReviewAgent — unit-tested and deployed in staging','Sprint B: Build AI UAT Assistant + DataGen Agent — integration-tested','Sprint C: Build AI Release Manager + ML-powered SAST integration','All agents pass quality gate: human review of 50 real outputs each'] },
      { name: 'Integration', range: 'Week 6–10', color: 'amber', milestones: ['Deploy agents in production alongside existing processes (2-week parallel run)','Define and document human-AI handoff protocols per PDLC phase','Begin role transition: team operates with 5 core roles from Sprint 7','AI Agent Ops: daily monitoring dashboard live for agent performance'] },
      { name: 'Full Deployment', range: 'Week 10–14', color: 'purple', milestones: ['Remove parallel processes — agents are primary for all target activities','AIOps platform live — managing all production alerts and triage','ALM consolidation complete — one platform for all work tracking','Self-healing CI/CD pipeline operational with AI failure prediction'] },
      { name: 'Optimise & Report', range: 'Week 14–16', color: 'teal', milestones: ['Full VSM re-measurement vs baseline (target: -55% PT, -72% WT)','Tune agent prompts based on 6 weeks of real production output quality','Calculate ROI vs 3.8× target; present to leadership','Publish team case study; assess Option C feasibility'] }
    ]
  },
  'option-c': {
    teamDuration: '20–26 weeks',
    enterpriseDuration: '18–24 months',
    teamNote: 'A 22-agent orchestration system is architecturally complex even for one team. Pilot phase is mandatory before the 2-role transition. Industry ref: Cognition AI built Devin-class agent systems in ~4 months.',
    phases: [
      { name: 'Design & Approval', range: 'Week 1–4', color: 'blue', milestones: ['Technical architecture for all 22 agents and orchestration layer','Operating model design: 2-role structure (Definer + Builder)','Team communication plan and workforce transition agreement','Technology stack selection: LangGraph / AutoGen / Agency Swarm'] },
      { name: 'Platform Build', range: 'Week 4–12', color: 'green', milestones: ['Month 2: Core agents live — coding, testing, review (8 agents)','Month 2–3: Orchestration layer + AI-native ALM replacement built','Month 3: AIOps agents + fully autonomous CI/CD pipeline deployed','All 22 agents integration-tested in staging with realistic workloads'] },
      { name: 'Pilot', range: 'Week 12–18', color: 'amber', milestones: ['2-person team (Definer + Builder) takes ownership — parallel with existing team','Human manual review of all agent outputs for first 3 weeks','Identify and fix agent failure modes; tune orchestration prompts','Security and compliance agents formally validated (SOC2, GDPR checks)'] },
      { name: 'Full Transition', range: 'Week 18–24', color: 'purple', milestones: ['Remove manual oversight from all validated agent workflows','Complete transition to 2-role operating model (team restructured)','All production support autonomous — zero L1/L2 human intervention','Real-time customer intent detection and proactive feature gen live'] },
      { name: 'Stabilise & Scale', range: 'Week 24–26', color: 'teal', milestones: ['VSM re-measurement vs baseline (target: -70% PT, -88% WT)','Calculate ROI vs 5.5× target; present board-level results','Document full playbook and agent configs for other teams to replicate','Publish internal case study; plan scale-out to next product team'] }
    ]
  }
}

// ─── Implementation Playbooks ─────────────────────────────────────────────────
const PLAYBOOKS = {
  'option-a': {
    label: 'Option A – Augmented Human',
    teamDuration: '6–10 weeks',
    teamSize: '8–15 people',
    effortEstimate: '~4 hrs/person/week during rollout',
    executiveSummary: 'This playbook guides your product team through deploying AI as a co-pilot across all PDLC activities. Every team member retains their role and decision authority — AI augments speed, quality, and insights. The team should expect measurable VSM improvement by Week 4 and full benefit realisation by Week 10.',
    targetMetrics: [
      { metric: 'Process Time (PT)', baseline: '100h (team total)', target: '65h', reduction: '35%', measure: 'Sprint velocity + time tracking' },
      { metric: 'Wait Time (WT)', baseline: '536h (team total)', target: '241h', reduction: '55%', measure: 'Jira/ADO cycle time reports' },
      { metric: 'Lead Time (LT)', baseline: '42 days', target: '24 days', reduction: '40%', measure: 'Story cycle time P50' },
      { metric: 'Flow Efficiency', baseline: '8%', target: '18%', reduction: '+10 pts', measure: 'VSM platform re-run' },
      { metric: 'Code review turnaround', baseline: '4–24 hrs', target: '1–2 hrs', reduction: '75%', measure: 'GitHub PR analytics' },
      { metric: 'Test authoring time', baseline: '16–40 hrs', target: '4–8 hrs', reduction: '75%', measure: 'QA team time log' }
    ],
    sprintPlan: [
      {
        sprint: 'Week 1', label: 'Foundation',
        actions: [
          { who: 'Tech Lead + Product Owner', what: 'Run baseline VSM measurement on this platform — capture current PT, WT, LT, FE as your benchmark' },
          { who: 'Tech Lead', what: 'Enable GitHub Copilot Enterprise for all developers — configure at org level in 2 hours; distribute licences' },
          { who: 'Scrum Master', what: 'Run 1-hour team kickoff: share VSM baseline, explain AI tool rollout plan, agree on success metrics and review cadence' },
          { who: 'DevOps Engineer', what: 'Audit current CI/CD pipeline — document all manual steps that will be automated in weeks 2–3' }
        ],
        outcomes: ['VSM baseline captured', 'GitHub Copilot enabled for all devs', 'Team aligned on goals and timeline']
      },
      {
        sprint: 'Week 2–3', label: 'Quick Wins',
        actions: [
          { who: 'Tech Lead + Developers', what: 'Configure ReviewAgent / GitHub Copilot code review. Add PR template asking team to note where AI flagged issues vs human. Run for 1 sprint before measuring.' },
          { who: 'DevOps Engineer', what: 'Integrate Semgrep or Snyk AI into CI pipeline. Set to "advisory" mode for week 1 to reduce friction. Switch to blocking-on-critical in week 2.' },
          { who: 'Product Owner', what: 'Enable Jira AI backlog health and AI story point suggestions. Share sample output with team before next sprint planning.' },
          { who: 'QA Lead', what: 'Configure ScenarioGen Agent or equivalent — generate BDD scenarios for 3 upcoming features and review quality with the team' }
        ],
        outcomes: ['Code review time reduced by first measurement', 'AI SAST catching issues before human review', 'AI backlog suggestions in use at planning']
      },
      {
        sprint: 'Week 3–6', label: 'Core AI Tool Deployment',
        actions: [
          { who: 'QA Engineer', what: 'Deploy AI performance test analyzer. Run it alongside current manual approach for 2 sprints to build confidence. Track hours saved.' },
          { who: 'DevOps Engineer', what: 'Integrate AI APM (Dynatrace Davis AI or Datadog AI). Configure anomaly detection baselines — allow 1 week of learning before enabling alerts.' },
          { who: 'DevOps Engineer', what: 'Configure AI-driven incident routing rules. Start with low-severity incidents only; escalate to all alerts in week 3 of this phase.' },
          { who: 'Tech Lead', what: 'Deploy AI-generated IaC templates with security policy validation. Validate 3 templates manually, then enable for routine infrastructure.' }
        ],
        outcomes: ['Automated performance testing live', 'AI monitoring baseline established', 'Incident routing partially automated']
      },
      {
        sprint: 'Week 6–8', label: 'Ways of Working Update',
        actions: [
          { who: 'Scrum Master', what: 'Run half-day AI collaboration workshop — demo all deployed tools; share prompt engineering basics; collect team feedback on friction points' },
          { who: 'Tech Lead + Scrum Master', what: 'Update Definition of Done: add "AI output reviewed" checkpoint for code, tests, and generated content' },
          { who: 'All team members', what: 'Each persona creates 3 reusable prompts for their top-3 daily tasks. Scrum Master curates into a shared team prompt library in Confluence/Notion.' },
          { who: 'Product Owner', what: 'Update OKRs to include flow efficiency and lead time targets. Make VSM metrics visible in team weekly dashboard.' }
        ],
        outcomes: ['Team prompt library created', 'Updated DoD with AI checkpoints', 'OKRs tied to VSM metrics']
      },
      {
        sprint: 'Week 8–10', label: 'Measure, Optimise & Report',
        actions: [
          { who: 'Product Owner + Tech Lead', what: 'Re-run VSM analysis on this platform. Compare to Week 1 baseline. Present delta to stakeholders.' },
          { who: 'Scrum Master', what: 'Run AI Adoption Retrospective: What worked? What had low adoption? What should we tune? Identify top 3 improvements for next cycle.' },
          { who: 'Tech Lead', what: 'Calculate ROI: (productivity hours saved × avg hourly rate) / tool cost. Target: 2.8× within 12 months annualised.' },
          { who: 'Product Owner', what: 'Document team case study — outcomes, lessons, recommended next steps. Share with leadership and other teams.' }
        ],
        outcomes: ['VSM improvement measured and documented', 'ROI calculated', 'Case study shared', 'Option B readiness assessed']
      }
    ],
    raci: [
      { activity: 'AI tool procurement & licensing', r: 'DevOps Engineer', a: 'Tech Lead', c: 'Product Owner', i: 'All team' },
      { activity: 'GitHub Copilot configuration', r: 'DevOps Engineer', a: 'Tech Lead', c: 'Developers', i: 'QA Lead' },
      { activity: 'CI/CD AI SAST integration', r: 'DevOps Engineer', a: 'Tech Lead', c: 'Developers', i: 'Product Owner' },
      { activity: 'AI backlog management setup', r: 'Product Owner', a: 'Scrum Master', c: 'Tech Lead', i: 'Developers' },
      { activity: 'AI test tool deployment', r: 'QA Engineer', a: 'QA Lead', c: 'Tech Lead', i: 'DevOps Engineer' },
      { activity: 'Prompt engineering playbook', r: 'Tech Lead', a: 'Scrum Master', c: 'All personas', i: 'Product Owner' },
      { activity: 'VSM baseline & re-measurement', r: 'Scrum Master', a: 'Product Owner', c: 'Tech Lead', i: 'All team' },
      { activity: 'AI APM configuration', r: 'DevOps Engineer', a: 'Tech Lead', c: 'QA Lead', i: 'Product Owner' }
    ],
    risks: [
      { risk: 'Low developer adoption of AI tools', severity: 'High', mitigation: 'Assign 1 AI champion per squad. Run Copilot for 1 sprint with daily 15-min sharing session. Leader models usage visibly.' },
      { risk: 'AI SAST false positives slow PRs', severity: 'Medium', mitigation: 'Run in advisory mode (informational only) for first week. Suppress low-severity findings. Review false positive rate weekly.' },
      { risk: 'Inconsistent prompt quality across team', severity: 'Medium', mitigation: 'Build shared prompt library by Week 6. Weekly prompt-sharing session in retrospective. CoE-curated templates as starting points.' },
      { risk: 'No baseline captured before changes begin', severity: 'High', mitigation: 'Day 1 action: run VSM baseline on this platform BEFORE deploying any tool. No baseline = no ROI evidence.' }
    ]
  },
  'option-b': {
    label: 'Option B – Hybrid',
    teamDuration: '12–16 weeks',
    teamSize: '5 core roles (post-transition)',
    effortEstimate: '~20 hrs/week agent build capacity required (Weeks 2–6)',
    executiveSummary: 'This playbook guides your team through building and deploying a custom AI agent orchestration layer across the highest-impact PDLC phases, while restructuring to 5 core human roles. Agent development runs in sprints; role transition is gradual and parallel-run before cutover. Expect measurable improvement by Week 10, full benefit by Week 16.',
    targetMetrics: [
      { metric: 'Process Time (PT)', baseline: '100h', target: '45h', reduction: '55%', measure: 'Sprint velocity + agent logs' },
      { metric: 'Wait Time (WT)', baseline: '536h', target: '150h', reduction: '72%', measure: 'Jira cycle time + agent telemetry' },
      { metric: 'Lead Time (LT)', baseline: '42 days', target: '19 days', reduction: '55%', measure: 'Story cycle time P50' },
      { metric: 'Flow Efficiency', baseline: '8%', target: '23%', reduction: '+15 pts', measure: 'VSM platform re-run' },
      { metric: 'Manual signoff gates', baseline: '3 gates (3–7 day waits)', target: '0 manual gates', reduction: '100%', measure: 'Release pipeline audit' },
      { metric: 'Deployment frequency', baseline: 'Weekly', target: 'Daily', reduction: '7×', measure: 'DORA metrics dashboard' }
    ],
    sprintPlan: [
      {
        sprint: 'Week 1–2', label: 'Architecture & Design',
        actions: [
          { who: 'Tech Lead', what: 'Design LangGraph StateGraph architecture for 5 core agents. Define agent inputs, outputs, state schema, and handoff triggers. Document in ADR.' },
          { who: 'Tech Lead + Product Owner', what: 'Define new 5-role operating model. Have 1-to-1 conversations with team members about their future role. No surprises.' },
          { who: 'DevOps Engineer', what: 'Select and configure consolidated ALM platform (Jira AI, Linear, or Shortcut). Migrate backlog in week 2. Decommission old tools.' },
          { who: 'Scrum Master', what: 'Establish AI Agent Operations rituals: daily 15-min agent health check, weekly agent performance review, agent incident runbook.' }
        ],
        outcomes: ['Agent architecture documented', 'Role transition plan communicated', 'ALM consolidation started']
      },
      {
        sprint: 'Week 2–6', label: 'Agent Build Sprints',
        actions: [
          { who: 'Tech Lead + Developer', what: 'Sprint A (Wk 2–3): Build FeatureGen Agent (feature → stories → ACs) and ReviewAgent (PR diff → structured review). Both deployed in staging.' },
          { who: 'QA Lead + Developer', what: 'Sprint B (Wk 3–4): Build AI UAT Assistant (consolidate test results → risk-scored readiness report) and DataGen Agent (schema → synthetic PII-safe data).' },
          { who: 'DevOps Engineer + Developer', what: 'Sprint C (Wk 4–6): Build AI Release Manager (auto-validate quality/security/performance gates) and ML-powered SAST integration. Deploy in staging.' },
          { who: 'All', what: 'Quality gate for every agent: each agent must produce acceptable output on 50 real work items before promotion to production.' }
        ],
        outcomes: ['5 core agents built and staging-validated', 'Each agent reviewed on 50 real items', 'Ready for production integration']
      },
      {
        sprint: 'Week 6–10', label: 'Integration & Parallel Run',
        actions: [
          { who: 'DevOps Engineer', what: 'Deploy all 5 agents to production in shadow mode — agents run alongside humans but humans still make final decisions. Compare agent vs human output for 2 weeks.' },
          { who: 'Tech Lead', what: 'Document human-AI handoff protocol for each PDLC phase: when agents own the action, when humans review, escalation criteria, rollback steps.' },
          { who: 'Scrum Master', what: 'Team transitions to 5 core roles from Sprint 7. Each new role gets a 1-day onboarding on their AI tools and the agent output they now own.' },
          { who: 'All', what: 'Agent Ops team monitors agent performance daily. Any agent output quality below 80% acceptance rate triggers immediate tuning sprint.' }
        ],
        outcomes: ['Shadow mode 2-week run complete', 'Human-AI handoff protocols documented', 'Team operating in 5-role model']
      },
      {
        sprint: 'Week 10–14', label: 'Full Deployment',
        actions: [
          { who: 'DevOps Engineer', what: 'Remove shadow mode — agents are primary for all target activities. Set up agent performance SLOs (response time, output quality score, error rate).' },
          { who: 'DevOps Engineer', what: 'AIOps platform live: all production alerts routed through AIOps triage. L1 incidents auto-resolved. L2 routed to DevOps with suggested fix.' },
          { who: 'Product Owner', what: 'AI-native ALM fully adopted — AI-generated sprint summaries, AI velocity predictions, AI risk flags on blocked items.' },
          { who: 'Tech Lead', what: 'Self-healing CI/CD live: ML-based build failure prediction prevents 30–40% of failures before they occur.' }
        ],
        outcomes: ['All 5 agents operating as primary (not shadow)', 'AIOps live', 'Self-healing CI/CD deployed']
      },
      {
        sprint: 'Week 14–16', label: 'Measure, Tune & Report',
        actions: [
          { who: 'Product Owner + Scrum Master', what: 'Re-run full VSM analysis. Compare to Week 1 baseline. Present: PT, WT, LT, FE deltas vs targets.' },
          { who: 'Tech Lead', what: 'Agent performance review: identify the 2 lowest-performing agents by output quality. Run 1-week tuning sprint on their prompts and retrieval context.' },
          { who: 'Product Owner', what: 'Calculate ROI: (PT + WT reduction hours × rate) + quality improvement savings / investment. Target 3.8× in 12 months annualised.' },
          { who: 'Scrum Master', what: 'Write and publish team case study. Present to leadership. Initiate Option C feasibility conversation.' }
        ],
        outcomes: ['VSM improvement measured', 'ROI calculated (target 3.8×)', 'Agents optimised', 'Case study published']
      }
    ],
    raci: [
      { activity: 'Agent architecture design', r: 'Tech Lead', a: 'Tech Lead', c: 'Developer + DevOps', i: 'Product Owner' },
      { activity: 'FeatureGen + ReviewAgent build', r: 'Developer', a: 'Tech Lead', c: 'Product Owner', i: 'QA Lead' },
      { activity: 'UAT Assistant + DataGen build', r: 'Developer', a: 'QA Lead', c: 'Tech Lead', i: 'DevOps Engineer' },
      { activity: 'AI Release Manager build', r: 'DevOps Engineer', a: 'Tech Lead', c: 'QA Lead', i: 'Product Owner' },
      { activity: 'Role transition conversations', r: 'Tech Lead', a: 'Product Owner', c: 'Scrum Master', i: 'All team' },
      { activity: 'Agent shadow-mode deployment', r: 'DevOps Engineer', a: 'Tech Lead', c: 'All team', i: 'Product Owner' },
      { activity: 'AIOps platform configuration', r: 'DevOps Engineer', a: 'Tech Lead', c: 'QA Lead', i: 'Product Owner' },
      { activity: 'VSM measurement & ROI report', r: 'Scrum Master', a: 'Product Owner', c: 'Tech Lead', i: 'All team' }
    ],
    risks: [
      { risk: 'Agent build takes longer than 4 sprints', severity: 'High', mitigation: 'Timebox each agent to 1 sprint. If not done, deploy partial agent with human fallback. Scope MVP — minimum viable agent first, enhancements later.' },
      { risk: 'Team resistance to role restructuring', severity: 'High', mitigation: '1-to-1 conversations before announcement. Involve team in designing the new roles. Show how new roles are higher-value, not downgraded.' },
      { risk: 'Agent output quality too low for production', severity: 'Medium', mitigation: 'Enforce 50-item quality gate. Require 80% acceptance rate before promotion. Keep human fallback in place for 2 weeks post-promotion.' },
      { risk: 'AIOps false positive alert storm', severity: 'Medium', mitigation: 'Run AIOps in advisory mode for 1 week. Tune alert thresholds. Suppress noisy signals before switching to full routing.' }
    ]
  },
  'option-c': {
    label: 'Option C – AI-First',
    teamDuration: '20–26 weeks',
    teamSize: '2 human roles (Product Definer + Product Builder)',
    effortEstimate: '~40 hrs/week engineering capacity for agent build (Weeks 4–12)',
    executiveSummary: 'This playbook guides your team through the most ambitious transformation — deploying 22 AI agents across all PDLC phases and transitioning to a 2-role operating model. It is structured as: Design, Build, Pilot (mandatory), Full Transition, Stabilise. The pilot phase is non-negotiable — no team should go to 2 roles without 6 weeks of validated agent performance.',
    targetMetrics: [
      { metric: 'Process Time (PT)', baseline: '100h', target: '30h', reduction: '70%', measure: 'Agent telemetry + audit logs' },
      { metric: 'Wait Time (WT)', baseline: '536h', target: '64h', reduction: '88%', measure: 'Agent orchestration logs' },
      { metric: 'Lead Time (LT)', baseline: '42 days', target: '13 days', reduction: '70%', measure: 'End-to-end cycle time' },
      { metric: 'Flow Efficiency', baseline: '8%', target: '32%', reduction: '+24 pts', measure: 'VSM platform re-run' },
      { metric: 'Deployment frequency', baseline: 'Weekly', target: 'Multiple per day', reduction: '7×+', measure: 'DORA deployment frequency' },
      { metric: 'Human roles required', baseline: '8+', target: '2', reduction: '75%', measure: 'Org chart' }
    ],
    sprintPlan: [
      {
        sprint: 'Week 1–4', label: 'Design & Architecture',
        actions: [
          { who: 'Tech Lead (Product Builder)', what: 'Design all 22 agent specifications: inputs, outputs, LLM prompts, retrieval sources, handoff triggers, error handling. Document as agent ADRs.' },
          { who: 'Product Owner (Product Definer)', what: 'Design 2-role operating model: write job descriptions, decision rights framework, escalation protocol, and outcome-setting cadence for Product Definer.' },
          { who: 'Tech Lead', what: 'Select orchestration technology: LangGraph StateGraph (recommended), AutoGen, or Agency Swarm. Deploy dev environment with shared state store.' },
          { who: 'Tech Lead + DevOps', what: 'Design AI-native CI/CD architecture: every stage has an AI quality gate. No human approval required for deployments below risk threshold.' }
        ],
        outcomes: ['All 22 agent specs documented', '2-role model designed and shared', 'Tech stack selected and dev environment live']
      },
      {
        sprint: 'Week 4–12', label: 'Platform & Agent Build',
        actions: [
          { who: 'Developer + Tech Lead', what: 'Month 2 (Wk 4–8): Build 8 core agents — FeatureGen, StoryGen, CodeGen, ReviewAgent, ScenarioGen, DataGen, AI SAST, AI DAST. Deploy to staging sequentially.' },
          { who: 'Developer + DevOps', what: 'Month 2–3 (Wk 6–10): Build orchestration layer (StateGraph router), AI-native ALM, and automated CI/CD pipeline with AI quality gates at every stage.' },
          { who: 'DevOps + Developer', what: 'Month 3 (Wk 10–12): Build remaining 14 agents — AI Release Manager, IncidentAgent, AIOps agents, AI APM, DesignGen, AI Architecture Advisor, and monitoring agents.' },
          { who: 'QA (transitioning)', what: 'Integration-test all 22 agents together in staging. Run end-to-end simulation: input a feature brief → agent orchestration delivers deployment-ready build.' }
        ],
        outcomes: ['All 22 agents built and integration-tested', 'AI-native ALM live in staging', 'Full pipeline E2E simulation passing']
      },
      {
        sprint: 'Week 12–18', label: 'Pilot (Mandatory)',
        actions: [
          { who: 'Product Definer', what: 'Take ownership of outcome-setting. Write weekly goal brief (problem to solve, constraints, acceptance criteria). No more detailed backlog writing — agents decompose from the brief.' },
          { who: 'Product Builder', what: 'Monitor agent orchestration daily: review agent output quality scores, intervene on exceptions, tune prompts when quality drops below threshold.' },
          { who: 'Both + DevOps (temporarily)', what: 'Manual review of ALL agent outputs for first 3 weeks. Approve or reject. Rejection reason fed back into agent context. Only move to auto-approve after 80%+ acceptance rate for 2 consecutive weeks.' },
          { who: 'Tech Lead (Product Builder)', what: 'Validate security and compliance agents: run against OWASP top 10, GDPR data handling, and SOC2 evidence collection requirements. Fix all gaps.' }
        ],
        outcomes: ['2-role model piloted for 6 weeks', '22 agents operating with ≥80% acceptance rate', 'Security and compliance validation complete']
      },
      {
        sprint: 'Week 18–24', label: 'Full Transition',
        actions: [
          { who: 'Product Builder', what: 'Remove manual approval from all workflows with ≥80% historical acceptance rate. Set exception thresholds — agent auto-escalates if output confidence < 70%.' },
          { who: 'Product Definer', what: 'AIOps fully autonomous: set escalation rule (Sev-1 only to human). All other production events handled by IncidentAgent with auto-remediation playbooks.' },
          { who: 'Product Definer', what: 'Real-time customer intent detection live: NLP analysis of support tickets, usage analytics, and market signals feeds directly into Product Definer weekly outcome briefs.' },
          { who: 'Product Builder', what: 'All workforce transition complete. Former team members in new roles or redeployed. Document all agent configs and operating procedures for continuity.' }
        ],
        outcomes: ['Full 2-role operating model live', 'All 22 agents autonomous (non-Sev-1)', 'Customer intent feeding roadmap', 'Team transition complete']
      },
      {
        sprint: 'Week 24–26', label: 'Stabilise & Scale',
        actions: [
          { who: 'Product Definer', what: 'Re-run VSM analysis. Compare to baseline. Present results: target -70% PT, -88% WT, +24 pts FE. Calculate ROI vs 5.5× target.' },
          { who: 'Product Builder', what: 'Document complete agent configuration playbook — prompts, orchestration routes, quality gates, tuning parameters. Prep for replication to next team.' },
          { who: 'Both', what: 'Publish internal case study with full metrics, timeline, lessons learned, and agent architecture overview.' },
          { who: 'Product Definer', what: 'Brief leadership on scale-out plan: which team is next? What modifications does the playbook need? What is the replication cost and time?' }
        ],
        outcomes: ['VSM improvement confirmed (target: -70% PT, -88% WT)', 'ROI calculated (target 5.5×)', 'Scale-out plan approved']
      }
    ],
    raci: [
      { activity: '22-agent architecture design', r: 'Product Builder', a: 'Product Builder', c: 'DevOps Engineer', i: 'Product Definer' },
      { activity: 'Core 8 agents build (Wk 4–8)', r: 'Developer→Product Builder', a: 'Product Builder', c: 'DevOps Engineer', i: 'Product Definer' },
      { activity: 'Orchestration layer build', r: 'DevOps Engineer', a: 'Product Builder', c: 'Developer', i: 'Product Definer' },
      { activity: 'AI-native ALM configuration', r: 'Product Builder', a: 'Product Builder', c: 'Product Definer', i: 'All' },
      { activity: 'Pilot outcome-setting briefs', r: 'Product Definer', a: 'Product Definer', c: 'Product Builder', i: 'Stakeholders' },
      { activity: 'Agent output quality review', r: 'Product Builder', a: 'Product Builder', c: 'Product Definer', i: 'Stakeholders' },
      { activity: 'Security & compliance validation', r: 'Product Builder', a: 'Product Builder', c: 'Security team', i: 'Product Definer' },
      { activity: 'Workforce transition', r: 'Product Definer', a: 'Product Definer', c: 'HR + Product Builder', i: 'All affected' }
    ],
    risks: [
      { risk: 'Agent orchestration instability in pilot', severity: 'Critical', mitigation: 'Mandatory 3-week manual-review period before any auto-approve. Rollback plan to Option B at any stage. Never remove human fallback before 80%+ acceptance rate sustained for 2 weeks.' },
      { risk: 'Team resistance to 2-role restructuring', severity: 'Critical', mitigation: 'Involve team in pilot phase. Give former team members first opportunity to become Product Builder. Provide reskilling time and budget. No surprise transitions.' },
      { risk: 'Agent quality degrades with novel inputs', severity: 'High', mitigation: 'Product Builder monitors quality scores daily. Set up automated regression test suite against 100 historical work items. Trigger re-tuning sprint if quality drops >10%.' },
      { risk: 'Security/compliance agents miss real vulnerabilities', severity: 'High', mitigation: 'Run parallel manual security review for 6 weeks during pilot. Only switch to agent-only after zero gap found in 3 consecutive independent audits.' }
    ]
  }
}

// ─── Implementation Timelines ─────────────────────────────────────────────────
const TIMELINE_COLORS = {
  blue:   { bg: 'bg-blue-100',   border: 'border-blue-300',   badge: 'bg-blue-600',   text: 'text-blue-800' },
  green:  { bg: 'bg-green-100',  border: 'border-green-300',  badge: 'bg-green-600',  text: 'text-green-800' },
  amber:  { bg: 'bg-amber-100',  border: 'border-amber-300',  badge: 'bg-amber-500',  text: 'text-amber-800' },
  purple: { bg: 'bg-purple-100', border: 'border-purple-300', badge: 'bg-purple-600', text: 'text-purple-800' },
  teal:   { bg: 'bg-teal-100',   border: 'border-teal-300',   badge: 'bg-teal-600',   text: 'text-teal-800' }
}

const SECTIONS = [
  { id: 'overview',  label: 'Overview' },
  { id: 'playbook',  label: 'Playbook' },
  { id: 'timeline',  label: 'Timeline' },
  { id: 'investment',label: 'Investment' },
  { id: 'benefits',  label: 'Benefits' },
  { id: 'org',       label: 'Org Change' },
  { id: 'tools',     label: 'Tools' },
  { id: 'devsecops', label: 'DevSecOps' },
  { id: 'aiops',     label: 'AI Ops' },
  { id: 'product',   label: 'Product-Centric' }
]

// ─── Component ────────────────────────────────────────────────────────────────
export default function BusinessCasePage() {
  const { activeScenario, setActiveScenario, addNotification, project } = useApp()
  const [running, setRunning]   = useState(false)
  const [activeSection, setSection] = useState('overview')
  const [openSprint, setOpenSprint] = useState(null)

  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const bc = BUSINESS_CASES[activeScenario]
  const tl = IMPLEMENTATION_TIMELINES[activeScenario]
  const pb = PLAYBOOKS[activeScenario]

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runBusinessCaseBuilder(project.id || 'demo', activeScenario)
      addNotification('Business case generated!', 'success')
    } catch { addNotification('Using built-in business case (demo mode)', 'info') }
    finally { setRunning(false) }
  }

  const SEVERITY_COLOR = { Critical: 'red', High: 'orange', Medium: 'amber' }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-600 to-orange-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Business Case & Implementation Playbook</h2>
            <p className="text-amber-100">Investment, ROI, implementation guide, timeline, org change, tools, DevSecOps, and AIOps requirements</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-amber-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-amber-50 shadow">
            {running ? '⏳ Building...' : '🤖 Run Business Case Agent'}
          </button>
        </div>
      </div>

      {/* Scenario selector */}
      <div className="grid grid-cols-3 gap-4">
        {FUTURE_STATE_SCENARIOS.map(s => {
          const sbc = BUSINESS_CASES[s.id]
          const stl = IMPLEMENTATION_TIMELINES[s.id]
          return (
            <button key={s.id} onClick={() => setActiveScenario(s.id)}
              className={`p-4 rounded-xl text-left border-2 transition-all ${activeScenario === s.id ? 'border-amber-500 bg-amber-50 shadow-md' : 'border-gray-200 bg-white hover:border-gray-400'}`}>
              <div className="font-bold text-gray-800 mb-1">{s.label}: {s.title.split('—')[0].trim()}</div>
              <div className="text-xs text-gray-500 mb-2">{s.subtitle}</div>
              <div className="text-xs space-y-1">
                <div><span className="text-gray-500">Investment: </span><span className="font-bold text-amber-700">{sbc.investmentRange}</span></div>
                <div><span className="text-gray-500">ROI: </span><span className="font-bold text-green-700">{sbc.roiMultiple} in {sbc.roiTimeline}</span></div>
                <div><span className="text-gray-500">Team timeline: </span><span className="font-bold text-blue-700">{stl.teamDuration}</span></div>
              </div>
            </button>
          )
        })}
      </div>

      {/* Section nav */}
      <div className="flex gap-2 overflow-x-auto bg-white p-3 rounded-xl border border-gray-200">
        {SECTIONS.map(s => (
          <button key={s.id} onClick={() => setSection(s.id)}
            className={`px-4 py-1.5 rounded-lg text-sm font-semibold whitespace-nowrap ${activeSection === s.id ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {s.id === 'playbook' ? '📋 ' : s.id === 'timeline' ? '📅 ' : ''}{s.label}
          </button>
        ))}
      </div>

      {/* ── Overview ── */}
      {activeSection === 'overview' && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Investment',    value: bc.investmentRange, color: 'amber', icon: '💰' },
            { label: 'ROI Multiple',  value: bc.roiMultiple,     color: 'green', icon: '📈' },
            { label: 'ROI Timeline',  value: bc.roiTimeline,     color: 'blue',  icon: '📅' },
            { label: 'Payback Period',value: bc.paybackPeriod,   color: 'purple',icon: '⏳' }
          ].map(m => (
            <div key={m.label} className="card card-body text-center">
              <div className="text-2xl mb-1">{m.icon}</div>
              <div className={`text-lg font-bold text-${m.color}-700`}>{m.value}</div>
              <div className="text-xs text-gray-500">{m.label}</div>
            </div>
          ))}
        </div>
      )}

      {/* ── Playbook ── */}
      {activeSection === 'playbook' && (
        <div className="space-y-6">
          {/* Playbook header */}
          <div className="bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200 rounded-2xl p-6">
            <div className="flex items-start gap-4">
              <div className="text-4xl">📋</div>
              <div className="flex-1">
                <h3 className="font-bold text-indigo-900 text-xl mb-1">Implementation Playbook — {pb.label}</h3>
                <p className="text-indigo-700 text-sm mb-4">{pb.executiveSummary}</p>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-white/80 rounded-lg p-3 border border-indigo-100">
                    <div className="text-xs text-gray-500 mb-0.5">Team Timeline</div>
                    <div className="font-bold text-indigo-700">{pb.teamDuration}</div>
                  </div>
                  <div className="bg-white/80 rounded-lg p-3 border border-indigo-100">
                    <div className="text-xs text-gray-500 mb-0.5">Team Composition</div>
                    <div className="font-bold text-indigo-700">{pb.teamSize}</div>
                  </div>
                  <div className="bg-white/80 rounded-lg p-3 border border-indigo-100">
                    <div className="text-xs text-gray-500 mb-0.5">Effort Required</div>
                    <div className="font-bold text-indigo-700">{pb.effortEstimate}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Target VSM Metrics */}
          <div className="card">
            <div className="card-header"><h3 className="font-bold text-gray-800">Target VSM Metrics — Success Criteria</h3></div>
            <div className="card-body">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-2 pr-4 text-xs font-semibold text-gray-600">Metric</th>
                      <th className="text-center py-2 px-3 text-xs font-semibold text-gray-600">Baseline</th>
                      <th className="text-center py-2 px-3 text-xs font-semibold text-gray-600">Target</th>
                      <th className="text-center py-2 px-3 text-xs font-semibold text-gray-600">Reduction</th>
                      <th className="text-left py-2 pl-3 text-xs font-semibold text-gray-600">How to Measure</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pb.targetMetrics.map((m, i) => (
                      <tr key={i} className={`border-b border-gray-100 ${i % 2 === 0 ? 'bg-gray-50' : ''}`}>
                        <td className="py-2.5 pr-4 font-semibold text-gray-800">{m.metric}</td>
                        <td className="py-2.5 px-3 text-center text-gray-600">{m.baseline}</td>
                        <td className="py-2.5 px-3 text-center font-bold text-green-700">{m.target}</td>
                        <td className="py-2.5 px-3 text-center"><span className="bg-green-100 text-green-800 px-2 py-0.5 rounded font-bold text-xs">{m.reduction}</span></td>
                        <td className="py-2.5 pl-3 text-gray-600 text-xs">{m.measure}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Sprint Plan */}
          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">Sprint-by-Sprint Implementation Plan</h3>
              <p className="text-xs text-gray-500">Expand each sprint to see specific actions, owners, and expected outcomes</p>
            </div>
            <div className="card-body space-y-3">
              {pb.sprintPlan.map((sp, idx) => {
                const isOpen = openSprint === idx
                return (
                  <div key={idx} className="border border-gray-200 rounded-xl overflow-hidden">
                    <button onClick={() => setOpenSprint(isOpen ? null : idx)}
                      className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50 text-left">
                      <div className="w-8 h-8 bg-indigo-600 text-white rounded-lg flex items-center justify-center font-bold text-sm shrink-0">{idx + 1}</div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-800">{sp.sprint} — {sp.label}</div>
                        <div className="text-xs text-gray-500">{sp.actions.length} actions · click to expand</div>
                      </div>
                      <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                    </button>
                    {isOpen && (
                      <div className="border-t border-gray-100 px-5 pb-5 slide-down">
                        <div className="mt-4 space-y-2.5">
                          {sp.actions.map((a, ai) => (
                            <div key={ai} className="bg-indigo-50 border border-indigo-200 rounded-lg p-3 text-sm">
                              <div className="flex items-start gap-3">
                                <span className="bg-indigo-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5">{ai + 1}</span>
                                <div className="flex-1">
                                  <div className="font-semibold text-indigo-900 text-xs mb-1">{a.who}</div>
                                  <div className="text-gray-700">{a.what}</div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                          <div className="text-xs font-semibold text-green-800 mb-1">Sprint Outcomes:</div>
                          <ul className="space-y-1">
                            {sp.outcomes.map((o, oi) => (
                              <li key={oi} className="flex items-center gap-2 text-xs text-green-700">
                                <span className="text-green-500">✓</span> {o}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          {/* RACI */}
          <div className="card">
            <div className="card-header"><h3 className="font-bold text-gray-800">Roles & Responsibilities (RACI)</h3></div>
            <div className="card-body overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b-2 border-gray-200">
                    <th className="text-left py-2 pr-4 font-semibold text-gray-700">Activity</th>
                    <th className="text-center py-2 px-2 font-semibold text-blue-700">Responsible (R)</th>
                    <th className="text-center py-2 px-2 font-semibold text-purple-700">Accountable (A)</th>
                    <th className="text-center py-2 px-2 font-semibold text-amber-700">Consulted (C)</th>
                    <th className="text-center py-2 px-2 font-semibold text-gray-500">Informed (I)</th>
                  </tr>
                </thead>
                <tbody>
                  {pb.raci.map((row, i) => (
                    <tr key={i} className={`border-b border-gray-100 ${i % 2 === 0 ? 'bg-gray-50' : ''}`}>
                      <td className="py-2.5 pr-4 font-medium text-gray-800">{row.activity}</td>
                      <td className="py-2.5 px-2 text-center text-blue-700 font-semibold">{row.r}</td>
                      <td className="py-2.5 px-2 text-center text-purple-700 font-semibold">{row.a}</td>
                      <td className="py-2.5 px-2 text-center text-amber-700">{row.c}</td>
                      <td className="py-2.5 px-2 text-center text-gray-500">{row.i}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Risk Register */}
          <div className="card">
            <div className="card-header"><h3 className="font-bold text-gray-800">Risk Register & Mitigations</h3></div>
            <div className="card-body space-y-3">
              {pb.risks.map((r, i) => {
                const col = SEVERITY_COLOR[r.severity] || 'gray'
                return (
                  <div key={i} className={`rounded-xl border p-4 bg-${col}-50 border-${col}-200`}>
                    <div className="flex items-start gap-3">
                      <span className={`bg-${col}-600 text-white text-xs font-bold px-2 py-0.5 rounded-full shrink-0 mt-0.5`}>{r.severity}</span>
                      <div className="flex-1">
                        <div className={`font-bold text-${col}-800 text-sm mb-1.5`}>{r.risk}</div>
                        <div className="text-sm text-gray-700">
                          <span className="font-semibold text-gray-600">Mitigation: </span>{r.mitigation}
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {/* ── Timeline ── */}
      {activeSection === 'timeline' && (
        <div className="space-y-4">
          {/* Team vs enterprise context */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
              <div className="font-bold text-blue-800 mb-1">Team-Level Timeline: {tl.teamDuration}</div>
              <div className="text-xs text-blue-700">{tl.teamNote}</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
              <div className="font-bold text-gray-700 mb-1">Enterprise / Programme Timeline: {tl.enterpriseDuration}</div>
              <div className="text-xs text-gray-600">Applies when rolling out across multiple teams with centralised procurement, governance, and change management at scale.</div>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h3 className="font-bold text-gray-800">📅 Implementation Timeline — {scenario?.label}</h3>
              <p className="text-xs text-gray-500">Team-level · {tl.teamDuration} · {tl.phases.length} phases</p>
            </div>
            <div className="card-body">
              <div className="flex gap-1 mb-6 rounded-full overflow-hidden h-3">
                {tl.phases.map((p, i) => <div key={i} className={`flex-1 ${TIMELINE_COLORS[p.color].badge} opacity-80`} title={`${p.name}: ${p.range}`} />)}
              </div>
              <div className="space-y-4">
                {tl.phases.map((phase, idx) => {
                  const c = TIMELINE_COLORS[phase.color]
                  return (
                    <div key={idx} className={`rounded-xl border-2 ${c.border} ${c.bg} overflow-hidden`}>
                      <div className="flex items-center gap-4 px-5 py-3">
                        <div className={`${c.badge} text-white text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap`}>{phase.range}</div>
                        <div className={`font-bold text-base ${c.text}`}>Phase {idx + 1}: {phase.name}</div>
                      </div>
                      <div className="px-5 pb-4 grid grid-cols-1 md:grid-cols-2 gap-2">
                        {phase.milestones.map((m, mi) => (
                          <div key={mi} className="flex items-start gap-2.5 bg-white/70 rounded-lg px-3 py-2.5 border border-white/50">
                            <span className={`${c.badge} text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5`}>{mi + 1}</span>
                            <span className="text-sm text-gray-700">{m}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Investment ── */}
      {activeSection === 'investment' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">💰 Investment Breakdown — {scenario?.label}</h3></div>
          <div className="card-body space-y-3">
            {Object.entries(bc.investment).map(([key, val]) => (
              <div key={key} className="flex items-start gap-4 p-4 bg-amber-50 rounded-lg border border-amber-200">
                <div className="w-32 shrink-0 text-xs font-bold text-amber-800 capitalize">{key}</div>
                <div className="text-sm text-gray-700">{val}</div>
              </div>
            ))}
            <div className="p-4 bg-amber-100 rounded-lg border border-amber-300 text-center">
              <div className="text-xl font-bold text-amber-800">Total: {bc.investmentRange}</div>
              <div className="text-xs text-amber-700 mt-1">One-time implementation investment</div>
            </div>
          </div>
        </div>
      )}

      {/* ── Benefits ── */}
      {activeSection === 'benefits' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">📈 Annual Benefits — {scenario?.label}</h3></div>
          <div className="card-body space-y-3">
            {Object.entries(bc.annualBenefits).map(([key, val]) => (
              <div key={key} className="flex items-start gap-4 p-4 bg-green-50 rounded-lg border border-green-200">
                <div className="w-40 shrink-0 text-xs font-bold text-green-800">
                  {key === 'ttmImprovement' ? 'Time-to-Market' : key === 'productivityGains' ? 'Productivity' : key === 'qualityImprovement' ? 'Quality' : 'Operational Savings'}
                </div>
                <div className="text-sm text-gray-700">{val}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeSection === 'org' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">👥 Organization Change Management — {scenario?.label}</h3></div>
          <div className="card-body"><ul className="space-y-3">{bc.orgChanges.map((c, i) => (<li key={i} className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200"><span className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">{i+1}</span><span className="text-sm text-gray-700">{c}</span></li>))}</ul></div>
        </div>
      )}

      {activeSection === 'tools' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🛠️ Tools & Platform Changes — {scenario?.label}</h3></div>
          <div className="card-body"><ul className="space-y-3">{bc.toolsChanges.map((c, i) => (<li key={i} className="flex items-start gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200"><span className="text-purple-700 font-bold text-sm">🔧</span><span className="text-sm text-gray-700">{c}</span></li>))}</ul></div>
        </div>
      )}

      {activeSection === 'devsecops' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🔒 DevSecOps Changes — {scenario?.label}</h3></div>
          <div className="card-body"><ul className="space-y-3">{bc.devSecOps.map((c, i) => (<li key={i} className="flex items-start gap-3 p-4 bg-red-50 rounded-lg border border-red-200"><span className="text-red-700">🛡️</span><span className="text-sm text-gray-700">{c}</span></li>))}</ul></div>
        </div>
      )}

      {activeSection === 'aiops' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🤖 AI Ops / Production Support — {scenario?.label}</h3></div>
          <div className="card-body"><ul className="space-y-3">{bc.aiOps.map((c, i) => (<li key={i} className="flex items-start gap-3 p-4 bg-indigo-50 rounded-lg border border-indigo-200"><span className="text-indigo-700">⚡</span><span className="text-sm text-gray-700">{c}</span></li>))}</ul></div>
        </div>
      )}

      {activeSection === 'product' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🎯 Product-Centric Ways of Working — {scenario?.label}</h3></div>
          <div className="card-body"><ul className="space-y-3">{bc.productCentricChanges.map((c, i) => (<li key={i} className="flex items-start gap-3 p-4 bg-teal-50 rounded-lg border border-teal-200"><span className="text-teal-700">🎯</span><span className="text-sm text-gray-700">{c}</span></li>))}</ul></div>
        </div>
      )}

      <div className="flex gap-4">
        <Link to="/recommendations" className="btn-primary flex-1 text-center py-3">💡 View All Recommendations →</Link>
        <Link to="/future-state"    className="btn-secondary flex-1 text-center py-3">← Future State VSM</Link>
      </div>
    </div>
  )
}
