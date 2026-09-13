import { useState } from 'react'

// ─── Slide data — derived from STUMP-PDLC-Options-A-B-C.pptx ─────────────────
const SLIDES = [
  {
    id: 'option-a',
    label: 'Option A',
    title: 'Augmented Human',
    subtitle: '16 AI assistants support each persona · Human remains the primary actor in every phase',
    mode: 'AI CO-PILOTS',
    modeDesc: 'Every role keeps full ownership. AI accelerates generation, surfaces insights, and handles repetitive tasks. Humans review, decide, and deliver.',
    color: 'blue',
    headerBg: 'from-blue-700 to-blue-900',
    accentBg: 'bg-blue-600',
    accentText: 'text-blue-700',
    accentLight: 'bg-blue-50 border-blue-200',
    badgeBg: 'bg-blue-100 text-blue-800 border-blue-300',
    metrics: [
      { label: 'Lead Time', value: '21–28 days', arrow: '↓' },
      { label: 'Flow Efficiency', value: '18–28%', arrow: '↑' },
      { label: 'Agent Utilisation', value: '30–50%', arrow: '' },
      { label: 'Deploy Freq', value: 'Weekly', arrow: '' },
    ],
    roles: [
      {
        role: 'Product Owner / Product Manager',
        icon: '🎯',
        mode: 'PRIMARY ACTOR',
        modeBg: 'bg-blue-600',
        phasesFocus: 'Ph1 Discovery & Planning · Ph6 Release Sign-off',
        responsibilities: [
          'Write feature intents in USB Docs format → Backlog Assistant auto-generates user stories and ACs',
          'Review AI-prioritised backlog each sprint; approve sprint candidate list from Jira AI suggestions',
          'Facilitate sprint planning using AI-suggested candidate list (target: < 90 min, was 3–4 hrs)',
          'Review and sign off on AI-generated release notes and risk summary before each deployment',
          'Monitor AI output quality via STUMP — escalate low-acceptance-rate stories to Eng Lead',
        ],
        tools: ['Backlog Assistant (GA)', 'USB Docs Pilot', 'Jira AI'],
        shift: 'Story writing: 4–6 hrs/sprint → 1–2 hrs (reviewing AI drafts)',
        shiftIcon: '⏱',
      },
      {
        role: 'UX Designer',
        icon: '🎨',
        mode: 'PRIMARY ACTOR',
        modeBg: 'bg-blue-600',
        phasesFocus: 'Ph2 Architecture & Design',
        responsibilities: [
          'Write design briefs with brand, user persona, and accessibility constraints as Figma AI context',
          'Review AI-generated wireframe options; select the best variant and refine for handoff',
          'Approve final designs before UX Design Coder MCP generates React/CSS component code',
          'Validate AI-generated component code against design system standards',
          'Maintain and update design system library that feeds AI context and constraints',
        ],
        tools: ['Figma AI Pilot', 'UX Design Coder MCP'],
        shift: 'Wireframe creation: 1–2 days → direction + refinement: 4–6 hours',
        shiftIcon: '⚡',
      },
      {
        role: 'Engineering Lead',
        icon: '⚙️',
        mode: 'PRIMARY ACTOR',
        modeBg: 'bg-blue-600',
        phasesFocus: 'Ph3 Development · Ph4 Build & CI/CD',
        responsibilities: [
          'Configure GitHub Copilot for the team: content exclusions, PII policies, seat management',
          'Curate Prompt Library with team-specific coding patterns, security standards, and anti-patterns',
          'Review Code Review Asst flagged items (High/Critical severity only) — not every PR line-by-line',
          'Set up DevBridge Pilot to connect GitHub ↔ Jira, Confluence, and AWS environments',
          'Configure PipelineIQ for build-time optimisation, parallel execution, and flaky test detection',
          'Run fortnightly AI quality review: track acceptance rate, override rate, time saved per agent',
        ],
        tools: ['GitHub Copilot', 'Code Review Asst (GA)', 'Prompt Library (GA)', 'DevBridge Pilot', 'PipelineIQ (GA)'],
        shift: 'PR reviews: every line → AI-escalated exceptions only (saves 6–10 hrs/sprint)',
        shiftIcon: '🔍',
      },
      {
        role: 'Scrum Master',
        icon: '🔄',
        mode: 'PRIMARY ACTOR',
        modeBg: 'bg-blue-600',
        phasesFocus: 'Ph1 Planning · Ph5 Test & QA · All sprint ceremonies',
        responsibilities: [
          'Facilitate sprint planning with AI sprint candidate list (target: < 90 min, was 3 hrs)',
          'Update WoW guides: Definition of Done must include AI usage declaration on every PR',
          'Monitor team AI adoption via STUMP Dashboard — flag phases with < 30% AI utilisation',
          'Track acceptance rate and override rate sprint-over-sprint; coach on quality improvement',
          'Run fortnightly AI wins/fails retrospective item using STUMP agent performance data',
          'Lead 1-hr AI literacy workshop per role and onboard new joiners to AI toolchain',
        ],
        tools: ['STUMP Dashboard', 'QA Suite Pilot', 'Jira AI'],
        shift: 'Ceremony prep: manual → AI-assisted data (planning down from 3 hrs to < 90 min)',
        shiftIcon: '📊',
      },
    ],
  },
  {
    id: 'option-b',
    label: 'Option B',
    title: 'Hybrid Agents',
    subtitle: '12 agents independently deliver key phase outputs · Humans focus on design, decisions & exceptions',
    mode: 'SELECTIVE AUTONOMY',
    modeDesc: 'Agents own routine delivery. Humans focus on strategic design, high-stakes decisions, and exception handling. Role scope narrows; quality responsibility deepens.',
    color: 'emerald',
    headerBg: 'from-cyan-600 to-teal-800',
    accentBg: 'bg-cyan-600',
    accentText: 'text-cyan-700',
    accentLight: 'bg-cyan-50 border-cyan-200',
    badgeBg: 'bg-cyan-100 text-cyan-800 border-cyan-300',
    metrics: [
      { label: 'Lead Time', value: '10–14 days', arrow: '↓' },
      { label: 'Flow Efficiency', value: '32–45%', arrow: '↑' },
      { label: 'Agent Utilisation', value: '60–75%', arrow: '' },
      { label: 'Deploy Freq', value: 'Daily', arrow: '' },
    ],
    roles: [
      {
        role: 'Product Owner / Product Manager',
        icon: '🎯',
        mode: 'DECISION MAKER',
        modeBg: 'bg-cyan-600',
        phasesFocus: 'Ph1 Outcomes & Approval · Ph6 Go/No-Go',
        responsibilities: [
          'Define high-level business outcomes and OKRs — not individual user stories (agent handles decomposition)',
          'Review Smart Backlog Agent-generated and prioritised backlog weekly; approve sprint candidate list',
          'Provide intent corrections to improve agent output quality (feeds back into agent context)',
          'Make go/no-go deployment decision based on Release Manager Agent risk and compliance summary',
          'Monitor agent acceptance rate and backlog accuracy via STUMP; escalate systemic quality issues',
          'Handle exceptions: complex regulatory requirements or novel scenarios agents cannot decompose',
        ],
        tools: ['Smart Backlog Agent (AUTO)', 'USB Docs (ASSIST)', 'Release Manager Agent (AUTO)'],
        shift: 'Backlog management: 8 hrs/sprint → reviewing agent outputs: ~2 hrs/sprint',
        shiftIcon: '⏱',
      },
      {
        role: 'UX Designer',
        icon: '🎨',
        mode: 'DESIGN DIRECTOR',
        modeBg: 'bg-cyan-600',
        phasesFocus: 'Ph2 Design Direction & Approval',
        responsibilities: [
          'Define design intent, brand constraints, and accessibility requirements as agent context (not wireframes)',
          'Review UX Design Agent output: accept, reject, or provide structured correction feedback',
          'Review Design Review Agent compliance report — approve or escalate brand/accessibility violations',
          'Handle design exceptions: novel interaction patterns and complex UX flows the agent cannot resolve',
          'Maintain design system library (agent context source) and update component standards quarterly',
          'Provide final design sign-off before Architecture and Development phases begin',
        ],
        tools: ['UX Design Agent (AUTO)', 'Design Review Agent (AUTO)'],
        shift: 'From full design creation (full sprint) → design governance: 4–6 hrs/sprint',
        shiftIcon: '⚡',
      },
      {
        role: 'Engineering Lead',
        icon: '⚙️',
        mode: 'TECHNICAL GOVERNOR',
        modeBg: 'bg-cyan-600',
        phasesFocus: 'Ph3 Quality Thresholds · Ph4 Pipeline Config · Escalations',
        responsibilities: [
          'Set and maintain quality thresholds: code coverage %, SAST severity levels, test pass rates',
          'Review CodeGen Agent outputs for critical or high-complexity architectural components only',
          'Handle Code Review Agent escalations: architecture decisions, security exceptions, compliance issues',
          'Configure Pipeline Agent: build optimisation rules, parallel execution, flaky test thresholds',
          'Monitor agent ROI metrics on STUMP: time saved, override rate, acceptance rate per agent',
          'Update Prompt Library as codebase patterns evolve; recalibrate agents showing high override rate',
        ],
        tools: ['CodeGen Agent (AUTO)', 'Code Review Agent (AUTO)', 'Pipeline Agent (AUTO)', 'Prompt Library (ASSIST)'],
        shift: 'Coding & reviewing: 20+ hrs/sprint → agent governance & exceptions: ~8 hrs/sprint',
        shiftIcon: '🔍',
      },
      {
        role: 'Scrum Master',
        icon: '🔄',
        mode: 'FLOW MANAGER',
        modeBg: 'bg-cyan-600',
        phasesFocus: 'Sprint Flow · Agent SLAs · Human Escalation Queue',
        responsibilities: [
          'Review and approve Sprint Agent-generated sprint plan each sprint (no longer facilitates planning from scratch)',
          'Monitor agent SLAs: QA Orchestrator, Pipeline Agent, Release Manager Agent throughput and error rates',
          'Manage escalation queue: route agent exceptions to the correct human decision-maker',
          'Facilitate streamlined retrospective using STUMP agent performance data as structured input',
          'Track DORA targets: Daily deployment frequency, CFR < 8%, MTTR < 2 hrs',
          'Identify and unblock inter-agent handoff failures and dependency bottlenecks',
        ],
        tools: ['STUMP Dashboard', 'QA Orchestrator (AUTO)', 'RenovateBot (ASSIST)'],
        shift: 'From ceremony facilitation → agent SLA monitoring & sprint flow optimisation',
        shiftIcon: '📊',
      },
    ],
  },
  {
    id: 'option-c',
    label: 'Option C',
    title: 'AI-First Orchestrated',
    subtitle: '22 agents orchestrate full PDLC end-to-end · Humans oversee, review and approve only',
    mode: 'HUMAN ROLE: OVERSEE · REVIEW · APPROVE',
    modeDesc: 'All PDLC execution is agent-driven. Humans set strategic direction, define acceptance criteria, maintain governance standards, and approve at critical gates only.',
    color: 'purple',
    headerBg: 'from-purple-700 to-indigo-900',
    accentBg: 'bg-purple-600',
    accentText: 'text-purple-700',
    accentLight: 'bg-purple-50 border-purple-200',
    badgeBg: 'bg-purple-100 text-purple-800 border-purple-300',
    metrics: [
      { label: 'Lead Time', value: '3–7 days', arrow: '↓↓' },
      { label: 'Flow Efficiency', value: '50–65%', arrow: '↑↑' },
      { label: 'Agent Utilisation', value: '85–95%', arrow: '' },
      { label: 'Deploy Freq', value: 'Multiple/day', arrow: '' },
    ],
    roles: [
      {
        role: 'Product Owner / Product Manager',
        icon: '🎯',
        mode: 'STRATEGIC APPROVER',
        modeBg: 'bg-purple-600',
        phasesFocus: 'Vision & Outcomes → Final Production Approval',
        responsibilities: [
          'Define vision, strategic outcomes, and acceptance criteria as Discovery Agent context inputs (not stories)',
          'Review Discovery Agent analysis → approve roadmap direction weekly (30 min, was 1-day planning)',
          'Review Backlog Agent-generated sprint stories → approve or reject with reason (not write)',
          'Review Sprint Agent plan → approve with minimal adjustment (agents handle estimation and capacity)',
          'Provide final go/no-go production approval to Release Gate Agent (sole human gate in Ph6)',
          'Monitor KPIs via STUMP: lead time 3–7 days, agent utilisation 85–95%, ROI 4.5–6×',
        ],
        tools: ['Discovery Agent', 'Backlog Agent', 'Sprint Agent', 'Release Gate Agent'],
        shift: '~70% effort reduction — from sprint management to strategic oversight (4–8 hrs/week)',
        shiftIcon: '⏱',
      },
      {
        role: 'UX Designer',
        icon: '🎨',
        mode: 'DESIGN APPROVER',
        modeBg: 'bg-purple-600',
        phasesFocus: 'Design Standards Governance · Final Approval',
        responsibilities: [
          'Define and maintain design principles, brand guidelines, and accessibility standards (agent context source)',
          'Review and approve or reject UI/UX Agent-generated wireframes and design assets',
          'Review Design Review Agent compliance report; escalate brand or accessibility violations',
          'Handle edge-case design decisions that agents flag as needing human judgement',
          'Quarterly design system review: keep agent context current as brand and standards evolve',
        ],
        tools: ['UI/UX Agent', 'Design Review Agent'],
        shift: '~75% effort reduction — from design execution to design governance and standards ownership',
        shiftIcon: '⚡',
      },
      {
        role: 'Engineering Lead',
        icon: '⚙️',
        mode: 'QUALITY GATE OWNER',
        modeBg: 'bg-purple-600',
        phasesFocus: 'Architecture Review · Pipeline Health · Quality Gate Parameters',
        responsibilities: [
          'Review Architecture Agent design decisions for high-risk or compliance-sensitive components only',
          'Set and maintain quality gate parameters: coverage %, security severity, performance SLAs',
          'Monitor Code Generator + Code Reviewer + Tech Debt Agent pipeline health via STUMP Agent Monitor',
          'Approve Rollback Agent activation for P1/P2 production incidents (human authorisation required)',
          'Review Tech Debt Agent quarterly backlog — approve tech debt prioritisation vs feature investment',
          'Ensure Quality Gate Agent thresholds meet compliance requirements linked to Archer Risk Database',
        ],
        tools: ['Architecture Agent', 'Code Generator', 'Code Reviewer', 'Tech Debt Agent', 'Build Agent', 'Quality Gate Agent', 'Security Scanner', 'Rollback Agent'],
        shift: 'From technical delivery → architectural governance and agent pipeline health oversight',
        shiftIcon: '🔍',
      },
      {
        role: 'Scrum Master',
        icon: '🔄',
        mode: 'SYSTEM HEALTH OWNER',
        modeBg: 'bg-purple-600',
        phasesFocus: '22-Agent Orchestration · Escalation Management · DORA Elite KPIs',
        responsibilities: [
          'Monitor 22-agent orchestration pipeline health: inter-agent handoffs, throughput, SLA breaches',
          'Manage all human escalation points from agents — surface only critical decisions to the team',
          'Own DORA Elite targets: lead time 3–7 days, multiple deploys/day, CFR < 5%, MTTR < 1 hr',
          'Run monthly governance review: Compliance Agent outputs against Archer risk controls',
          'Identify systemic agent failures; co-ordinate prompt recalibration with Engineering Lead',
          'Stakeholder reporting: STUMP executive dashboard, metrics progress vs Option A and B baselines',
        ],
        tools: ['Sprint Agent', 'Monitor Agent', 'Incident Triage Agent', 'Compliance Agent', 'STUMP Dashboard'],
        shift: 'From sprint management → AI system governance and DORA Elite performance ownership',
        shiftIcon: '📊',
      },
    ],
  },
]

