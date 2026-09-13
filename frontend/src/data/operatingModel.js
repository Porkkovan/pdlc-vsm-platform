// Operating Model data for Option A → B → C transitions
// Covers: team topology, agent-human interactions, governance tiers,
// agent monitoring (drift, accuracy, cost), ceremonies, Option C platform decision

export const OPERATING_MODEL = {

  // ─── Option A: AI-Enabled ─────────────────────────────────────────────────
  'option-a': {
    maturity: 'AI-Enabled',
    tagline: 'Human-first, AI-assisted',
    agentPct: 10,
    humanPct: 90,
    color: 'blue',
    teams: [
      { name: 'Product Squad ×8', size: '8–10 people', color: 'blue', type: 'Stream-Aligned',
        roles: ['Product Owner', 'Developer ×3', 'QA Engineer', 'BA', 'DevOps', 'AI Champion'],
        aiLayer: 'AI tools as personal productivity aids (Copilot, FeatureGen, DataGen)', agents: [] },
      { name: 'Platform Engineering', size: '4–6 people', color: 'purple', type: 'Platform Team',
        roles: ['DevOps Lead', 'SRE ×2', 'Cloud Engineer'],
        aiLayer: 'Deploys and maintains AI tool integrations (CI/CD, APM)', agents: [] },
      { name: 'AI Centre of Excellence', size: '2–3 people', color: 'amber', type: 'Enabling Team',
        roles: ['AI Champion Lead', 'Data Engineer'],
        aiLayer: 'Governs tool usage policies, prompt standards, acceptable-use policy', agents: [] },
    ],
    interactions: [
      { role: 'PO / BA', icon: '📋', color: 'blue',
        humanDoes: 'Writes all feature intents and acceptance criteria. Reviews AI-generated drafts and accepts/rejects. Runs sprint planning.',
        agentHelps: 'FeatureGen generates AC drafts from intent. Sprint Velocity Predictor suggests sprint scope from history.',
        agentNames: ['FeatureGen', 'Backlog Asst.', 'Sprint Velocity Predictor'],
        ownership: 'Human decides everything. AI is advisory.' },
      { role: 'Developer', icon: '💻', color: 'indigo',
        humanDoes: 'Writes all production code. Accepts or rejects Copilot suggestions line-by-line. Authors and reviews all PRs.',
        agentHelps: 'Copilot suggests completions in IDE. Code Review Asst. pre-annotates PRs for style and patterns.',
        agentNames: ['GitHub Copilot', 'Code Review Asst.'],
        ownership: 'Human writes code. AI reduces boilerplate effort ~25%.' },
      { role: 'QA Engineer', icon: '🧪', color: 'green',
        humanDoes: 'Authors all test plans and scripts. Validates test data schemas. Reviews regression results. Signs off UAT.',
        agentHelps: 'DataGen provisions synthetic test data. Smart Tester suggests test cases from ACs. AI Visual Regression flags UI anomalies.',
        agentNames: ['DataGen', 'Smart Tester', 'AI Visual Regression'],
        ownership: 'Human authors and executes tests. AI reduces data provisioning and script authoring effort.' },
      { role: 'DevOps / SRE', icon: '⚙️', color: 'orange',
        humanDoes: 'Manages all pipeline configs. Triages all alerts manually. Executes all deployments and rollbacks.',
        agentHelps: 'Log Analytics correlates build failures. AI APM reduces alert noise from 200+/day to ~50/day.',
        agentNames: ['Log Analytics', 'AI APM (Dynatrace/Datadog)'],
        ownership: 'Human operates the pipeline. AI reduces noise and speeds up diagnosis.' },
      { role: 'Architect', icon: '🏗️', color: 'purple',
        humanDoes: 'Reviews all ADRs. Runs EA Board. Approves all API designs. Identifies architecture risks.',
        agentHelps: 'USB Docs provides pattern lookup for ADR research. AI SAST flags security patterns in code.',
        agentNames: ['USB Docs', 'AI SAST'],
        ownership: 'All architecture decisions are human. AI reduces research time only.' },
      { role: 'Security / CISO', icon: '🔒', color: 'red',
        humanDoes: 'Manually triages all SAST findings. Collects compliance evidence before each audit. Signs off release risk.',
        agentHelps: 'App Vuln. Solution prioritises SAST findings. Dependabot auto-raises dependency update PRs.',
        agentNames: ['App Vuln. Solution', 'Dependabot'],
        ownership: 'Human approves all security decisions. AI reduces triage volume.' },
    ],
    governance: [
      { tier: 'Autonomous', color: 'green', pct: 5, examples: ['Test data provisioning', 'Dependency update PRs (advisory only)', 'Alert noise filtering'] },
      { tier: 'AI Advisory → Human Decides', color: 'amber', pct: 10, examples: ['Code suggestions (Copilot — line by line)', 'AC drafts (FeatureGen — PO reviews)', 'Sprint scope suggestions'] },
      { tier: 'Human Only', color: 'red', pct: 85, examples: ['All code merges', 'All deployments', 'All ADRs and architecture decisions', 'All sprint commitments', 'All release approvals', 'All compliance sign-offs'] },
    ],
    ceremonies: [
      { name: 'Sprint Planning', from: '3 hrs', to: '1.5 hrs', change: 'AI velocity forecast is starting point. Team still estimates, but debate is shorter.' },
      { name: 'Backlog Refinement', from: '3 hrs', to: '1.5 hrs', change: 'FeatureGen generates AC drafts before session. Team reviews AI output vs writing from scratch.' },
      { name: 'PR Review', from: '4–24 hr wait', to: '2–6 hr wait', change: 'Code Review Asst. pre-handles style/formatting. Human reviewer focuses on logic only.' },
      { name: 'Retrospective', from: '1 hr', to: '1.25 hrs', change: '"AI wins/fails" is now a standing agenda item.' },
    ],
    agentMonitoring: null,
  },

  // ─── Option B: AI-First ──────────────────────────────────────────────────
  'option-b': {
    maturity: 'AI-First',
    tagline: 'Agent-executes, Human-governs',
    agentPct: 60,
    humanPct: 40,
    color: 'purple',
    teams: [
      { name: 'Product Squad ×5–6', size: '4 FTE per pod', color: 'purple', type: 'Stream-Aligned',
        roles: ['AI Product Owner', 'Developer / Agent Operator ×2', 'QA Governor'],
        aiLayer: '11 of 21 agents deployed in high-impact phases. Squad reviews + approves agent outputs in covered phases; executes the remaining phases as in Option A.',
        agents: ['11 agents via Agent Platform (high-impact phases)'] },
      { name: 'Tech Lead / Architect', size: '0.3–0.5 FTE per pod (1 shared across 2–3 pods)', color: 'indigo', type: 'Shared / Fractional',
        roles: ['Tech Lead / Architect'],
        aiLayer: 'Reviews architecture decisions, novel patterns, and cross-pod design. Shared resource — NOT dedicated per pod.',
        agents: ['Architecture Agent', 'Design Review Agent', 'Tech Debt Agent'] },
      { name: 'Agent Ops', size: '0.4 FTE per pod (1 shared across 2–3 pods)', color: 'teal', type: 'Shared / Fractional',
        roles: ['Agent Operator / DevOps Engineer'],
        aiLayer: 'Operates agent platform from pod perspective — prompt tuning, exception handling, SLA monitoring. Shared resource.',
        agents: ['Build Agent', 'Pipeline Agent', 'Monitor Agent'] },
      { name: 'Agent Platform Team', size: '4–5 people (shared org-wide)', color: 'blue', type: 'Platform Team (Shared)',
        roles: ['Platform Lead', 'Agent Engineer ×2', 'SRE', 'AI Ops Engineer'],
        aiLayer: 'Owns agent infrastructure, prompt management, observability, SLAs. One team org-wide.', agents: ['Agent orchestration', 'Prompt registry', 'Agent observability'] },
      { name: 'AI Governance Board', size: '3–5 people (shared org-wide)', color: 'amber', type: 'Governing Body',
        roles: ['CTO', 'CISO', 'Head of Engineering', 'Risk Lead'],
        aiLayer: 'Sets autonomy thresholds quarterly. Reviews override and drift rates. One board org-wide.', agents: ['Policy framework', 'Threshold governance'] },
    ],
    interactions: [
      { role: 'AI Product Owner', icon: '📋', color: 'purple',
        scope: 'Per pod — 1 FTE',
        humanDoes: 'Sets feature intent in natural language for agent-covered phases. Reviews Discovery + Backlog Agent outputs. Approves agent-generated sprint plan. Handles edge cases. Continues to author stories directly for the half of the lifecycle that remains human-executed (as in Option A).',
        agentHelps: 'Discovery Agent → Backlog Agent → Sprint Agent pipeline auto-generates sprint-ready backlog from intent for agent-covered phases. Human approves the plan, not authors it.',
        agentNames: ['Discovery Agent', 'Backlog Agent', 'Sprint Agent'],
        ownership: 'Agent generates, Human approves. ~70% time saving vs Option A on agent-covered work. Per pod.' },
      { role: 'Developer / Agent Operator', icon: '💻', color: 'indigo',
        scope: 'Per pod — 2 FTE',
        humanDoes: 'Reviews Code Generator output for business logic correctness. Approves MRs (architecture focus only). Configures pod-specific agent prompts. Handles novel exceptions. Continues to author code directly for the half of the lifecycle not covered by agents.',
        agentHelps: 'Code Generator scaffolds features from approved designs. Code Reviewer pre-reviews for security / quality / debt. Tech Debt Agent surfaces remediations.',
        agentNames: ['Code Generator', 'Code Reviewer', 'Tech Debt Agent'],
        ownership: 'Agent writes code in covered phases, Human reviews and approves. Dev effort shifts from writing to directing on those phases. Per pod.' },
      { role: 'QA Governor', icon: '🧪', color: 'green',
        scope: 'Per pod — 1 FTE',
        humanDoes: 'Defines test strategy and coverage thresholds for the pod. Reviews QA Orchestrator execution reports. Approves UAT Agent signoff exceptions. Sets quality risk tolerance. Authors tests directly for the non-agent half of the lifecycle (as in Option A).',
        agentHelps: 'QA Orchestrator runs tests in agent-covered phases. UAT Agent coordinates signoff and generates readiness reports. Regression Agent selects test scope per change.',
        agentNames: ['QA Orchestrator', 'UAT Agent', 'Regression Agent'],
        ownership: 'Agents execute and report in covered phases. Human sets policy and reviews exceptions only. Per pod.' },
      { role: 'Tech Lead / Architect', icon: '🏗️', color: 'indigo',
        scope: 'Fractional — 0.3–0.5 FTE per pod (shared across 2–3 pods)',
        humanDoes: 'Reviews 15% of ADRs (novel patterns only). Approves API contracts. Sets architecture policy. Handles design decisions outside agent training scope. NOT dedicated to a single pod — one Tech Lead serves 2–3 pods.',
        agentHelps: 'Architecture Agent auto-screens 85% of ADRs. Design Review Agent validates against design system. API contracts auto-generated from requirements.',
        agentNames: ['Architecture Agent', 'Design Review Agent'],
        ownership: 'Agent handles standard patterns. Human focuses on strategic and novel decisions. Shared across 2–3 pods.' },
      { role: 'Agent Ops', icon: '⚙️', color: 'teal',
        scope: 'Fractional — 0.4 FTE per pod (shared across 2–3 pods)',
        humanDoes: 'Operates the deployed 11 agents from the pod perspective — prompt tuning, exception handling, SLA monitoring, pipeline config. Triages production incidents escalated by Monitor / Triage Agents. Investigates novel failure modes. Shared resource across 2–3 pods.',
        agentHelps: 'Build Agent monitors CI health. Pipeline Agent optimises run order. Deploy Agent executes deployments. Rollback Agent auto-recovers. Monitor Agent + Incident Triage Agent handle detection and known recovery.',
        agentNames: ['Build Agent', 'Pipeline Agent', 'Deploy Agent', 'Rollback Agent', 'Monitor Agent', 'Incident Triage Agent'],
        ownership: 'Agents operate the pipeline + production. Human responds to escalations (< 20% of events). Fractional across 2–3 pods. Absorbs what would have been a separate SRE / On-call role.' },
      { role: 'Agent Platform Team', icon: '🧬', color: 'blue',
        scope: 'Shared org-wide — NOT per-pod (see Team Topology above)',
        humanDoes: 'Owns the agent platform itself (orchestration, prompt registry, evaluation pipeline, observability, SLAs). Updates agent models on LLM-provider model changes. Manages prompt drift detection. Provides second-line support when an agent breaches its SLO. Team of 4–5 people serving all pods.',
        agentHelps: 'Platform-level — the team builds, maintains, and tunes the agents that other roles consume. Outputs: stable agents, evaluation reports, prompt-registry releases.',
        agentNames: ['Agent orchestration', 'Prompt registry', 'Agent observability'],
        ownership: 'Single shared team owns the agent platform for the whole organisation — not a per-pod role.' },
      { role: 'AI Governance Board', icon: '🏛️', color: 'amber',
        scope: 'Shared org-wide governing body (see Team Topology above)',
        humanDoes: 'Sets autonomy thresholds quarterly. Reviews override and drift rates. Sets Vuln. Fix Agent thresholds. Reviews Critical CVEs. Approves compliance framework changes. Handles regulatory inquiries. Members: CTO, CISO, Head of Engineering, Risk Lead.',
        agentHelps: 'Vuln. Fix Agent auto-remediates Low / Medium vulnerabilities. Release Gate Agent scores every change request. Compliance Agent monitors policy drift continuously across all pods.',
        agentNames: ['Vuln. Fix Agent', 'Release Gate Agent', 'Compliance Agent'],
        ownership: 'Agents handle routine compliance and security. Council sets policy + handles regulatory relationship. One board serves the entire organisation. Absorbs Security / Compliance Lead.' },
    ],
    governance: [
      { tier: 'Autonomous', color: 'green', pct: 40,
        examples: ['Low/Med vulnerability auto-fix PRs', 'Test data provisioning', 'Visual regression baseline updates', 'Build log root-cause summaries', 'Post-deploy canary health check', 'PIR draft generation', 'Dependency update PRs with compatibility test attached', 'Flaky test quarantine'] },
      { tier: 'Agent Proposes → Human Approves', color: 'amber', pct: 45,
        examples: ['Sprint plan (Sprint Agent → PO approval)', 'Code Generator output → Dev approval', 'Architecture ADRs (Architecture Agent → Architect)', 'Release gates (Release Gate Agent → Release Manager)', 'UAT signoff report (UAT Agent → QA Lead)', 'Incident RCA (Triage Agent → SRE lead)'] },
      { tier: 'Human Only', color: 'red', pct: 15,
        examples: ['New regulatory requirements', 'Strategic architecture shifts', 'Agent threshold configuration (quarterly AI Governance Board)', 'Novel production incident patterns', 'Organisational policy changes', 'Agent platform architecture decisions'] },
    ],
    ceremonies: [
      { name: 'Sprint Planning', from: '3 hrs', to: '30 min', change: 'Sprint Agent generates the plan. PO reviews and approves. No estimation debate.' },
      { name: 'Backlog Refinement', from: '3 hrs', to: '30 min', change: 'Discovery → Backlog Agent pipeline runs continuously. Ceremony becomes a backlog approval session.' },
      { name: 'Daily Standup', from: '15 min', to: '15 min', change: 'Focus shifts from developer progress to agent exceptions and human decisions required today.' },
      { name: 'Agent Health Review (new)', from: '—', to: '30 min/week', change: 'Platform team reviews agent utilisation, exception rates, override rates, prompt drift.' },
      { name: 'Retrospective', from: '1 hr', to: '1.5 hrs', change: 'Agent effectiveness is the primary agenda: override rate trends, quality issues, prompt improvements.' },
    ],
    agentMonitoring: {
      metrics: [
        { metric: 'Override Rate', desc: 'Human overrides as % of total agent decisions', target: '< 15%', alert: '> 25%', owner: 'Platform Team', why: 'High rate = agents not tuned or not trusted — signals need for prompt review' },
        { metric: 'Exception Rate', desc: '% of agent workflows requiring human intervention', target: '< 20%', alert: '> 35%', owner: 'Agent Operator', why: 'Reveals capability gaps — each exception is a prompt improvement opportunity' },
        { metric: 'Accuracy Score', desc: 'Correct agent decisions as % of sampled decisions (gold-set eval)', target: '> 90%', alert: '< 80%', owner: 'AI Governance Board', why: 'Foundation for trust calibration and autonomous threshold setting' },
        { metric: 'Agent Uptime', desc: '% availability of agent services across all pipeline stages', target: '> 99.5%', alert: '< 99%', owner: 'SRE / Platform', why: 'Downtime degrades to Option A mode — pipeline operates at reduced throughput' },
        { metric: 'Response Latency P99', desc: 'Agent invocation response time at 99th percentile', target: '< 30 sec', alert: '> 60 sec', owner: 'Platform Team', why: 'Slow agents create feedback loop delays, blocking developer throughput' },
        { metric: 'Cost per Agent Run', desc: 'LLM API + infrastructure cost per agent invocation (by type)', target: 'Within ±20% baseline', alert: '> 2× baseline', owner: 'FinOps / Eng Manager', why: 'Uncontrolled run costs = budget overrun; agent loops or oversized prompts are main culprits' },
        { metric: 'Prompt Drift Score', desc: 'Semantic distance of agent outputs vs validated baseline (cosine similarity)', target: '< 0.15 delta', alert: '> 0.25 delta', owner: 'AI CoE', why: 'LLM provider model updates silently degrade output quality — drift score catches this within 1 week' },
        { metric: 'Hallucination Rate', desc: '% of agent outputs flagged incorrect by human reviewers', target: '< 2%', alert: '> 5%', owner: 'AI Governance Board', why: 'Critical for regulated decisions (compliance evidence, security assessments, architecture approvals)' },
      ],
      costs: {
        estimate: '$8K–$18K / month',
        breakdown: [
          { item: 'LLM API (GPT-4o / Claude 3.5)', pct: 55, monthly: '$4K–$10K', note: 'Code review, architecture analysis, UAT report generation are the largest call volumes' },
          { item: 'Agent infrastructure (K8s, orchestration)', pct: 25, monthly: '$2K–$4K', note: 'Agent runtime containers, message queues, state management' },
          { item: 'Observability (traces, metrics, eval pipeline)', pct: 12, monthly: '$1K–$2.5K', note: 'Langfuse / LangSmith / OTEL pipeline for agent tracing and drift eval' },
          { item: 'Vector DB / RAG store', pct: 8, monthly: '$0.6K–$1.5K', note: 'Pinecone / pgvector — grows with document corpus (USB Docs, runbooks, code)' },
        ],
        optimisations: [
          'Cache LLM responses for repeated patterns (code formatting, standard SAST rules) — reduces calls 30–40%',
          'Use smaller models (Claude Haiku / GPT-3.5) for routing, summarisation, and low-stakes agents',
          'Batch non-time-sensitive agent runs (capacity forecasts, PIR generation, dependency scans) to off-peak windows',
          'Set per-agent hard token limits — prevents runaway cost from adversarial inputs or prompt injection',
        ],
      },
      driftDetection: 'Weekly automated evaluation: 50-sample gold-set test per agent. ML monitors output distribution shift. Drift > 0.25 pages Platform Team for prompt review. LLM provider model updates detected within 7 days vs typical 4–6 weeks without monitoring.',
    },
  },

  // ─── Option C: AI-Native ─────────────────────────────────────────────────
  'option-c': {
    maturity: 'AI-Native',
    tagline: 'Human-directs, Agents operate at scale',
    agentPct: 80,
    humanPct: 20,
    color: 'emerald',
    // Platform decision — 4 ways to deliver Option C. IDs match backend C_PLATFORM_OPTIONS.
    platforms: {
      homegrown: {
        name: 'Homegrown / Custom Build',
        tagline: 'Build all 21 agents in-house using LangGraph + Azure OpenAI — full control, no vendor lock-in',
        badge: 'bg-gray-700',
        investmentNote: 'Baseline — full build cost; no platform licence. Higher upfront, lower long-term per-seat cost at scale.',
        timelineNote: 'Longest of the four — 20–28 weeks before full 21-agent autonomous coverage',
        weeksToProd: 26,
        pros: [
          'Full architectural control — swap LLM providers, orchestration frameworks, data stores independently',
          'No vendor lock-in — OSS components (LangGraph + Azure OpenAI + Postgres + Langfuse)',
          'Custom training on proprietary internal data without third-party exposure',
          'Best long-term unit economics once amortised across the 21-agent fleet',
          'Integrate any best-of-breed tooling regardless of vendor compatibility',
        ],
        cons: [
          'Significant engineering effort: 6–8 person AI Platform Engineering team plus dedicated MLOps capability',
          'Platform reliability is fully your responsibility — SRE overhead for the entire agent infrastructure',
          'Slowest path to value: 20–28 weeks before full 21-agent autonomous coverage achieved',
          'LLMOps and prompt-engineering talent is scarce and expensive to hire and retain',
        ],
        platformOps: { name: 'AI Platform Engineering', size: '6–8 people',
          roles: ['Platform Architect', 'LLM Engineer ×2', 'MLOps / LLMOps Engineer', 'SRE ×2', 'Prompt / Policy Engineer', 'Agent Eval Engineer'] },
        investmentDelta: null,
        timelineDelta: null,
      },
      stump: {
        name: 'STUMP ADLC Platform',
        tagline: 'Subscription — pre-wired, fastest path to AI-Native production',
        badge: 'bg-emerald-700',
        investmentNote: '−$300K to −$600K on one-time build vs Homegrown (subscription replaces build). Adds $150K–$240K/yr recurring.',
        timelineNote: '8 weeks faster than Homegrown — production-ready in 18–22 weeks',
        weeksToProd: 18,
        pros: [
          'Pre-integrated agent orchestration — zero custom wiring between the 21 agents',
          'Domain-aware models baked in (financial services, banking patterns)',
          'Built-in compliance evidence packs for SOC2, ISO27001, PCI-DSS, SOX',
          'Single-pane observability dashboard across all agents from day one',
          'Quarterly model updates managed by STUMP — no internal MLOps required',
        ],
        cons: [
          'Platform-roadmap dependency — feature velocity tied to STUMP release cycle',
          'Deep customisation limited to configuration (not code-level agent modification)',
          'Data residency: requires STUMP cloud deployment or licensed on-prem agreement',
          'Recurring subscription cost — economics worsen vs Homegrown at large scale (200+ developers)',
        ],
        platformOps: { name: 'STUMP Platform Operations', size: '2–3 people',
          roles: ['STUMP Platform Admin', 'Prompt / Policy Engineer', 'AI Product Owner'] },
        investmentDelta: '−$300K to −$600K (+ subscription)',
        timelineDelta: '−8 weeks',
      },
      bmad: {
        name: 'BMAD Method (Open-Source)',
        tagline: 'Open-source agentic methodology — bring your own LLM, full control, lowest licence cost',
        badge: 'bg-indigo-700',
        investmentNote: '−$200K to −$400K vs Homegrown (no licence; uses open BMAD methodology + workflows)',
        timelineNote: '4 weeks faster than Homegrown — production-ready in 20–24 weeks',
        weeksToProd: 22,
        pros: [
          'Open-source agentic methodology — no licence cost, no vendor lock-in',
          'Pre-curated agent patterns and prompt libraries — accelerates authoring vs greenfield',
          'LLM-agnostic — works with Azure OpenAI, Anthropic Claude, Google Gemini, OSS models',
          'Community-driven methodology — peer-reviewed agent patterns',
          'Lower platform team headcount than Homegrown (4–5 vs 6–8)',
        ],
        cons: [
          'Framework only — does not replace internal build/integration effort',
          'Smaller community than mainstream commercial platforms — fewer integrators available',
          'Less commercial support — fixes depend on community PR cycle or internal triage',
          'Compliance evidence not bundled — must be built using the methodology',
        ],
        platformOps: { name: 'AI Platform Engineering (BMAD-Aligned)', size: '4–5 people',
          roles: ['Platform Lead', 'BMAD Practitioner', 'LLM Engineer', 'SRE', 'Prompt / Policy Engineer'] },
        investmentDelta: '−$200K to −$400K',
        timelineDelta: '−4 weeks',
      },
      copilot_workspace: {
        name: 'Commercial AI SaaS (Copilot Workspace / Devin)',
        tagline: 'Vendor-managed AI engineer platform — fastest setup, lowest internal capability requirement',
        badge: 'bg-amber-700',
        investmentNote: 'Comparable 3-year TCO to Homegrown, but shifted from one-time build to recurring per-seat subscription.',
        timelineNote: 'Fastest of the four — production-ready in 14–18 weeks',
        weeksToProd: 16,
        pros: [
          'Vendor manages agents end-to-end — no internal MLOps, no LLMOps, no agent authoring required',
          'Latest frontier model access — vendor upgrades baked into subscription',
          'Integrated developer experience — agents live inside IDE / GitHub / VS Code workflow',
          'Fastest time-to-value of all four options (16 weeks to production-ready)',
          'Vendor compliance certifications (SOC2, ISO27001) inherited',
        ],
        cons: [
          'Per-seat subscription costs scale linearly — economics worsen sharply at 200+ developers',
          'Data exposure to vendor — code, prompts, outputs flow through vendor infrastructure (regulated industries: deep review required)',
          'Limited customisation — agent behaviour shaped via prompts and skills, not code',
          'Vendor lock-in — switching cost grows as agent skills and prompts accumulate',
          'May not cover all 21 PDLC phases — strong on Code/CI/CD; weaker on Backlog, Architecture, Compliance',
        ],
        platformOps: { name: 'AI Adoption Team', size: '2 people',
          roles: ['AI Adoption Lead', 'Prompt / Skill Engineer'] },
        investmentDelta: '−$400K to −$800K (+ per-seat sub)',
        timelineDelta: '−10 weeks',
      },
      devin: {
        name: 'Devin (Cognition)',
        tagline: 'Autonomous SWE agent — assign tickets, Devin plans, codes, tests and opens PRs end-to-end',
        badge: 'bg-sky-700',
        investmentNote: '−$350K to −$550K vs Homegrown one-time; adds ~$2K–$4K per active Devin seat / yr',
        timelineNote: 'Fast dev-phase autonomy — production-ready in ~16 weeks',
        weeksToProd: 16,
        pros: [
          'Fastest dev-phase autonomy — Devin executes whole tickets from issue to merged PR',
          'Built-in sandboxed dev environment, browser and shell — minimal wiring',
          'Parallel Devin sessions scale throughput on well-scoped backlog items',
          'Reduces in-house platform team for the development phases',
        ],
        cons: [
          'Coverage skews to dev/test; Discovery, Architecture, Governance need supplemental agents',
          'Per-session/seat economics can be high at scale; supervision needed on ambiguous work',
          'Data-residency / source-access review required before regulated adoption',
          'Vendor-roadmap dependency for capability upgrades',
        ],
        platformOps: { name: 'Agent Adoption Pod', size: '2–3 people',
          roles: ['Devin Orchestration Lead', 'Prompt / Task Engineer', 'Eval & Guardrails Engineer'] },
        investmentDelta: '−$350K to −$550K (+ per-seat sub)',
        timelineDelta: '−10 weeks',
      },
      cursor: {
        name: 'Cursor (Anysphere)',
        tagline: 'AI-native IDE + background agents — deep in-editor codegen, multi-file edits and agentic tasks',
        badge: 'bg-violet-700',
        investmentNote: '−$250K to −$450K vs Homegrown one-time; adds ~$240–$480 per developer / yr',
        timelineNote: 'High developer adoption — production-ready in ~20 weeks',
        weeksToProd: 20,
        pros: [
          'Highest developer adoption — agents live in the IDE developers already use',
          'Strong multi-file edits, codebase-aware chat, and background agents',
          'Low switching cost; immediate Phase 4 velocity gains',
          'Privacy mode and enterprise controls available',
        ],
        cons: [
          'Developer-centric — assistive by default; full autonomy needs orchestration around it',
          'Limited native coverage of Discovery, Governance and AIOps phases',
          'Per-seat cost across a large org; model usage variability',
          'Vendor-roadmap dependency',
        ],
        platformOps: { name: 'Agent Adoption Pod', size: '2–3 people',
          roles: ['Dev Experience Lead', 'Prompt / Rules Engineer', 'Eval & Guardrails Engineer'] },
        investmentDelta: '−$250K to −$450K (+ per-seat sub)',
        timelineDelta: '−6 weeks',
      },
      flowsource: {
        name: 'Cognizant Flowsource',
        tagline: "Cognizant's AI-led SDLC platform — pre-integrated toolchain, accelerators and managed delivery agents",
        badge: 'bg-teal-700',
        investmentNote: '−$400K to −$700K vs Homegrown one-time (platform + accelerators + managed services); recurring platform + services fee',
        timelineNote: 'Fastest broad coverage — production-ready in ~16 weeks',
        weeksToProd: 16,
        pros: [
          'Pre-integrated, opinionated SDLC platform with accelerators across all phases',
          'Managed delivery + platform engineering by Cognizant — minimal in-house team',
          'Built-in governance, quality gates and reusable assets tuned for regulated enterprises',
          'Single accountable partner for platform, agents and delivery uplift',
        ],
        cons: [
          'Highest partner/services dependency — capability tied to Flowsource roadmap',
          'Customisation within platform guardrails; less code-level control than homegrown',
          'Data-residency / third-party access review required for regulated workloads',
          'Recurring platform + managed-services cost',
        ],
        platformOps: { name: 'Flowsource Engagement Team (Cognizant-managed)', size: '2–4 client-side',
          roles: ['Client Platform Owner', 'AI Product Owner', 'Governance / Risk Liaison'] },
        investmentDelta: '−$400K to −$700K (+ platform/services)',
        timelineDelta: '−10 weeks',
      },
    },
    teams: [
      { name: 'Product Pod ×3–4', size: '2 FTE per pod', color: 'emerald', type: 'Intent Team',
        roles: ['Product Definer', 'Product Builder'],
        aiLayer: 'Sets quarterly intent. Agents decompose, build, test, and deploy end-to-end. Builder handles exceptions and high-stakes reviews.', agents: ['Full 21-agent fleet — intent in, running software out'] },
      { name: 'Engineering Architect', size: '0.5–1 FTE per portfolio of 3–5 pods', color: 'purple', type: 'Shared / Fractional',
        roles: ['Engineering Architect'],
        aiLayer: 'Sets architectural policy and approves novel patterns flagged by Architecture Agent across all pods in the portfolio. Not dedicated headcount per pod — shared resource.',
        agents: ['Architecture Agent', 'Design Review Agent', 'Tech Debt Agent'] },
      { name: 'AI Platform Ops', size: 'Varies by platform', color: 'teal', type: 'Platform Team (Shared)',
        roles: ['See platform decision above'],
        aiLayer: 'Owns agent infrastructure, model lifecycle, cost governance, policy enforcement — shared across all portfolios.', agents: [] },
      { name: 'AI Governance Council', size: '4–6 people (shared org-wide)', color: 'amber', type: 'Governing Body',
        roles: ['CTO', 'CISO', 'Risk Officer', 'AI Ethics Lead', 'Regulatory Lead'],
        aiLayer: 'Sets policy, autonomous thresholds, reviews monthly agent performance, handles regulatory reporting. One council serves the entire organisation.', agents: [] },
    ],
    interactions: [
      { role: 'Product Definer', icon: '📋', color: 'emerald',
        scope: 'Per pod — 1 FTE',
        humanDoes: 'Sets quarterly product intent in natural language. Reviews weekly agent-generated outcomes. Approves or redirects at business decision gates. 1 FTE per pod.',
        agentHelps: 'Full Discovery → Backlog → Sprint pipeline runs autonomously. Human sets intent once; agents decompose to sprint stories, estimate, and sequence without human involvement in planning.',
        agentNames: ['Discovery Agent', 'Backlog Agent', 'Sprint Agent'],
        ownership: 'Quarterly intent + weekly outcome approval. 90% of planning is agent-autonomous. Per pod.' },
      { role: 'Product Builder', icon: '🛠️', color: 'indigo',
        scope: 'Per pod — 1 FTE',
        humanDoes: 'Oversees autonomous agent operations within the pod end-to-end. Reviews high-stakes agent outputs flagged by quality gates (code, tests, releases). Handles edge cases and exceptions. Tunes pod-specific agent prompts and policy. Triages production incidents escalated by agents. Sets and reviews quality risk appetite for the pod. Owns release-gate sign-off when agents escalate.',
        agentHelps: 'Code Generator + Code Reviewer + QA Orchestrator + UAT Agent + Regression Agent + Build / Pipeline / Deploy / Rollback Agents operate autonomously. Builder reviews the 15–25% of outputs that breach confidence thresholds or business-critical gates. Compliance Agent flags pod-level compliance issues to Builder; Builder escalates to Governance Council if needed.',
        agentNames: ['Code Generator', 'Code Reviewer', 'QA Orchestrator', 'UAT Agent', 'Regression Agent', 'Build Agent', 'Pipeline Agent', 'Deploy Agent', 'Rollback Agent'],
        ownership: 'Agents execute end-to-end across code, test, and release. Builder reviews exceptions only (~15–25%). Per pod. Absorbs what would have been a separate QA Strategist role in Option B.' },
      { role: 'Engineering Architect', icon: '🏗️', color: 'purple',
        scope: 'Fractional — 0.3–0.5 FTE per pod (shared across 3–5 pods)',
        humanDoes: 'Sets architecture policy and guardrails across the portfolio. Approves novel patterns flagged by Architecture Agent. Owns cross-pod design coherence and tech standards. Reviews ADRs authored by agents. NOT dedicated to a single pod — one architect serves a portfolio of 3–5 pods.',
        agentHelps: 'Architecture Agent handles 95% of design decisions using policy guardrails. Design Review Agent validates against design system. Tech Debt Agent scores remediation. Human reviews novel patterns and cross-pod impacts only.',
        agentNames: ['Architecture Agent', 'Design Review Agent', 'Tech Debt Agent'],
        ownership: 'Agents handle 95% of architecture autonomously. Human focuses on policy + novel patterns + cross-pod coherence.' },
      { role: 'AI Platform Ops Team', icon: '⚙️', color: 'teal',
        scope: 'Shared org-wide — NOT per-pod (see Team Topology above)',
        humanDoes: 'Maintains agent platform health (uptime, latency, cost). Handles completely novel failure modes. Updates agent models on LLM-provider model changes. Manages agent cost budgets and FinOps. Owns prompt registry, evaluation pipeline, drift detection. Responds to governance escalations. Team sizing varies by platform choice (2–8 people, see Team Topology card).',
        agentHelps: 'Monitor Agent handles all production observability across pods. Build / Pipeline / Deploy / Rollback Agents operate the full CI/CD pipeline autonomously. Team is the second-line responder when an agent breaches its SLO.',
        agentNames: ['Monitor Agent', 'Build Agent', 'Pipeline Agent', 'Deploy Agent', 'Rollback Agent'],
        ownership: 'Agents run the platform autonomously. Platform Ops Team responds to < 5% of events. Single shared team serves all pods — not a per-pod role.' },
      { role: 'AI Governance Council', icon: '🏛️', color: 'amber',
        scope: 'Shared org-wide governing body (see Team Topology above)',
        humanDoes: 'Sets regulatory compliance policies (SOC2, PCI-DSS, ISO27001, Dodd-Frank, SOX). Approves Compliance Agent rule changes. Sets autonomy thresholds quarterly. Reviews monthly agent performance. Handles regulatory inquiries and external audit responses. Members: CTO, CISO, Risk Officer, AI Ethics Lead, Regulatory Lead.',
        agentHelps: 'Compliance Agent monitors all PDLC phases continuously across all pods. Release Gate Agent enforces pre-deploy policies. Incident Triage Agent handles compliance events. Vuln. Fix Agent auto-remediates within policy scope. Audit evidence auto-generated quarterly.',
        agentNames: ['Compliance Agent', 'Release Gate Agent', 'Vuln. Fix Agent', 'Incident Triage Agent'],
        ownership: 'Agents monitor and enforce continuously. Council sets policy + handles regulatory relationship. One council serves the entire organisation — not per pod.' },
    ],
    governance: [
      { tier: 'Autonomous', color: 'green', pct: 65,
        examples: ['All standard code generation and review', 'Full CI/CD pipeline execution', 'Test execution and signoff for standard releases', 'All vulnerability remediation within policy scope', 'Deployment and auto-rollback decisions', 'Compliance evidence collection and packaging', 'Capacity scaling decisions', 'Sprint plan generation and story creation', 'Runbook generation and updates'] },
      { tier: 'Agent Proposes → Human Approves', color: 'amber', pct: 25,
        examples: ['Novel architectural patterns (outside training domain)', 'Regulatory framework changes', 'High-risk release business gate review', 'New agent capability deployment', 'Quarterly intent approval', 'High-severity CVE remediation strategy'] },
      { tier: 'Human Only', color: 'red', pct: 10,
        examples: ['Platform architecture decisions (the agent platform itself)', 'New regulatory regime adoption', 'Agent autonomous threshold changes', 'Ethics review of novel AI-generated outputs', 'Incident response for completely unknown failure patterns', 'Executive stakeholder communications'] },
    ],
    ceremonies: [
      { name: 'Quarterly Intent Setting', from: 'Sprint planning ×6/qtr', to: '1 × quarterly session', change: 'Business + Product set goals in natural language. Agents decompose to epics, stories, estimates autonomously. No sprint planning ceremony required.' },
      { name: 'Weekly Outcome Review', from: 'Sprint review ×6/qtr', to: 'Weekly 30-min review', change: 'Product Lead reviews what agents delivered vs intent. Approves continuations or redirects agent direction.' },
      { name: 'Gate Approvals (async)', from: 'CAB + ADR review + UAT sign-off meetings', to: 'Async approval < 24 hrs', change: 'Architecture, Release, and Compliance gates: agent presents decision package via platform UI, human approves async. No scheduled meetings.' },
      { name: 'Monthly Agent Performance Review', from: '—', to: 'Monthly 1 hr', change: 'AI Governance Council reviews all agent health metrics, cost trends, drift scores, override rates, and compliance posture.' },
    ],
    agentMonitoring: {
      metrics: [
        { metric: 'Autonomous Completion Rate', desc: '% of PDLC activities completed without human intervention', target: '> 80%', alert: '< 70%', owner: 'AI Governance Council', why: 'Core Option C KPI — defines the degree of genuine AI-nativeness achieved' },
        { metric: 'Prompt Drift Score', desc: 'Output quality delta vs validated baseline (cosine similarity, per agent)', target: '< 0.10 delta', alert: '> 0.20 delta', owner: 'Platform Ops', why: 'Stricter than Option B — 80% autonomy means drift propagates farther before human catches it' },
        { metric: 'Hallucination Rate', desc: '% of agent decisions flagged incorrect at human gate reviews', target: '< 1%', alert: '> 3%', owner: 'AI Governance Council', why: 'At 80% autonomy, even 3% error rate generates significant incorrect output volume downstream' },
        { metric: 'Policy Compliance Rate', desc: '% of autonomous agent actions compliant with all applicable policies', target: '> 99.5%', alert: '< 99%', owner: 'Risk & Compliance', why: 'Autonomous compliance in a regulated environment must be near-perfect — this is audit evidence' },
        { metric: 'Cost per Feature Delivered', desc: 'Total LLM + infra cost to deliver one production feature end-to-end', target: 'Tracked vs baseline ROI model', alert: '> 2× baseline', owner: 'FinOps / Platform Ops', why: 'Unit economics of autonomous delivery — the primary business case validation metric' },
        { metric: 'Human Gate Response Time', desc: 'Time from agent-surfaced gate to human approval or rejection', target: '< 4 hrs', alert: '> 24 hrs', owner: 'Product Lead / Eng Governor', why: 'Human latency becomes the #1 pipeline bottleneck in AI-Native — slow approvals defeat the model' },
        { metric: 'Override Rate', desc: 'Human overrides as % of total agent decisions', target: '< 8%', alert: '> 15%', owner: 'AI Governance Council', why: 'Higher override rate at Option C signals model regression or policy misalignment at scale' },
        { metric: 'Model Update Impact Score', desc: 'Output quality change after LLM provider model update (automated eval sweep)', target: '< 5% degradation', alert: '> 10% degradation', owner: 'Platform Ops', why: 'Silent LLM provider updates (e.g. model version changes) can degrade all 21 agents simultaneously' },
      ],
      costs: {
        estimate: '$20K–$45K / month',
        breakdown: [
          { item: 'LLM API — primary agents (GPT-4o / Claude Opus)', pct: 50, monthly: '$10K–$22K', note: '80% PDLC coverage means higher invocation volume. Code generation is the largest single cost driver.' },
          { item: 'Platform infrastructure (STUMP subscription or custom K8s)', pct: 20, monthly: '$4K–$9K', note: 'STUMP subscription or custom cluster + orchestration layer + state management' },
          { item: 'Observability, tracing & evaluation pipeline', pct: 15, monthly: '$3K–$7K', note: 'Agent traces, drift evaluation suite, gold-set testing, governance dashboards' },
          { item: 'Vector DB / knowledge stores', pct: 10, monthly: '$2K–$4.5K', note: 'USB Docs, runbooks, compliance frameworks, code context at scale' },
          { item: 'Model fine-tuning & evaluation datasets', pct: 5, monthly: '$1K–$2.5K', note: 'Periodic domain fine-tuning; evaluation dataset curation and maintenance' },
        ],
        optimisations: [
          'Semantic caching: reuse embeddings for similar code patterns — reduces LLM calls 35–50% for stable codebases',
          'Model tiering: Claude Haiku / GPT-3.5 for routing, formatting, and summarisation; Opus / GPT-4o reserved for reasoning-heavy agents (Architecture, Compliance, Release Gate)',
          'Batch non-time-sensitive agent runs — dependency scans, capacity forecasts, PIR generation — to off-peak hours for 30% cost reduction',
          'Per-agent hard token budgets with alerts — prevents runaway cost from adversarial prompts or orchestration loops',
          'FinOps dashboard with per-agent, per-product-pod cost allocation — drives accountability and targeted optimisation',
        ],
      },
      driftDetection: 'Continuous evaluation pipeline: daily 50-sample gold-set evaluation per agent type. ML anomaly detection on output distribution. Model update events trigger immediate full evaluation sweep (all 21 agents) before returning to autonomous mode. Platform Ops alerted within 2 hours of threshold breach. Quarterly full red-team evaluation by AI Governance Council.',
    },
  },
}


