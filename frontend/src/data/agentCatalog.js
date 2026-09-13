export const STATIC_AGENT_CATALOG = {
  'option-a': {
    totalTools: 16, humanModel: 'Human-Led + AI Augmented',
    byPhase: {
      'Phase 1 — Strategy & Roadmap':   ['Atlassian Intelligence', 'Linear AI', 'Notion AI'],
      'Phase 2 — Feature Definition':   ['GitHub Copilot Chat', 'Azure OpenAI', 'Jira AI'],
      'Phase 3 — Architecture':         ['GitHub Copilot', 'Miro AI Diagramming'],
      'Phase 4 — Development':          ['GitHub Copilot Business', 'Azure OpenAI Codex'],
      'Phase 5 — Testing':              ['Tonic.ai / DataGen', 'Applitools', 'Playwright AI'],
      'Phase 6 — DevSecOps':            ['Snyk', 'GitHub Advanced Security', 'Checkov'],
      'Phase 7 — AIOps & Monitoring':   ['Dynatrace Davis AI', 'Datadog AI', 'OpenTelemetry'],
    },
  },
  'option-b': {
    totalAgents: 21, humanModel: 'Hybrid: 5 Core Roles + 21 Assistive Agents (← on-demand)', notation: 'assistive',
    byPhase: {
      'Phase 1 — Discovery & Strategy': [
        { agent: '← Insight Analyst',       tool: 'Azure OpenAI + Notion AI',              role: 'Generates competitive insights, market analysis and strategic options on demand — human PO reviews' },
        { agent: '← Market Research Agent', tool: 'Azure OpenAI + Perplexity',             role: 'Pulls industry benchmarks and regulatory landscape on demand — human validates findings' },
      ],
      'Phase 2 — Feature Definition': [
        { agent: '← FeatureGen Agent',      tool: 'GitHub Copilot Chat + Azure OpenAI',    role: 'Drafts feature briefs and acceptance criteria from outcome statements — PO reviews and refines' },
        { agent: '← StoryGen Agent',        tool: 'Azure OpenAI + Jira AI',                role: 'Decomposes features into user stories with ACs and story points — PO refines and approves' },
      ],
      'Phase 3 — Architecture': [
        { agent: '← Architecture Review Agent', tool: 'Azure OpenAI + GitHub Copilot',    role: 'Reviews proposed architecture against security and compliance patterns — Tech Lead approves' },
        { agent: '← Dependency Mapper Agent',   tool: 'Azure OpenAI + Miro AI',           role: 'Maps service dependencies and risks in proposed changes — Tech Lead validates' },
      ],
      'Phase 4 — Development': [
        { agent: '← Code Generator Agent', tool: 'GitHub Copilot Enterprise',              role: 'Generates implementation code from story + ACs — developer reviews and merges' },
        { agent: '← Code Reviewer Agent',  tool: 'GitHub Copilot + CodeClimate',          role: 'Reviews PRs for bugs, patterns and security — developer confirms before merge' },
        { agent: '← PR Description Agent', tool: 'GitHub Copilot',                        role: 'Auto-drafts PR descriptions with change summary and risk flags — developer edits before publish' },
      ],
      'Phase 5 — Testing': [
        { agent: '← AI UAT Assistant',      tool: 'Azure OpenAI + TestRail',               role: 'Generates UAT test cases from ACs and user journeys — QA Lead reviews and executes' },
        { agent: '← DataGen Agent',         tool: 'Tonic.ai + Faker',                      role: 'Provisions synthetic test data in < 2 min on demand — QA Lead validates schema' },
        { agent: '← Test Case Generator',   tool: 'Azure OpenAI + TestRail',               role: 'Produces integration and regression test cases from story deltas — QA Lead approves suite' },
        { agent: '← Visual Regression Agent', tool: 'Applitools',                          role: 'Detects UI regressions across breakpoints on every deploy — QA Lead reviews diffs' },
      ],
      'Phase 6 — DevSecOps': [
        { agent: '← AI SAST Agent',          tool: 'Snyk + Semgrep',                       role: 'Runs security analysis on every PR — flags High/Critical for Tech Lead / CISO review' },
        { agent: '← Compliance-as-Code Agent', tool: 'Checkov + Drata',                    role: 'Validates IaC against SOC2/GDPR/Basel III policies — DevOps Engineer reviews waivers' },
        { agent: '← AI Release Manager',    tool: 'GitHub Actions + Azure DevOps',         role: 'Validates quality gates and coordinates deployment — DevOps Engineer approves each release' },
      ],
      'Phase 7 — AIOps & Monitoring': [
        { agent: '← AI Incident Triage',    tool: 'PagerDuty + Azure OpenAI',              role: 'Classifies and routes incidents to correct team in < 30 sec — engineer confirms routing' },
        { agent: '← Anomaly Detection Agent', tool: 'Dynatrace Davis AI + Datadog',        role: 'Detects production anomalies and surfaces root cause — on-call engineer takes action' },
        { agent: '← Auto-Remediation Agent', tool: 'Kubernetes + Dynatrace',              role: 'Executes pre-approved runbooks for known failure patterns — engineer reviews each remediation' },
        { agent: '← Predictive Scaler Agent', tool: 'AWS Predictive Scaling + KEDA',      role: 'Forecasts traffic 30–60 min ahead and pre-scales — DevOps Engineer sets guardrails' },
        { agent: '← Telemetry Sentinel',    tool: 'Datadog Watchdog + OpenTelemetry',      role: 'Converts production signals to Jira backlog items — PO reviews signal-driven tickets weekly' },
      ],
    },
  },
  'option-c': {
    totalAgents: 21, humanModel: 'AI-First: Product Definer + Product Builder + 21 Autonomous Agents (⚙)', notation: 'autonomous', platform: 'STUMP Agentic Platform',
    byPhase: {
      'Phase 1 — Discovery & Strategy': [
        { agent: '⚙ Insight Analyst',       tool: 'STUMP + Azure OpenAI',                  role: 'Runs discovery autonomously on new product brief — Product Definer reviews weekly output' },
        { agent: '⚙ Market Research Agent', tool: 'STUMP + Perplexity',                    role: 'Continuously monitors market signals and generates hypothesis briefs — Definer promotes to queue' },
      ],
      'Phase 2 — Feature Definition': [
        { agent: '⚙ FeatureGen Agent',      tool: 'STUMP + Azure OpenAI',                  role: 'Decomposes outcome brief into feature list with ACs autonomously — Definer approves sprint scope' },
        { agent: '⚙ StoryGen Agent',        tool: 'STUMP + Azure OpenAI',                  role: 'Auto-generates user stories from features — no human writes stories. Definer approves.' },
      ],
      'Phase 3 — Architecture': [
        { agent: '⚙ Architecture Review Agent', tool: 'STUMP + GitHub Copilot',            role: 'Validates and selects architecture pattern autonomously — Builder monitors SLOs and exceptions' },
        { agent: '⚙ Dependency Mapper Agent',   tool: 'STUMP + Azure OpenAI',              role: 'Maps all service dependencies and risk flags — Builder reviews exception queue only' },
      ],
      'Phase 4 — Development': [
        { agent: '⚙ Code Generator Agent', tool: 'STUMP + GitHub Copilot Enterprise',      role: 'Generates full implementation from story+ACs — commits to branch. Definer approves final PR.' },
        { agent: '⚙ Code Reviewer Agent',  tool: 'STUMP + GitHub Copilot',                role: 'Reviews every PR autonomously — blocks merge on quality violations without human intervention' },
        { agent: '⚙ PR Description Agent', tool: 'STUMP + GitHub Copilot',               role: 'Auto-generates PR metadata — no human writes PR descriptions in Stage 3' },
      ],
      'Phase 5 — Testing': [
        { agent: '⚙ AI UAT Assistant',      tool: 'STUMP + TestRail',                      role: 'Generates and executes UAT suites autonomously — Definer approves pass/fail gate only' },
        { agent: '⚙ DataGen Agent',         tool: 'STUMP + Tonic.ai',                      role: 'Provisions synthetic data autonomously before every test run — no human involvement required' },
        { agent: '⚙ Test Case Generator',   tool: 'STUMP + Azure OpenAI',                 role: 'Generates full regression suite from story deltas — autonomous execution, Builder monitors coverage' },
        { agent: '⚙ Visual Regression Agent', tool: 'STUMP + Applitools',                  role: 'Catches UI regressions autonomously — blocks deploy on regression without human gate' },
      ],
      'Phase 6 — DevSecOps (Governance Agents)': [
        { agent: '⚙ Secure-by-Design Architect', tool: 'STUMP + Checkov + AWS Config',     role: 'Validates every IaC change against CISO-approved policy library — blocks non-compliant deploys' },
        { agent: '⚙ Compliance-as-Code Orchestrator', tool: 'STUMP + Drata + Vanta',      role: 'Validates GDPR/DORA/Basel III on every commit — blocks violations, generates compliance evidence' },
        { agent: '⚙ MRM Agent',            tool: 'STUMP + Azure ML',                       role: 'Monitors model drift continuously — auto-disables feature flag if drift > threshold, alerts Builder' },
        { agent: '⚙ Governance Controller', tool: 'STUMP Platform',                        role: 'Wraps all agent transitions — validates every handoff meets governance protocol, immutable audit trail' },
        { agent: '⚙ AI Release Manager',   tool: 'STUMP + GitHub Actions',                 role: 'Orchestrates full deployment pipeline autonomously — all quality gates pass before prod' },
      ],
      'Phase 7 — AIOps & Intelligence': [
        { agent: '⚙ AI Incident Commander', tool: 'STUMP + PagerDuty + Dynatrace',         role: 'Handles all Sev-2 and below autonomously — classifies, routes, remediates, generates PIR. Sev-1 escalates.' },
        { agent: '⚙ Predictive Scaler Agent', tool: 'STUMP + KEDA + AWS Predictive',      role: 'Pre-scales infrastructure 30–60 min ahead of predicted load — no human intervention required' },
        { agent: '⚙ STUMP Intelligence Agent', tool: 'STUMP + Heap + Mixpanel',            role: 'Generates weekly feature hypothesis digest from live signals — Definer reviews and promotes to brief' },
      ],
    },
  },
}
