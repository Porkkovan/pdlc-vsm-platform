# PDLC VSM Platform — Service Architecture
**Version 1.0 · May 2026 · Cognizant Engineering Effectiveness Practice**

---

## Table of Contents

1. [Service Overview](#1-service-overview)
2. [Service Decomposition Map](#2-service-decomposition-map)
3. [Service Definitions](#3-service-definitions)
4. [API Contract Reference](#4-api-contract-reference)
5. [Service Communication Patterns](#5-service-communication-patterns)
6. [Data Ownership Map](#6-data-ownership-map)
7. [Deployment Units](#7-deployment-units)
8. [Phase 1 Monolith vs Phase 3 Decomposition](#8-phase-1-monolith-vs-phase-3-decomposition)

---

## 1. Service Overview

The platform's 24 frontend pages and 9 backend route modules group naturally into **six logical service domains**. In Phase 1 these are co-deployed as a single FastAPI monolith backed by PostgreSQL. In Phase 3, the higher-throughput or independently-scheduled domains (Agent Orchestration, ALM Integration) may be extracted into separate services.

| # | Service Domain | Route Modules | Frontend Pages | Core Responsibility |
|---|---|---|---|---|
| S1 | **Project & VSM Service** | `projects`, `vsm` | DashboardPage, CurrentVSMPage, VSMEditorPage | Project lifecycle (organisation → portfolio → product → team) and the canonical current-state Value Stream Map per project |
| S2 | **Analysis Service** | `analysis`, `agents` (pre-computed reads) | BottlenecksPage, ImprovementsPage, FutureStatePage, BusinessCasePage, RecommendationsPage | Bottleneck, improvement, future-state and business-case results produced by the LangGraph pipeline |
| S3 | **DevOps Maturity Service** | `devops_maturity` | DevOpsMaturityPage, DORAAssessmentPage, TransformationReadinessPage | 73-question DevOps maturity assessment across 4 dimensions; action item tracker; DORA scoring |
| S4 | **Agent Orchestration Service** | `agents`, `accuracy` | AgentsPage, AccuracyScorePage, PlaybookContextPage | LangGraph pipeline execution, run history, accuracy scoring, and team-context playbook contextualisation |
| S5 | **ALM Integration Service** | `alm` | ALMConnectPage | Connectors to Jira, Azure DevOps, GitHub, Linear, ServiceNow, CSV; raw-data → VSM mapping |
| S6 | **Knowledge & Configuration Service** | `settings_router`, `health` | SettingsPage, GovernancePage, OperationsIntelligencePage, LegacyModernisationPage, AIAssurancePage, GlossaryPage, RolesSlides | Platform configuration (LLM keys, ALM credentials, schedule), embedded knowledge base, and the static editorial content surfacing org-wide guidance |

The eight LangGraph agents (VSM Analyzer, Bottleneck Analyzer, Improvement Generator, Future State Designer, Business Case Builder, Benchmark Agent, Playbook Contextualizer, DevOps Maturity Agent) are owned by S4 but write outputs into tables read by S2 and S3.

---

## 2. Service Decomposition Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       FRONTEND  (React 18 + Vite SPA :3001)              │
│                                                                          │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ S1 Project   │  │ S2 Analysis   │  │ S3 DevOps    │  │ S4 Agents │ │
│  │ ──────────── │  │ ───────────── │  │   Maturity   │  │ ───────── │ │
│  │ Dashboard    │  │ Bottlenecks   │  │ ───────────  │  │ AgentsPage│ │
│  │ CurrentVSM   │  │ Improvements  │  │ DevOpsMat.   │  │ Accuracy  │ │
│  │ VSMEditor    │  │ FutureState   │  │ DORAAssess.  │  │ Playbook  │ │
│  │              │  │ BusinessCase  │  │ TransRdiness │  │           │ │
│  │              │  │ Recommends    │  │              │  │           │ │
│  └──────┬───────┘  └───────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
│         │                  │                  │                │       │
│  ┌──────┴───────┐  ┌───────┴───────┐          │         ┌─────┴─────┐ │
│  │ S5 ALM       │  │ S6 Knowledge  │          │         │  (shared) │ │
│  │ Connect      │  │ + Config      │          │         └───────────┘ │
│  │ ──────────── │  │ ───────────── │          │                       │
│  │ ALMConnect   │  │ Settings      │          │                       │
│  │              │  │ Governance    │          │                       │
│  │              │  │ OpsIntel      │          │                       │
│  │              │  │ Glossary, etc │          │                       │
│  └──────┬───────┘  └───────────────┘          │                       │
└─────────┼──────────────────────────────────────┼───────────────────────┘
          │  HTTP (Vite dev proxy) / Bearer JWT (prod)
          ▼                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                  API  (FastAPI Monolith — Phase 1, :8001)                │
│                                                                          │
│  /api/v1/projects         ─── S1 Project & VSM Service                  │
│  /api/v1/vsm              ─── S1 Project & VSM Service                  │
│  /api/v1/analysis         ─── S2 Analysis Service                       │
│  /api/v1/agents           ─── S4 Agent Orchestration Service            │
│  /api/v1/accuracy         ─── S4 Agent Orchestration Service            │
│  /api/v1/devops-maturity  ─── S3 DevOps Maturity Service                │
│  /api/v1/alm              ─── S5 ALM Integration Service                │
│  /api/v1/settings         ─── S6 Knowledge & Configuration Service      │
│  /api/v1/health           ─── S6 Knowledge & Configuration Service      │
│                                                                          │
│  Internal:                                                               │
│   orchestrator (LangGraph) ── invokes 8 agents in sequence               │
│   rag_engine + knowledge_base ─ BM25/TF-IDF retrieval (in-process)       │
│   llm.py ── Azure OpenAI → OpenAI fallback                               │
└──────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                ┌─────────────────────────────────┐
                │  PostgreSQL (asyncpg, 9 tables) │
                └─────────────────────────────────┘
```

---

## 3. Service Definitions

---

### S1 — Project & VSM Service

**Purpose:** The system of record for the organisational hierarchy (organisation → portfolio → product group → product → team) and the canonical current-state VSM snapshot per project. Every other service joins back to a `project_id` owned by S1.

**Route modules:** `projects.py`, `vsm.py`

**Endpoints:**

```
PROJECTS
GET    /api/v1/projects                   List all projects (sorted by created_at DESC)
POST   /api/v1/projects                   Create project (201)
GET    /api/v1/projects/{project_id}      Fetch single project
PUT    /api/v1/projects/{project_id}      Update project (org hierarchy, ALM config)
DELETE /api/v1/projects/{project_id}      Delete project (204; cascades to vsm_snapshots, analysis_runs)

VSM
POST   /api/v1/vsm/{project_id}           Save VSM snapshot (201) — source: alm | manual | sample
GET    /api/v1/vsm/{project_id}           Get latest VSM snapshot
PUT    /api/v1/vsm/{project_id}           Update existing snapshot (overrides JSON)
GET    /api/v1/vsm/{project_id}/metrics   Aggregate metrics from latest snapshot (PT, WT, FE, LT)
```

**Data owned:**
- `projects` — id (UUID str), name, organization, portfolio, product_group, product, team, industry, portfolios (JSON), product_groups (JSON), alm_tool, alm_config (JSON), created_at, updated_at
- `vsm_snapshots` — id, project_id (FK), source ('alm' | 'manual' | 'sample'), raw_data (JSON), vsm_data (JSON), summary (JSON), overrides (JSON), created_at
- `activity_metrics` — granular phase × activity metrics for time-series view (PT, WT, LT, cycle, throughput, WIP)

**Snapshot model:** Each `vsm_snapshots` row is immutable except for `overrides`. A re-fetch from ALM creates a new row; the latest row wins for read APIs. This preserves history for trend reporting.

**Role permissions:**

| Endpoint | platform_admin | engineering_lead | analyst | viewer |
|---|---|---|---|---|
| GET projects | ✅ all | ✅ own portfolio | ✅ all | ✅ read |
| POST project | ✅ | ✅ | ❌ | ❌ |
| PUT project | ✅ | ✅ own portfolio | ❌ | ❌ |
| DELETE project | ✅ | ❌ | ❌ | ❌ |
| POST vsm snapshot | ✅ | ✅ | ✅ | ❌ |
| PUT vsm (overrides) | ✅ | ✅ | ✅ | ❌ |
| GET vsm / metrics | ✅ | ✅ | ✅ | ✅ |

**Cache invalidation (Phase 2):**
- `POST /vsm/{id}` or `PUT /vsm/{id}` → invalidate `analysis:bottlenecks:{id}`, `analysis:improvements:{id}`, `analysis:future:{id}:*`, `analysis:business:{id}:*`

---

### S2 — Analysis Service

**Purpose:** Surfaces the pre-computed outputs of the LangGraph analysis pipeline (bottlenecks, improvements, three future-state scenarios, three business cases, industry benchmarks). The service is largely read-only at the API surface — the writes are performed by S4 (Agent Orchestration) when a pipeline run completes.

**Route modules:** `analysis.py`

**Endpoints:**

```
GET    /api/v1/analysis/{project_id}/bottlenecks
       Pre-computed bottlenecks for the latest run. Falls back to a default rule-based set if no run has executed.

GET    /api/v1/analysis/{project_id}/improvements
       Pre-computed improvement actions, ranked by ROI × confidence.

GET    /api/v1/analysis/{project_id}/future-state/{scenario}
       scenario ∈ { option-a (Augmented Human), option-b (Hybrid), option-c (AI-First / ADLC) }

GET    /api/v1/analysis/{project_id}/business-case/{scenario}
       Financial model for the named scenario: investment_range, roi_timeline, roi_multiple, payback_months.

GET    /api/v1/analysis/{project_id}/benchmarks
       Industry benchmarks (DORA elite/high/medium/low and lean VSM targets) for the project's industry.

GET    /api/v1/analysis/{project_id}/export
       Export the consolidated analysis report (JSON in Phase 1; PDF/PPTX in Phase 2 via build_*_deck.py utilities).
```

**Data owned:** None directly — reads from `analysis_runs.result` (owned by S4) and `vsm_snapshots` (owned by S1).

**Bottleneck schema (camelCase, returned to frontend):**
```json
{
  "phaseId": 6,
  "activityId": "release_management",
  "wasteType": "Approval delay",
  "rootCauses": ["CAB only meets Wednesdays", "manual change ticket creation"],
  "contributingFactors": ["regulated environment", "no automated risk scoring"],
  "currentPT": 6,
  "currentWT": 48,
  "feImpact": "-22%",
  "businessImpact": "Bi-weekly release cadence vs daily target",
  "linkedImprovements": ["imp_cab_automation", "imp_progressive_delivery"]
}
```

**Improvement schema:**
```json
{
  "id": "imp_cab_automation",
  "title": "Automated change risk scoring",
  "problem": "All changes route through manual CAB",
  "improvement": "AI risk scoring → auto-approve low risk; CAB only sees high risk",
  "agent": "ChangeRisk Agent",
  "type": "GenAI Agent",
  "expectedPTReduction": "30%",
  "expectedWTReduction": "70%",
  "timeToValue": "8 weeks",
  "roi": "4.2x",
  "effort": "M",
  "category": "Continuous Delivery"
}
```

**Future state schema:**
```json
{
  "scenarioId": "option-c",
  "scenarioLabel": "AI-First (ADLC)",
  "futurePT": 12,
  "futureWT": 18,
  "futureFE": "40%",
  "leadTimeDays": 7,
  "deploymentFrequency": "Daily",
  "cfr": "5%",
  "mttr": "1.0 day",
  "transformedPhases": [ /* per-phase before/after */ ]
}
```

**Role permissions:** All reads are gated by project visibility (S1 owns membership). No direct writes.

---

### S3 — DevOps Maturity Service

**Purpose:** Manages the 73-question DevOps maturity assessment across four dimensions (Cultural, Measurement, Process, Technical) and produces an action plan with prioritised remediation items. Surfaces an export endpoint that feeds findings back into the VSM input pipeline.

**Route modules:** `devops_maturity.py`

**Endpoints:**

```
ASSESSMENTS
POST   /api/v1/devops-maturity/assessments                      Create assessment (CreateAssessmentRequest)
GET    /api/v1/devops-maturity/assessments/project/{project_id} List assessments for a project
GET    /api/v1/devops-maturity/assessments/all                  List all assessments
GET    /api/v1/devops-maturity/assessments/{assessment_id}      Get single assessment
PUT    /api/v1/devops-maturity/assessments/{assessment_id}      Update assessment
DELETE /api/v1/devops-maturity/assessments/{assessment_id}      Delete assessment
POST   /api/v1/devops-maturity/assessments/{assessment_id}/run  Trigger AI scoring (async background)
PATCH  /api/v1/devops-maturity/assessments/{assessment_id}/responses  Save manual question scores + notes

ACTION ITEMS
GET    /api/v1/devops-maturity/assessments/{assessment_id}/action-items                List
POST   /api/v1/devops-maturity/assessments/{assessment_id}/action-items                Create custom item
PATCH  /api/v1/devops-maturity/assessments/{assessment_id}/action-items/{item_id}      Update
DELETE /api/v1/devops-maturity/assessments/{assessment_id}/action-items/{item_id}      Delete

REFERENCE
GET    /api/v1/devops-maturity/sources         Supported data source types (10: ALM, CI/CD, monitoring, etc.)
GET    /api/v1/devops-maturity/questions       All 73 questions grouped by dimension

VSM INPUT EXPORT
GET    /api/v1/devops-maturity/assessments/{assessment_id}/vsm-input
       Export findings as VSM input (used by S1 to enrich vsm_snapshots.summary)
```

**Data owned:**
- `devops_assessments` — id, project_id, organization, portfolio, product_group, team_name, industry, sources (JSON), notes, status, responses (JSON: `{question_id: {manual_score, notes}}`), result (JSON), created_at, updated_at
- `assessment_action_items` — id, assessment_id (FK), question_id, dimension, competency, title, description, priority, current_score, target_score, current_level, target_level, suggested_actions (JSON), responsible, target_date, status, notes, effort_estimate

**Question taxonomy (73 questions, 4 dimensions):**

```
CULTURAL (9 questions)
  team_collaboration       Cross-functional team alignment
  psychological_safety     Blame-free post-mortems
  continuous_learning      Lunch-and-learn cadence
  experimentation_culture  Hypothesis-driven delivery
  ... (5 more)

MEASUREMENT (11 questions)
  dora_metrics_tracked     Are the 4 DORA metrics measured?
  vsm_metrics_tracked      Are PT, WT, FE tracked per phase?
  customer_value_metrics   NPS / activation / retention
  ... (8 more)

PROCESS (9 questions)
  story_decomposition      Average story size in points
  wip_limits               Are WIP limits enforced?
  retrospective_cadence    Retro frequency + action follow-through
  ... (6 more)

TECHNICAL (14 questions)
  trunk_based_development  Branch lifespan
  feature_flag_coverage    % of changes behind flags
  test_pyramid_shape       Unit:integration:e2e ratio
  observability_stack      Logs/metrics/traces coverage
  ... (10 more)
```

**Maturity bands:**
```
PRE-CRAWL  (1-2): Ad hoc, no consistent practice
CRAWL      (3-4): Practice exists but inconsistent
WALK       (5-6): Practiced consistently within teams
RUN        (7-8): Systematised; measured; improving
FLY        (9-10): Industry-leading; outcome-driven; predictive
```

**AI scoring loop:** When `POST /assessments/{id}/run` is invoked, the DevOps Maturity Agent (S4) reads the team context + connected sources, scores each of the 73 questions, generates evidence-based commentary, and writes the result back to `devops_assessments.result`. The platform records both **AI score** and **manual override score** per question — the higher-precedence value wins for export.

**Role permissions:**

| Endpoint | platform_admin | engineering_lead | analyst | viewer |
|---|---|---|---|---|
| GET assessments | ✅ all | ✅ own portfolio | ✅ all | ✅ read |
| POST assessment | ✅ | ✅ | ✅ | ❌ |
| PUT assessment | ✅ | ✅ own | ✅ own | ❌ |
| POST run (AI scoring) | ✅ | ✅ | ✅ | ❌ |
| Action items (CUD) | ✅ | ✅ own | ✅ own | ❌ |
| GET questions / sources | ✅ | ✅ | ✅ | ✅ |

---

### S4 — Agent Orchestration Service

**Purpose:** Owns the LangGraph pipeline that chains the 8 analysis agents. Persists run history, exposes individual-agent endpoints for granular re-runs, and scores agent output quality against the canonical PDLC domain knowledge.

**Route modules:** `agents.py`, `accuracy.py`

**Endpoints:**

```
PIPELINE
POST   /api/v1/agents/run-analysis/{project_id}    Trigger full pipeline (async background)
                                                   returns {run_id, status: "started"}
GET    /api/v1/agents/status/{run_id}              Poll run status (pending/running/complete/failed)
GET    /api/v1/agents/result/{project_id}          Latest completed analysis result
GET    /api/v1/agents/history/{project_id}         All runs for a project

INDIVIDUAL AGENT TRIGGERS
POST   /api/v1/agents/vsm-analyzer/{project_id}
POST   /api/v1/agents/bottleneck-analyzer/{project_id}
POST   /api/v1/agents/improvement-generator/{project_id}
POST   /api/v1/agents/future-state-designer/{project_id}    body: {scenario: "all" | "option-a/b/c"}
POST   /api/v1/agents/business-case-builder/{project_id}
POST   /api/v1/agents/benchmark-agent/{project_id}

DEMO / SEED
POST   /api/v1/agents/seed-result/{project_id}     Seed a pre-built analysis result for demos

PLAYBOOK
POST   /api/v1/agents/contextualise-playbook/{project_id}
       body: {scenario_id, scenario_label, team_context, analysis_context, documents[]}
       Returns an implementation playbook tailored to the team's stack and constraints.

ACCURACY
GET    /api/v1/accuracy/{run_id}                   Score the named run's outputs against PDLC domain rules
```

**Data owned:**
- `analysis_runs` — id, project_id (FK), status ('pending' | 'running' | 'complete' | 'failed'), agents_run (JSON), result (JSON), error (Text), created_at, completed_at
- `scheduled_pipeline_runs` — id, project_id, trigger ('manual' | 'scheduled'), status, result_run_id, error, created_at, completed_at

**LangGraph pipeline (in-process):**

```
alm_connector → vsm_analyzer → benchmark_agent → bottleneck_analyzer
            → improvement_generator → future_state_designer → business_case_builder → END

Shared state: VSMAgentState (20-field TypedDict)
  project_id, project, alm_raw_data, vsm_data, overrides, benchmarks, metrics,
  bottlenecks, improvements, future_states, business_cases, recommendations,
  dora_calibration, errors, run_id, status, ...
```

Each node enriches the shared state. A failure in any node marks the run as `failed` with an error message but preserves the partial state for inspection.

**LLM provider chain:**
1. Azure OpenAI (preferred if `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` set) — deployment `gpt-4o`, API version `2024-02-15-preview`
2. OpenAI public API (if `OPENAI_API_KEY` set) — model `gpt-4o-mini`
3. Rule-based fallback (no key configured) — uses the static `IMPROVEMENT_CATALOGUE`, `SCENARIOS`, `BUSINESS_CASES` and `DORA_ELITE` dictionaries to assemble a coherent (if generic) output

Temperature is 0.2 and `max_tokens` is 4096 across both providers. LLM client construction is cached via `lru_cache`.

**Accuracy scoring:** `accuracy_scorer.py` evaluates each agent's output against:
- Schema adherence (no missing required fields)
- PDLC phase/activity ID validity
- Numerical bounds (FE ∈ [0, 100], PT/WT ≥ 0)
- RAG retrieval quality (did the relevant KB documents appear in the top-k for this agent's query?)
- Domain coherence (does the future-state FE exceed the current FE for each phase?)

**Role permissions:**

| Endpoint | platform_admin | engineering_lead | analyst | viewer |
|---|---|---|---|---|
| POST run-analysis | ✅ | ✅ | ✅ | ❌ |
| POST individual agent | ✅ | ✅ | ✅ | ❌ |
| POST seed-result | ✅ | ❌ | ❌ | ❌ |
| GET status / result / history | ✅ | ✅ | ✅ | ✅ read |
| POST contextualise-playbook | ✅ | ✅ | ✅ | ❌ |
| GET accuracy | ✅ | ✅ | ✅ | ✅ |

---

### S5 — ALM Integration Service

**Purpose:** Provides adapters for Application Lifecycle Management tools (Jira, Azure DevOps, GitHub, Linear, ServiceNow, CSV) and translates raw issue/work-item data into the canonical VSM input format that the analysis pipeline consumes.

**Route modules:** `alm.py`

**Endpoints:**

```
GET    /api/v1/alm/supported-tools     List ALM integrations: jira, ado, github, linear, servicenow, csv
POST   /api/v1/alm/test-connection     Test connectivity (ALMConfig: tool, url, username, token, project, board, filters)
POST   /api/v1/alm/fetch-data          Fetch from ALM + map to VSM format (writes to vsm_snapshots via S1)
POST   /api/v1/alm/map-to-vsm          Map an arbitrary raw-data dict to VSM structure (no fetch)
```

**Data owned:** No tables. Credentials are stored encrypted in `platform_settings` (owned by S6).

**Data consumed:**
- `platform_settings` — reads ALM credentials by key (e.g., `alm_jira`, `alm_ado`)
- Writes pass through to `vsm_snapshots` (owned by S1) with `source = 'alm'`

**Adapter contract:** Each adapter exposes `fetch(config) → raw_data` and `map_to_vsm(raw_data) → vsm_data`. The CSV adapter is the canonical reference — it expects a header row with: `ticket_id, type, title, sprint, status, story_points, cycle_time_days, wait_time_days, process_time_hours, phase, assignee, created_date, completed_date`.

**Failure modes:**
- `401/403` from ALM → `PLATFORM_UNAVAILABLE` (502) with operator-actionable message
- Schema-violating CSV → `VALIDATION_ERROR` (400) with row + column reference
- Empty result set → returns 200 with a synthetic 25-item sample dataset and a warning header (`X-VSM-Source: synthetic`)

**Role permissions:**

| Endpoint | platform_admin | engineering_lead | analyst | viewer |
|---|---|---|---|---|
| GET supported-tools | ✅ | ✅ | ✅ | ✅ |
| POST test-connection | ✅ | ✅ | ❌ | ❌ |
| POST fetch-data | ✅ | ✅ | ✅ | ❌ |
| POST map-to-vsm | ✅ | ✅ | ✅ | ❌ |

---

### S6 — Knowledge & Configuration Service

**Purpose:** Two distinct concerns bundled in Phase 1: (a) platform configuration (LLM credentials, ALM credentials, scheduled pipeline runs) and (b) the embedded knowledge base used by the RAG engine to ground agent outputs. The split is justified by the very low call volume on both — when either grows, it can be extracted.

**Route modules:** `settings_router.py`, `health.py`. The knowledge-base content is read in-process by `rag_engine.py`; no public CRUD endpoint exists for it in Phase 1 (planned for Phase 2).

**Endpoints:**

```
SETTINGS
GET    /api/v1/settings/status        LLM + ALM configuration status + scheduled-run status
POST   /api/v1/settings/llm           Save/update LLM config (provider, keys, endpoints, model)
POST   /api/v1/settings/alm           Save/update ALM credentials
POST   /api/v1/settings/schedule      Configure pipeline schedule (enabled, frequency, day_of_week, hour)
PUT    /api/v1/settings/schedule      Update schedule
GET    /api/v1/settings/schedule      Get schedule status

HEALTH
GET    /api/v1/health                 {status, app, version, agents: 8, pdlc_phases: 7, activities: 36}
```

**Data owned:**
- `platform_settings` — key (PK), value (Text), updated_at. Used as a key-value store: `llm_provider`, `llm_api_key`, `llm_endpoint`, `llm_model`, `alm_jira`, `alm_ado`, `schedule_enabled`, `schedule_frequency`, `schedule_day_of_week`, `schedule_hour`, etc. Values are JSON-encoded.

**Embedded knowledge base (read-only, source-controlled):** `backend/agents/knowledge_base.py` contains 100+ documents across four categories:
- **DORA Benchmarks** — elite/high/medium/low cutoffs for the four key metrics
- **Lean VSM** — Womack & Jones principles applied to software delivery
- **Transformation Patterns** — CAB elimination, progressive delivery, AI-augmented code review, etc.
- **Tool Integration** — sample queries, schema mappings for Jira/ADO/GitHub

The RAG engine (`rag_engine.py`) computes BM25 (k1=1.5, b=0.75) over a TF-IDF tokenisation of the corpus. No external vector DB; the corpus is small enough (~150KB total) to scan per query.

**Role permissions:**

| Endpoint | platform_admin | engineering_lead | analyst | viewer |
|---|---|---|---|---|
| GET status / health | ✅ | ✅ | ✅ | ✅ |
| POST/PUT settings | ✅ | ❌ | ❌ | ❌ |
| GET schedule | ✅ | ✅ | ✅ | ✅ |

---

## 4. API Contract Reference

### 4.1 Standard Response Envelope

All API responses follow the FastAPI convention with explicit envelopes for list endpoints:

```json
// Success (list)
{
  "data": [...],
  "meta": {
    "total": 137,
    "page": 1,
    "limit": 20,
    "pages": 7
  }
}

// Success (single)
{
  "data": { ... }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request body failed validation",
    "details": [
      { "field": "industry", "message": "field required" }
    ]
  }
}
```

### 4.2 Error Code Registry

| Code | HTTP | Description |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Pydantic schema validation failed |
| `UNAUTHORIZED` | 401 | No valid Bearer token (Phase 2 onwards) |
| `FORBIDDEN` | 403 | Insufficient role for this operation |
| `NOT_FOUND` | 404 | Requested resource does not exist |
| `CONFLICT` | 409 | Duplicate key or constraint violation |
| `LLM_UNAVAILABLE` | 502 | All LLM providers exhausted; rule-based fallback served if applicable |
| `PLATFORM_UNAVAILABLE` | 502 | ALM/source platform unreachable or returned 5xx |
| `RUN_FAILED` | 500 | LangGraph pipeline raised; partial state preserved in analysis_runs.error |
| `INTERNAL_ERROR` | 500 | Unhandled server error (no internal detail exposed) |

### 4.3 Key Request Schemas (Pydantic)

**POST /api/v1/projects**
```python
class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    organization: str
    portfolio: Optional[str] = None
    product_group: Optional[str] = None
    product: Optional[str] = None
    team: Optional[str] = None
    industry: Literal[
        "Financial Services - Banking",
        "Financial Services - Insurance",
        "Healthcare",
        "Retail & Consumer Goods",
        "Energy & Utilities",
        "Technology & Software",
        "Manufacturing",
        "Telecommunications",
    ]
    alm_tool: Optional[Literal["jira", "ado", "github", "linear", "servicenow", "csv"]] = None
    alm_config: Optional[Dict[str, Any]] = None
```

**POST /api/v1/vsm/{project_id}**
```python
class VSMSnapshotRequest(BaseModel):
    source: Literal["alm", "manual", "sample"]
    raw_data: Optional[Dict[str, Any]] = None
    vsm_data: Dict[str, Any]   # 7-phase × 36-activity matrix
    summary: Optional[Dict[str, Any]] = None
    overrides: Optional[Dict[str, Any]] = None
```

**POST /api/v1/devops-maturity/assessments**
```python
class CreateAssessmentRequest(BaseModel):
    project_id: Optional[str] = None
    organization: str
    portfolio: Optional[str] = None
    product_group: Optional[str] = None
    team_name: str
    industry: str
    sources: List[Literal[
        "jira", "ado", "github", "gitlab", "jenkins", "circleci",
        "datadog", "splunk", "sonarqube", "servicenow"
    ]]
    notes: Optional[str] = Field(default=None, max_length=2000)
```

**POST /api/v1/agents/contextualise-playbook/{project_id}**
```python
class PlaybookRequest(BaseModel):
    scenario_id: Literal["option-a", "option-b", "option-c"]
    scenario_label: str
    team_context: Dict[str, Any]           # tech_stack, team_size, methodology, cloud, compliance
    analysis_context: Dict[str, Any]       # from analysis_runs.result
    documents: List[Dict[str, Any]] = []   # uploaded supporting documents
```

**POST /api/v1/alm/test-connection**
```python
class ALMConfig(BaseModel):
    tool: Literal["jira", "ado", "github", "linear", "servicenow", "csv"]
    url: Optional[HttpUrl] = None
    username: Optional[str] = None
    token: Optional[SecretStr] = None
    project: Optional[str] = None
    board: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
```

### 4.4 Pagination Parameters (all list endpoints)

```
?page=1          (default: 1)
?limit=20        (default: 20, max: 100)
?sort=created_at (field name)
?order=desc      (asc | desc)
?filter[status]=complete  (filter by exact match; ANDed across keys)
```

### 4.5 Async Run Polling Contract

For all asynchronous operations (full pipeline run, DevOps assessment AI scoring) the client receives a 202 Accepted with a `run_id`. The frontend polls `GET /agents/status/{run_id}` at 5-second intervals up to a 5-minute cap. The polling endpoint returns:

```json
{
  "run_id": "8a2e...",
  "status": "running",            // pending | running | complete | failed
  "progress": {
    "current_agent": "improvement_generator",
    "completed_agents": ["alm_connector", "vsm_analyzer", "benchmark_agent", "bottleneck_analyzer"],
    "remaining_agents": ["future_state_designer", "business_case_builder"]
  },
  "started_at": "2026-05-16T11:32:50Z"
}
```

---

## 5. Service Communication Patterns

### 5.1 Within the Monolith (Phase 1)

All inter-service communication in Phase 1 is **direct Python function call** — same FastAPI process, same SQLAlchemy async session, same connection pool.

```
S2 Analysis  → reads analysis_runs (owned by S4) via shared session
S3 Maturity  → invokes S4 DevOps Maturity Agent directly
S4 Orchestr. → reads platform_settings (owned by S6) for LLM keys
S4 Orchestr. → invokes S5 ALM adapter for the alm_connector node
S1 Project   → writes vsm_snapshots after S5 fetch-data completes
```

This is acceptable in Phase 1 because:
- Single deployment unit; no network hop
- Shared async session and transaction scope
- Easier to debug; all logs in one stream

### 5.2 Pipeline Execution (Asynchronous In-Process)

```
Client (frontend)
   │  POST /api/v1/agents/run-analysis/{project_id}
   ▼
S4 agents route handler
   │  create analysis_runs row (status=pending)
   │  await db.close()                     ← critical: release session BEFORE bg task
   │  background_tasks.add_task(orchestrator.run_full_analysis, run_id, project_id)
   │  return 202 {run_id, status: "started"}
   ▼
(returns to client immediately)

In background:
   orchestrator.run_full_analysis
   │  status → running
   │  for each node in graph: invoke; update state; persist intermediate
   │  on success: status → complete
   │  on failure: status → failed, error → exception text
```

**Critical implementation note:** FastAPI runs background tasks **before** dependency cleanup, so the DB session must be explicitly closed inside the endpoint handler before `background_tasks.add_task(...)` is called. Otherwise the connection stays held for the full pipeline duration (90–180s), blocking the connection pool.

### 5.3 ALM Pull (Synchronous External Call)

For `POST /api/v1/alm/fetch-data` from S5:

```
Client (frontend)
   │  POST /api/v1/alm/fetch-data
   ▼
S5 alm route handler
   │  read credentials from platform_settings
   │  invoke adapter.fetch(config)
   │    │  HTTP GET to Jira/ADO/GitHub
   │    │  timeout: 30s
   │    │  retries: 2 with exponential backoff
   │    ▼
   │  adapter.map_to_vsm(raw_data) → vsm_data
   │  S5 calls S1's create_vsm_snapshot directly (in-process function call)
   ▼
Response: {snapshot_id, source: "alm", phase_count: 7, activity_count: 36}
```

Pattern: **Synchronous REST with retry**. If the ALM tool is unreachable after retries the endpoint returns `PLATFORM_UNAVAILABLE` (502).

### 5.4 Scheduled Pipeline Runs (Cron)

```
APScheduler fires per platform_settings.schedule_frequency
   │
   ▼
scheduler.tick():
   │  for each project with auto_run = true:
   │    POST internal: orchestrator.run_full_analysis(project_id)
   │    record scheduled_pipeline_runs row with trigger='scheduled'
```

Schedule format is `{frequency: weekly|daily, day_of_week: 0-6, hour: 0-23}` stored as JSON in `platform_settings`. The scheduler reads this on each tick and re-evaluates — config changes take effect within the next minute without a process restart.

### 5.5 Phase 3 — Event-Driven Decomposition (Future State)

When individual services are extracted, communication shifts to **Azure Service Bus** for async events and direct REST for synchronous reads:

```
Event: vsm.snapshot.created
  Published by: Project & VSM Service
  Consumed by:  Agent Orchestration Service (trigger new analysis run)
                DevOps Maturity Service (refresh related assessments)

Event: pipeline.run.completed
  Published by: Agent Orchestration Service
  Consumed by:  Project & VSM Service (update project.last_analysis_at)
                Notification Service (Teams/email to project owner)

Event: alm.credentials.updated
  Published by: Knowledge & Configuration Service
  Consumed by:  ALM Integration Service (invalidate adapter cache)
```

---

## 6. Data Ownership Map

Each table is owned by exactly one service. Other services may read but should not write directly.

| Table | Owning Service | Read-access Services |
|---|---|---|
| `projects` | S1 Project & VSM | S2, S3, S4 (all read project metadata in joins) |
| `vsm_snapshots` | S1 Project & VSM | S2, S4 (analysis reads), S3 (maturity context) |
| `activity_metrics` | S1 Project & VSM | S2, S4 |
| `analysis_runs` | S4 Agent Orchestration | S2 (all read endpoints), Dashboard |
| `scheduled_pipeline_runs` | S4 Agent Orchestration | S6 (status display in Settings UI) |
| `devops_assessments` | S3 DevOps Maturity | S1 (export → vsm enrichment), S4 (agent input) |
| `assessment_action_items` | S3 DevOps Maturity | None |
| `platform_settings` | S6 Knowledge & Config | S4 (LLM keys), S5 (ALM credentials) |
| Knowledge corpus (file) | S6 Knowledge & Config | S4 (RAG retrieval at runtime) |

**Cross-cutting tables (planned for Phase 2):**
- `users` — owned by an Auth service (currently absent; FastAPI Depends() placeholders in router signatures)
- `audit_log` — owned by an Audit service; written by all services via shared helper
- `notifications` — owned by a Notification service; populated on key events

---

## 7. Deployment Units

### 7.1 Phase 1 — Single Deployable (Monolith)

```
┌──────────────────────────────────────────────────────────┐
│  Docker image: acr-pdlc-vsm-prod.azurecr.io/api:{sha}    │
│                                                          │
│  Entrypoint: uvicorn backend.main:app --host 0.0.0.0     │
│                       --port 8001 --workers 4             │
│                                                          │
│  Contains all 6 service domains:                         │
│   S1 Project + S2 Analysis + S3 DevOps Maturity         │
│   + S4 Agent Orchestration + S5 ALM Integration         │
│   + S6 Knowledge & Config                                │
│  + Cross-cutting: logging, APScheduler, in-memory RAG    │
│                                                          │
│  Config (env vars from Key Vault via managed identity):  │
│   DATABASE_URL, AZURE_OPENAI_API_KEY,                    │
│   AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT,        │
│   OPENAI_API_KEY (fallback), JIRA_URL/USERNAME/TOKEN,    │
│   ADO_ORG_URL/ADO_PAT, APPINSIGHTS_CONNECTION_STRING     │
└──────────────────────────────────────────────────────────┘

Frontend: Azure Static Web Apps (separate deploy from GitHub Actions)
  Source: frontend/dist/ (Vite build output)
  Config: VITE_API_BASE_URL (=https://api.pdlc-vsm.internal),
          VITE_AZURE_CLIENT_ID, VITE_AZURE_TENANT_ID
```

### 7.2 Phase 3 — Potential Decomposed Deployment (Future)

```
┌────────────────┐  ┌────────────────┐  ┌─────────────────┐
│  Project & VSM │  │   Analysis API │  │ DevOps Maturity │
│  App Service B1│  │  App Service B1│  │  App Service B1 │
│  S1 routes     │  │  S2 routes     │  │  S3 routes      │
└────────────────┘  └────────────────┘  └─────────────────┘

┌────────────────────────────┐  ┌────────────────────────┐
│  Agent Orchestration       │  │  ALM Integration       │
│  Container App (B2/B3)     │  │  App Service B1 +      │
│  — burstable for LLM calls │  │  outbound NAT for SaaS │
│  S4 routes + scheduler     │  │  S5 routes             │
└────────────────────────────┘  └────────────────────────┘

┌────────────────┐  ┌───────────────────────────────────────┐
│ Config / KB API│  │  API Gateway (Azure API Management)    │
│ App Service B1 │  │  JWT validation, routing, rate limit   │
│ S6 routes      │  │  Single entry point for all clients    │
└────────────────┘  └───────────────────────────────────────┘
```

Trigger criteria for decomposition:
- Pipeline runs sustain > 50/hour (Agent Orchestration becomes the bottleneck)
- ALM polling expands beyond 6 connectors (S5 needs its own scaling profile)
- Multiple teams own different domains
- Compliance demands per-service audit boundaries

---

## 8. Phase 1 Monolith vs Phase 3 Decomposition

| Dimension | Phase 1 (Monolith) | Phase 3 (Decomposed) |
|---|---|---|
| **Deployment** | Single Docker image | 5–6 separate images, API gateway |
| **Scaling** | All services scale together | Each service scales independently |
| **Database** | Shared PostgreSQL, 9 tables | Schema-per-service or separate DBs |
| **Transactions** | Cross-service async transactions possible | Saga pattern; eventual consistency |
| **Testing** | Single pytest suite | Per-service test suites + contract tests |
| **Latency** | In-process function calls (< 1ms) | Network calls (5–50ms per hop) |
| **Failure isolation** | Single restart on uncaught exception | Circuit breakers per service |
| **Observability** | Single trace context | Distributed tracing (W3C trace-context) |
| **Pipeline isolation** | Long-running LLM calls share workers | Agent Orchestration on its own burstable plan |
| **Team model** | One team owns all | Service-aligned ownership |
| **Recommended for** | Phase 1–2: < 30 concurrent runs, single team | Phase 3+: > 100 concurrent runs, multiple teams |

**Recommendation:** Begin Phase 3 decomposition with **S4 Agent Orchestration** first — its workload profile (90–180s LLM-bound runs) is materially different from the rest of the platform, so isolating it onto a burstable plan removes the largest source of tail latency on the rest of the API. **S5 ALM Integration** is a natural second extraction since it owns its credentials, its scheduler, and its external dependencies. **S1 Project & VSM** is the highest-traffic and most tightly coupled and should be extracted last (or kept central as the "core" service while peripherals split off).

**Suggested decomposition order:**
```
1. S4 Agent Orchestration   (Q1 2027 — burstable LLM workload; own scheduler)
2. S5 ALM Integration       (Q1 2027 — own external deps; own credentials cache)
3. S6 Knowledge & Config    (Q2 2027 — low-traffic; simple CRUD; clean boundary)
4. S3 DevOps Maturity       (Q2 2027 — own tables; reads VSM for context only)
5. S2 Analysis              (Q3 2027 — read-projection of S4; could become a CQRS view)
6. S1 Project & VSM         (Q3 2027 — core; last; needs API gateway routing)
```

---

*Document prepared by Cognizant Engineering Effectiveness · May 2026*
*Companion documents: TECHNICAL_ARCHITECTURE.md, USER_GUIDE.md, PRODUCTION_READINESS.md*
