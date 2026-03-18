/**
 * Per-option future state phase & activity definitions.
 * Each option has distinct activities, process times, wait times.
 * Option C = ADLC (AI-Driven Lifecycle) using BMAD approach.
 *
 * activity.type:
 *   'human'    — human-only task
 *   'agent'    — fully AI/agent automated
 *   'hybrid'   — human leads, AI assists
 *   'oversight'— human spot-check / approval only
 *
 * All times in HOURS.
 * flowEfficiency per phase = processTime / (processTime + waitTime)
 */

// ─── OPTION A — AI-Assisted (40% automation) ─────────────────────────────────
// Same 7 phases, ~28 activities. All human roles retained. AI as co-pilot.
// PT ≈ 65h (-35%), WT ≈ 155h (-71%), activity-level FE ≈ 30%

export const OPTION_A_PHASES = [
  {
    id: 1,
    name: 'Backlog & Roadmap',
    subtitle: 'AI-Assisted Planning',
    activities: [
      {
        id: 'a-p1-1', name: 'AI Portfolio Flow Analytics',
        type: 'hybrid', role: 'Delivery Manager + AI VSM Analyzer', agent: 'AI VSM Analyzer',
        processTime: 5, waitTime: 8,
        desc: 'AI ingests cycle time, WIP, and lead time data from Jira/ADO. Surfaces bottleneck patterns and delay signals. DM reviews AI findings and prioritises.',
      },
      {
        id: 'a-p1-2', name: 'AI-Assisted Roadmap Definition',
        type: 'hybrid', role: 'Product Manager + AI Roadmap Assistant', agent: 'AI Roadmap Assistant',
        processTime: 10, waitTime: 8,
        desc: 'AI analyses market signals, competitor releases, and feedback to suggest roadmap priorities. PM refines sequencing and aligns with stakeholders.',
      },
      {
        id: 'a-p1-3', name: 'AI Feature + BDD Generation',
        type: 'hybrid', role: 'BA + FeatureGen/ScenarioGen Agents', agent: 'FeatureGen Agent',
        processTime: 2, waitTime: 8,
        desc: 'AI generates feature descriptions, acceptance criteria, and full Gherkin BDD scenarios from high-level goals. BA reviews and refines via chat.',
      },
      {
        id: 'a-p1-4', name: 'Story Creation + AI Estimation',
        type: 'hybrid', role: 'Product Owner + StoryGen Agent', agent: 'StoryGen Agent',
        processTime: 1, waitTime: 4,
        desc: 'AI decomposes features into user stories and suggests relative story point estimates based on historical velocity. PO reviews and approves.',
      },
    ],
  },
  {
    id: 2,
    name: 'Architecture & UX Design',
    subtitle: 'AI-Assisted Design',
    activities: [
      {
        id: 'a-p2-1', name: 'AI-Assisted Solution Architecture',
        type: 'hybrid', role: 'Solution Architect + AI Architecture Advisor', agent: 'AI Architecture Advisor',
        processTime: 6, waitTime: 16,
        desc: 'AI queries architecture pattern knowledge base, suggests stack options, and identifies trade-offs. Architect selects, customises, and signs off.',
      },
      {
        id: 'a-p2-2', name: 'AI UX Research + Wireframing',
        type: 'hybrid', role: 'UX Designer + DesignGen Agent', agent: 'DesignGen Agent',
        processTime: 5, waitTime: 8,
        desc: 'AI generates user flow diagrams and wireframe variants from persona + requirements prompts. UX designer refines selected variant.',
      },
      {
        id: 'a-p2-3', name: 'AI Hi-Fidelity Design + Handoff',
        type: 'hybrid', role: 'UI/UX Designer + DesignGen Agent', agent: 'DesignGen Agent',
        processTime: 12, waitTime: 8,
        desc: 'AI applies brand design tokens to wireframes, generates Figma mockups and component specs. Designer polishes and exports for handoff.',
      },
      {
        id: 'a-p2-4', name: 'AI Technical Design Documents',
        type: 'hybrid', role: 'Tech Lead + DesignDoc Agent', agent: 'DesignDoc Agent',
        processTime: 3, waitTime: 4,
        desc: 'AI generates API contracts, sequence diagrams, and technical README from user story. Tech Lead reviews for accuracy and completeness.',
      },
    ],
  },
  {
    id: 3,
    name: 'Code Management',
    subtitle: 'AI Co-pilot Coding',
    activities: [
      {
        id: 'a-p3-1', name: 'AI Co-pilot Feature Development',
        type: 'hybrid', role: 'Developer + CodeGen Agent', agent: 'CodeGen Agent',
        processTime: 13, waitTime: 0,
        desc: 'Developer leads implementation with AI providing real-time completions, boilerplate generation, refactor suggestions, and inline explanations.',
      },
      {
        id: 'a-p3-2', name: 'AI Unit Test Generation',
        type: 'agent', role: 'AI (Developer reviews)', agent: 'TestGen Agent',
        processTime: 0.5, waitTime: 0,
        desc: 'AI auto-generates unit tests from code and user stories, covering happy path, edge cases, and error scenarios to meet coverage thresholds.',
      },
      {
        id: 'a-p3-3', name: 'Automated Code Quality + Security',
        type: 'agent', role: 'AI (auto-run on every commit)', agent: 'AI Code Quality Tools',
        processTime: 0.5, waitTime: 0.5,
        desc: 'AI-powered SonarQube and Checkmarx scan on every push. Issues surfaced as PR inline comments with auto-fix suggestions.',
      },
      {
        id: 'a-p3-4', name: 'AI-Assisted Peer Review',
        type: 'hybrid', role: 'Tech Lead + ReviewAgent', agent: 'ReviewAgent',
        processTime: 1, waitTime: 8,
        desc: 'AI pre-reviews diff and adds context-aware comments on bugs, style, and security. Human reviewer validates AI findings and approves PR.',
      },
    ],
  },
  {
    id: 4,
    name: 'Continuous Integration',
    subtitle: 'AI-Optimised Build',
    activities: [
      {
        id: 'a-p4-1', name: 'AI-Optimised Build Pipeline',
        type: 'agent', role: 'AI Build Optimizer (DevOps configured)', agent: 'AI Build Optimizer',
        processTime: 0.4, waitTime: 1.5,
        desc: 'AI analyses dependency graph to enable parallel builds and smart caching. Average build time reduced from 22 min to 9 min.',
      },
      {
        id: 'a-p4-2', name: 'AI SAST + Artifact Creation',
        type: 'agent', role: 'AI SAST Tools + AI Artifact Manager', agent: 'AI SAST Tools',
        processTime: 0.4, waitTime: 1.5,
        desc: 'ML-powered SAST reduces false positives by 60%. Artifacts auto-tagged with metadata and compliance check results.',
      },
      {
        id: 'a-p4-3', name: 'Automated DEV Deployment',
        type: 'agent', role: 'AI Deployment Agent', agent: 'AI Deployment Agent',
        processTime: 0.4, waitTime: 0.5,
        desc: 'AI auto-provisions DEV environment, monitors deployment health, and rolls back automatically on anomaly detection.',
      },
    ],
  },
  {
    id: 5,
    name: 'Continuous Testing',
    subtitle: 'AI-Accelerated QA',
    activities: [
      {
        id: 'a-p5-1', name: 'AI Environment Auto-Provisioning',
        type: 'agent', role: 'AI Environment Manager', agent: 'AI Environment Manager',
        processTime: 1, waitTime: 1,
        desc: 'AI auto-provisions test environments with correct dependencies, service stubs, and network configurations in under 15 minutes.',
      },
      {
        id: 'a-p5-2', name: 'AI Synthetic Test Data Generation',
        type: 'agent', role: 'DataGen Agent', agent: 'DataGen Agent',
        processTime: 1, waitTime: 2,
        desc: 'AI generates privacy-compliant synthetic test data from database schema and PII rules. Eliminates manual test data setup waits.',
      },
      {
        id: 'a-p5-3', name: 'AI Smart Test Selection + Execution',
        type: 'agent', role: 'AI Test Selection + AI Test Execution', agent: 'AI Test Execution',
        processTime: 2, waitTime: 1,
        desc: 'AI uses change impact analysis to select minimal regression set. Parallelises execution across cloud grid. Predicts and quarantines flaky tests.',
      },
      {
        id: 'a-p5-4', name: 'AI Performance Testing',
        type: 'agent', role: 'AI Performance Analyzer', agent: 'AI Performance Analyzer',
        processTime: 5, waitTime: 3,
        desc: 'AI auto-generates load profiles from production traffic patterns. Executes performance tests and identifies regressions with code-change correlation.',
      },
      {
        id: 'a-p5-5', name: 'AI DAST Security Scan',
        type: 'agent', role: 'AI DAST Tools', agent: 'AI DAST Tools',
        processTime: 1.5, waitTime: 3,
        desc: 'AI-driven DAST uses intelligent fuzzing and learns application behaviour to reduce false positives by 55% vs manual scanning.',
      },
      {
        id: 'a-p5-6', name: 'AI-Assisted UAT + Signoff',
        type: 'hybrid', role: 'QA Lead + AI UAT Assistant + Product Owner', agent: 'AI UAT Assistant',
        processTime: 4, waitTime: 16,
        desc: 'AI consolidates all test results into a risk-scored readiness report. QA Lead and PO review AI report and sign off. Reduces review time from 2-5 days to same-day.',
      },
      {
        id: 'a-p5-7', name: 'AI Defect Triage + Routing',
        type: 'agent', role: 'AI Defect Triage', agent: 'AI Defect Triage',
        processTime: 1, waitTime: 0,
        desc: 'AI auto-categorises defects by root cause, assigns severity, and routes to the correct team. Eliminates triage meeting overhead.',
      },
    ],
  },
  {
    id: 6,
    name: 'Continuous Delivery',
    subtitle: 'AI-Orchestrated Release',
    activities: [
      {
        id: 'a-p6-1', name: 'AI IaC Generation + Validate',
        type: 'hybrid', role: 'DevOps Engineer + IaC Agent', agent: 'IaC Agent',
        processTime: 4, waitTime: 0,
        desc: 'AI generates Terraform/CDK templates from environment requirements. DevOps validates drift detection and applies.',
      },
      {
        id: 'a-p6-2', name: 'AI Stage Deployment + Monitoring',
        type: 'agent', role: 'AI Deployment Agent', agent: 'AI Deployment Agent',
        processTime: 1, waitTime: 4,
        desc: 'AI orchestrates SIT/UAT/staging deployments, monitors health checks, and auto-rolls back on failure within 2 minutes.',
      },
      {
        id: 'a-p6-3', name: 'AI Release Gate Assessment',
        type: 'hybrid', role: 'Release Manager + AI Release Manager', agent: 'AI Release Manager',
        processTime: 1, waitTime: 16,
        desc: 'AI validates all release criteria and produces a risk-scored readiness report. Release Manager reviews and approves. Eliminates CAB queue wait.',
      },
      {
        id: 'a-p6-4', name: 'AI Production Deployment',
        type: 'agent', role: 'AI Production Deploy', agent: 'AI Production Deploy',
        processTime: 1, waitTime: 4,
        desc: 'AI implements blue-green or canary deployment strategy. Monitors KPIs and auto-scales. Rolls back on anomaly within 90 seconds.',
      },
      {
        id: 'a-p6-5', name: 'AI Release Notes Generation',
        type: 'agent', role: 'ReleaseNotes Agent', agent: 'ReleaseNotes Agent',
        processTime: 0.2, waitTime: 0,
        desc: 'AI auto-generates audience-appropriate release notes from commits, Jira tickets, and PR descriptions.',
      },
    ],
  },
  {
    id: 7,
    name: 'Monitoring & Feedback',
    subtitle: 'AI-Powered AIOps',
    activities: [
      {
        id: 'a-p7-1', name: 'AI APM + Anomaly Detection',
        type: 'agent', role: 'AI APM (Davis AI)', agent: 'AI APM (Davis AI)',
        processTime: 1, waitTime: 0,
        desc: 'AI continuously monitors latency, error rates, and resource usage. Correlates anomalies with recent deployments and suggests root causes.',
      },
      {
        id: 'a-p7-2', name: 'AI Log Intelligence',
        type: 'agent', role: 'AI Log Analyzer', agent: 'AI Log Analyzer',
        processTime: 0.5, waitTime: 0,
        desc: 'NLP-powered log parsing detects patterns and anomalies across distributed services in real-time.',
      },
      {
        id: 'a-p7-3', name: 'AI Incident Management',
        type: 'hybrid', role: 'SRE + IncidentAgent', agent: 'IncidentAgent',
        processTime: 1.5, waitTime: 8,
        desc: 'AI auto-categorises incidents, routes to correct team, and generates RCA draft. SRE validates and executes resolution. MTTR reduced by ~60%.',
      },
      {
        id: 'a-p7-4', name: 'AI Customer Feedback Analysis',
        type: 'hybrid', role: 'Product Manager + FeedbackAgent', agent: 'FeedbackAgent',
        processTime: 1, waitTime: 16,
        desc: 'AI synthesises NPS, support tickets, and usage analytics into prioritised product insights and backlog recommendations.',
      },
    ],
  },
]