const OPTION_COLORS = {
  blue: {
    header: 'from-blue-700 to-blue-900',
    badge: 'bg-blue-600',
    badgeLight: 'bg-blue-100 text-blue-800 border border-blue-200',
    card: 'border-blue-200 bg-blue-50/40',
    dot: 'bg-blue-600',
    tool: 'bg-blue-100 text-blue-800 border border-blue-200',
    shift: 'bg-blue-50 border-blue-200 text-blue-900',
    metric: 'bg-blue-900/40 border-blue-500/30',
    tabActive: 'bg-blue-500 text-white',
    nav: 'hover:bg-blue-800',
  },
  amber: {
    header: 'from-cyan-600 to-teal-800',
    badge: 'bg-cyan-600',
    badgeLight: 'bg-cyan-100 text-cyan-800 border border-cyan-200',
    card: 'border-cyan-200 bg-cyan-50/40',
    dot: 'bg-cyan-500',
    tool: 'bg-cyan-100 text-cyan-800 border border-cyan-200',
    shift: 'bg-cyan-50 border-cyan-200 text-cyan-900',
    metric: 'bg-cyan-900/40 border-cyan-500/30',
    tabActive: 'bg-cyan-600 text-white',
    nav: 'hover:bg-cyan-800',
  },
  purple: {
    header: 'from-purple-700 to-indigo-900',
    badge: 'bg-purple-600',
    badgeLight: 'bg-purple-100 text-purple-800 border border-purple-200',
    card: 'border-purple-200 bg-purple-50/40',
    dot: 'bg-purple-600',
    tool: 'bg-purple-100 text-purple-800 border border-purple-200',
    shift: 'bg-purple-50 border-purple-200 text-purple-900',
    metric: 'bg-purple-900/40 border-purple-500/30',
    tabActive: 'bg-purple-500 text-white',
    nav: 'hover:bg-purple-800',
  },
}

