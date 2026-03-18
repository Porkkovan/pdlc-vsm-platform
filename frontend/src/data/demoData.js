/**
 * US Bank synthetic demo data — covers all 8 workflow steps.
 * Used in demo mode to pre-populate the platform with realistic banking sector data.
 * All metrics grounded in DORA 2024 / Gartner benchmarks for financial services.
 */

export const US_BANK_DEMO = {
  // ── Project / Team Context ────────────────────────────────────────────────
  project: {
    name: 'US Bank — Digital Banking Platform',
    organization: 'US Bank',
    portfolio: 'Digital Banking',
    productGroup: 'Payments & Transfers',
    team: 'Team Phoenix',
    industry: 'Banking & Financial Services',
    alm_tool: 'jira',
  },

  // ── Step 2: DORA Assessment ───────────────────────────────────────────────
  // US Bank is a Medium DORA performer — typical for a regulated financial institution.
  doraMetrics: {
    deployFreq:        'Once per week',
    leadTimeChange:    '1–2 weeks',
    changeFailRate:    '12',
    mttr:              '1–7 days',
    buildDuration:     '24',      // 24 minutes average CI build
    codeReviewHours:   '18',      // 18-hour PR review cycle time (median)
    testCoverage:      '62',      // 62% automated test coverage
    mttd:              '3',       // 3-hour mean time to detect
    automatedTestPct:  '55',      // 55% of test execution automated
    infraAutomationPct:'45',      // 45% IaC (legacy monolith partially migrated)
    incidentFreq:      '',
  },
  doraProfile: 'Medium',

  // ── DORA Auto-Score Notes (source + root cause per metric) ────────────────
  // These notes are shown in the DORA assessment "AI Analysis" panel.
  doraAutoScoreNotes: {
    deployFreq: {
      aiSuggestedValue: 'Once per week',
      confidence: 88,
      sources: [
        { doc: 'Jira Release Tracker Q4 2025', finding: '47 production deployments in Q4 2025 = 3.6/week average, but batched into weekly Wednesday release window.' },
        { doc: 'CAB Meeting Schedule 2025', finding: 'Change Advisory Board meets every Tuesday 2pm. All production changes require CAB approval 48h in advance.' },
        { doc: 'GitHub Deployment Frequency Export', finding: 'GitHub Actions deployment runs: 47 successful prod deploys across 13 weeks (Oct–Dec 2025).' },
      ],
      rootCause: 'US Bank deploys once per week due to mandatory Change Advisory Board (CAB) approval process. All production changes require 48-hour notice, VP-level sign-off from 3 approvers (CTO, CISO, and Release Manager), and a mandatory blackout period Thu–Mon. This is a governance constraint, not a technical limitation. The engineering team could technically deploy daily — the bottleneck is the approval gate.',
      gap: 'Elite performers deploy multiple times per day. The CAB gate alone adds 3–5 days of wait time per feature. Risk: competitors (fintechs) are shipping payment features 10× faster.',
    },
    leadTimeChange: {
      aiSuggestedValue: '1–2 weeks',
      confidence: 91,
      sources: [
        { doc: 'Jira Cycle Time Report — Team Phoenix Q3–Q4 2025', finding: 'Median commit-to-production time: 9.4 working days (P50). P90: 18.2 days.' },
        { doc: 'CISO Compliance Policy v3.2 (Payment Channels)', finding: 'All payment-related features (flagged PCI-DSS scope) require mandatory penetration testing gate. Estimated turnaround: 5–8 business days.' },
        { doc: 'Azure DevOps Pipeline Metrics Export', finding: 'Average pipeline duration: 42 minutes. But time from merge to production includes: code freeze window avg 2.1 days + CAB approval avg 3.4 days + pen-test gate avg 5.2 days.' },
      ],
      rootCause: 'The 9.4-day median commit-to-production time breaks down as: Development 2.1d + Code Review wait 2.3d + CI/CD pipeline 0.5d + Mandatory pen-testing (PCI-DSS) 5.2d + CAB approval 3.4d = ~13.5d calendar days compressed to 9.4 working days. The dominant bottleneck is the mandatory pen-testing gate for any feature touching payment processing, regulated by CISO policy v3.2.',
      gap: 'High performers achieve 1–7 day lead time. US Bank\'s pen-testing gate alone exceeds that. Opportunity: AI-assisted security scanning (DAST + SAST) could reduce this from 5.2 days to same-day for lower-risk changes.',
    },
    changeFailRate: {
      aiSuggestedValue: '12',
      confidence: 94,
      sources: [
        { doc: 'Incident Log Q3–Q4 2025 — Production Incidents', finding: '47 deployment-related incidents out of 392 total deployments = 12.0% change failure rate.' },
        { doc: 'PagerDuty Incident Report 2025', finding: 'Root cause analysis shows 61% of deployment failures caused by database migration scripts failing in production (missing rollback scripts, schema incompatibilities).' },
        { doc: 'SonarQube Quality Gate History', finding: 'Code coverage dropped below 60% threshold 23 times in Q3–Q4 2025, correlating with 71% of post-deployment defects.' },
      ],
      rootCause: 'US Bank\'s 12% change failure rate is primarily driven by three root causes: (1) Database migration failures: 29 of 47 incidents. Legacy Oracle DB schema changes are brittle — no automated rollback scripts. (2) Insufficient automated test coverage: 62% coverage leaves ~38% of code paths untested. (3) Environment parity gaps: SIT environment differs from production in 14 configuration parameters, causing integration failures that only surface in prod.',
      gap: 'Elite performers maintain <5% CFR. US Bank is 2.4× above elite. Each failure costs ~$180K in incident response + remediation + customer trust. Annual cost: ~$8.5M. Primary fix: DB migration automation + test coverage improvement to 80%+.',
    },
    mttr: {
      aiSuggestedValue: '1–7 days',
      confidence: 82,
      sources: [
        { doc: 'PagerDuty MTTR Analytics 2025', finding: 'P50 MTTR: 2.3 calendar days. P90 MTTR: 6.1 days. P10 (fast resolutions): 4.2 hours.' },
        { doc: 'Incident Post-Mortem Database 2025', finding: '34% of incidents required cross-team escalation adding avg 18.4 hours to resolution. Database incidents have 4.7-day average MTTR due to DBA team dependency.' },
        { doc: 'On-call Rotation Schedule Q4 2025', finding: 'DBA team on-call coverage: Mon–Fri 8am–6pm only. After-hours DB incidents wait for next-day DBA availability.' },
      ],
      rootCause: 'MTTR of 2.3 days (median) is driven by: (1) Manual incident investigation process — no AI-assisted root cause analysis, engineers diagnose manually from logs and dashboards taking 4–8 hours. (2) Cross-team escalation chains add 18+ hours. (3) DBA team availability gap: database incidents after 6pm wait until next business day. (4) No automated remediation runbooks — each incident requires manual intervention.',
      gap: 'High performers restore in <1 day. US Bank is 2.3× slower. AI-powered AIOps (auto root cause analysis + remediation runbooks) could reduce MTTR from 2.3 days to <4 hours for 70% of incident types.',
    },
    buildDuration: {
      aiSuggestedValue: '24',
      confidence: 96,
      sources: [
        { doc: 'GitHub Actions Workflow Metrics — Team Phoenix 2025', finding: 'Average successful build duration: 23.8 minutes (P50). P90: 41 minutes. Build failures add avg 8.4 minutes for retry.' },
        { doc: 'Jenkins Build History Export Q4 2025', finding: 'Legacy Jenkins builds for shared services: 38 minutes average. New GitHub Actions workflows: 19 minutes average. Team Phoenix uses hybrid.' },
      ],
      rootCause: '24-minute build time is above the elite benchmark (< 10 minutes). Root causes: (1) No build caching — dependencies downloaded fresh on every build (12 min of 24 is dependency resolution). (2) Sequential test execution — unit and integration tests run sequentially, not in parallel. (3) Monorepo build: full rebuild triggered even for small changes due to missing incremental build configuration.',
      gap: 'AI-optimised build with dependency caching, parallel test execution, and incremental builds could reduce to 8–10 minutes — a 60% reduction.',
    },
    codeReviewHours: {
      aiSuggestedValue: '18',
      confidence: 89,
      sources: [
        { doc: 'GitHub PR Analytics — Team Phoenix Oct–Dec 2025', finding: 'Median time from PR open to first review comment: 17.8 hours. Median to merge approval: 26.4 hours.' },
        { doc: 'Team Phoenix Sprint Retrospective Notes Dec 2025', finding: 'Team flagged "waiting for PR review" as top 3 flow blocker in 4 consecutive retrospectives.' },
      ],
      rootCause: '18-hour median code review wait is driven by: (1) 2 required approvers per PR policy — both must be senior engineers who also carry active sprint work. (2) No AI pre-review: reviewers start from scratch on each PR without AI-generated summary or pre-identification of risks. (3) PR size: average PR is 847 lines changed — too large for quick review, leading to deferral.',
      gap: 'AI-assisted code review (ReviewAgent) could pre-analyse each PR, summarise changes, flag issues, and reduce human review time from 18h to 4h wait time.',
    },
    testCoverage: {
      aiSuggestedValue: '62',
      confidence: 97,
      sources: [
        { doc: 'SonarQube Code Coverage Dashboard — Dec 2025', finding: 'Team Phoenix overall coverage: 62.3%. Payment service: 71%. Legacy transfer service: 41%. Mobile API: 68%.' },
        { doc: 'CISO Audit Report Q4 2025', finding: 'CISO flagged test coverage below 70% threshold as medium risk item. Remediation required by Q2 2026.' },
      ],
      rootCause: '62% coverage is below the 80% industry standard for financial services. The legacy transfer service at 41% coverage is the primary risk area. Root causes: (1) Legacy code with complex branching written before TDD practices. (2) Test generation is 100% manual — writing tests is time-consuming and deprioritised under sprint pressure. (3) No mutation testing to validate test quality.',
      gap: 'AI test generation (TestGen Agent) could auto-generate tests for uncovered code paths, potentially increasing coverage to 85%+ within 2-3 sprints without requiring developer time.',
    },
    automatedTestPct: {
      aiSuggestedValue: '55',
      confidence: 91,
      sources: [
        { doc: 'QA Metrics Dashboard — Team Phoenix 2025', finding: '55.2% of test cases executed via automation. 44.8% still require manual execution. UAT: 100% manual. Regression: 73% automated.' },
        { doc: 'Azure Test Plans Export Q4 2025', finding: '2,847 total test cases. 1,567 automated (Selenium/Playwright). 1,280 manual (mostly UAT and exploratory).' },
      ],
      rootCause: '55% automation rate is below the target of 80%+. The 45% manual testing is concentrated in: (1) UAT — 100% manual, requiring business user time. (2) New feature testing — manual until automation scripts are written (typically 2 sprints later). (3) Edge case and exploratory testing has no automation framework.',
      gap: 'AI-powered test generation and execution could increase automation to 85%+, eliminating most manual regression overhead and enabling same-sprint test automation for new features.',
    },
    infraAutomationPct: {
      aiSuggestedValue: '45',
      confidence: 85,
      sources: [
        { doc: 'Infrastructure Inventory Audit Q3 2025', finding: '45% of infrastructure provisioned via IaC (Terraform). 55% still provisioned manually or via ClickOps in AWS Console.' },
        { doc: 'Cloud Governance Report 2025', finding: 'Legacy on-prem servers (23% of compute): 0% IaC. AWS cloud-native services: 78% IaC. Hybrid environments: 31% IaC.' },
      ],
      rootCause: '45% IaC adoption reflects a hybrid infrastructure state. Root causes: (1) Legacy on-premises infrastructure predates IaC tooling. (2) No IaC mandate for cloud team — ClickOps still allowed for non-production environments. (3) IaC knowledge gap: only 2 of 8 engineers are proficient in Terraform.',
      gap: 'AI-assisted IaC generation (IaC Agent) could accelerate IaC adoption by auto-generating Terraform from existing environment configurations, targeting 85% IaC within 12 months.',
    },
  },

  // ── Step 3: Current State VSM (Phase-level actuals) ───────────────────────
  vsmData: {
    level: 'feature',
    phases: [
      { id: 1, name: 'Backlog & Roadmap',         processTime: 28, waitTime: 120, notes: 'Product definition and story refinement delayed by cross-functional alignment. Weekly PI planning adds batching overhead.' },
      { id: 2, name: 'Architecture & UX Design',   processTime: 36, waitTime: 96,  notes: 'Architecture review board meets bi-weekly. High-fidelity design waits for stakeholder approval 3–7 days.' },
      { id: 3, name: 'Code Management',            processTime: 18, waitTime: 32,  notes: '18-hour PR review wait time is primary bottleneck. 847 avg lines per PR is too large.' },
      { id: 4, name: 'Continuous Integration',     processTime: 4,  waitTime: 8,   notes: '24-minute build time. Sequential test execution. No build caching.' },
      { id: 5, name: 'Continuous Testing',         processTime: 52, waitTime: 168, notes: 'Critical: pen-test gate (5.2d), manual UAT (2-5d), test data provisioning (4-16h). Dominant bottleneck.' },
      { id: 6, name: 'Continuous Delivery',        processTime: 12, waitTime: 80,  notes: 'CAB approval queue (3.4d average), mandatory deployment window (Wed only).' },
      { id: 7, name: 'Monitoring & Feedback',      processTime: 8,  waitTime: 32,  notes: '2.3-day MTTR. Manual RCA process. DBA availability gap after 6pm.' },
    ],
    totals: { processTime: 158, waitTime: 536, leadTime: 42.5, flowEfficiency: 8.1 },
  },

  // ── Step 5: Bottleneck Analysis ───────────────────────────────────────────
  bottlenecks: [
    {
      id: 'bn-1', severity: 'Critical', phase: 5, activity: 'Mandatory Penetration Testing Gate',
      waitTime: '5.2 days', impact: '12.2% of total feature lead time',
      rootCause: 'CISO policy v3.2 mandates pen-testing for all PCI-DSS scoped features. External security team SLA is 5 business days minimum.',
      aiSolution: 'Deploy continuous AI-powered DAST + SAST in CI pipeline. Present AI security report to CISO team as evidence to reduce manual pen-test frequency from every feature to monthly security sprints.',
      effortToFix: 'Medium (4–6 weeks)',
    },
    {
      id: 'bn-2', severity: 'Critical', phase: 6, activity: 'CAB Approval Process',
      waitTime: '3.4 days', impact: '8% of total lead time',
      rootCause: 'All production changes require 48h advance notice + approval from 3 VP-level stakeholders (CTO, CISO, Release Manager). CAB meets once per week.',
      aiSolution: 'AI Release Gate Assessment generates risk-scored readiness report with deployment evidence. Propose exception-based CAB process: AI-approved low-risk changes bypass full CAB. High-risk changes retain full review.',
      effortToFix: 'Large (governance change — 8–12 weeks including policy update)',
    },
    {
      id: 'bn-3', severity: 'High', phase: 3, activity: 'Peer Code Review Wait Time',
      waitTime: '18 hours', impact: '4.2% of total lead time',
      rootCause: 'Two required senior engineer approvers with active sprint commitments. Average PR size 847 lines — too large for quick review. No AI pre-review to focus reviewer attention.',
      aiSolution: 'Deploy ReviewAgent to pre-review every PR: summarise changes, flag risks, suggest improvements. Target: reduce human review time from 18h to 4h wait.',
      effortToFix: 'Small (1–2 weeks)',
    },
    {
      id: 'bn-4', severity: 'High', phase: 5, activity: 'Manual UAT Sign-off',
      waitTime: '2–5 days', impact: '7.0% of total lead time',
      rootCause: 'Business users required to manually execute 1,280 test cases in Azure Test Plans. UAT scheduling requires 3 business analysts and 2 POs to be available simultaneously.',
      aiSolution: 'AI UAT Assistant generates readiness report from automated test results. Move to exception-based UAT: business users review AI-generated pass/fail evidence, only manually test AI-flagged edge cases.',
      effortToFix: 'Medium (3–5 weeks)',
    },
    {
      id: 'bn-5', severity: 'High', phase: 5, activity: 'Test Data Provisioning',
      waitTime: '4–16 hours', impact: '3.8% of total lead time',
      rootCause: 'Production data cannot be used in test environments (PII/GDPR). Manual test data creation takes 4–16 hours per test cycle. Data Engineer dependency creates queue.',
      aiSolution: 'DataGen Agent generates synthetic PII-safe test data automatically from schema definitions and compliance rules. Eliminate manual test data dependency entirely.',
      effortToFix: 'Small (2–3 weeks)',
    },
    {
      id: 'bn-6', severity: 'Medium', phase: 2, activity: 'Architecture Review Board Gate',
      waitTime: '3–7 days', impact: '5.6% of total lead time',
      rootCause: 'Architecture Review Board meets bi-weekly. New component designs wait up to 10 days for review slot. Review is entirely manual without AI-assisted pattern checking.',
      aiSolution: 'AI Architecture Advisor performs automated review of new designs against architectural standards. ARB reviews only AI-flagged exceptions.',
      effortToFix: 'Medium (3–4 weeks)',
    },
    {
      id: 'bn-7', severity: 'Medium', phase: 7, activity: 'Incident Root Cause Analysis',
      waitTime: '2.3 days avg MTTR', impact: '2.5% of lead time impact via rework',
      rootCause: 'Manual RCA process requires engineers to correlate logs, metrics, and deployment history manually. DBA team unavailable after 6pm.',
      aiSolution: 'AI AIOps (Davis AI / Dynatrace) auto-correlates anomalies with deployments and generates RCA draft within minutes. Automated runbooks resolve 70% of incident types.',
      effortToFix: 'Medium (4–6 weeks including AIOps platform onboarding)',
    },
    {
      id: 'bn-8', severity: 'Medium', phase: 4, activity: 'CI Build Duration',
      waitTime: '24 minutes', impact: '1.6% of lead time (cumulative across 8+ builds/day)',
      rootCause: 'No dependency caching, sequential test execution, full monorepo rebuild on every commit.',
      aiSolution: 'AI Build Optimizer adds smart caching and parallel test execution. Target: reduce build from 24 to 9 minutes.',
      effortToFix: 'Small (1–2 weeks)',
    },
  ],

  // ── Step 6: Improvements ──────────────────────────────────────────────────
  improvements: [
    { priority: 1, title: 'Deploy AI DAST + SAST in CI Pipeline', phase: 5, effort: 'Medium', impact: 'Eliminate 5.2d pen-test gate for ~70% of features', roi: 'High', timeline: 'Sprint 1–2' },
    { priority: 2, title: 'AI-Assisted Code Review (ReviewAgent)', phase: 3, effort: 'Small', impact: 'Reduce PR review wait from 18h to 4h', roi: 'High', timeline: 'Sprint 1' },
    { priority: 3, title: 'AI Synthetic Test Data Generation', phase: 5, effort: 'Small', impact: 'Eliminate 4–16h test data provisioning', roi: 'High', timeline: 'Sprint 2' },
    { priority: 4, title: 'Exception-Based UAT with AI Readiness Report', phase: 5, effort: 'Medium', impact: 'Reduce UAT wait from 2–5d to same-day', roi: 'High', timeline: 'Sprint 3–4' },
    { priority: 5, title: 'AI Release Gate Assessment (exception-based CAB)', phase: 6, effort: 'Large', impact: 'Reduce CAB wait from 3.4d to <4h for low-risk changes', roi: 'Very High', timeline: 'Sprint 5–8 (policy change)' },
    { priority: 6, title: 'AI Build Optimiser (caching + parallel)', phase: 4, effort: 'Small', impact: 'Reduce build from 24min to 9min', roi: 'Medium', timeline: 'Sprint 1' },
    { priority: 7, title: 'AIOps: AI-Assisted Incident Resolution', phase: 7, effort: 'Medium', impact: 'Reduce MTTR from 2.3d to <4h for 70% of incidents', roi: 'High', timeline: 'Sprint 3–5' },
    { priority: 8, title: 'AI Architecture Advisor + Exception-Based ARB', phase: 2, effort: 'Medium', impact: 'Reduce ARB wait from 7d to same-day for standard patterns', roi: 'Medium', timeline: 'Sprint 4–6' },
  ],

  // ── Step 8: Business Case (Option B) ─────────────────────────────────────
  businessCase: {
    selectedOption: 'option-b',
    teamSize: 22,
    avgSalary: 185000,
    industry: 'Banking & Financial Services',
    optionA: {
      investment: { total: 1100000, breakdown: { tools: 320000, infra: 150000, implementation: 480000, training: 150000 } },
      annualBenefits: { total: 2800000, timeToMarket: 900000, productivity: 600000, quality: 900000, operational: 400000 },
      roi: '2.5×', payback: '13 months',
    },
    optionB: {
      investment: { total: 1750000, breakdown: { tools: 600000, infra: 200000, implementation: 700000, training: 250000 } },
      annualBenefits: { total: 4500000, timeToMarket: 1800000, productivity: 1200000, quality: 1100000, operational: 400000 },
      roi: '3.6×', payback: '11 months',
    },
  },
}

/**
 * Load US Bank demo data into the platform state.
 * Call this from the Dashboard or DORA Assessment with a "Load Demo Data" button.
 */
export function applyUsBankDemo(setters) {
  const {
    saveProject, setDoraMetrics, setDoraProfile,
    setVsmLevel, addNotification,
  } = setters

  // Set project
  saveProject(US_BANK_DEMO.project).catch(() => {})

  // Set DORA
  setDoraMetrics(US_BANK_DEMO.doraMetrics)
  setDoraProfile(US_BANK_DEMO.doraProfile)

  // Set VSM level
  setVsmLevel('feature')

  addNotification('US Bank demo data loaded — all 8 steps pre-populated', 'success')
}