// ─── OPTION B — Hybrid (65% automation) ──────────────────────────────────────
// 7 phases, ~20 activities. 5 core human roles. AI handles execution in key phases.
// PT ≈ 30h (-70%), WT ≈ 38h (-93%), activity-level FE ≈ 44%

export const OPTION_B_PHASES = [
  {
    id: 1,
    name: 'Backlog & Roadmap',
    subtitle: 'AI-Led Planning Pipeline',
    activities: [
      {
        id: 'b-p1-1', name: 'AI Backlog Intelligence Pipeline',
        type: 'agent', role: 'AI VSM Analyzer + AI Roadmap Assistant (PO reviews output)', agent: 'AI Roadmap Assistant',
        processTime: 2, waitTime: 2,
        desc: 'AI continuously ingests ALM data, analyses market signals, and surfaces prioritised epics with effort estimates and delivery risk flags. PO reviews AI output.',
      },
      {
        id: 'b-p1-2', name: 'Product Owner Roadmap + Feature Definition',
        type: 'hybrid', role: 'Product Owner + FeatureGen/ScenarioGen Agents', agent: 'FeatureGen Agent',
        processTime: 5, waitTime: 8,
        desc: 'PO defines strategic direction and outcomes. AI generates feature descriptions, BDD scenarios, and user stories automatically from PO-defined epics.',
      },
    ],
  },
  {
    id: 2,
    name: 'Architecture & UX Design',
    subtitle: 'AI-Recommended Architecture',
    activities: [
      {
        id: 'b-p2-1', name: 'AI Architecture + UI Design Generation',
        type: 'agent', role: 'AI Architecture Advisor + DesignGen Agent (TL reviews)', agent: 'AI Architecture Advisor',
        processTime: 1, waitTime: 4,
        desc: 'AI generates architecture recommendation, API contracts, and UI wireframes autonomously. Tech Lead reviews AI output for feasibility and compliance.',
      },
      {
        id: 'b-p2-2', name: 'Tech Lead Architecture Decision + Sign-off',
        type: 'hybrid', role: 'Tech Lead / Architect (AI-informed)', agent: null,
        processTime: 3, waitTime: 8,
        desc: 'Tech Lead makes final architecture decision based on AI recommendation and team context. This is the key human judgment gate in design phase.',
      },
    ],
  },
  {
    id: 3,
    name: 'Code Management',
    subtitle: 'AI-Accelerated Development',
    activities: [
      {
        id: 'b-p3-1', name: 'AI-Assisted Feature Development',
        type: 'hybrid', role: 'Developer + CodeGen Agent', agent: 'CodeGen Agent',
        processTime: 10, waitTime: 0,
        desc: 'Developer implements features with heavy AI co-pilot support. AI generates implementation plans, boilerplate, tests, and documentation concurrently.',
      },
      {
        id: 'b-p3-2', name: 'AI Autonomous Code Review + Merge',
        type: 'agent', role: 'ReviewAgent + AI Code Quality Tools (auto-merge if pass)', agent: 'ReviewAgent',
        processTime: 0.3, waitTime: 2,
        desc: 'AI performs full code review: correctness, security, style, test coverage. Auto-merges if all quality gates pass. Only flags exceptions for human review.',
      },
      {
        id: 'b-p3-3', name: 'Tech Lead Security + Exception Review',
        type: 'oversight', role: 'Tech Lead (exception only)', agent: null,
        processTime: 0.5, waitTime: 2,
        desc: 'Tech Lead only reviews AI-flagged exceptions (security risks, architectural violations). ~20% of PRs require human attention in Hybrid model.',
      },
    ],
  },
  {
    id: 4,
    name: 'Continuous Integration',
    subtitle: 'Autonomous Build Pipeline',
    activities: [
      {
        id: 'b-p4-1', name: 'AI Self-Healing Build + SAST',
        type: 'agent', role: 'AI Build Optimizer + AI SAST Tools', agent: 'AI Build Optimizer',
        processTime: 0.3, waitTime: 0.8,
        desc: 'AI-optimised build with parallel execution, smart caching, and self-healing scripts. ML-powered SAST runs concurrently with near-zero false positives.',
      },
      {
        id: 'b-p4-2', name: 'AI Artifact + DEV Auto-Deploy',
        type: 'agent', role: 'AI Artifact Manager + AI Deployment Agent', agent: 'AI Deployment Agent',
        processTime: 0.2, waitTime: 0.3,
        desc: 'Artifacts auto-tagged and versioned. DEV environment provisioned and validated automatically. Zero human touch in CI pipeline.',
      },
    ],
  },
  {
    id: 5,
    name: 'Continuous Testing',
    subtitle: 'AI Quality Intelligence',
    activities: [
      {
        id: 'b-p5-1', name: 'AI Environment + Test Data Pipeline',
        type: 'agent', role: 'AI Environment Manager + DataGen Agent', agent: 'AI Environment Manager',
        processTime: 0.3, waitTime: 0.5,
        desc: 'AI provisions test environments and generates synthetic test data simultaneously in under 10 minutes. Eliminates all manual environment setup queues.',
      },
      {
        id: 'b-p5-2', name: 'AI Full Regression + Performance + Security',
        type: 'agent', role: 'AI Test Execution + AI Performance Analyzer + AI DAST Tools', agent: 'AI Test Execution',
        processTime: 2, waitTime: 1,
        desc: 'All test types run in parallel: regression, performance, and security. AI generates consolidated quality report with risk score and deployment recommendation.',
      },
      {
        id: 'b-p5-3', name: 'AI UAT Readiness Report + QA Lead Sign-off',
        type: 'oversight', role: 'QA Lead reviews AI readiness report', agent: 'AI UAT Assistant',
        processTime: 0.5, waitTime: 4,
        desc: 'AI generates UAT readiness report with test coverage, risk score, and pass/fail summary. QA Lead reviews and approves in exception-only model. Same-day signoff.',
      },
    ],
  },
  {
    id: 6,
    name: 'Continuous Delivery',
    subtitle: 'Zero-Touch Release Pipeline',
    activities: [
      {
        id: 'b-p6-1', name: 'AI IaC + Stage + Canary Deploy',
        type: 'agent', role: 'AI Deployment Agent + IaC Agent + AI Production Deploy', agent: 'AI Deployment Agent',
        processTime: 0.5, waitTime: 0.5,
        desc: 'AI generates IaC, deploys to staging, runs smoke tests, and executes canary production deployment — all automated in a single pipeline.',
      },
      {
        id: 'b-p6-2', name: 'AI Release Gate: Automated Risk Decision',
        type: 'agent', role: 'AI Release Manager (DevOps Engineer on-call for exceptions)', agent: 'AI Release Manager',
        processTime: 0.3, waitTime: 2,
        desc: 'AI validates all release criteria and makes pass/hold/rollback decision automatically. Human review only for AI-flagged high-risk releases (<10% of cases).',
      },
    ],
  },
  {
    id: 7,
    name: 'Monitoring & Feedback',
    subtitle: 'Autonomous AIOps',
    activities: [
      {
        id: 'b-p7-1', name: 'AI AIOps: APM + Logs + Auto-Resolution',
        type: 'agent', role: 'AI APM + AI Log Analyzer + IncidentAgent', agent: 'AI APM (Davis AI)',
        processTime: 0, waitTime: 0,
        desc: 'AI continuously monitors all signals and auto-resolves 80%+ of incidents without human intervention. P1 incidents escalated to on-call SRE.',
      },
      {
        id: 'b-p7-2', name: 'AI Product Intelligence Loop',
        type: 'agent', role: 'FeedbackAgent → auto-creates backlog items', agent: 'FeedbackAgent',
        processTime: 0.2, waitTime: 0,
        desc: 'AI synthesises customer feedback, usage patterns, and error trends into ranked backlog items. Feeds directly back to Phase 1 pipeline.',
      },
    ],
  },
]