export default function RolesSlides() {
  const [activeSlide, setActiveSlide] = useState(0)
  const slide = SLIDES[activeSlide]
  const c = OPTION_COLORS[slide.color]

  return (
    <div className="space-y-0 fade-in">
      {/* Slide navigator */}
      <div className="flex items-center gap-3 mb-4">
        <div className="text-sm font-bold text-gray-600 mr-1">PDLC Role Responsibilities:</div>
        {SLIDES.map((s, i) => (
          <button key={s.id} onClick={() => setActiveSlide(i)}
            className={`px-4 py-1.5 rounded-full text-sm font-bold border-2 transition-all ${
              activeSlide === i
                ? s.color === 'blue' ? 'bg-blue-500 text-white border-blue-700' : s.color === 'emerald' ? 'bg-cyan-600 text-white border-cyan-600' : 'bg-purple-500 text-white border-purple-700'
                : 'bg-white text-gray-600 border-gray-300 hover:border-gray-500'
            }`}>
            {s.label} — {s.title}
          </button>
        ))}
        <div className="ml-auto text-xs text-gray-400 font-medium">Slide {activeSlide + 1} of 3 · US Bank PDLC AI Transformation · STUMP Platform</div>
      </div>

      {/* ── SLIDE ── */}
      <div className="rounded-2xl overflow-hidden shadow-2xl border border-gray-200">

        {/* Slide header */}
        <div className={`bg-gradient-to-r ${c.header} px-8 py-6 text-white`}>
          <div className="flex items-start justify-between gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span className={`${c.badge} text-white text-xs font-black px-3 py-1 rounded-full tracking-widest uppercase`}>{slide.label}</span>
                <span className="text-white/60 text-xs font-bold tracking-widest uppercase border border-white/30 px-2 py-0.5 rounded">{slide.mode}</span>
              </div>
              <h1 className="text-2xl font-black mb-1">{slide.title}</h1>
              <p className="text-white/80 text-sm">{slide.subtitle}</p>
              <p className="text-white/60 text-xs mt-2 max-w-2xl">{slide.modeDesc}</p>
            </div>
            {/* KPI strip */}
            <div className="flex gap-2 shrink-0 flex-wrap justify-end">
              {slide.metrics.map(m => (
                <div key={m.label} className={`rounded-xl px-4 py-2.5 border text-center min-w-[90px] ${c.metric}`}>
                  <div className="text-white font-black text-lg leading-none">{m.value}</div>
                  <div className="text-white/60 text-[10px] mt-1 font-semibold uppercase tracking-wide">{m.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 2×2 Role cards grid */}
        <div className="bg-gray-50 p-6 grid grid-cols-2 gap-5">
          {slide.roles.map((role) => (
            <div key={role.role} className={`rounded-2xl border-2 ${c.card} overflow-hidden bg-white shadow-sm`}>
              {/* Role header */}
              <div className={`bg-gradient-to-r ${c.header} px-5 py-3.5 flex items-center gap-3`}>
                <span className="text-2xl">{role.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="font-black text-white text-sm leading-tight">{role.role}</div>
                  <div className="text-white/70 text-xs mt-0.5 truncate">{role.phasesFocus}</div>
                </div>
                <span className={`${role.modeBg} text-white text-[10px] font-black px-2.5 py-1 rounded-lg tracking-wider shrink-0 border border-white/20`}>
                  {role.mode}
                </span>
              </div>

              {/* Body */}
              <div className="px-5 py-4 space-y-4">
                {/* Responsibilities */}
                <div>
                  <div className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-2.5">KEY RESPONSIBILITIES</div>
                  <ul className="space-y-2">
                    {role.responsibilities.map((r, ri) => (
                      <li key={ri} className="flex items-start gap-2.5">
                        <span className={`${c.dot} text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center shrink-0 mt-0.5`}>{ri + 1}</span>
                        <span className="text-xs text-gray-700 leading-relaxed">{r}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* AI Tools */}
                <div>
                  <div className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-2">AI TOOLS / AGENTS USED</div>
                  <div className="flex flex-wrap gap-1.5">
                    {role.tools.map((t, ti) => (
                      <span key={ti} className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${c.tool}`}>{t}</span>
                    ))}
                  </div>
                </div>

                {/* Key shift */}
                <div className={`rounded-xl border p-3 ${c.shift}`}>
                  <div className="text-[10px] font-black uppercase tracking-widest mb-1 opacity-70">{role.shiftIcon} KEY SHIFT FROM TODAY</div>
                  <div className="text-xs font-semibold leading-relaxed">{role.shift}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Slide footer */}
        <div className={`bg-gradient-to-r ${c.header} px-8 py-2.5 flex items-center justify-between`}>
          <div className="text-white/50 text-[10px] font-semibold tracking-wider">© 2026 Cognizant · US Bank PDLC AI Transformation · Confidential · STUMP Platform · {slide.label}</div>
          <div className="flex items-center gap-3">
            <button onClick={() => setActiveSlide(i => Math.max(0, i - 1))} disabled={activeSlide === 0}
              className="text-white/60 hover:text-white text-xs px-3 py-1 rounded border border-white/20 hover:border-white/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all">← Prev</button>
            <div className="flex gap-1.5">
              {SLIDES.map((_, i) => (
                <button key={i} onClick={() => setActiveSlide(i)}
                  className={`w-2 h-2 rounded-full transition-all ${i === activeSlide ? 'bg-white' : 'bg-white/30 hover:bg-white/60'}`} />
              ))}
            </div>
            <button onClick={() => setActiveSlide(i => Math.min(SLIDES.length - 1, i + 1))} disabled={activeSlide === SLIDES.length - 1}
              className="text-white/60 hover:text-white text-xs px-3 py-1 rounded border border-white/20 hover:border-white/50 disabled:opacity-30 disabled:cursor-not-allowed transition-all">Next →</button>
          </div>
        </div>
      </div>

      {/* Comparison table below slides */}
      <div className="mt-6 bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div className="px-6 py-4 bg-gray-800 text-white">
          <h3 className="font-bold text-base">Role Mode Progression — Option A → B → C</h3>
          <p className="text-gray-400 text-xs mt-0.5">How each role's accountability and interaction model evolves as AI autonomy increases</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-gray-200 bg-gray-50">
                <th className="text-left py-3 px-4 text-xs font-black text-gray-700 uppercase tracking-wide w-40">Role</th>
                <th className="text-left py-3 px-4 text-xs font-black text-blue-700 uppercase tracking-wide">Option A — Augmented Human</th>
                <th className="text-left py-3 px-4 text-xs font-black text-cyan-700 uppercase tracking-wide">Option B — Hybrid Agents</th>
                <th className="text-left py-3 px-4 text-xs font-black text-purple-700 uppercase tracking-wide">Option C — AI-First</th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  role: '🎯 Product Owner',
                  a: { mode: 'Primary Actor', summary: 'Writes intents; reviews AI-generated ACs; runs planning with AI suggestions' },
                  b: { mode: 'Decision Maker', summary: 'Sets outcomes; approves Smart Backlog Agent output; go/no-go on deployments' },
                  c: { mode: 'Strategic Approver', summary: 'Defines vision & acceptance criteria; approves agent-generated roadmap; production gate only' },
                },
                {
                  role: '🎨 UX Designer',
                  a: { mode: 'Primary Actor', summary: 'Briefs Figma AI; reviews and refines AI wireframes; approves before handoff' },
                  b: { mode: 'Design Director', summary: 'Defines design intent; reviews UX Design Agent + Design Review Agent outputs' },
                  c: { mode: 'Design Approver', summary: 'Sets brand/accessibility standards; approves or rejects agent-generated designs only' },
                },
                {
                  role: '⚙️ Engineering Lead',
                  a: { mode: 'Primary Actor', summary: 'Configures Copilot; reviews AI-flagged PR exceptions; curates Prompt Library' },
                  b: { mode: 'Technical Governor', summary: 'Sets quality thresholds; reviews CodeGen escalations; governs Pipeline Agent config' },
                  c: { mode: 'Quality Gate Owner', summary: 'Reviews architecture for complex components; monitors 8-agent pipeline health; approves rollbacks' },
                },
                {
                  role: '🔄 Scrum Master',
                  a: { mode: 'Primary Actor', summary: 'Facilitates AI-assisted ceremonies; monitors adoption via STUMP; coaches AI literacy' },
                  b: { mode: 'Flow Manager', summary: 'Reviews Sprint Agent plan; monitors agent SLAs; manages escalation queue' },
                  c: { mode: 'System Health Owner', summary: 'Monitors 22-agent orchestration; owns DORA Elite KPIs; governs monthly compliance review' },
                },
              ].map((row, i) => (
                <tr key={i} className={`border-b border-gray-100 ${i % 2 === 0 ? 'bg-white' : 'bg-gray-50/60'}`}>
                  <td className="py-3.5 px-4 font-bold text-gray-800 text-sm align-top whitespace-nowrap">{row.role}</td>
                  <td className="py-3.5 px-4 align-top">
                    <span className="inline-block bg-blue-100 text-blue-800 text-[10px] font-black px-2 py-0.5 rounded-full mb-1 border border-blue-200">{row.a.mode}</span>
                    <div className="text-xs text-gray-600">{row.a.summary}</div>
                  </td>
                  <td className="py-3.5 px-4 align-top">
                    <span className="inline-block bg-cyan-100 text-cyan-800 text-[10px] font-black px-2 py-0.5 rounded-full mb-1 border border-cyan-200">{row.b.mode}</span>
                    <div className="text-xs text-gray-600">{row.b.summary}</div>
                  </td>
                  <td className="py-3.5 px-4 align-top">
                    <span className="inline-block bg-purple-100 text-purple-800 text-[10px] font-black px-2 py-0.5 rounded-full mb-1 border border-purple-200">{row.c.mode}</span>
                    <div className="text-xs text-gray-600">{row.c.summary}</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
