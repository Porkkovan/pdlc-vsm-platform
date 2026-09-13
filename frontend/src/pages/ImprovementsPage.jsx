import { useState } from 'react'
import { useApp } from '../contexts/AppContext'
import { PDLC_PHASES } from '../data/pdlcPhases'
import { agentsApi } from '../services/api'
import { Link } from 'react-router-dom'
import { IMPROVEMENTS_TO_BOTTLENECKS } from '../data/bottleneckCatalogue'
import StepReviewBar from '../components/StepReviewBar'
import InlineEditModal from '../components/common/InlineEditModal'

const DEFAULT_IMPROVEMENTS = [
  // ── Phase 1: Backlog & Roadmap ──────────────────────────────────────────────
  {
    id: 'imp-1a', phaseId: 1, phaseName: 'Backlog & Roadmap', activity: 'Feature Definition & Refinement',
    priority: 'High', title: 'FeatureGen Agent — AI Feature Authoring',
    problem: '4–8 hrs effort + 1–3 day PM/BA iteration cycles to reach shippable acceptance criteria',
    improvement: 'FeatureGen Agent generates structured feature definitions with ACs from high-level intent, using product personas via RAG. Reduces PM iteration from days to 30 minutes.',
    agent: 'FeatureGen Agent', type: 'GenAI Agent',
    expectedPTReduction: 50, expectedWTReduction: 70, category: 'GenAI Agent', timeToValue: '2–4 weeks', roi: '3.5×', effort: 'Low'
  },
  {
    id: 'imp-1b', phaseId: 1, phaseName: 'Backlog & Roadmap', activity: 'Epic Decomposition & Story Splitting',
    priority: 'Medium', title: 'AI Story Splitter — Epic-to-Sprint Decomposition',
    problem: '2–4 hrs per epic to split into sprint-ready stories; inconsistent vertical slicing quality across POs',
    improvement: 'AI Story Splitter decomposes epics into vertically-sliced, independently-deliverable stories using INVEST criteria. Consistent quality, 80% time saved on decomposition.',
    agent: 'AI Story Splitter', type: 'GenAI Agent',
    expectedPTReduction: 45, expectedWTReduction: 30, category: 'GenAI Agent', timeToValue: '2–3 weeks', roi: '3.2×', effort: 'Low'
  },
  {
    id: 'imp-1c', phaseId: 1, phaseName: 'Backlog & Roadmap', activity: 'Sprint Planning & Velocity Forecasting',
    priority: 'Medium', title: 'Sprint Velocity Predictor — AI Capacity Planning',
    problem: '1–3 day manual sprint planning; velocity estimates inaccurate by 30–40% with no historical regression analysis',
    improvement: 'Velocity Predictor analyses 12-sprint rolling history, team capacity, and ticket complexity to forecast sprint throughput with 85%+ accuracy. Reduces planning ceremony time by 50%.',
    agent: 'Velocity Predictor', type: 'AI Automation',
    expectedPTReduction: 30, expectedWTReduction: 40, category: 'AI Automation', timeToValue: '3–5 weeks', roi: '2.8×', effort: 'Low'
  },
  {
    id: 'imp-1d', phaseId: 1, phaseName: 'Backlog & Roadmap', activity: 'Dependency Mapping',
    priority: 'Low', title: 'AI Dependency Mapper — Cross-Team Risk Surfacing',
    problem: '8–24 hrs per PI planning cycle to manually identify cross-team dependencies; blockers discovered late in sprint',
    improvement: 'AI Dependency Mapper analyses Jira tickets across teams, identifies hidden dependencies via NLP, and auto-links related work. Reduces mid-sprint blockers by 60%.',
    agent: 'AI Dependency Mapper', type: 'AI Automation',
    expectedPTReduction: 0, expectedWTReduction: 55, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '2.2×', effort: 'Medium'
  },
  // ── Phase 2: Architecture & UX ─────────────────────────────────────────────
  {
    id: 'imp-2a', phaseId: 2, phaseName: 'Architecture & UX', activity: 'Architecture Decision Records (ADRs)',
    priority: 'High', title: 'AI Architecture Reviewer — ADR Quality Gate',
    problem: '4–8 hrs per ADR for review cycles; architecture risks identified post-implementation due to limited senior review bandwidth',
    improvement: 'AI Architecture Reviewer analyses proposed ADRs against existing patterns, flags risks, suggests alternatives, and generates structured feedback in < 5 minutes. Architect focuses on strategic trade-offs only.',
    agent: 'AI Architecture Reviewer', type: 'GenAI Agent',
    expectedPTReduction: 35, expectedWTReduction: 60, category: 'GenAI Agent', timeToValue: '3–4 weeks', roi: '3.0×', effort: 'Medium'
  },
  {
    id: 'imp-2b', phaseId: 2, phaseName: 'Architecture & UX', activity: 'UX Prototyping & Design Review',
    priority: 'Medium', title: 'UX Prototype Generator — AI-Assisted Design Iteration',
    problem: '3–5 day cycles between design intent and low-fidelity prototypes; designers overwhelmed with iteration requests',
    improvement: 'UX Prototype Generator creates clickable Figma-compatible wireframes from natural language specs and user personas. Reduces design cycle from 3 days to same-day for initial concepts.',
    agent: 'UX Prototype Generator', type: 'GenAI Agent',
    expectedPTReduction: 50, expectedWTReduction: 65, category: 'GenAI Agent', timeToValue: '4–6 weeks', roi: '3.3×', effort: 'Medium'
  },
  {
    id: 'imp-2c', phaseId: 2, phaseName: 'Architecture & UX', activity: 'API Design & Contract Definition',
    priority: 'Medium', title: 'API Contract Generator — OpenAPI Spec from Intent',
    problem: '4–8 hrs per API design; contract mismatches between teams discovered during integration testing, causing 1–2 week rework',
    improvement: 'API Contract Generator creates validated OpenAPI 3.0 specs from endpoint intent descriptions, enforces naming conventions, and detects breaking changes vs existing contracts automatically.',
    agent: 'API Contract Generator', type: 'GenAI Agent',
    expectedPTReduction: 60, expectedWTReduction: 40, category: 'GenAI Agent', timeToValue: '2–3 weeks', roi: '4.0×', effort: 'Low'
  },
  {
    id: 'imp-2d', phaseId: 2, phaseName: 'Architecture & UX', activity: 'Design Review & Accessibility Compliance',
    priority: 'Medium', title: 'Design Review Agent — AI-Powered Design Quality Gate',
    problem: '4–8 hrs manual design review per release; accessibility violations (WCAG AA) and brand drift discovered late in QA or post-release',
    improvement: 'Design Review Agent (← Figma AI) scans Figma designs against WCAG AA, brand guidelines, and design system tokens automatically. Flags violations with fix suggestions before dev handoff. Reduces manual review from 4–8 hrs to 30 min exception review.',
    agent: 'Design Review Agent', type: 'GenAI Agent',
    expectedPTReduction: 60, expectedWTReduction: 70, category: 'GenAI Agent', timeToValue: '3–5 weeks', roi: '2.8×', effort: 'Medium'
  },
  // ── Phase 3: Code Management ───────────────────────────────────────────────
  {
    id: 'imp-3a', phaseId: 3, phaseName: 'Code Management', activity: 'Coding (Feature Development)',
    priority: 'High', title: 'CodeGen Agent — AI-Assisted Development',
    problem: '8–32 hrs effort; boilerplate, context-switching overhead, and documentation lag slow feature throughput',
    improvement: 'Deploy GitHub Copilot/CodeGen Agent for real-time suggestions, boilerplate generation, refactoring, and inline documentation. Reduces development effort by 30–40% on typical features.',
    agent: 'CodeGen Agent', type: 'GenAI Agent',
    expectedPTReduction: 35, expectedWTReduction: 0, category: 'GenAI Agent', timeToValue: '1–2 weeks', roi: '4.5×', effort: 'Low'
  },
  {
    id: 'imp-3b', phaseId: 3, phaseName: 'Code Management', activity: 'Peer Code Review',
    priority: 'High', title: 'ReviewAgent — AI-Augmented Code Review',
    problem: '4–24 hr wait for reviewer availability; inconsistent review quality; reviewers spend 70% of time on style/formatting',
    improvement: 'ReviewAgent instantly analyses diffs, flags bugs/security/style issues, and produces structured review summaries. Human reviewer focuses on architecture and business logic. Reduces review wait from 24hrs to 30 mins.',
    agent: 'ReviewAgent', type: 'GenAI Agent',
    expectedPTReduction: 40, expectedWTReduction: 70, category: 'GenAI Agent', timeToValue: '2–3 weeks', roi: '5.0×', effort: 'Low'
  },
  {
    id: 'imp-3c', phaseId: 3, phaseName: 'Code Management', activity: 'Technical Debt Management',
    priority: 'Medium', title: 'Tech Debt Prioritiser — AI-Scored Remediation Queue',
    problem: '8–16 hrs/quarter to manually assess and prioritise technical debt backlog; debt grows faster than it is addressed',
    improvement: 'Tech Debt Prioritiser continuously scans codebase, scores debt items by business impact and refactor cost, and auto-populates a ranked remediation queue in Jira. Reduces assessment effort by 75%.',
    agent: 'Tech Debt Prioritiser', type: 'AI Automation',
    expectedPTReduction: 20, expectedWTReduction: 0, category: 'AI Automation', timeToValue: '3–5 weeks', roi: '2.5×', effort: 'Medium'
  },
  {
    id: 'imp-3d', phaseId: 3, phaseName: 'Code Management', activity: 'Merge Conflict Resolution',
    priority: 'Low', title: 'AI Merge Conflict Resolver — Intent-Aware Resolution',
    problem: '2–8 hrs per major merge conflict; developers context-switch from feature work to resolve conflicts manually',
    improvement: 'AI Merge Conflict Resolver analyses both branches intent, suggests semantically-correct resolution, and flags unresolvable conflicts for human review. Reduces resolution time by 70% on common patterns.',
    agent: 'AI Merge Resolver', type: 'AI Automation',
    expectedPTReduction: 25, expectedWTReduction: 15, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '2.0×', effort: 'Low'
  },
  // ── Phase 4: Continuous Integration ───────────────────────────────────────
  {
    id: 'imp-4a', phaseId: 4, phaseName: 'Continuous Integration', activity: 'Static Code Analysis (SAST)',
    priority: 'High', title: 'ML-Powered SAST — Fewer False Positives',
    problem: '1–4 hr wait; high false-positive rate (60%+) forces manual triaging and desensitises teams to real vulnerabilities',
    improvement: 'Upgrade to ML-powered SAST (Snyk/Semgrep) that contextually prioritises vulnerabilities and auto-suggests fixes. Reduces triaging overhead by 60%; real vulnerabilities actioned same-day.',
    agent: 'AI SAST Tools', type: 'AI Automation',
    expectedPTReduction: 40, expectedWTReduction: 60, category: 'AI Automation', timeToValue: '3–4 weeks', roi: '2.5×', effort: 'Medium'
  },
  {
    id: 'imp-4b', phaseId: 4, phaseName: 'Continuous Integration', activity: 'Build Failure Diagnostics',
    priority: 'High', title: 'AI Build Failure Diagnostics — Root Cause in Seconds',
    problem: '30 min–2 hrs per flaky/failing build to diagnose root cause; developers blocked while CI queues clear',
    improvement: 'AI Build Diagnostics analyses CI logs, correlates failures with recent code changes, and produces root-cause summaries with fix suggestions in < 30 seconds. Unblocks developers immediately.',
    agent: 'AI Build Diagnostics', type: 'AI Automation',
    expectedPTReduction: 55, expectedWTReduction: 30, category: 'AI Automation', timeToValue: '2–3 weeks', roi: '3.8×', effort: 'Low'
  },
  {
    id: 'imp-4c', phaseId: 4, phaseName: 'Continuous Integration', activity: 'Dependency & Vulnerability Management',
    priority: 'Medium', title: 'Dependency Vulnerability Auto-Fixer',
    problem: '4–16 hrs/sprint on dependency updates; security vulnerabilities in transitive dependencies go unpatched for weeks',
    improvement: 'AI Dependency Manager (Dependabot + LLM) auto-generates fix PRs for vulnerable dependencies, tests compatibility, and flags breaking changes. Keeps dependency tree clean without manual effort.',
    agent: 'Dependency Auto-Fixer', type: 'AI Automation',
    expectedPTReduction: 60, expectedWTReduction: 40, category: 'AI Automation', timeToValue: '1–2 weeks', roi: '3.0×', effort: 'Low'
  },
  {
    id: 'imp-4d', phaseId: 4, phaseName: 'Continuous Integration', activity: 'CI Pipeline Orchestration & Optimisation',
    priority: 'Medium', title: 'Pipeline Agent — Intelligent CI Orchestration',
    problem: '40–90 min CI pipeline runs; sequential stage execution; no intelligent test selection or parallelisation; build logs too noisy to action quickly',
    improvement: 'Pipeline Agent (← Log Analytics) analyses historical pipeline data to parallelise stages, select only relevant tests per change, detect flaky tests, and surface root-cause summaries from build logs. Cuts average CI time by 40–60%.',
    agent: 'Pipeline Agent', type: 'AI Automation',
    expectedPTReduction: 50, expectedWTReduction: 35, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '3.2×', effort: 'Medium'
  },
  // ── Phase 5: Continuous Testing ────────────────────────────────────────────
  {
    id: 'imp-5a', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Automated Performance Testing',
    priority: 'High', title: 'AI Performance Analyzer — Regression Detection',
    problem: '16–40 hrs effort; manual performance test authoring and analysis; regressions often missed until production',
    improvement: 'AI Performance Analyzer auto-detects regressions, correlates metrics with code changes, and suggests root-cause optimisations. Reduces effort to 4–8 hrs; catches regressions at PR stage.',
    agent: 'AI Performance Analyzer', type: 'AI Automation',
    expectedPTReduction: 75, expectedWTReduction: 60, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '3.2×', effort: 'Medium'
  },
  {
    id: 'imp-5b', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Manual SIT / UAT / NF Signoff',
    priority: 'High', title: 'AI UAT Assistant + Risk-Based Signoff',
    problem: '2–5 day wait for human UAT approval; manual test consolidation across multiple testers and environments',
    improvement: 'AI UAT Assistant auto-consolidates results, generates risk-scored readiness reports, enabling same-day signoff with exception-only human review. Reduces UAT cycle from 5 days to 4 hours.',
    agent: 'AI UAT Assistant', type: 'AI Automation',
    expectedPTReduction: 50, expectedWTReduction: 80, category: 'AI Automation', timeToValue: '6–8 weeks', roi: '4.1×', effort: 'High'
  },
  {
    id: 'imp-5c', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Test Data Generation / Management',
    priority: 'High', title: 'DataGen Agent — Synthetic Test Data on Demand',
    problem: '4–16 hr wait for test data provisioning; privacy/compliance risk with prod data copies in lower environments',
    improvement: 'DataGen Agent generates privacy-compliant synthetic data on-demand from schema constraints. Eliminates provisioning queues and removes prod-data risk in lower environments permanently.',
    agent: 'DataGen Agent', type: 'GenAI Agent',
    expectedPTReduction: 60, expectedWTReduction: 85, category: 'GenAI Agent', timeToValue: '3–4 weeks', roi: '3.8×', effort: 'Low'
  },
  {
    id: 'imp-5d', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Visual / UI Regression Testing',
    priority: 'Medium', title: 'AI Visual Regression Tester — Pixel-Intelligent Comparison',
    problem: '4–8 hrs/sprint on manual UI review; pixel-diff tools generate 200+ false positives per release',
    improvement: 'AI Visual Regression Tester uses computer vision to distinguish intentional design changes from regressions. Reduces false positives by 90%; testers review only genuine anomalies.',
    agent: 'AI Visual Regression', type: 'AI Automation',
    expectedPTReduction: 55, expectedWTReduction: 40, category: 'AI Automation', timeToValue: '3–5 weeks', roi: '2.8×', effort: 'Low'
  },
  {
    id: 'imp-5e', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Contract / Integration Testing',
    priority: 'Medium', title: 'Contract Testing Agent — API Compatibility Verification',
    problem: '2–4 week integration test cycles; consumer-producer API mismatches discovered post-deployment causing production incidents',
    improvement: 'Contract Testing Agent (Pact + AI) auto-generates and validates consumer-driven contracts at PR stage. API incompatibilities surface in < 5 minutes; eliminates late-stage integration failures.',
    agent: 'Contract Testing Agent', type: 'AI Automation',
    expectedPTReduction: 35, expectedWTReduction: 70, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '3.5×', effort: 'Medium'
  },
  {
    id: 'imp-5f', phaseId: 5, phaseName: 'Continuous Testing', activity: 'Regression Suite Optimisation',
    priority: 'High', title: 'Regression Agent — AI-Optimised Test Selection & Execution',
    problem: '4–12 hr full regression suite runs per release; all tests executed regardless of change scope; high flaky test rate degrades suite reliability',
    improvement: 'Regression Agent (← USB Docs) uses ML to select the minimal high-confidence test subset for each code change, parallels execution, quarantines flaky tests, and generates a risk-scored regression report. Reduces regression cycle from 12 hrs to 90 min at equivalent coverage confidence.',
    agent: 'Regression Agent', type: 'AI Automation',
    expectedPTReduction: 70, expectedWTReduction: 55, category: 'AI Automation', timeToValue: '5–7 weeks', roi: '3.9×', effort: 'Medium'
  },
  // ── Phase 6: Continuous Delivery ──────────────────────────────────────────
  {
    id: 'imp-6a', phaseId: 6, phaseName: 'Continuous Delivery', activity: 'Release Gates / Approvals',
    priority: 'High', title: 'AI Release Manager — Automated Gate Validation',
    problem: '1–5 day wait for CAB approval; manual risk assessment repeated for every deployment regardless of change scope',
    improvement: 'AI Release Manager auto-validates all release criteria, generates risk assessments with compliance evidence. Only outlier changes go to CAB; continuous deployment enabled with automated guardrails.',
    agent: 'AI Release Manager', type: 'AI Automation',
    expectedPTReduction: 60, expectedWTReduction: 75, category: 'AI Automation', timeToValue: '6–10 weeks', roi: '2.9×', effort: 'High'
  },
  {
    id: 'imp-6b', phaseId: 6, phaseName: 'Continuous Delivery', activity: 'Canary & Blue-Green Deployment Analysis',
    priority: 'Medium', title: 'AI Canary Analyser — Intelligent Traffic Routing',
    problem: '2–4 hrs manual monitoring per canary deployment; engineers on-call overnight to watch error rates and manually roll back',
    improvement: 'AI Canary Analyser monitors golden signals in real-time, auto-rolls back on anomaly detection, and generates post-deployment confidence score. No overnight watch required.',
    agent: 'AI Canary Analyser', type: 'AI Automation',
    expectedPTReduction: 40, expectedWTReduction: 50, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '3.1×', effort: 'Medium'
  },
  {
    id: 'imp-6c', phaseId: 6, phaseName: 'Continuous Delivery', activity: 'Runbook & Operational Documentation',
    priority: 'Low', title: 'AI Runbook Generator — Auto-Maintained Ops Docs',
    problem: '8–24 hrs to write and maintain deployment runbooks; runbooks frequently outdated (60%+ staleness) causing incident delays',
    improvement: 'AI Runbook Generator auto-creates and updates runbooks from CI/CD pipeline definitions and deployment history. Always-current docs; reduces incident resolution time by 30%.',
    agent: 'AI Runbook Generator', type: 'GenAI Agent',
    expectedPTReduction: 0, expectedWTReduction: 20, category: 'GenAI Agent', timeToValue: '2–3 weeks', roi: '2.0×', effort: 'Low'
  },
  {
    id: 'imp-6d', phaseId: 6, phaseName: 'Continuous Delivery', activity: 'Automated Rollback & Recovery',
    priority: 'High', title: 'Rollback Agent — Autonomous Failure Recovery',
    problem: '15–45 min to detect, decide, and execute rollback manually; engineers under pressure make slow or incorrect rollback decisions; customer impact window extended',
    improvement: 'Rollback Agent (← Log Analytics) monitors golden signals post-deployment, compares against pre-deployment baselines, auto-triggers rollback when breach thresholds are met, and notifies teams with a deployment health report. Customer impact window shrinks from 30 min to < 5 min.',
    agent: 'Rollback Agent', type: 'AI Automation',
    expectedPTReduction: 0, expectedWTReduction: 80, category: 'AI Automation', timeToValue: '5–8 weeks', roi: '4.5×', effort: 'High'
  },
  // ── Phase 7: Operations & Monitoring ──────────────────────────────────────
  {
    id: 'imp-7a', phaseId: 7, phaseName: 'Operations & Monitoring', activity: 'Incident Detection & Alerting',
    priority: 'High', title: 'AIOps Anomaly Detector — Proactive Incident Prevention',
    problem: '15–45 min MTTD on production incidents; alert fatigue (200+ alerts/day) with <5% actionable; incidents often customer-reported',
    improvement: 'AIOps Anomaly Detector correlates metrics, logs, and traces to detect anomalies before they become incidents. MTTD drops from 30 mins to < 2 mins; noise-to-signal ratio drops from 200:5 to 10:8.',
    agent: 'AIOps Anomaly Detector', type: 'AI Automation',
    expectedPTReduction: 0, expectedWTReduction: 0, category: 'AI Automation', timeToValue: '6–8 weeks', roi: '5.5×', effort: 'High'
  },
  {
    id: 'imp-7b', phaseId: 7, phaseName: 'Operations & Monitoring', activity: 'Incident Triage & Response',
    priority: 'High', title: 'AI Incident Auto-Triage — Severity & Owner Assignment',
    problem: '20–60 min to triage and route incidents; on-call engineers spend 40% of incident time on diagnosis vs resolution',
    improvement: 'AI Incident Triage auto-classifies severity, identifies probable owner, pulls relevant runbook sections, and drafts initial customer communication. MTTR reduced by 45%; engineer focuses on resolution.',
    agent: 'AI Incident Triage', type: 'AI Automation',
    expectedPTReduction: 0, expectedWTReduction: 0, category: 'AI Automation', timeToValue: '4–6 weeks', roi: '4.2×', effort: 'Medium'
  },
  {
    id: 'imp-7c', phaseId: 7, phaseName: 'Operations & Monitoring', activity: 'Capacity Planning & Cost Optimisation',
    priority: 'Medium', title: 'AI Capacity Forecaster — Predictive Scaling',
    problem: '8–16 hrs/month manual capacity analysis; over-provisioning by 30–50% due to conservative estimates; cost spikes during events',
    improvement: 'AI Capacity Forecaster predicts traffic/load patterns 4 weeks ahead using historical data and business calendar events. Auto-scales proactively; reduces cloud spend by 20–35% through right-sizing.',
    agent: 'AI Capacity Forecaster', type: 'AI Automation',
    expectedPTReduction: 0, expectedWTReduction: 0, category: 'AI Automation', timeToValue: '6–10 weeks', roi: '3.0×', effort: 'High'
  },
  {
    id: 'imp-7d', phaseId: 7, phaseName: 'Operations & Monitoring', activity: 'Post-Incident Reviews & Learning',
    priority: 'Low', title: 'AI Post-Incident Report Generator',
    problem: '4–8 hrs per PIR to compile timeline, identify contributing factors, and draft remediation actions; PIRs often delayed or skipped',
    improvement: 'AI PIR Generator reconstructs incident timeline from logs/alerts, identifies contributing factors via causal analysis, and drafts structured blameless PIR report. PIR time from 8hrs to 45 minutes.',
    agent: 'AI PIR Generator', type: 'GenAI Agent',
    expectedPTReduction: 0, expectedWTReduction: 0, category: 'GenAI Agent', timeToValue: '3–4 weeks', roi: '2.3×', effort: 'Low'
  },
  {
    id: 'imp-7e', phaseId: 7, phaseName: 'Operations & Monitoring', activity: 'Continuous Compliance Monitoring',
    priority: 'Medium', title: 'Compliance Agent — Automated Regulatory & Policy Assurance',
    problem: '2–4 weeks manual audit prep per cycle; compliance evidence collected ad-hoc; policy drift discovered late during audits causing remediation sprints',
    improvement: 'Compliance Agent (← Risk Asst.) continuously monitors infrastructure, pipelines, and access controls against policy frameworks (SOC2, ISO27001, PCI-DSS). Auto-generates evidence packages for audits and flags policy drift in real time. Audit prep reduced from 3 weeks to < 1 day.',
    agent: 'Compliance Agent', type: 'AI Automation',
    expectedPTReduction: 0, expectedWTReduction: 0, category: 'AI Automation', timeToValue: '8–12 weeks', roi: '3.5×', effort: 'High'
  },
]

