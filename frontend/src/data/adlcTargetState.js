// Canonical home-grown AI-Native ADLC target state (US Bank).
// Mirrors the "Stage 3 AI-Native ADLC" board (7 phases × 3 agents = 21), but the
// phase NAMES and ACTIVITIES are sourced from the VSM editor's PDLC_PHASES (the
// single source of truth), and each agent is mapped to the specific VSM activities
// it owns. Agents/tools stay fixed; phases/activities align with the VSM editor.

import { PDLC_PHASES } from './pdlcPhases'

// ADLC phase id ↔ VSM editor phase id, with the 3 agents per phase and the VSM
// activity names each agent owns.
const ADLC_DEF = [
  { id: 'Ph1', vsm: 1, agents: [
    { name: 'Discovery Agent', tool: 'DEV Bridge', activities: ['Product Roadmap Definition', 'Feature Definition & Refinement'] },
    { name: 'Backlog Agent', tool: 'USB Docs', activities: ['Portfolio Epic / VSM Tracking', 'User Story Creation & Refinement'] },
    { name: 'Sprint Agent', tool: 'GitHub Copilot', activities: ['BDD Scenario Writing'] },
  ] },
  { id: 'Ph2', vsm: 2, agents: [
    { name: 'Architecture Agent', tool: 'USB Docs', activities: ['Solution Architecture (High-Level)'] },
    { name: 'UI/UX Agent', tool: 'UX Design Coder', activities: ['UX/UI Research & Wireframing', 'UX/UI High-Fidelity Design & Handoff'] },
    { name: 'Design Review Agent', tool: 'Figma AI', activities: ['Technical Design (Low-Level)'] },
  ] },
  { id: 'Ph3', vsm: 3, agents: [
    { name: 'Code Generator', tool: 'UX Design Coder', activities: ['Coding (Feature Development)', 'Unit Testing'] },
    { name: 'Code Reviewer', tool: 'Code Review Asst.', activities: ['Code Quality / LGTM Analysis', 'Peer Code Review'] },
    { name: 'Tech Debt Agent', tool: 'DEV Bridge', activities: ['Knowledge Transfer / Documentation'] },
  ] },
  { id: 'Ph4', vsm: 4, agents: [
    { name: 'Build Agent', tool: 'QA Suite', activities: ['Build Process (CI)', 'Artifact Creation & Registry'] },
    { name: 'Vuln. Fix Agent', tool: 'App Vuln. Sol.', activities: ['Static Code Analysis (SAST)'] },
    { name: 'Pipeline Agent', tool: 'Log Analytics', activities: ['DEV Deployment'] },
  ] },
  { id: 'Ph5', vsm: 5, agents: [
    { name: 'QA Orchestrator', tool: 'Smart Tester', activities: ['Test Environment Setup', 'Test Data Generation / Management', 'Build Verification Testing (BVT)', 'Defect Triage & Management'] },
    { name: 'UAT Agent', tool: 'QA Suite', activities: ['Manual SIT / UAT / NF Signoff', 'Automated Performance Testing', 'Dynamic Security Testing (DAST)'] },
    { name: 'Regression Agent', tool: 'USB Docs', activities: ['Automated Component Regression', 'Automated Full Regression'] },
  ] },
  { id: 'Ph6', vsm: 6, agents: [
    { name: 'Release Gate Agent', tool: 'App Vuln. Sol.', activities: ['Release Gates / Approvals', 'Release Notes Generation'] },
    { name: 'Deploy Agent', tool: 'DEV Bridge', activities: ['Infrastructure as Code (IaC)', 'Stage Deployment (SIT/UAT/Staging)'] },
    { name: 'Rollback Agent', tool: 'Log Analytics', activities: ['Production Deployment'] },
  ] },
  { id: 'Ph7', vsm: 7, agents: [
    { name: 'Monitor Agent', tool: 'Log Analytics', activities: ['Application Performance Monitoring (APM)', 'Log Aggregation & Analysis'] },
    { name: 'Incident Triage', tool: 'USB Docs', activities: ['Incident Management & RCA'] },
    { name: 'Compliance Agent', tool: 'Risk Asst.', activities: ['Customer Feedback Loop'] },
  ] },
]