// ─── OPTION C — ADLC / AI-Driven Lifecycle (85%+ automation, BMAD approach) ──
// Phases renamed as AI capabilities. Only 2 human roles:
//   Product Definer: sets vision, outcomes, strategic intent
//   Product Builder: supervises agent orchestration, exception handling, production approval
//
// Near-zero wait time (no human queues).
// Flow efficiency ~62% (vs 8.1% current).
// PT ≈ 8h (mostly human oversight), WT ≈ 5h (pipeline processing only).
// This is the destination state — where the industry is heading 2026–2028.

export const OPTION_C_PHASES = [
  {
    id: 1,
    name: 'Intent & Outcome Definition',
    subtitle: 'ADLC Phase 1 — Product Definer',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p1-1', name: 'Product Vision + OKR Definition',
        type: 'human', role: 'Product Definer', agent: null,
        processTime: 2, waitTime: 0,
        desc: 'Product Definer articulates desired outcomes, success metrics (OKRs), and constraints in natural language. This is the sole human creative input that drives the entire ADLC pipeline.',
      },
      {
        id: 'c-p1-2', name: 'AI: Epic → Feature → Story → BDD Pipeline',
        type: 'agent', role: 'FeatureGen + ScenarioGen + StoryGen Agents', agent: 'FeatureGen Agent',
        processTime: 0.1, waitTime: 0,
        desc: 'Agent pipeline automatically decomposes vision into epics, features, user stories, and Gherkin BDD scenarios. Full backlog ready in under 10 minutes.',
      },
    ],
  },
  {
    id: 2,
    name: 'Autonomous Architecture & Design',
    subtitle: 'ADLC Phase 2 — Agent-Led',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p2-1', name: 'AI: Architecture + API + UI Design Generation',
        type: 'agent', role: 'AI Architecture Advisor + DesignDoc Agent + DesignGen Agent', agent: 'AI Architecture Advisor',
        processTime: 0.2, waitTime: 0,
        desc: 'Agents simultaneously generate: system architecture, API contracts (OpenAPI spec), UI wireframes and hi-fi designs. All output deposited to knowledge base for downstream agents.',
      },
      {
        id: 'c-p2-2', name: 'Product Builder: Design Review + Approve',
        type: 'oversight', role: 'Product Builder (15-minute review)', agent: null,
        processTime: 0.25, waitTime: 0.5,
        desc: 'Product Builder reviews AI-generated design artefacts for strategic alignment. Approves or redirects with natural language feedback. Target: <15 minutes review time.',
      },
    ],
  },
  {
    id: 3,
    name: 'Agentic Code Generation',
    subtitle: 'ADLC Phase 3 — CodeGen Agents',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p3-1', name: 'AI: Full Feature Implementation',
        type: 'agent', role: 'CodeGen Agent (full autonomous coding)', agent: 'CodeGen Agent',
        processTime: 0.5, waitTime: 0,
        desc: 'CodeGen agent writes complete feature implementation from API contracts and user stories. Includes all layers: API, business logic, persistence, and frontend components.',
      },
      {
        id: 'c-p3-2', name: 'AI: Test Suite + Quality Gate',
        type: 'agent', role: 'TestGen Agent + AI Code Quality Tools + AI SAST Tools', agent: 'TestGen Agent',
        processTime: 0.1, waitTime: 0,
        desc: 'Agents generate unit, integration, and contract tests concurrently with code generation. Quality and security gates run automatically. Coverage target: 90%+.',
      },
      {
        id: 'c-p3-3', name: 'AI: Autonomous PR Review + Merge',
        type: 'agent', role: 'ReviewAgent (auto-merge on gate pass)', agent: 'ReviewAgent',
        processTime: 0, waitTime: 0.2,
        desc: 'ReviewAgent validates code against architectural contracts and security policies. Auto-merges if all gates pass. Only flags violations requiring Product Builder attention.',
      },
    ],
  },
  {
    id: 4,
    name: 'Autonomous Integration Pipeline',
    subtitle: 'ADLC Phase 4 — Self-Healing CI',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p4-1', name: 'AI: Build + Security + Artifact (Parallel)',
        type: 'agent', role: 'AI Build Optimizer + AI SAST Tools + AI Artifact Manager', agent: 'AI Build Optimizer',
        processTime: 0.1, waitTime: 0.3,
        desc: 'Build, security scan, and artifact creation run in parallel. Build pipeline is self-healing — agents auto-fix common failures (dependency conflicts, flaky tests) without human intervention.',
      },
      {
        id: 'c-p4-2', name: 'AI: DEV Auto-Deploy + Validation',
        type: 'agent', role: 'AI Deployment Agent', agent: 'AI Deployment Agent',
        processTime: 0.1, waitTime: 0.2,
        desc: 'AI provisions DEV environment, deploys artifact, and validates health checks automatically. Zero human touch. Failed deployments trigger automated root cause analysis.',
      },
    ],
  },
  {
    id: 5,
    name: 'Continuous Quality Intelligence',
    subtitle: 'ADLC Phase 5 — Autonomous QA',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p5-1', name: 'AI: Environment + Synthetic Data (Auto)',
        type: 'agent', role: 'AI Environment Manager + DataGen Agent', agent: 'AI Environment Manager',
        processTime: 0.1, waitTime: 0.1,
        desc: 'Test environment and synthetic PII-safe data provisioned automatically in parallel. Environment ready in <5 minutes. No manual configuration required.',
      },
      {
        id: 'c-p5-2', name: 'AI: Full Test Suite (All Types Parallel)',
        type: 'agent', role: 'AI Test Execution + AI Performance Analyzer + AI DAST Tools', agent: 'AI Test Execution',
        processTime: 0.3, waitTime: 0.5,
        desc: 'All test types (regression, performance, security, accessibility) execute in parallel across cloud grid. AI generates consolidated pass/fail with confidence score and risk assessment.',
      },
      {
        id: 'c-p5-3', name: 'AI: Quality Gate Decision',
        type: 'agent', role: 'AI UAT Assistant (autonomous pass/hold decision)', agent: 'AI UAT Assistant',
        processTime: 0, waitTime: 0.2,
        desc: 'AI makes autonomous deploy/hold decision based on quality gate thresholds. Decision includes risk score, test coverage delta, and compliance evidence. No human UAT review required.',
      },
      {
        id: 'c-p5-4', name: 'Product Builder: Exception Oversight',
        type: 'oversight', role: 'Product Builder (only if AI flags exception)', agent: null,
        processTime: 0.1, waitTime: 0.3,
        desc: 'Product Builder reviews only AI-flagged quality exceptions (typically <5% of deployments). Reviews AI evidence report and approves or redirects. Target: <10 minute review.',
      },
    ],
  },
  {
    id: 6,
    name: 'Zero-Touch Delivery',
    subtitle: 'ADLC Phase 6 — Autonomous Deploy',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p6-1', name: 'AI: IaC + Stage + Canary Deploy (Pipeline)',
        type: 'agent', role: 'IaC Agent + AI Deployment Agent + AI Production Deploy', agent: 'IaC Agent',
        processTime: 0.2, waitTime: 0.5,
        desc: 'Agents generate IaC, deploy to staging, execute smoke tests, and initiate canary production deployment in a single automated pipeline. Human not in loop until production approval gate.',
      },
      {
        id: 'c-p6-2', name: 'Product Builder: Production Approval',
        type: 'oversight', role: 'Product Builder (sole production gate)', agent: null,
        processTime: 0.2, waitTime: 1,
        desc: 'The single mandatory human gate in ADLC. Product Builder reviews AI deployment report (canary metrics, risk score, rollback plan) and approves production promotion. Target: <20 minute review.',
      },
      {
        id: 'c-p6-3', name: 'AI: Release Notes + Stakeholder Comms',
        type: 'agent', role: 'ReleaseNotes Agent', agent: 'ReleaseNotes Agent',
        processTime: 0, waitTime: 0,
        desc: 'AI auto-generates audience-specific release notes (technical, business, executive) and triggers stakeholder notifications. Zero human time required.',
      },
    ],
  },
  {
    id: 7,
    name: 'AIOps & Continuous Learning',
    subtitle: 'ADLC Phase 7 — Autonomous Intelligence',
    adlcPhase: true,
    activities: [
      {
        id: 'c-p7-1', name: 'AI: Autonomous AIOps (24/7)',
        type: 'agent', role: 'AI APM + AI Log Analyzer + IncidentAgent (continuous)', agent: 'AI APM (Davis AI)',
        processTime: 0, waitTime: 0,
        desc: 'AI continuously monitors all production signals, auto-resolves 90%+ of incidents, performs root cause analysis, and executes remediation runbooks — all without human intervention.',
      },
      {
        id: 'c-p7-2', name: 'AI: Feedback → Backlog Intelligence Loop',
        type: 'agent', role: 'FeedbackAgent → FeatureGen Agent (auto-backlog)', agent: 'FeedbackAgent',
        processTime: 0.1, waitTime: 0,
        desc: 'AI synthesises user feedback, usage telemetry, and incident patterns into new feature opportunities. Automatically creates and prioritises backlog items, feeding into the next ADLC iteration.',
      },
    ],
  },
]

