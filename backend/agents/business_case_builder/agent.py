"""
Business Case Builder Agent
Generates comprehensive business cases for each future state scenario:
  - Investment breakdown (tools, infra, implementation, training, change)
  - Annual benefits (TTM, productivity, quality, ops)
  - ROI timeline and payback period
  - Org change management requirements
  - Tools & platform changes
  - DevSecOps changes
  - AI Ops / production support changes
  - Product-centric ways of working changes
"""
import logging
from ..state import VSMAgentState
from ..llm import ainvoke, has_llm

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Editable Cost Model
# ─────────────────────────────────────────────────────────────────────────────
# Structured, line-by-line cost breakdown used by the Business Case > ROI view.
# Every entry has an `id` so per-project overrides can replace individual lines
# without touching the rest. Custom lines added via the UI use ids prefixed
# `custom-`. All amounts in USD; ranges use {low, high}; flat values use {amount}.
#
# Defaults assume:
#   - FTE loaded cost: $150K / year (override-able per project)
#   - 1 product pod = 8 FTE in Option A baseline
#   - LLM token costs midrange from operatingModel.js agentMonitoring.costs
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_FTE_LOADED_USD = 150_000


# ─────────────────────────────────────────────────────────────────────────────
# Token Optimisation Levers
# ─────────────────────────────────────────────────────────────────────────────
# Eight realistic techniques to reduce LLM token spend in Options B and C.
# `reduction_pct` is the reduction applied to the *remaining* token cost (i.e.
# they compound multiplicatively, not additively).
#
# Levers are enabled per-scenario via cost_model_overrides.token_optimizations:
#   {
#     "token_optimizations": {
#       "option_b": ["model_tiering", "semantic_caching"],
#       "option_c": ["model_tiering", "semantic_caching", "batch_api",
#                    "ptu_provisioned", "prompt_compression"]
#     }
#   }
#
# Frontend toggles each lever and shows the live impact on the token line and
# rolled-up ROI. Each lever notes effort, prerequisites, and which scenarios it
# applies to.
# ─────────────────────────────────────────────────────────────────────────────

TOKEN_OPTIMIZATIONS = {
    "model_tiering": {
        "id":           "model_tiering",
        "name":         "Model tiering / routing",
        "description":  "Route to cheap models (Haiku / gpt-4o-mini / Gemini Flash) for routing, summarisation, classification, and low-stakes generation. Reserve frontier models (GPT-4o / Claude Opus) only for reasoning-heavy agents (Architecture, Compliance, Code Review on novel patterns).",
        "applies_to":   ["option-b", "option-c"],
        "reduction_pct": 40,
        "effort":       "Medium",
        "prerequisites":"Agent-by-agent complexity classification; per-agent model selection in llm.py wrapper",
    },
    "semantic_caching": {
        "id":           "semantic_caching",
        "name":         "Semantic caching",
        "description":  "Cache LLM responses keyed by semantic similarity of input. Cache hit rate typically 30–50% on stable codebases (code formatting, standard SAST rules, common patterns).",
        "applies_to":   ["option-b", "option-c"],
        "reduction_pct": 30,
        "effort":       "Medium",
        "prerequisites":"Redis + embedding store (Helicone / GPTCache / DIY with pgvector + Postgres)",
    },
    "batch_api": {
        "id":           "batch_api",
        "name":         "Batch / async inference",
        "description":  "Use OpenAI Batch API or Anthropic Message Batches API at 50% discount for non-time-sensitive agents (PIR generation, dependency scans, capacity forecasts, weekly compliance evidence packs).",
        "applies_to":   ["option-b", "option-c"],
        "reduction_pct": 15,
        "effort":       "Low",
        "prerequisites":"Identify which agents are deferrable; queue infrastructure for async results",
    },
    "ptu_provisioned": {
        "id":           "ptu_provisioned",
        "name":         "PTU / Provisioned Throughput",
        "description":  "Azure OpenAI Provisioned Throughput Units at sustained volume save 30–40% vs Pay-As-You-Go. Best for predictable high-volume agents (Code Generator, Code Reviewer).",
        "applies_to":   ["option-c"],
        "reduction_pct": 18,
        "effort":       "Low",
        "prerequisites":"Sustained monthly token volume > $20K/month; capacity commitment 1+ months",
    },
    "prompt_compression": {
        "id":           "prompt_compression",
        "name":         "Prompt compression",
        "description":  "LLMLingua / structured prompts cut input tokens 30–50%. System prompts and few-shot examples often consume 60–80% of input — moving static context to fine-tuned model knowledge or RAG retrieval pays off quickly.",
        "applies_to":   ["option-b", "option-c"],
        "reduction_pct": 12,
        "effort":       "Medium",
        "prerequisites":"LLMLingua (or similar) integration; prompt-engineering pass per agent",
    },
    "rule_based_prefilter": {
        "id":           "rule_based_prefilter",
        "name":         "Rule-based pre-filter",
        "description":  "Schema validation, code formatting, dependency analysis, and routine SAST checks use deterministic rules first. LLM is called only when rules can't resolve ambiguity.",
        "applies_to":   ["option-b", "option-c"],
        "reduction_pct": 10,
        "effort":       "Medium",
        "prerequisites":"Per-agent decision-tree: when can we skip the LLM call entirely?",
    },
    "agent_consolidation": {
        "id":           "agent_consolidation",
        "name":         "Agent consolidation",
        "description":  "Merge tightly-coupled agents (e.g., Code Generator + Code Reviewer) into multi-turn calls within a single agent. Cuts orchestration overhead 30–40% on consolidated agent pairs.",
        "applies_to":   ["option-c"],
        "reduction_pct": 8,
        "effort":       "High",
        "prerequisites":"Re-architect agent boundaries; preserve evaluation suite separation",
    },
    "fine_tuned_oss": {
        "id":           "fine_tuned_oss",
        "name":         "Fine-tuned open-source models",
        "description":  "Llama / Mistral / DeepSeek fine-tuned for repetitive narrow tasks (code formatting, ADR templating, standard test generation). 5–10× cheaper per call than GPT-4o, can match quality on narrow domains.",
        "applies_to":   ["option-c"],
        "reduction_pct": 15,
        "effort":       "Very High",
        "prerequisites":"MLOps capability (typically only viable on Homegrown or BMAD platform); training data; eval suite; ongoing model refresh",
    },
}


def apply_token_optimizations(base_low: float, base_high: float, enabled_ids: list[str], scenario_id: str):
    """Apply enabled token optimizations as compounding reductions on the token line.

    Returns (new_low, new_high, effective_reduction_pct, applied_levers_meta).
    """
    if not enabled_ids:
        return base_low, base_high, 0.0, []
    factor_low, factor_high = 1.0, 1.0
    applied = []
    for lid in enabled_ids:
        lever = TOKEN_OPTIMIZATIONS.get(lid)
        if not lever or scenario_id not in lever.get("applies_to", []):
            continue
        r = lever["reduction_pct"] / 100.0
        factor_low  *= (1 - r)
        factor_high *= (1 - r)
        applied.append({"id": lid, "name": lever["name"], "reduction_pct": lever["reduction_pct"]})
    return (
        base_low * factor_low,
        base_high * factor_high,
        round((1 - factor_low) * 100, 1),
        applied,
    )

