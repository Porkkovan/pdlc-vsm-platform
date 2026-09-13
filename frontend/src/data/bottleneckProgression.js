// Tool-stack progression per bottleneck aligned to PDLC Option ABC.pptx (latest)
// Stage 1 = Option A (16 AI tools, AI-Enabled)
// Stage 2 = Option B (21 agents, AI-First — each agent shows its parent tool in ←)
// Stage 3 = Option C (STUMP ADLC Platform, AI-Native)

export const BOTTLENECK_PROGRESSION = {

  // ── Phase 1: Backlog & Roadmap ────────────────────────────────────────────────

  'bn-1a': {
    currentTools: ['Jira', 'Confluence', 'Backlog Asst. (partial — 4/8 squads)', 'USB Docs'],
    stageA: 'Backlog Asst. + USB Docs deployed to all 8 squads. Story creation semi-automated from AC templates. Refinement wait: 1–3 days → 1 day. PI cadence unchanged.',
    stageB: 'Backlog Agent (← Backlog Asst.) runs on-demand — stories refined continuously without PI batch wait. AC quality gate auto-enforced. Discovery Agent (← DEV Bridge) surfaces demand signals upstream.',
    stageC: 'STUMP Platform: Backlog Agent + Discovery Agent orchestrated end-to-end. Human sets quarterly intent; agents decompose, refine, and sequence autonomously. PI batch dependency eliminated.',
  },
  'bn-1b': {
    currentTools: ['Confluence', 'Jira', 'DEV Bridge (partial)'],
    stageA: 'DEV Bridge connects Confluence + feedback channels → auto-structures Jira Epics with acceptance criteria templates. Manual epic authoring: 8h → 2h.',
    stageB: 'Discovery Agent (← DEV Bridge) continuously monitors all demand signals. Auto-creates structured Epics with PCI-DSS/SOX/AML compliance tags. Sprint Agent (← USB Docs) sequences dependency-aware.',
    stageC: 'STUMP Platform: Discovery Agent maintains a live demand registry. Intent Engine interprets executive priorities into epic backlog in real time. Zero manual epic authoring.',
  },
  'bn-1c': {
    currentTools: ['Jira', 'DEV Bridge (partial)', 'USB Docs'],
    stageA: 'USB Docs surfaces historical delivery patterns from 18-sprint history in planning ceremonies. Sizing debates shortened. Accuracy improves slightly — estimation remains manual.',
    stageB: 'Sprint Agent (← USB Docs) auto-sizes stories using velocity history + team capacity calendar. Sizing accuracy: 77% → 90%. Mid-sprint re-sizing: 23% → <5%.',
    stageC: 'STUMP Platform: Sprint Agent generates fully-sized sprint plan from backlog + capacity data. Human reviews and approves the sprint plan — no manual estimation.',
  },
  'bn-1d': {
    currentTools: ['Jira', 'Confluence', 'Spreadsheets (PI Planning)'],
    stageA: 'DEV Bridge surfaces cross-team Jira ticket links. USB Docs provides PI planning pattern lookup. Dependency map auto-generated from Jira data, reducing spreadsheet dependency ~40%.',
    stageB: 'Discovery Agent (← DEV Bridge) auto-detects cross-team dependencies from Jira epic relationships. Sprint Agent (← USB Docs) alerts on newly discovered blockers in real time.',
    stageC: 'STUMP Platform: Discovery Agent + Sprint Agent map all dependency chains at backlog generation time. Zero undiscovered mid-sprint blockers.',
  },

  // ── Phase 2: Architecture & UX ────────────────────────────────────────────────

  'bn-2a': {
    currentTools: ['Confluence', 'USB Docs (partial)', 'ShieldDocs'],
    stageA: 'USB Docs provides real-time ADR lookup — architects self-serve standard patterns against 140+ USB design templates. EA Board agenda reduced ~25% for clearly standard patterns.',
    stageB: 'Architecture Agent (← USB Docs) pre-screens all designs automatically. 85% of standard designs resolved within 24h without EA Board slot. Design Review Agent (← Figma AI) validates in parallel. Wait: 80h → 12h.',
    stageC: 'STUMP Platform: Architecture Agent auto-generates design proposals grounded in USB Docs. Human reviews and approves proposal before any development starts. EA Board handles strategic decisions only.',
  },
  'bn-2b': {
    currentTools: ['Figma', 'UX Design Coder (pilot — 1 squad)', 'Figma AI (pilot — 1 squad)'],
    stageA: 'UX Design Coder MCP + Figma AI deployed to all 8 squads (from pilot on 1). Design system validation automated. Wireframe-to-handoff cycle: 3 days → 1 day.',
    stageB: 'UI/UX Agent (← UX Design Coder) generates wireframe proposals from feature AC. Design Review Agent (← Figma AI) validates against US Bank design system before any developer sees the Figma file.',
    stageC: 'STUMP Platform: UI/UX Agent + Design Review Agent orchestrated — high-fidelity designs generated from feature intent. Human reviews and approves before code scaffolding starts.',
  },
  'bn-2c': {
    currentTools: ['Confluence (informal API specs)', 'GitLab', 'OpenAPI (ad hoc)'],
    stageA: 'DEV Bridge surfaces existing API contracts from Confluence. USB Docs provides API design pattern lookup. Breaking change detection added to GitLab CI as an advisory warning.',
    stageB: 'Architecture Agent (← USB Docs) auto-generates machine-readable OpenAPI contracts from feature requirements. Design Review Agent enforces contract testing as a CI quality gate.',
    stageC: 'STUMP Platform: API contracts generated and validated at backlog time from product intent. Compliance Agent validates all contracts continuously. Zero runtime contract surprises.',
  },

  'bn-2d': {
    currentTools: ['Figma', 'Manual design review checklist', 'Confluence (brand guidelines)'],
    stageA: 'Figma AI activated for all squads — auto-highlights contrast failures and spacing violations. Brand guideline doc linked in Figma. Manual review time: 4–8h → 2h.',
    stageB: 'Design Review Agent (← Figma AI) scans all Figma files automatically against WCAG AA, US Bank design system tokens, and brand rules before dev handoff. Violations surfaced in Figma with fix suggestions. Human reviews exceptions only.',
    stageC: 'STUMP Platform: Design Review Agent validates designs at generation time (UI/UX Agent output). Zero design-to-dev handoff violations. Accessibility compliance built into the generation prompt.',
  },

  // ── Phase 3: Code Management ──────────────────────────────────────────────────

  'bn-3a': {
    currentTools: ['GitLab', 'VS Code', 'GitHub Copilot (pilot — Avengers squad only)'],
    stageA: 'GitHub Copilot expanded to all 8 squads (from 1). Boilerplate, test stubs, and repetitive patterns reduced ~25%. UX Design Coder in pilot on 1 squad — Code Generator not yet available.',
    stageB: 'Code Generator (← UX Design Coder) scaffolds React components from approved Figma designs. Developers extend and review generated scaffolding, not build from scratch. Coding time: 8h → 4h for standard UI features.',
    stageC: 'STUMP Platform: Code Generator produces full feature scaffolding from approved design. Developer reviews business logic and approves merge. 70–85% of code AI-generated.',
  },
  'bn-3b': {
    currentTools: ['GitLab', 'Code Review Asst. (partial — Honeybee & Rasabee only)'],
    stageA: 'Code Review Asst. deployed to all 8 squads (from 2). GitLab MR size limit enforced at 400 lines. Mechanical checks (style, formatting, naming) automated. Review wait: 12h → 5h.',
    stageB: 'Code Reviewer (← Code Review Asst.) pre-annotates every MR with security findings, test gaps, and tech debt. Human reviewer focuses on architecture intent only. Time per MR: 2h → 30 min.',
    stageC: 'STUMP Platform: Code Reviewer completes full automated review. Human approves or requests specific changes. Same-day review cycle for all standard changes.',
  },
  'bn-3c': {
    currentTools: ['GitLab', 'SonarQube', 'Jira (manual tagging)'],
    stageA: 'Code Review Asst. flags tech debt patterns inline in every MR. DEV Bridge auto-tags debt items in Jira. Visibility improves significantly — risk scoring remains manual.',
    stageB: 'Tech Debt Agent (← DEV Bridge) scores debt impact and risk per item. Code Reviewer surfaces debt context alongside security findings. Low-risk refactors raised as auto-MRs for dev review.',
    stageC: 'STUMP Platform: Code Generator applies architectural best practices by default. Tech Debt Agent tracks and remediates drift continuously. Debt accumulation structurally reduced at source.',
  },
  'bn-3d': {
    currentTools: ['GitLab', 'VS Code'],
    stageA: 'GitHub Copilot assists with conflict resolution context. DEV Bridge surfaces branch overlap warnings. Branch lifetime limits enforced in GitLab pipeline config. Conflict frequency reduced ~30%.',
    stageB: 'Code Generator compresses feature branch lifetime — shorter branches mean fewer conflicts. Tech Debt Agent (← DEV Bridge) coordinates parallel development windows across squads.',
    stageC: 'STUMP Platform: Code Generator commits feature-complete scaffolding in a single batch per feature. Short-lived branches by design. Merge conflict frequency near-zero.',
  },

  // ── Phase 4: Continuous Integration ──────────────────────────────────────────

  'bn-4a': {
    currentTools: ['App Vuln. Solution', 'CloudBees CI'],
    stageA: 'App Vuln. Solution configured for auto-prioritisation — critical/high findings surfaced immediately; low/informational suppressed unless PCI-DSS scope. Triage time: 4h → 1h.',
    stageB: 'Vuln. Fix Agent (← App Vuln. Solution) auto-remediates low-severity vulnerabilities (dependency updates, misconfigs). Generates MR for dev review — zero manual triage for standard patterns.',
    stageC: 'STUMP Platform: Code Generator produces vulnerability-free code by design. Vuln. Fix Agent handles post-commit drift autonomously. Near-zero manual vulnerability triage.',
  },
  'bn-4b': {
    currentTools: ['CloudBees CI', 'Log Analytics', 'AppDynamics', 'Splunk'],
    stageA: 'Log Analytics connected to CloudBees post-build hooks — automated go/no-go with root cause summarisation. Flaky test detection enabled. Failure diagnosis: 2h → 30 min.',
    stageB: 'Build Agent (← QA Suite) monitors build health; Pipeline Agent (← Log Analytics) auto-quarantines flaky tests and correlates failures to recent changes. Root cause surfaced in minutes.',
    stageC: 'STUMP Platform: Build Agent + Pipeline Agent resolve common build failures autonomously. Human reviews only novel failure patterns not in the known-issue library.',
  },
  'bn-4c': {
    currentTools: ['CloudBees CI', 'App Vuln. Solution', 'JFrog Artifactory'],
    stageA: 'App Vuln. Solution configured for proactive dependency scanning on every PR. Critical dependency alerts automated in CloudBees pipeline. Vulnerable window: weeks → days.',
    stageB: 'Vuln. Fix Agent (← App Vuln. Solution) auto-raises dependency update MRs with compatibility test results attached. Pipeline Agent (← Log Analytics) validates update health post-deploy.',
    stageC: 'STUMP Platform: Code Generator selects secure, up-to-date dependency versions at code generation time. Vuln. Fix Agent handles post-commit dependency drift continuously.',
  },

  'bn-4d': {
    currentTools: ['CloudBees CI', 'Log Analytics', 'Manual pipeline configuration'],
    stageA: 'Log Analytics dashboards expose stage-level timing and flaky test frequency. CloudBees parallel pipeline config tuned. Average CI run: 80 min → 55 min.',
    stageB: 'Pipeline Agent (← Log Analytics) analyses historical run data to parallelise stages, select relevant tests per change, and quarantine flaky tests. CI run: 55 min → 25 min. Build Agent (← QA Suite) handles retry logic automatically.',
    stageC: 'STUMP Platform: Pipeline Agent orchestrates fully optimised CI with ML-driven test selection. Build Agent resolves common failures autonomously. Human reviews only novel pipeline failures.',
  },

  // ── Phase 5: Continuous Testing ───────────────────────────────────────────────

  'bn-5a': {
    currentTools: ['PractiTest', 'JMeter (manual scripts)', 'AppDynamics'],
    stageA: 'Smart Tester generates performance test scripts from API specs (no manual authoring). QA Suite provides parallel execution scaffolding. Run time reduced ~50%. Regressions auto-flagged.',
    stageB: 'QA Orchestrator (← Smart Tester) runs performance tests on every commit. Regression Agent (← USB Docs) detects degradation vs baseline. Human reviews anomalies only — no manual analysis.',
    stageC: 'STUMP Platform: QA Orchestrator + Regression Agent run performance validation continuously. Performance SLA enforced as a code generation constraint from the start of each feature.',
  },
  'bn-5b': {
    currentTools: ['App Vuln. Solution (major releases only)', 'BrowserStack', 'PractiTest'],
    stageA: 'App Vuln. Solution DAST integrated into CloudBees pipeline — runs on every release (not just major). BrowserStack automation scripts standardised. Manual trigger effort eliminated.',
    stageB: 'UAT Agent (← QA Suite) coordinates BrowserStack cross-browser automation. Vuln. Fix Agent (← App Vuln. Solution) assesses DAST results. UAT Agent generates signoff report — human approves, not executes.',
    stageC: 'STUMP Platform: UAT Agent + Compliance Agent (← Risk Asst.) handle full signoff documentation and evidence. Human approves a single summary report — no manual testing or signoff ceremonies.',
  },
  'bn-5c': {
    currentTools: ['Manual process', 'USB Docs (partial)', 'Production data copies (PII risk)'],
    stageA: 'USB Docs provides BSA/AML transaction pattern templates for manual test data construction. Search time reduced significantly. PII masking still manual — compliance risk persists.',
    stageB: 'QA Orchestrator (← Smart Tester) generates synthetic PII-safe test data using USB Docs BSA/AML transaction patterns. Realistic synthetic profiles auto-generated. Manual PII masking eliminated.',
    stageC: 'STUMP Platform: Regression Agent (← USB Docs) generates scenario-specific synthetic data on demand for every feature branch. PII exposure risk: zero. Compliance evidence auto-generated.',
  },
  'bn-5d': {
    currentTools: ['BrowserStack', 'PractiTest', 'Manual screenshot review (200+ images/release)'],
    stageA: 'Smart Tester adds AI-assisted visual diff — reduces false positive rate by ~60%. QA Suite manages baseline updates. BrowserStack test orchestration standardised across squads.',
    stageB: 'QA Orchestrator (← Smart Tester) + Regression Agent (← USB Docs): AI distinguishes intentional design changes from regressions. Human reviews only confirmed visual anomalies.',
    stageC: 'STUMP Platform: UX Design Coder + Design Review Agent generate design tokens as test constraints. Visual regression near-zero from structured, system-validated design output at source.',
  },
  'bn-5e': {
    currentTools: ['PractiTest', 'Confluence (manual API contracts)', 'GitLab CI'],
    stageA: 'USB Docs provides API contract pattern lookup. QA Suite generates consumer-driven contract test stubs. Breaking change detection added to CI pipeline as a blocking gate.',
    stageB: 'QA Orchestrator enforces contract tests on every MR. Architecture Agent (← USB Docs) validates API contracts at design approval — shift-left contract validation before any code is written.',
    stageC: 'STUMP Platform: API contracts generated and validated at backlog time. Compliance Agent enforces continuously across all consumer/producer pairs. Zero runtime contract surprises.',
  },

  'bn-5f': {
    currentTools: ['PractiTest', 'CloudBees CI', 'Manual regression test selection'],
    stageA: 'Smart Tester adds test impact analysis — high-risk paths flagged for mandatory execution. QA Suite parallelises execution across available agents. Regression run: 8h → 5h.',
    stageB: 'Regression Agent (← USB Docs) uses ML to select the minimal effective test subset per code change. QA Orchestrator (← Smart Tester) executes in parallel and quarantines flaky tests. Regression cycle: 5h → 90 min.',
    stageC: 'STUMP Platform: Regression Agent + QA Orchestrator run regression continuously. Each code commit validated with a minimal, high-confidence test set. Zero full-suite blocking runs required.',
  },

  // ── Phase 6: Continuous Delivery ─────────────────────────────────────────────

  'bn-6a': {
    currentTools: ['ServiceNow', 'App Vuln. Solution', 'DEV Bridge'],
    stageA: 'App Vuln. Solution scan results auto-attached to ServiceNow CRs — eliminates 2h/release of manual evidence preparation. Log Analytics provides automated deployment health signal. CAB schedule unchanged.',
    stageB: 'Release Gate Agent (← App Vuln. Solution) scores every CR on risk scale. Low-risk changes (65% of all CRs) auto-approved as Standard Changes — bypassing CAB queue. Wait: 80h → 12h for standard changes.',
    stageC: 'STUMP Platform: Release Gate Agent + Compliance Agent (← Risk Asst.) handle full CR lifecycle. Auto-approval rate: 90%. Human approves High/Regulatory changes only. Deploy Agent (← DEV Bridge) executes autonomously.',
  },
  'bn-6b': {
    currentTools: ['CloudBees Deploy', 'Log Analytics', 'AppDynamics (manual overnight monitoring)'],
    stageA: 'Log Analytics connected to CloudBees canary post-deploy hooks — automated go/no-go with golden signal baseline. Detection of canary issues: 2–4h → <15 min.',
    stageB: 'Pipeline Agent (← Log Analytics) monitors canary deployment health; triggers automated rollback if anomaly detected within 2 min. Human notified, not required to intervene.',
    stageC: 'STUMP Platform: Deploy Agent (← DEV Bridge) + Rollback Agent (← Log Analytics) operate canary promotions autonomously. Human intervention required only for novel error patterns.',
  },
  'bn-6c': {
    currentTools: ['DEV Bridge', 'Confluence (manual runbooks)', 'Jira'],
    stageA: 'DEV Bridge auto-generates release notes from Jira story summaries + commit messages. Log Analytics provides deployment health context. Manual drafting: 2h → 20 min review + approve.',
    stageB: 'Deploy Agent (← DEV Bridge) generates release notes, runbook delta, and risk classification as part of the deployment workflow. Runbooks auto-updated on every deploy.',
    stageC: 'STUMP Platform: Deploy Agent + Compliance Agent generate release notes, runbook, and compliance evidence as a single package at deploy time. Zero manual documentation required.',
  },

  'bn-6d': {
    currentTools: ['CloudBees Deploy', 'AppDynamics (manual monitoring)', 'Log Analytics'],
    stageA: 'Log Analytics post-deploy hooks provide automated golden signal comparison against pre-deploy baseline. Anomaly detection: 30 min manual → 5 min automated alert. Rollback still manually triggered.',
    stageB: 'Rollback Agent (← Log Analytics) monitors deployment health, compares golden signals to baseline, and auto-triggers rollback within 2 min of threshold breach. Human notified; rollback already in progress.',
    stageC: 'STUMP Platform: Deploy Agent (← DEV Bridge) + Rollback Agent manage full deployment lifecycle. Rollback decisions made autonomously at sub-minute speed. Customer impact window: <2 min.',
  },

  // ── Phase 7: Operations & Monitoring ─────────────────────────────────────────

  'bn-7a': {
    currentTools: ['AppDynamics', 'Splunk', 'Log Analytics', 'Risk Asst. (partial)'],
    stageA: 'Log Analytics applies risk-based threshold tuning — reduces noise from 200+/day to <50 actionable alerts. USB Docs provides historical incident context for on-call runbooks.',
    stageB: 'Monitor Agent (← Log Analytics) correlates AppDynamics + Splunk signals automatically. Alert-to-action routing automated. Actionable alert rate: <5% → >70%. MTTD: <5 min.',
    stageC: 'STUMP Platform: Monitor Agent detects anomalies pre-emptively before user impact using predictive baseline modelling. Incident Triage Agent (← USB Docs) auto-routes and pre-executes runbooks.',
  },
  'bn-7b': {
    currentTools: ['AppDynamics', 'Splunk', 'USB Docs', 'Risk Asst. (partial)'],
    stageA: 'Risk Asst. integrated into Splunk runbooks — historical incident context and runbook lookup surfaces for on-call engineers within Splunk. MTTR: 8.4h → 5.2h. Approaching 4h OCC SLA.',
    stageB: 'Monitor Agent (← Log Analytics) correlates all signals automatically. Incident Triage Agent (← USB Docs) executes runbook steps and generates RCA draft within 30 min of incident start. MTTR: 5.2h → 2.2h. P1 SLA breaches eliminated.',
    stageC: 'STUMP Platform: Incident Triage Agent auto-resolves known incident scenarios. Compliance Agent (← Risk Asst.) files regulatory evidence. Human approves resolution for novel incidents. MTTR: <45 min.',
  },
  'bn-7c': {
    currentTools: ['AppDynamics', 'Log Analytics', 'Spreadsheets (quarterly capacity reviews)'],
    stageA: 'Log Analytics + USB Docs surface capacity trend analysis from AppDynamics historical data. Quarterly reviews supplemented with monthly AI-generated forecasts. Over-provisioning visibility improved.',
    stageB: 'Monitor Agent (← Log Analytics) continuously models capacity requirements against business calendar events. Auto-scaling thresholds dynamically updated each sprint. Cloud waste reduced ~30%.',
    stageC: 'STUMP Platform: Monitor Agent + Compliance Agent provide predictive scaling driven by business intent signals. Over-provisioning structurally reduced to <10%.',
  },
  'bn-7d': {
    currentTools: ['Confluence (manual PIR template)', 'Splunk (manual log search)', 'Jira'],
    stageA: 'USB Docs + Log Analytics pre-populate incident timeline from Splunk logs automatically. PIR template auto-filled. Manual drafting: 4–8h → ~1h.',
    stageB: 'Incident Triage Agent (← USB Docs) auto-generates full PIR document from incident signals and runbook execution log. Action items auto-created in Jira with owners assigned. Human reviews and approves.',
    stageC: 'STUMP Platform: Full PIR generated within 1h of incident closure. Known failure patterns auto-feed into Regression Agent (← USB Docs) test suite. Recurrence rate near-zero via learning loop.',
  },
  'bn-7e': {
    currentTools: ['Risk Asst. (partial)', 'Manual audit prep spreadsheets', 'ServiceNow GRC (limited)'],
    stageA: 'Risk Asst. maps existing CI artefacts (SAST reports, test results, deployment logs) to SOC2/PCI controls automatically. Audit prep reduced by ~50%. Evidence still manually assembled.',
    stageB: 'Compliance Agent (← Risk Asst.) continuously monitors infrastructure and pipeline for policy drift. Auto-generates evidence packages per control framework. Audit prep: 3 weeks → 1 day.',
    stageC: 'STUMP Platform: Compliance Agent monitors all PDLC phases continuously. Policy violations blocked at source. Auditors access a live compliance dashboard — zero prep effort. Continuous compliance by design.',
  },
}
