/**
 * Canonical PDLC Phase & Activity definitions.
 * Sourced from VSM Analyzer Latest.html prototype — preserved exactly.
 * 7 phases, 36 activities.
 */
export const PDLC_PHASES = [
  {
    id: 1,
    name: 'Backlog & Roadmap',
    defaultEffortRange: { min: 31, max: 74 },
    defaultWaitRange:   { min: 3.5, max: 9 },
    effortUnit: 'hours',
    waitUnit: 'days',
    color: 'blue',
    activities: [
      {
        id: 'p1-a1',
        name: 'Portfolio Epic / VSM Tracking',
        defaultEffort: { min: 8, max: 16 },
        defaultWait:   { min: 1, max: 3 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Ingests flow data (cycle time, lead time, WIP). Uses ML to spot bottleneck patterns. Visualizes metrics & highlights issues. Suggests potential delay causes.',
        agent: 'AI VSM Analyzer',
        type: 'AI Automation',
        tools: ['Jira Align', 'Azure DevOps'],
        personas: ['Delivery Manager', 'Scrum Master']
      },
      {
        id: 'p1-a2',
        name: 'Product Roadmap Definition',
        defaultEffort: { min: 16, max: 40 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Analyzes market/competitor data & feedback. Analyzes backlog velocity & dependencies. Uses NLP for trends. Recommends feature priorities & timelines.',
        agent: 'AI Roadmap Assistant',
        type: 'AI Automation',
        tools: ['Jira Align', 'Confluence'],
        personas: ['Product Manager', 'Product Owner']
      },
      {
        id: 'p1-a3',
        name: 'Feature Definition & Refinement',
        defaultEffort: { min: 4, max: 8 },
        defaultWait:   { min: 1, max: 3 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Takes high-level goals. Accesses user research/personas (RAG). Generates title, description, AC using LLM. Iterates on PM feedback.',
        agent: 'FeatureGen Agent',
        type: 'GenAI Agent',
        tools: ['Jira', 'Confluence'],
        personas: ['Product Manager', 'Business Analyst']
      },
      {
        id: 'p1-a4',
        name: 'BDD Scenario Writing',
        defaultEffort: { min: 2, max: 4 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Reads feature description & AC. Identifies scenarios. Generates Gherkin syntax. Ensures style consistency.',
        agent: 'ScenarioGen Agent',
        type: 'GenAI Agent',
        tools: ['Jira', 'Confluence'],
        personas: ['Business Analyst', 'QA Lead']
      },
      {
        id: 'p1-a5',
        name: 'User Story Creation & Refinement',
        defaultEffort: { min: 1, max: 2 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Takes feature definition. Breaks feature into stories. Generates initial AC. Suggests effort estimates.',
        agent: 'StoryGen Agent',
        type: 'GenAI Agent',
        tools: ['Jira', 'Azure DevOps'],
        personas: ['Product Owner', 'Development Team']
      }
    ]
  },
  {
    id: 2,
    name: 'Architecture & UX Design',
    defaultEffortRange: { min: 36, max: 88 },
    defaultWaitRange:   { min: 8, max: 18.5 },
    effortUnit: 'hours',
    waitUnit: 'days',
    color: 'purple',
    activities: [
      {
        id: 'p2-a1',
        name: 'Solution Architecture (High-Level)',
        defaultEffort: { min: 8, max: 16 },
        defaultWait:   { min: 3, max: 7 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Analyzes NFRs, constraints, goals. Queries architecture pattern knowledge base. Suggests patterns & tech stack options. Identifies trade-offs & risks.',
        agent: 'AI Architecture Advisor',
        type: 'AI Automation',
        tools: ['Confluence', 'Draw.io', 'ADO'],
        personas: ['Solution Architect', 'Tech Lead']
      },
      {
        id: 'p2-a2',
        name: 'UX/UI Research & Wireframing',
        defaultEffort: { min: 8, max: 24 },
        defaultWait:   { min: 2, max: 5 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Takes personas, requirements, or prompts. Generates user flow diagrams. Creates wireframe options. Allows interactive refinement via chat.',
        agent: 'DesignGen Agent',
        type: 'GenAI Agent',
        tools: ['Figma', 'Miro'],
        personas: ['UX Designer', 'Product Manager']
      },
      {
        id: 'p2-a3',
        name: 'UX/UI High-Fidelity Design & Handoff',
        defaultEffort: { min: 16, max: 40 },
        defaultWait:   { min: 2, max: 5 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Takes wireframes & style guide. Applies visual styling. Generates mockups & prototypes. Exports assets & specs for handoff.',
        agent: 'DesignGen Agent',
        type: 'GenAI Agent',
        tools: ['Figma', 'Zeplin'],
        personas: ['UX Designer', 'UI Designer']
      },
      {
        id: 'p2-a4',
        name: 'Technical Design (Low-Level)',
        defaultEffort: { min: 4, max: 8 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Reads user story & high-level architecture. Suggests class structures, APIs. Generates sequence diagrams. Drafts technical docs (READMEs, API specs).',
        agent: 'DesignDoc Agent',
        type: 'GenAI Agent',
        tools: ['Confluence', 'Draw.io'],
        personas: ['Tech Lead', 'Senior Developer']
      }
    ]
  },
  {
    id: 3,
    name: 'Code Management',
    defaultEffortRange: { min: 13, max: 47 },
    defaultWaitRange:   { min: 4, max: 24 },
    effortUnit: 'hours',
    waitUnit: 'hours',
    color: 'green',
    activities: [
      {
        id: 'p3-a1',
        name: 'Coding (Feature Development)',
        defaultEffort: { min: 8, max: 32 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Provides real-time code suggestions & autocompletion. Generates boilerplate code/functions. Helps refactor & debug. Explains code.',
        agent: 'CodeGen Agent',
        type: 'GenAI Agent',
        tools: ['GitHub Copilot', 'VS Code', 'Git'],
        personas: ['Developer', 'Senior Developer']
      },
      {
        id: 'p3-a2',
        name: 'Unit Testing',
        defaultEffort: { min: 1, max: 2 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Analyzes code & user story. Auto-generates unit test cases with edge cases. Ensures coverage thresholds.',
        agent: 'TestGen Agent',
        type: 'GenAI Agent',
        tools: ['JUnit', 'Jest', 'Pytest'],
        personas: ['Developer']
      },
      {
        id: 'p3-a3',
        name: 'Code Quality / LGTM Analysis',
        defaultEffort: { min: 0.5, max: 1 },
        defaultWait:   { min: 0.5, max: 2 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Scans for code quality issues, security vulnerabilities, and best practice violations. Provides auto-fix suggestions.',
        agent: 'AI Code Quality Tools',
        type: 'AI Automation',
        tools: ['SonarQube', 'ESLint', 'Checkmarx'],
        personas: ['Developer', 'Tech Lead']
      },
      {
        id: 'p3-a4',
        name: 'Peer Code Review',
        defaultEffort: { min: 1, max: 2 },
        defaultWait:   { min: 4, max: 24 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-analyzes diffs. Comments on potential bugs, style issues, security. Summarizes changes for reviewers.',
        agent: 'ReviewAgent',
        type: 'GenAI Agent',
        tools: ['GitHub', 'Azure DevOps', 'Bitbucket'],
        personas: ['Senior Developer', 'Tech Lead']
      },
      {
        id: 'p3-a5',
        name: 'Knowledge Transfer / Documentation',
        defaultEffort: { min: 2, max: 8 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-generates READMEs, API docs, inline comments from code. Suggests knowledge base articles based on FAQs.',
        agent: 'DocGen Agent',
        type: 'GenAI Agent',
        tools: ['Confluence', 'ReadTheDocs'],
        personas: ['Developer', 'Tech Lead']
      }
    ]
  },
  {
    id: 4,
    name: 'Continuous Integration',
    defaultEffortRange: { min: 2, max: 6 },
    defaultWaitRange:   { min: 3, max: 10 },
    effortUnit: 'hours',
    waitUnit: 'hours',
    color: 'orange',
    activities: [
      {
        id: 'p4-a1',
        name: 'Build Process (CI)',
        defaultEffort: { min: 0.5, max: 1 },
        defaultWait:   { min: 1, max: 4 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Optimizes build scripts by analyzing dependencies. Suggests parallel build strategies. Identifies caching opportunities.',
        agent: 'AI Build Optimizer',
        type: 'AI Automation',
        tools: ['Jenkins', 'Azure DevOps', 'GitHub Actions'],
        personas: ['DevOps Engineer']
      },
      {
        id: 'p4-a2',
        name: 'Static Code Analysis (SAST)',
        defaultEffort: { min: 0.5, max: 1 },
        defaultWait:   { min: 1, max: 4 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'ML-powered SAST for fewer false positives. Prioritizes vulnerabilities by severity/context. Suggests fixes.',
        agent: 'AI SAST Tools',
        type: 'AI Automation',
        tools: ['Checkmarx', 'Veracode', 'SonarQube'],
        personas: ['Security Engineer', 'Developer']
      },
      {
        id: 'p4-a3',
        name: 'Artifact Creation & Registry',
        defaultEffort: { min: 0.5, max: 1 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-tags artifacts with metadata. Ensures compliance checks. Manages versioning and dependencies intelligently.',
        agent: 'AI Artifact Manager',
        type: 'AI Automation',
        tools: ['JFrog Artifactory', 'Nexus', 'ECR'],
        personas: ['DevOps Engineer']
      },
      {
        id: 'p4-a4',
        name: 'DEV Deployment',
        defaultEffort: { min: 0.5, max: 2 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-provisions DEV environment. Monitors deployment health. Rolls back on anomalies.',
        agent: 'AI Deployment Agent',
        type: 'AI Automation',
        tools: ['Kubernetes', 'Helm', 'ArgoCD'],
        personas: ['DevOps Engineer', 'Developer']
      }
    ]
  },
  {
    id: 5,
    name: 'Continuous Testing',
    defaultEffortRange: { min: 34, max: 98 },
    defaultWaitRange:   { min: 14.5, max: 41 },
    effortUnit: 'hours',
    waitUnit: 'hours',
    color: 'red',
    activities: [
      {
        id: 'p5-a1',
        name: 'Test Environment Setup',
        defaultEffort: { min: 2, max: 8 },
        defaultWait:   { min: 1, max: 4 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-provisions test environments. Configures dependencies and services. Validates readiness.',
        agent: 'AI Environment Manager',
        type: 'AI Automation',
        tools: ['Kubernetes', 'Terraform', 'Docker'],
        personas: ['DevOps Engineer', 'QA Engineer']
      },
      {
        id: 'p5-a2',
        name: 'Test Data Generation / Management',
        defaultEffort: { min: 2, max: 8 },
        defaultWait:   { min: 4, max: 16 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Generates realistic, privacy-compliant synthetic test data from schema and constraints.',
        agent: 'DataGen Agent',
        type: 'GenAI Agent',
        tools: ['Faker', 'Mockaroo', 'Informatica TDM'],
        personas: ['QA Engineer', 'Data Engineer']
      },
      {
        id: 'p5-a3',
        name: 'Build Verification Testing (BVT)',
        defaultEffort: { min: 0.5, max: 1 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Smart test selection based on code changes. Auto-generates smoke tests for new features.',
        agent: 'AI Test Selection',
        type: 'AI Automation',
        tools: ['Selenium', 'Playwright', 'Azure Test Plans'],
        personas: ['QA Engineer']
      },
      {
        id: 'p5-a4',
        name: 'Automated Component Regression',
        defaultEffort: { min: 1, max: 2 },
        defaultWait:   { min: 0.5, max: 1 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Uses Test Impact Analysis to run only relevant tests. Parallelizes execution. Predicts flaky tests.',
        agent: 'AI Test Selection',
        type: 'AI Automation',
        tools: ['Selenium Grid', 'Playwright', 'BrowserStack'],
        personas: ['QA Engineer', 'SDET']
      },
      {
        id: 'p5-a5',
        name: 'Automated Full Regression',
        defaultEffort: { min: 4, max: 12 },
        defaultWait:   { min: 1, max: 4 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-heals flaky tests. Prioritizes critical paths. Generates coverage reports with gap analysis.',
        agent: 'AI Test Execution',
        type: 'AI Automation',
        tools: ['Selenium Grid', 'TestNG', 'Extent Reports'],
        personas: ['QA Lead', 'SDET']
      },
      {
        id: 'p5-a6',
        name: 'Automated Performance Testing',
        defaultEffort: { min: 16, max: 40 },
        defaultWait:   { min: 2, max: 5 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-identifies performance regressions/bottlenecks. Correlates metrics with code changes. Suggests optimizations.',
        agent: 'AI Performance Analyzer',
        type: 'AI Automation',
        tools: ['JMeter', 'Gatling', 'k6'],
        personas: ['Performance Engineer', 'QA Lead']
      },
      {
        id: 'p5-a7',
        name: 'Dynamic Security Testing (DAST)',
        defaultEffort: { min: 2, max: 4 },
        defaultWait:   { min: 4, max: 16 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Learns app structure/behavior. Performs intelligent fuzzing. Reduces false positives.',
        agent: 'AI DAST Tools',
        type: 'AI Automation',
        tools: ['OWASP ZAP', 'Burp Suite', 'Veracode DAST'],
        personas: ['Security Engineer']
      },
      {
        id: 'p5-a8',
        name: 'Manual SIT / UAT / NF Signoff',
        defaultEffort: { min: 4, max: 8 },
        defaultWait:   { min: 2, max: 5 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Consolidates test results. Analyzes trends. Generates readiness reports with risk scores.',
        agent: 'AI UAT Assistant',
        type: 'AI Automation',
        tools: ['Azure Test Plans', 'Jira', 'TestRail'],
        personas: ['QA Lead', 'Business Analyst', 'Product Owner']
      },
      {
        id: 'p5-a9',
        name: 'Defect Triage & Management',
        defaultEffort: { min: 2, max: 8 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'hours',
        aiOpportunity: 'Auto-categorizes defects. Suggests root cause. Assigns priority. Routes to correct team.',
        agent: 'AI Defect Triage',
        type: 'AI Automation',
        tools: ['Jira', 'Azure DevOps'],
        personas: ['QA Lead', 'Developer']
      }
    ]
  },
  {
    id: 6,
    name: 'Continuous Delivery',
    defaultEffortRange: { min: 8, max: 28 },
    defaultWaitRange:   { min: 2, max: 10 },
    effortUnit: 'hours',
    waitUnit: 'days',
    color: 'teal',
    activities: [
      {
        id: 'p6-a1',
        name: 'Infrastructure as Code (IaC)',
        defaultEffort: { min: 4, max: 16 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Generates IaC templates from requirements. Validates configs. Detects drift. Suggests optimizations.',
        agent: 'IaC Agent',
        type: 'GenAI Agent',
        tools: ['Terraform', 'Pulumi', 'AWS CDK'],
        personas: ['DevOps Engineer', 'Cloud Architect']
      },
      {
        id: 'p6-a2',
        name: 'Stage Deployment (SIT/UAT/Staging)',
        defaultEffort: { min: 2, max: 4 },
        defaultWait:   { min: 0.5, max: 2 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Orchestrates multi-environment deployments. Monitors health. Auto-rollbacks on failure.',
        agent: 'AI Deployment Agent',
        type: 'AI Automation',
        tools: ['ArgoCD', 'Spinnaker', 'Azure DevOps'],
        personas: ['DevOps Engineer', 'Release Manager']
      },
      {
        id: 'p6-a3',
        name: 'Release Gates / Approvals',
        defaultEffort: { min: 1, max: 2 },
        defaultWait:   { min: 1, max: 5 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Auto-validates release criteria. Provides risk assessment. Recommends approval or delay.',
        agent: 'AI Release Manager',
        type: 'AI Automation',
        tools: ['Azure DevOps', 'ServiceNow', 'Jira'],
        personas: ['Release Manager', 'Change Advisor Board']
      },
      {
        id: 'p6-a4',
        name: 'Production Deployment',
        defaultEffort: { min: 1, max: 4 },
        defaultWait:   { min: 0.5, max: 3 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Implements blue-green/canary deployments. Monitors KPIs. Auto-scales. Rolls back on anomalies.',
        agent: 'AI Production Deploy',
        type: 'AI Automation',
        tools: ['Kubernetes', 'ArgoCD', 'AWS CodeDeploy'],
        personas: ['DevOps Engineer', 'SRE']
      },
      {
        id: 'p6-a5',
        name: 'Release Notes Generation',
        defaultEffort: { min: 0.5, max: 2 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Auto-generates release notes from commits/tickets. Formats for different audiences.',
        agent: 'ReleaseNotes Agent',
        type: 'GenAI Agent',
        tools: ['GitHub', 'Jira', 'Confluence'],
        personas: ['Release Manager', 'Product Manager']
      }
    ]
  },
  {
    id: 7,
    name: 'Monitoring & Feedback',
    defaultEffortRange: { min: 6, max: 18 },
    defaultWaitRange:   { min: 2, max: 8 },
    effortUnit: 'hours',
    waitUnit: 'days',
    color: 'cyan',
    activities: [
      {
        id: 'p7-a1',
        name: 'Application Performance Monitoring (APM)',
        defaultEffort: { min: 2, max: 4 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Auto-detects anomalies (latency, errors, resource usage). Correlates issues with deployments. Suggests root causes.',
        agent: 'AI APM (Davis AI)',
        type: 'AI Automation',
        tools: ['Dynatrace', 'Datadog', 'New Relic'],
        personas: ['SRE', 'Operations Engineer']
      },
      {
        id: 'p7-a2',
        name: 'Log Aggregation & Analysis',
        defaultEffort: { min: 1, max: 4 },
        defaultWait:   { min: 0, max: 0 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Uses NLP to parse logs. Detects patterns/anomalies. Correlates events across services.',
        agent: 'AI Log Analyzer',
        type: 'AI Automation',
        tools: ['Splunk', 'Elastic Stack', 'Datadog'],
        personas: ['Operations Engineer', 'SRE']
      },
      {
        id: 'p7-a3',
        name: 'Incident Management & RCA',
        defaultEffort: { min: 2, max: 8 },
        defaultWait:   { min: 1, max: 4 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Auto-categorizes incidents. Routes to correct team. Suggests resolution steps. Generates RCA drafts.',
        agent: 'IncidentAgent',
        type: 'GenAI Agent',
        tools: ['PagerDuty', 'ServiceNow', 'Jira Service Management'],
        personas: ['SRE', 'Operations Engineer', 'DevOps Engineer']
      },
      {
        id: 'p7-a4',
        name: 'Customer Feedback Loop',
        defaultEffort: { min: 1, max: 2 },
        defaultWait:   { min: 1, max: 4 },
        effortUnit: 'hours', waitUnit: 'days',
        aiOpportunity: 'Analyzes customer feedback (surveys, support tickets, NPS). Identifies themes. Suggests product improvements.',
        agent: 'FeedbackAgent',
        type: 'GenAI Agent',
        tools: ['Qualtrics', 'Zendesk', 'Intercom'],
        personas: ['Product Manager', 'Customer Success']
      }
    ]
  }
]

// Flat list of all activities (convenient for lookups)
export const ALL_ACTIVITIES = PDLC_PHASES.flatMap(p =>
  p.activities.map(a => ({ ...a, phaseId: p.id, phaseName: p.name }))
)

// ALM tool categories supported for integration
export const ALM_TOOLS = [
  { id: 'jira',        name: 'Jira',             logo: 'jira',    fields: ['summary', 'status', 'assignee', 'created', 'resolutiondate', 'story_points', 'cycle_time', 'lead_time'] },
  { id: 'ado',         name: 'Azure DevOps',     logo: 'ado',     fields: ['title', 'state', 'assigned_to', 'created_date', 'closed_date', 'story_points', 'cycle_time'] },
  { id: 'github',      name: 'GitHub Issues',    logo: 'github',  fields: ['title', 'state', 'assignee', 'created_at', 'closed_at'] },
  { id: 'linear',      name: 'Linear',           logo: 'linear',  fields: ['title', 'state', 'assignee', 'createdAt', 'completedAt', 'estimate'] },
  { id: 'servicenow',  name: 'ServiceNow',       logo: 'snow',    fields: ['short_description', 'state', 'assigned_to', 'opened_at', 'resolved_at'] },
  { id: 'csv',         name: 'CSV / Manual',     logo: 'csv',     fields: [] }
]

// VSM lean metrics definition
export const VSM_METRICS = [
  { key: 'processTime',    label: 'Process Time (PT)',     desc: 'Actual hands-on work time for value-adding activities',  unit: 'hours',   color: 'blue'  },
  { key: 'waitTime',       label: 'Wait Time (WT)',         desc: 'Non-value-adding time waiting for resources/approvals',  unit: 'hours',   color: 'red'   },
  { key: 'leadTime',       label: 'Lead Time (LT)',         desc: 'Total elapsed time from request to delivery',             unit: 'days',    color: 'purple'},
  { key: 'flowEfficiency', label: 'Flow Efficiency (FE)',   desc: 'PT ÷ LT × 100 — % of time that adds value',             unit: '%',       color: 'green' },
  { key: 'cycleTime',      label: 'Cycle Time (CT)',        desc: 'Time from start of work to completion per item',          unit: 'days',    color: 'orange'},
  { key: 'throughput',     label: 'Throughput',             desc: 'Number of items completed per sprint/week',               unit: 'items',   color: 'teal'  },
  { key: 'wip',            label: 'Work In Progress (WIP)', desc: 'Number of items actively being worked on',               unit: 'items',   color: 'gray'  }
]

// Future state scenario definitions
export const FUTURE_STATE_SCENARIOS = [
  {
    id: 'option-a',
    label: 'Option A',
    title: 'Augmented Human — AI as Co-pilot',
    subtitle: 'Modernize with RPA + GenAI agents assisting all PDLC personas',
    description: 'Introduce multiple AI/RPA assistants alongside every human role. Humans retain decision authority; agents accelerate and quality-check work at every step.',
    humanRoles: ['Product Manager', 'Business Analyst', 'Solution Architect', 'UX Designer', 'Developer', 'QA Engineer', 'DevOps Engineer', 'Operations'],
    aiAgents: ['AI Roadmap Assistant', 'FeatureGen Agent', 'ScenarioGen Agent', 'StoryGen Agent', 'DesignGen Agent', 'DesignDoc Agent', 'CodeGen Agent', 'TestGen Agent', 'ReviewAgent', 'DataGen Agent', 'AI SAST Tools', 'AI DAST Tools', 'AI Deployment Agent', 'AI APM', 'IncidentAgent', 'FeedbackAgent'],
    automationLevel: 40,
    color: 'blue',
    expectedImprovements: { leadTime: 40, flowEfficiency: 100, effort: 35 }
  },
  {
    id: 'option-b',
    label: 'Option B',
    title: 'Hybrid — Selective AI + Core Human Roles',
    subtitle: 'Strategic agents across PDLC + Compliance & Governance layer, key human roles in design/dev/test',
    description: 'Deploy AI agents in high-impact phases (testing, CI/CD, monitoring) while retaining core human roles for design, development, and product decisions. Adds 5 Compliance & Governance agents: Secure-by-Design Architect, Compliance-as-Code Orchestrator, Model Risk Management (MRM) Agent, Telemetry & Observability Sentinel, and Multi-Agent Governance Controller — ensuring every agent operates within regulatory guardrails (GDPR, DORA, Basel III).',
    humanRoles: ['Product Owner', 'Tech Lead / Architect', 'Developer', 'QA Lead', 'DevOps Engineer'],
    aiAgents: ['FeatureGen Agent', 'CodeGen Agent', 'TestGen Agent', 'AI Test Execution', 'AI Deployment Agent', 'AI APM', 'IncidentAgent', 'Secure-by-Design Architect', 'Compliance-as-Code Orchestrator', 'MRM Agent', 'Telemetry & Observability Sentinel', 'Multi-Agent Governance Controller'],
    automationLevel: 65,
    color: 'purple',
    expectedImprovements: { leadTime: 55, flowEfficiency: 175, effort: 55 }
  },
  {
    id: 'option-c',
    label: 'Option C',
    title: 'ADLC — AI-Driven Lifecycle (BMAD Approach)',
    subtitle: 'Product Definer + Product Builder supervise full agent orchestration with embedded governance',
    description: 'The AI-Driven Lifecycle (ADLC) model built on the BMAD (Build, Measure, Automate, Deploy) approach. Only two human roles: Product Definer sets vision & OKRs, Product Builder supervises the agent orchestration layer and holds the production approval gate. Near-zero wait time — agents operate 24/7 with no human queues. At full autonomy, the MRM Agent and Multi-Agent Governance Controller become critical control points: the MRM Agent enforces AI model explainability and triggers kill-switches for drift, while the Governance Controller ensures no single agent can bypass enterprise compliance protocols.',
    humanRoles: ['Product Definer', 'Product Builder'],
    aiAgents: ['FeatureGen Agent', 'ScenarioGen Agent', 'StoryGen Agent', 'AI Architecture Advisor', 'DesignGen Agent', 'DesignDoc Agent', 'CodeGen Agent', 'TestGen Agent', 'ReviewAgent', 'AI Code Quality Tools', 'AI Build Optimizer', 'AI SAST Tools', 'AI Artifact Manager', 'AI Deployment Agent', 'AI Environment Manager', 'DataGen Agent', 'AI Test Execution', 'AI Performance Analyzer', 'AI DAST Tools', 'AI UAT Assistant', 'IaC Agent', 'AI Production Deploy', 'AI Release Manager', 'ReleaseNotes Agent', 'AI APM (Davis AI)', 'AI Log Analyzer', 'IncidentAgent', 'FeedbackAgent', 'Secure-by-Design Architect', 'Compliance-as-Code Orchestrator', 'MRM Agent (kill-switch)', 'Telemetry & Observability Sentinel', 'Multi-Agent Governance Controller'],
    automationLevel: 92,
    color: 'emerald',
    expectedImprovements: { leadTime: 85, flowEfficiency: 650, effort: 92 }
  }
]
