# PDLC VSM Platform — Technical Architecture
**Version 1.0 · May 2026 · Cognizant Engineering Effectiveness Practice**

---

## Table of Contents

1. [Architecture Principles](#1-architecture-principles)
2. [System Context (C4 Level 1)](#2-system-context-c4-level-1)
3. [Container Diagram (C4 Level 2)](#3-container-diagram-c4-level-2)
4. [Component Diagram (C4 Level 3)](#4-component-diagram-c4-level-3)
5. [Data Architecture](#5-data-architecture)
6. [LangGraph Pipeline Architecture](#6-langgraph-pipeline-architecture)
7. [Infrastructure Architecture](#7-infrastructure-architecture)
8. [Network & Security Architecture](#8-network--security-architecture)
9. [Integration Architecture](#9-integration-architecture)
10. [Technology Stack Reference](#10-technology-stack-reference)
11. [Architecture Decisions Record](#11-architecture-decisions-record)

---

## 1. Architecture Principles

| # | Principle | Implication |
|---|---|---|
| P1 | **Secure by default** | Every endpoint authenticated in production; secrets in Azure Key Vault; no LLM keys in source |
| P2 | **Stateless API** | Pipeline runs are referenced by run_id; FastAPI workers are interchangeable |
| P3 | **Idempotent pipeline** | Re-running the analysis pipeline on the same VSM snapshot must produce comparable results; randomness is fenced to LLM temperature (0.2) |
| P4 | **Audit everything** | Every pipeline run logs its inputs (project_id, snapshot version), the agent chain, and timing for each node |
| P5 | **Fail gracefully** | LLM unavailability falls back to rule-based outputs; partial-state preservation on agent failure; never block the API on a stuck pipeline |
| P6 | **Observable by design** | Structured JSON logs, distributed traces over async boundaries, run-level dashboards from day one |
| P7 | **Progressive enhancement** | Phase 1 ships as a FastAPI monolith with in-process LangGraph; agent-orchestration extraction deferred to Phase 3 |
| P8 | **Domain knowledge owns the model** | The 7-phase × 36-activity PDLC taxonomy and DORA cut-offs live in `pdlc_data.py` and are versioned; LLM outputs are validated against this canonical structure |
| P9 | **RAG-grounded generation** | All agent prompts are augmented with retrieval from the embedded knowledge base; ungrounded hallucinations are rejected by the accuracy scorer |

---

## 2. System Context (C4 Level 1)

```
                        ┌───────────────────────────────────────────────────┐
                        │              Enterprise Network                    │
                        │                                                    │
   ┌──────────────┐     │   ┌─────────────────────────────────────────────┐ │
   │ Engineering  │─────┼──▶│                                             │ │
   │ Lead         │     │   │           PDLC VSM Platform                 │ │
   │ Analyst      │     │   │                                             │ │
   │ Platform Adm │     │   │  7-phase × 36-activity value stream model;  │ │
   │ Viewer       │     │   │  AI-assisted bottleneck analysis;           │ │
   └──────────────┘     │   │  3-scenario future-state design;            │ │
         │              │   │  ROI-quantified business cases              │ │
         │ HTTPS        │   └───────────┬─────────────────────────────────┘ │
         ▼              │               │                                   │
   ┌──────────────┐     │               │ REST                              │
   │  Azure Entra │◀────┼───────────────┘ + Bearer JWT                      │
   │  ID (IdP)    │     │               │                                   │
   └──────────────┘     │               ▼                                   │
                        │   ┌───────────────────────────────────────────┐  │
                        │   │           Source Systems (ALM)             │  │
                        │   │                                           │  │
                        │   │  ┌─────────┐  ┌─────────┐  ┌──────────┐ │  │
                        │   │  │  Jira   │  │  Azure  │  │  GitHub  │ │  │
                        │   │  │         │  │  DevOps │  │          │ │  │
                        │   │  └─────────┘  └─────────┘  └──────────┘ │  │
                        │   │                                           │  │
                        │   │  ┌─────────┐  ┌──────────┐               │  │
                        │   │  │ Linear  │  │ServiceNow│  ...           │  │
                        │   │  └─────────┘  └──────────┘               │  │
                        │   └───────────────────────────────────────────┘  │
                        │                                                    │
                        │   ┌───────────────────────────────────────────┐  │
                        │   │           LLM Provider                     │  │
                        │   │                                           │  │
                        │   │  ┌─────────────────────┐                  │  │
                        │   │  │  Azure OpenAI       │ ← primary        │  │
                        │   │  │  gpt-4o, gpt-4o-mini│                  │  │
                        │   │  └─────────────────────┘                  │  │
                        │   │                                           │  │
                        │   │  ┌─────────────────────┐                  │  │
                        │   │  │  OpenAI (fallback)  │                  │  │
                        │   │  └─────────────────────┘                  │  │
                        │   └───────────────────────────────────────────┘  │
                        │                                                    │
                        └───────────────────────────────────────────────────┘
```

**Actors:**

| Actor | Description | Role |
|---|---|---|
| Platform Admin | Engineering Effectiveness lead; manages projects, scheduling, LLM config | Full read/write, admin |
| Engineering Lead | Head of delivery for a portfolio or product group | Own-portfolio read/write, gate on initiatives |
| Analyst | Transformation analyst, consultant, or DevOps practitioner | Read all; submit/edit VSM, run pipeline, score maturity |
| Viewer | Executive sponsor, auditor | Read-only access to dashboards and reports |
| Azure Entra ID | Enterprise identity provider | Issues OIDC tokens; group-based role mapping |
| Jira / ADO / GitHub / Linear / ServiceNow | ALM source systems | Issue and work-item providers; pulled-only (no writes) |
| Azure OpenAI | Primary LLM provider | gpt-4o deployment for agent inference |
| OpenAI | Fallback LLM provider | gpt-4o-mini for environments without Azure access |

---

## 3. Container Diagram (C4 Level 2)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  PDLC VSM Platform — Azure-hosted Production System                           │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  FRONTEND CONTAINER                                                      │ │
│  │  React 18 + Vite 5 + TailwindCSS                                        │ │
│  │  Azure Static Web Apps — CDN-backed, managed SSL                        │ │
│  │  https://pdlc-vsm.internal                                              │ │
│  │                                                                          │ │
│  │  • 24 page modules (SPA, React Router 6)                                │ │
│  │  • MSAL React — Entra ID OIDC token acquisition                        │ │
│  │  • TanStack React Query — API response caching                          │ │
│  │  • Recharts + Chart.js — VSM, DORA, maturity visualisations             │ │
│  │  • xlsx — Excel export of analyses                                      │ │
│  │  • All API calls proxied via Bearer JWT                                 │ │
│  └──────────────────────────────┬───────────────────────────────────────────┘ │
│                                 │ HTTPS / Bearer JWT                           │
│  ┌──────────────────────────────▼───────────────────────────────────────────┐ │
│  │  API CONTAINER                                                            │ │
│  │  Python 3.13 + FastAPI 0.115 + Uvicorn (uvloop)                          │ │
│  │  Azure App Service (B2, Linux) — containerised (Docker)                 │ │
│  │  Port 8001 (internal)                                                    │ │
│  │                                                                          │ │
│  │  Middleware chain:                                                        │ │
│  │  TrustedHostMiddleware → CORSMiddleware → SessionMiddleware →            │ │
│  │  AuthBearerMiddleware → RBACDependency → Pydantic validation →           │ │
│  │  route handler → ExceptionHandler                                        │ │
│  │                                                                          │ │
│  │  9 route modules + /api/v1/health + /api/v1/openapi.json                │ │
│  │  Async background pipeline (FastAPI BackgroundTasks + LangGraph)         │ │
│  │  Scheduled pipeline runs (APScheduler, configurable cadence)            │ │
│  └────┬──────────────┬──────────────────────────────────┬───────────────────┘ │
│       │              │                                  │                      │
│       │ asyncpg      │ in-process                       │ HTTP                 │
│       ▼              ▼                                  ▼                      │
│  ┌──────────┐  ┌───────────────┐              ┌────────────────────────────┐ │
│  │PostgreSQL│  │ LangGraph     │              │ External Adapters           │ │
│  │Flexible  │  │ Orchestrator  │              │ Jira / ADO / GitHub /       │ │
│  │Server 16 │  │ + 8 agents    │              │ Linear / ServiceNow / CSV   │ │
│  │          │  │ + RAG engine  │              │ + Azure OpenAI / OpenAI     │ │
│  │Primary   │  │ + KB corpus   │              │ circuit-breaker + retry     │ │
│  │+ Replica │  │ (in-memory)   │              └────────────────────────────┘ │
│  └──────────┘  └───────────────┘                                              │
│                                               ┌────────────────────────────┐ │
│                                               │ Azure Key Vault             │ │
│                                               │ DATABASE_URL                │ │
│                                               │ AZURE_OPENAI_API_KEY        │ │
│                                               │ JIRA_API_TOKEN              │ │
│                                               │ ADO_PERSONAL_ACCESS_TOKEN   │ │
│                                               │ APPINSIGHTS_CONNECTION_STR  │ │
│                                               └────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  OBSERVABILITY                                                           │ │
│  │  Azure Application Insights (OpenTelemetry SDK) + Log Analytics         │ │
│  │  + Azure Monitor Alert Rules                                            │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Diagram (C4 Level 3)

### 4.1 API Container — Internal Components

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  backend/main.py — FastAPI Application Bootstrap                              │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  MIDDLEWARE LAYER (applied globally, in order)                           │ │
│  │                                                                          │ │
│  │  [1] TrustedHostMiddleware  — allowed hosts list                        │ │
│  │  [2] CORSMiddleware         — CORS_ORIGINS env var; preflight handling  │ │
│  │  [3] SessionMiddleware      — signed session cookie (for SSE channels)  │ │
│  │  [4] AuthBearerMiddleware   — JWT validation against Entra ID JWKS      │ │
│  │  [5] RBACDependency         — maps group claims → role → request.state  │ │
│  │  [6] structured_logger      — JSON request/response logging via loguru  │ │
│  │  [7] FastAPI Pydantic       — request body validation per route         │ │
│  │  [8] ExceptionHandler       — uniform error envelope (4xx/5xx)          │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  ROUTE LAYER (/api/v1/...)                                               │ │
│  │                                                                          │ │
│  │  projects             → backend/routers/projects.py                     │ │
│  │  vsm                  → backend/routers/vsm.py                          │ │
│  │  analysis             → backend/routers/analysis.py                     │ │
│  │  agents               → backend/routers/agents.py                       │ │
│  │  accuracy             → backend/routers/accuracy.py                     │ │
│  │  alm                  → backend/routers/alm.py                          │ │
│  │  devops-maturity      → backend/routers/devops_maturity.py              │ │
│  │  settings             → backend/routers/settings_router.py              │ │
│  │  health               → backend/routers/health.py                       │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  AGENT LAYER (backend/agents/)                                           │ │
│  │                                                                          │ │
│  │  orchestrator/graph.py     LangGraph StateGraph(VSMAgentState)          │ │
│  │                            run_full_analysis() entrypoint                │ │
│  │  alm_connector/agent.py    Fetches ALM data; maps to VSM input          │ │
│  │  vsm_analyzer/agent.py     Computes lean VSM metrics + DORA calibration │ │
│  │  benchmark_agent/agent.py  Loads industry benchmarks per industry tag   │ │
│  │  bottleneck_analyzer/      Identifies waste; root-cause analysis        │ │
│  │  improvement_generator/    Generates ROI-ranked improvement actions     │ │
│  │  future_state_designer/    Models 3 scenarios: option-a/b/c             │ │
│  │  business_case_builder/    Financial model + payback per scenario       │ │
│  │  playbook_contextualizer/  Generates implementation playbook            │ │
│  │  devops_maturity_agent/    Scores 73-question assessment                │ │
│  │                                                                          │ │
│  │  llm.py            Azure OpenAI / OpenAI factory (lru_cache)            │ │
│  │  rag_engine.py     BM25 over TF-IDF tokenised KB corpus                 │ │
│  │  knowledge_base.py 100+ docs across 4 categories (in-memory)            │ │
│  │  state.py          VSMAgentState TypedDict (20 fields)                  │ │
│  │  pdlc_data.py      Canonical 7-phase × 36-activity model + benchmarks   │ │
│  │  accuracy_scorer.py Validates agent outputs against PDLC domain rules   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  CROSS-CUTTING CONCERNS                                                  │ │
│  │                                                                          │ │
│  │  backend/database/db.py    asyncpg engine + AsyncSession factory        │ │
│  │  backend/core/config.py    Pydantic Settings (env + .env)               │ │
│  │  backend/models/*.py       SQLAlchemy declarative models                │ │
│  │  backend/utils/audit.py    write_audit_log(...) helper                  │ │
│  │  backend/utils/scheduler.py APScheduler instance + cron triggers        │ │
│  │  backend/utils/notify.py   Teams webhook + email dispatcher (Phase 2)   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Frontend Container — Internal Components

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  React 18 SPA                                                                 │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  BOOTSTRAP LAYER                                                         │ │
│  │  src/main.jsx  — MsalProvider → QueryClientProvider → App               │ │
│  │  src/App.jsx   — AuthenticatedTemplate → Layout → React Router          │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌──────────────────────────────┐  ┌──────────────────────────────────────┐  │
│  │  LAYOUT COMPONENTS           │  │  CONTEXT PROVIDERS                   │  │
│  │  Layout.jsx — app shell      │  │  ProjectContext — current project    │  │
│  │  Sidebar.jsx — nav + project │  │  (localStorage 'pdlc_project_id')    │  │
│  │  selector                    │  │  RunContext — latest run state       │  │
│  └──────────────────────────────┘  └──────────────────────────────────────┘  │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  PAGE MODULES (24 routes, React.lazy code-split per route)              │ │
│  │                                                                          │ │
│  │  ONBOARDING & DATA              ANALYSIS RESULTS                        │ │
│  │  /              Dashboard        /bottlenecks    BottlenecksPage         │ │
│  │  /alm-connect   ALMConnect       /improvements   ImprovementsPage        │ │
│  │  /current-vsm   CurrentVSM       /future-state   FutureStatePage         │ │
│  │  /vsm-editor    VSMEditor        /business-case  BusinessCasePage        │ │
│  │                                  /recommendations RecommendationsPage    │ │
│  │  MATURITY                                                                │ │
│  │  /devops-maturity DevOpsMaturity AGENTS & QUALITY                       │ │
│  │  /dora-assessment DORAAssessment /agents         AgentsPage              │ │
│  │  /transformation-readiness                       /accuracy-score Accuracy│ │
│  │                                  /playbook-context PlaybookContext      │ │
│  │  PRACTITIONER CONTENT                                                    │ │
│  │  /governance         Governance  CONFIGURATION                          │ │
│  │  /ops-intel          OpsIntel    /settings        Settings              │ │
│  │  /legacy-modernise   LegacyMod                                          │ │
│  │  /ai-assurance       AIAssurance ROLES / EDUCATION                      │ │
│  │  /glossary           Glossary    /roles-slides    RolesSlides           │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  SHARED COMPONENTS                                                       │ │
│  │  VSMGrid.jsx        — 7-phase × 36-activity grid with PT/WT cells       │ │
│  │  PhaseDrawer.jsx    — drill-down panel for one phase                    │ │
│  │  ScenarioCompare.jsx— option-a vs option-b vs option-c comparison       │ │
│  │  ROIChart.jsx       — payback timeline visualisation                    │ │
│  │  charts/            — Recharts + Chart.js wrappers                      │ │
│  │  ui/                — buttons, cards, badges, modals                    │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  API CLIENT LAYER                                                        │ │
│  │  axios instance — baseURL: VITE_API_BASE_URL                            │ │
│  │  Interceptor: attach Bearer token from MSAL on every request           │ │
│  │  axios-retry: 3 retries on 5xx/network errors, exponential backoff     │ │
│  │  TanStack React Query: staleTime 30s; refetchOnWindowFocus             │ │
│  │  Run-polling hook: useRunStatus(run_id) → polls /agents/status/{id}    │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Architecture

### 5.1 Entity Relationship Overview

```
                         ┌──────────────┐
                         │    users     │
                         │ (Entra sync) │
                         └──────┬───────┘
                                │ created_by / updated_by
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   ┌──────────────┐    1:M    ┌──────────────────┐                       │
│   │   projects   │──────────▶│  vsm_snapshots   │  (source: alm/manual/ │
│   │              │           │                  │   sample; immutable    │
│   │ org →        │           │  raw_data JSON   │   except overrides)   │
│   │ portfolio →  │           │  vsm_data JSON   │                       │
│   │ product →    │           │  summary JSON    │                       │
│   │ team         │           └──────────────────┘                       │
│   │              │    1:M    ┌──────────────────┐                       │
│   │ industry     │──────────▶│ analysis_runs    │  (LangGraph results)  │
│   │ alm_tool     │           │  status, result  │                       │
│   │ alm_config   │           │  agents_run JSON │                       │
│   │              │           └──────────────────┘                       │
│   │              │    1:M    ┌────────────────────┐                     │
│   │              │──────────▶│ activity_metrics   │  (per-activity      │
│   │              │           │ phase×activity     │   time series)      │
│   │              │           └────────────────────┘                     │
│   │              │    1:M    ┌──────────────────────┐                   │
│   │              │──────────▶│ devops_assessments   │  (maturity scores) │
│   │              │           └──────────┬───────────┘                   │
│   └──────────────┘                      │ 1:M                           │
│                                         ▼                               │
│                                  ┌─────────────────────────┐            │
│                                  │ assessment_action_items │            │
│                                  │  dimension, competency  │            │
│                                  │  priority, status       │            │
│                                  └─────────────────────────┘            │
│                                                                          │
│   ┌─────────────────────────┐     ┌──────────────────────────┐         │
│   │ platform_settings       │     │ scheduled_pipeline_runs  │         │
│   │ key → value (JSON)      │     │ project_id, trigger      │         │
│   │ (LLM cfg, ALM creds,    │     │ status, result_run_id    │         │
│   │  schedule cfg)          │     └──────────────────────────┘         │
│   └─────────────────────────┘                                          │
│                                                                          │
│   ┌──────────────┐     ┌──────────────────────┐                        │
│   │  audit_log   │     │  users / identity    │                        │
│   │  (immutable; │     │  (Entra sync;        │                        │
│   │   Phase 2)   │     │   Phase 2)           │                        │
│   └──────────────┘     └──────────────────────┘                        │
└──────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Core Entity: `analysis_runs` — Status Lifecycle

```
                    ┌─────────────┐
                    │   pending   │  (row created, bg task not yet started)
                    └──────┬──────┘
                           │ BackgroundTasks queue picks up
                           ▼
                    ┌─────────────┐
                    │   running   │  (orchestrator iterating LangGraph nodes)
                    └──────┬──────┘
                           │ node-by-node, updates agents_run[]
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
             ┌──────────┐  ┌──────────────────────┐
             │ complete │  │  failed              │
             │ result   │  │  error preserves     │
             │ JSON     │  │  partial state +     │
             │ populated│  │  exception text      │
             └──────────┘  └──────────────────────┘
                  │                  │
                  ▼                  ▼
            S2 reads via       Operator inspects
            /analysis/...      via /agents/history
```

### 5.3 PDLC Domain Model

```
7 Phases × 36 Activities — canonical taxonomy in pdlc_data.py

Phase 1 — Backlog & Roadmap                     (5 activities)
  Portfolio Epic, Product Roadmap, Feature Definition,
  BDD Scenario Writing, User Story Creation

Phase 2 — Architecture & UX Design              (4 activities)
  Technical Design, UX Design, Architecture Review, Story Refinement

Phase 3 — Code Management                       (5 activities)
  Branch Creation, Code Authoring, Peer Code Review,
  Merge to Main, Tagging

Phase 4 — Continuous Integration                (4 activities)
  Build, Dependency Resolution, Unit Test, Static Analysis

Phase 5 — Continuous Testing                    (9 activities)
  Env Provisioning, Test Data, Smoke, Functional,
  API/Contract, Performance, Security, UAT, Regression

Phase 6 — Continuous Delivery                   (5 activities)
  CAB Approval, Release Notes, Deploy to Stage,
  Production Deploy, Post-Deploy Smoke

Phase 7 — Monitoring & Feedback                 (4 activities)
  MTTD, Incident Triage, Customer Feedback, Retro

Each activity carries:
  effort (min/max hours), wait (min/max), unit, agent_name, type
  industry-benchmark p50 PT, p50 WT, p75 FE
```

### 5.4 Maturity Domain Structure

```
73 Questions × 4 Dimensions — canonical taxonomy in devops_maturity_questions.py

CULTURAL   (9 questions)
  Team Collaboration, Psychological Safety, Continuous Learning,
  Experimentation Culture, Leadership Sponsorship, Cross-functional
  Alignment, Blameless Post-mortems, Innovation Time, Career Growth

MEASUREMENT (11 questions)
  DORA Metrics, VSM Metrics, Customer Value Metrics, Engineering Health,
  Cost Awareness, SLA/SLO Coverage, Operational Telemetry,
  Quality Telemetry, Adoption Telemetry, Cost Telemetry, Productivity Index

PROCESS    (9 questions)
  Story Decomposition, WIP Limits, Retrospective Cadence, Backlog Hygiene,
  Definition of Done, Pair/Mob Programming, Code-Review SLA,
  Release Cadence, Hotfix Procedure

TECHNICAL  (14 questions)
  Trunk-based Dev, Feature Flag Coverage, Test Pyramid Shape,
  Observability Stack, Infrastructure as Code, Container Adoption,
  Container Orchestration, Database Change Management, Secrets Mgmt,
  Vulnerability Scanning, Dependency Management, Cloud Maturity,
  Build Cache Strategy, Branch Protection
```

### 5.5 Data Flow — Pipeline Run

```
POST /api/v1/agents/run-analysis/{project_id}

  ├── Persist analysis_runs row (status=pending)
  ├── Close DB session
  ├── BackgroundTasks queue → orchestrator.run_full_analysis
  └── Return 202 {run_id, status:'started'}

In background:
  status → running

  alm_connector node:
    └── ALMConfig from project.alm_config
        ├── adapter.fetch(config)            (or use uploaded CSV)
        └── _map_to_vsm(raw_data)            → VSMAgentState.vsm_data

  vsm_analyzer node:
    └── compute PT, WT, LT, FE per phase & aggregate
        _apply_dora_calibration()
        _estimate_deployment_freq()
        _estimate_cfr()                       → VSMAgentState.metrics

  benchmark_agent node:
    └── load DORA_ELITE / LEAN_VSM_TARGETS by industry
                                              → VSMAgentState.benchmarks

  bottleneck_analyzer node:
    └── for each phase: compare metrics vs benchmark
        LLM: root-cause analysis grounded by RAG retrieval
                                              → VSMAgentState.bottlenecks

  improvement_generator node:
    └── for each bottleneck: lookup IMPROVEMENT_CATALOGUE
        LLM: contextualise to team domain
                                              → VSMAgentState.improvements

  future_state_designer node:
    └── for option-a / option-b / option-c:
        apply scenario template + LLM contextualisation
                                              → VSMAgentState.future_states

  business_case_builder node:
    └── load BUSINESS_CASES per scenario
        compute investment_range, ROI, payback
                                              → VSMAgentState.business_cases

  status → complete
  result column ← {bottlenecks, improvements, future_states, business_cases}
```

### 5.6 Read vs Write Separation

| Operation | Database | Caching |
|---|---|---|
| Dashboard summary | Read replica | In-process LRU 60s TTL (Phase 1); Redis 60s TTL (Phase 2) |
| Latest VSM snapshot | Read replica | None — snapshot row is small |
| Analysis run result | Read replica | None — read once per session |
| All writes (snapshots, runs, assessments) | Primary | N/A |
| Scheduled pipeline tick | Primary | Reads platform_settings per tick |
| LLM call cost telemetry | Primary | Aggregated per run in `analysis_runs.result.cost` |

---

## 6. LangGraph Pipeline Architecture

### 6.1 Graph Topology

```
             ┌─────────────────┐
             │  alm_connector  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │  vsm_analyzer   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ benchmark_agent │
             └────────┬────────┘
                      │
                      ▼
             ┌────────────────────┐
             │ bottleneck_analyzer│
             └────────┬───────────┘
                      │
                      ▼
             ┌──────────────────────┐
             │ improvement_generator│
             └────────┬─────────────┘
                      │
                      ▼
             ┌────────────────────────┐
             │ future_state_designer  │  (option-a, option-b, option-c)
             └────────┬───────────────┘
                      │
                      ▼
             ┌──────────────────────┐
             │ business_case_builder│
             └────────┬─────────────┘
                      │
                      ▼
                    [END]
```

**Standalone-invocable agents** (out-of-band of the main pipeline):
- `playbook_contextualizer` — invoked from `POST /agents/contextualise-playbook/{project_id}` with team_context + analysis_context
- `devops_maturity_agent` — invoked from `POST /devops-maturity/assessments/{id}/run`

### 6.2 Shared State — `VSMAgentState`

```python
class VSMAgentState(TypedDict):
    # Inputs
    project_id: str
    project: dict                  # org/portfolio/team metadata
    alm_raw_data: dict             # raw payload from ALM adapter
    overrides: dict                # human overrides on VSM
    # Pipeline outputs (filled progressively)
    vsm_data: dict                 # 7 phases × 36 activities
    benchmarks: dict               # industry benchmarks
    metrics: dict                  # PT/WT/LT/FE aggregates + DORA
    bottlenecks: list[dict]
    improvements: list[dict]
    future_states: dict            # keyed by option-a/b/c
    business_cases: dict           # keyed by scenario
    recommendations: list[dict]    # cross-cutting actions
    dora_calibration: dict
    # Meta
    errors: list[str]
    run_id: str
    status: str
```

Each node returns a partial state dict that LangGraph merges into the shared state. Errors are accumulated but do not abort the graph by default — the orchestrator decides per-node whether failure is terminal (e.g., `vsm_analyzer` failure aborts; `benchmark_agent` failure logs and continues with empty benchmarks).

### 6.3 LLM Provider Chain

```python
def get_llm():
    if settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT:
        return AzureChatOpenAI(
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,   # gpt-4o
            api_version=settings.AZURE_OPENAI_API_VERSION,       # 2024-02-15-preview
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            temperature=0.2,
            max_tokens=4096,
        )
    if settings.OPENAI_API_KEY:
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,                          # gpt-4o-mini
            api_key=settings.OPENAI_API_KEY,
            temperature=0.2,
            max_tokens=4096,
        )
    return None   # signals rule-based fallback path
```

The factory is wrapped in `lru_cache` so repeated agent calls within a process reuse the same client (and the HTTP connection pool inside it).

### 6.4 RAG Engine

```
backend/agents/rag_engine.py

Index construction (lazy, once per process):
  - Tokenise each KB doc (lowercase, strip punctuation, drop stopwords)
  - Compute term-frequency per doc; build inverted index
  - Compute IDF over the corpus
  - Persist the index in module-level state

Retrieval:
  retrieve(query, top_k=5, category=None)
    - Tokenise query
    - For each candidate doc, compute BM25 score (k1=1.5, b=0.75)
    - Apply category filter if provided
    - Return top-k docs with scores

Agent integration:
  retrieve_for_agent(agent_name, context, top_k=4)
    - Agent-specific query templating
    - Calls retrieve() with category filter mapped from agent_name
  build_rag_context(agent_name, context, max_chars=2000)
    - Truncates retrieval to budget; formats as prompt header
```

No external vector database. The corpus is ~150KB of curated content (DORA benchmarks, lean VSM, transformation patterns, tool integration) and BM25 produces stable, explainable retrieval for this size. Migration to pgvector or Azure AI Search is on the Phase 2 roadmap when corpus growth exceeds 5MB.

### 6.5 Accuracy Scoring

```
For each completed run:

  Schema adherence       — every required field populated; types match
  PDLC ID validity       — phaseId ∈ [1,7]; activityId in canonical list
  Numerical bounds       — FE ∈ [0,100]; PT/WT ≥ 0; ROI ≥ 1.0
  RAG hit quality        — did the agent's top-4 retrieved docs match
                           the expected category for its task?
  Domain coherence       — sum(futureFE) > sum(currentFE) for at least 5/7 phases
  Business-case sanity   — payback_months between 3 and 60
                           investment_range["min"] < ["max"]

Score = weighted average of the above ∈ [0, 100]
Threshold for "production-grade": ≥ 80
```

The scorer is invoked automatically post-run and the score appears in `analysis_runs.result.accuracy_score`. Runs below threshold are flagged in the UI for human review before the result is exported.

---

## 7. Infrastructure Architecture

### 7.1 Azure Resource Layout

```
Azure Subscription: Engineering Effectiveness
│
└── Resource Group: rg-pdlc-vsm-prod  (East US 2)
    │
    ├── Compute
    │   ├── App Service Plan: asp-pdlc-vsm-prod (B2, Linux, 2 vCPU, 3.5GB)
    │   │   ├── App Service: app-pdlc-vsm-api          [Production slot]
    │   │   └── App Service: app-pdlc-vsm-api/staging  [Staging slot — swap for deploy]
    │   └── Static Web App: stapp-pdlc-vsm-frontend    [CDN-backed, global PoPs]
    │
    ├── Data
    │   ├── PostgreSQL Flexible Server: psql-pdlc-vsm-prod
    │   │   ├── Primary  (4 vCore, 16GB, 128GB storage, General Purpose)
    │   │   ├── Read Replica: psql-pdlc-vsm-read (East US 2)
    │   │   └── Backup: automated PITR, 7-day retention
    │   └── (Optional Phase 2) Azure Cache for Redis: redis-pdlc-vsm-prod
    │
    ├── AI
    │   └── Azure OpenAI: aoai-pdlc-vsm-prod
    │       ├── Deployment: gpt-4o          (capacity: 30K TPM)
    │       └── Deployment: gpt-4o-mini     (capacity: 60K TPM, used for accuracy scoring)
    │
    ├── Security
    │   ├── Key Vault: kv-pdlc-vsm-prod
    │   │   ├── SECRET: DATABASE-URL
    │   │   ├── SECRET: AZURE-OPENAI-API-KEY
    │   │   ├── SECRET: OPENAI-API-KEY            (fallback)
    │   │   ├── SECRET: JIRA-API-TOKEN
    │   │   ├── SECRET: ADO-PERSONAL-ACCESS-TOKEN
    │   │   └── SECRET: APPINSIGHTS-CONNECTION-STRING
    │   ├── Managed Identity (system-assigned): app-pdlc-vsm-api → kv-pdlc-vsm-prod
    │   └── Azure Entra ID: App Registration (PDLC VSM Platform)
    │
    ├── Containers
    │   └── Azure Container Registry: acr-pdlc-vsm-prod
    │       ├── api:latest        (python:3.13-slim multi-stage)
    │       └── api:{git-sha}     (tagged per deploy)
    │
    └── Observability
        ├── Application Insights: appi-pdlc-vsm-prod
        ├── Log Analytics Workspace: law-pdlc-vsm-prod
        └── Azure Monitor Alert Rules (see PRODUCTION_READINESS.md §11)
```

### 7.2 Deployment Flow

```
Developer pushes to main branch
        │
        ▼
GitHub Actions CI pipeline
        │
        ├── [1] pip install + pytest              (unit + integration tests)
        ├── [2] ruff + mypy                       (lint + type check)
        ├── [3] docker build → ACR push (api:{sha})
        ├── [4] npm ci && npm run build           (Vite → dist/)
        └── [5] Deploy to staging slot
                │
                ▼
        Smoke tests against staging
        GET /api/v1/health → 200
        POST /api/v1/agents/seed-result/{demo} → 201
        GET /api/v1/analysis/{demo}/bottlenecks → 200 with payload
                │
                ▼
        Manual approval gate (GitHub environment protection)
                │
                ▼
        az webapp deployment slot swap
        staging ⟷ production (zero-downtime)
                │
                ▼
        Production live — Application Insights confirms healthy
```

### 7.3 Auto-Scaling Policy

```
App Service Plan: asp-pdlc-vsm-prod
  Scale out rule:  CPU avg > 70% over 10 min → add 1 instance (max 4)
                   OR queue depth (active runs) > 5 → add 1 instance
  Scale in rule:   CPU avg < 30% AND queue depth = 0 over 20 min → remove 1 (min 1)

PostgreSQL Flexible Server:
  No auto-scale (manual tier upgrade path)
  Read replica handles dashboard/analysis-read load

Azure OpenAI:
  PTU (provisioned throughput units) for gpt-4o sized for 5 concurrent runs
  Standard PAYG fallback when PTU bursts above quota
  Monitor: tokens_per_minute, error_rate; alert on rate-limit responses
```

---

## 8. Network & Security Architecture

### 8.1 Traffic Flow

```
Internet
    │
    │ HTTPS (TLS 1.3)
    ▼
Azure Static Web Apps (CDN)              ← Frontend assets
    │
    │ HTTPS API calls with Bearer JWT
    ▼
Azure App Service (HTTPS endpoint)       ← API
    │ Inbound: HTTPS 443 only
    │ Outbound: PostgreSQL 5432, Azure OpenAI 443, Key Vault 443,
    │          ALM platform APIs 443
    ▼
Azure Virtual Network (Phase 2)
    ├── PostgreSQL Flexible Server       ← Private endpoint
    ├── Azure OpenAI                     ← Private endpoint
    └── Key Vault                        ← Private endpoint
```

### 8.2 Authentication Flow

```
Step 1 — User opens https://pdlc-vsm.internal
  → MSAL React: AuthenticatedTemplate requires authentication
  → Redirect to Azure Entra ID login page (tenant)
  → User authenticates (MFA enforced by tenant policy)
  → Entra ID issues access_token (JWT, 1-hour TTL) + refresh_token

Step 2 — React frontend makes API call
  → MSAL acquireTokenSilent() fetches valid token from cache
  → Axios interceptor attaches: Authorization: Bearer {access_token}
  → Request sent to App Service

Step 3 — API validates token
  → AuthBearerMiddleware (fastapi-azure-auth)
  → Downloads JWKS from Entra ID (cached)
  → Validates JWT signature, expiry, audience, issuer
  → Extracts claims: oid (user ID), email, groups (Entra group IDs)

Step 4 — RBAC dependency
  → Maps group IDs to roles:
    GROUP_PLATFORM_ADMIN   → role: 'platform_admin'
    GROUP_ENG_LEADS        → role: 'engineering_lead'
    GROUP_ANALYSTS         → role: 'analyst'
    (all authenticated)    → role: 'viewer' (fallback)
  → Sets request.state.user = {id, email, role, portfolio}

Step 5 — Route handler executes
  → require_role(['platform_admin', 'engineering_lead'])  — guard
  → Queries scoped by request.state.user.portfolio when role is 'engineering_lead'
  → Audit log entry written for mutations
```

### 8.3 Security Controls Summary

```
Layer               Control
─────────────────────────────────────────────────────────────
Transport           TLS 1.3 enforced; HTTP redirects to HTTPS
                    HSTS header (max-age: 31536000; includeSubDomains)

Authentication      Azure Entra ID OIDC; MFA enforced by tenant
                    Token expiry: 1 hour; silent refresh via MSAL

Authorisation       RBAC on all API routes; portfolio scoping for engineering_lead
                    403 response on insufficient role (no route enumeration)

Input validation    Pydantic models on every request body; 422 on violation
                    No raw SQL string concatenation (all SQLAlchemy parameterised)

Output              React escapes all dynamic content (XSS prevention)
                    CSP header blocks inline scripts and unknown origins

Secrets             Azure Key Vault; managed identity — no credentials in code
                    Secrets fetched at startup; never logged
                    LLM keys never returned by /settings endpoints

Rate limiting       60 req/min per authenticated user (Phase 2; slowapi)
                    Pipeline-run endpoint additionally enforces:
                      max 3 in-flight runs per project; max 10 platform-wide

LLM safety          Prompts grounded in canonical PDLC taxonomy
                    Outputs validated against schema before persisting
                    Cost cap per run (configurable; default $5)

Audit               audit_log table: all INSERT/UPDATE/DELETE with user identity
                    Immutable (INSERT only, no UPDATE/DELETE on audit_log)

Dependencies        GitHub Dependabot alerts for pip + npm CVEs
                    Base image: python:3.13-slim (minimal attack surface)

Network             App Service inbound: HTTPS only
                    Database + Key Vault + OpenAI: private endpoints (Phase 2)
```

---

## 9. Integration Architecture

### 9.1 ALM Adapter Pattern

Each ALM connector implements the same interface:

```python
# backend/agents/alm_connector/
#   ├── adapters/
#   │   ├── jira.py        → JiraAdapter
#   │   ├── ado.py         → AzureDevOpsAdapter
#   │   ├── github.py      → GitHubAdapter
#   │   ├── linear.py      → LinearAdapter
#   │   ├── servicenow.py  → ServiceNowAdapter
#   │   └── csv.py         → CSVAdapter
#   └── base.py            → BaseAdapter

class BaseAdapter(Protocol):
    def __init__(self, config: ALMConfig): ...
    async def health_check(self) -> bool: ...
    async def fetch(self) -> dict[str, Any]: ...                # raw payload
    def map_to_vsm(self, raw: dict) -> dict[str, Any]: ...      # canonical VSM

Behaviour:
  - Retry: 2 attempts, exponential backoff (1s, 2s); timeout 30s
  - Circuit breaker (custom): 5 consecutive failures → OPEN 60s
  - All errors logged with adapter name + config.tool
  - Response validation: Pydantic schema per adapter
```

### 9.2 LLM Call Resilience

```
backend/agents/llm.py

Synchronous call wrapper:
  - Timeout: 60s per call
  - Retry: 3 attempts on 429 (rate limit) or 5xx, with jittered backoff
  - On all-attempts-fail: emit LLM_UNAVAILABLE; rule-based fallback kicks in
  - Per-run token & cost telemetry logged to analysis_runs.result.cost

Cost cap:
  - Each agent has a max_tokens budget (typically 2048)
  - Total per-run cap default $5 (configurable via env var LLM_COST_CAP_USD)
  - On cap breach, remaining agents fall back to rule-based output
```

### 9.3 Pipeline Run Flow (end-to-end)

```
User clicks "Run Analysis" in Dashboard
        │
        ▼
POST /api/v1/agents/run-analysis/{project_id}
        │
        ├── Auth check: require_role(['platform_admin','engineering_lead','analyst'])
        │
        ├── Load project + latest vsm_snapshot from DB
        │
        ├── INSERT analysis_runs row (status='pending')
        │
        ├── await db.close()  ← critical: release session before bg task
        │
        ├── background_tasks.add_task(orchestrator.run_full_analysis,
        │                              run_id=row.id, project_id=...)
        │
        └── Return 202 {run_id, status: 'started'}

In background:
  orchestrator.run_full_analysis(run_id, project_id):
    - Open new session
    - UPDATE analysis_runs SET status='running'
    - Build LangGraph state from project + vsm_snapshot
    - graph.invoke(state)
        ├── For each node, on success: update agents_run[]
        ├── On node failure: log error, append to errors[], decide continue/abort
    - On completion: UPDATE result + status='complete' + completed_at=NOW()
    - On exception: UPDATE error + status='failed' + completed_at=NOW()
    - Invoke accuracy_scorer; write score to result.accuracy_score
    - Close session
```

### 9.4 Scheduled Pipeline Runs

```
APScheduler instance (BackgroundScheduler, configured at FastAPI startup)
        │
        ▼
Cron trigger reads platform_settings on each tick:
   schedule_enabled, schedule_frequency, schedule_day_of_week, schedule_hour
        │
        ▼
On fire:
  - For each project with auto_run = true:
      INSERT scheduled_pipeline_runs row (trigger='scheduled')
      Invoke orchestrator.run_full_analysis()
      On completion: UPDATE result_run_id = analysis_runs.id
```

Schedule cadence options: `weekly` (default), `daily`, `monthly` (Phase 2). The scheduler re-reads config on every tick, so changes propagate within one minute without a process restart.

---

## 10. Technology Stack Reference

### 10.1 Full Stack Matrix

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **FRONTEND** | | | |
| Framework | React | 18.3.1 | SPA UI framework |
| Build tool | Vite | 5.4.8 | Dev server + production bundler |
| Styling | TailwindCSS | 3.4.13 | Utility-first CSS |
| Routing | React Router | 6.26.1 | Client-side routing |
| Auth client | @azure/msal-react | latest | Entra ID OIDC token management |
| Server state | TanStack React Query | 5.x | API caching, loading states |
| Charts | Recharts + Chart.js | 2.12.7 / 4.4.4 | VSM, DORA, ROI visualisations |
| Icons | lucide-react + react-icons | 1.8.0 / 5.3.0 | Icon sets |
| HTTP | axios + axios-retry | 1.7.7 | REST client with retry |
| Excel export | xlsx | 0.18.5 | Analysis export |
| Date | date-fns | 4.1.0 | Date utilities |
| **BACKEND** | | | |
| Runtime | Python | 3.13 | Server runtime |
| Framework | FastAPI | 0.115 | Async REST API framework |
| Server | Uvicorn (uvloop) | latest | ASGI server |
| Auth | fastapi-azure-auth | 5.x | JWT validation against Entra |
| Validation | Pydantic | 2.x | Request schema + Settings |
| DB client | SQLAlchemy + asyncpg | 2.x / 0.30 | Async PostgreSQL |
| Migrations | Alembic (recommended) | 1.x | Versioned schema migrations |
| Scheduler | APScheduler | 3.x | Pipeline scheduler |
| Logging | loguru + python-json-logger | latest | Structured JSON logs |
| AI orchestration | LangGraph | latest | Multi-agent state graph |
| AI client | langchain-openai | latest | Azure / OpenAI ChatModel |
| RAG | rank-bm25 (custom) | — | In-process BM25 retrieval |
| Observability | opentelemetry-instrumentation-fastapi | latest | Trace + metric emission |
| **DATA** | | | |
| Database | PostgreSQL | 16 (Azure Flexible Server) | Primary data store |
| Cache | In-process LRU (Phase 1) / Redis (Phase 2) | — | Dashboard cache |
| **INFRASTRUCTURE** | | | |
| Cloud | Microsoft Azure | — | Strategic cloud |
| Frontend host | Azure Static Web Apps | — | CDN-backed SPA hosting |
| API host | Azure App Service | B2 Linux | Containerised FastAPI |
| Container registry | Azure Container Registry | — | Docker image store |
| Identity | Azure Entra ID | — | OIDC provider, RBAC groups |
| Secrets | Azure Key Vault | — | Secrets management |
| LLM | Azure OpenAI | gpt-4o, gpt-4o-mini | Primary inference |
| Monitoring | Azure Application Insights | — | APM + distributed tracing |
| **CI/CD** | | | |
| Source control | GitHub | — | Code repository |
| Pipeline | GitHub Actions | — | CI/CD automation |

---

## 11. Architecture Decisions Record

### ADR-001: FastAPI over Django
**Status:** Accepted
**Context:** Both frameworks are mature. Django brings ORM and admin out of the box. FastAPI brings async, automatic OpenAPI, and Pydantic validation.
**Decision:** Adopt FastAPI. The platform is API-first (no server-rendered pages), the workload is I/O bound (DB + LLM + ALM HTTP), and the OpenAPI auto-generation is high value for the React frontend.
**Consequence:** No batteries-included admin UI; admin functions live in `/settings` page. Validation centralised on Pydantic models — must be kept current.

### ADR-002: PostgreSQL with asyncpg (not SQLite)
**Status:** Accepted
**Context:** Earliest prototypes used SQLite for ease of bootstrapping. Production targets concurrent writes from scheduled runs + manual triggers.
**Decision:** Standardise on PostgreSQL via asyncpg. Configure connection pool (size 20, max overflow 10).
**Consequence:** Local development requires Postgres (e.g., Postgres.app on macOS). Adds an `init_db()` step in startup. Auto-table creation acceptable for Phase 1; switch to Alembic migrations before multi-environment rollout.

### ADR-003: Azure Entra ID over Custom JWT
**Status:** Accepted
**Context:** Enterprise SSO mandate; consistent identity across all internal tools.
**Decision:** Use Entra ID OIDC. Inherits MFA, conditional access, SSO, and group-based RBAC.
**Consequence:** Local dev uses a test tenant or short-lived dev tokens. JWT validation requires JWKS download; cache for 24h.

### ADR-004: LangGraph over Hand-Coded Pipeline
**Status:** Accepted
**Context:** The 7-step analysis pipeline could be a procedural script. LangGraph adds state-graph semantics and structured node retries.
**Decision:** Adopt LangGraph. The state-graph model makes the pipeline self-documenting, individually-invocable nodes trivial, and conditional routing (e.g., skip improvement generator when no bottlenecks) declarative.
**Consequence:** Additional dependency. Operators must understand the graph DSL to debug pipeline issues.

### ADR-005: In-Process BM25 Over External Vector DB
**Status:** Accepted (Phase 1)
**Context:** Could integrate Azure AI Search or pgvector for semantic retrieval. Current KB is ~150KB of curated content.
**Decision:** Use in-process BM25 (rank-bm25 style) for Phase 1. Document the migration path to pgvector if the corpus grows beyond 5MB or semantic recall becomes a blocker.
**Consequence:** Zero infrastructure cost; deterministic, explainable retrieval. Limited to lexical matching; synonym handling is manual via the agent-specific query templates.

### ADR-006: Rule-Based Fallback When LLM Unavailable
**Status:** Accepted
**Context:** Could fail loudly when LLM provider is unreachable. Static improvement catalogues are pre-authored.
**Decision:** Every agent has a deterministic, rule-based path. If both Azure OpenAI and OpenAI are unavailable, the pipeline still produces a coherent output drawn from `IMPROVEMENT_CATALOGUE`, `SCENARIOS`, `BUSINESS_CASES`, and `DORA_ELITE` dictionaries.
**Consequence:** Platform retains demo and analysis utility offline. Output is more generic; UI shows a "Rule-based output" badge so users can distinguish.

### ADR-007: Background Tasks for Pipeline Execution
**Status:** Accepted
**Context:** A pipeline run takes 90–180s. Doing this synchronously would tie up an HTTP worker for the full duration.
**Decision:** Use FastAPI BackgroundTasks. Endpoint returns 202 immediately with run_id; the frontend polls a status endpoint at 5s intervals.
**Consequence:** Must close the DB session **before** scheduling the background task (otherwise the connection stays held for the entire run). Worker exit kills in-flight runs — Phase 3 should migrate to a Celery/Arq queue with persistence.

### ADR-008: Monolith First, Decomposition Later
**Status:** Accepted
**Context:** The 9 route modules and 8 agents map loosely to bounded domains.
**Decision:** Ship Phase 1 as a containerised monolith. Plan extraction of Agent Orchestration and ALM Integration in Phase 3 once concurrent run volume justifies the operational overhead.
**Consequence:** Simpler deployment; shared connection pool; easier debugging. Decomposition path documented in SERVICE_ARCHITECTURE.md §8.

---

*Document prepared by Cognizant Engineering Effectiveness · May 2026*
*Companion documents: SERVICE_ARCHITECTURE.md, USER_GUIDE.md, PRODUCTION_READINESS.md*