DEFAULT_COST_MODEL = {
    "currency": "USD",
    "fte_loaded_cost_usd":     DEFAULT_FTE_LOADED_USD,
    "pods_in_portfolio":       4,

    # Current state — what a single pod costs today, annually
    "current_state_per_pod_annual": [
        {"id": "csa-people",   "category": "People",         "label": "8 FTE per pod × $150K loaded",                "amount": 1_200_000, "editable": True},
        {"id": "csa-tools",    "category": "Tools",          "label": "Copilot Enterprise + IDE AI plugins",          "amount":   100_000, "editable": True},
        {"id": "csa-infra",    "category": "Infrastructure", "label": "Cloud compute + CI/CD runners",                "amount":    80_000, "editable": True},
        {"id": "csa-lic",      "category": "Tools",          "label": "ALM + observability + security tool licences", "amount":    60_000, "editable": True},
    ],

    # Option B — one-time migration cost AND ongoing per-pod annual cost
    "option_b": {
        "one_time_migration": [
            {"id": "b-tools",    "category": "Tools",          "label": "Selective AI platforms for the 11 high-impact agents",   "low": 350_000, "high":   600_000, "editable": True},
            {"id": "b-infra",    "category": "Infrastructure", "label": "AI compute + model hosting (half-fleet sizing)",          "low": 180_000, "high":   300_000, "editable": True},
            {"id": "b-impl",     "category": "Implementation", "label": "Custom LangGraph build for the 11 agents",                "low": 300_000, "high":   650_000, "editable": True},
            {"id": "b-training", "category": "Training",       "label": "Reskill 4 dedicated + 2 fractional roles",                "low": 100_000, "high":   200_000, "editable": True},
            {"id": "b-chgmgmt",  "category": "Change Mgmt",    "label": "Role restructuring for agent-covered phases",             "low": 120_000, "high":   180_000, "editable": True},
        ],
        "ongoing_per_pod_annual": [
            {"id": "b-people",     "category": "People",        "label": "~4.7 FTE per pod (4 dedicated + 0.7 fractional) × $150K", "amount":  705_000, "editable": True},
            {"id": "b-tokens",     "category": "LLM Tokens",    "label": "Agent platform LLM API spend — $8K–$18K/month",          "low":      96_000, "high":   216_000, "editable": True},
            {"id": "b-agentmaint", "category": "Agent Maint.",  "label": "Prompt eval, gold-set tests, drift detection",            "amount":    60_000, "editable": True},
            {"id": "b-platform",   "category": "Platform",      "label": "Observability + vector DB + agent runtime infra",         "amount":    30_000, "editable": True},
        ],
    },

    # Option C — one-time migration cost AND ongoing per-pod annual cost
    # Note: platform choice (homegrown/stump/bmad/copilot_workspace) further
    # adjusts these via apply_c_platform() — see C_PLATFORM_OPTIONS below.
    "option_c": {
        "one_time_migration": [
            {"id": "c-tools",    "category": "Tools",          "label": "AI-native platform stack — all 21 agents",                "low":  800_000, "high": 1_400_000, "editable": True},
            {"id": "c-infra",    "category": "Infrastructure", "label": "Enterprise AI compute + fine-tuning infra (full fleet)",  "low":  500_000, "high":   900_000, "editable": True},
            {"id": "c-impl",     "category": "Implementation", "label": "End-to-end LangGraph orchestration for all 21 agents",    "low":  750_000, "high": 1_400_000, "editable": True},
            {"id": "c-training", "category": "Training",       "label": "Intensive reskill of retained Definer / Builder / Arch",  "low":  200_000, "high":   300_000, "editable": True},
            {"id": "c-chgmgmt",  "category": "Change Mgmt",    "label": "Major workforce transition + ethics + regulatory",        "low":  300_000, "high":   500_000, "editable": True},
        ],
        "ongoing_per_pod_annual": [
            {"id": "c-people",     "category": "People",        "label": "~2.2 FTE per pod (2 dedicated + 0.2 fractional Architect) × $150K", "amount":  330_000, "editable": True},
            {"id": "c-tokens",     "category": "LLM Tokens",    "label": "Full-fleet LLM API spend — $20K–$45K/month",                          "low":     240_000, "high":   540_000, "editable": True},
            {"id": "c-agentmaint", "category": "Agent Maint.",  "label": "Continuous eval pipeline, daily gold-set, red-team",                   "amount":   120_000, "editable": True},
            {"id": "c-platform",   "category": "Platform",      "label": "Platform subscription / per-seat (varies by C platform choice)",      "low":      60_000, "high":   180_000, "editable": True},
        ],
    },
}


def _amt(line):
    """Return the midpoint amount of a cost line (handles {amount} or {low,high})."""
    if "amount" in line:
        return float(line["amount"])
    return (float(line.get("low", 0)) + float(line.get("high", 0))) / 2


def _sum_lines(lines):
    return sum(_amt(l) for l in lines or [])


def compute_cost_summary(cost_model: dict) -> dict:
    """Roll up a cost model into a per-pod and portfolio-level summary."""
    pods = int(cost_model.get("pods_in_portfolio") or 4) or 1
    a_per_pod   = _sum_lines(cost_model.get("current_state_per_pod_annual"))
    b_one_time  = _sum_lines(cost_model.get("option_b", {}).get("one_time_migration"))
    b_per_pod   = _sum_lines(cost_model.get("option_b", {}).get("ongoing_per_pod_annual"))
    c_one_time  = _sum_lines(cost_model.get("option_c", {}).get("one_time_migration"))
    c_per_pod   = _sum_lines(cost_model.get("option_c", {}).get("ongoing_per_pod_annual"))
    return {
        "pods_in_portfolio":          pods,
        "current_state_per_pod":      a_per_pod,
        "current_state_portfolio":    a_per_pod * pods,
        "option_b": {
            "one_time":                    b_one_time,
            "ongoing_per_pod":             b_per_pod,
            "ongoing_portfolio":           b_per_pod * pods,
            "annual_savings_per_pod":      a_per_pod - b_per_pod,
            "annual_savings_portfolio":    (a_per_pod - b_per_pod) * pods,
            "payback_months":              _payback(b_one_time, (a_per_pod - b_per_pod) * pods),
        },
        "option_c": {
            "one_time":                    c_one_time,
            "ongoing_per_pod":             c_per_pod,
            "ongoing_portfolio":           c_per_pod * pods,
            "annual_savings_per_pod":      a_per_pod - c_per_pod,
            "annual_savings_portfolio":    (a_per_pod - c_per_pod) * pods,
            "payback_months":              _payback(c_one_time, (a_per_pod - c_per_pod) * pods),
        },
    }


def _payback(one_time: float, annual_saving: float) -> float:
    if annual_saving <= 0:
        return -1.0  # never pays back from cost savings alone
    return round(one_time / annual_saving * 12, 1)


def merge_cost_model(overrides: dict | None) -> dict:
    """Apply per-project line-level overrides to the default cost model.

    Override shape (all fields optional, partial merges supported):
      {
        "fte_loaded_cost_usd": 175000,
        "pods_in_portfolio":   6,
        "lines": {
          "csa-people": {"amount": 1300000, "label": "8 FTE × $162K"},
          "custom-foo": {"category": "Tools", "label": "Extra ALM seat", "amount": 24000},
          "b-tokens":   null   # null deletes the line
        }
      }
    """
    import copy
    base = copy.deepcopy(DEFAULT_COST_MODEL)
    if not overrides:
        return base
    if "fte_loaded_cost_usd" in overrides:
        base["fte_loaded_cost_usd"] = overrides["fte_loaded_cost_usd"]
    if "pods_in_portfolio" in overrides:
        base["pods_in_portfolio"] = overrides["pods_in_portfolio"]

    line_overrides = overrides.get("lines") or {}
    # Group all line collections so we can patch by id
    collections = [
        ("current_state_per_pod_annual", base["current_state_per_pod_annual"]),
        ("option_b/one_time_migration",  base["option_b"]["one_time_migration"]),
        ("option_b/ongoing_per_pod",     base["option_b"]["ongoing_per_pod_annual"]),
        ("option_c/one_time_migration",  base["option_c"]["one_time_migration"]),
        ("option_c/ongoing_per_pod",     base["option_c"]["ongoing_per_pod_annual"]),
    ]
    for _, coll in collections:
        for i, line in enumerate(list(coll)):
            lid = line["id"]
            if lid in line_overrides:
                patch = line_overrides[lid]
                if patch is None:
                    coll.remove(line)
                else:
                    coll[i] = {**line, **patch}
                # Mark as consumed so we don't add it again as a custom line
                line_overrides[lid] = "_applied"

    # Any leftover overrides that didn't match a default id become custom lines.
    # Custom line targets which collection via "_collection" field.
    coll_index = {
        "current_state_per_pod_annual": base["current_state_per_pod_annual"],
        "option_b_one_time":            base["option_b"]["one_time_migration"],
        "option_b_ongoing":             base["option_b"]["ongoing_per_pod_annual"],
        "option_c_one_time":            base["option_c"]["one_time_migration"],
        "option_c_ongoing":             base["option_c"]["ongoing_per_pod_annual"],
    }
    for lid, patch in line_overrides.items():
        if patch == "_applied" or patch is None:
            continue
        target = (patch or {}).get("_collection")
        if target in coll_index:
            line = {k: v for k, v in patch.items() if k != "_collection"}
            line.setdefault("id", lid)
            line.setdefault("editable", True)
            coll_index[target].append(line)

    # ── Apply token optimisations (per scenario) ─────────────────────────────
    # Reduces the LLM-Tokens line in each scenario's ongoing-cost collection.
    token_opts = (overrides or {}).get("token_optimizations") or {}
    for scenario_key, ongoing_path, line_id in [
        ("option_b", base["option_b"]["ongoing_per_pod_annual"], "b-tokens"),
        ("option_c", base["option_c"]["ongoing_per_pod_annual"], "c-tokens"),
    ]:
        enabled = token_opts.get(scenario_key) or []
        if not enabled:
            continue
        for line in ongoing_path:
            if line.get("id") != line_id:
                continue
            base_low  = float(line.get("low",  line.get("amount", 0)) or 0)
            base_high = float(line.get("high", line.get("amount", 0)) or 0)
            new_low, new_high, eff_pct, applied = apply_token_optimizations(
                base_low, base_high, enabled, scenario_key.replace("_", "-")
            )
            line["low"]  = round(new_low)
            line["high"] = round(new_high)
            line.pop("amount", None)
            line["token_optimizations_applied"] = applied
            line["token_optimizations_effective_reduction_pct"] = eff_pct
            line["token_optimizations_baseline"] = {"low": int(base_low), "high": int(base_high)}
            line["label"] = (line.get("label","").split(" — optimisations applied")[0]
                             + f" — optimisations applied ({eff_pct:.0f}% reduction)")
            break

    return base