// Deterministic per-team improvement variance for illustrative differentiation
function impHash(teamName, id) {
  let h = 0
  const str = teamName + id
  for (let i = 0; i < str.length; i++) h = (Math.imul(h, 37) + str.charCodeAt(i)) & 0x7fffffff
  return h
}

const IMP_PRIORITIES = ['Low', 'Medium', 'High']

function applyImprovementVariance(improvements, teamName) {
  if (!teamName) return improvements
  return improvements.map(imp => {
    const h = impHash(teamName, imp.id)
    const idx = IMP_PRIORITIES.indexOf(imp.priority)
    const shift = (h % 5) - 2  // most stay same, some shift ±1
    const newIdx = Math.max(0, Math.min(2, idx + (Math.abs(shift) <= 1 ? shift : 0)))
    // Vary reduction percentages by ±10–20 points for realism
    const ptDelta = ((h >> 6) % 21) - 10
    const wtDelta = ((h >> 10) % 21) - 10
    return {
      ...imp,
      priority: IMP_PRIORITIES[newIdx],
      expectedPTReduction: Math.max(0, Math.min(90, (imp.expectedPTReduction || 0) + ptDelta)),
      expectedWTReduction: Math.max(0, Math.min(90, (imp.expectedWTReduction || 0) + wtDelta)),
    }
  })
}