// ─── Phase metric summaries (pre-calculated for UI) ──────────────────────────
function summarisePhases(phases) {
  return phases.map(ph => {
    const totalPT = ph.activities.reduce((s, a) => s + a.processTime, 0)
    const totalWT = ph.activities.reduce((s, a) => s + a.waitTime, 0)
    const fe = totalPT + totalWT > 0 ? (totalPT / (totalPT + totalWT)) * 100 : 100
    const agentCount = ph.activities.filter(a => a.type === 'agent' || a.type === 'hybrid').length
    return {
      id: ph.id,
      name: ph.name,
      subtitle: ph.subtitle,
      adlcPhase: ph.adlcPhase || false,
      processTime: +totalPT.toFixed(1),
      waitTime: +totalWT.toFixed(1),
      flowEfficiency: +fe.toFixed(1),
      activityCount: ph.activities.length,
      agentCount,
      activities: ph.activities,
    }
  })
}

export const OPTION_A_SUMMARY = summarisePhases(OPTION_A_PHASES)
export const OPTION_B_SUMMARY = summarisePhases(OPTION_B_PHASES)
export const OPTION_C_SUMMARY = summarisePhases(OPTION_C_PHASES)

export const FUTURE_PHASE_MAP = {
  'option-a': OPTION_A_SUMMARY,
  'option-b': OPTION_B_SUMMARY,
  'option-c': OPTION_C_SUMMARY,
}

// Totals for each option (used in comparison)
export function getOptionTotals(optionId) {
  const phases = FUTURE_PHASE_MAP[optionId]
  if (!phases) return null
  const totalPT = phases.reduce((s, p) => s + p.processTime, 0)
  const totalWT = phases.reduce((s, p) => s + p.waitTime, 0)
  const totalActivities = phases.reduce((s, p) => s + p.activityCount, 0)
  const agentActivities = phases.reduce((s, p) => s + p.agentCount, 0)
  const fe = totalPT + totalWT > 0 ? (totalPT / (totalPT + totalWT)) * 100 : 100
  const lt = (totalPT + totalWT) / 8  // working days
  return {
    processTime: +totalPT.toFixed(1),
    waitTime: +totalWT.toFixed(1),
    flowEfficiency: +fe.toFixed(1),
    leadTime: +lt.toFixed(1),
    totalActivities,
    agentActivities,
  }
}