# ─────────────────────────────────────────────────────────────────────────────
# Option C — Platform Choice Catalogue
# ─────────────────────────────────────────────────────────────────────────────
# Option C ("AI-Native — Full 21-Agent Fleet") can be delivered in four ways.
# The selected platform overrides org_changes, tools_changes, devsecops_changes,
# aiops_changes, product_centric_changes AND nudges investment + timeline.
#
# API: GET /api/v1/analysis/{project_id}/business-case/option-c?platform=<id>
# Default (no platform query param): the base "homegrown" view is returned.
# ─────────────────────────────────────────────────────────────────────────────

C_PLATFORM_OPTIONS = {
    "homegrown": {
        "id":       "homegrown",
        "name":     "Homegrown / Custom Build",
        "tagline":  "Build all 21 agents in-house using LangGraph + Azure OpenAI — full control, no vendor lock-in",
        "investment_delta_text":  "Baseline. Full build cost; no platform licence. Higher upfront, lower long-term per-seat cost at scale.",
        "investment_delta_usd_low":  0,
        "investment_delta_usd_high": 0,
        "timeline_delta_weeks":   0,
        "production_ready_weeks": 26,
        "pros": [
            "Full architectural control — swap LLM providers, orchestration frameworks, vector stores independently",
            "No vendor lock-in — OSS components (LangGraph + Azure OpenAI + Postgres + Langfuse)",
            "Custom training on proprietary internal data without third-party exposure",
            "Best long-term unit economics at scale once amortised across 21 agents",
            "Integration with any best-of-breed tooling regardless of vendor compatibility"
        ],
        "cons": [
            "Significant engineering effort: 6–8 person AI Platform Engineering team plus dedicated MLOps capability",
            "Platform reliability is fully your responsibility — SRE overhead for the entire agent infrastructure",
            "Slowest path to value: 20–28 weeks before full 21-agent autonomous coverage achieved",
            "LLMOps and prompt-engineering talent is scarce and expensive to hire and retain",
            "Continuous platform-roadmap cost — internal R&D required to keep pace with frontier models"
        ],
        "platform_ops_team": {
            "name": "AI Platform Engineering",
            "size": "6–8 people",
            "roles": ["Platform Architect", "LLM Engineer ×2", "MLOps / LLMOps Engineer",
                      "SRE ×2", "Prompt / Policy Engineer", "Agent Eval Engineer"]
        },
        "agents_construction": (
            "All 21 agents authored in-house using LangGraph StateGraph orchestration. "
            "Each agent: custom system prompt, MCP tool wiring, gold-set evaluation suite, drift monitoring. "
            "Prompt registry under git version control. Continuous evaluation pipeline runs daily 50-sample gold-set per agent."
        ),
        "tools_changes": [
            "Build custom multi-agent orchestration layer: LangGraph StateGraph + Azure OpenAI + MCP tool servers — covers all 21 agents",
            "Author and version-control prompt registry in-house; LLM-agnostic so providers can be swapped",
            "Deploy open-source observability (Langfuse / LangSmith / OpenTelemetry) for agent traces, latency, cost telemetry",
            "Stand up pgvector or Pinecone as the canonical knowledge store; ingest org docs, runbooks, compliance frameworks",
            "AI-native ALM replaces traditional Jira / ADO; Jira retained read-only as compliance mirror",
            "Fully automated CI/CD/CD pipelines with AI decisions at every gate — built on top of existing GitOps stack"
        ],
        "devsecops_changes": [
            "Fully AI-managed DevSecOps pipeline from code commit to production — agents authored and maintained in-house",
            "AI security agents built on the same LangGraph framework as the rest of the fleet — single platform, single observability",
            "Autonomous compliance management (SOC2, ISO 27001, PCI-DSS, SOX) — audit evidence auto-generated by Compliance Agent",
            "AI-generated and maintained Architecture Decision Records, threat models, and security reviews — Product Builder reviews novel patterns"
        ],
        "aiops_changes": [
            "Fully autonomous AIOps — zero Level 1 / Level 2 human intervention; in-house Monitor / Triage / Rollback Agents",
            "Self-healing, self-scaling, and self-documenting production systems — runbooks generated and maintained by AI",
            "AI incident commander manages all production events; Product Builder receives async handoff packages for Sev-1",
            "Continuous capacity, performance, and cost optimisation by FinOps-trained agents — internally tuned"
        ],
        "product_centric_changes": [
            "Abolish traditional SDLC phase gates — move to continuous product evolution model where in-house agents execute end-to-end",
            "Product Definer sets weekly outcome goals in natural language; AI agents decompose, build, test, deploy autonomously",
            "Real-time customer intent detection feeds AI-driven roadmap prioritisation — no human PM authoring stories",
            "Proactive feature generation: AI identifies market opportunities; Product Definer chooses which proposals to greenlight"
        ],
        "org_changes_override": [
            "Stand up an AI Platform Engineering team (6–8) as a permanent capability — this team owns the full agent lifecycle",
            "Establish in-house AI / LLMOps practice — hiring is a critical-path activity for the first 12 weeks"
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–6)",
             "focus": "Hire/transfer the 6–8 person Platform Engineering team. Stand up LangGraph + Azure OpenAI infra. Build first 5 high-impact agents (Code Generator, Code Reviewer, QA Orchestrator, Release Gate, Monitor) in shadow mode."},
            {"phase": "Pilot (Weeks 7–14)",
             "focus": "Add the remaining 16 agents progressively. Run all 21 in shadow mode alongside human teams. Wire MCP tools, evaluation suite, drift detection. Begin Product Definer + Product Builder role definition."},
            {"phase": "Scale (Weeks 15–22)",
             "focus": "Promote agents from shadow to primary one phase at a time, lowest-risk first (Phase 4 CI, then Phase 7 Monitoring, then Phase 3 Code, etc.). Workforce transition plan executed in parallel. AI Governance Council operational."},
            {"phase": "Steady-state (Weeks 23+)",
             "focus": "All 21 agents operating autonomously across full PDLC. Monthly Agent Performance Review by AI Governance Council. Continuous evaluation pipeline detects model drift within 24h. Cost optimisation loop active."}
        ]
    },

    "stump": {
        "id":       "stump",
        "name":     "STUMP ADLC Platform",
        "tagline":  "Subscription — pre-wired, USB-trained, fastest path to AI-Native production",
        "investment_delta_text":  "–$300K to –$600K vs Homegrown on one-time build (subscription replaces internal build). Adds $150K–$240K / yr recurring subscription.",
        "investment_delta_usd_low":  -600,
        "investment_delta_usd_high": -300,
        "timeline_delta_weeks":   -8,
        "production_ready_weeks": 18,
        "pros": [
            "Pre-integrated agent orchestration — zero custom wiring between the 21 agents",
            "USB-trained / domain-aware models baked in (financial services, banking patterns)",
            "Built-in compliance evidence package for SOC2, ISO27001, PCI-DSS — auto-generated audit trails",
            "Single-pane observability dashboard across all agents from day one",
            "Quarterly model updates managed by STUMP team — no internal MLOps required",
            "Fastest path to 80–90% autonomous coverage — production-ready in 18–22 weeks"
        ],
        "cons": [
            "Platform-roadmap dependency — feature velocity tied to STUMP release cycle",
            "Deep customisation limited to configuration (not code-level agent modification)",
            "Data residency: requires STUMP cloud deployment or licensed on-prem agreement",
            "Recurring subscription cost — economics worsen vs Homegrown at large scale (> 200 developers)"
        ],
        "platform_ops_team": {
            "name": "STUMP Platform Operations",
            "size": "2–3 people",
            "roles": ["STUMP Platform Admin", "Prompt / Policy Engineer", "AI Product Owner"]
        },
        "agents_construction": (
            "All 21 agents pre-built, pre-integrated, pre-trained by STUMP team. "
            "Customer-side work is configuration only — connect to org's source control, ALM, CI/CD; "
            "configure policy thresholds, compliance frameworks, and override authority levels."
        ),
        "tools_changes": [
            "Adopt STUMP ADLC Platform subscription — covers all 21 agents end-to-end out of the box",
            "Configure STUMP integration to org source control (GitHub / ADO / GitLab), ALM, CI/CD, observability",
            "Use STUMP-included compliance evidence packs (SOC2, ISO27001, PCI-DSS, SOX) — eliminates custom audit tooling",
            "Single-pane STUMP observability dashboard replaces multiple monitoring tools",
            "STUMP-managed quarterly model updates with built-in evaluation — no internal MLOps stack required",
            "Jira / ADO retained read-only as compliance system of record; STUMP authors all work items"
        ],
        "devsecops_changes": [
            "STUMP-managed AI DevSecOps pipeline — security agents are part of the subscription",
            "Built-in compliance reporting (SOC2, ISO27001, PCI-DSS, SOX) — audit evidence packs auto-generated quarterly",
            "STUMP-included threat modelling and policy enforcement at every release gate",
            "Quarterly STUMP security review; novel attack patterns surfaced by STUMP CSIRT team"
        ],
        "aiops_changes": [
            "STUMP-managed AIOps — Monitor, Triage, Rollback Agents are part of the subscription",
            "Self-healing production systems with STUMP-tuned playbooks (banking / financial services baseline)",
            "STUMP incident commander manages all production events; AI Product Owner receives async handoff for Sev-1",
            "STUMP-driven capacity and cost optimisation — leverages cross-customer benchmarks for tuning"
        ],
        "product_centric_changes": [
            "Phase gates abolished; STUMP pipeline executes the full PDLC autonomously",
            "Product Definer sets weekly outcome goals via STUMP UI; agents execute autonomously",
            "STUMP-included customer intent detection (via integration with org analytics)",
            "STUMP cross-customer benchmark intelligence informs roadmap proposals (anonymised)"
        ],
        "org_changes_override": [
            "Significantly smaller AI Platform team (2–3 people, vs 6–8 for Homegrown)",
            "STUMP vendor relationship management becomes a key role for the Product Builder",
            "Quarterly STUMP roadmap review session integrated into governance cadence"
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–3)",
             "focus": "Sign STUMP subscription. Provision STUMP environment (cloud or licensed on-prem). Connect STUMP to org source control, ALM, CI/CD, observability stack."},
            {"phase": "Pilot (Weeks 4–10)",
             "focus": "Configure 21 agents to org-specific context: policy thresholds, compliance frameworks, override authority levels, code style guides. Run in shadow mode. Define Product Definer + Product Builder roles."},
            {"phase": "Scale (Weeks 11–18)",
             "focus": "Promote agents from shadow to primary one phase at a time. STUMP-managed cutover playbook. Workforce transition plan executes in parallel. AI Governance Council operational by Week 16."},
            {"phase": "Steady-state (Weeks 19+)",
             "focus": "All 21 STUMP agents autonomous. Quarterly STUMP roadmap reviews. Monthly Agent Performance Review tracking STUMP-published SLOs. No internal MLOps overhead."}
        ]
    },

    "bmad": {
        "id":       "bmad",
        "name":     "BMAD Method (Open-Source Agentic Framework)",
        "tagline":  "Open-source agentic methodology — bring your own LLM, full control, lowest licence cost",
        "investment_delta_text":  "–$200K to –$400K vs Homegrown (no platform licence; uses open BMAD methodology + workflows). Higher than STUMP — still requires internal build/integration team.",
        "investment_delta_usd_low":  -400,
        "investment_delta_usd_high": -200,
        "timeline_delta_weeks":   -4,
        "production_ready_weeks": 22,
        "pros": [
            "Open-source agentic methodology — no licence cost, no vendor lock-in",
            "Pre-curated agent patterns and prompt libraries — accelerate authoring vs greenfield Homegrown",
            "LLM-agnostic — works with Azure OpenAI, Anthropic Claude, Google Gemini, OSS models",
            "Community-driven methodology with active contributor base — peer-reviewed agent patterns",
            "Lower platform team headcount than Homegrown — methodology reduces design overhead"
        ],
        "cons": [
            "Framework only — does not replace internal build / integration effort; still need 4–5 platform engineers",
            "Smaller community than mainstream commercial platforms — fewer integrators and contractors available",
            "Less commercial support — fixes depend on community PR cycle or internal triage",
            "Methodology assumes mature agile + DevOps practice; teams with ad-hoc process need preparatory uplift",
            "Compliance evidence not bundled — must be built using the methodology, not delivered out of the box"
        ],
        "platform_ops_team": {
            "name": "AI Platform Engineering (BMAD-Aligned)",
            "size": "4–5 people",
            "roles": ["Platform Lead", "BMAD Practitioner / Methodology Champion",
                      "LLM Engineer", "SRE", "Prompt / Policy Engineer"]
        },
        "agents_construction": (
            "21 agents authored using BMAD-prescribed patterns: each agent follows BMAD's role/context/output schema. "
            "BMAD provides the methodology and prompt-library scaffolding; the team wires the actual LLM, tools, and "
            "orchestration (typically LangGraph or AutoGen) on top. LLM provider remains the org's choice."
        ),
        "tools_changes": [
            "Adopt BMAD framework — open-source methodology and prompt-library scaffolding for all 21 agents",
            "Build LangGraph (or AutoGen) orchestration on top of BMAD patterns; LLM provider is the org's choice",
            "Open-source observability (Langfuse / LangSmith) — community-supported, no vendor lock-in",
            "pgvector or Weaviate (open-source) as knowledge store — ingest org docs and runbooks",
            "AI-native ALM via BMAD-authored Backlog Agent; Jira retained read-only as compliance mirror",
            "Compliance evidence collection authored in-house using BMAD's policy-as-code patterns"
        ],
        "devsecops_changes": [
            "AI DevSecOps agents authored using BMAD's security patterns — auditable, peer-reviewable",
            "Compliance evidence collected by Compliance Agent built to BMAD's policy-as-code spec — frameworks: SOC2, ISO27001, PCI-DSS, SOX",
            "ML-based threat modelling agents tuned to org's specific threat surface — no shared cross-customer telemetry",
            "Architecture Decision Records authored by Architecture Agent using BMAD's ADR template"
        ],
        "aiops_changes": [
            "AIOps agents (Monitor, Triage, Rollback) authored using BMAD's incident-response patterns",
            "Self-healing playbooks tuned to org-specific stack; no cross-customer benchmark data (privacy-preserving)",
            "AI incident commander operates under BMAD's escalation framework; Product Builder owns Sev-1 handoff",
            "Cost optimisation loop tuned in-house using BMAD's FinOps agent template"
        ],
        "product_centric_changes": [
            "Phase gates abolished; BMAD-authored pipeline executes the full PDLC autonomously",
            "Product Definer sets weekly outcome goals; BMAD-pattern agents execute autonomously",
            "Customer intent detection authored using BMAD's market-signal agent template",
            "Proactive feature generation via BMAD's discovery-agent pattern"
        ],
        "org_changes_override": [
            "BMAD Practitioner role becomes the in-house methodology champion — owns pattern adoption and evolution",
            "Smaller AI Platform team than Homegrown (4–5 vs 6–8); methodology accelerates design + authoring",
            "Active community engagement — submit patterns back upstream; track BMAD release cycle"
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–4)",
             "focus": "Hire/transfer BMAD Practitioner. Stand up 4–5 person AI Platform team. Adopt BMAD framework; complete BMAD methodology training. Set up LangGraph + open-source observability stack."},
            {"phase": "Pilot (Weeks 5–12)",
             "focus": "Author first 11 agents using BMAD patterns (high-impact phases first). Run in shadow mode. Wire MCP tools, evaluation suite. Define Product Definer + Product Builder roles."},
            {"phase": "Scale (Weeks 13–20)",
             "focus": "Author remaining 10 agents. Promote agents from shadow to primary one phase at a time. Workforce transition plan in parallel. AI Governance Council operational."},
            {"phase": "Steady-state (Weeks 21+)",
             "focus": "All 21 BMAD-pattern agents autonomous. Monthly Agent Performance Review. Active contribution to BMAD community; track upstream methodology updates."}
        ]
    },

    "copilot_workspace": {
        "id":       "copilot_workspace",
        "name":     "Commercial AI Engineering SaaS (GitHub Copilot Workspace / Devin AI)",
        "tagline":  "Vendor-managed AI engineer platform — fastest setup, lowest internal capability requirement",
        "investment_delta_text":  "Comparable total to Homegrown on a 3-year TCO basis, but shifted from one-time build to recurring per-seat subscription. Lower upfront, higher recurring at scale.",
        "investment_delta_usd_low":  -800,
        "investment_delta_usd_high": -400,
        "timeline_delta_weeks":   -10,
        "production_ready_weeks": 16,
        "pros": [
            "Vendor manages agents end-to-end — no internal MLOps, no LLMOps, no agent authoring required",
            "Latest frontier model access — vendor upgrades baked into subscription",
            "Integrated developer experience — agents live inside the IDE / GitHub / VS Code workflow",
            "Fastest time-to-value of all four options (16 weeks to production-ready)",
            "Vendor compliance certifications (SOC2, ISO27001) inherited",
            "No internal hiring critical path — minimal headcount required"
        ],
        "cons": [
            "Per-seat subscription costs scale linearly — economics worsen sharply at 200+ developers",
            "Data exposure to vendor — code, prompts, outputs flow through vendor infrastructure (regulated industries: deep compliance and data residency review required)",
            "Limited customisation — agent behaviour shaped via prompts and skills, not code",
            "Vendor lock-in — switching cost grows as agent skills and prompts accumulate",
            "Roadmap dependency — feature velocity governed by vendor's commercial priorities",
            "May not cover all 21 PDLC phases — vendor agents typically strong on Code / CI / CD; weaker on Backlog, Architecture, Compliance"
        ],
        "platform_ops_team": {
            "name": "AI Adoption Team",
            "size": "2 people",
            "roles": ["AI Adoption Lead", "Prompt / Skill Engineer"]
        },
        "agents_construction": (
            "Vendor-provided agents (e.g. GitHub Copilot Workspace's planning / code / review agents, or Devin AI's "
            "autonomous engineer). Org-specific customisation via natural-language skills, prompts, and policy "
            "configurations. Where vendor agents do not cover a PDLC phase, supplement with selective in-house "
            "agents — typically Backlog, Compliance, and incident command."
        ),
        "tools_changes": [
            "Subscribe to GitHub Copilot Workspace OR Devin AI for full team — covers Code, Review, Test, CI/CD agent equivalents",
            "Author org-specific skills and prompts on the vendor platform — version-controlled in the vendor's skill registry",
            "Vendor-native observability and telemetry — no internal observability stack required for vendor agents",
            "Selective in-house agents to fill gaps (Backlog, Architecture, Compliance) — built using LangGraph as a thin supplement",
            "Vendor handles model updates and evaluation — internal team focuses on prompt tuning only",
            "AI-native ALM via vendor's planning agent; Jira retained read-only as compliance mirror"
        ],
        "devsecops_changes": [
            "Vendor-managed AI DevSecOps within vendor scope; supplement with in-house Compliance Agent for org-specific frameworks",
            "Compliance evidence collection partially inherited (vendor SOC2 / ISO27001) — gaps filled by supplemental in-house agents",
            "Vendor-managed threat modelling on code paths the vendor sees; in-house coverage for non-vendor surfaces",
            "Architecture Decision Records authored by supplemental in-house Architecture Agent"
        ],
        "aiops_changes": [
            "Vendor AIOps within vendor scope (e.g. CI/CD failure analysis); supplement with in-house Monitor + Triage Agents for non-vendor services",
            "Self-healing playbooks where vendor supports them; manual on-call for non-vendor surfaces",
            "AI incident commander only on services vendor agents touch; traditional on-call elsewhere",
            "Cost optimisation requires both vendor subscription tuning and internal cloud FinOps"
        ],
        "product_centric_changes": [
            "Phase gates abolished within vendor coverage; retained for non-vendor phases until supplemented",
            "Product Definer sets weekly outcomes via vendor planning UI; vendor agents execute end-to-end",
            "Customer intent detection requires supplemental in-house agent — not typically vendor-provided",
            "Proactive feature generation depends on vendor capability — currently limited; in-house supplement recommended"
        ],
        "org_changes_override": [
            "Smallest in-house team of the four options (2 people) — vendor manages most agent operations",
            "Vendor relationship management becomes the Product Builder's largest single responsibility",
            "Stricter data-residency and compliance review required before adoption in regulated environments",
            "Per-developer subscription cost becomes a recurring board-level line item"
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–2)",
             "focus": "Vendor compliance and data-residency review (longest single dependency). Sign subscription. Roll out vendor agents to a pilot squad. Stand up 2-person AI Adoption Team."},
            {"phase": "Pilot (Weeks 3–8)",
             "focus": "Pilot squad uses vendor agents on real work. Author org-specific skills and prompts. Identify coverage gaps. Define supplemental in-house agent scope (typically Backlog, Compliance, Architecture, Incident Command)."},
            {"phase": "Scale (Weeks 9–14)",
             "focus": "Full team adoption of vendor agents. Build supplemental in-house agents in parallel using LangGraph. Workforce transition plan in parallel."},
            {"phase": "Steady-state (Weeks 15+)",
             "focus": "All vendor + supplemental agents operating. Monthly vendor SLA review and supplemental agent SLO review. Continuous skill tuning."}
        ]
    },

    "devin": {
        "id": "devin", "name": "Devin (Cognition)",
        "tagline": "Autonomous SWE agent — assign tickets, Devin plans, codes, tests and opens PRs end-to-end",
        "investment_delta_text": "–$350K to –$550K vs Homegrown on one-time build; adds ~$2K–$4K per active Devin seat / yr recurring.",
        "investment_delta_usd_low": -550, "investment_delta_usd_high": -350,
        "timeline_delta_weeks": -10, "production_ready_weeks": 16,
        "pros": [
            "Fastest dev-phase autonomy — Devin executes whole tickets from issue to merged PR",
            "Built-in sandboxed dev environment, browser and shell — minimal wiring to start",
            "Strong on well-scoped backlog items and migrations; parallel Devin sessions scale throughput",
            "Reduces the in-house platform team needed for the development phases",
        ],
        "cons": [
            "Coverage skews to Phases 3–5 (dev/test); Discovery, Architecture, Governance still need other agents",
            "Per-session/seat economics can be high at scale; needs supervision on novel/ambiguous work",
            "Data-residency and source-access review required before regulated adoption",
            "Vendor-roadmap dependency for capability and model upgrades",
        ],
        "platform_ops_team": {"name": "Agent Adoption Pod", "size": "2–3 people",
                              "roles": ["Devin Orchestration Lead", "Prompt / Task Engineer", "Eval & Guardrails Engineer"]},
        "agents_construction": (
            "Devin handles Development/Test phases autonomously; supplemental LangGraph agents author the "
            "Discovery, Architecture, DevSecOps-governance and AIOps phases. Tasks queued to Devin from the "
            "backlog with acceptance criteria; PRs reviewed by the Code Reviewer agent + Product Builder on novel patterns."),
        "tools_changes": [
            "Adopt Devin for ticket-to-PR development; integrate with GitHub/ADO and CI",
            "Wrap Devin sessions with org guardrails, secrets policy and repo-scope limits",
            "Supplement non-dev phases with LangGraph agents on Azure OpenAI",
            "Langfuse/OpenTelemetry traces across Devin + supplemental agents for unified observability",
        ],
        "devsecops_changes": [
            "Devin PRs flow through the standard AI security gate (Snyk/Checkov/GH Advanced Security)",
            "Supplemental Compliance-as-Code agent validates regulated changes before merge",
        ],
        "aiops_changes": [
            "AIOps remains on supplemental Monitor/Triage agents; Devin not used for production incident command",
        ],
        "product_centric_changes": [
            "Product Builder curates and scopes the Devin task queue; Product Definer sets outcomes",
            "Throughput scales by running parallel Devin sessions on independent backlog items",
        ],
        "org_changes_override": [
            "Stand up a small Agent Adoption Pod (2–3) to orchestrate Devin tasks and own guardrails/evals",
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–2)", "focus": "Vendor + data-access review; connect Devin to repos/CI; define task templates and guardrails."},
            {"phase": "Pilot (Weeks 3–7)", "focus": "Devin runs scoped dev tickets in shadow then primary on one squad; supplemental agents for non-dev phases stood up."},
            {"phase": "Scale (Weeks 8–14)", "focus": "Parallel Devin sessions across squads; supplemental agents cover Discovery→Architecture→Governance→AIOps."},
            {"phase": "Steady-state (Weeks 15+)", "focus": "Devin autonomous on dev/test with reviewer-agent gates; monthly eval + cost optimisation."},
        ],
    },

    "cursor": {
        "id": "cursor", "name": "Cursor (Anysphere)",
        "tagline": "AI-native IDE + background agents — deep in-editor codegen, multi-file edits and agentic tasks",
        "investment_delta_text": "–$250K to –$450K vs Homegrown on one-time build; adds ~$240–$480 per developer / yr (Business/Enterprise).",
        "investment_delta_usd_low": -450, "investment_delta_usd_high": -250,
        "timeline_delta_weeks": -6, "production_ready_weeks": 20,
        "pros": [
            "Highest developer adoption — agents live in the IDE developers already use",
            "Strong multi-file edits, codebase-aware chat, and background agents for scoped tasks",
            "Low switching cost; immediate Phase 4 velocity gains",
            "Privacy mode and enterprise controls available",
        ],
        "cons": [
            "Developer-centric — assistive by default; full autonomy still needs orchestration around it",
            "Limited native coverage of Discovery, Governance and AIOps phases",
            "Per-seat cost across a large org; model usage variability",
            "Vendor-roadmap dependency",
        ],
        "platform_ops_team": {"name": "Agent Adoption Pod", "size": "2–3 people",
                              "roles": ["Dev Experience Lead", "Prompt / Rules Engineer", "Eval & Guardrails Engineer"]},
        "agents_construction": (
            "Cursor provides in-IDE assistive + background agents for Development/Test; supplemental LangGraph "
            "agents author Discovery, Architecture, DevSecOps-governance and AIOps. Org coding rules and context "
            "configured in Cursor; PR review via Code Reviewer agent + human gate on novel patterns."),
        "tools_changes": [
            "Roll out Cursor (Business/Enterprise) with org rules, privacy mode and codebase indexing",
            "Use Cursor background agents for scoped multi-file tasks; supplement non-dev phases with LangGraph",
            "Unified observability across Cursor usage + supplemental agents",
        ],
        "devsecops_changes": [
            "Cursor-authored changes flow through the standard AI security and compliance gates",
        ],
        "aiops_changes": [
            "AIOps handled by supplemental Monitor/Triage agents (outside Cursor)",
        ],
        "product_centric_changes": [
            "Developers stay in-loop with assistive agents; autonomy increases as background agents mature",
        ],
        "org_changes_override": [
            "Small Agent Adoption Pod owns Cursor rules, evals and the supplemental agent set",
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–2)", "focus": "Enterprise rollout, org rules, privacy/security review; index repos."},
            {"phase": "Pilot (Weeks 3–8)", "focus": "Pilot squad adopts Cursor + background agents; supplemental agents for non-dev phases stood up."},
            {"phase": "Scale (Weeks 9–16)", "focus": "Org-wide adoption; background agents take scoped tasks; supplemental agents cover remaining phases."},
            {"phase": "Steady-state (Weeks 17+)", "focus": "Assistive→supervised-autonomous on dev/test; monthly eval and cost review."},
        ],
    },

    "flowsource": {
        "id": "flowsource", "name": "Cognizant Flowsource",
        "tagline": "Cognizant's AI-led SDLC platform — pre-integrated toolchain, accelerators and managed delivery agents",
        "investment_delta_text": "–$400K to –$700K vs Homegrown on one-time build (platform + accelerators + managed services); recurring platform + services fee.",
        "investment_delta_usd_low": -700, "investment_delta_usd_high": -400,
        "timeline_delta_weeks": -10, "production_ready_weeks": 16,
        "pros": [
            "Pre-integrated, opinionated SDLC platform with accelerators across all phases — fastest broad coverage",
            "Managed delivery + platform engineering by Cognizant — minimal in-house platform team",
            "Built-in governance, quality gates and reusable assets tuned for regulated enterprises",
            "Single accountable partner for platform, agents and delivery uplift",
        ],
        "cons": [
            "Highest partner/services dependency — capability tied to Flowsource roadmap and engagement",
            "Customisation within platform guardrails; less code-level control than homegrown",
            "Data-residency / third-party access review required for regulated workloads",
            "Recurring platform + managed-services cost",
        ],
        "platform_ops_team": {"name": "Flowsource Engagement Team (Cognizant-managed)", "size": "2–4 client-side",
                              "roles": ["Client Platform Owner", "AI Product Owner", "Governance / Risk Liaison"]},
        "agents_construction": (
            "Flowsource ships pre-built, pre-integrated agents and accelerators across Discovery→AIOps, configured to "
            "the client's stack and policies by the Cognizant engagement team. Client-side work is configuration, "
            "policy thresholds and acceptance — Product Definer/Builder retain approval authority."),
        "tools_changes": [
            "Adopt the Flowsource toolchain and accelerators across the full PDLC; connect to client SCM/ALM/CI",
            "Configure policy thresholds, compliance frameworks and override authority — no custom agent build",
            "Flowsource observability + quality dashboards across all agents from day one",
        ],
        "devsecops_changes": [
            "Flowsource-managed AI DevSecOps with built-in compliance evidence (SOC2/ISO/PCI/DORA)",
            "Quality gates and audit trails managed by the platform; client reviews exceptions",
        ],
        "aiops_changes": [
            "Flowsource AIOps accelerators for monitoring/triage/remediation; Sev-1 escalates to client Product Builder",
        ],
        "product_centric_changes": [
            "Continuous product evolution on the Flowsource platform; Product Definer sets outcomes, platform executes",
            "Reusable accelerators shorten time-to-value across squads",
        ],
        "org_changes_override": [
            "Small client-side engagement team (2–4) governs the Cognizant-managed platform and delivery",
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–2)", "focus": "Engagement setup, data-residency/compliance review, connect stack, configure policies."},
            {"phase": "Pilot (Weeks 3–7)", "focus": "Pilot squad on Flowsource accelerators across phases; tune policies and acceptance gates."},
            {"phase": "Scale (Weeks 8–14)", "focus": "Roll out across squads; workforce transition in parallel; governance council operational."},
            {"phase": "Steady-state (Weeks 15+)", "focus": "Full PDLC on Flowsource; monthly platform SLA + agent SLO review; continuous accelerator updates."},
        ],
    },

    "baxter": {
        "id":       "baxter",
        "name":     "Baxter (Cognizant)",
        "tagline":  "Cognizant's AI-powered software engineering platform with specialized agents for enterprise delivery",
        "investment_delta_text":  "1.8× baseline — Cognizant managed service + platform license",
        "investment_delta_usd_low":  -400_000,
        "investment_delta_usd_high": -200_000,
        "timeline_delta_weeks":   -12,
        "production_ready_weeks": 6,
        "pros": [
            "Pre-built enterprise agents for each SDLC phase — 8 specialised agents with deep domain coverage",
            "Cognizant-managed operations and 24/7 support",
            "Integrated compliance and governance framework (SOC2, ISO27001, PCI-DSS, DORA)",
            "Rapid onboarding with industry-specific templates (Banking, Healthcare, Telco)",
            "Continuous platform evolution by Cognizant AI CoE",
            "Built-in continuous testing intelligence (Test Maestro) and predictive delivery analytics (Insight Engine)",
            "Enterprise ALM deep integration — Jira, ADO, ServiceNow native connectors",
        ],
        "cons": [
            "Vendor dependency on Cognizant platform team",
            "Limited customization of core agent behaviours",
            "Higher ongoing license costs vs open-source alternatives",
        ],
        "platform_ops_team": {
            "name": "Cognizant Baxter Platform Team",
            "size": "3–5 (Cognizant-managed)",
            "roles": ["Platform Lead", "Agent Configuration Specialist", "Integration Engineer"],
        },
        "agents_construction": (
            "8 specialised Baxter agents managed by Cognizant. Each agent tuned for enterprise "
            "delivery with industry-specific compliance templates. Agent Studio for configuration; "
            "Cognizant AI CoE handles model updates and agent evolution."
        ),
        "tools_changes": [
            "Baxter Platform provides 8 specialised agents covering all 7 PDLC phases",
            "Baxter Agent Studio for configuring agent behaviour, thresholds, and approval gates",
            "Enterprise ALM Connectors (Jira, ADO, ServiceNow) enable native data ingestion",
            "Governance Dashboard provides real-time compliance and delivery intelligence",
            "Compliance Automation Suite for SOC2/ISO/PCI/DORA evidence generation",
        ],
        "devsecops_changes": [
            "Baxter Security Sentinel: continuous scanning with auto-remediation, compliance mapping, and risk scoring",
            "Baxter Release Captain: orchestrates release pipelines with canary deployments, feature flags, and auto-rollback",
            "Built-in compliance evidence generation — audit trails auto-generated per deployment",
        ],
        "aiops_changes": [
            "Baxter Ops Guardian: predictive monitoring with self-healing, anomaly detection, and incident orchestration",
            "Baxter Insight Engine: continuous delivery intelligence — velocity trends, quality predictions, team health metrics",
            "Sev-1 auto-escalates to client Product Builder with full context package",
        ],
        "product_centric_changes": [
            "Continuous product evolution on Baxter platform; Product Definer sets outcomes, agents execute",
            "Baxter Story Crafter generates user stories from business requirements and market signals",
            "Predictive delivery analytics inform roadmap decisions before issues surface",
        ],
        "org_changes_override": [
            "Small client-side governance team (2–4) oversees Cognizant-managed Baxter platform",
            "Cognizant provides dedicated Platform Lead and Agent Configuration Specialists",
        ],
        "playbook_phasing": [
            {"phase": "Foundation (Weeks 1–2)", "focus": "Engagement setup, compliance review, connect enterprise ALM tools, configure governance policies."},
            {"phase": "Pilot (Weeks 3–4)", "focus": "Pilot squad on Baxter with Story Crafter + Code Pilot + Test Maestro; tune agent thresholds."},
            {"phase": "Scale (Weeks 5–6)", "focus": "Activate all 8 agents; roll out across squads; workforce transition; governance council operational."},
            {"phase": "Steady-state (Weeks 7+)", "focus": "Full PDLC on Baxter; monthly platform SLA + agent SLO review; continuous agent evolution by Cognizant AI CoE."},
        ],
    },
}