const PRIORITY_STYLES = {
  High:   'border-l-red-500',
  Medium: 'border-l-orange-400',
  Low:    'border-l-blue-400'
}

const PRIORITY_GROUPS = [
  { priority: 'High',   icon: '🔴', header: 'bg-sky-50 border-sky-200',       text: 'text-sky-800'    },
  { priority: 'Medium', icon: '🟠', header: 'bg-teal-50 border-teal-200', text: 'text-teal-800' },
  { priority: 'Low',    icon: '🔵', header: 'bg-blue-50 border-blue-200',     text: 'text-blue-800'   },
]

function PriorityAccordion({ group, improvements, liveBottleneckById, onEdit }) {
  const [open, setOpen] = useState(true)
  const imps = improvements.filter(i => i.priority === group.priority)
  if (imps.length === 0) return null
  return (
    <div className="rounded-xl border overflow-hidden">
      <button
        onClick={() => setOpen(v => !v)}
        className={`w-full flex items-center justify-between px-5 py-3 border-b ${group.header} hover:opacity-90 transition-opacity`}
      >
        <div className="flex items-center gap-2">
          <span>{group.icon}</span>
          <span className={`font-bold text-sm ${group.text}`}>{group.priority} Priority Improvements</span>
          <div className="flex gap-1 ml-2">
            {PDLC_PHASES.map(p => {
              const c = imps.filter(i => (i.phaseId ?? i.phase_id) === p.id).length
              if (!c) return null
              return (
                <span key={p.id} className="text-[10px] bg-white/70 border border-gray-300 rounded px-1.5 py-0.5 text-gray-600 font-medium">
                  P{p.id}:{c}
                </span>
              )
            })}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">{imps.length} improvement{imps.length !== 1 ? 's' : ''}</span>
          <span className="text-gray-400 text-xs">{open ? '▲' : '▼'}</span>
        </div>
      </button>
      {open && (
        <div className="p-4 bg-white">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {imps.map(imp => (
              <ImprovementCard key={imp.id} imp={imp} liveBottleneckById={liveBottleneckById} onEdit={onEdit} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

const STAGE_BADGE = {
  'Stage 1 (Option A)': { bg: 'bg-blue-100 text-blue-800 border-blue-300',  dot: 'bg-blue-500',   short: 'Stage 1' },
  'Stage 2 (Option B)': { bg: 'bg-purple-100 text-purple-800 border-purple-300', dot: 'bg-purple-500', short: 'Stage 2' },
  'Stage 3 (Option C)': { bg: 'bg-emerald-100 text-emerald-800 border-emerald-300', dot: 'bg-emerald-500', short: 'Stage 3' },
}

function ImprovementCard({ imp, liveBottleneckById, onEdit }) {
  const [showStages, setShowStages] = useState(false)
  const stageBadge = imp.stage_available_from ? STAGE_BADGE[imp.stage_available_from] : null
  const hasStageData = !!(imp.stage_1_partial || imp.stage_2_full || imp.stage_3_autonomous)
  return (
    <div className={`card border-l-4 ${PRIORITY_STYLES[imp.priority]}`}>
      <div className="card-body space-y-3">
        <div className="flex items-start justify-between gap-2">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <div className="font-bold text-gray-800">{imp.title || imp.activity}</div>
              {onEdit && (
                <button onClick={() => onEdit(imp)} className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold px-1.5 py-0.5 rounded hover:bg-indigo-50" title="Edit improvement">
                  ✏️
                </button>
              )}
              {stageBadge && (
                <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold border ${stageBadge.bg}`}>
                  Available: {stageBadge.short}
                </span>
              )}
            </div>
            <div className="text-xs text-gray-500 mt-0.5">{imp.phase_name || imp.phaseName} · {imp.activity}</div>
            {imp.agent && <div className="text-xs text-violet-700 font-semibold mt-0.5">🤖 {imp.agent}</div>}
          </div>
          {imp.priority && (
            <span className={`px-2 py-0.5 rounded-full text-xs font-bold border shrink-0 ${
              imp.priority === 'High'   ? 'bg-sky-100 text-sky-700 border-sky-300' :
              imp.priority === 'Medium' ? 'bg-teal-100 text-teal-700 border-teal-300' :
                                          'bg-blue-100 text-blue-700 border-blue-300'
            }`}>{imp.priority}</span>
          )}
        </div>

        {imp.problem && (
          <div className="bg-sky-50 rounded p-3 text-xs border border-sky-100">
            <span className="font-semibold text-sky-700">Problem: </span>{imp.problem}
          </div>
        )}
        {(imp.improvement || imp.how_it_works) && (
          <div className="bg-green-50 rounded p-3 text-xs border border-green-100">
            <span className="font-semibold text-green-700">Improvement: </span>{imp.improvement || imp.how_it_works}
          </div>
        )}

        {/* Stage-by-stage progression (seeded data) */}
        {hasStageData && (
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => setShowStages(v => !v)}
              className="w-full flex items-center justify-between px-3 py-2 bg-gray-50 text-xs font-semibold text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <span>Stage-by-Stage Progression (1 → 2 → 3)</span>
              <span className="text-gray-400">{showStages ? '▲' : '▼'}</span>
            </button>
            {showStages && (
              <div className="divide-y divide-gray-100">
                {imp.stage_1_partial && (
                  <div className="px-3 py-2.5 text-xs">
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className="w-2 h-2 rounded-full bg-blue-500 shrink-0" />
                      <span className="font-bold text-blue-700">Stage 1 (Option A) — AI-Enabled Tools</span>
                    </div>
                    <p className="text-gray-600 ml-3.5">{imp.stage_1_partial}</p>
                  </div>
                )}
                {imp.stage_2_full && (
                  <div className="px-3 py-2.5 text-xs bg-purple-50/30">
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className="w-2 h-2 rounded-full bg-purple-500 shrink-0" />
                      <span className="font-bold text-purple-700">Stage 2 (Option B) — 21 Agents Orchestrated</span>
                    </div>
                    <p className="text-gray-600 ml-3.5">{imp.stage_2_full}</p>
                  </div>
                )}
                {imp.stage_3_autonomous && (
                  <div className="px-3 py-2.5 text-xs bg-emerald-50/30">
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
                      <span className="font-bold text-emerald-700">Stage 3 (Option C) — STUMP Platform Autonomous</span>
                    </div>
                    <p className="text-gray-600 ml-3.5">{imp.stage_3_autonomous}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-3 gap-2 text-xs">
          <div className="bg-gray-50 rounded p-2 text-center">
            <div className="font-bold text-blue-600">
              {imp.effort_reduction_pct ? `-${imp.effort_reduction_pct}%` : (imp.expectedPTReduction > 0 ? `-${imp.expectedPTReduction}%` : '—')}
            </div>
            <div className="text-gray-500">Effort Reduction</div>
          </div>
          <div className="bg-gray-50 rounded p-2 text-center">
            <div className="font-bold text-sky-600">
              {imp.wait_reduction_pct ? `-${imp.wait_reduction_pct}%` : (imp.expectedWTReduction > 0 ? `-${imp.expectedWTReduction}%` : '—')}
            </div>
            <div className="text-gray-500">Wait Reduction</div>
          </div>
          <div className="bg-gray-50 rounded p-2 text-center">
            <div className="font-bold text-green-600">{imp.roi_estimate || imp.roi || '—'}</div>
            <div className="text-gray-500">Est. ROI</div>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 text-xs">
          {imp.tools?.length > 0 && imp.tools.map(t => (
            <span key={t} className="tag-ai">{t}</span>
          ))}
          {(!imp.tools || imp.tools.length === 0) && imp.agent && (
            <span className="tag-agent">{imp.agent}</span>
          )}
          {imp.implementation_weeks && (
            <span className="tag-process">⏱ {imp.implementation_weeks}w</span>
          )}
          {imp.timeToValue && <span className="tag-process">⏱ {imp.timeToValue}</span>}
          {imp.complexity && (
            <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${
              imp.complexity === 'Low'    ? 'bg-green-100 text-green-700 border-green-300' :
              imp.complexity === 'High'   ? 'bg-sky-100 text-sky-700 border-sky-300' :
                                            'bg-yellow-100 text-yellow-700 border-yellow-300'
            }`}>{imp.complexity} complexity</span>
          )}
          {imp.effort && (
            <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${
              imp.effort === 'Low'  ? 'bg-green-100 text-green-700 border-green-300' :
              imp.effort === 'High' ? 'bg-sky-100 text-sky-700 border-sky-300' :
                                      'bg-yellow-100 text-yellow-700 border-yellow-300'
            }`}>{imp.effort} effort</span>
          )}
          {imp.target_system && (
            <span className="bg-gray-100 text-gray-600 border border-gray-200 px-2 py-0.5 rounded text-xs">{imp.target_system}</span>
          )}
        </div>

        {/* Bottleneck cross-reference */}
        {(() => {
          const liveBn = imp.bottleneckId ? liveBottleneckById[imp.bottleneckId] : null
          const bnIds = imp.addresses_bottlenecks || []
          const liveBns = bnIds.map(id => liveBottleneckById[id]).filter(Boolean)
          const staticBns = !liveBn ? (IMPROVEMENTS_TO_BOTTLENECKS[imp.id] || []) : []
          const bns = liveBns.length > 0 ? liveBns : (liveBn ? [liveBn] : staticBns)
          return bns.map(bn => (
            <Link key={bn.id} to="/bottlenecks"
              className="flex items-center gap-1.5 text-xs text-sky-700 font-medium bg-sky-50 border border-sky-200 rounded-lg px-3 py-1.5 hover:bg-sky-100 transition-colors">
              <span className={`w-2 h-2 rounded-full shrink-0 ${
                bn.severity === 'critical' || bn.severity === 'Critical' ? 'bg-sky-600' :
                bn.severity === 'high' || bn.severity === 'High'         ? 'bg-teal-500' :
                bn.severity === 'medium' || bn.severity === 'Medium'     ? 'bg-yellow-500' : 'bg-blue-400'
              }`} />
              <span>Addresses bottleneck:</span>
              <span className="font-bold truncate">{bn.activity}</span>
            </Link>
          ))
        })()}
      </div>
    </div>
  )
}

const IMP_EDIT_FIELDS = [
  { key: 'priority', label: 'Priority', type: 'select', options: ['Low', 'Medium', 'High'] },
  { key: 'title', label: 'Title', type: 'text' },
  { key: 'problem', label: 'Problem Description', type: 'textarea', rows: 3 },
  { key: 'improvement', label: 'Improvement Description', type: 'textarea', rows: 3 },
  { key: 'expectedPTReduction', label: 'Expected PT Reduction (%)', type: 'number', min: 0, max: 100 },
  { key: 'expectedWTReduction', label: 'Expected WT Reduction (%)', type: 'number', min: 0, max: 100 },
  { key: 'roi', label: 'Estimated ROI (e.g. 3.5x)', type: 'text' },
  { key: 'agent', label: 'Agent / Tool Name', type: 'text' },
]

export default function ImprovementsPage() {
  const { analysisResult, addNotification, project } = useApp()
  const [running, setRunning] = useState(false)
  const [viewMode, setViewMode] = useState('phase')   // 'phase' | 'priority'
  const [filter, setFilter] = useState('all')
  const [phaseFilter, setPhaseFilter] = useState('all')
  const [editingImp, setEditingImp] = useState(null)
  const [impEdits, setImpEdits] = useState({})

  const saveImpEdit = (updated) => {
    setImpEdits(prev => ({ ...prev, [updated.id]: updated }))
    addNotification(`Improvement "${updated.title || updated.activity}" updated`, 'success')
  }

  const applyImpEdits = (imps) => imps.map(i => impEdits[i.id] ? { ...i, ...impEdits[i.id] } : i)

  const improvements = applyImpEdits(applyImprovementVariance(
    analysisResult?.improvements ?? DEFAULT_IMPROVEMENTS,
    project.team
  ))

  const liveBottleneckById = Object.fromEntries(
    (analysisResult?.bottlenecks ?? []).map(b => [b.id, b])
  )

  const filtered = improvements.filter(imp => {
    const pid = imp.phaseId ?? imp.phase_id
    return (
      (filter === 'all' || imp.priority === filter) &&
      (phaseFilter === 'all' || pid === parseInt(phaseFilter))
    )
  })

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runImprovementGen(project.id || 'demo')
      addNotification('Improvement generation complete!', 'success')
    } catch {
      addNotification('Using built-in improvement catalogue (demo mode)', 'info')
    } finally { setRunning(false) }
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Improvement Actions</h2>
            <p className="text-green-100">AI-generated improvements across all 7 PDLC phases — GenAI agents, AI automation, and process optimisations with ROI estimates</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-green-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-green-50 shadow">
            {running ? '⏳ Generating...' : '🤖 Run Improvement Agent'}
          </button>
        </div>
      </div>

      <StepReviewBar stepKey="improvements" stepLabel="Improvement Actions" />

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Improvements', value: improvements.length,                                             color: 'green'  },
          { label: 'Stage 1 Available',  value: improvements.filter(i => (i.stage_available_from || '').includes('Stage 1')).length, color: 'blue'   },
          { label: 'Stage 2 Available',  value: improvements.filter(i => (i.stage_available_from || '').includes('Stage 2')).length, color: 'purple' },
          { label: 'Stage 3 Available',  value: improvements.filter(i => (i.stage_available_from || '').includes('Stage 3')).length, color: 'emerald' }
        ].map(s => (
          <div key={s.label} className="card card-body text-center">
            <div className={`text-3xl font-bold text-${s.color}-600`}>{s.value}</div>
            <div className="text-xs text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* View toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-gray-500">View by:</span>
        <button
          onClick={() => setViewMode('phase')}
          className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            viewMode === 'phase' ? 'bg-blue-600 text-white shadow' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          📋 PDLC Phase
        </button>
        <button
          onClick={() => { setViewMode('priority'); setPhaseFilter('all'); setFilter('all') }}
          className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            viewMode === 'priority' ? 'bg-green-600 text-white shadow' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          🔴 Priority
        </button>
      </div>

      {/* ── PDLC Phase View: original filters + cards ── */}
      {viewMode === 'phase' && (
        <>
          {/* Filters */}
          <div className="bg-white p-4 rounded-xl border border-gray-200 space-y-3">
            {/* PDLC Phase filter */}
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 mr-1">PDLC Phase:</span>
              <button
                onClick={() => setPhaseFilter('all')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                  phaseFilter === 'all' ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}>
                All Phases
              </button>
              {PDLC_PHASES.map(p => {
                const count = improvements.filter(i => (i.phaseId ?? i.phase_id) === p.id).length
                const isActive = phaseFilter === String(p.id)
                return (
                  <button
                    key={p.id}
                    onClick={() => setPhaseFilter(isActive ? 'all' : String(p.id))}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 ${
                      isActive
                        ? 'bg-green-600 text-white'
                        : 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100'
                    }`}>
                    <span>P{p.id} {p.name.split(' ')[0]}</span>
                    <span className={`rounded-full px-1.5 text-[10px] font-bold ${isActive ? 'bg-white/30' : 'bg-green-200'}`}>
                      {count}
                    </span>
                  </button>
                )
              })}
            </div>

            {/* Priority filter */}
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 mr-1">Priority:</span>
              {['all','High','Medium','Low'].map(f => (
                <button key={f} onClick={() => setFilter(f)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                    filter === f ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}>
                  {f === 'all' ? `All (${improvements.length})` : `${f} (${improvements.filter(i => i.priority === f).length})`}
                </button>
              ))}
              <span className="text-xs text-gray-400 ml-auto">{filtered.length} of {improvements.length} shown</span>
            </div>
          </div>

          {/* Phase activity breakdown — shown when a phase is selected */}
          {phaseFilter !== 'all' && (() => {
            const phase = PDLC_PHASES.find(p => p.id === parseInt(phaseFilter))
            if (!phase) return null
            const phaseImps = improvements.filter(i => (i.phaseId ?? i.phase_id) === phase.id)
            const coveredActivities = new Set(phaseImps.map(i => i.activity))
            return (
              <div className="bg-white rounded-xl border border-green-200 overflow-hidden">
                <div className="bg-green-50 px-5 py-3 border-b border-green-100 flex items-center justify-between">
                  <div>
                    <span className="font-bold text-green-800">Phase {phase.id}: {phase.name}</span>
                    <span className="ml-3 text-xs text-green-600">
                      {phase.activities.length} activities · {phaseImps.length} improvement{phaseImps.length !== 1 ? 's' : ''}
                    </span>
                  </div>
                  <button onClick={() => setPhaseFilter('all')} className="text-xs text-green-500 hover:text-green-700">✕ Clear</button>
                </div>
                <div className="px-5 py-3">
                  <div className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Activities in this phase</div>
                  <div className="flex flex-wrap gap-2">
                    {phase.activities.map(act => {
                      const hasImp = coveredActivities.has(act.name)
                      const imp = phaseImps.find(i => i.activity === act.name)
                      return (
                        <span key={act.id} className={`text-xs px-2.5 py-1 rounded-full border font-medium flex items-center gap-1 ${
                          hasImp
                            ? 'bg-green-50 text-green-700 border-green-300'
                            : 'bg-gray-50 text-gray-500 border-gray-200'
                        }`}>
                          {hasImp ? '✓' : '·'} {act.name}
                          {imp && (
                            <span className={`ml-1 text-[10px] px-1 rounded font-bold ${
                              imp.priority === 'High'   ? 'bg-sky-100 text-sky-700' :
                              imp.priority === 'Medium' ? 'bg-teal-100 text-teal-700' :
                                                          'bg-blue-100 text-blue-700'
                            }`}>{imp.priority}</span>
                          )}
                        </span>
                      )
                    })}
                  </div>
                </div>
              </div>
            )
          })()}

          {/* Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {filtered.map(imp => (
              <ImprovementCard key={imp.id} imp={imp} liveBottleneckById={liveBottleneckById} onEdit={setEditingImp} />
            ))}
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-12 text-gray-400">
              <div className="text-4xl mb-3">🔍</div>
              <div className="font-medium">No improvements match the current filters</div>
            </div>
          )}
        </>
      )}

      {/* ── Priority View: accordion per priority, ALL improvements ── */}
      {viewMode === 'priority' && (
        <div className="space-y-4">
          <div className="text-xs text-gray-500 px-1">
            Showing all {improvements.length} improvements grouped by priority across all PDLC phases
          </div>
          {PRIORITY_GROUPS.map(group => (
            <PriorityAccordion
              key={group.priority}
              group={group}
              improvements={improvements}
              liveBottleneckById={liveBottleneckById}
              onEdit={setEditingImp}
            />
          ))}
        </div>
      )}

      <div className="flex gap-4">
        <Link to="/future-state" className="btn-primary flex-1 text-center py-3">🔮 Design Future State →</Link>
        <Link to="/bottlenecks"  className="btn-secondary flex-1 text-center py-3">← Bottlenecks</Link>
      </div>

      <InlineEditModal
        item={editingImp}
        fields={IMP_EDIT_FIELDS}
        title={editingImp ? `Edit: ${editingImp.title || editingImp.activity}` : 'Edit Improvement'}
        onSave={saveImpEdit}
        onClose={() => setEditingImp(null)}
      />

      {Object.keys(impEdits).length > 0 && (
        <div className="fixed bottom-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg text-xs font-semibold z-40">
          ✏️ {Object.keys(impEdits).length} improvement{Object.keys(impEdits).length !== 1 ? 's' : ''} edited (session)
        </div>
      )}
    </div>
  )
}
