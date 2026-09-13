# PDLC VSM Platform — Production Readiness Plan
**Version 1.0 · May 2026 · Cognizant Engineering Effectiveness Practice**

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current State Assessment](#2-current-state-assessment)
3. [Tech Stack Revisit](#3-tech-stack-revisit)
4. [Target Architecture](#4-target-architecture)
5. [Activity Mapping — Current vs Target](#5-activity-mapping--current-vs-target)
6. [Production Readiness Workstreams](#6-production-readiness-workstreams)
7. [Data Model Evolution](#7-data-model-evolution)
8. [Security & Compliance](#8-security--compliance)
9. [Integration Architecture](#9-integration-architecture)
10. [Infrastructure & Deployment](#10-infrastructure--deployment)
11. [Observability & Operations](#11-observability--operations)
12. [Phased Delivery Plan](#12-phased-delivery-plan)
13. [Risk Register](#13-risk-register)

---

## 1. Executive Summary

The PDLC VSM Platform is an engineering effectiveness diagnostic and transformation planner. It maps a team's product delivery lifecycle into a canonical 7-phase × 36-activity model, runs an 8-agent LangGraph pipeline to identify bottlenecks and recommend improvements, and produces three ROI-quantified transformation scenarios with board-ready business cases. The platform currently runs locally with PostgreSQL, a FastAPI backend, and a React frontend. The platform is functionally rich — 24 frontend pages, 9 route modules, 8 AI agents, 9 database tables — but requires significant structural hardening before enterprise deployment.

**What this document covers:**
- A revised technology stack suited to enterprise-scale, Azure-hosted deployment
- Redrawn activity maps showing how each workflow changes in production
- Six structured workstreams (Auth, API, AI/Pipeline, Integrations, Infra, Observability) with task-level detail
- A phased delivery plan across three milestones: Hardened MVP (Q3 2026), Connected Platform (Q4 2026), and Scale & Assurance (Q1 2027)

**Key structural decisions:**
| Concern | Current | Recommended |
|---|---|---|
| Authentication | None | Azure Entra ID (OIDC) + RBAC |
| API framework | FastAPI 0.115 | FastAPI 0.115 + Pydantic + fastapi-azure-auth |
| Frontend hosting | Vite dev server | Azure Static Web Apps |
| Backend hosting | Local Uvicorn | Azure App Service (containerised) |
| Database | Local PostgreSQL | Azure Database for PostgreSQL Flexible Server |
| Migrations | `Base.metadata.create_all()` | Alembic versioned migrations |
| Secrets | .env files | Azure Key Vault |
| Caching | None | In-process LRU (Phase 1) → Redis (Phase 2) |
| LLM | Direct API keys in code | Azure OpenAI w/ Key Vault refs + cost capping |
| Observability | loguru console | App Insights + OpenTelemetry traces |
| CI/CD | Manual | GitHub Actions → Azure slot swap |
| Real ALM integrations | CSV only (mocked APIs) | Live Jira/ADO/GitHub/Linear/ServiceNow |
| Pipeline persistence | In-memory background tasks | Persisted queue (Phase 3) |

---

## 2. Current State Assessment

### 2.1 What Is Built

The platform covers the complete engineering effectiveness diagnostic and planning journey across six functional areas:

| Functional Area | Modules | Status |
|---|---|---|
| **Project & VSM Capture** | Dashboard, ALM Connect, Current VSM, VSM Editor | ✅ Complete |
| **Maturity Assessment** | DORA Assessment, DevOps Maturity (73Q), Transformation Readiness | ✅ Complete |
| **AI Analysis** | Bottlenecks, Improvements, Recommendations, Accuracy Score | ✅ Complete |
| **Future State & Business Case** | Future State (A/B/C scenarios), Business Case | ✅ Complete |
| **Playbook & Agents** | Playbook Context, Agents (run history) | ✅ Complete |
| **Configuration & Reference** | Settings, Governance, Ops Intelligence, AI Assurance, Glossary | ⚠️ Partial (some pages static) |

### 2.2 What Is Missing for Production

**Blocking (must resolve before any live use):**
- No authentication or authorisation — all API endpoints are open
- LLM credentials and ALM tokens stored in plaintext `platform_settings` table
- CORS locked to `localhost:3001` only
- No audit trail of who triggered which run
- No cost cap on LLM spend per run; no per-tenant quota

**High Priority:**
- No API documentation published (FastAPI auto-OpenAPI exists but not exposed/secured)
- No rate limiting or request throttling
- No structured error envelope — Pydantic 422s leak field internals
- ALM connectors not all production-ready (CSV ready; Jira/ADO scaffolded; others stub)
- No automated tests (no pytest suite; no e2e)
- Pipeline runs are background tasks — restart kills in-flight runs

**Medium Priority:**
- No pagination on list endpoints
- No caching — every dashboard load re-runs aggregation
- No bulk export (PPTX/Excel/PDF building scripts exist but not wired to UI)
- No file attachment for ALM-evidence documents in maturity assessment
- RAG corpus growth path unclear; BM25-only retrieval

### 2.3 Quality Signal

| Dimension | Rating | Notes |
|---|---|---|
| Data model design | 🟢 Good | Async SQLAlchemy, FK integrity, JSON for flexible payloads |
| API surface | 🟡 Adequate | Functional but no versioning enforcement; mixed error patterns |
| Frontend quality | 🟢 Good | React 18, responsive, 24 pages, Recharts + Chart.js for data viz |
| AI quality | 🟡 Adequate | Accuracy scorer present but threshold not enforced before export |
| Security posture | 🔴 Not ready | Zero auth, open endpoints, secrets in DB plaintext |
| Observability | 🔴 Not ready | loguru console only, no distributed tracing |
| Test coverage | 🔴 Not ready | No tests |
| Deployment pipeline | 🔴 Not ready | Manual startup script only |

---

## 3. Tech Stack Revisit

### 3.1 Backend

| Layer | Current | Production Recommendation | Rationale |
|---|---|---|---|
| Runtime | Python 3.13 | Python 3.13 (**keep**) | Already modern; performance gains over 3.11 |
| Framework | FastAPI 0.115 | FastAPI 0.115 (**keep**) | Excellent async + auto-OpenAPI fit |
| ASGI server | Uvicorn (default loop) | **Uvicorn + uvloop**, workers=4 | uvloop ~2× faster on I/O-bound workloads |
| Auth middleware | None | **fastapi-azure-auth** (Entra ID OIDC) | Drop-in JWT validation against Entra JWKS |
| Authorisation | None | Custom RBAC dependency using JWT claims | Role claims from Entra ID mapped to platform roles |
| Database driver | asyncpg | asyncpg (**keep**) | High-perf async driver |
| Input validation | Pydantic 2.x | Pydantic 2.x (**keep**) | Already used throughout |
| Error handling | FastAPI default | **Centralised exception handler** with structured codes | `{error: {code, message, details}}` envelope |
| Rate limiting | None | **slowapi** + Redis store | Prevents abuse; works across multiple workers |
| Caching | None | In-process **lru_cache** (Phase 1); **aiocache + Redis** (Phase 2) | Dashboard aggregation cached 60s |
| Logging | loguru | **loguru + python-json-logger** + App Insights handler | Structured logs ingestible by Azure Monitor |
| API docs | Auto-generated, unsecured | Auto OpenAPI at `/api/v1/openapi.json`, Swagger UI at `/docs` (auth-gated) | Living API contract |
| Migrations | `Base.metadata.create_all()` | **Alembic** | Versioned migrations |
| Process management | Direct uvicorn | Containerised (Docker + Azure App Service) | Zero-downtime restarts |
| Scheduler | APScheduler in-process | APScheduler + Redis job store (Phase 2) | Survives restarts |

**New backend dependencies to add:**
```
fastapi-azure-auth          # Azure Entra ID JWT validation
slowapi                     # Rate limiting (FastAPI-compatible)
alembic                     # Versioned migrations
opentelemetry-instrumentation-fastapi   # Distributed tracing
opentelemetry-exporter-azure-monitor    # App Insights exporter
azure-keyvault-secrets      # Key Vault SDK
azure-identity              # Managed Identity auth
python-json-logger          # JSON log formatter
aiocache + aiocache[redis]  # Phase 2 caching
pytest pytest-asyncio       # Test harness
httpx                       # Used by tests + ALM adapters
```

### 3.2 Frontend

| Layer | Current | Production Recommendation | Rationale |
|---|---|---|---|
| Framework | React 18.3 + Vite 5.4 | React 18.3 + Vite 5.4 (**keep**) | Mature, well-suited |
| Styling | TailwindCSS 3.4 | TailwindCSS 3.4 (**keep**) | No change needed |
| Charts | Recharts + Chart.js | Recharts + Chart.js (**keep**) | Adequate for current viz |
| HTTP client | axios 1.7 | axios 1.7 + **axios-retry** | Adds automatic retry on transient failures |
| Auth client | None | **@azure/msal-react** | MSAL handles Entra ID token acquisition |
| State management | React Context | React Context + **TanStack React Query** | Caches API responses, manages stale/loading |
| Error boundaries | None | React error boundaries per major route | Prevents full-page crashes |
| Form validation | None | **react-hook-form** + Zod | Consistent validation for VSM Editor + Settings |
| Build output | Vite dev | `vite build` → Azure Static Web Apps | CDN-backed, managed SSL |
| Environment config | hardcoded localhost | `.env.production` + `VITE_API_BASE_URL` | Production API base injected at build time |
| Code splitting | None | React.lazy + Suspense per route | Smaller initial bundle |

**New frontend dependencies:**
```
@azure/msal-react @azure/msal-browser
@tanstack/react-query
react-hook-form @hookform/resolvers zod
axios-retry
```

### 3.3 Database

| Concern | Current | Production Recommendation |
|---|---|---|
| Engine | PostgreSQL 18 (local Postgres.app) | **Azure Database for PostgreSQL Flexible Server** v16 |
| Migrations | `Base.metadata.create_all()` on startup | **Alembic** — versioned migration files |
| Connection pooling | SQLAlchemy default | **PgBouncer** sidecar (transaction mode); pool max: 20 per worker |
| Backups | None | Azure Flexible Server automated backups (7-day retention, PITR) |
| Read replicas | None | One read replica for dashboard analytics |
| Secrets | .env plaintext | Azure Key Vault — `DATABASE_URL` fetched at startup via managed identity |
| Schema | JSON columns for results | Add GIN indexes on `analysis_runs.result`, `vsm_snapshots.vsm_data` paths used in queries |
| Audit trail | None | Add `audit_log` table populated by FastAPI middleware (see §7) |
| pgvector | Not used | Optional Phase 3 — migrate RAG corpus when > 5MB |

### 3.4 Infrastructure

| Component | Current | Production |
|---|---|---|
| Frontend hosting | Vite dev server `:3001` | Azure Static Web Apps — CDN-backed, custom domain, managed SSL |
| Backend hosting | Local Uvicorn `:8001` | Azure App Service (B2) — containerised, auto-scale to 4 instances |
| Container registry | None | Azure Container Registry |
| Database | Local PostgreSQL | Azure Database for PostgreSQL Flexible Server (General Purpose, 4 vCore) |
| Cache | None | Azure Cache for Redis (C1 Standard) — Phase 2 |
| Secrets | .env / DB plaintext | Azure Key Vault with Managed Identity binding to App Service |
| Identity | None | Azure Entra ID |
| LLM | Direct OpenAI/Azure key in env | **Azure OpenAI** w/ PTU + standard fallback, key in Key Vault |
| Monitoring | None | Azure Monitor + Application Insights + OpenTelemetry |
| Alerting | None | Azure Monitor alert rules → Microsoft Teams webhook |
| CI/CD | None | GitHub Actions → Azure deployment with slot swap |
| DNS/SSL | None | App Service managed certificate |

---

## 4. Target Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  USER LAYER                                                              │
│  Browser (MSAL auth) ──→ Azure Static Web Apps (React 18 + Vite)        │
│  Custom domain: pdlc-vsm.internal                                        │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ HTTPS + Bearer JWT
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  API LAYER                                                               │
│  Azure App Service (Python 3.13 + FastAPI + Uvicorn/uvloop)             │
│  ├── TrustedHostMiddleware (allowed hosts)                              │
│  ├── CORSMiddleware (configured allowlist)                              │
│  ├── fastapi-azure-auth (JWT validation)                                │
│  ├── RBAC dependency (role claims → permissions)                        │
│  ├── slowapi rate limiting (Redis store, Phase 2)                       │
│  ├── Pydantic request/response validation                               │
│  ├── loguru JSON logging → App Insights                                 │
│  ├── Centralised exception handler (structured codes)                   │
│  └── 9 route modules + /api/v1/health + /api/v1/openapi.json            │
└──────┬──────────────────────────────┬────────────────────────────────────┘
       │                              │
       ▼                              ▼
┌─────────────────┐        ┌──────────────────────┐
│  PostgreSQL 16   │        │  In-Process LRU       │
│  Flexible Server │        │  (Phase 1)            │
│  ├── Primary     │        │  ──────────────────   │
│  └── Read replica│        │  Azure Cache for      │
└─────────────────┘        │  Redis (Phase 2)      │
                            └──────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  AI LAYER                                                                │
│  ├── LangGraph orchestrator (8-agent pipeline)                          │
│  ├── RAG engine (BM25/TF-IDF over embedded KB corpus)                   │
│  ├── Accuracy scorer (post-run validation)                              │
│  ├── llm.py: Azure OpenAI (primary) → OpenAI (fallback) → rule-based    │
│  └── Background tasks (Phase 1) → Persistent queue (Phase 3)            │
└─────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  INTEGRATION LAYER                                                       │
│  ├── Jira         (REST + JQL) — circuit breaker + retry                │
│  ├── Azure DevOps (REST + WIQL)                                         │
│  ├── GitHub       (REST + GraphQL)                                      │
│  ├── Linear       (GraphQL)                                             │
│  ├── ServiceNow   (REST + OAuth)                                        │
│  └── CSV          (in-process)                                          │
└─────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  OBSERVABILITY                                                           │
│  Azure Application Insights ← loguru transport + OpenTelemetry          │
│  Azure Monitor ← App Service metrics                                    │
│  Alert rules → Microsoft Teams webhook (P1: on-call)                    │
└─────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  IDENTITY & SECRETS                                                      │
│  Azure Entra ID — OIDC provider for all users                           │
│  Azure Key Vault — DATABASE_URL, AZURE_OPENAI_API_KEY, ALM credentials  │
│  Managed Identity — App Service → Key Vault, App Service → Azure OpenAI │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Role Model

Four roles, mapped from Entra ID group membership:

| Role | Access | Personas |
|---|---|---|
| **Platform Admin** | Full read/write across all modules; LLM/ALM config; scheduling | Engineering Effectiveness Lead, Platform Owner |
| **Engineering Lead** | Full read/write within their portfolio; approves scenarios | Head of Engineering, Engineering Manager |
| **Analyst** | Read all; build/edit VSMs, run pipelines, score maturity | Transformation consultant, DevOps practitioner |
| **Viewer** | Read-only across all modules | Executive sponsor, Auditor |

---

## 5. Activity Mapping — Current vs Target

### 5.1 ALM Data Capture

**Current Flow:**
```
User uploads CSV or configures ALM connection (no auth)
  → POST /api/v1/alm/fetch-data (open endpoint)
    → CSV parsed or Jira/ADO HTTP call made
      → Raw data mapped to VSM
        → vsm_snapshots row created (source='alm'|'manual'|'sample')
```

**Target Flow:**
```
Authenticated user (analyst+) opens ALM Connect
  → MSAL token validated by API middleware
    → Pydantic schema validates ALMConfig
      → Credentials fetched from Key Vault (not request body)
        → ALM adapter invoked with circuit breaker + retry
          → On success: raw data + mapped VSM → vsm_snapshots
            → Audit log: {user_id, action:'VSM_INGEST', project_id, source, row_count}
              → Engineering Lead notified (Teams webhook) on first ingest for a project
```

**New touchpoints:** Authentication gate, credentials from Key Vault, audit logging, circuit breaker on adapter, ingest notification.

---

### 5.2 Pipeline Run

**Current Flow:**
```
User clicks "Run Analysis"
  → POST /api/v1/agents/run-analysis/{project_id}
    → analysis_runs row created (status='pending')
    → BackgroundTasks queue → orchestrator.run_full_analysis
    → 8 agents run in sequence, each calling LLM
    → On worker restart: in-flight run is killed (no recovery)
    → No cost cap; no rate limiting
```

**Target Flow:**
```
Authenticated user (analyst+) clicks "Run Analysis"
  → Rate limit check: max 3 in-flight per project; max 10 platform-wide
    → analysis_runs row created (status='pending')
    → Cost cap check: project budget remaining > 0
      → Background task (Phase 1) or persistent queue (Phase 3) picks up run
        → LangGraph state initialised; each node:
            → Audit log: {user_id, action:'AGENT_INVOKED', agent, run_id, tokens, cost}
            → LLM call with timeout + retry; cost charged against project budget
            → Output schema-validated before merging into state
          → Final state persisted; accuracy_scorer invoked
            → On accuracy_score < 80: result flagged for human review
              → Notification sent to user who initiated run
                → Audit log: {action:'RUN_COMPLETE', run_id, status, duration, total_cost}
```

**New touchpoints:** Rate limit, cost cap, per-agent audit, schema validation, accuracy gating, notification.

---

### 5.3 DevOps Maturity Assessment

**Current Flow:**
```
Anyone creates assessment manually (no auth)
  → Question scores entered, or AI scoring triggered
    → result stored; action items generated
```

**Target Flow:**
```
Authenticated analyst+ creates assessment
  → Linked to project (project must be visible to the user's portfolio)
    → AI scoring triggered → run uses LLM with cost cap
      → Per-question evidence trail saved (data_sources used, RAG hits)
        → Engineering Lead reviews and overrides (with mandatory note)
          → On approval: assessment locked + audit log written
            → Optionally exported as VSM input → enriches next pipeline run
```

**New touchpoints:** Project-scope authorisation, evidence trail, mandatory override notes, approval lock, export integration.

---

### 5.4 Business Case Export

**Current Flow:**
```
User clicks Export PPTX
  → Direct file download of unlocked artefact
    → No version tracking; no audit
```

**Target Flow:**
```
Engineering Lead approves a scenario (Option A / B / C)
  → Approval recorded: {approver_id, scenario, decided_at, notes}
    → "Locked" badge appears on Business Case
      → Export PPTX/Excel/PDF available
        → Each export logged: {user_id, run_id, scenario, format, downloaded_at}
          → Watermark with project_id + run_id + accuracy_score embedded
```

**New touchpoints:** Approval as gate, watermark, download audit.

---

### 5.5 Scheduled Pipeline Runs

**Current Flow:**
```
APScheduler reads platform_settings every minute
  → If schedule_enabled: trigger run on next cron
    → No persistence across restarts
      → No queue; no concurrency control
```

**Target Flow:**
```
APScheduler with Redis job store (Phase 2)
  → Survives worker restarts
    → Per-project schedule (Phase 3): weekly cadence + day-of-week + hour
      → On fire: cost-cap check + concurrency check (≤ 10 platform-wide)
        → Background task or persistent queue picks up
          → On failure: retry up to 3 with exponential backoff
            → Platform Admin notified on consecutive failures
```

**New touchpoints:** Persistent scheduler, per-project schedule, cost-cap gating, retry policy, failure alerts.

---

### 5.6 LLM Call Resilience

**Current Flow:**
```
Agent calls llm.py
  → Direct Azure/OpenAI HTTP call
    → On 429 or 5xx: exception bubbles; agent fails; pipeline aborts
      → No cost tracking; no per-tenant quota
```

**Target Flow:**
```
Agent calls llm.py wrapper
  → Cost cap check (per-run, per-project, per-platform)
    → Azure OpenAI primary call
      → On 429: wait + jittered retry (3 attempts)
      → On 5xx: retry (3 attempts)
        → If still failing: try OpenAI fallback
          → If all providers fail: invoke rule-based fallback
            → Mark agent output with "Rule-based" badge
              → Persist tokens used + cost in analysis_runs.result.cost
                → If cumulative cost exceeds 80% of cap: warn in UI
                  → On 100% cap hit: switch all subsequent agents to rule-based
```

**New touchpoints:** Cost cap, multi-provider fallback chain, telemetry, UI badges, graceful degradation.

---

## 6. Production Readiness Workstreams

### WS-1 · Authentication & Authorisation
**Priority: Blocking**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| Register app in Entra ID tenant | Platform + IT | 1 day | App registration with redirect URIs |
| Create Entra ID groups for 4 roles | IT | 0.5 day | Groups seeded with initial members |
| Add `fastapi-azure-auth` to FastAPI; validate JWT on all routes | Backend dev | 2 days | Middleware chain: trusted-host → CORS → auth → RBAC → route |
| Build RBAC dependency: `require_role(roles[])` | Backend dev | 1 day | Reads role claim from JWT; 403 on mismatch |
| Apply RBAC to all 9 route modules | Backend dev | 2 days | Per-route permission matrix documented |
| Add MSAL React to frontend; redirect to login on 401 | Frontend dev | 2 days | MSAL provider wraps App; acquire token silently |
| Add user identity to all mutation endpoints | Backend dev | 1 day | Stored in audit log and `created_by` columns |
| Add `created_by`, `updated_by` columns to projects, vsm_snapshots, analysis_runs, devops_assessments | Backend dev | 0.5 day | Alembic migration + backfill with 'system' |
| Integration test: all 4 roles against all 9 route modules | QA | 2 days | pytest + httpx async |
| **Total** | | **~12 days** | |

---

### WS-2 · API Hardening & Documentation
**Priority: Blocking**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| Audit all Pydantic schemas; ensure 100% coverage on routes | Backend dev | 2 days | ~30 schemas across 9 routers |
| Centralised exception handler with structured envelope | Backend dev | 1 day | `{error: {code, message, details}}` for all 4xx/5xx |
| Configure TrustedHost + CORS from env vars | Backend dev | 0.5 day | Remove hardcoded localhost |
| Add `slowapi` rate limiter (60 req/min per user) | Backend dev | 1 day | Phase 1: in-process; Phase 2: Redis-backed |
| Per-endpoint rate limits for expensive operations | Backend dev | 0.5 day | Pipeline run: max 3 in-flight/project |
| Secure auto-OpenAPI: `/docs` auth-gated to authenticated users | Backend dev | 0.5 day | |
| Add API versioning prefix `/api/v1/` (enforce) | Backend dev | 1 day | All frontend axios calls updated |
| Add pagination to all list endpoints | Backend dev | 2 days | Projects, assessments, runs, history |
| Structured JSON logging via loguru | Backend dev | 0.5 day | Replace plain prints |
| Cost cap implementation in `llm.py` wrapper | Backend dev | 2 days | Per-run, per-project, per-platform; configurable |
| Schema validation on agent outputs before persistence | Backend dev | 1 day | Reject malformed agent output; log + retry |
| **Total** | | **~12 days** | |

---

### WS-3 · Database & Data Management
**Priority: High**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| Migrate from `Base.metadata.create_all()` to **Alembic** | Backend dev | 1 day | Convert existing schema to numbered migration files |
| Add `audit_log` table + helper for INSERT/UPDATE/DELETE capture | Backend dev | 1 day | See §7 |
| Add `users` table synced from Entra on first login | Backend dev | 0.5 day | |
| Add `created_by`, `updated_by`, `created_at`, `updated_at` to mutable tables | Backend dev | 0.5 day | |
| Add GIN indexes on JSON columns used in dashboard queries | DBA | 0.5 day | `analysis_runs.result`, `devops_assessments.result` |
| Provision Azure Database for PostgreSQL Flexible Server | Platform | 1 day | General Purpose, 4 vCore, 16 GB; pooler enabled |
| Migrate local data to Azure PostgreSQL | Platform + DBA | 1 day | pg_dump → pg_restore; validate row counts |
| Move DATABASE_URL to Azure Key Vault | Platform | 0.5 day | Managed identity binding to App Service |
| Set up PITR (7-day retention) | Platform | 0.5 day | Azure portal config |
| Test connection pooling under load | Backend dev | 1 day | PgBouncer transaction mode |
| Add `project_budget_usd` column for cost cap | Backend dev | 0.5 day | Default $20/month per project |
| **Total** | | **~8 days** | |

---

### WS-4 · AI & Pipeline Hardening
**Priority: High**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| Move LLM keys to Key Vault; remove from `platform_settings` plaintext | Backend dev | 1 day | Managed identity → Key Vault |
| Implement cost cap chain (Azure → OpenAI → rule-based fallback) | Backend dev | 2 days | Per-agent budget; per-run cap; per-project monthly budget |
| Implement multi-attempt retry with jitter on LLM 429/5xx | Backend dev | 1 day | 3 retries; exponential backoff |
| Implement schema validation on every agent output | Backend dev | 1 day | Pydantic models per agent return shape |
| Enforce accuracy scorer threshold (default 80) before export | Backend dev | 1 day | Below threshold → flagged-for-review badge |
| Persistent run queue (Phase 3 — using Arq or Celery) | Backend dev | 3 days | Pipeline survives worker restart |
| Per-run telemetry (tokens, cost, latency per agent) | Backend dev | 1 day | Stored in `analysis_runs.result.telemetry` |
| Rate limit pipeline-run endpoint (max 3 in-flight/project; 10 platform-wide) | Backend dev | 1 day | |
| RAG corpus growth path: instrument to detect when migration to pgvector is needed | Backend dev | 0.5 day | Log query latency + recall metrics |
| Integration test for all 8 agents (mock LLM responses) | QA | 2 days | pytest + responses library |
| **Total** | | **~13.5 days** | |

---

### WS-5 · ALM Integrations
**Priority: Medium**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| Productionise Jira adapter (retry, circuit breaker, schema validate) | Backend dev | 2 days | JQL filters; pagination; rate limit |
| Productionise Azure DevOps adapter | Backend dev | 2 days | WIQL filters; PAT rotation |
| Productionise GitHub adapter | Backend dev | 2 days | REST + GraphQL; org-level rate limits |
| Productionise Linear adapter | Backend dev | 1 day | GraphQL only |
| Productionise ServiceNow adapter | Backend dev | 2 days | OAuth flow |
| Move ALM credentials to Key Vault | Backend dev | 0.5 day | Per-project secret refs |
| Define VSM mapping contract (Pydantic) — used across all adapters | Backend dev | 1 day | |
| Failure handling: `PLATFORM_UNAVAILABLE` envelope; synthetic-data warning header | Backend dev | 0.5 day | |
| Integration tests using mock servers | QA | 2 days | respx / httpx_mock |
| UI: live connection health + last-fetch timestamps | Frontend dev | 1 day | |
| **Total** | | **~14 days** | |

---

### WS-6 · Infrastructure & CI/CD
**Priority: High**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| Write `Dockerfile` for FastAPI backend | Platform | 1 day | Python 3.13-slim; multi-stage; non-root user |
| Write `Dockerfile` for React frontend build | Platform | 0.5 day | Build stage + nginx serve stage |
| Set up Azure Container Registry | Platform | 0.5 day | |
| Provision Azure App Service (B2) for backend | Platform | 0.5 day | Auto-scale: CPU > 70% → +1; queue depth > 5 → +1; max 4 |
| Provision Azure Static Web Apps for frontend | Platform | 0.5 day | Linked to GitHub |
| Provision Azure Cache for Redis (Phase 2) | Platform | 0.5 day | C1 Standard |
| Provision Azure Key Vault + managed identity binding | Platform | 1 day | |
| Provision Azure OpenAI (gpt-4o, gpt-4o-mini) | Platform | 0.5 day | PTU sized for 5 concurrent runs |
| GitHub Actions: lint → test → build → push → deploy | Platform | 2 days | ruff, mypy, pytest gates |
| Staging environment as App Service slot | Platform | 1 day | Slot swap for zero-downtime |
| Custom domain + managed SSL | Platform | 0.5 day | |
| `.env.production` template with all required vars | Platform | 0.5 day | |
| Smoke test production deployment | QA | 1 day | |
| **Total** | | **~10 days** | |

---

### WS-7 · Observability & Operations
**Priority: High**

| Task | Owner | Effort | Notes |
|---|---|---|---|
| OpenTelemetry instrumentation for FastAPI | Backend dev | 1 day | Auto-tracks requests, DB calls, HTTP outbound |
| Trace propagation across LangGraph nodes | Backend dev | 1 day | Span per agent; LLM call as sub-span |
| App Insights SDK for React frontend | Frontend dev | 0.5 day | Page views, JS errors |
| Define alert rules in Azure Monitor | Platform | 1 day | P1: error rate > 5%; P2: DB failures; P3: pipeline P95 > 5 min |
| Connect alerts to Microsoft Teams webhook | Platform | 0.5 day | Engineering Effectiveness Ops channel |
| Health check `/api/v1/health` extended to check DB + Azure OpenAI | Backend dev | 0.5 day | |
| Build runbook: deploy, rollback, DB restore, secret rotation, LLM provider failover | Platform | 1.5 days | |
| Define SLA targets | Platform | 0.5 day | Availability 99.5%; API p95 < 1s; pipeline p95 < 5 min |
| **Total** | | **~6.5 days** | |

---

## 7. Data Model Evolution

### 7.1 New Tables

**`audit_log`** — immutable change history
```sql
CREATE TABLE audit_log (
  id            BIGSERIAL PRIMARY KEY,
  table_name    TEXT NOT NULL,
  record_id     TEXT NOT NULL,
  action        TEXT NOT NULL CHECK (action IN ('INSERT','UPDATE','DELETE','RUN_START','RUN_COMPLETE','EXPORT')),
  user_id       TEXT NOT NULL,        -- Entra ID object ID
  user_email    TEXT,
  changed_fields JSONB,
  context       JSONB,                 -- run_id, scenario, etc.
  recorded_at   TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_audit_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_user ON audit_log(user_id);
```

**`users`** — local user profile cache (synced from Entra ID on first login)
```sql
CREATE TABLE users (
  id            SERIAL PRIMARY KEY,
  entra_id      TEXT UNIQUE NOT NULL,
  email         TEXT UNIQUE NOT NULL,
  display_name  TEXT,
  role          TEXT NOT NULL CHECK (role IN ('platform_admin','engineering_lead','analyst','viewer')),
  portfolio     TEXT,
  last_login_at TIMESTAMPTZ,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);
```

**`scenario_approvals`** — captures who approved Option A/B/C and when
```sql
CREATE TABLE scenario_approvals (
  id            SERIAL PRIMARY KEY,
  project_id    TEXT REFERENCES projects(id),
  run_id        TEXT REFERENCES analysis_runs(id),
  scenario      TEXT NOT NULL CHECK (scenario IN ('option-a','option-b','option-c')),
  approver_id   INTEGER REFERENCES users(id),
  notes         TEXT,
  decided_at    TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX idx_approval_project_scenario ON scenario_approvals(project_id, scenario)
  WHERE decided_at IS NOT NULL;
```

**`export_log`** — every export (PPTX/Excel/PDF) recorded
```sql
CREATE TABLE export_log (
  id            SERIAL PRIMARY KEY,
  project_id    TEXT REFERENCES projects(id),
  run_id        TEXT REFERENCES analysis_runs(id),
  scenario      TEXT,
  format        TEXT NOT NULL CHECK (format IN ('pptx','xlsx','pdf','json','md')),
  user_id       INTEGER REFERENCES users(id),
  downloaded_at TIMESTAMPTZ DEFAULT NOW()
);
```

**`project_budgets`** — per-project LLM cost cap
```sql
CREATE TABLE project_budgets (
  project_id          TEXT PRIMARY KEY REFERENCES projects(id),
  monthly_cap_usd     NUMERIC(10,2) NOT NULL DEFAULT 20.00,
  current_month_spend NUMERIC(10,2) NOT NULL DEFAULT 0.00,
  last_reset_at       TIMESTAMPTZ DEFAULT NOW()
);
```

**`notifications`** — outbound notification log
```sql
CREATE TABLE notifications (
  id            SERIAL PRIMARY KEY,
  recipient_id  INTEGER REFERENCES users(id),
  type          TEXT NOT NULL,
  reference_id  TEXT,
  payload       JSONB,
  channel       TEXT DEFAULT 'teams',
  sent_at       TIMESTAMPTZ,
  status        TEXT DEFAULT 'pending' CHECK (status IN ('pending','sent','failed'))
);
```

### 7.2 Columns to Add

```sql
-- projects
ALTER TABLE projects        ADD COLUMN created_by TEXT;
ALTER TABLE projects        ADD COLUMN updated_by TEXT;
ALTER TABLE projects        ADD COLUMN auto_run BOOLEAN DEFAULT false;

-- vsm_snapshots / analysis_runs / devops_assessments
ALTER TABLE vsm_snapshots   ADD COLUMN created_by TEXT;
ALTER TABLE analysis_runs   ADD COLUMN initiated_by TEXT;
ALTER TABLE analysis_runs   ADD COLUMN total_cost_usd NUMERIC(10,4) DEFAULT 0.0;
ALTER TABLE analysis_runs   ADD COLUMN accuracy_score INTEGER;
ALTER TABLE devops_assessments ADD COLUMN created_by TEXT;
ALTER TABLE devops_assessments ADD COLUMN approved_by TEXT;
ALTER TABLE devops_assessments ADD COLUMN approved_at TIMESTAMPTZ;
```

### 7.3 Migration Strategy

Each change becomes a numbered Alembic migration file under `backend/alembic/versions/`:
```
001_initial_schema.py          # current schema as baseline
002_add_users_table.py
003_add_audit_log.py
004_add_scenario_approvals.py
005_add_export_log.py
006_add_project_budgets.py
007_add_notifications.py
008_add_created_by_columns.py
009_add_run_telemetry.py
010_add_gin_indexes.py
```

Alembic tracks applied migrations in `alembic_version` and runs only unapplied ones on app startup (or via `alembic upgrade head` in CI).

---

## 8. Security & Compliance

### 8.1 Authentication Flow

```
Browser → MSAL acquireTokenSilent (OIDC)
       → Entra ID returns access token (JWT)
         → Frontend attaches Bearer token to every axios request
           → FastAPI fastapi-azure-auth validates JWT against JWKS
             → JWT claims extracted: oid (user ID), email, groups
               → RBAC dependency maps groups → role
                 → request.state.user = {id, email, role, portfolio}
                   → Route handler executes
```

### 8.2 Security Controls

| Control | Implementation |
|---|---|
| Transport security | HTTPS only (Azure managed cert); HSTS via middleware |
| Authentication | Azure Entra ID OIDC; MFA enforced by tenant policy |
| Authorisation | JWT claim-based RBAC; 403 on insufficient role |
| Input validation | Pydantic model on every request body; 422 on violation |
| SQL injection | All queries via SQLAlchemy parameterised statements |
| XSS | React escapes by default; CSP header via middleware |
| CSRF | SameSite cookie policy; Bearer token not cookie-based |
| Rate limiting | 60 req/min per user; pipeline-run rate-limited separately |
| Secrets | Azure Key Vault; never in source code or committed env files |
| Audit trail | `audit_log` table records all mutations + run starts + exports |
| LLM safety | Prompts grounded in canonical PDLC taxonomy; outputs schema-validated |
| Cost protection | Per-run, per-project, per-platform cost caps; auto-fallback to rule-based |
| Error exposure | Centralised exception handler; no DB errors or stack traces to clients |
| Dependency scanning | GitHub Dependabot alerts on pip and npm packages |

### 8.3 Regulatory Alignment

The platform is designed for use in regulated environments (banking, healthcare). Key alignments:

- **PCI-DSS / SOX-style controls**: full audit trail with user identity on every state change; immutable run history with accuracy scores
- **AI assurance**: every AI output schema-validated; accuracy threshold gates export; rule-based fallback preserves auditability when LLM unavailable
- **Data residency**: all data (including LLM call telemetry) remains in-region; Azure OpenAI deployment in same region as App Service
- **Right to explanation**: every recommendation traceable to source — VSM snapshot ID, RAG retrieval hits, LLM input/output stored against the run

---

## 9. Integration Architecture

### 9.1 ALM Adapter Pattern (Target)

```
┌─────────────────────────────────────────────────────────────┐
│  ALM ADAPTER (one per tool, common interface)               │
│                                                             │
│  1. Fetch credentials from Key Vault                        │
│     (managed identity → Key Vault → secret value)           │
│                                                             │
│  2. Circuit breaker check                                   │
│     5 consecutive failures → OPEN for 60s                   │
│                                                             │
│  3. HTTP call with retry + timeout                          │
│     GET {api_base}/issues?jql=...                           │
│     Authorization: Bearer {token}                           │
│     Retries: 2 with exponential backoff                     │
│     Timeout: 30s                                            │
│                                                             │
│  4. Response validation (Pydantic schema)                   │
│     If invalid → PLATFORM_UNAVAILABLE error                 │
│                                                             │
│  5. Map raw response → VSM input                            │
│     map_to_vsm(raw) → vsm_data dict                         │
│                                                             │
│  6. Persist to vsm_snapshots                                │
│     source='alm'                                            │
│                                                             │
│  7. Audit log                                               │
│     {user_id, project_id, tool, row_count}                  │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Adapter Contract

```python
class BaseAdapter(Protocol):
    def __init__(self, config: ALMConfig): ...
    async def health_check(self) -> bool: ...
    async def fetch(self) -> dict[str, Any]: ...
    def map_to_vsm(self, raw: dict) -> dict[str, Any]: ...
```

### 9.3 LLM Call Architecture (Target)

```
┌─────────────────────────────────────────────────────────────┐
│  LLM WRAPPER (backend/agents/llm.py)                        │
│                                                             │
│  1. Pre-flight check                                        │
│     - Per-run cost cap remaining > 0                        │
│     - Per-project monthly budget > 0                        │
│     - Platform-wide concurrent LLM calls < limit            │
│                                                             │
│  2. Build messages (system prompt + RAG context + user)     │
│                                                             │
│  3. Try Azure OpenAI                                        │
│     - Timeout 60s; retries 3 with jittered backoff          │
│     - On success: record tokens + cost                      │
│                                                             │
│  4. Fallback to OpenAI public API                           │
│     - Only if Azure not configured OR exhausted             │
│                                                             │
│  5. Fallback to rule-based path                             │
│     - If both providers fail                                │
│     - Output badged "Rule-based"                            │
│                                                             │
│  6. Telemetry persisted to analysis_runs.result.telemetry   │
│     {agent, provider, model, tokens, cost_usd, latency_ms}  │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Infrastructure & Deployment

### 10.1 Azure Resource Group Layout

```
Resource Group: rg-pdlc-vsm-prod (East US 2)
│
├── App Service Plan: asp-pdlc-vsm-prod (B2, Linux)
│   └── App Service: app-pdlc-vsm-api (Python 3.13)
│
├── Static Web App: stapp-pdlc-vsm-frontend
│
├── Azure Database for PostgreSQL Flexible Server
│   ├── Server: psql-pdlc-vsm-prod
│   ├── DB: pdlc_vsm
│   └── Replica: psql-pdlc-vsm-read
│
├── Azure Cache for Redis (Phase 2): redis-pdlc-vsm-prod
│
├── Azure OpenAI: aoai-pdlc-vsm-prod
│   ├── Deployment: gpt-4o (PTU 30K TPM)
│   └── Deployment: gpt-4o-mini (PAYG 60K TPM)
│
├── Azure Container Registry: acr-pdlc-vsm-prod
│
├── Key Vault: kv-pdlc-vsm-prod
│   ├── SECRET: DATABASE-URL
│   ├── SECRET: AZURE-OPENAI-API-KEY
│   ├── SECRET: OPENAI-API-KEY (fallback)
│   ├── SECRET: JIRA-API-TOKEN
│   ├── SECRET: ADO-PERSONAL-ACCESS-TOKEN
│   ├── SECRET: GITHUB-PAT
│   └── SECRET: APPINSIGHTS-CONNECTION-STRING
│
├── Application Insights: appi-pdlc-vsm-prod
│
└── Log Analytics Workspace: law-pdlc-vsm-prod
```

### 10.2 Environment Variables (production)

```bash
# Identity
AZURE_TENANT_ID=<tenant ID>
AZURE_CLIENT_ID=<App registration client ID>

# Database (from Key Vault)
DATABASE_URL=postgresql+asyncpg://...

# Redis (Phase 2)
REDIS_URL=rediss://...

# Azure OpenAI (from Key Vault)
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://aoai-pdlc-vsm-prod.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# OpenAI fallback
OPENAI_API_KEY=<from Key Vault>
OPENAI_MODEL=gpt-4o-mini

# Application
PORT=8001
CORS_ORIGINS=https://pdlc-vsm.internal
API_VERSION=v1
LLM_COST_CAP_USD=5.0

# ALM (per-project, from Key Vault)
JIRA_URL=https://...
JIRA_USERNAME=...
JIRA_API_TOKEN=...
ADO_ORG_URL=https://dev.azure.com/...
ADO_PERSONAL_ACCESS_TOKEN=...

# Observability
APPLICATIONINSIGHTS_CONNECTION_STRING=<from Key Vault>
LOG_LEVEL=INFO
OTEL_SERVICE_NAME=pdlc-vsm-api
```

### 10.3 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml (abbreviated)

on:
  push:
    branches: [main]      # deploys to staging
  release:
    types: [published]    # deploys to production

jobs:
  test:
    - pip install -r requirements.txt
    - ruff check .
    - mypy backend
    - pytest backend/tests
    - npm ci && npm run lint

  build-backend:
    - docker build -t acr-pdlc-vsm-prod.azurecr.io/api:$SHA .
    - docker push ...

  build-frontend:
    - npm ci && npm run build
    - Deploy to Azure Static Web Apps

  deploy-staging:
    needs: [test, build-backend, build-frontend]
    - az webapp deployment slot swap → staging slot

  smoke-test:
    - GET /api/v1/health → expect 200
    - POST /api/v1/agents/seed-result/{demo_project_id} → expect 201
    - GET /api/v1/analysis/{demo_project_id}/bottlenecks → expect 200

  deploy-production:           # manual approval gate
    needs: [smoke-test]
    - az webapp deployment slot swap → production slot
```

---

## 11. Observability & Operations

### 11.1 SLA Targets

| Metric | Target |
|---|---|
| Availability | 99.5% monthly |
| API p95 response time (non-pipeline) | < 1 second |
| Pipeline run p95 | < 5 minutes |
| Pipeline accuracy score (mean) | > 80 |
| LLM provider availability | 99.9% (combining Azure + OpenAI fallback) |
| DB query p95 | < 200ms |
| Dashboard load time (with cache) | < 2 seconds |

### 11.2 Alert Rules

| Condition | Severity | Channel |
|---|---|---|
| API error rate > 5% (5-min window) | P1 | Teams on-call |
| Pipeline failure rate > 20% (1-hour window) | P1 | Teams on-call |
| Azure OpenAI rate-limit responses sustained | P1 | Teams on-call |
| App Service CPU > 85% (10-min avg) | P2 | Teams Ops |
| PostgreSQL connection failures > 3 | P1 | Teams on-call |
| Pipeline run p95 > 8 minutes | P2 | Teams Ops |
| Accuracy score average < 70 over 1 hour | P2 | Teams Ops |
| Cost cap breached for any project | P3 | Email + Teams |
| Disk usage > 80% | P3 | Email |

### 11.3 Runbook Summary

| Scenario | Steps |
|---|---|
| **New deployment** | Push to `main` → CI runs → staging deploy → smoke test passes → manual approve → production swap |
| **Rollback** | `az webapp deployment slot swap --slot staging` (reverts to previous build) |
| **DB restore** | Azure Portal → Flexible Server → Point-in-Time Restore → specify timestamp |
| **Secret rotation** | Update secret in Key Vault → restart App Service (managed identity re-fetches on startup) |
| **LLM provider failover** | Set `AZURE_OPENAI_API_KEY` to empty in Key Vault → restart → falls back to OpenAI; or to empty for both → rule-based mode |
| **Pipeline backlog** | Pause `auto_run` on noisy projects via Settings → wait for queue to drain → re-enable progressively |
| **Cost cap breach** | Platform Admin reviews `project_budgets` → raise cap or pause auto-runs for that project → notify Engineering Lead |

---

## 12. Phased Delivery Plan

### Phase 1 — Hardened MVP (Q3 2026, ~8 weeks)
**Goal:** Platform is securely deployable to internal users.

| Workstream | Deliverables |
|---|---|
| WS-1 Auth | Entra ID OIDC, RBAC on all routes, MSAL in frontend |
| WS-2 API | Pydantic validation enforced, centralised exception handler, CORS config, rate limiting, cost cap |
| WS-3 Database | Alembic, audit_log, users, Azure PostgreSQL provisioned |
| WS-4 AI | Cost cap chain (Azure → OpenAI → rule-based), schema validation, accuracy threshold enforced |
| WS-6 Infra | Dockerfile, Azure App Service + Static Web Apps, Key Vault, GitHub Actions CI/CD |
| WS-7 Observability | OpenTelemetry, App Insights, P1/P2 alerts to Teams |

**Exit criteria:** 4 roles logging in via Entra ID; all mutations audit-logged; deployment via CI/CD; pipeline runs cost-capped; health check passing on Azure.

---

### Phase 2 — Connected Platform (Q4 2026, ~6 weeks)
**Goal:** Live ALM ingestion, scheduled runs, board-ready exports.

| Workstream | Deliverables |
|---|---|
| WS-5 ALM | Productionised Jira, Azure DevOps, GitHub, Linear, ServiceNow adapters with circuit breakers |
| WS-2 API | OpenAPI docs published, pagination on list endpoints, API versioning |
| WS-3 Database | scenario_approvals table; export_log; notifications; project_budgets |
| WS-4 AI | Persistent telemetry per run; accuracy reporting in dashboard |
| Frontend | React Query for server state; form validation with react-hook-form + Zod; error boundaries; PPTX/Excel/PDF export from UI |
| Infra | Redis cache provisioned; APScheduler with Redis job store |

**Exit criteria:** ALM ingestion working for all 5 connectors; scheduled runs surviving worker restarts; PPTX/Excel/PDF export from UI; portfolio-wide dashboard live.

---

### Phase 3 — Scale & Assurance (Q1 2027, ~4 weeks)
**Goal:** Feature-complete, performant, auditable, operationally mature.

| Area | Deliverables |
|---|---|
| Performance | Agent Orchestration extracted to burstable container; persistent run queue (Arq/Celery) |
| AI | RAG corpus migrated to pgvector if > 5MB; multi-agent self-critique |
| Features | Full-text search across projects and runs; document attachment for assessments; multi-tenant isolation |
| Testing | Full pytest suite + Playwright e2e + LLM accuracy benchmark |
| Compliance | Audit trail UI exposed to Viewer role; export watermarking; full DR test; security pen-test |
| Operations | Complete runbook; SLO dashboard; quarterly chaos test |

**Exit criteria:** 50 concurrent users with no degradation; audit trail visible to Viewer role; pen-test findings remediated; DR test passes within stated RTO.

---

## 13. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Entra ID app registration delayed by IT | Medium | High | Raise as dependency week 1 of Phase 1; use test tenant meanwhile |
| Azure OpenAI capacity insufficient for concurrent runs | Medium | High | Phase 1 provisions PTU with auto-fallback to PAYG; per-tenant concurrency caps |
| LLM cost overrun on first production rollout | High | Medium | Per-run, per-project, per-platform cost caps from day one; rule-based fallback always available |
| Accuracy score < threshold blocking exports | Medium | Medium | Manual override path in UI; threshold tunable; root-cause analysis runbook |
| Pipeline backgrounded but worker killed during run | High | Medium | Phase 1: surface failures clearly; document re-run; Phase 3: persistent queue removes the risk |
| ALM API rate limits hit during bulk fetch | Medium | Medium | Adapter implements adaptive pagination + backoff; analyst-visible "fetch in progress" status |
| PostgreSQL migration causes data loss | Low | High | pg_dump before migration; validate row counts; keep local DB as fallback for 2 weeks |
| MSAL / React Query library conflicts | Low | Medium | Introduce in isolated routes first (Dashboard); expand incrementally |
| Azure Key Vault managed identity blocked by IT policy | Medium | Medium | Document Key Vault access pattern; get IT approval in parallel with WS-1 |
| Scope creep adding new modules before hardening done | High | Medium | Phase 1 is strictly hardening only; new feature requests go to Phase 3 backlog |
| RAG retrieval quality degrades as KB grows | Low | Low | Instrument now; trigger pgvector migration at 5MB threshold |
| LLM provider deprecates model mid-programme | Low | Medium | Multi-provider fallback chain (Azure → OpenAI); abstract model name in config |

---

*Document prepared by Cognizant Engineering Effectiveness · May 2026*
*For questions: refer to the Engineering Effectiveness Programme Lead or raise an issue in the project repository.*