# Target-state delivery platform kinds. STUMP is the measurement/transformation
# platform, not a target ADLC delivery platform → excluded from the configurator.
PLATFORM_KIND = {
    "homegrown": "home_grown",
    "bmad": "cots", "copilot_workspace": "cots", "devin": "cots", "cursor": "cots",
    "flowsource": "service_provider",
    "baxter": "service_provider",
}
TARGET_STATE_PLATFORM_ORDER = ["homegrown", "bmad", "copilot_workspace", "devin", "cursor", "flowsource", "baxter"]


def target_state_platforms() -> list[dict]:
    """Platform catalog for the Target State Studio (excludes 'stump')."""
    out = []
    for pid in TARGET_STATE_PLATFORM_ORDER:
        p = C_PLATFORM_OPTIONS.get(pid)
        if not p:
            continue
        out.append({
            "id": pid, "name": p["name"], "tagline": p["tagline"],
            "kind": PLATFORM_KIND.get(pid, "cots"),
            "is_us_bank_target": pid == "homegrown",
            "investment_delta_text": p.get("investment_delta_text", ""),
            "investment_delta_usd_low": p.get("investment_delta_usd_low", 0),
            "investment_delta_usd_high": p.get("investment_delta_usd_high", 0),
            "timeline_delta_weeks": p.get("timeline_delta_weeks", 0),
            "production_ready_weeks": p.get("production_ready_weeks", 0),
            "pros": p.get("pros", []), "cons": p.get("cons", []),
            "platform_ops_team": p.get("platform_ops_team", {}),
            "agents_construction": p.get("agents_construction", ""),
            "tools_changes": p.get("tools_changes", []),
            "devsecops_changes": p.get("devsecops_changes", []),
            "aiops_changes": p.get("aiops_changes", []),
            "product_centric_changes": p.get("product_centric_changes", []),
            "playbook_phasing": p.get("playbook_phasing", []),
        })
    return out