const _vsmPhase = (id) => PDLC_PHASES.find(p => p.id === id) || {}

// Phase name + full activity list come from the VSM editor; agents stay fixed.
export const ADLC_PHASES = ADLC_DEF.map(d => {
  const vp = _vsmPhase(d.vsm)
  return {
    id: d.id,
    vsmPhaseId: d.vsm,
    name: vp.name || d.id,
    activities: (vp.activities || []).map(a => a.name),
    agents: d.agents,
  }
})

// name → mapped activities lookup (so saved compositions without activities still resolve).
export const AGENT_ACTIVITY_MAP = {}
ADLC_DEF.forEach(d => d.agents.forEach(a => { AGENT_ACTIVITY_MAP[a.name] = a.activities }))

export const ADLC_PHASE_TINT = [
  'bg-sky-500', 'bg-sky-400', 'bg-sky-500', 'bg-indigo-400',
  'bg-sky-400', 'bg-teal-500', 'bg-cyan-600',
]

export const ADLC_ORCH_STACK = {
  homegrown: 'GitHub Copilot + Azure OpenAI + MCP + LangChain + Agent Skills',
  bmad: 'BMAD Method + Azure OpenAI + MCP + Agent Skills',
  copilot_workspace: 'GitHub Copilot Workspace + Azure OpenAI + MCP',
  devin: 'Devin + Azure OpenAI + MCP + supplemental LangGraph agents',
  cursor: 'Cursor + background agents + Azure OpenAI + supplemental LangGraph',
  flowsource: 'Cognizant Flowsource + accelerators + Azure OpenAI + MCP',
  baxter: 'Cognizant Baxter + Agent Studio + Enterprise ALM Connectors + Governance',
}

export const ADLC_PLATFORM_NAME = {
  homegrown: 'STUMP Agentic Platform', bmad: 'BMAD Platform',
  copilot_workspace: 'Copilot Workspace', devin: 'Devin Platform',
  cursor: 'Cursor Platform', flowsource: 'Cognizant Flowsource',
  baxter: 'Cognizant Baxter',
}

export const ADLC_HUMAN_ROLE =
  'Provide Intent · Review Agent Output · Approve Before Merge / Deploy · Course-correct as needed (Platform does the rest)'

// Flatten the grid into editable composition agents (one row per agent), carrying
// the phase label, mapped VSM activities, posture and active flag.
export function seedAdlcAgents() {
  const out = []
  ADLC_PHASES.forEach(p => {
    const label = `${p.id} · ${p.name}`
    p.agents.forEach(a => out.push({
      phase: label, agent: a.name, tool: a.tool,
      activities: a.activities, role_posture: 'orchestrated', active: true,
    }))
  })
  return out
}

const INSIGHT_PHASE_MAP = {
  'Discovery': 'Ph1',
  'Architecture': 'Ph2',
  'Development': 'Ph3',
  'CI/CD': 'Ph4',
  'Testing': 'Ph5',
  'DevSecOps': 'Ph6',
  'Release': 'Ph6',
  'AIOps & Monitoring': 'Ph7',
  'Monitoring': 'Ph7',
}

export function seedAgentsForPlatform(platformId, insightAgents) {
  if (platformId === 'homegrown' || !insightAgents?.length) return seedAdlcAgents()

  return insightAgents.map(a => {
    const phId = INSIGHT_PHASE_MAP[a.phase] || 'Ph3'
    const vp = PDLC_PHASES.find(p => p.id === parseInt(phId.replace('Ph', '')))
    const phaseLabel = vp ? `${phId} · ${vp.name}` : `${phId} · ${a.phase}`
    return {
      phase: phaseLabel,
      agent: a.name,
      tool: a.description || '',
      activities: [],
      role_posture: 'orchestrated',
      active: true,
    }
  })
}
