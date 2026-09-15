import { useState, useEffect, useCallback } from 'react'
import { useApp } from '../contexts/AppContext'
import { FUTURE_STATE_SCENARIOS } from '../data/pdlcPhases'
import { getOptionTotals } from '../data/futureStatePhases'
import { agentsApi, projectsApi, targetStateApi } from '../services/api'
import { Link } from 'react-router-dom'
import { LANE_STYLE, PHASE_COLOR, TRANSFORMATION_ROADMAP } from '../data/transformationRoadmap'
import { STATIC_AGENT_CATALOG } from '../data/agentCatalog'
import ADLCGrid from '../components/ADLCGrid'
import { seedAdlcAgents } from '../data/adlcTargetState'
import { OPERATING_MODEL, resolveAgentParent, DEFAULT_AGENT_PARENT_MAP } from '../data/operatingModel'
import CostModelEditor from '../components/CostModelEditor'
import TargetStateBanner from '../components/TargetStateBanner'
import StepReviewBar from '../components/StepReviewBar'

// ─── Playbook Action Enrichment ──────────────────────────────────────────────
// Splits a platform phasing "focus" paragraph into individual actions and enriches
// each with who, description, how-to steps, tools, and success criteria based on
// keyword matching.  Keeps content platform-aware by injecting the platform name.
const ACTION_ENRICHMENT = [
  { match: /hire|transfer|recruit/i, who: 'Engineering Lead',
    desc: 'Identify and onboard the right talent — internal transfers or external hires — to fill critical platform roles.',
    how: '1. Define role requirements and JDs for each position.\n2. Check internal talent pool first — identify engineers with adjacent AI/ML experience.\n3. Post external roles with 2-week hiring sprint timeline.\n4. Run technical interview focused on agent orchestration, LLM evaluation, prompt engineering.\n5. Onboard with 1-week platform bootcamp.',
    tools: 'HR system, LinkedIn Recruiter, Internal talent marketplace', success: 'All positions filled and onboarded within the phase timeline' },
  { match: /stand up.*team|build.*team|form.*team/i, who: 'Engineering Lead',
    desc: 'Assemble the AI Platform Engineering team with clear roles, reporting lines, and sprint cadence.',
    how: '1. Define team charter: mission, scope, SLAs, escalation path.\n2. Assign roles: Platform Lead, LLM Engineers, SREs, Prompt Engineers.\n3. Set up team Slack channel, Jira board, and weekly sync cadence.\n4. Create team working agreement (code review policy, on-call rotation, deployment authority).\n5. Establish Day-1 priorities and first sprint backlog.',
    tools: 'Jira/ADO, Slack/Teams, Confluence', success: 'Team operational with sprint cadence, working agreement, and first backlog prioritised' },
  { match: /LangGraph|orchestrat|infra/i, who: 'Platform Engineer',
    desc: 'Provision the foundational infrastructure for agent orchestration, including LLM endpoints, vector stores, and observability.',
    how: '1. Provision Azure OpenAI (or chosen LLM provider) endpoints — GPT-4o for complex agents, GPT-4o-mini for routine.\n2. Deploy LangGraph runtime on Kubernetes (AKS/EKS) with auto-scaling.\n3. Set up pgvector or Weaviate as the knowledge store.\n4. Deploy observability stack: Langfuse / LangSmith for agent tracing.\n5. Configure CI/CD for agent code (GitHub Actions / ADO Pipelines).\n6. Run smoke tests on each component.',
    tools: 'Azure OpenAI, LangGraph, Kubernetes, pgvector, Langfuse', success: 'Infrastructure provisioned, smoke tests passing, agents deployable via CI/CD' },
  { match: /first.*agent|build.*agent|high.impact/i, who: 'LLM Engineer',
    desc: 'Build and deploy the first batch of high-impact agents in shadow mode to validate the platform without disrupting existing workflows.',
    how: '1. Prioritise agents by PDLC phase impact: Code Generator, Code Reviewer, QA Orchestrator, Release Gate, Monitor.\n2. Implement each agent using LangGraph StateGraph with structured input/output schemas.\n3. Wire MCP tool integrations (source control, CI/CD, ALM).\n4. Deploy in shadow mode — agents run alongside humans but don\'t block workflows.\n5. Build evaluation suite: golden datasets per agent, acceptance rate tracking.\n6. Run for 2 weeks minimum before moving to next phase.',
    tools: 'LangGraph, MCP Tools, Evaluation framework', success: 'First 5 agents running in shadow mode with >80% acceptance rate on golden datasets' },
  { match: /shadow mode|remaining.*agent|progressive/i, who: 'Platform Team',
    desc: 'Expand agent coverage across all PDLC phases while running in shadow mode to build confidence before promotion.',
    how: '1. Add agents in priority order (highest wait-time reduction first).\n2. Each agent follows: build → unit test → shadow deploy → 1-week evaluation → review.\n3. Wire inter-agent context sharing via shared state store.\n4. Implement drift detection: monitor output quality scores daily.\n5. Build rollback procedures for each agent.\n6. Run weekly agent performance review with team.',
    tools: 'LangGraph, Agent evaluation suite, Drift detection', success: 'All agents deployed in shadow mode, evaluation scores tracked, rollback tested' },
  { match: /MCP.*tool|evaluation|drift/i, who: 'Platform Engineer',
    desc: 'Connect agents to production tools and establish quality guardrails with evaluation and drift detection.',
    how: '1. Configure MCP tool connections: source control (GitHub/ADO), CI/CD, ALM (Jira), monitoring.\n2. Build evaluation suite with golden test cases per agent.\n3. Set up automated drift detection — alert when acceptance rate drops below threshold.\n4. Create agent performance dashboard showing quality scores, latency, cost per invocation.',
    tools: 'MCP, GitHub/ADO API, Evaluation framework, Grafana/Datadog', success: 'All tools connected, evaluation running on schedule, drift alerts configured' },
  { match: /Product Definer|Product Builder|role/i, who: 'Transformation Lead',
    desc: 'Define the new human roles that will operate alongside agents — Product Definer (outcomes) and Product Builder (oversight).',
    how: '1. Draft role descriptions: Product Definer (sets outcome briefs, acceptance criteria, approves final output) and Product Builder (monitors agent orchestration, tunes prompts, handles exceptions).\n2. Map existing roles to new roles — identify who transitions to which.\n3. Design 4-week reskilling curriculum per role.\n4. Run role definition workshops with affected team members.\n5. Begin parallel-run: team operates in both old and new role structures for 2–4 weeks.',
    tools: 'HR system, Training platform, Workshop materials', success: 'Role definitions published, reskilling curriculum designed, parallel-run started' },
  { match: /promote|primary|cutover/i, who: 'Platform Lead',
    desc: 'Transition agents from shadow to primary — they become the default for their PDLC activities, with humans in oversight.',
    how: '1. Rank agents by risk: promote lowest-risk first (CI/CD, monitoring, then code, design).\n2. For each agent: announce cutover date → run 1-week "primary with veto" mode → review acceptance rate → confirm or rollback.\n3. Update team workflows and ceremonies to reflect agent-primary operation.\n4. Keep human override authority active — any team member can pause an agent.\n5. Daily standup includes agent health check for first 2 weeks post-promotion.',
    tools: 'Agent orchestration platform, Team communication', success: 'Agents promoted to primary one phase at a time, acceptance rates maintained' },
  { match: /workforce|transition|resk/i, who: 'HR / Transformation Lead',
    desc: 'Execute the people transition plan — reskilling, role changes, and redeployment alongside agent promotion.',
    how: '1. Communicate transition timeline and support resources to all affected team members.\n2. Begin reskilling programmes: 3–4 weeks per person, role-specific curriculum.\n3. Run parallel operation: old and new roles active simultaneously.\n4. Gradual handover: reduce old role responsibilities as agent takes over.\n5. Support redeployment for roles that are fully absorbed by agents.\n6. Monthly check-in with every affected individual.',
    tools: 'HR system, Training platform, Reskilling materials', success: 'All affected individuals transitioned with reskilling complete, no involuntary disruption' },
  { match: /governance|council/i, who: 'Product Owner / Governance Lead',
    desc: 'Establish the AI Governance Council to oversee agent performance, ethics, compliance, and continuous improvement.',
    how: '1. Charter the council: membership (PO, Tech Lead, Compliance, Security), cadence (monthly), decision authority.\n2. Define governance KPIs: agent acceptance rate, override rate, compliance incidents, cost per transaction.\n3. Create governance dashboard (pull from agent telemetry).\n4. Run first governance review: inspect agent decisions, review overrides, validate compliance evidence.\n5. Publish governance report template for monthly cadence.',
    tools: 'Governance dashboard, Agent telemetry, Compliance tools', success: 'Governance Council operational, monthly reviews running, KPIs tracked' },
  { match: /autonomous|steady.state|all.*agent/i, who: 'Platform Team',
    desc: 'Operate in steady-state — all agents running autonomously across the full PDLC with continuous improvement.',
    how: '1. Confirm all agents at target acceptance rate (>90%).\n2. Establish monthly Agent Performance Review cadence.\n3. Activate cost optimisation loop: model tiering, caching, batch API.\n4. Run quarterly model evaluation — test newer models against current performance.\n5. Document full platform runbook for team replication.',
    tools: 'Agent platform, Cost dashboard, Model evaluation pipeline', success: 'All agents autonomous, monthly reviews running, cost optimised, runbook documented' },
  { match: /monthly.*review|performance.*review/i, who: 'Platform Lead',
    desc: 'Run regular agent performance reviews to catch degradation early and drive continuous improvement.',
    how: '1. Pull agent metrics: acceptance rate, latency, cost, override frequency, error rate.\n2. Compare to previous period — flag any >5% degradation.\n3. Review override logs — understand why humans intervened.\n4. Prioritise tuning actions: prompt updates, model swaps, tool configuration.\n5. Update agent evaluation datasets with new edge cases found.',
    tools: 'Agent telemetry dashboard, Evaluation suite', success: 'Performance review completed monthly, improvement actions tracked and closed' },
  { match: /cost.*optim|evaluation.*pipeline|model.*drift/i, who: 'Platform Engineer',
    desc: 'Continuously optimise agent costs and detect model drift before it impacts quality.',
    how: '1. Implement model tiering: route simple tasks to cheaper models (GPT-4o-mini), complex to GPT-4o.\n2. Enable semantic caching for repeated queries (30–50% cost reduction).\n3. Deploy automated drift detection — compare agent output quality daily against golden datasets.\n4. Set up alerting: quality score < threshold triggers investigation.\n5. Quarterly model swap evaluation: test newer/cheaper models.',
    tools: 'LLM gateway, Semantic cache, Drift detection, Cost dashboard', success: 'Cost reduced 30%+ from baseline, drift detected within 24h, no quality regression' },
  { match: /subscri|provision|environment|sign/i, who: 'Platform Admin',
    desc: 'Procure the platform subscription and provision the environment — cloud or on-premise as required.',
    how: '1. Complete procurement: sign subscription agreement, confirm SLA and data residency terms.\n2. Provision platform environment (cloud or licensed on-prem).\n3. Configure SSO/SAML integration for team access.\n4. Verify network connectivity: platform ↔ source control, CI/CD, ALM.\n5. Run platform health checks and confirm all services operational.',
    tools: 'Platform admin console, SSO provider, Network config', success: 'Platform provisioned, SSO live, all connectivity verified, health checks passing' },
  { match: /connect|integration|source control|CI.CD|ALM/i, who: 'Platform Admin',
    desc: 'Connect the platform to the organisation\'s existing toolchain — source control, CI/CD, ALM, and observability.',
    how: '1. Configure source control integration (GitHub / ADO / GitLab) — webhook + API token.\n2. Connect CI/CD pipeline (GitHub Actions / Jenkins / ADO Pipelines).\n3. Integrate ALM tool (Jira / ADO Boards) — bidirectional sync.\n4. Connect observability stack (Datadog / Dynatrace / Grafana).\n5. Run end-to-end integration test: trigger agent → verify tool actions.',
    tools: 'Source control, CI/CD, ALM, Observability APIs', success: 'All integrations live, end-to-end test passing, bidirectional sync confirmed' },
  { match: /configur|policy|threshold|compliance/i, who: 'Policy Engineer',
    desc: 'Configure platform agents with organisation-specific policies, quality thresholds, and compliance frameworks.',
    how: '1. Define policy thresholds: code quality minimums, security severity gates, test coverage targets.\n2. Configure compliance frameworks: SOC2, ISO27001, PCI-DSS as applicable.\n3. Set override authority levels: who can override which agent decisions.\n4. Configure code style guides and naming conventions.\n5. Validate configuration with test runs against sample repositories.',
    tools: 'Platform config UI, Compliance frameworks, Sample repos', success: 'All policies configured, compliance frameworks active, test validation passing' },
  { match: /BMAD|framework|methodology|pattern/i, who: 'BMAD Practitioner',
    desc: 'Adopt and customise the BMAD framework methodology for the organisation\'s agent development practices.',
    how: '1. Complete BMAD framework training for the platform team.\n2. Review BMAD agent pattern library — select patterns for each PDLC phase.\n3. Customise patterns to organisation context (domain language, tech stack, compliance requirements).\n4. Set up BMAD pattern repository with version control.\n5. Author first agent using BMAD pattern — validate the workflow.',
    tools: 'BMAD framework, Pattern library, Version control', success: 'Team trained, patterns customised, first agent authored and validated using BMAD' },
  { match: /open.source|observability|Langfuse|LangSmith/i, who: 'SRE / Platform Engineer',
    desc: 'Deploy the open-source observability stack for agent monitoring, tracing, and performance visibility.',
    how: '1. Deploy Langfuse or LangSmith for agent execution tracing.\n2. Configure trace collection for all agent invocations.\n3. Build dashboards: latency, cost, quality scores, error rates per agent.\n4. Set up alerting rules: latency P95 > threshold, error rate > 5%.\n5. Integrate with existing org monitoring (Grafana / Datadog).',
    tools: 'Langfuse/LangSmith, Grafana, Alerting system', success: 'All agents traced, dashboards live, alerting configured' },
]

function enrichPlaybookActions(focusText, platformName, phaseName) {
  return focusText.split(/\.\s+/).filter(s => s.trim()).map(sentence => {
    const title = sentence.trim().replace(/\.$/, '')
    const match = ACTION_ENRICHMENT.find(e => e.match.test(title))
    const pn = platformName || 'the platform'
    return {
      who: match?.who || 'Team',
      what: title + '.',
      description: match?.desc?.replace(/the platform/gi, pn) || '',
      how: match?.how?.replace(/the platform/gi, pn) || '',
      tools: match?.tools || '',
      success: match?.success || '',
    }
  })
}

// ─── Roles & Skills Evolution by AI Maturity Level ──────────────────────────
const ROLES_EVOLUTION = {
  1: {
    label: 'L1 — Assisted Prompting',
    fluencyLevel: 'AI-Aware',
    fluencyDesc: 'Basic understanding of AI concepts and terminology. Aware of how AI can enhance business processes.',
    teamStructure: 'Traditional pyramid — 10 humans, manual execution, no agents',
    roles: [
      { id: 'dev', name: 'Developer', count: 3, type: 'traditional',
        competencies: ['Full-stack development', 'Code review', 'Unit testing', 'Basic AI awareness'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' },
                     { course: 'GitHub Copilot Basics', hours: 2, format: 'Workshop' }] },
      { id: 'qa', name: 'QA Engineer', count: 2, type: 'traditional',
        competencies: ['Manual testing', 'Test automation basics', 'Defect management'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' },
                     { course: 'AI-Assisted Test Generation', hours: 3, format: 'Workshop' }] },
      { id: 'devops', name: 'DevOps Engineer', count: 1, type: 'traditional',
        competencies: ['CI/CD pipelines', 'Infrastructure as Code', 'Monitoring'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' },
                     { course: 'AI Pipeline Tools Overview', hours: 4, format: 'Workshop' }] },
      { id: 'ba', name: 'Business Analyst', count: 1, type: 'traditional',
        competencies: ['Requirements gathering', 'Story writing', 'Stakeholder management'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' }] },
      { id: 'sm', name: 'Scrum Master', count: 1, type: 'traditional',
        competencies: ['Agile ceremonies', 'Sprint planning', 'Impediment removal'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' }] },
      { id: 'arch', name: 'Solution Architect', count: 1, type: 'traditional',
        competencies: ['Solution design', 'Technology selection', 'Architecture governance'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' },
                     { course: 'AI Architecture Patterns', hours: 4, format: 'Workshop' }] },
      { id: 'support', name: 'App Support Analyst', count: 1, type: 'traditional',
        competencies: ['Incident triage', 'L1/L2 resolution', 'SLA management'],
        upskilling: [{ course: 'AI Fundamentals & Awareness', hours: 4, format: 'Async online' }] },
    ],
    agents: { count: 0, types: [], description: 'No AI agents — humans do all work; AI limited to basic IDE suggestions' },
  },
  2: {
    label: 'L2 — Agent Co-pilots',
    fluencyLevel: 'AI-Practitioner',
    fluencyDesc: 'Moderate proficiency applying AI tools and techniques to everyday delivery tasks. Identifies specific use cases where AI adds value.',
    teamStructure: 'Augmented pyramid — 9 humans with AI co-pilot tools across most phases',
    roles: [
      { id: 'dev', name: 'Developer', count: 3, type: 'traditional',
        competencies: ['Full-stack development', 'AI-assisted coding (Copilot)', 'Prompt engineering basics', 'AI output review'],
        upskilling: [{ course: 'GitHub Copilot Advanced', hours: 8, format: 'Workshop' },
                     { course: 'Prompt Engineering for Developers', hours: 6, format: 'Online + Lab' },
                     { course: 'AI Code Review Best Practices', hours: 4, format: 'Workshop' }] },
      { id: 'qa', name: 'QA Engineer', count: 2, type: 'traditional',
        competencies: ['AI-assisted test generation', 'Synthetic data management', 'AI output validation'],
        upskilling: [{ course: 'AI Test Generation Tools', hours: 8, format: 'Workshop' },
                     { course: 'DataGen & Synthetic Data', hours: 6, format: 'Online + Lab' }] },
      { id: 'devops', name: 'DevOps Engineer', count: 1, type: 'traditional',
        competencies: ['AI-enhanced CI/CD', 'ML-based SAST integration', 'Agent monitoring basics'],
        upskilling: [{ course: 'AI Pipeline Integration', hours: 8, format: 'Workshop' },
                     { course: 'Agent Monitoring & Observability', hours: 6, format: 'Online' }] },
      { id: 'ba', name: 'Business Analyst', count: 1, type: 'traditional',
        competencies: ['AI-assisted requirements', 'Intent writing for FeatureGen', 'AI output review'],
        upskilling: [{ course: 'FeatureGen Intent Writing', hours: 4, format: 'Workshop' },
                     { course: 'AI Story Review', hours: 2, format: 'Workshop' }] },
      { id: 'sm', name: 'Scrum Master', count: 1, type: 'evolving',
        competencies: ['AI-augmented ceremonies', 'AI velocity forecasting', 'Team AI adoption coaching'],
        upskilling: [{ course: 'AI Metrics & Dashboards', hours: 4, format: 'Workshop' },
                     { course: 'AI Ceremonies Guide', hours: 2, format: 'Online' }] },
      { id: 'arch', name: 'Solution Architect', count: 1, type: 'traditional',
        competencies: ['AI solution architecture', 'Agent design patterns', 'AI governance basics'],
        upskilling: [{ course: 'Agent Architecture Patterns', hours: 8, format: 'Workshop' },
                     { course: 'AI Governance Fundamentals', hours: 4, format: 'Online' }] },
    ],
    agents: { count: 5, types: ['Code Assistant', 'Test Assistant', 'CI/CD Assistant', 'Doc Generator', 'Review Assistant'],
              description: 'AI co-pilots assist in 5 phases — all outputs reviewed by humans before acceptance' },
  },
  3: {
    label: 'L3 — Supervised Independent',
    fluencyLevel: 'AI-Advanced User',
    fluencyDesc: 'Skilled in leveraging AI tools and platforms to solve complex problems. Guides implementation of AI in workflows.',
    teamStructure: 'Inverted pyramid emerging — 6 Frontier humans + 12 independent agents',
    roles: [
      { id: 'fae', name: 'Frontier AI Engineer (FAE)', count: 2, type: 'frontier',
        absorbs: ['Developer', 'QA Engineer', 'DevOps Engineer'],
        competencies: ['Requirements Extraction', 'Solution Architecture', 'Full-Stack Development', 'Data Pipeline Engineering',
                       'Quality & Compliance', 'CI/CD & DevSecOps', 'AI Prompt Orchestration', 'Stakeholder Engagement'],
        toolchain: ['GitHub Copilot', 'Claude', 'GiGi', 'Databricks Ginie'],
        typicalDay: { 'Judgment': 30, 'AI Orchestration': 25, 'Code Review': 20, 'Stakeholders': 15, 'Compliance': 10 },
        upskilling: [{ course: 'FAE Certification Program', hours: 80, format: '4-week intensive' },
                     { course: 'Multi-Agent Orchestration', hours: 24, format: 'Workshop series' },
                     { course: 'Advanced Prompt Engineering', hours: 16, format: 'Online + Lab' }] },
      { id: 'fbo', name: 'Frontier Business Operator (FBO)', count: 1, type: 'frontier',
        absorbs: ['Project Manager', 'Scrum Master', 'Business Analyst'],
        competencies: ['Backlog Ownership', 'Stakeholder Management', 'AI Output Validation', 'Domain Translation',
                       'Change Management', 'Value Realization', 'Sprint Analytics', 'Compliance'],
        toolchain: ['Lovable', 'Copilot for Office', 'Power BI + Copilot'],
        typicalDay: { 'Stakeholders': 35, 'AI Validation': 25, 'Backlog Mgmt': 20, 'Metrics': 10, 'Change': 10 },
        upskilling: [{ course: 'FBO Certification Program', hours: 60, format: '3-week intensive' },
                     { course: 'AI Output Validation & Governance', hours: 16, format: 'Workshop' },
                     { course: 'Change Management for AI Transformation', hours: 12, format: 'Online' }] },
      { id: 'fsa', name: 'Frontier Super Architect (FSA)', count: 1, type: 'frontier',
        absorbs: ['Product Owner', 'Solution Architect'],
        competencies: ['Domain / Tribe Leadership', 'AI Strategy', 'Architecture Governance', 'Cross-functional Orchestration',
                       'Regulated Domain Expertise', 'Platform Mastery + AI Fluency'],
        typicalDay: { 'Architecture': 30, 'Domain Governance': 25, 'AI Strategy': 20, 'Stakeholders': 15, 'Compliance': 10 },
        upskilling: [{ course: 'FSA Certification Program', hours: 60, format: '3-week intensive' },
                     { course: 'Agentic Architecture Mastery', hours: 24, format: 'Workshop series' }] },
      { id: 'fpe', name: 'Frontier Platform Engineer (FPE)', count: 1, type: 'frontier',
        absorbs: ['Platform Engineering', 'Platform Ops Engineer'],
        competencies: ['Platform Configuration', 'Platform Standardisation', 'Ops', 'Incident Diagnosis', 'Remediation'],
        upskilling: [{ course: 'FPE Certification Program', hours: 40, format: '2-week intensive' },
                     { course: 'AI Platform Operations', hours: 16, format: 'Workshop' }] },
      { id: 'fse', name: 'Frontier Support Engineer (FSE)', count: 1, type: 'frontier',
        absorbs: ['App Support Analyst', 'L2/L3 Support Engineer'],
        competencies: ['Reliability', 'Platform Ops', 'Incident Diagnosis', 'Remediation', 'Service Optimisation', 'Observability'],
        upskilling: [{ course: 'FSE Certification Program', hours: 40, format: '2-week intensive' },
                     { course: 'AIOps & Self-Healing Systems', hours: 16, format: 'Workshop' }] },
    ],
    agents: { count: 12, types: ['Code Generator', 'Code Reviewer', 'QA Orchestrator', 'DataGen', 'Release Gate',
                                  'CI/CD Agent', 'SAST Agent', 'Monitor Agent', 'FeatureGen', 'StoryGen',
                                  'Doc Generator', 'Compliance Agent'],
              description: 'Independent agents handle standard cases; humans review exceptions and quality gates' },
  },
  4: {
    label: 'L4 — Orchestrated Agents',
    fluencyLevel: 'AI-Champion',
    fluencyDesc: 'Mastery in integrating AI strategically across business units. Drives innovation and shapes enterprise-wide AI transformation.',
    teamStructure: 'Inverted pyramid — 4-5 Frontier humans govern 18 orchestrated agents',
    roles: [
      { id: 'fae', name: 'Frontier AI Engineer (FAE)', count: 2, type: 'frontier',
        absorbs: ['Developer', 'QA Engineer', 'DevOps Engineer', 'BA', 'Solution Architect'],
        competencies: ['Requirements Extraction', 'Solution Architecture', 'Full-Stack Development', 'Data Pipeline Engineering',
                       'Quality & Compliance', 'CI/CD & DevSecOps', 'AI Prompt Orchestration', 'Stakeholder Engagement'],
        toolchain: ['GitHub Copilot', 'Claude', 'GiGi', 'Databricks Ginie', 'C3.ai', 'n8n', 'th!nk.ai', 'Glean.ai'],
        typicalDay: { 'Judgment': 30, 'AI Orchestration': 25, 'Code Review': 20, 'Stakeholders': 15, 'Compliance': 10 },
        upskilling: [{ course: 'Advanced Multi-Agent Orchestration', hours: 40, format: 'Intensive workshop' },
                     { course: 'Agent Fleet Management', hours: 24, format: 'Online + Lab' }] },
      { id: 'fbo', name: 'Frontier Business Operator (FBO)', count: 1, type: 'frontier',
        absorbs: ['Project Manager', 'Scrum Master', 'Delivery Lead', 'Release Train Engineer', 'Business Analyst'],
        competencies: ['Backlog Ownership', 'Stakeholder Management', 'AI Output Validation', 'Domain Translation',
                       'Change Management', 'Value Realization', 'Sprint Analytics', 'Compliance'],
        toolchain: ['Lovable', 'Copilot for Office', 'Power BI + Copilot', 'Writer.AI'],
        typicalDay: { 'Stakeholders': 35, 'AI Validation': 25, 'Backlog Mgmt': 20, 'Metrics': 10, 'Change': 10 },
        upskilling: [{ course: 'Enterprise AI Governance', hours: 24, format: 'Workshop' },
                     { course: 'Outcome-Based Product Management', hours: 16, format: 'Online' }] },
      { id: 'fsa', name: 'Frontier Super Architect (FSA)', count: 1, type: 'frontier',
        absorbs: ['Product Owner', 'Solution Architect'],
        competencies: ['Domain / Tribe Leadership', 'AI Strategy', 'Architecture Governance', 'Cross-functional Orchestration',
                       'Regulated Domain Expertise', 'Platform Mastery + AI Fluency'],
        typicalDay: { 'Architecture': 30, 'Domain Governance': 25, 'AI Strategy': 20, 'Stakeholders': 15, 'Compliance': 10 },
        upskilling: [{ course: 'Enterprise AI Architecture', hours: 32, format: 'Workshop series' }] },
      { id: 'fse', name: 'Frontier Support Engineer (FSE)', count: 1, type: 'frontier',
        absorbs: ['App Support Analyst', 'L2/L3 Support Engineer', 'Platform Ops Engineer'],
        competencies: ['Reliability', 'Platform Ops', 'Incident Diagnosis', 'Remediation', 'Service Optimisation', 'Observability'],
        upskilling: [{ course: 'Advanced AIOps & Autonomous Operations', hours: 24, format: 'Workshop' }] },
    ],
    agents: { count: 18, types: ['Code Generator', 'Code Reviewer', 'QA Orchestrator', 'DataGen', 'Release Gate',
                                  'CI/CD Agent', 'SAST Agent', 'DAST Agent', 'Monitor Agent', 'Triage Agent',
                                  'FeatureGen', 'StoryGen', 'Doc Generator', 'Compliance Agent', 'MRM Agent',
                                  'Secure-by-Design', 'Governance Controller', 'Deployment Agent'],
              description: 'Multi-agent orchestration end-to-end; humans provide oversight and handle escalations' },
  },
  5: {
    label: 'L5 — Autonomous ADLC',
    fluencyLevel: 'AI-Champion+',
    fluencyDesc: 'Beyond mastery — shapes AI strategy at enterprise level. Defines how AI and humans co-evolve.',
    teamStructure: 'Fully inverted — 3 humans govern 21 autonomous agents across full PDLC',
    roles: [
      { id: 'pd', name: 'Product Definer (evolved FBO)', count: 1, type: 'frontier',
        absorbs: ['All business / operations roles'],
        competencies: ['Outcome Definition', 'Strategic Prioritisation', 'AI Fleet Governance', 'Business Value Realisation',
                       'Stakeholder Alignment', 'Compliance Oversight'],
        typicalDay: { 'Outcome Briefs': 30, 'Agent Output Review': 25, 'Stakeholders': 25, 'Governance': 20 },
        upskilling: [{ course: 'Product Definer Mastery', hours: 40, format: '2-week intensive' },
                     { course: 'AI Fleet Governance for Leaders', hours: 16, format: 'Online' }] },
      { id: 'pb', name: 'Product Builder (evolved FAE)', count: 1, type: 'frontier',
        absorbs: ['All technical / engineering roles'],
        competencies: ['Agent Orchestration Mastery', 'Exception Handling', 'Agent Performance Tuning',
                       'Quality Gate Management', 'Platform Reliability', 'Continuous Improvement'],
        typicalDay: { 'Agent Ops Dashboard': 30, 'Exception Queue': 25, 'Tuning & Improvement': 25, 'Compliance': 20 },
        upskilling: [{ course: 'Product Builder Mastery', hours: 40, format: '2-week intensive' },
                     { course: 'Agent Fleet Operations', hours: 24, format: 'Workshop' }] },
      { id: 'sa', name: 'Super Architect (evolved FSA)', count: 1, type: 'frontier',
        absorbs: ['Architecture + Domain governance'],
        competencies: ['Enterprise AI Architecture', 'Domain Orchestration', 'Cross-platform Governance',
                       'Risk Management', 'Innovation Pipeline', 'Regulatory Strategy'],
        typicalDay: { 'Architecture': 30, 'Domain Governance': 25, 'Innovation': 20, 'Regulatory': 15, 'Coaching': 10 },
        upskilling: [{ course: 'Enterprise Agentic Architecture', hours: 32, format: 'Workshop series' }] },
    ],
    agents: { count: 21, types: ['All 21 PDLC agents operating autonomously'],
              description: 'Full autonomous ADLC — agents coordinate end-to-end; humans govern at strategic level only' },
  },
}

// ─── Agent Cost Estimator Data ──────────────────────────────────────────────
const AGENT_COST_ESTIMATOR = {
  humanRoleCosts: {
    'Developer':        { annual: 130000, label: 'Developer' },
    'QA Engineer':      { annual: 110000, label: 'QA Engineer' },
    'DevOps Engineer':  { annual: 140000, label: 'DevOps Engineer' },
    'Business Analyst': { annual: 105000, label: 'Business Analyst' },
    'Scrum Master':     { annual: 115000, label: 'Scrum Master' },
    'Architect':        { annual: 170000, label: 'Solution Architect' },
    'Product Owner':    { annual: 140000, label: 'Product Owner' },
    'Support Analyst':  { annual: 90000,  label: 'App Support Analyst' },
    'L2/L3 Support':    { annual: 120000, label: 'L2/L3 Support Engineer' },
    'Platform Ops':     { annual: 135000, label: 'Platform Ops Engineer' },
    'FAE':              { annual: 185000, label: 'Frontier AI Engineer' },
    'FBO':              { annual: 155000, label: 'Frontier Business Operator' },
    'FSA':              { annual: 195000, label: 'Frontier Super Architect' },
    'FPE':              { annual: 160000, label: 'Frontier Platform Engineer' },
    'FSE':              { annual: 145000, label: 'Frontier Support Engineer' },
    'Product Definer (evolved FBO)': { annual: 175000, label: 'Product Definer' },
    'Product Builder (evolved FAE)': { annual: 195000, label: 'Product Builder' },
    'Super Architect (evolved FSA)': { annual: 210000, label: 'Super Architect' },
  },
  agentCostsByPlatform: {
    homegrown:          { perAgentMonth: 2800, infraMonth: 8000, llmTokenMonth: 12000, label: 'Homegrown / Custom Build' },
    stump:              { perAgentMonth: 1200, infraMonth: 0,    llmTokenMonth: 0,     subscriptionMonth: 15000, label: 'STUMP ADLC Platform' },
    bmad:               { perAgentMonth: 2200, infraMonth: 5000, llmTokenMonth: 10000, label: 'BMAD Framework' },
    copilot_workspace:  { perAgentMonth: 1800, infraMonth: 3000, llmTokenMonth: 8000,  label: 'Copilot Workspace' },
    devin:              { perAgentMonth: 1500, infraMonth: 2000, llmTokenMonth: 6000,  subscriptionMonth: 10000, label: 'Cognition Devin' },
    cursor:             { perAgentMonth: 1600, infraMonth: 2500, llmTokenMonth: 7000,  label: 'Cursor' },
    flowsource:         { perAgentMonth: 1400, infraMonth: 2000, llmTokenMonth: 5000,  subscriptionMonth: 8000, label: 'FlowSource' },
    baxter:             { perAgentMonth: 2000, infraMonth: 4000, llmTokenMonth: 9000,  label: 'Baxter' },
  },
  teamByLevel: {
    1: { humans: [
      { role: 'Developer', count: 3 }, { role: 'QA Engineer', count: 2 },
      { role: 'DevOps Engineer', count: 1 }, { role: 'Business Analyst', count: 1 },
      { role: 'Scrum Master', count: 1 }, { role: 'Architect', count: 1 },
      { role: 'Support Analyst', count: 1 }
    ], agents: 0, label: 'Traditional Team (A0)' },
    2: { humans: [
      { role: 'Developer', count: 3 }, { role: 'QA Engineer', count: 2 },
      { role: 'DevOps Engineer', count: 1 }, { role: 'Business Analyst', count: 1 },
      { role: 'Scrum Master', count: 1 }, { role: 'Architect', count: 1 }
    ], agents: 5, label: 'AI-Augmented Team' },
    3: { humans: [
      { role: 'FAE', count: 2 }, { role: 'FBO', count: 1 },
      { role: 'FSA', count: 1 }, { role: 'FSE', count: 1 },
      { role: 'FPE', count: 1 }
    ], agents: 12, label: 'Frontier Team (Emerging)' },
    4: { humans: [
      { role: 'FAE', count: 2 }, { role: 'FBO', count: 1 },
      { role: 'FSA', count: 1 }, { role: 'FSE', count: 1 }
    ], agents: 18, label: 'Frontier Team (A3)' },
    5: { humans: [
      { role: 'Product Definer (evolved FBO)', count: 1 }, { role: 'Product Builder (evolved FAE)', count: 1 },
      { role: 'Super Architect (evolved FSA)', count: 1 }
    ], agents: 21, label: 'Autonomous Team' },
  },
  transformationCostByLevel: {
    1: { training: 25000,  tooling: 50000,   changeManagement: 15000, hiring: 0,      total: 90000 },
    2: { training: 60000,  tooling: 150000,  changeManagement: 40000, hiring: 0,      total: 250000 },
    3: { training: 120000, tooling: 350000,  changeManagement: 100000, hiring: 200000, total: 770000 },
    4: { training: 200000, tooling: 600000,  changeManagement: 200000, hiring: 350000, total: 1350000 },
    5: { training: 250000, tooling: 900000,  changeManagement: 300000, hiring: 500000, total: 1950000 },
  },
}

const SCENARIO_TO_LEVEL = { 'option-a': 2, 'option-b': 3, 'option-c': 4 }

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
    orgChanges: [
      { title: 'Upskill all PDLC personas in AI tool collaboration', icon: '🎓', who: 'Engineering Manager + HR', timeline: 'Weeks 1–3', effort: '4 hrs per person (async)',
        what: 'Every role needs foundational skills to work effectively alongside AI agents — otherwise adoption stalls and people revert to manual methods.',
        how: '1. Run a 30-min skills gap survey (AI familiarity, current tool usage, fears). 2. Create role-specific learning paths: Copilot Fundamentals for devs, FeatureGen prompting for POs, DataGen schema writing for QA. 3. Schedule 4 hrs max async training per person — use GitHub Learning Pathways, Pluralsight, or internal workshops. 4. Designate AI Champion (senior dev, 10% time) to run fortnightly peer Q&A.',
        example: 'Learning paths by role:\n  Developer:  GitHub Copilot Fundamentals (4hr) + AI Code Review (2hr)\n  PO / BA:    FeatureGen Intent Writing (2hr) + AI Story Review (1hr)\n  QA:         DataGen Schema Writing (3hr) + AI Regression Oversight (2hr)\n  DevOps:     AI Pipeline Tools (4hr) + Agent Monitoring (2hr)\n  Scrum Master: AI Metrics Dashboards (1hr) + AI Ceremonies Guide (1hr)',
        successCriteria: '100% team completion of role-specific module. AI Champion nominated and active by Week 2. Fortnightly #ai-wins Slack channel posts from ≥ 3 team members.' },
      { title: 'Redefine roles to include AI supervision and prompt engineering', icon: '🔄', who: 'Engineering Manager', timeline: 'Week 2', effort: '1 day',
        what: 'Job descriptions and performance criteria must reflect the new expectation: developers supervise AI output, not just produce code manually.',
        how: '1. Add "AI output quality review" to all developer JDs and sprint acceptance criteria. 2. Update Definition of Done: AI-assisted work requires an explicit human review comment in the PR. 3. Add "prompt engineering" to developer competency framework — distinguish junior (uses defaults) from senior (writes custom prompts). 4. Update performance review template to include: AI adoption rate, quality of AI review decisions, prompt quality examples.',
        example: 'Updated Definition of Done additions:\n  ✓ If Copilot was used: inline comment explains what was AI-generated vs human-authored\n  ✓ PR description generated or reviewed by AI with PO/tech lead sign-off\n  ✓ No Copilot suggestion accepted without understanding what it does',
        successCriteria: 'Updated JDs published. All PRs from Week 4 include AI usage declaration. No AI suggestion accepted without reviewer comment.' },
      { title: 'Establish AI Centre of Excellence (CoE) for governance', icon: '🏛️', who: 'Engineering Manager + CTO', timeline: 'Week 3', effort: '2 days setup, ongoing 0.1 FTE',
        what: 'A lightweight CoE prevents ad-hoc AI tool proliferation and ensures consistent practices, data policies, and quality standards across teams.',
        how: '1. Appoint AI CoE Lead (AI Champion + 10% Engineering Manager time — no new hire needed at this scale). 2. Create CoE Confluence space: AI tool register, acceptable use policy, best practice library, incident log. 3. Establish monthly CoE review: new tool evaluations, quality incidents, training updates. 4. Publish AI Acceptable Use Policy (1-page): what data can go to cloud AI, what must stay on-prem.',
        example: 'AI Acceptable Use Policy (template):\n  ALLOWED: Code from internal repos (non-PII), public documentation, test schemas\n  FORBIDDEN: PII fields (SSN, email, card numbers), credentials, client-confidential data\n  GREY AREA: Escalate to CoE Lead before using\n  All violations reported to CISO within 24hrs',
        successCriteria: 'Acceptable use policy signed by all team members. CoE Confluence space live. First monthly review conducted.' },
      { title: 'Update ways of working guides for human-AI collaboration', icon: '📋', who: 'Scrum Master', timeline: 'Week 3–4', effort: '2 days',
        what: 'Sprint ceremonies, Definition of Done, and review processes must be updated — otherwise the team tries to fit AI into old processes and gets frustrated.',
        how: '1. Update backlog refinement: first 15 min = PO writes feature intents → FeatureGen runs → team reviews AI ACs (not writes). 2. Update sprint planning: AI velocity forecast as starting point, team adjusts for context. 3. Update PR process: AI pre-review required before human review, human reviewer acts only on flagged items. 4. Update retrospective: add "AI wins/fails" as a standing item.',
        example: 'Updated sprint ceremony agenda:\n  Refinement (1.5 hrs, was 3 hrs):\n    0:00–0:15  PO submits intents → FeatureGen generates ACs\n    0:15–1:00  Team reviews/refines AI-generated ACs\n    1:00–1:30  Estimation + dependency identification\n  Planning (90 min, was 3 hrs):\n    0:00–0:20  Review AI velocity forecast + sprint candidate list\n    0:20–1:20  Team confirms/adjusts sprint scope\n    1:20–1:30  Commitment + risk identification',
        successCriteria: 'Updated WoW doc published and team trained. Refinement ceremony time < 2 hrs. Sprint planning < 2 hrs.' },
      { title: 'Introduce AI literacy training (mandatory for all roles)', icon: '📚', who: 'HR + Engineering Manager', timeline: 'Weeks 1–4', effort: '4–6 hrs total per person',
        what: 'Without baseline AI literacy, developers misuse Copilot, POs write stories instead of intents, and QAs don\'t know how to validate AI-generated test data.',
        how: '1. Run pre-assessment: 10-question survey on AI concepts (week 1). 2. Assign role-specific courses based on gap. 3. Track completion via LMS (or GitHub Learning Pathways built-in tracking). 4. All team members must pass completion check before Week 5 AI tool activation. 5. New joiners: AI literacy course added to onboarding (mandatory by Day 14).',
        example: 'Training completion tracker (Confluence table):\n  Name     | Role     | Copilot | FeatureGen | DataGen | Completed |\n  ---      | ---      | ---     | ---        | ---     | ---       |\n  J.Smith  | Dev      | ✓       | -          | -       | Week 2    |\n  M.Jones  | PO       | -       | ✓          | -       | Week 3    |\n  K.Lee    | QA       | -       | -          | ✓       | Week 3    |',
        successCriteria: '100% team completion by Week 4. New joiners complete training by Day 14 of onboarding. Zero "accidental PII sent to AI" incidents.' },
    ],
    toolsChanges: [
      { title: 'Jira / ADO: Add AI-powered backlog management', icon: '📋', category: 'ALM', phase: 'Phase 1 — Backlog & Roadmap',
        current: 'Manual backlog grooming. POs spend 4–8 hrs/week on prioritization and story writing.',
        change: 'AI plugin auto-prioritizes backlog, suggests sprint candidates, and generates draft stories from epics.',
        how: '1. Install Atlassian Intelligence or Jira AI plugin (Marketplace). 2. Connect to Azure OpenAI API: Jira Admin → Settings → AI → API Key. 3. Enable "AI Sprint Suggestions" and "Backlog Prioritization" features. 4. PO reviews AI sprint suggestion before accepting — do not auto-accept for first 3 sprints.',
        example: '# Jira AI sprint suggestion via CLI (Atlassian API):\ncurl -X POST https://yourorg.atlassian.net/rest/ai/sprint-plan \\\n  -H "Authorization: Bearer $JIRA_API_TOKEN" \\\n  -d \'{"project":"PAYMENTS","sprintCapacity":60,"criteria":"business-value-first"}\'\n# Returns: ranked story list with effort estimates + dependency flags',
        tools: ['Atlassian Intelligence', 'Linear AI', 'Azure DevOps Copilot'],
        owner: 'Scrum Master', timeline: 'Week 2', effort: '1–2 days',
        successCriteria: 'Sprint planning ceremony < 90 min (was 3–4 hrs). PO backlog prep time reduced by 40%.' },
      { title: 'GitHub: Deploy Copilot Enterprise for all developers', icon: '🤖', category: 'Code Generation', phase: 'Phase 2/3 — Development',
        current: 'Developers write all code manually. No AI assistance in IDE.',
        change: 'Copilot assists with code generation, PR descriptions, and code review summaries. Target: 30–40% boilerplate effort eliminated.',
        how: '1. GitHub Org Admin → Settings → Copilot → Enable for all members. 2. Configure content exclusions (PII, secrets, regulated fields) BEFORE activating seats. 3. Install VS Code extension (marketplace) or JetBrains plugin. 4. Run 4hr "Copilot Fundamentals" async training for all devs. 5. Set acceptance rate target: 40–60% (not 100% — quality over quantity).',
        example: '# Content exclusions (.github/copilot-config.yml):\ncontent_exclusions:\n  - "**/.env*"\n  - "**/secrets/**"\n  - "**/pii/**"\n  - "**/*ssn*"\n  - "**/*card_number*"\n\n# Verify setup: open VS Code → type a function signature\n# → Copilot grey suggestion should appear in 2–3 seconds',
        tools: ['GitHub Copilot Business', 'VS Code', 'JetBrains IDE'],
        owner: 'DevOps Engineer', timeline: 'Week 1', effort: '4–8 hours',
        successCriteria: 'All developer seats active. Content exclusions configured and tested. Zero PII-sent-to-AI incidents.' },
      { title: 'Testing: Upgrade to AI-enhanced test frameworks', icon: '🧪', category: 'Testing', phase: 'Phase 5 — Testing',
        current: 'Manual test data provisioning (4–16 hr DBA ticket). Manual test script authoring. Regression suite: human-maintained.',
        change: 'DataGen Agent provisions synthetic test data in < 2 min. AI suggests test scenarios from ACs. AI Visual Regression detects UI anomalies.',
        how: '1. Install DataGen (pip install faker or Tonic.ai trial). 2. DBA reviews and approves entity schema definitions. 3. Integrate DataGen into CI: seed before integration tests, teardown after. 4. Add AI test suggestion to Definition of Ready: FeatureGen includes test scenarios alongside ACs. 5. Evaluate Applitools or Percy for visual regression automation.',
        example: '# GitHub Actions — test data integration:\n- name: Seed test data\n  run: datagen seed --profile payment_flow --count 100 --env ci\n\n- name: Run integration tests\n  run: npm run test:integration\n\n- name: Teardown\n  if: always()   # ← critical: cleans up even when tests fail\n  run: datagen teardown --profile payment_flow --env ci',
        tools: ['DataGen / Faker / Tonic.ai', 'Applitools', 'Percy', 'Playwright AI'],
        owner: 'QA Lead + DevOps', timeline: 'Weeks 3–5', effort: '3–5 days',
        successCriteria: 'Test data provisioning < 2 min (was 4–16 hrs). Zero production data in non-prod environments. Test suite run time unchanged or faster.' },
      { title: 'CI/CD: Integrate ML-based SAST and build optimizers', icon: '⚙️', category: 'CI/CD', phase: 'Phase 4 — CI / Phase 6 — CD',
        current: 'SAST runs weekly manually. Build times not optimized. Deployments require manual CAB approval for all changes.',
        change: 'SAST on every PR with AI triage (High/Critical = block). Build optimizer predicts flaky tests and skips unchanged modules. AI Release Manager validates low-risk deploys automatically.',
        how: '1. Add Snyk GitHub Actions step to every repo (before integration tests). 2. Configure severity thresholds with CISO: Critical/High = block, Medium = warn + Jira ticket. 3. Enable GitHub Actions path filtering: only rebuild affected modules. 4. Evaluate Gradle Build Scan / Bazel remote cache for build acceleration.',
        example: '# .github/workflows/ci.yml — SAST gate:\n- name: Snyk Security Scan\n  uses: snyk/actions/node@master\n  env:\n    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}\n  with:\n    args: --severity-threshold=high --fail-on=upgradable\n\n# Build optimization — only run tests for changed modules:\n- name: Detect changes\n  uses: dorny/paths-filter@v2\n  id: changes\n  with:\n    filters: |\n      payments: ["src/payments/**"]\n      auth: ["src/auth/**"]\n\n- name: Payments tests\n  if: steps.changes.outputs.payments == \'true\'\n  run: npm run test:payments',
        tools: ['Snyk', 'GitHub Advanced Security', 'Semgrep', 'Gradle Build Scan'],
        owner: 'DevOps Engineer', timeline: 'Weeks 2–4', effort: '4–8 hours',
        successCriteria: 'SAST running on 100% of PRs. Build time reduced by 20–30% via change detection. Zero High/Critical vulnerabilities merged to main.' },
      { title: 'Monitoring: Deploy AI APM platform', icon: '📡', category: 'Observability', phase: 'Phase 7 — Monitoring & Feedback',
        current: 'Manual alert triage (200+ alerts/day, < 5% actionable). MTTD: 15–45 min. Dashboards manually maintained.',
        change: 'AI APM auto-correlates anomalies, reduces alert noise by 90%, and surfaces root cause in < 2 min.',
        how: '1. Evaluate Dynatrace Davis AI, Datadog AI, or New Relic AI — deploy 30-day trial. 2. Connect all services (instrument with OpenTelemetry). 3. Configure AI baseline: let APM learn normal traffic patterns for 2 weeks before enabling alerts. 4. Suppress existing manual alerts during baseline period. 5. Switch to AI-driven alerting in Week 4.',
        example: '# OpenTelemetry auto-instrumentation (Node.js):\nnpm install @opentelemetry/auto-instrumentations-node\n\n# Start with OTEL collector:\nOTEL_EXPORTER_OTLP_ENDPOINT=http://dynatrace-collector:4317 \\\nOTEL_SERVICE_NAME=payments-service \\\nOTEL_NODE_ENABLED_INSTRUMENTATIONS=http,express,pg \\\nnode --require @opentelemetry/auto-instrumentations-node/register app.js\n\n# Dynatrace baseline config:\n# Settings → Anomaly Detection → Automatic Baseline → Enable for all services\n# Alert only on: probability > 90% AND impact = HIGH',
        tools: ['Dynatrace Davis AI', 'Datadog AI', 'New Relic AI', 'OpenTelemetry'],
        owner: 'DevOps Engineer', timeline: 'Weeks 4–6', effort: '2–3 days',
        successCriteria: 'Alert volume reduced by ≥ 80%. MTTD < 5 min (was 15–45 min). On-call engineers report fewer false-alarm pages.' },
    ],
    devSecOps: [
      { title: 'Shift-left security: AI-assisted SAST/DAST on every PR', icon: '🔍', pipelineStage: 'Code → PR', priority: 'P1 — Start Week 2',
        current: 'SAST runs manually once per week. 60%+ false positive rate. Real vulnerabilities lost in noise. Security reviewed only at release gate.',
        change: 'AI SAST runs on every PR automatically. ML triage eliminates noise: High/Critical = block merge, Medium = Jira ticket (auto). Security is continuous not periodic.',
        how: '1. Deploy Snyk via GitHub Actions (see config below). 2. Run in warn-only mode for 2 weeks — measure FP rate. 3. Tune thresholds with CISO to < 20% FP. 4. Enable blocking mode for High/Critical. 5. Wire Snyk→Jira: Critical auto-creates P1 ticket, High auto-creates P2. 6. Cancel weekly security review meeting — replace with Slack alert + async dashboard.',
        example: '# .github/workflows/security.yml\nname: Security Gate\non: [pull_request]\njobs:\n  sast:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Snyk SAST\n        uses: snyk/actions/node@master\n        env:\n          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}\n        with:\n          args: --severity-threshold=high --sarif-file-output=snyk.sarif\n      - name: Upload to GitHub Security tab\n        uses: github/codeql-action/upload-sarif@v2\n        with:\n          sarif_file: snyk.sarif\n\n# Jira auto-ticket on High+ finding:\n# Snyk dashboard → Integrations → Jira:\n#   Project: SEC-BACKLOG | Label: sast-finding | Priority: map severity→Jira priority',
        tools: ['Snyk', 'Semgrep', 'GitHub Advanced Security'],
        metrics: 'SAST coverage: 0% → 100% of PRs. FP rate: 60% → < 20%. Security triage time: 4 hrs/week → 0 (automated).' },
      { title: 'AI-generated IaC templates with security policy validation', icon: '🏗️', pipelineStage: 'Code → CD', priority: 'P2 — Start Week 4',
        current: 'IaC written manually. Security misconfigurations discovered in prod. No automated policy validation.',
        change: 'AI generates secure-by-default IaC templates. Every IaC change validated against security policies before deploy. Misconfigurations blocked at the gate.',
        how: '1. Deploy Checkov or AWS Config Rules for IaC policy validation. 2. Add IaC scan step to CI pipeline (runs after Terraform plan, before apply). 3. Configure AI IaC generator (GitHub Copilot can suggest Terraform from comments). 4. Build a library of approved, secure IaC modules in a shared repo — teams use modules, not raw resources. 5. CISO reviews policy library quarterly.',
        example: '# .github/workflows/iac-security.yml\n- name: Terraform Security Scan\n  uses: bridgecrewio/checkov-action@master\n  with:\n    directory: ./terraform\n    framework: terraform\n    soft_fail: false                # Hard fail on critical violations\n    check: CKV_AWS_*               # AWS security checks\n    skip_check: CKV_AWS_144        # Skip if intentionally waived\n\n# AI IaC generation (GitHub Copilot comment-driven):\n# Comment in .tf file: "# Create an S3 bucket with encryption, versioning, and public access blocked"\n# → Copilot generates compliant Terraform block',
        tools: ['Checkov', 'Terraform', 'AWS Config', 'GitHub Copilot'],
        metrics: 'IaC security violations in prod: reduced by 70%. Time to detect misconfiguration: days → seconds (at PR).' },
      { title: 'Automated compliance evidence collection for audit trails', icon: '📂', pipelineStage: 'All Phases', priority: 'P2 — Start Week 6',
        current: 'Compliance evidence collected manually before each audit (2–5 person-weeks effort). Evidence often stale or missing.',
        change: 'CI/CD pipeline automatically captures and archives compliance evidence at each deployment: test results, SAST reports, approvals, deployment logs.',
        how: '1. Add evidence capture steps to CI pipeline: archive test reports, SAST scan results, approval records, and deployment logs to S3/Azure Blob (7-year retention). 2. Generate compliance report from artefacts: map each artefact to compliance requirement (SOC2, ISO27001, etc.). 3. Evaluate Drata or Vanta for continuous compliance monitoring (auto-maps CI artefacts to control requirements). 4. Brief CISO: "audit evidence is always current — zero prep work for audits."',
        example: '# GitHub Actions — evidence archive:\n- name: Archive compliance evidence\n  if: github.ref == "refs/heads/main"\n  run: |\n    DEPLOY_ID="${{ github.sha }}-$(date +%Y%m%d-%H%M%S)"\n    aws s3 cp test-results/ s3://compliance-evidence/$DEPLOY_ID/tests/ --recursive\n    aws s3 cp snyk.sarif s3://compliance-evidence/$DEPLOY_ID/sast/\n    echo "Deployed by: ${{ github.actor }} at $(date)" \\\n      > s3://compliance-evidence/$DEPLOY_ID/deployment-record.txt\n\n# S3 bucket config (compliance-evidence):\n# Versioning: enabled | Object Lock: Compliance mode, 7 years',
        tools: ['Drata', 'Vanta', 'AWS S3 Object Lock', 'GitHub Actions'],
        metrics: 'Audit prep time: 2–5 person-weeks → < 1 day. Evidence completeness: 60% → 100%. Audit findings related to missing evidence: eliminated.' },
      { title: 'AI-powered secret scanning and dependency vulnerability alerts', icon: '🔑', pipelineStage: 'Code Commit', priority: 'P1 — Start Week 1',
        current: 'Secrets occasionally committed to repos and discovered late. Dependency vulnerabilities not monitored continuously.',
        change: 'GitHub Secret Scanning blocks commits with credentials. Dependabot auto-raises PRs for vulnerable dependencies. Zero secrets in repos.',
        how: '1. Enable GitHub Secret Scanning: Org Settings → Code Security → Enable secret scanning for all repos. 2. Enable Push Protection: blocks pushes that contain secrets (no opt-out without CISO approval). 3. Enable Dependabot: creates auto-PRs for dependency vulnerabilities. 4. Configure Dependabot alert threshold: auto-merge patch updates, require review for minor/major. 5. Add pre-commit hook locally: git-secrets or truffleHog to catch secrets before push.',
        example: '# .github/dependabot.yml\nversion: 2\nupdates:\n  - package-ecosystem: "npm"\n    directory: "/"\n    schedule:\n      interval: "weekly"\n    open-pull-requests-limit: 10\n    ignore:\n      - dependency-name: "*"\n        update-types: ["version-update:semver-major"]  # Require manual review for major\n    labels: ["dependencies", "security"]\n    reviewers: ["tech-lead"]\n\n# Enable push protection via GitHub CLI:\ngh api -X PUT /orgs/YOUR_ORG/secret-scanning/push-protection \\\n  --input \'{"enabled":true}\'',
        tools: ['GitHub Secret Scanning', 'Dependabot', 'truffleHog', 'git-secrets'],
        metrics: 'Secrets in repos: target 0 (enforce). Vulnerable dependency lag: weeks → days. Mean time to patch critical CVE: < 48 hrs.' },
    ],
    aiOps: [
      { title: 'AI-driven anomaly detection and auto-remediation', icon: '🔍', layer: 'Detection', priority: 'P1 — Start Week 6',
        current: 'Manual alert triage from Prometheus/CloudWatch. 200+ alerts/day, < 5% actionable. MTTD: 15–45 min. Engineers spend 30% of on-call shift on false alarms.',
        change: 'AI APM learns normal baseline and alerts only on genuine anomalies. 90% noise reduction. Auto-remediates known failure patterns (pod restart, scaling trigger, cache flush).',
        how: '1. Deploy Dynatrace Davis AI or Datadog AI (30-day trial). 2. Auto-instrument all services with OpenTelemetry. 3. Let AI learn baseline for 2 weeks (do not modify alert rules during this period). 4. Configure auto-remediation runbooks for top 5 known failure patterns. 5. After Week 4: suppress legacy alerts and switch to AI-only alerting.',
        example: '# OpenTelemetry auto-instrumentation (Node.js service):\nOTEL_SERVICE_NAME=payments-api \\\nOTEL_EXPORTER_OTLP_ENDPOINT=http://dynatrace:4317 \\\nOTEL_RESOURCE_ATTRIBUTES="team=payments,env=production" \\\nnode --require @opentelemetry/auto-instrumentations-node/register server.js\n\n# Auto-remediation rule example (Dynatrace):\n# Trigger: error_rate(payments-api) > 5% for 3 min\n# Action: POST https://jenkins/job/restart-payments-api/build\n# Cooldown: 15 min (prevents restart loop)',
        tools: ['Dynatrace Davis AI', 'Datadog AI Monitors', 'PagerDuty AIOps', 'OpenTelemetry'],
        metrics: 'Alert volume: 200/day → < 20/day actionable. MTTD: 15–45 min → < 3 min. On-call false alarm pages: reduced by 90%.' },
      { title: 'Predictive scaling based on ML traffic patterns', icon: '📈', layer: 'Capacity', priority: 'P2 — Start Week 8',
        current: 'Manual capacity planning quarterly. Reactive scaling (scale after the spike hits). Over-provisioned 40% of the time (cost waste).',
        change: 'ML model predicts load 30–60 min ahead based on historical patterns, calendar events, and upstream signals. Auto-scales proactively — zero lag, 25% cost reduction.',
        how: '1. Enable Kubernetes HPA (Horizontal Pod Autoscaler) if not already active. 2. Evaluate KEDA (Kubernetes Event-Driven Autoscaler) for event-based scaling. 3. For AWS: enable Predictive Scaling in Auto Scaling Groups (uses ML model trained on your history). 4. Configure minimum/maximum replica guardrails. 5. Monitor: compare actual vs predicted load for first 4 weeks. Tune prediction sensitivity.',
        example: '# AWS Auto Scaling — Predictive Scaling policy:\naws autoscaling put-scaling-policy \\\n  --auto-scaling-group-name payments-asg \\\n  --policy-name payments-predictive-scaling \\\n  --policy-type PredictiveScaling \\\n  --predictive-scaling-configuration file://predictive-config.json\n\n# predictive-config.json:\n{\n  "MetricSpecifications": [{\n    "TargetValue": 70,\n    "PredefinedMetricPairSpecification": {\n      "PredefinedMetricType": "ASGCPUUtilization"\n    }\n  }],\n  "Mode": "ForecastAndScale",\n  "SchedulingBufferTime": 300\n}',
        tools: ['AWS Predictive Scaling', 'KEDA', 'Kubernetes HPA', 'Datadog Forecast'],
        metrics: 'Scaling lag: reactive (minutes) → proactive (30–60 min ahead). Compute cost: reduced 20–30% via right-sizing. Zero capacity-related incidents.' },
      { title: 'Automated incident routing with NLP-based categorization', icon: '🚨', layer: 'Incident Response', priority: 'P1 — Start Week 6',
        current: 'Incidents manually categorized and routed to on-call. Triage takes 20–60 min. Wrong team paged 30% of the time. PIRs written manually (4–8 hrs each, often skipped).',
        change: 'NLP categorizes incident from alert text and routes to correct team in < 30 seconds. AI Triage Agent suggests root cause, severity, and first-response actions. AI PIR Generator produces draft PIR in 45 min.',
        how: '1. Connect alerting (PagerDuty/OpsGenie) to STUMP AI Triage Agent. 2. Train NLP classifier on last 6 months of incidents (label with: team, severity, category, root cause). 3. Configure routing rules: if classifier confidence > 85%, auto-route; < 85%, route to on-call triage queue. 4. Set up AI PIR Generator: triggers automatically 2 hrs after P1/P2 incident resolution. 5. Run 3 incident simulations before go-live.',
        example: '# PagerDuty → STUMP AI Triage webhook:\nPOST https://stump.internal/api/incident-triage\nPayload: {\n  "incident_id": "INC-2024-001",\n  "alert_body": "payments-api: 504 Gateway Timeout on /api/v1/transfer — 15% error rate",\n  "source": "dynatrace",\n  "triggered_at": "2024-04-23T14:32:00Z"\n}\n\n# STUMP response (< 30 seconds):\n{\n  "severity": "P2",\n  "category": "payments-api-latency",\n  "route_to_team": "payments-engineering",\n  "suggested_cause": "Downstream database connection pool exhausted (pattern matches INC-2024-089)",\n  "first_action": "Check RDS connection count: SHOW STATUS LIKE \'Threads_connected\'"\n}',
        tools: ['PagerDuty', 'OpsGenie', 'STUMP AI Triage', 'Slack AI'],
        metrics: 'Triage time: 20–60 min → < 2 min. Wrong-team routing: 30% → < 5%. PIR completion rate: 40% → > 90% (AI makes it easy).' },
      { title: 'Continuous feedback loop: production insights → backlog', icon: '🔄', layer: 'Feedback Loop', priority: 'P2 — Start Week 8',
        current: 'Production insights (errors, performance issues, user friction) reach the backlog weeks later (if ever). Engineering prioritizes tech debt independently of live signals.',
        change: 'Telemetry Sentinel connects production signals to Jira automatically: high-error-rate endpoints create bug tickets, slow user journeys create performance stories, model drift creates MRM tasks.',
        how: '1. Configure Telemetry Sentinel signal-to-backlog rules (see example). 2. Define thresholds: what constitutes a signal worthy of a Jira ticket. 3. Tag auto-created tickets with "production-signal" label for PO review. 4. PO reviews production-signal tickets weekly and promotes to sprint if priority warrants. 5. Track: % of sprint work originating from production signals (target: 20–30% — ensures team is responding to real user impact).',
        example: '# Telemetry Sentinel → Jira rules (stump config):\nsignal_rules:\n  - name: High error rate\n    condition: error_rate > 1% for 15min on endpoint\n    action: create_jira_bug\n    template:\n      project: PAYMENTS\n      summary: "⚠ High error rate: {endpoint} — {error_rate}% errors"\n      priority: P2\n      label: production-signal\n      description: "Auto-detected: {error_count} errors in last 15 min. Stacktrace: {top_error}"\n\n  - name: Page slow\n    condition: page_load_p75 > 3s for any page\n    action: create_jira_story\n    template:\n      summary: "🐢 Slow page: {page_name} — p75 {latency}ms"\n      label: production-signal,performance',
        tools: ['STUMP Telemetry Sentinel', 'Datadog Watchdog', 'Dynatrace Davis'],
        metrics: '% of sprint work driven by production signals: 0% → 20–30%. Mean time from signal to sprint: weeks → 1 sprint. User-impacting bugs discovered proactively: up 50%.' },
    ],
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
      operationalSavings: '$200K–$350K (automated ops and monitoring)',
      complianceAutomation: '$150K–$300K (Compliance-as-Code Orchestrator eliminates ~60% manual audit effort)',
      securityIncidentReduction: '$100K–$200K (Secure-by-Design Architect prevents misconfigurations; avg cost of cloud misconfiguration incident = $500K+)',
      modelRiskAvoidance: '$200K–$400K (MRM Agent prevents rogue model deployments; regulatory fines avoided)',
      businessRiskVisibility: '$50K–$100K (Telemetry Sentinel Business Risk Scores reduce mean time to governance escalation)'
    },
    orgChanges: [
      { title: 'Consolidate 8+ roles to 5 core roles', icon: '🔄', who: 'Engineering Manager + HR', timeline: 'Week 1–3', effort: '2–3 days',
        what: 'Stage 2 shifts work to agents — 8+ specialised roles (manual QA scripting, manual BA, dedicated code reviewer) become redundant. Five core roles remain: Product Owner, Tech Lead, Developer, QA Lead, DevOps Engineer.',
        how: '1. Map every current role to the 5-role model. Identify role transitions (e.g., QA Script Writer → QA Lead for agent oversight). 2. Have 1-to-1 conversations with each team member about their new scope BEFORE any formal announcement. 3. Write updated job descriptions for all 5 roles — emphasise AI agent oversight, quality gate ownership, and prompt engineering. 4. Run a 1-day transition workshop: what agents now do vs what each human role owns. 5. Parallel-run for 2 sprints before cutover — no role is removed until its agent replacement has passed the 50-item quality gate.',
        example: 'Role transition map (example):\n  BEFORE               →  AFTER\n  Manual QA scripter   →  QA Lead (oversees QA Orchestrator + DataGen Agent)\n  BA / story writer    →  Product Owner (writes feature intents, not stories)\n  Dedicated code rev.  →  Developer (uses ReviewAgent — reviews AI findings, not all code)\n  IaC engineer         →  DevOps (validates Secure-by-Design Architect output)\n  Release coordinator  →  Tech Lead (monitors AI Release Manager + override authority)',
        successCriteria: '5-role model live by Week 4. Each team member has a signed updated JD. Zero surprise redeployments — all transitions communicated in 1-to-1s. Agent quality gate passed before any role transition cutover.' },
      { title: 'Establish AI Agent Operations team (embedded)', icon: '🤖', who: 'Tech Lead + DevOps', timeline: 'Week 2', effort: '1 day setup + ongoing 15 min/day',
        what: 'Agents require ongoing tuning, monitoring, and quality oversight. Without an Agent Ops function, output quality degrades silently and teams lose trust in the agents.',
        how: '1. Designate Agent Ops Lead (Tech Lead, 20% time). DevOps Engineer handles infrastructure (agent uptime, latency, cost). 2. Daily 15-min Agent Ops standup: review each agent\'s quality score, error rate, and output acceptance rate. 3. Build Agent Ops Confluence space: agent registry, prompt library, quality gate definitions, incident runbook, tuning log. 4. Define SLOs per agent: output acceptance rate ≥ 80%, p95 response time < 30s, no silent failures. 5. Any agent below SLO triggers a 1-sprint tuning sprint — Agent Ops Lead owns it.',
        example: '# Agent health dashboard (Confluence table, updated daily):\nAgent            | Acceptance% | p95 Latency | Errors (7d) | Last Tuned | Status\n---              | ---         | ---         | ---         | ---        | ---\nFeatureGen       | 87%         | 8s          | 2           | Week 3     | ✅ OK\nReviewAgent      | 91%         | 4s          | 0           | Week 2     | ✅ OK\nQA Orchestrator  | 74%         | 18s         | 7           | —          | ⚠ Tune needed\nAI Release Mgr   | 93%         | 6s          | 1           | Week 4     | ✅ OK',
        successCriteria: 'Agent Ops Lead designated by Week 2. All 21 agents in registry with SLOs. Daily standup cadence live. No agent below 80% acceptance for > 3 consecutive days without a tuning sprint in progress.' },
      { title: 'Define human-AI handoff protocols per PDLC phase', icon: '📋', who: 'Tech Lead + Scrum Master', timeline: 'Week 3–5', effort: '3 days',
        what: 'Without explicit handoff protocols, humans either over-ride agents on every output (negating value) or rubber-stamp them (losing oversight). Clear protocols define when agents own the action and when humans review.',
        how: '1. For each phase, document: Trigger (what activates the agent), Agent output (what it produces), Human action (review / approve / escalate — never "write"), Override criteria (when human overrides). 2. Publish as a 1-page swim-lane diagram per phase in Confluence. 3. Run a half-day team workshop: walk through 3 real scenarios using the protocols. Role-play override scenarios. 4. Add handoff protocol summary to Definition of Done for every phase.',
        example: 'Handoff protocol — Phase 3 (Development):\n  Trigger:        PR opened by developer\n  Agent (←):      ReviewAgent scans diff → flags issues (Critical/High/Advisory)\n  Human action:   Developer reads all Critical/High flags, resolves or documents why not\n                  Tech Lead reviews PR only for Critical flags + business logic\n  Override rule:  If agent flags a false positive, developer adds "AI-override: [reason]"\n                  3+ false positives on same pattern → Tech Lead raises prompt tuning ticket\n  Time budget:    PR review ≤ 45 min (was 4–24 hrs manual)',
        successCriteria: 'Handoff protocol documented for all 7 PDLC phases. Published in Confluence. Team can correctly identify "agent owns / human reviews" boundary for 5 out of 5 scenario role-play questions.' },
      { title: 'Redesign team performance metrics for AI-human output', icon: '📊', who: 'Product Owner + Engineering Manager', timeline: 'Week 2', effort: '1 day',
        what: 'Legacy metrics (story points, code lines committed, manual test coverage %) measure human output and are meaningless when agents produce most of the work. Teams optimising for old metrics will undermine AI adoption.',
        how: '1. Retire story points as the primary delivery metric. Replace with lead time and flow efficiency (both captured on this VSM platform). 2. Add AI-human team metrics: agent output acceptance rate (measures quality), override rate (measures trust calibration), flow efficiency delta (measures transformation progress). 3. Update performance reviews: no individual is judged by volume of code or tests written — judged by quality of agent oversight, prompt quality, and VSM metric contributions. 4. Make VSM metrics visible: embed lead time and FE in the team weekly dashboard.',
        example: 'Updated team KPIs (Confluence table):\n  RETIRED                    →  REPLACED WITH\n  Story points completed      →  Lead time (P50) — target < 19 days\n  Manual test coverage %      →  Agent acceptance rate — target ≥ 85%\n  Lines of code committed      →  Flow efficiency — target 23%+\n  Defects found in testing    →  Defects escaped to prod (post-AI) — target near-zero\n  PRs reviewed manually       →  AI SAST critical findings resolved (%) — target 100%',
        successCriteria: 'New KPI dashboard live by Week 3. Story points NOT in sprint review slide. Lead time and flow efficiency in team weekly digest. Engineering Manager using new metrics in performance review template.' },
      { title: 'Executive sponsorship and AI governance programme', icon: '🏛️', who: 'Product Owner + CTO + CISO', timeline: 'Week 1 (kickoff) + ongoing', effort: '2 hrs/month ongoing',
        what: 'Stage 2 involves custom agent development, role restructuring, and compliance-aware AI tooling. Without executive sponsorship and governance, procurement stalls, agent deployments get blocked, and compliance concerns derail adoption.',
        how: '1. Identify exec sponsor (CTO or CIO) and schedule 30-min monthly AI governance review. 2. Create AI Governance Charter (1 page): what AI agents can decide, what requires human approval, what data they can access, escalation path for incidents. 3. Brief CISO on Compliance-as-Code Orchestrator and MRM Agent before deployment — get formal sign-off. 4. Set up cross-functional Slack #ai-governance channel: includes CISO, CTO, Product Owner, Tech Lead — any agent incident or override exception posted here within 24 hrs. 5. Quarterly board update: VSM metrics delta, ROI progress, risk register.',
        example: 'AI Governance Charter — summary (1 page):\n  Agents CAN decide:    Code review findings (flag/block/approve)\n                        Test data generation (auto-approved schemas only)\n                        Low-risk releases (below risk threshold defined by Tech Lead)\n  Agents CANNOT decide: Production access changes, PII schema changes, regulated feature launches\n  Data access:          Internal code repos, non-PII schemas, anonymised telemetry\n  Forbidden:            PII fields, credentials, regulatory documents (CISO-gated)\n  Incident escalation:  Agent override or failure → #ai-governance within 2 hrs',
        successCriteria: 'Exec sponsor nominated and governance review scheduled. AI Governance Charter signed by CTO + CISO. #ai-governance channel live. No agent deployed to production without CISO sign-off on data access scope.' },
    ],
    toolsChanges: [
      { title: 'Deploy LangGraph / LangChain agent orchestration layer', icon: '🧠', category: 'Orchestration', phase: 'Foundation',
        current: 'No agent orchestration infrastructure. Tools are standalone. Agents cannot pass context to each other or invoke tools dynamically.',
        change: 'LangGraph StateGraph manages agent workflows: state is shared across agents, transitions are conditional, and agents invoke tools on-demand (← assistive mode).',
        how: '1. Set up Python virtual environment. Install LangGraph and LangChain: `pip install langgraph langchain langchain-openai`. 2. Configure Azure OpenAI connection in .env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME. 3. Build base StateGraph with shared state schema (project context, phase, artifact refs). 4. Register MCP tool definitions for each external system (GitHub, Jira, Azure DevOps). 5. Deploy to Azure Container Apps or AWS ECS; expose health endpoint for Agent Ops monitoring.',
        example: '# LangGraph base StateGraph scaffold:\nfrom langgraph.graph import StateGraph, END\nfrom typing import TypedDict, Annotated\nimport operator\n\nclass PDLCState(TypedDict):\n    phase: str\n    feature_brief: str\n    stories: list[str]\n    review_findings: list[dict]\n    test_results: dict\n    release_ready: bool\n\nworkflow = StateGraph(PDLCState)\nworkflow.add_node("feature_gen", feature_gen_agent)\nworkflow.add_node("story_gen",   story_gen_agent)\nworkflow.add_node("review",      review_agent)\nworkflow.set_entry_point("feature_gen")\nworkflow.add_edge("feature_gen", "story_gen")\nworkflow.add_edge("story_gen",   "review")\nworkflow.add_edge("review",      END)\napp = workflow.compile()',
        tools: ['LangGraph', 'LangChain', 'Azure OpenAI', 'GitHub MCP', 'Azure DevOps MCP'],
        owner: 'Tech Lead + DevOps', timeline: 'Week 1–2', effort: '3–5 days',
        successCriteria: 'StateGraph compiles and runs locally. Azure OpenAI call succeeds. MCP tool invocations validated for GitHub and Jira. Health endpoint returning 200 OK.' },
      { title: 'FeatureGen + StoryGen Agents (Phase 1–2)', icon: '📋', category: 'Planning', phase: 'Phase 1–2 — Backlog & Roadmap',
        current: 'PO spends 4–8 hrs/week writing stories manually. BAs translate epics to stories and ACs by hand. Story quality varies by author.',
        change: 'FeatureGen converts feature intents to user stories with ACs in < 2 min. StoryGen decomposes epics to sprint-sized stories. PO reviews and approves — never writes from scratch. (← assistive: PO approves every output before Jira import.)',
        how: '1. FeatureGen: Build LangChain chain with system prompt instructing output in Gherkin BDD (Given/When/Then). Input: feature intent (2–5 sentences) from PO. Output: 3–8 user stories with acceptance criteria. 2. StoryGen: LangChain chain decomposing epics into sprint-sized tasks (≤ 8 story points). 3. Build Jira integration: agent calls Jira API to create draft tickets in "AI Review" column. PO promotes to backlog after review. 4. Configure retry on quality check: if story has < 3 ACs, agent retries with stricter prompt. 5. Quality gate: PO acceptance rate must reach 80% before removing "AI Review" column.',
        example: '# FeatureGen invoke (Python):\nfrom langchain_openai import AzureChatOpenAI\nfrom langchain.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_messages([\n  ("system", "You are a senior BA. Convert the feature intent into Gherkin user stories with ACs. Format: \'As a [role], I want [goal] so that [reason]. AC: Given/When/Then.\'"),\n  ("human", "{feature_intent}")\n])\nchain = prompt | AzureChatOpenAI(deployment_name="gpt-4o")\nresult = chain.invoke({"feature_intent": "Allow customers to schedule recurring payments"})\n# Output: 6 user stories with full Gherkin ACs in < 8 seconds',
        tools: ['LangChain', 'Azure OpenAI GPT-4o', 'Jira REST API', 'GitHub Copilot'],
        owner: 'Product Owner + Tech Lead', timeline: 'Week 2–3', effort: '4–6 days',
        successCriteria: 'PO story-writing time < 1 hr/sprint (was 4–8 hrs). FeatureGen acceptance rate ≥ 80% after 2 sprints. "AI Review" column in Jira populated before every refinement session.' },
      { title: 'CodeGen + ReviewAgent (Phase 3 — Development)', icon: '💻', category: 'Development', phase: 'Phase 3 — Development',
        current: 'Developers write all code manually. Code review is a bottleneck: 4–24 hrs turnaround, inconsistent coverage, reviewer fatigue on large PRs.',
        change: 'GitHub Copilot generates boilerplate, tests, and documentation. ReviewAgent (← assistive) analyses every PR diff: flags Critical/High/Advisory issues with explanations and suggestions. Human reviewer acts on findings — not re-reads the whole diff.',
        how: '1. Enable GitHub Copilot Enterprise at org level (Org Admin → Settings → Copilot). Configure content exclusions for PII and secrets. 2. Build ReviewAgent: LangChain agent with GitHub PR diff as input. Prompt: analyse for security issues, code quality, test coverage gaps, and architecture violations. Output: structured JSON (findings array with severity, location, explanation, suggested fix). 3. Wire ReviewAgent to GitHub via webhook (PR opened → agent runs → posts review comments via GitHub API). 4. Add mandatory ReviewAgent run to PR branch protection rules. Human reviewer focuses on Critical/High only. 5. Measure: acceptance rate of ReviewAgent suggestions by developers.',
        example: '# ReviewAgent PR webhook handler (FastAPI):\n@app.post("/webhooks/github-pr")\nasync def on_pr_opened(payload: dict):\n    diff = await github.get_pr_diff(payload["pull_request"]["url"])\n    findings = await review_agent.analyze(diff)\n    comments = [\n        {"path": f["file"], "line": f["line"],\n         "body": f"[{f[\'severity\']}] {f[\'issue\']}\\n\\n**Suggested fix:** {f[\'suggestion\']}"}\n        for f in findings if f["severity"] in ("Critical", "High")\n    ]\n    await github.post_review_comments(payload["pull_request"]["number"], comments)\n# Result: PR review pre-populated with AI findings before human reviewer opens it',
        tools: ['GitHub Copilot Enterprise', 'LangChain + Azure OpenAI', 'GitHub Webhooks API', 'VS Code / JetBrains'],
        owner: 'Tech Lead + Developers', timeline: 'Week 2–4', effort: '3–5 days',
        successCriteria: 'ReviewAgent running on 100% of PRs. Code review turnaround < 2 hrs (was 4–24 hrs). Critical/High finding resolution rate ≥ 95% before merge. Developer Copilot suggestion acceptance rate ≥ 35%.' },
      { title: 'QA Orchestrator + DataGen Agent (Phase 5 — Testing)', icon: '🧪', category: 'Testing', phase: 'Phase 5 — Testing',
        current: 'Manual test scripting: 16–40 hrs per feature. Test data provisioned via DBA ticket (4–16 hrs). No AI in test automation. Regression suite manually maintained.',
        change: 'QA Orchestrator generates BDD test scenarios from stories and orchestrates test execution. DataGen Agent provisions synthetic, PII-safe test data in < 2 min. (← assistive: QA Lead reviews scenario list before execution.)',
        how: '1. DataGen Agent: LangChain chain with entity schema input → generates Faker-based synthetic data matching schema. Add DBA review step for new schemas. Integrate with CI: seed before integration tests, teardown after. 2. QA Orchestrator: reads story ACs from Jira → generates BDD feature files (Cucumber/Playwright format) → QA Lead reviews and approves → CI pipeline runs. 3. Wire DataGen to CI: GitHub Actions step "Seed test data" calls DataGen REST API before integration test suite. 4. Configure QA Orchestrator to flag coverage gaps: if a story AC has no corresponding test scenario, flag in PR comment.',
        example: '# DataGen Agent API call (from CI pipeline):\ncurl -X POST https://datagen.internal/api/seed \\\n  -H "Authorization: Bearer $DATAGEN_TOKEN" \\\n  -d \'{"schema":"payment_transaction","count":500,"env":"ci","pii_safe":true}\'\n# Returns: dataset seeded, DB connection string for test run\n\n# GitHub Actions integration:\n- name: Seed test data\n  run: |\n    curl -sX POST $DATAGEN_URL/seed -d \'{"schema":"$SCHEMA","count":200,"env":"ci"}\'\n- name: Run integration tests\n  run: npm run test:integration\n- name: Teardown data\n  if: always()\n  run: curl -sX DELETE $DATAGEN_URL/seed/ci',
        tools: ['LangChain + Azure OpenAI', 'Faker / Tonic.ai', 'Playwright', 'Cucumber', 'GitHub Actions'],
        owner: 'QA Lead + DevOps', timeline: 'Week 3–6', effort: '4–6 days',
        successCriteria: 'Test data provisioning < 2 min (was 4–16 hrs). Zero production data in non-prod environments. QA Orchestrator coverage: 100% of story ACs have a corresponding test scenario. Test suite run time unchanged or faster.' },
      { title: 'AI Release Manager + Compliance-as-Code Orchestrator (Phase 6)', icon: '🚦', category: 'Release / Compliance', phase: 'Phase 6 — CD & Release Gate',
        current: 'Manual CAB approval for all releases (3–7 day wait). Compliance checks done by humans before each release. No automated quality or security gate before production.',
        change: 'AI Release Manager validates quality, security, and performance gates and approves low-risk releases automatically. Compliance-as-Code Orchestrator validates GDPR, DORA, and Basel III rules on every commit. (← assistive: Tech Lead retains override authority and reviews all gate decisions.)',
        how: '1. AI Release Manager: LangChain agent ingesting: SAST report, test pass rate, performance delta, compliance score. Decision tree: if all gates green → auto-approve. If any gate amber → Tech Lead notification + 1-hr window to review. If any gate red → block + incident ticket. 2. Compliance-as-Code Orchestrator: encode GDPR (no PII in logs), DORA (change failure rate < 5%), Basel III (model explainability present) as executable rules. Run against every PR before merge. 3. Configure rule library in GitOps repo — CISO reviews and approves rule changes via PR. 4. Wire all decisions to Jira/Slack: every auto-approve and every block posts to #releases channel.',
        example: '# AI Release Manager decision logic (pseudocode):\nrelease_decision = release_manager.evaluate({\n  "sast_critical_findings": 0,        # must be 0\n  "test_pass_rate": 98.5,              # must be >= 95%\n  "performance_regression": -1.2,     # must be > -5%\n  "compliance_score": 97,             # must be >= 90\n  "last_production_incident_hrs": 72  # must be > 24\n})\n\n# Result: {"decision": "APPROVED", "risk_level": "LOW",\n#          "rationale": "All gates green. Auto-approved."}\n# OR:     {"decision": "HOLD", "risk_level": "MEDIUM",\n#          "rationale": "Test pass rate 93%. Tech Lead review required."}',
        tools: ['LangChain + Azure OpenAI', 'Snyk', 'GitHub Actions', 'OPA (Open Policy Agent)', 'Slack API'],
        owner: 'DevOps Engineer + Tech Lead', timeline: 'Week 5–8', effort: '5–7 days',
        successCriteria: 'Manual CAB approval eliminated for low-risk releases. AI Release Manager auto-approving ≥ 70% of releases. Compliance-as-Code Orchestrator catching GDPR/DORA violations before merge. Zero High/Critical findings reaching production.' },
    ],
    devSecOps: [
      { title: 'Secure-by-Design Architect: AI IaC policy validation on every PR', icon: '🏗️', pipelineStage: 'Code → PR → CD', priority: 'P1 — Week 2',
        current: 'IaC written manually. Security misconfigurations found in production. No automated policy validation. CISO reviews only at release gate (days later).',
        change: 'Secure-by-Design Architect agent validates every IaC change against cloud security policies at PR time. Misconfigurations blocked before merge. CISO reviews exceptions only (← assistive: Tech Lead can override with documented justification).',
        how: '1. Deploy Checkov in CI pipeline (GitHub Actions). 2. Build Secure-by-Design Architect on LangChain: ingests Checkov output + IaC diff → classifies findings (Critical/High/Advisory) → generates human-readable explanation + recommended fix. 3. Load bank-specific policy library: approved VPC patterns, encryption requirements, access policy templates. 4. Wire agent to post findings as PR comments with severity tags. 5. CISO reviews and approves the policy library quarterly via PR — no ad-hoc changes.',
        example: '# .github/workflows/iac-security.yml\n- name: IaC Security Scan (Checkov)\n  uses: bridgecrewio/checkov-action@master\n  with:\n    directory: ./terraform\n    framework: terraform\n    soft_fail: false\n    output_format: json\n    output_file_path: checkov-report.json\n\n- name: Secure-by-Design Architect Analysis\n  run: |\n    python secure_by_design_agent.py \\\n      --checkov-report checkov-report.json \\\n      --iac-diff ${{ github.event.pull_request.diff_url }} \\\n      --post-to-pr ${{ github.event.pull_request.number }}\n# Agent posts: "CRITICAL: S3 bucket has public access enabled. This violates\n# CKV_AWS_20. Recommended fix: add block_public_acls = true"',
        tools: ['Checkov', 'LangChain + Azure OpenAI', 'Terraform', 'GitHub Actions', 'OPA'],
        metrics: 'IaC violations reaching production: reduced by 90%. CISO review time: weekly → exception-only. IaC PR review time: days → minutes (agent runs in < 60s).' },
      { title: 'Compliance-as-Code Orchestrator: GDPR / DORA / Basel III on every commit', icon: '⚖️', pipelineStage: 'Code Commit → PR', priority: 'P1 — Week 6',
        current: 'Compliance checks are manual, periodic (quarterly), and done by humans. Compliance violations discovered late — after code is in production.',
        change: 'Compliance-as-Code Orchestrator encodes GDPR, DORA, and Basel III rules as executable policies. Validated on every commit — violations blocked at PR. Continuous compliance assurance, not periodic audits. (← assistive: Compliance team reviews flagged violations and approves exceptions.)',
        how: '1. Encode GDPR rules: no PII in logs (detect via regex + LLM classification), data retention policies in schema definitions, consent check in API routes. 2. Encode DORA rules: change failure rate alert if CFR > 5%, recovery time SLA alert. 3. Encode Basel III: model explainability report required before any model-driven feature merge. 4. Deploy as OPA (Open Policy Agent) policies in CI pipeline. Build LangChain layer to generate human-readable explanations when a rule fires. 5. Configure auto-ticket in compliance backlog for every violation: compliance team reviews within 48 hrs.',
        example: '# OPA policy: GDPR — no PII in logs (Rego):\npackage gdpr.logging\nviolation[msg] {\n  input.log_fields[field]\n  re_match(`(?i)(ssn|social_security|card_number|date_of_birth|email)`, field)\n  msg := sprintf("GDPR violation: PII field \'%v\' found in log statement at %v", [field, input.location])\n}\n\n# Basel III: model explainability check (Python agent):\nif "model_prediction" in changed_api_routes:\n    explainability_report = mrm_agent.check_explainability(model_id)\n    if not explainability_report.is_compliant:\n        block_merge("Basel III: Explainability report required before deploying model-driven feature")',
        tools: ['OPA (Open Policy Agent)', 'LangChain + Azure OpenAI', 'GitHub Actions', 'Drata / Vanta'],
        metrics: 'Compliance violations reaching production: target 0. Manual audit prep: 2–5 person-weeks → < 1 day. Compliance coverage: 60% → 100% of commits checked.' },
      { title: 'MRM Agent: Model Risk Monitoring with kill-switch', icon: '🎛️', pipelineStage: 'All Phases (ongoing)', priority: 'P2 — Week 8',
        current: 'AI models deployed without model risk governance. No monitoring for model drift, explainability, or bias. SR 11-7 compliance not addressed.',
        change: 'MRM Agent monitors all model-driven features: tracks drift, generates explainability reports, flags bias, and triggers kill-switch if risk threshold exceeded. (← assistive: MRO (Model Risk Officer) reviews and approves all risk threshold parameters.)',
        how: '1. Define model registry: enumerate all AI/ML models in production (credit scoring, fraud detection, recommendation engines). 2. Configure MRM Agent with risk parameters (approved by MRO): drift threshold (e.g., PSI > 0.2), explainability score floor, bias metric limits. 3. MRM Agent runs weekly batch checks: compares model output distribution vs baseline, generates SHAP-based explainability report, checks protected attribute correlations. 4. Configure kill-switch: if any parameter breaches threshold → MRM Agent auto-disables model feature flag → alerts Tech Lead + MRO. 5. Store all explainability reports in S3/Azure Blob (7-year retention for SR 11-7).',
        example: '# MRM Agent weekly check (Python LangChain):\nresult = mrm_agent.run_weekly_check({\n  "model_id": "fraud_detection_v2",\n  "prediction_sample": last_7_days_predictions,\n  "baseline_sample": baseline_predictions\n})\n# Output:\n# {"drift_score": 0.12, "threshold": 0.20, "status": "OK",\n#  "explainability_score": 0.84, "bias_flag": false,\n#  "recommendation": "Model performing within parameters. No action required."}\n\n# Kill-switch trigger:\nif result["drift_score"] > 0.20:\n    feature_flags.disable("fraud_detection_v2")\n    alert_mro(result)',
        tools: ['LangChain + Azure OpenAI', 'SHAP', 'Evidently AI', 'Azure ML', 'LaunchDarkly (feature flags)'],
        metrics: 'SR 11-7 compliance: achieved. Model drift incidents in production: detected before user impact. Mean time to detect model degradation: weeks → hours.' },
      { title: 'Multi-Agent Governance Controller: bypass detection and audit trail', icon: '🛡️', pipelineStage: 'All agent handoffs', priority: 'P1 — Week 6',
        current: 'No governance layer over AI agent actions. Agents could produce output that bypasses human oversight. No audit trail of agent decisions.',
        change: 'Multi-Agent Governance Controller intercepts all agent handoffs, validates that each transition follows approved protocols, detects bypass attempts, and maintains an immutable audit trail. (← assistive: governance board reviews Controller configuration quarterly.)',
        how: '1. Wrap LangGraph StateGraph transitions with a governance middleware layer. Every agent handoff passes through the Controller before state is updated. 2. Controller checks: was the previous step completed with required human approval? Is the receiving agent authorised for this data type? Did any agent attempt to skip a required gate? 3. If bypass detected: block transition, log to governance audit trail, alert Tech Lead within 5 min. 4. Audit trail: every agent decision logged to append-only store (S3 Object Lock / Azure Immutable Blob). 5. Monthly governance review: Controller logs reviewed for anomalies; any bypass attempt investigated.',
        example: '# Governance Controller middleware:\nclass GovernanceController:\n    REQUIRED_APPROVALS = {\n        "story_gen → code_gen": "product_owner_approved",\n        "review_agent → release_gate": "critical_findings_resolved",\n        "release_gate → production": "tech_lead_approved OR auto_approve_criteria_met"\n    }\n    def validate_transition(self, from_node, to_node, state):\n        rule = self.REQUIRED_APPROVALS.get(f"{from_node} → {to_node}")\n        if rule and not self._evaluate(rule, state):\n            self._log_bypass_attempt(from_node, to_node, state)\n            raise GovernanceViolation(f"Transition blocked: {rule} not satisfied")\n        self._log_approved_transition(from_node, to_node)',
        tools: ['LangGraph middleware', 'Azure Immutable Blob / S3 Object Lock', 'PagerDuty', 'Slack API'],
        metrics: 'Agent bypass attempts: detected within 5 min (100% detection). Audit trail completeness: 100% of transitions logged. Governance board sign-off: achieved before production go-live.' },
    ],
    aiOps: [
      { title: 'Self-healing CI/CD with ML failure prediction', icon: '🔄', layer: 'Pipeline Reliability', priority: 'P1 — Week 10',
        current: 'Build failures detected after the fact. On-call engineer manually diagnoses and restarts failed pipelines. No prediction of flaky tests or likely failures.',
        change: 'ML model trained on build history predicts likely failures before they occur — skipping known-flaky tests, pre-caching dependencies. Self-healing: failed pipeline steps auto-retry with adjusted parameters. (← assistive: DevOps Engineer reviews all auto-remediation actions in Agent Ops dashboard.)',
        how: '1. Enable GitHub Actions build telemetry export (step durations, failure rates, flaky test history) to Datadog or custom store. 2. Train failure prediction model on 6 months of build history. Input: changed file paths, time of day, branch. Predict: probability of failure in each pipeline step. 3. Configure self-healing rules: if step probability of failure > 60% → increase timeout; if test known-flaky → retry up to 3×. 4. Wire to Slack: every self-heal event posted to #ci-health with root cause and action taken. 5. DevOps reviews daily: validate that auto-remediation actions were appropriate.',
        example: '# ML failure predictor (simplified):\nfrom sklearn.ensemble import GradientBoostingClassifier\npredictions = model.predict_proba([{\n  "changed_paths": ["src/payments/**"],\n  "hour_of_day": 14,\n  "branch_type": "feature",\n  "author_commit_rate": 0.8\n}])\n# {"step_probabilities": {"unit_tests": 0.12, "integration_tests": 0.68, "e2e": 0.22}}\n\n# Self-healing action:\nif predictions["integration_tests"] > 0.60:\n    pipeline.set_timeout("integration_tests", timeout_multiplier=1.5)\n    pipeline.enable_retry("integration_tests", max_retries=2)',
        tools: ['GitHub Actions', 'Datadog ML', 'scikit-learn', 'Slack API'],
        metrics: 'Build failure rate: reduced 30–40% via prediction. Mean time to fix failed build: 2 hrs → 15 min (self-heal). Engineer on-call pages for CI: reduced by 50%.' },
      { title: 'AIOps platform: all production alerts managed by AI', icon: '🚨', layer: 'Incident Response', priority: 'P1 — Week 10',
        current: '200+ alerts/day. L1 engineers spend 30% of on-call time on false alarms. MTTD: 15–45 min. Wrong team paged 30% of the time. PIRs written manually (often skipped).',
        change: 'AIOps platform (Dynatrace Davis AI or Datadog AI) manages all alerts: 90% noise reduction, NLP-based routing to correct team, auto-remediation of known patterns. AI PIR Generator produces draft PIR in 45 min. (← assistive: P1 incidents always escalated to human engineer with AI pre-analysis.)',
        how: '1. Deploy Dynatrace Davis AI (30-day trial → enterprise). Auto-instrument all services with OpenTelemetry. 2. Let AI learn baseline for 2 weeks — do not modify alert rules during this period. 3. Configure auto-remediation runbooks for top 5 known failure patterns (pod restart, cache flush, DB connection pool reset). 4. Wire NLP classifier to PagerDuty routing: incident text → team routing confidence score. If > 85% → auto-route; < 85% → triage queue. 5. AI PIR Generator: 2 hrs after any P1/P2 resolution → generate draft PIR from incident timeline, actions taken, root cause tags.',
        example: '# OpenTelemetry auto-instrumentation (Node.js):\nOTEL_SERVICE_NAME=payments-api \\\nOTEL_EXPORTER_OTLP_ENDPOINT=http://dynatrace-collector:4317 \\\nOTEL_RESOURCE_ATTRIBUTES="team=payments,env=production" \\\nnode --require @opentelemetry/auto-instrumentations-node/register server.js\n\n# Auto-remediation rule (Dynatrace):\n# Trigger: error_rate(payments-api) > 5% for 3 min\n# Action: POST https://k8s/apis/apps/v1/namespaces/prod/deployments/payments/restart\n# Cooldown: 15 min\n# Notify: #payments-oncall Slack',
        tools: ['Dynatrace Davis AI', 'Datadog AI', 'PagerDuty AIOps', 'OpenTelemetry'],
        metrics: 'Alert volume: 200/day → < 20/day actionable. MTTD: 15–45 min → < 3 min. Wrong-team routing: 30% → < 5%. PIR completion rate: 40% → > 90%.' },
      { title: 'Telemetry Sentinel: production signals to backlog automatically', icon: '📡', layer: 'Feedback Loop', priority: 'P2 — Week 12',
        current: 'Production issues (high error rates, slow journeys, model drift) reach the backlog weeks later — if ever. Tech debt prioritised independently of live user impact.',
        change: 'Telemetry Sentinel monitors production telemetry and automatically creates Jira tickets for anomalies meeting defined thresholds. Business Risk Scores surface governance-level risks to the dashboard. (← assistive: PO reviews all auto-created tickets weekly before promoting to sprint.)',
        how: '1. Connect Datadog/Dynatrace to Telemetry Sentinel via webhook on alert rules. 2. Define signal-to-ticket rules: high error rate → bug P2, slow page load → performance story, model drift → MRM task. 3. Configure Business Risk Score: composite metric from error rate, compliance violations, model drift, and security incidents. Publish to governance dashboard. 4. All auto-created tickets tagged "production-signal" — PO reviews weekly. 5. Track % of sprint work originating from production signals (target: 20–30%).',
        example: '# Telemetry Sentinel signal rules (YAML config):\nsignal_rules:\n  - name: high_error_rate\n    condition: error_rate > 1.0% for 15min\n    action: create_jira_ticket\n    jira_template:\n      project: PAYMENTS\n      issuetype: Bug\n      priority: P2\n      summary: "⚠ High error rate: {endpoint} — {error_rate}%"\n      labels: [production-signal, auto-generated]\n\n  - name: compliance_policy_violation\n    condition: compliance_score < 90\n    action: create_jira_ticket AND alert_governance_dashboard\n    business_risk_weight: 0.4',
        tools: ['Datadog Watchdog', 'Dynatrace Davis', 'Jira REST API', 'Slack API'],
        metrics: 'Mean time from production signal to sprint: weeks → 1 sprint. % sprint work from production signals: 0% → 20–30%. Governance team alert lag: days → real-time.' },
      { title: 'ML-based predictive capacity and cost optimisation', icon: '📈', layer: 'Capacity', priority: 'P2 — Week 12',
        current: 'Reactive scaling — scale after the spike hits. Manual capacity planning quarterly. Over-provisioned 40% of time (cost waste). No ML-informed scheduling.',
        change: 'ML predictive scaling forecasts load 30–60 min ahead based on historical patterns and calendar signals. Kubernetes auto-scales proactively. Cost optimiser right-sizes idle pods. (← assistive: DevOps Engineer reviews scaling recommendations weekly.)',
        how: '1. Enable AWS Predictive Scaling or KEDA for Kubernetes event-driven autoscaling. 2. Configure prediction horizon: 60-min ahead forecast using historical traffic + US Bank calendar (payroll cycles, month-end). 3. Set scaling guardrails: min replicas = 2, max = 20. Alert if predicted load approaches max guardrail. 4. Cost optimiser: Kubecost or AWS Compute Optimizer reviews idle pod usage weekly — suggests right-sizing. 5. DevOps reviews weekly recommendations before applying — never auto-apply major sizing changes.',
        example: '# KEDA — event-driven autoscaling (payments queue):\napiVersion: keda.sh/v1alpha1\nkind: ScaledObject\nmetadata:\n  name: payments-processor-scaler\nspec:\n  scaleTargetRef:\n    name: payments-processor\n  minReplicaCount: 2\n  maxReplicaCount: 20\n  triggers:\n    - type: azure-servicebus\n      metadata:\n        queueName: payment-requests\n        messageCount: "100"  # 1 replica per 100 queued messages\n    - type: cron\n      metadata:\n        timezone: "America/Chicago"\n        start: "0 9 * * 1-5"   # Pre-scale every weekday morning\n        end:   "0 18 * * 1-5"\n        desiredReplicas: "8"',
        tools: ['KEDA', 'AWS Predictive Scaling', 'Kubernetes HPA', 'Kubecost', 'Datadog Forecast'],
        metrics: 'Scaling lag: reactive → proactive (30–60 min ahead). Compute cost: reduced 20–30% via right-sizing. Capacity-related incidents: target 0.' },
    ],
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
      operationalSavings: '$400K–$700K (fully autonomous ops)',
      complianceAutomation: '$300K–$600K (full Compliance-as-Code coverage eliminates manual audit function; continuous regulatory assurance)',
      securityIncidentReduction: '$250K–$500K (Secure-by-Design enforced at every deployment gate; security debt eliminated)',
      modelRiskAvoidance: '$400K–$800K (MRM Agent with kill-switch prevents catastrophic model failures; meets SR 11-7 model risk guidance)',
      governanceEfficiency: '$150K–$300K (Multi-Agent Governance Controller eliminates inter-team governance overhead and escalation delays)'
    },
    orgChanges: [
      { title: 'Restructure to 2 human roles: Product Definer + Product Builder', icon: '🔁', who: 'CTO + Product Owner + Engineering Manager', timeline: 'Week 14–20 (after Pilot)', effort: '1 week planning + 6 weeks transition',
        what: 'Stage 3 deploys 21 autonomous agents across all PDLC phases. The only remaining human roles are: Product Definer (sets outcomes and accepts deliverables) and Product Builder (supervises agent orchestration and maintains quality gates). All other roles either transition to these two or are redeployed.',
        how: '1. Complete the 6-week pilot phase FIRST — never begin the 2-role transition until 21 agents pass 80%+ acceptance rate. 2. Identify Definer and Builder candidates internally: Definer = former Product Owner/senior BA; Builder = Tech Lead/Senior Developer. Both roles require intensive reskilling (3–4 weeks). 3. Map every former team member to one of: (a) Product Definer, (b) Product Builder, (c) redeployment to another team, (d) reskilling programme. 4. Run parallel for 6 weeks: former team and 2-person pilot team work concurrently — agents handle all Phase 3–6 work. 5. Full transition only after pilot achieves 80%+ for 2 consecutive weeks.',
        example: 'Transition map (example 8-person team → 2-role model):\n  BEFORE               →  AFTER (or transition path)\n  Product Owner        →  Product Definer (reskill: outcome briefs, acceptance criteria)\n  Tech Lead            →  Product Builder (reskill: agent monitoring, prompt tuning)\n  3 Developers         →  1 joins Product Builder pool; 2 redeployed to other teams\n  QA Lead              →  Reskilled as Product Builder for QA agent oversight\n  DevOps Engineer      →  Platform support role (STUMP platform operations)\n  Scrum Master         →  Redeployed (ceremonies eliminated by autonomous cadence)\n\nAll transitions announced in week 14. Reskilling budget: 3–4 weeks per person.',
        successCriteria: 'No 2-role transition before pilot phase 80%+ gate is passed. All former team members have a documented transition path. Zero involuntary departures (internal redeployment or reskilling for all). Board-level operating model approval received.' },
      { title: 'Product Definer role: outcomes over backlog', icon: '🎯', who: 'Product Owner → Product Definer', timeline: 'Week 1–4 (design) + Week 14 (go-live)', effort: '3-week reskilling',
        what: 'The Product Definer does not write stories or manage a backlog. They write weekly outcome briefs — the "what and why" — and approve agent-generated deliverables. A fundamental mindset shift from managing tasks to setting outcomes.',
        how: '1. Reskilling curriculum (3 weeks): Week 1 — outcome thinking vs task thinking (design thinking workshop). Week 2 — writing effective outcome briefs (practice with real features, get feedback from agents). Week 3 — approving and rejecting agent output (criteria: does it meet the outcome, not "do I like the code?"). 2. Outcome brief template (see example). 3. Weekly cadence: Monday — Definer writes weekly outcome brief → agents decompose. Thursday — Definer reviews agent-produced artifacts. Friday — Definer approval or rejection with specific feedback. 4. Definer does NOT read Jira tickets or story points. Reviews: live product output, acceptance criteria coverage, user journey completeness.',
        example: 'Outcome brief template (Monday weekly):\n  OUTCOME: Allow business banking customers to schedule recurring international payments\n  CONSTRAINTS:\n    - Must comply with OFAC sanctions check on every beneficiary\n    - Max 5 payment rules per account (regulatory limit)\n    - Must be accessible from both web and mobile\n  ACCEPTANCE CRITERIA:\n    - Customer can create, edit, and delete a recurring payment rule\n    - Failed payments generate a notification within 2 minutes\n    - Sanctions check occurs synchronously before confirming schedule\n  OUT OF SCOPE THIS WEEK:\n    - Multi-currency FX conversion (separate outcome next week)\n  DEADLINE: Thursday review\n\n→ Agents receive this brief and decompose: FeatureGen → StoryGen → CodeGen → TestGen → Deploy',
        successCriteria: 'Definer writing outcome briefs (not stories) from Week 14. Average brief-to-deployed-feature cycle: < 2 days (non-regulated). Definer approval rate ≥ 85% without rewrite requests. Board satisfied with outcome-driven roadmap visibility.' },
      { title: 'Product Builder role: agent supervision and quality gates', icon: '🔧', who: 'Tech Lead → Product Builder', timeline: 'Week 4–12 (platform build) + Week 14 (go-live)', effort: '4-week reskilling',
        what: 'The Product Builder does not write code or tests. They supervise agent orchestration, maintain quality gates, tune agent prompts when output degrades, and escalate Sev-1 incidents. A shift from producer to platform engineer.',
        how: '1. Reskilling curriculum (4 weeks): Week 1–2 — STUMP platform operations (deploying agents, reading StateGraph logs, interpreting quality scores). Week 3 — prompt engineering for production agents (structured feedback to tune agent behaviour). Week 4 — exception handling: when and how to escalate, roll back, or override an agent decision. 2. Daily Builder rituals: 15-min agent health check (quality scores, SLOs, error rates), review overnight exception queue, tune any agent below 80% acceptance. 3. Builder has full override authority: can pause any agent, roll back a deployment, or disable a feature flag if agent output is unsafe.',
        example: 'Builder daily routine:\n  08:30  Review Agent Ops dashboard — check all 21 agent SLOs\n         Flag: QA Orchestrator acceptance rate dropped to 74% → add to tuning queue\n  09:00  Review exception queue — 3 items from overnight\n         Item 1: Secure-by-Design blocked a release → review justification → approve override\n         Item 2: FeatureGen low-confidence output → reject, add context to brief\n         Item 3: Auto-remediation pod restart loop → investigate root cause\n  10:00  Tuning sprint (when needed): rewrite QA Orchestrator system prompt\n         Test on 20 historical items → acceptance rate 88% → promote\n  Async: Review all Sev-1 escalations; respond to Product Definer questions about agent constraints',
        successCriteria: 'Builder has completed 4-week reskilling before Week 14. All 21 agents within SLO 95%+ of the time. Builder average response time to agent quality degradation: < 4 hrs. Zero production incidents due to undetected agent drift.' },
      { title: 'Workforce transition and reskilling programme', icon: '🎓', who: 'HR + CTO + Engineering Manager', timeline: 'Week 8–20 (parallel with pilot)', effort: '3–4 weeks per person',
        what: 'The transition from 8+ roles to 2 is the most significant people change in Stage 3. Without a structured reskilling and redeployment programme, the transformation will face resistance, attrition, and ethical risk.',
        how: '1. In Week 8: hold all-hands to explain the transformation, the 2-role model, and the transition support available. No surprises — every person knows their path before the pilot begins. 2. Reskilling budget: $3K–$5K per person for external courses (AI product management, LangGraph developer, prompt engineering). 3. Internal mobility: work with HR to identify open Product Builder and Definer roles across other product teams — Stage 3 creates exportable talent. 4. For team members who choose to leave: enhanced severance + 60-day job placement support. 5. Transition tracking: monthly board report showing % of team with confirmed transition path.',
        example: 'Workforce transition dashboard (monthly board update):\n  Role                | Count | Transition Path          | Status\n  ---                 | ---   | ---                      | ---\n  Product Owner       | 1     | → Product Definer        | Reskilling wk 2/3 ✅\n  Tech Lead           | 1     | → Product Builder        | Reskilling wk 3/4 ✅\n  Senior Developer    | 1     | → Product Builder pool   | Reskilling wk 1/4 🔄\n  Developer           | 2     | → Redeployed (Team B/C)  | Offers accepted ✅\n  QA Lead             | 1     | → Product Builder (QA)   | Reskilling wk 2/4 🔄\n  Scrum Master        | 1     | → Agile Coach (CoE)      | Transfer confirmed ✅\n  DevOps              | 1     | → Platform Eng (STUMP)   | Confirmed ✅',
        successCriteria: '100% of team members have a documented, agreed transition path before Week 14 cutover. Zero involuntary redundancies without internal placement or enhanced package. Reskilling completion rate: 100%. Board receives monthly transition dashboard.' },
      { title: 'Board-level operating model approval and governance framework', icon: '🏛️', who: 'CTO + CISO + CCO + Board', timeline: 'Week 1–4 (proposal) + Week 14 (approval gate)', effort: '5–10 days across stakeholders',
        what: 'A 2-role autonomous AI model managing a regulated banking product requires explicit board-level approval. This is not a team-level decision — it involves regulatory risk, model risk, workforce restructuring, and significant capital investment.',
        how: '1. Prepare board briefing (see example). 2. CCO (Chief Compliance Officer) review: present Compliance-as-Code Orchestrator and MRM Agent parameters for approval before any autonomous agent touches regulated data. 3. CISO review: data access scope, secrets management, audit trail completeness. Sign off on Governance Controller architecture. 4. Risk committee: review Sev-1 escalation protocols, kill-switch procedures, rollback plans. 5. Formal board resolution approving: (a) 2-role operating model, (b) STUMP Platform architecture, (c) agent autonomy parameters, (d) workforce transition plan.',
        example: 'Board briefing — executive summary (1 page):\n  PROPOSAL: Deploy STUMP Agentic Platform for [Product Name]\n  INVESTMENT: $2.5M–$4.5M (capex) | ROI: 5.5× in 18–24 months\n  WORKFORCE: Transition from 8+ roles to 2 (Product Definer + Product Builder)\n  REGULATORY: MRM Agent (SR 11-7 compliant) + Compliance-as-Code (GDPR/DORA/Basel III)\n  RISK CONTROLS:\n    • Kill-switch: any model/agent disabled in < 30 seconds by Product Builder\n    • Sev-1: always escalated to human engineer (never autonomous)\n    • Governance Controller: all agent transitions logged to immutable audit trail\n    • Pilot: mandatory 6-week pilot before full transition (80% acceptance gate)\n  BOARD ASKS:\n    1. Approve operating model transition (2-role structure)\n    2. Approve $3.5M budget (midpoint)\n    3. Confirm regulatory engagement with OCC/FDIC before go-live',
        successCriteria: 'Formal board resolution received before Week 14 transition. CCO and CISO sign-off on data scope and compliance architecture. Regulatory engagement initiated (OCC/FDIC notification). All governance parameters locked in writing before pilot cutover.' },
    ],
    toolsChanges: [
      { title: 'STUMP Agentic Platform: LangGraph + LangChain + Agent Skills', icon: '⚙️', category: 'Platform Foundation', phase: 'All Phases (autonomous)',
        current: 'No autonomous agent platform. Stage 2 agents are assistive (← on-demand). Platform does not support continuous orchestration, inter-agent context sharing, or autonomous decision cycles.',
        change: 'STUMP Agentic Platform deploys on Azure with LangGraph StateGraph orchestrating 21 agents. Every agent uses ⚙ gear notation — platform-managed, autonomous. Agent Skills provide pre-built tool integrations. Agents run on platform cadence, not human request.',
        how: '1. Platform infrastructure: Azure Container Apps (agent runtime), Azure OpenAI (LLM), Azure Service Bus (inter-agent messaging), Azure Cosmos DB (shared state store), Azure Key Vault (secrets). 2. LangGraph StateGraph: define all 21 agent nodes + conditional transition logic. State schema holds full PDLC context (feature brief → stories → code → tests → deploy). 3. Agent Skills library: pre-built skills for GitHub, Jira, Azure DevOps, Confluence, Datadog, Snyk — agents invoke skills as tools. 4. Platform controller: autonomous orchestration loop runs on configurable cadence (default: on demand triggered by Product Definer weekly brief). 5. Observability: all agent invocations, tool calls, and state transitions logged to Azure Application Insights.',
        example: '# STUMP Platform — agent invocation (platform-managed):\n# Platform receives Product Definer weekly brief → orchestrates full ADLC\nstump_platform.process_outcome_brief({\n  "brief_id": "2024-W15-payments",\n  "outcome": "Allow customers to schedule recurring international payments",\n  "constraints": ["OFAC check required", "5 rules max per account"],\n  "acceptance_criteria": ["...", "..."],\n  "deadline": "2024-04-19"\n})\n\n# Platform autonomously runs:\n# ⚙ Discovery Agent → ⚙ FeatureGen → ⚙ StoryGen → ⚙ CodeGen\n# → ⚙ Code Reviewer → ⚙ QA Orchestrator → ⚙ DataGen\n# → ⚙ AI SAST → ⚙ AI Release Manager → ⚙ Deploy Agent\n# All within ADLC loop — Product Definer approves final output',
        tools: ['LangGraph', 'LangChain', 'Azure OpenAI GPT-4o', 'Azure Container Apps', 'Azure Service Bus', 'Azure Cosmos DB'],
        owner: 'Product Builder + DevOps', timeline: 'Week 4–12', effort: '8 weeks engineering',
        successCriteria: 'STUMP Platform running all 21 agents in staging. End-to-end E2E test: outcome brief → deployed feature in < 4 hrs (non-regulated). All agent SLOs met. Platform uptime ≥ 99.5%.' },
      { title: 'Autonomous ADLC Pipeline: Code Generator → CI → Test → Deploy', icon: '🚀', category: 'Autonomous Delivery', phase: 'Phase 3–6 (automated end-to-end)',
        current: 'Phases 3–6 involve manual coding, testing, and deployment with human oversight at every step. Lead time for a user story: 7–21 days. Multiple handoffs between developers, QA, and DevOps.',
        change: 'STUMP Platform runs a fully autonomous ADLC for non-regulated user stories: Code Generator (~1 hr) → Build + CI (~20 min) → AI test suite (~30 min) → auto-deploy (~30 min) → single Product Definer approval (~30 min). Total: < 3 hrs for a standard user story. (Human: Provide Intent → Review → Approve Only.)',
        how: '1. Code Generator (⚙ Azure OpenAI + GitHub Copilot): reads story + ACs from STUMP state → generates implementation + unit tests. Commits to feature branch. 2. CI Pipeline (⚙ GitHub Actions): on commit → run build, unit tests, SAST, IaC scan. All AI-gated — failures auto-remediated or escalated. 3. AI Test Suite (⚙ QA Orchestrator + DataGen): generates integration + BDD tests, seeds data, runs full suite. Test coverage report auto-generated. 4. AI Release Manager (⚙): validates all quality gates → auto-deploys to staging. 5. Product Definer approval: one-click approve/reject with AI-generated summary of what was built, test coverage, compliance status.',
        example: '# ADLC pipeline execution log (abbreviated):\n[10:00] Product Definer submits outcome brief: "Recurring international payments"\n[10:02] ⚙ Discovery Agent: ingests brief → maps to existing capabilities\n[10:05] ⚙ FeatureGen Agent: generates 6 user stories with ACs\n[10:08] ⚙ StoryGen Agent: decomposes to sprint tasks, estimates effort\n[10:15] ⚙ Code Generator: writes implementation for Story 1 of 6 (payments rule engine)\n[11:10] ⚙ CI Pipeline: build ✅ | unit tests 98.3% ✅ | SAST 0 critical ✅\n[11:30] ⚙ QA Orchestrator: generated 23 BDD scenarios → all passing ✅\n[11:45] ⚙ AI Release Manager: all gates green → deployed to staging ✅\n[12:00] Product Definer notified: "Story ready for approval"\n        Summary: Payments rule engine implemented. 23 tests passing. OFAC check integrated.\n[12:30] Product Definer: APPROVED → auto-deploy to production triggered',
        tools: ['Azure OpenAI GPT-4o', 'GitHub Copilot', 'GitHub Actions', 'LangGraph', 'Playwright', 'Snyk'],
        owner: 'STUMP Platform (autonomous) — Product Builder monitors', timeline: 'Week 10–14 (build) + Week 14 (go-live)', effort: '4 weeks engineering',
        successCriteria: 'Non-regulated user story: brief → production in < 3 hrs. Regulated user story: < 1 day (with mandatory compliance gate stops). Code Generator output acceptance rate ≥ 85%. Test coverage ≥ 90% per story.' },
      { title: 'AI-native ALM: replace Jira/ADO with intent-driven platform', icon: '📋', category: 'ALM', phase: 'Phase 1–2 — Planning',
        current: 'Jira/ADO used for manual backlog management. Product Owner writes tickets. Story points estimated by humans. Backlog grooming: 3–4 hrs/sprint. All tasks human-created.',
        change: 'AI-native ALM ingests Product Definer outcome briefs → auto-generates work items, estimates, and priority scores. No human-created Jira tickets. All work tracked automatically from agent execution logs. Product Definer views: outcome completion %, not sprint velocity.',
        how: '1. Evaluate AI-native ALM options: Shortcut + AI (most mature), or build custom STUMP work tracker on Azure Cosmos DB. 2. Outcome brief → work item decomposition: STUMP auto-creates work items from FeatureGen + StoryGen agent output. Humans never write tickets. 3. Progress tracking: every agent execution updates work item status. Product Definer sees % complete per outcome. 4. Decommission Jira story point estimation — replace with STUMP effort estimation from historical agent run durations. 5. Retain Jira for compliance evidence only (read-only mirror of STUMP state for audit trail).',
        example: '# STUMP work tracker auto-create (from FeatureGen output):\nfor story in feature_gen_output.user_stories:\n    stump.create_work_item({\n        "title": story.title,\n        "type": "user_story",\n        "acceptance_criteria": story.acs,\n        "outcome_ref": brief_id,\n        "assigned_to": "⚙ Code Generator Agent",\n        "estimated_duration_hrs": story.estimated_hrs,\n        "created_by": "STUMP Platform (automated)"\n    })\n# Product Definer dashboard:\n# Outcome: Recurring International Payments\n#   ▓▓▓▓▓▓▓▓░░ 80% complete (5 of 6 stories deployed)\n#   Estimated completion: 3 hrs',
        tools: ['Azure Cosmos DB', 'LangGraph', 'Shortcut AI', 'Jira (compliance mirror only)'],
        owner: 'Product Builder', timeline: 'Week 6–10', effort: '2–3 weeks',
        successCriteria: 'Zero human-created Jira tickets from Week 14. Outcome completion % visible to Product Definer in real time. Jira retained as read-only compliance mirror. Agent execution auto-updates work item status 100% of the time.' },
      { title: 'Governance Agent Stack: Secure-by-Design + Compliance-as-Code + MRM + Controller', icon: '🛡️', category: 'Governance (autonomous)', phase: 'All Phases — every deployment gate',
        current: 'Governance checks are manual and periodic. Compliance reviews take weeks. Model risk assessed infrequently. No autonomous enforcement of security or regulatory policies.',
        change: 'Four specialised governance agents run autonomously at every deployment gate: (1) Secure-by-Design Architect — IaC policy; (2) Compliance-as-Code Orchestrator — GDPR/DORA/Basel III; (3) MRM Agent — model drift + kill-switch; (4) Governance Controller — agent bypass detection. Only exceptions escalate to human. (⚙ fully autonomous — no human in the loop for standard flows.)',
        how: '1. Secure-by-Design Architect (⚙): runs on every IaC change. Blocks non-compliant configurations autonomously. Only CISO-defined waivers allowed. 2. Compliance-as-Code Orchestrator (⚙): validates GDPR, DORA, Basel III on every commit. Blocks non-compliant code autonomously. Generates compliance evidence artefacts. 3. MRM Agent (⚙): continuous model monitoring. Drift > threshold → auto-disable feature flag + alert Product Builder. Kill-switch tested quarterly. 4. Governance Controller (⚙): wraps all agent transitions. Validates every handoff meets governance protocol. Immutable audit trail. 5. All four agents integrated into STUMP StateGraph — no deployment reaches production without passing all four.',
        example: '# Governance agent cascade at every deployment gate:\n# StateGraph transition: review_agent → release_gate\ngovernance_controller.validate({\n    "transition": "review → release",\n    "checks": [\n        secure_by_design.check(iac_diff),       # ⚙ IaC scan\n        compliance_orchestrator.check(commit),   # ⚙ GDPR/DORA/Basel III\n        mrm_agent.check(model_artifacts),        # ⚙ Drift + explainability\n    ]\n})\n# If all pass: transition approved autonomously + logged\n# If any fail: deployment blocked + Product Builder alerted\n#              Reason + recommended fix posted to #governance-alerts',
        tools: ['OPA', 'LangGraph', 'SHAP', 'Evidently AI', 'Azure Immutable Blob', 'LaunchDarkly'],
        owner: 'STUMP Platform (autonomous) — CCO + CISO own rule library', timeline: 'Week 8–14', effort: '4–6 weeks',
        successCriteria: 'All 4 governance agents integrated into StateGraph. Zero compliance violations reaching production. MRM kill-switch tested and documented. Immutable audit trail complete for every deployment. CCO + CISO formal sign-off.' },
      { title: 'Real-time intelligence: customer intent detection + proactive feature generation', icon: '🧠', category: 'Intelligence', phase: 'Continuous (post go-live)',
        current: 'Feature ideas come from PO intuition, stakeholder requests, and quarterly roadmap reviews. No real-time connection between production usage signals and product roadmap.',
        change: 'STUMP continuously monitors customer behaviour, support tickets, usage analytics, and market signals. NLP analysis detects unmet needs → generates feature hypotheses → Product Definer reviews weekly. Roadmap driven by live signals, not intuition.',
        how: '1. Customer signal ingestion: connect support ticket system, usage analytics (Heap/Mixpanel), app ratings, and social media mentions to STUMP Telemetry Sentinel. 2. NLP classifier: LLM analyses signal stream for pain points, feature requests, confusion patterns. Groups into themes (e.g., "users struggling with recurring payment rules"). 3. Feature hypothesis generator: for each theme exceeding signal threshold → generate feature hypothesis brief (problem statement, evidence, estimated user impact, compliance flag if regulated). 4. Product Definer weekly review: 15-min session to review top 5 AI-generated hypotheses. Promote top 2 to outcome brief queue. 5. Feedback loop: track which hypotheses became features, their adoption rate, and back-fill AI training data.',
        example: '# Customer intent detection weekly summary (Slack digest):\n📊 STUMP Intelligence Report — Week 15\n\n🔴 High-signal themes (>50 mentions this week):\n  1. "Recurring payment rules" — 73 support tickets + 0.8★ store reviews\n     Hypothesis: Allow multi-rule scheduling with conflict detection\n     Estimated impact: Affects 12% of business customers. OFAC compliance needed.\n     → PROMOTE TO BRIEF? [Yes ↑] [Defer →] [Dismiss ✕]\n\n  2. "Payment status visibility" — 61 app crash reports + 44 tickets\n     Hypothesis: Real-time payment status push notification\n     Estimated impact: Reduces support ticket volume 15%. No regulatory flag.\n     → PROMOTE TO BRIEF? [Yes ↑] [Defer →] [Dismiss ✕]',
        tools: ['LangChain + Azure OpenAI', 'Heap / Mixpanel', 'Datadog RUM', 'Zendesk / ServiceNow API', 'Slack Blocks API'],
        owner: 'STUMP Platform (autonomous) — Product Definer reviews weekly', timeline: 'Week 20+ (post full transition)', effort: '2–3 weeks (post-platform)',
        successCriteria: '% of outcome briefs originating from STUMP intelligence signals: target ≥ 40% by Month 6. Signal-to-brief cycle: < 7 days. Product Definer reports higher confidence in roadmap decisions. NPS uplift from proactively addressed pain points: target +5 points.' },
    ],
    devSecOps: [
      { title: 'Autonomous Secure-by-Design Architect: zero human in security loop', icon: '🏗️', pipelineStage: 'Code → PR → IaC → CD', priority: 'P1 — Week 8',
        current: 'Security reviews are human-led, periodic, and reactive. Misconfigurations discovered in production. CISO approval required for every IaC change.',
        change: 'Secure-by-Design Architect agent (⚙ autonomous) validates ALL IaC and security configurations on every commit. Blocks non-compliant code without human intervention. CISO owns the rule library — not individual deployments. Exceptions require explicit waiver in code.',
        how: '1. Load CISO-approved policy library into OPA: encryption requirements, network segmentation rules, access policy templates, secret management standards. 2. Secure-by-Design Architect (⚙) runs on every PR and every Terraform plan: compares change against policy library. 3. Non-compliant → blocked autonomously. Agent posts remediation suggestion with exact IaC fix. No human review required for standard violations. 4. Exception workflow: developer adds `# governance-waiver: [reason]` comment + creates exemption ticket. CISO reviews weekly batch. 5. All decisions logged to immutable audit trail (compliance evidence).',
        example: '# Secure-by-Design Architect — autonomous violation + auto-fix:\n# Detected: S3 bucket without server-side encryption (CKV_AWS_19)\n# Agent response (posted to PR):\n"""\n⚙ SECURE-BY-DESIGN ARCHITECT [BLOCKED]\nViolation: CKV_AWS_19 — S3 bucket missing server-side encryption\nPolicy: All storage resources require AES-256 encryption at rest\n\nAuto-fix: Replace your aws_s3_bucket resource with:\n  resource "aws_s3_bucket_server_side_encryption_configuration" "example" {\n    bucket = aws_s3_bucket.example.id\n    rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }\n  }\n\nIf intentional waiver required:\n  Add: # governance-waiver: reason=legacy-migration approved-by=CISO\n  Create exemption ticket: SEC-BACKLOG\n"""',
        tools: ['OPA', 'Checkov', 'LangChain + Azure OpenAI', 'GitHub Actions', 'Azure Immutable Blob'],
        metrics: 'Security violations in production: target 0. CISO time on individual PR reviews: 100% → 0% (owns rule library, not PRs). Security debt accumulation: eliminated (every deployment secure by default).' },
      { title: 'Full Compliance-as-Code: zero manual audit function', icon: '⚖️', pipelineStage: 'Commit → PR → Release', priority: 'P1 — Week 10',
        current: 'Manual compliance reviews before each release (2–5 person-weeks per audit). Evidence collected manually. Compliance team involved in every release. Violations discovered post-release.',
        change: 'Compliance-as-Code Orchestrator (⚙ autonomous) validates GDPR, DORA, and Basel III rules on every commit. Compliance evidence captured automatically at every deployment. Manual audit function eliminated — replaced by continuous assurance. External auditors access automated evidence store directly.',
        how: '1. Encode complete ruleset: GDPR (PII handling, consent, data retention), DORA (change failure rate < 5%, recovery time SLA), Basel III (model explainability, risk capital calculation transparency). 2. OPA policy library: 120+ rules covering all applicable regulations. CISO + CCO review quarterly. 3. Compliance evidence capture: every deployment archives to Azure Immutable Blob: test results, SAST output, GDPR scan, model explainability reports, approval records. 4. Automated compliance report: generated on every release — maps artefacts to regulatory requirements. External auditor access: read-only S3/Blob portal. 5. Compliance team shifts from evidence collection to rule library governance.',
        example: '# Compliance-as-Code orchestrator report (auto-generated per release):\n{\n  "release_id": "payments-v2.14.0",\n  "deployed_at": "2024-04-18T14:32Z",\n  "compliance_status": "COMPLIANT",\n  "gdpr": {\n    "pii_in_logs": false, "consent_check_present": true,\n    "retention_policy_enforced": true, "status": "PASS"\n  },\n  "dora": {\n    "change_failure_rate_30d": 1.8, "threshold": 5.0,\n    "recovery_time_p75_hrs": 0.4, "status": "PASS"\n  },\n  "basel_iii": {\n    "explainability_report": "s3://compliance/fraud-model-v2-shap.pdf",\n    "risk_capital_transparency": "documented", "status": "PASS"\n  },\n  "evidence_location": "s3://compliance-evidence/payments-v2.14.0/"\n}',
        tools: ['OPA', 'LangChain + Azure OpenAI', 'Drata', 'Azure Immutable Blob / S3 Object Lock', 'GitHub Actions'],
        metrics: 'Manual audit prep: 2–5 person-weeks → 0 (automated). Compliance violations reaching production: target 0. External audit duration: weeks → days (auditor reads automated evidence). Evidence completeness: 100%.' },
      { title: 'MRM Agent: autonomous model governance with kill-switch (SR 11-7)', icon: '🎛️', pipelineStage: 'Continuous monitoring + every model deployment', priority: 'P1 — Week 12',
        current: 'No systematic model risk governance. SR 11-7 compliance not verified. Model drift undetected until user complaints. No automated kill-switch.',
        change: 'MRM Agent (⚙ autonomous) continuously monitors all production models: drift detection, explainability scoring, bias monitoring. Kill-switch auto-disables any model breaching risk parameters — no human action required. Product Builder alerted. Full SR 11-7 compliance documented.',
        how: '1. Model registry: enumerate all AI/ML models in production. MRM Agent registers each with risk parameters (approved by MRO). 2. Continuous monitoring (⚙): MRM Agent runs hourly drift checks (PSI, KL divergence), weekly explainability reports (SHAP values), daily bias scoring (protected attribute analysis). 3. Kill-switch configuration: if ANY risk parameter breached → LaunchDarkly feature flag auto-disabled → MRM Agent posts incident to #model-risk + pings Product Builder. Target response: kill-switch in < 30 seconds from breach detection. 4. Model deployment gate: no new model goes to production without passing MRM Agent pre-deployment review (baseline explainability, bias audit, risk parameter sign-off by MRO). 5. All reports in S3 with 7-year retention for SR 11-7.',
        example: '# MRM Agent kill-switch trigger (autonomous):\n# Detected: fraud_detection_v3 PSI drift = 0.34 (threshold: 0.20)\nmrm_agent.handle_breach({\n  "model_id": "fraud_detection_v3",\n  "breach_type": "drift",\n  "psi_score": 0.34,\n  "threshold": 0.20\n})\n# Actions (all autonomous, < 30 seconds):\n# 1. feature_flags.disable("fraud_detection_v3")  ← kill-switch\n# 2. slack.alert("#model-risk", "⚠ KILL-SWITCH ACTIVATED: fraud_detection_v3")\n# 3. pagerduty.create_incident(severity="P2", team="model-risk")\n# 4. create_explainability_report(model_id, reason="drift_breach")\n# 5. s3.archive(report, "s3://compliance/mrm-incidents/")',
        tools: ['SHAP', 'Evidently AI', 'LaunchDarkly', 'LangChain + Azure OpenAI', 'Azure ML', 'PagerDuty'],
        metrics: 'SR 11-7 compliance: fully documented. Kill-switch activation: < 30 seconds from breach detection. Model drift incidents in production: detected before user impact. Explainability report coverage: 100% of production models.' },
      { title: 'Autonomous incident response: AI Incident Commander (Sev-2 and below)', icon: '🚨', pipelineStage: 'Production (continuous)', priority: 'P1 — Week 14',
        current: 'All incidents routed to human on-call. L1/L2 engineers spend 60–70% of on-call time on automatable toil. PIRs written manually or skipped. MTTD: 15–45 min.',
        change: 'STUMP AI Incident Commander (⚙ autonomous) handles all Sev-2 and below: classifies, routes, auto-remediates with pre-approved playbooks, updates status page, and generates PIR. Sev-1 only escalates to Product Builder. (Human: Provide Intent for new runbooks → Review PIR → Approve Only for Sev-1.)',
        how: '1. AI Incident Commander ingests all alerts from Dynatrace/Datadog via webhook. 2. NLP classifier: categorises incident by type, severity, and affected service. Confidence > 85% → autonomous action; < 85% → escalate to Product Builder. 3. Auto-remediation playbooks: pre-approved by Product Builder for top 20 failure patterns (pod restart, cache flush, connection pool reset, circuit breaker trip). 4. Status page: AI updates status page for all Sev-2+ incidents within 2 min. 5. PIR generator: 2 hrs after resolution → draft PIR auto-generated from incident timeline, actions taken, root cause. Product Builder reviews and publishes (no writing required).',
        example: '# AI Incident Commander autonomous resolution:\n# Alert: payments-api error rate 8.3% (threshold: 5%)\n{\n  "incident_id": "INC-2024-0412",\n  "classification": "Sev-2 — payments-api latency spike",\n  "root_cause": "DB connection pool exhausted (matches pattern INC-2024-0089)",\n  "autonomous_action": {\n    "playbook": "db_connection_pool_reset",\n    "steps": [\n      "Increased connection pool max from 100 to 150",\n      "Restarted payments-api pods (rolling restart, zero downtime)",\n      "Verified error rate returned to < 0.1% within 4 min"\n    ]\n  },\n  "status_page_update": "Investigating elevated error rates in Payments. ETA: resolved.",\n  "escalated_to_human": false,\n  "resolution_time_min": 6\n}',
        tools: ['Dynatrace Davis AI', 'PagerDuty', 'LangChain + Azure OpenAI', 'Statuspage.io', 'Kubernetes API'],
        metrics: 'L1/L2 incidents requiring human: 100% → Sev-1 only (< 5% of incidents). MTTD: 15–45 min → < 2 min. MTTR: 2–4 hrs → < 15 min (Sev-2). PIR completion rate: 40% → 100%.' },
    ],
    aiOps: [
      { title: 'Fully autonomous AIOps: zero L1/L2 human intervention', icon: '🤖', layer: 'Full Stack Autonomous', priority: 'P1 — Week 14',
        current: 'L1 and L2 engineers handle all production alerts, incidents, and remediations manually. 70–80% of on-call time is toil. Engineers fatigued. MTTD: 15–45 min.',
        change: 'STUMP AIOps (⚙) manages ALL production operations end-to-end: anomaly detection, incident classification, auto-remediation, capacity management, cost optimisation. Sev-1 only escalates to Product Builder. Zero L1/L2 human intervention required. (Human: Provide intent for new runbooks → Review PIR → Approve escalations.)',
        how: '1. Deploy Dynatrace Davis AI + STUMP AI Incident Commander as unified AIOps stack. 2. Auto-instrument all services with OpenTelemetry. Baseline AI learning period: 2 weeks (do not change alert rules). 3. Encode top 30 failure patterns as auto-remediation playbooks (approved by Product Builder). 4. Configure escalation rule: only Sev-1 (major outage, data breach, compliance breach) escalates to human. Everything else: autonomous. 5. Monthly AIOps review: Product Builder reviews all auto-remediations, validates playbooks, retires obsolete patterns.',
        example: '# AIOps autonomous operations summary (weekly):\n📊 STUMP AIOps Week 15 Operations Report\n\nIncidents handled: 47 total\n  ✅ 44 auto-resolved (Sev-2/3/4) — avg resolution: 8 min\n  ⚠️  2 escalated to Product Builder (Sev-1) — resolved in 23 min, 41 min\n  ✅  1 false positive suppressed (known flaky health check)\n\nTop auto-remediated patterns:\n  1. DB connection pool exhaustion (18×) — pool auto-expanded\n  2. Pod OOM (11×) — memory limit auto-increased within guardrails\n  3. CDN cache miss spike (8×) — cache warm-up job triggered\n\nCost savings this week: $2,340 (right-sizing + spot instance optimisation)\nAI prediction accuracy: 94.2% (alert relevance)',
        tools: ['Dynatrace Davis AI', 'STUMP AI Incident Commander', 'OpenTelemetry', 'PagerDuty', 'Kubernetes API'],
        metrics: 'L1/L2 human incidents: 100% → Sev-1 only. MTTD: 15–45 min → < 2 min. MTTR (Sev-2): 2–4 hrs → < 15 min. On-call false alarm pages: reduced by 95%.' },
      { title: 'Self-healing, self-scaling, self-documenting infrastructure', icon: '♻️', layer: 'Infrastructure Autonomy', priority: 'P1 — Week 12',
        current: 'Infrastructure scaling is reactive. Runbooks maintained manually (often out of date). Infrastructure documentation written by humans (rarely updated). Scaling lag: minutes after spike hits.',
        change: 'STUMP Platform manages infrastructure autonomously: predictive scaling (30–60 min ahead), self-healing on failure (pod restarts, circuit breaker trips, cache flushes), and auto-generates runbooks from incident patterns. Infrastructure documentation is always current because agents write it. (⚙ fully autonomous within approved guardrails.)',
        how: '1. Predictive scaling: train ML model on 12 months traffic history + US Bank calendar signals (payroll run dates, month-end batch, holiday patterns). AWS Predictive Scaling or KEDA + custom forecaster. 2. Self-healing: Kubernetes Operator watches for pre-defined failure patterns. Auto-applies remediation from approved playbook library. 3. Auto-generated runbooks: after every novel incident, STUMP generates a runbook draft from resolution steps. Product Builder reviews and promotes to playbook library. 4. Infrastructure as code: every infrastructure change generated by Copilot + validated by Secure-by-Design Architect → applied by pipeline. No manual Terraform edits.',
        example: '# Predictive scaling — US Bank payroll day (1st of month):\n# STUMP detects: date = 2024-05-01 (payroll processing day)\n# Historical pattern: 3.4× normal traffic spike at 09:00 CT\npredictive_scaler.apply({\n  "trigger": "calendar_event",\n  "event": "payroll_processing",\n  "predicted_load_multiplier": 3.4,\n  "scale_at": "2024-05-01T08:30:00-05:00",  # 30 min before spike\n  "scale_down_at": "2024-05-01T14:00:00-05:00",\n  "target_service": "payments-processor",\n  "target_replicas": 24,  # from 7 (baseline)\n  "notify": ["#platform-ops"]\n})',
        tools: ['KEDA', 'AWS Predictive Scaling', 'Kubernetes Operator', 'LangChain + Azure OpenAI', 'Terraform', 'GitHub Actions'],
        metrics: 'Scaling lag: reactive → proactive (30–60 min ahead). Runbook coverage: 60% → 100% (auto-generated). Infrastructure incidents from misconfiguration: target 0. Compute cost: reduced 25–35% via predictive right-sizing.' },
      { title: 'Continuous product intelligence: telemetry → outcome brief pipeline', icon: '🔄', layer: 'Feedback Loop', priority: 'P2 — Week 20',
        current: 'Production signals (errors, slow journeys, user friction) reach roadmap via manual analysis — weeks or months later. Engineering prioritises tech debt without live user impact data.',
        change: 'STUMP Intelligence Agent (⚙) continuously monitors production telemetry, support signals, and usage analytics. Detects unmet customer needs and generates feature hypotheses. Product Definer receives weekly intelligence digest — roadmap inputs are live signals, not guesswork.',
        how: '1. Connect all signal sources: Dynatrace (errors, latency), Heap/Mixpanel (usage journeys), Zendesk/ServiceNow (support tickets), app store ratings. 2. NLP signal clustering: LLM groups related signals into themes. Business Risk Score weighted composite: severity × frequency × customer impact × regulatory flag. 3. Feature hypothesis generation: for each theme above threshold → generate outcome brief draft. 4. Weekly Product Definer digest (Slack): top 5 hypotheses with evidence, estimated user impact, compliance flag. Definer promotes top 2 to brief queue. 5. Hypothesis tracking: % of AI-generated hypotheses that became shipped features. Training feedback loop for NLP model.',
        example: '# STUMP Intelligence weekly digest (Slack Block Kit):\n🧠 STUMP Intelligence — Week 15 Top Signals\n\n1. [HIGH IMPACT] "Payment confirmation delays"\n   Signals: 89 support tickets + 2.1★ store reviews + p95 latency: 4.2s\n   Hypothesis: Async payment confirmation with push notification\n   Impact estimate: ~8,000 affected users/week | No regulatory flag\n   [Promote to brief ↑] [Defer →]\n\n2. [COMPLIANCE FLAG] "Recurring payment edit conflicts"\n   Signals: 34 tickets + OFAC check failure in 3% of edits\n   Hypothesis: Conflict detection + re-validation on rule edit\n   Impact estimate: ~1,200 business customers | OFAC compliance required\n   [Promote to brief ↑] [Defer →]',
        tools: ['LangChain + Azure OpenAI', 'Heap / Mixpanel', 'Zendesk API', 'Datadog RUM', 'Slack Blocks API'],
        metrics: '% outcome briefs from live signals: 0% → ≥ 40% by Month 6. Signal-to-brief cycle: weeks → 7 days. Proactive issue resolution (before user complaint): target 30% of issues. NPS uplift from proactive fixes: +5 points.' },
      { title: 'AI incident commander: Sev-1 escalation with full context handoff', icon: '🎖️', layer: 'Incident Response', priority: 'P1 — Week 14',
        current: 'On-call engineer paged for all incidents. Spends 15–30 min gathering context before even starting diagnosis. PIRs often skipped due to time pressure.',
        change: 'AI Incident Commander (⚙) handles Sev-2 and below autonomously. For Sev-1: Product Builder is paged with a complete pre-diagnosis pack — root cause hypothesis, affected services, blast radius, initial remediation steps attempted. Engineer starts at diagnosis, not context-gathering. PIRs auto-generated within 2 hrs of resolution.',
        how: '1. Sev-1 detection: AI Incident Commander classifies incident. Sev-1 criteria: major payment processing outage, data breach indicators, compliance breach detected, blast radius > 10% of users. 2. Pre-diagnosis pack generation (automated, < 2 min after detection): root cause hypothesis from pattern matching, affected service dependency map, recent changes in last 24 hrs, similar past incidents (top 3 with resolution times), initial remediation steps already attempted by AI. 3. PagerDuty alert to Product Builder: includes pre-diagnosis pack as structured JSON + Slack message. 4. AI assists Product Builder during incident: answers queries ("what changed in the last hour?", "what is the blast radius?") using telemetry data. 5. PIR generator: triggered 2 hrs after resolution. Draft ready in 45 min. Product Builder reviews and publishes.',
        example: '# Sev-1 handoff pack (sent to Product Builder via PagerDuty + Slack):\n🔴 SEV-1 ESCALATED — Payments API down\nAlert time: 14:32 UTC | Escalated to human: 14:32 UTC\n\n📊 Pre-diagnosis:\n  Root cause hypothesis: Database failover incomplete — primary RDS unreachable\n  Affected services: payments-api, fraud-detection, account-balance\n  Blast radius: 100% of payment transactions failing (est. 15,000 users affected)\n  Recent changes (last 24hrs): DB maintenance window ran 12:00–13:30 UTC\n\n⚡ AI actions already attempted:\n  ✅ Triggered pod restart (no effect — DB connection issue)\n  ✅ Enabled circuit breaker (degraded mode active — balance reads OK)\n  ❌ Attempted DB connection pool flush (failed — DB unreachable)\n\n🔗 Runbooks: [DB Failover] [RDS Recovery] [Circuit Breaker Management]\n💬 Ask AI: "What changed in RDS in last 6 hours?" → [AI Assist Active]',
        tools: ['Dynatrace Davis AI', 'PagerDuty', 'LangChain + Azure OpenAI', 'AWS RDS / Azure SQL', 'Slack Blocks API'],
        metrics: 'Time from Sev-1 page to diagnosis start: 30 min → < 3 min (pre-diagnosis pack). MTTR Sev-1: reduced 40–60%. PIR completion rate: 40% → 100% (auto-generated). Product Builder on-call time for Sev-2 and below: eliminated.' },
    ],
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
      { name: 'Core Tools', range: 'Week 3–6', color: 'emerald', milestones: ['Deploy AI performance test analyzer (target: 75% authoring time reduction)','Integrate AI APM platform (Dynatrace Davis AI or Datadog AI)','Configure AI-driven incident routing and auto-remediation rules','AI-generated IaC templates with security policy validation live'] },
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
      { name: 'Integration', range: 'Week 6–10', color: 'emerald', milestones: ['Deploy agents in production alongside existing processes (2-week parallel run)','Define and document human-AI handoff protocols per PDLC phase','Begin role transition: team operates with 5 core roles from Sprint 7','AI Agent Ops: daily monitoring dashboard live for agent performance'] },
      { name: 'Compliance Agent Setup', range: 'Week 10–13', color: 'sky', milestones: ['Configure Secure-by-Design Architect: load cloud architecture standards and IaC rejection rules','Deploy Compliance-as-Code Orchestrator: encode GDPR, DORA, Basel III rules against staging commits','Baseline MRM Agent: define model explainability thresholds and kill-switch parameters with MRO sign-off','Activate Telemetry Sentinel: configure Business Risk Score thresholds; connect to governance dashboard','Wire Multi-Agent Governance Controller: test agent hand-off protocols and bypass detection'] },
      { name: 'Full Deployment', range: 'Week 13–16', color: 'purple', milestones: ['Remove parallel processes — agents are primary for all target activities','AIOps platform live — managing all production alerts and triage','ALM consolidation complete — one platform for all work tracking','Self-healing CI/CD pipeline operational with AI failure prediction'] },
      { name: 'Optimise & Report', range: 'Week 16–18', color: 'teal', milestones: ['Full VSM re-measurement vs baseline (target: -55% PT, -72% WT)','Tune agent prompts based on 6 weeks of real production output quality','Calculate ROI vs 3.8× target — include compliance automation savings','Publish team case study; assess Option C feasibility'] }
    ]
  },
  'option-c': {
    teamDuration: '20–26 weeks',
    enterpriseDuration: '18–24 months',
    teamNote: 'A 22-agent orchestration system is architecturally complex even for one team. Pilot phase is mandatory before the 2-role transition. Industry ref: Cognition AI built Devin-class agent systems in ~4 months.',
    phases: [
      { name: 'Design & Approval', range: 'Week 1–4', color: 'blue', milestones: ['Technical architecture for all 13 agents and orchestration layer (including 5 governance agents)','Operating model design: 2-role structure (Definer + Builder)','Team communication plan and workforce transition agreement','Technology stack selection: LangGraph / AutoGen / Agency Swarm','Governance architecture: MRM Agent risk parameters and Governance Controller protocol definitions signed off by CTO + CCO'] },
      { name: 'Platform Build', range: 'Week 4–12', color: 'green', milestones: ['Month 2: Core agents live — coding, testing, review','Month 2–3: Orchestration layer + Governance Controller + AI-native ALM replacement built','Month 3: AIOps agents + Telemetry Sentinel + fully autonomous CI/CD pipeline deployed','Secure-by-Design Architect and Compliance-as-Code Orchestrator integrated into every deployment gate','MRM Agent connected to all model versioning pipelines; kill-switch tested in staging'] },
      { name: 'Compliance Baseline', range: 'Week 10–14', color: 'sky', milestones: ['MRM Agent: generate baseline Explainability Reports for all models entering production','Compliance-as-Code: full GDPR, DORA, Basel III ruleset validated against 3 months of commit history','Secure-by-Design: IaC baseline approved by CISO; all new IaC auto-validated','Telemetry Sentinel: Business Risk Score thresholds calibrated with governance board','Governance Controller: bypass detection tested — confirm no dev agent can execute without approval'] },
      { name: 'Pilot', range: 'Week 14–20', color: 'emerald', milestones: ['2-person team (Definer + Builder) takes ownership — parallel with existing team','Human manual review of all agent outputs for first 3 weeks','Identify and fix agent failure modes; tune orchestration prompts','All 5 governance agents formally validated (SOC2, GDPR, Basel III, MRM risk parameters)'] },
      { name: 'Full Transition', range: 'Week 20–26', color: 'purple', milestones: ['Remove manual oversight from all validated agent workflows','Complete transition to 2-role operating model (team restructured)','All production support autonomous — zero L1/L2 human intervention','Real-time customer intent detection and proactive feature gen live'] },
      { name: 'Stabilise & Scale', range: 'Week 26–28', color: 'teal', milestones: ['VSM re-measurement vs baseline (target: -70% PT, -88% WT)','Calculate ROI vs 5.5× target including compliance automation savings; present board-level results','Document full playbook and agent configs (including governance agents) for other teams to replicate','Publish internal case study; plan scale-out to next product team'] }
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
  amber:  { bg: 'bg-emerald-100',  border: 'border-emerald-300',  badge: 'bg-emerald-500',  text: 'text-emerald-800' },
  purple: { bg: 'bg-purple-100', border: 'border-purple-300', badge: 'bg-purple-600', text: 'text-purple-800' },
  teal:   { bg: 'bg-teal-100',   border: 'border-teal-300',   badge: 'bg-teal-600',   text: 'text-teal-800' },
  red:    { bg: 'bg-sky-100',    border: 'border-sky-300',    badge: 'bg-sky-600',    text: 'text-sky-800' },
  indigo: { bg: 'bg-indigo-100', border: 'border-indigo-300', badge: 'bg-indigo-600', text: 'text-indigo-800' },
  orange: { bg: 'bg-teal-100', border: 'border-teal-300', badge: 'bg-teal-600', text: 'text-teal-800' },
}

const SECTIONS = [
  { id: 'overview',  label: 'Overview' },
  { id: 'opmodel',   label: '🏗 Operating Model' },
  { id: 'costmodel', label: '💰 Cost Model & ROI' },
  { id: 'playbook',  label: 'Playbook' },
  { id: 'timeline',  label: 'Timeline' },
  { id: 'roadmap',   label: '🗺 Roadmap' },
  { id: 'tracker',   label: '✅ Action Tracker' },
  { id: 'teamplans', label: '👥 Team Plans' },
  { id: 'investment',label: 'Investment' },
  { id: 'benefits',  label: 'Benefits' },
  { id: 'org',       label: 'Org Change' },
  { id: 'tools',     label: 'Tools' },
  { id: 'devsecops', label: '🔒 DevSecOps' },
  { id: 'aiops',     label: '🤖 AI Ops' },
  { id: 'product',   label: 'Product-Centric' },
  { id: 'roles',     label: '👥 Roles & Skills' },
  { id: 'costestimator', label: '💵 Cost Estimator' },
]

const OPTION_META = {
  'option-a': { label: 'Option A', badge: 'bg-blue-600',   ring: 'ring-blue-400',   light: 'bg-blue-50',   border: 'border-blue-200',   text: 'text-blue-800',   duration: '6–10 wks',  roi: '2.8×' },
  'option-b': { label: 'Option B', badge: 'bg-purple-600', ring: 'ring-purple-400', light: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-800', duration: '12–16 wks', roi: '3.8×' },
  'option-c': { label: 'Option C', badge: 'bg-emerald-600',ring: 'ring-emerald-400',light: 'bg-emerald-50',border: 'border-emerald-200',text: 'text-emerald-800',duration: '20–26 wks', roi: '5.5×' },
}

// ─── Component ────────────────────────────────────────────────────────────────
// ─── Reusable: Editable Action List ──────────────────────────────────────────
// Rich expandable action cards with description, how-to, tools, success criteria.
// Supports both string items (roadmap) and object items (playbook sprints).
function EditableActionList({ items, onChange, tone = 'indigo' }) {
  const [expandIdx, setExpandIdx] = useState(null)
  const [editIdx, setEditIdx] = useState(null)
  const [editForm, setEditForm] = useState({})
  const [adding, setAdding] = useState(false)
  const [addForm, setAddForm] = useState({ who: '', what: '', description: '', how: '', tools: '', success: '' })

  const isObj = (x) => x && typeof x === 'object'
  const startEdit = (i) => {
    const item = items[i]
    setEditIdx(i)
    setEditForm(isObj(item) ? { who: item.who || '', what: item.what || '', description: item.description || '', how: item.how || '', tools: item.tools || '', success: item.success || '' }
      : { who: '', what: item || '', description: '', how: '', tools: '', success: '' })
  }
  const saveEdit = () => {
    if (editIdx === null) return
    const next = [...items]
    if (isObj(next[editIdx])) next[editIdx] = { ...next[editIdx], ...editForm }
    else next[editIdx] = editForm.what || editForm.description || ''
    onChange(next); setEditIdx(null); setExpandIdx(editIdx)
  }
  const remove = (i) => { onChange(items.filter((_, j) => j !== i)); if (expandIdx === i) setExpandIdx(null) }
  const addItem = () => {
    if (!addForm.what.trim()) return
    const entry = isObj(items[0]) ? { ...addForm } : addForm.what.trim()
    onChange([...items, entry])
    setAddForm({ who: '', what: '', description: '', how: '', tools: '', success: '' }); setAdding(false)
  }

  const inputCls = "w-full text-sm border border-gray-300 rounded-lg px-2.5 py-1.5 focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400"
  const labelCls = "text-xs font-semibold text-gray-500 mb-0.5 block"

  const renderEditForm = (form, setForm, onSave, onCancel) => (
    <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-4 space-y-2.5 ml-7">
      <div className="grid grid-cols-2 gap-2">
        <div><label className={labelCls}>Owner / Role</label><input value={form.who} onChange={e => setForm({...form, who: e.target.value})} className={inputCls} placeholder="e.g. Platform Lead, Tech Lead" /></div>
        <div><label className={labelCls}>Action Title</label><input value={form.what} onChange={e => setForm({...form, what: e.target.value})} className={inputCls} placeholder="Short action title" /></div>
      </div>
      <div><label className={labelCls}>Description — What & Why</label><textarea value={form.description} onChange={e => setForm({...form, description: e.target.value})} className={inputCls} rows={2} placeholder="What this action involves and why it matters" /></div>
      <div><label className={labelCls}>How to Execute — Step-by-step</label><textarea value={form.how} onChange={e => setForm({...form, how: e.target.value})} className={inputCls} rows={3} placeholder="1. First step&#10;2. Second step&#10;3. ..." /></div>
      <div className="grid grid-cols-2 gap-2">
        <div><label className={labelCls}>Tools / Resources</label><input value={form.tools} onChange={e => setForm({...form, tools: e.target.value})} className={inputCls} placeholder="e.g. LangGraph, Azure OpenAI, Jira" /></div>
        <div><label className={labelCls}>Success Criteria</label><input value={form.success} onChange={e => setForm({...form, success: e.target.value})} className={inputCls} placeholder="How to know this is done" /></div>
      </div>
      <div className="flex gap-2 pt-1">
        <button onClick={onSave} className="text-xs bg-emerald-600 text-white px-4 py-1.5 rounded-lg hover:bg-emerald-700 font-semibold">Save</button>
        <button onClick={onCancel} className="text-xs bg-gray-200 text-gray-600 px-4 py-1.5 rounded-lg hover:bg-gray-300">Cancel</button>
      </div>
    </div>
  )

  return (
    <div className="space-y-2">
      {items.map((item, i) => {
        const text = item?.what ?? item
        const who = item?.who
        const desc = item?.description
        const how = item?.how
        const tools = item?.tools
        const success = item?.success
        const hasDetail = desc || how || tools || success
        const isExpanded = expandIdx === i
        const isEditing = editIdx === i

        if (isEditing) return <div key={i}>{renderEditForm(editForm, setEditForm, saveEdit, () => setEditIdx(null))}</div>

        return (
          <div key={i} className={`group rounded-xl border transition-all ${isExpanded ? 'border-indigo-300 bg-white shadow-sm' : 'border-gray-200 bg-white hover:border-gray-300'}`}>
            <div className="flex items-start gap-3 px-3 py-2.5 cursor-pointer" onClick={() => setExpandIdx(isExpanded ? null : i)}>
              <span className={`bg-${tone}-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5`}>{i + 1}</span>
              <div className="flex-1 min-w-0">
                <div className="flex items-start gap-2">
                  <div className="flex-1">
                    {who && <span className="font-semibold text-indigo-900 text-xs mr-1.5 bg-indigo-50 px-1.5 py-0.5 rounded">{who}</span>}
                    <span className="text-sm font-medium text-gray-800">{text}</span>
                  </div>
                  <div className="flex gap-1 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" onClick={e => e.stopPropagation()}>
                    <button onClick={() => startEdit(i)} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded hover:bg-blue-100 hover:text-blue-700" title="Edit">✏️</button>
                    <button onClick={() => remove(i)} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded hover:bg-red-100 hover:text-red-700" title="Remove">✕</button>
                  </div>
                </div>
                {!isExpanded && desc && <div className="text-xs text-gray-500 mt-0.5 truncate">{desc}</div>}
              </div>
              <span className="text-gray-400 text-xs shrink-0 mt-1">{isExpanded ? '▲' : '▼'}</span>
            </div>
            {isExpanded && (
              <div className="border-t border-gray-100 px-4 pb-3 pt-2 space-y-2 text-sm">
                {desc && <div><span className="text-xs font-semibold text-gray-500">Description:</span><div className="text-gray-700 mt-0.5">{desc}</div></div>}
                {how && <div><span className="text-xs font-semibold text-gray-500">How to Execute:</span><div className="text-gray-700 mt-0.5 whitespace-pre-line font-mono text-xs bg-gray-50 rounded-lg p-2.5 border border-gray-200">{how}</div></div>}
                {tools && <div className="flex items-start gap-2"><span className="text-xs font-semibold text-gray-500 shrink-0">Tools:</span><div className="flex flex-wrap gap-1">{tools.split(',').map((t,ti) => <span key={ti} className="bg-indigo-50 text-indigo-700 text-xs px-2 py-0.5 rounded-full border border-indigo-200">{t.trim()}</span>)}</div></div>}
                {success && <div><span className="text-xs font-semibold text-gray-500">Success Criteria:</span><div className="text-emerald-700 mt-0.5 text-xs bg-emerald-50 rounded-lg px-2.5 py-1.5 border border-emerald-200">{success}</div></div>}
                {!hasDetail && <div className="text-xs text-gray-400 italic">No details yet — click ✏️ to add description, how-to steps, tools, and success criteria.</div>}
              </div>
            )}
          </div>
        )
      })}
      {adding ? renderEditForm(addForm, setAddForm, addItem, () => { setAdding(false); setAddForm({ who: '', what: '', description: '', how: '', tools: '', success: '' }) })
      : (
        <button onClick={() => setAdding(true)}
          className="ml-7 text-xs text-indigo-600 hover:text-indigo-800 font-semibold flex items-center gap-1 py-1">
          <span className="text-base leading-none">+</span> Add action
        </button>
      )}
    </div>
  )
}

// ─── Reusable: Editable RACI Table ──────────────────────────────────────────
function EditableRaciTable({ raci, onChange }) {
  const [editIdx, setEditIdx] = useState(null)
  const [editRow, setEditRow] = useState({})
  const [adding, setAdding] = useState(false)
  const [addRow, setAddRow] = useState({ activity: '', r: '', a: '', c: '', i: '' })

  const startEdit = (i) => { setEditIdx(i); setEditRow({ ...raci[i] }) }
  const saveEdit = () => { const next = [...raci]; next[editIdx] = editRow; onChange(next); setEditIdx(null) }
  const remove = (i) => onChange(raci.filter((_, j) => j !== i))
  const addItem = () => { if (!addRow.activity.trim()) return; onChange([...raci, addRow]); setAddRow({ activity: '', r: '', a: '', c: '', i: '' }); setAdding(false) }

  const cellClass = "py-2 px-2 text-center text-xs"
  const inputClass = "w-full text-xs border border-gray-300 rounded px-1.5 py-1 focus:ring-1 focus:ring-indigo-300"

  return (
    <div id="pb-raci" className="card">
      <div className="card-header flex items-center justify-between">
        <h3 className="font-bold text-gray-800">Roles & Responsibilities (RACI)</h3>
        {!adding && <button onClick={() => setAdding(true)} className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold">+ Add row</button>}
      </div>
      <div className="card-body overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-2 pr-4 font-semibold text-gray-700">Activity</th>
              <th className="text-center py-2 px-2 font-semibold text-blue-700">Responsible (R)</th>
              <th className="text-center py-2 px-2 font-semibold text-purple-700">Accountable (A)</th>
              <th className="text-center py-2 px-2 font-semibold text-emerald-700">Consulted (C)</th>
              <th className="text-center py-2 px-2 font-semibold text-gray-500">Informed (I)</th>
              <th className="w-16"></th>
            </tr>
          </thead>
          <tbody>
            {raci.map((row, i) => editIdx === i ? (
              <tr key={i} className="bg-indigo-50">
                <td className="py-2 pr-2"><input value={editRow.activity} onChange={e => setEditRow({...editRow, activity: e.target.value})} className={inputClass} /></td>
                <td className={cellClass}><input value={editRow.r} onChange={e => setEditRow({...editRow, r: e.target.value})} className={inputClass} /></td>
                <td className={cellClass}><input value={editRow.a} onChange={e => setEditRow({...editRow, a: e.target.value})} className={inputClass} /></td>
                <td className={cellClass}><input value={editRow.c} onChange={e => setEditRow({...editRow, c: e.target.value})} className={inputClass} /></td>
                <td className={cellClass}><input value={editRow.i} onChange={e => setEditRow({...editRow, i: e.target.value})} className={inputClass} /></td>
                <td className="py-2 px-1 flex gap-1">
                  <button onClick={saveEdit} className="text-xs bg-emerald-600 text-white px-2 py-1 rounded hover:bg-emerald-700">Save</button>
                  <button onClick={() => setEditIdx(null)} className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded hover:bg-gray-300">Cancel</button>
                </td>
              </tr>
            ) : (
              <tr key={i} className={`group border-b border-gray-100 ${i % 2 === 0 ? 'bg-gray-50' : ''}`}>
                <td className="py-2.5 pr-4 font-medium text-gray-800">{row.activity}</td>
                <td className="py-2.5 px-2 text-center text-blue-700 font-semibold">{row.r}</td>
                <td className="py-2.5 px-2 text-center text-purple-700 font-semibold">{row.a}</td>
                <td className="py-2.5 px-2 text-center text-emerald-700">{row.c}</td>
                <td className="py-2.5 px-2 text-center text-gray-500">{row.i}</td>
                <td className="py-2.5 px-1 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                  <button onClick={() => startEdit(i)} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded hover:bg-blue-100 hover:text-blue-700" title="Edit">✏️</button>
                  <button onClick={() => remove(i)} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded hover:bg-red-100 hover:text-red-700" title="Remove">✕</button>
                </td>
              </tr>
            ))}
            {adding && (
              <tr className="bg-indigo-50">
                <td className="py-2 pr-2"><input value={addRow.activity} onChange={e => setAddRow({...addRow, activity: e.target.value})} className={inputClass} placeholder="Activity" autoFocus /></td>
                <td className={cellClass}><input value={addRow.r} onChange={e => setAddRow({...addRow, r: e.target.value})} className={inputClass} placeholder="R" /></td>
                <td className={cellClass}><input value={addRow.a} onChange={e => setAddRow({...addRow, a: e.target.value})} className={inputClass} placeholder="A" /></td>
                <td className={cellClass}><input value={addRow.c} onChange={e => setAddRow({...addRow, c: e.target.value})} className={inputClass} placeholder="C" /></td>
                <td className={cellClass}><input value={addRow.i} onChange={e => setAddRow({...addRow, i: e.target.value})} className={inputClass} placeholder="I" /></td>
                <td className="py-2 px-1 flex gap-1">
                  <button onClick={addItem} className="text-xs bg-emerald-600 text-white px-2 py-1 rounded hover:bg-emerald-700">Add</button>
                  <button onClick={() => setAdding(false)} className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded hover:bg-gray-300">Cancel</button>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

// ─── Reusable: Editable Risk Register ───────────────────────────────────────
function EditableRiskRegister({ risks, onChange }) {
  const [editIdx, setEditIdx] = useState(null)
  const [editRow, setEditRow] = useState({})
  const [adding, setAdding] = useState(false)
  const [addRow, setAddRow] = useState({ risk: '', severity: 'Medium', mitigation: '' })
  const SEVERITY_COLOR = { Critical: 'sky', High: 'teal', Medium: 'emerald' }

  const startEdit = (i) => { setEditIdx(i); setEditRow({ ...risks[i] }) }
  const saveEdit = () => { const next = [...risks]; next[editIdx] = editRow; onChange(next); setEditIdx(null) }
  const remove = (i) => onChange(risks.filter((_, j) => j !== i))
  const addItem = () => { if (!addRow.risk.trim()) return; onChange([...risks, addRow]); setAddRow({ risk: '', severity: 'Medium', mitigation: '' }); setAdding(false) }

  return (
    <div id="pb-risks" className="card">
      <div className="card-header flex items-center justify-between">
        <h3 className="font-bold text-gray-800">Risk Register & Mitigations</h3>
        {!adding && <button onClick={() => setAdding(true)} className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold">+ Add risk</button>}
      </div>
      <div className="card-body space-y-3">
        {risks.map((r, i) => {
          const col = SEVERITY_COLOR[r.severity] || 'gray'
          return editIdx === i ? (
            <div key={i} className="rounded-xl border p-4 bg-indigo-50 border-indigo-200 space-y-2">
              <input value={editRow.risk} onChange={e => setEditRow({...editRow, risk: e.target.value})}
                className="w-full text-sm border border-gray-300 rounded-lg px-3 py-1.5 font-semibold" placeholder="Risk description" />
              <div className="flex gap-2 items-center">
                <label className="text-xs text-gray-600">Severity:</label>
                <select value={editRow.severity} onChange={e => setEditRow({...editRow, severity: e.target.value})}
                  className="text-xs border border-gray-300 rounded px-2 py-1">
                  <option>Critical</option><option>High</option><option>Medium</option>
                </select>
              </div>
              <textarea value={editRow.mitigation} onChange={e => setEditRow({...editRow, mitigation: e.target.value})}
                className="w-full text-sm border border-gray-300 rounded-lg px-3 py-1.5" rows={2} placeholder="Mitigation strategy" />
              <div className="flex gap-2">
                <button onClick={saveEdit} className="text-xs bg-emerald-600 text-white px-3 py-1 rounded-lg hover:bg-emerald-700">Save</button>
                <button onClick={() => setEditIdx(null)} className="text-xs bg-gray-200 text-gray-600 px-3 py-1 rounded-lg hover:bg-gray-300">Cancel</button>
              </div>
            </div>
          ) : (
            <div key={i} className={`group rounded-xl border p-4 bg-${col}-50 border-${col}-200`}>
              <div className="flex items-start gap-3">
                <span className={`bg-${col}-600 text-white text-xs font-bold px-2 py-0.5 rounded-full shrink-0 mt-0.5`}>{r.severity}</span>
                <div className="flex-1">
                  <div className={`font-bold text-${col}-800 text-sm mb-1.5`}>{r.risk}</div>
                  <div className="text-sm text-gray-700">
                    <span className="font-semibold text-gray-600">Mitigation: </span>{r.mitigation}
                  </div>
                </div>
                <div className="opacity-0 group-hover:opacity-100 flex gap-1 shrink-0 transition-opacity">
                  <button onClick={() => startEdit(i)} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded hover:bg-blue-100 hover:text-blue-700" title="Edit">✏️</button>
                  <button onClick={() => remove(i)} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded hover:bg-red-100 hover:text-red-700" title="Remove">✕</button>
                </div>
              </div>
            </div>
          )
        })}
        {adding && (
          <div className="rounded-xl border p-4 bg-indigo-50 border-indigo-200 space-y-2">
            <input value={addRow.risk} onChange={e => setAddRow({...addRow, risk: e.target.value})}
              className="w-full text-sm border border-gray-300 rounded-lg px-3 py-1.5 font-semibold" placeholder="Risk description" autoFocus />
            <div className="flex gap-2 items-center">
              <label className="text-xs text-gray-600">Severity:</label>
              <select value={addRow.severity} onChange={e => setAddRow({...addRow, severity: e.target.value})}
                className="text-xs border border-gray-300 rounded px-2 py-1">
                <option>Critical</option><option>High</option><option>Medium</option>
              </select>
            </div>
            <textarea value={addRow.mitigation} onChange={e => setAddRow({...addRow, mitigation: e.target.value})}
              className="w-full text-sm border border-gray-300 rounded-lg px-3 py-1.5" rows={2} placeholder="Mitigation strategy" />
            <div className="flex gap-2">
              <button onClick={addItem} className="text-xs bg-emerald-600 text-white px-3 py-1 rounded-lg hover:bg-emerald-700">Add</button>
              <button onClick={() => setAdding(false)} className="text-xs bg-gray-200 text-gray-600 px-3 py-1 rounded-lg hover:bg-gray-300">Cancel</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// ─── Reusable: Coverage Section (used inside the Playbook) ───────────────────
// Renders a collection of "change" items (tools, org, devsecops, aiops) with
// expandable per-item cards that show what/how/example/successCriteria.
function CoverageSection({ id, title, icon, tone, tabLabel, tabId, description, items, renderItem }) {
  const [openIdx, setOpenIdx] = useState(null)
  const [sectionOpen, setSectionOpen] = useState(true)
  const toneMap = {
    blue:   { bar: 'bg-blue-500',   text: 'text-blue-100',   border: 'border-blue-200',   chip: 'bg-blue-50 text-blue-800' },
    purple: { bar: 'bg-purple-500', text: 'text-purple-100', border: 'border-purple-200', chip: 'bg-purple-50 text-purple-800' },
    red:    { bar: 'bg-sky-500',    text: 'text-sky-100',    border: 'border-sky-200',    chip: 'bg-sky-50 text-sky-800' },
    indigo: { bar: 'bg-indigo-500', text: 'text-indigo-100', border: 'border-indigo-200', chip: 'bg-indigo-50 text-indigo-800' },
    teal:   { bar: 'bg-teal-500',   text: 'text-teal-100',   border: 'border-teal-200',   chip: 'bg-teal-50 text-teal-800' },
  }[tone] || { bar: 'bg-gray-700', text: 'text-gray-100', border: 'border-gray-200', chip: 'bg-gray-50 text-gray-800' }

  if (!items || items.length === 0) return null

  return (
    <div id={id} className={`rounded-2xl border ${toneMap.border} bg-white overflow-hidden`}>
      <button onClick={() => setSectionOpen(o => !o)} className={`w-full ${toneMap.bar} px-5 py-4 flex items-center justify-between text-left`}>
        <div className="flex-1">
          <div className="font-semibold text-white text-base tracking-tight flex items-center gap-2">
            <span>{icon}</span><span>{title}</span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${toneMap.chip}`}>{items.length} items</span>
          </div>
          <div className={`text-xs mt-1 ${toneMap.text}`}>{description}</div>
        </div>
        <div className="flex items-center gap-2 ml-4">
          <span className="text-[10px] bg-white/10 text-white px-2 py-1 rounded">Also in: <strong>{tabLabel}</strong> tab</span>
          <span className="text-white">{sectionOpen ? '▾' : '▸'}</span>
        </div>
      </button>
      {sectionOpen && (
        <div className="divide-y divide-gray-100">
          {items.map((raw, i) => {
            const r = renderItem(raw)
            const isOpen = openIdx === i
            return (
              <div key={i}>
                <button onClick={() => setOpenIdx(isOpen ? null : i)} className="w-full px-5 py-3 flex items-center gap-3 hover:bg-gray-50 text-left">
                  <span className="text-xl">{r.icon || '•'}</span>
                  <div className="flex-1">
                    <div className="font-semibold text-gray-900 text-sm">{r.title}</div>
                    <div className="text-[11px] text-gray-500 mt-0.5 flex flex-wrap gap-x-3">
                      {r.meta && <span>{r.meta}</span>}
                      {r.owner && <span>👤 {r.owner}</span>}
                      {r.timeline && <span>⏱ {r.timeline}</span>}
                      {r.effort && <span>⚙ {r.effort}</span>}
                    </div>
                  </div>
                  <span className="text-gray-400 text-xs">{isOpen ? '▾' : '▸'}</span>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 space-y-3 bg-gray-50">
                    {r.fields.filter(f => f.value).map((f, fi) => (
                      <div key={fi}>
                        <div className="text-[10px] font-bold uppercase tracking-wide text-gray-500 mb-1">{f.label}</div>
                        {f.code ? (
                          <pre className="bg-gray-900 text-gray-100 text-[11px] p-3 rounded-lg overflow-x-auto whitespace-pre-wrap font-mono leading-relaxed">{f.value}</pre>
                        ) : f.mono ? (
                          <div className="text-xs text-gray-800 whitespace-pre-wrap bg-white border border-gray-200 rounded-lg p-3 leading-relaxed">{f.value}</div>
                        ) : (
                          <div className="text-xs text-gray-700 leading-relaxed">{f.value}</div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}


export default function BusinessCasePage() {
  const { activeScenario, setActiveScenario, addNotification, project, analysisResult, vsmLevel } = useApp()
  const [running, setRunning]       = useState(false)
  const [activeSection, setSection]  = useState('overview')
  const [openSprint, setOpenSprint]  = useState(null)
  const [editedCases, setEditedCases]       = useState(() => JSON.parse(JSON.stringify(BUSINESS_CASES)))
  const [editedPlaybooks, setEditedPlaybooks] = useState(() => JSON.parse(JSON.stringify(PLAYBOOKS)))
  const [editingItem, setEditingItem] = useState(null) // { source:'cases'|'playbooks', section, idx }
  const [editForm, setEditForm]       = useState({})
  const [rmPhaseIdx, setRmPhaseIdx]   = useState(null)
  const [rmLane, setRmLane]           = useState('all')
  const [editedRoadmap, setEditedRoadmap] = useState(() => JSON.parse(JSON.stringify(TRANSFORMATION_ROADMAP)))
  const [editedTsSprintPlan, setEditedTsSprintPlan] = useState(null)
  const [optCPlatform, setOptCPlatform] = useState('stump') // 'homegrown' | 'stump' | 'bmad' | 'copilot_workspace'
  // Configured Target State drives the scenario + platform (instead of A/B/C).
  const [tsCfg, setTsCfg] = useState(null)
  const [tsSteps, setTsSteps] = useState([])      // [{level,label,outcome_scenario,is_target}]
  const [tsStepIdx, setTsStepIdx] = useState(0)
  const [tsPlatformDetail, setTsPlatformDetail] = useState(null) // platform_detail from roadmap response
  useEffect(() => {
    if (!project?.id) { setTsCfg(null); setTsSteps([]); setTsPlatformDetail(null); return }
    const load = () => targetStateApi.getConfig(project.id).then(d => {
      const cfg = d && d.configured !== false ? d : null
      setTsCfg(cfg)
      if (cfg) {
        targetStateApi.roadmap(project.id, {
          platform: cfg.platform, current_level: cfg.current_level, target_level: cfg.target_level,
          interim_count: cfg.interim_count, risk_appetite: cfg.risk_appetite,
        }).then(rm => {
          setTsSteps(rm.steps || [])
          setTsPlatformDetail(rm.platform_detail || null)
          // Build editable sprint plan from platform phasing — split and enrich each action
          if (rm.platform_detail?.playbook_phasing) {
            const platformName = rm.platform_detail.name || rm.platform_detail.id || ''
            setEditedTsSprintPlan(rm.platform_detail.playbook_phasing.map((p, i) => ({
              sprint: `Phase ${i + 1}`, label: p.phase,
              actions: enrichPlaybookActions(p.focus, platformName, p.phase),
              outcomes: [],
            })))
          }
          const tgtIdx = (rm.steps || []).findIndex(s => s.is_target)
          const idx = tgtIdx >= 0 ? tgtIdx : (rm.steps || []).length - 1
          setTsStepIdx(idx)
          const sc = rm.steps?.[idx]?.outcome_scenario
          if (sc) setActiveScenario(sc)
          if (cfg.platform) setOptCPlatform(cfg.platform)
        }).catch(() => {})
      }
    }).catch(() => setTsCfg(null))
    load()
    const onFocus = () => load()
    window.addEventListener('focus', onFocus)
    return () => window.removeEventListener('focus', onFocus)
  }, [project?.id]) // eslint-disable-line

  const pickTsStep = (idx) => {
    setTsStepIdx(idx)
    const sc = tsSteps[idx]?.outcome_scenario
    if (sc) setActiveScenario(sc)
  }
  // ─── Per-org agent → Option A parent-tool lineage (editable) ──────────────
  const [parentMap, setParentMap]               = useState({})
  const [parentMapDirty, setParentMapDirty]     = useState(false)
  const [parentMapSaving, setParentMapSaving]   = useState(false)
  const [parentMapEditorOpen, setParentMapEditorOpen] = useState(false)
  useEffect(() => {
    if (!project?.id) { setParentMap({}); return }
    projectsApi.getOptionAParentMap(project.id)
      .then(r => { setParentMap(r?.option_a_parent_map || {}); setParentMapDirty(false) })
      .catch(() => setParentMap({}))
  }, [project?.id])
  const [trackerData, setTrackerData] = useState(() => {
    try { return JSON.parse(localStorage.getItem('pdlc_tracker') || '{}') } catch { return {} }
  })
  const [trackerFilter, setTrackerFilter] = useState({ lane: 'all', status: 'all', phase: 'all' })
  const [trackerSort, setTrackerSort]     = useState({ col: 'phase', dir: 'asc' })
  const [editingAction, setEditingAction] = useState(null)
  const [teamPlans, setTeamPlans] = useState(() => {
    try { return JSON.parse(localStorage.getItem('pdlc_team_plans') || '{}') } catch { return {} }
  })
  const [teamTrackers, setTeamTrackers] = useState(() => {
    try { return JSON.parse(localStorage.getItem('pdlc_team_trackers') || '{}') } catch { return {} }
  })
  const [addingTeam, setAddingTeam] = useState(false)
  const [newTeamName, setNewTeamName] = useState('')
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [costOverrides, setCostOverrides] = useState({})
  const [rolesOverrides, setRolesOverrides] = useState({})

  const saveTracker = (next) => {
    setTrackerData(next)
    localStorage.setItem('pdlc_tracker', JSON.stringify(next))
  }
  const updateAction = (id, field, value) => {
    saveTracker({ ...trackerData, [id]: { ...(trackerData[id] || {}), [field]: value } })
  }

  // Flatten all roadmap actions for current scenario into a table
  const getFlatActions = (scenario) => {
    const rm = editedRoadmap[scenario]
    if (!rm) return []
    const rows = []
    rm.phases.forEach((ph, phIdx) => {
      Object.keys(LANE_STYLE).forEach(lane => {
        ;(ph[lane] || []).forEach((action, itemIdx) => {
          const id = `${scenario}_${phIdx}_${lane}_${itemIdx}`
          rows.push({ id, phaseIdx: phIdx, phaseName: ph.name, phaseRange: ph.range, phaseColor: ph.color, lane, action })
        })
      })
    })
    return rows
  }

  // Extract all teams from project productGroups hierarchy
  const getAllTeams = () => {
    const teams = []
    ;(project.productGroups || []).forEach(pg => {
      ;(pg.products || []).forEach(prod => {
        ;(prod.teams || []).forEach(t => {
          if (!teams.find(x => x.name === t)) teams.push({ name: t, product: prod.name, productGroup: pg.name })
        })
      })
    })
    // If no teams in project yet, fall back to project.team
    if (teams.length === 0 && project.team) teams.push({ name: project.team, product: project.product || '', productGroup: project.productGroup || '' })
    // Also include any manually added teams from teamPlans not in productGroups
    Object.keys(teamPlans).forEach(t => { if (!teams.find(x => x.name === t)) teams.push({ name: t, product: '', productGroup: '' }) })
    return teams
  }

  const saveTeamPlan = (teamName, option) => {
    const next = { ...teamPlans, [teamName]: { option, savedAt: new Date().toISOString() } }
    setTeamPlans(next)
    localStorage.setItem('pdlc_team_plans', JSON.stringify(next))
  }

  const removeTeamPlan = (teamName) => {
    const next = { ...teamPlans }
    delete next[teamName]
    setTeamPlans(next)
    localStorage.setItem('pdlc_team_plans', JSON.stringify(next))
    const tt = { ...teamTrackers }
    delete tt[teamName]
    setTeamTrackers(tt)
    localStorage.setItem('pdlc_team_trackers', JSON.stringify(tt))
  }

  const updateTeamAction = (teamName, id, field, value) => {
    const teamData = teamTrackers[teamName] || {}
    const next = { ...teamTrackers, [teamName]: { ...teamData, [id]: { ...(teamData[id] || {}), [field]: value } } }
    setTeamTrackers(next)
    localStorage.setItem('pdlc_team_trackers', JSON.stringify(next))
  }

  const getTeamProgress = (teamName) => {
    const plan = teamPlans[teamName]
    if (!plan) return null
    const actions = getFlatActions(plan.option)
    if (actions.length === 0) return { pct: 0, done: 0, total: 0, byLane: {} }
    const td = teamTrackers[teamName] || {}
    const done = actions.filter(a => td[a.id]?.status === 'complete').length
    const byLane = {}
    Object.keys(LANE_STYLE).forEach(lane => {
      const laneActions = actions.filter(a => a.lane === lane)
      const laneDone = laneActions.filter(a => td[a.id]?.status === 'complete').length
      byLane[lane] = { done: laneDone, total: laneActions.length }
    })
    return { pct: Math.round((done / actions.length) * 100), done, total: actions.length, byLane }
  }

  const scenario = FUTURE_STATE_SCENARIOS.find(s => s.id === activeScenario)
  const bc = editedCases[activeScenario]
  const tl = IMPLEMENTATION_TIMELINES[activeScenario]
  const basePb = editedPlaybooks[activeScenario]

  // When Target State Studio is configured, override playbook header + phasing with level/platform context
  const activeStep = tsSteps[tsStepIdx]
  const pb = (tsCfg && tsPlatformDetail && activeStep && basePb)
    ? {
        ...basePb,
        label: `L${activeStep.level} — ${activeStep.label} (${tsPlatformDetail.name || tsPlatformDetail.id})`,
        executiveSummary: `${activeStep.summary || basePb.executiveSummary} Platform: ${tsPlatformDetail.name}. ${tsPlatformDetail.tagline || ''}`.trim(),
        teamSize: activeStep.human_roles_retained
          ? `${activeStep.human_roles_retained} retained roles`
          : basePb.teamSize,
        teamDuration: tsPlatformDetail.playbook_phasing?.length
          ? tsPlatformDetail.playbook_phasing[tsPlatformDetail.playbook_phasing.length - 1]?.phase?.match(/\d+/g)?.pop()
            ? `~${tsPlatformDetail.playbook_phasing[tsPlatformDetail.playbook_phasing.length - 1].phase.match(/\d+/g).pop()}+ weeks`
            : basePb.teamDuration
          : basePb.teamDuration,
        sprintPlan: editedTsSprintPlan || (tsPlatformDetail.playbook_phasing || []).map((p, i) => ({
          sprint: `Phase ${i + 1}`, label: p.phase,
          actions: enrichPlaybookActions(p.focus, tsPlatformDetail.name || '', p.phase),
          outcomes: [],
        })),
      }
    : basePb

  const openEdit = (source, section, idx) => {
    const data = source === 'cases' ? editedCases : editedPlaybooks
    setEditingItem({ source, section, idx })
    setEditForm({ ...data[activeScenario][section][idx] })
  }

  const saveItem = () => {
    if (!editingItem) return
    const { source, section, idx } = editingItem
    if (source === 'cases') {
      setEditedCases(prev => {
        const next = JSON.parse(JSON.stringify(prev))
        next[activeScenario][section][idx] = editForm
        return next
      })
    } else {
      setEditedPlaybooks(prev => {
        const next = JSON.parse(JSON.stringify(prev))
        next[activeScenario][section][idx] = editForm
        return next
      })
    }
    setEditingItem(null)
  }

  const runAgent = async () => {
    setRunning(true)
    try {
      await agentsApi.runBusinessCaseBuilder(project.id || 'demo', activeScenario)
      addNotification('Business case generated!', 'success')
    } catch { addNotification('Using built-in business case (demo mode)', 'info') }
    finally { setRunning(false) }
  }

  const SEVERITY_COLOR = { Critical: 'sky', High: 'teal', Medium: 'emerald' }

  return (
    <div className="space-y-6 fade-in">
      <TargetStateBanner />
      {/* Header */}
      <div className="bg-gradient-to-r from-sky-500 to-emerald-500 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Business Case & Implementation Playbook</h2>
            <p className="text-emerald-100">Investment, ROI, implementation guide, timeline, org change, tools, DevSecOps, and AIOps requirements</p>
          </div>
          <button onClick={runAgent} disabled={running} className="bg-white text-emerald-700 px-5 py-2.5 rounded-lg font-semibold text-sm hover:bg-emerald-50 shadow">
            {running ? '⏳ Building...' : '🤖 Run Business Case Agent'}
          </button>
        </div>
      </div>

      <StepReviewBar stepKey="business_case" stepLabel="Business Case" />

      {/* Configured target-state step selector (replaces A/B/C when a target is set) */}
      {tsCfg && tsSteps.length > 0 && (
        <div className="bg-gradient-to-r from-sky-50 to-indigo-50 p-4 rounded-xl border-2 border-sky-200">
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-bold bg-sky-600 text-white px-2 py-0.5 rounded-full">Target State Driven</span>
                <span className="text-sm font-bold text-sky-800">{(tsCfg.platform || '').replace('_', ' ')} Platform</span>
              </div>
              <div className="text-xs text-gray-500">
                All business case tabs — operating model, tools, roadmap, action plan — reflect the selected maturity level below.
                <b className="text-sky-700 ml-1">{tsSteps.map(s => `L${s.level}`).join(' → ')}</b>
              </div>
            </div>
            <Link to="/target-state" className="text-xs px-3 py-1.5 bg-sky-600 text-white rounded-lg font-semibold hover:bg-sky-700">
              Edit in Studio
            </Link>
          </div>
          <div className="flex flex-wrap gap-2">
            {tsSteps.map((s, i) => {
              const isActive = i === tsStepIdx
              return (
                <button key={s.step} onClick={() => { pickTsStep(i); setRmPhaseIdx(null) }}
                  className={`px-4 py-2.5 rounded-lg text-sm font-semibold border-2 transition-all ${
                    isActive
                      ? 'border-sky-600 bg-sky-500 text-white shadow-md scale-105'
                      : 'border-gray-200 bg-white text-gray-600 hover:border-sky-300 hover:bg-sky-50'
                  }`}>
                  <div className="flex items-center gap-1.5">
                    {s.is_target && <span className="text-amber-300">★</span>}
                    <span>L{s.level}</span>
                    <span className="text-xs opacity-80">· {s.label}</span>
                  </div>
                  <div className={`text-[10px] mt-0.5 ${isActive ? 'text-sky-100' : 'text-gray-400'}`}>
                    {s.ml_band || s.outcome_scenario.replace('option-', 'Option ').toUpperCase()}
                    {s.is_target && ' (Target)'}
                  </div>
                </button>
              )
            })}
          </div>
          {tsSteps[tsStepIdx] && (
            <div className="mt-3 pt-2 border-t border-sky-200/50 flex items-center gap-3 text-xs text-sky-700">
              <span className="font-semibold">Current view: L{tsSteps[tsStepIdx].level} — {tsSteps[tsStepIdx].label}</span>
              <span className="text-sky-500">|</span>
              <span>Platform: {(tsCfg.platform || '').replace('_', ' ')}</span>
              <span className="text-sky-500">|</span>
              <span>Risk appetite: {tsCfg.risk_appetite || 'medium'}</span>
              {tsCfg.current_level && (
                <>
                  <span className="text-sky-500">|</span>
                  <span>Current: L{tsCfg.current_level} → Target: L{tsCfg.target_level}</span>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* Scenario selector (classic A/B/C — hidden when a target state is configured) */}
      {!tsCfg && <div className="grid grid-cols-3 gap-4">
        {FUTURE_STATE_SCENARIOS.map(s => {
          const sbc = BUSINESS_CASES[s.id]
          const stl = IMPLEMENTATION_TIMELINES[s.id]
          return (
            <button key={s.id} onClick={() => { setActiveScenario(s.id); setRmPhaseIdx(null) }}
              className={`p-4 rounded-xl text-left border-2 transition-all ${activeScenario === s.id ? 'border-emerald-500 bg-emerald-50 shadow-md' : 'border-gray-200 bg-white hover:border-gray-400'}`}>
              <div className="font-bold text-gray-800 mb-1">{s.label}: {s.title.split('—')[0].trim()}</div>
              <div className="text-xs text-gray-500 mb-2">{s.subtitle}</div>
              <div className="text-xs space-y-1">
                <div><span className="text-gray-500">Investment: </span><span className="font-bold text-emerald-700">{sbc.investmentRange}</span></div>
                <div><span className="text-gray-500">ROI: </span><span className="font-bold text-green-700">{sbc.roiMultiple} in {sbc.roiTimeline}</span></div>
                <div><span className="text-gray-500">Team timeline: </span><span className="font-bold text-blue-700">{stl.teamDuration}</span></div>
              </div>
            </button>
          )
        })}
      </div>}

      {/* Section nav */}
      <div className="flex flex-wrap gap-2 bg-white p-3 rounded-xl border border-gray-200">
        {SECTIONS.map(s => (
          <button key={s.id} onClick={() => setSection(s.id)}
            className={`px-4 py-1.5 rounded-lg text-sm font-semibold whitespace-nowrap ${activeSection === s.id ? 'bg-emerald-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {s.id === 'playbook' ? '📋 ' : s.id === 'timeline' ? '📅 ' : s.id === 'devsecops' ? '🔒 ' : s.id === 'aiops' ? '🤖 ' : ''}{s.label}
          </button>
        ))}
      </div>

      {/* ── Overview ── */}
      {activeSection === 'overview' && (() => {
        const CURRENT_BASE = vsmLevel === 'user-story'
          ? { leadTime: 8.5, processTime: 40, waitTime: 130, flowEfficiency: 10.2 }
          : { leadTime: 42.5, processTime: 100, waitTime: 536, flowEfficiency: 8.1 }
        const fsTotals = getOptionTotals(activeScenario)
        const arMetrics = analysisResult?.metrics || null
        return (
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Investment',    value: bc.investmentRange, color: 'emerald', icon: '💰' },
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

          {/* Future State VSM Metrics — current → projected */}
          <div className="card overflow-hidden">
            <div className="bg-gradient-to-r from-sky-500 to-teal-500 px-5 py-3 flex items-center justify-between">
              <div>
                <div className="font-bold text-white text-sm">Future State VSM Metrics — {scenario?.label}</div>
                <div className="text-xs text-white/80">
                  {tsCfg ? `L${tsSteps[tsStepIdx]?.level || '?'} target on ${(tsCfg.platform || '').replace('_', ' ')}` : 'Current → Projected improvement'}
                  {arMetrics && <span className="ml-2 bg-white/20 px-1.5 py-0.5 rounded text-[10px]">Analysis data available</span>}
                </div>
              </div>
              <Link to="/future-state" className="text-xs bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-lg font-semibold">
                View Full Future State
              </Link>
            </div>
            <div className="card-body">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Process Time', current: `${CURRENT_BASE.processTime}h`, future: `${fsTotals.processTime}h`, pct: Math.round((1 - fsTotals.processTime / CURRENT_BASE.processTime) * 100), icon: '⚡' },
                  { label: 'Wait Time', current: `${CURRENT_BASE.waitTime}h`, future: `${fsTotals.waitTime}h`, pct: Math.round((1 - fsTotals.waitTime / CURRENT_BASE.waitTime) * 100), icon: '⏱️' },
                  { label: 'Lead Time', current: `${CURRENT_BASE.leadTime}d`, future: `${fsTotals.leadTime}d`, pct: Math.round((1 - fsTotals.leadTime / CURRENT_BASE.leadTime) * 100), icon: '📉' },
                  { label: 'Flow Efficiency', current: `${CURRENT_BASE.flowEfficiency}%`, future: `${fsTotals.flowEfficiency}%`, pct: Math.round(fsTotals.flowEfficiency - CURRENT_BASE.flowEfficiency), icon: '🔄', isUp: true },
                ].map(m => (
                  <div key={m.label} className="text-center p-3 bg-gray-50 rounded-xl">
                    <div className="text-lg mb-1">{m.icon}</div>
                    <div className="text-xs text-gray-500 mb-1">{m.label}</div>
                    <div className="flex items-center justify-center gap-2">
                      <span className="text-sm text-gray-400 line-through">{m.current}</span>
                      <span className="text-gray-400">→</span>
                      <span className="text-sm font-bold text-gray-800">{m.future}</span>
                    </div>
                    <div className={`text-xs font-bold mt-1 ${m.isUp ? 'text-green-600' : m.pct > 0 ? 'text-green-600' : 'text-gray-500'}`}>
                      {m.isUp ? `+${m.pct} pts` : m.pct > 0 ? `-${m.pct}%` : 'No change'}
                    </div>
                  </div>
                ))}
              </div>
              {analysisResult?.bottlenecks?.length > 0 && (
                <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
                  <span className="bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-semibold">{analysisResult.bottlenecks.length} bottlenecks identified</span>
                  <Link to="/bottlenecks" className="text-sky-600 hover:underline">View analysis →</Link>
                </div>
              )}
            </div>
          </div>
        </div>
        )
      })()}

      {/* ── Operating Model ── */}
      {activeSection === 'opmodel' && (() => {
        const om = OPERATING_MODEL[activeScenario]
        if (!om) return null
        const platform = activeScenario === 'option-c' ? om.platforms[optCPlatform] : null
        const teamForDisplay = activeScenario === 'option-c'
          ? om.teams.map(t => t.name === 'AI Platform Ops' ? { ...t, roles: platform.platformOps.roles, size: platform.platformOps.size, name: platform.platformOps.name } : t)
          : om.teams

        const govColors = { green: { bg: 'bg-green-100', border: 'border-green-300', badge: 'bg-green-600', text: 'text-green-800', bar: 'bg-green-500' }, amber: { bg: 'bg-emerald-100', border: 'border-emerald-300', badge: 'bg-emerald-600', text: 'text-emerald-800', bar: 'bg-emerald-500' }, red: { bg: 'bg-sky-100', border: 'border-sky-300', badge: 'bg-sky-600', text: 'text-sky-800', bar: 'bg-sky-500' } }
        const roleColors = { blue: 'bg-blue-50 border-blue-200', purple: 'bg-purple-50 border-purple-200', green: 'bg-green-50 border-green-200', orange: 'bg-teal-50 border-teal-200', red: 'bg-sky-50 border-sky-200', teal: 'bg-teal-50 border-teal-200', indigo: 'bg-indigo-50 border-indigo-200', emerald: 'bg-emerald-50 border-emerald-200' }
        const roleBadge = { blue: 'bg-blue-600', purple: 'bg-purple-600', green: 'bg-green-600', orange: 'bg-teal-600', red: 'bg-sky-600', teal: 'bg-teal-600', indigo: 'bg-indigo-600', emerald: 'bg-emerald-600' }
        const teamBg = { blue: 'border-blue-300 bg-blue-50', purple: 'border-purple-300 bg-purple-50', indigo: 'border-indigo-300 bg-indigo-50', amber: 'border-emerald-300 bg-emerald-50', emerald: 'border-emerald-300 bg-emerald-50', teal: 'border-teal-300 bg-teal-50' }
        const teamBadge = { blue: 'bg-blue-600', purple: 'bg-purple-600', indigo: 'bg-indigo-600', amber: 'bg-emerald-600', emerald: 'bg-emerald-600', teal: 'bg-teal-600' }

        return (
          <div className="space-y-8">

            {/* ── Header ── */}
            <div className={`rounded-2xl border-2 p-6 ${activeScenario === 'option-a' ? 'bg-blue-50 border-blue-200' : activeScenario === 'option-b' ? 'bg-purple-50 border-purple-200' : 'bg-emerald-50 border-emerald-200'}`}>
              <div className="flex items-start justify-between gap-6">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`text-xs font-bold px-3 py-1 rounded-full text-white ${activeScenario === 'option-a' ? 'bg-blue-600' : activeScenario === 'option-b' ? 'bg-purple-600' : 'bg-emerald-600'}`}>{scenario?.label}</span>
                    {tsCfg && tsSteps[tsStepIdx] && (
                      <span className="text-xs font-bold bg-sky-100 text-sky-700 px-2 py-0.5 rounded-full border border-sky-300">
                        L{tsSteps[tsStepIdx].level} · {(tsCfg.platform || '').replace('_', ' ')}
                      </span>
                    )}
                    <span className="text-lg font-bold text-gray-900">{om.maturity}</span>
                    <span className="text-sm text-gray-500">— {om.tagline}</span>
                  </div>
                  <p className="text-sm text-gray-600 mb-4">How engineering teams are structured, what humans do vs agents do, and how performance and cost are governed at this maturity level.</p>
                  {/* Human vs Agent split bar */}
                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-gray-600">Human Activity</span>
                      <span className="text-gray-600">Agent Activity</span>
                    </div>
                    <div className="flex h-6 rounded-full overflow-hidden border border-gray-300">
                      <div className="flex items-center justify-center text-white text-xs font-bold transition-all duration-500" style={{ width: `${om.humanPct}%`, background: activeScenario === 'option-a' ? '#2563eb' : activeScenario === 'option-b' ? '#7c3aed' : '#059669' }}>{om.humanPct}% Human</div>
                      <div className="flex items-center justify-center text-white text-xs font-bold transition-all duration-500" style={{ width: `${om.agentPct}%`, background: '#1e293b' }}>{om.agentPct}% Agents</div>
                    </div>
                    <div className="flex justify-between text-[10px] text-gray-400 mt-1">
                      <span>Humans decide and execute</span>
                      <span>Agents execute autonomously</span>
                    </div>
                  </div>
                </div>
                {/* Summary stats */}
                <div className="grid grid-cols-2 gap-3 shrink-0">
                  {[
                    { label: 'Team Size', value: activeScenario === 'option-a' ? '8–10 / squad' : activeScenario === 'option-b' ? '5–7 / squad' : '3–5 / pod' },
                    { label: 'Squads / Pods', value: activeScenario === 'option-a' ? '8 squads' : activeScenario === 'option-b' ? '5–6 squads' : '3–4 pods' },
                    { label: 'Agent Fleet', value: activeScenario === 'option-a' ? '16 tools' : activeScenario === 'option-b' ? '21 agents' : '21 agents (full)' },
                    { label: 'Governance Model', value: activeScenario === 'option-a' ? 'Human-first' : activeScenario === 'option-b' ? 'Tiered' : 'Policy-first' },
                  ].map(s => (
                    <div key={s.label} className="bg-white/80 rounded-xl p-3 border border-white text-center min-w-[100px]">
                      <div className="text-xs text-gray-500 mb-0.5">{s.label}</div>
                      <div className="text-sm font-bold text-gray-800">{s.value}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* ── Option C Platform Decision ── */}
            {activeScenario === 'option-c' && (
              <div className="rounded-2xl border-2 border-gray-200 overflow-hidden">
                <div className="bg-gray-800 px-5 py-4 flex items-center gap-3">
                  <span className="text-2xl">🏛️</span>
                  <div>
                    <div className="font-bold text-white text-base">Option C Platform Decision</div>
                    <div className="text-gray-400 text-xs mt-0.5">Choose your agent orchestration strategy — this affects investment, timeline, team composition, and operating model</div>
                  </div>
                </div>
                <div className="p-5 bg-white">
                  <div className="grid grid-cols-2 xl:grid-cols-4 gap-3 mb-5">
                    {Object.entries(om.platforms).map(([key, plat]) => {
                      const selectorAccent = {
                        homegrown:         { border: 'border-gray-700',     bg: 'bg-gray-50',     chip: 'Full Control',   tone: 'text-emerald-700' },
                        stump:             { border: 'border-emerald-500',  bg: 'bg-emerald-50',  chip: 'Recommended',    tone: 'text-emerald-700' },
                        bmad:              { border: 'border-indigo-500',   bg: 'bg-indigo-50',   chip: 'Open Source',    tone: 'text-indigo-700' },
                        copilot_workspace: { border: 'border-emerald-500',    bg: 'bg-emerald-50',    chip: 'Fastest',        tone: 'text-emerald-700' },
                      }[key] || { border: 'border-gray-500', bg: 'bg-gray-50', chip: 'Option', tone: 'text-gray-700' }
                      const selected = optCPlatform === key
                      return (
                        <button key={key} onClick={() => setOptCPlatform(key)}
                          className={`text-left rounded-xl border-2 p-3 transition-all flex flex-col h-full ${selected ? `${selectorAccent.border} ${selectorAccent.bg} shadow-md` : 'border-gray-200 bg-white hover:border-gray-400'}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className={`text-[10px] font-bold text-white px-2 py-0.5 rounded-full ${plat.badge}`}>{selectorAccent.chip}</span>
                            {selected && <span className="text-emerald-600 text-sm">✓</span>}
                          </div>
                          <div className="font-bold text-gray-900 text-sm mb-1 leading-tight">{plat.name}</div>
                          <div className="text-[11px] text-gray-500 mb-3 leading-snug">{plat.tagline}</div>
                          <div className="space-y-1 mt-auto">
                            <div className="text-[11px]"><span className="font-semibold text-gray-600">Investment: </span><span className={`font-semibold ${selectorAccent.tone}`}>{plat.investmentNote}</span></div>
                            <div className="text-[11px]"><span className="font-semibold text-gray-600">Timeline: </span><span className={`font-semibold ${selectorAccent.tone}`}>{plat.timelineNote}</span></div>
                            <div className="text-[11px]"><span className="font-semibold text-gray-600">Ops team: </span><span className="text-gray-700">{plat.platformOps.size} · {plat.platformOps.name}</span></div>
                          </div>
                        </button>
                      )
                    })}
                  </div>
                  {/* Pros / Cons */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-xs font-bold text-green-700 uppercase tracking-wide mb-2">✓ Advantages — {platform?.name}</div>
                      <ul className="space-y-1.5">
                        {platform?.pros.map((p, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                            <span className="text-green-500 mt-0.5 shrink-0">✓</span>{p}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <div className="text-xs font-bold text-sky-700 uppercase tracking-wide mb-2">⚠ Considerations — {platform?.name}</div>
                      <ul className="space-y-1.5">
                        {platform?.cons.map((c, i) => (
                          <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
                            <span className="text-emerald-500 mt-0.5 shrink-0">⚠</span>{c}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* ── Per-org Agent Lineage Editor (contextualises the "← parent" labels on every pill) ── */}
            <div className="rounded-2xl border border-gray-200 overflow-hidden bg-white">
              <button
                onClick={() => setParentMapEditorOpen(o => !o)}
                className="w-full px-5 py-3 flex items-center justify-between bg-gray-50 hover:bg-gray-100 transition-colors border-b border-gray-200">
                <div className="flex items-center gap-3">
                  <span className="text-lg">🧬</span>
                  <div className="text-left">
                    <div className="font-semibold text-gray-900 text-sm">Customise Agent Lineage for {project?.organization || 'this organisation'}</div>
                    <div className="text-xs text-gray-500">Override the Option A parent tool shown under each Option B agent pill. {Object.keys(parentMap).length > 0 ? `${Object.keys(parentMap).length} of 21 agents customised — falling back to US Bank defaults for the rest.` : 'Currently using US Bank defaults for all 21 agents.'}</div>
                  </div>
                </div>
                <span className="text-gray-400 text-xs">{parentMapEditorOpen ? '▾ Close' : '▸ Edit'}</span>
              </button>
              {parentMapEditorOpen && (
                <div className="p-5">
                  <div className="grid grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-2 mb-4">
                    {Object.keys(DEFAULT_AGENT_PARENT_MAP).map(agentName => {
                      const overridden = parentMap[agentName] !== undefined
                      const value = overridden ? parentMap[agentName] : ''
                      const placeholder = DEFAULT_AGENT_PARENT_MAP[agentName]
                      return (
                        <label key={agentName} className="flex flex-col gap-1">
                          <span className="text-[11px] font-semibold text-gray-700">{agentName}</span>
                          <input
                            type="text"
                            value={value}
                            placeholder={`Default: ← ${placeholder}`}
                            onChange={e => {
                              const v = e.target.value
                              setParentMap(prev => {
                                const next = { ...prev }
                                if (v.trim() === '') delete next[agentName]
                                else next[agentName] = v
                                return next
                              })
                              setParentMapDirty(true)
                            }}
                            className={`text-xs px-2 py-1.5 rounded-md border focus:outline-none focus:ring-2 ${overridden ? 'border-indigo-300 bg-indigo-50 focus:ring-indigo-300' : 'border-gray-200 bg-white focus:ring-gray-300'}`}
                          />
                        </label>
                      )
                    })}
                  </div>
                  <div className="flex items-center justify-between pt-3 border-t border-gray-200">
                    <div className="text-xs text-gray-500">
                      Tip: capture these from the team's current ALM / DevSecOps / observability stack during ALM Connect or DORA Assessment intake.
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => { setParentMap({}); setParentMapDirty(true) }}
                        className="text-xs px-3 py-1.5 rounded-md border border-gray-300 text-gray-600 hover:bg-gray-50">
                        Reset to defaults
                      </button>
                      <button
                        disabled={!parentMapDirty || parentMapSaving || !project?.id}
                        onClick={async () => {
                          setParentMapSaving(true)
                          try {
                            await projectsApi.putOptionAParentMap(project.id, parentMap)
                            setParentMapDirty(false)
                            addNotification?.({ type: 'success', message: 'Agent lineage saved' })
                          } catch (err) {
                            addNotification?.({ type: 'error', message: 'Failed to save: ' + (err?.message || 'unknown') })
                          } finally {
                            setParentMapSaving(false)
                          }
                        }}
                        className="text-xs px-4 py-1.5 rounded-md bg-indigo-600 text-white font-semibold hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
                        {parentMapSaving ? 'Saving…' : parentMapDirty ? 'Save Changes' : 'Saved'}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* ── Team Topology ── */}
            <div className="rounded-2xl border border-gray-200 overflow-hidden">
              <div className="bg-slate-900 px-5 py-4">
                <div className="font-semibold text-white text-lg tracking-tight">Team Topology — {scenario?.label}: {om.maturity}</div>
                <div className="text-slate-200 text-xs mt-1">How engineering teams are structured and what AI layer each team owns</div>
              </div>
              <div className="p-5 bg-white">
                <div className={`grid gap-4 ${teamForDisplay.length >= 4 ? 'grid-cols-2 xl:grid-cols-4' : 'grid-cols-3'}`}>
                  {teamForDisplay.map((team, ti) => (
                    <div key={ti} className={`rounded-xl border-2 p-4 ${teamBg[team.color] || 'border-gray-200 bg-gray-50'}`}>
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <div className="font-bold text-gray-900 text-sm">{team.name}</div>
                          <div className="text-xs text-gray-500">{team.size}</div>
                        </div>
                        <span className={`text-[10px] font-bold text-white px-2 py-0.5 rounded-full shrink-0 ${teamBadge[team.color] || 'bg-gray-600'}`}>{team.type}</span>
                      </div>
                      <div className="mb-3">
                        <div className="text-[10px] font-bold text-gray-400 uppercase tracking-wide mb-1.5">Roles</div>
                        <div className="flex flex-wrap gap-1">
                          {team.roles.map((r, ri) => (
                            <span key={ri} className="bg-white border border-gray-200 text-gray-700 text-[10px] px-1.5 py-0.5 rounded-full">{r}</span>
                          ))}
                        </div>
                      </div>
                      <div className={`rounded-lg p-2.5 border ${teamBg[team.color] || 'bg-gray-50 border-gray-200'}`} style={{ background: 'rgba(255,255,255,0.6)' }}>
                        <div className="text-[10px] font-bold text-gray-500 uppercase tracking-wide mb-1">AI / Agent Layer</div>
                        <div className="text-[11px] text-gray-700">{team.aiLayer}</div>
                      </div>
                    </div>
                  ))}
                </div>
                {/* Agent fleet connector line — each agent shows its parent tool / platform */}
                {activeScenario !== 'option-a' && (
                  <div className="mt-4 bg-slate-900 rounded-xl p-3">
                    <div className="text-slate-300 text-[10px] font-bold uppercase tracking-wide mb-2">Agent Platform — Lineage from {activeScenario === 'option-b' ? 'Option A tools' : 'selected platform'}</div>
                    <div className="flex flex-wrap gap-1.5">
                      {(activeScenario === 'option-b'
                        ? ['Discovery Agent','Backlog Agent','Sprint Agent','Architecture Agent','Design Review Agent','Code Generator','Code Reviewer','Tech Debt Agent','Build Agent','Pipeline Agent','Vuln. Fix Agent','QA Orchestrator','UAT Agent','Regression Agent','Release Gate Agent','Deploy Agent','Rollback Agent','Monitor Agent','Incident Triage Agent','Compliance Agent']
                        : ['Discovery Agent','Backlog Agent','Sprint Agent','Architecture Agent','Design Review Agent','Code Generator','Code Reviewer','Tech Debt Agent','Build Agent','Pipeline Agent','Vuln. Fix Agent','QA Orchestrator','UAT Agent','Regression Agent','Release Gate Agent','Deploy Agent','Rollback Agent','Monitor Agent','Incident Triage Agent','Compliance Agent']
                      ).map((a, i) => {
                        const parent = resolveAgentParent(a, {
                          scenario: activeScenario,
                          platform: activeScenario === 'option-c' ? optCPlatform : null,
                          orgMap: (parentMap && Object.keys(parentMap).length) ? parentMap : null,
                        })
                        return (
                          <span key={i} className="inline-flex flex-col items-center whitespace-nowrap bg-slate-700 rounded-md overflow-hidden">
                            <span className="text-slate-100 text-[10px] px-2 pt-1 font-medium leading-tight">{a}</span>
                            {parent && (
                              <span className="text-slate-400 text-[8.5px] px-2 pb-1 leading-tight italic">← {parent}</span>
                            )}
                          </span>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* ── Agent ↔ Human Interaction Diagram ── */}
            <div className="rounded-2xl border border-gray-200 overflow-hidden">
              <div className="bg-indigo-900 px-5 py-4">
                <div className="font-semibold text-white text-lg tracking-tight">Agent ↔ Human Interaction Model</div>
                <div className="text-indigo-100 text-xs mt-1">Which agents interact with which human roles, what humans are responsible for, and what agents handle autonomously</div>
              </div>
              {/* Column headers */}
              <div className="grid grid-cols-12 gap-0 bg-gray-100 border-b border-gray-200 text-[10px] font-bold uppercase tracking-wide text-gray-600">
                <div className="col-span-3 px-4 py-2 border-r border-gray-200">Role</div>
                <div className="col-span-4 px-4 py-2 border-r border-gray-200">Human Responsibilities</div>
                <div className="col-span-5 px-4 py-2">Agent Responsibilities &amp; Tools</div>
              </div>
              <div className="divide-y divide-gray-100">
                {om.interactions.map((row, ri) => (
                  <div key={ri} className={`grid grid-cols-12 gap-0 ${ri % 2 === 0 ? 'bg-white' : 'bg-gray-50/60'}`}>
                    {/* Role */}
                    <div className={`col-span-3 p-4 border-r border-gray-200 ${roleColors[row.color] || 'bg-gray-50 border-gray-200'}`}>
                      <div className="flex items-center gap-2 mb-1.5">
                        <span className={`w-9 h-9 rounded-full flex items-center justify-center text-base shrink-0 ${roleBadge[row.color] || 'bg-gray-600'}`}>{row.icon}</span>
                        <span className="font-bold text-gray-900 text-sm leading-tight">{row.role}</span>
                      </div>
                      {row.scope && (() => {
                        const isShared = /shared|fractional|org-wide|governance/i.test(row.scope)
                        return (
                          <span className={`inline-block text-[9.5px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full ${isShared ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-emerald-100 text-emerald-800 border border-emerald-200'}`}>
                            {row.scope}
                          </span>
                        )
                      })()}
                    </div>
                    {/* Human Responsibilities */}
                    <div className="col-span-4 p-4 border-r border-gray-200">
                      <p className="text-xs text-gray-700 leading-relaxed">{row.humanDoes}</p>
                    </div>
                    {/* Agent Responsibilities & Tools */}
                    <div className="col-span-5 p-4">
                      <p className="text-xs text-gray-700 mb-2.5 leading-relaxed">{row.agentHelps}</p>
                      <div className="flex flex-wrap gap-1.5 mb-2.5">
                        {row.agentNames.map((a, ai) => {
                          const parent = resolveAgentParent(a, {
                            scenario: activeScenario,
                            platform: activeScenario === 'option-c' ? optCPlatform : null,
                            orgMap: (parentMap && Object.keys(parentMap).length) ? parentMap : null,
                          })
                          return (
                            <span key={ai} className="inline-flex flex-col items-center whitespace-nowrap bg-slate-800 rounded-md overflow-hidden">
                              <span className="text-slate-100 text-[10px] px-2.5 pt-1 font-medium leading-tight">{a}</span>
                              {parent && (
                                <span className="text-slate-300 text-[8.5px] px-2.5 pb-1 leading-tight italic">← {parent}</span>
                              )}
                            </span>
                          )
                        })}
                      </div>
                      <div className="flex items-start gap-1.5 pt-2 border-t border-gray-200">
                        <span className="text-gray-400 text-xs leading-none mt-0.5">⇄</span>
                        <span className="text-[10px] text-gray-500 italic leading-snug">{row.ownership}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* ── Governance Tiers ── */}
            <div className="rounded-2xl border border-gray-200 overflow-hidden">
              <div className="bg-gray-900 px-5 py-4">
                <div className="font-semibold text-white text-lg tracking-tight">Decision Governance Framework</div>
                <div className="text-gray-200 text-xs mt-1">What agents decide autonomously, what requires human approval, and what remains human-only</div>
              </div>
              <div className="p-5 bg-white space-y-3">
                {/* Visual bar */}
                <div className="flex h-8 rounded-full overflow-hidden border border-gray-200 mb-4">
                  {om.governance.map((g, gi) => {
                    const c = govColors[g.color]
                    return (
                      <div key={gi} className={`flex items-center justify-center text-white text-xs font-bold transition-all ${c.bar}`} style={{ width: `${g.pct}%` }}>
                        {g.pct >= 15 ? `${g.pct}%` : ''}
                      </div>
                    )
                  })}
                </div>
                <div className="grid grid-cols-3 gap-4">
                  {om.governance.map((g, gi) => {
                    const c = govColors[g.color]
                    return (
                      <div key={gi} className={`rounded-xl border p-4 ${c.bg} ${c.border}`}>
                        <div className="flex items-center gap-2 mb-2">
                          <span className={`w-6 h-6 rounded-full text-white text-xs font-bold flex items-center justify-center ${c.badge}`}>{g.pct}%</span>
                          <span className={`font-bold text-sm ${c.text}`}>{g.tier}</span>
                        </div>
                        <p className="text-xs text-gray-600 mb-2">{g.description}</p>
                        <ul className="space-y-1">
                          {g.examples.map((ex, ei) => (
                            <li key={ei} className="text-[11px] text-gray-700 flex items-start gap-1.5">
                              <span className={`mt-0.5 shrink-0 ${g.color === 'green' ? 'text-green-500' : g.color === 'emerald' ? 'text-emerald-500' : 'text-sky-500'}`}>•</span>{ex}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )
                  })}
                </div>
              </div>
            </div>

            {/* ── Ceremony Changes ── */}
            <div className="rounded-2xl border border-gray-200 overflow-hidden">
              <div className="bg-blue-900 px-5 py-4">
                <div className="font-semibold text-white text-lg tracking-tight">Ceremony &amp; Ways of Working Changes</div>
                <div className="text-blue-100 text-xs mt-1">How team rituals and cadences transform at this maturity level</div>
              </div>
              <div className="divide-y divide-gray-100">
                <div className="grid grid-cols-12 gap-0 bg-gray-50 border-b border-gray-200">
                  {['Ceremony / Ritual', 'Before', 'After', 'What Changes'].map((h, i) => (
                    <div key={i} className={`px-4 py-2.5 text-[10px] font-bold text-gray-500 uppercase tracking-wide ${i === 0 ? 'col-span-3' : i === 1 ? 'col-span-2 text-center' : i === 2 ? 'col-span-2 text-center' : 'col-span-5'}`}>{h}</div>
                  ))}
                </div>
                {om.ceremonies.map((c, ci) => (
                  <div key={ci} className={`grid grid-cols-12 gap-0 ${ci % 2 === 0 ? 'bg-white' : 'bg-gray-50/40'}`}>
                    <div className="col-span-3 px-4 py-3 font-semibold text-gray-800 text-sm border-r border-gray-100">{c.name}</div>
                    <div className="col-span-2 px-4 py-3 text-center text-xs text-sky-700 font-mono border-r border-gray-100">{c.from}</div>
                    <div className="col-span-2 px-4 py-3 text-center text-xs text-green-700 font-bold font-mono border-r border-gray-100">{c.to}</div>
                    <div className="col-span-5 px-4 py-3 text-xs text-gray-600">{c.change}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* ── Agent Monitoring Framework (Option B & C only) ── */}
            {om.agentMonitoring && (
              <div className="space-y-5">
                <div className="rounded-2xl border-2 border-slate-700 overflow-hidden">
                  <div className="bg-slate-900 px-5 py-4">
                    <div className="font-bold text-white text-base">Agent Monitoring & Observability Framework</div>
                    <div className="text-slate-300 text-xs mt-0.5">How to monitor agent performance, detect drift, measure accuracy, and govern cost</div>
                  </div>

                  {/* Metrics table */}
                  <div className="bg-white">
                    <div className="grid grid-cols-12 gap-0 bg-slate-800 border-b border-slate-600">
                      {['Metric', 'Description', 'Target', 'Alert Threshold', 'Owner', 'Why It Matters'].map((h, i) => (
                        <div key={i} className={`px-3 py-2.5 text-[10px] font-bold text-slate-300 uppercase tracking-wide ${i === 0 ? 'col-span-2' : i === 1 ? 'col-span-3' : i === 2 ? 'col-span-1 text-center' : i === 3 ? 'col-span-1 text-center' : i === 4 ? 'col-span-2' : 'col-span-3'}`}>{h}</div>
                      ))}
                    </div>
                    <div className="divide-y divide-gray-100">
                      {om.agentMonitoring.metrics.map((m, mi) => (
                        <div key={mi} className={`grid grid-cols-12 gap-0 ${mi % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}`}>
                          <div className="col-span-2 px-3 py-3 border-r border-gray-100">
                            <span className="bg-slate-800 text-slate-100 text-[10px] font-bold px-2 py-0.5 rounded-md">{m.metric}</span>
                          </div>
                          <div className="col-span-3 px-3 py-3 text-xs text-gray-600 border-r border-gray-100">{m.desc}</div>
                          <div className="col-span-1 px-3 py-3 text-center border-r border-gray-100">
                            <span className="text-[11px] font-bold text-green-700 bg-green-50 px-1.5 py-0.5 rounded">{m.target}</span>
                          </div>
                          <div className="col-span-1 px-3 py-3 text-center border-r border-gray-100">
                            <span className="text-[11px] font-bold text-sky-700 bg-sky-50 px-1.5 py-0.5 rounded">{m.alert}</span>
                          </div>
                          <div className="col-span-2 px-3 py-3 text-xs text-gray-500 border-r border-gray-100">{m.owner}</div>
                          <div className="col-span-3 px-3 py-3 text-xs text-gray-600 italic">{m.why}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Drift Detection */}
                <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-start gap-3">
                  <span className="text-2xl shrink-0">🔎</span>
                  <div>
                    <div className="font-bold text-emerald-800 text-sm mb-1">Prompt Drift & Model Update Detection</div>
                    <p className="text-xs text-emerald-900">{om.agentMonitoring.driftDetection}</p>
                  </div>
                </div>

                {/* Cost breakdown */}
                <div className="rounded-2xl border border-gray-200 overflow-hidden">
                  <div className="bg-emerald-900 px-5 py-4 flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-white text-lg tracking-tight">Agent Operating Cost — {scenario?.label}</div>
                      <div className="text-emerald-100 text-xs mt-1">Monthly LLM + infrastructure + observability spend for the full agent fleet</div>
                    </div>
                    <div className="text-right">
                      <div className="text-[10px] text-green-300 uppercase font-bold">Estimated Monthly</div>
                      <div className="text-xl font-bold text-white">{om.agentMonitoring.costs.estimate}</div>
                    </div>
                  </div>
                  <div className="p-5 bg-white">
                    <div className="grid grid-cols-2 gap-5">
                      {/* Breakdown */}
                      <div>
                        <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">Cost Breakdown</div>
                        <div className="space-y-2">
                          {om.agentMonitoring.costs.breakdown.map((b, bi) => (
                            <div key={bi} className="space-y-1">
                              <div className="flex justify-between text-xs">
                                <span className="font-semibold text-gray-700">{b.item}</span>
                                <span className="font-bold text-gray-900">{b.monthly}</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <div className="flex-1 bg-gray-100 rounded-full h-2">
                                  <div className="h-2 rounded-full bg-emerald-500 transition-all" style={{ width: `${b.pct}%` }}></div>
                                </div>
                                <span className="text-[10px] text-gray-400 w-8 text-right">{b.pct}%</span>
                              </div>
                              <div className="text-[10px] text-gray-400">{b.note}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                      {/* Optimisations */}
                      <div>
                        <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">Cost Optimisation Levers</div>
                        <div className="space-y-2">
                          {om.agentMonitoring.costs.optimisations.map((opt, oi) => (
                            <div key={oi} className="flex items-start gap-2 bg-green-50 border border-green-200 rounded-lg p-2.5">
                              <span className="text-green-600 shrink-0 mt-0.5 text-sm">💡</span>
                              <span className="text-xs text-gray-700">{opt}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        )
      })()}

      {/* ── Cost Model & ROI Calculator ── */}
      {activeSection === 'costmodel' && (
        <CostModelEditor projectId={project?.id} addNotification={addNotification} />
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

          {/* One-stop document banner — covers Tools, Org Change, DevSecOps, AI Ops, Product-Centric */}
          <div className="rounded-2xl border-2 border-emerald-300 bg-gradient-to-r from-emerald-50 to-teal-50 p-5">
            <div className="flex items-start gap-3">
              <div className="text-3xl shrink-0">🗂️</div>
              <div className="flex-1">
                <div className="font-bold text-emerald-900 text-base">This Playbook is the One-Stop Document for {activeStep ? `L${activeStep.level} — ${activeStep.label}` : scenario?.label}</div>
                <div className="text-xs text-emerald-800 mt-1 leading-relaxed">
                  Everything you need to execute {activeStep ? `L${activeStep.level} (${activeStep.label})` : scenario?.label}{tsPlatformDetail ? ` on ${tsPlatformDetail.name}` : ''} is consolidated below — phase-by-phase plan with detailed <strong>how-to steps</strong>, plus inline coverage of every change captured in the dedicated tabs. Use this as your single source of truth; jump to a specific tab only when you need to drill deeper.
                </div>
                <div className="mt-3 flex flex-wrap gap-2 text-[11px]">
                  <a href="#pb-tools"     className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">🧰 Tools & Tech ({pb.toolsChanges?.length || 0})</a>
                  <a href="#pb-org"       className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">🔄 Org & Change Mgmt ({pb.orgChanges?.length || 0})</a>
                  <a href="#pb-devsecops" className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">🔒 DevSecOps ({bc.devSecOps?.length || 0})</a>
                  <a href="#pb-aiops"     className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">🤖 AI Ops ({bc.aiOps?.length || 0})</a>
                  <a href="#pb-product"   className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">🎯 Product-Centric ({pb.productCentricChanges?.length || 0})</a>
                  <a href="#pb-raci"      className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">👥 RACI</a>
                  <a href="#pb-risks"     className="bg-white border border-emerald-200 text-emerald-800 px-3 py-1 rounded-full hover:bg-emerald-100">⚠ Risks</a>
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
              <h3 className="font-bold text-gray-800">Phase-by-Phase Implementation Plan</h3>
              <p className="text-xs text-gray-500">Expand each phase to see and edit specific actions, owners, and expected outcomes</p>
            </div>
            <div className="card-body space-y-3">
              {pb.sprintPlan.map((sp, idx) => {
                const isOpen = openSprint === idx
                const updateSprintActions = (newActions) => {
                  if (tsCfg && editedTsSprintPlan) {
                    setEditedTsSprintPlan(prev => prev.map((s, i) => i === idx ? { ...s, actions: newActions } : s))
                  } else {
                    setEditedPlaybooks(prev => {
                      const next = JSON.parse(JSON.stringify(prev))
                      next[activeScenario].sprintPlan[idx].actions = newActions
                      return next
                    })
                  }
                }
                return (
                  <div key={idx} className="border border-gray-200 rounded-xl overflow-hidden">
                    <button onClick={() => setOpenSprint(isOpen ? null : idx)}
                      className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50 text-left">
                      <div className="w-8 h-8 bg-indigo-600 text-white rounded-lg flex items-center justify-center font-bold text-sm shrink-0">{idx + 1}</div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-800">{sp.sprint} — {sp.label}</div>
                        <div className="text-xs text-gray-500">{sp.actions.length} actions · click to expand · hover to edit</div>
                      </div>
                      <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
                    </button>
                    {isOpen && (
                      <div className="border-t border-gray-100 px-5 pb-5 slide-down">
                        <div className="mt-4">
                          <EditableActionList items={sp.actions} onChange={updateSprintActions} />
                        </div>
                        {sp.outcomes && sp.outcomes.length > 0 && (
                        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                          <div className="text-xs font-semibold text-green-800 mb-1">Phase Outcomes:</div>
                          <ul className="space-y-1">
                            {sp.outcomes.map((o, oi) => (
                              <li key={oi} className="flex items-center gap-2 text-xs text-green-700">
                                <span className="text-green-500">✓</span> {o}
                              </li>
                            ))}
                          </ul>
                        </div>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          {/* ── Inline coverage: Tools & Technology ─────────────────────── */}
          <CoverageSection
            id="pb-tools" title="Tools & Technology Changes" icon="🧰"
            tone="blue" tabLabel="Tools" tabId="tools"
            description="The detailed how-to for every tool / agent deployment that supports the sprint plan above. Each entry shows current state, the agent change being made, step-by-step deployment, working configuration example, and success criteria."
            items={pb.toolsChanges || []}
            renderItem={(c) => ({
              title: c.title, icon: c.icon, meta: [c.category, c.phase].filter(Boolean).join(' · '),
              owner: c.owner, timeline: c.timeline, effort: c.effort,
              fields: [
                { label: 'Current state', value: c.current },
                { label: 'Target change', value: c.change },
                { label: 'How to execute', value: c.how, mono: true },
                { label: 'Working example', value: c.example, code: true },
                { label: 'Tools used', value: (c.tools || []).join(', ') },
                { label: 'Success criteria', value: c.successCriteria },
              ],
            })}
          />

          {/* ── Inline coverage: Org & Change Management ──────────────── */}
          <CoverageSection
            id="pb-org" title="Org & Change Management" icon="🔄"
            tone="purple" tabLabel="Org Change" tabId="org"
            description="Role restructuring, agent operations setup, governance, and KPI redesign that must happen alongside tool deployment. Each entry shows what changes, how to do it, a worked example, and success criteria."
            items={pb.orgChanges || []}
            renderItem={(c) => ({
              title: c.title, icon: c.icon, meta: '',
              owner: c.who, timeline: c.timeline, effort: c.effort,
              fields: [
                { label: 'What changes',    value: c.what },
                { label: 'How to execute',  value: c.how, mono: true },
                { label: 'Worked example',  value: c.example, code: true },
                { label: 'Success criteria',value: c.successCriteria },
              ],
            })}
          />

          {/* ── Inline coverage: DevSecOps ─────────────────────────────── */}
          <CoverageSection
            id="pb-devsecops" title="DevSecOps Pipeline Changes" icon="🔒"
            tone="red" tabLabel="DevSecOps" tabId="devsecops"
            description="AI-powered security gates at each pipeline stage. Each entry includes current vs target state, working CI/CD config, and measurable outcomes."
            items={(bc.devSecOps || []).filter(c => typeof c !== 'string')}
            renderItem={(c) => ({
              title: c.title, icon: c.icon, meta: [c.pipelineStage, c.priority].filter(Boolean).join(' · '),
              owner: '', timeline: '', effort: '',
              fields: [
                { label: 'Current state',  value: c.current },
                { label: 'Target change',  value: c.change },
                { label: 'How to execute', value: c.how, mono: true },
                { label: 'Working example',value: c.example, code: true },
                { label: 'Tools used',     value: (c.tools || []).join(', ') },
                { label: 'Expected metrics impact', value: c.metrics },
              ],
            })}
          />

          {/* ── Inline coverage: AI Ops / Production Support ──────────── */}
          <CoverageSection
            id="pb-aiops" title="AI Ops / Production Support" icon="🤖"
            tone="indigo" tabLabel="AI Ops" tabId="aiops"
            description="How to set up AI-driven production observability, incident response, and capacity management. Each entry shows current vs target, step-by-step configuration, and outcomes."
            items={(bc.aiOps || []).filter(c => typeof c !== 'string')}
            renderItem={(c) => ({
              title: c.title, icon: c.icon, meta: [c.pipelineStage, c.priority].filter(Boolean).join(' · '),
              owner: '', timeline: '', effort: '',
              fields: [
                { label: 'Current state',  value: c.current },
                { label: 'Target change',  value: c.change },
                { label: 'How to execute', value: c.how, mono: true },
                { label: 'Working example',value: c.example, code: true },
                { label: 'Tools used',     value: (c.tools || []).join(', ') },
                { label: 'Expected metrics impact', value: c.metrics },
              ],
            })}
          />

          {/* ── Inline coverage: Product-Centric WoW ──────────────────── */}
          {pb.productCentricChanges && pb.productCentricChanges.length > 0 && (
            <div id="pb-product" className="rounded-2xl border border-gray-200 bg-white overflow-hidden">
              <div className="bg-teal-500 px-5 py-4 flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white text-base tracking-tight flex items-center gap-2">🎯 Product-Centric Ways of Working</div>
                  <div className="text-teal-100 text-xs mt-1">Organisational shifts to make the product team the unit of value — not the project. Also visible on the Product-Centric tab.</div>
                </div>
                <button onClick={() => setSection('product')} className="text-[11px] bg-white/10 hover:bg-white/20 text-white px-3 py-1 rounded-md">Open full tab →</button>
              </div>
              <ul className="p-5 space-y-2">
                {pb.productCentricChanges.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-teal-500 mt-1">●</span>
                    <span>{c}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* RACI */}
          <EditableRaciTable raci={pb.raci} onChange={(newRaci) => {
            setEditedPlaybooks(prev => {
              const next = JSON.parse(JSON.stringify(prev))
              next[activeScenario].raci = newRaci
              return next
            })
          }} />

          <EditableRiskRegister risks={pb.risks} onChange={(newRisks) => {
            setEditedPlaybooks(prev => {
              const next = JSON.parse(JSON.stringify(prev))
              next[activeScenario].risks = newRisks
              return next
            })
          }} />

          {/* Contextualise CTA */}
          <div className="bg-indigo-50 border-2 border-indigo-200 rounded-2xl p-5 text-center">
            <div className="text-2xl mb-2">🎯</div>
            <div className="font-bold text-indigo-800 text-lg mb-1">Make this playbook 90%+ accurate</div>
            <p className="text-sm text-indigo-700 mb-4">
              The playbook above uses industry defaults. Provide your team context, technology stack, compliance requirements, and supporting documents to generate a personalised version specific to your team.
            </p>
            <Link to="/playbook-context" className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-8 py-3 rounded-xl text-sm shadow-md">
              🚀 Contextualise My Playbook →
            </Link>
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
      {/* ── Roadmap ── */}
      {activeSection === 'roadmap' && (() => {
        const rm = editedRoadmap[activeScenario]
        if (!rm) return null
        const lanes = Object.keys(LANE_STYLE)
        const openPhaseIdx = rmPhaseIdx
        const setOpenPhaseIdx = setRmPhaseIdx
        const activeLane = rmLane
        const setActiveLane = setRmLane
        return (
          <div className="space-y-4">
            {/* Header */}
            <div className="bg-gradient-to-r from-sky-500 to-emerald-500 rounded-2xl p-5 text-white">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h3 className="font-bold text-xl mb-1">
                    Transformation Roadmap — {tsCfg && tsSteps[tsStepIdx] ? `L${tsSteps[tsStepIdx].level} (${(tsCfg.platform || '').replace('_', ' ')})` : scenario?.label}
                  </h3>
                  <p className="text-sm opacity-90">{rm.humanModel}</p>
                  <p className="text-xs opacity-75 mt-1">
                    {tsCfg ? 'Actions to reach the selected target state level' : 'All improvement actions to achieve this option'} — across People, Tools, DevSecOps, AIOps and Measurement
                  </p>
                </div>
                <div className="flex gap-3 flex-wrap">
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Duration</div>
                    <div className="font-bold">{rm.duration}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Phases</div>
                    <div className="font-bold">{rm.phases.length}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Lane filter pills */}
            <div className="flex gap-2 flex-wrap">
              <button onClick={() => setActiveLane('all')}
                className={`px-3 py-1 rounded-full text-xs font-semibold border transition-all ${activeLane === 'all' ? 'bg-gray-700 text-white border-gray-700' : 'bg-white text-gray-600 border-gray-300 hover:border-gray-500'}`}>
                All Lanes
              </button>
              {lanes.map(l => {
                const s = LANE_STYLE[l]
                return (
                  <button key={l} onClick={() => setActiveLane(activeLane === l ? 'all' : l)}
                    className={`px-3 py-1 rounded-full text-xs font-semibold border transition-all ${activeLane === l ? `${s.badge} text-white border-transparent` : `bg-white ${s.text} ${s.border}`}`}>
                    {s.label}
                  </button>
                )
              })}
            </div>

            {/* Phase strip */}
            <div className="grid gap-1" style={{ gridTemplateColumns: `repeat(${rm.phases.length}, 1fr)` }}>
              {rm.phases.map((ph, i) => {
                const clr = PHASE_COLOR[ph.color] || 'bg-gray-500'
                const isOpen = openPhaseIdx === i
                return (
                  <button key={i} onClick={() => setOpenPhaseIdx(isOpen ? null : i)}
                    className={`rounded-lg p-2 text-left border-2 transition-all ${isOpen ? 'border-emerald-400 shadow-md' : 'border-gray-200 hover:border-emerald-300'} bg-white`}>
                    <div className={`${clr} text-white text-xs font-bold px-2 py-0.5 rounded-full mb-1.5 inline-block`}>{ph.range}</div>
                    <div className="font-semibold text-gray-800 text-xs leading-tight">{ph.name}</div>
                    <div className="flex gap-0.5 mt-1.5 flex-wrap">
                      {lanes.filter(l => ph[l]?.length > 0).map(l => (
                        <span key={l} className={`w-2 h-2 rounded-full ${LANE_STYLE[l].dot}`} title={LANE_STYLE[l].label} />
                      ))}
                    </div>
                  </button>
                )
              })}
            </div>

            {/* Expanded phase panel */}
            {openPhaseIdx !== null && (() => {
              const ph = rm.phases[openPhaseIdx]
              const visibleLanes = activeLane === 'all' ? lanes : [activeLane]
              return (
                <div className="border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
                  <div className={`${PHASE_COLOR[ph.color] || 'bg-gray-600'} px-5 py-3 flex items-center justify-between`}>
                    <div>
                      <span className="font-bold text-white text-base">{ph.range} — {ph.name}</span>
                      <span className="ml-3 text-white/70 text-xs">
                        {lanes.reduce((n, l) => n + (ph[l]?.length || 0), 0)} activities across {lanes.filter(l => ph[l]?.length > 0).length} lanes
                      </span>
                    </div>
                    <button onClick={() => setOpenPhaseIdx(null)} className="text-white/70 hover:text-white text-sm">✕ Close</button>
                  </div>
                  <div className="bg-white divide-y divide-gray-100">
                    {visibleLanes.map(lane => {
                      const items = ph[lane] || []
                      if (items.length === 0 && activeLane !== 'all' && activeLane !== lane) return null
                      const ls = LANE_STYLE[lane]
                      const updateLaneActions = (newItems) => {
                        setEditedRoadmap(prev => {
                          const next = JSON.parse(JSON.stringify(prev))
                          next[activeScenario].phases[openPhaseIdx][lane] = newItems
                          return next
                        })
                      }
                      return (
                        <div key={lane} className={`px-5 py-4 ${ls.bg}`}>
                          <div className="flex items-center gap-2 mb-3">
                            <span className={`${ls.badge} text-white text-xs font-bold px-3 py-0.5 rounded-full`}>{ls.label}</span>
                            <span className="text-xs text-gray-500">{items.length} actions · hover to edit</span>
                          </div>
                          <EditableActionList items={items} onChange={updateLaneActions} tone={lane === 'org' ? 'blue' : lane === 'tools' ? 'purple' : lane === 'devsecops' ? 'red' : lane === 'aiops' ? 'indigo' : 'teal'} />
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })()}

            {/* Full Gantt table */}
            <div className="card overflow-hidden">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Swim-Lane Roadmap — All Phases</h3>
                <p className="text-xs text-gray-500">Click a phase card above to drill into its activities · {activeLane === 'all' ? 'All swim lanes shown' : `Lane filter: ${LANE_STYLE[activeLane]?.label}`}</p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-xs border-collapse min-w-max">
                  <thead>
                    <tr>
                      <th className="text-left px-3 py-2 bg-gray-50 border border-gray-200 font-semibold text-gray-600 w-36 sticky left-0 z-10">Lane</th>
                      {rm.phases.map((ph, i) => (
                        <th key={i} className="px-3 py-2 bg-gray-50 border border-gray-200 text-center" style={{ minWidth: '140px' }}>
                          <div className={`${PHASE_COLOR[ph.color] || 'bg-gray-500'} text-white px-2 py-0.5 rounded-full font-bold inline-block mb-0.5`}>{ph.range}</div>
                          <div className="font-semibold text-gray-700 text-xs">{ph.name}</div>
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {(activeLane === 'all' ? lanes : [activeLane]).map(lane => {
                      const ls = LANE_STYLE[lane]
                      if (!rm.phases.some(ph => (ph[lane] || []).length > 0)) return null
                      return (
                        <tr key={lane} className="align-top">
                          <td className={`px-3 py-3 border border-gray-200 font-semibold ${ls.text} ${ls.bg} sticky left-0`}>{ls.label}</td>
                          {rm.phases.map((ph, pi) => {
                            const items = ph[lane] || []
                            return (
                              <td key={pi} className={`px-2 py-2 border border-gray-200 ${ls.bg} align-top cursor-pointer hover:ring-2 hover:ring-inset hover:ring-indigo-300`}
                                onClick={() => { setRmPhaseIdx(pi); setRmLane(lane) }} title="Click to edit actions">
                                {items.length === 0 ? (
                                  <div className="text-gray-300 text-center py-2">—</div>
                                ) : (
                                  <ul className="space-y-1">
                                    {items.map((item, ii) => (
                                      <li key={ii} className={`flex items-start gap-1.5 bg-white border ${ls.border} rounded px-2 py-1.5`}>
                                        <span className={`${ls.dot} w-1.5 h-1.5 rounded-full shrink-0 mt-1`} />
                                        <span className="text-gray-700 leading-snug">{item}</span>
                                      </li>
                                    ))}
                                  </ul>
                                )}
                              </td>
                            )
                          })}
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )
      })()}

      {/* ── Action Tracker ── */}
      {activeSection === 'tracker' && (() => {
        const STATUS_META = {
          not_started: { label: 'Not Started', bg: 'bg-gray-100',   text: 'text-gray-600',   dot: 'bg-gray-400'   },
          in_progress:  { label: 'In Progress', bg: 'bg-blue-100',   text: 'text-blue-700',   dot: 'bg-blue-500'   },
          complete:     { label: 'Complete',    bg: 'bg-green-100',  text: 'text-green-700',  dot: 'bg-green-500'  },
          blocked:      { label: 'Blocked',     bg: 'bg-sky-100',    text: 'text-sky-700',    dot: 'bg-sky-500'    },
          deferred:     { label: 'Deferred',    bg: 'bg-emerald-100',  text: 'text-emerald-700',  dot: 'bg-emerald-500'  },
        }
        const allActions = getFlatActions(activeScenario)
        const rm = TRANSFORMATION_ROADMAP[activeScenario]

        // Compute stats
        const totals = allActions.length
        const byStatus = Object.keys(STATUS_META).reduce((a, k) => {
          a[k] = allActions.filter(r => (trackerData[r.id]?.status || 'not_started') === k).length
          return a
        }, {})
        const completePct = totals > 0 ? Math.round((byStatus.complete / totals) * 100) : 0
        const inProgressPct = totals > 0 ? Math.round((byStatus.in_progress / totals) * 100) : 0

        // Filter
        const filtered = allActions.filter(r => {
          const td = trackerData[r.id] || {}
          const st = td.status || 'not_started'
          if (trackerFilter.lane !== 'all' && r.lane !== trackerFilter.lane) return false
          if (trackerFilter.status !== 'all' && st !== trackerFilter.status) return false
          if (trackerFilter.phase !== 'all' && r.phaseIdx !== parseInt(trackerFilter.phase)) return false
          return true
        })

        // Sort
        const sorted = [...filtered].sort((a, b) => {
          const td_a = trackerData[a.id] || {}, td_b = trackerData[b.id] || {}
          let va, vb
          if (trackerSort.col === 'phase')      { va = a.phaseIdx;                         vb = b.phaseIdx }
          else if (trackerSort.col === 'lane')  { va = a.lane;                              vb = b.lane }
          else if (trackerSort.col === 'status'){ va = td_a.status || 'not_started';        vb = td_b.status || 'not_started' }
          else if (trackerSort.col === 'owner') { va = (td_a.owner || '').toLowerCase();    vb = (td_b.owner || '').toLowerCase() }
          else if (trackerSort.col === 'date')  { va = td_a.targetDate || 'zzzz';           vb = td_b.targetDate || 'zzzz' }
          else                                  { va = a.action.toLowerCase();              vb = b.action.toLowerCase() }
          if (va < vb) return trackerSort.dir === 'asc' ? -1 : 1
          if (va > vb) return trackerSort.dir === 'asc' ? 1 : -1
          return 0
        })

        const toggleSort = (col) => setTrackerSort(s => ({ col, dir: s.col === col && s.dir === 'asc' ? 'desc' : 'asc' }))
        const sortIcon = (col) => trackerSort.col === col ? (trackerSort.dir === 'asc' ? ' ↑' : ' ↓') : ''

        return (
          <div className="space-y-4">
            {/* Header */}
            <div className="bg-gradient-to-r from-teal-600 to-cyan-700 rounded-2xl p-5 text-white">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h3 className="font-bold text-xl mb-1">Action Tracker — {scenario?.label}</h3>
                  <p className="text-sm opacity-90">{rm?.humanModel} · {rm?.duration}</p>
                  <p className="text-xs opacity-75 mt-1">Track every transformation action to closure. Updates saved automatically.</p>
                </div>
                <div className="flex gap-3 flex-wrap">
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Total Actions</div>
                    <div className="font-bold text-lg">{totals}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Complete</div>
                    <div className="font-bold text-lg text-green-300">{completePct}%</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">In Progress</div>
                    <div className="font-bold text-lg text-blue-300">{byStatus.in_progress}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Blocked</div>
                    <div className="font-bold text-lg text-sky-300">{byStatus.blocked}</div>
                  </div>
                </div>
              </div>
              {/* Progress bar */}
              <div className="mt-4">
                <div className="flex justify-between text-xs opacity-75 mb-1">
                  <span>Overall Progress</span>
                  <span>{byStatus.complete} of {totals} complete</span>
                </div>
                <div className="h-3 bg-white/20 rounded-full overflow-hidden flex">
                  <div className="bg-green-400 h-full transition-all" style={{ width: `${completePct}%` }} />
                  <div className="bg-blue-400 h-full transition-all" style={{ width: `${inProgressPct}%` }} />
                </div>
                <div className="flex gap-4 mt-1.5 text-xs opacity-70">
                  <span className="flex items-center gap-1"><span className="w-2 h-2 bg-green-400 rounded-full inline-block" /> Complete</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 bg-blue-400 rounded-full inline-block" /> In Progress</span>
                  <span className="flex items-center gap-1"><span className="w-2 h-2 bg-white/40 rounded-full inline-block" /> Not Started</span>
                </div>
              </div>
            </div>

            {/* Stats by lane */}
            <div className="grid grid-cols-5 gap-2">
              {Object.entries(LANE_STYLE).map(([lane, ls]) => {
                const laneActions = allActions.filter(r => r.lane === lane)
                const done = laneActions.filter(r => (trackerData[r.id]?.status || 'not_started') === 'complete').length
                const pct = laneActions.length > 0 ? Math.round((done / laneActions.length) * 100) : 0
                return (
                  <div key={lane} className={`${ls.bg} border ${ls.border} rounded-xl p-3 cursor-pointer transition-all ${trackerFilter.lane === lane ? 'ring-2 ring-offset-1 ' + ls.border : ''}`}
                    onClick={() => setTrackerFilter(f => ({ ...f, lane: f.lane === lane ? 'all' : lane }))}>
                    <div className="text-xs font-semibold text-gray-700 mb-1">{ls.label}</div>
                    <div className="flex items-end gap-2">
                      <div className={`text-lg font-bold ${ls.text}`}>{pct}%</div>
                      <div className="text-xs text-gray-500 mb-0.5">{done}/{laneActions.length}</div>
                    </div>
                    <div className="h-1.5 bg-gray-200 rounded-full mt-1 overflow-hidden">
                      <div className={`h-full ${ls.badge} rounded-full`} style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Filters */}
            <div className="bg-white border border-gray-200 rounded-xl p-3 flex flex-wrap gap-3 items-center">
              <span className="text-xs font-semibold text-gray-600">Filter:</span>
              <select value={trackerFilter.phase} onChange={e => setTrackerFilter(f => ({ ...f, phase: e.target.value }))}
                className="text-xs border border-gray-200 rounded-lg px-2 py-1.5 bg-white">
                <option value="all">All Phases</option>
                {rm?.phases.map((ph, i) => <option key={i} value={i}>{ph.range} — {ph.name}</option>)}
              </select>
              <select value={trackerFilter.lane} onChange={e => setTrackerFilter(f => ({ ...f, lane: e.target.value }))}
                className="text-xs border border-gray-200 rounded-lg px-2 py-1.5 bg-white">
                <option value="all">All Lanes</option>
                {Object.entries(LANE_STYLE).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
              </select>
              <select value={trackerFilter.status} onChange={e => setTrackerFilter(f => ({ ...f, status: e.target.value }))}
                className="text-xs border border-gray-200 rounded-lg px-2 py-1.5 bg-white">
                <option value="all">All Statuses</option>
                {Object.entries(STATUS_META).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
              </select>
              <span className="text-xs text-gray-400 ml-auto">{filtered.length} of {totals} actions</span>
              <button onClick={() => { if(window.confirm('Reset all tracker data for this option?')) saveTracker({}) }}
                className="text-xs text-sky-500 hover:text-sky-700 border border-sky-200 px-2 py-1 rounded-lg">Reset All</button>
            </div>

            {/* Action table */}
            <div className="card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-xs border-collapse">
                  <thead className="bg-gray-50 sticky top-0">
                    <tr>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 w-6">#</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 cursor-pointer hover:bg-gray-100 min-w-72"
                        onClick={() => toggleSort('action')}>Action{sortIcon('action')}</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 cursor-pointer hover:bg-gray-100 whitespace-nowrap"
                        onClick={() => toggleSort('lane')}>Track{sortIcon('lane')}</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 cursor-pointer hover:bg-gray-100 whitespace-nowrap"
                        onClick={() => toggleSort('phase')}>Phase / Week{sortIcon('phase')}</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 cursor-pointer hover:bg-gray-100 whitespace-nowrap"
                        onClick={() => toggleSort('date')}>Target Date{sortIcon('date')}</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 cursor-pointer hover:bg-gray-100"
                        onClick={() => toggleSort('status')}>Status{sortIcon('status')}</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 cursor-pointer hover:bg-gray-100 whitespace-nowrap"
                        onClick={() => toggleSort('owner')}>Owner{sortIcon('owner')}</th>
                      <th className="text-left px-3 py-2.5 border-b border-gray-200 font-semibold text-gray-600 min-w-48">Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sorted.map((row, i) => {
                      const td = trackerData[row.id] || {}
                      const status = td.status || 'not_started'
                      const sm = STATUS_META[status]
                      const ls = LANE_STYLE[row.lane]
                      const phClr = PHASE_COLOR[row.phaseColor] || 'bg-gray-500'
                      const isEditing = editingAction === row.id
                      return (
                        <tr key={row.id} className={`border-b border-gray-100 transition-colors ${status === 'complete' ? 'bg-green-50/40' : status === 'blocked' ? 'bg-sky-50/40' : i % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}`}>
                          <td className="px-3 py-2.5 text-gray-400 font-mono">{i + 1}</td>

                          {/* Action text */}
                          <td className="px-3 py-2.5">
                            <span className={`text-sm text-gray-800 ${status === 'complete' ? 'line-through text-gray-400' : ''}`}>{row.action}</span>
                          </td>

                          {/* Lane */}
                          <td className="px-3 py-2.5 whitespace-nowrap">
                            <span className={`${ls.badge} text-white text-xs px-2 py-0.5 rounded-full font-medium`}>{ls.label.replace(/^.+ /, '')}</span>
                          </td>

                          {/* Phase/Week */}
                          <td className="px-3 py-2.5 whitespace-nowrap">
                            <div className={`${phClr} text-white text-xs px-2 py-0.5 rounded-full font-bold inline-block mb-0.5`}>{row.phaseRange}</div>
                            <div className="text-xs text-gray-500">{row.phaseName}</div>
                          </td>

                          {/* Target Date */}
                          <td className="px-3 py-2.5">
                            <input type="date" value={td.targetDate || ''} onChange={e => updateAction(row.id, 'targetDate', e.target.value)}
                              className="text-xs border border-gray-200 rounded-lg px-2 py-1 bg-white w-32 focus:border-teal-400 focus:outline-none" />
                          </td>

                          {/* Status */}
                          <td className="px-3 py-2.5">
                            <select value={status} onChange={e => updateAction(row.id, 'status', e.target.value)}
                              className={`text-xs font-semibold border rounded-lg px-2 py-1 cursor-pointer focus:outline-none ${sm.bg} ${sm.text} border-transparent`}>
                              {Object.entries(STATUS_META).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
                            </select>
                          </td>

                          {/* Owner */}
                          <td className="px-3 py-2.5">
                            <input type="text" value={td.owner || ''} onChange={e => updateAction(row.id, 'owner', e.target.value)}
                              placeholder="Assign owner…"
                              className="text-xs border border-gray-200 rounded-lg px-2 py-1 bg-white w-32 focus:border-teal-400 focus:outline-none placeholder-gray-300" />
                          </td>

                          {/* Notes */}
                          <td className="px-3 py-2.5">
                            {isEditing ? (
                              <textarea value={td.notes || ''} onChange={e => updateAction(row.id, 'notes', e.target.value)}
                                onBlur={() => setEditingAction(null)} autoFocus rows={2}
                                className="text-xs border border-teal-300 rounded-lg px-2 py-1 w-full focus:outline-none resize-none"
                                placeholder="Add notes…" />
                            ) : (
                              <div className="flex items-start gap-1 group cursor-pointer min-h-6"
                                onClick={() => setEditingAction(row.id)}>
                                <span className="text-xs text-gray-600 flex-1">{td.notes || <span className="text-gray-300 italic">Add notes…</span>}</span>
                                <span className="text-gray-300 group-hover:text-gray-500 text-xs opacity-0 group-hover:opacity-100 shrink-0">✏</span>
                              </div>
                            )}
                          </td>
                        </tr>
                      )
                    })}
                    {sorted.length === 0 && (
                      <tr><td colSpan={8} className="text-center py-8 text-gray-400">No actions match the current filters.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Export hint */}
            <div className="bg-teal-50 border border-teal-200 rounded-xl p-3 flex items-center gap-3">
              <span className="text-teal-600">💾</span>
              <span className="text-xs text-teal-700">Tracker data is saved automatically to your browser. Status, owner, target date and notes persist across sessions for each option.</span>
            </div>
          </div>
        )
      })()}

      {/* ── Team Plans ─────────────────────────────────────────────────────── */}
      {activeSection === 'teamplans' && (() => {
        const teams = getAllTeams()
        const STATUS_META_TP = {
          not_started: { label: 'Not Started', bg: 'bg-gray-100', text: 'text-gray-600', dot: 'bg-gray-400' },
          in_progress:  { label: 'In Progress', bg: 'bg-blue-100', text: 'text-blue-700', dot: 'bg-blue-500' },
          complete:     { label: 'Complete',    bg: 'bg-green-100', text: 'text-green-700', dot: 'bg-green-500' },
          blocked:      { label: 'Blocked',     bg: 'bg-sky-100',  text: 'text-sky-700',  dot: 'bg-sky-500' },
          deferred:     { label: 'Deferred',    bg: 'bg-emerald-100',text: 'text-emerald-700',dot: 'bg-emerald-500' },
        }
        return (
          <div className="space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-slate-700 to-slate-900 rounded-2xl p-6 text-white">
              <div className="flex items-center justify-between flex-wrap gap-3">
                <div>
                  <h3 className="font-bold text-xl">👥 Team Plans — Assigned Options &amp; Progress</h3>
                  <p className="text-sm text-slate-300 mt-1">Assign an Option A / B / C transformation plan to each team and track their implementation progress independently.</p>
                </div>
                <button onClick={() => setAddingTeam(v => !v)}
                  className="bg-white/20 hover:bg-white/30 text-white text-sm font-bold px-4 py-2 rounded-lg transition-colors">
                  + Add Team
                </button>
              </div>
              {addingTeam && (
                <div className="mt-4 flex items-center gap-2">
                  <input value={newTeamName} onChange={e => setNewTeamName(e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && newTeamName.trim()) { saveTeamPlan(newTeamName.trim(), 'option-a'); setNewTeamName(''); setAddingTeam(false) } }}
                    placeholder="Enter team name (e.g. Team Phoenix)" className="flex-1 bg-white/10 border border-white/30 text-white placeholder-white/40 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-white/50" />
                  <button onClick={() => { if (newTeamName.trim()) { saveTeamPlan(newTeamName.trim(), 'option-a'); setNewTeamName(''); setAddingTeam(false) } }}
                    className="bg-green-500 hover:bg-green-400 text-white text-sm font-bold px-3 py-1.5 rounded-lg">Add</button>
                  <button onClick={() => { setAddingTeam(false); setNewTeamName('') }}
                    className="bg-white/10 text-white text-sm px-3 py-1.5 rounded-lg">Cancel</button>
                </div>
              )}
            </div>

            {/* Summary tiles */}
            {Object.keys(teamPlans).length > 0 && (
              <div className="grid grid-cols-3 gap-3">
                {['option-a','option-b','option-c'].map(opt => {
                  const count = Object.values(teamPlans).filter(p => p.option === opt).length
                  const m = OPTION_META[opt]
                  return (
                    <div key={opt} className={`rounded-xl border ${m.border} ${m.light} p-4 text-center`}>
                      <div className={`text-2xl font-bold ${m.text}`}>{count}</div>
                      <div className={`text-xs font-bold ${m.text} mt-0.5`}>{m.label}</div>
                      <div className="text-xs text-gray-500">{count === 1 ? 'team' : 'teams'}</div>
                    </div>
                  )
                })}
              </div>
            )}

            {/* No teams yet */}
            {teams.length === 0 && (
              <div className="card card-body text-center py-12 text-gray-400">
                <div className="text-4xl mb-3">👥</div>
                <div className="font-semibold text-gray-600">No teams found</div>
                <div className="text-sm mt-1">Add teams above, or set up your product hierarchy in the ALM Connect step.</div>
              </div>
            )}

            {/* Team cards */}
            <div className="space-y-4">
              {teams.map(team => {
                const plan = teamPlans[team.name]
                const progress = getTeamProgress(team.name)
                const isSelected = selectedTeam === team.name
                const td = teamTrackers[team.name] || {}
                const planActions = plan ? getFlatActions(plan.option) : []
                const m = plan ? OPTION_META[plan.option] : null

                return (
                  <div key={team.name} className={`rounded-2xl border-2 overflow-hidden transition-all ${plan ? `${m.border}` : 'border-gray-200'}`}>
                    {/* Card header */}
                    <div className={`px-5 py-4 flex items-center justify-between flex-wrap gap-3 ${plan ? m.light : 'bg-gray-50'}`}>
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-white text-lg ${plan ? m.badge : 'bg-gray-400'}`}>
                          {team.name.charAt(0)}
                        </div>
                        <div>
                          <div className="font-bold text-gray-900">{team.name}</div>
                          {(team.product || team.productGroup) && (
                            <div className="text-xs text-gray-500">{[team.productGroup, team.product].filter(Boolean).join(' › ')}</div>
                          )}
                        </div>
                        {plan && <span className={`text-white text-xs font-bold px-3 py-1 rounded-full ${m.badge}`}>{m.label} · {m.duration} · ROI {m.roi}</span>}
                        {!plan && <span className="bg-gray-200 text-gray-500 text-xs font-semibold px-3 py-1 rounded-full">No option selected</span>}
                      </div>
                      <div className="flex items-center gap-2 flex-wrap">
                        {/* Option selector */}
                        {['option-a','option-b','option-c'].map(opt => {
                          const om = OPTION_META[opt]
                          const active = plan?.option === opt
                          return (
                            <button key={opt} onClick={() => saveTeamPlan(team.name, opt)}
                              className={`text-xs font-bold px-3 py-1.5 rounded-lg border transition-all ${active ? `${om.badge} text-white border-transparent shadow` : `bg-white ${om.text} ${om.border} hover:${om.light}`}`}>
                              {om.label}
                            </button>
                          )
                        })}
                        <button onClick={() => setSelectedTeam(isSelected ? null : team.name)}
                          className="text-xs font-bold px-3 py-1.5 rounded-lg bg-slate-700 text-white hover:bg-slate-600 transition-colors">
                          {isSelected ? '▲ Hide' : '▼ Tracker'}
                        </button>
                        <button onClick={() => removeTeamPlan(team.name)}
                          className="text-xs text-gray-400 hover:text-sky-500 px-2 py-1.5 rounded-lg hover:bg-sky-50 transition-colors">✕</button>
                      </div>
                    </div>

                    {/* Progress bar */}
                    {progress && (
                      <div className="px-5 py-3 bg-white border-t border-gray-100">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-4">
                            <span className="text-sm font-bold text-gray-800">{progress.pct}% complete</span>
                            <span className="text-xs text-gray-500">{progress.done} / {progress.total} actions</span>
                          </div>
                          {plan && <span className="text-xs text-gray-400">Saved {new Date(plan.savedAt).toLocaleDateString()}</span>}
                        </div>
                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden mb-3">
                          <div className={`h-full rounded-full transition-all ${m.badge}`} style={{ width: `${progress.pct}%` }} />
                        </div>
                        <div className="flex gap-3 flex-wrap">
                          {Object.entries(progress.byLane).map(([lane, stat]) => {
                            const ls = LANE_STYLE[lane]
                            const pct = stat.total > 0 ? Math.round((stat.done / stat.total) * 100) : 0
                            return (
                              <div key={lane} className={`flex items-center gap-1.5 px-2 py-1 rounded-lg ${ls.bg} border ${ls.border}`}>
                                <span className="text-xs font-semibold truncate max-w-20" style={{ color: undefined }} ><span className={ls.text}>{ls.label}</span></span>
                                <span className={`text-xs font-bold ${ls.text}`}>{pct}%</span>
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    )}
                    {!progress && plan && (
                      <div className="px-5 py-3 bg-white border-t border-gray-100 text-xs text-gray-400">No progress recorded yet — open the tracker below to start.</div>
                    )}

                    {/* Inline mini-tracker */}
                    {isSelected && plan && (() => {
                      const STATUS_OPTS = Object.entries(STATUS_META_TP)
                      const actions = planActions
                      return (
                        <div className="border-t border-gray-200 bg-gray-50">
                          <div className="px-5 py-3 border-b border-gray-200 flex items-center justify-between">
                            <span className="text-sm font-bold text-gray-700">{team.name} — {m.label} Action Tracker ({actions.length} actions)</span>
                            <button onClick={() => {
                              const resetTd = { ...teamTrackers }
                              delete resetTd[team.name]
                              setTeamTrackers(resetTd)
                              localStorage.setItem('pdlc_team_trackers', JSON.stringify(resetTd))
                            }} className="text-xs text-sky-400 hover:text-sky-600">Reset</button>
                          </div>
                          <div className="overflow-x-auto">
                            <table className="w-full text-xs">
                              <thead className="bg-white border-b border-gray-200">
                                <tr>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500 w-8">#</th>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500">Action</th>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500 w-28">Track</th>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500 w-28">Phase</th>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500 w-28">Status</th>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500 w-28">Owner</th>
                                  <th className="text-left px-3 py-2 font-semibold text-gray-500 w-28">Target Date</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-gray-100">
                                {actions.map((row, ri) => {
                                  const d = td[row.id] || {}
                                  const ls = LANE_STYLE[row.lane]
                                  const sm = STATUS_META_TP[d.status || 'not_started']
                                  return (
                                    <tr key={row.id} className="hover:bg-white transition-colors">
                                      <td className="px-3 py-2 text-gray-400">{ri + 1}</td>
                                      <td className="px-3 py-2 text-gray-700 max-w-xs">{row.action}</td>
                                      <td className="px-3 py-2">
                                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold text-white ${ls.badge}`}>{ls.label.replace(/^[^\s]+\s/, '')}</span>
                                      </td>
                                      <td className="px-3 py-2 text-gray-500">{row.phaseName}</td>
                                      <td className="px-3 py-2">
                                        <select value={d.status || 'not_started'} onChange={e => updateTeamAction(team.name, row.id, 'status', e.target.value)}
                                          className={`text-[11px] font-semibold rounded px-1.5 py-0.5 border-0 outline-none cursor-pointer ${sm.bg} ${sm.text}`}>
                                          {STATUS_OPTS.map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
                                        </select>
                                      </td>
                                      <td className="px-3 py-2">
                                        <input value={d.owner || ''} onChange={e => updateTeamAction(team.name, row.id, 'owner', e.target.value)}
                                          placeholder="Owner" className="w-24 text-xs border border-gray-200 rounded px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-blue-300" />
                                      </td>
                                      <td className="px-3 py-2">
                                        <input type="date" value={d.targetDate || ''} onChange={e => updateTeamAction(team.name, row.id, 'targetDate', e.target.value)}
                                          className="text-xs border border-gray-200 rounded px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-blue-300" />
                                      </td>
                                    </tr>
                                  )
                                })}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )
                    })()}
                  </div>
                )
              })}
            </div>
          </div>
        )
      })()}

      {activeSection === 'investment' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">💰 Investment Breakdown — {scenario?.label}</h3></div>
          <div className="card-body space-y-3">
            {Object.entries(bc.investment).map(([key, val]) => (
              <div key={key} className="flex items-start gap-4 p-4 bg-emerald-50 rounded-lg border border-emerald-200">
                <div className="w-32 shrink-0 text-xs font-bold text-emerald-800 capitalize">{key}</div>
                <div className="text-sm text-gray-700">{val}</div>
              </div>
            ))}
            <div className="p-4 bg-emerald-100 rounded-lg border border-emerald-300 text-center">
              <div className="text-xl font-bold text-emerald-800">Total: {bc.investmentRange}</div>
              <div className="text-xs text-emerald-700 mt-1">One-time implementation investment</div>
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
                  {key === 'ttmImprovement' ? 'Time-to-Market' : key === 'productivityGains' ? 'Productivity' : key === 'qualityImprovement' ? 'Quality' : key === 'operationalSavings' ? 'Operational Savings' : key === 'complianceAutomation' ? 'Compliance Automation' : key === 'securityIncidentReduction' ? 'Security Incident Reduction' : key === 'modelRiskAvoidance' ? 'Model Risk Avoidance' : key === 'businessRiskVisibility' ? 'Business Risk Visibility' : key === 'governanceEfficiency' ? 'Governance Efficiency' : 'Benefit'}
                </div>
                <div className="text-sm text-gray-700">{val}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeSection === 'org' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-2xl p-5">
            <h3 className="font-bold text-blue-900 text-lg mb-1">👥 Organization Change Management — {scenario?.label}</h3>
            <p className="text-sm text-blue-700">Step-by-step guide for each organizational change. Each entry shows WHAT changes, HOW to execute it with numbered steps, a real example, and success criteria.</p>
          </div>
          {bc.orgChanges.map((c, i) => {
            if (typeof c === 'string') return (
              <div key={i} className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <span className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">{i+1}</span>
                <span className="text-sm text-gray-700">{c}</span>
              </div>
            )
            const howSteps = c.how ? c.how.split(/\d+\.\s+/).filter(Boolean) : []
            return (
              <div key={i} className="rounded-2xl overflow-hidden border border-gray-200 shadow-sm">
                <div className="bg-blue-600 px-5 py-4 flex items-start gap-3">
                  <span className="text-2xl">{c.icon}</span>
                  <div className="flex-1">
                    <div className="font-bold text-white text-base">{c.title}</div>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {c.who && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">👤 {c.who}</span>}
                      {c.timeline && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">📅 {c.timeline}</span>}
                      {c.effort && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">⏱ {c.effort}</span>}
                    </div>
                  </div>
                  <button onClick={() => openEdit('cases', 'orgChanges', i)}
                    className="shrink-0 bg-white/20 hover:bg-white/40 text-white text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors">
                    ✏ Edit
                  </button>
                </div>
                <div className="bg-white p-5 space-y-4">
                  {c.what && (
                    <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                      <div className="text-xs font-bold text-blue-700 uppercase tracking-wide mb-2">WHAT &amp; WHY</div>
                      <p className="text-sm text-gray-700">{c.what}</p>
                    </div>
                  )}
                  {howSteps.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">HOW — Step by Step</div>
                      <div className="space-y-2">
                        {howSteps.map((step, si) => (
                          <div key={si} className="flex items-start gap-3 bg-indigo-50 border border-indigo-200 rounded-lg p-3">
                            <span className="bg-indigo-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5">{si + 1}</span>
                            <span className="text-sm text-gray-700">{step.trim()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {c.example && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">EXAMPLE</div>
                      <pre className="bg-gray-900 text-green-300 font-mono text-[11px] p-4 rounded-xl whitespace-pre overflow-x-auto">{c.example}</pre>
                    </div>
                  )}
                  {c.successCriteria && (
                    <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                      <div className="text-xs font-bold text-green-700 uppercase tracking-wide mb-2">✓ SUCCESS CRITERIA</div>
                      <p className="text-sm text-gray-700">{c.successCriteria}</p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {activeSection === 'tools' && (() => {
        const catalog = STATIC_AGENT_CATALOG[activeScenario]
        const tsAgents = tsCfg ? ((tsCfg.target_composition?.agents?.length ? tsCfg.target_composition.agents : seedAdlcAgents())) : null
        return (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-2xl p-5">
            <h3 className="font-bold text-purple-900 text-lg mb-1">🛠️ Tools &amp; Agents — {tsCfg ? `selected future state (L${tsSteps[tsStepIdx]?.level})` : scenario?.label}</h3>
            <p className="text-sm text-purple-700">{tsCfg ? 'The exact agents, tools & activities from your Target State composition (edit them in the Studio). Setup guidance for the platform follows below.' : 'Each tool change shows a before/after comparison, numbered setup steps, a working config example, and how to verify success.'}</p>
          </div>

          {/* Configured future-state composition — the agents/tools actually selected */}
          {tsCfg && (
            <ADLCGrid agents={tsAgents} platformId={tsCfg.platform}
              title={`Agents & Tools — ${(tsCfg.platform || '').replace('_', ' ')} (L${tsSteps[tsStepIdx]?.level})`} />
          )}

          {/* Generic per-scenario reference table — only when no target configured */}
          {!tsCfg && catalog && (
            <div className="card overflow-hidden">
              <div className={`px-5 py-3 flex items-center justify-between ${activeScenario === 'option-a' ? 'bg-blue-500' : activeScenario === 'option-b' ? 'bg-purple-500' : 'bg-emerald-500'}`}>
                <div>
                  <div className="font-bold text-white">
                    {activeScenario === 'option-a' ? `Stage 1 — ${catalog.totalTools} AI Tools by PDLC Phase` : `Stage ${activeScenario === 'option-b' ? '2' : '3'} — ${catalog.totalAgents} ${activeScenario === 'option-b' ? 'Assistive (←)' : 'Autonomous (⚙)'} Agents to Configure`}
                  </div>
                  <div className="text-xs text-white/70 mt-0.5">{catalog.humanModel}</div>
                </div>
                <span className={`text-xs font-bold px-3 py-1 rounded-full ${activeScenario === 'option-a' ? 'bg-blue-500 text-white' : activeScenario === 'option-b' ? 'bg-purple-500 text-white' : 'bg-emerald-500 text-white'}`}>
                  {activeScenario === 'option-a' ? `${catalog.totalTools} Tools` : `${catalog.totalAgents} Agents`}
                </span>
              </div>
              <div className="card-body p-0">
                {activeScenario === 'option-a' ? (
                  <table className="w-full text-xs">
                    <thead className="bg-blue-50 border-b border-blue-100">
                      <tr>
                        <th className="text-left px-4 py-2.5 font-semibold text-blue-700 w-48">PDLC Phase</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-blue-700">Tools to Deploy &amp; Configure</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {Object.entries(catalog.byPhase).map(([phase, tools], i) => (
                        <tr key={phase} className={i % 2 === 0 ? 'bg-white' : 'bg-blue-50/20'}>
                          <td className="px-4 py-2 font-semibold text-gray-700">{phase}</td>
                          <td className="px-4 py-2"><div className="flex flex-wrap gap-1">{tools.map(t => <span key={t} className="bg-blue-50 border border-blue-200 text-blue-800 px-2 py-0.5 rounded font-semibold">{t}</span>)}</div></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <table className="w-full text-xs">
                    <thead className={`border-b ${activeScenario === 'option-b' ? 'bg-purple-50 border-purple-100' : 'bg-emerald-50 border-emerald-100'}`}>
                      <tr>
                        <th className={`text-left px-4 py-2.5 font-semibold w-44 ${activeScenario === 'option-b' ? 'text-purple-700' : 'text-emerald-700'}`}>PDLC Phase</th>
                        <th className={`text-left px-4 py-2.5 font-semibold ${activeScenario === 'option-b' ? 'text-purple-700' : 'text-emerald-700'}`}>Agent</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-gray-600 w-20">Mode</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-gray-600">Platform / Tools</th>
                        <th className="text-left px-4 py-2.5 font-semibold text-gray-600">What it does — Human role</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {Object.entries(catalog.byPhase).map(([phase, agents], pi) =>
                        agents.map((ag, ai) => (
                          <tr key={`${pi}-${ai}`} className={pi % 2 === 0 ? 'bg-white' : activeScenario === 'option-b' ? 'bg-purple-50/20' : 'bg-emerald-50/20'}>
                            {ai === 0 && <td className="px-4 py-2 font-semibold text-gray-700 align-top text-[11px]" rowSpan={agents.length}>{phase}</td>}
                            <td className="px-4 py-2">
                              <span className={`px-2 py-0.5 rounded font-bold border ${activeScenario === 'option-b' ? 'bg-purple-50 border-purple-200 text-purple-900' : 'bg-emerald-50 border-emerald-300 text-emerald-900'}`}>🤖 {ag.agent}</span>
                            </td>
                            <td className="px-4 py-2">
                              {activeScenario === 'option-b'
                                ? <span className="bg-teal-50 border border-teal-200 text-teal-700 px-1.5 py-0.5 rounded text-[10px] font-bold">Assistive</span>
                                : <span className="bg-emerald-600 text-white px-1.5 py-0.5 rounded text-[10px] font-bold">Autonomous</span>
                              }
                            </td>
                            <td className="px-4 py-2"><span className={`px-2 py-0.5 rounded font-mono text-[11px] ${activeScenario === 'option-b' ? 'bg-blue-50 text-blue-700' : 'bg-teal-50 text-teal-700'}`}>{ag.tool}</span></td>
                            <td className="px-4 py-2 text-gray-600 text-[11px]">{ag.role}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}

          <div className="text-xs font-bold text-gray-500 uppercase tracking-widest pt-2">Implementation Details — How to Configure Each Tool</div>
          {bc.toolsChanges.map((c, i) => {
            if (typeof c === 'string') return (
              <div key={i} className="flex items-start gap-3 p-4 bg-purple-50 rounded-lg border border-purple-200">
                <span className="text-purple-700 font-bold">🔧</span>
                <span className="text-sm text-gray-700">{c}</span>
              </div>
            )
            const howSteps = c.how ? c.how.split(/\d+\.\s+/).filter(Boolean) : []
            return (
              <div key={i} className="rounded-2xl overflow-hidden border border-gray-200 shadow-sm">
                <div className="bg-purple-500 px-5 py-4 flex items-start gap-3">
                  <span className="text-2xl">{c.icon}</span>
                  <div className="flex-1">
                    <div className="font-bold text-white text-base">{c.title}</div>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {c.category && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">{c.category}</span>}
                      {c.phase && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">{c.phase}</span>}
                      {c.timeline && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">📅 {c.timeline}</span>}
                      {c.effort && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">⏱ {c.effort}</span>}
                    </div>
                  </div>
                  <button onClick={() => openEdit('cases', 'toolsChanges', i)}
                    className="shrink-0 bg-white/20 hover:bg-white/40 text-white text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors">
                    ✏ Edit
                  </button>
                </div>
                <div className="bg-white p-5 space-y-4">
                  {(c.current || c.change) && (
                    <div className="grid grid-cols-2 gap-3">
                      {c.current && (
                        <div className="bg-sky-50 border border-sky-200 rounded-xl p-3">
                          <div className="text-xs font-bold text-sky-600 uppercase mb-1">BEFORE</div>
                          <p className="text-sm text-gray-700">{c.current}</p>
                        </div>
                      )}
                      {c.change && (
                        <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                          <div className="text-xs font-bold text-green-600 uppercase mb-1">AFTER</div>
                          <p className="text-sm text-gray-700">{c.change}</p>
                        </div>
                      )}
                    </div>
                  )}
                  {howSteps.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">HOW TO IMPLEMENT</div>
                      <div className="space-y-2">
                        {howSteps.map((step, si) => (
                          <div key={si} className="flex items-start gap-3 bg-purple-50 border border-purple-200 rounded-lg p-3">
                            <span className="bg-purple-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5">{si + 1}</span>
                            <span className="text-sm text-gray-700">{step.trim()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {c.example && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">CONFIG EXAMPLE</div>
                      <pre className="bg-gray-900 text-green-300 font-mono text-[11px] p-4 rounded-xl whitespace-pre overflow-x-auto">{c.example}</pre>
                    </div>
                  )}
                  <div className="flex flex-wrap gap-4">
                    {c.tools?.length > 0 && (
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">TOOLS</div>
                        <div className="flex flex-wrap gap-1.5">
                          {c.tools.map((t, ti) => <span key={ti} className="bg-purple-100 text-purple-800 text-xs px-2 py-0.5 rounded-full font-medium">{t}</span>)}
                        </div>
                      </div>
                    )}
                    {c.owner && (
                      <div>
                        <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">OWNER</div>
                        <span className="bg-gray-100 text-gray-700 text-xs px-3 py-1 rounded-full">{c.owner}</span>
                      </div>
                    )}
                  </div>
                  {c.successCriteria && (
                    <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                      <div className="text-xs font-bold text-green-700 uppercase tracking-wide mb-2">✓ SUCCESS CRITERIA</div>
                      <p className="text-sm text-gray-700">{c.successCriteria}</p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
        )
      })()}

      {activeSection === 'devsecops' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-sky-50 to-teal-50 border border-sky-200 rounded-2xl p-5">
            <h3 className="font-bold text-sky-900 text-lg mb-1">
              🔒 DevSecOps Pipeline Changes — {tsCfg && tsSteps[tsStepIdx] ? `L${tsSteps[tsStepIdx].level}` : scenario?.label}
              {tsCfg && <span className="ml-2 text-xs bg-sky-200 text-sky-800 px-2 py-0.5 rounded-full font-semibold">Target State Driven</span>}
            </h3>
            <p className="text-sm text-sky-700">
              {tsCfg ? `Security gates calibrated to L${tsSteps[tsStepIdx]?.level || '?'} maturity on ${(tsCfg.platform || '').replace('_', ' ')}` : 'How to implement AI-powered security at each pipeline stage'}. Includes working config snippets, before/after comparison, and measurable outcomes.
            </p>
          </div>
          <div className="bg-gray-900 rounded-2xl p-5 overflow-x-auto">
            <div className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-3">CI/CD Pipeline — AI Security Gates</div>
            <div className="flex items-end gap-0 min-w-max">
              {[
                { stage: 'Commit', icon: '📝', tool: 'Secret Scan', color: 'sky' },
                { stage: 'PR / Review', icon: '🔍', tool: 'AI SAST', color: 'teal' },
                { stage: 'Build', icon: '🏗️', tool: 'IaC Scan', color: 'emerald' },
                { stage: 'Integration', icon: '🧪', tool: 'DAST', color: 'blue' },
                { stage: 'Release Gate', icon: '🚦', tool: 'AI Release Mgr', color: 'green' },
                { stage: 'Production', icon: '🌐', tool: 'AIOps Monitor', color: 'purple' },
              ].map((s, si) => (
                <div key={si} className="flex items-center">
                  <div className="flex flex-col items-center">
                    <div className="text-xl mb-1">{s.icon}</div>
                    <div className="bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-center" style={{ width: '108px' }}>
                      <div className="text-white text-xs font-bold">{s.stage}</div>
                      <div className="text-xs mt-0.5" style={{ color: s.color === 'sky' ? '#38bdf8' : s.color === 'teal' ? '#2dd4bf' : s.color === 'emerald' ? '#34d399' : s.color === 'blue' ? '#60a5fa' : s.color === 'green' ? '#34d399' : '#a78bfa' }}>{s.tool}</div>
                    </div>
                  </div>
                  {si < 5 && <div className="text-gray-500 text-base mx-1 mb-5">›</div>}
                </div>
              ))}
            </div>
          </div>
          {bc.devSecOps.map((c, i) => {
            if (typeof c === 'string') return (
              <div key={i} className="flex items-start gap-3 p-4 bg-sky-50 rounded-lg border border-sky-200">
                <span className="text-sky-700">🛡️</span>
                <span className="text-sm text-gray-700">{c}</span>
              </div>
            )
            const howSteps = c.how ? c.how.split(/\d+\.\s+/).filter(Boolean) : []
            return (
              <div key={i} className="rounded-2xl overflow-hidden border border-gray-200 shadow-sm">
                <div className="bg-sky-500 px-5 py-4 flex items-start gap-3">
                  <span className="text-2xl">{c.icon}</span>
                  <div className="flex-1">
                    <div className="font-bold text-white text-base">{c.title}</div>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {c.pipelineStage && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">🔗 {c.pipelineStage}</span>}
                      {c.priority && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">🎯 {c.priority}</span>}
                    </div>
                  </div>
                  <button onClick={() => openEdit('cases', 'devSecOps', i)}
                    className="shrink-0 bg-white/20 hover:bg-white/40 text-white text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors">
                    ✏ Edit
                  </button>
                </div>
                <div className="bg-white p-5 space-y-4">
                  {(c.current || c.change) && (
                    <div className="grid grid-cols-2 gap-3">
                      {c.current && (
                        <div className="bg-sky-50 border border-sky-200 rounded-xl p-3">
                          <div className="text-xs font-bold text-sky-600 uppercase mb-1">CURRENT STATE</div>
                          <p className="text-sm text-gray-700">{c.current}</p>
                        </div>
                      )}
                      {c.change && (
                        <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                          <div className="text-xs font-bold text-green-600 uppercase mb-1">TARGET STATE</div>
                          <p className="text-sm text-gray-700">{c.change}</p>
                        </div>
                      )}
                    </div>
                  )}
                  {howSteps.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">HOW TO IMPLEMENT</div>
                      <div className="space-y-2">
                        {howSteps.map((step, si) => (
                          <div key={si} className="flex items-start gap-3 bg-sky-50 border border-sky-200 rounded-lg p-3">
                            <span className="bg-sky-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5">{si + 1}</span>
                            <span className="text-sm text-gray-700">{step.trim()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {c.example && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">CONFIG / CODE EXAMPLE</div>
                      <pre className="bg-gray-900 text-green-300 font-mono text-[11px] p-4 rounded-xl whitespace-pre overflow-x-auto">{c.example}</pre>
                    </div>
                  )}
                  {c.tools?.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">TOOLS</div>
                      <div className="flex flex-wrap gap-1.5">
                        {c.tools.map((t, ti) => <span key={ti} className="bg-sky-100 text-sky-800 text-xs px-2 py-0.5 rounded-full font-medium">{t}</span>)}
                      </div>
                    </div>
                  )}
                  {c.metrics && (
                    <div className="bg-teal-50 border border-teal-200 rounded-xl p-4">
                      <div className="text-xs font-bold text-teal-700 uppercase tracking-wide mb-2">📊 METRICS</div>
                      <p className="text-sm text-gray-700">{c.metrics}</p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {activeSection === 'aiops' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-2xl p-5">
            <h3 className="font-bold text-indigo-900 text-lg mb-1">
              🤖 AI Ops / Production Support — {tsCfg && tsSteps[tsStepIdx] ? `L${tsSteps[tsStepIdx].level}` : scenario?.label}
              {tsCfg && <span className="ml-2 text-xs bg-indigo-200 text-indigo-800 px-2 py-0.5 rounded-full font-semibold">Target State Driven</span>}
            </h3>
            <p className="text-sm text-indigo-700">
              {tsCfg ? `AIOps stack for L${tsSteps[tsStepIdx]?.level || '?'} maturity on ${(tsCfg.platform || '').replace('_', ' ')}` : 'How to set up AI-driven production operations'}. Each change shows exactly how to configure it with working commands, current vs target state, and measurable outcomes.
            </p>
          </div>
          <div className="bg-gray-900 rounded-2xl p-5">
            <div className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-3">AIOps Observability Stack</div>
            <div className="grid grid-cols-4 gap-2">
              {[
                { layer: 'Feedback Loop', icon: '🔄', tools: 'Telemetry → Backlog', clr: '#34d399' },
                { layer: 'Incident Response', icon: '🚨', tools: 'NLP Routing + PIR', clr: '#38bdf8' },
                { layer: 'Detection', icon: '🔍', tools: 'AI Anomaly Detection', clr: '#60a5fa' },
                { layer: 'Capacity', icon: '📈', tools: 'ML Predictive Scaling', clr: '#a78bfa' },
              ].map((l, li) => (
                <div key={li} className="bg-gray-800 border border-gray-600 rounded-xl p-3 text-center">
                  <div className="text-xl mb-1">{l.icon}</div>
                  <div className="text-white text-xs font-bold">{l.layer}</div>
                  <div className="text-[10px] mt-0.5" style={{ color: l.clr }}>{l.tools}</div>
                </div>
              ))}
            </div>
          </div>
          {bc.aiOps.map((c, i) => {
            if (typeof c === 'string') return (
              <div key={i} className="flex items-start gap-3 p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                <span className="text-indigo-700">⚡</span>
                <span className="text-sm text-gray-700">{c}</span>
              </div>
            )
            const howSteps = c.how ? c.how.split(/\d+\.\s+/).filter(Boolean) : []
            return (
              <div key={i} className="rounded-2xl overflow-hidden border border-gray-200 shadow-sm">
                <div className="bg-indigo-500 px-5 py-4 flex items-start gap-3">
                  <span className="text-2xl">{c.icon}</span>
                  <div className="flex-1">
                    <div className="font-bold text-white text-base">{c.title}</div>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {c.layer && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">🏗 {c.layer}</span>}
                      {c.priority && <span className="bg-white/20 text-white text-xs px-2 py-0.5 rounded-full">🎯 {c.priority}</span>}
                    </div>
                  </div>
                  <button onClick={() => openEdit('cases', 'aiOps', i)}
                    className="shrink-0 bg-white/20 hover:bg-white/40 text-white text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors">
                    ✏ Edit
                  </button>
                </div>
                <div className="bg-white p-5 space-y-4">
                  {(c.current || c.change) && (
                    <div className="grid grid-cols-2 gap-3">
                      {c.current && (
                        <div className="bg-sky-50 border border-sky-200 rounded-xl p-3">
                          <div className="text-xs font-bold text-sky-600 uppercase mb-1">CURRENT STATE</div>
                          <p className="text-sm text-gray-700">{c.current}</p>
                        </div>
                      )}
                      {c.change && (
                        <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                          <div className="text-xs font-bold text-green-600 uppercase mb-1">TARGET STATE</div>
                          <p className="text-sm text-gray-700">{c.change}</p>
                        </div>
                      )}
                    </div>
                  )}
                  {howSteps.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">HOW TO IMPLEMENT</div>
                      <div className="space-y-2">
                        {howSteps.map((step, si) => (
                          <div key={si} className="flex items-start gap-3 bg-indigo-50 border border-indigo-200 rounded-lg p-3">
                            <span className="bg-indigo-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5">{si + 1}</span>
                            <span className="text-sm text-gray-700">{step.trim()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {c.example && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">CONFIG / CODE EXAMPLE</div>
                      <pre className="bg-gray-900 text-green-300 font-mono text-[11px] p-4 rounded-xl whitespace-pre overflow-x-auto">{c.example}</pre>
                    </div>
                  )}
                  {c.tools?.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">TOOLS</div>
                      <div className="flex flex-wrap gap-1.5">
                        {c.tools.map((t, ti) => <span key={ti} className="bg-indigo-100 text-indigo-800 text-xs px-2 py-0.5 rounded-full font-medium">{t}</span>)}
                      </div>
                    </div>
                  )}
                  {c.metrics && (
                    <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                      <div className="text-xs font-bold text-blue-700 uppercase tracking-wide mb-2">📊 METRICS</div>
                      <p className="text-sm text-gray-700">{c.metrics}</p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {activeSection === 'product' && (
        <div className="card">
          <div className="card-header"><h3 className="font-bold text-gray-800">🎯 Product-Centric Ways of Working — {scenario?.label}</h3></div>
          <div className="card-body"><ul className="space-y-3">{bc.productCentricChanges.map((c, i) => (<li key={i} className="flex items-start gap-3 p-4 bg-teal-50 rounded-lg border border-teal-200"><span className="text-teal-700">🎯</span><span className="text-sm text-gray-700">{c}</span></li>))}</ul></div>
        </div>
      )}

      {/* ── Roles & Skills Evolution ── */}
      {activeSection === 'roles' && (() => {
        const effectiveLevel = activeStep?.level || SCENARIO_TO_LEVEL[activeScenario] || 2
        const evo = ROLES_EVOLUTION[effectiveLevel]
        if (!evo) return null
        const totalHumans = evo.roles.reduce((s, r) => s + (rolesOverrides[`${effectiveLevel}_${r.id}_count`] ?? r.count), 0)
        const totalAgents = evo.agents.count
        const totalUpskillHrs = evo.roles.reduce((s, r) => s + r.upskilling.reduce((h, u) => h + u.hours, 0) * (rolesOverrides[`${effectiveLevel}_${r.id}_count`] ?? r.count), 0)
        const typeBadge = (t) => t === 'frontier' ? 'bg-purple-100 text-purple-800 border-purple-300' : t === 'evolving' ? 'bg-amber-100 text-amber-800 border-amber-300' : 'bg-gray-100 text-gray-600 border-gray-300'
        return (
          <div className="space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-2xl p-6 text-white">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h3 className="font-bold text-xl mb-1">Roles & Skills Evolution — {evo.label}</h3>
                  <p className="text-sm opacity-90">{evo.teamStructure}</p>
                  <p className="text-xs opacity-75 mt-1">
                    Based on the Frontier Workforce Model — from traditional pyramid to AI-native inverted structure
                    {tsCfg && <span className="ml-1 bg-white/20 px-2 py-0.5 rounded-full text-[10px] font-bold">Target State Driven</span>}
                  </p>
                </div>
                <div className="flex gap-3 flex-wrap">
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Humans</div>
                    <div className="font-bold text-lg">{totalHumans}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">AI Agents</div>
                    <div className="font-bold text-lg">{totalAgents}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">AI Fluency</div>
                    <div className="font-bold text-sm">{evo.fluencyLevel}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Level selector strip */}
            <div className="flex gap-1">
              {[1,2,3,4,5].map(lv => {
                const lvEvo = ROLES_EVOLUTION[lv]
                const isActive = lv === effectiveLevel
                return (
                  <button key={lv} disabled
                    className={`flex-1 rounded-lg px-3 py-2 text-xs font-semibold text-center transition-all ${isActive ? 'bg-violet-600 text-white shadow-md' : 'bg-gray-100 text-gray-500'}`}>
                    L{lv} — {lvEvo.fluencyLevel}
                  </button>
                )
              })}
            </div>

            {/* AI Fluency Level */}
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-5">
              <div className="flex items-start gap-3">
                <div className="text-3xl">🎓</div>
                <div>
                  <div className="font-bold text-amber-900 text-base">AI Fluency: {evo.fluencyLevel}</div>
                  <p className="text-sm text-amber-800 mt-1">{evo.fluencyDesc}</p>
                  <div className="mt-3 flex gap-2">
                    {['AI-Aware', 'AI-Practitioner', 'AI-Advanced User', 'AI-Champion', 'AI-Champion+'].map((fl, i) => (
                      <div key={fl} className={`text-[10px] px-2 py-1 rounded-full font-semibold border ${fl === evo.fluencyLevel ? 'bg-amber-600 text-white border-amber-600' : 'bg-white text-gray-400 border-gray-200'}`}>
                        L{i+1}: {fl}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Roles Table */}
            <div className="card">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Team Composition — {totalHumans} Humans + {totalAgents} Agents</h3>
                <p className="text-xs text-gray-500">Click count to edit · Frontier roles absorb traditional roles shown below</p>
              </div>
              <div className="card-body">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b-2 border-gray-200">
                        <th className="text-left py-2.5 pr-4 text-xs font-semibold text-gray-600 uppercase">Role</th>
                        <th className="text-center py-2.5 px-3 text-xs font-semibold text-gray-600 uppercase w-16">Count</th>
                        <th className="text-center py-2.5 px-3 text-xs font-semibold text-gray-600 uppercase w-24">Type</th>
                        <th className="text-left py-2.5 px-3 text-xs font-semibold text-gray-600 uppercase">Competencies</th>
                        {effectiveLevel >= 3 && <th className="text-left py-2.5 px-3 text-xs font-semibold text-gray-600 uppercase">Absorbs</th>}
                      </tr>
                    </thead>
                    <tbody>
                      {evo.roles.map((role, ri) => {
                        const overrideKey = `${effectiveLevel}_${role.id}_count`
                        const roleCount = rolesOverrides[overrideKey] ?? role.count
                        return (
                          <tr key={role.id} className={`border-b border-gray-100 ${ri % 2 === 0 ? 'bg-gray-50/50' : ''}`}>
                            <td className="py-3 pr-4">
                              <div className="font-semibold text-gray-800">{role.name}</div>
                              {role.toolchain && (
                                <div className="flex flex-wrap gap-1 mt-1">
                                  {role.toolchain.map(t => (
                                    <span key={t} className="text-[9px] bg-blue-50 text-blue-700 border border-blue-200 px-1.5 py-0.5 rounded">{t}</span>
                                  ))}
                                </div>
                              )}
                            </td>
                            <td className="py-3 px-3 text-center">
                              <input type="number" min={0} max={20}
                                className="w-14 text-center border border-gray-300 rounded-lg py-1 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-violet-400"
                                value={roleCount}
                                onChange={e => setRolesOverrides(prev => ({ ...prev, [overrideKey]: Math.max(0, parseInt(e.target.value) || 0) }))} />
                            </td>
                            <td className="py-3 px-3 text-center">
                              <span className={`text-[10px] font-bold px-2 py-1 rounded-full border ${typeBadge(role.type)}`}>
                                {role.type === 'frontier' ? 'Frontier' : role.type === 'evolving' ? 'Evolving' : 'Traditional'}
                              </span>
                            </td>
                            <td className="py-3 px-3">
                              <div className="flex flex-wrap gap-1">
                                {role.competencies.map(c => (
                                  <span key={c} className="text-[10px] bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded-full">{c}</span>
                                ))}
                              </div>
                            </td>
                            {effectiveLevel >= 3 && (
                              <td className="py-3 px-3">
                                {role.absorbs ? (
                                  <div className="flex flex-wrap gap-1">
                                    {role.absorbs.map(a => (
                                      <span key={a} className="text-[10px] bg-red-50 text-red-600 border border-red-200 px-2 py-0.5 rounded-full line-through">{a}</span>
                                    ))}
                                  </div>
                                ) : <span className="text-xs text-gray-400">—</span>}
                              </td>
                            )}
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Typical Day (for frontier roles with typicalDay) */}
            {evo.roles.some(r => r.typicalDay) && (
              <div className="card">
                <div className="card-header">
                  <h3 className="font-bold text-gray-800">Typical Day — Time Allocation</h3>
                  <p className="text-xs text-gray-500">How frontier roles spend their time at L{effectiveLevel}</p>
                </div>
                <div className="card-body">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {evo.roles.filter(r => r.typicalDay).map(role => (
                      <div key={role.id} className="bg-gradient-to-b from-violet-50 to-white border border-violet-200 rounded-xl p-4">
                        <div className="font-semibold text-violet-900 text-sm mb-3">{role.name}</div>
                        <div className="space-y-2">
                          {Object.entries(role.typicalDay).map(([activity, pct]) => (
                            <div key={activity} className="flex items-center gap-2">
                              <div className="flex-1">
                                <div className="flex justify-between text-xs mb-0.5">
                                  <span className="text-gray-700">{activity}</span>
                                  <span className="font-bold text-violet-700">{pct}%</span>
                                </div>
                                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                  <div className="h-full bg-violet-500 rounded-full" style={{ width: `${pct}%` }} />
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Upskilling / Learning Plan */}
            <div className="card">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Upskilling & Learning Plan</h3>
                <p className="text-xs text-gray-500">Total: ~{totalUpskillHrs.toLocaleString()} person-hours across {totalHumans} team members</p>
              </div>
              <div className="card-body space-y-4">
                {evo.roles.map(role => {
                  const roleCount = rolesOverrides[`${effectiveLevel}_${role.id}_count`] ?? role.count
                  if (roleCount === 0) return null
                  return (
                    <div key={role.id} className="border border-gray-200 rounded-xl overflow-hidden">
                      <div className="bg-gray-50 px-4 py-2.5 flex items-center justify-between">
                        <div className="font-semibold text-gray-800 text-sm">{role.name} <span className="text-gray-400 font-normal">({roleCount}x)</span></div>
                        <div className="text-xs text-gray-500">{role.upskilling.reduce((h, u) => h + u.hours, 0)} hrs per person</div>
                      </div>
                      <div className="p-4">
                        <table className="w-full text-sm">
                          <thead>
                            <tr className="border-b border-gray-100">
                              <th className="text-left py-1.5 pr-4 text-xs font-semibold text-gray-500">Course</th>
                              <th className="text-center py-1.5 px-3 text-xs font-semibold text-gray-500 w-20">Hours</th>
                              <th className="text-left py-1.5 px-3 text-xs font-semibold text-gray-500">Format</th>
                              <th className="text-right py-1.5 pl-3 text-xs font-semibold text-gray-500 w-28">Total Hrs</th>
                            </tr>
                          </thead>
                          <tbody>
                            {role.upskilling.map((u, ui) => (
                              <tr key={ui} className="border-b border-gray-50">
                                <td className="py-2 pr-4 text-gray-700">{u.course}</td>
                                <td className="py-2 px-3 text-center font-semibold text-violet-700">{u.hours}</td>
                                <td className="py-2 px-3"><span className="text-[10px] bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full border border-blue-200">{u.format}</span></td>
                                <td className="py-2 pl-3 text-right font-semibold text-gray-600">{u.hours * roleCount}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Agent Layer */}
            <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl p-5 text-white">
              <div className="flex items-start gap-3">
                <div className="text-3xl">🤖</div>
                <div className="flex-1">
                  <div className="font-bold text-lg mb-1">AI Agent Layer — {totalAgents} Agents</div>
                  <p className="text-sm opacity-80 mb-3">{evo.agents.description}</p>
                  {evo.agents.types.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {evo.agents.types.map(t => (
                        <span key={t} className="text-[10px] bg-white/10 text-white/90 px-2.5 py-1 rounded-full border border-white/20">{t}</span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Level comparison mini-strip */}
            <div className="bg-violet-50 border border-violet-200 rounded-2xl p-5">
              <div className="font-bold text-violet-900 text-sm mb-3">Team Evolution: L1 to L5</div>
              <div className="grid grid-cols-5 gap-2">
                {[1,2,3,4,5].map(lv => {
                  const lv2 = ROLES_EVOLUTION[lv]
                  const lvHumans = lv2.roles.reduce((s, r) => s + r.count, 0)
                  const isActive = lv === effectiveLevel
                  return (
                    <div key={lv} className={`rounded-xl p-3 text-center border-2 ${isActive ? 'border-violet-500 bg-white shadow-md' : 'border-transparent bg-white/60'}`}>
                      <div className={`text-xs font-bold ${isActive ? 'text-violet-700' : 'text-gray-500'}`}>L{lv}</div>
                      <div className="flex justify-center gap-1 mt-2">
                        <div>
                          <div className="text-lg font-bold text-gray-800">{lvHumans}</div>
                          <div className="text-[9px] text-gray-500">humans</div>
                        </div>
                        <div className="text-gray-300 self-center">+</div>
                        <div>
                          <div className="text-lg font-bold text-emerald-600">{lv2.agents.count}</div>
                          <div className="text-[9px] text-gray-500">agents</div>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )
      })()}

      {/* ── Cost Estimator ── */}
      {activeSection === 'costestimator' && (() => {
        const effectiveLevel = activeStep?.level || SCENARIO_TO_LEVEL[activeScenario] || 2
        const platformId = tsCfg?.platform || optCPlatform || 'stump'
        const platformCosts = AGENT_COST_ESTIMATOR.agentCostsByPlatform[platformId] || AGENT_COST_ESTIMATOR.agentCostsByPlatform.stump
        const baselineTeam = AGENT_COST_ESTIMATOR.teamByLevel[1]
        const targetTeam = AGENT_COST_ESTIMATOR.teamByLevel[effectiveLevel]
        const xformCost = AGENT_COST_ESTIMATOR.transformationCostByLevel[effectiveLevel]

        const getHumanCost = (teamDef) => teamDef.humans.reduce((total, h) => {
          const overrideKey = `human_${h.role}_cost`
          const countKey = `human_${h.role}_count_L${effectiveLevel}`
          const annual = costOverrides[overrideKey] ?? (AGENT_COST_ESTIMATOR.humanRoleCosts[h.role]?.annual || 130000)
          const count = costOverrides[countKey] ?? h.count
          return total + (annual * count)
        }, 0)

        const baselineHumanCost = getHumanCost(baselineTeam)
        const targetHumanCost = getHumanCost(targetTeam)
        const agentCount = costOverrides.agentCount ?? targetTeam.agents
        const agentMonthly = (platformCosts.perAgentMonth * agentCount) + (platformCosts.infraMonth || 0) + (platformCosts.llmTokenMonth || 0) + (platformCosts.subscriptionMonth || 0)
        const agentAnnual = agentMonthly * 12
        const overrideTraining = costOverrides.xform_training ?? xformCost.training
        const overrideTooling = costOverrides.xform_tooling ?? xformCost.tooling
        const overrideChangeMgmt = costOverrides.xform_changeMgmt ?? xformCost.changeManagement
        const overrideHiring = costOverrides.xform_hiring ?? xformCost.hiring
        const oneTimeCost = overrideTraining + overrideTooling + overrideChangeMgmt + overrideHiring
        const yr1Total = oneTimeCost + targetHumanCost + agentAnnual
        const yr2Total = targetHumanCost + agentAnnual
        const baselineAnnual = baselineHumanCost
        const yr1Savings = baselineAnnual - (targetHumanCost + agentAnnual)
        const yr2Savings = baselineAnnual - (targetHumanCost + agentAnnual)
        const yr1NetSavings = yr1Savings - oneTimeCost
        const paybackMonths = yr1Savings > 0 ? Math.ceil(oneTimeCost / (yr1Savings / 12)) : 0

        const fmt = (n) => n >= 0 ? `$${(n/1000).toFixed(0)}K` : `-$${(Math.abs(n)/1000).toFixed(0)}K`
        const fmtFull = (n) => `$${n.toLocaleString()}`

        return (
          <div className="space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-emerald-600 to-teal-600 rounded-2xl p-6 text-white">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h3 className="font-bold text-xl mb-1">Transformation Cost Estimator</h3>
                  <p className="text-sm opacity-90">
                    One-time transformation + running costs for L{effectiveLevel} on {platformCosts.label}
                    {tsCfg && <span className="ml-1 bg-white/20 px-2 py-0.5 rounded-full text-[10px] font-bold">Target State Driven</span>}
                  </p>
                </div>
                <div className="flex gap-3 flex-wrap">
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">One-time</div>
                    <div className="font-bold">{fmt(oneTimeCost)}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Year 1 Total</div>
                    <div className="font-bold">{fmt(yr1Total)}</div>
                  </div>
                  <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                    <div className="text-xs opacity-80">Year 2 Running</div>
                    <div className="font-bold">{fmt(yr2Total)}</div>
                  </div>
                  {yr1Savings > 0 && (
                    <div className="bg-white/20 rounded-xl px-4 py-2 text-center">
                      <div className="text-xs opacity-80">Payback</div>
                      <div className="font-bold">{paybackMonths} months</div>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Baseline vs Target side-by-side */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-5">
                <div className="font-bold text-red-800 text-base mb-1">Baseline: {baselineTeam.label}</div>
                <div className="text-xs text-red-700 mb-3">{baselineTeam.humans.reduce((s,h) => s + h.count, 0)} humans · 0 agents</div>
                <div className="text-3xl font-bold text-red-900">{fmt(baselineHumanCost)}<span className="text-sm font-normal text-red-600"> / year</span></div>
                <div className="mt-3 space-y-1">
                  {baselineTeam.humans.map(h => (
                    <div key={h.role} className="flex justify-between text-xs text-red-700">
                      <span>{h.role} x{h.count}</span>
                      <span className="font-semibold">{fmt((AGENT_COST_ESTIMATOR.humanRoleCosts[h.role]?.annual || 130000) * h.count)}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-emerald-50 border-2 border-emerald-200 rounded-2xl p-5">
                <div className="font-bold text-emerald-800 text-base mb-1">Target: L{effectiveLevel} — {targetTeam.label}</div>
                <div className="text-xs text-emerald-700 mb-3">{targetTeam.humans.reduce((s,h) => s + (costOverrides[`human_${h.role}_count_L${effectiveLevel}`] ?? h.count), 0)} humans · {agentCount} agents</div>
                <div className="text-3xl font-bold text-emerald-900">{fmt(targetHumanCost + agentAnnual)}<span className="text-sm font-normal text-emerald-600"> / year</span></div>
                <div className="mt-3 space-y-1">
                  {targetTeam.humans.map(h => {
                    const cnt = costOverrides[`human_${h.role}_count_L${effectiveLevel}`] ?? h.count
                    const ann = costOverrides[`human_${h.role}_cost`] ?? (AGENT_COST_ESTIMATOR.humanRoleCosts[h.role]?.annual || 130000)
                    return (
                      <div key={h.role} className="flex justify-between text-xs text-emerald-700">
                        <span>{h.role} x{cnt}</span>
                        <span className="font-semibold">{fmt(ann * cnt)}</span>
                      </div>
                    )
                  })}
                  <div className="flex justify-between text-xs text-emerald-700 pt-1 border-t border-emerald-200">
                    <span>AI Agents x{agentCount} ({platformCosts.label})</span>
                    <span className="font-semibold">{fmt(agentAnnual)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Human Cost Breakdown (editable) */}
            <div className="card">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Human Cost Breakdown — L{effectiveLevel} Target Team</h3>
                <p className="text-xs text-gray-500">Edit count or annual cost to adjust the estimate</p>
              </div>
              <div className="card-body">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="text-left py-2 pr-4 text-xs font-semibold text-gray-600 uppercase">Role</th>
                      <th className="text-center py-2 px-3 text-xs font-semibold text-gray-600 uppercase w-20">Count</th>
                      <th className="text-right py-2 px-3 text-xs font-semibold text-gray-600 uppercase w-32">Annual / Person</th>
                      <th className="text-right py-2 pl-3 text-xs font-semibold text-gray-600 uppercase w-28">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {targetTeam.humans.map((h, i) => {
                      const countKey = `human_${h.role}_count_L${effectiveLevel}`
                      const costKey = `human_${h.role}_cost`
                      const cnt = costOverrides[countKey] ?? h.count
                      const ann = costOverrides[costKey] ?? (AGENT_COST_ESTIMATOR.humanRoleCosts[h.role]?.annual || 130000)
                      return (
                        <tr key={h.role} className={`border-b border-gray-100 ${i % 2 === 0 ? 'bg-gray-50/50' : ''}`}>
                          <td className="py-2.5 pr-4 font-semibold text-gray-800">{AGENT_COST_ESTIMATOR.humanRoleCosts[h.role]?.label || h.role}</td>
                          <td className="py-2.5 px-3 text-center">
                            <input type="number" min={0} max={50}
                              className="w-16 text-center border border-gray-300 rounded-lg py-1 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-emerald-400"
                              value={cnt}
                              onChange={e => setCostOverrides(prev => ({ ...prev, [countKey]: Math.max(0, parseInt(e.target.value) || 0) }))} />
                          </td>
                          <td className="py-2.5 px-3 text-right">
                            <input type="number" step={5000} min={0}
                              className="w-28 text-right border border-gray-300 rounded-lg py-1 px-2 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-400"
                              value={ann}
                              onChange={e => setCostOverrides(prev => ({ ...prev, [costKey]: Math.max(0, parseInt(e.target.value) || 0) }))} />
                          </td>
                          <td className="py-2.5 pl-3 text-right font-bold text-emerald-700">{fmtFull(ann * cnt)}</td>
                        </tr>
                      )
                    })}
                    <tr className="border-t-2 border-gray-300 bg-emerald-50">
                      <td className="py-2.5 pr-4 font-bold text-gray-800" colSpan={3}>Total Human Cost</td>
                      <td className="py-2.5 pl-3 text-right font-bold text-emerald-800 text-base">{fmtFull(targetHumanCost)}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Agent Running Cost */}
            <div className="card">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Agent Running Cost — {platformCosts.label}</h3>
                <p className="text-xs text-gray-500">Monthly costs for {agentCount} agents on the selected platform</p>
              </div>
              <div className="card-body">
                <div className="flex items-center gap-4 mb-4">
                  <label className="text-sm font-semibold text-gray-700">Agent Count:</label>
                  <input type="number" min={0} max={50}
                    className="w-20 text-center border border-gray-300 rounded-lg py-1.5 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-teal-400"
                    value={agentCount}
                    onChange={e => setCostOverrides(prev => ({ ...prev, agentCount: Math.max(0, parseInt(e.target.value) || 0) }))} />
                </div>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="text-left py-2 pr-4 text-xs font-semibold text-gray-600 uppercase">Cost Component</th>
                      <th className="text-right py-2 px-3 text-xs font-semibold text-gray-600 uppercase w-28">Monthly</th>
                      <th className="text-right py-2 pl-3 text-xs font-semibold text-gray-600 uppercase w-28">Annual</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b border-gray-100 bg-gray-50/50">
                      <td className="py-2.5 pr-4 text-gray-700">Per-agent cost ({agentCount} agents x {fmtFull(platformCosts.perAgentMonth)}/mo)</td>
                      <td className="py-2.5 px-3 text-right font-semibold">{fmtFull(platformCosts.perAgentMonth * agentCount)}</td>
                      <td className="py-2.5 pl-3 text-right font-semibold">{fmtFull(platformCosts.perAgentMonth * agentCount * 12)}</td>
                    </tr>
                    {platformCosts.infraMonth > 0 && (
                      <tr className="border-b border-gray-100">
                        <td className="py-2.5 pr-4 text-gray-700">Infrastructure (compute, storage)</td>
                        <td className="py-2.5 px-3 text-right font-semibold">{fmtFull(platformCosts.infraMonth)}</td>
                        <td className="py-2.5 pl-3 text-right font-semibold">{fmtFull(platformCosts.infraMonth * 12)}</td>
                      </tr>
                    )}
                    {platformCosts.llmTokenMonth > 0 && (
                      <tr className="border-b border-gray-100 bg-gray-50/50">
                        <td className="py-2.5 pr-4 text-gray-700">LLM token costs (API spend)</td>
                        <td className="py-2.5 px-3 text-right font-semibold">{fmtFull(platformCosts.llmTokenMonth)}</td>
                        <td className="py-2.5 pl-3 text-right font-semibold">{fmtFull(platformCosts.llmTokenMonth * 12)}</td>
                      </tr>
                    )}
                    {platformCosts.subscriptionMonth > 0 && (
                      <tr className="border-b border-gray-100">
                        <td className="py-2.5 pr-4 text-gray-700">Platform subscription</td>
                        <td className="py-2.5 px-3 text-right font-semibold">{fmtFull(platformCosts.subscriptionMonth)}</td>
                        <td className="py-2.5 pl-3 text-right font-semibold">{fmtFull(platformCosts.subscriptionMonth * 12)}</td>
                      </tr>
                    )}
                    <tr className="border-t-2 border-gray-300 bg-teal-50">
                      <td className="py-2.5 pr-4 font-bold text-gray-800">Total Agent Running Cost</td>
                      <td className="py-2.5 px-3 text-right font-bold text-teal-700">{fmtFull(agentMonthly)}</td>
                      <td className="py-2.5 pl-3 text-right font-bold text-teal-800 text-base">{fmtFull(agentAnnual)}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* One-Time Transformation Cost (editable) */}
            <div className="card">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">One-Time Transformation Cost</h3>
                <p className="text-xs text-gray-500">Investment to reach L{effectiveLevel} — edit each line to adjust</p>
              </div>
              <div className="card-body">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b-2 border-gray-200">
                      <th className="text-left py-2 pr-4 text-xs font-semibold text-gray-600 uppercase">Category</th>
                      <th className="text-right py-2 pl-3 text-xs font-semibold text-gray-600 uppercase w-36">Amount (USD)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[
                      { key: 'xform_training', label: 'Training & Certification', defaultVal: xformCost.training },
                      { key: 'xform_tooling', label: 'Tooling & Platform Setup', defaultVal: xformCost.tooling },
                      { key: 'xform_changeMgmt', label: 'Change Management', defaultVal: xformCost.changeManagement },
                      { key: 'xform_hiring', label: 'Hiring / Talent Acquisition', defaultVal: xformCost.hiring },
                    ].map((item, i) => (
                      <tr key={item.key} className={`border-b border-gray-100 ${i % 2 === 0 ? 'bg-gray-50/50' : ''}`}>
                        <td className="py-2.5 pr-4 text-gray-700">{item.label}</td>
                        <td className="py-2.5 pl-3 text-right">
                          <input type="number" step={5000} min={0}
                            className="w-32 text-right border border-gray-300 rounded-lg py-1 px-2 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-amber-400"
                            value={costOverrides[item.key] ?? item.defaultVal}
                            onChange={e => setCostOverrides(prev => ({ ...prev, [item.key]: Math.max(0, parseInt(e.target.value) || 0) }))} />
                        </td>
                      </tr>
                    ))}
                    <tr className="border-t-2 border-gray-300 bg-amber-50">
                      <td className="py-2.5 pr-4 font-bold text-gray-800">Total One-Time Cost</td>
                      <td className="py-2.5 pl-3 text-right font-bold text-amber-800 text-base">{fmtFull(oneTimeCost)}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Total Cost of Ownership Summary */}
            <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl p-6 text-white">
              <h3 className="font-bold text-lg mb-4">Total Cost of Ownership — 3-Year View</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-white/10 rounded-xl p-4 text-center">
                  <div className="text-xs text-white/70">One-Time Investment</div>
                  <div className="font-bold text-xl mt-1">{fmt(oneTimeCost)}</div>
                </div>
                <div className="bg-white/10 rounded-xl p-4 text-center">
                  <div className="text-xs text-white/70">Year 1 (incl. one-time)</div>
                  <div className="font-bold text-xl mt-1">{fmt(yr1Total)}</div>
                </div>
                <div className="bg-white/10 rounded-xl p-4 text-center">
                  <div className="text-xs text-white/70">Year 2 Running</div>
                  <div className="font-bold text-xl mt-1">{fmt(yr2Total)}</div>
                </div>
                <div className="bg-white/10 rounded-xl p-4 text-center">
                  <div className="text-xs text-white/70">Year 3 Running</div>
                  <div className="font-bold text-xl mt-1">{fmt(yr2Total)}</div>
                </div>
              </div>
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/20">
                    <th className="text-left py-2 pr-4 text-xs font-semibold text-white/70 uppercase">Component</th>
                    <th className="text-right py-2 px-3 text-xs font-semibold text-white/70 uppercase">Year 1</th>
                    <th className="text-right py-2 px-3 text-xs font-semibold text-white/70 uppercase">Year 2</th>
                    <th className="text-right py-2 pl-3 text-xs font-semibold text-white/70 uppercase">Year 3</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-white/10">
                    <td className="py-2 pr-4 text-white/90">One-Time Transformation</td>
                    <td className="py-2 px-3 text-right">{fmtFull(oneTimeCost)}</td>
                    <td className="py-2 px-3 text-right text-white/40">—</td>
                    <td className="py-2 pl-3 text-right text-white/40">—</td>
                  </tr>
                  <tr className="border-b border-white/10">
                    <td className="py-2 pr-4 text-white/90">Human Team Cost</td>
                    <td className="py-2 px-3 text-right">{fmtFull(targetHumanCost)}</td>
                    <td className="py-2 px-3 text-right">{fmtFull(targetHumanCost)}</td>
                    <td className="py-2 pl-3 text-right">{fmtFull(targetHumanCost)}</td>
                  </tr>
                  <tr className="border-b border-white/10">
                    <td className="py-2 pr-4 text-white/90">Agent Running Cost</td>
                    <td className="py-2 px-3 text-right">{fmtFull(agentAnnual)}</td>
                    <td className="py-2 px-3 text-right">{fmtFull(agentAnnual)}</td>
                    <td className="py-2 pl-3 text-right">{fmtFull(agentAnnual)}</td>
                  </tr>
                  <tr className="border-t-2 border-white/30">
                    <td className="py-2.5 pr-4 font-bold text-white">Total</td>
                    <td className="py-2.5 px-3 text-right font-bold">{fmtFull(yr1Total)}</td>
                    <td className="py-2.5 px-3 text-right font-bold">{fmtFull(yr2Total)}</td>
                    <td className="py-2.5 pl-3 text-right font-bold">{fmtFull(yr2Total)}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Savings Projection */}
            <div className={`rounded-2xl p-6 border-2 ${yr1Savings > 0 ? 'bg-green-50 border-green-300' : 'bg-orange-50 border-orange-300'}`}>
              <h3 className={`font-bold text-lg mb-4 ${yr1Savings > 0 ? 'text-green-800' : 'text-orange-800'}`}>
                Savings Projection vs Baseline (L1 Traditional Team)
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-white rounded-xl p-4 text-center border border-gray-200">
                  <div className="text-xs text-gray-500">Baseline Annual Cost</div>
                  <div className="font-bold text-lg text-gray-800 mt-1">{fmt(baselineAnnual)}</div>
                  <div className="text-[10px] text-gray-400">{baselineTeam.humans.reduce((s,h)=>s+h.count,0)} humans, 0 agents</div>
                </div>
                <div className="bg-white rounded-xl p-4 text-center border border-gray-200">
                  <div className="text-xs text-gray-500">Annual Running Savings</div>
                  <div className={`font-bold text-lg mt-1 ${yr1Savings > 0 ? 'text-green-700' : 'text-orange-700'}`}>{yr1Savings > 0 ? '+' : ''}{fmt(yr1Savings)}</div>
                  <div className="text-[10px] text-gray-400">{yr1Savings > 0 ? 'saved' : 'additional cost'} per year</div>
                </div>
                <div className="bg-white rounded-xl p-4 text-center border border-gray-200">
                  <div className="text-xs text-gray-500">Year 1 Net (incl. one-time)</div>
                  <div className={`font-bold text-lg mt-1 ${yr1NetSavings > 0 ? 'text-green-700' : 'text-orange-700'}`}>{yr1NetSavings > 0 ? '+' : ''}{fmt(yr1NetSavings)}</div>
                  <div className="text-[10px] text-gray-400">after transformation investment</div>
                </div>
                <div className="bg-white rounded-xl p-4 text-center border border-gray-200">
                  <div className="text-xs text-gray-500">Payback Period</div>
                  <div className="font-bold text-lg text-gray-800 mt-1">
                    {paybackMonths > 0 && paybackMonths <= 36 ? `${paybackMonths} months` : paybackMonths > 36 ? '36+ months' : '—'}
                  </div>
                  <div className="text-[10px] text-gray-400">to recover one-time cost</div>
                </div>
              </div>
              {yr1Savings > 0 && (
                <div className="mt-4 bg-white rounded-xl p-4 border border-green-200">
                  <div className="text-sm text-green-800">
                    <strong>3-Year Cumulative Savings:</strong> {fmtFull(yr1NetSavings + yr2Savings * 2)} — the transformation pays for itself
                    {paybackMonths > 0 && paybackMonths <= 12 && ` within Year 1`}
                    {paybackMonths > 12 && paybackMonths <= 24 && ` during Year 2`}
                    {paybackMonths > 24 && paybackMonths <= 36 && ` during Year 3`}
                    .
                  </div>
                </div>
              )}
            </div>

            {/* Platform comparison mini-table */}
            <div className="card">
              <div className="card-header">
                <h3 className="font-bold text-gray-800">Platform Cost Comparison — {agentCount} Agents</h3>
                <p className="text-xs text-gray-500">Annual agent running cost across all platforms (does not include human costs)</p>
              </div>
              <div className="card-body">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b-2 border-gray-200">
                        <th className="text-left py-2 pr-4 text-xs font-semibold text-gray-600 uppercase">Platform</th>
                        <th className="text-right py-2 px-3 text-xs font-semibold text-gray-600 uppercase">Per-Agent/mo</th>
                        <th className="text-right py-2 px-3 text-xs font-semibold text-gray-600 uppercase">Infra/mo</th>
                        <th className="text-right py-2 px-3 text-xs font-semibold text-gray-600 uppercase">LLM/mo</th>
                        <th className="text-right py-2 px-3 text-xs font-semibold text-gray-600 uppercase">Subscription/mo</th>
                        <th className="text-right py-2 pl-3 text-xs font-semibold text-gray-600 uppercase">Annual Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(AGENT_COST_ESTIMATOR.agentCostsByPlatform).map(([pid, pc], i) => {
                        const annTotal = ((pc.perAgentMonth * agentCount) + (pc.infraMonth || 0) + (pc.llmTokenMonth || 0) + (pc.subscriptionMonth || 0)) * 12
                        const isSelected = pid === platformId
                        return (
                          <tr key={pid} className={`border-b border-gray-100 ${isSelected ? 'bg-emerald-50 font-semibold' : i % 2 === 0 ? 'bg-gray-50/50' : ''}`}>
                            <td className="py-2.5 pr-4">
                              {pc.label}
                              {isSelected && <span className="ml-2 text-[9px] bg-emerald-600 text-white px-1.5 py-0.5 rounded-full">Selected</span>}
                            </td>
                            <td className="py-2.5 px-3 text-right">{fmtFull(pc.perAgentMonth)}</td>
                            <td className="py-2.5 px-3 text-right">{pc.infraMonth ? fmtFull(pc.infraMonth) : '—'}</td>
                            <td className="py-2.5 px-3 text-right">{pc.llmTokenMonth ? fmtFull(pc.llmTokenMonth) : '—'}</td>
                            <td className="py-2.5 px-3 text-right">{pc.subscriptionMonth ? fmtFull(pc.subscriptionMonth) : '—'}</td>
                            <td className={`py-2.5 pl-3 text-right font-bold ${isSelected ? 'text-emerald-700' : 'text-gray-700'}`}>{fmtFull(annTotal)}</td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )
      })()}

      <div className="flex gap-4">
        <Link to="/recommendations" className="btn-primary flex-1 text-center py-3">💡 View All Recommendations →</Link>
        <Link to="/future-state"    className="btn-secondary flex-1 text-center py-3">← Future State VSM</Link>
      </div>

      {/* ── Edit Modal ── */}
      {editingItem && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4" onClick={() => setEditingItem(null)}>
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[92vh] overflow-y-auto flex flex-col" onClick={e => e.stopPropagation()}>
            {/* Modal header */}
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl z-10">
              <div>
                <div className="font-bold text-gray-800 text-base">✏ Edit Card</div>
                <div className="text-xs text-gray-500 mt-0.5">Changes are local to this session. All fields support markdown-style formatting.</div>
              </div>
              <div className="flex gap-2">
                <button onClick={saveItem} className="bg-green-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-green-700 shadow-sm">✓ Save</button>
                <button onClick={() => setEditingItem(null)} className="bg-gray-100 text-gray-600 px-4 py-2 rounded-xl text-sm hover:bg-gray-200">✕ Cancel</button>
              </div>
            </div>
            {/* Modal body */}
            <div className="p-6 space-y-5 flex-1">
              {editForm.title !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Title</label>
                  <input className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                    value={editForm.title} onChange={e => setEditForm(f => ({...f, title: e.target.value}))} />
                </div>
              )}
              {editForm.what !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">What &amp; Why</label>
                  <textarea className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-400" rows={3}
                    value={editForm.what} onChange={e => setEditForm(f => ({...f, what: e.target.value}))} />
                </div>
              )}
              {editForm.current !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Current State (Before)</label>
                  <textarea className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-400" rows={3}
                    value={editForm.current} onChange={e => setEditForm(f => ({...f, current: e.target.value}))} />
                </div>
              )}
              {editForm.change !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Target State (After)</label>
                  <textarea className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-blue-400" rows={3}
                    value={editForm.change} onChange={e => setEditForm(f => ({...f, change: e.target.value}))} />
                </div>
              )}
              {editForm.how !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">
                    HOW — Numbered Steps
                    <span className="text-gray-400 font-normal ml-2 normal-case">Format: "1. Step one. 2. Step two." — each step on same line</span>
                  </label>
                  <textarea className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm font-mono resize-y focus:outline-none focus:ring-2 focus:ring-blue-400" rows={8}
                    value={editForm.how} onChange={e => setEditForm(f => ({...f, how: e.target.value}))} />
                </div>
              )}
              {editForm.example !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Example / Config Code</label>
                  <textarea className="w-full border-2 border-gray-700 rounded-xl px-3 py-3 font-mono text-[11px] bg-gray-900 text-green-300 resize-y focus:outline-none focus:ring-2 focus:ring-green-500" rows={10}
                    value={editForm.example} onChange={e => setEditForm(f => ({...f, example: e.target.value}))} />
                </div>
              )}
              {editForm.successCriteria !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Success Criteria</label>
                  <textarea className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-green-400" rows={3}
                    value={editForm.successCriteria} onChange={e => setEditForm(f => ({...f, successCriteria: e.target.value}))} />
                </div>
              )}
              {editForm.metrics !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Metrics</label>
                  <textarea className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-teal-400" rows={3}
                    value={editForm.metrics} onChange={e => setEditForm(f => ({...f, metrics: e.target.value}))} />
                </div>
              )}
              {editForm.tools !== undefined && (
                <div>
                  <label className="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1">Tools (comma-separated)</label>
                  <input className="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400"
                    value={Array.isArray(editForm.tools) ? editForm.tools.join(', ') : editForm.tools}
                    onChange={e => setEditForm(f => ({...f, tools: e.target.value.split(',').map(t => t.trim()).filter(Boolean)}))} />
                </div>
              )}
            </div>
            {/* Modal footer */}
            <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-3 flex justify-end gap-2 rounded-b-2xl">
              <button onClick={() => setEditingItem(null)} className="bg-gray-200 text-gray-600 px-5 py-2 rounded-xl text-sm hover:bg-gray-300">Cancel</button>
              <button onClick={saveItem} className="bg-green-600 text-white px-6 py-2 rounded-xl text-sm font-semibold hover:bg-green-700 shadow-sm">✓ Save Changes</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