def apply_c_platform(bc: dict, platform: str) -> dict:
    """
    Merge an Option C platform choice's overrides into the base Option C business case.

    Returns a new dict with the selected platform's tools_changes / devsecops_changes /
    aiops_changes / product_centric_changes / org_changes replacing the base values,
    plus the platform's investment_delta, timeline_delta, pros/cons, ops team, and
    playbook phasing surfaced as additional top-level keys.
    """
    if platform not in C_PLATFORM_OPTIONS:
        return bc
    opt = C_PLATFORM_OPTIONS[platform]
    merged = {**bc}
    merged["selected_platform"]       = opt["id"]
    merged["platform_name"]           = opt["name"]
    merged["platform_tagline"]        = opt["tagline"]
    merged["investment_delta_text"]   = opt["investment_delta_text"]
    merged["investment_delta_usd"]    = {"low": opt["investment_delta_usd_low"],
                                         "high": opt["investment_delta_usd_high"]}
    merged["timeline_delta_weeks"]    = opt["timeline_delta_weeks"]
    merged["production_ready_weeks"]  = opt["production_ready_weeks"]
    merged["platform_pros"]           = opt["pros"]
    merged["platform_cons"]           = opt["cons"]
    merged["platform_ops_team"]       = opt["platform_ops_team"]
    merged["agents_construction"]     = opt["agents_construction"]
    merged["playbook_phasing"]        = opt["playbook_phasing"]
    # Full overrides of the matching base sections
    merged["tools_changes"]           = opt["tools_changes"]
    merged["devsecops_changes"]       = opt["devsecops_changes"]
    merged["aiops_changes"]           = opt["aiops_changes"]
    merged["product_centric_changes"] = opt["product_centric_changes"]
    # Append platform-specific org changes on top of the base org_changes
    merged["org_changes"]             = bc.get("org_changes", []) + opt.get("org_changes_override", [])
    return merged


