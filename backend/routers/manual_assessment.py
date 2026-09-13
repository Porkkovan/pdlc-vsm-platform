"""Pod Agentic Maturity Assessment — 6-pillar, 30-question self-assessment.

Level scale and team-mix benchmarks adapted from the ADLC L1–L5 ladder.
Each question is scored 1–5. Pillar score = average of its 5 questions.
Overall maturity = average of 6 pillar scores.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..database.db import get_db
from ..database.models import ManualAssessmentResponse, Project

router = APIRouter(prefix="/manual-assessment", tags=["manual-assessment"])

# ─── Consistent L1-L5 maturity levels ────────────────────────────────────────
MATURITY_LEVELS = {
    1: {"band": "L1", "label": "Foundation (Assisted)", "color": "#ef4444",
        "description": "Processes are manual and ad-hoc; no agentic input. AI used only informally by individuals, if at all.",
        "human_pct": 80, "agent_pct": 20, "benchmark_mix": "~9 humans : 2 agents"},
    2: {"band": "L2", "label": "Augmentation (Co-Piloted)", "color": "#f97316",
        "description": "AI copilots help draft plans, code and tests; humans finalise and approve everything.",
        "human_pct": 60, "agent_pct": 40, "benchmark_mix": "~8 humans : 6 agents"},
    3: {"band": "L3", "label": "Automation (Supervised-Independent)", "color": "#eab308",
        "description": "Agents independently execute standard tasks; humans handle exceptions and sign off gates.",
        "human_pct": 38, "agent_pct": 62, "benchmark_mix": "~6 humans : 12 agents"},
    4: {"band": "L4", "label": "Transformation (Orchestrated)", "color": "#22c55e",
        "description": "Multi-agent workflows run most activities end-to-end; humans set priorities and escalation.",
        "human_pct": 22, "agent_pct": 78, "benchmark_mix": "~4 humans : 18 agents"},
    5: {"band": "L5", "label": "Reinvention (Autonomous)", "color": "#3b82f6",
        "description": "Fully autonomous with human involvement limited to strategic intent and governance.",
        "human_pct": 10, "agent_pct": 90, "benchmark_mix": "~3 humans : 21 agents"},
}

# ─── 6 Pillars × 5 Questions = 30 total ──────────────────────────────────────
PILLARS = [
    {"id": 1, "name": "Operating Model & Ways of Working",
     "description": "How the pod plans, executes and governs its day-to-day work."},
    {"id": 2, "name": "Service Catalogue & Scope",
     "description": "What the pod delivers, and how that scope is catalogued and exposed."},
    {"id": 3, "name": "Organisation, Roles & Team Mix",
     "description": "Structure, hierarchy, and the human-to-agent composition of the pod."},
    {"id": 4, "name": "People Capability & AI Fluency",
     "description": "Skills, fluency and learning pathways the pod's people have today."},
    {"id": 5, "name": "Tooling & Agentic Platform",
     "description": "The tools, infrastructure and agent platform the pod builds/works on."},
    {"id": 6, "name": "Governance, Risk & Change Management",
     "description": "Guardrails, policy adherence, and how the pod manages adoption/change."},
]

ASSESSMENT_QUESTIONS = [
    # ── Pillar 1: Operating Model & Ways of Working ───────────────────────
    {"id": "q01", "pillar_id": 1, "pillar_name": "Operating Model & Ways of Working",
     "question": "Planning & Governance Rhythm",
     "rubric": {
         1: "Planning is manual and ad hoc; no agentic input used in ceremonies.",
         2: "AI copilots help draft plans/backlogs; humans finalise and approve everything.",
         3: "Agents populate & maintain plans for standard work; humans validate exceptions.",
         4: "Multi-agent workflows run most planning end-to-end; humans set priorities & escalation.",
         5: "Planning is autonomous and continuously self-adjusting; humans set strategic intent only.",
     }},
    {"id": "q02", "pillar_id": 1, "pillar_name": "Operating Model & Ways of Working",
     "question": "Task Execution",
     "rubric": {
         1: "All execution is manual; AI used only informally by individuals, if at all.",
         2: "AI assists individual tasks (drafting, coding, testing); humans do the actual work.",
         3: "Agents independently execute standard, repeatable tasks; humans handle exceptions.",
         4: "Most execution runs through orchestrated agents across the lifecycle; humans govern.",
         5: "Execution is fully autonomous end-to-end; humans intervene only strategically.",
     }},
    {"id": "q03", "pillar_id": 1, "pillar_name": "Operating Model & Ways of Working",
     "question": "Quality Assurance & Review",
     "rubric": {
         1: "Quality checks are manual and inconsistent; no defined review standard.",
         2: "Defined review steps exist; every AI/agent output is human-reviewed before use.",
         3: "Agents perform first-pass QA; humans review by exception & sign off gates.",
         4: "Multi-agent QA pipelines run continuously; humans review only flagged exceptions.",
         5: "QA is autonomous and self-correcting; humans audit outcomes periodically, not per-item.",
     }},
    {"id": "q04", "pillar_id": 1, "pillar_name": "Operating Model & Ways of Working",
     "question": "Continuous Improvement",
     "rubric": {
         1: "No structured retro/improvement process for how the pod works.",
         2: "Regular retros happen; improvements are identified and applied manually.",
         3: "Agents help surface patterns/bottlenecks; humans decide & apply improvements.",
         4: "Agents propose and test operating-model improvements; humans approve rollout.",
         5: "The operating model self-optimises continuously; humans review outcomes periodically.",
     }},
    {"id": "q05", "pillar_id": 1, "pillar_name": "Operating Model & Ways of Working",
     "question": "Autonomy & Escalation",
     "rubric": {
         1: "Every action requires human initiation and sign-off; no autonomy exists.",
         2: "Humans approve every AI-assisted output before it moves forward.",
         3: "Agents act independently on standard cases; humans handle only exceptions.",
         4: "Agents operate broadly autonomously with defined escalation triggers to humans.",
         5: "Full autonomy with human involvement limited to strategic escalations only.",
     }},

    # ── Pillar 2: Service Catalogue & Scope ───────────────────────────────
    {"id": "q06", "pillar_id": 2, "pillar_name": "Service Catalogue & Scope",
     "question": "Catalogue Definition",
     "rubric": {
         1: "No documented list of the pod's services or deliverables exists.",
         2: "A basic list of services/deliverables exists, maintained manually and infrequently.",
         3: "Catalogue is structured & versioned, with clear descriptions per service.",
         4: "Catalogue is agent-curated and stays current with actual delivery activity.",
         5: "Catalogue self-evolves, with agents proposing new services from demand signals.",
     }},
    {"id": "q07", "pillar_id": 2, "pillar_name": "Service Catalogue & Scope",
     "question": "Discoverability",
     "rubric": {
         1: "Stakeholders learn about services informally, through conversation or tribal knowledge.",
         2: "Services are documented somewhere, but not easy for stakeholders to find.",
         3: "Catalogue lives in a discoverable, structured location (portal/backlog tool).",
         4: "Catalogue is actively surfaced to consumers via agent-assisted recommendations.",
         5: "Consumers can self-serve and discover the right service automatically via agent-driven search.",
     }},
    {"id": "q08", "pillar_id": 2, "pillar_name": "Service Catalogue & Scope",
     "question": "Ownership & SLAs",
     "rubric": {
         1: "No clear owner or service-level expectation exists for what the pod delivers.",
         2: "Owners are informally known; SLAs are not documented or tracked.",
         3: "Each service has a named owner and a documented SLA.",
         4: "SLA adherence is tracked & reported automatically; agents flag breaches.",
         5: "SLAs are dynamically managed and optimised by agents based on demand & risk.",
     }},
    {"id": "q09", "pillar_id": 2, "pillar_name": "Service Catalogue & Scope",
     "question": "Currency & Maintenance",
     "rubric": {
         1: "Catalogue (if any) is rarely, if ever, updated.",
         2: "Catalogue is updated occasionally, through manual review cycles.",
         3: "Catalogue is reviewed & updated on a regular, defined cadence.",
         4: "Catalogue updates automatically as delivery activity changes.",
         5: "Catalogue continuously self-maintains with no manual update cycle needed.",
     }},
    {"id": "q10", "pillar_id": 2, "pillar_name": "Service Catalogue & Scope",
     "question": "Innovation & Expansion",
     "rubric": {
         1: "New services are added only through ad hoc requests, if at all.",
         2: "New services are added via a manual scoping/prioritisation process.",
         3: "New (incl. agentic) services follow a defined intake & assessment process.",
         4: "Agents actively identify and propose candidate new agentic services.",
         5: "New services are continuously generated, tested & retired by agents autonomously.",
     }},

    # ── Pillar 3: Organisation, Roles & Team Mix ─────────────────────────
    {"id": "q11", "pillar_id": 3, "pillar_name": "Organisation, Roles & Team Mix",
     "question": "Role Structure",
     "rubric": {
         1: "Full traditional role set (PO, BA, Architect, Devs, QA, Scrum, DevOps).",
         2: "Same roles retained, each individually AI-augmented.",
         3: "Roles begin to consolidate (e.g., PO/BA merge) as agents take on tasks.",
         4: "Roles shift toward Product Definer / Builder / Architect / AI Governance.",
         5: "Minimal core roles (2-3) oversee a largely autonomous agent workforce.",
     }},
    {"id": "q12", "pillar_id": 3, "pillar_name": "Organisation, Roles & Team Mix",
     "question": "Reporting & Hierarchy",
     "rubric": {
         1: "Traditional multi-layer hierarchy; all decisions flow through standard reporting.",
         2: "Hierarchy unchanged; AI tools support decision-making within existing layers.",
         3: "Hierarchy flattens slightly as agents absorb coordination/reporting tasks.",
         4: "Hierarchy is lean; agents handle most status reporting & coordination.",
         5: "Hierarchy is minimal; humans focus purely on strategic decisions.",
     }},
    {"id": "q13", "pillar_id": 3, "pillar_name": "Organisation, Roles & Team Mix",
     "question": "Human : Agent Ratio",
     "rubric": {
         1: "~80% human / 20% agent (roughly 9 humans : 2 agents).",
         2: "~60% human / 40% agent (roughly 8 humans : 6 agents).",
         3: "~38% human / 62% agent (roughly 6 humans : 12 agents).",
         4: "~22% human / 78% agent (roughly 4 humans : 18 agents).",
         5: "~10% human / 90% agent (roughly 3 humans : 21 agents).",
     }},
    {"id": "q14", "pillar_id": 3, "pillar_name": "Organisation, Roles & Team Mix",
     "question": "Role Accountability for Agents",
     "rubric": {
         1: "No one is formally accountable for agent behaviour or output.",
         2: "Individual humans are informally responsible for the AI tools they use.",
         3: "Defined roles (e.g., Tech Lead/QA Lead) own agent oversight & quality.",
         4: "A dedicated AI Governance role owns agent performance & compliance.",
         5: "Accountability is embedded in autonomous governance; humans set policy only.",
     }},
    {"id": "q15", "pillar_id": 3, "pillar_name": "Organisation, Roles & Team Mix",
     "question": "Scalability of Structure",
     "rubric": {
         1: "Structure is rigid; scaling requires proportional headcount growth.",
         2: "Structure can flex slightly by adding AI tools to existing roles.",
         3: "Structure can absorb more agent-driven work without major redesign.",
         4: "Structure is explicitly designed to scale via orchestrated agents.",
         5: "Structure scales elastically; agent capacity expands independent of headcount.",
     }},

    # ── Pillar 4: People Capability & AI Fluency ─────────────────────────
    {"id": "q16", "pillar_id": 4, "pillar_name": "People Capability & AI Fluency",
     "question": "AI / Prompt Literacy",
     "rubric": {
         1: "Little to no working knowledge of AI/prompting tools in the pod.",
         2: "Team can use prompting/copilot tools competently for individual tasks.",
         3: "Team writes advanced prompts/workflows to direct independent agents.",
         4: "Team designs prompt/agent chains for multi-agent orchestration.",
         5: "Team is fluent in agentic-native design patterns as a core skill.",
     }},
    {"id": "q17", "pillar_id": 4, "pillar_name": "People Capability & AI Fluency",
     "question": "Agent Configuration & Direction Skills",
     "rubric": {
         1: "No one in the pod can configure or direct an AI agent.",
         2: "A few individuals can configure basic AI assistants for their own use.",
         3: "Team can configure, direct & QA independent agents on defined tasks.",
         4: "Team can design & tune multi-agent orchestration workflows.",
         5: "Team operates as agent designers/architects across the delivery lifecycle.",
     }},
    {"id": "q18", "pillar_id": 4, "pillar_name": "People Capability & AI Fluency",
     "question": "Learning & Development Pathways",
     "rubric": {
         1: "No defined role/skill pathway exists for AI or agentic skills.",
         2: "Some ad hoc training resources exist; no formal pathway.",
         3: "Role/skill pathways are defined, with assigned training assets.",
         4: "Pathways include hands-on orchestration experience & mentoring.",
         5: "Pathways sustain a pipeline of frontier, agentic-native talent.",
     }},
    {"id": "q19", "pillar_id": 4, "pillar_name": "People Capability & AI Fluency",
     "question": "Talent Acquisition & Retention",
     "rubric": {
         1: "Hiring/retention criteria don't consider AI/agentic skills at all.",
         2: "Job specs mention AI familiarity as a nice-to-have.",
         3: "Hiring actively targets agent-configuration & AI-fluency skills.",
         4: "Hiring & retention are shaped around agentic-native role profiles.",
         5: "The pod attracts/retains frontier AI talent as a competitive differentiator.",
     }},
    {"id": "q20", "pillar_id": 4, "pillar_name": "People Capability & AI Fluency",
     "question": "Culture of Continuous Learning",
     "rubric": {
         1: "No visible culture of ongoing learning around AI/agentic ways of working.",
         2: "Learning happens reactively, individual-driven, with little reinforcement.",
         3: "Learning is actively encouraged & reinforced through team rituals.",
         4: "Continuous learning is embedded into how the pod operates day to day.",
         5: "Learning & experimentation with agentic methods is a cultural default.",
     }},

    # ── Pillar 5: Tooling & Agentic Platform ─────────────────────────────
    {"id": "q21", "pillar_id": 5, "pillar_name": "Tooling & Agentic Platform",
     "question": "Core Tooling Baseline",
     "rubric": {
         1: "Standard dev/collaboration tooling only; no AI or agent tooling present.",
         2: "AI copilots are available but bolted onto existing tools ad hoc.",
         3: "AI copilots are properly integrated into the core toolchain (IDE, tickets, docs).",
         4: "Tooling includes agent deployment & monitoring capability across the lifecycle.",
         5: "Tooling is a fully autonomous, self-monitoring agentic platform.",
     }},
    {"id": "q22", "pillar_id": 5, "pillar_name": "Tooling & Agentic Platform",
     "question": "AI Copilot Integration",
     "rubric": {
         1: "No copilots are used in the pod's daily tooling.",
         2: "Copilots are used inconsistently, dependent on individual preference.",
         3: "Copilots are standard practice, integrated into core workflows.",
         4: "Copilots are the default interface for most routine tasks.",
         5: "Copilot capability has evolved into autonomous agent execution.",
     }},
    {"id": "q23", "pillar_id": 5, "pillar_name": "Tooling & Agentic Platform",
     "question": "Agent Deployment & Monitoring",
     "rubric": {
         1: "No infrastructure exists to deploy or monitor agents.",
         2: "Basic sandbox/testing setups exist for experimenting with agents.",
         3: "Platform supports deploying & monitoring independent agents on standard tasks.",
         4: "Platform supports deploying orchestrated multi-agent workflows with monitoring.",
         5: "Platform autonomously deploys, monitors & self-heals agent workflows.",
     }},
    {"id": "q24", "pillar_id": 5, "pillar_name": "Tooling & Agentic Platform",
     "question": "Multi-Agent Orchestration",
     "rubric": {
         1: "No orchestration capability; agents (if any) operate in isolation.",
         2: "Simple, single-agent automations exist with no orchestration layer.",
         3: "Basic orchestration links a few agents for defined workflows.",
         4: "A dedicated orchestration platform runs agents across the full lifecycle.",
         5: "Orchestration is autonomous & self-optimising across the platform.",
     }},
    {"id": "q25", "pillar_id": 5, "pillar_name": "Tooling & Agentic Platform",
     "question": "Observability & Self-Healing",
     "rubric": {
         1: "No observability into AI/agent performance or failures.",
         2: "Basic logging exists; issues are found and fixed manually.",
         3: "Dashboards & alerts flag agent issues for human follow-up.",
         4: "Automated remediation handles common agent failures; humans handle the rest.",
         5: "Platform is self-healing with guardrails that catch & correct issues autonomously.",
     }},

    # ── Pillar 6: Governance, Risk & Change Management ───────────────────
    {"id": "q26", "pillar_id": 6, "pillar_name": "Governance, Risk & Change Management",
     "question": "AI / Agent Policy",
     "rubric": {
         1: "No formal AI or agent usage policy exists.",
         2: "A baseline AI usage policy exists but is not consistently applied.",
         3: "Policy is defined, communicated & applied across the pod.",
         4: "Policy adherence is actively monitored as part of daily operations.",
         5: "Policy is largely encoded as automated, enforced guardrails (policy-as-code).",
     }},
    {"id": "q27", "pillar_id": 6, "pillar_name": "Governance, Risk & Change Management",
     "question": "Guardrails & Escalation Paths",
     "rubric": {
         1: "No defined guardrails or escalation path for AI/agent issues.",
         2: "Informal escalation happens; guardrails are not documented.",
         3: "Guardrails & escalation paths are clearly defined and understood.",
         4: "Guardrails are actively enforced with automated escalation triggers.",
         5: "Guardrails are autonomous circuit-breakers requiring human approval only for exceptions.",
     }},
    {"id": "q28", "pillar_id": 6, "pillar_name": "Governance, Risk & Change Management",
     "question": "Risk & Compliance Management",
     "rubric": {
         1: "AI/agent-related risk is not actively tracked or managed.",
         2: "Risks are identified informally, with no structured tracking.",
         3: "A structured risk register/process covers AI & agent-related risk.",
         4: "Risk monitoring is continuous, with agents flagging emerging risk.",
         5: "Risk management is largely automated, with real-time compliance monitoring.",
     }},
    {"id": "q29", "pillar_id": 6, "pillar_name": "Governance, Risk & Change Management",
     "question": "Change Management & Adoption",
     "rubric": {
         1: "Change is not actively managed; adoption is left to individuals.",
         2: "Change is communicated top-down, with limited two-way engagement.",
         3: "A structured change/adoption plan exists for agentic ways of working.",
         4: "Change management continuously reinforces adoption through feedback loops.",
         5: "Agentic ways of working are the cultural norm; minimal active change effort needed.",
     }},
    {"id": "q30", "pillar_id": 6, "pillar_name": "Governance, Risk & Change Management",
     "question": "Culture & Communication",
     "rubric": {
         1: "Little to no communication about the pod's AI/agentic direction.",
         2: "Vision & plans are communicated, but reinforcement is inconsistent.",
         3: "Communication is regular and reinforces the AI/agentic vision.",
         4: "Communication loops include feedback & visible progress updates.",
         5: "AI/agentic vision is fully embedded in team culture & identity.",
     }},
]

SCORE_MAP = {"yes": 1.0, "partial": 0.5, "no": 0.0}


def _score_to_level(avg: float) -> int:
    """Convert a 1-5 average score to a maturity level."""
    if avg >= 4.5:
        return 5
    if avg >= 3.5:
        return 4
    if avg >= 2.5:
        return 3
    if avg >= 1.5:
        return 2
    return 1


def _score_to_band(level: int) -> str:
    return MATURITY_LEVELS.get(level, MATURITY_LEVELS[3])["band"]


def _level_label(level: int) -> str:
    return MATURITY_LEVELS.get(level, MATURITY_LEVELS[1])["label"]


def _calculate_maturity_from_responses(response_map: dict) -> dict:
    """Core maturity calculation. response_map: {question_id: score_int_1_5}."""
    pillar_scores = {}
    for q in ASSESSMENT_QUESTIONS:
        pid = q["pillar_id"]
        raw = response_map.get(q["id"])
        score = int(raw) if raw is not None and str(raw).isdigit() else 0
        if score < 1:
            score = 0
        pillar_scores.setdefault(pid, []).append(score)

    pillars = []
    for pdef in PILLARS:
        pid = pdef["id"]
        scores = pillar_scores.get(pid, [])
        answered_scores = [s for s in scores if s > 0]
        avg = sum(answered_scores) / len(answered_scores) if answered_scores else 0
        level = _score_to_level(avg) if answered_scores else 0
        pillars.append({
            "pillar_id": pid,
            "pillar_name": pdef["name"],
            "avg_score": round(avg, 2),
            "level": level,
            "level_label": _level_label(level) if level > 0 else "Not Assessed",
            "answered": len(answered_scores),
            "total": len(scores),
        })

    all_answered = [s for sl in pillar_scores.values() for s in sl if s > 0]
    overall_avg = sum(all_answered) / len(all_answered) if all_answered else 0
    overall_level = _score_to_level(overall_avg) if all_answered else 0

    return {
        "overall_score": round(overall_avg, 2),
        "overall_level": overall_level,
        "overall_label": _level_label(overall_level) if overall_level > 0 else "Not Assessed",
        "maturity_band": _score_to_band(overall_level) if overall_level > 0 else "N/A",
        "pillars": pillars,
        "total_questions": len(ASSESSMENT_QUESTIONS),
        "total_answered": len(all_answered),
    }


# ─── Pydantic models ─────────────────────────────────────────────────────────

class ResponseIn(BaseModel):
    question_id: str
    response: str = "0"
    notes: Optional[str] = None
    respondent: Optional[str] = None


class BulkResponseIn(BaseModel):
    responses: list[ResponseIn]
    product_group: Optional[str] = None
    product: Optional[str] = None
    team: Optional[str] = None


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/questions")
async def get_questions():
    return {"pillars": PILLARS, "questions": ASSESSMENT_QUESTIONS}


@router.get("/levels")
async def get_maturity_levels():
    return MATURITY_LEVELS


@router.get("/{project_id}/responses")
async def get_responses(
    project_id: str,
    team: Optional[str] = Query(None),
    product_group: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    conditions = [ManualAssessmentResponse.project_id == project_id]
    if team:
        conditions.append(ManualAssessmentResponse.team == team)
    if product_group:
        conditions.append(ManualAssessmentResponse.product_group == product_group)
    if product:
        conditions.append(ManualAssessmentResponse.product == product)
    result = await db.execute(
        select(ManualAssessmentResponse).where(and_(*conditions))
    )
    rows = result.scalars().all()
    return {
        r.question_id: {
            "response": r.response, "notes": r.notes, "respondent": r.respondent,
            "product_group": r.product_group, "product": r.product, "team": r.team,
        }
        for r in rows
    }


@router.post("/{project_id}/responses")
async def save_responses(project_id: str, body: BulkResponseIn, db: AsyncSession = Depends(get_db)):
    for r in body.responses:
        q = next((q for q in ASSESSMENT_QUESTIONS if q["id"] == r.question_id), None)
        if not q:
            continue
        conditions = [
            ManualAssessmentResponse.project_id == project_id,
            ManualAssessmentResponse.question_id == r.question_id,
        ]
        if body.team:
            conditions.append(ManualAssessmentResponse.team == body.team)
        else:
            conditions.append(ManualAssessmentResponse.team.is_(None))

        existing = await db.execute(select(ManualAssessmentResponse).where(and_(*conditions)))
        row = existing.scalar_one_or_none()
        if row:
            row.response = r.response
            row.notes = r.notes
            row.respondent = r.respondent
            row.product_group = body.product_group
            row.product = body.product
            row.updated_at = datetime.utcnow()
        else:
            db.add(ManualAssessmentResponse(
                project_id=project_id,
                phase_id=q["pillar_id"],
                question_id=r.question_id,
                response=r.response,
                notes=r.notes,
                respondent=r.respondent,
                product_group=body.product_group,
                product=body.product,
                team=body.team,
            ))
    await db.commit()
    return {"saved": len(body.responses)}


@router.get("/{project_id}/maturity")
async def calculate_maturity(
    project_id: str,
    team: Optional[str] = Query(None),
    product_group: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    conditions = [ManualAssessmentResponse.project_id == project_id]
    if team:
        conditions.append(ManualAssessmentResponse.team == team)
    if product_group:
        conditions.append(ManualAssessmentResponse.product_group == product_group)
    if product:
        conditions.append(ManualAssessmentResponse.product == product)

    result = await db.execute(select(ManualAssessmentResponse).where(and_(*conditions)))
    rows = result.scalars().all()
    response_map = {r.question_id: r.response for r in rows}
    maturity = _calculate_maturity_from_responses(response_map)
    maturity["team"] = team
    maturity["product_group"] = product_group
    maturity["product"] = product
    return maturity


@router.get("/{project_id}/teams")
async def list_assessed_teams(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            ManualAssessmentResponse.product_group,
            ManualAssessmentResponse.product,
            ManualAssessmentResponse.team,
        )
        .where(ManualAssessmentResponse.project_id == project_id)
        .distinct()
    )
    rows = result.all()
    return [
        {"product_group": r[0], "product": r[1], "team": r[2]}
        for r in rows
    ]


@router.get("/{project_id}/dashboard")
async def maturity_dashboard(project_id: str, db: AsyncSession = Depends(get_db)):
    """Portfolio-level maturity dashboard: maturity per team, heatmap data, aggregates."""
    result = await db.execute(
        select(ManualAssessmentResponse)
        .where(ManualAssessmentResponse.project_id == project_id)
    )
    all_rows = result.scalars().all()

    team_responses: dict[str, dict] = {}
    for r in all_rows:
        key = f"{r.product_group or ''}|{r.product or ''}|{r.team or ''}"
        if key not in team_responses:
            team_responses[key] = {
                "product_group": r.product_group, "product": r.product, "team": r.team,
                "responses": {},
            }
        team_responses[key]["responses"][r.question_id] = r.response

    team_maturity = []
    heatmap_data = []
    for key, info in team_responses.items():
        m = _calculate_maturity_from_responses(info["responses"])
        team_label = info["team"] or info["product"] or info["product_group"] or "Default"
        entry = {
            "team": team_label,
            "product_group": info["product_group"],
            "product": info["product"],
            "overall_level": m["overall_level"],
            "overall_label": m["overall_label"],
            "overall_score": m["overall_score"],
            "maturity_band": m["maturity_band"],
            "pillars": m["pillars"],
            "total_answered": m["total_answered"],
        }
        team_maturity.append(entry)
        for p in m["pillars"]:
            heatmap_data.append({
                "team": team_label,
                "product_group": info["product_group"],
                "product": info["product"],
                "pillar_id": p["pillar_id"],
                "pillar_name": p["pillar_name"],
                "level": p["level"],
                "level_label": p["level_label"],
                "score": p["avg_score"],
            })

    all_response_map = {r.question_id: r.response for r in all_rows}
    portfolio_maturity = _calculate_maturity_from_responses(all_response_map) if all_rows else None

    return {
        "teams": team_maturity,
        "heatmap": heatmap_data,
        "portfolio": portfolio_maturity,
        "maturity_levels": MATURITY_LEVELS,
        "total_teams": len(team_maturity),
    }


@router.post("/{project_id}/seed-demo")
async def seed_demo_teams(project_id: str, db: AsyncSession = Depends(get_db)):
    """Seed the two Rabobank tribe pod assessments as illustrative demo data."""
    DEMO_TEAMS = [
        {
            "product_group": "RetailNL Tech", "product": "Tribe APF", "team": "BeCloud",
            "assessor": "Rammurthy Mudaliar", "human_ftes": 24, "agents_active": 0,
            "scores": {
                "q01": 1, "q02": 2, "q03": 3, "q04": 2, "q05": 1,
                "q06": 1, "q07": 3, "q08": 3, "q09": 3, "q10": 2,
                "q11": 2, "q12": 2, "q13": 1, "q14": 1, "q15": 2,
                "q16": 3, "q17": 2, "q18": 3, "q19": 3, "q20": 4,
                "q21": 3, "q22": 3, "q23": 2, "q24": 2, "q25": 1,
                "q26": 2, "q27": 1, "q28": 2, "q29": 4, "q30": 3,
            },
        },
        {
            "product_group": "RetailNL Tech", "product": "Tribe Payments", "team": "PARN",
            "assessor": "Jagannathan Jayaraaman", "human_ftes": 20, "agents_active": 0,
            "scores": {
                "q01": 1, "q02": 2, "q03": 3, "q04": 3, "q05": 1,
                "q06": 1, "q07": 3, "q08": 3, "q09": 3, "q10": 2,
                "q11": 2, "q12": 2, "q13": 1, "q14": 1, "q15": 2,
                "q16": 3, "q17": 2, "q18": 3, "q19": 3, "q20": 4,
                "q21": 3, "q22": 3, "q23": 2, "q24": 2, "q25": 1,
                "q26": 2, "q27": 1, "q28": 2, "q29": 4, "q30": 3,
            },
        },
    ]

    count = 0
    for team_info in DEMO_TEAMS:
        for qid, score in team_info["scores"].items():
            q = next((q for q in ASSESSMENT_QUESTIONS if q["id"] == qid), None)
            if not q:
                continue
            conditions = [
                ManualAssessmentResponse.project_id == project_id,
                ManualAssessmentResponse.question_id == qid,
                ManualAssessmentResponse.team == team_info["team"],
            ]
            existing = await db.execute(select(ManualAssessmentResponse).where(and_(*conditions)))
            row = existing.scalar_one_or_none()
            if row:
                row.response = str(score)
                row.respondent = team_info["assessor"]
                row.product_group = team_info["product_group"]
                row.product = team_info["product"]
                row.updated_at = datetime.utcnow()
            else:
                db.add(ManualAssessmentResponse(
                    project_id=project_id,
                    phase_id=q["pillar_id"],
                    question_id=qid,
                    response=str(score),
                    respondent=team_info["assessor"],
                    product_group=team_info["product_group"],
                    product=team_info["product"],
                    team=team_info["team"],
                ))
            count += 1

    await db.commit()
    return {
        "seeded": count,
        "teams": len(DEMO_TEAMS),
        "team_list": [
            {"product_group": t["product_group"], "product": t["product"], "team": t["team"],
             "assessor": t["assessor"], "human_ftes": t["human_ftes"], "agents_active": t["agents_active"]}
            for t in DEMO_TEAMS
        ],
    }