// ─────────────────────────────────────────────────────────────────────────────
// Agent → Parent-Tool Lineage
// ─────────────────────────────────────────────────────────────────────────────
// Every Option B agent is an evolution of a tool that already exists in the
// org's Option A (current state) stack. This map captures the lineage so the
// Business Case > Operating Model view can render each Option B/C agent as
// "Agent Name ← Parent Tool".
//
// DEFAULT_AGENT_PARENT_MAP is the US Bank baseline (matches the lineage in
// bottleneckProgression.js verbatim). For other organisations, override per
// project — see resolveAgentParent() below.
//
// Recommended backend wiring for non-US-Bank orgs:
//   - Persist `project.option_a_parent_map` (JSON) when the team's current
//     Option A tooling is captured (DORA assessment or ALM Connect flow).
//   - Frontend passes that override to resolveAgentParent({ orgMap: ... })
//   - Falls back to DEFAULT_AGENT_PARENT_MAP when no project override exists.
// ─────────────────────────────────────────────────────────────────────────────

export const DEFAULT_AGENT_PARENT_MAP = {
  // Discovery & Backlog
  'Discovery Agent':           'DEV Bridge',
  'Backlog Agent':             'Backlog Asst.',
  'Sprint Agent':              'USB Docs',
  // Architecture & Design
  'Architecture Agent':        'USB Docs',
  'Design Review Agent':       'Figma AI',
  'UI/UX Agent':               'UX Design Coder',
  // Code
  'Code Generator':            'UX Design Coder',
  'Code Reviewer':             'Code Review Asst.',
  'Tech Debt Agent':           'DEV Bridge',
  // CI / Build / Pipeline
  'Build Agent':               'QA Suite',
  'Pipeline Agent':            'Log Analytics',
  // Security
  'Vuln. Fix Agent':           'App Vuln. Solution',
  // QA / UAT / Regression
  'QA Orchestrator':           'Smart Tester',
  'UAT Agent':                 'QA Suite',
  'Regression Agent':          'USB Docs',
  // Release / Deploy
  'Release Gate Agent':        'Change Asst.',
  'Deploy Agent':              'CloudBees',
  'Rollback Agent':            'CloudBees',
  // Production / Monitoring
  'Monitor Agent':             'AppDynamics',
  'Incident Triage Agent':     'Splunk',
  'Compliance Agent':          'Risk Asst.',
}

// Option C: parent flips from the legacy Option A tool to the chosen agent
// platform — the team is no longer evolving USB tools, they are operating on
// a different orchestration substrate.
export const C_PLATFORM_PARENT_LABEL = {
  homegrown:         'Custom build',
  stump:             'STUMP Platform',
  bmad:              'BMAD Method',
  copilot_workspace: 'Copilot Workspace',
}

/**
 * Resolve the parent-tool label to render under an agent pill.
 *
 * @param {string} agentName  – e.g. 'Architecture Agent'
 * @param {object} ctx
 *   @prop {string} scenario  – 'option-a' | 'option-b' | 'option-c'
 *   @prop {string} [platform] – for option-c: 'homegrown'|'stump'|'bmad'|'copilot_workspace'
 *   @prop {object} [orgMap]   – per-project override of DEFAULT_AGENT_PARENT_MAP
 * @returns {string|null} parent tool/platform label, or null if no lineage
 */
export function resolveAgentParent(agentName, { scenario, platform, orgMap } = {}) {
  if (scenario === 'option-c' && platform) {
    return C_PLATFORM_PARENT_LABEL[platform] || null
  }
  const map = orgMap || DEFAULT_AGENT_PARENT_MAP
  return map[agentName] || null
}