BUSINESS_CASES = {
    "option-a": {
        "investment_range":    "$800K – $1.5M",
        "roi_timeline":        "12–18 months",
        "roi_multiple":        2.8,
        "payback_months":      14,
        "investment": {
            "tools":           "$250K–$400K (AI tools, IDE plugins, platform licenses)",
            "infrastructure":  "$100K–$200K (GPU compute, vector DBs, API costs)",
            "implementation":  "$300K–$600K (integration, prompt engineering, testing)",
            "training":        "$100K–$200K (upskilling all PDLC personas)",
            "change_mgmt":     "$100K–$150K (org change management, communications)"
        },
        "annual_benefits": {
            "ttm_improvement":     "$600K–$900K (faster feature delivery, competitive advantage)",
            "productivity_gains":  "$400K–$600K (35% effort reduction across team)",
            "quality_improvement": "$200K–$300K (fewer defects, less rework)",
            "operational_savings": "$100K–$150K (automated testing, deployments)"
        },
        "org_changes": [
            "Upskill all PDLC personas in AI tool collaboration and prompt engineering",
            "Redefine roles to include AI supervision, output validation, and exception handling",
            "Establish AI Centre of Excellence (CoE) for governance and best practices",
            "Update ways of working guides for human-AI collaboration patterns",
            "Introduce mandatory AI literacy training for all team members"
        ],
        "tools_changes": [
            "Jira / ADO: Deploy AI-powered backlog management and VSM plugins",
            "GitHub: Roll out Copilot Enterprise for all developers",
            "Testing: Upgrade to AI-enhanced test frameworks (Playwright AI, Testim)",
            "CI/CD: Integrate ML-based build optimizers and AI-powered SAST",
            "Monitoring: Deploy AI APM (Dynatrace Davis AI or Datadog AI)"
        ],
        "devsecops_changes": [
            "Shift-left security with AI-assisted SAST/DAST integrated in every PR",
            "AI-generated IaC templates with automated security policy validation",
            "Continuous compliance evidence collection for audit trails",
            "AI-powered secret scanning and dependency vulnerability monitoring"
        ],
        "aiops_changes": [
            "AI-driven anomaly detection and auto-remediation for common issues",
            "Predictive scaling using ML traffic pattern analysis",
            "Automated incident routing with NLP-based categorization",
            "Continuous feedback loop: production insights → AI-prioritized backlog"
        ],
        "product_centric_changes": [
            "Reorganize from project to persistent product teams with stable membership",
            "OKRs tied to product outcomes and customer value, not delivery velocity",
            "Quarterly business review cadence enhanced by AI-generated insights",
            "Customer feedback continuously integrated into roadmap via AI analysis"
        ]
    },
    "option-b": {
        "investment_range":    "$1.0M – $1.8M",
        "roi_timeline":        "10–15 months",
        "roi_multiple":        3.4,
        "payback_months":      12,
        "investment": {
            "tools":           "$350K–$600K (~11 agents deployed in high-impact PDLC phases; remaining phases retain Option A AI co-pilot tools)",
            "infrastructure":  "$180K–$300K (AI compute and model hosting sized for half-fleet; shared with Option A tooling)",
            "implementation":  "$300K–$650K (custom LangGraph build for the deployed 11 agents; phase-by-phase integration)",
            "training":        "$100K–$200K (5 core roles trained for agent governance; remaining team upskilled on Option A AI tools)",
            "change_mgmt":     "$120K–$180K (role restructuring for agent-covered phases; minimal change for human-covered phases)"
        },
        "annual_benefits": {
            "ttm_improvement":     "$700K–$1.1M (45% faster delivery on agent-covered phases; baseline on human-covered phases)",
            "productivity_gains":  "$450K–$750K (~4.7 effective FTE per pod vs 8 in Option A: 4 dedicated + ~0.7 fractional shared across 2–3 pods)",
            "quality_improvement": "$250K–$400K (AI quality gates on agent-covered phases; standard QA on human-covered phases)",
            "operational_savings": "$150K–$250K (AIOps + agent monitoring on covered phases; manual ops on remainder)"
        },
        "org_changes": [
            "Deploy ~11 of 21 agents in high-impact PDLC phases (typically Code Generation, Code Review, QA Orchestration, Release Gate, Monitor, Triage). Remaining phases continue with Option A AI co-pilot model — humans execute, AI assists.",
            "Restructure each product pod to 4 dedicated roles: Product Owner (1 FTE), Developer / Agent Operator (2 FTE), QA Lead (1 FTE). These execute both the agent-covered phases (as reviewers) and the human-covered phases (as authors).",
            "Add 2 shared / fractional roles allocated across pods: Tech Lead / Architect (0.3–0.5 FTE per pod, 1 shared across 2–3 pods) and Agent Ops / DevOps Engineer (0.4 FTE per pod, 1 shared across 2–3 pods).",
            "Total per-pod effective headcount: ~4.7 FTE (4 dedicated + 0.7 fractional). Down from 8 in Option A.",
            "Establish human-AI handoff protocols at each phase boundary — clear ownership of which phases are agent-led vs human-led.",
            "Create a small Agent Platform Team (4–5 people org-wide) to manage, tune, and govern the 11 deployed agents.",
            "Redesign performance metrics: agent-covered phases measured on agent SLOs (acceptance %, override rate); human-covered phases keep traditional team-velocity metrics.",
            "Monthly governance review reconciling agent KPIs with team KPIs — preventing two-tier measurement gaming."
        ],
        "tools_changes": [
            "Selective consolidation: AI-native ALM (Linear / Shortcut / Jira AI) for agent-covered phases; existing Jira/ADO retained for human-covered phases as system of record.",
            "Deploy custom LangChain/LangGraph orchestration layer scoped to the deployed 11 agents — half-fleet footprint.",
            "Replace manual test scripting with AI-generated suites in agent-covered phases; human-authored tests remain for the human-covered half.",
            "GitOps-native CI/CD with AI release gating for agent-covered code paths; conventional CI/CD for remaining paths.",
            "Unified observability across both halves — single-pane-of-glass shows agent SLOs alongside human team telemetry."
        ],
        "devsecops_changes": [
            "Zero-trust security enforced by AI policy agents in agent-covered pipeline stages; manual SAST/DAST gates remain in human-covered stages.",
            "AI-generated runbooks for incidents arising in agent-covered phases; human-authored runbooks elsewhere.",
            "Continuous compliance validation by AI audit agents (SOC2, ISO 27001) for agent-touched artefacts; periodic human audit for the rest.",
            "ML-based threat modelling on agent-generated designs; traditional review for human-led architecture work."
        ],
        "aiops_changes": [
            "Self-healing CI/CD pipelines with AI failure prediction in agent-covered phases — Build / Pipeline / Deploy / Rollback Agents active.",
            "AIOps platform manages production alerts, triage, and initial response for services from agent-covered phases; conventional on-call rotation for legacy services.",
            "Automated capacity planning using ML demand forecasting in agent scope; manual capacity reviews elsewhere.",
            "Post-incident learning auto-generated by AI for agent-handled events; human PIR for novel incidents and non-agent services."
        ],
        "product_centric_changes": [
            "Product teams own the full value stream end-to-end, but split execution: agents for the half that is automated, humans for the half that is not.",
            "Eliminate hand-offs within each half; the half-boundary itself becomes a new explicit handoff governed by the Agent Ops team.",
            "Continuous product discovery embedded as a permanent ritual; Discovery Agent supports human-led discovery on the non-agent half.",
            "AI-generated real-time dashboards on agent-covered phases; standard Jira / VSM reporting on the rest — unified at the team level."
        ]
    },
    "option-c": {
        "investment_range":    "$2.4M – $4.2M",
        "roi_timeline":        "18–24 months",
        "roi_multiple":        5.5,
        "payback_months":      19,
        "investment": {
            "tools":           "$800K–$1.4M (all 21 agents deployed — comprehensive AI-native platform stack covering every PDLC phase)",
            "infrastructure":  "$500K–$900K (enterprise AI compute, model fine-tuning infrastructure sized for full-fleet 21-agent workload)",
            "implementation":  "$750K–$1.4M (end-to-end LangGraph orchestration for all 21 agents; review-and-approve UX for Product Definer / Builder)",
            "training":        "$200K–$300K (intensive reskilling for the 2 retained roles — Product Definer and Product Builder; redeployment planning for departing roles)",
            "change_mgmt":     "$300K–$500K (major org transformation, workforce transition plan, ethics and regulatory engagement)"
        },
        "annual_benefits": {
            "ttm_improvement":     "$1.8M–$2.8M (70% faster delivery end-to-end — all 21 agents execute, humans only review and approve at gates)",
            "productivity_gains":  "$1.5M–$2.1M (70% effort reduction; per-pod ~2 FTE for execution oversight + 0.5–1 FTE shared Engineering Architect across 3–5 pods — no humans on the execution path)",
            "quality_improvement": "$500K–$800K (AI quality gates on every phase, agent self-critique, near-zero rework)",
            "operational_savings": "$400K–$700K (fully autonomous operations — AI incident commander, AI compliance, AI cost optimisation)"
        },
        "org_changes": [
            "All 21 agents execute the PDLC end-to-end. Humans do not author code, write tests, run pipelines, or operate production — they only review and approve at gates and policy thresholds.",
            "Restructure each product pod to 2 dedicated human roles: Product Definer (1 FTE — sets strategic vision, outcomes, acceptance criteria) and Product Builder (1 FTE — oversees agent execution, reviews high-stakes outputs, handles exceptions and prompt tuning for the pod).",
            "Add a shared Engineering Architect role at 0.5–1 FTE per portfolio of 3–5 pods (NOT dedicated to a single pod). Sets architecture policy across pods, approves novel patterns flagged by Architecture Agent, owns cross-pod design coherence.",
            "Total per-pod effective headcount: ~2.2 FTE (2 dedicated + 0.2 fractional architect). 8+ legacy roles displaced from execution; agents take their place.",
            "Replace sprint cadence with Quarterly Intent Setting + Weekly Outcome Review; gate approvals are async and < 24h.",
            "Major workforce transition plan: reskilling (to Definer / Builder / Architect), redeployment, and attrition management for the displaced roles.",
            "AI Governance Council (CTO, CISO, Risk Officer, AI Ethics Lead, Regulatory Lead) sets policy, autonomous thresholds, reviews monthly agent performance — one council org-wide, shared across all portfolios.",
            "Board-level approval required for operating-model change of this magnitude; external change-management specialist engagement strongly recommended."
        ],
        "tools_changes": [
            "Adopt full AI-native product engineering platform (STUMP ADLC Platform, Devin AI, or GitHub Copilot Workspace) covering every PDLC phase end-to-end.",
            "Multi-agent orchestration (LangGraph / AutoGen / Agency Swarm) wiring all 21 agents into a single autonomous pipeline.",
            "AI-native project management replaces traditional Jira / ADO entirely — Jira retained read-only as compliance mirror.",
            "Fully automated CI/CD/CD pipelines with AI decisions at every quality and release gate; humans approve only the highest-risk releases.",
            "Integrated AI product analytics replaces all manual reporting and dashboards — Product Definer sees agent-generated business signals in real time."
        ],
        "devsecops_changes": [
            "Fully AI-managed DevSecOps pipeline from code commit to production deployment — no human in the inner loop.",
            "AI security agents continuously monitor, detect, and auto-remediate threats within policy scope; human review only for novel attack patterns and regulatory exceptions.",
            "Autonomous compliance management (SOC2, ISO 27001, PCI-DSS, SOX) — audit evidence auto-generated; humans validate quarterly evidence packages.",
            "AI-generated and maintained Architecture Decision Records (ADRs), threat models, and security reviews — Product Builder reviews ADRs flagged as novel."
        ],
        "aiops_changes": [
            "Fully autonomous AIOps — zero Level 1 / Level 2 human intervention in production; humans engage only on Sev-1.",
            "AI-driven continuous capacity, performance, and cost optimisation across the full production estate.",
            "Self-healing, self-scaling, and self-documenting production systems — runbooks generated and maintained by AI.",
            "AI incident commander manages all production events; Product Builder receives async handoff packages, approves remediation, and signs off post-incident reviews."
        ],
        "product_centric_changes": [
            "Abolish traditional SDLC phase gates — move to continuous product evolution model where agents execute end-to-end.",
            "Product Definer sets weekly outcome goals in natural language; AI agents decompose, build, test, deploy and operate autonomously without human execution.",
            "Real-time customer intent detection feeds directly into AI-driven roadmap prioritisation — no human PM authoring stories.",
            "Proactive feature generation: AI identifies market opportunities before humans request them; Product Definer chooses which proposals to greenlight."
        ]
    }
}


async def run_business_case_builder(state: VSMAgentState) -> VSMAgentState:
    """Generate business cases for all 3 future state scenarios."""
    logger.info("[Business Case Builder] Building business cases for 3 scenarios")

    future_states = state.get("future_states", {})
    business_cases = {}

    for scenario_id, bc in BUSINESS_CASES.items():
        fs = future_states.get(scenario_id, {})
        vs_current = fs.get("vs_current", {})

        # Enrich with calculated metrics
        business_cases[scenario_id] = {
            **bc,
            "scenario_id":     scenario_id,
            "scenario_label":  fs.get("label", scenario_id),
            "scenario_title":  fs.get("title", ""),
            "metrics_summary": {
                "lt_reduction":  vs_current.get("lt_reduction_pct", 0),
                "fe_gain":       vs_current.get("fe_absolute_gain", 0),
                "pt_reduction":  vs_current.get("pt_reduction_pct", 0),
                "wt_reduction":  vs_current.get("wt_reduction_pct", 0)
            }
        }

    # Option C carries a build-vs-buy platform catalogue. Default view is "homegrown";
    # the analysis endpoint accepts ?platform=<id> to apply the selected overrides.
    if "option-c" in business_cases:
        business_cases["option-c"]["platform_catalog"] = {
            pid: {
                "id":            opt["id"],
                "name":          opt["name"],
                "tagline":       opt["tagline"],
                "weeks_to_prod": opt["production_ready_weeks"],
                "investment_delta_text": opt["investment_delta_text"],
            }
            for pid, opt in C_PLATFORM_OPTIONS.items()
        }
        business_cases["option-c"]["default_platform"] = "homegrown"

    # LLM-enhanced: generate tailored executive summary and risk section per scenario
    if has_llm():
        business_cases = await _enrich_business_cases(business_cases, state)

    return {**state, "business_cases": business_cases}


async def _enrich_business_cases(business_cases: dict, state: dict) -> dict:
    """Add LLM-generated executive summary and key risks per business case."""
    project  = state.get("project", {})
    industry = project.get("industry", "Technology")

    for scenario_id, bc in business_cases.items():
        prompt = f"""You are a management consultant building a business case for a PDLC transformation.

Organisation: {project.get('organization', 'Enterprise')}  Industry: {industry}
Scenario: {bc.get('scenario_label', '')} — {bc.get('scenario_title', '')}
Investment: {bc['investment_range']}
ROI: {bc['roi_multiple']}× in {bc['roi_timeline']}
Lead Time Reduction: {bc.get('metrics_summary', {}).get('lt_reduction', '?')}%
Flow Efficiency Gain: {bc.get('metrics_summary', {}).get('fe_gain', '?')} percentage points

Write:
1. A 3-sentence executive summary suitable for a C-suite audience (paragraph, no bullets)
2. Top 3 implementation risks with one-line mitigation for each

Return ONLY JSON, no extra text:
{{
  "executive_summary": "<3 sentences>",
  "risks": [
    {{"risk": "<risk>", "mitigation": "<mitigation>"}},
    {{"risk": "<risk>", "mitigation": "<mitigation>"}},
    {{"risk": "<risk>", "mitigation": "<mitigation>"}}
  ]
}}"""
        try:
            raw = await ainvoke(prompt)
            import json, re
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                bc["executive_summary"] = result.get("executive_summary", "")
                bc["risks"]             = result.get("risks", [])
        except Exception as ex:
            logger.warning(f"[Business Case Builder] LLM enrichment failed for {scenario_id}: {ex}")

    return business_cases
